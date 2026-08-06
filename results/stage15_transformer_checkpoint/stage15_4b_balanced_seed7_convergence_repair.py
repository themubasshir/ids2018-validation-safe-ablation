
from __future__ import annotations

from pathlib import Path
from datetime import datetime, timezone
import importlib.util
import json
import os
import random
import shutil
import time

import joblib
import numpy as np
import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    confusion_matrix,
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

CANDIDATE_CONFIG_PATH = Path(
    os.environ["STAGE15_CANDIDATE_CONFIG"]
)

EXTENSION_CONFIG_PATH = Path(
    os.environ["STAGE15_EXTENSION_CONFIG"]
)

ORIGINAL_RESULT_PATH = Path(
    os.environ["STAGE15_ORIGINAL_RESULT"]
)

ORIGINAL_HISTORY_PATH = Path(
    os.environ["STAGE15_ORIGINAL_HISTORY"]
)

ORIGINAL_BEST_CHECKPOINT_PATH = Path(
    os.environ["STAGE15_ORIGINAL_BEST_CHECKPOINT"]
)

ORIGINAL_LAST_CHECKPOINT_PATH = Path(
    os.environ["STAGE15_ORIGINAL_LAST_CHECKPOINT"]
)

EXTENSION_HISTORY_PATH = Path(
    os.environ["STAGE15_EXTENSION_HISTORY"]
)

COMBINED_HISTORY_PATH = Path(
    os.environ["STAGE15_COMBINED_HISTORY"]
)

THRESHOLD_SWEEP_PATH = Path(
    os.environ["STAGE15_THRESHOLD_SWEEP"]
)

VALIDATION_PROBABILITIES_PATH = Path(
    os.environ["STAGE15_VALIDATION_PROBABILITIES"]
)

EXTENDED_BEST_CHECKPOINT_PATH = Path(
    os.environ["STAGE15_EXTENDED_BEST_CHECKPOINT"]
)

EXTENDED_LAST_CHECKPOINT_PATH = Path(
    os.environ["STAGE15_EXTENDED_LAST_CHECKPOINT"]
)

RESULT_PATH = Path(
    os.environ["STAGE15_RESULT"]
)

COMPARISON_PATH = Path(
    os.environ["STAGE15_COMPARISON"]
)

METADATA_PATH = Path(
    os.environ["STAGE15_METADATA"]
)


# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------

def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)

    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


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

    if not np.all(
        selected_indices[:-1]
        <= selected_indices[1:]
    ):
        raise ValueError(
            "Selected indices must be sorted."
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
        usecols=feature_names + ["binary_label"],
        chunksize=chunk_size,
    ):
        global_end = global_start + len(chunk)

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
                selected_indices[left:right]
            )

            local_positions = (
                selected_global - global_start
            )

            selected_chunk = chunk.iloc[
                local_positions
            ]

            X_selected[left:right] = (
                selected_chunk[feature_names]
                .to_numpy(
                    dtype=np.float64,
                    copy=True,
                )
            )

            y_selected[left:right] = (
                selected_chunk["binary_label"]
                .to_numpy(
                    dtype=np.float32,
                    copy=True,
                )
            )

            filled[left:right] = True

        global_start = global_end

    if not filled.all():
        missing_count = int(
            np.sum(~filled)
        )

        raise RuntimeError(
            f"Failed to load {missing_count} selected rows."
        )

    return X_selected, y_selected


def binary_metrics(
    y_true,
    probabilities,
    threshold,
):
    predictions = (
        probabilities >= threshold
    ).astype(np.int8)

    tn, fp, fn, tp = confusion_matrix(
        y_true,
        predictions,
        labels=[0, 1],
    ).ravel()

    precision = precision_score(
        y_true,
        predictions,
        zero_division=0,
    )

    recall = recall_score(
        y_true,
        predictions,
        zero_division=0,
    )

    f1 = (
        2.0 * precision * recall
        / (precision + recall)
        if precision + recall > 0
        else 0.0
    )

    beta_squared = 4.0

    f2 = (
        (1.0 + beta_squared)
        * precision
        * recall
        / (
            beta_squared * precision
            + recall
        )
        if (
            beta_squared * precision
            + recall
        ) > 0
        else 0.0
    )

    fpr = (
        fp / (fp + tn)
        if fp + tn > 0
        else 0.0
    )

    fnr = (
        fn / (fn + tp)
        if fn + tp > 0
        else 0.0
    )

    return {
        "threshold": float(threshold),
        "accuracy": float(
            accuracy_score(
                y_true,
                predictions,
            )
        ),
        "precision": float(precision),
        "recall": float(recall),
        "f1": float(f1),
        "f2": float(f2),
        "fpr": float(fpr),
        "fnr": float(fnr),
        "true_negative": int(tn),
        "false_positive": int(fp),
        "false_negative": int(fn),
        "true_positive": int(tp),
    }


