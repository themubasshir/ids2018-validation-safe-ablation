# Stage22 Cross-Role Exact Duplicate Sanitization

## Status

**SEALED BEFORE LABEL READING AND BEFORE MODEL EXECUTION**

Scientific parent:

`d25fb074b8967d1c653934bb55ec6eece3e4b191`

Stage22-1F chronological partition lock SHA256:

`f80e74a6d0a67152fe4eac9f6acb33e80096f7f9ae3d59c2f5cde0d07ad428f6`

Stage22-1E exact 70-feature duplicate mapping SHA256:

`44b6ec8393998e6c843e8943e6a12a0940a183c6e6a9eed2de2bb1274f73fc08`

## Frozen rule

The role ordering is:

1. Development
2. Validation
3. Final test

For an exact frozen 70-feature fingerprint appearing in more than one
eligible chronological role, Stage22 retains **all occurrences in the earliest
eligible role** and excludes **all occurrences from every later role**.

Within-role duplicates remain.

Rows already excluded because of ambiguous source-day provenance do not
participate in choosing the earliest eligible role and remain excluded.

## Cross-role groups before sanitization

- Eligible exact groups: **217,071**
- Single-role exact groups: **217,071**
- Cross-role exact groups: **0**

No exact group crossed chronological roles before sanitization.

## Row counts

### Before duplicate sanitization

- Development: **156,821**
- Validation: **15,245**
- Final test: **68,867**
- Ambiguous provenance excluded: **59,995**

### New duplicate exclusions

- Development: **0**
- Validation: **0**
- Final test: **0**
- Total: **0**

### After duplicate sanitization

- Development: **156,821**
- Validation: **15,245**
- Final test: **68,867**
- Total excluded: **59,995**

## Frozen-day audit

| Capture day | Before | Duplicate excluded | Retained |
|---|---:|---:|---:|
| 2018-02-14 | 18,813 | 0 | 18,813 |
| 2018-02-15 | 35,664 | 0 | 35,664 |
| 2018-02-16 | 29,783 | 0 | 29,783 |
| 2018-02-21 | 39,962 | 0 | 39,962 |
| 2018-02-22 | 15,721 | 0 | 15,721 |
| 2018-02-23 | 16,878 | 0 | 16,878 |
| 2018-02-28 | 15,245 | 0 | 15,245 |
| 2018-03-01 | 30,737 | 0 | 30,737 |
| 2018-03-02 | 38,130 | 0 | 38,130 |

## Exact leakage invariant after sanitization

- Development vs Validation exact-group overlap: **0**
- Development vs Final-test exact-group overlap: **0**
- Validation vs Final-test exact-group overlap: **0**

The Stage22 exact cross-role duplicate leakage invariant therefore passes.

## Chronology remains immutable

Development remains:

- `2018-02-14`
- `2018-02-15`
- `2018-02-16`
- `2018-02-21`
- `2018-02-22`
- `2018-02-23`

Validation remains:

- `2018-02-28`

Final test remains:

- `2018-03-01`
- `2018-03-02`

No frozen usable capture day became empty after duplicate sanitization.

## Sanitized membership artifact

`results/stage22_temporal_session_safe/stage22_1g_sanitized_chronological_partition.parquet`

SHA256:

`d1c4b3536ab317b11e9288e0f2eb9b4883635eddb06f77e8e4cc9c4ae964cc9c`

Summary SHA256:

`fa27a742141a144780fcc90cbec2d103eec69f71397cfaba3daa97a11651cb1d`

Scientific seal SHA256:

`04ec2533bffacb206f467f98bef717069b0dcc91c90198c50b3f024145314b6a`

## Outcome governance

Stage22-1G did not read `Label`, `binary_label`, the flagship predictor matrix,
model scores, or any final-test outcome.

No preprocessing was fit.

No model was trained.

No threshold was selected.

No validation or final-test metric was computed.

Authorized Stage22 final-outcome openings consumed: **0**.
