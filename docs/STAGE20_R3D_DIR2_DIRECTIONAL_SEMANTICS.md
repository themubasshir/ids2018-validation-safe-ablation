# Stage20-R3D-DIR2 — Directional Semantics Diagnostic

## Status

**DIAGNOSTIC ONLY — NO SCIENTIFIC RULE CHANGE**

## Persistence correction

Commit `8c531ae8da941e2dc928689215bfbeb225544dce` correctly preserved the DIR2 directional
diagnostic, but its generated population summary incorrectly recorded
D5 source-faithful accepted membership as 637/675.

That persistence-layer statement is corrected here.

The scientific distinction is:

- raw historical C9/C11 exact S4 membership: **637/675**
- D5 source-faithful accepted membership: **635/675**
- V1 exact S4 membership: **318/675**

D5 reclassifies reconstructed flow indices **471** and **473** as
duration/export inconsistencies. Their reconstructed signatures are not
modified and no label duration is substituted.

## D5 -> V1 transition matrix

- exact -> exact: **295**
- exact -> absent: **340**
- absent -> exact: **23**
- absent -> absent: **17**

## Directional diagnostic

Current zero-based S4 changed-position counts:

| Position | Count |
|---:|---:|
| 9 | 354 |
| 10 | 202 |
| 11 | 153 |
| 12 | 135 |
| 13 | 44 |
| 14 | 62 |

Changed signatures: **379**

Changed-field total: **950**

The `(9, 11, 12)` pattern occurs in **90** flows.

Changed flows whose first retained packet source differs from final
stored BasicFlow source orientation:

`[471, 473]`

Their intersection with the `(9, 11, 12)` population is empty.

Therefore the earlier two-flow directional hypothesis remains
**unsupported**.

No payload rule, lifecycle rule, matching rule, or label value is
changed by this diagnostic.

## Machine-readable artifact

`results/stage20_1c16_runtime_recovery/stage20_r3d_dir2_directional_semantics.json`

SHA256:

`a6e528bd7b4643d66699e104ad7ba6144ba4bd642e18b47f5c031a169946054e`

## Holdout integrity

- Friday requests: **0**
- Friday reads: **0**
- Friday openings: **0/1**
- Friday status: **CLOSED**
