from __future__ import annotations

import os
import sys
import gc
import json
import time
import queue
import signal
import resource
import threading
import traceback
import importlib.util
from pathlib import Path

import psutil


RSS_SAMPLE_INTERVAL_SECONDS = 0.005


def atomic_json(path, obj):

    path = Path(path)

    tmp = Path(
        str(path)
        +
        ".tmp"
    )

    raw = (
        json.dumps(
            obj,
            indent=2,
            sort_keys=True,
        )
        +
        "\n"
    ).encode(
        "utf-8"
    )


    with tmp.open(
        "wb"
    ) as f:

        f.write(
            raw
        )

        f.flush()

        os.fsync(
            f.fileno()
        )


    os.replace(
        tmp,
        path,
    )


def import_path(name, path):

    spec = importlib.util.spec_from_file_location(
        name,
        str(path),
    )

    if (
        spec is None
        or
        spec.loader is None
    ):

        raise RuntimeError(
            f"Unable to import {path}"
        )


    module = importlib.util.module_from_spec(
        spec
    )

    spec.loader.exec_module(
        module
    )

    return module


def extract_torch_state(obj):

    import torch

    if not isinstance(
        obj,
        dict,
    ):

        raise TypeError(
            f"Unsupported checkpoint root type: {type(obj)}"
        )


    if (
        obj
        and
        all(
            torch.is_tensor(v)
            for v in obj.values()
        )
    ):

        return obj


    for key in [
        "model_state_dict",
        "state_dict",
        "model_state",
        "network_state_dict",
        "model",
    ]:

        candidate = obj.get(
            key
        )


        if (
            isinstance(
                candidate,
                dict,
            )
            and
            candidate
            and
            all(
                torch.is_tensor(v)
                for v in candidate.values()
            )
        ):

            return candidate


    raise RuntimeError(
        "Unable to identify torch state_dict."
    )


def torch_load_state(path):

    import torch

    try:

        obj = torch.load(
            str(path),
            map_location="cpu",
            weights_only=True,
        )


    except TypeError:

        obj = torch.load(
            str(path),
            map_location="cpu",
        )


    return extract_torch_state(
        obj
    )


def configure_torch_threads(
    thread_count,
):

    import torch

    torch.set_num_threads(
        int(
            thread_count
        )
    )


    try:

        torch.set_num_interop_threads(
            1
        )


    except RuntimeError:

        pass


def make_ipv4_packet(
    rng,
    protocol,
    length,
):

    import numpy as np

    packet = bytearray(
        rng.integers(
            0,
            256,
            size=int(
                length
            ),
            dtype=np.uint8,
        ).tobytes()
    )

    packet[
        0
    ] = 0x45

    packet[
        2:4
    ] = int(
        length
    ).to_bytes(
        2,
        "big",
    )

    packet[
        6
    ] = (
        packet[
            6
        ]
        &
        0xE0
    )

    packet[
        7
    ] = 0

    packet[
        9
    ] = int(
        protocol
    )

    return bytes(
        packet
    )


def build_group_a_input(
    repo,
    batch_size,
    seed,
):

    import joblib
    import numpy as np

    scaler = joblib.load(
        repo
        / "results/stage15_transformer_checkpoint/"
          "stage15_2_standard_scaler.joblib"
    )


    derived_seed = (
        int(seed)
        +
        int(batch_size)
    )

    rng = np.random.default_rng(
        derived_seed
    )


    Z = rng.normal(
        0.0,
        1.0,
        size=(
            batch_size,
            70,
        ),
    ).astype(
        np.float32
    )


    mean = np.asarray(
        scaler.mean_,
        dtype=np.float32,
    )

    scale = np.asarray(
        scaler.scale_,
        dtype=np.float32,
    )


    X_raw = (
        mean[
            None,
            :
        ]
        +
        Z
        *
        scale[
            None,
            :
        ]
    ).astype(
        np.float32,
        copy=False,
    )


    return (
        Z,
        X_raw,
    )


