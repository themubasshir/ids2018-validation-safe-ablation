# Stage 15 Transformer Checkpoint

This package preserves Transformer feasibility, duplicate-safe
partitioning, preprocessing, P100 compatibility, architecture
screening, convergence analysis, and independent multi-seed
confirmation.

## Duplicate-safe data

- Training rows: 154,686
- Validation rows: 37,835
- Holdout rows: 46,849
- Predictors: 70
- Cross-split exact-pattern overlap: zero

## Stage 15.4B convergence repair

The FT_BALANCED seed-7 run originally obtained its best
checkpoint at the 40-epoch ceiling.

The run was continued with the exact saved:

- model state
- optimizer state
- scheduler state
- DataLoader RNG byte state
- class weighting
- early-stopping policy

Only the maximum epoch allowance changed.

### Repaired seed-7 result

- Best epoch: 50
- Final epoch: 56
- Validation threshold: 0.6949999999999997
- Validation F1: 0.866284523189161
- Validation recall: 0.7774036662925552
- Validation PR-AUC: 0.9291636892316072
- Convergence repaired: true

## Repaired three-seed aggregate

- Provisional leader: FT_BALANCED
- Runner-up: FT_COMPACT
- Mean F1: 0.8654792204569005
- F1 standard deviation: 0.0016824237516274293
- Worst-seed F1: 0.8635455023671751
- Mean PR-AUC: 0.9276945190543403
- Mean recall: 0.7743795984536725
- Seed wins: 3 of 3
- Mean F1 margin: 0.002433791142884112
- Best-checkpoint ceiling hits: 0

All predefined first-phase lead conditions pass after convergence
repair.

## Selection status

The architecture remains unfrozen because two final independent
confirmation seeds remain under the predefined protocol.

## Scientific boundary

The duplicate-safe holdout remains untouched and has not been used
for architecture selection, early stopping, threshold selection,
probability generation, or performance evaluation.

## Next step

Evaluate seeds 313 and 997 across all three candidate architectures,
then aggregate five independent confirmation seeds.

## Packaging policy

Runtime-generated `__pycache__` directories and `.pyc` files are
excluded.
