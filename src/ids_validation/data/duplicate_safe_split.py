"""Stage 15 duplicate-safe split methodology and frozen feature registry."""

from __future__ import annotations

from collections.abc import Mapping, Sequence

import numpy as np


SPLIT_SEED = 42
SPLIT_PRIORITY = ("train", "validation", "holdout")
ORIGINAL_SPLIT_SIZES = {"train": 192_593, "validation": 48_149, "holdout": 60_186}
DUPLICATE_SAFE_SPLIT_SIZES = {"train": 154_686, "validation": 37_835, "holdout": 46_849}
CONSTANT_FEATURE_INDICES = (32, 34, 56, 57, 58, 59, 60, 61)
CONSTANT_FEATURES = (
    "Bwd PSH Flags",
    "Bwd URG Flags",
    "Fwd Byts/b Avg",
    "Fwd Pkts/b Avg",
    "Fwd Blk Rate Avg",
    "Bwd Byts/b Avg",
    "Bwd Pkts/b Avg",
    "Bwd Blk Rate Avg",
)
RETAINED_FEATURES = (
    "Dst Port",
    "Protocol",
    "Flow Duration",
    "Tot Fwd Pkts",
    "Tot Bwd Pkts",
    "TotLen Fwd Pkts",
    "TotLen Bwd Pkts",
    "Fwd Pkt Len Max",
    "Fwd Pkt Len Min",
    "Fwd Pkt Len Mean",
    "Fwd Pkt Len Std",
    "Bwd Pkt Len Max",
    "Bwd Pkt Len Min",
    "Bwd Pkt Len Mean",
    "Bwd Pkt Len Std",
    "Flow Byts/s",
    "Flow Pkts/s",
    "Flow IAT Mean",
    "Flow IAT Std",
    "Flow IAT Max",
    "Flow IAT Min",
    "Fwd IAT Tot",
    "Fwd IAT Mean",
    "Fwd IAT Std",
    "Fwd IAT Max",
    "Fwd IAT Min",
    "Bwd IAT Tot",
    "Bwd IAT Mean",
    "Bwd IAT Std",
    "Bwd IAT Max",
    "Bwd IAT Min",
    "Fwd PSH Flags",
    "Fwd URG Flags",
    "Fwd Header Len",
    "Bwd Header Len",
    "Fwd Pkts/s",
    "Bwd Pkts/s",
    "Pkt Len Min",
    "Pkt Len Max",
    "Pkt Len Mean",
    "Pkt Len Std",
    "Pkt Len Var",
    "FIN Flag Cnt",
    "SYN Flag Cnt",
    "RST Flag Cnt",
    "PSH Flag Cnt",
    "ACK Flag Cnt",
    "URG Flag Cnt",
    "CWE Flag Count",
    "ECE Flag Cnt",
    "Down/Up Ratio",
    "Pkt Size Avg",
    "Fwd Seg Size Avg",
    "Bwd Seg Size Avg",
    "Subflow Fwd Pkts",
    "Subflow Fwd Byts",
    "Subflow Bwd Pkts",
    "Subflow Bwd Byts",
    "Init Fwd Win Byts",
    "Init Bwd Win Byts",
    "Fwd Act Data Pkts",
    "Fwd Seg Size Min",
    "Active Mean",
    "Active Std",
    "Active Max",
    "Active Min",
    "Idle Mean",
    "Idle Std",
    "Idle Max",
    "Idle Min",
)


def select_first_representatives(indices: Sequence[int], pattern_hashes: Sequence[int]) -> np.ndarray:
    """Select the smallest original row index for every pattern.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 163
    Original stage: Stage 15
    Frozen artifacts generated: results/stage15_transformer_checkpoint/stage15_1_duplicate_safe_split_indices.npz
    Notes: This is a toy/static helper. It consumes caller-supplied hashes and never opens the scientific dataset or frozen split.
    """

    candidates = np.asarray(indices, dtype=np.int64)
    hashes = np.asarray(pattern_hashes)
    if candidates.ndim != 1 or hashes.ndim != 1:
        raise ValueError("indices and pattern_hashes must be one-dimensional")
    if len(candidates) and (candidates.min() < 0 or candidates.max() >= len(hashes)):
        raise IndexError("an index falls outside pattern_hashes")
    representatives: dict[int, int] = {}
    for row_index in np.sort(candidates):
        representatives.setdefault(int(hashes[row_index]), int(row_index))
    return np.asarray(sorted(representatives.values()), dtype=np.int64)


