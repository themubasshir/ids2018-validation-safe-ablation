
from __future__ import annotations

from pathlib import Path
from datetime import datetime, timezone
import importlib.util
import json
import math
import os
import random
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

MULTISEED_CONFIG_PATH = Path(
    os.environ["STAGE15_MULTISEED_CONFIG"]
)

RUN_DIRECTORY = Path(
    os.environ["STAGE15_RUN_DIRECTORY"]
)

MODEL_DIRECTORY = Path(
    os.environ["STAGE15_MODEL_DIRECTORY"]
)

TRAINING_HISTORY_PATH = Path(
    os.environ["STAGE15_TRAINING_HISTORY"]
)

SEED_METRICS_PATH = Path(
    os.environ["STAGE15_SEED_METRICS"]
)

CANDIDATE_SUMMARY_PATH = Path(
    os.environ["STAGE15_CANDIDATE_SUMMARY"]
)

SEED_WINNERS_PATH = Path(
    os.environ["STAGE15_SEED_WINNERS"]
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

def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)

    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


# ------------------------------------------------------------
# Read only training and validation rows
# ------------------------------------------------------------

def load_selected_rows(
    dataset_path: Path,
    feature_names: list[str],
    selected_indices: np.ndarray,
    chunk_size: int = 50_000,
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
            "Selected row indices must be sorted."
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


# ------------------------------------------------------------
# Metric helpers
# ------------------------------------------------------------

def binary_metrics(
    y_true: np.ndarray,
    probabilities: np.ndarray,
    threshold: float,
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
    y_true: np.ndarray,
    probabilities: np.ndarray,
    minimum: float,
    maximum: float,
    step: float,
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
    MULTISEED_CONFIG_PATH,
    "r",
    encoding="utf-8",
) as file:
    multiseed_configuration = json.load(file)

retained_features = list(
    feature_configuration["retained_features"]
)

candidates = list(
    candidate_configuration["candidates"]
)

confirmation_seeds = list(
    multiseed_configuration[
        "confirmation_seeds"
    ]
)

training_protocol = (
    multiseed_configuration[
        "training_protocol"
    ]
)

threshold_protocol = (
    multiseed_configuration[
        "threshold_protocol"
    ]
)

if len(retained_features) != 70:
    raise RuntimeError(
        "Expected 70 retained predictors."
    )

if 42 in confirmation_seeds:
    raise RuntimeError(
        "Seed 42 must not be reused in independent confirmation."
    )

if confirmation_seeds != [7, 29, 101]:
    raise RuntimeError(
        "Unexpected confirmation seed list."
    )


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
        "The current PyTorch build lacks sm_60."
    )


# ------------------------------------------------------------
# Load only train and validation indices
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

# holdout_indices is deliberately never accessed.

if len(train_indices) != 154_686:
    raise RuntimeError(
        "Unexpected duplicate-safe training size."
    )

if len(validation_indices) != 37_835:
    raise RuntimeError(
        "Unexpected duplicate-safe validation size."
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
# Apply archived training-only scaler
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
# Training-only class weight
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
# Shared validation loader
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

batch_size = int(
    training_protocol["batch_size"]
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
# Import FT-Transformer
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
# Output directories
# ------------------------------------------------------------

RUN_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True,
)

MODEL_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True,
)


# ------------------------------------------------------------
# Execute independent candidate × seed runs
# ------------------------------------------------------------

all_run_results = []

experiment_start = time.perf_counter()

total_runs = (
    len(candidates)
    * len(confirmation_seeds)
)

run_counter = 0

