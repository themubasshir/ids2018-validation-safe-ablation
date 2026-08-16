
from __future__ import annotations

from pathlib import Path
from collections import OrderedDict
import gc
import hashlib
import importlib.util
import json
import math
import os
import platform
import random
import re
import subprocess
import time
import urllib.error
import urllib.parse
import urllib.request

import numpy as np
import torch


# =============================================================================
# Frozen constants
# =============================================================================

WORK = Path("/kaggle/working")

REPO = (
    WORK
    / "ids2018-validation-safe-ablation"
)

CORPUS_ROOT = (
    WORK
    / "stage20_compact_corpus"
)

OUT = (
    WORK
    / "stage21_training"
)

OUT.mkdir(
    parents=True,
    exist_ok=True,
)


EXPECTED_HEAD = (
    "de15ff09907c5a0fdecbd51cc457a28adb80bb3f"
)


PROTOCOL = (
    REPO
    / "results"
    / "stage21_architecture"
    / "stage21_0_cnn_vit_followup_protocol_lock.json"
)

EXPECTED_PROTOCOL_SHA = (
    "1a60a0e6b12e88e9c8ceefb83278b71011b4fa396e821c22a093b69fcdb364f5"
)


VIT_MODULE = (
    REPO
    / "scripts"
    / "stage21_masked_vit.py"
)

EXPECTED_VIT_SHA = (
    "3af99e4ea7061c68a676dc8fa7e485a7d13278f8947e4f8a8fbf2069dc31e3cb"
)


LOADER_MODULE = (
    REPO
    / "scripts"
    / "stage20_compact_corpus.py"
)

EXPECTED_LOADER_SHA = (
    "a1ba15881afeb1cf4de9225a06df9ae676b95f596c8ddced7734a445ba7624d0"
)


RUNTIME_RECEIPT = (
    OUT
    / "stage21_2_exact_runtime_preflight.json"
)

EXPECTED_RUNTIME_RECEIPT_SHA = (
    "b730b0b16175828ce299f1b5021048516e436c032532c55ccd68827141817d81"
)


TRAIN_DAYS = (
    "Monday",
    "Tuesday",
    "Wednesday",
)


EXPECTED_COUNTS = {

    "Monday": (
        528_509,
        528_509,
        0,
    ),

    "Tuesday": (
        4_170,
        4_008,
        162,
    ),

    "Wednesday": (
        12_951,
        8_657,
        4_294,
    ),
}


TOTAL = 545_630

TRAIN_BENIGN = 541_174
TRAIN_ATTACK = 4_456

POS_WEIGHT = 121.448384201077

SEED = 42

EPOCHS = 10
BATCH_SIZE = 256

BATCHES_PER_EPOCH = 2_132
FINAL_BATCH_SIZE = 94
TOTAL_OPTIMIZER_STEPS = 21_320


EXPECTED_PERMUTATION_SHA = [

    "de1012063844a04591311c784c6c1584a9f2c793f3a4354490f6dca7a03a6ee4",

    "6b894f543574743120b96e9f4416f4776c32e1199290fb2028df268bba54fccb",

    "7f5637f40b719404e6b4c36c95f600ce177dcfe4c9dece2fc02f4066a9fa6e11",

    "45b0b51470f80057624b2b53952b82ea72740af39233262beba01a2e83f0d449",

    "2276345b5b7097fd7d591894ecaa5e20ad3fbc84b138459e1e7daaa63cb332c8",

    "13b2aa847368c7cc50516cbb92c98a22bb4763e0a82649bddc7da49b1905c36a",

    "4ac3216ab2e7e18c28ce74141f9329485f1d9f0a217c2bbf5ca5045719cb324a",

    "90d8d64698703698d24dee7ac0338dc5f3a7f68cad34fdb3a7f9fd325ef779dc",

    "bd90520ca905011e7a68f282c1b9a8c78061fd7d496c9b74a792c487f982a250",

    "160a700ce25fbe9134b5ad2f86532b6d35d443f25dd9d234fa9781131a70705e",
]


FINAL_STATE = (
    OUT
    / "stage21_2_epoch10_model_state_dict.pt"
)

FINAL_MANIFEST = (
    OUT
    / "stage21_2_training_manifest.json"
)


RECOVERY_RELEASE_TAG = (
    "stage21-2-training-recovery-v1"
)

RECOVERY_RELEASE_NAME = (
    "Stage21-2 Training Recovery"
)


# =============================================================================
# Helpers
# =============================================================================

def sha256_file(path):

    h = hashlib.sha256()

    with Path(path).open("rb") as f:

        while True:

            b = f.read(
                16 * 1024 * 1024
            )

            if not b:
                break

            h.update(b)

    return h.hexdigest()


