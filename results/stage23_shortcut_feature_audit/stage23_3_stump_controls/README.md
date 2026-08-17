# Stage23-3 — Depth-1 Stump Controls

This directory seals the six prospectively frozen Stage23 depth-1
single-feature stump controls.

## Frozen design

Features:

1. `Dst Port`
2. `Init Fwd Win Byts`
3. `Fwd Seg Size Min`

Each feature was evaluated under:

- `RANDOM_NATURAL`
- `CHRONOLOGICAL_NATURAL`

Implementation:

- `sklearn.tree.DecisionTreeClassifier`
- `max_depth = 1`
- `random_state = 42`
- training-membership-only median imputation
- fixed operating threshold = 0.50

## Fit accounting

- Primary boosted fits: 24 / 24
- Placebo boosted fits: 20 / 20
- Depth-1 stump fits: 6 / 6
- **Stage23 total: 50 / 50**

The Stage23 frozen model-fit budget is exhausted.
No additional Stage23 model fit is authorized.

## Interpretation boundary

The stump controls test whether individual pre-specified features provide
discriminative signal under the frozen random and chronological validation
regimes.

Large random-to-chronological degradation is consistent with split-specific
or shortcut-like signal that transfers poorly. It does not, by itself, prove
that a feature is leakage or establish causality.

Raw March 1 and March 2 data were not accessed.
