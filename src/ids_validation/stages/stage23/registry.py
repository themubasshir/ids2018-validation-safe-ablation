"""Static Stage23 shortcut-audit contracts for provenance-safe checks."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any


PRIMARY_SUBSETS = {
    "FULL": (70, ()),
    "NO_DST_PORT": (69, ("Dst Port",)),
    "NO_PORTS": (68, ("Dst Port", "Protocol")),
    "NO_INIT_FWD_WIN_BYTS": (69, ("Init Fwd Win Byts",)),
    "NO_FWD_SEG_SIZE_MIN": (69, ("Fwd Seg Size Min",)),
    "NO_SUSPICIOUS_GROUP": (
        67,
        ("Dst Port", "Init Fwd Win Byts", "Fwd Seg Size Min"),
    ),
    "BEHAVIOR_ONLY": (
        63,
        (
            "Dst Port",
            "Protocol",
            "Fwd Header Len",
            "Bwd Header Len",
            "Init Fwd Win Byts",
            "Init Bwd Win Byts",
            "Fwd Seg Size Min",
        ),
    ),
}

FIT_BUDGET = {
    "new_primary_boosted_component_fits": 24,
    "new_placebo_boosted_component_fits": 20,
    "new_stump_fits": 6,
    "total_new_model_fits": 50,
}


def primary_subset_contract_is_frozen(subsets: Mapping[str, Any]) -> bool:
    """Validate static subset counts and removed-feature names.

    Source notebook: notebooks/archive/stage23_research_executed.ipynb
    Original physical cell(s): 7, 9
    Original stage: Stage23-0A and Stage23-0B
    Frozen artifacts generated: feature_subset_spec.json, behavior_only_features.json, suspicious_group.json
    Notes: Accepts caller-provided metadata only. It never reads a feature
    matrix, membership, probability, label, model or target holdout.
    """

    try:
        for name, (count, removed) in PRIMARY_SUBSETS.items():
            observed = subsets[name]
            if int(observed["feature_count"]) != count:
                return False
            if tuple(observed["removed"]) != removed:
                return False
    except (KeyError, TypeError, ValueError):
        return False
    return True


def no_ports_claim_is_accurate(
    full_features: Sequence[str], removed_features: Sequence[str]
) -> bool:
    """Check the frozen NO_PORTS terminology boundary.

    Source notebook: notebooks/archive/stage23_research_executed.ipynb
    Original physical cell(s): 7, 9, 75
    Original stage: Stage23-0 and Stage23-7
    Frozen artifacts generated: feature_subset_spec.json, stage23_final_closure_receipt.json
    Notes: Src Port is absent from the frozen 70-feature space. The historical
    NO_PORTS cell removed Dst Port and Protocol; it did not remove Src Port.
    """

    return (
        "Src Port" not in full_features
        and tuple(removed_features) == ("Dst Port", "Protocol")
    )


def fit_budget_is_closed(counts: Mapping[str, Any]) -> bool:
    """Validate the frozen 50-of-50 model-fit ledger.

    Source notebook: notebooks/archive/stage23_research_executed.ipynb
    Original physical cell(s): 7, 48, 75
    Original stage: Stage23-0, Stage23-3 and Stage23-7
    Frozen artifacts generated: expected_model_count.json, stage23_3_stump_controls_summary.json, stage23_final_closure_receipt.json
    Notes: Count metadata only; this function cannot fit, deserialize or run a
    model and cannot authorize additional computation.
    """

    try:
        return all(int(counts[key]) == value for key, value in FIT_BUDGET.items())
    except (KeyError, TypeError, ValueError):
        return False


def shap_reporting_label_is_safe(
    component_specific: bool, consensus_label: str
) -> bool:
    """Enforce the component-SHAP interpretation boundary.

    Source notebook: notebooks/archive/stage23_research_executed.ipynb
    Original physical cell(s): 7, 52-58, 75
    Original stage: Stage23-0, Stage23-5 and Stage23-7
    Frozen artifacts generated: shap_spec.json, stage23_5b_treeshap_summary.json, stage23_final_closure_receipt.json
    Notes: No SHAP values are accepted or computed. The equal-weight normalized
    consensus is descriptive and is not exact SHAP for the averaged ensemble.
    """

    return component_specific and consensus_label == "DESCRIPTIVE_ONLY"
