# Stage23-0 — Prospective Shortcut-Feature Audit Protocol

## Scientific question

To what extent does IDS performance depend on shortcut-prone contextual or
TCP-stack features, and does that dependence change between random and
chronologically separated evaluation?

## Governance

This protocol was constructed before any Stage23 model was trained and before
any Stage23 performance metric was calculated.

The primary development evaluations are the exact frozen Stage22R
`RANDOM_NATURAL` and `CHRONOLOGICAL_NATURAL` memberships.

Raw March 1 and March 2 access is permanently forbidden.

## Primary subsets

1. `FULL`
2. `NO_DST_PORT`
3. `NO_PORTS`
4. `NO_INIT_FWD_WIN_BYTS`
5. `NO_FWD_SEG_SIZE_MIN`
6. `NO_SUSPICIOUS_GROUP`
7. `BEHAVIOR_ONLY`

### Important NO_PORTS definition

The frozen 70-feature Stage22R feature space contains `Dst Port` and `Protocol`
but does not contain `Src Port`.

Therefore Stage23 prospectively operationalizes `NO_PORTS` as removing:

- `Dst Port`
- `Protocol`

Its semantic interpretation is a transport-identifier restriction. No
Stage23 manuscript text may claim that `Src Port` was removed.

## Primary evidence

- PR-AUC
- ROC-AUC
- difference-of-removal-penalties across random and chronological validation

Fixed threshold 0.50 operating metrics are secondary.

No per-subset threshold optimization is part of the primary Stage23 evidence.

## Behavior-only

The behavior-only feature list is explicitly frozen in
`behavior_only_features.json` before training.

It must be called behavior-restricted performance, not true performance.

## Placebo controls

Five fixed 3-feature behavioral placebo ablations are frozen before training.

## SHAP

A fixed 5,000-row balanced SHAP cohort is frozen separately for each split.
The same row locators are reused for every subset within that split.

## Uncertainty

Full-validation metrics remain the point estimates. Paired stratified
bootstrap uncertainty uses a separately frozen 50,000-row natural-prevalence
cohort per split with 1,000 replicates.

## Anti-adaptation

No subset, suspicious-group membership, behavior-only feature, placebo
membership, primary metric, SHAP cohort, uncertainty method, model
hyperparameter, or split may change after this protocol is sealed.
