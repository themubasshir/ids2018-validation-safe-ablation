"""Static Stage22R membership, threshold and governance contracts."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any


CELL_ORDER = (
    "RANDOM_NATURAL",
    "RANDOM_REBALANCED",
    "CHRONOLOGICAL_NATURAL",
    "CHRONOLOGICAL_REBALANCED",
)

MEMBERSHIP_COUNTS = {
    "RANDOM_NATURAL": {"train": (11_529_922, 1_577_839, 9_952_083), "validation": (2_882_481, 394_460, 2_488_021)},
    "RANDOM_REBALANCED": {"train": (3_926_435, 1_577_839, 2_348_596), "validation": (2_882_481, 394_460, 2_488_021)},
    "CHRONOLOGICAL_NATURAL": {"train": (13_818_623, 1_910_043, 11_908_580), "validation": (593_780, 62_256, 531_524)},
    "CHRONOLOGICAL_REBALANCED": {"train": (4_753_121, 1_910_043, 2_843_078), "validation": (593_780, 62_256, 531_524)},
}

VALIDATION_THRESHOLDS = {
    "RANDOM_NATURAL": {"standard": 0.50, "balanced": 0.46, "security": 0.10},
    "RANDOM_REBALANCED": {"standard": 0.50, "balanced": 0.70, "security": 0.26},
    "CHRONOLOGICAL_NATURAL": {"standard": 0.50, "balanced": 0.07, "security": 0.07},
    "CHRONOLOGICAL_REBALANCED": {"standard": 0.50, "balanced": 0.07, "security": 0.07},
}


def development_threshold_grid_integer_percent() -> tuple[int, ...]:
    """Return the frozen Stage22R source-validation threshold grid.

    Source notebook: notebooks/archive/stage21_stage22_research_continues.ipynb
    Original physical cell(s): 110, 121, 127, 129, 131
    Original stage: Stage22R-0I and Stage22R-2A through Stage22R-2D
    Frozen artifacts generated: stage22r_0i_kaggle_faithful_protocol_lock.json, four Stage22R development result JSON files
    Notes: Integers avoid floating-point ambiguity. This helper never receives
    probabilities, labels, targets or scientific rows and selects no threshold.
    """

    return tuple(range(5, 96))


def membership_counts_are_frozen(cells: Mapping[str, Any]) -> bool:
    """Check toy/static cell counts against the four frozen memberships.

    Source notebook: notebooks/archive/stage21_stage22_research_continues.ipynb
    Original physical cell(s): 118, 119
    Original stage: Stage22R-1B0 and Stage22R-1B1
    Frozen artifacts generated: stage22r_1b0_membership_execution_lock.json, stage22r_1b1_membership_summary.json
    Notes: The caller supplies count dictionaries only. No membership bitset,
    feature matrix, label vector, validation data or final holdout is opened.
    """

    try:
        for cell, roles in MEMBERSHIP_COUNTS.items():
            for role, expected in roles.items():
                observed = cells[cell][role]
                actual = (
                    int(observed["rows"]),
                    int(observed["attack"]),
                    int(observed["benign"]),
                )
                if actual != expected or actual[0] != actual[1] + actual[2]:
                    return False
    except (KeyError, TypeError, ValueError):
        return False
    return True


def chance_pr_auc(attack: int, total: int) -> float:
    """Return the class-prevalence PR-AUC chance anchor for toy counts.

    Source notebook: notebooks/archive/stage21_stage22_research_continues.ipynb
    Original physical cell(s): 121, 127, 129, 131, 135
    Original stage: Stage22R development and final evaluation
    Frozen artifacts generated: four Stage22R development result JSON files, stage22r_final_holdout_result.json
    Notes: This is the declared prevalence identity only. It does not read a
    target, compute model scores, run inference or evaluate a scientific result.
    """

    if total <= 0 or attack < 0 or attack > total:
        raise ValueError("Require 0 <= attack <= total and total > 0")
    return attack / total


def final_opening_is_permanently_closed(opening: Mapping[str, Any]) -> bool:
    """Validate the frozen one-of-one final-opening governance state.

    Source notebook: notebooks/archive/stage21_stage22_research_continues.ipynb
    Original physical cell(s): 133, 134, 135, 136
    Original stage: Stage22R-FINAL
    Frozen artifacts generated: stage22r_final_holdout_result.json
    Notes: Accepts caller-provided metadata only. It never opens Mar1/Mar2,
    loads probabilities/models, performs inference or changes a threshold.
    """

    return (
        opening.get("maximum_authorized") == 1
        and opening.get("consumed") == 1
        and opening.get("permanently_closed") is True
        and opening.get("post_holdout_model_change") is False
        and opening.get("post_holdout_threshold_change") is False
        and opening.get("post_holdout_calibration") is False
    )
