
from pathlib import Path
import hashlib
import importlib.util
import json
import math
import os

import numpy as np
import torch


WORK = Path("/kaggle/working")
REPO = WORK / "ids2018-validation-safe-ablation"
THURSDAY = WORK / "stage20_compact_corpus/Thursday"

MODEL = (
    REPO
    / "results/stage21_architecture/"
    "stage21_2_epoch10_model_state_dict.pt"
)

VIT_MODULE = REPO / "scripts/stage21_masked_vit.py"
LOADER_MODULE = REPO / "scripts/stage20_compact_corpus.py"

OUT = WORK / "stage21_validation"
OUT.mkdir(parents=True, exist_ok=True)

PROBS = OUT / "stage21_3_thursday_probabilities.npy"
EVAL = OUT / "stage21_3_thursday_validation_evaluation.json"

MODEL_SHA = (
    "221e9c805fb663acacf2f0f2ca95dba7cb4b2ec4c4de5a3650cf4adeb99b5ef8"
)

MODEL_STATE_SHA = (
    "9da47df6cd5c821eef3d2c8a501296cd6070b835c719999f572f3dec2d560771"
)

PARENT = "7f63e836609aa63939d01929b33fd4ccfa897a44"


def sha256_file(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        while True:
            b = f.read(16 * 1024 * 1024)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def import_path(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def save_npy_atomic(path, array):
    tmp = Path(str(path) + ".tmp")
    with tmp.open("wb") as f:
        np.save(f, array, allow_pickle=False)
    os.replace(tmp, path)


def atomic_json(path, obj):
    tmp = Path(str(path) + ".tmp")
    tmp.write_text(
        json.dumps(obj, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(tmp, path)


def canonical_state_sha256(state):
    h = hashlib.sha256()

    for name in sorted(state.keys()):
        arr = (
            state[name]
            .detach()
            .cpu()
            .contiguous()
            .numpy()
        )

        nb = name.encode("utf-8")
        db = str(arr.dtype).encode("ascii")

        h.update(len(nb).to_bytes(4, "little"))
        h.update(nb)
        h.update(len(db).to_bytes(2, "little"))
        h.update(db)
        h.update(
            np.asarray(
                arr.shape,
                dtype=np.int64,
            ).tobytes()
        )
        h.update(arr.tobytes(order="C"))

    return h.hexdigest()


# ---------------------------------------------------------------------------
# Exact frozen runtime
# ---------------------------------------------------------------------------

assert np.__version__ == "2.4.6"
assert torch.__version__ == "2.10.0+cu126"
assert torch.version.cuda == "12.6"
assert torch.cuda.is_available()

assert os.environ["CUBLAS_WORKSPACE_CONFIG"] == ":4096:8"

torch.backends.cudnn.benchmark = False
torch.backends.cudnn.deterministic = True
torch.backends.cuda.matmul.allow_tf32 = False
torch.backends.cudnn.allow_tf32 = False
torch.use_deterministic_algorithms(True)
torch.set_float32_matmul_precision("highest")

device = torch.device("cuda")


# ---------------------------------------------------------------------------
# Exact Thursday compact data
# ---------------------------------------------------------------------------

encoded = np.fromfile(
    THURSDAY / "encoded_bytes.bin",
    dtype=np.uint8,
)

lengths = np.load(
    THURSDAY / "packet_lengths.npy",
    allow_pickle=False,
)

offsets = np.load(
    THURSDAY / "flow_offsets.npy",
    allow_pickle=False,
)

labels = np.load(
    THURSDAY / "labels.npy",
    allow_pickle=False,
)

assert lengths.shape == (8197, 64)
assert offsets.shape == (8198,)
assert labels.shape == (8197,)
assert labels.dtype == np.uint8
assert int(offsets[0]) == 0
assert int(offsets[-1]) == len(encoded)

counts = np.bincount(labels, minlength=2)

assert int(counts[0]) == 8155
assert int(counts[1]) == 42


# ---------------------------------------------------------------------------
# Exact dense reconstruction, verified against frozen loader BEFORE forward
# ---------------------------------------------------------------------------

cols = np.arange(256, dtype=np.uint16)[None, None, :]

mask = (
    cols
    <
    lengths[:, :, None]
)

assert int(mask.sum()) == len(encoded)

image = np.zeros(
    (8197, 64, 256),
    dtype=np.uint8,
)

image[mask] = encoded


loader_mod = import_path(
    "stage20_compact_corpus_s21e3",
    LOADER_MODULE,
)

official = loader_mod.Stage20CompactCorpus(
    THURSDAY
)

for i in range(128):
    oi, om, ol = official.reconstruct(i)

    assert np.array_equal(
        image[i],
        oi,
    )

    assert np.array_equal(
        mask[i],
        om,
    )

    assert int(labels[i]) == int(ol)

print(
    "Thursday dense reconstruction ↔ frozen loader first128: PASS",
    flush=True,
)


# ---------------------------------------------------------------------------
# ONE inference pass, unless probabilities already exist.
# ---------------------------------------------------------------------------

if not PROBS.exists():

    assert not EVAL.exists()

    vit_mod = import_path(
        "stage21_masked_vit_s21e3",
        VIT_MODULE,
    )

    model = vit_mod.Stage21MaskedViTv1()

    assert (
        vit_mod.count_trainable_parameters(model)
        ==
        91969
    )

    state = torch.load(
        MODEL,
        map_location="cpu",
        weights_only=True,
    )

    assert (
        canonical_state_sha256(state)
        ==
        MODEL_STATE_SHA
    )

    model.load_state_dict(
        state,
        strict=True,
    )

    model.to(device)
    model.eval()

    batches = []
    BATCH = 256

    with torch.inference_mode():

        for start in range(
            0,
            8197,
            BATCH,
        ):
            end = min(
                start + BATCH,
                8197,
            )

            x = (
                torch.from_numpy(
                    np.ascontiguousarray(
                        image[start:end]
                    )
                )
                .to(
                    device=device,
                    dtype=torch.float32,
                )
                .unsqueeze(1)
                .div_(255.0)
            )

            m = (
                torch.from_numpy(
                    np.ascontiguousarray(
                        mask[start:end]
                    )
                )
                .to(
                    device=device,
                    dtype=torch.bool,
                )
                .unsqueeze(1)
            )

            logits = model(x, m)

            p = (
                torch.sigmoid(logits)
                .to(dtype=torch.float32)
                .cpu()
                .numpy()
                .astype(
                    np.float32,
                    copy=False,
                )
            )

            batches.append(p)

    probabilities = np.concatenate(
        batches
    ).astype(
        np.float32,
        copy=False,
    )

    assert probabilities.shape == (8197,)
    assert probabilities.dtype == np.float32
    assert np.all(np.isfinite(probabilities))

    save_npy_atomic(
        PROBS,
        probabilities,
    )

    print(
        "Thursday Stage21 model inference passes: 1",
        flush=True,
    )

else:

    probabilities = np.load(
        PROBS,
        allow_pickle=False,
    )

    assert probabilities.shape == (8197,)
    assert probabilities.dtype == np.float32
    assert np.all(np.isfinite(probabilities))

    print(
        "Existing persisted Thursday probabilities detected: "
        "NO additional model inference",
        flush=True,
    )


# ---------------------------------------------------------------------------
# Metrics — inherited exact Stage20-1E3 semantics
# ---------------------------------------------------------------------------

def operating_metrics(
    threshold_integer_percent,
):

    threshold = (
        threshold_integer_percent
        /
        100.0
    )

    pred = (
        probabilities
        >=
        threshold
    )

    positive = labels == 1
    negative = ~positive

    TP = int(np.count_nonzero(pred & positive))
    FP = int(np.count_nonzero(pred & negative))
    TN = int(np.count_nonzero((~pred) & negative))
    FN = int(np.count_nonzero((~pred) & positive))

    n = TP + TN + FP + FN

    precision = (
        TP / (TP + FP)
        if TP + FP
        else 0.0
    )

    recall = (
        TP / (TP + FN)
        if TP + FN
        else 0.0
    )

    f1_den = 2 * TP + FP + FN

    f1 = (
        2 * TP / f1_den
        if f1_den
        else 0.0
    )

    f2_den = (
        5 * TP
        +
        FP
        +
        4 * FN
    )

    f2 = (
        5 * TP / f2_den
        if f2_den
        else 0.0
    )

    fpr = (
        FP / (FP + TN)
        if FP + TN
        else 0.0
    )

    fnr = (
        FN / (FN + TP)
        if FN + TP
        else 0.0
    )

    return {
        "threshold_integer_percent":
            int(threshold_integer_percent),

        "threshold":
            float(threshold),

        "prediction_rule":
            "ATTACK_IF_FLOAT32_SIGMOID_PROBABILITY_GTE_THRESHOLD",

        "TP": TP,
        "TN": TN,
        "FP": FP,
        "FN": FN,

        "Accuracy":
            (TP + TN) / n,

        "Precision":
            precision,

        "Recall":
            recall,

        "F1":
            f1,

        "F2":
            f2,

        "FPR":
            fpr,

        "FNR":
            fnr,
    }


grid = [
    operating_metrics(i)
    for i in range(5, 96)
]


# ---------------------------------------------------------------------------
# Exact-rational comparator helpers
# ---------------------------------------------------------------------------

def ratio_cmp(
    a_num,
    a_den,
    b_num,
    b_den,
):
    left = a_num * b_den
    right = b_num * a_den

    return (
        1
        if left > right
        else
        -1
        if left < right
        else
        0
    )


def better_balanced(a, b):

    # 1. MAX F1 exactly
    cmp = ratio_cmp(
        2 * a["TP"],
        2 * a["TP"] + a["FP"] + a["FN"],
        2 * b["TP"],
        2 * b["TP"] + b["FP"] + b["FN"],
    )

    if cmp:
        return cmp > 0

    # 2. LOWER FPR
    cmp = ratio_cmp(
        a["FP"],
        a["FP"] + a["TN"],
        b["FP"],
        b["FP"] + b["TN"],
    )

    if cmp:
        return cmp < 0

    # 3. HIGHER RECALL
    cmp = ratio_cmp(
        a["TP"],
        a["TP"] + a["FN"],
        b["TP"],
        b["TP"] + b["FN"],
    )

    if cmp:
        return cmp > 0

    # 4. CLOSER TO 0.50
    da = abs(
        a["threshold_integer_percent"]
        -
        50
    )

    db = abs(
        b["threshold_integer_percent"]
        -
        50
    )

    if da != db:
        return da < db

    # 5. LOWER THRESHOLD
    return (
        a["threshold_integer_percent"]
        <
        b["threshold_integer_percent"]
    )


def better_security(a, b):

    # 1. MAX F2 exactly
    cmp = ratio_cmp(
        5 * a["TP"],
        5 * a["TP"] + a["FP"] + 4 * a["FN"],
        5 * b["TP"],
        5 * b["TP"] + b["FP"] + 4 * b["FN"],
    )

    if cmp:
        return cmp > 0

    # 2. LOWER FPR
    cmp = ratio_cmp(
        a["FP"],
        a["FP"] + a["TN"],
        b["FP"],
        b["FP"] + b["TN"],
    )

    if cmp:
        return cmp < 0

    # 3. HIGHER RECALL
    cmp = ratio_cmp(
        a["TP"],
        a["TP"] + a["FN"],
        b["TP"],
        b["TP"] + b["FN"],
    )

    if cmp:
        return cmp > 0

    # 4. LOWER THRESHOLD
    return (
        a["threshold_integer_percent"]
        <
        b["threshold_integer_percent"]
    )


balanced = grid[0]

for record in grid[1:]:
    if better_balanced(
        record,
        balanced,
    ):
        balanced = record


security_candidates = [
    r
    for r in grid
    if (
        20 * r["FP"]
        <=
        r["FP"] + r["TN"]
    )
]


security = None

if security_candidates:
    security = security_candidates[0]

    for record in security_candidates[1:]:
        if better_security(
            record,
            security,
        ):
            security = record


standard = next(
    r
    for r in grid
    if r["threshold_integer_percent"] == 50
)


# ---------------------------------------------------------------------------
# Grouped ROC-AUC and noninterpolated AP from persisted FLOAT32 scores
# ---------------------------------------------------------------------------

def grouped_auc(
    y,
    score,
):

    y = np.asarray(
        y,
        dtype=np.uint8,
    )

    score = np.asarray(
        score,
        dtype=np.float32,
    )

    order = np.argsort(
        -score,
        kind="stable",
    )

    ys = y[order]
    ss = score[order]

    P = int(np.count_nonzero(y == 1))
    N = int(np.count_nonzero(y == 0))

    assert P > 0 and N > 0

    tp = 0
    fp = 0

    prev_tp = 0
    prev_fp = 0

    roc_area_num = 0.0
    ap = 0.0

    i = 0
    n = len(y)

    while i < n:

        j = i + 1

        while (
            j < n
            and
            ss[j] == ss[i]
        ):
            j += 1

        group = ys[i:j]

        gtp = int(
            np.count_nonzero(
                group == 1
            )
        )

        gfp = int(
            (j - i) - gtp
        )

        tp += gtp
        fp += gfp

        # trapezoid in count coordinates
        roc_area_num += (
            (fp - prev_fp)
            *
            (tp + prev_tp)
            /
            2.0
        )

        if gtp:
            recall_delta = (
                (tp - prev_tp)
                /
                P
            )

            precision = (
                tp
                /
                (tp + fp)
            )

            ap += (
                recall_delta
                *
                precision
            )

        prev_tp = tp
        prev_fp = fp

        i = j

    roc_auc = (
        roc_area_num
        /
        (P * N)
    )

    return (
        float(roc_auc),
        float(ap),
    )


roc_auc, pr_auc = grouped_auc(
    labels,
    probabilities,
)


# ---------------------------------------------------------------------------
# Persist Stage21-3 source-of-truth evaluation
# ---------------------------------------------------------------------------

evaluation = {
    "checkpoint":
        "Stage21-3",

    "status":
        "THURSDAY_EVALUATED_ONCE_AND_STAGE21_VIT_OPERATING_POINTS_FROZEN",

    "parent_commit":
        PARENT,

    "model": {
        "name":
            "Stage21MaskedViTv1",

        "epoch":
            10,

        "checkpoint_path":
            "results/stage21_architecture/"
            "stage21_2_epoch10_model_state_dict.pt",

        "checkpoint_sha256":
            MODEL_SHA,

        "canonical_state_sha256":
            MODEL_STATE_SHA,

        "retrained_after_training":
            False,
    },

    "validation_population": {
        "day":
            "Thursday",

        "flows":
            8197,

        "benign":
            8155,

        "attack":
            42,
    },

    "probabilities": {
        "path":
            "results/stage21_architecture/"
            "stage21_3_thursday_probabilities.npy",

        "shape":
            [8197],

        "dtype":
            "float32",

        "bytes":
            int(PROBS.stat().st_size),

        "sha256":
            sha256_file(PROBS),

        "minimum":
            float(probabilities.min()),

        "maximum":
            float(probabilities.max()),

        "mean":
            float(probabilities.mean()),

        "order":
            "THURSDAY_COMPACT_CORPUS_EXPORT_ORDER",

        "source_of_truth_for_metrics":
            True,
    },

    "score_metrics": {
        "ROC_AUC":
            roc_auc,

        "PR_AUC":
            pr_auc,
    },

    "threshold_grid": {
        "count":
            91,

        "integer_percent_values":
            list(range(5, 96)),

        "records":
            grid,
    },

    "operating_points": {
        "standard": {
            "selection":
                "FIXED_0_50",

            "metrics":
                standard,
        },

        "balanced": {
            "selection":
                "MAXIMUM_VALIDATION_F1_WITH_FROZEN_TIE_BREAKS",

            "metrics":
                balanced,
        },

        "security": (
            {
                "available":
                    True,

                "constraint":
                    "FPR_LE_0_05",

                "selection":
                    "MAXIMUM_VALIDATION_F2_WITH_FROZEN_TIE_BREAKS",

                "metrics":
                    security,
            }
            if security is not None
            else
            {
                "available":
                    False,

                "constraint":
                    "FPR_LE_0_05",

                "selection":
                    "UNAVAILABLE_NO_RELAXATION",

                "metrics":
                    None,
            }
        ),
    },

    "metric_definitions": {
        "ROC_AUC":
            "DISTINCT_SCORE_GROUPED_TRAPEZOIDAL_ROC_AREA_FROM_PERSISTED_FLOAT32_PROBABILITIES",

        "PR_AUC":
            "DISTINCT_SCORE_GROUPED_NONINTERPOLATED_AVERAGE_PRECISION_FROM_PERSISTED_FLOAT32_PROBABILITIES",

        "tie_handling_for_auc":
            "ALL_IDENTICAL_FLOAT32_SCORES_ENTER_CURVE_SIMULTANEOUSLY",
    },

    "runtime": {
        "python":
            "3.12.13",

        "numpy":
            np.__version__,

        "torch":
            torch.__version__,

        "cuda_build":
            torch.version.cuda,

        "gpu":
            torch.cuda.get_device_name(0),

        "automatic_mixed_precision":
            False,

        "tf32":
            False,

        "deterministic_algorithms":
            True,

        "model_mode":
            "EVAL",

        "autograd":
            "INFERENCE_MODE_NO_GRAD",

        "batch_size_operational":
            256,
    },

    "scientific_boundary": {
        "Thursday_model_evaluation_performed":
            True,

        "Thursday_evaluation_passes":
            1,

        "Thursday_threshold_selection_performed":
            True,

        "thresholds_frozen_after_this_checkpoint":
            True,

        "model_retrained":
            False,

        "optimizer_steps_after_Stage21_2":
            0,

        "Friday_accessed":
            False,

        "Friday_status":
            "LOCKED_REUSE_BENCHMARK_NOT_YET_OPENED_FOR_STAGE21",
    },

    "next_checkpoint":
        "Stage21-4",
}


atomic_json(
    EVAL,
    evaluation,
)


print()
print("=" * 78)
print("STAGE21-3 LOCAL VALIDATION RESULT")
print("=" * 78)

print(
    "probabilities SHA256:",
    evaluation["probabilities"]["sha256"],
)

print(
    "ROC-AUC:",
    roc_auc,
)

print(
    "PR-AUC:",
    pr_auc,
)

print()
print(
    "standard threshold:",
    standard["threshold"],
)

print(
    "  F1:",
    standard["F1"],
    "Recall:",
    standard["Recall"],
    "FPR:",
    standard["FPR"],
)

print()
print(
    "balanced threshold:",
    balanced["threshold"],
)

print(
    "  F1:",
    balanced["F1"],
    "Recall:",
    balanced["Recall"],
    "FPR:",
    balanced["FPR"],
)

print()

if security is None:
    print("security threshold: UNAVAILABLE")
else:
    print(
        "security threshold:",
        security["threshold"],
    )

    print(
        "  F2:",
        security["F2"],
        "Recall:",
        security["Recall"],
        "FPR:",
        security["FPR"],
    )

print()
print("Thursday inference passes: 1")
print("Friday accessed: NO")
