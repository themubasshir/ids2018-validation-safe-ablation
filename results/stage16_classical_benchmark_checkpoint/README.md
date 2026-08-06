# Stage 16 Classical Benchmark

This package contains the exact duplicate-safe classical
baseline experiment performed after the Stage 15 Transformer
experiment was frozen.

## Development data

- Training rows: 154,686
- Validation rows: 37,835
- Predictors: 70
- Existing classical results reused: none
- Baseline seed: 42

The large deterministic development matrices are excluded from
Git. Their exact SHA-256 identities remain stored in the cache
manifest and pretraining lock.

## Baseline candidate set

Twelve classical candidates were fitted:

1. Logistic Regression
2. Gaussian Naive Bayes
3. K-Nearest Neighbors
4. Linear SVM
5. Decision Tree
6. Random Forest
7. Extra Trees
8. AdaBoost
9. Gradient Boosting
10. XGBoost
11. LightGBM
12. CatBoost

## Baseline winner

- Model: XGBoost
- Validation-selected threshold: 0.44
- Accuracy: 0.9369895599312805
- Precision: 0.9636160714285714
- Recall: 0.8075196408529742
- F1: 0.8786891919397517
- F2: 0.8345576863594185
- FPR: 0.012010463102825775
- FNR: 0.19248035914702583
- ROC-AUC: 0.9670573787201974
- PR-AUC: 0.9449217502319894

## Validation-selected tuning set

The following five candidates are frozen for validation-only
hyperparameter tuning:

1. XGBoost
2. LightGBM
3. CatBoost
4. K-Nearest Neighbors
5. Random Forest

## Preserved artifacts

The package includes:

- All 12 fitted baseline model files
- All 12 validation probability vectors
- All 12 threshold sweeps
- All 12 candidate run records
- Default-threshold metrics
- Validation-selected metrics
- Complete ranking
- Exact top-five selection
- Baseline selection lock

## Scientific boundary

All models were fitted using only the duplicate-safe training
split. Threshold selection and ranking used only the
duplicate-safe validation split.

At package creation:

- Baseline model fits: 12
- Validation probability vectors: 12
- Threshold sweeps: 12
- Holdout indices loaded: false
- Holdout features loaded: false
- Holdout labels loaded: false
- Holdout predictions generated: false
- Holdout metrics generated: false

The baseline validation advantage over the Transformer is not a
final superiority claim. Final comparison requires the frozen
classical holdout batch evaluation.
