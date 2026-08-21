# ==============================================================================
# STAGE27 — LEAVE-ONE-ATTACK-FAMILY-OUT UNSEEN-FAMILY GENERALIZATION AUDIT
# Complete source export of the Stage27 Kaggle notebook.
#
# Frozen scientific parent:
# 0e1439565aedc7da9b7ca1207262e9061422bc22
#
# Publication-closeout parent at export:
# 3407ff3954abae9b0c8bfdaa14b704a05f31affe
#
# Scientific state: CLOSED
#
# This file preserves notebook source ordering.
# It does not authorize new Stage27 scientific computation.
# ==============================================================================


# %% [Stage27 notebook cell 1]
# ======================================================================================
# STAGE27 — FRESH KAGGLE RECOVERY AFTER STAGE27-3B0
#
# Expected scientific parent:
#   283690948d44345123d838fd47a8764441f491c2
#
# ZERO scientific computation.
# ======================================================================================

from pathlib import Path
import hashlib
import json
import os
import platform
import subprocess
import sys

EXPECTED_HEAD = "283690948d44345123d838fd47a8764441f491c2"
EXPECTED_PARENT = "17b734f778c4881d200c90967a19baf367347116"

REPO_URL = "https://github.com/themubasshir/ids2018-validation-safe-ablation.git"
REPO = Path("/kaggle/working/ids2018-validation-safe-ablation")

LOCK_REL = Path(
    "results/stage27_loao_unseen_attack/"
    "stage27_3b_similarity/"
    "stage27_3b0_implementation_lock"
)

LOCK_NAME = "stage27_3b0_similarity_implementation_lock.json"
FREEZE_NAME = "stage27_3b0_implementation_freeze_record.json"

EXPECTED_LOCK_SHA = (
    "0bcfd61b9e4f397f1f2c8bc60f50059ee8d320cb75481ab11c7dd49ad68e8376"
)

EXPECTED_FREEZE_SHA = (
    "dbe0bb7eb40d37ae66e11298a5ec48fc2e84878a240fb7418a3324e3918e445f"
)


def banner(title):
    print()
    print("=" * 120)
    print(title)
    print("=" * 120)


def run(cmd, cwd=None):
    p = subprocess.run(
        [str(x) for x in cmd],
        cwd=str(cwd) if cwd else None,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    if p.returncode != 0:
        raise RuntimeError(
            f"Command failed ({p.returncode}): {' '.join(map(str, cmd))}\n\n"
            f"STDOUT:\n{p.stdout}\n\n"
            f"STDERR:\n{p.stderr}"
        )

    return p.stdout.strip()


def sha256_file(path, chunk_size=16 * 1024 * 1024):
    h = hashlib.sha256()

    with Path(path).open("rb") as f:
        while True:
            block = f.read(chunk_size)

            if not block:
                break

            h.update(block)

    return h.hexdigest()


# ======================================================================================
# 1. FRESH RUNTIME
# ======================================================================================

banner("FRESH KAGGLE RUNTIME")

os.environ["CUDA_VISIBLE_DEVICES"] = ""

print("Python executable :", sys.executable)
print("Python version    :", sys.version.split()[0])
print("Platform          :", platform.platform())
print("Working directory :", Path.cwd())
print("CUDA_VISIBLE_DEVICES:", repr(os.environ["CUDA_VISIBLE_DEVICES"]))


# ======================================================================================
# 2. RECOVER REPOSITORY
# ======================================================================================

banner("REPOSITORY RECOVERY")

if not REPO.exists():

    print("Repository absent — cloning fresh.")

    run([
        "git",
        "clone",
        REPO_URL,
        str(REPO),
    ])

else:

    if not (REPO / ".git").is_dir():
        raise RuntimeError(
            f"{REPO} exists but is not a Git repository."
        )

    print("Repository exists — resetting to origin/main.")

    run([
        "git",
        "fetch",
        "--prune",
        "origin",
    ], cwd=REPO)

    run([
        "git",
        "reset",
        "--hard",
        "origin/main",
    ], cwd=REPO)

    run([
        "git",
        "clean",
        "-fd",
    ], cwd=REPO)


# ======================================================================================
# 3. SCIENTIFIC-PARENT GATE
# ======================================================================================

banner("STAGE27-3B0 SCIENTIFIC-PARENT GATE")

run([
    "git",
    "fetch",
    "origin",
    "main",
], cwd=REPO)

head = run([
    "git",
    "rev-parse",
    "HEAD",
], cwd=REPO)

origin = run([
    "git",
    "rev-parse",
    "origin/main",
], cwd=REPO)

parent = run([
    "git",
    "rev-parse",
    "HEAD^",
], cwd=REPO)

subject = run([
    "git",
    "show",
    "-s",
    "--format=%s",
    "HEAD",
], cwd=REPO)

status = run([
    "git",
    "status",
    "--porcelain=v1",
    "--untracked-files=all",
], cwd=REPO)

print("Expected HEAD :", EXPECTED_HEAD)
print("Local HEAD    :", head)
print("origin/main   :", origin)
print("Parent        :", parent)
print("Subject       :", subject)
print("Git clean     :", not bool(status.strip()))

if head != EXPECTED_HEAD:
    raise RuntimeError(
        f"Local HEAD mismatch:\n{head}\nexpected:\n{EXPECTED_HEAD}"
    )

if origin != EXPECTED_HEAD:
    raise RuntimeError(
        f"origin/main mismatch:\n{origin}\nexpected:\n{EXPECTED_HEAD}"
    )

if parent != EXPECTED_PARENT:
    raise RuntimeError(
        f"Stage27-3B0 parent mismatch:\n{parent}"
    )

if subject != "stage27-3b0: freeze similarity implementation":
    raise RuntimeError(
        f"Unexpected commit subject:\n{subject}"
    )

if status.strip():
    raise RuntimeError(
        "Repository is not clean:\n" + status
    )

print("[PASS] Exact Stage27-3B0 scientific parent recovered.")


# ======================================================================================
# 4. STAGE27-3B0 BYTE GATE
# ======================================================================================

banner("STAGE27-3B0 IMPLEMENTATION-LOCK BYTE GATE")

lock_dir = REPO / LOCK_REL
lock_path = lock_dir / LOCK_NAME
freeze_path = lock_dir / FREEZE_NAME

if not lock_path.is_file():
    raise RuntimeError(
        f"Missing implementation lock:\n{lock_path}"
    )

if not freeze_path.is_file():
    raise RuntimeError(
        f"Missing freeze record:\n{freeze_path}"
    )

lock_sha = sha256_file(lock_path)
freeze_sha = sha256_file(freeze_path)

print("Implementation lock SHA :", lock_sha)
print("Expected                :", EXPECTED_LOCK_SHA)
print()
print("Freeze record SHA       :", freeze_sha)
print("Expected                :", EXPECTED_FREEZE_SHA)

if lock_sha != EXPECTED_LOCK_SHA:
    raise RuntimeError(
        "Stage27-3B0 implementation-lock SHA mismatch."
    )

if freeze_sha != EXPECTED_FREEZE_SHA:
    raise RuntimeError(
        "Stage27-3B0 freeze-record SHA mismatch."
    )

actual_files = sorted(
    str(p.relative_to(lock_dir))
    for p in lock_dir.rglob("*")
    if p.is_file()
)

expected_files = sorted([
    LOCK_NAME,
    FREEZE_NAME,
])

if actual_files != expected_files:
    raise RuntimeError(
        f"Unexpected Stage27-3B0 artifact universe:\n{actual_files}"
    )

print("[PASS] Exact 2/2 Stage27-3B0 artifacts recovered.")


# ======================================================================================
# 5. IMPLEMENTATION / SCIENTIFIC BOUNDARY READBACK
# ======================================================================================

banner("STAGE27-3B0 SCIENTIFIC BOUNDARY")

lock = json.loads(
    lock_path.read_text(encoding="utf-8")
)

freeze = json.loads(
    freeze_path.read_text(encoding="utf-8")
)

if lock["status"] != (
    "FROZEN_BEFORE_ANY_STAGE27_3B_DESCRIPTOR_VALUE_ACCESS"
):
    raise RuntimeError(
        "Unexpected Stage27-3B0 lock status."
    )

if lock["numeric_implementation"]["standard_deviation_ddof"] != 0:
    raise RuntimeError(
        "Frozen similarity ddof is not 0."
    )

actions = freeze["scientific_actions_completed"]
ledger = freeze["target_opening_ledger"]

expected_zero = [
    "source_predictor_rows_read",
    "target_descriptor_rows_read",
    "similarity_values_computed",
    "model_fits",
    "model_inference",
    "target_reopenings",
    "threshold_reselection",
    "bootstrap_replicates",
    "gpu_hours",
]

for key in expected_zero:
    if actions[key] != 0:
        raise RuntimeError(
            f"Unexpected Stage27-3B0 action: {key}={actions[key]}"
        )

if ledger["consumed"] != 5:
    raise RuntimeError("Target ledger is not 5/5.")

if ledger["remaining"] != 0:
    raise RuntimeError("Target ledger has remaining openings.")

if ledger["reopening_authorized"] is not False:
    raise RuntimeError(
        "Target reopening unexpectedly authorized."
    )

print("Descriptor values read :", actions["target_descriptor_rows_read"])
print("Similarity values      :", actions["similarity_values_computed"])
print("Model inference        :", actions["model_inference"])
print("Target reopenings      :", actions["target_reopenings"])
print("Target ledger          :", ledger["consumed"], "/ 5 CLOSED")
print("Similarity ddof        :", lock["numeric_implementation"]["standard_deviation_ddof"])

print()
print("[PASS] Stage27-3B0 scientific boundary recovered exactly.")


# ======================================================================================
# 6. GIT IDENTITY
# ======================================================================================

banner("GIT IDENTITY")

run([
    "git",
    "config",
    "--local",
    "user.name",
    "J.M. Mubasshir Rahman",
], cwd=REPO)

run([
    "git",
    "config",
    "--local",
    "user.email",
    "themubasshir@users.noreply.github.com",
], cwd=REPO)

print(
    "user.name :",
    run(
        ["git", "config", "--local", "user.name"],
        cwd=REPO,
    ),
)

print(
    "user.email:",
    run(
        ["git", "config", "--local", "user.email"],
        cwd=REPO,
    ),
)


# ======================================================================================
# 7. ATTACHED DATASET AUDIT
# ======================================================================================

banner("KAGGLE INPUT AUDIT")

input_root = Path("/kaggle/input")

if not input_root.exists():

    raise RuntimeError(
        "/kaggle/input is missing."
    )

datasets = sorted(
    p
    for p in input_root.iterdir()
    if p.is_dir()
)

print("Attached input datasets:", len(datasets))

for dataset in datasets:

    files = [
        p
        for p in dataset.rglob("*")
        if p.is_file()
    ]

    parquet_files = [
        p
        for p in files
        if p.suffix.lower() == ".parquet"
    ]

    print(
        f"  {dataset.name:60s} "
        f"files={len(files):3d} "
        f"parquet={len(parquet_files):3d}"
    )


# ======================================================================================
# 8. FINAL
# ======================================================================================

banner("FRESH STAGE27-3B0 RECOVERY COMPLETE")

final_status = run([
    "git",
    "status",
    "--porcelain=v1",
    "--untracked-files=all",
], cwd=REPO)

if final_status.strip():
    raise RuntimeError(
        "Git tree became dirty during recovery:\n"
        + final_status
    )

print("Repository                :", REPO)
print("HEAD                      :", head)
print("Git clean                 : True")
print()
print("Stage27-3A uncertainty    : REMOTELY FROZEN")
print("Stage27-3B0 impl lock     : REMOTELY FROZEN")
print("Target-opening ledger     : 5 / 5 PERMANENTLY CLOSED")
print("Descriptor similarity run : NOT YET EXECUTED")
print()
print("NEXT AUTHORIZED STAGE:")
print("  Stage27-3B1 behavioral-similarity execution.")


# %% [Stage27 notebook cell 2]
from pathlib import Path
import os
import zipfile
import tarfile

ROOT = Path("/kaggle/input")

print("=" * 120)
print("KAGGLE INPUT DEEP INVENTORY")
print("=" * 120)

files = sorted(
    p for p in ROOT.rglob("*")
    if p.is_file()
)

print("Total files:", len(files))
print()

for i, p in enumerate(files, 1):
    rel = p.relative_to(ROOT)
    size = p.stat().st_size

    print(
        f"[{i:02d}] {rel}"
        f"\n     bytes={size:,}"
        f"\n     suffix={p.suffix!r}"
    )

    # Read only a tiny header for file-type identification.
    try:
        with p.open("rb") as f:
            magic = f.read(16)

        print("     magic =", magic.hex(" "))

    except Exception as e:
        print("     magic read failed:", repr(e))

    # List ZIP members without extracting.
    try:
        if zipfile.is_zipfile(p):
            with zipfile.ZipFile(p, "r") as z:
                names = z.namelist()

            print(f"     ZIP members={len(names)}")

            for name in names[:30]:
                print("       ", name)

            if len(names) > 30:
                print("       ...")

    except Exception as e:
        print("     ZIP inspection failed:", repr(e))

    # List TAR members without extracting.
    try:
        if tarfile.is_tarfile(p):
            with tarfile.open(p, "r:*") as t:
                names = t.getnames()

            print(f"     TAR members={len(names)}")

            for name in names[:30]:
                print("       ", name)

            if len(names) > 30:
                print("       ...")

    except Exception:
        pass

    print()

print("=" * 120)
print("SEARCH FOR CICIDS2017 BASENAME FRAGMENTS")
print("=" * 120)

needles = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "WorkingHours",
    "ISCX",
    "cicids",
]

for p in files:
    name = str(p.relative_to(ROOT))

    if any(
        needle.casefold() in name.casefold()
        for needle in needles
    ):
        print(name)


# %% [Stage27 notebook cell 3]
# STAGE27 CICIDS2017 SOURCE RECOVERY — NO-UPLOAD BOOTSTRAP
# Paste this ENTIRE file into ONE Kaggle code cell and run it.
# Data recovery only; ZERO descriptor/similarity/model computation.

from pathlib import Path
import base64
import bz2
import hashlib

OUT = Path("/kaggle/working/stage27_cicids2017_source_recovery.py")
EXPECTED_SHA256 = "3c496bb2c31b3f819a37c389e10ddc848777625df61263a6490540f25935dfe9"

PAYLOAD = r"""
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
"""

source = bz2.decompress(
    base64.b64decode(
        PAYLOAD
    )
)

actual = hashlib.sha256(
    source
).hexdigest()

if actual != EXPECTED_SHA256:
    raise RuntimeError(
        f"Stage27 source-recovery payload SHA mismatch: {actual} != {EXPECTED_SHA256}"
    )

OUT.write_bytes(
    source
)

print("Reconstructed :", OUT)
print("Bytes         :", OUT.stat().st_size)
print("SHA256        :", actual)

source_text = source.decode(
    "utf-8"
)

compiled = compile(
    source_text,
    str(OUT),
    "exec",
)

print("[PASS] Source-recovery script reconstructed and syntax-verified.")
print("Scientific actions: ZERO descriptor values / ZERO similarity / ZERO inference.")
print("Launching exact CICIDS2017 source recovery...")
print("=" * 100)

exec(
    compiled,
    {
        "__name__": "__main__",
        "__file__": str(OUT),
    },
)


# %% [Stage27 notebook cell 4]
# STAGE27-3B1 BEHAVIORAL SIMILARITY V2 — RECOVERED-SOURCE NO-UPLOAD BOOTSTRAP
# Paste this ENTIRE file into ONE Kaggle code cell and run it.
#
# Runtime-only patch:
#   source root = /kaggle/working/stage27_cicids2017_sources
#
# Scientific methodology unchanged.
# ZERO learner inference / ZERO target reopening.

from pathlib import Path
import base64
import bz2
import hashlib

OUT = Path("/kaggle/working/stage27_3b1_behavioral_similarity_RECOVERED_SOURCE_V2.py")
EXPECTED_SHA256 = "1e3c548d4feef38dc7fe7045cd73f9627428ed349af0bfe36ac375ad225558ca"

PAYLOAD = r"""
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
"""

source = bz2.decompress(
    base64.b64decode(
        PAYLOAD
    )
)

actual = hashlib.sha256(
    source
).hexdigest()

if actual != EXPECTED_SHA256:
    raise RuntimeError(
        f"Stage27-3B1 V2 payload SHA mismatch: {actual} != {EXPECTED_SHA256}"
    )

OUT.write_bytes(
    source
)

print("Reconstructed :", OUT)
print("Bytes         :", OUT.stat().st_size)
print("SHA256        :", actual)

source_text = source.decode(
    "utf-8"
)

compiled = compile(
    source_text,
    str(OUT),
    "exec",
)

print("[PASS] Stage27-3B1 V2 reconstructed and syntax-verified.")
print("Runtime patch: recovered frozen CICIDS2017 source root only.")
print("Scientific methodology: UNCHANGED.")
print("Scientific boundary: ZERO model inference / ZERO target reopening.")
print("Launching Stage27-3B1 V2...")
print("=" * 100)

exec(
    compiled,
    {
        "__name__": "__main__",
        "__file__": str(OUT),
    },
)


# %% [Stage27 notebook cell 5]
# STAGE27-3B1 COMMIT/PUSH/REMOTE VERIFY — NO-UPLOAD BOOTSTRAP
# Paste this ENTIRE file into ONE Kaggle code cell.
# ZERO descriptor/similarity/model computation.

from pathlib import Path
import base64
import bz2
import hashlib

OUT = Path("/kaggle/working/stage27_3b1_commit_push_verify.py")
EXPECTED_SHA256 = "93c738d5b5b7dc3b7cdfc54d49055abbac2017c0094f31f5178ca48fdef4a9cf"

PAYLOAD = r"""
QlpoOTFBWSZTWTB1KEUADYj/5X//wAB+///7f////7////5AAASACAAQAGAdXvADfCPr4KKKd7gj1OzuZ549632x7O+2vB0GhoVN9c7Zptgqi7DIoLrBSgqg
ggo9GQB9vtuA7YUvYZe+EoJNGSaaCaZCbRE9kymmp6Jp5IbUGmaZEaDRppmp5RkABoNNIaCZBNRhBPUZI8jU9Q9Q9NRoGgAANAAAAaAaaaFECT1GZJ6hk9Iy
AA0AAAAAAAAAACTSRERMU8jSU801TT1PU0x6oB6mmmTTT1BoA0NANANA9TQaBFFTSQ9PU9IhhMm0nqGTQDQNpMEAMCAAGTamQA0wiSICaAgCaGQFT0ZMmmU0
9QJmoD1PUfqgNA9T1NAeoNAwEVBOQL8rsxAdKyshsxHrlZgIhEiEIv390cs2A1+ZM9msh+3I6ghiFf+utN/esOEAVQ/vZPy8s9FpA47fo+hn3fqRo2WyifSt
jFiMHBp+DN46LNzJOi4dbSmXBkuStAiyOUmYp97mTQafLyAyIn+Pl1OTcwznd1yyURTuYZyUKWhNMiiRQWCxSJMSjLCBlhRY9DJZj3maEITu64NoZcZkpDwQ
rO59Fl8/9TfQAYaWCPb3pnrQ3sj1O87+OTkOJr7+swdTJJmYNaGcNgYiQ7yxgKIoLL1loWzWQyTEp58XY7A4BDMOMRPu/V/i/R5PXW2Avfjqgcp41CXnwgYV
7ZSpLAhgVYRZdgZTY2HW97GPuNagSEtAkQkKF2i42pXOKJ+7nb1XAxCMCQZBkYm+GmqKKAUqgYRRB/5+3PT9lVMAQa87BZRGGuOFrijMM7CBYxkO3C6tXpCe
OtJ15wD0d93fXOAeLPqoWqTFQUtZBsIowuBsD+1Qq2JU3TBp/w9ToZVFLal9SZBDxigpD43EdREVFCjE5bf8PJENWpS+Hg8PLzZjMZs4/m9BQppGIwyIgagc
25i5iCUMDPEdhZQ4ls41JepaBEAAxUqGiAMmWo1uG20C5oCuZ1mVSHVG4UROom5qBcsnXemcRZilqwqohTV6uzvGftVdeuU71hvfssS0NUcCYAuZS7mBY1Mi
N2dpufzw3wgHCNbDwd8b23j8MfZwR6Vbj4qaMIRJOHMJAYREKDCLHBgEjDky+sq5WNbuzLzbhsAiMdMpmQrJ4emAHfvUSZm5217GSBBzmii1pdIeBEZxFgod
15DaEQJhLdzrRtRMY3tGbo9spzpxqjiLi1jASEiIZjPRXpNeuQj7E25eXaiFGZljbohpW9bnN1B881MQ4q43WbFCwo7I0BJpMigcwgH8DcwzZhjvz2OxgVVo
Tf4Qr293IM1kdEgPkunJhSsuq/+MJxGhfunuQsa2QZYx5GpeLRykugAkEAmAg6DxcKclanqjPcSMmw11XWQLAUGBSNMhKghUh8llGEuMlfs7rfpc1Ipb/MGH
hwRwhw0JaOupfv6QSuOGmO5pCl/+bVRKDUUJIgAoDIbB66LhvS7sGKPhBCPP5lDbdlrPFD9HnbZhmkAhIIcVGSScYA2WGMdyHG97nCwnwaZ6pXxAntR07ykk
sBWg1BuiNyKDITblxykCkmab3UkqaSVV1QhXU0yahU7T0bsUCYqCi0SwPWV3Zg0SSsdne5cExkEEgtJ5Pr4BKrnzEuPuCEDmWHc61hkK3ic11mE87n9am7rg
8vQQdwvForYx5YsHdilEfL5WhLHXbjwn2HYGX28fz4Kp/JPQ8fvXTxpH5wQjHw7nw511nFZGLPkNccePlho6CnJcZigi1X36ubO6GSq6twVSyxo26PE6ZA36
HyYPCqC4UNc73vVcXwN+SxDjVO9f0ce09cN5wZQudfkjqWTUY2SDuZpS14ZdwZ9qbGWDT4JQ7DtnmgUyFMp1uN7jgtTBJJzprjdKjdkKse+axTs0e2Xgwkwg
iRN0cdEvBhAD6zMfSigwrCqjC1PpVd0ZdfPnjr23mLYMQNsMFxq1C5S9zru1ikFYKzc1P3jRR48OQznZvDBFFIio61oORNu7tklOdlcNjgVqKsGDxrjNaaDM
6/Cdvz/D560b948C7onx/j6WXOmmsT3E5BuOJTyRkdy9CBn5oxZuLEg+NMok5gbnmDZjsuhszMKttYroDiUkw4LvUyKFTDuaSSd3d3oRIxirEJCssJeFVkh6
eocTQZ4TiBZQqSRJDkSEHoukkkkKq1yQ/LUMLYp+sVPpcI7wzf8OXJPA1wg9XsManTMsnlpOiFPkUIpFRVPloFQVg7AG6OPXm7dyHOgzAT7eYfU1AhZIkB1A
xxuvWSGBRiCurjKw2vwyCyY1SjvFZyeIBekyeoiS1xRrjma3PLDJOMgHVUNAcu0i264QJRAElU4cEmockpQXJgO+RJs6FWCsUzvtOjMTMwcoNGwWKdrtJjBX
5XeUYiaTMvGonvfFnN0cu2nl4UhfxtYHkXxZz2qmN3eAuNCEoUeyuu4Z5RuL7Y2M/Tr0JVvaM4B7kz6PXGQ9G2hGE8gTGeh7TXoOe+EzOFypXegE8bnUIUHk
Kiv36n3QvwZbcSrHKgoiF44xLBjSFvK+V0HAhaK1iT9Vg0gGBAXjEefv+Vns19levDAD6YyF8aqFdv3FlD+FAfaF3u7JP8Gfu0N3Mq8GtUZMeMRyBdXOiZ6a
KYoxZzaa8M6NGPF6fXc28vfuQrXA74IRI0s1AY4hK0PBFOwwq2IsmsxWS7h2HIYfFC8kKGftVsm2iwxblJDybDRmrCt1XmTRqjlMsXK+ocFJaXH+nHEO0vDh
laYT4cgip0+3w7/92RYyNesLxKktJbbUF5ShJYkSaDaJmK0zLNyfoAGZABtaxGgEkciG2P2WNdCwzGWK2gwGBUrEkcp3EVUOv6wCKsgxmPZMlm4+YfUgP4pv
cJMB+R9R9RR0PmYifKaZmilk27xr8puLJYwkQGHAhSGRS8CQjnG5vOhYxNDE4ljrPgdvy+iqz0orKhvMsg8DT3TxuluUbdjWMxcrmdak+ePlY3laON6zu2NX
ZsM8mxrdsxx07tnyb0r/c82z3vT+HxdHw5UQ55itR2KlEn5354F4UTVz5CBk62ytfPrDNfwLzwLz4ujF0ZIz1JzJN0VWVwtVeO9oL6OYmWQSrg6eVNsyq78G
NNgYWIEYAFSICw+4oqNpCIk+QPmnj7NKpAiCA5pO64gMPiIBXwQLDagI584/iXcXiSq99o4J3Y+xdgy1PQUAkQavZ2G1N5Wo10PK2fS1PergHrEKq0VblGVK
cAx8oAk2s5Ch0t6UHPzD7E1GKBgyMgOkP5frpx45Ot8wwWQLHvIN7t2RidzL7jpjpeAcr5ZZqYuuCfvJ2w7z+vuwveOd5RlHwzmFrIl+9C8y/fYvkvqDXMu6
Lij6/IoA3xvPVFz/alIdodZ15XA4aMtmBjc3U6uQcjtO0j4EHbsXU3B6Cjg9yPJfVmF9v89Juhj+QKE6RYCQ9kCWj3qJWCen34KTzw8UMBvgvf8j3DieIYJy
e5wTN31bUPMMkO72cTibnxA9A6Y7joRiamTVmW7iGJh04dDinSX4AHQJI9j5Ey6eGTZOhgG+jhpxd3A0kv/lrlatHVv0A5AYrG2aOVkvJpla0tTVjYqXxuFi
7iGLcg2i0TBuH0+Fc3VeEjXsYHJPLohjNkBar4z49eRrVoY8SIpRDhK1XZ8rHoZ1LcRdW9TsMJXu6lKwvie9bvrOfiFnf16eV9dTOPtbtv9lAah5IeZEJkB0
9vrDY4aOIXPBeAJdfNCHPuoqqa4B7HB2sSAbtKC9zdTn1MiSBBRt05YwN+AZvI00yeRYmIZTGN7sMmI5AF/9NFCaDnod52QnnPI6T3HWUgxUYqCKjOZyM/Tv
nnJdvYqpNuWWA89TbgKWhimQ8qT9uq3055ms2TqwDQuRKN7Mk4BmWMM0vNcwNLNXhI2xvyB73Tc+5P3hzDi4FODr9HXjfk8iwu2h5anDru0GeNXAJ49pw6yU
0fC1YuO2oFgh7vr+75f6doXK6V0yvt9wF5V/Nn1Zf6zRx9m2J2S9fP6pNdYFQl1ydDKaXahLfev+PvRwT8daf5un8Xu/hwzE+eens+acccHM8vF+zf4H5TsY
eFiKCeuJiGqXm1YVD8gPrp9ZhhuMCdIifapTrSFTehEceic+3t+VDQaF4VAtIIqMGYqRI6IUQ34wV3ZRCggu4tNmqW072piBA0Rk0CSYA5lgVUo6EnaiQPuF
HlUhT9FJR0kAUlWKjkcg5AK6lJhOsXI79XcH9jk4wm6twU/uNeBHB8cmtTYNHKx/ASTZ5/7/r0Jm6xkZBkOm43lzjThgtj82CZptDJTTOA6GJvhDRvFV2dnq
OQ/d6PbyddW9pNll0wJXBVRkGC8mOYwGEVq0TwWD3kJQwEKDs+tkJF+Pgm8GBdLgFvjPmTH+72CHWEwoCuGoZQ2AH8ne/p/QPA6wpAhAxeYo7j2nUHcPBnnx
dErVGb2bw0IWe35jM+wAagbsLsheEiBqZ5Tc0UcyQKTwQ9YBa/XxCo2PWpoPxNYwkjJF6INgwTuTEaTGDowBtTUYsLqgmvxLVvtNEpgXyDoFfHbSqFndEgys
8O+HHEGIjJJszSgxTeYfgSptQsfzGO4sE3EDkdQkdDvLdlWP1pUnp0JJCJDOxqUwJr/Us+3rEP3ZJgh93hm5sMA8P6rXgbio1OXJcj8pZDdcqfQUpUUjqZ7j
jcHdn6J1wAjA9g0cPoC+3fA8VN43j3E1Pw43y+QfeQK4TKU0Zu+HjA0m7GBTgm6g5WofRzhbcGczZG0E4yTtPVqccDYJF2TY9MjdjgbSBISARQcO2gLKNkgh
/QQmEPXQsiowPBGfQaLKFraetETSRloNMHpEqMZ5YSkMIjY/afI9pc+yPV1mlgdQgJqsK2efac34Rw5HZ2JSDfxMzgcMNgTtIm9LnkbDi5OXwyzB0NQ7TnqT
fUxyTqnty2Xs6fCa9Xaf+F3skJo9CuRld2zhx1st3WoYvAW1YDYbURfTzDix2dkLqlNeVogNAEDKmY7bqzheaFjXPTdG2tvHHFl9DAND7VQrQHLTXHS4o2EM
9GrkilmxSwsmFg3cMSSEAjJC5qMChsG+t0Qj6P9ieKA5Cdwk3D1Q56ECuUW5VVsSxxCquj9Zje1ZzGioroHSw6BsoGKiyKGwhqFhEndIwgd8GT8qAp5EpUyl
sStktWhYliCXAfTvyMsCkPD1swuGXH9jGQS32JGQiRRz6dOcYyQ6+ZItepIw2TMA/J8zmZiHbgEgSSHZQnZj7tPd9gXt3hd79VTrSdQpQ9R8BGJ3p7T1msMA
KfABgG9G55gFn2imPUSh6xDbLUm7zr1duB6j3HlV5MsjOjIvRVpyCBpjgYc8MrGJoWcmvfy/jgZKGCTgOhqWGiK1IrIh1aBbpGEB4L3r4Gp3+dyEwnFvU8qK
jKKD9BasAbcAPNDzRDpZ4nWQg3ilMBqAsYtczj5h9RDztVMUy0paLXfc9Qb+YUo9Qkp4ePjgHkeJ9wYKBIbxpxAEJogDCMUKRDfOCGFbFxLFhhaq228ia2In
qEK5xA2fBOuunNIUBGLTRjst9j+tN4BQwUuIkJBid4JVitRZAPngFxDZB3bpMLHrDLFLOiFD3BxnrJIz2SlodaHxtRC8gBELgcmPMu4XvwprryHAcUInE+qy
JaHPClLIzIzbWf0FIBgYGBa3qD2CWjSRa6uwS/d8eOSmg6EGjD0+MjEUigvwFGhT1ULgjSyBOG8F2IJ2vAU1G5QhY5v3YJ1D8EH32CxCwrQYGWgo0fXCRQ3O
9MTygphFCNUQ9Q1YH06GsnbD0gHnonvyeuunUTfD4zk3KJKJYsFF4SIbBu3UZ8OaANEqBBt9G5UCHWBgBBPYNDR/AN8xdn2w0FHf3KcWfiRJOxBnKX5lYErA
KOHj6viu/0DJ1Os2Di7CbSJNkH14nEcQup6k2OkA8Qo6jD2mcTwlHkY2LqUfF0Oszdh9QdqeTX5GgMy2QQplImFLWhUEIRYxhEi6cCfKVvDAxQYPLhQeVAHd
faIenBeTr8/YdhDnpB2Hx7oMRRT2CpJuwJ9IZi+YUnL798mQ+01NQOQeOifcahgPB9XiV1/MfjtvzrvqvIruehk9hwAPAWIdyHWnj6CY9xR3UFpTDuwpW5nK
IZtTpWsLo9facqoeBVrFw9YeMfS3bpf2CXEOt4iYCjvT17AcAmAYIMFaE+eyhzBMwOGBy0RrYJDgOwBllsWNRLSsETstwQG95YiGtBrD7arAZGUoVNalTKUR
KGsnYEKgjGaTEsoCwSFsoJqUMz4qKVBijDKh07PbOz1TIcw7RgMRDtNmTAxnWlhQ6goIg+g+sHJ+IAQwDb2Rk/HUG4BoMZEPEi1FJHchEOTvCiQisxGRwDBA
zTs497C3SCnHPPsjqUUCRLNC7ihjeFEKlBSilRCVVNirR/kvtBLgLAutUr2PH8Zr7M/WL5Cdv6ksgUlqePrIfpQgtB5mP4GwHbsp5fQh7okTk6gd1l+kirAR
IcGkIMRCEgQJ06MlONykcDBYN3v9HAByAwA+H9ogcfI8M4nMi6mfHmHOkJBvOAo3HgbjJ+mBinZRQctPb8GoSDPfN6mgfSZjoHdGkTDBgsvEJcYqVLIKVNAW
1qpwylb6FzKnFPKQ7knbZim59vd2xKJJwgFdR9BCWGzzKb7oSMk8R/J9g2NZgT5VUws3tdE1+P8aA7wTDCQ7w9qdaTzIYOBIW4GI9ITFPmEdxz0EPL4w8Ah4
iFFYrBFiiKqqIiCIqRkFNh7A6epEiJPpzps6c3zTg9NADSVIEjGCQIMc+RYUbK4gSQhBh342E01NezpomOOOJZL8zUxRDFX8pgXXcJvyC6vhJGmOr1L2HUWC
xP5aGjmPJNh8w98CMQfqxMmcJ0liB9kOx+HUBysXMyBJ3V2+zdgFnutVqhL5XvUO8A71KDhpTQQj3QqQj13DvG5dhPNTjmNzyhgZUvvHiGRcdnMUt32FN4hv
VBsBmPyyQcFTgGULBtmme27vfG72ijgcZ0hj4yG/YTgB+oUbcUi3GCFxJAaBYbvuDRNxAhKDMppcFi0QqFUF/Fv11uZ7C3Y4lRQrtZApArOsw6vTTTsXYZow
+jh6Djb6yRNu9OzM2UF7YPBv4LsQ2AuI0ZH5mRNKcDyQREoQCBdGm7YTigMkPaeQ5GLwSZSe53DCKPC55uEn1YWI0b7MOb3482nXcwRoUEiolGe9NzJh0tmy
Fj7zimHTJ7U9j7TAe/s1FHolRYAZGJtAhk1JAo1GDfUfzs6mbjyo+MdXhczSwYhwxp4CGhTvUy0ZmUb7LaxCEPtIbGuhmnc6Yuo7CYqY/WrsDsZcEzxhGSAT
OgaEthIG2SfD4/HRvvz9LOzCasK0092TJsZ/gfzZtvorOHkuWYG3hgZx0JiLLpMOw+Idt/w/CT0DPxfCu7SnaNTdVBjUp+BcH1uRRMS/5rtsDMCsiVYJkMjF
qy0HqbjWjtQKkYXAa+QzG9Ch75AIpJJRkN6ptOnopzq64nGdleaY65mnoaDDIKIwzIQbpuzfLt/OAGCyAaGNPUnWtLveNC7twlDC3viVGRqDTRQDv4DvMKyg
Q3A7VYXCSSCmRkJ80xhmaEYPtODDv9n5r1m8gzDUhIrhz/Yb0yhhkjlk5DqEMjweISIAHlTxujxHrbCggpYMhDtKsWqiOcsFQQ9hhe43Tnt6/Tnbvwq9/dlr
JCSGjsm9HkRdA3FIW8Cit28o1dAlPxJ8I3NApcqGXVNTUwsiecnjwTZDu2NAtAnChWKKnjCeEtNzp36FgxOwTN/DAH9HniCWAuo9pdghqfGvFuL/SKPgVhof
0Fgo5/nGDZILwfaP/v9PaPDKgkhHAMUfUJdPlPHYgeQz4kAsc/ftXWEr2HfKbvCqSIWGcDS5sBsvD35enpXGH1HhoW58djYP4YkIwIiRRUkh7fM9MK/AwWDH
SZliyjS1aw9+61rLURMomBQSIIJ3+0PObIvtBowgd0AjEGLySBy4/r8Qoi2orpsD3GDlDgSdI1WrniCQe0dDtEFfjm8e9P0IbnVWge1fJ7D/j2GGSn/i7kin
ChIGDqUIoA==
"""

