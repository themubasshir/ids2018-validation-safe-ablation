# Experiment Protocol

## Stage 1: Data Preparation

The processed binary CSE-CIC-IDS2018 dataset contains 300,928 records and 80 columns. The predictors are the 78 feature columns after excluding `Label` and `binary_label`. A deterministic stratified split with random state `42` creates 192,593 training records, 48,149 validation records, and 60,186 holdout test records. `StandardScaler` is fitted only on the training split.

## Stage 2: Baseline Ablation

Sixteen model families are evaluated on validation data at the standard threshold. The archived baseline table ranks XGBoost first by validation F1, followed closely by LightGBM and CatBoost.

## Stage 3: Top-Five Tuning

The validation-selected top five are XGBoost, LightGBM, CatBoost, MLP, and 1D-CNN. Boosting models use recorded search outputs and best-parameter JSON files. Neural models preserve candidate outputs and training histories where present.

## Stage 4: Threshold Analysis

Validation probabilities are swept across thresholds for all top-five tuned models. Two operating points are selected from validation results: balanced maximum validation F1 and constrained maximum validation F2 subject to FPR <= 5%.

## Stage 5: Final Holdout Test

The holdout test set is evaluated only after model and threshold decisions are complete. XGBoost Tuned at threshold `0.51` is the balanced operating point. LightGBM Tuned at threshold `0.26` is the constrained-security operating point.

## Stage 6: Dual-Model SHAP

SHAP is computed for both selected models on the same deterministic stratified holdout sample of 5,000 records, with 2,500 benign and 2,500 attack records. The archived summaries compare global feature rankings and top-20 overlap.

## Stage 7: Publication Assets

Publication figures, CSV tables, LaTeX tables, and metadata are copied from the archive. Generated Markdown summaries can be refreshed with `python scripts/generate_comparison_report.py`.

## Stage 8: Paired Bootstrap Confidence

A paired class-stratified bootstrap with 2,000 successful replicates quantifies holdout-sample uncertainty for selected operating points. The same bootstrap indices are used for XGBoost and LightGBM in every replicate. Balanced model differences are interpreted as statistically unresolved when intervals include zero.

## Stage 9: Calibration Assessment

Calibration is assessed post-selection on the holdout set without recalibration. The analysis includes Brier score, log loss, equal-width and equal-frequency calibration bins, bin-count sensitivity, Brier decomposition, and paired bootstrap intervals with 2,000 successful replicates.

## Stage 10: Operational Cost Analysis

The operational cost stage evaluates thresholds under relative false-negative to false-positive cost ratios, compares frozen validation-selected operating points on holdout data, and estimates break-even cost ratios for security thresholds. The analysis documents why unconstrained high FN:FP ratios can select low thresholds with unacceptable FPR, motivating the explicit FPR <= 5% constraint.

## Stage 11: Attack-Category Analysis

Attack labels are reconstructed for the holdout predictions without including raw predictor features. Category-level detection rates, support counts, paired tests, threshold effects, and hardest-category summaries are reported for 12 attack categories.

## Stage 12: Fixed-Hyperparameter Multi-Seed Robustness

Seeds `42`, `52`, `62`, `72`, and `82` repeat the split, model fitting, validation threshold selection, and holdout evaluation for XGBoost and LightGBM. Hyperparameters remain fixed from the seed-42 tuning stage; the complete hyperparameter search is not repeated for every seed.
