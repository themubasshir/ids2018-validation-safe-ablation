# Frozen Stage 19.3 model definition.
# SingleScaleTemporalTransformer control.
# Do not modify for any Stage 19.3 seed.

import math

import torch
import torch.nn as nn


SEQ_LEN = 60
INPUT_DIM = 80

D_MODEL = 64
N_HEADS = 4
N_LAYERS = 2
D_FF = 128
DROPOUT = 0.10


def relative_sinusoidal_encoding(
    seq_len,
    d_model,
):
    """
    Deterministic relative lag encoding.

    Token lags:
        -(seq_len-1), ..., -1, 0

    The final/current token therefore has lag 0.
    """

    lag = torch.arange(
        -(seq_len - 1),
        1,
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
        seq_len,
        d_model,
        dtype=torch.float32,
    )

    pe[:, 0::2] = torch.sin(
        lag
        * div_term
    )

    pe[:, 1::2] = torch.cos(
        lag
        * div_term
    )

    return pe


class SingleScaleTemporalTransformer(
    nn.Module
):

    def __init__(
        self,
    ):

        super().__init__()


        self.input_projection = nn.Linear(
            INPUT_DIM,
            D_MODEL,
        )


        self.register_buffer(
            "relative_position_encoding",
            relative_sinusoidal_encoding(
                SEQ_LEN,
                D_MODEL,
            ).unsqueeze(0),
            persistent=True,
        )


        causal_mask = torch.triu(
            torch.ones(
                SEQ_LEN,
                SEQ_LEN,
                dtype=torch.bool,
            ),
            diagonal=1,
        )


        self.register_buffer(
            "causal_mask",
            causal_mask,
            persistent=True,
        )


        encoder_layer = (
            nn.TransformerEncoderLayer(
                d_model=D_MODEL,
                nhead=N_HEADS,
                dim_feedforward=D_FF,
                dropout=DROPOUT,
                activation="gelu",
                batch_first=True,
                norm_first=True,
            )
        )


        self.encoder = nn.TransformerEncoder(
            encoder_layer,
            num_layers=N_LAYERS,
        )


        self.final_norm = nn.LayerNorm(
            D_MODEL
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
        x,
    ):

        if x.ndim != 3:

            raise ValueError(
                "input must be [batch, 60, 80]"
            )


        if x.shape[1:] != (
            SEQ_LEN,
            INPUT_DIM,
        ):

            raise ValueError(
                "unexpected temporal input shape"
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


        current_state = (
            self.final_norm(
                h[:, -1, :]
            )
        )


        logits = (
            self.classifier(
                current_state
            )
            .squeeze(-1)
        )


        return logits
