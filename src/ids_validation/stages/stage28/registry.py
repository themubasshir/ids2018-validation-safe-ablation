"""Static Stage28 seed, component, closure and final-wall contracts."""

from __future__ import annotations

from collections.abc import Mapping, Sequence


SEEDS = (42, 43, 44, 45, 46)
FAMILIES = ("BOT", "DDOS", "INFILTRATION", "PORT_SCAN", "WEB_ATTACK")
LEARNERS = ("XGBOOST", "LIGHTGBM")
STAGE22_UNITS = ("RANDOM_NATURAL", "CHRONOLOGICAL_NATURAL")


def seed_spec_is_frozen(
    seeds: Sequence[int], reference_seed: int, membership_seed: int
) -> bool:
    """Validate the fixed five model seeds and random membership seed."""

    return tuple(seeds) == SEEDS and reference_seed == 42 and membership_seed == 42


def component_manifest_is_exact(
    components: int,
    new_fit_components: int,
    reuse_components: int,
    scientific_evaluation_cells: int,
) -> bool:
    """Validate the terminal 120-component execution manifest."""

    return (
        components == 120
        and new_fit_components == 108
        and reuse_components == 12
        and scientific_evaluation_cells == 110
    )


def empirical_ledger_is_closed(
    authorized_new_fits: int,
    consumed_new_fits: int,
    remaining_new_fits: int,
    chronology_loao_realizations: int,
    random_loao_realizations: int,
    shared_holdout_evaluations: int,
) -> bool:
    """Validate all frozen Stage28 empirical ledger totals."""

    return (
        authorized_new_fits == 108
        and consumed_new_fits == 108
        and remaining_new_fits == 0
        and chronology_loao_realizations == 50
        and random_loao_realizations == 50
        and shared_holdout_evaluations == 10
    )


def shared_holdout_direction_is_five_of_five(
    claims: Mapping[str, Mapping[str, int]],
) -> bool:
    """Validate both frozen random-below-chronological direction counts."""

    required = ("PR_RANDOM_LT_CHRONO", "ROC_RANDOM_LT_CHRONO")
    return all(
        claims.get(name, {}).get("supporting") == 5
        and claims.get(name, {}).get("total") == 5
        for name in required
    )


def final_wall_is_closed(
    stage29_authorized: bool,
    new_fits_authorized: int,
    target_reopenings_authorized: int,
    threshold_reselection_authorized: int,
    new_significance_tests_authorized: int,
) -> bool:
    """Validate the frozen terminal scientific boundary after Stage28."""

    return (
        stage29_authorized is False
        and new_fits_authorized == 0
        and target_reopenings_authorized == 0
        and threshold_reselection_authorized == 0
        and new_significance_tests_authorized == 0
    )
