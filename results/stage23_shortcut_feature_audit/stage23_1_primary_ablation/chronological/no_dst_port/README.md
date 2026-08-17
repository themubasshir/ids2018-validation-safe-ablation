# Stage23-1B — NO_DST_PORT × CHRONOLOGICAL_NATURAL

This directory freezes the matched chronological partner of Stage23-1A.

## Frozen cell

- Subset: `NO_DST_PORT`
- Split: `CHRONOLOGICAL_NATURAL`
- Removed feature: `Dst Port`
- Retained features: 69
- New boosted-model fits: 2
- Total Stage23 fits after this cell: 4 / 50
- Threshold optimization: none
- Per-subset tuning: none
- Rebalancing: none

## Chronological ranking results

- Attack prevalence: 0.104846912998
- PR-AUC: 0.102473686409
- ROC-AUC: 0.488864390761
- FULL − NO_DST_PORT PR-AUC penalty: +0.003741468725
- FULL − NO_DST_PORT ROC-AUC penalty: +0.026054035633

## Split × ablation interaction

Frozen definition:

`I(S) = Δ_RANDOM(S) - Δ_CHRONOLOGICAL(S)`

Point estimates:

- PR-AUC interaction: -0.003411625576
- ROC-AUC interaction: -0.025902681372

These are point estimates only.

The preregistered Stage23 uncertainty analysis must be completed before
inferential interpretation of the interaction.

## Governance

- Raw March 1 access: forbidden
- Raw March 2 access: forbidden
- Stage23-0 unchanged
- No threshold optimization
- No subset-specific tuning
- No rebalancing
