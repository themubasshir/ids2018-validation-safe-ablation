# Stage23-1A — NO_DST_PORT × RANDOM_NATURAL

This directory freezes the first reduced-feature Stage23 primary-ablation cell.

## Frozen cell

- Subset: `NO_DST_PORT`
- Split: `RANDOM_NATURAL`
- Removed feature: `Dst Port`
- Retained features: 69
- New boosted-model fits: 2
- Threshold optimization: none
- Per-subset tuning: none
- Rebalancing: none

## Ranking results

- Attack prevalence: 0.136847389454
- PR-AUC: 0.995260198750
- ROC-AUC: 0.998473210513
- FULL − NO_DST_PORT PR-AUC penalty: +0.000329843149
- FULL − NO_DST_PORT ROC-AUC penalty: +0.000151354261

## Fixed threshold 0.50

- Accuracy: 0.995601011767
- Precision: 0.999458390242
- Recall: 0.968379556863
- F1: 0.983673553474
- FPR: 0.000083198655
- FNR: 0.031620443137

## Interpretation status

No split-by-ablation shortcut interaction is interpreted from this result alone.

The matched frozen `NO_DST_PORT × CHRONOLOGICAL_NATURAL` cell must be
completed before the primary interaction can be evaluated.

Raw March 1 and March 2 remain permanently closed.
