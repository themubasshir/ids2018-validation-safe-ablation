"""Stage 17 frozen-attention analysis formulas for toy or static inputs only."""

from __future__ import annotations

from collections.abc import Iterable, Sequence

import numpy as np


CHECKPOINT_SEEDS = (7, 29, 101, 313, 997)
CONFUSION_STATES = ("TP", "TN", "FP", "FN")
TOP_K_VALUES = (5, 10, 20)


def evenly_spaced_positions(group_size: int, count: int = 16) -> np.ndarray:
    """Return the deterministic Stage 17 panel ranks.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 225
    Original stage: Stage 17.1
    Frozen artifacts generated: stage17_1_selected_cases.csv
    Notes: Group members were first ordered by absolute threshold margin and validation-row position.
    """

    if group_size < count or count <= 0:
        raise ValueError("group_size must be at least the positive requested count")
    return np.floor(np.linspace(0, group_size - 1, count)).astype(np.int64)


def direct_cls_feature_attention(attention: Sequence[Sequence[float]]) -> np.ndarray:
    """Remove CLS self-attention and renormalize its 70 feature-key weights.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 225
    Original stage: Stage 17.1
    Frozen artifacts generated: stage17_1_attention_arrays.npz
    Notes: Input is one square 71-token attention matrix; this helper performs no model loading or inference.
    """

    matrix = np.asarray(attention, dtype=np.float64)
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1] or matrix.shape[0] < 2:
        raise ValueError("attention must be a square matrix containing CLS and feature tokens")
    feature_weights = matrix[0, 1:].copy()
    total = float(feature_weights.sum())
    if total <= 0:
        raise ValueError("CLS-to-feature attention must have a positive sum")
    return feature_weights / total


def normalized_entropy(weights: Sequence[float]) -> float:
    """Calculate Shannon entropy normalized by log(feature count).

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 225, 230
    Original stage: Stage 17.1–17.2
    Frozen artifacts generated: stage17_1_attention_arrays.npz, stage17_2_layer_head_entropy_summary.csv
    Notes: Zero-probability terms contribute zero after feature renormalization.
    """

    array = np.asarray(weights, dtype=np.float64).reshape(-1)
    if len(array) < 2 or np.any(array < 0):
        raise ValueError("weights must contain at least two non-negative values")
    total = float(array.sum())
    if total <= 0:
        raise ValueError("weights must have a positive sum")
    probabilities = array / total
    positive = probabilities > 0
    return float(-np.sum(probabilities[positive] * np.log(probabilities[positive])) / np.log(len(probabilities)))


def attention_rollout(attention_by_layer_and_head: Sequence[Sequence[Sequence[Sequence[float]]]]) -> np.ndarray:
    """Apply the locked Stage 17 residual attention-rollout rule.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 225
    Original stage: Stage 17.1
    Frozen artifacts generated: stage17_1_attention_arrays.npz
    Notes: Expected axes are layer, head, query token, key token. This pure NumPy helper cannot access a checkpoint.
    """

    attentions = np.asarray(attention_by_layer_and_head, dtype=np.float64)
    if attentions.ndim != 4 or attentions.shape[2] != attentions.shape[3] or attentions.shape[2] < 2:
        raise ValueError("attention must have shape [layers, heads, tokens, tokens]")
    token_count = attentions.shape[2]
    rollout = np.eye(token_count, dtype=np.float64)
    identity = np.eye(token_count, dtype=np.float64)
    for layer in attentions:
        residual_attention = np.mean(layer, axis=0) + identity
        row_sums = residual_attention.sum(axis=1, keepdims=True)
        if np.any(row_sums <= 0):
            raise ValueError("every residual-attention row must have a positive sum")
        rollout = (residual_attention / row_sums) @ rollout
    cls_features = rollout[0, 1:]
    total = float(cls_features.sum())
    if total <= 0:
        raise ValueError("final CLS rollout must assign positive mass to feature tokens")
    return cls_features / total


def deterministic_top_indices(values: Sequence[float], k: int) -> np.ndarray:
    """Rank descending values with ascending feature position as the tie-break.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 230, 235
    Original stage: Stage 17.2–17.3
    Frozen artifacts generated: stage17_2_global_rollout_feature_ranking.csv, stage17_3b_topk_overlap_detail.csv
    """

    array = np.asarray(values, dtype=np.float64).reshape(-1)
    if k < 0:
        raise ValueError("k must be non-negative")
    positions = np.arange(len(array))
    return np.lexsort((positions, -array))[:k]


def cosine_similarity(first: Sequence[float], second: Sequence[float]) -> float:
    """Calculate cosine similarity for two frozen-method vectors."""

    left = np.asarray(first, dtype=np.float64).reshape(-1)
    right = np.asarray(second, dtype=np.float64).reshape(-1)
    if left.shape != right.shape:
        raise ValueError("vectors must have identical shapes")
    denominator = float(np.linalg.norm(left) * np.linalg.norm(right))
    return float("nan") if denominator == 0 else float(np.dot(left, right) / denominator)


def jaccard_similarity(first: Iterable[int], second: Iterable[int]) -> float:
    """Calculate top-k Jaccard similarity, returning NaN for an empty union."""

    left = {int(value) for value in first}
    right = {int(value) for value in second}
    union = left | right
    return float("nan") if not union else float(len(left & right) / len(union))
