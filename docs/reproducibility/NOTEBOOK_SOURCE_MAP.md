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

## Stage01-Stage20 approved extraction map

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

### Stage11 — cell 120

- Reconstruct the original attack taxonomy from stripped `Label` strings and
  apply the already-frozen XGBoost 0.51/0.27 and LightGBM 0.50/0.26 operating
  points.
- Preserve 12 exact categories, their 24,186 total attack support, 1,000 paired
  bootstrap replicates at seed 42, Wilson intervals, exact paired
  McNemar/binomial tests and Benjamini-Hochberg correction.
- SQL Injection support remains 13 and is explicitly labelled low support
  under the historical minimum-support-20 presentation/ranking rule.
- Extracted safe interfaces: `src/ids_validation/evaluation/attack_categories.py`,
  the Stage11 protocol/config and `scripts/reproduce_stage11.py`.
- Extraction did not reconstruct/open the holdout or recompute category
  metrics.

### Stage12 — cells 121-129

- Cell 121 repairs constructor keyword collisions. Cell 122 repeats the
  stratified 64/16/20 split for seeds 42, 52, 62, 72 and 82, fits fixed
  seed-42 hyperparameters, and selects validation operating points on the
  0.05-0.95 grid by 0.01 using the historical tie chains.
- This estimates repeated-split/fixed-fit robustness only; hyperparameter
  search is not repeated and full-pipeline/HPO uncertainty is not estimated.
- Cells 123-129 contain presence, inventory, destructive cleanup and archival
  packaging operations. The safe extraction exposes none of the cleanup or
  archive mutations.
- Extracted safe interfaces: `src/ids_validation/evaluation/multiseed.py`, the
  Stage12 protocol/config and `scripts/reproduce_stage12.py`.
- No estimator was fitted and no split or threshold was scientifically rerun.

### Stage13 — cells 130-146

- Preserve shortest-path artifact discovery, exact holdout reconstruction and
  archived-probability verification logic, the 20,000-row training-only LIME
  background, outcome/disagreement panels, 5,000-sample initial LIME with 15
  terms, the selected 10,000-sample continuous wider-kernel configuration and
  five perturbation seeds 137000-141000.
- Preserve local SHAP-LIME top-k, cosine, Spearman and sign-agreement formulas,
  paired explanation seeds and study-specific fidelity/reliability labels.
- Extracted safe interfaces: `src/ids_validation/explainability/lime_analysis.py`,
  `src/ids_validation/explainability/local_agreement.py`, the Stage13
  protocol/config and `scripts/reproduce_stage13.py`.
- LIME 0.2.0.1 is proven; SHAP, SciPy and Matplotlib versions remain
  `VERSION_NOT_PROVEN`. Neither LIME nor SHAP was run and the holdout was not
  reconstructed or opened.

### Stage14 — cells 147-161

- Preserve MLP/CNN input compatibility, repository-scaler provenance, the
  outcome-stratified 64-case panel, pre-sigmoid attack-logit target, zero,
  benign-median and 32-reference benign baselines, and 16/32/64/128-step
  trapezoidal convergence audit with 128 steps selected.
- Extracted mathematical helpers accept only caller-supplied toy gradient
  grids. They do not import TensorFlow, load neural artifacts or compute
  gradients.
- Extracted safe interfaces:
  `src/ids_validation/explainability/integrated_gradients.py`, the Stage14
  protocol/config and `scripts/reproduce_stage14.py`.
- TensorFlow 2.19.0 is proven for this stage only; standalone Keras,
  scikit-learn, Joblib and Matplotlib remain `VERSION_NOT_PROVEN`.

### Stage15 — cells 162-170 and 172-189

- Cell 163 constructs the deterministic train-priority duplicate-safe split:
  globally exclude binary-conflicting patterns, retain the minimum original
  row per pattern, then exclude train patterns from validation and prior-split
  patterns from holdout. Frozen safe sizes are 154,686/37,835/46,849 with zero
  post-processing overlap or within-split duplicates.
- Remove eight exact constant predictors and retain the frozen ordered 70
  numerical features. Fit `StandardScaler` and derive the positive-class
  weight from duplicate-safe training rows only.
- Frozen `FT_BALANCED` uses a feature-specific numerical tokenizer plus CLS,
  no positional encoding, 64-dimensional tokens, eight heads, three layers,
  feed-forward width 256, dropout 0.1 and 159,169 parameters. AdamW uses
  learning rate 0.0005 and weight decay 0.00001; batch size is 1,024.
- The locked seeds are 7, 29, 101, 313 and 997. Threshold 0.73 is frozen from
  the validation-only robust plateau and applied to the unweighted mean of the
  five checkpoint probabilities.
- The Stage15.5B lock records architecture, threshold and checkpoint hashes
  before the historical Stage15.6A one-time holdout opening. Extraction checks
  checkpoint bytes only and performs no training, deserialization, inference,
  threshold selection or holdout access.
- Extracted safe interfaces: `src/ids_validation/data/duplicate_safe_split.py`,
  `src/ids_validation/models/ft_transformer.py`, the Stage15 protocol/config
  and `scripts/reproduce_stage15.py`.
- Physical cell 171 is explicitly excluded; it belongs to Stage16.

## Stage16-Stage20 map

