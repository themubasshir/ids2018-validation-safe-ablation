"""Stage 13 LIME configuration, sampling, and fidelity helpers."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

import numpy as np


RANDOM_STATE = 42
BACKGROUND_SIZE = 20_000
INITIAL_NUM_SAMPLES = 5_000
SELECTED_NUM_SAMPLES = 10_000
NUM_FEATURES = 15
ATTACK_LABEL_INDEX = 1
INITIAL_BASE_SEED = 130_500
SENSITIVITY_BASE_SEED = 136_000
FULL_PANEL_BASE_SEED = 137_700
PERTURBATION_BASE_SEEDS = (137_000, 138_000, 139_000, 140_000, 141_000)
SELECTED_KERNEL_WIDTH = 8.831760866327848


def sample_training_background(labels: Sequence[int], size: int = BACKGROUND_SIZE, seed: int = RANDOM_STATE) -> np.ndarray:
    """Select the exact Stage 13 stratified training-background positions.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 134
    Original stage: Stage 13
    Frozen artifacts generated: metadata/lime/lime_background_manifest.csv, metadata/lime/lime_background_data.npz
    Notes: Uses one StratifiedShuffleSplit and sorts the selected positions; entry points never call it on scientific data.
    """

    from sklearn.model_selection import StratifiedShuffleSplit

    targets = np.asarray(labels).reshape(-1)
    actual_size = min(size, len(targets))
    splitter = StratifiedShuffleSplit(n_splits=1, train_size=actual_size, random_state=seed)
    positions, _ = next(splitter.split(np.zeros((len(targets), 1)), targets))
    return np.sort(np.asarray(positions, dtype=np.int64))


def explanation_seed(base_seed: int, case_number: int) -> int:
    """Derive a Stage 13 paired-model explanation seed.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 135, 136, 137, 139
    Original stage: Stage 13
    Frozen artifacts generated: results/lime/lime_initial_explanation_summary.csv, results/lime/lime_seed_stability_runs.csv, results/lime/lime_full_panel_summary.csv
    Notes: Both models receive the same base_seed + case_number value for a paired case/configuration.
    """

    return int(base_seed + case_number)


def fidelity_metrics(model_probability: float, local_prediction: float, threshold: float) -> dict[str, float | int | bool]:
    """Calculate Stage 13 local-surrogate fidelity and decision agreement.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 135, 136, 137, 139
    Original stage: Stage 13
    Frozen artifacts generated: results/lime/lime_fidelity_configuration_results.csv, results/lime/lime_full_panel_summary.csv
    Notes: Fidelity gap uses the unclipped local prediction; decision agreement thresholds its [0,1]-clipped value.
    """

    clipped = float(np.clip(local_prediction, 0.0, 1.0))
    model_decision = int(model_probability >= threshold)
    local_decision = int(clipped >= threshold)
    return {
        "model_probability": float(model_probability),
        "local_prediction": float(local_prediction),
        "local_prediction_clipped": clipped,
        "fidelity_gap": float(abs(model_probability - local_prediction)),
        "model_decision": model_decision,
        "local_decision": local_decision,
        "decision_agreement": local_decision == model_decision,
    }


def build_selected_explainer(
    training_data: np.ndarray,
    training_labels: Sequence[int],
    feature_names: Sequence[str],
    random_state: int,
) -> Any:
    """Construct the selected Stage 13.6A LIME explainer without explaining a case.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 136, 137, 139
    Original stage: Stage 13
    Frozen artifacts generated: metadata/lime/stage13_6a_selected_lime_configuration.json
    Notes: Imports LIME lazily; selected explanations historically use 10,000 samples, 15 features, Euclidean distance, and this continuous wider-kernel configuration.
    """

    from lime.lime_tabular import LimeTabularExplainer

    return LimeTabularExplainer(
        training_data=np.asarray(training_data),
        training_labels=np.asarray(training_labels),
        feature_names=list(feature_names),
        class_names=["Benign", "Attack"],
        mode="classification",
        discretize_continuous=False,
        feature_selection="auto",
        sample_around_instance=True,
        kernel_width=SELECTED_KERNEL_WIDTH,
        random_state=random_state,
    )
