# Stage23-1H — NO_FWD_SEG_SIZE_MIN × CHRONOLOGICAL_NATURAL

This directory freezes the chronological partner of the
`NO_FWD_SEG_SIZE_MIN` primary ablation.

## Frozen cell

- Removed feature: `Fwd Seg Size Min`
- Semantic label: `minimum_forward_segment_ablation`
- Retained features: 69
- Split: `CHRONOLOGICAL_NATURAL`
- New boosted-model fits: 2
- Total Stage23 fits after cell: 16 / 50
- Threshold optimization: none
- Per-subset tuning: none
- Rebalancing: none

## Chronological ranking

- Attack prevalence: 0.104846912998
- PR-AUC: 0.105454756063
- ROC-AUC: 0.511682110206
- FULL − ablated PR-AUC penalty: +0.000760399071
- FULL − ablated ROC-AUC penalty: +0.003236316188

## Split × ablation interaction

Frozen definition:

`I(S) = Δ_RANDOM(S) - Δ_CHRONOLOGICAL(S)`

Point estimates:

- PR-AUC interaction: -0.000746493265
- ROC-AUC interaction: -0.003220538824
- F1@0.50 interaction: +0.000071623304
- Recall@0.50 interaction: +0.000021984972
- FPR@0.50 interaction: +0.000018557332

These remain point estimates only. The preregistered paired bootstrap
uncertainty analysis is required before inferential interpretation.

Raw March 1 and March 2 remain permanently closed.
