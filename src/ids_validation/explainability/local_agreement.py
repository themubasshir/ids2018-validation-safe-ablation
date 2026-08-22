"""Stage 13 LIME stability and local SHAP–LIME agreement helpers."""

from __future__ import annotations

from collections.abc import Iterable, Sequence

import numpy as np


TOP_K_VALUES = (5, 10, 15)


def deterministic_top_indices(values: Sequence[float], k: int) -> np.ndarray:
    """Rank local terms by absolute magnitude with feature index as the tie-break.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 138, 139
    Original stage: Stage 13
    Frozen artifacts generated: results/lime/local_shap_lime_agreement.csv, results/lime/lime_shap_full_panel_agreement.csv
    Notes: Exact np.lexsort((indices, -abs(values))) semantics.
    """

    array = np.asarray(values, dtype=np.float64)
    if k < 0:
        raise ValueError("k must be non-negative")
    indices = np.arange(len(array))
    return np.lexsort((indices, -np.abs(array)))[:k]


def jaccard_similarity(first: Iterable[int], second: Iterable[int]) -> float:
    """Calculate the Stage 13 top-k Jaccard similarity.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 137, 138, 139
    Original stage: Stage 13
    Frozen artifacts generated: results/lime/lime_seed_stability_pairwise.csv, results/lime/local_shap_lime_agreement.csv
    Notes: Returns NaN for an empty union, matching the Stage 13 local-agreement implementation.
    """

    first_set = {int(value) for value in first}
    second_set = {int(value) for value in second}
    union = first_set | second_set
    return float("nan") if not union else float(len(first_set & second_set) / len(union))


def cosine_similarity(first: Sequence[float], second: Sequence[float]) -> float:
    """Calculate Stage 13 sparse-attribution cosine similarity.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 135, 137, 138, 139
    Original stage: Stage 13
    Frozen artifacts generated: results/lime/lime_seed_stability_pairwise.csv, results/lime/local_shap_lime_agreement.csv
    Notes: Returns NaN when either vector has zero norm.
    """

    left = np.asarray(first, dtype=np.float64)
    right = np.asarray(second, dtype=np.float64)
    denominator = np.linalg.norm(left) * np.linalg.norm(right)
    return float("nan") if denominator == 0 else float(np.dot(left, right) / denominator)


def shared_sign_agreement(first: Sequence[float], second: Sequence[float]) -> dict[str, float | int]:
    """Measure sign agreement where both Stage 13 sparse vectors are nonzero.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 137
    Original stage: Stage 13
    Frozen artifacts generated: results/lime/lime_seed_stability_pairwise.csv
    Notes: Empty shared support yields count zero and NaN agreement.
    """

    left = np.asarray(first, dtype=np.float64)
    right = np.asarray(second, dtype=np.float64)
    shared = np.where((left != 0) & (right != 0))[0]
    if len(shared) == 0:
        return {"shared_feature_count": 0, "sign_agreement": float("nan")}
    return {"shared_feature_count": int(len(shared)), "sign_agreement": float(np.mean(np.sign(left[shared]) == np.sign(right[shared])))}


def spearman_agreement(first: Sequence[float], second: Sequence[float], *, absolute: bool = False) -> dict[str, float]:
    """Calculate the historical Stage 13 Spearman agreement and p-value.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 137, 138, 139
    Original stage: Stage 13
    Frozen artifacts generated: results/lime/lime_seed_stability_pairwise.csv, results/lime/local_shap_lime_agreement.csv
    Notes: SciPy is imported lazily and its Stage 13 runtime version is VERSION_NOT_PROVEN.
    """

    from scipy.stats import spearmanr

    left = np.asarray(first, dtype=np.float64)
    right = np.asarray(second, dtype=np.float64)
    if absolute:
        left, right = np.abs(left), np.abs(right)
    correlation, p_value = spearmanr(left, right)
    return {"correlation": float(correlation), "p_value": float(p_value)}


def classify_stability(top10_jaccard: float, cosine: float) -> str:
    """Apply the study-specific Stage 13 perturbation-stability labels.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 137
    Original stage: Stage 13
    Frozen artifacts generated: results/lime/lime_seed_stability_case_summary.csv
    Notes: High requires Jaccard >=0.75 and cosine >=0.80; Moderate requires >=0.50 and >=0.60; these are not universal standards.
    """

    if top10_jaccard >= 0.75 and cosine >= 0.80:
        return "High"
    if top10_jaccard >= 0.50 and cosine >= 0.60:
        return "Moderate"
    return "Low"


def classify_reliability(
    decision_agreement: bool,
    local_r2: float,
    fidelity_gap: float,
    top10_jaccard: float,
    absolute_cosine: float,
) -> str:
    """Apply the Stage 13.7B study-specific reliability classification.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 139
    Original stage: Stage 13
    Frozen artifacts generated: results/lime/lime_shap_full_panel_agreement.csv
    Notes: Criteria are descriptive for this study and are not universal LIME/SHAP validity standards.
    """

    fidelity_qualified = decision_agreement and local_r2 >= 0.30 and fidelity_gap <= 0.10
    cross_method_qualified = top10_jaccard >= 0.40 and absolute_cosine >= 0.50
    if fidelity_qualified and cross_method_qualified:
        return "Qualified supplementary explanation"
    if not decision_agreement:
        return "Local decision mismatch"
    if not fidelity_qualified:
        return "Fidelity-limited"
    return "Cross-method divergent"