def select_threshold(
    y_true,
    probabilities,
    minimum,
    maximum,
    step,
):
    thresholds = np.arange(
        minimum,
        maximum + step / 2.0,
        step,
    )

    rows = [
        binary_metrics(
            y_true,
            probabilities,
            float(threshold),
        )
        for threshold in thresholds
    ]

    selected = sorted(
        rows,
        key=lambda row: (
            -row["f1"],
            -row["f2"],
            -row["recall"],
            row["fpr"],
            row["threshold"],
        ),
    )[0]

    return selected, rows


@torch.no_grad()
def evaluate_validation(
    model,
    loader,
    criterion,
    device,
):
    model.eval()

    total_loss = 0.0
    total_rows = 0
    probability_batches = []
    label_batches = []

    for features, labels in loader:
        features = features.to(
            device,
            non_blocking=True,
        )

        labels_device = labels.to(
            device,
            non_blocking=True,
        )

        logits = model(features)

        loss = criterion(
            logits,
            labels_device,
        )

        batch_rows = int(
            labels.shape[0]
        )

        total_loss += (
            float(loss.item())
            * batch_rows
        )

        total_rows += batch_rows

        probability_batches.append(
            torch.sigmoid(logits)
            .detach()
            .cpu()
            .numpy()
        )

        label_batches.append(
            labels.numpy()
        )

    probabilities = np.concatenate(
        probability_batches
    ).astype(np.float64)

    labels = np.concatenate(
        label_batches
    ).astype(np.int8)

    return {
        "loss": float(
            total_loss / total_rows
        ),
        "roc_auc": float(
            roc_auc_score(
                labels,
                probabilities,
            )
        ),
        "pr_auc": float(
            average_precision_score(
                labels,
                probabilities,
            )
        ),
        "probabilities": probabilities,
        "labels": labels,
    }


# ------------------------------------------------------------
# Load configuration
# ------------------------------------------------------------

with open(
    FEATURE_CONFIGURATION_PATH,
    "r",
    encoding="utf-8",
) as file:
    feature_configuration = json.load(file)

with open(
    CANDIDATE_CONFIG_PATH,
    "r",
    encoding="utf-8",
) as file:
    candidate_configuration = json.load(file)

with open(
    EXTENSION_CONFIG_PATH,
    "r",
    encoding="utf-8",
) as file:
    extension_configuration = json.load(file)

with open(
    ORIGINAL_RESULT_PATH,
    "r",
    encoding="utf-8",
) as file:
    original_result = json.load(file)

retained_features = list(
    feature_configuration["retained_features"]
)

balanced_candidates = [
    candidate
    for candidate in candidate_configuration["candidates"]
    if candidate["candidate_id"] == "FT_BALANCED"
]

if len(balanced_candidates) != 1:
    raise RuntimeError(
        "FT_BALANCED configuration was not resolved uniquely."
    )

candidate = balanced_candidates[0]

candidate_id = "FT_BALANCED"
seed = 7
run_id = "FT_BALANCED_seed_7"

if len(retained_features) != 70:
    raise RuntimeError(
        "Expected 70 retained predictors."
    )

set_seed(seed)


# ------------------------------------------------------------
# Validate CUDA
# ------------------------------------------------------------

if not torch.cuda.is_available():
    raise RuntimeError(
        "CUDA is unavailable."
    )

device = torch.device("cuda:0")

device_name = torch.cuda.get_device_name(0)

device_capability = list(
    torch.cuda.get_device_capability(0)
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
        "PyTorch build lacks sm_60."
    )


# ------------------------------------------------------------
# Load training and validation indices only
# ------------------------------------------------------------

split_archive = np.load(
    SAFE_SPLIT_PATH,
    allow_pickle=False,
)

train_indices = np.asarray(
    split_archive["train_indices"],
    dtype=np.int64,
)

validation_indices = np.asarray(
    split_archive["validation_indices"],
    dtype=np.int64,
)

# The holdout index array is deliberately not accessed.

if len(train_indices) != 154_686:
    raise RuntimeError(
        "Unexpected training-row count."
    )

