#!/usr/bin/env python3
"""
Stage26-6F1 locked derived-summary bootstrap correction worker.

IMPORTANT:
- This file is frozen in Stage26-6F0 before any corrected CI is computed.
- It consumes only immutable Stage26-2 raw timing observations.
- It performs no model loading, inference, timing, or predictive evaluation.
- It never overwrites historical Stage26-2 artifacts.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import numpy as np


BOOTSTRAP_REPLICATES = 2000
BOOTSTRAP_SEED = 26042
CI_PERCENTILES = (2.5, 97.5)
PERCENTILE_METHOD = "linear"


def load_csv(path: Path):

    with path.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as f:

        return list(
            csv.DictReader(
                f
            )
        )


def percentile_ci(values):

    values = np.asarray(
        values,
        dtype=np.float64,
    )

    result = np.percentile(
        values,
        CI_PERCENTILES,
        method=PERCENTILE_METHOD,
    )

    return [
        float(
            result[0]
        ),
        float(
            result[1]
        ),
    ]


def exact_point_estimates(
    elapsed_ms,
    throughput,
):

    n = int(
        elapsed_ms.size
    )

    result = {
        "p50_batch_latency_ms":
            float(
                np.percentile(
                    elapsed_ms,
                    50,
                    method=PERCENTILE_METHOD,
                )
            ),

        "p95_batch_latency_ms":
            float(
                np.percentile(
                    elapsed_ms,
                    95,
                    method=PERCENTILE_METHOD,
                )
            ),

        "p99_batch_latency_ms_if_n_gte_100":
            (
                float(
                    np.percentile(
                        elapsed_ms,
                        99,
                        method=PERCENTILE_METHOD,
                    )
                )
                if n >= 100
                else None
            ),

        "median_throughput_flows_per_second":
            float(
                np.median(
                    throughput
                )
            ),
    }

    return result


def corrected_bootstrap_for_condition(
    elapsed_ns,
    flows_per_second,
):

    elapsed_ns = np.asarray(
        elapsed_ns,
        dtype=np.float64,
    )

    throughput = np.asarray(
        flows_per_second,
        dtype=np.float64,
    )


    if elapsed_ns.ndim != 1:

        raise RuntimeError(
            "elapsed_ns must be one-dimensional."
        )


    if throughput.ndim != 1:

        raise RuntimeError(
            "flows_per_second must be one-dimensional."
        )


    if elapsed_ns.size != throughput.size:

        raise RuntimeError(
            "Latency and throughput observation counts differ."
        )


    n = int(
        elapsed_ns.size
    )


    if n <= 0:

        raise RuntimeError(
            "Cannot bootstrap an empty condition."
        )


    # Historical point-estimate semantics established by Stage26-6E:
    # convert raw nanoseconds to float64 milliseconds BEFORE percentile.
    elapsed_ms = (
        elapsed_ns
        /
        1_000_000.0
    )


    # FROZEN CORRECTION:
    # literal condition-local seed; absolutely no derived seed.
    rng = np.random.default_rng(
        BOOTSTRAP_SEED
    )


    indices = rng.integers(
        0,
        n,
        size=(
            BOOTSTRAP_REPLICATES,
            n,
        ),
        endpoint=False,
        dtype=np.int64,
    )


    # Same resample matrix reused for all frozen targets.
    boot_latency = elapsed_ms[
        indices
    ]

    boot_throughput = throughput[
        indices
    ]


    p50_rep = np.percentile(
        boot_latency,
        50,
        axis=1,
        method=PERCENTILE_METHOD,
    )

    p95_rep = np.percentile(
        boot_latency,
        95,
        axis=1,
        method=PERCENTILE_METHOD,
    )


    if n >= 100:

        p99_rep = np.percentile(
            boot_latency,
            99,
            axis=1,
            method=PERCENTILE_METHOD,
        )

    else:

        p99_rep = None


    median_throughput_rep = np.median(
        boot_throughput,
        axis=1,
    )


    point = exact_point_estimates(
        elapsed_ms,
        throughput,
    )


    result = {
        "n":
            n,

        "bootstrap_replicates":
            BOOTSTRAP_REPLICATES,

        "bootstrap_seed":
            BOOTSTRAP_SEED,

        "rng":
            "numpy.random.default_rng_PCG64",

        "sampling":
            "WITH_REPLACEMENT",

        "same_resample_indices_for_all_targets":
            True,

        "point_estimate_integrity":
            point,

        "corrected_ci95": {
            "p50_batch_latency_ms":
                percentile_ci(
                    p50_rep
                ),

            "p95_batch_latency_ms":
                percentile_ci(
                    p95_rep
                ),

            "p99_batch_latency_ms_if_n_gte_100":
                (
                    percentile_ci(
                        p99_rep
                    )
                    if p99_rep is not None
                    else None
                ),

            "median_throughput_flows_per_second":
                percentile_ci(
                    median_throughput_rep
                ),
        },
    }


    return result


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--raw-csv",
        required=True,
    )

    parser.add_argument(
        "--summary-csv",
        required=True,
    )

    parser.add_argument(
        "--condition-status-csv",
        required=True,
    )

    parser.add_argument(
        "--output-json",
        required=True,
    )

    args = parser.parse_args()


    raw_path = Path(
        args.raw_csv
    )

    summary_path = Path(
        args.summary_csv
    )

    status_path = Path(
        args.condition_status_csv
    )

    output_path = Path(
        args.output_json
    )


    raw_rows = load_csv(
        raw_path
    )

    summary_rows = load_csv(
        summary_path
    )

    status_rows = load_csv(
        status_path
    )


    summary_by_condition = {
        row[
            "condition_id"
        ]:
            row
        for row in summary_rows
    }


    status_by_condition = {
        row[
            "condition_id"
        ]:
            row
        for row in status_rows
    }


    condition_ids = sorted(
        status_by_condition,
        key=lambda value: int(
            value.split(
                "_"
            )[
                -1
            ]
        ),
    )


    output_conditions = []


    for condition_id in condition_ids:

        status_row = status_by_condition[
            condition_id
        ]

        status = status_row[
            "status"
        ]


        if status != "PASS":

            output_conditions.append(
                {
                    "condition_id":
                        condition_id,

                    "status":
                        status,

                    "bootstrap_computed":
                        False,

                    "reason":
                        "NON_PASS_FROZEN_RESOURCE_OUTCOME",
                }
            )

            continue


        raw_condition = [
            row
            for row in raw_rows
            if row[
                "condition_id"
            ]
            ==
            condition_id
        ]


        if not raw_condition:

            raise RuntimeError(
                f"{condition_id}: PASS but raw observations absent."
            )


        if any(
            row[
                "status"
            ]
            !=
            "PASS"
            for row in raw_condition
        ):

            raise RuntimeError(
                f"{condition_id}: non-PASS raw row found."
            )


        summary_row = summary_by_condition[
            condition_id
        ]


        expected_n = int(
            summary_row[
                "n"
            ]
        )


        if len(
            raw_condition
        ) != expected_n:

            raise RuntimeError(
                f"{condition_id}: raw n mismatch."
            )


        elapsed_ns = [
            int(
                row[
                    "elapsed_ns"
                ]
            )
            for row in raw_condition
        ]

        throughput = [
            float(
                row[
                    "flows_per_second"
                ]
            )
            for row in raw_condition
        ]


        corrected = corrected_bootstrap_for_condition(
            elapsed_ns,
            throughput,
        )


        # -------------------------------------------------------------
        # Integrity gate:
        # corrected procedure must reproduce immutable point estimates.
        # It is forbidden to replace point estimates.
        # -------------------------------------------------------------

        point = corrected[
            "point_estimate_integrity"
        ]


        stored_p50 = float(
            summary_row[
                "p50_batch_latency_ms"
            ]
        )

        stored_p95 = float(
            summary_row[
                "p95_batch_latency_ms"
            ]
        )

        stored_tp = float(
            summary_row[
                "median_throughput_flows_per_second"
            ]
        )


        if point[
            "p50_batch_latency_ms"
        ] != stored_p50:

            raise RuntimeError(
                f"{condition_id}: p50 point-estimate integrity failed."
            )


        if point[
            "p95_batch_latency_ms"
        ] != stored_p95:

            raise RuntimeError(
                f"{condition_id}: p95 point-estimate integrity failed."
            )


        if point[
            "median_throughput_flows_per_second"
        ] != stored_tp:

            raise RuntimeError(
                f"{condition_id}: throughput point-estimate integrity failed."
            )


        if expected_n >= 100:

            stored_p99 = float(
                summary_row[
                    "p99_batch_latency_ms_if_n_gte_100"
                ]
            )


            if point[
                "p99_batch_latency_ms_if_n_gte_100"
            ] != stored_p99:

                raise RuntimeError(
                    f"{condition_id}: p99 point-estimate integrity failed."
                )


        else:

            if (
                summary_row[
                    "p99_batch_latency_ms_if_n_gte_100"
                ]
                not in {
                    "",
                    None,
                }
            ):

                raise RuntimeError(
                    f"{condition_id}: unexpected historical p99 for n<100."
                )


        output_conditions.append(
            {
                "condition_id":
                    condition_id,

                "target_id":
                    summary_row[
                        "target_id"
                    ],

                "comparison_group":
                    summary_row[
                        "comparison_group"
                    ],

                "hardware_mode":
                    summary_row[
                        "hardware_mode"
                    ],

                "thread_count":
                    int(
                        summary_row[
                            "thread_count"
                        ]
                    ),

                "batch_size":
                    int(
                        summary_row[
                            "batch_size"
                        ]
                    ),

                "status":
                    "PASS",

                "bootstrap_computed":
                    True,

                "historical_CI_status":
                    "HISTORICAL_NOT_PROTOCOL_CERTIFIED",

                "corrected_CI_status":
                    "PROTOCOL_CERTIFIED_DERIVED_UNCERTAINTY",

                "historical_ci95": {
                    "p50_batch_latency_ms": [
                        float(
                            summary_row[
                                "p50_ci95_low_ms"
                            ]
                        ),
                        float(
                            summary_row[
                                "p50_ci95_high_ms"
                            ]
                        ),
                    ],

                    "p95_batch_latency_ms": [
                        float(
                            summary_row[
                                "p95_ci95_low_ms"
                            ]
                        ),
                        float(
                            summary_row[
                                "p95_ci95_high_ms"
                            ]
                        ),
                    ],

                    "p99_batch_latency_ms_if_n_gte_100":
                        (
                            [
                                float(
                                    summary_row[
                                        "p99_ci95_low_ms_if_n_gte_100"
                                    ]
                                ),
                                float(
                                    summary_row[
                                        "p99_ci95_high_ms_if_n_gte_100"
                                    ]
                                ),
                            ]
                            if expected_n >= 100
                            else None
                        ),

                    "median_throughput_flows_per_second": [
                        float(
                            summary_row[
                                "median_throughput_ci95_low"
                            ]
                        ),
                        float(
                            summary_row[
                                "median_throughput_ci95_high"
                            ]
                        ),
                    ],
                },

                **corrected,
            }
        )


    payload = {
        "schema":
            "stage26_6f1_bootstrap_corrected_uncertainty_v1",

        "bootstrap_protocol": {
            "replicates":
                BOOTSTRAP_REPLICATES,

            "seed":
                BOOTSTRAP_SEED,

            "rng":
                "numpy.random.default_rng_PCG64",

            "condition_local_seed_reset":
                True,

            "same_resample_indices_for_all_targets":
                True,

            "percentile_method":
                PERCENTILE_METHOD,

            "ci_percentiles":
                list(
                    CI_PERCENTILES
                ),
        },

        "conditions":
            output_conditions,
    }


    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )


    with output_path.open(
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            payload,
            f,
            indent=2,
            sort_keys=True,
            allow_nan=False,
        )

        f.write(
            "\n"
        )


if __name__ == "__main__":
    main()