def git(*args):

    r = subprocess.run(
        ["git", *args],
        cwd=REPO,
        text=True,
        capture_output=True,
    )

    if r.returncode != 0:

        raise RuntimeError(
            r.stdout
            +
            "\n"
            +
            r.stderr
        )

    return r.stdout.strip()


def import_path(
    name,
    path,
):

    spec = importlib.util.spec_from_file_location(
        name,
        path,
    )

    mod = importlib.util.module_from_spec(
        spec
    )

    spec.loader.exec_module(
        mod
    )

    return mod


def canonical_state_sha256(
    model,
):

    h = hashlib.sha256()


    for name in sorted(
        model.state_dict().keys()
    ):

        tensor = (
            model.state_dict()[name]
            .detach()
            .cpu()
            .contiguous()
        )

        array = tensor.numpy()


        nb = name.encode(
            "utf-8"
        )

        db = str(
            array.dtype
        ).encode(
            "ascii"
        )


        h.update(
            len(nb).to_bytes(
                4,
                "little",
            )
        )

        h.update(nb)

        h.update(
            len(db).to_bytes(
                2,
                "little",
            )
        )

        h.update(db)

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


def mem_available_bytes():

    for line in Path(
        "/proc/meminfo"
    ).read_text().splitlines():

        if line.startswith(
            "MemAvailable:"
        ):

            return (
                int(
                    line.split()[1]
                )
                *
                1024
            )

    return 0


# =============================================================================
# GitHub API helpers
# =============================================================================

TOKEN = os.environ.get(
    "GITHUB_TOKEN"
)

assert TOKEN


API_BASE = (
    "https://api.github.com/repos/"
    "themubasshir/"
    "ids2018-validation-safe-ablation"
)


def github_request(
    method,
    url,
    *,
    data=None,
    content_type=None,
    accept="application/vnd.github+json",
):

    headers = {

        "Authorization":
            f"Bearer {TOKEN}",

        "Accept":
            accept,

        "X-GitHub-Api-Version":
            "2022-11-28",

        "User-Agent":
            "stage21-training-recovery",
    }


    if content_type:

        headers[
            "Content-Type"
        ] = content_type


    req = urllib.request.Request(
        url,
        data=data,
        headers=headers,
        method=method,
    )


    return urllib.request.urlopen(
        req,
        timeout=300,
    )


def github_json(
    method,
    url,
    *,
    payload=None,
):

    data = None

    if payload is not None:

        data = json.dumps(
            payload
        ).encode(
            "utf-8"
        )


    with github_request(
        method,
        url,
        data=data,
        content_type=(
            "application/json"
            if data is not None
            else None
        ),
    ) as r:

        raw = r.read()


    if not raw:
        return None


    return json.loads(
        raw.decode(
            "utf-8"
        )
    )


def ensure_recovery_release():

    url = (
        API_BASE
        +
        "/releases/tags/"
        +
        RECOVERY_RELEASE_TAG
    )


    try:

        return github_json(
            "GET",
            url,
        )


    except urllib.error.HTTPError as e:

        if e.code != 404:
            raise


    release = github_json(
        "POST",
        API_BASE
        +
        "/releases",

        payload={

            "tag_name":
                RECOVERY_RELEASE_TAG,

            "target_commitish":
                EXPECTED_HEAD,

            "name":
                RECOVERY_RELEASE_NAME,

            "body":
                (
                    "Operational Stage21-2 epoch-boundary "
                    "recovery checkpoints. Not scientific "
                    "model-selection artifacts."
                ),

            "draft":
                False,

            "prerelease":
                True,
        },
    )


    return release


def refresh_release():

    return github_json(
        "GET",
        API_BASE
        +
        "/releases/tags/"
        +
        RECOVERY_RELEASE_TAG,
    )


def latest_remote_recovery():

    release = refresh_release()


    pattern = re.compile(
        r"^stage21-2-recovery-epoch(\d{2})\.pt$"
    )


    choices = []


    for asset in release.get(
        "assets",
        []
    ):

        m = pattern.match(
            asset["name"]
        )

        if not m:
            continue


        choices.append(
            (
                int(
                    m.group(1)
                ),
                asset,
            )
        )


    if not choices:
        return None


    return max(
        choices,
        key=lambda x: x[0],
    )


def download_asset(
    asset,
    destination,
):

    req = urllib.request.Request(
        asset["url"],
        headers={

            "Authorization":
                f"Bearer {TOKEN}",

            "Accept":
                "application/octet-stream",

            "User-Agent":
                "stage21-training-recovery",
        },
    )


    with urllib.request.urlopen(
        req,
        timeout=300,
    ) as r:

        data = r.read()


    Path(
        destination
    ).write_bytes(
        data
    )


