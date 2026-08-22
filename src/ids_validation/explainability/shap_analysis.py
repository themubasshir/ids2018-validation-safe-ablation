"""Stage 6 dual-model TreeSHAP methodology with no implicit execution path."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

import numpy as np


RANDOM_STATE = 42
BENIGN_SAMPLE_SIZE = 2_500
ATTACK_SAMPLE_SIZE = 2_500
TOTAL_SAMPLE_SIZE = BENIGN_SAMPLE_SIZE + ATTACK_SAMPLE_SIZE
TOP_FEATURE_COUNT = 20
XGB_THRESHOLD = 0.51
LGBM_THRESHOLD = 0.26

SHAP_ARTIFACT_SCHEMAS = {
    "shared_shap_sample_manifest.csv": (
        "Test Position",
        "True Label",
        "XGBoost Attack Probability",
        "LightGBM Attack Probability",
    ),
    "xgboost_shap_top20_features.csv": (
        "Display Rank",
        "Feature",
        "XGBoost Mean Absolute SHAP",
        "XGBoost Normalized Importance",
        "XGBoost Rank",
    ),
    "lightgbm_shap_top20_features.csv": (
        "Display Rank",
        "Feature",
        "LightGBM Mean Absolute SHAP",
        "LightGBM Normalized Importance",
        "LightGBM Rank",
    ),
    "xgboost_lightgbm_shap_global_comparison.csv": (
        "Feature",
        "XGBoost Mean Absolute SHAP",
        "LightGBM Mean Absolute SHAP",
        "XGBoost Normalized Importance",
        "LightGBM Normalized Importance",
        "XGBoost Rank",
        "LightGBM Rank",
        "Absolute Rank Difference",
    ),
    "xgboost_lightgbm_top20_overlap.csv": (
        "Feature",
        "XGBoost Mean Absolute SHAP",
        "LightGBM Mean Absolute SHAP",
        "XGBoost Normalized Importance",
        "LightGBM Normalized Importance",
        "XGBoost Rank",
        "LightGBM Rank",
        "Absolute Rank Difference",
        "In XGBoost Top 20",
        "In LightGBM Top 20",
        "Shared Top 20",
    ),
}


def select_shared_sample_indices(
    labels: np.ndarray,
    *,
    benign_sample_size: int = BENIGN_SAMPLE_SIZE,
    attack_sample_size: int = ATTACK_SAMPLE_SIZE,
    random_state: int = RANDOM_STATE,
) -> np.ndarray:
    """Select and shuffle the exact Stage 6 class-balanced explanation sample.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 108
    Original stage: Stage 6
    Frozen artifacts generated: results/shap/shared_shap_sample_manifest.csv
    Notes: Uses default_rng, choice without replacement per class, concatenation, then in-place shuffle.
    """

    labels = np.asarray(labels, dtype=np.int32).reshape(-1)
    rng = np.random.default_rng(random_state)
    benign_indices = np.where(labels == 0)[0]
    attack_indices = np.where(labels == 1)[0]
    selected_benign = rng.choice(benign_indices, size=benign_sample_size, replace=False)
    selected_attack = rng.choice(attack_indices, size=attack_sample_size, replace=False)
    sample_indices = np.concatenate([selected_benign, selected_attack])
    rng.shuffle(sample_indices)
    return sample_indices


def extract_binary_shap_values(model: Any, features: np.ndarray) -> tuple[Any, np.ndarray, float]:
    """Construct TreeExplainer and normalize historical binary-output shapes.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 108
    Original stage: Stage 6
    Frozen artifacts generated: results/shap/xgboost_shap_values.npy, results/shap/lightgbm_shap_values.npy
    Notes: Calling this function performs SHAP computation; safety-gated entry points never call it. SHAP version is VERSION_NOT_PROVEN.
    """

    import shap

    explainer = shap.TreeExplainer(model)
    try:
        raw_values = explainer.shap_values(features, check_additivity=False)
    except TypeError:
        raw_values = explainer.shap_values(features)

    if isinstance(raw_values, list):
        values = np.asarray(raw_values[-1])
    elif hasattr(raw_values, "values"):
        values = np.asarray(raw_values.values)
    else:
        values = np.asarray(raw_values)

    if values.ndim == 3:
        if values.shape[-1] == 2:
            values = values[:, :, 1]
        elif values.shape[0] == 2:
            values = values[1]
    if values.shape != features.shape:
        raise ValueError(f"Unexpected SHAP matrix shape. Expected {features.shape}; received {values.shape}.")

    expected_array = np.asarray(explainer.expected_value).reshape(-1)
    return explainer, values, float(expected_array[-1])


def select_representative_attack(labels: np.ndarray, probabilities: np.ndarray, threshold: float) -> int:
    """Select the highest-probability correctly detected attack, with fallback.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 108
    Original stage: Stage 6
    Frozen artifacts generated: figures/xgboost_shap_attack_waterfall.png, figures/lightgbm_shap_attack_waterfall.png
    Notes: The fallback is the highest-probability attack when none meets the frozen threshold.
    """

    labels = np.asarray(labels).reshape(-1)
    probabilities = np.asarray(probabilities).reshape(-1)
    correctly_detected = np.where((labels == 1) & (probabilities >= threshold))[0]
    if len(correctly_detected) > 0:
        return int(correctly_detected[np.argmax(probabilities[correctly_detected])])
    attack_positions = np.where(labels == 1)[0]
    return int(attack_positions[np.argmax(probabilities[attack_positions])])


def rank_min_descending(values: Sequence[float]) -> np.ndarray:
    """Reproduce pandas descending rank(method='min') for finite values.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 108
    Original stage: Stage 6
    Frozen artifacts generated: results/shap/xgboost_lightgbm_shap_global_comparison.csv
    Notes: This dependency-light helper is for static/toy equivalence checks, not SHAP recomputation.
    """

    array = np.asarray(values, dtype=np.float64)
    return np.asarray([1 + int(np.sum(array > value)) for value in array], dtype=np.int64)


def build_global_importance_records(
    feature_names: Sequence[str],
    xgb_shap_values: np.ndarray,
    lgbm_shap_values: np.ndarray,
) -> list[dict[str, Any]]:
    """Build Stage 6 mean-absolute, normalized, rank-comparison records.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 108
    Original stage: Stage 6
    Frozen artifacts generated: results/shap/xgboost_lightgbm_shap_global_comparison.csv
    Notes: Intended for toy/static checks in this phase; entry points never load saved SHAP matrices.
    """

    xgb_mean = np.mean(np.abs(np.asarray(xgb_shap_values)), axis=0)
    lgbm_mean = np.mean(np.abs(np.asarray(lgbm_shap_values)), axis=0)
    if len(feature_names) != len(xgb_mean) or len(feature_names) != len(lgbm_mean):
        raise ValueError("Feature-name and SHAP column counts differ")
    xgb_ranks = rank_min_descending(xgb_mean)
    lgbm_ranks = rank_min_descending(lgbm_mean)
    rows = [
        {
            "Feature": str(feature),
            "XGBoost Mean Absolute SHAP": float(xgb_mean[index]),
            "LightGBM Mean Absolute SHAP": float(lgbm_mean[index]),
            "XGBoost Normalized Importance": float(xgb_mean[index] / np.sum(xgb_mean)),
            "LightGBM Normalized Importance": float(lgbm_mean[index] / np.sum(lgbm_mean)),
            "XGBoost Rank": int(xgb_ranks[index]),
            "LightGBM Rank": int(lgbm_ranks[index]),
            "Absolute Rank Difference": int(abs(xgb_ranks[index] - lgbm_ranks[index])),
        }
        for index, feature in enumerate(feature_names)
    ]
    return sorted(rows, key=lambda row: (row["XGBoost Rank"], row["LightGBM Rank"]))


def top_feature_overlap(records: Sequence[dict[str, Any]], top_k: int = TOP_FEATURE_COUNT) -> dict[str, Any]:
    """Calculate the historical top-k union, intersection, and Jaccard value.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 108
    Original stage: Stage 6
    Frozen artifacts generated: results/shap/xgboost_lightgbm_top20_overlap.csv, metadata/dual_model_shap_metadata.json
    Notes: Ties use the already-materialized minimum ranks and rank ordering.
    """

    xgb_top = {row["Feature"] for row in sorted(records, key=lambda row: row["XGBoost Rank"])[:top_k]}
    lgbm_top = {row["Feature"] for row in sorted(records, key=lambda row: row["LightGBM Rank"])[:top_k]}
    shared = xgb_top & lgbm_top
    union = xgb_top | lgbm_top
    return {"xgboost": xgb_top, "lightgbm": lgbm_top, "shared": shared, "union": union, "jaccard": len(shared) / len(union)}