| Stage | Physical cells | Purpose; main dependencies and frozen decisions |
|---:|---:|---|
| 16 | 171; 190-222 | Twelve-model duplicate-safe classical benchmark, top-five tuning, multi-seed confirmation, limited ensemble comparison and one holdout. Cell 171 is the approved out-of-sequence Stage16 source. Final ensemble is 0.5 LightGBM + 0.5 XGBoost at 0.46. |
| 17 | 223-239 | Post-result five-checkpoint attention analysis on a deterministic 64-case validation panel and cross-method comparison. No training or holdout access. |
| 18 | 240-289 | Representation-first temporal/ViT/graph feasibility; temporal supported with constraints, ViT rejected, graph experiment restricted to Feb-20 directed 60-second snapshots with seeds 7/29/101. |
| 19 | 290-311 | Chronological one-second bins; train Feb14-23, validate Feb28, holdout Mar01-02; train-only preprocessing; single-scale and MTemporal seeds 7/29/101; threshold grid 0.01-0.99 by 0.01. |
| 20 | 312-461 | CICIDS2017 source/label forensics, directed-S4 reconstruction and errata, 64x256x1 packet image, compact corpora, fixed Stage20MaskedCNNv1 seed 42 for 10 epochs, Thursday threshold freeze and Friday governance. The later completed Friday opening is frozen evidence without a mapped notebook execution cell. |

### Stage16 — cell 171 and cells 190-222

- Inherits the exact Stage15 duplicate-safe 70-feature representation and
  split memberships; it does not create another split.
- Preserves the twelve classical candidates, five-candidate tuning budget,
  five-seed confirmation, limited ensemble comparison and final equal-weight
  LightGBM/XGBoost strategy at threshold 0.46.
- Extracted interfaces are `src/ids_validation/models/classical.py`, the
  Stage16 protocol/config and `scripts/reproduce_stage16.py`.
- Verification hashes frozen artifacts only. It does not construct, load or
  fit an estimator and does not reopen the historical holdout.

### Stage17 — cells 223-239

- Uses the five already-frozen Stage15 checkpoints as historical inputs for a
  deterministic 64-case validation panel, head/layer/rollout summaries,
  stability and cross-method comparisons.
- Extracted attention helpers accept toy tensors only. The historical private
  attention hook remains explicitly framework-sensitive.
- Extracted interfaces are `src/ids_validation/evaluation/attention.py`, the
  Stage17 protocol/config and `scripts/reproduce_stage17.py`.
- No training, holdout access, checkpoint load or attention recomputation was
  performed.

### Stage18 — cells 240-289

- Preserves three historically distinct conclusions: temporal supported with
  constraints; ViT unsupported by the then-available artifacts; graph
  supported with constraints.
- The graph branch uses source-restricted Feb-20 data, directed 60-second
  snapshots, EdgeOnlyMLP and Graph Transformer controls, and seeds 7/29/101.
- Extracted interfaces are `src/ids_validation/data/graph_snapshots.py`,
  `src/ids_validation/models/graph_models.py`, the Stage18 protocol/config and
  `scripts/reproduce_stage18.py`.
- Stage20 evidence is later in the chronology and must not rewrite the Stage18
  ViT conclusion.

### Stage19 — cells 290-311

- Freezes forward chronology: Feb 14-23 TRAIN, Feb 28 VALIDATION and Mar 1-2
  HOLDOUT; one-second wall-clock bins; train-only imputation/scaling; and no
  cross-day or cross-partition windows.
- Preserves the fine 60-second control and three-branch 60/300/1200-second
  MTemporal model for seeds 7/29/101, plus the 0.01-0.99 threshold grid.
- Extracted interfaces are `src/ids_validation/data/temporal_bins.py`,
  `src/ids_validation/models/temporal_models.py`, the Stage19 protocol/config
  and `scripts/reproduce_stage19.py`.
- Only synthetic window/shape checks and artifact-byte verification are
  exposed; temporal materialization, fitting and inference remain disabled.

### Stage20 — cells 312-461

- The required fine-grained historical map is in
  `STAGE20_SUBSTAGE_MAP.md` and `STAGE20_CELL_MAP.csv`.
- Cells 312-411 cover source/label provenance, exact directed-S4 semantics,
  historical extractor forensics, C8 flag serialization, D5 baseline erratum,
  negative global V1 validation, C16 recovery and stopped mechanism search.
- Cells 412-434 freeze the train-only 64x256x1 packet representation and the
  Monday-Wednesday TRAIN plus Thursday VALIDATION compact-corpus receipts.
- Cells 435-454 preserve the sole masked-CNN architecture, seed 42, ten fixed
  epochs, isolated P100 runtime, one Thursday pass and frozen thresholds 0.50
  and 0.17.
- Cells 455-461 map only to the E4 prelock, one Kaggle opening attempt stopped
  by the operational storage gate, and subsequent diagnostics/cleanup audits.
  Seven later Colab/Xet and completed Friday artifacts are frozen repository
  evidence with status `NOTEBOOK_CELL_NOT_MAPPED`.
- Extracted interfaces are the ten subpackages under
  `src/ids_validation/stages/stage20/`, the static masked-CNN model spec, six
  Stage20 config files and `scripts/reproduce_stage20.py`.
- No source download, PCAP parse, flow reconstruction, packet-image or corpus
  regeneration, checkpoint load, training, inference, threshold selection, or
  Thursday/Friday opening is exposed or performed.

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