if len(validation_indices) != 37_835:
    raise RuntimeError(
        "Unexpected validation-row count."
    )

combined_indices = np.sort(
    np.concatenate(
        [
            train_indices,
            validation_indices,
        ]
    )
)

X_selected_raw, y_selected = (
    load_selected_rows(
        DATASET_PATH,
        retained_features,
        combined_indices,
    )
)

train_positions = np.searchsorted(
    combined_indices,
    train_indices,
)

validation_positions = np.searchsorted(
    combined_indices,
    validation_indices,
)

X_train_raw = X_selected_raw[
    train_positions
]

X_validation_raw = X_selected_raw[
    validation_positions
]

y_train = y_selected[
    train_positions
]

y_validation = y_selected[
    validation_positions
]

del X_selected_raw
del y_selected


# ------------------------------------------------------------
# Apply training-only scaler
# ------------------------------------------------------------

scaler = joblib.load(
    SCALER_PATH
)

if int(scaler.n_features_in_) != 70:
    raise RuntimeError(
        "Unexpected scaler feature count."
    )

X_train = scaler.transform(
    X_train_raw
).astype(
    np.float32,
    copy=False,
)

X_validation = scaler.transform(
    X_validation_raw
).astype(
    np.float32,
    copy=False,
)

del X_train_raw
del X_validation_raw

if not np.isfinite(X_train).all():
    raise RuntimeError(
        "Training features contain non-finite values."
    )

if not np.isfinite(X_validation).all():
    raise RuntimeError(
        "Validation features contain non-finite values."
    )


# ------------------------------------------------------------
# Class weight from training labels only
# ------------------------------------------------------------

training_benign_count = int(
    np.sum(y_train == 0)
)

training_attack_count = int(
    np.sum(y_train == 1)
)

if training_benign_count != 110_161:
    raise RuntimeError(
        "Unexpected training benign count."
    )

if training_attack_count != 44_525:
    raise RuntimeError(
        "Unexpected training attack count."
    )

positive_class_weight = float(
    training_benign_count
    / training_attack_count
)


# ------------------------------------------------------------
# Import model class
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
        "Unable to import FT-Transformer module."
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
# Select resume checkpoint
# ------------------------------------------------------------

if EXTENDED_LAST_CHECKPOINT_PATH.exists():
    resume_checkpoint_path = (
        EXTENDED_LAST_CHECKPOINT_PATH
    )

    print(
        "Existing Stage 15.4B continuation checkpoint found."
    )

else:
    resume_checkpoint_path = (
        ORIGINAL_LAST_CHECKPOINT_PATH
    )

    if not EXTENDED_BEST_CHECKPOINT_PATH.exists():
        shutil.copy2(
            ORIGINAL_BEST_CHECKPOINT_PATH,
            EXTENDED_BEST_CHECKPOINT_PATH,
        )

    print(
        "Starting continuation from the "
        "Stage 15.4A epoch-40 checkpoint."
    )

resume_checkpoint = torch.load(
    resume_checkpoint_path,
    map_location=device,
    weights_only=False,
)

if resume_checkpoint["candidate_id"] != candidate_id:
    raise RuntimeError(
        "Resume checkpoint candidate mismatch."
    )

if int(resume_checkpoint["seed"]) != seed:
    raise RuntimeError(
        "Resume checkpoint seed mismatch."
    )

resume_epoch = int(
    resume_checkpoint["epoch"]
)

if resume_epoch < 40:
    raise RuntimeError(
        "Resume checkpoint predates epoch 40."
    )

maximum_total_epochs = int(
    extension_configuration[
        "maximum_total_epochs"
    ]
)

if resume_epoch > maximum_total_epochs:
    raise RuntimeError(
        "Resume checkpoint exceeds the configured ceiling."
    )


# ------------------------------------------------------------
# Restore exact shuffled-data generator state
# ------------------------------------------------------------

loader_generator = torch.Generator()

# STAGE15_NATIVE_BYTE_RNG_STATE_PATCH
# Reconstruct the saved RNG bytes as a native CPU ByteTensor
# belonging to the currently active isolated PyTorch runtime.
# The byte sequence is preserved exactly; the generator is not
# reseeded or reset.
raw_loader_generator_state = resume_checkpoint[
    "loader_generator_state"
]

if hasattr(
    raw_loader_generator_state,
    "detach",
):
    raw_loader_state_array = (
        raw_loader_generator_state
        .detach()
        .cpu()
        .numpy()
        .astype(
            np.uint8,
            copy=True,
        )
    )
