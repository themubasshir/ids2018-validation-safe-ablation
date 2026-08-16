
from pathlib import Path
from collections import OrderedDict

import hashlib
import json
import math
import os
import sys
import time

import numpy as np


WORK = Path("/kaggle/working")
REPO = WORK / "ids2018-validation-safe-ablation"

RESULTS = REPO / "results/stage21_architecture"

OUT = WORK / "stage21_5_analysis"

CNN_PROBS_PATH = (
    REPO
    / "results/stage20_1e_training/"
      "stage20_1e4_friday_probabilities.npy"
)

CNN_EVAL_PATH = (
    REPO
    / "results/stage20_1e_training/"
      "stage20_1e4_friday_holdout_evaluation.json"
)

VIT_PROBS_PATH = (
    RESULTS
    / "stage21_4_friday_probabilities.npy"
)

VIT_EVAL_PATH = (
    RESULTS
    / "stage21_4_friday_reuse_evaluation.json"
)

LABELS_PATH = (
    WORK
    / "stage20_compact_corpus/Friday/labels.npy"
)

RESULT_PATH = (
    OUT
    / "stage21_5_cnn_vit_descriptive_comparison.json"
)

BOOT_PATH = (
    OUT
    / "stage21_5_paired_bootstrap_deltas.npy"
)


PARENT = "6497229a2c8ff3c4bc3b4b9d9185e95b2336e56e"

CNN_PROB_SHA = (
    "e46a112e1e0320f645ec9d9502f0b3c0d8bdcf3987b50b2cd2352ef7484e2124"
)

VIT_PROB_SHA = (
    "aeb24de4d40a56b7d69b2a8bedcca995e248f680f2e50b3fa3ee3db2a06f16ad"
)

LABEL_SHA = (
    "239b124119824fac23cff9fdcfbc24bc46227a0b6d4b1ad2201e955c263347d8"
)

REPLICATES = 10_000
SEED = 21_042
N = 12_088


def sha256_file(path):
    h = hashlib.sha256()

    with Path(path).open("rb") as f:
        while True:
            b = f.read(16 * 1024 * 1024)
            if not b:
                break
            h.update(b)

    return h.hexdigest()


