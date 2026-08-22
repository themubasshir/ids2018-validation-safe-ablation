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

## Stage01-Stage10 approved extraction map

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
- Extracted safe interfaces: `src/ids_validation/data/ids2018.py`,
  `src/ids_validation/stages/stage01/protocol.py`,
  `configs/stage01/protocol.json` and `scripts/reproduce_stage01.py`.

### Stage02 — cells 94-95

- Cell 94: twelve classical/boosting baselines using the historical raw/scaled
  input assignments and fixed constructors.
- Cell 95: MLP, 1D-CNN, LSTM and Transformer Encoder baselines with training-only
  internal early-stopping split, maximum 30 epochs and seed 42.
- Inputs: Stage01 raw/scaled train and validation arrays.
- Outputs: per-model validation results, saved models, histories,
  configurations, environment versions and the 16-model merged ranking.
- Holdout dependency: none; Stage02 does not use the test partition.
- Extracted safe interfaces: `src/ids_validation/models/baselines.py`,
  `src/ids_validation/models/neural.py`,
  `src/ids_validation/evaluation/metrics.py`, the Stage02 protocol/config and
  `scripts/reproduce_stage02.py`.

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
- Extracted safe interfaces: `src/ids_validation/models/tuning.py`, the tuned
  builders in `src/ids_validation/models/neural.py`, the Stage03
  protocol/config and `scripts/reproduce_stage03.py`.

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
- Extracted safe interfaces: `src/ids_validation/evaluation/metrics.py`,
  `src/ids_validation/evaluation/thresholds.py`, the Stage04 protocol/config
  and `scripts/reproduce_stage04.py`.

### Stage05 — cells 105 and 107

- Cell 105: one-time XGBoost holdout evaluation with standard threshold 0.50
  and the constrained security threshold 0.27 verified against Stage04.
- Cell 107: objective-specific comparison using XGBoost balanced threshold 0.51
  and LightGBM security threshold 0.26, while also reporting standard 0.50.
- Inputs: frozen Stage03 models, Stage04 selected thresholds and Stage01 holdout
  arrays.
- Outputs: frozen holdout probabilities, operating-point metrics and metadata.
- Governance: extraction and verification must not call these inference paths.
- Extracted safe interfaces: Stage05 metric-record constructors in
  `src/ids_validation/evaluation/metrics.py`, the Stage05 protocol/config and
  `scripts/reproduce_stage05.py`. The entry point has no execution mode.

### Stage06 — cell 108

- Construct one shared class-balanced sample using seed 42: 2,500 benign and
  2,500 attack rows, sampled without replacement and shuffled once.
- Explain the frozen XGBoost and LightGBM models with TreeSHAP, normalize the
  binary-output shapes, rank each model's top 20 features and compare the
  shared top 15. Frozen decision thresholds remain 0.51 and 0.26.
- Inputs: Stage01 holdout arrays and Stage03 serialized model artifacts.
- Outputs: SHAP arrays, five result tables, six figures and metadata.
- Extracted safe interfaces: `src/ids_validation/explainability/shap_analysis.py`,
  the Stage06 protocol/config and `scripts/reproduce_stage06.py`.
- Verification limitation: the exact historical Joblib model inputs and SHAP
  matrices are absent. Native JSON/TXT models are not asserted to be identical
  substitutes, and the historical SHAP version is `VERSION_NOT_PROVEN`.

### Stage07 — cells 109-115

- Cell 109 generates publication figures/tables and assembles publication
  assets using frozen Stage02-Stage06 results.
- Cells 110-114 are archival operations: historical ZIP deletion, inventory,
  SHA256 manifest creation, tar creation and archive verification.
- Cell 115 is a required-file presence check.
- Expected publication set: 15 figures, four CSV tables and four LaTeX tables.
- Extracted safe interfaces: `src/ids_validation/stages/stage07/publication.py`,
  the Stage07 protocol/config and `scripts/reproduce_stage07.py`.
- Safety divergence: the extracted path reports ZIP cleanup candidates but
  never deletes them, renders archive/checksum commands without executing them,
  and verifies asset presence only. The complete historical archive and its
  file manifest are absent; only `metadata/source_archive.sha256` remains.

### Stage08 — cells 116-117

- Perform 2,000 paired class-stratified bootstrap replicates with seed 42 and
  95% percentile intervals. Each replicate shares sampled benign and attack
  indices across models and operating points.
- Evaluate the frozen standard and objective-specific thresholds: XGBoost
  0.50/0.51/0.27 and LightGBM 0.50/0.26.
- Cell 117 is a required-file presence check.
- Extracted safe interfaces: `src/ids_validation/evaluation/bootstrap.py`, the
  Stage08 protocol/config and `scripts/reproduce_stage08.py`.
- Extraction verification opens frozen bootstrap NPZ files only for key,
  schema and shape checks; it does not generate bootstrap replicates or read
  holdout target/probability inputs.

### Stage09 — cell 118

- Assess calibration without recalibration using a primary 15-bin analysis and
  10/15/20-bin sensitivity, plus ECE, MCE, RMSCE, Brier score, log loss,
  Brier decomposition and calibration intercept/slope methodology.
- Confidence intervals use the same 2,000-replicate paired stratified bootstrap
  design as Stage08.
- Extracted safe interfaces: `src/ids_validation/evaluation/calibration.py`, the
  Stage09 protocol/config and `scripts/reproduce_stage09.py`.
- Extraction verification is structural only and does not execute calibration
  or bootstrap computations on frozen holdout inputs.

### Stage10 — cell 119

- Evaluate relative FN:FP cost ratios 1, 2, 5, 10, 20, 50 and 100 using
  `FP + ratio * FN`, select thresholds on validation data, and report holdout
  results descriptively at frozen thresholds.
- The cost-ratio threshold search is unconstrained and uses the exact tie chain:
  cost ascending, FN ascending, FP ascending, F2 descending, threshold
  descending. The Stage04 5% FPR constraint applies only to the separately
  frozen security operating points (XGBoost 0.27, LightGBM 0.26).
- Extracted safe interfaces: `src/ids_validation/evaluation/operating_cost.py`,
  the Stage10 protocol/config and `scripts/reproduce_stage10.py`.
- Extraction verification checks the frozen 14-row validation-selection table
  only; it performs no threshold search and opens no holdout inputs.

## Stage11-Stage20 map

| Stage | Physical cells | Purpose; main dependencies and frozen decisions |
|---:|---:|---|
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
