# Stage22 Provenance Recovery Evidence

## Status

**SEALED AFTER EXACT PROVENANCE RECOVERY AND BEFORE ROLE ASSIGNMENT**

Scientific parent:

`8c005468e99d30c11f7d8930b2cb786f180366bb`

Stage22-1B frozen provenance procedure SHA256:

`2966b0cf2a197fefdd7eda1fda3bac665a3581c182eccab917bc2775b553a061`

## Exact Stage22-1C evidence

Row provenance mapping:

`results/stage22_temporal_session_safe/stage22_1c_row_provenance.parquet`

SHA256:

`b00ae439254a7aa5f6e1a0fb715339be26df229ad65af26dc102c28b25b0ce6e`

Runtime provenance summary:

`results/stage22_temporal_session_safe/stage22_1c_provenance_summary.json`

SHA256:

`733d2c127628c69317a0536aefd244b73db8df4a9930937055df42bbd3a81f49`

Stage22-1D evidence seal SHA256:

`6d2f40d1915e131ceffca723848f5270a9ee8887acb13fe035a0d8c86d27b8b8`

## Provenance result

The exact frozen 78-predictor provenance procedure accounted for all
**300,928** flagship rows.

- UNIQUE: **240,933**
- AMBIGUOUS: **59,995**
- UNMAPPED: **0**

Because `UNMAPPED = 0`, the frozen provenance hard-stop was not triggered.

Ambiguous rows are not repaired. They remain excluded from every later
Stage22 role according to the pre-existing protocol.

## Exact-vector audit

- Physical flagship rows: **300,928**
- Distinct exact 78-feature vectors: **240,546**
- Repeated exact-vector rows: **60,382**
- 64-bit flagship accelerator collision buckets: **0**
- Rejected source accelerator collisions: **0**

## Unique provenance rows by capture day

| Capture day | Unique rows |
|---|---:|
| 2018-02-14 | 18,813 |
| 2018-02-15 | 35,664 |
| 2018-02-16 | 29,783 |
| 2018-02-20 | 0 |
| 2018-02-21 | 39,962 |
| 2018-02-22 | 15,721 |
| 2018-02-23 | 16,878 |
| 2018-02-28 | 15,245 |
| 2018-03-01 | 30,737 |
| 2018-03-02 | 38,130 |

## Important unresolved partition-boundary observation

`2018-02-20` has **0 uniquely attributable flagship rows**.

This Stage22-1D seal deliberately records that observation without deciding
whether the day qualifies as a usable Stage22 chronological partition day.

No labels, attack distributions, class balance, model scores, or model
performance may be used to resolve that methodological question.

## Governance

Stage22-1D did not:

- read `Label`;
- read `binary_label`;
- reread flagship predictors;
- construct development, validation, or final-test roles;
- perform duplicate sanitization;
- fit preprocessing;
- train models;
- run inference;
- select thresholds;
- compute model metrics.

## Next boundary

`STAGE22-1E — FREEZE 70-FEATURE EXACT DUPLICATE GROUP EVIDENCE`

Stage22-1E will derive exact duplicate-group identities in the frozen
Stage15/Stage16 70-feature space before any chronological role assignment.

It will not yet remove duplicate rows.
