"""Static Stage 19 temporal-model registries and toy threshold selection."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass

import numpy as np


SEEDS = (7, 29, 101)


@dataclass(frozen=True)
class TemporalTransformerSpec:
    """Frozen shared temporal-encoder metadata; not an estimator."""

    input_dimension: int = 80
    model_dimension: int = 64
    heads: int = 4
    layers_per_branch: int = 2
    feedforward_dimension: int = 128
    dropout: float = 0.1


SINGLE_SCALE_SPEC = TemporalTransformerSpec()
MTEMPORAL_SPEC = TemporalTransformerSpec()


def threshold_grid() -> np.ndarray:
    """Return the exact Stage 19 validation-only threshold grid.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 290, 308
    Original stage: Stage 19.0, 19.5
    Frozen artifacts generated: stage19_5_validation_threshold_grid.csv
    Notes: Static grid only; accepts no scientific probabilities.
    """

    return np.arange(1, 100, dtype=np.int64) / 100.0


def select_validation_threshold(rows: Sequence[Mapping[str, float]]) -> Mapping[str, float]:
    """Apply maximum F1, higher recall, then lower threshold to toy rows.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 308
    Original stage: Stage 19.5
    Frozen artifacts generated: stage19_5_frozen_operating_points.json
    Notes: No stage entry point accepts scientific probabilities or permits threshold reselection.
    """

    if not rows:
        raise ValueError("rows must not be empty")
    return min(rows, key=lambda row: (-row["f1"], -row["recall"], row["threshold"]))