else:
    raw_loader_state_array = np.asarray(
        raw_loader_generator_state,
        dtype=np.uint8,
    ).copy()

raw_loader_state_array = (
    raw_loader_state_array
    .reshape(-1)
)

native_loader_generator_state = torch.tensor(
    raw_loader_state_array,
    dtype=torch.uint8,
    device="cpu",
)

if (
    native_loader_generator_state.dtype
    != torch.uint8
):
    raise RuntimeError(
        "Reconstructed RNG state is not uint8."
    )

if (
    native_loader_generator_state.device.type
    != "cpu"
):
    raise RuntimeError(
        "Reconstructed RNG state is not on CPU."
    )

if not np.array_equal(
    native_loader_generator_state.numpy(),
    raw_loader_state_array,
):
    raise RuntimeError(
        "RNG-state byte reconstruction was not exact."
    )

loader_generator.set_state(
    native_loader_generator_state
)

print(
    "Restored exact DataLoader RNG state:",
    int(
        native_loader_generator_state.numel()
    ),
    "bytes",
)

training_dataset = TensorDataset(
    torch.from_numpy(X_train),
    torch.from_numpy(
        y_train.astype(
            np.float32,
            copy=False,
        )
    ),
)

validation_dataset = TensorDataset(
    torch.from_numpy(X_validation),
    torch.from_numpy(
        y_validation.astype(
            np.float32,
            copy=False,
        )
    ),
)

batch_size = int(
    extension_configuration[
        "batch_size"
    ]
)

training_loader = DataLoader(
    training_dataset,
    batch_size=batch_size,
    shuffle=True,
    generator=loader_generator,
    num_workers=2,
    pin_memory=True,
    persistent_workers=True,
    drop_last=False,
)

validation_loader = DataLoader(
    validation_dataset,
    batch_size=batch_size,
    shuffle=False,
    num_workers=2,
    pin_memory=True,
    persistent_workers=True,
    drop_last=False,
)


# ------------------------------------------------------------
# Restore model, optimizer, and scheduler
# ------------------------------------------------------------

torch.cuda.empty_cache()
torch.cuda.reset_peak_memory_stats()

model = NumericFTTransformer(
    n_features=70,
    d_token=int(candidate["d_token"]),
    n_heads=int(candidate["n_heads"]),
    n_layers=int(candidate["n_layers"]),
    d_ff=int(candidate["d_ff"]),
    dropout=float(candidate["dropout"]),
).to(device)

parameter_count = int(
    sum(
        parameter.numel()
        for parameter in model.parameters()
        if parameter.requires_grad
    )
)

criterion = nn.BCEWithLogitsLoss(
    pos_weight=torch.tensor(
        positive_class_weight,
        dtype=torch.float32,
        device=device,
    )
)

optimizer = torch.optim.AdamW(
    model.parameters(),
    lr=float(candidate["learning_rate"]),
    weight_decay=float(
        candidate["weight_decay"]
    ),
)

scheduler = (
    torch.optim.lr_scheduler
    .ReduceLROnPlateau(
        optimizer,
        mode="max",
        factor=0.5,
        patience=2,
        min_lr=1e-5,
    )
)

model.load_state_dict(
    resume_checkpoint[
        "model_state_dict"
    ]
)

optimizer.load_state_dict(
    resume_checkpoint[
        "optimizer_state_dict"
    ]
)

scheduler.load_state_dict(
    resume_checkpoint[
        "scheduler_state_dict"
    ]
)

best_epoch = int(
    resume_checkpoint["best_epoch"]
)

best_pr_auc = float(
    resume_checkpoint["best_pr_auc"]
)

best_validation_loss = float(
    resume_checkpoint[
        "best_validation_loss"
    ]
)

epochs_without_improvement = int(
    resume_checkpoint[
        "epochs_without_improvement"
    ]
)

if best_epoch < 40:
    raise RuntimeError(
        "Expected a best checkpoint at or after epoch 40."
    )


# ------------------------------------------------------------
# Restore continuation history
# ------------------------------------------------------------

if EXTENSION_HISTORY_PATH.exists():
    extension_history_rows = (
        pd.read_csv(
            EXTENSION_HISTORY_PATH
        )
        .to_dict(orient="records")
    )
else:
    extension_history_rows = []

existing_extension_epochs = {
    int(row["epoch"])
    for row in extension_history_rows
}

if existing_extension_epochs:
    if max(existing_extension_epochs) != resume_epoch:
        raise RuntimeError(
            "Continuation history and resume checkpoint "
            "are inconsistent."
        )


