
from pathlib import Path

import hashlib
import importlib.util
import json
import os

import numpy as np
import torch


WORK = Path("/kaggle/working")

REPO = (
    WORK
    / "ids2018-validation-safe-ablation"
)

RESULTS = (
    REPO
    / "results"
    / "stage21_architecture"
)

FRIDAY = (
    WORK
    / "stage20_compact_corpus"
    / "Friday"
)

OUT = (
    WORK
    / "stage21_friday_eval"
)

OUT.mkdir(
    parents=True,
    exist_ok=True,
)


MODEL = (
    RESULTS
    / "stage21_2_epoch10_model_state_dict.pt"
)

VIT_MODULE = (
    REPO
    / "scripts"
    / "stage21_masked_vit.py"
)

LOADER_MODULE = (
    REPO
    / "scripts"
    / "stage20_compact_corpus.py"
)

S3 = (
    RESULTS
    / "stage21_3_remote_seal_receipt.json"
)


PROBS = (
    OUT
    / "stage21_4_friday_probabilities.npy"
)

EVAL = (
    OUT
    / "stage21_4_friday_reuse_evaluation.json"
)


PARENT = (
    "f35fb3cf259b6bab34c8f622f59266e24cb2b32e"
)

MODEL_SHA = (
    "221e9c805fb663acacf2f0f2ca95dba7cb4b2ec4c4de5a3650cf4adeb99b5ef8"
)

MODEL_STATE_SHA = (
    "9da47df6cd5c821eef3d2c8a501296cd6070b835c719999f572f3dec2d560771"
)

VIT_SHA = (
    "3af99e4ea7061c68a676dc8fa7e485a7d13278f8947e4f8a8fbf2069dc31e3cb"
)

LOADER_SHA = (
    "a1ba15881afeb1cf4de9225a06df9ae676b95f596c8ddced7734a445ba7624d0"
)


EXPECTED_COMPACT = {
    "encoded_bytes.bin": (
        8679226,
        "f6dd1900f2767edc20a112b9f9875b3410667c3dace1dd2ff729cb3ce37952d2",
    ),

    "flow_offsets.npy": (
        96840,
        "5e66ab4e85eb21eca8c7ea36c45461e1ac1f21d25acb0fb812c2221db02917aa",
    ),

    "labels.npy": (
        12216,
        "239b124119824fac23cff9fdcfbc24bc46227a0b6d4b1ad2201e955c263347d8",
    ),

    "packet_lengths.npy": (
        1547392,
        "f1790f6e9ddc9f24954cf72eb72359c7052e8736cdb97516afff74b7805ba878",
    ),
}


def sha256_file(
    path,
):

    h = hashlib.sha256()

    total = 0

    with Path(path).open(
        "rb"
    ) as fh:

        while True:

            block = fh.read(
                16 * 1024 * 1024
            )

            if not block:
                break

            h.update(
                block
            )

            total += len(
                block
            )

    return (
        h.hexdigest(),
        total,
    )


def import_path(
    name,
    path,
):

    spec = (
        importlib.util
        .spec_from_file_location(
            name,
            path,
        )
    )

    assert spec is not None
    assert spec.loader is not None

    module = (
        importlib.util
        .module_from_spec(
            spec
        )
    )

    spec.loader.exec_module(
        module
    )

    return module


def save_npy_atomic(
    path,
    array,
):

    tmp = Path(
        str(path)
        +
        ".tmp"
    )

    with tmp.open(
        "wb"
    ) as fh:

        np.save(
            fh,
            array,
            allow_pickle=False,
        )


    os.replace(
        tmp,
        path,
    )


def atomic_json(
    path,
    obj,
):

    tmp = Path(
        str(path)
        +
        ".tmp"
    )

    tmp.write_text(
        json.dumps(
            obj,
            indent=2,
            sort_keys=True,
        )
        +
        "\n",
        encoding="utf-8",
    )

    os.replace(
        tmp,
        path,
    )