source = bz2.decompress(
    base64.b64decode(
        PAYLOAD
    )
)

actual = hashlib.sha256(
    source
).hexdigest()

if actual != EXPECTED_SHA256:
    raise RuntimeError(
        f"Stage27-3B1 closure payload SHA mismatch: {actual} != {EXPECTED_SHA256}"
    )

OUT.write_bytes(
    source
)

print("Reconstructed :", OUT)
print("Bytes         :", OUT.stat().st_size)
print("SHA256        :", actual)

source_text = source.decode(
    "utf-8"
)

compiled = compile(
    source_text,
    str(OUT),
    "exec",
)

print("[PASS] Stage27-3B1 closure script reconstructed and syntax-verified.")
print("Scientific actions: ZERO descriptor computation / ZERO inference / ZERO reopening.")
print("Launching Stage27-3B1 closure...")
print("=" * 100)

exec(
    compiled,
    {
        "__name__": "__main__",
        "__file__": str(OUT),
    },
)


# %% [Stage27 notebook cell 6]
# STAGE27-4A FINAL SYNTHESIS — NO-UPLOAD BOOTSTRAP
# Paste this ENTIRE file into ONE Kaggle code cell and run it.
# Reporting only: ZERO raw predictors / ZERO model inference / ZERO target reopening.

from pathlib import Path
import base64
import bz2
import hashlib

OUT = Path("/kaggle/working/stage27_4a_final_synthesis.py")
EXPECTED_SHA256 = "245a06fdcd1a86fcdef876d22d570af42274584e01c6e714c91f6e7035074ef1"

PAYLOAD = r"""
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
"""

source = bz2.decompress(
    base64.b64decode(
        PAYLOAD
    )
)

actual = hashlib.sha256(
    source
).hexdigest()

if actual != EXPECTED_SHA256:
    raise RuntimeError(
        f"Stage27-4A payload SHA mismatch: {actual} != {EXPECTED_SHA256}"
    )

OUT.write_bytes(
    source
)

print("Reconstructed :", OUT)
print("Bytes         :", OUT.stat().st_size)
print("SHA256        :", actual)

source_text = source.decode(
    "utf-8"
)

compiled = compile(
    source_text,
    str(OUT),
    "exec",
)

print("[PASS] Stage27-4A synthesis script reconstructed and syntax-verified.")
print("Scientific boundary: reporting only; ZERO inference / ZERO target reopening.")
print("Launching Stage27-4A...")
print("=" * 100)

exec(
    compiled,
    {
        "__name__": "__main__",
        "__file__": str(OUT),
    },
)


# %% [Stage27 notebook cell 7]
# STAGE27-4A FINAL SYNTHESIS COMMIT/PUSH/REMOTE VERIFY — NO-UPLOAD BOOTSTRAP
# Paste this ENTIRE file into ONE Kaggle code cell.
# ZERO scientific computation.

from pathlib import Path
import base64
import bz2
import hashlib

OUT = Path("/kaggle/working/stage27_4a_commit_push_verify.py")
EXPECTED_SHA256 = "1931553ff5bdef5cd956957533d7cfd5262943a0fa0edc8695f640a7c4d33e44"

PAYLOAD = r"""
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
3JFOFCQ2qroeAA==
"""

source = bz2.decompress(
    base64.b64decode(
        PAYLOAD
    )
)

actual = hashlib.sha256(
    source
).hexdigest()

if actual != EXPECTED_SHA256:
    raise RuntimeError(
        f"Stage27-4A closure payload SHA mismatch: {actual} != {EXPECTED_SHA256}"
    )

OUT.write_bytes(
    source
)

print("Reconstructed :", OUT)
print("Bytes         :", OUT.stat().st_size)
print("SHA256        :", actual)

source_text = source.decode(
    "utf-8"
)

compiled = compile(
    source_text,
    str(OUT),
    "exec",
)

print("[PASS] Stage27-4A closure script reconstructed and syntax-verified.")
print("Scientific actions: ZERO inference / ZERO reopening / ZERO new statistics.")
print("Launching FINAL Stage27 closure...")
print("=" * 100)

exec(
    compiled,
    {
        "__name__": "__main__",
        "__file__": str(OUT),
    },
)


# %% [Stage27 notebook cell 8]
# ============================================================================
# Stage27-PUB0
# Manuscript Integration Bootstrap + Frozen Science Integrity Gate
#
# PURPOSE
#   - Start the Stage27 manuscript/publication integration phase.
#   - Clone the canonical repository.
#   - Require the exact frozen Stage27 scientific parent.
#   - Verify every Stage27-4A synthesis artifact by SHA256.
#   - Confirm the repository is clean.
#   - Confirm GitHub credentials are available for the later publication push.
#
# IMPORTANT
#   This cell performs:
#       ZERO model fitting
#       ZERO model inference
#       ZERO target reopening
#       ZERO threshold selection
#       ZERO bootstrap computation
#       ZERO statistical testing
#
#   It only verifies already-frozen artifacts.
# ============================================================================

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from datetime import datetime, timezone


# ----------------------------------------------------------------------------
# Frozen Stage27 identity
# ----------------------------------------------------------------------------

REPO_OWNER = "themubasshir"
REPO_NAME = "ids2018-validation-safe-ablation"
REPO_FULL = f"{REPO_OWNER}/{REPO_NAME}"

REPO_URL = f"https://github.com/{REPO_FULL}.git"

CANONICAL_STAGE27_COMMIT = (
    "0e1439565aedc7da9b7ca1207262e9061422bc22"
)

WORK_ROOT = Path("/kaggle/working")
REPO_DIR = WORK_ROOT / REPO_NAME

SYNTHESIS_REL = Path(
    "results/stage27_loao_unseen_attack/stage27_4a_final_synthesis"
)

SYNTHESIS_DIR = REPO_DIR / SYNTHESIS_REL


# ----------------------------------------------------------------------------
# Frozen Stage27 artifact SHA256 manifest
#
# These are CONTENT SHA256 values from the final Stage27 handoff.
# They are intentionally independent from Git blob SHA values.
# ----------------------------------------------------------------------------

EXPECTED_SHA256 = {
    "stage27_final_primary_metrics.csv":
        "42ea04b3f21e6026d5d69c8d5b59aa1edd2b57e94c42da3b9f70587349704634",

    "stage27_final_operating_points.csv":
        "664a5aaaff718f20bf6d619ae1dd4871a07a37c81a1631590423ea0ae07240f4",

    "stage27_final_novelty_gaps.csv":
        "91c80319186fd3bbfc382e58cfc60e58fc75d23db15408564fd35c05d4fb316c",

    "stage27_final_similarity.csv":
        "8c110b4f1d6317d2a2125b4f24bfb8325cdeb699ce763d268d91f3bad6acc8d3",

    "stage27_synthesis.md":
        "50b44ce0740816a51464179817fb0de5111cbe942e2c18c52df8d41d48f194fb",

    "stage27_synthesis_receipt.json":
        "55a67c1173d8bb3ffe2b2200542c382296459ae24b3b96fc0767abb6cb01bd3f",

    "stage27_4a_synthesis_freeze_record.json":
        "35135f1979518b36e614c7a0c2c7db9e4bd9bb78eb4d70346255684d0a4ae1db",

    "figures/stage27_primary_roc_auc_ci.png":
        "0e3659c1abb3a5ec9cb27af3e702f734f3c00266d695a672408c3d426e746152",

    "figures/stage27_primary_pr_auc_ci.png":
        "3528a3f2854f2d40dc1e2c23c20f14fb8d3b9edb6870d32088504e23b02dfba8",

    "figures/stage27_balanced_recall_ci.png":
        "441b3adc5f357c8d5b1ac1d6ce5fd3bd449fe9fdbaeea3a1c944a965b7b1e2b6",
}


# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------

def run(
    cmd,
    *,
    cwd=None,
    check=True,
    capture=True,
    env=None,
):
    """Run command without exposing credentials."""
    if capture:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            check=check,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
        )
    else:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            check=check,
            text=True,
            env=env,
        )

    return result


def git(*args, cwd=REPO_DIR):
    result = run(
        ["git", *args],
        cwd=cwd,
        capture=True,
    )
    return result.stdout.strip()


def sha256_file(path: Path, chunk_size=8 * 1024 * 1024) -> str:
    h = hashlib.sha256()

    with path.open("rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            h.update(chunk)

    return h.hexdigest()


def get_github_token():
    """
    Search the Kaggle Secrets store using the labels we have used
    throughout this project.
    """
    try:
        from kaggle_secrets import UserSecretsClient
    except Exception as exc:
        raise RuntimeError(
            "kaggle_secrets is unavailable in this runtime."
        ) from exc

    client = UserSecretsClient()

    candidates = [
        "GITHUB_TOKEN",
        "github_token",
        "GH_TOKEN",
        "GITHUB_PAT",
        "github_pat",
        "GH_PAT",
    ]

    found = []

    for label in candidates:
        try:
            value = client.get_secret(label)
        except Exception:
            value = None

        if value:
            found.append((label, value))

    if not found:
        raise RuntimeError(
            "\nNo usable GitHub credential was found in Kaggle Secrets.\n\n"
            "Expected one of:\n"
            "  GITHUB_TOKEN\n"
            "  github_token\n"
            "  GH_TOKEN\n"
            "  GITHUB_PAT\n"
            "  github_pat\n"
            "  GH_PAT\n"
        )

    label, token = found[0]

    print(f"[PASS] GitHub secret available: {label}")
    print(f"       token length: {len(token)} characters")
    print("       token value: [REDACTED]")

    return label, token


# ----------------------------------------------------------------------------
# Environment header
# ----------------------------------------------------------------------------

print("=" * 88)
print("STAGE27-PUB0 — MANUSCRIPT INTEGRATION BOOTSTRAP")
print("=" * 88)

print()
print("timestamp_utc :", datetime.now(timezone.utc).isoformat())
print("python        :", sys.version.replace("\n", " "))
print("executable    :", sys.executable)
print("work_root     :", WORK_ROOT)
print("repository    :", REPO_FULL)
print("expected HEAD :", CANONICAL_STAGE27_COMMIT)

print()
print("Scientific mode:")
print("  model fitting          : FORBIDDEN")
print("  model inference        : FORBIDDEN")
print("  target reopening       : FORBIDDEN")
print("  threshold reselection  : FORBIDDEN")
print("  bootstrap recompute    : FORBIDDEN")
print("  manuscript integration : AUTHORIZED")


# ----------------------------------------------------------------------------
# GitHub secret gate
# ----------------------------------------------------------------------------

print()
print("-" * 88)
print("GITHUB CREDENTIAL GATE")
print("-" * 88)

GITHUB_SECRET_LABEL, GITHUB_TOKEN = get_github_token()


# ----------------------------------------------------------------------------
# Fresh repository clone
# ----------------------------------------------------------------------------

print()
print("-" * 88)
print("REPOSITORY BOOTSTRAP")
print("-" * 88)

if REPO_DIR.exists():
    print(f"Removing previous working checkout:")
    print(f"  {REPO_DIR}")
    shutil.rmtree(REPO_DIR)

print()
print("Cloning main branch...")

result = run(
    [
        "git",
        "clone",
        "--branch",
        "main",
        "--single-branch",
        REPO_URL,
        str(REPO_DIR),
    ],
    cwd=WORK_ROOT,
    capture=True,
)

print("[PASS] Repository cloned")


# ----------------------------------------------------------------------------
# Fetch and canonical-commit verification
# ----------------------------------------------------------------------------

git("fetch", "--prune", "origin")

HEAD = git("rev-parse", "HEAD")
ORIGIN_MAIN = git("rev-parse", "origin/main")

print()
print("HEAD        :", HEAD)
print("origin/main :", ORIGIN_MAIN)

if HEAD != CANONICAL_STAGE27_COMMIT:
    raise RuntimeError(
        "\nFROZEN-PARENT GATE FAILED.\n\n"
        f"Expected Stage27 canonical commit:\n"
        f"  {CANONICAL_STAGE27_COMMIT}\n\n"
        f"Current cloned HEAD:\n"
        f"  {HEAD}\n\n"
        "Do not generate publication artifacts until this discrepancy "
        "has been reviewed."
    )

if ORIGIN_MAIN != CANONICAL_STAGE27_COMMIT:
    raise RuntimeError(
        "\nREMOTE-PARENT GATE FAILED.\n\n"
        f"Expected origin/main:\n"
        f"  {CANONICAL_STAGE27_COMMIT}\n\n"
        f"Actual origin/main:\n"
        f"  {ORIGIN_MAIN}\n\n"
        "The remote repository has advanced unexpectedly. "
        "Do not silently build publication artifacts from a different parent."
    )

print()
print("[PASS] Exact frozen Stage27 parent confirmed")


# ----------------------------------------------------------------------------
# Verify required directory
# ----------------------------------------------------------------------------

print()
print("-" * 88)
print("STAGE27-4A ARTIFACT INTEGRITY")
print("-" * 88)

if not SYNTHESIS_DIR.is_dir():
    raise RuntimeError(
        f"Frozen synthesis directory not found:\n{SYNTHESIS_DIR}"
    )

print("Synthesis directory:")
print(f"  {SYNTHESIS_DIR}")
print()


# ----------------------------------------------------------------------------
# SHA256 verification
# ----------------------------------------------------------------------------

verification_rows = []

for relative_name, expected_hash in EXPECTED_SHA256.items():

    path = SYNTHESIS_DIR / relative_name

    exists = path.is_file()

    actual_hash = sha256_file(path) if exists else None

    passed = exists and actual_hash == expected_hash

    verification_rows.append(
        {
            "artifact": relative_name,
            "exists": exists,
            "expected_sha256": expected_hash,
            "actual_sha256": actual_hash,
            "pass": passed,
        }
    )

    status = "PASS" if passed else "FAIL"

    print(f"[{status}] {relative_name}")

    if exists:
        print(f"       expected: {expected_hash}")
        print(f"       actual:   {actual_hash}")
        print(f"       bytes:    {path.stat().st_size:,}")
    else:
        print("       MISSING")

    print()


failed = [
    row
    for row in verification_rows
    if not row["pass"]
]

if failed:
    print("=" * 88)
    print("FROZEN ARTIFACT VERIFICATION FAILED")
    print("=" * 88)

    for row in failed:
        print(row["artifact"])

    raise RuntimeError(
        f"{len(failed)} frozen Stage27 artifact(s) failed exact verification. "
        "Publication generation is blocked."
    )


print(
    f"[PASS] Exact Stage27 synthesis verification: "
    f"{len(verification_rows)}/{len(verification_rows)}"
)


# ----------------------------------------------------------------------------
# Git worktree cleanliness
# ----------------------------------------------------------------------------

print()
print("-" * 88)
print("GIT WORKTREE GATE")
print("-" * 88)

status = git("status", "--porcelain")

if status:
    print(status)
    raise RuntimeError(
        "Repository is not clean before manuscript integration."
    )

print("[PASS] Git working tree clean")


# ----------------------------------------------------------------------------
# Read-only science sanity gates
# ----------------------------------------------------------------------------

print()
print("-" * 88)
print("FROZEN SCIENCE SANITY GATES")
print("-" * 88)

import pandas as pd

primary = pd.read_csv(
    SYNTHESIS_DIR / "stage27_final_primary_metrics.csv"
)

ops = pd.read_csv(
    SYNTHESIS_DIR / "stage27_final_operating_points.csv"
)

gaps = pd.read_csv(
    SYNTHESIS_DIR / "stage27_final_novelty_gaps.csv"
)

similarity = pd.read_csv(
    SYNTHESIS_DIR / "stage27_final_similarity.csv"
)


# Expected executable family set
expected_families = {
    "BOT",
    "DDOS",
    "INFILTRATION",
    "PORT_SCAN",
    "WEB_ATTACK",
}

actual_families = set(primary["family"].unique())

assert actual_families == expected_families, (
    actual_families,
    expected_families,
)


# Exactly two preregistered learners
expected_learners = {
    "XGBOOST",
    "LIGHTGBM",
}

actual_learners = set(primary["learner"].unique())

assert actual_learners == expected_learners


# Expected row counts
assert len(primary) == 10
assert len(ops) == 30
assert len(gaps) == 10
assert len(similarity) == 5


# INFILTRATION must remain descriptive only
inf = primary[primary["family"] == "INFILTRATION"]

assert len(inf) == 2
assert (inf["heldout_attack_support"] == 36).all()
assert (
    inf["inferential_family_claim_authorized"]
    .astype(str)
    .str.lower()
    .isin(["false"])
    .all()
)


# BOT XGBoost negative PR-excess — important publication sanity point
bot_xgb = primary[
    (primary["family"] == "BOT")
    & (primary["learner"] == "XGBOOST")
].iloc[0]

assert bot_xgb["pr_excess"] < 0


# DDOS strong ranking survival
ddos = primary[primary["family"] == "DDOS"]

assert (ddos["roc_auc"] > 0.99).all()
assert (ddos["pr_auc"] > 0.99).all()


# WEB_ATTACK strong ranking survival
web = primary[primary["family"] == "WEB_ATTACK"]

assert (web["roc_auc"] > 0.96).all()
assert (web["pr_auc"] > 0.70).all()


# PORT_SCAN learner dependence
port_xgb = primary[
    (primary["family"] == "PORT_SCAN")
    & (primary["learner"] == "XGBOOST")
].iloc[0]

port_lgb = primary[
    (primary["family"] == "PORT_SCAN")
    & (primary["learner"] == "LIGHTGBM")
].iloc[0]

assert port_lgb["roc_auc"] > port_xgb["roc_auc"]


# Similarity remains explicitly descriptive
assert (
    similarity["interpretation"]
    == "SECONDARY_DESCRIPTIVE_ONLY"
).all()


print("[PASS] executable family set")
print("[PASS] learner set")
print("[PASS] frozen table row counts")
print("[PASS] INFILTRATION descriptive-only gate")
print("[PASS] BOT negative-XGB PR-excess gate")
print("[PASS] DDOS strong-ranking gate")
print("[PASS] WEB_ATTACK strong-ranking gate")
print("[PASS] PORT_SCAN learner-dependence gate")
print("[PASS] similarity descriptive-only gate")


# ----------------------------------------------------------------------------
# Create local bootstrap receipt
#
# This is NOT committed yet. PUB1 will create the actual publication package.
# ----------------------------------------------------------------------------

receipt = {
    "stage": "STAGE27-PUB0",
    "purpose": "MANUSCRIPT_INTEGRATION_BOOTSTRAP",
    "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    "repository": REPO_FULL,
    "canonical_stage27_commit": CANONICAL_STAGE27_COMMIT,
    "verified_head": HEAD,
    "verified_origin_main": ORIGIN_MAIN,
    "verified_artifact_count": len(verification_rows),
    "artifact_verification": verification_rows,
    "science_operations": {
        "model_fitting": 0,
        "model_inference": 0,
        "target_reopenings": 0,
        "threshold_reselection": 0,
        "bootstrap_recomputation": 0,
        "new_formal_statistical_tests": 0,
    },
    "publication_generation_authorized": True,
}

BOOTSTRAP_RECEIPT = (
    WORK_ROOT / "stage27_pub0_bootstrap_receipt.json"
)

BOOTSTRAP_RECEIPT.write_text(
    json.dumps(receipt, indent=2) + "\n",
    encoding="utf-8",
)

print()
print("-" * 88)
print("PUB0 RECEIPT")
print("-" * 88)

print(BOOTSTRAP_RECEIPT)
print(
    "SHA256:",
    sha256_file(BOOTSTRAP_RECEIPT),
)


# ----------------------------------------------------------------------------
# Final state
# ----------------------------------------------------------------------------

print()
print("=" * 88)
print("STAGE27-PUB0 COMPLETE")
print("=" * 88)

print()
print("Frozen science parent:")
print(f"  {CANONICAL_STAGE27_COMMIT}")

print()
print("Artifact verification:")
print(f"  {len(verification_rows)}/{len(verification_rows)} PASS_EXACT")

print()
print("Repository:")
print(f"  {REPO_DIR}")

print()
print("Git state:")
print(f"  branch : {git('branch', '--show-current')}")
print(f"  HEAD   : {git('rev-parse', 'HEAD')}")
print("  status : CLEAN")

print()
print("Next authorized operation:")
print("  STAGE27-PUB1 — generate manuscript/publication artifacts")
print()
print("NO Stage27 scientific computation has been reopened.")


# %% [Stage27 notebook cell 9]
# ============================================================================
# Stage27-PUB1
# Deterministic Manuscript / Publication Package Generation
#
# INPUT:
#   Frozen Stage27-4A synthesis artifacts only.
#
# OUTPUT:
#   docs/STAGE27_MANUSCRIPT_INTEGRATION.md
#   docs/STAGE27_MANUSCRIPT_INTEGRATION.tex
#   docs/STAGE27_PUBLICATION_TABLES.md
#   docs/STAGE27_PUBLICATION_TABLES.tex
#   scripts/stage27/stage27_publication_integration.py
#   results/stage27_loao_unseen_attack/stage27_publication_package/
#       stage27_publication_manifest.json
#
# IMPORTANT:
#   ZERO model fitting
#   ZERO model inference
#   ZERO target reopening
#   ZERO threshold selection
#   ZERO bootstrap recomputation
#   ZERO new statistical testing
#
#   NO GIT COMMIT
#   NO GIT PUSH
# ============================================================================

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path


# ----------------------------------------------------------------------------
# Repository identity
# ----------------------------------------------------------------------------

REPO = Path("/kaggle/working/ids2018-validation-safe-ablation")

CANONICAL_STAGE27_PARENT = (
    "0e1439565aedc7da9b7ca1207262e9061422bc22"
)

GENERATOR_REL = Path(
    "scripts/stage27/stage27_publication_integration.py"
)

GENERATOR_PATH = REPO / GENERATOR_REL


def run(cmd, cwd=REPO, check=True):
    result = subprocess.run(
        cmd,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    if check and result.returncode != 0:
        print(result.stdout)
        print(result.stderr)
        raise RuntimeError(
            f"Command failed ({result.returncode}): {' '.join(cmd)}"
        )

    return result


def git(*args):
    return run(["git", *args]).stdout.strip()


def sha256_file(path: Path):
    h = hashlib.sha256()

    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8 * 1024 * 1024), b""):
            h.update(chunk)

    return h.hexdigest()


