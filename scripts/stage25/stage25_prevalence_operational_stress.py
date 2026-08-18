# ==============================================================================
# STAGE25 — PREVALENCE AND OPERATIONAL STRESS
# Reconstructed/exported from the Stage25 Kaggle notebook.
#
# Scientific state: CLOSED
# No new model fitting/inference is authorized by this export.
# ==============================================================================

# %% [Stage25 notebook cell 1]
# ==============================================================================
# STAGE25-0 — PREVALENCE & OPERATIONAL STRESS AUDIT
# COMPLETE PRE-PROJECTION PROTOCOL LOCK
#
# NEW KAGGLE NOTEBOOK BOOTSTRAP + FROZEN ARTIFACT INHERITANCE
#
# SCIENTIFIC OBJECTIVE
# --------------------
# How do already-frozen discrimination and operating-point characteristics
# from Stage22R and Stage24 translate under lower deployment prevalences and
# finite SOC alert-processing capacity?
#
# ABSOLUTE STAGE25 RULES
# ----------------------
# NEW MODEL FITS:             0
# NEW MODEL INFERENCE:        0
# NEW PROBABILITY ARRAYS:     0
# TARGET REOPENINGS:          0
#
# THIS CELL:
#   - reads frozen JSON / CSV / text / model bytes for SHA verification only
#   - DOES NOT import LightGBM / XGBoost / sklearn
#   - DOES NOT load any probability NPZ/NPY
#   - DOES NOT calculate any Stage25 prevalence projection
#   - DOES NOT calculate PPV/NPV/LR/cost/workload results
#
# It only inventories frozen operating points and commits the COMPLETE
# Stage25-0 protocol before any analytic projection is allowed.
#
# Expected current GitHub main:
#   ad5a01ae9021183f6c5b8046c2647fd5dad7cb6d
#
# After this cell succeeds:
#   STOP.
#   Stage25-1 begins only after independent remote verification.
# ==============================================================================

from __future__ import annotations

import os
import json
import math
import base64
import hashlib
import subprocess
from pathlib import Path
from datetime import datetime, timezone


# ==============================================================================
# 0. FROZEN REPOSITORY ANCHORS
# ==============================================================================

REPO_URL = (
    "https://github.com/"
    "themubasshir/ids2018-validation-safe-ablation.git"
)

REPO = Path(
    "/kaggle/working/ids2018-validation-safe-ablation"
)

EXPECTED_PARENT = (
    "ad5a01ae9021183f6c5b8046c2647fd5dad7cb6d"
)


# Stage24 scientific final freeze.
EXPECTED_STAGE24_FINAL_SYNTHESIS_SHA = (
    "785bbcb00140f4d7e07e9b49ad33924166b5995e66a229c986d5b1abcbcaee4b"
)

# Stage24 publication/reproducibility manifest.
EXPECTED_STAGE24_PUBLICATION_MANIFEST_SHA = (
    "7cc628debf53e22ee0c71e21e307f7e9fa766cbeecdd527174db2dbe47e3bf82"
)


# ==============================================================================
# 1. STAGE25 FROZEN DESIGN CONSTANTS
# ==============================================================================

PREVALENCE_GRID = [
    0.10,
    0.03,
    0.01,
    0.003,
    0.001,
    0.0001,
]

PPV_TARGETS = [
    0.10,
    0.25,
    0.50,
    0.75,
    0.90,
]

BENIGN_FLOWS_PER_DAY = 1_000_000

ALERT_SERVICE_MINUTES = 2

ANALYST_SHIFT_MINUTES = 480

ANALYST_CAPACITY_TIERS = [
    1,
    3,
    10,
]

C_FP = 1

C_FN = 100


# ==============================================================================
# 2. HELPERS
# ==============================================================================

def run_cmd(
    args,
    *,
    cwd=None,
    check=True,
    preserve_whitespace=False,
):

    p = subprocess.run(
        [str(x) for x in args],
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    if check and p.returncode != 0:

        raise RuntimeError(
            "\nCommand failed:\n"
            +
            " ".join(
                str(x)
                for x in args
            )
            +
            "\n\n"
            +
            (p.stdout or "")
        )

    output = (
        p.stdout
        or
        ""
    )

    if preserve_whitespace:

        return output

    return output.strip()


def git_cmd(
    *args,
    auth_header=None,
    check=True,
):

    cmd = [
        "git"
    ]

    if auth_header is not None:

        cmd += [
            "-c",
            "credential.helper=",
            "-c",
            f"http.extraHeader=AUTHORIZATION: Basic {auth_header}",
        ]

    cmd += [
        str(x)
        for x in args
    ]

    return run_cmd(
        cmd,
        cwd=REPO,
        check=check,
    )


def sha256_file(
    path,
):

    path = Path(
        path
    )

    h = hashlib.sha256()

    with path.open(
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

    return h.hexdigest()


def load_json(
    path,
):

    path = Path(
        path
    )

    if not path.is_file():

        raise RuntimeError(
            f"Missing JSON artifact:\n{path}"
        )

    return json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )


def write_json(
    path,
    payload,
):

    path = Path(
        path
    )

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    path.write_text(
        json.dumps(
            payload,
            indent=2,
            sort_keys=True,
            ensure_ascii=False,
        )
        +
        "\n",
        encoding="utf-8",
    )


def write_text(
    path,
    text,
):

    path = Path(
        path
    )

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    path.write_text(
        str(
            text
        ).rstrip()
        +
        "\n",
        encoding="utf-8",
    )


def verify_sha(
    path,
    expected,
    label,
):

    path = Path(
        path
    )

    if not path.is_file():

        raise RuntimeError(
            f"Missing {label}:\n{path}"
        )

    actual = sha256_file(
        path
    )

    if actual != expected:

        raise RuntimeError(
            f"\n{label} SHA mismatch.\n"
            f"Expected: {expected}\n"
            f"Actual:   {actual}\n"
            f"File:     {path}"
        )

    return actual


def verify_sidecar(
    artifact,
):

    artifact = Path(
        artifact
    )

    sidecar = artifact.with_suffix(
        ".sha256"
    )

    if not sidecar.is_file():

        raise RuntimeError(
            "\nMissing SHA sidecar:\n"
            f"{sidecar}"
        )

    expected = (
        sidecar
        .read_text(
            encoding="utf-8"
        )
        .strip()
        .split()[0]
    )

    actual = sha256_file(
        artifact
    )

    if actual != expected:

        raise RuntimeError(
            "\nSidecar SHA verification failed.\n"
            f"Artifact: {artifact}\n"
            f"Expected: {expected}\n"
            f"Actual:   {actual}"
        )

    return actual


def safe_div(
    numerator,
    denominator,
):

    if denominator == 0:

        return None

    return (
        numerator
        /
        denominator
    )


def assert_close(
    actual,
    expected,
    *,
    tolerance=5e-15,
    label="value",
):

    if actual is None or expected is None:

        if actual != expected:

            raise RuntimeError(
                f"{label}: None mismatch."
            )

        return

    if abs(
        float(
            actual
        )
        -
        float(
            expected
        )
    ) > tolerance:

        raise RuntimeError(
            "\nFrozen metric consistency failure.\n"
            f"{label}\n"
            f"Expected: {expected}\n"
            f"Actual:   {actual}"
        )


def canonical_operating_point(
    source,
):

    tp = int(
        source[
            "tp"
        ]
    )

    tn = int(
        source[
            "tn"
        ]
    )

    fp = int(
        source[
            "fp"
        ]
    )

    fn = int(
        source[
            "fn"
        ]
    )

    attack = (
        tp
        +
        fn
    )

    benign = (
        tn
        +
        fp
    )

    rows = (
        attack
        +
        benign
    )

    precision_from_counts = safe_div(
        tp,
        tp
        +
        fp,
    )

    recall_from_counts = safe_div(
        tp,
        attack,
    )

    fpr_from_counts = safe_div(
        fp,
        benign,
    )

    prevalence = safe_div(
        attack,
        rows,
    )


    if "precision" in source:

        assert_close(
            precision_from_counts,
            source[
                "precision"
            ],
            label="precision",
        )


    if "recall" in source:

        assert_close(
            recall_from_counts,
            source[
                "recall"
            ],
            label="recall/TPR",
        )


    if "fpr" in source:

        assert_close(
            fpr_from_counts,
            source[
                "fpr"
            ],
            label="FPR",
        )


    threshold = float(
        source[
            "threshold"
        ]
    )


    return {
        "threshold":
            threshold,

        "tp":
            tp,

        "tn":
            tn,

        "fp":
            fp,

        "fn":
            fn,

        "tpr":
            float(
                recall_from_counts
            ),

        "recall":
            float(
                recall_from_counts
            ),

        "fpr":
            float(
                fpr_from_counts
            ),

        "precision":
            (
                None
                if precision_from_counts is None
                else float(
                    precision_from_counts
                )
            ),

        "f1":
            (
                None
                if source.get(
                    "f1"
                ) is None
                else float(
                    source[
                        "f1"
                    ]
                )
            ),

        "f2":
            (
                None
                if source.get(
                    "f2"
                ) is None
                else float(
                    source[
                        "f2"
                    ]
                )
            ),

        "fnr":
            float(
                1.0
                -
                recall_from_counts
            ),

        "attack":
            attack,

        "benign":
            benign,

        "rows":
            rows,

        "observed_prevalence":
            float(
                prevalence
            ),
    }


def assert_population_identity(
    operating_points,
    cell_id,
):

    identities = {
        (
            op[
                "attack"
            ],
            op[
                "benign"
            ],
            op[
                "rows"
            ],
        )
        for op in operating_points.values()
    }

    if len(
        identities
    ) != 1:

        raise RuntimeError(
            "\nOperating points use different evaluation populations:\n"
            f"{cell_id}\n"
            f"{identities}"
        )

    attack, benign, rows = next(
        iter(
            identities
        )
    )

    return {
        "attack":
            int(
                attack
            ),

        "benign":
            int(
                benign
            ),

        "rows":
            int(
                rows
            ),

        "observed_prevalence":
            float(
                attack
                /
                rows
            ),
    }


def metrics_container_stage24(
    result,
):

    metrics = result[
        "metrics"
    ]

    # Stage24-2B identity receipt nests copied metrics under "values".
    if (
        isinstance(
            metrics,
            dict,
        )
        and
        "values" in metrics
    ):

        metrics = metrics[
            "values"
        ]

    return metrics


def selected_target_identity(
    target_population,
):

    if not isinstance(
        target_population,
        dict,
    ):

        return {}

    permitted = [
        "dataset",
        "file",
        "rows",
        "benign",
        "attack",
        "prevalence",
        "binary_label_sha256",
        "original_row_index_sha256",
        "clean_position_sha256",
        "raw_source_sha256",
        "raw_source_expected_sha256",
        "stage22r_day07_cache_expected_sha256",
        "canonical_row_order",
        "materialization_mode",
        "membership_source",
    ]

    return {
        key:
            target_population[
                key
            ]
        for key in permitted
        if key in target_population
    }


def recursive_hash_fields(
    obj,
    *,
    path="root",
    out=None,
):

    if out is None:

        out = []

    if isinstance(
        obj,
        dict,
    ):

        for key, value in obj.items():

            child_path = (
                f"{path}.{key}"
            )

            if (
                isinstance(
                    value,
                    str,
                )
                and
                key.lower().endswith(
                    "sha256"
                )
                and
                len(
                    value
                )
                ==
                64
            ):

                out.append(
                    {
                        "json_path":
                            child_path,

                        "sha256":
                            value,
                    }
                )

            else:

                recursive_hash_fields(
                    value,
                    path=child_path,
                    out=out,
                )


    elif isinstance(
        obj,
        list,
    ):

        for index, value in enumerate(
            obj
        ):

            recursive_hash_fields(
                value,
                path=(
                    f"{path}[{index}]"
                ),
                out=out,
            )


    return out


# ==============================================================================
# 3. GITHUB TOKEN
# ==============================================================================

print("=" * 118)
print("GITHUB CREDENTIAL")
print("=" * 118)


github_token = None

token_source = None


try:

    from kaggle_secrets import UserSecretsClient

    secrets = UserSecretsClient()

    for name in [
        "GITHUB_TOKEN",
        "github_token",
        "GH_TOKEN",
        "GITHUB_PAT",
        "github_pat",
    ]:

        try:

            value = secrets.get_secret(
                name
            )

            if (
                value
                and
                value.strip()
            ):

                github_token = value.strip()

                token_source = name

                break

        except Exception:

            pass

except Exception:

    pass


if github_token is None:

    for name in [
        "GITHUB_TOKEN",
        "GH_TOKEN",
    ]:

        value = os.environ.get(
            name
        )

        if (
            value
            and
            value.strip()
        ):

            github_token = value.strip()

            token_source = (
                "ENV:"
                +
                name
            )

            break


if github_token is None:

    raise RuntimeError(
        "\nGitHub token not found.\n\n"
        "Expected Kaggle Secret:\n"
        "    GITHUB_TOKEN"
    )


auth_header = base64.b64encode(
    (
        "x-access-token:"
        +
        github_token
    ).encode()
).decode()


print(
    "GitHub credential:",
    token_source,
)

print()


# ==============================================================================
# 4. NEW-NOTEBOOK REPOSITORY BOOTSTRAP
# ==============================================================================

print("=" * 118)
print("REPOSITORY BOOTSTRAP")
print("=" * 118)


if not REPO.exists():

    run_cmd(
        [
            "git",
            "clone",
            "--depth",
            "1",
            "--branch",
            "main",
            REPO_URL,
            str(
                REPO
            ),
        ]
    )

    print(
        "[CLONED]",
        REPO,
    )

else:

    if not (
        REPO
        /
        ".git"
    ).is_dir():

        raise RuntimeError(
            "\nRepository path exists but is not a Git repository:\n"
            f"{REPO}"
        )


    status_before_fetch = git_cmd(
        "status",
        "--porcelain",
    )


    if status_before_fetch:

        raise RuntimeError(
            "\nExisting repository is not clean.\n"
            "Refusing to overwrite local work:\n"
            +
            status_before_fetch
        )


    git_cmd(
        "fetch",
        "origin",
        "main",
    )


    remote_fetch_sha = git_cmd(
        "rev-parse",
        "origin/main",
    )


    if remote_fetch_sha != EXPECTED_PARENT:

        raise RuntimeError(
            "\norigin/main does not match the frozen Stage25 parent.\n"
            f"Expected: {EXPECTED_PARENT}\n"
            f"Actual:   {remote_fetch_sha}"
        )


    git_cmd(
        "checkout",
        "main",
    )


    git_cmd(
        "merge",
        "--ff-only",
        "origin/main",
    )


head = git_cmd(
    "rev-parse",
    "HEAD",
)


status = git_cmd(
    "status",
    "--porcelain",
)


remote_before = git_cmd(
    "ls-remote",
    "origin",
    "refs/heads/main",
    auth_header=auth_header,
).split()[0]


print(
    "Local HEAD: ",
    head,
)

print(
    "Remote main:",
    remote_before,
)


if head != EXPECTED_PARENT:

    raise RuntimeError(
        "\nUnexpected local HEAD.\n"
        f"Expected: {EXPECTED_PARENT}\n"
        f"Actual:   {head}"
    )


if remote_before != EXPECTED_PARENT:

    raise RuntimeError(
        "\nUnexpected remote main.\n"
        f"Expected: {EXPECTED_PARENT}\n"
        f"Actual:   {remote_before}"
    )


if status:

    raise RuntimeError(
        "\nRepository not clean after bootstrap:\n"
        +
        status
    )


print()

print(
    "[PASS] Exact Stage24 publication-closeout commit checked out."
)

print(
    "[PASS] Repository clean."
)

print()


# ==============================================================================
# 5. OUTPUT GUARD
# ==============================================================================

STAGE25_BASE = (
    REPO
    /
    "results"
    /
    "stage25_prevalence_stress"
)

LOCK_DIR = (
    STAGE25_BASE
    /
    "stage25_0_protocol_lock"
)


if LOCK_DIR.exists():

    if any(
        LOCK_DIR.iterdir()
    ):

        raise RuntimeError(
            "\nStage25-0 protocol-lock directory already contains artifacts.\n"
            "Refusing accidental protocol replacement:\n"
            f"{LOCK_DIR}"
        )


# ==============================================================================
# 6. FROZEN SOURCE PATHS
# ==============================================================================

# ------------------------------------------------------------------------------
# Stage22R closure and split receipts
# ------------------------------------------------------------------------------

STAGE22_CLOSEOUT = (
    REPO
    /
    "results/stage22r_training/"
    "stage22r_publication_closeout/"
    "stage22r_publication_closeout_manifest.json"
)


STAGE22_MEMBERSHIP_SUMMARY = (
    REPO
    /
    "results/stage22r_protocol_recovery/"
    "stage22r_1b1_development_memberships/"
    "stage22r_1b1_membership_summary.json"
)


STAGE22_RANDOM_MEMBERSHIP = (
    REPO
    /
    "results/stage22r_protocol_recovery/"
    "stage22r_1b1_development_memberships/"
    "random_validation.packbits"
)


STAGE22_DAY_OFFSETS = (
    REPO
    /
    "results/stage22r_protocol_recovery/"
    "stage22r_1b1_development_memberships/"
    "stage22r_1b1_day_offsets.csv"
)


STAGE22_RANDOM_RESULT = (
    REPO
    /
    "results/stage22r_training/"
    "stage22r_2a_random_natural/"
    "stage22r_2a_random_natural_result.json"
)


STAGE22_CHRON_RESULT = (
    REPO
    /
    "results/stage22r_training/"
    "stage22r_2c_chronological_natural/"
    "stage22r_2c_chronological_natural_result.json"
)


# ------------------------------------------------------------------------------
# Stage24 closure / lock
# ------------------------------------------------------------------------------

STAGE24_FINAL = (
    REPO
    /
    "results/stage24_cross_dataset/"
    "stage24_6_final_synthesis/"
    "stage24_6_final_synthesis.json"
)


STAGE24_PUBLICATION_MANIFEST = (
    REPO
    /
    "results/stage24_cross_dataset/"
    "stage24_publication_package/"
    "stage24_publication_package_manifest.json"
)


STAGE24_FINAL_PROTOCOL = (
    REPO
    /
    "results/stage24_cross_dataset/"
    "stage24_0_protocol_lock/"
    "stage24_0c_final_preopening_protocol_lock.json"
)


STAGE24_SOURCE_CONTRACT = (
    REPO
    /
    "results/stage24_cross_dataset/"
    "stage24_0_protocol_lock/"
    "stage24_0b2_complete_cicids2017_source_contract.json"
)


# ------------------------------------------------------------------------------
# Stage24 eligible primary target cells
# ------------------------------------------------------------------------------

STAGE24_2A = (
    REPO
    /
    "results/stage24_cross_dataset/"
    "stage24_2_primary_target_openings/"
    "stage24_2a_bridge62_published/"
    "stage24_2a_bridge62_published_result.json"
)


STAGE24_2B = (
    REPO
    /
    "results/stage24_cross_dataset/"
    "stage24_2_primary_target_openings/"
    "stage24_2b_bridge62_flag_corrected/"
    "stage24_2b_bridge62_flag_corrected_identity_result.json"
)


STAGE24_2C = (
    REPO
    /
    "results/stage24_cross_dataset/"
    "stage24_2_primary_target_openings/"
    "stage24_2c_bridge70_published/"
    "stage24_2c_bridge70_published_result.json"
)


STAGE24_2D = (
    REPO
    /
    "results/stage24_cross_dataset/"
    "stage24_2_primary_target_openings/"
    "stage24_2d_bridge70_flag_corrected/"
    "stage24_2d_bridge70_flag_corrected_result.json"
)


# ------------------------------------------------------------------------------
# Stage24 eligible reciprocal target cells
# ------------------------------------------------------------------------------

STAGE24_5A = (
    REPO
    /
    "results/stage24_cross_dataset/"
    "stage24_5_secondary_target_openings/"
    "stage24_5a_bridge62_ids2018_feb28/"
    "stage24_5a_secondary_bridge62_ids2018_feb28_result.json"
)


STAGE24_5B = (
    REPO
    /
    "results/stage24_cross_dataset/"
    "stage24_5_secondary_target_openings/"
    "stage24_5b_bridge70_ids2018_feb28/"
    "stage24_5b_secondary_bridge70_ids2018_feb28_result.json"
)


# ------------------------------------------------------------------------------
# Threshold source artifacts
# ------------------------------------------------------------------------------

STAGE22_RANDOM_THRESHOLD_GRID = (
    STAGE22_RANDOM_RESULT.parent
    /
    "random_natural_validation_threshold_grid.csv"
)


STAGE22_CHRON_THRESHOLD_GRID = (
    STAGE22_CHRON_RESULT.parent
    /
    "chronological_natural_validation_threshold_grid.csv"
)


STAGE24_PRIMARY_BRIDGE62_THRESHOLD_GRID = (
    REPO
    /
    "results/stage24_cross_dataset/"
    "stage24_1_primary_source_sanity/"
    "stage24_1b_bridge62_source_refit/"
    "bridge62_validation_threshold_grid.csv"
)


STAGE24_SECONDARY_BRIDGE62_THRESHOLD_GRID = (
    REPO
    /
    "results/stage24_cross_dataset/"
    "stage24_4_secondary_source_training/"
    "stage24_4a_bridge62_xgboost/"
    "secondary_bridge62_validation_threshold_grid.csv"
)


STAGE24_SECONDARY_BRIDGE70_THRESHOLD_GRID = (
    REPO
    /
    "results/stage24_cross_dataset/"
    "stage24_4_secondary_source_training/"
    "stage24_4b_bridge70_xgboost/"
    "secondary_bridge70_validation_threshold_grid.csv"
)


STAGE24_SECONDARY_BRIDGE62_SOURCE_RESULT = (
    REPO
    /
    "results/stage24_cross_dataset/"
    "stage24_4_secondary_source_training/"
    "stage24_4a_bridge62_xgboost/"
    "stage24_4a_secondary_bridge62_result.json"
)


STAGE24_SECONDARY_BRIDGE70_SOURCE_RESULT = (
    REPO
    /
    "results/stage24_cross_dataset/"
    "stage24_4_secondary_source_training/"
    "stage24_4b_bridge70_xgboost/"
    "stage24_4b_secondary_bridge70_result.json"
)


# ==============================================================================
# 7. VERIFY STAGE22R CLOSURE
# ==============================================================================

print("=" * 118)
print("STAGE22R CLOSURE VERIFICATION")
print("=" * 118)


stage22_closeout = load_json(
    STAGE22_CLOSEOUT
)


if (
    stage22_closeout[
        "status"
    ]
    !=
    "PUBLICATION_ASSETS_GENERATED_FROM_FROZEN_SUMMARIES_ONLY"
):

    raise RuntimeError(
        "Unexpected Stage22R publication closeout status."
    )


scientific_result = stage22_closeout[
    "scientific_result"
]


if (
    scientific_result[
        "holdout_status"
    ]
    !=
    "PERMANENTLY_CLOSED"
):

    raise RuntimeError(
        "Stage22R holdout is not permanently closed."
    )


if (
    int(
        scientific_result[
            "holdout_openings_consumed"
        ]
    )
    !=
    int(
        scientific_result[
            "maximum_authorized_openings"
        ]
    )
):

    raise RuntimeError(
        "Stage22R holdout-opening accounting changed."
    )


stage22_closeout_sha = sha256_file(
    STAGE22_CLOSEOUT
)


print(
    "Closeout SHA:",
    stage22_closeout_sha,
)

print(
    "Scientific result commit:",
    scientific_result[
        "commit"
    ],
)

print(
    "Holdout status:",
    scientific_result[
        "holdout_status"
    ],
)

print()

print(
    "[PASS] Stage22R closure verified."
)

print()


# ==============================================================================
# 8. VERIFY STAGE24 CLOSURE
# ==============================================================================

print("=" * 118)
print("STAGE24 CLOSURE VERIFICATION")
print("=" * 118)


stage24_final_sha = verify_sidecar(
    STAGE24_FINAL
)


if (
    stage24_final_sha
    !=
    EXPECTED_STAGE24_FINAL_SYNTHESIS_SHA
):

    raise RuntimeError(
        "\nUnexpected Stage24 final synthesis SHA.\n"
        f"Expected: {EXPECTED_STAGE24_FINAL_SYNTHESIS_SHA}\n"
        f"Actual:   {stage24_final_sha}"
    )


stage24_final = load_json(
    STAGE24_FINAL
)


if (
    stage24_final[
        "status"
    ]
    !=
    "STAGE24_CROSS_DATASET_AUDIT_COMPLETE"
):

    raise RuntimeError(
        "Stage24 scientific status changed."
    )


if (
    stage24_final[
        "completion"
    ][
        "Stage24_complete"
    ]
    is not True
):

    raise RuntimeError(
        "Stage24 completion flag changed."
    )


if (
    stage24_final[
        "completion"
    ][
        "scientific_fits"
    ]
    !=
    "4/4"
):

    raise RuntimeError(
        "Stage24 fit accounting changed."
    )


if (
    stage24_final[
        "completion"
    ][
        "evaluable_target_openings"
    ]
    !=
    "6/6"
):

    raise RuntimeError(
        "Stage24 opening accounting changed."
    )


stage24_pub_manifest_sha = verify_sidecar(
    STAGE24_PUBLICATION_MANIFEST
)


if (
    stage24_pub_manifest_sha
    !=
    EXPECTED_STAGE24_PUBLICATION_MANIFEST_SHA
):

    raise RuntimeError(
        "\nStage24 publication manifest SHA changed.\n"
        f"Expected: {EXPECTED_STAGE24_PUBLICATION_MANIFEST_SHA}\n"
        f"Actual:   {stage24_pub_manifest_sha}"
    )


stage24_pub_manifest = load_json(
    STAGE24_PUBLICATION_MANIFEST
)


if (
    stage24_pub_manifest[
        "scientific_execution_closed"
    ]
    is not True
):

    raise RuntimeError(
        "Stage24 publication manifest does not mark science closed."
    )


stage24_protocol_sha = verify_sidecar(
    STAGE24_FINAL_PROTOCOL
)


stage24_source_contract_sha = verify_sidecar(
    STAGE24_SOURCE_CONTRACT
)


print(
    "Final synthesis SHA:      ",
    stage24_final_sha,
)

print(
    "Publication manifest SHA: ",
    stage24_pub_manifest_sha,
)

print(
    "Final protocol SHA:       ",
    stage24_protocol_sha,
)

print(
    "CICIDS2017 contract SHA:   ",
    stage24_source_contract_sha,
)

print()

print(
    "[PASS] Stage24 is scientifically closed."
)

print()


# ==============================================================================
# 9. VERIFY STAGE22R MEMBERSHIP RECEIPTS
# ==============================================================================

print("=" * 118)
print("STAGE22R SPLIT RECEIPTS")
print("=" * 118)


membership_summary = load_json(
    STAGE22_MEMBERSHIP_SUMMARY
)


membership_summary_sha = sha256_file(
    STAGE22_MEMBERSHIP_SUMMARY
)


random_membership_sha = sha256_file(
    STAGE22_RANDOM_MEMBERSHIP
)


expected_random_membership_sha = (
    membership_summary[
        "artifacts"
    ][
        "random_validation.packbits"
    ][
        "sha256"
    ]
)


if (
    random_membership_sha
    !=
    expected_random_membership_sha
):

    raise RuntimeError(
        "Stage22R random validation membership SHA mismatch."
    )


day_offsets_sha = sha256_file(
    STAGE22_DAY_OFFSETS
)


expected_day_offsets_sha = (
    membership_summary[
        "artifacts"
    ][
        "stage22r_1b1_day_offsets.csv"
    ][
        "sha256"
    ]
)


if day_offsets_sha != expected_day_offsets_sha:

    raise RuntimeError(
        "Stage22R day-offset receipt SHA mismatch."
    )


print(
    "Membership summary SHA:",
    membership_summary_sha,
)

print(
    "Random validation membership SHA:",
    random_membership_sha,
)

print(
    "Chronological day-offset SHA:",
    day_offsets_sha,
)

print()

print(
    "[PASS] Random split membership is byte-frozen."
)

print(
    "[PASS] Chronological validation remains deterministic day_id=7."
)

print()


# ==============================================================================
# 10. LOAD FROZEN RESULT RECEIPTS
# ==============================================================================

stage22_random = load_json(
    STAGE22_RANDOM_RESULT
)

stage22_chron = load_json(
    STAGE22_CHRON_RESULT
)

stage24_2a = load_json(
    STAGE24_2A
)

stage24_2b = load_json(
    STAGE24_2B
)

stage24_2c = load_json(
    STAGE24_2C
)

stage24_2d = load_json(
    STAGE24_2D
)

stage24_5a = load_json(
    STAGE24_5A
)

stage24_5b = load_json(
    STAGE24_5B
)


# Stage24 result sidecars must all still verify.
for path in [
    STAGE24_2A,
    STAGE24_2B,
    STAGE24_2C,
    STAGE24_2D,
    STAGE24_5A,
    STAGE24_5B,
    STAGE24_SECONDARY_BRIDGE62_SOURCE_RESULT,
    STAGE24_SECONDARY_BRIDGE70_SOURCE_RESULT,
]:

    verify_sidecar(
        path
    )


# ==============================================================================
# 11. STAGE22R OPERATING-POINT EXTRACTION
# ==============================================================================

print("=" * 118)
print("STAGE22R FROZEN OPERATING POINTS")
print("=" * 118)


def extract_stage22_operating_points(
    result,
):

    points = {}

    for name in [
        "standard",
        "balanced",
        "security",
    ]:

        source = result[
            "operating_points"
        ][
            name
        ]

        if (
            isinstance(
                source,
                dict,
            )
            and
            "result" in source
        ):

            source = source[
                "result"
            ]

        points[
            name.upper()
        ] = canonical_operating_point(
            source
        )

    return points


stage22_random_ops = extract_stage22_operating_points(
    stage22_random
)


stage22_chron_ops = extract_stage22_operating_points(
    stage22_chron
)


stage22_random_population = assert_population_identity(
    stage22_random_ops,
    "STAGE22_RANDOM",
)


stage22_chron_population = assert_population_identity(
    stage22_chron_ops,
    "STAGE22_CHRONOLOGICAL",
)


# Compare counts against frozen data receipt.
for result, population, label in [
    (
        stage22_random,
        stage22_random_population,
        "RANDOM_NATURAL",
    ),
    (
        stage22_chron,
        stage22_chron_population,
        "CHRONOLOGICAL_NATURAL",
    ),
]:

    frozen_validation = result[
        "data"
    ][
        "validation"
    ]

    for key in [
        "rows",
        "attack",
        "benign",
    ]:

        if (
            int(
                frozen_validation[
                    key
                ]
            )
            !=
            int(
                population[
                    key
                ]
            )
        ):

            raise RuntimeError(
                f"{label}: frozen validation {key} mismatch."
            )


random_prevalence = stage22_random_population[
    "observed_prevalence"
]


chron_prevalence = stage22_chron_population[
    "observed_prevalence"
]


print(
    "RANDOM_NATURAL prevalence:      ",
    f"{random_prevalence:.17f}",
)

print(
    "CHRONOLOGICAL_NATURAL prevalence:",
    f"{chron_prevalence:.17f}",
)

print()


for cell_name, points in [
    (
        "RANDOM_NATURAL",
        stage22_random_ops,
    ),
    (
        "CHRONOLOGICAL_NATURAL",
        stage22_chron_ops,
    ),
]:

    print(
        cell_name
    )

    for op_name, op in points.items():

        print(
            f"  {op_name:8s}"
            f" threshold={op['threshold']:.9f}"
            f" TPR={op['tpr']:.15f}"
            f" FPR={op['fpr']:.15f}"
            f" precision={op['precision']:.15f}"
            f" TP={op['tp']:,}"
            f" FP={op['fp']:,}"
        )

    print()


# ==============================================================================
# 12. VERIFY STAGE22R MODEL + THRESHOLD ARTIFACT SHAS
# ==============================================================================

artifact_hash_cache = {}


def hash_and_cache(
    path,
):

    path = Path(
        path
    )

    key = str(
        path.relative_to(
            REPO
        )
    )

    if key not in artifact_hash_cache:

        artifact_hash_cache[
            key
        ] = sha256_file(
            path
        )

    return artifact_hash_cache[
        key
    ]


def verify_stage22_models(
    result,
    result_path,
):

    result_path = Path(
        result_path
    )

    hashes = result[
        "artifacts"
    ][
        "hashes_before_result_json"
    ]

    model_entries = {}

    for filename, expected_sha in hashes.items():

        if (
            "model" not in filename
        ):

            continue

        path = (
            result_path.parent
            /
            filename
        )

        actual = hash_and_cache(
            path
        )

        if actual != expected_sha:

            raise RuntimeError(
                "\nStage22 model SHA mismatch.\n"
                f"File: {path}\n"
                f"Expected: {expected_sha}\n"
                f"Actual:   {actual}"
            )

        if "lightgbm" in filename:

            model_entries[
                "lightgbm"
            ] = {
                "path":
                    str(
                        path.relative_to(
                            REPO
                        )
                    ),

                "sha256":
                    actual,
            }

        elif "xgboost" in filename:

            model_entries[
                "xgboost"
            ] = {
                "path":
                    str(
                        path.relative_to(
                            REPO
                        )
                    ),

                "sha256":
                    actual,
            }

    return model_entries


stage22_random_models = verify_stage22_models(
    stage22_random,
    STAGE22_RANDOM_RESULT,
)


stage22_chron_models = verify_stage22_models(
    stage22_chron,
    STAGE22_CHRON_RESULT,
)


# Threshold grid verification against Stage22 result-declared hashes.
random_threshold_grid_sha = hash_and_cache(
    STAGE22_RANDOM_THRESHOLD_GRID
)


if (
    random_threshold_grid_sha
    !=
    stage22_random[
        "artifacts"
    ][
        "hashes_before_result_json"
    ][
        STAGE22_RANDOM_THRESHOLD_GRID.name
    ]
):

    raise RuntimeError(
        "Random-natural threshold grid SHA mismatch."
    )


chron_threshold_grid_sha = hash_and_cache(
    STAGE22_CHRON_THRESHOLD_GRID
)


if (
    chron_threshold_grid_sha
    !=
    stage22_chron[
        "artifacts"
    ][
        "hashes_before_result_json"
    ][
        STAGE22_CHRON_THRESHOLD_GRID.name
    ]
):

    raise RuntimeError(
        "Chronological-natural threshold grid SHA mismatch."
    )


# ==============================================================================
# 13. STAGE24 OPERATING-POINT EXTRACTION
# ==============================================================================

print("=" * 118)
print("STAGE24 FROZEN OPERATING POINTS")
print("=" * 118)


def extract_stage24_operating_points(
    result,
):

    metrics = metrics_container_stage24(
        result
    )

    thresholded = metrics[
        "thresholded"
    ]

    points = {}

    for name in [
        "standard",
        "balanced",
        "security",
    ]:

        points[
            name.upper()
        ] = canonical_operating_point(
            thresholded[
                name
            ]
        )

    return points


stage24_result_specs = [
    {
        "cell_id":
            "STAGE24_2018_TO_2017_BRIDGE62_PUBLISHED",

        "stage":
            "Stage24-2A",

        "family":
            "STAGE24_2018_TO_2017",

        "direction":
            "IDS2018_TO_CICIDS2017",

        "bridge":
            "bridge62",

        "variant":
            "PUBLISHED",

        "result":
            stage24_2a,

        "path":
            STAGE24_2A,

        "threshold_grid":
            STAGE24_PRIMARY_BRIDGE62_THRESHOLD_GRID,

        "threshold_selection_dataset":
            "IDS2018_02-28-2018_SOURCE_VALIDATION",

        "identity_duplicate_of":
            None,
    },

    {
        "cell_id":
            "STAGE24_2018_TO_2017_BRIDGE62_FLAG_CORRECTED",

        "stage":
            "Stage24-2B",

        "family":
            "STAGE24_2018_TO_2017",

        "direction":
            "IDS2018_TO_CICIDS2017",

        "bridge":
            "bridge62",

        "variant":
            "FLAG_CORRECTED",

        "result":
            stage24_2b,

        "path":
            STAGE24_2B,

        "threshold_grid":
            STAGE24_PRIMARY_BRIDGE62_THRESHOLD_GRID,

        "threshold_selection_dataset":
            "IDS2018_02-28-2018_SOURCE_VALIDATION",

        "identity_duplicate_of":
            "STAGE24_2018_TO_2017_BRIDGE62_PUBLISHED",
    },

    {
        "cell_id":
            "STAGE24_2018_TO_2017_BRIDGE70_PUBLISHED",

        "stage":
            "Stage24-2C",

        "family":
            "STAGE24_2018_TO_2017",

        "direction":
            "IDS2018_TO_CICIDS2017",

        "bridge":
            "bridge70",

        "variant":
            "PUBLISHED",

        "result":
            stage24_2c,

        "path":
            STAGE24_2C,

        "threshold_grid":
            STAGE22_CHRON_THRESHOLD_GRID,

        "threshold_selection_dataset":
            "IDS2018_02-28-2018_SOURCE_VALIDATION",

        "identity_duplicate_of":
            None,
    },

    {
        "cell_id":
            "STAGE24_2018_TO_2017_BRIDGE70_FLAG_CORRECTED",

        "stage":
            "Stage24-2D",

        "family":
            "STAGE24_2018_TO_2017",

        "direction":
            "IDS2018_TO_CICIDS2017",

        "bridge":
            "bridge70",

        "variant":
            "FLAG_CORRECTED",

        "result":
            stage24_2d,

        "path":
            STAGE24_2D,

        "threshold_grid":
            STAGE22_CHRON_THRESHOLD_GRID,

        "threshold_selection_dataset":
            "IDS2018_02-28-2018_SOURCE_VALIDATION",

        "identity_duplicate_of":
            None,
    },

    {
        "cell_id":
            "STAGE24_2017_TO_2018_BRIDGE62",

        "stage":
            "Stage24-5A",

        "family":
            "STAGE24_2017_TO_2018",

        "direction":
            "CICIDS2017_TO_IDS2018",

        "bridge":
            "bridge62",

        "variant":
            "FLAG_CORRECTED_SOURCE_SEMANTICS",

        "result":
            stage24_5a,

        "path":
            STAGE24_5A,

        "threshold_grid":
            STAGE24_SECONDARY_BRIDGE62_THRESHOLD_GRID,

        "threshold_selection_dataset":
            "CICIDS2017_THURSDAY_SOURCE_VALIDATION",

        "identity_duplicate_of":
            None,
    },

    {
        "cell_id":
            "STAGE24_2017_TO_2018_BRIDGE70",

        "stage":
            "Stage24-5B",

        "family":
            "STAGE24_2017_TO_2018",

        "direction":
            "CICIDS2017_TO_IDS2018",

        "bridge":
            "bridge70",

        "variant":
            "FLAG_CORRECTED_SOURCE_SEMANTICS",

        "result":
            stage24_5b,

        "path":
            STAGE24_5B,

        "threshold_grid":
            STAGE24_SECONDARY_BRIDGE70_THRESHOLD_GRID,

        "threshold_selection_dataset":
            "CICIDS2017_THURSDAY_SOURCE_VALIDATION",

        "identity_duplicate_of":
            None,
    },
]


stage24_cells_runtime = []


for spec in stage24_result_specs:

    ops = extract_stage24_operating_points(
        spec[
            "result"
        ]
    )

    population = assert_population_identity(
        ops,
        spec[
            "cell_id"
        ],
    )

    result_sha = verify_sidecar(
        spec[
            "path"
        ]
    )

    threshold_grid_sha = hash_and_cache(
        spec[
            "threshold_grid"
        ]
    )

    stage24_cells_runtime.append(
        {
            **spec,

            "operating_points":
                ops,

            "population":
                population,

            "result_sha":
                result_sha,

            "threshold_grid_sha":
                threshold_grid_sha,
        }
    )


# Bridge62 PUBLISHED == FLAG_CORRECTED must remain exactly identical.
primary_b62_pub = next(
    item
    for item in stage24_cells_runtime
    if item[
        "cell_id"
    ]
    ==
    "STAGE24_2018_TO_2017_BRIDGE62_PUBLISHED"
)


primary_b62_corr = next(
    item
    for item in stage24_cells_runtime
    if item[
        "cell_id"
    ]
    ==
    "STAGE24_2018_TO_2017_BRIDGE62_FLAG_CORRECTED"
)


if (
    primary_b62_pub[
        "operating_points"
    ]
    !=
    primary_b62_corr[
        "operating_points"
    ]
):

    raise RuntimeError(
        "Stage24 bridge62 PUBLISHED/CORRECTED operating points are not identical."
    )


print(
    "[PASS] Stage24 bridge62 target-semantic invariance retained."
)

print()


for item in stage24_cells_runtime:

    print(
        item[
            "cell_id"
        ],
        "prevalence=",
        f"{item['population']['observed_prevalence']:.17f}",
    )

    for op_name, op in item[
        "operating_points"
    ].items():

        print(
            f"  {op_name:8s}"
            f" threshold={op['threshold']:.9f}"
            f" TPR={op['tpr']:.15f}"
            f" FPR={op['fpr']:.15f}"
            f" precision={op['precision']:.15f}"
            f" TP={op['tp']:,}"
            f" FP={op['fp']:,}"
        )

    print()


# ==============================================================================
# 14. STAGE24 MODEL SHA EXTRACTION + BYTE VERIFICATION
# ==============================================================================

def stage24_expected_models(
    item,
):

    result = item[
        "result"
    ]

    direction = item[
        "direction"
    ]

    bridge = item[
        "bridge"
    ]


    # Secondary direction has one XGBoost model.
    if direction == "CICIDS2017_TO_IDS2018":

        model = result[
            "model"
        ]

        return {
            "xgboost": {
                "path":
                    model[
                        "model_file"
                    ],

                "sha256":
                    model[
                        "model_sha256"
                    ],
            }
        }


    # Primary direction.
    if bridge == "bridge62":

        # 2A uses nested model metadata.
        if (
            "models" in result
            and
            isinstance(
                result[
                    "models"
                ].get(
                    "lightgbm"
                ),
                dict,
            )
        ):

            return {
                "lightgbm": {
                    "path":
                        result[
                            "models"
                        ][
                            "lightgbm"
                        ][
                            "model_file"
                        ],

                    "sha256":
                        result[
                            "models"
                        ][
                            "lightgbm"
                        ][
                            "model_sha256"
                        ],
                },

                "xgboost": {
                    "path":
                        result[
                            "models"
                        ][
                            "xgboost"
                        ][
                            "model_file"
                        ],

                    "sha256":
                        result[
                            "models"
                        ][
                            "xgboost"
                        ][
                            "model_sha256"
                        ],
                },
            }


        # 2B identity receipt records hashes directly.
        return {
            "lightgbm": {
                "path":
                    (
                        "results/stage24_cross_dataset/"
                        "stage24_1_primary_source_sanity/"
                        "stage24_1b_bridge62_source_refit/"
                        "bridge62_lightgbm_model.txt"
                    ),

                "sha256":
                    result[
                        "models"
                    ][
                        "lightgbm_sha256"
                    ],
            },

            "xgboost": {
                "path":
                    (
                        "results/stage24_cross_dataset/"
                        "stage24_1_primary_source_sanity/"
                        "stage24_1b_bridge62_source_refit/"
                        "bridge62_xgboost_model.json"
                    ),

                "sha256":
                    result[
                        "models"
                    ][
                        "xgboost_sha256"
                    ],
            },
        }


    # bridge70 reuses exact Stage22R chronological-natural pair.
    models = result[
        "models"
    ]

    if isinstance(
        models.get(
            "lightgbm"
        ),
        dict,
    ):

        return {
            "lightgbm": {
                "path":
                    models[
                        "lightgbm"
                    ][
                        "model_file"
                    ],

                "sha256":
                    models[
                        "lightgbm"
                    ][
                        "model_sha256"
                    ],
            },

            "xgboost": {
                "path":
                    models[
                        "xgboost"
                    ][
                        "model_file"
                    ],

                "sha256":
                    models[
                        "xgboost"
                    ][
                        "model_sha256"
                    ],
            },
        }


    raise RuntimeError(
        "Could not recover Stage24 primary model identities."
    )


for item in stage24_cells_runtime:

    models = stage24_expected_models(
        item
    )

    verified_models = {}


    for model_name, model_spec in models.items():

        path = (
            REPO
            /
            model_spec[
                "path"
            ]
        )

        actual_sha = hash_and_cache(
            path
        )

        expected_sha = model_spec[
            "sha256"
        ]

        if actual_sha != expected_sha:

            raise RuntimeError(
                "\nStage24 model SHA mismatch.\n"
                f"Cell: {item['cell_id']}\n"
                f"Model: {model_name}\n"
                f"Expected: {expected_sha}\n"
                f"Actual:   {actual_sha}"
            )


        verified_models[
            model_name
        ] = {
            "path":
                model_spec[
                    "path"
                ],

            "sha256":
                actual_sha,
        }


    item[
        "models"
    ] = verified_models


print(
    "[PASS] All inherited model file SHAs verified as bytes."
)

print(
    "[PASS] No model library imported."
)

print(
    "[PASS] No model object loaded."
)

print()


# ==============================================================================
# 15. BUILD EXACT INHERITED CELL INVENTORY
# ==============================================================================

stage22_random_result_sha = sha256_file(
    STAGE22_RANDOM_RESULT
)

stage22_chron_result_sha = sha256_file(
    STAGE22_CHRON_RESULT
)


# Both Stage22 results point to the same membership-summary receipt.
expected_membership_summary_sha_random = (
    stage22_random[
        "frozen_inputs"
    ][
        "stage22r_1b1_membership_summary"
    ][
        "sha256"
    ]
)

expected_membership_summary_sha_chron = (
    stage22_chron[
        "frozen_inputs"
    ][
        "stage22r_1b1_membership_summary"
    ][
        "sha256"
    ]
)


if not (
    membership_summary_sha
    ==
    expected_membership_summary_sha_random
    ==
    expected_membership_summary_sha_chron
):

    raise RuntimeError(
        "Stage22R membership-summary SHA disagreement."
    )


inherited_cells = []


inherited_cells.append(
    {
        "cell_id":
            "STAGE22_RANDOM",

        "source_stage":
            "Stage22R-2A",

        "family":
            "STAGE22_RANDOM",

        "direction":
            "IDS2018_RANDOM_VALIDATION",

        "bridge":
            "FULL_70_FEATURE",

        "variant":
            "RANDOM_NATURAL",

        "result_artifact": {
            "path":
                str(
                    STAGE22_RANDOM_RESULT.relative_to(
                        REPO
                    )
                ),

            "sha256":
                stage22_random_result_sha,
        },

        "models":
            stage22_random_models,

        "split_identity": {
            "type":
                "FROZEN_RANDOM_VALIDATION_MEMBERSHIP_BITSET",

            "membership_artifact":
                str(
                    STAGE22_RANDOM_MEMBERSHIP.relative_to(
                        REPO
                    )
                ),

            "membership_sha256":
                random_membership_sha,

            "membership_summary_artifact":
                str(
                    STAGE22_MEMBERSHIP_SUMMARY.relative_to(
                        REPO
                    )
                ),

            "membership_summary_sha256":
                membership_summary_sha,

            "derivation":
                membership_summary[
                    "membership_derivation"
                ][
                    "RANDOM_NATURAL_validation"
                ],
        },

        "threshold_source": {
            "selection_population":
                "STAGE22_RANDOM_VALIDATION",

            "threshold_grid_artifact":
                str(
                    STAGE22_RANDOM_THRESHOLD_GRID.relative_to(
                        REPO
                    )
                ),

            "threshold_grid_sha256":
                random_threshold_grid_sha,

            "target_or_deployment_retuning":
                False,
        },

        "evaluation_population":
            stage22_random_population,

        "operating_points":
            stage22_random_ops,

        "identity_duplicate_of":
            None,
    }
)


inherited_cells.append(
    {
        "cell_id":
            "STAGE22_CHRONOLOGICAL",

        "source_stage":
            "Stage22R-2C",

        "family":
            "STAGE22_CHRONOLOGICAL",

        "direction":
            "IDS2018_FORWARD_TEMPORAL_VALIDATION",

        "bridge":
            "FULL_70_FEATURE",

        "variant":
            "CHRONOLOGICAL_NATURAL",

        "result_artifact": {
            "path":
                str(
                    STAGE22_CHRON_RESULT.relative_to(
                        REPO
                    )
                ),

            "sha256":
                stage22_chron_result_sha,
        },

        "models":
            stage22_chron_models,

        "split_identity": {
            "type":
                "DETERMINISTIC_DAY_BASED_MEMBERSHIP",

            "membership_summary_artifact":
                str(
                    STAGE22_MEMBERSHIP_SUMMARY.relative_to(
                        REPO
                    )
                ),

            "membership_summary_sha256":
                membership_summary_sha,

            "day_offsets_artifact":
                str(
                    STAGE22_DAY_OFFSETS.relative_to(
                        REPO
                    )
                ),

            "day_offsets_sha256":
                day_offsets_sha,

            "validation_rule":
                membership_summary[
                    "membership_derivation"
                ][
                    "CHRONOLOGICAL_NATURAL_validation"
                ],

            "note":
                (
                    "No separate chronological validation bitset exists; "
                    "the frozen membership is deterministic day_id=7 and "
                    "is anchored by the membership-summary and day-offset receipts."
                ),
        },

        "threshold_source": {
            "selection_population":
                "STAGE22_CHRONOLOGICAL_VALIDATION_02_28_2018",

            "threshold_grid_artifact":
                str(
                    STAGE22_CHRON_THRESHOLD_GRID.relative_to(
                        REPO
                    )
                ),

            "threshold_grid_sha256":
                chron_threshold_grid_sha,

            "target_or_deployment_retuning":
                False,
        },

        "evaluation_population":
            stage22_chron_population,

        "operating_points":
            stage22_chron_ops,

        "identity_duplicate_of":
            None,
    }
)


# ------------------------------------------------------------------------------
# Stage24 target identity helper
# ------------------------------------------------------------------------------

stage24_primary_target_population = (
    stage24_final[
        "primary_direction"
    ].get(
        "target_population",
        {}
    )
)


for item in stage24_cells_runtime:

    result = item[
        "result"
    ]


    target_identity = selected_target_identity(
        result.get(
            "target_population",
            {}
        )
    )


    # Stage24-2B deliberately reuses 2A population and prediction identity.
    if (
        item[
            "identity_duplicate_of"
        ]
        ==
        "STAGE24_2018_TO_2017_BRIDGE62_PUBLISHED"
    ):

        source_identity = selected_target_identity(
            stage24_2a.get(
                "target_population",
                {}
            )
        )

        if source_identity:

            target_identity = source_identity


    if item[
        "direction"
    ] == "IDS2018_TO_CICIDS2017":

        split_identity = {
            "source_split_type":
                "STAGE22R_CHRONOLOGICAL_NATURAL",

            "source_membership_summary_sha256":
                membership_summary_sha,

            "source_day_offsets_sha256":
                day_offsets_sha,

            "source_train_rule":
                "day_id 0..6",

            "source_validation_rule":
                "day_id 7 = 02-28-2018",

            "target_population_type":
                "CICIDS2017_FULL_EFFECTIVE_POPULATION",

            "target_rows":
                item[
                    "population"
                ][
                    "rows"
                ],

            "target_attack":
                item[
                    "population"
                ][
                    "attack"
                ],

            "target_benign":
                item[
                    "population"
                ][
                    "benign"
                ],

            "target_identity":
                target_identity,

            "stage24_protocol_sha256":
                stage24_protocol_sha,

            "cicids2017_source_contract_sha256":
                stage24_source_contract_sha,
        }


    else:

        split_identity = {
            "source_split_type":
                "CICIDS2017_MON_WED_TRAIN_THURSDAY_VALIDATION",

            "stage24_protocol_sha256":
                stage24_protocol_sha,

            "cicids2017_source_contract_sha256":
                stage24_source_contract_sha,

            "target_population_type":
                "IDS2018_FEB28_FROZEN_K79_CLEAN_POPULATION",

            "target_identity":
                target_identity,
        }


    inherited_cells.append(
        {
            "cell_id":
                item[
                    "cell_id"
                ],

            "source_stage":
                item[
                    "stage"
                ],

            "family":
                item[
                    "family"
                ],

            "direction":
                item[
                    "direction"
                ],

            "bridge":
                item[
                    "bridge"
                ],

            "variant":
                item[
                    "variant"
                ],

            "result_artifact": {
                "path":
                    str(
                        item[
                            "path"
                        ].relative_to(
                            REPO
                        )
                    ),

                "sha256":
                    item[
                        "result_sha"
                    ],
            },

            "models":
                item[
                    "models"
                ],

            "split_identity":
                split_identity,

            "threshold_source": {
                "selection_population":
                    item[
                        "threshold_selection_dataset"
                    ],

                "threshold_grid_artifact":
                    str(
                        item[
                            "threshold_grid"
                        ].relative_to(
                            REPO
                        )
                    ),

                "threshold_grid_sha256":
                    item[
                        "threshold_grid_sha"
                    ],

                "target_or_deployment_retuning":
                    False,
            },

            "evaluation_population":
                item[
                    "population"
                ],

            "operating_points":
                item[
                    "operating_points"
                ],

            "identity_duplicate_of":
                item[
                    "identity_duplicate_of"
                ],
        }
    )


# ==============================================================================
# 16. COMPLETE CELL / OPERATING-POINT ACCOUNTING
# ==============================================================================

expected_cell_ids = {
    "STAGE22_RANDOM",
    "STAGE22_CHRONOLOGICAL",

    "STAGE24_2018_TO_2017_BRIDGE62_PUBLISHED",
    "STAGE24_2018_TO_2017_BRIDGE62_FLAG_CORRECTED",
    "STAGE24_2018_TO_2017_BRIDGE70_PUBLISHED",
    "STAGE24_2018_TO_2017_BRIDGE70_FLAG_CORRECTED",

    "STAGE24_2017_TO_2018_BRIDGE62",
    "STAGE24_2017_TO_2018_BRIDGE70",
}


actual_cell_ids = {
    cell[
        "cell_id"
    ]
    for cell in inherited_cells
}


if actual_cell_ids != expected_cell_ids:

    raise RuntimeError(
        "\nInherited Stage25 cell set mismatch.\n"
        f"Expected: {sorted(expected_cell_ids)}\n"
        f"Actual:   {sorted(actual_cell_ids)}"
    )


for cell in inherited_cells:

    if set(
        cell[
            "operating_points"
        ].keys()
    ) != {
        "STANDARD",
        "BALANCED",
        "SECURITY",
    }:

        raise RuntimeError(
            f"{cell['cell_id']}: operating-point names changed."
        )


operating_point_count = sum(
    len(
        cell[
            "operating_points"
        ]
    )
    for cell in inherited_cells
)


if operating_point_count != 24:

    raise RuntimeError(
        "\nUnexpected Stage25 inherited operating-point count.\n"
        f"Expected: 24\n"
        f"Actual:   {operating_point_count}"
    )


print("=" * 118)
print("INHERITED CELL ACCOUNTING")
print("=" * 118)

print(
    "Eligible frozen cells:",
    len(
        inherited_cells
    ),
)

print(
    "Frozen operating points:",
    operating_point_count,
)

print()

print(
    "Excluded by frozen Stage25 scope:"
)

print(
    "  Stage22 RANDOM_REBALANCED"
)

print(
    "  Stage22 CHRONOLOGICAL_REBALANCED"
)

print(
    "  Stage22 final holdout (closure evidence only, not a planned Stage25 family)"
)

print(
    "  Stage24 bridge62 GROUNDED_S4 (administratively cancelled)"
)

print(
    "  Stage24 bridge70 GROUNDED_S4 (administratively cancelled)"
)

print()


# ==============================================================================
# 17. OBSERVED PREVALENCE RECEIPTS
# ==============================================================================

observed_prevalence_receipts = []


for cell in inherited_cells:

    pop = cell[
        "evaluation_population"
    ]

    observed_prevalence_receipts.append(
        {
            "cell_id":
                cell[
                    "cell_id"
                ],

            "family":
                cell[
                    "family"
                ],

            "direction":
                cell[
                    "direction"
                ],

            "bridge":
                cell[
                    "bridge"
                ],

            "variant":
                cell[
                    "variant"
                ],

            "rows":
                pop[
                    "rows"
                ],

            "benign":
                pop[
                    "benign"
                ],

            "attack":
                pop[
                    "attack"
                ],

            "observed_prevalence":
                pop[
                    "observed_prevalence"
                ],

            "source":
                "EXACT_FROZEN_CONFUSION_COUNTS",
        }
    )


# Explicit exact values expected from repository.
assert_close(
    random_prevalence,
    0.13684738945373795,
    tolerance=1e-17,
    label="Stage22 RANDOM_NATURAL exact prevalence",
)


assert_close(
    chron_prevalence,
    0.10484691299808009,
    tolerance=1e-17,
    label="Stage22 CHRONOLOGICAL_NATURAL exact prevalence",
)


stage24_primary_prevalences = {
    item[
        "population"
    ][
        "observed_prevalence"
    ]
    for item in stage24_cells_runtime
    if item[
        "family"
    ]
    ==
    "STAGE24_2018_TO_2017"
}


if len(
    stage24_primary_prevalences
) != 1:

    raise RuntimeError(
        "Stage24 primary cells do not share one target prevalence."
    )


stage24_primary_prevalence = next(
    iter(
        stage24_primary_prevalences
    )
)


assert_close(
    stage24_primary_prevalence,
    0.19699633629757277,
    tolerance=1e-17,
    label="Stage24 IDS2018->CICIDS2017 target prevalence",
)


stage24_secondary_prevalences = {
    item[
        "population"
    ][
        "observed_prevalence"
    ]
    for item in stage24_cells_runtime
    if item[
        "family"
    ]
    ==
    "STAGE24_2017_TO_2018"
}


if stage24_secondary_prevalences != {
    chron_prevalence
}:

    raise RuntimeError(
        "Stage24 secondary target prevalence changed."
    )


print("=" * 118)
print("OBSERVED PREVALENCE MARKERS")
print("=" * 118)

print(
    "Stage22 RANDOM_NATURAL:          ",
    f"{random_prevalence:.17f}",
)

print(
    "Stage22 CHRONOLOGICAL_NATURAL:   ",
    f"{chron_prevalence:.17f}",
)

print(
    "Stage24 IDS2018 -> CICIDS2017:   ",
    f"{stage24_primary_prevalence:.17f}",
)

print(
    "Stage24 CICIDS2017 -> IDS2018:   ",
    f"{chron_prevalence:.17f}",
)

print()


# ==============================================================================
# 18. HANDOFF / DURABLE-REPOSITORY RECONCILIATION
# ==============================================================================

handoff_reconciliation = {
    "rule":
        (
            "DURABLE_REPOSITORY_ARTIFACTS_OVERRIDE_HANDOFF_TEXT_IF_ANY "
            "DISCREPANCY EXISTS"
        ),

    "discrepancies_found":
        0,

    "items": [
        {
            "topic":
                "Stage22 random-natural observed prevalence",

            "handoff":
                "approximately 13.68%",

            "repository_exact":
                random_prevalence,

            "resolution":
                "HANDOFF_WAS_ROUNDED; REPOSITORY_EXACT_VALUE_FROZEN",
        },

        {
            "topic":
                "Stage22 chronological-natural observed prevalence",

            "handoff":
                "approximately 10.48%",

            "repository_exact":
                chron_prevalence,

            "resolution":
                "HANDOFF_WAS_ROUNDED; REPOSITORY_EXACT_VALUE_FROZEN",
        },

        {
            "topic":
                "Stage24 target prevalences",

            "handoff":
                "recover from frozen artifacts",

            "repository_exact": {
                "IDS2018_TO_CICIDS2017":
                    stage24_primary_prevalence,

                "CICIDS2017_TO_IDS2018":
                    chron_prevalence,
            },

            "resolution":
                "RECOVERED_FROM_DURABLE_FROZEN_RECEIPTS",
        },

        {
            "topic":
                "GROUNDED_S4 Stage24 cells",

            "handoff":
                "do not invent unavailable target cells",

            "repository":
                "2 cells administratively cancelled and not reallocated",

            "resolution":
                "EXCLUDED_FROM_STAGE25_OPERATING_POINT_INVENTORY",
        },
    ],
}


# ==============================================================================
# 19. DECLARED HASH RECEIPTS
#
# Probability artifacts are NOT opened here.
# We record only SHA strings already embedded in frozen JSON receipts.
# ==============================================================================

declared_hash_receipts = {}


for cell in inherited_cells:

    result_path = (
        REPO
        /
        cell[
            "result_artifact"
        ][
            "path"
        ]
    )

    result = load_json(
        result_path
    )

    declared_hash_receipts[
        cell[
            "cell_id"
        ]
    ] = recursive_hash_fields(
        result
    )


# Add all files actually byte-hashed by Stage25-0.
for path in [
    STAGE22_CLOSEOUT,
    STAGE22_MEMBERSHIP_SUMMARY,
    STAGE22_RANDOM_MEMBERSHIP,
    STAGE22_DAY_OFFSETS,

    STAGE22_RANDOM_RESULT,
    STAGE22_CHRON_RESULT,

    STAGE24_FINAL,
    STAGE24_PUBLICATION_MANIFEST,
    STAGE24_FINAL_PROTOCOL,
    STAGE24_SOURCE_CONTRACT,

    STAGE24_2A,
    STAGE24_2B,
    STAGE24_2C,
    STAGE24_2D,
    STAGE24_5A,
    STAGE24_5B,

    STAGE24_SECONDARY_BRIDGE62_SOURCE_RESULT,
    STAGE24_SECONDARY_BRIDGE70_SOURCE_RESULT,

    STAGE22_RANDOM_THRESHOLD_GRID,
    STAGE22_CHRON_THRESHOLD_GRID,
    STAGE24_PRIMARY_BRIDGE62_THRESHOLD_GRID,
    STAGE24_SECONDARY_BRIDGE62_THRESHOLD_GRID,
    STAGE24_SECONDARY_BRIDGE70_THRESHOLD_GRID,
]:

    artifact_hash_cache[
        str(
            path.relative_to(
                REPO
            )
        )
    ] = sha256_file(
        path
    )


# ==============================================================================
# 20. CREATE PROTOCOL DIRECTORY ONLY AFTER ALL INHERITANCE CHECKS PASS
# ==============================================================================

LOCK_DIR.mkdir(
    parents=True,
    exist_ok=False,
)


# ==============================================================================
# 21. FREEZE PREVALENCE + PPV TARGET GRID
# ==============================================================================

prevalence_grid_payload = {
    "stage":
        "Stage25-0",

    "status":
        "FROZEN_BEFORE_ANY_PROJECTION",

    "primary_prevalence_grid": {
        "decimal_probabilities":
            PREVALENCE_GRID,

        "percent_labels": [
            "10%",
            "3%",
            "1%",
            "0.3%",
            "0.1%",
            "0.01%",
        ],

        "lowest_prevalence_must_not_be_dropped":
            True,

        "changes_after_remote_freeze":
            "FORBIDDEN",
    },

    "ppv_targets": {
        "decimal_probabilities":
            PPV_TARGETS,

        "percent_labels": [
            "10%",
            "25%",
            "50%",
            "75%",
            "90%",
        ],

        "changes_after_remote_freeze":
            "FORBIDDEN",
    },

    "observed_prevalence_markers": {
        "STAGE22_RANDOM":
            random_prevalence,

        "STAGE22_CHRONOLOGICAL":
            chron_prevalence,

        "STAGE24_2018_TO_2017":
            stage24_primary_prevalence,

        "STAGE24_2017_TO_2018":
            chron_prevalence,
    },

    "important_note":
        (
            "10% is a deployment-stress grid point and MUST NOT be generically "
            "called the benchmark prevalence. Each inherited cell retains its "
            "own exact observed prevalence marker."
        ),
}


# ==============================================================================
# 22. FREEZE PRIOR-SHIFT ASSUMPTION
# ==============================================================================

prior_shift_payload = {
    "stage":
        "Stage25-0",

    "assumption_name":
        "PRIOR_PROBABILITY_SHIFT_ONLY",

    "held_invariant_within_each_inherited_operating_point": {
        "TPR":
            "P(predicted_attack | attack)",

        "FPR":
            "P(predicted_attack | benign)",
    },

    "varied_quantity": {
        "attack_prevalence":
            "pi = P(attack)",
    },

    "within_cell_rule":
        (
            "same frozen model + same frozen threshold + same frozen TPR/FPR; "
            "only prevalence varies analytically"
        ),

    "between_cell_rule":
        (
            "Random, chronological, bridge, extractor-variant and cross-dataset "
            "cells retain their different empirical TPR/FPR characteristics."
        ),

    "critical_limitation":
        (
            "This is an analytic deployment-stress projection, NOT empirical "
            "deployment validation. Real domain/temporal shift may alter "
            "P(X|Y), and therefore TPR/FPR themselves."
        ),

    "prohibited_causal_statement":
        (
            "Random splitting succeeds purely because prevalence is higher."
        ),

    "post_freeze_change":
        "FORBIDDEN",
}


# ==============================================================================
# 23. FREEZE TRAFFIC-VOLUME SEMANTICS
# ==============================================================================

traffic_volume_payload = {
    "stage":
        "Stage25-0",

    "reference_volume": {
        "benign_flows_per_day":
            BENIGN_FLOWS_PER_DAY,

        "semantics":
            "FIXED_BENIGN_TRAFFIC_VOLUME",

        "not_fixed_total_traffic":
            True,
    },

    "frozen_equations": {
        "B":
            "1,000,000 benign flows/day",

        "N_total":
            "B / (1 - pi)",

        "A_attack":
            "pi * B / (1 - pi)",

        "TP":
            "TPR * A_attack",

        "FN":
            "(1 - TPR) * A_attack",

        "FP":
            "FPR * B",

        "TN":
            "(1 - FPR) * B",

        "total_alerts":
            "TP + FP",

        "false_alert_fraction":
            "FP / (TP + FP) when TP + FP > 0",
    },

    "operational_implication":
        (
            "At fixed benign traffic volume and fixed FPR, false-positive "
            "volume does not decrease merely because attacks become rarer."
        ),

    "scenario_not_universal_enterprise_claim":
        True,

    "changes_after_remote_freeze":
        "FORBIDDEN",
}


# ==============================================================================
# 24. FREEZE BAYESIAN / LIKELIHOOD-RATIO EQUATIONS
# ==============================================================================

bayesian_equations = {
    "PPV":
        (
            "TPR*pi / (TPR*pi + FPR*(1-pi))"
        ),

    "NPV":
        (
            "(1-FPR)*(1-pi) / "
            "((1-FPR)*(1-pi) + (1-TPR)*pi)"
        ),

    "LR_plus":
        "TPR / FPR",

    "LR_minus":
        "(1-TPR) / (1-FPR)",

    "prior_odds":
        "pi / (1-pi)",

    "posterior_odds_after_positive":
        "prior_odds * LR_plus",

    "posterior_probability_after_positive":
        "posterior_odds / (1 + posterior_odds)",

    "PPV_cliff_general":
        (
            "pi_star_ppv_q = q*FPR / "
            "(TPR*(1-q) + q*FPR)"
        ),

    "PPV50_cliff":
        (
            "pi_star_ppv50 = FPR / (TPR + FPR)"
        ),

    "required_FPR_for_target_PPV":
        (
            "FPR_required = "
            "TPR*pi*(1-q) / (q*(1-pi))"
        ),
}


# ==============================================================================
# 25. FREEZE SOC CAPACITY MODEL
# ==============================================================================

alerts_per_analyst_day = (
    ANALYST_SHIFT_MINUTES
    /
    ALERT_SERVICE_MINUTES
)


if alerts_per_analyst_day != 240:

    raise RuntimeError(
        "Frozen analyst-capacity arithmetic changed."
    )


capacity_tiers = {}


for k in ANALYST_CAPACITY_TIERS:

    capacity_tiers[
        str(
            k
        )
    ] = {
        "analyst_days":
            k,

        "analyst_hours_per_day":
            8
            *
            k,

        "alerts_per_day":
            int(
                alerts_per_analyst_day
                *
                k
            ),

        "false_positive_only_fpr_capacity_ceiling":
            (
                alerts_per_analyst_day
                *
                k
                /
                BENIGN_FLOWS_PER_DAY
            ),
    }


analyst_capacity_payload = {
    "stage":
        "Stage25-0",

    "service_time": {
        "minutes_per_alert":
            ALERT_SERVICE_MINUTES,

        "status":
            "ASSUMED_REFERENCE_WORKLOAD_SCENARIO",

        "not_universal_SOC_constant":
            True,
    },

    "shift": {
        "minutes_per_analyst_day":
            ANALYST_SHIFT_MINUTES,

        "hours_per_analyst_day":
            8,

        "alerts_per_analyst_day":
            int(
                alerts_per_analyst_day
            ),
    },

    "capacity_tiers":
        capacity_tiers,

    "frozen_equations": {
        "false_alert_hours":
            "FP * 2 / 60",

        "total_alert_processing_hours":
            "(TP + FP) * 2 / 60",

        "ACI_k":
            "(TP + FP) / (240*k)",

        "false_positive_only_FPR_capacity":
            "(480*k/s) / B",

        "exact_total_alert_capacity_condition":
            (
                "TPR*pi*B/(1-pi) + FPR*B <= 240*k"
            ),

        "exact_total_alert_FPR_ceiling":
            (
                "FPR <= 240*k/B - TPR*pi/(1-pi); "
                "if RHS < 0, total-alert capacity is infeasible even at FPR=0"
            ),
    },

    "formal_term":
        "SOC Capacity Exceedance",

    "prohibited_formal_term":
        "SOC Bankruptcy",

    "capacity_feasibility_does_not_equal_operational_usefulness":
        True,

    "changes_after_remote_freeze":
        "FORBIDDEN",
}


# ==============================================================================
# 26. FREEZE RELATIVE COST MODEL
# ==============================================================================

cost_payload = {
    "stage":
        "Stage25-0",

    "units":
        "RELATIVE_OPERATIONAL_COST_UNITS",

    "not_currency":
        True,

    "C_FP":
        C_FP,

    "C_FN":
        C_FN,

    "ratio":
        "1:100",

    "frozen_equations": {
        "model_cost":
            "FP*C_FP + FN*C_FN",

        "ignore_cost":
            "A_attack*C_FN",

        "exact_cost_break_even_prevalence":
            (
                "pi_star_cost = "
                "(C_FP*FPR) / "
                "(C_FN*TPR + C_FP*FPR)"
            ),
    },

    "interpretation":
        (
            "Under the frozen relative-cost assumptions, pi_star_cost is the "
            "prevalence boundary at which use of the classifier and the "
            "simplified ignore/non-deployment reference have equal expected "
            "relative cost."
        ),

    "limitations": [
        (
            "These values are sensitivity-analysis units, not dollars."
        ),
        (
            "Every malicious flow must not be interpreted as an independent breach."
        ),
        (
            "The ignore reference is deliberately simplified."
        ),
    ],

    "changes_after_remote_freeze":
        "FORBIDDEN",
}


# ==============================================================================
# 27. FREEZE THRESHOLD POLICY
# ==============================================================================

threshold_policy_payload = {
    "stage":
        "Stage25-0",

    "stage22": {
        "eligible_cells": [
            "RANDOM_NATURAL",
            "CHRONOLOGICAL_NATURAL",
        ],

        "eligible_operating_points": [
            "STANDARD",
            "BALANCED",
            "SECURITY",
        ],

        "thresholds":
            "EXACT_INHERITED_FROZEN_VALUES_ONLY",
    },

    "stage24": {
        "eligible_families": [
            "STAGE24_2018_TO_2017",
            "STAGE24_2017_TO_2018",
        ],

        "eligible_cells": sorted(
            cell_id
            for cell_id in expected_cell_ids
            if cell_id.startswith(
                "STAGE24_"
            )
        ),

        "eligible_operating_points": [
            "STANDARD",
            "BALANCED",
            "SECURITY",
        ],

        "thresholds":
            "EXACT_SOURCE_FROZEN_STAGE24_VALUES_ONLY",

        "grounded_s4":
            "NOT_ELIGIBLE_ADMINISTRATIVELY_CANCELLED",
    },

    "absolutely_forbidden": [
        "target-specific threshold optimization",
        "prevalence-specific threshold optimization",
        "PPV-specific threshold selection",
        "new F1 maximization",
        "new F2 maximization",
        "new probability inference",
        "new calibration",
    ],

    "post_freeze_change":
        "FORBIDDEN",
}


# ==============================================================================
# 28. FREEZE UNCERTAINTY POLICY
# ==============================================================================

uncertainty_payload = {
    "stage":
        "Stage25-0",

    "projection_uncertainty": {
        "conditional_on_frozen_inputs_and_assumptions":
            "NONE",

        "meaning":
            (
                "Stage25 equations are deterministic transformations of the "
                "inherited TPR/FPR estimates and frozen scenario assumptions."
            ),
    },

    "empirical_estimation_uncertainty": {
        "exists":
            True,

        "source":
            "FINITE_SAMPLES_USED_TO_ESTIMATE_INHERITED_TPR_AND_FPR",

        "propagated_in_stage25":
            False,

        "reason":
            (
                "No inherited artifact provides the complete per-operating-point "
                "joint TPR/FPR sampling distributions needed for propagation "
                "across all eight Stage25 cells. Existing Stage24 paired "
                "bootstrap artifacts concern selected PR-AUC/ROC-AUC/Brier "
                "differences and are not a substitute."
            ),
    },

    "new_bootstrap_sampling":
        "FORBIDDEN",

    "reporting_language":
        (
            "Projection equations are exact conditional on frozen inputs and "
            "assumptions; projected values are not exact population truths."
        ),

    "post_freeze_change":
        "FORBIDDEN",
}


# ==============================================================================
# 29. FREEZE NUMERICAL POLICY
# ==============================================================================

numerical_policy_payload = {
    "stage":
        "Stage25-0",

    "calculation_dtype":
        "IEEE754_FLOAT64",

    "arbitrary_epsilon":
        "FORBIDDEN",

    "LR_plus": {
        "normal":
            "TPR/FPR",

        "if_FPR_zero_and_TPR_positive":
            "POSITIVE_INFINITY",

        "if_FPR_zero_and_TPR_zero":
            "UNDEFINED_NULL_0_OVER_0",
    },

    "LR_minus": {
        "normal":
            "(1-TPR)/(1-FPR)",

        "if_1_minus_FPR_zero_and_1_minus_TPR_positive":
            "POSITIVE_INFINITY",

        "if_both_numerator_and_denominator_zero":
            "UNDEFINED_NULL_0_OVER_0",
    },

    "PPV_NPV": {
        "zero_denominator":
            "UNDEFINED_NULL_WITH_EXPLICIT_STATUS",

        "no_epsilon":
            True,
    },

    "break_even_equations": {
        "zero_denominator":
            "UNDEFINED_NULL_WITH_EXPLICIT_STATUS",

        "no_grid_approximation":
            True,
    },

    "rounding": {
        "internal_computation":
            "NO_DISPLAY_ROUNDING",

        "CSV_storage":
            "FULL_PYTHON_FLOAT_REPR",

        "publication_display":
            "ROUND_ONLY_AT_PRESENTATION_LAYER",
    },

    "post_freeze_change":
        "FORBIDDEN",
}


# ==============================================================================
# 30. FREEZE INTERPRETATION MATRIX
# ==============================================================================

interpretation_matrix_payload = {
    "stage":
        "Stage25-0",

    "entries": [
        {
            "result":
                "PPV falls sharply as prevalence decreases within the same frozen cell",

            "permitted_interpretation":
                (
                    "The operating point is sensitive to prior attack prevalence."
                ),
        },

        {
            "result":
                "PPV < 10% at 0.1% prevalence",

            "permitted_interpretation":
                (
                    "Under the frozen prior-shift projection, fewer than one "
                    "in ten positive alerts corresponds to an attack."
                ),
        },

        {
            "result":
                "ACI_1 > 1",

            "permitted_interpretation":
                (
                    "Projected alert volume exceeds one assumed analyst-day "
                    "of processing capacity."
                ),
        },

        {
            "result":
                "ACI_3 > 1",

            "permitted_interpretation":
                (
                    "Projected alert volume exceeds three assumed analyst-days "
                    "of processing capacity."
                ),
        },

        {
            "result":
                "Observed FPR > capacity FPR",

            "permitted_interpretation":
                (
                    "False-alert rate alone exceeds the specified SOC capacity scenario."
                ),
        },

        {
            "result":
                "Cost(Model) > Cost(Ignore)",

            "permitted_interpretation":
                (
                    "Under the frozen 1:100 relative-cost model, the simplified "
                    "non-deployment reference has lower expected relative cost."
                ),
        },

        {
            "result":
                "Security threshold still exceeds capacity",

            "permitted_interpretation":
                (
                    "The tested FPR constraint does not guarantee feasibility "
                    "under the assumed traffic/capacity scenario."
                ),
        },

        {
            "result":
                "Ranking strong but operational projection poor",

            "permitted_interpretation":
                (
                    "Ranking quality does not by itself establish deployment utility."
                ),
        },

        {
            "result":
                "Chronological projection worse than random",

            "permitted_interpretation":
                (
                    "Frozen chronological operating characteristics yield poorer "
                    "projected utility; prevalence alone must not be assumed causal."
                ),
        },

        {
            "result":
                "Cross-dataset projection collapses",

            "permitted_interpretation":
                (
                    "The transferred operating point is not operationally robust "
                    "under the tested analytic projection."
                ),
        },

        {
            "result":
                "Model survives 0.1% stress",

            "permitted_interpretation":
                (
                    "The tested frozen operating point remains comparatively "
                    "informative under the stated assumptions; empirical deployment "
                    "validation is still required."
                ),
        },
    ],

    "between_direction_averaging":
        "FORBIDDEN",

    "between_bridge_averaging":
        "FORBIDDEN",

    "between_extractor_variant_averaging":
        "FORBIDDEN",

    "post_freeze_change":
        "FORBIDDEN",
}


# ==============================================================================
# 31. FREEZE PROHIBITED CLAIMS
# ==============================================================================

prohibited_claims_payload = {
    "stage":
        "Stage25-0",

    "claims": [
        "The model is good for enterprise deployment.",
        "The model is operationally useless.",
        "Random splitting succeeds purely because of prevalence.",
        "High F1 means low FPR.",
        "We proved the IDS field is broken.",
        "These are real SOC alert counts.",
        "Relative operational cost units are dollars.",
        "Every false negative is an independent breach.",
        "1,000,000 benign flows/day represents all enterprises.",
        "Stage25 is empirical deployment validation.",
        "The two Stage24 transfer directions can be averaged.",
        "GROUNDED_S4 was evaluated in Stage24.",
    ],

    "preferred_qualifier":
        (
            "Under the frozen prior-shift, traffic-volume, "
            "analyst-service-time, and relative-cost assumptions..."
        ),

    "post_freeze_change":
        "FORBIDDEN",
}


# ==============================================================================
# 32. FREEZE FIGURE PLAN
# ==============================================================================

figure_plan_payload = {
    "stage":
        "Stage25-0",

    "primary_figures": [
        {
            "id":
                "Figure25-A",

            "title":
                "PPV Cliff",

            "x_axis":
                "attack prevalence (log scale)",

            "y_axis":
                "PPV",

            "required_elements": [
                "all eligible frozen operating points shown separately",
                "50% PPV reference line",
                "10% PPV reference line",
                "exact observed-prevalence markers",
                "all six deployment-grid points",
            ],
        },

        {
            "id":
                "Figure25-B",

            "title":
                "SOC Capacity Exceedance",

            "x_axis":
                "attack prevalence (log scale)",

            "y_axis":
                "total alert-processing hours/day",

            "required_reference_lines_hours": [
                8,
                24,
                80,
            ],

            "required_secondary_quantity":
                "false-alert workload",
        },

        {
            "id":
                "Figure25-C",

            "title":
                "Benchmark-to-Deployment Translation",

            "observed_side": [
                "F1",
                "Precision",
                "Recall/TPR",
                "FPR",
                "Observed prevalence",
            ],

            "projection_side_at_prevalence":
                0.001,

            "projected_side": [
                "PPV",
                "FP/day",
                "TP/day",
                "Total alerts/day",
                "Analyst hours/day",
            ],

            "F1_and_PPV_are_not_interchangeable":
                True,
        },

        {
            "id":
                "Figure25-D",

            "title":
                "Required FPR for Target PPV",

            "x_axis":
                "attack prevalence (log scale)",

            "y_axis":
                "maximum permissible FPR",

            "PPV_target_curves":
                PPV_TARGETS,

            "overlay_actual_frozen_FPR":
                True,
        },
    ],

    "supplementary_figures": [
        {
            "id":
                "Figure25-E",

            "title":
                "Bayesian Evidence Translation",

            "status":
                "FROZEN_SUPPLEMENTARY_FIGURE_NOT_OUTCOME_DEPENDENT",

            "content":
                (
                    "prior probability -> posterior probability after a positive "
                    "alert for representative inherited LR+ values"
                ),
        },
    ],

    "outcome_based_figure_dropping":
        "FORBIDDEN",
}


# ==============================================================================
# 33. FREEZE REQUIRED SANITY TESTS
# ==============================================================================

sanity_test_plan = {
    "stage":
        "Stage25-0",

    "required_tests": [
        {
            "name":
                "PPV_AT_OBSERVED_PREVALENCE",

            "requirement":
                (
                    "For every inherited operating point, projection at its exact "
                    "observed prevalence must reproduce frozen precision within "
                    "numerical tolerance."
                ),
        },

        {
            "name":
                "PPV_MONOTONICITY",

            "requirement":
                (
                    "For fixed TPR>0 and FPR>0, PPV must be monotonically "
                    "increasing with prevalence."
                ),
        },

        {
            "name":
                "FP_INVARIANCE",

            "requirement":
                (
                    "For one operating point, FP = FPR*1,000,000 must be "
                    "identical across all six prevalence grid points."
                ),
        },

        {
            "name":
                "COST_BREAK_EVEN_SIGN_REVERSAL",

            "requirement":
                (
                    "Evaluate immediately below and above analytic pi_star_cost "
                    "and verify the expected model-vs-ignore cost inequality reverses."
                ),
        },

        {
            "name":
                "PPV50_EXACT_CHECK",

            "requirement":
                (
                    "At analytic pi_star_PPV50, recomputed PPV must equal 0.5 "
                    "within numerical tolerance."
                ),
        },

        {
            "name":
                "PROJECTED_CONFUSION_IDENTITIES",

            "requirement":
                (
                    "TP+FN must equal projected attack flows and FP+TN must equal "
                    "exactly 1,000,000 benign flows within floating tolerance."
                ),
        },

        {
            "name":
                "NO_PROJECTION_CELL_MISSING",

            "requirement":
                (
                    "All 24 operating points x 6 prevalences must be present "
                    "after Stage25-1."
                ),

            "expected_rows":
                24
                *
                6,
        },
    ],

    "test_dropping_after_results":
        "FORBIDDEN",
}


# ==============================================================================
# 34. FREEZE SUCCESS CONDITIONS
# ==============================================================================

success_condition_payload = {
    "stage":
        "Stage25-0",

    "operational_collapse_required":
        False,

    "valid_outcome_classes": [
        "SEVERE_BASE_RATE_COLLAPSE",
        "MODERATE_DEGRADATION",
        "THRESHOLD_SPECIFIC_SURVIVAL",
        "SECURITY_OPERATING_POINT_SURVIVAL",
        "SOC_CAPACITY_EXCEEDANCE",
        "COST_BREAK_EVEN_AT_VERY_LOW_PREVALENCE",
        "UNEXPECTED_OPERATIONAL_ROBUSTNESS",
    ],

    "rule":
        (
            "Unexpectedly favorable or unfavorable operating projections are "
            "reported exactly as produced under the frozen assumptions."
        ),

    "post_result_success_redefinition":
        "FORBIDDEN",
}


# ==============================================================================
# 35. FREEZE ANTI-ADAPTATION
# ==============================================================================

anti_adaptation_payload = {
    "stage":
        "Stage25-0",

    "after_remote_protocol_freeze": {
        "change_prevalence_grid":
            "FORBIDDEN",

        "drop_0_01_percent_prevalence":
            "FORBIDDEN",

        "change_benign_traffic_volume":
            "FORBIDDEN",

        "change_alert_service_time":
            "FORBIDDEN",

        "change_analyst_capacity_tiers":
            "FORBIDDEN",

        "change_relative_cost_ratio":
            "FORBIDDEN",

        "change_PPV_target_grid":
            "FORBIDDEN",

        "select_new_threshold":
            "FORBIDDEN",

        "target_specific_threshold_optimization":
            "FORBIDDEN",

        "prevalence_specific_threshold_optimization":
            "FORBIDDEN",

        "PPV_specific_threshold_selection":
            "FORBIDDEN",

        "new_probability_inference":
            "FORBIDDEN",

        "new_probability_array":
            "FORBIDDEN",

        "model_refit":
            "FORBIDDEN",

        "target_reopening":
            "FORBIDDEN",

        "drop_poor_operating_point":
            "FORBIDDEN",

        "add_favorable_cost_ratio_after_results":
            "FORBIDDEN",

        "relabel_relative_cost_as_currency":
            "FORBIDDEN",

        "redefine_SOC_capacity_after_results":
            "FORBIDDEN",

        "average_stage24_transfer_directions":
            "FORBIDDEN",
    },

    "unexpected_results":
        "REPORT_AS_RESULTS",
}


# ==============================================================================
# 36. BUILD INHERITED ARTIFACT HASH MANIFEST
# ==============================================================================

inherited_artifact_hashes_payload = {
    "stage":
        "Stage25-0",

    "repository_parent_commit":
        EXPECTED_PARENT,

    "byte_verified_artifacts":
        dict(
            sorted(
                artifact_hash_cache.items()
            )
        ),

    "closure_receipts": {
        "stage22_publication_closeout": {
            "path":
                str(
                    STAGE22_CLOSEOUT.relative_to(
                        REPO
                    )
                ),

            "sha256":
                stage22_closeout_sha,
        },

        "stage24_final_synthesis": {
            "path":
                str(
                    STAGE24_FINAL.relative_to(
                        REPO
                    )
                ),

            "sha256":
                stage24_final_sha,
        },

        "stage24_publication_manifest": {
            "path":
                str(
                    STAGE24_PUBLICATION_MANIFEST.relative_to(
                        REPO
                    )
                ),

            "sha256":
                stage24_pub_manifest_sha,
        },

        "stage24_final_protocol": {
            "path":
                str(
                    STAGE24_FINAL_PROTOCOL.relative_to(
                        REPO
                    )
                ),

            "sha256":
                stage24_protocol_sha,
        },

        "stage24_cicids2017_source_contract": {
            "path":
                str(
                    STAGE24_SOURCE_CONTRACT.relative_to(
                        REPO
                    )
                ),

            "sha256":
                stage24_source_contract_sha,
        },
    },

    "declared_hash_fields_from_frozen_results":
        declared_hash_receipts,

    "scientific_access_policy": {
        "probability_npz_files_opened":
            0,

        "probability_npy_files_opened":
            0,

        "probability_arrays_created":
            0,

        "model_objects_loaded":
            0,

        "model_inference_calls":
            0,

        "model_fit_calls":
            0,

        "target_reopenings":
            0,

        "note":
            (
                "Model files were read only as opaque bytes for SHA256 "
                "verification; no ML library was imported."
            ),
    },
}


# ==============================================================================
# 37. BUILD INHERITED OPERATING POINT PAYLOAD
# ==============================================================================

inherited_operating_points_payload = {
    "stage":
        "Stage25-0",

    "status":
        "FROZEN_OPERATING_POINT_INVENTORY_BEFORE_PROJECTION",

    "repository_parent_commit":
        EXPECTED_PARENT,

    "cell_count":
        len(
            inherited_cells
        ),

    "operating_point_count":
        operating_point_count,

    "required_operating_points_per_cell": [
        "STANDARD",
        "BALANCED",
        "SECURITY",
    ],

    "cells":
        inherited_cells,

    "excluded_cells": [
        {
            "cell":
                "STAGE22_RANDOM_REBALANCED",

            "reason":
                (
                    "Stage25 handoff freezes natural-prevalence Stage22 families "
                    "for primary operational translation."
                ),
        },

        {
            "cell":
                "STAGE22_CHRONOLOGICAL_REBALANCED",

            "reason":
                (
                    "Stage25 handoff freezes natural-prevalence Stage22 families "
                    "for primary operational translation."
                ),
        },

        {
            "cell":
                "STAGE22_FINAL_SINGLE_HOLDOUT",

            "reason":
                (
                    "Used as closure evidence; not one of the planned Stage25 "
                    "top-level operating-point families."
                ),
        },

        {
            "cell":
                "STAGE24_2018_TO_2017_BRIDGE62_GROUNDED_S4",

            "reason":
                "ADMINISTRATIVELY_CANCELLED_BEFORE_STAGE24_OPENING",
        },

        {
            "cell":
                "STAGE24_2018_TO_2017_BRIDGE70_GROUNDED_S4",

            "reason":
                "ADMINISTRATIVELY_CANCELLED_BEFORE_STAGE24_OPENING",
        },
    ],

    "no_new_threshold_derivation":
        True,

    "no_new_probability_access":
        True,
}


# ==============================================================================
# 38. WRITE ALL PRE-FREEZE ARTIFACTS
# ==============================================================================

protocol_payloads = {
    "prevalence_grid.json":
        prevalence_grid_payload,

    "observed_prevalence_receipts.json": {
        "stage":
            "Stage25-0",

        "status":
            "EXACT_OBSERVED_PREVALENCES_RECOVERED",

        "receipts":
            observed_prevalence_receipts,
    },

    "inherited_operating_points.json":
        inherited_operating_points_payload,

    "inherited_artifact_hashes.json":
        inherited_artifact_hashes_payload,

    "prior_shift_assumption.json":
        prior_shift_payload,

    "traffic_volume_spec.json":
        traffic_volume_payload,

    "analyst_capacity_spec.json":
        analyst_capacity_payload,

    "cost_model.json":
        cost_payload,

    "threshold_policy.json":
        threshold_policy_payload,

    "uncertainty_policy.json":
        uncertainty_payload,

    "numerical_policy.json":
        numerical_policy_payload,

    "interpretation_matrix.json":
        interpretation_matrix_payload,

    "prohibited_claims.json":
        prohibited_claims_payload,

    "figure_plan.json":
        figure_plan_payload,

    "sanity_test_plan.json":
        sanity_test_plan,

    "success_condition.json":
        success_condition_payload,

    "anti_adaptation.json":
        anti_adaptation_payload,

    "handoff_reconciliation.json":
        handoff_reconciliation,
}


for filename, payload in protocol_payloads.items():

    write_json(
        LOCK_DIR
        /
        filename,
        payload,
    )


# ==============================================================================
# 39. FREEZE RECORD
# ==============================================================================

protocol_file_hashes = {}


for filename in sorted(
    protocol_payloads
):

    path = (
        LOCK_DIR
        /
        filename
    )

    protocol_file_hashes[
        filename
    ] = sha256_file(
        path
    )


freeze_record = {
    "stage":
        "Stage25-0",

    "status":
        "COMPLETE_PROTOCOL_LOCK_READY_FOR_REMOTE_FREEZE",

    "created_at_utc":
        datetime.now(
            timezone.utc
        ).isoformat(),

    "repository_parent_commit":
        EXPECTED_PARENT,

    "scientific_objective":
        (
            "Translate frozen discrimination and operating-point characteristics "
            "under lower prior attack prevalences and finite SOC processing "
            "capacity without new modeling or inference."
        ),

    "inheritance": {
        "stage22_cells":
            2,

        "stage24_cells":
            6,

        "total_cells":
            8,

        "operating_points_per_cell":
            3,

        "total_operating_points":
            24,
    },

    "projection_grid": {
        "prevalence_points":
            6,

        "expected_projection_rows":
            24
            *
            6,

        "PPV_targets":
            5,
    },

    "absolute_rules": {
        "new_model_fits":
            0,

        "new_model_inference":
            0,

        "new_probability_arrays":
            0,

        "target_reopenings":
            0,
    },

    "scientific_access_during_stage25_0": {
        "model_fit_calls":
            0,

        "model_inference_calls":
            0,

        "probability_artifacts_opened":
            0,

        "probability_arrays_created":
            0,

        "target_feature_values_read":
            0,

        "target_labels_newly_read":
            0,

        "prevalence_projections_calculated":
            0,

        "PPV_projections_calculated":
            0,

        "SOC_workload_projections_calculated":
            0,

        "cost_projections_calculated":
            0,
    },

    "base_rate_vs_domain_shift": {
        "Stage25_isolates":
            "BASE_RATE_PRIOR_SHIFT_WITH_FIXED_TPR_FPR",

        "Stages22_and24_demonstrate":
            "TPR_FPR_CAN_CHANGE_ACROSS_TEMPORAL_AND_DOMAIN_BOUNDARIES",

        "must_not_conflate":
            True,
    },

    "success_requires_operational_collapse":
        False,

    "next_authorized_action_after_remote_verification":
        "STAGE25_1_BAYESIAN_PROJECTIONS",

    "next_action_before_remote_verification":
        "NONE",

    "protocol_file_hashes":
        protocol_file_hashes,

    "handoff_discrepancies":
        0,
}


FREEZE_RECORD_PATH = (
    LOCK_DIR
    /
    "freeze_record.json"
)


write_json(
    FREEZE_RECORD_PATH,
    freeze_record,
)


freeze_record_sha = sha256_file(
    FREEZE_RECORD_PATH
)


FREEZE_SHA_PATH = (
    LOCK_DIR
    /
    "freeze_record.sha256"
)


write_text(
    FREEZE_SHA_PATH,
    (
        f"{freeze_record_sha}  "
        f"{FREEZE_RECORD_PATH.name}"
    ),
)


# ==============================================================================
# 40. LOCK DIRECTORY CHECKSUM MANIFEST
# ==============================================================================

CHECKSUMS_PATH = (
    LOCK_DIR
    /
    "checksums.sha256"
)


checksum_lines = []


for path in sorted(
    LOCK_DIR.iterdir(),
    key=lambda p:
        p.name,
):

    if path == CHECKSUMS_PATH:

        continue

    checksum_lines.append(
        f"{sha256_file(path)}  {path.name}"
    )


write_text(
    CHECKSUMS_PATH,
    "\n".join(
        checksum_lines
    ),
)


print("=" * 118)
print("STAGE25-0 LOCAL PROTOCOL FREEZE")
print("=" * 118)

print(
    "Lock directory:"
)

print(
    " ",
    LOCK_DIR.relative_to(
        REPO
    )
)

print()

print(
    "Protocol JSON files:",
    len(
        protocol_payloads
    )
    +
    1,
)

print(
    "Inherited cells:",
    len(
        inherited_cells
    ),
)

print(
    "Inherited operating points:",
    operating_point_count,
)

print(
    "Future projection rows frozen:",
    operating_point_count
    *
    len(
        PREVALENCE_GRID
    ),
)

print()

print(
    "Freeze record SHA:"
)

print(
    " ",
    freeze_record_sha
)

print()

print(
    "PROJECTIONS CALCULATED: 0"
)

print(
    "MODEL FITS:             0"
)

print(
    "MODEL INFERENCE:        0"
)

print(
    "PROBABILITY ARRAYS:     0"
)

print(
    "TARGET REOPENINGS:      0"
)

print()


# ==============================================================================
# 41. GIT DIRTY-STATE SAFETY
# ==============================================================================

print("=" * 118)
print("GIT SAFETY AUDIT")
print("=" * 118)


modified_tracked = {
    line
    for line in git_cmd(
        "diff",
        "--name-only",
    ).splitlines()
    if line
}


untracked = {
    line
    for line in git_cmd(
        "ls-files",
        "--others",
        "--exclude-standard",
    ).splitlines()
    if line
}


dirty_paths = (
    modified_tracked
    |
    untracked
)


allowed_prefix = (
    "results/stage25_prevalence_stress/"
    "stage25_0_protocol_lock/"
)


unexpected = [
    path
    for path in sorted(
        dirty_paths
    )
    if not path.startswith(
        allowed_prefix
    )
]


if unexpected:

    raise RuntimeError(
        "\nUnexpected repository changes before Stage25-0 commit:\n"
        +
        "\n".join(
            unexpected
        )
    )


if not dirty_paths:

    raise RuntimeError(
        "No Stage25-0 files found to commit."
    )


print(
    "[PASS] Only Stage25-0 protocol-lock artifacts are dirty."
)

print()


# ==============================================================================
# 42. REMOTE PARENT RECHECK BEFORE COMMIT
# ==============================================================================

remote_precommit = git_cmd(
    "ls-remote",
    "origin",
    "refs/heads/main",
    auth_header=auth_header,
).split()[0]


if remote_precommit != EXPECTED_PARENT:

    raise RuntimeError(
        "\nRemote main moved during Stage25-0 preparation.\n"
        f"Expected: {EXPECTED_PARENT}\n"
        f"Actual:   {remote_precommit}\n\n"
        "Protocol has NOT been committed."
    )


print(
    "[PASS] Remote main unchanged before protocol-lock commit."
)

print()


# ==============================================================================
# 43. GIT AUTHOR SAFETY
# ==============================================================================

author_name = git_cmd(
    "config",
    "--local",
    "--get",
    "user.name",
    check=False,
)


author_email = git_cmd(
    "config",
    "--local",
    "--get",
    "user.email",
    check=False,
)


if not author_name:

    git_cmd(
        "config",
        "--local",
        "user.name",
        git_cmd(
            "log",
            "-1",
            "--format=%an",
        ),
    )


if not author_email:

    git_cmd(
        "config",
        "--local",
        "user.email",
        git_cmd(
            "log",
            "-1",
            "--format=%ae",
        ),
    )


# ==============================================================================
# 44. STAGE ONLY THE STAGE25-0 LOCK
# ==============================================================================

git_cmd(
    "add",
    "--",
    str(
        LOCK_DIR.relative_to(
            REPO
        )
    ),
)


staged = {
    line
    for line in git_cmd(
        "diff",
        "--cached",
        "--name-only",
    ).splitlines()
    if line
}


if not staged:

    raise RuntimeError(
        "No Stage25-0 files staged."
    )


unexpected_staged = [
    path
    for path in sorted(
        staged
    )
    if not path.startswith(
        allowed_prefix
    )
]


if unexpected_staged:

    raise RuntimeError(
        "\nUnexpected files staged:\n"
        +
        "\n".join(
            unexpected_staged
        )
    )


remaining_unstaged = {
    line
    for line in git_cmd(
        "diff",
        "--name-only",
    ).splitlines()
    if line
}


remaining_untracked = {
    line
    for line in git_cmd(
        "ls-files",
        "--others",
        "--exclude-standard",
    ).splitlines()
    if line
}


if (
    remaining_unstaged
    or
    remaining_untracked
):

    raise RuntimeError(
        "\nStage25-0 changes remain unstaged.\n"
        f"Tracked: {sorted(remaining_unstaged)}\n"
        f"Untracked: {sorted(remaining_untracked)}"
    )


print(
    "[PASS] Only complete Stage25-0 lock is staged."
)

print()


# ==============================================================================
# 45. COMMIT
# ==============================================================================

print("=" * 118)
print("COMMIT STAGE25-0 PROTOCOL LOCK")
print("=" * 118)


commit_output = git_cmd(
    "commit",
    "-m",
    "stage25: freeze prevalence operational stress protocol",
)


print(
    commit_output
)

print()


commit = git_cmd(
    "rev-parse",
    "HEAD",
)


parent = git_cmd(
    "rev-parse",
    "HEAD^",
)


if parent != EXPECTED_PARENT:

    raise RuntimeError(
        "\nStage25-0 commit parent mismatch.\n"
        f"Expected: {EXPECTED_PARENT}\n"
        f"Actual:   {parent}"
    )


print(
    "Stage25-0 commit:"
)

print(
    " ",
    commit
)

print()


# ==============================================================================
# 46. PUSH + REMOTE VERIFICATION
# ==============================================================================

print("=" * 118)
print("PUSH + REMOTE VERIFY")
print("=" * 118)


push_output = git_cmd(
    "push",
    "origin",
    "HEAD:main",
    auth_header=auth_header,
)


print(
    push_output
)

print()


remote_after = git_cmd(
    "ls-remote",
    "origin",
    "refs/heads/main",
    auth_header=auth_header,
).split()[0]


if remote_after != commit:

    raise RuntimeError(
        "\nRemote verification failed.\n"
        f"Local:  {commit}\n"
        f"Remote: {remote_after}"
    )


final_status = git_cmd(
    "status",
    "--porcelain",
)


if final_status:

    raise RuntimeError(
        "\nRepository is not clean after Stage25-0 push:\n"
        +
        final_status
    )


print(
    "[PASS] Remote main == Stage25-0 protocol-lock commit."
)

print(
    "[PASS] Repository clean."
)

print()


# ==============================================================================
# 47. FINAL LOCK SUMMARY
# ==============================================================================

print("=" * 118)
print("STAGE25-0 PROTOCOL LOCK: PASS")
print("=" * 118)

print()

print(
    "Parent Stage24 closeout:"
)

print(
    " ",
    EXPECTED_PARENT
)

print()

print(
    "Stage25-0 commit:"
)

print(
    " ",
    commit
)

print()

print(
    "Remote main:"
)

print(
    " ",
    remote_after
)

print()

print(
    "Freeze record SHA:"
)

print(
    " ",
    freeze_record_sha
)

print()

print(
    "Inherited frozen cells:        8"
)

print(
    "Inherited operating points:    24"
)

print(
    "Frozen prevalence grid:        6 points"
)

print(
    "Frozen PPV target grid:        5 points"
)

print(
    "Frozen benign flows/day:       1,000,000"
)

print(
    "Frozen alert service time:     2 minutes"
)

print(
    "Frozen analyst tiers:          1 / 3 / 10"
)

print(
    "Frozen relative costs:         FP=1 / FN=100"
)

print()

print(
    "NEW MODEL FITS:                0"
)

print(
    "NEW MODEL INFERENCE:           0"
)

print(
    "NEW PROBABILITY ARRAYS:        0"
)

print(
    "TARGET REOPENINGS:             0"
)

print()

print(
    "STAGE25 PROJECTIONS COMPUTED:  0"
)

print()

print(
    "NEXT AUTHORIZED ACTION:"
)

print(
    "  Stage25-1 — Bayesian prevalence projections"
)

print(
    "  ONLY AFTER independent GitHub verification of this lock."
)

print()

print(
    "STOP HERE — DO NOT CALCULATE PPV YET."
)

print("=" * 118)

# %% [Stage25 notebook cell 2]
# ==============================================================================
# STAGE25-0-R1 — COMPLETE PROTOCOL-LOCK RECOVERY
#
# Root cause of previous failure:
#   Stage24-2D bridge70 stores:
#
#       models.lightgbm.model_sha256
#       models.xgboost.model_sha256
#
#   but intentionally does NOT repeat model_file.
#
#   bridge70 reuses the exact Stage22R CHRONOLOGICAL_NATURAL models.
#
# Recovery:
#   Use canonical frozen model paths according to bridge/direction and verify
#   the bytes against the SHA256 values declared by the Stage24 receipts.
#
# PREVIOUS FAILURE OCCURRED BEFORE:
#   - creation of stage25_0_protocol_lock
#   - any Stage25 projection
#   - any PPV calculation
#   - any SOC projection
#   - any cost projection
#   - any git add / commit / push
#
# ABSOLUTE STAGE25 ACCOUNTING REMAINS:
#
#   NEW MODEL FITS:             0
#   NEW MODEL INFERENCE:        0
#   NEW PROBABILITY ARRAYS:     0
#   TARGET REOPENINGS:          0
#   STAGE25 PROJECTIONS:        0
#
# This cell performs Stage25-0 ONLY.
# ==============================================================================

from __future__ import annotations

import os
import json
import base64
import hashlib
import subprocess
from pathlib import Path
from datetime import datetime, timezone


print("=" * 120)
print("STAGE25-0-R1 — COMPLETE PROTOCOL-LOCK RECOVERY")
print("=" * 120)
print()


# ==============================================================================
# 0. FROZEN REPOSITORY ANCHORS
# ==============================================================================

REPO_URL = (
    "https://github.com/"
    "themubasshir/ids2018-validation-safe-ablation.git"
)

REPO = Path(
    "/kaggle/working/ids2018-validation-safe-ablation"
)

EXPECTED_PARENT = (
    "ad5a01ae9021183f6c5b8046c2647fd5dad7cb6d"
)

EXPECTED_STAGE24_FINAL_SYNTHESIS_SHA = (
    "785bbcb00140f4d7e07e9b49ad33924166b5995e66a229c986d5b1abcbcaee4b"
)

EXPECTED_STAGE24_PUBLICATION_MANIFEST_SHA = (
    "7cc628debf53e22ee0c71e21e307f7e9fa766cbeecdd527174db2dbe47e3bf82"
)

EXPECTED_STAGE24_PROTOCOL_SHA = (
    "8ef234a9d283f2008f21b9add4361f14328d1f3c1cffa278077f59d9eb9e37c2"
)

EXPECTED_STAGE24_CICIDS2017_CONTRACT_SHA = (
    "96f7fc5c0227660fe8ec17f5173630ee2ac71f6be199e81ee37dac0ad25d9779"
)

EXPECTED_STAGE22_MEMBERSHIP_SUMMARY_SHA = (
    "b4dc00345ba8ca91a1d194949ca0321225676664c84a11b45cf4ee4bfcfa799d"
)

EXPECTED_STAGE22_RANDOM_MEMBERSHIP_SHA = (
    "8a308aa5c28008895559a87ba2335a82eac69a4a3b99303d42d598f7afbe2fad"
)

EXPECTED_STAGE22_DAY_OFFSETS_SHA = (
    "22a1c2b9b208596d53d1e860a2ec426542a22f23de2a8236baa4dae2583e0d5a"
)


# ==============================================================================
# 1. FROZEN STAGE25 DESIGN
# ==============================================================================

PREVALENCE_GRID = [
    0.10,
    0.03,
    0.01,
    0.003,
    0.001,
    0.0001,
]

PPV_TARGETS = [
    0.10,
    0.25,
    0.50,
    0.75,
    0.90,
]

BENIGN_FLOWS_PER_DAY = 1_000_000

ALERT_SERVICE_MINUTES = 2

ANALYST_SHIFT_MINUTES = 480

ANALYST_TIERS = [
    1,
    3,
    10,
]

C_FP = 1

C_FN = 100


# ==============================================================================
# 2. HELPERS
# ==============================================================================

def run_cmd(
    args,
    *,
    cwd=None,
    check=True,
):

    p = subprocess.run(
        [str(x) for x in args],
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    if check and p.returncode != 0:

        raise RuntimeError(
            "\nCommand failed:\n"
            +
            " ".join(
                str(x)
                for x in args
            )
            +
            "\n\n"
            +
            (p.stdout or "")
        )

    return (
        p.stdout
        or
        ""
    ).strip()


def git_cmd(
    *args,
    auth_header=None,
    check=True,
):

    cmd = [
        "git"
    ]

    if auth_header is not None:

        cmd += [
            "-c",
            "credential.helper=",
            "-c",
            f"http.extraHeader=AUTHORIZATION: Basic {auth_header}",
        ]

    cmd.extend(
        str(x)
        for x in args
    )

    return run_cmd(
        cmd,
        cwd=REPO,
        check=check,
    )


def sha256_file(
    path,
):

    path = Path(
        path
    )

    h = hashlib.sha256()

    with path.open(
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

    return h.hexdigest()


def load_json(
    path,
):

    path = Path(
        path
    )

    if not path.is_file():

        raise RuntimeError(
            f"Missing JSON:\n{path}"
        )

    return json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )


def write_json(
    path,
    payload,
):

    path = Path(
        path
    )

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    path.write_text(
        json.dumps(
            payload,
            indent=2,
            sort_keys=True,
            ensure_ascii=False,
        )
        +
        "\n",
        encoding="utf-8",
    )


def write_text(
    path,
    text,
):

    path = Path(
        path
    )

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    path.write_text(
        str(
            text
        ).rstrip()
        +
        "\n",
        encoding="utf-8",
    )


def verify_sha(
    path,
    expected,
    label,
):

    path = Path(
        path
    )

    if not path.is_file():

        raise RuntimeError(
            f"Missing {label}:\n{path}"
        )

    actual = sha256_file(
        path
    )

    if actual != expected:

        raise RuntimeError(
            f"\n{label} SHA mismatch.\n"
            f"Expected: {expected}\n"
            f"Actual:   {actual}\n"
            f"Path:     {path}"
        )

    return actual


def verify_sidecar(
    artifact,
):

    artifact = Path(
        artifact
    )

    sidecar = artifact.with_suffix(
        ".sha256"
    )

    if not sidecar.is_file():

        raise RuntimeError(
            "\nMissing SHA sidecar:\n"
            f"{sidecar}"
        )

    expected = (
        sidecar
        .read_text(
            encoding="utf-8"
        )
        .strip()
        .split()[0]
    )

    actual = sha256_file(
        artifact
    )

    if actual != expected:

        raise RuntimeError(
            "\nSHA sidecar mismatch.\n"
            f"Artifact: {artifact}\n"
            f"Expected: {expected}\n"
            f"Actual:   {actual}"
        )

    return actual


def safe_div(
    a,
    b,
):

    if b == 0:

        return None

    return (
        a
        /
        b
    )


def assert_close(
    actual,
    expected,
    *,
    tolerance=5e-15,
    label="value",
):

    if (
        actual is None
        or
        expected is None
    ):

        if actual != expected:

            raise RuntimeError(
                f"{label}: None mismatch"
            )

        return

    delta = abs(
        float(
            actual
        )
        -
        float(
            expected
        )
    )

    if delta > tolerance:

        raise RuntimeError(
            "\nFrozen-value mismatch.\n"
            f"{label}\n"
            f"Expected: {expected}\n"
            f"Actual:   {actual}\n"
            f"Delta:    {delta}"
        )


def canonical_op(
    source,
):

    tp = int(
        source[
            "tp"
        ]
    )

    tn = int(
        source[
            "tn"
        ]
    )

    fp = int(
        source[
            "fp"
        ]
    )

    fn = int(
        source[
            "fn"
        ]
    )

    attack = (
        tp
        +
        fn
    )

    benign = (
        tn
        +
        fp
    )

    rows = (
        attack
        +
        benign
    )

    tpr = safe_div(
        tp,
        attack,
    )

    fpr = safe_div(
        fp,
        benign,
    )

    precision = safe_div(
        tp,
        tp
        +
        fp,
    )

    prevalence = safe_div(
        attack,
        rows,
    )


    if "recall" in source:

        assert_close(
            tpr,
            source[
                "recall"
            ],
            label="TPR/recall",
        )


    if "fpr" in source:

        assert_close(
            fpr,
            source[
                "fpr"
            ],
            label="FPR",
        )


    if "precision" in source:

        assert_close(
            precision,
            source[
                "precision"
            ],
            label="precision",
        )


    return {
        "threshold":
            float(
                source[
                    "threshold"
                ]
            ),

        "tp":
            tp,

        "tn":
            tn,

        "fp":
            fp,

        "fn":
            fn,

        "attack":
            attack,

        "benign":
            benign,

        "rows":
            rows,

        "tpr":
            float(
                tpr
            ),

        "recall":
            float(
                tpr
            ),

        "fpr":
            float(
                fpr
            ),

        "precision":
            (
                None
                if precision is None
                else float(
                    precision
                )
            ),

        "f1":
            (
                None
                if source.get(
                    "f1"
                ) is None
                else float(
                    source[
                        "f1"
                    ]
                )
            ),

        "f2":
            (
                None
                if source.get(
                    "f2"
                ) is None
                else float(
                    source[
                        "f2"
                    ]
                )
            ),

        "fnr":
            float(
                1.0
                -
                tpr
            ),

        "observed_prevalence":
            float(
                prevalence
            ),
    }


def extract_stage22_ops(
    result,
):

    output = {}

    for name in [
        "standard",
        "balanced",
        "security",
    ]:

        source = (
            result[
                "operating_points"
            ][
                name
            ]
        )

        if (
            isinstance(
                source,
                dict,
            )
            and
            "result" in source
        ):

            source = source[
                "result"
            ]

        output[
            name.upper()
        ] = canonical_op(
            source
        )

    return output


def stage24_metrics(
    result,
):

    metrics = result[
        "metrics"
    ]

    if (
        isinstance(
            metrics,
            dict,
        )
        and
        "values" in metrics
    ):

        metrics = metrics[
            "values"
        ]

    return metrics


def extract_stage24_ops(
    result,
):

    thresholded = stage24_metrics(
        result
    )[
        "thresholded"
    ]

    return {
        name.upper():
            canonical_op(
                thresholded[
                    name
                ]
            )
        for name in [
            "standard",
            "balanced",
            "security",
        ]
    }


def population_from_ops(
    ops,
    cell_id,
):

    identities = {
        (
            op[
                "attack"
            ],
            op[
                "benign"
            ],
            op[
                "rows"
            ],
        )
        for op in ops.values()
    }

    if len(
        identities
    ) != 1:

        raise RuntimeError(
            f"{cell_id}: operating-point populations differ."
        )

    attack, benign, rows = next(
        iter(
            identities
        )
    )

    return {
        "attack":
            int(
                attack
            ),

        "benign":
            int(
                benign
            ),

        "rows":
            int(
                rows
            ),

        "observed_prevalence":
            float(
                attack
                /
                rows
            ),
    }


def recursive_sha_fields(
    obj,
    *,
    prefix="root",
    output=None,
):

    if output is None:

        output = []

    if isinstance(
        obj,
        dict,
    ):

        for key, value in obj.items():

            child = (
                prefix
                +
                "."
                +
                str(
                    key
                )
            )

            if (
                isinstance(
                    value,
                    str,
                )
                and
                key.lower().endswith(
                    "sha256"
                )
                and
                len(
                    value
                )
                ==
                64
            ):

                output.append(
                    {
                        "json_path":
                            child,

                        "sha256":
                            value,
                    }
                )

            else:

                recursive_sha_fields(
                    value,
                    prefix=child,
                    output=output,
                )


    elif isinstance(
        obj,
        list,
    ):

        for index, value in enumerate(
            obj
        ):

            recursive_sha_fields(
                value,
                prefix=(
                    f"{prefix}[{index}]"
                ),
                output=output,
            )

    return output


def select_target_identity(
    result,
):

    population = result.get(
        "target_population",
        {}
    )

    if not isinstance(
        population,
        dict,
    ):

        return {}

    keep = [
        "dataset",
        "file",
        "rows",
        "benign",
        "attack",
        "prevalence",
        "binary_label_sha256",
        "original_row_index_sha256",
        "clean_position_sha256",
        "raw_source_sha256",
        "raw_source_expected_sha256",
        "stage22r_day07_cache_expected_sha256",
        "canonical_row_order",
        "materialization_mode",
        "membership_source",
    ]

    return {
        key:
            population[
                key
            ]
        for key in keep
        if key in population
    }


# ==============================================================================
# 3. GITHUB CREDENTIAL
# ==============================================================================

print("=" * 120)
print("GITHUB CREDENTIAL")
print("=" * 120)


github_token = None

token_source = None


try:

    from kaggle_secrets import UserSecretsClient

    client = UserSecretsClient()

    for name in [
        "GITHUB_TOKEN",
        "github_token",
        "GH_TOKEN",
        "GITHUB_PAT",
        "github_pat",
    ]:

        try:

            value = client.get_secret(
                name
            )

            if (
                value
                and
                value.strip()
            ):

                github_token = value.strip()

                token_source = name

                break

        except Exception:

            pass

except Exception:

    pass


if github_token is None:

    for name in [
        "GITHUB_TOKEN",
        "GH_TOKEN",
    ]:

        value = os.environ.get(
            name
        )

        if (
            value
            and
            value.strip()
        ):

            github_token = value.strip()

            token_source = (
                "ENV:"
                +
                name
            )

            break


if github_token is None:

    raise RuntimeError(
        "GitHub token unavailable."
    )


auth_header = base64.b64encode(
    (
        "x-access-token:"
        +
        github_token
    ).encode()
).decode()


print(
    "GitHub credential:",
    token_source,
)

print()


# ==============================================================================
# 4. REPOSITORY RECOVERY GATE
# ==============================================================================

print("=" * 120)
print("REPOSITORY RECOVERY GATE")
print("=" * 120)


if not REPO.exists():

    run_cmd(
        [
            "git",
            "clone",
            "--depth",
            "1",
            "--branch",
            "main",
            REPO_URL,
            str(
                REPO
            ),
        ]
    )


if not (
    REPO
    /
    ".git"
).is_dir():

    raise RuntimeError(
        "Repository path is invalid."
    )


head = git_cmd(
    "rev-parse",
    "HEAD",
)


remote_before = git_cmd(
    "ls-remote",
    "origin",
    "refs/heads/main",
    auth_header=auth_header,
).split()[0]


status = git_cmd(
    "status",
    "--porcelain",
)


print(
    "Local HEAD: ",
    head,
)

print(
    "Remote main:",
    remote_before,
)


if head != EXPECTED_PARENT:

    raise RuntimeError(
        "\nUnexpected local HEAD.\n"
        f"Expected: {EXPECTED_PARENT}\n"
        f"Actual:   {head}"
    )


if remote_before != EXPECTED_PARENT:

    raise RuntimeError(
        "\nUnexpected remote main.\n"
        f"Expected: {EXPECTED_PARENT}\n"
        f"Actual:   {remote_before}"
    )


if status:

    raise RuntimeError(
        "\nRepository is dirty before recovery:\n"
        +
        status
    )


print(
    "[PASS] Previous failed Stage25-0 attempt left repository untouched."
)

print(
    "[PASS] No Stage25 commit exists yet."
)

print()


# ==============================================================================
# 5. PATHS
# ==============================================================================

RESULTS = (
    REPO
    /
    "results"
)

STAGE25_BASE = (
    RESULTS
    /
    "stage25_prevalence_stress"
)

LOCK_DIR = (
    STAGE25_BASE
    /
    "stage25_0_protocol_lock"
)


if LOCK_DIR.exists():

    existing = list(
        LOCK_DIR.iterdir()
    )

    if existing:

        raise RuntimeError(
            "\nUnexpected existing Stage25 lock artifacts:\n"
            +
            "\n".join(
                str(
                    p
                )
                for p in existing
            )
        )


# ------------------------------------------------------------------------------
# Stage22R
# ------------------------------------------------------------------------------

STAGE22_CLOSEOUT = (
    RESULTS
    /
    "stage22r_training/"
    "stage22r_publication_closeout/"
    "stage22r_publication_closeout_manifest.json"
)

STAGE22_MEMBERSHIP_SUMMARY = (
    RESULTS
    /
    "stage22r_protocol_recovery/"
    "stage22r_1b1_development_memberships/"
    "stage22r_1b1_membership_summary.json"
)

STAGE22_RANDOM_MEMBERSHIP = (
    RESULTS
    /
    "stage22r_protocol_recovery/"
    "stage22r_1b1_development_memberships/"
    "random_validation.packbits"
)

STAGE22_DAY_OFFSETS = (
    RESULTS
    /
    "stage22r_protocol_recovery/"
    "stage22r_1b1_development_memberships/"
    "stage22r_1b1_day_offsets.csv"
)

STAGE22_RANDOM_RESULT = (
    RESULTS
    /
    "stage22r_training/"
    "stage22r_2a_random_natural/"
    "stage22r_2a_random_natural_result.json"
)

STAGE22_CHRON_RESULT = (
    RESULTS
    /
    "stage22r_training/"
    "stage22r_2c_chronological_natural/"
    "stage22r_2c_chronological_natural_result.json"
)

STAGE22_RANDOM_THRESHOLD_GRID = (
    STAGE22_RANDOM_RESULT.parent
    /
    "random_natural_validation_threshold_grid.csv"
)

STAGE22_CHRON_THRESHOLD_GRID = (
    STAGE22_CHRON_RESULT.parent
    /
    "chronological_natural_validation_threshold_grid.csv"
)

STAGE22_RANDOM_LGBM = (
    STAGE22_RANDOM_RESULT.parent
    /
    "random_natural_lightgbm_model.txt"
)

STAGE22_RANDOM_XGB = (
    STAGE22_RANDOM_RESULT.parent
    /
    "random_natural_xgboost_model.json"
)

STAGE22_CHRON_LGBM = (
    STAGE22_CHRON_RESULT.parent
    /
    "chronological_natural_lightgbm_model.txt"
)

STAGE22_CHRON_XGB = (
    STAGE22_CHRON_RESULT.parent
    /
    "chronological_natural_xgboost_model.json"
)


# ------------------------------------------------------------------------------
# Stage24 closure
# ------------------------------------------------------------------------------

STAGE24_ROOT = (
    RESULTS
    /
    "stage24_cross_dataset"
)

STAGE24_FINAL = (
    STAGE24_ROOT
    /
    "stage24_6_final_synthesis/"
    "stage24_6_final_synthesis.json"
)

STAGE24_PUBLICATION_MANIFEST = (
    STAGE24_ROOT
    /
    "stage24_publication_package/"
    "stage24_publication_package_manifest.json"
)

STAGE24_PROTOCOL = (
    STAGE24_ROOT
    /
    "stage24_0_protocol_lock/"
    "stage24_0c_final_preopening_protocol_lock.json"
)

STAGE24_CICIDS2017_CONTRACT = (
    STAGE24_ROOT
    /
    "stage24_0_protocol_lock/"
    "stage24_0b2_complete_cicids2017_source_contract.json"
)


# ------------------------------------------------------------------------------
# Stage24 target results
# ------------------------------------------------------------------------------

STAGE24_2A = (
    STAGE24_ROOT
    /
    "stage24_2_primary_target_openings/"
    "stage24_2a_bridge62_published/"
    "stage24_2a_bridge62_published_result.json"
)

STAGE24_2B = (
    STAGE24_ROOT
    /
    "stage24_2_primary_target_openings/"
    "stage24_2b_bridge62_flag_corrected/"
    "stage24_2b_bridge62_flag_corrected_identity_result.json"
)

STAGE24_2C = (
    STAGE24_ROOT
    /
    "stage24_2_primary_target_openings/"
    "stage24_2c_bridge70_published/"
    "stage24_2c_bridge70_published_result.json"
)

STAGE24_2D = (
    STAGE24_ROOT
    /
    "stage24_2_primary_target_openings/"
    "stage24_2d_bridge70_flag_corrected/"
    "stage24_2d_bridge70_flag_corrected_result.json"
)

STAGE24_5A = (
    STAGE24_ROOT
    /
    "stage24_5_secondary_target_openings/"
    "stage24_5a_bridge62_ids2018_feb28/"
    "stage24_5a_secondary_bridge62_ids2018_feb28_result.json"
)

STAGE24_5B = (
    STAGE24_ROOT
    /
    "stage24_5_secondary_target_openings/"
    "stage24_5b_bridge70_ids2018_feb28/"
    "stage24_5b_secondary_bridge70_ids2018_feb28_result.json"
)


# ------------------------------------------------------------------------------
# Stage24 source models + threshold grids
# ------------------------------------------------------------------------------

PRIMARY_B62_DIR = (
    STAGE24_ROOT
    /
    "stage24_1_primary_source_sanity/"
    "stage24_1b_bridge62_source_refit"
)

PRIMARY_B62_LGBM = (
    PRIMARY_B62_DIR
    /
    "bridge62_lightgbm_model.txt"
)

PRIMARY_B62_XGB = (
    PRIMARY_B62_DIR
    /
    "bridge62_xgboost_model.json"
)

PRIMARY_B62_THRESHOLD_GRID = (
    PRIMARY_B62_DIR
    /
    "bridge62_validation_threshold_grid.csv"
)


SECONDARY_B62_DIR = (
    STAGE24_ROOT
    /
    "stage24_4_secondary_source_training/"
    "stage24_4a_bridge62_xgboost"
)

SECONDARY_B62_MODEL = (
    SECONDARY_B62_DIR
    /
    "secondary_bridge62_xgboost_model.json"
)

SECONDARY_B62_THRESHOLD_GRID = (
    SECONDARY_B62_DIR
    /
    "secondary_bridge62_validation_threshold_grid.csv"
)

SECONDARY_B62_SOURCE_RESULT = (
    SECONDARY_B62_DIR
    /
    "stage24_4a_secondary_bridge62_result.json"
)


SECONDARY_B70_DIR = (
    STAGE24_ROOT
    /
    "stage24_4_secondary_source_training/"
    "stage24_4b_bridge70_xgboost"
)

SECONDARY_B70_MODEL = (
    SECONDARY_B70_DIR
    /
    "secondary_bridge70_xgboost_model.json"
)

SECONDARY_B70_THRESHOLD_GRID = (
    SECONDARY_B70_DIR
    /
    "secondary_bridge70_validation_threshold_grid.csv"
)

SECONDARY_B70_SOURCE_RESULT = (
    SECONDARY_B70_DIR
    /
    "stage24_4b_secondary_bridge70_result.json"
)


# ==============================================================================
# 6. CLOSURE VERIFICATION
# ==============================================================================

print("=" * 120)
print("FROZEN CLOSURE VERIFICATION")
print("=" * 120)


stage22_closeout = load_json(
    STAGE22_CLOSEOUT
)


if (
    stage22_closeout[
        "scientific_result"
    ][
        "holdout_status"
    ]
    !=
    "PERMANENTLY_CLOSED"
):

    raise RuntimeError(
        "Stage22R holdout closure changed."
    )


stage24_final_sha = verify_sidecar(
    STAGE24_FINAL
)


if (
    stage24_final_sha
    !=
    EXPECTED_STAGE24_FINAL_SYNTHESIS_SHA
):

    raise RuntimeError(
        "Stage24 final synthesis SHA changed."
    )


stage24_final = load_json(
    STAGE24_FINAL
)


if (
    stage24_final[
        "status"
    ]
    !=
    "STAGE24_CROSS_DATASET_AUDIT_COMPLETE"
):

    raise RuntimeError(
        "Stage24 status changed."
    )


if (
    stage24_final[
        "completion"
    ][
        "scientific_fits"
    ]
    !=
    "4/4"
):

    raise RuntimeError(
        "Stage24 fit accounting changed."
    )


if (
    stage24_final[
        "completion"
    ][
        "evaluable_target_openings"
    ]
    !=
    "6/6"
):

    raise RuntimeError(
        "Stage24 target-opening accounting changed."
    )


stage24_pub_sha = verify_sidecar(
    STAGE24_PUBLICATION_MANIFEST
)


if (
    stage24_pub_sha
    !=
    EXPECTED_STAGE24_PUBLICATION_MANIFEST_SHA
):

    raise RuntimeError(
        "Stage24 publication manifest changed."
    )


stage24_protocol_sha = verify_sidecar(
    STAGE24_PROTOCOL
)


if (
    stage24_protocol_sha
    !=
    EXPECTED_STAGE24_PROTOCOL_SHA
):

    raise RuntimeError(
        "Stage24 protocol SHA changed."
    )


stage24_contract_sha = verify_sidecar(
    STAGE24_CICIDS2017_CONTRACT
)


if (
    stage24_contract_sha
    !=
    EXPECTED_STAGE24_CICIDS2017_CONTRACT_SHA
):

    raise RuntimeError(
        "Stage24 CICIDS2017 contract changed."
    )


print(
    "Stage22R holdout:        PERMANENTLY_CLOSED"
)

print(
    "Stage24 final SHA:      ",
    stage24_final_sha,
)

print(
    "Stage24 protocol SHA:   ",
    stage24_protocol_sha,
)

print(
    "Stage24 contract SHA:   ",
    stage24_contract_sha,
)

print()

print(
    "[PASS] Stage22R and Stage24 scientific state remains closed."
)

print()


# ==============================================================================
# 7. SPLIT RECEIPTS
# ==============================================================================

print("=" * 120)
print("FROZEN SPLIT RECEIPTS")
print("=" * 120)


membership_summary = load_json(
    STAGE22_MEMBERSHIP_SUMMARY
)


membership_summary_sha = verify_sha(
    STAGE22_MEMBERSHIP_SUMMARY,
    EXPECTED_STAGE22_MEMBERSHIP_SUMMARY_SHA,
    "Stage22R membership summary",
)


random_membership_sha = verify_sha(
    STAGE22_RANDOM_MEMBERSHIP,
    EXPECTED_STAGE22_RANDOM_MEMBERSHIP_SHA,
    "Stage22R random membership",
)


day_offsets_sha = verify_sha(
    STAGE22_DAY_OFFSETS,
    EXPECTED_STAGE22_DAY_OFFSETS_SHA,
    "Stage22R day offsets",
)


print(
    "Membership summary SHA:",
    membership_summary_sha,
)

print(
    "Random split SHA:      ",
    random_membership_sha,
)

print(
    "Chronological receipt: ",
    day_offsets_sha,
)

print()


# ==============================================================================
# 8. LOAD RESULT RECEIPTS
# ==============================================================================

stage22_random = load_json(
    STAGE22_RANDOM_RESULT
)

stage22_chron = load_json(
    STAGE22_CHRON_RESULT
)

stage24_2a = load_json(
    STAGE24_2A
)

stage24_2b = load_json(
    STAGE24_2B
)

stage24_2c = load_json(
    STAGE24_2C
)

stage24_2d = load_json(
    STAGE24_2D
)

stage24_5a = load_json(
    STAGE24_5A
)

stage24_5b = load_json(
    STAGE24_5B
)


for path in [
    STAGE24_2A,
    STAGE24_2B,
    STAGE24_2C,
    STAGE24_2D,
    STAGE24_5A,
    STAGE24_5B,
    SECONDARY_B62_SOURCE_RESULT,
    SECONDARY_B70_SOURCE_RESULT,
]:

    verify_sidecar(
        path
    )


# ==============================================================================
# 9. OPERATING-POINT EXTRACTION
# ==============================================================================

stage22_random_ops = extract_stage22_ops(
    stage22_random
)

stage22_chron_ops = extract_stage22_ops(
    stage22_chron
)

stage22_random_population = population_from_ops(
    stage22_random_ops,
    "STAGE22_RANDOM",
)

stage22_chron_population = population_from_ops(
    stage22_chron_ops,
    "STAGE22_CHRONOLOGICAL",
)


stage24_specs = [
    {
        "cell_id":
            "STAGE24_2018_TO_2017_BRIDGE62_PUBLISHED",

        "stage":
            "Stage24-2A",

        "family":
            "STAGE24_2018_TO_2017",

        "direction":
            "IDS2018_TO_CICIDS2017",

        "bridge":
            "bridge62",

        "variant":
            "PUBLISHED",

        "path":
            STAGE24_2A,

        "result":
            stage24_2a,

        "threshold_grid":
            PRIMARY_B62_THRESHOLD_GRID,

        "threshold_source":
            "IDS2018_02-28-2018_SOURCE_VALIDATION",

        "duplicate_of":
            None,
    },

    {
        "cell_id":
            "STAGE24_2018_TO_2017_BRIDGE62_FLAG_CORRECTED",

        "stage":
            "Stage24-2B",

        "family":
            "STAGE24_2018_TO_2017",

        "direction":
            "IDS2018_TO_CICIDS2017",

        "bridge":
            "bridge62",

        "variant":
            "FLAG_CORRECTED",

        "path":
            STAGE24_2B,

        "result":
            stage24_2b,

        "threshold_grid":
            PRIMARY_B62_THRESHOLD_GRID,

        "threshold_source":
            "IDS2018_02-28-2018_SOURCE_VALIDATION",

        "duplicate_of":
            "STAGE24_2018_TO_2017_BRIDGE62_PUBLISHED",
    },

    {
        "cell_id":
            "STAGE24_2018_TO_2017_BRIDGE70_PUBLISHED",

        "stage":
            "Stage24-2C",

        "family":
            "STAGE24_2018_TO_2017",

        "direction":
            "IDS2018_TO_CICIDS2017",

        "bridge":
            "bridge70",

        "variant":
            "PUBLISHED",

        "path":
            STAGE24_2C,

        "result":
            stage24_2c,

        "threshold_grid":
            STAGE22_CHRON_THRESHOLD_GRID,

        "threshold_source":
            "IDS2018_02-28-2018_SOURCE_VALIDATION",

        "duplicate_of":
            None,
    },

    {
        "cell_id":
            "STAGE24_2018_TO_2017_BRIDGE70_FLAG_CORRECTED",

        "stage":
            "Stage24-2D",

        "family":
            "STAGE24_2018_TO_2017",

        "direction":
            "IDS2018_TO_CICIDS2017",

        "bridge":
            "bridge70",

        "variant":
            "FLAG_CORRECTED",

        "path":
            STAGE24_2D,

        "result":
            stage24_2d,

        "threshold_grid":
            STAGE22_CHRON_THRESHOLD_GRID,

        "threshold_source":
            "IDS2018_02-28-2018_SOURCE_VALIDATION",

        "duplicate_of":
            None,
    },

    {
        "cell_id":
            "STAGE24_2017_TO_2018_BRIDGE62",

        "stage":
            "Stage24-5A",

        "family":
            "STAGE24_2017_TO_2018",

        "direction":
            "CICIDS2017_TO_IDS2018",

        "bridge":
            "bridge62",

        "variant":
            "FLAG_CORRECTED_SOURCE_SEMANTICS",

        "path":
            STAGE24_5A,

        "result":
            stage24_5a,

        "threshold_grid":
            SECONDARY_B62_THRESHOLD_GRID,

        "threshold_source":
            "CICIDS2017_THURSDAY_SOURCE_VALIDATION",

        "duplicate_of":
            None,
    },

    {
        "cell_id":
            "STAGE24_2017_TO_2018_BRIDGE70",

        "stage":
            "Stage24-5B",

        "family":
            "STAGE24_2017_TO_2018",

        "direction":
            "CICIDS2017_TO_IDS2018",

        "bridge":
            "bridge70",

        "variant":
            "FLAG_CORRECTED_SOURCE_SEMANTICS",

        "path":
            STAGE24_5B,

        "result":
            stage24_5b,

        "threshold_grid":
            SECONDARY_B70_THRESHOLD_GRID,

        "threshold_source":
            "CICIDS2017_THURSDAY_SOURCE_VALIDATION",

        "duplicate_of":
            None,
    },
]


for spec in stage24_specs:

    spec[
        "ops"
    ] = extract_stage24_ops(
        spec[
            "result"
        ]
    )

    spec[
        "population"
    ] = population_from_ops(
        spec[
            "ops"
        ],
        spec[
            "cell_id"
        ],
    )

    spec[
        "result_sha"
    ] = verify_sidecar(
        spec[
            "path"
        ]
    )

    spec[
        "threshold_grid_sha"
    ] = sha256_file(
        spec[
            "threshold_grid"
        ]
    )


# ==============================================================================
# 10. VERIFY BRIDGE62 SEMANTIC IDENTITY
# ==============================================================================

b62_pub = next(
    x
    for x in stage24_specs
    if x[
        "cell_id"
    ]
    ==
    "STAGE24_2018_TO_2017_BRIDGE62_PUBLISHED"
)

b62_cor = next(
    x
    for x in stage24_specs
    if x[
        "cell_id"
    ]
    ==
    "STAGE24_2018_TO_2017_BRIDGE62_FLAG_CORRECTED"
)


if (
    b62_pub[
        "ops"
    ]
    !=
    b62_cor[
        "ops"
    ]
):

    raise RuntimeError(
        "Stage24 bridge62 PUBLISHED/CORRECTED identity changed."
    )


print("=" * 120)
print("OPERATING-POINT INVENTORY")
print("=" * 120)

print(
    "[PASS] Stage24 bridge62 PUBLISHED == FLAG_CORRECTED."
)

print()


# ==============================================================================
# 11. CORRECTED MODEL PROVENANCE
#
# IMPORTANT RECOVERY:
#
#   bridge70 always uses canonical Stage22R chronological models.
#
#   We NEVER depend on Stage24-2C/2D having model_file fields.
# ==============================================================================

def expected_stage24_models(
    spec,
):

    direction = spec[
        "direction"
    ]

    bridge = spec[
        "bridge"
    ]

    result = spec[
        "result"
    ]


    # --------------------------------------------------------------------------
    # IDS2018 -> CICIDS2017 bridge62
    # --------------------------------------------------------------------------

    if (
        direction
        ==
        "IDS2018_TO_CICIDS2017"
        and
        bridge
        ==
        "bridge62"
    ):

        if (
            spec[
                "variant"
            ]
            ==
            "PUBLISHED"
        ):

            expected_lgbm = (
                result[
                    "models"
                ][
                    "lightgbm"
                ][
                    "model_sha256"
                ]
            )

            expected_xgb = (
                result[
                    "models"
                ][
                    "xgboost"
                ][
                    "model_sha256"
                ]
            )

        else:

            expected_lgbm = (
                result[
                    "models"
                ][
                    "lightgbm_sha256"
                ]
            )

            expected_xgb = (
                result[
                    "models"
                ][
                    "xgboost_sha256"
                ]
            )


        return {
            "lightgbm": {
                "path":
                    PRIMARY_B62_LGBM,

                "expected_sha256":
                    expected_lgbm,
            },

            "xgboost": {
                "path":
                    PRIMARY_B62_XGB,

                "expected_sha256":
                    expected_xgb,
            },
        }


    # --------------------------------------------------------------------------
    # IDS2018 -> CICIDS2017 bridge70
    #
    # RECOVERY FIX:
    # Stage24-2D records hashes, but may omit model_file.
    # Canonical path is inherited Stage22R CHRONOLOGICAL_NATURAL.
    # --------------------------------------------------------------------------

    if (
        direction
        ==
        "IDS2018_TO_CICIDS2017"
        and
        bridge
        ==
        "bridge70"
    ):

        expected_lgbm = (
            result[
                "models"
            ][
                "lightgbm"
            ][
                "model_sha256"
            ]
        )

        expected_xgb = (
            result[
                "models"
            ][
                "xgboost"
            ][
                "model_sha256"
            ]
        )


        return {
            "lightgbm": {
                "path":
                    STAGE22_CHRON_LGBM,

                "expected_sha256":
                    expected_lgbm,

                "path_provenance":
                    "CANONICAL_STAGE22R_CHRONOLOGICAL_NATURAL_MODEL",
            },

            "xgboost": {
                "path":
                    STAGE22_CHRON_XGB,

                "expected_sha256":
                    expected_xgb,

                "path_provenance":
                    "CANONICAL_STAGE22R_CHRONOLOGICAL_NATURAL_MODEL",
            },
        }


    # --------------------------------------------------------------------------
    # CICIDS2017 -> IDS2018 bridge62
    # --------------------------------------------------------------------------

    if (
        direction
        ==
        "CICIDS2017_TO_IDS2018"
        and
        bridge
        ==
        "bridge62"
    ):

        return {
            "xgboost": {
                "path":
                    SECONDARY_B62_MODEL,

                "expected_sha256":
                    result[
                        "model"
                    ][
                        "model_sha256"
                    ],
            }
        }


    # --------------------------------------------------------------------------
    # CICIDS2017 -> IDS2018 bridge70
    # --------------------------------------------------------------------------

    if (
        direction
        ==
        "CICIDS2017_TO_IDS2018"
        and
        bridge
        ==
        "bridge70"
    ):

        return {
            "xgboost": {
                "path":
                    SECONDARY_B70_MODEL,

                "expected_sha256":
                    result[
                        "model"
                    ][
                        "model_sha256"
                    ],
            }
        }


    raise RuntimeError(
        "Unknown Stage24 model configuration."
    )


for spec in stage24_specs:

    verified = {}


    for model_name, model_spec in expected_stage24_models(
        spec
    ).items():

        path = model_spec[
            "path"
        ]

        actual_sha = sha256_file(
            path
        )

        expected_sha = model_spec[
            "expected_sha256"
        ]


        if actual_sha != expected_sha:

            raise RuntimeError(
                "\nStage24 model SHA mismatch.\n"
                f"Cell:     {spec['cell_id']}\n"
                f"Model:    {model_name}\n"
                f"Path:     {path}\n"
                f"Expected: {expected_sha}\n"
                f"Actual:   {actual_sha}"
            )


        entry = {
            "path":
                str(
                    path.relative_to(
                        REPO
                    )
                ),

            "sha256":
                actual_sha,
        }


        if (
            "path_provenance"
            in
            model_spec
        ):

            entry[
                "path_provenance"
            ] = model_spec[
                "path_provenance"
            ]


        verified[
            model_name
        ] = entry


    spec[
        "verified_models"
    ] = verified


print(
    "[PASS] Stage24 model provenance recovered."
)

print(
    "[PASS] Stage24-2D bridge70 canonical Stage22R paths verified by SHA."
)

print(
    "[PASS] No ML library imported; models inspected as bytes only."
)

print()


# ==============================================================================
# 12. VERIFY STAGE22 MODEL FILES
# ==============================================================================

def verify_stage22_model(
    result,
    path,
):

    expected = (
        result[
            "artifacts"
        ][
            "hashes_before_result_json"
        ][
            path.name
        ]
    )

    return verify_sha(
        path,
        expected,
        path.name,
    )


stage22_random_lgbm_sha = verify_stage22_model(
    stage22_random,
    STAGE22_RANDOM_LGBM,
)

stage22_random_xgb_sha = verify_stage22_model(
    stage22_random,
    STAGE22_RANDOM_XGB,
)

stage22_chron_lgbm_sha = verify_stage22_model(
    stage22_chron,
    STAGE22_CHRON_LGBM,
)

stage22_chron_xgb_sha = verify_stage22_model(
    stage22_chron,
    STAGE22_CHRON_XGB,
)


# Threshold grids.
stage22_random_threshold_sha = verify_stage22_model(
    stage22_random,
    STAGE22_RANDOM_THRESHOLD_GRID,
)

stage22_chron_threshold_sha = verify_stage22_model(
    stage22_chron,
    STAGE22_CHRON_THRESHOLD_GRID,
)


# ==============================================================================
# 13. EXACT OBSERVED PREVALENCES
# ==============================================================================

random_prevalence = (
    stage22_random_population[
        "observed_prevalence"
    ]
)

chron_prevalence = (
    stage22_chron_population[
        "observed_prevalence"
    ]
)


assert_close(
    random_prevalence,
    0.13684738945373795,
    tolerance=1e-17,
    label="Stage22 random prevalence",
)

assert_close(
    chron_prevalence,
    0.10484691299808009,
    tolerance=1e-17,
    label="Stage22 chronological prevalence",
)


primary_prevalences = {
    spec[
        "population"
    ][
        "observed_prevalence"
    ]
    for spec in stage24_specs
    if (
        spec[
            "family"
        ]
        ==
        "STAGE24_2018_TO_2017"
    )
}


if len(
    primary_prevalences
) != 1:

    raise RuntimeError(
        "Stage24 primary target prevalence mismatch."
    )


stage24_primary_prevalence = next(
    iter(
        primary_prevalences
    )
)


assert_close(
    stage24_primary_prevalence,
    0.19699633629757277,
    tolerance=1e-17,
    label="Stage24 primary prevalence",
)


secondary_prevalences = {
    spec[
        "population"
    ][
        "observed_prevalence"
    ]
    for spec in stage24_specs
    if (
        spec[
            "family"
        ]
        ==
        "STAGE24_2017_TO_2018"
    )
}


if secondary_prevalences != {
    chron_prevalence
}:

    raise RuntimeError(
        "Stage24 secondary prevalence mismatch."
    )


print("=" * 120)
print("EXACT OBSERVED PREVALENCES")
print("=" * 120)

print(
    "Stage22 random:             ",
    f"{random_prevalence:.17f}",
)

print(
    "Stage22 chronological:      ",
    f"{chron_prevalence:.17f}",
)

print(
    "Stage24 2018 -> 2017:       ",
    f"{stage24_primary_prevalence:.17f}",
)

print(
    "Stage24 2017 -> 2018:       ",
    f"{chron_prevalence:.17f}",
)

print()


# ==============================================================================
# 14. BUILD STAGE22 INVENTORY
# ==============================================================================

stage22_random_result_sha = sha256_file(
    STAGE22_RANDOM_RESULT
)

stage22_chron_result_sha = sha256_file(
    STAGE22_CHRON_RESULT
)


inherited_cells = [
    {
        "cell_id":
            "STAGE22_RANDOM",

        "source_stage":
            "Stage22R-2A",

        "family":
            "STAGE22_RANDOM",

        "direction":
            "IDS2018_RANDOM_VALIDATION",

        "bridge":
            "FULL_70_FEATURE",

        "variant":
            "RANDOM_NATURAL",

        "result_artifact": {
            "path":
                str(
                    STAGE22_RANDOM_RESULT.relative_to(
                        REPO
                    )
                ),

            "sha256":
                stage22_random_result_sha,
        },

        "models": {
            "lightgbm": {
                "path":
                    str(
                        STAGE22_RANDOM_LGBM.relative_to(
                            REPO
                        )
                    ),

                "sha256":
                    stage22_random_lgbm_sha,
            },

            "xgboost": {
                "path":
                    str(
                        STAGE22_RANDOM_XGB.relative_to(
                            REPO
                        )
                    ),

                "sha256":
                    stage22_random_xgb_sha,
            },
        },

        "split_identity": {
            "type":
                "FROZEN_RANDOM_VALIDATION_MEMBERSHIP_BITSET",

            "membership_path":
                str(
                    STAGE22_RANDOM_MEMBERSHIP.relative_to(
                        REPO
                    )
                ),

            "membership_sha256":
                random_membership_sha,

            "membership_summary_sha256":
                membership_summary_sha,

            "derivation":
                membership_summary[
                    "membership_derivation"
                ][
                    "RANDOM_NATURAL_validation"
                ],
        },

        "threshold_source": {
            "selection_population":
                "STAGE22_RANDOM_VALIDATION",

            "threshold_grid_path":
                str(
                    STAGE22_RANDOM_THRESHOLD_GRID.relative_to(
                        REPO
                    )
                ),

            "threshold_grid_sha256":
                stage22_random_threshold_sha,

            "deployment_retuning":
                False,
        },

        "evaluation_population":
            stage22_random_population,

        "operating_points":
            stage22_random_ops,

        "identity_duplicate_of":
            None,
    },

    {
        "cell_id":
            "STAGE22_CHRONOLOGICAL",

        "source_stage":
            "Stage22R-2C",

        "family":
            "STAGE22_CHRONOLOGICAL",

        "direction":
            "IDS2018_FORWARD_TEMPORAL_VALIDATION",

        "bridge":
            "FULL_70_FEATURE",

        "variant":
            "CHRONOLOGICAL_NATURAL",

        "result_artifact": {
            "path":
                str(
                    STAGE22_CHRON_RESULT.relative_to(
                        REPO
                    )
                ),

            "sha256":
                stage22_chron_result_sha,
        },

        "models": {
            "lightgbm": {
                "path":
                    str(
                        STAGE22_CHRON_LGBM.relative_to(
                            REPO
                        )
                    ),

                "sha256":
                    stage22_chron_lgbm_sha,
            },

            "xgboost": {
                "path":
                    str(
                        STAGE22_CHRON_XGB.relative_to(
                            REPO
                        )
                    ),

                "sha256":
                    stage22_chron_xgb_sha,
            },
        },

        "split_identity": {
            "type":
                "DETERMINISTIC_DAY_BASED_MEMBERSHIP",

            "membership_summary_sha256":
                membership_summary_sha,

            "day_offsets_sha256":
                day_offsets_sha,

            "validation_rule":
                membership_summary[
                    "membership_derivation"
                ][
                    "CHRONOLOGICAL_NATURAL_validation"
                ],

            "note":
                (
                    "Chronological validation is frozen as day_id=7; "
                    "no separate bitset is required."
                ),
        },

        "threshold_source": {
            "selection_population":
                "STAGE22_CHRONOLOGICAL_VALIDATION_02_28_2018",

            "threshold_grid_path":
                str(
                    STAGE22_CHRON_THRESHOLD_GRID.relative_to(
                        REPO
                    )
                ),

            "threshold_grid_sha256":
                stage22_chron_threshold_sha,

            "deployment_retuning":
                False,
        },

        "evaluation_population":
            stage22_chron_population,

        "operating_points":
            stage22_chron_ops,

        "identity_duplicate_of":
            None,
    },
]


# ==============================================================================
# 15. ADD STAGE24 INVENTORY
# ==============================================================================

for spec in stage24_specs:

    target_identity = select_target_identity(
        spec[
            "result"
        ]
    )


    if (
        spec[
            "duplicate_of"
        ]
        ==
        "STAGE24_2018_TO_2017_BRIDGE62_PUBLISHED"
    ):

        source_identity = select_target_identity(
            stage24_2a
        )

        if source_identity:

            target_identity = source_identity


    if (
        spec[
            "direction"
        ]
        ==
        "IDS2018_TO_CICIDS2017"
    ):

        split_identity = {
            "source_split":
                "STAGE22R_CHRONOLOGICAL_NATURAL",

            "source_train":
                "day_id 0..6",

            "source_validation":
                "day_id 7 = 02-28-2018",

            "source_membership_summary_sha256":
                membership_summary_sha,

            "source_day_offsets_sha256":
                day_offsets_sha,

            "target_population":
                "FULL_EFFECTIVE_CICIDS2017",

            "target_rows":
                spec[
                    "population"
                ][
                    "rows"
                ],

            "target_attack":
                spec[
                    "population"
                ][
                    "attack"
                ],

            "target_benign":
                spec[
                    "population"
                ][
                    "benign"
                ],

            "target_identity":
                target_identity,

            "stage24_protocol_sha256":
                stage24_protocol_sha,

            "cicids2017_contract_sha256":
                stage24_contract_sha,
        }


    else:

        split_identity = {
            "source_split":
                "CICIDS2017_MON_WED_TRAIN_THURSDAY_VALIDATE",

            "target_population":
                "IDS2018_FEB28_FROZEN_K79",

            "target_identity":
                target_identity,

            "stage24_protocol_sha256":
                stage24_protocol_sha,

            "cicids2017_contract_sha256":
                stage24_contract_sha,
        }


    inherited_cells.append(
        {
            "cell_id":
                spec[
                    "cell_id"
                ],

            "source_stage":
                spec[
                    "stage"
                ],

            "family":
                spec[
                    "family"
                ],

            "direction":
                spec[
                    "direction"
                ],

            "bridge":
                spec[
                    "bridge"
                ],

            "variant":
                spec[
                    "variant"
                ],

            "result_artifact": {
                "path":
                    str(
                        spec[
                            "path"
                        ].relative_to(
                            REPO
                        )
                    ),

                "sha256":
                    spec[
                        "result_sha"
                    ],
            },

            "models":
                spec[
                    "verified_models"
                ],

            "split_identity":
                split_identity,

            "threshold_source": {
                "selection_population":
                    spec[
                        "threshold_source"
                    ],

                "threshold_grid_path":
                    str(
                        spec[
                            "threshold_grid"
                        ].relative_to(
                            REPO
                        )
                    ),

                "threshold_grid_sha256":
                    spec[
                        "threshold_grid_sha"
                    ],

                "deployment_retuning":
                    False,
            },

            "evaluation_population":
                spec[
                    "population"
                ],

            "operating_points":
                spec[
                    "ops"
                ],

            "identity_duplicate_of":
                spec[
                    "duplicate_of"
                ],
        }
    )


expected_cells = {
    "STAGE22_RANDOM",
    "STAGE22_CHRONOLOGICAL",

    "STAGE24_2018_TO_2017_BRIDGE62_PUBLISHED",
    "STAGE24_2018_TO_2017_BRIDGE62_FLAG_CORRECTED",
    "STAGE24_2018_TO_2017_BRIDGE70_PUBLISHED",
    "STAGE24_2018_TO_2017_BRIDGE70_FLAG_CORRECTED",

    "STAGE24_2017_TO_2018_BRIDGE62",
    "STAGE24_2017_TO_2018_BRIDGE70",
}


actual_cells = {
    cell[
        "cell_id"
    ]
    for cell in inherited_cells
}


if actual_cells != expected_cells:

    raise RuntimeError(
        "Inherited Stage25 cell inventory mismatch."
    )


for cell in inherited_cells:

    if (
        set(
            cell[
                "operating_points"
            ].keys()
        )
        !=
        {
            "STANDARD",
            "BALANCED",
            "SECURITY",
        }
    ):

        raise RuntimeError(
            f"{cell['cell_id']}: threshold inventory mismatch."
        )


operating_point_count = sum(
    len(
        cell[
            "operating_points"
        ]
    )
    for cell in inherited_cells
)


if operating_point_count != 24:

    raise RuntimeError(
        f"Expected 24 operating points; found {operating_point_count}."
    )


print("=" * 120)
print("INHERITED STAGE25 INVENTORY")
print("=" * 120)

print(
    "Frozen cells:            ",
    len(
        inherited_cells
    ),
)

print(
    "Frozen operating points: ",
    operating_point_count,
)

print(
    "Future projection rows:  ",
    operating_point_count
    *
    len(
        PREVALENCE_GRID
    ),
)

print()

print(
    "[PASS] Complete 8-cell / 24-operating-point inventory recovered."
)

print()


# ==============================================================================
# 16. DECLARED HASH RECEIPTS
#
# IMPORTANT:
# We do not open probability arrays.
# Only hash strings embedded in frozen result JSON are inventoried.
# ==============================================================================

declared_hashes = {}


for cell in inherited_cells:

    result = load_json(
        REPO
        /
        cell[
            "result_artifact"
        ][
            "path"
        ]
    )

    declared_hashes[
        cell[
            "cell_id"
        ]
    ] = recursive_sha_fields(
        result
    )


# ==============================================================================
# 17. BYTE-VERIFIED ARTIFACT MANIFEST
# ==============================================================================

byte_verified_paths = [
    STAGE22_CLOSEOUT,
    STAGE22_MEMBERSHIP_SUMMARY,
    STAGE22_RANDOM_MEMBERSHIP,
    STAGE22_DAY_OFFSETS,

    STAGE22_RANDOM_RESULT,
    STAGE22_CHRON_RESULT,

    STAGE22_RANDOM_THRESHOLD_GRID,
    STAGE22_CHRON_THRESHOLD_GRID,

    STAGE22_RANDOM_LGBM,
    STAGE22_RANDOM_XGB,
    STAGE22_CHRON_LGBM,
    STAGE22_CHRON_XGB,

    STAGE24_FINAL,
    STAGE24_PUBLICATION_MANIFEST,
    STAGE24_PROTOCOL,
    STAGE24_CICIDS2017_CONTRACT,

    STAGE24_2A,
    STAGE24_2B,
    STAGE24_2C,
    STAGE24_2D,
    STAGE24_5A,
    STAGE24_5B,

    PRIMARY_B62_LGBM,
    PRIMARY_B62_XGB,
    PRIMARY_B62_THRESHOLD_GRID,

    SECONDARY_B62_MODEL,
    SECONDARY_B62_THRESHOLD_GRID,
    SECONDARY_B62_SOURCE_RESULT,

    SECONDARY_B70_MODEL,
    SECONDARY_B70_THRESHOLD_GRID,
    SECONDARY_B70_SOURCE_RESULT,
]


byte_verified = {}


for path in byte_verified_paths:

    byte_verified[
        str(
            path.relative_to(
                REPO
            )
        )
    ] = sha256_file(
        path
    )


# ==============================================================================
# 18. HANDOFF RECONCILIATION
# ==============================================================================

handoff_reconciliation = {
    "rule":
        "DURABLE_REPOSITORY_EVIDENCE_OVERRIDES_ROUNDED_HANDOFF_TEXT",

    "substantive_discrepancies_found":
        0,

    "recoveries": [
        {
            "topic":
                "Stage22 random observed prevalence",

            "handoff":
                "approximately 13.68%",

            "repository_exact":
                random_prevalence,

            "resolution":
                "ROUNDED_HANDOFF_REPLACED_BY_EXACT_REPOSITORY_VALUE",
        },

        {
            "topic":
                "Stage22 chronological observed prevalence",

            "handoff":
                "approximately 10.48%",

            "repository_exact":
                chron_prevalence,

            "resolution":
                "ROUNDED_HANDOFF_REPLACED_BY_EXACT_REPOSITORY_VALUE",
        },

        {
            "topic":
                "Stage24 primary target prevalence",

            "repository_exact":
                stage24_primary_prevalence,

            "resolution":
                "RECOVERED_FROM_FROZEN_TARGET_COUNTS",
        },

        {
            "topic":
                "Stage24 bridge70 model-file provenance",

            "repository_observation":
                (
                    "Stage24-2D records inherited bridge70 model SHA256 "
                    "values without repeating model_file."
                ),

            "resolution":
                (
                    "Canonical Stage22R CHRONOLOGICAL_NATURAL model paths "
                    "are frozen in Stage25 and verified byte-for-byte against "
                    "the Stage24-declared SHA256 values."
                ),

            "scientific_change":
                False,
        },

        {
            "topic":
                "Stage24 GROUNDED_S4",

            "repository":
                "2 cells administratively cancelled before target opening",

            "resolution":
                "EXCLUDED; NO SUBSTITUTE AND NO REALLOCATION",
        },
    ],
}


# ==============================================================================
# 19. OBSERVED PREVALENCE RECEIPTS
# ==============================================================================

observed_receipts = []


for cell in inherited_cells:

    p = cell[
        "evaluation_population"
    ]

    observed_receipts.append(
        {
            "cell_id":
                cell[
                    "cell_id"
                ],

            "family":
                cell[
                    "family"
                ],

            "direction":
                cell[
                    "direction"
                ],

            "bridge":
                cell[
                    "bridge"
                ],

            "variant":
                cell[
                    "variant"
                ],

            "rows":
                p[
                    "rows"
                ],

            "benign":
                p[
                    "benign"
                ],

            "attack":
                p[
                    "attack"
                ],

            "observed_prevalence":
                p[
                    "observed_prevalence"
                ],

            "derivation":
                "FROZEN_CONFUSION_COUNTS",
        }
    )


# ==============================================================================
# 20. CREATE LOCK DIRECTORY
#
# Everything before this line was verification only.
# ==============================================================================

LOCK_DIR.mkdir(
    parents=True,
    exist_ok=False,
)


# ==============================================================================
# 21. PREVALENCE GRID
# ==============================================================================

prevalence_payload = {
    "stage":
        "Stage25-0",

    "status":
        "FROZEN_BEFORE_PROJECTION",

    "prevalence_grid": {
        "decimal":
            PREVALENCE_GRID,

        "labels": [
            "10%",
            "3%",
            "1%",
            "0.3%",
            "0.1%",
            "0.01%",
        ],

        "dropping_lowest_point":
            "FORBIDDEN",
    },

    "ppv_target_grid": {
        "decimal":
            PPV_TARGETS,

        "labels": [
            "10%",
            "25%",
            "50%",
            "75%",
            "90%",
        ],
    },

    "observed_markers": {
        "STAGE22_RANDOM":
            random_prevalence,

        "STAGE22_CHRONOLOGICAL":
            chron_prevalence,

        "STAGE24_2018_TO_2017":
            stage24_primary_prevalence,

        "STAGE24_2017_TO_2018":
            chron_prevalence,
    },

    "note":
        (
            "10% is a deployment-stress grid point, not a generic "
            "benchmark prevalence."
        ),
}


# ==============================================================================
# 22. PRIOR-SHIFT ASSUMPTION
# ==============================================================================

prior_shift_payload = {
    "stage":
        "Stage25-0",

    "assumption":
        "PRIOR_PROBABILITY_SHIFT_ONLY",

    "held_fixed_within_cell": [
        "TPR",
        "FPR",
        "model",
        "threshold",
    ],

    "varied":
        "attack_prevalence_pi",

    "within_cell_interpretation":
        (
            "Only the prior attack probability changes analytically."
        ),

    "between_cell_interpretation":
        (
            "Different frozen cells retain different TPR/FPR values caused "
            "by their original validation/domain conditions."
        ),

    "critical_limitation":
        (
            "Stage25 is analytic deployment-stress projection and not "
            "empirical production validation. Domain or temporal shift can "
            "change P(X|Y), TPR and FPR."
        ),

    "base_rate_and_domain_shift_must_not_be_conflated":
        True,
}


# ==============================================================================
# 23. TRAFFIC SPECIFICATION
# ==============================================================================

traffic_payload = {
    "stage":
        "Stage25-0",

    "benign_flows_per_day":
        BENIGN_FLOWS_PER_DAY,

    "volume_semantics":
        "FIXED_BENIGN_VOLUME_NOT_FIXED_TOTAL_VOLUME",

    "equations": {
        "N_total":
            "B / (1 - pi)",

        "A":
            "pi * B / (1 - pi)",

        "TP":
            "TPR * A",

        "FN":
            "(1 - TPR) * A",

        "FP":
            "FPR * B",

        "TN":
            "(1 - FPR) * B",

        "alerts":
            "TP + FP",

        "false_alert_fraction":
            "FP / (TP + FP)",
    },

    "important_implication":
        (
            "At fixed benign volume and fixed FPR, FP/day does not fall "
            "merely because attack prevalence falls."
        ),

    "enterprise_representativeness_claim":
        False,
}


# ==============================================================================
# 24. BAYESIAN EQUATIONS — STRINGS ONLY
# ==============================================================================

bayesian_payload = {
    "stage":
        "Stage25-0",

    "equations": {
        "PPV":
            (
                "TPR*pi / "
                "(TPR*pi + FPR*(1-pi))"
            ),

        "NPV":
            (
                "(1-FPR)*(1-pi) / "
                "((1-FPR)*(1-pi) + (1-TPR)*pi)"
            ),

        "LR_plus":
            "TPR / FPR",

        "LR_minus":
            "(1-TPR) / (1-FPR)",

        "prior_odds":
            "pi / (1-pi)",

        "posterior_odds_positive":
            "prior_odds * LR_plus",

        "ppv_break_even_q":
            (
                "q*FPR / "
                "(TPR*(1-q) + q*FPR)"
            ),

        "ppv50":
            "FPR / (TPR + FPR)",

        "required_fpr_for_ppv_q":
            (
                "TPR*pi*(1-q) / "
                "(q*(1-pi))"
            ),
    },

    "graphical_approximation_of_break_even":
        "FORBIDDEN",
}


# ==============================================================================
# 25. ANALYST CAPACITY SPEC
# ==============================================================================

alerts_per_analyst_day = (
    ANALYST_SHIFT_MINUTES
    //
    ALERT_SERVICE_MINUTES
)


if alerts_per_analyst_day != 240:

    raise RuntimeError(
        "Analyst capacity arithmetic changed."
    )


capacity_tiers = {}


for k in ANALYST_TIERS:

    capacity_tiers[
        str(
            k
        )
    ] = {
        "analyst_days":
            k,

        "analyst_hours":
            8
            *
            k,

        "alert_capacity_per_day":
            alerts_per_analyst_day
            *
            k,

        "false_positive_only_fpr_capacity":
            (
                alerts_per_analyst_day
                *
                k
                /
                BENIGN_FLOWS_PER_DAY
            ),
    }


capacity_payload = {
    "stage":
        "Stage25-0",

    "minutes_per_alert":
        ALERT_SERVICE_MINUTES,

    "service_time_semantics":
        "ASSUMED_REFERENCE_SCENARIO_NOT_UNIVERSAL_SOC_CONSTANT",

    "analyst_shift_minutes":
        ANALYST_SHIFT_MINUTES,

    "alerts_per_analyst_day":
        alerts_per_analyst_day,

    "tiers":
        capacity_tiers,

    "equations": {
        "false_alert_hours":
            "FP * 2 / 60",

        "alert_hours":
            "(TP + FP) * 2 / 60",

        "ACI_k":
            "(TP + FP) / (240*k)",

        "FP_only_FPR_capacity":
            "(480*k/s) / B",

        "total_alert_condition":
            (
                "TPR*pi*B/(1-pi) + FPR*B <= 240*k"
            ),

        "total_alert_FPR_ceiling":
            (
                "240*k/B - TPR*pi/(1-pi)"
            ),
    },

    "formal_term":
        "SOC Capacity Exceedance",

    "capacity_fit_does_not_imply_operational_usefulness":
        True,
}


# ==============================================================================
# 26. RELATIVE COST SPEC
# ==============================================================================

cost_payload = {
    "stage":
        "Stage25-0",

    "units":
        "RELATIVE_OPERATIONAL_COST_UNITS",

    "currency":
        False,

    "C_FP":
        C_FP,

    "C_FN":
        C_FN,

    "ratio":
        "1:100",

    "equations": {
        "model":
            "FP*C_FP + FN*C_FN",

        "ignore":
            "A*C_FN",

        "cost_break_even_prevalence":
            (
                "(C_FP*FPR) / "
                "(C_FN*TPR + C_FP*FPR)"
            ),
    },

    "limitations": [
        "Not financial loss.",
        "Not dollars.",
        "Each malicious flow is not an independent breach.",
        "The ignore/non-deployment comparator is simplified.",
    ],
}


# ==============================================================================
# 27. THRESHOLD POLICY
# ==============================================================================

threshold_policy = {
    "stage":
        "Stage25-0",

    "stage22_cells": [
        "STAGE22_RANDOM",
        "STAGE22_CHRONOLOGICAL",
    ],

    "stage24_cells": sorted(
        c
        for c in expected_cells
        if c.startswith(
            "STAGE24_"
        )
    ),

    "allowed_operating_points": [
        "STANDARD",
        "BALANCED",
        "SECURITY",
    ],

    "threshold_source":
        "EXACT_FROZEN_SOURCE_VALIDATION_ONLY",

    "forbidden": [
        "target-specific threshold optimization",
        "prevalence-specific threshold optimization",
        "PPV-specific threshold selection",
        "new F1 maximization",
        "new F2 maximization",
        "new calibration",
        "new probability inference",
    ],

    "grounded_s4":
        "NOT_ELIGIBLE_STAGE24_CANCELLED",
}


# ==============================================================================
# 28. NUMERICAL POLICY
# ==============================================================================

numerical_policy = {
    "stage":
        "Stage25-0",

    "calculation_dtype":
        "IEEE754_FLOAT64",

    "epsilon_injection":
        "FORBIDDEN",

    "LR_plus": {
        "normal":
            "TPR/FPR",

        "FPR_zero_TPR_positive":
            "POSITIVE_INFINITY",

        "FPR_zero_TPR_zero":
            "NULL_UNDEFINED_0_OVER_0",
    },

    "LR_minus": {
        "normal":
            "(1-TPR)/(1-FPR)",

        "denominator_zero_numerator_positive":
            "POSITIVE_INFINITY",

        "both_zero":
            "NULL_UNDEFINED_0_OVER_0",
    },

    "other_zero_denominators":
        "NULL_WITH_EXPLICIT_STATUS",

    "break_even_values":
        "ANALYTIC_NOT_GRID_APPROXIMATED",

    "internal_rounding":
        "NONE",

    "presentation_rounding":
        "ALLOWED_ONLY_AT_REPORTING_LAYER",
}


# ==============================================================================
# 29. UNCERTAINTY POLICY
# ==============================================================================

uncertainty_policy = {
    "stage":
        "Stage25-0",

    "conditional_projection_uncertainty":
        "NONE",

    "reason":
        (
            "Stage25 projections are deterministic conditional on inherited "
            "TPR/FPR and frozen assumptions."
        ),

    "empirical_estimation_uncertainty_exists":
        True,

    "inherited_TPR_FPR_uncertainty_propagated":
        False,

    "reason_not_propagated":
        (
            "A complete joint TPR/FPR sampling distribution is not durably "
            "available for every inherited operating point. Stage24 paired "
            "bootstrap artifacts concern PR-AUC/ROC-AUC/Brier comparisons "
            "and do not substitute for this."
        ),

    "new_bootstrap":
        "FORBIDDEN",

    "required_language":
        (
            "Values are exact conditional transformations of frozen empirical "
            "estimates and assumptions, not exact production-population truths."
        ),
}


# ==============================================================================
# 30. INTERPRETATION MATRIX
# ==============================================================================

interpretation_matrix = {
    "stage":
        "Stage25-0",

    "entries": [
        {
            "result":
                "PPV decreases as prevalence decreases within a frozen cell",

            "permitted":
                "Operating point is sensitive to prior prevalence.",
        },

        {
            "result":
                "PPV < 10% at 0.1% prevalence",

            "permitted":
                (
                    "Under the frozen prior-shift projection, fewer than "
                    "one in ten positive alerts corresponds to an attack."
                ),
        },

        {
            "result":
                "ACI_1 > 1",

            "permitted":
                "Projected alerts exceed one assumed analyst-day.",
        },

        {
            "result":
                "ACI_3 > 1",

            "permitted":
                "Projected alerts exceed three assumed analyst-days.",
        },

        {
            "result":
                "Frozen FPR > capacity FPR",

            "permitted":
                (
                    "False-alert rate alone exceeds the specified capacity scenario."
                ),
        },

        {
            "result":
                "Cost(Model) > Cost(Ignore)",

            "permitted":
                (
                    "Under the frozen 1:100 relative-cost model, the simplified "
                    "ignore reference has lower expected relative cost."
                ),
        },

        {
            "result":
                "Security threshold exceeds capacity",

            "permitted":
                (
                    "The tested security FPR constraint does not guarantee "
                    "capacity feasibility."
                ),
        },

        {
            "result":
                "Strong ranking but poor operational projection",

            "permitted":
                (
                    "Ranking quality alone does not establish deployment utility."
                ),
        },

        {
            "result":
                "Chronological projection worse than random",

            "permitted":
                (
                    "Frozen chronological operating characteristics produce "
                    "poorer projection; prevalence alone must not be assumed causal."
                ),
        },

        {
            "result":
                "Cross-dataset projection collapses",

            "permitted":
                (
                    "Transferred operating point is not operationally robust "
                    "under the tested projection."
                ),
        },

        {
            "result":
                "Operating point survives 0.1% stress",

            "permitted":
                (
                    "It remains comparatively informative under the assumptions; "
                    "empirical deployment validation is still required."
                ),
        },
    ],

    "average_directions":
        "FORBIDDEN",

    "average_bridges":
        "FORBIDDEN",

    "average_extractor_variants":
        "FORBIDDEN",
}


# ==============================================================================
# 31. PROHIBITED CLAIMS
# ==============================================================================

prohibited_claims = {
    "stage":
        "Stage25-0",

    "claims": [
        "The model is good for enterprise deployment.",
        "The model is operationally useless.",
        "Random splitting succeeds purely because prevalence is higher.",
        "High F1 means low FPR.",
        "We proved the IDS field is broken.",
        "These are real SOC alert counts.",
        "Relative cost units are dollars.",
        "Every false negative represents an independent breach.",
        "One million benign flows/day represents every enterprise.",
        "Stage25 constitutes empirical production validation.",
        "Stage24 transfer directions may be averaged.",
    ],

    "preferred_prefix":
        (
            "Under the frozen prior-shift, traffic-volume, "
            "analyst-service-time, and relative-cost assumptions..."
        ),
}


# ==============================================================================
# 32. FIGURE PLAN — FROZEN BEFORE RESULTS
# ==============================================================================

figure_plan = {
    "stage":
        "Stage25-0",

    "primary": [
        {
            "id":
                "25-A",

            "title":
                "PPV Cliff",

            "x":
                "prevalence log scale",

            "y":
                "PPV",

            "required": [
                "50% reference",
                "10% reference",
                "observed prevalence markers",
                "deployment-grid points",
            ],
        },

        {
            "id":
                "25-B",

            "title":
                "SOC Capacity Exceedance",

            "x":
                "prevalence log scale",

            "y":
                "alert-processing hours/day",

            "capacity_reference_hours": [
                8,
                24,
                80,
            ],

            "also_report":
                "FP-only workload",
        },

        {
            "id":
                "25-C",

            "title":
                "Benchmark-to-Deployment Translation",

            "projection_prevalence":
                0.001,

            "observed_metrics": [
                "F1",
                "precision",
                "recall",
                "FPR",
                "observed prevalence",
            ],

            "projected_metrics": [
                "PPV",
                "FP/day",
                "TP/day",
                "alerts/day",
                "analyst-hours/day",
            ],

            "F1_is_not_PPV":
                True,
        },

        {
            "id":
                "25-D",

            "title":
                "Required FPR for Target PPV",

            "x":
                "prevalence log scale",

            "y":
                "maximum permissible FPR",

            "target_ppv":
                PPV_TARGETS,

            "overlay_actual_fpr":
                True,
        },
    ],

    "supplementary": [
        {
            "id":
                "25-E",

            "title":
                "Bayesian Evidence Translation",

            "content":
                (
                    "Prior probability to posterior probability after "
                    "positive alert using representative inherited LR+."
                ),

            "status":
                "FROZEN_BEFORE_RESULTS",
        },
    ],

    "drop_figure_based_on_results":
        "FORBIDDEN",
}


# ==============================================================================
# 33. SANITY TEST PLAN
# ==============================================================================

sanity_tests = {
    "stage":
        "Stage25-0",

    "tests": [
        {
            "name":
                "PPV_AT_OBSERVED_PREVALENCE",

            "requirement":
                (
                    "Projected PPV at exact original prevalence reproduces "
                    "frozen precision."
                ),
        },

        {
            "name":
                "PPV_MONOTONICITY",

            "requirement":
                (
                    "For fixed TPR>0 and FPR>0, PPV increases with prevalence."
                ),
        },

        {
            "name":
                "FP_INVARIANCE",

            "requirement":
                (
                    "FP=FPR*1,000,000 is invariant across prevalence for "
                    "a fixed operating point."
                ),
        },

        {
            "name":
                "COST_BREAK_EVEN_SIGN_REVERSAL",

            "requirement":
                (
                    "Model-vs-ignore inequality reverses immediately around "
                    "analytic pi_star_cost."
                ),
        },

        {
            "name":
                "PPV50_CHECK",

            "requirement":
                "PPV equals 0.5 at analytic pi_star_PPV50.",
        },

        {
            "name":
                "CONFUSION_IDENTITIES",

            "requirement":
                (
                    "TP+FN equals attack volume and FP+TN equals 1,000,000."
                ),
        },

        {
            "name":
                "COMPLETE_PROJECTION_MATRIX",

            "expected_rows":
                24
                *
                6,

            "requirement":
                "24 operating points x 6 prevalence levels.",
        },
    ],

    "drop_test_based_on_results":
        "FORBIDDEN",
}


# ==============================================================================
# 34. SUCCESS CONDITION
# ==============================================================================

success_condition = {
    "stage":
        "Stage25-0",

    "operational_collapse_required":
        False,

    "valid_outcomes": [
        "SEVERE_BASE_RATE_COLLAPSE",
        "MODERATE_DEGRADATION",
        "THRESHOLD_SPECIFIC_SURVIVAL",
        "SECURITY_OPERATING_POINT_SURVIVAL",
        "SOC_CAPACITY_EXCEEDANCE",
        "COST_BREAK_EVEN_AT_VERY_LOW_PREVALENCE",
        "UNEXPECTED_OPERATIONAL_ROBUSTNESS",
    ],

    "unexpected_results":
        "REPORT_EXACTLY",
}


# ==============================================================================
# 35. ANTI-ADAPTATION
# ==============================================================================

anti_adaptation = {
    "stage":
        "Stage25-0",

    "after_remote_freeze": {
        "change_prevalence_grid":
            "FORBIDDEN",

        "drop_0.01_percent":
            "FORBIDDEN",

        "change_traffic_volume":
            "FORBIDDEN",

        "change_service_time":
            "FORBIDDEN",

        "change_capacity_tiers":
            "FORBIDDEN",

        "change_cost_ratio":
            "FORBIDDEN",

        "change_ppv_targets":
            "FORBIDDEN",

        "new_threshold":
            "FORBIDDEN",

        "prevalence_specific_threshold":
            "FORBIDDEN",

        "ppv_specific_threshold":
            "FORBIDDEN",

        "new_inference":
            "FORBIDDEN",

        "new_probability_array":
            "FORBIDDEN",

        "model_refit":
            "FORBIDDEN",

        "target_reopening":
            "FORBIDDEN",

        "drop_poor_result":
            "FORBIDDEN",

        "add_favorable_cost_ratio":
            "FORBIDDEN",

        "redefine_capacity":
            "FORBIDDEN",

        "average_transfer_directions":
            "FORBIDDEN",
    },

    "unexpected_results":
        "REPORT_AS_RESULTS",
}


# ==============================================================================
# 36. INHERITED ARTIFACT HASH MANIFEST
# ==============================================================================

artifact_hash_payload = {
    "stage":
        "Stage25-0",

    "repository_parent":
        EXPECTED_PARENT,

    "byte_verified":
        dict(
            sorted(
                byte_verified.items()
            )
        ),

    "closure_anchors": {
        "stage24_final_synthesis_sha256":
            stage24_final_sha,

        "stage24_publication_manifest_sha256":
            stage24_pub_sha,

        "stage24_protocol_sha256":
            stage24_protocol_sha,

        "stage24_cicids2017_contract_sha256":
            stage24_contract_sha,

        "stage22_membership_summary_sha256":
            membership_summary_sha,

        "stage22_random_membership_sha256":
            random_membership_sha,

        "stage22_day_offsets_sha256":
            day_offsets_sha,
    },

    "declared_sha_fields_from_frozen_result_receipts":
        declared_hashes,

    "stage25_0_scientific_access": {
        "probability_npz_opened":
            0,

        "probability_npy_opened":
            0,

        "probability_arrays_created":
            0,

        "model_objects_loaded":
            0,

        "model_fit_calls":
            0,

        "model_inference_calls":
            0,

        "target_reopenings":
            0,

        "model_file_byte_reads":
            "SHA256_VERIFICATION_ONLY",
    },
}


# ==============================================================================
# 37. INHERITED OPERATING POINT PAYLOAD
# ==============================================================================

operating_point_payload = {
    "stage":
        "Stage25-0",

    "status":
        "FROZEN_BEFORE_ANY_STAGE25_PROJECTION",

    "repository_parent":
        EXPECTED_PARENT,

    "cell_count":
        len(
            inherited_cells
        ),

    "operating_point_count":
        operating_point_count,

    "cells":
        inherited_cells,

    "excluded": [
        {
            "cell":
                "STAGE22_RANDOM_REBALANCED",

            "reason":
                "NOT_IN_FROZEN_STAGE25_PRIMARY_NATURAL_PREVALENCE_FAMILY",
        },

        {
            "cell":
                "STAGE22_CHRONOLOGICAL_REBALANCED",

            "reason":
                "NOT_IN_FROZEN_STAGE25_PRIMARY_NATURAL_PREVALENCE_FAMILY",
        },

        {
            "cell":
                "STAGE22_FINAL_SINGLE_HOLDOUT",

            "reason":
                (
                    "USED_AS_CLOSURE_EVIDENCE_ONLY; NOT_A_FROZEN_STAGE25 "
                    "OPERATING_POINT_FAMILY"
                ),
        },

        {
            "cell":
                "STAGE24_BRIDGE62_GROUNDED_S4",

            "reason":
                "ADMINISTRATIVELY_CANCELLED_BEFORE_STAGE24_OPENING",
        },

        {
            "cell":
                "STAGE24_BRIDGE70_GROUNDED_S4",

            "reason":
                "ADMINISTRATIVELY_CANCELLED_BEFORE_STAGE24_OPENING",
        },
    ],

    "new_threshold_derivation":
        False,

    "new_prediction_access":
        False,
}


# ==============================================================================
# 38. WRITE PROTOCOL ARTIFACTS
# ==============================================================================

protocol_payloads = {
    "prevalence_grid.json":
        prevalence_payload,

    "observed_prevalence_receipts.json": {
        "stage":
            "Stage25-0",

        "status":
            "EXACT_FROZEN_PREVALENCES",

        "receipts":
            observed_receipts,
    },

    "inherited_operating_points.json":
        operating_point_payload,

    "inherited_artifact_hashes.json":
        artifact_hash_payload,

    "prior_shift_assumption.json":
        prior_shift_payload,

    "traffic_volume_spec.json":
        traffic_payload,

    "bayesian_equations.json":
        bayesian_payload,

    "analyst_capacity_spec.json":
        capacity_payload,

    "cost_model.json":
        cost_payload,

    "threshold_policy.json":
        threshold_policy,

    "numerical_policy.json":
        numerical_policy,

    "uncertainty_policy.json":
        uncertainty_policy,

    "interpretation_matrix.json":
        interpretation_matrix,

    "prohibited_claims.json":
        prohibited_claims,

    "figure_plan.json":
        figure_plan,

    "sanity_test_plan.json":
        sanity_tests,

    "success_condition.json":
        success_condition,

    "anti_adaptation.json":
        anti_adaptation,

    "handoff_reconciliation.json":
        handoff_reconciliation,
}


for filename, payload in protocol_payloads.items():

    write_json(
        LOCK_DIR
        /
        filename,
        payload,
    )


# ==============================================================================
# 39. FREEZE RECORD
# ==============================================================================

protocol_hashes = {
    filename:
        sha256_file(
            LOCK_DIR
            /
            filename
        )
    for filename in sorted(
        protocol_payloads
    )
}


freeze_record = {
    "stage":
        "Stage25-0",

    "status":
        "COMPLETE_PROTOCOL_LOCK_READY_FOR_REMOTE_FREEZE",

    "created_at_utc":
        datetime.now(
            timezone.utc
        ).isoformat(),

    "repository_parent":
        EXPECTED_PARENT,

    "objective":
        (
            "Analytically translate already-frozen operating characteristics "
            "under deployment prevalence and SOC-capacity stress."
        ),

    "inheritance": {
        "stage22_cells":
            2,

        "stage24_cells":
            6,

        "total_cells":
            8,

        "operating_points":
            24,
    },

    "future_analysis_shape": {
        "prevalence_points":
            6,

        "projected_rows":
            144,

        "ppv_targets":
            5,
    },

    "absolute_stage25_rules": {
        "new_model_fits":
            0,

        "new_model_inference":
            0,

        "new_probability_arrays":
            0,

        "target_reopenings":
            0,
    },

    "stage25_0_scientific_access": {
        "model_fit_calls":
            0,

        "model_inference_calls":
            0,

        "probability_arrays_opened":
            0,

        "probability_arrays_created":
            0,

        "target_features_read":
            0,

        "target_reopenings":
            0,

        "prevalence_projections_calculated":
            0,

        "ppv_projections_calculated":
            0,

        "soc_projections_calculated":
            0,

        "cost_projections_calculated":
            0,
    },

    "recovery_note": {
        "previous_failure":
            (
                "Stage24-2D bridge70 model receipt omitted model_file "
                "because model was inherited from Stage22R."
            ),

        "resolution":
            (
                "Canonical Stage22R chronological model paths were used and "
                "verified against Stage24 model SHA256 receipts."
            ),

        "scientific_change":
            False,

        "projection_performed_before_fix":
            False,
    },

    "stage25_isolates":
        "BASE_RATE_PRIOR_SHIFT_WITH_FIXED_TPR_FPR",

    "stage22_stage24_show":
        "TPR_FPR_CAN_CHANGE_UNDER_TEMPORAL_AND_DOMAIN_SHIFT",

    "must_not_conflate":
        True,

    "operational_collapse_required":
        False,

    "next_authorized_after_remote_verification":
        "STAGE25_1_BAYESIAN_PROJECTION",

    "protocol_file_hashes":
        protocol_hashes,
}


FREEZE_RECORD = (
    LOCK_DIR
    /
    "freeze_record.json"
)


write_json(
    FREEZE_RECORD,
    freeze_record,
)


freeze_record_sha = sha256_file(
    FREEZE_RECORD
)


write_text(
    LOCK_DIR
    /
    "freeze_record.sha256",
    (
        f"{freeze_record_sha}  "
        "freeze_record.json"
    ),
)


# ==============================================================================
# 40. CHECKSUM MANIFEST
# ==============================================================================

CHECKSUMS = (
    LOCK_DIR
    /
    "checksums.sha256"
)


lines = []


for path in sorted(
    LOCK_DIR.iterdir(),
    key=lambda p:
        p.name,
):

    if path == CHECKSUMS:

        continue

    lines.append(
        f"{sha256_file(path)}  {path.name}"
    )


write_text(
    CHECKSUMS,
    "\n".join(
        lines
    ),
)


print("=" * 120)
print("LOCAL STAGE25-0 LOCK CREATED")
print("=" * 120)

print(
    "Directory:"
)

print(
    " ",
    LOCK_DIR.relative_to(
        REPO
    )
)

print()

print(
    "Freeze record SHA:"
)

print(
    " ",
    freeze_record_sha
)

print()

print(
    "Frozen cells:             8"
)

print(
    "Frozen operating points:  24"
)

print(
    "Frozen prevalence points: 6"
)

print(
    "Future projection rows:   144"
)

print()

print(
    "STAGE25 PROJECTIONS:      0"
)

print(
    "MODEL FITS:               0"
)

print(
    "MODEL INFERENCE:          0"
)

print(
    "PROBABILITY ARRAYS:       0"
)

print(
    "TARGET REOPENINGS:        0"
)

print()


# ==============================================================================
# 41. GIT SAFETY AUDIT
# ==============================================================================

print("=" * 120)
print("GIT SAFETY AUDIT")
print("=" * 120)


tracked_dirty = {
    line
    for line in git_cmd(
        "diff",
        "--name-only",
    ).splitlines()
    if line
}


untracked = {
    line
    for line in git_cmd(
        "ls-files",
        "--others",
        "--exclude-standard",
    ).splitlines()
    if line
}


dirty = (
    tracked_dirty
    |
    untracked
)


allowed_prefix = (
    "results/stage25_prevalence_stress/"
    "stage25_0_protocol_lock/"
)


unexpected = [
    path
    for path in sorted(
        dirty
    )
    if not path.startswith(
        allowed_prefix
    )
]


if unexpected:

    raise RuntimeError(
        "\nUnexpected repository changes:\n"
        +
        "\n".join(
            unexpected
        )
    )


if not dirty:

    raise RuntimeError(
        "Stage25-0 generated no repository changes."
    )


print(
    "[PASS] Only Stage25-0 lock files are dirty."
)

print()


# ==============================================================================
# 42. REMOTE PARENT GATE
# ==============================================================================

remote_precommit = git_cmd(
    "ls-remote",
    "origin",
    "refs/heads/main",
    auth_header=auth_header,
).split()[0]


if remote_precommit != EXPECTED_PARENT:

    raise RuntimeError(
        "\nRemote main moved before protocol commit.\n"
        f"Expected: {EXPECTED_PARENT}\n"
        f"Actual:   {remote_precommit}"
    )


print(
    "[PASS] Remote main unchanged before commit."
)

print()


# ==============================================================================
# 43. GIT AUTHOR
# ==============================================================================

author_name = git_cmd(
    "config",
    "--local",
    "--get",
    "user.name",
    check=False,
)


author_email = git_cmd(
    "config",
    "--local",
    "--get",
    "user.email",
    check=False,
)


if not author_name:

    git_cmd(
        "config",
        "--local",
        "user.name",
        git_cmd(
            "log",
            "-1",
            "--format=%an",
        ),
    )


if not author_email:

    git_cmd(
        "config",
        "--local",
        "user.email",
        git_cmd(
            "log",
            "-1",
            "--format=%ae",
        ),
    )


# ==============================================================================
# 44. STAGE
# ==============================================================================

git_cmd(
    "add",
    "--",
    str(
        LOCK_DIR.relative_to(
            REPO
        )
    ),
)


staged = {
    line
    for line in git_cmd(
        "diff",
        "--cached",
        "--name-only",
    ).splitlines()
    if line
}


if not staged:

    raise RuntimeError(
        "No Stage25-0 files staged."
    )


bad_staged = [
    p
    for p in staged
    if not p.startswith(
        allowed_prefix
    )
]


if bad_staged:

    raise RuntimeError(
        "\nUnexpected staged files:\n"
        +
        "\n".join(
            sorted(
                bad_staged
            )
        )
    )


if git_cmd(
    "diff",
    "--name-only",
):

    raise RuntimeError(
        "Unstaged tracked changes remain."
    )


if git_cmd(
    "ls-files",
    "--others",
    "--exclude-standard",
):

    raise RuntimeError(
        "Untracked changes remain."
    )


print(
    "[PASS] Complete Stage25-0 lock staged and nothing else."
)

print()


# ==============================================================================
# 45. COMMIT
# ==============================================================================

print("=" * 120)
print("COMMIT STAGE25-0")
print("=" * 120)


commit_output = git_cmd(
    "commit",
    "-m",
    "stage25: freeze prevalence operational stress protocol",
)


print(
    commit_output
)

print()


commit = git_cmd(
    "rev-parse",
    "HEAD",
)


parent = git_cmd(
    "rev-parse",
    "HEAD^",
)


if parent != EXPECTED_PARENT:

    raise RuntimeError(
        "\nStage25-0 parent mismatch.\n"
        f"Expected: {EXPECTED_PARENT}\n"
        f"Actual:   {parent}"
    )


print(
    "Commit:",
    commit,
)

print()


# ==============================================================================
# 46. PUSH + REMOTE VERIFY
# ==============================================================================

print("=" * 120)
print("PUSH + REMOTE VERIFICATION")
print("=" * 120)


push_output = git_cmd(
    "push",
    "origin",
    "HEAD:main",
    auth_header=auth_header,
)


print(
    push_output
)

print()


remote_after = git_cmd(
    "ls-remote",
    "origin",
    "refs/heads/main",
    auth_header=auth_header,
).split()[0]


if remote_after != commit:

    raise RuntimeError(
        "\nRemote verification failed.\n"
        f"Local:  {commit}\n"
        f"Remote: {remote_after}"
    )


status_after = git_cmd(
    "status",
    "--porcelain",
)


if status_after:

    raise RuntimeError(
        "\nRepository not clean after push:\n"
        +
        status_after
    )


print(
    "[PASS] Remote main == Stage25-0 lock commit."
)

print(
    "[PASS] Repository clean."
)

print()


# ==============================================================================
# 47. FINAL
# ==============================================================================

print("=" * 120)
print("STAGE25-0 PROTOCOL LOCK: PASS")
print("=" * 120)

print()

print(
    "Parent Stage24 closeout:"
)

print(
    " ",
    EXPECTED_PARENT
)

print()

print(
    "Stage25-0 commit:"
)

print(
    " ",
    commit
)

print()

print(
    "Remote main:"
)

print(
    " ",
    remote_after
)

print()

print(
    "Freeze record SHA:"
)

print(
    " ",
    freeze_record_sha
)

print()

print(
    "Inherited cells:              8"
)

print(
    "Inherited operating points:   24"
)

print(
    "Prevalence grid:              10%, 3%, 1%, 0.3%, 0.1%, 0.01%"
)

print(
    "PPV target grid:              10%, 25%, 50%, 75%, 90%"
)

print(
    "Benign flows/day:             1,000,000"
)

print(
    "Alert service time:           2 minutes"
)

print(
    "Analyst tiers:                1 / 3 / 10"
)

print(
    "Relative cost:                FP=1 / FN=100"
)

print()

print(
    "NEW MODEL FITS:               0"
)

print(
    "NEW MODEL INFERENCE:          0"
)

print(
    "NEW PROBABILITY ARRAYS:       0"
)

print(
    "TARGET REOPENINGS:            0"
)

print(
    "STAGE25 PROJECTIONS:          0"
)

print()

print(
    "NEXT AUTHORIZED ACTION:"
)

print(
    "  STAGE25-1 — BAYESIAN PREVALENCE PROJECTION"
)

print(
    "  ONLY AFTER independent GitHub verification."
)

print()

print(
    "STOP HERE."
)

print("=" * 120)

# %% [Stage25 notebook cell 3]
# ==============================================================================
# STAGE25-1 — BAYESIAN PREVALENCE PROJECTION
#
# Authorized by remotely frozen Stage25-0 protocol:
#   commit:
#     988fc5dd85018659749466ad9f8a1efcd5723ca9
#
# PURPOSE
# -------
# Deterministically translate the 24 frozen operating points across the
# preregistered prevalence grid:
#
#   10%, 3%, 1%, 0.3%, 0.1%, 0.01%
#
# Compute:
#   - PPV
#   - NPV
#   - LR+
#   - LR-
#   - prior odds
#   - posterior odds after positive alert
#   - posterior probability after positive alert
#   - analytic prevalence needed for PPV targets:
#       10%, 25%, 50%, 75%, 90%
#   - required FPR for each PPV target at each prevalence
#
# SCIENTIFIC RULES
# ----------------
# NEW MODEL FITS:             0
# NEW MODEL INFERENCE:        0
# NEW PROBABILITY ARRAYS:     0
# TARGET REOPENINGS:          0
# NEW THRESHOLD SELECTION:    0
#
# This stage reads ONLY the frozen Stage25-0 protocol artifacts.
#
# It DOES NOT:
#   - load model files
#   - load Stage22/Stage24 predictions
#   - read target features
#   - read target labels
#   - calculate SOC capacity
#   - calculate relative cost
#
# Stage25-1 is therefore a deterministic analytic transformation of the
# already-frozen empirical TPR/FPR values.
# ==============================================================================

from __future__ import annotations

import os
import csv
import json
import math
import base64
import hashlib
import subprocess
from pathlib import Path
from datetime import datetime, timezone


print("=" * 120)
print("STAGE25-1 — BAYESIAN PREVALENCE PROJECTION")
print("=" * 120)
print()


# ==============================================================================
# 0. FROZEN ANCHORS
# ==============================================================================

REPO = Path(
    "/kaggle/working/ids2018-validation-safe-ablation"
)

EXPECTED_PARENT = (
    "988fc5dd85018659749466ad9f8a1efcd5723ca9"
)

EXPECTED_FREEZE_RECORD_SHA = (
    "d231af1e4f07363c4d932acc99e1052e3b33bd2d24ca22e4386f4c7c378827b7"
)

LOCK_DIR = (
    REPO
    / "results"
    / "stage25_prevalence_stress"
    / "stage25_0_protocol_lock"
)

OUT_DIR = (
    REPO
    / "results"
    / "stage25_prevalence_stress"
    / "stage25_1_bayesian_projection"
)

FREEZE_RECORD = (
    LOCK_DIR
    / "freeze_record.json"
)

FREEZE_RECORD_SHA = (
    LOCK_DIR
    / "freeze_record.sha256"
)

CHECKSUMS = (
    LOCK_DIR
    / "checksums.sha256"
)

INHERITED_OPS = (
    LOCK_DIR
    / "inherited_operating_points.json"
)

PREVALENCE_SPEC = (
    LOCK_DIR
    / "prevalence_grid.json"
)

BAYESIAN_SPEC = (
    LOCK_DIR
    / "bayesian_equations.json"
)

NUMERICAL_SPEC = (
    LOCK_DIR
    / "numerical_policy.json"
)

SANITY_SPEC = (
    LOCK_DIR
    / "sanity_test_plan.json"
)

ANTI_ADAPTATION = (
    LOCK_DIR
    / "anti_adaptation.json"
)


# ==============================================================================
# 1. HELPERS
# ==============================================================================

def run_cmd(
    args,
    *,
    cwd=None,
    check=True,
):

    proc = subprocess.run(
        [str(x) for x in args],
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    if check and proc.returncode != 0:

        raise RuntimeError(
            "\nCommand failed:\n"
            + " ".join(str(x) for x in args)
            + "\n\n"
            + (proc.stdout or "")
        )

    return (proc.stdout or "").strip()


def git_cmd(
    *args,
    auth_header=None,
    check=True,
):

    cmd = ["git"]

    if auth_header is not None:

        cmd += [
            "-c",
            "credential.helper=",
            "-c",
            f"http.extraHeader=AUTHORIZATION: Basic {auth_header}",
        ]

    cmd += [str(x) for x in args]

    return run_cmd(
        cmd,
        cwd=REPO,
        check=check,
    )


def sha256_file(
    path,
):

    path = Path(path)

    h = hashlib.sha256()

    with path.open("rb") as fh:

        while True:

            block = fh.read(
                16 * 1024 * 1024
            )

            if not block:
                break

            h.update(block)

    return h.hexdigest()


def load_json(
    path,
):

    path = Path(path)

    if not path.is_file():

        raise RuntimeError(
            f"Missing JSON:\n{path}"
        )

    return json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )


def write_json(
    path,
    payload,
):

    path = Path(path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    path.write_text(
        json.dumps(
            payload,
            indent=2,
            sort_keys=True,
            ensure_ascii=False,
            allow_nan=False,
        )
        + "\n",
        encoding="utf-8",
    )


def write_text(
    path,
    text,
):

    path = Path(path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    path.write_text(
        str(text).rstrip()
        + "\n",
        encoding="utf-8",
    )


def write_csv(
    path,
    rows,
):

    path = Path(path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    rows = list(rows)

    if not rows:

        raise RuntimeError(
            f"Cannot write empty CSV:\n{path}"
        )

    fields = list(
        rows[0].keys()
    )

    with path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as fh:

        writer = csv.DictWriter(
            fh,
            fieldnames=fields,
            lineterminator="\n",
        )

        writer.writeheader()

        for row in rows:

            if list(row.keys()) != fields:

                raise RuntimeError(
                    f"Inconsistent CSV field order:\n{path}"
                )

            writer.writerow(row)


def assert_close(
    actual,
    expected,
    *,
    atol=5e-14,
    label="value",
):

    if actual is None or expected is None:

        if actual != expected:

            raise RuntimeError(
                f"{label}: None mismatch."
            )

        return

    if not math.isclose(
        float(actual),
        float(expected),
        rel_tol=0.0,
        abs_tol=atol,
    ):

        raise RuntimeError(
            "\nNumerical consistency failure.\n"
            f"{label}\n"
            f"Expected: {expected!r}\n"
            f"Actual:   {actual!r}\n"
            f"Delta:    {float(actual)-float(expected):+.17e}"
        )


def ppv(
    tpr,
    fpr,
    pi,
):

    numerator = (
        tpr
        *
        pi
    )

    denominator = (
        numerator
        +
        fpr
        *
        (
            1.0
            -
            pi
        )
    )

    if denominator == 0.0:

        return None

    return (
        numerator
        /
        denominator
    )


def npv(
    tpr,
    fpr,
    pi,
):

    numerator = (
        (
            1.0
            -
            fpr
        )
        *
        (
            1.0
            -
            pi
        )
    )

    denominator = (
        numerator
        +
        (
            1.0
            -
            tpr
        )
        *
        pi
    )

    if denominator == 0.0:

        return None

    return (
        numerator
        /
        denominator
    )


def lr_plus(
    tpr,
    fpr,
):

    if fpr == 0.0:

        if tpr > 0.0:

            return (
                None,
                "POSITIVE_INFINITY",
            )

        return (
            None,
            "UNDEFINED_0_OVER_0",
        )

    return (
        tpr
        /
        fpr,
        "FINITE",
    )


def lr_minus(
    tpr,
    fpr,
):

    numerator = (
        1.0
        -
        tpr
    )

    denominator = (
        1.0
        -
        fpr
    )

    if denominator == 0.0:

        if numerator > 0.0:

            return (
                None,
                "POSITIVE_INFINITY",
            )

        return (
            None,
            "UNDEFINED_0_OVER_0",
        )

    return (
        numerator
        /
        denominator,
        "FINITE",
    )


def prior_odds(
    pi,
):

    if pi == 1.0:

        return None

    return (
        pi
        /
        (
            1.0
            -
            pi
        )
    )


def posterior_after_positive(
    pi,
    lr_value,
    lr_status,
):

    po = prior_odds(pi)

    if po is None:

        return {
            "prior_odds":
                None,

            "posterior_odds":
                None,

            "posterior_probability":
                None,

            "status":
                "UNDEFINED_PRIOR_ODDS",
        }


    if lr_status == "POSITIVE_INFINITY":

        if pi > 0.0:

            return {
                "prior_odds":
                    po,

                "posterior_odds":
                    None,

                "posterior_probability":
                    1.0,

                "status":
                    "POSITIVE_INFINITY_POSTERIOR_ODDS",
            }

        return {
            "prior_odds":
                po,

            "posterior_odds":
                None,

            "posterior_probability":
                None,

            "status":
                "UNDEFINED_ZERO_PRIOR_TIMES_INFINITY",
        }


    if lr_status != "FINITE":

        return {
            "prior_odds":
                po,

            "posterior_odds":
                None,

            "posterior_probability":
                None,

            "status":
                lr_status,
        }


    posterior_odds = (
        po
        *
        lr_value
    )

    posterior_probability = (
        posterior_odds
        /
        (
            1.0
            +
            posterior_odds
        )
    )


    return {
        "prior_odds":
            po,

        "posterior_odds":
            posterior_odds,

        "posterior_probability":
            posterior_probability,

        "status":
            "FINITE",
    }


def ppv_cliff_prevalence(
    tpr,
    fpr,
    q,
):

    denominator = (
        tpr
        *
        (
            1.0
            -
            q
        )
        +
        q
        *
        fpr
    )

    if denominator == 0.0:

        return (
            None,
            "UNDEFINED_ZERO_DENOMINATOR",
        )

    value = (
        q
        *
        fpr
        /
        denominator
    )

    return (
        value,
        "FINITE",
    )


def required_fpr(
    tpr,
    pi,
    q,
):

    denominator = (
        q
        *
        (
            1.0
            -
            pi
        )
    )

    if denominator == 0.0:

        return (
            None,
            "UNDEFINED_ZERO_DENOMINATOR",
        )

    value = (
        tpr
        *
        pi
        *
        (
            1.0
            -
            q
        )
        /
        denominator
    )

    return (
        value,
        "FINITE",
    )


# ==============================================================================
# 2. REPOSITORY + PROTOCOL GATE
# ==============================================================================

print("=" * 120)
print("GOVERNANCE GATE")
print("=" * 120)


head = git_cmd(
    "rev-parse",
    "HEAD",
)

status = git_cmd(
    "status",
    "--porcelain",
)


print(
    "HEAD:",
    head,
)


if head != EXPECTED_PARENT:

    raise RuntimeError(
        "\nUnexpected Stage25 parent.\n"
        f"Expected: {EXPECTED_PARENT}\n"
        f"Actual:   {head}"
    )


if status:

    raise RuntimeError(
        "\nRepository must be clean before Stage25-1:\n"
        + status
    )


if OUT_DIR.exists():

    existing = list(
        OUT_DIR.iterdir()
    )

    if existing:

        raise RuntimeError(
            "\nStage25-1 output directory already contains artifacts.\n"
            "Refusing accidental regeneration:\n"
            + "\n".join(
                str(x)
                for x in existing
            )
        )


freeze_sha = sha256_file(
    FREEZE_RECORD
)


if freeze_sha != EXPECTED_FREEZE_RECORD_SHA:

    raise RuntimeError(
        "\nStage25-0 freeze-record SHA mismatch.\n"
        f"Expected: {EXPECTED_FREEZE_RECORD_SHA}\n"
        f"Actual:   {freeze_sha}"
    )


sidecar_expected = (
    FREEZE_RECORD_SHA
    .read_text(
        encoding="utf-8"
    )
    .strip()
    .split()[0]
)


if sidecar_expected != EXPECTED_FREEZE_RECORD_SHA:

    raise RuntimeError(
        "Stage25-0 freeze-record sidecar changed."
    )


freeze = load_json(
    FREEZE_RECORD
)


if (
    freeze[
        "status"
    ]
    !=
    "COMPLETE_PROTOCOL_LOCK_READY_FOR_REMOTE_FREEZE"
):

    raise RuntimeError(
        "Stage25-0 lock status changed."
    )


if (
    freeze[
        "next_authorized_after_remote_verification"
    ]
    !=
    "STAGE25_1_BAYESIAN_PROJECTION"
):

    raise RuntimeError(
        "Stage25-1 is not the authorized next action."
    )


absolute_rules = freeze[
    "absolute_stage25_rules"
]


if absolute_rules != {
    "new_model_fits": 0,
    "new_model_inference": 0,
    "new_probability_arrays": 0,
    "target_reopenings": 0,
}:

    raise RuntimeError(
        "Stage25 absolute scientific rules changed."
    )


print(
    "Freeze record SHA:",
    freeze_sha,
)

print(
    "[PASS] Stage25-0 lock is exact."
)

print(
    "[PASS] Stage25-1 is remotely authorized."
)

print()


# ==============================================================================
# 3. VERIFY EVERY STAGE25-0 CHECKSUM
# ==============================================================================

print("=" * 120)
print("PROTOCOL CHECKSUM VERIFICATION")
print("=" * 120)


checksum_lines = [
    line.strip()
    for line in CHECKSUMS.read_text(
        encoding="utf-8"
    ).splitlines()
    if line.strip()
]


verified_checksum_count = 0


for line in checksum_lines:

    expected_sha, filename = line.split(
        None,
        1,
    )

    filename = filename.strip()

    path = (
        LOCK_DIR
        /
        filename
    )

    actual_sha = sha256_file(
        path
    )


    if actual_sha != expected_sha:

        raise RuntimeError(
            "\nProtocol checksum mismatch.\n"
            f"File:     {filename}\n"
            f"Expected: {expected_sha}\n"
            f"Actual:   {actual_sha}"
        )


    verified_checksum_count += 1


for filename, expected_sha in freeze[
    "protocol_file_hashes"
].items():

    path = (
        LOCK_DIR
        /
        filename
    )

    actual_sha = sha256_file(
        path
    )


    if actual_sha != expected_sha:

        raise RuntimeError(
            "\nFreeze-record protocol hash mismatch.\n"
            f"File: {filename}"
        )


print(
    "Files verified:",
    verified_checksum_count,
)

print(
    "[PASS] Complete Stage25-0 protocol checksum chain verified."
)

print()


# ==============================================================================
# 4. LOAD FROZEN INPUTS
# ==============================================================================

inventory = load_json(
    INHERITED_OPS
)

prevalence_spec = load_json(
    PREVALENCE_SPEC
)

bayesian_spec = load_json(
    BAYESIAN_SPEC
)

numerical_spec = load_json(
    NUMERICAL_SPEC
)

sanity_spec = load_json(
    SANITY_SPEC
)

anti_adaptation = load_json(
    ANTI_ADAPTATION
)


if inventory[
    "cell_count"
] != 8:

    raise RuntimeError(
        "Expected 8 inherited cells."
    )


if inventory[
    "operating_point_count"
] != 24:

    raise RuntimeError(
        "Expected 24 inherited operating points."
    )


if inventory[
    "new_prediction_access"
] is not False:

    raise RuntimeError(
        "Unexpected prediction-access policy."
    )


if inventory[
    "new_threshold_derivation"
] is not False:

    raise RuntimeError(
        "Unexpected threshold policy."
    )


prevalence_grid = prevalence_spec[
    "prevalence_grid"
][
    "decimal"
]


ppv_targets = prevalence_spec[
    "ppv_target_grid"
][
    "decimal"
]


if prevalence_grid != [
    0.10,
    0.03,
    0.01,
    0.003,
    0.001,
    0.0001,
]:

    raise RuntimeError(
        "Frozen prevalence grid changed."
    )


if ppv_targets != [
    0.10,
    0.25,
    0.50,
    0.75,
    0.90,
]:

    raise RuntimeError(
        "Frozen PPV target grid changed."
    )


if numerical_spec[
    "calculation_dtype"
] != "IEEE754_FLOAT64":

    raise RuntimeError(
        "Unexpected numerical policy."
    )


if numerical_spec[
    "epsilon_injection"
] != "FORBIDDEN":

    raise RuntimeError(
        "Unexpected epsilon policy."
    )


print(
    "Cells:             ",
    inventory[
        "cell_count"
    ],
)

print(
    "Operating points:  ",
    inventory[
        "operating_point_count"
    ],
)

print(
    "Prevalence points: ",
    len(
        prevalence_grid
    ),
)

print(
    "PPV targets:       ",
    len(
        ppv_targets
    ),
)

print()


# ==============================================================================
# 5. FLATTEN OPERATING POINTS
# ==============================================================================

operating_points = []


for cell in inventory[
    "cells"
]:

    for op_name in [
        "STANDARD",
        "BALANCED",
        "SECURITY",
    ]:

        op = cell[
            "operating_points"
        ][
            op_name
        ]


        operating_points.append(
            {
                "cell_id":
                    cell[
                        "cell_id"
                    ],

                "source_stage":
                    cell[
                        "source_stage"
                    ],

                "family":
                    cell[
                        "family"
                    ],

                "direction":
                    cell[
                        "direction"
                    ],

                "bridge":
                    cell[
                        "bridge"
                    ],

                "variant":
                    cell[
                        "variant"
                    ],

                "identity_duplicate_of":
                    cell.get(
                        "identity_duplicate_of"
                    ),

                "operating_point":
                    op_name,

                "threshold":
                    float(
                        op[
                            "threshold"
                        ]
                    ),

                "tpr":
                    float(
                        op[
                            "tpr"
                        ]
                    ),

                "fpr":
                    float(
                        op[
                            "fpr"
                        ]
                    ),

                "frozen_precision":
                    (
                        None
                        if op[
                            "precision"
                        ] is None
                        else float(
                            op[
                                "precision"
                            ]
                        )
                    ),

                "frozen_f1":
                    (
                        None
                        if op.get(
                            "f1"
                        ) is None
                        else float(
                            op[
                                "f1"
                            ]
                        )
                    ),

                "frozen_f2":
                    (
                        None
                        if op.get(
                            "f2"
                        ) is None
                        else float(
                            op[
                                "f2"
                            ]
                        )
                    ),

                "observed_prevalence":
                    float(
                        cell[
                            "evaluation_population"
                        ][
                            "observed_prevalence"
                        ]
                    ),

                "evaluation_rows":
                    int(
                        cell[
                            "evaluation_population"
                        ][
                            "rows"
                        ]
                    ),

                "evaluation_attack":
                    int(
                        cell[
                            "evaluation_population"
                        ][
                            "attack"
                        ]
                    ),

                "evaluation_benign":
                    int(
                        cell[
                            "evaluation_population"
                        ][
                            "benign"
                        ]
                    ),
            }
        )


if len(
    operating_points
) != 24:

    raise RuntimeError(
        "Flattened operating-point count is not 24."
    )


unique_keys = {
    (
        row[
            "cell_id"
        ],
        row[
            "operating_point"
        ],
    )
    for row in operating_points
}


if len(
    unique_keys
) != 24:

    raise RuntimeError(
        "Operating-point identifiers are not unique."
    )


print(
    "[PASS] 24 frozen operating points flattened."
)

print()


# ==============================================================================
# 6. LIKELIHOOD RATIOS + OBSERVED PREVALENCE REPRODUCTION
# ==============================================================================

lr_rows = []

observed_ppv_tests = []


for op in operating_points:

    tpr = op[
        "tpr"
    ]

    fpr = op[
        "fpr"
    ]

    lp_value, lp_status = lr_plus(
        tpr,
        fpr,
    )

    lm_value, lm_status = lr_minus(
        tpr,
        fpr,
    )


    observed_pi = op[
        "observed_prevalence"
    ]

    reproduced_precision = ppv(
        tpr,
        fpr,
        observed_pi,
    )


    assert_close(
        reproduced_precision,
        op[
            "frozen_precision"
        ],
        atol=5e-14,
        label=(
            op[
                "cell_id"
            ]
            +
            "/"
            +
            op[
                "operating_point"
            ]
            +
            " observed-prevalence PPV"
        ),
    )


    observed_ppv_tests.append(
        {
            "cell_id":
                op[
                    "cell_id"
                ],

            "operating_point":
                op[
                    "operating_point"
                ],

            "observed_prevalence":
                observed_pi,

            "frozen_precision":
                op[
                    "frozen_precision"
                ],

            "recomputed_ppv":
                reproduced_precision,

            "absolute_error":
                abs(
                    reproduced_precision
                    -
                    op[
                        "frozen_precision"
                    ]
                ),

            "passed":
                True,
        }
    )


    lr_rows.append(
        {
            "cell_id":
                op[
                    "cell_id"
                ],

            "family":
                op[
                    "family"
                ],

            "direction":
                op[
                    "direction"
                ],

            "bridge":
                op[
                    "bridge"
                ],

            "variant":
                op[
                    "variant"
                ],

            "operating_point":
                op[
                    "operating_point"
                ],

            "threshold":
                op[
                    "threshold"
                ],

            "tpr":
                tpr,

            "fpr":
                fpr,

            "lr_plus":
                lp_value,

            "lr_plus_status":
                lp_status,

            "lr_minus":
                lm_value,

            "lr_minus_status":
                lm_status,

            "observed_prevalence":
                observed_pi,

            "frozen_precision":
                op[
                    "frozen_precision"
                ],
        }
    )


print("=" * 120)
print("OBSERVED-PREVALENCE REPRODUCTION")
print("=" * 120)

print(
    "Operating points checked:",
    len(
        observed_ppv_tests
    ),
)

print(
    "Maximum |recomputed PPV - frozen precision|:",
    max(
        row[
            "absolute_error"
        ]
        for row in observed_ppv_tests
    ),
)

print()

print(
    "[PASS] All 24 frozen precisions reproduced from TPR/FPR/prevalence."
)

print()


# ==============================================================================
# 7. 144-ROW BAYESIAN PREVALENCE PROJECTION
# ==============================================================================

projection_rows = []


for op in operating_points:

    tpr = op[
        "tpr"
    ]

    fpr = op[
        "fpr"
    ]


    lp_value, lp_status = lr_plus(
        tpr,
        fpr,
    )

    lm_value, lm_status = lr_minus(
        tpr,
        fpr,
    )


    for prevalence_index, pi in enumerate(
        prevalence_grid
    ):

        projected_ppv = ppv(
            tpr,
            fpr,
            pi,
        )

        projected_npv = npv(
            tpr,
            fpr,
            pi,
        )

        posterior = posterior_after_positive(
            pi,
            lp_value,
            lp_status,
        )


        if (
            projected_ppv is not None
            and
            posterior[
                "posterior_probability"
            ] is not None
        ):

            assert_close(
                posterior[
                    "posterior_probability"
                ],
                projected_ppv,
                atol=5e-14,
                label=(
                    op[
                        "cell_id"
                    ]
                    +
                    "/"
                    +
                    op[
                        "operating_point"
                    ]
                    +
                    f"/pi={pi} Bayes odds identity"
                ),
            )


        projection_rows.append(
            {
                "cell_id":
                    op[
                        "cell_id"
                    ],

                "source_stage":
                    op[
                        "source_stage"
                    ],

                "family":
                    op[
                        "family"
                    ],

                "direction":
                    op[
                        "direction"
                    ],

                "bridge":
                    op[
                        "bridge"
                    ],

                "variant":
                    op[
                        "variant"
                    ],

                "identity_duplicate_of":
                    op[
                        "identity_duplicate_of"
                    ],

                "operating_point":
                    op[
                        "operating_point"
                    ],

                "threshold":
                    op[
                        "threshold"
                    ],

                "tpr":
                    tpr,

                "fpr":
                    fpr,

                "frozen_f1":
                    op[
                        "frozen_f1"
                    ],

                "frozen_precision":
                    op[
                        "frozen_precision"
                    ],

                "observed_prevalence":
                    op[
                        "observed_prevalence"
                    ],

                "prevalence_index":
                    prevalence_index,

                "projection_prevalence":
                    pi,

                "ppv":
                    projected_ppv,

                "npv":
                    projected_npv,

                "lr_plus":
                    lp_value,

                "lr_plus_status":
                    lp_status,

                "lr_minus":
                    lm_value,

                "lr_minus_status":
                    lm_status,

                "prior_odds":
                    posterior[
                        "prior_odds"
                    ],

                "posterior_odds_positive":
                    posterior[
                        "posterior_odds"
                    ],

                "posterior_probability_positive":
                    posterior[
                        "posterior_probability"
                    ],

                "posterior_status":
                    posterior[
                        "status"
                    ],
            }
        )


expected_projection_rows = (
    24
    *
    6
)


if len(
    projection_rows
) != expected_projection_rows:

    raise RuntimeError(
        "\nProjection matrix incomplete.\n"
        f"Expected: {expected_projection_rows}\n"
        f"Actual:   {len(projection_rows)}"
    )


projection_keys = {
    (
        row[
            "cell_id"
        ],
        row[
            "operating_point"
        ],
        row[
            "projection_prevalence"
        ],
    )
    for row in projection_rows
}


if len(
    projection_keys
) != expected_projection_rows:

    raise RuntimeError(
        "Projection matrix contains duplicate cells."
    )


print("=" * 120)
print("BAYESIAN PROJECTION MATRIX")
print("=" * 120)

print(
    "Rows:",
    len(
        projection_rows
    ),
)

print(
    "[PASS] Complete 24 × 6 = 144 projection matrix."
)

print()


# ==============================================================================
# 8. PPV MONOTONICITY TEST
# ==============================================================================

monotonicity_tests = []


for op in operating_points:

    rows = [
        row
        for row in projection_rows
        if (
            row[
                "cell_id"
            ]
            ==
            op[
                "cell_id"
            ]
            and
            row[
                "operating_point"
            ]
            ==
            op[
                "operating_point"
            ]
        )
    ]


    rows = sorted(
        rows,
        key=lambda x:
            x[
                "projection_prevalence"
            ],
    )


    ppv_values = [
        row[
            "ppv"
        ]
        for row in rows
    ]


    if any(
        value is None
        for value in ppv_values
    ):

        raise RuntimeError(
            "Unexpected undefined PPV in frozen Stage25 grid."
        )


    nondecreasing = all(
        ppv_values[
            i
        ]
        <=
        ppv_values[
            i + 1
        ]
        +
        1e-15
        for i in range(
            len(
                ppv_values
            )
            -
            1
        )
    )


    if (
        op[
            "tpr"
        ]
        >
        0.0
        and
        op[
            "fpr"
        ]
        >
        0.0
    ):

        strict = all(
            ppv_values[
                i
            ]
            <
            ppv_values[
                i + 1
            ]
            for i in range(
                len(
                    ppv_values
                )
                -
                1
            )
        )

    else:

        strict = None


    if not nondecreasing:

        raise RuntimeError(
            "\nPPV monotonicity failed:\n"
            f"{op['cell_id']} / {op['operating_point']}"
        )


    if (
        strict is False
        and
        op[
            "tpr"
        ]
        >
        0.0
        and
        op[
            "fpr"
        ]
        >
        0.0
    ):

        raise RuntimeError(
            "\nStrict PPV monotonicity failed:\n"
            f"{op['cell_id']} / {op['operating_point']}"
        )


    monotonicity_tests.append(
        {
            "cell_id":
                op[
                    "cell_id"
                ],

            "operating_point":
                op[
                    "operating_point"
                ],

            "nondecreasing":
                nondecreasing,

            "strict_when_tpr_fpr_positive":
                strict,

            "passed":
                True,
        }
    )


print(
    "[PASS] PPV monotonicity verified for all 24 operating points."
)

print()


# ==============================================================================
# 9. ANALYTIC PPV CLIFFS
# ==============================================================================

ppv_cliff_rows = []

ppv_cliff_tests = []


for op in operating_points:

    for q in ppv_targets:

        pi_star, status_star = ppv_cliff_prevalence(
            op[
                "tpr"
            ],
            op[
                "fpr"
            ],
            q,
        )


        recomputed_q = None

        absolute_error = None


        if (
            status_star
            ==
            "FINITE"
        ):

            recomputed_q = ppv(
                op[
                    "tpr"
                ],
                op[
                    "fpr"
                ],
                pi_star,
            )


            assert_close(
                recomputed_q,
                q,
                atol=5e-13,
                label=(
                    op[
                        "cell_id"
                    ]
                    +
                    "/"
                    +
                    op[
                        "operating_point"
                    ]
                    +
                    f"/PPV target={q}"
                ),
            )


            absolute_error = abs(
                recomputed_q
                -
                q
            )


        ppv_cliff_rows.append(
            {
                "cell_id":
                    op[
                        "cell_id"
                    ],

                "family":
                    op[
                        "family"
                    ],

                "direction":
                    op[
                        "direction"
                    ],

                "bridge":
                    op[
                        "bridge"
                    ],

                "variant":
                    op[
                        "variant"
                    ],

                "operating_point":
                    op[
                        "operating_point"
                    ],

                "threshold":
                    op[
                        "threshold"
                    ],

                "tpr":
                    op[
                        "tpr"
                    ],

                "fpr":
                    op[
                        "fpr"
                    ],

                "ppv_target":
                    q,

                "required_prevalence":
                    pi_star,

                "status":
                    status_star,

                "verification_ppv":
                    recomputed_q,
            }
        )


        ppv_cliff_tests.append(
            {
                "cell_id":
                    op[
                        "cell_id"
                    ],

                "operating_point":
                    op[
                        "operating_point"
                    ],

                "ppv_target":
                    q,

                "required_prevalence":
                    pi_star,

                "verification_ppv":
                    recomputed_q,

                "absolute_error":
                    absolute_error,

                "passed":
                    True,
            }
        )


if len(
    ppv_cliff_rows
) != (
    24
    *
    5
):

    raise RuntimeError(
        "PPV cliff table must contain 120 rows."
    )


ppv50_tests = [
    row
    for row in ppv_cliff_tests
    if row[
        "ppv_target"
    ]
    ==
    0.50
]


if len(
    ppv50_tests
) != 24:

    raise RuntimeError(
        "Expected 24 PPV50 tests."
    )


print("=" * 120)
print("ANALYTIC PPV CLIFFS")
print("=" * 120)

print(
    "Target equations checked:",
    len(
        ppv_cliff_tests
    ),
)

print(
    "PPV50 checks:",
    len(
        ppv50_tests
    ),
)

print(
    "[PASS] Analytic PPV cliff identities verified."
)

print()


# ==============================================================================
# 10. REQUIRED FPR FOR TARGET PPV
# ==============================================================================

required_fpr_rows = []

required_fpr_tests = []


for op in operating_points:

    for pi in prevalence_grid:

        for q in ppv_targets:

            max_fpr, status_fpr = required_fpr(
                op[
                    "tpr"
                ],
                pi,
                q,
            )


            actual_fpr = op[
                "fpr"
            ]


            meets_required_fpr = (
                None
                if max_fpr is None
                else
                actual_fpr
                <=
                max_fpr
            )


            ppv_at_required = None

            absolute_error = None


            if (
                status_fpr
                ==
                "FINITE"
            ):

                ppv_at_required = ppv(
                    op[
                        "tpr"
                    ],
                    max_fpr,
                    pi,
                )


                assert_close(
                    ppv_at_required,
                    q,
                    atol=5e-13,
                    label=(
                        op[
                            "cell_id"
                        ]
                        +
                        "/"
                        +
                        op[
                            "operating_point"
                        ]
                        +
                        f"/pi={pi}/target PPV={q}"
                    ),
                )


                absolute_error = abs(
                    ppv_at_required
                    -
                    q
                )


            required_fpr_rows.append(
                {
                    "cell_id":
                        op[
                            "cell_id"
                        ],

                    "family":
                        op[
                            "family"
                        ],

                    "direction":
                        op[
                            "direction"
                        ],

                    "bridge":
                        op[
                            "bridge"
                        ],

                    "variant":
                        op[
                            "variant"
                        ],

                    "operating_point":
                        op[
                            "operating_point"
                        ],

                    "threshold":
                        op[
                            "threshold"
                        ],

                    "tpr":
                        op[
                            "tpr"
                        ],

                    "actual_fpr":
                        actual_fpr,

                    "projection_prevalence":
                        pi,

                    "ppv_target":
                        q,

                    "required_max_fpr":
                        max_fpr,

                    "required_fpr_status":
                        status_fpr,

                    "actual_fpr_meets_requirement":
                        meets_required_fpr,

                    "verification_ppv":
                        ppv_at_required,
                }
            )


            required_fpr_tests.append(
                {
                    "cell_id":
                        op[
                            "cell_id"
                        ],

                    "operating_point":
                        op[
                            "operating_point"
                        ],

                    "projection_prevalence":
                        pi,

                    "ppv_target":
                        q,

                    "absolute_error":
                        absolute_error,

                    "passed":
                        True,
                }
            )


if len(
    required_fpr_rows
) != (
    24
    *
    6
    *
    5
):

    raise RuntimeError(
        "Required-FPR table must contain 720 rows."
    )


print(
    "Required-FPR equations:",
    len(
        required_fpr_rows
    ),
)

print(
    "[PASS] All target-PPV FPR equations verified."
)

print()


# ==============================================================================
# 11. HEADLINE LOW-PREVALENCE VIEW
#
# Descriptive output only.
# No cells are dropped or selected based on these results.
# ==============================================================================

print("=" * 120)
print("HEADLINE LOW-PREVALENCE PROJECTIONS")
print("=" * 120)


for pi in [
    0.001,
    0.0001,
]:

    print()

    print(
        f"Projection prevalence = {pi:.4%}"
    )

    print(
        "-" * 120
    )


    subset = [
        row
        for row in projection_rows
        if row[
            "projection_prevalence"
        ]
        ==
        pi
    ]


    for row in subset:

        print(
            f"{row['cell_id']:<52s} "
            f"{row['operating_point']:<8s} "
            f"TPR={row['tpr']:.6f} "
            f"FPR={row['fpr']:.6f} "
            f"PPV={row['ppv']:.6f} "
            f"NPV={row['npv']:.6f}"
        )


print()


# ==============================================================================
# 12. SANITY TEST SUMMARY
# ==============================================================================

sanity_results = {
    "stage":
        "Stage25-1",

    "status":
        "PASS",

    "tests": {
        "PPV_AT_OBSERVED_PREVALENCE": {
            "expected_checks":
                24,

            "completed_checks":
                len(
                    observed_ppv_tests
                ),

            "maximum_absolute_error":
                max(
                    row[
                        "absolute_error"
                    ]
                    for row in observed_ppv_tests
                ),

            "passed":
                all(
                    row[
                        "passed"
                    ]
                    for row in observed_ppv_tests
                ),
        },

        "PPV_MONOTONICITY": {
            "expected_checks":
                24,

            "completed_checks":
                len(
                    monotonicity_tests
                ),

            "passed":
                all(
                    row[
                        "passed"
                    ]
                    for row in monotonicity_tests
                ),
        },

        "PPV_TARGET_CLIFF_IDENTITY": {
            "expected_checks":
                120,

            "completed_checks":
                len(
                    ppv_cliff_tests
                ),

            "maximum_absolute_error":
                max(
                    row[
                        "absolute_error"
                    ]
                    for row in ppv_cliff_tests
                    if row[
                        "absolute_error"
                    ] is not None
                ),

            "passed":
                all(
                    row[
                        "passed"
                    ]
                    for row in ppv_cliff_tests
                ),
        },

        "PPV50_EXACT_CHECK": {
            "expected_checks":
                24,

            "completed_checks":
                len(
                    ppv50_tests
                ),

            "maximum_absolute_error":
                max(
                    row[
                        "absolute_error"
                    ]
                    for row in ppv50_tests
                    if row[
                        "absolute_error"
                    ] is not None
                ),

            "passed":
                all(
                    row[
                        "passed"
                    ]
                    for row in ppv50_tests
                ),
        },

        "REQUIRED_FPR_IDENTITY": {
            "expected_checks":
                720,

            "completed_checks":
                len(
                    required_fpr_tests
                ),

            "maximum_absolute_error":
                max(
                    row[
                        "absolute_error"
                    ]
                    for row in required_fpr_tests
                    if row[
                        "absolute_error"
                    ] is not None
                ),

            "passed":
                all(
                    row[
                        "passed"
                    ]
                    for row in required_fpr_tests
                ),
        },

        "COMPLETE_PROJECTION_MATRIX": {
            "expected_rows":
                144,

            "actual_rows":
                len(
                    projection_rows
                ),

            "unique_rows":
                len(
                    projection_keys
                ),

            "passed":
                (
                    len(
                        projection_rows
                    )
                    ==
                    144
                    and
                    len(
                        projection_keys
                    )
                    ==
                    144
                ),
        },
    },

    "stage25_0_tests_not_yet_due": [
        "FP_INVARIANCE",
        "COST_BREAK_EVEN_SIGN_REVERSAL",
        "PROJECTED_CONFUSION_IDENTITIES",
    ],

    "reason_not_yet_due":
        (
            "These require traffic-volume and/or cost calculations "
            "scheduled after the Bayesian projection stage."
        ),
}


if not all(
    test[
        "passed"
    ]
    for test in sanity_results[
        "tests"
    ].values()
):

    raise RuntimeError(
        "Stage25-1 sanity test failure."
    )


print("=" * 120)
print("SANITY TESTS")
print("=" * 120)

for name, result in sanity_results[
    "tests"
].items():

    print(
        f"[PASS] {name}"
    )


print()


# ==============================================================================
# 13. CREATE OUTPUT DIRECTORY
# ==============================================================================

OUT_DIR.mkdir(
    parents=True,
    exist_ok=False,
)


# ==============================================================================
# 14. WRITE TABLES
# ==============================================================================

PROJECTION_CSV = (
    OUT_DIR
    / "stage25_1_bayesian_projection_grid.csv"
)

LIKELIHOOD_CSV = (
    OUT_DIR
    / "stage25_1_likelihood_ratios.csv"
)

PPV_CLIFF_CSV = (
    OUT_DIR
    / "stage25_1_ppv_cliffs.csv"
)

REQUIRED_FPR_CSV = (
    OUT_DIR
    / "stage25_1_required_fpr_for_target_ppv.csv"
)

SANITY_JSON = (
    OUT_DIR
    / "stage25_1_sanity_tests.json"
)


write_csv(
    PROJECTION_CSV,
    projection_rows,
)

write_csv(
    LIKELIHOOD_CSV,
    lr_rows,
)

write_csv(
    PPV_CLIFF_CSV,
    ppv_cliff_rows,
)

write_csv(
    REQUIRED_FPR_CSV,
    required_fpr_rows,
)

write_json(
    SANITY_JSON,
    sanity_results,
)


# ==============================================================================
# 15. RESULT SUMMARY
# ==============================================================================

def projection_lookup(
    cell_id,
    operating_point,
    pi,
):

    matches = [
        row
        for row in projection_rows
        if (
            row[
                "cell_id"
            ]
            ==
            cell_id
            and
            row[
                "operating_point"
            ]
            ==
            operating_point
            and
            row[
                "projection_prevalence"
            ]
            ==
            pi
        )
    ]

    if len(
        matches
    ) != 1:

        raise RuntimeError(
            "Projection lookup is not unique."
        )

    return matches[
        0
    ]


headline = {}


for cell_id in sorted(
    {
        row[
            "cell_id"
        ]
        for row in operating_points
    }
):

    headline[
        cell_id
    ] = {}

    for op_name in [
        "STANDARD",
        "BALANCED",
        "SECURITY",
    ]:

        headline[
            cell_id
        ][
            op_name
        ] = {
            "ppv_at_0_1_percent":
                projection_lookup(
                    cell_id,
                    op_name,
                    0.001,
                )[
                    "ppv"
                ],

            "ppv_at_0_01_percent":
                projection_lookup(
                    cell_id,
                    op_name,
                    0.0001,
                )[
                    "ppv"
                ],
        }


result = {
    "stage":
        "Stage25-1",

    "status":
        "BAYESIAN_PREVALENCE_PROJECTION_COMPLETE",

    "created_at_utc":
        datetime.now(
            timezone.utc
        ).isoformat(),

    "repository_parent_commit":
        EXPECTED_PARENT,

    "protocol_freeze_record_sha256":
        EXPECTED_FREEZE_RECORD_SHA,

    "scientific_access": {
        "model_fit_calls":
            0,

        "model_inference_calls":
            0,

        "model_files_loaded":
            0,

        "probability_arrays_opened":
            0,

        "probability_arrays_created":
            0,

        "target_features_read":
            0,

        "target_labels_read":
            0,

        "target_reopenings":
            0,

        "threshold_searches":
            0,
    },

    "analysis": {
        "inherited_cells":
            8,

        "inherited_operating_points":
            24,

        "prevalence_points":
            6,

        "bayesian_projection_rows":
            len(
                projection_rows
            ),

        "likelihood_ratio_rows":
            len(
                lr_rows
            ),

        "ppv_cliff_rows":
            len(
                ppv_cliff_rows
            ),

        "required_fpr_rows":
            len(
                required_fpr_rows
            ),
    },

    "frozen_prevalence_grid":
        prevalence_grid,

    "frozen_ppv_targets":
        ppv_targets,

    "headline_low_prevalence_ppv":
        headline,

    "sanity_test_status":
        "PASS",

    "interpretation_boundary":
        (
            "All Stage25-1 values are deterministic conditional "
            "transformations of frozen TPR/FPR estimates under the "
            "preregistered prior-probability-shift assumption. They are "
            "not empirical production-deployment measurements."
        ),

    "next_authorized_stage":
        "STAGE25_2_TRAFFIC_AND_SOC_CAPACITY_PROJECTION",

    "artifacts": {},
}


# ==============================================================================
# 16. ARTIFACT HASHES
# ==============================================================================

result[
    "artifacts"
] = {
    str(
        PROJECTION_CSV.relative_to(
            REPO
        )
    ):
        sha256_file(
            PROJECTION_CSV
        ),

    str(
        LIKELIHOOD_CSV.relative_to(
            REPO
        )
    ):
        sha256_file(
            LIKELIHOOD_CSV
        ),

    str(
        PPV_CLIFF_CSV.relative_to(
            REPO
        )
    ):
        sha256_file(
            PPV_CLIFF_CSV
        ),

    str(
        REQUIRED_FPR_CSV.relative_to(
            REPO
        )
    ):
        sha256_file(
            REQUIRED_FPR_CSV
        ),

    str(
        SANITY_JSON.relative_to(
            REPO
        )
    ):
        sha256_file(
            SANITY_JSON
        ),
}


RESULT_JSON = (
    OUT_DIR
    / "stage25_1_bayesian_projection_result.json"
)


write_json(
    RESULT_JSON,
    result,
)


result_sha = sha256_file(
    RESULT_JSON
)


RESULT_SHA = (
    OUT_DIR
    / "stage25_1_bayesian_projection_result.sha256"
)


write_text(
    RESULT_SHA,
    (
        f"{result_sha}  "
        f"{RESULT_JSON.name}"
    ),
)


CHECKSUM_FILE = (
    OUT_DIR
    / "checksums.sha256"
)


checksum_paths = [
    PROJECTION_CSV,
    LIKELIHOOD_CSV,
    PPV_CLIFF_CSV,
    REQUIRED_FPR_CSV,
    SANITY_JSON,
    RESULT_JSON,
    RESULT_SHA,
]


write_text(
    CHECKSUM_FILE,
    "\n".join(
        (
            f"{sha256_file(path)}  "
            f"{path.name}"
        )
        for path in checksum_paths
    ),
)


print("=" * 120)
print("STAGE25-1 ARTIFACTS")
print("=" * 120)

for path in (
    checksum_paths
    +
    [
        CHECKSUM_FILE
    ]
):

    print(
        path.relative_to(
            REPO
        )
    )


print()

print(
    "Result SHA:"
)

print(
    " ",
    result_sha
)

print()


# ==============================================================================
# 17. GITHUB TOKEN
# ==============================================================================

github_token = None

token_source = None


try:

    from kaggle_secrets import UserSecretsClient

    client = UserSecretsClient()

    for name in [
        "GITHUB_TOKEN",
        "github_token",
        "GH_TOKEN",
        "GITHUB_PAT",
        "github_pat",
    ]:

        try:

            value = client.get_secret(
                name
            )

            if (
                value
                and
                value.strip()
            ):

                github_token = value.strip()

                token_source = name

                break

        except Exception:

            pass

except Exception:

    pass


if github_token is None:

    for name in [
        "GITHUB_TOKEN",
        "GH_TOKEN",
    ]:

        value = os.environ.get(
            name
        )

        if (
            value
            and
            value.strip()
        ):

            github_token = value.strip()

            token_source = (
                "ENV:"
                +
                name
            )

            break


if github_token is None:

    raise RuntimeError(
        "GitHub token unavailable."
    )


auth_header = base64.b64encode(
    (
        "x-access-token:"
        +
        github_token
    ).encode()
).decode()


# ==============================================================================
# 18. GIT SAFETY
# ==============================================================================

print("=" * 120)
print("GIT SAFETY")
print("=" * 120)


remote_before = git_cmd(
    "ls-remote",
    "origin",
    "refs/heads/main",
    auth_header=auth_header,
).split()[0]


if remote_before != EXPECTED_PARENT:

    raise RuntimeError(
        "\nRemote main moved before Stage25-1 commit.\n"
        f"Expected: {EXPECTED_PARENT}\n"
        f"Actual:   {remote_before}"
    )


tracked_dirty = {
    line
    for line in git_cmd(
        "diff",
        "--name-only",
    ).splitlines()
    if line
}


untracked = {
    line
    for line in git_cmd(
        "ls-files",
        "--others",
        "--exclude-standard",
    ).splitlines()
    if line
}


dirty = (
    tracked_dirty
    |
    untracked
)


allowed_prefix = (
    "results/stage25_prevalence_stress/"
    "stage25_1_bayesian_projection/"
)


unexpected = [
    path
    for path in sorted(
        dirty
    )
    if not path.startswith(
        allowed_prefix
    )
]


if unexpected:

    raise RuntimeError(
        "\nUnexpected repository changes:\n"
        +
        "\n".join(
            unexpected
        )
    )


if not dirty:

    raise RuntimeError(
        "No Stage25-1 changes found."
    )


print(
    "GitHub credential:",
    token_source,
)

print(
    "[PASS] Remote main remains Stage25-0 freeze."
)

print(
    "[PASS] Only Stage25-1 output artifacts are dirty."
)

print()


# ==============================================================================
# 19. GIT AUTHOR
# ==============================================================================

if not git_cmd(
    "config",
    "--local",
    "--get",
    "user.name",
    check=False,
):

    git_cmd(
        "config",
        "--local",
        "user.name",
        git_cmd(
            "log",
            "-1",
            "--format=%an",
        ),
    )


if not git_cmd(
    "config",
    "--local",
    "--get",
    "user.email",
    check=False,
):

    git_cmd(
        "config",
        "--local",
        "user.email",
        git_cmd(
            "log",
            "-1",
            "--format=%ae",
        ),
    )


# ==============================================================================
# 20. STAGE + COMMIT
# ==============================================================================

git_cmd(
    "add",
    "--",
    str(
        OUT_DIR.relative_to(
            REPO
        )
    ),
)


staged = {
    line
    for line in git_cmd(
        "diff",
        "--cached",
        "--name-only",
    ).splitlines()
    if line
}


if not staged:

    raise RuntimeError(
        "No Stage25-1 files staged."
    )


bad_staged = [
    path
    for path in staged
    if not path.startswith(
        allowed_prefix
    )
]


if bad_staged:

    raise RuntimeError(
        "\nUnexpected staged files:\n"
        +
        "\n".join(
            sorted(
                bad_staged
            )
        )
    )


if git_cmd(
    "diff",
    "--name-only",
):

    raise RuntimeError(
        "Unstaged tracked files remain."
    )


if git_cmd(
    "ls-files",
    "--others",
    "--exclude-standard",
):

    raise RuntimeError(
        "Untracked files remain."
    )


print(
    "[PASS] Stage25-1 artifacts staged exclusively."
)

print()


print("=" * 120)
print("COMMIT STAGE25-1")
print("=" * 120)


commit_output = git_cmd(
    "commit",
    "-m",
    "stage25: freeze Bayesian prevalence projections",
)


print(
    commit_output
)

print()


commit = git_cmd(
    "rev-parse",
    "HEAD",
)

parent = git_cmd(
    "rev-parse",
    "HEAD^",
)


if parent != EXPECTED_PARENT:

    raise RuntimeError(
        "\nStage25-1 parent mismatch.\n"
        f"Expected: {EXPECTED_PARENT}\n"
        f"Actual:   {parent}"
    )


# ==============================================================================
# 21. PUSH + VERIFY
# ==============================================================================

print("=" * 120)
print("PUSH + REMOTE VERIFY")
print("=" * 120)


push_output = git_cmd(
    "push",
    "origin",
    "HEAD:main",
    auth_header=auth_header,
)


print(
    push_output
)

print()


remote_after = git_cmd(
    "ls-remote",
    "origin",
    "refs/heads/main",
    auth_header=auth_header,
).split()[0]


if remote_after != commit:

    raise RuntimeError(
        "\nRemote verification failed.\n"
        f"Local:  {commit}\n"
        f"Remote: {remote_after}"
    )


if git_cmd(
    "status",
    "--porcelain",
):

    raise RuntimeError(
        "Repository not clean after Stage25-1 push."
    )


print(
    "[PASS] Stage25-1 pushed."
)

print(
    "[PASS] Repository clean."
)

print()


# ==============================================================================
# 22. FINAL
# ==============================================================================

print("=" * 120)
print("STAGE25-1 BAYESIAN PREVALENCE PROJECTION: PASS")
print("=" * 120)

print()

print(
    "Parent protocol commit:"
)

print(
    " ",
    EXPECTED_PARENT
)

print()

print(
    "Stage25-1 commit:"
)

print(
    " ",
    commit
)

print()

print(
    "Remote main:"
)

print(
    " ",
    remote_after
)

print()

print(
    "Result SHA:"
)

print(
    " ",
    result_sha
)

print()

print(
    "Frozen operating points:       24"
)

print(
    "Prevalence levels:             6"
)

print(
    "Bayesian projection rows:      144"
)

print(
    "PPV cliff equations:           120"
)

print(
    "Required-FPR equations:        720"
)

print()

print(
    "SANITY:"
)

print(
    "  Observed precision recovery: PASS"
)

print(
    "  PPV monotonicity:            PASS"
)

print(
    "  PPV cliff identities:        PASS"
)

print(
    "  PPV50 identities:            PASS"
)

print(
    "  Required-FPR identities:     PASS"
)

print(
    "  Complete 24×6 matrix:        PASS"
)

print()

print(
    "NEW MODEL FITS:                0"
)

print(
    "NEW MODEL INFERENCE:           0"
)

print(
    "NEW PROBABILITY ARRAYS:        0"
)

print(
    "TARGET REOPENINGS:             0"
)

print()

print(
    "NEXT AUTHORIZED:"
)

print(
    "  Stage25-2 — traffic-volume + SOC capacity projection"
)

print()

print(
    "STOP HERE."
)

print("=" * 120)

# %% [Stage25 notebook cell 4]
# ==============================================================================
# STAGE25-2 — TRAFFIC-VOLUME + SOC CAPACITY PROJECTION
#
# Authorized parent:
#   bfcc41741e055356c82f8f2f04042f3c2556b090
#
# Frozen Stage25-1 result SHA:
#   81e4d96494c3432745f97428b722cc8870f75372a2c4570653ec59e7bcaa25ff
#
# PURPOSE
# -------
# Translate the already-frozen Stage25-1 Bayesian projection matrix into:
#
#   - projected attack flows/day
#   - TP/day
#   - FN/day
#   - FP/day
#   - TN/day
#   - total alerts/day
#   - false-alert fraction
#   - false-alert processing hours/day
#   - total alert-processing hours/day
#   - SOC capacity index for 1 / 3 / 10 analyst-day tiers
#   - exact total-alert FPR capacity ceiling
#
# FROZEN SCENARIO
# ---------------
#   benign flows/day          = 1,000,000
#   service time              = 2 min / alert
#   analyst shift             = 480 min/day
#   alerts / analyst-day      = 240
#   capacity tiers            = 1 / 3 / 10 analyst-days
#
# SCIENTIFIC RULES
# ----------------
# NEW MODEL FITS:             0
# NEW MODEL INFERENCE:        0
# NEW PROBABILITY ARRAYS:     0
# TARGET REOPENINGS:          0
# NEW THRESHOLDS:             0
#
# NO COST ANALYSIS IN THIS CELL.
#
# Stage25-2 reads only frozen Stage25-0/1 artifacts.
# ==============================================================================

from __future__ import annotations

import os
import csv
import json
import math
import base64
import hashlib
import subprocess
from pathlib import Path
from datetime import datetime, timezone


print("=" * 120)
print("STAGE25-2 — TRAFFIC-VOLUME + SOC CAPACITY PROJECTION")
print("=" * 120)
print()


# ==============================================================================
# 0. FROZEN ANCHORS
# ==============================================================================

REPO = Path(
    "/kaggle/working/ids2018-validation-safe-ablation"
)

EXPECTED_PARENT = (
    "bfcc41741e055356c82f8f2f04042f3c2556b090"
)

EXPECTED_STAGE25_0_FREEZE_SHA = (
    "d231af1e4f07363c4d932acc99e1052e3b33bd2d24ca22e4386f4c7c378827b7"
)

EXPECTED_STAGE25_1_RESULT_SHA = (
    "81e4d96494c3432745f97428b722cc8870f75372a2c4570653ec59e7bcaa25ff"
)


STAGE25_BASE = (
    REPO
    / "results"
    / "stage25_prevalence_stress"
)


LOCK_DIR = (
    STAGE25_BASE
    / "stage25_0_protocol_lock"
)


STAGE25_1_DIR = (
    STAGE25_BASE
    / "stage25_1_bayesian_projection"
)


OUT_DIR = (
    STAGE25_BASE
    / "stage25_2_traffic_soc_capacity"
)


FREEZE_RECORD = (
    LOCK_DIR
    / "freeze_record.json"
)


TRAFFIC_SPEC = (
    LOCK_DIR
    / "traffic_volume_spec.json"
)


CAPACITY_SPEC = (
    LOCK_DIR
    / "analyst_capacity_spec.json"
)


SANITY_SPEC = (
    LOCK_DIR
    / "sanity_test_plan.json"
)


ANTI_ADAPTATION = (
    LOCK_DIR
    / "anti_adaptation.json"
)


STAGE25_1_RESULT = (
    STAGE25_1_DIR
    / "stage25_1_bayesian_projection_result.json"
)


STAGE25_1_RESULT_SHA = (
    STAGE25_1_DIR
    / "stage25_1_bayesian_projection_result.sha256"
)


STAGE25_1_CHECKSUMS = (
    STAGE25_1_DIR
    / "checksums.sha256"
)


STAGE25_1_GRID = (
    STAGE25_1_DIR
    / "stage25_1_bayesian_projection_grid.csv"
)


# ==============================================================================
# 1. HELPERS
# ==============================================================================

def run_cmd(
    args,
    *,
    cwd=None,
    check=True,
):

    proc = subprocess.run(
        [str(x) for x in args],
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    if check and proc.returncode != 0:

        raise RuntimeError(
            "\nCommand failed:\n"
            + " ".join(str(x) for x in args)
            + "\n\n"
            + (proc.stdout or "")
        )

    return (proc.stdout or "").strip()


def git_cmd(
    *args,
    auth_header=None,
    check=True,
):

    cmd = [
        "git"
    ]

    if auth_header is not None:

        cmd += [
            "-c",
            "credential.helper=",
            "-c",
            f"http.extraHeader=AUTHORIZATION: Basic {auth_header}",
        ]

    cmd += [
        str(x)
        for x in args
    ]

    return run_cmd(
        cmd,
        cwd=REPO,
        check=check,
    )


def sha256_file(
    path,
):

    path = Path(
        path
    )

    h = hashlib.sha256()

    with path.open(
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

    return h.hexdigest()


def load_json(
    path,
):

    path = Path(
        path
    )

    if not path.is_file():

        raise RuntimeError(
            f"Missing JSON:\n{path}"
        )

    return json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )


def write_json(
    path,
    payload,
):

    path = Path(
        path
    )

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    path.write_text(
        json.dumps(
            payload,
            indent=2,
            sort_keys=True,
            ensure_ascii=False,
            allow_nan=False,
        )
        + "\n",
        encoding="utf-8",
    )


def write_text(
    path,
    text,
):

    path = Path(
        path
    )

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    path.write_text(
        str(
            text
        ).rstrip()
        + "\n",
        encoding="utf-8",
    )


def read_csv(
    path,
):

    path = Path(
        path
    )

    if not path.is_file():

        raise RuntimeError(
            f"Missing CSV:\n{path}"
        )

    with path.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as fh:

        return list(
            csv.DictReader(
                fh
            )
        )


def write_csv(
    path,
    rows,
):

    path = Path(
        path
    )

    rows = list(
        rows
    )

    if not rows:

        raise RuntimeError(
            f"Refusing empty CSV:\n{path}"
        )

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    fields = list(
        rows[0].keys()
    )

    with path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as fh:

        writer = csv.DictWriter(
            fh,
            fieldnames=fields,
            lineterminator="\n",
        )

        writer.writeheader()

        for row in rows:

            if list(
                row.keys()
            ) != fields:

                raise RuntimeError(
                    f"Inconsistent CSV schema:\n{path}"
                )

            writer.writerow(
                row
            )


def assert_close(
    actual,
    expected,
    *,
    atol=1e-9,
    label="value",
):

    if not math.isclose(
        float(
            actual
        ),
        float(
            expected
        ),
        rel_tol=0.0,
        abs_tol=atol,
    ):

        raise RuntimeError(
            "\nNumerical identity failure.\n"
            f"{label}\n"
            f"Expected: {expected!r}\n"
            f"Actual:   {actual!r}\n"
            f"Delta:    {float(actual) - float(expected):+.17e}"
        )


def parse_optional_string(
    value,
):

    if value is None:

        return None

    value = str(
        value
    )

    if value == "":

        return None

    return value


# ==============================================================================
# 2. GOVERNANCE GATE
# ==============================================================================

print("=" * 120)
print("GOVERNANCE GATE")
print("=" * 120)


head = git_cmd(
    "rev-parse",
    "HEAD",
)


status = git_cmd(
    "status",
    "--porcelain",
)


print(
    "HEAD:",
    head,
)


if head != EXPECTED_PARENT:

    raise RuntimeError(
        "\nUnexpected Stage25-2 parent.\n"
        f"Expected: {EXPECTED_PARENT}\n"
        f"Actual:   {head}"
    )


if status:

    raise RuntimeError(
        "\nRepository must be clean before Stage25-2:\n"
        + status
    )


if OUT_DIR.exists():

    existing = list(
        OUT_DIR.iterdir()
    )

    if existing:

        raise RuntimeError(
            "\nStage25-2 output directory already contains artifacts:\n"
            + "\n".join(
                str(x)
                for x in existing
            )
        )


freeze_sha = sha256_file(
    FREEZE_RECORD
)


if freeze_sha != EXPECTED_STAGE25_0_FREEZE_SHA:

    raise RuntimeError(
        "\nStage25-0 freeze SHA mismatch.\n"
        f"Expected: {EXPECTED_STAGE25_0_FREEZE_SHA}\n"
        f"Actual:   {freeze_sha}"
    )


stage25_1_sha = sha256_file(
    STAGE25_1_RESULT
)


if stage25_1_sha != EXPECTED_STAGE25_1_RESULT_SHA:

    raise RuntimeError(
        "\nStage25-1 result SHA mismatch.\n"
        f"Expected: {EXPECTED_STAGE25_1_RESULT_SHA}\n"
        f"Actual:   {stage25_1_sha}"
    )


sidecar_sha = (
    STAGE25_1_RESULT_SHA
    .read_text(
        encoding="utf-8"
    )
    .strip()
    .split()[0]
)


if sidecar_sha != EXPECTED_STAGE25_1_RESULT_SHA:

    raise RuntimeError(
        "Stage25-1 result sidecar changed."
    )


stage25_1_result = load_json(
    STAGE25_1_RESULT
)


if (
    stage25_1_result[
        "status"
    ]
    !=
    "BAYESIAN_PREVALENCE_PROJECTION_COMPLETE"
):

    raise RuntimeError(
        "Stage25-1 result status changed."
    )


if (
    stage25_1_result[
        "next_authorized_stage"
    ]
    !=
    "STAGE25_2_TRAFFIC_AND_SOC_CAPACITY_PROJECTION"
):

    raise RuntimeError(
        "Stage25-2 is not the authorized next action."
    )


for key in [
    "model_fit_calls",
    "model_inference_calls",
    "probability_arrays_opened",
    "probability_arrays_created",
    "target_features_read",
    "target_labels_read",
    "target_reopenings",
    "threshold_searches",
]:

    if (
        int(
            stage25_1_result[
                "scientific_access"
            ][
                key
            ]
        )
        !=
        0
    ):

        raise RuntimeError(
            f"Unexpected Stage25-1 scientific access counter: {key}"
        )


print(
    "Stage25-0 freeze SHA:",
    freeze_sha,
)

print(
    "Stage25-1 result SHA:",
    stage25_1_sha,
)

print()

print(
    "[PASS] Stage25-2 authorized."
)

print(
    "[PASS] No model/inference/reopening activity inherited."
)

print()


# ==============================================================================
# 3. VERIFY COMPLETE STAGE25-1 CHECKSUM CHAIN
# ==============================================================================

print("=" * 120)
print("STAGE25-1 CHECKSUM VERIFICATION")
print("=" * 120)


checksum_lines = [
    line.strip()
    for line in STAGE25_1_CHECKSUMS.read_text(
        encoding="utf-8"
    ).splitlines()
    if line.strip()
]


verified = 0


for line in checksum_lines:

    expected_sha, filename = line.split(
        None,
        1,
    )

    filename = filename.strip()

    artifact = (
        STAGE25_1_DIR
        / filename
    )

    actual_sha = sha256_file(
        artifact
    )


    if actual_sha != expected_sha:

        raise RuntimeError(
            "\nStage25-1 checksum mismatch.\n"
            f"Artifact: {filename}\n"
            f"Expected: {expected_sha}\n"
            f"Actual:   {actual_sha}"
        )


    verified += 1


for relative_path, expected_sha in stage25_1_result[
    "artifacts"
].items():

    artifact = (
        REPO
        / relative_path
    )

    actual_sha = sha256_file(
        artifact
    )


    if actual_sha != expected_sha:

        raise RuntimeError(
            "\nStage25-1 result-declared artifact mismatch.\n"
            f"Artifact: {relative_path}"
        )


print(
    "Checksum entries verified:",
    verified,
)

print(
    "[PASS] Complete Stage25-1 artifact chain verified."
)

print()


# ==============================================================================
# 4. LOAD FROZEN TRAFFIC / CAPACITY SPECIFICATION
# ==============================================================================

traffic_spec = load_json(
    TRAFFIC_SPEC
)

capacity_spec = load_json(
    CAPACITY_SPEC
)

sanity_spec = load_json(
    SANITY_SPEC
)

anti_adaptation = load_json(
    ANTI_ADAPTATION
)


B = int(
    traffic_spec[
        "benign_flows_per_day"
    ]
)


SERVICE_MINUTES = int(
    capacity_spec[
        "minutes_per_alert"
    ]
)


SHIFT_MINUTES = int(
    capacity_spec[
        "analyst_shift_minutes"
    ]
)


ALERTS_PER_ANALYST_DAY = int(
    capacity_spec[
        "alerts_per_analyst_day"
    ]
)


if B != 1_000_000:

    raise RuntimeError(
        "Frozen benign-flow volume changed."
    )


if SERVICE_MINUTES != 2:

    raise RuntimeError(
        "Frozen alert service time changed."
    )


if SHIFT_MINUTES != 480:

    raise RuntimeError(
        "Frozen analyst shift changed."
    )


if ALERTS_PER_ANALYST_DAY != 240:

    raise RuntimeError(
        "Frozen analyst alert capacity changed."
    )


TIERS = [
    1,
    3,
    10,
]


for k in TIERS:

    tier = capacity_spec[
        "tiers"
    ][
        str(
            k
        )
    ]

    expected_alert_capacity = (
        ALERTS_PER_ANALYST_DAY
        *
        k
    )


    if int(
        tier[
            "alert_capacity_per_day"
        ]
    ) != expected_alert_capacity:

        raise RuntimeError(
            f"Capacity tier {k} changed."
        )


    expected_fpr_capacity = (
        expected_alert_capacity
        /
        B
    )


    assert_close(
        tier[
            "false_positive_only_fpr_capacity"
        ],
        expected_fpr_capacity,
        atol=1e-15,
        label=f"FP-only FPR tier {k}",
    )


print(
    "Benign flows/day:       ",
    f"{B:,}",
)

print(
    "Minutes / alert:         ",
    SERVICE_MINUTES,
)

print(
    "Alerts / analyst-day:    ",
    ALERTS_PER_ANALYST_DAY,
)

print(
    "Analyst-day tiers:       ",
    TIERS,
)

print()


# ==============================================================================
# 5. LOAD AND VALIDATE 144-ROW STAGE25-1 GRID
# ==============================================================================

stage25_1_rows_raw = read_csv(
    STAGE25_1_GRID
)


if len(
    stage25_1_rows_raw
) != 144:

    raise RuntimeError(
        "\nStage25-1 projection row count changed.\n"
        f"Expected: 144\n"
        f"Actual:   {len(stage25_1_rows_raw)}"
    )


projection_rows = []


for raw in stage25_1_rows_raw:

    row = {
        "cell_id":
            raw[
                "cell_id"
            ],

        "source_stage":
            raw[
                "source_stage"
            ],

        "family":
            raw[
                "family"
            ],

        "direction":
            raw[
                "direction"
            ],

        "bridge":
            raw[
                "bridge"
            ],

        "variant":
            raw[
                "variant"
            ],

        "identity_duplicate_of":
            parse_optional_string(
                raw[
                    "identity_duplicate_of"
                ]
            ),

        "operating_point":
            raw[
                "operating_point"
            ],

        "threshold":
            float(
                raw[
                    "threshold"
                ]
            ),

        "tpr":
            float(
                raw[
                    "tpr"
                ]
            ),

        "fpr":
            float(
                raw[
                    "fpr"
                ]
            ),

        "frozen_f1":
            (
                None
                if raw[
                    "frozen_f1"
                ]
                ==
                ""
                else float(
                    raw[
                        "frozen_f1"
                    ]
                )
            ),

        "frozen_precision":
            float(
                raw[
                    "frozen_precision"
                ]
            ),

        "observed_prevalence":
            float(
                raw[
                    "observed_prevalence"
                ]
            ),

        "prevalence_index":
            int(
                raw[
                    "prevalence_index"
                ]
            ),

        "projection_prevalence":
            float(
                raw[
                    "projection_prevalence"
                ]
            ),

        "ppv":
            float(
                raw[
                    "ppv"
                ]
            ),

        "npv":
            float(
                raw[
                    "npv"
                ]
            ),
    }


    projection_rows.append(
        row
    )


unique_projection_keys = {
    (
        row[
            "cell_id"
        ],
        row[
            "operating_point"
        ],
        row[
            "projection_prevalence"
        ],
    )
    for row in projection_rows
}


if len(
    unique_projection_keys
) != 144:

    raise RuntimeError(
        "Stage25-1 projection keys are not unique."
    )


print(
    "[PASS] Exact 144-row Bayesian grid loaded."
)

print()


# ==============================================================================
# 6. TRAFFIC-VOLUME + SOC PROJECTION
# ==============================================================================

wide_rows = []

capacity_long_rows = []


for row in projection_rows:

    pi = row[
        "projection_prevalence"
    ]

    tpr = row[
        "tpr"
    ]

    fpr = row[
        "fpr"
    ]


    if not (
        0.0
        <
        pi
        <
        1.0
    ):

        raise RuntimeError(
            f"Invalid prevalence: {pi}"
        )


    attack_flows = (
        pi
        *
        B
        /
        (
            1.0
            -
            pi
        )
    )


    total_flows = (
        B
        +
        attack_flows
    )


    tp = (
        tpr
        *
        attack_flows
    )


    fn = (
        (
            1.0
            -
            tpr
        )
        *
        attack_flows
    )


    fp = (
        fpr
        *
        B
    )


    tn = (
        (
            1.0
            -
            fpr
        )
        *
        B
    )


    alerts = (
        tp
        +
        fp
    )


    false_alert_fraction = (
        None
        if alerts == 0.0
        else
        fp
        /
        alerts
    )


    false_alert_hours = (
        fp
        *
        SERVICE_MINUTES
        /
        60.0
    )


    true_alert_hours = (
        tp
        *
        SERVICE_MINUTES
        /
        60.0
    )


    total_alert_hours = (
        alerts
        *
        SERVICE_MINUTES
        /
        60.0
    )


    analyst_days_required = (
        alerts
        /
        ALERTS_PER_ANALYST_DAY
    )


    # --------------------------------------------------------------------------
    # Cross-check Stage25-1 Bayesian PPV / NPV using projected confusion counts.
    # --------------------------------------------------------------------------

    count_ppv = (
        None
        if (
            tp
            +
            fp
        )
        ==
        0.0
        else
        tp
        /
        (
            tp
            +
            fp
        )
    )


    count_npv = (
        None
        if (
            tn
            +
            fn
        )
        ==
        0.0
        else
        tn
        /
        (
            tn
            +
            fn
        )
    )


    assert_close(
        count_ppv,
        row[
            "ppv"
        ],
        atol=5e-13,
        label=(
            row[
                "cell_id"
            ]
            +
            "/"
            +
            row[
                "operating_point"
            ]
            +
            f"/pi={pi}/PPV"
        ),
    )


    assert_close(
        count_npv,
        row[
            "npv"
        ],
        atol=5e-13,
        label=(
            row[
                "cell_id"
            ]
            +
            "/"
            +
            row[
                "operating_point"
            ]
            +
            f"/pi={pi}/NPV"
        ),
    )


    # --------------------------------------------------------------------------
    # Core confusion identities.
    # --------------------------------------------------------------------------

    assert_close(
        tp
        +
        fn,
        attack_flows,
        atol=1e-7,
        label="TP+FN attack identity",
    )


    assert_close(
        fp
        +
        tn,
        B,
        atol=1e-7,
        label="FP+TN benign identity",
    )


    assert_close(
        attack_flows
        +
        B,
        total_flows,
        atol=1e-7,
        label="total flow identity",
    )


    wide = {
        "cell_id":
            row[
                "cell_id"
            ],

        "source_stage":
            row[
                "source_stage"
            ],

        "family":
            row[
                "family"
            ],

        "direction":
            row[
                "direction"
            ],

        "bridge":
            row[
                "bridge"
            ],

        "variant":
            row[
                "variant"
            ],

        "identity_duplicate_of":
            row[
                "identity_duplicate_of"
            ],

        "operating_point":
            row[
                "operating_point"
            ],

        "threshold":
            row[
                "threshold"
            ],

        "tpr":
            tpr,

        "fpr":
            fpr,

        "frozen_f1":
            row[
                "frozen_f1"
            ],

        "frozen_precision":
            row[
                "frozen_precision"
            ],

        "observed_prevalence":
            row[
                "observed_prevalence"
            ],

        "projection_prevalence":
            pi,

        "stage25_1_ppv":
            row[
                "ppv"
            ],

        "stage25_1_npv":
            row[
                "npv"
            ],

        "benign_flows_per_day":
            B,

        "projected_attack_flows_per_day":
            attack_flows,

        "projected_total_flows_per_day":
            total_flows,

        "tp_per_day":
            tp,

        "fn_per_day":
            fn,

        "fp_per_day":
            fp,

        "tn_per_day":
            tn,

        "total_alerts_per_day":
            alerts,

        "false_alert_fraction":
            false_alert_fraction,

        "true_alert_processing_hours_per_day":
            true_alert_hours,

        "false_alert_processing_hours_per_day":
            false_alert_hours,

        "total_alert_processing_hours_per_day":
            total_alert_hours,

        "analyst_days_required":
            analyst_days_required,
    }


    for k in TIERS:

        capacity_alerts = (
            ALERTS_PER_ANALYST_DAY
            *
            k
        )


        capacity_hours = (
            SHIFT_MINUTES
            *
            k
            /
            60.0
        )


        aci = (
            alerts
            /
            capacity_alerts
        )


        fp_only_aci = (
            fp
            /
            capacity_alerts
        )


        capacity_exceeded = (
            alerts
            >
            capacity_alerts
        )


        fp_only_capacity_exceeded = (
            fp
            >
            capacity_alerts
        )


        alert_headroom = (
            capacity_alerts
            -
            alerts
        )


        hour_headroom = (
            capacity_hours
            -
            total_alert_hours
        )


        # Frozen exact formula:
        #
        # FPR <= 240*k/B - TPR*pi/(1-pi)
        #
        exact_fpr_ceiling = (
            capacity_alerts
            /
            B
            -
            tpr
            *
            pi
            /
            (
                1.0
                -
                pi
            )
        )


        feasible_even_at_fpr_zero = (
            exact_fpr_ceiling
            >=
            0.0
        )


        actual_fpr_meets_total_capacity = (
            feasible_even_at_fpr_zero
            and
            fpr
            <=
            exact_fpr_ceiling
        )


        fp_only_fpr_ceiling = (
            capacity_alerts
            /
            B
        )


        actual_fpr_meets_fp_only_capacity = (
            fpr
            <=
            fp_only_fpr_ceiling
        )


        # ACI equivalence:
        # alerts/(240*k) == processing_hours/(8*k)
        assert_close(
            aci,
            total_alert_hours
            /
            capacity_hours,
            atol=1e-13,
            label=(
                f"ACI identity k={k}"
            ),
        )


        if (
            actual_fpr_meets_total_capacity
            !=
            (
                alerts
                <=
                capacity_alerts
            )
        ):

            raise RuntimeError(
                "\nExact total-capacity FPR inequality disagrees "
                "with direct alert-volume calculation.\n"
                f"Cell: {row['cell_id']}\n"
                f"OP: {row['operating_point']}\n"
                f"pi: {pi}\n"
                f"k: {k}"
            )


        wide[
            f"capacity_{k}_analyst_alerts_per_day"
        ] = capacity_alerts


        wide[
            f"capacity_{k}_analyst_hours_per_day"
        ] = capacity_hours


        wide[
            f"aci_{k}"
        ] = aci


        wide[
            f"fp_only_aci_{k}"
        ] = fp_only_aci


        wide[
            f"capacity_exceeded_{k}"
        ] = capacity_exceeded


        wide[
            f"fp_only_capacity_exceeded_{k}"
        ] = fp_only_capacity_exceeded


        wide[
            f"alert_headroom_{k}"
        ] = alert_headroom


        wide[
            f"hour_headroom_{k}"
        ] = hour_headroom


        wide[
            f"exact_total_alert_fpr_ceiling_{k}"
        ] = exact_fpr_ceiling


        wide[
            f"feasible_even_at_fpr_zero_{k}"
        ] = feasible_even_at_fpr_zero


        wide[
            f"actual_fpr_meets_total_capacity_{k}"
        ] = actual_fpr_meets_total_capacity


        wide[
            f"fp_only_fpr_ceiling_{k}"
        ] = fp_only_fpr_ceiling


        wide[
            f"actual_fpr_meets_fp_only_capacity_{k}"
        ] = actual_fpr_meets_fp_only_capacity


        capacity_long_rows.append(
            {
                "cell_id":
                    row[
                        "cell_id"
                    ],

                "family":
                    row[
                        "family"
                    ],

                "direction":
                    row[
                        "direction"
                    ],

                "bridge":
                    row[
                        "bridge"
                    ],

                "variant":
                    row[
                        "variant"
                    ],

                "operating_point":
                    row[
                        "operating_point"
                    ],

                "threshold":
                    row[
                        "threshold"
                    ],

                "projection_prevalence":
                    pi,

                "tpr":
                    tpr,

                "fpr":
                    fpr,

                "tp_per_day":
                    tp,

                "fp_per_day":
                    fp,

                "total_alerts_per_day":
                    alerts,

                "total_alert_processing_hours_per_day":
                    total_alert_hours,

                "analyst_tier":
                    k,

                "alert_capacity_per_day":
                    capacity_alerts,

                "capacity_hours_per_day":
                    capacity_hours,

                "aci":
                    aci,

                "fp_only_aci":
                    fp_only_aci,

                "capacity_exceeded":
                    capacity_exceeded,

                "fp_only_capacity_exceeded":
                    fp_only_capacity_exceeded,

                "alert_headroom":
                    alert_headroom,

                "hour_headroom":
                    hour_headroom,

                "exact_total_alert_fpr_ceiling":
                    exact_fpr_ceiling,

                "feasible_even_at_fpr_zero":
                    feasible_even_at_fpr_zero,

                "actual_fpr_meets_total_capacity":
                    actual_fpr_meets_total_capacity,

                "fp_only_fpr_ceiling":
                    fp_only_fpr_ceiling,

                "actual_fpr_meets_fp_only_capacity":
                    actual_fpr_meets_fp_only_capacity,
            }
        )


    wide_rows.append(
        wide
    )


if len(
    wide_rows
) != 144:

    raise RuntimeError(
        "Stage25-2 wide projection must contain 144 rows."
    )


if len(
    capacity_long_rows
) != (
    144
    *
    3
):

    raise RuntimeError(
        "Stage25-2 capacity-long table must contain 432 rows."
    )


print("=" * 120)
print("TRAFFIC + CAPACITY PROJECTION")
print("=" * 120)

print(
    "Traffic projection rows:",
    len(
        wide_rows
    ),
)

print(
    "Capacity-tier rows:     ",
    len(
        capacity_long_rows
    ),
)

print()

print(
    "[PASS] 144 traffic projections complete."
)

print(
    "[PASS] 432 tier-specific SOC capacity projections complete."
)

print()


# ==============================================================================
# 7. FP INVARIANCE SANITY TEST
# ==============================================================================

fp_invariance_tests = []


op_keys = sorted(
    {
        (
            row[
                "cell_id"
            ],
            row[
                "operating_point"
            ],
        )
        for row in wide_rows
    }
)


if len(
    op_keys
) != 24:

    raise RuntimeError(
        "Expected 24 unique operating points."
    )


for cell_id, op_name in op_keys:

    rows = [
        row
        for row in wide_rows
        if (
            row[
                "cell_id"
            ]
            ==
            cell_id
            and
            row[
                "operating_point"
            ]
            ==
            op_name
        )
    ]


    if len(
        rows
    ) != 6:

        raise RuntimeError(
            "Each operating point must have six prevalence rows."
        )


    fp_values = [
        row[
            "fp_per_day"
        ]
        for row in rows
    ]


    fp_range = (
        max(
            fp_values
        )
        -
        min(
            fp_values
        )
    )


    if fp_range > 1e-12:

        raise RuntimeError(
            "\nFP invariance failure.\n"
            f"{cell_id} / {op_name}\n"
            f"Range: {fp_range}"
        )


    fp_invariance_tests.append(
        {
            "cell_id":
                cell_id,

            "operating_point":
                op_name,

            "fp_per_day":
                fp_values[
                    0
                ],

            "max_minus_min":
                fp_range,

            "passed":
                True,
        }
    )


print(
    "[PASS] FP/day invariance verified across prevalence for all 24 operating points."
)

print()


# ==============================================================================
# 8. FIXED-FPR FALSE-ALERT WORKLOAD TABLE
# ==============================================================================

fp_workload_rows = []


for cell_id, op_name in op_keys:

    source_rows = [
        row
        for row in wide_rows
        if (
            row[
                "cell_id"
            ]
            ==
            cell_id
            and
            row[
                "operating_point"
            ]
            ==
            op_name
        )
    ]


    first = source_rows[
        0
    ]


    fp_per_day = first[
        "fp_per_day"
    ]


    false_alert_hours = first[
        "false_alert_processing_hours_per_day"
    ]


    fp_workload_rows.append(
        {
            "cell_id":
                cell_id,

            "family":
                first[
                    "family"
                ],

            "direction":
                first[
                    "direction"
                ],

            "bridge":
                first[
                    "bridge"
                ],

            "variant":
                first[
                    "variant"
                ],

            "operating_point":
                op_name,

            "threshold":
                first[
                    "threshold"
                ],

            "fpr":
                first[
                    "fpr"
                ],

            "fp_per_day":
                fp_per_day,

            "false_alert_processing_hours_per_day":
                false_alert_hours,

            "false_alert_analyst_days_per_day":
                fp_per_day
                /
                ALERTS_PER_ANALYST_DAY,

            "fp_only_exceeds_1_analyst":
                fp_per_day
                >
                240,

            "fp_only_exceeds_3_analysts":
                fp_per_day
                >
                720,

            "fp_only_exceeds_10_analysts":
                fp_per_day
                >
                2400,
        }
    )


if len(
    fp_workload_rows
) != 24:

    raise RuntimeError(
        "FP workload table must contain 24 rows."
    )


# ==============================================================================
# 9. SANITY SUMMARY
# ==============================================================================

ppv_identity_checks = 144

npv_identity_checks = 144

confusion_identity_checks = (
    144
    *
    3
)

aci_identity_checks = (
    144
    *
    3
)

capacity_equivalence_checks = (
    144
    *
    3
)


sanity_results = {
    "stage":
        "Stage25-2",

    "status":
        "PASS",

    "tests": {
        "FP_INVARIANCE": {
            "expected_checks":
                24,

            "completed_checks":
                len(
                    fp_invariance_tests
                ),

            "maximum_fp_range":
                max(
                    row[
                        "max_minus_min"
                    ]
                    for row in fp_invariance_tests
                ),

            "passed":
                all(
                    row[
                        "passed"
                    ]
                    for row in fp_invariance_tests
                ),
        },

        "PROJECTED_CONFUSION_IDENTITIES": {
            "projection_rows":
                144,

            "identities_per_row": [
                "TP+FN=A",
                "FP+TN=B",
                "A+B=N_total",
            ],

            "completed_checks":
                confusion_identity_checks,

            "passed":
                True,
        },

        "STAGE25_1_PPV_IDENTITY": {
            "expected_checks":
                144,

            "completed_checks":
                ppv_identity_checks,

            "passed":
                True,
        },

        "STAGE25_1_NPV_IDENTITY": {
            "expected_checks":
                144,

            "completed_checks":
                npv_identity_checks,

            "passed":
                True,
        },

        "ACI_HOURS_IDENTITY": {
            "expected_checks":
                432,

            "completed_checks":
                aci_identity_checks,

            "identity":
                (
                    "alerts/(240*k) == "
                    "processing_hours/(8*k)"
                ),

            "passed":
                True,
        },

        "TOTAL_CAPACITY_FPR_INEQUALITY_IDENTITY": {
            "expected_checks":
                432,

            "completed_checks":
                capacity_equivalence_checks,

            "identity":
                (
                    "direct alerts<=capacity agrees with "
                    "FPR <= 240*k/B - TPR*pi/(1-pi)"
                ),

            "passed":
                True,
        },

        "COMPLETE_TRAFFIC_MATRIX": {
            "expected_rows":
                144,

            "actual_rows":
                len(
                    wide_rows
                ),

            "passed":
                len(
                    wide_rows
                )
                ==
                144,
        },

        "COMPLETE_CAPACITY_MATRIX": {
            "expected_rows":
                432,

            "actual_rows":
                len(
                    capacity_long_rows
                ),

            "passed":
                len(
                    capacity_long_rows
                )
                ==
                432,
        },
    },

    "stage25_0_test_not_yet_due": {
        "COST_BREAK_EVEN_SIGN_REVERSAL":
            (
                "Deferred to Stage25-3 relative-cost analysis."
            ),
    },
}


if not all(
    result[
        "passed"
    ]
    for result in sanity_results[
        "tests"
    ].values()
):

    raise RuntimeError(
        "Stage25-2 sanity failure."
    )


print("=" * 120)
print("SANITY TESTS")
print("=" * 120)


for name in sanity_results[
    "tests"
]:

    print(
        "[PASS]",
        name,
    )


print()


# ==============================================================================
# 10. CAPACITY SUMMARY COUNTS
# ==============================================================================

capacity_summary = {}


for k in TIERS:

    capacity_summary[
        str(
            k
        )
    ] = {}


    for pi in [
        0.10,
        0.03,
        0.01,
        0.003,
        0.001,
        0.0001,
    ]:

        rows = [
            row
            for row in capacity_long_rows
            if (
                row[
                    "analyst_tier"
                ]
                ==
                k
                and
                row[
                    "projection_prevalence"
                ]
                ==
                pi
            )
        ]


        if len(
            rows
        ) != 24:

            raise RuntimeError(
                "Capacity summary cell must contain 24 operating points."
            )


        capacity_summary[
            str(
                k
            )
        ][
            str(
                pi
            )
        ] = {
            "operating_points":
                24,

            "capacity_exceeded_count":
                sum(
                    bool(
                        row[
                            "capacity_exceeded"
                        ]
                    )
                    for row in rows
                ),

            "capacity_feasible_count":
                sum(
                    not bool(
                        row[
                            "capacity_exceeded"
                        ]
                    )
                    for row in rows
                ),

            "fp_only_capacity_exceeded_count":
                sum(
                    bool(
                        row[
                            "fp_only_capacity_exceeded"
                        ]
                    )
                    for row in rows
                ),

            "infeasible_even_at_fpr_zero_count":
                sum(
                    not bool(
                        row[
                            "feasible_even_at_fpr_zero"
                        ]
                    )
                    for row in rows
                ),
        }


# ==============================================================================
# 11. HEADLINE LOW-PREVALENCE VIEW
# ==============================================================================

print("=" * 120)
print("HEADLINE SOC PROJECTIONS")
print("=" * 120)


for pi in [
    0.001,
    0.0001,
]:

    print()

    print(
        f"Projection prevalence = {pi:.4%}"
    )

    print(
        "-" * 120
    )


    rows = [
        row
        for row in wide_rows
        if row[
            "projection_prevalence"
        ]
        ==
        pi
    ]


    for row in rows:

        print(
            f"{row['cell_id']:<52s} "
            f"{row['operating_point']:<8s} "
            f"FP/day={row['fp_per_day']:>10.2f} "
            f"TP/day={row['tp_per_day']:>10.2f} "
            f"alerts={row['total_alerts_per_day']:>10.2f} "
            f"hours={row['total_alert_processing_hours_per_day']:>9.2f} "
            f"ACI1={row['aci_1']:>8.3f} "
            f"ACI3={row['aci_3']:>8.3f} "
            f"ACI10={row['aci_10']:>8.3f}"
        )


print()


# ==============================================================================
# 12. CREATE OUTPUT DIRECTORY
# ==============================================================================

OUT_DIR.mkdir(
    parents=True,
    exist_ok=False,
)


TRAFFIC_CSV = (
    OUT_DIR
    / "stage25_2_traffic_soc_projection.csv"
)


CAPACITY_CSV = (
    OUT_DIR
    / "stage25_2_capacity_tiers.csv"
)


FP_WORKLOAD_CSV = (
    OUT_DIR
    / "stage25_2_fixed_fpr_false_alert_workload.csv"
)


SANITY_JSON = (
    OUT_DIR
    / "stage25_2_sanity_tests.json"
)


CAPACITY_SUMMARY_JSON = (
    OUT_DIR
    / "stage25_2_capacity_summary.json"
)


write_csv(
    TRAFFIC_CSV,
    wide_rows,
)


write_csv(
    CAPACITY_CSV,
    capacity_long_rows,
)


write_csv(
    FP_WORKLOAD_CSV,
    fp_workload_rows,
)


write_json(
    SANITY_JSON,
    sanity_results,
)


write_json(
    CAPACITY_SUMMARY_JSON,
    {
        "stage":
            "Stage25-2",

        "capacity_summary":
            capacity_summary,

        "note":
            (
                "Counts summarize the 24 frozen operating points separately "
                "at each frozen prevalence and analyst tier."
            ),
    },
)


# ==============================================================================
# 13. RESULT JSON
# ==============================================================================

result_payload = {
    "stage":
        "Stage25-2",

    "status":
        "TRAFFIC_AND_SOC_CAPACITY_PROJECTION_COMPLETE",

    "created_at_utc":
        datetime.now(
            timezone.utc
        ).isoformat(),

    "repository_parent_commit":
        EXPECTED_PARENT,

    "stage25_0_freeze_sha256":
        EXPECTED_STAGE25_0_FREEZE_SHA,

    "stage25_1_result_sha256":
        EXPECTED_STAGE25_1_RESULT_SHA,

    "scientific_access": {
        "model_fit_calls":
            0,

        "model_inference_calls":
            0,

        "model_files_loaded":
            0,

        "probability_arrays_opened":
            0,

        "probability_arrays_created":
            0,

        "target_features_read":
            0,

        "target_labels_read":
            0,

        "target_reopenings":
            0,

        "threshold_searches":
            0,
    },

    "frozen_scenario": {
        "benign_flows_per_day":
            B,

        "minutes_per_alert":
            SERVICE_MINUTES,

        "analyst_shift_minutes":
            SHIFT_MINUTES,

        "alerts_per_analyst_day":
            ALERTS_PER_ANALYST_DAY,

        "analyst_tiers":
            TIERS,
    },

    "analysis": {
        "traffic_projection_rows":
            len(
                wide_rows
            ),

        "capacity_tier_rows":
            len(
                capacity_long_rows
            ),

        "fixed_fpr_workload_rows":
            len(
                fp_workload_rows
            ),

        "operating_points":
            24,

        "prevalence_points":
            6,
    },

    "capacity_summary":
        capacity_summary,

    "sanity_test_status":
        "PASS",

    "interpretation_boundary":
        (
            "SOC workload values are deterministic scenario projections "
            "conditional on frozen TPR/FPR, fixed 1,000,000 benign flows/day, "
            "2 minutes per alert, and the preregistered analyst-capacity tiers. "
            "They are not measured production SOC workloads."
        ),

    "next_authorized_stage":
        "STAGE25_3_RELATIVE_COST_AND_BREAK_EVEN_ANALYSIS",

    "artifacts":
        {},
}


result_payload[
    "artifacts"
] = {
    str(
        TRAFFIC_CSV.relative_to(
            REPO
        )
    ):
        sha256_file(
            TRAFFIC_CSV
        ),

    str(
        CAPACITY_CSV.relative_to(
            REPO
        )
    ):
        sha256_file(
            CAPACITY_CSV
        ),

    str(
        FP_WORKLOAD_CSV.relative_to(
            REPO
        )
    ):
        sha256_file(
            FP_WORKLOAD_CSV
        ),

    str(
        SANITY_JSON.relative_to(
            REPO
        )
    ):
        sha256_file(
            SANITY_JSON
        ),

    str(
        CAPACITY_SUMMARY_JSON.relative_to(
            REPO
        )
    ):
        sha256_file(
            CAPACITY_SUMMARY_JSON
        ),
}


RESULT_JSON = (
    OUT_DIR
    / "stage25_2_traffic_soc_capacity_result.json"
)


write_json(
    RESULT_JSON,
    result_payload,
)


result_sha = sha256_file(
    RESULT_JSON
)


RESULT_SHA = (
    OUT_DIR
    / "stage25_2_traffic_soc_capacity_result.sha256"
)


write_text(
    RESULT_SHA,
    (
        f"{result_sha}  "
        f"{RESULT_JSON.name}"
    ),
)


CHECKSUMS_OUT = (
    OUT_DIR
    / "checksums.sha256"
)


checksum_artifacts = [
    TRAFFIC_CSV,
    CAPACITY_CSV,
    FP_WORKLOAD_CSV,
    SANITY_JSON,
    CAPACITY_SUMMARY_JSON,
    RESULT_JSON,
    RESULT_SHA,
]


write_text(
    CHECKSUMS_OUT,
    "\n".join(
        (
            f"{sha256_file(path)}  "
            f"{path.name}"
        )
        for path in checksum_artifacts
    ),
)


print("=" * 120)
print("STAGE25-2 ARTIFACTS")
print("=" * 120)


for path in (
    checksum_artifacts
    +
    [
        CHECKSUMS_OUT
    ]
):

    print(
        path.relative_to(
            REPO
        )
    )


print()

print(
    "Result SHA:"
)

print(
    " ",
    result_sha
)

print()


# ==============================================================================
# 14. GITHUB CREDENTIAL
# ==============================================================================

github_token = None

token_source = None


try:

    from kaggle_secrets import UserSecretsClient

    client = UserSecretsClient()


    for name in [
        "GITHUB_TOKEN",
        "github_token",
        "GH_TOKEN",
        "GITHUB_PAT",
        "github_pat",
    ]:

        try:

            value = client.get_secret(
                name
            )

            if (
                value
                and
                value.strip()
            ):

                github_token = value.strip()

                token_source = name

                break

        except Exception:

            pass

except Exception:

    pass


if github_token is None:

    for name in [
        "GITHUB_TOKEN",
        "GH_TOKEN",
    ]:

        value = os.environ.get(
            name
        )

        if (
            value
            and
            value.strip()
        ):

            github_token = value.strip()

            token_source = (
                "ENV:"
                +
                name
            )

            break


if github_token is None:

    raise RuntimeError(
        "GitHub token unavailable."
    )


auth_header = base64.b64encode(
    (
        "x-access-token:"
        +
        github_token
    ).encode()
).decode()


# ==============================================================================
# 15. GIT SAFETY
# ==============================================================================

print("=" * 120)
print("GIT SAFETY")
print("=" * 120)


remote_before = git_cmd(
    "ls-remote",
    "origin",
    "refs/heads/main",
    auth_header=auth_header,
).split()[0]


if remote_before != EXPECTED_PARENT:

    raise RuntimeError(
        "\nRemote main moved before Stage25-2 commit.\n"
        f"Expected: {EXPECTED_PARENT}\n"
        f"Actual:   {remote_before}"
    )


tracked_dirty = {
    line
    for line in git_cmd(
        "diff",
        "--name-only",
    ).splitlines()
    if line
}


untracked = {
    line
    for line in git_cmd(
        "ls-files",
        "--others",
        "--exclude-standard",
    ).splitlines()
    if line
}


dirty = (
    tracked_dirty
    |
    untracked
)


allowed_prefix = (
    "results/stage25_prevalence_stress/"
    "stage25_2_traffic_soc_capacity/"
)


unexpected = [
    path
    for path in sorted(
        dirty
    )
    if not path.startswith(
        allowed_prefix
    )
]


if unexpected:

    raise RuntimeError(
        "\nUnexpected repository changes:\n"
        +
        "\n".join(
            unexpected
        )
    )


if not dirty:

    raise RuntimeError(
        "No Stage25-2 artifacts found."
    )


print(
    "GitHub credential:",
    token_source,
)

print(
    "[PASS] Remote main remains Stage25-1 commit."
)

print(
    "[PASS] Only Stage25-2 artifacts are dirty."
)

print()


# ==============================================================================
# 16. GIT AUTHOR
# ==============================================================================

if not git_cmd(
    "config",
    "--local",
    "--get",
    "user.name",
    check=False,
):

    git_cmd(
        "config",
        "--local",
        "user.name",
        git_cmd(
            "log",
            "-1",
            "--format=%an",
        ),
    )


if not git_cmd(
    "config",
    "--local",
    "--get",
    "user.email",
    check=False,
):

    git_cmd(
        "config",
        "--local",
        "user.email",
        git_cmd(
            "log",
            "-1",
            "--format=%ae",
        ),
    )


# ==============================================================================
# 17. STAGE + COMMIT
# ==============================================================================

git_cmd(
    "add",
    "--",
    str(
        OUT_DIR.relative_to(
            REPO
        )
    ),
)


staged = {
    line
    for line in git_cmd(
        "diff",
        "--cached",
        "--name-only",
    ).splitlines()
    if line
}


if not staged:

    raise RuntimeError(
        "No Stage25-2 files staged."
    )


bad_staged = [
    path
    for path in staged
    if not path.startswith(
        allowed_prefix
    )
]


if bad_staged:

    raise RuntimeError(
        "\nUnexpected staged files:\n"
        +
        "\n".join(
            sorted(
                bad_staged
            )
        )
    )


if git_cmd(
    "diff",
    "--name-only",
):

    raise RuntimeError(
        "Unstaged tracked files remain."
    )


if git_cmd(
    "ls-files",
    "--others",
    "--exclude-standard",
):

    raise RuntimeError(
        "Untracked files remain."
    )


print(
    "[PASS] Stage25-2 artifacts staged exclusively."
)

print()


print("=" * 120)
print("COMMIT STAGE25-2")
print("=" * 120)


commit_output = git_cmd(
    "commit",
    "-m",
    "stage25: freeze traffic and SOC capacity projections",
)


print(
    commit_output
)

print()


commit = git_cmd(
    "rev-parse",
    "HEAD",
)


parent = git_cmd(
    "rev-parse",
    "HEAD^",
)


if parent != EXPECTED_PARENT:

    raise RuntimeError(
        "\nStage25-2 parent mismatch.\n"
        f"Expected: {EXPECTED_PARENT}\n"
        f"Actual:   {parent}"
    )


# ==============================================================================
# 18. PUSH + VERIFY
# ==============================================================================

print("=" * 120)
print("PUSH + REMOTE VERIFY")
print("=" * 120)


push_output = git_cmd(
    "push",
    "origin",
    "HEAD:main",
    auth_header=auth_header,
)


print(
    push_output
)

print()


remote_after = git_cmd(
    "ls-remote",
    "origin",
    "refs/heads/main",
    auth_header=auth_header,
).split()[0]


if remote_after != commit:

    raise RuntimeError(
        "\nRemote verification failed.\n"
        f"Local:  {commit}\n"
        f"Remote: {remote_after}"
    )


if git_cmd(
    "status",
    "--porcelain",
):

    raise RuntimeError(
        "Repository not clean after Stage25-2 push."
    )


print(
    "[PASS] Stage25-2 pushed."
)

print(
    "[PASS] Repository clean."
)

print()


# ==============================================================================
# 19. FINAL
# ==============================================================================

print("=" * 120)
print("STAGE25-2 TRAFFIC + SOC CAPACITY PROJECTION: PASS")
print("=" * 120)

print()

print(
    "Parent Stage25-1 commit:"
)

print(
    " ",
    EXPECTED_PARENT
)

print()

print(
    "Stage25-2 commit:"
)

print(
    " ",
    commit
)

print()

print(
    "Remote main:"
)

print(
    " ",
    remote_after
)

print()

print(
    "Result SHA:"
)

print(
    " ",
    result_sha
)

print()

print(
    "Traffic projection rows:       144"
)

print(
    "Capacity-tier rows:            432"
)

print(
    "Fixed-FPR workload rows:       24"
)

print()

print(
    "SANITY:"
)

print(
    "  FP invariance:                PASS"
)

print(
    "  Projected confusion identity: PASS"
)

print(
    "  Stage25-1 PPV identity:       PASS"
)

print(
    "  Stage25-1 NPV identity:       PASS"
)

print(
    "  ACI/hour identity:            PASS"
)

print(
    "  Exact capacity inequality:    PASS"
)

print(
    "  Complete traffic matrix:      PASS"
)

print(
    "  Complete capacity matrix:     PASS"
)

print()

print(
    "NEW MODEL FITS:                0"
)

print(
    "NEW MODEL INFERENCE:           0"
)

print(
    "NEW PROBABILITY ARRAYS:        0"
)

print(
    "TARGET REOPENINGS:             0"
)

print()

print(
    "NEXT AUTHORIZED:"
)

print(
    "  Stage25-3 — relative cost + analytic break-even analysis"
)

print()

print(
    "STOP HERE."
)

print("=" * 120)

# %% [Stage25 notebook cell 5]
# ==============================================================================
# STAGE25-3 — EXACT BREAK-EVEN ANALYSIS
#
# Authorized parent:
#   e905a490aa6b7fdd3c22b021b11de270c9b57784
#
# Frozen Stage25-2 result SHA:
#   1e3e66eb1dcf416585fd3f0fada8675b6950fde5f3f45af006a25b1aec872737
#
# PURPOSE
# -------
# Complete the preregistered exact analytic break-even layer:
#
#   1. cost projection on all 144 frozen prevalence rows
#   2. exact analytic cost break-even prevalence for all 24 operating points
#   3. verify model-vs-ignore inequality immediately below/above break-even
#   4. preserve Stage25-1 exact PPV break-even table
#   5. preserve Stage25-1 exact required-FPR table
#
# Frozen relative cost:
#
#   C_FP = 1
#   C_FN = 100
#
# Units:
#   RELATIVE OPERATIONAL COST UNITS
#   NOT dollars
#
# Exact model cost:
#
#   C_model = FP*C_FP + FN*C_FN
#
# Exact simplified ignore/non-deployment cost:
#
#   C_ignore = A*C_FN
#
# Exact cost break-even prevalence:
#
#                    C_FP * FPR
#   pi*_cost = ---------------------------
#               C_FN*TPR + C_FP*FPR
#
# ABSOLUTE SCIENTIFIC RULES
# -------------------------
# NEW MODEL FITS:             0
# NEW MODEL INFERENCE:        0
# NEW PROBABILITY ARRAYS:     0
# TARGET REOPENINGS:          0
# NEW THRESHOLDS:             0
#
# This cell does NOT generate Stage25 figures yet.
# Stage25-4 does benchmark -> operational translation next.
# ==============================================================================

from __future__ import annotations

import os
import csv
import json
import math
import base64
import shutil
import hashlib
import subprocess
from pathlib import Path
from datetime import datetime, timezone


print("=" * 120)
print("STAGE25-3 — EXACT BREAK-EVEN ANALYSIS")
print("=" * 120)
print()


# ==============================================================================
# 0. FROZEN ANCHORS
# ==============================================================================

REPO = Path(
    "/kaggle/working/ids2018-validation-safe-ablation"
)

EXPECTED_PARENT = (
    "e905a490aa6b7fdd3c22b021b11de270c9b57784"
)

EXPECTED_STAGE25_0_FREEZE_SHA = (
    "d231af1e4f07363c4d932acc99e1052e3b33bd2d24ca22e4386f4c7c378827b7"
)

EXPECTED_STAGE25_1_RESULT_SHA = (
    "81e4d96494c3432745f97428b722cc8870f75372a2c4570653ec59e7bcaa25ff"
)

EXPECTED_STAGE25_2_RESULT_SHA = (
    "1e3e66eb1dcf416585fd3f0fada8675b6950fde5f3f45af006a25b1aec872737"
)


STAGE25_BASE = (
    REPO
    / "results"
    / "stage25_prevalence_stress"
)


LOCK_DIR = (
    STAGE25_BASE
    / "stage25_0_protocol_lock"
)


STAGE25_1_DIR = (
    STAGE25_BASE
    / "stage25_1_bayesian_projection"
)


STAGE25_2_DIR = (
    STAGE25_BASE
    / "stage25_2_traffic_soc_capacity"
)


OUT_DIR = (
    STAGE25_BASE
    / "stage25_3_break_even_analysis"
)


FREEZE_RECORD = (
    LOCK_DIR
    / "freeze_record.json"
)


COST_SPEC = (
    LOCK_DIR
    / "cost_model.json"
)


NUMERICAL_SPEC = (
    LOCK_DIR
    / "numerical_policy.json"
)


SANITY_SPEC = (
    LOCK_DIR
    / "sanity_test_plan.json"
)


ANTI_ADAPTATION = (
    LOCK_DIR
    / "anti_adaptation.json"
)


STAGE25_1_RESULT = (
    STAGE25_1_DIR
    / "stage25_1_bayesian_projection_result.json"
)


STAGE25_1_PPV_CLIFF = (
    STAGE25_1_DIR
    / "stage25_1_ppv_cliffs.csv"
)


STAGE25_1_REQUIRED_FPR = (
    STAGE25_1_DIR
    / "stage25_1_required_fpr_for_target_ppv.csv"
)


STAGE25_2_RESULT = (
    STAGE25_2_DIR
    / "stage25_2_traffic_soc_capacity_result.json"
)


STAGE25_2_RESULT_SHA = (
    STAGE25_2_DIR
    / "stage25_2_traffic_soc_capacity_result.sha256"
)


STAGE25_2_CHECKSUMS = (
    STAGE25_2_DIR
    / "checksums.sha256"
)


STAGE25_2_TRAFFIC = (
    STAGE25_2_DIR
    / "stage25_2_traffic_soc_projection.csv"
)


# ==============================================================================
# 1. HELPERS
# ==============================================================================

def run_cmd(
    args,
    *,
    cwd=None,
    check=True,
):

    p = subprocess.run(
        [str(x) for x in args],
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    if check and p.returncode != 0:

        raise RuntimeError(
            "\nCommand failed:\n"
            +
            " ".join(
                str(x)
                for x in args
            )
            +
            "\n\n"
            +
            (
                p.stdout
                or
                ""
            )
        )

    return (
        p.stdout
        or
        ""
    ).strip()


def git_cmd(
    *args,
    auth_header=None,
    check=True,
):

    cmd = [
        "git"
    ]

    if auth_header is not None:

        cmd += [
            "-c",
            "credential.helper=",
            "-c",
            f"http.extraHeader=AUTHORIZATION: Basic {auth_header}",
        ]

    cmd += [
        str(x)
        for x in args
    ]

    return run_cmd(
        cmd,
        cwd=REPO,
        check=check,
    )


def sha256_file(
    path,
):

    path = Path(
        path
    )

    h = hashlib.sha256()

    with path.open(
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

    return h.hexdigest()


def load_json(
    path,
):

    path = Path(
        path
    )

    if not path.is_file():

        raise RuntimeError(
            f"Missing JSON:\n{path}"
        )

    return json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )


def write_json(
    path,
    payload,
):

    path = Path(
        path
    )

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    path.write_text(
        json.dumps(
            payload,
            indent=2,
            sort_keys=True,
            ensure_ascii=False,
            allow_nan=False,
        )
        +
        "\n",
        encoding="utf-8",
    )


def write_text(
    path,
    text,
):

    path = Path(
        path
    )

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    path.write_text(
        str(
            text
        ).rstrip()
        +
        "\n",
        encoding="utf-8",
    )


def read_csv(
    path,
):

    path = Path(
        path
    )

    if not path.is_file():

        raise RuntimeError(
            f"Missing CSV:\n{path}"
        )

    with path.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as fh:

        return list(
            csv.DictReader(
                fh
            )
        )


def write_csv(
    path,
    rows,
):

    path = Path(
        path
    )

    rows = list(
        rows
    )

    if not rows:

        raise RuntimeError(
            f"Refusing to write empty CSV:\n{path}"
        )

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    fields = list(
        rows[
            0
        ].keys()
    )

    with path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as fh:

        writer = csv.DictWriter(
            fh,
            fieldnames=fields,
            lineterminator="\n",
        )

        writer.writeheader()

        for row in rows:

            if list(
                row.keys()
            ) != fields:

                raise RuntimeError(
                    f"Inconsistent CSV schema:\n{path}"
                )

            writer.writerow(
                row
            )


def assert_close(
    actual,
    expected,
    *,
    atol=1e-9,
    label="value",
):

    if not math.isclose(
        float(
            actual
        ),
        float(
            expected
        ),
        rel_tol=0.0,
        abs_tol=atol,
    ):

        raise RuntimeError(
            "\nNumerical identity failure.\n"
            f"{label}\n"
            f"Expected: {expected!r}\n"
            f"Actual:   {actual!r}\n"
            f"Delta:    "
            f"{float(actual) - float(expected):+.17e}"
        )


def parse_optional(
    value,
):

    if value is None:

        return None

    value = str(
        value
    )

    if value == "":

        return None

    return value


def model_cost_from_counts(
    fp,
    fn,
    c_fp,
    c_fn,
):

    return (
        fp
        *
        c_fp
        +
        fn
        *
        c_fn
    )


def ignore_cost_from_attack(
    attack,
    c_fn,
):

    return (
        attack
        *
        c_fn
    )


def analytic_cost_break_even(
    tpr,
    fpr,
    c_fp,
    c_fn,
):

    numerator = (
        c_fp
        *
        fpr
    )

    denominator = (
        c_fn
        *
        tpr
        +
        c_fp
        *
        fpr
    )


    if denominator == 0.0:

        return (
            None,
            "UNDEFINED_ZERO_DENOMINATOR",
        )


    value = (
        numerator
        /
        denominator
    )


    if value == 0.0:

        return (
            0.0,
            "BOUNDARY_ZERO",
        )


    if value == 1.0:

        return (
            1.0,
            "BOUNDARY_ONE",
        )


    if not (
        0.0
        <
        value
        <
        1.0
    ):

        raise RuntimeError(
            f"Invalid cost break-even prevalence: {value}"
        )


    return (
        value,
        "INTERIOR_FINITE",
    )


def analytic_cost_delta_per_benign_flow(
    pi,
    tpr,
    fpr,
    c_fp,
    c_fn,
):

    # ----------------------------------------------------------
    # (C_model - C_ignore) / B
    #
    # = C_FP*FPR - C_FN*TPR*pi/(1-pi)
    # ----------------------------------------------------------

    if not (
        0.0
        <=
        pi
        <
        1.0
    ):

        raise RuntimeError(
            f"Invalid prevalence: {pi}"
        )


    return (
        c_fp
        *
        fpr
        -
        c_fn
        *
        tpr
        *
        pi
        /
        (
            1.0
            -
            pi
        )
    )


# ==============================================================================
# 2. GOVERNANCE GATE
# ==============================================================================

print("=" * 120)
print("GOVERNANCE GATE")
print("=" * 120)


head = git_cmd(
    "rev-parse",
    "HEAD",
)


status = git_cmd(
    "status",
    "--porcelain",
)


print(
    "HEAD:",
    head,
)


if head != EXPECTED_PARENT:

    raise RuntimeError(
        "\nUnexpected Stage25-3 parent.\n"
        f"Expected: {EXPECTED_PARENT}\n"
        f"Actual:   {head}"
    )


if status:

    raise RuntimeError(
        "\nRepository must be clean before Stage25-3:\n"
        +
        status
    )


if OUT_DIR.exists():

    existing = list(
        OUT_DIR.iterdir()
    )

    if existing:

        raise RuntimeError(
            "\nStage25-3 output directory already contains artifacts:\n"
            +
            "\n".join(
                str(
                    x
                )
                for x in existing
            )
        )


freeze_sha = sha256_file(
    FREEZE_RECORD
)


if freeze_sha != EXPECTED_STAGE25_0_FREEZE_SHA:

    raise RuntimeError(
        "Stage25-0 freeze SHA changed."
    )


stage25_1_sha = sha256_file(
    STAGE25_1_RESULT
)


if stage25_1_sha != EXPECTED_STAGE25_1_RESULT_SHA:

    raise RuntimeError(
        "Stage25-1 result SHA changed."
    )


stage25_2_sha = sha256_file(
    STAGE25_2_RESULT
)


if stage25_2_sha != EXPECTED_STAGE25_2_RESULT_SHA:

    raise RuntimeError(
        "\nStage25-2 result SHA changed.\n"
        f"Expected: {EXPECTED_STAGE25_2_RESULT_SHA}\n"
        f"Actual:   {stage25_2_sha}"
    )


stage25_2_sidecar = (
    STAGE25_2_RESULT_SHA
    .read_text(
        encoding="utf-8"
    )
    .strip()
    .split()[0]
)


if stage25_2_sidecar != EXPECTED_STAGE25_2_RESULT_SHA:

    raise RuntimeError(
        "Stage25-2 SHA sidecar changed."
    )


stage25_2_result = load_json(
    STAGE25_2_RESULT
)


if (
    stage25_2_result[
        "status"
    ]
    !=
    "TRAFFIC_AND_SOC_CAPACITY_PROJECTION_COMPLETE"
):

    raise RuntimeError(
        "Stage25-2 status changed."
    )


if (
    stage25_2_result[
        "next_authorized_stage"
    ]
    !=
    "STAGE25_3_RELATIVE_COST_AND_BREAK_EVEN_ANALYSIS"
):

    raise RuntimeError(
        "Stage25-3 is not the authorized next stage."
    )


for key, value in stage25_2_result[
    "scientific_access"
].items():

    if int(
        value
    ) != 0:

        raise RuntimeError(
            f"Unexpected scientific access counter: {key}={value}"
        )


print(
    "Stage25-0 freeze SHA:",
    freeze_sha,
)

print(
    "Stage25-1 result SHA:",
    stage25_1_sha,
)

print(
    "Stage25-2 result SHA:",
    stage25_2_sha,
)

print()

print(
    "[PASS] Stage25-3 authorized."
)

print(
    "[PASS] No fit/inference/reopening activity inherited."
)

print()


# ==============================================================================
# 3. VERIFY STAGE25-2 CHECKSUM CHAIN
# ==============================================================================

print("=" * 120)
print("STAGE25-2 CHECKSUM VERIFICATION")
print("=" * 120)


checksum_lines = [
    line.strip()
    for line in STAGE25_2_CHECKSUMS.read_text(
        encoding="utf-8"
    ).splitlines()
    if line.strip()
]


verified_count = 0


for line in checksum_lines:

    expected_sha, filename = line.split(
        None,
        1,
    )

    artifact = (
        STAGE25_2_DIR
        /
        filename.strip()
    )

    actual_sha = sha256_file(
        artifact
    )


    if actual_sha != expected_sha:

        raise RuntimeError(
            "\nStage25-2 checksum mismatch.\n"
            f"Artifact: {artifact.name}\n"
            f"Expected: {expected_sha}\n"
            f"Actual:   {actual_sha}"
        )


    verified_count += 1


for relative_path, expected_sha in stage25_2_result[
    "artifacts"
].items():

    artifact = (
        REPO
        /
        relative_path
    )

    actual_sha = sha256_file(
        artifact
    )


    if actual_sha != expected_sha:

        raise RuntimeError(
            "\nStage25-2 result artifact mismatch:\n"
            f"{relative_path}"
        )


print(
    "Checksum entries verified:",
    verified_count,
)

print(
    "[PASS] Stage25-2 artifact chain exact."
)

print()


# ==============================================================================
# 4. VERIFY STAGE25-1 EXACT BREAK-EVEN INPUT TABLES
# ==============================================================================

print("=" * 120)
print("STAGE25-1 ANALYTIC TABLE VERIFICATION")
print("=" * 120)


stage25_1_result = load_json(
    STAGE25_1_RESULT
)


ppv_cliff_relative = str(
    STAGE25_1_PPV_CLIFF.relative_to(
        REPO
    )
)


required_fpr_relative = str(
    STAGE25_1_REQUIRED_FPR.relative_to(
        REPO
    )
)


expected_ppv_cliff_sha = (
    stage25_1_result[
        "artifacts"
    ][
        ppv_cliff_relative
    ]
)


expected_required_fpr_sha = (
    stage25_1_result[
        "artifacts"
    ][
        required_fpr_relative
    ]
)


actual_ppv_cliff_sha = sha256_file(
    STAGE25_1_PPV_CLIFF
)


actual_required_fpr_sha = sha256_file(
    STAGE25_1_REQUIRED_FPR
)


if actual_ppv_cliff_sha != expected_ppv_cliff_sha:

    raise RuntimeError(
        "Stage25-1 PPV cliff table changed."
    )


if actual_required_fpr_sha != expected_required_fpr_sha:

    raise RuntimeError(
        "Stage25-1 required-FPR table changed."
    )


ppv_cliff_rows = read_csv(
    STAGE25_1_PPV_CLIFF
)


required_fpr_rows = read_csv(
    STAGE25_1_REQUIRED_FPR
)


if len(
    ppv_cliff_rows
) != 120:

    raise RuntimeError(
        "Stage25-1 PPV cliff table must contain 120 rows."
    )


if len(
    required_fpr_rows
) != 720:

    raise RuntimeError(
        "Stage25-1 required-FPR table must contain 720 rows."
    )


print(
    "PPV break-even rows: ",
    len(
        ppv_cliff_rows
    ),
)

print(
    "Required-FPR rows:   ",
    len(
        required_fpr_rows
    ),
)

print()

print(
    "[PASS] Existing exact PPV break-even analyses verified."
)

print()


# ==============================================================================
# 5. LOAD FROZEN COST MODEL
# ==============================================================================

cost_spec = load_json(
    COST_SPEC
)


numerical_spec = load_json(
    NUMERICAL_SPEC
)


sanity_spec = load_json(
    SANITY_SPEC
)


anti_adaptation = load_json(
    ANTI_ADAPTATION
)


C_FP = int(
    cost_spec[
        "C_FP"
    ]
)


C_FN = int(
    cost_spec[
        "C_FN"
    ]
)


if C_FP != 1:

    raise RuntimeError(
        "Frozen C_FP changed."
    )


if C_FN != 100:

    raise RuntimeError(
        "Frozen C_FN changed."
    )


if cost_spec[
    "currency"
] is not False:

    raise RuntimeError(
        "Relative cost was incorrectly relabeled as currency."
    )


if (
    cost_spec[
        "units"
    ]
    !=
    "RELATIVE_OPERATIONAL_COST_UNITS"
):

    raise RuntimeError(
        "Frozen cost-unit semantics changed."
    )


if (
    numerical_spec[
        "calculation_dtype"
    ]
    !=
    "IEEE754_FLOAT64"
):

    raise RuntimeError(
        "Numerical policy changed."
    )


print(
    "C_FP:",
    C_FP,
)

print(
    "C_FN:",
    C_FN,
)

print(
    "Ratio:",
    f"{C_FP}:{C_FN}",
)

print(
    "Units:",
    cost_spec[
        "units"
    ],
)

print()

print(
    "[PASS] Relative-cost assumptions exact."
)

print()


# ==============================================================================
# 6. LOAD EXACT STAGE25-2 TRAFFIC MATRIX
# ==============================================================================

traffic_raw = read_csv(
    STAGE25_2_TRAFFIC
)


if len(
    traffic_raw
) != 144:

    raise RuntimeError(
        "\nStage25-2 traffic matrix changed.\n"
        f"Expected: 144\n"
        f"Actual:   {len(traffic_raw)}"
    )


traffic_rows = []


for raw in traffic_raw:

    traffic_rows.append(
        {
            "cell_id":
                raw[
                    "cell_id"
                ],

            "source_stage":
                raw[
                    "source_stage"
                ],

            "family":
                raw[
                    "family"
                ],

            "direction":
                raw[
                    "direction"
                ],

            "bridge":
                raw[
                    "bridge"
                ],

            "variant":
                raw[
                    "variant"
                ],

            "identity_duplicate_of":
                parse_optional(
                    raw[
                        "identity_duplicate_of"
                    ]
                ),

            "operating_point":
                raw[
                    "operating_point"
                ],

            "threshold":
                float(
                    raw[
                        "threshold"
                    ]
                ),

            "tpr":
                float(
                    raw[
                        "tpr"
                    ]
                ),

            "fpr":
                float(
                    raw[
                        "fpr"
                    ]
                ),

            "frozen_f1":
                (
                    None
                    if raw[
                        "frozen_f1"
                    ]
                    ==
                    ""
                    else
                    float(
                        raw[
                            "frozen_f1"
                        ]
                    )
                ),

            "frozen_precision":
                float(
                    raw[
                        "frozen_precision"
                    ]
                ),

            "observed_prevalence":
                float(
                    raw[
                        "observed_prevalence"
                    ]
                ),

            "projection_prevalence":
                float(
                    raw[
                        "projection_prevalence"
                    ]
                ),

            "benign_flows_per_day":
                float(
                    raw[
                        "benign_flows_per_day"
                    ]
                ),

            "attack_flows_per_day":
                float(
                    raw[
                        "projected_attack_flows_per_day"
                    ]
                ),

            "total_flows_per_day":
                float(
                    raw[
                        "projected_total_flows_per_day"
                    ]
                ),

            "tp_per_day":
                float(
                    raw[
                        "tp_per_day"
                    ]
                ),

            "fn_per_day":
                float(
                    raw[
                        "fn_per_day"
                    ]
                ),

            "fp_per_day":
                float(
                    raw[
                        "fp_per_day"
                    ]
                ),

            "tn_per_day":
                float(
                    raw[
                        "tn_per_day"
                    ]
                ),

            "alerts_per_day":
                float(
                    raw[
                        "total_alerts_per_day"
                    ]
                ),

            "alert_hours_per_day":
                float(
                    raw[
                        "total_alert_processing_hours_per_day"
                    ]
                ),
        }
    )


traffic_keys = {
    (
        row[
            "cell_id"
        ],
        row[
            "operating_point"
        ],
        row[
            "projection_prevalence"
        ],
    )
    for row in traffic_rows
}


if len(
    traffic_keys
) != 144:

    raise RuntimeError(
        "Traffic matrix keys are not unique."
    )


print(
    "[PASS] Exact 144-row Stage25-2 traffic matrix loaded."
)

print()


# ==============================================================================
# 7. 144-ROW RELATIVE COST PROJECTION
# ==============================================================================

cost_projection_rows = []


for row in traffic_rows:

    model_cost = model_cost_from_counts(
        row[
            "fp_per_day"
        ],
        row[
            "fn_per_day"
        ],
        C_FP,
        C_FN,
    )


    ignore_cost = ignore_cost_from_attack(
        row[
            "attack_flows_per_day"
        ],
        C_FN,
    )


    cost_delta = (
        model_cost
        -
        ignore_cost
    )


    # ----------------------------------------------------------
    # Equivalent identity:
    #
    # C_model - C_ignore
    #   = FP*C_FP - TP*C_FN
    # ----------------------------------------------------------

    identity_delta = (
        row[
            "fp_per_day"
        ]
        *
        C_FP
        -
        row[
            "tp_per_day"
        ]
        *
        C_FN
    )


    assert_close(
        cost_delta,
        identity_delta,
        atol=1e-7,
        label=(
            row[
                "cell_id"
            ]
            +
            "/"
            +
            row[
                "operating_point"
            ]
            +
            "/cost-delta identity"
        ),
    )


    if ignore_cost == 0.0:

        cost_ratio = None

        relative_savings = None

    else:

        cost_ratio = (
            model_cost
            /
            ignore_cost
        )

        relative_savings = (
            ignore_cost
            -
            model_cost
        ) / ignore_cost


    tolerance = (
        1e-10
        *
        max(
            1.0,
            abs(
                model_cost
            ),
            abs(
                ignore_cost
            ),
        )
    )


    if abs(
        cost_delta
    ) <= tolerance:

        preferred = (
            "EQUAL_WITHIN_NUMERICAL_TOLERANCE"
        )

    elif cost_delta < 0.0:

        preferred = (
            "MODEL_LOWER_RELATIVE_COST"
        )

    else:

        preferred = (
            "IGNORE_LOWER_RELATIVE_COST"
        )


    cost_projection_rows.append(
        {
            "cell_id":
                row[
                    "cell_id"
                ],

            "source_stage":
                row[
                    "source_stage"
                ],

            "family":
                row[
                    "family"
                ],

            "direction":
                row[
                    "direction"
                ],

            "bridge":
                row[
                    "bridge"
                ],

            "variant":
                row[
                    "variant"
                ],

            "identity_duplicate_of":
                row[
                    "identity_duplicate_of"
                ],

            "operating_point":
                row[
                    "operating_point"
                ],

            "threshold":
                row[
                    "threshold"
                ],

            "tpr":
                row[
                    "tpr"
                ],

            "fpr":
                row[
                    "fpr"
                ],

            "observed_prevalence":
                row[
                    "observed_prevalence"
                ],

            "projection_prevalence":
                row[
                    "projection_prevalence"
                ],

            "benign_flows_per_day":
                row[
                    "benign_flows_per_day"
                ],

            "attack_flows_per_day":
                row[
                    "attack_flows_per_day"
                ],

            "tp_per_day":
                row[
                    "tp_per_day"
                ],

            "fn_per_day":
                row[
                    "fn_per_day"
                ],

            "fp_per_day":
                row[
                    "fp_per_day"
                ],

            "C_FP":
                C_FP,

            "C_FN":
                C_FN,

            "model_relative_cost":
                model_cost,

            "ignore_relative_cost":
                ignore_cost,

            "model_minus_ignore":
                cost_delta,

            "model_to_ignore_cost_ratio":
                cost_ratio,

            "relative_savings_vs_ignore":
                relative_savings,

            "preferred_under_frozen_cost_model":
                preferred,
        }
    )


if len(
    cost_projection_rows
) != 144:

    raise RuntimeError(
        "Cost projection must contain 144 rows."
    )


print("=" * 120)
print("RELATIVE COST GRID")
print("=" * 120)

print(
    "Rows:",
    len(
        cost_projection_rows
    ),
)

print(
    "[PASS] Relative-cost projection complete."
)

print()


# ==============================================================================
# 8. UNIQUE OPERATING POINT INVENTORY
# ==============================================================================

op_lookup = {}


for row in traffic_rows:

    key = (
        row[
            "cell_id"
        ],
        row[
            "operating_point"
        ],
    )


    candidate = {
        "cell_id":
            row[
                "cell_id"
            ],

        "source_stage":
            row[
                "source_stage"
            ],

        "family":
            row[
                "family"
            ],

        "direction":
            row[
                "direction"
            ],

        "bridge":
            row[
                "bridge"
            ],

        "variant":
            row[
                "variant"
            ],

        "identity_duplicate_of":
            row[
                "identity_duplicate_of"
            ],

        "operating_point":
            row[
                "operating_point"
            ],

        "threshold":
            row[
                "threshold"
            ],

        "tpr":
            row[
                "tpr"
            ],

        "fpr":
            row[
                "fpr"
            ],

        "observed_prevalence":
            row[
                "observed_prevalence"
            ],

        "benign_flows_per_day":
            row[
                "benign_flows_per_day"
            ],
    }


    if key in op_lookup:

        existing = op_lookup[
            key
        ]


        for field in [
            "threshold",
            "tpr",
            "fpr",
            "observed_prevalence",
            "benign_flows_per_day",
        ]:

            assert_close(
                candidate[
                    field
                ],
                existing[
                    field
                ],
                atol=1e-15,
                label=(
                    f"{key}/{field}"
                ),
            )

    else:

        op_lookup[
            key
        ] = candidate


if len(
    op_lookup
) != 24:

    raise RuntimeError(
        "\nExpected 24 operating points.\n"
        f"Actual: {len(op_lookup)}"
    )


# ==============================================================================
# 9. EXACT ANALYTIC COST BREAK-EVEN
# ==============================================================================

break_even_rows = []

sign_reversal_tests = []

RELATIVE_NEIGHBOR_EPS = 1e-6


for key in sorted(
    op_lookup
):

    op = op_lookup[
        key
    ]


    tpr = op[
        "tpr"
    ]

    fpr = op[
        "fpr"
    ]


    pi_star, status_star = analytic_cost_break_even(
        tpr,
        fpr,
        C_FP,
        C_FN,
    )


    if status_star != "INTERIOR_FINITE":

        raise RuntimeError(
            "\nCurrent inherited operating point produced a boundary/"
            "undefined cost break-even unexpectedly.\n"
            f"{op['cell_id']} / {op['operating_point']}\n"
            f"status={status_star}\n"
            f"pi*={pi_star}"
        )


    # ----------------------------------------------------------
    # Exact algebraic equality check.
    # ----------------------------------------------------------

    delta_per_B_at_star = (
        analytic_cost_delta_per_benign_flow(
            pi_star,
            tpr,
            fpr,
            C_FP,
            C_FN,
        )
    )


    if abs(
        delta_per_B_at_star
    ) > 5e-15:

        raise RuntimeError(
            "\nAnalytic cost break-even equality failed.\n"
            f"{op['cell_id']} / {op['operating_point']}\n"
            f"delta/B={delta_per_B_at_star}"
        )


    # ----------------------------------------------------------
    # Evaluate immediately below/above.
    #
    # Frozen sanity-test meaning:
    #   below pi*  -> FP cost dominates -> Ignore lower cost
    #   above pi*  -> avoided TP miss-cost dominates -> Model lower cost
    # ----------------------------------------------------------

    pi_below = (
        pi_star
        *
        (
            1.0
            -
            RELATIVE_NEIGHBOR_EPS
        )
    )


    pi_above = (
        pi_star
        *
        (
            1.0
            +
            RELATIVE_NEIGHBOR_EPS
        )
    )


    if pi_below <= 0.0:

        pi_below = math.nextafter(
            pi_star,
            0.0,
        )


    if pi_above >= 1.0:

        pi_above = math.nextafter(
            pi_star,
            1.0,
        )


    delta_below = (
        analytic_cost_delta_per_benign_flow(
            pi_below,
            tpr,
            fpr,
            C_FP,
            C_FN,
        )
    )


    delta_above = (
        analytic_cost_delta_per_benign_flow(
            pi_above,
            tpr,
            fpr,
            C_FP,
            C_FN,
        )
    )


    if not (
        delta_below
        >
        0.0
    ):

        raise RuntimeError(
            "\nCost sign reversal failed BELOW break-even.\n"
            f"{op['cell_id']} / {op['operating_point']}\n"
            f"pi*={pi_star}\n"
            f"below={pi_below}\n"
            f"delta/B={delta_below}"
        )


    if not (
        delta_above
        <
        0.0
    ):

        raise RuntimeError(
            "\nCost sign reversal failed ABOVE break-even.\n"
            f"{op['cell_id']} / {op['operating_point']}\n"
            f"pi*={pi_star}\n"
            f"above={pi_above}\n"
            f"delta/B={delta_above}"
        )


    # ----------------------------------------------------------
    # Count-form verification at pi* using the frozen B.
    # ----------------------------------------------------------

    B = op[
        "benign_flows_per_day"
    ]


    attack_star = (
        pi_star
        *
        B
        /
        (
            1.0
            -
            pi_star
        )
    )


    tp_star = (
        tpr
        *
        attack_star
    )


    fn_star = (
        (
            1.0
            -
            tpr
        )
        *
        attack_star
    )


    fp_star = (
        fpr
        *
        B
    )


    model_star = model_cost_from_counts(
        fp_star,
        fn_star,
        C_FP,
        C_FN,
    )


    ignore_star = ignore_cost_from_attack(
        attack_star,
        C_FN,
    )


    assert_close(
        model_star,
        ignore_star,
        atol=1e-6,
        label=(
            op[
                "cell_id"
            ]
            +
            "/"
            +
            op[
                "operating_point"
            ]
            +
            "/cost break-even count equality"
        ),
    )


    break_even_rows.append(
        {
            "cell_id":
                op[
                    "cell_id"
                ],

            "source_stage":
                op[
                    "source_stage"
                ],

            "family":
                op[
                    "family"
                ],

            "direction":
                op[
                    "direction"
                ],

            "bridge":
                op[
                    "bridge"
                ],

            "variant":
                op[
                    "variant"
                ],

            "identity_duplicate_of":
                op[
                    "identity_duplicate_of"
                ],

            "operating_point":
                op[
                    "operating_point"
                ],

            "threshold":
                op[
                    "threshold"
                ],

            "tpr":
                tpr,

            "fpr":
                fpr,

            "C_FP":
                C_FP,

            "C_FN":
                C_FN,

            "cost_break_even_prevalence":
                pi_star,

            "cost_break_even_percent":
                (
                    pi_star
                    *
                    100.0
                ),

            "status":
                status_star,

            "model_minus_ignore_per_B_at_break_even":
                delta_per_B_at_star,

            "verification_attack_flows_per_day":
                attack_star,

            "verification_fp_per_day":
                fp_star,

            "verification_tp_per_day":
                tp_star,

            "verification_fn_per_day":
                fn_star,

            "verification_model_cost":
                model_star,

            "verification_ignore_cost":
                ignore_star,

            "neighbor_relative_epsilon":
                RELATIVE_NEIGHBOR_EPS,

            "prevalence_immediately_below":
                pi_below,

            "model_minus_ignore_per_B_below":
                delta_below,

            "preferred_below":
                "IGNORE_LOWER_RELATIVE_COST",

            "prevalence_immediately_above":
                pi_above,

            "model_minus_ignore_per_B_above":
                delta_above,

            "preferred_above":
                "MODEL_LOWER_RELATIVE_COST",
        }
    )


    sign_reversal_tests.append(
        {
            "cell_id":
                op[
                    "cell_id"
                ],

            "operating_point":
                op[
                    "operating_point"
                ],

            "cost_break_even_prevalence":
                pi_star,

            "delta_per_B_at_break_even":
                delta_per_B_at_star,

            "delta_per_B_below":
                delta_below,

            "delta_per_B_above":
                delta_above,

            "below_ignore_lower":
                (
                    delta_below
                    >
                    0.0
                ),

            "above_model_lower":
                (
                    delta_above
                    <
                    0.0
                ),

            "passed":
                True,
        }
    )


if len(
    break_even_rows
) != 24:

    raise RuntimeError(
        "Cost break-even table must contain 24 rows."
    )


print("=" * 120)
print("EXACT COST BREAK-EVEN")
print("=" * 120)

print(
    "Operating points:",
    len(
        break_even_rows
    ),
)

print(
    "[PASS] 24 exact analytic cost break-even prevalences."
)

print(
    "[PASS] 24 below/above sign reversals."
)

print()


# ==============================================================================
# 10. GRID CONSISTENCY WITH ANALYTIC BREAK-EVEN
# ==============================================================================

break_even_lookup = {
    (
        row[
            "cell_id"
        ],
        row[
            "operating_point"
        ],
    ):
        row[
            "cost_break_even_prevalence"
        ]
    for row in break_even_rows
}


grid_break_even_tests = []


for row in cost_projection_rows:

    pi_star = break_even_lookup[
        (
            row[
                "cell_id"
            ],
            row[
                "operating_point"
            ],
        )
    ]


    pi = row[
        "projection_prevalence"
    ]


    if pi > pi_star:

        expected = (
            "MODEL_LOWER_RELATIVE_COST"
        )

    elif pi < pi_star:

        expected = (
            "IGNORE_LOWER_RELATIVE_COST"
        )

    else:

        expected = (
            "EQUAL_WITHIN_NUMERICAL_TOLERANCE"
        )


    actual = row[
        "preferred_under_frozen_cost_model"
    ]


    # Exact equality with a grid point is extraordinarily unlikely.
    # If it happens, allow tolerance-classification.
    if expected.startswith(
        "EQUAL"
    ):

        pass

    elif actual != expected:

        raise RuntimeError(
            "\nGrid cost decision disagrees with analytic break-even.\n"
            f"{row['cell_id']} / {row['operating_point']}\n"
            f"pi={pi}\n"
            f"pi*={pi_star}\n"
            f"Expected={expected}\n"
            f"Actual={actual}"
        )


    grid_break_even_tests.append(
        {
            "cell_id":
                row[
                    "cell_id"
                ],

            "operating_point":
                row[
                    "operating_point"
                ],

            "projection_prevalence":
                pi,

            "cost_break_even_prevalence":
                pi_star,

            "expected_decision":
                expected,

            "actual_decision":
                actual,

            "passed":
                True,
        }
    )


if len(
    grid_break_even_tests
) != 144:

    raise RuntimeError(
        "Expected 144 grid/break-even consistency checks."
    )


print(
    "[PASS] All 144 grid cost decisions agree with exact break-even boundary."
)

print()


# ==============================================================================
# 11. COST DECISION SUMMARY
# ==============================================================================

prevalence_grid = [
    0.10,
    0.03,
    0.01,
    0.003,
    0.001,
    0.0001,
]


family_names = [
    "STAGE22_RANDOM",
    "STAGE22_CHRONOLOGICAL",
    "STAGE24_2018_TO_2017",
    "STAGE24_2017_TO_2018",
]


summary = {
    "all_operating_points":
        {},

    "by_family":
        {},
}


for pi in prevalence_grid:

    rows = [
        row
        for row in cost_projection_rows
        if row[
            "projection_prevalence"
        ]
        ==
        pi
    ]


    if len(
        rows
    ) != 24:

        raise RuntimeError(
            "Cost summary requires 24 rows per prevalence."
        )


    summary[
        "all_operating_points"
    ][
        str(
            pi
        )
    ] = {
        "operating_points":
            24,

        "model_lower_count":
            sum(
                row[
                    "preferred_under_frozen_cost_model"
                ]
                ==
                "MODEL_LOWER_RELATIVE_COST"
                for row in rows
            ),

        "ignore_lower_count":
            sum(
                row[
                    "preferred_under_frozen_cost_model"
                ]
                ==
                "IGNORE_LOWER_RELATIVE_COST"
                for row in rows
            ),

        "equal_count":
            sum(
                row[
                    "preferred_under_frozen_cost_model"
                ]
                ==
                "EQUAL_WITHIN_NUMERICAL_TOLERANCE"
                for row in rows
            ),
    }


for family in family_names:

    summary[
        "by_family"
    ][
        family
    ] = {}


    for pi in prevalence_grid:

        rows = [
            row
            for row in cost_projection_rows
            if (
                row[
                    "family"
                ]
                ==
                family
                and
                row[
                    "projection_prevalence"
                ]
                ==
                pi
            )
        ]


        summary[
            "by_family"
        ][
            family
        ][
            str(
                pi
            )
        ] = {
            "operating_points":
                len(
                    rows
                ),

            "model_lower_count":
                sum(
                    row[
                        "preferred_under_frozen_cost_model"
                    ]
                    ==
                    "MODEL_LOWER_RELATIVE_COST"
                    for row in rows
                ),

            "ignore_lower_count":
                sum(
                    row[
                        "preferred_under_frozen_cost_model"
                    ]
                    ==
                    "IGNORE_LOWER_RELATIVE_COST"
                    for row in rows
                ),

            "equal_count":
                sum(
                    row[
                        "preferred_under_frozen_cost_model"
                    ]
                    ==
                    "EQUAL_WITHIN_NUMERICAL_TOLERANCE"
                    for row in rows
                ),
        }


# ==============================================================================
# 12. HEADLINE LOW-PREVALENCE COST VIEW
# ==============================================================================

print("=" * 120)
print("HEADLINE RELATIVE-COST PROJECTIONS")
print("=" * 120)


for pi in [
    0.001,
    0.0001,
]:

    print()

    print(
        f"Projection prevalence = {pi:.4%}"
    )

    print(
        "-" * 120
    )


    rows = [
        row
        for row in cost_projection_rows
        if row[
            "projection_prevalence"
        ]
        ==
        pi
    ]


    for row in rows:

        pi_star = break_even_lookup[
            (
                row[
                    "cell_id"
                ],
                row[
                    "operating_point"
                ],
            )
        ]


        print(
            f"{row['cell_id']:<52s} "
            f"{row['operating_point']:<8s} "
            f"C_model={row['model_relative_cost']:>12.2f} "
            f"C_ignore={row['ignore_relative_cost']:>12.2f} "
            f"ratio={row['model_to_ignore_cost_ratio']:>10.4f} "
            f"pi*={pi_star:>11.8f} "
            f"{row['preferred_under_frozen_cost_model']}"
        )


print()


# ==============================================================================
# 13. REQUIRED SANITY TEST RESULTS
# ==============================================================================

sanity_payload = {
    "stage":
        "Stage25-3",

    "status":
        "PASS",

    "tests": {
        "COST_BREAK_EVEN_EQUALITY": {
            "expected_checks":
                24,

            "completed_checks":
                len(
                    break_even_rows
                ),

            "maximum_abs_delta_per_B":
                max(
                    abs(
                        row[
                            "model_minus_ignore_per_B_at_break_even"
                        ]
                    )
                    for row in break_even_rows
                ),

            "passed":
                True,
        },

        "COST_BREAK_EVEN_SIGN_REVERSAL": {
            "expected_checks":
                24,

            "completed_checks":
                len(
                    sign_reversal_tests
                ),

            "below_break_even":
                "IGNORE_LOWER_RELATIVE_COST",

            "above_break_even":
                "MODEL_LOWER_RELATIVE_COST",

            "passed":
                all(
                    row[
                        "passed"
                    ]
                    for row in sign_reversal_tests
                ),
        },

        "GRID_DECISION_MATCHES_ANALYTIC_BOUNDARY": {
            "expected_checks":
                144,

            "completed_checks":
                len(
                    grid_break_even_tests
                ),

            "passed":
                all(
                    row[
                        "passed"
                    ]
                    for row in grid_break_even_tests
                ),
        },

        "COST_DELTA_IDENTITY": {
            "identity":
                (
                    "C_model - C_ignore = "
                    "FP*C_FP - TP*C_FN"
                ),

            "expected_checks":
                144,

            "completed_checks":
                144,

            "passed":
                True,
        },

        "COMPLETE_COST_GRID": {
            "expected_rows":
                144,

            "actual_rows":
                len(
                    cost_projection_rows
                ),

            "passed":
                len(
                    cost_projection_rows
                )
                ==
                144,
        },

        "EXACT_PPV_BREAK_EVEN_TABLE_RETAINED": {
            "expected_rows":
                120,

            "actual_rows":
                len(
                    ppv_cliff_rows
                ),

            "source_sha256":
                actual_ppv_cliff_sha,

            "passed":
                len(
                    ppv_cliff_rows
                )
                ==
                120,
        },

        "EXACT_REQUIRED_FPR_TABLE_RETAINED": {
            "expected_rows":
                720,

            "actual_rows":
                len(
                    required_fpr_rows
                ),

            "source_sha256":
                actual_required_fpr_sha,

            "passed":
                len(
                    required_fpr_rows
                )
                ==
                720,
        },
    },
}


if not all(
    test[
        "passed"
    ]
    for test in sanity_payload[
        "tests"
    ].values()
):

    raise RuntimeError(
        "Stage25-3 sanity test failure."
    )


print("=" * 120)
print("SANITY TESTS")
print("=" * 120)


for name in sanity_payload[
    "tests"
]:

    print(
        "[PASS]",
        name,
    )


print()


# ==============================================================================
# 14. CREATE OUTPUT DIRECTORY
# ==============================================================================

OUT_DIR.mkdir(
    parents=True,
    exist_ok=False,
)


COST_GRID_CSV = (
    OUT_DIR
    / "cost_projection_grid.csv"
)


COST_BREAK_EVEN_CSV = (
    OUT_DIR
    / "cost_break_even_points.csv"
)


PPV_BREAK_EVEN_CSV = (
    OUT_DIR
    / "ppv_break_even_points.csv"
)


REQUIRED_FPR_CSV = (
    OUT_DIR
    / "required_fpr_by_ppv.csv"
)


COST_SUMMARY_JSON = (
    OUT_DIR
    / "cost_summary.json"
)


SANITY_JSON = (
    OUT_DIR
    / "stage25_3_sanity_tests.json"
)


write_csv(
    COST_GRID_CSV,
    cost_projection_rows,
)


write_csv(
    COST_BREAK_EVEN_CSV,
    break_even_rows,
)


# Preserve the exact already-frozen Stage25-1 analytic outputs byte-for-byte.
shutil.copy2(
    STAGE25_1_PPV_CLIFF,
    PPV_BREAK_EVEN_CSV,
)


shutil.copy2(
    STAGE25_1_REQUIRED_FPR,
    REQUIRED_FPR_CSV,
)


if sha256_file(
    PPV_BREAK_EVEN_CSV
) != actual_ppv_cliff_sha:

    raise RuntimeError(
        "PPV break-even copy is not byte-identical."
    )


if sha256_file(
    REQUIRED_FPR_CSV
) != actual_required_fpr_sha:

    raise RuntimeError(
        "Required-FPR copy is not byte-identical."
    )


write_json(
    COST_SUMMARY_JSON,
    {
        "stage":
            "Stage25-3",

        "relative_cost_model": {
            "C_FP":
                C_FP,

            "C_FN":
                C_FN,

            "units":
                "RELATIVE_OPERATIONAL_COST_UNITS",

            "not_currency":
                True,
        },

        "decision_summary":
            summary,

        "cost_break_even_min":
            min(
                row[
                    "cost_break_even_prevalence"
                ]
                for row in break_even_rows
            ),

        "cost_break_even_max":
            max(
                row[
                    "cost_break_even_prevalence"
                ]
                for row in break_even_rows
            ),

        "interpretation":
            (
                "For prevalence below an operating point's analytic "
                "cost break-even, the simplified ignore reference has "
                "lower expected relative operational cost. Above the "
                "break-even, the frozen model operating point has lower "
                "expected relative operational cost under C_FP=1/C_FN=100."
            ),

        "limitations": [
            "Cost units are not currency.",
            "The comparator is a simplified non-deployment/ignore reference.",
            "Every malicious flow is not interpreted as an independent breach.",
            "Results are conditional on frozen TPR/FPR and cost assumptions.",
        ],
    },
)


write_json(
    SANITY_JSON,
    sanity_payload,
)


# ==============================================================================
# 15. RESULT JSON
# ==============================================================================

result_payload = {
    "stage":
        "Stage25-3",

    "status":
        "EXACT_BREAK_EVEN_ANALYSIS_COMPLETE",

    "created_at_utc":
        datetime.now(
            timezone.utc
        ).isoformat(),

    "repository_parent_commit":
        EXPECTED_PARENT,

    "stage25_0_freeze_sha256":
        EXPECTED_STAGE25_0_FREEZE_SHA,

    "stage25_1_result_sha256":
        EXPECTED_STAGE25_1_RESULT_SHA,

    "stage25_2_result_sha256":
        EXPECTED_STAGE25_2_RESULT_SHA,

    "scientific_access": {
        "model_fit_calls":
            0,

        "model_inference_calls":
            0,

        "model_files_loaded":
            0,

        "probability_arrays_opened":
            0,

        "probability_arrays_created":
            0,

        "target_features_read":
            0,

        "target_labels_read":
            0,

        "target_reopenings":
            0,

        "threshold_searches":
            0,
    },

    "frozen_relative_cost": {
        "C_FP":
            C_FP,

        "C_FN":
            C_FN,

        "units":
            "RELATIVE_OPERATIONAL_COST_UNITS",

        "currency":
            False,
    },

    "analysis": {
        "operating_points":
            24,

        "prevalence_points":
            6,

        "cost_projection_rows":
            len(
                cost_projection_rows
            ),

        "cost_break_even_rows":
            len(
                break_even_rows
            ),

        "ppv_break_even_rows":
            len(
                ppv_cliff_rows
            ),

        "required_fpr_rows":
            len(
                required_fpr_rows
            ),
    },

    "cost_decision_summary":
        summary,

    "sanity_test_status":
        "PASS",

    "interpretation_boundary":
        (
            "All cost results are deterministic relative-operational-cost "
            "projections under the frozen 1:100 FP/FN cost ratio. "
            "They are not financial-loss estimates and do not imply that "
            "each malicious flow corresponds to an independent breach."
        ),

    "next_authorized_stage":
        "STAGE25_4_BENCHMARK_TO_OPERATIONAL_TRANSLATION",

    "artifacts":
        {},
}


result_payload[
    "artifacts"
] = {
    str(
        COST_GRID_CSV.relative_to(
            REPO
        )
    ):
        sha256_file(
            COST_GRID_CSV
        ),

    str(
        COST_BREAK_EVEN_CSV.relative_to(
            REPO
        )
    ):
        sha256_file(
            COST_BREAK_EVEN_CSV
        ),

    str(
        PPV_BREAK_EVEN_CSV.relative_to(
            REPO
        )
    ):
        sha256_file(
            PPV_BREAK_EVEN_CSV
        ),

    str(
        REQUIRED_FPR_CSV.relative_to(
            REPO
        )
    ):
        sha256_file(
            REQUIRED_FPR_CSV
        ),

    str(
        COST_SUMMARY_JSON.relative_to(
            REPO
        )
    ):
        sha256_file(
            COST_SUMMARY_JSON
        ),

    str(
        SANITY_JSON.relative_to(
            REPO
        )
    ):
        sha256_file(
            SANITY_JSON
        ),
}


RESULT_JSON = (
    OUT_DIR
    / "stage25_3_break_even_result.json"
)


write_json(
    RESULT_JSON,
    result_payload,
)


result_sha = sha256_file(
    RESULT_JSON
)


RESULT_SHA = (
    OUT_DIR
    / "stage25_3_break_even_result.sha256"
)


write_text(
    RESULT_SHA,
    (
        f"{result_sha}  "
        f"{RESULT_JSON.name}"
    ),
)


CHECKSUMS_OUT = (
    OUT_DIR
    / "checksums.sha256"
)


checksum_paths = [
    COST_GRID_CSV,
    COST_BREAK_EVEN_CSV,
    PPV_BREAK_EVEN_CSV,
    REQUIRED_FPR_CSV,
    COST_SUMMARY_JSON,
    SANITY_JSON,
    RESULT_JSON,
    RESULT_SHA,
]


write_text(
    CHECKSUMS_OUT,
    "\n".join(
        (
            f"{sha256_file(path)}  "
            f"{path.name}"
        )
        for path in checksum_paths
    ),
)


print("=" * 120)
print("STAGE25-3 ARTIFACTS")
print("=" * 120)


for path in (
    checksum_paths
    +
    [
        CHECKSUMS_OUT
    ]
):

    print(
        path.relative_to(
            REPO
        )
    )


print()

print(
    "Result SHA:"
)

print(
    " ",
    result_sha
)

print()


# ==============================================================================
# 16. GITHUB CREDENTIAL
# ==============================================================================

github_token = None

token_source = None


try:

    from kaggle_secrets import UserSecretsClient

    client = UserSecretsClient()


    for name in [
        "GITHUB_TOKEN",
        "github_token",
        "GH_TOKEN",
        "GITHUB_PAT",
        "github_pat",
    ]:

        try:

            value = client.get_secret(
                name
            )

            if (
                value
                and
                value.strip()
            ):

                github_token = value.strip()

                token_source = name

                break

        except Exception:

            pass

except Exception:

    pass


if github_token is None:

    for name in [
        "GITHUB_TOKEN",
        "GH_TOKEN",
    ]:

        value = os.environ.get(
            name
        )

        if (
            value
            and
            value.strip()
        ):

            github_token = value.strip()

            token_source = (
                "ENV:"
                +
                name
            )

            break


if github_token is None:

    raise RuntimeError(
        "GitHub token unavailable."
    )


auth_header = base64.b64encode(
    (
        "x-access-token:"
        +
        github_token
    ).encode()
).decode()


# ==============================================================================
# 17. GIT SAFETY
# ==============================================================================

print("=" * 120)
print("GIT SAFETY")
print("=" * 120)


remote_before = git_cmd(
    "ls-remote",
    "origin",
    "refs/heads/main",
    auth_header=auth_header,
).split()[0]


if remote_before != EXPECTED_PARENT:

    raise RuntimeError(
        "\nRemote main moved before Stage25-3 commit.\n"
        f"Expected: {EXPECTED_PARENT}\n"
        f"Actual:   {remote_before}"
    )


tracked_dirty = {
    line
    for line in git_cmd(
        "diff",
        "--name-only",
    ).splitlines()
    if line
}


untracked = {
    line
    for line in git_cmd(
        "ls-files",
        "--others",
        "--exclude-standard",
    ).splitlines()
    if line
}


dirty = (
    tracked_dirty
    |
    untracked
)


allowed_prefix = (
    "results/stage25_prevalence_stress/"
    "stage25_3_break_even_analysis/"
)


unexpected = [
    path
    for path in sorted(
        dirty
    )
    if not path.startswith(
        allowed_prefix
    )
]


if unexpected:

    raise RuntimeError(
        "\nUnexpected repository changes:\n"
        +
        "\n".join(
            unexpected
        )
    )


if not dirty:

    raise RuntimeError(
        "No Stage25-3 artifacts found."
    )


print(
    "GitHub credential:",
    token_source,
)

print(
    "[PASS] Remote main remains exact Stage25-2 commit."
)

print(
    "[PASS] Only Stage25-3 artifacts are dirty."
)

print()


# ==============================================================================
# 18. GIT AUTHOR
# ==============================================================================

if not git_cmd(
    "config",
    "--local",
    "--get",
    "user.name",
    check=False,
):

    git_cmd(
        "config",
        "--local",
        "user.name",
        git_cmd(
            "log",
            "-1",
            "--format=%an",
        ),
    )


if not git_cmd(
    "config",
    "--local",
    "--get",
    "user.email",
    check=False,
):

    git_cmd(
        "config",
        "--local",
        "user.email",
        git_cmd(
            "log",
            "-1",
            "--format=%ae",
        ),
    )


# ==============================================================================
# 19. STAGE
# ==============================================================================

git_cmd(
    "add",
    "--",
    str(
        OUT_DIR.relative_to(
            REPO
        )
    ),
)


staged = {
    line
    for line in git_cmd(
        "diff",
        "--cached",
        "--name-only",
    ).splitlines()
    if line
}


if not staged:

    raise RuntimeError(
        "No Stage25-3 files staged."
    )


bad_staged = [
    path
    for path in staged
    if not path.startswith(
        allowed_prefix
    )
]


if bad_staged:

    raise RuntimeError(
        "\nUnexpected staged files:\n"
        +
        "\n".join(
            sorted(
                bad_staged
            )
        )
    )


if git_cmd(
    "diff",
    "--name-only",
):

    raise RuntimeError(
        "Unstaged tracked files remain."
    )


if git_cmd(
    "ls-files",
    "--others",
    "--exclude-standard",
):

    raise RuntimeError(
        "Untracked files remain."
    )


print(
    "[PASS] Stage25-3 artifacts staged exclusively."
)

print()


# ==============================================================================
# 20. COMMIT
# ==============================================================================

print("=" * 120)
print("COMMIT STAGE25-3")
print("=" * 120)


commit_output = git_cmd(
    "commit",
    "-m",
    "stage25: freeze exact break-even analysis",
)


print(
    commit_output
)

print()


commit = git_cmd(
    "rev-parse",
    "HEAD",
)


parent = git_cmd(
    "rev-parse",
    "HEAD^",
)


if parent != EXPECTED_PARENT:

    raise RuntimeError(
        "\nStage25-3 parent mismatch.\n"
        f"Expected: {EXPECTED_PARENT}\n"
        f"Actual:   {parent}"
    )


# ==============================================================================
# 21. PUSH + REMOTE VERIFY
# ==============================================================================

print("=" * 120)
print("PUSH + REMOTE VERIFY")
print("=" * 120)


push_output = git_cmd(
    "push",
    "origin",
    "HEAD:main",
    auth_header=auth_header,
)


print(
    push_output
)

print()


remote_after = git_cmd(
    "ls-remote",
    "origin",
    "refs/heads/main",
    auth_header=auth_header,
).split()[0]


if remote_after != commit:

    raise RuntimeError(
        "\nRemote verification failed.\n"
        f"Local:  {commit}\n"
        f"Remote: {remote_after}"
    )


if git_cmd(
    "status",
    "--porcelain",
):

    raise RuntimeError(
        "Repository not clean after Stage25-3 push."
    )


print(
    "[PASS] Stage25-3 pushed."
)

print(
    "[PASS] Repository clean."
)

print()


# ==============================================================================
# 22. FINAL
# ==============================================================================

print("=" * 120)
print("STAGE25-3 EXACT BREAK-EVEN ANALYSIS: PASS")
print("=" * 120)

print()

print(
    "Parent Stage25-2 commit:"
)

print(
    " ",
    EXPECTED_PARENT
)

print()

print(
    "Stage25-3 commit:"
)

print(
    " ",
    commit
)

print()

print(
    "Remote main:"
)

print(
    " ",
    remote_after
)

print()

print(
    "Result SHA:"
)

print(
    " ",
    result_sha
)

print()

print(
    "Cost projection rows:          144"
)

print(
    "Exact cost break-even rows:    24"
)

print(
    "Exact PPV break-even rows:     120"
)

print(
    "Required-FPR rows:             720"
)

print()

print(
    "SANITY:"
)

print(
    "  Cost equality at pi*:        PASS"
)

print(
    "  Below/above sign reversal:   PASS"
)

print(
    "  Grid vs analytic boundary:   PASS"
)

print(
    "  Cost-delta identity:         PASS"
)

print(
    "  PPV break-even preserved:    PASS"
)

print(
    "  Required-FPR preserved:      PASS"
)

print()

print(
    "NEW MODEL FITS:                0"
)

print(
    "NEW MODEL INFERENCE:           0"
)

print(
    "NEW PROBABILITY ARRAYS:        0"
)

print(
    "TARGET REOPENINGS:             0"
)

print()

print(
    "NEXT AUTHORIZED:"
)

print(
    "  Stage25-4 — benchmark -> operational translation"
)

print()

print(
    "STOP HERE."
)

print("=" * 120)

# %% [Stage25 notebook cell 6]
# ==============================================================================
# STAGE25-4 — BENCHMARK -> OPERATIONAL TRANSLATION
#             + ALL PREREGISTERED FIGURES
#             + COMPLETE SANITY RE-AUDIT
#
# Authorized parent:
#   5d1f9b2437ed7731f375acf01667c0faac57494e
#
# Frozen Stage25-3 result SHA:
#   f7c59d81d1532e0a61461bc9f213e9947b5edfe15fd2f8d9eb5d10d0f6bf6732
#
# PURPOSE
# -------
# 1. Join Stage25-1 Bayesian projections,
#         Stage25-2 traffic/SOC projections,
#         Stage25-3 cost/break-even projections
#    into one exact 144-row publication matrix.
#
# 2. Build the frozen benchmark -> operational translation at pi=0.001:
#
#    Observed:
#       F1
#       precision
#       recall / TPR
#       FPR
#       observed prevalence
#
#    Projected at 0.1%:
#       PPV
#       FP/day
#       TP/day
#       alerts/day
#       analyst-hours/day
#
# 3. Generate EVERY preregistered figure:
#
#       Figure25-A  PPV Cliff
#       Figure25-B  SOC Capacity Exceedance
#       Figure25-C  Benchmark-to-Deployment Translation
#       Figure25-D  Required FPR for Target PPV
#       Figure25-E  Bayesian Evidence Translation
#
#    Formats:
#       PNG + SVG
#
# 4. Re-audit ALL frozen Stage25 sanity requirements.
#
# ABSOLUTE SCIENTIFIC RULES
# -------------------------
# NEW MODEL FITS:             0
# NEW MODEL INFERENCE:        0
# NEW PROBABILITY ARRAYS:     0
# TARGET REOPENINGS:          0
# NEW THRESHOLDS:             0
# NEW CALIBRATION:            0
#
# This stage does NOT alter any Stage25-0/1/2/3 scientific artifact.
#
# NEXT AFTER SUCCESS:
#   Stage25-5 — final audit + seal + publication closeout
# ==============================================================================

from __future__ import annotations

import os
import csv
import json
import math
import base64
import hashlib
import subprocess
from pathlib import Path
from datetime import datetime, timezone

import numpy as np

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt


print("=" * 120)
print("STAGE25-4 — BENCHMARK -> OPERATIONAL TRANSLATION + FIGURES")
print("=" * 120)
print()


# ==============================================================================
# 0. FROZEN ANCHORS
# ==============================================================================

REPO = Path(
    "/kaggle/working/ids2018-validation-safe-ablation"
)

EXPECTED_PARENT = (
    "5d1f9b2437ed7731f375acf01667c0faac57494e"
)

EXPECTED_STAGE25_0_FREEZE_SHA = (
    "d231af1e4f07363c4d932acc99e1052e3b33bd2d24ca22e4386f4c7c378827b7"
)

EXPECTED_STAGE25_1_RESULT_SHA = (
    "81e4d96494c3432745f97428b722cc8870f75372a2c4570653ec59e7bcaa25ff"
)

EXPECTED_STAGE25_2_RESULT_SHA = (
    "1e3e66eb1dcf416585fd3f0fada8675b6950fde5f3f45af006a25b1aec872737"
)

EXPECTED_STAGE25_3_RESULT_SHA = (
    "f7c59d81d1532e0a61461bc9f213e9947b5edfe15fd2f8d9eb5d10d0f6bf6732"
)


STAGE25_BASE = (
    REPO
    / "results"
    / "stage25_prevalence_stress"
)

LOCK_DIR = (
    STAGE25_BASE
    / "stage25_0_protocol_lock"
)

S1_DIR = (
    STAGE25_BASE
    / "stage25_1_bayesian_projection"
)

S2_DIR = (
    STAGE25_BASE
    / "stage25_2_traffic_soc_capacity"
)

S3_DIR = (
    STAGE25_BASE
    / "stage25_3_break_even_analysis"
)

OUT_DIR = (
    STAGE25_BASE
    / "stage25_4_benchmark_operational_translation"
)

FIG_DIR = (
    REPO
    / "figures"
    / "stage25_prevalence_stress"
)


FREEZE_RECORD = (
    LOCK_DIR
    / "freeze_record.json"
)

FIGURE_PLAN = (
    LOCK_DIR
    / "figure_plan.json"
)

SANITY_PLAN = (
    LOCK_DIR
    / "sanity_test_plan.json"
)

PREVALENCE_SPEC = (
    LOCK_DIR
    / "prevalence_grid.json"
)

CAPACITY_SPEC = (
    LOCK_DIR
    / "analyst_capacity_spec.json"
)

ANTI_ADAPTATION = (
    LOCK_DIR
    / "anti_adaptation.json"
)


S1_RESULT = (
    S1_DIR
    / "stage25_1_bayesian_projection_result.json"
)

S1_GRID = (
    S1_DIR
    / "stage25_1_bayesian_projection_grid.csv"
)

S1_LR = (
    S1_DIR
    / "stage25_1_likelihood_ratios.csv"
)

S1_REQUIRED_FPR = (
    S1_DIR
    / "stage25_1_required_fpr_for_target_ppv.csv"
)

S1_SANITY = (
    S1_DIR
    / "stage25_1_sanity_tests.json"
)


S2_RESULT = (
    S2_DIR
    / "stage25_2_traffic_soc_capacity_result.json"
)

S2_TRAFFIC = (
    S2_DIR
    / "stage25_2_traffic_soc_projection.csv"
)

S2_SANITY = (
    S2_DIR
    / "stage25_2_sanity_tests.json"
)


S3_RESULT = (
    S3_DIR
    / "stage25_3_break_even_result.json"
)

S3_COST_GRID = (
    S3_DIR
    / "cost_projection_grid.csv"
)

S3_COST_BREAK_EVEN = (
    S3_DIR
    / "cost_break_even_points.csv"
)

S3_SANITY = (
    S3_DIR
    / "stage25_3_sanity_tests.json"
)


# ==============================================================================
# 1. HELPERS
# ==============================================================================

def run_cmd(
    args,
    *,
    cwd=None,
    check=True,
):

    p = subprocess.run(
        [str(x) for x in args],
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    if check and p.returncode != 0:

        raise RuntimeError(
            "\nCommand failed:\n"
            +
            " ".join(
                str(x)
                for x in args
            )
            +
            "\n\n"
            +
            (
                p.stdout
                or
                ""
            )
        )

    return (
        p.stdout
        or
        ""
    ).strip()


def git_cmd(
    *args,
    auth_header=None,
    check=True,
):

    cmd = [
        "git"
    ]

    if auth_header is not None:

        cmd += [
            "-c",
            "credential.helper=",
            "-c",
            f"http.extraHeader=AUTHORIZATION: Basic {auth_header}",
        ]

    cmd += [
        str(x)
        for x in args
    ]

    return run_cmd(
        cmd,
        cwd=REPO,
        check=check,
    )


def sha256_file(
    path,
):

    path = Path(
        path
    )

    h = hashlib.sha256()

    with path.open(
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

    return h.hexdigest()


def load_json(
    path,
):

    path = Path(
        path
    )

    if not path.is_file():

        raise RuntimeError(
            f"Missing JSON:\n{path}"
        )

    return json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )


def write_json(
    path,
    payload,
):

    path = Path(
        path
    )

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    path.write_text(
        json.dumps(
            payload,
            indent=2,
            sort_keys=True,
            ensure_ascii=False,
            allow_nan=False,
        )
        +
        "\n",
        encoding="utf-8",
    )


def write_text(
    path,
    text,
):

    path = Path(
        path
    )

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    path.write_text(
        str(
            text
        ).rstrip()
        +
        "\n",
        encoding="utf-8",
    )


def read_csv(
    path,
):

    path = Path(
        path
    )

    if not path.is_file():

        raise RuntimeError(
            f"Missing CSV:\n{path}"
        )

    with path.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as fh:

        return list(
            csv.DictReader(
                fh
            )
        )


def write_csv(
    path,
    rows,
):

    path = Path(
        path
    )

    rows = list(
        rows
    )

    if not rows:

        raise RuntimeError(
            f"Refusing empty CSV:\n{path}"
        )

    fields = list(
        rows[
            0
        ].keys()
    )

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as fh:

        writer = csv.DictWriter(
            fh,
            fieldnames=fields,
            lineterminator="\n",
        )

        writer.writeheader()

        for row in rows:

            if list(
                row.keys()
            ) != fields:

                raise RuntimeError(
                    f"Inconsistent CSV schema:\n{path}"
                )

            writer.writerow(
                row
            )


def assert_close(
    actual,
    expected,
    *,
    atol=1e-10,
    label="value",
):

    if not math.isclose(
        float(
            actual
        ),
        float(
            expected
        ),
        rel_tol=0.0,
        abs_tol=atol,
    ):

        raise RuntimeError(
            "\nNumerical identity failure.\n"
            f"{label}\n"
            f"Expected: {expected!r}\n"
            f"Actual:   {actual!r}\n"
            f"Delta:    "
            f"{float(actual)-float(expected):+.17e}"
        )


def optional_float(
    value,
):

    if value is None:

        return None

    value = str(
        value
    )

    if value == "":

        return None

    return float(
        value
    )


def optional_string(
    value,
):

    if value is None:

        return None

    value = str(
        value
    )

    if value == "":

        return None

    return value


def bool_from_csv(
    value,
):

    if isinstance(
        value,
        bool,
    ):

        return value

    value = str(
        value
    ).strip().lower()

    if value == "true":

        return True

    if value == "false":

        return False

    raise RuntimeError(
        f"Invalid CSV boolean: {value!r}"
    )


def verify_result_sha(
    path,
    expected,
    label,
):

    actual = sha256_file(
        path
    )

    if actual != expected:

        raise RuntimeError(
            f"\n{label} SHA mismatch.\n"
            f"Expected: {expected}\n"
            f"Actual:   {actual}"
        )

    return actual


def save_figure(
    fig,
    stem,
):

    FIG_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    png = (
        FIG_DIR
        /
        f"{stem}.png"
    )

    svg = (
        FIG_DIR
        /
        f"{stem}.svg"
    )

    fig.savefig(
        png,
        dpi=300,
        bbox_inches="tight",
    )

    fig.savefig(
        svg,
        bbox_inches="tight",
    )

    plt.close(
        fig
    )

    if not png.is_file():

        raise RuntimeError(
            f"PNG not created: {png}"
        )

    if not svg.is_file():

        raise RuntimeError(
            f"SVG not created: {svg}"
        )

    if png.stat().st_size <= 0:

        raise RuntimeError(
            f"Empty PNG: {png}"
        )

    if svg.stat().st_size <= 0:

        raise RuntimeError(
            f"Empty SVG: {svg}"
        )

    return {
        "png": {
            "path":
                str(
                    png.relative_to(
                        REPO
                    )
                ),

            "sha256":
                sha256_file(
                    png
                ),

            "bytes":
                png.stat().st_size,
        },

        "svg": {
            "path":
                str(
                    svg.relative_to(
                        REPO
                    )
                ),

            "sha256":
                sha256_file(
                    svg
                ),

            "bytes":
                svg.stat().st_size,
        },
    }


# ==============================================================================
# 2. GOVERNANCE
# ==============================================================================

print("=" * 120)
print("GOVERNANCE")
print("=" * 120)


head = git_cmd(
    "rev-parse",
    "HEAD",
)


status = git_cmd(
    "status",
    "--porcelain",
)


print(
    "HEAD:",
    head,
)


if head != EXPECTED_PARENT:

    raise RuntimeError(
        "\nUnexpected Stage25-4 parent.\n"
        f"Expected: {EXPECTED_PARENT}\n"
        f"Actual:   {head}"
    )


if status:

    raise RuntimeError(
        "\nRepository must be clean before Stage25-4:\n"
        +
        status
    )


if OUT_DIR.exists():

    existing = list(
        OUT_DIR.iterdir()
    )

    if existing:

        raise RuntimeError(
            "\nStage25-4 output directory already exists with files:\n"
            +
            "\n".join(
                str(
                    p
                )
                for p in existing
            )
        )


if FIG_DIR.exists():

    existing_figures = list(
        FIG_DIR.iterdir()
    )

    if existing_figures:

        raise RuntimeError(
            "\nStage25 figure directory already contains files.\n"
            "Refusing accidental regeneration:\n"
            +
            "\n".join(
                str(
                    p
                )
                for p in existing_figures
            )
        )


freeze_sha = sha256_file(
    FREEZE_RECORD
)


if freeze_sha != EXPECTED_STAGE25_0_FREEZE_SHA:

    raise RuntimeError(
        "Stage25-0 freeze SHA changed."
    )


s1_sha = verify_result_sha(
    S1_RESULT,
    EXPECTED_STAGE25_1_RESULT_SHA,
    "Stage25-1 result",
)


s2_sha = verify_result_sha(
    S2_RESULT,
    EXPECTED_STAGE25_2_RESULT_SHA,
    "Stage25-2 result",
)


s3_sha = verify_result_sha(
    S3_RESULT,
    EXPECTED_STAGE25_3_RESULT_SHA,
    "Stage25-3 result",
)


s3_result = load_json(
    S3_RESULT
)


if (
    s3_result[
        "status"
    ]
    !=
    "EXACT_BREAK_EVEN_ANALYSIS_COMPLETE"
):

    raise RuntimeError(
        "Stage25-3 status changed."
    )


if (
    s3_result[
        "next_authorized_stage"
    ]
    !=
    "STAGE25_4_BENCHMARK_TO_OPERATIONAL_TRANSLATION"
):

    raise RuntimeError(
        "Stage25-4 is not authorized."
    )


for key, value in s3_result[
    "scientific_access"
].items():

    if int(
        value
    ) != 0:

        raise RuntimeError(
            f"Unexpected Stage25-3 scientific access: {key}={value}"
        )


print(
    "Stage25-0 freeze SHA:",
    freeze_sha,
)

print(
    "Stage25-1 result SHA:",
    s1_sha,
)

print(
    "Stage25-2 result SHA:",
    s2_sha,
)

print(
    "Stage25-3 result SHA:",
    s3_sha,
)

print()

print(
    "[PASS] Stage25-4 authorized."
)

print(
    "[PASS] No fit/inference/reopening activity."
)

print()


# ==============================================================================
# 3. VERIFY FROZEN FIGURE + SANITY PLANS
# ==============================================================================

print("=" * 120)
print("FROZEN FIGURE + SANITY PLAN")
print("=" * 120)


freeze_record = load_json(
    FREEZE_RECORD
)


protocol_hashes = freeze_record[
    "protocol_file_hashes"
]


for filename in [
    "figure_plan.json",
    "sanity_test_plan.json",
    "prevalence_grid.json",
    "analyst_capacity_spec.json",
    "anti_adaptation.json",
]:

    path = (
        LOCK_DIR
        /
        filename
    )

    actual = sha256_file(
        path
    )

    expected = protocol_hashes[
        filename
    ]

    if actual != expected:

        raise RuntimeError(
            "\nFrozen protocol artifact changed.\n"
            f"{filename}\n"
            f"Expected: {expected}\n"
            f"Actual:   {actual}"
        )


figure_plan = load_json(
    FIGURE_PLAN
)


sanity_plan = load_json(
    SANITY_PLAN
)


prevalence_spec = load_json(
    PREVALENCE_SPEC
)


capacity_spec = load_json(
    CAPACITY_SPEC
)


if (
    figure_plan[
        "drop_figure_based_on_results"
    ]
    !=
    "FORBIDDEN"
):

    raise RuntimeError(
        "Figure anti-selection rule changed."
    )


primary_figure_ids = [
    item[
        "id"
    ]
    for item in figure_plan[
        "primary"
    ]
]


supp_figure_ids = [
    item[
        "id"
    ]
    for item in figure_plan[
        "supplementary"
    ]
]


if primary_figure_ids != [
    "25-A",
    "25-B",
    "25-C",
    "25-D",
]:

    raise RuntimeError(
        "Primary figure plan changed."
    )


if supp_figure_ids != [
    "25-E"
]:

    raise RuntimeError(
        "Supplementary figure plan changed."
    )


expected_sanity_names = [
    "PPV_AT_OBSERVED_PREVALENCE",
    "PPV_MONOTONICITY",
    "FP_INVARIANCE",
    "COST_BREAK_EVEN_SIGN_REVERSAL",
    "PPV50_CHECK",
    "CONFUSION_IDENTITIES",
    "COMPLETE_PROJECTION_MATRIX",
]


actual_sanity_names = [
    item[
        "name"
    ]
    for item in sanity_plan[
        "tests"
    ]
]


if actual_sanity_names != expected_sanity_names:

    raise RuntimeError(
        "Frozen sanity-test plan changed."
    )


print(
    "Primary figures:",
    primary_figure_ids,
)

print(
    "Supplementary figures:",
    supp_figure_ids,
)

print(
    "Sanity tests:",
    len(
        actual_sanity_names
    ),
)

print()

print(
    "[PASS] Frozen figure plan exact."
)

print(
    "[PASS] Frozen sanity plan exact."
)

print()


# ==============================================================================
# 4. LOAD EXACT STAGE25 TABLES
# ==============================================================================

s1_rows_raw = read_csv(
    S1_GRID
)


s2_rows_raw = read_csv(
    S2_TRAFFIC
)


s3_cost_raw = read_csv(
    S3_COST_GRID
)


s3_break_even_raw = read_csv(
    S3_COST_BREAK_EVEN
)


required_fpr_raw = read_csv(
    S1_REQUIRED_FPR
)


lr_raw = read_csv(
    S1_LR
)


if len(
    s1_rows_raw
) != 144:

    raise RuntimeError(
        "Stage25-1 grid row count changed."
    )


if len(
    s2_rows_raw
) != 144:

    raise RuntimeError(
        "Stage25-2 grid row count changed."
    )


if len(
    s3_cost_raw
) != 144:

    raise RuntimeError(
        "Stage25-3 cost grid row count changed."
    )


if len(
    s3_break_even_raw
) != 24:

    raise RuntimeError(
        "Stage25-3 break-even row count changed."
    )


if len(
    required_fpr_raw
) != 720:

    raise RuntimeError(
        "Required-FPR row count changed."
    )


if len(
    lr_raw
) != 24:

    raise RuntimeError(
        "Likelihood-ratio row count changed."
    )


# ==============================================================================
# 5. NORMALIZE STAGE25-1
# ==============================================================================

s1_rows = []


for raw in s1_rows_raw:

    s1_rows.append(
        {
            "cell_id":
                raw[
                    "cell_id"
                ],

            "source_stage":
                raw[
                    "source_stage"
                ],

            "family":
                raw[
                    "family"
                ],

            "direction":
                raw[
                    "direction"
                ],

            "bridge":
                raw[
                    "bridge"
                ],

            "variant":
                raw[
                    "variant"
                ],

            "identity_duplicate_of":
                optional_string(
                    raw[
                        "identity_duplicate_of"
                    ]
                ),

            "operating_point":
                raw[
                    "operating_point"
                ],

            "threshold":
                float(
                    raw[
                        "threshold"
                    ]
                ),

            "tpr":
                float(
                    raw[
                        "tpr"
                    ]
                ),

            "fpr":
                float(
                    raw[
                        "fpr"
                    ]
                ),

            "frozen_f1":
                optional_float(
                    raw[
                        "frozen_f1"
                    ]
                ),

            "frozen_precision":
                float(
                    raw[
                        "frozen_precision"
                    ]
                ),

            "observed_prevalence":
                float(
                    raw[
                        "observed_prevalence"
                    ]
                ),

            "projection_prevalence":
                float(
                    raw[
                        "projection_prevalence"
                    ]
                ),

            "ppv":
                float(
                    raw[
                        "ppv"
                    ]
                ),

            "npv":
                float(
                    raw[
                        "npv"
                    ]
                ),

            "lr_plus":
                optional_float(
                    raw[
                        "lr_plus"
                    ]
                ),

            "lr_plus_status":
                raw[
                    "lr_plus_status"
                ],

            "lr_minus":
                optional_float(
                    raw[
                        "lr_minus"
                    ]
                ),

            "lr_minus_status":
                raw[
                    "lr_minus_status"
                ],
        }
    )


# ==============================================================================
# 6. NORMALIZE STAGE25-2
# ==============================================================================

s2_lookup = {}


for raw in s2_rows_raw:

    key = (
        raw[
            "cell_id"
        ],
        raw[
            "operating_point"
        ],
        float(
            raw[
                "projection_prevalence"
            ]
        ),
    )


    if key in s2_lookup:

        raise RuntimeError(
            f"Duplicate Stage25-2 key: {key}"
        )


    s2_lookup[
        key
    ] = {
        "tp_per_day":
            float(
                raw[
                    "tp_per_day"
                ]
            ),

        "fn_per_day":
            float(
                raw[
                    "fn_per_day"
                ]
            ),

        "fp_per_day":
            float(
                raw[
                    "fp_per_day"
                ]
            ),

        "tn_per_day":
            float(
                raw[
                    "tn_per_day"
                ]
            ),

        "total_alerts_per_day":
            float(
                raw[
                    "total_alerts_per_day"
                ]
            ),

        "false_alert_fraction":
            float(
                raw[
                    "false_alert_fraction"
                ]
            ),

        "false_alert_processing_hours_per_day":
            float(
                raw[
                    "false_alert_processing_hours_per_day"
                ]
            ),

        "total_alert_processing_hours_per_day":
            float(
                raw[
                    "total_alert_processing_hours_per_day"
                ]
            ),

        "analyst_days_required":
            float(
                raw[
                    "analyst_days_required"
                ]
            ),

        "aci_1":
            float(
                raw[
                    "aci_1"
                ]
            ),

        "aci_3":
            float(
                raw[
                    "aci_3"
                ]
            ),

        "aci_10":
            float(
                raw[
                    "aci_10"
                ]
            ),

        "capacity_exceeded_1":
            bool_from_csv(
                raw[
                    "capacity_exceeded_1"
                ]
            ),

        "capacity_exceeded_3":
            bool_from_csv(
                raw[
                    "capacity_exceeded_3"
                ]
            ),

        "capacity_exceeded_10":
            bool_from_csv(
                raw[
                    "capacity_exceeded_10"
                ]
            ),
    }


# ==============================================================================
# 7. NORMALIZE STAGE25-3
# ==============================================================================

s3_cost_lookup = {}


for raw in s3_cost_raw:

    key = (
        raw[
            "cell_id"
        ],
        raw[
            "operating_point"
        ],
        float(
            raw[
                "projection_prevalence"
            ]
        ),
    )


    if key in s3_cost_lookup:

        raise RuntimeError(
            f"Duplicate Stage25-3 cost key: {key}"
        )


    s3_cost_lookup[
        key
    ] = {
        "model_relative_cost":
            float(
                raw[
                    "model_relative_cost"
                ]
            ),

        "ignore_relative_cost":
            float(
                raw[
                    "ignore_relative_cost"
                ]
            ),

        "model_minus_ignore":
            float(
                raw[
                    "model_minus_ignore"
                ]
            ),

        "model_to_ignore_cost_ratio":
            optional_float(
                raw[
                    "model_to_ignore_cost_ratio"
                ]
            ),

        "relative_savings_vs_ignore":
            optional_float(
                raw[
                    "relative_savings_vs_ignore"
                ]
            ),

        "preferred_under_frozen_cost_model":
            raw[
                "preferred_under_frozen_cost_model"
            ],
    }


break_even_lookup = {}


for raw in s3_break_even_raw:

    key = (
        raw[
            "cell_id"
        ],
        raw[
            "operating_point"
        ],
    )


    if key in break_even_lookup:

        raise RuntimeError(
            f"Duplicate cost break-even key: {key}"
        )


    break_even_lookup[
        key
    ] = {
        "cost_break_even_prevalence":
            float(
                raw[
                    "cost_break_even_prevalence"
                ]
            ),

        "cost_break_even_percent":
            float(
                raw[
                    "cost_break_even_percent"
                ]
            ),
    }


# ==============================================================================
# 8. BUILD EXACT 144-ROW MASTER PUBLICATION MATRIX
# ==============================================================================

master_rows = []


for row in s1_rows:

    key3 = (
        row[
            "cell_id"
        ],
        row[
            "operating_point"
        ],
        row[
            "projection_prevalence"
        ],
    )


    key2 = (
        row[
            "cell_id"
        ],
        row[
            "operating_point"
        ],
    )


    if key3 not in s2_lookup:

        raise RuntimeError(
            f"Missing Stage25-2 join key: {key3}"
        )


    if key3 not in s3_cost_lookup:

        raise RuntimeError(
            f"Missing Stage25-3 join key: {key3}"
        )


    if key2 not in break_even_lookup:

        raise RuntimeError(
            f"Missing cost break-even key: {key2}"
        )


    s2 = s2_lookup[
        key3
    ]

    s3 = s3_cost_lookup[
        key3
    ]

    be = break_even_lookup[
        key2
    ]


    master_rows.append(
        {
            "cell_id":
                row[
                    "cell_id"
                ],

            "source_stage":
                row[
                    "source_stage"
                ],

            "family":
                row[
                    "family"
                ],

            "direction":
                row[
                    "direction"
                ],

            "bridge":
                row[
                    "bridge"
                ],

            "variant":
                row[
                    "variant"
                ],

            "identity_duplicate_of":
                row[
                    "identity_duplicate_of"
                ],

            "operating_point":
                row[
                    "operating_point"
                ],

            "threshold":
                row[
                    "threshold"
                ],

            "tpr":
                row[
                    "tpr"
                ],

            "fpr":
                row[
                    "fpr"
                ],

            "frozen_f1":
                row[
                    "frozen_f1"
                ],

            "frozen_precision":
                row[
                    "frozen_precision"
                ],

            "observed_prevalence":
                row[
                    "observed_prevalence"
                ],

            "projection_prevalence":
                row[
                    "projection_prevalence"
                ],

            "projected_ppv":
                row[
                    "ppv"
                ],

            "projected_npv":
                row[
                    "npv"
                ],

            "lr_plus":
                row[
                    "lr_plus"
                ],

            "lr_plus_status":
                row[
                    "lr_plus_status"
                ],

            "lr_minus":
                row[
                    "lr_minus"
                ],

            "lr_minus_status":
                row[
                    "lr_minus_status"
                ],

            "tp_per_day":
                s2[
                    "tp_per_day"
                ],

            "fn_per_day":
                s2[
                    "fn_per_day"
                ],

            "fp_per_day":
                s2[
                    "fp_per_day"
                ],

            "tn_per_day":
                s2[
                    "tn_per_day"
                ],

            "total_alerts_per_day":
                s2[
                    "total_alerts_per_day"
                ],

            "false_alert_fraction":
                s2[
                    "false_alert_fraction"
                ],

            "false_alert_processing_hours_per_day":
                s2[
                    "false_alert_processing_hours_per_day"
                ],

            "total_alert_processing_hours_per_day":
                s2[
                    "total_alert_processing_hours_per_day"
                ],

            "analyst_days_required":
                s2[
                    "analyst_days_required"
                ],

            "aci_1":
                s2[
                    "aci_1"
                ],

            "aci_3":
                s2[
                    "aci_3"
                ],

            "aci_10":
                s2[
                    "aci_10"
                ],

            "capacity_exceeded_1":
                s2[
                    "capacity_exceeded_1"
                ],

            "capacity_exceeded_3":
                s2[
                    "capacity_exceeded_3"
                ],

            "capacity_exceeded_10":
                s2[
                    "capacity_exceeded_10"
                ],

            "model_relative_cost":
                s3[
                    "model_relative_cost"
                ],

            "ignore_relative_cost":
                s3[
                    "ignore_relative_cost"
                ],

            "model_minus_ignore":
                s3[
                    "model_minus_ignore"
                ],

            "model_to_ignore_cost_ratio":
                s3[
                    "model_to_ignore_cost_ratio"
                ],

            "relative_savings_vs_ignore":
                s3[
                    "relative_savings_vs_ignore"
                ],

            "preferred_under_frozen_cost_model":
                s3[
                    "preferred_under_frozen_cost_model"
                ],

            "cost_break_even_prevalence":
                be[
                    "cost_break_even_prevalence"
                ],

            "cost_break_even_percent":
                be[
                    "cost_break_even_percent"
                ],
        }
    )


if len(
    master_rows
) != 144:

    raise RuntimeError(
        "\nMaster matrix must contain 144 rows.\n"
        f"Actual: {len(master_rows)}"
    )


master_keys = {
    (
        row[
            "cell_id"
        ],
        row[
            "operating_point"
        ],
        row[
            "projection_prevalence"
        ],
    )
    for row in master_rows
}


if len(
    master_keys
) != 144:

    raise RuntimeError(
        "Master matrix keys are not unique."
    )


print("=" * 120)
print("MASTER PUBLICATION MATRIX")
print("=" * 120)

print(
    "Rows:",
    len(
        master_rows
    ),
)

print(
    "[PASS] Exact Stage25-1/2/3 join: 144 / 144."
)

print()


# ==============================================================================
# 9. BENCHMARK -> OPERATIONAL TRANSLATION AT 0.1%
# ==============================================================================

TRANSLATION_PREVALENCE = 0.001


translation_rows = []


for row in master_rows:

    if row[
        "projection_prevalence"
    ] != TRANSLATION_PREVALENCE:

        continue


    translation_rows.append(
        {
            "cell_id":
                row[
                    "cell_id"
                ],

            "family":
                row[
                    "family"
                ],

            "direction":
                row[
                    "direction"
                ],

            "bridge":
                row[
                    "bridge"
                ],

            "variant":
                row[
                    "variant"
                ],

            "operating_point":
                row[
                    "operating_point"
                ],

            "threshold":
                row[
                    "threshold"
                ],

            # --------------------------------------------------
            # Frozen empirical benchmark / target characteristics
            # --------------------------------------------------

            "observed_f1":
                row[
                    "frozen_f1"
                ],

            "observed_precision":
                row[
                    "frozen_precision"
                ],

            "observed_recall_tpr":
                row[
                    "tpr"
                ],

            "observed_fpr":
                row[
                    "fpr"
                ],

            "observed_prevalence":
                row[
                    "observed_prevalence"
                ],

            # --------------------------------------------------
            # Frozen 0.1% deployment-stress projection
            # --------------------------------------------------

            "projection_prevalence":
                TRANSLATION_PREVALENCE,

            "projected_ppv":
                row[
                    "projected_ppv"
                ],

            "projected_fp_per_day":
                row[
                    "fp_per_day"
                ],

            "projected_tp_per_day":
                row[
                    "tp_per_day"
                ],

            "projected_total_alerts_per_day":
                row[
                    "total_alerts_per_day"
                ],

            "projected_alert_processing_hours_per_day":
                row[
                    "total_alert_processing_hours_per_day"
                ],

            "projected_aci_1":
                row[
                    "aci_1"
                ],

            "projected_aci_3":
                row[
                    "aci_3"
                ],

            "projected_aci_10":
                row[
                    "aci_10"
                ],

            "projected_relative_cost_decision":
                row[
                    "preferred_under_frozen_cost_model"
                ],

            "cost_break_even_prevalence":
                row[
                    "cost_break_even_prevalence"
                ],
        }
    )


if len(
    translation_rows
) != 24:

    raise RuntimeError(
        "\nTranslation table must contain 24 rows.\n"
        f"Actual: {len(translation_rows)}"
    )


print("=" * 120)
print("BENCHMARK -> OPERATIONAL TRANSLATION @ 0.1%")
print("=" * 120)

print(
    "Rows:",
    len(
        translation_rows
    ),
)

print()


for row in translation_rows:

    print(
        f"{row['cell_id']:<52s} "
        f"{row['operating_point']:<8s} "
        f"F1={row['observed_f1'] if row['observed_f1'] is not None else float('nan'):.6f} "
        f"Prec={row['observed_precision']:.6f} "
        f"TPR={row['observed_recall_tpr']:.6f} "
        f"FPR={row['observed_fpr']:.6f} "
        f"=> PPV@0.1%={row['projected_ppv']:.6f} "
        f"FP/day={row['projected_fp_per_day']:.1f} "
        f"TP/day={row['projected_tp_per_day']:.1f} "
        f"alerts={row['projected_total_alerts_per_day']:.1f} "
        f"hours={row['projected_alert_processing_hours_per_day']:.1f}"
    )


print()


# ==============================================================================
# 10. SHORT LABELS FOR FIGURES
# ==============================================================================

def cell_base_label(
    row,
):

    cell = row[
        "cell_id"
    ]


    mapping = {
        "STAGE22_RANDOM":
            "S22 Random",

        "STAGE22_CHRONOLOGICAL":
            "S22 Chron",

        "STAGE24_2018_TO_2017_BRIDGE62_PUBLISHED":
            "18→17 B62 Pub",

        "STAGE24_2018_TO_2017_BRIDGE62_FLAG_CORRECTED":
            "18→17 B62 Corr",

        "STAGE24_2018_TO_2017_BRIDGE70_PUBLISHED":
            "18→17 B70 Pub",

        "STAGE24_2018_TO_2017_BRIDGE70_FLAG_CORRECTED":
            "18→17 B70 Corr",

        "STAGE24_2017_TO_2018_BRIDGE62":
            "17→18 B62",

        "STAGE24_2017_TO_2018_BRIDGE70":
            "17→18 B70",
    }


    if cell not in mapping:

        raise RuntimeError(
            f"Unknown cell label: {cell}"
        )


    return mapping[
        cell
    ]


def operating_point_short(
    name,
):

    return {
        "STANDARD":
            "Std",

        "BALANCED":
            "Bal",

        "SECURITY":
            "Sec",
    }[
        name
    ]


def figure_series_label(
    row,
):

    return (
        cell_base_label(
            row
        )
        +
        " / "
        +
        operating_point_short(
            row[
                "operating_point"
            ]
        )
    )


family_order = [
    "STAGE22_RANDOM",
    "STAGE22_CHRONOLOGICAL",
    "STAGE24_2018_TO_2017",
    "STAGE24_2017_TO_2018",
]


family_titles = {
    "STAGE22_RANDOM":
        "Stage22 Random-Natural",

    "STAGE22_CHRONOLOGICAL":
        "Stage22 Chronological-Natural",

    "STAGE24_2018_TO_2017":
        "Stage24 IDS2018 → CICIDS2017",

    "STAGE24_2017_TO_2018":
        "Stage24 CICIDS2017 → IDS2018",
}


# ==============================================================================
# 11. FIGURE 25-A — PPV CLIFF
# ==============================================================================

print("=" * 120)
print("FIGURE 25-A — PPV CLIFF")
print("=" * 120)


fig, axes = plt.subplots(
    2,
    2,
    figsize=(
        18,
        12,
    ),
    sharex=True,
    sharey=True,
)


axes = axes.flatten()


for ax, family in zip(
    axes,
    family_order,
):

    family_rows = [
        row
        for row in master_rows
        if row[
            "family"
        ]
        ==
        family
    ]


    series_keys = sorted(
        {
            (
                row[
                    "cell_id"
                ],
                row[
                    "operating_point"
                ],
            )
            for row in family_rows
        }
    )


    for cell_id, op_name in series_keys:

        rows = sorted(
            [
                row
                for row in family_rows
                if (
                    row[
                        "cell_id"
                    ]
                    ==
                    cell_id
                    and
                    row[
                        "operating_point"
                    ]
                    ==
                    op_name
                )
            ],
            key=lambda x:
                x[
                    "projection_prevalence"
                ],
        )


        x = [
            row[
                "projection_prevalence"
            ]
            for row in rows
        ]


        y = [
            row[
                "projected_ppv"
            ]
            for row in rows
        ]


        line = ax.plot(
            x,
            y,
            marker="o",
            markersize=4,
            linewidth=1.3,
            label=figure_series_label(
                rows[
                    0
                ]
            ),
        )[0]


        observed_x = rows[
            0
        ][
            "observed_prevalence"
        ]


        observed_y = rows[
            0
        ][
            "frozen_precision"
        ]


        ax.scatter(
            [
                observed_x
            ],
            [
                observed_y
            ],
            marker="X",
            s=50,
            color=line.get_color(),
            zorder=5,
        )


    ax.axhline(
        0.50,
        linestyle="--",
        linewidth=1.0,
        color="black",
        alpha=0.7,
    )


    ax.axhline(
        0.10,
        linestyle=":",
        linewidth=1.0,
        color="black",
        alpha=0.7,
    )


    for pi in prevalence_spec[
        "prevalence_grid"
    ][
        "decimal"
    ]:

        ax.axvline(
            pi,
            linewidth=0.45,
            alpha=0.12,
            color="black",
        )


    ax.set_xscale(
        "log"
    )

    ax.set_xlim(
        8e-5,
        0.25,
    )

    ax.set_ylim(
        0.0,
        1.02,
    )

    ax.set_title(
        family_titles[
            family
        ]
    )

    ax.grid(
        True,
        which="both",
        alpha=0.20,
    )


    ax.legend(
        fontsize=6.5,
        loc="best",
    )


for ax in axes[
    2:
]:

    ax.set_xlabel(
        "Attack prevalence"
    )


for ax in axes[
    ::2
]:

    ax.set_ylabel(
        "Positive predictive value (PPV)"
    )


fig.suptitle(
    (
        "Figure 25-A. PPV cliff under frozen prior-probability shift\n"
        "X markers denote exact observed-prevalence precision; "
        "circles denote preregistered deployment-stress points."
    ),
    fontsize=14,
)


fig.tight_layout(
    rect=[
        0,
        0,
        1,
        0.95,
    ]
)


fig25a = save_figure(
    fig,
    "figure25_a_ppv_cliff",
)


print(
    "[CREATED]",
    fig25a[
        "png"
    ][
        "path"
    ],
)

print(
    "[CREATED]",
    fig25a[
        "svg"
    ][
        "path"
    ],
)

print()


# ==============================================================================
# 12. FIGURE 25-B — SOC CAPACITY EXCEEDANCE
# ==============================================================================

print("=" * 120)
print("FIGURE 25-B — SOC CAPACITY EXCEEDANCE")
print("=" * 120)


fig, axes = plt.subplots(
    2,
    2,
    figsize=(
        18,
        12,
    ),
    sharex=True,
)


axes = axes.flatten()


for ax, family in zip(
    axes,
    family_order,
):

    family_rows = [
        row
        for row in master_rows
        if row[
            "family"
        ]
        ==
        family
    ]


    series_keys = sorted(
        {
            (
                row[
                    "cell_id"
                ],
                row[
                    "operating_point"
                ],
            )
            for row in family_rows
        }
    )


    for cell_id, op_name in series_keys:

        rows = sorted(
            [
                row
                for row in family_rows
                if (
                    row[
                        "cell_id"
                    ]
                    ==
                    cell_id
                    and
                    row[
                        "operating_point"
                    ]
                    ==
                    op_name
                )
            ],
            key=lambda x:
                x[
                    "projection_prevalence"
                ],
        )


        x = [
            row[
                "projection_prevalence"
            ]
            for row in rows
        ]


        total_hours = [
            row[
                "total_alert_processing_hours_per_day"
            ]
            for row in rows
        ]


        fp_hours = [
            row[
                "false_alert_processing_hours_per_day"
            ]
            for row in rows
        ]


        line = ax.plot(
            x,
            total_hours,
            marker="o",
            markersize=3.5,
            linewidth=1.3,
            label=figure_series_label(
                rows[
                    0
                ]
            ),
        )[0]


        ax.plot(
            x,
            fp_hours,
            linestyle="--",
            linewidth=0.8,
            alpha=0.55,
            color=line.get_color(),
        )


    for hours, label in [
        (
            8,
            "1 analyst-day",
        ),
        (
            24,
            "3 analyst-days",
        ),
        (
            80,
            "10 analyst-days",
        ),
    ]:

        ax.axhline(
            hours,
            linestyle=":",
            linewidth=1.0,
            color="black",
            alpha=0.55,
        )


    ax.set_xscale(
        "log"
    )

    ax.set_xlim(
        8e-5,
        0.12,
    )

    ax.set_title(
        family_titles[
            family
        ]
    )

    ax.grid(
        True,
        which="both",
        alpha=0.20,
    )


    ax.legend(
        fontsize=6.5,
        loc="best",
    )


for ax in axes[
    2:
]:

    ax.set_xlabel(
        "Attack prevalence"
    )


for ax in axes[
    ::2
]:

    ax.set_ylabel(
        "Alert-processing hours/day"
    )


fig.suptitle(
    (
        "Figure 25-B. SOC capacity exceedance under frozen traffic assumptions\n"
        "Solid = total alert workload; dashed = false-alert workload; "
        "reference lines = 8, 24, and 80 analyst-hours/day."
    ),
    fontsize=14,
)


fig.tight_layout(
    rect=[
        0,
        0,
        1,
        0.95,
    ]
)


fig25b = save_figure(
    fig,
    "figure25_b_soc_capacity_exceedance",
)


print(
    "[CREATED]",
    fig25b[
        "png"
    ][
        "path"
    ],
)

print(
    "[CREATED]",
    fig25b[
        "svg"
    ][
        "path"
    ],
)

print()


# ==============================================================================
# 13. FIGURE 25-C — BENCHMARK TO DEPLOYMENT TRANSLATION
#
# A publication table-figure avoids mixing incomparable metric scales.
# ==============================================================================
# noqa: E501

print("=" * 120)
print("FIGURE 25-C — BENCHMARK TO DEPLOYMENT TRANSLATION")
print("=" * 120)


translation_display = sorted(
    translation_rows,
    key=lambda row:
        (
            family_order.index(
                row[
                    "family"
                ]
            ),
            row[
                "cell_id"
            ],
            [
                "STANDARD",
                "BALANCED",
                "SECURITY",
            ].index(
                row[
                    "operating_point"
                ]
            ),
        ),
)


column_labels = [
    "Operating point",
    "F1",
    "Precision",
    "Recall",
    "FPR",
    "Observed π",
    "PPV @ 0.1%",
    "FP/day",
    "TP/day",
    "Alerts/day",
    "Hours/day",
]


table_rows = []


for row in translation_display:

    table_rows.append(
        [
            (
                cell_base_label(
                    row
                )
                +
                " / "
                +
                operating_point_short(
                    row[
                        "operating_point"
                    ]
                )
            ),

            (
                "—"
                if row[
                    "observed_f1"
                ] is None
                else
                f"{row['observed_f1']:.4f}"
            ),

            f"{row['observed_precision']:.4f}",

            f"{row['observed_recall_tpr']:.4f}",

            f"{row['observed_fpr']:.6f}",

            f"{row['observed_prevalence']:.4f}",

            f"{row['projected_ppv']:.4f}",

            f"{row['projected_fp_per_day']:,.1f}",

            f"{row['projected_tp_per_day']:,.1f}",

            f"{row['projected_total_alerts_per_day']:,.1f}",

            f"{row['projected_alert_processing_hours_per_day']:,.1f}",
        ]
    )


fig, ax = plt.subplots(
    figsize=(
        20,
        14,
    )
)


ax.axis(
    "off"
)


table = ax.table(
    cellText=table_rows,
    colLabels=column_labels,
    loc="center",
    cellLoc="center",
    colLoc="center",
)


table.auto_set_font_size(
    False
)


table.set_fontsize(
    7.3
)


table.scale(
    1.0,
    1.45,
)


for (
    row_index,
    col_index
), cell in table.get_celld().items():

    if row_index == 0:

        cell.set_text_props(
            weight="bold"
        )


    if col_index == 0:

        cell.set_text_props(
            ha="left"
        )


ax.set_title(
    (
        "Figure 25-C. Benchmark-to-deployment translation at 0.1% attack prevalence\n"
        "Observed benchmark/target metrics are shown beside frozen deployment-stress projections."
    ),
    fontsize=14,
    pad=22,
)


fig25c = save_figure(
    fig,
    "figure25_c_benchmark_to_deployment_translation",
)


print(
    "[CREATED]",
    fig25c[
        "png"
    ][
        "path"
    ],
)

print(
    "[CREATED]",
    fig25c[
        "svg"
    ][
        "path"
    ],
)

print()


# ==============================================================================
# 14. FIGURE 25-D — REQUIRED FPR FOR TARGET PPV
#
# 24 small multiples:
#   no operating point is selected/dropped after seeing results.
# ==============================================================================
# noqa: E501

print("=" * 120)
print("FIGURE 25-D — REQUIRED FPR FOR TARGET PPV")
print("=" * 120)


required_rows = []


for raw in required_fpr_raw:

    required_rows.append(
        {
            "cell_id":
                raw[
                    "cell_id"
                ],

            "family":
                raw[
                    "family"
                ],

            "direction":
                raw[
                    "direction"
                ],

            "bridge":
                raw[
                    "bridge"
                ],

            "variant":
                raw[
                    "variant"
                ],

            "operating_point":
                raw[
                    "operating_point"
                ],

            "threshold":
                float(
                    raw[
                        "threshold"
                    ]
                ),

            "tpr":
                float(
                    raw[
                        "tpr"
                    ]
                ),

            "actual_fpr":
                float(
                    raw[
                        "actual_fpr"
                    ]
                ),

            "projection_prevalence":
                float(
                    raw[
                        "projection_prevalence"
                    ]
                ),

            "ppv_target":
                float(
                    raw[
                        "ppv_target"
                    ]
                ),

            "required_max_fpr":
                float(
                    raw[
                        "required_max_fpr"
                    ]
                ),
        }
    )


op_keys = sorted(
    {
        (
            row[
                "cell_id"
            ],
            row[
                "operating_point"
            ],
        )
        for row in required_rows
    },
    key=lambda key:
        (
            family_order.index(
                next(
                    row[
                        "family"
                    ]
                    for row in required_rows
                    if (
                        row[
                            "cell_id"
                        ],
                        row[
                            "operating_point"
                        ],
                    )
                    ==
                    key
                )
            ),
            key[
                0
            ],
            [
                "STANDARD",
                "BALANCED",
                "SECURITY",
            ].index(
                key[
                    1
                ]
            ),
        ),
)


if len(
    op_keys
) != 24:

    raise RuntimeError(
        "Figure25-D expected 24 operating points."
    )


fig, axes = plt.subplots(
    6,
    4,
    figsize=(
        18,
        24,
    ),
    sharex=True,
)


axes = axes.flatten()


target_values = [
    0.10,
    0.25,
    0.50,
    0.75,
    0.90,
]


legend_handles = None

legend_labels = None


for ax, key in zip(
    axes,
    op_keys,
):

    cell_id, op_name = key


    rows_for_op = [
        row
        for row in required_rows
        if (
            row[
                "cell_id"
            ]
            ==
            cell_id
            and
            row[
                "operating_point"
            ]
            ==
            op_name
        )
    ]


    if len(
        rows_for_op
    ) != 30:

        raise RuntimeError(
            f"Figure25-D expected 30 rows for {key}."
        )


    for target in target_values:

        rows = sorted(
            [
                row
                for row in rows_for_op
                if row[
                    "ppv_target"
                ]
                ==
                target
            ],
            key=lambda row:
                row[
                    "projection_prevalence"
                ],
        )


        ax.plot(
            [
                row[
                    "projection_prevalence"
                ]
                for row in rows
            ],
            [
                row[
                    "required_max_fpr"
                ]
                for row in rows
            ],
            marker="o",
            markersize=2.5,
            linewidth=1.0,
            label=(
                f"PPV {target:.0%}"
            ),
        )


    actual_fpr = rows_for_op[
        0
    ][
        "actual_fpr"
    ]


    ax.axhline(
        actual_fpr,
        linestyle="--",
        linewidth=1.0,
        color="black",
        label="Actual frozen FPR",
    )


    ax.set_xscale(
        "log"
    )

    ax.set_yscale(
        "log"
    )

    ax.grid(
        True,
        which="both",
        alpha=0.15,
    )


    temp_row = {
        "cell_id":
            cell_id,

        "operating_point":
            op_name,
    }


    ax.set_title(
        figure_series_label(
            temp_row
        ),
        fontsize=8,
    )


    if legend_handles is None:

        legend_handles, legend_labels = (
            ax.get_legend_handles_labels()
        )


for ax in axes[
    -4:
]:

    ax.set_xlabel(
        "Attack prevalence"
    )


for index, ax in enumerate(
    axes
):

    if index % 4 == 0:

        ax.set_ylabel(
            "Maximum permissible FPR"
        )


fig.legend(
    legend_handles,
    legend_labels,
    loc="upper center",
    ncol=6,
    fontsize=9,
    bbox_to_anchor=(
        0.5,
        0.985,
    ),
)


fig.suptitle(
    (
        "Figure 25-D. Required false-positive rate for target PPV\n"
        "All 24 frozen operating points are shown; dashed line = actual frozen FPR."
    ),
    fontsize=14,
    y=0.997,
)


fig.tight_layout(
    rect=[
        0,
        0,
        1,
        0.97,
    ]
)


fig25d = save_figure(
    fig,
    "figure25_d_required_fpr_for_target_ppv",
)


print(
    "[CREATED]",
    fig25d[
        "png"
    ][
        "path"
    ],
)

print(
    "[CREATED]",
    fig25d[
        "svg"
    ][
        "path"
    ],
)

print()


# ==============================================================================
# 15. FIGURE 25-E — BAYESIAN EVIDENCE TRANSLATION
#
# Avoid post-result representative selection:
#   show ALL 24 inherited operating points.
# ==============================================================================
# noqa: E501

print("=" * 120)
print("FIGURE 25-E — BAYESIAN EVIDENCE TRANSLATION")
print("=" * 120)


fig, axes = plt.subplots(
    2,
    2,
    figsize=(
        18,
        12,
    ),
    sharex=True,
    sharey=True,
)


axes = axes.flatten()


for ax, family in zip(
    axes,
    family_order,
):

    rows_family = [
        row
        for row in master_rows
        if row[
            "family"
        ]
        ==
        family
    ]


    keys = sorted(
        {
            (
                row[
                    "cell_id"
                ],
                row[
                    "operating_point"
                ],
            )
            for row in rows_family
        }
    )


    for key in keys:

        rows = sorted(
            [
                row
                for row in rows_family
                if (
                    row[
                        "cell_id"
                    ],
                    row[
                        "operating_point"
                    ],
                )
                ==
                key
            ],
            key=lambda row:
                row[
                    "projection_prevalence"
                ],
        )


        ax.plot(
            [
                row[
                    "projection_prevalence"
                ]
                for row in rows
            ],
            [
                row[
                    "projected_ppv"
                ]
                for row in rows
            ],
            marker="o",
            markersize=3,
            linewidth=1.1,
            label=figure_series_label(
                rows[
                    0
                ]
            ),
        )


    # Evidence-neutral reference: posterior == prior.
    diagonal_x = np.array(
        prevalence_spec[
            "prevalence_grid"
        ][
            "decimal"
        ],
        dtype=float,
    )


    ax.plot(
        diagonal_x,
        diagonal_x,
        linestyle=":",
        color="black",
        linewidth=1.0,
        label="Posterior = prior",
    )


    ax.set_xscale(
        "log"
    )

    ax.set_yscale(
        "log"
    )

    ax.set_xlim(
        8e-5,
        0.12,
    )

    ax.set_ylim(
        1e-6,
        1.0,
    )

    ax.grid(
        True,
        which="both",
        alpha=0.18,
    )


    ax.set_title(
        family_titles[
            family
        ]
    )


    ax.legend(
        fontsize=6.5,
        loc="best",
    )


for ax in axes[
    2:
]:

    ax.set_xlabel(
        "Prior attack probability"
    )


for ax in axes[
    ::2
]:

    ax.set_ylabel(
        "Posterior attack probability after positive alert"
    )


fig.suptitle(
    (
        "Figure 25-E. Bayesian evidence translation for all inherited LR+ operating points\n"
        "Posterior attack probability after a positive alert is shown across the frozen prevalence grid."
    ),
    fontsize=14,
)


fig.tight_layout(
    rect=[
        0,
        0,
        1,
        0.95,
    ]
)


fig25e = save_figure(
    fig,
    "figure25_e_bayesian_evidence_translation",
)


print(
    "[CREATED]",
    fig25e[
        "png"
    ][
        "path"
    ],
)

print(
    "[CREATED]",
    fig25e[
        "svg"
    ][
        "path"
    ],
)

print()


# ==============================================================================
# 16. COMPLETE PREREGISTERED SANITY RE-AUDIT
# ==============================================================================

print("=" * 120)
print("COMPLETE PREREGISTERED SANITY RE-AUDIT")
print("=" * 120)


s1_sanity = load_json(
    S1_SANITY
)


s2_sanity = load_json(
    S2_SANITY
)


s3_sanity = load_json(
    S3_SANITY
)


sanity_receipts = {
    "PPV_AT_OBSERVED_PREVALENCE": {
        "source_stage":
            "Stage25-1",

        "source_test":
            "PPV_AT_OBSERVED_PREVALENCE",

        "passed":
            bool(
                s1_sanity[
                    "tests"
                ][
                    "PPV_AT_OBSERVED_PREVALENCE"
                ][
                    "passed"
                ]
            ),
    },

    "PPV_MONOTONICITY": {
        "source_stage":
            "Stage25-1",

        "source_test":
            "PPV_MONOTONICITY",

        "passed":
            bool(
                s1_sanity[
                    "tests"
                ][
                    "PPV_MONOTONICITY"
                ][
                    "passed"
                ]
            ),
    },

    "FP_INVARIANCE": {
        "source_stage":
            "Stage25-2",

        "source_test":
            "FP_INVARIANCE",

        "passed":
            bool(
                s2_sanity[
                    "tests"
                ][
                    "FP_INVARIANCE"
                ][
                    "passed"
                ]
            ),
    },

    "COST_BREAK_EVEN_SIGN_REVERSAL": {
        "source_stage":
            "Stage25-3",

        "source_test":
            "COST_BREAK_EVEN_SIGN_REVERSAL",

        "passed":
            bool(
                s3_sanity[
                    "tests"
                ][
                    "COST_BREAK_EVEN_SIGN_REVERSAL"
                ][
                    "passed"
                ]
            ),
    },

    "PPV50_CHECK": {
        "source_stage":
            "Stage25-1",

        "source_test":
            "PPV50_EXACT_CHECK",

        "passed":
            bool(
                s1_sanity[
                    "tests"
                ][
                    "PPV50_EXACT_CHECK"
                ][
                    "passed"
                ]
            ),
    },

    "CONFUSION_IDENTITIES": {
        "source_stage":
            "Stage25-2",

        "source_test":
            "PROJECTED_CONFUSION_IDENTITIES",

        "passed":
            bool(
                s2_sanity[
                    "tests"
                ][
                    "PROJECTED_CONFUSION_IDENTITIES"
                ][
                    "passed"
                ]
            ),
    },

    "COMPLETE_PROJECTION_MATRIX": {
        "source_stage":
            "Stage25-1 + Stage25-4 join",

        "source_test":
            "COMPLETE_PROJECTION_MATRIX",

        "passed":
            (
                bool(
                    s1_sanity[
                        "tests"
                    ][
                        "COMPLETE_PROJECTION_MATRIX"
                    ][
                        "passed"
                    ]
                )
                and
                len(
                    master_rows
                )
                ==
                144
            ),
    },
}


if set(
    sanity_receipts.keys()
) != set(
    expected_sanity_names
):

    raise RuntimeError(
        "Sanity receipt set does not match frozen plan."
    )


if not all(
    item[
        "passed"
    ]
    for item in sanity_receipts.values()
):

    failed = [
        name
        for name, item in sanity_receipts.items()
        if not item[
            "passed"
        ]
    ]

    raise RuntimeError(
        "\nFrozen sanity re-audit failed:\n"
        +
        "\n".join(
            failed
        )
    )


for name in expected_sanity_names:

    print(
        "[PASS]",
        name,
    )


print()

print(
    "[PASS] ALL 7 preregistered Stage25 sanity requirements satisfied."
)

print()


# ==============================================================================
# 17. FIGURE COMPLETENESS AUDIT
# ==============================================================================

figure_manifest = {
    "stage":
        "Stage25-4",

    "frozen_figure_plan_status":
        "ALL_REQUIRED_FIGURES_GENERATED",

    "outcome_based_figure_dropping":
        False,

    "figures": {
        "25-A":
            fig25a,

        "25-B":
            fig25b,

        "25-C":
            fig25c,

        "25-D":
            fig25d,

        "25-E":
            fig25e,
    },
}


if set(
    figure_manifest[
        "figures"
    ].keys()
) != {
    "25-A",
    "25-B",
    "25-C",
    "25-D",
    "25-E",
}:

    raise RuntimeError(
        "Figure manifest incomplete."
    )


print("=" * 120)
print("FIGURE COMPLETENESS")
print("=" * 120)


for figure_id in [
    "25-A",
    "25-B",
    "25-C",
    "25-D",
    "25-E",
]:

    print(
        "[PASS]",
        figure_id,
        "PNG + SVG",
    )


print()


# ==============================================================================
# 18. LOW-PREVALENCE SUMMARY
# ==============================================================================

low_prevalence_rows = []


for pi in [
    0.001,
    0.0001,
]:

    rows = [
        row
        for row in master_rows
        if row[
            "projection_prevalence"
        ]
        ==
        pi
    ]


    if len(
        rows
    ) != 24:

        raise RuntimeError(
            f"Expected 24 rows at pi={pi}."
        )


    for row in rows:

        low_prevalence_rows.append(
            {
                "cell_id":
                    row[
                        "cell_id"
                    ],

                "family":
                    row[
                        "family"
                    ],

                "operating_point":
                    row[
                        "operating_point"
                    ],

                "projection_prevalence":
                    pi,

                "ppv":
                    row[
                        "projected_ppv"
                    ],

                "fpr":
                    row[
                        "fpr"
                    ],

                "fp_per_day":
                    row[
                        "fp_per_day"
                    ],

                "tp_per_day":
                    row[
                        "tp_per_day"
                    ],

                "total_alerts_per_day":
                    row[
                        "total_alerts_per_day"
                    ],

                "alert_processing_hours_per_day":
                    row[
                        "total_alert_processing_hours_per_day"
                    ],

                "aci_1":
                    row[
                        "aci_1"
                    ],

                "aci_3":
                    row[
                        "aci_3"
                    ],

                "aci_10":
                    row[
                        "aci_10"
                    ],

                "relative_cost_decision":
                    row[
                        "preferred_under_frozen_cost_model"
                    ],

                "cost_break_even_prevalence":
                    row[
                        "cost_break_even_prevalence"
                    ],
            }
        )


if len(
    low_prevalence_rows
) != 48:

    raise RuntimeError(
        "Low-prevalence summary must contain 48 rows."
    )


# ==============================================================================
# 19. CREATE RESULT DIRECTORY + PUBLICATION TABLES
# ==============================================================================

OUT_DIR.mkdir(
    parents=True,
    exist_ok=False,
)


MASTER_CSV = (
    OUT_DIR
    / "stage25_4_master_projection_matrix.csv"
)


TRANSLATION_CSV = (
    OUT_DIR
    / "stage25_4_benchmark_to_operational_translation_0p1pct.csv"
)


LOW_PREVALENCE_CSV = (
    OUT_DIR
    / "stage25_4_low_prevalence_summary.csv"
)


SANITY_JSON = (
    OUT_DIR
    / "stage25_4_complete_sanity_audit.json"
)


FIGURE_MANIFEST_JSON = (
    OUT_DIR
    / "stage25_4_figure_manifest.json"
)


write_csv(
    MASTER_CSV,
    master_rows,
)


write_csv(
    TRANSLATION_CSV,
    translation_rows,
)


write_csv(
    LOW_PREVALENCE_CSV,
    low_prevalence_rows,
)


write_json(
    SANITY_JSON,
    {
        "stage":
            "Stage25-4",

        "status":
            "ALL_PREREGISTERED_SANITY_TESTS_PASS",

        "frozen_test_count":
            7,

        "tests":
            sanity_receipts,

        "master_projection_rows":
            len(
                master_rows
            ),

        "translation_rows_at_0_1_percent":
            len(
                translation_rows
            ),
    },
)


write_json(
    FIGURE_MANIFEST_JSON,
    figure_manifest,
)


# ==============================================================================
# 20. RESULT
# ==============================================================================

result_payload = {
    "stage":
        "Stage25-4",

    "status":
        "BENCHMARK_TO_OPERATIONAL_TRANSLATION_AND_FIGURES_COMPLETE",

    "created_at_utc":
        datetime.now(
            timezone.utc
        ).isoformat(),

    "repository_parent_commit":
        EXPECTED_PARENT,

    "stage25_0_freeze_sha256":
        EXPECTED_STAGE25_0_FREEZE_SHA,

    "stage25_1_result_sha256":
        EXPECTED_STAGE25_1_RESULT_SHA,

    "stage25_2_result_sha256":
        EXPECTED_STAGE25_2_RESULT_SHA,

    "stage25_3_result_sha256":
        EXPECTED_STAGE25_3_RESULT_SHA,

    "scientific_access": {
        "model_fit_calls":
            0,

        "model_inference_calls":
            0,

        "model_files_loaded":
            0,

        "probability_arrays_opened":
            0,

        "probability_arrays_created":
            0,

        "target_features_read":
            0,

        "target_labels_read":
            0,

        "target_reopenings":
            0,

        "threshold_searches":
            0,

        "calibration_runs":
            0,
    },

    "analysis": {
        "master_projection_rows":
            len(
                master_rows
            ),

        "benchmark_translation_rows":
            len(
                translation_rows
            ),

        "benchmark_translation_prevalence":
            TRANSLATION_PREVALENCE,

        "low_prevalence_summary_rows":
            len(
                low_prevalence_rows
            ),

        "primary_figures":
            4,

        "supplementary_figures":
            1,

        "figure_files":
            10,

        "preregistered_sanity_tests":
            7,
    },

    "figure_plan": {
        "25-A":
            "PPV Cliff",

        "25-B":
            "SOC Capacity Exceedance",

        "25-C":
            "Benchmark-to-Deployment Translation",

        "25-D":
            "Required FPR for Target PPV",

        "25-E":
            "Bayesian Evidence Translation",
    },

    "sanity_status":
        "ALL_7_PREREGISTERED_TESTS_PASS",

    "interpretation_boundary":
        (
            "The benchmark-to-operational translation is a deterministic "
            "projection from frozen empirical TPR/FPR operating points under "
            "the preregistered prior-shift, traffic-volume, alert-service-time, "
            "capacity, and relative-cost assumptions. It is not empirical "
            "production validation."
        ),

    "next_authorized_stage":
        "STAGE25_5_FINAL_AUDIT_AND_SEAL",

    "artifacts":
        {},
}


artifact_paths = [
    MASTER_CSV,
    TRANSLATION_CSV,
    LOW_PREVALENCE_CSV,
    SANITY_JSON,
    FIGURE_MANIFEST_JSON,
]


for item in figure_manifest[
    "figures"
].values():

    artifact_paths.append(
        REPO
        /
        item[
            "png"
        ][
            "path"
        ]
    )

    artifact_paths.append(
        REPO
        /
        item[
            "svg"
        ][
            "path"
        ]
    )


for path in artifact_paths:

    result_payload[
        "artifacts"
    ][
        str(
            path.relative_to(
                REPO
            )
        )
    ] = sha256_file(
        path
    )


RESULT_JSON = (
    OUT_DIR
    / "stage25_4_translation_result.json"
)


write_json(
    RESULT_JSON,
    result_payload,
)


result_sha = sha256_file(
    RESULT_JSON
)


RESULT_SHA = (
    OUT_DIR
    / "stage25_4_translation_result.sha256"
)


write_text(
    RESULT_SHA,
    (
        f"{result_sha}  "
        f"{RESULT_JSON.name}"
    ),
)


CHECKSUMS = (
    OUT_DIR
    / "checksums.sha256"
)


checksum_paths = (
    artifact_paths
    +
    [
        RESULT_JSON,
        RESULT_SHA,
    ]
)


write_text(
    CHECKSUMS,
    "\n".join(
        (
            f"{sha256_file(path)}  "
            f"{path.relative_to(REPO)}"
        )
        for path in checksum_paths
    ),
)


print("=" * 120)
print("STAGE25-4 ARTIFACTS")
print("=" * 120)


for path in [
    MASTER_CSV,
    TRANSLATION_CSV,
    LOW_PREVALENCE_CSV,
    SANITY_JSON,
    FIGURE_MANIFEST_JSON,
    RESULT_JSON,
    RESULT_SHA,
    CHECKSUMS,
]:

    print(
        path.relative_to(
            REPO
        )
    )


print()

print(
    "Figures:"
)


for figure_id, item in figure_manifest[
    "figures"
].items():

    print(
        f"  {figure_id}:"
    )

    print(
        "   ",
        item[
            "png"
        ][
            "path"
        ]
    )

    print(
        "   ",
        item[
            "svg"
        ][
            "path"
        ]
    )


print()

print(
    "Result SHA:"
)

print(
    " ",
    result_sha
)

print()


# ==============================================================================
# 21. GITHUB CREDENTIAL
# ==============================================================================

github_token = None

token_source = None


try:

    from kaggle_secrets import UserSecretsClient

    client = UserSecretsClient()


    for name in [
        "GITHUB_TOKEN",
        "github_token",
        "GH_TOKEN",
        "GITHUB_PAT",
        "github_pat",
    ]:

        try:

            value = client.get_secret(
                name
            )

            if (
                value
                and
                value.strip()
            ):

                github_token = value.strip()

                token_source = name

                break

        except Exception:

            pass

except Exception:

    pass


if github_token is None:

    for name in [
        "GITHUB_TOKEN",
        "GH_TOKEN",
    ]:

        value = os.environ.get(
            name
        )

        if (
            value
            and
            value.strip()
        ):

            github_token = value.strip()

            token_source = (
                "ENV:"
                +
                name
            )

            break


if github_token is None:

    raise RuntimeError(
        "GitHub token unavailable."
    )


auth_header = base64.b64encode(
    (
        "x-access-token:"
        +
        github_token
    ).encode()
).decode()


# ==============================================================================
# 22. GIT SAFETY
# ==============================================================================

print("=" * 120)
print("GIT SAFETY")
print("=" * 120)


remote_before = git_cmd(
    "ls-remote",
    "origin",
    "refs/heads/main",
    auth_header=auth_header,
).split()[0]


if remote_before != EXPECTED_PARENT:

    raise RuntimeError(
        "\nRemote main moved before Stage25-4 commit.\n"
        f"Expected: {EXPECTED_PARENT}\n"
        f"Actual:   {remote_before}"
    )


tracked_dirty = {
    line
    for line in git_cmd(
        "diff",
        "--name-only",
    ).splitlines()
    if line
}


untracked = {
    line
    for line in git_cmd(
        "ls-files",
        "--others",
        "--exclude-standard",
    ).splitlines()
    if line
}


dirty = (
    tracked_dirty
    |
    untracked
)


allowed_prefixes = (
    (
        "results/stage25_prevalence_stress/"
        "stage25_4_benchmark_operational_translation/"
    ),
    "figures/stage25_prevalence_stress/",
)


unexpected = [
    path
    for path in sorted(
        dirty
    )
    if not any(
        path.startswith(
            prefix
        )
        for prefix in allowed_prefixes
    )
]


if unexpected:

    raise RuntimeError(
        "\nUnexpected repository changes:\n"
        +
        "\n".join(
            unexpected
        )
    )


if not dirty:

    raise RuntimeError(
        "No Stage25-4 artifacts found."
    )


print(
    "GitHub credential:",
    token_source,
)

print(
    "[PASS] Remote main remains exact Stage25-3 commit."
)

print(
    "[PASS] Only Stage25-4 results + frozen figures are dirty."
)

print()


# ==============================================================================
# 23. GIT AUTHOR
# ==============================================================================

if not git_cmd(
    "config",
    "--local",
    "--get",
    "user.name",
    check=False,
):

    git_cmd(
        "config",
        "--local",
        "user.name",
        git_cmd(
            "log",
            "-1",
            "--format=%an",
        ),
    )


if not git_cmd(
    "config",
    "--local",
    "--get",
    "user.email",
    check=False,
):

    git_cmd(
        "config",
        "--local",
        "user.email",
        git_cmd(
            "log",
            "-1",
            "--format=%ae",
        ),
    )


# ==============================================================================
# 24. STAGE
# ==============================================================================

git_cmd(
    "add",
    "--",
    str(
        OUT_DIR.relative_to(
            REPO
        )
    ),
    str(
        FIG_DIR.relative_to(
            REPO
        )
    ),
)


staged = {
    line
    for line in git_cmd(
        "diff",
        "--cached",
        "--name-only",
    ).splitlines()
    if line
}


if not staged:

    raise RuntimeError(
        "No Stage25-4 files staged."
    )


bad_staged = [
    path
    for path in staged
    if not any(
        path.startswith(
            prefix
        )
        for prefix in allowed_prefixes
    )
]


if bad_staged:

    raise RuntimeError(
        "\nUnexpected staged files:\n"
        +
        "\n".join(
            sorted(
                bad_staged
            )
        )
    )


if git_cmd(
    "diff",
    "--name-only",
):

    raise RuntimeError(
        "Unstaged tracked files remain."
    )


if git_cmd(
    "ls-files",
    "--others",
    "--exclude-standard",
):

    raise RuntimeError(
        "Untracked files remain."
    )


print(
    "[PASS] Stage25-4 result + all 10 figure files staged exclusively."
)

print()


# ==============================================================================
# 25. COMMIT
# ==============================================================================

print("=" * 120)
print("COMMIT STAGE25-4")
print("=" * 120)


commit_output = git_cmd(
    "commit",
    "-m",
    "stage25: freeze benchmark operational translation and figures",
)


print(
    commit_output
)

print()


commit = git_cmd(
    "rev-parse",
    "HEAD",
)


parent = git_cmd(
    "rev-parse",
    "HEAD^",
)


if parent != EXPECTED_PARENT:

    raise RuntimeError(
        "\nStage25-4 parent mismatch.\n"
        f"Expected: {EXPECTED_PARENT}\n"
        f"Actual:   {parent}"
    )


# ==============================================================================
# 26. PUSH + REMOTE VERIFY
# ==============================================================================

print("=" * 120)
print("PUSH + REMOTE VERIFY")
print("=" * 120)


push_output = git_cmd(
    "push",
    "origin",
    "HEAD:main",
    auth_header=auth_header,
)


print(
    push_output
)

print()


remote_after = git_cmd(
    "ls-remote",
    "origin",
    "refs/heads/main",
    auth_header=auth_header,
).split()[0]


if remote_after != commit:

    raise RuntimeError(
        "\nRemote verification failed.\n"
        f"Local:  {commit}\n"
        f"Remote: {remote_after}"
    )


if git_cmd(
    "status",
    "--porcelain",
):

    raise RuntimeError(
        "Repository not clean after Stage25-4 push."
    )


print(
    "[PASS] Stage25-4 pushed."
)

print(
    "[PASS] Repository clean."
)

print()


# ==============================================================================
# 27. FINAL
# ==============================================================================

print("=" * 120)
print("STAGE25-4 BENCHMARK -> OPERATIONAL TRANSLATION: PASS")
print("=" * 120)

print()

print(
    "Parent Stage25-3 commit:"
)

print(
    " ",
    EXPECTED_PARENT
)

print()

print(
    "Stage25-4 commit:"
)

print(
    " ",
    commit
)

print()

print(
    "Remote main:"
)

print(
    " ",
    remote_after
)

print()

print(
    "Result SHA:"
)

print(
    " ",
    result_sha
)

print()

print(
    "Master projection rows:        144"
)

print(
    "0.1% translation rows:         24"
)

print(
    "Low-prevalence summary rows:   48"
)

print()

print(
    "FIGURES:"
)

print(
    "  Figure25-A PPV Cliff:                      PNG + SVG"
)

print(
    "  Figure25-B SOC Capacity Exceedance:        PNG + SVG"
)

print(
    "  Figure25-C Benchmark -> Deployment:        PNG + SVG"
)

print(
    "  Figure25-D Required FPR for Target PPV:    PNG + SVG"
)

print(
    "  Figure25-E Bayesian Evidence Translation:  PNG + SVG"
)

print()

print(
    "SANITY:"
)

print(
    "  PPV @ observed prevalence:    PASS"
)

print(
    "  PPV monotonicity:             PASS"
)

print(
    "  FP invariance:                PASS"
)

print(
    "  Cost sign reversal:           PASS"
)

print(
    "  PPV50 identity:               PASS"
)

print(
    "  Confusion identities:         PASS"
)

print(
    "  Complete 24x6 matrix:         PASS"
)

print()

print(
    "ALL 7 PREREGISTERED TESTS:     PASS"
)

print()

print(
    "NEW MODEL FITS:                0"
)

print(
    "NEW MODEL INFERENCE:           0"
)

print(
    "NEW PROBABILITY ARRAYS:        0"
)

print(
    "TARGET REOPENINGS:             0"
)

print()

print(
    "NEXT AUTHORIZED:"
)

print(
    "  Stage25-5 — FINAL AUDIT + SEAL"
)

print()

print(
    "STOP HERE."
)

print("=" * 120)

# %% [Stage25 notebook cell 7]
# ==============================================================================
# STAGE25-5 — FINAL AUDIT + SCIENTIFIC SEAL
#             + PUBLICATION PACKAGE
#             + MANUSCRIPT INTEGRATION
#             + NOTEBOOK/SCRIPT EXPORT
#             + GITHUB CLOSEOUT
#
# Authorized parent:
#   7820b9865a08f78107673207480c54d8dd0fe3eb
#
# Frozen Stage25-4 result SHA:
#   8fcc28f0ce2a616a166f22f4a33d0c76001f8ef9a337739bd32c14778932c205
#
# PURPOSE
# -------
# Final Stage25 closeout only.
#
# This cell performs:
#
#   1. Complete Stage25 commit-chain and artifact audit
#   2. Re-verification of all Stage25 scientific-access counters
#   3. Re-verification of all 7 preregistered sanity tests
#   4. Re-verification of all 5 preregistered figures / 10 files
#   5. Publication tables
#   6. Paper-ready Results
#   7. Discussion
#   8. Limitations / Threats to Validity
#   9. Contributions
#  10. Markdown + LaTeX manuscript integration
#  11. Current Stage25 notebook export
#  12. Sanitized GitHub notebook export
#  13. Python script export
#  14. Publication manifest
#  15. Final Stage25 synthesis / scientific seal
#  16. README + journal-extension summary update
#  17. Downloadable notebook/script ZIP
#  18. Downloadable publication-package ZIP
#  19. Git commit + push + remote verification
#
# ABSOLUTE SCIENTIFIC RULES
# -------------------------
# NEW MODEL FITS:             0
# NEW MODEL INFERENCE:        0
# NEW PROBABILITY ARRAYS:     0
# TARGET REOPENINGS:          0
# NEW THRESHOLDS:             0
# NEW CALIBRATION:            0
# NEW SCIENTIFIC PROJECTION:  0
#
# Stage25-5 only audits, summarizes, packages and seals ALREADY-FROZEN results.
# ==============================================================================

from __future__ import annotations

import os
import re
import csv
import json
import math
import base64
import shutil
import zipfile
import hashlib
import subprocess
from pathlib import Path
from datetime import datetime, timezone


print("=" * 120)
print("STAGE25-5 — FINAL AUDIT + SCIENTIFIC SEAL + PUBLICATION CLOSEOUT")
print("=" * 120)
print()


# ==============================================================================
# 0. FROZEN ANCHORS
# ==============================================================================

REPO = Path(
    "/kaggle/working/ids2018-validation-safe-ablation"
)

EXPECTED_PARENT = (
    "7820b9865a08f78107673207480c54d8dd0fe3eb"
)

STAGE24_CLOSEOUT_COMMIT = (
    "ad5a01ae9021183f6c5b8046c2647fd5dad7cb6d"
)

STAGE25_0_COMMIT = (
    "988fc5dd85018659749466ad9f8a1efcd5723ca9"
)

STAGE25_1_COMMIT = (
    "bfcc41741e055356c82f8f2f04042f3c2556b090"
)

STAGE25_2_COMMIT = (
    "e905a490aa6b7fdd3c22b021b11de270c9b57784"
)

STAGE25_3_COMMIT = (
    "5d1f9b2437ed7731f375acf01667c0faac57494e"
)

STAGE25_4_COMMIT = (
    "7820b9865a08f78107673207480c54d8dd0fe3eb"
)


EXPECTED_STAGE25_0_FREEZE_SHA = (
    "d231af1e4f07363c4d932acc99e1052e3b33bd2d24ca22e4386f4c7c378827b7"
)

EXPECTED_STAGE25_1_RESULT_SHA = (
    "81e4d96494c3432745f97428b722cc8870f75372a2c4570653ec59e7bcaa25ff"
)

EXPECTED_STAGE25_2_RESULT_SHA = (
    "1e3e66eb1dcf416585fd3f0fada8675b6950fde5f3f45af006a25b1aec872737"
)

EXPECTED_STAGE25_3_RESULT_SHA = (
    "f7c59d81d1532e0a61461bc9f213e9947b5edfe15fd2f8d9eb5d10d0f6bf6732"
)

EXPECTED_STAGE25_4_RESULT_SHA = (
    "8fcc28f0ce2a616a166f22f4a33d0c76001f8ef9a337739bd32c14778932c205"
)


STAGE25_BASE = (
    REPO
    / "results"
    / "stage25_prevalence_stress"
)

LOCK_DIR = (
    STAGE25_BASE
    / "stage25_0_protocol_lock"
)

S1_DIR = (
    STAGE25_BASE
    / "stage25_1_bayesian_projection"
)

S2_DIR = (
    STAGE25_BASE
    / "stage25_2_traffic_soc_capacity"
)

S3_DIR = (
    STAGE25_BASE
    / "stage25_3_break_even_analysis"
)

S4_DIR = (
    STAGE25_BASE
    / "stage25_4_benchmark_operational_translation"
)

FINAL_DIR = (
    STAGE25_BASE
    / "stage25_5_final_audit_and_seal"
)

PUB_DIR = (
    STAGE25_BASE
    / "stage25_publication_package"
)

PUB_TABLE_DIR = (
    PUB_DIR
    / "tables"
)

FIG_DIR = (
    REPO
    / "figures"
    / "stage25_prevalence_stress"
)

SCRIPT_DIR = (
    REPO
    / "scripts"
    / "stage25"
)

DOC_DIR = (
    REPO
    / "docs"
)


# ------------------------------------------------------------------------------
# Frozen protocol / stage results
# ------------------------------------------------------------------------------

FREEZE_RECORD = (
    LOCK_DIR
    / "freeze_record.json"
)

FIGURE_PLAN = (
    LOCK_DIR
    / "figure_plan.json"
)

SANITY_PLAN = (
    LOCK_DIR
    / "sanity_test_plan.json"
)

ANTI_ADAPTATION = (
    LOCK_DIR
    / "anti_adaptation.json"
)

UNCERTAINTY_POLICY = (
    LOCK_DIR
    / "uncertainty_policy.json"
)

PROHIBITED_CLAIMS = (
    LOCK_DIR
    / "prohibited_claims.json"
)


S1_RESULT = (
    S1_DIR
    / "stage25_1_bayesian_projection_result.json"
)

S2_RESULT = (
    S2_DIR
    / "stage25_2_traffic_soc_capacity_result.json"
)

S3_RESULT = (
    S3_DIR
    / "stage25_3_break_even_result.json"
)

S4_RESULT = (
    S4_DIR
    / "stage25_4_translation_result.json"
)


S1_SANITY = (
    S1_DIR
    / "stage25_1_sanity_tests.json"
)

S2_SANITY = (
    S2_DIR
    / "stage25_2_sanity_tests.json"
)

S3_SANITY = (
    S3_DIR
    / "stage25_3_sanity_tests.json"
)

S4_SANITY = (
    S4_DIR
    / "stage25_4_complete_sanity_audit.json"
)


MASTER_CSV = (
    S4_DIR
    / "stage25_4_master_projection_matrix.csv"
)

TRANSLATION_CSV = (
    S4_DIR
    / "stage25_4_benchmark_to_operational_translation_0p1pct.csv"
)

LOW_PREVALENCE_CSV = (
    S4_DIR
    / "stage25_4_low_prevalence_summary.csv"
)

FIGURE_MANIFEST = (
    S4_DIR
    / "stage25_4_figure_manifest.json"
)

COST_BREAK_EVEN_CSV = (
    S3_DIR
    / "cost_break_even_points.csv"
)


README = (
    REPO
    / "README.md"
)

JOURNAL_SUMMARY = (
    DOC_DIR
    / "JOURNAL_EXTENSION_SUMMARY.md"
)


# ==============================================================================
# 1. HELPERS
# ==============================================================================

def run_cmd(
    args,
    *,
    cwd=None,
    check=True,
):

    p = subprocess.run(
        [str(x) for x in args],
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    if check and p.returncode != 0:

        raise RuntimeError(
            "\nCommand failed:\n"
            +
            " ".join(
                str(x)
                for x in args
            )
            +
            "\n\n"
            +
            (
                p.stdout
                or
                ""
            )
        )

    return (
        p.stdout
        or
        ""
    ).strip()


def git_cmd(
    *args,
    auth_header=None,
    check=True,
):

    cmd = [
        "git"
    ]

    if auth_header is not None:

        cmd += [
            "-c",
            "credential.helper=",
            "-c",
            f"http.extraHeader=AUTHORIZATION: Basic {auth_header}",
        ]

    cmd += [
        str(x)
        for x in args
    ]

    return run_cmd(
        cmd,
        cwd=REPO,
        check=check,
    )


def sha256_file(
    path,
):

    path = Path(
        path
    )

    h = hashlib.sha256()

    with path.open(
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

    return h.hexdigest()


def load_json(
    path,
):

    path = Path(
        path
    )

    if not path.is_file():

        raise RuntimeError(
            f"Missing JSON:\n{path}"
        )

    return json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )


def write_json(
    path,
    payload,
):

    path = Path(
        path
    )

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    path.write_text(
        json.dumps(
            payload,
            indent=2,
            sort_keys=True,
            ensure_ascii=False,
            allow_nan=False,
        )
        +
        "\n",
        encoding="utf-8",
    )


def write_text(
    path,
    text,
):

    path = Path(
        path
    )

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    path.write_text(
        str(
            text
        ).rstrip()
        +
        "\n",
        encoding="utf-8",
    )


def read_csv(
    path,
):

    path = Path(
        path
    )

    if not path.is_file():

        raise RuntimeError(
            f"Missing CSV:\n{path}"
        )

    with path.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as fh:

        return list(
            csv.DictReader(
                fh
            )
        )


def write_csv(
    path,
    rows,
):

    path = Path(
        path
    )

    rows = list(
        rows
    )

    if not rows:

        raise RuntimeError(
            f"Refusing empty CSV:\n{path}"
        )

    fields = list(
        rows[
            0
        ].keys()
    )

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as fh:

        writer = csv.DictWriter(
            fh,
            fieldnames=fields,
            lineterminator="\n",
        )

        writer.writeheader()

        for row in rows:

            if list(
                row.keys()
            ) != fields:

                raise RuntimeError(
                    f"Inconsistent CSV schema:\n{path}"
                )

            writer.writerow(
                row
            )


def optional_float(
    value,
):

    if value is None:

        return None

    value = str(
        value
    )

    if value == "":

        return None

    return float(
        value
    )


def optional_string(
    value,
):

    if value is None:

        return None

    value = str(
        value
    )

    if value == "":

        return None

    return value


def assert_close(
    actual,
    expected,
    *,
    atol=1e-12,
    label="value",
):

    if not math.isclose(
        float(
            actual
        ),
        float(
            expected
        ),
        rel_tol=0.0,
        abs_tol=atol,
    ):

        raise RuntimeError(
            "\nNumerical identity failure.\n"
            f"{label}\n"
            f"Expected: {expected!r}\n"
            f"Actual:   {actual!r}\n"
            f"Delta:    "
            f"{float(actual)-float(expected):+.17e}"
        )


def verify_sha(
    path,
    expected,
    label,
):

    actual = sha256_file(
        path
    )

    if actual != expected:

        raise RuntimeError(
            f"\n{label} SHA mismatch.\n"
            f"Expected: {expected}\n"
            f"Actual:   {actual}\n"
            f"Path:     {path}"
        )

    return actual


def verify_declared_artifacts(
    result,
):

    count = 0

    for relative_path, expected_sha in result[
        "artifacts"
    ].items():

        path = (
            REPO
            /
            relative_path
        )

        if not path.is_file():

            raise RuntimeError(
                f"Missing declared artifact:\n{relative_path}"
            )

        actual_sha = sha256_file(
            path
        )

        if actual_sha != expected_sha:

            raise RuntimeError(
                "\nDeclared artifact SHA mismatch.\n"
                f"Artifact: {relative_path}\n"
                f"Expected: {expected_sha}\n"
                f"Actual:   {actual_sha}"
            )

        count += 1

    return count


def append_once(
    path,
    marker,
    block,
):

    path = Path(
        path
    )

    text = path.read_text(
        encoding="utf-8"
    )

    if marker in text:

        raise RuntimeError(
            f"Closeout marker already exists in {path.name}."
        )

    text = (
        text.rstrip()
        +
        "\n\n"
        +
        marker
        +
        "\n"
        +
        block.strip()
        +
        "\n"
    )

    path.write_text(
        text,
        encoding="utf-8",
    )


def latex_escape(
    text,
):

    text = str(
        text
    )

    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }

    result = ""

    for char in text:

        result += replacements.get(
            char,
            char,
        )

    return result


def markdown_table(
    rows,
    columns,
):

    header = (
        "| "
        +
        " | ".join(
            label
            for _, label in columns
        )
        +
        " |"
    )

    separator = (
        "| "
        +
        " | ".join(
            "---"
            for _ in columns
        )
        +
        " |"
    )

    lines = [
        header,
        separator,
    ]

    for row in rows:

        values = []

        for key, _ in columns:

            value = row[
                key
            ]

            values.append(
                str(
                    value
                )
            )

        lines.append(
            "| "
            +
            " | ".join(
                values
            )
            +
            " |"
        )

    return "\n".join(
        lines
    )


def normalize_source(
    source,
):

    if source is None:

        return ""

    if isinstance(
        source,
        list,
    ):

        return "".join(
            str(x)
            for x in source
        )

    return str(
        source
    )


def sanitize_source(
    source,
):

    source = normalize_source(
        source
    )

    token_patterns = [
        r"ghp_[A-Za-z0-9]{20,}",
        r"github_pat_[A-Za-z0-9_]{20,}",
        r"gho_[A-Za-z0-9]{20,}",
        r"ghu_[A-Za-z0-9]{20,}",
        r"ghs_[A-Za-z0-9]{20,}",
        r"ghr_[A-Za-z0-9]{20,}",
    ]

    for pattern in token_patterns:

        source = re.sub(
            pattern,
            "REDACTED_GITHUB_TOKEN",
            source,
        )

    return source


def friendly_cell(
    cell_id,
):

    mapping = {
        "STAGE22_RANDOM":
            "Stage22 Random",

        "STAGE22_CHRONOLOGICAL":
            "Stage22 Chronological",

        "STAGE24_2018_TO_2017_BRIDGE62_PUBLISHED":
            "IDS2018→CICIDS2017 B62 Published",

        "STAGE24_2018_TO_2017_BRIDGE62_FLAG_CORRECTED":
            "IDS2018→CICIDS2017 B62 Corrected",

        "STAGE24_2018_TO_2017_BRIDGE70_PUBLISHED":
            "IDS2018→CICIDS2017 B70 Published",

        "STAGE24_2018_TO_2017_BRIDGE70_FLAG_CORRECTED":
            "IDS2018→CICIDS2017 B70 Corrected",

        "STAGE24_2017_TO_2018_BRIDGE62":
            "CICIDS2017→IDS2018 B62",

        "STAGE24_2017_TO_2018_BRIDGE70":
            "CICIDS2017→IDS2018 B70",
    }

    if cell_id not in mapping:

        raise RuntimeError(
            f"Unknown cell: {cell_id}"
        )

    return mapping[
        cell_id
    ]


CELL_ORDER = [
    "STAGE22_RANDOM",
    "STAGE22_CHRONOLOGICAL",
    "STAGE24_2018_TO_2017_BRIDGE62_PUBLISHED",
    "STAGE24_2018_TO_2017_BRIDGE62_FLAG_CORRECTED",
    "STAGE24_2018_TO_2017_BRIDGE70_PUBLISHED",
    "STAGE24_2018_TO_2017_BRIDGE70_FLAG_CORRECTED",
    "STAGE24_2017_TO_2018_BRIDGE62",
    "STAGE24_2017_TO_2018_BRIDGE70",
]

OP_ORDER = [
    "STANDARD",
    "BALANCED",
    "SECURITY",
]

FAMILY_ORDER = [
    "STAGE22_RANDOM",
    "STAGE22_CHRONOLOGICAL",
    "STAGE24_2018_TO_2017",
    "STAGE24_2017_TO_2018",
]


# ==============================================================================
# 2. GOVERNANCE GATE
# ==============================================================================

print("=" * 120)
print("GOVERNANCE GATE")
print("=" * 120)


head = git_cmd(
    "rev-parse",
    "HEAD",
)


status = git_cmd(
    "status",
    "--porcelain",
)


print(
    "HEAD:",
    head,
)


if head != EXPECTED_PARENT:

    raise RuntimeError(
        "\nUnexpected Stage25-5 parent.\n"
        f"Expected: {EXPECTED_PARENT}\n"
        f"Actual:   {head}"
    )


if status:

    raise RuntimeError(
        "\nRepository must be clean before Stage25-5:\n"
        +
        status
    )


for path in [
    FINAL_DIR,
    PUB_DIR,
]:

    if path.exists():

        existing = list(
            path.iterdir()
        )

        if existing:

            raise RuntimeError(
                f"\nUnexpected existing closeout artifacts:\n{path}"
            )


for path in [
    SCRIPT_DIR
    / "stage25_prevalence_operational_stress.ipynb",

    SCRIPT_DIR
    / "stage25_prevalence_operational_stress.py",
]:

    if path.exists():

        raise RuntimeError(
            f"Stage25 export already exists:\n{path}"
        )


print(
    "[PASS] Exact Stage25-4 parent."
)

print(
    "[PASS] Repository clean."
)

print()


# ==============================================================================
# 3. COMMIT-CHAIN AUDIT
# ==============================================================================

print("=" * 120)
print("STAGE25 COMMIT-CHAIN AUDIT")
print("=" * 120)


expected_chain = [
    (
        STAGE25_0_COMMIT,
        STAGE24_CLOSEOUT_COMMIT,
        "Stage25-0",
    ),
    (
        STAGE25_1_COMMIT,
        STAGE25_0_COMMIT,
        "Stage25-1",
    ),
    (
        STAGE25_2_COMMIT,
        STAGE25_1_COMMIT,
        "Stage25-2",
    ),
    (
        STAGE25_3_COMMIT,
        STAGE25_2_COMMIT,
        "Stage25-3",
    ),
    (
        STAGE25_4_COMMIT,
        STAGE25_3_COMMIT,
        "Stage25-4",
    ),
]


commit_chain_receipts = []


for commit_sha, expected_parent, stage_name in expected_chain:

    actual_commit = git_cmd(
        "rev-parse",
        commit_sha,
    )

    if actual_commit != commit_sha:

        raise RuntimeError(
            f"{stage_name}: commit resolution mismatch."
        )


    actual_parent = git_cmd(
        "rev-parse",
        f"{commit_sha}^",
    )


    if actual_parent != expected_parent:

        raise RuntimeError(
            "\nStage25 commit ancestry mismatch.\n"
            f"Stage:    {stage_name}\n"
            f"Commit:   {commit_sha}\n"
            f"Expected parent: {expected_parent}\n"
            f"Actual parent:   {actual_parent}"
        )


    commit_chain_receipts.append(
        {
            "stage":
                stage_name,

            "commit":
                commit_sha,

            "parent":
                actual_parent,

            "passed":
                True,
        }
    )


print(
    "[PASS] Stage24 closeout -> Stage25-0 -> 1 -> 2 -> 3 -> 4 is strictly linear."
)

print()


# ==============================================================================
# 4. FROZEN RESULT SHA AUDIT
# ==============================================================================

print("=" * 120)
print("FROZEN RESULT SHA AUDIT")
print("=" * 120)


freeze_sha = verify_sha(
    FREEZE_RECORD,
    EXPECTED_STAGE25_0_FREEZE_SHA,
    "Stage25-0 freeze record",
)


s1_sha = verify_sha(
    S1_RESULT,
    EXPECTED_STAGE25_1_RESULT_SHA,
    "Stage25-1 result",
)


s2_sha = verify_sha(
    S2_RESULT,
    EXPECTED_STAGE25_2_RESULT_SHA,
    "Stage25-2 result",
)


s3_sha = verify_sha(
    S3_RESULT,
    EXPECTED_STAGE25_3_RESULT_SHA,
    "Stage25-3 result",
)


s4_sha = verify_sha(
    S4_RESULT,
    EXPECTED_STAGE25_4_RESULT_SHA,
    "Stage25-4 result",
)


print(
    "Stage25-0:",
    freeze_sha,
)

print(
    "Stage25-1:",
    s1_sha,
)

print(
    "Stage25-2:",
    s2_sha,
)

print(
    "Stage25-3:",
    s3_sha,
)

print(
    "Stage25-4:",
    s4_sha,
)

print()

print(
    "[PASS] All frozen Stage25 result anchors exact."
)

print()


# ==============================================================================
# 5. DECLARED ARTIFACT + SCIENTIFIC ACCESS AUDIT
# ==============================================================================

print("=" * 120)
print("SCIENTIFIC ACCESS + ARTIFACT AUDIT")
print("=" * 120)


stage_results = {
    "Stage25-1":
        load_json(
            S1_RESULT
        ),

    "Stage25-2":
        load_json(
            S2_RESULT
        ),

    "Stage25-3":
        load_json(
            S3_RESULT
        ),

    "Stage25-4":
        load_json(
            S4_RESULT
        ),
}


declared_artifact_count = 0


for stage_name, result in stage_results.items():

    declared_artifact_count += verify_declared_artifacts(
        result
    )


    for key, value in result[
        "scientific_access"
    ].items():

        if int(
            value
        ) != 0:

            raise RuntimeError(
                "\nScientific-access violation.\n"
                f"Stage: {stage_name}\n"
                f"{key}={value}"
            )


print(
    "Declared artifacts verified:",
    declared_artifact_count,
)

print(
    "[PASS] Model fits:            0"
)

print(
    "[PASS] Model inference:       0"
)

print(
    "[PASS] Probability arrays:    0"
)

print(
    "[PASS] Target reopenings:     0"
)

print(
    "[PASS] Threshold searches:    0"
)

print(
    "[PASS] Calibration runs:      0"
)

print()


# ==============================================================================
# 6. SANITY + FIGURE AUDIT
# ==============================================================================

print("=" * 120)
print("SANITY + FIGURE AUDIT")
print("=" * 120)


s4_sanity = load_json(
    S4_SANITY
)


if (
    s4_sanity[
        "status"
    ]
    !=
    "ALL_PREREGISTERED_SANITY_TESTS_PASS"
):

    raise RuntimeError(
        "Stage25-4 sanity status changed."
    )


if int(
    s4_sanity[
        "frozen_test_count"
    ]) != 7:

    raise RuntimeError(
        "Frozen sanity-test count changed."
    )


for name, receipt in s4_sanity[
    "tests"
].items():

    if receipt[
        "passed"
    ] is not True:

        raise RuntimeError(
            f"Sanity test failed: {name}"
        )


figure_manifest = load_json(
    FIGURE_MANIFEST
)


if (
    figure_manifest[
        "frozen_figure_plan_status"
    ]
    !=
    "ALL_REQUIRED_FIGURES_GENERATED"
):

    raise RuntimeError(
        "Stage25 figure completeness changed."
    )


if figure_manifest[
    "outcome_based_figure_dropping"
] is not False:

    raise RuntimeError(
        "Outcome-based figure selection detected."
    )


expected_figure_ids = {
    "25-A",
    "25-B",
    "25-C",
    "25-D",
    "25-E",
}


if set(
    figure_manifest[
        "figures"
    ].keys()
) != expected_figure_ids:

    raise RuntimeError(
        "Frozen figure inventory changed."
    )


figure_files_verified = 0


for figure_id, formats in figure_manifest[
    "figures"
].items():

    for fmt in [
        "png",
        "svg",
    ]:

        relative_path = formats[
            fmt
        ][
            "path"
        ]

        expected_sha = formats[
            fmt
        ][
            "sha256"
        ]

        path = (
            REPO
            /
            relative_path
        )


        actual_sha = sha256_file(
            path
        )


        if actual_sha != expected_sha:

            raise RuntimeError(
                "\nFigure SHA mismatch.\n"
                f"{figure_id} / {fmt}\n"
                f"Expected: {expected_sha}\n"
                f"Actual:   {actual_sha}"
            )


        figure_files_verified += 1


if figure_files_verified != 10:

    raise RuntimeError(
        "Expected 10 Stage25 figure files."
    )


print(
    "[PASS] All 7 preregistered sanity tests."
)

print(
    "[PASS] 5/5 preregistered figures."
)

print(
    "[PASS] 10/10 PNG/SVG files byte-verified."
)

print()


# ==============================================================================
# 7. LOAD FROZEN PUBLICATION MATRICES
# ==============================================================================

master_raw = read_csv(
    MASTER_CSV
)


translation_raw = read_csv(
    TRANSLATION_CSV
)


low_raw = read_csv(
    LOW_PREVALENCE_CSV
)


break_even_raw = read_csv(
    COST_BREAK_EVEN_CSV
)


if len(
    master_raw
) != 144:

    raise RuntimeError(
        "Master projection matrix must remain 144 rows."
    )


if len(
    translation_raw
) != 24:

    raise RuntimeError(
        "Translation table must remain 24 rows."
    )


if len(
    low_raw
) != 48:

    raise RuntimeError(
        "Low-prevalence table must remain 48 rows."
    )


if len(
    break_even_raw
) != 24:

    raise RuntimeError(
        "Cost break-even table must remain 24 rows."
    )


print(
    "Master rows:           ",
    len(
        master_raw
    ),
)

print(
    "0.1% translation rows: ",
    len(
        translation_raw
    ),
)

print(
    "Low-prevalence rows:   ",
    len(
        low_raw
    ),
)

print(
    "Break-even rows:       ",
    len(
        break_even_raw
    ),
)

print()


# ==============================================================================
# 8. NORMALIZE 0.1% TRANSLATION TABLE
# ==============================================================================

translation = []


for raw in translation_raw:

    translation.append(
        {
            "cell_id":
                raw[
                    "cell_id"
                ],

            "family":
                raw[
                    "family"
                ],

            "direction":
                raw[
                    "direction"
                ],

            "bridge":
                raw[
                    "bridge"
                ],

            "variant":
                raw[
                    "variant"
                ],

            "operating_point":
                raw[
                    "operating_point"
                ],

            "threshold":
                float(
                    raw[
                        "threshold"
                    ]
                ),

            "observed_f1":
                optional_float(
                    raw[
                        "observed_f1"
                    ]
                ),

            "observed_precision":
                float(
                    raw[
                        "observed_precision"
                    ]
                ),

            "observed_recall_tpr":
                float(
                    raw[
                        "observed_recall_tpr"
                    ]
                ),

            "observed_fpr":
                float(
                    raw[
                        "observed_fpr"
                    ]
                ),

            "observed_prevalence":
                float(
                    raw[
                        "observed_prevalence"
                    ]
                ),

            "projection_prevalence":
                float(
                    raw[
                        "projection_prevalence"
                    ]
                ),

            "projected_ppv":
                float(
                    raw[
                        "projected_ppv"
                    ]
                ),

            "projected_fp_per_day":
                float(
                    raw[
                        "projected_fp_per_day"
                    ]
                ),

            "projected_tp_per_day":
                float(
                    raw[
                        "projected_tp_per_day"
                    ]
                ),

            "projected_total_alerts_per_day":
                float(
                    raw[
                        "projected_total_alerts_per_day"
                    ]
                ),

            "projected_alert_processing_hours_per_day":
                float(
                    raw[
                        "projected_alert_processing_hours_per_day"
                    ]
                ),

            "projected_aci_1":
                float(
                    raw[
                        "projected_aci_1"
                    ]
                ),

            "projected_aci_3":
                float(
                    raw[
                        "projected_aci_3"
                    ]
                ),

            "projected_aci_10":
                float(
                    raw[
                        "projected_aci_10"
                    ]
                ),

            "projected_relative_cost_decision":
                raw[
                    "projected_relative_cost_decision"
                ],

            "cost_break_even_prevalence":
                float(
                    raw[
                        "cost_break_even_prevalence"
                    ]
                ),
        }
    )


translation = sorted(
    translation,
    key=lambda row:
        (
            CELL_ORDER.index(
                row[
                    "cell_id"
                ]
            ),
            OP_ORDER.index(
                row[
                    "operating_point"
                ]
            ),
        ),
)


# ==============================================================================
# 9. EXACT HEADLINE RECEIPTS
# ==============================================================================

def find_translation(
    cell_id,
    operating_point,
):

    rows = [
        row
        for row in translation
        if (
            row[
                "cell_id"
            ]
            ==
            cell_id
            and
            row[
                "operating_point"
            ]
            ==
            operating_point
        )
    ]

    if len(
        rows
    ) != 1:

        raise RuntimeError(
            f"Translation lookup not unique: {cell_id}/{operating_point}"
        )

    return rows[
        0
    ]


random_std = find_translation(
    "STAGE22_RANDOM",
    "STANDARD",
)


random_bal = find_translation(
    "STAGE22_RANDOM",
    "BALANCED",
)


random_sec = find_translation(
    "STAGE22_RANDOM",
    "SECURITY",
)


chron_std = find_translation(
    "STAGE22_CHRONOLOGICAL",
    "STANDARD",
)


chron_bal = find_translation(
    "STAGE22_CHRONOLOGICAL",
    "BALANCED",
)


primary_standard = [
    row
    for row in translation
    if (
        row[
            "family"
        ]
        ==
        "STAGE24_2018_TO_2017"
        and
        row[
            "operating_point"
        ]
        ==
        "STANDARD"
    )
]


primary_balanced = [
    row
    for row in translation
    if (
        row[
            "family"
        ]
        ==
        "STAGE24_2018_TO_2017"
        and
        row[
            "operating_point"
        ]
        ==
        "BALANCED"
    )
]


secondary_standard = [
    row
    for row in translation
    if (
        row[
            "family"
        ]
        ==
        "STAGE24_2017_TO_2018"
        and
        row[
            "operating_point"
        ]
        ==
        "STANDARD"
    )
]


secondary_all = [
    row
    for row in translation
    if row[
        "family"
    ]
    ==
    "STAGE24_2017_TO_2018"
]


primary_standard_ppv_min = min(
    row[
        "projected_ppv"
    ]
    for row in primary_standard
)


primary_standard_ppv_max = max(
    row[
        "projected_ppv"
    ]
    for row in primary_standard
)


primary_standard_hours_min = min(
    row[
        "projected_alert_processing_hours_per_day"
    ]
    for row in primary_standard
)


primary_standard_hours_max = max(
    row[
        "projected_alert_processing_hours_per_day"
    ]
    for row in primary_standard
)


primary_balanced_ppv_min = min(
    row[
        "projected_ppv"
    ]
    for row in primary_balanced
)


primary_balanced_ppv_max = max(
    row[
        "projected_ppv"
    ]
    for row in primary_balanced
)


primary_balanced_hours_min = min(
    row[
        "projected_alert_processing_hours_per_day"
    ]
    for row in primary_balanced
)


primary_balanced_hours_max = max(
    row[
        "projected_alert_processing_hours_per_day"
    ]
    for row in primary_balanced
)


secondary_standard_ppv_min = min(
    row[
        "projected_ppv"
    ]
    for row in secondary_standard
)


secondary_standard_ppv_max = max(
    row[
        "projected_ppv"
    ]
    for row in secondary_standard
)


secondary_tp_min = min(
    row[
        "projected_tp_per_day"
    ]
    for row in secondary_all
)


secondary_tp_max = max(
    row[
        "projected_tp_per_day"
    ]
    for row in secondary_all
)


# ------------------------------------------------------------------------------
# Frozen Stage25-3 cost summary.
# ------------------------------------------------------------------------------

s3_result = load_json(
    S3_RESULT
)


cost_summary = s3_result[
    "cost_decision_summary"
][
    "all_operating_points"
]


cost_0p1 = cost_summary[
    "0.001"
]


cost_0p01 = cost_summary[
    "0.0001"
]


if (
    int(
        cost_0p1[
            "model_lower_count"
        ]
    )
    !=
    15
):

    raise RuntimeError(
        "Unexpected 0.1% cost-decision count."
    )


if (
    int(
        cost_0p01[
            "model_lower_count"
        ]
    )
    !=
    3
):

    raise RuntimeError(
        "Unexpected 0.01% cost-decision count."
    )


# ------------------------------------------------------------------------------
# Cost break-even ranges by family.
# ------------------------------------------------------------------------------

break_even = []


for raw in break_even_raw:

    break_even.append(
        {
            "cell_id":
                raw[
                    "cell_id"
                ],

            "family":
                raw[
                    "family"
                ],

            "operating_point":
                raw[
                    "operating_point"
                ],

            "prevalence":
                float(
                    raw[
                        "cost_break_even_prevalence"
                    ]
                ),

            "percent":
                float(
                    raw[
                        "cost_break_even_percent"
                    ]
                ),
        }
    )


family_break_even = {}


for family in FAMILY_ORDER:

    rows = [
        row
        for row in break_even
        if row[
            "family"
        ]
        ==
        family
    ]


    family_break_even[
        family
    ] = {
        "min_prevalence":
            min(
                row[
                    "prevalence"
                ]
                for row in rows
            ),

        "max_prevalence":
            max(
                row[
                    "prevalence"
                ]
                for row in rows
            ),

        "min_percent":
            min(
                row[
                    "percent"
                ]
                for row in rows
            ),

        "max_percent":
            max(
                row[
                    "percent"
                ]
                for row in rows
            ),

        "operating_points":
            len(
                rows
            ),
    }


print("=" * 120)
print("HEADLINE FROZEN FINDINGS")
print("=" * 120)

print(
    "Stage22 random STANDARD @ 0.1%:"
)

print(
    f"  PPV:       {random_std['projected_ppv']:.6f}"
)

print(
    f"  FP/day:    {random_std['projected_fp_per_day']:.2f}"
)

print(
    f"  TP/day:    {random_std['projected_tp_per_day']:.2f}"
)

print(
    f"  Hours/day: {random_std['projected_alert_processing_hours_per_day']:.2f}"
)

print()

print(
    "Stage22 chronological STANDARD @ 0.1%:"
)

print(
    f"  PPV:       {chron_std['projected_ppv']:.9f}"
)

print(
    f"  TP/day:    {chron_std['projected_tp_per_day']:.6f}"
)

print(
    f"  FP/day:    {chron_std['projected_fp_per_day']:.2f}"
)

print()

print(
    "IDS2018 -> CICIDS2017 STANDARD @ 0.1%:"
)

print(
    f"  PPV range: {primary_standard_ppv_min:.6f} .. {primary_standard_ppv_max:.6f}"
)

print(
    f"  workload:  {primary_standard_hours_min:.2f} .. {primary_standard_hours_max:.2f} hours/day"
)

print()

print(
    "CICIDS2017 -> IDS2018 STANDARD @ 0.1%:"
)

print(
    f"  PPV range: {secondary_standard_ppv_min:.9f} .. {secondary_standard_ppv_max:.9f}"
)

print()

print(
    "Relative cost @ 0.1%:"
)

print(
    f"  model lower:  {cost_0p1['model_lower_count']} / 24"
)

print(
    f"  ignore lower: {cost_0p1['ignore_lower_count']} / 24"
)

print()

print(
    "Relative cost @ 0.01%:"
)

print(
    f"  model lower:  {cost_0p01['model_lower_count']} / 24"
)

print(
    f"  ignore lower: {cost_0p01['ignore_lower_count']} / 24"
)

print()


# ==============================================================================
# 10. PUBLICATION TABLES
# ==============================================================================

print("=" * 120)
print("PUBLICATION TABLES")
print("=" * 120)


PUB_TABLE_DIR.mkdir(
    parents=True,
    exist_ok=False,
)


# ------------------------------------------------------------------------------
# Table 25-1 — STANDARD operating point translation at 0.1%.
# ------------------------------------------------------------------------------

table1_rows = []


for row in translation:

    if row[
        "operating_point"
    ] != "STANDARD":

        continue


    table1_rows.append(
        {
            "evaluation_cell":
                friendly_cell(
                    row[
                        "cell_id"
                    ]
                ),

            "threshold":
                row[
                    "threshold"
                ],

            "observed_f1":
                row[
                    "observed_f1"
                ],

            "observed_precision":
                row[
                    "observed_precision"
                ],

            "observed_tpr":
                row[
                    "observed_recall_tpr"
                ],

            "observed_fpr":
                row[
                    "observed_fpr"
                ],

            "observed_prevalence":
                row[
                    "observed_prevalence"
                ],

            "projected_prevalence":
                row[
                    "projection_prevalence"
                ],

            "projected_ppv":
                row[
                    "projected_ppv"
                ],

            "projected_fp_per_day":
                row[
                    "projected_fp_per_day"
                ],

            "projected_tp_per_day":
                row[
                    "projected_tp_per_day"
                ],

            "projected_alerts_per_day":
                row[
                    "projected_total_alerts_per_day"
                ],

            "projected_hours_per_day":
                row[
                    "projected_alert_processing_hours_per_day"
                ],

            "cost_decision":
                row[
                    "projected_relative_cost_decision"
                ],
        }
    )


if len(
    table1_rows
) != 8:

    raise RuntimeError(
        "Table25-1 must contain eight STANDARD rows."
    )


TABLE1_CSV = (
    PUB_TABLE_DIR
    / "table25_1_standard_operational_translation_0p1pct.csv"
)


write_csv(
    TABLE1_CSV,
    table1_rows,
)


# ------------------------------------------------------------------------------
# Table 25-2 — all 24 operating points at 0.1%.
# ------------------------------------------------------------------------------

table2_rows = []


for row in translation:

    table2_rows.append(
        {
            "evaluation_cell":
                friendly_cell(
                    row[
                        "cell_id"
                    ]
                ),

            "operating_point":
                row[
                    "operating_point"
                ],

            "threshold":
                row[
                    "threshold"
                ],

            "tpr":
                row[
                    "observed_recall_tpr"
                ],

            "fpr":
                row[
                    "observed_fpr"
                ],

            "observed_precision":
                row[
                    "observed_precision"
                ],

            "projected_ppv_at_0p1pct":
                row[
                    "projected_ppv"
                ],

            "fp_per_day":
                row[
                    "projected_fp_per_day"
                ],

            "tp_per_day":
                row[
                    "projected_tp_per_day"
                ],

            "alerts_per_day":
                row[
                    "projected_total_alerts_per_day"
                ],

            "processing_hours_per_day":
                row[
                    "projected_alert_processing_hours_per_day"
                ],

            "aci_1":
                row[
                    "projected_aci_1"
                ],

            "aci_3":
                row[
                    "projected_aci_3"
                ],

            "aci_10":
                row[
                    "projected_aci_10"
                ],

            "relative_cost_decision":
                row[
                    "projected_relative_cost_decision"
                ],
        }
    )


TABLE2_CSV = (
    PUB_TABLE_DIR
    / "table25_2_all_operating_points_0p1pct.csv"
)


write_csv(
    TABLE2_CSV,
    table2_rows,
)


# ------------------------------------------------------------------------------
# Table 25-3 — exact 24 cost break-even points.
# ------------------------------------------------------------------------------

table3_rows = []


for row in sorted(
    break_even,
    key=lambda row:
        (
            CELL_ORDER.index(
                row[
                    "cell_id"
                ]
            ),
            OP_ORDER.index(
                row[
                    "operating_point"
                ]
            ),
        ),
):

    table3_rows.append(
        {
            "evaluation_cell":
                friendly_cell(
                    row[
                        "cell_id"
                    ]
                ),

            "operating_point":
                row[
                    "operating_point"
                ],

            "cost_break_even_prevalence":
                row[
                    "prevalence"
                ],

            "cost_break_even_percent":
                row[
                    "percent"
                ],
        }
    )


TABLE3_CSV = (
    PUB_TABLE_DIR
    / "table25_3_exact_cost_break_even.csv"
)


write_csv(
    TABLE3_CSV,
    table3_rows,
)


# ------------------------------------------------------------------------------
# Table 25-4 — family-level relative-cost decision counts.
# ------------------------------------------------------------------------------

table4_rows = []


s3_family_cost = s3_result[
    "cost_decision_summary"
][
    "by_family"
]


for family in FAMILY_ORDER:

    prevalence_keys = sorted(
        s3_family_cost[
            family
        ].keys(),
        key=float,
        reverse=True,
    )


    for prevalence_key in prevalence_keys:

        receipt = s3_family_cost[
            family
        ][
            prevalence_key
        ]


        table4_rows.append(
            {
                "family":
                    family,

                "projection_prevalence":
                    float(
                        prevalence_key
                    ),

                "operating_points":
                    int(
                        receipt[
                            "operating_points"
                        ]
                    ),

                "model_lower_count":
                    int(
                        receipt[
                            "model_lower_count"
                        ]
                    ),

                "ignore_lower_count":
                    int(
                        receipt[
                            "ignore_lower_count"
                        ]
                    ),

                "equal_count":
                    int(
                        receipt[
                            "equal_count"
                        ]
                    ),
            }
        )


TABLE4_CSV = (
    PUB_TABLE_DIR
    / "table25_4_family_relative_cost_decisions.csv"
)


write_csv(
    TABLE4_CSV,
    table4_rows,
)


# ------------------------------------------------------------------------------
# Table 25-5 — frozen sanity/governance.
# ------------------------------------------------------------------------------

table5_rows = []


for test_name, receipt in s4_sanity[
    "tests"
].items():

    table5_rows.append(
        {
            "audit_item":
                test_name,

            "source_stage":
                receipt[
                    "source_stage"
                ],

            "status":
                (
                    "PASS"
                    if receipt[
                        "passed"
                    ]
                    else
                    "FAIL"
                ),
        }
    )


TABLE5_CSV = (
    PUB_TABLE_DIR
    / "table25_5_preregistered_sanity_audit.csv"
)


write_csv(
    TABLE5_CSV,
    table5_rows,
)


for path in [
    TABLE1_CSV,
    TABLE2_CSV,
    TABLE3_CSV,
    TABLE4_CSV,
    TABLE5_CSV,
]:

    print(
        "[CREATED]",
        path.relative_to(
            REPO
        )
    )


print()


# ==============================================================================
# 11. PAPER-READY MANUSCRIPT TEXT
# ==============================================================================

print("=" * 120)
print("PAPER-READY RESULTS / DISCUSSION / LIMITATIONS / CONTRIBUTIONS")
print("=" * 120)


results_md = f"""
## Stage25 Results — Prevalence and Operational Stress

Stage25 translated the already-frozen Stage22 and Stage24 operating
characteristics into deployment-stress quantities without model refitting,
new inference, target reopening, threshold re-selection, or calibration.
Twenty-four frozen operating points were evaluated across six
preregistered attack prevalences (10%, 3%, 1%, 0.3%, 0.1%, and 0.01%),
yielding 144 deterministic prior-shift projections.

At the preregistered 0.1% attack prevalence, the Stage22 random-natural
STANDARD operating point retained a PPV of
{random_std['projected_ppv']:.6f} despite the large reduction from its
observed prevalence of {random_std['observed_prevalence']:.6f}. Its very
low FPR ({random_std['observed_fpr']:.8f}) produced only
{random_std['projected_fp_per_day']:.1f} false alerts per one million
benign flows/day, while the frozen TPR ({random_std['observed_recall_tpr']:.6f})
projected {random_std['projected_tp_per_day']:.1f} true alerts/day.
Nevertheless, the combined workload was
{random_std['projected_alert_processing_hours_per_day']:.1f}
analyst-hours/day under the preregistered two-minute service-time
assumption. Thus, high PPV did not by itself imply low SOC workload.

The random-natural SECURITY operating point exposed the complementary
failure mode. Although its frozen recall increased to
{random_sec['observed_recall_tpr']:.6f}, its FPR of
{random_sec['observed_fpr']:.6f} generated
{random_sec['projected_fp_per_day']:.1f} false alerts/day at 0.1%
prevalence. PPV fell to {random_sec['projected_ppv']:.6f} and projected
workload rose to
{random_sec['projected_alert_processing_hours_per_day']:.1f}
hours/day. The result shows why a security-oriented recall objective does
not automatically satisfy a deployment-scale false-positive constraint.

Temporal validation produced a qualitatively different picture. The
Stage22 chronological STANDARD operating point fit easily within the
assumed analyst-capacity envelope, but only because its frozen TPR was
{chron_std['observed_recall_tpr']:.8f}. At 0.1% prevalence it projected
only {chron_std['projected_tp_per_day']:.4f} true detections/day against
{chron_std['projected_fp_per_day']:.1f} false alerts/day, yielding PPV
{chron_std['projected_ppv']:.9f}. Capacity feasibility therefore cannot
be interpreted as evidence of operational usefulness when detection has
collapsed.

The cross-dataset direction retained the Stage24 asymmetry. For
IDS2018→CICIDS2017 STANDARD operating points, projected PPV at 0.1%
ranged from {primary_standard_ppv_min:.6f} to
{primary_standard_ppv_max:.6f}, while projected workload ranged from
{primary_standard_hours_min:.1f} to
{primary_standard_hours_max:.1f} analyst-hours/day. For the corresponding
BALANCED operating points, PPV ranged from
{primary_balanced_ppv_min:.6f} to {primary_balanced_ppv_max:.6f} and
workload from {primary_balanced_hours_min:.1f} to
{primary_balanced_hours_max:.1f} hours/day. Hence substantial ranking
signal in the primary transfer direction did not translate into a
low-volume alert stream under the frozen deployment scenario.

The reverse CICIDS2017→IDS2018 direction remained operationally collapsed.
Its STANDARD projected PPV was only
{secondary_standard_ppv_min:.9f}–{secondary_standard_ppv_max:.9f} at
0.1% prevalence. Across all reverse-transfer frozen operating points,
projected true detections ranged only from {secondary_tp_min:.4f} to
{secondary_tp_max:.4f} per day under the fixed one-million-benign-flow
scenario. This extends the Stage24 directional asymmetry from ranking
metrics to deployment-facing quantities.

The relative-cost analysis further demonstrated the importance of the
base rate. Under the preregistered relative cost ratio
C_FP:C_FN = 1:100, 15 of 24 operating points had lower projected model
cost than the simplified ignore reference at 0.1% prevalence, whereas
only 3 of 24 remained lower-cost at 0.01%. The latter three were the
Stage22 random-natural operating points; the chronological and both
cross-dataset families favored the simplified ignore reference at that
extreme prevalence. These are relative operational cost units, not
financial-loss estimates.

Across Stage25, all seven preregistered sanity tests passed, all five
preregistered figures were retained, and no result-dependent figure,
threshold, prevalence point, capacity tier, traffic assumption, or cost
ratio was changed.
""".strip()


discussion_md = """
## Stage25 Discussion

Stage25 separates two mechanisms that are frequently conflated in IDS
evaluation. Stage22 and Stage24 demonstrate that temporal and domain
shift can alter the class-conditional operating characteristics
themselves, including TPR and FPR. Stage25 instead holds each frozen
operating point fixed and changes only the attack prior. The resulting
PPV cliffs therefore quantify base-rate sensitivity conditional on the
empirically observed operating point; they do not claim that TPR and FPR
would remain invariant in a real future network.

The projections show that very low FPR is the dominant prerequisite for
maintaining useful PPV when attacks are rare. This is visible even for
the strongest random-natural operating points: a threshold with high
recall but an FPR in the order of 10^-3 to 10^-2 can generate thousands
of false alerts per million benign flows and sharply reduce PPV. The
operational consequence is stronger than a benchmark F1 or ROC-oriented
summary alone suggests.

SOC capacity introduces a second distinction. An operating point may
have high PPV and still exceed a small analyst team because true alerts
also require service. Conversely, an operating point may fit comfortably
within capacity because it detects almost no attacks. Therefore,
capacity feasibility and detection usefulness are separate requirements,
and neither should be inferred from the other.

The Stage24 cross-dataset asymmetry remains visible after operational
translation. IDS2018→CICIDS2017 retained materially greater detection
utility than CICIDS2017→IDS2018, yet its frozen FPR still produced a heavy
false-alert workload at low prevalence. The reverse direction combined
weak TPR with non-negligible FPR, creating the least favorable
deployment-facing profile. This reinforces the need for bidirectional
cross-dataset testing rather than a single portability result.

Finally, the exact PPV and relative-cost break-even calculations provide
interpretable operating boundaries rather than grid-dependent graphical
approximations. They identify the prior-prevalence regimes in which a
frozen operating point changes character under the stated assumptions.
They should be read as conditional decision-analysis tools rather than
claims of universal deployment suitability.
""".strip()


limitations_md = """
## Stage25 Limitations and Threats to Validity

Stage25 is an analytic deployment-stress audit, not empirical production
validation. The primary assumption is prior-probability shift: within
each frozen operating point, TPR and FPR are held constant while attack
prevalence changes. Real networks may also exhibit covariate, concept,
protocol, topology, user-behavior, attacker, and extractor shift, all of
which can alter TPR and FPR.

The traffic scenario fixes benign volume at one million flows/day. This
is a transparent reference scale rather than a claim that one million
benign flows represents every enterprise. Likewise, two minutes per
alert and analyst tiers of one, three, and ten analyst-days are
preregistered reference scenarios rather than universal SOC constants.

The relative cost model uses C_FP=1 and C_FN=100 in dimensionless
relative operational cost units. These values are not currency, are not
financial-loss estimates, and do not imply that each malicious flow is
an independent compromise or breach. The simplified ignore comparator
is intentionally limited.

Stage25 projections are deterministic conditional transformations of
frozen empirical estimates. No complete joint TPR/FPR sampling
distribution was available for every inherited operating point, so
uncertainty in those empirical rates was not propagated through the
deployment projections and no new bootstrap was introduced.

The source datasets remain benchmark traffic captures rather than live
production SOC telemetry. Their age, traffic generation, attack mix,
feature-extractor semantics, and class structure constrain external
validity. Stage24 additionally could not evaluate the preregistered
GROUNDED_S4 cells because exact durable physical membership could not be
recovered without introducing a new heuristic; Stage25 correctly does
not manufacture a substitute for those cancelled cells.

No target-specific or prevalence-specific threshold optimization was
performed. Consequently, Stage25 evaluates the deployment implications
of the frozen validation-selected operating points, not the best
threshold that could be obtained after observing a deployment target.
""".strip()


contributions_md = """
## Stage25 Contributions

Stage25 contributes a validation-safe operational translation layer for
intrusion-detection evaluation. First, it converts frozen TPR/FPR
operating points into exact Bayesian PPV/NPV projections across a
predeclared low-prevalence grid without reopening targets or retuning
thresholds. Second, it translates the same operating points into
false-alert volume, true-alert volume, analyst workload, and explicit
SOC-capacity exceedance under a reproducible reference scenario. Third,
it derives analytic PPV, required-FPR, and relative-cost break-even
boundaries rather than relying on visually selected grid crossings.
Fourth, it links random, chronological, and bidirectional cross-dataset
results in one audit trail, showing how base-rate stress and
temporal/domain shift produce distinct but interacting deployment risks.
Finally, every assumption, operating point, figure, sanity test, and
artifact is preregistered or hash-frozen, preserving the study's
validation-safe governance through publication closeout.
""".strip()


MANUSCRIPT_MD = (
    DOC_DIR
    / "STAGE25_MANUSCRIPT_INTEGRATION.md"
)


write_text(
    MANUSCRIPT_MD,
    "\n\n".join(
        [
            "# Stage25 Manuscript Integration",
            results_md,
            discussion_md,
            limitations_md,
            contributions_md,
        ]
    ),
)


# ------------------------------------------------------------------------------
# LaTeX manuscript integration.
# ------------------------------------------------------------------------------

results_tex = f"""
\\subsection{{Prevalence and Operational Stress Results}}

Stage25 translated the already-frozen Stage22 and Stage24 operating
characteristics into deployment-stress quantities without model
refitting, new inference, target reopening, threshold re-selection, or
calibration. Twenty-four frozen operating points were evaluated across
six preregistered attack prevalences (10\\%, 3\\%, 1\\%, 0.3\\%, 0.1\\%,
and 0.01\\%), yielding 144 deterministic prior-shift projections.

At 0.1\\% prevalence, the Stage22 random-natural STANDARD operating point
retained PPV {random_std['projected_ppv']:.6f}, with
{random_std['projected_fp_per_day']:.1f} false alerts/day and
{random_std['projected_tp_per_day']:.1f} true alerts/day per one million
benign flows. The projected processing requirement was
{random_std['projected_alert_processing_hours_per_day']:.1f}
analyst-hours/day. The SECURITY operating point increased frozen recall
to {random_sec['observed_recall_tpr']:.6f}, but its FPR of
{random_sec['observed_fpr']:.6f} produced
{random_sec['projected_fp_per_day']:.1f} false alerts/day, reducing PPV
to {random_sec['projected_ppv']:.6f}.

The chronological STANDARD operating point projected PPV
{chron_std['projected_ppv']:.9f} and only
{chron_std['projected_tp_per_day']:.4f} true detections/day at 0.1\\%
prevalence. For IDS2018$\\rightarrow$CICIDS2017 STANDARD transfer,
projected PPV ranged from {primary_standard_ppv_min:.6f} to
{primary_standard_ppv_max:.6f}, whereas the reverse
CICIDS2017$\\rightarrow$IDS2018 STANDARD transfer yielded only
{secondary_standard_ppv_min:.9f}--{secondary_standard_ppv_max:.9f}.

Under the frozen relative-cost ratio $C_{{FP}}:C_{{FN}}=1:100$, 15/24
operating points had lower relative cost than the simplified ignore
reference at 0.1\\% prevalence, compared with only 3/24 at 0.01\\%.
All seven preregistered sanity tests passed.
""".strip()


discussion_tex = r"""
\subsection{Discussion}

Stage25 separates prior-probability shift from temporal and domain shift.
The former changes PPV even when TPR and FPR are held fixed, whereas the
latter can change the operating characteristics themselves. The results
show that low FPR is a critical requirement for preserving alert
precision at rare attack prevalences, and that high benchmark recall can
still produce an operationally excessive false-alert stream.

SOC capacity and detection usefulness must also be interpreted
separately. An operating point can exceed a small analyst team's capacity
despite high PPV because true alerts require service, while another can
fit within capacity simply because detection has collapsed. The
bidirectional Stage24 asymmetry remains visible under this operational
translation.

The analytic break-even calculations identify exact prevalence
boundaries under the frozen assumptions and avoid post-hoc graphical
selection. They are conditional decision-analysis tools rather than
claims of universal deployment readiness.
""".strip()


limitations_tex = r"""
\subsection{Limitations and Threats to Validity}

Stage25 assumes prior-probability shift within each frozen operating
point and is not empirical production validation. Real environments may
change the class-conditional feature distributions and therefore TPR and
FPR. The fixed one-million-benign-flow volume, two-minute alert service
time, and one/three/ten analyst-day capacity tiers are reference
scenarios rather than universal SOC constants.

The $C_{FP}=1$, $C_{FN}=100$ cost model uses dimensionless relative
operational cost units and must not be interpreted as financial loss.
The projections are deterministic conditional transformations of frozen
empirical estimates; TPR/FPR estimation uncertainty is not propagated.
The benchmark datasets also differ from contemporary live enterprise
telemetry. Finally, Stage24 GROUNDED\_S4 cells remained non-evaluable
because exact durable physical membership was unavailable, and Stage25
does not introduce a heuristic replacement.
""".strip()


contributions_tex = r"""
\subsection{Contributions}

Stage25 provides a validation-safe operational translation layer that:
(i) projects frozen operating points across preregistered attack
prevalences using exact Bayesian relations; (ii) converts operating
characteristics into projected alert volume and SOC workload;
(iii) derives analytic PPV, required-FPR, and relative-cost break-even
boundaries; (iv) connects random, chronological, and bidirectional
cross-dataset results without averaging incompatible directions; and
(v) preserves preregistered assumptions, figures, sanity tests, and
artifact-level reproducibility through the final scientific seal.
""".strip()


MANUSCRIPT_TEX = (
    DOC_DIR
    / "STAGE25_MANUSCRIPT_INTEGRATION.tex"
)


write_text(
    MANUSCRIPT_TEX,
    "\n\n".join(
        [
            "% Stage25 manuscript integration",
            results_tex,
            discussion_tex,
            limitations_tex,
            contributions_tex,
        ]
    ),
)


print(
    "[CREATED]",
    MANUSCRIPT_MD.relative_to(
        REPO
    )
)

print(
    "[CREATED]",
    MANUSCRIPT_TEX.relative_to(
        REPO
    )
)

print()


# ==============================================================================
# 12. PUBLICATION TABLE DOCUMENTS
# ==============================================================================

standard_doc_rows = []


for row in table1_rows:

    standard_doc_rows.append(
        {
            "cell":
                row[
                    "evaluation_cell"
                ],

            "F1":
                (
                    "—"
                    if row[
                        "observed_f1"
                    ] is None
                    else
                    f"{row['observed_f1']:.4f}"
                ),

            "precision":
                f"{row['observed_precision']:.4f}",

            "TPR":
                f"{row['observed_tpr']:.4f}",

            "FPR":
                f"{row['observed_fpr']:.6f}",

            "PPV":
                f"{row['projected_ppv']:.4f}",

            "FP/day":
                f"{row['projected_fp_per_day']:.1f}",

            "TP/day":
                f"{row['projected_tp_per_day']:.1f}",

            "hours/day":
                f"{row['projected_hours_per_day']:.1f}",
        }
    )


tables_md = f"""
# Stage25 Publication Tables

## Table 25-I — STANDARD Operating Point: Benchmark to 0.1% Deployment Stress

{markdown_table(
    standard_doc_rows,
    [
        ("cell", "Evaluation cell"),
        ("F1", "Observed F1"),
        ("precision", "Observed precision"),
        ("TPR", "TPR"),
        ("FPR", "FPR"),
        ("PPV", "PPV @ 0.1%"),
        ("FP/day", "FP/day"),
        ("TP/day", "TP/day"),
        ("hours/day", "Hours/day"),
    ],
)}

The complete 24-operating-point version is stored in
`table25_2_all_operating_points_0p1pct.csv`.

## Table 25-II — Exact Cost Break-Even Coverage

All 24 exact analytic cost break-even points are stored in
`table25_3_exact_cost_break_even.csv`.

Family ranges:

| Family | Minimum break-even | Maximum break-even |
| --- | ---: | ---: |
| Stage22 Random | {family_break_even['STAGE22_RANDOM']['min_percent']:.6f}% | {family_break_even['STAGE22_RANDOM']['max_percent']:.6f}% |
| Stage22 Chronological | {family_break_even['STAGE22_CHRONOLOGICAL']['min_percent']:.6f}% | {family_break_even['STAGE22_CHRONOLOGICAL']['max_percent']:.6f}% |
| IDS2018→CICIDS2017 | {family_break_even['STAGE24_2018_TO_2017']['min_percent']:.6f}% | {family_break_even['STAGE24_2018_TO_2017']['max_percent']:.6f}% |
| CICIDS2017→IDS2018 | {family_break_even['STAGE24_2017_TO_2018']['min_percent']:.6f}% | {family_break_even['STAGE24_2017_TO_2018']['max_percent']:.6f}% |

## Table 25-III — Governance and Sanity

All seven preregistered sanity tests passed. No Stage25 model fitting,
model inference, probability-array generation, target reopening,
threshold search, or calibration was performed.
""".strip()


TABLES_MD = (
    DOC_DIR
    / "STAGE25_PUBLICATION_TABLES.md"
)


write_text(
    TABLES_MD,
    tables_md,
)


table_rows_tex = []


for row in standard_doc_rows:

    table_rows_tex.append(
        " & ".join(
            [
                latex_escape(
                    row[
                        "cell"
                    ]
                ),
                row[
                    "F1"
                ],
                row[
                    "precision"
                ],
                row[
                    "TPR"
                ],
                row[
                    "FPR"
                ],
                row[
                    "PPV"
                ],
                row[
                    "FP/day"
                ],
                row[
                    "TP/day"
                ],
                row[
                    "hours/day"
                ],
            ]
        )
        +
        r" \\"
    )


tables_tex = (
    r"""
% Stage25 paper-ready publication table
\begin{table*}[t]
\caption{STANDARD Operating Point: Benchmark-to-Deployment Translation at 0.1\% Attack Prevalence}
\centering
\small
\begin{tabular}{lrrrrrrrr}
\hline
Evaluation Cell & F1 & Prec. & TPR & FPR & PPV & FP/day & TP/day & h/day \\
\hline
"""
    +
    "\n".join(
        table_rows_tex
    )
    +
    r"""
\hline
\end{tabular}
\label{tab:stage25_standard_translation}
\end{table*}

\noindent
All 24 frozen operating points, exact cost break-even values, family-level
cost decisions, and preregistered sanity receipts are retained in the
Stage25 publication CSV package.
"""
)


TABLES_TEX = (
    DOC_DIR
    / "STAGE25_PUBLICATION_TABLES.tex"
)


write_text(
    TABLES_TEX,
    tables_tex,
)


print(
    "[CREATED]",
    TABLES_MD.relative_to(
        REPO
    )
)

print(
    "[CREATED]",
    TABLES_TEX.relative_to(
        REPO
    )
)

print()


# ==============================================================================
# 13. CURRENT NOTEBOOK RECOVERY + EXPORT
# ==============================================================================

print("=" * 120)
print("STAGE25 NOTEBOOK + SCRIPT EXPORT")
print("=" * 120)


EXPORT_DIR = Path(
    "/kaggle/working/stage25_exports"
)


EXPORT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


FULL_NOTEBOOK = (
    EXPORT_DIR
    / "stage25_prevalence_operational_stress_FULL.ipynb"
)


GITHUB_NOTEBOOK = (
    SCRIPT_DIR
    / "stage25_prevalence_operational_stress.ipynb"
)


GITHUB_SCRIPT = (
    SCRIPT_DIR
    / "stage25_prevalence_operational_stress.py"
)


SCRIPT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# ------------------------------------------------------------------------------
# Search for a durable notebook file first.
# ------------------------------------------------------------------------------

candidate_notebooks = []


for search_root in [
    Path(
        "/kaggle/working"
    ),
    EXPORT_DIR,
]:

    if not search_root.exists():

        continue

    for candidate in search_root.glob(
        "*.ipynb"
    ):

        name_lower = candidate.name.lower()

        if (
            "stage25"
            in
            name_lower
            and
            candidate != FULL_NOTEBOOK
        ):

            candidate_notebooks.append(
                candidate
            )


candidate_notebooks = sorted(
    set(
        candidate_notebooks
    ),
    key=lambda p:
        p.stat().st_mtime,
    reverse=True,
)


notebook_source_mode = None

notebook = None

source_notebook_path = None


if candidate_notebooks:

    for candidate in candidate_notebooks:

        try:

            candidate_payload = json.loads(
                candidate.read_text(
                    encoding="utf-8"
                )
            )

            if (
                isinstance(
                    candidate_payload,
                    dict,
                )
                and
                isinstance(
                    candidate_payload.get(
                        "cells"
                    ),
                    list,
                )
            ):

                combined_source = "\n".join(
                    normalize_source(
                        cell.get(
                            "source"
                        )
                    )
                    for cell in candidate_payload[
                        "cells"
                    ]
                )


                if (
                    "STAGE25-0"
                    in
                    combined_source
                    and
                    "STAGE25-4"
                    in
                    combined_source
                ):

                    notebook = candidate_payload

                    source_notebook_path = candidate

                    notebook_source_mode = (
                        "RECOVERED_FROM_DURABLE_STAGE25_NOTEBOOK"
                    )

                    break

        except Exception:

            pass


# ------------------------------------------------------------------------------
# Fallback: reconstruct notebook from current IPython kernel input history.
# ------------------------------------------------------------------------------

if notebook is None:

    try:

        ip = get_ipython()

    except Exception:

        ip = None


    if ip is None:

        raise RuntimeError(
            "\nUnable to recover Stage25 notebook.\n"
            "No durable notebook file and no active IPython kernel."
        )


    raw_history = list(
        ip.history_manager.input_hist_raw[
            1:
        ]
    )


    sources = [
        normalize_source(
            src
        )
        for src in raw_history
        if normalize_source(
            src
        ).strip()
    ]


    combined_source = "\n".join(
        sources
    )


    required_history_markers = [
        "STAGE25-0",
        "STAGE25-1",
        "STAGE25-2",
        "STAGE25-3",
        "STAGE25-4",
    ]


    missing_history_markers = [
        marker
        for marker in required_history_markers
        if marker not in combined_source
    ]


    if missing_history_markers:

        raise RuntimeError(
            "\nCurrent kernel history is not sufficient to reconstruct "
            "the complete Stage25 notebook.\n"
            "Missing markers:\n"
            +
            "\n".join(
                missing_history_markers
            )
        )


    notebook = {
        "cells": [
            {
                "cell_type":
                    "code",

                "execution_count":
                    None,

                "metadata":
                    {},

                "outputs":
                    [],

                "source":
                    source.splitlines(
                        keepends=True
                    ),
            }
            for source in sources
        ],

        "metadata": {
            "kernelspec": {
                "display_name":
                    "Python 3",

                "language":
                    "python",

                "name":
                    "python3",
            },

            "language_info": {
                "name":
                    "python",
            },

            "stage25_export": {
                "mode":
                    "RECOVERED_FROM_CURRENT_KERNEL_INPUT_HISTORY",

                "note":
                    (
                        "Code-cell execution history reconstructed because "
                        "the live Kaggle draft notebook file was not exposed "
                        "as a durable filesystem object."
                    ),
            },
        },

        "nbformat":
            4,

        "nbformat_minor":
            5,
    }


    notebook_source_mode = (
        "RECOVERED_FROM_CURRENT_KERNEL_INPUT_HISTORY"
    )


# ------------------------------------------------------------------------------
# Verify Stage25 coverage.
# ------------------------------------------------------------------------------

combined_source = "\n".join(
    normalize_source(
        cell.get(
            "source"
        )
    )
    for cell in notebook[
        "cells"
    ]
)


for marker in [
    "STAGE25-0",
    "STAGE25-1",
    "STAGE25-2",
    "STAGE25-3",
    "STAGE25-4",
]:

    if marker not in combined_source:

        raise RuntimeError(
            f"Recovered notebook missing marker: {marker}"
        )


# ------------------------------------------------------------------------------
# Full downloadable notebook.
# ------------------------------------------------------------------------------

FULL_NOTEBOOK.write_text(
    json.dumps(
        notebook,
        indent=1,
        ensure_ascii=False,
    )
    +
    "\n",
    encoding="utf-8",
)


full_notebook_sha = sha256_file(
    FULL_NOTEBOOK
)


# ------------------------------------------------------------------------------
# Sanitized GitHub notebook.
# ------------------------------------------------------------------------------

sanitized_notebook = json.loads(
    json.dumps(
        notebook
    )
)


for cell in sanitized_notebook[
    "cells"
]:

    source = sanitize_source(
        cell.get(
            "source"
        )
    )


    cell[
        "source"
    ] = source.splitlines(
        keepends=True
    )


    if cell.get(
        "cell_type"
    ) == "code":

        cell[
            "execution_count"
        ] = None

        cell[
            "outputs"
        ] = []


    # Keep only non-sensitive generic cell metadata.
    cell[
        "metadata"
    ] = {}


sanitized_notebook[
    "metadata"
] = {
    "kernelspec": {
        "display_name":
            "Python 3",

        "language":
            "python",

        "name":
            "python3",
    },

    "language_info": {
        "name":
            "python",
    },

    "stage25_export": {
        "scientific_status":
            "CLOSED",

        "source_mode":
            notebook_source_mode,

        "outputs_removed":
            True,

        "secrets_sanitized":
            True,
    },
}


GITHUB_NOTEBOOK.write_text(
    json.dumps(
        sanitized_notebook,
        indent=1,
        ensure_ascii=False,
    )
    +
    "\n",
    encoding="utf-8",
)


github_notebook_sha = sha256_file(
    GITHUB_NOTEBOOK
)


# ------------------------------------------------------------------------------
# Python script export.
# ------------------------------------------------------------------------------

script_lines = [
    "# ==============================================================================",
    "# STAGE25 — PREVALENCE AND OPERATIONAL STRESS",
    "# Reconstructed/exported from the Stage25 Kaggle notebook.",
    "#",
    "# Scientific state: CLOSED",
    "# No new model fitting/inference is authorized by this export.",
    "# ==============================================================================",
    "",
]


for index, cell in enumerate(
    sanitized_notebook[
        "cells"
    ],
    start=1,
):

    cell_type = cell.get(
        "cell_type"
    )


    source = normalize_source(
        cell.get(
            "source"
        )
    )


    if cell_type == "code":

        script_lines.append(
            f"# %% [Stage25 notebook cell {index}]"
        )

        script_lines.extend(
            source.splitlines()
        )

        script_lines.append(
            ""
        )


    elif cell_type == "markdown":

        script_lines.append(
            f"# %% [markdown cell {index}]"
        )

        for line in source.splitlines():

            script_lines.append(
                "# "
                +
                line
            )

        script_lines.append(
            ""
        )


GITHUB_SCRIPT.write_text(
    "\n".join(
        script_lines
    ).rstrip()
    +
    "\n",
    encoding="utf-8",
)


github_script_sha = sha256_file(
    GITHUB_SCRIPT
)


print(
    "Notebook recovery mode:",
    notebook_source_mode,
)

if source_notebook_path is not None:

    print(
        "Notebook source:",
        source_notebook_path,
    )


print(
    "Cells:",
    len(
        notebook[
            "cells"
        ]
    ),
)

print()

print(
    "Full downloadable notebook:"
)

print(
    " ",
    FULL_NOTEBOOK
)

print(
    "SHA256:",
    full_notebook_sha,
)

print()

print(
    "Sanitized GitHub notebook:"
)

print(
    " ",
    GITHUB_NOTEBOOK.relative_to(
        REPO
    )
)

print(
    "SHA256:",
    github_notebook_sha,
)

print()

print(
    "Python script:"
)

print(
    " ",
    GITHUB_SCRIPT.relative_to(
        REPO
    )
)

print(
    "SHA256:",
    github_script_sha,
)

print()


# ==============================================================================
# 14. README + JOURNAL SUMMARY UPDATE
# ==============================================================================

print("=" * 120)
print("README + JOURNAL SUMMARY UPDATE")
print("=" * 120)


README_MARKER = (
    "<!-- STAGE25_PREVALENCE_OPERATIONAL_STRESS_CLOSEOUT -->"
)


README_BLOCK = f"""
## Stage25 — Prevalence and Operational Stress Audit

**Status: SCIENTIFICALLY CLOSED**

Stage25 analytically translated 24 already-frozen Stage22/Stage24
operating points across six preregistered attack prevalences without
model refitting, new inference, target reopening, threshold tuning, or
calibration.

Key frozen outputs:

- 24 operating points
- 6 prevalence levels
- 144 Bayesian / traffic / SOC / relative-cost projections
- 120 exact PPV break-even calculations
- 720 required-FPR calculations
- 24 exact relative-cost break-even prevalences
- 5 preregistered figures (PNG + SVG)
- 7/7 preregistered sanity tests passed
- fixed reference scenario: 1,000,000 benign flows/day, 2 min/alert,
  analyst tiers 1/3/10, relative cost C_FP:C_FN = 1:100

The analysis demonstrates that benchmark precision and F1 do not directly
determine deployment PPV or SOC workload under rare attacks; very low FPR
is essential, capacity feasibility is distinct from detection usefulness,
and the Stage24 cross-dataset asymmetry persists under deployment-facing
translation.

Stage25-0 commit: `{STAGE25_0_COMMIT}`  
Stage25-1 commit: `{STAGE25_1_COMMIT}`  
Stage25-2 commit: `{STAGE25_2_COMMIT}`  
Stage25-3 commit: `{STAGE25_3_COMMIT}`  
Stage25-4 commit: `{STAGE25_4_COMMIT}`

Publication material is under:

- `results/stage25_prevalence_stress/stage25_publication_package/`
- `figures/stage25_prevalence_stress/`
- `docs/STAGE25_MANUSCRIPT_INTEGRATION.md`
- `scripts/stage25/`
""".strip()


append_once(
    README,
    README_MARKER,
    README_BLOCK,
)


JOURNAL_MARKER = (
    "<!-- STAGE25_JOURNAL_EXTENSION_CLOSEOUT -->"
)


JOURNAL_BLOCK = f"""
## Stage25 — Deployment Prevalence and SOC Operational Stress

Stage25 is now scientifically closed. The stage uses the frozen Stage22
random/chronological and Stage24 bidirectional cross-dataset operating
points and performs no new model fitting or target access.

The extension contributes a prior-shift deployment analysis across
10%, 3%, 1%, 0.3%, 0.1%, and 0.01% attack prevalence. It reports PPV,
NPV, likelihood-ratio evidence translation, exact PPV thresholds,
required FPR for target PPV, projected false/true alert volume,
analyst-processing workload, SOC capacity exceedance, and a frozen
relative cost model.

At 0.1% prevalence the Stage22 random STANDARD operating point retains
PPV {random_std['projected_ppv']:.6f} but still requires
{random_std['projected_alert_processing_hours_per_day']:.1f}
analyst-hours/day because true positives themselves consume capacity.
The chronological STANDARD operating point instead projects PPV
{chron_std['projected_ppv']:.9f} with only
{chron_std['projected_tp_per_day']:.4f} true alerts/day, showing why
capacity fit cannot be equated with operational usefulness.

The primary IDS2018→CICIDS2017 STANDARD transfer projects PPV
{primary_standard_ppv_min:.6f}–{primary_standard_ppv_max:.6f} at 0.1%,
whereas the reverse CICIDS2017→IDS2018 STANDARD direction projects only
{secondary_standard_ppv_min:.9f}–{secondary_standard_ppv_max:.9f}.
Under the frozen 1:100 relative-cost scenario, 15/24 operating points
favor the model at 0.1% prevalence but only 3/24 do so at 0.01%.

All seven preregistered sanity checks pass and all five preregistered
figures are retained.

Stage25-4 frozen result SHA:
`{EXPECTED_STAGE25_4_RESULT_SHA}`
""".strip()


append_once(
    JOURNAL_SUMMARY,
    JOURNAL_MARKER,
    JOURNAL_BLOCK,
)


print(
    "[PASS] README updated."
)

print(
    "[PASS] JOURNAL_EXTENSION_SUMMARY updated."
)

print()


# ==============================================================================
# 15. PUBLICATION PACKAGE MANIFEST
# ==============================================================================

print("=" * 120)
print("PUBLICATION PACKAGE MANIFEST")
print("=" * 120)


publication_docs = [
    MANUSCRIPT_MD,
    MANUSCRIPT_TEX,
    TABLES_MD,
    TABLES_TEX,
]


publication_tables = [
    TABLE1_CSV,
    TABLE2_CSV,
    TABLE3_CSV,
    TABLE4_CSV,
    TABLE5_CSV,
]


publication_figures = []


for figure_id in sorted(
    figure_manifest[
        "figures"
    ]
):

    for fmt in [
        "png",
        "svg",
    ]:

        publication_figures.append(
            REPO
            /
            figure_manifest[
                "figures"
            ][
                figure_id
            ][
                fmt
            ][
                "path"
            ]
        )


publication_scripts = [
    GITHUB_NOTEBOOK,
    GITHUB_SCRIPT,
]


publication_manifest_payload = {
    "stage":
        "Stage25",

    "status":
        "PUBLICATION_PACKAGE_COMPLETE",

    "scientific_status":
        "CLOSED",

    "source_parent_commit":
        EXPECTED_PARENT,

    "frozen_result_shas": {
        "stage25_0":
            EXPECTED_STAGE25_0_FREEZE_SHA,

        "stage25_1":
            EXPECTED_STAGE25_1_RESULT_SHA,

        "stage25_2":
            EXPECTED_STAGE25_2_RESULT_SHA,

        "stage25_3":
            EXPECTED_STAGE25_3_RESULT_SHA,

        "stage25_4":
            EXPECTED_STAGE25_4_RESULT_SHA,
    },

    "tables": {
        str(
            path.relative_to(
                REPO
            )
        ):
            sha256_file(
                path
            )
        for path in publication_tables
    },

    "figures": {
        str(
            path.relative_to(
                REPO
            )
        ):
            sha256_file(
                path
            )
        for path in publication_figures
    },

    "documents": {
        str(
            path.relative_to(
                REPO
            )
        ):
            sha256_file(
                path
            )
        for path in publication_docs
    },

    "reproducibility_exports": {
        str(
            path.relative_to(
                REPO
            )
        ):
            sha256_file(
                path
            )
        for path in publication_scripts
    },

    "external_downloadable_notebook": {
        "path":
            str(
                FULL_NOTEBOOK
            ),

        "sha256":
            full_notebook_sha,

        "source_mode":
            notebook_source_mode,
    },

    "governance": {
        "new_model_fits":
            0,

        "new_model_inference":
            0,

        "new_probability_arrays":
            0,

        "target_reopenings":
            0,

        "new_threshold_searches":
            0,

        "new_calibration":
            0,

        "preregistered_sanity_tests":
            "7/7 PASS",

        "preregistered_figures":
            "5/5 COMPLETE",

        "figure_files":
            "10/10 VERIFIED",
    },
}


PUBLICATION_MANIFEST = (
    PUB_DIR
    / "stage25_publication_package_manifest.json"
)


write_json(
    PUBLICATION_MANIFEST,
    publication_manifest_payload,
)


publication_manifest_sha = sha256_file(
    PUBLICATION_MANIFEST
)


PUBLICATION_MANIFEST_SHA = (
    PUB_DIR
    / "stage25_publication_package_manifest.sha256"
)


write_text(
    PUBLICATION_MANIFEST_SHA,
    (
        f"{publication_manifest_sha}  "
        f"{PUBLICATION_MANIFEST.name}"
    ),
)


print(
    "Publication manifest SHA:"
)

print(
    " ",
    publication_manifest_sha
)

print()


# ==============================================================================
# 16. PUBLICATION CLOSEOUT DOCUMENT
# ==============================================================================

CLOSEOUT_MD = (
    DOC_DIR
    / "STAGE25_PUBLICATION_CLOSEOUT.md"
)


closeout_text = f"""
# Stage25 Publication and Reproducibility Closeout

## Scientific Status

**STAGE25 = CLOSED**

Stage25 completed the preregistered prevalence and operational-stress
audit without any model refitting, new inference, target reopening,
threshold search, or calibration.

## Frozen Scientific Chain

- Stage25-0 protocol lock: `{STAGE25_0_COMMIT}`
- Stage25-1 Bayesian projection: `{STAGE25_1_COMMIT}`
- Stage25-2 traffic/SOC capacity: `{STAGE25_2_COMMIT}`
- Stage25-3 exact break-even analysis: `{STAGE25_3_COMMIT}`
- Stage25-4 benchmark→operational translation and figures: `{STAGE25_4_COMMIT}`

## Final Accounting

- inherited cells: 8
- inherited operating points: 24
- prevalence levels: 6
- projection rows: 144
- exact PPV break-even rows: 120
- required-FPR rows: 720
- exact cost break-even rows: 24
- preregistered sanity tests: 7/7 PASS
- preregistered figures: 5/5 complete
- figure files: 10/10 verified
- new model fits: 0
- new model inference: 0
- new probability arrays: 0
- target reopenings: 0

## Reproducibility Exports

GitHub notebook:

`scripts/stage25/stage25_prevalence_operational_stress.ipynb`

GitHub Python script:

`scripts/stage25/stage25_prevalence_operational_stress.py`

Full downloadable notebook:

`{FULL_NOTEBOOK}`

## Publication Package

Manifest SHA256:

`{publication_manifest_sha}`

Publication tables, manuscript sections, figures, and reproducibility
exports are frozen under the Stage25 publication package and associated
repository paths.

Stage25 performs conditional analytic deployment projections; it does
not claim empirical production validation.
""".strip()


write_text(
    CLOSEOUT_MD,
    closeout_text,
)


# ==============================================================================
# 17. FINAL AUDIT RECEIPT
# ==============================================================================

print("=" * 120)
print("FINAL AUDIT RECEIPT")
print("=" * 120)


FINAL_DIR.mkdir(
    parents=True,
    exist_ok=False,
)


final_audit_payload = {
    "stage":
        "Stage25-5",

    "status":
        "FINAL_AUDIT_PASS",

    "created_at_utc":
        datetime.now(
            timezone.utc
        ).isoformat(),

    "repository_parent_commit":
        EXPECTED_PARENT,

    "commit_chain":
        commit_chain_receipts,

    "frozen_result_shas": {
        "stage25_0_freeze_record":
            freeze_sha,

        "stage25_1_result":
            s1_sha,

        "stage25_2_result":
            s2_sha,

        "stage25_3_result":
            s3_sha,

        "stage25_4_result":
            s4_sha,
    },

    "publication_manifest_sha256":
        publication_manifest_sha,

    "scientific_access": {
        "new_model_fits":
            0,

        "new_model_inference":
            0,

        "model_files_loaded_for_science":
            0,

        "probability_arrays_opened":
            0,

        "probability_arrays_created":
            0,

        "target_features_read":
            0,

        "target_labels_read":
            0,

        "target_reopenings":
            0,

        "threshold_searches":
            0,

        "calibration_runs":
            0,

        "new_stage25_projections":
            0,
    },

    "scientific_inventory": {
        "inherited_cells":
            8,

        "operating_points":
            24,

        "prevalence_levels":
            6,

        "projection_rows":
            144,

        "ppv_break_even_rows":
            120,

        "required_fpr_rows":
            720,

        "cost_break_even_rows":
            24,
    },

    "sanity": {
        "preregistered_tests":
            7,

        "passed":
            7,

        "failed":
            0,
    },

    "figures": {
        "preregistered":
            5,

        "generated":
            5,

        "png_svg_files":
            10,

        "verified":
            10,

        "outcome_based_dropping":
            False,
    },

    "reproducibility": {
        "notebook_source_mode":
            notebook_source_mode,

        "full_notebook_sha256":
            full_notebook_sha,

        "github_notebook_sha256":
            github_notebook_sha,

        "github_script_sha256":
            github_script_sha,
    },

    "publication_documents": {
        str(
            path.relative_to(
                REPO
            )
        ):
            sha256_file(
                path
            )
        for path in (
            publication_docs
            +
            [
                CLOSEOUT_MD,
            ]
        )
    },

    "readme_sha256":
        sha256_file(
            README
        ),

    "journal_extension_summary_sha256":
        sha256_file(
            JOURNAL_SUMMARY
        ),

    "audit_conclusion":
        (
            "Stage25 scientific execution is complete and sealed. "
            "All downstream work is publication/reproducibility packaging "
            "only; Stage25 scientific adaptation is prohibited."
        ),
}


FINAL_AUDIT_JSON = (
    FINAL_DIR
    / "stage25_5_final_audit.json"
)


write_json(
    FINAL_AUDIT_JSON,
    final_audit_payload,
)


final_audit_sha = sha256_file(
    FINAL_AUDIT_JSON
)


print(
    "Final audit SHA:"
)

print(
    " ",
    final_audit_sha
)

print()


# ==============================================================================
# 18. FINAL SCIENTIFIC SYNTHESIS / SEAL
# ==============================================================================

final_synthesis_payload = {
    "stage":
        "Stage25",

    "status":
        "STAGE25_PREVALENCE_OPERATIONAL_STRESS_COMPLETE",

    "scientific_status":
        "CLOSED_AND_SEALED",

    "created_at_utc":
        datetime.now(
            timezone.utc
        ).isoformat(),

    "repository_parent_before_closeout":
        EXPECTED_PARENT,

    "stage25_commit_chain": {
        "stage25_0":
            STAGE25_0_COMMIT,

        "stage25_1":
            STAGE25_1_COMMIT,

        "stage25_2":
            STAGE25_2_COMMIT,

        "stage25_3":
            STAGE25_3_COMMIT,

        "stage25_4":
            STAGE25_4_COMMIT,
    },

    "frozen_result_shas": {
        "stage25_0":
            EXPECTED_STAGE25_0_FREEZE_SHA,

        "stage25_1":
            EXPECTED_STAGE25_1_RESULT_SHA,

        "stage25_2":
            EXPECTED_STAGE25_2_RESULT_SHA,

        "stage25_3":
            EXPECTED_STAGE25_3_RESULT_SHA,

        "stage25_4":
            EXPECTED_STAGE25_4_RESULT_SHA,
    },

    "stage25_5_final_audit_sha256":
        final_audit_sha,

    "publication_manifest_sha256":
        publication_manifest_sha,

    "completion": {
        "protocol_lock":
            "PASS",

        "bayesian_prevalence_projection":
            "PASS",

        "traffic_soc_capacity_projection":
            "PASS",

        "exact_break_even_analysis":
            "PASS",

        "benchmark_operational_translation":
            "PASS",

        "publication_figures":
            "5/5 COMPLETE",

        "preregistered_sanity_tests":
            "7/7 PASS",

        "publication_package":
            "COMPLETE",

        "notebook_script_export":
            "COMPLETE",

        "scientific_execution":
            "CLOSED",
    },

    "absolute_scientific_accounting": {
        "new_model_fits":
            0,

        "new_model_inference":
            0,

        "new_probability_arrays":
            0,

        "target_reopenings":
            0,

        "new_threshold_searches":
            0,

        "new_calibration":
            0,
    },

    "frozen_scenario": {
        "prevalence_grid": [
            0.10,
            0.03,
            0.01,
            0.003,
            0.001,
            0.0001,
        ],

        "benign_flows_per_day":
            1_000_000,

        "minutes_per_alert":
            2,

        "analyst_tiers":
            [
                1,
                3,
                10,
            ],

        "relative_cost_C_FP":
            1,

        "relative_cost_C_FN":
            100,
    },

    "headline_findings": {
        "stage22_random_standard_at_0p1pct": {
            "ppv":
                random_std[
                    "projected_ppv"
                ],

            "fp_per_day":
                random_std[
                    "projected_fp_per_day"
                ],

            "tp_per_day":
                random_std[
                    "projected_tp_per_day"
                ],

            "processing_hours_per_day":
                random_std[
                    "projected_alert_processing_hours_per_day"
                ],
        },

        "stage22_chronological_standard_at_0p1pct": {
            "ppv":
                chron_std[
                    "projected_ppv"
                ],

            "fp_per_day":
                chron_std[
                    "projected_fp_per_day"
                ],

            "tp_per_day":
                chron_std[
                    "projected_tp_per_day"
                ],

            "processing_hours_per_day":
                chron_std[
                    "projected_alert_processing_hours_per_day"
                ],
        },

        "ids2018_to_cicids2017_standard_at_0p1pct": {
            "ppv_min":
                primary_standard_ppv_min,

            "ppv_max":
                primary_standard_ppv_max,

            "processing_hours_min":
                primary_standard_hours_min,

            "processing_hours_max":
                primary_standard_hours_max,
        },

        "cicids2017_to_ids2018_standard_at_0p1pct": {
            "ppv_min":
                secondary_standard_ppv_min,

            "ppv_max":
                secondary_standard_ppv_max,
        },

        "relative_cost_at_0p1pct": {
            "model_lower":
                int(
                    cost_0p1[
                        "model_lower_count"
                    ]
                ),

            "ignore_lower":
                int(
                    cost_0p1[
                        "ignore_lower_count"
                    ]
                ),
        },

        "relative_cost_at_0p01pct": {
            "model_lower":
                int(
                    cost_0p01[
                        "model_lower_count"
                    ]
                ),

            "ignore_lower":
                int(
                    cost_0p01[
                        "ignore_lower_count"
                    ]
                ),
        },

        "cost_break_even_ranges":
            family_break_even,
    },

    "scientific_interpretation": [
        (
            "Base-rate stress can sharply change PPV even when a frozen "
            "TPR/FPR operating point is held fixed."
        ),
        (
            "Very low FPR is necessary for useful positive-alert precision "
            "under rare attacks."
        ),
        (
            "High PPV does not guarantee low SOC workload because true "
            "alerts also require analyst service."
        ),
        (
            "Capacity feasibility does not guarantee useful detection when "
            "TPR has collapsed."
        ),
        (
            "Stage24 directional cross-dataset asymmetry persists after "
            "deployment-facing translation."
        ),
        (
            "Relative-cost conclusions depend on prevalence and the frozen "
            "dimensionless 1:100 FP/FN cost assumption."
        ),
    ],

    "limitations": [
        "Prior-probability-shift assumption within each operating point.",
        "Fixed one-million-benign-flow reference volume.",
        "Two-minute alert-service reference assumption.",
        "Dimensionless 1:100 relative-cost model, not financial loss.",
        "No propagated TPR/FPR estimation uncertainty.",
        "Benchmark datasets are not live production telemetry.",
        "Stage24 GROUNDED_S4 cells remain non-evaluable.",
        "No deployment- or prevalence-specific threshold retuning.",
    ],

    "final_rule":
        (
            "NO FURTHER STAGE25 SCIENTIFIC FITTING, INFERENCE, TARGET "
            "OPENING, THRESHOLD TUNING, CALIBRATION, ASSUMPTION CHANGES, "
            "OR RESULT-DEPENDENT FIGURE SELECTION."
        ),

    "next_project_action":
        (
            "START THE FINAL REMAINING RESEARCH STAGE IN A NEW NOTEBOOK; "
            "DO NOT REOPEN STAGE25."
        ),
}


FINAL_SYNTHESIS_JSON = (
    FINAL_DIR
    / "stage25_5_final_synthesis.json"
)


write_json(
    FINAL_SYNTHESIS_JSON,
    final_synthesis_payload,
)


final_synthesis_sha = sha256_file(
    FINAL_SYNTHESIS_JSON
)


FINAL_SYNTHESIS_SHA = (
    FINAL_DIR
    / "stage25_5_final_synthesis.sha256"
)


write_text(
    FINAL_SYNTHESIS_SHA,
    (
        f"{final_synthesis_sha}  "
        f"{FINAL_SYNTHESIS_JSON.name}"
    ),
)


FINAL_SYNTHESIS_MD = (
    FINAL_DIR
    / "stage25_5_final_synthesis.md"
)


final_synthesis_md_text = f"""
# Stage25 Final Scientific Synthesis

**Status: CLOSED AND SEALED**

Final synthesis SHA256:

`{final_synthesis_sha}`

Publication manifest SHA256:

`{publication_manifest_sha}`

## Completion

- Stage25-0 protocol lock: PASS
- Stage25-1 Bayesian projection: PASS
- Stage25-2 traffic/SOC capacity projection: PASS
- Stage25-3 exact break-even analysis: PASS
- Stage25-4 benchmark→operational translation: PASS
- preregistered figures: 5/5 complete
- preregistered sanity tests: 7/7 PASS
- publication package: COMPLETE
- notebook/script export: COMPLETE

## Scientific Accounting

- new model fits: 0
- new model inference: 0
- new probability arrays: 0
- target reopenings: 0
- threshold searches: 0
- calibration runs: 0

## Central Result

Stage25 shows that deployment interpretation changes materially under rare
attack prevalence even when each empirical operating point is frozen.
Very low FPR is required to preserve positive-alert precision, SOC
capacity and detection usefulness must be evaluated separately, and the
Stage24 bidirectional transfer asymmetry persists in deployment-facing
PPV and workload projections.

At 0.1% attack prevalence, the Stage22 random STANDARD operating point
projects PPV {random_std['projected_ppv']:.6f} with
{random_std['projected_fp_per_day']:.1f} FP/day and
{random_std['projected_tp_per_day']:.1f} TP/day, but still requires
{random_std['projected_alert_processing_hours_per_day']:.1f}
analyst-hours/day.

The Stage22 chronological STANDARD operating point projects PPV
{chron_std['projected_ppv']:.9f} and only
{chron_std['projected_tp_per_day']:.4f} TP/day, demonstrating that low
workload may reflect detection collapse rather than operational success.

IDS2018→CICIDS2017 STANDARD PPV at 0.1% ranges from
{primary_standard_ppv_min:.6f} to {primary_standard_ppv_max:.6f};
CICIDS2017→IDS2018 STANDARD PPV ranges only from
{secondary_standard_ppv_min:.9f} to {secondary_standard_ppv_max:.9f}.

Under the frozen relative-cost ratio C_FP:C_FN=1:100, 15/24 operating
points favor the model at 0.1% prevalence but only 3/24 at 0.01%.

## Final Governance Rule

**Stage25 must not be scientifically reopened.**

No further Stage25 fitting, inference, target opening, threshold tuning,
calibration, assumption modification, or result-dependent figure
selection is authorized.
""".strip()


write_text(
    FINAL_SYNTHESIS_MD,
    final_synthesis_md_text,
)


print(
    "Final synthesis SHA:"
)

print(
    " ",
    final_synthesis_sha
)

print()


# ==============================================================================
# 19. FINAL CHECKSUM MANIFEST
# ==============================================================================

FINAL_CHECKSUMS = (
    FINAL_DIR
    / "checksums.sha256"
)


final_checksum_paths = [
    FINAL_AUDIT_JSON,
    FINAL_SYNTHESIS_JSON,
    FINAL_SYNTHESIS_SHA,
    FINAL_SYNTHESIS_MD,
]


write_text(
    FINAL_CHECKSUMS,
    "\n".join(
        (
            f"{sha256_file(path)}  "
            f"{path.name}"
        )
        for path in final_checksum_paths
    ),
)


# ==============================================================================
# 20. DOWNLOADABLE ZIP EXPORTS
# ==============================================================================

print("=" * 120)
print("DOWNLOADABLE EXPORTS")
print("=" * 120)


NOTEBOOK_ZIP = Path(
    "/kaggle/working/stage25_notebook_export.zip"
)


PUBLICATION_ZIP = Path(
    "/kaggle/working/stage25_publication_package.zip"
)


for zip_path in [
    NOTEBOOK_ZIP,
    PUBLICATION_ZIP,
]:

    if zip_path.exists():

        zip_path.unlink()


# ------------------------------------------------------------------------------
# Notebook / script ZIP.
# ------------------------------------------------------------------------------

with zipfile.ZipFile(
    NOTEBOOK_ZIP,
    "w",
    compression=zipfile.ZIP_DEFLATED,
    compresslevel=9,
) as zf:

    zf.write(
        FULL_NOTEBOOK,
        arcname=FULL_NOTEBOOK.name,
    )

    zf.write(
        GITHUB_NOTEBOOK,
        arcname=(
            "github/"
            +
            GITHUB_NOTEBOOK.name
        ),
    )

    zf.write(
        GITHUB_SCRIPT,
        arcname=(
            "github/"
            +
            GITHUB_SCRIPT.name
        ),
    )


notebook_zip_sha = sha256_file(
    NOTEBOOK_ZIP
)


# ------------------------------------------------------------------------------
# Publication ZIP.
# ------------------------------------------------------------------------------

publication_zip_files = []


publication_zip_files.extend(
    publication_tables
)

publication_zip_files.extend(
    publication_docs
)

publication_zip_files.extend(
    [
        CLOSEOUT_MD,
        PUBLICATION_MANIFEST,
        PUBLICATION_MANIFEST_SHA,
        FINAL_AUDIT_JSON,
        FINAL_SYNTHESIS_JSON,
        FINAL_SYNTHESIS_SHA,
        FINAL_SYNTHESIS_MD,
        FINAL_CHECKSUMS,
        GITHUB_NOTEBOOK,
        GITHUB_SCRIPT,
    ]
)

publication_zip_files.extend(
    publication_figures
)


with zipfile.ZipFile(
    PUBLICATION_ZIP,
    "w",
    compression=zipfile.ZIP_DEFLATED,
    compresslevel=9,
) as zf:

    seen = set()

    for path in publication_zip_files:

        path = Path(
            path
        )

        if path in seen:

            continue

        seen.add(
            path
        )

        if path.is_relative_to(
            REPO
        ):

            arcname = str(
                path.relative_to(
                    REPO
                )
            )

        else:

            arcname = path.name


        zf.write(
            path,
            arcname=arcname,
        )


publication_zip_sha = sha256_file(
    PUBLICATION_ZIP
)


print(
    "Notebook/script ZIP:"
)

print(
    " ",
    NOTEBOOK_ZIP
)

print(
    "SHA256:",
    notebook_zip_sha,
)

print()

print(
    "Publication ZIP:"
)

print(
    " ",
    PUBLICATION_ZIP
)

print(
    "SHA256:",
    publication_zip_sha,
)

print()


# ==============================================================================
# 21. FINAL LOCAL ARTIFACT AUDIT
# ==============================================================================

print("=" * 120)
print("FINAL LOCAL ARTIFACT AUDIT")
print("=" * 120)


required_repo_files = [
    TABLE1_CSV,
    TABLE2_CSV,
    TABLE3_CSV,
    TABLE4_CSV,
    TABLE5_CSV,
    MANUSCRIPT_MD,
    MANUSCRIPT_TEX,
    TABLES_MD,
    TABLES_TEX,
    CLOSEOUT_MD,
    PUBLICATION_MANIFEST,
    PUBLICATION_MANIFEST_SHA,
    GITHUB_NOTEBOOK,
    GITHUB_SCRIPT,
    FINAL_AUDIT_JSON,
    FINAL_SYNTHESIS_JSON,
    FINAL_SYNTHESIS_SHA,
    FINAL_SYNTHESIS_MD,
    FINAL_CHECKSUMS,
]


for path in required_repo_files:

    if not path.is_file():

        raise RuntimeError(
            f"Missing Stage25 closeout artifact:\n{path}"
        )


if len(
    publication_figures
) != 10:

    raise RuntimeError(
        "Publication figure count changed."
    )


print(
    "[PASS] Publication tables:       5"
)

print(
    "[PASS] Publication figures:      10 files"
)

print(
    "[PASS] Manuscript integration:   MD + TEX"
)

print(
    "[PASS] Publication tables docs:  MD + TEX"
)

print(
    "[PASS] Notebook export:          COMPLETE"
)

print(
    "[PASS] Python script export:     COMPLETE"
)

print(
    "[PASS] Final audit:              COMPLETE"
)

print(
    "[PASS] Final synthesis:          COMPLETE"
)

print()


# ==============================================================================
# 22. GITHUB CREDENTIAL
# ==============================================================================

github_token = None

token_source = None


try:

    from kaggle_secrets import UserSecretsClient

    client = UserSecretsClient()


    for name in [
        "GITHUB_TOKEN",
        "github_token",
        "GH_TOKEN",
        "GITHUB_PAT",
        "github_pat",
    ]:

        try:

            value = client.get_secret(
                name
            )

            if (
                value
                and
                value.strip()
            ):

                github_token = value.strip()

                token_source = name

                break

        except Exception:

            pass

except Exception:

    pass


if github_token is None:

    for name in [
        "GITHUB_TOKEN",
        "GH_TOKEN",
    ]:

        value = os.environ.get(
            name
        )

        if (
            value
            and
            value.strip()
        ):

            github_token = value.strip()

            token_source = (
                "ENV:"
                +
                name
            )

            break


if github_token is None:

    raise RuntimeError(
        "GitHub token unavailable."
    )


auth_header = base64.b64encode(
    (
        "x-access-token:"
        +
        github_token
    ).encode()
).decode()


# ==============================================================================
# 23. GIT DIRTY-STATE AUDIT
# ==============================================================================

print("=" * 120)
print("GIT DIRTY-STATE AUDIT")
print("=" * 120)


remote_before = git_cmd(
    "ls-remote",
    "origin",
    "refs/heads/main",
    auth_header=auth_header,
).split()[0]


if remote_before != EXPECTED_PARENT:

    raise RuntimeError(
        "\nRemote main moved before Stage25 closeout.\n"
        f"Expected: {EXPECTED_PARENT}\n"
        f"Actual:   {remote_before}"
    )


tracked_dirty = {
    line
    for line in git_cmd(
        "diff",
        "--name-only",
    ).splitlines()
    if line
}


untracked = {
    line
    for line in git_cmd(
        "ls-files",
        "--others",
        "--exclude-standard",
    ).splitlines()
    if line
}


dirty = (
    tracked_dirty
    |
    untracked
)


allowed_exact = {
    "README.md",
    "docs/JOURNAL_EXTENSION_SUMMARY.md",
    "docs/STAGE25_MANUSCRIPT_INTEGRATION.md",
    "docs/STAGE25_MANUSCRIPT_INTEGRATION.tex",
    "docs/STAGE25_PUBLICATION_TABLES.md",
    "docs/STAGE25_PUBLICATION_TABLES.tex",
    "docs/STAGE25_PUBLICATION_CLOSEOUT.md",
}


allowed_prefixes = (
    (
        "results/stage25_prevalence_stress/"
        "stage25_5_final_audit_and_seal/"
    ),
    (
        "results/stage25_prevalence_stress/"
        "stage25_publication_package/"
    ),
    "scripts/stage25/",
)


unexpected = [
    path
    for path in sorted(
        dirty
    )
    if (
        path not in allowed_exact
        and
        not any(
            path.startswith(
                prefix
            )
            for prefix in allowed_prefixes
        )
    )
]


if unexpected:

    raise RuntimeError(
        "\nUnexpected repository modifications:\n"
        +
        "\n".join(
            unexpected
        )
    )


if not dirty:

    raise RuntimeError(
        "Stage25-5 produced no repository changes."
    )


print(
    "GitHub credential:",
    token_source,
)

print(
    "[PASS] Remote main remains exact Stage25-4 commit."
)

print(
    "[PASS] Only Stage25 closeout/publication/export files are dirty."
)

print()


# ==============================================================================
# 24. GIT AUTHOR
# ==============================================================================

if not git_cmd(
    "config",
    "--local",
    "--get",
    "user.name",
    check=False,
):

    git_cmd(
        "config",
        "--local",
        "user.name",
        git_cmd(
            "log",
            "-1",
            "--format=%an",
        ),
    )


if not git_cmd(
    "config",
    "--local",
    "--get",
    "user.email",
    check=False,
):

    git_cmd(
        "config",
        "--local",
        "user.email",
        git_cmd(
            "log",
            "-1",
            "--format=%ae",
        ),
    )


# ==============================================================================
# 25. STAGE CLOSEOUT FILES
# ==============================================================================

git_cmd(
    "add",
    "--",
    "README.md",
    "docs/JOURNAL_EXTENSION_SUMMARY.md",
    "docs/STAGE25_MANUSCRIPT_INTEGRATION.md",
    "docs/STAGE25_MANUSCRIPT_INTEGRATION.tex",
    "docs/STAGE25_PUBLICATION_TABLES.md",
    "docs/STAGE25_PUBLICATION_TABLES.tex",
    "docs/STAGE25_PUBLICATION_CLOSEOUT.md",
    str(
        FINAL_DIR.relative_to(
            REPO
        )
    ),
    str(
        PUB_DIR.relative_to(
            REPO
        )
    ),
    str(
        SCRIPT_DIR.relative_to(
            REPO
        )
    ),
)


staged = {
    line
    for line in git_cmd(
        "diff",
        "--cached",
        "--name-only",
    ).splitlines()
    if line
}


if not staged:

    raise RuntimeError(
        "No Stage25-5 files staged."
    )


unexpected_staged = [
    path
    for path in sorted(
        staged
    )
    if (
        path not in allowed_exact
        and
        not any(
            path.startswith(
                prefix
            )
            for prefix in allowed_prefixes
        )
    )
]


if unexpected_staged:

    raise RuntimeError(
        "\nUnexpected staged files:\n"
        +
        "\n".join(
            unexpected_staged
        )
    )


if git_cmd(
    "diff",
    "--name-only",
):

    raise RuntimeError(
        "Unstaged tracked changes remain."
    )


if git_cmd(
    "ls-files",
    "--others",
    "--exclude-standard",
):

    raise RuntimeError(
        "Untracked repository files remain."
    )


print(
    "[PASS] Stage25 closeout staged exclusively."
)

print()


# ==============================================================================
# 26. COMMIT
# ==============================================================================

print("=" * 120)
print("COMMIT STAGE25 FINAL CLOSEOUT")
print("=" * 120)


commit_output = git_cmd(
    "commit",
    "-m",
    "stage25: final audit seal and publication closeout",
)


print(
    commit_output
)

print()


closeout_commit = git_cmd(
    "rev-parse",
    "HEAD",
)


closeout_parent = git_cmd(
    "rev-parse",
    "HEAD^",
)


if closeout_parent != EXPECTED_PARENT:

    raise RuntimeError(
        "\nStage25 final closeout parent mismatch.\n"
        f"Expected: {EXPECTED_PARENT}\n"
        f"Actual:   {closeout_parent}"
    )


print(
    "Stage25 final commit:"
)

print(
    " ",
    closeout_commit
)

print()


# ==============================================================================
# 27. PUSH + REMOTE VERIFY
# ==============================================================================

print("=" * 120)
print("PUSH + REMOTE VERIFICATION")
print("=" * 120)


push_output = git_cmd(
    "push",
    "origin",
    "HEAD:main",
    auth_header=auth_header,
)


print(
    push_output
)

print()


remote_after = git_cmd(
    "ls-remote",
    "origin",
    "refs/heads/main",
    auth_header=auth_header,
).split()[0]


if remote_after != closeout_commit:

    raise RuntimeError(
        "\nRemote verification failed.\n"
        f"Local:  {closeout_commit}\n"
        f"Remote: {remote_after}"
    )


status_after = git_cmd(
    "status",
    "--porcelain",
)


if status_after:

    raise RuntimeError(
        "\nRepository is not clean after Stage25 closeout:\n"
        +
        status_after
    )


print(
    "[PASS] Remote main == Stage25 final closeout commit."
)

print(
    "[PASS] Repository clean."
)

print()


# ==============================================================================
# 28. FINAL OUTPUT
# ==============================================================================

print("=" * 120)
print("STAGE25 FINAL SCIENTIFIC + PUBLICATION CLOSEOUT: PASS")
print("=" * 120)

print()

print(
    "Scientific Stage25 status:       CLOSED AND SEALED"
)

print()

print(
    "Stage25-0 commit:"
)

print(
    " ",
    STAGE25_0_COMMIT
)

print()

print(
    "Stage25-1 commit:"
)

print(
    " ",
    STAGE25_1_COMMIT
)

print()

print(
    "Stage25-2 commit:"
)

print(
    " ",
    STAGE25_2_COMMIT
)

print()

print(
    "Stage25-3 commit:"
)

print(
    " ",
    STAGE25_3_COMMIT
)

print()

print(
    "Stage25-4 commit:"
)

print(
    " ",
    STAGE25_4_COMMIT
)

print()

print(
    "Stage25 FINAL closeout commit:"
)

print(
    " ",
    closeout_commit
)

print()

print(
    "Remote main:"
)

print(
    " ",
    remote_after
)

print()

print(
    "Final audit SHA:"
)

print(
    " ",
    final_audit_sha
)

print()

print(
    "Final synthesis SHA:"
)

print(
    " ",
    final_synthesis_sha
)

print()

print(
    "Publication manifest SHA:"
)

print(
    " ",
    publication_manifest_sha
)

print()

print(
    "SCIENTIFIC ACCOUNTING"
)

print(
    "  New model fits:             0"
)

print(
    "  New model inference:        0"
)

print(
    "  New probability arrays:     0"
)

print(
    "  Target reopenings:          0"
)

print(
    "  Threshold searches:         0"
)

print(
    "  Calibration runs:           0"
)

print()

print(
    "STAGE25 ANALYSIS"
)

print(
    "  Frozen operating points:    24"
)

print(
    "  Prevalence levels:          6"
)

print(
    "  Projection rows:            144"
)

print(
    "  PPV break-even rows:        120"
)

print(
    "  Required-FPR rows:          720"
)

print(
    "  Cost break-even rows:       24"
)

print(
    "  Sanity tests:               7 / 7 PASS"
)

print(
    "  Figures:                    5 / 5"
)

print(
    "  Figure files:               10 / 10"
)

print()

print(
    "PUBLICATION PACKAGE"
)

print(
    "  Tables:                     PUSHED"
)

print(
    "  Figures:                    PUSHED"
)

print(
    "  Results:                    PUSHED"
)

print(
    "  Discussion:                 PUSHED"
)

print(
    "  Limitations / Threats:      PUSHED"
)

print(
    "  Contributions:              PUSHED"
)

print()

print(
    "REPRODUCIBILITY"
)

print(
    "  GitHub notebook:"
)

print(
    "   scripts/stage25/stage25_prevalence_operational_stress.ipynb"
)

print(
    "  GitHub Python script:"
)

print(
    "   scripts/stage25/stage25_prevalence_operational_stress.py"
)

print()

print(
    "  Full downloadable notebook:"
)

print(
    "  ",
    FULL_NOTEBOOK
)

print()

print(
    "  Notebook/script ZIP:"
)

print(
    "  ",
    NOTEBOOK_ZIP
)

print(
    "  SHA256:",
    notebook_zip_sha
)

print()

print(
    "  Publication ZIP:"
)

print(
    "  ",
    PUBLICATION_ZIP
)

print(
    "  SHA256:",
    publication_zip_sha
)

print()

print(
    "============================================================"
)

print(
    "STAGE25 = COMPLETELY FINISHED 😂"
)

print(
    "ONE RESEARCH STAGE LEFT."
)

print(
    "============================================================"
)

print()
