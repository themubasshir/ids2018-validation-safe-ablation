"""Validation-safe IDS2018 data preparation extracted from Stage 1."""

from __future__ import annotations

import hashlib
from collections.abc import Iterable, Sequence

import numpy as np


RANDOM_STATE = 42
TARGET_COLUMN = "binary_label"
EXCLUDED_COLUMNS = ("Label", "binary_label")
TEST_SIZE = 0.20
VALIDATION_SHARE_OF_TRAINING_POOL = 0.20


def predictor_columns(columns: Iterable[str]) -> list[str]:
    """Return notebook-order predictor columns after the two exclusions.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 93
    Original stage: Stage 1
    Frozen artifacts generated: metadata/feature_names.json, metadata/split_metadata.json
    Notes: Preserves source-column order; it does not sort feature names.
    """

    excluded = set(EXCLUDED_COLUMNS)
    return [column for column in columns if column not in excluded]


def feature_signature(feature_columns: Sequence[str]) -> str:
    """Calculate the notebook's newline-joined SHA-256 feature signature.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 93
    Original stage: Stage 1
    Frozen artifacts generated: metadata/split_metadata.json
    Notes: The order-sensitive signature uses UTF-8 bytes and no trailing newline.
    """

    return hashlib.sha256("\n".join(feature_columns).encode("utf-8")).hexdigest()


def summarize_split(split_name: str, labels: np.ndarray) -> dict[str, int | float | str]:
    """Summarize record and class counts using the original formulas.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 93
    Original stage: Stage 1
    Frozen artifacts generated: metadata/split_summary.csv, metadata/split_metadata.json
    Notes: Benign is label 0 and attack is label 1, exactly as in the notebook.
    """

    benign = int(np.sum(labels == 0))
    attack = int(np.sum(labels == 1))
    total = int(len(labels))
    return {
        "Split": split_name,
        "Records": total,
        "Benign": benign,
        "Attack": attack,
        "Benign Ratio": benign / total,
        "Attack Ratio": attack / total,
    }


def create_split_indices(labels: np.ndarray, random_state: int = RANDOM_STATE) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Create the exact stratified 64/16/20 positional split.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 93
    Original stage: Stage 1
    Frozen artifacts generated: metadata/split_indices.npz
    Notes: Requires scikit-learn 1.6.1 for the historically proven environment.
    """

    from sklearn.model_selection import train_test_split

    all_indices = np.arange(len(labels), dtype=np.int64)
    train_val_indices, test_indices = train_test_split(
        all_indices,
        test_size=TEST_SIZE,
        random_state=random_state,
        stratify=labels,
    )
    train_indices, val_indices = train_test_split(
        train_val_indices,
        test_size=VALIDATION_SHARE_OF_TRAINING_POOL,
        random_state=random_state,
        stratify=labels[train_val_indices],
    )
    return train_indices, val_indices, test_indices


def fit_training_scaler(
    train_features: np.ndarray,
    validation_features: np.ndarray,
    test_features: np.ndarray,
) -> tuple[object, np.ndarray, np.ndarray, np.ndarray]:
    """Fit StandardScaler on training records only and transform all splits.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 93
    Original stage: Stage 1
    Frozen artifacts generated: metadata/standard_scaler.joblib
    Notes: Validation and untouched test data are never passed to scaler.fit.
    """

    from sklearn.preprocessing import StandardScaler

    scaler = StandardScaler()
    train_scaled = scaler.fit_transform(train_features)
    validation_scaled = scaler.transform(validation_features)
    test_scaled = scaler.transform(test_features)
    return scaler, train_scaled, validation_scaled, test_scaled
