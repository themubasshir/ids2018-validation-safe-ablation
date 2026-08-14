"""Stage21 near-parameter-matched masked Vision Transformer.

Frozen by Stage21-0 before any Stage21 model training or real-data forward pass.

Input:
    image:        float32 [B,1,64,256], byte values divided by 255
    padding_mask: bool    [B,1,64,256], True only for authentic retained bytes

The padding mask is auxiliary only:
- padded pixels are forced to zero before patch projection;
- a patch is valid iff it contains >=1 authentic pixel;
- invalid patch tokens are zero-gated;
- invalid patch tokens are excluded as attention keys;
- the mask is not concatenated as an input feature channel.

No external/pretrained weights are used.
"""

from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.functional as F


IMAGE_ROWS = 64
IMAGE_COLS = 256

PATCH_ROWS = 8
PATCH_COLS = 16
PATCH_DIM = PATCH_ROWS * PATCH_COLS

GRID_ROWS = IMAGE_ROWS // PATCH_ROWS
GRID_COLS = IMAGE_COLS // PATCH_COLS
NUM_PATCHES = GRID_ROWS * GRID_COLS

EMBED_DIM = 64
NUM_HEADS = 4
HEAD_DIM = EMBED_DIM // NUM_HEADS
DEPTH = 2
MLP_DIM = 160

CLASSIFIER_DROPOUT = 0.25


def _gate_tokens(
    x: torch.Tensor,
    patch_valid: torch.Tensor,
) -> torch.Tensor:
    """Keep CLS; zero every invalid patch token exactly."""

    cls = x[:, :1, :]

    patches = (
        x[:, 1:, :]
        *
        patch_valid.unsqueeze(-1).to(dtype=x.dtype)
    )

    return torch.cat(
        (cls, patches),
        dim=1,
    )


class Stage21SelfAttention(nn.Module):
    """Explicit deterministic multi-head self-attention."""

    def __init__(self) -> None:
        super().__init__()

        self.qkv = nn.Linear(
            EMBED_DIM,
            3 * EMBED_DIM,
            bias=True,
        )

        self.out = nn.Linear(
            EMBED_DIM,
            EMBED_DIM,
            bias=True,
        )

    def forward(
        self,
        x: torch.Tensor,
        key_valid: torch.Tensor,
    ) -> torch.Tensor:

        b, n, d = x.shape

        qkv = self.qkv(x).reshape(
            b,
            n,
            3,
            NUM_HEADS,
            HEAD_DIM,
        )

        q, k, v = qkv.unbind(dim=2)

        q = q.transpose(1, 2)
        k = k.transpose(1, 2)
        v = v.transpose(1, 2)

        logits = (
            torch.matmul(
                q,
                k.transpose(-2, -1),
            )
            *
            (HEAD_DIM ** -0.5)
        )

        logits = logits.masked_fill(
            ~key_valid[:, None, None, :],
            float("-inf"),
        )

        attn = torch.softmax(
            logits,
            dim=-1,
        )

        out = torch.matmul(
            attn,
            v,
        )

        out = (
            out.transpose(1, 2)
            .contiguous()
            .reshape(
                b,
                n,
                d,
            )
        )

        return self.out(out)


class Stage21ViTBlock(nn.Module):
    """Pre-LN Transformer encoder block."""

    def __init__(self) -> None:
        super().__init__()

        self.norm1 = nn.LayerNorm(
            EMBED_DIM,
            eps=1e-5,
        )

        self.attn = Stage21SelfAttention()

        self.norm2 = nn.LayerNorm(
            EMBED_DIM,
            eps=1e-5,
        )

        self.fc1 = nn.Linear(
            EMBED_DIM,
            MLP_DIM,
            bias=True,
        )

        self.fc2 = nn.Linear(
            MLP_DIM,
            EMBED_DIM,
            bias=True,
        )

    def forward(
        self,
        x: torch.Tensor,
        key_valid: torch.Tensor,
        patch_valid: torch.Tensor,
    ) -> torch.Tensor:

        x = (
            x
            +
            self.attn(
                self.norm1(x),
                key_valid,
            )
        )

        x = _gate_tokens(
            x,
            patch_valid,
        )

        y = self.fc2(
            F.gelu(
                self.fc1(
                    self.norm2(x)
                ),
                approximate="none",
            )
        )

        x = x + y

        x = _gate_tokens(
            x,
            patch_valid,
        )

        return x