for candidate in candidates:
    candidate_id = candidate["candidate_id"]

    for seed in confirmation_seeds:
        run_counter += 1

        run_id = (
            f"{candidate_id}_seed_{seed}"
        )

        print("\n" + "=" * 104)
        print(
            f"RUN {run_counter}/{total_runs}: {run_id}"
        )
        print("=" * 104)

        run_result_path = (
            RUN_DIRECTORY
            / f"{run_id}_result.json"
        )

        run_history_path = (
            RUN_DIRECTORY
            / f"{run_id}_history.csv"
        )

        run_threshold_path = (
            RUN_DIRECTORY
            / f"{run_id}_thresholds.csv"
        )

        run_probability_path = (
            RUN_DIRECTORY
            / f"{run_id}_validation_probabilities.npz"
        )

        best_checkpoint_path = (
            MODEL_DIRECTORY
            / f"{run_id}_best.pt"
        )

        last_checkpoint_path = (
            MODEL_DIRECTORY
            / f"{run_id}_last.pt"
        )

        required_completed_run_files = [
            run_result_path,
            run_history_path,
            run_threshold_path,
            run_probability_path,
            best_checkpoint_path,
        ]

        if all(
            path.exists()
            for path in required_completed_run_files
        ):
            with open(
                run_result_path,
                "r",
                encoding="utf-8",
            ) as file:
                existing_result = json.load(file)

            if (
                existing_result.get("status")
                == "COMPLETED"
                and existing_result.get(
                    "holdout_status"
                )
                == "UNTOUCHED"
            ):
                all_run_results.append(
                    existing_result
                )

                print(
                    "Completed run found; skipping retraining."
                )
                print(
                    "  Best epoch:",
                    existing_result["best_epoch"],
                )
                print(
                    "  Validation F1:",
                    existing_result["f1"],
                )
                print(
                    "  Validation PR-AUC:",
                    existing_result["pr_auc"],
                )

                continue

        set_seed(seed)

        loader_generator = torch.Generator()
        loader_generator.manual_seed(seed)

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
            batch_size=batch_size,
            shuffle=True,
            generator=loader_generator,
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

        scheduler = (
            torch.optim.lr_scheduler
            .ReduceLROnPlateau(
                optimizer,
                mode="max",
                factor=float(
                    training_protocol[
                        "scheduler"
                    ]["factor"]
                ),
                patience=int(
                    training_protocol[
                        "scheduler"
                    ]["patience"]
                ),
                min_lr=float(
                    training_protocol[
                        "scheduler"
                    ]["minimum_learning_rate"]
                ),
            )
        )

        start_epoch = 1
        best_epoch = None
        best_pr_auc = -math.inf
        best_validation_loss = math.inf
        epochs_without_improvement = 0
        history_rows = []

        if last_checkpoint_path.exists():
            print(
                "Incomplete run checkpoint found; resuming."
            )

            last_checkpoint = torch.load(
                last_checkpoint_path,
                map_location=device,
                weights_only=False,
            )

            model.load_state_dict(
                last_checkpoint[
                    "model_state_dict"
                ]
            )

            optimizer.load_state_dict(
                last_checkpoint[
                    "optimizer_state_dict"
                ]
            )

            scheduler.load_state_dict(
                last_checkpoint[
                    "scheduler_state_dict"
                ]
            )

            start_epoch = int(
                last_checkpoint["epoch"]
            ) + 1

            best_epoch = (
                int(last_checkpoint["best_epoch"])
                if last_checkpoint["best_epoch"]
                is not None
                else None
            )

            best_pr_auc = float(
                last_checkpoint["best_pr_auc"]
            )

            best_validation_loss = float(
                last_checkpoint[
                    "best_validation_loss"
                ]
            )

            epochs_without_improvement = int(
                last_checkpoint[
                    "epochs_without_improvement"
                ]
            )

            loader_generator.set_state(
                last_checkpoint[
                    "loader_generator_state"
                ]
            )

            if run_history_path.exists():
                history_rows = (
                    pd.read_csv(
                        run_history_path
                    )
                    .to_dict(
                        orient="records"
                    )
                )

            print(
                "  Resuming from epoch:",
                start_epoch,
            )

        maximum_epochs = int(
            training_protocol[
                "maximum_epochs"
            ]
        )

        patience = int(
            training_protocol[
                "early_stopping_patience"
            ]
        )

        gradient_clip_norm = float(
            training_protocol[
                "gradient_clip_norm"
            ]
        )

        improvement_tolerance = float(
            training_protocol[
                "checkpoint_improvement_tolerance"
            ]
        )

        run_start = time.perf_counter()

        final_epoch_executed = (
            start_epoch - 1
        )

        for epoch in range(
            start_epoch,
            maximum_epochs + 1,
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
                        f"{run_id} produced "
                        "a non-finite loss."
                    )

                loss.backward()

                gradient_norm = (
                    torch.nn.utils
                    .clip_grad_norm_(
                        model.parameters(),
                        max_norm=gradient_clip_norm,
                    )
                )

                if not torch.isfinite(
                    gradient_norm
                ):
                    raise FloatingPointError(
                        f"{run_id} produced "
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

                total_training_rows += (
                    batch_rows
                )

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
                best_validation_loss = (
                    validation_loss
                )
                epochs_without_improvement = 0

                torch.save(
                    {
                        "run_id": run_id,
                        "candidate_id": candidate_id,
                        "seed": int(seed),
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
                    },
                    best_checkpoint_path,
                )

            else:
                epochs_without_improvement += 1

            epoch_seconds = float(
                time.perf_counter()
                - epoch_start
            )

            history_rows.append(
                {
                    "run_id": run_id,
                    "candidate_id": candidate_id,
                    "seed": int(seed),
                    "epoch": int(epoch),
                    "training_loss": training_loss,
                    "validation_loss": (
                        validation_loss
                    ),
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
                    "epochs_without_improvement": (
                        epochs_without_improvement
                    ),
                    "epoch_seconds": epoch_seconds,
                }
            )

            pd.DataFrame(
                history_rows
            ).to_csv(
                run_history_path,
                index=False,
            )

            torch.save(
                {
                    "run_id": run_id,
                    "candidate_id": candidate_id,
                    "seed": int(seed),
                    "architecture": candidate,
                    "epoch": int(epoch),
                    "best_epoch": best_epoch,
                    "best_pr_auc": best_pr_auc,
                    "best_validation_loss": (
                        best_validation_loss
                    ),
                    "epochs_without_improvement": (
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
                },
                last_checkpoint_path,
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
                print(
                    "Early stopping triggered."
                )
                break

        if best_epoch is None:
            raise RuntimeError(
                f"No best checkpoint was created for {run_id}."
            )

        best_checkpoint = torch.load(
            best_checkpoint_path,
            map_location=device,
            weights_only=False,
        )

        model.load_state_dict(
            best_checkpoint[
                "model_state_dict"
            ]
        )

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
                threshold_protocol["minimum"]
            ),
            maximum=float(
                threshold_protocol["maximum"]
            ),
            step=float(
                threshold_protocol["step"]
            ),
        )

        threshold_frame = pd.DataFrame(
            [
                {
                    "run_id": run_id,
                    "candidate_id": candidate_id,
                    "seed": int(seed),
                    **row,
                }
                for row in threshold_rows
            ]
        )

        threshold_frame.to_csv(
            run_threshold_path,
            index=False,
        )

        np.savez_compressed(
            run_probability_path,
            y_true=validation_labels,
            probabilities=(
                validation_probabilities.astype(
                    np.float32
                )
            ),
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

        runtime_seconds = float(
            time.perf_counter()
            - run_start
        )

        peak_gpu_memory_mb = float(
            torch.cuda.max_memory_allocated()
            / (1024 ** 2)
        )

        run_result = {
            "stage": "15.4A",
            "status": "COMPLETED",
            "run_id": run_id,
            "candidate_id": candidate_id,
            "seed": int(seed),
            "architecture": candidate,
            "parameter_count": parameter_count,
            "best_epoch": int(best_epoch),
            "final_epoch_executed": int(
                final_epoch_executed
            ),
            "epoch_ceiling_reached": bool(
                final_epoch_executed
                == maximum_epochs
            ),
            "best_checkpoint_at_epoch_ceiling": bool(
                best_epoch == maximum_epochs
            ),
            "best_validation_loss": float(
                best_validation_loss
            ),
            "roc_auc": final_roc_auc,
            "pr_auc": final_pr_auc,
            **selected_threshold_metrics,
            "peak_gpu_memory_mb": (
                peak_gpu_memory_mb
            ),
            "runtime_seconds": runtime_seconds,
            "best_checkpoint_path": str(
                best_checkpoint_path
            ),
            "last_checkpoint_path": str(
                last_checkpoint_path
            ),
            "validation_probability_path": str(
                run_probability_path
            ),
            "holdout_status": "UNTOUCHED",
        }

        with open(
            run_result_path,
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                run_result,
                file,
                indent=2,
            )

        all_run_results.append(
            run_result
        )

        print("\nCompleted run result:")
        print(
            "  Best epoch:",
            run_result["best_epoch"],
        )
        print(
            "  Threshold:",
            run_result["threshold"],
        )
        print(
            "  Validation F1:",
            run_result["f1"],
        )
        print(
            "  Validation PR-AUC:",
            run_result["pr_auc"],
        )
        print(
            "  Validation recall:",
            run_result["recall"],
        )
        print(
            "  Peak GPU memory:",
            f"{peak_gpu_memory_mb:.2f} MB",
        )

        del model
        del optimizer
        del scheduler
        del best_checkpoint
        del training_loader
        del training_dataset

        torch.cuda.empty_cache()


# ------------------------------------------------------------
# Verify run completeness
# ------------------------------------------------------------

if len(all_run_results) != total_runs:
    raise RuntimeError(
        "Expected "
        f"{total_runs} completed runs, found "
        f"{len(all_run_results)}."
    )

run_ids = [
    result["run_id"]
    for result in all_run_results
]

if len(set(run_ids)) != total_runs:
    raise RuntimeError(
        "Duplicate run identifiers detected."
    )

if any(
    result["holdout_status"] != "UNTOUCHED"
    for result in all_run_results
):
    raise RuntimeError(
        "Unexpected holdout status."
    )


# ------------------------------------------------------------
# Combine per-run histories and threshold sweeps
# ------------------------------------------------------------

history_frames = []

threshold_frames = []

for result in all_run_results:
    run_id = result["run_id"]

    history_frames.append(
        pd.read_csv(
            RUN_DIRECTORY
            / f"{run_id}_history.csv"
        )
    )

    threshold_frames.append(
        pd.read_csv(
            RUN_DIRECTORY
            / f"{run_id}_thresholds.csv"
        )
    )

combined_history = pd.concat(
    history_frames,
    ignore_index=True,
)

combined_thresholds = pd.concat(
    threshold_frames,
    ignore_index=True,
)

combined_history.to_csv(
    TRAINING_HISTORY_PATH,
    index=False,
)

combined_thresholds.to_csv(
    THRESHOLD_SWEEP_PATH,
    index=False,
)


# ------------------------------------------------------------
# Seed-level metrics
# ------------------------------------------------------------

seed_metrics_frame = (
    pd.DataFrame(all_run_results)
    [
        [
            "run_id",
            "candidate_id",
            "seed",
            "parameter_count",
            "best_epoch",
            "final_epoch_executed",
            "epoch_ceiling_reached",
            "best_checkpoint_at_epoch_ceiling",
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
            "true_negative",
            "false_positive",
            "false_negative",
            "true_positive",
            "peak_gpu_memory_mb",
            "runtime_seconds",
        ]
    ]
    .sort_values(
        [
            "seed",
            "candidate_id",
        ]
    )
    .reset_index(drop=True)
)

seed_metrics_frame.to_csv(
    SEED_METRICS_PATH,
    index=False,
)


# ------------------------------------------------------------
# Determine winner within each confirmation seed
# ------------------------------------------------------------

seed_winner_rows = []

seed_win_counts = {
    candidate["candidate_id"]: 0
    for candidate in candidates
}

for seed in confirmation_seeds:
    seed_records = [
        result
        for result in all_run_results
        if result["seed"] == seed
    ]

    seed_winner = sorted(
        seed_records,
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

    seed_win_counts[
        seed_winner["candidate_id"]
    ] += 1

    seed_winner_rows.append(
        {
            "seed": int(seed),
            "winning_candidate_id": (
                seed_winner["candidate_id"]
            ),
            "winning_f1": float(
                seed_winner["f1"]
            ),
            "winning_pr_auc": float(
                seed_winner["pr_auc"]
            ),
            "winning_recall": float(
                seed_winner["recall"]
            ),
            "winning_threshold": float(
                seed_winner["threshold"]
            ),
        }
    )

seed_winners_frame = pd.DataFrame(
    seed_winner_rows
)

seed_winners_frame.to_csv(
    SEED_WINNERS_PATH,
    index=False,
)


# ------------------------------------------------------------
# Aggregate candidate stability
# ------------------------------------------------------------

candidate_summary_rows = []

for candidate in candidates:
    candidate_id = candidate["candidate_id"]

    group = seed_metrics_frame[
        seed_metrics_frame[
            "candidate_id"
        ]
        == candidate_id
    ]

    if len(group) != len(
        confirmation_seeds
    ):
        raise RuntimeError(
            f"Incomplete seed results for {candidate_id}."
        )

    candidate_summary_rows.append(
        {
            "candidate_id": candidate_id,
            "parameter_count": int(
                group["parameter_count"].iloc[0]
            ),
            "seed_count": int(len(group)),
            "seed_win_count": int(
                seed_win_counts[candidate_id]
            ),
            "mean_best_epoch": float(
                group["best_epoch"].mean()
            ),
            "maximum_best_epoch": int(
                group["best_epoch"].max()
            ),
            "best_checkpoint_ceiling_hits": int(
                group[
                    "best_checkpoint_at_epoch_ceiling"
                ].sum()
            ),
            "mean_threshold": float(
                group["threshold"].mean()
            ),
            "threshold_std": float(
                group["threshold"].std(ddof=1)
            ),
            "mean_accuracy": float(
                group["accuracy"].mean()
            ),
            "accuracy_std": float(
                group["accuracy"].std(ddof=1)
            ),
            "mean_precision": float(
                group["precision"].mean()
            ),
            "precision_std": float(
                group["precision"].std(ddof=1)
            ),
            "mean_recall": float(
                group["recall"].mean()
            ),
            "recall_std": float(
                group["recall"].std(ddof=1)
            ),
            "mean_f1": float(
                group["f1"].mean()
            ),
            "f1_std": float(
                group["f1"].std(ddof=1)
            ),
            "minimum_f1": float(
                group["f1"].min()
            ),
            "maximum_f1": float(
                group["f1"].max()
            ),
            "mean_f2": float(
                group["f2"].mean()
            ),
            "f2_std": float(
                group["f2"].std(ddof=1)
            ),
            "mean_fpr": float(
                group["fpr"].mean()
            ),
            "fpr_std": float(
                group["fpr"].std(ddof=1)
            ),
            "mean_fnr": float(
                group["fnr"].mean()
            ),
            "fnr_std": float(
                group["fnr"].std(ddof=1)
            ),
            "mean_roc_auc": float(
                group["roc_auc"].mean()
            ),
            "roc_auc_std": float(
                group["roc_auc"].std(ddof=1)
            ),
            "mean_pr_auc": float(
                group["pr_auc"].mean()
            ),
            "pr_auc_std": float(
                group["pr_auc"].std(ddof=1)
            ),
            "mean_peak_gpu_memory_mb": float(
                group[
                    "peak_gpu_memory_mb"
                ].mean()
            ),
            "total_runtime_seconds": float(
                group["runtime_seconds"].sum()
            ),
        }
    )

candidate_summary_frame = pd.DataFrame(
    candidate_summary_rows
)


# ------------------------------------------------------------
# Aggregate architecture ranking
# ------------------------------------------------------------

candidate_summary_frame = (
    candidate_summary_frame
    .sort_values(
        by=[
            "mean_f1",
            "mean_pr_auc",
            "minimum_f1",
            "f1_std",
            "mean_f2",
            "mean_recall",
            "parameter_count",
            "candidate_id",
        ],
        ascending=[
            False,
            False,
            False,
            True,
            False,
            False,
            True,
            True,
        ],
    )
    .reset_index(drop=True)
)

candidate_summary_frame.insert(
    0,
    "aggregate_rank",
    np.arange(
        1,
        len(candidate_summary_frame) + 1,
    ),
)

candidate_summary_frame.to_csv(
    CANDIDATE_SUMMARY_PATH,
    index=False,
)

leader = (
    candidate_summary_frame.iloc[0]
    .to_dict()
)

runner_up = (
    candidate_summary_frame.iloc[1]
    .to_dict()
)

mean_f1_margin = float(
    leader["mean_f1"]
    - runner_up["mean_f1"]
)

minimum_required_margin = float(
    multiseed_configuration[
        "phase_1_clear_lead_rule"
    ]["minimum_mean_f1_margin"]
)

minimum_required_seed_wins = int(
    multiseed_configuration[
        "phase_1_clear_lead_rule"
    ]["minimum_seed_wins"]
)

leader_clear_margin = bool(
    mean_f1_margin
    >= minimum_required_margin
)

leader_seed_win_requirement = bool(
    int(leader["seed_win_count"])
    >= minimum_required_seed_wins
)

leader_convergence_requirement = bool(
    int(
        leader[
            "best_checkpoint_ceiling_hits"
        ]
    )
    == 0
)

phase_1_clear_lead = bool(
    leader_clear_margin
    and leader_seed_win_requirement
    and leader_convergence_requirement
)

if phase_1_clear_lead:
    confirmation_status = (
        "CLEAR_PROVISIONAL_MULTI_SEED_LEAD"
    )

    recommended_next_step = (
        "Run two additional independent confirmation "
        "seeds for the leading architecture and closest "
        "runner-up, then freeze architecture and threshold."
    )

else:
    confirmation_status = (
        "CLOSE_OR_UNSTABLE_MULTI_SEED_RANKING"
    )

    recommended_next_step = (
        "Expand confirmation with two additional seeds "
        "before architecture freezing."
    )


# ------------------------------------------------------------
# Consolidate validation probabilities
# ------------------------------------------------------------

probability_archive = {
    "y_true": y_validation.astype(
        np.int8,
        copy=False,
    )
}

for result in all_run_results:
    run_probability_archive = np.load(
        result[
            "validation_probability_path"
        ],
        allow_pickle=False,
    )

    run_labels = np.asarray(
        run_probability_archive["y_true"],
        dtype=np.int8,
    )

    if not np.array_equal(
        run_labels,
        y_validation.astype(np.int8),
    ):
        raise RuntimeError(
            "Stored validation labels are inconsistent."
        )

    probability_archive[
        result["run_id"]
    ] = np.asarray(
        run_probability_archive[
            "probabilities"
        ],
        dtype=np.float32,
    )

np.savez_compressed(
    VALIDATION_PROBABILITIES_PATH,
    **probability_archive,
)


# ------------------------------------------------------------
# Save selection and result records
# ------------------------------------------------------------

selection_record = {
    "stage": "15.4A",
    "selection_scope": (
        "Independent seeds 7, 29, and 101 using "
        "duplicate-safe training and validation only"
    ),
    "screening_seed_excluded": 42,
    "aggregate_selection_rule": (
        multiseed_configuration[
            "aggregate_selection_rule"
        ]
    ),
    "provisional_multiseed_leader": (
        leader["candidate_id"]
    ),
    "runner_up": (
        runner_up["candidate_id"]
    ),
    "leader_summary": leader,
    "runner_up_summary": runner_up,
    "mean_f1_margin": mean_f1_margin,
    "phase_1_requirements": {
        "mean_f1_margin_passed": (
            leader_clear_margin
        ),
        "seed_win_requirement_passed": (
            leader_seed_win_requirement
        ),
        "convergence_requirement_passed": (
            leader_convergence_requirement
        ),
    },
    "confirmation_status": (
        confirmation_status
    ),
    "architecture_frozen": False,
    "recommended_next_step": (
        recommended_next_step
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

experiment_runtime_seconds = float(
    time.perf_counter()
    - experiment_start
)

result_record = {
    "stage": "15.4A",
    "generated_at_utc": datetime.now(
        timezone.utc
    ).isoformat(),
    "confirmation_seeds": confirmation_seeds,
    "candidate_count": int(
        len(candidates)
    ),
    "completed_run_count": int(
        len(all_run_results)
    ),
    "expected_run_count": int(
        total_runs
    ),
    "runtime_seconds": (
        experiment_runtime_seconds
    ),
    "runtime_minutes": float(
        experiment_runtime_seconds / 60.0
    ),
    "seed_level_results": (
        all_run_results
    ),
    "candidate_summary": (
        candidate_summary_frame
        .to_dict(orient="records")
    ),
    "seed_winners": (
        seed_winner_rows
    ),
    "selection": selection_record,
    "GPU": {
        "device": device_name,
        "capability": device_capability,
        "torch_version": torch.__version__,
        "CUDA_runtime": torch.version.cuda,
        "compiled_architectures": (
            compiled_architectures
        ),
    },
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
    "stage": "15.4A",
    "generated_at_utc": datetime.now(
        timezone.utc
    ).isoformat(),
    "scientific_purpose": (
        "Measure architecture robustness to independent "
        "model initialization and training-order seeds."
    ),
    "screening_seed_excluded": 42,
    "confirmation_seeds": confirmation_seeds,
    "from_scratch_training": True,
    "resume_safe": True,
    "resume_artifacts": [
        "per-run last checkpoint",
        "per-run best checkpoint",
        "per-run epoch history",
        "per-run threshold sweep",
        "per-run validation probabilities",
        "per-run final result",
    ],
    "preprocessing": (
        "Archived StandardScaler fit on duplicate-safe "
        "training rows only"
    ),
    "early_stopping_data": (
        "Duplicate-safe validation only"
    ),
    "threshold_selection_data": (
        "Duplicate-safe validation only"
    ),
    "holdout_indices_loaded": False,
    "holdout_features_loaded": False,
    "holdout_labels_loaded": False,
    "holdout_probabilities_generated": False,
    "holdout_metrics_generated": False,
    "architecture_frozen": False,
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
print("STAGE 15.4A MULTI-SEED CONFIRMATION SUMMARY")
print("=" * 112)

print("\nRuntime:")
print(
    f"  {experiment_runtime_seconds / 60.0:.2f} minutes"
)

print("\nCompleted independent runs:")
print(
    f"  {len(all_run_results)} / {total_runs}"
)

print("\nSeed-level validation results:")
print(
    seed_metrics_frame[
        [
            "candidate_id",
            "seed",
            "best_epoch",
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

print("\nCandidate multi-seed summary:")
print(
    candidate_summary_frame[
        [
            "aggregate_rank",
            "candidate_id",
            "parameter_count",
            "seed_win_count",
            "mean_f1",
            "f1_std",
            "minimum_f1",
            "mean_f2",
            "mean_recall",
            "mean_pr_auc",
            "pr_auc_std",
            "best_checkpoint_ceiling_hits",
        ]
    ].to_string(index=False)
)

print("\nSeed winners:")
print(
    seed_winners_frame.to_string(
        index=False
    )
)

print("\nProvisional multi-seed leader:")
print(
    " ",
    selection_record[
        "provisional_multiseed_leader"
    ],
)

print(
    "  Runner-up:",
    selection_record["runner_up"],
)

print(
    "  Mean F1 margin:",
    selection_record["mean_f1_margin"],
)

print(
    "  Mean F1:",
    leader["mean_f1"],
)

print(
    "  F1 standard deviation:",
    leader["f1_std"],
)

print(
    "  Worst-seed F1:",
    leader["minimum_f1"],
)

print(
    "  Mean PR-AUC:",
    leader["mean_pr_auc"],
)

print(
    "  Seed wins:",
    int(leader["seed_win_count"]),
)

print("\nConfirmation status:")
print(
    " ",
    confirmation_status
)

print("\nArchitecture frozen:")
print("  FALSE")

print("\nHoldout status:")
print("  UNTOUCHED")

print("\nRecommended next step:")
print(
    " ",
    recommended_next_step
)

print("\nSaved artifacts:")
print(TRAINING_HISTORY_PATH)
print(SEED_METRICS_PATH)
print(CANDIDATE_SUMMARY_PATH)
print(SEED_WINNERS_PATH)
print(THRESHOLD_SWEEP_PATH)
print(VALIDATION_PROBABILITIES_PATH)
print(SELECTION_PATH)
print(RESULT_PATH)
print(METADATA_PATH)
print(RUN_DIRECTORY)
print(MODEL_DIRECTORY)

print("\nStage 15.4A complete.")