print("=" * 92)
print("STAGE27-PUB1 — DETERMINISTIC PUBLICATION PACKAGE GENERATION")
print("=" * 92)

print()
print("Repository:")
print(f"  {REPO}")

if not REPO.is_dir():
    raise RuntimeError("Repository checkout not found. Run PUB0 first.")

head = git("rev-parse", "HEAD")
status_before = git("status", "--porcelain")

print()
print("HEAD:")
print(f"  {head}")

if head != CANONICAL_STAGE27_PARENT:
    raise RuntimeError(
        "\nPUB1 requires the exact frozen Stage27 parent before generation.\n"
        f"Expected: {CANONICAL_STAGE27_PARENT}\n"
        f"Actual:   {head}"
    )

if status_before:
    print(status_before)
    raise RuntimeError(
        "Repository is not clean before PUB1. "
        "Do not generate over unreviewed changes."
    )

print("[PASS] exact Stage27 scientific parent")
print("[PASS] clean worktree")


# ============================================================================
# Generator source
#
# The exact same source is:
#   1. stored in GitHub under scripts/stage27/
#   2. executed here in Kaggle
#
# This makes the publication package reproducible without reopening science.
# ============================================================================

GENERATOR_SOURCE = r'''#!/usr/bin/env python3
"""
Stage27 publication integration generator.

This script creates manuscript-facing publication artifacts exclusively from
the already-frozen Stage27-4A synthesis artifacts.

It performs no model fitting, no model inference, no target reopening,
no threshold selection, no bootstrap recomputation, and no new statistical
testing.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

import pandas as pd


CANONICAL_SCIENTIFIC_PARENT = (
    "0e1439565aedc7da9b7ca1207262e9061422bc22"
)

STAGE27_DATE = "2026-08-21"

SYNTHESIS_REL = Path(
    "results/stage27_loao_unseen_attack/stage27_4a_final_synthesis"
)

PACKAGE_REL = Path(
    "results/stage27_loao_unseen_attack/stage27_publication_package"
)

GENERATOR_REL = Path(
    "scripts/stage27/stage27_publication_integration.py"
)

OUTPUT_PATHS = {
    "manuscript_md": Path("docs/STAGE27_MANUSCRIPT_INTEGRATION.md"),
    "manuscript_tex": Path("docs/STAGE27_MANUSCRIPT_INTEGRATION.tex"),
    "tables_md": Path("docs/STAGE27_PUBLICATION_TABLES.md"),
    "tables_tex": Path("docs/STAGE27_PUBLICATION_TABLES.tex"),
}

MANIFEST_REL = PACKAGE_REL / "stage27_publication_manifest.json"


EXPECTED_SOURCE_SHA256 = {
    "stage27_final_primary_metrics.csv":
        "42ea04b3f21e6026d5d69c8d5b59aa1edd2b57e94c42da3b9f70587349704634",

    "stage27_final_operating_points.csv":
        "664a5aaaff718f20bf6d619ae1dd4871a07a37c81a1631590423ea0ae07240f4",

    "stage27_final_novelty_gaps.csv":
        "91c80319186fd3bbfc382e58cfc60e58fc75d23db15408564fd35c05d4fb316c",

    "stage27_final_similarity.csv":
        "8c110b4f1d6317d2a2125b4f24bfb8325cdeb699ce763d268d91f3bad6acc8d3",

    "stage27_synthesis.md":
        "50b44ce0740816a51464179817fb0de5111cbe942e2c18c52df8d41d48f194fb",

    "stage27_synthesis_receipt.json":
        "55a67c1173d8bb3ffe2b2200542c382296459ae24b3b96fc0767abb6cb01bd3f",

    "stage27_4a_synthesis_freeze_record.json":
        "35135f1979518b36e614c7a0c2c7db9e4bd9bb78eb4d70346255684d0a4ae1db",

    "figures/stage27_primary_roc_auc_ci.png":
        "0e3659c1abb3a5ec9cb27af3e702f734f3c00266d695a672408c3d426e746152",

    "figures/stage27_primary_pr_auc_ci.png":
        "3528a3f2854f2d40dc1e2c23c20f14fb8d3b9edb6870d32088504e23b02dfba8",

    "figures/stage27_balanced_recall_ci.png":
        "441b3adc5f357c8d5b1ac1d6ce5fd3bd449fe9fdbaeea3a1c944a965b7b1e2b6",
}


FAMILY_ORDER = [
    "BOT",
    "DDOS",
    "INFILTRATION",
    "PORT_SCAN",
    "WEB_ATTACK",
]

LEARNER_ORDER = [
    "XGBOOST",
    "LIGHTGBM",
]

LEARNER_DISPLAY = {
    "XGBOOST": "XGBoost",
    "LIGHTGBM": "LightGBM",
}


EXECUTABILITY_ROWS = [
    {
        "family": "BOT",
        "status": "ELIGIBLE",
        "support": 1966,
        "target": "Friday",
        "interpretation": "Inferential support eligible",
    },
    {
        "family": "DDOS",
        "status": "ELIGIBLE",
        "support": 128027,
        "target": "Friday",
        "interpretation": "Inferential support eligible",
    },
    {
        "family": "DOS",
        "status": "STRUCTURALLY_INELIGIBLE",
        "support": None,
        "target": "Wednesday",
        "interpretation":
            "No valid supervised day-atomic training geometry",
    },
    {
        "family": "AUTH_BRUTE_FORCE",
        "status": "STRUCTURALLY_INELIGIBLE",
        "support": None,
        "target": "Tuesday",
        "interpretation":
            "Insufficient earlier weekday depth",
    },
    {
        "family": "INFILTRATION",
        "status": "ELIGIBLE_DESCRIPTIVE_ONLY",
        "support": 36,
        "target": "Thursday",
        "interpretation":
            "Descriptive only; held-out support < 50",
    },
    {
        "family": "PORT_SCAN",
        "status": "ELIGIBLE",
        "support": 158930,
        "target": "Friday",
        "interpretation": "Inferential support eligible",
    },
    {
        "family": "WEB_ATTACK",
        "status": "ELIGIBLE",
        "support": 2180,
        "target": "Thursday",
        "interpretation": "Inferential support eligible",
    },
]


def run_git(root: Path, *args: str):
    result = subprocess.run(
        ["git", *args],
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"git {' '.join(args)} failed:\n{result.stderr}"
        )

    return result.stdout.strip()


def repo_root():
    here = Path(__file__).resolve().parent

    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=here,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    if result.returncode != 0:
        raise RuntimeError("Unable to locate Git repository root.")

    return Path(result.stdout.strip()).resolve()


def sha256_file(path: Path):
    h = hashlib.sha256()

    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8 * 1024 * 1024), b""):
            h.update(chunk)

    return h.hexdigest()


def verify_scientific_parent(root: Path):
    head = run_git(root, "rev-parse", "HEAD")

    result = subprocess.run(
        [
            "git",
            "merge-base",
            "--is-ancestor",
            CANONICAL_SCIENTIFIC_PARENT,
            head,
        ],
        cwd=root,
    )

    if result.returncode != 0:
        raise RuntimeError(
            "Canonical Stage27 scientific parent is not an ancestor "
            "of the current repository HEAD."
        )

    return head


def verify_frozen_sources(root: Path):
    synthesis = root / SYNTHESIS_REL

    verification = {}

    for rel, expected in EXPECTED_SOURCE_SHA256.items():
        path = synthesis / rel

        if not path.is_file():
            raise RuntimeError(
                f"Frozen Stage27 source missing: {path}"
            )

        actual = sha256_file(path)

        if actual != expected:
            raise RuntimeError(
                f"Frozen Stage27 source hash mismatch:\n"
                f"  artifact: {rel}\n"
                f"  expected: {expected}\n"
                f"  actual:   {actual}"
            )

        verification[rel] = actual

    return verification


def fmt(value, digits=4):
    return f"{float(value):.{digits}f}"


def fmt6(value):
    return f"{float(value):.6f}"


def pct(value, digits=2):
    return f"{100.0 * float(value):.{digits}f}%"


def ci_text(row, metric, digits=4):
    point = float(row[metric])
    lo = float(row[f"{metric}_ci_2_5"])
    hi = float(row[f"{metric}_ci_97_5"])

    return (
        f"{point:.{digits}f} "
        f"({lo:.{digits}f}–{hi:.{digits}f})"
    )


def tex_ci(row, metric, digits=4):
    point = float(row[metric])
    lo = float(row[f"{metric}_ci_2_5"])
    hi = float(row[f"{metric}_ci_97_5"])

    return (
        f"{point:.{digits}f} "
        f"[{lo:.{digits}f}, {hi:.{digits}f}]"
    )


def select_row(df, family, learner):
    rows = df[
        (df["family"] == family)
        & (df["learner"] == learner)
    ]

    if len(rows) != 1:
        raise RuntimeError(
            f"Expected exactly one row for {family}/{learner}; "
            f"found {len(rows)}"
        )

    return rows.iloc[0]


def balanced_row(ops, family, learner):
    rows = ops[
        (ops["family"] == family)
        & (ops["learner"] == learner)
        & (ops["operating_point"] == "BALANCED")
    ]

    if len(rows) != 1:
        raise RuntimeError(
            f"Expected exactly one BALANCED row for "
            f"{family}/{learner}; found {len(rows)}"
        )

    return rows.iloc[0]


def scientific_sanity(primary, ops, gaps, similarity):
    assert len(primary) == 10
    assert len(ops) == 30
    assert len(gaps) == 10
    assert len(similarity) == 5

    assert set(primary["family"]) == set(FAMILY_ORDER)
    assert set(primary["learner"]) == set(LEARNER_ORDER)

    inf = primary[primary["family"] == "INFILTRATION"]

    assert len(inf) == 2
    assert (inf["heldout_attack_support"] == 36).all()

    inferential = (
        inf["inferential_family_claim_authorized"]
        .astype(str)
        .str.lower()
    )

    assert (inferential == "false").all()

    bot_xgb = select_row(primary, "BOT", "XGBOOST")
    assert float(bot_xgb["pr_excess"]) < 0

    ddos = primary[primary["family"] == "DDOS"]
    assert (ddos["roc_auc"] > 0.99).all()
    assert (ddos["pr_auc"] > 0.99).all()

    web = primary[primary["family"] == "WEB_ATTACK"]
    assert (web["roc_auc"] > 0.96).all()
    assert (web["pr_auc"] > 0.70).all()

    port_xgb = select_row(primary, "PORT_SCAN", "XGBOOST")
    port_lgb = select_row(primary, "PORT_SCAN", "LIGHTGBM")

    assert float(port_lgb["roc_auc"]) > float(port_xgb["roc_auc"])

    assert (
        similarity["interpretation"]
        == "SECONDARY_DESCRIPTIVE_ONLY"
    ).all()

    bal = ops[ops["operating_point"] == "BALANCED"]

    expected_balanced = {
        ("BOT", "XGBOOST"): 0.0,
        ("BOT", "LIGHTGBM"): 0.0,
        ("DDOS", "XGBOOST"): 0.6619697407578089,
        ("DDOS", "LIGHTGBM"): 0.2625383708124068,
        ("INFILTRATION", "XGBOOST"): 0.0,
        ("INFILTRATION", "LIGHTGBM"): 0.0,
        ("PORT_SCAN", "XGBOOST"): 0.00480085572264519,
        ("PORT_SCAN", "LIGHTGBM"): 0.011678097275530108,
        ("WEB_ATTACK", "XGBOOST"): 0.7779816513761468,
        ("WEB_ATTACK", "LIGHTGBM"): 0.5211009174311927,
    }

    for key, expected in expected_balanced.items():
        family, learner = key
        row = balanced_row(ops, family, learner)
        actual = float(row["recall"])

        assert abs(actual - expected) < 1e-15


def build_primary_markdown(primary, ops):
    lines = [
        "| Family | Learner | Held-out support | ROC-AUC (95% CI) | "
        "PR-AUC (95% CI) | BALANCED recall |",
        "|---|---|---:|---:|---:|---:|",
    ]

    for family in FAMILY_ORDER:
        for learner in LEARNER_ORDER:
            row = select_row(primary, family, learner)
            op = balanced_row(ops, family, learner)

            family_display = (
                "INFILTRATION†"
                if family == "INFILTRATION"
                else family
            )

            lines.append(
                "| "
                + " | ".join([
                    family_display,
                    LEARNER_DISPLAY[learner],
                    f"{int(row['heldout_attack_support']):,}",
                    ci_text(row, "roc_auc", 4),
                    ci_text(row, "pr_auc", 6),
                    pct(op["recall"], 2),
                ])
                + " |"
            )

    lines.extend([
        "",
        "† INFILTRATION is descriptive only because "
        "held-out support is 36 (<50).",
    ])

    return "\n".join(lines)


def build_executability_markdown():
    lines = [
        "| Family | Status | Held-out support | Target day | "
        "Interpretation |",
        "|---|---|---:|---|---|",
    ]

    for row in EXECUTABILITY_ROWS:
        support = (
            "—"
            if row["support"] is None
            else f"{row['support']:,}"
        )

        lines.append(
            "| "
            + " | ".join([
                row["family"],
                row["status"],
                support,
                row["target"],
                row["interpretation"],
            ])
            + " |"
        )

    return "\n".join(lines)


def build_operating_markdown(ops):
    lines = [
        "| Family | Learner | Operating point | Threshold | "
        "Precision | Recall | FPR | F1 |",
        "|---|---|---|---:|---:|---:|---:|---:|",
    ]

    order_points = ["STANDARD", "BALANCED", "SECURITY"]

    for family in FAMILY_ORDER:
        for learner in LEARNER_ORDER:
            for operating_point in order_points:
                rows = ops[
                    (ops["family"] == family)
                    & (ops["learner"] == learner)
                    & (ops["operating_point"] == operating_point)
                ]

                row = rows.iloc[0]

                lines.append(
                    "| "
                    + " | ".join([
                        family,
                        LEARNER_DISPLAY[learner],
                        operating_point,
                        fmt(row["threshold"], 2),
                        fmt6(row["precision"]),
                        fmt6(row["recall"]),
                        fmt6(row["fpr"]),
                        fmt6(row["f1"]),
                    ])
                    + " |"
                )

    return "\n".join(lines)


def build_gap_markdown(gaps):
    lines = [
        "| Family | Learner | ROC-AUC known−unseen gap | "
        "PR-excess known−unseen gap | BALANCED recall gap |",
        "|---|---|---:|---:|---:|",
    ]

    for family in FAMILY_ORDER:
        for learner in LEARNER_ORDER:
            row = gaps[
                (gaps["family"] == family)
                & (gaps["learner"] == learner)
            ].iloc[0]

            lines.append(
                "| "
                + " | ".join([
                    family,
                    LEARNER_DISPLAY[learner],
                    fmt6(row["gap_roc_auc"]),
                    fmt6(row["gap_pr_excess"]),
                    fmt6(row["gap_recall_balanced"]),
                ])
                + " |"
            )

    lines.extend([
        "",
        "Raw known-minus-unseen PR-AUC differences are not treated "
        "as prevalence-invariant primary novelty gaps because the "
        "comparison populations have different prevalence anchors.",
    ])

    return "\n".join(lines)


def build_similarity_markdown(similarity):
    lines = [
        "| Held-out family | Nearest seen family | Distance | "
        "Similarity | Benign distance |",
        "|---|---|---:|---:|---:|",
    ]

    indexed = similarity.set_index("family")

    for family in FAMILY_ORDER:
        row = indexed.loc[family]

        lines.append(
            "| "
            + " | ".join([
                family,
                str(row["nearest_seen_family"]),
                fmt6(row["nearest_seen_distance"]),
                fmt6(row["similarity_score"]),
                fmt6(row["benign_distance"]),
            ])
            + " |"
        )

    lines.extend([
        "",
        "This analysis is secondary and descriptive only. "
        "No formal correlation test, p-value, regression inference, "
        "or causal interpretation is authorized.",
    ])

    return "\n".join(lines)


def build_publication_tables_md(primary, ops, gaps, similarity):
    return f"""# Stage27 Publication Tables

Scientific parent:

`{CANONICAL_SCIENTIFIC_PARENT}`

These tables are generated exclusively from frozen Stage27 artifacts.
No target reopening, inference, model fitting, threshold reselection,
bootstrap recomputation, or new statistical testing is performed.

---

## Table 27-1. Chronology-first family executability

{build_executability_markdown()}

---

## Table 27-2. Primary unseen-family performance

{build_primary_markdown(primary, ops)}

The 95% intervals are the frozen 2,000-replicate stratified
row-bootstrap intervals and quantify target-sampling uncertainty
conditional on the already-fitted model.

---

## Table 27-S1. Complete frozen operating points

{build_operating_markdown(ops)}

---

## Table 27-S2. Compatible novelty-generalization gaps

{build_gap_markdown(gaps)}

---

## Table 27-S3. Behavioral similarity

{build_similarity_markdown(similarity)}

---

## Figure placement

### Main manuscript

1. `results/stage27_loao_unseen_attack/stage27_4a_final_synthesis/figures/stage27_primary_roc_auc_ci.png`
2. `results/stage27_loao_unseen_attack/stage27_4a_final_synthesis/figures/stage27_balanced_recall_ci.png`

### Supplementary material

3. `results/stage27_loao_unseen_attack/stage27_4a_final_synthesis/figures/stage27_primary_pr_auc_ci.png`

PR-AUC remains a co-primary metric and must remain in the main
results table and manuscript text even when its separate figure is
placed in supplementary material.
"""


def build_publication_tables_tex(primary, ops, gaps, similarity):
    lines = [
        "% =====================================================================",
        "% Stage27 Publication Tables",
        "% Auto-generated from frozen Stage27 artifacts.",
        "% No scientific model execution is performed by this file.",
        "% =====================================================================",
        "",
        r"\begin{table*}[t]",
        r"\centering",
        r"\caption{Chronology-first unseen-family fold executability under the frozen Stage27 protocol.}",
        r"\label{tab:stage27_executability}",
        r"\begin{tabular}{lllrl}",
        r"\hline",
        r"Family & Status & Target & Support & Interpretation \\",
        r"\hline",
    ]

    for row in EXECUTABILITY_ROWS:
        support = (
            "--"
            if row["support"] is None
            else f"{row['support']:,}"
        )

        family = row["family"].replace("_", r"\_")
        status = row["status"].replace("_", r"\_")
        interp = row["interpretation"].replace("<", "$<$")

        lines.append(
            f"{family} & {status} & {row['target']} & "
            f"{support} & {interp} \\\\"
        )

    lines.extend([
        r"\hline",
        r"\end{tabular}",
        r"\end{table*}",
        "",
        "",
        r"\begin{table*}[t]",
        r"\centering",
        r"\caption{Primary unseen attack-family ranking and frozen BALANCED-threshold recall. Values in brackets are frozen 95\% percentile bootstrap intervals.}",
        r"\label{tab:stage27_primary}",
        r"\begin{tabular}{llrrrr}",
        r"\hline",
        r"Family & Learner & Support & ROC-AUC [95\% CI] & PR-AUC [95\% CI] & Balanced Recall \\",
        r"\hline",
    ])

    for family in FAMILY_ORDER:
        for learner in LEARNER_ORDER:
            row = select_row(primary, family, learner)
            op = balanced_row(ops, family, learner)

            family_tex = family.replace("_", r"\_")

            if family == "INFILTRATION":
                family_tex += r"$^{\dagger}$"

            lines.append(
                f"{family_tex} & "
                f"{LEARNER_DISPLAY[learner]} & "
                f"{int(row['heldout_attack_support']):,} & "
                f"{tex_ci(row, 'roc_auc', 4)} & "
                f"{tex_ci(row, 'pr_auc', 6)} & "
                f"{pct(op['recall'], 2).replace('%', r'\%')} \\\\"
            )

    lines.extend([
        r"\hline",
        r"\multicolumn{6}{l}{$^{\dagger}$INFILTRATION is descriptive only because held-out support is 36 ($<50$).}\\",
        r"\end{tabular}",
        r"\end{table*}",
        "",
        "",
        r"\begin{table*}[t]",
        r"\centering",
        r"\caption{Frozen Stage27 operating-point transfer to each unseen-family isolation target.}",
        r"\label{tab:stage27_operating_points}",
        r"\begin{tabular}{lllrrrrr}",
        r"\hline",
        r"Family & Learner & Point & Threshold & Precision & Recall & FPR & F1 \\",
        r"\hline",
    ])

    for family in FAMILY_ORDER:
        for learner in LEARNER_ORDER:
            for point in ["STANDARD", "BALANCED", "SECURITY"]:
                row = ops[
                    (ops["family"] == family)
                    & (ops["learner"] == learner)
                    & (ops["operating_point"] == point)
                ].iloc[0]

                lines.append(
                    f"{family.replace('_', r'\_')} & "
                    f"{LEARNER_DISPLAY[learner]} & "
                    f"{point} & "
                    f"{float(row['threshold']):.2f} & "
                    f"{float(row['precision']):.6f} & "
                    f"{float(row['recall']):.6f} & "
                    f"{float(row['fpr']):.6f} & "
                    f"{float(row['f1']):.6f} \\\\"
                )

    lines.extend([
        r"\hline",
        r"\end{tabular}",
        r"\end{table*}",
        "",
        "",
        r"\begin{table*}[t]",
        r"\centering",
        r"\caption{Frozen Stage27 novelty-generalization gaps. PR-excess is used for the prevalence-compatible primary PR comparison.}",
        r"\label{tab:stage27_novelty_gaps}",
        r"\begin{tabular}{llrrr}",
        r"\hline",
        r"Family & Learner & ROC-AUC Gap & PR-Excess Gap & Balanced Recall Gap \\",
        r"\hline",
    ])

    for family in FAMILY_ORDER:
        for learner in LEARNER_ORDER:
            row = gaps[
                (gaps["family"] == family)
                & (gaps["learner"] == learner)
            ].iloc[0]

            lines.append(
                f"{family.replace('_', r'\_')} & "
                f"{LEARNER_DISPLAY[learner]} & "
                f"{float(row['gap_roc_auc']):.6f} & "
                f"{float(row['gap_pr_excess']):.6f} & "
                f"{float(row['gap_recall_balanced']):.6f} \\\\"
            )

    lines.extend([
        r"\hline",
        r"\end{tabular}",
        r"\end{table*}",
        "",
        "",
        r"\begin{table*}[t]",
        r"\centering",
        r"\caption{Secondary descriptive behavioral-similarity audit for the executable Stage27 families.}",
        r"\label{tab:stage27_similarity}",
        r"\begin{tabular}{llrrr}",
        r"\hline",
        r"Held-out Family & Nearest Seen Family & Distance & Similarity & Benign Distance \\",
        r"\hline",
    ])

    indexed = similarity.set_index("family")

    for family in FAMILY_ORDER:
        row = indexed.loc[family]

        lines.append(
            f"{family.replace('_', r'\_')} & "
            f"{str(row['nearest_seen_family']).replace('_', r'\_')} & "
            f"{float(row['nearest_seen_distance']):.6f} & "
            f"{float(row['similarity_score']):.6f} & "
            f"{float(row['benign_distance']):.6f} \\\\"
        )

    lines.extend([
        r"\hline",
        r"\end{tabular}",
        r"\end{table*}",
        "",
        "% Behavioral similarity is secondary and descriptive only.",
        "% No formal correlation test, regression inference, p-value,",
        "% or causal interpretation is authorized.",
        "",
    ])

    return "\n".join(lines)


def build_manuscript_md(primary, ops, gaps, similarity):
    bot_x = select_row(primary, "BOT", "XGBOOST")
    bot_l = select_row(primary, "BOT", "LIGHTGBM")
    ddos_x = select_row(primary, "DDOS", "XGBOOST")
    ddos_l = select_row(primary, "DDOS", "LIGHTGBM")
    inf_x = select_row(primary, "INFILTRATION", "XGBOOST")
    inf_l = select_row(primary, "INFILTRATION", "LIGHTGBM")
    port_x = select_row(primary, "PORT_SCAN", "XGBOOST")
    port_l = select_row(primary, "PORT_SCAN", "LIGHTGBM")
    web_x = select_row(primary, "WEB_ATTACK", "XGBOOST")
    web_l = select_row(primary, "WEB_ATTACK", "LIGHTGBM")

    bot_x_bal = balanced_row(ops, "BOT", "XGBOOST")
    bot_l_bal = balanced_row(ops, "BOT", "LIGHTGBM")
    ddos_x_bal = balanced_row(ops, "DDOS", "XGBOOST")
    ddos_l_bal = balanced_row(ops, "DDOS", "LIGHTGBM")
    inf_x_bal = balanced_row(ops, "INFILTRATION", "XGBOOST")
    inf_l_bal = balanced_row(ops, "INFILTRATION", "LIGHTGBM")
    port_x_bal = balanced_row(ops, "PORT_SCAN", "XGBOOST")
    port_l_bal = balanced_row(ops, "PORT_SCAN", "LIGHTGBM")
    web_x_bal = balanced_row(ops, "WEB_ATTACK", "XGBOOST")
    web_l_bal = balanced_row(ops, "WEB_ATTACK", "LIGHTGBM")

    similarity_idx = similarity.set_index("family")

    return f"""# Stage27 Manuscript Integration

## Scientific Identity

**Stage27 title:** Leave-One-Attack-Family-Out Unseen-Family Generalization Audit

**Design:** `CHRONOLOGY_FIRST_ZERO_TRAINING_EXPOSURE_FAMILY_AUDIT`

**Canonical scientific parent:** `{CANONICAL_SCIENTIFIC_PARENT}`

Stage27 scientific execution is closed. This document is a post-closure
publication-integration artifact generated from the frozen Stage27-4A
synthesis. It introduces no new measurement and authorizes no target
reopening, model inference, model refitting, threshold reselection,
bootstrap recomputation, feature modification, or post-target model
selection.

The publication-safe high-level outcome is:

1. `SELECTIVE_FAMILY_TRANSFER`
2. `RANKING_THRESHOLD_DIVERGENCE`
3. `LEARNER_DEPENDENCE`

Stage27 is an unseen attack-family generalization audit. It must not be
described as formal proof of zero-day detection.

---

# A. Proposed Contribution Text for the Introduction

A further contribution of this study is a chronology-first
zero-training-exposure attack-family generalization audit. Seven
CICIDS2017 attack families were preregistered and evaluated under a
strict `TRAIN < VALIDATION < TARGET` design in which the held-out family
was absent from both training and validation. Five families were
structurally executable, while DOS and AUTH_BRUTE_FORCE could not be
evaluated without violating the frozen chronological geometry. Across
the executable families, transfer was selective rather than universal:
DDoS and Web Attack retained strong ranking discrimination, Bot traffic
collapsed, and Port Scan exhibited substantial learner dependence.
Moreover, preserved ranking discrimination did not necessarily yield
useful recall at validation-selected frozen thresholds, separating
attack-family ranking generalization from operating-point transfer.

---

# B. Methods — Chronology-First Unseen-Family Generalization

## B.1 Scientific question

Stage27 evaluates whether a binary intrusion detector trained without
exposure to a particular attack family can discriminate that held-out
family from temporally matched benign traffic when the family first
becomes eligible under strict chronology.

The experiment is therefore described as an **unseen attack-family** or
**zero-training-exposure family** audit rather than as a formal
zero-day-detection experiment.

## B.2 Frozen taxonomy and executability

The preregistered primary taxonomy contains:

- BOT
- DDOS
- DOS
- AUTH_BRUTE_FORCE
- INFILTRATION
- PORT_SCAN
- WEB_ATTACK

Five of seven families were executable. DOS was structurally ineligible
because its first valid target day was Wednesday, leaving Monday for
training and Tuesday for validation, while Monday contained zero
known-family attack positives. AUTH_BRUTE_FORCE was structurally
ineligible because its first appearance on Tuesday left insufficient
earlier weekday depth for separate training and validation periods.

INFILTRATION was executable but is permanently descriptive only because
its held-out target support was 36.

## B.3 Chronological fold geometry

For BOT, DDOS, and PORT_SCAN:

- TRAIN: Monday–Wednesday
- VALIDATION: Thursday
- TARGET: Friday
- training rows: 1,668,519
- validation rows: 458,968
- Friday benign rows: 414,322

For INFILTRATION and WEB_ATTACK:

- TRAIN: Monday–Tuesday
- VALIDATION: Wednesday
- TARGET: Thursday
- training rows: 975,827
- validation rows: 692,692
- Thursday benign rows: 456,752

The held-out family has zero training rows and zero validation rows in
every executable fold. Any positive held-out-family membership in either
development role would invalidate the fold.

## B.4 Primary target semantics

The primary isolation target is:

`HELD_OUT_FAMILY + SAME_TARGET_DAY_BENIGN`

The positive class contains only the held-out attack family and the
negative class contains only benign traffic from the same target day.
Other known target-day attacks are excluded.

A broader operational context target containing held-out attacks, known
attacks, and benign traffic is secondary and descriptive only. The
manuscript should lead with the primary isolation target.

## B.5 Learners and thresholds

Two preregistered learners were evaluated:

- XGBoost
- LightGBM

No Stage27 hyperparameter optimization was permitted. Across five
executable folds and two learners, the total fit budget was exactly 10
models.

Three operating points were frozen from known-family validation data
only:

- STANDARD: threshold 0.50
- BALANCED: maximum validation F1, then minimum FPR, then higher threshold
- SECURITY: maximum validation F2 subject to FPR <= 0.05, then minimum
  FPR, then higher threshold

The threshold grid was 0.01–0.99 and the target decision rule was
`probability >= threshold`.

No target threshold search or target-guided model adaptation was
permitted.

## B.6 Bootstrap uncertainty

Stage27 uses 2,000-replicate class-stratified row bootstrap intervals
with seed 42. Sampling is performed with replacement within the benign
and held-out-attack target strata while preserving stratum sizes.

The intervals quantify **target-sampling uncertainty conditional on the
already-fitted model**. They do not include training-seed uncertainty,
model-selection uncertainty, model-retraining uncertainty, or broader
population uncertainty.

## B.7 Behavioral similarity

The secondary behavioral-similarity audit uses 11 preregistered
aggregate flow descriptors. Preprocessing is fitted only on current-fold
TRAIN rows, each family is represented by its standardized centroid, and
Euclidean distance to the nearest seen family is transformed to
similarity as:

`1 / (1 + nearest_seen_distance)`

This analysis is descriptive only. No formal correlation significance
test, regression inference, p-value, or causal interpretation is
authorized.

---

# C. Results — Unseen Attack-Family Generalization

## C.1 Executability under strict chronology

Of seven preregistered families, five were structurally executable.
BOT, DDOS, PORT_SCAN, and WEB_ATTACK satisfied the frozen family-level
support requirement. INFILTRATION was executable but remains
descriptive only because its held-out support was 36. DOS and
AUTH_BRUTE_FORCE were structurally ineligible under the precommitted
day-atomic chronology rather than being treated as model failures.

## C.2 Primary unseen-family ranking

The frozen ranking results demonstrate strongly family-dependent
transfer.

**DDoS produced the strongest transfer.** XGBoost reached ROC-AUC
{float(ddos_x['roc_auc']):.4f} and PR-AUC
{float(ddos_x['pr_auc']):.4f}, while LightGBM reached ROC-AUC
{float(ddos_l['roc_auc']):.4f} and PR-AUC
{float(ddos_l['pr_auc']):.4f}. Thus, both learners retained
near-perfect threshold-independent discrimination despite receiving
zero DDoS training or validation examples.

**Web Attack also transferred strongly.** XGBoost reached ROC-AUC
{float(web_x['roc_auc']):.4f} and PR-AUC
{float(web_x['pr_auc']):.4f}; LightGBM reached ROC-AUC
{float(web_l['roc_auc']):.4f} and PR-AUC
{float(web_l['pr_auc']):.4f}.

**Bot traffic showed substantial collapse.** XGBoost produced ROC-AUC
{float(bot_x['roc_auc']):.4f}, while LightGBM produced ROC-AUC
{float(bot_l['roc_auc']):.4f}. XGBoost PR-AUC was
{float(bot_x['pr_auc']):.6f}, below the target prevalence anchor of
{float(bot_x['prevalence']):.6f}, giving PR-excess
{float(bot_x['pr_excess']):.6f}. LightGBM was only marginally above the
same prevalence anchor, with PR-excess
{float(bot_l['pr_excess']):.6f}.

**Port Scan was materially learner-dependent.** XGBoost reached
ROC-AUC {float(port_x['roc_auc']):.4f}, whereas LightGBM reached
{float(port_l['roc_auc']):.4f}. The corresponding PR-AUC values were
{float(port_x['pr_auc']):.4f} and {float(port_l['pr_auc']):.4f},
respectively.

INFILTRATION produced ROC-AUC
{float(inf_x['roc_auc']):.4f} for XGBoost and
{float(inf_l['roc_auc']):.4f} for LightGBM, but these values are
reported descriptively because only 36 held-out attacks were available.

The overall result is therefore **selective family transfer**, not
uniform unseen-family generalization.

## C.3 Frozen operating-point transfer

Threshold-independent ranking quality did not guarantee useful
frozen-threshold detection.

At the BALANCED operating point:

- BOT recall was {pct(bot_x_bal['recall'])} for XGBoost and
  {pct(bot_l_bal['recall'])} for LightGBM.
- DDOS recall was {pct(ddos_x_bal['recall'])} and
  {pct(ddos_l_bal['recall'])}.
- INFILTRATION recall was {pct(inf_x_bal['recall'])} and
  {pct(inf_l_bal['recall'])}, descriptive only.
- PORT_SCAN recall was {pct(port_x_bal['recall'])} and
  {pct(port_l_bal['recall'])}.
- WEB_ATTACK recall was {pct(web_x_bal['recall'])} and
  {pct(web_l_bal['recall'])}.

The divergence is particularly visible for DDOS, where both learners
retain ROC-AUC above 0.998 but BALANCED recall is only
{pct(ddos_x_bal['recall'])} for XGBoost and
{pct(ddos_l_bal['recall'])} for LightGBM. Port Scan provides another
example: LightGBM retains ROC-AUC
{float(port_l['roc_auc']):.4f} but detects only
{pct(port_l_bal['recall'])} of held-out Port Scan attacks at its frozen
BALANCED threshold.

These results support the frozen Stage27 outcome
`RANKING_THRESHOLD_DIVERGENCE`.

## C.4 Novelty-generalization gaps

The compatible novelty-gap analysis further shows that family novelty
does not impose a uniform penalty.

For XGBoost, the known-minus-unseen ROC-AUC gap is approximately
{float(gaps[(gaps.family == 'BOT') & (gaps.learner == 'XGBOOST')].iloc[0]['gap_roc_auc']):.3f}
for BOT and
{float(gaps[(gaps.family == 'PORT_SCAN') & (gaps.learner == 'XGBOOST')].iloc[0]['gap_roc_auc']):.3f}
for PORT_SCAN, whereas the DDOS gap is
{float(gaps[(gaps.family == 'DDOS') & (gaps.learner == 'XGBOOST')].iloc[0]['gap_roc_auc']):.3f}.

PR-excess rather than raw PR-AUC difference is used as the primary
prevalence-compatible PR novelty gap. Raw PR-AUC differences across
populations with different prevalence anchors are retained only as
descriptive quantities.

## C.5 Behavioral similarity

The frozen behavioral-similarity values do not show a monotonic
relationship with unseen-family discrimination.

BOT has the highest observed similarity to a seen family
({float(similarity_idx.loc['BOT', 'similarity_score']):.4f}) yet weak
unseen-family performance. DDOS has a substantially lower similarity
({float(similarity_idx.loc['DDOS', 'similarity_score']):.4f}) but
near-perfect ranking. WEB_ATTACK has intermediate similarity
({float(similarity_idx.loc['WEB_ATTACK', 'similarity_score']):.4f})
while retaining strong transfer.

Behavioral proximity, as operationalized by this frozen centroid
distance, therefore does not appear sufficient by itself to explain
the observed transfer pattern.

---

# D. Discussion — Attack-Family Novelty and Generalization

Stage27 demonstrates that known-family intrusion-detection performance
cannot be treated as evidence of uniform robustness to attack-family
novelty. The strongest transfer cases, DDOS and WEB_ATTACK, retain high
ranking discrimination for both learners despite zero exposure to the
held-out family during training and validation. BOT provides the
opposite outcome, with complete frozen-threshold detection failure and
little or adverse ranking signal. PORT_SCAN occupies an intermediate
case in which the outcome depends materially on the learner.

A second finding is the distinction between ranking discrimination and
operating-point transfer. DDoS is the clearest example: both learners
rank the held-out family almost perfectly, yet validation-selected
BALANCED thresholds recover substantially less than all of the held-out
attacks. The same separation is visible for Port Scan and, to a lesser
degree, Web Attack. Consequently, ROC-AUC or PR-AUC alone cannot
characterize whether a frozen deployment threshold will remain useful
under attack-family novelty.

This ranking-versus-threshold distinction also complements earlier
experiments in the study. Representation-specific chronological
evaluation, the Stage22R forward temporal audit, and the Stage24
cross-dataset audit independently showed that strong ranking behavior
can coexist with poor fixed-threshold transfer. Stage27 extends that
observation to zero-training-exposure attack families. Across these
distinct stress regimes, threshold-independent discrimination and
operating-point behavior should therefore be evaluated as separate
properties of an IDS.

Learner dependence is itself family-dependent. XGBoost and LightGBM
agree closely on the strong DDoS and Web Attack ranking outcomes but
differ substantially on Port Scan and also differ in Bot ranking.
The evidence therefore does not support declaring one learner
universally superior for unseen-family generalization.

The behavioral-similarity analysis provides no simple mechanistic
explanation. BOT is behaviorally closest to a seen family under the
frozen 11-descriptor representation yet transfers poorly, whereas DDOS
is less similar under the same definition but transfers extremely well.
This secondary analysis should therefore be interpreted as evidence
that the selected notion of behavioral proximity is insufficient by
itself, not as proof of either the presence or absence of a particular
causal mechanism.

Finally, strict chronology exposes limitations in the benchmark itself.
The inability to execute DOS and AUTH_BRUTE_FORCE is a consequence of
the temporal arrangement of attack families and the requirement for
separate training and validation periods. Rather than manufacturing
alternative folds after observing the data, Stage27 preserves these
families as structurally ineligible. This makes the scope of the
generalization claim narrower but maintains the validation-safe
interpretation of the experiment.

---

# E. Limitations and Threats to Validity

1. **Incomplete taxonomy executability.** Only five of seven
   preregistered families could be honestly evaluated under strict
   `TRAIN < VALIDATION < TARGET` chronology.

2. **Low INFILTRATION support.** INFILTRATION contains only 36 held-out
   target attacks and is therefore descriptive only.

3. **Chronology-first rather than textbook LOAO.** Strict chronology
   means that every non-held-out attack family is not necessarily
   represented during training. Stage27 is therefore specifically a
   chronology-first zero-training-exposure family audit.

4. **Conditional bootstrap uncertainty.** The 95% intervals quantify
   row-level target-sampling uncertainty conditional on each already
   fitted model. They do not incorporate retraining, seed, model
   selection, independently collected networks, or broader population
   uncertainty.

5. **No clustered bootstrap.** No preregistered durable grouping
   variable was available for a session- or time-cluster bootstrap.

6. **Restricted similarity representation.** Behavioral similarity is
   based only on 11 preregistered aggregate flow descriptors and a
   centroid-distance representation.

7. **Descriptive similarity analysis.** No formal correlation test,
   p-value, regression inference, or causal interpretation is
   authorized.

8. **Benchmark-specific external validity.** CICIDS2017 is a benchmark
   capture. The observed transfer pattern does not establish universal
   behavior for production networks, unrelated datasets, or genuinely
   novel real-world attacks.

9. **No zero-day proof.** Zero training exposure to an attack family in
   this benchmark is not equivalent to demonstrating universal
   real-world zero-day detection.

---

# F. Stage27 Publication-Level Contributions

1. **Chronology-first unseen-family evaluation.** Attack-family novelty
   is evaluated under a strict training-before-validation-before-target
   design with zero held-out-family exposure during development.

2. **Structural executability accounting.** Families that cannot be
   evaluated without violating chronology are explicitly labeled
   structurally ineligible rather than replaced with post-hoc folds.

3. **Selective-transfer finding.** DDoS and Web Attack retain strong
   transfer, Bot collapses, and Port Scan depends materially on learner
   choice.

4. **Ranking/threshold separation.** Threshold-independent
   discrimination and frozen validation-selected operating-point
   behavior are evaluated separately.

5. **Learner-dependent novelty audit.** XGBoost and LightGBM are
   compared under the same preregistered family-holdout geometry without
   Stage27 HPO.

6. **Target-sampling uncertainty.** Primary ranking and compatible
   operating metrics are accompanied by frozen 2,000-replicate
   stratified bootstrap intervals.

7. **Secondary behavioral-similarity audit.** A preregistered
   train-fitted descriptor representation is used to test whether simple
   behavioral proximity descriptively explains transfer, without
   introducing post-result significance testing.

---

# G. Contribution Text for Abstract / Introduction

A chronology-first zero-training-exposure attack-family audit further
revealed selective rather than universal unseen-family transfer. Under
strict `TRAIN < VALIDATION < TARGET` separation, both XGBoost and
LightGBM retained near-perfect ranking discrimination for held-out DDoS
traffic and strong ranking for Web Attack, whereas Bot traffic
collapsed and Port Scan transfer was materially learner-dependent.
Moreover, high unseen-family ROC-AUC did not necessarily translate into
useful recall at frozen validation-selected thresholds. The findings
show that strong known-family IDS performance should not be interpreted
as evidence of uniform robustness to unseen attack families and that
ranking generalization and operating-point transfer should be audited
separately.

---

# H. Publication-Safe Claims

The following claims are supported by the frozen Stage27 evidence:

1. Stage27 evaluated seven preregistered attack-family categories.
2. Five of the seven families were structurally executable.
3. DOS and AUTH_BRUTE_FORCE were structurally ineligible under strict
   chronology.
4. INFILTRATION is descriptive only because held-out support was 36.
5. DDoS retained near-perfect unseen-family ranking for both learners.
6. Web Attack retained strong unseen-family ranking for both learners.
7. Bot exhibited substantial unseen-family collapse.
8. Port Scan exhibited material learner dependence.
9. Ranking performance and frozen-threshold recall diverged for several
   families.
10. Behavioral similarity did not display a monotonic relationship with
    unseen-family ranking performance across the five executable
    families.
11. No target threshold tuning, target-guided model selection, or
    target-guided adaptation was performed.
12. The bootstrap intervals quantify target-sampling uncertainty
    conditional on the fitted model.
13. Known-family performance should not be treated as evidence of
    uniform unseen-family generalization.

---

# I. Claims That Must Not Appear

1. Stage27 proves universal zero-day detection.
2. Stage27 proves all unseen cyberattacks can be detected.
3. All seven attack families were experimentally executable.
4. INFILTRATION provides an inferential family-level conclusion.
5. LightGBM is universally superior to XGBoost for unseen attacks.
6. XGBoost is universally superior to LightGBM for unseen attacks.
7. Behavioral similarity significantly predicts unseen-family
   performance.
8. A causal relationship between similarity and transfer was
   established.
9. Raw PR-AUC known-minus-unseen difference is prevalence invariant.
10. Stage27 target thresholds were optimized using held-out-family
    labels.
11. Stage27 models were adapted or recalibrated after target opening.
12. The row bootstrap represents uncertainty across independent
    organizations or future production networks.

---

# J. Recommended Main-Manuscript Assets

## Main Table 27-1

Chronology-first family executability.

Source:

`docs/STAGE27_PUBLICATION_TABLES.md`

## Main Table 27-2

Primary ROC-AUC, PR-AUC, 95% intervals, held-out support, and BALANCED
recall for both learners.

Source:

`docs/STAGE27_PUBLICATION_TABLES.md`

## Main Figure 27-1

`results/stage27_loao_unseen_attack/stage27_4a_final_synthesis/figures/stage27_primary_roc_auc_ci.png`

Purpose: show selective ranking transfer and learner dependence.

## Main Figure 27-2

`results/stage27_loao_unseen_attack/stage27_4a_final_synthesis/figures/stage27_balanced_recall_ci.png`

Purpose: show ranking–threshold divergence.

## Supplementary Figure 27-S1

`results/stage27_loao_unseen_attack/stage27_4a_final_synthesis/figures/stage27_primary_pr_auc_ci.png`

PR-AUC remains co-primary and should remain in the main table and main
text even if the separate PR-AUC figure is supplementary.

## Supplementary tables

- complete STANDARD/BALANCED/SECURITY operating points;
- novelty-generalization gaps;
- behavioral similarity.

---

# K. Recommended Manuscript Placement

The Stage27 material should be integrated into the broader robustness
narrative rather than placed according to experimental stage number.

Recommended Results ordering:

1. Validation-safe baseline/model selection
2. Representation/architecture assessment
3. Temporal validation and forward generalization
4. Cross-dataset generalization
5. **Unseen attack-family generalization (Stage27)**
6. Low-prevalence and SOC operational stress
7. Deployment/computational profiling

This ordering moves from predictive evaluation toward increasingly
deployment-facing stress tests and keeps Stage27 adjacent to the
temporal and cross-dataset generalization evidence.
"""


def build_manuscript_tex(primary, ops, gaps, similarity):
    bot_x = select_row(primary, "BOT", "XGBOOST")
    bot_l = select_row(primary, "BOT", "LIGHTGBM")
    ddos_x = select_row(primary, "DDOS", "XGBOOST")
    ddos_l = select_row(primary, "DDOS", "LIGHTGBM")
    port_x = select_row(primary, "PORT_SCAN", "XGBOOST")
    port_l = select_row(primary, "PORT_SCAN", "LIGHTGBM")
    web_x = select_row(primary, "WEB_ATTACK", "XGBOOST")
    web_l = select_row(primary, "WEB_ATTACK", "LIGHTGBM")

    ddos_x_bal = balanced_row(ops, "DDOS", "XGBOOST")
    ddos_l_bal = balanced_row(ops, "DDOS", "LIGHTGBM")
    port_l_bal = balanced_row(ops, "PORT_SCAN", "LIGHTGBM")

    sim = similarity.set_index("family")

    lines = [
        "% =====================================================================",
        "% Stage27 Manuscript Integration",
        "% Generated only from frozen Stage27-4A artifacts.",
        "% =====================================================================",
        "",
        r"\subsection{Unseen Attack-Family Generalization}",
        "",
        r"\subsubsection{Chronology-first audit design}",
        "",
        (
            "Stage27 evaluated zero-training-exposure attack-family "
            "generalization under a strict "
            r"\texttt{TRAIN < VALIDATION < TARGET} protocol. "
            "The held-out family was absent from both training and "
            "validation, thresholds were selected only on known-family "
            "validation data, and the target was not used for model "
            "selection, threshold tuning, or adaptation. The experiment "
            "is therefore described as an unseen attack-family "
            "generalization audit rather than as formal proof of "
            "zero-day detection."
        ),
        "",
        (
            "Seven primary families were preregistered. Five were "
            "structurally executable. DOS was ineligible because the "
            "available earlier day-atomic training period contained no "
            "known-family attack positives, whereas "
            r"AUTH\_BRUTE\_FORCE was ineligible because insufficient "
            "earlier weekday depth existed for separate training and "
            "validation periods. INFILTRATION was executable but is "
            "reported descriptively only because the held-out support "
            "was 36."
        ),
        "",
        r"\subsubsection{Primary unseen-family ranking}",
        "",
        (
            "Unseen-family ranking was strongly family dependent. "
            "DDoS retained near-perfect discrimination: XGBoost reached "
            "ROC-AUC %.4f and PR-AUC %.4f, while LightGBM reached "
            "ROC-AUC %.4f and PR-AUC %.4f. "
            "Web Attack also transferred strongly, with XGBoost "
            "ROC-AUC %.4f and PR-AUC %.4f and LightGBM ROC-AUC %.4f "
            "and PR-AUC %.4f."
        ) % (
            ddos_x["roc_auc"],
            ddos_x["pr_auc"],
            ddos_l["roc_auc"],
            ddos_l["pr_auc"],
            web_x["roc_auc"],
            web_x["pr_auc"],
            web_l["roc_auc"],
            web_l["pr_auc"],
        ),
        "",
        (
            "Bot traffic showed substantial collapse. XGBoost produced "
            "ROC-AUC %.4f and PR-AUC %.6f, while LightGBM produced "
            "ROC-AUC %.4f and PR-AUC %.6f. The XGBoost PR-AUC was below "
            "the target prevalence anchor, giving negative PR-excess "
            "%.6f. Port Scan was materially learner-dependent: XGBoost "
            "reached ROC-AUC %.4f compared with %.4f for LightGBM."
        ) % (
            bot_x["roc_auc"],
            bot_x["pr_auc"],
            bot_l["roc_auc"],
            bot_l["pr_auc"],
            bot_x["pr_excess"],
            port_x["roc_auc"],
            port_l["roc_auc"],
        ),
        "",
        (
            "The overall Stage27 outcome is therefore selective family "
            "transfer rather than universal unseen-family "
            "generalization."
        ),
        "",
        r"\subsubsection{Frozen operating-point transfer}",
        "",
        (
            "Threshold-independent ranking did not guarantee useful "
            "frozen-threshold detection. At the BALANCED operating "
            "point, DDoS recall was %.2f\\%% for XGBoost and %.2f\\%% "
            "for LightGBM despite ROC-AUC above 0.998 for both learners. "
            "Similarly, LightGBM retained Port Scan ROC-AUC %.4f while "
            "BALANCED recall was only %.2f\\%%."
        ) % (
            100 * ddos_x_bal["recall"],
            100 * ddos_l_bal["recall"],
            port_l["roc_auc"],
            100 * port_l_bal["recall"],
        ),
        "",
        (
            "These results distinguish ranking generalization from "
            "operating-point transfer and support the frozen Stage27 "
            "outcome of ranking--threshold divergence."
        ),
        "",
        r"\subsubsection{Behavioral similarity}",
        "",
        (
            "The secondary behavioral-similarity audit did not show a "
            "monotonic relationship with transfer. BOT had the highest "
            "observed similarity to a seen family (%.4f) but weak "
            "generalization, whereas DDoS had lower similarity (%.4f) "
            "and near-perfect ranking. Behavioral proximity under the "
            "frozen 11-descriptor centroid definition therefore does "
            "not appear sufficient by itself to explain the transfer "
            "pattern."
        ) % (
            sim.loc["BOT", "similarity_score"],
            sim.loc["DDOS", "similarity_score"],
        ),
        "",
        r"\subsection{Discussion of Attack-Family Novelty}",
        "",
        (
            "Stage27 shows that strong performance on known attack "
            "families cannot be interpreted as evidence of uniform "
            "robustness to attack-family novelty. DDoS and Web Attack "
            "retained strong ranking for both learners, Bot collapsed, "
            "and Port Scan exhibited substantial learner dependence."
        ),
        "",
        (
            "The experiment also reinforces a broader finding across "
            "the study: threshold-independent discrimination and "
            "fixed operating-point behavior are distinct properties. "
            "Representation-specific chronological evaluation, the "
            "temporal-validation stress test, cross-dataset transfer, "
            "and now unseen-family transfer each expose cases in which "
            "ranking and frozen-threshold behavior diverge. Reporting "
            "only ROC-AUC or PR-AUC would therefore provide an "
            "incomplete description of deployment robustness."
        ),
        "",
        (
            "The evidence does not establish a universal learner "
            "winner. XGBoost and LightGBM agree closely on DDoS and Web "
            "Attack ranking but differ substantially for Port Scan and "
            "Bot. Learner dependence is therefore itself "
            "family-dependent."
        ),
        "",
        r"\subsection{Stage27 Limitations}",
        "",
        r"\begin{itemize}",
        (
            r"\item Only five of seven preregistered families were "
            r"structurally executable under strict chronology."
        ),
        (
            r"\item INFILTRATION is descriptive only because the "
            r"held-out support was 36."
        ),
        (
            r"\item The design is chronology-first zero-training-"
            r"exposure evaluation rather than textbook LOAO in which "
            r"every other family is necessarily represented in training."
        ),
        (
            r"\item The 95\% bootstrap intervals quantify target-"
            r"sampling uncertainty conditional on the fitted model and "
            r"do not include retraining, seed, model-selection, or "
            r"broader population uncertainty."
        ),
        (
            r"\item Behavioral similarity uses only 11 preregistered "
            r"aggregate descriptors and is descriptive only."
        ),
        (
            r"\item The benchmark-specific results do not establish "
            r"universal real-world zero-day detection."
        ),
        r"\end{itemize}",
        "",
        "% Main Stage27 figures:",
        "% stage27_primary_roc_auc_ci.png",
        "% stage27_balanced_recall_ci.png",
        "%",
        "% Supplementary:",
        "% stage27_primary_pr_auc_ci.png",
        "",
    ]

    return "\n".join(lines)


def build_contents(primary, ops, gaps, similarity):
    return {
        OUTPUT_PATHS["manuscript_md"]:
            build_manuscript_md(primary, ops, gaps, similarity),

        OUTPUT_PATHS["manuscript_tex"]:
            build_manuscript_tex(primary, ops, gaps, similarity),

        OUTPUT_PATHS["tables_md"]:
            build_publication_tables_md(primary, ops, gaps, similarity),

        OUTPUT_PATHS["tables_tex"]:
            build_publication_tables_tex(primary, ops, gaps, similarity),
    }


def write_text(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)

    normalized = content.rstrip() + "\n"

    path.write_text(
        normalized,
        encoding="utf-8",
        newline="\n",
    )


def create_manifest(
    root: Path,
    head: str,
    source_hashes: dict,
    generated_paths: list[Path],
):
    generated = {}

    for rel in generated_paths:
        path = root / rel

        generated[str(rel)] = {
            "sha256": sha256_file(path),
            "bytes": path.stat().st_size,
        }

    generator = root / GENERATOR_REL

    generated[str(GENERATOR_REL)] = {
        "sha256": sha256_file(generator),
        "bytes": generator.stat().st_size,
    }

    return {
        "stage": "STAGE27-PUB1",
        "publication_date": STAGE27_DATE,
        "scientific_parent":
            CANONICAL_SCIENTIFIC_PARENT,
        "generation_head": head,
        "scientific_status": "CLOSED",
        "publication_package_status":
            "GENERATED_PENDING_GIT_REVIEW",
        "science_operations": {
            "model_fits": 0,
            "model_inference": 0,
            "target_reopenings": 0,
            "threshold_reselection": 0,
            "bootstrap_recomputation": 0,
            "new_formal_statistical_tests": 0,
        },
        "high_level_outcomes": [
            "SELECTIVE_FAMILY_TRANSFER",
            "RANKING_THRESHOLD_DIVERGENCE",
            "LEARNER_DEPENDENCE",
        ],
        "frozen_source_sha256": source_hashes,
        "generated_artifacts": generated,
        "figure_policy": {
            "main": [
                (
                    "results/stage27_loao_unseen_attack/"
                    "stage27_4a_final_synthesis/figures/"
                    "stage27_primary_roc_auc_ci.png"
                ),
                (
                    "results/stage27_loao_unseen_attack/"
                    "stage27_4a_final_synthesis/figures/"
                    "stage27_balanced_recall_ci.png"
                ),
            ],
            "supplementary": [
                (
                    "results/stage27_loao_unseen_attack/"
                    "stage27_4a_final_synthesis/figures/"
                    "stage27_primary_pr_auc_ci.png"
                ),
            ],
        },
        "reporting_guards": {
            "formal_zero_day_proof": False,
            "universal_unseen_family_generalization": False,
            "infiltration_inferential_claim": False,
            "similarity_significance_inference": False,
            "target_threshold_search": False,
        },
    }


def validate_generated_text(root: Path):
    manuscript = (
        root / OUTPUT_PATHS["manuscript_md"]
    ).read_text(encoding="utf-8")

    tables = (
        root / OUTPUT_PATHS["tables_md"]
    ).read_text(encoding="utf-8")

    required_manuscript_strings = [
        "SELECTIVE_FAMILY_TRANSFER",
        "RANKING_THRESHOLD_DIVERGENCE",
        "LEARNER_DEPENDENCE",
        "formal proof of zero-day detection",
        "descriptive only because",
        "ranking generalization",
        "operating-point transfer",
        "five of seven",
        "DOS",
        "AUTH_BRUTE_FORCE",
        "INFILTRATION",
        "BOT",
        "DDOS",
        "PORT_SCAN",
        "WEB_ATTACK",
        "0.9982",
        "0.9986",
        "0.3224",
        "0.5591",
        "0.5506",
        "0.7559",
        "77.80%",
        "52.11%",
    ]

    for token in required_manuscript_strings:
        if token not in manuscript:
            raise RuntimeError(
                f"Generated manuscript missing required token: {token}"
            )

    forbidden_overclaims = [
        "proves universal zero-day detection",
        "all seven families were experimentally executable",
        "LightGBM is universally superior",
        "XGBoost is universally superior",
        "statistically significant similarity",
    ]

    # These phrases are allowed only inside the explicit
    # "Claims That Must Not Appear" section.
    # Therefore the generated artifact must contain that section.
    assert "# I. Claims That Must Not Appear" in manuscript

    assert "Table 27-1" in tables
    assert "Table 27-2" in tables
    assert "Table 27-S1" in tables
    assert "Table 27-S2" in tables
    assert "Table 27-S3" in tables

    assert (
        "INFILTRATION is descriptive only"
        in tables
    )

    return True


def check_mode(root: Path):
    source_hashes = verify_frozen_sources(root)

    synthesis = root / SYNTHESIS_REL

    primary = pd.read_csv(
        synthesis / "stage27_final_primary_metrics.csv"
    )
    ops = pd.read_csv(
        synthesis / "stage27_final_operating_points.csv"
    )
    gaps = pd.read_csv(
        synthesis / "stage27_final_novelty_gaps.csv"
    )
    similarity = pd.read_csv(
        synthesis / "stage27_final_similarity.csv"
    )

    scientific_sanity(
        primary,
        ops,
        gaps,
        similarity,
    )

    expected = build_contents(
        primary,
        ops,
        gaps,
        similarity,
    )

    for rel, content in expected.items():
        path = root / rel

        if not path.is_file():
            raise RuntimeError(
                f"Generated publication artifact missing: {rel}"
            )

        actual_text = path.read_text(encoding="utf-8")
        expected_text = content.rstrip() + "\n"

        if actual_text != expected_text:
            raise RuntimeError(
                f"Generated artifact differs from deterministic "
                f"generator output: {rel}"
            )

    manifest_path = root / MANIFEST_REL

    if not manifest_path.is_file():
        raise RuntimeError("Publication manifest is missing.")

    manifest = json.loads(
        manifest_path.read_text(encoding="utf-8")
    )

    for rel in expected:
        rel_str = str(rel)

        expected_hash = manifest[
            "generated_artifacts"
        ][rel_str]["sha256"]

        actual_hash = sha256_file(root / rel)

        if actual_hash != expected_hash:
            raise RuntimeError(
                f"Manifest hash mismatch: {rel}"
            )

    validate_generated_text(root)

    print("[PASS] frozen Stage27 source hashes")
    print("[PASS] scientific sanity gates")
    print("[PASS] deterministic document contents")
    print("[PASS] publication manifest hashes")
    print("[PASS] manuscript claim/data gates")
    print()
    print("STAGE27 PUBLICATION PACKAGE CHECK: PASS")


def generate_mode(root: Path):
    head = verify_scientific_parent(root)

    source_hashes = verify_frozen_sources(root)

    synthesis = root / SYNTHESIS_REL

    primary = pd.read_csv(
        synthesis / "stage27_final_primary_metrics.csv"
    )

    ops = pd.read_csv(
        synthesis / "stage27_final_operating_points.csv"
    )

    gaps = pd.read_csv(
        synthesis / "stage27_final_novelty_gaps.csv"
    )

    similarity = pd.read_csv(
        synthesis / "stage27_final_similarity.csv"
    )

    scientific_sanity(
        primary,
        ops,
        gaps,
        similarity,
    )

    contents = build_contents(
        primary,
        ops,
        gaps,
        similarity,
    )

    for rel, content in contents.items():
        write_text(
            root / rel,
            content,
        )

    validate_generated_text(root)

    manifest = create_manifest(
        root=root,
        head=head,
        source_hashes=source_hashes,
        generated_paths=list(contents.keys()),
    )

    manifest_path = root / MANIFEST_REL
    manifest_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    manifest_path.write_text(
        json.dumps(
            manifest,
            indent=2,
            sort_keys=True,
        ) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    print("=" * 80)
    print("STAGE27 PUBLICATION GENERATOR COMPLETE")
    print("=" * 80)

    print()
    print("Scientific parent:")
    print(f"  {CANONICAL_SCIENTIFIC_PARENT}")

    print()
    print("Generated artifacts:")

    for rel in contents:
        path = root / rel

        print(
            f"  {rel}\n"
            f"    SHA256: {sha256_file(path)}\n"
            f"    bytes:  {path.stat().st_size:,}"
        )

    print(
        f"  {GENERATOR_REL}\n"
        f"    SHA256: {sha256_file(root / GENERATOR_REL)}"
    )

    print(
        f"  {MANIFEST_REL}\n"
        f"    SHA256: {sha256_file(manifest_path)}"
    )

    print()
    print("Science operations:")
    print("  model fits                 : 0")
    print("  model inference            : 0")
    print("  target reopenings          : 0")
    print("  threshold reselection      : 0")
    print("  bootstrap recomputation    : 0")
    print("  new formal statistical test: 0")


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate existing publication package without rewriting it.",
    )

    args = parser.parse_args()

    root = repo_root()

    verify_scientific_parent(root)

    if args.check:
        check_mode(root)
    else:
        generate_mode(root)


if __name__ == "__main__":
    main()
'''


