"""Static Stage27 taxonomy, membership, threshold and ledger contracts."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any


FAMILY_ORDER = (
    "BOT",
    "DDOS",
    "DOS",
    "AUTH_BRUTE_FORCE",
    "INFILTRATION",
    "PORT_SCAN",
    "WEB_ATTACK",
)
ELIGIBLE_FOLDS = ("BOT", "DDOS", "INFILTRATION", "PORT_SCAN", "WEB_ATTACK")
STRUCTURALLY_INELIGIBLE_FOLDS = ("DOS", "AUTH_BRUTE_FORCE")
INFERENTIAL_FOLDS = ("BOT", "DDOS", "PORT_SCAN", "WEB_ATTACK")
DESCRIPTIVE_ONLY_FOLDS = ("INFILTRATION",)
LEARNERS = ("XGBOOST", "LIGHTGBM")


def taxonomy_is_frozen(
    family_order: Sequence[str],
    eligible: Sequence[str],
    structurally_ineligible: Sequence[str],
    descriptive_only: Sequence[str],
) -> bool:
    """Validate the immutable seven-family/support classification."""

    return (
        tuple(family_order) == FAMILY_ORDER
        and tuple(eligible) == ELIGIBLE_FOLDS
        and tuple(structurally_ineligible) == STRUCTURALLY_INELIGIBLE_FOLDS
        and tuple(descriptive_only) == DESCRIPTIVE_ONLY_FOLDS
    )


def membership_exclusion_is_exact(receipts: Mapping[str, Mapping[str, Any]]) -> bool:
    """Assert zero held-out-family train/validation support for all five folds."""

    if tuple(receipts) != ELIGIBLE_FOLDS:
        return False
    return all(
        row.get("train_count") == 0
        and row.get("validation_count") == 0
        and row.get("train_required") == 0
        and row.get("validation_required") == 0
        and row.get("status") == "PASS"
        for row in receipts.values()
    )


def class_weight(train_benign: int, train_attack: int) -> float:
    """Return the frozen fold-specific positive class-weight formula."""

    if train_attack <= 0:
        raise ValueError("train_attack must be positive")
    return train_benign / train_attack


def threshold_grid() -> tuple[float, ...]:
    """Return the prospectively frozen 0.01 through 0.99 grid."""

    return tuple(value / 100.0 for value in range(1, 100))


def fit_and_opening_ledgers_are_closed(
    fit_authorized: int,
    fit_completed: int,
    openings_budget: int,
    openings_consumed: int,
    openings_remaining: int,
    reopening_authorized: bool,
) -> bool:
    """Validate the terminal ten-fit and five-opening ledgers."""

    return (
        fit_authorized == 10
        and fit_completed == 10
        and openings_budget == 5
        and openings_consumed == 5
        and openings_remaining == 0
        and reopening_authorized is False
    )


def conclusion_labels_are_frozen(labels: Sequence[str]) -> bool:
    """Validate the qualified Stage27 synthesis labels."""

    return tuple(labels) == (
        "SELECTIVE_FAMILY_TRANSFER",
        "RANKING_THRESHOLD_DIVERGENCE",
        "LEARNER_DEPENDENCE",
    )
