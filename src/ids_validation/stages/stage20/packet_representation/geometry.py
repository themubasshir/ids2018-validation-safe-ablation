"""Train-only nearest-rank geometry rules for toy histograms."""

from __future__ import annotations

from collections.abc import Mapping
from math import ceil


def _nearest_rank(histogram: Mapping[int, int], quantile: float = 0.95) -> int:
    if not 0 < quantile <= 1:
        raise ValueError("quantile must be in (0, 1]")
    frequencies = {int(value): int(count) for value, count in histogram.items()}
    if not frequencies or any(value < 0 or count < 0 for value, count in frequencies.items()):
        raise ValueError("histogram must contain non-negative values and counts")
    population = sum(frequencies.values())
    if population <= 0:
        raise ValueError("histogram population must be positive")
    rank = ceil(quantile * population)
    cumulative = 0
    for value in sorted(frequencies):
        cumulative += frequencies[value]
        if cumulative >= rank:
            return value
    raise AssertionError("unreachable nearest-rank state")


def _next_power_of_two(value: int) -> int:
    return 1 if value <= 1 else 1 << (value - 1).bit_length()


def select_geometry(flow_packet_histogram: Mapping[int, int], packet_length_histogram: Mapping[int, int]) -> tuple[int, int, int]:
    """Apply the Stage20-1D frozen dimension rule to toy TRAIN histograms.

    Source notebook: physical cells 412–420.  Frozen artifacts: Stage20-1D0,
    1D1-S, and 1D3.  The historical exact daily histograms were integer-summed
    before one combined nearest-rank p95; daily quantiles were never averaged.
    """

    flow_p95 = _nearest_rank(flow_packet_histogram)
    byte_p95 = _nearest_rank(packet_length_histogram)
    rows = min(64, max(16, _next_power_of_two(flow_p95)))
    columns = min(256, max(64, ceil(byte_p95 / 32) * 32))
    if rows * columns > 16_384:
        raise ValueError("selected geometry exceeds the frozen maximum image area")
    return rows, columns, 1