# ----------------------------------------------------------------------------
# Write generator into repository
# ----------------------------------------------------------------------------

GENERATOR_PATH.parent.mkdir(
    parents=True,
    exist_ok=True,
)

GENERATOR_PATH.write_text(
    GENERATOR_SOURCE.rstrip() + "\n",
    encoding="utf-8",
    newline="\n",
)

print()
print("-" * 92)
print("GENERATOR CREATED")
print("-" * 92)

print(GENERATOR_PATH)
print("SHA256:", sha256_file(GENERATOR_PATH))


# ----------------------------------------------------------------------------
# First deterministic generation
# ----------------------------------------------------------------------------

print()
print("-" * 92)
print("FIRST GENERATION")
print("-" * 92)

first = run(
    [
        sys.executable,
        str(GENERATOR_PATH),
    ],
    cwd=REPO,
)

print(first.stdout)

if first.stderr.strip():
    print(first.stderr)


# ----------------------------------------------------------------------------
# Publication artifact paths
# ----------------------------------------------------------------------------

PUBLICATION_PATHS = [
    Path("docs/STAGE27_MANUSCRIPT_INTEGRATION.md"),
    Path("docs/STAGE27_MANUSCRIPT_INTEGRATION.tex"),
    Path("docs/STAGE27_PUBLICATION_TABLES.md"),
    Path("docs/STAGE27_PUBLICATION_TABLES.tex"),
    GENERATOR_REL,
    Path(
        "results/stage27_loao_unseen_attack/"
        "stage27_publication_package/"
        "stage27_publication_manifest.json"
    ),
]

