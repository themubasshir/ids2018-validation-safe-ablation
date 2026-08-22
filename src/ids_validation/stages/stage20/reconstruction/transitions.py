"""D5/V1 distinctions and exact/absent transition accounting."""

from __future__ import annotations


D5_COUNTS = {
    "population": 675,
    "membership_exact": 635,
    "length_only_tcp_residuals": 37,
    "duration_export_inconsistencies": 2,
    "protocol0_anchor_inconsistencies": 1,
}
V1_COUNTS = {"membership_exact": 318, "absent": 357, "changed_flows": 379}
TRANSITION_COUNTS = {
    "exact_to_exact": 295,
    "exact_to_absent": 340,
    "absent_to_exact": 23,
    "absent_to_absent": 17,
}


def classify_transition(source_faithful_exact: bool, v1_exact: bool) -> str:
    """Classify a toy pair under the frozen C15/C16 transition vocabulary.

    Source notebook: physical cells 376–379 and 406 (Stage20-1C15-D5,
    1C15-V1/V2, and 1C16-A-R2).  This helper evaluates no packet, flow,
    signature, or label.  V1 was a pre-frozen global payload hypothesis whose
    validation regressed exact membership; it is not an accepted rule.
    """

    before = "exact" if source_faithful_exact else "absent"
    after = "exact" if v1_exact else "absent"
    return f"{before}_to_{after}"
