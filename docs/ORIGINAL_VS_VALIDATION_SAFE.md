# Original vs Validation-Safe Evaluation

This repository is a methodological refinement, robustness analysis, and reproducibility extension of the original IDS2018 threshold-ablation work. It is not intended to discredit the original experiment.

## Original Repository

- Used an 80/20 train-test split.
- Previously reported 79 features.
- Some model or architecture choices were based on test F1.
- Threshold analysis reused test data.
- Presented LightGBM as the main winner.

## Validation-Safe Repository

- Uses a 64/16/20 train/validation/holdout split.
- Corrects the predictor count to 78 after excluding `Label` and `binary_label`.
- Performs model selection using validation data.
- Performs threshold selection using validation data.
- Reports XGBoost as the balanced validation-selected winner.
- Reports LightGBM as the constrained-security validation-selected winner.
- Uses holdout data only for descriptive final reporting after selections are fixed.
