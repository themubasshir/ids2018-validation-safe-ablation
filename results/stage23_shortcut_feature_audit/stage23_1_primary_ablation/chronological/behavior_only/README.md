# Stage23-1L — BEHAVIOR_ONLY × CHRONOLOGICAL_NATURAL

This directory freezes the chronological partner of the prospectively
defined behavior-restricted feature set and closes the Stage23 primary
boosted-ablation block.

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

Correct interpretation term:

**behavior-restricted performance**

This must not be described as “true performance” or as a deployment
performance estimate.

## Chronological execution

- Train rows: 13,818,623
- Validation rows: 593,780
- New boosted-model fits: 2
- Stage23 fits after execution: 24 / 50
- Execution source: sealed deterministic execution cache v1
- Parquet reads: 0
- Cache materialization: 58.791 s

## Behavior-restricted chronological ranking

- Attack prevalence: 0.104846912998
- PR-AUC: 0.095539807865
- FULL PR-AUC: 0.106215155134
- FULL − BEHAVIOR_ONLY PR penalty: +0.010675347269

- ROC-AUC: 0.476481778469
- FULL ROC-AUC: 0.514918426394
- FULL − BEHAVIOR_ONLY ROC penalty: +0.038436647924

The chronological BEHAVIOR_ONLY PR-AUC is below attack prevalence and
ROC-AUC is below 0.5 on this development split. This is a descriptive
observation only and does not by itself establish causal shortcut
dependence.

## Fixed threshold 0.50

- Accuracy: 0.856387887770
- Precision: 0.050535030852
- Recall: 0.020785145207
- F1: 0.029455282147
- FPR: 0.045740173539
- FNR: 0.979214854793

Confusion matrix:

- TN: 507,212
- FP: 24,312
- FN: 60,962
- TP: 1,294

## Frozen BEHAVIOR_ONLY interaction point estimates

Definition:

`I(S) = Δ_RANDOM(S) - Δ_CHRONOLOGICAL(S)`

- Random PR penalty: +0.014002038042
- Chronological PR penalty: +0.010675347269
- PR-AUC interaction: +0.003326690773

- Random ROC penalty: +0.002483324722
- Chronological ROC penalty: +0.038436647924
- ROC-AUC interaction: -0.035953323203

Supplementary:

- F1@0.50 interaction: +0.066711960023
- Recall@0.50 interaction: +0.046671997632
- FPR@0.50 interaction: +0.037948796978

The PR-AUC and ROC-AUC interaction point estimates have opposite signs.
Interpretation therefore remains metric-specific.

All interaction values remain **point estimates only** until the frozen
paired-bootstrap uncertainty analysis is executed.

## Primary boosted-ablation block

After this seal:

- Frozen primary subsets: 7
- Evaluation splits per subset: 2
- Primary boosted fits complete: 24 / 24
- Stage23 total model fits complete: 24 / 50

The Stage23 primary boosted-ablation block is now complete.

## Remaining Stage23 model fits

- Placebo boosted fits: 20
- Depth-1 stump fits: 6
- Remaining total: 26

## Governance

- Threshold optimization: no
- Subset-specific tuning: no
- Rebalancing: no
- SHAP: no
- Placebo execution in Stage23-1L: no
- Raw March 1 access: no
- Raw March 2 access: no
- Stage23-0 modified: no
- Execution-cache definition modified: no

## Next block

`Stage23 placebo ablation block`
