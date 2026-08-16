# Stage22 70-Feature Exact Duplicate Group Evidence

## Status

**SEALED BEFORE CHRONOLOGICAL ROLE ASSIGNMENT AND BEFORE DUPLICATE EXCLUSION**

Scientific parent:

`e8ba6e6f990e187cca2d2f7a428c6186a9c115bc`

Stage22-1D provenance evidence seal:

`6d2f40d1915e131ceffca723848f5270a9ee8887acb13fe035a0d8c86d27b8b8`

## Frozen duplicate identity

Exact duplicate membership is defined exclusively on the frozen
Stage15/Stage16 **70-predictor** input vector.

The representation is:

- `pandas.to_numeric(errors='coerce')`;
- IEEE-754 float64;
- signed zero canonicalized to `+0.0`;
- no rounding;
- no tolerance;
- no fuzzy matching;
- no imputation.

A pandas 64-bit row hash is only a lookup accelerator.

Every group assignment was confirmed using complete exact 70-vector equality.

The SHA256 vector digest stored in the evidence is an audit identity only.

Neither labels nor provenance participate in duplicate-group identity.

## Result

- Physical flagship rows: **300,928**
- Distinct exact 70-feature groups: **240,546**
- Singleton groups: **233,661**
- Duplicate groups: **6,885**
- Rows in duplicate groups: **67,267**
- Repeated rows beyond first member: **60,382**
- Largest exact group: **17,265 rows**
- 64-bit accelerator collision buckets: **0**
- SHA256 audit digest collisions: **0**

## Evidence

Row-to-group mapping:

`results/stage22_temporal_session_safe/stage22_1e_70_feature_duplicate_groups.parquet`

SHA256:

`44b6ec8393998e6c843e8943e6a12a0940a183c6e6a9eed2de2bb1274f73fc08`

Summary:

`results/stage22_temporal_session_safe/stage22_1e_70_feature_duplicate_group_summary.json`

SHA256:

`590989f18525ed0b8f4450c616c75b85c04d6bf1ce3a4388b7ee9011bda26b7d`

Evidence seal SHA256:

`1db4e574b1b6c858152b9977c0dcb206dac46cd8110ef465ff332803a9b3bc00`

## Governance

Stage22-1E did **not**:

- read `Label`;
- read `binary_label`;
- use capture-day provenance to create groups;
- construct development/validation/final roles;
- exclude duplicate rows;
- fit preprocessing;
- train models;
- run inference;
- select thresholds;
- compute validation metrics;
- compute final-test metrics.

## Next methodological boundary

The exact duplicate structure is now frozen independently of partition roles.

The next Stage22 step must resolve the deterministic meaning of a
**usable capture day** and construct the chronology using only the already
sealed provenance evidence and the frozen protocol.

Only after those roles exist may the already-preregistered rule be applied:

> retain occurrences in the earliest chronological role and exclude
> occurrences from every later role.

The `2018-02-20` zero-unique-row observation remains unresolved here.
Stage22-1E does not use it to assign any role.
