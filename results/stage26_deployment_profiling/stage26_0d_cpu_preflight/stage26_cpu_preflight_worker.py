from __future__ import annotations

import os
import sys
import json
import hashlib
import importlib.util
from pathlib import Path


# =============================================================================
# No performance timing is permitted in this worker.
# =============================================================================

FORBIDDEN_CLOCK_NAMES = [
    "perf_counter",
    "monotonic",
    "process_time",
    "thread_time",
    "time_ns",
]


def sha256_array(array):
    import numpy as np

    a = np.ascontiguousarray(
        array
    )

    h = hashlib.sha256()

    h.update(
        str(
            a.dtype
        ).encode("ascii")
    )

    h.update(
        json.dumps(
            list(
                a.shape
            )
        ).encode("ascii")
    )

    h.update(
        a.tobytes(
            order="C"
        )
    )

    return h.hexdigest()


def import_path(name, path):

    spec = importlib.util.spec_from_file_location(
        name,
        str(path),
    )

    if spec is None or spec.loader is None:
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
            f"Checkpoint root type unsupported: {type(obj)}"
        )

    # Direct state_dict.
    if obj and all(
        torch.is_tensor(v)
        for v in obj.values()
    ):
        return (
            obj,
            "DIRECT_STATE_DICT",
        )

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
            return (
                candidate,
                key,
            )

    raise RuntimeError(
        "Unable to identify torch state_dict layout. "
        f"Top-level keys={list(obj.keys())[:30]}"
    )


def torch_load_state(path):

    import torch

    try:
        obj = torch.load(
            str(path),
            map_location="cpu",
            weights_only=True,
        )

        load_mode = (
            "torch.load(weights_only=True)"
        )

    except TypeError:

        obj = torch.load(
            str(path),
            map_location="cpu",
        )

        load_mode = (
            "torch.load(default)"
        )

    state, state_layout = (
        extract_torch_state(
            obj
        )
    )

    return (
        state,
        load_mode,
        state_layout,
    )


def configure_torch_threads(thread_count):

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
        # This is still checked below. A mismatch fails the preflight.
        pass

    return {
        "torch_num_threads":
            int(
                torch.get_num_threads()
            ),

        "torch_num_interop_threads":
            int(
                torch.get_num_interop_threads()
            ),
    }


