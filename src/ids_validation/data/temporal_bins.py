"""Stage 19 train-frozen preprocessing and causal toy-window helpers."""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np


BASE_FEATURE_COUNT = 78
TOKEN_FEATURE_COUNT = 80
WARMUP_SECONDS = 1200
FINE_TOKEN_SECONDS = 1
FINE_TOKEN_COUNT = 60
MEDIUM_TOKEN_SECONDS = 15
MEDIUM_TOKEN_COUNT = 20
COARSE_TOKEN_SECONDS = 60
COARSE_TOKEN_COUNT = 20


def standardize_base(
    feature_mean_raw: Sequence[Sequence[float]],
    train_impute_mean: Sequence[float],
    train_scale: Sequence[float],
) -> np.ndarray:
    """Apply caller-supplied TRAIN means/scales to second-level toy features.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 300
    Original stage: Stage 19.2B
    Frozen artifacts generated: stage19_2b_window_constructor.py, stage19_2b_train_only_scaler.npz
    Notes: Non-finite values are imputed with TRAIN means, so fully empty bins map to standardized zero.
    """

    values = np.asarray(feature_mean_raw, dtype=np.float64)
    means = np.asarray(train_impute_mean, dtype=np.float64)
    scales = np.asarray(train_scale, dtype=np.float64)
    if values.ndim != 2 or values.shape[1] != BASE_FEATURE_COUNT:
        raise ValueError("feature_mean_raw must have 78 columns")
    if means.shape != (BASE_FEATURE_COUNT,) or scales.shape != (BASE_FEATURE_COUNT,):
        raise ValueError("TRAIN preprocessing vectors must contain 78 values")
    if np.any(scales <= 0):
        raise ValueError("TRAIN scales must be positive")
    standardized = (np.where(np.isfinite(values), values, means) - means) / scales
    if not np.all(np.isfinite(standardized)):
        raise ValueError("standardized values must be finite")
    return standardized.astype(np.float32)


def _append_activity(base_tokens: np.ndarray, flow_count: np.ndarray) -> np.ndarray:
    log_count = np.log1p(flow_count).astype(np.float32)
    occupied = (flow_count > 0).astype(np.float32)
    return np.concatenate([base_tokens.astype(np.float32), log_count[:, None], occupied[:, None]], axis=1).astype(np.float32)


def construct_multiscale(
    base_standardized: Sequence[Sequence[float]],
    flow_count: Sequence[int],
    target_local_index: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Construct one fine/medium/coarse causal sample from toy arrays.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 300
    Original stage: Stage 19.2B
    Frozen artifacts generated: stage19_2b_window_constructor.py, stage19_2b_temporal_index_manifest.csv
    Notes: All branches end at the current second; no future, cross-day, or cross-partition context is accessed.
    """

    base = np.asarray(base_standardized, dtype=np.float32)
    counts = np.asarray(flow_count, dtype=np.int64)
    target = int(target_local_index)
    if base.ndim != 2 or base.shape[1] != BASE_FEATURE_COUNT or counts.shape != (len(base),):
        raise ValueError("base and flow-count shapes do not match the 78-feature protocol")
    if target < WARMUP_SECONDS or target >= len(base):
        raise ValueError("target must follow the frozen 20-minute warmup and remain in the source day")

    fine_base = base[target - 59 : target + 1]
    fine_count = counts[target - 59 : target + 1]
    medium_base = base[target - 299 : target + 1].reshape(20, 15, 78).mean(axis=1, dtype=np.float32)
    medium_count = counts[target - 299 : target + 1].reshape(20, 15).sum(axis=1, dtype=np.int64)
    coarse_base = base[target - 1199 : target + 1].reshape(20, 60, 78).mean(axis=1, dtype=np.float32)
    coarse_count = counts[target - 1199 : target + 1].reshape(20, 60).sum(axis=1, dtype=np.int64)

    fine = _append_activity(fine_base, fine_count)
    medium = _append_activity(medium_base, medium_count)
    coarse = _append_activity(coarse_base, coarse_count)
    if fine.shape != (60, 80) or medium.shape != (20, 80) or coarse.shape != (20, 80):
        raise RuntimeError("invalid Stage 19 temporal token shape")
    return fine, medium, coarse


def construct_fine_only(
    base_standardized: Sequence[Sequence[float]],
    flow_count: Sequence[int],
    target_local_index: int,
) -> np.ndarray:
    """Return the frozen single-scale control's fine branch for toy arrays."""

    fine, _, _ = construct_multiscale(base_standardized, flow_count, target_local_index)
    return fine
