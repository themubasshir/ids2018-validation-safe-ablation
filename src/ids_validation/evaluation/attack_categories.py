"""Stage 11 attack-category analysis helpers for static and toy verification."""

from __future__ import annotations

import math
from collections.abc import Sequence
from statistics import NormalDist

import numpy as np


RANDOM_STATE = 42
CATEGORY_BOOTSTRAP_REPLICATES = 1_000
CONFIDENCE_LEVEL = 0.95
MINIMUM_SUPPORT_FOR_RANKING = 20
MINIMUM_SUPPORT_FOR_LABELLED_FIGURES = 20

ATTACK_CATEGORIES = (
    "Bot",
    "Brute Force -Web",
    "Brute Force -XSS",
    "DDOS attack-HOIC",
    "DDOS attack-LOIC-UDP",
    "DoS attacks-GoldenEye",
    "DoS attacks-Hulk",
    "DoS attacks-SlowHTTPTest",
    "DoS attacks-Slowloris",
    "FTP-BruteForce",
    "Infilteration",
    "SQL Injection",
)

FROZEN_SUPPORT_COUNTS = {
    "Bot": 3_998,
    "Brute Force -Web": 134,
    "Brute Force -XSS": 50,
    "DDOS attack-HOIC": 3_970,
    "DDOS attack-LOIC-UDP": 75,
    "DoS attacks-GoldenEye": 3_141,
    "DoS attacks-Hulk": 347,
    "DoS attacks-SlowHTTPTest": 3_721,
    "DoS attacks-Slowloris": 820,
    "FTP-BruteForce": 3_950,
    "Infilteration": 3_967,
    "SQL Injection": 13,
}

OPERATING_POINTS = {
    "xgboost_balanced": {"Model": "XGBoost Tuned", "Threshold": 0.51},
    "xgboost_security": {"Model": "XGBoost Tuned", "Threshold": 0.27},
    "lightgbm_balanced": {"Model": "LightGBM Tuned", "Threshold": 0.50},
    "lightgbm_security": {"Model": "LightGBM Tuned", "Threshold": 0.26},
}


def normalize_original_labels(labels: Sequence[object]) -> np.ndarray:
    """Strip labels and collapse internal whitespace without changing case.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 120
    Original stage: Stage 11
    Frozen artifacts generated: results/attack_category/attack_category_support_summary.csv
    Notes: The normalized lowercase copy is used only to identify benign rows; original stripped spelling defines the category taxonomy.
    """

    return np.asarray([" ".join(str(label).strip().split()) for label in labels], dtype=object)


def reconstruct_binary_labels(labels: Sequence[object]) -> np.ndarray:
    """Reconstruct the historical binary target as non-benign versus benign.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 120
    Original stage: Stage 11
    Frozen artifacts generated: results/attack_category/holdout_attack_category_prediction_manifest.csv
    Notes: This helper is for toy/static verification; extraction never calls it on the scientific holdout.
    """

    normalized = normalize_original_labels(labels)
    return np.asarray([label.lower() != "benign" for label in normalized], dtype=np.int8)


def support_status(support: int, minimum_support: int = MINIMUM_SUPPORT_FOR_RANKING) -> str:
    """Label support using the notebook's frozen hardest-category cutoff.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 120
    Original stage: Stage 11
    Frozen artifacts generated: results/attack_category/hardest_attack_categories.csv
    Notes: The status adds no new threshold: cell 120 explicitly uses minimum support 20 for ranking and labelled figures.
    """

    if support < 0:
        raise ValueError("support must be non-negative")
    return "RANKING_ELIGIBLE" if support >= minimum_support else "LOW_SUPPORT"


