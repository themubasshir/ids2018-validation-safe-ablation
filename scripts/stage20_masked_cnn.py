"""Stage20 frozen masked 2D-CNN architecture.

Architecture freeze:
    Stage20-1E0

Representation:
    Stage20-1D0 / Stage20-1D3 / Stage20-1D4-B

The packet-byte image remains one channel. The Boolean padding mask is a
separate auxiliary tensor used only for deterministic gating and masked global
average pooling; it is not a second packet-byte channel.
"""

from __future__ import annotations

import torch
from torch import nn
from torch.nn import functional as F


ROWS = 64
COLS = 256
IMAGE_CHANNELS = 1

MODEL_NAME = "Stage20MaskedCNNv1"
EXPECTED_TRAINABLE_PARAMETERS = 93025


class Stage20MaskedCNNv1(nn.Module):
    """Single pre-registered masked CNN for the Stage20 packet-image branch."""

    def __init__(self) -> None:
        super().__init__()

        self.conv1 = nn.Conv2d(
            1,
            32,
            kernel_size=3,
            stride=1,
            padding=1,
            bias=False,
        )
        self.norm1 = nn.GroupNorm(
            8,
            32,
        )

        self.conv2 = nn.Conv2d(
            32,
            64,
            kernel_size=3,
            stride=1,
            padding=1,
            bias=False,
        )
        self.norm2 = nn.GroupNorm(
            8,
            64,
        )

        self.conv3 = nn.Conv2d(
            64,
            128,
            kernel_size=3,
            stride=1,
            padding=1,
            bias=False,
        )
        self.norm3 = nn.GroupNorm(
            8,
            128,
        )

        self.dropout = nn.Dropout(
            p=0.25,
        )

        self.classifier = nn.Linear(
            128,
            1,
            bias=True,
        )

        self.reset_parameters()

    def reset_parameters(self) -> None:
        """Frozen initialization family; caller freezes the RNG seed."""

        for conv in (
            self.conv1,
            self.conv2,
            self.conv3,
        ):
            nn.init.kaiming_normal_(
                conv.weight,
                mode="fan_out",
                nonlinearity="relu",
            )

        for norm in (
            self.norm1,
            self.norm2,
            self.norm3,
        ):
            nn.init.ones_(
                norm.weight,
            )
            nn.init.zeros_(
                norm.bias,
            )

        nn.init.xavier_uniform_(
            self.classifier.weight,
        )
        nn.init.zeros_(
            self.classifier.bias,
        )

    @staticmethod
    def _pool_mask(
        mask: torch.Tensor,
    ) -> torch.Tensor:
        return F.max_pool2d(
            mask,
            kernel_size=2,
            stride=2,
        )

    @staticmethod
    def _validate_inputs(
        image: torch.Tensor,
        padding_mask: torch.Tensor,
    ) -> None:
        if image.ndim != 4:
            raise ValueError(
                f"image must be NCHW, got ndim={image.ndim}"
            )

        if padding_mask.ndim != 4:
            raise ValueError(
                f"padding_mask must be NCHW, got ndim={padding_mask.ndim}"
            )

        if tuple(image.shape[1:]) != (
            1,
            ROWS,
            COLS,
        ):
            raise ValueError(
                f"expected image shape [N,1,{ROWS},{COLS}], "
                f"got {tuple(image.shape)}"
            )

        if tuple(padding_mask.shape) != tuple(
            image.shape
        ):
            raise ValueError(
                "padding_mask must have the same NCHW shape as image"
            )

    def forward(
        self,
        image: torch.Tensor,
        padding_mask: torch.Tensor,
    ) -> torch.Tensor:
        """Return one binary-classification logit per flow."""

        self._validate_inputs(
            image,
            padding_mask,
        )

        x = image.to(
            dtype=torch.float32,
        )

        m = padding_mask.to(
            dtype=x.dtype,
        )

        # Frozen storage-to-model scaling.
        x = x / 255.0

        # Padding mask is an auxiliary gating tensor, not an image channel.
        x = x * m

        x = self.conv1(x)
        x = self.norm1(x)
        x = F.relu(
            x,
            inplace=False,
        )
        x = F.max_pool2d(
            x,
            kernel_size=2,
            stride=2,
        )
        m = self._pool_mask(m)
        x = x * m

        x = self.conv2(x)
        x = self.norm2(x)
        x = F.relu(
            x,
            inplace=False,
        )
        x = F.max_pool2d(
            x,
            kernel_size=2,
            stride=2,
        )
        m = self._pool_mask(m)
        x = x * m

        x = self.conv3(x)
        x = self.norm3(x)
        x = F.relu(
            x,
            inplace=False,
        )
        x = F.max_pool2d(
            x,
            kernel_size=2,
            stride=2,
        )
        m = self._pool_mask(m)
        x = x * m

        denominator = m.sum(
            dim=(2, 3),
        ).clamp_min(
            1.0,
        )

        pooled = (
            (x * m).sum(
                dim=(2, 3),
            )
            /
            denominator
        )

        pooled = self.dropout(
            pooled
        )

        logits = self.classifier(
            pooled
        ).squeeze(
            1
        )

        return logits


def count_trainable_parameters(
    model: nn.Module,
) -> int:
    return int(
        sum(
            parameter.numel()
            for parameter in model.parameters()
            if parameter.requires_grad
        )
    )