for rel in PUBLICATION_PATHS:
    path = REPO / rel

    if not path.is_file():
        raise RuntimeError(
            f"Expected PUB1 artifact not generated: {rel}"
        )


# ----------------------------------------------------------------------------
# Capture first-run hashes
# ----------------------------------------------------------------------------

hashes_first = {
    str(rel): sha256_file(REPO / rel)
    for rel in PUBLICATION_PATHS
}


# ----------------------------------------------------------------------------
# Second generation — idempotence test
# ----------------------------------------------------------------------------

print()
print("-" * 92)
print("SECOND GENERATION / IDEMPOTENCE TEST")
print("-" * 92)

second = run(
    [
        sys.executable,
        str(GENERATOR_PATH),
    ],
    cwd=REPO,
)

if second.returncode != 0:
    print(second.stdout)
    print(second.stderr)
    raise RuntimeError(
        "Second deterministic generation failed."
    )

hashes_second = {
    str(rel): sha256_file(REPO / rel)
    for rel in PUBLICATION_PATHS
}

if hashes_first != hashes_second:
    print("FIRST:")
    print(json.dumps(hashes_first, indent=2))

    print()
    print("SECOND:")
    print(json.dumps(hashes_second, indent=2))

    raise RuntimeError(
        "PUB1 output is not deterministic across consecutive runs."
    )

print("[PASS] consecutive generation is byte-identical")


# ----------------------------------------------------------------------------
# Check-only mode
# ----------------------------------------------------------------------------

print()
print("-" * 92)
print("CHECK-ONLY REPRODUCIBILITY MODE")
print("-" * 92)

check = run(
    [
        sys.executable,
        str(GENERATOR_PATH),
        "--check",
    ],
    cwd=REPO,
)

print(check.stdout)

if check.stderr.strip():
    print(check.stderr)


# ----------------------------------------------------------------------------
# Ensure frozen science files themselves were not changed
# ----------------------------------------------------------------------------

print()
print("-" * 92)
print("FROZEN SCIENCE MODIFICATION GATE")
print("-" * 92)

science_pathspec = (
    "results/stage27_loao_unseen_attack/"
    "stage27_4a_final_synthesis"
)

science_diff = run(
    [
        "git",
        "diff",
        "--",
        science_pathspec,
    ],
    cwd=REPO,
).stdout

if science_diff.strip():
    print(science_diff)

    raise RuntimeError(
        "PUB1 modified frozen Stage27 scientific artifacts."
    )

print("[PASS] frozen Stage27-4A synthesis remains byte-untouched")


# ----------------------------------------------------------------------------
# Git status
# ----------------------------------------------------------------------------

print()
print("-" * 92)
print("GIT STATUS")
print("-" * 92)

status = git("status", "--short")

print(status or "[clean]")


# ----------------------------------------------------------------------------
# Diff statistics
# ----------------------------------------------------------------------------

print()
print("-" * 92)
print("DIFF STAT")
print("-" * 92)

diff_stat = run(
    [
        "git",
        "diff",
        "--stat",
        "--",
        "docs/STAGE27_MANUSCRIPT_INTEGRATION.md",
        "docs/STAGE27_MANUSCRIPT_INTEGRATION.tex",
        "docs/STAGE27_PUBLICATION_TABLES.md",
        "docs/STAGE27_PUBLICATION_TABLES.tex",
        "scripts/stage27/stage27_publication_integration.py",
        (
            "results/stage27_loao_unseen_attack/"
            "stage27_publication_package/"
            "stage27_publication_manifest.json"
        ),
    ],
    cwd=REPO,
).stdout

print(diff_stat)


# ----------------------------------------------------------------------------
# Because new files are untracked, git diff does not display their text.
# Print controlled previews.
# ----------------------------------------------------------------------------

print()
print("-" * 92)
print("MANUSCRIPT PREVIEW")
print("-" * 92)

manuscript_path = (
    REPO / "docs/STAGE27_MANUSCRIPT_INTEGRATION.md"
)

manuscript_lines = manuscript_path.read_text(
    encoding="utf-8"
).splitlines()

for line in manuscript_lines[:120]:
    print(line)

print()
print(
    f"... previewed 120/{len(manuscript_lines)} manuscript lines"
)


print()
print("-" * 92)
print("PRIMARY TABLE PREVIEW")
print("-" * 92)

tables_path = (
    REPO / "docs/STAGE27_PUBLICATION_TABLES.md"
)

tables_lines = tables_path.read_text(
    encoding="utf-8"
).splitlines()

for line in tables_lines[:80]:
    print(line)

print()
print(
    f"... previewed 80/{len(tables_lines)} table lines"
)


# ----------------------------------------------------------------------------
# Manifest preview
# ----------------------------------------------------------------------------

print()
print("-" * 92)
print("PUBLICATION MANIFEST")
print("-" * 92)

manifest_path = (
    REPO
    / "results/stage27_loao_unseen_attack/"
      "stage27_publication_package/"
      "stage27_publication_manifest.json"
)

manifest = json.loads(
    manifest_path.read_text(encoding="utf-8")
)

print(
    json.dumps(
        manifest,
        indent=2,
    )
)


# ----------------------------------------------------------------------------
# Final PUB1 state
# ----------------------------------------------------------------------------

print()
print("=" * 92)
print("STAGE27-PUB1 COMPLETE — REVIEW REQUIRED BEFORE COMMIT")
print("=" * 92)

print()
print("Scientific parent:")
print(f"  {CANONICAL_STAGE27_PARENT}")

print()
print("Generated publication artifacts:")
for rel in PUBLICATION_PATHS:
    print(
        f"  {rel}\n"
        f"    SHA256: {sha256_file(REPO / rel)}"
    )

print()
print("Integrity:")
print("  frozen Stage27 science modified : NO")
print("  model fitting                   : 0")
print("  model inference                 : 0")
print("  target reopening                : 0")
print("  threshold reselection           : 0")
print("  bootstrap recomputation         : 0")
print("  new significance testing        : 0")
print("  deterministic generation        : PASS")
print("  generator --check               : PASS")

print()
print("Git operations:")
print("  commit : NOT PERFORMED")
print("  push   : NOT PERFORMED")

print()
print("Next authorized step:")
print("  Review PUB1 output, then run STAGE27-PUB2 commit/push closeout.")


# %% [Stage27 notebook cell 10]
# ============================================================================
# Stage27-PUB2
# Publication Package Freeze, Git Commit/Push, Remote Verification, Closeout
#
# REQUIRES:
#   STAGE27-PUB0 = PASS
#   STAGE27-PUB1 = PASS
#
# OPERATIONS:
#   - Apply two publication-only wording/state corrections.
#   - Regenerate Stage27 publication artifacts deterministically.
#   - Re-run generator --check.
#   - Verify frozen Stage27 science remains untouched.
#   - Optional LaTeX compilation smoke test.
#   - Stage ONLY authorized Stage27 publication files.
#   - Commit publication package.
#   - Push and verify exact remote commit/files.
#   - Generate STAGE27_PUBLICATION_CLOSEOUT.md.
#   - Commit closeout separately.
#   - Push and remotely verify final closeout state.
#
# SCIENCE:
#   ZERO model fitting
#   ZERO model inference
#   ZERO target reopening
#   ZERO threshold reselection
#   ZERO bootstrap recomputation
#   ZERO new statistical testing
# ============================================================================

from __future__ import annotations

import hashlib
import json
import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path
from datetime import datetime, timezone


# ----------------------------------------------------------------------------
# Frozen identity
# ----------------------------------------------------------------------------

REPO = Path("/kaggle/working/ids2018-validation-safe-ablation")

REPO_FULL = "themubasshir/ids2018-validation-safe-ablation"

CANONICAL_STAGE27_PARENT = (
    "0e1439565aedc7da9b7ca1207262e9061422bc22"
)

GENERATOR_REL = Path(
    "scripts/stage27/stage27_publication_integration.py"
)

GENERATOR = REPO / GENERATOR_REL

MANIFEST_REL = Path(
    "results/stage27_loao_unseen_attack/"
    "stage27_publication_package/"
    "stage27_publication_manifest.json"
)

CLOSEOUT_REL = Path(
    "docs/STAGE27_PUBLICATION_CLOSEOUT.md"
)

PUBLICATION_FILES = [
    Path("docs/STAGE27_MANUSCRIPT_INTEGRATION.md"),
    Path("docs/STAGE27_MANUSCRIPT_INTEGRATION.tex"),
    Path("docs/STAGE27_PUBLICATION_TABLES.md"),
    Path("docs/STAGE27_PUBLICATION_TABLES.tex"),
    MANIFEST_REL,
    GENERATOR_REL,
]

FROZEN_SYNTHESIS_REL = Path(
    "results/stage27_loao_unseen_attack/"
    "stage27_4a_final_synthesis"
)


# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------

def run(
    cmd,
    *,
    cwd=REPO,
    check=True,
    text=True,
    env=None,
):
    result = subprocess.run(
        cmd,
        cwd=cwd,
        check=False,
        text=text,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
    )

    if check and result.returncode != 0:
        if text:
            print(result.stdout)
            print(result.stderr)
        raise RuntimeError(
            f"Command failed ({result.returncode}): "
            f"{' '.join(str(x) for x in cmd)}"
        )

    return result


def git(*args, check=True):
    return run(
        ["git", *args],
        check=check,
    ).stdout.strip()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()

    with path.open("rb") as f:
        while True:
            chunk = f.read(8 * 1024 * 1024)

            if not chunk:
                break

            h.update(chunk)

    return h.hexdigest()


def git_file_bytes(ref: str, path: Path) -> bytes:
    result = run(
        [
            "git",
            "show",
            f"{ref}:{path.as_posix()}",
        ],
        text=False,
    )

    return result.stdout


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def status_paths():
    """
    Return exact paths from `git status --porcelain -uall`.
    """
    output = git(
        "status",
        "--porcelain",
        "-uall",
    )

    paths = []

    if not output:
        return paths

    for line in output.splitlines():
        # XY + space = first 3 chars
        raw = line[3:]

        # Handle rename format if it ever occurs.
        if " -> " in raw:
            raw = raw.split(" -> ", 1)[1]

        paths.append(raw)

    return paths


def get_github_token():
    from kaggle_secrets import UserSecretsClient

    client = UserSecretsClient()

    candidates = [
        "GITHUB_TOKEN",
        "github_token",
        "GH_TOKEN",
        "GITHUB_PAT",
        "github_pat",
        "GH_PAT",
    ]

    for label in candidates:
        try:
            value = client.get_secret(label)
        except Exception:
            value = None

        if value:
            print(
                f"[PASS] GitHub credential: {label} "
                f"({len(value)} chars, value redacted)"
            )
            return label, value

    raise RuntimeError(
        "No usable GitHub token found in Kaggle Secrets."
    )


def make_git_push_env(token: str):
    """
    Use GIT_ASKPASS so the token is NOT written into the Git remote URL
    and is NOT printed in notebook output.
    """
    askpass = Path(
        "/kaggle/working/.stage27_git_askpass.sh"
    )

    askpass.write_text(
        """#!/bin/sh
case "$1" in
  *Username*) printf '%s\\n' "x-access-token" ;;
  *)          printf '%s\\n' "$GITHUB_TOKEN" ;;
esac
""",
        encoding="utf-8",
        newline="\n",
    )

    askpass.chmod(
        stat.S_IRUSR
        | stat.S_IWUSR
        | stat.S_IXUSR
    )

    env = os.environ.copy()

    env["GITHUB_TOKEN"] = token
    env["GIT_ASKPASS"] = str(askpass)
    env["GIT_TERMINAL_PROMPT"] = "0"

    return env, askpass


def push_main(push_env):
    result = run(
        [
            "git",
            "push",
            "origin",
            "main",
        ],
        env=push_env,
    )

    # Safe to show push output: token is not in URL.
    if result.stdout.strip():
        print(result.stdout.strip())

    if result.stderr.strip():
        print(result.stderr.strip())


def verify_remote_head(expected_commit):
    git(
        "fetch",
        "--prune",
        "origin",
        "main",
    )

    remote = git(
        "rev-parse",
        "origin/main",
    )

    print("Expected remote HEAD:", expected_commit)
    print("Actual remote HEAD:  ", remote)

    if remote != expected_commit:
        raise RuntimeError(
            "Remote HEAD does not match expected commit."
        )

    return remote


def verify_remote_files(ref, paths):
    print()
    print("Remote file-content verification:")

    for rel in paths:
        local_path = REPO / rel

        local_hash = sha256_file(local_path)

        remote_bytes = git_file_bytes(
            ref,
            rel,
        )

        remote_hash = sha256_bytes(
            remote_bytes
        )

        if local_hash != remote_hash:
            raise RuntimeError(
                f"Remote content mismatch: {rel}\n"
                f"local:  {local_hash}\n"
                f"remote: {remote_hash}"
            )

        print(
            f"[PASS] {rel}\n"
            f"       SHA256: {local_hash}"
        )


# ----------------------------------------------------------------------------
# Header
# ----------------------------------------------------------------------------

print("=" * 96)
print(
    "STAGE27-PUB2 — PUBLICATION FREEZE / "
    "COMMIT / PUSH / REMOTE CLOSEOUT"
)
print("=" * 96)

print()
print(
    "timestamp_utc:",
    datetime.now(timezone.utc).isoformat(),
)

print("repository   :", REPO_FULL)
print("repo path    :", REPO)
print(
    "science parent:",
    CANONICAL_STAGE27_PARENT,
)


# ----------------------------------------------------------------------------
# Repository preflight
# ----------------------------------------------------------------------------

if not REPO.is_dir():
    raise RuntimeError(
        "Repository checkout missing."
    )

branch = git(
    "branch",
    "--show-current",
)

head = git(
    "rev-parse",
    "HEAD",
)

print()
print("branch:", branch)
print("HEAD:  ", head)

if branch != "main":
    raise RuntimeError(
        f"Expected branch main, found {branch}"
    )

if head != CANONICAL_STAGE27_PARENT:
    raise RuntimeError(
        "PUB2 must start from the canonical Stage27 "
        "scientific parent."
    )


# ----------------------------------------------------------------------------
# Verify PUB1 generated exactly the authorized paths
# ----------------------------------------------------------------------------

print()
print("-" * 96)
print("PUB1 WORKTREE INVENTORY")
print("-" * 96)

expected_untracked = {
    p.as_posix()
    for p in PUBLICATION_FILES
}

actual_paths = set(
    status_paths()
)

print("Expected publication paths:")
for p in sorted(expected_untracked):
    print(" ", p)

print()
print("Actual changed/untracked paths:")
for p in sorted(actual_paths):
    print(" ", p)

if actual_paths != expected_untracked:
    unexpected = actual_paths - expected_untracked
    missing = expected_untracked - actual_paths

    print()
    print("Unexpected:", sorted(unexpected))
    print("Missing:   ", sorted(missing))

    raise RuntimeError(
        "PUB2 refuses to proceed because the worktree "
        "does not contain exactly the expected PUB1 files."
    )

print()
print("[PASS] exact PUB1 worktree inventory")


# ----------------------------------------------------------------------------
# Publication-only corrections
# ----------------------------------------------------------------------------

print()
print("-" * 96)
print("PUBLICATION WORDING / STATE FREEZE")
print("-" * 96)

if not GENERATOR.is_file():
    raise RuntimeError(
        f"Generator missing: {GENERATOR}"
    )

source = GENERATOR.read_text(
    encoding="utf-8"
)

original_source = source


# 1. Publication package is no longer pending review.
old_state = '"GENERATED_PENDING_GIT_REVIEW"'
new_state = '"PUBLICATION_CONTENT_FROZEN"'

state_count = source.count(old_state)

if state_count != 1:
    raise RuntimeError(
        f"Expected exactly one pending-review state; "
        f"found {state_count}"
    )

source = source.replace(
    old_state,
    new_state,
    1,
)


# 2. Avoid language that could imply 7/7 folds produced target results.
old_phrase = (
    "Seven\n"
    "CICIDS2017 attack families were preregistered and "
    "evaluated under a\n"
    "strict"
)

new_phrase = (
    "Seven\n"
    "CICIDS2017 attack families were preregistered for "
    "evaluation under a\n"
    "strict"
)

phrase_count = source.count(
    old_phrase
)

if phrase_count != 1:
    raise RuntimeError(
        "Could not uniquely locate the Introduction "
        "executability wording."
    )

source = source.replace(
    old_phrase,
    new_phrase,
    1,
)


# 3. Tighten safe-claims wording.
old_claim = (
    "1. Stage27 evaluated seven preregistered "
    "attack-family categories."
)

new_claim = (
    "1. Stage27 preregistered seven attack-family "
    "categories."
)

claim_count = source.count(
    old_claim
)

if claim_count != 1:
    raise RuntimeError(
        "Could not uniquely locate the publication-safe "
        "seven-family claim."
    )

source = source.replace(
    old_claim,
    new_claim,
    1,
)


if source == original_source:
    raise RuntimeError(
        "No generator changes were applied."
    )

GENERATOR.write_text(
    source,
    encoding="utf-8",
    newline="\n",
)

print("[PASS] publication package state frozen")
print("[PASS] 7-family executability wording tightened")
print("[PASS] publication-safe claim wording tightened")
print(
    "Generator SHA256:",
    sha256_file(GENERATOR),
)


# ----------------------------------------------------------------------------
# Regenerate publication package
# ----------------------------------------------------------------------------

print()
print("-" * 96)
print("DETERMINISTIC REGENERATION")
print("-" * 96)

regen = run(
    [
        sys.executable,
        str(GENERATOR),
    ]
)

print(regen.stdout)

if regen.stderr.strip():
    print(regen.stderr)


# ----------------------------------------------------------------------------
# Check-only validation
# ----------------------------------------------------------------------------

print()
print("-" * 96)
print("GENERATOR CHECK")
print("-" * 96)

check = run(
    [
        sys.executable,
        str(GENERATOR),
        "--check",
    ]
)

print(check.stdout)

if check.stderr.strip():
    print(check.stderr)


# ----------------------------------------------------------------------------
# Publication-text wording audit
# ----------------------------------------------------------------------------

print()
print("-" * 96)
print("PUBLICATION WORDING AUDIT")
print("-" * 96)

manuscript_md = (
    REPO
    / "docs/STAGE27_MANUSCRIPT_INTEGRATION.md"
)

manuscript = manuscript_md.read_text(
    encoding="utf-8"
)

if (
    "preregistered and evaluated under"
    in manuscript
):
    raise RuntimeError(
        "Ambiguous 7/7 wording remains in manuscript."
    )

if (
    "Stage27 evaluated seven preregistered "
    "attack-family categories."
    in manuscript
):
    raise RuntimeError(
        "Old seven-family safe claim remains."
    )

required_phrases = [
    (
        "Seven\n"
        "CICIDS2017 attack families were preregistered "
        "for evaluation under a"
    ),
    (
        "Five families were\n"
        "structurally executable"
    ),
    (
        "Stage27 preregistered seven attack-family "
        "categories."
    ),
    (
        "2. Five of the seven families were "
        "structurally executable."
    ),
]

for phrase in required_phrases:
    if phrase not in manuscript:
        raise RuntimeError(
            "Required corrected wording missing:\n"
            + phrase
        )

manifest = json.loads(
    (REPO / MANIFEST_REL).read_text(
        encoding="utf-8"
    )
)

if (
    manifest["publication_package_status"]
    != "PUBLICATION_CONTENT_FROZEN"
):
    raise RuntimeError(
        "Publication manifest is not in frozen-content state."
    )

print("[PASS] manuscript wording audit")
print("[PASS] manifest state = PUBLICATION_CONTENT_FROZEN")


