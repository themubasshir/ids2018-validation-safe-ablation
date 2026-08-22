"""Binary metric formulas from the canonical Stage 2–5 cells."""

from __future__ import annotations

from typing import Any

import numpy as np


def _counts(labels: np.ndarray, predictions: np.ndarray) -> tuple[int, int, int, int]:
    labels = np.asarray(labels).reshape(-1)
    predictions = np.asarray(predictions, dtype=np.int32).reshape(-1)
    tn = int(np.sum((labels == 0) & (predictions == 0)))
    fp = int(np.sum((labels == 0) & (predictions == 1)))
    fn = int(np.sum((labels == 1) & (predictions == 0)))
    tp = int(np.sum((labels == 1) & (predictions == 1)))
    return tn, fp, fn, tp


def _scores(tn: int, fp: int, fn: int, tp: int) -> tuple[float, float, float, float, float]:
    total = tn + fp + fn + tp
    accuracy = (tp + tn) / total
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    f2 = 5 * precision * recall / (4 * precision + recall) if 4 * precision + recall else 0.0
    return accuracy, precision, recall, f1, f2


def calculate_baseline_metrics(labels: np.ndarray, predictions: np.ndarray) -> dict[str, float | int]:
    """Calculate the Stage 2 baseline metric record.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 94, 95
    Original stage: Stage 2
    Frozen artifacts generated: results/baseline/baseline12_validation_results.csv, results/baseline/baseline4_neural_validation_results.csv
    Notes: Implements labels=[0,1] and zero_division=0 semantics.
    """

    tn, fp, fn, tp = _counts(labels, predictions)
    accuracy, precision, recall, f1, _ = _scores(tn, fp, fn, tp)
    fpr = fp / (fp + tn) if fp + tn else 0.0
    fnr = fn / (fn + tp) if fn + tp else 0.0
    return {"Accuracy": accuracy, "Precision": precision, "Recall": recall, "F1-score": f1, "FPR": fpr, "FNR": fnr, "TP": tp, "TN": tn, "FP": fp, "FN": fn}


def calculate_threshold_metrics(model_name: str, labels: np.ndarray, scores: np.ndarray, threshold: float) -> dict[str, Any]:
    """Calculate one Stage 4 validation threshold record.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 102, 106
    Original stage: Stage 4
    Frozen artifacts generated: results/threshold/winning_model_validation_threshold_sweep.csv, results/threshold/all_top5_validation_threshold_sweep.csv
    Notes: The notebook global winning_model is an explicit argument here.
    """

    predictions = (np.asarray(scores).reshape(-1) >= threshold).astype(np.int32)
    tn, fp, fn, tp = _counts(labels, predictions)
    accuracy, precision, recall, f1, f2 = _scores(tn, fp, fn, tp)
    fpr = fp / (fp + tn) if fp + tn else 0.0
    fnr = fn / (fn + tp) if fn + tp else 0.0
    return {"Model": model_name, "Evaluation Split": "Validation", "Threshold": float(threshold), "Accuracy": accuracy, "Precision": precision, "Recall": recall, "F1-score": f1, "F2-score": f2, "FPR": fpr, "FNR": fnr, "TP": tp, "TN": tn, "FP": fp, "FN": fn}


def calculate_final_test_metrics(model_name: str, labels: np.ndarray, probabilities: np.ndarray, threshold: float, operating_point: str) -> dict[str, Any]:
    """Calculate the Stage 5 frozen-model untouched-test metric record.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 105
    Original stage: Stage 5
    Frozen artifacts generated: results/holdout/xgboost_final_test_operating_points.csv
    Notes: The notebook global FINAL_MODEL_NAME is an explicit argument here.
    """

    predictions = (np.asarray(probabilities).reshape(-1) >= threshold).astype(np.int32)
    tn, fp, fn, tp = _counts(labels, predictions)
    accuracy, precision, recall, f1, f2 = _scores(tn, fp, fn, tp)
    fpr = fp / (fp + tn) if fp + tn else 0.0
    fnr = fn / (fn + tp) if fn + tp else 0.0
    return {"Operating Point": operating_point, "Model": model_name, "Evaluation Split": "Untouched Test", "Threshold": float(threshold), "Accuracy": accuracy, "Precision": precision, "Recall": recall, "F1-score": f1, "F2-score": f2, "FPR": fpr, "FNR": fnr, "TP": tp, "TN": tn, "FP": fp, "FN": fn}


def calculate_objective_test_metrics(model_name: str, objective: str, labels: np.ndarray, probabilities: np.ndarray, threshold: float) -> dict[str, Any]:
    """Calculate the Stage 5 objective-specific holdout record.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 107
    Original stage: Stage 5
    Frozen artifacts generated: results/holdout/objective_specific_final_test_results.csv
    Notes: Preserves the source cell's unguarded FPR and FNR division behavior.
    """

    predictions = (np.asarray(probabilities).reshape(-1) >= threshold).astype(np.int32)
    tn, fp, fn, tp = _counts(labels, predictions)
    accuracy, precision, recall, f1, f2 = _scores(tn, fp, fn, tp)
    fpr = float(np.divide(np.int64(fp), np.int64(fp + tn)))
    fnr = float(np.divide(np.int64(fn), np.int64(fn + tp)))
    from sklearn.metrics import average_precision_score, roc_auc_score

    return {"Objective": objective, "Model": model_name, "Evaluation Split": "Holdout Test", "Threshold": float(threshold), "Accuracy": accuracy, "Precision": precision, "Recall": recall, "F1-score": f1, "F2-score": f2, "FPR": fpr, "FNR": fnr, "TP": tp, "TN": tn, "FP": fp, "FN": fn, "ROC-AUC": roc_auc_score(labels, probabilities), "PR-AUC": average_precision_score(labels, probabilities)}
