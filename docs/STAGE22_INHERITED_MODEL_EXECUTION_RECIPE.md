# Stage22-2A — Inherited Model Execution Recipe Lock

## Status

**FROZEN BEFORE ANY STAGE22 LABEL ACCESS OR MODEL EXECUTION**

Scientific parent:

`966d8eae2c7eb6ae4fbc362f2dbc8afddabd46d4`

Lock SHA256:

`6c0a733d75735fe10c5ed90621f79157577c055cdab14bc981e6f161a1749a0a`

## Stage22 population boundary

The already-sealed Stage22 sanitized chronological partition remains unchanged:

- DEVELOPMENT: **156,821 rows**
- VALIDATION: **15,245 rows**
- FINAL_TEST: **68,867 rows**
- exact 70-feature cross-role duplicate overlap: **0**
- duplicate exclusions introduced at Stage22-1G: **0**
- ambiguous-provenance exclusions inherited: **59,995**

No row roles are changed by Stage22-2A.

## Frozen predictors

Exactly **70** Stage15/Stage16 predictors are used, in the inherited order.

There is:

- no Stage22 feature search;
- no Stage22 feature addition;
- no Stage22 feature removal;
- no Stage22 shortcut-feature removal.

Shortcut-feature analysis remains deferred to Stage23.

## Transformer

Mandatory family:

**FT_BALANCED_5_CHECKPOINT_ENSEMBLE**

Seeds:

`7, 29, 101, 313, 997`

Architecture:

- NumericFTTransformer
- d_token: 64
- heads: 8
- layers: 3
- feed-forward width: 256
- dropout: 0.1
- GELU
- no positional encoding
- single binary logit

### Transformer preprocessing

A **fresh StandardScaler** is fit using sanitized Stage22 DEVELOPMENT predictors only.

The historical Stage15 scaler is a structural/reference artifact only and is **not reused**.

- raw numeric load: float64
- StandardScaler: with_mean=True, with_std=True
- clipping: NO
- imputation: NO
- transformed model input: float32
- VALIDATION in scaler fit: NO
- FINAL_TEST in scaler fit: NO

### Transformer loss

`BCEWithLogitsLoss`

Positive-class weight is recomputed once as:

`DEVELOPMENT benign count / DEVELOPMENT attack count`

Only DEVELOPMENT labels may define this statistic.

### Transformer training

- maximum epochs: 70
- batch size: 1024
- AdamW
- learning rate: 0.0005
- weight decay: 0.00001
- gradient clip norm: 1.0
- precision: float32

The inherited Stage15 checkpoint rule remains active:

- ReduceLROnPlateau monitors Stage22 VALIDATION PR-AUC;
- factor 0.5;
- patience 2;
- minimum LR 1e-5;
- best checkpoint maximizes Stage22 VALIDATION PR-AUC;
- checkpoint improvement tolerance 1e-7;
- early stopping patience 6.

**Validation never participates in gradient updates or scaler fitting.**

This is the frozen operational interpretation of Stage22's simultaneous requirements to:

1. train using DEVELOPMENT only; and
2. inherit the Stage15 architecture/training/checkpoint rule exactly.

The five best-checkpoint attack-probability vectors are averaged with equal weight 0.2.

## Classical strategy

Mandatory family:

**ENS_LGBM_XGB_EQUAL**

Component 1:

**LightGBM / LGBM_11**

```text
n_estimators=400
learning_rate=0.06
num_leaves=127
max_depth=12
subsample=0.9
colsample_bytree=1.0
reg_alpha=0.0
reg_lambda=3.0
min_child_samples=20
subsample_freq=1
random_state=42
```

Component 2:

**XGBoost / XGB_11**

```text
n_estimators=400
learning_rate=0.06
max_depth=7
subsample=0.9
colsample_bytree=1.0
min_child_weight=1
gamma=0.0
reg_alpha=0.0
reg_lambda=3.0
random_state=42
```

Both use the raw **70-feature float32** representation.

No StandardScaler is used by either classical component.

Both are freshly fit on sanitized Stage22 DEVELOPMENT only.

No validation rows enter classical fitting.

Final ensemble probability:

`0.5 * P_LIGHTGBM + 0.5 * P_XGBOOST`

## Stage22 threshold protocol

Historical Stage15 thresholds and the historical Stage16 threshold 0.46 are references only.

They are **not** Stage22 operating thresholds.

Stage22 uses only its preregistered validation grid:

- standard: **0.50**
- candidate grid: **0.01–0.99 inclusive, step 0.01**
- balanced: maximize F1; tie -> lower FPR; tie -> higher threshold
- security: FPR <= 0.05, maximize F2; tie -> lower FPR; tie -> higher threshold
- if no security threshold is feasible: report infeasible, never relax the constraint.

No FINAL_TEST threshold search is allowed.

## Failure policy before training

If DEVELOPMENT contains only one binary class, the inherited training experiment is scientifically infeasible.

Do **not**:

- reassign days;
- change class weighting;
- add rows;
- substitute models;
- alter features;
- relax chronology.

Stop and report the frozen limitation.

## Final-test embargo

Stage22-2A reads:

- FINAL_TEST predictors: **NO**
- FINAL_TEST labels: **NO**
- FINAL_TEST scores: **NO**
- final outcome openings consumed: **0**

FINAL_TEST remains sealed.

## Next authorized checkpoint

**Stage22-2B — materialize sanitized DEVELOPMENT/VALIDATION labeled matrices and fit the DEVELOPMENT-only Transformer StandardScaler.**

Stage22-2B may read only the frozen predictors plus `binary_label` for DEVELOPMENT and VALIDATION row IDs.

FINAL_TEST predictors and labels remain sealed.
