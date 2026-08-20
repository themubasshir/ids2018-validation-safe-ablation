#!/usr/bin/env python3
from __future__ import annotations

import os
import sys
import json
import time
import hashlib
import importlib.util
from pathlib import Path

import numpy as np


ROWS = 64
COLS = 256


def atomic_json(path: Path, obj) -> None:

    path = Path(path)
    tmp = Path(str(path) + ".tmp")

    with tmp.open("w", encoding="utf-8") as fh:

        json.dump(
            obj,
            fh,
            indent=2,
            sort_keys=True,
        )

        fh.write("\n")
        fh.flush()
        os.fsync(fh.fileno())

    os.replace(tmp, path)


def fingerprint(
    image: np.ndarray,
    padding_mask: np.ndarray,
) -> str:

    h = hashlib.sha256()

    h.update(
        np.ascontiguousarray(
            image
        ).tobytes()
    )

    h.update(
        np.ascontiguousarray(
            padding_mask
        ).tobytes()
    )

    return h.hexdigest()


class RepresentationSource:

    def __init__(self, corpus_dir: Path):

        self.corpus_dir = Path(corpus_dir)

        self.encoded_path = (
            self.corpus_dir
            / "encoded_bytes.bin"
        )

        self.offsets_path = (
            self.corpus_dir
            / "flow_offsets.npy"
        )

        self.lengths_path = (
            self.corpus_dir
            / "packet_lengths.npy"
        )

        for path in (
            self.encoded_path,
            self.offsets_path,
            self.lengths_path,
        ):

            if not path.is_file():

                raise FileNotFoundError(
                    path
                )

        self.flow_offsets = np.load(
            self.offsets_path,
            mmap_mode="r",
            allow_pickle=False,
        )

        self.packet_lengths = np.load(
            self.lengths_path,
            mmap_mode="r",
            allow_pickle=False,
        )

        self.encoded_bytes = np.memmap(
            self.encoded_path,
            dtype=np.uint8,
            mode="r",
        )

        if (
            self.packet_lengths.ndim != 2
            or
            self.packet_lengths.shape[1] != ROWS
        ):

            raise ValueError(
                "packet_lengths.npy must be [N,64]"
            )

        self.n = int(
            self.packet_lengths.shape[0]
        )

        if self.flow_offsets.shape != (
            self.n + 1,
        ):

            raise ValueError(
                "flow_offsets.npy must be [N+1]"
            )

        if self.packet_lengths.dtype != np.uint16:

            raise ValueError(
                "packet_lengths dtype must be uint16"
            )

        if self.flow_offsets.dtype != np.uint64:

            raise ValueError(
                "flow_offsets dtype must be uint64"
            )

        if int(
            self.flow_offsets[0]
        ) != 0:

            raise ValueError(
                "first offset must be zero"
            )

        if int(
            self.flow_offsets[-1]
        ) != int(
            self.encoded_bytes.size
        ):

            raise ValueError(
                "final offset != encoded byte count"
            )


    def reconstruct(
        self,
        index: int,
    ) -> tuple[np.ndarray, np.ndarray]:

        index = int(index)

        if index < 0:
            index += self.n

        if index < 0 or index >= self.n:

            raise IndexError(
                index
            )

        lengths = np.asarray(
            self.packet_lengths[index],
            dtype=np.uint16,
        )

        if np.any(
            lengths > COLS
        ):

            raise ValueError(
                "packet length exceeds 256"
            )

        # Frozen geometry: retained packet rows are contiguous from row 0.
        zero_seen = False

        for value in lengths.tolist():

            value = int(value)

            if value == 0:

                zero_seen = True

            elif zero_seen:

                raise ValueError(
                    "positive packet length after zero-padding row"
                )

        start = int(
            self.flow_offsets[index]
        )

        end = int(
            self.flow_offsets[index + 1]
        )

        expected = int(
            lengths.astype(
                np.uint64
            ).sum()
        )

        if end - start != expected:

            raise ValueError(
                "offset delta != sum(packet_lengths)"
            )

        image = np.zeros(
            (
                ROWS,
                COLS,
            ),
            dtype=np.uint8,
        )

        padding_mask = np.zeros(
            (
                ROWS,
                COLS,
            ),
            dtype=np.bool_,
        )

        cursor = start

        for row_index, packet_length in enumerate(
            lengths.tolist()
        ):

            packet_length = int(
                packet_length
            )

            if packet_length == 0:
                continue

            next_cursor = (
                cursor
                +
                packet_length
            )

            image[
                row_index,
                :packet_length,
            ] = self.encoded_bytes[
                cursor:
                next_cursor
            ]

            padding_mask[
                row_index,
                :packet_length,
            ] = True

            cursor = next_cursor

        if cursor != end:

            raise ValueError(
                "byte traversal ended at unexpected offset"
            )

        return (
            image,
            padding_mask,
        )


    def materialize_batch(
        self,
        indices: np.ndarray,
    ) -> tuple[np.ndarray, np.ndarray]:

        indices = np.asarray(
            indices,
            dtype=np.int64,
        ).reshape(-1)

        batch_size = int(
            indices.size
        )

        images = np.zeros(
            (
                batch_size,
                ROWS,
                COLS,
            ),
            dtype=np.uint8,
        )

        padding_masks = np.zeros(
            (
                batch_size,
                ROWS,
                COLS,
            ),
            dtype=np.bool_,
        )

        for batch_index, flow_index in enumerate(
            indices.tolist()
        ):

            image, padding_mask = self.reconstruct(
                int(
                    flow_index
                )
            )

            images[
                batch_index
            ] = image

            padding_masks[
                batch_index
            ] = padding_mask

        return (
            images,
            padding_masks,
        )