def upload_recovery(
    epoch_number,
    path,
):

    release = refresh_release()


    asset_name = (
        f"stage21-2-recovery-epoch"
        f"{epoch_number:02d}.pt"
    )


    # Idempotent rerun protection.
    for asset in release.get(
        "assets",
        []
    ):

        if (
            asset["name"]
            ==
            asset_name
        ):

            local_sha = sha256_file(
                path
            )

            digest = asset.get(
                "digest"
            )


            if digest:

                assert (
                    digest
                    ==
                    "sha256:"
                    +
                    local_sha
                )


            print(
                f"  remote recovery epoch "
                f"{epoch_number}: ALREADY DURABLE",
                flush=True,
            )

            return asset


    upload_base = (
        release[
            "upload_url"
        ].split(
            "{"
        )[0]
    )


    upload_url = (
        upload_base
        +
        "?"
        +
        urllib.parse.urlencode(
            {
                "name":
                    asset_name
            }
        )
    )


    raw = Path(
        path
    ).read_bytes()


    last_error = None


    for attempt in range(
        1,
        6,
    ):

        try:

            with github_request(
                "POST",
                upload_url,
                data=raw,
                content_type=(
                    "application/octet-stream"
                ),
            ) as r:

                asset = json.loads(
                    r.read().decode(
                        "utf-8"
                    )
                )


            assert (
                int(
                    asset["size"]
                )
                ==
                len(raw)
            )


            local_sha = hashlib.sha256(
                raw
            ).hexdigest()


            if asset.get(
                "digest"
            ):

                assert (
                    asset["digest"]
                    ==
                    "sha256:"
                    +
                    local_sha
                )


            print(
                f"  remote recovery epoch "
                f"{epoch_number}: PASS "
                f"(asset {asset['id']})",
                flush=True,
            )

            return asset


        except Exception as exc:

            last_error = exc

            print(
                f"  recovery upload attempt "
                f"{attempt}/5 failed: {exc}",
                flush=True,
            )

            time.sleep(
                2
                *
                attempt
            )


    raise last_error


# =============================================================================
# Start / exact runtime
# =============================================================================

print("=" * 78)
print("STAGE21-2 — FAST FROZEN ViT TRAINING")
print("=" * 78)


print()
print("Runtime:")
print("  Python:", platform.python_version())
print("  NumPy: ", np.__version__)
print("  Torch: ", torch.__version__)
print("  CUDA:  ", torch.version.cuda)
print("  GPU:   ", torch.cuda.get_device_name(0))


assert platform.python_version() == "3.12.13"
assert np.__version__ == "2.4.6"
assert torch.__version__ == "2.10.0+cu126"
assert torch.version.cuda == "12.6"
assert torch.cuda.is_available()

assert (
    os.environ[
        "CUBLAS_WORKSPACE_CONFIG"
    ]
    ==
    ":4096:8"
)


# =============================================================================
# Small immutable gates only — NO giant corpus rehash
# =============================================================================

assert git(
    "rev-parse",
    "HEAD",
) == EXPECTED_HEAD

assert git(
    "status",
    "--porcelain",
) == ""


assert (
    sha256_file(
        PROTOCOL
    )
    ==
    EXPECTED_PROTOCOL_SHA
)

assert (
    sha256_file(
        VIT_MODULE
    )
    ==
    EXPECTED_VIT_SHA
)

assert (
    sha256_file(
        LOADER_MODULE
    )
    ==
    EXPECTED_LOADER_SHA
)

assert (
    sha256_file(
        RUNTIME_RECEIPT
    )
    ==
    EXPECTED_RUNTIME_RECEIPT_SHA
)


print()
print(
    "Immutable protocol/code/runtime gates: PASS"
)


# =============================================================================
# Determinism
# =============================================================================

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
# Load TRAIN compact arrays once
# =============================================================================

print()
print("=" * 78)
print("LOADING FROZEN TRAIN POPULATION")
print("=" * 78)


encoded_parts = []
length_parts = []
label_parts = []
offset_parts = []

encoded_base = 0