# ------------------------------------------------------------
# Continue training
# ------------------------------------------------------------

start_epoch = resume_epoch + 1

patience = int(
    extension_configuration[
        "early_stopping_patience"
    ]
)

gradient_clip_norm = float(
    extension_configuration[
        "gradient_clip_norm"
    ]
)

improvement_tolerance = float(
    extension_configuration[
        "checkpoint_improvement_tolerance"
    ]
)

continuation_start = time.perf_counter()

final_epoch_executed = resume_epoch
early_stopping_triggered = False

for epoch in range(
    start_epoch,
    maximum_total_epochs + 1,
):
    epoch_start = time.perf_counter()

    model.train()

    total_training_loss = 0.0
    total_training_rows = 0

    for features, labels in training_loader:
        features = features.to(
            device,
            non_blocking=True,
        )

        labels = labels.to(
            device,
            non_blocking=True,
        )

        optimizer.zero_grad(
            set_to_none=True
        )

        logits = model(features)

        loss = criterion(
            logits,
            labels,
        )

        if not torch.isfinite(loss):
            raise FloatingPointError(
                "Non-finite training loss encountered."
            )

        loss.backward()

        gradient_norm = (
            torch.nn.utils.clip_grad_norm_(
                model.parameters(),
                max_norm=gradient_clip_norm,
            )
        )

        if not torch.isfinite(
            gradient_norm
        ):
            raise FloatingPointError(
                "Non-finite gradient norm encountered."
            )

        optimizer.step()

        batch_rows = int(
            labels.shape[0]
        )

        total_training_loss += (
            float(loss.item())
            * batch_rows
        )

        total_training_rows += batch_rows

    training_loss = float(
        total_training_loss
        / total_training_rows
    )

    validation_result = evaluate_validation(
        model,
        validation_loader,
        criterion,
        device,
    )

    validation_loss = float(
        validation_result["loss"]
    )

    validation_roc_auc = float(
        validation_result["roc_auc"]
    )

    validation_pr_auc = float(
        validation_result["pr_auc"]
    )

    scheduler.step(
        validation_pr_auc
    )

    current_learning_rate = float(
        optimizer.param_groups[0]["lr"]
    )

    improved = bool(
        validation_pr_auc
        > best_pr_auc
        + improvement_tolerance
        or (
            abs(
                validation_pr_auc
                - best_pr_auc
            )
            <= improvement_tolerance
            and validation_loss
            < best_validation_loss
        )
    )

    if improved:
        best_epoch = int(epoch)
        best_pr_auc = validation_pr_auc
        best_validation_loss = validation_loss
        epochs_without_improvement = 0

        torch.save(
            {
                "stage": "15.4B",
                "run_id": run_id,
                "candidate_id": candidate_id,
                "seed": seed,
                "architecture": candidate,
                "epoch": int(epoch),
                "model_state_dict": (
                    model.state_dict()
                ),
                "optimizer_state_dict": (
                    optimizer.state_dict()
                ),
                "scheduler_state_dict": (
                    scheduler.state_dict()
                ),
                "validation_pr_auc": (
                    best_pr_auc
                ),
                "validation_loss": (
                    best_validation_loss
                ),
                "positive_class_weight": (
                    positive_class_weight
                ),
                "feature_count": 70,
                "continued_from_epoch": 40,
            },
            EXTENDED_BEST_CHECKPOINT_PATH,
        )

    else:
        epochs_without_improvement += 1

    epoch_seconds = float(
        time.perf_counter()
        - epoch_start
    )

    extension_history_rows.append(
        {
            "stage": "15.4B",
            "run_id": run_id,
            "candidate_id": candidate_id,
            "seed": seed,
            "epoch": int(epoch),
            "training_loss": training_loss,
            "validation_loss": validation_loss,
            "validation_roc_auc": (
                validation_roc_auc
            ),
            "validation_pr_auc": (
                validation_pr_auc
            ),
            "learning_rate": (
                current_learning_rate
            ),
            "improved_best_checkpoint": (
                improved
            ),
            "best_epoch_after_epoch": (
                best_epoch
            ),
            "epochs_without_improvement": (
                epochs_without_improvement
            ),
            "epoch_seconds": epoch_seconds,
        }
    )

    pd.DataFrame(
        extension_history_rows
    ).to_csv(
        EXTENSION_HISTORY_PATH,
        index=False,
    )

    torch.save(
        {
            "stage": "15.4B",
            "run_id": run_id,
            "candidate_id": candidate_id,
            "seed": seed,
            "architecture": candidate,
            "epoch": int(epoch),
            "best_epoch": int(best_epoch),
            "best_pr_auc": float(
                best_pr_auc
            ),
            "best_validation_loss": float(
                best_validation_loss
            ),
            "epochs_without_improvement": int(
                epochs_without_improvement
            ),
            "model_state_dict": (
                model.state_dict()
            ),
            "optimizer_state_dict": (
                optimizer.state_dict()
            ),
            "scheduler_state_dict": (
                scheduler.state_dict()
            ),
            "loader_generator_state": (
                loader_generator.get_state()
            ),
            "continued_from_epoch": 40,
        },
        EXTENDED_LAST_CHECKPOINT_PATH,
    )

    final_epoch_executed = int(epoch)

    print(
        f"Epoch {epoch:02d} | "
        f"train loss {training_loss:.6f} | "
        f"val loss {validation_loss:.6f} | "
        f"ROC-AUC {validation_roc_auc:.6f} | "
        f"PR-AUC {validation_pr_auc:.6f} | "
        f"lr {current_learning_rate:.2e} | "
        f"{epoch_seconds:.1f}s"
    )

    if (
        epochs_without_improvement
        >= patience
    ):
        early_stopping_triggered = True

        print(
            "Convergence early stopping triggered."
        )

        break


