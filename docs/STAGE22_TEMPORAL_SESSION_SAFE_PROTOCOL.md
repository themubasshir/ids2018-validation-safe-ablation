# Stage22 — Temporal / Session-Isolated Flagship Rerun

## Stage22-0 protocol status

**Status:** PRE-EXECUTION PREREGISTRATION LOCK

**Frozen parent:** `93944ea30d941abe055b7ad6ef261225fd61b175`

**Stage21 archive tag:** `publication-through-stage21-v1`

**Protocol SHA256:** `df9654a1bcff9ff02404e6b2cf6dde5d1ac1bf679d6a5884509427ef1b0fc062`

**Created UTC:** `2026-08-16T15:27:37+00:00`

No IDS2018 source data, Stage22 partition, model training, model inference,
validation score, threshold search, or Stage22 final-test outcome was accessed
or executed by Stage22-0.

---

## Scientific purpose

Stage22 re-evaluates the established IDS2018 flagship flow-feature model
recipes under a chronological source-capture-day partition.

It addresses the methodological concern that a row-level random/stratified
split can permit temporally related traffic structure to occur across
development and evaluation roles.

Stage22 is explicitly classified as:

`STRICTER_INTERNAL_TEMPORAL_REEVALUATION_NOT_INDEPENDENT_CONFIRMATION`

It is **not** external validation and must not be described as untouched
independent confirmation because the model-family choices were inherited from
earlier IDS2018 experiments.

---

## Frozen analysis universe

The analysis universe remains the exact processed IDS2018 corpus underlying
the established **300,928-row** flagship experiment.

Stage22 does not add source rows or select source days based on model
performance, attack coverage, or class balance.

Before any model fitting, Stage22 must deterministically recover the original
source capture day/file provenance of the flagship corpus.

Rows with ambiguous cross-day provenance are excluded from every role.

Rows that cannot be deterministically accounted for cause a hard stop rather
than fuzzy/post-hoc assignment.

---

## Frozen temporal grouping

The indivisible grouping unit is:

`ORIGINAL_SOURCE_CAPTURE_DAY`

All files belonging to the same calendar capture day receive the same role.

Usable capture days are sorted chronologically.

Provided at least five usable capture days exist:

- **Development:** all days except the latest three
- **Validation:** third-from-last usable day
- **Final test:** latest two usable days

The final two days form one pooled final test and are also reported
individually.

No chronological role may be changed because of:

- class balance
- attack-family composition
- validation performance
- final performance
- model preference

If the chronological design produces an inconvenient distribution, that is
reported rather than repaired post hoc.

---

## Session-isolation interpretation

Capture-day grouping is deliberately coarser than an individual flow/session.

Consequently, a session occurring within one capture day cannot be split
across development, validation, and final-test roles.

Stage22 does not invent unavailable five-tuple/session identifiers.

---

## Frozen duplicate-leakage rule

Exact duplicate fingerprints use the frozen **70-predictor** Stage15/Stage16
input feature space, excluding labels and provenance.

If the same exact feature fingerprint appears across chronological roles:

1. retain occurrences in the **earliest** role;
2. remove occurrences from all later roles;
3. require zero cross-role duplicate overlap afterward.

Within-role duplicates are retained but counted and reported.

The duplicate rule cannot change after observing model results.

---

## Frozen model families

Exactly two mandatory inherited flagship families are rerun.

### Classical

`ENS_LGBM_XGB_EQUAL`

- frozen Stage16 LightGBM component
- frozen Stage16 XGBoost component
- arithmetic mean of attack probabilities
- exact Stage16 component configurations
- retrained from scratch on Stage22 development
- no hyperparameter search

### Transformer

`FT_BALANCED_5_CHECKPOINT_ENSEMBLE`

Architecture:

`FT_BALANCED`

Frozen seeds:

`7, 29, 101, 313, 997`

The five probabilities are combined by arithmetic mean.

Architecture, training, checkpoint, and seed rules remain inherited from
Stage15.

There is no Stage22 architecture search, seed search, or hyperparameter
search.

Both families must be reported; Stage22 does not use the final test to select
one as a replacement for the other.

---

## Frozen preprocessing rule

Model-specific preprocessing follows the corresponding inherited Stage15 or
Stage16 recipe.

Any learned preprocessing statistic must be fit on **Stage22 development
only**.

Validation and final-test data may not fit or alter preprocessing.

---

## Frozen threshold policy

Stage22 thresholds are selected from the **new Stage22 validation partition
only**.

Historical Stage15/Stage16 numerical thresholds are not Stage22 primary
operating thresholds.

Reference threshold:

`0.50`

Validation grid:

`0.01, 0.02, ..., 0.99`

### Balanced threshold