def canonical_state_sha256(
    state,
):

    h = hashlib.sha256()


    for name in sorted(
        state.keys()
    ):

        array = (
            state[
                name
            ]
            .detach()
            .cpu()
            .contiguous()
            .numpy()
        )


        name_bytes = (
            name.encode(
                "utf-8"
            )
        )

        dtype_bytes = (
            str(
                array.dtype
            ).encode(
                "ascii"
            )
        )


        h.update(
            len(
                name_bytes
            ).to_bytes(
                4,
                "little",
            )
        )

        h.update(
            name_bytes
        )


        h.update(
            len(
                dtype_bytes
            ).to_bytes(
                2,
                "little",
            )
        )

        h.update(
            dtype_bytes
        )


        h.update(
            np.asarray(
                array.shape,
                dtype=np.int64,
            ).tobytes()
        )


        h.update(
            array.tobytes(
                order="C"
            )
        )


    return h.hexdigest()


# =============================================================================
# Exact frozen runtime
# =============================================================================

assert np.__version__ == "2.4.6"

assert (
    torch.__version__
    ==
    "2.10.0+cu126"
)

assert (
    torch.version.cuda
    ==
    "12.6"
)

assert torch.cuda.is_available()

assert (
    os.environ[
        "CUBLAS_WORKSPACE_CONFIG"
    ]
    ==
    ":4096:8"
)


torch.backends.cudnn.benchmark = False
torch.backends.cudnn.deterministic = True

torch.backends.cuda.matmul.allow_tf32 = False
torch.backends.cudnn.allow_tf32 = False

torch.use_deterministic_algorithms(
    True
)

torch.set_float32_matmul_precision(
    "highest"
)


device = torch.device(
    "cuda"
)


# =============================================================================
# Frozen files and thresholds
# =============================================================================

assert (
    sha256_file(
        MODEL
    )[0]
    ==
    MODEL_SHA
)

assert (
    sha256_file(
        VIT_MODULE
    )[0]
    ==
    VIT_SHA
)

assert (
    sha256_file(
        LOADER_MODULE
    )[0]
    ==
    LOADER_SHA
)


stage21_3 = json.loads(
    S3.read_text(
        encoding="utf-8"
    )
)


assert (
    stage21_3[
        "scientific_boundary"
    ][
        "thresholds_frozen"
    ]
    is True
)


assert (
    stage21_3[
        "scientific_boundary"
    ][
        "Friday_accessed"
    ]
    is False
)


assert (
    stage21_3[
        "operating_points"
    ][
        "standard"
    ][
        "metrics"
    ][
        "threshold_integer_percent"
    ]
    ==
    50
)


assert (
    stage21_3[
        "operating_points"
    ][
        "balanced"
    ][
        "metrics"
    ][
        "threshold_integer_percent"
    ]
    ==
    42
)


assert (
    stage21_3[
        "operating_points"
    ][
        "security"
    ][
        "metrics"
    ][
        "threshold_integer_percent"
    ]
    ==
    24
)


for (
    name,
    (
        expected_size,
        expected_sha,
    ),
) in (
    EXPECTED_COMPACT.items()
):

    actual_sha, actual_size = (
        sha256_file(
            FRIDAY
            /
            name
        )
    )

    assert (
        actual_size
        ==
        expected_size
    )

    assert (
        actual_sha
        ==
        expected_sha
    )


# =============================================================================
# Exact dense reconstruction
# =============================================================================

encoded = np.fromfile(
    FRIDAY
    / "encoded_bytes.bin",
    dtype=np.uint8,
)


lengths = np.load(
    FRIDAY
    / "packet_lengths.npy",
    allow_pickle=False,
)


offsets = np.load(
    FRIDAY
    / "flow_offsets.npy",
    allow_pickle=False,
)


labels = np.load(
    FRIDAY
    / "labels.npy",
    allow_pickle=False,
)


assert (
    lengths.shape
    ==
    (
        12088,
        64,
    )
)

assert (
    offsets.shape
    ==
    (
        12089,
    )
)

assert (
    labels.shape
    ==
    (
        12088,
    )
)

assert (
    labels.dtype
    ==
    np.uint8
)


assert (
    int(
        offsets[
            0
        ]
    )
    ==
    0
)

assert (
    int(
        offsets[
            -1
        ]
    )
    ==
    len(
        encoded
    )
)


