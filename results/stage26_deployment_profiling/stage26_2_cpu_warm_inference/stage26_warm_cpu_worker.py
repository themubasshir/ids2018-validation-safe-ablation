from __future__ import annotations

import os
import sys
import gc
import json
import hashlib
import traceback
import importlib.util
from pathlib import Path
from time import perf_counter_ns


def atomic_json(path, obj):

    path = Path(
        path
    )

    tmp = Path(
        str(path)
        + ".tmp"
    )

    raw = (
        json.dumps(
            obj,
            indent=2,
            sort_keys=True,
        )
        + "\n"
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


def import_path(
    name,
    path,
):

    spec = (
        importlib.util.spec_from_file_location(
            name,
            str(
                path
            ),
        )
    )

    if (
        spec is None
        or
        spec.loader is None
    ):

        raise RuntimeError(
            f"Unable to import {path}"
        )

    module = (
        importlib.util.module_from_spec(
            spec
        )
    )

    spec.loader.exec_module(
        module
    )

    return module


def sha256_array(array):

    import numpy as np

    a = np.ascontiguousarray(
        array
    )

    h = hashlib.sha256()

    h.update(
        str(
            a.dtype
        ).encode(
            "ascii"
        )
    )

    h.update(
        json.dumps(
            list(
                a.shape
            )
        ).encode(
            "ascii"
        )
    )

    h.update(
        a.tobytes(
            order="C"
        )
    )

    return h.hexdigest()


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
            torch.is_tensor(
                value
            )
            for value in obj.values()
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
                torch.is_tensor(
                    value
                )
                for value in candidate.values()
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
            str(
                path
            ),
            map_location="cpu",
            weights_only=True,
        )

    except TypeError:

        obj = torch.load(
            str(
                path
            ),
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

    if int(
        torch.get_num_threads()
    ) != int(
        thread_count
    ):

        raise RuntimeError(
            "PyTorch intra-op thread mismatch."
        )

    if int(
        torch.get_num_interop_threads()
    ) != 1:

        raise RuntimeError(
            "PyTorch inter-op thread mismatch."
        )


def validate_probability_vector(
    probability,
    *,
    expected_rows,
):

    import numpy as np

    p = np.asarray(
        probability
    ).reshape(
        -1
    )

    if p.shape != (
        int(
            expected_rows
        ),
    ):

        raise RuntimeError(
            f"Unexpected output shape: {p.shape}; "
            f"expected {(int(expected_rows),)}"
        )

    if not np.isfinite(
        p
    ).all():

        raise RuntimeError(
            "Non-finite probability."
        )

    if (
        (p < 0.0).any()
        or
        (p > 1.0).any()
    ):

        raise RuntimeError(
            "Probability outside [0,1]."
        )

    return p


# =============================================================================
# GROUP A INPUT
# =============================================================================

def build_group_a_input(
    *,
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

    if int(
        scaler.n_features_in_
    ) != 70:

        raise RuntimeError(
            "Frozen scaler feature count mismatch."
        )

    derived_seed = (
        int(
            seed
        )
        +
        int(
            batch_size
        )
    )

    rng = np.random.default_rng(
        derived_seed
    )

    Z = rng.normal(
        loc=0.0,
        scale=1.0,
        size=(
            int(
                batch_size
            ),
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

    if not np.isfinite(
        Z
    ).all():

        raise RuntimeError(
            "Non-finite FT synthetic input."
        )

    if not np.isfinite(
        X_raw
    ).all():

        raise RuntimeError(
            "Non-finite tree synthetic input."
        )

    return (
        Z,
        X_raw,
        derived_seed,
    )


# =============================================================================
# GROUP B INPUT
# =============================================================================

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


def build_packet_input(
    *,
    repo,
    batch_size,
    seed,
    need_scaled_float,
):

    import numpy as np

    encoder = import_path(
        "stage26_packet_encoder",
        (
            repo
            / "scripts/stage20_packet_image_encoder.py"
        ),
    )

    derived_seed = (
        int(
            seed
        )
        +
        1_000_000
        +
        int(
            batch_size
        )
    )

    rng = np.random.default_rng(
        derived_seed
    )

    images_uint8 = np.zeros(
        (
            int(
                batch_size
            ),
            1,
            64,
            256,
        ),
        dtype=np.uint8,
    )

    padding_mask = np.zeros(
        (
            int(
                batch_size
            ),
            1,
            64,
            256,
        ),
        dtype=np.bool_,
    )

    for flow_index in range(
        int(
            batch_size
        )
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

            packet_length = int(
                rng.integers(
                    40,
                    257,
                )
            )

            packets.append(
                make_ipv4_packet(
                    rng,
                    protocol,
                    packet_length,
                )
            )

        image, mask = (
            encoder.encode_flow(
                packets
            )
        )

        images_uint8[
            flow_index,
            0,
        ] = image

        padding_mask[
            flow_index,
            0,
        ] = mask


    if need_scaled_float:

        image_model = (
            images_uint8.astype(
                np.float32
            )
            /
            np.float32(
                255.0
            )
        )

        del images_uint8

        return (
            image_model,
            padding_mask,
            derived_seed,
        )


    return (
        images_uint8,
        padding_mask,
        derived_seed,
    )


# =============================================================================
# FT CONSTRUCTION
# =============================================================================

def build_ft_model(
    *,
    ft_module,
    architecture_record,
    checkpoint,
):

    arch = architecture_record[
        "architecture"
    ]

    model = (
        ft_module.NumericFTTransformer(
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
    )

    state = torch_load_state(
        checkpoint
    )

    model.load_state_dict(
        state,
        strict=True,
    )

    model.eval()

    parameter_count = int(
        sum(
            p.numel()
            for p in model.parameters()
            if p.requires_grad
        )
    )

    if parameter_count != 159169:

        raise RuntimeError(
            f"FT parameter count mismatch: {parameter_count}"
        )

    return model


# =============================================================================
# MEASUREMENT
# =============================================================================

def execute_measurement(
    config,
):

    repo = Path(
        config[
            "repo"
        ]
    )

    target = config[
        "target_id"
    ]

    hardware_mode = config[
        "hardware_mode"
    ]

    thread_count = int(
        config[
            "thread_count"
        ]
    )

    affinity = [
        int(
            x
        )
        for x in config[
            "affinity"
        ]
    ]

    batch_size = int(
        config[
            "batch_size"
        ]
    )

    warmup_runs = int(
        config[
            "warmup_runs"
        ]
    )

    timed_runs = int(
        config[
            "timed_runs"
        ]
    )

    seed = int(
        config[
            "measurement_seed"
        ]
    )

    condition_id = config[
        "condition_id"
    ]

    execution_order = int(
        config[
            "execution_order"
        ]
    )


    # -------------------------------------------------------------------------
    # CPU affinity before numerical / ML imports.
    # -------------------------------------------------------------------------

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


    observed_affinity = (
        sorted(
            os.sched_getaffinity(
                0
            )
        )
        if hasattr(
            os,
            "sched_getaffinity",
        )
        else
        None
    )


    if (
        observed_affinity is not None
        and
        observed_affinity != affinity
    ):

        raise RuntimeError(
            f"Affinity mismatch: "
            f"{observed_affinity} != {affinity}"
        )


    # Default CPython GC semantics are preserved.
    gc_enabled = bool(
        gc.isenabled()
    )


    # -------------------------------------------------------------------------
    # Imports + input + model load OUTSIDE timed region.
    # -------------------------------------------------------------------------

    if target in {
        "STAGE16_XGBOOST_TUNED",
        "STAGE16_LIGHTGBM_TUNED",
        "STAGE16_CATBOOST_TUNED",
        "ENS_LGBM_XGB_EQUAL",
    }:

        import numpy as np
        import joblib

        Z, X_raw, derived_seed = (
            build_group_a_input(
                repo=repo,
                batch_size=batch_size,
                seed=seed,
            )
        )


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
                )[:, 1]


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
                )[:, 1]


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
                )[:, 1]


        else:

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

                xgb_p = (
                    xgb_model.predict_proba(
                        X_raw
                    )[:, 1]
                )

                lgb_p = (
                    lgb_model.predict_proba(
                        X_raw
                    )[:, 1]
                )

                return (
                    np.asarray(
                        xgb_p,
                        dtype=np.float64,
                    )
                    +
                    np.asarray(
                        lgb_p,
                        dtype=np.float64,
                    )
                ) / 2.0


    elif target in {
        "FT_BALANCED_5_CHECKPOINT_SOFT_VOTING",
        "FT_BALANCED_SINGLE_RESOURCE_REFERENCE",
    }:

        import numpy as np
        import torch

        configure_torch_threads(
            thread_count
        )

        derived_seed = (
            seed
            +
            batch_size
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

        x = torch.from_numpy(
            Z
        )

        ft_module = import_path(
            "stage26_ft_module",
            (
                repo
                / "results/stage15_transformer_checkpoint/"
                  "ft_transformer_numeric.py"
            ),
        )

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
                (
                    repo
                    / "results/stage15_transformer_checkpoint/"
                      "stage15_4b_models/"
                      "FT_BALANCED_seed_7_best_extended.pt"
                ),

            29:
                (
                    repo
                    / "results/stage15_transformer_checkpoint/"
                      "stage15_4a_models/"
                      "FT_BALANCED_seed_29_best.pt"
                ),

            101:
                (
                    repo
                    / "results/stage15_transformer_checkpoint/"
                      "stage15_4a_models/"
                      "FT_BALANCED_seed_101_best.pt"
                ),

            313:
                (
                    repo
                    / "results/stage15_transformer_checkpoint/"
                      "stage15_4c_models/"
                      "FT_BALANCED_seed_313_best.pt"
                ),

            997:
                (
                    repo
                    / "results/stage15_transformer_checkpoint/"
                      "stage15_4c_models/"
                      "FT_BALANCED_seed_997_best.pt"
                ),
        }

        seeds = (
            [
                7,
                29,
                101,
                313,
                997,
            ]
            if
            target
            ==
            "FT_BALANCED_5_CHECKPOINT_SOFT_VOTING"
            else
            [
                7
            ]
        )

        models = []

        for checkpoint_seed in seeds:

            models.append(
                build_ft_model(
                    ft_module=ft_module,
                    architecture_record=architecture_record,
                    checkpoint=checkpoint_paths[
                        checkpoint_seed
                    ],
                )
            )


        def infer():

            member_probabilities = []

            with torch.inference_mode():

                for model in models:

                    logits = model(
                        x
                    )

                    member_probabilities.append(
                        torch.sigmoid(
                            logits
                        )
                        .detach()
                        .cpu()
                        .numpy()
                    )

            return np.mean(
                np.stack(
                    member_probabilities,
                    axis=0,
                ),
                axis=0,
            )


    elif target == "STAGE20_MASKED_CNN_V1":

        import numpy as np
        import torch

        configure_torch_threads(
            thread_count
        )

        (
            image_np,
            mask_np,
            derived_seed,
        ) = build_packet_input(
            repo=repo,
            batch_size=batch_size,
            seed=seed,
            need_scaled_float=False,
        )

        cnn_module = import_path(
            "stage26_cnn_module",
            (
                repo
                / "scripts/stage20_masked_cnn.py"
            ),
        )

        model = (
            cnn_module.Stage20MaskedCNNv1()
        )

        state = torch_load_state(
            repo
            / "results/stage20_1e_training/"
              "stage20_1e2_epoch10_model_state_dict.pt"
        )

        model.load_state_dict(
            state,
            strict=True,
        )

        model.eval()

        parameter_count = int(
            cnn_module.count_trainable_parameters(
                model
            )
        )

        if parameter_count != 93025:

            raise RuntimeError(
                f"CNN parameter mismatch: {parameter_count}"
            )

        # Authentic frozen CNN boundary:
        # uint8 image, bool mask; float32/255 occurs inside forward().
        image = torch.from_numpy(
            image_np
        )

        mask = torch.from_numpy(
            mask_np
        )


        def infer():

            with torch.inference_mode():

                logits = model(
                    image,
                    mask,
                )

                return (
                    torch.sigmoid(
                        logits
                    )
                    .detach()
                    .cpu()
                    .numpy()
                )


    elif target == "STAGE21_MASKED_VIT_V1":

        import numpy as np
        import torch

        configure_torch_threads(
            thread_count
        )

        (
            image_np,
            mask_np,
            derived_seed,
        ) = build_packet_input(
            repo=repo,
            batch_size=batch_size,
            seed=seed,
            need_scaled_float=True,
        )

        vit_module = import_path(
            "stage26_vit_module",
            (
                repo
                / "scripts/stage21_masked_vit.py"
            ),
        )

        model = (
            vit_module.Stage21MaskedViTv1()
        )

        state = torch_load_state(
            repo
            / "results/stage21_architecture/"
              "stage21_2_epoch10_model_state_dict.pt"
        )

        model.load_state_dict(
            state,
            strict=True,
        )

        model.eval()

        parameter_count = int(
            vit_module.count_trainable_parameters(
                model
            )
        )

        if parameter_count != 91969:

            raise RuntimeError(
                f"ViT parameter mismatch: {parameter_count}"
            )

        # Authentic frozen ViT boundary:
        # already-scaled float32 image + bool mask.
        image = torch.from_numpy(
            image_np
        )

        mask = torch.from_numpy(
            mask_np
        )


        def infer():

            with torch.inference_mode():

                logits = model(
                    image,
                    mask,
                )

                return (
                    torch.sigmoid(
                        logits
                    )
                    .detach()
                    .cpu()
                    .numpy()
                )


    else:

        raise RuntimeError(
            f"Unknown target: {target}"
        )


    # -------------------------------------------------------------------------
    # Exact frozen warmup count.
    # -------------------------------------------------------------------------

    warmup_last_output = None

    for _ in range(
        warmup_runs
    ):

        warmup_last_output = infer()


    warmup_p = validate_probability_vector(
        warmup_last_output,
        expected_rows=batch_size,
    )

    warmup_output_sha256 = (
        sha256_array(
            warmup_p
        )
    )


    # -------------------------------------------------------------------------
    # Exact frozen timed count.
    # -------------------------------------------------------------------------

    elapsed_ns = []

    timed_last_output = None


    for _ in range(
        timed_runs
    ):

        start_ns = (
            perf_counter_ns()
        )

        timed_last_output = infer()

        end_ns = (
            perf_counter_ns()
        )

        elapsed = int(
            end_ns
            -
            start_ns
        )

        if elapsed <= 0:

            raise RuntimeError(
                f"Non-positive elapsed_ns: {elapsed}"
            )

        elapsed_ns.append(
            elapsed
        )


    timed_p = validate_probability_vector(
        timed_last_output,
        expected_rows=batch_size,
    )

    timed_output_sha256 = (
        sha256_array(
            timed_p
        )
    )


    if (
        warmup_output_sha256
        !=
        timed_output_sha256
    ):

        raise RuntimeError(
            "Prediction fingerprint changed between "
            "warmup and timed steady-state execution."
        )


    return {
        "schema":
            "stage26_2_condition_receipt_v1",

        "status":
            "PASS",

        "condition_id":
            condition_id,

        "execution_order":
            execution_order,

        "target_id":
            target,

        "hardware_mode":
            hardware_mode,

        "thread_count":
            thread_count,

        "affinity_requested":
            affinity,

        "affinity_observed":
            observed_affinity,

        "batch_size":
            batch_size,

        "warmup_runs":
            warmup_runs,

        "timed_runs":
            timed_runs,

        "derived_input_seed":
            int(
                derived_seed
            ),

        "python_gc_enabled":
            gc_enabled,

        "elapsed_ns":
            elapsed_ns,

        "warmup_output_sha256":
            warmup_output_sha256,

        "timed_output_sha256":
            timed_output_sha256,

        "timing_clock":
            "time.perf_counter_ns",

        "timing_boundary":
            (
                "prepared_model_input_to_materialized_attack_probability"
            ),

        "memory_profiled":
            False,

        "holdout_accessed":
            False,

        "gpu_used":
            False,
    }


def main():

    config_path = Path(
        sys.argv[
            1
        ]
    )

    config = json.loads(
        config_path.read_text(
            encoding="utf-8"
        )
    )

    result_path = Path(
        config[
            "result_path"
        ]
    )


    try:

        result = execute_measurement(
            config
        )


    except MemoryError as exc:

        result = {
            "schema":
                "stage26_2_condition_receipt_v1",

            "status":
                "RESOURCE_LIMIT_OOM",

            "condition_id":
                config[
                    "condition_id"
                ],

            "execution_order":
                int(
                    config[
                        "execution_order"
                    ]
                ),

            "target_id":
                config[
                    "target_id"
                ],

            "hardware_mode":
                config[
                    "hardware_mode"
                ],

            "thread_count":
                int(
                    config[
                        "thread_count"
                    ]
                ),

            "affinity_requested":
                config[
                    "affinity"
                ],

            "batch_size":
                int(
                    config[
                        "batch_size"
                    ]
                ),

            "warmup_runs":
                int(
                    config[
                        "warmup_runs"
                    ]
                ),

            "timed_runs":
                int(
                    config[
                        "timed_runs"
                    ]
                ),

            "exception_type":
                type(
                    exc
                ).__name__,

            "exception_message":
                str(
                    exc
                ),

            "elapsed_ns":
                [],

            "memory_profiled":
                False,

            "holdout_accessed":
                False,

            "gpu_used":
                False,
        }


    except RuntimeError as exc:

        message = str(
            exc
        ).lower()

        oom_like = (
            "out of memory"
            in
            message
            or
            "cannot allocate memory"
            in
            message
            or
            "bad alloc"
            in
            message
        )


        if oom_like:

            result = {
                "schema":
                    "stage26_2_condition_receipt_v1",

                "status":
                    "RESOURCE_LIMIT_OOM",

                "condition_id":
                    config[
                        "condition_id"
                    ],

                "execution_order":
                    int(
                        config[
                            "execution_order"
                        ]
                    ),

                "target_id":
                    config[
                        "target_id"
                    ],

                "hardware_mode":
                    config[
                        "hardware_mode"
                    ],

                "thread_count":
                    int(
                        config[
                            "thread_count"
                        ]
                    ),

                "affinity_requested":
                    config[
                        "affinity"
                    ],

                "batch_size":
                    int(
                        config[
                            "batch_size"
                        ]
                    ),

                "warmup_runs":
                    int(
                        config[
                            "warmup_runs"
                        ]
                    ),

                "timed_runs":
                    int(
                        config[
                            "timed_runs"
                        ]
                    ),

                "exception_type":
                    type(
                        exc
                    ).__name__,

                "exception_message":
                    str(
                        exc
                    ),

                "elapsed_ns":
                    [],

                "memory_profiled":
                    False,

                "holdout_accessed":
                    False,

                "gpu_used":
                    False,
            }


        else:

            result = {
                "schema":
                    "stage26_2_condition_receipt_v1",

                "status":
                    "WORKER_FAILURE",

                "condition_id":
                    config[
                        "condition_id"
                    ],

                "execution_order":
                    int(
                        config[
                            "execution_order"
                    ]
                ),

                "target_id":
                    config[
                        "target_id"
                    ],

                "hardware_mode":
                    config[
                        "hardware_mode"
                    ],

                "thread_count":
                    int(
                        config[
                            "thread_count"
                    ]
                ),

                "affinity_requested":
                    config[
                        "affinity"
                    ],

                "batch_size":
                    int(
                        config[
                            "batch_size"
                    ]
                ),

                "warmup_runs":
                    int(
                        config[
                            "warmup_runs"
                    ]
                ),

                "timed_runs":
                    int(
                        config[
                            "timed_runs"
                    ]
                ),

                "exception_type":
                    type(
                        exc
                    ).__name__,

                "exception_message":
                    str(
                        exc
                    ),

                "traceback":
                    traceback.format_exc(),

                "elapsed_ns":
                    [],

                "memory_profiled":
                    False,

                "holdout_accessed":
                    False,

                "gpu_used":
                    False,
            }


    except Exception as exc:

        result = {
            "schema":
                "stage26_2_condition_receipt_v1",

            "status":
                "WORKER_FAILURE",

            "condition_id":
                config[
                    "condition_id"
                ],

            "execution_order":
                int(
                    config[
                        "execution_order"
                    ]
                ),

            "target_id":
                config[
                    "target_id"
                ],

            "hardware_mode":
                config[
                    "hardware_mode"
                ],

            "thread_count":
                int(
                    config[
                        "thread_count"
                    ]
                ),

            "affinity_requested":
                config[
                    "affinity"
                ],

            "batch_size":
                int(
                    config[
                        "batch_size"
                    ]
                ),

            "warmup_runs":
                int(
                    config[
                        "warmup_runs"
                    ]
                ),

            "timed_runs":
                int(
                    config[
                        "timed_runs"
                    ]
                ),

            "exception_type":
                type(
                    exc
                ).__name__,

            "exception_message":
                str(
                    exc
                ),

            "traceback":
                traceback.format_exc(),

            "elapsed_ns":
                [],

            "memory_profiled":
                False,

            "holdout_accessed":
                False,

            "gpu_used":
                False,
        }


    atomic_json(
        result_path,
        result,
    )


    # One machine-readable line last.
    print(
        json.dumps(
            {
                "status":
                    result[
                        "status"
                    ],

                "condition_id":
                    result[
                        "condition_id"
                    ],

                "execution_order":
                    result[
                        "execution_order"
                    ],

                "target_id":
                    result[
                        "target_id"
                    ],

                "hardware_mode":
                    result[
                        "hardware_mode"
                    ],

                "batch_size":
                    result[
                        "batch_size"
                    ],
            },
            sort_keys=True,
        ),
        flush=True,
    )


    if result[
        "status"
    ] == "WORKER_FAILURE":

        sys.exit(
            2
        )


if __name__ == "__main__":

    main()