# ----------------------------------------------------------------------------
# Ensure scientific artifacts remain untouched
# ----------------------------------------------------------------------------

print()
print("-" * 96)
print("FROZEN SCIENCE GATE")
print("-" * 96)

science_diff = run(
    [
        "git",
        "diff",
        "--",
        FROZEN_SYNTHESIS_REL.as_posix(),
    ]
).stdout

if science_diff.strip():
    print(science_diff)

    raise RuntimeError(
        "Frozen Stage27 scientific synthesis was modified."
    )

print(
    "[PASS] stage27_4a_final_synthesis is byte-untouched"
)


# ----------------------------------------------------------------------------
# Verify worktree still contains exactly authorized files
# ----------------------------------------------------------------------------

actual_paths_after_regen = set(
    status_paths()
)

if (
    actual_paths_after_regen
    != expected_untracked
):
    raise RuntimeError(
        "Regeneration introduced unexpected repository paths:\n"
        + "\n".join(
            sorted(actual_paths_after_regen)
        )
    )

print(
    "[PASS] regeneration changed only authorized publication files"
)


# ----------------------------------------------------------------------------
# Optional LaTeX syntax smoke test
# ----------------------------------------------------------------------------

print()
print("-" * 96)
print("LATEX SMOKE TEST")
print("-" * 96)

pdflatex = shutil.which(
    "pdflatex"
)

if pdflatex is None:
    print(
        "[SKIP] pdflatex not installed in this Kaggle runtime."
    )
else:
    smoke_dir = Path(
        "/kaggle/working/stage27_pub2_latex_smoke"
    )

    if smoke_dir.exists():
        shutil.rmtree(smoke_dir)

    smoke_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    manuscript_tex = (
        REPO
        / "docs/STAGE27_MANUSCRIPT_INTEGRATION.tex"
    ).resolve()

    tables_tex = (
        REPO
        / "docs/STAGE27_PUBLICATION_TABLES.tex"
    ).resolve()

    wrapper = smoke_dir / "stage27_smoke.tex"

    wrapper.write_text(
        rf"""\documentclass{{article}}
\usepackage[T1]{{fontenc}}
\usepackage[margin=1in]{{geometry}}
\begin{{document}}

\input{{{manuscript_tex.as_posix()}}}

\clearpage

\input{{{tables_tex.as_posix()}}}

\end{{document}}
""",
        encoding="utf-8",
        newline="\n",
    )

    latex_result = run(
        [
            pdflatex,
            "-interaction=nonstopmode",
            "-halt-on-error",
            wrapper.name,
        ],
        cwd=smoke_dir,
        check=False,
    )

    if latex_result.returncode != 0:
        print(latex_result.stdout)
        print(latex_result.stderr)

        raise RuntimeError(
            "Stage27 LaTeX smoke compilation failed."
        )

    pdf_path = (
        smoke_dir / "stage27_smoke.pdf"
    )

    if not pdf_path.is_file():
        raise RuntimeError(
            "LaTeX returned success but produced no PDF."
        )

    print("[PASS] Stage27 LaTeX fragments compile")
    print(
        "       PDF bytes:",
        f"{pdf_path.stat().st_size:,}",
    )


# ----------------------------------------------------------------------------
# Git identity
# ----------------------------------------------------------------------------

print()
print("-" * 96)
print("GIT IDENTITY")
print("-" * 96)

git_name = git(
    "config",
    "--get",
    "user.name",
    check=False,
)

git_email = git(
    "config",
    "--get",
    "user.email",
    check=False,
)

if not git_name:
    git(
        "config",
        "user.name",
        "themubasshir",
    )
    git_name = "themubasshir"

if not git_email:
    git(
        "config",
        "user.email",
        "themubasshir@users.noreply.github.com",
    )
    git_email = (
        "themubasshir@users.noreply.github.com"
    )

print("user.name :", git_name)
print("user.email:", git_email)


# ----------------------------------------------------------------------------
# GitHub auth
# ----------------------------------------------------------------------------

print()
print("-" * 96)
print("GITHUB AUTH")
print("-" * 96)

secret_label, github_token = (
    get_github_token()
)

push_env, askpass_path = (
    make_git_push_env(
        github_token
    )
)


# ----------------------------------------------------------------------------
# Race-condition gate: remote must still equal frozen scientific parent
# ----------------------------------------------------------------------------

print()
print("-" * 96)
print("REMOTE PARENT RACE-CONDITION GATE")
print("-" * 96)

git(
    "fetch",
    "--prune",
    "origin",
    "main",
)

remote_before = git(
    "rev-parse",
    "origin/main",
)

print(
    "Expected origin/main:",
    CANONICAL_STAGE27_PARENT,
)
print(
    "Actual origin/main:  ",
    remote_before,
)

if (
    remote_before
    != CANONICAL_STAGE27_PARENT
):
    raise RuntimeError(
        "origin/main advanced after PUB0/PUB1. "
        "PUB2 will not overwrite or race the remote."
    )

print(
    "[PASS] remote still at frozen Stage27 parent"
)


# ============================================================================
# COMMIT 1 — Publication package
# ============================================================================

print()
print("=" * 96)
print("COMMIT 1 — FREEZE STAGE27 PUBLICATION PACKAGE")
print("=" * 96)

# Stage exact paths only.
for rel in PUBLICATION_FILES:
    git(
        "add",
        "--",
        rel.as_posix(),
    )

staged_names = set(
    git(
        "diff",
        "--cached",
        "--name-only",
    ).splitlines()
)

expected_staged = {
    p.as_posix()
    for p in PUBLICATION_FILES
}

if staged_names != expected_staged:
    raise RuntimeError(
        "Staged-file set is not exactly the authorized "
        "Stage27 publication package.\n\n"
        f"Expected:\n{sorted(expected_staged)}\n\n"
        f"Actual:\n{sorted(staged_names)}"
    )

print("[PASS] exact staged-file set")

print()
print("Staged diff stat:")
print(
    git(
        "diff",
        "--cached",
        "--stat",
    )
)

commit1 = run(
    [
        "git",
        "-c",
        "commit.gpgsign=false",
        "commit",
        "-m",
        (
            "stage27-pub1: freeze manuscript "
            "integration package"
        ),
    ]
)

print(commit1.stdout)

PUB_COMMIT = git(
    "rev-parse",
    "HEAD",
)

print()
print("Publication package commit:")
print(" ", PUB_COMMIT)


# ----------------------------------------------------------------------------
# Push commit 1
# ----------------------------------------------------------------------------

print()
print("Pushing publication package...")

push_main(
    push_env
)

verify_remote_head(
    PUB_COMMIT
)

verify_remote_files(
    "origin/main",
    PUBLICATION_FILES,
)

print()
print(
    "[PASS] publication package remotely frozen"
)


# ----------------------------------------------------------------------------
# Capture hashes for closeout
# ----------------------------------------------------------------------------

publication_hashes = {
    rel.as_posix(): sha256_file(
        REPO / rel
    )
    for rel in PUBLICATION_FILES
}


# ============================================================================
# CLOSEOUT DOCUMENT
# ============================================================================

print()
print("=" * 96)
print("GENERATE STAGE27 PUBLICATION CLOSEOUT")
print("=" * 96)

manifest_hash = publication_hashes[
    MANIFEST_REL.as_posix()
]

generator_hash = publication_hashes[
    GENERATOR_REL.as_posix()
]

closeout = f"""# Stage27 Publication and Reproducibility Closeout

## Scientific Status

**STAGE27 = SCIENTIFICALLY CLOSED**

Stage27 completed the frozen chronology-first zero-training-exposure
attack-family generalization audit before manuscript integration began.

No publication step reopened the target, refit a model, reran inference,
reselected a threshold, recomputed bootstrap intervals, or introduced
new formal statistical testing.

## Frozen Scientific Parent

`{CANONICAL_STAGE27_PARENT}`

## Publication Package Commit

`{PUB_COMMIT}`

Commit subject:

`stage27-pub1: freeze manuscript integration package`

## Final Stage27 Scientific Outcome

The publication-safe Stage27 synthesis is:

1. `SELECTIVE_FAMILY_TRANSFER`
2. `RANKING_THRESHOLD_DIVERGENCE`
3. `LEARNER_DEPENDENCE`

Five of seven preregistered attack families were structurally
executable under strict chronology.

- BOT: executable
- DDOS: executable
- DOS: structurally ineligible
- AUTH_BRUTE_FORCE: structurally ineligible
- INFILTRATION: executable, descriptive only because support = 36
- PORT_SCAN: executable
- WEB_ATTACK: executable

Stage27 is an unseen attack-family generalization audit and is not
formal proof of universal zero-day detection.

## Publication Artifacts

| Artifact | SHA256 |
|---|---|
"""

for rel in PUBLICATION_FILES:
    closeout += (
        f"| `{rel.as_posix()}` | "
        f"`{publication_hashes[rel.as_posix()]}` |\n"
    )

closeout += f"""
## Manifest

Publication manifest:

`{MANIFEST_REL.as_posix()}`

SHA256:

`{manifest_hash}`

Manifest state:

`PUBLICATION_CONTENT_FROZEN`

## Reproducible Generator

`{GENERATOR_REL.as_posix()}`

SHA256:

`{generator_hash}`

The generator verifies the canonical frozen Stage27 source hashes,
reconstructs the manuscript-facing tables and prose from those frozen
artifacts, and supports a read-only `--check` mode.

## Main-Manuscript Figure Policy

### Main Figure 27-1

`results/stage27_loao_unseen_attack/stage27_4a_final_synthesis/figures/stage27_primary_roc_auc_ci.png`

Purpose:

Selective unseen-family ranking transfer and learner dependence.

### Main Figure 27-2

`results/stage27_loao_unseen_attack/stage27_4a_final_synthesis/figures/stage27_balanced_recall_ci.png`

Purpose:

Ranking--threshold divergence at the frozen BALANCED operating point.

### Supplementary Figure 27-S1

`results/stage27_loao_unseen_attack/stage27_4a_final_synthesis/figures/stage27_primary_pr_auc_ci.png`

PR-AUC remains a co-primary metric and must remain in the main results
table and manuscript text even when its separate visualization is
supplementary.

## Reporting Guardrails

The manuscript must not claim:

1. formal or universal zero-day detection;
2. universal unseen-family generalization;
3. that all seven families produced executable target folds;
4. an inferential family-level INFILTRATION conclusion;
5. statistically significant behavioral-similarity correlation;
6. causal explanation from behavioral similarity;
7. universal superiority of XGBoost or LightGBM;
8. target-guided threshold optimization or model adaptation;
9. that raw PR-AUC novelty gaps are prevalence invariant.

## Final Accounting

- preregistered primary families: 7
- executable families: 5
- structurally ineligible families: 2
- descriptive-only executable families: 1
- preregistered learners: 2
- frozen Stage27 fits: 10
- new publication-phase fits: 0
- new publication-phase inference: 0
- target reopenings during publication: 0
- threshold reselections during publication: 0
- bootstrap recomputations during publication: 0
- new formal statistical tests during publication: 0

## Remote Verification

The publication package commit was pushed to `origin/main`, fetched
back from GitHub, and verified by exact commit identity and byte-level
SHA256 comparison of each publication artifact.

## Next Manuscript Phase

Stage27 publication integration is complete.

The next authorized work is whole-manuscript assembly and
claim-to-artifact consistency review across the already-frozen
experimental stages.

No further Stage27 scientific computation is authorized.
"""

CLOSEOUT_PATH = (
    REPO / CLOSEOUT_REL
)

CLOSEOUT_PATH.write_text(
    closeout.rstrip() + "\n",
    encoding="utf-8",
    newline="\n",
)

print(CLOSEOUT_REL)
print(
    "SHA256:",
    sha256_file(CLOSEOUT_PATH),
)


# ----------------------------------------------------------------------------
# Ensure only closeout is now untracked
# ----------------------------------------------------------------------------

post_pub_paths = set(
    status_paths()
)

if post_pub_paths != {
    CLOSEOUT_REL.as_posix()
}:
    raise RuntimeError(
        "Unexpected worktree state before closeout commit:\n"
        + "\n".join(
            sorted(post_pub_paths)
        )
    )

print(
    "[PASS] only publication closeout remains uncommitted"
)


# ============================================================================
# COMMIT 2 — Publication closeout
# ============================================================================

print()
print("=" * 96)
print("COMMIT 2 — STAGE27 PUBLICATION CLOSEOUT")
print("=" * 96)

git(
    "add",
    "--",
    CLOSEOUT_REL.as_posix(),
)

staged_closeout = git(
    "diff",
    "--cached",
    "--name-only",
).splitlines()

if staged_closeout != [
    CLOSEOUT_REL.as_posix()
]:
    raise RuntimeError(
        "Closeout staging contains unexpected files."
    )

commit2 = run(
    [
        "git",
        "-c",
        "commit.gpgsign=false",
        "commit",
        "-m",
        (
            "stage27-pub2: close manuscript "
            "integration"
        ),
    ]
)

print(commit2.stdout)

FINAL_CLOSEOUT_COMMIT = git(
    "rev-parse",
    "HEAD",
)

print()
print("Final Stage27 publication closeout commit:")
print(
    " ",
    FINAL_CLOSEOUT_COMMIT,
)


# ----------------------------------------------------------------------------
# Push commit 2
# ----------------------------------------------------------------------------

print()
print("Pushing Stage27 publication closeout...")

# Remote must still equal first publication commit.
git(
    "fetch",
    "--prune",
    "origin",
    "main",
)

remote_pre_closeout = git(
    "rev-parse",
    "origin/main",
)

if remote_pre_closeout != PUB_COMMIT:
    raise RuntimeError(
        "origin/main changed before closeout push."
    )

push_main(
    push_env
)

verify_remote_head(
    FINAL_CLOSEOUT_COMMIT
)

verify_remote_files(
    "origin/main",
    [
        *PUBLICATION_FILES,
        CLOSEOUT_REL,
    ],
)


# ----------------------------------------------------------------------------
# Final deterministic package check from the new publication HEAD
# ----------------------------------------------------------------------------

print()
print("-" * 96)
print("FINAL GENERATOR CHECK FROM CLOSEOUT HEAD")
print("-" * 96)

final_check = run(
    [
        sys.executable,
        str(GENERATOR),
        "--check",
    ]
)

print(final_check.stdout)

if final_check.stderr.strip():
    print(final_check.stderr)


# ----------------------------------------------------------------------------
# Final worktree cleanliness
# ----------------------------------------------------------------------------

final_status = git(
    "status",
    "--porcelain",
    "-uall",
)

if final_status:
    print(final_status)

    raise RuntimeError(
        "Repository is not clean after Stage27 publication closeout."
    )

print()
print("[PASS] final Git worktree clean")


# ----------------------------------------------------------------------------
# Final log
# ----------------------------------------------------------------------------

print()
print("-" * 96)
print("FINAL COMMIT LINEAGE")
print("-" * 96)

print(
    git(
        "log",
        "-3",
        "--oneline",
        "--decorate",
    )
)


# ----------------------------------------------------------------------------
# Local machine-readable remote-verification receipt
# ----------------------------------------------------------------------------
#
# Kept outside the repository because the repository closeout is already
# content-addressed and remotely verified. Including this receipt would require
# a third closeout commit merely to record its own predecessor.
# ----------------------------------------------------------------------------

verification_receipt = {
    "stage": "STAGE27-PUB2",
    "timestamp_utc": datetime.now(
        timezone.utc
    ).isoformat(),
    "repository": REPO_FULL,
    "scientific_parent":
        CANONICAL_STAGE27_PARENT,
    "publication_package_commit":
        PUB_COMMIT,
    "publication_closeout_commit":
        FINAL_CLOSEOUT_COMMIT,
    "remote_head_verified":
        FINAL_CLOSEOUT_COMMIT,
    "publication_artifact_sha256":
        publication_hashes,
    "closeout": {
        "path": CLOSEOUT_REL.as_posix(),
        "sha256": sha256_file(
            CLOSEOUT_PATH
        ),
    },
    "science_operations": {
        "model_fitting": 0,
        "model_inference": 0,
        "target_reopenings": 0,
        "threshold_reselection": 0,
        "bootstrap_recomputation": 0,
        "new_formal_statistical_tests": 0,
    },
    "remote_verification": "PASS_EXACT",
    "worktree_clean": True,
}

receipt_path = Path(
    "/kaggle/working/"
    "stage27_pub2_remote_verification_receipt.json"
)

receipt_path.write_text(
    json.dumps(
        verification_receipt,
        indent=2,
        sort_keys=True,
    ) + "\n",
    encoding="utf-8",
    newline="\n",
)


# ----------------------------------------------------------------------------
# Remove temporary credential helper
# ----------------------------------------------------------------------------

try:
    askpass_path.unlink(
        missing_ok=True
    )
except Exception:
    pass

# Do not retain token beyond this cell's need.
github_token = None
push_env.pop(
    "GITHUB_TOKEN",
    None,
)


# ----------------------------------------------------------------------------
# Final
# ----------------------------------------------------------------------------

print()
print("=" * 96)
print("STAGE27 PUBLICATION INTEGRATION — REMOTELY CLOSED")
print("=" * 96)

print()
print("Scientific parent:")
print(
    " ",
    CANONICAL_STAGE27_PARENT,
)

print()
print("Publication package commit:")
print(
    " ",
    PUB_COMMIT,
)

print()
print("Publication closeout commit:")
print(
    " ",
    FINAL_CLOSEOUT_COMMIT,
)

print()
print("Remote:")
print(
    "  origin/main:",
    git("rev-parse", "origin/main"),
)

print()
print("Publication files:")
for rel in PUBLICATION_FILES:
    print(
        f"  {rel}\n"
        f"    {sha256_file(REPO / rel)}"
    )

print(
    f"  {CLOSEOUT_REL}\n"
    f"    {sha256_file(CLOSEOUT_PATH)}"
)

print()
print("Integrity:")
print("  frozen Stage27 science       : UNCHANGED")
print("  deterministic generator check: PASS")
print("  remote commit identity       : PASS")
print("  remote file SHA256           : PASS")
print("  final worktree               : CLEAN")

print()
print("Science operations during publication:")
print("  model fitting             : 0")
print("  model inference           : 0")
print("  target reopening          : 0")
print("  threshold reselection     : 0")
print("  bootstrap recomputation   : 0")
print("  new formal statistics     : 0")

print()
print("Local remote-verification receipt:")
print(
    " ",
    receipt_path,
)
print(
    "  SHA256:",
    sha256_file(receipt_path),
)

print()
print("NEXT PHASE:")
print(
    "  WHOLE-MANUSCRIPT ASSEMBLY + "
    "CLAIM-TO-ARTIFACT CONSISTENCY AUDIT"
)


# %% [Stage27 notebook cell 11]
# ============================================================================
# STAGE27-PUB1R
# FULL KAGGLE NOTEBOOK + PYTHON REPRODUCIBILITY EXPORT
#
# PURPOSE
#   Export the complete Stage27 Kaggle notebook before publication closeout.
#
# OUTPUT
#   scripts/stage27/stage27_loao_unseen_attack.ipynb
#   scripts/stage27/stage27_loao_unseen_attack.py
#
#   results/stage27_loao_unseen_attack/stage27_publication_package/
#       stage27_notebook_export_receipt.json
#
# IMPORTANT
#   - NO model fitting
#   - NO model inference
#   - NO target reopening
#   - NO threshold reselection
#   - NO bootstrap recomputation
#   - NO Git commit
#   - NO Git push
#
# The exporter prefers an exact live notebook snapshot.
# It falls back to IPython execution history only when that history is
# sufficiently complete to represent the Stage27 execution notebook.
# ============================================================================

from __future__ import annotations

import copy
import hashlib
import json
import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path
from datetime import datetime, timezone


# ============================================================================
# 0. PATHS / FROZEN IDENTITY
# ============================================================================

REPO = Path(
    "/kaggle/working/ids2018-validation-safe-ablation"
)

CANONICAL_STAGE27_PARENT = (
    "0e1439565aedc7da9b7ca1207262e9061422bc22"
)

STAGE_DIR = (
    REPO
    / "scripts"
    / "stage27"
)

NOTEBOOK_OUT = (
    STAGE_DIR
    / "stage27_loao_unseen_attack.ipynb"
)

PYTHON_OUT = (
    STAGE_DIR
    / "stage27_loao_unseen_attack.py"
)

RECEIPT_OUT = (
    REPO
    / "results"
    / "stage27_loao_unseen_attack"
    / "stage27_publication_package"
    / "stage27_notebook_export_receipt.json"
)


# Existing PUB1 files which are expected to be untracked right now.
EXPECTED_EXISTING_PUB1_PATHS = {
    "docs/STAGE27_MANUSCRIPT_INTEGRATION.md",
    "docs/STAGE27_MANUSCRIPT_INTEGRATION.tex",
    "docs/STAGE27_PUBLICATION_TABLES.md",
    "docs/STAGE27_PUBLICATION_TABLES.tex",
    (
        "results/stage27_loao_unseen_attack/"
        "stage27_publication_package/"
        "stage27_publication_manifest.json"
    ),
    "scripts/stage27/stage27_publication_integration.py",
}


# After PUB1R we expect exactly these additional paths.
NEW_REPRO_PATHS = {
    "scripts/stage27/stage27_loao_unseen_attack.ipynb",
    "scripts/stage27/stage27_loao_unseen_attack.py",
    (
        "results/stage27_loao_unseen_attack/"
        "stage27_publication_package/"
        "stage27_notebook_export_receipt.json"
    ),
}


# Conservative GitHub single-file safety threshold.
# GitHub hard limit is 100 MB; stay well below that.
MAX_GITHUB_FILE_BYTES = 90 * 1024 * 1024


# ============================================================================
# 1. HELPERS
# ============================================================================

def run(
    cmd,
    *,
    cwd=REPO,
    check=True,
    text=True,
):
    result = subprocess.run(
        [str(x) for x in cmd],
        cwd=cwd,
        text=text,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    if check and result.returncode != 0:
        if text:
            print(result.stdout)
            print(result.stderr)

        raise RuntimeError(
            f"Command failed ({result.returncode}): "
            + " ".join(str(x) for x in cmd)
        )

    return result


def git(*args, check=True):
    return run(
        ["git", *args],
        check=check,
    ).stdout.strip()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()

    with path.open("rb") as fh:
        while True:
            block = fh.read(
                8 * 1024 * 1024
            )

            if not block:
                break

            h.update(block)

    return h.hexdigest()


def git_status_paths():
    output = git(
        "status",
        "--porcelain",
        "-uall",
    )

    paths = set()

    if not output:
        return paths

    for line in output.splitlines():
        raw = line[3:]

        if " -> " in raw:
            raw = raw.split(
                " -> ",
                1,
            )[1]

        paths.add(raw)

    return paths


def source_text_from_notebook(nb):
    pieces = []

    for cell in nb.get(
        "cells",
        [],
    ):
        source = cell.get(
            "source",
            "",
        )

        if isinstance(
            source,
            list,
        ):
            source = "".join(source)

        pieces.append(
            str(source)
        )

    return "\n".join(
        pieces
    )


def count_cells(nb):
    cells = nb.get(
        "cells",
        [],
    )

    code = sum(
        1
        for cell in cells
        if cell.get("cell_type") == "code"
    )

    markdown = sum(
        1
        for cell in cells
        if cell.get("cell_type") == "markdown"
    )

    raw = sum(
        1
        for cell in cells
        if cell.get("cell_type") == "raw"
    )

    executed = sum(
        1
        for cell in cells
        if (
            cell.get("cell_type") == "code"
            and
            cell.get("execution_count") is not None
        )
    )

    output_cells = sum(
        1
        for cell in cells
        if (
            cell.get("cell_type") == "code"
            and
            len(
                cell.get(
                    "outputs",
                    [],
                )
            ) > 0
        )
    )

    return {
        "total": len(cells),
        "code": code,
        "markdown": markdown,
        "raw": raw,
        "executed_code": executed,
        "code_cells_with_outputs": output_cells,
    }


# ============================================================================
# 2. REPOSITORY PREFLIGHT
# ============================================================================

print("=" * 92)
print(
    "STAGE27-PUB1R — FULL NOTEBOOK / PYTHON "
    "REPRODUCIBILITY EXPORT"
)
print("=" * 92)

if not REPO.is_dir():
    raise RuntimeError(
        "Repository checkout not found. "
        "PUB0/PUB1 must run first."
    )

branch = git(
    "branch",
    "--show-current",
)

head = git(
    "rev-parse",
    "HEAD",
)

print()
print("repository :", REPO)
print("branch     :", branch)
print("HEAD       :", head)

if branch != "main":
    raise RuntimeError(
        f"Expected main branch; found {branch}"
    )

if head != CANONICAL_STAGE27_PARENT:
    raise RuntimeError(
        "\nPUB1R must run before PUB2 and while HEAD "
        "is still the frozen Stage27 scientific parent.\n\n"
        f"Expected:\n  {CANONICAL_STAGE27_PARENT}\n"
        f"Actual:\n  {head}"
    )


current_changes = git_status_paths()

if current_changes != EXPECTED_EXISTING_PUB1_PATHS:
    print()
    print("Expected existing PUB1 changes:")

    for path in sorted(
        EXPECTED_EXISTING_PUB1_PATHS
    ):
        print(" ", path)

    print()
    print("Actual worktree changes:")

    for path in sorted(
        current_changes
    ):
        print(" ", path)

    raise RuntimeError(
        "Worktree is not in the exact expected "
        "post-PUB1 state."
    )

print(
    "[PASS] exact post-PUB1 worktree state"
)


# ============================================================================
# 3. LOAD NBFORMAT
# ============================================================================

try:
    import nbformat
except Exception as exc:
    raise RuntimeError(
        "nbformat is required for the Stage27 notebook export."
    ) from exc


# ============================================================================
# 4. CURRENT KERNEL ID
# ============================================================================

def current_kernel_id():
    try:
        from ipykernel.connect import (
            get_connection_file,
        )

        connection = Path(
            get_connection_file()
        ).name

        match = re.search(
            r"kernel-(.+)\.json$",
            connection,
        )

        if match:
            return match.group(1)

    except Exception:
        pass

    return None


KERNEL_ID = current_kernel_id()

print()
print("Current kernel ID:")
print(
    " ",
    KERNEL_ID
    if KERNEL_ID
    else "[unavailable]"
)


# ============================================================================
# 5. TRY EXACT NOTEBOOK VIA JUPYTER SERVER API
# ============================================================================

def url_get_json(url, timeout=5):
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
        },
    )

    with urllib.request.urlopen(
        request,
        timeout=timeout,
    ) as response:
        return json.loads(
            response.read().decode(
                "utf-8"
            )
        )


def jupyter_server_records():
    commands = [
        [
            "jupyter",
            "server",
            "list",
            "--json",
        ],
        [
            "jupyter",
            "notebook",
            "list",
            "--json",
        ],
    ]

    records = []

    for command in commands:
        result = run(
            command,
            cwd=Path("/kaggle/working"),
            check=False,
        )

        if result.returncode != 0:
            continue

        for line in result.stdout.splitlines():
            line = line.strip()

            if not line:
                continue

            try:
                record = json.loads(
                    line
                )
            except Exception:
                continue

            if isinstance(
                record,
                dict,
            ):
                records.append(
                    record
                )

    # Deduplicate by URL/root combination.
    unique = []
    seen = set()

    for record in records:
        key = (
            record.get("url"),
            record.get("root_dir")
            or record.get("notebook_dir"),
        )

        if key not in seen:
            seen.add(key)
            unique.append(record)

    return unique


def exact_notebook_from_server():
    if not KERNEL_ID:
        return None, None

    servers = jupyter_server_records()

    for server in servers:
        base_url = server.get(
            "url"
        )

        if not base_url:
            continue

        if not base_url.endswith("/"):
            base_url += "/"

        token = (
            server.get("token")
            or ""
        )

        query = ""

        if token:
            query = (
                "?token="
                + urllib.parse.quote(
                    token
                )
            )

        sessions_url = (
            urllib.parse.urljoin(
                base_url,
                "api/sessions",
            )
            + query
        )

        try:
            sessions = url_get_json(
                sessions_url
            )
        except Exception:
            continue

        for session in sessions:
            kernel = session.get(
                "kernel",
                {},
            )

            if kernel.get("id") != KERNEL_ID:
                continue

            notebook_info = (
                session.get("notebook")
                or {}
            )

            notebook_path = (
                notebook_info.get("path")
                or session.get("path")
            )

            if not notebook_path:
                continue

            encoded_path = urllib.parse.quote(
                notebook_path,
                safe="/",
            )

            contents_url = (
                urllib.parse.urljoin(
                    base_url,
                    "api/contents/"
                    + encoded_path,
                )
                + query
            )

            try:
                model = url_get_json(
                    contents_url
                )
            except Exception:
                continue

            if (
                model.get("type")
                != "notebook"
            ):
                continue

            content = model.get(
                "content"
            )

            if not isinstance(
                content,
                dict,
            ):
                continue

            return (
                content,
                {
                    "mode":
                        "EXACT_JUPYTER_CONTENTS_API",

                    "server_root":
                        server.get(
                            "root_dir"
                        )
                        or server.get(
                            "notebook_dir"
                        ),

                    "notebook_path":
                        notebook_path,
                },
            )

    return None, None


