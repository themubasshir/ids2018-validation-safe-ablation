"""Stage 12 fixed-hyperparameter multi-seed robustness methodology."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

import numpy as np


SEEDS = (42, 52, 62, 72, 82)
FPR_LIMIT = 0.05
CPU_THREADS = 4
EXPECTED_SPLIT_SIZES = {"train": 192_593, "validation": 48_149, "test": 60_186}
RUNTIME_PARAMETER_KEYS = {
    "random_state",
    "seed",
    "n_jobs",
    "device",
    "device_type",
    "gpu_id",
    "gpu_device_id",
    "predictor",
    "tree_method",
    "verbosity",
    "verbose",
    "early_stopping_rounds",
    "callbacks",
}


def threshold_grid() -> np.ndarray:
    """Return the exact Stage 12 0.05–0.95 threshold grid.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 122
    Original stage: Stage 12
    Frozen artifacts generated: results/multiseed/multiseed_model_operating_points.csv
    Notes: Uses np.round(np.arange(0.05, 0.951, 0.01), 2), yielding 91 values.
    """

    return np.round(np.arange(0.05, 0.951, 0.01), 2)


def repeated_stratified_split_indices(labels: Sequence[int], seed: int) -> dict[str, np.ndarray]:
    """Construct one historical Stage 12 stratified 64/16/20 split.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 122
    Original stage: Stage 12
    Frozen artifacts generated: results/multiseed/multiseed_split_summary.csv
    Notes: Toy/static helper; it performs the two train_test_split calls but is never invoked by a stage entry point or on the scientific dataset.
    """

    from sklearn.model_selection import train_test_split

    targets = np.asarray(labels).reshape(-1)
    indices = np.arange(len(targets), dtype=np.int64)
    train_validation, test = train_test_split(indices, test_size=0.20, stratify=targets, random_state=seed)
    train, validation = train_test_split(
        train_validation,
        test_size=0.20,
        stratify=targets[train_validation],
        random_state=seed,
    )
    return {"train": np.asarray(train), "validation": np.asarray(validation), "test": np.asarray(test)}


def strip_runtime_parameters(parameters: Mapping[str, Any]) -> dict[str, Any]:
    """Remove settings reassigned by the corrected Stage 12 constructors.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 121, 122
    Original stage: Stage 12
    Frozen artifacts generated: metadata/multiseed/fixed_model_parameters.json
    Notes: Cell 121 is the constructor patch preventing duplicate keyword arguments.
    """

    return {key: value for key, value in parameters.items() if key not in RUNTIME_PARAMETER_KEYS}


def build_xgboost(parameters: Mapping[str, Any], seed: int, cpu_threads: int = CPU_THREADS) -> Any:
    """Construct, but never fit, the corrected Stage 12 XGBoost estimator.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 121, 122
    Original stage: Stage 12
    Frozen artifacts generated: metadata/multiseed/fixed_model_parameters.json
    Notes: Imports XGBoost lazily and reapplies random_state, n_jobs, hist tree method, and verbosity after removing session-specific parameters.
    """

    from xgboost import XGBClassifier

    clean = strip_runtime_parameters(parameters)
    clean.update({"random_state": seed, "n_jobs": cpu_threads, "tree_method": "hist", "verbosity": 0})
    return XGBClassifier(**clean)


def build_lightgbm(parameters: Mapping[str, Any], seed: int, cpu_threads: int = CPU_THREADS) -> Any:
    """Construct, but never fit, the corrected Stage 12 LightGBM estimator.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 121, 122
    Original stage: Stage 12
    Frozen artifacts generated: metadata/multiseed/fixed_model_parameters.json
    Notes: Imports LightGBM lazily and reapplies random_state, n_jobs, CPU device type, and verbosity after removing session-specific parameters.
    """

    from lightgbm import LGBMClassifier

    clean = strip_runtime_parameters(parameters)
    clean.update({"random_state": seed, "n_jobs": cpu_threads, "device_type": "cpu", "verbosity": -1})
    return LGBMClassifier(**clean)


def calculate_threshold_metrics(labels: Sequence[int], probabilities: Sequence[float], threshold: float) -> dict[str, float | int]:
    """Calculate the exact Stage 12 threshold-dependent metrics.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 122
    Original stage: Stage 12
    Frozen artifacts generated: results/multiseed/multiseed_model_operating_points.csv
    Notes: Returns zero for zero-denominator rates and excludes AUC metrics, which historically used scikit-learn on full probability vectors.
    """

    targets = np.asarray(labels).reshape(-1)
    scores = np.asarray(probabilities, dtype=np.float64).reshape(-1)
    if len(targets) != len(scores):
        raise ValueError("labels and probabilities must have equal length")
    predictions = scores >= threshold
    positive = targets == 1
    negative = targets == 0
    tp = int(np.sum(predictions & positive))
    tn = int(np.sum((~predictions) & negative))
    fp = int(np.sum(predictions & negative))
    fn = int(np.sum((~predictions) & positive))
    divide = lambda numerator, denominator: 0.0 if denominator == 0 else float(numerator / denominator)
    precision = divide(tp, tp + fp)
    recall = divide(tp, tp + fn)
    return {
        "Accuracy": divide(tp + tn, tp + tn + fp + fn),
        "Precision": precision,
        "Recall": recall,
        "F1-score": divide(2 * precision * recall, precision + recall),
        "F2-score": divide(5 * precision * recall, 4 * precision + recall),
        "FPR": divide(fp, fp + tn),
        "FNR": divide(fn, fn + tp),
        "TP": tp,
        "TN": tn,
        "FP": fp,
        "FN": fn,
    }


def select_balanced_point(rows: Sequence[Mapping[str, float]]) -> Mapping[str, float]:
    """Select the Stage 12 balanced threshold with its exact tie chain.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 122
    Original stage: Stage 12
    Frozen artifacts generated: results/multiseed/multiseed_model_operating_points.csv
    Notes: Orders F1, recall, precision descending; FPR ascending; threshold descending.
    """

    if not rows:
        raise ValueError("rows must not be empty")
    return min(rows, key=lambda row: (-row["F1-score"], -row["Recall"], -row["Precision"], row["FPR"], -row["Threshold"]))


def select_security_point(rows: Sequence[Mapping[str, float]], fpr_limit: float = FPR_LIMIT) -> Mapping[str, float]:
    """Select the constrained Stage 12 security threshold with its exact tie chain.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 122
    Original stage: Stage 12
    Frozen artifacts generated: results/multiseed/multiseed_model_operating_points.csv
    Notes: Filters FPR <= 0.05 then orders F2, recall, F1 descending; FPR ascending; threshold descending.
    """

    eligible = [row for row in rows if row["FPR"] <= fpr_limit]
    if not eligible:
        raise ValueError(f"No threshold satisfies FPR <= {fpr_limit}")
    return min(eligible, key=lambda row: (-row["F2-score"], -row["Recall"], -row["F1-score"], row["FPR"], -row["Threshold"]))


def aggregate_values(values: Sequence[float]) -> dict[str, float]:
    """Return the Stage 12 mean/std/min/max/median aggregation.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 122
    Original stage: Stage 12
    Frozen artifacts generated: results/multiseed/multiseed_metric_summary.csv
    Notes: Sample standard deviation uses ddof=1 to match pandas groupby aggregation.
    """

    array = np.asarray(values, dtype=np.float64)
    if len(array) == 0:
        raise ValueError("values must not be empty")
    return {
        "mean": float(np.mean(array)),
        "std": float(np.std(array, ddof=1)) if len(array) > 1 else float("nan"),
        "min": float(np.min(array)),
        "max": float(np.max(array)),
        "median": float(np.median(array)),
    }


def paired_model_differences(xgboost_values: Sequence[float], lightgbm_values: Sequence[float]) -> np.ndarray:
    """Calculate paired seed-wise differences as XGBoost minus LightGBM.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 122
    Original stage: Stage 12
    Frozen artifacts generated: results/multiseed/multiseed_paired_model_differences.csv
    Notes: Inputs must already be aligned by seed; this helper performs no fitting or artifact loading.
    """

    first = np.asarray(xgboost_values, dtype=np.float64)
    second = np.asarray(lightgbm_values, dtype=np.float64)
    if first.shape != second.shape:
        raise ValueError("paired arrays must have identical shapes")
    return first - second