# ------------------------------------------------------------
# Load best extended checkpoint
# ------------------------------------------------------------

if not EXTENDED_BEST_CHECKPOINT_PATH.exists():
    raise FileNotFoundError(
        "Extended best checkpoint was not created."
    )

best_checkpoint = torch.load(
    EXTENDED_BEST_CHECKPOINT_PATH,
    map_location=device,
    weights_only=False,
)

model.load_state_dict(
    best_checkpoint[
        "model_state_dict"
    ]
)

extended_best_epoch = int(
    best_checkpoint["epoch"]
)

extended_best_pr_auc = float(
    best_checkpoint[
        "validation_pr_auc"
    ]
)

extended_best_validation_loss = float(
    best_checkpoint[
        "validation_loss"
    ]
)


# ------------------------------------------------------------
# Final validation evaluation
# ------------------------------------------------------------

final_validation = evaluate_validation(
    model,
    validation_loader,
    criterion,
    device,
)

validation_probabilities = (
    final_validation[
        "probabilities"
    ]
)

validation_labels = (
    final_validation[
        "labels"
    ]
)

if not np.array_equal(
    validation_labels,
    y_validation.astype(np.int8),
):
    raise RuntimeError(
        "Validation label ordering changed."
    )

selected_threshold_metrics, (
    threshold_rows
) = select_threshold(
    validation_labels,
    validation_probabilities,
    minimum=float(
        extension_configuration[
            "threshold_minimum"
        ]
    ),
    maximum=float(
        extension_configuration[
            "threshold_maximum"
        ]
    ),
    step=float(
        extension_configuration[
            "threshold_step"
        ]
    ),
)

pd.DataFrame(
    [
        {
            "run_id": run_id,
            "candidate_id": candidate_id,
            "seed": seed,
            **row,
        }
        for row in threshold_rows
    ]
).to_csv(
    THRESHOLD_SWEEP_PATH,
    index=False,
)

np.savez_compressed(
    VALIDATION_PROBABILITIES_PATH,
    y_true=validation_labels,
    probabilities=(
        validation_probabilities.astype(
            np.float32
        )
    ),
)

extended_roc_auc = float(
    roc_auc_score(
        validation_labels,
        validation_probabilities,
    )
)

extended_pr_auc = float(
    average_precision_score(
        validation_labels,
        validation_probabilities,
    )
)


# ------------------------------------------------------------
# Combine original and extension histories
# ------------------------------------------------------------

original_history = pd.read_csv(
    ORIGINAL_HISTORY_PATH
)

extension_history = pd.read_csv(
    EXTENSION_HISTORY_PATH
)

if int(original_history["epoch"].max()) != 40:
    raise RuntimeError(
        "Original history does not end at epoch 40."
    )

if not extension_history.empty:
    if int(extension_history["epoch"].min()) != 41:
        raise RuntimeError(
            "Extension history does not begin at epoch 41."
        )

combined_history = pd.concat(
    [
        original_history,
        extension_history,
    ],
    ignore_index=True,
    sort=False,
)

if combined_history["epoch"].duplicated().any():
    raise RuntimeError(
        "Combined history contains duplicate epochs."
    )

