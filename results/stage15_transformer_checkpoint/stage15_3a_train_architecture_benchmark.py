
from __future__ import annotations

from pathlib import Path
from datetime import datetime, timezone
import importlib.util
import json
import math
import os
import random
import time
import warnings

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


warnings.filterwarnings(
    "ignore",
    category=UserWarning,
)


# ------------------------------------------------------------
# Configuration from environment
# ------------------------------------------------------------

DATASET_PATH = Path(
    os.environ["STAGE15_DATASET_PATH"]
)

STAGE15_DIR = Path(
    os.environ["STAGE15_DIR"]
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

RESULT_PATH = Path(
    os.environ["STAGE15_RESULT"]
)

TRAINING_HISTORY_PATH = Path(
    os.environ["STAGE15_TRAINING_HISTORY"]
)

VALIDATION_METRICS_PATH = Path(
    os.environ["STAGE15_VALIDATION_METRICS"]
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

METADATA_PATH = Path(
    os.environ["STAGE15_METADATA"]
)

MODEL_DIR = Path(
    os.environ["STAGE15_MODEL_DIR"]
)


# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------

def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)

    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


def load_selected_rows(
    dataset_path: Path,
    feature_names: list[str],
    target_indices: np.ndarray,
    chunk_size: int = 50_000,
):
    """
    Read only the selected training/validation rows.

    Holdout rows are never retained in memory.
    """

    target_indices = np.asarray(
        target_indices,
        dtype=np.int64,
    )

    if not np.all(
        target_indices[:-1]
        <= target_indices[1:]
    ):
        raise ValueError(
            "target_indices must be sorted."
        )

    row_count = len(
        target_indices
    )

    X_selected = np.empty(
        (
            row_count,
            len(feature_names),
        ),
        dtype=np.float64,
    )

    y_selected = np.empty(
        row_count,
        dtype=np.float32,
    )

    filled = np.zeros(
        row_count,
        dtype=bool,
    )

    global_start = 0

    reader = pd.read_csv(
        dataset_path,
        usecols=(
            feature_names
            + ["binary_label"]
        ),
        chunksize=chunk_size,
    )

    for chunk in reader:
        global_end = (
            global_start
            + len(chunk)
        )

        left = np.searchsorted(
            target_indices,
            global_start,
            side="left",
        )

        right = np.searchsorted(
            target_indices,
            global_end,
            side="left",
        )

        if right > left:
            selected_global = (
                target_indices[
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

        global_start = global_end

    if not filled.all():
        missing_count = int(
            np.sum(
                ~filled
            )
        )

        raise RuntimeError(
            f"Failed to load {missing_count} selected rows."
        )

    return X_selected, y_selected


def binary_metrics(
    y_true: np.ndarray,
    probabilities: np.ndarray,
    threshold: float,
):
    predictions = (
        probabilities
        >= threshold
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
        2.0
        * precision
        * recall
        /
        (
            precision
            + recall
        )
        if (
            precision
            + recall
        )
        > 0
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
        /
        (
            beta_squared
            * precision
            + recall
        )
        if (
            beta_squared
            * precision
            + recall
        )
        > 0
        else 0.0
    )

    fpr = (
        fp
        /
        (
            fp
            + tn
        )
        if (
            fp
            + tn
        )
        > 0
        else 0.0
    )

    fnr = (
        fn
        /
        (
            fn
            + tp
        )
        if (
            fn
            + tp
        )
        > 0
        else 0.0
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
        "precision": float(
            precision
        ),
        "recall": float(
            recall
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
    }


def select_threshold(
    y_true: np.ndarray,
    probabilities: np.ndarray,
    threshold_minimum: float,
    threshold_maximum: float,
    threshold_step: float,
):
    thresholds = np.arange(
        threshold_minimum,
        threshold_maximum
        + threshold_step / 2.0,
        threshold_step,
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
def predict_probabilities(
    model,
    loader,
    device,
):
    model.eval()

    probability_batches = []
    label_batches = []

    for features, labels in loader:
        features = features.to(
            device,
            non_blocking=True,
        )

        logits = model(
            features
        )

        probabilities = torch.sigmoid(
            logits
        )

        probability_batches.append(
            probabilities
            .detach()
            .cpu()
            .numpy()
        )

        label_batches.append(
            labels.numpy()
        )

    return (
        np.concatenate(
            probability_batches
        ).astype(
            np.float64
        ),
        np.concatenate(
            label_batches
        ).astype(
            np.int8
        ),
    )


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

            logits = model(
                features
            )

            loss = criterion(
                logits,
                labels_device,
            )

            batch_rows = int(
                labels.shape[0]
            )

            total_loss += float(
                loss.item()
            ) * batch_rows

            total_rows += batch_rows

            probability_batches.append(
                torch.sigmoid(
                    logits
                )
                .detach()
                .cpu()
                .numpy()
            )

            label_batches.append(
                labels.numpy()
            )

    probabilities = np.concatenate(
        probability_batches
    ).astype(
        np.float64
    )

    labels = np.concatenate(
        label_batches
    ).astype(
        np.int8
    )

    return {
        "loss": float(
            total_loss
            /
            total_rows
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
    benchmark_configuration = json.load(file)

retained_features = list(
    feature_configuration[
        "retained_features"
    ]
)

if len(retained_features) != 70:
    raise RuntimeError(
        "Expected 70 retained features."
    )

protocol = benchmark_configuration[
    "training_protocol"
]

candidates = benchmark_configuration[
    "candidates"
]

seed = int(
    benchmark_configuration[
        "seed"
    ]
)

set_seed(seed)


# ------------------------------------------------------------
# Validate CUDA environment
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
        "Expected P100 capability [6, 0], found "
        f"{device_capability}."
    )

if "sm_60" not in compiled_architectures:
    raise RuntimeError(
        "Installed PyTorch does not include sm_60."
    )


# ------------------------------------------------------------
# Load only train and validation indices
# ------------------------------------------------------------

split_archive = np.load(
    SAFE_SPLIT_PATH,
    allow_pickle=False,
)

train_indices = np.asarray(
    split_archive[
        "train_indices"
    ],
    dtype=np.int64,
)

validation_indices = np.asarray(
    split_archive[
        "validation_indices"
    ],
    dtype=np.int64,
)

# The holdout_indices entry is intentionally not read.

if len(train_indices) != 154_686:
    raise RuntimeError(
        "Unexpected training-row count."
    )

if len(validation_indices) != 37_835:
    raise RuntimeError(
        "Unexpected validation-row count."
    )


# ------------------------------------------------------------
# Read only selected training and validation rows
# ------------------------------------------------------------

combined_selected_indices = np.sort(
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
        combined_selected_indices,
    )
)

train_positions = np.searchsorted(
    combined_selected_indices,
    train_indices,
)

validation_positions = np.searchsorted(
    combined_selected_indices,
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

if int(
    scaler.n_features_in_
) != 70:
    raise RuntimeError(
        "Scaler feature count is not 70."
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

if not np.isfinite(
    X_train
).all():
    raise RuntimeError(
        "Training matrix contains non-finite values."
    )

if not np.isfinite(
    X_validation
).all():
    raise RuntimeError(
        "Validation matrix contains non-finite values."
    )


# ------------------------------------------------------------
# Class weight from training labels only
# ------------------------------------------------------------

training_benign_count = int(
    np.sum(
        y_train == 0
    )
)

training_attack_count = int(
    np.sum(
        y_train == 1
    )
)

positive_class_weight = float(
    training_benign_count
    /
    training_attack_count
)

if training_benign_count != 110_161:
    raise RuntimeError(
        "Unexpected training benign count."
    )

if training_attack_count != 44_525:
    raise RuntimeError(
        "Unexpected training attack count."
    )


# ------------------------------------------------------------
# Data loaders
# ------------------------------------------------------------

X_train_tensor = torch.from_numpy(
    X_train
)

y_train_tensor = torch.from_numpy(
    y_train.astype(
        np.float32,
        copy=False,
    )
)

X_validation_tensor = torch.from_numpy(
    X_validation
)

y_validation_tensor = torch.from_numpy(
    y_validation.astype(
        np.float32,
        copy=False,
    )
)

training_dataset = TensorDataset(
    X_train_tensor,
    y_train_tensor,
)

validation_dataset = TensorDataset(
    X_validation_tensor,
    y_validation_tensor,
)

loader_generator = torch.Generator()
loader_generator.manual_seed(seed)

batch_size = int(
    protocol[
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
# Import model module
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
        "Unable to load FT-Transformer module."
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
# Benchmark candidates
# ------------------------------------------------------------

MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

history_rows = []
validation_metric_rows = []
threshold_rows = []

validation_probability_archive = {
    "y_true": y_validation.astype(
        np.int8,
        copy=False,
    )
}

candidate_results = []

benchmark_start_time = time.perf_counter()

maximum_epochs = int(
    protocol[
        "maximum_epochs"
    ]
)

early_stopping_patience = int(
    protocol[
        "early_stopping_patience"
    ]
)

gradient_clip_norm = float(
    protocol[
        "gradient_clip_norm"
    ]
)

for candidate_number, candidate in enumerate(
    candidates,
    start=1,
):
    candidate_id = candidate[
        "candidate_id"
    ]

    print("\n" + "=" * 100)
    print(
        f"CANDIDATE {candidate_number}/{len(candidates)}: "
        f"{candidate_id}"
    )
    print("=" * 100)

    set_seed(seed)

    torch.cuda.empty_cache()
    torch.cuda.reset_peak_memory_stats()

    model = NumericFTTransformer(
        n_features=70,
        d_token=int(
            candidate[
                "d_token"
            ]
        ),
        n_heads=int(
            candidate[
                "n_heads"
            ]
        ),
        n_layers=int(
            candidate[
                "n_layers"
            ]
        ),
        d_ff=int(
            candidate[
                "d_ff"
            ]
        ),
        dropout=float(
            candidate[
                "dropout"
            ]
        ),
    ).to(device)

    parameter_count = int(
        sum(
            parameter.numel()
            for parameter
            in model.parameters()
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
        lr=float(
            candidate[
                "learning_rate"
            ]
        ),
        weight_decay=float(
            candidate[
                "weight_decay"
            ]
        ),
    )

    scheduler = (
        torch.optim.lr_scheduler
        .ReduceLROnPlateau(
            optimizer,
            mode="max",
            factor=float(
                protocol[
                    "scheduler_factor"
                ]
            ),
            patience=int(
                protocol[
                    "scheduler_patience"
                ]
            ),
            min_lr=float(
                protocol[
                    "minimum_learning_rate"
                ]
            ),
        )
    )

    checkpoint_path = (
        MODEL_DIR
        / f"{candidate_id}_best.pt"
    )

    best_pr_auc = -math.inf
    best_validation_loss = math.inf
    best_epoch = None
    epochs_without_improvement = 0

    candidate_start_time = (
        time.perf_counter()
    )

    for epoch in range(
        1,
        maximum_epochs + 1,
    ):
        epoch_start_time = (
            time.perf_counter()
        )

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

            logits = model(
                features
            )

            loss = criterion(
                logits,
                labels,
            )

            if not torch.isfinite(
                loss
            ):
                raise FloatingPointError(
                    f"{candidate_id} produced "
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
                    f"{candidate_id} produced "
                    "non-finite gradients."
                )

            optimizer.step()

            batch_rows = int(
                labels.shape[0]
            )

            total_training_loss += (
                float(
                    loss.item()
                )
                * batch_rows
            )

            total_training_rows += (
                batch_rows
            )

        training_loss = float(
            total_training_loss
            /
            total_training_rows
        )

        validation_result = (
            evaluate_validation(
                model,
                validation_loader,
                criterion,
                device,
            )
        )

        validation_loss = (
            validation_result[
                "loss"
            ]
        )

        validation_roc_auc = (
            validation_result[
                "roc_auc"
            ]
        )

        validation_pr_auc = (
            validation_result[
                "pr_auc"
            ]
        )

        scheduler.step(
            validation_pr_auc
        )

        current_learning_rate = float(
            optimizer.param_groups[
                0
            ][
                "lr"
            ]
        )

        epoch_seconds = float(
            time.perf_counter()
            - epoch_start_time
        )

        history_rows.append(
            {
                "candidate_id": candidate_id,
                "epoch": int(
                    epoch
                ),
                "training_loss": (
                    training_loss
                ),
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
                "epoch_seconds": (
                    epoch_seconds
                ),
            }
        )

        improved = bool(
            validation_pr_auc
            > best_pr_auc
            + 1e-7
            or
            (
                abs(
                    validation_pr_auc
                    - best_pr_auc
                )
                <= 1e-7
                and
                validation_loss
                < best_validation_loss
            )
        )

        if improved:
            best_pr_auc = (
                validation_pr_auc
            )

            best_validation_loss = (
                validation_loss
            )

            best_epoch = int(
                epoch
            )

            epochs_without_improvement = 0

            torch.save(
                {
                    "candidate_id": (
                        candidate_id
                    ),
                    "architecture": (
                        candidate
                    ),
                    "epoch": (
                        best_epoch
                    ),
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
                },
                checkpoint_path,
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
                "Early stopping triggered."
            )
            break

    if best_epoch is None:
        raise RuntimeError(
            f"No checkpoint was saved for {candidate_id}."
        )

    checkpoint = torch.load(
        checkpoint_path,
        map_location=device,
        weights_only=False,
    )

    model.load_state_dict(
        checkpoint[
            "model_state_dict"
        ]
    )

    validation_probabilities, (
        validation_labels
    ) = predict_probabilities(
        model,
        validation_loader,
        device,
    )

    if not np.array_equal(
        validation_labels,
        y_validation.astype(
            np.int8
        ),
    ):
        raise RuntimeError(
            "Validation label order changed."
        )

    validation_roc_auc = float(
        roc_auc_score(
            validation_labels,
            validation_probabilities,
        )
    )

    validation_pr_auc = float(
        average_precision_score(
            validation_labels,
            validation_probabilities,
        )
    )

    selected_threshold_metrics, (
        candidate_threshold_rows
    ) = select_threshold(
        validation_labels,
        validation_probabilities,
        threshold_minimum=float(
            protocol[
                "threshold_minimum"
            ]
        ),
        threshold_maximum=float(
            protocol[
                "threshold_maximum"
            ]
        ),
        threshold_step=float(
            protocol[
                "threshold_step"
            ]
        ),
    )

    for row in candidate_threshold_rows:
        threshold_rows.append(
            {
                "candidate_id": (
                    candidate_id
                ),
                **row,
            }
        )

    peak_gpu_memory_mb = float(
        torch.cuda.max_memory_allocated()
        /
        (1024 ** 2)
    )

    candidate_seconds = float(
        time.perf_counter()
        - candidate_start_time
    )

    validation_metric_record = {
        "candidate_id": candidate_id,
        "parameter_count": (
            parameter_count
        ),
        "best_epoch": (
            best_epoch
        ),
        "epochs_executed": int(
            max(
                row["epoch"]
                for row in history_rows
                if (
                    row[
                        "candidate_id"
                    ]
                    == candidate_id
                )
            )
        ),
        "best_validation_loss": float(
            best_validation_loss
        ),
        "roc_auc": (
            validation_roc_auc
        ),
        "pr_auc": (
            validation_pr_auc
        ),
        **selected_threshold_metrics,
        "peak_gpu_memory_mb": (
            peak_gpu_memory_mb
        ),
        "runtime_seconds": (
            candidate_seconds
        ),
        "checkpoint_path": str(
            checkpoint_path
        ),
    }

    validation_metric_rows.append(
        validation_metric_record
    )

    candidate_results.append(
        {
            "candidate_id": candidate_id,
            "architecture": candidate,
            "validation": (
                validation_metric_record
            ),
        }
    )

    validation_probability_archive[
        candidate_id
    ] = validation_probabilities.astype(
        np.float32
    )

    print("\nSelected validation result:")
    print(
        f"  Best epoch: {best_epoch}"
    )
    print(
        f"  Threshold: "
        f"{selected_threshold_metrics['threshold']:.3f}"
    )
    print(
        f"  F1: "
        f"{selected_threshold_metrics['f1']:.6f}"
    )
    print(
        f"  F2: "
        f"{selected_threshold_metrics['f2']:.6f}"
    )
    print(
        f"  Precision: "
        f"{selected_threshold_metrics['precision']:.6f}"
    )
    print(
        f"  Recall: "
        f"{selected_threshold_metrics['recall']:.6f}"
    )
    print(
        f"  PR-AUC: {validation_pr_auc:.6f}"
    )
    print(
        f"  Peak GPU memory: "
        f"{peak_gpu_memory_mb:.2f} MB"
    )

    del model
    del optimizer
    del scheduler
    del checkpoint

    torch.cuda.empty_cache()


# ------------------------------------------------------------
# Select architecture using validation only
# ------------------------------------------------------------

selected_candidate = sorted(
    validation_metric_rows,
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

selected_candidate_id = (
    selected_candidate[
        "candidate_id"
    ]
)

benchmark_seconds = float(
    time.perf_counter()
    - benchmark_start_time
)


# ------------------------------------------------------------
# Save tables and probability archive
# ------------------------------------------------------------

history_frame = pd.DataFrame(
    history_rows
)

validation_metrics_frame = (
    pd.DataFrame(
        validation_metric_rows
    )
    .sort_values(
        [
            "f1",
            "pr_auc",
        ],
        ascending=False,
    )
    .reset_index(
        drop=True
    )
)

threshold_frame = pd.DataFrame(
    threshold_rows
)

history_frame.to_csv(
    TRAINING_HISTORY_PATH,
    index=False,
)

validation_metrics_frame.to_csv(
    VALIDATION_METRICS_PATH,
    index=False,
)

threshold_frame.to_csv(
    THRESHOLD_SWEEP_PATH,
    index=False,
)

np.savez_compressed(
    VALIDATION_PROBABILITIES_PATH,
    **validation_probability_archive,
)


# ------------------------------------------------------------
# Save architecture selection
# ------------------------------------------------------------

selection_record = {
    "stage": "15.3A",
    "selection_data": (
        "Duplicate-safe validation split only"
    ),
    "selection_rule": [
        "Highest validation F1 at a validation-selected threshold",
        "Highest validation PR-AUC",
        "Highest validation F2",
        "Highest validation recall",
        "Lowest validation false-negative rate",
        "Lowest parameter count",
        "Lexicographic candidate ID",
    ],
    "selected_candidate_id": (
        selected_candidate_id
    ),
    "selected_validation_metrics": (
        selected_candidate
    ),
    "selected_checkpoint": (
        selected_candidate[
            "checkpoint_path"
        ]
    ),
    "architecture_status": (
        "Provisional validation-selected winner. "
        "Requires multi-seed confirmation before holdout evaluation."
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
# Save complete result and metadata
# ------------------------------------------------------------

result_record = {
    "stage": "15.3A",
    "generated_at_utc": datetime.now(
        timezone.utc
    ).isoformat(),
    "runtime_seconds": (
        benchmark_seconds
    ),
    "runtime_minutes": float(
        benchmark_seconds
        /
        60.0
    ),
    "candidate_count": int(
        len(
            candidates
        )
    ),
    "candidate_results": (
        candidate_results
    ),
    "selected_candidate": (
        selection_record
    ),
    "GPU": {
        "device": device_name,
        "capability": device_capability,
        "torch_version": torch.__version__,
        "CUDA_runtime": torch.version.cuda,
        "compiled_architectures": (
            compiled_architectures
        ),
    },
    "data": {
        "training_rows": int(
            len(
                train_indices
            )
        ),
        "validation_rows": int(
            len(
                validation_indices
            )
        ),
        "retained_features": 70,
        "training_benign": (
            training_benign_count
        ),
        "training_attack": (
            training_attack_count
        ),
        "positive_class_weight": (
            positive_class_weight
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
    "stage": "15.3A",
    "generated_at_utc": datetime.now(
        timezone.utc
    ).isoformat(),
    "purpose": (
        "Compare compact FT-Transformer architectures "
        "using duplicate-safe training and validation only."
    ),
    "dataset_loading_policy": (
        "The CSV was read in chunks and only rows belonging "
        "to the training or validation index sets were retained."
    ),
    "holdout_access": False,
    "holdout_indices_loaded": False,
    "holdout_features_loaded": False,
    "holdout_labels_loaded": False,
    "holdout_probabilities_generated": False,
    "holdout_metrics_generated": False,
    "preprocessing": (
        "Archived StandardScaler fit on duplicate-safe "
        "training rows only"
    ),
    "class_weighting": (
        "Positive-class weight derived from training labels only"
    ),
    "early_stopping_metric": "Validation PR-AUC",
    "threshold_selection": (
        "Validation F1 with deterministic tie-breaking"
    ),
    "next_step": (
        "Run multi-seed confirmation for the provisional "
        "winning architecture before touching holdout."
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
# Final report
# ------------------------------------------------------------

print("\n" + "=" * 110)
print("STAGE 15.3A ARCHITECTURE BENCHMARK SUMMARY")
print("=" * 110)

print("\nRuntime:")
print(
    f"  {benchmark_seconds / 60.0:.2f} minutes"
)

print("\nValidation architecture comparison:")
print(
    validation_metrics_frame[
        [
            "candidate_id",
            "parameter_count",
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
            "peak_gpu_memory_mb",
            "runtime_seconds",
        ]
    ].to_string(
        index=False
    )
)

print("\nProvisional selected architecture:")
print(
    " ",
    selected_candidate_id
)

print(
    "  Validation threshold:",
    selected_candidate[
        "threshold"
    ],
)

print(
    "  Validation F1:",
    selected_candidate[
        "f1"
    ],
)

print(
    "  Validation F2:",
    selected_candidate[
        "f2"
    ],
)

print(
    "  Validation PR-AUC:",
    selected_candidate[
        "pr_auc"
    ],
)

print(
    "  Validation recall:",
    selected_candidate[
        "recall"
    ],
)

print(
    "  Validation FNR:",
    selected_candidate[
        "fnr"
    ],
)

print("\nSelection status:")
print(
    "  PROVISIONAL — MULTI-SEED CONFIRMATION REQUIRED"
)

print("\nHoldout status:")
print("  UNTOUCHED")

print("\nSaved artifacts:")
print(TRAINING_HISTORY_PATH)
print(VALIDATION_METRICS_PATH)
print(THRESHOLD_SWEEP_PATH)
print(VALIDATION_PROBABILITIES_PATH)
print(SELECTION_PATH)
print(RESULT_PATH)
print(METADATA_PATH)
print(MODEL_DIR)

print("\nStage 15.3A complete.")
