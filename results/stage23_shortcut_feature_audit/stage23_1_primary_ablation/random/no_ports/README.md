# Stage23-1C — NO_PORTS × RANDOM_NATURAL

This directory freezes the random-split `NO_PORTS` primary-ablation cell.

## Frozen operational definition

`NO_PORTS` removes:

- `Dst Port`
- `Protocol`

`Src Port` is not present in the frozen Stage22R 70-feature model input.

The operational semantic label is:

`transport_identifier_restriction`

## Frozen cell

- Split: `RANDOM_NATURAL`
- Retained features: 68
- New boosted-model fits: 2
- Total Stage23 fits after cell: 6 / 50
- Threshold optimization: none
- Per-subset tuning: none
- Rebalancing: none

## Ranking results

- Attack prevalence: 0.136847389454
- PR-AUC: 0.995267437645
- ROC-AUC: 0.998475655106
- FULL − NO_PORTS PR-AUC penalty: +0.000322604254
- FULL − NO_PORTS ROC-AUC penalty: +0.000148909668

## Interpretation status

The split × ablation interaction is not yet available.

The matched frozen `NO_PORTS × CHRONOLOGICAL_NATURAL` cell must be
completed before the interaction point estimate is calculated.

Raw March 1 and March 2 remain permanently closed.