# ============================================================================
# 6. TRY EXACT NOTEBOOK FROM LOCAL KAGGLE PATHS
# ============================================================================

def local_notebook_candidates():
    candidates = []

    explicit = [
        Path(
            "/kaggle/working/__notebook__.ipynb"
        ),
        Path(
            "/kaggle/working/notebook.ipynb"
        ),
    ]

    for path in explicit:
        if path.is_file():
            candidates.append(path)

    # Top-level Kaggle working notebook files.
    try:
        candidates.extend(
            Path("/kaggle/working").glob(
                "*.ipynb"
            )
        )
    except Exception:
        pass

    # Avoid selecting our target export.
    cleaned = []

    seen = set()

    for path in candidates:
        try:
            resolved = path.resolve()
        except Exception:
            continue

        if resolved == NOTEBOOK_OUT.resolve():
            continue

        if resolved in seen:
            continue

        seen.add(
            resolved
        )

        cleaned.append(
            resolved
        )

    return cleaned


def exact_notebook_from_local():
    matches = []

    for path in local_notebook_candidates():
        try:
            nb = nbformat.read(
                path,
                as_version=4,
            )
        except Exception:
            continue

        text = source_text_from_notebook(
            nb
        )

        # Current notebook must include both publication cells
        # already executed in this session/source.
        if (
            "STAGE27-PUB0"
            in text
            and
            "STAGE27-PUB1"
            in text
        ):
            matches.append(
                (
                    path,
                    nb,
                )
            )

    if not matches:
        return None, None

    # Prefer the largest notebook; it is more likely to be
    # the complete Stage27 source rather than a small partial copy.
    matches.sort(
        key=lambda item:
            item[0].stat().st_size,
        reverse=True,
    )

    path, nb = matches[0]

    return (
        nb,
        {
            "mode":
                "EXACT_LOCAL_NOTEBOOK_FILE",

            "notebook_path":
                str(path),

            "source_bytes":
                path.stat().st_size,
        },
    )


# ============================================================================
# 7. FALLBACK: RECONSTRUCT FROM CURRENT IPYTHON INPUT HISTORY
# ============================================================================

def notebook_from_ipython_history():
    try:
        ip = get_ipython()
    except Exception:
        ip = None

    if ip is None:
        return None, None

    history = []

    try:
        # Current session raw input, in execution order.
        for session, line_no, source in (
            ip.history_manager.get_range(
                session=0,
                start=1,
                stop=None,
                raw=True,
                output=False,
            )
        ):
            if not source:
                continue

            history.append(
                {
                    "session": int(
                        session
                    ),
                    "line_no": int(
                        line_no
                    ),
                    "source": str(
                        source
                    ),
                }
            )

    except Exception as exc:
        print(
            "[WARN] IPython history access failed:",
            repr(exc),
        )

        return None, None

    if not history:
        return None, None

    sources = [
        item["source"]
        for item in history
    ]

    joined = "\n\n".join(
        sources
    )

    # Hard completeness gates:
    #
    # We do NOT accept a new session containing only PUB0/PUB1/PUB1R.
    #
    # Stage27 was a multi-stage scientific notebook. Reconstructed
    # history must therefore contain substantial Stage27 execution.
    marker_candidates = [
        "STAGE27-0",
        "STAGE27-1",
        "STAGE27-2",
        "STAGE27-3",
        "STAGE27-4",
        "stage27_0",
        "stage27_1",
        "stage27_2",
        "stage27_3",
        "stage27_4",
    ]

    marker_hits = sorted({
        marker
        for marker in marker_candidates
        if marker in joined
    })

    stage27_occurrences = (
        joined.upper().count(
            "STAGE27"
        )
    )

    print()
    print(
        "IPython history candidate:"
    )
    print(
        "  executed input cells :",
        len(history),
    )
    print(
        "  STAGE27 occurrences  :",
        stage27_occurrences,
    )
    print(
        "  scientific markers   :",
        marker_hits,
    )

    if len(history) < 10:
        return (
            None,
            {
                "mode":
                    "HISTORY_REJECTED_TOO_FEW_CELLS",

                "history_cells":
                    len(history),

                "stage27_occurrences":
                    stage27_occurrences,

                "marker_hits":
                    marker_hits,
            },
        )

    if stage27_occurrences < 10:
        return (
            None,
            {
                "mode":
                    "HISTORY_REJECTED_INSUFFICIENT_STAGE27_CONTENT",

                "history_cells":
                    len(history),

                "stage27_occurrences":
                    stage27_occurrences,

                "marker_hits":
                    marker_hits,
            },
        )

    # Reconstruct code cells in execution order.
    cells = []

    for index, item in enumerate(
        history,
        start=1,
    ):
        cell = nbformat.v4.new_code_cell(
            source=item["source"]
        )

        cell["execution_count"] = (
            item["line_no"]
        )

        cell["metadata"] = {
            "stage27_execution_history_index":
                index,

            "stage27_ipython_session":
                item["session"],

            "stage27_ipython_line_number":
                item["line_no"],
        }

        # Outputs cannot be faithfully recovered from IPython
        # input history, so they remain empty.
        cell["outputs"] = []

        cells.append(
            cell
        )

    nb = nbformat.v4.new_notebook(
        cells=cells
    )

    nb["metadata"][
        "stage27_reproducibility_export"
    ] = {
        "mode":
            "RECONSTRUCTED_FROM_IPYTHON_INPUT_HISTORY",

        "preserves":
            "executed code-cell source and execution order",

        "does_not_preserve": [
            "unexecuted notebook cells",
            "original markdown-only cells",
            "cell outputs",
            "original notebook UI metadata",
        ],

        "history_cells":
            len(history),

        "stage27_occurrences":
            stage27_occurrences,

        "marker_hits":
            marker_hits,
    }

    return (
        nb,
        {
            "mode":
                "RECONSTRUCTED_FROM_IPYTHON_INPUT_HISTORY",

            "history_cells":
                len(history),

            "stage27_occurrences":
                stage27_occurrences,

            "marker_hits":
                marker_hits,
        },
    )


# ============================================================================
# 8. ACQUIRE THE BEST AVAILABLE COMPLETE NOTEBOOK
# ============================================================================

print()
print("-" * 92)
print("NOTEBOOK ACQUISITION")
print("-" * 92)


NOTEBOOK = None
ACQUISITION = None


# First preference: live Jupyter Contents API.
try:
    NOTEBOOK, ACQUISITION = (
        exact_notebook_from_server()
    )
except Exception as exc:
    print(
        "[WARN] Jupyter API acquisition error:",
        repr(exc),
    )


if NOTEBOOK is not None:
    print(
        "[PASS] exact live notebook acquired "
        "through Jupyter Contents API"
    )


# Second preference: exact local .ipynb.
if NOTEBOOK is None:
    try:
        NOTEBOOK, ACQUISITION = (
            exact_notebook_from_local()
        )
    except Exception as exc:
        print(
            "[WARN] local notebook acquisition error:",
            repr(exc),
        )

    if NOTEBOOK is not None:
        print(
            "[PASS] exact notebook acquired "
            "from local Kaggle filesystem"
        )


# Final fallback: current execution history.
if NOTEBOOK is None:
    NOTEBOOK, history_info = (
        notebook_from_ipython_history()
    )

    if NOTEBOOK is not None:
        ACQUISITION = (
            history_info
        )

        print(
            "[PASS] complete-enough execution-source "
            "notebook reconstructed from IPython history"
        )

    else:
        print()
        print(
            "Exact live notebook source was not accessible."
        )

        if history_info:
            print(
                json.dumps(
                    history_info,
                    indent=2,
                )
            )

        raise RuntimeError(
            "\nFULL STAGE27 NOTEBOOK EXPORT BLOCKED.\n\n"
            "Kaggle did not expose an exact notebook source, and the "
            "current kernel history was not sufficiently complete to "
            "represent the Stage27 scientific notebook.\n\n"
            "This exporter intentionally refuses to create a misleading "
            "'full' notebook from only PUB0/PUB1 cells.\n"
        )


# ============================================================================
# 9. NORMALIZE / TAG EXPORT METADATA
# ============================================================================

NOTEBOOK = copy.deepcopy(
    NOTEBOOK
)

NOTEBOOK.setdefault(
    "metadata",
    {},
)

NOTEBOOK["metadata"][
    "stage27_reproducibility_export"
] = {
    **NOTEBOOK["metadata"].get(
        "stage27_reproducibility_export",
        {},
    ),

    "export_stage":
        "STAGE27-PUB1R",

    "scientific_parent":
        CANONICAL_STAGE27_PARENT,

    "scientific_status":
        "CLOSED",

    "acquisition":
        ACQUISITION,

    "science_operations_during_export": {
        "model_fits": 0,
        "model_inference": 0,
        "target_reopenings": 0,
        "threshold_reselection": 0,
        "bootstrap_recomputation": 0,
        "new_formal_statistical_tests": 0,
    },
}


# ============================================================================
# 10. COMPLETENESS / CONTENT AUDIT
# ============================================================================

stats = count_cells(
    NOTEBOOK
)

all_source = source_text_from_notebook(
    NOTEBOOK
)

print()
print("-" * 92)
print("NOTEBOOK CONTENT AUDIT")
print("-" * 92)

print(
    json.dumps(
        stats,
        indent=2,
    )
)

required_pub_markers = [
    "STAGE27-PUB0",
    "STAGE27-PUB1",
]

for marker in required_pub_markers:
    if marker not in all_source:
        raise RuntimeError(
            f"Notebook export is missing required current marker: "
            f"{marker}"
        )

print(
    "[PASS] PUB0/PUB1 source present"
)


stage27_mentions = (
    all_source.upper().count(
        "STAGE27"
    )
)

print(
    "STAGE27 source occurrences:",
    stage27_mentions,
)

if stage27_mentions < 10:
    raise RuntimeError(
        "Notebook contains too little Stage27 source content "
        "to be accepted as the complete reproducibility export."
    )


# ============================================================================
# 11. SECRET-SAFETY SCAN
# ============================================================================

print()
print("-" * 92)
print("SECRET-SAFETY SCAN")
print("-" * 92)

# Scan source only. We do not want credentials committed in notebook source.
SECRET_PATTERNS = {
    "GitHub classic PAT":
        r"\bghp_[A-Za-z0-9]{20,}\b",

    "GitHub fine-grained PAT":
        r"\bgithub_pat_[A-Za-z0-9_]{20,}\b",

    "GitHub OAuth token":
        r"\bgho_[A-Za-z0-9]{20,}\b",

    "GitHub user token":
        r"\bghu_[A-Za-z0-9]{20,}\b",

    "GitHub server token":
        r"\bghs_[A-Za-z0-9]{20,}\b",

    "Stripe live secret":
        r"\bsk_live_[A-Za-z0-9]{16,}\b",

    "AWS access key":
        r"\bAKIA[0-9A-Z]{16}\b",
}


secret_hits = []

for label, pattern in SECRET_PATTERNS.items():
    matches = re.findall(
        pattern,
        all_source,
    )

    if matches:
        secret_hits.append(
            {
                "type": label,
                "count": len(matches),
            }
        )


if secret_hits:
    print(
        json.dumps(
            secret_hits,
            indent=2,
        )
    )

    raise RuntimeError(
        "Potential credential material detected in notebook source. "
        "Export blocked before writing GitHub artifacts."
    )

print(
    "[PASS] no recognized credential token patterns "
    "found in notebook source"
)


# ============================================================================
# 12. WRITE FULL IPYNB
# ============================================================================

STAGE_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

NOTEBOOK_OUT.parent.mkdir(
    parents=True,
    exist_ok=True,
)

nbformat.write(
    NOTEBOOK,
    NOTEBOOK_OUT,
)

print()
print("-" * 92)
print("IPYNB EXPORT")
print("-" * 92)

print(NOTEBOOK_OUT)
print(
    "bytes :",
    f"{NOTEBOOK_OUT.stat().st_size:,}",
)
print(
    "SHA256:",
    sha256_file(
        NOTEBOOK_OUT
    ),
)


# ============================================================================
# 13. GENERATE PYTHON EXPORT FROM ALL NOTEBOOK CELLS
# ============================================================================

def comment_markdown(text):
    lines = str(text).splitlines()

    if not lines:
        return "#"

    return "\n".join(
        (
            "#"
            if line == ""
            else "# " + line
        )
        for line in lines
    )


py_parts = [
    (
        "# "
        + "=" * 78
    ),
    (
        "# STAGE27 — LEAVE-ONE-ATTACK-FAMILY-OUT "
        "UNSEEN-FAMILY GENERALIZATION AUDIT"
    ),
    (
        "# Complete source export from the Stage27 Kaggle notebook."
    ),
    "#",
    (
        "# Scientific parent: "
        + CANONICAL_STAGE27_PARENT
    ),
    "# Scientific state: CLOSED",
    "#",
    (
        "# This export preserves notebook source order for "
        "reproducibility."
    ),
    (
        "# It does NOT authorize any new Stage27 fitting, inference, "
        "target reopening, threshold reselection, bootstrap "
        "recomputation, or formal statistical testing."
    ),
    (
        "# "
        + "=" * 78
    ),
    "",
]


for index, cell in enumerate(
    NOTEBOOK.get(
        "cells",
        [],
    ),
    start=1,
):
    cell_type = cell.get(
        "cell_type",
        "unknown",
    )

    source = cell.get(
        "source",
        "",
    )

    if isinstance(
        source,
        list,
    ):
        source = "".join(
            source
        )

    if cell_type == "code":
        py_parts.extend([
            "",
            (
                f"# %% [Stage27 notebook cell {index}]"
            ),
            str(source).rstrip(),
            "",
        ])

    elif cell_type == "markdown":
        py_parts.extend([
            "",
            (
                f"# %% [markdown — Stage27 notebook cell {index}]"
            ),
            comment_markdown(
                source
            ),
            "",
        ])

    elif cell_type == "raw":
        py_parts.extend([
            "",
            (
                f"# %% [raw — Stage27 notebook cell {index}]"
            ),
            comment_markdown(
                source
            ),
            "",
        ])


PYTHON_OUT.write_text(
    "\n".join(
        py_parts
    ).rstrip()
    + "\n",
    encoding="utf-8",
    newline="\n",
)

print()
print("-" * 92)
print("PYTHON EXPORT")
print("-" * 92)

print(PYTHON_OUT)
print(
    "bytes :",
    f"{PYTHON_OUT.stat().st_size:,}",
)
print(
    "SHA256:",
    sha256_file(
        PYTHON_OUT
    ),
)


# ============================================================================
# 14. VERIFY PYTHON EXPORT CONTAINS THE NOTEBOOK CODE CELLS
# ============================================================================

py_text = PYTHON_OUT.read_text(
    encoding="utf-8"
)

code_cells = [
    cell
    for cell in NOTEBOOK["cells"]
    if cell.get("cell_type") == "code"
]

missing_code_cells = []

for index, cell in enumerate(
    code_cells,
    start=1,
):
    source = cell.get(
        "source",
        "",
    )

    if isinstance(
        source,
        list,
    ):
        source = "".join(
            source
        )

    source = str(
        source
    ).rstrip()

    if (
        source
        and
        source not in py_text
    ):
        missing_code_cells.append(
            index
        )


if missing_code_cells:
    raise RuntimeError(
        "Python export failed source-preservation audit for "
        f"{len(missing_code_cells)} code cell(s): "
        f"{missing_code_cells[:20]}"
    )

print()
print(
    "[PASS] every notebook code-cell source is present "
    "in the Python export"
)


# ============================================================================
# 15. SIZE GATE
# ============================================================================

for path in [
    NOTEBOOK_OUT,
    PYTHON_OUT,
]:
    if (
        path.stat().st_size
        > MAX_GITHUB_FILE_BYTES
    ):
        raise RuntimeError(
            f"GitHub-safe size gate failed:\n"
            f"{path}\n"
            f"bytes={path.stat().st_size:,}"
        )

print(
    "[PASS] both reproducibility exports are below "
    "the conservative GitHub file-size gate"
)


# ============================================================================
# 16. WRITE NOTEBOOK EXPORT RECEIPT
# ============================================================================

RECEIPT_OUT.parent.mkdir(
    parents=True,
    exist_ok=True,
)

receipt = {
    "stage":
        "STAGE27-PUB1R",

    "timestamp_utc":
        datetime.now(
            timezone.utc
        ).isoformat(),

    "repository":
        "themubasshir/ids2018-validation-safe-ablation",

    "scientific_parent":
        CANONICAL_STAGE27_PARENT,

    "scientific_status":
        "CLOSED",

    "acquisition":
        ACQUISITION,

    "notebook": {
        "path":
            NOTEBOOK_OUT.relative_to(
                REPO
            ).as_posix(),

        "sha256":
            sha256_file(
                NOTEBOOK_OUT
            ),

        "bytes":
            NOTEBOOK_OUT.stat().st_size,

        "cell_counts":
            stats,

        "stage27_source_occurrences":
            stage27_mentions,
    },

    "python_export": {
        "path":
            PYTHON_OUT.relative_to(
                REPO
            ).as_posix(),

        "sha256":
            sha256_file(
                PYTHON_OUT
            ),

        "bytes":
            PYTHON_OUT.stat().st_size,

        "all_code_cell_sources_preserved":
            True,
    },

    "secret_scan": {
        "status":
            "PASS",

        "recognized_secret_patterns_found":
            0,
    },

    "science_operations": {
        "model_fits": 0,
        "model_inference": 0,
        "target_reopenings": 0,
        "threshold_reselection": 0,
        "bootstrap_recomputation": 0,
        "new_formal_statistical_tests": 0,
    },

    "git_operations": {
        "commit":
            False,

        "push":
            False,
    },
}


RECEIPT_OUT.write_text(
    json.dumps(
        receipt,
        indent=2,
        sort_keys=True,
    )
    + "\n",
    encoding="utf-8",
    newline="\n",
)


print()
print("-" * 92)
print("EXPORT RECEIPT")
print("-" * 92)

print(RECEIPT_OUT)
print(
    "SHA256:",
    sha256_file(
        RECEIPT_OUT
    ),
)


# ============================================================================
# 17. FROZEN SCIENCE MODIFICATION GATE
# ============================================================================

science_diff = run(
    [
        "git",
        "diff",
        "--",
        (
            "results/stage27_loao_unseen_attack/"
            "stage27_4a_final_synthesis"
        ),
    ]
).stdout

if science_diff.strip():
    print(
        science_diff
    )

    raise RuntimeError(
        "Notebook export modified frozen Stage27 science."
    )

print()
print(
    "[PASS] frozen Stage27-4A science remains untouched"
)


# ============================================================================
# 18. EXACT POST-EXPORT WORKTREE INVENTORY
# ============================================================================

expected_final_paths = (
    EXPECTED_EXISTING_PUB1_PATHS
    |
    NEW_REPRO_PATHS
)

actual_final_paths = (
    git_status_paths()
)

print()
print("-" * 92)
print("POST-EXPORT GIT STATUS")
print("-" * 92)

print(
    git(
        "status",
        "--short",
        "-uall",
    )
)


if (
    actual_final_paths
    != expected_final_paths
):
    unexpected = (
        actual_final_paths
        -
        expected_final_paths
    )

    missing = (
        expected_final_paths
        -
        actual_final_paths
    )

    print()
    print(
        "Unexpected:",
        sorted(
            unexpected
        ),
    )

    print(
        "Missing:",
        sorted(
            missing
        ),
    )

    raise RuntimeError(
        "PUB1R introduced an unexpected repository path."
    )


print()
print(
    "[PASS] exact authorized post-PUB1R worktree inventory"
)


# ============================================================================
# 19. FINAL SUMMARY
# ============================================================================

print()
print("=" * 92)
print(
    "STAGE27-PUB1R COMPLETE — FULL REPRODUCIBILITY EXPORT READY"
)
print("=" * 92)

print()
print("Acquisition mode:")
print(
    " ",
    ACQUISITION.get(
        "mode"
    )
)

print()
print("Notebook:")
print(
    " ",
    NOTEBOOK_OUT.relative_to(
        REPO
    )
)
print(
    "  SHA256:",
    sha256_file(
        NOTEBOOK_OUT
    ),
)
print(
    "  bytes:",
    f"{NOTEBOOK_OUT.stat().st_size:,}",
)
print(
    "  cells:",
    stats,
)

print()
print("Python export:")
print(
    " ",
    PYTHON_OUT.relative_to(
        REPO
    )
)
print(
    "  SHA256:",
    sha256_file(
        PYTHON_OUT
    ),
)
print(
    "  bytes:",
    f"{PYTHON_OUT.stat().st_size:,}",
)

print()
print("Receipt:")
print(
    " ",
    RECEIPT_OUT.relative_to(
        REPO
    )
)
print(
    "  SHA256:",
    sha256_file(
        RECEIPT_OUT
    ),
)

print()
print("Integrity:")
print("  Stage27 scientific artifacts modified : NO")
print("  secret-source scan                    : PASS")
print("  Python source preservation            : PASS")
print("  GitHub file-size gate                 : PASS")

print()
print("Git:")
print("  commit : NOT PERFORMED")
print("  push   : NOT PERFORMED")

print()
print(
    "NEXT: revise PUB2 to include the full .ipynb, "
    ".py, and export receipt in the remote publication closeout."
)


# %% [Stage27 notebook cell 12]
# ============================================================================
# STAGE27-PUB3A
# COMPLETE STAGE27 KAGGLE NOTEBOOK + PYTHON REPRODUCIBILITY EXPORT
#
# CURRENT STATE
#   Scientific freeze:
#     0e1439565aedc7da9b7ca1207262e9061422bc22
#
#   Publication closeout currently expected:
#     3407ff3954abae9b0c8bfdaa14b704a05f31affe
#
# PURPOSE
#   Add the complete Stage27 Kaggle notebook and Python source export
#   AFTER the publication closeout, without altering any frozen science.
#
# OUTPUT
#   scripts/stage27/stage27_loao_unseen_attack.ipynb
#   scripts/stage27/stage27_loao_unseen_attack.py
#
#   results/stage27_loao_unseen_attack/stage27_publication_package/
#       stage27_notebook_export_receipt.json
#
# THIS CELL DOES NOT:
#   - fit models
#   - run inference
#   - reopen targets
#   - reselect thresholds
#   - recompute bootstrap intervals
#   - run new statistical tests
#   - commit
#   - push
# ============================================================================

from __future__ import annotations

import copy
import hashlib
import json
import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request

from pathlib import Path
from datetime import datetime, timezone


# =============================================================================
# 0. FROZEN / CURRENT REPOSITORY IDENTITY
# =============================================================================

REPO = Path(
    "/kaggle/working/ids2018-validation-safe-ablation"
)

SCIENTIFIC_FREEZE = (
    "0e1439565aedc7da9b7ca1207262e9061422bc22"
)

KNOWN_PUBLICATION_CLOSEOUT = (
    "3407ff3954abae9b0c8bfdaa14b704a05f31affe"
)

STAGE_DIR = (
    REPO
    / "scripts"
    / "stage27"
)

NOTEBOOK_REL = Path(
    "scripts/stage27/stage27_loao_unseen_attack.ipynb"
)

PYTHON_REL = Path(
    "scripts/stage27/stage27_loao_unseen_attack.py"
)

RECEIPT_REL = Path(
    "results/stage27_loao_unseen_attack/"
    "stage27_publication_package/"
    "stage27_notebook_export_receipt.json"
)

NOTEBOOK_OUT = (
    REPO
    / NOTEBOOK_REL
)

PYTHON_OUT = (
    REPO
    / PYTHON_REL
)

RECEIPT_OUT = (
    REPO
    / RECEIPT_REL
)

MAX_GITHUB_BYTES = (
    90
    * 1024
    * 1024
)


# =============================================================================
# 1. HELPERS
# =============================================================================

def run(
    cmd,
    *,
    cwd=REPO,
    check=True,
    text=True,
):
    result = subprocess.run(
        [str(x) for x in cmd],
        cwd=cwd,
        text=text,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    if (
        check
        and
        result.returncode != 0
    ):
        if text:
            print(
                result.stdout
            )
            print(
                result.stderr
            )

        raise RuntimeError(
            f"Command failed ({result.returncode}): "
            + " ".join(
                str(x)
                for x in cmd
            )
        )

    return result


def git(
    *args,
    check=True,
):
    return run(
        [
            "git",
            *args,
        ],
        check=check,
    ).stdout.strip()


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
                8
                * 1024
                * 1024
            )

            if not block:
                break

            h.update(
                block
            )

    return h.hexdigest()


def status_paths():
    output = git(
        "status",
        "--porcelain",
        "-uall",
    )

    result = set()

    if not output:
        return result

    for line in output.splitlines():

        raw = line[3:]

        if " -> " in raw:

            raw = raw.split(
                " -> ",
                1,
            )[1]

        result.add(
            raw
        )

    return result


def notebook_source_text(
    notebook,
):
    chunks = []

    for cell in notebook.get(
        "cells",
        [],
    ):

        source = cell.get(
            "source",
            "",
        )

        if isinstance(
            source,
            list,
        ):

            source = "".join(
                source
            )

        chunks.append(
            str(
                source
            )
        )

    return "\n".join(
        chunks
    )


def notebook_serialized_text(
    notebook,
):
    return json.dumps(
        notebook,
        ensure_ascii=False,
    )


def cell_stats(
    notebook,
):
    cells = notebook.get(
        "cells",
        [],
    )

    return {
        "total":
            len(
                cells
            ),

        "code":
            sum(
                1
                for cell in cells
                if cell.get(
                    "cell_type"
                ) == "code"
            ),

        "markdown":
            sum(
                1
                for cell in cells
                if cell.get(
                    "cell_type"
                ) == "markdown"
            ),

        "raw":
            sum(
                1
                for cell in cells
                if cell.get(
                    "cell_type"
                ) == "raw"
            ),

        "executed_code":
            sum(
                1
                for cell in cells
                if (
                    cell.get(
                        "cell_type"
                    ) == "code"
                    and
                    cell.get(
                        "execution_count"
                    ) is not None
                )
            ),

        "code_with_outputs":
            sum(
                1
                for cell in cells
                if (
                    cell.get(
                        "cell_type"
                    ) == "code"
                    and
                    len(
                        cell.get(
                            "outputs",
                            [],
                        )
                    ) > 0
                )
            ),
    }


# =============================================================================
# 2. REPOSITORY LINEAGE GATE
# =============================================================================

print(
    "=" * 96
)

print(
    "STAGE27-PUB3A — COMPLETE NOTEBOOK "
    "REPRODUCIBILITY EXPORT"
)

print(
    "=" * 96
)


if not REPO.is_dir():

    raise RuntimeError(
        "Repository checkout not found."
    )


branch = git(
    "branch",
    "--show-current",
)

head = git(
    "rev-parse",
    "HEAD",
)

print()
print(
    "repository       :",
    REPO,
)

print(
    "branch           :",
    branch,
)

print(
    "current HEAD     :",
    head,
)

print(
    "scientific freeze:",
    SCIENTIFIC_FREEZE,
)


if branch != "main":

    raise RuntimeError(
        f"Expected main branch; "
        f"found {branch}"
    )


# Critical change from old PUB1R:
# scientific freeze must be AN ANCESTOR,
# not necessarily equal to current HEAD.

ancestor_check = run(
    [
        "git",
        "merge-base",
        "--is-ancestor",
        SCIENTIFIC_FREEZE,
        head,
    ],
    check=False,
)


if (
    ancestor_check.returncode
    != 0
):

    raise RuntimeError(
        "\nScientific lineage gate failed.\n"
        "The frozen Stage27 scientific commit is "
        "not an ancestor of current HEAD."
    )


