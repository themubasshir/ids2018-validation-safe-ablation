
from pathlib import Path

import hashlib
import importlib.util
import json
import math
import os
import time

import numpy as np
import torch
from torch.nn import functional as F


# =============================================================================
# Frozen constants
# =============================================================================

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

OUT = (
    WORK
    / "stage21_xai1b_run"
)

OUT.mkdir(
    parents=True,
    exist_ok=True,
)


FRIDAY = (
    WORK
    / "stage20_compact_corpus"
    / "Friday"
)

COHORT_PATH = (
    RESULTS
    / "stage21_xai0_friday_cohort_indices.npy"
)

XAI0_LOCK = (
    RESULTS
    / "stage21_xai0_postresult_explainability_protocol_lock.json"
)

PREFLIGHT = (
    RESULTS
    / "stage21_xai1a_exact_preflight_receipt.json"
)


CNN_MODEL_PATH = (
    REPO
    / "results"
    / "stage20_1e_training"
    / "stage20_1e2_epoch10_model_state_dict.pt"
)

VIT_MODEL_PATH = (
    RESULTS
    / "stage21_2_epoch10_model_state_dict.pt"
)

CNN_MODULE_PATH = (
    REPO
    / "scripts"
    / "stage20_masked_cnn.py"
)

VIT_MODULE_PATH = (
    REPO
    / "scripts"
    / "stage21_masked_vit.py"
)

LOADER_MODULE_PATH = (
    REPO
    / "scripts"
    / "stage20_compact_corpus.py"
)


CNN_PROB_PATH = (
    REPO
    / "results"
    / "stage20_1e_training"
    / "stage20_1e4_friday_probabilities.npy"
)

VIT_PROB_PATH = (
    RESULTS
    / "stage21_4_friday_probabilities.npy"
)


RESULT_PATH = (
    OUT
    / "stage21_xai1b_integrated_gradients_result.json"
)

SUMMARY_PATH = (
    OUT
    / "stage21_xai1b_per_flow_summaries.npy"
)

PATCH_PATH = (
    OUT
    / "stage21_xai1b_patch_mass.npy"
)

ROW_PATH = (
    OUT
    / "stage21_xai1b_row_mass.npy"
)

BYTE_PATH = (
    OUT
    / "stage21_xai1b_byte_mass.npy"
)

HEATMAP_PATH = (
    OUT
    / "stage21_xai1b_class_mean_normalized_heatmap.npy"
)


EXPECTED_PREFLIGHT_PARENT = (
    "b26af9b8c54fda46f8b10c796d8bedbe8fca362f"
)

HARNESS_COMMIT = os.environ[
    "STAGE21_XAI_HARNESS_COMMIT"
]


EXPECTED_COHORT_SHA = (
    "ba29cf4611db82fa3c72b84f99ee537425c61c087c96ba96f02091f1156f83d8"
)

EXPECTED_LABEL_SHA = (
    "239b124119824fac23cff9fdcfbc24bc46227a0b6d4b1ad2201e955c263347d8"
)

EXPECTED_CNN_CHECKPOINT_SHA = (
    "3ebc71e579dc8e0e545981b2d60eea643148fe53e0902f8df8e47556243ad30b"
)

EXPECTED_CNN_STATE_SHA = (
    "ae9c913b13db62ab933198dd7721f0d1826b26a55773e3b560dc735cbb8c8092"
)

EXPECTED_CNN_MODULE_SHA = (
    "3638ae622017a36e6eeb33f227135829695ff2f3581c9b43787a02c1a440b9d4"
)

EXPECTED_VIT_CHECKPOINT_SHA = (
    "221e9c805fb663acacf2f0f2ca95dba7cb4b2ec4c4de5a3650cf4adeb99b5ef8"
)

EXPECTED_VIT_STATE_SHA = (
    "9da47df6cd5c821eef3d2c8a501296cd6070b835c719999f572f3dec2d560771"
)

EXPECTED_VIT_MODULE_SHA = (
    "3af99e4ea7061c68a676dc8fa7e485a7d13278f8947e4f8a8fbf2069dc31e3cb"
)

EXPECTED_LOADER_SHA = (
    "a1ba15881afeb1cf4de9225a06df9ae676b95f596c8ddced7734a445ba7624d0"
)

EXPECTED_CNN_PROB_SHA = (
    "e46a112e1e0320f645ec9d9502f0b3c0d8bdcf3987b50b2cd2352ef7484e2124"
)

EXPECTED_VIT_PROB_SHA = (
    "aeb24de4d40a56b7d69b2a8bedcca995e248f680f2e50b3fa3ee3db2a06f16ad"
)


ROWS = 64
COLS = 256

PATCH_ROWS = 8
PATCH_COLS = 16

GRID_ROWS = 8
GRID_COLS = 16

COHORT_N = 512

IG_STEPS = 64

FLOW_BATCH = 8
ALPHA_CHUNK = 8

assert IG_STEPS % ALPHA_CHUNK == 0

ENDPOINT_PROBABILITY_ABS_TOLERANCE = 1e-5

RELATIVE_COMPLETENESS_DENOMINATOR_FLOOR = 1e-12


MODEL_NAMES = [
    "CNN",
    "ViT",
]

SUMMARY_NAMES = [
    "LOGIT_INPUT",
    "LOGIT_ZERO_BASELINE",
    "IG_COMPLETENESS_RESIDUAL",
    "IG_RELATIVE_COMPLETENESS_ERROR",
    "PADDED_PIXEL_ATTRIBUTION_MASS_FRACTION",
    "NORMALIZED_VALID_PATCH_ENTROPY",
    "TOP1_PATCH_MASS_FRACTION",
    "TOP5_PATCH_MASS_FRACTION",
    "FIRST_16_PACKET_ROWS_MASS_FRACTION",
    "MIDDLE_32_PACKET_ROWS_MASS_FRACTION",
    "LAST_16_PACKET_ROWS_MASS_FRACTION",
]

SUMMARY_INDEX = {
    name: index
    for index, name
    in enumerate(
        SUMMARY_NAMES
    )
}


# =============================================================================
# Helpers
# =============================================================================

def sha256_file(
    path,
    block=16 * 1024 * 1024,
):

    h = hashlib.sha256()
    total = 0

    with Path(path).open(
        "rb"
    ) as fh:

        while True:

            data = fh.read(
                block
            )

            if not data:
                break

            h.update(
                data
            )

            total += len(
                data
            )

    return h.hexdigest(), total


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