def import_module(
    name: str,
    path: Path,
):

    spec = importlib.util.spec_from_file_location(
        name,
        path,
    )

    if spec is None or spec.loader is None:

        raise RuntimeError(
            f"unable to import {path}"
        )

    module = importlib.util.module_from_spec(
        spec
    )

    spec.loader.exec_module(
        module
    )

    return module



class _LabelNeutralValidationShim:
    """
    No-I/O compatibility object for the historical reconstruct() third output.

    Stage26 equivalence compares ONLY historical outputs 0 and 1:
        image, padding_mask

    The historical method nevertheless reads self.labels[index] after those
    representation outputs have already been constructed. Returning uint8(0)
    allows that unrelated third-output path to complete without opening
    labels.npy.
    """

    def __getitem__(
        self,
        index,
    ):

        _ = int(
            index
        )

        return np.uint8(
            0
        )


def run_equivalence(
    cfg: dict,
    source: RepresentationSource,
) -> dict:

    historical_module = import_module(
        "stage26_historical_compact_loader",
        Path(
            cfg[
                "historical_loader_path"
            ]
        ),
    )

    historical_class = getattr(
        historical_module,
        cfg[
            "historical_loader_class"
        ],
    )

    # ---------------------------------------------------------------------
    # LABEL-FREE HISTORICAL EQUIVALENCE ADAPTER
    #
    # Do NOT invoke Stage20CompactCorpus.__init__ because the historical
    # constructor requires labels.npy. The frozen Stage26 representation
    # boundary explicitly forbids label access.
    #
    # reconstruct() uses exactly five object attributes:
    #   _n, packet_lengths, flow_offsets, encoded_bytes, labels
    #
    # The first four are bound directly to this worker's exact authoritative
    # representation source. The fifth is a no-I/O neutral shim used solely
    # by the historical method's third output after image/mask construction.
    # ---------------------------------------------------------------------

    historical = historical_class.__new__(
        historical_class
    )

    historical._n = source.n

    historical.packet_lengths = (
        source.packet_lengths
    )

    historical.flow_offsets = (
        source.flow_offsets
    )

    historical.encoded_bytes = (
        source.encoded_bytes
    )

    historical.labels = (
        _LabelNeutralValidationShim()
    )

    start_index = int(
        cfg[
            "start_index"
        ]
    )

    flow_count = int(
        cfg[
            "flow_count"
        ]
    )

    aggregate = hashlib.sha256()

    for flow_index in range(
        start_index,
        start_index + flow_count,
    ):

        new_image, new_mask = (
            source.reconstruct(
                flow_index
            )
        )

        historical_result = historical.reconstruct(
            flow_index
        )

        if not isinstance(
            historical_result,
            tuple,
        ):

            raise RuntimeError(
                "historical reconstruct() did not return tuple"
            )

        if len(
            historical_result
        ) < 2:

            raise RuntimeError(
                "historical reconstruct() returned fewer than 2 objects"
            )

        old_image = np.asarray(
            historical_result[
                0
            ]
        )

        old_mask = np.asarray(
            historical_result[
                1
            ]
        )

        if old_image.shape != (
            ROWS,
            COLS,
        ):

            raise RuntimeError(
                f"historical image shape mismatch at {flow_index}"
            )

        if old_mask.shape != (
            ROWS,
            COLS,
        ):

            raise RuntimeError(
                f"historical padding-mask shape mismatch at {flow_index}"
            )

        if old_image.dtype != np.uint8:

            raise RuntimeError(
                f"historical image dtype mismatch at {flow_index}"
            )

        if old_mask.dtype != np.bool_:

            raise RuntimeError(
                f"historical mask dtype mismatch at {flow_index}"
            )

        if not np.array_equal(
            new_image,
            old_image,
        ):

            raise RuntimeError(
                f"image equivalence failure at flow {flow_index}"
            )

        if not np.array_equal(
            new_mask,
            old_mask,
        ):

            raise RuntimeError(
                f"padding-mask equivalence failure at flow {flow_index}"
            )

        aggregate.update(
            np.ascontiguousarray(
                new_image
            ).tobytes()
        )

        aggregate.update(
            np.ascontiguousarray(
                new_mask
            ).tobytes()
        )

    return {
        "status":
            "PASS",

        "mode":
            "VALIDATE_EQUIVALENCE",

        "start_index":
            start_index,

        "flow_count":
            flow_count,

        "end_index_exclusive":
            start_index + flow_count,

        "representation_fingerprint_sha256":
            aggregate.hexdigest(),

        "timing_performed":
            False,

        "historical_constructor_invoked":
            False,

        "historical_labels_file_opened":
            False,

        "label_neutral_validation_shim_used":
            True,

        "historical_outputs_compared": [
            "image",
            "padding_mask",
        ],

        "historical_label_output_compared":
            False,

        "gpu_used":
            False,
    }


