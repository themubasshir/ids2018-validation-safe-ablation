"""Static Stage24 bridge, ledger and direction-separation contracts."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any


AGGREGATE_FLAG_FEATURES = (
    "FIN Flag Cnt",
    "SYN Flag Cnt",
    "RST Flag Cnt",
    "PSH Flag Cnt",
    "ACK Flag Cnt",
    "URG Flag Cnt",
    "CWE Flag Count",
    "ECE Flag Cnt",
)


def bridge62_exclusion_is_frozen(excluded: Sequence[str]) -> bool:
    """Validate the static bridge62 aggregate-flag exclusion.

    Source notebook: notebooks/archive/stage24_cross_dataset_executed.ipynb
    Original physical cell(s): 6, 8
    Original stage: Stage24-0C
    Frozen artifacts generated: stage24_0c_semantic_bridge_spec.json, stage24_0c_final_preopening_protocol_lock.json
    Notes: Names only. This helper does not construct, modify or apply either
    operational feature bridge and reads no source or target values.
    """

    return tuple(excluded) == AGGREGATE_FLAG_FEATURES


def feature_bridge_counts_are_frozen(bridge: Mapping[str, Any]) -> bool:
    """Check the declared 62/70 feature bridge dimensions.

    Source notebook: notebooks/archive/stage24_cross_dataset_executed.ipynb
    Original physical cell(s): 6, 8
    Original stage: Stage24-0C
    Frozen artifacts generated: stage24_0c_semantic_bridge_spec.json
    Notes: Caller-provided counts only; no mapping search, fuzzy match, feature
    remapping, matrix materialization or target inspection is possible here.
    """

    return (
        bridge.get("bridge62") == 62
        and bridge.get("bridge70") == 70
        and bridge.get("mapping_search_performed") is False
        and bridge.get("fuzzy_mapping") is False
    )


def opening_ledger_is_closed(ledger: Mapping[str, Any]) -> bool:
    """Validate the terminal Stage24 opening ledger.

    Source notebook: notebooks/archive/stage24_cross_dataset_executed.ipynb
    Original physical cell(s): 42, 46, 48, 50, 52, 58, 59
    Original stage: Stage24-1C through Stage24-6
    Frozen artifacts generated: stage24_1c_ex1_grounded_s4_durable_artifact_infeasibility_amendment.json, stage24_6_final_synthesis.json
    Notes: Metadata only. It cannot open a target, reallocate a cancelled slot,
    fit a model, perform inference or authorize additional work.
    """

    return (
        ledger.get("evaluable_budget") == 6
        and ledger.get("evaluable_consumed") == 6
        and ledger.get("administratively_cancelled") == 2
        and ledger.get("cancelled_slots_reallocated") is False
        and ledger.get("remaining") == 0
    )


def transfer_directions_remain_separate(
    direction_names: Sequence[str], averaging_performed: bool
) -> bool:
    """Enforce the frozen bidirectional reporting boundary.

    Source notebook: notebooks/archive/stage24_cross_dataset_executed.ipynb
    Original physical cell(s): 59, 60
    Original stage: Stage24-6 and Stage24-PUB
    Frozen artifacts generated: stage24_6_final_synthesis.json, table24_1_bidirectional_generalization.csv
    Notes: Direction labels only. The two directions use different models,
    target populations and prevalences and must never be averaged.
    """

    return tuple(direction_names) == (
        "IDS2018_TO_CICIDS2017",
        "CICIDS2017_TO_IDS2018",
    ) and averaging_performed is False