counts = np.bincount(
    labels,
    minlength=2,
)


assert (
    int(
        counts[
            0
        ]
    )
    ==
    6486
)

assert (
    int(
        counts[
            1
        ]
    )
    ==
    5602
)


cols = np.arange(
    256,
    dtype=np.uint16,
)[
    None,
    None,
    :
]


mask = (
    cols
    <
    lengths[
        :,
        :,
        None,
    ]
)


assert (
    int(
        mask.sum()
    )
    ==
    len(
        encoded
    )
)


image = np.zeros(
    (
        12088,
        64,
        256,
    ),
    dtype=np.uint8,
)


image[
    mask
] = encoded


loader_module = import_path(
    "stage20_compact_corpus_s21e4",
    LOADER_MODULE,
)


official = (
    loader_module
    .Stage20CompactCorpus(
        FRIDAY
    )
)


for index in range(
    128
):

    official_image, official_mask, official_label = (
        official.reconstruct(
            index
        )
    )


    assert np.array_equal(
        image[
            index
        ],
        official_image,
    )


    assert np.array_equal(
        mask[
            index
        ],
        official_mask,
    )


    assert (
        int(
            labels[
                index
            ]
        )
        ==
        int(
            official_label
        )
    )


print(
    "Friday dense reconstruction ↔ frozen loader first128: PASS",
    flush=True,
)


# =============================================================================
# ONE model inference pass
# =============================================================================

inference_performed_this_run = False


if not PROBS.exists():

    assert not EVAL.exists()


    vit_module = import_path(
        "stage21_masked_vit_s21e4",
        VIT_MODULE,
    )


    model = (
        vit_module
        .Stage21MaskedViTv1()
    )


    assert (
        vit_module
        .count_trainable_parameters(
            model
        )
        ==
        91969
    )


    state = torch.load(
        MODEL,
        map_location="cpu",
        weights_only=True,
    )


    assert (
        canonical_state_sha256(
            state
        )
        ==
        MODEL_STATE_SHA
    )


    model.load_state_dict(
        state,
        strict=True,
    )


    model.to(
        device
    )

    model.eval()


    batches = []

    BATCH = 256


    with torch.inference_mode():

        for start in range(
            0,
            12088,
            BATCH,
        ):

            end = min(
                start
                +
                BATCH,
                12088,
            )


            x = (
                torch.from_numpy(
                    np.ascontiguousarray(
                        image[
                            start:
                            end
                        ]
                    )
                )
                .to(
                    device=device,
                    dtype=torch.float32,
                )
                .unsqueeze(
                    1
                )
                .div_(
                    255.0
                )
            )


            m = (
                torch.from_numpy(
                    np.ascontiguousarray(
                        mask[
                            start:
                            end
                        ]
                    )
                )
                .to(
                    device=device,
                    dtype=torch.bool,
                )
                .unsqueeze(
                    1
                )
            )


            logits = model(
                x,
                m,
            )


            probabilities_batch = (
                torch.sigmoid(
                    logits
                )
                .to(
                    dtype=torch.float32
                )
                .cpu()
                .numpy()
                .astype(
                    np.float32,
                    copy=False,
                )
            )


            batches.append(
                probabilities_batch
            )


    probabilities = np.concatenate(
        batches
    ).astype(
        np.float32,
        copy=False,
    )


    assert (
        probabilities.shape
        ==
        (
            12088,
        )
    )

    assert (
        probabilities.dtype
        ==
        np.float32
    )

    assert np.all(
        np.isfinite(
            probabilities
        )
    )


    # Persist immediately BEFORE metric/document/git work.
    save_npy_atomic(
        PROBS,
        probabilities,
    )


    inference_performed_this_run = True


    print(
        "Friday Stage21 ViT inference passes: 1",
        flush=True,
    )


else:

    probabilities = np.load(
        PROBS,
        allow_pickle=False,
    )


    assert (
        probabilities.shape
        ==
        (
            12088,
        )
    )

    assert (
        probabilities.dtype
        ==
        np.float32
    )

    assert np.all(
        np.isfinite(
            probabilities
        )
    )


    print(
        "Existing persisted Friday probabilities detected: "
        "NO additional model inference",
        flush=True,
    )