def run_benchmark(
    cfg: dict,
    source: RepresentationSource,
) -> dict:

    start_index = int(
        cfg[
            "start_index"
        ]
    )

    batch_size = int(
        cfg[
            "batch_size"
        ]
    )

    warmup_runs = int(
        cfg[
            "warmup_runs"
        ]
    )

    timed_runs = int(
        cfg[
            "timed_runs"
        ]
    )

    indices = np.arange(
        start_index,
        start_index + batch_size,
        dtype=np.int64,
    )

    warm_fingerprint = None

    for _ in range(
        warmup_runs
    ):

        images, masks = (
            source.materialize_batch(
                indices
            )
        )

        # Outside any timer.
        warm_fingerprint = fingerprint(
            images,
            masks,
        )

    observations = []

    reference_fingerprint = None

    for iteration in range(
        1,
        timed_runs + 1,
    ):

        start_ns = time.perf_counter_ns()

        images, masks = (
            source.materialize_batch(
                indices
            )
        )

        end_ns = time.perf_counter_ns()

        elapsed_ns = int(
            end_ns
            -
            start_ns
        )

        if elapsed_ns <= 0:

            raise RuntimeError(
                "non-positive elapsed time"
            )


        elapsed_seconds = (
            elapsed_ns
            /
            1_000_000_000.0
        )

        observations.append(
            {
                "iteration_index":
                    iteration,

                "elapsed_ns":
                    elapsed_ns,

                "elapsed_seconds":
                    elapsed_seconds,

                "flows":
                    batch_size,

                "flows_per_second":
                    (
                        batch_size
                        /
                        elapsed_seconds
                    ),

                "image_output_bytes":
                    int(
                        images.nbytes
                    ),

                "padding_mask_output_bytes":
                    int(
                        masks.nbytes
                    ),

                "total_output_bytes":
                    int(
                        images.nbytes
                        +
                        masks.nbytes
                    ),
            }
        )

    # Stage26-8B sensitivity V3:
    # perform full-output integrity read only AFTER all timed iterations.
    # This removes the historical inter-iteration fingerprint/cache-state
    # perturbation while preserving the exact materialization timer boundary.
    if not observations:

        raise RuntimeError(
            "no timed observations produced"
        )

    reference_fingerprint = fingerprint(
        images,
        masks,
    )

    if (
        warm_fingerprint is not None
        and
        reference_fingerprint
        !=
        warm_fingerprint
    ):

        raise RuntimeError(
            "final timed representation differs from final warmup representation"
        )


    return {
        "status":
            "PASS",

        "mode":
            "BENCHMARK_TIMED",

        "start_index":
            start_index,

        "batch_size":
            batch_size,

        "end_index_exclusive":
            start_index + batch_size,

        "warmup_runs":
            warmup_runs,

        "timed_runs":
            timed_runs,

        "representation_fingerprint_sha256":
            reference_fingerprint,

        "warm_representation_fingerprint_sha256":
            warm_fingerprint,

        "observations":
            observations,

        "timing_performed":
            True,

        "float32_div255_performed":
            False,

        "model_loaded":
            False,

        "gpu_used":
            False,
    }


