# Stage23-1K — BEHAVIOR_ONLY × RANDOM_NATURAL

This directory freezes the RANDOM_NATURAL result for the prospectively
defined behavior-restricted feature set.

## Frozen feature restriction

Excluded exactly:

- `Dst Port`
- `Protocol`
- `Fwd Header Len`
- `Bwd Header Len`
- `Init Fwd Win Byts`
- `Init Bwd Win Byts`
- `Fwd Seg Size Min`

Retained features: 63

Semantic label:

`behavior_restricted_feature_set`

The correct interpretation term is **behavior-restricted performance**.

This result must not be described as “true performance” or as a direct
deployment-performance estimate.

## Execution

- Split: `RANDOM_NATURAL`
- Train rows: 11,529,922
- Validation rows: 2,882,481
- New boosted-model fits: 2
- Stage23 fits after this result: 22 / 50
- Execution source: sealed deterministic execution cache v1
- Parquet reads: 0
- Cache materialization: 65.198 s
- Threshold optimization: none
- Subset-specific tuning: none
- Rebalancing: none

## Ranking results

- Attack prevalence: 0.136847389454
- BEHAVIOR_ONLY PR-AUC: 0.981588003857
- FULL PR-AUC: 0.995590041899
- FULL − BEHAVIOR_ONLY PR-AUC penalty: +0.014002038042

- BEHAVIOR_ONLY ROC-AUC: 0.996141240052
- FULL ROC-AUC: 0.998624564774
- FULL − BEHAVIOR_ONLY ROC-AUC penalty: +0.002483324722

## Fixed threshold 0.50

- Accuracy: 0.985431994174
- Precision: 0.950588054817
- Recall: 0.942539167469
- F1: 0.946546500675
- FPR: 0.007767619325
- FNR: 0.057460832531

Confusion matrix:

- TN: 2,468,695
- FP: 19,326
- FN: 22,666
- TP: 371,794

## Current interpretation

Despite excluding the frozen contextual/TCP-stack feature set,
RANDOM_NATURAL ranking performance remains high:

- PR-AUC: 0.981588003857
- ROC-AUC: 0.996141240052

However, the restriction produces a larger RANDOM_NATURAL penalty than any
earlier frozen primary subset evaluated so far.

This is descriptive only at this stage.

## Interaction status

The matched chronological partner has not yet been executed.

Therefore the split × ablation interaction remains pending until:

`Stage23-1L BEHAVIOR_ONLY × CHRONOLOGICAL_NATURAL`

## Governance

- Stage23 fits sealed after this result: 22 / 50
- Optimized execution cache used: yes
- Parquet files read: 0
- Threshold optimization: no
- Subset-specific tuning: no
- Rebalancing: no
- SHAP: no
- Placebo: no
- Raw March 1 access: no
- Raw March 2 access: no
- Stage23-0 modified: no

## Next authorized model cell

`Stage23-1L BEHAVIOR_ONLY × CHRONOLOGICAL_NATURAL`
