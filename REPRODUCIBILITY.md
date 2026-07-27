# Reproducibility

The archive uses random state `42` and a stratified 64/16/20 split: 192,593 training records, 48,149 validation records, and 60,186 holdout test records. The full processed dataset has 300,928 rows, 78 predictor features, and excludes `Label` and `binary_label` from model inputs.

`StandardScaler` is fit only on the training data. Scaled two-dimensional inputs are used for models that require scaling, raw tabular inputs are used for tree boosting where recorded, and neural models use their saved two-dimensional or three-dimensional representations according to the stage metadata and result tables.

Boosting models were selected and tuned without holdout feedback. The available metadata records training-only cross-validation for boosting models and training-only early-stopping style selection for neural candidates. Final threshold selection was performed on validation outputs only.

The holdout test split is used only after model and threshold selection. Reported holdout metrics are descriptive final estimates, not selection criteria.

CPU/GPU differences are documented in the result tables. Several archived runs used GPU acceleration for XGBoost, LightGBM, CatBoost, MLP, and 1D-CNN; CPU-only reruns can differ in timing and, for some libraries, tiny numeric details.

To restore artifacts, install `requirements.txt`, place the processed dataset locally if rerunning from data, and use the files in `metadata/` for feature names, split metadata, split indices, and scaler state. Verify the source archive checksum with the companion `.sha256` file when available.

Notebook availability: the archive bundle included `notebook9662bff2fb.ipynb`, copied here as `notebooks/original_kaggle_working_notebook.ipynb`. Stage-specific notebooks were not present, so this repository provides maintainable validation and report-generation scripts rather than reconstructed notebooks.