def import_path(
    name,
    path,
):

    spec = (
        importlib.util
        .spec_from_file_location(
            name,
            str(path),
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


def stage20_canonical_state_sha256(
    state_dict,
):

    h = hashlib.sha256()

    for name in sorted(
        state_dict
    ):

        arr = (
            state_dict[name]
            .detach()
            .cpu()
            .contiguous()
            .numpy()
        )

        for piece in (
            name.encode(
                "utf-8"
            ),
            str(
                arr.dtype
            ).encode(
                "ascii"
            ),
            json.dumps(
                list(
                    arr.shape
                ),
                separators=(
                    ",",
                    ":",
                ),
            ).encode(
                "ascii"
            ),
            arr.tobytes(
                order="C"
            ),
        ):

            h.update(
                len(
                    piece
                ).to_bytes(
                    8,
                    "big",
                )
            )

            h.update(
                piece
            )

    return h.hexdigest()


def stage21_canonical_state_sha256(
    state,
):

    h = hashlib.sha256()

    for name in sorted(
        state.keys()
    ):

        array = (
            state[name]
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


def descriptive_stats(
    values,
):

    values = np.asarray(
        values,
        dtype=np.float64,
    )

    assert values.ndim == 1
    assert len(values) > 0
    assert np.all(
        np.isfinite(
            values
        )
    )

    return {
        "mean":
            float(
                np.mean(
                    values
                )
            ),

        "median":
            float(
                np.median(
                    values
                )
            ),

        "q25":
            float(
                np.quantile(
                    values,
                    0.25,
                    method="linear",
                )
            ),

        "q75":
            float(
                np.quantile(
                    values,
                    0.75,
                    method="linear",
                )
            ),

        "minimum":
            float(
                np.min(
                    values
                )
            ),

        "maximum":
            float(
                np.max(
                    values
                )
            ),
    }


# =============================================================================
# Frozen execution-code identity
# =============================================================================

SCRIPT_PATH = Path(
    __file__
).resolve()

SCRIPT_SHA, SCRIPT_BYTES = (
    sha256_file(
        SCRIPT_PATH
    )
)


# =============================================================================
# Runtime boundary
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


print("=" * 92)
print("STAGE21-XAI1B WORKER")
print("=" * 92)

print(
    "execution script SHA256:",
    SCRIPT_SHA,
)

print(
    "harness commit:",
    HARNESS_COMMIT,
)

print(
    "GPU:",
    torch.cuda.get_device_name(
        0
    ),
)


# =============================================================================
# Protocol/preflight gates
# =============================================================================

lock = json.loads(
    XAI0_LOCK.read_text(
        encoding="utf-8"
    )
)

preflight = json.loads(
    PREFLIGHT.read_text(
        encoding="utf-8"
    )
)


assert lock["checkpoint"] == "Stage21-XAI0"

assert (
    lock["status"]
    ==
    "POSTRESULT_EXPLAINABILITY_PROTOCOL_FROZEN_BEFORE_ATTRIBUTION_EXECUTION"
)

assert (
    lock["attribution"]["method"]
    ==
    "INTEGRATED_GRADIENTS"
)

assert (
    lock["attribution"]["integration_steps"]
    ==
    IG_STEPS
)

assert (
    lock["attribution"]["integration_rule"]
    ==
    "RIEMANN_MIDPOINT"
)

assert (
    lock["attribution"]["baseline"]
    ==
    "ALL_ZERO_NORMALIZED_IMAGE"
)

assert (
    lock["attribution"]["validity_mask_during_integration"]
    ==
    "FIXED_TO_ORIGINAL_FLOW_MASK"
)

assert (
    preflight["status"]
    ==
    "EXACT_XAI_PREFLIGHT_DURABLE_BEFORE_ANY_ATTRIBUTION"
)

assert (
    preflight[
        "scientific_boundary"
    ][
        "integrated_gradient_runs"
    ]
    ==
    0
)

assert (
    preflight[
        "scientific_boundary"
    ][
        "gradient_passes"
    ]
    ==
    0
)


# =============================================================================
# File identities
# =============================================================================

assert (
    sha256_file(
        COHORT_PATH
    )[0]
    ==
    EXPECTED_COHORT_SHA
)

assert (
    sha256_file(
        FRIDAY
        /
        "labels.npy"
    )[0]
    ==
    EXPECTED_LABEL_SHA
)

assert (
    sha256_file(
        CNN_MODEL_PATH
    )[0]
    ==
    EXPECTED_CNN_CHECKPOINT_SHA
)

assert (
    sha256_file(
        VIT_MODEL_PATH
    )[0]
    ==
    EXPECTED_VIT_CHECKPOINT_SHA
)

assert (
    sha256_file(
        CNN_MODULE_PATH
    )[0]
    ==
    EXPECTED_CNN_MODULE_SHA
)

assert (
    sha256_file(
        VIT_MODULE_PATH
    )[0]
    ==
    EXPECTED_VIT_MODULE_SHA
)

assert (
    sha256_file(
        LOADER_MODULE_PATH
    )[0]
    ==
    EXPECTED_LOADER_SHA
)

assert (
    sha256_file(
        CNN_PROB_PATH
    )[0]
    ==
    EXPECTED_CNN_PROB_SHA
)

assert (
    sha256_file(
        VIT_PROB_PATH
    )[0]
    ==
    EXPECTED_VIT_PROB_SHA
)


print()
print("Frozen input identities: PASS")


# =============================================================================
# Load cohort and exact compact representation
# =============================================================================

cohort_indices = np.load(
    COHORT_PATH,
    allow_pickle=False,
)

assert (
    cohort_indices.shape
    ==
    (
        COHORT_N,
    )
)

assert (
    cohort_indices.dtype
    ==
    np.int64
)

assert (
    len(
        np.unique(
            cohort_indices
        )
    )
    ==
    COHORT_N
)


loader_module = import_path(
    "stage20_compact_corpus_xai1b",
    LOADER_MODULE_PATH,
)

corpus = (
    loader_module
    .Stage20CompactCorpus(
        FRIDAY
    )
)


images = np.zeros(
    (
        COHORT_N,
        ROWS,
        COLS,
    ),
    dtype=np.uint8,
)

masks = np.zeros(
    (
        COHORT_N,
        ROWS,
        COLS,
    ),
    dtype=np.bool_,
)

labels = np.zeros(
    (
        COHORT_N,
    ),
    dtype=np.uint8,
)


for local_index, corpus_index in enumerate(
    cohort_indices.tolist()
):

    image, mask, label = (
        corpus.reconstruct(
            corpus_index
        )
    )

    images[
        local_index
    ] = image

    masks[
        local_index
    ] = mask

    labels[
        local_index
    ] = label


counts = np.bincount(
    labels,
    minlength=2,
)

assert int(
    counts[0]
) == 256

assert int(
    counts[1]
) == 256


print(
    "Locked 512-flow cohort reconstruction: PASS"
)


# =============================================================================
# Frozen model loading
# =============================================================================

cnn_module = import_path(
    "stage20_masked_cnn_xai1b",
    CNN_MODULE_PATH,
)

vit_module = import_path(
    "stage21_masked_vit_xai1b",
    VIT_MODULE_PATH,
)


cnn = (
    cnn_module
    .Stage20MaskedCNNv1()
)

vit = (
    vit_module
    .Stage21MaskedViTv1()
)


cnn_state = torch.load(
    CNN_MODEL_PATH,
    map_location="cpu",
    weights_only=True,
)

vit_state = torch.load(
    VIT_MODEL_PATH,
    map_location="cpu",
    weights_only=True,
)


assert (
    stage20_canonical_state_sha256(
        cnn_state
    )
    ==
    EXPECTED_CNN_STATE_SHA
)

assert (
    stage21_canonical_state_sha256(
        vit_state
    )
    ==
    EXPECTED_VIT_STATE_SHA
)


cnn.load_state_dict(
    cnn_state,
    strict=True,
)

vit.load_state_dict(
    vit_state,
    strict=True,
)


assert (
    cnn_module
    .count_trainable_parameters(
        cnn
    )
    ==
    93025
)

assert (
    vit_module
    .count_trainable_parameters(
        vit
    )
    ==
    91969
)


for model in (
    cnn,
    vit,
):

    model.eval()

    for parameter in model.parameters():

        parameter.requires_grad_(
            False
        )


    model.to(
        device
    )


print(
    "Frozen model identity/load gate: PASS"
)


# =============================================================================
# Common normalized attribution domain
#
# The Stage20 CNN's historical public forward() accepts storage-domain byte
# values and divides by 255 internally.
#
# XAI0 locked the attribution domain as normalized float32 [0,1].
#
# Therefore the CNN adapter starts immediately AFTER the historical /255 step
# and reproduces every remaining frozen operation exactly.
#
# ViT already consumes normalized float32 directly.
# =============================================================================

def cnn_normalized_forward(
    image,
    padding_mask,
):

    if image.ndim != 4:
        raise ValueError(
            "CNN normalized image must be NCHW"
        )

    if padding_mask.shape != image.shape:
        raise ValueError(
            "CNN normalized image/mask shape mismatch"
        )


    x = image.to(
        dtype=torch.float32
    )

    m = padding_mask.to(
        dtype=x.dtype
    )


    x = x * m


    x = cnn.conv1(
        x
    )

    x = cnn.norm1(
        x
    )

    x = F.relu(
        x,
        inplace=False,
    )

    x = F.max_pool2d(
        x,
        kernel_size=2,
        stride=2,
    )

    m = cnn._pool_mask(
        m
    )

    x = x * m


    x = cnn.conv2(
        x
    )

    x = cnn.norm2(
        x
    )

    x = F.relu(
        x,
        inplace=False,
    )

    x = F.max_pool2d(
        x,
        kernel_size=2,
        stride=2,
    )

    m = cnn._pool_mask(
        m
    )

    x = x * m


    x = cnn.conv3(
        x
    )

    x = cnn.norm3(
        x
    )

    x = F.relu(
        x,
        inplace=False,
    )

    x = F.max_pool2d(
        x,
        kernel_size=2,
        stride=2,
    )

    m = cnn._pool_mask(
        m
    )

    x = x * m


    denominator = m.sum(
        dim=(
            2,
            3,
        )
    ).clamp_min(
        1.0
    )


    pooled = (
        (
            x
            *
            m
        ).sum(
            dim=(
                2,
                3,
            )
        )
        /
        denominator
    )


    pooled = cnn.dropout(
        pooled
    )


    return cnn.classifier(
        pooled
    ).squeeze(
        1
    )


def vit_normalized_forward(
    image,
    padding_mask,
):

    return vit(
        image,
        padding_mask,
    )


FORWARD_FUNCTIONS = {
    "CNN":
        cnn_normalized_forward,

    "ViT":
        vit_normalized_forward,
}


FROZEN_PROBABILITIES = {
    "CNN":
        np.load(
            CNN_PROB_PATH,
            allow_pickle=False,
        ),

    "ViT":
        np.load(
            VIT_PROB_PATH,
            allow_pickle=False,
        ),
}


assert (
    FROZEN_PROBABILITIES[
        "CNN"
    ].shape
    ==
    (
        12088,
    )
)

assert (
    FROZEN_PROBABILITIES[
        "ViT"
    ].shape
    ==
    (
        12088,
    )
)


# =============================================================================
# Partial-output recovery helpers
# =============================================================================

def model_dir(
    model_name,
):

    directory = (
        OUT
        /
        model_name.lower()
    )

    directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    return directory


def model_paths(
    model_name,
):

    d = model_dir(
        model_name
    )

    return {
        "summary":
            d
            /
            "summary.npy",

        "patch":
            d
            /
            "patch.npy",

        "row":
            d
            /
            "row.npy",

        "byte":
            d
            /
            "byte.npy",

        "heatmap":
            d
            /
            "heatmap.npy",

        "status":
            d
            /
            "status.json",
    }


def verify_completed_model(
    model_name,
):

    paths = model_paths(
        model_name
    )

    if not paths[
        "status"
    ].is_file():

        return None


    status = json.loads(
        paths[
            "status"
        ].read_text(
            encoding="utf-8"
        )
    )


    if (
        status.get(
            "status"
        )
        !=
        "MODEL_LOCKED_IG_COMPLETE"
    ):

        return None


    assert (
        status[
            "execution_script_sha256"
        ]
        ==
        SCRIPT_SHA
    )


    for key in (
        "summary",
        "patch",
        "row",
        "byte",
        "heatmap",
    ):

        path = paths[
            key
        ]

        assert path.is_file()

        actual_sha, actual_bytes = (
            sha256_file(
                path
            )
        )

        expected = (
            status[
                "artifacts"
            ][
                key
            ]
        )

        assert (
            actual_sha
            ==
            expected[
                "sha256"
            ]
        )

        assert (
            actual_bytes
            ==
            expected[
                "bytes"
            ]
        )


    return status


# =============================================================================
# Model execution
# =============================================================================

def execute_model(
    model_name,
):

    existing = verify_completed_model(
        model_name
    )


    if existing is not None:

        print()
        print(
            model_name,
            "locked IG operational outputs already complete;"
            " reusing exact bytes.",
            flush=True,
        )

        return existing


    paths = model_paths(
        model_name
    )


    # Reject partial products without a valid completion receipt.
    for key in (
        "summary",
        "patch",
        "row",
        "byte",
        "heatmap",
    ):

        if paths[
            key
        ].exists():

            paths[
                key
            ].unlink()


    if paths[
        "status"
    ].exists():

        paths[
            "status"
        ].unlink()


    forward_fn = (
        FORWARD_FUNCTIONS[
            model_name
        ]
    )


    frozen_probability_vector = (
        FROZEN_PROBABILITIES[
            model_name
        ]
    )


    summary = np.zeros(
        (
            COHORT_N,
            len(
                SUMMARY_NAMES
            ),
        ),
        dtype=np.float64,
    )


    patch_mass = np.zeros(
        (
            COHORT_N,
            GRID_ROWS,
            GRID_COLS,
        ),
        dtype=np.float32,
    )


    row_mass = np.zeros(
        (
            COHORT_N,
            ROWS,
        ),
        dtype=np.float32,
    )


    byte_mass = np.zeros(
        (
            COHORT_N,
            COLS,
        ),
        dtype=np.float32,
    )


    heatmap_sum = np.zeros(
        (
            2,
            ROWS,
            COLS,
        ),
        dtype=np.float64,
    )


    endpoint_input_logits = np.zeros(
        (
            COHORT_N,
        ),
        dtype=np.float32,
    )

    endpoint_zero_logits = np.zeros(
        (
            COHORT_N,
        ),
        dtype=np.float32,
    )


    start_time = time.time()

    forward_invocations = 0
    gradient_autograd_calls = 0


    # ---------------------------------------------------------------------
    # Endpoint consistency gate FIRST.
    #
    # This verifies that the frozen normalized execution path reproduces
    # the already-sealed Friday probabilities before any gradient is taken.
    # ---------------------------------------------------------------------

    print()
    print("=" * 88)
    print(
        model_name,
        "ENDPOINT CONSISTENCY GATE"
    )
    print("=" * 88)


    with torch.inference_mode():

        for start in range(
            0,
            COHORT_N,
            FLOW_BATCH,
        ):

            end = min(
                start
                +
                FLOW_BATCH,
                COHORT_N,
            )


            x = (
                torch.from_numpy(
                    np.ascontiguousarray(
                        images[
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
                        masks[
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


            input_logits = forward_fn(
                x,
                m,
            )

            forward_invocations += 1


            zero_logits = forward_fn(
                torch.zeros_like(
                    x
                ),
                m,
            )

            forward_invocations += 1


            endpoint_input_logits[
                start:
                end
            ] = (
                input_logits
                .detach()
                .cpu()
                .numpy()
                .astype(
                    np.float32,
                    copy=False,
                )
            )


            endpoint_zero_logits[
                start:
                end
            ] = (
                zero_logits
                .detach()
                .cpu()
                .numpy()
                .astype(
                    np.float32,
                    copy=False,
                )
            )


    endpoint_probabilities = (
        1.0
        /
        (
            1.0
            +
            np.exp(
                -endpoint_input_logits.astype(
                    np.float64
                )
            )
        )
    ).astype(
        np.float32
    )


    frozen_cohort_probabilities = (
        frozen_probability_vector[
            cohort_indices
        ].astype(
            np.float32,
            copy=False,
        )
    )


    endpoint_abs_difference = np.abs(
        endpoint_probabilities.astype(
            np.float64
        )
        -
        frozen_cohort_probabilities.astype(
            np.float64
        )
    )


    endpoint_max_abs_difference = float(
        np.max(
            endpoint_abs_difference
        )
    )


    endpoint_mean_abs_difference = float(
        np.mean(
            endpoint_abs_difference
        )
    )


    print(
        "maximum |recomputed - frozen probability|:",
        endpoint_max_abs_difference,
    )

    print(
        "mean    |recomputed - frozen probability|:",
        endpoint_mean_abs_difference,
    )

    print(
        "frozen tolerance:",
        ENDPOINT_PROBABILITY_ABS_TOLERANCE,
    )


    assert (
        endpoint_max_abs_difference
        <=
        ENDPOINT_PROBABILITY_ABS_TOLERANCE
    ), (
        model_name,
        endpoint_max_abs_difference,
    )


    print(
        model_name,
        "endpoint consistency: PASS",
        flush=True,
    )


    # ---------------------------------------------------------------------
    # Locked midpoint IG.
    # ---------------------------------------------------------------------

    print()
    print("=" * 88)
    print(
        model_name,
        "64-STEP MIDPOINT INTEGRATED GRADIENTS"
    )
    print("=" * 88)


    alphas = (
        (
            torch.arange(
                IG_STEPS,
                device=device,
                dtype=torch.float32,
            )
            +
            0.5
        )
        /
        float(
            IG_STEPS
        )
    )


    for start in range(
        0,
        COHORT_N,
        FLOW_BATCH,
    ):

        end = min(
            start
            +
            FLOW_BATCH,
            COHORT_N,
        )

        B = end - start


        x = (
            torch.from_numpy(
                np.ascontiguousarray(
                    images[
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
                    masks[
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


        grad_sum = torch.zeros_like(
            x
        )


        for alpha_start in range(
            0,
            IG_STEPS,
            ALPHA_CHUNK,
        ):

            alpha_end = (
                alpha_start
                +
                ALPHA_CHUNK
            )


            alpha_chunk = alphas[
                alpha_start:
                alpha_end
            ]


            C = int(
                alpha_chunk.numel()
            )


            scaled = (
                x[
                    :,
                    None,
                    :,
                    :,
                    :,
                ]
                *
                alpha_chunk[
                    None,
                    :,
                    None,
                    None,
                    None,
                ]
            )


            scaled = (
                scaled
                .reshape(
                    B
                    *
                    C,
                    1,
                    ROWS,
                    COLS,
                )
                .clone()
                .detach()
                .requires_grad_(
                    True
                )
            )


            repeated_mask = (
                m[
                    :,
                    None,
                    :,
                    :,
                    :,
                ]
                .expand(
                    B,
                    C,
                    1,
                    ROWS,
                    COLS,
                )
                .reshape(
                    B
                    *
                    C,
                    1,
                    ROWS,
                    COLS,
                )
            )


            logits = forward_fn(
                scaled,
                repeated_mask,
            )

            forward_invocations += 1


            gradients = torch.autograd.grad(
                outputs=logits.sum(),
                inputs=scaled,
                create_graph=False,
                retain_graph=False,
                only_inputs=True,
            )[0]

            gradient_autograd_calls += 1


            gradients = gradients.reshape(
                B,
                C,
                1,
                ROWS,
                COLS,
            )


            grad_sum = (
                grad_sum
                +
                gradients.sum(
                    dim=1
                )
            )


        average_gradient = (
            grad_sum
            /
            float(
                IG_STEPS
            )
        )


        # zero baseline => (x - 0) * average gradient
        ig = (
            x
            *
            average_gradient
        )


        signed_sum = ig.sum(
            dim=(
                1,
                2,
                3,
            )
        )


        input_logits = torch.from_numpy(
            endpoint_input_logits[
                start:
                end
            ]
        ).to(
            device=device,
            dtype=torch.float32,
        )


        zero_logits = torch.from_numpy(
            endpoint_zero_logits[
                start:
                end
            ]
        ).to(
            device=device,
            dtype=torch.float32,
        )


        logit_delta = (
            input_logits
            -
            zero_logits
        )


        residual = (
            signed_sum
            -
            logit_delta
        )


        relative_error = (
            residual.abs()
            /
            logit_delta.abs().clamp_min(
                RELATIVE_COMPLETENESS_DENOMINATOR_FLOOR
            )
        )


        abs_ig = ig.abs()

        spatial = abs_ig[
            :,
            0,
            :,
            :,
        ]


        mask_spatial = m[
            :,
            0,
            :,
            :,
        ]


        total_mass = spatial.sum(
            dim=(
                1,
                2,
            )
        )


        padded_mass = (
            spatial
            *
            (
                ~mask_spatial
            ).to(
                dtype=spatial.dtype
            )
        ).sum(
            dim=(
                1,
                2,
            )
        )


        mass_denominator = (
            total_mass.clamp_min(
                1e-30
            )
        )


        padded_fraction = (
            padded_mass
            /
            mass_denominator
        )


        patch = (
            spatial
            .reshape(
                B,
                GRID_ROWS,
                PATCH_ROWS,
                GRID_COLS,
                PATCH_COLS,
            )
            .sum(
                dim=(
                    2,
                    4,
                )
            )
        )


        patch_valid = (
            mask_spatial
            .reshape(
                B,
                GRID_ROWS,
                PATCH_ROWS,
                GRID_COLS,
                PATCH_COLS,
            )
            .any(
                dim=2
            )
            .any(
                dim=3
            )
        )


        rows = spatial.sum(
            dim=2
        )

        columns = spatial.sum(
            dim=1
        )


        normalized_spatial = (
            spatial
            /
            mass_denominator[
                :,
                None,
                None,
            ]
        )


        # If total mass is exactly zero, normalized map is defined as zero.
        zero_mass = (
            total_mass
            <=
            0
        )


        if bool(
            zero_mass.any()
        ):

            normalized_spatial[
                zero_mass
            ] = 0.0


        # -------------------------------------------------------------
        # Per-flow patch concentration and entropy.
        # -------------------------------------------------------------

        patch_np = (
            patch
            .detach()
            .cpu()
            .numpy()
            .astype(
                np.float32,
                copy=False,
            )
        )


        patch_valid_np = (
            patch_valid
            .detach()
            .cpu()
            .numpy()
        )


        total_mass_np = (
            total_mass
            .detach()
            .cpu()
            .numpy()
            .astype(
                np.float64,
                copy=False,
            )
        )


        entropy_np = np.zeros(
            B,
            dtype=np.float64,
        )

        top1_np = np.zeros(
            B,
            dtype=np.float64,
        )

        top5_np = np.zeros(
            B,
            dtype=np.float64,
        )


        for local in range(
            B
        ):

            mass_total = float(
                total_mass_np[
                    local
                ]
            )


            valid_flat = (
                patch_valid_np[
                    local
                ].reshape(
                    -1
                )
            )


            valid_masses = (
                patch_np[
                    local
                ].reshape(
                    -1
                )[
                    valid_flat
                ].astype(
                    np.float64,
                    copy=False,
                )
            )


            K = int(
                valid_masses.size
            )


            if (
                mass_total
                <=
                0.0
                or
                K
                ==
                0
            ):

                continue


            probabilities = (
                valid_masses
                /
                mass_total
            )


            positive = (
                probabilities
                >
                0.0
            )


            if (
                K
                >
                1
            ):

                entropy = -float(
                    np.sum(
                        probabilities[
                            positive
                        ]
                        *
                        np.log(
                            probabilities[
                                positive
                            ]
                        ),
                        dtype=np.float64,
                    )
                )


                entropy_np[
                    local
                ] = (
                    entropy
                    /
                    math.log(
                        K
                    )
                )


            sorted_masses = np.sort(
                valid_masses
            )


            top1_np[
                local
            ] = (
                float(
                    sorted_masses[
                        -1
                    ]
                )
                /
                mass_total
            )


            top_k = min(
                5,
                K,
            )


            top5_np[
                local
            ] = (
                float(
                    np.sum(
                        sorted_masses[
                            -top_k:
                        ],
                        dtype=np.float64,
                    )
                )
                /
                mass_total
            )


        # -------------------------------------------------------------
        # Row-region fractions.
        # -------------------------------------------------------------

        first16 = spatial[
            :,
            0:16,
            :,
        ].sum(
            dim=(
                1,
                2,
            )
        )


        middle32 = spatial[
            :,
            16:48,
            :,
        ].sum(
            dim=(
                1,
                2,
            )
        )


        last16 = spatial[
            :,
            48:64,
            :,
        ].sum(
            dim=(
                1,
                2,
            )
        )


        first16_fraction = (
            first16
            /
            mass_denominator
        )

        middle32_fraction = (
            middle32
            /
            mass_denominator
        )

        last16_fraction = (
            last16
            /
            mass_denominator
        )


        if bool(
            zero_mass.any()
        ):

            first16_fraction[
                zero_mass
            ] = 0.0

            middle32_fraction[
                zero_mass
            ] = 0.0

            last16_fraction[
                zero_mass
            ] = 0.0


        # -------------------------------------------------------------
        # Persist batch-level aggregates to CPU arrays.
        # -------------------------------------------------------------

        patch_mass[
            start:
            end
        ] = patch_np


        row_mass[
            start:
            end
        ] = (
            rows
            .detach()
            .cpu()
            .numpy()
            .astype(
                np.float32,
                copy=False,
            )
        )


        byte_mass[
            start:
            end
        ] = (
            columns
            .detach()
            .cpu()
            .numpy()
            .astype(
                np.float32,
                copy=False,
            )
        )


        summary[
            start:
            end,
            SUMMARY_INDEX[
                "LOGIT_INPUT"
            ],
        ] = endpoint_input_logits[
            start:
            end
        ].astype(
            np.float64
        )


        summary[
            start:
            end,
            SUMMARY_INDEX[
                "LOGIT_ZERO_BASELINE"
            ],
        ] = endpoint_zero_logits[
            start:
            end
        ].astype(
            np.float64
        )


        summary[
            start:
            end,
            SUMMARY_INDEX[
                "IG_COMPLETENESS_RESIDUAL"
            ],
        ] = (
            residual
            .detach()
            .cpu()
            .numpy()
            .astype(
                np.float64,
                copy=False,
            )
        )


        summary[
            start:
            end,
            SUMMARY_INDEX[
                "IG_RELATIVE_COMPLETENESS_ERROR"
            ],
        ] = (
            relative_error
            .detach()
            .cpu()
            .numpy()
            .astype(
                np.float64,
                copy=False,
            )
        )


        summary[
            start:
            end,
            SUMMARY_INDEX[
                "PADDED_PIXEL_ATTRIBUTION_MASS_FRACTION"
            ],
        ] = (
            padded_fraction
            .detach()
            .cpu()
            .numpy()
            .astype(
                np.float64,
                copy=False,
            )
        )


        summary[
            start:
            end,
            SUMMARY_INDEX[
                "NORMALIZED_VALID_PATCH_ENTROPY"
            ],
        ] = entropy_np


        summary[
            start:
            end,
            SUMMARY_INDEX[
                "TOP1_PATCH_MASS_FRACTION"
            ],
        ] = top1_np


        summary[
            start:
            end,
            SUMMARY_INDEX[
                "TOP5_PATCH_MASS_FRACTION"
            ],
        ] = top5_np


        summary[
            start:
            end,
            SUMMARY_INDEX[
                "FIRST_16_PACKET_ROWS_MASS_FRACTION"
            ],
        ] = (
            first16_fraction
            .detach()
            .cpu()
            .numpy()
            .astype(
                np.float64,
                copy=False,
            )
        )


        summary[
            start:
            end,
            SUMMARY_INDEX[
                "MIDDLE_32_PACKET_ROWS_MASS_FRACTION"
            ],
        ] = (
            middle32_fraction
            .detach()
            .cpu()
            .numpy()
            .astype(
                np.float64,
                copy=False,
            )
        )


        summary[
            start:
            end,
            SUMMARY_INDEX[
                "LAST_16_PACKET_ROWS_MASS_FRACTION"
            ],
        ] = (
            last16_fraction
            .detach()
            .cpu()
            .numpy()
            .astype(
                np.float64,
                copy=False,
            )
        )


        normalized_np = (
            normalized_spatial
            .detach()
            .cpu()
            .numpy()
            .astype(
                np.float64,
                copy=False,
            )
        )


        local_labels = labels[
            start:
            end
        ]


        for class_value in (
            0,
            1,
        ):

            select = (
                local_labels
                ==
                class_value
            )


            if np.any(
                select
            ):

                heatmap_sum[
                    class_value
                ] += np.sum(
                    normalized_np[
                        select
                    ],
                    axis=0,
                    dtype=np.float64,
                )


        completed = end


        if (
            completed
            %
            64
            ==
            0
            or
            completed
            ==
            COHORT_N
        ):

            elapsed = (
                time.time()
                -
                start_time
            )

            print(
                f"  {model_name}: "
                f"{completed:3d}/{COHORT_N} flows "
                f"elapsed={elapsed:.2f}s",
                flush=True,
            )


    # ---------------------------------------------------------------------
    # Final model-level checks.
    # ---------------------------------------------------------------------

    assert np.all(
        np.isfinite(
            summary
        )
    )

    assert np.all(
        np.isfinite(
            patch_mass
        )
    )

    assert np.all(
        np.isfinite(
            row_mass
        )
    )

    assert np.all(
        np.isfinite(
            byte_mass
        )
    )


    class_counts = np.bincount(
        labels,
        minlength=2,
    ).astype(
        np.float64
    )


    heatmap = (
        heatmap_sum
        /
        class_counts[
            :,
            None,
            None,
        ]
    )


    assert np.all(
        np.isfinite(
            heatmap
        )
    )


    # Aggregate mass identity.
    patch_totals = patch_mass.sum(
        axis=(
            1,
            2,
        ),
        dtype=np.float64,
    )

    row_totals = row_mass.sum(
        axis=1,
        dtype=np.float64,
    )

    byte_totals = byte_mass.sum(
        axis=1,
        dtype=np.float64,
    )


    assert np.allclose(
        patch_totals,
        row_totals,
        rtol=2e-5,
        atol=2e-6,
    )

    assert np.allclose(
        patch_totals,
        byte_totals,
        rtol=2e-5,
        atol=2e-6,
    )


    # -------------------------------------------------------------
    # Persist operational model result.
    # -------------------------------------------------------------

    save_npy_atomic(
        paths[
            "summary"
        ],
        summary,
    )

    save_npy_atomic(
        paths[
            "patch"
        ],
        patch_mass,
    )

    save_npy_atomic(
        paths[
            "row"
        ],
        row_mass,
    )

    save_npy_atomic(
        paths[
            "byte"
        ],
        byte_mass,
    )

    save_npy_atomic(
        paths[
            "heatmap"
        ],
        heatmap,
    )


    artifact_records = {}


    for key in (
        "summary",
        "patch",
        "row",
        "byte",
        "heatmap",
    ):

        digest, size = (
            sha256_file(
                paths[
                    key
                ]
            )
        )

        artifact_records[
            key
        ] = {
            "sha256":
                digest,

            "bytes":
                size,
        }


    elapsed = (
        time.time()
        -
        start_time
    )


    status = {
        "status":
            "MODEL_LOCKED_IG_COMPLETE",

        "model":
            model_name,

        "execution_script_sha256":
            SCRIPT_SHA,

        "harness_commit":
            HARNESS_COMMIT,

        "cohort_flows":
            COHORT_N,

        "IG_steps_per_flow":
            IG_STEPS,

        "integration_rule":
            "RIEMANN_MIDPOINT",

        "baseline":
            "ALL_ZERO_NORMALIZED_IMAGE",

        "validity_mask":
            "FIXED_ORIGINAL_MASK",

        "gradient_flow_alpha_evaluations":
            COHORT_N
            *
            IG_STEPS,

        "gradient_autograd_calls":
            gradient_autograd_calls,

        "endpoint_flow_evaluations":
            COHORT_N
            *
            2,

        "batched_forward_invocations":
            forward_invocations,

        "endpoint_probability_gate": {
            "absolute_tolerance":
                ENDPOINT_PROBABILITY_ABS_TOLERANCE,

            "maximum_absolute_difference":
                endpoint_max_abs_difference,

            "mean_absolute_difference":
                endpoint_mean_abs_difference,

            "passed":
                True,
        },

        "artifacts":
            artifact_records,

        "elapsed_seconds_operational":
            elapsed,

        "scientific_boundary": {
            "threshold_search":
                False,

            "threshold_reselection":
                False,

            "model_retraining":
                False,

            "optimizer_steps":
                0,

            "attribution_method_search":
                False,

            "alternative_baseline":
                False,
        },
    }


    atomic_json(
        paths[
            "status"
        ],
        status,
    )


    print()
    print(
        model_name,
        "LOCKED IG COMPLETE",
        flush=True,
    )

    print(
        "  gradient flow-alpha evaluations:",
        status[
            "gradient_flow_alpha_evaluations"
        ],
        flush=True,
    )

    print(
        "  endpoint probability max abs difference:",
        endpoint_max_abs_difference,
        flush=True,
    )


    return status


# =============================================================================
# Execute in frozen order: CNN then ViT
# =============================================================================

cnn_status = execute_model(
    "CNN"
)

vit_status = execute_model(
    "ViT"
)


# =============================================================================
# Load exact completed model artifacts
# =============================================================================

model_arrays = {}


for model_name in MODEL_NAMES:

    paths = model_paths(
        model_name
    )

    status = verify_completed_model(
        model_name
    )

    assert status is not None


    model_arrays[
        model_name
    ] = {
        "summary":
            np.load(
                paths[
                    "summary"
                ],
                allow_pickle=False,
            ),

        "patch":
            np.load(
                paths[
                    "patch"
                ],
                allow_pickle=False,
            ),

        "row":
            np.load(
                paths[
                    "row"
                ],
                allow_pickle=False,
            ),

        "byte":
            np.load(
                paths[
                    "byte"
                ],
                allow_pickle=False,
            ),

        "heatmap":
            np.load(
                paths[
                    "heatmap"
                ],
                allow_pickle=False,
            ),
    }


# =============================================================================
# Combined frozen-axis artifacts
#
# model axis:
#   0 = CNN
#   1 = ViT
#
# class axis in heatmap:
#   0 = TRUE_BENIGN
#   1 = TRUE_ATTACK
# =============================================================================

combined_summary = np.stack(
    [
        model_arrays[
            "CNN"
        ][
            "summary"
        ],

        model_arrays[
            "ViT"
        ][
            "summary"
        ],
    ],
    axis=1,
).astype(
    np.float64,
    copy=False,
)


combined_patch = np.stack(
    [
        model_arrays[
            "CNN"
        ][
            "patch"
        ],

        model_arrays[
            "ViT"
        ][
            "patch"
        ],
    ],
    axis=1,
).astype(
    np.float32,
    copy=False,
)


combined_row = np.stack(
    [
        model_arrays[
            "CNN"
        ][
            "row"
        ],

        model_arrays[
            "ViT"
        ][
            "row"
        ],
    ],
    axis=1,
).astype(
    np.float32,
    copy=False,
)


combined_byte = np.stack(
    [
        model_arrays[
            "CNN"
        ][
            "byte"
        ],

        model_arrays[
            "ViT"
        ][
            "byte"
        ],
    ],
    axis=1,
).astype(
    np.float32,
    copy=False,
)


combined_heatmap = np.stack(
    [
        model_arrays[
            "CNN"
        ][
            "heatmap"
        ],

        model_arrays[
            "ViT"
        ][
            "heatmap"
        ],
    ],
    axis=0,
).astype(
    np.float64,
    copy=False,
)


assert (
    combined_summary.shape
    ==
    (
        512,
        2,
        11,
    )
)

assert (
    combined_patch.shape
    ==
    (
        512,
        2,
        8,
        16,
    )
)

assert (
    combined_row.shape
    ==
    (
        512,
        2,
        64,
    )
)

assert (
    combined_byte.shape
    ==
    (
        512,
        2,
        256,
    )
)

assert (
    combined_heatmap.shape
    ==
    (
        2,
        2,
        64,
        256,
    )
)


save_npy_atomic(
    SUMMARY_PATH,
    combined_summary,
)

save_npy_atomic(
    PATCH_PATH,
    combined_patch,
)

save_npy_atomic(
    ROW_PATH,
    combined_row,
)

save_npy_atomic(
    BYTE_PATH,
    combined_byte,
)

save_npy_atomic(
    HEATMAP_PATH,
    combined_heatmap,
)


# =============================================================================
# Predeclared descriptive summaries
# =============================================================================

model_axis = {
    "CNN":
        0,

    "ViT":
        1,
}


strata = {
    "TRUE_BENIGN":
        (
            labels
            ==
            0
        ),

    "TRUE_ATTACK":
        (
            labels
            ==
            1
        ),
}


descriptive = {}


for model_name in MODEL_NAMES:

    model_index = (
        model_axis[
            model_name
        ]
    )

    descriptive[
        model_name
    ] = {}


    for stratum_name, selector in strata.items():

        descriptive[
            model_name
        ][
            stratum_name
        ] = {}


        for metric_index, metric_name in enumerate(
            SUMMARY_NAMES
        ):

            values = combined_summary[
                selector,
                model_index,
                metric_index,
            ]


            descriptive[
                model_name
            ][
                stratum_name
            ][
                metric_name
            ] = descriptive_stats(
                values
            )


# =============================================================================
# Paired ViT-minus-CNN summaries on same flows
# =============================================================================

paired = {}


for stratum_name, selector in strata.items():

    paired[
        stratum_name
    ] = {}


    for metric_index, metric_name in enumerate(
        SUMMARY_NAMES
    ):

        delta = (
            combined_summary[
                selector,
                1,
                metric_index,
            ]
            -
            combined_summary[
                selector,
                0,
                metric_index,
            ]
        )


        paired[
            stratum_name
        ][
            metric_name
        ] = descriptive_stats(
            delta
        )


# =============================================================================
# Final artifact audit
# =============================================================================

artifact_paths = {
    "per_flow_summaries":
        SUMMARY_PATH,

    "patch_mass":
        PATCH_PATH,

    "row_mass":
        ROW_PATH,

    "byte_mass":
        BYTE_PATH,

    "class_mean_normalized_heatmap":
        HEATMAP_PATH,
}


artifact_records = {}


for name, path in artifact_paths.items():

    digest, size = sha256_file(
        path
    )

    artifact_records[
        name
    ] = {
        "path":
            "results/stage21_architecture/"
            +
            path.name,

        "sha256":
            digest,

        "bytes":
            size,
    }


result = {
    "checkpoint":
        "Stage21-XAI1B",

    "status":
        "LOCKED_POSTRESULT_INTEGRATED_GRADIENTS_COMPLETE",

    "preflight_parent_commit":
        EXPECTED_PREFLIGHT_PARENT,

    "execution_harness_commit":
        HARNESS_COMMIT,

    "execution_script_sha256":
        SCRIPT_SHA,

    "study_role":
        "POSTRESULT_DESCRIPTIVE_ONLY",

    "Friday_role":
        "LOCKED_REUSE_BENCHMARK_NON_CONFIRMATORY",

    "cohort": {
        "flows":
            COHORT_N,

        "true_benign":
            256,

        "true_attack":
            256,

        "indices_sha256":
            EXPECTED_COHORT_SHA,

        "selection":
            "TRUE_LABEL_ONLY",
    },

    "attribution": {
        "method":
            "INTEGRATED_GRADIENTS",

        "target":
            "ATTACK_LOGIT_PRE_SIGMOID",

        "baseline":
            "ALL_ZERO_NORMALIZED_IMAGE",

        "validity_mask":
            "FIXED_ORIGINAL_FLOW_MASK",

        "integration_path":
            "STRAIGHT_LINE",

        "integration_rule":
            "RIEMANN_MIDPOINT",

        "steps":
            IG_STEPS,

        "dtype":
            "FLOAT32",

        "CNN_normalized_adapter":
            (
                "STARTS_IMMEDIATELY_AFTER_FROZEN_STAGE20_INTERNAL_DIV255;"
                "ALL_SUBSEQUENT_FROZEN_CNN_OPERATIONS_UNCHANGED"
            ),

        "ViT_normalized_adapter":
            "DIRECT_FROZEN_STAGE21_FORWARD",
    },

    "quality_definition": {
        "IG_COMPLETENESS_RESIDUAL":
            (
                "SUM_SIGNED_IG_MINUS_"
                "(INPUT_LOGIT_MINUS_ZERO_BASELINE_LOGIT)"
            ),

        "IG_RELATIVE_COMPLETENESS_ERROR":
            (
                "ABS_COMPLETENESS_RESIDUAL_DIVIDED_BY_"
                "MAX(ABS_LOGIT_DELTA,1E-12)"
            ),

        "PADDED_PIXEL_ATTRIBUTION_MASS_FRACTION":
            (
                "ABS_IG_MASS_ON_FALSE_MASK_PIXELS_DIVIDED_BY_"
                "TOTAL_ABS_IG_MASS"
            ),

        "NORMALIZED_VALID_PATCH_ENTROPY":
            (
                "SHANNON_ENTROPY_OF_ABS_IG_MASS_ACROSS_VALID_8x16_PATCHES"
                "_DIVIDED_BY_LOG(NUM_VALID_PATCHES);"
                "DEFINED_ZERO_WHEN_LEQ_ONE_VALID_PATCH_OR_ZERO_TOTAL_MASS"
            ),

        "TOP5_PATCH_RULE":
            (
                "SUM_LARGEST_MIN(5,NUM_VALID_PATCHES)_VALID_PATCH_MASSES"
                "_DIVIDED_BY_TOTAL_ABS_IG_MASS"
            ),
    },

    "artifact_axes": {
        "per_flow_summaries":
            [
                "FLOW_512",
                "MODEL_[CNN,ViT]",
                "METRIC_11",
            ],

        "patch_mass":
            [
                "FLOW_512",
                "MODEL_[CNN,ViT]",
                "PATCH_ROW_8",
                "PATCH_COL_16",
            ],

        "row_mass":
            [
                "FLOW_512",
                "MODEL_[CNN,ViT]",
                "PACKET_ROW_64",
            ],

        "byte_mass":
            [
                "FLOW_512",
                "MODEL_[CNN,ViT]",
                "BYTE_POSITION_256",
            ],

        "class_mean_normalized_heatmap":
            [
                "MODEL_[CNN,ViT]",
                "TRUE_CLASS_[BENIGN,ATTACK]",
                "PACKET_ROW_64",
                "BYTE_POSITION_256",
            ],
    },

    "summary_metric_names":
        SUMMARY_NAMES,

    "model_execution": {
        "CNN":
            cnn_status,

        "ViT":
            vit_status,
    },

    "descriptive_by_true_class":
        descriptive,

    "paired_ViT_minus_CNN_by_true_class":
        paired,

    "artifacts":
        artifact_records,

    "scientific_boundary": {
        "architecture_result_changed":
            False,

        "model_selected_from_XAI":
            False,

        "threshold_search":
            False,

        "threshold_reselection":
            False,

        "training":
            False,

        "optimizer_steps":
            0,

        "attribution_method_search":
            False,

        "alternative_baseline":
            False,

        "cohort_changed":
            False,

        "examples_selected_by_visual_appeal":
            False,

        "causal_claim":
            False,

        "independent_confirmation_claim":
            False,

        "general_ViT_superiority_claim":
            False,

        "post_result_explainability":
            True,
    },
}


atomic_json(
    RESULT_PATH,
    result,
)


# =============================================================================
# Visible frozen descriptive output
# =============================================================================

print()
print("=" * 92)
print("STAGE21-XAI1B LOCKED IG RESULT")
print("=" * 92)


for stratum in (
    "TRUE_BENIGN",
    "TRUE_ATTACK",
):

    print()
    print(stratum)

    for metric in (
        "IG_RELATIVE_COMPLETENESS_ERROR",
        "PADDED_PIXEL_ATTRIBUTION_MASS_FRACTION",
        "NORMALIZED_VALID_PATCH_ENTROPY",
        "TOP1_PATCH_MASS_FRACTION",
        "TOP5_PATCH_MASS_FRACTION",
        "FIRST_16_PACKET_ROWS_MASS_FRACTION",
        "MIDDLE_32_PACKET_ROWS_MASS_FRACTION",
        "LAST_16_PACKET_ROWS_MASS_FRACTION",
    ):

        cnn_median = (
            descriptive[
                "CNN"
            ][
                stratum
            ][
                metric
            ][
                "median"
            ]
        )

        vit_median = (
            descriptive[
                "ViT"
            ][
                stratum
            ][
                metric
            ][
                "median"
            ]
        )

        delta_median = (
            paired[
                stratum
            ][
                metric
            ][
                "median"
            ]
        )


        print(
            f"  {metric}:"
        )

        print(
            "    CNN median:",
            cnn_median,
        )

        print(
            "    ViT median:",
            vit_median,
        )

        print(
            "    paired ViT-CNN median:",
            delta_median,
        )


print()
print("Artifacts:")

for name, record in artifact_records.items():

    print(
        f"  {name}:"
    )

    print(
        "    bytes:",
        record[
            "bytes"
        ],
    )

    print(
        "    SHA256:",
        record[
            "sha256"
        ],
    )


print()
print("Threshold search:         NO")
print("Threshold reselection:    NO")
print("Training:                 NO")
print("Architecture search:      NO")
print("Attribution method search:NO")
print("Alternative baseline:     NO")
print("Optimizer steps:          0")

print("=" * 92)
