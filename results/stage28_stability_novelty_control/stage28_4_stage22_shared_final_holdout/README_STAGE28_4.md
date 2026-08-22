# Stage28-4 — Stage22 shared-final-holdout robustness inference

## Scientific status

- New model fits: 0
- Frozen component-model inferences: 20
- Ensemble evaluations: 10
- Threshold selections: 0
- Model selections: 0
- New formal significance tests: 0
- Stage28 fit ledger: 108 / 108 consumed
- Remaining new fits: 0

## Holdout

- Rows: 1,374,133
- Benign: 998,788
- Attack: 375,345
- Features: 70
- dtype: float64
- X SHA256: `50979ff283ddebaceb6442004c5b80b85e4fb40d02041a5150f730683b3d7c8e`
- y SHA256: `b99cf695a49ad2b0a8811fa269a55dcfb99cb700f473ceae8c9ecac2c8661a78`

The holdout had already been opened historically by Stage22R.
Stage28-4 is preregistered robustness re-evaluation, not a new blind test.

## Recovery

The initial Stage28-4 execution successfully materialized the holdout but
stopped before model inference because a compact AUTO-A result receipt omitted
the redundant `models.ensemble_probability` field.

R1 reused the already-materialized in-memory holdout and did not reread the
March source files.

## Frozen directional stability

PR claim:

`PR_AUC_RANDOM_NATURAL < PR_AUC_CHRONOLOGICAL_NATURAL`

Support: 5 / 5
Stability rate: 1.000000

ROC claim:

`ROC_AUC_RANDOM_NATURAL < ROC_AUC_CHRONOLOGICAL_NATURAL`

Support: 5 / 5
Stability rate: 1.000000

## Closure

Stage28 empirical work is complete after this result.

No Stage29 is authorized.
The remaining work is zero-fit synthesis and manuscript integration.