for day in TRAIN_DAYS:

    d = (
        CORPUS_ROOT
        /
        day
    )

    assert d.is_dir()


    encoded = np.fromfile(
        d
        /
        "encoded_bytes.bin",
        dtype=np.uint8,
    )


    lengths = np.load(
        d
        /
        "packet_lengths.npy",
        allow_pickle=False,
    )


    labels = np.load(
        d
        /
        "labels.npy",
        allow_pickle=False,
    )


    offsets = np.load(
        d
        /
        "flow_offsets.npy",
        allow_pickle=False,
    )


    n_expected, b_expected, a_expected = (
        EXPECTED_COUNTS[
            day
        ]
    )


    assert labels.shape == (
        n_expected,
    )

    assert lengths.shape == (
        n_expected,
        64,
    )

    counts = np.bincount(
        labels,
        minlength=2,
    )


    assert int(
        counts[0]
    ) == b_expected

    assert int(
        counts[1]
    ) == a_expected


    assert int(
        offsets[0]
    ) == 0

    assert int(
        offsets[-1]
    ) == len(
        encoded
    )


    encoded_parts.append(
        encoded
    )

    length_parts.append(
        lengths
    )

    label_parts.append(
        labels
    )


    offset_parts.append(
        (
            offsets[
                1:
            ].astype(
                np.uint64,
                copy=False,
            )
            +
            np.uint64(
                encoded_base
            )
        )
    )


    encoded_base += len(
        encoded
    )


    print(
        f"  {day:<9}"
        f" flows={n_expected:,}"
        f" benign={b_expected:,}"
        f" attack={a_expected:,}",
        flush=True,
    )


encoded = np.concatenate(
    encoded_parts
)

lengths = np.concatenate(
    length_parts,
    axis=0,
)

labels = np.concatenate(
    label_parts,
    axis=0,
)

flow_offsets = np.concatenate(
    [
        np.array(
            [0],
            dtype=np.uint64,
        ),
        *offset_parts,
    ]
)


del encoded_parts
del length_parts
del label_parts
del offset_parts


assert labels.shape == (
    TOTAL,
)

assert lengths.shape == (
    TOTAL,
    64,
)

assert flow_offsets.shape == (
    TOTAL + 1,
)


counts = np.bincount(
    labels,
    minlength=2,
)


assert int(
    counts[0]
) == TRAIN_BENIGN

assert int(
    counts[1]
) == TRAIN_ATTACK


print()
print(
    f"Combined TRAIN: "
    f"{TOTAL:,} flows | "
    f"{TRAIN_BENIGN:,} benign | "
    f"{TRAIN_ATTACK:,} attack"
)


# =============================================================================
# Permutation identities — fast, before training
# =============================================================================

for epoch0 in range(
    EPOCHS
):

    p = (
        np.random.default_rng(
            SEED
            +
            epoch0
        )
        .permutation(
            TOTAL
        )
    )


    h = hashlib.sha256(
        p.tobytes()
    ).hexdigest()


    assert (
        h
        ==
        EXPECTED_PERMUTATION_SHA[
            epoch0
        ]
    )


print(
    "All 10 frozen permutation identities: PASS"
)


# =============================================================================
# FAST DENSE CACHE
#
# Scientific bytes are unchanged.
# uint8 image only.
# Padding mask still generated from frozen packet_lengths.
# =============================================================================

COLS = np.arange(
    256,
    dtype=np.uint16,
)[
    None,
    None,
    :
]


available_before = (
    mem_available_bytes()
)


DENSE_BYTES = (
    TOTAL
    *
    64
    *
    256
)


USE_DENSE_CACHE = (
    available_before
    >=
    14
    *
    1024
    *
    1024
    *
    1024
)


print()
print("=" * 78)

if USE_DENSE_CACHE:

    print(
        "BUILDING FAST UINT8 TRAIN CACHE IN RAM"
    )

else:

    print(
        "RAM BELOW DENSE-CACHE SAFETY FLOOR — USING COMPACT BATCH MODE"
    )

print("=" * 78)


dense = None


if USE_DENSE_CACHE:

    print(
        f"  cache bytes: "
        f"{DENSE_BYTES:,} "
        f"({DENSE_BYTES / 1024**3:.2f} GiB)"
    )

    print(
        f"  MemAvailable before: "
        f"{available_before / 1024**3:.2f} GiB"
    )


    dense = np.empty(
        (
            TOTAL,
            64,
            256,
        ),
        dtype=np.uint8,
    )


    chunk = 2_048

    cache_started = time.time()


    for start in range(
        0,
        TOTAL,
        chunk,
    ):

        end = min(
            start
            +
            chunk,
            TOTAL,
        )


        chunk_lengths = lengths[
            start:end
        ]


        valid = (
            COLS
            <
            chunk_lengths[
                :,
                :,
                None,
            ]
        )


        image = np.zeros(
            valid.shape,
            dtype=np.uint8,
        )


        byte_start = int(
            flow_offsets[
                start
            ]
        )

        byte_end = int(
            flow_offsets[
                end
            ]
        )


        source = encoded[
            byte_start:
            byte_end
        ]


        assert (
            int(
                valid.sum()
            )
            ==
            len(
                source
            )
        )


        image[
            valid
        ] = source


        dense[
            start:end
        ] = image


        if (
            end == TOTAL
            or
            end % 50_000 < chunk
        ):

            print(
                f"  cached "
                f"{end:,}/{TOTAL:,}",
                flush=True,
            )


    print(
        f"  dense cache complete in "
        f"{time.time() - cache_started:.1f}s"
    )


    # Compact authentic bytes/offsets no longer needed during epochs.
    del encoded
    del flow_offsets

    gc.collect()


