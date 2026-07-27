# Reproducibility

The archive uses random state `42` and a stratified 64/16/20 split: 192,593 training records, 48,149 validation records, and 60,186 holdout test records. The full processed dataset has 300,928 rows, 78 predictor features, and excludes `Label` and `binary_label` from model inputs.

`StandardScaler` is fit only on the training data. Scaled two-dimensional inputs are used for models that require scaling, raw tabular inputs are used for tree boosting where recorded, and neural models use their saved two-dimensional or three-dimensional representations according to the stage metadata and result tables.

Boosting models were selected and tuned without holdout feedback. The available metadata records training-only cross-validation for boosting models and training-only early-stopping style selection for neural candidates. Final threshold selection was performed on validation outputs only.

The holdout test split is used only after model and threshold selection. Reported holdout metrics are descriptive final estimates, not selection criteria.

CPU/GPU differences are documented in the result tables. Several archived runs used GPU acceleration for XGBoost, LightGBM, CatBoost, MLP, and 1D-CNN; CPU-only reruns can differ in timing and, for some libraries, tiny numeric details.

To restore artifacts, install `requirements.txt`, place the processed dataset locally if rerunning from data, and use the files in `metadata/` for feature names, split metadata, split indices, and scaler state. Verify the source archive checksum with the companion `.sha256` file when available.

Notebook availability: the archive bundle included `notebook9662bff2fb.ipynb`, copied here as `notebooks/original_kaggle_working_notebook.ipynb`. Stage-specific notebooks were not present, so this repository provides maintainable validation and report-generation scripts rather than reconstructed notebooks.

## Journal-Extension Reproducibility

Stage 8 uses paired class-stratified percentile bootstrap confidence intervals with random state `42`, 2,000 successful replicates, and identical bootstrap indices for paired XGBoost/LightGBM comparisons.

Stage 9 assesses calibration on the frozen holdout probabilities without recalibration. It uses 15-bin equal-width and equal-frequency reliability summaries, sensitivity checks with 10, 15, and 20 bins, Brier decomposition, and 2,000 paired bootstrap replicates.

Stage 10 uses a relative operational cost model where false-negative cost is expressed as a multiple of false-positive investigation cost. It evaluates validation-selected thresholds on the holdout set and reports break-even FN:FP ratios for switching to security operating points.

Stage 11 reconstructs holdout attack-category labels for category-level analysis. The included prediction manifest contains original dataset indices, category labels, binary labels, probabilities, and predictions; it does not contain raw predictor features.

Stage 12 is a fixed-hyperparameter multi-seed robustness study using seeds `42`, `52`, `62`, `72`, and `82`. For every seed, the split, model fitting, validation threshold selection, and holdout evaluation are repeated. The complete hyperparameter search is not repeated for every seed. The stage metadata records Linux CPU execution with 4 CPU threads for the robustness extension.

Limitations: the extension quantifies uncertainty, calibration, operational trade-offs, category-level performance, and split/training robustness, but it remains a single-dataset study and does not establish cross-dataset generalization.