def build_packet_input(
    repo,
    batch_size,
    seed,
    need_scaled_float,
):

    import numpy as np

    encoder = import_path(
        "stage26_memory_encoder",
        repo
        / "scripts/stage20_packet_image_encoder.py",
    )


    derived_seed = (
        int(seed)
        +
        1_000_000
        +
        int(batch_size)
    )

    rng = np.random.default_rng(
        derived_seed
    )


    images = np.zeros(
        (
            batch_size,
            1,
            64,
            256,
        ),
        dtype=np.uint8,
    )

    masks = np.zeros(
        (
            batch_size,
            1,
            64,
            256,
        ),
        dtype=np.bool_,
    )


    for i in range(
        batch_size
    ):

        packet_count = int(
            rng.integers(
                1,
                65,
            )
        )

        packets = []


        for _ in range(
            packet_count
        ):

            protocol = (
                6
                if int(
                    rng.integers(
                        0,
                        2,
                    )
                ) == 0
                else 17
            )


            length = int(
                rng.integers(
                    40,
                    257,
                )
            )


            packets.append(
                make_ipv4_packet(
                    rng,
                    protocol,
                    length,
                )
            )


        image, mask = encoder.encode_flow(
            packets
        )


        images[
            i,
            0
        ] = image

        masks[
            i,
            0
        ] = mask


    if need_scaled_float:

        images = (
            images.astype(
                np.float32
            )
            /
            np.float32(
                255.0
            )
        )


    return (
        images,
        masks,
    )


def build_ft_model(
    ft_module,
    architecture_record,
    checkpoint,
):

    arch = architecture_record[
        "architecture"
    ]


    model = ft_module.NumericFTTransformer(
        n_features=int(
            architecture_record[
                "input_predictor_count"
            ]
        ),
        d_token=int(
            arch[
                "d_token"
            ]
        ),
        n_heads=int(
            arch[
                "n_heads"
            ]
        ),
        n_layers=int(
            arch[
                "n_layers"
            ]
        ),
        d_ff=int(
            arch[
                "d_ff"
            ]
        ),
        dropout=float(
            arch[
                "dropout"
            ]
        ),
    )


    model.load_state_dict(
        torch_load_state(
            checkpoint
        ),
        strict=True,
    )


    model.eval()

    return model


def start_rss_sampler(
    process,
    stop_event,
    samples,
):

    while not stop_event.is_set():

        try:

            rss = int(
                process.memory_info().rss
            )

            samples.append(
                rss
            )


        except psutil.NoSuchProcess:

            break


        stop_event.wait(
            RSS_SAMPLE_INTERVAL_SECONDS
        )


