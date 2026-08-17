# Stage23-1F — NO_INIT_FWD_WIN_BYTS × CHRONOLOGICAL_NATURAL

This directory freezes the chronological partner of the
`NO_INIT_FWD_WIN_BYTS` primary ablation.

## Frozen cell

- Removed feature: `Init Fwd Win Byts`
- Retained features: 69
- Split: `CHRONOLOGICAL_NATURAL`
- New boosted-model fits: 2
- Total Stage23 fits after cell: 12 / 50
- Threshold optimization: none
- Per-subset tuning: none
- Rebalancing: none

## Chronological ranking

- Attack prevalence: 0.104846912998
- PR-AUC: 0.106031684604
- ROC-AUC: 0.509211682791
- FULL − ablated PR-AUC penalty: +0.000183470530
- FULL − ablated ROC-AUC penalty: +0.005706743603

## Split × ablation interaction

Frozen definition:

`I(S) = Δ_RANDOM(S) - Δ_CHRONOLOGICAL(S)`

Point estimates:

- PR-AUC interaction: +0.001989122538
- ROC-AUC interaction: -0.005274192868
- F1@0.50 interaction: +0.012250129142
- Recall@0.50 interaction: +0.002946345630
- FPR@0.50 interaction: -0.001946060588

The PR-AUC and ROC-AUC point estimates have different signs.

No inferential interpretation is made here. The preregistered paired
bootstrap uncertainty analysis remains required.

Raw March 1 and March 2 remain permanently closed.