combined_history.to_csv(
    COMBINED_HISTORY_PATH,
    index=False,
)


# ------------------------------------------------------------
# Save comparison and result
# ------------------------------------------------------------

original_f1 = float(
    original_result["f1"]
)

original_pr_auc = float(
    original_result["pr_auc"]
)

original_recall = float(
    original_result["recall"]
)

original_f2 = float(
    original_result["f2"]
)

comparison_record = {
    "candidate_id": candidate_id,
    "seed": seed,
    "original_best_epoch": int(
        original_result["best_epoch"]
    ),
    "extended_best_epoch": (
        extended_best_epoch
    ),
    "original_final_epoch": int(
        original_result[
            "final_epoch_executed"
        ]
    ),
    "extended_final_epoch": (
        final_epoch_executed
    ),
    "original_threshold": float(
        original_result["threshold"]
    ),
    "extended_threshold": float(
        selected_threshold_metrics[
            "threshold"
        ]
    ),
    "original_f1": original_f1,
    "extended_f1": float(
        selected_threshold_metrics["f1"]
    ),
    "f1_change": float(
        selected_threshold_metrics["f1"]
        - original_f1
    ),
    "original_f2": original_f2,
    "extended_f2": float(
        selected_threshold_metrics["f2"]
    ),
    "f2_change": float(
        selected_threshold_metrics["f2"]
        - original_f2
    ),
    "original_recall": original_recall,
    "extended_recall": float(
        selected_threshold_metrics[
            "recall"
        ]
    ),
    "recall_change": float(
        selected_threshold_metrics[
            "recall"
        ]
        - original_recall
    ),
    "original_pr_auc": original_pr_auc,
    "extended_pr_auc": extended_pr_auc,
    "pr_auc_change": float(
        extended_pr_auc
        - original_pr_auc
    ),
}

pd.DataFrame(
    [comparison_record]
).to_csv(
    COMPARISON_PATH,
    index=False,
)

best_checkpoint_at_extension_ceiling = bool(
    extended_best_epoch
    == maximum_total_epochs
)

convergence_repaired = bool(
    not best_checkpoint_at_extension_ceiling
)

continuation_runtime_seconds = float(
    time.perf_counter()
    - continuation_start
)

peak_gpu_memory_mb = float(
    torch.cuda.max_memory_allocated()
    / (1024 ** 2)
)

result_record = {
    "stage": "15.4B",
    "status": "COMPLETED",
    "run_id": run_id,
    "candidate_id": candidate_id,
    "seed": seed,
    "resume_source": str(
        ORIGINAL_LAST_CHECKPOINT_PATH
    ),
    "continued_from_epoch": 40,
    "maximum_total_epochs": (
        maximum_total_epochs
    ),
    "original_result": {
        "best_epoch": int(
            original_result["best_epoch"]
        ),
        "final_epoch_executed": int(
            original_result[
                "final_epoch_executed"
            ]
        ),
        "threshold": float(
            original_result["threshold"]
        ),
        "f1": original_f1,
        "f2": original_f2,
        "recall": original_recall,
        "pr_auc": original_pr_auc,
    },
    "extended_result": {
        "parameter_count": (
            parameter_count
        ),
        "best_epoch": (
            extended_best_epoch
        ),
        "final_epoch_executed": (
            final_epoch_executed
        ),
        "additional_epochs_executed": int(
            final_epoch_executed - 40
        ),
        "early_stopping_triggered": (
            early_stopping_triggered
        ),
        "best_checkpoint_at_extension_ceiling": (
            best_checkpoint_at_extension_ceiling
        ),
        "convergence_repaired": (
            convergence_repaired
        ),
        "best_validation_loss": (
            extended_best_validation_loss
        ),
        "roc_auc": extended_roc_auc,
        "pr_auc": extended_pr_auc,
        **selected_threshold_metrics,
        "peak_gpu_memory_mb": (
            peak_gpu_memory_mb
        ),
        "runtime_seconds": (
            continuation_runtime_seconds
        ),
        "best_checkpoint_path": str(
            EXTENDED_BEST_CHECKPOINT_PATH
        ),
        "last_checkpoint_path": str(
            EXTENDED_LAST_CHECKPOINT_PATH
        ),
    },
    "metric_changes": {
        "f1_change": (
            comparison_record["f1_change"]
        ),
        "f2_change": (
            comparison_record["f2_change"]
        ),
        "recall_change": (
            comparison_record[
                "recall_change"
            ]
        ),
        "pr_auc_change": (
            comparison_record[
                "pr_auc_change"
            ]
        ),
    },
    "architecture_frozen": False,
    "holdout_status": "UNTOUCHED",
}

