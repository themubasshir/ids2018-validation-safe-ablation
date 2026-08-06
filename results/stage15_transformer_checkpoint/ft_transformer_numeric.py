
from __future__ import annotations

import math

import torch
from torch import nn


class NumericalFeatureTokenizer(nn.Module):
    """
    Converts each scalar numerical feature into a feature-specific
    token. Feature identity is represented by feature-specific
    parameters rather than positional or sequential encodings.
    """

    def __init__(
        self,
        n_features: int,
        d_token: int,
    ) -> None:
        super().__init__()

        if n_features < 1:
            raise ValueError(
                "n_features must be positive."
            )

        if d_token < 1:
            raise ValueError(
                "d_token must be positive."
            )

        self.n_features = int(n_features)
        self.d_token = int(d_token)

        self.weight = nn.Parameter(
            torch.empty(
                self.n_features,
                self.d_token,
            )
        )

        self.bias = nn.Parameter(
            torch.empty(
                self.n_features,
                self.d_token,
            )
        )

        self.reset_parameters()

    def reset_parameters(self) -> None:
        bound = 1.0 / math.sqrt(
            self.d_token
        )

        nn.init.uniform_(
            self.weight,
            -bound,
            bound,
        )

        nn.init.uniform_(
            self.bias,
            -bound,
            bound,
        )

    def forward(
        self,
        x: torch.Tensor,
    ) -> torch.Tensor:

        if x.ndim != 2:
            raise ValueError(
                "Expected x with shape "
                "(batch_size, n_features)."
            )

        if x.shape[1] != self.n_features:
            raise ValueError(
                "Input feature count does not match "
                "the tokenizer configuration."
            )

        return (
            x.unsqueeze(-1)
            * self.weight.unsqueeze(0)
            + self.bias.unsqueeze(0)
        )


class NumericFTTransformer(nn.Module):
    """
    FT-Transformer-style binary classifier for numerical tabular
    features.

    No temporal, spatial, or sequential positional encoding is used.
    """

    def __init__(
        self,
        n_features: int,
        d_token: int = 64,
        n_heads: int = 8,
        n_layers: int = 3,
        d_ff: int = 256,
        dropout: float = 0.1,
    ) -> None:
        super().__init__()

        if d_token % n_heads != 0:
            raise ValueError(
                "d_token must be divisible by n_heads."
            )

        self.n_features = int(n_features)
        self.d_token = int(d_token)

        self.tokenizer = NumericalFeatureTokenizer(
            n_features=self.n_features,
            d_token=self.d_token,
        )

        self.cls_token = nn.Parameter(
            torch.empty(
                1,
                1,
                self.d_token,
            )
        )

        nn.init.normal_(
            self.cls_token,
            mean=0.0,
            std=0.02,
        )

        encoder_layer = nn.TransformerEncoderLayer(
            d_model=self.d_token,
            nhead=int(n_heads),
            dim_feedforward=int(d_ff),
            dropout=float(dropout),
            activation="gelu",
            batch_first=True,
            norm_first=True,
        )

        try:
            self.encoder = nn.TransformerEncoder(
                encoder_layer,
                num_layers=int(n_layers),
                enable_nested_tensor=False,
            )
        except TypeError:
            self.encoder = nn.TransformerEncoder(
                encoder_layer,
                num_layers=int(n_layers),
            )

        self.output_norm = nn.LayerNorm(
            self.d_token
        )

        self.output_head = nn.Linear(
            self.d_token,
            1,
        )

    def forward(
        self,
        x: torch.Tensor,
    ) -> torch.Tensor:

        tokens = self.tokenizer(x)

        cls_tokens = self.cls_token.expand(
            x.shape[0],
            -1,
            -1,
        )

        tokens = torch.cat(
            [
                cls_tokens,
                tokens,
            ],
            dim=1,
        )

        encoded = self.encoder(tokens)

        cls_representation = self.output_norm(
            encoded[:, 0]
        )

        logits = self.output_head(
            cls_representation
        ).squeeze(-1)

        return logits
