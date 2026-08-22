"""Stage20-1E3 validation threshold declarations and toy helpers."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from fractions import Fraction


STANDARD_THRESHOLD = 0.50
BALANCED_THRESHOLD = 0.17
SECURITY_THRESHOLD = 0.17


def threshold_grid() -> tuple[float, ...]:
    """Return the predeclared 0.05–0.95 integer-percent grid."""

    return tuple(value / 100 for value in range(5, 96))


def _rates(row: Mapping[str, int]) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    tp, tn, fp, fn = (int(row[key]) for key in ("TP", "TN", "FP", "FN"))
    f1_denominator = 2 * tp + fp + fn
    f2_denominator = 5 * tp + fp + 4 * fn
    fpr_denominator = fp + tn
    recall_denominator = tp + fn
    return (
        Fraction(2 * tp, f1_denominator) if f1_denominator else Fraction(0),
        Fraction(5 * tp, f2_denominator) if f2_denominator else Fraction(0),
        Fraction(fp, fpr_denominator) if fpr_denominator else Fraction(0),
        Fraction(tp, recall_denominator) if recall_denominator else Fraction(0),
    )


def select_balanced(rows: Sequence[Mapping[str, int]]) -> Mapping[str, int]:
    """Apply the frozen balanced tie rule to caller-supplied toy counts only.

    Source notebook: physical cells 423 and 449.  The repository entry point
    exposes no probability input and cannot reselect a scientific threshold.
    """

    if not rows:
        raise ValueError("rows must not be empty")

    def key(row: Mapping[str, int]) -> tuple[Fraction, Fraction, Fraction, int, int]:
        f1, _, fpr, recall = _rates(row)
        threshold = int(row["threshold_integer_percent"])
        return (-f1, fpr, -recall, abs(threshold - 50), threshold)

    return min(rows, key=key)


def select_security(rows: Sequence[Mapping[str, int]]) -> Mapping[str, int] | None:
    """Apply frozen FPR<=0.05/F2 rules to caller-supplied toy counts only."""

    eligible = [row for row in rows if _rates(row)[2] <= Fraction(1, 20)]
    if not eligible:
        return None

    def key(row: Mapping[str, int]) -> tuple[Fraction, Fraction, Fraction, int]:
        _, f2, fpr, recall = _rates(row)
        return (-f2, fpr, -recall, int(row["threshold_integer_percent"]))

    return min(eligible, key=key)
