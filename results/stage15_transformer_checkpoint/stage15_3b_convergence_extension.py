
from __future__ import annotations

from pathlib import Path
from datetime import datetime, timezone
import importlib.util
import json
import math
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
from torch.utils.data import DataLoader, TensorDataset


# ------------------------------------------------------------
# Paths from environment
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
    os.environ["STAGE15_CANDIDATES"]
)

EXTENSION_CONFIG_PATH = Path(
    os.environ["STAGE15_EXTENSION_CONFIG"]
)

ORIGINAL_METRICS_PATH = Path(
    os.environ["STAGE15_ORIGINAL_METRICS"]
)

ORIGINAL_MODEL_DIR = Path(
    os.environ["STAGE15_ORIGINAL_MODEL_DIR"]
)

EXTENDED_MODEL_DIR = Path(
    os.environ["STAGE15_EXTENDED_MODEL_DIR"]
)

EXTENSION_HISTORY_PATH = Path(
    os.environ["STAGE15_EXTENSION_HISTORY"]
)

EXTENDED_METRICS_PATH = Path(
    os.environ["STAGE15_EXTENDED_METRICS"]
)

COMPARISON_PATH = Path(
    os.environ["STAGE15_COMPARISON"]
)

THRESHOLD_SWEEP_PATH = Path(
    os.environ["STAGE15_THRESHOLD_SWEEP"]
)

VALIDATION_PROBABILITIES_PATH = Path(
    os.environ["STAGE15_VALIDATION_PROBABILITIES"]
)

SELECTION_PATH = Path(
    os.environ["STAGE15_SELECTION"]
)

RESULT_PATH = Path(
    os.environ["STAGE15_RESULT"]
)

METADATA_PATH = Path(
    os.environ["STAGE15_METADATA"]
)


# ------------------------------------------------------------
# Reproducibility
# ------------------------------------------------------------

def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)

    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


# ------------------------------------------------------------
# Load selected rows without retaining holdout
# ------------------------------------------------------------

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
            selected_global = selected_indices[left:right]

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
        raise RuntimeError(
            "Not all selected rows were loaded."
        )

    return X_selected, y_selected


# ------------------------------------------------------------
# Evaluation helpers
# ------------------------------------------------------------

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

    with torch.no_grad():
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
# Load configurations
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

retained_features = list(
    feature_configuration["retained_features"]
)

candidates = candidate_configuration["candidates"]
seed = int(extension_configuration["seed"])

if len(retained_features) != 70:
    raise RuntimeError(
        "Expected 70 retained predictors."
    )

set_seed(seed)


# ------------------------------------------------------------
# CUDA validation
# ------------------------------------------------------------

if not torch.cuda.is_available():
    raise RuntimeError(
        "CUDA is unavailable."
    )

device = torch.device("cuda:0")

if list(
    torch.cuda.get_device_capability(0)
) != [6, 0]:
    raise RuntimeError(
        "Expected Tesla P100 capability [6, 0]."
    )

if "sm_60" not in torch.cuda.get_arch_list():
    raise RuntimeError(
        "PyTorch build does not contain sm_60."
    )


# ------------------------------------------------------------
# Load train and validation indices only
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

# holdout_indices is deliberately not read.

if len(train_indices) != 154_686:
    raise RuntimeError(
        "Unexpected training size."
    )

if len(validation_indices) != 37_835:
    raise RuntimeError(
        "Unexpected validation size."
    )

combined_indices = np.sort(
    np.concatenate(
        [
            train_indices,
            validation_indices,
        ]
    )
)

X_selected, y_selected = load_selected_rows(
    DATASET_PATH,
    retained_features,
    combined_indices,
)

train_positions = np.searchsorted(
    combined_indices,
    train_indices,
)

validation_positions = np.searchsorted(
    combined_indices,
    validation_indices,
)

X_train_raw = X_selected[
    train_positions
]

X_validation_raw = X_selected[
    validation_positions
]

y_train = y_selected[
    train_positions
]

y_validation = y_selected[
    validation_positions
]

del X_selected
del y_selected


# ------------------------------------------------------------
# Apply archived training-only scaler
# ------------------------------------------------------------

