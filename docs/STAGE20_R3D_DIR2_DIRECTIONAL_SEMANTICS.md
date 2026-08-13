# Stage20-R3D-DIR2 — Directional Semantics Diagnostic

## Status

**DIAGNOSTIC ONLY — NO SCIENTIFIC RULE CHANGE**

Parent HEAD before this checkpoint:

`88f2c182764795785b29fb02b80056f9157b211c`

## Current runtime result

The source-faithful reconstruction currently produces the following
zero-based S4 changed-position counts under frozen TCP payload V1:

| S4 position | Current | Earlier internal vector | Delta |
|---:|---:|---:|---:|
| 9  | 354 | 352 | +2 |
| 10 | 202 | 204 | -2 |
| 11 | 153 | 151 | +2 |
| 12 | 135 | 135 | 0 |
| 13 | 44  | 46  | -2 |
| 14 | 62  | 64  | -2 |

Current changed-field total: **950**

Earlier internal-vector total: **952**

## Pattern diagnostic

Changed-position pattern `(9, 11, 12)`:

- count: **90**
- indices: `[0, 1, 2, 3, 4, 5, 6, 7, 30, 33, 80, 81, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 206, 242, 312, 313, 330, 371, 373, 383, 386, 388, 390, 440, 479, 482, 496, 509, 536, 537, 539, 542, 553, 554, 556, 567, 578, 604, 607, 609, 611, 613, 615, 626, 627, 637, 638, 653, 659, 664, 665, 666, 668, 670, 672]`

Changed-position pattern `(10, 12, 13, 14)`:

- count: **0**

## Historical timeout-constructor orientation diagnostic

Changed flows whose first retained packet source differs from the
final stored BasicFlow source orientation:

`[471, 473]`

Count: **2**

Intersection with the `(9, 11, 12)` population:

`[]`

Therefore the earlier hypothesis that exactly two timeout-replacement
flows explain the aggregate changed-position discrepancy is **not
supported**.

No reconstruction rule is changed at this checkpoint.

## Major runtime checkpoints

- raw historical exact S4: **637/675**
- D5 source-faithful accepted: **637/675**
- V1 exact S4: **318/675**

## Artifact

`results/stage20_1c16_runtime_recovery/stage20_r3d_dir2_directional_semantics.json`

SHA256:

`e8631b7eb82b60b028d7bb22218d673c0d209501b2f4dd55eaa54c785ed5823d`

## Holdout integrity

- Friday requests: **0**
- Friday reads: **0**
- Friday openings: **0/1**
- Friday status: **CLOSED**