def category_support(labels: Sequence[object], binary_labels: Sequence[int]) -> list[dict[str, int | str]]:
    """Count sorted attack categories while retaining exact stripped spellings.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 120
    Original stage: Stage 11
    Frozen artifacts generated: results/attack_category/attack_category_support_summary.csv
    Notes: Toy grouping helper only; no taxonomy smoothing, merging, or scientific holdout reconstruction occurs.
    """

    original = normalize_original_labels(labels)
    targets = np.asarray(binary_labels, dtype=np.int8).reshape(-1)
    if len(original) != len(targets):
        raise ValueError("labels and binary_labels must have equal length")
    rows = []
    for category in sorted(set(original[targets == 1])):
        support = int(np.sum((original == category) & (targets == 1)))
        rows.append({"Attack Category": str(category), "Support": support, "Support Status": support_status(support)})
    return rows


def wilson_interval(successes: int, total: int, confidence_level: float = CONFIDENCE_LEVEL) -> tuple[float, float]:
    """Calculate the exact Stage 11 Wilson score interval.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 120
    Original stage: Stage 11
    Frozen artifacts generated: results/attack_category/attack_category_operating_point_metrics.csv
    Notes: NormalDist supplies the same standard-normal quantile used historically through scipy.stats.norm.ppf.
    """

    if total == 0:
        return (math.nan, math.nan)
    if total < 0 or successes < 0 or successes > total:
        raise ValueError("successes must be between zero and total")
    z_value = NormalDist().inv_cdf(1 - (1 - confidence_level) / 2)
    proportion = successes / total
    denominator = 1 + z_value**2 / total
    centre = (proportion + z_value**2 / (2 * total)) / denominator
    margin = z_value / denominator * math.sqrt(proportion * (1 - proportion) / total + z_value**2 / (4 * total**2))
    return (max(0.0, centre - margin), min(1.0, centre + margin))


def paired_bootstrap_detection_difference(
    first_predictions: Sequence[int | float],
    second_predictions: Sequence[int | float],
    seed: int,
    *,
    replicates: int = CATEGORY_BOOTSTRAP_REPLICATES,
) -> tuple[float, float]:
    """Return the Stage 11 paired percentile interval for a detection-rate difference.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 120
    Original stage: Stage 11
    Frozen artifacts generated: results/attack_category/paired_xgboost_*_vs_lightgbm_security.csv
    Notes: Defaults to 1,000 replicates; tests may pass a small count on synthetic arrays only. Scientific target data are never accepted by an entry point.
    """

    first = np.asarray(first_predictions, dtype=np.float64).reshape(-1)
    second = np.asarray(second_predictions, dtype=np.float64).reshape(-1)
    if len(first) != len(second):
        raise ValueError("paired predictions must have equal length")
    if len(first) == 0:
        return (math.nan, math.nan)
    if replicates <= 0:
        raise ValueError("replicates must be positive")
    rng = np.random.default_rng(seed)
    differences = np.empty(replicates, dtype=np.float64)
    for replicate_index in range(replicates):
        sampled_positions = rng.integers(0, len(first), size=len(first))
        differences[replicate_index] = np.mean(first[sampled_positions]) - np.mean(second[sampled_positions])
    return (float(np.percentile(differences, 2.5)), float(np.percentile(differences, 97.5)))


def benjamini_hochberg(p_values: Sequence[float]) -> np.ndarray:
    """Apply the Stage 11 Benjamini-Hochberg FDR adjustment.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 120
    Original stage: Stage 11
    Frozen artifacts generated: results/attack_category/paired_xgboost_*_vs_lightgbm_security.csv
    Notes: Exact static helper; no significance tests are recomputed on scientific predictions.
    """

    values = np.asarray(p_values, dtype=np.float64)
    count = len(values)
    if count == 0:
        return values.copy()
    order = np.argsort(values)
    ranked = values[order]
    adjusted_ranked = ranked * count / np.arange(1, count + 1)
    adjusted_ranked = np.minimum.accumulate(adjusted_ranked[::-1])[::-1]
    adjusted = np.empty_like(adjusted_ranked)
    adjusted[order] = np.clip(adjusted_ranked, 0, 1)
    return adjusted
