"""Stage 8 paired class-stratified percentile-bootstrap methodology."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

import numpy as np


N_BOOTSTRAP = 2_000
RANDOM_STATE = 42
CONFIDENCE_LEVEL = 0.95
LOWER_PERCENTILE = 100 * (1.0 - CONFIDENCE_LEVEL) / 2
UPPER_PERCENTILE = 100 * (1 - (1.0 - CONFIDENCE_LEVEL) / 2)

OPERATING_POINTS = {
    "xgboost_standard": {"Model": "XGBoost Tuned", "Objective": "Standard Reference", "Threshold": 0.50},
    "xgboost_balanced": {"Model": "XGBoost Tuned", "Objective": "Maximum Validation F1", "Threshold": 0.51},
    "xgboost_security": {"Model": "XGBoost Tuned", "Objective": "Constrained Maximum F2", "Threshold": 0.27},
    "lightgbm_balanced": {"Model": "LightGBM Tuned", "Objective": "Maximum Validation F1", "Threshold": 0.50},
    "lightgbm_security": {"Model": "LightGBM Tuned", "Objective": "Constrained Maximum F2", "Threshold": 0.26},
}

RATE_METRICS = ("Accuracy", "Precision", "Recall", "F1-score", "F2-score", "FPR", "FNR", "Specificity", "ROC-AUC", "PR-AUC")
COUNT_METRICS = ("TP", "TN", "FP", "FN")


def safe_divide(numerator: float | int, denominator: float | int) -> float:
    """Apply the Stage 8 zero-denominator convention.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 116
    Original stage: Stage 8
    Frozen artifacts generated: results/statistical_confidence/bootstrap_point_estimates.csv
    Notes: Returns 0.0 when the denominator is zero.
    """

    if denominator == 0:
        return 0.0
    return float(numerator / denominator)


def calculate_threshold_metrics(
    labels: np.ndarray,
    probabilities: np.ndarray,
    threshold: float,
    roc_auc: float,
    pr_auc: float,
) -> dict[str, float | int]:
    """Calculate one frozen-operating-point Stage 8 metric record.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 116
    Original stage: Stage 8
    Frozen artifacts generated: results/statistical_confidence/bootstrap_point_estimates.csv, results/statistical_confidence/bootstrap_replicates.npz
    Notes: ROC-AUC and PR-AUC are explicit inputs because their historical calculation used scikit-learn 1.6.1.
    """

    labels = np.asarray(labels).reshape(-1)
    probabilities = np.asarray(probabilities).reshape(-1)
    predictions = probabilities >= threshold
    labels_positive = labels == 1
    labels_negative = labels == 0
    tp = int(np.sum(predictions & labels_positive))
    tn = int(np.sum((~predictions) & labels_negative))
    fp = int(np.sum(predictions & labels_negative))
    fn = int(np.sum((~predictions) & labels_positive))
    precision = safe_divide(tp, tp + fp)
    recall = safe_divide(tp, tp + fn)
    f1 = safe_divide(2 * precision * recall, precision + recall)
    f2 = safe_divide(5 * precision * recall, 4 * precision + recall)
    fpr = safe_divide(fp, fp + tn)
    fnr = safe_divide(fn, fn + tp)
    specificity = safe_divide(tn, tn + fp)
    accuracy = safe_divide(tp + tn, tp + tn + fp + fn)
    return {
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1-score": f1,
        "F2-score": f2,
        "FPR": fpr,
        "FNR": fnr,
        "Specificity": specificity,
        "ROC-AUC": float(roc_auc),
        "PR-AUC": float(pr_auc),
        "TP": tp,
        "TN": tn,
        "FP": fp,
        "FN": fn,
    }


def generate_replicate_seeds(n_bootstrap: int = N_BOOTSTRAP, random_state: int = RANDOM_STATE) -> np.ndarray:
    """Generate Stage 8 replicate seeds through SeedSequence.generate_state.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 116
    Original stage: Stage 8
    Frozen artifacts generated: results/statistical_confidence/bootstrap_replicates.npz
    Notes: The output dtype is uint64 and seeds are later cast to Python int per replicate.
    """

    seed_sequence = np.random.SeedSequence(random_state)
    return seed_sequence.generate_state(n_bootstrap, dtype=np.uint64)


def paired_stratified_resample_indices(labels: np.ndarray, seed_value: int) -> np.ndarray:
    """Create one paired class-stratified bootstrap index vector.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 116
    Original stage: Stage 8
    Frozen artifacts generated: results/statistical_confidence/bootstrap_replicates.npz
    Notes: Benign and attack indices are sampled separately with replacement and concatenated without shuffling; callers reuse the same indices for both models.
    """

    labels = np.asarray(labels).reshape(-1)
    benign_indices = np.where(labels == 0)[0]
    attack_indices = np.where(labels == 1)[0]
    rng = np.random.default_rng(int(seed_value))
    sampled_benign = rng.choice(benign_indices, size=len(benign_indices), replace=True)
    sampled_attack = rng.choice(attack_indices, size=len(attack_indices), replace=True)
    return np.concatenate([sampled_benign, sampled_attack])


def summarize_distribution(
    values: Sequence[float],
    point_estimate: float,
    *,
    lower_percentile: float = LOWER_PERCENTILE,
    upper_percentile: float = UPPER_PERCENTILE,
) -> dict[str, float | int]:
    """Calculate the exact Stage 8 percentile-bootstrap summary.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 116
    Original stage: Stage 8
    Frozen artifacts generated: results/statistical_confidence/operating_point_bootstrap_intervals.csv, results/statistical_confidence/paired_*_differences.csv
    Notes: Uses np.percentile and sample standard deviation with ddof=1; no BCa correction is applied.
    """

    array = np.asarray(values, dtype=np.float64)
    lower = float(np.percentile(array, lower_percentile))
    upper = float(np.percentile(array, upper_percentile))
    return {
        "Point Estimate": float(point_estimate),
        "Bootstrap Mean": float(np.mean(array)),
        "Bootstrap Median": float(np.median(array)),
        "Bootstrap Standard Error": float(np.std(array, ddof=1)),
        "CI Lower": lower,
        "CI Upper": upper,
        "CI Width": upper - lower,
        "Successful Replicates": int(len(array)),
    }


def paired_difference_summary(
    first_values: Sequence[float],
    second_values: Sequence[float],
    first_point: float,
    second_point: float,
) -> dict[str, Any]:
    """Summarize Stage 8 paired differences using first-minus-second.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 116
    Original stage: Stage 8
    Frozen artifacts generated: results/statistical_confidence/paired_balanced_model_differences.csv, results/statistical_confidence/paired_security_model_differences.csv
    Notes: Toy/static helper; it does not load the frozen 2,000-replicate file.
    """

    differences = np.asarray(first_values, dtype=np.float64) - np.asarray(second_values, dtype=np.float64)
    summary = summarize_distribution(differences, first_point - second_point)
    lower = float(summary["CI Lower"])
    upper = float(summary["CI Upper"])
    interpretation = "Entire CI above zero" if lower > 0 else "Entire CI below zero" if upper < 0 else "CI includes zero"
    return {
        **summary,
        "Difference Convention": "First minus second",
        "Proportion Above Zero": float(np.mean(differences > 0)),
        "Proportion Below Zero": float(np.mean(differences < 0)),
        "CI Interpretation": interpretation,
    }
