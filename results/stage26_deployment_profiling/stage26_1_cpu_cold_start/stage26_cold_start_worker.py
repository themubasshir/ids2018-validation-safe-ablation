from __future__ import annotations

import os
import sys
import json
import hashlib
import importlib.util
from pathlib import Path
from time import perf_counter_ns


# Earliest practical timestamp after interpreter + stdlib startup.
PROCESS_ENTRY_NS = perf_counter_ns()


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

    if obj and all(
        torch.is_tensor(v)
        for v in obj.values()
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
            and candidate
            and all(
                torch.is_tensor(v)
                for v in candidate.values()
            )
        ):
            return candidate

    raise RuntimeError(
        "Unable to identify state_dict."
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


def build_group_a_input(
    *,
    repo,
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
            "Scaler feature count mismatch."
        )

    derived_seed = (
        int(seed)
        +
        1
    )

    rng = np.random.default_rng(
        derived_seed
    )

    Z = rng.normal(
        0.0,
        1.0,
        size=(
            1,
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

    return Z, X_raw


def build_ft_input(
    *,
    seed,
):

    import numpy as np

    derived_seed = (
        int(seed)
        +
        1
    )

    rng = np.random.default_rng(
        derived_seed
    )

    return rng.normal(
        0.0,
        1.0,
        size=(
            1,
            70,
        ),
    ).astype(
        np.float32
    )


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
            size=int(length),
            dtype=np.uint8,
        ).tobytes()
    )

    packet[0] = 0x45

    packet[2:4] = int(
        length
    ).to_bytes(
        2,
        "big",
    )

    packet[6] = (
        packet[6]
        &
        0xE0
    )

    packet[7] = 0

    packet[9] = int(
        protocol
    )

    return bytes(
        packet
    )


def build_packet_input(
    *,
    encoder,
    seed,
):

    import numpy as np

    derived_seed = (
        int(seed)
        +
        1_000_001
    )

    rng = np.random.default_rng(
        derived_seed
    )

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

    image, mask = encoder.encode_flow(
        packets
    )

    image_uint8 = image[
        None,
        None,
        :,
        :,
    ]

    mask = mask[
        None,
        None,
        :,
        :,
    ]

    image_scaled = (
        image_uint8.astype(
            np.float32
        )
        /
        np.float32(
            255.0
        )
    )

    return (
        image_uint8,
        image_scaled,
        mask,
    )


def validate_probability(probability):

    import numpy as np

    p = np.asarray(
        probability
    ).reshape(
        -1
    )

    if p.shape != (
        1,
    ):
        raise RuntimeError(
            f"Unexpected output shape: {p.shape}"
        )

    if not np.isfinite(
        p
    ).all():
        raise RuntimeError(
            "Non-finite prediction."
        )

    if (
        (p < 0.0).any()
        or
        (p > 1.0).any()
    ):
        raise RuntimeError(
            "Invalid probability."
        )

    return p


def build_ft_model(
    *,
    ft_module,
    arch_record,
    checkpoint,
):

    import torch

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

    state = torch_load_state(
        checkpoint
    )

    model.load_state_dict(
        state,
        strict=True,
    )

    model.eval()

    parameter_count = sum(
        int(
            p.numel()
        )
        for p in model.parameters()
        if p.requires_grad
    )

    if parameter_count != 159169:
        raise RuntimeError(
            f"FT parameter mismatch: {parameter_count}"
        )

    return model


def main():

    config = json.loads(
        Path(
            sys.argv[1]
        ).read_text(
            encoding="utf-8"
        )
    )

    repo = Path(
        config[
            "repo"
        ]
    )

    target = config[
        "target_id"
    ]

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

    parent_spawn_start_ns = int(
        os.environ[
            "STAGE26_PARENT_SPAWN_START_NS"
        ]
    )


    # -------------------------------------------------------------------------
    # Exact CPU placement before ML imports.
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

    if (
        observed_affinity is not None
        and
        observed_affinity != affinity
    ):
        raise RuntimeError(
            f"Affinity mismatch: "
            f"{observed_affinity} != {affinity}"
        )


    worker_ready_ns = perf_counter_ns()


    # -------------------------------------------------------------------------
    # FRAMEWORK IMPORT COMPONENT
    # -------------------------------------------------------------------------

    framework_import_start_ns = (
        perf_counter_ns()
    )


    if target in {
        "STAGE16_XGBOOST_TUNED",
    }:

        import numpy as np
        import joblib
        import xgboost


    elif target in {
        "STAGE16_LIGHTGBM_TUNED",
    }:

        import numpy as np
        import joblib
        import lightgbm


    elif target in {
        "STAGE16_CATBOOST_TUNED",
    }:

        import numpy as np
        import joblib
        import catboost


    elif target == "ENS_LGBM_XGB_EQUAL":

        import numpy as np
        import joblib
        import xgboost
        import lightgbm


    elif target in {
        "FT_BALANCED_5_CHECKPOINT_SOFT_VOTING",
        "FT_BALANCED_SINGLE_RESOURCE_REFERENCE",
    }:

        import numpy as np
        import torch

        configure_torch_threads(
            thread_count
        )

        ft_module = import_path(
            "stage26_ft_module",
            (
                repo
                / "results/stage15_transformer_checkpoint/"
                  "ft_transformer_numeric.py"
            ),
        )


    elif target == "STAGE20_MASKED_CNN_V1":

        import numpy as np
        import torch

        configure_torch_threads(
            thread_count
        )

        encoder = import_path(
            "stage26_packet_encoder",
            (
                repo
                / "scripts/stage20_packet_image_encoder.py"
            ),
        )

        cnn_module = import_path(
            "stage26_cnn_module",
            (
                repo
                / "scripts/stage20_masked_cnn.py"
            ),
        )


    elif target == "STAGE21_MASKED_VIT_V1":

        import numpy as np
        import torch

        configure_torch_threads(
            thread_count
        )

        encoder = import_path(
            "stage26_packet_encoder",
            (
                repo
                / "scripts/stage20_packet_image_encoder.py"
            ),
        )

        vit_module = import_path(
            "stage26_vit_module",
            (
                repo
                / "scripts/stage21_masked_vit.py"
            ),
        )


    else:
        raise RuntimeError(
            f"Unknown target: {target}"
        )


    framework_import_end_ns = (
        perf_counter_ns()
    )


    # -------------------------------------------------------------------------
    # SYNTHETIC INPUT PREPARATION — supplementary cold component.
    # NOT part of primary model-deserialization or first-prediction duration.
    # -------------------------------------------------------------------------

    input_preparation_start_ns = (
        perf_counter_ns()
    )


    if target in {
        "STAGE16_XGBOOST_TUNED",
        "STAGE16_LIGHTGBM_TUNED",
        "STAGE16_CATBOOST_TUNED",
        "ENS_LGBM_XGB_EQUAL",
    }:

        Z, X_raw = build_group_a_input(
            repo=repo,
            seed=seed,
        )


    elif target in {
        "FT_BALANCED_5_CHECKPOINT_SOFT_VOTING",
        "FT_BALANCED_SINGLE_RESOURCE_REFERENCE",
    }:

        Z = build_ft_input(
            seed=seed
        )


    elif target in {
        "STAGE20_MASKED_CNN_V1",
        "STAGE21_MASKED_VIT_V1",
    }:

        (
            image_uint8,
            image_scaled,
            padding_mask,
        ) = build_packet_input(
            encoder=encoder,
            seed=seed,
        )


    input_preparation_end_ns = (
        perf_counter_ns()
    )


    # -------------------------------------------------------------------------
    # MODEL DESERIALIZATION / CONSTRUCTION COMPONENT
    # -------------------------------------------------------------------------

    model_load_start_ns = (
        perf_counter_ns()
    )


    if target == "STAGE16_XGBOOST_TUNED":

        model = joblib.load(
            repo
            / "results/stage16_classical_benchmark_checkpoint/"
              "stage16_3_tuned_models/XGBOOST_tuned.joblib"
        )

        model.set_params(
            n_jobs=thread_count
        )


    elif target == "STAGE16_LIGHTGBM_TUNED":

        model = joblib.load(
            repo
            / "results/stage16_classical_benchmark_checkpoint/"
              "stage16_3_tuned_models/LIGHTGBM_tuned.joblib"
        )

        model.set_params(
            n_jobs=thread_count
        )


    elif target == "STAGE16_CATBOOST_TUNED":

        model = joblib.load(
            repo
            / "results/stage16_classical_benchmark_checkpoint/"
              "stage16_3_tuned_models/CATBOOST_tuned.joblib"
        )


    elif target == "ENS_LGBM_XGB_EQUAL":

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


    elif target in {
        "FT_BALANCED_5_CHECKPOINT_SOFT_VOTING",
        "FT_BALANCED_SINGLE_RESOURCE_REFERENCE",
    }:

        arch_record = json.loads(
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

        seeds = (
            [7, 29, 101, 313, 997]
            if target
            ==
            "FT_BALANCED_5_CHECKPOINT_SOFT_VOTING"
            else
            [7]
        )

        ft_models = []

        for checkpoint_seed in seeds:

            ft_models.append(
                build_ft_model(
                    ft_module=ft_module,
                    arch_record=arch_record,
                    checkpoint=checkpoint_paths[
                        checkpoint_seed
                    ],
                )
            )


    elif target == "STAGE20_MASKED_CNN_V1":

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


    elif target == "STAGE21_MASKED_VIT_V1":

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


    model_load_end_ns = (
        perf_counter_ns()
    )


    # -------------------------------------------------------------------------
    # FIRST PREDICTION COMPONENT
    # Prepared model input -> materialized attack probability.
    # -------------------------------------------------------------------------

    first_prediction_start_ns = (
        perf_counter_ns()
    )


    if target == "STAGE16_XGBOOST_TUNED":

        probability = model.predict_proba(
            X_raw
        )[:, 1]


    elif target == "STAGE16_LIGHTGBM_TUNED":

        probability = model.predict_proba(
            X_raw
        )[:, 1]


    elif target == "STAGE16_CATBOOST_TUNED":

        probability = model.predict_proba(
            X_raw,
            thread_count=thread_count,
        )[:, 1]


    elif target == "ENS_LGBM_XGB_EQUAL":

        xgb_p = xgb_model.predict_proba(
            X_raw
        )[:, 1]

        lgb_p = lgb_model.predict_proba(
            X_raw
        )[:, 1]

        probability = (
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

        x = torch.from_numpy(
            Z
        )

        member_probabilities = []

        with torch.inference_mode():

            for ft_model in ft_models:

                logits = ft_model(
                    x
                )

                member_probabilities.append(
                    torch.sigmoid(
                        logits
                    ).detach().cpu().numpy()
                )

        probability = np.mean(
            np.stack(
                member_probabilities,
                axis=0,
            ),
            axis=0,
        )


    elif target == "STAGE20_MASKED_CNN_V1":

        image = torch.from_numpy(
            image_uint8
        )

        mask = torch.from_numpy(
            padding_mask
        )

        with torch.inference_mode():

            logits = model(
                image,
                mask,
            )

            probability = torch.sigmoid(
                logits
            ).detach().cpu().numpy()


    elif target == "STAGE21_MASKED_VIT_V1":

        image = torch.from_numpy(
            image_scaled
        )

        mask = torch.from_numpy(
            padding_mask
        )

        with torch.inference_mode():

            logits = model(
                image,
                mask,
            )

            probability = torch.sigmoid(
                logits
            ).detach().cpu().numpy()


    # Materialization is complete here.
    first_prediction_end_ns = (
        perf_counter_ns()
    )


    p = validate_probability(
        probability
    )

    output_sha256 = sha256_array(
        p
    )


    result = {
        "schema":
            "stage26_1_cold_start_observation_v1",

        "status":
            "PASS",

        "target_id":
            target,

        "hardware_mode":
            "CPU_1_PHYSICAL_CORE",

        "thread_count":
            thread_count,

        "affinity_requested":
            affinity,

        "affinity_observed":
            observed_affinity,

        "batch_size":
            1,

        "output_sha256":
            output_sha256,

        "process_entry_ns":
            int(
                PROCESS_ENTRY_NS
            ),

        "worker_ready_ns":
            int(
                worker_ready_ns
            ),

        "framework_import_start_ns":
            int(
                framework_import_start_ns
            ),

        "framework_import_end_ns":
            int(
                framework_import_end_ns
            ),

        "input_preparation_start_ns":
            int(
                input_preparation_start_ns
            ),

        "input_preparation_end_ns":
            int(
                input_preparation_end_ns
            ),

        "model_load_start_ns":
            int(
                model_load_start_ns
            ),

        "model_load_end_ns":
            int(
                model_load_end_ns
            ),

        "first_prediction_start_ns":
            int(
                first_prediction_start_ns
            ),

        "first_prediction_end_ns":
            int(
                first_prediction_end_ns
            ),

        "process_spawn_to_worker_ready_ns":
            int(
                worker_ready_ns
                -
                parent_spawn_start_ns
            ),

        "framework_import_ns":
            int(
                framework_import_end_ns
                -
                framework_import_start_ns
            ),

        "input_preparation_ns":
            int(
                input_preparation_end_ns
                -
                input_preparation_start_ns
            ),

        "model_deserialization_load_ns":
            int(
                model_load_end_ns
                -
                model_load_start_ns
            ),

        "first_prediction_ns":
            int(
                first_prediction_end_ns
                -
                first_prediction_start_ns
            ),

        "spawn_to_first_output_ns":
            int(
                first_prediction_end_ns
                -
                parent_spawn_start_ns
            ),

        "holdout_accessed":
            False,

        "memory_profiled":
            False,

        "gpu_used":
            False,
    }


    for key in [
        "process_spawn_to_worker_ready_ns",
        "framework_import_ns",
        "input_preparation_ns",
        "model_deserialization_load_ns",
        "first_prediction_ns",
        "spawn_to_first_output_ns",
    ]:

        if result[
            key
        ] < 0:
            raise RuntimeError(
                f"Negative timing component: {key}"
            )


    print(
        json.dumps(
            result,
            sort_keys=True,
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
