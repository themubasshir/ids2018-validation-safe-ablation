"""Stage 9 descriptive calibration methodology without recalibration."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

import numpy as np


N_BOOTSTRAP = 2_000
RANDOM_STATE = 42
CONFIDENCE_LEVEL = 0.95
PRIMARY_BIN_COUNT = 15
BIN_SENSITIVITY_COUNTS = (10, 15, 20)
RECALIBRATION_PERFORMED = False


def calibration_bin_records(
    labels: np.ndarray,
    probabilities: np.ndarray,
    n_bins: int,
    strategy: str,
) -> list[dict[str, float | int]]:
    """Build Stage 9 calibration-bin records with exact edge semantics.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 118
    Original stage: Stage 9
    Frozen artifacts generated: results/calibration/calibration_bins_equal_width.csv, results/calibration/calibration_bins_equal_frequency.csv
    Notes: np.digitize uses edges[1:-1] with right=True; empty bins are omitted and quantile edges are uniqued after endpoints are forced to 0 and 1.
    """

    labels = np.asarray(labels, dtype=np.int8)
    probabilities = np.asarray(probabilities, dtype=np.float64)
    if strategy == "uniform":
        edges = np.linspace(0.0, 1.0, n_bins + 1)
    elif strategy == "quantile":
        edges = np.quantile(probabilities, np.linspace(0.0, 1.0, n_bins + 1))
        edges[0] = 0.0
        edges[-1] = 1.0
        edges = np.unique(edges)
        if len(edges) < 2:
            edges = np.array([0.0, 1.0])
    else:
        raise ValueError(f"Unknown binning strategy: {strategy}")

    bin_ids = np.digitize(probabilities, edges[1:-1], right=True)
    rows: list[dict[str, float | int]] = []
    for bin_index in range(len(edges) - 1):
        mask = bin_ids == bin_index
        count = int(np.sum(mask))
        if count == 0:
            continue
        mean_probability = float(np.mean(probabilities[mask]))
        observed_frequency = float(np.mean(labels[mask]))
        gap = mean_probability - observed_frequency
        rows.append({
            "Bin Index": bin_index + 1,
            "Bin Lower": float(edges[bin_index]),
            "Bin Upper": float(edges[bin_index + 1]),
            "Count": count,
            "Weight": count / len(labels),
            "Mean Predicted Probability": mean_probability,
            "Observed Attack Frequency": observed_frequency,
            "Calibration Gap": gap,
            "Absolute Calibration Gap": abs(gap),
            "Squared Calibration Gap": gap ** 2,
        })
    return rows


def build_calibration_table(labels: np.ndarray, probabilities: np.ndarray, n_bins: int, strategy: str) -> Any:
    """Return the historical pandas calibration table when pandas is available.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 118
    Original stage: Stage 9
    Frozen artifacts generated: results/calibration/calibration_bins_equal_width.csv, results/calibration/calibration_bins_equal_frequency.csv
    Notes: Pandas 2.3.3 is proven by Stage 9 metadata; import is lazy so toy formula tests need only NumPy.
    """

    import pandas as pd

    return pd.DataFrame(calibration_bin_records(labels, probabilities, n_bins, strategy))


def summarize_calibration_records(records: Sequence[dict[str, float | int]]) -> dict[str, float | int]:
    """Calculate Stage 9 ECE, MCE, and RMSCE from bin records.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 118
    Original stage: Stage 9
    Frozen artifacts generated: results/calibration/calibration_metric_point_estimates.csv, results/calibration/calibration_bin_sensitivity.csv
    Notes: ECE is the weighted absolute gap; RMSCE is sqrt(weighted squared gap).
    """

    weights = np.asarray([row["Weight"] for row in records], dtype=np.float64)
    gaps = np.asarray([row["Calibration Gap"] for row in records], dtype=np.float64)
    absolute_gaps = np.abs(gaps)
    return {
        "ECE": float(np.sum(weights * absolute_gaps)),
        "MCE": float(np.max(absolute_gaps)),
        "RMSCE": float(np.sqrt(np.sum(weights * gaps ** 2))),
        "Non-empty Bins": int(len(records)),
    }


def summarize_calibration_table(table: Any) -> dict[str, float | int]:
    """Calculate Stage 9 calibration summaries from the historical DataFrame.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 118
    Original stage: Stage 9
    Frozen artifacts generated: results/calibration/calibration_metric_point_estimates.csv
    Notes: Adapts DataFrame rows to the dependency-light exact formula helper.
    """

    return summarize_calibration_records(table.to_dict(orient="records"))


def calculate_log_loss(labels: np.ndarray, probabilities: np.ndarray) -> float:
    """Calculate Stage 9 binary log loss with 1e-15 clipping.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 118
    Original stage: Stage 9
    Frozen artifacts generated: results/calibration/calibration_metric_point_estimates.csv
    Notes: This is the notebook formula, not a substituted library implementation.
    """

    labels = np.asarray(labels)
    clipped = np.clip(np.asarray(probabilities), 1e-15, 1 - 1e-15)
    return float(-np.mean(labels * np.log(clipped) + (1 - labels) * np.log(1 - clipped)))


def calculate_brier_score(labels: np.ndarray, probabilities: np.ndarray) -> float:
    """Calculate the exact Stage 9 mean squared probability error.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 118
    Original stage: Stage 9
    Frozen artifacts generated: results/calibration/calibration_metric_point_estimates.csv
    Notes: No library Brier implementation is substituted.
    """

    return float(np.mean((np.asarray(probabilities) - np.asarray(labels)) ** 2))


def calculate_calibration_metrics(labels: np.ndarray, probabilities: np.ndarray, n_bins: int = PRIMARY_BIN_COUNT) -> dict[str, float]:
    """Calculate Stage 9 Brier/log-loss and uniform/quantile error metrics.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 118
    Original stage: Stage 9
    Frozen artifacts generated: results/calibration/calibration_metric_point_estimates.csv, results/calibration/calibration_bootstrap_replicates.npz
    Notes: This dependency-light implementation preserves the notebook's bin construction and formulas.
    """

    uniform = summarize_calibration_records(calibration_bin_records(labels, probabilities, n_bins, "uniform"))
    quantile = summarize_calibration_records(calibration_bin_records(labels, probabilities, n_bins, "quantile"))
    return {
        "Brier Score": calculate_brier_score(labels, probabilities),
        "Log Loss": calculate_log_loss(labels, probabilities),
        f"ECE Uniform {n_bins}": float(uniform["ECE"]),
        f"MCE Uniform {n_bins}": float(uniform["MCE"]),
        f"RMSCE Uniform {n_bins}": float(uniform["RMSCE"]),
        f"Adaptive ECE Quantile {n_bins}": float(quantile["ECE"]),
        f"MCE Quantile {n_bins}": float(quantile["MCE"]),
        f"RMSCE Quantile {n_bins}": float(quantile["RMSCE"]),
    }


def calculate_brier_decomposition(
    labels: np.ndarray,
    calibration_records: Sequence[dict[str, float | int]],
    actual_brier_score: float,
) -> dict[str, float]:
    """Calculate the Stage 9 binned Brier decomposition.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 118
    Original stage: Stage 9
    Frozen artifacts generated: results/calibration/brier_score_decomposition.csv
    Notes: Decomposition is based on the primary uniform-bin table and may have a nonzero residual.
    """

    prevalence = float(np.mean(labels))
    weights = np.asarray([row["Weight"] for row in calibration_records], dtype=np.float64)
    means = np.asarray([row["Mean Predicted Probability"] for row in calibration_records], dtype=np.float64)
    observed = np.asarray([row["Observed Attack Frequency"] for row in calibration_records], dtype=np.float64)
    reliability = float(np.sum(weights * (means - observed) ** 2))
    resolution = float(np.sum(weights * (observed - prevalence) ** 2))
    uncertainty = float(prevalence * (1 - prevalence))
    reconstructed = uncertainty - resolution + reliability
    return {
        "Prevalence": prevalence,
        "Reliability": reliability,
        "Resolution": resolution,
        "Uncertainty": uncertainty,
        "Reconstructed Brier": reconstructed,
        "Actual Brier": actual_brier_score,
        "Decomposition Residual": actual_brier_score - reconstructed,
    }


def calculate_calibration_slope_intercept(labels: np.ndarray, probabilities: np.ndarray) -> dict[str, float | bool]:
    """Fit the descriptive Stage 9 calibration intercept and slope.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 118
    Original stage: Stage 9
    Frozen artifacts generated: results/calibration/calibration_metric_point_estimates.csv
    Notes: Uses SciPy 1.16.3 BFGS with analytic gradient and x0=[0,1]; safety-gated entry points never call it.
    """

    from scipy.optimize import minimize
    from scipy.special import expit

    clipped = np.clip(probabilities, 1e-6, 1 - 1e-6)
    logits = np.log(clipped / (1 - clipped))
    labels_float = np.asarray(labels).astype(np.float64)

    def objective(parameters: np.ndarray) -> float:
        intercept, slope = parameters
        linear_predictor = intercept + slope * logits
        return float(np.sum(np.logaddexp(0.0, linear_predictor) - labels_float * linear_predictor))

    def gradient(parameters: np.ndarray) -> np.ndarray:
        intercept, slope = parameters
        linear_predictor = intercept + slope * logits
        residual = expit(linear_predictor) - labels_float
        return np.array([np.sum(residual), np.sum(residual * logits)])

    result = minimize(objective, x0=np.array([0.0, 1.0]), jac=gradient, method="BFGS")
    return {
        "Calibration Intercept": float(result.x[0]),
        "Calibration Slope": float(result.x[1]),
        "Calibration Regression Converged": bool(result.success),
    }