def conflicting_binary_pattern_hashes(pattern_hashes: Sequence[int], labels: Sequence[int]) -> np.ndarray:
    """Return hashes associated with more than one binary label.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 163
    Original stage: Stage 15
    Frozen artifacts generated: results/stage15_transformer_checkpoint/stage15_1_conflicting_pattern_summary.csv
    Notes: The historical hashes came from pandas.util.hash_pandas_object(index=False). This helper does not hash or inspect feature values.
    """

    hashes = np.asarray(pattern_hashes)
    targets = np.asarray(labels).reshape(-1)
    if hashes.ndim != 1 or len(hashes) != len(targets):
        raise ValueError("pattern_hashes and labels must be aligned one-dimensional arrays")
    observed: dict[int, set[int]] = {}
    for pattern_hash, label in zip(hashes, targets, strict=True):
        observed.setdefault(int(pattern_hash), set()).add(int(label))
    return np.asarray(sorted(key for key, values in observed.items() if len(values) > 1), dtype=hashes.dtype)


def construct_duplicate_safe_indices(
    pattern_hashes: Sequence[int],
    labels: Sequence[int],
    original_splits: Mapping[str, Sequence[int]],
) -> dict[str, np.ndarray]:
    """Apply the exact train-priority Stage 15 duplicate policy to supplied hashes.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 163
    Original stage: Stage 15
    Frozen artifacts generated: results/stage15_transformer_checkpoint/stage15_1_duplicate_safe_split_indices.npz
    Notes: Globally conflicting binary patterns are removed, then the minimum-index representative is retained in train, validation, and holdout priority order. This helper is for synthetic equivalence tests only.
    """

    hashes = np.asarray(pattern_hashes)
    targets = np.asarray(labels).reshape(-1)
    if hashes.ndim != 1 or len(hashes) != len(targets):
        raise ValueError("pattern_hashes and labels must be aligned one-dimensional arrays")
    if set(original_splits) != set(SPLIT_PRIORITY):
        raise ValueError(f"original_splits must contain exactly {SPLIT_PRIORITY}")

    conflicting = set(int(value) for value in conflicting_binary_pattern_hashes(hashes, targets))
    seen: set[int] = set()
    safe: dict[str, np.ndarray] = {}
    for split_name in SPLIT_PRIORITY:
        candidates = np.asarray(original_splits[split_name], dtype=np.int64)
        allowed = np.asarray(
            [index for index in candidates if int(hashes[index]) not in conflicting and int(hashes[index]) not in seen],
            dtype=np.int64,
        )
        safe_indices = select_first_representatives(allowed, hashes)
        safe[split_name] = safe_indices
        seen.update(int(value) for value in hashes[safe_indices])
    return safe


def verify_duplicate_safe_invariants(splits: Mapping[str, Sequence[int]], pattern_hashes: Sequence[int]) -> bool:
    """Verify no within- or cross-split pattern duplicates remain.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 163
    Original stage: Stage 15
    Frozen artifacts generated: results/stage15_transformer_checkpoint/stage15_1_cross_split_verification.csv
    Notes: Returns a Boolean for toy/static verification and does not load scientific artifacts.
    """

    hashes = np.asarray(pattern_hashes)
    seen: set[int] = set()
    for split_name in SPLIT_PRIORITY:
        split_hashes = [int(value) for value in hashes[np.asarray(splits[split_name], dtype=np.int64)]]
        current = set(split_hashes)
        if len(current) != len(split_hashes) or current & seen:
            return False
        seen.update(current)
    return True