# =============================================================================
# Accelerated batch builder
# =============================================================================

def compact_batch(
    indices,
):

    batch_lengths = lengths[
        indices
    ]


    starts = flow_offsets[
        indices
    ].astype(
        np.int64,
        copy=False,
    )

    ends = flow_offsets[
        indices
        +
        1
    ].astype(
        np.int64,
        copy=False,
    )


    sizes = (
        ends
        -
        starts
    )


    valid = (
        COLS
        <
        batch_lengths[
            :,
            :,
            None,
        ]
    )


    total_bytes = int(
        sizes.sum()
    )


    repeated_starts = np.repeat(
        starts,
        sizes,
    )


    origins = np.repeat(
        (
            np.cumsum(
                sizes
            )
            -
            sizes
        ),
        sizes,
    )


    src_idx = (
        repeated_starts
        +
        (
            np.arange(
                total_bytes,
                dtype=np.int64,
            )
            -
            origins
        )
    )


    source = encoded[
        src_idx
    ]


    image = np.zeros(
        valid.shape,
        dtype=np.uint8,
    )


    image[
        valid
    ] = source


    return (
        image,
        valid,
        labels[
            indices
        ],
    )


def build_batch(
    indices,
):

    indices = np.asarray(
        indices,
        dtype=np.int64,
    )


    batch_lengths = lengths[
        indices
    ]


    mask = (
        COLS
        <
        batch_lengths[
            :,
            :,
            None,
        ]
    )


    if dense is not None:

        return (
            dense[
                indices
            ],
            mask,
            labels[
                indices
            ],
        )


    return compact_batch(
        indices
    )


# =============================================================================
# Exact cache/loader verification before model sees real data
# =============================================================================

loader_mod = import_path(
    "stage20_compact_corpus_stage21",
    LOADER_MODULE,
)


official_m = (
    loader_mod
    .Stage20CompactCorpus(
        CORPUS_ROOT
        /
        "Monday"
    )
)


test_indices = np.arange(
    128,
    dtype=np.int64,
)


test_image, test_mask, test_labels = (
    build_batch(
        test_indices
    )
)


for i in range(
    128
):

    oi, om, ol = (
        official_m.reconstruct(
            i
        )
    )


    assert np.array_equal(
        test_image[i],
        oi,
    )

    assert np.array_equal(
        test_mask[i],
        om,
    )

    assert int(
        test_labels[i]
    ) == int(
        ol
    )


print(
    "Fast TRAIN cache ↔ frozen loader first128: PASS"
)


del official_m
del test_image
del test_mask
del test_labels

gc.collect()


# =============================================================================
# Prepare operational recovery release BEFORE training
# =============================================================================

release = ensure_recovery_release()


print()
print(
    "Recovery release:",
    RECOVERY_RELEASE_TAG,
)

print(
    "  release id:",
    release["id"],
)


latest = latest_remote_recovery()


# =============================================================================
# Frozen model initialization
# =============================================================================

vit_mod = import_path(
    "stage21_masked_vit_stage21",
    VIT_MODULE,
)


random.seed(
    SEED
)

np.random.seed(
    SEED
)

torch.manual_seed(
    SEED
)

torch.cuda.manual_seed_all(
    SEED
)


model = (
    vit_mod
    .Stage21MaskedViTv1()
)


assert (
    vit_mod
    .count_trainable_parameters(
        model
    )
    ==
    91_969
)


model = model.to(
    device
)


criterion = (
    torch.nn
    .BCEWithLogitsLoss(
        pos_weight=torch.tensor(
            POS_WEIGHT,
            dtype=torch.float32,
            device=device,
        )
    )
)


optimizer = (
    torch.optim.AdamW(
        model.parameters(),
        lr=0.001,
        betas=(
            0.9,
            0.999,
        ),
        eps=1e-8,
        weight_decay=0.0001,
    )
)


epochs_audit = []

optimizer_steps = 0

start_epoch0 = 0


# =============================================================================
# Optional REMOTE resume
# =============================================================================

