# Stage20-1C16-A-DU1 — D-Cohort Changed-Position Forensic

## Status

**DIAGNOSTIC ONLY — NO RULE CHANGE**

Parent commit:

`b0ebf4bf7b89ebf6569c56f1b027a2b0128e0297`

## Frozen scientific state

- population: **675**
- D5 exact: **635/675**
- V1 exact: **318/675**
- A: **295**
- B: **340**
- C: **23**
- D: **17**

## D membership

`[14, 25, 35, 36, 52, 123, 199, 307, 309, 324, 327, 333, 334, 336, 337, 471, 473]`

The D membership remains exactly:

- 14 remaining TCP length residuals
- duration/export cases **471** and **473**
- protocol-0 anchor **199**

No cohort membership was changed.

## Actual changed-position union

Current source-faithful runtime:

`[9, 10, 11, 12, 14]`

Earlier internal expected union:

`[9, 10, 12, 13, 14]`

Match:

**False**

## Changed-position counts

`{9: 14, 10: 12, 11: 2, 12: 12, 14: 11}`

## Pattern populations

- `[]`: **1** flows — `[199]`
- `[10, 14]`: **2** flows — `[52, 123]`
- `[9, 10, 12]`: **1** flows — `[36]`
- `[9, 10, 12, 14]`: **9** flows — `[14, 25, 35, 309, 324, 327, 333, 336, 337]`
- `[9, 11]`: **2** flows — `[471, 473]`
- `[9, 12]`: **2** flows — `[307, 334]`

## Per-flow D audit

| Index | Protocol | Termination | Duration µs | Changed positions |
|---:|---:|---|---:|---|
| 14 | 6 | FIN | 18378 | `[9, 10, 12, 14]` |
| 25 | 6 | FIN | 77033 | `[9, 10, 12, 14]` |
| 35 | 6 | FIN | 3536 | `[9, 10, 12, 14]` |
| 36 | 6 | FIN | 519267 | `[9, 10, 12]` |
| 52 | 6 | FIN | 15745 | `[10, 14]` |
| 123 | 6 | FIN | 2489 | `[10, 14]` |
| 199 | 0 | FLOW_TIMEOUT | 114364596 | `[]` |
| 307 | 6 | FIN | 862 | `[9, 12]` |
| 309 | 6 | FIN | 3312046 | `[9, 10, 12, 14]` |
| 324 | 6 | FIN | 1340800 | `[9, 10, 12, 14]` |
| 327 | 6 | FIN | 7681758 | `[9, 10, 12, 14]` |
| 333 | 6 | FIN | 570 | `[9, 10, 12, 14]` |
| 334 | 6 | FIN | 846 | `[9, 12]` |
| 336 | 6 | FIN | 78550 | `[9, 10, 12, 14]` |
| 337 | 6 | FIN | 3594274 | `[9, 10, 12, 14]` |
| 471 | 6 | FIN | 224 | `[9, 11]` |
| 473 | 6 | FIN | 262 | `[9, 11]` |

## Interpretation

This checkpoint does **not** alter:

- D5 classification
- V1 TCP payload semantics
- reconstructed signatures
- transition membership
- lifecycle logic
- exact matching

It exists solely because the previous C16-A recovery attempted to enforce
an older internal D-cohort position-union assertion that the current
source-faithful runtime did not satisfy.

## Artifact

`results/stage20_1c16_runtime_recovery/stage20_1c16a_d_cohort_union_forensic.json`

SHA256:

`862fa0203122c2e03da2c8de6da0bf484d56dcd6dc461dab9512fdbcfb0733ea`

## Holdout integrity

- Friday requests: **0**
- Friday reads: **0**
- Friday openings: **0/1**
- Friday status: **CLOSED**
