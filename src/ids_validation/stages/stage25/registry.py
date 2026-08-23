"""Pure scalar formulas from the frozen Stage25 analytic protocol.

These helpers accept caller-provided scalar values only. They do not locate or
open repository artifacts, models, predictions, targets, or holdouts.
"""

from __future__ import annotations

from dataclasses import dataclass


PREVALENCE_GRID = (0.1, 0.03, 0.01, 0.003, 0.001, 0.0001)
PPV_TARGETS = (0.1, 0.25, 0.5, 0.75, 0.9)
ANALYST_TIERS = (1, 3, 10)
BENIGN_FLOWS_PER_DAY = 1_000_000.0
MINUTES_PER_ALERT = 2.0
COST_FP = 1.0
COST_FN = 100.0


@dataclass(frozen=True)
class ProjectedConfusion:
    """Expected daily counts under fixed TPR/FPR and benign volume."""

    attack: float
    total: float
    tp: float
    fp: float
    tn: float
    fn: float
    alerts: float


def ppv(tpr: float, fpr: float, prevalence: float) -> float:
    """Return PPV under the frozen prior-probability-shift equation."""

    numerator = tpr * prevalence
    return numerator / (numerator + fpr * (1.0 - prevalence))


def npv(tpr: float, fpr: float, prevalence: float) -> float:
    """Return NPV under the frozen prior-probability-shift equation."""

    numerator = (1.0 - fpr) * (1.0 - prevalence)
    return numerator / (numerator + (1.0 - tpr) * prevalence)


def likelihood_ratios(tpr: float, fpr: float) -> tuple[float, float]:
    """Return the frozen positive and negative likelihood ratios."""

    return tpr / fpr, (1.0 - tpr) / (1.0 - fpr)


def ppv_break_even_prevalence(tpr: float, fpr: float, target_ppv: float) -> float:
    """Return exact prevalence at which PPV equals ``target_ppv``."""

    return target_ppv * fpr / (tpr * (1.0 - target_ppv) + target_ppv * fpr)


def required_fpr(tpr: float, prevalence: float, target_ppv: float) -> float:
    """Return the maximum FPR compatible with the requested PPV."""

    return tpr * prevalence * (1.0 - target_ppv) / (target_ppv * (1.0 - prevalence))


def cost_break_even_prevalence(
    tpr: float,
    fpr: float,
    cost_fp: float = COST_FP,
    cost_fn: float = COST_FN,
) -> float:
    """Return the frozen model-versus-ignore relative-cost boundary."""

    return cost_fp * fpr / (cost_fn * tpr + cost_fp * fpr)


def project_confusion(
    tpr: float,
    fpr: float,
    prevalence: float,
    benign_flows: float = BENIGN_FLOWS_PER_DAY,
) -> ProjectedConfusion:
    """Project daily expected counts without accessing any scientific data."""

    attack = prevalence * benign_flows / (1.0 - prevalence)
    tp = tpr * attack
    fn = (1.0 - tpr) * attack
    fp = fpr * benign_flows
    tn = (1.0 - fpr) * benign_flows
    return ProjectedConfusion(
        attack=attack,
        total=attack + benign_flows,
        tp=tp,
        fp=fp,
        tn=tn,
        fn=fn,
        alerts=tp + fp,
    )


def analyst_capacity_fpr_ceiling(
    tpr: float,
    prevalence: float,
    analysts: int,
    benign_flows: float = BENIGN_FLOWS_PER_DAY,
    minutes_per_alert: float = MINUTES_PER_ALERT,
) -> float:
    """Return the exact total-alert FPR ceiling for an eight-hour shift."""

    alerts_per_analyst = 480.0 / minutes_per_alert
    return alerts_per_analyst * analysts / benign_flows - tpr * prevalence / (1.0 - prevalence)


def frozen_grid_shape_is_exact(
    operating_points: int,
    projection_rows: int,
    ppv_break_even_rows: int,
    required_fpr_rows: int,
    cost_break_even_rows: int,
) -> bool:
    """Validate the terminal Stage25 analytic table dimensions."""

    return (
        operating_points == 24
        and projection_rows == 144
        and ppv_break_even_rows == 120
        and required_fpr_rows == 720
        and cost_break_even_rows == 24
    )
