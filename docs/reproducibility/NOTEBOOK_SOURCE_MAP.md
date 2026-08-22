# Authoritative Notebook Source Map

## Locator and identity

Canonical source:

`notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb`

SHA256:

`147760f81f5db581c2cbc92b3c7c24060b823dfa50ac9d9a2156eb132b51b3ce`

Cell references below are physical 1-based positions in the immutable archive.
Execution counters are not locators. The complete per-cell map, including
source hashes, classifications and detected path references, is in
`NOTEBOOK_CELL_MAP.csv`.

## Pre-canonical history

| Cells | Classification | Role |
|---:|---|---|
| 1-6 | precursor | Kaggle environment, mounted-input inventory and initial dataset/split state. |
| 7-67 | superseded | Earlier baseline, tuning, threshold, neural and SHAP workflow drafts. Retained unchanged. |
| 68-72 | precursor | Transition to the explicit train/validation/holdout split and saved split/scaler artifacts. |
| 73-91 | superseded | Earlier validation-safe stage drafts replaced by the `ids2018_clean_validation_v2` cells. |
| 92 | precursor | Notebook-global state probe immediately before the canonical Stage01 cell. |

## Stage01-Stage05 approved extraction map

### Stage01 — cell 93

- Purpose: construct the canonical processed-data representation and
  stratified 64/16/20 split.
- Inputs: `merged_balanced_ids2018_safe.csv`; target `binary_label`.
- Transformations: exclude `Label` and `binary_label`; retain 78 predictors in
  dataframe order; reserve 20% stratified test; split the remaining 80% into
  80% train and 20% validation; fit `StandardScaler` on train only.
- Seed: 42.
- Outputs: split indices, feature names, scaler, split summary, split metadata
  and SHA256 feature-order signature.
- Dependencies: none of the later model or threshold cells.

### Stage02 — cells 94-95

- Cell 94: twelve classical/boosting baselines using the historical raw/scaled
  input assignments and fixed constructors.
- Cell 95: MLP, 1D-CNN, LSTM and Transformer Encoder baselines with training-only
  internal early-stopping split, maximum 30 epochs and seed 42.
- Inputs: Stage01 raw/scaled train and validation arrays.
- Outputs: per-model validation results, saved models, histories,
  configurations, environment versions and the 16-model merged ranking.
- Holdout dependency: none; Stage02 does not use the test partition.

### Stage03 — cells 96-101

- Cells 96-98: XGBoost, LightGBM and CatBoost randomized tuning with 15 sampled
  candidates, three-fold shuffled stratified CV on training only, seed 42 and
  external validation reporting at threshold 0.50.
- Cells 99-100: historical MLP and CNN candidate tuning with a 15% internal
  training-only validation partition and maximum 50 epochs.
- Cell 101: merge the five already-generated tuned result/probability artifacts.
- Outputs: search logs, selected parameters, native/joblib/Keras models,
  validation probabilities, histories and combined artifact manifest.
- Holdout dependency: none.

### Stage04 — cells 102-104 and 106

- Cell 102: rank the tuned models using validation F1, recall and precision;
  sweep the winning model from 0.05 through 0.95 inclusive by 0.01; record
  standard 0.50, maximum-F1 and maximum-F2 points.
- Cell 103: select the constrained security point under FPR <= 0.05 using the
  historical ordering/tie behavior.
- Cell 104: package the Stage04 directory.
- Cell 106: apply the same frozen grid and objectives to all five tuned models.
- Inputs: Stage03 validation result and probability artifacts.
- Outputs: full sweeps, selected operating points, neighborhood tables and
  threshold provenance metadata.
- Holdout dependency: none.

### Stage05 — cells 105 and 107

- Cell 105: one-time XGBoost holdout evaluation with standard threshold 0.50
  and the constrained security threshold 0.27 verified against Stage04.
- Cell 107: objective-specific comparison using XGBoost balanced threshold 0.51
  and LightGBM security threshold 0.26, while also reporting standard 0.50.
