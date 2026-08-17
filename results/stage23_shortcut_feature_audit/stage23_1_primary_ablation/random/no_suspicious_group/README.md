# Stage23-1I — NO_SUSPICIOUS_GROUP × RANDOM_NATURAL

This directory freezes the RANDOM_NATURAL result for the prospectively
defined three-feature suspicious-group ablation.

## Frozen subset

Removed exactly:

- `Dst Port`
- `Init Fwd Win Byts`
- `Fwd Seg Size Min`

Retained features: 67

Semantic label:

`joint_shortcut_prone_group_ablation`

## Execution

- Split: `RANDOM_NATURAL`
- Train rows: 11,529,922
- Validation rows: 2,882,481
- New boosted-model fits: 2
- Stage23 fits after this cell: 18 / 50
- Threshold optimization: none
- Subset-specific tuning: none
- Rebalancing: none

## Ranking results

- Attack prevalence: 0.136847389454
- PR-AUC: 0.989601245441
- ROC-AUC: 0.997408519130
- FULL − ablated PR-AUC penalty: +0.005988796458
- FULL − ablated ROC-AUC penalty: +0.001216045643

## Fixed threshold 0.50

- Accuracy: 0.989896550923
- Precision: 0.965033718849
- Recall: 0.960989707448
- F1: 0.963007467606
- FPR: 0.005520451797
- FNR: 0.039010292552

Confusion matrix:

- TN: 2,474,286
- FP: 13,735
- FN: 15,388
- TP: 379,072

## Interaction status

The matched `CHRONOLOGICAL_NATURAL` result has not yet been executed.

Therefore the frozen split × ablation interaction remains pending.

## Execution optimization note

Before the next model cell, a zero-fit deterministic execution-cache
optimization may be constructed and verified. It must not change:

- row membership
- labels
- clean positions
- feature values
- feature order
- input dtype
- model specifications
- model seeds
- thresholds
- ensemble definition
- Stage23 fit accounting

The next authorized model cell remains:

`Stage23-1J NO_SUSPICIOUS_GROUP × CHRONOLOGICAL_NATURAL`

Raw March 1 and March 2 remain permanently closed.
