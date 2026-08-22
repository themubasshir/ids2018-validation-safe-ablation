"""Exact validation-only Stage 4 threshold grids and tie breakers."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any

import numpy as np


FPR_LIMIT = 0.05


def threshold_grid() -> np.ndarray:
    """Return the authoritative 0.05–0.95 inclusive threshold grid.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 102, 106
    Original stage: Stage 4
    Frozen artifacts generated: results/threshold/winning_model_validation_threshold_sweep.csv, results/threshold/all_top5_validation_threshold_sweep.csv
    Notes: Uses np.round(np.arange(0.05, 0.951, 0.01), 2), yielding 91 values.
    """

    return np.round(np.arange(0.05, 0.951, 0.01), 2)


def rank_validation_models(rows: Iterable[Mapping[str, Any]]) -> list[dict[str, Any]]:
    """Rank validation models by F1, recall, then precision descending.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 95, 102
    Original stage: Stage 2 / Stage 4
    Frozen artifacts generated: results/baseline/validation_selected_top5_models.csv
    Notes: No holdout metric is part of this ordering.
    """

    return sorted((dict(row) for row in rows), key=lambda row: (-row["F1-score"], -row["Recall"], -row["Precision"]))


def select_winner_operating_points(rows: Iterable[Mapping[str, Any]], fpr_limit: float = FPR_LIMIT) -> dict[str, dict[str, Any]]:
    """Apply the canonical single-winner Stage 4 tie-break rules.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 102, 103
    Original stage: Stage 4
    Frozen artifacts generated: results/threshold/selected_validation_operating_points.csv, results/threshold/final_validation_threshold_selection.csv
    Notes: Single-winner maximum-F2 ranks F1 before recall; constrained F2 ranks recall before F1.
    """

    values = [dict(row) for row in rows]
    standard = next(row for row in values if np.isclose(row["Threshold"], 0.50))
    best_f1 = min(values, key=lambda row: (-row["F1-score"], -row["Recall"], row["FPR"], -row["Threshold"]))
    best_f2 = min(values, key=lambda row: (-row["F2-score"], -row["F1-score"], -row["Recall"], row["FPR"], -row["Threshold"]))
    eligible = [row for row in values if row["FPR"] <= fpr_limit]
    if not eligible:
        raise RuntimeError("No threshold satisfies the specified FPR limit.")
    constrained = min(eligible, key=lambda row: (-row["F2-score"], -row["Recall"], -row["F1-score"], row["FPR"], -row["Threshold"]))
    return {"Standard": standard, "Maximum Validation F1": best_f1, "Unconstrained Maximum F2": best_f2, "Constrained Maximum F2": constrained}


def select_all_model_operating_points(rows: Iterable[Mapping[str, Any]], fpr_limit: float = FPR_LIMIT) -> dict[str, dict[str, Any]]:
    """Apply the canonical all-model Stage 4 per-model tie-break rules.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 106
    Original stage: Stage 4
    Frozen artifacts generated: results/threshold/all_top5_selected_validation_operating_points.csv
    Notes: Unlike cell 102, the all-model maximum-F2 chain ranks recall before F1.
    """

    values = [dict(row) for row in rows]
    standard = next(row for row in values if np.isclose(row["Threshold"], 0.50))
    best_f1 = min(values, key=lambda row: (-row["F1-score"], -row["Recall"], row["FPR"], -row["Threshold"]))
    best_f2 = min(values, key=lambda row: (-row["F2-score"], -row["Recall"], -row["F1-score"], row["FPR"], -row["Threshold"]))
    eligible = [row for row in values if row["FPR"] <= fpr_limit]
    if not eligible:
        raise RuntimeError(f"No threshold satisfies FPR <= {fpr_limit:.2f}.")
    constrained = min(eligible, key=lambda row: (-row["F2-score"], -row["Recall"], -row["F1-score"], row["FPR"], -row["Threshold"]))
    return {"Standard Threshold": standard, "Maximum Validation F1": best_f1, "Unconstrained Maximum F2": best_f2, "Constrained Maximum F2": constrained}


def select_cross_model_leaders(rows_by_operating_point: Mapping[str, Iterable[Mapping[str, Any]]]) -> dict[str, dict[str, Any]]:
    """Select the four cross-model Stage 4 leaders with exact key order.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 106
    Original stage: Stage 4
    Frozen artifacts generated: results/threshold/cross_model_threshold_leaders.csv
    Notes: The constrained leader is chosen on validation F2, recall, F1, then lower FPR.
    """

    standards = [dict(row) for row in rows_by_operating_point["Standard Threshold"]]
    best_f1s = [dict(row) for row in rows_by_operating_point["Maximum Validation F1"]]
    best_f2s = [dict(row) for row in rows_by_operating_point["Unconstrained Maximum F2"]]
    constrained = [dict(row) for row in rows_by_operating_point["Constrained Maximum F2"]]
    return {
        "Best Standard F1": min(standards, key=lambda row: (-row["F1-score"], -row["Recall"], -row["Precision"])),
        "Best Threshold-Optimized F1": min(best_f1s, key=lambda row: (-row["F1-score"], -row["Recall"], row["FPR"])),
        "Best Unconstrained F2": min(best_f2s, key=lambda row: (-row["F2-score"], -row["Recall"], -row["F1-score"])),
        "Best Constrained F2": min(constrained, key=lambda row: (-row["F2-score"], -row["Recall"], -row["F1-score"], row["FPR"])),
    }
