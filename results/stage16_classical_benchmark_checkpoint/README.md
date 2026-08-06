# Stage 16 Duplicate-Safe Classical Benchmark

This checkpoint preserves the completed duplicate-safe
classical baseline and hyperparameter-tuning experiments.

## Dataset identity

- Duplicate-safe training rows: 154,686
- Duplicate-safe validation rows: 37,835
- Predictors: 70
- Existing classical artifacts reused: none

The large deterministic development matrices remain outside
Git and are represented by immutable SHA-256 identities.

## Baseline experiment

Twelve classical baselines were fitted using the training split
and ranked using the validation split. The baseline winner was
XGBoost.

## Locked tuning experiment

Five validation-selected baseline candidates were tuned:

1. XGBoost
2. LightGBM
3. CatBoost
4. K-Nearest Neighbors
5. Random Forest

The search contained 12 precommitted configurations per model,
giving 60 configurations and 10,860 threshold evaluations.

## Tuned validation leader

- Candidate: LightGBM
- Configuration: LGBM_11
- Threshold: 0.47
- Accuracy: 0.9384961014933264
- Precision: 0.9673706559392112
- Recall: 0.8096707818930041
- F1: 0.8815233440252532
- F2: 0.8369588336523774
- FPR: 0.0107578381166414
- FNR: 0.1903292181069958
- ROC-AUC: 0.9682541016535458
- PR-AUC: 0.9466063189077636

## Frozen multi-seed confirmation set

Candidates within 0.0025 validation F1 of the tuned leader are
frozen for independent multi-seed confirmation:

1. LightGBM — LGBM_11
2. XGBoost — XGB_11
3. Random Forest — RF_09

The exact independent confirmation seeds have not yet been
executed. They must be precommitted before confirmation begins.

## Preserved tuning artifacts

- 60 trial run records
- 60 trial validation probability vectors
- 60 trial threshold sweeps
- Five tuned model files
- Five tuned validation probability vectors
- Five tuned threshold sweeps
- Complete tuned ranking
- Baseline-to-tuned comparison
- Tuned-selection lock

Nonwinning trial model files were intentionally deleted after
each candidate winner was safely preserved.

## Scientific boundary

All tuning fits used only the duplicate-safe training split.
All tuning selection and threshold decisions used only the
duplicate-safe validation split.

At checkpoint creation:

- Multi-seed confirmation performed: false
- Final classical winner frozen: false
- Holdout indices loaded: false
- Holdout features loaded: false
- Holdout labels loaded: false
- Holdout predictions generated: false
- Holdout metrics generated: false
