# Stage27-0A — Family × Day Feasibility Audit

**Status:** COMPLETE — ZERO FIT / ZERO INFERENCE FEASIBILITY AUDIT  
**Execution parent:** `e47f44751bc71d219c5d0f3b3fca06d62037fb8b`  
**Primary compute policy:** CPU, GPU budget = 0 hours  
**Created:** 2026-08-20T17:05:29.087454+00:00

## Scientific purpose

Stage27-0A determines which chronology-first unseen-family folds are structurally
possible **before** any Stage27 model results exist.

The originally proposed universal geometry was:

```text
Monday–Wednesday -> TRAIN
Thursday         -> VALIDATION
Friday           -> HELD-OUT FAMILY TARGET
```

That geometry is **not feasible for all seven families** because CICIDS2017 attack
families occur on different weekdays.

## Population decision

Stage27-0A uses the **full Stage24 CICIDS2017 effective target population** as the
family-support source.

This is deliberate. The committed Stage20 compact raw-byte release corpora preserve
exact raw-byte flows but persist only:

```text
encoded_bytes.bin
flow_offsets.npy
labels.npy
packet_lengths.npy
```

and the manifest join counts are binary `0/1`. No durable attack-family label array is
present. Therefore the Stage20 compact corpus remains valid for the Stage20 binary
raw-byte experiment, but it is **not** a durable seven-family membership source for
Stage27 LOAO construction.

No release archive was downloaded or recreated during Stage27-0A.

## Frozen seven-family taxonomy

```text
BOT
DDOS
DOS
AUTH_BRUTE_FORCE
INFILTRATION
PORT_SCAN
WEB_ATTACK
```

`heartbleed` remains `TARGET_ONLY_UNSEEN` and is excluded from the seven-family
primary matrix.

## Exact family × weekday support

| Family | Mon | Tue | Wed | Thu | Fri | Total |
|---|---:|---:|---:|---:|---:|---:|
| BOT | 0 | 0 | 0 | 0 | 1,966 | 1,966 |
| DDOS | 0 | 0 | 0 | 0 | 128,027 | 128,027 |
| DOS | 0 | 0 | 252,661 | 0 | 0 | 252,661 |
| AUTH_BRUTE_FORCE | 0 | 13,835 | 0 | 0 | 0 | 13,835 |
| INFILTRATION | 0 | 0 | 0 | 36 | 0 | 36 |
| PORT_SCAN | 0 | 0 | 0 | 0 | 158,930 | 158,930 |
| WEB_ATTACK | 0 | 0 | 0 | 2,180 | 0 | 2,180 |

Seven-family total: **557,635**

Heartbleed excluded from the primary seven-family matrix: **11**

All non-benign rows including Heartbleed: **557,646**

## Benign support by weekday

| Day | Benign support |
|---|---:|
| Monday | 529,918 |
| Tuesday | 432,074 |
| Wednesday | 440,031 |
| Thursday | 456,752 |
| Friday | 414,322 |
| **TOTAL** | **2,273,097** |

## Original geometry decision

The universal Mon–Wed / Thu / Fri seven-fold geometry is **STRUCTURALLY INFEASIBLE**.

Only the three Friday families — BOT, DDOS and PORT_SCAN — have positive target support
on Friday. DOS appears only Wednesday, AUTH_BRUTE_FORCE only Tuesday, and
INFILTRATION/WEB_ATTACK only Thursday.

The original geometry is therefore rejected **before model fitting**. This is a
feasibility correction, not result-driven adaptation.

## Day-atomic chronology-first feasibility

Stage27-0A applies the following feasibility rule:

```text
TRAIN < VALIDATION < TARGET
```

using weekday-atomic partitions. An executable fold additionally requires:

- zero held-out-family positives in TRAIN;
- zero held-out-family positives in VALIDATION;
- benign and at least one known-family attack positive in TRAIN;
- benign and at least one known-family attack positive in VALIDATION;
- same-target-day benign support for the primary isolation target.

| Family | Target day | Positive support | Stage27-0A status | Corrected geometry |
|---|---|---:|---|---|
| BOT | Friday | 1,966 | ELIGIBLE | Monday,Tuesday,Wednesday → Thursday → Friday |
| DDOS | Friday | 128,027 | ELIGIBLE | Monday,Tuesday,Wednesday → Thursday → Friday |
| DOS | Wednesday | 252,661 | STRUCTURALLY_INELIGIBLE | — |
| AUTH_BRUTE_FORCE | Tuesday | 13,835 | STRUCTURALLY_INELIGIBLE | — |
| INFILTRATION | Thursday | 36 | ELIGIBLE_DESCRIPTIVE_ONLY | Monday,Tuesday → Wednesday → Thursday |
| PORT_SCAN | Friday | 158,930 | ELIGIBLE | Monday,Tuesday,Wednesday → Thursday → Friday |
| WEB_ATTACK | Thursday | 2,180 | ELIGIBLE | Monday,Tuesday → Wednesday → Thursday |

### Structurally ineligible

- **AUTH_BRUTE_FORCE** — first appears Tuesday. There are not two earlier weekday
  partitions for separate day-atomic TRAIN and VALIDATION, and Monday has no attack
  positives.
- **DOS** — first appears Wednesday. The only day-atomic split is Monday TRAIN /
  Tuesday VALIDATION / Wednesday TARGET, but Monday contains no known attack positives,
  so a supervised binary IDS cannot be trained honestly under that geometry.

These families are retained in the taxonomy and marked
`STRUCTURALLY_INELIGIBLE`; they are not silently dropped.

### Eligible but descriptive-only

- **INFILTRATION** has only **36** positives, below the preregistered recommended
  inferential support threshold of 50. It remains eligible for execution but must be
  marked `DESCRIPTIVE_ONLY`.

## Important semantic limit for Stage27-0

Because chronology is primary, some non-held-out attack families may occur only on or
after a fold's target day and therefore may also be absent from training.

Stage27-0 should therefore describe the executable design precisely as a:

> **chronology-first zero-training-exposure family audit**

and should not imply that every non-held-out family is necessarily represented in
training for every fold.

## Stage27-0A result

```text
Eligible folds:             5
Structurally ineligible:    2
Descriptive-only eligible:  1
Stage27 model fits:         0
Stage27 model inference:    0
GPU execution:              NO
```

Eligible families:

```text
BOT
DDOS
INFILTRATION   [DESCRIPTIVE_ONLY]
PORT_SCAN
WEB_ATTACK
```

Structurally ineligible families:

```text
AUTH_BRUTE_FORCE
DOS
```

## Next gate

Stage27-0 protocol construction is authorized **only after this Stage27-0A artifact
set is committed and the remote `main` SHA is verified**.

This script performs that commit/push/remote verification and then stops. It does not
construct Stage27-0.