scaler = joblib.load(SCALER_PATH)

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
        "Training values are non-finite."
    )

if not np.isfinite(X_validation).all():
    raise RuntimeError(
        "Validation values are non-finite."
    )


# ------------------------------------------------------------
# Class weighting
# ------------------------------------------------------------

training_benign_count = int(
    np.sum(y_train == 0)
)

training_attack_count = int(
    np.sum(y_train == 1)
)

positive_class_weight = float(
    training_benign_count
    / training_attack_count
)

if training_benign_count != 110_161:
    raise RuntimeError(
        "Unexpected benign count."
    )

if training_attack_count != 44_525:
    raise RuntimeError(
        "Unexpected attack count."
    )


# ------------------------------------------------------------
# Validation loader
# ------------------------------------------------------------

validation_dataset = TensorDataset(
    torch.from_numpy(X_validation),
    torch.from_numpy(
        y_validation.astype(
            np.float32,
            copy=False,
        )
    ),
)

validation_loader = DataLoader(
    validation_dataset,
    batch_size=int(
        extension_configuration[
            "batch_size"
        ]
    ),
    shuffle=False,
    num_workers=2,
    pin_memory=True,
    persistent_workers=True,
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
        "Unable to import model module."
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
# Original metrics
# ------------------------------------------------------------

original_metrics = pd.read_csv(
    ORIGINAL_METRICS_PATH
)

original_metrics_by_candidate = {
    row["candidate_id"]: row.to_dict()
    for _, row in original_metrics.iterrows()
}


# ------------------------------------------------------------
# Extend each candidate
# ------------------------------------------------------------

EXTENDED_MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

history_rows = []
extended_metric_rows = []
comparison_rows = []
threshold_rows = []

probability_archive = {
    "y_true": y_validation.astype(
        np.int8,
        copy=False,
    )
}

candidate_results = []

benchmark_start = time.perf_counter()

for candidate_number, candidate in enumerate(
    candidates,
    start=1,
):
    candidate_id = candidate["candidate_id"]

    print("\n" + "=" * 100)
    print(
        f"EXTENDING {candidate_number}/{len(candidates)}: "
        f"{candidate_id}"
    )
    print("=" * 100)

    set_seed(seed)

    training_generator = torch.Generator()
    training_generator.manual_seed(seed)

    training_dataset = TensorDataset(
        torch.from_numpy(X_train),
        torch.from_numpy(
            y_train.astype(
                np.float32,
                copy=False,
            )
        ),
    )

    training_loader = DataLoader(
        training_dataset,
        batch_size=int(
            extension_configuration[
                "batch_size"
            ]
        ),
        shuffle=True,
        generator=training_generator,
        num_workers=2,
        pin_memory=True,
        persistent_workers=True,
        drop_last=False,
    )

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

    original_checkpoint_path = (
        ORIGINAL_MODEL_DIR
        / f"{candidate_id}_best.pt"
    )

    checkpoint = torch.load(
        original_checkpoint_path,
        map_location=device,
        weights_only=False,
    )

    model.load_state_dict(
        checkpoint["model_state_dict"]
    )

    optimizer.load_state_dict(
        checkpoint["optimizer_state_dict"]
    )

    start_epoch = int(
        checkpoint["epoch"]
    )

    if start_epoch != int(
        extension_configuration[
            "start_epoch_expected"
        ]
    ):
        raise RuntimeError(
            f"{candidate_id} expected epoch 15, "
            f"found {start_epoch}."
        )

    best_epoch = start_epoch
    best_pr_auc = float(
        checkpoint["validation_pr_auc"]
    )
    best_validation_loss = float(
        checkpoint["validation_loss"]
    )

    extended_checkpoint_path = (
        EXTENDED_MODEL_DIR
        / f"{candidate_id}_best_extended.pt"
    )

    shutil.copy2(
        original_checkpoint_path,
        extended_checkpoint_path,
    )

    scheduler = (
        torch.optim.lr_scheduler
        .ReduceLROnPlateau(
            optimizer,
            mode="max",
            factor=float(
                extension_configuration[
                    "scheduler"
                ]["factor"]
            ),
            patience=int(
                extension_configuration[
                    "scheduler"
                ]["patience"]
            ),
            min_lr=float(
                extension_configuration[
                    "scheduler"
                ]["minimum_learning_rate"]
            ),
        )
    )

    # Initialize scheduler using the archived best metric.
    scheduler.step(best_pr_auc)

    epochs_without_improvement = 0

    candidate_start = time.perf_counter()

    maximum_total_epoch = int(
        extension_configuration[
            "maximum_total_epoch"
        ]
    )

    early_stopping_patience = int(
        extension_configuration[
            "early_stopping_patience"
        ]
    )

    for epoch in range(
        start_epoch + 1,
        maximum_total_epoch + 1,
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
                    f"{candidate_id} generated "
                    "a non-finite training loss."
                )

            loss.backward()

            gradient_norm = (
                torch.nn.utils.clip_grad_norm_(
                    model.parameters(),
                    max_norm=float(
                        extension_configuration[
                            "gradient_clip_norm"
                        ]
                    ),
                )
            )

            if not torch.isfinite(
                gradient_norm
            ):
                raise FloatingPointError(
                    f"{candidate_id} generated "
                    "non-finite gradients."
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

        validation_result = (
            evaluate_validation(
                model,
                validation_loader,
                criterion,
                device,
            )
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

        epoch_seconds = float(
            time.perf_counter() - epoch_start
        )

        improvement_tolerance = float(
            extension_configuration[
                "checkpoint_improvement_tolerance"
            ]
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

        history_rows.append(
            {
                "candidate_id": candidate_id,
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
                "epoch_seconds": epoch_seconds,
            }
        )

        if improved:
            best_pr_auc = validation_pr_auc
            best_validation_loss = (
                validation_loss
            )
            best_epoch = int(epoch)
            epochs_without_improvement = 0

            torch.save(
                {
                    "candidate_id": candidate_id,
                    "architecture": candidate,
                    "epoch": best_epoch,
                    "model_state_dict": (
                        model.state_dict()
                    ),
                    "optimizer_state_dict": (
                        optimizer.state_dict()
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
                    "seed": seed,
                    "continued_from_epoch": (
                        start_epoch
                    ),
                },
                extended_checkpoint_path,
            )

        else:
            epochs_without_improvement += 1

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
            >= early_stopping_patience
        ):
            print(
                "Convergence early stopping triggered."
            )
            break

    best_checkpoint = torch.load(
        extended_checkpoint_path,
        map_location=device,
        weights_only=False,
    )

    model.load_state_dict(
        best_checkpoint["model_state_dict"]
    )

    final_validation = evaluate_validation(
        model,
        validation_loader,
        criterion,
        device,
    )

    validation_probabilities = (
        final_validation["probabilities"]
    )

    validation_labels = (
        final_validation["labels"]
    )

    if not np.array_equal(
        validation_labels,
        y_validation.astype(np.int8),
    ):
        raise RuntimeError(
            "Validation label ordering changed."
        )

    selected_threshold_metrics, (
        candidate_threshold_rows
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

    for row in candidate_threshold_rows:
        threshold_rows.append(
            {
                "candidate_id": candidate_id,
                **row,
            }
        )

    final_roc_auc = float(
        roc_auc_score(
            validation_labels,
            validation_probabilities,
        )
    )

    final_pr_auc = float(
        average_precision_score(
            validation_labels,
            validation_probabilities,
        )
    )

    candidate_history = [
        row
        for row in history_rows
        if row["candidate_id"] == candidate_id
    ]

    epochs_executed = int(
        candidate_history[-1]["epoch"]
    )

    peak_gpu_memory_mb = float(
        torch.cuda.max_memory_allocated()
        / (1024 ** 2)
    )

    runtime_seconds = float(
        time.perf_counter()
        - candidate_start
    )

    extended_record = {
        "candidate_id": candidate_id,
        "parameter_count": parameter_count,
        "original_best_epoch": start_epoch,
        "extended_best_epoch": int(
            best_checkpoint["epoch"]
        ),
        "final_epoch_executed": (
            epochs_executed
        ),
        "additional_epochs_executed": int(
            epochs_executed - start_epoch
        ),
        "best_validation_loss": float(
            best_checkpoint["validation_loss"]
        ),
        "roc_auc": final_roc_auc,
        "pr_auc": final_pr_auc,
        **selected_threshold_metrics,
        "peak_gpu_memory_mb": (
            peak_gpu_memory_mb
        ),
        "runtime_seconds": runtime_seconds,
        "checkpoint_path": str(
            extended_checkpoint_path
        ),
    }

    extended_metric_rows.append(
        extended_record
    )

    original_record = (
        original_metrics_by_candidate[
            candidate_id
        ]
    )

    comparison_rows.append(
        {
            "candidate_id": candidate_id,
            "original_best_epoch": int(
                original_record["best_epoch"]
            ),
            "extended_best_epoch": int(
                extended_record[
                    "extended_best_epoch"
                ]
            ),
            "original_threshold": float(
                original_record["threshold"]
            ),
            "extended_threshold": float(
                extended_record["threshold"]
            ),
            "original_f1": float(
                original_record["f1"]
            ),
            "extended_f1": float(
                extended_record["f1"]
            ),
            "f1_change": float(
                extended_record["f1"]
                - original_record["f1"]
            ),
            "original_f2": float(
                original_record["f2"]
            ),
            "extended_f2": float(
                extended_record["f2"]
            ),
            "f2_change": float(
                extended_record["f2"]
                - original_record["f2"]
            ),
            "original_pr_auc": float(
                original_record["pr_auc"]
            ),
            "extended_pr_auc": float(
                extended_record["pr_auc"]
            ),
            "pr_auc_change": float(
                extended_record["pr_auc"]
                - original_record["pr_auc"]
            ),
            "original_recall": float(
                original_record["recall"]
            ),
            "extended_recall": float(
                extended_record["recall"]
            ),
            "recall_change": float(
                extended_record["recall"]
                - original_record["recall"]
            ),
            "original_fnr": float(
                original_record["fnr"]
            ),
            "extended_fnr": float(
                extended_record["fnr"]
            ),
            "fnr_change": float(
                extended_record["fnr"]
                - original_record["fnr"]
            ),
        }
    )

    probability_archive[
        candidate_id
    ] = validation_probabilities.astype(
        np.float32
    )

    candidate_results.append(
        {
            "candidate_id": candidate_id,
            "architecture": candidate,
            "validation": extended_record,
        }
    )

    print("\nConvergence-adjusted result:")
    print(
        "  Extended best epoch:",
        extended_record["extended_best_epoch"],
    )
    print(
        "  Selected threshold:",
        extended_record["threshold"],
    )
    print(
        "  Validation F1:",
        extended_record["f1"],
    )
    print(
        "  Validation PR-AUC:",
        extended_record["pr_auc"],
    )
    print(
        "  Validation recall:",
        extended_record["recall"],
    )

    del model
    del optimizer
    del scheduler
    del checkpoint
    del best_checkpoint
    del training_loader
    del training_dataset

    torch.cuda.empty_cache()


# ------------------------------------------------------------
# Save outputs
# ------------------------------------------------------------

history_frame = pd.DataFrame(
    history_rows
)

extended_metrics_frame = (
    pd.DataFrame(
        extended_metric_rows
    )
    .sort_values(
        ["f1", "pr_auc"],
        ascending=False,
    )
    .reset_index(drop=True)
)

comparison_frame = pd.DataFrame(
    comparison_rows
)

threshold_frame = pd.DataFrame(
    threshold_rows
)

history_frame.to_csv(
    EXTENSION_HISTORY_PATH,
    index=False,
)

extended_metrics_frame.to_csv(
    EXTENDED_METRICS_PATH,
    index=False,
)

comparison_frame.to_csv(
    COMPARISON_PATH,
    index=False,
)

threshold_frame.to_csv(
    THRESHOLD_SWEEP_PATH,
    index=False,
)

np.savez_compressed(
    VALIDATION_PROBABILITIES_PATH,
    **probability_archive,
)


# ------------------------------------------------------------
# Convergence-adjusted provisional selection
# ------------------------------------------------------------

selected_candidate = sorted(
    extended_metric_rows,
    key=lambda row: (
        -row["f1"],
        -row["pr_auc"],
        -row["f2"],
        -row["recall"],
        row["fnr"],
        row["parameter_count"],
        row["candidate_id"],
    ),
)[0]

selection_record = {
    "stage": "15.3B",
    "selection_data": (
        "Duplicate-safe validation split only"
    ),
    "selected_candidate_id": (
        selected_candidate["candidate_id"]
    ),
    "selected_validation_metrics": (
        selected_candidate
    ),
    "selection_rule": (
        extension_configuration[
            "architecture_selection_rule"
        ]
    ),
    "status": (
        "Convergence-adjusted provisional winner. "
        "Multi-seed confirmation remains required."
    ),
    "holdout_status": "UNTOUCHED",
}

with open(
    SELECTION_PATH,
    "w",
    encoding="utf-8",
) as file:
    json.dump(
        selection_record,
        file,
        indent=2,
    )


# ------------------------------------------------------------
# Result and metadata
# ------------------------------------------------------------

runtime_seconds = float(
    time.perf_counter()
    - benchmark_start
)

result_record = {
    "stage": "15.3B",
    "generated_at_utc": datetime.now(
        timezone.utc
    ).isoformat(),
    "runtime_seconds": runtime_seconds,
    "runtime_minutes": float(
        runtime_seconds / 60.0
    ),
    "candidate_results": candidate_results,
    "selection": selection_record,
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
    "stage": "15.3B",
    "generated_at_utc": datetime.now(
        timezone.utc
    ).isoformat(),
    "purpose": (
        "Determine whether the Stage 15.3A ranking "
        "was affected by the 15-epoch training ceiling."
    ),
    "resume_policy": (
        "Resume each seed-42 best checkpoint and continue "
        "training to at most 30 total epochs."
    ),
    "selection_metric": (
        "Validation F1 at a validation-selected threshold"
    ),
    "early_stopping_metric": (
        "Validation PR-AUC"
    ),
    "holdout_indices_loaded": False,
    "holdout_features_loaded": False,
    "holdout_labels_loaded": False,
    "holdout_probabilities_generated": False,
    "holdout_metrics_generated": False,
    "next_step": (
        "Multi-seed confirmation of the "
        "convergence-adjusted candidate ranking."
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

print("\n" + "=" * 110)
print("STAGE 15.3B CONVERGENCE EXTENSION SUMMARY")
print("=" * 110)

print("\nRuntime:")
print(
    f"  {runtime_seconds / 60.0:.2f} minutes"
)

print("\nExtended validation comparison:")
print(
    extended_metrics_frame[
        [
            "candidate_id",
            "parameter_count",
            "original_best_epoch",
            "extended_best_epoch",
            "final_epoch_executed",
            "threshold",
            "accuracy",
            "precision",
            "recall",
            "f1",
            "f2",
            "fpr",
            "fnr",
            "roc_auc",
            "pr_auc",
        ]
    ].to_string(index=False)
)

print("\nOriginal-to-extended changes:")
print(
    comparison_frame[
        [
            "candidate_id",
            "f1_change",
            "f2_change",
            "pr_auc_change",
            "recall_change",
            "fnr_change",
        ]
    ].to_string(index=False)
)

print("\nConvergence-adjusted provisional winner:")
print(
    " ",
    selected_candidate["candidate_id"]
)

print(
    "  Best epoch:",
    selected_candidate["extended_best_epoch"],
)

print(
    "  Validation threshold:",
    selected_candidate["threshold"],
)

print(
    "  Validation F1:",
    selected_candidate["f1"],
)

print(
    "  Validation PR-AUC:",
    selected_candidate["pr_auc"],
)

print(
    "  Validation recall:",
    selected_candidate["recall"],
)

print("\nSelection status:")
print(
    "  PROVISIONAL — MULTI-SEED CONFIRMATION REQUIRED"
)

print("\nHoldout status:")
print("  UNTOUCHED")

print("\nSaved artifacts:")
print(EXTENSION_HISTORY_PATH)
print(EXTENDED_METRICS_PATH)
print(COMPARISON_PATH)
print(THRESHOLD_SWEEP_PATH)
print(VALIDATION_PROBABILITIES_PATH)
print(SELECTION_PATH)
print(RESULT_PATH)
print(METADATA_PATH)
print(EXTENDED_MODEL_DIR)

print("\nStage 15.3B complete.")
