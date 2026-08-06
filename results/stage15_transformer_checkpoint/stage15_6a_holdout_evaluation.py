
from __future__ import annotations

from pathlib import Path
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import math
import os
import time

import joblib
import numpy as np
import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    brier_score_loss,
    confusion_matrix,
    log_loss,
    matthews_corrcoef,
    precision_score,
    recall_score,
    roc_auc_score,
)

import torch
from torch import nn
from torch.utils.data import (
    DataLoader,
    TensorDataset,
)


# ------------------------------------------------------------
# Paths
# ------------------------------------------------------------

DATASET_PATH = Path(
    os.environ["STAGE15_DATASET_PATH"]
)

MODEL_MODULE_PATH = Path(
    os.environ["STAGE15_MODEL_MODULE"]
)

SAFE_SPLIT_PATH = Path(
    os.environ["STAGE15_SAFE_SPLIT"]
)

FEATURE_CONFIGURATION_PATH = Path(
    os.environ["STAGE15_FEATURE_CONFIGURATION"]
)

SCALER_PATH = Path(
    os.environ["STAGE15_SCALER"]
)

FROZEN_ARCHITECTURE_PATH = Path(
    os.environ["STAGE15_FROZEN_ARCHITECTURE"]
)

PREHOLDOUT_LOCK_PATH = Path(
    os.environ["STAGE15_PREHOLDOUT_LOCK"]
)

EVALUATION_PLAN_PATH = Path(
    os.environ["STAGE15_EVALUATION_PLAN"]
)

EXECUTION_STATE_PATH = Path(
    os.environ["STAGE15_EXECUTION_STATE"]
)

VALIDATION_PROBABILITIES_PATH = Path(
    os.environ["STAGE15_VALIDATION_PROBABILITIES"]
)

VALIDATION_COMMON_THRESHOLD_METRICS_PATH = Path(
    os.environ[
        "STAGE15_VALIDATION_COMMON_THRESHOLD_METRICS"
    ]
)

SEED_PROBABILITY_DIRECTORY = Path(
    os.environ["STAGE15_SEED_PROBABILITY_DIRECTORY"]
)

HOLDOUT_PROBABILITIES_PATH = Path(
    os.environ["STAGE15_HOLDOUT_PROBABILITIES"]
)

HOLDOUT_PREDICTIONS_PATH = Path(
    os.environ["STAGE15_HOLDOUT_PREDICTIONS"]
)

SEED_METRICS_PATH = Path(
    os.environ["STAGE15_SEED_METRICS"]
)

SEED_AGGREGATE_PATH = Path(
    os.environ["STAGE15_SEED_AGGREGATE"]
)

ENSEMBLE_METRICS_PATH = Path(
    os.environ["STAGE15_ENSEMBLE_METRICS"]
)

CONFUSION_MATRICES_PATH = Path(
    os.environ["STAGE15_CONFUSION_MATRICES"]
)

VALIDATION_HOLDOUT_GAPS_PATH = Path(
    os.environ["STAGE15_VALIDATION_HOLDOUT_GAPS"]
)

ENSEMBLE_VALIDATION_HOLDOUT_GAP_PATH = Path(
    os.environ[
        "STAGE15_ENSEMBLE_VALIDATION_HOLDOUT_GAP"
    ]
)

RESULT_PATH = Path(
    os.environ["STAGE15_RESULT"]
)

METADATA_PATH = Path(
    os.environ["STAGE15_METADATA"]
)


# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------

def sha256_file(path):
    digest = hashlib.sha256()

    with path.open("rb") as file:
        while True:
            block = file.read(
                1024 * 1024
            )

            if not block:
                break

            digest.update(block)

    return digest.hexdigest()


def atomic_json_write(
    path,
    record,
):
    temporary_path = path.with_suffix(
        path.suffix + ".tmp"
    )

    temporary_path.write_text(
        json.dumps(
            record,
            indent=2,
        ),
        encoding="utf-8",
    )

    temporary_path.replace(
        path
    )


def load_selected_rows(
    dataset_path,
    feature_names,
    selected_indices,
    chunk_size=50_000,
):
    selected_indices = np.asarray(
        selected_indices,
        dtype=np.int64,
    )

    if selected_indices.ndim != 1:
        raise ValueError(
            "Holdout indices must be one-dimensional."
        )

    if not np.all(
        selected_indices[:-1]
        <= selected_indices[1:]
    ):
        raise ValueError(
            "Holdout indices must be sorted."
        )

    if len(
        np.unique(
            selected_indices
        )
    ) != len(
        selected_indices
    ):
        raise ValueError(
            "Holdout indices contain duplicates."
        )

    X_selected = np.empty(
        (
            len(selected_indices),
            len(feature_names),
        ),
        dtype=np.float64,
    )

    y_selected = np.empty(
        len(selected_indices),
        dtype=np.float32,
    )

    filled = np.zeros(
        len(selected_indices),
        dtype=bool,
    )

    global_start = 0

    for chunk in pd.read_csv(
        dataset_path,
        usecols=(
            feature_names
            + ["binary_label"]
        ),
        chunksize=chunk_size,
    ):
        global_end = (
            global_start
            + len(chunk)
        )

        left = np.searchsorted(
            selected_indices,
            global_start,
            side="left",
        )

        right = np.searchsorted(
            selected_indices,
            global_end,
            side="left",
        )

        if right > left:
            selected_global = (
                selected_indices[
                    left:right
                ]
            )

            local_positions = (
                selected_global
                - global_start
            )

            selected_chunk = chunk.iloc[
                local_positions
            ]

            X_selected[
                left:right
            ] = (
                selected_chunk[
                    feature_names
                ]
                .to_numpy(
                    dtype=np.float64,
                    copy=True,
                )
            )

            y_selected[
                left:right
            ] = (
                selected_chunk[
                    "binary_label"
                ]
                .to_numpy(
                    dtype=np.float32,
                    copy=True,
                )
            )

            filled[
                left:right
            ] = True

        global_start = (
            global_end
        )

    if not filled.all():
        raise RuntimeError(
            "Failed to load "
            f"{int(np.sum(~filled))} "
            "holdout rows."
        )

    return (
        X_selected,
        y_selected,
    )


