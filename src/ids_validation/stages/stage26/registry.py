"""Static Stage26 measurement contracts and toy-array statistics.

Nothing in this module imports a timing clock, changes CPU affinity, loads a
model, queries a GPU, or executes an inference/profile loop.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence


BATCH_SIZES = (1, 64, 256, 1024, 8192)
WARMUP_TIMED_RUNS = {
    1: (50, 200),
    64: (30, 150),
    256: (20, 100),
    1024: (10, 50),
    8192: (5, 20),
}
PROFILE_TARGETS = (
    "STAGE16_XGBOOST_TUNED",
    "STAGE16_LIGHTGBM_TUNED",
    "STAGE16_CATBOOST_TUNED",
    "FT_BALANCED_5_CHECKPOINT_SOFT_VOTING",
    "STAGE20_MASKED_CNN_V1",
    "STAGE21_MASKED_VIT_V1",
    "ENS_LGBM_XGB_EQUAL",
    "FT_BALANCED_SINGLE_RESOURCE_REFERENCE",
)
CPU_MODES = {
    "CPU_1_PHYSICAL_CORE": {"affinity": (0,), "thread_count": 1},
    "CPU_2_PHYSICAL_CORE": {"affinity": (0, 1), "thread_count": 2},
}
PUBLICATION_FIGURE_STEMS = (
    "F26_CAPACITY_SCALING",
    "F26_COLD_START",
    "F26_COMPONENT_BOUNDARY",
    "F26_CPU1_GPU_P95_SPEEDUP",
    "F26_GPU_DELTA_PEAK_MEMORY",
    "F26_MEMORY_PACKAGE",
    "F26_PARETO",
    "F26_REPRESENTATION_SENSITIVITY",
    "F26_WARM_LATENCY",
    "F26_WARM_THROUGHPUT",
)


def linear_percentile(values: Iterable[float], quantile: float) -> float:
    """Return the frozen linear percentile definition for a toy sequence."""

    ordered = sorted(float(value) for value in values)
    if not ordered:
        raise ValueError("values must not be empty")
    if not 0.0 <= quantile <= 1.0:
        raise ValueError("quantile must be between zero and one")
    position = (len(ordered) - 1) * quantile
    lower = int(position)
    upper = min(lower + 1, len(ordered) - 1)
    fraction = position - lower
    return ordered[lower] + fraction * (ordered[upper] - ordered[lower])


def summarize_toy_timing_ms(elapsed_ns: Iterable[int]) -> dict[str, float]:
    """Summarize caller-provided toy nanoseconds without performing timing."""

    milliseconds = [float(value) / 1_000_000.0 for value in elapsed_ns]
    return {
        "p50_ms": linear_percentile(milliseconds, 0.50),
        "p95_ms": linear_percentile(milliseconds, 0.95),
        "p99_ms": linear_percentile(milliseconds, 0.99),
    }


def execution_plan_is_frozen(
    targets: Sequence[str],
    batch_sizes: Sequence[int],
    condition_count: int,
    seed: int,
) -> bool:
    """Validate the static 8-target, 2-mode, 5-batch execution plan."""

    return (
        tuple(targets) == PROFILE_TARGETS
        and tuple(batch_sizes) == BATCH_SIZES
        and condition_count == 80
        and seed == 26042
    )


def warmup_schedule_is_frozen(schedule: Mapping[int, Sequence[int]]) -> bool:
    """Validate warmup/timed counts without running a benchmark."""

    return {int(key): tuple(value) for key, value in schedule.items()} == WARMUP_TIMED_RUNS


def gpu_contract_is_frozen(
    gpu_name: str,
    synchronization_rule: str,
    condition_count: int,
    raw_observations: int,
) -> bool:
    """Validate the historical single-T4 receipt fields."""

    return (
        gpu_name == "Tesla T4"
        and synchronization_rule == "DEVICE_SYNCHRONIZE_BEFORE_AND_AFTER_EVERY_TIMED_REGION"
        and condition_count == 40
        and raw_observations == 3100
    )


def publication_figure_inventory_is_complete(stems: Sequence[str]) -> bool:
    """Validate the ten frozen figure stems; rendering is never invoked."""

    return tuple(stems) == PUBLICATION_FIGURE_STEMS
