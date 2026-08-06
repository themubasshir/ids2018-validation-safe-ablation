# Stage 15 Transformer Checkpoint

This package preserves the complete Transformer feasibility,
duplicate-safe partitioning, preprocessing, GPU compatibility,
architecture screening, convergence extension, and independent
multi-seed confirmation work.

## Repository state

- Base commit: `14337726fd76ec041fda1561be50aae627b1a93d`
- Generated: `2026-08-06T13:12:36.655412+00:00`
- Branch: `main`

## Duplicate-safe data

- Training rows: 154,686
- Validation rows: 37,835
- Holdout rows: 46,849
- Retained predictors: 70
- Cross-split exact-pattern overlap: zero

## Stage 15.4A independent confirmation

Architectures:

- FT_COMPACT
- FT_BALANCED
- FT_DEEP_REGULARIZED

Independent confirmation seeds:

- 7
- 29
- 101

Completed candidate-seed runs: 9/9

### Provisional leader

- Architecture: FT_BALANCED
- Runner-up: FT_COMPACT
- Mean validation F1: 0.8641820553183144
- Validation F1 standard deviation: 0.002178217156171591
- Worst-seed validation F1: 0.8623930277734025
- Mean validation PR-AUC: 0.9269290149821972
- Mean validation recall: 0.771293178700586
- Seed wins: 2
- Mean F1 margin: 0.0011366260042979803

Confirmation status:

`CLOSE_OR_UNSTABLE_MULTI_SEED_RANKING`

The architecture is not frozen because one FT_BALANCED run obtained
its best checkpoint at the 40-epoch ceiling. Additional convergence
and independent-seed confirmation are required.

## Scientific boundary

The duplicate-safe holdout remains untouched. It has not been used
for architecture selection, early stopping, threshold selection,
probability generation, or model evaluation.

## Next step

1. Continue the ceiling-limited FT_BALANCED seed-7 run.
2. Add two independent confirmation seeds across all three
   architectures.
3. Aggregate five independent seeds.
4. Freeze the architecture only after convergence and stability
   conditions pass.

## Packaging policy

Runtime-generated `__pycache__` directories and `.pyc` files are
excluded.