def binary_metrics(
    y_true,
    probabilities,
    threshold,
):
    probabilities = np.asarray(
        probabilities,
        dtype=np.float64,
    )

    predictions = (
        probabilities
        >= threshold
    ).astype(np.int8)

    tn, fp, fn, tp = confusion_matrix(
        y_true,
        predictions,
        labels=[0, 1],
    ).ravel()

    precision = float(
        precision_score(
            y_true,
            predictions,
            zero_division=0,
        )
    )

    recall = float(
        recall_score(
            y_true,
            predictions,
            zero_division=0,
        )
    )

    f1 = (
        2.0
        * precision
        * recall
        / (
            precision
            + recall
        )
        if (
            precision
            + recall
        ) > 0
        else 0.0
    )

    beta_squared = 4.0

    f2 = (
        (
            1.0
            + beta_squared
        )
        * precision
        * recall
        / (
            beta_squared
            * precision
            + recall
        )
        if (
            beta_squared
            * precision
            + recall
        ) > 0
        else 0.0
    )

    fpr = (
        fp / (fp + tn)
        if (
            fp + tn
        ) > 0
        else 0.0
    )

    fnr = (
        fn / (fn + tp)
        if (
            fn + tp
        ) > 0
        else 0.0
    )

    specificity = (
        tn / (tn + fp)
        if (
            tn + fp
        ) > 0
        else 0.0
    )

    balanced_accuracy = (
        recall
        + specificity
    ) / 2.0

    clipped_probabilities = np.clip(
        probabilities,
        1e-7,
        1.0 - 1e-7,
    )

    return {
        "threshold": float(
            threshold
        ),

        "accuracy": float(
            accuracy_score(
                y_true,
                predictions,
            )
        ),

        "precision": (
            precision
        ),

        "recall": (
            recall
        ),

        "specificity": float(
            specificity
        ),

        "balanced_accuracy": float(
            balanced_accuracy
        ),

        "f1": float(
            f1
        ),

        "f2": float(
            f2
        ),

        "fpr": float(
            fpr
        ),

        "fnr": float(
            fnr
        ),

        "mcc": float(
            matthews_corrcoef(
                y_true,
                predictions,
            )
        ),

        "roc_auc": float(
            roc_auc_score(
                y_true,
                probabilities,
            )
        ),

        "pr_auc": float(
            average_precision_score(
                y_true,
                probabilities,
            )
        ),

        "brier_score": float(
            brier_score_loss(
                y_true,
                probabilities,
            )
        ),

        "log_loss": float(
            log_loss(
                y_true,
                clipped_probabilities,
                labels=[0, 1],
            )
        ),

        "true_negative": int(
            tn
        ),

        "false_positive": int(
            fp
        ),

        "false_negative": int(
            fn
        ),

        "true_positive": int(
            tp
        ),

        "predicted_attack_count": int(
            np.sum(
                predictions == 1
            )
        ),

        "predicted_benign_count": int(
            np.sum(
                predictions == 0
            )
        ),
    }


@torch.no_grad()
def predict_probabilities(
    model,
    loader,
    device,
):
    model.eval()

    probability_batches = []

    for (features,) in loader:
        features = features.to(
            device,
            non_blocking=True,
        )

        logits = model(
            features
        ).reshape(-1)

        probabilities = torch.sigmoid(
            logits
        )

        probability_batches.append(
            probabilities
            .detach()
            .cpu()
            .numpy()
        )

    return np.concatenate(
        probability_batches
    ).astype(np.float32)


# ------------------------------------------------------------
# Load locked records
# ------------------------------------------------------------

with open(
    EVALUATION_PLAN_PATH,
    "r",
    encoding="utf-8",
) as file:
    evaluation_plan = json.load(file)

with open(
    PREHOLDOUT_LOCK_PATH,
    "r",
    encoding="utf-8",
) as file:
    preholdout_lock = json.load(file)

with open(
    FROZEN_ARCHITECTURE_PATH,
    "r",
    encoding="utf-8",
) as file:
    frozen_architecture = json.load(file)

with open(
    EXECUTION_STATE_PATH,
    "r",
    encoding="utf-8",
) as file:
    execution_state = json.load(file)

if (
    execution_state.get(
        "status"
    )
    == "COMPLETED"
):
    raise RuntimeError(
        "The holdout evaluation already completed."
    )

if (
    execution_state.get(
        "holdout_evaluation_count",
        0,
    )
    not in [0, 1]
):
    raise RuntimeError(
        "Invalid holdout evaluation count."
    )

if (
    evaluation_plan.get(
        "candidate_id"
    )
    != "FT_BALANCED"
):
    raise RuntimeError(
        "Evaluation-plan candidate mismatch."
    )

if abs(
    float(
        evaluation_plan[
            "operating_threshold"
        ]
    )
    - 0.73
) > 1e-12:
    raise RuntimeError(
        "Evaluation-plan threshold mismatch."
    )

expected_seeds = [
    7,
    29,
    101,
    313,
    997,
]

if (
    evaluation_plan.get(
        "checkpoint_seeds"
    )
    != expected_seeds
):
    raise RuntimeError(
        "Evaluation-plan seed set mismatch."
    )

if (
    frozen_architecture.get(
        "candidate_id"
    )
    != "FT_BALANCED"
):
    raise RuntimeError(
        "Frozen architecture mismatch."
    )

architecture = (
    frozen_architecture[
        "architecture"
    ]
)

retained_parameter_count = int(
    frozen_architecture[
        "five_seed_summary"
    ][
        "parameter_count"
    ]
)