def atomic_json(path, obj):
    tmp = Path(str(path) + ".tmp")

    tmp.write_text(
        json.dumps(obj, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    os.replace(tmp, path)


def save_npy_atomic(path, array):
    tmp = Path(str(path) + ".tmp")

    with tmp.open("wb") as f:
        np.save(
            f,
            array,
            allow_pickle=False,
        )

    os.replace(tmp, path)


# =========================================================================
# Load exact aligned persisted scores
# =========================================================================

assert sha256_file(CNN_PROBS_PATH) == CNN_PROB_SHA
assert sha256_file(VIT_PROBS_PATH) == VIT_PROB_SHA
assert sha256_file(LABELS_PATH) == LABEL_SHA

cnn = np.load(
    CNN_PROBS_PATH,
    allow_pickle=False,
)

vit = np.load(
    VIT_PROBS_PATH,
    allow_pickle=False,
)

labels = np.load(
    LABELS_PATH,
    allow_pickle=False,
)

assert cnn.shape == (N,)
assert vit.shape == (N,)
assert labels.shape == (N,)

assert cnn.dtype == np.float32
assert vit.dtype == np.float32
assert labels.dtype == np.uint8

assert np.all(np.isfinite(cnn))
assert np.all(np.isfinite(vit))

class_counts = np.bincount(
    labels,
    minlength=2,
)

assert int(class_counts[0]) == 6486
assert int(class_counts[1]) == 5602


cnn_eval = json.loads(
    CNN_EVAL_PATH.read_text(encoding="utf-8")
)

vit_eval = json.loads(
    VIT_EVAL_PATH.read_text(encoding="utf-8")
)


# =========================================================================
# Grouped-score metric plan
#
# Bootstrap multiplicity changes how often each flow appears but DOES NOT
# change the ordering of its persisted score. Therefore we sort each model
# once and use bootstrap multiplicities as exact integer weights.
#
# This is exactly equivalent to constructing each resampled score vector
# and re-sorting it, but much faster.
# =========================================================================

def make_plan(score):
    order = np.argsort(
        -score,
        kind="stable",
    )

    sorted_score = score[order]
    sorted_label = labels[order].astype(
        np.int64,
        copy=False,
    )

    starts = np.concatenate(
        (
            np.array([0], dtype=np.int64),
            np.flatnonzero(
                sorted_score[1:]
                !=
                sorted_score[:-1]
            ).astype(np.int64)
            +
            1,
        )
    )

    return {
        "order": order,
        "sorted_label": sorted_label,
        "starts": starts,
    }


cnn_plan = make_plan(cnn)
vit_plan = make_plan(vit)


def weighted_grouped_auc(plan, counts):
    ordered_counts = counts[
        plan["order"]
    ].astype(
        np.int64,
        copy=False,
    )

    y = plan["sorted_label"]

    positive_weights = (
        ordered_counts
        *
        y
    )

    negative_weights = (
        ordered_counts
        *
        (
            1
            -
            y
        )
    )

    group_tp = np.add.reduceat(
        positive_weights,
        plan["starts"],
    )

    group_fp = np.add.reduceat(
        negative_weights,
        plan["starts"],
    )

    tp = np.cumsum(
        group_tp,
        dtype=np.int64,
    )

    fp = np.cumsum(
        group_fp,
        dtype=np.int64,
    )

    P = int(tp[-1])
    Nneg = int(fp[-1])

    assert P > 0
    assert Nneg > 0

    prev_tp = np.empty_like(tp)
    prev_fp = np.empty_like(fp)

    prev_tp[0] = 0
    prev_fp[0] = 0

    prev_tp[1:] = tp[:-1]
    prev_fp[1:] = fp[:-1]

    roc_numerator = np.sum(
        (
            fp
            -
            prev_fp
        )
        *
        (
            tp
            +
            prev_tp
        )
        /
        2.0,
        dtype=np.float64,
    )

    roc_auc = (
        roc_numerator
        /
        (
            P
            *
            Nneg
        )
    )

    nonzero_positive_groups = (
        group_tp
        >
        0
    )

    recall_delta = (
        group_tp[
            nonzero_positive_groups
        ].astype(np.float64)
        /
        P
    )

    precision = (
        tp[
            nonzero_positive_groups
        ].astype(np.float64)
        /
        (
            tp[
                nonzero_positive_groups
            ]
            +
            fp[
                nonzero_positive_groups
            ]
        )
    )

    average_precision = np.sum(
        recall_delta
        *
        precision,
        dtype=np.float64,
    )

    return (
        float(roc_auc),
        float(average_precision),
    )


# =========================================================================
# Reproduce sealed observed metrics from persisted scores
# =========================================================================

ones = np.ones(
    N,
    dtype=np.int64,
)

cnn_roc, cnn_pr = weighted_grouped_auc(
    cnn_plan,
    ones,
)

vit_roc, vit_pr = weighted_grouped_auc(
    vit_plan,
    ones,
)


sealed_cnn_roc = float(
    cnn_eval["score_metrics"]["ROC_AUC"]
)

sealed_cnn_pr = float(
    cnn_eval["score_metrics"]["PR_AUC"]
)

sealed_vit_roc = float(
    vit_eval["score_metrics"]["ROC_AUC"]
)

sealed_vit_pr = float(
    vit_eval["score_metrics"]["PR_AUC"]
)


assert math.isclose(
    cnn_roc,
    sealed_cnn_roc,
    rel_tol=0.0,
    abs_tol=1e-12,
)

assert math.isclose(
    cnn_pr,
    sealed_cnn_pr,
    rel_tol=0.0,
    abs_tol=1e-12,
)

assert math.isclose(
    vit_roc,
    sealed_vit_roc,
    rel_tol=0.0,
    abs_tol=1e-12,
)

assert math.isclose(
    vit_pr,
    sealed_vit_pr,
    rel_tol=0.0,
    abs_tol=1e-12,
)


# =========================================================================
# Numerical reproduction audit
#
# The Stage21-5D pre-bootstrap diagnostic established that reconstruction from
# the exact persisted score vectors reproduces the sealed metrics to within
# 3.664e-15.  The small discrepancy is floating-point accumulation order only.
#
# The already-sealed Stage20 / Stage21-4 metrics therefore remain the exact
# observed source-of-truth point estimates.  Weighted grouped-score arithmetic
# is used only for paired bootstrap replicates.
# =========================================================================

recomputed_cnn_roc = float(cnn_roc)
recomputed_cnn_pr = float(cnn_pr)

recomputed_vit_roc = float(vit_roc)
recomputed_vit_pr = float(vit_pr)


cnn_roc = float(sealed_cnn_roc)
cnn_pr = float(sealed_cnn_pr)

vit_roc = float(sealed_vit_roc)
vit_pr = float(sealed_vit_pr)


delta_roc = (
    vit_roc
    -
    cnn_roc
)

delta_pr = (
    vit_pr
    -
    cnn_pr
)


if delta_roc > 0 and delta_pr > 0:
    classification = (
        "DESCRIPTIVE_BENCHMARK_IMPROVEMENT_ON_BOTH_RANKING_METRICS"
    )

elif delta_roc <= 0 and delta_pr <= 0:
    classification = (
        "NO_BENCHMARK_RANKING_IMPROVEMENT"
    )

else:
    classification = (
        "MIXED_BENCHMARK_RESULT"
    )


print("=" * 88)
print("OBSERVED FROZEN CNN-vs-ViT RANKING COMPARISON")
print("=" * 88)

print("CNN ROC-AUC:", cnn_roc)
print("ViT ROC-AUC:", vit_roc)
print("Δ ROC-AUC:  ", delta_roc)

print()

print("CNN PR-AUC: ", cnn_pr)
print("ViT PR-AUC: ", vit_pr)
print("Δ PR-AUC:   ", delta_pr)

print()

print("Classification:")
print(" ", classification)


# =========================================================================
# Secondary preregistered descriptive operating-point deltas
# =========================================================================

cnn_standard = (
    cnn_eval["operating_points"]
    ["standard"]
    ["metrics"]
)

cnn_balanced = (
    cnn_eval["operating_points"]
    ["balanced"]
    ["metrics"]
)

cnn_security = (
    cnn_eval["operating_points"]
    ["security"]
    ["metrics"]
)


vit_standard = (
    vit_eval["operating_points"]
    ["standard"]
    ["metrics"]
)

vit_balanced = (
    vit_eval["operating_points"]
    ["balanced"]
    ["metrics"]
)

vit_security = (
    vit_eval["operating_points"]
    ["security"]
    ["metrics"]
)


assert cnn_standard["threshold"] == 0.50
assert cnn_balanced["threshold"] == 0.17
assert cnn_security["threshold"] == 0.17

assert vit_standard["threshold"] == 0.50
assert vit_balanced["threshold"] == 0.42
assert vit_security["threshold"] == 0.24


secondary = {
    "STANDARD_0_50_F1": {
        "CNN":
            float(cnn_standard["F1"]),

        "ViT":
            float(vit_standard["F1"]),

        "ViT_MINUS_CNN":
            float(
                vit_standard["F1"]
                -
                cnn_standard["F1"]
            ),
    },

    "STANDARD_0_50_RECALL": {
        "CNN":
            float(cnn_standard["Recall"]),

        "ViT":
            float(vit_standard["Recall"]),

        "ViT_MINUS_CNN":
            float(
                vit_standard["Recall"]
                -
                cnn_standard["Recall"]
            ),
    },

    "VALIDATION_SELECTED_BALANCED_F1": {
        "CNN_threshold":
            0.17,

        "ViT_threshold":
            0.42,

        "CNN":
            float(cnn_balanced["F1"]),

        "ViT":
            float(vit_balanced["F1"]),

        "ViT_MINUS_CNN":
            float(
                vit_balanced["F1"]
                -
                cnn_balanced["F1"]
            ),
    },

    "VALIDATION_SELECTED_BALANCED_RECALL": {
        "CNN_threshold":
            0.17,

        "ViT_threshold":
            0.42,

        "CNN":
            float(cnn_balanced["Recall"]),

        "ViT":
            float(vit_balanced["Recall"]),

        "ViT_MINUS_CNN":
            float(
                vit_balanced["Recall"]
                -
                cnn_balanced["Recall"]
            ),
    },

    "VALIDATION_SELECTED_SECURITY_F2": {
        "CNN_threshold":
            0.17,

        "ViT_threshold":
            0.24,

        "CNN":
            float(cnn_security["F2"]),

        "ViT":
            float(vit_security["F2"]),

        "ViT_MINUS_CNN":
            float(
                vit_security["F2"]
                -
                cnn_security["F2"]
            ),
    },

    "VALIDATION_SELECTED_SECURITY_RECALL": {
        "CNN_threshold":
            0.17,

        "ViT_threshold":
            0.24,

        "CNN":
            float(cnn_security["Recall"]),

        "ViT":
            float(vit_security["Recall"]),

        "ViT_MINUS_CNN":
            float(
                vit_security["Recall"]
                -
                cnn_security["Recall"]
            ),
    },
}


# =========================================================================
# Preregistered paired FLOW bootstrap
# =========================================================================

print()
print("=" * 88)
print("PAIRED FLOW BOOTSTRAP — 10,000 REPLICATES")
print("=" * 88)

rng = np.random.default_rng(
    SEED
)

bootstrap = np.empty(
    (
        REPLICATES,
        2,
    ),
    dtype=np.float64,
)


start_time = time.time()


for replicate in range(
    REPLICATES
):

    # Standard flow-level bootstrap:
    # sample N flow indices with replacement.
    sampled_indices = rng.integers(
        0,
        N,
        size=N,
        dtype=np.int64,
    )

    # Multiplicity representation is mathematically identical to
    # materializing the paired resampled score arrays.
    counts = np.bincount(
        sampled_indices,
        minlength=N,
    ).astype(
        np.int64,
        copy=False,
    )

    # Same counts for BOTH models = paired bootstrap.
    cnn_r_roc, cnn_r_pr = weighted_grouped_auc(
        cnn_plan,
        counts,
    )

    vit_r_roc, vit_r_pr = weighted_grouped_auc(
        vit_plan,
        counts,
    )

    bootstrap[
        replicate,
        0,
    ] = (
        vit_r_roc
        -
        cnn_r_roc
    )

    bootstrap[
        replicate,
        1,
    ] = (
        vit_r_pr
        -
        cnn_r_pr
    )


    if (
        replicate + 1
    ) % 1000 == 0:

        elapsed = (
            time.time()
            -
            start_time
        )

        print(
            f"  {replicate + 1:,}/{REPLICATES:,} "
            f"elapsed={elapsed:.2f}s",
            flush=True,
        )


assert bootstrap.shape == (
    REPLICATES,
    2,
)

assert bootstrap.dtype == np.float64

assert np.all(
    np.isfinite(
        bootstrap
    )
)


save_npy_atomic(
    BOOT_PATH,
    bootstrap,
)


# =========================================================================
# Frozen percentile interval rule
#
# Protocol specified PERCENTILE_95_PERCENT.
# Endpoints are therefore empirical 2.5th and 97.5th percentiles.
# NumPy's explicit "linear" percentile interpolation is recorded.
# =========================================================================

roc_ci = np.quantile(
    bootstrap[
        :,
        0,
    ],
    [
        0.025,
        0.975,
    ],
    method="linear",
)


pr_ci = np.quantile(
    bootstrap[
        :,
        1,
    ],
    [
        0.025,
        0.975,
    ],
    method="linear",
)


roc_median = float(
    np.quantile(
        bootstrap[:, 0],
        0.5,
        method="linear",
    )
)

pr_median = float(
    np.quantile(
        bootstrap[:, 1],
        0.5,
        method="linear",
    )
)


bootstrap_sha = sha256_file(
    BOOT_PATH
)


result = {
    "checkpoint":
        "Stage21-5",

    "status":
        "PREREGISTERED_DESCRIPTIVE_CNN_VIT_COMPARISON_COMPLETE",

    "parent_commit":
        PARENT,

    "role":
        "LOCKED_FRIDAY_REUSE_BENCHMARK_NON_CONFIRMATORY",

    "claim_boundary": {
        "confirmatory":
            False,

        "architecture_selection_from_Friday":
            False,

        "model_selection_from_bootstrap":
            False,

        "threshold_selection_from_Friday":
            False,

        "general_architecture_superiority_claim":
            False,
    },

    "population": {
        "flows":
            N,

        "benign":
            int(class_counts[0]),

        "attack":
            int(class_counts[1]),

        "pairing":
            "EXACT_SAME_FRIDAY_COMPACT_CORPUS_EXPORT_ORDER",
    },

    "inputs": {
        "CNN_probabilities_sha256":
            CNN_PROB_SHA,

        "ViT_probabilities_sha256":
            VIT_PROB_SHA,

        "labels_sha256":
            LABEL_SHA,
    },

    "co_primary_descriptive": {
        "CNN_ROC_AUC":
            float(cnn_roc),

        "ViT_ROC_AUC":
            float(vit_roc),

        "ViT_MINUS_CNN_ROC_AUC":
            float(delta_roc),

        "CNN_PR_AUC":
            float(cnn_pr),

        "ViT_PR_AUC":
            float(vit_pr),

        "ViT_MINUS_CNN_PR_AUC":
            float(delta_pr),

        "classification":
            classification,
    },

    "paired_bootstrap": {
        "unit":
            "FLOW",

        "paired":
            True,

        "replicates":
            REPLICATES,

        "seed":
            SEED,

        "rng":
            "numpy.random.default_rng_PCG64",

        "numpy_version":
            np.__version__,

        "interval":
            "PERCENTILE_95_PERCENT",

        "percentiles":
            [
                2.5,
                97.5,
            ],

        "quantile_method":
            "linear",

        "delta_definition":
            "ViT_MINUS_CNN",

        "targets": {
            "DELTA_ROC_AUC": {
                "observed":
                    float(delta_roc),

                "bootstrap_median":
                    roc_median,

                "percentile_95_CI": [
                    float(roc_ci[0]),
                    float(roc_ci[1]),
                ],
            },

            "DELTA_PR_AUC": {
                "observed":
                    float(delta_pr),

                "bootstrap_median":
                    pr_median,

                "percentile_95_CI": [
                    float(pr_ci[0]),
                    float(pr_ci[1]),
                ],
            },
        },

        "artifact": {
            "path":
                "results/stage21_architecture/"
                "stage21_5_paired_bootstrap_deltas.npy",

            "shape":
                [
                    REPLICATES,
                    2,
                ],

            "dtype":
                "float64",

            "columns": [
                "ViT_MINUS_CNN_ROC_AUC",
                "ViT_MINUS_CNN_PR_AUC",
            ],

            "sha256":
                bootstrap_sha,
        },

        "descriptive_not_confirmatory":
            True,
    },

    "secondary_descriptive_deltas":
        secondary,

    "scientific_boundary": {
        "new_model_forward_passes":
            0,

        "CNN_retrained":
            False,

        "ViT_retrained":
            False,

        "optimizer_steps":
            0,

        "Friday_threshold_search":
            False,

        "Friday_threshold_reselection":
            False,

        "architecture_search":
            False,

        "bootstrap_used_for_selection":
            False,

        "new_candidate_added":
            False,
    },
}


result["numerical_reproduction_gate"] = {
    "purpose":
        "VERIFY_PERSISTED_SCORE_METRIC_RECONSTRUCTION_BEFORE_BOOTSTRAP",

    "observed_source_of_truth":
        "SEALED_STAGE20_AND_STAGE21_4_SCORE_METRICS",

    "reproduction_tolerance_abs":
        1e-12,

    "CNN": {
        "ROC_AUC": {
            "sealed":
                float(sealed_cnn_roc),

            "recomputed":
                float(recomputed_cnn_roc),

            "absolute_difference":
                float(
                    abs(
                        recomputed_cnn_roc
                        -
                        sealed_cnn_roc
                    )
                ),
        },

        "PR_AUC": {
            "sealed":
                float(sealed_cnn_pr),

            "recomputed":
                float(recomputed_cnn_pr),

            "absolute_difference":
                float(
                    abs(
                        recomputed_cnn_pr
                        -
                        sealed_cnn_pr
                    )
                ),
        },
    },

    "ViT": {
        "ROC_AUC": {
            "sealed":
                float(sealed_vit_roc),

            "recomputed":
                float(recomputed_vit_roc),

            "absolute_difference":
                float(
                    abs(
                        recomputed_vit_roc
                        -
                        sealed_vit_roc
                    )
                ),
        },

        "PR_AUC": {
            "sealed":
                float(sealed_vit_pr),

            "recomputed":
                float(recomputed_vit_pr),

            "absolute_difference":
                float(
                    abs(
                        recomputed_vit_pr
                        -
                        sealed_vit_pr
                    )
                ),
        },
    },

    "gate_pass":
        True,

    "scientific_specification_changed":
        False,

    "bootstrap_specification_changed":
        False,
}


atomic_json(
    RESULT_PATH,
    result,
)


print()
print("=" * 88)
print("STAGE21-5 BOOTSTRAP RESULT")
print("=" * 88)

print(
    "Δ ROC-AUC observed:",
    delta_roc,
)

print(
    "Δ ROC-AUC 95% CI:",
    float(roc_ci[0]),
    float(roc_ci[1]),
)

print()
print(
    "Δ PR-AUC observed:",
    delta_pr,
)

print(
    "Δ PR-AUC 95% CI:",
    float(pr_ci[0]),
    float(pr_ci[1]),
)

print()
print(
    "Classification:",
    classification,
)

print()
print(
    "Bootstrap artifact SHA256:",
    bootstrap_sha,
)

print()
print("New model forwards:          0")
print("Threshold search:            NO")
print("Threshold reselection:       NO")
print("Training:                    NO")
print("Architecture selection:      NO")
print("Bootstrap-based selection:   NO")
print("=" * 88)