class Stage21MaskedViTv1(nn.Module):
    """Frozen Stage21 single-candidate ViT."""

    def __init__(self) -> None:
        super().__init__()

        self.patch_proj = nn.Linear(
            PATCH_DIM,
            EMBED_DIM,
            bias=True,
        )

        self.cls_token = nn.Parameter(
            torch.empty(
                1,
                1,
                EMBED_DIM,
            )
        )

        self.pos_embed = nn.Parameter(
            torch.empty(
                1,
                NUM_PATCHES + 1,
                EMBED_DIM,
            )
        )

        self.blocks = nn.ModuleList(
            [
                Stage21ViTBlock()
                for _ in range(DEPTH)
            ]
        )

        self.final_norm = nn.LayerNorm(
            EMBED_DIM,
            eps=1e-5,
        )

        self.dropout = nn.Dropout(
            CLASSIFIER_DROPOUT,
        )

        self.head = nn.Linear(
            EMBED_DIM,
            1,
            bias=True,
        )

        self.reset_parameters()

    def reset_parameters(self) -> None:

        nn.init.xavier_uniform_(
            self.patch_proj.weight
        )
        nn.init.zeros_(
            self.patch_proj.bias
        )

        nn.init.normal_(
            self.cls_token,
            mean=0.0,
            std=0.02,
        )

        nn.init.normal_(
            self.pos_embed,
            mean=0.0,
            std=0.02,
        )

        for block in self.blocks:

            nn.init.ones_(
                block.norm1.weight
            )
            nn.init.zeros_(
                block.norm1.bias
            )

            nn.init.ones_(
                block.norm2.weight
            )
            nn.init.zeros_(
                block.norm2.bias
            )

            nn.init.xavier_uniform_(
                block.attn.qkv.weight
            )
            nn.init.zeros_(
                block.attn.qkv.bias
            )

            nn.init.xavier_uniform_(
                block.attn.out.weight
            )
            nn.init.zeros_(
                block.attn.out.bias
            )

            nn.init.xavier_uniform_(
                block.fc1.weight
            )
            nn.init.zeros_(
                block.fc1.bias
            )

            nn.init.xavier_uniform_(
                block.fc2.weight
            )
            nn.init.zeros_(
                block.fc2.bias
            )

        nn.init.ones_(
            self.final_norm.weight
        )
        nn.init.zeros_(
            self.final_norm.bias
        )

        nn.init.xavier_uniform_(
            self.head.weight
        )
        nn.init.zeros_(
            self.head.bias
        )

    @staticmethod
    def _patchify(
        x: torch.Tensor,
    ) -> torch.Tensor:

        b, c, h, w = x.shape

        if (
            c,
            h,
            w,
        ) != (
            1,
            IMAGE_ROWS,
            IMAGE_COLS,
        ):
            raise ValueError(
                "expected "
                f"[B,1,{IMAGE_ROWS},{IMAGE_COLS}], "
                f"got {tuple(x.shape)}"
            )

        x = x.reshape(
            b,
            1,
            GRID_ROWS,
            PATCH_ROWS,
            GRID_COLS,
            PATCH_COLS,
        )

        x = x.permute(
            0,
            2,
            4,
            1,
            3,
            5,
        ).contiguous()

        return x.reshape(
            b,
            NUM_PATCHES,
            PATCH_DIM,
        )

    def forward(
        self,
        image: torch.Tensor,
        padding_mask: torch.Tensor,
    ) -> torch.Tensor:

        if (
            image.ndim != 4
            or
            padding_mask.ndim != 4
        ):
            raise ValueError(
                "image and padding_mask must be rank-4"
            )

        if image.shape != padding_mask.shape:
            raise ValueError(
                "image and padding_mask shapes must match"
            )

        if image.shape[1:] != (
            1,
            IMAGE_ROWS,
            IMAGE_COLS,
        ):
            raise ValueError(
                "expected "
                f"[B,1,{IMAGE_ROWS},{IMAGE_COLS}]"
            )

        if image.dtype != torch.float32:
            raise ValueError(
                "image must be float32"
            )

        if padding_mask.dtype != torch.bool:
            raise ValueError(
                "padding_mask must be bool"
            )

        authentic = (
            image
            *
            padding_mask.to(
                dtype=image.dtype
            )
        )

        patch_pixels = self._patchify(
            authentic
        )

        patch_mask = (
            self._patchify(
                padding_mask.to(
                    dtype=torch.float32
                )
            )
            >
            0.5
        )

        patch_valid = patch_mask.any(
            dim=-1
        )

        tokens = self.patch_proj(
            patch_pixels
        )

        tokens = (
            tokens
            *
            patch_valid.unsqueeze(-1).to(
                dtype=tokens.dtype
            )
        )

        cls = self.cls_token.expand(
            image.shape[0],
            -1,
            -1,
        )

        x = torch.cat(
            (
                cls,
                tokens,
            ),
            dim=1,
        )

        x = x + self.pos_embed

        x = _gate_tokens(
            x,
            patch_valid,
        )

        cls_valid = torch.ones(
            (
                image.shape[0],
                1,
            ),
            dtype=torch.bool,
            device=image.device,
        )

        key_valid = torch.cat(
            (
                cls_valid,
                patch_valid,
            ),
            dim=1,
        )

        for block in self.blocks:
            x = block(
                x,
                key_valid,
                patch_valid,
            )

        cls_out = self.final_norm(
            x[:, 0, :]
        )

        logits = self.head(
            self.dropout(
                cls_out
            )
        ).squeeze(-1)

        return logits


def count_trainable_parameters(
    model: nn.Module,
) -> int:
    return sum(
        int(p.numel())
        for p in model.parameters()
        if p.requires_grad
    )