def main():

    config = json.loads(
        Path(
            sys.argv[
                1
            ]
        ).read_text(
            encoding="utf-8"
        )
    )


    result_path = Path(
        config[
            "result_path"
        ]
    )


    repo = Path(
        config[
            "repo"
        ]
    )

    target = config[
        "target_id"
    ]

    batch_size = int(
        config[
            "batch_size"
        ]
    )

    thread_count = int(
        config[
            "thread_count"
        ]
    )

    affinity = [
        int(x)
        for x in config[
            "affinity"
        ]
    ]

    seed = int(
        config[
            "measurement_seed"
        ]
    )


    if hasattr(
        os,
        "sched_setaffinity",
    ):

        os.sched_setaffinity(
            0,
            set(
                affinity
            ),
        )


    process = psutil.Process(
        os.getpid()
    )


    # -------------------------------------------------------------------------
    # Required imports + deterministic input preparation.
    # -------------------------------------------------------------------------

    if target in {
        "STAGE16_XGBOOST_TUNED",
        "STAGE16_LIGHTGBM_TUNED",
        "STAGE16_CATBOOST_TUNED",
        "ENS_LGBM_XGB_EQUAL",
    }:

        import numpy as np
        import joblib


        Z, X_raw = build_group_a_input(
            repo,
            batch_size,
            seed,
        )


    elif target in {
        "FT_BALANCED_SINGLE_RESOURCE_REFERENCE",
        "FT_BALANCED_5_CHECKPOINT_SOFT_VOTING",
    }:

        import numpy as np
        import torch


        configure_torch_threads(
            thread_count
        )


        Z, _ = build_group_a_input(
            repo,
            batch_size,
            seed,
        )


        x = torch.from_numpy(
            Z
        )


        ft_module = import_path(
            "stage26_memory_ft",
            repo
            / "results/stage15_transformer_checkpoint/"
              "ft_transformer_numeric.py",
        )


    elif target == "STAGE20_MASKED_CNN_V1":

        import numpy as np
        import torch


        configure_torch_threads(
            thread_count
        )


        image_np, mask_np = build_packet_input(
            repo,
            batch_size,
            seed,
            False,
        )


        image = torch.from_numpy(
            image_np
        )

        mask = torch.from_numpy(
            mask_np
        )


        cnn_module = import_path(
            "stage26_memory_cnn",
            repo
            / "scripts/stage20_masked_cnn.py",
        )


    elif target == "STAGE21_MASKED_VIT_V1":

        import numpy as np
        import torch


        configure_torch_threads(
            thread_count
        )


        image_np, mask_np = build_packet_input(
            repo,
            batch_size,
            seed,
            True,
        )


        image = torch.from_numpy(
            image_np
        )

        mask = torch.from_numpy(
            mask_np
        )


        vit_module = import_path(
            "stage26_memory_vit",
            repo
            / "scripts/stage21_masked_vit.py",
        )


    else:

        raise RuntimeError(
            f"Unknown target: {target}"
        )


    baseline_rss = int(
        process.memory_info().rss
    )


    # -------------------------------------------------------------------------
    # Model load/construction.
    # -------------------------------------------------------------------------

    if target == "STAGE16_XGBOOST_TUNED":

        import xgboost


        model = joblib.load(
            repo
            / "results/stage16_classical_benchmark_checkpoint/"
              "stage16_3_tuned_models/XGBOOST_tuned.joblib"
        )


        model.set_params(
            n_jobs=thread_count
        )


        def infer():

            return model.predict_proba(
                X_raw
            )[
                :,
                1
            ]


    elif target == "STAGE16_LIGHTGBM_TUNED":

        import lightgbm


        model = joblib.load(
            repo
            / "results/stage16_classical_benchmark_checkpoint/"
              "stage16_3_tuned_models/LIGHTGBM_tuned.joblib"
        )


        model.set_params(
            n_jobs=thread_count
        )


        def infer():

            return model.predict_proba(
                X_raw
            )[
                :,
                1
            ]


    elif target == "STAGE16_CATBOOST_TUNED":

        import catboost


        model = joblib.load(
            repo
            / "results/stage16_classical_benchmark_checkpoint/"
              "stage16_3_tuned_models/CATBOOST_tuned.joblib"
        )


        def infer():

            return model.predict_proba(
                X_raw,
                thread_count=thread_count,
            )[
                :,
                1
            ]


    elif target == "ENS_LGBM_XGB_EQUAL":

        import xgboost
        import lightgbm


        xgb_model = joblib.load(
            repo
            / "results/stage16_classical_benchmark_checkpoint/"
              "stage16_3_tuned_models/XGBOOST_tuned.joblib"
        )

        lgb_model = joblib.load(
            repo
            / "results/stage16_classical_benchmark_checkpoint/"
              "stage16_3_tuned_models/LIGHTGBM_tuned.joblib"
        )


        xgb_model.set_params(
            n_jobs=thread_count
        )

        lgb_model.set_params(
            n_jobs=thread_count
        )


        def infer():

            a = xgb_model.predict_proba(
                X_raw
            )[
                :,
                1
            ]

            b = lgb_model.predict_proba(
                X_raw
            )[
                :,
                1
            ]

            return (
                np.asarray(
                    a,
                    dtype=np.float64,
                )
                +
                np.asarray(
                    b,
                    dtype=np.float64,
                )
            ) / 2.0


    elif target in {
        "FT_BALANCED_SINGLE_RESOURCE_REFERENCE",
        "FT_BALANCED_5_CHECKPOINT_SOFT_VOTING",
    }:

        architecture_record = json.loads(
            (
                repo
                / "results/stage15_transformer_checkpoint/"
                  "stage15_4c_frozen_architecture.json"
            ).read_text(
                encoding="utf-8"
            )
        )


        checkpoint_paths = {
            7:
                repo
                / "results/stage15_transformer_checkpoint/"
                  "stage15_4b_models/"
                  "FT_BALANCED_seed_7_best_extended.pt",

            29:
                repo
                / "results/stage15_transformer_checkpoint/"
                  "stage15_4a_models/"
                  "FT_BALANCED_seed_29_best.pt",

            101:
                repo
                / "results/stage15_transformer_checkpoint/"
                  "stage15_4a_models/"
                  "FT_BALANCED_seed_101_best.pt",

            313:
                repo
                / "results/stage15_transformer_checkpoint/"
                  "stage15_4c_models/"
                  "FT_BALANCED_seed_313_best.pt",

            997:
                repo
                / "results/stage15_transformer_checkpoint/"
                  "stage15_4c_models/"
                  "FT_BALANCED_seed_997_best.pt",
        }


        checkpoint_seeds = (
            [
                7
            ]
            if target
            ==
            "FT_BALANCED_SINGLE_RESOURCE_REFERENCE"
            else
            [
                7,
                29,
                101,
                313,
                997,
            ]
        )


        models = [
            build_ft_model(
                ft_module,
                architecture_record,
                checkpoint_paths[
                    checkpoint_seed
                ],
            )
            for checkpoint_seed
            in checkpoint_seeds
        ]


        def infer():

            outputs = []


            with torch.inference_mode():

                for model in models:

                    outputs.append(
                        torch.sigmoid(
                            model(
                                x
                            )
                        )
                        .detach()
                        .cpu()
                        .numpy()
                    )


            return np.mean(
                np.stack(
                    outputs,
                    axis=0,
                ),
                axis=0,
            )


    elif target == "STAGE20_MASKED_CNN_V1":

        model = (
            cnn_module.Stage20MaskedCNNv1()
        )


        model.load_state_dict(
            torch_load_state(
                repo
                / "results/stage20_1e_training/"
                  "stage20_1e2_epoch10_model_state_dict.pt"
            ),
            strict=True,
        )


        model.eval()


        def infer():

            with torch.inference_mode():

                return (
                    torch.sigmoid(
                        model(
                            image,
                            mask,
                        )
                    )
                    .detach()
                    .cpu()
                    .numpy()
                )


    elif target == "STAGE21_MASKED_VIT_V1":

        model = (
            vit_module.Stage21MaskedViTv1()
        )


        model.load_state_dict(
            torch_load_state(
                repo
                / "results/stage21_architecture/"
                  "stage21_2_epoch10_model_state_dict.pt"
            ),
            strict=True,
        )


        model.eval()


        def infer():

            with torch.inference_mode():

                return (
                    torch.sigmoid(
                        model(
                            image,
                            mask,
                        )
                    )
                    .detach()
                    .cpu()
                    .numpy()
                )


    loaded_rss = int(
        process.memory_info().rss
    )


    # -------------------------------------------------------------------------
    # 5 ms sampled memory-only inference.
    # Exactly ONE inference pass.
    # Timing is intentionally not measured.
    # -------------------------------------------------------------------------

    samples = [
        loaded_rss
    ]

    stop_event = threading.Event()


    sampler = threading.Thread(
        target=start_rss_sampler,
        args=(
            process,
            stop_event,
            samples,
        ),
        daemon=True,
    )


    sampler.start()


    try:

        output = infer()


    finally:

        # Explicit post-inference RSS sample.
        try:

            samples.append(
                int(
                    process.memory_info().rss
                )
            )


        except Exception:

            pass


        stop_event.set()

        sampler.join(
            timeout=1.0
        )


    # Ensure output materialized.
    import numpy as np


    output = np.asarray(
        output
    ).reshape(
        -1
    )


    if output.shape != (
        batch_size,
    ):

        raise RuntimeError(
            f"Unexpected output shape: {output.shape}"
        )


    if not np.isfinite(
        output
    ).all():

        raise RuntimeError(
            "Non-finite model output."
        )


    peak_rss = int(
        max(
            samples
        )
    )


    ru = resource.getrusage(
        resource.RUSAGE_SELF
    )


    # Linux ru_maxrss is KiB.
    ru_maxrss_bytes = int(
        ru.ru_maxrss
        *
        1024
    )


    result = {
        "schema":
            "stage26_3_memory_observation_v1",

        "status":
            "PASS",

        "memory_execution_order":
            int(
                config[
                    "memory_execution_order"
                ]
            ),

        "source_cpu_execution_order":
            int(
                config[
                    "source_cpu_execution_order"
                ]
            ),

        "condition_id":
            config[
                "condition_id"
            ],

        "target_id":
            target,

        "hardware_mode":
            config[
                "hardware_mode"
            ],

        "thread_count":
            thread_count,

        "affinity_requested":
            affinity,

        "batch_size":
            batch_size,

        "memory_repetition":
            int(
                config[
                    "memory_repetition"
                ]
            ),

        "rss_sampling_interval_ms":
            5,

        "rss_sample_count":
            len(
                samples
            ),

        "baseline_rss_bytes":
            baseline_rss,

        "loaded_rss_bytes":
            loaded_rss,

        "peak_rss_bytes":
            peak_rss,

        "delta_model_rss_bytes":
            int(
                loaded_rss
                -
                baseline_rss
            ),

        "delta_peak_rss_bytes":
            int(
                peak_rss
                -
                baseline_rss
            ),

        "ru_maxrss_bytes_descriptive":
            ru_maxrss_bytes,

        "timing_performed":
            False,

        "inference_passes":
            1,

        "holdout_accessed":
            False,

        "gpu_used":
            False,
    }


    atomic_json(
        result_path,
        result,
    )


if __name__ == "__main__":

    main()
