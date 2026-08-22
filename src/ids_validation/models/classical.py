"""Stage 16 duplicate-safe classical benchmark registries and toy helpers."""

from __future__ import annotations

from collections.abc import Mapping, Sequence

import numpy as np


BASELINE_SEED = 42
BASELINE_CANDIDATES = (
    "LOGISTIC_REGRESSION",
    "GAUSSIAN_NAIVE_BAYES",
    "K_NEAREST_NEIGHBORS",
    "LINEAR_SVM",
    "DECISION_TREE",
    "RANDOM_FOREST",
    "EXTRA_TREES",
    "ADABOOST",
    "GRADIENT_BOOSTING",
    "XGBOOST",
    "LIGHTGBM",
    "CATBOOST",
)
SCALED_CANDIDATES = (
    "LOGISTIC_REGRESSION",
    "GAUSSIAN_NAIVE_BAYES",
    "K_NEAREST_NEIGHBORS",
    "LINEAR_SVM",
)
RAW_CANDIDATES = tuple(candidate for candidate in BASELINE_CANDIDATES if candidate not in SCALED_CANDIDATES)
TOP5_TUNING_CANDIDATES = ("XGBOOST", "LIGHTGBM", "CATBOOST", "K_NEAREST_NEIGHBORS", "RANDOM_FOREST")
CONFIGURATIONS_PER_TUNING_CANDIDATE = 12
CONFIRMATION_CANDIDATES = ("LIGHTGBM", "XGBOOST", "RANDOM_FOREST")
CONFIRMATION_SEEDS = (7, 29, 101, 313, 997)
FINAL_STRATEGY_ID = "ENS_LGBM_XGB_EQUAL"
FINAL_MEMBERS = ("LIGHTGBM", "XGBOOST")
FINAL_WEIGHTS = (0.5, 0.5)
FINAL_THRESHOLD = 0.46
CLASS_WEIGHTING_POLICY = {
    "global_weighting": None,
    "candidate_specific_only": True,
    "final_lightgbm": None,
    "final_xgboost": None,
    "confirmation_random_forest": None,
}


def threshold_grid() -> np.ndarray:
    """Return the exact Stage 16 validation threshold grid.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 194, 197, 203, 207, 211, 213
    Original stage: Stage 16
    Frozen artifacts generated: results/stage16_classical_benchmark_checkpoint/stage16_2b_baseline_selection_lock.json
    Notes: Integer construction 50..950 by 5 divided by 1000 yields 181 thresholds and avoids floating-step ambiguity.
    """

    return np.arange(50, 951, 5, dtype=np.int64) / 1000.0


def select_validation_threshold(rows: Sequence[Mapping[str, float]]) -> Mapping[str, float]:
    """Apply the frozen Stage 16 validation-only threshold tie chain.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 194, 197, 207, 213
    Original stage: Stage 16
    Frozen artifacts generated: results/stage16_classical_benchmark_checkpoint/stage16_5c_final_classical_strategy_lock.json
    Notes: Synthetic/static helper only; no stage entry point accepts scientific probabilities or performs threshold selection.
    """

    if not rows:
        raise ValueError("rows must not be empty")
    return min(rows, key=lambda row: (-row["f1"], -row["f2"], -row["recall"], row["fpr"], row["threshold"]))


def equal_weight_lightgbm_xgboost(lightgbm: Sequence[float], xgboost: Sequence[float]) -> np.ndarray:
    """Combine two caller-supplied toy vectors using the frozen 0.5/0.5 rule.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 211, 213, 215, 218, 220, 221
    Original stage: Stage 16
    Frozen artifacts generated: results/stage16_classical_benchmark_checkpoint/stage16_5c_final_classical_strategy_lock.json
    Notes: This arithmetic helper neither loads models nor generates scientific component probabilities.
    """

    first = np.asarray(lightgbm, dtype=np.float64)
    second = np.asarray(xgboost, dtype=np.float64)
    if first.shape != second.shape:
        raise ValueError("component probability vectors must have identical shapes")
    return 0.5 * first + 0.5 * second
