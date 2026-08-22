"""Safety-gated Stage 15 FT-Transformer architecture definition."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


FROZEN_CANDIDATE_ID = "FT_BALANCED"
CONFIRMATION_SEEDS = (7, 29, 101, 313, 997)
FROZEN_THRESHOLD = 0.73
EXPECTED_PARAMETER_COUNT = 159_169


@dataclass(frozen=True)
class FTTransformerConfiguration:
    """Frozen Stage 15 FT_BALANCED architecture and optimizer settings."""

    n_features: int = 70
    d_token: int = 64
    n_heads: int = 8
    n_layers: int = 3
    d_ff: int = 256
    dropout: float = 0.1
    learning_rate: float = 0.0005
    weight_decay: float = 0.00001
    batch_size: int = 1024
    maximum_epochs: int = 70
    early_stopping_patience: int = 6
    gradient_clip_norm: float = 1.0


FROZEN_CONFIGURATION = FTTransformerConfiguration()


def expected_parameter_count(configuration: FTTransformerConfiguration = FROZEN_CONFIGURATION) -> int:
    """Calculate the exact trainable-parameter count without importing PyTorch.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 165, 174, 183, 185
    Original stage: Stage 15
    Frozen artifacts generated: results/stage15_transformer_checkpoint/stage15_2_architecture_config.json, results/stage15_transformer_checkpoint/stage15_4c_frozen_architecture.json
    Notes: Covers the numerical tokenizer, CLS token, TransformerEncoder layers, output LayerNorm, and one-logit head.
    """

    config = configuration
    tokenizer = 2 * config.n_features * config.d_token
    cls_token = config.d_token
    attention = 4 * config.d_token * config.d_token + 4 * config.d_token
    feed_forward = 2 * config.d_token * config.d_ff + config.d_ff + config.d_token
    layer_norms = 4 * config.d_token
    encoder = config.n_layers * (attention + feed_forward + layer_norms)
    output = 2 * config.d_token + config.d_token + 1
    return tokenizer + cls_token + encoder + output


def load_numeric_ft_transformer_class() -> type[Any]:
    """Return the checkpoint-compatible historical model class via a lazy import.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 165, 174, 175, 178, 180, 183, 184, 188
    Original stage: Stage 15
    Frozen artifacts generated: results/stage15_transformer_checkpoint/ft_transformer_numeric.py and locked .pt checkpoints
    Notes: Merely calling this function imports PyTorch and defines the architecture. Stage entry points never call it, never instantiate the class, and never load checkpoints.
    """

    import math

    import torch
    from torch import nn

    class NumericalFeatureTokenizer(nn.Module):
        def __init__(self, n_features: int, d_token: int) -> None:
            super().__init__()
            if n_features < 1 or d_token < 1:
                raise ValueError("n_features and d_token must be positive")
            self.n_features = int(n_features)
            self.d_token = int(d_token)
            self.weight = nn.Parameter(torch.empty(self.n_features, self.d_token))
            self.bias = nn.Parameter(torch.empty(self.n_features, self.d_token))
            self.reset_parameters()

        def reset_parameters(self) -> None:
            bound = 1.0 / math.sqrt(self.d_token)
            nn.init.uniform_(self.weight, -bound, bound)
            nn.init.uniform_(self.bias, -bound, bound)

        def forward(self, x: Any) -> Any:
            if x.ndim != 2 or x.shape[1] != self.n_features:
                raise ValueError("Expected x with shape (batch_size, n_features)")
            return x.unsqueeze(-1) * self.weight.unsqueeze(0) + self.bias.unsqueeze(0)

    class NumericFTTransformer(nn.Module):
        """FT-Transformer-style binary classifier for numerical tabular features."""

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
                raise ValueError("d_token must be divisible by n_heads")
            self.n_features = int(n_features)
            self.d_token = int(d_token)
            self.tokenizer = NumericalFeatureTokenizer(self.n_features, self.d_token)
            self.cls_token = nn.Parameter(torch.empty(1, 1, self.d_token))
            nn.init.normal_(self.cls_token, mean=0.0, std=0.02)
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
                self.encoder = nn.TransformerEncoder(encoder_layer, num_layers=int(n_layers), enable_nested_tensor=False)
            except TypeError:
                self.encoder = nn.TransformerEncoder(encoder_layer, num_layers=int(n_layers))
            self.output_norm = nn.LayerNorm(self.d_token)
            self.output_head = nn.Linear(self.d_token, 1)

        def forward(self, x: Any) -> Any:
            tokens = self.tokenizer(x)
            cls_tokens = self.cls_token.expand(x.shape[0], -1, -1)
            encoded = self.encoder(torch.cat([cls_tokens, tokens], dim=1))
            return self.output_head(self.output_norm(encoded[:, 0])).squeeze(-1)

    NumericFTTransformer.__name__ = "NumericFTTransformer"
    NumericFTTransformer.__qualname__ = "NumericFTTransformer"
    return NumericFTTransformer


def build_numeric_ft_transformer(configuration: FTTransformerConfiguration = FROZEN_CONFIGURATION) -> Any:
    """Construct, but never train or load, the frozen Stage 15 architecture.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 165, 174, 175, 178, 180, 183, 184, 188
    Original stage: Stage 15
    Frozen artifacts generated: results/stage15_transformer_checkpoint/stage15_4c_models/*.pt
    Notes: This explicit opt-in helper performs architecture construction only. No optimizer, checkpoint, data, inference, or fit operation is attached.
    """

    model_class = load_numeric_ft_transformer_class()
    return model_class(
        n_features=configuration.n_features,
        d_token=configuration.d_token,
        n_heads=configuration.n_heads,
        n_layers=configuration.n_layers,
        d_ff=configuration.d_ff,
        dropout=configuration.dropout,
    )
