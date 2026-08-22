"""Stage 18 source-restricted graph partition and toy shape helpers."""

from __future__ import annotations

from collections.abc import Sequence
from datetime import datetime

import numpy as np


SOURCE_DATE = "2018-02-20"
SNAPSHOT_SECONDS = 60
TRAIN_START = datetime.fromisoformat("2018-02-20 01:00:00")
TRAIN_END = datetime.fromisoformat("2018-02-20 08:59:59")
VALIDATION_START = datetime.fromisoformat("2018-02-20 09:00:00")
VALIDATION_END = datetime.fromisoformat("2018-02-20 10:59:59")
HOLDOUT_START = datetime.fromisoformat("2018-02-20 11:00:00")
HOLDOUT_END = datetime.fromisoformat("2018-02-20 12:59:59")


def chronological_partition(timestamp: datetime) -> str:
    """Classify a toy timestamp under the frozen Stage 18.3 graph chronology.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 268–269
    Original stage: Stage 18.3C–18.3D
    Frozen artifacts generated: stage18_3c_graph_development_protocol.json, stage18_3d_partition_summary.csv
    Notes: Times outside the precommitted Feb-20 development periods are excluded.
    """

    if TRAIN_START <= timestamp <= TRAIN_END:
        return "train"
    if VALIDATION_START <= timestamp <= VALIDATION_END:
        return "validation"
    if HOLDOUT_START <= timestamp <= HOLDOUT_END:
        return "holdout"
    return "excluded"


def wall_clock_snapshot_indices(seconds_since_midnight: Sequence[int], duration_seconds: int = SNAPSHOT_SECONDS) -> np.ndarray:
    """Map caller-supplied toy second offsets to non-overlapping wall-clock bins.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 268–269
    Original stage: Stage 18.3C–18.3D
    Frozen artifacts generated: stage18_3d_snapshot_audit.csv
    Notes: The historical representation used recorded clock-minute boundaries and invented no within-second order.
    """

    seconds = np.asarray(seconds_since_midnight, dtype=np.int64)
    if duration_seconds <= 0 or np.any(seconds < 0):
        raise ValueError("duration must be positive and second offsets must be non-negative")
    return seconds // duration_seconds


def validate_directed_multigraph_shapes(
    source_nodes: Sequence[int],
    destination_nodes: Sequence[int],
    edge_features: Sequence[Sequence[float]],
    edge_labels: Sequence[int] | None = None,
) -> dict[str, int]:
    """Validate only the shapes of a toy directed multigraph snapshot.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 269, 271
    Original stage: Stage 18.3D–18.3F
    Frozen artifacts generated: stage18_3f_graph_tensor_summary.json
    Notes: Parallel edges and direction are preserved; this helper constructs no scientific graph or model tensor.
    """

    source = np.asarray(source_nodes).reshape(-1)
    destination = np.asarray(destination_nodes).reshape(-1)
    features = np.asarray(edge_features)
    if features.ndim != 2 or len(source) != len(destination) or len(source) != len(features):
        raise ValueError("source, destination, and edge-feature rows must align")
    if edge_labels is not None and len(np.asarray(edge_labels).reshape(-1)) != len(source):
        raise ValueError("edge labels must align when supplied")
    node_count = len(np.unique(np.concatenate([source, destination]))) if len(source) else 0
    return {"nodes": int(node_count), "edges": int(len(source)), "edge_feature_dim": int(features.shape[1])}
