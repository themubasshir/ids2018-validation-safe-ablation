"""Stage 10 historical operational-cost and alert-burden methodology."""

from __future__ import annotations

import math
from collections.abc import Sequence
from typing import Any

import numpy as np


COST_RATIOS = (1, 2, 5, 10, 20, 50, 100)
FALSE_POSITIVE_COST = 1.0
CONFIDENCE_LEVEL = 0.95
THRESHOLD_GRID = tuple(float(value) for value in np.round(np.arange(0.05, 0.951, 0.01), 2))
FROZEN_OPERATING_POINTS = (
    {"Operating Point": "XGBoost Standard", "Model": "XGBoost Tuned", "Threshold": 0.50},
    {"Operating Point": "XGBoost Balanced", "Model": "XGBoost Tuned", "Threshold": 0.51},
    {"Operating Point": "XGBoost Security", "Model": "XGBoost Tuned", "Threshold": 0.27},
    {"Operating Point": "LightGBM Balanced", "Model": "LightGBM Tuned", "Threshold": 0.50},
    {"Operating Point": "LightGBM Security", "Model": "LightGBM Tuned", "Threshold": 0.26},
)


def safe_divide(numerator: float | int, denominator: float | int) -> float:
    """Apply the Stage 10 zero-denominator convention.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 119
    Original stage: Stage 10
    Frozen artifacts generated: results/operational_cost/holdout_cost_ratio_evaluation.csv
    Notes: Returns 0.0 when the denominator is zero.
    """

    if denominator == 0:
        return 0.0
    return float(numerator / denominator)


def calculate_metrics(labels: np.ndarray, probabilities: np.ndarray, threshold: float) -> dict[str, float | int]:
    """Calculate Stage 10 threshold metrics.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 119
    Original stage: Stage 10
    Frozen artifacts generated: results/operational_cost/holdout_cost_ratio_evaluation.csv, results/operational_cost/frozen_operating_point_costs.csv
    Notes: Entry points never invoke this on frozen holdout probabilities.
    """

    labels = np.asarray(labels).reshape(-1)
    predictions = np.asarray(probabilities).reshape(-1) >= threshold
    positive = labels == 1
    negative = labels == 0
    tp = int(np.sum(predictions & positive))
    tn = int(np.sum((~predictions) & negative))
    fp = int(np.sum(predictions & negative))
    fn = int(np.sum((~predictions) & positive))
    precision = safe_divide(tp, tp + fp)
    recall = safe_divide(tp, tp + fn)
    f1 = safe_divide(2 * precision * recall, precision + recall)
    f2 = safe_divide(5 * precision * recall, 4 * precision + recall)
    fpr = safe_divide(fp, fp + tn)
    fnr = safe_divide(fn, fn + tp)
    accuracy = safe_divide(tp + tn, tp + tn + fp + fn)
    return {"Accuracy": accuracy, "Precision": precision, "Recall": recall, "F1-score": f1, "F2-score": f2, "FPR": fpr, "FNR": fnr, "TP": tp, "TN": tn, "FP": fp, "FN": fn}


def operational_cost(fp: int, fn: int, fn_to_fp_ratio: float, fp_unit_cost: float = FALSE_POSITIVE_COST) -> float:
    """Calculate Stage 10 cost as C_FP*FP + C_FN*FN.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 119
    Original stage: Stage 10
    Frozen artifacts generated: results/operational_cost/validation_cost_ratio_threshold_selection.csv, results/operational_cost/frozen_operating_point_costs.csv
    Notes: Cost ratios are relative hypothetical units rather than monetary estimates.
    """

    return float(fp_unit_cost * fp + fn_to_fp_ratio * fn)


def select_validation_cost_threshold(rows: Sequence[dict[str, Any]], fn_to_fp_ratio: float) -> dict[str, Any]:
    """Apply Stage 10's exact unconstrained cost-selection tie chain.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 119
    Original stage: Stage 10
    Frozen artifacts generated: results/operational_cost/validation_cost_ratio_threshold_selection.csv
    Notes: Sorts by cost asc, FN asc, FP asc, F2 desc, threshold desc. Cell 119 applies no FPR filter; 5% constraints only provenance frozen Stage 4 security points.
    """

    candidates = []
    for row in rows:
        candidate = dict(row)
        candidate["Operational Cost"] = operational_cost(int(candidate["FP"]), int(candidate["FN"]), fn_to_fp_ratio)
        candidates.append(candidate)
    if not candidates:
        raise ValueError("No threshold sweep rows supplied")
    return min(candidates, key=lambda row: (row["Operational Cost"], row["FN"], row["FP"], -row["F2-score"], -row["Threshold"]))


def break_even_cost_ratio(security_fp: int, security_fn: int, reference_fp: int, reference_fn: int) -> float:
    """Calculate additional false alerts per false negative reduced.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 119
    Original stage: Stage 10
    Frozen artifacts generated: results/operational_cost/break_even_cost_analysis.csv
    Notes: Returns NaN when the security point does not reduce false negatives.
    """

    additional_fp = security_fp - reference_fp
    fn_reduction = reference_fn - security_fn
    return additional_fp / fn_reduction if fn_reduction > 0 else math.nan


def pareto_frontier(rows: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    """Extract the Stage 10 FP/FN Pareto frontier.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 119
    Original stage: Stage 10
    Frozen artifacts generated: results/operational_cost/validation_fp_fn_pareto_frontier.csv
    Notes: Rows sort by FP then FN ascending and are retained only on a strict improvement in the best FN seen.
    """

    best_fn_seen = math.inf
    frontier = []
    for row in sorted((dict(value) for value in rows), key=lambda value: (value["FP"], value["FN"])):
        current_fn = int(row["FN"])
        if current_fn < best_fn_seen:
            row["Pareto Efficient"] = True
            frontier.append(row)
            best_fn_seen = current_fn
    return frontier