if retained_parameter_count != 159_169:
    raise RuntimeError(
        "Unexpected frozen parameter count."
    )


# ------------------------------------------------------------
# Verify exact locked checkpoints again
# ------------------------------------------------------------

checkpoint_paths = {}

for seed in expected_seeds:
    locked_record = (
        preholdout_lock[
            "checkpoint_locks"
        ][
            str(seed)
        ]
    )

    checkpoint_path = Path(
        locked_record[
            "path"
        ]
    )

    if not checkpoint_path.exists():
        raise FileNotFoundError(
            f"Checkpoint missing for seed {seed}."
        )

    if (
        sha256_file(
            checkpoint_path
        )
        != locked_record[
            "sha256"
        ]
    ):
        raise RuntimeError(
            f"Checkpoint hash changed for seed {seed}."
        )

    checkpoint_paths[
        seed
    ] = checkpoint_path


# ------------------------------------------------------------
# Mark the single evaluation event as started
# ------------------------------------------------------------

if (
    execution_state.get(
        "status"
    )
    == "PREPARED"
):
    execution_state.update(
        {
            "status": "STARTED",
            "started_at_utc": datetime.now(
                timezone.utc
            ).isoformat(),
            "holdout_opened": False,
            "holdout_evaluation_count": 1,
            "completed_seed_inferences": [],
            "metrics_generated": False,
        }
    )

    atomic_json_write(
        EXECUTION_STATE_PATH,
        execution_state,
    )

elif (
    execution_state.get(
        "status"
    )
    != "STARTED"
):
    raise RuntimeError(
        "Unexpected execution-state status."
    )


# ------------------------------------------------------------
# Load feature configuration
# ------------------------------------------------------------

with open(
    FEATURE_CONFIGURATION_PATH,
    "r",
    encoding="utf-8",
) as file:
    feature_configuration = json.load(file)

retained_features = list(
    feature_configuration[
        "retained_features"
    ]
)

if len(retained_features) != 70:
    raise RuntimeError(
        "Expected 70 retained predictors."
    )


# ------------------------------------------------------------
# Open the holdout indices for the first evaluation event
# ------------------------------------------------------------

split_archive = np.load(
    SAFE_SPLIT_PATH,
    allow_pickle=False,
)

if "holdout_indices" not in split_archive.files:
    raise RuntimeError(
        "Duplicate-safe holdout indices are missing."
    )

holdout_indices = np.asarray(
    split_archive[
        "holdout_indices"
    ],
    dtype=np.int64,
)

# Training and validation index arrays are deliberately not accessed.

if len(holdout_indices) != 46_849:
    raise RuntimeError(
        "Unexpected duplicate-safe holdout size."
    )

if len(
    np.unique(
        holdout_indices
    )
) != len(
    holdout_indices
):
    raise RuntimeError(
        "Duplicate holdout indices detected."
    )

execution_state.update(
    {
        "status": "STARTED",
        "holdout_opened": True,
        "holdout_opened_at_utc": (
            execution_state.get(
                "holdout_opened_at_utc"
            )
            or datetime.now(
                timezone.utc
            ).isoformat()
        ),
        "holdout_evaluation_count": 1,
    }
)

atomic_json_write(
    EXECUTION_STATE_PATH,
    execution_state,
)


# ------------------------------------------------------------
# Load holdout features and labels once
# ------------------------------------------------------------

X_holdout_raw, y_holdout_float = (
    load_selected_rows(
        DATASET_PATH,
        retained_features,
        holdout_indices,
    )
)

y_holdout = y_holdout_float.astype(
    np.int8,
    copy=False,
)

del y_holdout_float

if not np.array_equal(
    np.unique(
        y_holdout
    ),
    np.array(
        [0, 1],
        dtype=np.int8,
    ),
):
    raise RuntimeError(
        "Holdout labels are not binary."
    )

holdout_benign_count = int(
    np.sum(
        y_holdout == 0
    )
)

holdout_attack_count = int(
    np.sum(
        y_holdout == 1
    )
)

if holdout_benign_count != 33_674:
    raise RuntimeError(
        "Unexpected holdout benign count."
    )

if holdout_attack_count != 13_175:
    raise RuntimeError(
        "Unexpected holdout attack count."
    )


# ------------------------------------------------------------
# Apply the archived training-only scaler
# ------------------------------------------------------------

scaler = joblib.load(
    SCALER_PATH
)

if int(
    scaler.n_features_in_
) != 70:
    raise RuntimeError(
        "Unexpected scaler feature count."
    )

X_holdout = scaler.transform(
    X_holdout_raw
).astype(
    np.float32,
    copy=False,
)

del X_holdout_raw

if not np.isfinite(
    X_holdout
).all():
    raise RuntimeError(
        "Scaled holdout features contain "
        "non-finite values."
    )


# ------------------------------------------------------------
# Prepare deterministic inference loader
# ------------------------------------------------------------

holdout_dataset = TensorDataset(
    torch.from_numpy(
        X_holdout
    )
)

holdout_loader = DataLoader(
    holdout_dataset,
    batch_size=int(
        evaluation_plan[
            "inference_batch_size"
        ]
    ),
    shuffle=False,
    num_workers=2,
    pin_memory=True,
    persistent_workers=True,
    drop_last=False,
)


# ------------------------------------------------------------
# Import frozen model class
# ------------------------------------------------------------

module_spec = importlib.util.spec_from_file_location(
    "ft_transformer_numeric",
    MODEL_MODULE_PATH,
)

if (
    module_spec is None
    or module_spec.loader is None
):
    raise ImportError(
        "Unable to import the frozen model module."
    )

model_module = importlib.util.module_from_spec(
    module_spec
)

module_spec.loader.exec_module(
    model_module
)

NumericFTTransformer = (
    model_module.NumericFTTransformer
)


# ------------------------------------------------------------
# Validate isolated CUDA environment
# ------------------------------------------------------------

if not torch.cuda.is_available():
    raise RuntimeError(
        "CUDA is unavailable."
    )

