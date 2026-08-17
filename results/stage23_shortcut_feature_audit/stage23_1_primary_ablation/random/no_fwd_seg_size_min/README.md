# Stage23-1G — NO_FWD_SEG_SIZE_MIN × RANDOM_NATURAL

This directory freezes the random-split single-feature ablation of
`Fwd Seg Size Min`.

## Frozen cell

- Subset: `NO_FWD_SEG_SIZE_MIN`
- Split: `RANDOM_NATURAL`
- Removed feature: `Fwd Seg Size Min`
- Semantic label: `minimum_forward_segment_ablation`
- Retained features: 69
- New boosted-model fits: 2
- Total Stage23 fits after cell: 14 / 50
- Threshold optimization: none
- Per-subset tuning: none
- Rebalancing: none

## Ranking results

- Attack prevalence: 0.136847389454
- PR-AUC: 0.995576136093
- ROC-AUC: 0.998608787410
- FULL − ablated PR-AUC penalty: +0.000013905806
- FULL − ablated ROC-AUC penalty: +0.000015777364

## Fixed threshold 0.50

- Accuracy: 0.995651662578
- Precision: 0.999748768705
- Recall: 0.968468285758
- F1: 0.983859959978
- FPR: 0.000038584883
- FNR: 0.031531714242

## Interpretation status

The matched chronological ablation has not yet been executed.

Therefore the preregistered split × ablation interaction remains pending.

Raw March 1 and March 2 remain permanently closed.