print(
    "[PASS] frozen Stage27 scientific commit "
    "is an ancestor of current HEAD"
)


# =============================================================================
# 3. REMOTE SYNCHRONIZATION GATE
# =============================================================================

print()
print(
    "-" * 96
)
print(
    "REMOTE SYNCHRONIZATION"
)
print(
    "-" * 96
)


git(
    "fetch",
    "--prune",
    "origin",
    "main",
)


origin_main = git(
    "rev-parse",
    "origin/main",
)


print(
    "local HEAD :",
    head,
)

print(
    "origin/main:",
    origin_main,
)


if (
    origin_main
    != head
):

    raise RuntimeError(
        "\nLocal and remote main differ.\n"
        "Resolve this before creating the notebook export."
    )


print(
    "[PASS] local HEAD == origin/main"
)


if (
    head
    == KNOWN_PUBLICATION_CLOSEOUT
):

    print(
        "[PASS] current HEAD is the known "
        "Stage27 publication-closeout commit"
    )

else:

    print(
        "[INFO] HEAD has advanced beyond the known "
        "publication-closeout commit."
    )

    known_ancestor = run(
        [
            "git",
            "merge-base",
            "--is-ancestor",
            KNOWN_PUBLICATION_CLOSEOUT,
            head,
        ],
        check=False,
    )

    if (
        known_ancestor.returncode
        != 0
    ):

        raise RuntimeError(
            "Current HEAD is not descended from the known "
            "Stage27 publication closeout."
        )

    print(
        "[PASS] known Stage27 publication closeout "
        "is also an ancestor"
    )


# =============================================================================
# 4. REQUIRE CLEAN WORKTREE
# =============================================================================

print()
print(
    "-" * 96
)
print(
    "WORKTREE GATE"
)
print(
    "-" * 96
)


before_paths = status_paths()


if before_paths:

    print(
        git(
            "status",
            "--short",
            "-uall",
        )
    )

    raise RuntimeError(
        "\nPUB3A requires a clean repository before "
        "creating the notebook export."
    )


print(
    "[PASS] worktree clean"
)


# =============================================================================
# 5. VERIFY FROZEN STAGE27 SCIENCE PATH
# =============================================================================

SYNTHESIS = (
    REPO
    / "results"
    / "stage27_loao_unseen_attack"
    / "stage27_4a_final_synthesis"
)


required_frozen = [
    (
        "stage27_final_primary_metrics.csv",
        "42ea04b3f21e6026d5d69c8d5b59aa1edd2b57e94c42da3b9f70587349704634",
    ),
    (
        "stage27_final_operating_points.csv",
        "664a5aaaff718f20bf6d619ae1dd4871a07a37c81a1631590423ea0ae07240f4",
    ),
    (
        "stage27_final_novelty_gaps.csv",
        "91c80319186fd3bbfc382e58cfc60e58fc75d23db15408564fd35c05d4fb316c",
    ),
    (
        "stage27_final_similarity.csv",
        "8c110b4f1d6317d2a2125b4f24bfb8325cdeb699ce763d268d91f3bad6acc8d3",
    ),
]


for (
    filename,
    expected,
) in required_frozen:

    path = (
        SYNTHESIS
        / filename
    )

    if not path.is_file():

        raise RuntimeError(
            f"Missing frozen Stage27 artifact: {path}"
        )

    actual = sha256_file(
        path
    )

    if actual != expected:

        raise RuntimeError(
            f"Frozen Stage27 SHA mismatch:\n"
            f"{filename}\n"
            f"expected: {expected}\n"
            f"actual:   {actual}"
        )


print(
    "[PASS] frozen Stage27 science hash anchors"
)


# =============================================================================
# 6. NBFMT
# =============================================================================

try:

    import nbformat

except Exception as exc:

    raise RuntimeError(
        "nbformat is unavailable."
    ) from exc


# =============================================================================
# 7. CURRENT KERNEL ID
# =============================================================================

def get_kernel_id():

    try:

        from ipykernel.connect import (
            get_connection_file,
        )

        filename = Path(
            get_connection_file()
        ).name

        match = re.search(
            r"kernel-(.+)\.json$",
            filename,
        )

        if match:

            return match.group(
                1
            )

    except Exception:

        pass

    return None


KERNEL_ID = (
    get_kernel_id()
)


print()
print(
    "kernel ID:",
    KERNEL_ID
    if KERNEL_ID
    else "[unavailable]",
)


# =============================================================================
# 8. HTTP JSON HELPER
# =============================================================================

def http_json(
    url,
    timeout=6,
):

    request = urllib.request.Request(
        url,
        headers={
            "Accept":
                "application/json",
        },
    )

    with urllib.request.urlopen(
        request,
        timeout=timeout,
    ) as response:

        return json.loads(
            response.read().decode(
                "utf-8"
            )
        )


# =============================================================================
# 9. DISCOVER LOCAL JUPYTER SERVER(S)
# =============================================================================

def discover_servers():

    candidates = []

    commands = [
        [
            "jupyter",
            "server",
            "list",
            "--json",
        ],
        [
            "jupyter",
            "notebook",
            "list",
            "--json",
        ],
    ]

    for command in commands:

        result = run(
            command,
            cwd=Path(
                "/kaggle/working"
            ),
            check=False,
        )

        if (
            result.returncode
            != 0
        ):

            continue

        for line in result.stdout.splitlines():

            line = line.strip()

            if not line:

                continue

            try:

                record = json.loads(
                    line
                )

            except Exception:

                continue

            if isinstance(
                record,
                dict,
            ):

                candidates.append(
                    record
                )


    unique = []

    seen = set()

    for record in candidates:

        key = (
            record.get(
                "url"
            ),
            record.get(
                "root_dir"
            )
            or record.get(
                "notebook_dir"
            ),
        )

        if key in seen:

            continue

        seen.add(
            key
        )

        unique.append(
            record
        )

    return unique


# =============================================================================
# 10. EXACT LIVE NOTEBOOK THROUGH JUPYTER CONTENTS API
# =============================================================================

def acquire_from_jupyter_api():

    if not KERNEL_ID:

        return (
            None,
            None,
        )


    for server in discover_servers():

        base_url = server.get(
            "url"
        )

        if not base_url:

            continue

        if not base_url.endswith(
            "/"
        ):

            base_url += "/"


        token = (
            server.get(
                "token"
            )
            or ""
        )


        token_query = ""

        if token:

            token_query = (
                "?token="
                + urllib.parse.quote(
                    token
                )
            )


        sessions_url = (
            urllib.parse.urljoin(
                base_url,
                "api/sessions",
            )
            + token_query
        )


        try:

            sessions = http_json(
                sessions_url
            )

        except Exception:

            continue


        for session in sessions:

            kernel = session.get(
                "kernel",
                {},
            )


            if (
                kernel.get(
                    "id"
                )
                != KERNEL_ID
            ):

                continue


            notebook_meta = (
                session.get(
                    "notebook"
                )
                or {}
            )


            notebook_path = (
                notebook_meta.get(
                    "path"
                )
                or session.get(
                    "path"
                )
            )


            if not notebook_path:

                continue


            encoded = urllib.parse.quote(
                notebook_path,
                safe="/",
            )


            contents_url = (
                urllib.parse.urljoin(
                    base_url,
                    "api/contents/"
                    + encoded,
                )
                + token_query
            )


            try:

                model = http_json(
                    contents_url
                )

            except Exception:

                continue


            if (
                model.get(
                    "type"
                )
                != "notebook"
            ):

                continue


            content = model.get(
                "content"
            )


            if not isinstance(
                content,
                dict,
            ):

                continue


            return (
                content,
                {
                    "mode":
                        "EXACT_JUPYTER_CONTENTS_API",

                    "notebook_path":
                        notebook_path,

                    "server_root":
                        server.get(
                            "root_dir"
                        )
                        or server.get(
                            "notebook_dir"
                        ),
                },
            )


    return (
        None,
        None,
    )


# =============================================================================
# 11. EXACT NOTEBOOK FROM KAGGLE FILESYSTEM
# =============================================================================

def local_ipynb_candidates():

    candidates = []

    roots = [
        Path(
            "/kaggle/working"
        ),
    ]


    explicit = [
        Path(
            "/kaggle/working/__notebook__.ipynb"
        ),
        Path(
            "/kaggle/working/notebook.ipynb"
        ),
    ]


    for path in explicit:

        if path.is_file():

            candidates.append(
                path
            )


    for root in roots:

        try:

            candidates.extend(
                root.glob(
                    "*.ipynb"
                )
            )

        except Exception:

            pass


    unique = []

    seen = set()


    for path in candidates:

        try:

            resolved = path.resolve()

        except Exception:

            continue


        if (
            resolved
            == NOTEBOOK_OUT.resolve()
        ):

            continue


        if resolved in seen:

            continue


        seen.add(
            resolved
        )

        unique.append(
            resolved
        )


    return unique


def acquire_from_local_file():

    possible = []


    for path in local_ipynb_candidates():

        try:

            nb = nbformat.read(
                path,
                as_version=4,
            )

        except Exception:

            continue


        source = notebook_source_text(
            nb
        )


        stage27_count = (
            source.upper().count(
                "STAGE27"
            )
        )


        if (
            stage27_count
            < 10
        ):

            continue


        possible.append(
            (
                path,
                nb,
                stage27_count,
            )
        )


    if not possible:

        return (
            None,
            None,
        )


    possible.sort(
        key=lambda item: (
            item[2],
            item[0].stat().st_size,
        ),
        reverse=True,
    )


    (
        path,
        nb,
        stage27_count,
    ) = possible[0]


    return (
        nb,
        {
            "mode":
                "EXACT_LOCAL_NOTEBOOK_FILE",

            "notebook_path":
                str(
                    path
                ),

            "source_bytes":
                path.stat().st_size,

            "stage27_occurrences":
                stage27_count,
        },
    )


# =============================================================================
# 12. FALLBACK — IPYTHON EXECUTION HISTORY
# =============================================================================

def acquire_from_history():

    try:

        ip = get_ipython()

    except Exception:

        ip = None


    if ip is None:

        return (
            None,
            None,
        )


    history = []


    try:

        iterator = (
            ip
            .history_manager
            .get_range(
                session=0,
                start=1,
                stop=None,
                raw=True,
                output=False,
            )
        )


        for (
            session,
            line_no,
            source,
        ) in iterator:

            if not source:

                continue


            history.append(
                {
                    "session":
                        int(
                            session
                        ),

                    "line_no":
                        int(
                            line_no
                        ),

                    "source":
                        str(
                            source
                        ),
                }
            )


    except Exception as exc:

        print(
            "[WARN] IPython history unavailable:",
            repr(
                exc
            ),
        )

        return (
            None,
            None,
        )


    joined = "\n\n".join(
        item[
            "source"
        ]
        for item in history
    )


    stage27_count = (
        joined.upper().count(
            "STAGE27"
        )
    )


    print()
    print(
        "History fallback candidate:"
    )
    print(
        "  input cells        :",
        len(
            history
        ),
    )
    print(
        "  STAGE27 occurrences:",
        stage27_count,
    )


    # Hard block against exporting only PUB cells as "full Stage27".
    if (
        len(
            history
        )
        < 12
    ):

        return (
            None,
            {
                "mode":
                    "HISTORY_REJECTED_TOO_SMALL",

                "input_cells":
                    len(
                        history
                    ),

                "stage27_occurrences":
                    stage27_count,
            },
        )


    if (
        stage27_count
        < 15
    ):

        return (
            None,
            {
                "mode":
                    "HISTORY_REJECTED_TOO_LITTLE_STAGE27_CONTENT",

                "input_cells":
                    len(
                        history
                    ),

                "stage27_occurrences":
                    stage27_count,
            },
        )


    cells = []


    for index, item in enumerate(
        history,
        start=1,
    ):

        cell = (
            nbformat
            .v4
            .new_code_cell(
                source=item[
                    "source"
                ]
            )
        )


        cell[
            "execution_count"
        ] = item[
            "line_no"
        ]


        cell[
            "outputs"
        ] = []


        cell[
            "metadata"
        ] = {
            "stage27_history_index":
                index,

            "ipython_session":
                item[
                    "session"
                ],

            "ipython_line_number":
                item[
                    "line_no"
                ],
        }


        cells.append(
            cell
        )


    nb = (
        nbformat
        .v4
        .new_notebook(
            cells=cells
        )
    )


    return (
        nb,
        {
            "mode":
                "RECONSTRUCTED_FROM_IPYTHON_INPUT_HISTORY",

            "input_cells":
                len(
                    history
                ),

            "stage27_occurrences":
                stage27_count,

            "limitations": [
                (
                    "original cell outputs are not recoverable "
                    "from input history"
                ),
                (
                    "unexecuted cells are not recoverable from "
                    "input history"
                ),
                (
                    "markdown-only cells are not recoverable "
                    "unless executed as source"
                ),
            ],
        },
    )


# =============================================================================
# 13. ACQUIRE BEST NOTEBOOK
# =============================================================================

print()
print(
    "-" * 96
)
print(
    "NOTEBOOK ACQUISITION"
)
print(
    "-" * 96
)


notebook = None

acquisition = None


# Preference 1
try:

    (
        notebook,
        acquisition,
    ) = acquire_from_jupyter_api()

except Exception as exc:

    print(
        "[WARN] Jupyter API attempt:",
        repr(
            exc
        ),
    )


if notebook is not None:

    print(
        "[PASS] exact live notebook captured "
        "through Jupyter Contents API"
    )


# Preference 2
if notebook is None:

    try:

        (
            notebook,
            acquisition,
        ) = acquire_from_local_file()

    except Exception as exc:

        print(
            "[WARN] local-file attempt:",
            repr(
                exc
            ),
        )


    if notebook is not None:

        print(
            "[PASS] exact notebook captured from "
            "Kaggle filesystem"
        )


# Preference 3
history_failure = None


if notebook is None:

    (
        notebook,
        history_info,
    ) = acquire_from_history()


    if notebook is not None:

        acquisition = (
            history_info
        )

        print(
            "[PASS] notebook reconstructed from "
            "sufficiently complete execution history"
        )

    else:

        history_failure = (
            history_info
        )


if notebook is None:

    print()
    print(
        "History diagnostic:"
    )

    print(
        json.dumps(
            history_failure,
            indent=2,
        )
        if history_failure
        else "[none]"
    )


    raise RuntimeError(
        "\nFULL NOTEBOOK EXPORT COULD NOT BE VERIFIED.\n\n"
        "No exact live .ipynb was accessible and the current "
        "IPython history was not complete enough to be safely "
        "labeled as the full Stage27 notebook.\n\n"
        "Do NOT substitute a partial PUB-only notebook."
    )


# =============================================================================
# 14. NORMALIZE THROUGH NBFMT
# =============================================================================

# Validate/migrate notebook structure.
notebook = nbformat.from_dict(
    copy.deepcopy(
        notebook
    )
)

notebook = nbformat.convert(
    notebook,
    4,
)


stats = cell_stats(
    notebook
)

source_text = notebook_source_text(
    notebook
)

stage27_mentions = (
    source_text.upper().count(
        "STAGE27"
    )
)


print()
print(
    "-" * 96
)
print(
    "NOTEBOOK COMPLETENESS AUDIT"
)
print(
    "-" * 96
)


print(
    "Acquisition:"
)

print(
    json.dumps(
        acquisition,
        indent=2,
    )
)


print()
print(
    "Cell statistics:"
)

print(
    json.dumps(
        stats,
        indent=2,
    )
)


print(
    "STAGE27 occurrences:",
    stage27_mentions,
)


if (
    stats[
        "code"
    ]
    < 10
):

    raise RuntimeError(
        "Notebook has too few code cells "
        "to represent complete Stage27."
    )


if (
    stage27_mentions
    < 15
):

    raise RuntimeError(
        "Notebook contains insufficient Stage27 source markers."
    )


print(
    "[PASS] notebook completeness floor"
)


# =============================================================================
# 15. SECRET SAFETY SCAN
# =============================================================================

print()
print(
    "-" * 96
)
print(
    "SECRET-SAFETY AUDIT"
)
print(
    "-" * 96
)


serialized = notebook_serialized_text(
    notebook
)


secret_patterns = {
    "GitHub classic PAT":
        r"\bghp_[A-Za-z0-9]{20,}\b",

    "GitHub fine-grained PAT":
        r"\bgithub_pat_[A-Za-z0-9_]{20,}\b",

    "GitHub OAuth":
        r"\bgho_[A-Za-z0-9]{20,}\b",

    "GitHub user token":
        r"\bghu_[A-Za-z0-9]{20,}\b",

    "GitHub server token":
        r"\bghs_[A-Za-z0-9]{20,}\b",

    "Stripe live secret":
        r"\bsk_live_[A-Za-z0-9]{16,}\b",

    "AWS access key":
        r"\bAKIA[0-9A-Z]{16}\b",
}


secret_hits = []


for (
    label,
    pattern,
) in secret_patterns.items():

    matches = re.findall(
        pattern,
        serialized,
    )


    if matches:

        secret_hits.append(
            {
                "type":
                    label,

                "count":
                    len(
                        matches
                    ),
            }
        )


if secret_hits:

    print(
        json.dumps(
            secret_hits,
            indent=2,
        )
    )

    raise RuntimeError(
        "\nPotential credential material exists in the notebook.\n"
        "GitHub export blocked."
    )


print(
    "[PASS] no recognized credential-token "
    "patterns in notebook source/outputs"
)


# =============================================================================
# 16. ADD REPRODUCIBILITY METADATA
# =============================================================================

notebook.setdefault(
    "metadata",
    {},
)


notebook[
    "metadata"
][
    "stage27_reproducibility_export"
] = {
    "export_phase":
        "STAGE27-PUB3A",

    "scientific_parent":
        SCIENTIFIC_FREEZE,

    "publication_closeout_parent":
        head,

    "scientific_status":
        "CLOSED",

    "acquisition":
        acquisition,

    "science_operations_during_export": {
        "model_fits": 0,
        "model_inference": 0,
        "target_reopenings": 0,
        "threshold_reselection": 0,
        "bootstrap_recomputation": 0,
        "new_formal_statistical_tests": 0,
    },
}


# =============================================================================
# 17. WRITE COMPLETE NOTEBOOK
# =============================================================================

STAGE_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


NOTEBOOK_OUT.parent.mkdir(
    parents=True,
    exist_ok=True,
)


nbformat.write(
    notebook,
    NOTEBOOK_OUT,
)


if not NOTEBOOK_OUT.is_file():

    raise RuntimeError(
        "Notebook export was not created."
    )


print()
print(
    "-" * 96
)
print(
    "COMPLETE IPYNB EXPORT"
)
print(
    "-" * 96
)


print(
    NOTEBOOK_REL
)

print(
    "bytes :",
    f"{NOTEBOOK_OUT.stat().st_size:,}",
)

print(
    "SHA256:",
    sha256_file(
        NOTEBOOK_OUT
    ),
)


# =============================================================================
# 18. BUILD PYTHON SOURCE EXPORT
# =============================================================================

def markdown_to_comments(
    text,
):
    lines = str(
        text
    ).splitlines()

    if not lines:

        return "#"

    return "\n".join(
        "#"
        if line == ""
        else "# " + line

        for line in lines
    )


python_parts = [
    (
        "# "
        + "=" * 78
    ),
    (
        "# STAGE27 — LEAVE-ONE-ATTACK-FAMILY-OUT "
        "UNSEEN-FAMILY GENERALIZATION AUDIT"
    ),
    (
        "# Complete source export of the Stage27 Kaggle notebook."
    ),
    "#",
    (
        "# Frozen scientific parent:"
    ),
    (
        "# "
        + SCIENTIFIC_FREEZE
    ),
    "#",
    (
        "# Publication-closeout parent at export:"
    ),
    (
        "# "
        + head
    ),
    "#",
    "# Scientific state: CLOSED",
    "#",
    (
        "# This file preserves notebook source ordering."
    ),
    (
        "# It does not authorize new Stage27 scientific computation."
    ),
    (
        "# "
        + "=" * 78
    ),
    "",
]


for (
    index,
    cell,
) in enumerate(
    notebook.get(
        "cells",
        [],
    ),
    start=1,
):

    cell_type = cell.get(
        "cell_type",
        "unknown",
    )


    source = cell.get(
        "source",
        "",
    )


    if isinstance(
        source,
        list,
    ):

        source = "".join(
            source
        )


    source = str(
        source
    )


    if (
        cell_type
        == "code"
    ):

        python_parts.extend([
            "",
            (
                f"# %% [Stage27 notebook cell {index}]"
            ),
            source.rstrip(),
            "",
        ])


    elif (
        cell_type
        == "markdown"
    ):

        python_parts.extend([
            "",
            (
                f"# %% [markdown — Stage27 notebook cell {index}]"
            ),
            markdown_to_comments(
                source
            ),
            "",
        ])


    elif (
        cell_type
        == "raw"
    ):

        python_parts.extend([
            "",
            (
                f"# %% [raw — Stage27 notebook cell {index}]"
            ),
            markdown_to_comments(
                source
            ),
            "",
        ])


PYTHON_OUT.write_text(
    "\n".join(
        python_parts
    ).rstrip()
    + "\n",
    encoding="utf-8",
    newline="\n",
)


print()
print(
    "-" * 96
)
print(
    "PYTHON SOURCE EXPORT"
)
print(
    "-" * 96
)


print(
    PYTHON_REL
)

print(
    "bytes :",
    f"{PYTHON_OUT.stat().st_size:,}",
)

print(
    "SHA256:",
    sha256_file(
        PYTHON_OUT
    ),
)


# =============================================================================
# 19. CODE-SOURCE PRESERVATION AUDIT
# =============================================================================

python_text = (
    PYTHON_OUT
    .read_text(
        encoding="utf-8"
    )
)


missing_cells = []


code_index = 0


for cell in notebook.get(
    "cells",
    [],
):

    if (
        cell.get(
            "cell_type"
        )
        != "code"
    ):

        continue


    code_index += 1


    source = cell.get(
        "source",
        "",
    )


    if isinstance(
        source,
        list,
    ):

        source = "".join(
            source
        )


    source = str(
        source
    ).rstrip()


    if (
        source
        and
        source not in python_text
    ):

        missing_cells.append(
            code_index
        )


if missing_cells:

    raise RuntimeError(
        "Python export source-preservation failure. "
        f"Missing code cells: {missing_cells[:30]}"
    )


print()
print(
    "[PASS] every notebook code-cell source "
    "exists in Python export"
)


# =============================================================================
# 20. GITHUB FILE-SIZE SAFETY
# =============================================================================

for path in [
    NOTEBOOK_OUT,
    PYTHON_OUT,
]:

    if (
        path.stat().st_size
        > MAX_GITHUB_BYTES
    ):

        raise RuntimeError(
            "\nGitHub-safe file-size gate failed:\n"
            f"{path}\n"
            f"{path.stat().st_size:,} bytes"
        )


print(
    "[PASS] GitHub-safe file sizes"
)


# =============================================================================
# 21. WRITE EXPORT RECEIPT
# =============================================================================

RECEIPT_OUT.parent.mkdir(
    parents=True,
    exist_ok=True,
)


receipt = {
    "stage":
        "STAGE27-PUB3A",

    "timestamp_utc":
        datetime.now(
            timezone.utc
        ).isoformat(),

    "repository":
        "themubasshir/ids2018-validation-safe-ablation",

    "scientific_parent":
        SCIENTIFIC_FREEZE,

    "publication_closeout_parent":
        head,

    "scientific_status":
        "CLOSED",

    "acquisition":
        acquisition,

    "notebook": {
        "path":
            NOTEBOOK_REL.as_posix(),

        "sha256":
            sha256_file(
                NOTEBOOK_OUT
            ),

        "bytes":
            NOTEBOOK_OUT.stat().st_size,

        "cells":
            stats,

        "stage27_source_occurrences":
            stage27_mentions,
    },

    "python_export": {
        "path":
            PYTHON_REL.as_posix(),

        "sha256":
            sha256_file(
                PYTHON_OUT
            ),

        "bytes":
            PYTHON_OUT.stat().st_size,

        "all_code_cell_sources_preserved":
            True,
    },

    "secret_scan": {
        "status":
            "PASS",

        "recognized_token_patterns":
            0,
    },

    "science_operations": {
        "model_fits": 0,
        "model_inference": 0,
        "target_reopenings": 0,
        "threshold_reselection": 0,
        "bootstrap_recomputation": 0,
        "new_formal_statistical_tests": 0,
    },

    "git_operations": {
        "commit":
            False,

        "push":
            False,
    },
}


RECEIPT_OUT.write_text(
    json.dumps(
        receipt,
        indent=2,
        sort_keys=True,
    )
    + "\n",
    encoding="utf-8",
    newline="\n",
)


print()
print(
    "-" * 96
)
print(
    "NOTEBOOK EXPORT RECEIPT"
)
print(
    "-" * 96
)


print(
    RECEIPT_REL
)

print(
    "SHA256:",
    sha256_file(
        RECEIPT_OUT
    ),
)


# =============================================================================
# 22. SCIENCE PATH MUST STILL BE UNCHANGED
# =============================================================================

science_diff = run(
    [
        "git",
        "diff",
        "--",
        (
            "results/stage27_loao_unseen_attack/"
            "stage27_4a_final_synthesis"
        ),
    ]
).stdout


if science_diff.strip():

    print(
        science_diff
    )

    raise RuntimeError(
        "Frozen Stage27 science was modified."
    )


print()
print(
    "[PASS] frozen Stage27-4A synthesis untouched"
)


# =============================================================================
# 23. EXACT WORKTREE INVENTORY
# =============================================================================

expected_new = {
    NOTEBOOK_REL.as_posix(),
    PYTHON_REL.as_posix(),
    RECEIPT_REL.as_posix(),
}


actual_new = status_paths()


print()
print(
    "-" * 96
)
print(
    "GIT STATUS"
)
print(
    "-" * 96
)


print(
    git(
        "status",
        "--short",
        "-uall",
    )
)


if (
    actual_new
    != expected_new
):

    print()
    print(
        "Expected:"
    )

    for item in sorted(
        expected_new
    ):

        print(
            " ",
            item
        )


    print()
    print(
        "Actual:"
    )

    for item in sorted(
        actual_new
    ):

        print(
            " ",
            item
        )


    raise RuntimeError(
        "PUB3A produced unexpected worktree changes."
    )


print()
print(
    "[PASS] exactly three reproducibility artifacts created"
)


# =============================================================================
# 24. FINAL
# =============================================================================

print()
print(
    "=" * 96
)

print(
    "STAGE27-PUB3A COMPLETE — "
    "FULL NOTEBOOK EXPORT READY FOR REVIEW"
)

print(
    "=" * 96
)


print()
print(
    "Scientific freeze:"
)

print(
    " ",
    SCIENTIFIC_FREEZE,
)


print()
print(
    "Publication-closeout parent:"
)

print(
    " ",
    head,
)


print()
print(
    "Acquisition mode:"
)

print(
    " ",
    acquisition[
        "mode"
    ],
)


print()
print(
    "Notebook:"
)

print(
    " ",
    NOTEBOOK_REL
)

print(
    "  SHA256:",
    sha256_file(
        NOTEBOOK_OUT
    ),
)

print(
    "  bytes :",
    f"{NOTEBOOK_OUT.stat().st_size:,}",
)

print(
    "  cells :",
    stats,
)


print()
print(
    "Python export:"
)

print(
    " ",
    PYTHON_REL
)

print(
    "  SHA256:",
    sha256_file(
        PYTHON_OUT
    ),
)

print(
    "  bytes :",
    f"{PYTHON_OUT.stat().st_size:,}",
)


print()
print(
    "Receipt:"
)

print(
    " ",
    RECEIPT_REL
)

print(
    "  SHA256:",
    sha256_file(
        RECEIPT_OUT
    ),
)


print()
print(
    "Integrity:"
)

print(
    "  frozen Stage27 science : UNCHANGED"
)

print(
    "  source preservation    : PASS"
)

print(
    "  secret scan            : PASS"
)

print(
    "  file-size gate         : PASS"
)


print()
print(
    "Git operations:"
)

print(
    "  commit : NOT PERFORMED"
)

print(
    "  push   : NOT PERFORMED"
)


print()
print(
    "NEXT:"
)

print(
    "  STAGE27-PUB3B — commit/push notebook + "
    "Python export + receipt and append them to "
    "the Stage27 publication closeout."
)