device = torch.device(
    "cuda:0"
)

device_name = torch.cuda.get_device_name(
    0
)

device_capability = list(
    torch.cuda.get_device_capability(
        0
    )
)

compiled_architectures = list(
    torch.cuda.get_arch_list()
)

if device_capability != [6, 0]:
    raise RuntimeError(
        "Expected Tesla P100 capability [6, 0]."
    )

if "sm_60" not in compiled_architectures:
    raise RuntimeError(
        "The isolated PyTorch build lacks sm_60."
    )


# ------------------------------------------------------------
# Generate five locked probability vectors
#
# No metrics are calculated or printed until every vector exists.
# ------------------------------------------------------------

SEED_PROBABILITY_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True,
)

holdout_probabilities_by_seed = {}

inference_records = []

evaluation_start = time.perf_counter()

for seed in expected_seeds:
    probability_path = (
        SEED_PROBABILITY_DIRECTORY
        / f"FT_BALANCED_seed_{seed}_holdout_probabilities.npz"
    )

    if probability_path.exists():
        stored_archive = np.load(
            probability_path,
            allow_pickle=False,
        )

        probabilities = np.asarray(
            stored_archive[
                "probabilities"
            ],
            dtype=np.float32,
        )

        stored_indices = np.asarray(
            stored_archive[
                "holdout_indices"
            ],
            dtype=np.int64,
        )

        if not np.array_equal(
            stored_indices,
            holdout_indices,
        ):
            raise RuntimeError(
                f"Stored holdout ordering differs for seed {seed}."
            )

        if probabilities.shape != y_holdout.shape:
            raise RuntimeError(
                f"Stored probability shape differs for seed {seed}."
            )

        inference_seconds = float(
            stored_archive[
                "inference_seconds"
            ][0]
        )

        peak_gpu_memory_mb = float(
            stored_archive[
                "peak_gpu_memory_mb"
            ][0]
        )

        reused_existing_probability = True

    else:
        torch.cuda.empty_cache()
        torch.cuda.reset_peak_memory_stats()

        model = NumericFTTransformer(
            n_features=70,
            d_token=int(
                architecture[
                    "d_token"
                ]
            ),
            n_heads=int(
                architecture[
                    "n_heads"
                ]
            ),
            n_layers=int(
                architecture[
                    "n_layers"
                ]
            ),
            d_ff=int(
                architecture[
                    "d_ff"
                ]
            ),
            dropout=float(
                architecture[
                    "dropout"
                ]
            ),
        ).to(
            device
        )

        parameter_count = int(
            sum(
                parameter.numel()
                for parameter in model.parameters()
                if parameter.requires_grad
            )
        )

        if parameter_count != 159_169:
            raise RuntimeError(
                "Frozen model parameter count changed."
            )

        checkpoint = torch.load(
            checkpoint_paths[
                seed
            ],
            map_location=device,
            weights_only=False,
        )

        if checkpoint.get(
            "candidate_id"
        ) != "FT_BALANCED":
            raise RuntimeError(
                f"Checkpoint candidate mismatch for seed {seed}."
            )

        if int(
            checkpoint.get(
                "seed"
            )
        ) != seed:
            raise RuntimeError(
                f"Checkpoint seed mismatch for seed {seed}."
            )

        model.load_state_dict(
            checkpoint[
                "model_state_dict"
            ]
        )

        inference_start = time.perf_counter()

        probabilities = predict_probabilities(
            model,
            holdout_loader,
            device,
        )

        torch.cuda.synchronize()

        inference_seconds = float(
            time.perf_counter()
            - inference_start
        )

        peak_gpu_memory_mb = float(
            torch.cuda.max_memory_allocated()
            / (1024 ** 2)
        )

        if probabilities.shape != y_holdout.shape:
            raise RuntimeError(
                f"Holdout probability shape differs for seed {seed}."
            )

        if not np.isfinite(
            probabilities
        ).all():
            raise RuntimeError(
                f"Non-finite holdout probabilities for seed {seed}."
            )

        if (
            float(
                np.min(
                    probabilities
                )
            ) < 0.0
            or float(
                np.max(
                    probabilities
                )
            ) > 1.0
        ):
            raise RuntimeError(
                f"Invalid probability range for seed {seed}."
            )

        np.savez_compressed(
            probability_path,
            probabilities=probabilities,
            holdout_indices=holdout_indices,
            inference_seconds=np.array(
                [
                    inference_seconds
                ],
                dtype=np.float64,
            ),
            peak_gpu_memory_mb=np.array(
                [
                    peak_gpu_memory_mb
                ],
                dtype=np.float64,
            ),
        )

        reused_existing_probability = False

        del model
        del checkpoint

        torch.cuda.empty_cache()

    holdout_probabilities_by_seed[
        seed
    ] = probabilities

    inference_records.append(
        {
            "seed": int(
                seed
            ),
            "probability_path": str(
                probability_path
            ),
            "probability_sha256": sha256_file(
                probability_path
            ),
            "inference_seconds": (
                inference_seconds
            ),
            "peak_gpu_memory_mb": (
                peak_gpu_memory_mb
            ),
            "reused_existing_probability": (
                reused_existing_probability
            ),
        }
    )

    completed_seeds = sorted(
        set(
            execution_state.get(
                "completed_seed_inferences",
                [],
            )
        )
        | {
            seed
        }
    )

    execution_state[
        "completed_seed_inferences"
    ] = completed_seeds

    atomic_json_write(
        EXECUTION_STATE_PATH,
        execution_state,
    )


# ------------------------------------------------------------
# Verify all five probability vectors before metric generation
# ------------------------------------------------------------

if sorted(
    holdout_probabilities_by_seed.keys()
) != expected_seeds:
    raise RuntimeError(
        "The complete five-seed probability set "
        "was not generated."
    )