def main():

    if len(
        sys.argv
    ) != 2:

        raise SystemExit(
            "usage: stage26_representation_worker_v1.py CONFIG.json"
        )

    config_path = Path(
        sys.argv[
            1
        ]
    )

    cfg = json.loads(
        config_path.read_text(
            encoding="utf-8"
        )
    )

    affinity = cfg.get(
        "affinity"
    )

    if affinity is not None:

        if not hasattr(
            os,
            "sched_setaffinity",
        ):

            raise RuntimeError(
                "sched_setaffinity unavailable"
            )

        os.sched_setaffinity(
            0,
            {
                int(cpu)
                for cpu in affinity
            },
        )

    source = RepresentationSource(
        Path(
            cfg[
                "corpus_dir"
            ]
        )
    )

    if source.n != int(
        cfg[
            "expected_flow_count"
        ]
    ):

        raise RuntimeError(
            "corpus flow count mismatch"
        )

    mode = cfg[
        "mode"
    ]

    if mode == "VALIDATE_EQUIVALENCE":

        result = run_equivalence(
            cfg,
            source,
        )

    elif mode == "BENCHMARK_TIMED":

        result = run_benchmark(
            cfg,
            source,
        )

    else:

        raise RuntimeError(
            f"unknown mode: {mode}"
        )

    result.update(
        {
            "schema":
                "stage26_representation_worker_result_v3",

            "worker_pid":
                os.getpid(),

            "population_flow_count":
                source.n,

            "image_shape_per_flow":
                [
                    ROWS,
                    COLS,
                ],

            "image_dtype":
                "uint8",

            "padding_mask_shape_per_flow":
                [
                    ROWS,
                    COLS,
                ],

            "padding_mask_dtype":
                "bool",

            "corpus_created_or_modified":
                False,

            "pcap_accessed":
                False,

            "labels_accessed":
                False,
        }
    )

    atomic_json(
        Path(
            cfg[
                "result_path"
            ]
        ),
        result,
    )


if __name__ == "__main__":
    main()
