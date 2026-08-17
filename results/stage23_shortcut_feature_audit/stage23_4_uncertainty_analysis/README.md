# Stage23-4 — Frozen Uncertainty Analysis

This directory seals the prospectively frozen uncertainty analysis for
Stage23 shortcut-feature auditing.

## Method

- 50,000-row frozen cohort per natural split
- RANDOM_NATURAL:
  - 43,158 benign
  - 6,842 attack
- CHRONOLOGICAL_NATURAL:
  - 44,758 benign
  - 5,242 attack
- 1,000 paired stratified bootstrap replicates
- `numpy.random.RandomState(seed=42)` restarted independently per split
- benign and attack rows resampled separately with replacement
- identical sampled rows within each split/replicate for FULL and ablated models
- percentile 95% interval `[2.5th, 97.5th]`

## Headline uncertainty quantities

- PR-AUC removal penalty
- ROC-AUC removal penalty
- PR-AUC split-by-ablation interaction
- ROC-AUC split-by-ablation interaction

Interaction:

`I(S) = (FULL_R - ABLATED_R) - (FULL_C - ABLATED_C)`

Full-validation metrics remain the primary point estimates.
Bootstrap intervals are supplementary uncertainty from the frozen cohorts.

## Interpretation boundary

An interaction CI lying above or below zero indicates that the frozen
cohort bootstrap does not span zero for that interaction estimate.

It does **not** establish that a feature is leakage or prove causality.
Placebo interactions must remain part of the interpretation.

## Governance

- Stage23 model-fit budget: **50 / 50**
- New fits in Stage23-4: **0**
- Raw Mar1 accessed: **NO**
- Raw Mar2 accessed: **NO**
- Parquet files read: **0**