probability_matrix = np.vstack(
    [
        holdout_probabilities_by_seed[
            seed
        ]
        for seed in expected_seeds
    ]
).astype(
    np.float32,
    copy=False,
)

if probability_matrix.shape != (
    5,
    46_849,
):
    raise RuntimeError(
        "Unexpected five-seed holdout probability shape."
    )

ensemble_probabilities = np.mean(
    probability_matrix.astype(
        np.float64
    ),
    axis=0,
).astype(
    np.float32
)

frozen_threshold = 0.73

seed_predictions = (
    probability_matrix
    >= frozen_threshold
).astype(
    np.int8
)

ensemble_predictions = (
    ensemble_probabilities
    >= frozen_threshold
).astype(
    np.int8
)


# ------------------------------------------------------------
# Save consolidated probabilities and predictions
# ------------------------------------------------------------

probability_archive = {
    "y_true": y_holdout,
    "holdout_indices": holdout_indices,
    "ensemble_probabilities": (
        ensemble_probabilities
    ),
}

prediction_archive = {
    "y_true": y_holdout,
    "holdout_indices": holdout_indices,
    "ensemble_predictions": (
        ensemble_predictions
    ),
}

for row_index, seed in enumerate(
    expected_seeds
):
    probability_archive[
        f"seed_{seed}"
    ] = probability_matrix[
        row_index
    ]

    prediction_archive[
        f"seed_{seed}"
    ] = seed_predictions[
        row_index
    ]

np.savez_compressed(
    HOLDOUT_PROBABILITIES_PATH,
    **probability_archive,
)

np.savez_compressed(
    HOLDOUT_PREDICTIONS_PATH,
    **prediction_archive,
)


# ------------------------------------------------------------
# Generate locked-threshold individual metrics
# ------------------------------------------------------------

seed_metric_rows = []

confusion_rows = []

for seed in expected_seeds:
    metrics = binary_metrics(
        y_holdout,
        holdout_probabilities_by_seed[
            seed
        ],
        frozen_threshold,
    )

    inference_record = next(
        record
        for record in inference_records
        if record["seed"] == seed
    )

    seed_metric_rows.append(
        {
            "candidate_id": (
                "FT_BALANCED"
            ),

            "seed": int(
                seed
            ),

            **metrics,

            "inference_seconds": float(
                inference_record[
                    "inference_seconds"
                ]
            ),

            "peak_gpu_memory_mb": float(
                inference_record[
                    "peak_gpu_memory_mb"
                ]
            ),
        }
    )

    confusion_rows.append(
        {
            "model": (
                f"FT_BALANCED_seed_{seed}"
            ),
            "seed": int(
                seed
            ),
            "threshold": (
                frozen_threshold
            ),
            "true_negative": (
                metrics[
                    "true_negative"
                ]
            ),
            "false_positive": (
                metrics[
                    "false_positive"
                ]
            ),
            "false_negative": (
                metrics[
                    "false_negative"
                ]
            ),
            "true_positive": (
                metrics[
                    "true_positive"
                ]
            ),
        }
    )

seed_metrics_frame = pd.DataFrame(
    seed_metric_rows
).sort_values(
    "seed"
).reset_index(
    drop=True
)

seed_metrics_frame.to_csv(
    SEED_METRICS_PATH,
    index=False,
)


# ------------------------------------------------------------
# Generate ensemble metrics
# ------------------------------------------------------------

ensemble_metrics = binary_metrics(
    y_holdout,
    ensemble_probabilities,
    frozen_threshold,
)

ensemble_metrics.update(
    {
        "model": (
            "five_checkpoint_soft_voting_ensemble"
        ),

        "candidate_id": (
            "FT_BALANCED"
        ),

        "checkpoint_count": 5,

        "checkpoint_seeds": (
            expected_seeds
        ),

        "ensemble_method": (
            "unweighted arithmetic mean probabilities"
        ),

        "primary_endpoint": "f1",

        "holdout_row_count": int(
            len(
                y_holdout
            )
        ),

        "holdout_benign_count": (
            holdout_benign_count
        ),

        "holdout_attack_count": (
            holdout_attack_count
        ),

        "holdout_attack_rate": float(
            holdout_attack_count
            / len(
                y_holdout
            )
        ),
    }
)

atomic_json_write(
    ENSEMBLE_METRICS_PATH,
    ensemble_metrics,
)

confusion_rows.append(
    {
        "model": (
            "five_checkpoint_soft_voting_ensemble"
        ),
        "seed": None,
        "threshold": (
            frozen_threshold
        ),
        "true_negative": (
            ensemble_metrics[
                "true_negative"
            ]
        ),
        "false_positive": (
            ensemble_metrics[
                "false_positive"
            ]
        ),
        "false_negative": (
            ensemble_metrics[
                "false_negative"
            ]
        ),
        "true_positive": (
            ensemble_metrics[
                "true_positive"
            ]
        ),
    }
)

pd.DataFrame(
    confusion_rows
).to_csv(
    CONFUSION_MATRICES_PATH,
    index=False,
)


# ------------------------------------------------------------
# Aggregate individual-checkpoint robustness
# ------------------------------------------------------------

metrics_to_aggregate = [
    "accuracy",
    "precision",
    "recall",
    "specificity",
    "balanced_accuracy",
    "f1",
    "f2",
    "fpr",
    "fnr",
    "mcc",
    "roc_auc",
    "pr_auc",
    "brier_score",
    "log_loss",
    "inference_seconds",
    "peak_gpu_memory_mb",
]

aggregate_record = {
    "candidate_id": (
        "FT_BALANCED"
    ),

    "checkpoint_count": 5,

    "threshold": (
        frozen_threshold
    ),
}

