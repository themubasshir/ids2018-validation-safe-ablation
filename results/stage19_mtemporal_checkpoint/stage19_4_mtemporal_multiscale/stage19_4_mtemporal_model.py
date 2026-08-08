
# Frozen Stage 19.4 MTemporal-IDS definition.

import math

import torch
import torch.nn as nn


INPUT_DIM = 80

D_MODEL = 64

N_HEADS = 4

N_LAYERS = 2

D_FF = 128

DROPOUT = 0.10


FINE_END_LAGS = list(
    range(-59, 1, 1)
)

MEDIUM_END_LAGS = list(
    range(-285, 1, 15)
)

COARSE_END_LAGS = list(
    range(-1140, 1, 60)
)


def temporal_sinusoidal_encoding(
    lag_seconds,
    d_model,
):
    """
    Deterministic relative temporal encoding using actual
    token-end lag in seconds relative to prediction time.
    """

    lag = torch.tensor(
        lag_seconds,
        dtype=torch.float32,
    ).unsqueeze(1)


    div_term = torch.exp(
        torch.arange(
            0,
            d_model,
            2,
            dtype=torch.float32,
        )
        * (
            -math.log(10000.0)
            / d_model
        )
    )


    pe = torch.zeros(
        len(lag_seconds),
        d_model,
        dtype=torch.float32,
    )


    pe[:, 0::2] = torch.sin(
        lag * div_term
    )


    pe[:, 1::2] = torch.cos(
        lag * div_term
    )


    return pe


class TemporalBranch(
    nn.Module
):

    def __init__(
        self,
        lag_seconds,
    ):

        super().__init__()


        self.seq_len = len(
            lag_seconds
        )


        self.input_projection = nn.Linear(
            INPUT_DIM,
            D_MODEL,
        )


        self.register_buffer(
            "relative_position_encoding",
            temporal_sinusoidal_encoding(
                lag_seconds,
                D_MODEL,
            ).unsqueeze(0),
            persistent=True,
        )


        causal_mask = torch.triu(
            torch.ones(
                self.seq_len,
                self.seq_len,
                dtype=torch.bool,
            ),
            diagonal=1,
        )


        self.register_buffer(
            "causal_mask",
            causal_mask,
            persistent=True,
        )


        encoder_layer = nn.TransformerEncoderLayer(
            d_model=D_MODEL,
            nhead=N_HEADS,
            dim_feedforward=D_FF,
            dropout=DROPOUT,
            activation="gelu",
            batch_first=True,
            norm_first=True,
        )


        self.encoder = nn.TransformerEncoder(
            encoder_layer,
            num_layers=N_LAYERS,
        )


        self.final_norm = nn.LayerNorm(
            D_MODEL
        )


    def forward(
        self,
        x,
    ):

        if x.ndim != 3:
            raise ValueError(
                "branch input must be 3-D"
            )


        if x.shape[1] != self.seq_len:
            raise ValueError(
                "branch sequence length mismatch"
            )


        if x.shape[2] != INPUT_DIM:
            raise ValueError(
                "branch input dimension mismatch"
            )


        h = self.input_projection(
            x
        )


        h = (
            h
            +
            self.relative_position_encoding
        )


        h = self.encoder(
            h,
            mask=self.causal_mask,
        )


        summary = self.final_norm(
            h[:, -1, :]
        )


        return summary


class MTemporalIDS(
    nn.Module
):

    def __init__(
        self,
    ):

        super().__init__()


        self.fine_branch = TemporalBranch(
            FINE_END_LAGS
        )


        self.medium_branch = TemporalBranch(
            MEDIUM_END_LAGS
        )


        self.coarse_branch = TemporalBranch(
            COARSE_END_LAGS
        )


        self.scale_gate = nn.Sequential(

            nn.Linear(
                3 * D_MODEL,
                D_MODEL,
            ),

            nn.GELU(),

            nn.Linear(
                D_MODEL,
                3,
            ),
        )


        self.classifier = nn.Sequential(

            nn.Linear(
                D_MODEL,
                D_MODEL,
            ),

            nn.GELU(),

            nn.Dropout(
                DROPOUT
            ),

            nn.Linear(
                D_MODEL,
                1,
            ),
        )


    def forward(
        self,
        fine,
        medium,
        coarse,
        return_gate=False,
    ):

        fine_summary = self.fine_branch(
            fine
        )


        medium_summary = self.medium_branch(
            medium
        )


        coarse_summary = self.coarse_branch(
            coarse
        )


        concatenated = torch.cat(
            [
                fine_summary,
                medium_summary,
                coarse_summary,
            ],
            dim=1,
        )


        gate_logits = self.scale_gate(
            concatenated
        )


        gate_weights = torch.softmax(
            gate_logits,
            dim=1,
        )


        stacked = torch.stack(
            [
                fine_summary,
                medium_summary,
                coarse_summary,
            ],
            dim=1,
        )


        fused = torch.sum(
            stacked
            *
            gate_weights.unsqueeze(-1),
            dim=1,
        )


        logits = (
            self.classifier(
                fused
            )
            .squeeze(-1)
        )


        if return_gate:
            return (
                logits,
                gate_weights,
            )


        return logits
