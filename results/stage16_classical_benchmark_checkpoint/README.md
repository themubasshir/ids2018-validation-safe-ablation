# Stage 16 Classical Benchmark Checkpoint

This checkpoint locks the classical-model comparison protocol
before the first duplicate-safe classical model is fitted.

## Candidate set

Twelve classical candidates are locked:

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

The earlier MLP, 1D-CNN, LSTM, and Transformer Encoder results
are excluded from this classical benchmark.

## Duplicate-safe development data

- Training rows: 154,686
- Validation rows: 37,835
- Predictors: 70
- Existing classical artifacts reused: none

Both raw and training-only-standardized caches were constructed
from the exact Stage 15 duplicate-safe training and validation
indices.

## Cache policy

The eight NumPy cache files total approximately 104 MB and are
not duplicated in Git. Their paths, shapes, dtypes, sizes, and
SHA-256 hashes are stored in:

- `stage16_1_data_cache_manifest.json`
- `stage16_1b_pretraining_protocol_lock.json`

## Scientific boundary

At checkpoint creation:

- Classical model fits: 0
- Validation predictions: 0
- Holdout indices loaded: false
- Holdout features loaded: false
- Holdout labels loaded: false
- Holdout predictions generated: false
- Holdout metrics generated: false

Model fitting may use only the duplicate-safe training cache.
Threshold selection and candidate ranking may use only the
duplicate-safe validation cache.