for metric in metrics_to_aggregate:
    values = seed_metrics_frame[
        metric
    ].to_numpy(
        dtype=np.float64
    )

    aggregate_record[
        f"mean_{metric}"
    ] = float(
        np.mean(
            values
        )
    )

    aggregate_record[
        f"std_{metric}"
    ] = float(
        np.std(
            values,
            ddof=1,
        )
    )

    aggregate_record[
        f"minimum_{metric}"
    ] = float(
        np.min(
            values
        )
    )

    aggregate_record[
        f"maximum_{metric}"
    ] = float(
        np.max(
            values
        )
    )

seed_aggregate_frame = pd.DataFrame(
    [
        aggregate_record
    ]
)

seed_aggregate_frame.to_csv(
    SEED_AGGREGATE_PATH,
    index=False,
)


# ------------------------------------------------------------
# Validation-to-holdout gaps for individual checkpoints
# ------------------------------------------------------------

validation_seed_metrics = pd.read_csv(
    VALIDATION_COMMON_THRESHOLD_METRICS_PATH
)

validation_seed_metrics[
    "seed"
] = validation_seed_metrics[
    "seed"
].astype(int)

validation_seed_metrics = (
    validation_seed_metrics
    .sort_values(
        "seed"
    )
    .reset_index(drop=True)
)

if validation_seed_metrics[
    "seed"
].tolist() != expected_seeds:
    raise RuntimeError(
        "Validation common-threshold seed ordering differs."
    )

gap_rows = []

for seed in expected_seeds:
    validation_row = (
        validation_seed_metrics[
            validation_seed_metrics[
                "seed"
            ]
            == seed
        ]
        .iloc[0]
    )

    holdout_row = (
        seed_metrics_frame[
            seed_metrics_frame[
                "seed"
            ]
            == seed
        ]
        .iloc[0]
    )

    gap_rows.append(
        {
            "seed": int(
                seed
            ),

            "threshold": (
                frozen_threshold
            ),

            "validation_accuracy": float(
                validation_row[
                    "accuracy"
                ]
            ),

            "holdout_accuracy": float(
                holdout_row[
                    "accuracy"
                ]
            ),

            "accuracy_gap_holdout_minus_validation": float(
                holdout_row[
                    "accuracy"
                ]
                - validation_row[
                    "accuracy"
                ]
            ),

            "validation_precision": float(
                validation_row[
                    "precision"
                ]
            ),

            "holdout_precision": float(
                holdout_row[
                    "precision"
                ]
            ),

            "precision_gap_holdout_minus_validation": float(
                holdout_row[
                    "precision"
                ]
                - validation_row[
                    "precision"
                ]
            ),

            "validation_recall": float(
                validation_row[
                    "recall"
                ]
            ),

            "holdout_recall": float(
                holdout_row[
                    "recall"
                ]
            ),

            "recall_gap_holdout_minus_validation": float(
                holdout_row[
                    "recall"
                ]
                - validation_row[
                    "recall"
                ]
            ),

            "validation_f1": float(
                validation_row[
                    "f1"
                ]
            ),

            "holdout_f1": float(
                holdout_row[
                    "f1"
                ]
            ),

            "f1_gap_holdout_minus_validation": float(
                holdout_row[
                    "f1"
                ]
                - validation_row[
                    "f1"
                ]
            ),

            "validation_f2": float(
                validation_row[
                    "f2"
                ]
            ),

            "holdout_f2": float(
                holdout_row[
                    "f2"
                ]
            ),

            "f2_gap_holdout_minus_validation": float(
                holdout_row[
                    "f2"
                ]
                - validation_row[
                    "f2"
                ]
            ),

            "validation_fpr": float(
                validation_row[
                    "fpr"
                ]
            ),

            "holdout_fpr": float(
                holdout_row[
                    "fpr"
                ]
            ),

            "fpr_gap_holdout_minus_validation": float(
                holdout_row[
                    "fpr"
                ]
                - validation_row[
                    "fpr"
                ]
            ),

            "validation_fnr": float(
                validation_row[
                    "fnr"
                ]
            ),

            "holdout_fnr": float(
                holdout_row[
                    "fnr"
                ]
            ),

            "fnr_gap_holdout_minus_validation": float(
                holdout_row[
                    "fnr"
                ]
                - validation_row[
                    "fnr"
                ]
            ),

            "validation_roc_auc": float(
                validation_row[
                    "roc_auc"
                ]
            ),

            "holdout_roc_auc": float(
                holdout_row[
                    "roc_auc"
                ]
            ),

            "roc_auc_gap_holdout_minus_validation": float(
                holdout_row[
                    "roc_auc"
                ]
                - validation_row[
                    "roc_auc"
                ]
            ),

            "validation_pr_auc": float(
                validation_row[
                    "pr_auc"
                ]
            ),

            "holdout_pr_auc": float(
                holdout_row[
                    "pr_auc"
                ]
            ),

            "pr_auc_gap_holdout_minus_validation": float(
                holdout_row[
                    "pr_auc"
                ]
                - validation_row[
                    "pr_auc"
                ]
            ),
        }
    )

gap_frame = pd.DataFrame(
    gap_rows
)

gap_frame.to_csv(
    VALIDATION_HOLDOUT_GAPS_PATH,
    index=False,
)


# ------------------------------------------------------------
# Ensemble validation comparison
# ------------------------------------------------------------

validation_archive = np.load(
    VALIDATION_PROBABILITIES_PATH,
    allow_pickle=False,
)

validation_labels = np.asarray(
    validation_archive[
        "y_true"
    ],
    dtype=np.int8,
)

validation_probability_matrix = np.vstack(
    [
        np.asarray(
            validation_archive[
                f"seed_{seed}"
            ],
            dtype=np.float64,
        )
        for seed in expected_seeds
    ]
)

validation_ensemble_probabilities = np.mean(
    validation_probability_matrix,
    axis=0,
)

validation_ensemble_metrics = binary_metrics(
    validation_labels,
    validation_ensemble_probabilities,
    frozen_threshold,
)

ensemble_gap_metrics = {}

