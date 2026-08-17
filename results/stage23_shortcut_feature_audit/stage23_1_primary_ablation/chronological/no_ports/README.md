# Stage23-1D — NO_PORTS × CHRONOLOGICAL_NATURAL

This directory freezes the matched chronological `NO_PORTS` primary-ablation
cell.

## Frozen operational definition

`NO_PORTS` removes:

- `Dst Port`
- `Protocol`

`Src Port` is not present in the frozen Stage22R 70-feature model input.

## Frozen result

- Retained features: 68
- PR-AUC: 0.102473487388
- ROC-AUC: 0.488863937353
- FULL − NO_PORTS PR-AUC penalty: +0.003741667746
- FULL − NO_PORTS ROC-AUC penalty: +0.026054489040

## Split × ablation interaction

`I(S) = Δ_RANDOM(S) - Δ_CHRONOLOGICAL(S)`

- PR-AUC interaction: -0.003419063492
- ROC-AUC interaction: -0.025905579373

These are point estimates only. The preregistered uncertainty analysis is
required before inferential interpretation.

## Governance

- Stage23 model fits sealed after this cell: 8 / 50
- Threshold optimization: none
- Per-subset tuning: none
- Rebalancing: none
- Raw March 1 and March 2: permanently closed