Maximize F1.

Tie breaking:

1. lower FPR
2. higher threshold

### Security threshold

Eligibility:

`FPR <= 0.05`

Among eligible thresholds, maximize F2.

Tie breaking:

1. lower FPR
2. higher threshold

If no eligible security threshold exists, report:

`SECURITY_THRESHOLD_INFEASIBLE`

The FPR constraint may not be relaxed.

There is no final-test threshold search.

---

## Frozen metrics

Ranking:

- PR-AUC
- ROC-AUC

Operating point:

- TP
- FP
- TN
- FN
- Accuracy
- Precision
- Recall
- F1
- F2
- MCC
- FPR
- FNR

Final metrics are reported for:

- pooled latest-two-day final test
- each final capture day separately

Undefined metrics remain explicitly undefined/NaN.

Stage22 preregisters no formal significance test or bootstrap inference.

---

## Final-test governance

Final labels remain sealed until a later Stage22 pre-final-test lock has
frozen and pushed:

- partition hashes
- provenance/exclusion hashes
- preprocessing hashes
- trained-model hashes
- validation-selected thresholds
- evaluation-code hashes
- final execution authorization

Authorized final outcome openings:

`1`

Future selection openings:

`0`

The single opening evaluates **both models and all frozen operating points**.

After final evaluation there is no:

- threshold reselection
- hyperparameter tuning
- architecture selection
- feature selection
- preprocessing change
- duplicate-rule change
- capture-day reassignment
- final-score-motivated retraining

Permitted classification:

`PREREGISTERED_TEMPORAL_REPARTITION_INTERNAL_FINAL_TEST`

Explicit non-claim:

`NOT_EXTERNAL_OR_INDEPENDENT_CONFIRMATION`

---

## Next authorized step

`STAGE22-1 — SOURCE PROVENANCE INVENTORY`

Stage22-1 may locate/hash original daily source files and recover deterministic
row-to-day provenance.

Stage22-1 may **not** train models, select thresholds, or compute final-test
performance.

---

## Immutable inherited references

- `0501fc6e12208a7d34374ef50444a2fb5dd5ac9f788229e1848b6c244087cd78`  `docs/EXPERIMENT_PROTOCOL.md`
- `67e5bc9ae0a870b48d3ed8981096a76cea77ed28b981dc2686e626eb6d539eab`  `docs/PUBLICATION_ARCHIVE_THROUGH_STAGE21.md`
- `bbe392324367669d47364ebf1bebf11bf9b814f1035c557176815980ef0b36c4`  `metadata/feature_names.json`
- `fc91b2648fa8e38a8d27c6a2228ffd74cfa93e0440c1aa881825b30a62df5ba7`  `results/publication_archive_through_stage21/publication_archive_through_stage21_final_seal.json`
- `f80045b4a7750379ee6473575829d4124549038c6bbcd350be2724db0cdf3872`  `results/stage15_transformer_checkpoint/stage15_1_feature_configuration.json`
- `12a09e9e3b72808c588ae486549c7d48d1ea3695b623458836d775218fae3c9b`  `results/stage15_transformer_checkpoint/stage15_4c_final_seed_configuration.json`
- `4a1f5788eaacaca55f171684d5550509bdc07de832731dd58234f4e3300b88fa`  `results/stage15_transformer_checkpoint/stage15_4c_frozen_architecture.json`
- `45cb0008b313cdc027ff08a5910efa04c3a74661e4e9e09ff28d6035c24e5adb`  `results/stage15_transformer_checkpoint/stage15_5a_frozen_operating_threshold.json`
- `eceeb4f7d5df4bfce554fa7b8a56d87fcba626e6bfd1c77bfbe87cb36979f6ae`  `results/stage15_transformer_checkpoint/stage15_5b_preholdout_decision_lock.json`
- `da1c2d9376ff7c6ee39b5e49ee4c9a44fa594c5dc65713b9b3db1921d20cb4c8`  `results/stage16_classical_benchmark_checkpoint/stage16_5a_ensemble_protocol_lock.json`
- `1c119dc730f29e9d673eb1ef7d8bc714a82822a3a12c3d7212030e2050d23256`  `results/stage16_classical_benchmark_checkpoint/stage16_5c_final_classical_strategy_lock.json`
- `370c5ba2fa23698712f696e5dd496b64984ab5ae230b1db929cf348811519b40`  `results/stage16_classical_benchmark_checkpoint/stage16_6a_one_time_holdout_authorization_lock.json`
- `8eafe1bedb8c5fed5f0236aa8df5e4a8d4f0e1b3313d4b96dac47eca9fa25857`  `results/stage16_classical_benchmark_checkpoint/stage16_6c_final_classical_holdout_lock.json`
