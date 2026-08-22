"""Static Stage 20 masked-CNN architecture declaration.

Importing this module constructs no PyTorch object and cannot deserialize the
frozen checkpoint.  It records architecture metadata only.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ConvolutionBlockSpec:
    """One frozen convolution, normalization, activation, and pooling block."""

    input_channels: int
    output_channels: int
    kernel_size: int = 3
    group_norm_groups: int = 8
    pool_size: int = 2


@dataclass(frozen=True)
class MaskedCNNSpec:
    """Metadata for the sole precommitted Stage20MaskedCNNv1 candidate."""

    name: str
    input_shape: tuple[int, int, int]
    blocks: tuple[ConvolutionBlockSpec, ...]
    aggregation: str
    dropout: float
    classifier_input: int
    trainable_parameters: int


MASKED_CNN_SPEC = MaskedCNNSpec(
    name="Stage20MaskedCNNv1",
    input_shape=(1, 64, 256),
    blocks=(
        ConvolutionBlockSpec(1, 32),
        ConvolutionBlockSpec(32, 64),
        ConvolutionBlockSpec(64, 128),
    ),
    aggregation="MASKED_GLOBAL_AVERAGE_POOLING",
    dropout=0.25,
    classifier_input=128,
    trainable_parameters=93_025,
)