if latest is not None:

    remote_epoch, asset = latest


    print()
    print(
        f"Remote recovery detected: "
        f"epoch {remote_epoch}"
    )


    recovery_path = (
        OUT
        /
        asset[
            "name"
        ]
    )


    download_asset(
        asset,
        recovery_path,
    )


    if asset.get(
        "digest"
    ):

        assert (
            asset["digest"]
            ==
            "sha256:"
            +
            sha256_file(
                recovery_path
            )
        )


    recovery = torch.load(
        recovery_path,
        map_location=device,
        weights_only=False,
    )


    assert (
        recovery[
            "checkpoint"
        ]
        ==
        "Stage21-2-REMOTE-RECOVERY"
    )

    assert (
        recovery[
            "repository_head"
        ]
        ==
        EXPECTED_HEAD
    )

    assert (
        recovery[
            "torch_version"
        ]
        ==
        torch.__version__
    )

    assert (
        recovery[
            "cuda_build"
        ]
        ==
        torch.version.cuda
    )

    # Do not resume across different GPU architectures.
    assert (
        recovery[
            "gpu_name"
        ]
        ==
        torch.cuda.get_device_name(
            0
        )
    )


    completed = int(
        recovery[
            "completed_epochs"
        ]
    )


    assert (
        completed
        ==
        remote_epoch
    )

    assert (
        0
        <
        completed
        <=
        EPOCHS
    )


    model.load_state_dict(
        recovery[
            "model_state"
        ]
    )


    optimizer.load_state_dict(
        recovery[
            "optimizer_state"
        ]
    )


    torch.set_rng_state(
        recovery[
            "torch_cpu_rng_state"
        ].cpu()
    )


    torch.cuda.set_rng_state_all(
        [
            x.cpu()
            for x
            in recovery[
                "torch_cuda_rng_states"
            ]
        ]
    )


    epochs_audit = recovery[
        "epochs_audit"
    ]


    optimizer_steps = int(
        recovery[
            "optimizer_steps"
        ]
    )


    start_epoch0 = completed


    print(
        f"REMOTE RECOVERY LOAD: PASS"
    )

    print(
        f"Resuming at epoch "
        f"{start_epoch0 + 1}"
        if start_epoch0 < EPOCHS
        else
        "All 10 epochs already durable remotely."
    )


else:

    print()
    print(
        "Remote recovery: NONE — starting epoch 1."
    )


# =============================================================================
# Training
# =============================================================================

print()
print("=" * 78)
print("BEGIN FROZEN STAGE21-2 TRAINING")
print("=" * 78)

print("Thursday accessed: NO")
print("Friday accessed:   NO")
print("Validation:        NONE")
print("Epoch selection:   NONE")


training_started = time.time()


