# Stage23-1J — NO_SUSPICIOUS_GROUP × CHRONOLOGICAL_NATURAL

This directory freezes the chronological partner of the prospectively
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

- Split: `CHRONOLOGICAL_NATURAL`
- Train rows: 13,818,623
- Validation rows: 593,780
- New boosted-model fits: 2
- Stage23 fits after this cell: 20 / 50
- Execution source: sealed deterministic execution cache v1
- Parquet reads: 0
- Cache materialization: 41.670 s
- Threshold optimization: none
- Subset-specific tuning: none
- Rebalancing: none

## Chronological ranking

- Attack prevalence: 0.104846912998
- PR-AUC: 0.104666926088
- ROC-AUC: 0.489392507661
- FULL − ablated PR-AUC penalty: +0.001548229046
- FULL − ablated ROC-AUC penalty: +0.025525918733

## Fixed threshold 0.50

- Accuracy: 0.890407221530
- Precision: 0.155332681018
- Recall: 0.010199820098
- F1: 0.019142650428
- FPR: 0.006496414085
- FNR: 0.989800179902

Confusion matrix:

- TN: 528,071
- FP: 3,453
- FN: 61,621
- TP: 635

## Frozen split × ablation point interaction

Definition:

`I(S) = Δ_RANDOM(S) - Δ_CHRONOLOGICAL(S)`

Point estimates:

- PR-AUC interaction: +0.004440567412
- ROC-AUC interaction: -0.024309873089
- F1@0.50 interaction: +0.039938361373
- Recall@0.50 interaction: +0.017636132544
- FPR@0.50 interaction: +0.000952205052

The PR-AUC and ROC-AUC interactions currently have opposite signs.
Accordingly, interpretation remains metric-specific.

These remain **point estimates only**. The preregistered paired bootstrap
uncertainty analysis is required before inferential interpretation.

## Governance

- Stage23 fits sealed after this result: 20 / 50
- Execution-cache optimization: yes
- Cache scientifically sealed: yes
- Parquet files read: 0
- Raw March 1 access: no
- Raw March 2 access: no
- Stage23-0 modified: no
- Threshold optimization: no
- Per-subset tuning: no

## Next authorized model cell

`Stage23-1K BEHAVIOR_ONLY × RANDOM_NATURAL`