- Inputs: frozen Stage03 models, Stage04 selected thresholds and Stage01 holdout
  arrays.
- Outputs: frozen holdout probabilities, operating-point metrics and metadata.
- Governance: extraction and verification must not call these inference paths.

## Stage06-Stage20 map

| Stage | Physical cells | Purpose; main dependencies and frozen decisions |
|---:|---:|---|
| 06 | 108 | Dual-model TreeSHAP using frozen XGBoost/LightGBM, seed 42, 2,500 benign + 2,500 attack samples, top 20 features and thresholds 0.51/0.26. Depends on Stages01/03/05. |
| 07 | 109-115 | Publication tables/figures, manifests and complete-working archive verification. No model fitting. |
| 08 | 116-117 | Paired class-stratified bootstrap, 2,000 replicates, seed 42, 95% intervals over frozen probabilities and thresholds. |
| 09 | 118 | Calibration without recalibration; 2,000 bootstrap replicates; primary 15 bins with 10/15/20-bin sensitivity. |
| 10 | 119 | Relative operational costs for FN:FP ratios 1, 2, 5, 10, 20, 50 and 100; validation selection with descriptive holdout evaluation. |
| 11 | 120 | Attack-category reconstruction and frozen operating-point analysis; 1,000 paired bootstrap replicates. |
| 12 | 121-129 | Constructor patch, seeds 42/52/62/72/82, fixed hyperparameters, per-seed split/fitting/validation threshold selection and packaging. |
| 13 | 130-146 | Artifact discovery, holdout reconstruction checks, LIME background/case analysis, configuration and seed sensitivity, local SHAP-LIME agreement and packaging. |
| 14 | 147-161 | Neural artifact compatibility, scaler reconstruction, MLP/CNN Integrated Gradients, convergence/reference sensitivity and recovery/package cells. |
| 15 | 162-170; 172-189 | Duplicate-safe 70-feature FT-Transformer; P100-compatible isolated runtime; candidates and convergence repairs; seeds 7/29/101/313/997; `FT_BALANCED`; threshold 0.73; one holdout opening. |
| 16 | 171; 190-222 | Twelve-model duplicate-safe classical benchmark, top-five tuning, multi-seed confirmation, limited ensemble comparison and one holdout. Cell 171 is the approved out-of-sequence Stage16 source. Final ensemble is 0.5 LightGBM + 0.5 XGBoost at 0.46. |
| 17 | 223-239 | Post-result five-checkpoint attention analysis on a deterministic 64-case validation panel and cross-method comparison. No training or holdout access. |
| 18 | 240-289 | Representation-first temporal/ViT/graph feasibility; temporal supported with constraints, ViT rejected, graph experiment restricted to Feb-20 directed 60-second snapshots with seeds 7/29/101. |
| 19 | 290-311 | Chronological one-second bins; train Feb14-23, validate Feb28, holdout Mar01-02; train-only preprocessing; single-scale and MTemporal seeds 7/29/101; threshold grid 0.01-0.99 by 0.01. |
| 20 | 312-461 | CICIDS2017 source/label forensics, directed-S4 reconstruction and errata, 64x256x1 packet image, compact corpora, fixed Stage20MaskedCNNv1 seed 42 for 10 epochs, Thursday threshold freeze and one Friday holdout opening. |

## Stage21 cells embedded in the archive

Physical cells 462-488 are Stage21 source-restoration work and are classified
`stage21_out_of_filename_scope`. They are preserved because removing them would
mutate the historical notebook. They must not be extracted as Stage20 logic.

## Provenance rule for extracted functions

Every extracted scientific function must record:

```text
Source notebook:
Original physical cell(s):
Original stage:
Frozen artifacts generated:
Notes:
```

Recovery, repair, superseded and packaging code must not be promoted into a
canonical scientific path without an explicit evidence-backed decision in the
discrepancy register.