for epoch0 in range(
    start_epoch0,
    EPOCHS,
):

    epoch_number = (
        epoch0
        +
        1
    )


    epoch_seed = (
        SEED
        +
        epoch0
    )


    permutation = (
        np.random.default_rng(
            epoch_seed
        )
        .permutation(
            TOTAL
        )
    )


    permutation_sha = hashlib.sha256(
        permutation.tobytes()
    ).hexdigest()


    assert (
        permutation_sha
        ==
        EXPECTED_PERMUTATION_SHA[
            epoch0
        ]
    )


    model.train()


    epoch_started = time.time()

    weighted_loss_sum = 0.0

    examples_seen = 0
    batches_seen = 0

    grad_norm_sum = 0.0
    max_grad_norm = 0.0


    print()
    print(
        "-" * 78
    )

    print(
        f"EPOCH {epoch_number}/10 "
        f"| seed={epoch_seed}"
    )

    print(
        "-" * 78
    )


    for batch_number, start in enumerate(
        range(
            0,
            TOTAL,
            BATCH_SIZE,
        ),
        start=1,
    ):

        idx = permutation[
            start:
            start
            +
            BATCH_SIZE
        ]


        image_np, mask_np, target_np = (
            build_batch(
                idx
            )
        )


        image = (
            torch.from_numpy(
                np.ascontiguousarray(
                    image_np
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


        mask = (
            torch.from_numpy(
                np.ascontiguousarray(
                    mask_np
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


        target = (
            torch.from_numpy(
                np.asarray(
                    target_np,
                    dtype=np.float32,
                )
            )
            .to(
                device
            )
        )


        optimizer.zero_grad(
            set_to_none=True
        )


        logits = model(
            image,
            mask,
        )


        loss = criterion(
            logits,
            target,
        )


        assert torch.isfinite(
            loss
        )


        loss.backward()


        grad_norm = (
            torch.nn.utils
            .clip_grad_norm_(
                model.parameters(),
                max_norm=5.0,
            )
        )


        grad_norm_f = float(
            grad_norm.detach().cpu()
        )


        optimizer.step()


        optimizer_steps += 1


        n = len(
            idx
        )


        weighted_loss_sum += (
            float(
                loss.detach().cpu()
            )
            *
            n
        )


        examples_seen += n

        batches_seen += 1

        grad_norm_sum += grad_norm_f

        max_grad_norm = max(
            max_grad_norm,
            grad_norm_f,
        )


        # Frequent stdout to keep Kaggle alive.
        if (
            batch_number == 1
            or
            batch_number % 25 == 0
            or
            batch_number
            ==
            BATCHES_PER_EPOCH
        ):

            elapsed = (
                time.time()
                -
                epoch_started
            )


            print(
                f"  ep={epoch_number:02d} "
                f"batch={batch_number:04d}/"
                f"{BATCHES_PER_EPOCH} "
                f"loss="
                f"{weighted_loss_sum/examples_seen:.8f} "
                f"elapsed="
                f"{elapsed/60:.2f}m",
                flush=True,
            )


    assert examples_seen == TOTAL
    assert batches_seen == BATCHES_PER_EPOCH

    assert (
        optimizer_steps
        ==
        epoch_number
        *
        BATCHES_PER_EPOCH
    )


    elapsed_epoch = (
        time.time()
        -
        epoch_started
    )


    state_sha = canonical_state_sha256(
        model
    )


    epoch_record = {

        "epoch":
            epoch_number,

        "zero_based_epoch_index":
            epoch0,

        "epoch_seed":
            epoch_seed,

        "permutation_sha256":
            permutation_sha,

        "examples":
            TOTAL,

        "batches":
            BATCHES_PER_EPOCH,

        "mean_weighted_bce_loss":
            float(
                weighted_loss_sum
                /
                TOTAL
            ),

        "mean_preclip_gradient_norm":
            float(
                grad_norm_sum
                /
                batches_seen
            ),

        "max_preclip_gradient_norm":
            float(
                max_grad_norm
            ),

        "canonical_model_state_sha256":
            state_sha,

        "optimizer_steps_cumulative":
            optimizer_steps,

        "validation_used":
            False,

        "selection_based_on_loss":
            False,

        "elapsed_seconds_operational":
            float(
                elapsed_epoch
            ),
    }


    epochs_audit.append(
        epoch_record
    )


    print()
    print(
        f"EPOCH {epoch_number} COMPLETE"
    )

    print(
        f"  loss: "
        f"{epoch_record['mean_weighted_bce_loss']:.9f}"
    )

    print(
        f"  state SHA: "
        f"{state_sha}"
    )

    print(
        f"  steps: "
        f"{optimizer_steps}"
    )

    print(
        f"  time: "
        f"{elapsed_epoch/60:.2f} min"
    )


    # =========================================================================
    # Durable epoch boundary
    # =========================================================================

    recovery_path = (
        OUT
        /
        (
            f"stage21-2-recovery-"
            f"epoch{epoch_number:02d}.pt"
        )
    )


    recovery_tmp = Path(
        str(
            recovery_path
        )
        +
        ".tmp"
    )


    recovery_payload = {

        "checkpoint":
            "Stage21-2-REMOTE-RECOVERY",

        "repository_head":
            EXPECTED_HEAD,

        "completed_epochs":
            epoch_number,

        "optimizer_steps":
            optimizer_steps,

        "torch_version":
            torch.__version__,

        "cuda_build":
            torch.version.cuda,

        "gpu_name":
            torch.cuda.get_device_name(
                0
            ),

        "model_state":
            OrderedDict(
                (
                    name,
                    tensor.detach().cpu()
                )
                for name, tensor
                in model.state_dict().items()
            ),

        "optimizer_state":
            optimizer.state_dict(),

        "torch_cpu_rng_state":
            torch.get_rng_state(),

        "torch_cuda_rng_states":
            torch.cuda.get_rng_state_all(),

        "epochs_audit":
            epochs_audit,

        "Thursday_accessed":
            False,

        "Friday_accessed":
            False,
    }


    torch.save(
        recovery_payload,
        recovery_tmp,
    )


    os.replace(
        recovery_tmp,
        recovery_path,
    )


    recovery_sha = sha256_file(
        recovery_path
    )


    print(
        f"  local recovery SHA: "
        f"{recovery_sha}",
        flush=True,
    )


    upload_recovery(
        epoch_number,
        recovery_path,
    )


    print(
        f"  EPOCH {epoch_number} "
        f"DURABLE REMOTELY",
        flush=True,
    )


# =============================================================================
# Final fixed epoch-10 output
# =============================================================================

assert len(
    epochs_audit
) == 10

assert (
    optimizer_steps
    ==
    TOTAL_OPTIMIZER_STEPS
)


final_state_sha = canonical_state_sha256(
    model
)


assert (
    final_state_sha
    ==
    epochs_audit[
        -1
    ][
        "canonical_model_state_sha256"
    ]
)


final_cpu_state = OrderedDict(
    (
        name,
        tensor.detach().cpu()
    )
    for name, tensor
    in model.state_dict().items()
)


tmp = Path(
    str(
        FINAL_STATE
    )
    +
    ".tmp"
)


torch.save(
    final_cpu_state,
    tmp,
)


os.replace(
    tmp,
    FINAL_STATE,
)


final_checkpoint_sha = sha256_file(
    FINAL_STATE
)


manifest = {

    "checkpoint":
        "Stage21-2",

    "status":
        "FROZEN_STAGE21_MASKED_VIT_TRAINED_EXACTLY_10_EPOCHS",

    "repository_parent":
        EXPECTED_HEAD,

    "model":
        "Stage21MaskedViTv1",

    "trainable_parameters":
        91_969,

    "train_population": {

        "days":
            [
                "Monday",
                "Tuesday",
                "Wednesday",
            ],

        "flows":
            TOTAL,

        "benign":
            TRAIN_BENIGN,

        "attack":
            TRAIN_ATTACK,

        "positive_class_weight":
            POS_WEIGHT,
    },

    "training": {

        "seed":
            42,

        "epochs":
            10,

        "batch_size":
            256,

        "optimizer":
            "AdamW",

        "learning_rate":
            0.001,

        "weight_decay":
            0.0001,

        "betas":
            [
                0.9,
                0.999,
            ],

        "eps":
            1e-8,

        "gradient_clip_norm":
            5.0,

        "automatic_mixed_precision":
            False,

        "scheduler":
            None,

        "augmentation":
            False,

        "early_stopping":
            False,

        "validation_during_training":
            False,

        "final_epoch":
            10,

        "optimizer_steps":
            optimizer_steps,
    },

    "epochs":
        epochs_audit,

    "runtime": {

        "python":
            platform.python_version(),

        "numpy":
            np.__version__,

        "torch":
            torch.__version__,

        "cuda_build":
            torch.version.cuda,

        "gpu":
            torch.cuda.get_device_name(
                0
            ),

        "cudnn":
            torch.backends.cudnn.version(),

        "TF32":
            False,

        "deterministic_algorithms":
            True,
    },

    "operational_acceleration": {

        "dense_uint8_train_cache":
            dense is not None,

        "dense_cache_scientific_change":
            False,

        "padding_mask_from_frozen_packet_lengths":
            True,

        "first128_loader_equivalence":
            True,

        "remote_epoch_recovery":
            True,
    },

    "final_model": {

        "path":
            str(
                FINAL_STATE
            ),

        "bytes":
            int(
                FINAL_STATE.stat().st_size
            ),

        "checkpoint_sha256":
            final_checkpoint_sha,

        "canonical_tensor_state_sha256":
            final_state_sha,
    },

    "scientific_boundary": {

        "Thursday_model_forward":
            False,

        "Thursday_probability_generation":
            False,

        "Thursday_threshold_selection":
            False,

        "Friday_accessed":
            False,

        "candidate_count":
            1,

        "epoch_selected_by_result":
            False,

        "final_epoch_reason":
            "PREREGISTERED_FIXED_EPOCH_10",
    },
}


atomic_json(
    FINAL_MANIFEST,
    manifest,
)


manifest_sha = sha256_file(
    FINAL_MANIFEST
)


print()
print("=" * 78)
print("STAGE21-2 FROZEN ViT TRAINING: PASS")
print("=" * 78)

print()
print("epochs:          10")
print(
    "optimizer steps:",
    optimizer_steps,
)

print()
print("Final checkpoint:")
print(" ", FINAL_STATE)

print(
    " SHA256:",
    final_checkpoint_sha,
)

print(
    " canonical state SHA256:",
    final_state_sha,
)

print()
print("Manifest:")
print(" ", FINAL_MANIFEST)

print(
    " SHA256:",
    manifest_sha,
)

print()
print(
    "All 10 epoch boundaries durable remotely: YES"
)

print("Thursday accessed: NO")
print("Friday accessed:   NO")

print()
print("NEXT:")
print(
    "  SEAL + PUSH STAGE21-2"
)

print(
    "  THEN STAGE21-3 THURSDAY EVALUATION ONCE"
)

print("=" * 78)