for metric in [
    "accuracy",
    "precision",
    "recall",
    "specificity",
    "balanced_accuracy",
    "f1",
    "f2",
    "fpr",
    "fnr",
    "mcc",
    "roc_auc",
    "pr_auc",
    "brier_score",
    "log_loss",
]:
    ensemble_gap_metrics[
        f"validation_{metric}"
    ] = float(
        validation_ensemble_metrics[
            metric
        ]
    )

    ensemble_gap_metrics[
        f"holdout_{metric}"
    ] = float(
        ensemble_metrics[
            metric
        ]
    )

    ensemble_gap_metrics[
        (
            f"{metric}_gap_"
            "holdout_minus_validation"
        )
    ] = float(
        ensemble_metrics[
            metric
        ]
        - validation_ensemble_metrics[
            metric
        ]
    )

ensemble_gap_record = {
    "model": (
        "five_checkpoint_soft_voting_ensemble"
    ),

    "threshold": (
        frozen_threshold
    ),

    "ensemble_method": (
        "unweighted arithmetic mean probabilities"
    ),

    **ensemble_gap_metrics,
}

atomic_json_write(
    ENSEMBLE_VALIDATION_HOLDOUT_GAP_PATH,
    ensemble_gap_record,
)


# ------------------------------------------------------------
# Save final result and metadata
# ------------------------------------------------------------

evaluation_runtime_seconds = float(
    time.perf_counter()
    - evaluation_start
)

result_record = {
    "stage": "15.6A",

    "status": "COMPLETED",

    "completed_at_utc": datetime.now(
        timezone.utc
    ).isoformat(),

    "preholdout_commit": (
        evaluation_plan[
            "preholdout_commit"
        ]
    ),

    "preholdout_lock_sha256": (
        evaluation_plan[
            "preholdout_lock_sha256"
        ]
    ),

    "candidate_id": "FT_BALANCED",

    "architecture_frozen": True,

    "threshold": (
        frozen_threshold
    ),

    "threshold_frozen": True,

    "checkpoint_set_frozen": True,

    "checkpoint_seeds": (
        expected_seeds
    ),

    "holdout_row_count": int(
        len(
            y_holdout
        )
    ),

    "holdout_benign_count": (
        holdout_benign_count
    ),

    "holdout_attack_count": (
        holdout_attack_count
    ),

    "individual_checkpoint_metrics": (
        seed_metrics_frame.to_dict(
            orient="records"
        )
    ),

    "individual_checkpoint_aggregate": (
        aggregate_record
    ),

    "primary_ensemble_result": (
        ensemble_metrics
    ),

    "ensemble_validation_holdout_gap": (
        ensemble_gap_record
    ),

    "evaluation_runtime_seconds": (
        evaluation_runtime_seconds
    ),

    "holdout_opened": True,

    "holdout_evaluation_count": 1,

    "holdout_status": "EVALUATED_ONCE",

    "selection_after_holdout": False,

    "threshold_adjustment_after_holdout": False,

    "retraining_after_holdout": False,

    "artifacts": {
        "holdout_probabilities": str(
            HOLDOUT_PROBABILITIES_PATH
        ),

        "holdout_predictions": str(
            HOLDOUT_PREDICTIONS_PATH
        ),

        "seed_metrics": str(
            SEED_METRICS_PATH
        ),

        "seed_aggregate": str(
            SEED_AGGREGATE_PATH
        ),

        "ensemble_metrics": str(
            ENSEMBLE_METRICS_PATH
        ),

        "confusion_matrices": str(
            CONFUSION_MATRICES_PATH
        ),

        "validation_holdout_gaps": str(
            VALIDATION_HOLDOUT_GAPS_PATH
        ),

        "ensemble_validation_holdout_gap": str(
            ENSEMBLE_VALIDATION_HOLDOUT_GAP_PATH
        ),
    },
}

atomic_json_write(
    RESULT_PATH,
    result_record,
)

metadata = {
    "stage": "15.6A",

    "generated_at_utc": datetime.now(
        timezone.utc
    ).isoformat(),

    "scientific_boundary": (
        "One locked evaluation event after architecture, "
        "threshold, and checkpoint hashes were committed"
    ),

    "primary_reported_model": (
        "Five-checkpoint FT_BALANCED "
        "soft-voting ensemble"
    ),

    "ensemble_method": (
        "Unweighted arithmetic mean probabilities"
    ),

    "operating_threshold": (
        frozen_threshold
    ),

    "architecture_search_during_holdout": False,

    "checkpoint_selection_during_holdout": False,

    "threshold_search_during_holdout": False,

    "threshold_adjustment_during_holdout": False,

    "hyperparameter_tuning_during_holdout": False,

    "calibration_fitting_during_holdout": False,

    "retraining_during_holdout": False,

    "holdout_indices_loaded": True,

    "holdout_features_loaded": True,

    "holdout_labels_loaded": True,

    "holdout_probabilities_generated": True,

    "holdout_metrics_generated": True,

    "holdout_evaluation_count": 1,

    "holdout_status": "EVALUATED_ONCE",

    "GPU": {
        "device": (
            device_name
        ),

        "capability": (
            device_capability
        ),

        "torch_version": (
            torch.__version__
        ),

        "CUDA_runtime": (
            torch.version.cuda
        ),

        "compiled_architectures": (
            compiled_architectures
        ),
    },
}

atomic_json_write(
    METADATA_PATH,
    metadata,
)


# ------------------------------------------------------------
# Finalize execution state
# ------------------------------------------------------------

output_paths = [
    HOLDOUT_PROBABILITIES_PATH,
    HOLDOUT_PREDICTIONS_PATH,
    SEED_METRICS_PATH,
    SEED_AGGREGATE_PATH,
    ENSEMBLE_METRICS_PATH,
    CONFUSION_MATRICES_PATH,
    VALIDATION_HOLDOUT_GAPS_PATH,
    ENSEMBLE_VALIDATION_HOLDOUT_GAP_PATH,
    RESULT_PATH,
    METADATA_PATH,
]

