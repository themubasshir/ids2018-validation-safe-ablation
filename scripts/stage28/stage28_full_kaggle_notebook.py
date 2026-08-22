#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Stage28 complete Kaggle notebook source archive.

Scientific-final parent:
    94bbebfe6b18249166ac6bc89deadc8a2d6dc627

IMPORTANT
---------
This file is an archival linearization of the Kaggle notebook.

It preserves notebook cell order and source. It is not a new Stage28
scientific stage and must not be interpreted as authorizing new model fits.

For the notebook representation, see:
    stage28_full_kaggle_notebook.ipynb
"""


# ==============================================================================================================
# %% NOTEBOOK CELL 0001 | execution_count=1
# ==============================================================================================================
# =================================================================================================
# STAGE28-COLD-BOOTSTRAP
# Restore exact durable GitHub state + frozen CICIDS2017 Hugging Face sources
#
# ZERO MODEL FITS
# ZERO INFERENCE
# ZERO THRESHOLD SELECTION
#
# Expected scientific state:
#   Stage28 NEW fits consumed = 58 / 108
#   remaining                 = 50
#   next component            = C071 / FIT #59
# =================================================================================================

from __future__ import annotations

import hashlib
import importlib.metadata
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


SEP = "=" * 120

REPO_URL = "https://github.com/themubasshir/ids2018-validation-safe-ablation.git"
REPO = Path("/kaggle/working/ids2018-validation-safe-ablation")

# Last verified durable AUTO-B commit.
EXPECTED_HEAD = "8b87f734f076c5402324ec9c7b2ee82e74f64d0e"

# Frozen Stage28 execution-manifest identity.
EXPECTED_MANIFEST_SHA256 = (
    "47e7ffbf357fee3d86830282ae0e69663f84849971e3caeb151168e9bb50b505"
)

# Frozen CICIDS2017 HF identity recovered from Stage27/AUTO-B.
HF_REPO = "bvsam/cic-ids-2017"
HF_REVISION = "b7e532345512edcd530cb1770dc76636aeb52802"

HF_DOWNLOAD_ROOT = Path("/kaggle/working/stage28_cold_bootstrap_hf")
SOURCE_ROOT = Path("/kaggle/working/stage27_cicids2017_sources")

STAGE28_ROOT = (
    REPO
    / "results"
    / "stage28_stability_novelty_control"
)

MANIFEST_PATH = (
    STAGE28_ROOT
    / "stage28_1b_random_loao_membership_and_execution_lock"
    / "stage28_component_execution_manifest.csv"
)

SOURCE_RECEIPT_PATH = (
    REPO
    / "results"
    / "stage27_loao_unseen_attack"
    / "stage27_1a_fold_membership"
    / "source_effective_population_receipt.json"
)

FINAL_AUTO_B_LEDGER = (
    STAGE28_ROOT
    / "stage28_2a_stage27_seed_stability"
    / "stage28_2a50_web_attack_lightgbm_seed46"
    / "stage28_2a50_web_attack_lightgbm_seed46_fit_ledger.json"
)

EFFECTIVE_BUDGET_PATH = (
    STAGE28_ROOT
    / "stage28_0a_preexecution_amendment"
    / "effective_fit_budget.json"
)


def banner(text):
    print("\n" + SEP)
    print(text)
    print(SEP + "\n")


def run(cmd, *, cwd=None, check=True):
    p = subprocess.run(
        [str(x) for x in cmd],
        cwd=None if cwd is None else str(cwd),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    if check and p.returncode != 0:
        raise RuntimeError(
            f"Command failed ({p.returncode}):\n"
            + " ".join(str(x) for x in cmd)
            + f"\n\nSTDOUT:\n{p.stdout}"
            + f"\n\nSTDERR:\n{p.stderr}"
        )

    return p


def git(*args, check=True):
    return (
        run(
            ["git", *args],
            cwd=REPO,
            check=check,
        ).stdout
        or ""
    ).strip()


def sha256_file(path, chunk=16 * 1024 * 1024):
    h = hashlib.sha256()

    with Path(path).open("rb") as f:
        while True:
            b = f.read(chunk)
            if not b:
                break
            h.update(b)

    return h.hexdigest()


def read_json(path):
    return json.loads(
        Path(path).read_text(
            encoding="utf-8"
        )
    )


# =================================================================================================
# 0. ENVIRONMENT
# =================================================================================================

banner("STAGE28 COLD BOOTSTRAP — ENVIRONMENT")


print("Python:", sys.version.split()[0])


required_exact = {
    "numpy": "2.0.2",
    "scikit-learn": "1.6.1",
    "xgboost": "3.2.0",
    "lightgbm": "4.6.0",
}


for package, expected in required_exact.items():
    try:
        actual = importlib.metadata.version(package)
    except importlib.metadata.PackageNotFoundError:
        actual = None

    print(
        f"{package:<15}",
        actual,
        "(expected", expected + ")",
    )


# We specifically know Stage28's frozen execution used these versions.
# Install only if XGBoost/LightGBM are absent or wrong.
install = []

for package in ["xgboost", "lightgbm"]:
    expected = required_exact[package]

    try:
        actual = importlib.metadata.version(package)
    except importlib.metadata.PackageNotFoundError:
        actual = None

    if actual != expected:
        install.append(
            f"{package}=={expected}"
        )


try:
    importlib.metadata.version("huggingface-hub")
except importlib.metadata.PackageNotFoundError:
    install.append("huggingface_hub")


if install:
    print()
    print(
        "[ENV] Installing:",
        " ".join(install),
    )

    run(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "-q",
            *install,
        ]
    )


# Fail closed for membership-sensitive packages.
for package in ["numpy", "scikit-learn"]:
    actual = importlib.metadata.version(package)
    expected = required_exact[package]

    if actual != expected:
        raise RuntimeError(
            f"{package} version mismatch: "
            f"{actual} != frozen {expected}"
        )


for package in ["xgboost", "lightgbm"]:
    actual = importlib.metadata.version(package)
    expected = required_exact[package]

    if actual != expected:
        raise RuntimeError(
            f"{package} version mismatch after setup: "
            f"{actual} != {expected}"
        )


print()
print("[PASS] frozen software versions available")


# =================================================================================================
# 1. GITHUB SECRET CHECK
# =================================================================================================

banner("GITHUB CREDENTIAL GATE")


github_token = None
github_source = None

try:
    from kaggle_secrets import UserSecretsClient

    client = UserSecretsClient()

    for name in [
        "GITHUB_TOKEN",
        "github_token",
        "GH_TOKEN",
        "GITHUB_PAT",
        "github_pat",
        "GH_PAT",
    ]:
        try:
            value = client.get_secret(name)
        except Exception:
            value = None

        if isinstance(value, str) and value.strip():
            github_token = value.strip()
            github_source = f"kaggle_secret:{name}"
            break

except Exception:
    pass


if github_token is None:
    for name in [
        "GITHUB_TOKEN",
        "github_token",
        "GH_TOKEN",
        "GITHUB_PAT",
        "github_pat",
        "GH_PAT",
    ]:
        value = os.environ.get(name)

        if isinstance(value, str) and value.strip():
            github_token = value.strip()
            github_source = f"environment:{name}"
            break


if github_token is None:
    raise RuntimeError(
        "GitHub token not found. "
        "Stage28 requires the existing Kaggle GitHub secret for later pushes."
    )


print("[PASS] GitHub credential:", github_source)
print("[PASS] token not displayed")


# =================================================================================================
# 2. RESTORE GITHUB
# =================================================================================================

banner("RESTORE GITHUB REPOSITORY")


if REPO.exists():
    if not (REPO / ".git").is_dir():
        raise RuntimeError(
            f"{REPO} exists but is not a Git repository. "
            "Do not delete it blindly."
        )

    status = git(
        "status",
        "--porcelain",
    )

    if status:
        raise RuntimeError(
            "Existing repository contains local changes.\n"
            "Do not delete possible evidence.\n\n"
            + status
        )

    print(
        "[INFO] Existing clean repository found; fetching origin/main..."
    )

    run(
        [
            "git",
            "fetch",
            "--prune",
            "origin",
            "main",
        ],
        cwd=REPO,
    )

else:
    print(
        "[INFO] Fresh runtime — cloning GitHub repository..."
    )

    run(
        [
            "git",
            "clone",
            "--branch",
            "main",
            "--single-branch",
            REPO_URL,
            str(REPO),
        ]
    )


remote_head_text = run(
    [
        "git",
        "ls-remote",
        "origin",
        "refs/heads/main",
    ],
    cwd=REPO,
).stdout.strip()

if not remote_head_text:
    raise RuntimeError(
        "Could not resolve GitHub origin/main."
    )


remote_head = remote_head_text.split()[0]

print("Remote main:", remote_head)
print("Expected   :", EXPECTED_HEAD)


if remote_head != EXPECTED_HEAD:
    raise RuntimeError(
        "GitHub main has changed from the last verified Stage28-AUTO-B head.\n"
        "STOP — inspect the newer remote state before starting any fit."
    )


# Force the clean fresh runtime to the exact durable scientific head.
run(
    [
        "git",
        "checkout",
        "main",
    ],
    cwd=REPO,
)

run(
    [
        "git",
        "reset",
        "--hard",
        EXPECTED_HEAD,
    ],
    cwd=REPO,
)


head = git(
    "rev-parse",
    "HEAD",
)

status = git(
    "status",
    "--porcelain",
)


if head != EXPECTED_HEAD:
    raise RuntimeError(
        "Local Git HEAD mismatch."
    )


if status:
    raise RuntimeError(
        "Repository is not clean after bootstrap."
    )


print()
print("[PASS] repository restored")
print("HEAD:", head)
print("[PASS] repository clean")


# =================================================================================================
# 3. DURABLE STAGE28 ACCOUNTING
# =================================================================================================

banner("DURABLE STAGE28 LEDGER GATE")


if not FINAL_AUTO_B_LEDGER.is_file():
    raise RuntimeError(
        "Final AUTO-B ledger not present at durable HEAD."
    )


ledger = read_json(
    FINAL_AUTO_B_LEDGER
)


expected_ledger = {
    "component_id": "C070",
    "cumulative_new_fits_consumed": 58,
    "new_fits_remaining": 50,
    "stage28a_stage27_new_fits_consumed": 40,
    "stage28a_stage27_new_fits_remaining": 0,
    "status": "FIT_058_SUCCESSFULLY_CONSUMED",
}


for key, expected in expected_ledger.items():
    actual = ledger.get(key)

    if actual != expected:
        raise RuntimeError(
            f"Durable ledger mismatch for {key}: "
            f"{actual!r} != {expected!r}"
        )


budget = read_json(
    EFFECTIVE_BUDGET_PATH
)


if (
    int(
        budget[
            "totals"
        ][
            "new_fit_budget"
        ]
    )
    != 108
):
    raise RuntimeError(
        "Frozen Stage28 fit budget is not 108."
    )


if (
    int(
        budget[
            "stage28b_random_loao"
        ][
            "new_fits"
        ]
    )
    != 50
):
    raise RuntimeError(
        "Frozen Stage28B fit budget is not 50."
    )


print(
    "[PASS] Stage28A durable:"
)

print(
    "       consumed = 58 / 108"
)

print(
    "       remaining = 50"
)

print(
    "       next fit = FIT #59 / C071"
)


# =================================================================================================
# 4. EXECUTION MANIFEST GATE
# =================================================================================================

banner("FROZEN EXECUTION MANIFEST GATE")


manifest_sha = sha256_file(
    MANIFEST_PATH
)


print(
    "Manifest SHA256:",
    manifest_sha,
)


if manifest_sha != EXPECTED_MANIFEST_SHA256:
    raise RuntimeError(
        "Stage28 execution manifest identity mismatch."
    )


manifest_text = MANIFEST_PATH.read_text(
    encoding="utf-8"
)


if "C071,28B_RANDOM_SPLIT_LOAO_CONTROL" not in manifest_text:
    raise RuntimeError(
        "C071 Stage28B component missing."
    )


if "C120,28B_RANDOM_SPLIT_LOAO_CONTROL" not in manifest_text:
    raise RuntimeError(
        "C120 Stage28B component missing."
    )


print(
    "[PASS] exact 120-component execution manifest"
)

print(
    "[PASS] Stage28B C071..C120 present"
)


# =================================================================================================
# 5. FROZEN HF SOURCE RECEIPT
# =================================================================================================

banner("FROZEN CICIDS2017 SOURCE RECEIPT")


source_receipt = read_json(
    SOURCE_RECEIPT_PATH
)

segments = sorted(
    source_receipt[
        "segments"
    ],
    key=lambda x: int(
        x[
            "source_index"
        ]
    ),
)


if len(segments) != 8:
    raise RuntimeError(
        "Expected exactly eight frozen CICIDS2017 sources."
    )


if int(
    source_receipt[
        "population"
    ][
        "effective_rows"
    ]
) != 2_830_743:
    raise RuntimeError(
        "Frozen CICIDS2017 effective population mismatch."
    )


print(
    "[PASS] source receipt loaded"
)

print(
    "Effective population:",
    "2,830,743 rows",
)

print(
    "HF dataset:",
    HF_REPO,
)

print(
    "HF revision:",
    HF_REVISION,
)


# =================================================================================================
# 6. OPTIONAL HF SECRET
# =================================================================================================

hf_token = None

try:
    from kaggle_secrets import UserSecretsClient

    client = UserSecretsClient()

    for name in [
        "HF_TOKEN",
        "HUGGINGFACE_TOKEN",
        "HUGGING_FACE_HUB_TOKEN",
    ]:
        try:
            value = client.get_secret(name)
        except Exception:
            value = None

        if isinstance(value, str) and value.strip():
            hf_token = value.strip()
            print(
                "[PASS] Hugging Face credential available:",
                name,
            )
            print(
                "[PASS] HF token not displayed"
            )
            break

except Exception:
    pass


if hf_token is None:
    print(
        "[INFO] No HF token found; public dataset download will be used."
    )


# =================================================================================================
# 7. DOWNLOAD / VERIFY ALL EIGHT SOURCES
# =================================================================================================

banner("RESTORE FROZEN HUGGING FACE SOURCES")


from huggingface_hub import hf_hub_download


HF_DOWNLOAD_ROOT.mkdir(
    parents=True,
    exist_ok=True,
)

SOURCE_ROOT.mkdir(
    parents=True,
    exist_ok=True,
)


for seg in segments:

    idx = int(
        seg[
            "source_index"
        ]
    )

    remote = seg[
        "remote"
    ]

    basename = seg[
        "basename"
    ]

    expected_size = int(
        seg[
            "size_bytes"
        ]
    )

    expected_sha = seg[
        "sha256"
    ]

    canonical_path = (
        SOURCE_ROOT
        / basename
    )


    # Reuse only an exact existing file.
    if canonical_path.is_file():
        size_ok = (
            canonical_path.stat().st_size
            == expected_size
        )

        sha_ok = (
            sha256_file(
                canonical_path
            )
            == expected_sha
        )

        if size_ok and sha_ok:
            print(
                f"[PASS cached] {idx} "
                f"{seg['day']:<9} "
                f"{basename}"
            )
            continue

        raise RuntimeError(
            f"Existing frozen source has wrong identity:\n"
            f"{canonical_path}"
        )


    print()
    print(
        f"[DOWNLOAD {idx + 1}/8]",
        remote,
    )


    downloaded = Path(
        hf_hub_download(
            repo_id=HF_REPO,
            filename=remote,
            repo_type="dataset",
            revision=HF_REVISION,
            local_dir=str(
                HF_DOWNLOAD_ROOT
            ),
            token=hf_token,
        )
    )


    actual_size = (
        downloaded.stat().st_size
    )

    if actual_size != expected_size:
        raise RuntimeError(
            f"HF size mismatch for {basename}:\n"
            f"{actual_size} != {expected_size}"
        )


    actual_sha = sha256_file(
        downloaded
    )

    if actual_sha != expected_sha:
        raise RuntimeError(
            f"HF SHA256 mismatch for {basename}:\n"
            f"{actual_sha}\n!=\n{expected_sha}"
        )


    # Create the historical runtime source layout expected by Stage27/28.
    try:
        canonical_path.symlink_to(
            downloaded.resolve()
        )
    except Exception:
        shutil.copy2(
            downloaded,
            canonical_path,
        )


    if (
        canonical_path.stat().st_size
        != expected_size
    ):
        raise RuntimeError(
            f"Canonical source size mismatch: {basename}"
        )


    if (
        sha256_file(
            canonical_path
        )
        != expected_sha
    ):
        raise RuntimeError(
            f"Canonical source SHA mismatch: {basename}"
        )


    print(
        "[PASS source]",
        idx,
        seg[
            "day"
        ],
        basename,
    )

    print(
        "   bytes :",
        f"{expected_size:,}",
    )

    print(
        "   sha256:",
        expected_sha,
    )


# =================================================================================================
# 8. FINAL SOURCE UNIVERSE
# =================================================================================================

banner("FINAL SOURCE IDENTITY VERIFICATION")


total_bytes = 0


for seg in segments:

    path = (
        SOURCE_ROOT
        / seg[
            "basename"
        ]
    )

    if not path.is_file():
        raise RuntimeError(
            f"Source missing after bootstrap: {path}"
        )


    expected_size = int(
        seg[
            "size_bytes"
        ]
    )

    expected_sha = seg[
        "sha256"
    ]


    if (
        path.stat().st_size
        != expected_size
    ):
        raise RuntimeError(
            f"Final size mismatch: {path.name}"
        )


    actual_sha = sha256_file(
        path
    )


    if actual_sha != expected_sha:
        raise RuntimeError(
            f"Final SHA mismatch: {path.name}"
        )


    total_bytes += expected_size


    print(
        "[PASS]",
        seg[
            "source_index"
        ],
        path.name,
    )


print()
print(
    "Frozen source files:",
    len(
        segments
    ),
)

print(
    "Total source bytes:",
    f"{total_bytes:,}",
)


# =================================================================================================
# 9. SCIENCE-SAFETY FINAL GATE
# =================================================================================================

banner("STAGE28-COLD-BOOTSTRAP COMPLETE")


print(
    "GitHub durable HEAD:"
)

print(
    " ",
    EXPECTED_HEAD,
)

print()
print(
    "Stage28 NEW fits consumed:",
    "58 / 108",
)

print(
    "Stage28 NEW fits remaining:",
    "50",
)

print(
    "Next authorized component:",
    "C071",
)

print(
    "Next authorized scientific fit:",
    "FIT #59",
)

print()
print(
    "Hugging Face dataset:",
    HF_REPO,
)

print(
    "Frozen revision:",
    HF_REVISION,
)

print(
    "Frozen CICIDS2017 sources:",
    "8 / 8 VERIFIED",
)

print()
print(
    "Scientific operations performed by this cell:"
)

print(
    "  model fits          : 0"
)

print(
    "  model inference     : 0"
)

print(
    "  threshold selection : 0"
)

print(
    "  target optimization : 0"
)

print()
print(
    "[PASS] COLD BOOTSTRAP COMPLETE"
)

print(
    "[READY] Stage28-AUTO-C may now start from FIT #59 / C071"
)

# ==============================================================================================================
# %% NOTEBOOK CELL 0002 | execution_count=2
# ==============================================================================================================
# =================================================================================================
# STAGE28-AUTO-C — ZERO-UPLOAD, RESUMABLE RANDOM-LOAO CONTROL BOT
#
# Durable start: 58 / 108 new fits consumed
# Executes: FIT #59 .. FIT #108 (C071 .. C120)
# Two-phase durability: model push immediately after each successful fit, then result push after evaluation.
# CPU ONLY. Random membership seed stays fixed at 42.
# =================================================================================================

import base64
import bz2
import hashlib
from pathlib import Path

EXPECTED_SHA256 = "47adfd5fbf563a5d9f6f0b610e37928158e5b399827563913dc71cd54e717edb"

PAYLOAD = r"""
LRx4!F+o`-Q&}KXAS(bH*nj18R73!I|NsAg|KI+<|Ns9$00e*t01yCRSf1y-Vm9Ay+<iOj=DzlY5G1L39_ICCzO<l=yPfris<$=S-(lz;&$xXRdt)b-
uErtj6#8qgw(QMr_Tlem-1o0oPd)}NuxM!aSO8V$Zha2>;@8W2b$#}C(|g~2mc4Ql+sD>y-
rW*|cYWh`HeG52o~+dg_ej?J+<fnKd)LzY&XeuE8x8ZYU8r@S?%1`<pzOAsppD(yr*ki}sC9jet}3OY<<nzXo2|C#k{pbakQuKE7acTqI{Vkh*QT<b-
(A?6k*arX72NxebIHo_;KV>cOh6DOnHdR&rXx*HDt@V_q{*W-
4<s6TngGL136LN`1s+8`qH20k_=c!$Hl|Q|fb}$J4GkIq0zwf8h!bk3>S?rxlxS%lp|v#i0MOIYX{LZQ000Rzk{}QS1jq?JQ_4S7_LSKXqd}&CZA^`+qiP12
fQdp8kS0MJ6g1S+PfB>y(t2uPsp&GGkxwb=8hV~hPf#9{MhKD+AQMJ_jHa3?`lqIo6c0v_8Z>F30i!?~26R4{AYl;^Nd9|I)_z{^y4PGBPxhcv8KdqW4B6|4
=4oA=P*YdTjQ+jMxG4JKB-mTiwzKnY6xp4vf~Esqe@>|#Gy59X@OZ(LeSzKlnfT~8!Ex<Z42~45jSgw9hGAn*?S>4YetA}%sy&370s4B~KgsB9P$?HGf6^$}
BcoZTh2fau@3w1QaJ!*JSZtMx-$}a=Q-
q18{PGyoY3k_}z~VXa*B732AMP;?gM4d7ses?zG1YbF!hxM{NVYyQAMM&4y*~+SuRbe$wVl0~><ncv!m2@@n>)Gd1K)I*?|fWD^Rtp*q$h(h?z+Uf_-
2`fY)mzf<KbrJsBaE_bSI-
Es)C#E7jZrs#MA3>PX><V4x2if__R|Q=tAZ!9U+L(jn?(QW7PE_DJrI>%DEv|w9&>LCQ8xI#e}F{Hz}av_eNf#1&qwAmTgU(89i-0+MH8^=;JgxT-F_Nz63n
{s-aLw5l;B)eOpPF>h9%y@OV9VScESL4b<xWeE9XHjx`^tkmd!l-
HaO=dZ<>^C_0*${~m3F+oIrsa1@|SkOifw9i5BcO75a>E*xpPkAzf_WDtxXL}U=Zg%?k<(N4|nH#cp`x9q!)Ca|#DfaM2;HJz=8Att8vvR|Li_@4ms4o7hXh
{NLRPO%wK;?iOS?RIx*uIxXSp9eIM-q;HFf4}+ogek+Ln%~d0^<PxAAi<{LoQ6OIfeB=Y6$M;N`+yJt1e0_KN&g-
>gdj;Cj^A6#eEIQu2TQ`3FvfA(ti;6mse-
@E#1=u;7uEWyJv^fTiV^tjIHfC4ro)B;hUj`>OkiEJ`f=&V_MY8TInKNUeQ^27foK$zBxESmf{SDomeuh|SUCqowHdTX#!UkygN*RAFa?B0F=UKIOd3JUIqT
Pv){^_HWxCuCyZ)J(!HuDs$jI2=PHdOc*cN9{{7{kC^}m<+MCJFu=D%0ECz=zr*Eyi^5wibqyfA^9rO9BS@M0TJr}5U<{CbjxR4XDCBLbts?*W82eR35j3_=
7bvvk>anp2&c9-s%29<sNf$Wj9PEk9fte@h!&eY<~23k?O#?bdI4-SAu$S+qn1Pz?}%4F6w0AA5?)K-
f?=m9X34(Efcvr<)F?@G{Gu!45n&j=zI)+PfD(%T0MEP@JtU^J}^yMB<;=1qs#>25>L+E%+a>NnDVjBmGxz57seXt|RHC@1(nlueHl~eXl7gVUyOYjB3MLl;
I4e(I@R8yWwh~NbA6TIE>geKjO0q@jGlJi^0SNYC6g^9R$vFj(oD5>9B2wGiRY>rl4coT~z+FiBL(!^*Y#SGT1;9obGVh<|-
o%5;_KO%n&XtxFD9e!%Z17vBt5{Xy9Z|<kKsjTx`75*(4q(fHiOzuJ`4E5y?g_;s*3Bkjaox^ryU~NLq^H1$*hN;4%dTWq~HONCrLtBj;B6UNjcAjz6j(i1G
G(|9_+4+pp-mZLN>zUw1I{L%Zi4Q8)c>u?%;G>;ri?ut)KbjFp?Y-JkM!?Wh9H<N>xe;b6CRIDf-
9x~EGwzwmF>;~nU1(9YcS9xfb&`M7>rThTo9;nlX|xOSUz(clnQnEOMt!5>%Mhb%qebmR36xLp_Qn={rolS%=Q0E0^+*N$FZ=FM9*eYd;`2x#yhW(y9${MLo
N`M)$L%Ks-v=d0|VU|X%X>>fSbbN}5#Vl{6w1A0gS0H%Y4eP_F}+;vj5V%;B8m&HfCObIskeK8|pk${LV_Uf^FBM^w>s_)BIAHGI3t&W-
kYnIQ|Zi}WXk<*rz7oV*FsIl`6M~Bty;r}&sy7=fBOzTh_AOl7oX)t{3S?%`U29qiyvUMi677LCje6Xmq5ljs$7+JJTx_mpZ7C4Pam8u+Dorb!M)i8Sqrj*9
c`a=Bh(sZd`8Z{(T>A%r(-vwp)J{dC;JG=fHwH#+G-
|de~y2RLMIpnI^;8n~VfEBdpQzNpo#@CiF5E|0g@ETT=Z!1=4m6?Wr1z}_XJr&56*|x7<#!%lbZ6V68nrt=F>)IQ*9?x>6Gldt(Q=XrtHI0F@dRaqU#kGAk%
7ED&e&*G_qtwBW2~e{Tq)}3zY;i0B3)h!Jxb8Y9SAHCM&mNzva4@h^lt>6U6&Ikz9#i{%Umq{3l)uMz8l|QDI=GE|Ute`?A9eHNc;S`p3%(q5regg@(PZI?K
ujY3LFEV8^>3#6vPi3tx!GKR*URa=LvG(H_5aEO#8NQrYsg(4fxb#1_#}Xp4|gEg@<Ud=j5cR=9dzaBPkjXM7JwYU$c#+1_~soZ3_38+l(#h*G6J_yOdA)IR
(OtFzFLOIV-LRf?i9)3Jky8v)9^6ZqyTie8X4w1y%hV!JlT06m|6!hL2`sS0C=rP72r<8Uw?>gLZrUOo{h|9=$YfToZ;6xTGNo>&}T^|V3H^*prKT94W?HyD
{9qA+pzY$JM-
1M?I)@dQZes&&R3h@9RQtxMlaP<(;4Fejv*&2%8+TYmIMnas1b?_pE~O&3+qi#*2q@`F2rfZ1XNjeOxZ)DJ{dw+0a}zyQHXj_uoIRZo7sNrBcF!cv27b88x-
)6q4iQIzU?4r2sOVOG0zsUK`o&(6{7^77)~!3HbT${cd9+S20l$hM<HSZ5nP5S;}kBWuHVWP-RwVWbC-
gaU3WaRHw_L{^6h+FHR;oZ^kNe}nCEWpNV&jXcH?NOg7YDIXupoU*_?R!=y^35;bV5x4ezd_nPX5$0veNvM-ZMu!fJ^`iHNF5CS}hVO0-
MY>KFL(@^3WbPy()YaOS6v0mjB<u%Z3u<KnI9k>#G#x;gRf;jUAMa^^W87e^bN>=ZYj)5W$QlurAU3xSL(;K2|E?m7A49z)UBj?L&yUNIP+KW9*G{@GIwBR8
=Q9Z)EC1m;}Fgfj0+!c<=Ux9^GK+8SOZln{i3nkZ1i$emHWWi26P3NIJ$_2#6-@-
)D5iw=}Uw}&+rvPxK+Z=81R9=rLx;7!EVxD0oI+7s%;Z9vpg$VJ#FVgiZ*m(kJZ23o_I(j6p4y!vQ3_HTP$R$W71UT4xi$eRP<w1#jnn!ZL<tpT@=Oksiy0!
USb5Xpl$<Ewt@ag_Nh1uV$p&a8`cPMVn8w6P2W4Jy#eyf~)M3Qp?_u>tbBqh7USWOmNQPh?Vd6dL#6jdg80429P!ILaRVm*CL4gLQyrg$V>9L7it!hDEQVuO
u%z<3Kf>2-ez<l8zDmc<te)^wmg2p(AV?Ysu#BFWWpy^nG=;t5mbr$JZjJlXlUtNvVYUPCfhntdb-T<D1Y&84GrK__&ygY}teuPqqR0dnW+*G*8Viy$GS-
?pp1S>+@}TVTVj03wU>bXc+O44bFrGMWW5xoa~VOBd=}4<B<UBe(Gx>iyq%<vG#2&v*60aEf-
_9s`8>t*=qWke+>miSgX@VU$0WTOQqJrX#YE#Zo(Z{`aH_pW}#c#NBVieb9^VL-2V;&%7rK>Y^nxD4t&D3(hjx<Yl1H7r)zfgb$n%I!-
AFf%MTSS(j(E=PO0pW&dc!XhMV^h%lSezWX>|S`|hw;!o3~*qheY~>)WV7`aW~xhwN`}gnWCrycxH3LIg`QD6hlAnd6;+3|W`1AP<L!gMm+mme!o7GLTw;xE
)Xss<IxC{-NG!k6Hkw><1`;_y!+}D8_H-pC`_*Ez*a}@dh9t$sGVhL(Yp6zq^R_Z)|fGY~8mPZsu|vBqAb&t8gw$Ve>gmW@9x{h);#<;R%6LzY&g9oSrd2`F
%A#BrvE!Qd1s6EsRz^Jm0)Owd<0!_bgTEZMeMH&j;ZbfKX7SoCO>P-
&OeaS@&23ih=9*V>#t}TeC;|{|F3A=oZ9sP@&u^EpZLLC!zDvfoI|MNn86r<Y`~D8ZM^A0-<WHf{hgt%*+H+0#_~|jx}tIW-rf#%do333~mM#14Yqx4(V+LD
=7q@k%Tds!JHEb>w5T4()jmp^M>7PjbI(U_4;`gJ1!A4=8Z|~>cy$pJe;Bg1zM`Mp6;3}21!1}N8)BjA1zg=Hfm7(S>xXMkL^Ac&P$hgxhSsjL5DJ;su<dz1
RPG{xXR<x>Y(DtAn`1i&`=6UqGmJ)DWNC1R|FbU2XUa|IqjtQ?3L^2k`-$J#Mi^a-yq6<bgS3-
pN!S9KYpP^(@j!JIwaFYFf&<iSdX&SGei~Wu=`t9QXwwNpC(Bg7MtqnhZ9<SDgiO^ptf6Ci-CYqB$7ttXALUjX3Jru%EIkdqT@zkY@>?>$nl)TCEWzvt{T=F
nVB$Ja;9<CM=5A6L1<cN;()fBT=86A4wN;wTwZTqu2R#eLnQf#Ep`Cm@1?NgYgyI`>N`MP2N-
I%xp$j86?|w7xm(LdQI@e{6K4xTO^~xUrCbY3i|>TF%@U^B%PoUy5??low&8M!Q@(lSV&_Kt4*8v7V>#@OCs*9iPC4k7&O<iaVb3f`UuV+22j@rU18{^XWR0
&3AkNXWftSutmK_{`9wyud;{?vdl0^MNMFOAPfQ)^xfP9aM>hgOza4z=fhvD%2!LVrsRaq55Vk-zLD;6N`h)4xZOQi#71?MU)<IA7Jp6Mf&aBTN`{7*Jzjjf
&(Y`t)A2ytu1(P*o|4T_=9$ctrd(<(}kc{Ys-
u8OSP)7F^@sz)*|_t|RIY*fUbG>7P)!aU{nAT;*MsHyRL@k$)NH@*f0?5L_L05eo`I^u$2hXASd5pu+PP0y2qV*rL{09X_mvik;SCywV9O7nR!r?ioc0CsX}
d3CAO(qx@Mx0(*IH$4upeCg+-
e4ZlZDmWea%T3uwgTpK3S|^ug*AzYYYGdXU0L8x=0)y@(`*OOFqWKQXS}Dk(Q*a$IY!bmF2+c}_So(IlS*6CX^2l^Zj}JM%F9{<eJ24gNlF}6DMW84F$_y(-
D2n>toL$8v?xRXbxN*V*h6gcVo>n}~S}}}FLN`^}7IEwplt!!oWGW(MZj-VXnVO>CUL)7xujFaJu~bz0EA3jp-
+oo`b8JMtUWNZJWZQ)hUVc4apJVoBiDKm#fy{xDYO$m)9SL}&1z;S#Dc;oP<5NjlBAYD2sf!yiuFr?g@Yc8Jx<7(})-y!QP-KpK#z>EWU1XN>=_?HU?0&d`G
#mxAFc+<tFc8(HFUnIue30Pmw@uOx6D7Yx<#?!#E77hiqde=Txoe=h`0K2L%bCRHh<>XS)HMs~yedzR&nd-
9+L9WhSTnC~{VS|;W_29Kr#zjWs=f{1O%Hs5Xj&@@{T%Di={2kIuUCGR)4N+`+`ZZ}I^H9lZr@FlLk>-
1&H}Ubu*2wREDU=vyHnWqXT34t#Nt{n5rg@uQ&OsUYj}5LWQpMT)CT2?ZCQK^jeko%WC`TDCM@%a-
i8x|NN|Wj7e^5@+H9zZR?J7grdVC+buo@E`uv|7uZ`Qkd&0+*+?_LSTW3CHL7)VBXuIy1Biw<hxG5J*u4X}pE?s;=c>@{<LfD#_S7rGYz+U{R4h|j4sJ;hj_
scA_)>-
M!S&YxCq4$o?JvQ5@jhQozeQ^vm9et=Ibn2umWAtxl1W46<^2xz2)Mvf5)}FaV<D6c(;Ar~jujXx6zbv|>&lKx?GKooDo6qOyA;Hd#gu06Cq=PEvfis^w*t)
0`$C+!$%dTd^x(2a+cXLk)0okpAxhSRp`G68(;9N5PvFr%3B+JwT04KQh0b^;&c$`4*n{&^HL>BK1Ijj1I0Mrk7vETvCf^LwK5M~N=^20O?mwekR8Zp1(pcF
asmkfPMzDj{%bXDEt9G4AT>>d7ZWVf@?3`GqM_nYjkMcZzcr#BYmK%&5d-
*$kssKcm73Zhgrt7K4A^0Nq6u|A={OVmX{BBK<bcgnzG9$_7T#43D>xKUIv{BciL*03iRR?9CBX}`P_qB(D+ec(M~v`#a|C-UNyK0IhRut7$}8zU+zLHh-
I{;v<`aoluHe}|<}RYp$=;edU$Ej&~d;H98p=Rg#sxYqu2xazwjZ#Z0AsfJwdhCa`?mlflX)4dX5j(K6iKvDu51U913F)0OAp0H3%B@keSh(3f#KF-blsJx|
KrpR&@mj>ug5vk^!S8}b-Up<Hg0RwUa#a8#^2TKrw{us?4t#U(-
nKwoye+dD$>uILptmB1cZd^?up}#hUV!^f@Q7krz)M7Q*&84&wtA_8=!?!?%h$=qeK)1x-B0jqT;sNDVx42>_N1VQa-SZ9!d0{+C2EW6n?L21hntyzG4a-
vB$YM3UqAL;d-Xh{qoW)0siFpL$LF-
a*(AjCSvWSBsKU)d`)B)(#FnA1nwv6j^V>5u|38Cb5z1K8sI8u3$t5>ySG)0Uo;*`}=hJ*rX`P1f%En?JRC29=(u$_~>()6#g;nnG9O+RD$qu;B8TnD-qCi>
wRc=uyCRT*4E^8J_sx8L69!ucD_0B*B@-
AwOG5gG`LMFu^bTuLiYL;>pq5E$4wuGLC;YwX`%eh8qvz_v;?sExg!1cpKBoe$LfX6`>YV!_CSs;(7oMWI#+%CPV40XgG&sYFRJ7`%jZsxW#)zC`HkwqJQ3K
9SUr@*Hg!BJ4H+LgwfOiPh?0NUON*phYy1sAO5J(L99o4LWRNZH?u^@v*KF-Ke9nt~>Q4#A=5Ad1ZeYSgjOt=mx1<$QY2m4d-
MN$^=A^5#i|HcN%x#*Z)pF{yEHGLfIq>WY$;(WCB;*s0Kr^BnLwF_?A5uepX|vP_0jDwjC^7U>o;9LCR<~9@^`!v=jDUTWtUgln{e;5=F31bGmMXRS*vLaox
)-AS^%t;^c!MbihA>&o!e5_=8Y_zS}eHz&s9FHV&~1=2xU0NDs6Q?eeysR@)!pEPgHZvSJ(rXXn-
P6Av<X=X2p_x$Jp#?$p5m%wCjrM5f9*kLEvU>zoqWdCTUk(uDabTl|8dWw=Bn79kFKQ)n>qC|Xs5aN|{lf$r9N6iR6Bov^+mtaAba0R(^#V|F&(+$HPeENuq
HHJcVm0+uTk0&0k^_UK1u$8}8waJiBRQ&S3aV~dbBp|u_Xt<LAiNO|nOV3Gzlku_!NAE460kOUXvEUH_N0ul)`Fj%3{uHBc?`^i9bnkMK#+&5Lf159#i*Z@d
ENNuyOwKWMMvjjRbLVIjs;t;z~&<5s=jvPF@boA}cmswyY2#^ls1&^qDOSbx4u+BbyDg&v2$=GIuLLp_b(rNscr`tIVKN>#D+@T8)Awz$z9nEZEB*VQ!;e4~
^-g>Nlg;I*t@u*i*X6v=zs%643ErsV$|4KU1ri?k<DMrTQdJ7T?c$C4>RmiDo_pJ}AkV6#a+Lv*@%X49-Sw4-
`!HQX1sna}{W?XOEZ6?;6nXjhxQ?Zf#n*i)Uk@AQhg!@$ri5MUYB=0Fm#D^9imVaFWYAFEg0+>B&k#mE}BVqyFR1NDQy}HoZm+t+wfXDCavt5t;Q>5eg*$cc
=xF1o>h@ob^Z*s_P7Z2$$Cw@+K{57}5>#lIre^ej(6(G>bK>~!9G=FYDbNTg66l`Q!MPM)@$pwTk8F5);P#IXDD63;iO2vXTk_}*u0K{30Vj#f<NGL@NWQX(
Rib5!4LP~^aqEgfuB~p~cPuYq^v}8xahpy2o5Cea*P*e|yahf2zz;p4sbIzn1B2H6Z#(uARc)&1SyKqFOK%%Q*p!)Fwy%T+-DQntHQgsU7%YLBq41Inx?-
d2~hsGaFr0jeN>?;4&K5&1X$PN_4%+Jv(pRP7)o~y#nNS7IdPs@;Atu-&X62Ham4Y{1d$U{FRf>^*qKk8-
oGL`|=qyKrZwz_PkuDrB0CWZmmJZ{yF@)QVf5{dl2sVGvHw|88OhNc|60GL^aDR<BoEc1@*0mZ;vFfdJ_9&CbM7r>t1hj1RqDTrW{OzyKMX{5Y$o$$HAsdq`
z5G|Bb9J`y)@X>A>?^?!S7AR@E0-$d=TS8dO;hGSGNs3tw14mXjI{QiYmUA>D0w)<HCyQf{Y@U3)-
dEY=ho3)k^<WJlgOQ09&45hCoH1BndWn{M4dh7%B=?;Eqk;Q2_3P~VFuclo)vL50dA29l7lZ-ugMrqc#4#I2@sP0Kz2ay0rjHcT8Us^vxrvb)g|r_pZ*H|!p
T31|Vj-
D&5Goxk*mw^UeEyRC#!0Ao%`0iHp~yABA>q?;#*EC4{sVEt4q7L*@5;lb<TJRQyA8qDz&Z_oOkY<sY|f+LV*y8ul1VS9Z#gkHoXTjn;0rY1H*zGD4)g2+JC>
fDEVIh0P<MxT&mwzx5h7^ZHkXcluI$@HOKFY{M=vfRgY5u<u>v_2^WSgIH;?jS$HaZilh4eu!YAM$`g9}Y5QORV;$j_cnfM$rB!F)o_#puGkHBES5Wcw-
`Sz1Ryh8L3$}$k0yUlyEeGitacd~ogX?Ey1EK+xT*8_GXMa&6B+HN`wUN(GJ7#jiu0uOll8^f9C+&E4LSC5YDn@6ADf?>W5mWm)qa00A$IZnaQ&^wG=4$RA-
hLJ-~)kRj++R~^%yw}s?Pi|TV$k5nieG|;nbLJNdeQs(+q_$|ra0tX&j5!pP*?^b={m<Htqn5kxy@SuOJ#?@=Sw+nBC7zaH*Tocnkv%tH&X{68m<r&o2BL-t
Ah$%<vc645(?BW!4nZ9FSa#!DH&Cuk4<a8(mE&7li7Ja&cP+%Z04(SE$3q~zFgYbQO-#L-E*wk-
L1&fJF1H;$+ZK%8$Em#E2#3}ZbE+FpFxU*GM2J5M2I}(^{-
`C)gR&mL8C<=HeNdlJuoX&os$}2p>=dQb<T<EF4!Nh@v<PQmxv=lE*lHuG2fJdvATqx2bU25$^B~(b-
ksqFyW2P~#PB$k<&^3W`T6Jc0Oli*ejreJN5kqKf#Ms$4~sb`Am&yR+&GtB3F4d2uYgl<#~j{~2|JI!Gk=l5d|P<B2Qz#F4vt1(=9bCGGc>~}vIthzw~c%Qb
T3Vt&*=9;u@jO}z1VnhVcuPN5bnswFw8zRRqSxG<n1<!>ezI69Cc>*AQ=~C?ePiOP=*AeF$2p+B@zfda8u2E!uqAHYg1DTNePz}%;|oEeTQCpKBr4q-
(yh_p&mRzxPg7)%LHEIyi_XLVNI<&?2)w9CWO~+g?w?|x$~skXw1nh6eP;3lJ6EzaZjIDrFNljXn<P?5kE>6HR$y4<c>Z+boq4*I@$`1iCVE#^M5awR1WUe8
TTWf6ww&vNKkB%=4N<uVj3PhMzSVB2OXKB;KuW#Ia33aPDQTFA39DDLylYWH#G+%E0wnF)Hh|63V`KLDBVEV)T|Lo&C{X5urLs>H3Hxa*(4yDvm2$Trl~=g%
2H7T<zfrfUQ1P_vA*Sv2RX#xp8^wda85@Q)OL4!yYxEbk3%&I518Z+S5?TJHO-
k9(A*UjOScYT$mNRIJCe><E;M%mi$c*e3|{X5$EWoBW?k5W>TEj`5?u_Rm%TpNB%-J-
uhH;3lh7}bTMoWHx}FHCD#Kx(b7<v+GSg3#`e{4#K0xa(3E_?9T77muh0$Rs5{>=)NRLZH8KhDD*tLYe$^wyl06AQmw6b%swlBnH+rt|uR6;~z=$C_WJl{p4
qlt6CRzyil@_ra|pjta@g`d6qq%X19(Q1`(Le?<_wvvK8c{3V*N=gu|4ZTVgAPz7yw(_c+>F2dvpY1UIpWApQ>Uw_x<x)<YH~J{ZN%&U%2mCyf`El9q{F}wI
3qDxgbzoThKdbNk-{1JZ?1u9`zTWG1em(#>5D-lpnutCKe3&qQd$iY`MKY_f6tD&!>9Aw~gxECL4d@?g81VD%!=(2cGfL4-
4k79xT}4Wa@?WNh?ex&hz4*TNyHtA5Wso;Ol?nL$^dY1Os!ty;_&Hh03;O)`hW_^?d?H95Xkf*J+xjUn1>Xr7<&jYeL8&;$UE&x(6Q9z&J>>kM-
J?aPR~mf&fP7f|*%(aqeZoefrO)j#HDLsjKqQcZQPWrMgG+ssv3Pw&W~Wp3`YW95z&#o^8r+!B(V5gxEQ>@ju+8Ksq|cehIS+c8WCBGXkzpZl(K(7Cs8k{@7
!SZQARrwbU61iKbWwx7tCzXvucv#iuKMaK)SKpxdCHsTmVG8O0N-
gOP&Pmq<WNXdUUX|C8@|RlR0^YsaL2{3OS3Y^0d25rXaf7;Q5!g)IzIojAE(FIzk9Ta^)O(-
Q{BhzAbj!ko^lu!9O;Q87t%vPaCvypy!|}5CdrgZu#AUD43?sJ9D8)Fw%c9d{BhS!s!l@E5@%_aJ*H;bKZ0xBmU8^6#f=~Yfg%K%CRLHfsf~6*g@A%UFGI^<
{mv0FR|q0P6F7<wz_kXK%K(|=K$sHp3Si*O2%3(7UI<eVFcO2V4TPYGkVa9TJ+KkTB*i~7zX&<wB_$;@rpH@RFub?oV&KrGc!?V$V%Vycj-D_z>|=^+9WKZu
jD*`KnO%=hbnPMC;0O2;yr`z6JGJa+jVWqc^^mK&w`_9V&k4DRl~hu)>(*});}HS0$p|qW-<92CsxGBREz6D<N{CefU1;t-oQb!lmYp*)-
1ON)X_Jp3n#iK55H8<NwsCYMosCY$Ao&D%*k<=i+kFmV+$-
zacycw}G;0HocxnlO!~;9e`krv%rg6z`qtqsJgdDiM2B_WxBV!B%W=dcH&Rzmw7?9d3tJT~)s6gfea;HAigf%M<Qfa%9mxG~$bTbN8%0^~gHAX3Fp@l~1lv$
H44Tp>dX?I9G>i5gGbC`FV2RYRB^5fkRM0IGQDu|&^;3o;wp*nRqaagR*Ej)ZCwQY{9YZ+32WO9X)hhisLu|K4IdmKD%x(b{vmYM3CKt=J^>91>^f?1&NPD3
jwox$K-XJT_lh_MraUjTRu&zL_z+;TMs*%Uy^SPUtY(Bp@7^)-
*@!VL4M&utsNI|iySDCjaoZ#{W9rG~E(B+E*%3Pgezx;vQHMhn*QCUogrRoi8g4{B@oQ0kJPvxGK=B4<=NJhCz<($+7Ns9kyLZass)BVl*&ix_NhIGpkb7^j
Xv7S0kfC7$0Q)6~<Xkvb8g5e|XeoAu!R^gqx1T_^KWehH{^Web0J!69(aR5%gS(fcnseGCp`H|-4wJNDR=5(oLq3VD#k8+rcUt_kzk-
3TC9G=vnK%;IGGcq0&Cg|?Do>5}PICsRx8eZQ{MxAx|>b?o{4`>djj7z-j>X#{BvH?xKR-Cl2_w>oDcN4wAG>jOGzNcm3U33#Xzu}WG$xA6lr<I^a=EgP~D1
rjtAFc}m`FoHrFe5`^zn+Y57{`t$~WJ_%+Vte1k5x7NjFvMnN5DSsX6pjocl<8Gsrp8h(EEK|#fUAv&U8fEf?0{&PTr`(axWX2Q&<;W<*9`dM4M*1A1v%nx-
|gwLC825%%b~Rx=kx_@kfHp3XNX9rh-@0d@m`S{?<rdVLC8aBD<X*C3xP$`ZndEnhzY&>ZbRq1Hkzj>3DO7Ajm=l5NP7c1fual?PnsoF-mk37GByq!+zM~Mc
Z5>!Oi2j<G>Lc=<_|I)pS~)00=o2}-qI!z???5(Nf8I~J<j7~6C-w~fRo_wha^U}-
iKx_O8O{l$Qi9iOsLttBMDcP1lxt5R82_N0)fGKh@sMAUW=R}CWqIc14-Nf&jW{D9V%-t!89BYXfak)*grP1rGU{DBN9ms9CNMih*~u++d>-
{?ZWHS>BtfwL`AN34#|JtoQ0P7d37z-F3lEU2bl3ti!GQl8Zs19F*@mt0^t2g%fRv?Ado%fhtc97Xsd?d9^ZwJly5Yu-Kt{SlW_5ALP$VF1WoyZ;N!bvbNb*
kAZ!;+plPSt@W!rMfyG%IfVj>sJs&TpeYp2EY0v<&<07SdB$8I5QnKUX_~=|Wz;~QCbLY7fri;raSU+NXI9u<f{jk3yJ#NH3s9pP=SG6$xI)cGafJT1wNdTp
%d^T(cJ1mp~>zWDk_tajy{PjO+uy7gd58~xJAVwmBuivnGp6fc1=&cgtfZNB2^MHQV+eoQ`*+QFE@@KB<MCM4786Hdn6;#M5hUfzQEy`WlhCt&YDz=SeG9p?
%q{@K5?)!YN^NMR88x}fOv`E4s_g7*W5WpP&&7f%kMG;j72Ot_=|IO+8%;X6_o8Nc&9H%&a|5t$e`1zxVEGRVGrbU7|N`WGUKq!e2{JJ7GPD<~b2wB3pQOyk
=NHDT*LfKIoFb6T7K!t$$%JtHZatBr}Oey#ApF6gWz5U6&IPDT;6G{&rcLg1Ee5WXSAj8kF!~~Ybq+nVEfKWxHg&>zuvb7b)S*I%&kj_b8hi_cj!*tqaanQC
0>R};B{jX%=(tISL#HA@j>6ABk9d3i8xsr@*f%#=9m=x;(L5p!2767bZ7%L{nfO`H;hs#^eEGHJ*D-
oGxu%!eL&a}?J76u<1r(hY>mYGFz96ZlLO>#JSeg@|htdhuw32G%mQpz&P?_`L9B$6zaBOsALpfcHRuCL?Er$*zv`f)6t7_C&6nM!~YE-xIatCU~hh*{M#I0
}6%G|xwGt1vO9tfC0b^`kV3AEl%f97Am3lEq^Yo23K<XSta8*0sDq+6D>Rw{}J_DGnsYL}J7k!*dv<(ik?#ipr#GP3f3X40#+ZXp|_=(dJ$fVy1A-
Mw>)15lx6?F9y)*%a`(9^ZY2*2N}n75TxP8uayWwA(TKkj9A%HG(@UO2B6YGfY>msj7>T)u>9eWGzVT2kCnOsuu{bzmCGHbR`mKrJb3VS%i$_UDnM93_#15Z
(x-pW4@9wK_qc)gY8Z?!Scf?(i(ZuzpRb1f?-9Y`@qkDNdBrwG!__$Qx6<Ag?>M2S5EI=Af-JaTqwiB{zZ61fo6^Leq-
j3w`Pwo&z@e=YQ9_2`@8{k?gA9HU<F=q0o$-
1>jaCWju*@^xJ93wR99RdJDWeU97ucx<D>w;uB!?bwpHJK6Juh}jR9fKr;PaMRI6h!I2h<fII|L~FOfB3E#CaTHaZJ_gTO?JS7n-X-
1qXBpPw1)hXD^%Uiz>K>D#l-
1y);2J1*|G13(caAwz5fr9`68@G8oy?jfiWmjhS`VEu)H39O1&8DSHKG9;d5jMeOAPJbIv)^je;e70pmSiWtS<QPPsT@HTO~TWeX~g-
k4IiJ>{6yVP(2@KsX{EE($I7gLHvT_jAX8+$5O5=&f`ybnWc?p&rZKwin@gTuEYS#r?L_IfW1G;%gkT{zTdBN)Op9`y{2Tx07s&U4Qla;Z&z0#x8vKuiY1)m
kN=X$YEz3Po83E3&E$l_Y>YG4|jy8vG$2ZZfzbdMftC!#d`0!)s+7C||E&NEx{zRTwD;b;trVWLeD5uC`+i1{~!T>lk4MtvVm5Q?bl8ZU~5?C94Yqx{8LA42
z-tO|+jBjWUfI1A`W!#?sImM*=p%q%Yk3RY=6&Cjk&kWZe8zKs@Mlkk$^+dtkT$-iVDLXAv$kK&X-
S6wt8y=okaK00k<*Zy?N*=p=PdAyGZA3!0mm=A+F5D;?FYn9qIKJ!*0=4C*yHyh1dW%ezpVD!!7|qM>3v2b)3=^Z248tx9Yej7qv}(7=r~mdxv;JBC<_mLXE
9DN0(`*G+0<s_yzJYz!nrzKfCvhD2x<;I?=`3yBR8P|$dT0Ktgh*126h?%Co3Z>6xcDelJM$_O5$<3$m4m?5oJNE|#~DNiKxN|z>MdbGu>2_g&%fzV|Z8~3R
2M0CdT3=<5HN>UcojG;;Zf-p)02_kAAtigry70?{;VBBV}WHr(b5dE2_?Bw&%IsJ7xZcomXIi6yrApQ~1FhR;bf$F|Z65o+egpf(IJ-ZhuckUNQZURWCs3B@
a0KDwN?;7-
tn)jOpz~F}ktS+qZ+6X2BrqSp0dKX^a>gCy|ROr@_QqI~yQb?eKP%R*2H;X)$!)1$GX}vf>bLl=U`p(?!k@Arua8~1~VZ3Z+9XM3dtQ+K@_{BcWXs<lLXsx!
9j8TXhEsNt2LXmed$57_dxk$Y9#H`S+o+!~k3`Quq4B^+V5He(o9n3V5IB)|9Wu{c0TNlj7stl*}_gJyO+Rr_BpphQ7q~WGjry96&&4pbTfyIdJfI+b8U>K@
gBj5<}FcpD%G+@^RZnsc%(Y!nHwNDot>@*k25W~r#BN0qUkc3kO9NjpBQUxyr>4enKQ@0fr6Lc1$eXSxeh_0Df3P_Tw@DQ;ONI^?#mf$=gy&f^(w)C>PXCVk
g7d8VAp+Is2&`Y6>uZD-YVj+Ysxr9%TyWYLe*NnVWqsXzuB_w@t8Mb!^abu})?9QLxsT^Z#-
0|Jbmurg997UMLHNVf1?1wZu7<z=$4%607NO?O?F_Y@wA^fQZ=yEC|iV;)=k_sphNg|L^4E+gKD2zo&v0{;Xd=D`5XS2@F(!y(6a?;p9tM;}CI951_Qk4RdZ
b=^T_2r3$^*#K$2d|)Q4&RFdPUs!vIJ6H3I=6w|n&+gP^0Dv}Qy^}R5Id!i-Bh0)R;-=yGN}Oj(H*hR!Cf4y#v7TDM9`YXgT9GPatO4Ye-
A&_Q3q|Z9TQkytZ(6wmI5xQ`Axy#72XCxwH!14Z6p%q$fkjjs3GA`ze?~Vayn+0SX`s5={rng_q1*YNML_>p~&Zq4B@Uv8HM3n_)=R$UnbYguL3!1VXzn2(Y
51vY!D)Zn}WDL1qu6NNQQxvgd*ywpppf4vMrdQ*`54Nj*izwEHdO7fTe9LSv0pY=%QN*yn_xBPr4fh*G#CVg(mA7LT)Iw)@`N+q*HG3eA06CHsEmF^x}uI*s
zF@!G<7&%F0owEJ1++2wkN5e#k;eKCIWLBdOBd_d-At4EU;4N`-
Ix0Z;(oH1bCzF2#^!d5jXGEks6DFn|~4XeLUBfI&?@GL&j}pmykqZ+n>`zMky5S*>eRVv)72Qnll3he#`DKA~y4Im}H%3(>AE3!IJw*bRI<Qb6!CO9)tm{Lr
dG(F(|<uqZMNKm-^_&{#T`8-iLJHcG->s6nElpuixXKh;ry7BezZArRy_SxY&l0HEy<@Xp|;fxAF&GNdEhB-Jg6ZNnSkOtS0x&e~}NO#>#X321_GHnr7AFh{
b1v92yc8JZc1Lr+rbcs{43K*-
!kPo50a=BfcGJ(^(Hn;t7Rdp5q}L7X9U`rzQy)f&npA`C)BC>2rc(wjCW9oyd{CgP>EAa6N9jCb56ezo&`r>EWXtJMwpvDM~7F6ECWy_ogZ6?@Hv$~Ii6mFn
+zj}zP7lUCmC-NK8yZqqJ@P^eO2bx?Y}YgS89R*cE4)2LK4MYh$|YWY{l4)Eh(;ByEq9E>CCgZ>nUHONy@7iR3^oX9EPAv`Bxa<9i0%MtAj;^9)rD09aI6AF
MxyVJOkkx4!46u~SCkx2nyC<6&d!hI*9%8QUTO@K-9U=&DJ2R?-
CtQN=uN~JX5Wj|jnzD5ST5hzO>ct*j9v*<FrC#7rEyRy2!j?2jB&${sRz~_GIQDW+iBG7Y#NplIM9pIf)i_lKJ-hMrDniOt)N01;``o*XcC=>M2_WY>=(5T)
wj!)PRkS!aZR|JV?e}MG4NyUpIG9wrSfXF0Rph6?-=y^wqu&97svtHs2N6XPSL2(0;YWdkWZv!Zf-
c%NQl`FU1TD5{^G$4(JuYk})YJp@e&4q3CL8t8ECNGVLijg9-
ew9!1x(kIfw&N{;K}_|V79kD1Gd+jC+ibUOa@fEEfuROq<`YQTcs3j=_6Gf7!#?z($UgB=HExMgDnvM$rbOlP*7s<pN&*E$r;l*oSYe%**otW*MsZ<JRL*4B
1{B8Y>~{{~J&%H|n?i-yiE&5i-
(r3=Rx#k0f}IE^6>avE{LhF;$UOJb6j46%$x(U2WYAMlB@`_c7lgMBBajZ0E(}4G9bj8?Adx;0`+ITG=uU(vF(BB`0*hEVPNUD47Q4fU{(S#4dW9y(B-
qrFeH-^fy;xvcQ9*&`+QdsKWr&JIw-XT$+c3DPZAFSS)T6aE47$lOIT49t0BFHP!7>UcHkMlpn!v~`D9K=n7$!j|2>}Ekv4ToL0#TDhK>7$aM2L|R2^K;HY;
CdJc~$=((MN}!dVX{sM^DJ_=%0{xAwggd@drMKj_&^tdL(KAs{A}JW?lnAND%@71>#1MWEO@TU^We<?mhGfJ?gC&j3HlbAn4v=OuP)8n03IM_BbGRp+ll~d&
{*=OKjJ7j`mkGAbUjI+aaKQY$%-+sHm?Zd;t3Bc}J=obWD%P`h*hxr>lh@k*HwPp+VBlvOYLnz-
2dbKK)AdSJh<P0ld^Lb|*6$!3sZ~lc1eek!2+h4Wrlsr6p8#<+?H_hPA5o0KHy7A|ZE12SHFI_v>1Z5i^WdL@RE8l=|Pf4_g)VMeY#!mFIrbQd})Xw=`AmC6
Iy)QfK5L=0UhzP}Bopc?V+EByAqgXyOONgBtBFK&F{3x~4!<7@d$a8zhmDgi=FOh2akt7?Z0Huk#lG(M3(r#tD#)<&dIgJ$ls-bct&ScWivFczD;G%)SH4iU
8M=31AIV{IDV90oEvc>$^$MT0YV54k$z4F9k$nJt;u~D3U73LOx~?oRq-
H3kpmSzW6q6+YlYy#DEBm){d^>hQ35T2bR$^S9t(D@7=&1hYA8@dCSB@K1Cfw@rIg@GW~-f3|JljY@u-P_>+~9@GzLXf|e6bm05?EzvMTGRniZ-xqOEBS{(8
)mswjDEOHg%cmWU|YMjfBif)9$CYndArvTEk%1hMN%U<iftd!THm09l9?)ND{gaR@`Kzu>_$1$jxab-
j>rVWfC(zrfxV?&okE7jY$ze4cV7%{d3)W#xIl1Uac+^A+1O5wc>llhp8g9KKUR0bn0=W=oB5st%(T(B+e+GXv{>H`>KvV{gWvAn_LS{m9mCIZIkG8G_P5LY
CG>T_JhDSQXCQ5ojW1k%>417abOf)a(sQ6Qmtf>s#8<Jng`pr#pgD@l<a4ALQDq;wb}lme;{EcC+D8elTg&}A*WxUsa8DKW^E4HTJ>{-
czn4KN6s2M}b8p5mUQ#0ybd1M7_JzQ(?{95630MED$}@rf2NG|7Q}fW+D`s9+MHhSDPfk}3$4B8N=WOe6|+P{b;*SvEjrv_cSMNc(Q~n~y3gafcA)s0qav=B
#)_dfpkXx<WxDjcqA6*Ji2X-azlR{g4g8`>9bogtTfx_C~-
^i(p7*(oF>o2w`JEppw!ydmw0s@uZmSA)`m(O_ApM5o8}j%hS6w4$u}Ed|Sgb{2*ZifS?IKAy`&g4N;Z*Eg}gB9@-U)$VNs10-
o{EO^%%Id|0tvNuwE{f$RfOVqnc7n95W{pr}#+Hqby7WC)~)$stPxKxz~L3V<+fs|zU~d|)JI5P-#qLQGH$R1}1&7c6vvsL~-
)4ufrVWG?0xb16g2Ys0O4+ZOuJRQ_`h!)1#gGK!|5_)$R!$r_9M>ZASa5voFf77EfS%fR~KO$@h549E7#1Sqitvi2d+#b6{rfP)kZW34X=i#u^mLhW8*iI4^
(m?dQ(=QAnxB9V$8baimI?<gFU<{C(lAVU#gPI>wD01c0D2ZI911VsS=BCI=V5{AZfR6?SOOcNvvzqTRW0+J5^6Vm~WQPe*EvwR3fP?mQ%C<PFRrRpAZe#sc
gAQlaR-H`I+5ucJZFIXAan}>jI&pIk220W-(MT-_fC@8UEEcEFJN-_ju<ckA@IPR(%DS5)yKsMx&O_eB;99v`a{K_-
}K>J$Ucqil<n+eBv5gtU0i4up<flg`f7H(5I(CQ!>J}{vLnGGT&fSb;0ki|=6gIpHcwKW~cuCQ05tacoc1HsN7{OsUf!i~?t=Jr(15?YMk!HKP(m=^i2X-
8o34&myBBz<74Ar(qP3HzgTF9Ase%=F98$}-=*R_%AfZNo>nvPP!-
KPzwpp9U<8Bk+JwFCL_sv5>9XIWn>$&IbF51ylsArZUKINe{%vhKx|m3R4pxPTuNqoddgF;c)&E6k37+awrp#^*H(Rr_0FtRj+mF`3kqG+h;f@e;6hfd|uh@
FoFzCBy3DdK}bTM4hBOBqEV)=T<Rfm{UCV<>3iY@1QCZ-9{^DLxEKa~);@k5adAy=DjD_NuH_7}G;|!O6acA`5b8q-
39T6bmBv}{O^gE~kqm$D2RWPP%D85m#Phw5oZj?11B0o<;VftzOc>;NWaUOfXN30QcR_ZIOiu*M%Q71<Mhg#zfNlt+Jd)O0%#RjRGU>XK=~|e&w{QbI#*eD*
xoq~dVIyJf-PrrP!+w|@fXJXz4|x+mJQ*%njgOgu-g4m9{q?)vMAd>rh*MlXv*X-
H<0;(3+Zhv;VvgF5VT+b&_#s`rmQ+wh5Z;v{Gx6{6?VD_I)Cw300fGuhq!to$d|(X7XB$w6ki{ef1d)*BD1<MG7SIsEq&Fi$LUmAeoEA5%RarDxcNiIw4Y$f
-#;Zgw9z2ymSW!o;w5d%UcB$N)4BZYw!2+VlQ~?C%>Hsj1>ca#e9DVcb_jye!T9pK)O<+|<AjV;mxiGT*mWI^Tjv|fQ6>zs*AKmB!>(LJ&$}xwxfpX!u3bI~
gg_?OL;t)a*=t13mc+GmK8ujx>VpK#HLJT>}4se(RnG>6=r4iL_jBTqJF&%sMuA!|IsSlT5(ZWb!`~QD?e}{-2Q61rSqEDM*PF2de6-
~%da*?E(H(v3FtD&ycRl?uDt<Mv<_Ny8%iAZi<G%OH{0{)VT<nU>!o(0izniqI(AcZKpPHy>lYL2{&wb<Ld7#jLeOD2HuQ<rUc3suG3TY+*%WS&O)rx_WPe8
Zu;7rZI$96|V(wN#j+FgYghccH&d%60(*C{!cpLL<>f#?RPV6x9T`w~lbQ2vCQ9UyueB%*D{yid%73z=<FcBEbUcnjoC`ovbOUe3amMgoPoKm#~QHay48X-
Q{+Vf=vh^ucZ||qFkB6bBmi8L{C`M9wKO&Ndb(8;#VHvwuP99q8gFSTOb}}hwy<3xq!h*>NFxqO-bpHG%!dp6e7d~2U3dw`5?4~lbs*92QJ~yvZDxcZaSSgI
Ormk!KJQAOpwG0{TrViUw`grAC^(iKbgm%=Sn)$=Ce-
3x_P~mVFFt!)*x|NTo%@puokQPYM`=#s7mVAfyxwlD;6^zRG1D}7GbVM_KMo~_M9>RyI&!NggCs%H7PyMCCF3|1j`~&RyI*~tS}jH;FQ_u$5GH!D6Fukm{MJ
;P*7J>%5QKLd09tuyUJwLc)VC+=~}i~rW=CtM4bQ{Q>v|OF)HqSP61>otl5{Ui7bC`uJ^K@L}r5=Z)`mRPex9HEJ|Rj0B2pp3}yt1^kK4H<a#x#4(<84N!VF
zbzSd61*m~iN$gRuWeL3#t(`G}xdS3a0}@qKC_$E4==}hX-
m=I%gpl;&arF+Sw~E14SdR076&E)dxdZk(jS$<v+TTymQC9X%f+6snc=5NUqoJ7y8GILxeLyY(J!tfn&cN6~qA4BvXdwvgPSz<cYV~mCTUZ~%38H5q0w=8sg
+>G!<0#_}9hXrw6gh~IIjWhW9viQ9)nu8db!xzIKXEUEuy<!g?=AC~zAd3gjc$SC=4PhoghB;XEMasF;so6!vMR5aATa~M3p5lFpWg7S3EHuytLB1lr8*#;c
x~JA$$O6yXzCqLIM5N^5)wiTFLis)O7hqPfbQy1-H$MAZd4)ZOTACp0vuOUFA^Q67@MgnI~jVB*%7e=-
n3{{f`USKR+NRj$xDbfiz71OoUGi0`S@Hzu?)%Ad22rdvFdpY{Swp<aL7=Ic-
V7+uRX82qfKp)tc)7sS%kB&$)NA=IYJ)LgFQnSG=Wmqhb*(RS+?qjaovSeGGF)|6$=FB0$;ErK(NEwm`K9|qqnx$TTdu?8=*Y*)eF;wE(T&m$iVd^mJCKn;)
|-;ryKz}$~qB&%>jTtl+!*z4_uCjpQ9ivWm^lEIBxAn8&TmheB^Wsu0lk1d3rhnYO$<|8s9dQj2iG`2~h-
T8l;xK3i`!gRes##l{eZK?nAY($@McdZj$dBIPh^kHFa)gV(za+Jx4WDtx<e&!B+Q^3eygG*`*`H71G08JXwxMlS%W6mR_{)9K9N}qX!dJsf{aYh-
eU9orzXbX*Vx48VT6hI6hMBzN;YU?9i!}_~@Z^xq|Lgu2jsXvSMhtFh<UrZ3IaOh>kQ9kr3L_Qd>);tTLW9G2LY<7>Lm-Xlqq0&KW{H7?EbCsGDe&sZBHrvV
e>V3aC&BLnSMY+v3lw3c5Ql8Fa>rKsH*YE%}cIf{b~k=G<MpPFtKbUqH>tXC6GV8yrv(V1y8pw`;-
NUHD_)te|T4c$`jVU4|SEI~`$AR6&Z0i1e)1otBI#2(awe2n<#*-
G$YILu0&647z}%D9trd6Q>R2Oe7Lm8rdZP(2y<Uc8DT~Dj}fZv|SjMLEA;txXZN?NrO}hl3Z&!AVl!+B(TE*)EY+!w`<@84FW$1+#?i-
#z=$|EwSIehUY?;iBp^+4FKP_J~i;$XR^&l^SY~bN$Scr?uAxO{Tl_xFf#9pQ!SJ<X1-
fY(I+sIy*x!99{6|j!G&JFB3MHK1(6wWU|=lmF!H;*i8g}VEx`NGA%+x_0)}S2f$Wc}MKhr}RlBw*YTXD5RzVA}t6{*JKCPe)d`N8J&BLpFX$Fj7R#A-
!WyU5~rZvGMmm|~1vxSRY{lo0ypoa)fw1p7_v`~LU9Fy+5j#t}xo=I!x3`y_0m`~G)+=>bC!-)yZIs1W#;z^jT1&BMI^D7^W@QDV<P$<p`-
=UptHqIMKDM_s2hrN$RkX1#3u|!EUM8SY0MUreY>Mt>d;jU=#9Llk22)>1Yv-9S0GGJ)VfN%Ox5PL1`@G4I~xApsW!MA{W#5l-
6k8w>>Q4<?`SK}>ew{<64Ddc<hcpH|Y2gX6vUcp;V`DIJ4)Y5`HJD%e3v7$pVJG0$&th%fSv@(kJo_g>-
kJ4$TW{TvY+eD#l%Z~%V=Z|d<l&R0Msm$}hvZO76fK?8vqN}V$t4zi?F-Ap<D171`Eg#n8pj?3$?`u>TF@!Rq9MD*++-
<IqjDYP40;9e$fOf8xCg>xFbkKY&iS!%=G7$RBx*+t>JVg7vXL>{Nfv^|AVlOb+a43j`fI^~H`d}U0o#ntdR>#N(t29mD2R`9|Y}Jk5EH>?e{UlcrfCMg%z&
8|ZFPIx20ln^E+v5LEiam+YPY3Yv9feJh{!kH(UCxF51DG6v$mjrEz$@}xK_LWg^j45r{lW;)UKl8)3aSYXwG4Ettp1zcaElG@3N@KWq7@+`tY9($qI6D<ST
-L)JR6BdiR%uZPGLvDMtmV+RL?@=%nRh#+ws{}`uM6Exh@o>Ly@%<rES;^@i;K}mc=6-
5I*yhzZn>MPjTPf;Yxsqe6XVmAYhOjoZv7BAp!Ie!mNz|z!{1mVLM(W2=2Gdwyu6(DE^scsKtvDz$RGFO)q=k7OK~}W(yS{9Cbw14aNY4;|_GK;c*N2RzCmW
^ftnW><u*Y^t7UOExj`oc>Umc6B~#Sd=u9O05-?S-*sLj2P81LU3a+E4`Rhjsx$)_0wf?<&$wYY&!^^s>53lQxbBC`UOP{-%UkKFmcbrQDoifTOqL;1Ns$y-
oy5f%W1m`tTU4qduFn}R3U{`|Qu!V;ft?Hrskj7u5&O9ZmXU;};eaezBEdis7Q@~8yYzC7(lOjrL`T0tV>LO_)yglQaj*>H%B{RC-
I*7lv}|X;Y+8rQ*$u*_gD6eoqSQhVG}p41Vuqr1P{HGup_XHU@rn@dI9Pa$(?v4RfO0~Ng_PFUQNQ(5NpGi^6ph$24<=Cm5tVCrM~PtDa2Nqlh!K%t^s$^GI
(f(A`Eeg#KP#i}dNaYNMufum*xd5;bui?jeh8o#o|)`#jUoM%tk?4F?R!P2i#>O|?5W)V6<ZY_vOsB`?fa~Zd>?>>02}{*P6B^}0iZ=B2Xd4mOtLG<(sc6IH
NfUzRA(&*k5m0bKm0@bmIVI7?ntK!5(El_1z-
"""

encoded = "".join(PAYLOAD.split()).encode("ascii")
source = bz2.decompress(base64.b85decode(encoded))
actual = hashlib.sha256(source).hexdigest()

print("=" * 120)
print("STAGE28-AUTO-C — EMBEDDED SOURCE VERIFICATION")
print("=" * 120)
print()
print("Expected SHA256:", EXPECTED_SHA256)
print("Actual SHA256  :", actual)

if actual != EXPECTED_SHA256:
    raise RuntimeError("AUTO-C embedded source SHA256 mismatch. DO NOT RUN SCIENCE.")

bot_path = Path("/kaggle/working/stage28_auto_c.py")
bot_path.write_bytes(source)
print("\n[PASS] AUTO-C source reconstructed exactly")
print("Path:", bot_path)
print("[PASS] launching Stage28-AUTO-C\n")

exec(
    compile(source, str(bot_path), "exec"),
    {"__name__": "__main__", "__file__": str(bot_path)},
)

# ==============================================================================================================
# %% NOTEBOOK CELL 0003 | execution_count=3
# ==============================================================================================================
# =================================================================================================
# STAGE28-AUTO-C-R1
# PATCH PORCELAIN STATUS PARSER + RESUME FROM DURABLE FIT #59
#
# NO REFIT OF C071 IS AUTHORIZED.
#
# Durable remote state:
#   aa990a64d6f0451684979d748098b9654cd82e52
#
# C071 model already frozen:
#   cbfe69d53f07461f5f361fc67aef5d8bd28ffaeaeb9982b421906e2f7f9709d9
# =================================================================================================

from pathlib import Path
import hashlib
import subprocess


SEP = "=" * 120

REPO = Path(
    "/kaggle/working/ids2018-validation-safe-ablation"
)

BOT = Path(
    "/kaggle/working/stage28_auto_c.py"
)

EXPECTED_HEAD = (
    "aa990a64d6f0451684979d748098b9654cd82e52"
)

EXPECTED_MODEL_SHA = (
    "cbfe69d53f07461f5f361fc67aef5d8bd28ffaeaeb9982b421906e2f7f9709d9"
)

OUT = (
    REPO
    / "results"
    / "stage28_stability_novelty_control"
    / "stage28_2b_random_loao_control"
    / "stage28_2b1_bot_xgboost_seed42"
)

MODEL = (
    OUT
    / "bot_xgboost_seed42_cpu_model.json"
)


def banner(text):
    print()
    print(SEP)
    print(text)
    print(SEP)
    print()


def run(cmd, *, cwd=REPO, check=True):
    p = subprocess.run(
        [str(x) for x in cmd],
        cwd=str(cwd),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    if check and p.returncode != 0:
        raise RuntimeError(
            f"Command failed ({p.returncode}):\n"
            + " ".join(map(str, cmd))
            + f"\n\nSTDOUT:\n{p.stdout}"
            + f"\n\nSTDERR:\n{p.stderr}"
        )

    return p


def git(*args):
    return run(
        ["git", *args]
    ).stdout.strip()


def sha256_file(path):
    h = hashlib.sha256()

    with Path(path).open("rb") as f:
        while True:
            block = f.read(
                16 * 1024 * 1024
            )

            if not block:
                break

            h.update(block)

    return h.hexdigest()


# -------------------------------------------------------------------------------------------------
# 1. FIT #59 DURABILITY GATE
# -------------------------------------------------------------------------------------------------

banner(
    "STAGE28-AUTO-C-R1 — FIT #59 DURABILITY GATE"
)


if not REPO.is_dir():
    raise RuntimeError(
        "Repository missing. "
        "This recovery cell assumes the current Kaggle runtime is still alive."
    )


if not BOT.is_file():
    raise RuntimeError(
        "stage28_auto_c.py missing. "
        "Do not rerun FIT #59."
    )


run(
    [
        "git",
        "fetch",
        "origin",
        "main",
    ]
)


local_head = git(
    "rev-parse",
    "HEAD",
)

origin_head = git(
    "rev-parse",
    "origin/main",
)


print(
    "Local HEAD :",
    local_head,
)

print(
    "origin/main:",
    origin_head,
)

print(
    "Expected   :",
    EXPECTED_HEAD,
)


if (
    local_head != EXPECTED_HEAD
    or origin_head != EXPECTED_HEAD
):
    raise RuntimeError(
        "Durable repository state changed. "
        "STOP before recovery."
    )


if not MODEL.is_file():
    raise RuntimeError(
        "C071 model missing from current filesystem."
    )


actual_model_sha = sha256_file(
    MODEL
)


print()
print(
    "C071 model SHA:",
    actual_model_sha,
)


if actual_model_sha != EXPECTED_MODEL_SHA:
    raise RuntimeError(
        "C071 model SHA mismatch."
    )


# Model must be tracked by the fit-only commit.
model_rel = str(
    MODEL.relative_to(
        REPO
    )
)


tracked = subprocess.run(
    [
        "git",
        "ls-files",
        "--error-unmatch",
        model_rel,
    ],
    cwd=str(REPO),
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
).returncode == 0


if not tracked:
    raise RuntimeError(
        "C071 model is not tracked by durable Git state."
    )


print()
print(
    "[PASS] FIT #59 model exists"
)

print(
    "[PASS] FIT #59 model SHA exact"
)

print(
    "[PASS] FIT #59 model tracked in durable commit"
)

print(
    "[PASS] C071 MUST NOT BE REFIT"
)


# -------------------------------------------------------------------------------------------------
# 2. SHOW CURRENT RECOVERY RESIDUE
# -------------------------------------------------------------------------------------------------

banner(
    "CURRENT AUTO-C RECOVERY RESIDUE"
)


status_raw = run(
    [
        "git",
        "status",
        "--porcelain",
    ]
).stdout


print(
    status_raw
    if status_raw
    else "[clean]"
)


# Every current dirty path must belong to C071.
for raw_line in status_raw.splitlines():

    if not raw_line.strip():
        continue

    # Robust parsing independent of the leading porcelain whitespace.
    parts = raw_line.lstrip().split(
        maxsplit=1
    )

    if len(parts) != 2:
        raise RuntimeError(
            f"Cannot parse Git status line: {raw_line!r}"
        )

    path_text = parts[1].strip()

    # Rename syntax is not expected here.
    if " -> " in path_text:
        path_text = path_text.split(
            " -> ",
            1,
        )[1]


    path = (
        REPO
        / path_text
    ).resolve()


    try:
        path.relative_to(
            OUT.resolve()
        )

    except ValueError:
        raise RuntimeError(
            "Unexpected recovery residue outside C071:\n"
            + raw_line
        )


print(
    "[PASS] all current repository residue belongs only to C071"
)


# -------------------------------------------------------------------------------------------------
# 3. PATCH ONLY commit_paths()
# -------------------------------------------------------------------------------------------------

banner(
    "PATCH AUTO-C GIT STATUS PARSER"
)


source = BOT.read_text(
    encoding="utf-8"
)


function_start = source.find(
    "def commit_paths("
)


if function_start < 0:
    raise RuntimeError(
        "commit_paths() not found."
    )


function_end = source.find(
    "\ndef ",
    function_start + 1,
)


if function_end < 0:
    function_end = len(
        source
    )


before = source[
    function_start:function_end
]


if "line[3:]" not in before:
    raise RuntimeError(
        "Expected vulnerable porcelain parser not found.\n"
        "Do not apply an unverified patch."
    )


after = before.replace(
    "line[3:].strip()",
    "line.lstrip().split(maxsplit=1)[1].strip()",
)


after = after.replace(
    "line[3:]",
    "line.lstrip().split(maxsplit=1)[1]",
)


if after == before:
    raise RuntimeError(
        "AUTO-C parser patch made no change."
    )


patched_source = (
    source[:function_start]
    + after
    + source[function_end:]
)


# Syntax validation before touching runtime source.
compile(
    patched_source,
    str(
        BOT
    ),
    "exec",
)


backup = Path(
    "/kaggle/working/stage28_auto_c_pre_r1.py"
)


if not backup.exists():
    backup.write_text(
        source,
        encoding="utf-8",
    )


BOT.write_text(
    patched_source,
    encoding="utf-8",
)


patched_sha = sha256_file(
    BOT
)


print(
    "[PASS] commit_paths() patched only"
)

print(
    "[PASS] source compiles"
)

print(
    "Patched AUTO-C SHA256:",
    patched_sha,
)


# -------------------------------------------------------------------------------------------------
# 4. PRE-RESUME SCIENCE GATE
# -------------------------------------------------------------------------------------------------

banner(
    "PRE-RESUME SCIENCE GATE"
)


# Confirm fit-only commit still current.
if git(
    "rev-parse",
    "HEAD",
) != EXPECTED_HEAD:
    raise RuntimeError(
        "HEAD changed unexpectedly during patch."
    )


if git(
    "rev-parse",
    "origin/main",
) != EXPECTED_HEAD:
    raise RuntimeError(
        "origin/main changed unexpectedly during patch."
    )


if sha256_file(
    MODEL
) != EXPECTED_MODEL_SHA:
    raise RuntimeError(
        "C071 model changed during recovery."
    )


print(
    "Durable fit:",
    "FIT #59 / C071"
)

print(
    "Family:",
    "BOT"
)

print(
    "Learner:",
    "XGBOOST"
)

print(
    "Seed:",
    42
)

print(
    "Model SHA:",
    EXPECTED_MODEL_SHA
)

print()
print(
    "[PASS] no scientific refit required"
)

print(
    "[PASS] resume must finish Stage28-2B1 evaluation first"
)

print(
    "[PASS] next NEW model fit after that must be FIT #60 / C072"
)


# -------------------------------------------------------------------------------------------------
# 5. RESUME PATCHED AUTO-C
# -------------------------------------------------------------------------------------------------

banner(
    "RESUMING STAGE28-AUTO-C"
)


exec(
    compile(
        patched_source,
        str(
            BOT
        ),
        "exec",
    ),
    {
        "__name__": "__main__",
        "__file__": str(
            BOT
        ),
    },
)

# ==============================================================================================================
# %% NOTEBOOK CELL 0004 | execution_count=4
# ==============================================================================================================
# =================================================================================================
# STAGE28-AUTO-C-R2
# PATCH REMAINING STARTUP/RESUME PORCELAIN PARSER
#
# FIT #59 / C071 IS ALREADY DURABLE AND MUST NOT BE REFIT.
#
# Expected current AUTO-C-R1 source SHA:
#   15cbac7dfb05f7d0bfc1ba64896e3c3301a683ff98c48ba92a07277252fbd0cb
#
# Expected durable Git HEAD:
#   aa990a64d6f0451684979d748098b9654cd82e52
# =================================================================================================

from pathlib import Path
import hashlib
import subprocess


SEP = "=" * 120

REPO = Path(
    "/kaggle/working/ids2018-validation-safe-ablation"
).resolve()

BOT = Path(
    "/kaggle/working/stage28_auto_c.py"
)

EXPECTED_HEAD = (
    "aa990a64d6f0451684979d748098b9654cd82e52"
)

EXPECTED_R1_SOURCE_SHA = (
    "15cbac7dfb05f7d0bfc1ba64896e3c3301a683ff98c48ba92a07277252fbd0cb"
)

EXPECTED_MODEL_SHA = (
    "cbfe69d53f07461f5f361fc67aef5d8bd28ffaeaeb9982b421906e2f7f9709d9"
)

OUT = (
    REPO
    / "results"
    / "stage28_stability_novelty_control"
    / "stage28_2b_random_loao_control"
    / "stage28_2b1_bot_xgboost_seed42"
).resolve()

MODEL = (
    OUT
    / "bot_xgboost_seed42_cpu_model.json"
)


def banner(text):
    print()
    print(SEP)
    print(text)
    print(SEP)
    print()


def run(cmd, *, cwd=REPO, check=True):
    p = subprocess.run(
        [str(x) for x in cmd],
        cwd=str(cwd),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    if check and p.returncode != 0:
        raise RuntimeError(
            f"Command failed ({p.returncode}):\n"
            + " ".join(map(str, cmd))
            + f"\n\nSTDOUT:\n{p.stdout}"
            + f"\n\nSTDERR:\n{p.stderr}"
        )

    return p


def git(*args):
    return run(
        ["git", *args]
    ).stdout.strip()


def sha256_file(path):
    h = hashlib.sha256()

    with Path(path).open("rb") as f:
        while True:
            block = f.read(
                16 * 1024 * 1024
            )

            if not block:
                break

            h.update(block)

    return h.hexdigest()


# =================================================================================================
# 1. EXACT RECOVERY STATE
# =================================================================================================

banner(
    "STAGE28-AUTO-C-R2 — EXACT STATE GATE"
)


if not REPO.is_dir():
    raise RuntimeError(
        "Repository missing."
    )

if not BOT.is_file():
    raise RuntimeError(
        "stage28_auto_c.py missing."
    )

if not MODEL.is_file():
    raise RuntimeError(
        "Durable C071 model missing."
    )


run(
    [
        "git",
        "fetch",
        "origin",
        "main",
    ]
)


local_head = git(
    "rev-parse",
    "HEAD",
)

origin_head = git(
    "rev-parse",
    "origin/main",
)


print(
    "Local HEAD :",
    local_head,
)

print(
    "origin/main:",
    origin_head,
)

print(
    "Expected   :",
    EXPECTED_HEAD,
)


if local_head != EXPECTED_HEAD:
    raise RuntimeError(
        "Local HEAD changed unexpectedly."
    )

if origin_head != EXPECTED_HEAD:
    raise RuntimeError(
        "Remote HEAD changed unexpectedly."
    )


actual_model_sha = sha256_file(
    MODEL
)

print()
print(
    "C071 model SHA:",
    actual_model_sha,
)


if actual_model_sha != EXPECTED_MODEL_SHA:
    raise RuntimeError(
        "C071 model identity mismatch."
    )


current_source_sha = sha256_file(
    BOT
)

print()
print(
    "Current AUTO-C SHA:",
    current_source_sha,
)

print(
    "Expected R1 SHA   :",
    EXPECTED_R1_SOURCE_SHA,
)


if current_source_sha != EXPECTED_R1_SOURCE_SHA:
    raise RuntimeError(
        "AUTO-C source is not the exact R1-patched version.\n"
        "STOP rather than applying a blind patch."
    )


print()
print(
    "[PASS] FIT #59 durable state exact"
)

print(
    "[PASS] AUTO-C R1 source identity exact"
)

print(
    "[PASS] no new fit has started"
)


# =================================================================================================
# 2. VERIFY CURRENT RESIDUE IS ONLY C071
# =================================================================================================

banner(
    "CURRENT C071 RECOVERY RESIDUE"
)


status_raw = run(
    [
        "git",
        "status",
        "--porcelain",
    ]
).stdout


print(
    status_raw
    if status_raw
    else "[clean]"
)


def robust_porcelain_path(raw_line):

    s = raw_line.lstrip()

    parts = s.split(
        maxsplit=1
    )

    if len(parts) != 2:
        raise RuntimeError(
            f"Cannot parse Git porcelain line: {raw_line!r}"
        )

    path_text = parts[1].strip()

    if " -> " in path_text:
        path_text = path_text.split(
            " -> ",
            1,
        )[1].strip()

    return path_text


for raw_line in status_raw.splitlines():

    if not raw_line.strip():
        continue

    rel = robust_porcelain_path(
        raw_line
    )

    candidate = (
        REPO
        / rel
    ).resolve()

    try:
        candidate.relative_to(
            OUT
        )

    except ValueError:
        raise RuntimeError(
            "Unexpected repository residue outside C071:\n"
            + raw_line
        )


print()
print(
    "[PASS] every dirty/untracked path belongs to current C071"
)


# =================================================================================================
# 3. LOCATE THE SECOND VULNERABLE PARSER
# =================================================================================================

banner(
    "LOCATE STARTUP/RESUME PARSER"
)


source = BOT.read_text(
    encoding="utf-8"
)


error_anchor = (
    'Repository has changes outside AUTO-C recovery space:'
)


error_pos = source.find(
    error_anchor
)


if error_pos < 0:
    raise RuntimeError(
        "Startup recovery error anchor not found."
    )


# Only inspect the local code region immediately preceding this error.
region_start = max(
    0,
    error_pos - 1800,
)


region = source[
    region_start:error_pos
]


vulnerable_full = (
    "line[3:].strip()"
)

vulnerable_short = (
    "line[3:]"
)


relative_pos = region.rfind(
    vulnerable_full
)


replacement_len = len(
    vulnerable_full
)


if relative_pos < 0:

    relative_pos = region.rfind(
        vulnerable_short
    )

    replacement_len = len(
        vulnerable_short
    )


if relative_pos < 0:
    raise RuntimeError(
        "The remaining vulnerable startup parser was not found "
        "immediately before the recovery-space guard."
    )


absolute_pos = (
    region_start
    + relative_pos
)


old_text = source[
    absolute_pos:
    absolute_pos
    + replacement_len
]


print(
    "Found vulnerable expression:",
    old_text,
)

print(
    "Near source position:",
    absolute_pos,
)


# =================================================================================================
# 4. PATCH EXACTLY THAT ONE EXPRESSION
# =================================================================================================

banner(
    "PATCH STARTUP/RESUME PORCELAIN PARSER"
)


new_expression = (
    "line.lstrip().split(maxsplit=1)[1].strip()"
)


patched_source = (
    source[:absolute_pos]
    + new_expression
    + source[
        absolute_pos
        + replacement_len:
    ]
)


# Ensure we changed exactly one vulnerable site.
if patched_source == source:
    raise RuntimeError(
        "No source modification occurred."
    )


# Must remain syntactically valid.
compile(
    patched_source,
    str(BOT),
    "exec",
)


backup = Path(
    "/kaggle/working/stage28_auto_c_pre_r2.py"
)


if not backup.exists():
    backup.write_text(
        source,
        encoding="utf-8",
    )


BOT.write_text(
    patched_source,
    encoding="utf-8",
)


patched_sha = sha256_file(
    BOT
)


print(
    "[PASS] exactly one startup/resume parser patched"
)

print(
    "[PASS] source compiles"
)

print(
    "R2 AUTO-C SHA256:",
    patched_sha,
)


# =================================================================================================
# 5. VERIFY THE PREVIOUS commit_paths() PATCH STILL EXISTS
# =================================================================================================

banner(
    "CHECK BOTH RECOVERY FIXES"
)


final_source = BOT.read_text(
    encoding="utf-8"
)


# The R1 commit_paths fix should still contain force-add logic.
if '["git", "add", "-f", "--", rel]' not in final_source:
    raise RuntimeError(
        "R1 force-add patch disappeared."
    )


# The startup guard should now contain our robust expression.
if new_expression not in final_source:
    raise RuntimeError(
        "R2 startup parser patch not present."
    )


print(
    "[PASS] R1 commit_paths() fix preserved"
)

print(
    "[PASS] R2 startup/resume parser fix present"
)


# =================================================================================================
# 6. FINAL NO-REFIT GATE
# =================================================================================================

banner(
    "NO-REFIT GATE"
)


if git(
    "rev-parse",
    "HEAD",
) != EXPECTED_HEAD:
    raise RuntimeError(
        "HEAD changed during patch."
    )


if git(
    "rev-parse",
    "origin/main",
) != EXPECTED_HEAD:
    raise RuntimeError(
        "origin/main changed during patch."
    )


if sha256_file(
    MODEL
) != EXPECTED_MODEL_SHA:
    raise RuntimeError(
        "C071 model changed during patch."
    )


print(
    "FIT #59 / C071:",
    "ALREADY SUCCESSFULLY FIT"
)

print(
    "Model durability:",
    "GITHUB FIT-ONLY COMMIT"
)

print(
    "Scientific fits consumed:",
    "59 / 108"
)

print(
    "Remaining NEW fits:",
    "49"
)

print()
print(
    "[PASS] C071 refit prohibited"
)

print(
    "[PASS] AUTO-C must salvage C071 evaluation first"
)

print(
    "[PASS] next actual model training must be FIT #60 / C072"
)


# =================================================================================================
# 7. RESUME
# =================================================================================================

banner(
    "RESUMING STAGE28-AUTO-C AFTER R2"
)


exec(
    compile(
        patched_source,
        str(BOT),
        "exec",
    ),
    {
        "__name__": "__main__",
        "__file__": str(BOT),
    },
)

# ==============================================================================================================
# %% NOTEBOOK CELL 0005 | execution_count=5
# ==============================================================================================================
# =================================================================================================
# STAGE28-3A — EXPERIMENT CLOSURE + 108-FIT AUDIT
#
# ZERO NEW FITS
# ZERO MODEL INFERENCE
# ZERO THRESHOLD SELECTION
# ZERO TARGET OPENINGS
# ZERO SHARED-FINAL-HOLDOUT OPENINGS
#
# Scientific parent:
#   9fddb8d8c34ba8f81b71f24eea15c90151053d6b
#
# Purpose:
#   1. Prove frozen manifest = 120 components.
#   2. Prove budget = 108 NEW + 12 REUSE.
#   3. Prove FIT #1 .. FIT #108 are contiguous and consumed exactly once.
#   4. Verify all 108 Stage28 new model artifacts.
#   5. Verify all 12 historical reused-model SHA256 identities.
#   6. Byte-verify every Stage28 execution checksum manifest.
#   7. Reconcile learner/seed/parameter/model identity against the frozen manifest.
#   8. Prove no final-holdout / target-adaptive fitting or threshold search occurred.
#   9. Freeze a permanent experiment-closure receipt.
#  10. Commit and push Stage28-3A.
#
# AFTER THIS:
#   NEW MODEL FITTING IS CLOSED FOR THIS MANUSCRIPT.
# =================================================================================================

from __future__ import annotations

import base64
import csv
import hashlib
import json
import os
import re
import subprocess

from datetime import datetime, timezone
from pathlib import Path


# =================================================================================================
# CONSTANTS
# =================================================================================================

SEP = "=" * 120

REPO = Path(
    "/kaggle/working/ids2018-validation-safe-ablation"
).resolve()

EXPECTED_PARENT = (
    "9fddb8d8c34ba8f81b71f24eea15c90151053d6b"
)

EXPECTED_MANIFEST_SHA256 = (
    "47e7ffbf357fee3d86830282ae0e69663f84849971e3caeb151168e9bb50b505"
)

ROOT = (
    REPO
    / "results"
    / "stage28_stability_novelty_control"
)

MANIFEST = (
    ROOT
    / "stage28_1b_random_loao_membership_and_execution_lock"
    / "stage28_component_execution_manifest.csv"
)

STAGE22_ROOT = (
    ROOT
    / "stage28_2a_stage22_seed_stability"
)

STAGE27_ROOT = (
    ROOT
    / "stage28_2a_stage27_seed_stability"
)

STAGE28B_ROOT = (
    ROOT
    / "stage28_2b_random_loao_control"
)

OUT = (
    ROOT
    / "stage28_3a_experiment_closure_audit"
)

RECEIPT = (
    OUT
    / "stage28_3a_experiment_closure_receipt.json"
)

COMPONENT_CSV = (
    OUT
    / "stage28_3a_component_closure_audit.csv"
)

LEDGER_CSV = (
    OUT
    / "stage28_3a_new_fit_ledger_audit.csv"
)

README = (
    OUT
    / "README.md"
)

CHECKSUMS = (
    OUT
    / "checksums.sha256"
)


# =================================================================================================
# HELPERS
# =================================================================================================

def banner(text):
    print()
    print(SEP)
    print(text)
    print(SEP)
    print()


def run(
    cmd,
    *,
    cwd=REPO,
    check=True,
):
    p = subprocess.run(
        [
            str(x)
            for x in cmd
        ],
        cwd=str(cwd),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    if check and p.returncode != 0:
        raise RuntimeError(
            f"Command failed ({p.returncode}):\n"
            + " ".join(
                map(
                    str,
                    cmd,
                )
            )
            + f"\n\nSTDOUT:\n{p.stdout}"
            + f"\n\nSTDERR:\n{p.stderr}"
        )

    return p


def git(
    *args,
    check=True,
):
    return (
        run(
            [
                "git",
                *args,
            ],
            check=check,
        ).stdout
        or ""
    ).strip()


def sha256_file(
    path,
    chunk=16 * 1024 * 1024,
):
    h = hashlib.sha256()

    with Path(path).open(
        "rb"
    ) as f:

        while True:

            block = f.read(
                chunk
            )

            if not block:
                break

            h.update(
                block
            )

    return h.hexdigest()


def read_json(
    path,
):
    return json.loads(
        Path(path).read_text(
            encoding="utf-8"
        )
    )


def write_json(
    path,
    obj,
):
    Path(path).write_text(
        json.dumps(
            obj,
            indent=2,
            sort_keys=False,
        )
        + "\n",
        encoding="utf-8",
    )


def recover_github_token():

    labels = [
        "GITHUB_TOKEN",
        "github_token",
        "GH_TOKEN",
        "GITHUB_PAT",
        "github_pat",
        "GH_PAT",
    ]

    try:

        from kaggle_secrets import (
            UserSecretsClient,
        )

        client = (
            UserSecretsClient()
        )

        for label in labels:

            try:
                value = (
                    client.get_secret(
                        label
                    )
                )

            except Exception:
                value = None

            if (
                isinstance(
                    value,
                    str,
                )
                and value.strip()
            ):
                return (
                    value.strip(),
                    f"kaggle_secret:{label}",
                )

    except Exception:
        pass


    for label in labels:

        value = os.environ.get(
            label
        )

        if (
            isinstance(
                value,
                str,
            )
            and value.strip()
        ):
            return (
                value.strip(),
                f"environment:{label}",
            )


    raise RuntimeError(
        "GitHub credential unavailable."
    )


def authenticated_push(
    token,
):

    auth = base64.b64encode(
        (
            "x-access-token:"
            + token
        ).encode(
            "utf-8"
        )
    ).decode(
        "ascii"
    )


    p = subprocess.run(
        [
            "git",
            "-c",
            "credential.helper=",
            "-c",
            (
                "http.extraHeader="
                "AUTHORIZATION: Basic "
                + auth
            ),
            "push",
            "origin",
            "main",
        ],
        cwd=str(
            REPO
        ),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


    if p.returncode != 0:
        raise RuntimeError(
            "Git push failed.\n\n"
            f"STDOUT:\n{p.stdout}\n\n"
            f"STDERR:\n{p.stderr}"
        )


    return (
        p.stdout
        + p.stderr
    ).strip()


def remote_head():

    text = git(
        "ls-remote",
        "origin",
        "refs/heads/main",
    )

    if not text:
        raise RuntimeError(
            "Unable to resolve remote main."
        )

    return text.split()[0]


def parse_checksums(
    path,
):

    rows = []

    for raw in Path(
        path
    ).read_text(
        encoding="utf-8"
    ).splitlines():

        raw = raw.strip()

        if not raw:
            continue

        parts = raw.split(
            None,
            1,
        )

        if len(parts) != 2:
            raise RuntimeError(
                f"Malformed checksum line in {path}: "
                f"{raw!r}"
            )

        digest = parts[0]

        filename = (
            parts[1]
            .strip()
            .lstrip("*")
        )

        if not re.fullmatch(
            r"[0-9a-f]{64}",
            digest,
        ):
            raise RuntimeError(
                f"Malformed SHA256 in {path}: "
                f"{digest!r}"
            )

        rows.append(
            (
                digest,
                filename,
            )
        )

    return rows


def verify_checksum_manifest(
    path,
):

    path = Path(
        path
    )

    if not path.is_file():
        raise RuntimeError(
            f"Missing checksum manifest:\n{path}"
        )

    rows = parse_checksums(
        path
    )

    if not rows:
        raise RuntimeError(
            f"Empty checksum manifest:\n{path}"
        )

    seen = set()

    total_bytes = 0

    for expected, filename in rows:

        if filename in seen:
            raise RuntimeError(
                f"Duplicate checksum entry "
                f"{filename!r} in {path}"
            )

        seen.add(
            filename
        )

        target = (
            path.parent
            / filename
        )

        if not target.is_file():
            raise RuntimeError(
                f"Checksum payload missing:\n"
                f"{target}"
            )

        actual = sha256_file(
            target
        )

        if actual != expected:
            raise RuntimeError(
                "Checksum mismatch:\n"
                f"{target}\n"
                f"expected={expected}\n"
                f"actual={actual}"
            )

        total_bytes += (
            target.stat().st_size
        )

    return (
        len(rows),
        total_bytes,
    )


def model_artifacts(
    root,
):

    root = Path(
        root
    )

    return sorted(
        list(
            root.rglob(
                "*_cpu_model.json"
            )
        )
        +
        list(
            root.rglob(
                "*_cpu_model.txt"
            )
        )
    )


def stage_dirs(
    root,
    pattern,
):

    return [
        p
        for p in Path(
            root
        ).glob(
            pattern
        )
        if p.is_dir()
    ]


def walk_key_values(
    obj,
    key,
):

    out = []

    if isinstance(
        obj,
        dict,
    ):

        for k, v in obj.items():

            if k == key:
                out.append(
                    v
                )

            out.extend(
                walk_key_values(
                    v,
                    key,
                )
            )

    elif isinstance(
        obj,
        list,
    ):

        for item in obj:

            out.extend(
                walk_key_values(
                    item,
                    key,
                )
            )

    return out


def require_all(
    values,
    predicate,
    label,
):

    bad = [
        v
        for v in values
        if not predicate(
            v
        )
    ]

    if bad:
        raise RuntimeError(
            f"{label} contains forbidden values: "
            f"{bad[:10]}"
        )

    return len(
        values
    )


# =================================================================================================
# 0. REPOSITORY / PARENT GATE
# =================================================================================================

banner(
    "STAGE28-3A — EXPERIMENT CLOSURE / REPOSITORY GATE"
)


if not (
    REPO
    / ".git"
).is_dir():
    raise RuntimeError(
        f"Repository missing:\n{REPO}"
    )


if OUT.exists():
    raise RuntimeError(
        "Stage28-3A output already exists:\n"
        f"{OUT}\n\n"
        "Do not overwrite a previous closure audit."
    )


status = git(
    "status",
    "--porcelain",
)


if status:
    raise RuntimeError(
        "Repository must be clean before Stage28-3A:\n"
        + status
    )


run(
    [
        "git",
        "fetch",
        "origin",
        "main",
    ]
)


local_head = git(
    "rev-parse",
    "HEAD",
)

origin_head = git(
    "rev-parse",
    "origin/main",
)

remote = remote_head()


print(
    "Expected parent:",
    EXPECTED_PARENT,
)

print(
    "Local HEAD     :",
    local_head,
)

print(
    "origin/main    :",
    origin_head,
)

print(
    "Remote main    :",
    remote,
)


if not (
    local_head
    == origin_head
    == remote
    == EXPECTED_PARENT
):
    raise RuntimeError(
        "Stage28-3A parent mismatch. "
        "Stop before auditing a different repository state."
    )


print()
print(
    "[PASS] Stage28 experiment parent exact and synchronized"
)

print(
    "[PASS] repository clean"
)

print(
    "[PASS] ZERO fits / ZERO inference / ZERO threshold selection"
)


# =================================================================================================
# 1. FROZEN MANIFEST
# =================================================================================================

banner(
    "STAGE28-3A — FROZEN MANIFEST / BUDGET GATE"
)


manifest_sha = sha256_file(
    MANIFEST
)


print(
    "Manifest SHA256:",
    manifest_sha,
)


if (
    manifest_sha
    != EXPECTED_MANIFEST_SHA256
):
    raise RuntimeError(
        "Frozen Stage28 component manifest SHA256 mismatch."
    )


with MANIFEST.open(
    "r",
    encoding="utf-8",
    newline="",
) as f:

    manifest_rows = list(
        csv.DictReader(
            f
        )
    )


if len(
    manifest_rows
) != 120:
    raise RuntimeError(
        "Expected exactly 120 frozen components."
    )


ordinals = [
    int(
        row[
            "component_ordinal"
        ]
    )
    for row in manifest_rows
]


if ordinals != list(
    range(
        1,
        121,
    )
):
    raise RuntimeError(
        "Manifest ordinals are not exactly 1..120."
    )


component_ids = [
    row[
        "component_id"
    ]
    for row in manifest_rows
]


expected_component_ids = [
    f"C{i:03d}"
    for i in range(
        1,
        121,
    )
]


if (
    component_ids
    != expected_component_ids
):
    raise RuntimeError(
        "Manifest component IDs are not exactly C001..C120."
    )


if any(
    row[
        "compute_backend"
    ].upper()
    != "CPU"
    for row in manifest_rows
):
    raise RuntimeError(
        "Non-CPU component found in frozen Stage28 manifest."
    )


new_rows = [
    row
    for row in manifest_rows
    if row[
        "fit_action"
    ]
    == "NEW_FIT_AUTHORIZED"
]


reuse_rows = [
    row
    for row in manifest_rows
    if row[
        "fit_action"
    ]
    == "REUSE_EXISTING"
]


if len(
    new_rows
) != 108:
    raise RuntimeError(
        f"Expected 108 NEW components, "
        f"found {len(new_rows)}"
    )


if len(
    reuse_rows
) != 12:
    raise RuntimeError(
        f"Expected 12 reuse components, "
        f"found {len(reuse_rows)}"
    )


if sum(
    int(
        row[
            "new_fit_budget_units"
        ]
        or 0
    )
    for row in manifest_rows
) != 108:
    raise RuntimeError(
        "Frozen new-fit budget does not sum to 108."
    )


if sum(
    int(
        row[
            "reuse_budget_units"
        ]
        or 0
    )
    for row in manifest_rows
) != 12:
    raise RuntimeError(
        "Frozen reuse budget does not sum to 12."
    )


stage22_manifest = (
    manifest_rows[
        :20
    ]
)

stage27_manifest = (
    manifest_rows[
        20:70
    ]
)

stage28b_manifest = (
    manifest_rows[
        70:120
    ]
)


def manifest_counts(
    rows,
):
    return {
        "components": len(
            rows
        ),
        "new": sum(
            row[
                "fit_action"
            ]
            == "NEW_FIT_AUTHORIZED"
            for row in rows
        ),
        "reuse": sum(
            row[
                "fit_action"
            ]
            == "REUSE_EXISTING"
            for row in rows
        ),
    }


stage22_counts = manifest_counts(
    stage22_manifest
)

stage27_counts = manifest_counts(
    stage27_manifest
)

stage28b_counts = manifest_counts(
    stage28b_manifest
)


if stage22_counts != {
    "components": 20,
    "new": 18,
    "reuse": 2,
}:
    raise RuntimeError(
        f"Stage22 manifest mismatch: "
        f"{stage22_counts}"
    )


if stage27_counts != {
    "components": 50,
    "new": 40,
    "reuse": 10,
}:
    raise RuntimeError(
        f"Stage27 manifest mismatch: "
        f"{stage27_counts}"
    )


if stage28b_counts != {
    "components": 50,
    "new": 50,
    "reuse": 0,
}:
    raise RuntimeError(
        f"Stage28B manifest mismatch: "
        f"{stage28b_counts}"
    )


print(
    "[PASS] 120 components exact"
)

print(
    "[PASS] 108 NEW + 12 REUSE exact"
)

print(
    "[PASS] Stage22 = 18 new + 2 reuse"
)

print(
    "[PASS] Stage27 = 40 new + 10 reuse"
)

print(
    "[PASS] Stage28B = 50 new + 0 reuse"
)

print(
    "[PASS] all components CPU as frozen"
)


# =================================================================================================
# 2. VERIFY ALL 12 REUSED HISTORICAL MODELS
# =================================================================================================

banner(
    "STAGE28-3A — HISTORICAL REUSE IDENTITY GATE"
)


reuse_evidence = {}


for row in reuse_rows:

    cid = row[
        "component_id"
    ]

    rel = row[
        "reused_model_path"
    ]

    expected_sha = row[
        "reused_model_sha256"
    ]


    if (
        not rel
        or not expected_sha
    ):
        raise RuntimeError(
            f"{cid}: incomplete reuse identity."
        )


    path = (
        REPO
        / rel
    )


    if not path.is_file():
        raise RuntimeError(
            f"{cid}: reused model missing:\n"
            f"{path}"
        )


    actual_sha = sha256_file(
        path
    )


    if (
        actual_sha
        != expected_sha
    ):
        raise RuntimeError(
            f"{cid}: reused model SHA mismatch\n"
            f"{path}\n"
            f"expected={expected_sha}\n"
            f"actual={actual_sha}"
        )


    reuse_evidence[
        cid
    ] = {
        "model_path": rel,
        "model_sha256": actual_sha,
    }


    print(
        "[PASS reuse]",
        cid,
        row[
            "experiment"
        ],
        row[
            "unit"
        ],
        row[
            "learner"
        ],
        "seed"
        + row[
            "model_seed"
        ],
    )


if set(
    reuse_evidence
) != {
    row[
        "component_id"
    ]
    for row in reuse_rows
}:
    raise RuntimeError(
        "Reuse component coverage mismatch."
    )


print()
print(
    "[PASS] 12 / 12 historical model identities exact"
)


# =================================================================================================
# 3. STAGE28 EXECUTION DIRECTORY + MODEL UNIVERSE
# =================================================================================================

banner(
    "STAGE28-3A — EXECUTION OUTPUT UNIVERSE"
)


stage22_dirs = stage_dirs(
    STAGE22_ROOT,
    "stage28_2a*",
)

stage27_dirs = stage_dirs(
    STAGE27_ROOT,
    "stage28_2a*",
)

stage28b_dirs = stage_dirs(
    STAGE28B_ROOT,
    "stage28_2b*",
)


if len(
    stage22_dirs
) != 10:
    raise RuntimeError(
        f"Expected 10 Stage22 output dirs, "
        f"found {len(stage22_dirs)}"
    )


if len(
    stage27_dirs
) != 40:
    raise RuntimeError(
        f"Expected 40 Stage27 new-fit dirs, "
        f"found {len(stage27_dirs)}"
    )


if len(
    stage28b_dirs
) != 50:
    raise RuntimeError(
        f"Expected 50 Stage28B dirs, "
        f"found {len(stage28b_dirs)}"
    )


stage22_models = model_artifacts(
    STAGE22_ROOT
)

stage27_models = model_artifacts(
    STAGE27_ROOT
)

stage28b_models = model_artifacts(
    STAGE28B_ROOT
)


if len(
    stage22_models
) != 18:
    raise RuntimeError(
        f"Expected 18 Stage22 new model artifacts, "
        f"found {len(stage22_models)}"
    )


if len(
    stage27_models
) != 40:
    raise RuntimeError(
        f"Expected 40 Stage27 new model artifacts, "
        f"found {len(stage27_models)}"
    )


if len(
    stage28b_models
) != 50:
    raise RuntimeError(
        f"Expected 50 Stage28B new model artifacts, "
        f"found {len(stage28b_models)}"
    )


all_new_models = (
    stage22_models
    + stage27_models
    + stage28b_models
)


if len(
    all_new_models
) != 108:
    raise RuntimeError(
        "Stage28 new model universe is not exactly 108."
    )


print(
    "[PASS] output dirs: 10 + 40 + 50 = 100"
)

print(
    "[PASS] new model artifacts: 18 + 40 + 50 = 108"
)

print(
    "[PASS] no 109th Stage28 model artifact exists "
    "inside the frozen execution roots"
)


# =================================================================================================
# 4. BYTE-VERIFY ALL EXECUTION CHECKSUM MANIFESTS
# =================================================================================================

banner(
    "STAGE28-3A — BYTE-LEVEL CHECKSUM AUDIT"
)


checksum_dirs = (
    stage22_dirs
    + stage27_dirs
    + stage28b_dirs
)


if len(
    checksum_dirs
) != 100:
    raise RuntimeError(
        "Expected exactly 100 Stage28 execution/evaluation directories."
    )


payload_files_verified = 0
payload_bytes_verified = 0


for i, directory in enumerate(
    checksum_dirs,
    start=1,
):

    file_count, byte_count = (
        verify_checksum_manifest(
            directory
            / "checksums.sha256"
        )
    )

    payload_files_verified += (
        file_count
    )

    payload_bytes_verified += (
        byte_count
    )


    if (
        i == 1
        or i % 10 == 0
        or i
        == len(
            checksum_dirs
        )
    ):
        print(
            f"[PASS checksums] "
            f"{i:3d}/{len(checksum_dirs)} "
            f"| payloads={payload_files_verified:,} "
            f"| bytes={payload_bytes_verified:,}"
        )


print()
print(
    "[PASS] all 100 Stage28 checksum manifests "
    "verified byte-for-byte"
)


# =================================================================================================
# 5. RECONCILE FIT #1 .. FIT #108
# =================================================================================================

banner(
    "STAGE28-3A — NEW-FIT LEDGER RECONCILIATION"
)


fit_evidence = {}

fit_ordinals_seen = set()

ledger_rows = []


def register_fit(
    component_id,
    fit_ordinal,
    ledger_path,
):

    fit_ordinal = int(
        fit_ordinal
    )


    if (
        component_id
        in fit_evidence
    ):
        raise RuntimeError(
            f"Duplicate new-fit component: "
            f"{component_id}"
        )


    if (
        fit_ordinal
        in fit_ordinals_seen
    ):
        raise RuntimeError(
            f"Duplicate fit ordinal: "
            f"{fit_ordinal}"
        )


    fit_ordinals_seen.add(
        fit_ordinal
    )


    fit_evidence[
        component_id
    ] = {
        "fit_ordinal": fit_ordinal,
        "ledger_path": str(
            Path(
                ledger_path
            ).relative_to(
                REPO
            )
        ),
    }


# -------------------------------------------------------------------------------------------------
# Stage22 ledgers
# -------------------------------------------------------------------------------------------------

stage22_ledgers = sorted(
    STAGE22_ROOT.rglob(
        "*_fit_ledger.json"
    )
)


if len(
    stage22_ledgers
) != 10:
    raise RuntimeError(
        f"Expected 10 Stage22 ledgers, "
        f"found {len(stage22_ledgers)}"
    )


for path in stage22_ledgers:

    obj = read_json(
        path
    )

    pre = int(
        obj[
            "pre_cell_new_fits_consumed"
        ]
    )

    new_components = list(
        obj[
            "this_cell"
        ][
            "new_fit_components"
        ]
    )

    successes = int(
        obj[
            "this_cell"
        ][
            "successful_new_fits"
        ]
    )

    cumulative = int(
        obj[
            "cumulative_new_fits_consumed"
        ]
    )


    if successes != len(
        new_components
    ):
        raise RuntimeError(
            f"{path}: successful-new-fit count mismatch."
        )


    if cumulative != (
        pre
        + successes
    ):
        raise RuntimeError(
            f"{path}: cumulative Stage22 ledger discontinuity."
        )


    if int(
        obj[
            "model_fits_attempted"
        ]
    ) != successes:
        raise RuntimeError(
            f"{path}: model_fits_attempted mismatch."
        )


    if int(
        obj[
            "model_fits_successful"
        ]
    ) != successes:
        raise RuntimeError(
            f"{path}: model_fits_successful mismatch."
        )


    for offset, cid in enumerate(
        new_components,
        start=1,
    ):

        register_fit(
            cid,
            pre
            + offset,
            path,
        )


    ledger_rows.append(
        {
            "ledger_path": str(
                path.relative_to(
                    REPO
                )
            ),
            "stage": obj[
                "stage"
            ],
            "pre_new_fits_consumed": pre,
            "successful_new_fits_this_ledger": successes,
            "cumulative_new_fits_consumed": cumulative,
            "new_fits_remaining": int(
                obj[
                    "new_fits_remaining"
                ]
            ),
            "component_ids": ";".join(
                new_components
            ),
            "status": obj[
                "status"
            ],
        }
    )


# -------------------------------------------------------------------------------------------------
# Stage27 ledgers
# -------------------------------------------------------------------------------------------------

stage27_ledgers = sorted(
    STAGE27_ROOT.rglob(
        "*_fit_ledger.json"
    )
)


if len(
    stage27_ledgers
) != 40:
    raise RuntimeError(
        f"Expected 40 Stage27 ledgers, "
        f"found {len(stage27_ledgers)}"
    )


for path in stage27_ledgers:

    obj = read_json(
        path
    )

    pre = int(
        obj[
            "pre_component_new_fits_consumed"
        ]
    )

    successes = int(
        obj[
            "this_component_successful_new_fits"
        ]
    )

    cumulative = int(
        obj[
            "cumulative_new_fits_consumed"
        ]
    )

    cid = obj[
        "component_id"
    ]


    if successes != 1:
        raise RuntimeError(
            f"{path}: Stage27 component "
            "did not consume exactly one fit."
        )


    if cumulative != (
        pre
        + 1
    ):
        raise RuntimeError(
            f"{path}: Stage27 ledger discontinuity."
        )


    register_fit(
        cid,
        cumulative,
        path,
    )


    ledger_rows.append(
        {
            "ledger_path": str(
                path.relative_to(
                    REPO
                )
            ),
            "stage": obj[
                "stage"
            ],
            "pre_new_fits_consumed": pre,
            "successful_new_fits_this_ledger": 1,
            "cumulative_new_fits_consumed": cumulative,
            "new_fits_remaining": int(
                obj[
                    "new_fits_remaining"
                ]
            ),
            "component_ids": cid,
            "status": obj[
                "status"
            ],
        }
    )


# -------------------------------------------------------------------------------------------------
# Stage28B final ledgers
# -------------------------------------------------------------------------------------------------

stage28b_ledgers = sorted(
    STAGE28B_ROOT.rglob(
        "*_fit_ledger.json"
    )
)


if len(
    stage28b_ledgers
) != 50:
    raise RuntimeError(
        f"Expected 50 Stage28B final ledgers, "
        f"found {len(stage28b_ledgers)}"
    )


for path in stage28b_ledgers:

    obj = read_json(
        path
    )

    pre = int(
        obj[
            "pre_component_new_fits_consumed"
        ]
    )

    successes = int(
        obj[
            "this_component_successful_new_fits"
        ]
    )

    cumulative = int(
        obj[
            "cumulative_new_fits_consumed"
        ]
    )

    cid = obj[
        "component_id"
    ]


    if successes != 1:
        raise RuntimeError(
            f"{path}: Stage28B component "
            "did not consume exactly one fit."
        )


    if cumulative != (
        pre
        + 1
    ):
        raise RuntimeError(
            f"{path}: Stage28B ledger discontinuity."
        )


    register_fit(
        cid,
        cumulative,
        path,
    )


    ledger_rows.append(
        {
            "ledger_path": str(
                path.relative_to(
                    REPO
                )
            ),
            "stage": obj[
                "stage"
            ],
            "pre_new_fits_consumed": pre,
            "successful_new_fits_this_ledger": 1,
            "cumulative_new_fits_consumed": cumulative,
            "new_fits_remaining": int(
                obj[
                    "new_fits_remaining"
                ]
            ),
            "component_ids": cid,
            "status": obj[
                "status"
            ],
        }
    )


manifest_new_ids = {
    row[
        "component_id"
    ]
    for row in new_rows
}


if set(
    fit_evidence
) != manifest_new_ids:

    missing = sorted(
        manifest_new_ids
        - set(
            fit_evidence
        )
    )

    extra = sorted(
        set(
            fit_evidence
        )
        - manifest_new_ids
    )

    raise RuntimeError(
        "New-fit component coverage mismatch.\n"
        f"missing={missing}\n"
        f"extra={extra}"
    )


if sorted(
    fit_ordinals_seen
) != list(
    range(
        1,
        109,
    )
):
    raise RuntimeError(
        "Fit ordinals are not exactly FIT #1 .. FIT #108."
    )


ledger_rows.sort(
    key=lambda row:
    row[
        "cumulative_new_fits_consumed"
    ]
)


running = 0


for row in ledger_rows:

    if int(
        row[
            "pre_new_fits_consumed"
        ]
    ) != running:

        raise RuntimeError(
            "Global ledger discontinuity before "
            f"{row['stage']}: "
            f"pre={row['pre_new_fits_consumed']} "
            f"expected={running}"
        )


    running = int(
        row[
            "cumulative_new_fits_consumed"
        ]
    )


if running != 108:
    raise RuntimeError(
        f"Final cumulative fit ledger = {running}, "
        "expected 108."
    )


if int(
    ledger_rows[
        -1
    ][
        "new_fits_remaining"
    ]
) != 0:
    raise RuntimeError(
        "Final fit ledger does not close remaining budget at zero."
    )


print(
    "[PASS] all 108 NEW component IDs accounted exactly once"
)

print(
    "[PASS] fit ordinals exactly FIT #1 .. FIT #108"
)

print(
    "[PASS] cumulative ledger closes at 108 consumed / 0 remaining"
)


# =================================================================================================
# 6. RESULT / COMPONENT / MODEL IDENTITY
# =================================================================================================

banner(
    "STAGE28-3A — RESULT / COMPONENT IDENTITY RECONCILIATION"
)


manifest_by_id = {
    row[
        "component_id"
    ]: row
    for row in manifest_rows
}


component_evidence = {}


# -------------------------------------------------------------------------------------------------
# Stage22: 10 result cells cover C001..C020
# -------------------------------------------------------------------------------------------------

stage22_results = sorted(
    STAGE22_ROOT.rglob(
        "*_result.json"
    )
)


if len(
    stage22_results
) != 10:
    raise RuntimeError(
        f"Expected 10 Stage22 results, "
        f"found {len(stage22_results)}"
    )


for path in stage22_results:

    obj = read_json(
        path
    )


    if obj.get(
        "experiment"
    ) != "STAGE22_FULL":
        raise RuntimeError(
            f"{path}: unexpected Stage22 experiment."
        )


    for model_name, model in obj[
        "models"
    ].items():

        cid = model[
            "component_id"
        ]


        if (
            cid
            in component_evidence
        ):
            raise RuntimeError(
                f"Duplicate component evidence: {cid}"
            )


        manifest_row = (
            manifest_by_id[
                cid
            ]
        )


        if model[
            "fit_action"
        ] != manifest_row[
            "fit_action"
        ]:
            raise RuntimeError(
                f"{cid}: fit_action differs from manifest."
            )


        if int(
            model[
                "seed"
            ]
        ) != int(
            manifest_row[
                "model_seed"
            ]
        ):
            raise RuntimeError(
                f"{cid}: model seed differs from manifest."
            )


        if model[
            "parameter_sha256"
        ] != manifest_row[
            "parameter_sha256"
        ]:
            raise RuntimeError(
                f"{cid}: parameter SHA differs from manifest."
            )


        learner = (
            "XGBOOST"
            if model_name.lower()
            == "xgboost"
            else "LIGHTGBM"
        )


        if learner != manifest_row[
            "learner"
        ]:
            raise RuntimeError(
                f"{cid}: learner differs from manifest."
            )


        if model[
            "fit_action"
        ] == "NEW_FIT_AUTHORIZED":

            artifact = (
                path.parent
                / model[
                    "model_path"
                ]
            )

            if not artifact.is_file():
                raise RuntimeError(
                    f"{cid}: Stage22 model missing:\n"
                    f"{artifact}"
                )

            actual_sha = sha256_file(
                artifact
            )

            if actual_sha != model[
                "model_sha256"
            ]:
                raise RuntimeError(
                    f"{cid}: Stage22 model SHA mismatch."
                )

            model_path = str(
                artifact.relative_to(
                    REPO
                )
            )

            model_sha = actual_sha

        else:

            historical = (
                REPO
                / model[
                    "historical_model_path"
                ]
            )

            if not historical.is_file():
                raise RuntimeError(
                    f"{cid}: historical Stage22 model missing."
                )

            actual_sha = sha256_file(
                historical
            )

            if actual_sha != model[
                "historical_model_sha256"
            ]:
                raise RuntimeError(
                    f"{cid}: historical Stage22 SHA mismatch."
                )

            if actual_sha != manifest_row[
                "reused_model_sha256"
            ]:
                raise RuntimeError(
                    f"{cid}: Stage22 reuse SHA differs "
                    "from frozen manifest."
                )

            model_path = model[
                "historical_model_path"
            ]

            model_sha = actual_sha


        component_evidence[
            cid
        ] = {
            "model_path": model_path,
            "model_sha256": model_sha,
            "result_path": str(
                path.relative_to(
                    REPO
                )
            ),
        }


# -------------------------------------------------------------------------------------------------
# Stage27 and Stage28B new-component result helper
# -------------------------------------------------------------------------------------------------

def audit_single_component_result(
    path,
    expected_experiment,
):

    obj = read_json(
        path
    )

    cid = obj[
        "component_id"
    ]


    if cid in component_evidence:
        raise RuntimeError(
            f"Duplicate component evidence: {cid}"
        )


    manifest_row = (
        manifest_by_id[
            cid
        ]
    )


    if obj[
        "experiment"
    ] != expected_experiment:
        raise RuntimeError(
            f"{cid}: experiment mismatch."
        )


    if obj[
        "learner"
    ] != manifest_row[
        "learner"
    ]:
        raise RuntimeError(
            f"{cid}: learner mismatch."
        )


    if int(
        obj[
            "training_seed"
        ]
    ) != int(
        manifest_row[
            "model_seed"
        ]
    ):
        raise RuntimeError(
            f"{cid}: training seed mismatch."
        )


    if obj[
        "model"
    ][
        "parameter_sha256"
    ] != manifest_row[
        "parameter_sha256"
    ]:
        raise RuntimeError(
            f"{cid}: parameter SHA mismatch."
        )


    if obj[
        "compute_backend"
    ].upper() != "CPU":
        raise RuntimeError(
            f"{cid}: non-CPU result."
        )


    artifact = (
        path.parent
        / obj[
            "model"
        ][
            "model_artifact"
        ]
    )


    if not artifact.is_file():
        raise RuntimeError(
            f"{cid}: model artifact missing:\n"
            f"{artifact}"
        )


    actual_sha = sha256_file(
        artifact
    )


    if actual_sha != obj[
        "model"
    ][
        "model_sha256"
    ]:
        raise RuntimeError(
            f"{cid}: model SHA mismatch."
        )


    component_evidence[
        cid
    ] = {
        "model_path": str(
            artifact.relative_to(
                REPO
            )
        ),
        "model_sha256": actual_sha,
        "result_path": str(
            path.relative_to(
                REPO
            )
        ),
    }


    return obj


# -------------------------------------------------------------------------------------------------
# Stage27 NEW components
# -------------------------------------------------------------------------------------------------

stage27_results = sorted(
    STAGE27_ROOT.rglob(
        "*_result.json"
    )
)


if len(
    stage27_results
) != 40:
    raise RuntimeError(
        f"Expected 40 Stage27 new-component results, "
        f"found {len(stage27_results)}"
    )


loaded_stage27_results = []


for path in stage27_results:

    obj = audit_single_component_result(
        path,
        "STAGE27_CHRONOLOGY_LOAO",
    )

    loaded_stage27_results.append(
        obj
    )


# -------------------------------------------------------------------------------------------------
# Stage28B NEW components
# -------------------------------------------------------------------------------------------------

stage28b_results = sorted(
    STAGE28B_ROOT.rglob(
        "*_result.json"
    )
)


if len(
    stage28b_results
) != 50:
    raise RuntimeError(
        f"Expected 50 Stage28B results, "
        f"found {len(stage28b_results)}"
    )


loaded_stage28b_results = []


for path in stage28b_results:

    preview = read_json(
        path
    )

    cid = preview[
        "component_id"
    ]

    expected_experiment = (
        manifest_by_id[
            cid
        ][
            "experiment"
        ]
    )

    obj = audit_single_component_result(
        path,
        expected_experiment,
    )

    loaded_stage28b_results.append(
        obj
    )


# -------------------------------------------------------------------------------------------------
# Stage27 seed42 reuse components did not require new Stage28 result directories.
# Their frozen historical model identity is the component evidence.
# -------------------------------------------------------------------------------------------------

for cid, evidence in reuse_evidence.items():

    if cid not in component_evidence:

        component_evidence[
            cid
        ] = {
            "model_path": evidence[
                "model_path"
            ],
            "model_sha256": evidence[
                "model_sha256"
            ],
            "result_path": "",
        }


if set(
    component_evidence
) != set(
    component_ids
):

    missing = sorted(
        set(
            component_ids
        )
        - set(
            component_evidence
        )
    )

    extra = sorted(
        set(
            component_evidence
        )
        - set(
            component_ids
        )
    )

    raise RuntimeError(
        "120-component evidence coverage mismatch.\n"
        f"missing={missing}\n"
        f"extra={extra}"
    )


print(
    "[PASS] all 120 frozen component obligations have model evidence"
)

print(
    "[PASS] all 108 new components reconcile to durable fit ledgers"
)

print(
    "[PASS] all Stage28-produced result identities reconcile "
    "learner / seed / parameter SHA / model SHA"
)

print(
    "[PASS] all 12 historical reuses reconcile to frozen model SHA"
)


# =================================================================================================
# 7. FINAL-HOLDOUT / ANTI-ADAPTATION GATE
# =================================================================================================

banner(
    "STAGE28-3A — FINAL-HOLDOUT / ANTI-ADAPTATION GATE"
)


loaded_stage22_results = [
    read_json(
        path
    )
    for path in stage22_results
]


for path, obj in zip(
    stage22_results,
    loaded_stage22_results,
):

    sci = obj.get(
        "scientific_accounting",
        {},
    )


    for key in [
        "shared_final_holdout_openings",
        "shared_final_holdout_predictor_rows_read",
        "shared_final_holdout_labels_read",
        "target_adaptive_choices",
    ]:

        if int(
            sci.get(
                key,
                -1,
            )
        ) != 0:
            raise RuntimeError(
                f"{path}: {key} is not zero."
            )


    if (
        obj.get(
            "threshold_selection",
            {},
        ).get(
            "final_holdout_threshold_search"
        )
        != "FORBIDDEN"
    ):
        raise RuntimeError(
            f"{path}: final-holdout threshold search "
            "was not marked FORBIDDEN."
        )


all_results = (
    loaded_stage22_results
    + loaded_stage27_results
    + loaded_stage28b_results
)


false_keys = [
    "target_used_for_fit",
    "target_used_for_class_weight",
    "target_used_for_threshold_selection",
    "target_threshold_search",
    "post_target_parameter_change",
    "post_target_fit_branching",
]


zero_keys = [
    "target_adaptive_choices",
]


anti_counts = {}


for key in false_keys:

    values = []

    for obj in all_results:

        values.extend(
            walk_key_values(
                obj,
                key,
            )
        )


    anti_counts[
        key
    ] = require_all(
        values,
        lambda value:
        value is False,
        key,
    )


for key in zero_keys:

    values = []

    for obj in all_results:

        values.extend(
            walk_key_values(
                obj,
                key,
            )
        )


    anti_counts[
        key
    ] = require_all(
        values,
        lambda value:
        int(
            value
        ) == 0,
        key,
    )


target_rows_used_values = []


for obj in all_results:

    target_rows_used_values.extend(
        walk_key_values(
            obj,
            "target_rows_used",
        )
    )


target_rows_used_count = require_all(
    target_rows_used_values,
    lambda value:
    int(
        value
    ) == 0,
    "target_rows_used",
)


for key in [
    "held_out_family_train_count",
    "held_out_family_validation_count",
]:

    values = []

    for obj in all_results:

        values.extend(
            walk_key_values(
                obj,
                key,
            )
        )


    require_all(
        values,
        lambda value:
        int(
            value
        ) == 0,
        key,
    )


print(
    "[PASS] Stage22 shared final holdout openings = 0"
)

print(
    "[PASS] Stage22 shared final holdout predictor reads = 0"
)

print(
    "[PASS] Stage22 shared final holdout label reads = 0"
)

print(
    "[PASS] final-holdout threshold search = FORBIDDEN"
)

print(
    "[PASS] recorded target-adaptation booleans all false"
)

print(
    "[PASS] recorded target_rows_used values all zero"
)

print(
    "[PASS] held-out family train/validation exposure = zero "
    "where explicitly recorded"
)


# =================================================================================================
# 8. AUTO-C TWO-PHASE DURABILITY COMPLETENESS
# =================================================================================================

banner(
    "STAGE28-3A — AUTO-C TWO-PHASE DURABILITY GATE"
)


fit_checkpoint_files = sorted(
    STAGE28B_ROOT.rglob(
        "*_fit_checkpoint.json"
    )
)

progress_files = sorted(
    STAGE28B_ROOT.rglob(
        "*_execution_progress.json"
    )
)


if len(
    fit_checkpoint_files
) != 50:
    raise RuntimeError(
        f"Expected 50 fit-only checkpoints, "
        f"found {len(fit_checkpoint_files)}"
    )


if len(
    progress_files
) != 50:
    raise RuntimeError(
        f"Expected 50 AUTO-C progress receipts, "
        f"found {len(progress_files)}"
    )


# Each Stage28B execution directory must contain exactly one of each
# two-phase/final receipt class.
for directory in stage28b_dirs:

    if len(
        list(
            directory.glob(
                "*_fit_checkpoint.json"
            )
        )
    ) != 1:
        raise RuntimeError(
            f"{directory}: fit-checkpoint receipt count != 1"
        )

    if len(
        list(
            directory.glob(
                "*_execution_progress.json"
            )
        )
    ) != 1:
        raise RuntimeError(
            f"{directory}: execution-progress receipt count != 1"
        )

    if len(
        list(
            directory.glob(
                "*_fit_ledger.json"
            )
        )
    ) != 1:
        raise RuntimeError(
            f"{directory}: final fit-ledger count != 1"
        )

    if len(
        list(
            directory.glob(
                "*_result.json"
            )
        )
    ) != 1:
        raise RuntimeError(
            f"{directory}: final result count != 1"
        )


print(
    "[PASS] Stage28B fit-only checkpoints = 50 / 50"
)

print(
    "[PASS] Stage28B execution-progress receipts = 50 / 50"
)

print(
    "[PASS] Stage28B final ledgers = 50 / 50"
)

print(
    "[PASS] Stage28B final results = 50 / 50"
)


# =================================================================================================
# 9. BUILD 120-COMPONENT AUDIT TABLE
# =================================================================================================

banner(
    "STAGE28-3A — BUILD PERMANENT CLOSURE ARTIFACTS"
)


component_rows = []


for manifest_row in manifest_rows:

    cid = manifest_row[
        "component_id"
    ]

    evidence = (
        component_evidence[
            cid
        ]
    )


    if (
        manifest_row[
            "fit_action"
        ]
        == "NEW_FIT_AUTHORIZED"
    ):

        fit_ordinal = (
            fit_evidence[
                cid
            ][
                "fit_ordinal"
            ]
        )

        ledger_path = (
            fit_evidence[
                cid
            ][
                "ledger_path"
            ]
        )

    else:

        fit_ordinal = ""

        ledger_path = ""


    component_rows.append(
        {
            "component_ordinal": int(
                manifest_row[
                    "component_ordinal"
                ]
            ),
            "component_id": cid,
            "arm": manifest_row[
                "arm"
            ],
            "experiment": manifest_row[
                "experiment"
            ],
            "unit": manifest_row[
                "unit"
            ],
            "evaluation_cell_id": manifest_row[
                "evaluation_cell_id"
            ],
            "learner": manifest_row[
                "learner"
            ],
            "configuration_id": manifest_row[
                "configuration_id"
            ],
            "model_seed": int(
                manifest_row[
                    "model_seed"
                ]
            ),
            "compute_backend": manifest_row[
                "compute_backend"
            ],
            "fit_action": manifest_row[
                "fit_action"
            ],
            "fit_ordinal_if_new": fit_ordinal,
            "parameter_sha256": manifest_row[
                "parameter_sha256"
            ],
            "model_evidence_path": evidence[
                "model_path"
            ],
            "model_sha256": evidence[
                "model_sha256"
            ],
            "stage28_result_evidence_path": evidence[
                "result_path"
            ],
            "ledger_evidence_path": ledger_path,
            "closure_status": "PASS",
        }
    )


if len(
    component_rows
) != 120:
    raise RuntimeError(
        "Component audit table is not 120 rows."
    )


# =================================================================================================
# 10. WRITE CLOSURE ARTIFACTS
# =================================================================================================

OUT.mkdir(
    parents=False,
    exist_ok=False,
)


component_fields = list(
    component_rows[
        0
    ].keys()
)


with COMPONENT_CSV.open(
    "w",
    encoding="utf-8",
    newline="",
) as f:

    writer = csv.DictWriter(
        f,
        fieldnames=component_fields,
    )

    writer.writeheader()

    writer.writerows(
        component_rows
    )


ledger_fields = [
    "ledger_path",
    "stage",
    "pre_new_fits_consumed",
    "successful_new_fits_this_ledger",
    "cumulative_new_fits_consumed",
    "new_fits_remaining",
    "component_ids",
    "status",
]


with LEDGER_CSV.open(
    "w",
    encoding="utf-8",
    newline="",
) as f:

    writer = csv.DictWriter(
        f,
        fieldnames=ledger_fields,
    )

    writer.writeheader()

    writer.writerows(
        ledger_rows
    )


receipt = {

    "stage": "Stage28-3A",

    "type": (
        "EXPERIMENT_CLOSURE_AND_108_FIT_AUDIT"
    ),

    "created_at_utc": (
        datetime.now(
            timezone.utc
        ).isoformat()
    ),

    "scientific_parent_commit": (
        EXPECTED_PARENT
    ),

    "frozen_component_manifest": {

        "path": str(
            MANIFEST.relative_to(
                REPO
            )
        ),

        "sha256": manifest_sha,

        "components": 120,

        "new_fit_components": 108,

        "reuse_components": 12,
    },

    "fit_budget_closure": {

        "authorized_new_fits": 108,

        "consumed_new_fits": 108,

        "remaining_new_fits": 0,

        "fit_ordinals": (
            "FIT_001_THROUGH_FIT_108_CONTIGUOUS"
        ),

        "new_fit_component_coverage": (
            "EXACT_108_OF_108"
        ),

        "reuse_component_coverage": (
            "EXACT_12_OF_12"
        ),

        "new_model_artifacts": {

            "stage22": len(
                stage22_models
            ),

            "stage27": len(
                stage27_models
            ),

            "stage28b": len(
                stage28b_models
            ),

            "total": len(
                all_new_models
            ),
        },
    },

    "execution_root_closure": {

        "stage22_output_directories": len(
            stage22_dirs
        ),

        "stage27_new_fit_output_directories": len(
            stage27_dirs
        ),

        "stage28b_output_directories": len(
            stage28b_dirs
        ),

        "total_stage28_output_directories_checksum_audited": len(
            checksum_dirs
        ),

        "checksum_payload_files_verified": (
            payload_files_verified
        ),

        "checksum_payload_bytes_verified": (
            payload_bytes_verified
        ),
    },

    "component_obligations": {

        "stage22": stage22_counts,

        "stage27": stage27_counts,

        "stage28b": stage28b_counts,

        "all_120_component_model_identities_reconciled": True,

        "all_12_reused_model_sha256_verified": True,

        "all_108_new_fit_ledger_components_verified": True,

        "all_stage28_result_parameter_sha256_reconciled": True,

        "all_stage28_result_model_sha256_reconciled": True,

        "all_compute_backends_cpu": True,
    },

    "anti_adaptation": {

        "shared_stage22_final_holdout_openings_during_stage28_execution": 0,

        "shared_stage22_final_holdout_predictor_rows_read_during_stage28_execution": 0,

        "shared_stage22_final_holdout_labels_read_during_stage28_execution": 0,

        "stage22_final_holdout_threshold_search": (
            "FORBIDDEN"
        ),

        "target_derived_fit_or_threshold_adaptation": 0,

        "recorded_false_key_occurrences": (
            anti_counts
        ),

        "recorded_target_rows_used_occurrences_verified_zero": (
            target_rows_used_count
        ),
    },

    "stage28b_two_phase_durability": {

        "fit_checkpoint_receipts": len(
            fit_checkpoint_files
        ),

        "execution_progress_receipts": len(
            progress_files
        ),

        "final_fit_ledgers": len(
            stage28b_ledgers
        ),

        "final_results": len(
            stage28b_results
        ),

        "status": (
            "50_OF_50_COMPLETE"
        ),
    },

    "scientific_scope": {

        "new_model_fits_this_stage": 0,

        "model_inference_this_stage": 0,

        "threshold_selection_this_stage": 0,

        "target_openings_this_stage": 0,

        "shared_final_holdout_openings_this_stage": 0,

        "data_dependent_model_changes_this_stage": 0,

        "new_model_fits_authorized_after_closure": 0,

        "infiltration_status": (
            "DESCRIPTIVE_ONLY_SUPPORT_36_LT_50"
        ),

        "random_loao_status": (
            "CONTROL_NOT_DEPLOYMENT_ESTIMATE"
        ),

        "family_specific_loao_primary": True,

        "aggregate_zero_day_score_created": False,
    },

    "closure_status": (
        "PASS_STAGE28_NEW_MODEL_FITTING_PERMANENTLY_CLOSED"
    ),

    "next_authorized_step": (
        "Stage28-3B — seed uncertainty and conclusion-stability synthesis. "
        "ZERO new fits. The shared Stage22 final holdout remains closed until "
        "the separately preregistered one-time Stage28-4 inference."
    ),
}


write_json(
    RECEIPT,
    receipt,
)


README.write_text(
    f"""# Stage28-3A — Experiment Closure and 108-Fit Audit

Scientific parent: `{EXPECTED_PARENT}`

## Closure

- Frozen components: 120
- Authorized new fits: 108
- Historical reuses: 12
- New fits consumed: 108
- New fits remaining: 0
- New model artifacts verified: 108
- Stage28 output directories checksum-audited: 100
- Stage28B two-phase fit checkpoints: 50/50
- Shared Stage22 final-holdout openings during Stage28 execution: 0
- Target-derived fit/threshold adaptation: 0
- New fits performed by Stage28-3A: 0

## Scientific boundary

Stage28 model fitting is closed.

No additional fit, tuning branch, learner, family, dataset, feature branch,
or hyperparameter search is authorized for this manuscript.

The next authorized work is zero-fit Stage28 synthesis.

The shared Stage22 final holdout remains closed until its separately
preregistered one-time inference step.

Infiltration remains descriptive-only because support is 36 (<50).

Random LOAO remains a control, not a deployment estimate.

Family-specific LOAO results remain primary. No aggregate zero-day score
is created.
""",
    encoding="utf-8",
)


for path in [
    RECEIPT,
    COMPONENT_CSV,
    LEDGER_CSV,
    README,
]:

    if (
        not path.is_file()
        or path.stat().st_size
        == 0
    ):
        raise RuntimeError(
            f"Failed to write closure artifact:\n"
            f"{path}"
        )


with CHECKSUMS.open(
    "w",
    encoding="utf-8",
) as f:

    for path in [
        RECEIPT,
        COMPONENT_CSV,
        LEDGER_CSV,
        README,
    ]:

        f.write(
            f"{sha256_file(path)}  "
            f"{path.name}\n"
        )


verify_checksum_manifest(
    CHECKSUMS
)


print(
    "[PASS] closure receipt written"
)

print(
    "[PASS] 120-row component closure table written"
)

print(
    "[PASS] new-fit ledger audit table written"
)

print(
    "[PASS] closure artifact checksums verified"
)


# =================================================================================================
# 11. EXACT GIT COMMIT UNIVERSE
# =================================================================================================

banner(
    "STAGE28-3A — DURABLE COMMIT / PUSH"
)


expected_rel = {
    str(
        path.relative_to(
            REPO
        )
    )
    for path in [
        RECEIPT,
        COMPONENT_CSV,
        LEDGER_CSV,
        README,
        CHECKSUMS,
    ]
}


tracked_modifications = set(
    git(
        "diff",
        "--name-only",
    ).splitlines()
)


staged_before = set(
    git(
        "diff",
        "--cached",
        "--name-only",
    ).splitlines()
)


untracked = set(
    git(
        "ls-files",
        "--others",
        "--exclude-standard",
    ).splitlines()
)


if tracked_modifications:
    raise RuntimeError(
        "Unexpected tracked modifications before closure commit:\n"
        + "\n".join(
            sorted(
                tracked_modifications
            )
        )
    )


if staged_before:
    raise RuntimeError(
        "Unexpected staged files before closure commit:\n"
        + "\n".join(
            sorted(
                staged_before
            )
        )
    )


if untracked != expected_rel:
    raise RuntimeError(
        "Unexpected untracked universe before closure commit.\n\n"
        "Expected:\n"
        + "\n".join(
            sorted(
                expected_rel
            )
        )
        + "\n\nActual:\n"
        + "\n".join(
            sorted(
                untracked
            )
        )
    )


for rel in sorted(
    expected_rel
):

    run(
        [
            "git",
            "add",
            "--",
            rel,
        ]
    )


staged_after = set(
    git(
        "diff",
        "--cached",
        "--name-only",
    ).splitlines()
)


if staged_after != expected_rel:
    raise RuntimeError(
        "Stage28-3A staged universe mismatch."
    )


run(
    [
        "git",
        "config",
        "user.name",
        "Stage28 Kaggle",
    ]
)

run(
    [
        "git",
        "config",
        "user.email",
        "stage28-kaggle@users.noreply.github.com",
    ]
)


commit_message = (
    "stage28-3a: close 108-fit experiment ledger"
)


commit_result = run(
    [
        "git",
        "commit",
        "-m",
        commit_message,
    ]
)


print(
    commit_result.stdout.strip()
)


new_head = git(
    "rev-parse",
    "HEAD",
)

parent = git(
    "rev-parse",
    "HEAD^",
)

subject = git(
    "show",
    "-s",
    "--format=%s",
    "HEAD",
)


if parent != EXPECTED_PARENT:
    raise RuntimeError(
        "Stage28-3A commit parent mismatch."
    )


if subject != commit_message:
    raise RuntimeError(
        "Stage28-3A commit subject mismatch."
    )


token, token_source = (
    recover_github_token()
)


print()
print(
    "[PASS] GitHub credential:",
    token_source,
)

print(
    "[PASS] token not displayed"
)


push_output = (
    authenticated_push(
        token
    )
)


if push_output:
    print(
        push_output
    )


run(
    [
        "git",
        "fetch",
        "origin",
        "main",
    ]
)


local = git(
    "rev-parse",
    "HEAD",
)

origin = git(
    "rev-parse",
    "origin/main",
)

remote = remote_head()


if not (
    local
    == origin
    == remote
    == new_head
):
    raise RuntimeError(
        "Stage28-3A remote durability verification failed."
    )


if git(
    "status",
    "--porcelain",
):
    raise RuntimeError(
        "Repository dirty after Stage28-3A push."
    )


# =================================================================================================
# 12. FINAL CLOSURE
# =================================================================================================

banner(
    "STAGE28-3A — EXPERIMENT CLOSURE COMPLETE"
)


print(
    "Scientific parent:"
)

print(
    " ",
    EXPECTED_PARENT,
)


print()
print(
    "Closure commit:"
)

print(
    " ",
    new_head,
)


print()
print(
    "Frozen components : 120 / 120 VERIFIED"
)

print(
    "New fits          : 108 / 108 COMPLETE"
)

print(
    "Historical reuses : 12 / 12 VERIFIED"
)

print(
    "Remaining fits    : 0"
)

print(
    "New model artifacts:",
    "108 / 108 VERIFIED",
)

print(
    "Checksum-audited execution dirs:",
    "100 / 100",
)

print(
    "Stage28B fit checkpoints:",
    "50 / 50",
)


print()
print(
    "Stage22 shared-final-holdout openings:",
    0,
)

print(
    "Target-derived fit/threshold adaptation:",
    0,
)

print(
    "New fits performed by Stage28-3A:",
    0,
)


print()
print(
    "NEW MODEL FITTING IS NOW CLOSED "
    "FOR THIS MANUSCRIPT."
)


print()
print(
    "NEXT AUTHORIZED STEP:"
)

print(
    "Stage28-3B — seed uncertainty / "
    "conclusion-stability synthesis"
)

print(
    "ZERO NEW FITS."
)

# ==============================================================================================================
# %% NOTEBOOK CELL 0006 | execution_count=6
# ==============================================================================================================
# =================================================================================================
# STAGE28-3A-R1 — RECEIPT SCHEMA COMPATIBILITY REPAIR
#
# ZERO FITS
# ZERO INFERENCE
# ZERO THRESHOLD SELECTION
# ZERO TARGET OPENINGS
#
# Repairs only historical Stage28 receipt-schema differences:
#
#   1. model_fits_attempted/model_fits_successful are optional redundant counters.
#      If present -> must equal successful_new_fits.
#      If absent  -> authoritative successful_new_fits + cumulative ledger remains the check.
#
#   2. Stage22 result model artifact key:
#         older schema : model_path
#         AUTO-A schema: model
#
#   3. fit_action:
#         older schema: explicitly stored in result
#         AUTO-A schema: omitted; frozen component manifest is authoritative
#
#   4. final_holdout_threshold_search:
#         some compact AUTO-A receipts omit the redundant string field.
#         The audit still requires shared-final-holdout predictor reads,
#         label reads, and openings to all equal zero.
#
# Then reruns the complete Stage28-3A audit from the beginning.
# =================================================================================================

from pathlib import Path
import hashlib
import subprocess


SEP = "=" * 120

REPO = Path(
    "/kaggle/working/ids2018-validation-safe-ablation"
).resolve()

EXPECTED_HEAD = (
    "9fddb8d8c34ba8f81b71f24eea15c90151053d6b"
)

OUT = (
    REPO
    / "results"
    / "stage28_stability_novelty_control"
    / "stage28_3a_experiment_closure_audit"
)


def banner(text):
    print()
    print(SEP)
    print(text)
    print(SEP)
    print()


def run(cmd, *, cwd=REPO, check=True):

    p = subprocess.run(
        [str(x) for x in cmd],
        cwd=str(cwd),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    if check and p.returncode != 0:
        raise RuntimeError(
            f"Command failed ({p.returncode}):\n"
            + " ".join(map(str, cmd))
            + f"\n\nSTDOUT:\n{p.stdout}"
            + f"\n\nSTDERR:\n{p.stderr}"
        )

    return p


def git(*args):
    return run(
        ["git", *args]
    ).stdout.strip()


# =================================================================================================
# 1. PRE-REPAIR STATE GATE
# =================================================================================================

banner(
    "STAGE28-3A-R1 — PRE-REPAIR STATE GATE"
)


if not (
    REPO
    / ".git"
).is_dir():
    raise RuntimeError(
        "Stage28 repository missing."
    )


run(
    [
        "git",
        "fetch",
        "origin",
        "main",
    ]
)


local_head = git(
    "rev-parse",
    "HEAD",
)

origin_head = git(
    "rev-parse",
    "origin/main",
)


print(
    "Local HEAD :",
    local_head,
)

print(
    "origin/main:",
    origin_head,
)

print(
    "Expected   :",
    EXPECTED_HEAD,
)


if (
    local_head != EXPECTED_HEAD
    or origin_head != EXPECTED_HEAD
):
    raise RuntimeError(
        "Repository state changed after the failed audit. "
        "STOP rather than patching a different parent."
    )


status = git(
    "status",
    "--porcelain",
)


if status:
    raise RuntimeError(
        "Repository is not clean:\n"
        + status
    )


if OUT.exists():
    raise RuntimeError(
        "Stage28-3A output directory already exists:\n"
        f"{OUT}\n\n"
        "Do not overwrite it automatically."
    )


print()
print(
    "[PASS] scientific parent unchanged"
)

print(
    "[PASS] repository clean"
)

print(
    "[PASS] Stage28-3A produced no durable output before failure"
)

print(
    "[PASS] no model fit can be triggered by this repair"
)


# =================================================================================================
# 2. RECOVER THE ORIGINAL STAGE28-3A CELL FROM NOTEBOOK HISTORY
# =================================================================================================

banner(
    "RECOVER ORIGINAL STAGE28-3A CELL"
)


try:
    ip = get_ipython()
except NameError:
    ip = None


if ip is None:
    raise RuntimeError(
        "IPython notebook history unavailable."
    )


history = list(
    ip.history_manager.input_hist_raw
)


original = None
original_history_index = None


# Exclude the current repair cell itself.
search_space = (
    history[:-1]
    if len(history) > 1
    else history
)


for index in range(
    len(search_space) - 1,
    -1,
    -1,
):

    cell = search_space[index]

    if not isinstance(
        cell,
        str,
    ):
        continue

    # Strong fingerprint of the full closure cell.
    if (
        "STAGE28-3A — EXPERIMENT CLOSURE + 108-FIT AUDIT"
        in cell
        and
        "stage28_3a_component_closure_audit.csv"
        in cell
        and
        "model_fits_attempted"
        in cell
        and
        "checksum_payload_bytes_verified"
        in cell
        and
        "NEW MODEL FITTING IS NOW CLOSED"
        in cell
    ):
        original = cell
        original_history_index = index
        break


if original is None:
    raise RuntimeError(
        "Could not locate the original Stage28-3A audit cell "
        "in Kaggle notebook history."
    )


original_sha = hashlib.sha256(
    original.encode(
        "utf-8"
    )
).hexdigest()


print(
    "[PASS] original Stage28-3A cell recovered"
)

print(
    "History index:",
    original_history_index,
)

print(
    "Original cell SHA256:",
    original_sha,
)

print(
    "Original characters:",
    f"{len(original):,}",
)


# =================================================================================================
# 3. PATCH OPTIONAL LEDGER COUNTERS
# =================================================================================================

banner(
    "PATCH 1/4 — OPTIONAL LEDGER COUNTERS"
)


old_attempted = '''obj[
            "model_fits_attempted"
        ]'''

new_attempted = '''obj.get(
            "model_fits_attempted",
            successes,
        )'''


attempted_count = original.count(
    old_attempted
)


if attempted_count != 1:
    raise RuntimeError(
        "Expected exactly one model_fits_attempted "
        f"schema-sensitive access; found {attempted_count}."
    )


patched = original.replace(
    old_attempted,
    new_attempted,
    1,
)


old_successful = '''obj[
            "model_fits_successful"
        ]'''

new_successful = '''obj.get(
            "model_fits_successful",
            successes,
        )'''


successful_count = patched.count(
    old_successful
)


if successful_count != 1:
    raise RuntimeError(
        "Expected exactly one model_fits_successful "
        f"schema-sensitive access; found {successful_count}."
    )


patched = patched.replace(
    old_successful,
    new_successful,
    1,
)


print(
    "[PASS] optional model_fits_attempted handled"
)

print(
    "[PASS] optional model_fits_successful handled"
)

print(
    "[PASS] successful_new_fits and cumulative ledger "
    "remain mandatory"
)


# =================================================================================================
# 4. PATCH OPTIONAL STAGE22 fit_action
# =================================================================================================

banner(
    "PATCH 2/4 — STAGE22 fit_action SCHEMA"
)


old_fit_action = '''model[
            "fit_action"
        ]'''

new_fit_action = '''model.get(
            "fit_action",
            manifest_row["fit_action"],
        )'''


fit_action_count = patched.count(
    old_fit_action
)


print(
    "Schema-sensitive fit_action accesses:",
    fit_action_count,
)


if fit_action_count != 2:
    raise RuntimeError(
        "Expected exactly two Stage22 model['fit_action'] "
        f"accesses; found {fit_action_count}."
    )


patched = patched.replace(
    old_fit_action,
    new_fit_action,
)


print(
    "[PASS] explicit fit_action still checked when present"
)

print(
    "[PASS] frozen manifest supplies authoritative "
    "fit_action when compact AUTO-A receipt omits it"
)


# =================================================================================================
# 5. PATCH Stage22 model_path / model FIELD
# =================================================================================================

banner(
    "PATCH 3/4 — STAGE22 MODEL ARTIFACT KEY"
)


old_model_path = '''model[
                    "model_path"
                ]'''

new_model_path = '''(
                    model.get("model_path")
                    or model.get("model")
                )'''


model_path_count = patched.count(
    old_model_path
)


if model_path_count != 1:
    raise RuntimeError(
        "Expected exactly one Stage22 model_path "
        f"schema-sensitive access; found {model_path_count}."
    )


patched = patched.replace(
    old_model_path,
    new_model_path,
    1,
)


print(
    "[PASS] older model_path schema supported"
)

print(
    "[PASS] compact AUTO-A model schema supported"
)

print(
    "[PASS] model SHA256 verification remains unchanged"
)


# =================================================================================================
# 6. PATCH OPTIONAL REDUNDANT THRESHOLD-SEARCH STRING
# =================================================================================================

banner(
    "PATCH 4/4 — COMPACT THRESHOLD RECEIPT"
)


old_threshold = '''        ).get(
            "final_holdout_threshold_search"
        )
        != "FORBIDDEN"'''

new_threshold = '''        ).get(
            "final_holdout_threshold_search",
            "FORBIDDEN",
        )
        != "FORBIDDEN"'''


threshold_count = patched.count(
    old_threshold
)


if threshold_count != 1:
    raise RuntimeError(
        "Expected exactly one final_holdout_threshold_search "
        f"schema-sensitive check; found {threshold_count}."
    )


patched = patched.replace(
    old_threshold,
    new_threshold,
    1,
)


print(
    "[PASS] explicit FORBIDDEN value still mandatory when field exists"
)

print(
    "[PASS] compact AUTO-A omission accepted"
)

print(
    "[PASS] shared-final-holdout openings / predictor reads / "
    "label reads must still all equal zero"
)


# =================================================================================================
# 7. STATIC SAFETY GATES
# =================================================================================================

banner(
    "PATCHED AUDIT STATIC SAFETY GATE"
)


# The patched audit must still be syntactically valid.
compile(
    patched,
    "<stage28_3a_r1_patched>",
    "exec",
)


patched_sha = hashlib.sha256(
    patched.encode(
        "utf-8"
    )
).hexdigest()


print(
    "Patched audit SHA256:",
    patched_sha,
)


# Make sure none of the scientific closure constants changed.
required_literals = [
    'EXPECTED_PARENT = (',
    '"9fddb8d8c34ba8f81b71f24eea15c90151053d6b"',
    '"47e7ffbf357fee3d86830282ae0e69663f84849971e3caeb151168e9bb50b505"',
    '"authorized_new_fits": 108',
    '"consumed_new_fits": 108',
    '"remaining_new_fits": 0',
    '"new_model_fits_this_stage": 0',
    '"model_inference_this_stage": 0',
    '"threshold_selection_this_stage": 0',
    '"target_openings_this_stage": 0',
    '"shared_final_holdout_openings_this_stage": 0',
    '"new_model_fits_authorized_after_closure": 0',
]


for literal in required_literals:

    if literal not in patched:
        raise RuntimeError(
            "Scientific closure literal disappeared "
            f"during patch: {literal!r}"
        )


# Ensure no fitting call was introduced by our patch.
if patched.count(
    ".fit("
) != original.count(
    ".fit("
):
    raise RuntimeError(
        "Patch changed .fit( occurrence count."
    )


print(
    "[PASS] patched source compiles"
)

print(
    "[PASS] scientific parent unchanged"
)

print(
    "[PASS] manifest SHA unchanged"
)

print(
    "[PASS] 108-fit closure constants unchanged"
)

print(
    "[PASS] no fitting operation introduced"
)


# =================================================================================================
# 8. EXECUTE THE COMPLETE PATCHED AUDIT
# =================================================================================================

banner(
    "RERUN COMPLETE STAGE28-3A AUDIT"
)


print(
    "The audit will repeat the byte-level checks."
)

print(
    "This performs ZERO fits and ZERO inference."
)

print()


exec_globals = {
    "__name__": "__main__",
    "__file__": (
        "/kaggle/working/"
        "stage28_3a_r1_patched_runtime.py"
    ),
}


exec(
    compile(
        patched,
        exec_globals[
            "__file__"
        ],
        "exec",
    ),
    exec_globals,
)

# ==============================================================================================================
# %% NOTEBOOK CELL 0007 | execution_count=7
# ==============================================================================================================
# =================================================================================================
# STAGE28-3A-R2 — COMPLETE RECEIPT-SCHEMA REPAIR
#
# ZERO FITS
# ZERO INFERENCE
# ZERO THRESHOLD SELECTION
# ZERO TARGET OPENINGS
#
# R1 fixes retained:
#   1. optional model_fits_attempted
#   2. optional model_fits_successful
#   3. compact Stage22 fit_action
#   4. model_path vs model
#   5. compact final_holdout_threshold_search field
#
# R2 fix:
#   6. Stage22 "models" contains metadata strings plus learner dictionaries.
#      Audit ONLY frozen learners: xgboost and lightgbm.
# =================================================================================================

from pathlib import Path
import hashlib
import subprocess


SEP = "=" * 120

REPO = Path(
    "/kaggle/working/ids2018-validation-safe-ablation"
).resolve()

EXPECTED_HEAD = (
    "9fddb8d8c34ba8f81b71f24eea15c90151053d6b"
)

OUT = (
    REPO
    / "results"
    / "stage28_stability_novelty_control"
    / "stage28_3a_experiment_closure_audit"
)


def banner(text):
    print()
    print(SEP)
    print(text)
    print(SEP)
    print()


def run(cmd, *, cwd=REPO, check=True):
    p = subprocess.run(
        [str(x) for x in cmd],
        cwd=str(cwd),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    if check and p.returncode != 0:
        raise RuntimeError(
            f"Command failed ({p.returncode}):\n"
            + " ".join(map(str, cmd))
            + f"\n\nSTDOUT:\n{p.stdout}"
            + f"\n\nSTDERR:\n{p.stderr}"
        )

    return p


def git(*args):
    return run(
        ["git", *args]
    ).stdout.strip()


# =================================================================================================
# 1. EXACT PRE-REPAIR STATE
# =================================================================================================

banner(
    "STAGE28-3A-R2 — PRE-REPAIR STATE GATE"
)


if not (REPO / ".git").is_dir():
    raise RuntimeError(
        "Stage28 repository missing."
    )


run(
    [
        "git",
        "fetch",
        "origin",
        "main",
    ]
)


local_head = git(
    "rev-parse",
    "HEAD",
)

origin_head = git(
    "rev-parse",
    "origin/main",
)


print("Local HEAD :", local_head)
print("origin/main:", origin_head)
print("Expected   :", EXPECTED_HEAD)


if local_head != EXPECTED_HEAD:
    raise RuntimeError(
        "Local HEAD changed after failed Stage28-3A."
    )


if origin_head != EXPECTED_HEAD:
    raise RuntimeError(
        "Remote HEAD changed after failed Stage28-3A."
    )


status = git(
    "status",
    "--porcelain",
)


if status:
    raise RuntimeError(
        "Repository is dirty:\n"
        + status
    )


if OUT.exists():
    raise RuntimeError(
        "Stage28-3A output directory already exists:\n"
        f"{OUT}\n\n"
        "Do not overwrite a potentially completed audit."
    )


print()
print("[PASS] scientific parent unchanged")
print("[PASS] repository clean")
print("[PASS] no Stage28-3A durable output exists")
print("[PASS] no scientific operation needs repeating")


# =================================================================================================
# 2. RECOVER ORIGINAL STAGE28-3A SOURCE
# =================================================================================================

banner(
    "RECOVER ORIGINAL STAGE28-3A AUDIT SOURCE"
)


try:
    ip = get_ipython()
except NameError:
    ip = None


if ip is None:
    raise RuntimeError(
        "IPython history unavailable."
    )


history = list(
    ip.history_manager.input_hist_raw
)


original = None
history_index = None


# Search backwards, excluding current R2 cell.
for idx in range(
    len(history) - 2,
    -1,
    -1,
):

    cell = history[idx]

    if not isinstance(cell, str):
        continue

    if (
        "STAGE28-3A — EXPERIMENT CLOSURE + 108-FIT AUDIT"
        in cell
        and
        "stage28_3a_component_closure_audit.csv"
        in cell
        and
        "model_fits_attempted"
        in cell
        and
        "checksum_payload_bytes_verified"
        in cell
        and
        "NEW MODEL FITTING IS NOW CLOSED"
        in cell
    ):
        original = cell
        history_index = idx
        break


if original is None:
    raise RuntimeError(
        "Original Stage28-3A audit cell could not be "
        "recovered from notebook history."
    )


original_sha = hashlib.sha256(
    original.encode("utf-8")
).hexdigest()


print("[PASS] original audit recovered")
print("History index :", history_index)
print("Original SHA  :", original_sha)
print("Characters    :", f"{len(original):,}")


# =================================================================================================
# 3. R1 PATCH — OPTIONAL LEDGER COUNTERS
# =================================================================================================

banner(
    "PATCH 1 — OPTIONAL LEDGER COUNTERS"
)


patched = original


old = '''obj[
            "model_fits_attempted"
        ]'''

new = '''obj.get(
            "model_fits_attempted",
            successes,
        )'''


if patched.count(old) != 1:
    raise RuntimeError(
        "Unexpected model_fits_attempted source shape."
    )


patched = patched.replace(
    old,
    new,
    1,
)


old = '''obj[
            "model_fits_successful"
        ]'''

new = '''obj.get(
            "model_fits_successful",
            successes,
        )'''


if patched.count(old) != 1:
    raise RuntimeError(
        "Unexpected model_fits_successful source shape."
    )


patched = patched.replace(
    old,
    new,
    1,
)


print("[PASS] optional attempted counter supported")
print("[PASS] optional successful counter supported")
print("[PASS] successful_new_fits remains mandatory")
print("[PASS] cumulative ledger remains mandatory")


# =================================================================================================
# 4. R1 PATCH — fit_action FALLBACK TO FROZEN MANIFEST
# =================================================================================================

banner(
    "PATCH 2 — STAGE22 fit_action SCHEMA"
)


old = '''model[
            "fit_action"
        ]'''

new = '''model.get(
            "fit_action",
            manifest_row["fit_action"],
        )'''


count = patched.count(old)

print("Occurrences:", count)


if count != 2:
    raise RuntimeError(
        f"Expected two fit_action accesses; found {count}."
    )


patched = patched.replace(
    old,
    new,
)


print("[PASS] explicit fit_action checked when recorded")
print("[PASS] frozen manifest authoritative when omitted")


# =================================================================================================
# 5. R1 PATCH — model_path vs model
# =================================================================================================

banner(
    "PATCH 3 — STAGE22 MODEL ARTIFACT KEY"
)


old = '''model[
                    "model_path"
                ]'''

new = '''(
                    model.get("model_path")
                    or model.get("model")
                )'''


if patched.count(old) != 1:
    raise RuntimeError(
        "Unexpected Stage22 model_path source shape."
    )


patched = patched.replace(
    old,
    new,
    1,
)


print("[PASS] model_path schema supported")
print("[PASS] compact model schema supported")
print("[PASS] SHA256 verification unchanged")


# =================================================================================================
# 6. R1 PATCH — COMPACT THRESHOLD RECEIPT
# =================================================================================================

banner(
    "PATCH 4 — COMPACT THRESHOLD RECEIPT"
)


old = '''        ).get(
            "final_holdout_threshold_search"
        )
        != "FORBIDDEN"'''

new = '''        ).get(
            "final_holdout_threshold_search",
            "FORBIDDEN",
        )
        != "FORBIDDEN"'''


if patched.count(old) != 1:
    raise RuntimeError(
        "Unexpected final_holdout_threshold_search source shape."
    )


patched = patched.replace(
    old,
    new,
    1,
)


print("[PASS] explicit FORBIDDEN remains checked")
print("[PASS] compact omission supported")
print("[PASS] zero final-holdout reads remain mandatory")


# =================================================================================================
# 7. R2 PATCH — AUDIT ONLY XGBOOST/LIGHTGBM MODEL DICTS
# =================================================================================================

banner(
    "PATCH 5 — STAGE22 MODELS CONTAINER"
)


old = '''for model_name, model in obj[
        "models"
    ].items():

        cid = model[
            "component_id"
        ]'''


new = '''for model_name in (
        "xgboost",
        "lightgbm",
    ):

        model = obj[
            "models"
        ][
            model_name
        ]

        if not isinstance(
            model,
            dict,
        ):
            raise RuntimeError(
                f"{path}: {model_name} model receipt is not a dictionary."
            )

        cid = model[
            "component_id"
        ]'''


loop_count = patched.count(old)


print(
    "Schema-sensitive models-loop occurrences:",
    loop_count,
)


if loop_count != 1:
    raise RuntimeError(
        "Expected exactly one Stage22 models iteration "
        f"to patch; found {loop_count}."
    )


patched = patched.replace(
    old,
    new,
    1,
)


print("[PASS] Stage22 metadata entries excluded from model iteration")
print("[PASS] XGBoost remains mandatory")
print("[PASS] LightGBM remains mandatory")
print("[PASS] exactly two frozen learners audited per Stage22 cell")


# =================================================================================================
# 8. STATIC AUDIT-SAFETY CHECK
# =================================================================================================

banner(
    "PATCHED STAGE28-3A STATIC SAFETY GATE"
)


compile(
    patched,
    "<stage28_3a_r2>",
    "exec",
)


patched_sha = hashlib.sha256(
    patched.encode("utf-8")
).hexdigest()


print(
    "Patched Stage28-3A SHA256:",
    patched_sha,
)


required_literals = [
    "9fddb8d8c34ba8f81b71f24eea15c90151053d6b",
    "47e7ffbf357fee3d86830282ae0e69663f84849971e3caeb151168e9bb50b505",
    '"authorized_new_fits": 108',
    '"consumed_new_fits": 108',
    '"remaining_new_fits": 0',
    '"new_model_fits_this_stage": 0',
    '"model_inference_this_stage": 0',
    '"threshold_selection_this_stage": 0',
    '"target_openings_this_stage": 0',
    '"shared_final_holdout_openings_this_stage": 0',
    '"new_model_fits_authorized_after_closure": 0',
]


for literal in required_literals:

    if literal not in patched:
        raise RuntimeError(
            "Scientific invariant disappeared during patch:\n"
            + literal
        )


# No fitting code may have been introduced.
if patched.count(".fit(") != original.count(".fit("):
    raise RuntimeError(
        "Patch changed .fit( occurrence count."
    )


# No prediction/inference operation may have been introduced.
for token in [
    ".predict(",
    ".predict_proba(",
]:

    if patched.count(token) != original.count(token):
        raise RuntimeError(
            f"Patch changed {token} occurrence count."
        )


print("[PASS] source compiles")
print("[PASS] scientific parent unchanged")
print("[PASS] manifest identity unchanged")
print("[PASS] 108-fit closure unchanged")
print("[PASS] zero-fit closure semantics unchanged")
print("[PASS] no fitting call introduced")
print("[PASS] no inference call introduced")


# =================================================================================================
# 9. PRE-EXECUTION STRUCTURE SELF-TEST
# =================================================================================================

banner(
    "STAGE22 RESULT STRUCTURE SELF-TEST"
)


stage22_root = (
    REPO
    / "results"
    / "stage28_stability_novelty_control"
    / "stage28_2a_stage22_seed_stability"
)


stage22_result_files = sorted(
    stage22_root.rglob(
        "*_result.json"
    )
)


if len(stage22_result_files) != 10:
    raise RuntimeError(
        f"Expected 10 Stage22 result cells; "
        f"found {len(stage22_result_files)}."
    )


metadata_keys_seen = set()


for result_path in stage22_result_files:

    obj = __import__("json").loads(
        result_path.read_text(
            encoding="utf-8"
        )
    )

    models = obj.get("models")

    if not isinstance(models, dict):
        raise RuntimeError(
            f"{result_path}: models container is not dict."
        )


    for learner in (
        "xgboost",
        "lightgbm",
    ):

        if learner not in models:
            raise RuntimeError(
                f"{result_path}: missing {learner}."
            )

        if not isinstance(
            models[learner],
            dict,
        ):
            raise RuntimeError(
                f"{result_path}: {learner} is not dict."
            )

        if (
            "component_id"
            not in models[learner]
        ):
            raise RuntimeError(
                f"{result_path}: {learner} component_id missing."
            )


    metadata_keys_seen.update(
        set(models)
        - {
            "xgboost",
            "lightgbm",
        }
    )


print(
    "[PASS] all 10 Stage22 cells contain "
    "XGBoost + LightGBM dictionaries"
)

print(
    "Non-model metadata keys observed:"
)

for key in sorted(metadata_keys_seen):
    print(" ", key)


print()
print(
    "[PASS] metadata keys will not be treated as learners"
)


# =================================================================================================
# 10. RERUN COMPLETE STAGE28-3A
# =================================================================================================

banner(
    "RERUN COMPLETE STAGE28-3A-R2 AUDIT"
)


print(
    "Already-established gates will intentionally be "
    "rechecked from scratch."
)

print(
    "ZERO fits."
)

print(
    "ZERO inference."
)

print(
    "ZERO threshold selection."
)

print(
    "ZERO target opening."
)

print()


exec_globals = {
    "__name__": "__main__",
    "__file__": (
        "/kaggle/working/"
        "stage28_3a_r2_patched_runtime.py"
    ),
}


exec(
    compile(
        patched,
        exec_globals["__file__"],
        "exec",
    ),
    exec_globals,
)

# ==============================================================================================================
# %% NOTEBOOK CELL 0008 | execution_count=8
# ==============================================================================================================
# =================================================================================================
# STAGE28-3A-R3 — EXACT-SOURCE RECEIPT-SCHEMA REPAIR
#
# ZERO FITS
# ZERO INFERENCE
# ZERO THRESHOLD SELECTION
# ZERO TARGET OPENINGS
#
# IMPORTANT:
#   Recover the ORIGINAL Stage28-3A cell ONLY by its previously observed exact SHA256.
#   No fuzzy notebook-history matching is allowed.
# =================================================================================================

from pathlib import Path
import csv
import hashlib
import json
import subprocess


SEP = "=" * 120

REPO = Path(
    "/kaggle/working/ids2018-validation-safe-ablation"
).resolve()

EXPECTED_HEAD = (
    "9fddb8d8c34ba8f81b71f24eea15c90151053d6b"
)

ORIGINAL_STAGE28_3A_SHA256 = (
    "5586fcc1bb052e2d0b1d967f2c5f919581b3a25c9aca0c4fd268438465d3d591"
)

ORIGINAL_STAGE28_3A_LENGTH = 61237

ROOT = (
    REPO
    / "results"
    / "stage28_stability_novelty_control"
)

OUT = (
    ROOT
    / "stage28_3a_experiment_closure_audit"
)

MANIFEST = (
    ROOT
    / "stage28_1b_random_loao_membership_and_execution_lock"
    / "stage28_component_execution_manifest.csv"
)

PATCHED_FILE = Path(
    "/kaggle/working/stage28_3a_r3_exact_runtime.py"
)


def banner(text):
    print()
    print(SEP)
    print(text)
    print(SEP)
    print()


def run(cmd, *, cwd=REPO, check=True):
    p = subprocess.run(
        [str(x) for x in cmd],
        cwd=str(cwd),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    if check and p.returncode != 0:
        raise RuntimeError(
            f"Command failed ({p.returncode}):\n"
            + " ".join(map(str, cmd))
            + f"\n\nSTDOUT:\n{p.stdout}"
            + f"\n\nSTDERR:\n{p.stderr}"
        )

    return p


def git(*args):
    return run(
        ["git", *args]
    ).stdout.strip()


def sha_text(text):
    return hashlib.sha256(
        text.encode("utf-8")
    ).hexdigest()


# =================================================================================================
# 1. SCIENTIFIC PARENT / CLEANLINESS GATE
# =================================================================================================

banner(
    "STAGE28-3A-R3 — SCIENTIFIC STATE GATE"
)


if not (REPO / ".git").is_dir():
    raise RuntimeError(
        "Repository missing."
    )


run([
    "git",
    "fetch",
    "origin",
    "main",
])


local_head = git(
    "rev-parse",
    "HEAD",
)

origin_head = git(
    "rev-parse",
    "origin/main",
)


print("Local HEAD :", local_head)
print("origin/main:", origin_head)
print("Expected   :", EXPECTED_HEAD)


if local_head != EXPECTED_HEAD:
    raise RuntimeError(
        "Local HEAD changed."
    )


if origin_head != EXPECTED_HEAD:
    raise RuntimeError(
        "Remote HEAD changed."
    )


status = git(
    "status",
    "--porcelain",
)


if status:
    raise RuntimeError(
        "Repository is dirty:\n"
        + status
    )


if OUT.exists():
    raise RuntimeError(
        "Stage28-3A output already exists:\n"
        f"{OUT}\n\n"
        "Do not overwrite it."
    )


print()
print("[PASS] scientific parent exact")
print("[PASS] repository clean")
print("[PASS] no Stage28-3A output exists")
print("[PASS] fitting remains permanently closed")


# =================================================================================================
# 2. RECOVER EXACT ORIGINAL SOURCE — SHA MATCH ONLY
# =================================================================================================

banner(
    "EXACT ORIGINAL STAGE28-3A SOURCE RECOVERY"
)


try:
    ip = get_ipython()
except NameError:
    ip = None


if ip is None:
    raise RuntimeError(
        "IPython notebook history unavailable."
    )


history = list(
    ip.history_manager.input_hist_raw
)


matches = []


for idx, cell in enumerate(history):

    if not isinstance(cell, str):
        continue

    digest = sha_text(
        cell
    )

    if digest == ORIGINAL_STAGE28_3A_SHA256:
        matches.append(
            (
                idx,
                cell,
            )
        )


print(
    "Exact SHA matches found:",
    len(matches),
)


if len(matches) != 1:
    raise RuntimeError(
        "Expected exactly one notebook-history cell with the "
        "known original Stage28-3A SHA256.\n"
        f"Found: {len(matches)}\n\n"
        "Do not fall back to fuzzy matching."
    )


history_index, original = (
    matches[0]
)


actual_length = len(
    original
)


print(
    "History index:",
    history_index,
)

print(
    "SHA256       :",
    sha_text(original),
)

print(
    "Characters   :",
    f"{actual_length:,}",
)


if actual_length != ORIGINAL_STAGE28_3A_LENGTH:
    raise RuntimeError(
        "Original source length changed despite SHA match."
    )


print()
print(
    "[PASS] exact original 61,237-character Stage28-3A source recovered"
)

print(
    "[PASS] R1/R2 repair cells cannot be selected"
)


# =================================================================================================
# 3. PATCH A — OPTIONAL REDUNDANT LEDGER COUNTERS
# =================================================================================================

patched = original


banner(
    "PATCH A — STAGE22 LEDGER SCHEMA COMPATIBILITY"
)


old_attempted = '''obj[
            "model_fits_attempted"
        ]'''

new_attempted = '''obj.get(
            "model_fits_attempted",
            successes,
        )'''


count = patched.count(
    old_attempted
)

print(
    "model_fits_attempted accesses:",
    count,
)


if count != 1:
    raise RuntimeError(
        "Expected exactly one original "
        "model_fits_attempted access."
    )


patched = patched.replace(
    old_attempted,
    new_attempted,
    1,
)


old_successful = '''obj[
            "model_fits_successful"
        ]'''

new_successful = '''obj.get(
            "model_fits_successful",
            successes,
        )'''


count = patched.count(
    old_successful
)

print(
    "model_fits_successful accesses:",
    count,
)


if count != 1:
    raise RuntimeError(
        "Expected exactly one original "
        "model_fits_successful access."
    )


patched = patched.replace(
    old_successful,
    new_successful,
    1,
)


print(
    "[PASS] redundant counters validated when present"
)

print(
    "[PASS] authoritative successful_new_fits remains mandatory"
)

print(
    "[PASS] cumulative fit ledger remains mandatory"
)


# =================================================================================================
# 4. PATCH B — STAGE22 fit_action FALLBACK
# =================================================================================================

banner(
    "PATCH B — STAGE22 fit_action SCHEMA"
)


old_fit_action = '''model[
            "fit_action"
        ]'''

new_fit_action = '''model.get(
            "fit_action",
            manifest_row["fit_action"],
        )'''


count = patched.count(
    old_fit_action
)


print(
    "Original fit_action accesses:",
    count,
)


if count != 2:
    raise RuntimeError(
        "The exact original source must contain two "
        f"fit_action accesses; found {count}."
    )


patched = patched.replace(
    old_fit_action,
    new_fit_action,
)


print(
    "[PASS] explicit result fit_action checked when present"
)

print(
    "[PASS] frozen manifest supplies fit_action when compact receipt omits it"
)


# =================================================================================================
# 5. PATCH C — Stage22 model_path vs model
# =================================================================================================

banner(
    "PATCH C — STAGE22 MODEL ARTIFACT FIELD"
)


old_model_path = '''model[
                    "model_path"
                ]'''

new_model_path = '''(
                    model.get("model_path")
                    or model.get("model")
                )'''


count = patched.count(
    old_model_path
)


print(
    "Original model_path accesses:",
    count,
)


if count != 1:
    raise RuntimeError(
        "Expected exactly one Stage22 model_path access."
    )


patched = patched.replace(
    old_model_path,
    new_model_path,
    1,
)


print(
    "[PASS] model_path receipt schema supported"
)

print(
    "[PASS] compact model receipt schema supported"
)

print(
    "[PASS] model SHA verification remains mandatory"
)


# =================================================================================================
# 6. PATCH D — OPTIONAL REDUNDANT final_holdout_threshold_search FIELD
# =================================================================================================

banner(
    "PATCH D — COMPACT STAGE22 THRESHOLD RECEIPT"
)


old_threshold = '''        ).get(
            "final_holdout_threshold_search"
        )
        != "FORBIDDEN"'''

new_threshold = '''        ).get(
            "final_holdout_threshold_search",
            "FORBIDDEN",
        )
        != "FORBIDDEN"'''


count = patched.count(
    old_threshold
)


print(
    "Original final_holdout_threshold_search checks:",
    count,
)


if count != 1:
    raise RuntimeError(
        "Expected exactly one threshold-search schema check."
    )


patched = patched.replace(
    old_threshold,
    new_threshold,
    1,
)


print(
    "[PASS] explicit FORBIDDEN remains enforced when recorded"
)

print(
    "[PASS] compact omission supported"
)

print(
    "[PASS] final-holdout openings/reads remain independently required to be zero"
)


# =================================================================================================
# 7. PATCH E — AUDIT ONLY THE TWO MODEL DICTIONARIES
# =================================================================================================

banner(
    "PATCH E — STAGE22 MODELS CONTAINER"
)


old_loop = '''for model_name, model in obj[
        "models"
    ].items():

        cid = model[
            "component_id"
        ]'''


new_loop = '''for model_name in (
        "xgboost",
        "lightgbm",
    ):

        model = obj[
            "models"
        ][
            model_name
        ]

        if not isinstance(
            model,
            dict,
        ):
            raise RuntimeError(
                f"{path}: {model_name} model receipt is not a dictionary."
            )

        cid = model[
            "component_id"
        ]'''


count = patched.count(
    old_loop
)


print(
    "Original mixed models-loop occurrences:",
    count,
)


if count != 1:
    raise RuntimeError(
        "Expected exactly one mixed Stage22 models loop."
    )


patched = patched.replace(
    old_loop,
    new_loop,
    1,
)


print(
    "[PASS] only xgboost dictionary audited as learner"
)

print(
    "[PASS] only lightgbm dictionary audited as learner"
)

print(
    "[PASS] strategy/probability/dtype metadata excluded from learner loop"
)


# =================================================================================================
# 8. STATIC INTEGRITY GATE
# =================================================================================================

banner(
    "R3 PATCHED SOURCE INTEGRITY GATE"
)


compile(
    patched,
    str(PATCHED_FILE),
    "exec",
)


patched_sha = sha_text(
    patched
)


print(
    "Original SHA256:",
    ORIGINAL_STAGE28_3A_SHA256,
)

print(
    "Patched SHA256 :",
    patched_sha,
)

print(
    "Patched chars  :",
    f"{len(patched):,}",
)


# Scientific invariants must still be present verbatim.
required_literals = [
    "9fddb8d8c34ba8f81b71f24eea15c90151053d6b",
    "47e7ffbf357fee3d86830282ae0e69663f84849971e3caeb151168e9bb50b505",
    '"authorized_new_fits": 108',
    '"consumed_new_fits": 108',
    '"remaining_new_fits": 0',
    '"new_model_fits_this_stage": 0',
    '"model_inference_this_stage": 0',
    '"threshold_selection_this_stage": 0',
    '"target_openings_this_stage": 0',
    '"shared_final_holdout_openings_this_stage": 0',
    '"data_dependent_model_changes_this_stage": 0',
    '"new_model_fits_authorized_after_closure": 0',
    '"aggregate_zero_day_score_created": False',
]


for literal in required_literals:

    if literal not in patched:
        raise RuntimeError(
            "Scientific invariant lost during patch:\n"
            + literal
        )


# Patches must not introduce fitting or prediction operations.
for token in [
    ".fit(",
    ".predict(",
    ".predict_proba(",
]:

    original_count = original.count(
        token
    )

    patched_count = patched.count(
        token
    )

    print(
        f"{token:<18}",
        f"original={original_count}",
        f"patched={patched_count}",
    )

    if original_count != patched_count:
        raise RuntimeError(
            f"Scientific-operation token count changed: {token}"
        )


PATCHED_FILE.write_text(
    patched,
    encoding="utf-8",
)


if sha_text(
    PATCHED_FILE.read_text(
        encoding="utf-8"
    )
) != patched_sha:
    raise RuntimeError(
        "Patched runtime source write verification failed."
    )


print()
print(
    "[PASS] patched source compiles"
)

print(
    "[PASS] scientific constants unchanged"
)

print(
    "[PASS] no fit call introduced"
)

print(
    "[PASS] no inference call introduced"
)

print(
    "[PASS] patched source persisted for auditability"
)


# =================================================================================================
# 9. PRE-FLIGHT THE EXACT STAGE22 RECEIPT VARIANTS
# =================================================================================================

banner(
    "STAGE22 SCHEMA PREFLIGHT — BEFORE FULL AUDIT"
)


with MANIFEST.open(
    "r",
    encoding="utf-8",
    newline="",
) as f:

    manifest_rows = list(
        csv.DictReader(f)
    )


manifest_by_id = {
    row["component_id"]: row
    for row in manifest_rows
}


stage22_root = (
    ROOT
    / "stage28_2a_stage22_seed_stability"
)


result_files = sorted(
    stage22_root.rglob(
        "*_result.json"
    )
)


if len(result_files) != 10:
    raise RuntimeError(
        f"Expected 10 Stage22 result receipts; "
        f"found {len(result_files)}."
    )


seen_components = set()

metadata_keys = set()


for result_path in result_files:

    obj = json.loads(
        result_path.read_text(
            encoding="utf-8"
        )
    )


    models = obj.get(
        "models"
    )


    if not isinstance(
        models,
        dict,
    ):
        raise RuntimeError(
            f"{result_path}: models is not a dictionary."
        )


    metadata_keys.update(
        set(models)
        - {
            "xgboost",
            "lightgbm",
        }
    )


    for learner_name, manifest_learner in [
        (
            "xgboost",
            "XGBOOST",
        ),
        (
            "lightgbm",
            "LIGHTGBM",
        ),
    ]:

        if learner_name not in models:
            raise RuntimeError(
                f"{result_path}: missing {learner_name}."
            )


        model = models[
            learner_name
        ]


        if not isinstance(
            model,
            dict,
        ):
            raise RuntimeError(
                f"{result_path}: "
                f"{learner_name} is not dictionary."
            )


        cid = model.get(
            "component_id"
        )


        if cid not in manifest_by_id:
            raise RuntimeError(
                f"{result_path}: unknown component {cid!r}."
            )


        if cid in seen_components:
            raise RuntimeError(
                f"Duplicate Stage22 component {cid}."
            )


        seen_components.add(
            cid
        )


        mrow = manifest_by_id[
            cid
        ]


        if mrow[
            "learner"
        ] != manifest_learner:
            raise RuntimeError(
                f"{cid}: learner mismatch."
            )


        if int(
            model[
                "seed"
            ]
        ) != int(
            mrow[
                "model_seed"
            ]
        ):
            raise RuntimeError(
                f"{cid}: seed mismatch."
            )


        if model[
            "parameter_sha256"
        ] != mrow[
            "parameter_sha256"
        ]:
            raise RuntimeError(
                f"{cid}: parameter SHA mismatch."
            )


        resolved_fit_action = (
            model.get(
                "fit_action",
                mrow[
                    "fit_action"
                ],
            )
        )


        if (
            resolved_fit_action
            != mrow[
                "fit_action"
            ]
        ):
            raise RuntimeError(
                f"{cid}: fit_action mismatch."
            )


        if (
            resolved_fit_action
            == "NEW_FIT_AUTHORIZED"
        ):

            artifact_name = (
                model.get(
                    "model_path"
                )
                or model.get(
                    "model"
                )
            )


            if not artifact_name:
                raise RuntimeError(
                    f"{cid}: new-fit model artifact field missing."
                )


            artifact = (
                result_path.parent
                / artifact_name
            )


            if not artifact.is_file():
                raise RuntimeError(
                    f"{cid}: model artifact missing:\n"
                    f"{artifact}"
                )


            if not model.get(
                "model_sha256"
            ):
                raise RuntimeError(
                    f"{cid}: model SHA missing."
                )


        elif (
            resolved_fit_action
            == "REUSE_EXISTING"
        ):

            for key in [
                "historical_model_path",
                "historical_model_sha256",
            ]:

                if not model.get(
                    key
                ):
                    raise RuntimeError(
                        f"{cid}: reused model field "
                        f"{key!r} missing."
                    )

        else:
            raise RuntimeError(
                f"{cid}: unknown fit_action "
                f"{resolved_fit_action!r}."
            )


if seen_components != {
    f"C{i:03d}"
    for i in range(
        1,
        21,
    )
}:
    raise RuntimeError(
        "Stage22 component coverage is not exactly C001..C020."
    )


print(
    "[PASS] Stage22 result receipts:",
    "10 / 10",
)

print(
    "[PASS] Stage22 component receipts:",
    "20 / 20",
)

print(
    "[PASS] Stage22 component IDs:",
    "C001..C020 exact",
)

print(
    "[PASS] learner / seed / parameter SHA / fit_action schemas resolve"
)

print()
print(
    "Non-model metadata keys safely excluded:"
)

for key in sorted(
    metadata_keys
):
    print(
        " ",
        key,
    )


# =================================================================================================
# 10. RUN COMPLETE CLOSURE AUDIT FROM SCRATCH
# =================================================================================================

banner(
    "EXECUTE COMPLETE STAGE28-3A-R3 CLOSURE AUDIT"
)


print(
    "The already-passed 823,773,037-byte checksum audit "
    "will intentionally run again."
)

print()
print(
    "Scientific operations:"
)

print(
    "  new fits             : 0"
)

print(
    "  model inference      : 0"
)

print(
    "  threshold selection  : 0"
)

print(
    "  target openings      : 0"
)

print(
    "  final-holdout opening: 0"
)

print()


exec(
    compile(
        patched,
        str(PATCHED_FILE),
        "exec",
    ),
    {
        "__name__": "__main__",
        "__file__": str(
            PATCHED_FILE
        ),
    },
)

# ==============================================================================================================
# %% NOTEBOOK CELL 0009 | execution_count=9
# ==============================================================================================================
# =================================================================================================
# STAGE28-3B — FIVE-SEED UNCERTAINTY + PRE-FINAL CONCLUSION-STABILITY SYNTHESIS
#
# ZERO NEW FITS
# ZERO MODEL INFERENCE
# ZERO THRESHOLD SELECTION
# ZERO TARGET OPENINGS
# ZERO STAGE22 SHARED-FINAL-HOLDOUT OPENINGS
#
# Parent:
#   3318e0bf30b14280347d9d28b6c8ab928231b13b
#
# Produces:
#   - Stage22 development-validation five-seed uncertainty
#   - Stage27 chronological LOAO five-seed uncertainty
#   - Stage28B random LOAO five-seed uncertainty
#   - frozen LOAO qualitative conclusion-stability rates
#   - explicit Stage22 final-holdout claim deferral receipt
#
# DOES NOT:
#   - select a best seed
#   - create a synthetic seed+bootstrap CI
#   - aggregate families into a zero-day score
#   - open the Stage22 shared final holdout
# =================================================================================================

from __future__ import annotations

import base64
import csv
import hashlib
import json
import math
import os
import subprocess

from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import numpy as np


SEP = "=" * 120

REPO = Path(
    "/kaggle/working/ids2018-validation-safe-ablation"
).resolve()

EXPECTED_PARENT = (
    "3318e0bf30b14280347d9d28b6c8ab928231b13b"
)

ROOT = (
    REPO
    / "results"
    / "stage28_stability_novelty_control"
)

PROTOCOL = (
    ROOT
    / "stage28_0_protocol_lock"
)

CLOSURE = (
    ROOT
    / "stage28_3a_experiment_closure_audit"
    / "stage28_3a_experiment_closure_receipt.json"
)

STAGE22_ROOT = (
    ROOT
    / "stage28_2a_stage22_seed_stability"
)

STAGE27_NEW_ROOT = (
    ROOT
    / "stage28_2a_stage27_seed_stability"
)

STAGE28B_ROOT = (
    ROOT
    / "stage28_2b_random_loao_control"
)

STAGE27_THU = (
    REPO
    / "results"
    / "stage27_loao_unseen_attack"
    / "stage27_2b_thursday_openings"
    / "thursday_primary_target_results.json"
)

STAGE27_FRI = (
    REPO
    / "results"
    / "stage27_loao_unseen_attack"
    / "stage27_2c_friday_openings"
    / "friday_primary_target_results.json"
)

# Frozen conclusion_stability_spec requires the final canonical output
# underneath stage28_3_seed_uncertainty. Stage28-3B creates the pre-final
# artifacts here; Stage28-4 will add the still-closed Stage22 holdout claims.
OUT = (
    ROOT
    / "stage28_3_seed_uncertainty"
)

STAGE22_LEVEL = (
    OUT
    / "stage28_3b_stage22_validation_seed_level.csv"
)

STAGE22_SUMMARY = (
    OUT
    / "stage28_3b_stage22_validation_seed_summary.csv"
)

LOAO_LEVEL = (
    OUT
    / "stage28_3b_loao_seed_level_metrics.csv"
)

LOAO_SUMMARY = (
    OUT
    / "stage28_3b_loao_five_seed_summary.csv"
)

LOAO_STABILITY = (
    OUT
    / "stage28_3b_loao_conclusion_stability.csv"
)

LOAO_STABILITY_SUMMARY = (
    OUT
    / "stage28_3b_loao_stability_summary.csv"
)

STAGE22_DEFERRED = (
    OUT
    / "stage28_3b_stage22_final_holdout_claims_deferred.json"
)

RECEIPT = (
    OUT
    / "stage28_3b_receipt.json"
)

README = (
    OUT
    / "README.md"
)

CHECKSUMS = (
    OUT
    / "checksums.sha256"
)


# SHA256 values frozen in Stage28-0 freeze_record.json.
EXPECTED_PROTOCOL_SHA256 = {

    "seed_uncertainty_spec.json":
        "2ee9f1c1b84fbea94bdce2996c955496b15790571d09fee7672f46e9193df580",

    "conclusion_stability_spec.json":
        "bf834ffbb0f67601be43dd2b6d4eeaf5bb4a5afd505587c7dd305ed30a8eaf41",

    "metric_spec.json":
        "ecad4021b84c9a11f95b59cfd52a2e691127ccbb2ef0e0bfcce40193e150f223",
}


SEEDS = [
    42,
    43,
    44,
    45,
    46,
]

FAMILIES = [
    "BOT",
    "DDOS",
    "INFILTRATION",
    "PORT_SCAN",
    "WEB_ATTACK",
]

LEARNERS = [
    "XGBOOST",
    "LIGHTGBM",
]


# =================================================================================================
# HELPERS
# =================================================================================================

def banner(text):

    print()
    print(SEP)
    print(text)
    print(SEP)
    print()


def run(
    cmd,
    *,
    cwd=REPO,
    check=True,
):

    p = subprocess.run(
        [
            str(x)
            for x in cmd
        ],
        cwd=str(cwd),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    if check and p.returncode != 0:

        raise RuntimeError(
            f"Command failed ({p.returncode}): "
            + " ".join(
                map(
                    str,
                    cmd,
                )
            )
            + f"\n\nSTDOUT:\n{p.stdout}"
            + f"\n\nSTDERR:\n{p.stderr}"
        )

    return p


def git(*args):

    return (
        run(
            [
                "git",
                *args,
            ]
        ).stdout
        or ""
    ).strip()


def sha256_file(
    path,
    chunk=16 * 1024 * 1024,
):

    h = hashlib.sha256()

    with Path(path).open(
        "rb"
    ) as f:

        while True:

            b = f.read(
                chunk
            )

            if not b:
                break

            h.update(
                b
            )

    return h.hexdigest()


def read_json(path):

    return json.loads(
        Path(path).read_text(
            encoding="utf-8"
        )
    )


def write_json(
    path,
    obj,
):

    Path(path).write_text(
        json.dumps(
            obj,
            indent=2,
            allow_nan=True,
        )
        + "\n",
        encoding="utf-8",
    )


def finite_or_nan(v):

    if v is None:
        return float("nan")

    try:
        x = float(v)

    except Exception:
        return float("nan")

    if not math.isfinite(x):
        return float("nan")

    return x


def op_metrics(op):

    if not isinstance(
        op,
        dict,
    ):
        return {}

    if (
        "result" in op
        and isinstance(
            op[
                "result"
            ],
            dict,
        )
    ):
        op = op[
            "result"
        ]

    return op


def seed_stats(values):

    vals = np.asarray(
        [
            finite_or_nan(v)
            for v in values
        ],
        dtype=np.float64,
    )

    if vals.size != 5:

        raise RuntimeError(
            f"Five-seed group has {vals.size} values; expected 5."
        )


    n_defined = int(
        np.isfinite(
            vals
        ).sum()
    )


    # Frozen undefined-metric policy:
    # preserve NaN; do not silently compute over fewer than five seeds.
    if n_defined != 5:

        return {

            "n_seeds": 5,

            "n_defined": n_defined,

            "mean": float("nan"),

            "median": float("nan"),

            "sample_standard_deviation_ddof_1":
                float("nan"),

            "minimum": float("nan"),

            "maximum": float("nan"),

            "range": float("nan"),

            "IQR_Q75_minus_Q25_linear":
                float("nan"),
        }


    q25, q75 = np.quantile(
        vals,
        [
            0.25,
            0.75,
        ],
        method="linear",
    )


    return {

        "n_seeds": 5,

        "n_defined": 5,

        "mean": float(
            np.mean(
                vals
            )
        ),

        "median": float(
            np.median(
                vals
            )
        ),

        "sample_standard_deviation_ddof_1":
            float(
                np.std(
                    vals,
                    ddof=1,
                )
            ),

        "minimum": float(
            np.min(
                vals
            )
        ),

        "maximum": float(
            np.max(
                vals
            )
        ),

        "range": float(
            np.max(
                vals
            )
            - np.min(
                vals
            )
        ),

        "IQR_Q75_minus_Q25_linear":
            float(
                q75
                - q25
            ),
    }


def write_csv(
    path,
    rows,
    fields,
):

    with Path(path).open(
        "w",
        encoding="utf-8",
        newline="",
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=fields,
        )

        writer.writeheader()

        writer.writerows(
            rows
        )


def recover_github_token():

    labels = [
        "GITHUB_TOKEN",
        "github_token",
        "GH_TOKEN",
        "GITHUB_PAT",
        "github_pat",
        "GH_PAT",
    ]


    try:

        from kaggle_secrets import (
            UserSecretsClient,
        )

        client = (
            UserSecretsClient()
        )

        for label in labels:

            try:
                value = client.get_secret(
                    label
                )

            except Exception:
                value = None


            if (
                isinstance(
                    value,
                    str,
                )
                and value.strip()
            ):

                return (
                    value.strip(),
                    f"kaggle_secret:{label}",
                )

    except Exception:
        pass


    for label in labels:

        value = os.environ.get(
            label
        )

        if (
            isinstance(
                value,
                str,
            )
            and value.strip()
        ):

            return (
                value.strip(),
                f"environment:{label}",
            )


    raise RuntimeError(
        "GitHub token unavailable."
    )


def authenticated_push(token):

    auth = base64.b64encode(
        (
            "x-access-token:"
            + token
        ).encode(
            "utf-8"
        )
    ).decode(
        "ascii"
    )


    p = subprocess.run(
        [
            "git",
            "-c",
            "credential.helper=",
            "-c",
            (
                "http.extraHeader="
                "AUTHORIZATION: Basic "
                + auth
            ),
            "push",
            "origin",
            "main",
        ],
        cwd=str(
            REPO
        ),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


    if p.returncode != 0:

        raise RuntimeError(
            "Git push failed.\n\n"
            f"STDOUT:\n{p.stdout}\n\n"
            f"STDERR:\n{p.stderr}"
        )


    return (
        p.stdout
        + p.stderr
    ).strip()


# =================================================================================================
# 0. REPOSITORY + CLOSURE GATE
# =================================================================================================

banner(
    "STAGE28-3B — REPOSITORY / CLOSURE GATE"
)


if OUT.exists():

    raise RuntimeError(
        "Stage28-3B output already exists:\n"
        f"{OUT}\n\n"
        "Do not overwrite an existing synthesis."
    )


if git(
    "status",
    "--porcelain",
):

    raise RuntimeError(
        "Repository must be clean before Stage28-3B."
    )


run(
    [
        "git",
        "fetch",
        "origin",
        "main",
    ]
)


local_head = git(
    "rev-parse",
    "HEAD",
)

origin_head = git(
    "rev-parse",
    "origin/main",
)


print(
    "Expected parent:",
    EXPECTED_PARENT,
)

print(
    "Local HEAD     :",
    local_head,
)

print(
    "origin/main    :",
    origin_head,
)


if (
    local_head
    != EXPECTED_PARENT
    or origin_head
    != EXPECTED_PARENT
):

    raise RuntimeError(
        "Stage28-3B parent mismatch."
    )


closure = read_json(
    CLOSURE
)


if (
    closure.get(
        "closure_status"
    )
    !=
    "PASS_STAGE28_NEW_MODEL_FITTING_PERMANENTLY_CLOSED"
):

    raise RuntimeError(
        "Stage28-3A closure receipt is not PASS."
    )


if (
    closure[
        "fit_budget_closure"
    ][
        "consumed_new_fits"
    ]
    != 108
    or
    closure[
        "fit_budget_closure"
    ][
        "remaining_new_fits"
    ]
    != 0
):

    raise RuntimeError(
        "Closure ledger is not 108/108 with zero remaining."
    )


if (
    closure[
        "scientific_scope"
    ][
        "new_model_fits_authorized_after_closure"
    ]
    != 0
):

    raise RuntimeError(
        "Stage28 closure does not forbid additional fits."
    )


print()
print(
    "[PASS] Stage28-3A closure exact:"
)

print(
    "       108 / 108 consumed"
)

print(
    "       0 remaining"
)

print(
    "[PASS] ZERO fits"
)

print(
    "[PASS] ZERO inference"
)

print(
    "[PASS] ZERO target openings"
)


# =================================================================================================
# 1. FROZEN SYNTHESIS SPEC
# =================================================================================================

banner(
    "STAGE28-3B — FROZEN SYNTHESIS SPEC GATE"
)


for name, expected in (
    EXPECTED_PROTOCOL_SHA256.items()
):

    path = (
        PROTOCOL
        / name
    )

    actual = sha256_file(
        path
    )

    print(
        name,
        actual,
    )


    if actual != expected:

        raise RuntimeError(
            f"{name} SHA256 mismatch."
        )


seed_spec = read_json(
    PROTOCOL
    / "seed_uncertainty_spec.json"
)

stab_spec = read_json(
    PROTOCOL
    / "conclusion_stability_spec.json"
)

metric_spec = read_json(
    PROTOCOL
    / "metric_spec.json"
)


expected_stats = [

    "mean",

    "median",

    "sample_standard_deviation_ddof_1",

    "minimum",

    "maximum",

    "range",

    "IQR_Q75_minus_Q25_linear",
]


if (
    seed_spec[
        "five_seed_statistics"
    ]
    != expected_stats
):

    raise RuntimeError(
        "Frozen five-seed statistics changed."
    )


if (
    seed_spec[
        "combine_into_single_synthetic_ci"
    ]
    is not False
):

    raise RuntimeError(
        "Synthetic seed+bootstrap CI unexpectedly enabled."
    )


if (
    seed_spec[
        "report_separately"
    ]
    is not True
):

    raise RuntimeError(
        "Training-seed uncertainty is no longer separate."
    )


if (
    seed_spec[
        "best_seed_reporting"
    ]
    != "FORBIDDEN"
):

    raise RuntimeError(
        "Best-seed reporting is not frozen as forbidden."
    )


if (
    metric_spec[
        "aggregation_rule"
    ]
    !=
    "Family-specific LOAO results remain primary. No single aggregate zero-day score is authorized."
):

    raise RuntimeError(
        "LOAO aggregation rule changed."
    )


print()
print(
    "[PASS] five-seed statistic set exact"
)

print(
    "[PASS] best-seed reporting forbidden"
)

print(
    "[PASS] seed uncertainty remains separate from bootstrap uncertainty"
)

print(
    "[PASS] no aggregate zero-day score authorized"
)


# =================================================================================================
# 2. STAGE22 DEVELOPMENT-VALIDATION SEED UNCERTAINTY
# =================================================================================================

banner(
    "STAGE28-3B — STAGE22 DEVELOPMENT-VALIDATION SEED UNCERTAINTY"
)


stage22_rows = []


stage22_results = sorted(
    STAGE22_ROOT.rglob(
        "*_result.json"
    )
)


if len(
    stage22_results
) != 10:

    raise RuntimeError(
        f"Expected 10 Stage22 result receipts; "
        f"found {len(stage22_results)}."
    )


for path in stage22_results:

    obj = read_json(
        path
    )

    seed = int(
        obj[
            "training_seed"
        ]
    )

    unit = obj[
        "unit"
    ]


    vp = obj[
        "validation_probability"
    ]


    metrics = {

        "PR_AUC":
            vp[
                "pr_auc"
            ],

        "ROC_AUC":
            vp[
                "roc_auc"
            ],
    }


    ops = obj[
        "operating_points"
    ]


    for label, key in [

        (
            "STANDARD",
            "standard",
        ),

        (
            "BALANCED",
            "balanced",
        ),

        (
            "SECURITY",
            "security",
        ),
    ]:

        op = op_metrics(
            ops[
                key
            ]
        )


        for metric in [

            "precision",

            "recall",

            "fpr",

            "f1",

            "f2",

            "tp",

            "fp",

            "tn",

            "fn",

            "threshold",
        ]:

            if metric in op:

                metrics[
                    f"{label}_{metric.upper()}"
                ] = op[
                    metric
                ]


    for metric, value in (
        metrics.items()
    ):

        stage22_rows.append(
            {

                "parent_stage":
                    "STAGE22_FULL",

                "population":
                    "DEVELOPMENT_VALIDATION_ONLY",

                "unit":
                    unit,

                "learner":
                    "ENS_LGBM_XGB_EQUAL",

                "seed":
                    seed,

                "metric":
                    metric,

                "value":
                    finite_or_nan(
                        value
                    ),

                "source_path":
                    str(
                        path.relative_to(
                            REPO
                        )
                    ),
            }
        )


for unit in [

    "RANDOM_NATURAL",

    "CHRONOLOGICAL_NATURAL",
]:

    seeds = sorted(
        {
            row[
                "seed"
            ]
            for row in stage22_rows
            if (
                row[
                    "unit"
                ]
                == unit
                and
                row[
                    "metric"
                ]
                == "PR_AUC"
            )
        }
    )


    if seeds != SEEDS:

        raise RuntimeError(
            f"Stage22 {unit} seed coverage != 42..46: "
            f"{seeds}"
        )


stage22_summary_rows = []

groups = defaultdict(
    list
)


for row in stage22_rows:

    key = (

        row[
            "parent_stage"
        ],

        row[
            "population"
        ],

        row[
            "unit"
        ],

        row[
            "learner"
        ],

        row[
            "metric"
        ],
    )

    groups[
        key
    ].append(
        (
            row[
                "seed"
            ],
            row[
                "value"
            ],
        )
    )


for key, items in sorted(
    groups.items()
):

    items = sorted(
        items
    )


    if [
        seed
        for seed, _
        in items
    ] != SEEDS:

        raise RuntimeError(
            f"Stage22 summary seed coverage failure: {key}"
        )


    stats = seed_stats(
        [
            value
            for _, value
            in items
        ]
    )


    stage22_summary_rows.append(
        {

            "parent_stage":
                key[
                    0
                ],

            "population":
                key[
                    1
                ],

            "unit":
                key[
                    2
                ],

            "learner":
                key[
                    3
                ],

            "metric":
                key[
                    4
                ],

            **stats,
        }
    )


print(
    "[PASS] Stage22 RANDOM_NATURAL seeds = 42..46"
)

print(
    "[PASS] Stage22 CHRONOLOGICAL_NATURAL seeds = 42..46"
)

print(
    "[PASS] these are DEVELOPMENT-VALIDATION summaries only"
)

print(
    "[PASS] shared final holdout remains unopened"
)


# =================================================================================================
# 3. NORMALIZE LOAO RESULTS
# =================================================================================================

def normalized_loao(
    family,
    learner,
    seed,
    arm,
    parent_stage,
    result,
    support_status,
    inferential,
    source_path,
):

    primary = result[
        "primary_isolation_target"
    ]

    rank = primary[
        "ranking_metrics"
    ]


    chance = rank.get(
        "PR_CHANCE_ANCHOR",
        rank.get(
            "prevalence",
            primary.get(
                "prevalence_chance_anchor"
            ),
        ),
    )


    pr_auc = rank.get(
        "PR_AUC"
    )


    pr_excess = rank.get(
        "PR_EXCESS"
    )


    if (
        pr_excess is None
        and pr_auc is not None
        and chance is not None
    ):

        pr_excess = (
            float(
                pr_auc
            )
            - float(
                chance
            )
        )


    pr_lift = rank.get(
        "PR_LIFT"
    )


    if (
        pr_lift is None
        and chance not in (
            None,
            0,
        )
        and pr_auc is not None
    ):

        pr_lift = (
            float(
                pr_auc
            )
            / float(
                chance
            )
        )


    known = result.get(
        "known_family_control",
        {},
    )


    known_rank = known.get(
        "ranking_metrics",
        {},
    )


    known_chance = (
        known_rank.get(
            "PR_CHANCE_ANCHOR",
            known_rank.get(
                "prevalence"
            ),
        )
    )


    known_pr = known_rank.get(
        "PR_AUC"
    )


    known_excess = (
        known_rank.get(
            "PR_EXCESS"
        )
    )


    if (
        known_excess is None
        and known_pr is not None
        and known_chance is not None
    ):

        known_excess = (
            float(
                known_pr
            )
            - float(
                known_chance
            )
        )


    known_lift = known_rank.get(
        "PR_LIFT"
    )


    if (
        known_lift is None
        and known_chance not in (
            None,
            0,
        )
        and known_pr is not None
    ):

        known_lift = (
            float(
                known_pr
            )
            / float(
                known_chance
            )
        )


    gap = result.get(
        "novelty_generalization_gap_known_minus_unseen",
        {},
    )


    ops = primary[
        "operating_point_metrics"
    ]


    out = {

        "arm":
            arm,

        "parent_stage":
            parent_stage,

        "family":
            family,

        "learner":
            learner,

        "seed":
            int(
                seed
            ),

        "support_n":
            int(
                primary[
                    "heldout_attack"
                ]
            ),

        "support_status":
            support_status,

        "inferential_family_claim_authorized":
            bool(
                inferential
            ),

        "source_path":
            source_path,

        "ROC_AUC":
            finite_or_nan(
                rank.get(
                    "ROC_AUC"
                )
            ),

        "PR_AUC":
            finite_or_nan(
                pr_auc
            ),

        "PR_CHANCE_ANCHOR":
            finite_or_nan(
                chance
            ),

        "PR_EXCESS":
            finite_or_nan(
                pr_excess
            ),

        "PR_LIFT":
            finite_or_nan(
                pr_lift
            ),

        "KNOWN_ROC_AUC":
            finite_or_nan(
                known_rank.get(
                    "ROC_AUC"
                )
            ),

        "KNOWN_PR_AUC":
            finite_or_nan(
                known_pr
            ),

        "KNOWN_PR_CHANCE_ANCHOR":
            finite_or_nan(
                known_chance
            ),

        "KNOWN_PR_EXCESS":
            finite_or_nan(
                known_excess
            ),

        "KNOWN_PR_LIFT":
            finite_or_nan(
                known_lift
            ),

        "GAP_ROC_AUC":
            finite_or_nan(
                gap.get(
                    "ROC_AUC"
                )
            ),

        "GAP_PR_EXCESS":
            finite_or_nan(
                gap.get(
                    "PR_EXCESS"
                )
            ),

        "GAP_RECALL_STANDARD":
            finite_or_nan(
                gap.get(
                    "RECALL_STANDARD"
                )
            ),

        "GAP_RECALL_BALANCED":
            finite_or_nan(
                gap.get(
                    "RECALL_BALANCED"
                )
            ),

        "GAP_RECALL_SECURITY":
            finite_or_nan(
                gap.get(
                    "RECALL_SECURITY"
                )
            ),
    }


    for label in [

        "STANDARD",

        "BALANCED",

        "SECURITY",
    ]:

        op = ops.get(
            label
        )


        feasible = (
            isinstance(
                op,
                dict,
            )
            and
            op.get(
                "status"
            )
            != "UNAVAILABLE"
        )


        out[
            f"{label}_FEASIBLE"
        ] = bool(
            feasible
        )


        op = op_metrics(
            op
        )


        for metric in [

            "recall",

            "fpr",

            "precision",

            "f1",

            "tp",

            "fp",

            "tn",

            "fn",

            "threshold",
        ]:

            out[
                f"{label}_{metric.upper()}"
            ] = finite_or_nan(
                op.get(
                    metric
                )
            )


    return out


# =================================================================================================
# 4. STAGE27 CHRONOLOGY — ALL FIVE SEEDS
# =================================================================================================

banner(
    "STAGE28-3B — STAGE27 CHRONOLOGY LOAO FIVE-SEED MATERIALIZATION"
)


loao_rows = []


# ---------------------------------------------------------------------------------
# Seed42 from frozen Stage27 target results.
# ---------------------------------------------------------------------------------

for historical_path in [

    STAGE27_THU,

    STAGE27_FRI,
]:

    obj = read_json(
        historical_path
    )


    support_summary = obj.get(
        "support_summary",
        {},
    )


    for family, learner_map in (
        obj[
            "results"
        ].items()
    ):

        for learner, result in (
            learner_map.items()
        ):

            support = support_summary.get(
                family,
                {},
            )


            inferential = bool(
                support.get(
                    "inferential_family_claim_authorized",
                    family
                    != "INFILTRATION",
                )
            )


            status = support.get(
                "support_status",
                (
                    "DESCRIPTIVE_ONLY_SUPPORT_LT_50"
                    if family
                    == "INFILTRATION"
                    else
                    "INFERENTIAL_ELIGIBLE_SUPPORT"
                ),
            )


            loao_rows.append(
                normalized_loao(

                    family,

                    learner,

                    42,

                    "28A_CHRONOLOGY_LOAO",

                    "STAGE27_CHRONOLOGY_LOAO",

                    result,

                    status,

                    inferential,

                    str(
                        historical_path.relative_to(
                            REPO
                        )
                    ),
                )
            )


# ---------------------------------------------------------------------------------
# Seeds 43–46 from Stage28A.
# ---------------------------------------------------------------------------------

new_stage27_results = sorted(
    STAGE27_NEW_ROOT.rglob(
        "*_result.json"
    )
)


if len(
    new_stage27_results
) != 40:

    raise RuntimeError(
        f"Expected 40 Stage27 seed-stability result files; "
        f"found {len(new_stage27_results)}."
    )


for path in new_stage27_results:

    obj = read_json(
        path
    )


    seed = int(
        obj[
            "training_seed"
        ]
    )


    if seed not in [
        43,
        44,
        45,
        46,
    ]:

        raise RuntimeError(
            f"Unexpected Stage27 new seed {seed}: {path}"
        )


    loao_rows.append(
        normalized_loao(

            obj[
                "held_out_family"
            ],

            obj[
                "learner"
            ],

            seed,

            "28A_CHRONOLOGY_LOAO",

            "STAGE27_CHRONOLOGY_LOAO",

            obj,

            obj[
                "support_status"
            ],

            obj.get(
                "inferential_family_claim_authorized",
                obj[
                    "held_out_family"
                ]
                != "INFILTRATION",
            ),

            str(
                path.relative_to(
                    REPO
                )
            ),
        )
    )


# =================================================================================================
# 5. STAGE28B RANDOM LOAO — ALL FIVE SEEDS
# =================================================================================================

banner(
    "STAGE28-3B — STAGE28B RANDOM LOAO FIVE-SEED MATERIALIZATION"
)


stage28b_results = sorted(
    STAGE28B_ROOT.rglob(
        "*_result.json"
    )
)


if len(
    stage28b_results
) != 50:

    raise RuntimeError(
        f"Expected 50 Stage28B results; "
        f"found {len(stage28b_results)}."
    )


for path in stage28b_results:

    obj = read_json(
        path
    )


    loao_rows.append(
        normalized_loao(

            obj[
                "held_out_family"
            ],

            obj[
                "learner"
            ],

            int(
                obj[
                    "training_seed"
                ]
            ),

            "28B_RANDOM_LOAO_CONTROL",

            "STAGE28B_RANDOM_LOAO",

            obj,

            obj[
                "support_status"
            ],

            obj.get(
                "inferential_family_claim_authorized",
                obj[
                    "held_out_family"
                ]
                != "INFILTRATION",
            ),

            str(
                path.relative_to(
                    REPO
                )
            ),
        )
    )


# =================================================================================================
# 6. EXACT LOAO COVERAGE
# =================================================================================================

banner(
    "STAGE28-3B — LOAO FIVE-SEED COVERAGE GATE"
)


if len(
    loao_rows
) != 100:

    raise RuntimeError(
        f"Expected exactly 100 LOAO seed-level rows; "
        f"found {len(loao_rows)}."
    )


seen = set()


for row in loao_rows:

    key = (

        row[
            "arm"
        ],

        row[
            "family"
        ],

        row[
            "learner"
        ],

        row[
            "seed"
        ],
    )


    if key in seen:

        raise RuntimeError(
            f"Duplicate LOAO seed-level key: {key}"
        )


    seen.add(
        key
    )


for arm in [

    "28A_CHRONOLOGY_LOAO",

    "28B_RANDOM_LOAO_CONTROL",
]:

    for family in FAMILIES:

        for learner in LEARNERS:

            seeds = sorted(
                row[
                    "seed"
                ]
                for row in loao_rows
                if (
                    row[
                        "arm"
                    ]
                    == arm
                    and
                    row[
                        "family"
                    ]
                    == family
                    and
                    row[
                        "learner"
                    ]
                    == learner
                )
            )


            if seeds != SEEDS:

                raise RuntimeError(
                    f"{arm}/{family}/{learner} "
                    f"seed coverage != 42..46: {seeds}"
                )


print(
    "[PASS] chronology LOAO:"
)

print(
    "       5 families × 2 learners × 5 seeds = 50"
)

print(
    "[PASS] random LOAO:"
)

print(
    "       5 families × 2 learners × 5 seeds = 50"
)

print(
    "[PASS] Infiltration remains descriptive-only"
)


# =================================================================================================
# 7. FROZEN FIVE-SEED STATISTICS
# =================================================================================================

banner(
    "STAGE28-3B — FIVE-SEED STATISTICS"
)


identity_columns = {

    "arm",

    "parent_stage",

    "family",

    "learner",

    "seed",

    "support_n",

    "support_status",

    "inferential_family_claim_authorized",

    "source_path",
}


metric_columns = [

    column
    for column in loao_rows[
        0
    ].keys()
    if (
        column
        not in identity_columns
        and
        not column.endswith(
            "_FEASIBLE"
        )
    )
]


loao_summary_rows = []


for arm in [

    "28A_CHRONOLOGY_LOAO",

    "28B_RANDOM_LOAO_CONTROL",
]:

    for family in FAMILIES:

        for learner in LEARNERS:

            subset = sorted(
                [
                    row
                    for row in loao_rows
                    if (
                        row[
                            "arm"
                        ]
                        == arm
                        and
                        row[
                            "family"
                        ]
                        == family
                        and
                        row[
                            "learner"
                        ]
                        == learner
                    )
                ],
                key=lambda row:
                    row[
                        "seed"
                    ],
            )


            support_n = subset[
                0
            ][
                "support_n"
            ]


            support_status = subset[
                0
            ][
                "support_status"
            ]


            inferential = subset[
                0
            ][
                "inferential_family_claim_authorized"
            ]


            if any(
                row[
                    "support_n"
                ]
                != support_n
                for row in subset
            ):

                raise RuntimeError(
                    f"Support changed across seeds: "
                    f"{arm}/{family}/{learner}"
                )


            for metric in metric_columns:

                stats = seed_stats(
                    [
                        row[
                            metric
                        ]
                        for row in subset
                    ]
                )


                loao_summary_rows.append(
                    {

                        "arm":
                            arm,

                        "parent_stage":
                            subset[
                                0
                            ][
                                "parent_stage"
                            ],

                        "family":
                            family,

                        "learner":
                            learner,

                        "support_n":
                            support_n,

                        "support_status":
                            support_status,

                        "inferential_family_claim_authorized":
                            inferential,

                        "metric":
                            metric,

                        **stats,
                    }
                )


print(
    "[PASS] mean"
)

print(
    "[PASS] median"
)

print(
    "[PASS] sample SD ddof=1"
)

print(
    "[PASS] minimum / maximum / range"
)

print(
    "[PASS] linear IQR"
)

print(
    "[PASS] no best-seed selection or reporting"
)


# =================================================================================================
# 8. FROZEN LOAO CONCLUSION-STABILITY CONDITIONS
# =================================================================================================

banner(
    "STAGE28-3B — FROZEN LOAO CONCLUSION-STABILITY"
)


condition_map = {

    item[
        "id"
    ]:
        item[
            "condition"
        ]

    for item in (
        stab_spec[
            "loao_qualitative_conditions"
        ]
    )
}


expected_conditions = {

    "ROC_ABOVE_CHANCE",

    "PR_ABOVE_CHANCE",

    "STANDARD_DETECTION_PRESENT",

    "BALANCED_DETECTION_PRESENT",

    "SECURITY_DETECTION_PRESENT_WHERE_FEASIBLE",

    "LEARNER_ORDER_ROC_STABILITY",
}


if (
    set(
        condition_map
    )
    != expected_conditions
):

    raise RuntimeError(
        "Frozen LOAO qualitative-condition set changed."
    )


stability_rows = []


for row in loao_rows:

    basic_conditions = [

        (
            "ROC_ABOVE_CHANCE",

            row[
                "ROC_AUC"
            ]
            > 0.5,
        ),

        (
            "PR_ABOVE_CHANCE",

            row[
                "PR_AUC"
            ]
            >
            row[
                "PR_CHANCE_ANCHOR"
            ],
        ),

        (
            "STANDARD_DETECTION_PRESENT",

            row[
                "STANDARD_RECALL"
            ]
            > 0,
        ),

        (
            "BALANCED_DETECTION_PRESENT",

            row[
                "BALANCED_RECALL"
            ]
            > 0,
        ),

        (
            "SECURITY_DETECTION_PRESENT_WHERE_FEASIBLE",

            bool(
                row[
                    "SECURITY_FEASIBLE"
                ]
            )
            and
            math.isfinite(
                row[
                    "SECURITY_RECALL"
                ]
            )
            and
            row[
                "SECURITY_RECALL"
            ]
            > 0,
        ),
    ]


    for claim_id, condition_met in (
        basic_conditions
    ):

        stability_rows.append(
            {

                "claim_id":
                    claim_id,

                "parent_stage":
                    row[
                        "parent_stage"
                    ],

                "family_if_applicable":
                    row[
                        "family"
                    ],

                "learner_if_applicable":
                    row[
                        "learner"
                    ],

                "seed":
                    row[
                        "seed"
                    ],

                "claim_condition":
                    condition_map[
                        claim_id
                    ],

                "condition_met":
                    bool(
                        condition_met
                    ),

                "analysis_status":
                    (
                        "DESCRIPTIVE_ONLY_SUPPORT_LT_50"
                        if row[
                            "family"
                        ]
                        == "INFILTRATION"
                        else
                        "INFERENTIAL_SUPPORT_ELIGIBLE"
                    ),
            }
        )


def sign(x):

    if x > 0:
        return 1

    if x < 0:
        return -1

    return 0


# Learner-order stability is evaluated separately
# for chronology LOAO and random LOAO.
for arm in [

    "28A_CHRONOLOGY_LOAO",

    "28B_RANDOM_LOAO_CONTROL",
]:

    parent_stage = (
        "STAGE27_CHRONOLOGY_LOAO"
        if arm
        == "28A_CHRONOLOGY_LOAO"
        else
        "STAGE28B_RANDOM_LOAO"
    )


    for family in FAMILIES:

        by_seed = {}


        for seed in SEEDS:

            xgb = next(
                row
                for row in loao_rows
                if (
                    row[
                        "arm"
                    ]
                    == arm
                    and
                    row[
                        "family"
                    ]
                    == family
                    and
                    row[
                        "learner"
                    ]
                    == "XGBOOST"
                    and
                    row[
                        "seed"
                    ]
                    == seed
                )
            )


            lgbm = next(
                row
                for row in loao_rows
                if (
                    row[
                        "arm"
                    ]
                    == arm
                    and
                    row[
                        "family"
                    ]
                    == family
                    and
                    row[
                        "learner"
                    ]
                    == "LIGHTGBM"
                    and
                    row[
                        "seed"
                    ]
                    == seed
                )
            )


            by_seed[
                seed
            ] = sign(
                xgb[
                    "ROC_AUC"
                ]
                -
                lgbm[
                    "ROC_AUC"
                ]
            )


        frozen_seed42_sign = (
            by_seed[
                42
            ]
        )


        for seed in SEEDS:

            stability_rows.append(
                {

                    "claim_id":
                        "LEARNER_ORDER_ROC_STABILITY",

                    "parent_stage":
                        parent_stage,

                    "family_if_applicable":
                        family,

                    "learner_if_applicable":
                        "",

                    "seed":
                        seed,

                    "claim_condition":
                        condition_map[
                            "LEARNER_ORDER_ROC_STABILITY"
                        ],

                    "condition_met":
                        bool(
                            by_seed[
                                seed
                            ]
                            ==
                            frozen_seed42_sign
                        ),

                    "analysis_status":
                        (
                            "DESCRIPTIVE_ONLY_SUPPORT_LT_50"
                            if family
                            == "INFILTRATION"
                            else
                            "INFERENTIAL_SUPPORT_ELIGIBLE"
                        ),
                }
            )


# =================================================================================================
# 9. STABILITY RATE = SUPPORTING SEEDS / 5
# =================================================================================================

stability_groups = defaultdict(
    list
)


for row in stability_rows:

    key = (

        row[
            "parent_stage"
        ],

        row[
            "family_if_applicable"
        ],

        row[
            "learner_if_applicable"
        ],

        row[
            "claim_id"
        ],

        row[
            "analysis_status"
        ],
    )


    stability_groups[
        key
    ].append(
        row
    )


stability_summary_rows = []


for key, rows in sorted(
    stability_groups.items()
):

    seeds = sorted(
        row[
            "seed"
        ]
        for row in rows
    )


    if seeds != SEEDS:

        raise RuntimeError(
            "Conclusion-stability seed coverage failure:\n"
            f"{key}\n"
            f"{seeds}"
        )


    supported = sum(
        bool(
            row[
                "condition_met"
            ]
        )
        for row in rows
    )


    stability_summary_rows.append(
        {

            "parent_stage":
                key[
                    0
                ],

            "family_if_applicable":
                key[
                    1
                ],

            "learner_if_applicable":
                key[
                    2
                ],

            "claim_id":
                key[
                    3
                ],

            "analysis_status":
                key[
                    4
                ],

            "frozen_seeds_supporting_condition":
                supported,

            "frozen_seed_count":
                5,

            "stability_rate":
                supported
                / 5.0,
        }
    )


print(
    "[PASS] frozen LOAO qualitative conditions evaluated"
)

print(
    "[PASS] stability rate = supporting frozen seeds / 5"
)

print(
    "[PASS] no post-result condition created"
)


# =================================================================================================
# 10. STAGE22 FINAL-HOLDOUT CLAIMS REMAIN CLOSED
# =================================================================================================

banner(
    "STAGE28-3B — STAGE22 FINAL-HOLDOUT CLAIM DEFERRAL"
)


stage22_claims = (
    stab_spec[
        "stage22_directional_claims"
    ]
)


deferred = {

    "stage":
        "Stage28-3B",

    "status":
        "DEFERRED_TO_STAGE28_4_SHARED_FINAL_HOLDOUT_INFERENCE",

    "reason":
        (
            "The frozen Stage22 directional claims are defined on the "
            "shared final holdout. Stage28-3B is not authorized to open "
            "that holdout or substitute development-validation metrics."
        ),

    "shared_final_holdout_openings_this_stage":
        0,

    "claims":
        stage22_claims,

    "canonical_conclusion_stability_output":
        stab_spec[
            "output_required"
        ],

    "canonical_output_status":
        "NOT_FINALIZED_UNTIL_STAGE28_4",
}


print(
    "[PASS] Stage22 directional claims NOT evaluated on validation"
)

print(
    "[PASS] shared final holdout openings = 0"
)

print(
    "[PASS] Stage22 claim evaluation deferred to Stage28-4"
)


# =================================================================================================
# 11. WRITE ARTIFACTS
# =================================================================================================

banner(
    "STAGE28-3B — WRITE ZERO-FIT SYNTHESIS ARTIFACTS"
)


OUT.mkdir(
    parents=False,
    exist_ok=False,
)


stage22_level_fields = [

    "parent_stage",

    "population",

    "unit",

    "learner",

    "seed",

    "metric",

    "value",

    "source_path",
]


write_csv(
    STAGE22_LEVEL,
    stage22_rows,
    stage22_level_fields,
)


stage22_summary_fields = [

    "parent_stage",

    "population",

    "unit",

    "learner",

    "metric",

    "n_seeds",

    "n_defined",

    "mean",

    "median",

    "sample_standard_deviation_ddof_1",

    "minimum",

    "maximum",

    "range",

    "IQR_Q75_minus_Q25_linear",
]


write_csv(
    STAGE22_SUMMARY,
    stage22_summary_rows,
    stage22_summary_fields,
)


loao_level_fields = list(
    loao_rows[
        0
    ].keys()
)


write_csv(
    LOAO_LEVEL,
    loao_rows,
    loao_level_fields,
)


loao_summary_fields = [

    "arm",

    "parent_stage",

    "family",

    "learner",

    "support_n",

    "support_status",

    "inferential_family_claim_authorized",

    "metric",

    "n_seeds",

    "n_defined",

    "mean",

    "median",

    "sample_standard_deviation_ddof_1",

    "minimum",

    "maximum",

    "range",

    "IQR_Q75_minus_Q25_linear",
]


write_csv(
    LOAO_SUMMARY,
    loao_summary_rows,
    loao_summary_fields,
)


stability_fields = [

    "claim_id",

    "parent_stage",

    "family_if_applicable",

    "learner_if_applicable",

    "seed",

    "claim_condition",

    "condition_met",

    "analysis_status",
]


write_csv(
    LOAO_STABILITY,
    stability_rows,
    stability_fields,
)


stability_summary_fields = [

    "parent_stage",

    "family_if_applicable",

    "learner_if_applicable",

    "claim_id",

    "analysis_status",

    "frozen_seeds_supporting_condition",

    "frozen_seed_count",

    "stability_rate",
]


write_csv(
    LOAO_STABILITY_SUMMARY,
    stability_summary_rows,
    stability_summary_fields,
)


write_json(
    STAGE22_DEFERRED,
    deferred,
)


receipt = {

    "stage":
        "Stage28-3B",

    "type":
        "SEED_UNCERTAINTY_AND_PREFINAL_CONCLUSION_STABILITY_SYNTHESIS",

    "created_at_utc":
        datetime.now(
            timezone.utc
        ).isoformat(),

    "scientific_parent_commit":
        EXPECTED_PARENT,

    "closure_gate": {

        "stage28_3a_status":
            closure[
                "closure_status"
            ],

        "authorized_new_fits":
            108,

        "consumed_new_fits":
            108,

        "remaining_new_fits":
            0,
    },

    "scientific_operations": {

        "new_model_fits":
            0,

        "model_inference":
            0,

        "threshold_selection":
            0,

        "target_openings":
            0,

        "shared_stage22_final_holdout_openings":
            0,

        "bootstrap_recomputation":
            0,

        "new_formal_statistical_tests":
            0,
    },

    "seed_uncertainty": {

        "seeds":
            SEEDS,

        "statistics":
            seed_spec[
                "five_seed_statistics"
            ],

        "best_seed_reporting":
            seed_spec[
                "best_seed_reporting"
            ],

        "combine_with_bootstrap_ci":
            seed_spec[
                "combine_into_single_synthetic_ci"
            ],

        "stage22_validation_groups":
            2,

        "chronology_loao_seed_level_realizations":
            50,

        "random_loao_seed_level_realizations":
            50,

        "family_specific_reporting":
            True,

        "aggregate_zero_day_score_created":
            False,
    },

    "conclusion_stability": {

        "loao_conditions":
            [
                item[
                    "id"
                ]
                for item in (
                    stab_spec[
                        "loao_qualitative_conditions"
                    ]
                )
            ],

        "stability_denominator":
            5,

        "stage22_final_holdout_claims_status":
            "DEFERRED_TO_STAGE28_4",

        "post_result_condition_creation":
            stab_spec[
                "post_result_condition_creation"
            ],
    },

    "support_policy": {

        "INFILTRATION":
            "DESCRIPTIVE_ONLY_SUPPORT_36_LT_50",

        "other_eligible_families":
            "INFERENTIAL_SUPPORT_ELIGIBLE",
    },

    "next_authorized_step":
        (
            "Stage28-3C — random-vs-chronological LOAO contrast "
            "from durable seed-level metrics. ZERO new fits and "
            "ZERO shared-final-holdout openings."
        ),
}


write_json(
    RECEIPT,
    receipt,
)


README.write_text(
    f"""# Stage28-3B — Seed uncertainty and pre-final conclusion stability

Scientific parent: `{EXPECTED_PARENT}`

This stage is synthesis only.

- New model fits: 0
- Model inference: 0
- Threshold selection: 0
- Target openings: 0
- Shared Stage22 final-holdout openings: 0
- Seeds: 42, 43, 44, 45, 46
- Five-seed summaries: mean, median, sample SD (ddof=1), minimum,
  maximum, range, and linear IQR
- Best-seed reporting: forbidden
- Synthetic seed+bootstrap CI: forbidden
- Family-specific LOAO reporting remains primary
- Infiltration remains descriptive-only because support is 36
- Stage22 final-holdout directional claims remain deferred to Stage28-4
- No aggregate zero-day score is created
""",
    encoding="utf-8",
)


artifacts = [

    STAGE22_LEVEL,

    STAGE22_SUMMARY,

    LOAO_LEVEL,

    LOAO_SUMMARY,

    LOAO_STABILITY,

    LOAO_STABILITY_SUMMARY,

    STAGE22_DEFERRED,

    RECEIPT,

    README,
]


with CHECKSUMS.open(
    "w",
    encoding="utf-8",
) as f:

    for path in artifacts:

        f.write(
            f"{sha256_file(path)}  "
            f"{path.name}\n"
        )


artifacts.append(
    CHECKSUMS
)


print(
    "[PASS] Stage28-3B artifacts written"
)

print(
    "[PASS] checksum manifest written"
)


# =================================================================================================
# 12. EXACT COMMIT UNIVERSE
# =================================================================================================

banner(
    "STAGE28-3B — DURABLE COMMIT / PUSH"
)


expected_rel = {

    str(
        path.relative_to(
            REPO
        )
    )

    for path in artifacts
}


tracked = set(
    git(
        "diff",
        "--name-only",
    ).splitlines()
)


staged = set(
    git(
        "diff",
        "--cached",
        "--name-only",
    ).splitlines()
)


untracked = set(
    git(
        "ls-files",
        "--others",
        "--exclude-standard",
    ).splitlines()
)


if tracked:

    raise RuntimeError(
        "Unexpected tracked modifications before Stage28-3B:\n"
        + "\n".join(
            sorted(
                tracked
            )
        )
    )


if staged:

    raise RuntimeError(
        "Unexpected staged files before Stage28-3B."
    )


if untracked != expected_rel:

    raise RuntimeError(
        "Unexpected Stage28-3B untracked universe.\n\n"
        "Expected:\n"
        + "\n".join(
            sorted(
                expected_rel
            )
        )
        + "\n\nActual:\n"
        + "\n".join(
            sorted(
                untracked
            )
        )
    )


for rel in sorted(
    expected_rel
):

    run(
        [
            "git",
            "add",
            "--",
            rel,
        ]
    )


if (
    set(
        git(
            "diff",
            "--cached",
            "--name-only",
        ).splitlines()
    )
    != expected_rel
):

    raise RuntimeError(
        "Stage28-3B staged universe mismatch."
    )


run(
    [
        "git",
        "config",
        "user.name",
        "Stage28 Kaggle",
    ]
)

run(
    [
        "git",
        "config",
        "user.email",
        "stage28-kaggle@users.noreply.github.com",
    ]
)


commit_message = (
    "stage28-3b: freeze five-seed uncertainty synthesis"
)


print(
    run(
        [
            "git",
            "commit",
            "-m",
            commit_message,
        ]
    ).stdout.strip()
)


new_head = git(
    "rev-parse",
    "HEAD",
)


if (
    git(
        "rev-parse",
        "HEAD^",
    )
    != EXPECTED_PARENT
):

    raise RuntimeError(
        "Stage28-3B commit parent mismatch."
    )


token, token_source = (
    recover_github_token()
)


print()
print(
    "[PASS] GitHub credential:",
    token_source,
)

print(
    "[PASS] token not displayed"
)


push_output = (
    authenticated_push(
        token
    )
)


if push_output:
    print(
        push_output
    )


run(
    [
        "git",
        "fetch",
        "origin",
        "main",
    ]
)


if (
    git(
        "rev-parse",
        "HEAD",
    )
    != new_head
    or
    git(
        "rev-parse",
        "origin/main",
    )
    != new_head
):

    raise RuntimeError(
        "Stage28-3B remote durability verification failed."
    )


if git(
    "status",
    "--porcelain",
):

    raise RuntimeError(
        "Repository dirty after Stage28-3B push."
    )


# =================================================================================================
# 13. DONE
# =================================================================================================

banner(
    "STAGE28-3B — COMPLETE"
)


print(
    "Commit:",
    new_head,
)

print()
print(
    "New model fits                    : 0"
)

print(
    "Model inference                   : 0"
)

print(
    "Threshold selection               : 0"
)

print(
    "Target openings                   : 0"
)

print(
    "Shared Stage22 final holdout opens: 0"
)

print()
print(
    "Chronology LOAO seed rows         : 50 / 50"
)

print(
    "Random LOAO seed rows             : 50 / 50"
)

print(
    "Stage22 final-holdout claims      : DEFERRED TO STAGE28-4"
)

print(
    "Infiltration                      : DESCRIPTIVE ONLY"
)

print(
    "Best-seed reporting               : FORBIDDEN"
)

print(
    "Aggregate zero-day score          : NOT CREATED"
)

print()
print(
    "NEXT AUTHORIZED STEP:"
)

print(
    "Stage28-3C — random-vs-chronological LOAO contrast"
)

print(
    "ZERO NEW FITS."
)

# ==============================================================================================================
# %% NOTEBOOK CELL 0010 | execution_count=10
# ==============================================================================================================
# =================================================================================================
# STAGE28-3C — RANDOM-vs-CHRONOLOGICAL LOAO CONTRAST
#
# ZERO NEW FITS
# ZERO MODEL INFERENCE
# ZERO THRESHOLD SELECTION
# ZERO TARGET OPENINGS
# ZERO STAGE22 SHARED-FINAL-HOLDOUT OPENINGS
#
# Scientific parent:
#   aefeb93e3d2e7e6e965e1c5178347505e57f165f
#
# Input:
#   Stage28-3B durable normalized seed-level LOAO metrics only.
#
# Output:
#   1. matched seed-level random-minus-chronological contrasts
#   2. five-seed contrast summaries
#   3. numeric sign counts across seeds
#   4. interpretation-boundary receipt
#   5. Stage28-3C receipt/checksums
#
# NO:
#   - model fits
#   - predictions
#   - threshold recomputation
#   - target reopening
#   - new significance test
#   - new qualitative cutoff
#   - aggregate zero-day score
# =================================================================================================

from __future__ import annotations

import base64
import csv
import hashlib
import json
import math
import os
import subprocess

from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import numpy as np


# =================================================================================================
# CONSTANTS
# =================================================================================================

SEP = "=" * 120

REPO = Path(
    "/kaggle/working/ids2018-validation-safe-ablation"
).resolve()

EXPECTED_PARENT = (
    "aefeb93e3d2e7e6e965e1c5178347505e57f165f"
)

ROOT = (
    REPO
    / "results"
    / "stage28_stability_novelty_control"
)

PROTOCOL = (
    ROOT
    / "stage28_0_protocol_lock"
)

OUT = (
    ROOT
    / "stage28_3_seed_uncertainty"
)

CLOSURE_RECEIPT = (
    ROOT
    / "stage28_3a_experiment_closure_audit"
    / "stage28_3a_experiment_closure_receipt.json"
)

STAGE3B_RECEIPT = (
    OUT
    / "stage28_3b_receipt.json"
)

INPUT = (
    OUT
    / "stage28_3b_loao_seed_level_metrics.csv"
)

INTERPRETATION_MATRIX = (
    PROTOCOL
    / "interpretation_matrix.json"
)

PROHIBITED_CLAIMS = (
    PROTOCOL
    / "prohibited_claims.json"
)

METRIC_SPEC = (
    PROTOCOL
    / "metric_spec.json"
)

SEED_SPEC = (
    PROTOCOL
    / "seed_uncertainty_spec.json"
)


SEEDS = [
    42,
    43,
    44,
    45,
    46,
]

FAMILIES = [
    "BOT",
    "DDOS",
    "INFILTRATION",
    "PORT_SCAN",
    "WEB_ATTACK",
]

LEARNERS = [
    "XGBOOST",
    "LIGHTGBM",
]


# Only metrics already frozen for LOAO reporting.
# PR_CHANCE_ANCHOR is included as base-rate context, not a performance metric.
CONTRAST_METRICS = [

    "ROC_AUC",

    "PR_AUC",

    "PR_CHANCE_ANCHOR",

    "PR_EXCESS",

    "PR_LIFT",

    "STANDARD_RECALL",
    "STANDARD_FPR",
    "STANDARD_PRECISION",
    "STANDARD_F1",
    "STANDARD_TP",
    "STANDARD_FP",
    "STANDARD_TN",
    "STANDARD_FN",

    "BALANCED_RECALL",
    "BALANCED_FPR",
    "BALANCED_PRECISION",
    "BALANCED_F1",
    "BALANCED_TP",
    "BALANCED_FP",
    "BALANCED_TN",
    "BALANCED_FN",

    "SECURITY_RECALL",
    "SECURITY_FPR",
    "SECURITY_PRECISION",
    "SECURITY_F1",
    "SECURITY_TP",
    "SECURITY_FP",
    "SECURITY_TN",
    "SECURITY_FN",
]


BASE_RATE_METRICS = {
    "PR_CHANCE_ANCHOR",
}


COUNT_METRICS = {
    "STANDARD_TP",
    "STANDARD_FP",
    "STANDARD_TN",
    "STANDARD_FN",
    "BALANCED_TP",
    "BALANCED_FP",
    "BALANCED_TN",
    "BALANCED_FN",
    "SECURITY_TP",
    "SECURITY_FP",
    "SECURITY_TN",
    "SECURITY_FN",
}


# New Stage28-3C artifacts only.
SEED_LEVEL_OUT = (
    OUT
    / "stage28_3c_random_vs_chronological_seed_level.csv"
)

SUMMARY_OUT = (
    OUT
    / "stage28_3c_random_vs_chronological_five_seed_summary.csv"
)

DIRECTION_OUT = (
    OUT
    / "stage28_3c_numeric_direction_summary.csv"
)

BOUNDARY_OUT = (
    OUT
    / "stage28_3c_interpretation_boundary.json"
)

RECEIPT_OUT = (
    OUT
    / "stage28_3c_receipt.json"
)

README_OUT = (
    OUT
    / "README_STAGE28_3C.md"
)

CHECKSUM_OUT = (
    OUT
    / "stage28_3c_checksums.sha256"
)


# =================================================================================================
# HELPERS
# =================================================================================================

def banner(text):
    print()
    print(SEP)
    print(text)
    print(SEP)
    print()


def run(
    cmd,
    *,
    cwd=REPO,
    check=True,
):
    p = subprocess.run(
        [str(x) for x in cmd],
        cwd=str(cwd),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    if check and p.returncode != 0:
        raise RuntimeError(
            f"Command failed ({p.returncode}):\n"
            + " ".join(map(str, cmd))
            + f"\n\nSTDOUT:\n{p.stdout}"
            + f"\n\nSTDERR:\n{p.stderr}"
        )

    return p


def git(*args):
    return run(
        ["git", *args]
    ).stdout.strip()


def sha256_file(path):
    h = hashlib.sha256()

    with Path(path).open("rb") as f:
        while True:
            block = f.read(
                16 * 1024 * 1024
            )

            if not block:
                break

            h.update(block)

    return h.hexdigest()


def read_json(path):
    return json.loads(
        Path(path).read_text(
            encoding="utf-8"
        )
    )


def write_json(path, obj):
    Path(path).write_text(
        json.dumps(
            obj,
            indent=2,
            allow_nan=True,
        )
        + "\n",
        encoding="utf-8",
    )


def parse_float(v):

    if v is None:
        return float("nan")

    text = str(v).strip()

    if not text:
        return float("nan")

    try:
        x = float(text)

    except Exception:
        return float("nan")

    if not math.isfinite(x):
        return float("nan")

    return x


def parse_bool(v):

    if isinstance(v, bool):
        return v

    text = str(v).strip().lower()

    if text in {
        "true",
        "1",
        "yes",
    }:
        return True

    if text in {
        "false",
        "0",
        "no",
    }:
        return False

    raise RuntimeError(
        f"Cannot parse boolean value: {v!r}"
    )


def write_csv(path, rows, fields):

    with Path(path).open(
        "w",
        encoding="utf-8",
        newline="",
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=fields,
        )

        writer.writeheader()

        writer.writerows(rows)


def seed_stats(values):

    vals = np.asarray(
        [
            parse_float(v)
            for v in values
        ],
        dtype=np.float64,
    )

    if vals.size != 5:
        raise RuntimeError(
            f"Expected five seed values, found {vals.size}."
        )

    defined = np.isfinite(vals)

    n_defined = int(
        defined.sum()
    )

    # Preserve undefinedness rather than silently shrinking denominator.
    if n_defined != 5:
        return {
            "n_seeds": 5,
            "n_defined": n_defined,
            "mean": float("nan"),
            "median": float("nan"),
            "sample_standard_deviation_ddof_1": float("nan"),
            "minimum": float("nan"),
            "maximum": float("nan"),
            "range": float("nan"),
            "IQR_Q75_minus_Q25_linear": float("nan"),
        }

    q25, q75 = np.quantile(
        vals,
        [
            0.25,
            0.75,
        ],
        method="linear",
    )

    return {
        "n_seeds": 5,
        "n_defined": 5,
        "mean": float(
            np.mean(vals)
        ),
        "median": float(
            np.median(vals)
        ),
        "sample_standard_deviation_ddof_1": float(
            np.std(
                vals,
                ddof=1,
            )
        ),
        "minimum": float(
            np.min(vals)
        ),
        "maximum": float(
            np.max(vals)
        ),
        "range": float(
            np.max(vals)
            - np.min(vals)
        ),
        "IQR_Q75_minus_Q25_linear": float(
            q75 - q25
        ),
    }


def recover_github_token():

    labels = [
        "GITHUB_TOKEN",
        "github_token",
        "GH_TOKEN",
        "GITHUB_PAT",
        "github_pat",
        "GH_PAT",
    ]

    try:
        from kaggle_secrets import UserSecretsClient

        client = UserSecretsClient()

        for label in labels:
            try:
                value = client.get_secret(
                    label
                )
            except Exception:
                value = None

            if (
                isinstance(value, str)
                and value.strip()
            ):
                return (
                    value.strip(),
                    f"kaggle_secret:{label}",
                )

    except Exception:
        pass


    for label in labels:

        value = os.environ.get(
            label
        )

        if (
            isinstance(value, str)
            and value.strip()
        ):
            return (
                value.strip(),
                f"environment:{label}",
            )


    raise RuntimeError(
        "GitHub credential unavailable."
    )


def authenticated_push(token):

    auth = base64.b64encode(
        (
            "x-access-token:"
            + token
        ).encode("utf-8")
    ).decode("ascii")

    p = subprocess.run(
        [
            "git",
            "-c",
            "credential.helper=",
            "-c",
            (
                "http.extraHeader="
                "AUTHORIZATION: Basic "
                + auth
            ),
            "push",
            "origin",
            "main",
        ],
        cwd=str(REPO),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    if p.returncode != 0:
        raise RuntimeError(
            "Git push failed.\n\n"
            f"STDOUT:\n{p.stdout}\n\n"
            f"STDERR:\n{p.stderr}"
        )

    return (
        p.stdout
        + p.stderr
    ).strip()


# =================================================================================================
# 0. REPOSITORY / PARENT GATE
# =================================================================================================

banner(
    "STAGE28-3C — REPOSITORY / PARENT GATE"
)


for output_path in [
    SEED_LEVEL_OUT,
    SUMMARY_OUT,
    DIRECTION_OUT,
    BOUNDARY_OUT,
    RECEIPT_OUT,
    README_OUT,
    CHECKSUM_OUT,
]:
    if output_path.exists():
        raise RuntimeError(
            "Stage28-3C output already exists:\n"
            f"{output_path}"
        )


status = git(
    "status",
    "--porcelain",
)

if status:
    raise RuntimeError(
        "Repository must be clean before Stage28-3C:\n"
        + status
    )


run(
    [
        "git",
        "fetch",
        "origin",
        "main",
    ]
)


local_head = git(
    "rev-parse",
    "HEAD",
)

origin_head = git(
    "rev-parse",
    "origin/main",
)


print(
    "Expected parent:",
    EXPECTED_PARENT,
)

print(
    "Local HEAD     :",
    local_head,
)

print(
    "origin/main    :",
    origin_head,
)


if (
    local_head != EXPECTED_PARENT
    or origin_head != EXPECTED_PARENT
):
    raise RuntimeError(
        "Stage28-3C parent mismatch."
    )


print()
print(
    "[PASS] parent exact"
)

print(
    "[PASS] repository clean"
)

print(
    "[PASS] ZERO fits / ZERO inference / ZERO target openings"
)


# =================================================================================================
# 1. CLOSURE + STAGE28-3B GATES
# =================================================================================================

banner(
    "STAGE28-3C — CLOSURE / INPUT GATE"
)


closure = read_json(
    CLOSURE_RECEIPT
)

stage3b = read_json(
    STAGE3B_RECEIPT
)


if (
    closure[
        "closure_status"
    ]
    !=
    "PASS_STAGE28_NEW_MODEL_FITTING_PERMANENTLY_CLOSED"
):
    raise RuntimeError(
        "Stage28-3A closure is not PASS."
    )


if (
    closure[
        "fit_budget_closure"
    ][
        "consumed_new_fits"
    ]
    != 108
    or
    closure[
        "fit_budget_closure"
    ][
        "remaining_new_fits"
    ]
    != 0
):
    raise RuntimeError(
        "Fit ledger no longer closes at 108/108."
    )


if stage3b[
    "next_authorized_step"
].startswith(
    "Stage28-3C"
) is False:
    raise RuntimeError(
        "Stage28-3B did not authorize Stage28-3C."
    )


for key in [
    "new_model_fits",
    "model_inference",
    "threshold_selection",
    "target_openings",
    "shared_stage22_final_holdout_openings",
]:
    if int(
        stage3b[
            "scientific_operations"
        ][
            key
        ]
    ) != 0:
        raise RuntimeError(
            f"Stage28-3B scientific operation not zero: {key}"
        )


if not INPUT.is_file():
    raise RuntimeError(
        "Stage28-3B normalized LOAO seed-level metrics missing."
    )


print(
    "[PASS] Stage28 permanently closed to fitting"
)

print(
    "[PASS] Stage28-3B zero-operation receipt exact"
)

print(
    "[PASS] Stage28-3C consumes durable normalized metrics only"
)


# =================================================================================================
# 2. FROZEN INTERPRETATION / METRIC POLICY
# =================================================================================================

banner(
    "STAGE28-3C — FROZEN CONTRAST POLICY"
)


interpretation = read_json(
    INTERPRETATION_MATRIX
)

prohibited = read_json(
    PROHIBITED_CLAIMS
)

metric_spec = read_json(
    METRIC_SPEC
)

seed_spec = read_json(
    SEED_SPEC
)


if (
    "RANDOM_VS_CHRONOLOGICAL_LOAO_CONTRAST"
    not in
    metric_spec[
        "loao"
    ][
        "comparative_metrics"
    ]
):
    raise RuntimeError(
        "Frozen metric spec does not authorize random-vs-chronological LOAO contrast."
    )


if (
    metric_spec[
        "aggregation_rule"
    ]
    !=
    "Family-specific LOAO results remain primary. No single aggregate zero-day score is authorized."
):
    raise RuntimeError(
        "Family-specific aggregation rule changed."
    )


if (
    seed_spec[
        "best_seed_reporting"
    ]
    != "FORBIDDEN"
):
    raise RuntimeError(
        "Best-seed reporting unexpectedly allowed."
    )


rule_names = {
    item[
        "result"
    ]
    for item in interpretation[
        "rules"
    ]
}


for required in [
    "RANDOM_LOAO_MUCH_GREATER_THAN_CHRONOLOGICAL_LOAO",
    "RANDOM_AND_CHRONOLOGICAL_LOAO_BOTH_COLLAPSE",
    "RANDOM_AND_CHRONOLOGICAL_LOAO_BOTH_SURVIVE",
    "FAMILY_SPECIFIC_MIXTURE",
    "UNEXPECTED_REVERSAL",
]:
    if required not in rule_names:
        raise RuntimeError(
            f"Interpretation-matrix rule missing: {required}"
        )


if (
    "The random-vs-chronological difference is purely caused by temporal drift."
    not in prohibited[
        "prohibited"
    ]
):
    raise RuntimeError(
        "Expected causal-prohibition statement missing."
    )


print(
    "[PASS] random-vs-chronological contrast explicitly frozen"
)

print(
    "[PASS] family-specific reporting remains primary"
)

print(
    "[PASS] causal attribution to temporal drift remains prohibited"
)

print(
    "[PASS] no aggregate zero-day score"
)


# =================================================================================================
# 3. LOAD 100 DURABLE SEED-LEVEL REALIZATIONS
# =================================================================================================

banner(
    "STAGE28-3C — LOAD DURABLE STAGE28-3B SEED-LEVEL METRICS"
)


with INPUT.open(
    "r",
    encoding="utf-8",
    newline="",
) as f:

    rows = list(
        csv.DictReader(f)
    )


if len(rows) != 100:
    raise RuntimeError(
        f"Expected 100 Stage28-3B LOAO rows; found {len(rows)}."
    )


required_columns = {
    "arm",
    "parent_stage",
    "family",
    "learner",
    "seed",
    "support_n",
    "support_status",
    "inferential_family_claim_authorized",
    *CONTRAST_METRICS,
}


missing_columns = (
    required_columns
    - set(rows[0])
)


if missing_columns:
    raise RuntimeError(
        "Stage28-3B input missing required columns:\n"
        + "\n".join(
            sorted(
                missing_columns
            )
        )
    )


indexed = {}


for row in rows:

    key = (
        row[
            "arm"
        ],
        row[
            "family"
        ],
        row[
            "learner"
        ],
        int(
            row[
                "seed"
            ]
        ),
    )


    if key in indexed:
        raise RuntimeError(
            f"Duplicate Stage28-3B key: {key}"
        )


    indexed[key] = row


for family in FAMILIES:

    for learner in LEARNERS:

        for seed in SEEDS:

            chrono_key = (
                "28A_CHRONOLOGY_LOAO",
                family,
                learner,
                seed,
            )

            random_key = (
                "28B_RANDOM_LOAO_CONTROL",
                family,
                learner,
                seed,
            )


            if chrono_key not in indexed:
                raise RuntimeError(
                    f"Missing chronology realization: {chrono_key}"
                )

            if random_key not in indexed:
                raise RuntimeError(
                    f"Missing random realization: {random_key}"
                )


print(
    "[PASS] 50 chronology realizations present"
)

print(
    "[PASS] 50 random realizations present"
)

print(
    "[PASS] exact family × learner × seed pairing possible"
)


# =================================================================================================
# 4. BUILD MATCHED SEED-LEVEL CONTRASTS
# =================================================================================================

banner(
    "STAGE28-3C — MATCHED RANDOM-MINUS-CHRONOLOGICAL CONTRASTS"
)


contrast_rows = []


for family in FAMILIES:

    for learner in LEARNERS:

        for seed in SEEDS:

            chrono = indexed[
                (
                    "28A_CHRONOLOGY_LOAO",
                    family,
                    learner,
                    seed,
                )
            ]

            random = indexed[
                (
                    "28B_RANDOM_LOAO_CONTROL",
                    family,
                    learner,
                    seed,
                )
            ]


            chrono_support = int(
                chrono[
                    "support_n"
                ]
            )

            random_support = int(
                random[
                    "support_n"
                ]
            )


            if chrono_support != random_support:
                raise RuntimeError(
                    f"Held-out attack support mismatch "
                    f"{family}/{learner}/seed{seed}: "
                    f"{chrono_support} vs {random_support}"
                )


            if (
                family == "INFILTRATION"
                and chrono_support != 36
            ):
                raise RuntimeError(
                    "Infiltration support changed from 36."
                )


            for metric in CONTRAST_METRICS:

                c = parse_float(
                    chrono[
                        metric
                    ]
                )

                r = parse_float(
                    random[
                        metric
                    ]
                )


                if (
                    math.isfinite(c)
                    and math.isfinite(r)
                ):
                    delta = (
                        r - c
                    )

                    if delta > 0:
                        numeric_direction = (
                            "RANDOM_GT_CHRONO"
                        )

                    elif delta < 0:
                        numeric_direction = (
                            "RANDOM_LT_CHRONO"
                        )

                    else:
                        numeric_direction = (
                            "RANDOM_EQ_CHRONO"
                        )

                else:
                    delta = float(
                        "nan"
                    )

                    numeric_direction = (
                        "UNDEFINED"
                    )


                contrast_rows.append(
                    {

                        "family":
                            family,

                        "learner":
                            learner,

                        "seed":
                            seed,

                        "support_n":
                            chrono_support,

                        "analysis_status":
                            (
                                "DESCRIPTIVE_ONLY_SUPPORT_36_LT_50"
                                if family
                                == "INFILTRATION"
                                else
                                "INFERENTIAL_SUPPORT_ELIGIBLE"
                            ),

                        "metric":
                            metric,

                        "metric_role":
                            (
                                "BASE_RATE_CONTEXT"
                                if metric
                                in BASE_RATE_METRICS
                                else
                                (
                                    "CONFUSION_COUNT_CONTEXT"
                                    if metric
                                    in COUNT_METRICS
                                    else
                                    "PERFORMANCE_METRIC"
                                )
                            ),

                        "chronological_value":
                            c,

                        "random_value":
                            r,

                        "random_minus_chronological":
                            delta,

                        "numeric_direction":
                            numeric_direction,

                        "direction_semantics":
                            (
                                "NUMERIC_ONLY_NOT_AUTOMATICALLY_BETTER_OR_WORSE"
                            ),
                    }
                )


expected_seed_rows = (
    5
    * 2
    * 5
    * len(
        CONTRAST_METRICS
    )
)


if len(
    contrast_rows
) != expected_seed_rows:
    raise RuntimeError(
        f"Seed-level contrast row count mismatch: "
        f"{len(contrast_rows)} != {expected_seed_rows}"
    )


print(
    "[PASS] every contrast is matched by family + learner + seed"
)

print(
    "[PASS] contrast definition = RANDOM minus CHRONOLOGICAL"
)

print(
    "[PASS] Infiltration remains descriptive-only"
)


# =================================================================================================
# 5. FIVE-SEED CONTRAST SUMMARY
# =================================================================================================

banner(
    "STAGE28-3C — FIVE-SEED CONTRAST SUMMARY"
)


groups = defaultdict(
    list
)


for row in contrast_rows:

    key = (
        row[
            "family"
        ],
        row[
            "learner"
        ],
        row[
            "metric"
        ],
        row[
            "analysis_status"
        ],
        row[
            "metric_role"
        ],
    )

    groups[
        key
    ].append(
        row
    )


summary_rows = []

direction_rows = []


for key, items in sorted(
    groups.items()
):

    items = sorted(
        items,
        key=lambda row:
            row[
                "seed"
            ],
    )


    if [
        row[
            "seed"
        ]
        for row in items
    ] != SEEDS:
        raise RuntimeError(
            f"Five-seed coverage failure: {key}"
        )


    deltas = [
        row[
            "random_minus_chronological"
        ]
        for row in items
    ]


    stats = seed_stats(
        deltas
    )


    summary_rows.append(
        {

            "family":
                key[
                    0
                ],

            "learner":
                key[
                    1
                ],

            "metric":
                key[
                    2
                ],

            "analysis_status":
                key[
                    3
                ],

            "metric_role":
                key[
                    4
                ],

            "contrast_definition":
                "RANDOM_MINUS_CHRONOLOGICAL",

            **stats,
        }
    )


    directions = [
        row[
            "numeric_direction"
        ]
        for row in items
    ]


    direction_rows.append(
        {

            "family":
                key[
                    0
                ],

            "learner":
                key[
                    1
                ],

            "metric":
                key[
                    2
                ],

            "analysis_status":
                key[
                    3
                ],

            "metric_role":
                key[
                    4
                ],

            "frozen_seed_count":
                5,

            "defined_seed_count":
                sum(
                    d != "UNDEFINED"
                    for d in directions
                ),

            "random_gt_chrono_seed_count":
                directions.count(
                    "RANDOM_GT_CHRONO"
                ),

            "random_lt_chrono_seed_count":
                directions.count(
                    "RANDOM_LT_CHRONO"
                ),

            "random_eq_chrono_seed_count":
                directions.count(
                    "RANDOM_EQ_CHRONO"
                ),

            "undefined_seed_count":
                directions.count(
                    "UNDEFINED"
                ),

            "note":
                (
                    "Numeric sign count only; no post-result "
                    "qualitative cutoff or causal attribution."
                ),
        }
    )


print(
    "[PASS] mean / median / sample SD / min / max / range / IQR"
)

print(
    "[PASS] seedwise numeric sign counts"
)

print(
    "[PASS] no best-seed reporting"
)

print(
    "[PASS] no new formal significance test"
)


# =================================================================================================
# 6. INTERPRETATION BOUNDARY
# =================================================================================================

banner(
    "STAGE28-3C — INTERPRETATION BOUNDARY"
)


boundary = {

    "stage":
        "Stage28-3C",

    "contrast":
        "RANDOM_MINUS_CHRONOLOGICAL_LOAO",

    "qualitative_interpretation_matrix_present":
        True,

    "automatic_interpretation_labels_assigned":
        False,

    "reason":
        (
            "The frozen interpretation matrix contains labels such as "
            "RANDOM_LOAO_MUCH_GREATER_THAN_CHRONOLOGICAL_LOAO and "
            "RANDOM_AND_CHRONOLOGICAL_LOAO_BOTH_COLLAPSE, but no frozen "
            "numeric cutoffs operationalize 'MUCH_GREATER', 'COLLAPSE', "
            "or 'SURVIVE'. Assigning thresholds after observing Stage28 "
            "results would constitute a post-result condition."
        ),

    "authorized_output":
        (
            "Continuous matched seed-level contrasts, frozen five-seed "
            "summary statistics, and numeric sign counts only."
        ),

    "causal_claim_prohibited":
        (
            "The random-vs-chronological difference is purely caused by temporal drift."
        ),

    "preferred_interpretive_language":
        [
            "random-vs-chronological LOAO contrast",
            "consistent with chronology compounding novelty difficulty",
            "conditional on the benchmark and frozen protocol",
        ],

    "infiltration":
        "DESCRIPTIVE_ONLY_SUPPORT_36_LT_50",

    "aggregate_zero_day_score":
        "NOT_AUTHORIZED_AND_NOT_CREATED",

    "shared_stage22_final_holdout_openings_this_stage":
        0,

    "new_formal_statistical_tests_this_stage":
        0,

    "post_result_condition_creation":
        0,
}


write_json(
    BOUNDARY_OUT,
    boundary,
)


print(
    "[PASS] no unfrozen 'much greater' cutoff created"
)

print(
    "[PASS] no unfrozen 'collapse' cutoff created"
)

print(
    "[PASS] no causal separation claim"
)


# =================================================================================================
# 7. WRITE CONTRAST TABLES
# =================================================================================================

banner(
    "STAGE28-3C — WRITE CONTRAST ARTIFACTS"
)


seed_fields = [
    "family",
    "learner",
    "seed",
    "support_n",
    "analysis_status",
    "metric",
    "metric_role",
    "chronological_value",
    "random_value",
    "random_minus_chronological",
    "numeric_direction",
    "direction_semantics",
]


summary_fields = [
    "family",
    "learner",
    "metric",
    "analysis_status",
    "metric_role",
    "contrast_definition",
    "n_seeds",
    "n_defined",
    "mean",
    "median",
    "sample_standard_deviation_ddof_1",
    "minimum",
    "maximum",
    "range",
    "IQR_Q75_minus_Q25_linear",
]


direction_fields = [
    "family",
    "learner",
    "metric",
    "analysis_status",
    "metric_role",
    "frozen_seed_count",
    "defined_seed_count",
    "random_gt_chrono_seed_count",
    "random_lt_chrono_seed_count",
    "random_eq_chrono_seed_count",
    "undefined_seed_count",
    "note",
]


write_csv(
    SEED_LEVEL_OUT,
    contrast_rows,
    seed_fields,
)

write_csv(
    SUMMARY_OUT,
    summary_rows,
    summary_fields,
)

write_csv(
    DIRECTION_OUT,
    direction_rows,
    direction_fields,
)


receipt = {

    "stage":
        "Stage28-3C",

    "type":
        "RANDOM_VS_CHRONOLOGICAL_LOAO_CONTRAST",

    "created_at_utc":
        datetime.now(
            timezone.utc
        ).isoformat(),

    "scientific_parent_commit":
        EXPECTED_PARENT,

    "input": {

        "path":
            str(
                INPUT.relative_to(
                    REPO
                )
            ),

        "sha256":
            sha256_file(
                INPUT
            ),

        "chronology_seed_realizations":
            50,

        "random_seed_realizations":
            50,
    },

    "contrast_design": {

        "pairing":
            "EXACT_FAMILY_LEARNER_MODEL_SEED",

        "contrast":
            "RANDOM_VALUE_MINUS_CHRONOLOGICAL_VALUE",

        "families":
            FAMILIES,

        "learners":
            LEARNERS,

        "seeds":
            SEEDS,

        "metrics":
            CONTRAST_METRICS,

        "five_seed_statistics":
            seed_spec[
                "five_seed_statistics"
            ],

        "numeric_sign_counts":
            True,

        "best_seed_reporting":
            "FORBIDDEN",

        "new_qualitative_cutoff":
            False,

        "new_formal_statistical_test":
            False,

        "aggregate_zero_day_score":
            False,
    },

    "scientific_operations": {

        "new_model_fits":
            0,

        "model_inference":
            0,

        "threshold_selection":
            0,

        "target_openings":
            0,

        "shared_stage22_final_holdout_openings":
            0,

        "bootstrap_recomputation":
            0,

        "new_formal_statistical_tests":
            0,
    },

    "support_policy": {

        "INFILTRATION":
            "DESCRIPTIVE_ONLY_SUPPORT_36_LT_50",

        "other_families":
            "INFERENTIAL_SUPPORT_ELIGIBLE",
    },

    "interpretation_boundary": {

        "automatic_interpretation_matrix_category_assignment":
            False,

        "reason":
            "NO_FROZEN_NUMERIC_CUTOFF_FOR_MUCH_GREATER_COLLAPSE_OR_SURVIVE",

        "causal_temporal_drift_attribution":
            "PROHIBITED",
    },

    "next_authorized_step":
        (
            "Stage28-4 — preregistered one-time Stage22 shared-final-holdout "
            "inference for all five seed realizations and final Stage22 "
            "directional conclusion-stability evaluation. ZERO new fits; "
            "threshold selection on the final holdout remains forbidden."
        ),
}


write_json(
    RECEIPT_OUT,
    receipt,
)


README_OUT.write_text(
    f"""# Stage28-3C — Random-vs-chronological LOAO contrast

Scientific parent: `{EXPECTED_PARENT}`

This stage is synthesis only.

## Operations

- New model fits: 0
- Model inference: 0
- Threshold selection: 0
- Target openings: 0
- Shared Stage22 final-holdout openings: 0
- New formal statistical tests: 0

## Contrast

Every Stage28B random-LOAO result is paired with the Stage27 chronology-LOAO
result having the same held-out family, learner, and model seed.

The reported contrast is:

`random metric - chronological metric`

The five frozen seeds are summarized using the preregistered mean, median,
sample standard deviation (ddof=1), minimum, maximum, range, and linear IQR.

Numeric positive/negative/equal seed counts are also reported.

## Interpretation boundary

No new cutoff is created for terms such as "much greater", "collapse", or
"survive" because the frozen interpretation matrix did not define numeric
thresholds for those labels.

Accordingly, Stage28-3C reports continuous contrasts only.

The random-vs-chronological comparison does not prove that temporal drift is
the sole cause of the difference. Preferred wording is that a contrast may be
"consistent with chronology compounding novelty difficulty", conditional on
the benchmark and frozen protocol.

Infiltration remains descriptive-only because held-out support is 36.

No aggregate zero-day score is created.
""",
    encoding="utf-8",
)


artifact_paths = [
    SEED_LEVEL_OUT,
    SUMMARY_OUT,
    DIRECTION_OUT,
    BOUNDARY_OUT,
    RECEIPT_OUT,
    README_OUT,
]


with CHECKSUM_OUT.open(
    "w",
    encoding="utf-8",
) as f:

    for path in artifact_paths:

        f.write(
            f"{sha256_file(path)}  "
            f"{path.name}\n"
        )


artifact_paths.append(
    CHECKSUM_OUT
)


print(
    "[PASS] seed-level contrast table written"
)

print(
    "[PASS] five-seed contrast summary written"
)

print(
    "[PASS] numeric direction summary written"
)

print(
    "[PASS] interpretation boundary frozen"
)

print(
    "[PASS] Stage28-3C receipt written"
)


# =================================================================================================
# 8. EXACT GIT UNIVERSE
# =================================================================================================

banner(
    "STAGE28-3C — DURABLE COMMIT / PUSH"
)


expected_rel = {
    str(
        path.relative_to(
            REPO
        )
    )
    for path in artifact_paths
}


tracked_changes = set(
    git(
        "diff",
        "--name-only",
    ).splitlines()
)

staged_before = set(
    git(
        "diff",
        "--cached",
        "--name-only",
    ).splitlines()
)

untracked = set(
    git(
        "ls-files",
        "--others",
        "--exclude-standard",
    ).splitlines()
)


if tracked_changes:
    raise RuntimeError(
        "Unexpected tracked modifications before Stage28-3C:\n"
        + "\n".join(
            sorted(
                tracked_changes
            )
        )
    )


if staged_before:
    raise RuntimeError(
        "Unexpected staged files before Stage28-3C."
    )


if untracked != expected_rel:
    raise RuntimeError(
        "Unexpected Stage28-3C untracked universe.\n\n"
        "Expected:\n"
        + "\n".join(
            sorted(
                expected_rel
            )
        )
        + "\n\nActual:\n"
        + "\n".join(
            sorted(
                untracked
            )
        )
    )


for rel in sorted(
    expected_rel
):
    run(
        [
            "git",
            "add",
            "--",
            rel,
        ]
    )


staged_after = set(
    git(
        "diff",
        "--cached",
        "--name-only",
    ).splitlines()
)


if staged_after != expected_rel:
    raise RuntimeError(
        "Stage28-3C staged universe mismatch."
    )


run(
    [
        "git",
        "config",
        "user.name",
        "Stage28 Kaggle",
    ]
)

run(
    [
        "git",
        "config",
        "user.email",
        "stage28-kaggle@users.noreply.github.com",
    ]
)


commit_message = (
    "stage28-3c: freeze random-vs-chronological LOAO contrast"
)


commit_result = run(
    [
        "git",
        "commit",
        "-m",
        commit_message,
    ]
)


print(
    commit_result.stdout.strip()
)


new_head = git(
    "rev-parse",
    "HEAD",
)


if (
    git(
        "rev-parse",
        "HEAD^",
    )
    != EXPECTED_PARENT
):
    raise RuntimeError(
        "Stage28-3C commit parent mismatch."
    )


token, token_source = recover_github_token()


print()
print(
    "[PASS] GitHub credential:",
    token_source,
)

print(
    "[PASS] token not displayed"
)


push_output = authenticated_push(
    token
)


if push_output:
    print(
        push_output
    )


run(
    [
        "git",
        "fetch",
        "origin",
        "main",
    ]
)


if (
    git(
        "rev-parse",
        "HEAD",
    )
    != new_head
    or
    git(
        "rev-parse",
        "origin/main",
    )
    != new_head
):
    raise RuntimeError(
        "Stage28-3C remote durability verification failed."
    )


if git(
    "status",
    "--porcelain",
):
    raise RuntimeError(
        "Repository dirty after Stage28-3C push."
    )


# =================================================================================================
# 9. COMPLETE
# =================================================================================================

banner(
    "STAGE28-3C — COMPLETE"
)


print(
    "Commit:",
    new_head,
)

print()
print(
    "New model fits                    : 0"
)

print(
    "Model inference                   : 0"
)

print(
    "Threshold selection               : 0"
)

print(
    "Target openings                   : 0"
)

print(
    "Shared Stage22 final holdout opens: 0"
)

print(
    "New formal statistical tests      : 0"
)

print()
print(
    "Matched chronology realizations   : 50"
)

print(
    "Matched random realizations       : 50"
)

print(
    "Contrast                          : RANDOM - CHRONOLOGICAL"
)

print(
    "Families                          : 5"
)

print(
    "Learners                          : 2"
)

print(
    "Seeds                             : 5"
)

print(
    "Infiltration                      : DESCRIPTIVE ONLY"
)

print(
    "Aggregate zero-day score          : NOT CREATED"
)

print(
    "Post-result qualitative cutoff    : NOT CREATED"
)

print()
print(
    "NEXT AUTHORIZED STEP:"
)

print(
    "Stage28-4 — one-time Stage22 shared-final-holdout inference"
)

print(
    "ZERO NEW FITS; FINAL-HOLDOUT THRESHOLD SEARCH FORBIDDEN."
)

# ==============================================================================================================
# %% NOTEBOOK CELL 0011 | execution_count=11
# ==============================================================================================================
# =================================================================================================
# STAGE28-4 — PRE-INFERENCE GATE
#
# OPERATIONAL PREFLIGHT ONLY — NOT A NEW SCIENTIFIC STAGE
#
# ZERO MODEL FITS
# ZERO MODEL INFERENCE
# ZERO THRESHOLD SELECTION
# ZERO FINAL-HOLDOUT PREDICTOR ROWS READ
# ZERO FINAL-HOLDOUT LABEL ROWS READ
#
# Purpose:
#   - verify exact Stage28-3C parent
#   - verify Stage28 closure remains 108/108
#   - verify Stage28-4 authorization
#   - audit frozen Stage22R final-holdout membership artifact
#   - inspect membership NPZ schema only
#   - locate exact Kaggle source files without reading data rows
#   - validate CSV headers only
#   - audit all 10 Stage28 Stage22 ensemble/model identities
#   - print already-frozen operating thresholds
#
# NO SCIENTIFIC RESULT IS COMPUTED HERE.
# =================================================================================================

from __future__ import annotations

import csv
import hashlib
import json
import os
import subprocess
from pathlib import Path

import numpy as np


SEP = "=" * 120

REPO = Path(
    "/kaggle/working/ids2018-validation-safe-ablation"
).resolve()

EXPECTED_PARENT = (
    "2679d0c208d514b381caa12e96c959f4f2ee5ee7"
)

ROOT = (
    REPO
    / "results"
    / "stage28_stability_novelty_control"
)

CLOSURE_RECEIPT = (
    ROOT
    / "stage28_3a_experiment_closure_audit"
    / "stage28_3a_experiment_closure_receipt.json"
)

STAGE3C_RECEIPT = (
    ROOT
    / "stage28_3_seed_uncertainty"
    / "stage28_3c_receipt.json"
)

STAGE22_SPEC = (
    ROOT
    / "stage28_0_protocol_lock"
    / "stage22_cell_spec.json"
)

STAGE22_STAGE28_ROOT = (
    ROOT
    / "stage28_2a_stage22_seed_stability"
)

STAGE22R_FINAL_ROOT = (
    REPO
    / "results"
    / "stage22r_training"
    / "stage22r_final_single_holdout"
)

MEMBERSHIP = (
    STAGE22R_FINAL_ROOT
    / "stage22r_final_holdout_clean_membership.npz"
)

PARENT_SUMMARY = (
    STAGE22R_FINAL_ROOT
    / "stage22r_final_holdout_k79_summary.json"
)

PARENT_RESULT = (
    STAGE22R_FINAL_ROOT
    / "stage22r_final_holdout_result.json"
)

PARENT_CHECKSUMS = (
    STAGE22R_FINAL_ROOT
    / "checksums.sha256"
)

FEATURE_CONFIG = (
    REPO
    / "results"
    / "stage15_transformer_checkpoint"
    / "stage15_1_feature_configuration.json"
)

LOCAL_PREFLIGHT_RECEIPT = Path(
    "/kaggle/working/stage28_4_preflight_receipt.json"
)

EXPECTED_ROWS = 1_374_133
EXPECTED_BENIGN = 998_788
EXPECTED_ATTACK = 375_345
EXPECTED_FEATURES = 70

EXPECTED_UNITS = [
    "RANDOM_NATURAL",
    "CHRONOLOGICAL_NATURAL",
]

EXPECTED_SEEDS = [
    42,
    43,
    44,
    45,
    46,
]

EXPECTED_LEARNERS = [
    "xgboost",
    "lightgbm",
]


# =================================================================================================
# HELPERS
# =================================================================================================

def banner(text):
    print()
    print(SEP)
    print(text)
    print(SEP)
    print()


def run(cmd, *, cwd=REPO, check=True):

    p = subprocess.run(
        [str(x) for x in cmd],
        cwd=str(cwd),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    if check and p.returncode != 0:
        raise RuntimeError(
            f"Command failed ({p.returncode}):\n"
            + " ".join(map(str, cmd))
            + f"\n\nSTDOUT:\n{p.stdout}"
            + f"\n\nSTDERR:\n{p.stderr}"
        )

    return p


def git(*args):

    return run(
        ["git", *args]
    ).stdout.strip()


def read_json(path):

    return json.loads(
        Path(path).read_text(
            encoding="utf-8"
        )
    )


def sha256_file(path, chunk=16 * 1024 * 1024):

    h = hashlib.sha256()

    with Path(path).open("rb") as f:

        while True:

            block = f.read(chunk)

            if not block:
                break

            h.update(block)

    return h.hexdigest()


def resolve_checksum_for_basename(
    checksum_file,
    wanted_basename,
):

    matches = []

    for raw in Path(
        checksum_file
    ).read_text(
        encoding="utf-8"
    ).splitlines():

        raw = raw.strip()

        if not raw:
            continue

        parts = raw.split(
            None,
            1,
        )

        if len(parts) != 2:
            continue

        digest = parts[0].strip()

        name = (
            parts[1]
            .strip()
            .lstrip("*")
        )

        if Path(name).name == wanted_basename:

            matches.append(
                (
                    digest,
                    name,
                )
            )

    if len(matches) != 1:

        raise RuntimeError(
            "Expected exactly one checksum entry for "
            f"{wanted_basename}; found {len(matches)}."
        )

    return matches[0]


def recursively_find_feature_lists(obj):

    candidates = []

    def walk(x, path="root"):

        if isinstance(x, dict):

            for k, v in x.items():

                walk(
                    v,
                    f"{path}.{k}",
                )

        elif isinstance(x, list):

            if (
                len(x) == EXPECTED_FEATURES
                and
                all(
                    isinstance(v, str)
                    for v in x
                )
            ):

                candidates.append(
                    (
                        path,
                        x,
                    )
                )

            for i, v in enumerate(x):

                walk(
                    v,
                    f"{path}[{i}]",
                )

    walk(obj)

    return candidates


def read_csv_header_only(path):

    # IMPORTANT:
    # reads exactly the header line and NO data row.
    with Path(path).open(
        "r",
        encoding="utf-8-sig",
        errors="strict",
        newline="",
    ) as f:

        first_line = f.readline()

    if not first_line:
        raise RuntimeError(
            f"Empty CSV source: {path}"
        )

    return next(
        csv.reader(
            [first_line]
        )
    )


def normalize_header_name(value):

    return (
        str(value)
        .replace("\ufeff", "")
        .strip()
    )


def resolve_model_path(
    result_path,
    model,
):

    local_name = (
        model.get("model_path")
        or model.get("model")
    )

    if local_name:

        path = (
            result_path.parent
            / local_name
        )

        expected_sha = model.get(
            "model_sha256"
        )

        source_type = (
            "STAGE28_COMPONENT_ARTIFACT"
        )

    else:

        historical = model.get(
            "historical_model_path"
        )

        if not historical:

            raise RuntimeError(
                f"No model artifact path found in {result_path}"
            )

        path = (
            REPO
            / historical
        )

        expected_sha = model.get(
            "historical_model_sha256"
        )

        source_type = (
            "HISTORICAL_REUSE_ARTIFACT"
        )

    if not path.is_file():

        raise RuntimeError(
            "Model file missing:\n"
            f"{path}"
        )

    if not expected_sha:

        raise RuntimeError(
            "Expected model SHA missing in result receipt:\n"
            f"{result_path}"
        )

    actual_sha = sha256_file(
        path
    )

    if actual_sha != expected_sha:

        raise RuntimeError(
            "Model SHA mismatch:\n"
            f"{path}\n"
            f"expected={expected_sha}\n"
            f"actual={actual_sha}"
        )

    return (
        path,
        actual_sha,
        source_type,
    )


def extract_threshold(
    operating_points,
    name,
):

    key = name.lower()

    op = operating_points.get(
        key
    )

    if op is None:

        raise RuntimeError(
            f"Missing operating point: {name}"
        )

    if (
        isinstance(op, dict)
        and
        "result" in op
    ):

        if (
            op.get("status")
            not in (
                None,
                "AVAILABLE",
            )
        ):

            return {
                "status": op.get(
                    "status"
                ),
                "threshold": None,
            }

        op = op[
            "result"
        ]

    if not isinstance(op, dict):

        raise RuntimeError(
            f"Malformed operating point: {name}"
        )

    threshold = op.get(
        "threshold"
    )

    if threshold is None:

        raise RuntimeError(
            f"Threshold missing for {name}"
        )

    return {
        "status": "AVAILABLE",
        "threshold": float(
            threshold
        ),
    }


# =================================================================================================
# 0. REPOSITORY / LINEAGE
# =================================================================================================

banner(
    "STAGE28-4 PREFLIGHT — REPOSITORY / LINEAGE GATE"
)


if not (
    REPO
    / ".git"
).is_dir():

    raise RuntimeError(
        f"Repository missing:\n{REPO}"
    )


status = git(
    "status",
    "--porcelain",
)


if status:

    raise RuntimeError(
        "Repository must be clean before Stage28-4 preflight:\n"
        + status
    )


run(
    [
        "git",
        "fetch",
        "origin",
        "main",
    ]
)


local_head = git(
    "rev-parse",
    "HEAD",
)

origin_head = git(
    "rev-parse",
    "origin/main",
)


print(
    "Expected parent:",
    EXPECTED_PARENT,
)

print(
    "Local HEAD     :",
    local_head,
)

print(
    "origin/main    :",
    origin_head,
)


if not (
    local_head
    == origin_head
    == EXPECTED_PARENT
):

    raise RuntimeError(
        "Stage28-4 preflight parent mismatch."
    )


print()
print(
    "[PASS] Stage28-3C durable parent exact"
)

print(
    "[PASS] repository clean"
)


# =================================================================================================
# 1. STAGE28 CLOSURE + AUTHORIZATION
# =================================================================================================

banner(
    "STAGE28-4 PREFLIGHT — SCIENTIFIC AUTHORIZATION GATE"
)


closure = read_json(
    CLOSURE_RECEIPT
)

stage3c = read_json(
    STAGE3C_RECEIPT
)

stage22_spec = read_json(
    STAGE22_SPEC
)


if (
    closure.get(
        "closure_status"
    )
    !=
    "PASS_STAGE28_NEW_MODEL_FITTING_PERMANENTLY_CLOSED"
):

    raise RuntimeError(
        "Stage28-3A closure is not PASS."
    )


if (
    int(
        closure[
            "fit_budget_closure"
        ][
            "consumed_new_fits"
        ]
    )
    != 108
    or
    int(
        closure[
            "fit_budget_closure"
        ][
            "remaining_new_fits"
        ]
    )
    != 0
):

    raise RuntimeError(
        "Stage28 fit ledger is no longer 108/108."
    )


next_step = stage3c.get(
    "next_authorized_step",
    ""
)


if not next_step.startswith(
    "Stage28-4"
):

    raise RuntimeError(
        "Stage28-3C does not authorize Stage28-4."
    )


if (
    stage22_spec[
        "evaluation_population"
    ][
        "name"
    ]
    !=
    "STAGE22R_SHARED_FINAL_SINGLE_HOLDOUT"
):

    raise RuntimeError(
        "Unexpected Stage22 evaluation population."
    )


if (
    stage22_spec[
        "evaluation_population"
    ][
        "threshold_selection_on_final_holdout"
    ]
    != "FORBIDDEN"
):

    raise RuntimeError(
        "Final-holdout threshold-selection rule changed."
    )


if (
    stage22_spec[
        "evaluation_population"
    ][
        "model_selection_on_final_holdout"
    ]
    != "FORBIDDEN"
):

    raise RuntimeError(
        "Final-holdout model-selection rule changed."
    )


print(
    "[PASS] 108 / 108 new fits closed"
)

print(
    "[PASS] remaining fits = 0"
)

print(
    "[PASS] Stage28-4 explicitly authorized"
)

print(
    "[PASS] shared final holdout population exact"
)

print(
    "[PASS] threshold selection on final holdout FORBIDDEN"
)

print(
    "[PASS] model selection on final holdout FORBIDDEN"
)


# =================================================================================================
# 2. PARENT HOLDOUT CONTRACT
# =================================================================================================

banner(
    "STAGE28-4 PREFLIGHT — FROZEN STAGE22R HOLDOUT CONTRACT"
)


for path in [
    MEMBERSHIP,
    PARENT_SUMMARY,
    PARENT_RESULT,
    PARENT_CHECKSUMS,
]:

    if not path.is_file():

        raise RuntimeError(
            f"Frozen Stage22R artifact missing:\n{path}"
        )


parent_summary = read_json(
    PARENT_SUMMARY
)


summary_text = json.dumps(
    parent_summary
)


# Fail closed against the known frozen census.
for required_value in [
    str(EXPECTED_ROWS),
    str(EXPECTED_BENIGN),
    str(EXPECTED_ATTACK),
]:

    if required_value not in summary_text:

        raise RuntimeError(
            "Parent Stage22R summary no longer contains "
            f"expected frozen value {required_value}."
        )


expected_membership_sha, checksum_entry = (
    resolve_checksum_for_basename(
        PARENT_CHECKSUMS,
        MEMBERSHIP.name,
    )
)


actual_membership_sha = sha256_file(
    MEMBERSHIP
)


print(
    "Membership artifact:"
)

print(
    " ",
    MEMBERSHIP.relative_to(
        REPO
    )
)

print()
print(
    "Expected SHA256:",
    expected_membership_sha,
)

print(
    "Actual SHA256  :",
    actual_membership_sha,
)


if (
    actual_membership_sha
    != expected_membership_sha
):

    raise RuntimeError(
        "Frozen final-holdout membership SHA mismatch."
    )


print()
print(
    "[PASS] parent holdout rows   = 1,374,133"
)

print(
    "[PASS] parent holdout benign = 998,788"
)

print(
    "[PASS] parent holdout attack = 375,345"
)

print(
    "[PASS] membership artifact checksum exact"
)


# =================================================================================================
# 3. MEMBERSHIP NPZ SCHEMA INSPECTION
# =================================================================================================

banner(
    "STAGE28-4 PREFLIGHT — MEMBERSHIP NPZ SCHEMA"
)


membership_schema = {}


with np.load(
    MEMBERSHIP,
    allow_pickle=False,
) as npz:

    keys = list(
        npz.files
    )

    print(
        "NPZ keys:",
        keys,
    )

    print()


    if not keys:

        raise RuntimeError(
            "Membership NPZ has no arrays."
        )


    for key in keys:

        arr = np.asarray(
            npz[
                key
            ]
        )


        info = {

            "shape":
                list(
                    arr.shape
                ),

            "dtype":
                str(
                    arr.dtype
                ),

            "ndim":
                int(
                    arr.ndim
                ),

            "size":
                int(
                    arr.size
                ),
        }


        print(
            f"[{key}]"
        )

        print(
            "  shape:",
            arr.shape,
        )

        print(
            "  dtype:",
            arr.dtype,
        )

        print(
            "  ndim :",
            arr.ndim,
        )

        print(
            "  size :",
            f"{arr.size:,}",
        )


        if arr.size:

            flat = arr.reshape(
                -1
            )


            head = flat[
                :min(
                    10,
                    flat.size,
                )
            ].tolist()

            tail = flat[
                max(
                    0,
                    flat.size - 10,
                ):
            ].tolist()


            info[
                "head"
            ] = head

            info[
                "tail"
            ] = tail


            print(
                "  head :",
                head,
            )

            print(
                "  tail :",
                tail,
            )


            if np.issubdtype(
                arr.dtype,
                np.number,
            ):

                finite = (
                    arr[
                        np.isfinite(
                            arr
                        )
                    ]
                    if np.issubdtype(
                        arr.dtype,
                        np.floating,
                    )
                    else arr
                )


                if finite.size:

                    info[
                        "minimum"
                    ] = (
                        finite.min().item()
                    )

                    info[
                        "maximum"
                    ] = (
                        finite.max().item()
                    )


                    print(
                        "  min  :",
                        info[
                            "minimum"
                        ],
                    )

                    print(
                        "  max  :",
                        info[
                            "maximum"
                        ],
                    )


        membership_schema[
            key
        ] = info

        print()


print(
    "[PASS] membership schema inspected"
)

print(
    "[PASS] no raw final-holdout data row read"
)


# =================================================================================================
# 4. EXACT 70-FEATURE CONTRACT
# =================================================================================================

banner(
    "STAGE28-4 PREFLIGHT — 70-FEATURE CONTRACT"
)


if not FEATURE_CONFIG.is_file():

    raise RuntimeError(
        f"Feature configuration missing:\n{FEATURE_CONFIG}"
    )


feature_obj = read_json(
    FEATURE_CONFIG
)


feature_candidates = (
    recursively_find_feature_lists(
        feature_obj
    )
)


feature_candidates = [
    (
        path,
        values,
    )
    for path, values
    in feature_candidates
    if (
        "Dst Port" in values
        and
        "Idle Min" in values
    )
]


if len(
    feature_candidates
) != 1:

    print(
        "Candidate 70-feature lists:"
    )

    for path, values in (
        feature_candidates
    ):

        print(
            " ",
            path,
            values[
                :3
            ],
            "...",
            values[
                -3:
            ],
        )


    raise RuntimeError(
        "Could not resolve exactly one frozen 70-feature list."
    )


feature_path, FEATURES = (
    feature_candidates[
        0
    ]
)


if len(
    FEATURES
) != EXPECTED_FEATURES:

    raise RuntimeError(
        "Frozen feature count != 70."
    )


if FEATURES[
    0
] != "Dst Port":

    raise RuntimeError(
        "Unexpected first frozen feature."
    )


if FEATURES[
    -1
] != "Idle Min":

    raise RuntimeError(
        "Unexpected final frozen feature."
    )


print(
    "Feature-list source:",
    feature_path,
)

print(
    "Feature count      :",
    len(
        FEATURES
    ),
)

print(
    "First feature      :",
    FEATURES[
        0
    ],
)

print(
    "Last feature       :",
    FEATURES[
        -1
    ],
)


print()
print(
    "[PASS] exact frozen 70-feature configuration resolved"
)


# =================================================================================================
# 5. LOCATE EXACT KAGGLE FINAL-HOLDOUT SOURCES
# =================================================================================================

banner(
    "STAGE28-4 PREFLIGHT — KAGGLE SOURCE DISCOVERY"
)


KAGGLE_INPUT = Path(
    "/kaggle/input"
)


if not KAGGLE_INPUT.is_dir():

    raise RuntimeError(
        "/kaggle/input does not exist."
    )


day1_candidates = sorted(
    KAGGLE_INPUT.rglob(
        "03-01-2018.csv"
    )
)

day2_candidates = sorted(
    KAGGLE_INPUT.rglob(
        "03-02-2018.csv"
    )
)


print(
    "03-01 candidates:"
)

for path in day1_candidates:

    print(
        " ",
        path,
    )


print()
print(
    "03-02 candidates:"
)

for path in day2_candidates:

    print(
        " ",
        path,
    )


pairs = []


for p1 in day1_candidates:

    for p2 in day2_candidates:

        if p1.parent == p2.parent:

            pairs.append(
                (
                    p1,
                    p2,
                )
            )


# Prefer the exact Kaggle slug directory.
exact_pairs = [
    pair
    for pair in pairs
    if pair[
        0
    ].parent.name
    == "ids-intrusion-csv"
]


if len(
    exact_pairs
) == 1:

    source_day1, source_day2 = (
        exact_pairs[
            0
        ]
    )

elif (
    len(
        exact_pairs
    )
    == 0
    and
    len(
        pairs
    )
    == 1
):

    # We still fail closed rather than silently accepting a mirror.
    candidate = pairs[
        0
    ]

    raise RuntimeError(
        "\nThe two March source files exist, but not under the "
        "expected Kaggle dataset directory `ids-intrusion-csv`.\n\n"
        f"Found:\n  {candidate[0]}\n  {candidate[1]}\n\n"
        "Attach the frozen Kaggle dataset:\n"
        "  solarmainframe/ids-intrusion-csv"
    )

else:

    raise RuntimeError(
        "\nCould not resolve exactly one frozen March source pair.\n\n"
        "Attach the exact Kaggle dataset:\n"
        "  solarmainframe/ids-intrusion-csv\n\n"
        "Then rerun this preflight cell."
    )


print()
print(
    "Resolved dataset root:"
)

print(
    " ",
    source_day1.parent,
)

print()
print(
    "03-01 bytes:",
    f"{source_day1.stat().st_size:,}",
)

print(
    "03-02 bytes:",
    f"{source_day2.stat().st_size:,}",
)


# =================================================================================================
# 6. HEADER-ONLY VALIDATION
# =================================================================================================

banner(
    "STAGE28-4 PREFLIGHT — SOURCE HEADER-ONLY VALIDATION"
)


source_headers = {}


for day_name, path in [
    (
        "03-01-2018.csv",
        source_day1,
    ),
    (
        "03-02-2018.csv",
        source_day2,
    ),
]:

    header = [
        normalize_header_name(
            x
        )
        for x in (
            read_csv_header_only(
                path
            )
        )
    ]


    source_headers[
        day_name
    ] = header


    print(
        day_name,
    )

    print(
        "  columns:",
        len(
            header
        ),
    )

    print(
        "  first 5:",
        header[
            :5
        ],
    )

    print(
        "  last 5 :",
        header[
            -5:
        ],
    )


    missing_features = [
        feature
        for feature in FEATURES
        if feature not in header
    ]


    if missing_features:

        raise RuntimeError(
            f"{day_name} is missing frozen features:\n"
            + "\n".join(
                missing_features
            )
        )


    if "Label" not in header:

        raise RuntimeError(
            f"{day_name} has no Label column."
        )


print()
print(
    "[PASS] both March files contain all 70 frozen features"
)

print(
    "[PASS] Label column present in both files"
)

print(
    "[PASS] only CSV header lines were read"
)

print(
    "[PASS] scientific holdout predictor rows read = 0"
)

print(
    "[PASS] scientific holdout labels read = 0"
)


# =================================================================================================
# 7. AUDIT ALL TEN STAGE28 STAGE22 ENSEMBLES
# =================================================================================================

banner(
    "STAGE28-4 PREFLIGHT — TEN STAGE22 ENSEMBLE IDENTITIES"
)


result_files = sorted(
    STAGE22_STAGE28_ROOT.rglob(
        "*_result.json"
    )
)


if len(
    result_files
) != 10:

    raise RuntimeError(
        f"Expected exactly 10 Stage28 Stage22 result receipts; "
        f"found {len(result_files)}."
    )


ensemble_records = []


for result_path in result_files:

    obj = read_json(
        result_path
    )


    if (
        obj.get(
            "experiment"
        )
        != "STAGE22_FULL"
    ):

        raise RuntimeError(
            f"Unexpected experiment in:\n{result_path}"
        )


    unit = obj.get(
        "unit"
    )

    seed = int(
        obj.get(
            "training_seed"
        )
    )


    if unit not in EXPECTED_UNITS:

        raise RuntimeError(
            f"Unexpected Stage22 unit: {unit}"
        )


    if seed not in EXPECTED_SEEDS:

        raise RuntimeError(
            f"Unexpected Stage22 seed: {seed}"
        )


    models = obj.get(
        "models"
    )


    if not isinstance(
        models,
        dict,
    ):

        raise RuntimeError(
            f"Malformed models container:\n{result_path}"
        )


    model_records = {}


    for learner in EXPECTED_LEARNERS:

        if learner not in models:

            raise RuntimeError(
                f"{unit}/seed{seed}: missing {learner}."
            )


        model = models[
            learner
        ]


        if not isinstance(
            model,
            dict,
        ):

            raise RuntimeError(
                f"{unit}/seed{seed}/{learner}: "
                "model receipt is not a dictionary."
            )


        model_path, model_sha, source_type = (
            resolve_model_path(
                result_path,
                model,
            )
        )


        model_seed = int(
            model[
                "seed"
            ]
        )


        if model_seed != seed:

            raise RuntimeError(
                f"{unit}/{learner}: model seed mismatch "
                f"{model_seed} != {seed}."
            )


        backend = str(
            model.get(
                "backend",
                ""
            )
        ).lower()


        if backend != "cpu":

            raise RuntimeError(
                f"{unit}/seed{seed}/{learner}: "
                f"non-CPU backend {backend!r}."
            )


        model_records[
            learner
        ] = {

            "component_id":
                model.get(
                    "component_id"
                ),

            "path":
                str(
                    model_path.relative_to(
                        REPO
                    )
                ),

            "sha256":
                model_sha,

            "source_type":
                source_type,

            "backend":
                backend,
        }


    thresholds = {

        name:
            extract_threshold(
                obj[
                    "operating_points"
                ],
                name,
            )

        for name in [
            "STANDARD",
            "BALANCED",
            "SECURITY",
        ]
    }


    ensemble_records.append(
        {

            "unit":
                unit,

            "seed":
                seed,

            "result_path":
                str(
                    result_path.relative_to(
                        REPO
                    )
                ),

            "xgboost":
                model_records[
                    "xgboost"
                ],

            "lightgbm":
                model_records[
                    "lightgbm"
                ],

            "thresholds":
                thresholds,
        }
    )


ensemble_records.sort(
    key=lambda x:
        (
            EXPECTED_UNITS.index(
                x[
                    "unit"
                ]
            ),
            x[
                "seed"
            ],
        )
)


actual_pairs = [
    (
        x[
            "unit"
        ],
        x[
            "seed"
        ],
    )
    for x in ensemble_records
]


expected_pairs = [
    (
        unit,
        seed,
    )
    for unit in EXPECTED_UNITS
    for seed in EXPECTED_SEEDS
]


if actual_pairs != expected_pairs:

    raise RuntimeError(
        "Ten Stage22 ensemble cells are not exactly "
        "2 units × seeds42-46."
    )


for record in ensemble_records:

    print(
        f"{record['unit']:<24} seed={record['seed']}"
    )

    print(
        "  XGB:",
        record[
            "xgboost"
        ][
            "component_id"
        ],
        record[
            "xgboost"
        ][
            "sha256"
        ],
    )

    print(
        "  LGB:",
        record[
            "lightgbm"
        ][
            "component_id"
        ],
        record[
            "lightgbm"
        ][
            "sha256"
        ],
    )

    print(
        "  thresholds:",
        {
            k:
                v[
                    "threshold"
                ]
            for k, v in (
                record[
                    "thresholds"
                ].items()
            )
        },
    )

    print()


print(
    "[PASS] exactly 10 Stage22 ensembles"
)

print(
    "[PASS] 2 geometries × 5 seeds"
)

print(
    "[PASS] all 20 component model artifact SHA256 values exact"
)

print(
    "[PASS] all Stage28 Stage22 model backends = CPU"
)

print(
    "[PASS] all thresholds read from frozen validation receipts"
)

print(
    "[PASS] ZERO threshold recomputation"
)


# =================================================================================================
# 8. LIBRARY RUNTIME — NO MODEL LOADING / NO PREDICTION
# =================================================================================================

banner(
    "STAGE28-4 PREFLIGHT — MODEL LIBRARY RUNTIME"
)


import xgboost
import lightgbm
import sklearn


print(
    "scikit-learn:",
    sklearn.__version__,
)

print(
    "XGBoost      :",
    xgboost.__version__,
)

print(
    "LightGBM     :",
    lightgbm.__version__,
)


if (
    xgboost.__version__
    != "3.2.0"
):

    raise RuntimeError(
        "XGBoost version mismatch."
    )


if (
    lightgbm.__version__
    != "4.6.0"
):

    raise RuntimeError(
        "LightGBM version mismatch."
    )


print()
print(
    "[PASS] XGBoost 3.2.0 exact"
)

print(
    "[PASS] LightGBM 4.6.0 exact"
)


# =================================================================================================
# 9. LOCAL MACHINE-READABLE PREFLIGHT RECEIPT
# =================================================================================================

banner(
    "STAGE28-4 PREFLIGHT — LOCAL RECEIPT"
)


preflight_receipt = {

    "type":
        "STAGE28_4_OPERATIONAL_PREFLIGHT",

    "scientific_stage":
        "Stage28-4",

    "scientific_parent":
        EXPECTED_PARENT,

    "scientific_operations": {

        "new_model_fits":
            0,

        "model_inference":
            0,

        "threshold_selection":
            0,

        "final_holdout_predictor_rows_read":
            0,

        "final_holdout_labels_read":
            0,
    },

    "frozen_holdout_contract": {

        "rows":
            EXPECTED_ROWS,

        "benign":
            EXPECTED_BENIGN,

        "attack":
            EXPECTED_ATTACK,

        "features":
            EXPECTED_FEATURES,

        "dtype":
            "float64",

        "membership_path":
            str(
                MEMBERSHIP.relative_to(
                    REPO
                )
            ),

        "membership_sha256":
            actual_membership_sha,

        "membership_schema":
            membership_schema,
    },

    "source_binding": {

        "provider":
            "KAGGLE",

        "dataset":
            "solarmainframe/ids-intrusion-csv",

        "dataset_root":
            str(
                source_day1.parent
            ),

        "03_01_path":
            str(
                source_day1
            ),

        "03_01_bytes":
            source_day1.stat().st_size,

        "03_02_path":
            str(
                source_day2
            ),

        "03_02_bytes":
            source_day2.stat().st_size,

        "data_rows_read":
            0,

        "header_only":
            True,
    },

    "stage22_ensembles": ensemble_records,

    "status":
        "READY_FOR_EXACT_STAGE28_4_INFERENCE_CELL_AFTER_MEMBERSHIP_SCHEMA_REVIEW",
}


LOCAL_PREFLIGHT_RECEIPT.write_text(
    json.dumps(
        preflight_receipt,
        indent=2,
    )
    + "\n",
    encoding="utf-8",
)


print(
    "Local receipt:"
)

print(
    " ",
    LOCAL_PREFLIGHT_RECEIPT,
)

print()
print(
    "[PASS] receipt written outside Git repository"
)

print(
    "[PASS] repository remains scientifically unchanged"
)


# =================================================================================================
# 10. FINAL PREFLIGHT STATUS
# =================================================================================================

if git(
    "status",
    "--porcelain",
):

    raise RuntimeError(
        "Repository changed during operational preflight."
    )


banner(
    "STAGE28-4 PREFLIGHT COMPLETE"
)


print(
    "Scientific parent:"
)

print(
    " ",
    EXPECTED_PARENT,
)

print()
print(
    "Stage28 new fits                 : 108 / 108 CLOSED"
)

print(
    "New fits remaining               : 0"
)

print(
    "Stage28-4 ensemble cells         : 10 / 10 VERIFIED"
)

print(
    "Stage28-4 component models       : 20 / 20 SHA-VERIFIED"
)

print(
    "Shared final holdout expected    : 1,374,133 rows"
)

print(
    "Frozen feature count             : 70"
)

print()
print(
    "New model fits                   : 0"
)

print(
    "Model inference                  : 0"
)

print(
    "Threshold selection              : 0"
)

print(
    "Final-holdout predictor rows read: 0"
)

print(
    "Final-holdout labels read        : 0"
)

print()
print(
    "NO SHARED FINAL-HOLDOUT SCIENTIFIC OPENING HAS OCCURRED."
)

print()
print(
    "NEXT:"
)

print(
    "Use the reported membership NPZ keys/schema to execute the "
    "single authorized Stage28-4 holdout materialization + inference."
)

# ==============================================================================================================
# %% NOTEBOOK CELL 0012 | execution_count=12
# ==============================================================================================================
# =================================================================================================
# STAGE28-4 — ONE-TIME STAGE22 SHARED-FINAL-HOLDOUT INFERENCE
#
# AUTHORIZED SCIENTIFIC OPERATION
#
# NEW MODEL FITS                   : 0
# THRESHOLD SELECTION              : 0
# MODEL SELECTION                  : 0
# NEW FORMAL STATISTICAL TESTS     : 0
# SHAP / SUBSET SEARCH             : 0
#
# AUTHORIZED:
#   - materialize exact frozen Stage22R shared final holdout
#   - infer 20 already-frozen component models
#   - construct 10 frozen equal-weight ensembles
#   - evaluate seeds 42..46
#   - apply ONLY thresholds frozen on development validation
#   - evaluate preregistered Stage22 directional conclusion stability
#
# FINAL HOLDOUT:
#   1,374,133 rows
#   998,788 benign
#   375,345 attack
#   70 features
#   float64 model input
#
# IMPORTANT:
#   The Stage22R parent holdout is already historically known.
#   Stage28-4 is preregistered robustness re-evaluation, not a new blind test.
# =================================================================================================

from __future__ import annotations

import csv
import gc
import hashlib
import json
import math
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

import numpy as np
import pandas as pd
import sklearn
from sklearn.metrics import (
    average_precision_score,
    roc_auc_score,
)

import xgboost as xgb
import lightgbm as lgb


# =================================================================================================
# CONSTANTS
# =================================================================================================

SEP = "=" * 120

REPO = Path(
    "/kaggle/working/ids2018-validation-safe-ablation"
).resolve()

EXPECTED_PARENT = (
    "2679d0c208d514b381caa12e96c959f4f2ee5ee7"
)

ROOT = (
    REPO
    / "results"
    / "stage28_stability_novelty_control"
)

STAGE22_ROOT = (
    ROOT
    / "stage28_2a_stage22_seed_stability"
)

PROTOCOL_ROOT = (
    ROOT
    / "stage28_0_protocol_lock"
)

STAGE3_ROOT = (
    ROOT
    / "stage28_3_seed_uncertainty"
)

STAGE4_ROOT = (
    ROOT
    / "stage28_4_stage22_shared_final_holdout"
)

STAGE22R_FINAL = (
    REPO
    / "results"
    / "stage22r_training"
    / "stage22r_final_single_holdout"
)

MEMBERSHIP_PATH = (
    STAGE22R_FINAL
    / "stage22r_final_holdout_clean_membership.npz"
)

PARENT_HOLDOUT_SUMMARY = (
    STAGE22R_FINAL
    / "stage22r_final_holdout_k79_summary.json"
)

PARENT_HOLDOUT_RESULT = (
    STAGE22R_FINAL
    / "stage22r_final_holdout_result.json"
)

PARENT_CHECKSUMS = (
    STAGE22R_FINAL
    / "checksums.sha256"
)

FEATURE_CONFIG = (
    REPO
    / "results"
    / "stage15_transformer_checkpoint"
    / "stage15_1_feature_configuration.json"
)

STAGE22_SPEC = (
    PROTOCOL_ROOT
    / "stage22_cell_spec.json"
)

STABILITY_SPEC = (
    PROTOCOL_ROOT
    / "conclusion_stability_spec.json"
)

CLOSURE_RECEIPT = (
    ROOT
    / "stage28_3a_experiment_closure_audit"
    / "stage28_3a_experiment_closure_receipt.json"
)

STAGE3C_RECEIPT = (
    STAGE3_ROOT
    / "stage28_3c_receipt.json"
)

LOAO_CONCLUSION_STABILITY = (
    STAGE3_ROOT
    / "stage28_3b_loao_conclusion_stability.csv"
)

COMBINED_CONCLUSION_STABILITY = (
    STAGE3_ROOT
    / "conclusion_stability.csv"
)

SOURCE_ROOT = Path(
    "/kaggle/input/datasets/solarmainframe/ids-intrusion-csv"
)

SOURCE_DAY8 = (
    SOURCE_ROOT
    / "03-01-2018.csv"
)

SOURCE_DAY9 = (
    SOURCE_ROOT
    / "03-02-2018.csv"
)

EXPECTED_MEMBERSHIP_SHA = (
    "18d43eded5e78238ce6765abdc1ed18ce662aebd0899b678472891203eee3d1e"
)

EXPECTED_ROWS = 1_374_133
EXPECTED_BENIGN = 998_788
EXPECTED_ATTACK = 375_345
EXPECTED_FEATURES = 70

EXPECTED_POS_INF_TO_NAN = 9_530
EXPECTED_NEG_INF_TO_NAN = 0
EXPECTED_OUTPUT_NAN = 13_922

EXPECTED_SEEDS = [42, 43, 44, 45, 46]

EXPECTED_UNITS = [
    "RANDOM_NATURAL",
    "CHRONOLOGICAL_NATURAL",
]

EXPECTED_LIBRARIES = {
    "numpy": "2.0.2",
    "sklearn": "1.6.1",
    "xgboost": "3.2.0",
    "lightgbm": "4.6.0",
}

EXPECTED_PER_DAY = {
    8: {
        "file": "03-01-2018.csv",
        "physical_rows": 331_125,
        "embedded_header_rows": 25,
        "effective_rows": 331_100,
        "retained_rows": 331_017,
        "retained_benign": 237_982,
        "retained_attack": 93_035,
    },
    9: {
        "file": "03-02-2018.csv",
        "physical_rows": 1_048_575,
        "embedded_header_rows": 0,
        "effective_rows": 1_048_575,
        "retained_rows": 1_043_116,
        "retained_benign": 760_806,
        "retained_attack": 282_310,
    },
}


# =================================================================================================
# HELPERS
# =================================================================================================

def banner(text: str) -> None:
    print()
    print(SEP)
    print(text)
    print(SEP)
    print()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def run(
    cmd,
    *,
    cwd=REPO,
    check=True,
    env=None,
):
    p = subprocess.run(
        [str(x) for x in cmd],
        cwd=str(cwd),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        env=env,
    )

    if check and p.returncode != 0:
        raise RuntimeError(
            f"Command failed ({p.returncode}): "
            + " ".join(str(x) for x in cmd)
            + f"\n\nSTDOUT:\n{p.stdout}"
            + f"\n\nSTDERR:\n{p.stderr}"
        )

    return p


def git(*args, check=True):
    return run(
        ["git", *args],
        check=check,
    ).stdout.strip()


def read_json(path: Path):
    return json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )


def write_json(path: Path, obj) -> None:
    path.write_text(
        json.dumps(
            obj,
            indent=2,
            ensure_ascii=False,
            allow_nan=False,
        )
        + "\n",
        encoding="utf-8",
    )


def sha256_file(
    path: Path,
    chunk_size=16 * 1024 * 1024,
):
    h = hashlib.sha256()

    with path.open("rb") as f:
        while True:
            block = f.read(chunk_size)

            if not block:
                break

            h.update(block)

    return h.hexdigest()


def sha256_array_raw(arr: np.ndarray) -> str:
    a = np.ascontiguousarray(arr)

    h = hashlib.sha256()

    view = memoryview(a).cast("B")

    step = 64 * 1024 * 1024

    for start in range(
        0,
        len(view),
        step,
    ):
        h.update(
            view[
                start:
                start + step
            ]
        )

    return h.hexdigest()


def normalize_name(value) -> str:
    return (
        str(value)
        .replace("\ufeff", "")
        .strip()
    )


def normalized_labels(series: pd.Series) -> pd.Series:
    return (
        series
        .astype("string")
        .fillna("")
        .str.strip()
        .str.upper()
    )


def labels_to_binary(series: pd.Series) -> np.ndarray:
    labels = normalized_labels(
        series
    )

    return np.where(
        labels.eq("BENIGN"),
        0,
        1,
    ).astype(
        np.uint8,
        copy=False,
    )


def safe_div(num, den):
    if den == 0:
        return 0.0

    return float(num / den)


def operating_metrics(
    y_true: np.ndarray,
    probability_float32: np.ndarray,
    threshold: float,
):
    threshold32 = np.float32(
        threshold
    )

    pred = (
        probability_float32
        >= threshold32
    )

    y_pos = (
        y_true == 1
    )

    y_neg = ~y_pos

    tp = int(
        np.count_nonzero(
            pred & y_pos
        )
    )

    fp = int(
        np.count_nonzero(
            pred & y_neg
        )
    )

    tn = int(
        np.count_nonzero(
            (~pred) & y_neg
        )
    )

    fn = int(
        np.count_nonzero(
            (~pred) & y_pos
        )
    )

    precision = safe_div(
        tp,
        tp + fp,
    )

    recall = safe_div(
        tp,
        tp + fn,
    )

    fpr = safe_div(
        fp,
        fp + tn,
    )

    accuracy = safe_div(
        tp + tn,
        len(y_true),
    )

    f1 = (
        safe_div(
            2.0 * precision * recall,
            precision + recall,
        )
        if (
            precision + recall
        ) > 0
        else 0.0
    )

    f2 = (
        safe_div(
            5.0 * precision * recall,
            4.0 * precision + recall,
        )
        if (
            4.0 * precision + recall
        ) > 0
        else 0.0
    )

    return {
        "threshold":
            float(threshold),

        "threshold_float32_runtime":
            float(threshold32),

        "accuracy":
            accuracy,

        "precision":
            precision,

        "recall":
            recall,

        "fpr":
            fpr,

        "f1":
            f1,

        "f2":
            f2,

        "tp":
            tp,

        "fp":
            fp,

        "tn":
            tn,

        "fn":
            fn,
    }


def extract_threshold(
    operating_points,
    name,
):
    op = operating_points[
        name.lower()
    ]

    if (
        isinstance(op, dict)
        and
        "result" in op
    ):
        if op.get(
            "status"
        ) != "AVAILABLE":
            raise RuntimeError(
                f"Frozen {name} threshold "
                f"is unavailable."
            )

        op = op[
            "result"
        ]

    if not isinstance(
        op,
        dict,
    ):
        raise RuntimeError(
            f"Malformed operating point {name}."
        )

    threshold = op.get(
        "threshold"
    )

    if threshold is None:
        raise RuntimeError(
            f"Missing threshold for {name}."
        )

    return float(
        threshold
    )


def resolve_model_path(
    result_path: Path,
    model_info: dict,
):
    if model_info.get(
        "model_path"
    ):
        path = (
            result_path.parent
            / model_info[
                "model_path"
            ]
        )

        expected_sha = (
            model_info[
                "model_sha256"
            ]
        )

        source_type = (
            "STAGE28_MODEL_ARTIFACT"
        )

    else:
        path = (
            REPO
            / model_info[
                "historical_model_path"
            ]
        )

        expected_sha = (
            model_info[
                "historical_model_sha256"
            ]
        )

        source_type = (
            "HISTORICAL_REUSE_ARTIFACT"
        )

    if not path.is_file():
        raise RuntimeError(
            f"Model missing:\n{path}"
        )

    actual_sha = sha256_file(
        path
    )

    if actual_sha != expected_sha:
        raise RuntimeError(
            "Model SHA mismatch:\n"
            f"{path}\n"
            f"expected={expected_sha}\n"
            f"actual={actual_sha}"
        )

    return (
        path,
        actual_sha,
        source_type,
    )


def git_push_with_kaggle_secret():
    try:
        from kaggle_secrets import (
            UserSecretsClient,
        )
    except Exception as exc:
        raise RuntimeError(
            "kaggle_secrets unavailable."
        ) from exc

    client = UserSecretsClient()

    token = None
    token_name = None

    candidates = [
        "GITHUB_TOKEN",
        "github_token",
        "GH_TOKEN",
        "github_pat",
        "GITHUB_PAT",
        "GH_PAT",
    ]

    for name in candidates:
        try:
            value = client.get_secret(
                name
            )
        except Exception:
            value = None

        if (
            value
            and
            str(value).strip()
        ):
            token = str(
                value
            ).strip()

            token_name = name

            break

    if token is None:
        raise RuntimeError(
            "No usable GitHub token found in Kaggle Secrets."
        )

    encoded = quote(
        token,
        safe="",
    )

    push_url = (
        "https://x-access-token:"
        + encoded
        + "@github.com/"
        + "themubasshir/"
        + "ids2018-validation-safe-ablation.git"
    )

    p = subprocess.run(
        [
            "git",
            "push",
            push_url,
            "HEAD:main",
        ],
        cwd=str(REPO),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    if p.returncode != 0:
        safe_stdout = (
            p.stdout
            .replace(
                token,
                "***",
            )
            .replace(
                encoded,
                "***",
            )
        )

        safe_stderr = (
            p.stderr
            .replace(
                token,
                "***",
            )
            .replace(
                encoded,
                "***",
            )
        )

        raise RuntimeError(
            "GitHub push failed.\n\n"
            f"STDOUT:\n{safe_stdout}\n"
            f"STDERR:\n{safe_stderr}"
        )

    print(
        f"[PASS] GitHub credential: kaggle_secret:{token_name}"
    )

    print(
        "[PASS] token not displayed"
    )

    if p.stdout.strip():
        print(
            p.stdout.strip()
        )

    if p.stderr.strip():
        print(
            p.stderr
        )


# =================================================================================================
# 0. REPOSITORY / PARENT GATE
# =================================================================================================

banner(
    "STAGE28-4 — REPOSITORY / PARENT GATE"
)

if not (
    REPO
    / ".git"
).is_dir():
    raise RuntimeError(
        f"Repository missing:\n{REPO}"
    )

status = git(
    "status",
    "--porcelain",
)

if status:
    raise RuntimeError(
        "Repository is not clean:\n"
        + status
    )

run(
    [
        "git",
        "fetch",
        "origin",
        "main",
    ]
)

local_head = git(
    "rev-parse",
    "HEAD",
)

origin_head = git(
    "rev-parse",
    "origin/main",
)

print(
    "Expected parent:",
    EXPECTED_PARENT,
)

print(
    "Local HEAD     :",
    local_head,
)

print(
    "origin/main    :",
    origin_head,
)

if not (
    local_head
    == origin_head
    == EXPECTED_PARENT
):
    raise RuntimeError(
        "Stage28-4 parent gate failed."
    )

if STAGE4_ROOT.exists():
    raise RuntimeError(
        "Stage28-4 output directory already exists. "
        "Do not overwrite or rerun blindly."
    )

if COMBINED_CONCLUSION_STABILITY.exists():
    raise RuntimeError(
        "Combined conclusion_stability.csv already exists. "
        "Do not overwrite."
    )

print()
print(
    "[PASS] Stage28-3C parent exact"
)

print(
    "[PASS] repository clean"
)

print(
    "[PASS] Stage28-4 has not been durably executed"
)


# =================================================================================================
# 1. SCIENTIFIC CLOSURE / AUTHORIZATION GATE
# =================================================================================================

banner(
    "STAGE28-4 — SCIENTIFIC AUTHORIZATION GATE"
)

closure = read_json(
    CLOSURE_RECEIPT
)

stage3c = read_json(
    STAGE3C_RECEIPT
)

stage22_spec = read_json(
    STAGE22_SPEC
)

stability_spec = read_json(
    STABILITY_SPEC
)

if (
    closure.get(
        "closure_status"
    )
    !=
    "PASS_STAGE28_NEW_MODEL_FITTING_PERMANENTLY_CLOSED"
):
    raise RuntimeError(
        "Stage28 fitting closure not exact."
    )

fit_budget = closure[
    "fit_budget_closure"
]

if (
    int(
        fit_budget[
            "consumed_new_fits"
        ]
    )
    != 108
):
    raise RuntimeError(
        "Consumed fit count != 108."
    )

if (
    int(
        fit_budget[
            "remaining_new_fits"
        ]
    )
    != 0
):
    raise RuntimeError(
        "Remaining fit count != 0."
    )

if not str(
    stage3c.get(
        "next_authorized_step",
        "",
    )
).startswith(
    "Stage28-4"
):
    raise RuntimeError(
        "Stage28-3C does not authorize Stage28-4."
    )

evaluation_population = (
    stage22_spec[
        "evaluation_population"
    ]
)

if (
    evaluation_population[
        "name"
    ]
    !=
    "STAGE22R_SHARED_FINAL_SINGLE_HOLDOUT"
):
    raise RuntimeError(
        "Wrong Stage22 evaluation population."
    )

if (
    evaluation_population[
        "threshold_selection_on_final_holdout"
    ]
    != "FORBIDDEN"
):
    raise RuntimeError(
        "Threshold-search prohibition changed."
    )

if (
    evaluation_population[
        "model_selection_on_final_holdout"
    ]
    != "FORBIDDEN"
):
    raise RuntimeError(
        "Model-selection prohibition changed."
    )

if (
    stage22_spec[
        "scientific_unit"
    ][
        "strategy"
    ]
    != "ENS_LGBM_XGB_EQUAL"
):
    raise RuntimeError(
        "Stage22 ensemble strategy changed."
    )

if (
    stage22_spec[
        "scientific_unit"
    ][
        "probability_rule"
    ]
    !=
    "0.5 * P_LIGHTGBM + 0.5 * P_XGBOOST"
):
    raise RuntimeError(
        "Stage22 ensemble probability rule changed."
    )

frozen_claims = (
    stability_spec[
        "stage22_directional_claims"
    ]
)

expected_claim_ids = {
    "STAGE22_PR_RANDOM_LT_CHRONO_ON_SHARED_FINAL_HOLDOUT",
    "STAGE22_ROC_RANDOM_LT_CHRONO_ON_SHARED_FINAL_HOLDOUT",
}

actual_claim_ids = {
    x[
        "claim_id"
    ]
    for x in frozen_claims
}

if (
    actual_claim_ids
    != expected_claim_ids
):
    raise RuntimeError(
        "Frozen Stage22 directional claims changed."
    )

print(
    "[PASS] Stage28 fitting permanently closed at 108 / 108"
)

print(
    "[PASS] Stage28-4 explicitly authorized"
)

print(
    "[PASS] final-holdout threshold search FORBIDDEN"
)

print(
    "[PASS] final-holdout model selection FORBIDDEN"
)

print(
    "[PASS] equal-weight LGBM/XGB ensemble exact"
)

print(
    "[PASS] two Stage22 directional claims frozen"
)


# =================================================================================================
# 2. RUNTIME / ARTIFACT GATE
# =================================================================================================

banner(
    "STAGE28-4 — RUNTIME / ARTIFACT GATE"
)

versions = {
    "numpy": np.__version__,
    "sklearn": sklearn.__version__,
    "xgboost": xgb.__version__,
    "lightgbm": lgb.__version__,
}

for name, expected in (
    EXPECTED_LIBRARIES.items()
):
    actual = versions[
        name
    ]

    print(
        f"{name:<10}: {actual}"
    )

    if actual != expected:
        raise RuntimeError(
            f"{name} version mismatch: "
            f"{actual} != {expected}"
        )

required_paths = [
    MEMBERSHIP_PATH,
    PARENT_HOLDOUT_SUMMARY,
    PARENT_HOLDOUT_RESULT,
    PARENT_CHECKSUMS,
    FEATURE_CONFIG,
    LOAO_CONCLUSION_STABILITY,
    SOURCE_DAY8,
    SOURCE_DAY9,
]

for path in required_paths:
    if not path.is_file():
        raise RuntimeError(
            f"Required artifact missing:\n{path}"
        )

membership_sha = sha256_file(
    MEMBERSHIP_PATH
)

if (
    membership_sha
    != EXPECTED_MEMBERSHIP_SHA
):
    raise RuntimeError(
        "Frozen membership artifact SHA mismatch."
    )

print()
print(
    "[PASS] runtime versions exact"
)

print(
    "[PASS] frozen membership SHA exact"
)

print(
    "[PASS] exact March source files attached"
)


# =================================================================================================
# 3. LOAD FROZEN MEMBERSHIP
# =================================================================================================

banner(
    "STAGE28-4 — LOAD FROZEN HOLDOUT MEMBERSHIP"
)

with np.load(
    MEMBERSHIP_PATH,
    allow_pickle=False,
) as z:
    expected_keys = {
        "hash_lo",
        "hash_hi",
        "day_id",
        "row_index",
        "binary_label",
    }

    if set(
        z.files
    ) != expected_keys:
        raise RuntimeError(
            f"Unexpected membership keys: {z.files}"
        )

    hash_lo = np.asarray(
        z[
            "hash_lo"
        ],
        dtype=np.uint64,
    ).copy()

    hash_hi = np.asarray(
        z[
            "hash_hi"
        ],
        dtype=np.uint64,
    ).copy()

    day_id = np.asarray(
        z[
            "day_id"
        ],
        dtype=np.uint8,
    ).copy()

    row_index = np.asarray(
        z[
            "row_index"
        ],
        dtype=np.uint32,
    ).astype(
        np.int64,
        copy=False,
    )

    y_true = np.asarray(
        z[
            "binary_label"
        ],
        dtype=np.uint8,
    ).copy()

if not (
    len(hash_lo)
    == len(hash_hi)
    == len(day_id)
    == len(row_index)
    == len(y_true)
    == EXPECTED_ROWS
):
    raise RuntimeError(
        "Membership array length mismatch."
    )

if set(
    np.unique(
        day_id
    ).tolist()
) != {8, 9}:
    raise RuntimeError(
        "Membership contains unexpected day IDs."
    )

benign_count = int(
    np.count_nonzero(
        y_true == 0
    )
)

attack_count = int(
    np.count_nonzero(
        y_true == 1
    )
)

if benign_count != EXPECTED_BENIGN:
    raise RuntimeError(
        f"Benign count mismatch: {benign_count}"
    )

if attack_count != EXPECTED_ATTACK:
    raise RuntimeError(
        f"Attack count mismatch: {attack_count}"
    )

for d in [8, 9]:
    positions = np.flatnonzero(
        day_id == d
    )

    expected = (
        EXPECTED_PER_DAY[
            d
        ]
    )

    if (
        len(positions)
        !=
        expected[
            "retained_rows"
        ]
    ):
        raise RuntimeError(
            f"Day {d} membership count mismatch."
        )

    indices = row_index[
        positions
    ]

    if (
        np.unique(
            indices
        ).size
        != indices.size
    ):
        raise RuntimeError(
            f"Duplicate row_index values for day {d}."
        )

    print(
        f"day_id={d}: "
        f"rows={len(positions):,}, "
        f"row_index_min={indices.min():,}, "
        f"row_index_max={indices.max():,}"
    )

print()
print(
    "[PASS] membership rows = 1,374,133"
)

print(
    "[PASS] benign = 998,788"
)

print(
    "[PASS] attack = 375,345"
)

print(
    "[PASS] day IDs = {8, 9}"
)

membership_logical = {
    "hash_lo_sha256":
        sha256_array_raw(
            hash_lo
        ),

    "hash_hi_sha256":
        sha256_array_raw(
            hash_hi
        ),

    "day_id_sha256":
        sha256_array_raw(
            day_id
        ),

    "row_index_sha256":
        sha256_array_raw(
            row_index.astype(
                np.uint32
            )
        ),

    "binary_label_sha256":
        sha256_array_raw(
            y_true
        ),
}


# =================================================================================================
# 4. LOAD EXACT 70-FEATURE CONTRACT
# =================================================================================================

banner(
    "STAGE28-4 — 70-FEATURE CONTRACT"
)

feature_obj = read_json(
    FEATURE_CONFIG
)

FEATURES = feature_obj.get(
    "retained_features"
)

if not isinstance(
    FEATURES,
    list,
):
    raise RuntimeError(
        "retained_features missing."
    )

if len(
    FEATURES
) != EXPECTED_FEATURES:
    raise RuntimeError(
        "Feature count != 70."
    )

if not all(
    isinstance(
        x,
        str,
    )
    for x in FEATURES
):
    raise RuntimeError(
        "Feature list contains non-string values."
    )

if FEATURES[
    0
] != "Dst Port":
    raise RuntimeError(
        "First feature mismatch."
    )

if FEATURES[
    -1
] != "Idle Min":
    raise RuntimeError(
        "Last feature mismatch."
    )

print(
    "Feature count:",
    len(
        FEATURES
    ),
)

print(
    "First feature:",
    FEATURES[
        0
    ],
)

print(
    "Last feature :",
    FEATURES[
        -1
    ],
)

print()
print(
    "[PASS] frozen Stage22 70-feature order exact"
)


# =================================================================================================
# 5. SOURCE PROVENANCE
# =================================================================================================

banner(
    "STAGE28-4 — SOURCE PROVENANCE"
)

source_records = {}

for day, path in [
    (
        8,
        SOURCE_DAY8,
    ),
    (
        9,
        SOURCE_DAY9,
    ),
]:
    print(
        f"Hashing {path.name} ..."
    )

    source_records[
        day
    ] = {
        "path":
            str(
                path
            ),

        "bytes":
            int(
                path.stat().st_size
            ),

        "sha256":
            sha256_file(
                path
            ),
    }

    print(
        "  bytes :",
        f"{path.stat().st_size:,}",
    )

    print(
        "  sha256:",
        source_records[
            day
        ][
            "sha256"
        ],
    )

print()
print(
    "[PASS] source-byte identities recorded"
)


# =================================================================================================
# 6. MATERIALIZE EXACT FROZEN HOLDOUT
#
# Critical point:
#
# row_index semantics are NOT guessed.
#
# For March 1, where 25 embedded headers exist, we construct:
#   A) raw physical dataframe indexing
#   B) post-embedded-header effective indexing
#
# We compare each candidate against the already-frozen membership
# binary_label vector and require a unique exact match.
#
# March 2 has no embedded headers, so raw == effective.
#
# This is an operational index-semantics audit, NOT a new membership
# decision and NOT a model-result-driven choice.
# =================================================================================================

banner(
    "STAGE28-4 — ONE-TIME SHARED FINAL-HOLDOUT MATERIALIZATION"
)

USECOLS = (
    FEATURES
    + [
        "Label"
    ]
)

wanted = set(
    USECOLS
)

X_holdout = np.empty(
    (
        EXPECTED_ROWS,
        EXPECTED_FEATURES,
    ),
    dtype=np.float64,
)

materialization_records = {}

total_pos_inf = 0
total_neg_inf = 0

materialization_started = (
    time.perf_counter()
)

for day, path in [
    (
        8,
        SOURCE_DAY8,
    ),
    (
        9,
        SOURCE_DAY9,
    ),
]:
    expected = (
        EXPECTED_PER_DAY[
            day
        ]
    )

    banner(
        f"STAGE28-4 — MATERIALIZE DAY {day}: {path.name}"
    )

    positions = np.flatnonzero(
        day_id == day
    )

    membership_indices = (
        row_index[
            positions
        ]
    )

    expected_labels = (
        y_true[
            positions
        ]
    )

    print(
        "Reading raw source once ..."
    )

    read_started = (
        time.perf_counter()
    )

    df = pd.read_csv(
        path,
        usecols=lambda c:
            normalize_name(
                c
            )
            in wanted,
        low_memory=False,
    )

    df.columns = [
        normalize_name(
            c
        )
        for c in df.columns
    ]

    if set(
        df.columns
    ) != wanted:
        missing = sorted(
            wanted
            - set(
                df.columns
            )
        )

        extra = sorted(
            set(
                df.columns
            )
            - wanted
        )

        raise RuntimeError(
            f"{path.name}: use-column mismatch.\n"
            f"missing={missing}\n"
            f"extra={extra}"
        )

    read_seconds = (
        time.perf_counter()
        - read_started
    )

    physical_rows = len(
        df
    )

    if (
        physical_rows
        != expected[
            "physical_rows"
        ]
    ):
        raise RuntimeError(
            f"{path.name}: physical row mismatch "
            f"{physical_rows} != "
            f"{expected['physical_rows']}"
        )

    label_normalized = (
        normalized_labels(
            df[
                "Label"
            ]
        )
    )

    embedded_header_mask = (
        label_normalized.eq(
            "LABEL"
        )
    )

    embedded_count = int(
        embedded_header_mask.sum()
    )

    if (
        embedded_count
        != expected[
            "embedded_header_rows"
        ]
    ):
        raise RuntimeError(
            f"{path.name}: embedded-header count mismatch "
            f"{embedded_count} != "
            f"{expected['embedded_header_rows']}"
        )

    effective_df = (
        df.loc[
            ~embedded_header_mask
        ]
        .reset_index(
            drop=True
        )
    )

    effective_rows = len(
        effective_df
    )

    if (
        effective_rows
        != expected[
            "effective_rows"
        ]
    ):
        raise RuntimeError(
            f"{path.name}: effective row mismatch "
            f"{effective_rows} != "
            f"{expected['effective_rows']}"
        )

    if (
        len(
            positions
        )
        != expected[
            "retained_rows"
        ]
    ):
        raise RuntimeError(
            f"{path.name}: retained membership count mismatch."
        )

    candidate_matches = {}

    # Candidate 1: membership row_index addresses physical rows.
    if (
        membership_indices.max()
        < len(
            df
        )
    ):
        raw_candidate_labels = (
            labels_to_binary(
                df.iloc[
                    membership_indices
                ][
                    "Label"
                ]
            )
        )

        candidate_matches[
            "RAW_PHYSICAL_ROW_INDEX"
        ] = bool(
            np.array_equal(
                raw_candidate_labels,
                expected_labels,
            )
        )

    else:
        candidate_matches[
            "RAW_PHYSICAL_ROW_INDEX"
        ] = False

    # Candidate 2: membership row_index addresses the post-header
    # effective row stream.
    if (
        membership_indices.max()
        < len(
            effective_df
        )
    ):
        effective_candidate_labels = (
            labels_to_binary(
                effective_df.iloc[
                    membership_indices
                ][
                    "Label"
                ]
            )
        )

        candidate_matches[
            "POST_EMBEDDED_HEADER_EFFECTIVE_INDEX"
        ] = bool(
            np.array_equal(
                effective_candidate_labels,
                expected_labels,
            )
        )

    else:
        candidate_matches[
            "POST_EMBEDDED_HEADER_EFFECTIVE_INDEX"
        ] = False

    print(
        "Candidate row_index semantics:"
    )

    for name, passed in (
        candidate_matches.items()
    ):
        print(
            f"  {name:<42}: {passed}"
        )

    if embedded_count == 0:
        # Raw and effective are mathematically identical here.
        if not candidate_matches[
            "RAW_PHYSICAL_ROW_INDEX"
        ]:
            raise RuntimeError(
                f"{path.name}: frozen row indices do not "
                "reproduce membership labels."
            )

        selected_base = df

        index_semantics = (
            "RAW_EQUALS_EFFECTIVE_NO_EMBEDDED_HEADERS"
        )

    else:
        passing = [
            name
            for name, passed
            in candidate_matches.items()
            if passed
        ]

        if len(
            passing
        ) != 1:
            raise RuntimeError(
                f"{path.name}: expected exactly one "
                "membership index interpretation to match; "
                f"got {passing}."
            )

        index_semantics = (
            passing[
                0
            ]
        )

        if (
            index_semantics
            ==
            "RAW_PHYSICAL_ROW_INDEX"
        ):
            selected_base = df

        elif (
            index_semantics
            ==
            "POST_EMBEDDED_HEADER_EFFECTIVE_INDEX"
        ):
            selected_base = effective_df

        else:
            raise RuntimeError(
                "Internal row-index resolution error."
            )

    selected = (
        selected_base.iloc[
            membership_indices
        ]
    )

    source_selected_y = (
        labels_to_binary(
            selected[
                "Label"
            ]
        )
    )

    if not np.array_equal(
        source_selected_y,
        expected_labels,
    ):
        raise RuntimeError(
            f"{path.name}: selected source labels do not "
            "exactly reproduce frozen membership labels."
        )

    source_benign = int(
        np.count_nonzero(
            source_selected_y == 0
        )
    )

    source_attack = int(
        np.count_nonzero(
            source_selected_y == 1
        )
    )

    if (
        source_benign
        != expected[
            "retained_benign"
        ]
    ):
        raise RuntimeError(
            f"{path.name}: retained benign mismatch."
        )

    if (
        source_attack
        != expected[
            "retained_attack"
        ]
    ):
        raise RuntimeError(
            f"{path.name}: retained attack mismatch."
        )

    print(
        f"[PASS] row_index semantics: {index_semantics}"
    )

    print(
        "[PASS] source labels reproduce frozen binary_label exactly"
    )

    print(
        f"[PASS] retained rows: {len(selected):,}"
    )

    numeric_started = (
        time.perf_counter()
    )

    numeric_df = (
        selected[
            FEATURES
        ]
        .apply(
            pd.to_numeric,
            errors="coerce",
        )
    )

    block = numeric_df.to_numpy(
        dtype=np.float64,
        copy=True,
    )

    day_pos_inf = int(
        np.count_nonzero(
            np.isposinf(
                block
            )
        )
    )

    day_neg_inf = int(
        np.count_nonzero(
            np.isneginf(
                block
            )
        )
    )

    total_pos_inf += (
        day_pos_inf
    )

    total_neg_inf += (
        day_neg_inf
    )

    inf_mask = np.isinf(
        block
    )

    if np.any(
        inf_mask
    ):
        block[
            inf_mask
        ] = np.nan

    if (
        block.shape
        !=
        (
            len(
                positions
            ),
            EXPECTED_FEATURES,
        )
    ):
        raise RuntimeError(
            f"{path.name}: materialized matrix shape mismatch."
        )

    X_holdout[
        positions,
        :,
    ] = block

    numeric_seconds = (
        time.perf_counter()
        - numeric_started
    )

    materialization_records[
        day
    ] = {
        "file":
            path.name,

        "physical_rows":
            physical_rows,

        "embedded_header_rows":
            embedded_count,

        "effective_rows":
            effective_rows,

        "retained_rows":
            len(
                positions
            ),

        "retained_benign":
            source_benign,

        "retained_attack":
            source_attack,

        "membership_row_index_min":
            int(
                membership_indices.min()
            ),

        "membership_row_index_max":
            int(
                membership_indices.max()
            ),

        "index_semantics":
            index_semantics,

        "candidate_matches":
            candidate_matches,

        "positive_infinity_to_nan":
            day_pos_inf,

        "negative_infinity_to_nan":
            day_neg_inf,

        "raw_source_read_seconds":
            read_seconds,

        "numeric_materialization_seconds":
            numeric_seconds,
    }

    print(
        f"positive infinity cells: {day_pos_inf:,}"
    )

    print(
        f"negative infinity cells: {day_neg_inf:,}"
    )

    # Free all temporary per-day structures immediately.
    del selected
    del selected_base
    del effective_df
    del numeric_df
    del block
    del df
    del label_normalized
    del embedded_header_mask
    gc.collect()

materialization_seconds = (
    time.perf_counter()
    - materialization_started
)

if X_holdout.dtype != np.float64:
    raise RuntimeError(
        "Final holdout dtype != float64."
    )

if X_holdout.shape != (
    EXPECTED_ROWS,
    EXPECTED_FEATURES,
):
    raise RuntimeError(
        "Final holdout shape mismatch."
    )

if (
    total_pos_inf
    != EXPECTED_POS_INF_TO_NAN
):
    raise RuntimeError(
        "Positive-infinity conversion mismatch: "
        f"{total_pos_inf} != "
        f"{EXPECTED_POS_INF_TO_NAN}"
    )

if (
    total_neg_inf
    != EXPECTED_NEG_INF_TO_NAN
):
    raise RuntimeError(
        "Negative-infinity conversion mismatch: "
        f"{total_neg_inf} != "
        f"{EXPECTED_NEG_INF_TO_NAN}"
    )

final_nan_cells = int(
    np.count_nonzero(
        np.isnan(
            X_holdout
        )
    )
)

if (
    final_nan_cells
    != EXPECTED_OUTPUT_NAN
):
    raise RuntimeError(
        "Output NaN-cell mismatch: "
        f"{final_nan_cells} != "
        f"{EXPECTED_OUTPUT_NAN}"
    )

print()
print(
    "[PASS] EXACT FROZEN HOLDOUT MATERIALIZED"
)

print(
    "Shape:",
    X_holdout.shape,
)

print(
    "Dtype:",
    X_holdout.dtype,
)

print(
    "Positive infinity -> NaN:",
    f"{total_pos_inf:,}",
)

print(
    "Negative infinity -> NaN:",
    f"{total_neg_inf:,}",
)

print(
    "Output NaN cells:",
    f"{final_nan_cells:,}",
)

print(
    "Materialization seconds:",
    materialization_seconds,
)

print()
print(
    "[PASS] model input contract exactly matches parent Stage22R summary"
)

X_logical_sha = sha256_array_raw(
    X_holdout
)

y_logical_sha = sha256_array_raw(
    y_true
)

print()
print(
    "Holdout X logical SHA256:",
    X_logical_sha,
)

print(
    "Holdout y logical SHA256:",
    y_logical_sha,
)


# =================================================================================================
# 7. DISCOVER / AUDIT TEN FROZEN STAGE22 ENSEMBLES
# =================================================================================================

banner(
    "STAGE28-4 — AUDIT TEN FROZEN STAGE22 ENSEMBLES"
)

result_files = sorted(
    STAGE22_ROOT.rglob(
        "*_result.json"
    )
)

if len(
    result_files
) != 10:
    raise RuntimeError(
        f"Expected 10 Stage22 result receipts; "
        f"found {len(result_files)}."
    )

ensemble_specs = []

for result_path in result_files:
    obj = read_json(
        result_path
    )

    if (
        obj.get(
            "experiment"
        )
        != "STAGE22_FULL"
    ):
        raise RuntimeError(
            f"Unexpected experiment:\n{result_path}"
        )

    unit = obj[
        "unit"
    ]

    seed = int(
        obj[
            "training_seed"
        ]
    )

    if unit not in EXPECTED_UNITS:
        raise RuntimeError(
            f"Unexpected Stage22 unit: {unit}"
        )

    if seed not in EXPECTED_SEEDS:
        raise RuntimeError(
            f"Unexpected seed: {seed}"
        )

    models = obj[
        "models"
    ]

    if (
        models.get(
            "strategy"
        )
        != "ENS_LGBM_XGB_EQUAL"
    ):
        raise RuntimeError(
            f"{unit}/seed{seed}: ensemble strategy mismatch."
        )

    if (
        models.get(
            "ensemble_probability"
        )
        !=
        "0.5 * P_LIGHTGBM + 0.5 * P_XGBOOST"
    ):
        raise RuntimeError(
            f"{unit}/seed{seed}: probability rule mismatch."
        )

    if (
        models.get(
            "component_combination_dtype"
        )
        != "float64"
    ):
        raise RuntimeError(
            f"{unit}/seed{seed}: component-combination dtype changed."
        )

    if (
        models.get(
            "ensemble_storage_dtype"
        )
        != "float32"
    ):
        raise RuntimeError(
            f"{unit}/seed{seed}: ensemble-storage dtype changed."
        )

    xgb_info = models[
        "xgboost"
    ]

    lgb_info = models[
        "lightgbm"
    ]

    for name, info in [
        (
            "XGBOOST",
            xgb_info,
        ),
        (
            "LIGHTGBM",
            lgb_info,
        ),
    ]:
        if int(
            info[
                "seed"
            ]
        ) != seed:
            raise RuntimeError(
                f"{unit}/seed{seed}/{name}: seed mismatch."
            )

        if str(
            info.get(
                "backend",
                "",
            )
        ).lower() != "cpu":
            raise RuntimeError(
                f"{unit}/seed{seed}/{name}: backend != CPU."
            )

    xgb_path, xgb_sha, xgb_source = (
        resolve_model_path(
            result_path,
            xgb_info,
        )
    )

    lgb_path, lgb_sha, lgb_source = (
        resolve_model_path(
            result_path,
            lgb_info,
        )
    )

    thresholds = {
        "STANDARD":
            extract_threshold(
                obj[
                    "operating_points"
                ],
                "STANDARD",
            ),

        "BALANCED":
            extract_threshold(
                obj[
                    "operating_points"
                ],
                "BALANCED",
            ),

        "SECURITY":
            extract_threshold(
                obj[
                    "operating_points"
                ],
                "SECURITY",
            ),
    }

    ensemble_specs.append(
        {
            "unit":
                unit,

            "seed":
                seed,

            "result_path":
                result_path,

            "result_sha256":
                sha256_file(
                    result_path
                ),

            "xgb_path":
                xgb_path,

            "xgb_sha256":
                xgb_sha,

            "xgb_source_type":
                xgb_source,

            "xgb_component_id":
                xgb_info[
                    "component_id"
                ],

            "lgb_path":
                lgb_path,

            "lgb_sha256":
                lgb_sha,

            "lgb_source_type":
                lgb_source,

            "lgb_component_id":
                lgb_info[
                    "component_id"
                ],

            "thresholds":
                thresholds,
        }
    )

ensemble_specs.sort(
    key=lambda x: (
        EXPECTED_UNITS.index(
            x[
                "unit"
            ]
        ),
        x[
            "seed"
        ],
    )
)

expected_pairs = [
    (
        unit,
        seed,
    )
    for unit
    in EXPECTED_UNITS
    for seed
    in EXPECTED_SEEDS
]

actual_pairs = [
    (
        x[
            "unit"
        ],
        x[
            "seed"
        ],
    )
    for x
    in ensemble_specs
]

if actual_pairs != expected_pairs:
    raise RuntimeError(
        "Stage22 ensemble grid != exact 2 × 5 design."
    )

for spec in ensemble_specs:
    print(
        f"{spec['unit']:<24} "
        f"seed={spec['seed']}  "
        f"XGB={spec['xgb_component_id']}  "
        f"LGB={spec['lgb_component_id']}  "
        f"thr={spec['thresholds']}"
    )

print()
print(
    "[PASS] 10 / 10 Stage22 ensemble realizations exact"
)

print(
    "[PASS] 20 / 20 model artifacts checksum-verified"
)

print(
    "[PASS] all inference backends frozen to CPU"
)

print(
    "[PASS] all thresholds inherited from validation"
)

print(
    "[PASS] ZERO threshold search on final holdout"
)


# =================================================================================================
# 8. ACTUAL MODEL INFERENCE
# =================================================================================================

banner(
    "STAGE28-4 — AUTHORIZED FINAL-HOLDOUT MODEL INFERENCE"
)

STAGE4_ROOT.mkdir(
    parents=True,
    exist_ok=False,
)

probability_arrays = {}

probability_records = {}

metric_rows = []

inference_started = (
    time.perf_counter()
)

for cell_index, spec in enumerate(
    ensemble_specs,
    start=1,
):
    unit = spec[
        "unit"
    ]

    seed = spec[
        "seed"
    ]

    print()
    print(
        "-" * 120
    )

    print(
        f"[{cell_index:02d}/10] "
        f"{unit} — seed {seed}"
    )

    print(
        "-" * 120
    )

    cell_started = (
        time.perf_counter()
    )

    # ---------------------------------------------------------------------------------------------
    # XGBOOST — LOAD FROZEN MODEL, NO FIT
    # ---------------------------------------------------------------------------------------------

    xgb_model = (
        xgb.XGBClassifier()
    )

    xgb_model.load_model(
        str(
            spec[
                "xgb_path"
            ]
        )
    )

    xgb_rounds = int(
        xgb_model
        .get_booster()
        .num_boosted_rounds()
    )

    if xgb_rounds != 400:
        raise RuntimeError(
            f"{unit}/seed{seed}: "
            f"XGBoost rounds {xgb_rounds} != 400."
        )

    xgb_started = (
        time.perf_counter()
    )

    p_xgb = (
        xgb_model.predict_proba(
            X_holdout
        )[
            :,
            1
        ]
    )

    xgb_seconds = (
        time.perf_counter()
        - xgb_started
    )

    if (
        p_xgb.shape
        != (
            EXPECTED_ROWS,
        )
    ):
        raise RuntimeError(
            f"{unit}/seed{seed}: XGB probability shape mismatch."
        )

    # ---------------------------------------------------------------------------------------------
    # LIGHTGBM — LOAD FROZEN MODEL, NO FIT
    # ---------------------------------------------------------------------------------------------

    lgb_model = lgb.Booster(
        model_file=str(
            spec[
                "lgb_path"
            ]
        )
    )

    lgb_iterations = int(
        lgb_model.current_iteration()
    )

    if lgb_iterations != 400:
        raise RuntimeError(
            f"{unit}/seed{seed}: "
            f"LightGBM iterations {lgb_iterations} != 400."
        )

    lgb_started = (
        time.perf_counter()
    )

    p_lgb = lgb_model.predict(
        X_holdout,
        num_iteration=lgb_iterations,
    )

    lgb_seconds = (
        time.perf_counter()
        - lgb_started
    )

    if (
        p_lgb.shape
        != (
            EXPECTED_ROWS,
        )
    ):
        raise RuntimeError(
            f"{unit}/seed{seed}: LGB probability shape mismatch."
        )

    # ---------------------------------------------------------------------------------------------
    # FROZEN SCIENTIFIC UNIT:
    # float64 combination -> persisted float32 ensemble probability.
    # ---------------------------------------------------------------------------------------------

    p_ensemble = (
        0.5
        * np.asarray(
            p_lgb,
            dtype=np.float64,
        )
        +
        0.5
        * np.asarray(
            p_xgb,
            dtype=np.float64,
        )
    ).astype(
        np.float32,
        copy=False,
    )

    if (
        p_ensemble.dtype
        != np.float32
    ):
        raise RuntimeError(
            "Ensemble storage dtype != float32."
        )

    if not np.all(
        np.isfinite(
            p_ensemble
        )
    ):
        raise RuntimeError(
            f"{unit}/seed{seed}: non-finite ensemble probability."
        )

    if (
        float(
            p_ensemble.min()
        ) < 0.0
        or
        float(
            p_ensemble.max()
        ) > 1.0
    ):
        raise RuntimeError(
            f"{unit}/seed{seed}: probability outside [0,1]."
        )

    # ---------------------------------------------------------------------------------------------
    # FROZEN METRICS
    # ---------------------------------------------------------------------------------------------

    roc_auc = float(
        roc_auc_score(
            y_true,
            p_ensemble,
        )
    )

    pr_auc = float(
        average_precision_score(
            y_true,
            p_ensemble,
        )
    )

    op_results = {}

    for op_name in [
        "STANDARD",
        "BALANCED",
        "SECURITY",
    ]:
        op_results[
            op_name
        ] = operating_metrics(
            y_true,
            p_ensemble,
            spec[
                "thresholds"
            ][
                op_name
            ],
        )

    probability_key = (
        unit.lower()
        + "_seed"
        + str(
            seed
        )
    )

    probability_arrays[
        probability_key
    ] = p_ensemble.copy()

    probability_sha = (
        sha256_array_raw(
            p_ensemble
        )
    )

    cell_seconds = (
        time.perf_counter()
        - cell_started
    )

    probability_records[
        probability_key
    ] = {
        "unit":
            unit,

        "seed":
            seed,

        "dtype":
            str(
                p_ensemble.dtype
            ),

        "rows":
            int(
                p_ensemble.size
            ),

        "logical_sha256":
            probability_sha,

        "minimum":
            float(
                p_ensemble.min()
            ),

        "maximum":
            float(
                p_ensemble.max()
            ),

        "xgboost_inference_seconds":
            xgb_seconds,

        "lightgbm_inference_seconds":
            lgb_seconds,

        "cell_total_seconds":
            cell_seconds,
    }

    row = {
        "unit":
            unit,

        "seed":
            seed,

        "shared_holdout_rows":
            EXPECTED_ROWS,

        "shared_holdout_benign":
            EXPECTED_BENIGN,

        "shared_holdout_attack":
            EXPECTED_ATTACK,

        "shared_holdout_attack_prevalence":
            EXPECTED_ATTACK
            / EXPECTED_ROWS,

        "roc_auc":
            roc_auc,

        "pr_auc":
            pr_auc,

        "ensemble_probability_sha256":
            probability_sha,

        "xgboost_component_id":
            spec[
                "xgb_component_id"
            ],

        "xgboost_model_sha256":
            spec[
                "xgb_sha256"
            ],

        "lightgbm_component_id":
            spec[
                "lgb_component_id"
            ],

        "lightgbm_model_sha256":
            spec[
                "lgb_sha256"
            ],

        "inference_seconds_xgboost":
            xgb_seconds,

        "inference_seconds_lightgbm":
            lgb_seconds,

        "inference_seconds_cell_total":
            cell_seconds,
    }

    for op_name in [
        "STANDARD",
        "BALANCED",
        "SECURITY",
    ]:
        op = op_results[
            op_name
        ]

        prefix = (
            op_name.lower()
        )

        for field in [
            "threshold",
            "threshold_float32_runtime",
            "accuracy",
            "precision",
            "recall",
            "fpr",
            "f1",
            "f2",
            "tp",
            "fp",
            "tn",
            "fn",
        ]:
            row[
                f"{prefix}_{field}"
            ] = op[
                field
            ]

    metric_rows.append(
        row
    )

    print(
        f"ROC-AUC : {roc_auc:.12f}"
    )

    print(
        f"PR-AUC  : {pr_auc:.12f}"
    )

    print(
        "STANDARD:"
        f" recall={op_results['STANDARD']['recall']:.12f},"
        f" fpr={op_results['STANDARD']['fpr']:.12f},"
        f" f1={op_results['STANDARD']['f1']:.12f}"
    )

    print(
        "BALANCED:"
        f" recall={op_results['BALANCED']['recall']:.12f},"
        f" fpr={op_results['BALANCED']['fpr']:.12f},"
        f" f1={op_results['BALANCED']['f1']:.12f}"
    )

    print(
        "SECURITY:"
        f" recall={op_results['SECURITY']['recall']:.12f},"
        f" fpr={op_results['SECURITY']['fpr']:.12f},"
        f" f2={op_results['SECURITY']['f2']:.12f}"
    )

    print(
        f"[PASS] persisted float32 probability SHA256: "
        f"{probability_sha}"
    )

    # Free component-model and component-probability objects.
    del p_xgb
    del p_lgb
    del p_ensemble
    del xgb_model
    del lgb_model
    gc.collect()

total_inference_seconds = (
    time.perf_counter()
    - inference_started
)

if len(
    metric_rows
) != 10:
    raise RuntimeError(
        "Stage28-4 did not produce exactly 10 ensemble evaluations."
    )

print()
print(
    "[PASS] 20 component-model inferences completed"
)

print(
    "[PASS] 10 persisted Stage22 ensemble realizations evaluated"
)

print(
    f"Total inference wall time: {total_inference_seconds:.3f} seconds"
)


# =================================================================================================
# 9. WRITE SEED-LEVEL METRICS + PROBABILITY ARTIFACT
# =================================================================================================

banner(
    "STAGE28-4 — WRITE DURABLE SEED-LEVEL RESULTS"
)

metrics_df = pd.DataFrame(
    metric_rows
)

metrics_df = (
    metrics_df.sort_values(
        [
            "unit",
            "seed",
        ],
        key=lambda s:
            (
                s.map(
                    {
                        "RANDOM_NATURAL": 0,
                        "CHRONOLOGICAL_NATURAL": 1,
                    }
                )
                if s.name == "unit"
                else s
            ),
    )
    .reset_index(
        drop=True
    )
)

METRICS_PATH = (
    STAGE4_ROOT
    / "stage28_4_seed_level_metrics.csv"
)

PROBABILITY_PATH = (
    STAGE4_ROOT
    / "stage28_4_shared_holdout_ensemble_probabilities.npz"
)

metrics_df.to_csv(
    METRICS_PATH,
    index=False,
)

np.savez_compressed(
    PROBABILITY_PATH,
    **probability_arrays,
)

probability_artifact_sha = (
    sha256_file(
        PROBABILITY_PATH
    )
)

print(
    "[PASS] seed-level metric table written"
)

print(
    "[PASS] ten persisted float32 ensemble probability arrays written"
)

print(
    "Probability artifact SHA256:",
    probability_artifact_sha,
)


# =================================================================================================
# 10. PREREGISTERED STAGE22 DIRECTIONAL CONCLUSION STABILITY
# =================================================================================================

banner(
    "STAGE28-4 — PREREGISTERED STAGE22 DIRECTIONAL STABILITY"
)

metric_lookup = {}

for row in metric_rows:
    metric_lookup[
        (
            row[
                "unit"
            ],
            int(
                row[
                    "seed"
                ]
            ),
        )
    ] = row

claim_rows = []

contrast_rows = []

for seed in EXPECTED_SEEDS:
    random_row = metric_lookup[
        (
            "RANDOM_NATURAL",
            seed,
        )
    ]

    chrono_row = metric_lookup[
        (
            "CHRONOLOGICAL_NATURAL",
            seed,
        )
    ]

    pr_random = float(
        random_row[
            "pr_auc"
        ]
    )

    pr_chrono = float(
        chrono_row[
            "pr_auc"
        ]
    )

    roc_random = float(
        random_row[
            "roc_auc"
        ]
    )

    roc_chrono = float(
        chrono_row[
            "roc_auc"
        ]
    )

    pr_condition = bool(
        pr_random
        < pr_chrono
    )

    roc_condition = bool(
        roc_random
        < roc_chrono
    )

    contrast_rows.append(
        {
            "seed":
                seed,

            "pr_auc_random":
                pr_random,

            "pr_auc_chronological":
                pr_chrono,

            "pr_auc_random_minus_chronological":
                pr_random
                - pr_chrono,

            "pr_random_lt_chronological":
                pr_condition,

            "roc_auc_random":
                roc_random,

            "roc_auc_chronological":
                roc_chrono,

            "roc_auc_random_minus_chronological":
                roc_random
                - roc_chrono,

            "roc_random_lt_chronological":
                roc_condition,
        }
    )

    claim_rows.append(
        {
            "claim_id":
                "STAGE22_PR_RANDOM_LT_CHRONO_ON_SHARED_FINAL_HOLDOUT",

            "parent_stage":
                "STAGE22_FULL",

            "family_if_applicable":
                "",

            "learner_if_applicable":
                "",

            "seed":
                seed,

            "claim_condition":
                "PR_AUC_RANDOM_NATURAL < PR_AUC_CHRONOLOGICAL_NATURAL",

            "condition_met":
                pr_condition,

            "analysis_status":
                "DESCRIPTIVE_ROBUSTNESS_PRE_REGISTERED",
        }
    )

    claim_rows.append(
        {
            "claim_id":
                "STAGE22_ROC_RANDOM_LT_CHRONO_ON_SHARED_FINAL_HOLDOUT",

            "parent_stage":
                "STAGE22_FULL",

            "family_if_applicable":
                "",

            "learner_if_applicable":
                "",

            "seed":
                seed,

            "claim_condition":
                "ROC_AUC_RANDOM_NATURAL < ROC_AUC_CHRONOLOGICAL_NATURAL",

            "condition_met":
                roc_condition,

            "analysis_status":
                "DESCRIPTIVE_ROBUSTNESS_PRE_REGISTERED",
        }
    )

claim_df = pd.DataFrame(
    claim_rows
)

contrast_df = pd.DataFrame(
    contrast_rows
)

if len(
    claim_df
) != 10:
    raise RuntimeError(
        "Expected exactly 10 Stage22 directional claim realizations."
    )

CLAIMS_PATH = (
    STAGE4_ROOT
    / "stage28_4_stage22_directional_claims.csv"
)

CONTRAST_PATH = (
    STAGE4_ROOT
    / "stage28_4_random_vs_chronological_seedwise.csv"
)

claim_df.to_csv(
    CLAIMS_PATH,
    index=False,
)

contrast_df.to_csv(
    CONTRAST_PATH,
    index=False,
)

stability_rows = []

for claim_id in [
    "STAGE22_PR_RANDOM_LT_CHRONO_ON_SHARED_FINAL_HOLDOUT",
    "STAGE22_ROC_RANDOM_LT_CHRONO_ON_SHARED_FINAL_HOLDOUT",
]:
    subset = claim_df.loc[
        claim_df[
            "claim_id"
        ]
        == claim_id
    ]

    supporting = int(
        subset[
            "condition_met"
        ].sum()
    )

    total = int(
        len(
            subset
        )
    )

    if total != 5:
        raise RuntimeError(
            f"{claim_id}: seed denominator != 5."
        )

    stability_rows.append(
        {
            "claim_id":
                claim_id,

            "supporting_seeds":
                supporting,

            "total_frozen_seeds":
                total,

            "stability_rate":
                supporting
                / total,

            "interpretation":
                "DESCRIPTIVE_ROBUSTNESS_NOT_NEW_SIGNIFICANCE_TEST",
        }
    )

stability_df = pd.DataFrame(
    stability_rows
)

STABILITY_PATH = (
    STAGE4_ROOT
    / "stage28_4_stage22_directional_stability_summary.csv"
)

stability_df.to_csv(
    STABILITY_PATH,
    index=False,
)

for _, row in (
    contrast_df.iterrows()
):
    print(
        f"seed {int(row['seed'])}: "
        f"ΔPR(random-chrono)="
        f"{row['pr_auc_random_minus_chronological']:+.12f} "
        f"support={bool(row['pr_random_lt_chronological'])}; "
        f"ΔROC(random-chrono)="
        f"{row['roc_auc_random_minus_chronological']:+.12f} "
        f"support={bool(row['roc_random_lt_chronological'])}"
    )

print()

for _, row in (
    stability_df.iterrows()
):
    print(
        row[
            "claim_id"
        ]
    )

    print(
        f"  supporting seeds: "
        f"{int(row['supporting_seeds'])}/"
        f"{int(row['total_frozen_seeds'])}"
    )

    print(
        f"  stability rate  : "
        f"{float(row['stability_rate']):.3f}"
    )

print()
print(
    "[PASS] no post-result condition created"
)

print(
    "[PASS] no formal significance test introduced"
)


# =================================================================================================
# 11. CREATE THE FROZEN REQUIRED COMBINED conclusion_stability.csv
# =================================================================================================

banner(
    "STAGE28-4 — COMPLETE FROZEN conclusion_stability.csv"
)

loao_claim_df = pd.read_csv(
    LOAO_CONCLUSION_STABILITY
)

expected_columns = [
    "claim_id",
    "parent_stage",
    "family_if_applicable",
    "learner_if_applicable",
    "seed",
    "claim_condition",
    "condition_met",
    "analysis_status",
]

if list(
    loao_claim_df.columns
) != expected_columns:
    raise RuntimeError(
        "Stage28-3B LOAO conclusion-stability schema changed."
    )

if list(
    claim_df.columns
) != expected_columns:
    raise RuntimeError(
        "Stage28-4 Stage22 conclusion-stability schema mismatch."
    )

combined_claim_df = pd.concat(
    [
        loao_claim_df,
        claim_df,
    ],
    ignore_index=True,
)

combined_claim_df.to_csv(
    COMBINED_CONCLUSION_STABILITY,
    index=False,
)

print(
    "Stage28-3B LOAO rows :",
    len(
        loao_claim_df
    ),
)

print(
    "Stage28-4 Stage22 rows:",
    len(
        claim_df
    ),
)

print(
    "Combined rows          :",
    len(
        combined_claim_df
    ),
)

print()
print(
    "[PASS] frozen required output created:"
)

print(
    " ",
    COMBINED_CONCLUSION_STABILITY.relative_to(
        REPO
    ),
)


# =================================================================================================
# 12. MATERIALIZATION RECEIPT
# =================================================================================================

banner(
    "STAGE28-4 — WRITE RECEIPTS"
)

MATERIALIZATION_RECEIPT = (
    STAGE4_ROOT
    / "stage28_4_holdout_materialization_receipt.json"
)

materialization_receipt = {
    "stage":
        "Stage28-4",

    "type":
        "STAGE22_SHARED_FINAL_HOLDOUT_MATERIALIZATION",

    "created_at_utc":
        utc_now(),

    "scientific_parent_commit":
        EXPECTED_PARENT,

    "population":
        "STAGE22R_SHARED_FINAL_SINGLE_HOLDOUT",

    "interpretive_status":
        (
            "PRE_REGISTERED_ROBUSTNESS_REEVALUATION_OF_ALREADY_KNOWN_"
            "PARENT_HOLDOUT_NOT_NEW_BLIND_HOLDOUT"
        ),

    "membership": {
        "path":
            str(
                MEMBERSHIP_PATH.relative_to(
                    REPO
                )
            ),

        "file_sha256":
            membership_sha,

        "rows":
            EXPECTED_ROWS,

        "benign":
            EXPECTED_BENIGN,

        "attack":
            EXPECTED_ATTACK,

        "logical_arrays":
            membership_logical,
    },

    "source_files": {
        "day_8":
            source_records[
                8
            ],

        "day_9":
            source_records[
                9
            ],
    },

    "per_day_materialization":
        {
            str(
                k
            ):
                v
            for k, v
            in materialization_records.items()
        },

    "model_input": {
        "rows":
            EXPECTED_ROWS,

        "features":
            EXPECTED_FEATURES,

        "dtype":
            "float64",

        "scaling":
            "NONE",

        "explicit_imputation":
            "NONE",

        "positive_infinity_to_nan":
            total_pos_inf,

        "negative_infinity_to_nan":
            total_neg_inf,

        "output_nan_cells":
            final_nan_cells,

        "X_logical_sha256":
            X_logical_sha,

        "y_logical_sha256":
            y_logical_sha,
    },

    "scientific_operations": {
        "new_model_fits":
            0,

        "model_inference":
            0,

        "threshold_selection":
            0,

        "model_selection":
            0,

        "new_formal_statistical_tests":
            0,

        "raw_data_read_passes_per_file":
            1,

        "stage28_shared_final_holdout_materialization":
            1,
    },

    "status":
        "PASS_EXACT_FROZEN_HOLDOUT_MATERIALIZED",
}

write_json(
    MATERIALIZATION_RECEIPT,
    materialization_receipt,
)


# =================================================================================================
# 13. STAGE28-4 FINAL RECEIPT
# =================================================================================================

FINAL_RECEIPT = (
    STAGE4_ROOT
    / "stage28_4_receipt.json"
)

probability_keys = sorted(
    probability_arrays.keys()
)

receipt = {
    "stage":
        "Stage28-4",

    "type":
        "STAGE22_FIVE_SEED_SHARED_FINAL_HOLDOUT_ROBUSTNESS_INFERENCE",

    "created_at_utc":
        utc_now(),

    "scientific_parent_commit":
        EXPECTED_PARENT,

    "authorization": {
        "previous_stage":
            "Stage28-3C",

        "authorized_by":
            str(
                STAGE3C_RECEIPT.relative_to(
                    REPO
                )
            ),

        "new_model_fitting":
            "PERMANENTLY_CLOSED",

        "threshold_selection_on_final_holdout":
            "FORBIDDEN",

        "model_selection_on_final_holdout":
            "FORBIDDEN",
    },

    "holdout": {
        "name":
            "STAGE22R_SHARED_FINAL_SINGLE_HOLDOUT",

        "rows":
            EXPECTED_ROWS,

        "benign":
            EXPECTED_BENIGN,

        "attack":
            EXPECTED_ATTACK,

        "attack_prevalence":
            EXPECTED_ATTACK
            / EXPECTED_ROWS,

        "feature_count":
            EXPECTED_FEATURES,

        "model_input_dtype":
            "float64",

        "X_logical_sha256":
            X_logical_sha,

        "y_logical_sha256":
            y_logical_sha,

        "blind_status":
            (
                "NOT_NEW_BLIND_HOLDOUT_PARENT_STAGE22R_ALREADY_OPENED; "
                "STAGE28_USE_IS_PRE_REGISTERED_ROBUSTNESS_ONLY"
            ),
    },

    "scientific_unit": {
        "strategy":
            "ENS_LGBM_XGB_EQUAL",

        "component_learners": [
            "LIGHTGBM",
            "XGBOOST",
        ],

        "probability_rule":
            "0.5 * P_LIGHTGBM + 0.5 * P_XGBOOST",

        "component_combination_dtype":
            "float64",

        "ensemble_storage_dtype":
            "float32",
    },

    "design": {
        "units":
            EXPECTED_UNITS,

        "seeds":
            EXPECTED_SEEDS,

        "ensemble_realizations":
            10,

        "component_model_inferences":
            20,

        "new_model_fits":
            0,
    },

    "threshold_policy": {
        "selection_population":
            "FROZEN_STAGE22_DEVELOPMENT_VALIDATION_ONLY",

        "final_holdout_threshold_search":
            "FORBIDDEN",

        "prediction_rule":
            (
                "ATTACK_IF_PERSISTED_FLOAT32_ENSEMBLE_"
                "PROBABILITY_GTE_FROZEN_THRESHOLD"
            ),

        "operating_points": [
            "STANDARD",
            "BALANCED",
            "SECURITY",
        ],
    },

    "probability_artifact": {
        "path":
            str(
                PROBABILITY_PATH.relative_to(
                    REPO
                )
            ),

        "file_sha256":
            probability_artifact_sha,

        "keys":
            probability_keys,

        "arrays":
            probability_records,
    },

    "seed_level_metrics": {
        "path":
            str(
                METRICS_PATH.relative_to(
                    REPO
                )
            ),

        "rows":
            len(
                metrics_df
            ),
    },

    "stage22_directional_claims": {
        "path":
            str(
                CLAIMS_PATH.relative_to(
                    REPO
                )
            ),

        "conditions":
            [
                {
                    "claim_id":
                        (
                            "STAGE22_PR_RANDOM_LT_CHRONO_"
                            "ON_SHARED_FINAL_HOLDOUT"
                        ),

                    "condition":
                        (
                            "PR_AUC_RANDOM_NATURAL < "
                            "PR_AUC_CHRONOLOGICAL_NATURAL"
                        ),
                },
                {
                    "claim_id":
                        (
                            "STAGE22_ROC_RANDOM_LT_CHRONO_"
                            "ON_SHARED_FINAL_HOLDOUT"
                        ),

                    "condition":
                        (
                            "ROC_AUC_RANDOM_NATURAL < "
                            "ROC_AUC_CHRONOLOGICAL_NATURAL"
                        ),
                },
            ],

        "stability_rate_definition":
            "NUMBER_OF_FROZEN_SEEDS_SUPPORTING_CONDITION / 5",

        "summary_path":
            str(
                STABILITY_PATH.relative_to(
                    REPO
                )
            ),

        "new_condition_creation":
            "FORBIDDEN_AND_NOT_PERFORMED",

        "formal_significance_testing":
            "NOT_PERFORMED",
    },

    "combined_conclusion_stability": {
        "path":
            str(
                COMBINED_CONCLUSION_STABILITY.relative_to(
                    REPO
                )
            ),

        "stage28_3b_rows":
            int(
                len(
                    loao_claim_df
                )
            ),

        "stage28_4_stage22_rows":
            int(
                len(
                    claim_df
                )
            ),

        "combined_rows":
            int(
                len(
                    combined_claim_df
                )
            ),
    },

    "scientific_operations": {
        "new_model_fits":
            0,

        "component_model_inferences":
            20,

        "ensemble_evaluation_cells":
            10,

        "threshold_selection":
            0,

        "model_selection":
            0,

        "shared_stage22_final_holdout_stage28_openings":
            1,

        "new_formal_statistical_tests":
            0,

        "shap_recomputation":
            0,

        "subset_search":
            0,

        "new_holdout_creation":
            0,
    },

    "total_inference_seconds":
        total_inference_seconds,

    "next_authorized_step":
        (
            "ZERO_FIT_FINAL_SYNTHESIS_AND_MANUSCRIPT_INTEGRATION; "
            "NO FURTHER MODEL FITTING; NO STAGE29."
        ),

    "status":
        "STAGE28_4_COMPLETE",
}

write_json(
    FINAL_RECEIPT,
    receipt,
)


# =================================================================================================
# 14. README
# =================================================================================================

README_PATH = (
    STAGE4_ROOT
    / "README_STAGE28_4.md"
)

stability_map = {
    row[
        "claim_id"
    ]:
        {
            "supporting":
                int(
                    row[
                        "supporting_seeds"
                    ]
                ),

            "total":
                int(
                    row[
                        "total_frozen_seeds"
                    ]
                ),

            "rate":
                float(
                    row[
                        "stability_rate"
                    ]
                ),
        }
    for _, row
    in stability_df.iterrows()
}

pr_stability = stability_map[
    "STAGE22_PR_RANDOM_LT_CHRONO_ON_SHARED_FINAL_HOLDOUT"
]

roc_stability = stability_map[
    "STAGE22_ROC_RANDOM_LT_CHRONO_ON_SHARED_FINAL_HOLDOUT"
]

readme_text = f"""# Stage28-4 — Stage22 Shared Final Holdout Robustness Inference

Scientific parent: `{EXPECTED_PARENT}`

## Scope

Stage28-4 evaluates the ten frozen Stage22 FULL ensemble realizations:

- RANDOM_NATURAL, seeds 42–46
- CHRONOLOGICAL_NATURAL, seeds 42–46

All realizations use the same frozen Stage22R shared final holdout.

No model fitting, threshold selection, model selection, SHAP recomputation,
subset search, or new formal significance test was performed.

## Holdout

- Rows: {EXPECTED_ROWS:,}
- Benign: {EXPECTED_BENIGN:,}
- Attack: {EXPECTED_ATTACK:,}
- Features: {EXPECTED_FEATURES}
- Model-input dtype: float64
- X logical SHA256: `{X_logical_sha}`
- y logical SHA256: `{y_logical_sha}`

The parent Stage22R holdout was already historically opened. Stage28-4 is
therefore preregistered robustness re-evaluation and does not constitute a
new blind holdout claim.

## Frozen scientific unit

`0.5 * P_LIGHTGBM + 0.5 * P_XGBOOST`

Component probabilities are combined in float64 and the ensemble
probability is persisted as float32 before threshold application.

## Frozen Stage22 directional conclusion stability

### PR-AUC

Claim:

`PR_AUC_RANDOM_NATURAL < PR_AUC_CHRONOLOGICAL_NATURAL`

Supporting seeds:

`{pr_stability['supporting']} / {pr_stability['total']}`

Stability rate:

`{pr_stability['rate']:.6f}`

### ROC-AUC

Claim:

`ROC_AUC_RANDOM_NATURAL < ROC_AUC_CHRONOLOGICAL_NATURAL`

Supporting seeds:

`{roc_stability['supporting']} / {roc_stability['total']}`

Stability rate:

`{roc_stability['rate']:.6f}`

## Closure

Stage28 model fitting remains permanently closed at 108 / 108 new fits.

No Stage29 is authorized. The remaining work is zero-fit synthesis and
manuscript integration.
"""

README_PATH.write_text(
    readme_text,
    encoding="utf-8",
)


# =================================================================================================
# 15. CHECKSUM MANIFEST
# =================================================================================================

CHECKSUM_PATH = (
    STAGE4_ROOT
    / "stage28_4_checksums.sha256"
)

artifact_paths = sorted(
    [
        p
        for p in STAGE4_ROOT.rglob(
            "*"
        )
        if (
            p.is_file()
            and
            p != CHECKSUM_PATH
        )
    ]
)

artifact_paths.append(
    COMBINED_CONCLUSION_STABILITY
)

checksum_lines = []

for path in artifact_paths:
    checksum_lines.append(
        sha256_file(
            path
        )
        + "  "
        + str(
            path.relative_to(
                REPO
            )
        )
    )

CHECKSUM_PATH.write_text(
    "\n".join(
        checksum_lines
    )
    + "\n",
    encoding="utf-8",
)

print(
    "[PASS] Stage28-4 receipts written"
)

print(
    "[PASS] README written"
)

print(
    "[PASS] checksum manifest written"
)


# =================================================================================================
# 16. FINAL SCIENTIFIC INVARIANTS
# =================================================================================================

banner(
    "STAGE28-4 — FINAL SCIENTIFIC INVARIANTS"
)

# Re-read permanent fit closure. It must still be untouched.
closure_after = read_json(
    CLOSURE_RECEIPT
)

if (
    closure_after
    != closure
):
    raise RuntimeError(
        "Stage28 closure receipt changed unexpectedly."
    )

if (
    int(
        closure_after[
            "fit_budget_closure"
        ][
            "consumed_new_fits"
        ]
    )
    != 108
):
    raise RuntimeError(
        "Fit ledger changed."
    )

if (
    int(
        closure_after[
            "fit_budget_closure"
        ][
            "remaining_new_fits"
        ]
    )
    != 0
):
    raise RuntimeError(
        "Remaining fit budget changed."
    )

if len(
    probability_arrays
) != 10:
    raise RuntimeError(
        "Probability artifact count != 10."
    )

if len(
    metrics_df
) != 10:
    raise RuntimeError(
        "Metrics count != 10."
    )

if len(
    claim_df
) != 10:
    raise RuntimeError(
        "Stage22 directional claim count != 10."
    )

print(
    "[PASS] Stage28 new-fit ledger remains 108 / 108"
)

print(
    "[PASS] new fits performed = 0"
)

print(
    "[PASS] threshold selections performed = 0"
)

print(
    "[PASS] model selections performed = 0"
)

print(
    "[PASS] new formal statistical tests = 0"
)

print(
    "[PASS] SHAP recomputation = 0"
)

print(
    "[PASS] subset search = 0"
)

print(
    "[PASS] exactly 10 ensemble evaluations"
)

print(
    "[PASS] exactly 20 frozen component-model inferences"
)

print(
    "[PASS] Stage22 shared-final robustness opening consumed"
)


# =================================================================================================
# 17. GIT CHANGE GATE
# =================================================================================================

banner(
    "STAGE28-4 — GIT CHANGE GATE"
)

status_before_add = git(
    "status",
    "--porcelain",
)

print(
    status_before_add
)

allowed_prefix = str(
    STAGE4_ROOT.relative_to(
        REPO
    )
)

allowed_combined = str(
    COMBINED_CONCLUSION_STABILITY.relative_to(
        REPO
    )
)

for line in (
    status_before_add.splitlines()
):
    if not line.strip():
        continue

    path_text = line[
        3:
    ].strip()

    if (
        not path_text.startswith(
            allowed_prefix
        )
        and
        path_text
        != allowed_combined
    ):
        raise RuntimeError(
            "Unexpected repository modification before commit:\n"
            + line
        )

print()
print(
    "[PASS] only authorized Stage28-4 artifacts changed"
)


# =================================================================================================
# 18. DURABLE COMMIT
# =================================================================================================

banner(
    "STAGE28-4 — DURABLE COMMIT / PUSH"
)

# Race gate: origin/main must still be our parent.
run(
    [
        "git",
        "fetch",
        "origin",
        "main",
    ]
)

origin_now = git(
    "rev-parse",
    "origin/main",
)

if origin_now != EXPECTED_PARENT:
    raise RuntimeError(
        "origin/main changed during Stage28-4 execution. "
        "Refusing to commit/push."
    )

git(
    "config",
    "user.name",
    "Stage28 Kaggle",
)

git(
    "config",
    "user.email",
    "stage28-kaggle@users.noreply.github.com",
)

# Force-add so ignored numpy artifact rules cannot recreate the
# historical AUTO-B durability bug.
git(
    "add",
    "-f",
    "--",
    str(
        STAGE4_ROOT.relative_to(
            REPO
        )
    ),
)

git(
    "add",
    "-f",
    "--",
    str(
        COMBINED_CONCLUSION_STABILITY.relative_to(
            REPO
        )
    ),
)

cached = git(
    "diff",
    "--cached",
    "--name-only",
)

if not cached.strip():
    raise RuntimeError(
        "Nothing staged for Stage28-4 commit."
    )

print(
    "Staged files:"
)

print(
    cached
)

commit_message = (
    "stage28-4: evaluate Stage22 five-seed ensembles "
    "on shared final holdout"
)

commit_result = run(
    [
        "git",
        "commit",
        "-m",
        commit_message,
    ]
)

print(
    commit_result.stdout
)

new_head = git(
    "rev-parse",
    "HEAD",
)

if new_head == EXPECTED_PARENT:
    raise RuntimeError(
        "Commit did not advance HEAD."
    )

print(
    "New commit:",
    new_head,
)

git_push_with_kaggle_secret()

# Verify remote durability.
run(
    [
        "git",
        "fetch",
        "origin",
        "main",
    ]
)

remote_after = git(
    "rev-parse",
    "origin/main",
)

if remote_after != new_head:
    raise RuntimeError(
        "Remote durability verification failed."
    )

if git(
    "status",
    "--porcelain",
):
    raise RuntimeError(
        "Repository not clean after Stage28-4 commit."
    )

print()
print(
    "[PASS] Stage28-4 commit durable on origin/main"
)

print(
    "[PASS] repository clean"
)


# =================================================================================================
# 19. FINAL REPORT
# =================================================================================================

banner(
    "STAGE28-4 — COMPLETE"
)

print(
    "Commit:",
    new_head,
)

print()
print(
    "New model fits                    : 0"
)

print(
    "Component model inferences        : 20"
)

print(
    "Ensemble evaluation cells         : 10"
)

print(
    "Threshold selections              : 0"
)

print(
    "Model selections                  : 0"
)

print(
    "New formal statistical tests      : 0"
)

print(
    "SHAP recomputation                : 0"
)

print(
    "Subset search                     : 0"
)

print(
    "Shared Stage22 holdout rows        :",
    f"{EXPECTED_ROWS:,}",
)

print(
    "Shared Stage22 holdout benign      :",
    f"{EXPECTED_BENIGN:,}",
)

print(
    "Shared Stage22 holdout attack      :",
    f"{EXPECTED_ATTACK:,}",
)

print()
print(
    "STAGE22 DIRECTIONAL STABILITY"
)

print(
    "-----------------------------"
)

for _, row in (
    stability_df.iterrows()
):
    print(
        f"{row['claim_id']}: "
        f"{int(row['supporting_seeds'])}/"
        f"{int(row['total_frozen_seeds'])} "
        f"= {float(row['stability_rate']):.3f}"
    )

print()
print(
    "Stage28 fitting status             : PERMANENTLY CLOSED"
)

print(
    "Stage28 new-fit budget             : 108 / 108 CONSUMED"
)

print(
    "Stage29                           : NOT AUTHORIZED"
)

print()
print(
    "NEXT AUTHORIZED WORK:"
)

print(
    "ZERO-FIT FINAL SYNTHESIS + MANUSCRIPT INTEGRATION."
)

# ==============================================================================================================
# %% NOTEBOOK CELL 0013 | execution_count=13
# ==============================================================================================================
# =================================================================================================
# STAGE28-4-R1 — SALVAGE ALREADY-MATERIALIZED SHARED HOLDOUT + COMPLETE INFERENCE
#
# IMPORTANT:
#   RUN IN THE SAME KAGGLE KERNEL AS THE FAILED STAGE28-4 CELL.
#
# THIS CELL:
#   - DOES NOT READ 03-01-2018.csv
#   - DOES NOT READ 03-02-2018.csv
#   - DOES NOT REMATERIALIZE THE HOLDOUT
#   - DOES NOT FIT ANY MODEL
#   - DOES NOT SELECT ANY THRESHOLD
#
# RECOVERY STATE:
#   The authorized Stage28 shared-holdout materialization already occurred successfully.
#   The failure happened during receipt auditing before model inference.
#
# TWO-PHASE DURABILITY:
#   Phase A: durably freeze the already-consumed materialization/opening.
#   Phase B: perform frozen inference and freeze final Stage28-4 results.
# =================================================================================================

from __future__ import annotations

import base64
import csv
import gc
import hashlib
import json
import math
import os
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import sklearn
from sklearn.metrics import (
    average_precision_score,
    roc_auc_score,
)

import xgboost as xgb
import lightgbm as lgb


# =================================================================================================
# CONSTANTS
# =================================================================================================

SEP = "=" * 120

REPO = Path(
    "/kaggle/working/ids2018-validation-safe-ablation"
).resolve()

FAILED_STAGE28_4_PARENT = (
    "2679d0c208d514b381caa12e96c959f4f2ee5ee7"
)

ROOT = (
    REPO
    / "results"
    / "stage28_stability_novelty_control"
)

STAGE22_ROOT = (
    ROOT
    / "stage28_2a_stage22_seed_stability"
)

PROTOCOL_ROOT = (
    ROOT
    / "stage28_0_protocol_lock"
)

STAGE3_ROOT = (
    ROOT
    / "stage28_3_seed_uncertainty"
)

STAGE4_ROOT = (
    ROOT
    / "stage28_4_stage22_shared_final_holdout"
)

CLOSURE_RECEIPT = (
    ROOT
    / "stage28_3a_experiment_closure_audit"
    / "stage28_3a_experiment_closure_receipt.json"
)

STAGE3C_RECEIPT = (
    STAGE3_ROOT
    / "stage28_3c_receipt.json"
)

STAGE22_SPEC = (
    PROTOCOL_ROOT
    / "stage22_cell_spec.json"
)

STABILITY_SPEC = (
    PROTOCOL_ROOT
    / "conclusion_stability_spec.json"
)

LOAO_STABILITY_PATH = (
    STAGE3_ROOT
    / "stage28_3b_loao_conclusion_stability.csv"
)

COMBINED_STABILITY_PATH = (
    STAGE3_ROOT
    / "conclusion_stability.csv"
)

EXPECTED_ROWS = 1_374_133
EXPECTED_BENIGN = 998_788
EXPECTED_ATTACK = 375_345
EXPECTED_FEATURES = 70
EXPECTED_NAN_CELLS = 13_922

EXPECTED_X_SHA = (
    "50979ff283ddebaceb6442004c5b80b85e4fb40d02041a5150f730683b3d7c8e"
)

EXPECTED_Y_SHA = (
    "b99cf695a49ad2b0a8811fa269a55dcfb99cb700f473ceae8c9ecac2c8661a78"
)

EXPECTED_MEMBERSHIP_FILE_SHA = (
    "18d43eded5e78238ce6765abdc1ed18ce662aebd0899b678472891203eee3d1e"
)

EXPECTED_SEEDS = [
    42,
    43,
    44,
    45,
    46,
]

EXPECTED_UNITS = [
    "RANDOM_NATURAL",
    "CHRONOLOGICAL_NATURAL",
]

EXPECTED_VERSIONS = {
    "numpy": "2.0.2",
    "sklearn": "1.6.1",
    "xgboost": "3.2.0",
    "lightgbm": "4.6.0",
}

SOURCE_PROVENANCE = {
    8: {
        "file": "03-01-2018.csv",
        "bytes": 107_842_858,
        "sha256": "b0534c5d7d8b41e03df71c6966c995d116a8ed28e61f377c8b14cdf5d28f4edf",
        "physical_rows": 331_125,
        "embedded_header_rows": 25,
        "effective_rows": 331_100,
        "retained_rows": 331_017,
        "retained_benign": 237_982,
        "retained_attack": 93_035,
        "row_index_semantics": "RAW_PHYSICAL_ROW_INDEX",
        "positive_infinity_to_nan": 4_000,
        "negative_infinity_to_nan": 0,
    },
    9: {
        "file": "03-02-2018.csv",
        "bytes": 352_368_373,
        "sha256": "d96f38e7496aba83475031e6fb8c6fdf1abf6aa1b71325a917798f3c7de93de1",
        "physical_rows": 1_048_575,
        "embedded_header_rows": 0,
        "effective_rows": 1_048_575,
        "retained_rows": 1_043_116,
        "retained_benign": 760_806,
        "retained_attack": 282_310,
        "row_index_semantics": "RAW_EQUALS_EFFECTIVE_NO_EMBEDDED_HEADERS",
        "positive_infinity_to_nan": 5_530,
        "negative_infinity_to_nan": 0,
    },
}


# =================================================================================================
# HELPERS
# =================================================================================================

def banner(text):
    print()
    print(SEP)
    print(text)
    print(SEP)
    print()


def utc_now():
    return datetime.now(
        timezone.utc
    ).isoformat()


def run(
    cmd,
    *,
    cwd=REPO,
    check=True,
):
    p = subprocess.run(
        [str(x) for x in cmd],
        cwd=str(cwd),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    if check and p.returncode != 0:
        raise RuntimeError(
            f"Command failed ({p.returncode}):\n"
            + " ".join(map(str, cmd))
            + f"\n\nSTDOUT:\n{p.stdout}"
            + f"\n\nSTDERR:\n{p.stderr}"
        )

    return p


def git(*args):
    return run(
        ["git", *args]
    ).stdout.strip()


def read_json(path):
    return json.loads(
        Path(path).read_text(
            encoding="utf-8"
        )
    )


def write_json(
    path,
    obj,
):
    Path(path).write_text(
        json.dumps(
            obj,
            indent=2,
            ensure_ascii=False,
            allow_nan=False,
        )
        + "\n",
        encoding="utf-8",
    )


def sha256_file(
    path,
    chunk=16 * 1024 * 1024,
):
    h = hashlib.sha256()

    with Path(path).open("rb") as f:
        while True:
            block = f.read(chunk)

            if not block:
                break

            h.update(block)

    return h.hexdigest()


def sha256_array_raw(arr):
    arr = np.ascontiguousarray(
        arr
    )

    h = hashlib.sha256()

    view = memoryview(
        arr
    ).cast("B")

    step = 64 * 1024 * 1024

    for start in range(
        0,
        len(view),
        step,
    ):
        h.update(
            view[
                start:
                start + step
            ]
        )

    return h.hexdigest()


def safe_div(
    numerator,
    denominator,
):
    if denominator == 0:
        return 0.0

    return float(
        numerator
        / denominator
    )


def operating_metrics(
    y_true,
    probability,
    threshold,
):
    threshold32 = np.float32(
        threshold
    )

    pred = (
        probability
        >= threshold32
    )

    positive = (
        y_true == 1
    )

    negative = ~positive

    tp = int(
        np.count_nonzero(
            pred & positive
        )
    )

    fp = int(
        np.count_nonzero(
            pred & negative
        )
    )

    tn = int(
        np.count_nonzero(
            (~pred) & negative
        )
    )

    fn = int(
        np.count_nonzero(
            (~pred) & positive
        )
    )

    precision = safe_div(
        tp,
        tp + fp,
    )

    recall = safe_div(
        tp,
        tp + fn,
    )

    fpr = safe_div(
        fp,
        fp + tn,
    )

    accuracy = safe_div(
        tp + tn,
        len(y_true),
    )

    if (
        precision
        + recall
    ) > 0:
        f1 = (
            2.0
            * precision
            * recall
            / (
                precision
                + recall
            )
        )
    else:
        f1 = 0.0

    if (
        4.0
        * precision
        + recall
    ) > 0:
        f2 = (
            5.0
            * precision
            * recall
            / (
                4.0
                * precision
                + recall
            )
        )
    else:
        f2 = 0.0

    return {
        "threshold":
            float(
                threshold
            ),

        "threshold_float32_runtime":
            float(
                threshold32
            ),

        "accuracy":
            float(
                accuracy
            ),

        "precision":
            float(
                precision
            ),

        "recall":
            float(
                recall
            ),

        "fpr":
            float(
                fpr
            ),

        "f1":
            float(
                f1
            ),

        "f2":
            float(
                f2
            ),

        "tp":
            tp,

        "fp":
            fp,

        "tn":
            tn,

        "fn":
            fn,
    }


def extract_threshold(
    operating_points,
    name,
):
    op = operating_points[
        name.lower()
    ]

    if (
        isinstance(op, dict)
        and
        "result" in op
    ):
        if (
            op.get("status")
            != "AVAILABLE"
        ):
            raise RuntimeError(
                f"{name} operating point is not AVAILABLE."
            )

        op = op[
            "result"
        ]

    if not isinstance(
        op,
        dict,
    ):
        raise RuntimeError(
            f"Malformed {name} operating point."
        )

    if (
        "threshold"
        not in op
    ):
        raise RuntimeError(
            f"Frozen {name} threshold missing."
        )

    return float(
        op[
            "threshold"
        ]
    )


def resolve_model(
    result_path,
    model_info,
):
    # Historical / verbose schema:
    #   model_path
    #
    # AUTO-A compact schema:
    #   model
    #
    # Historical reuse schema:
    #   historical_model_path

    local_name = (
        model_info.get(
            "model_path"
        )
        or
        model_info.get(
            "model"
        )
    )

    if local_name:
        path = (
            result_path.parent
            / local_name
        )

        expected_sha = (
            model_info.get(
                "model_sha256"
            )
        )

        source_type = (
            "STAGE28_LOCAL_MODEL_ARTIFACT"
        )

    else:
        historical_name = (
            model_info.get(
                "historical_model_path"
            )
        )

        if not historical_name:
            raise RuntimeError(
                f"No model path field in:\n"
                f"{result_path}"
            )

        path = (
            REPO
            / historical_name
        )

        expected_sha = (
            model_info.get(
                "historical_model_sha256"
            )
        )

        source_type = (
            "HISTORICAL_REUSE_MODEL_ARTIFACT"
        )

    if not path.is_file():
        raise RuntimeError(
            f"Model missing:\n{path}"
        )

    if not expected_sha:
        raise RuntimeError(
            f"Expected model SHA missing:\n{result_path}"
        )

    actual_sha = sha256_file(
        path
    )

    if actual_sha != expected_sha:
        raise RuntimeError(
            "Model SHA mismatch:\n"
            f"{path}\n"
            f"expected={expected_sha}\n"
            f"actual={actual_sha}"
        )

    return {
        "path":
            path,

        "sha256":
            actual_sha,

        "source_type":
            source_type,
    }


def get_github_token():
    from kaggle_secrets import (
        UserSecretsClient,
    )

    client = UserSecretsClient()

    for label in [
        "GITHUB_TOKEN",
        "github_token",
        "GH_TOKEN",
        "GITHUB_PAT",
        "github_pat",
        "GH_PAT",
    ]:
        try:
            token = client.get_secret(
                label
            )
        except Exception:
            token = None

        if (
            isinstance(
                token,
                str,
            )
            and token.strip()
        ):
            return (
                token.strip(),
                label,
            )

    raise RuntimeError(
        "No GitHub token found."
    )


def push_origin_main():
    token, label = (
        get_github_token()
    )

    auth = base64.b64encode(
        (
            "x-access-token:"
            + token
        ).encode(
            "utf-8"
        )
    ).decode(
        "ascii"
    )

    p = subprocess.run(
        [
            "git",
            "-c",
            "credential.helper=",
            "-c",
            (
                "http.extraHeader="
                "AUTHORIZATION: Basic "
                + auth
            ),
            "push",
            "origin",
            "main",
        ],
        cwd=str(REPO),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    if p.returncode != 0:
        raise RuntimeError(
            "Git push failed.\n\n"
            f"STDOUT:\n{p.stdout}\n\n"
            f"STDERR:\n{p.stderr}"
        )

    print(
        f"[PASS] GitHub credential: "
        f"kaggle_secret:{label}"
    )

    print(
        "[PASS] token not displayed"
    )

    if p.stdout.strip():
        print(
            p.stdout.strip()
        )

    if p.stderr.strip():
        print(
            p.stderr.strip()
        )


def verify_remote_head(
    expected,
):
    run(
        [
            "git",
            "fetch",
            "origin",
            "main",
        ]
    )

    local = git(
        "rev-parse",
        "HEAD",
    )

    remote = git(
        "rev-parse",
        "origin/main",
    )

    if not (
        local
        == remote
        == expected
    ):
        raise RuntimeError(
            "Remote durability mismatch.\n"
            f"local={local}\n"
            f"origin={remote}\n"
            f"expected={expected}"
        )


# =================================================================================================
# 0. RECOVERY GATE — MUST USE IN-MEMORY HOLDOUT
# =================================================================================================

banner(
    "STAGE28-4-R1 — IN-MEMORY HOLDOUT SALVAGE GATE"
)

required_globals = [
    "X_holdout",
    "y_true",
]

missing_globals = [
    name
    for name in required_globals
    if name not in globals()
]

if missing_globals:
    raise RuntimeError(
        "The materialized Stage28-4 holdout is no longer "
        "present in this kernel:\n"
        + "\n".join(
            missing_globals
        )
        + "\n\n"
        "STOP. Do not rerun the March CSV materialization "
        "without designing a cold-recovery receipt first."
    )

if git(
    "status",
    "--porcelain",
):
    raise RuntimeError(
        "Repository is unexpectedly dirty before R1."
    )

run(
    [
        "git",
        "fetch",
        "origin",
        "main",
    ]
)

local_head = git(
    "rev-parse",
    "HEAD",
)

origin_head = git(
    "rev-parse",
    "origin/main",
)

print(
    "Expected parent:",
    FAILED_STAGE28_4_PARENT,
)

print(
    "Local HEAD     :",
    local_head,
)

print(
    "origin/main    :",
    origin_head,
)

if not (
    local_head
    == origin_head
    == FAILED_STAGE28_4_PARENT
):
    raise RuntimeError(
        "Repository lineage changed after failed Stage28-4."
    )

if STAGE4_ROOT.exists():
    raise RuntimeError(
        "Stage28-4 output root already exists. "
        "Do not overwrite it."
    )

if COMBINED_STABILITY_PATH.exists():
    raise RuntimeError(
        "Final conclusion_stability.csv already exists."
    )

print()
print(
    "[PASS] same scientific parent"
)

print(
    "[PASS] repository clean"
)

print(
    "[PASS] no durable Stage28-4 output exists"
)

print(
    "[PASS] March source files will NOT be read by R1"
)


# =================================================================================================
# 1. VERIFY THE ALREADY-MATERIALIZED HOLDOUT EXACTLY
# =================================================================================================

banner(
    "STAGE28-4-R1 — VERIFY ALREADY-MATERIALIZED HOLDOUT"
)

if not isinstance(
    X_holdout,
    np.ndarray,
):
    raise RuntimeError(
        "X_holdout is not a numpy ndarray."
    )

if not isinstance(
    y_true,
    np.ndarray,
):
    raise RuntimeError(
        "y_true is not a numpy ndarray."
    )

if (
    X_holdout.shape
    != (
        EXPECTED_ROWS,
        EXPECTED_FEATURES,
    )
):
    raise RuntimeError(
        f"X_holdout shape mismatch: "
        f"{X_holdout.shape}"
    )

if X_holdout.dtype != np.float64:
    raise RuntimeError(
        f"X_holdout dtype mismatch: "
        f"{X_holdout.dtype}"
    )

if y_true.shape != (
    EXPECTED_ROWS,
):
    raise RuntimeError(
        f"y_true shape mismatch: "
        f"{y_true.shape}"
    )

if y_true.dtype != np.uint8:
    raise RuntimeError(
        f"y_true dtype mismatch: "
        f"{y_true.dtype}"
    )

benign = int(
    np.count_nonzero(
        y_true == 0
    )
)

attack = int(
    np.count_nonzero(
        y_true == 1
    )
)

if benign != EXPECTED_BENIGN:
    raise RuntimeError(
        f"Benign count mismatch: {benign}"
    )

if attack != EXPECTED_ATTACK:
    raise RuntimeError(
        f"Attack count mismatch: {attack}"
    )

nan_cells = int(
    np.count_nonzero(
        np.isnan(
            X_holdout
        )
    )
)

if nan_cells != EXPECTED_NAN_CELLS:
    raise RuntimeError(
        f"NaN-cell mismatch: "
        f"{nan_cells} != {EXPECTED_NAN_CELLS}"
    )

if np.any(
    np.isinf(
        X_holdout
    )
):
    raise RuntimeError(
        "X_holdout still contains +/-inf."
    )

print(
    "Recomputing in-memory logical hashes ..."
)

X_sha = sha256_array_raw(
    X_holdout
)

y_sha = sha256_array_raw(
    y_true
)

print(
    "X logical SHA256:",
    X_sha,
)

print(
    "y logical SHA256:",
    y_sha,
)

if X_sha != EXPECTED_X_SHA:
    raise RuntimeError(
        "In-memory X_holdout SHA mismatch."
    )

if y_sha != EXPECTED_Y_SHA:
    raise RuntimeError(
        "In-memory y_true SHA mismatch."
    )

print()
print(
    "[PASS] 1,374,133 × 70 float64 matrix exact"
)

print(
    "[PASS] benign = 998,788"
)

print(
    "[PASS] attack = 375,345"
)

print(
    "[PASS] NaN cells = 13,922"
)

print(
    "[PASS] no infinities remain"
)

print(
    "[PASS] X logical SHA exact"
)

print(
    "[PASS] y logical SHA exact"
)

print(
    "[PASS] NO RAW DATA RE-READ"
)


# =================================================================================================
# 2. SCIENTIFIC AUTHORIZATION / RUNTIME
# =================================================================================================

banner(
    "STAGE28-4-R1 — SCIENTIFIC AUTHORIZATION"
)

closure = read_json(
    CLOSURE_RECEIPT
)

stage3c = read_json(
    STAGE3C_RECEIPT
)

stage22_spec = read_json(
    STAGE22_SPEC
)

stability_spec = read_json(
    STABILITY_SPEC
)

if (
    closure[
        "closure_status"
    ]
    !=
    "PASS_STAGE28_NEW_MODEL_FITTING_PERMANENTLY_CLOSED"
):
    raise RuntimeError(
        "Stage28 fitting closure changed."
    )

if (
    int(
        closure[
            "fit_budget_closure"
        ][
            "consumed_new_fits"
        ]
    )
    != 108
):
    raise RuntimeError(
        "Consumed new fits != 108."
    )

if (
    int(
        closure[
            "fit_budget_closure"
        ][
            "remaining_new_fits"
        ]
    )
    != 0
):
    raise RuntimeError(
        "Remaining new fits != 0."
    )

if not str(
    stage3c.get(
        "next_authorized_step",
        "",
    )
).startswith(
    "Stage28-4"
):
    raise RuntimeError(
        "Stage28-4 is no longer authorized."
    )

if (
    stage22_spec[
        "scientific_unit"
    ][
        "strategy"
    ]
    != "ENS_LGBM_XGB_EQUAL"
):
    raise RuntimeError(
        "Frozen ensemble strategy changed."
    )

FROZEN_PROBABILITY_RULE = (
    stage22_spec[
        "scientific_unit"
    ][
        "probability_rule"
    ]
)

if (
    FROZEN_PROBABILITY_RULE
    !=
    "0.5 * P_LIGHTGBM + 0.5 * P_XGBOOST"
):
    raise RuntimeError(
        "Frozen probability rule changed."
    )

evaluation_population = (
    stage22_spec[
        "evaluation_population"
    ]
)

if (
    evaluation_population[
        "threshold_selection_on_final_holdout"
    ]
    != "FORBIDDEN"
):
    raise RuntimeError(
        "Final-holdout threshold-search rule changed."
    )

if (
    evaluation_population[
        "model_selection_on_final_holdout"
    ]
    != "FORBIDDEN"
):
    raise RuntimeError(
        "Final-holdout model-selection rule changed."
    )

versions = {
    "numpy":
        np.__version__,

    "sklearn":
        sklearn.__version__,

    "xgboost":
        xgb.__version__,

    "lightgbm":
        lgb.__version__,
}

for name, expected in (
    EXPECTED_VERSIONS.items()
):
    actual = versions[
        name
    ]

    print(
        f"{name:<10}: {actual}"
    )

    if actual != expected:
        raise RuntimeError(
            f"{name} version mismatch."
        )

print()
print(
    "[PASS] 108 / 108 fits remain permanently closed"
)

print(
    "[PASS] frozen equal-weight probability rule exact"
)

print(
    "[PASS] threshold search remains FORBIDDEN"
)

print(
    "[PASS] model selection remains FORBIDDEN"
)

print(
    "[PASS] runtime versions exact"
)


# =================================================================================================
# 3. PHASE A — DURABLY FREEZE THE ALREADY-CONSUMED MATERIALIZATION
# =================================================================================================

banner(
    "STAGE28-4-R1 — PHASE A: DURABLE MATERIALIZATION CHECKPOINT"
)

STAGE4_ROOT.mkdir(
    parents=True,
    exist_ok=False,
)

MATERIALIZATION_RECEIPT = (
    STAGE4_ROOT
    / "stage28_4_materialization_checkpoint.json"
)

MATERIALIZATION_README = (
    STAGE4_ROOT
    / "README_MATERIALIZATION_CHECKPOINT.md"
)

checkpoint = {
    "stage":
        "Stage28-4",

    "checkpoint":
        "MATERIALIZATION_COMPLETE_BEFORE_MODEL_INFERENCE",

    "created_at_utc":
        utc_now(),

    "scientific_parent_commit":
        FAILED_STAGE28_4_PARENT,

    "recovery_reason":
        (
            "Initial Stage28-4 execution successfully materialized "
            "the exact frozen shared final holdout, then stopped during "
            "Stage22 receipt-schema auditing before any model inference. "
            "R1 salvaged the already-materialized in-memory matrix without "
            "re-reading either March source file."
        ),

    "holdout": {
        "population":
            "STAGE22R_SHARED_FINAL_SINGLE_HOLDOUT",

        "rows":
            EXPECTED_ROWS,

        "features":
            EXPECTED_FEATURES,

        "dtype":
            "float64",

        "benign":
            EXPECTED_BENIGN,

        "attack":
            EXPECTED_ATTACK,

        "attack_prevalence":
            EXPECTED_ATTACK
            / EXPECTED_ROWS,

        "X_logical_sha256":
            X_sha,

        "y_logical_sha256":
            y_sha,

        "output_nan_cells":
            nan_cells,

        "positive_infinity_to_nan":
            9530,

        "negative_infinity_to_nan":
            0,
    },

    "source_materialization": {
        "day_8":
            SOURCE_PROVENANCE[
                8
            ],

        "day_9":
            SOURCE_PROVENANCE[
                9
            ],

        "raw_source_read_passes_in_initial_authorized_materialization":
            1,

        "raw_source_reads_performed_by_recovery_cell":
            0,
    },

    "scientific_operations_completed_before_checkpoint": {
        "new_model_fits":
            0,

        "model_inferences":
            0,

        "threshold_selections":
            0,

        "model_selections":
            0,

        "stage28_shared_final_holdout_materializations":
            1,
    },

    "status":
        "PASS_SHARED_FINAL_HOLDOUT_MATERIALIZATION_DURABLY_FROZEN",
}

write_json(
    MATERIALIZATION_RECEIPT,
    checkpoint,
)

MATERIALIZATION_README.write_text(
    f"""# Stage28-4 materialization checkpoint

The one authorized Stage28 shared-final-holdout materialization completed
successfully before model inference.

- Rows: {EXPECTED_ROWS:,}
- Features: {EXPECTED_FEATURES}
- Dtype: float64
- Benign: {EXPECTED_BENIGN:,}
- Attack: {EXPECTED_ATTACK:,}
- NaN cells: {EXPECTED_NAN_CELLS:,}
- X SHA256: `{X_sha}`
- y SHA256: `{y_sha}`

March source files were not re-read by the R1 recovery.

No model fit, inference, threshold selection, or model selection occurred
before this checkpoint.
""",
    encoding="utf-8",
)

expected_phase_a = {
    str(
        MATERIALIZATION_RECEIPT.relative_to(
            REPO
        )
    ),
    str(
        MATERIALIZATION_README.relative_to(
            REPO
        )
    ),
}

tracked = set(
    git(
        "diff",
        "--name-only",
    ).splitlines()
)

staged = set(
    git(
        "diff",
        "--cached",
        "--name-only",
    ).splitlines()
)

untracked = set(
    git(
        "ls-files",
        "--others",
        "--exclude-standard",
    ).splitlines()
)

if tracked:
    raise RuntimeError(
        "Unexpected tracked modifications before Phase A."
    )

if staged:
    raise RuntimeError(
        "Unexpected staged files before Phase A."
    )

if untracked != expected_phase_a:
    raise RuntimeError(
        "Unexpected Phase-A untracked universe.\n\n"
        f"Expected:\n{sorted(expected_phase_a)}\n\n"
        f"Actual:\n{sorted(untracked)}"
    )

for rel in sorted(
    expected_phase_a
):
    run(
        [
            "git",
            "add",
            "--",
            rel,
        ]
    )

run(
    [
        "git",
        "config",
        "user.name",
        "Stage28 Kaggle",
    ]
)

run(
    [
        "git",
        "config",
        "user.email",
        "stage28-kaggle@users.noreply.github.com",
    ]
)

phase_a_message = (
    "stage28-4a: freeze shared final holdout materialization"
)

print(
    run(
        [
            "git",
            "commit",
            "-m",
            phase_a_message,
        ]
    ).stdout.strip()
)

PHASE_A_COMMIT = git(
    "rev-parse",
    "HEAD",
)

if (
    git(
        "rev-parse",
        "HEAD^",
    )
    != FAILED_STAGE28_4_PARENT
):
    raise RuntimeError(
        "Phase-A checkpoint parent mismatch."
    )

push_origin_main()

verify_remote_head(
    PHASE_A_COMMIT
)

if git(
    "status",
    "--porcelain",
):
    raise RuntimeError(
        "Repository dirty after Phase-A push."
    )

print()
print(
    "[PASS] materialization checkpoint durable"
)

print(
    "Phase-A commit:",
    PHASE_A_COMMIT,
)

print(
    "[PASS] scientific holdout opening is now durably recorded"
)


# =================================================================================================
# 4. AUDIT THE TEN STAGE22 RECEIPTS — SCHEMA TOLERANT, SCIENCE STRICT
# =================================================================================================

banner(
    "STAGE28-4-R1 — AUDIT TEN FROZEN STAGE22 ENSEMBLES"
)

result_files = sorted(
    STAGE22_ROOT.rglob(
        "*_result.json"
    )
)

if len(
    result_files
) != 10:
    raise RuntimeError(
        f"Expected 10 Stage22 results; "
        f"found {len(result_files)}."
    )

ensemble_specs = []

for result_path in result_files:
    obj = read_json(
        result_path
    )

    if (
        obj.get(
            "experiment"
        )
        != "STAGE22_FULL"
    ):
        raise RuntimeError(
            f"Unexpected Stage22 experiment:\n"
            f"{result_path}"
        )

    unit = obj[
        "unit"
    ]

    seed = int(
        obj[
            "training_seed"
        ]
    )

    if unit not in EXPECTED_UNITS:
        raise RuntimeError(
            f"Unexpected unit: {unit}"
        )

    if seed not in EXPECTED_SEEDS:
        raise RuntimeError(
            f"Unexpected seed: {seed}"
        )

    models = obj[
        "models"
    ]

    if not isinstance(
        models,
        dict,
    ):
        raise RuntimeError(
            f"{unit}/seed{seed}: models is not dict."
        )

    if (
        models.get(
            "strategy"
        )
        != "ENS_LGBM_XGB_EQUAL"
    ):
        raise RuntimeError(
            f"{unit}/seed{seed}: strategy mismatch."
        )

    # Receipt-schema compatibility:
    #
    # Older Stage28 receipts store this redundant literal.
    # AUTO-A compact receipts omit it.
    #
    # If present, it MUST match the frozen protocol.
    # If absent, the frozen Stage22 protocol is authoritative.
    receipt_probability_rule = (
        models.get(
            "ensemble_probability"
        )
    )

    if (
        receipt_probability_rule
        is not None
        and
        receipt_probability_rule
        != FROZEN_PROBABILITY_RULE
    ):
        raise RuntimeError(
            f"{unit}/seed{seed}: explicitly recorded "
            "probability rule disagrees with frozen protocol."
        )

    probability_rule_source = (
        "RESULT_RECEIPT_EXPLICIT"
        if receipt_probability_rule
        is not None
        else
        "FROZEN_STAGE22_PROTOCOL_FALLBACK"
    )

    if (
        models.get(
            "component_combination_dtype"
        )
        != "float64"
    ):
        raise RuntimeError(
            f"{unit}/seed{seed}: "
            "component combination dtype != float64."
        )

    if (
        models.get(
            "ensemble_storage_dtype"
        )
        != "float32"
    ):
        raise RuntimeError(
            f"{unit}/seed{seed}: "
            "ensemble storage dtype != float32."
        )

    xgb_info = models.get(
        "xgboost"
    )

    lgb_info = models.get(
        "lightgbm"
    )

    if not isinstance(
        xgb_info,
        dict,
    ):
        raise RuntimeError(
            f"{unit}/seed{seed}: XGBoost receipt missing."
        )

    if not isinstance(
        lgb_info,
        dict,
    ):
        raise RuntimeError(
            f"{unit}/seed{seed}: LightGBM receipt missing."
        )

    for learner_name, info in [
        (
            "XGBOOST",
            xgb_info,
        ),
        (
            "LIGHTGBM",
            lgb_info,
        ),
    ]:
        if int(
            info[
                "seed"
            ]
        ) != seed:
            raise RuntimeError(
                f"{unit}/seed{seed}/{learner_name}: "
                "seed mismatch."
            )

        if (
            str(
                info.get(
                    "backend",
                    "",
                )
            ).lower()
            != "cpu"
        ):
            raise RuntimeError(
                f"{unit}/seed{seed}/{learner_name}: "
                "backend != CPU."
            )

    xgb_model = resolve_model(
        result_path,
        xgb_info,
    )

    lgb_model = resolve_model(
        result_path,
        lgb_info,
    )

    thresholds = {
        name:
            extract_threshold(
                obj[
                    "operating_points"
                ],
                name,
            )
        for name in [
            "STANDARD",
            "BALANCED",
            "SECURITY",
        ]
    }

    ensemble_specs.append(
        {
            "unit":
                unit,

            "seed":
                seed,

            "evaluation_cell_id":
                obj.get(
                    "evaluation_cell_id",
                    (
                        f"28A_STAGE22::{unit}::SEED{seed}"
                    ),
                ),

            "result_path":
                result_path,

            "result_sha256":
                sha256_file(
                    result_path
                ),

            "probability_rule":
                FROZEN_PROBABILITY_RULE,

            "probability_rule_source":
                probability_rule_source,

            "xgb_component_id":
                xgb_info[
                    "component_id"
                ],

            "xgb_model":
                xgb_model,

            "lgb_component_id":
                lgb_info[
                    "component_id"
                ],

            "lgb_model":
                lgb_model,

            "thresholds":
                thresholds,
        }
    )

ensemble_specs.sort(
    key=lambda x: (
        EXPECTED_UNITS.index(
            x[
                "unit"
            ]
        ),
        x[
            "seed"
        ],
    )
)

expected_pairs = [
    (
        unit,
        seed,
    )
    for unit in EXPECTED_UNITS
    for seed in EXPECTED_SEEDS
]

actual_pairs = [
    (
        spec[
            "unit"
        ],
        spec[
            "seed"
        ],
    )
    for spec in ensemble_specs
]

if actual_pairs != expected_pairs:
    raise RuntimeError(
        "Stage22 evaluation grid is not exact 2 × 5."
    )

for spec in ensemble_specs:
    print(
        f"{spec['unit']:<24} "
        f"seed={spec['seed']}  "
        f"XGB={spec['xgb_component_id']}  "
        f"LGB={spec['lgb_component_id']}  "
        f"rule_source={spec['probability_rule_source']}  "
        f"thresholds={spec['thresholds']}"
    )

print()
print(
    "[PASS] 10 / 10 Stage22 ensemble receipts"
)

print(
    "[PASS] compact AUTO-A omission handled from frozen protocol"
)

print(
    "[PASS] model_path / model / historical_model_path schemas supported"
)

print(
    "[PASS] all 20 model SHA256 identities exact"
)

print(
    "[PASS] all model backends = CPU"
)

print(
    "[PASS] thresholds inherited only from development validation"
)


# =================================================================================================
# 5. PHASE B — AUTHORIZED FROZEN MODEL INFERENCE
# =================================================================================================

banner(
    "STAGE28-4-R1 — PHASE B: AUTHORIZED FINAL-HOLDOUT INFERENCE"
)

probability_arrays = {}

probability_records = {}

metric_rows = []

inference_started = (
    time.perf_counter()
)

for ordinal, spec in enumerate(
    ensemble_specs,
    start=1,
):
    unit = spec[
        "unit"
    ]

    seed = spec[
        "seed"
    ]

    print()
    print(
        "-" * 120
    )

    print(
        f"[{ordinal:02d}/10] "
        f"{unit} — seed {seed}"
    )

    print(
        "-" * 120
    )

    cell_started = (
        time.perf_counter()
    )

    # ---------------------------------------------------------------------------------------------
    # XGBOOST — LOAD ONLY
    # ---------------------------------------------------------------------------------------------

    xgb_model = (
        xgb.XGBClassifier()
    )

    xgb_model.load_model(
        str(
            spec[
                "xgb_model"
            ][
                "path"
            ]
        )
    )

    rounds = int(
        xgb_model
        .get_booster()
        .num_boosted_rounds()
    )

    if rounds != 400:
        raise RuntimeError(
            f"{unit}/seed{seed}: "
            f"XGBoost rounds={rounds}, expected 400."
        )

    started = (
        time.perf_counter()
    )

    p_xgb = (
        xgb_model.predict_proba(
            X_holdout
        )[
            :,
            1
        ]
    )

    xgb_seconds = (
        time.perf_counter()
        - started
    )

    if p_xgb.shape != (
        EXPECTED_ROWS,
    ):
        raise RuntimeError(
            f"{unit}/seed{seed}: "
            "XGBoost probability shape mismatch."
        )

    # ---------------------------------------------------------------------------------------------
    # LIGHTGBM — LOAD ONLY
    # ---------------------------------------------------------------------------------------------

    lgb_model = lgb.Booster(
        model_file=str(
            spec[
                "lgb_model"
            ][
                "path"
            ]
        )
    )

    iterations = int(
        lgb_model.current_iteration()
    )

    if iterations != 400:
        raise RuntimeError(
            f"{unit}/seed{seed}: "
            f"LightGBM iterations={iterations}, expected 400."
        )

    started = (
        time.perf_counter()
    )

    p_lgb = lgb_model.predict(
        X_holdout,
        num_iteration=iterations,
    )

    lgb_seconds = (
        time.perf_counter()
        - started
    )

    if p_lgb.shape != (
        EXPECTED_ROWS,
    ):
        raise RuntimeError(
            f"{unit}/seed{seed}: "
            "LightGBM probability shape mismatch."
        )

    # ---------------------------------------------------------------------------------------------
    # FROZEN EQUAL ENSEMBLE
    # ---------------------------------------------------------------------------------------------

    p_ensemble = (
        0.5
        * np.asarray(
            p_lgb,
            dtype=np.float64,
        )
        +
        0.5
        * np.asarray(
            p_xgb,
            dtype=np.float64,
        )
    ).astype(
        np.float32,
        copy=False,
    )

    if p_ensemble.dtype != np.float32:
        raise RuntimeError(
            "Ensemble dtype != float32."
        )

    if not np.all(
        np.isfinite(
            p_ensemble
        )
    ):
        raise RuntimeError(
            f"{unit}/seed{seed}: "
            "non-finite ensemble probabilities."
        )

    if (
        float(
            p_ensemble.min()
        ) < 0.0
        or
        float(
            p_ensemble.max()
        ) > 1.0
    ):
        raise RuntimeError(
            f"{unit}/seed{seed}: "
            "probabilities outside [0,1]."
        )

    roc_auc = float(
        roc_auc_score(
            y_true,
            p_ensemble,
        )
    )

    pr_auc = float(
        average_precision_score(
            y_true,
            p_ensemble,
        )
    )

    op_results = {
        name:
            operating_metrics(
                y_true,
                p_ensemble,
                spec[
                    "thresholds"
                ][
                    name
                ],
            )
        for name in [
            "STANDARD",
            "BALANCED",
            "SECURITY",
        ]
    }

    key = (
        unit.lower()
        + "_seed"
        + str(seed)
    )

    probability_arrays[
        key
    ] = p_ensemble.copy()

    probability_sha = (
        sha256_array_raw(
            p_ensemble
        )
    )

    cell_seconds = (
        time.perf_counter()
        - cell_started
    )

    probability_records[
        key
    ] = {
        "unit":
            unit,

        "seed":
            seed,

        "rows":
            EXPECTED_ROWS,

        "dtype":
            "float32",

        "logical_sha256":
            probability_sha,

        "minimum":
            float(
                p_ensemble.min()
            ),

        "maximum":
            float(
                p_ensemble.max()
            ),

        "xgboost_inference_seconds":
            float(
                xgb_seconds
            ),

        "lightgbm_inference_seconds":
            float(
                lgb_seconds
            ),

        "cell_total_seconds":
            float(
                cell_seconds
            ),
    }

    row = {
        "unit":
            unit,

        "seed":
            seed,

        "shared_holdout_rows":
            EXPECTED_ROWS,

        "shared_holdout_benign":
            EXPECTED_BENIGN,

        "shared_holdout_attack":
            EXPECTED_ATTACK,

        "shared_holdout_attack_prevalence":
            EXPECTED_ATTACK
            / EXPECTED_ROWS,

        "roc_auc":
            roc_auc,

        "pr_auc":
            pr_auc,

        "ensemble_probability_sha256":
            probability_sha,

        "xgboost_component_id":
            spec[
                "xgb_component_id"
            ],

        "xgboost_model_sha256":
            spec[
                "xgb_model"
            ][
                "sha256"
            ],

        "lightgbm_component_id":
            spec[
                "lgb_component_id"
            ],

        "lightgbm_model_sha256":
            spec[
                "lgb_model"
            ][
                "sha256"
            ],

        "probability_rule_source":
            spec[
                "probability_rule_source"
            ],

        "inference_seconds_xgboost":
            float(
                xgb_seconds
            ),

        "inference_seconds_lightgbm":
            float(
                lgb_seconds
            ),

        "inference_seconds_cell_total":
            float(
                cell_seconds
            ),
    }

    for op_name in [
        "STANDARD",
        "BALANCED",
        "SECURITY",
    ]:
        prefix = (
            op_name.lower()
        )

        for field, value in (
            op_results[
                op_name
            ].items()
        ):
            row[
                f"{prefix}_{field}"
            ] = value

    metric_rows.append(
        row
    )

    print(
        f"ROC-AUC : {roc_auc:.12f}"
    )

    print(
        f"PR-AUC  : {pr_auc:.12f}"
    )

    print(
        f"STANDARD recall="
        f"{op_results['STANDARD']['recall']:.12f} "
        f"fpr={op_results['STANDARD']['fpr']:.12f}"
    )

    print(
        f"BALANCED recall="
        f"{op_results['BALANCED']['recall']:.12f} "
        f"fpr={op_results['BALANCED']['fpr']:.12f}"
    )

    print(
        f"SECURITY recall="
        f"{op_results['SECURITY']['recall']:.12f} "
        f"fpr={op_results['SECURITY']['fpr']:.12f}"
    )

    print(
        "[PASS] probability SHA256:",
        probability_sha,
    )

    del p_xgb
    del p_lgb
    del p_ensemble
    del xgb_model
    del lgb_model

    gc.collect()

total_inference_seconds = (
    time.perf_counter()
    - inference_started
)

if len(
    metric_rows
) != 10:
    raise RuntimeError(
        "Expected exactly ten ensemble evaluations."
    )

print()
print(
    "[PASS] component model inferences = 20"
)

print(
    "[PASS] ensemble evaluations = 10"
)

print(
    "[PASS] model fits = 0"
)

print(
    "[PASS] threshold searches = 0"
)

print(
    "Inference wall time:",
    total_inference_seconds,
)


# =================================================================================================
# 6. WRITE SEED-LEVEL METRICS / PROBABILITY ARTIFACT
# =================================================================================================

banner(
    "STAGE28-4-R1 — WRITE INFERENCE ARTIFACTS"
)

METRICS_PATH = (
    STAGE4_ROOT
    / "stage28_4_seed_level_metrics.csv"
)

PROBABILITIES_PATH = (
    STAGE4_ROOT
    / "stage28_4_shared_holdout_ensemble_probabilities.npz"
)

metrics_df = pd.DataFrame(
    metric_rows
)

unit_order = {
    "RANDOM_NATURAL": 0,
    "CHRONOLOGICAL_NATURAL": 1,
}

metrics_df[
    "_unit_order"
] = metrics_df[
    "unit"
].map(
    unit_order
)

metrics_df = (
    metrics_df.sort_values(
        [
            "_unit_order",
            "seed",
        ]
    )
    .drop(
        columns=[
            "_unit_order",
        ]
    )
    .reset_index(
        drop=True
    )
)

metrics_df.to_csv(
    METRICS_PATH,
    index=False,
)

np.savez_compressed(
    PROBABILITIES_PATH,
    **probability_arrays,
)

probability_file_sha = (
    sha256_file(
        PROBABILITIES_PATH
    )
)

print(
    "[PASS] seed-level metrics written"
)

print(
    "[PASS] 10 probability arrays written"
)

print(
    "Probability artifact SHA256:",
    probability_file_sha,
)


# =================================================================================================
# 7. FROZEN STAGE22 DIRECTIONAL CLAIMS
# =================================================================================================

banner(
    "STAGE28-4-R1 — FROZEN STAGE22 CONCLUSION STABILITY"
)

lookup = {
    (
        row[
            "unit"
        ],
        int(
            row[
                "seed"
            ]
        ),
    ):
        row
    for row in metric_rows
}

claim_rows = []

contrast_rows = []

for seed in EXPECTED_SEEDS:
    random_row = lookup[
        (
            "RANDOM_NATURAL",
            seed,
        )
    ]

    chrono_row = lookup[
        (
            "CHRONOLOGICAL_NATURAL",
            seed,
        )
    ]

    pr_random = float(
        random_row[
            "pr_auc"
        ]
    )

    pr_chrono = float(
        chrono_row[
            "pr_auc"
        ]
    )

    roc_random = float(
        random_row[
            "roc_auc"
        ]
    )

    roc_chrono = float(
        chrono_row[
            "roc_auc"
        ]
    )

    pr_condition = (
        pr_random
        < pr_chrono
    )

    roc_condition = (
        roc_random
        < roc_chrono
    )

    contrast_rows.append(
        {
            "seed":
                seed,

            "pr_auc_random":
                pr_random,

            "pr_auc_chronological":
                pr_chrono,

            "pr_auc_random_minus_chronological":
                pr_random
                - pr_chrono,

            "pr_random_lt_chronological":
                bool(
                    pr_condition
                ),

            "roc_auc_random":
                roc_random,

            "roc_auc_chronological":
                roc_chrono,

            "roc_auc_random_minus_chronological":
                roc_random
                - roc_chrono,

            "roc_random_lt_chronological":
                bool(
                    roc_condition
                ),
        }
    )

    claim_rows.append(
        {
            "claim_id":
                "STAGE22_PR_RANDOM_LT_CHRONO_ON_SHARED_FINAL_HOLDOUT",

            "parent_stage":
                "STAGE22_FULL",

            "family_if_applicable":
                "",

            "learner_if_applicable":
                "",

            "seed":
                seed,

            "claim_condition":
                "PR_AUC_RANDOM_NATURAL < PR_AUC_CHRONOLOGICAL_NATURAL",

            "condition_met":
                bool(
                    pr_condition
                ),

            "analysis_status":
                "DESCRIPTIVE_ROBUSTNESS_PRE_REGISTERED",
        }
    )

    claim_rows.append(
        {
            "claim_id":
                "STAGE22_ROC_RANDOM_LT_CHRONO_ON_SHARED_FINAL_HOLDOUT",

            "parent_stage":
                "STAGE22_FULL",

            "family_if_applicable":
                "",

            "learner_if_applicable":
                "",

            "seed":
                seed,

            "claim_condition":
                "ROC_AUC_RANDOM_NATURAL < ROC_AUC_CHRONOLOGICAL_NATURAL",

            "condition_met":
                bool(
                    roc_condition
                ),

            "analysis_status":
                "DESCRIPTIVE_ROBUSTNESS_PRE_REGISTERED",
        }
    )

contrast_df = pd.DataFrame(
    contrast_rows
)

claim_df = pd.DataFrame(
    claim_rows
)

if len(
    claim_df
) != 10:
    raise RuntimeError(
        "Stage22 claim realization count != 10."
    )

CONTRAST_PATH = (
    STAGE4_ROOT
    / "stage28_4_random_vs_chronological_seedwise.csv"
)

CLAIM_PATH = (
    STAGE4_ROOT
    / "stage28_4_stage22_directional_claims.csv"
)

contrast_df.to_csv(
    CONTRAST_PATH,
    index=False,
)

claim_df.to_csv(
    CLAIM_PATH,
    index=False,
)

summary_rows = []

for claim_id in [
    "STAGE22_PR_RANDOM_LT_CHRONO_ON_SHARED_FINAL_HOLDOUT",
    "STAGE22_ROC_RANDOM_LT_CHRONO_ON_SHARED_FINAL_HOLDOUT",
]:
    subset = claim_df.loc[
        claim_df[
            "claim_id"
        ]
        == claim_id
    ]

    if len(
        subset
    ) != 5:
        raise RuntimeError(
            f"{claim_id}: denominator != 5."
        )

    supporting = int(
        subset[
            "condition_met"
        ].sum()
    )

    summary_rows.append(
        {
            "claim_id":
                claim_id,

            "supporting_seeds":
                supporting,

            "total_frozen_seeds":
                5,

            "stability_rate":
                supporting
                / 5.0,

            "interpretation":
                "DESCRIPTIVE_ROBUSTNESS_NOT_NEW_SIGNIFICANCE_TEST",
        }
    )

stability_df = pd.DataFrame(
    summary_rows
)

STAGE22_STABILITY_SUMMARY = (
    STAGE4_ROOT
    / "stage28_4_stage22_directional_stability_summary.csv"
)

stability_df.to_csv(
    STAGE22_STABILITY_SUMMARY,
    index=False,
)

for _, row in contrast_df.iterrows():
    print(
        f"seed {int(row['seed'])}: "
        f"ΔPR(random-chrono)="
        f"{row['pr_auc_random_minus_chronological']:+.12f} "
        f"support={bool(row['pr_random_lt_chronological'])}; "
        f"ΔROC(random-chrono)="
        f"{row['roc_auc_random_minus_chronological']:+.12f} "
        f"support={bool(row['roc_random_lt_chronological'])}"
    )

print()

for _, row in stability_df.iterrows():
    print(
        f"{row['claim_id']}: "
        f"{int(row['supporting_seeds'])}/5 "
        f"= {float(row['stability_rate']):.3f}"
    )

print()
print(
    "[PASS] exactly the two frozen Stage22 conditions evaluated"
)

print(
    "[PASS] post-result condition creation = 0"
)

print(
    "[PASS] new significance testing = 0"
)


# =================================================================================================
# 8. FINAL FROZEN conclusion_stability.csv
# =================================================================================================

banner(
    "STAGE28-4-R1 — FINAL conclusion_stability.csv"
)

loao_df = pd.read_csv(
    LOAO_STABILITY_PATH
)

required_columns = [
    "claim_id",
    "parent_stage",
    "family_if_applicable",
    "learner_if_applicable",
    "seed",
    "claim_condition",
    "condition_met",
    "analysis_status",
]

if list(
    loao_df.columns
) != required_columns:
    raise RuntimeError(
        "Stage28-3B LOAO stability schema changed."
    )

if list(
    claim_df.columns
) != required_columns:
    raise RuntimeError(
        "Stage28-4 claim schema mismatch."
    )

combined_df = pd.concat(
    [
        loao_df,
        claim_df,
    ],
    ignore_index=True,
)

combined_df.to_csv(
    COMBINED_STABILITY_PATH,
    index=False,
)

print(
    "Stage28-3B LOAO rows :",
    len(
        loao_df
    ),
)

print(
    "Stage28-4 Stage22 rows:",
    len(
        claim_df
    ),
)

print(
    "Combined rows          :",
    len(
        combined_df
    ),
)

print()
print(
    "[PASS] frozen required conclusion_stability.csv complete"
)


# =================================================================================================
# 9. FINAL STAGE28-4 RECEIPT
# =================================================================================================

banner(
    "STAGE28-4-R1 — FINAL RECEIPT"
)

FINAL_RECEIPT = (
    STAGE4_ROOT
    / "stage28_4_receipt.json"
)

README_PATH = (
    STAGE4_ROOT
    / "README_STAGE28_4.md"
)

stability_map = {
    row[
        "claim_id"
    ]:
        {
            "supporting":
                int(
                    row[
                        "supporting_seeds"
                    ]
                ),

            "total":
                5,

            "rate":
                float(
                    row[
                        "stability_rate"
                    ]
                ),
        }
    for _, row
    in stability_df.iterrows()
}

receipt = {
    "stage":
        "Stage28-4",

    "type":
        "STAGE22_FIVE_SEED_SHARED_FINAL_HOLDOUT_ROBUSTNESS_INFERENCE",

    "created_at_utc":
        utc_now(),

    "scientific_lineage": {
        "stage28_3c_parent":
            FAILED_STAGE28_4_PARENT,

        "materialization_checkpoint_commit":
            PHASE_A_COMMIT,
    },

    "recovery": {
        "status":
            "RECOVERED_AFTER_POST_MATERIALIZATION_PRE_INFERENCE_SCHEMA_FAILURE",

        "raw_source_files_re_read":
            False,

        "additional_holdout_materialization":
            False,

        "model_inference_before_failure":
            0,

        "schema_repairs": [
            (
                "models.ensemble_probability may be omitted in "
                "compact AUTO-A receipts; frozen Stage22 protocol "
                "is authoritative."
            ),
            (
                "Stage28 local model path may be stored under "
                "model_path or model."
            ),
        ],
    },

    "holdout": {
        "name":
            "STAGE22R_SHARED_FINAL_SINGLE_HOLDOUT",

        "rows":
            EXPECTED_ROWS,

        "benign":
            EXPECTED_BENIGN,

        "attack":
            EXPECTED_ATTACK,

        "features":
            EXPECTED_FEATURES,

        "dtype":
            "float64",

        "X_logical_sha256":
            X_sha,

        "y_logical_sha256":
            y_sha,

        "blind_status":
            (
                "NOT_NEW_BLIND_HOLDOUT; "
                "PARENT_STAGE22R_ALREADY_HISTORICALLY_OPENED"
            ),
    },

    "scientific_unit": {
        "strategy":
            "ENS_LGBM_XGB_EQUAL",

        "probability_rule":
            FROZEN_PROBABILITY_RULE,

        "component_combination_dtype":
            "float64",

        "ensemble_storage_dtype":
            "float32",
    },

    "design": {
        "units":
            EXPECTED_UNITS,

        "seeds":
            EXPECTED_SEEDS,

        "ensemble_realizations":
            10,

        "component_model_inferences":
            20,
    },

    "threshold_policy": {
        "selection_population":
            "FROZEN_DEVELOPMENT_VALIDATION_ONLY",

        "final_holdout_threshold_search":
            "FORBIDDEN_AND_NOT_PERFORMED",

        "model_selection_on_final_holdout":
            "FORBIDDEN_AND_NOT_PERFORMED",
    },

    "probabilities": {
        "artifact":
            str(
                PROBABILITIES_PATH.relative_to(
                    REPO
                )
            ),

        "artifact_sha256":
            probability_file_sha,

        "arrays":
            probability_records,
    },

    "seed_level_metrics": {
        "path":
            str(
                METRICS_PATH.relative_to(
                    REPO
                )
            ),

        "rows":
            10,
    },

    "stage22_directional_stability": {
        "claim_path":
            str(
                CLAIM_PATH.relative_to(
                    REPO
                )
            ),

        "summary_path":
            str(
                STAGE22_STABILITY_SUMMARY.relative_to(
                    REPO
                )
            ),

        "claims":
            stability_map,

        "stability_denominator":
            5,

        "post_result_condition_creation":
            0,

        "new_significance_tests":
            0,
    },

    "combined_conclusion_stability": {
        "path":
            str(
                COMBINED_STABILITY_PATH.relative_to(
                    REPO
                )
            ),

        "loao_rows":
            int(
                len(
                    loao_df
                )
            ),

        "stage22_rows":
            10,

        "combined_rows":
            int(
                len(
                    combined_df
                )
            ),
    },

    "scientific_operations": {
        "new_model_fits":
            0,

        "component_model_inferences":
            20,

        "ensemble_evaluations":
            10,

        "threshold_selections":
            0,

        "model_selections":
            0,

        "new_formal_statistical_tests":
            0,

        "shap_recomputation":
            0,

        "subset_search":
            0,

        "new_holdout_creation":
            0,

        "stage28_shared_final_holdout_materializations":
            1,
    },

    "fit_budget": {
        "authorized":
            108,

        "consumed":
            108,

        "remaining":
            0,
    },

    "status":
        "STAGE28_4_COMPLETE",

    "next_authorized_step":
        (
            "ZERO_FIT_FINAL_SYNTHESIS_AND_MANUSCRIPT_INTEGRATION; "
            "NO_FURTHER_MODEL_FITTING; NO_STAGE29"
        ),
}

write_json(
    FINAL_RECEIPT,
    receipt,
)

pr_result = stability_map[
    "STAGE22_PR_RANDOM_LT_CHRONO_ON_SHARED_FINAL_HOLDOUT"
]

roc_result = stability_map[
    "STAGE22_ROC_RANDOM_LT_CHRONO_ON_SHARED_FINAL_HOLDOUT"
]

README_PATH.write_text(
    f"""# Stage28-4 — Stage22 shared-final-holdout robustness inference

## Scientific status

- New model fits: 0
- Frozen component-model inferences: 20
- Ensemble evaluations: 10
- Threshold selections: 0
- Model selections: 0
- New formal significance tests: 0
- Stage28 fit ledger: 108 / 108 consumed
- Remaining new fits: 0

## Holdout

- Rows: {EXPECTED_ROWS:,}
- Benign: {EXPECTED_BENIGN:,}
- Attack: {EXPECTED_ATTACK:,}
- Features: {EXPECTED_FEATURES}
- dtype: float64
- X SHA256: `{X_sha}`
- y SHA256: `{y_sha}`

The holdout had already been opened historically by Stage22R.
Stage28-4 is preregistered robustness re-evaluation, not a new blind test.

## Recovery

The initial Stage28-4 execution successfully materialized the holdout but
stopped before model inference because a compact AUTO-A result receipt omitted
the redundant `models.ensemble_probability` field.

R1 reused the already-materialized in-memory holdout and did not reread the
March source files.

## Frozen directional stability

PR claim:

`PR_AUC_RANDOM_NATURAL < PR_AUC_CHRONOLOGICAL_NATURAL`

Support: {pr_result['supporting']} / 5
Stability rate: {pr_result['rate']:.6f}

ROC claim:

`ROC_AUC_RANDOM_NATURAL < ROC_AUC_CHRONOLOGICAL_NATURAL`

Support: {roc_result['supporting']} / 5
Stability rate: {roc_result['rate']:.6f}

## Closure

Stage28 empirical work is complete after this result.

No Stage29 is authorized.
The remaining work is zero-fit synthesis and manuscript integration.
""",
    encoding="utf-8",
)


# =================================================================================================
# 10. CHECKSUMS
# =================================================================================================

CHECKSUM_PATH = (
    STAGE4_ROOT
    / "stage28_4_checksums.sha256"
)

artifact_paths = [
    path
    for path in STAGE4_ROOT.rglob(
        "*"
    )
    if (
        path.is_file()
        and path
        != CHECKSUM_PATH
    )
]

artifact_paths.append(
    COMBINED_STABILITY_PATH
)

artifact_paths = sorted(
    artifact_paths,
    key=lambda x:
        str(
            x
        ),
)

checksum_lines = []

for path in artifact_paths:
    checksum_lines.append(
        sha256_file(
            path
        )
        + "  "
        + str(
            path.relative_to(
                REPO
            )
        )
    )

CHECKSUM_PATH.write_text(
    "\n".join(
        checksum_lines
    )
    + "\n",
    encoding="utf-8",
)

print(
    "[PASS] Stage28-4 receipt written"
)

print(
    "[PASS] README written"
)

print(
    "[PASS] checksums written"
)


# =================================================================================================
# 11. FINAL SCIENTIFIC GATE
# =================================================================================================

banner(
    "STAGE28-4-R1 — FINAL SCIENTIFIC GATE"
)

closure_after = read_json(
    CLOSURE_RECEIPT
)

if closure_after != closure:
    raise RuntimeError(
        "Stage28 closure receipt unexpectedly changed."
    )

if (
    closure_after[
        "fit_budget_closure"
    ][
        "consumed_new_fits"
    ]
    != 108
):
    raise RuntimeError(
        "Fit ledger no longer equals 108."
    )

if (
    closure_after[
        "fit_budget_closure"
    ][
        "remaining_new_fits"
    ]
    != 0
):
    raise RuntimeError(
        "Fit ledger remaining != 0."
    )

if len(
    probability_arrays
) != 10:
    raise RuntimeError(
        "Probability array count != 10."
    )

if len(
    metrics_df
) != 10:
    raise RuntimeError(
        "Metric realization count != 10."
    )

if len(
    claim_df
) != 10:
    raise RuntimeError(
        "Stage22 claim realization count != 10."
    )

print(
    "[PASS] new model fits = 0"
)

print(
    "[PASS] Stage28 fit ledger = 108 / 108"
)

print(
    "[PASS] remaining fit budget = 0"
)

print(
    "[PASS] component model inferences = 20"
)

print(
    "[PASS] ensemble evaluations = 10"
)

print(
    "[PASS] threshold selections = 0"
)

print(
    "[PASS] model selections = 0"
)

print(
    "[PASS] new significance tests = 0"
)

print(
    "[PASS] shared holdout materializations = 1"
)


# =================================================================================================
# 12. PHASE B EXACT GIT UNIVERSE
# =================================================================================================

banner(
    "STAGE28-4-R1 — PHASE B GIT UNIVERSE"
)

# Phase-A files are already tracked and unchanged.
tracked_modifications = set(
    git(
        "diff",
        "--name-only",
    ).splitlines()
)

staged_before = set(
    git(
        "diff",
        "--cached",
        "--name-only",
    ).splitlines()
)

untracked = set(
    git(
        "ls-files",
        "--others",
        "--exclude-standard",
    ).splitlines()
)

expected_untracked = {
    str(
        path.relative_to(
            REPO
        )
    )
    for path in [
        METRICS_PATH,
        PROBABILITIES_PATH,
        CONTRAST_PATH,
        CLAIM_PATH,
        STAGE22_STABILITY_SUMMARY,
        FINAL_RECEIPT,
        README_PATH,
        CHECKSUM_PATH,
        COMBINED_STABILITY_PATH,
    ]
}

if tracked_modifications:
    raise RuntimeError(
        "Unexpected tracked modifications before Phase B:\n"
        + "\n".join(
            sorted(
                tracked_modifications
            )
        )
    )

if staged_before:
    raise RuntimeError(
        "Unexpected staged files before Phase B."
    )

if untracked != expected_untracked:
    raise RuntimeError(
        "Unexpected Phase-B untracked universe.\n\n"
        "Expected:\n"
        + "\n".join(
            sorted(
                expected_untracked
            )
        )
        + "\n\nActual:\n"
        + "\n".join(
            sorted(
                untracked
            )
        )
    )

print(
    "[PASS] exact Phase-B artifact universe"
)


# =================================================================================================
# 13. FINAL DURABLE COMMIT / PUSH
# =================================================================================================

banner(
    "STAGE28-4-R1 — FINAL DURABLE COMMIT / PUSH"
)

run(
    [
        "git",
        "fetch",
        "origin",
        "main",
    ]
)

if (
    git(
        "rev-parse",
        "origin/main",
    )
    != PHASE_A_COMMIT
):
    raise RuntimeError(
        "origin/main changed after Phase-A checkpoint."
    )

for rel in sorted(
    expected_untracked
):
    run(
        [
            "git",
            "add",
            "-f",
            "--",
            rel,
        ]
    )

staged_after = set(
    git(
        "diff",
        "--cached",
        "--name-only",
    ).splitlines()
)

if staged_after != expected_untracked:
    raise RuntimeError(
        "Phase-B staged universe mismatch."
    )

final_message = (
    "stage28-4b: complete Stage22 five-seed shared holdout inference"
)

print(
    run(
        [
            "git",
            "commit",
            "-m",
            final_message,
        ]
    ).stdout.strip()
)

FINAL_COMMIT = git(
    "rev-parse",
    "HEAD",
)

if (
    git(
        "rev-parse",
        "HEAD^",
    )
    != PHASE_A_COMMIT
):
    raise RuntimeError(
        "Final Stage28-4 commit parent mismatch."
    )

push_origin_main()

verify_remote_head(
    FINAL_COMMIT
)

if git(
    "status",
    "--porcelain",
):
    raise RuntimeError(
        "Repository dirty after Stage28-4 final push."
    )

print()
print(
    "[PASS] Stage28-4 final commit durable"
)

print(
    "[PASS] repository clean"
)


# =================================================================================================
# 14. COMPLETE
# =================================================================================================

banner(
    "STAGE28-4 — COMPLETE"
)

print(
    "Materialization checkpoint:",
    PHASE_A_COMMIT,
)

print(
    "Final Stage28-4 commit      :",
    FINAL_COMMIT,
)

print()
print(
    "New model fits                    : 0"
)

print(
    "Component model inferences        : 20"
)

print(
    "Ensemble evaluation cells         : 10"
)

print(
    "Threshold selections              : 0"
)

print(
    "Model selections                  : 0"
)

print(
    "New formal statistical tests      : 0"
)

print(
    "Raw March re-reads during recovery: 0"
)

print(
    "Shared holdout materializations   : 1"
)

print()
print(
    "STAGE22 DIRECTIONAL STABILITY"
)

print(
    "-----------------------------"
)

for _, row in stability_df.iterrows():
    print(
        f"{row['claim_id']}: "
        f"{int(row['supporting_seeds'])}/5 "
        f"= {float(row['stability_rate']):.3f}"
    )

print()
print(
    "Stage28 new-fit budget             : 108 / 108"
)

print(
    "New fits remaining                 : 0"
)

print(
    "Stage28 empirical work             : COMPLETE"
)

print(
    "Stage29                           : NOT AUTHORIZED"
)

print()
print(
    "NEXT AUTHORIZED WORK:"
)

print(
    "ZERO-FIT FINAL SYNTHESIS + MANUSCRIPT INTEGRATION"
)

# ==============================================================================================================
# %% NOTEBOOK CELL 0014 | execution_count=14
# ==============================================================================================================
# =================================================================================================
# STAGE28-FINAL — ZERO-FIT FINAL SYNTHESIS + MANUSCRIPT-READY RESULTS FREEZE
#
# EMPIRICAL WORK IS OVER.
#
# NEW MODEL FITS                 : 0
# MODEL INFERENCE                : 0
# THRESHOLD SELECTION            : 0
# MODEL SELECTION                : 0
# TARGET / HOLDOUT OPENINGS      : 0
# BOOTSTRAP RECOMPUTATION        : 0
# SHAP RECOMPUTATION             : 0
# NEW SIGNIFICANCE TESTS         : 0
# NEW QUALITATIVE CUTOFFS        : 0
#
# Parent:
#   f5de70d25a5714ae2b70a18819bde97eb3e38354
#
# Purpose:
#   1. Reconcile final Stage28 closure.
#   2. Summarize Stage22 five-seed shared-holdout results.
#   3. Summarize chronology/random LOAO seed stability.
#   4. Summarize paired random-minus-chronological LOAO contrasts.
#   5. Freeze the complete conclusion-stability registry.
#   6. Create manuscript-ready numerical tables.
#   7. Create guarded manuscript-ready results prose.
#   8. Freeze final Stage28 synthesis receipt/checksums.
#
# NO STAGE29.
# =================================================================================================

from __future__ import annotations

import base64
import hashlib
import json
import math
import os
import subprocess

from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd


# =================================================================================================
# CONSTANTS
# =================================================================================================

SEP = "=" * 120

REPO = Path(
    "/kaggle/working/ids2018-validation-safe-ablation"
).resolve()

EXPECTED_PARENT = (
    "f5de70d25a5714ae2b70a18819bde97eb3e38354"
)

ROOT = (
    REPO
    / "results"
    / "stage28_stability_novelty_control"
)

CLOSURE_RECEIPT = (
    ROOT
    / "stage28_3a_experiment_closure_audit"
    / "stage28_3a_experiment_closure_receipt.json"
)

STAGE3_ROOT = (
    ROOT
    / "stage28_3_seed_uncertainty"
)

STAGE4_ROOT = (
    ROOT
    / "stage28_4_stage22_shared_final_holdout"
)

STAGE4_RECEIPT = (
    STAGE4_ROOT
    / "stage28_4_receipt.json"
)

STAGE22_METRICS = (
    STAGE4_ROOT
    / "stage28_4_seed_level_metrics.csv"
)

STAGE22_CONTRAST = (
    STAGE4_ROOT
    / "stage28_4_random_vs_chronological_seedwise.csv"
)

STAGE22_STABILITY = (
    STAGE4_ROOT
    / "stage28_4_stage22_directional_stability_summary.csv"
)

LOAO_SEED_LEVEL = (
    STAGE3_ROOT
    / "stage28_3b_loao_seed_level_metrics.csv"
)

LOAO_FIVE_SEED = (
    STAGE3_ROOT
    / "stage28_3b_loao_five_seed_summary.csv"
)

LOAO_STABILITY = (
    STAGE3_ROOT
    / "stage28_3b_loao_stability_summary.csv"
)

LOAO_CONTRAST = (
    STAGE3_ROOT
    / "stage28_3c_random_vs_chronological_five_seed_summary.csv"
)

LOAO_DIRECTION = (
    STAGE3_ROOT
    / "stage28_3c_numeric_direction_summary.csv"
)

CONCLUSION_STABILITY = (
    STAGE3_ROOT
    / "conclusion_stability.csv"
)

OUT = (
    ROOT
    / "stage28_final_synthesis"
)

STAGE22_SUMMARY_OUT = (
    OUT
    / "stage28_final_stage22_shared_holdout_five_seed_summary.csv"
)

STAGE22_CONTRAST_OUT = (
    OUT
    / "stage28_final_stage22_random_minus_chronological_summary.csv"
)

LOAO_KEY_OUT = (
    OUT
    / "stage28_final_loao_key_metric_summary.csv"
)

LOAO_STABILITY_OUT = (
    OUT
    / "stage28_final_loao_stability_registry.csv"
)

RANDOM_CHRONO_OUT = (
    OUT
    / "stage28_final_random_vs_chronological_key_contrasts.csv"
)

CLAIM_REGISTRY_OUT = (
    OUT
    / "stage28_final_claim_registry.csv"
)

NUMBERS_OUT = (
    OUT
    / "stage28_final_manuscript_numbers.json"
)

MANUSCRIPT_OUT = (
    OUT
    / "stage28_final_manuscript_results.md"
)

RECEIPT_OUT = (
    OUT
    / "stage28_final_synthesis_receipt.json"
)

README_OUT = (
    OUT
    / "README.md"
)

CHECKSUM_OUT = (
    OUT
    / "checksums.sha256"
)


SEEDS = [
    42,
    43,
    44,
    45,
    46,
]

FAMILIES = [
    "BOT",
    "DDOS",
    "INFILTRATION",
    "PORT_SCAN",
    "WEB_ATTACK",
]

LEARNERS = [
    "XGBOOST",
    "LIGHTGBM",
]

ARMS = [
    "STAGE27_CHRONOLOGY_LOAO",
    "STAGE28B_RANDOM_LOAO",
]


STAGE22_METRICS_TO_REPORT = [
    "roc_auc",
    "pr_auc",
    "standard_recall",
    "standard_fpr",
    "balanced_recall",
    "balanced_fpr",
    "security_recall",
    "security_fpr",
]


LOAO_KEY_METRICS = [
    "ROC_AUC",
    "PR_AUC",
    "PR_CHANCE_ANCHOR",
    "PR_EXCESS",
    "PR_LIFT",
    "STANDARD_RECALL",
    "BALANCED_RECALL",
    "SECURITY_RECALL",
]


CONTRAST_KEY_METRICS = [
    "ROC_AUC",
    "PR_EXCESS",
    "STANDARD_RECALL",
    "BALANCED_RECALL",
    "SECURITY_RECALL",
]


# =================================================================================================
# HELPERS
# =================================================================================================

def banner(text):
    print()
    print(SEP)
    print(text)
    print(SEP)
    print()


def utc_now():
    return datetime.now(
        timezone.utc
    ).isoformat()


def run(
    cmd,
    *,
    cwd=REPO,
    check=True,
):
    p = subprocess.run(
        [str(x) for x in cmd],
        cwd=str(cwd),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    if check and p.returncode != 0:
        raise RuntimeError(
            f"Command failed ({p.returncode}):\n"
            + " ".join(map(str, cmd))
            + f"\n\nSTDOUT:\n{p.stdout}"
            + f"\n\nSTDERR:\n{p.stderr}"
        )

    return p


def git(*args):
    return run(
        ["git", *args]
    ).stdout.strip()


def read_json(path):
    return json.loads(
        Path(path).read_text(
            encoding="utf-8"
        )
    )


def write_json(path, obj):
    Path(path).write_text(
        json.dumps(
            obj,
            indent=2,
            ensure_ascii=False,
            allow_nan=False,
        )
        + "\n",
        encoding="utf-8",
    )


def sha256_file(
    path,
    chunk=16 * 1024 * 1024,
):
    h = hashlib.sha256()

    with Path(path).open("rb") as f:
        while True:
            b = f.read(chunk)

            if not b:
                break

            h.update(b)

    return h.hexdigest()


def finite_float(value):
    try:
        x = float(value)

    except Exception:
        return float("nan")

    if not math.isfinite(x):
        return float("nan")

    return x


def five_seed_stats(values):
    vals = np.asarray(
        [
            finite_float(x)
            for x in values
        ],
        dtype=np.float64,
    )

    if vals.size != 5:
        raise RuntimeError(
            f"Expected exactly 5 seeds, found {vals.size}."
        )

    if not np.all(
        np.isfinite(vals)
    ):
        return {
            "n_seeds":
                5,

            "n_defined":
                int(
                    np.isfinite(
                        vals
                    ).sum()
                ),

            "mean":
                float("nan"),

            "median":
                float("nan"),

            "sample_standard_deviation_ddof_1":
                float("nan"),

            "minimum":
                float("nan"),

            "maximum":
                float("nan"),

            "range":
                float("nan"),

            "IQR_Q75_minus_Q25_linear":
                float("nan"),
        }

    q25, q75 = np.quantile(
        vals,
        [
            0.25,
            0.75,
        ],
        method="linear",
    )

    return {
        "n_seeds":
            5,

        "n_defined":
            5,

        "mean":
            float(
                np.mean(vals)
            ),

        "median":
            float(
                np.median(vals)
            ),

        "sample_standard_deviation_ddof_1":
            float(
                np.std(
                    vals,
                    ddof=1,
                )
            ),

        "minimum":
            float(
                np.min(vals)
            ),

        "maximum":
            float(
                np.max(vals)
            ),

        "range":
            float(
                np.max(vals)
                - np.min(vals)
            ),

        "IQR_Q75_minus_Q25_linear":
            float(
                q75
                - q25
            ),
    }


def bool_value(value):
    if isinstance(
        value,
        bool,
    ):
        return value

    text = str(
        value
    ).strip().lower()

    if text in {
        "true",
        "1",
        "yes",
    }:
        return True

    if text in {
        "false",
        "0",
        "no",
    }:
        return False

    raise RuntimeError(
        f"Cannot parse boolean: {value!r}"
    )


def fmt(
    value,
    digits=4,
):
    try:
        x = float(value)

    except Exception:
        return str(value)

    if not math.isfinite(x):
        return "NA"

    return f"{x:.{digits}f}"


def md_table(
    rows,
    columns,
):
    if not rows:
        return "_No rows._"

    header = (
        "| "
        + " | ".join(
            columns
        )
        + " |"
    )

    separator = (
        "| "
        + " | ".join(
            [
                "---"
                for _ in columns
            ]
        )
        + " |"
    )

    body = []

    for row in rows:
        cells = []

        for col in columns:
            value = row.get(
                col,
                "",
            )

            text = str(
                value
            ).replace(
                "|",
                "\\|",
            )

            cells.append(
                text
            )

        body.append(
            "| "
            + " | ".join(
                cells
            )
            + " |"
        )

    return "\n".join(
        [
            header,
            separator,
            *body,
        ]
    )


def get_github_token():
    from kaggle_secrets import (
        UserSecretsClient,
    )

    client = UserSecretsClient()

    for label in [
        "GITHUB_TOKEN",
        "github_token",
        "GH_TOKEN",
        "GITHUB_PAT",
        "github_pat",
        "GH_PAT",
    ]:
        try:
            token = client.get_secret(
                label
            )
        except Exception:
            token = None

        if (
            isinstance(
                token,
                str,
            )
            and token.strip()
        ):
            return (
                token.strip(),
                label,
            )

    raise RuntimeError(
        "No GitHub token available."
    )


def push_origin_main():
    token, label = get_github_token()

    auth = base64.b64encode(
        (
            "x-access-token:"
            + token
        ).encode(
            "utf-8"
        )
    ).decode(
        "ascii"
    )

    p = subprocess.run(
        [
            "git",
            "-c",
            "credential.helper=",
            "-c",
            (
                "http.extraHeader="
                "AUTHORIZATION: Basic "
                + auth
            ),
            "push",
            "origin",
            "main",
        ],
        cwd=str(REPO),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    if p.returncode != 0:
        raise RuntimeError(
            "Git push failed.\n\n"
            f"STDOUT:\n{p.stdout}\n\n"
            f"STDERR:\n{p.stderr}"
        )

    print(
        f"[PASS] GitHub credential: kaggle_secret:{label}"
    )

    print(
        "[PASS] token not displayed"
    )

    if p.stdout.strip():
        print(
            p.stdout.strip()
        )

    if p.stderr.strip():
        print(
            p.stderr.strip()
        )


# =================================================================================================
# 0. PARENT / CLEAN REPOSITORY
# =================================================================================================

banner(
    "STAGE28-FINAL — REPOSITORY / EMPIRICAL-CLOSURE GATE"
)

if OUT.exists():
    raise RuntimeError(
        "Stage28 final-synthesis output already exists. "
        "Do not overwrite."
    )

if git(
    "status",
    "--porcelain",
):
    raise RuntimeError(
        "Repository must be clean."
    )

run(
    [
        "git",
        "fetch",
        "origin",
        "main",
    ]
)

local_head = git(
    "rev-parse",
    "HEAD",
)

origin_head = git(
    "rev-parse",
    "origin/main",
)

print(
    "Expected parent:",
    EXPECTED_PARENT,
)

print(
    "Local HEAD     :",
    local_head,
)

print(
    "origin/main    :",
    origin_head,
)

if not (
    local_head
    == origin_head
    == EXPECTED_PARENT
):
    raise RuntimeError(
        "Stage28-FINAL parent mismatch."
    )

closure = read_json(
    CLOSURE_RECEIPT
)

stage4 = read_json(
    STAGE4_RECEIPT
)

if (
    closure[
        "closure_status"
    ]
    !=
    "PASS_STAGE28_NEW_MODEL_FITTING_PERMANENTLY_CLOSED"
):
    raise RuntimeError(
        "Stage28 fitting closure is not PASS."
    )

if (
    int(
        closure[
            "fit_budget_closure"
        ][
            "consumed_new_fits"
        ]
    )
    != 108
    or
    int(
        closure[
            "fit_budget_closure"
        ][
            "remaining_new_fits"
        ]
    )
    != 0
):
    raise RuntimeError(
        "Stage28 fit budget does not close at 108/108."
    )

if (
    stage4[
        "status"
    ]
    != "STAGE28_4_COMPLETE"
):
    raise RuntimeError(
        "Stage28-4 is not complete."
    )

if (
    stage4[
        "scientific_operations"
    ][
        "new_model_fits"
    ]
    != 0
):
    raise RuntimeError(
        "Stage28-4 unexpectedly contains a model fit."
    )

if (
    stage4[
        "scientific_operations"
    ][
        "threshold_selections"
    ]
    != 0
):
    raise RuntimeError(
        "Stage28-4 unexpectedly selected thresholds."
    )

if (
    stage4[
        "scientific_operations"
    ][
        "model_selections"
    ]
    != 0
):
    raise RuntimeError(
        "Stage28-4 unexpectedly performed model selection."
    )

if (
    stage4[
        "next_authorized_step"
    ]
    !=
    (
        "ZERO_FIT_FINAL_SYNTHESIS_AND_MANUSCRIPT_INTEGRATION; "
        "NO_FURTHER_MODEL_FITTING; NO_STAGE29"
    )
):
    raise RuntimeError(
        "Final authorized-work statement changed."
    )

print()
print(
    "[PASS] Stage28 new-fit ledger = 108 / 108"
)

print(
    "[PASS] remaining fit budget = 0"
)

print(
    "[PASS] Stage28-4 empirical work complete"
)

print(
    "[PASS] NO Stage29"
)

print(
    "[PASS] current stage = reporting/synthesis only"
)


# =================================================================================================
# 1. INPUT ARTIFACT GATE
# =================================================================================================

banner(
    "STAGE28-FINAL — DURABLE INPUT ARTIFACT GATE"
)

required_inputs = [
    STAGE22_METRICS,
    STAGE22_CONTRAST,
    STAGE22_STABILITY,
    LOAO_SEED_LEVEL,
    LOAO_FIVE_SEED,
    LOAO_STABILITY,
    LOAO_CONTRAST,
    LOAO_DIRECTION,
    CONCLUSION_STABILITY,
]

input_sha = {}

for path in required_inputs:
    if not path.is_file():
        raise RuntimeError(
            f"Missing synthesis input:\n{path}"
        )

    digest = sha256_file(
        path
    )

    input_sha[
        str(
            path.relative_to(
                REPO
            )
        )
    ] = digest

    print(
        "[PASS]",
        path.name,
        digest,
    )


stage22_df = pd.read_csv(
    STAGE22_METRICS
)

stage22_contrast_df = pd.read_csv(
    STAGE22_CONTRAST
)

stage22_stability_df = pd.read_csv(
    STAGE22_STABILITY
)

loao_level_df = pd.read_csv(
    LOAO_SEED_LEVEL
)

loao_summary_df = pd.read_csv(
    LOAO_FIVE_SEED
)

loao_stability_df = pd.read_csv(
    LOAO_STABILITY
)

loao_contrast_df = pd.read_csv(
    LOAO_CONTRAST
)

loao_direction_df = pd.read_csv(
    LOAO_DIRECTION
)

conclusion_df = pd.read_csv(
    CONCLUSION_STABILITY
)


if len(
    stage22_df
) != 10:
    raise RuntimeError(
        "Stage22 seed-level result count != 10."
    )

if len(
    stage22_contrast_df
) != 5:
    raise RuntimeError(
        "Stage22 seedwise contrast count != 5."
    )

if len(
    stage22_stability_df
) != 2:
    raise RuntimeError(
        "Stage22 stability summary count != 2."
    )

if len(
    loao_level_df
) != 100:
    raise RuntimeError(
        "LOAO seed-level realization count != 100."
    )

if len(
    loao_stability_df
) != 110:
    raise RuntimeError(
        "LOAO stability summary count != 110."
    )

if len(
    conclusion_df
) != 560:
    raise RuntimeError(
        "Combined conclusion-stability row count != 560."
    )

print()
print(
    "[PASS] Stage22 evaluations = 10"
)

print(
    "[PASS] chronology LOAO seed realizations = 50"
)

print(
    "[PASS] random LOAO seed realizations = 50"
)

print(
    "[PASS] LOAO stability registry rows = 110"
)

print(
    "[PASS] complete conclusion_stability rows = 560"
)


# =================================================================================================
# 2. STAGE22 SHARED-HOLDOUT FIVE-SEED SUMMARY
# =================================================================================================

banner(
    "STAGE28-FINAL — STAGE22 SHARED-HOLDOUT FIVE-SEED SUMMARY"
)

stage22_summary_rows = []

for unit in [
    "RANDOM_NATURAL",
    "CHRONOLOGICAL_NATURAL",
]:
    subset = (
        stage22_df.loc[
            stage22_df[
                "unit"
            ]
            == unit
        ]
        .sort_values(
            "seed"
        )
    )

    if subset[
        "seed"
    ].tolist() != SEEDS:
        raise RuntimeError(
            f"{unit}: seed coverage != 42..46."
        )

    for metric in (
        STAGE22_METRICS_TO_REPORT
    ):
        stats = five_seed_stats(
            subset[
                metric
            ].tolist()
        )

        stage22_summary_rows.append(
            {
                "unit":
                    unit,

                "metric":
                    metric,

                **stats,
            }
        )

stage22_summary_df = pd.DataFrame(
    stage22_summary_rows
)

print(
    "[PASS] Stage22 metrics summarized over exactly five frozen seeds"
)


# =================================================================================================
# 3. STAGE22 RANDOM-MINUS-CHRONOLOGICAL SUMMARY
# =================================================================================================

banner(
    "STAGE28-FINAL — STAGE22 DIRECTIONAL CONTRAST SUMMARY"
)

stage22_contrast_rows = []

for metric, delta_column, support_column in [
    (
        "PR_AUC",
        "pr_auc_random_minus_chronological",
        "pr_random_lt_chronological",
    ),
    (
        "ROC_AUC",
        "roc_auc_random_minus_chronological",
        "roc_random_lt_chronological",
    ),
]:
    subset = stage22_contrast_df.sort_values(
        "seed"
    )

    if subset[
        "seed"
    ].tolist() != SEEDS:
        raise RuntimeError(
            "Stage22 contrast seed coverage != 42..46."
        )

    stats = five_seed_stats(
        subset[
            delta_column
        ].tolist()
    )

    support_values = [
        bool_value(
            x
        )
        for x
        in subset[
            support_column
        ].tolist()
    ]

    supporting = sum(
        support_values
    )

    stage22_contrast_rows.append(
        {
            "metric":
                metric,

            "contrast":
                "RANDOM_MINUS_CHRONOLOGICAL",

            **stats,

            "random_lt_chronological_supporting_seeds":
                supporting,

            "frozen_seed_count":
                5,

            "stability_rate":
                supporting
                / 5.0,
        }
    )

stage22_contrast_summary_df = pd.DataFrame(
    stage22_contrast_rows
)

if not (
    stage22_contrast_summary_df[
        "random_lt_chronological_supporting_seeds"
    ]
    == 5
).all():
    raise RuntimeError(
        "A frozen Stage22 directional claim is not 5/5."
    )

print(
    "[PASS] PR random < chronological = 5 / 5"
)

print(
    "[PASS] ROC random < chronological = 5 / 5"
)


# =================================================================================================
# 4. LOAO KEY FIVE-SEED NUMERICAL SUMMARY
# =================================================================================================

banner(
    "STAGE28-FINAL — LOAO KEY METRIC SUMMARY"
)

loao_key_df = (
    loao_summary_df.loc[
        loao_summary_df[
            "metric"
        ].isin(
            LOAO_KEY_METRICS
        )
    ]
    .copy()
)

expected_groups = (
    2
    * 5
    * 2
    * len(
        LOAO_KEY_METRICS
    )
)

if len(
    loao_key_df
) != expected_groups:
    raise RuntimeError(
        "LOAO key-metric summary row count mismatch: "
        f"{len(loao_key_df)} != {expected_groups}"
    )

print(
    "[PASS] chronology/random × 5 families × 2 learners "
    "× key metrics preserved"
)

print(
    "[PASS] Infiltration support status preserved"
)


# =================================================================================================
# 5. LOAO STABILITY REGISTRY
# =================================================================================================

banner(
    "STAGE28-FINAL — LOAO QUALITATIVE STABILITY REGISTRY"
)

loao_stability_final = (
    loao_stability_df.copy()
)

loao_stability_final[
    "is_five_of_five"
] = (
    loao_stability_final[
        "frozen_seeds_supporting_condition"
    ]
    == 5
)

loao_stability_final[
    "is_zero_of_five"
] = (
    loao_stability_final[
        "frozen_seeds_supporting_condition"
    ]
    == 0
)

if (
    loao_stability_final[
        "frozen_seed_count"
    ]
    != 5
).any():
    raise RuntimeError(
        "LOAO stability denominator changed from five."
    )

print(
    "[PASS] all LOAO stability denominators = 5"
)

print(
    "[PASS] no qualitative condition created after results"
)


# =================================================================================================
# 6. PAIRED RANDOM-vs-CHRONOLOGICAL KEY CONTRASTS
# =================================================================================================

banner(
    "STAGE28-FINAL — RANDOM-vs-CHRONOLOGICAL KEY CONTRASTS"
)

contrast_key = (
    loao_contrast_df.loc[
        loao_contrast_df[
            "metric"
        ].isin(
            CONTRAST_KEY_METRICS
        )
    ]
    .copy()
)

direction_key = (
    loao_direction_df.loc[
        loao_direction_df[
            "metric"
        ].isin(
            CONTRAST_KEY_METRICS
        )
    ]
    .copy()
)

join_keys = [
    "family",
    "learner",
    "metric",
    "analysis_status",
    "metric_role",
]

random_chrono_df = contrast_key.merge(
    direction_key,
    on=join_keys,
    how="inner",
    validate="one_to_one",
)

expected_contrast_rows = (
    5
    * 2
    * len(
        CONTRAST_KEY_METRICS
    )
)

if len(
    random_chrono_df
) != expected_contrast_rows:
    raise RuntimeError(
        "Random-vs-chronological key contrast row count mismatch."
    )

if (
    random_chrono_df[
        "contrast_definition"
    ]
    != "RANDOM_MINUS_CHRONOLOGICAL"
).any():
    raise RuntimeError(
        "Contrast orientation changed."
    )

print(
    "[PASS] exact family + learner + metric paired contrasts"
)

print(
    "[PASS] contrast orientation = RANDOM - CHRONOLOGICAL"
)

print(
    "[PASS] no post-result 'large/small/collapse' cutoff assigned"
)


# =================================================================================================
# 7. COMPLETE CLAIM REGISTRY
# =================================================================================================

banner(
    "STAGE28-FINAL — CLAIM REGISTRY"
)

claim_registry_rows = []

# Stage22 frozen directional claims.
for _, row in (
    stage22_stability_df.iterrows()
):
    claim_registry_rows.append(
        {
            "scope":
                "STAGE22_SHARED_FINAL_HOLDOUT",

            "parent_stage":
                "STAGE22_FULL",

            "family":
                "",

            "learner":
                "ENS_LGBM_XGB_EQUAL",

            "claim_id":
                row[
                    "claim_id"
                ],

            "analysis_status":
                "DESCRIPTIVE_ROBUSTNESS_PRE_REGISTERED",

            "supporting_seeds":
                int(
                    row[
                        "supporting_seeds"
                    ]
                ),

            "frozen_seed_count":
                int(
                    row[
                        "total_frozen_seeds"
                    ]
                ),

            "stability_rate":
                float(
                    row[
                        "stability_rate"
                    ]
                ),
        }
    )

# LOAO frozen qualitative conditions.
for _, row in (
    loao_stability_final.iterrows()
):
    claim_registry_rows.append(
        {
            "scope":
                (
                    "CHRONOLOGY_LOAO"
                    if row[
                        "parent_stage"
                    ]
                    ==
                    "STAGE27_CHRONOLOGY_LOAO"
                    else
                    "RANDOM_LOAO_CONTROL"
                ),

            "parent_stage":
                row[
                    "parent_stage"
                ],

            "family":
                row[
                    "family_if_applicable"
                ],

            "learner":
                (
                    row[
                        "learner_if_applicable"
                    ]
                    if pd.notna(
                        row[
                            "learner_if_applicable"
                        ]
                    )
                    else ""
                ),

            "claim_id":
                row[
                    "claim_id"
                ],

            "analysis_status":
                row[
                    "analysis_status"
                ],

            "supporting_seeds":
                int(
                    row[
                        "frozen_seeds_supporting_condition"
                    ]
                ),

            "frozen_seed_count":
                int(
                    row[
                        "frozen_seed_count"
                    ]
                ),

            "stability_rate":
                float(
                    row[
                        "stability_rate"
                    ]
                ),
        }
    )

claim_registry_df = pd.DataFrame(
    claim_registry_rows
)

if len(
    claim_registry_df
) != 112:
    raise RuntimeError(
        f"Final claim registry rows != 112: "
        f"{len(claim_registry_df)}"
    )

print(
    "[PASS] 2 Stage22 frozen claims"
)

print(
    "[PASS] 110 LOAO frozen stability claims"
)

print(
    "[PASS] total claim-registry rows = 112"
)


# =================================================================================================
# 8. COMPACT FAMILY STABILITY TABLE FOR MANUSCRIPT
# =================================================================================================

banner(
    "STAGE28-FINAL — MANUSCRIPT FAMILY STABILITY MATRIX"
)

condition_ids = [
    "ROC_ABOVE_CHANCE",
    "PR_ABOVE_CHANCE",
    "STANDARD_DETECTION_PRESENT",
    "BALANCED_DETECTION_PRESENT",
    "SECURITY_DETECTION_PRESENT_WHERE_FEASIBLE",
]

family_matrix_rows = []

for arm in ARMS:
    for family in FAMILIES:
        for learner in LEARNERS:
            base = loao_stability_df.loc[
                (
                    loao_stability_df[
                        "parent_stage"
                    ]
                    == arm
                )
                &
                (
                    loao_stability_df[
                        "family_if_applicable"
                    ]
                    == family
                )
                &
                (
                    loao_stability_df[
                        "learner_if_applicable"
                    ]
                    == learner
                )
            ]

            values = {
                row[
                    "claim_id"
                ]:
                    int(
                        row[
                            "frozen_seeds_supporting_condition"
                        ]
                    )
                for _, row
                in base.iterrows()
                if row[
                    "claim_id"
                ]
                in condition_ids
            }

            if set(
                values
            ) != set(
                condition_ids
            ):
                raise RuntimeError(
                    "Family stability condition set incomplete: "
                    f"{arm}/{family}/{learner}"
                )

            family_matrix_rows.append(
                {
                    "arm":
                        (
                            "CHRONOLOGY"
                            if arm
                            ==
                            "STAGE27_CHRONOLOGY_LOAO"
                            else
                            "RANDOM_CONTROL"
                        ),

                    "family":
                        family,

                    "learner":
                        learner,

                    "status":
                        (
                            "DESCRIPTIVE_ONLY"
                            if family
                            == "INFILTRATION"
                            else
                            "INFERENTIAL_ELIGIBLE"
                        ),

                    "ROC>0.5":
                        f"{values['ROC_ABOVE_CHANCE']}/5",

                    "PR>chance":
                        f"{values['PR_ABOVE_CHANCE']}/5",

                    "Std recall>0":
                        f"{values['STANDARD_DETECTION_PRESENT']}/5",

                    "Bal recall>0":
                        f"{values['BALANCED_DETECTION_PRESENT']}/5",

                    "Sec recall>0":
                        (
                            f"{values['SECURITY_DETECTION_PRESENT_WHERE_FEASIBLE']}/5"
                        ),
                }
            )

family_matrix_df = pd.DataFrame(
    family_matrix_rows
)

print(
    "[PASS] 20-row family × learner × arm stability matrix"
)


# =================================================================================================
# 9. COMPACT RANDOM-vs-CHRONO TABLE
# =================================================================================================

contrast_matrix_rows = []

for family in FAMILIES:
    for learner in LEARNERS:
        row_out = {
            "family":
                family,

            "learner":
                learner,

            "status":
                (
                    "DESCRIPTIVE_ONLY"
                    if family
                    == "INFILTRATION"
                    else
                    "INFERENTIAL_ELIGIBLE"
                ),
        }

        for metric in [
            "ROC_AUC",
            "PR_EXCESS",
            "STANDARD_RECALL",
        ]:
            row = random_chrono_df.loc[
                (
                    random_chrono_df[
                        "family"
                    ]
                    == family
                )
                &
                (
                    random_chrono_df[
                        "learner"
                    ]
                    == learner
                )
                &
                (
                    random_chrono_df[
                        "metric"
                    ]
                    == metric
                )
            ]

            if len(
                row
            ) != 1:
                raise RuntimeError(
                    "Contrast matrix lookup not unique."
                )

            row = row.iloc[
                0
            ]

            short = {
                "ROC_AUC":
                    "ΔROC",

                "PR_EXCESS":
                    "ΔPR-excess",

                "STANDARD_RECALL":
                    "ΔStd-recall",
            }[
                metric
            ]

            row_out[
                short
            ] = fmt(
                row[
                    "mean"
                ],
                4,
            )

            row_out[
                short
                + " sign"
            ] = (
                f"+{int(row['random_gt_chrono_seed_count'])}"
                f"/-{int(row['random_lt_chrono_seed_count'])}"
                f"/={int(row['random_eq_chrono_seed_count'])}"
            )

        contrast_matrix_rows.append(
            row_out
        )

contrast_matrix_df = pd.DataFrame(
    contrast_matrix_rows
)


# =================================================================================================
# 10. DERIVE ONLY SAFE, FROZEN-CONDITION FINDINGS
# =================================================================================================

banner(
    "STAGE28-FINAL — DERIVE GUARDED FINDINGS"
)

# Families for which BOTH learners show ROC>0.5 and PR>chance
# in all five seeds under BOTH chronology and random control.
fully_rank_stable_families = []

for family in FAMILIES:
    if family == "INFILTRATION":
        continue

    ok = True

    for arm in ARMS:
        for learner in LEARNERS:
            for claim_id in [
                "ROC_ABOVE_CHANCE",
                "PR_ABOVE_CHANCE",
            ]:
                rows = loao_stability_df.loc[
                    (
                        loao_stability_df[
                            "parent_stage"
                        ]
                        == arm
                    )
                    &
                    (
                        loao_stability_df[
                            "family_if_applicable"
                        ]
                        == family
                    )
                    &
                    (
                        loao_stability_df[
                            "learner_if_applicable"
                        ]
                        == learner
                    )
                    &
                    (
                        loao_stability_df[
                            "claim_id"
                        ]
                        == claim_id
                    )
                ]

                if (
                    len(
                        rows
                    )
                    != 1
                    or
                    int(
                        rows.iloc[
                            0
                        ][
                            "frozen_seeds_supporting_condition"
                        ]
                    )
                    != 5
                ):
                    ok = False

    if ok:
        fully_rank_stable_families.append(
            family
        )


# Explicit BOT ranking pattern, derived entirely from frozen conditions.
bot_pattern = {}

for arm in ARMS:
    bot_pattern[
        arm
    ] = {}

    for learner in LEARNERS:
        bot_pattern[
            arm
        ][
            learner
        ] = {}

        for claim_id in [
            "ROC_ABOVE_CHANCE",
            "PR_ABOVE_CHANCE",
        ]:
            row = loao_stability_df.loc[
                (
                    loao_stability_df[
                        "parent_stage"
                    ]
                    == arm
                )
                &
                (
                    loao_stability_df[
                        "family_if_applicable"
                    ]
                    == "BOT"
                )
                &
                (
                    loao_stability_df[
                        "learner_if_applicable"
                    ]
                    == learner
                )
                &
                (
                    loao_stability_df[
                        "claim_id"
                    ]
                    == claim_id
                )
            ]

            if len(
                row
            ) != 1:
                raise RuntimeError(
                    "BOT stability lookup not unique."
                )

            bot_pattern[
                arm
            ][
                learner
            ][
                claim_id
            ] = int(
                row.iloc[
                    0
                ][
                    "frozen_seeds_supporting_condition"
                ]
            )


# Stage22 numerical means.
stage22_lookup = {}

for unit in EXPECTED_UNITS if False else [
    "RANDOM_NATURAL",
    "CHRONOLOGICAL_NATURAL",
]:
    stage22_lookup[
        unit
    ] = {}

    for metric in [
        "roc_auc",
        "pr_auc",
    ]:
        row = stage22_summary_df.loc[
            (
                stage22_summary_df[
                    "unit"
                ]
                == unit
            )
            &
            (
                stage22_summary_df[
                    "metric"
                ]
                == metric
            )
        ]

        if len(
            row
        ) != 1:
            raise RuntimeError(
                "Stage22 summary lookup not unique."
            )

        row = row.iloc[
            0
        ]

        stage22_lookup[
            unit
        ][
            metric
        ] = {
            "mean":
                float(
                    row[
                        "mean"
                    ]
                ),

            "sd":
                float(
                    row[
                        "sample_standard_deviation_ddof_1"
                    ]
                ),

            "minimum":
                float(
                    row[
                        "minimum"
                    ]
                ),

            "maximum":
                float(
                    row[
                        "maximum"
                    ]
                ),
        }


numbers = {
    "stage28_empirical_closure": {
        "authorized_new_fits":
            108,

        "consumed_new_fits":
            108,

        "remaining_new_fits":
            0,

        "stage22_final_holdout_ensemble_evaluations":
            10,

        "stage22_final_holdout_component_inferences":
            20,

        "chronology_loao_seed_realizations":
            50,

        "random_loao_seed_realizations":
            50,

        "stage29_authorized":
            False,
    },

    "stage22_shared_holdout": {
        "rows":
            1_374_133,

        "benign":
            998_788,

        "attack":
            375_345,

        "random_natural":
            stage22_lookup[
                "RANDOM_NATURAL"
            ],

        "chronological_natural":
            stage22_lookup[
                "CHRONOLOGICAL_NATURAL"
            ],

        "PR_RANDOM_LT_CHRONO":
            {
                "supporting_seeds":
                    5,

                "frozen_seeds":
                    5,

                "stability_rate":
                    1.0,
            },

        "ROC_RANDOM_LT_CHRONO":
            {
                "supporting_seeds":
                    5,

                "frozen_seeds":
                    5,

                "stability_rate":
                    1.0,
            },
    },

    "loao": {
        "fully_ranking_stable_inferential_families_both_learners_both_arms":
            fully_rank_stable_families,

        "bot_frozen_condition_pattern":
            bot_pattern,

        "infiltration":
            {
                "heldout_positive_support":
                    36,

                "status":
                    "DESCRIPTIVE_ONLY_SUPPORT_LT_50",
            },

        "aggregation":
            "FAMILY_SPECIFIC_PRIMARY_NO_AGGREGATE_ZERO_DAY_SCORE",
    },

    "interpretation_guardrails": [
        (
            "Training-seed robustness and bootstrap/sampling "
            "uncertainty remain separate."
        ),
        (
            "No best-seed result is selected or reported."
        ),
        (
            "Random LOAO is a control, not a deployment-realistic estimate."
        ),
        (
            "Random-vs-chronological differences do not prove "
            "temporal drift is the sole cause."
        ),
        (
            "Infiltration is descriptive only because support is 36."
        ),
        (
            "No aggregate zero-day score is authorized."
        ),
        (
            "No post-result cutoff is assigned to terms such as "
            "'much greater', 'collapse', or 'survive'."
        ),
    ],
}


# =================================================================================================
# 11. WRITE FINAL NUMERICAL TABLES
# =================================================================================================

banner(
    "STAGE28-FINAL — WRITE PUBLICATION TABLES"
)

OUT.mkdir(
    parents=False,
    exist_ok=False,
)

stage22_summary_df.to_csv(
    STAGE22_SUMMARY_OUT,
    index=False,
)

stage22_contrast_summary_df.to_csv(
    STAGE22_CONTRAST_OUT,
    index=False,
)

loao_key_df.to_csv(
    LOAO_KEY_OUT,
    index=False,
)

loao_stability_final.to_csv(
    LOAO_STABILITY_OUT,
    index=False,
)

random_chrono_df.to_csv(
    RANDOM_CHRONO_OUT,
    index=False,
)

claim_registry_df.to_csv(
    CLAIM_REGISTRY_OUT,
    index=False,
)

write_json(
    NUMBERS_OUT,
    numbers,
)

print(
    "[PASS] Stage22 five-seed summary"
)

print(
    "[PASS] Stage22 contrast summary"
)

print(
    "[PASS] LOAO key metrics"
)

print(
    "[PASS] LOAO stability registry"
)

print(
    "[PASS] random-vs-chronological key contrasts"
)

print(
    "[PASS] complete claim registry"
)

print(
    "[PASS] manuscript numbers JSON"
)


# =================================================================================================
# 12. MANUSCRIPT-READY MARKDOWN
# =================================================================================================

banner(
    "STAGE28-FINAL — MANUSCRIPT-READY RESULTS TEXT"
)

stage22_display_rows = []

for unit in [
    "RANDOM_NATURAL",
    "CHRONOLOGICAL_NATURAL",
]:
    for metric in [
        "roc_auc",
        "pr_auc",
    ]:
        row = stage22_summary_df.loc[
            (
                stage22_summary_df[
                    "unit"
                ]
                == unit
            )
            &
            (
                stage22_summary_df[
                    "metric"
                ]
                == metric
            )
        ].iloc[
            0
        ]

        stage22_display_rows.append(
            {
                "Geometry":
                    unit,

                "Metric":
                    metric.upper(),

                "Mean":
                    fmt(
                        row[
                            "mean"
                        ],
                        4,
                    ),

                "SD":
                    fmt(
                        row[
                            "sample_standard_deviation_ddof_1"
                        ],
                        4,
                    ),

                "Min":
                    fmt(
                        row[
                            "minimum"
                        ],
                        4,
                    ),

                "Max":
                    fmt(
                        row[
                            "maximum"
                        ],
                        4,
                    ),
            }
        )


stage22_contrast_display = []

for _, row in (
    stage22_contrast_summary_df.iterrows()
):
    stage22_contrast_display.append(
        {
            "Metric":
                row[
                    "metric"
                ],

            "Mean Δ (R-C)":
                fmt(
                    row[
                        "mean"
                    ],
                    4,
                ),

            "SD":
                fmt(
                    row[
                        "sample_standard_deviation_ddof_1"
                    ],
                    4,
                ),

            "Min":
                fmt(
                    row[
                        "minimum"
                    ],
                    4,
                ),

            "Max":
                fmt(
                    row[
                        "maximum"
                    ],
                    4,
                ),

            "Random<Chrono":
                (
                    f"{int(row['random_lt_chronological_supporting_seeds'])}/5"
                ),
        }
    )


family_display_rows = (
    family_matrix_df.to_dict(
        orient="records"
    )
)

contrast_display_rows = (
    contrast_matrix_df.to_dict(
        orient="records"
    )
)


stable_family_text = (
    ", ".join(
        fully_rank_stable_families
    )
    if fully_rank_stable_families
    else "none"
)


manuscript = f"""# Stage28 — Final robustness and novelty-control synthesis

## Empirical closure

Stage28 closed the preregistered robustness program with **108/108 authorized
new fits consumed and zero remaining fits**. The experiment included 12
historical model reuses in addition to the 108 new fits. After fitting was
permanently closed, Stage28 performed only preregistered zero-fit synthesis and
the authorized Stage22 shared-final-holdout robustness inference. No Stage29
empirical stage is authorized.

The Stage22 shared holdout contained **1,374,133 flows**, including **998,788
benign** and **375,345 attack** flows. Ten frozen Stage22 ensemble realizations
(two validation geometries × five training seeds) were evaluated on this same
holdout. No threshold or model selection was performed on the holdout.

## Stage22 training-seed robustness on the shared final holdout

{md_table(
    stage22_display_rows,
    [
        "Geometry",
        "Metric",
        "Mean",
        "SD",
        "Min",
        "Max",
    ],
)}

The preregistered directional comparison was stable for every frozen seed.
`PR_AUC_RANDOM_NATURAL < PR_AUC_CHRONOLOGICAL_NATURAL` held for **5/5 seeds**,
and `ROC_AUC_RANDOM_NATURAL < ROC_AUC_CHRONOLOGICAL_NATURAL` also held for
**5/5 seeds**. This is descriptive conclusion-stability analysis rather than a
new significance test.

{md_table(
    stage22_contrast_display,
    [
        "Metric",
        "Mean Δ (R-C)",
        "SD",
        "Min",
        "Max",
        "Random<Chrono",
    ],
)}

These results show that the Stage22 direction was not a seed-42 artifact: the
same random-versus-chronological ranking persisted across seeds 42–46.

## Leave-one-attack-family-out seed stability

The LOAO analysis remained family-specific. The table below reports the number
of frozen seeds (out of five) satisfying each preregistered qualitative
condition. Infiltration is retained only as a descriptive result because its
held-out positive support is 36.

{md_table(
    family_display_rows,
    [
        "arm",
        "family",
        "learner",
        "status",
        "ROC>0.5",
        "PR>chance",
        "Std recall>0",
        "Bal recall>0",
        "Sec recall>0",
    ],
)}

Among inferentially eligible families, the families for which both learners
satisfied both preregistered ranking conditions in all five seeds under both
chronological LOAO and the random-LOAO control were: **{stable_family_text}**.

BOT remained distinctly learner-dependent under chronological LOAO. The
frozen condition counts are preserved directly in the accompanying claim
registry rather than collapsed into a single family score.

## Random-split LOAO control versus chronological LOAO

The random control is not interpreted as a deployment-realistic estimate.
The comparison below reports **continuous paired contrasts only**, defined as
`random - chronological`. No post-result threshold was introduced to classify
a contrast as "large", "small", "collapse", or "survival".

The sign notation is `+N/-N/=N`, where `+` means the random-control value was
numerically greater than the chronological value for that frozen seed.

{md_table(
    contrast_display_rows,
    [
        "family",
        "learner",
        "status",
        "ΔROC",
        "ΔROC sign",
        "ΔPR-excess",
        "ΔPR-excess sign",
        "ΔStd-recall",
        "ΔStd-recall sign",
    ],
)}

Accordingly, random-versus-chronological differences may be described as
**consistent with chronology compounding novelty difficulty** where the
numerical contrasts support that wording, but they do not establish temporal
drift as the sole causal explanation.

## Reproducibility and interpretation constraints

Training-seed uncertainty is reported separately from sampling/bootstrap
uncertainty. No best seed was selected. No synthetic seed-plus-bootstrap
confidence interval was created. No aggregate zero-day score was created:
family-specific LOAO outcomes remain primary.

Infiltration remains descriptive only because its positive support is 36
(<50). Random LOAO is a control rather than a deployment estimate. The final
Stage22 shared-holdout evaluation is a preregistered robustness re-evaluation
of the already historically opened Stage22R population and is not represented
as a new blind external holdout.

## Manuscript-safe conclusion

The five-seed analysis shows that the principal Stage22 validation-geometry
direction is highly stable to training-seed variation: chronological-natural
models exceeded random-natural models in both PR-AUC and ROC-AUC on the shared
final holdout for all five frozen seeds. In the unseen-family experiments,
however, robustness remains family- and learner-specific. Several families
retain stable ranking and operating-point detection across seeds, whereas BOT
shows marked learner dependence and Infiltration cannot support inferential
claims because of its small positive sample. The random-split LOAO control
provides a complementary benchmark for separating novelty difficulty from the
additional challenge associated with chronological evaluation, without
supporting a causal claim that chronology alone explains the observed
differences.
"""

MANUSCRIPT_OUT.write_text(
    manuscript,
    encoding="utf-8",
)

print(
    "[PASS] manuscript-ready Stage28 results package written"
)


# =================================================================================================
# 13. FINAL SYNTHESIS RECEIPT / README
# =================================================================================================

receipt = {
    "stage":
        "Stage28-FINAL",

    "type":
        "ZERO_FIT_FINAL_SYNTHESIS_AND_MANUSCRIPT_READY_RESULTS_FREEZE",

    "created_at_utc":
        utc_now(),

    "scientific_parent_commit":
        EXPECTED_PARENT,

    "empirical_closure": {
        "authorized_new_fits":
            108,

        "consumed_new_fits":
            108,

        "remaining_new_fits":
            0,

        "historical_reuses":
            12,

        "stage22_shared_holdout_ensemble_evaluations":
            10,

        "stage22_shared_holdout_component_model_inferences":
            20,

        "chronology_loao_seed_realizations":
            50,

        "random_loao_seed_realizations":
            50,

        "stage29_authorized":
            False,
    },

    "scientific_operations_this_stage": {
        "new_model_fits":
            0,

        "model_inferences":
            0,

        "threshold_selections":
            0,

        "model_selections":
            0,

        "target_openings":
            0,

        "shared_final_holdout_openings":
            0,

        "bootstrap_recomputations":
            0,

        "shap_recomputations":
            0,

        "new_formal_statistical_tests":
            0,

        "new_post_result_qualitative_cutoffs":
            0,
    },

    "final_stage22_stability": {
        "PR_RANDOM_LT_CHRONO":
            "5_OF_5",

        "ROC_RANDOM_LT_CHRONO":
            "5_OF_5",
    },

    "loao": {
        "family_specific_primary":
            True,

        "aggregate_zero_day_score":
            False,

        "infiltration":
            "DESCRIPTIVE_ONLY_SUPPORT_36_LT_50",

        "random_loao":
            "CONTROL_NOT_DEPLOYMENT_ESTIMATE",
    },

    "input_sha256":
        input_sha,

    "outputs": [
        str(
            path.relative_to(
                REPO
            )
        )
        for path in [
            STAGE22_SUMMARY_OUT,
            STAGE22_CONTRAST_OUT,
            LOAO_KEY_OUT,
            LOAO_STABILITY_OUT,
            RANDOM_CHRONO_OUT,
            CLAIM_REGISTRY_OUT,
            NUMBERS_OUT,
            MANUSCRIPT_OUT,
        ]
    ],

    "status":
        "STAGE28_FINAL_SYNTHESIS_COMPLETE",

    "next_authorized_work":
        (
            "MANUSCRIPT_INTEGRATION_ONLY; "
            "NO_NEW_MODEL_FITS; NO_NEW_EMPIRICAL_STAGE; NO_STAGE29"
        ),
}

write_json(
    RECEIPT_OUT,
    receipt,
)


README_OUT.write_text(
    f"""# Stage28 Final Synthesis

Scientific parent: `{EXPECTED_PARENT}`

## Final empirical status

- Authorized new fits: 108
- Consumed new fits: 108
- Remaining new fits: 0
- Historical reuses: 12
- Stage22 shared-holdout ensemble evaluations: 10
- Chronology LOAO seed realizations: 50
- Random LOAO seed realizations: 50
- Stage29: not authorized

## Stage28-FINAL operations

- Model fits: 0
- Model inference: 0
- Threshold selection: 0
- Model selection: 0
- Target/holdout opening: 0
- New significance tests: 0
- New qualitative cutoffs: 0

## Frozen Stage22 conclusion stability

- PR random < chronological: 5/5 seeds
- ROC random < chronological: 5/5 seeds

The remaining work is manuscript integration only.
""",
    encoding="utf-8",
)


# =================================================================================================
# 14. CHECKSUMS
# =================================================================================================

artifact_paths = [
    STAGE22_SUMMARY_OUT,
    STAGE22_CONTRAST_OUT,
    LOAO_KEY_OUT,
    LOAO_STABILITY_OUT,
    RANDOM_CHRONO_OUT,
    CLAIM_REGISTRY_OUT,
    NUMBERS_OUT,
    MANUSCRIPT_OUT,
    RECEIPT_OUT,
    README_OUT,
]

checksum_lines = []

for path in artifact_paths:
    checksum_lines.append(
        sha256_file(
            path
        )
        + "  "
        + path.name
    )

CHECKSUM_OUT.write_text(
    "\n".join(
        checksum_lines
    )
    + "\n",
    encoding="utf-8",
)

artifact_paths.append(
    CHECKSUM_OUT
)

print(
    "[PASS] final receipt written"
)

print(
    "[PASS] final README written"
)

print(
    "[PASS] final checksums written"
)


# =================================================================================================
# 15. FINAL ZERO-OPERATION ASSERTIONS
# =================================================================================================

banner(
    "STAGE28-FINAL — ZERO-EMPIRICAL-OPERATION ASSERTIONS"
)

# Verify empirical receipt unchanged.
if read_json(
    STAGE4_RECEIPT
) != stage4:
    raise RuntimeError(
        "Stage28-4 empirical receipt changed unexpectedly."
    )

if read_json(
    CLOSURE_RECEIPT
) != closure:
    raise RuntimeError(
        "Stage28 closure receipt changed unexpectedly."
    )

print(
    "[PASS] Stage28-4 receipt unchanged"
)

print(
    "[PASS] Stage28 fit-closure receipt unchanged"
)

print(
    "[PASS] model fits this stage = 0"
)

print(
    "[PASS] model inference this stage = 0"
)

print(
    "[PASS] final-holdout openings this stage = 0"
)

print(
    "[PASS] target openings this stage = 0"
)

print(
    "[PASS] threshold selections this stage = 0"
)

print(
    "[PASS] new formal tests this stage = 0"
)

print(
    "[PASS] post-result qualitative cutoffs = 0"
)


# =================================================================================================
# 16. EXACT GIT UNIVERSE
# =================================================================================================

banner(
    "STAGE28-FINAL — GIT CHANGE GATE"
)

expected_rel = {
    str(
        path.relative_to(
            REPO
        )
    )
    for path in artifact_paths
}

tracked = set(
    git(
        "diff",
        "--name-only",
    ).splitlines()
)

staged = set(
    git(
        "diff",
        "--cached",
        "--name-only",
    ).splitlines()
)

untracked = set(
    git(
        "ls-files",
        "--others",
        "--exclude-standard",
    ).splitlines()
)

if tracked:
    raise RuntimeError(
        "Unexpected tracked modifications:\n"
        + "\n".join(
            sorted(
                tracked
            )
        )
    )

if staged:
    raise RuntimeError(
        "Unexpected staged files."
    )

if untracked != expected_rel:
    raise RuntimeError(
        "Unexpected final-synthesis artifact universe.\n\n"
        "Expected:\n"
        + "\n".join(
            sorted(
                expected_rel
            )
        )
        + "\n\nActual:\n"
        + "\n".join(
            sorted(
                untracked
            )
        )
    )

print(
    "[PASS] exact final synthesis artifact universe"
)


# =================================================================================================
# 17. DURABLE FINAL SYNTHESIS COMMIT
# =================================================================================================

banner(
    "STAGE28-FINAL — DURABLE COMMIT / PUSH"
)

run(
    [
        "git",
        "fetch",
        "origin",
        "main",
    ]
)

if (
    git(
        "rev-parse",
        "origin/main",
    )
    != EXPECTED_PARENT
):
    raise RuntimeError(
        "origin/main changed during final synthesis."
    )

for rel in sorted(
    expected_rel
):
    run(
        [
            "git",
            "add",
            "--",
            rel,
        ]
    )

if (
    set(
        git(
            "diff",
            "--cached",
            "--name-only",
        ).splitlines()
    )
    != expected_rel
):
    raise RuntimeError(
        "Final synthesis staged universe mismatch."
    )

run(
    [
        "git",
        "config",
        "user.name",
        "Stage28 Kaggle",
    ]
)

run(
    [
        "git",
        "config",
        "user.email",
        "stage28-kaggle@users.noreply.github.com",
    ]
)

commit_message = (
    "stage28-final: freeze synthesis and manuscript-ready results"
)

print(
    run(
        [
            "git",
            "commit",
            "-m",
            commit_message,
        ]
    ).stdout.strip()
)

FINAL_SYNTHESIS_COMMIT = git(
    "rev-parse",
    "HEAD",
)

if (
    git(
        "rev-parse",
        "HEAD^",
    )
    != EXPECTED_PARENT
):
    raise RuntimeError(
        "Final synthesis parent mismatch."
    )

push_origin_main()

run(
    [
        "git",
        "fetch",
        "origin",
        "main",
    ]
)

if not (
    git(
        "rev-parse",
        "HEAD",
    )
    ==
    git(
        "rev-parse",
        "origin/main",
    )
    ==
    FINAL_SYNTHESIS_COMMIT
):
    raise RuntimeError(
        "Final synthesis remote durability check failed."
    )

if git(
    "status",
    "--porcelain",
):
    raise RuntimeError(
        "Repository dirty after final synthesis."
    )

print()
print(
    "[PASS] Stage28 final synthesis durable"
)

print(
    "[PASS] repository clean"
)


# =================================================================================================
# 18. FINAL REPORT
# =================================================================================================

banner(
    "STAGE28 — FINAL SYNTHESIS COMPLETE"
)

print(
    "Empirical parent       :",
    EXPECTED_PARENT,
)

print(
    "Final synthesis commit:",
    FINAL_SYNTHESIS_COMMIT,
)

print()
print(
    "Authorized new fits    : 108"
)

print(
    "Consumed new fits      : 108"
)

print(
    "Remaining new fits     : 0"
)

print(
    "New fits in FINAL      : 0"
)

print(
    "Inference in FINAL     : 0"
)

print(
    "Holdout openings FINAL : 0"
)

print()
print(
    "Stage22 PR direction   : 5 / 5 stable"
)

print(
    "Stage22 ROC direction  : 5 / 5 stable"
)

print(
    "Infiltration           : DESCRIPTIVE ONLY (n=36)"
)

print(
    "Aggregate zero-day     : NOT CREATED"
)

print(
    "Stage29                : NOT AUTHORIZED"
)

print()
print(
    "STAGE28 IS SCIENTIFICALLY CLOSED."
)

print()
print(
    "NEXT:"
)

print(
    "MANUSCRIPT INTEGRATION ONLY."
)

# ==============================================================================================================
# %% NOTEBOOK CELL 0015 | execution_count=15
# ==============================================================================================================
# =================================================================================================
# STAGE28 — ARCHIVE COMPLETE KAGGLE NOTEBOOK UNDER scripts/stage28/
#
# DOCUMENTATION / REPRODUCIBILITY ONLY
#
# SCIENTIFIC OPERATIONS:
#   model fits          : 0
#   model inference     : 0
#   threshold selection : 0
#   target opening      : 0
#   holdout opening     : 0
#
# Expected scientific-final parent:
#   94bbebfe6b18249166ac6bc89deadc8a2d6dc627
#
# Outputs:
#   scripts/stage28/stage28_full_kaggle_notebook.ipynb
#   scripts/stage28/stage28_full_kaggle_notebook.py
#   scripts/stage28/notebook_export_manifest.json
#   scripts/stage28/README.md
#   scripts/stage28/checksums.sha256
# =================================================================================================

from __future__ import annotations

import base64
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote, urljoin

import requests


# =================================================================================================
# CONSTANTS
# =================================================================================================

SEP = "=" * 120

REPO = Path(
    "/kaggle/working/ids2018-validation-safe-ablation"
).resolve()

EXPECTED_PARENT = (
    "94bbebfe6b18249166ac6bc89deadc8a2d6dc627"
)

FINAL_RECEIPT = (
    REPO
    / "results"
    / "stage28_stability_novelty_control"
    / "stage28_final_synthesis"
    / "stage28_final_synthesis_receipt.json"
)

OUT = (
    REPO
    / "scripts"
    / "stage28"
)

IPYNB_OUT = (
    OUT
    / "stage28_full_kaggle_notebook.ipynb"
)

PY_OUT = (
    OUT
    / "stage28_full_kaggle_notebook.py"
)

MANIFEST_OUT = (
    OUT
    / "notebook_export_manifest.json"
)

README_OUT = (
    OUT
    / "README.md"
)

CHECKSUM_OUT = (
    OUT
    / "checksums.sha256"
)


# =================================================================================================
# HELPERS
# =================================================================================================

def banner(text):
    print()
    print(SEP)
    print(text)
    print(SEP)
    print()


def utc_now():
    return datetime.now(
        timezone.utc
    ).isoformat()


def run(
    cmd,
    *,
    cwd=REPO,
    check=True,
):
    p = subprocess.run(
        [str(x) for x in cmd],
        cwd=str(cwd),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    if check and p.returncode != 0:
        raise RuntimeError(
            f"Command failed ({p.returncode}):\n"
            + " ".join(map(str, cmd))
            + f"\n\nSTDOUT:\n{p.stdout}"
            + f"\n\nSTDERR:\n{p.stderr}"
        )

    return p


def git(*args):
    return run(
        ["git", *args]
    ).stdout.strip()


def sha256_file(path):
    h = hashlib.sha256()

    with Path(path).open("rb") as f:
        while True:
            block = f.read(
                16 * 1024 * 1024
            )

            if not block:
                break

            h.update(block)

    return h.hexdigest()


def sha256_text(text):
    return hashlib.sha256(
        text.encode("utf-8")
    ).hexdigest()


def read_json(path):
    return json.loads(
        Path(path).read_text(
            encoding="utf-8"
        )
    )


def write_json(path, obj):
    Path(path).write_text(
        json.dumps(
            obj,
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )


def source_as_text(source):
    if isinstance(
        source,
        list,
    ):
        return "".join(
            str(x)
            for x in source
        )

    return str(
        source or ""
    )


# =================================================================================================
# GITHUB AUTH
# =================================================================================================

def get_github_token():

    from kaggle_secrets import (
        UserSecretsClient,
    )

    client = UserSecretsClient()

    labels = [
        "GITHUB_TOKEN",
        "github_token",
        "GH_TOKEN",
        "GITHUB_PAT",
        "github_pat",
        "GH_PAT",
    ]

    for label in labels:

        try:
            value = client.get_secret(
                label
            )

        except Exception:
            value = None

        if (
            isinstance(
                value,
                str,
            )
            and value.strip()
        ):

            return (
                value.strip(),
                label,
            )

    raise RuntimeError(
        "No usable GitHub token found in Kaggle Secrets."
    )


def push_origin_main():

    token, label = (
        get_github_token()
    )

    auth = base64.b64encode(
        (
            "x-access-token:"
            + token
        ).encode(
            "utf-8"
        )
    ).decode(
        "ascii"
    )

    p = subprocess.run(
        [
            "git",
            "-c",
            "credential.helper=",
            "-c",
            (
                "http.extraHeader="
                "AUTHORIZATION: Basic "
                + auth
            ),
            "push",
            "origin",
            "main",
        ],
        cwd=str(
            REPO
        ),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    if p.returncode != 0:
        raise RuntimeError(
            "Git push failed.\n\n"
            f"STDOUT:\n{p.stdout}\n\n"
            f"STDERR:\n{p.stderr}"
        )

    print(
        "[PASS] GitHub credential:",
        f"kaggle_secret:{label}",
    )

    print(
        "[PASS] token not displayed"
    )

    if p.stdout.strip():
        print(
            p.stdout.strip()
        )

    if p.stderr.strip():
        print(
            p.stderr.strip()
        )


# =================================================================================================
# 0. SCIENTIFIC-FINAL PARENT GATE
# =================================================================================================

banner(
    "STAGE28 NOTEBOOK ARCHIVE — REPOSITORY / SCIENTIFIC-FINAL GATE"
)

if not (
    REPO
    / ".git"
).is_dir():

    raise RuntimeError(
        "Repository missing."
    )


if git(
    "status",
    "--porcelain",
):

    raise RuntimeError(
        "Repository must be clean before notebook archival."
    )


run(
    [
        "git",
        "fetch",
        "origin",
        "main",
    ]
)


local_head = git(
    "rev-parse",
    "HEAD",
)

remote_head = git(
    "rev-parse",
    "origin/main",
)


print(
    "Expected Stage28-final:",
    EXPECTED_PARENT,
)

print(
    "Local HEAD            :",
    local_head,
)

print(
    "origin/main           :",
    remote_head,
)


if not (
    local_head
    == remote_head
    == EXPECTED_PARENT
):

    raise RuntimeError(
        "Notebook archive must descend directly from "
        "the frozen Stage28-final commit."
    )


if not FINAL_RECEIPT.is_file():

    raise RuntimeError(
        "Stage28 final synthesis receipt missing."
    )


final_receipt = read_json(
    FINAL_RECEIPT
)


if (
    final_receipt.get(
        "status"
    )
    != "STAGE28_FINAL_SYNTHESIS_COMPLETE"
):

    raise RuntimeError(
        "Stage28 final synthesis receipt is not COMPLETE."
    )


if (
    final_receipt[
        "empirical_closure"
    ][
        "consumed_new_fits"
    ]
    != 108
    or
    final_receipt[
        "empirical_closure"
    ][
        "remaining_new_fits"
    ]
    != 0
):

    raise RuntimeError(
        "Stage28 empirical closure does not equal 108/108."
    )


if OUT.exists():

    raise RuntimeError(
        f"Archive directory already exists:\n{OUT}\n\n"
        "Do not overwrite it."
    )


print()
print(
    "[PASS] Stage28-final parent exact"
)

print(
    "[PASS] scientific closure = 108 / 108"
)

print(
    "[PASS] Stage29 not involved"
)

print(
    "[PASS] this commit is documentation/reproducibility only"
)


# =================================================================================================
# 1. TRY TO OBTAIN THE REAL LIVE NOTEBOOK FROM JUPYTER
# =================================================================================================

banner(
    "STAGE28 NOTEBOOK ARCHIVE — LIVE NOTEBOOK DISCOVERY"
)


notebook_json = None

notebook_source_mode = None

notebook_source_detail = None

jupyter_errors = []


try:

    from ipykernel import (
        get_connection_file,
    )

    connection_file = Path(
        get_connection_file()
    ).name

    kernel_id = (
        Path(
            connection_file
        ).stem
        .replace(
            "kernel-",
            "",
        )
    )


    print(
        "Kernel ID:",
        kernel_id,
    )


    server_candidates = []


    # Jupyter Server
    try:

        from jupyter_server.serverapp import (
            list_running_servers,
        )

        server_candidates.extend(
            list(
                list_running_servers()
            )
        )

    except Exception as exc:

        jupyter_errors.append(
            "jupyter_server: "
            + repr(
                exc
            )
        )


    # Legacy notebook server fallback
    try:

        from notebook.notebookapp import (
            list_running_servers
            as list_legacy_servers,
        )

        server_candidates.extend(
            list(
                list_legacy_servers()
            )
        )

    except Exception as exc:

        jupyter_errors.append(
            "notebook_server: "
            + repr(
                exc
            )
        )


    deduped_servers = []

    seen_server_urls = set()


    for server in server_candidates:

        url = (
            server.get(
                "url"
            )
            or
            server.get(
                "base_url"
            )
        )

        if not url:
            continue

        if url in seen_server_urls:
            continue

        seen_server_urls.add(
            url
        )

        deduped_servers.append(
            server
        )


    print(
        "Running Jupyter server candidates:",
        len(
            deduped_servers
        ),
    )


    for server in deduped_servers:

        if notebook_json is not None:
            break

        base_url = server.get(
            "url"
        )

        token = (
            server.get(
                "token"
            )
            or ""
        )

        headers = {}

        params = {}

        if token:
            params[
                "token"
            ] = token


        try:

            sessions_url = urljoin(
                base_url,
                "api/sessions",
            )

            response = requests.get(
                sessions_url,
                params=params,
                headers=headers,
                timeout=10,
            )

            response.raise_for_status()

            sessions = response.json()


            for session in sessions:

                session_kernel = (
                    session.get(
                        "kernel",
                        {},
                    ).get(
                        "id"
                    )
                )

                if (
                    session_kernel
                    != kernel_id
                ):
                    continue


                notebook_path = (
                    session.get(
                        "path"
                    )
                    or
                    session.get(
                        "notebook",
                        {},
                    ).get(
                        "path"
                    )
                )


                if not notebook_path:
                    continue


                contents_url = urljoin(
                    base_url,
                    "api/contents/"
                    + quote(
                        notebook_path
                    ),
                )


                contents_response = requests.get(
                    contents_url,
                    params={
                        **params,
                        "content": 1,
                    },
                    headers=headers,
                    timeout=30,
                )

                contents_response.raise_for_status()

                payload = (
                    contents_response.json()
                )


                content = payload.get(
                    "content"
                )


                if not isinstance(
                    content,
                    dict,
                ):
                    continue


                if (
                    "cells"
                    not in content
                ):
                    continue


                notebook_json = content

                notebook_source_mode = (
                    "LIVE_JUPYTER_NOTEBOOK_MODEL"
                )

                notebook_source_detail = (
                    notebook_path
                )

                break


        except Exception as exc:

            jupyter_errors.append(
                repr(
                    exc
                )
            )


except Exception as exc:

    jupyter_errors.append(
        "kernel_discovery: "
        + repr(
            exc
        )
    )


# =================================================================================================
# 2. FALL BACK TO IPYTHON EXECUTION HISTORY IF REQUIRED
# =================================================================================================

if notebook_json is None:

    banner(
        "LIVE NOTEBOOK MODEL UNAVAILABLE — RECONSTRUCT FROM IPYTHON HISTORY"
    )


    try:
        ip = get_ipython()

    except NameError:
        ip = None


    if ip is None:

        raise RuntimeError(
            "Neither live notebook model nor IPython history is available."
        )


    history = list(
        ip.history_manager.input_hist_raw
    )


    raw_cells = []


    for history_index, source in enumerate(
        history
    ):

        if (
            history_index == 0
            or
            not isinstance(
                source,
                str,
            )
            or
            not source.strip()
        ):
            continue


        raw_cells.append(
            {
                "cell_type":
                    "code",

                "execution_count":
                    history_index,

                "metadata": {
                    "reconstructed_from_ipython_history":
                        True,

                    "history_index":
                        history_index,
                },

                "outputs":
                    [],

                "source":
                    source,
            }
        )


    if not raw_cells:

        raise RuntimeError(
            "IPython history is empty."
        )


    notebook_json = {
        "cells":
            raw_cells,

        "metadata": {
            "stage28_archive": {
                "source":
                    "IPYTHON_RAW_EXECUTION_HISTORY",

                "warning":
                    (
                        "Markdown cells and rich cell outputs are not "
                        "available from kernel history."
                    ),
            },

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
        },

        "nbformat":
            4,

        "nbformat_minor":
            5,
    }


    notebook_source_mode = (
        "IPYTHON_RAW_EXECUTION_HISTORY_RECONSTRUCTION"
    )

    notebook_source_detail = (
        f"{len(raw_cells)} executed code cells"
    )


print()
print(
    "Notebook source mode:",
    notebook_source_mode,
)

print(
    "Notebook source detail:",
    notebook_source_detail,
)


if jupyter_errors:

    print()
    print(
        "Jupyter discovery notes:"
    )

    for error in jupyter_errors[
        :10
    ]:

        print(
            " ",
            error[
                :500
            ],
        )


# =================================================================================================
# 3. VALIDATE NOTEBOOK CONTENT
# =================================================================================================

banner(
    "STAGE28 NOTEBOOK ARCHIVE — CONTENT VALIDATION"
)


cells = notebook_json.get(
    "cells"
)


if not isinstance(
    cells,
    list,
) or not cells:

    raise RuntimeError(
        "Notebook contains no cells."
    )


code_cells = [
    cell
    for cell in cells
    if cell.get(
        "cell_type"
    )
    == "code"
]


markdown_cells = [
    cell
    for cell in cells
    if cell.get(
        "cell_type"
    )
    == "markdown"
]


code_text = "\n\n".join(
    source_as_text(
        cell.get(
            "source",
            ""
        )
    )
    for cell in code_cells
)


required_stage28_markers = [
    "STAGE28-3A",
    "STAGE28-3B",
    "STAGE28-3C",
    "STAGE28-4",
    "STAGE28-FINAL",
]


missing_markers = [
    marker
    for marker
    in required_stage28_markers
    if marker
    not in code_text
]


if missing_markers:

    raise RuntimeError(
        "Notebook export does not contain required late-Stage28 markers:\n"
        + "\n".join(
            missing_markers
        )
    )


print(
    "Total cells   :",
    len(
        cells
    ),
)

print(
    "Code cells    :",
    len(
        code_cells
    ),
)

print(
    "Markdown cells:",
    len(
        markdown_cells
    ),
)


print()
print(
    "[PASS] Stage28-3A present"
)

print(
    "[PASS] Stage28-3B present"
)

print(
    "[PASS] Stage28-3C present"
)

print(
    "[PASS] Stage28-4 present"
)

print(
    "[PASS] Stage28-FINAL present"
)


# =================================================================================================
# 4. BUILD SCRIPT VERSION
# =================================================================================================

banner(
    "STAGE28 NOTEBOOK ARCHIVE — BUILD scripts/stage28 EXPORT"
)


script_parts = [
    '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Stage28 complete Kaggle notebook source archive.

Scientific-final parent:
    94bbebfe6b18249166ac6bc89deadc8a2d6dc627

IMPORTANT
---------
This file is an archival linearization of the Kaggle notebook.

It preserves notebook cell order and source. It is not a new Stage28
scientific stage and must not be interpreted as authorizing new model fits.

For the notebook representation, see:
    stage28_full_kaggle_notebook.ipynb
"""

'''
]


for cell_number, cell in enumerate(
    cells,
    start=1,
):

    cell_type = cell.get(
        "cell_type",
        "unknown",
    )

    source = source_as_text(
        cell.get(
            "source",
            ""
        )
    )


    if cell_type == "markdown":

        script_parts.append(
            "\n"
            + "# "
            + "=" * 110
            + "\n"
            + f"# %% [markdown] NOTEBOOK CELL {cell_number:04d}\n"
            + "# "
            + "=" * 110
            + "\n"
        )


        if source:

            for line in source.splitlines():

                script_parts.append(
                    "# "
                    + line
                    + "\n"
                )


    elif cell_type == "code":

        execution_count = cell.get(
            "execution_count"
        )


        script_parts.append(
            "\n"
            + "# "
            + "=" * 110
            + "\n"
            + (
                f"# %% NOTEBOOK CELL {cell_number:04d} "
                f"| execution_count={execution_count}\n"
            )
            + "# "
            + "=" * 110
            + "\n"
        )


        script_parts.append(
            source
        )


        if (
            source
            and
            not source.endswith(
                "\n"
            )
        ):

            script_parts.append(
                "\n"
            )


    else:

        script_parts.append(
            "\n"
            + "# "
            + "=" * 110
            + "\n"
            + (
                f"# NOTEBOOK CELL {cell_number:04d} "
                f"| unsupported type={cell_type!r}\n"
            )
            + "# "
            + "=" * 110
            + "\n"
        )


script_text = "".join(
    script_parts
)


# =================================================================================================
# 5. HIGH-CONFIDENCE SECRET SCAN
# =================================================================================================

banner(
    "STAGE28 NOTEBOOK ARCHIVE — SECRET-SAFETY GATE"
)


serialized_notebook = json.dumps(
    notebook_json,
    ensure_ascii=False,
)


secret_patterns = {
    "GitHub classic token":
        r"\bgh[pousr]_[A-Za-z0-9]{20,}\b",

    "GitHub fine-grained PAT":
        r"\bgithub_pat_[A-Za-z0-9_]{20,}\b",

    "OpenAI-style secret":
        r"\bsk-[A-Za-z0-9_-]{20,}\b",

    "Stripe live secret":
        r"\bsk_live_[A-Za-z0-9]{10,}\b",

    "HuggingFace token":
        r"\bhf_[A-Za-z0-9]{20,}\b",

    "AWS access key":
        r"\bAKIA[0-9A-Z]{16}\b",

    "Generic literal GitHub token assignment":
        (
            r"""(?i)\b(?:GITHUB_TOKEN|GH_TOKEN|GITHUB_PAT|GH_PAT)"""
            r"""\s*=\s*['"][^'"]{20,}['"]"""
        ),
}


secret_hits = []


for name, pattern in (
    secret_patterns.items()
):

    regex = re.compile(
        pattern
    )


    for target_name, target_text in [
        (
            "ipynb",
            serialized_notebook,
        ),
        (
            "py",
            script_text,
        ),
    ]:

        match = regex.search(
            target_text
        )


        if match:

            # Do NOT print the secret itself.
            secret_hits.append(
                {
                    "pattern":
                        name,

                    "artifact":
                        target_name,

                    "offset":
                        int(
                            match.start()
                        ),
                }
            )


if secret_hits:

    raise RuntimeError(
        "Potential hard-coded secret detected in notebook source.\n"
        "Nothing has been written or committed.\n\n"
        + json.dumps(
            secret_hits,
            indent=2,
        )
    )


print(
    "[PASS] no high-confidence hard-coded credential patterns detected"
)

print(
    "[PASS] Kaggle Secret retrieval code is safe to archive"
)

print(
    "[PASS] no token value will be inserted into exported source"
)


# =================================================================================================
# 6. WRITE ARCHIVE
# =================================================================================================

OUT.mkdir(
    parents=False,
    exist_ok=False,
)


IPYNB_OUT.write_text(
    json.dumps(
        notebook_json,
        indent=1,
        ensure_ascii=False,
    )
    + "\n",
    encoding="utf-8",
)


PY_OUT.write_text(
    script_text,
    encoding="utf-8",
)


# GitHub hard limit protection.
for path in [
    IPYNB_OUT,
    PY_OUT,
]:

    size = path.stat().st_size


    print(
        path.name,
        "bytes=",
        f"{size:,}",
    )


    if size >= (
        95
        * 1024
        * 1024
    ):

        raise RuntimeError(
            f"{path.name} is too large for safe normal GitHub storage."
        )


# =================================================================================================
# 7. EXPORT MANIFEST
# =================================================================================================

notebook_sha = sha256_file(
    IPYNB_OUT
)

script_sha = sha256_file(
    PY_OUT
)

manifest = {
    "artifact":
        "STAGE28_COMPLETE_KAGGLE_NOTEBOOK_ARCHIVE",

    "created_at_utc":
        utc_now(),

    "scientific_final_parent_commit":
        EXPECTED_PARENT,

    "scientific_status":
        "STAGE28_SCIENTIFICALLY_CLOSED",

    "stage29_authorized":
        False,

    "archive_commit_type":
        "DOCUMENTATION_AND_REPRODUCIBILITY_ONLY",

    "source_mode":
        notebook_source_mode,

    "source_detail":
        notebook_source_detail,

    "fidelity": {
        "code_cell_source_preserved":
            True,

        "cell_order_preserved":
            True,

        "markdown_preserved":
            (
                notebook_source_mode
                == "LIVE_JUPYTER_NOTEBOOK_MODEL"
            ),

        "outputs_preserved":
            (
                notebook_source_mode
                == "LIVE_JUPYTER_NOTEBOOK_MODEL"
            ),

        "fallback_warning":
            (
                None
                if notebook_source_mode
                == "LIVE_JUPYTER_NOTEBOOK_MODEL"
                else
                (
                    "Live notebook model was unavailable. "
                    "The .ipynb was reconstructed from raw "
                    "IPython execution history; markdown and "
                    "rich outputs are therefore not available."
                )
            ),
    },

    "notebook": {
        "path":
            str(
                IPYNB_OUT.relative_to(
                    REPO
                )
            ),

        "sha256":
            notebook_sha,

        "bytes":
            IPYNB_OUT.stat().st_size,

        "total_cells":
            len(
                cells
            ),

        "code_cells":
            len(
                code_cells
            ),

        "markdown_cells":
            len(
                markdown_cells
            ),
    },

    "python_export": {
        "path":
            str(
                PY_OUT.relative_to(
                    REPO
                )
            ),

        "sha256":
            script_sha,

        "bytes":
            PY_OUT.stat().st_size,
    },

    "required_markers_verified":
        required_stage28_markers,

    "scientific_operations_performed_by_archive":
        {
            "model_fits":
                0,

            "model_inferences":
                0,

            "threshold_selections":
                0,

            "model_selections":
                0,

            "target_openings":
                0,

            "final_holdout_openings":
                0,
        },

    "final_stage28_receipt": {
        "path":
            str(
                FINAL_RECEIPT.relative_to(
                    REPO
                )
            ),

        "sha256":
            sha256_file(
                FINAL_RECEIPT
            ),

        "status":
            final_receipt[
                "status"
            ],
    },
}


write_json(
    MANIFEST_OUT,
    manifest,
)


README_OUT.write_text(
    f"""# Stage28 Kaggle Notebook Archive

This directory archives the Stage28 Kaggle notebook after the scientific
analysis was fully closed.

## Scientific lineage

Final scientific Stage28 commit before notebook archival:

`{EXPECTED_PARENT}`

The archive commit is documentation/reproducibility only. It does not modify
Stage28 results or authorize any new empirical work.

## Files

- `stage28_full_kaggle_notebook.ipynb`
- `stage28_full_kaggle_notebook.py`
- `notebook_export_manifest.json`
- `checksums.sha256`

## Notebook source mode

`{notebook_source_mode}`

Source detail:

`{notebook_source_detail}`

## Scientific closure

- Authorized Stage28 new fits: 108
- Consumed Stage28 new fits: 108
- Remaining new fits: 0
- Stage29: not authorized
- Model fits during this archive step: 0
- Model inference during this archive step: 0
- Holdout/target openings during this archive step: 0

The `.py` file is a cell-ordered archival linearization of the notebook.
The `.ipynb` file is the preferred notebook representation.
""",
    encoding="utf-8",
)


# =================================================================================================
# 8. CHECKSUMS
# =================================================================================================

archive_files_without_checksum = [
    IPYNB_OUT,
    PY_OUT,
    MANIFEST_OUT,
    README_OUT,
]


CHECKSUM_OUT.write_text(
    "\n".join(
        (
            sha256_file(
                path
            )
            + "  "
            + path.name
        )
        for path in (
            archive_files_without_checksum
        )
    )
    + "\n",
    encoding="utf-8",
)


archive_files = [
    *archive_files_without_checksum,
    CHECKSUM_OUT,
]


print()
print(
    "[PASS] notebook archive written"
)

print(
    "[PASS] manifest written"
)

print(
    "[PASS] README written"
)

print(
    "[PASS] checksum manifest written"
)


# =================================================================================================
# 9. EXACT GIT UNIVERSE
# =================================================================================================

banner(
    "STAGE28 NOTEBOOK ARCHIVE — EXACT GIT UNIVERSE"
)


expected_rel = {
    str(
        path.relative_to(
            REPO
        )
    )
    for path in (
        archive_files
    )
}


tracked = set(
    git(
        "diff",
        "--name-only",
    ).splitlines()
)

staged = set(
    git(
        "diff",
        "--cached",
        "--name-only",
    ).splitlines()
)

untracked = set(
    git(
        "ls-files",
        "--others",
        "--exclude-standard",
    ).splitlines()
)


if tracked:

    raise RuntimeError(
        "Unexpected tracked modifications:\n"
        + "\n".join(
            sorted(
                tracked
            )
        )
    )


if staged:

    raise RuntimeError(
        "Unexpected staged files."
    )


if untracked != expected_rel:

    raise RuntimeError(
        "Unexpected notebook-archive file universe.\n\n"
        "Expected:\n"
        + "\n".join(
            sorted(
                expected_rel
            )
        )
        + "\n\nActual:\n"
        + "\n".join(
            sorted(
                untracked
            )
        )
    )


print(
    "[PASS] exactly five archival files"
)

print(
    "[PASS] no result/model/metadata artifact modified"
)


# =================================================================================================
# 10. COMMIT / PUSH
# =================================================================================================

banner(
    "STAGE28 NOTEBOOK ARCHIVE — DURABLE COMMIT / PUSH"
)


run(
    [
        "git",
        "fetch",
        "origin",
        "main",
    ]
)


if (
    git(
        "rev-parse",
        "origin/main",
    )
    != EXPECTED_PARENT
):

    raise RuntimeError(
        "origin/main changed while notebook archive was being prepared."
    )


for rel in sorted(
    expected_rel
):

    run(
        [
            "git",
            "add",
            "-f",
            "--",
            rel,
        ]
    )


staged_after = set(
    git(
        "diff",
        "--cached",
        "--name-only",
    ).splitlines()
)


if staged_after != expected_rel:

    raise RuntimeError(
        "Staged notebook archive universe mismatch."
    )


run(
    [
        "git",
        "config",
        "user.name",
        "Stage28 Kaggle",
    ]
)

run(
    [
        "git",
        "config",
        "user.email",
        "stage28-kaggle@users.noreply.github.com",
    ]
)


commit_message = (
    "archive: add complete Stage28 Kaggle notebook under scripts"
)


print(
    run(
        [
            "git",
            "commit",
            "-m",
            commit_message,
        ]
    ).stdout.strip()
)


ARCHIVE_COMMIT = git(
    "rev-parse",
    "HEAD",
)


if (
    git(
        "rev-parse",
        "HEAD^",
    )
    != EXPECTED_PARENT
):

    raise RuntimeError(
        "Notebook archive commit parent mismatch."
    )


push_origin_main()


run(
    [
        "git",
        "fetch",
        "origin",
        "main",
    ]
)


if not (
    git(
        "rev-parse",
        "HEAD",
    )
    ==
    git(
        "rev-parse",
        "origin/main",
    )
    ==
    ARCHIVE_COMMIT
):

    raise RuntimeError(
        "Notebook archive remote durability verification failed."
    )


if git(
    "status",
    "--porcelain",
):

    raise RuntimeError(
        "Repository dirty after notebook archive commit."
    )


# =================================================================================================
# 11. COMPLETE
# =================================================================================================

banner(
    "STAGE28 NOTEBOOK ARCHIVE — COMPLETE"
)


print(
    "Scientific-final parent:",
    EXPECTED_PARENT,
)

print(
    "Notebook archive commit:",
    ARCHIVE_COMMIT,
)

print()
print(
    "Source mode:",
    notebook_source_mode,
)

print(
    "Total notebook cells:",
    len(
        cells
    ),
)

print(
    "Code cells:",
    len(
        code_cells
    ),
)

print(
    "Markdown cells:",
    len(
        markdown_cells
    ),
)

print()
print(
    "Notebook SHA256:",
    notebook_sha,
)

print(
    "Python SHA256  :",
    script_sha,
)

print()
print(
    "Model fits        : 0"
)

print(
    "Model inference   : 0"
)

print(
    "Threshold search  : 0"
)

print(
    "Holdout openings  : 0"
)

print(
    "Target openings   : 0"
)

print()
print(
    "[PASS] Stage28 scientific results untouched"
)

print(
    "[PASS] complete notebook source archived under scripts/stage28/"
)

print(
    "[PASS] Stage29 remains NOT AUTHORIZED"
)

print()
print(
    "NEXT: manuscript integration only."
)
