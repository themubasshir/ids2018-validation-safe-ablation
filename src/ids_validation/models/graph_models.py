"""Static Stage 18 graph-model registries and toy threshold formulas."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass

import numpy as np


SEEDS = (7, 29, 101)


@dataclass(frozen=True)
class EdgeOnlyMLPSpec:
    """Frozen EdgeOnlyMLPControl architecture metadata; not an estimator."""

    input_dim: int = 70
    hidden_dims: tuple[int, int] = (128, 64)
    dropout: float = 0.1
    parameter_count: int = 17_409


@dataclass(frozen=True)
class DirectedGraphTransformerSpec:
    """Frozen EdgeAwareDirectedGraphTransformer metadata; not an estimator."""

    node_feature_dim: int = 5
    edge_feature_dim: int = 70
    model_dimension: int = 64
    attention_heads: int = 4
    graph_layers: int = 2
    feedforward_dimension: int = 128
    dropout: float = 0.1
    parameter_count: int = 113_993


EDGE_ONLY_SPEC = EdgeOnlyMLPSpec()
GRAPH_TRANSFORMER_SPEC = DirectedGraphTransformerSpec()


def threshold_grid() -> np.ndarray:
    """Return the exact Stage 18.3 validation threshold grid.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 270, 273, 282
    Original stage: Stage 18.3E, 18.3H, 18.3J
    Frozen artifacts generated: stage18_3h_validation_threshold_sweep.csv, stage18_3j_validation_threshold_sweep.csv
    """

    return np.arange(1, 100, dtype=np.int64) / 100.0


def select_validation_threshold(rows: Sequence[Mapping[str, float]]) -> Mapping[str, float]:
    """Apply the precommitted validation-only F1/recall/lower-threshold rule.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 270, 273, 282
    Original stage: Stage 18.3E, 18.3H, 18.3J
    Frozen artifacts generated: stage18_3h_edgeonly_ensemble_metrics.json, stage18_3j_graph_transformer_ensemble_metrics.json
    Notes: This helper accepts caller-supplied toy rows and performs no inference or scientific threshold reselection.
    """

    if not rows:
        raise ValueError("rows must not be empty")
    return min(rows, key=lambda row: (-row["f1"], -row["recall"], row["threshold"]))