with open(
    RESULT_PATH,
    "w",
    encoding="utf-8",
) as file:
    json.dump(
        result_record,
        file,
        indent=2,
    )

metadata = {
    "stage": "15.4B",
    "generated_at_utc": datetime.now(
        timezone.utc
    ).isoformat(),
    "purpose": (
        "Resolve the Stage 15.4A FT_BALANCED seed-7 "
        "best-checkpoint-at-ceiling condition."
    ),
    "continuation_integrity": {
        "model_state_restored": True,
        "optimizer_state_restored": True,
        "scheduler_state_restored": True,
        "shuffle_generator_state_restored": True,
        "class_weight_unchanged": True,
        "early_stopping_metric_unchanged": True,
        "early_stopping_patience_unchanged": True,
        "only_epoch_ceiling_changed": True,
    },
    "data_access": {
        "training_indices_loaded": True,
        "validation_indices_loaded": True,
        "holdout_indices_loaded": False,
        "holdout_features_loaded": False,
        "holdout_labels_loaded": False,
        "holdout_probabilities_generated": False,
        "holdout_metrics_generated": False,
    },
    "architecture_frozen": False,
    "next_step": (
        "Add two independent confirmation seeds across "
        "all three architectures and aggregate five seeds."
    ),
}

with open(
    METADATA_PATH,
    "w",
    encoding="utf-8",
) as file:
    json.dump(
        metadata,
        file,
        indent=2,
    )


# ------------------------------------------------------------
# Final summary
# ------------------------------------------------------------

print("\n" + "=" * 112)
print("STAGE 15.4B CONVERGENCE REPAIR SUMMARY")
print("=" * 112)

print("\nContinuation:")
print("  Candidate: FT_BALANCED")
print("  Seed: 7")
print("  Original ceiling: 40")
print(
    "  Extended ceiling:",
    maximum_total_epochs,
)
print(
    "  Final epoch executed:",
    final_epoch_executed,
)
print(
    "  Extended best epoch:",
    extended_best_epoch,
)
print(
    "  Early stopping triggered:",
    early_stopping_triggered,
)

print("\nExtended validation result:")
print(
    "  Threshold:",
    selected_threshold_metrics[
        "threshold"
    ],
)
print(
    "  Accuracy:",
    selected_threshold_metrics[
        "accuracy"
    ],
)
print(
    "  Precision:",
    selected_threshold_metrics[
        "precision"
    ],
)
print(
    "  Recall:",
    selected_threshold_metrics[
        "recall"
    ],
)
print(
    "  F1:",
    selected_threshold_metrics[
        "f1"
    ],
)
print(
    "  F2:",
    selected_threshold_metrics[
        "f2"
    ],
)
print(
    "  FPR:",
    selected_threshold_metrics[
        "fpr"
    ],
)
print(
    "  FNR:",
    selected_threshold_metrics[
        "fnr"
    ],
)
print(
    "  ROC-AUC:",
    extended_roc_auc,
)
print(
    "  PR-AUC:",
    extended_pr_auc,
)

print("\nOriginal-to-extended change:")
print(
    "  F1 change:",
    comparison_record["f1_change"],
)
print(
    "  F2 change:",
    comparison_record["f2_change"],
)
print(
    "  Recall change:",
    comparison_record[
        "recall_change"
    ],
)
print(
    "  PR-AUC change:",
    comparison_record[
        "pr_auc_change"
    ],
)

print("\nConvergence assessment:")
print(
    "  Best checkpoint at epoch 70:",
    best_checkpoint_at_extension_ceiling,
)
print(
    "  Convergence repaired:",
    convergence_repaired,
)

print("\nArchitecture frozen:")
print("  FALSE")

print("\nHoldout status:")
print("  UNTOUCHED")

print("\nSaved artifacts:")
print(EXTENSION_HISTORY_PATH)
print(COMBINED_HISTORY_PATH)
print(THRESHOLD_SWEEP_PATH)
print(VALIDATION_PROBABILITIES_PATH)
print(EXTENDED_BEST_CHECKPOINT_PATH)
print(EXTENDED_LAST_CHECKPOINT_PATH)
print(COMPARISON_PATH)
print(RESULT_PATH)
print(METADATA_PATH)

print("\nStage 15.4B complete.")