def build_group_a_input(
    *,
    repo,
    batch_size,
    seed,
):

    import joblib
    import numpy as np

    scaler_path = (
        repo
        / "results/stage15_transformer_checkpoint/"
          "stage15_2_standard_scaler.joblib"
    )

    scaler = joblib.load(
        scaler_path
    )

    if int(
        scaler.n_features_in_
    ) != 70:
        raise RuntimeError(
            "Frozen scaler does not have 70 features."
        )

    # Frozen implementation of:
    # "deterministic from frozen seed derived from batch size"
    #
    # No performance result is consulted.
    derived_seed = (
        int(seed)
        +
        int(batch_size)
    )

    rng = np.random.default_rng(
        derived_seed
    )

    Z = rng.normal(
        loc=0.0,
        scale=1.0,
        size=(
            int(batch_size),
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
        mean[None, :]
        +
        Z
        *
        scale[None, :]
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

    return {
        "Z": Z,
        "X_raw": X_raw,
        "derived_seed": derived_seed,
    }


def make_ipv4_packet(
    rng,
    protocol,
    length,
):

    import numpy as np

    if length < 40:
        raise ValueError(
            "Synthetic packet length must be >=40."
        )

    packet = bytearray(
        rng.integers(
            0,
            256,
            size=int(length),
            dtype=np.uint8,
        ).tobytes()
    )

    # IPv4 + IHL 5.
    packet[0] = 0x45

    # Total length.
    packet[2:4] = int(
        length
    ).to_bytes(
        2,
        "big",
    )

    # Fragment offset = zero.
    packet[6] = (
        packet[6]
        &
        0xE0
    )

    packet[7] = 0

    # Protocol 6 TCP / 17 UDP.
    packet[9] = int(
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
        int(seed)
        +
        1_000_000
        +
        int(batch_size)
    )

    rng = np.random.default_rng(
        derived_seed
    )

    images_uint8 = np.zeros(
        (
            int(batch_size),
            1,
            64,
            256,
        ),
        dtype=np.uint8,
    )

    masks = np.zeros(
        (
            int(batch_size),
            1,
            64,
            256,
        ),
        dtype=np.bool_,
    )

    for flow_idx in range(
        int(batch_size)
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
            flow_idx,
            0,
        ] = image

        masks[
            flow_idx,
            0,
        ] = mask

    images_scaled = (
        images_uint8.astype(
            np.float32
        )
        /
        np.float32(
            255.0
        )
    )

    return {
        "image_uint8":
            images_uint8,

        "image_scaled":
            images_scaled,

        "padding_mask":
            masks,

        "derived_seed":
            derived_seed,
    }


def validate_probability_vector(
    probabilities,
    *,
    expected_rows,
):

    import numpy as np

    p = np.asarray(
        probabilities
    )

    p = p.reshape(
        -1
    )

    if p.shape != (
        int(expected_rows),
    ):
        raise RuntimeError(
            f"Unexpected probability shape: {p.shape}"
        )

    if not np.isfinite(
        p
    ).all():
        raise RuntimeError(
            "Non-finite prediction encountered."
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


def load_ft_model(
    *,
    repo,
    checkpoint_path,
):

    import torch

    ft_module = import_path(
        "stage26_ft_transformer",
        (
            repo
            / "results/stage15_transformer_checkpoint/"
              "ft_transformer_numeric.py"
        ),
    )

    arch_path = (
        repo
        / "results/stage15_transformer_checkpoint/"
          "stage15_4c_frozen_architecture.json"
    )

    arch_record = json.loads(
        arch_path.read_text(
            encoding="utf-8"
        )
    )

    arch = arch_record[
        "architecture"
    ]

    model = ft_module.NumericFTTransformer(
        n_features=int(
            arch_record[
                "input_predictor_count"
            ]
        ),
        d_token=int(
            arch["d_token"]
        ),
        n_heads=int(
            arch["n_heads"]
        ),
        n_layers=int(
            arch["n_layers"]
        ),
        d_ff=int(
            arch["d_ff"]
        ),
        dropout=float(
            arch["dropout"]
        ),
    )

    state, load_mode, layout = (
        torch_load_state(
            checkpoint_path
        )
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
            "FT parameter count mismatch: "
            f"{parameter_count}"
        )

    return (
        model,
        parameter_count,
        load_mode,
        layout,
    )


def main():

    config_path = Path(
        sys.argv[1]
    )

    config = json.loads(
        config_path.read_text(
            encoding="utf-8"
        )
    )

    repo = Path(
        config["repo"]
    )

    target = config[
        "target_id"
    ]

    hardware_mode = config[
        "hardware_mode"
    ]

    thread_count = int(
        config["thread_count"]
    )

    affinity = [
        int(x)
        for x in config[
            "affinity"
        ]
    ]

    batch_size = int(
        config.get(
            "batch_size",
            1,
        )
    )

    seed = int(
        config["measurement_seed"]
    )


    # -------------------------------------------------------------------------
    # Freeze CPU affinity BEFORE framework import.
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
        else None
    )


    result = {
        "status": "STARTED",
        "target_id": target,
        "hardware_mode": hardware_mode,
        "thread_count_requested": thread_count,
        "affinity_requested": affinity,
        "affinity_observed": observed_affinity,
        "batch_size": batch_size,
        "timing_performed": False,
        "memory_profiling_performed": False,
        "holdout_accessed": False,
        "gpu_used": False,
    }


    if (
        observed_affinity is not None
        and
        observed_affinity != affinity
    ):
        raise RuntimeError(
            f"Affinity mismatch: {observed_affinity} != {affinity}"
        )


    # -------------------------------------------------------------------------
    # Group A classical models
    # -------------------------------------------------------------------------

    if target in {
        "STAGE16_XGBOOST_TUNED",
        "STAGE16_LIGHTGBM_TUNED",
        "STAGE16_CATBOOST_TUNED",
        "ENS_LGBM_XGB_EQUAL",
    }:

        import joblib
        import numpy as np

        inputs = build_group_a_input(
            repo=repo,
            batch_size=batch_size,
            seed=seed,
        )

        X = inputs[
            "X_raw"
        ]

        result[
            "derived_input_seed"
        ] = inputs[
            "derived_seed"
        ]

        result[
            "input_shape"
        ] = list(
            X.shape
        )

        result[
            "input_dtype"
        ] = str(
            X.dtype
        )


        if target == "STAGE16_XGBOOST_TUNED":

            import xgboost

            path = (
                repo
                / "results/stage16_classical_benchmark_checkpoint/"
                  "stage16_3_tuned_models/XGBOOST_tuned.joblib"
            )

            model = joblib.load(
                path
            )

            if hasattr(
                model,
                "set_params",
            ):
                model.set_params(
                    n_jobs=thread_count
                )

            probabilities = (
                model.predict_proba(
                    X
                )[:, 1]
            )

            result[
                "framework_version"
            ] = xgboost.__version__

            result[
                "model_class"
            ] = (
                model.__class__.__module__
                + "."
                + model.__class__.__name__
            )


        elif target == "STAGE16_LIGHTGBM_TUNED":

            import lightgbm

            path = (
                repo
                / "results/stage16_classical_benchmark_checkpoint/"
                  "stage16_3_tuned_models/LIGHTGBM_tuned.joblib"
            )

            model = joblib.load(
                path
            )

            if hasattr(
                model,
                "set_params",
            ):
                model.set_params(
                    n_jobs=thread_count
                )

            probabilities = (
                model.predict_proba(
                    X
                )[:, 1]
            )

            result[
                "framework_version"
            ] = lightgbm.__version__

            result[
                "model_class"
            ] = (
                model.__class__.__module__
                + "."
                + model.__class__.__name__
            )


        elif target == "STAGE16_CATBOOST_TUNED":

            import catboost

            path = (
                repo
                / "results/stage16_classical_benchmark_checkpoint/"
                  "stage16_3_tuned_models/CATBOOST_tuned.joblib"
            )

            model = joblib.load(
                path
            )

            probabilities = (
                model.predict_proba(
                    X,
                    thread_count=thread_count,
                )[:, 1]
            )

            result[
                "framework_version"
            ] = catboost.__version__

            result[
                "model_class"
            ] = (
                model.__class__.__module__
                + "."
                + model.__class__.__name__
            )


        else:

            import xgboost
            import lightgbm

            xgb_path = (
                repo
                / "results/stage16_classical_benchmark_checkpoint/"
                  "stage16_3_tuned_models/XGBOOST_tuned.joblib"
            )

            lgb_path = (
                repo
                / "results/stage16_classical_benchmark_checkpoint/"
                  "stage16_3_tuned_models/LIGHTGBM_tuned.joblib"
            )

            xgb_model = joblib.load(
                xgb_path
            )

            lgb_model = joblib.load(
                lgb_path
            )

            if hasattr(
                xgb_model,
                "set_params",
            ):
                xgb_model.set_params(
                    n_jobs=thread_count
                )

            if hasattr(
                lgb_model,
                "set_params",
            ):
                lgb_model.set_params(
                    n_jobs=thread_count
                )

            xgb_p = (
                xgb_model.predict_proba(
                    X
                )[:, 1]
            )

            lgb_p = (
                lgb_model.predict_proba(
                    X
                )[:, 1]
            )

            probabilities = (
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

            result[
                "framework_version"
            ] = {
                "xgboost":
                    xgboost.__version__,
                "lightgbm":
                    lightgbm.__version__,
            }

            result[
                "model_class"
            ] = (
                "EqualWeight("
                + xgb_model.__class__.__name__
                + ","
                + lgb_model.__class__.__name__
                + ")"
            )


        p = validate_probability_vector(
            probabilities,
            expected_rows=batch_size,
        )

        result[
            "output_shape"
        ] = list(
            p.shape
        )

        result[
            "output_dtype"
        ] = str(
            p.dtype
        )

        result[
            "output_sha256"
        ] = sha256_array(
            p
        )


    # -------------------------------------------------------------------------
    # FT models
    # -------------------------------------------------------------------------

    elif target in {
        "FT_BALANCED_5_CHECKPOINT_SOFT_VOTING",
        "FT_BALANCED_SINGLE_RESOURCE_REFERENCE",
    }:

        import numpy as np
        import torch

        thread_receipt = (
            configure_torch_threads(
                thread_count
            )
        )

        result.update(
            thread_receipt
        )

        inputs = build_group_a_input(
            repo=repo,
            batch_size=batch_size,
            seed=seed,
        )

        Z = inputs[
            "Z"
        ]

        result[
            "derived_input_seed"
        ] = inputs[
            "derived_seed"
        ]

        result[
            "input_shape"
        ] = list(
            Z.shape
        )

        result[
            "input_dtype"
        ] = str(
            Z.dtype
        )

        x = torch.from_numpy(
            Z
        )

        seed_paths = {
            7:
                repo
                / "results/stage15_transformer_checkpoint/"
                  "stage15_4b_models/FT_BALANCED_seed_7_best_extended.pt",

            29:
                repo
                / "results/stage15_transformer_checkpoint/"
                  "stage15_4a_models/FT_BALANCED_seed_29_best.pt",

            101:
                repo
                / "results/stage15_transformer_checkpoint/"
                  "stage15_4a_models/FT_BALANCED_seed_101_best.pt",

            313:
                repo
                / "results/stage15_transformer_checkpoint/"
                  "stage15_4c_models/FT_BALANCED_seed_313_best.pt",

            997:
                repo
                / "results/stage15_transformer_checkpoint/"
                  "stage15_4c_models/FT_BALANCED_seed_997_best.pt",
        }

        seeds = (
            [7, 29, 101, 313, 997]
            if target
            ==
            "FT_BALANCED_5_CHECKPOINT_SOFT_VOTING"
            else
            [7]
        )

        member_probabilities = []

        load_receipts = []

        for checkpoint_seed in seeds:

            (
                model,
                parameter_count,
                load_mode,
                layout,
            ) = load_ft_model(
                repo=repo,
                checkpoint_path=seed_paths[
                    checkpoint_seed
                ],
            )

            with torch.inference_mode():

                logits = model(
                    x
                )

                member_p = torch.sigmoid(
                    logits
                ).detach().cpu().numpy()

            member_probabilities.append(
                member_p
            )

            load_receipts.append(
                {
                    "seed":
                        checkpoint_seed,

                    "parameter_count":
                        parameter_count,

                    "load_mode":
                        load_mode,

                    "state_layout":
                        layout,
                }
            )

        probabilities = np.mean(
            np.stack(
                member_probabilities,
                axis=0,
            ),
            axis=0,
        )

        p = validate_probability_vector(
            probabilities,
            expected_rows=batch_size,
        )

        result[
            "framework_version"
        ] = torch.__version__

        result[
            "model_class"
        ] = (
            "NumericFTTransformer"
        )

        result[
            "checkpoint_count"
        ] = len(
            seeds
        )

        result[
            "load_receipts"
        ] = load_receipts

        result[
            "output_shape"
        ] = list(
            p.shape
        )

        result[
            "output_dtype"
        ] = str(
            p.dtype
        )

        result[
            "output_sha256"
        ] = sha256_array(
            p
        )


    # -------------------------------------------------------------------------
    # CNN / ViT
    # -------------------------------------------------------------------------

    elif target in {
        "STAGE20_MASKED_CNN_V1",
        "STAGE21_MASKED_VIT_V1",
    }:

        import numpy as np
        import torch

        thread_receipt = (
            configure_torch_threads(
                thread_count
            )
        )

        result.update(
            thread_receipt
        )

        inputs = build_packet_input(
            repo=repo,
            batch_size=batch_size,
            seed=seed,
        )

        result[
            "derived_input_seed"
        ] = inputs[
            "derived_seed"
        ]

        mask = torch.from_numpy(
            inputs[
                "padding_mask"
            ]
        )


        if target == "STAGE20_MASKED_CNN_V1":

            module = import_path(
                "stage26_cnn_module",
                (
                    repo
                    / "scripts/stage20_masked_cnn.py"
                ),
            )

            model = (
                module.Stage20MaskedCNNv1()
            )

            state, load_mode, layout = (
                torch_load_state(
                    repo
                    / "results/stage20_1e_training/"
                      "stage20_1e2_epoch10_model_state_dict.pt"
                )
            )

            model.load_state_dict(
                state,
                strict=True,
            )

            model.eval()

            parameter_count = int(
                module.count_trainable_parameters(
                    model
                )
            )

            if parameter_count != 93025:
                raise RuntimeError(
                    f"CNN parameter count mismatch: {parameter_count}"
                )

            # Authentic frozen CNN boundary:
            # uint8 packet image + bool padding mask.
            # CNN itself performs float32 / 255 inside forward().
            image = torch.from_numpy(
                inputs[
                    "image_uint8"
                ]
            )

            result[
                "input_boundary"
            ] = (
                "UINT8_IMAGE__CNN_INTERNAL_FLOAT32_DIV255"
            )


        else:

            module = import_path(
                "stage26_vit_module",
                (
                    repo
                    / "scripts/stage21_masked_vit.py"
                ),
            )

            model = (
                module.Stage21MaskedViTv1()
            )

            state, load_mode, layout = (
                torch_load_state(
                    repo
                    / "results/stage21_architecture/"
                      "stage21_2_epoch10_model_state_dict.pt"
                )
            )

            model.load_state_dict(
                state,
                strict=True,
            )

            model.eval()

            parameter_count = int(
                module.count_trainable_parameters(
                    model
                )
            )

            if parameter_count != 91969:
                raise RuntimeError(
                    f"ViT parameter count mismatch: {parameter_count}"
                )

            # Authentic frozen ViT boundary:
            # already-scaled float32 image + bool mask.
            image = torch.from_numpy(
                inputs[
                    "image_scaled"
                ]
            )

            result[
                "input_boundary"
            ] = (
                "FLOAT32_DIV255_BEFORE_VIT_FORWARD"
            )


        result[
            "input_shape"
        ] = list(
            image.shape
        )

        result[
            "input_dtype"
        ] = str(
            image.dtype
        )

        result[
            "padding_mask_shape"
        ] = list(
            mask.shape
        )

        result[
            "padding_mask_dtype"
        ] = str(
            mask.dtype
        )

        with torch.inference_mode():

            logits = model(
                image,
                mask,
            )

            probabilities = torch.sigmoid(
                logits
            ).detach().cpu().numpy()

        p = validate_probability_vector(
            probabilities,
            expected_rows=batch_size,
        )

        result[
            "framework_version"
        ] = torch.__version__

        result[
            "model_class"
        ] = (
            model.__class__.__module__
            + "."
            + model.__class__.__name__
        )

        result[
            "parameter_count"
        ] = parameter_count

        result[
            "load_mode"
        ] = load_mode

        result[
            "state_layout"
        ] = layout

        result[
            "output_shape"
        ] = list(
            p.shape
        )

        result[
            "output_dtype"
        ] = str(
            p.dtype
        )

        result[
            "output_sha256"
        ] = sha256_array(
            p
        )


    else:
        raise RuntimeError(
            f"Unknown target: {target}"
        )


    # -------------------------------------------------------------------------
    # Universal final gates
    # -------------------------------------------------------------------------

    if result.get(
        "torch_num_threads"
    ) is not None:

        if (
            result[
                "torch_num_threads"
            ]
            !=
            thread_count
        ):
            raise RuntimeError(
                "PyTorch intra-op thread mismatch."
            )

        if (
            result[
                "torch_num_interop_threads"
            ]
            !=
            1
        ):
            raise RuntimeError(
                "PyTorch inter-op thread mismatch."
            )


    result[
        "status"
    ] = "PASS"

    result[
        "prediction_count"
    ] = int(
        batch_size
    )

    result[
        "timing_performed"
    ] = False

    result[
        "memory_profiling_performed"
    ] = False

    result[
        "holdout_accessed"
    ] = False

    result[
        "gpu_used"
    ] = False


    print(
        json.dumps(
            result,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