output_hashes = {
    str(path): sha256_file(
        path
    )
    for path in output_paths
}

execution_state.update(
    {
        "status": "COMPLETED",

        "completed_at_utc": datetime.now(
            timezone.utc
        ).isoformat(),

        "holdout_opened": True,

        "holdout_evaluation_count": 1,

        "completed_seed_inferences": (
            expected_seeds
        ),

        "metrics_generated": True,

        "result_path": str(
            RESULT_PATH
        ),

        "output_hashes": (
            output_hashes
        ),
    }
)

atomic_json_write(
    EXECUTION_STATE_PATH,
    execution_state,
)


# ------------------------------------------------------------
# Final summary
# ------------------------------------------------------------

print("\n" + "=" * 118)
print("STAGE 15.6A ONE-TIME HOLDOUT EVALUATION SUMMARY")
print("=" * 118)

print("\nLocked policy:")
print("  Architecture: FT_BALANCED")
print("  Checkpoints: 5")
print(
    "  Seeds:",
    expected_seeds,
)
print("  Frozen threshold: 0.73")
print(
    "  Ensemble:",
    "unweighted arithmetic mean probabilities",
)

print("\nHoldout composition:")
print(
    "  Rows:",
    len(
        y_holdout
    ),
)
print(
    "  Benign:",
    holdout_benign_count,
)
print(
    "  Attack:",
    holdout_attack_count,
)
print(
    "  Attack rate:",
    holdout_attack_count
    / len(
        y_holdout
    ),
)

print("\nIndividual checkpoint results:")
print(
    seed_metrics_frame[
        [
            "seed",
            "threshold",
            "accuracy",
            "precision",
            "recall",
            "f1",
            "f2",
            "fpr",
            "fnr",
            "mcc",
            "roc_auc",
            "pr_auc",
        ]
    ].to_string(
        index=False
    )
)

print("\nFive-checkpoint robustness:")
print(
    "  Mean accuracy:",
    aggregate_record[
        "mean_accuracy"
    ],
)
print(
    "  Mean precision:",
    aggregate_record[
        "mean_precision"
    ],
)
print(
    "  Mean recall:",
    aggregate_record[
        "mean_recall"
    ],
)
print(
    "  Mean F1:",
    aggregate_record[
        "mean_f1"
    ],
)
print(
    "  F1 standard deviation:",
    aggregate_record[
        "std_f1"
    ],
)
print(
    "  Minimum F1:",
    aggregate_record[
        "minimum_f1"
    ],
)
print(
    "  Maximum F1:",
    aggregate_record[
        "maximum_f1"
    ],
)
print(
    "  Mean PR-AUC:",
    aggregate_record[
        "mean_pr_auc"
    ],
)

print("\nPrimary soft-voting ensemble result:")
print(
    "  Accuracy:",
    ensemble_metrics[
        "accuracy"
    ],
)
print(
    "  Precision:",
    ensemble_metrics[
        "precision"
    ],
)
print(
    "  Recall:",
    ensemble_metrics[
        "recall"
    ],
)
print(
    "  F1:",
    ensemble_metrics[
        "f1"
    ],
)
print(
    "  F2:",
    ensemble_metrics[
        "f2"
    ],
)
print(
    "  FPR:",
    ensemble_metrics[
        "fpr"
    ],
)
print(
    "  FNR:",
    ensemble_metrics[
        "fnr"
    ],
)
print(
    "  MCC:",
    ensemble_metrics[
        "mcc"
    ],
)
print(
    "  ROC-AUC:",
    ensemble_metrics[
        "roc_auc"
    ],
)
print(
    "  PR-AUC:",
    ensemble_metrics[
        "pr_auc"
    ],
)
print(
    "  Brier score:",
    ensemble_metrics[
        "brier_score"
    ],
)
print(
    "  Log loss:",
    ensemble_metrics[
        "log_loss"
    ],
)

print("\nEnsemble confusion matrix:")
print(
    "  True negatives:",
    ensemble_metrics[
        "true_negative"
    ],
)
print(
    "  False positives:",
    ensemble_metrics[
        "false_positive"
    ],
)
print(
    "  False negatives:",
    ensemble_metrics[
        "false_negative"
    ],
)
print(
    "  True positives:",
    ensemble_metrics[
        "true_positive"
    ],
)

print("\nEnsemble validation-to-holdout gaps:")
print(
    "  F1 gap:",
    ensemble_gap_record[
        "f1_gap_holdout_minus_validation"
    ],
)
print(
    "  Recall gap:",
    ensemble_gap_record[
        "recall_gap_holdout_minus_validation"
    ],
)
print(
    "  Precision gap:",
    ensemble_gap_record[
        "precision_gap_holdout_minus_validation"
    ],
)
print(
    "  PR-AUC gap:",
    ensemble_gap_record[
        "pr_auc_gap_holdout_minus_validation"
    ],
)

print("\nScientific status:")
print("  Architecture changed after holdout: FALSE")
print("  Checkpoint selected after holdout: FALSE")
print("  Threshold searched on holdout: FALSE")
print("  Threshold changed after holdout: FALSE")
print("  Retraining after holdout: FALSE")
print("  Holdout evaluation count: 1")
print("  Holdout status: EVALUATED_ONCE")

print("\nSaved artifacts:")
print(HOLDOUT_PROBABILITIES_PATH)
print(HOLDOUT_PREDICTIONS_PATH)
print(SEED_METRICS_PATH)
print(SEED_AGGREGATE_PATH)
print(ENSEMBLE_METRICS_PATH)
print(CONFUSION_MATRICES_PATH)
print(VALIDATION_HOLDOUT_GAPS_PATH)
print(ENSEMBLE_VALIDATION_HOLDOUT_GAP_PATH)
print(RESULT_PATH)
print(METADATA_PATH)
print(EXECUTION_STATE_PATH)

print("\nStage 15.6A complete.")