# =============================================================================
# Fixed operating points ONLY
# =============================================================================

def operating_metrics(
    threshold_integer_percent,
):

    threshold = (
        threshold_integer_percent
        /
        100.0
    )


    prediction = (
        probabilities
        >=
        threshold
    )


    positive = (
        labels
        ==
        1
    )

    negative = ~positive


    TP = int(
        np.count_nonzero(
            prediction
            &
            positive
        )
    )

    FP = int(
        np.count_nonzero(
            prediction
            &
            negative
        )
    )

    TN = int(
        np.count_nonzero(
            (~prediction)
            &
            negative
        )
    )

    FN = int(
        np.count_nonzero(
            (~prediction)
            &
            positive
        )
    )


    n = (
        TP
        +
        TN
        +
        FP
        +
        FN
    )


    precision = (
        TP
        /
        (
            TP
            +
            FP
        )
        if (
            TP
            +
            FP
        )
        else 0.0
    )


    recall = (
        TP
        /
        (
            TP
            +
            FN
        )
        if (
            TP
            +
            FN
        )
        else 0.0
    )


    f1_den = (
        2
        *
        TP
        +
        FP
        +
        FN
    )


    f1 = (
        2
        *
        TP
        /
        f1_den
        if f1_den
        else 0.0
    )


    f2_den = (
        5
        *
        TP
        +
        FP
        +
        4
        *
        FN
    )


    f2 = (
        5
        *
        TP
        /
        f2_den
        if f2_den
        else 0.0
    )


    fpr = (
        FP
        /
        (
            FP
            +
            TN
        )
        if (
            FP
            +
            TN
        )
        else 0.0
    )


    fnr = (
        FN
        /
        (
            FN
            +
            TP
        )
        if (
            FN
            +
            TP
        )
        else 0.0
    )


    return {
        "threshold_integer_percent":
            int(
                threshold_integer_percent
            ),

        "threshold":
            float(
                threshold
            ),

        "prediction_rule":
            "ATTACK_IF_FLOAT32_SIGMOID_PROBABILITY_GTE_THRESHOLD",

        "TP":
            TP,

        "TN":
            TN,

        "FP":
            FP,

        "FN":
            FN,

        "Accuracy":
            (
                TP
                +
                TN
            )
            /
            n,

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


    sorted_y = y[
        order
    ]

    sorted_score = score[
        order
    ]


    positives = int(
        np.count_nonzero(
            y
            ==
            1
        )
    )

    negatives = int(
        np.count_nonzero(
            y
            ==
            0
        )
    )


    assert positives > 0
    assert negatives > 0


    tp = 0
    fp = 0

    previous_tp = 0
    previous_fp = 0


    roc_area_numerator = 0.0

    average_precision = 0.0


    index = 0

    count = len(
        y
    )


    while index < count:

        end = (
            index
            +
            1
        )


        while (
            end
            <
            count
            and
            sorted_score[
                end
            ]
            ==
            sorted_score[
                index
            ]
        ):

            end += 1


        group = sorted_y[
            index:
            end
        ]


        group_tp = int(
            np.count_nonzero(
                group
                ==
                1
            )
        )


        group_fp = int(
            (
                end
                -
                index
            )
            -
            group_tp
        )


        tp += group_tp

        fp += group_fp


        roc_area_numerator += (
            (
                fp
                -
                previous_fp
            )
            *
            (
                tp
                +
                previous_tp
            )
            /
            2.0
        )


        if group_tp:

            recall_delta = (
                tp
                -
                previous_tp
            ) / positives


            precision = (
                tp
                /
                (
                    tp
                    +
                    fp
                )
            )


            average_precision += (
                recall_delta
                *
                precision
            )


        previous_tp = tp

        previous_fp = fp

        index = end


    return (
        float(
            roc_area_numerator
            /
            (
                positives
                *
                negatives
            )
        ),

        float(
            average_precision
        ),
    )


standard = operating_metrics(
    50
)

balanced = operating_metrics(
    42
)

security = operating_metrics(
    24
)


roc_auc, pr_auc = grouped_auc(
    labels,
    probabilities,
)


evaluation = {
    "checkpoint":
        "Stage21-4",

    "status":
        "FRIDAY_LOCKED_REUSE_BENCHMARK_EVALUATED_ONCE_WITH_NO_SELECTION",

    "parent_commit":
        PARENT,

    "role": {
        "day":
            "Friday",

        "designation":
            "LOCKED_REUSE_BENCHMARK_NON_CONFIRMATORY",

        "independent_confirmation":
            False,

        "known_before_stage21_lock":
            True,

        "selection_permitted":
            False,
    },

    "model": {
        "name":
            "Stage21MaskedViTv1",

        "epoch":
            10,

        "checkpoint_sha256":
            MODEL_SHA,

        "canonical_state_sha256":
            MODEL_STATE_SHA,

        "retrained_after_stage21_3":
            False,
    },

    "population": {
        "flows":
            12088,

        "benign":
            6486,

        "attack":
            5602,
    },

    "probabilities": {
        "path":
            "results/stage21_architecture/"
            "stage21_4_friday_probabilities.npy",

        "shape":
            [
                12088
            ],

        "dtype":
            "float32",

        "sha256":
            sha256_file(
                PROBS
            )[0],
    },

    "score_metrics": {
        "ROC_AUC":
            roc_auc,

        "PR_AUC":
            pr_auc,

        "ROC_AUC_definition":
            "DISTINCT_SCORE_GROUPED_TRAPEZOIDAL_ROC_AREA_FROM_PERSISTED_FLOAT32_PROBABILITIES",

        "PR_AUC_definition":
            "DISTINCT_SCORE_GROUPED_NONINTERPOLATED_AVERAGE_PRECISION_FROM_PERSISTED_FLOAT32_PROBABILITIES",
    },

    "operating_points": {
        "standard": {
            "source":
                "FIXED_0_50",

            "metrics":
                standard,
        },

        "balanced": {
            "source":
                "THURSDAY_FROZEN_STAGE21_3",

            "metrics":
                balanced,
        },

        "security": {
            "source":
                "THURSDAY_FROZEN_STAGE21_3",

            "metrics":
                security,
        },
    },

    "scientific_boundary": {
        "Friday_model_inference_passes_total":
            1,

        "Friday_model_inference_performed_this_run":
            inference_performed_this_run,

        "Friday_threshold_grid_evaluated":
            False,

        "Friday_threshold_search":
            False,

        "Friday_threshold_reselection":
            False,

        "Friday_model_retraining":
            False,

        "optimizer_steps":
            0,

        "architecture_change":
            False,

        "representation_change":
            False,

        "join_change":
            False,
    },
}


atomic_json(
    EVAL,
    evaluation,
)


print()
print("=" * 88)
print("STAGE21-4 FRIDAY LOCKED REUSE RESULT")
print("=" * 88)

print(
    "ROC-AUC:",
    roc_auc,
)

print(
    "PR-AUC: ",
    pr_auc,
)


for (
    name,
    record,
) in (
    (
        "standard",
        standard,
    ),

    (
        "balanced",
        balanced,
    ),

    (
        "security",
        security,
    ),
):

    print()
    print(
        name,
        "threshold",
        record[
            "threshold"
        ],
    )

    print(
        "  TP/FN/TN/FP:",
        record[
            "TP"
        ],
        record[
            "FN"
        ],
        record[
            "TN"
        ],
        record[
            "FP"
        ],
    )

    print(
        "  Precision:",
        record[
            "Precision"
        ],
    )

    print(
        "  Recall:   ",
        record[
            "Recall"
        ],
    )

    print(
        "  F1:       ",
        record[
            "F1"
        ],
    )

    print(
        "  F2:       ",
        record[
            "F2"
        ],
    )

    print(
        "  FPR:      ",
        record[
            "FPR"
        ],
    )


print()
print("Friday threshold grid:        NO")
print("Friday threshold search:      NO")
print("Friday threshold reselection: NO")
print("Training:                     NO")
print("Optimizer steps:              0")

print("=" * 88)
