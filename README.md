# IDS2018 Validation-Safe Threshold Ablation

This repository publishes a clean, reproducible validation-safe refinement of the IDS2018 explainable threshold ablation experiment. The goal is methodological hygiene: use validation data for model and threshold selection, reserve the holdout set for final descriptive reporting, and preserve the original experiment lineage without redistributing raw CSE-CIC-IDS2018 data.

Original repository: https://github.com/themubasshir/ids2018-explainable-threshold-ablation

## Workflow

```mermaid
flowchart LR
  A["Processed CSE-CIC-IDS2018 binary dataset"] --> B["64/16/20 stratified split, seed 42"]
  B --> C["StandardScaler fit on training only"]
  C --> D["16-model validation baseline"]
  D --> E["Tune top five on training data"]
  E --> F["Validation threshold selection"]
  F --> G["Holdout-only final reporting"]
  G --> H["Dual-model SHAP on shared holdout sample"]
```

## Experiment Overview

- Dataset: rebalanced binary CSE-CIC-IDS2018 processed dataset.
- Records: 300,928 total, with 180,000 benign and 120,928 attack records.
- Predictors: 78 features; `Label` and `binary_label` are excluded from predictors.
- Split: 192,593 training records, 48,149 validation records, and 60,186 holdout test records.
- Random state: 42.
- Scaling: `StandardScaler` fit only on the training split.
- Baseline: 16 validation-evaluated models.
- Tuned top five: XGBoost, LightGBM, CatBoost, MLP, and 1D-CNN.

![Tuned top-five validation F1 comparison](figures/figure02_tuned_top5_f1_comparison.png)

## Key Results

The balanced operating point is XGBoost Tuned at validation-selected threshold `0.51`. On the holdout test set it reached precision `0.9897505499134179`, recall `0.8743901430579675`, F1 `0.9285008671218141`, FPR `0.006083333333333333`, ROC-AUC `0.9801912125472036`, and PR-AUC `0.9776433333080397`.

The constrained-security operating point is LightGBM Tuned at validation-selected threshold `0.26`, selected by maximum validation F2 subject to FPR <= 5%. On the holdout test set it reached precision `0.9290071162317859`, recall `0.90680559001075`, F1 `0.9177721052851823`, F2 `0.9111605955862803`, FPR `0.04655555555555556`, and FN `2254`.

![Final holdout objective comparison](figures/figure06_final_holdout_objective_comparison.png)

## Explainability

Dual-model SHAP uses an identical deterministic stratified holdout sample of 5,000 records: 2,500 benign and 2,500 attack. XGBoost and LightGBM share 15 of their top-20 features, with top-20 Jaccard similarity `0.6`, all-feature Spearman rank correlation `0.8540662778147889`, and p-value `2.839526154790284e-23`. The common top three features are `Init Fwd Win Byts`, `Fwd Seg Size Min`, and `Dst Port`.

![SHAP rank agreement](figures/figure09_shap_rank_agreement.png)

## Journal-Extension Analyses

Stages 8-12 add journal-strengthening robustness and deployment analyses.

1. Bootstrap confidence: balanced XGBoost and LightGBM differences are statistically unresolved because all major paired confidence intervals include zero. See `docs/STATISTICAL_CONFIDENCE.md`.
2. Calibration: both selected models are reasonably calibrated, with no statistically resolved calibration winner and no recalibration performed. See `docs/CALIBRATION_ASSESSMENT.md`.
3. Operational cost: LightGBM security becomes preferable to LightGBM balanced when one missed attack costs more than `1.8407079646017699` false-positive investigations. See `docs/OPERATIONAL_COST_ANALYSIS.md`.
4. Attack categories: residual errors are concentrated mainly in `Infilteration` and `Brute Force -Web`; most DoS/DDoS and FTP brute-force categories reached 100% detection. See `docs/ATTACK_CATEGORY_ANALYSIS.md`.
5. Multi-seed robustness: XGBoost was selected for the balanced objective in `3/5` fixed-hyperparameter runs, and LightGBM was selected for the security objective in `4/5`. See `docs/MULTISEED_ROBUSTNESS.md`.

![Bootstrap operating-point intervals](figures/statistical_confidence/figure_bootstrap_operating_point_intervals.png)

![Calibration metric intervals](figures/calibration/figure_calibration_metric_intervals.png)

![Break-even cost ratios](figures/operational_cost/figure_break_even_cost_ratios.png)

![Attack-category detection rates](figures/attack_category/figure_attack_category_detection_rates.png)

![Multi-seed winner frequency](figures/multiseed/figure_multiseed_winner_frequency.png)

The cross-stage interpretation is summarized in `docs/JOURNAL_EXTENSION_SUMMARY.md`, and manuscript figure recommendations are listed in `figures/JOURNAL_FIGURE_INDEX.md`.

## Repository Structure

- `metadata/`: split metadata, feature names, scaler, checksums, environment details, and validation report.
- `results/baseline/`: 16-model validation ablation outputs.
- `results/tuning/`: top-five tuning outputs, probabilities, histories, parameters, and manifests.
- `results/threshold/`: validation threshold sweeps and operating-point selections.
- `results/holdout/`: final holdout summaries and probability files for selected objectives.
- `results/shap/`: SHAP top-feature tables and rank-comparison CSVs.
- `results/statistical_confidence/`: Stage 8 paired bootstrap confidence outputs.
- `results/calibration/`: Stage 9 calibration metrics, bins, and bootstrap intervals.
- `results/operational_cost/`: Stage 10 cost-ratio and break-even analyses.
- `results/attack_category/`: Stage 11 category-level detection and paired tests.
- `results/multiseed/`: Stage 12 fixed-hyperparameter multi-seed robustness outputs.
- `results/comparison/`: generated Markdown summaries from CSV artifacts.
- `models/`: portable top-five tuned model artifacts.
- `figures/` and `tables/`: publication figures and CSV/LaTeX tables.
- `docs/`: detailed protocol, comparison with the original repository, and exact result summary.
- `scripts/`: repository validation and generated-report utilities.

## Setup

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python scripts\generate_comparison_report.py
python scripts\validate_repository.py
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/generate_comparison_report.py
python scripts/validate_repository.py
```

## Kaggle Reproduction Notes

The archived experiment references `/kaggle/input/datasets/jmmubasshirrahman/ids2018-balanced-binary-dataset/merged_balanced_ids2018_safe.csv`. Place the processed dataset locally according to `DATASET.md` if you need to reproduce training, tuning, and threshold sweeps. Raw and processed dataset files are intentionally not redistributed in this repository.

## Limitations

This repository preserves exact archived metrics and artifacts, but it does not fabricate missing outputs. The copied notebook is the available Kaggle working notebook from the archive bundle; additional stage-specific notebooks were not present. Large raw SHAP matrices and oversized baseline joblib artifacts remain in the full archive rather than Git.

## Citation

If you use this repository, cite the CSE-CIC-IDS2018 dataset source and this validation-safe reproducibility repository. This work should be read as a methodological refinement, robustness analysis, and reproducibility extension of the original experiment.

<!-- BEGIN STAGE 13 LOCAL EXPLANATION RELIABILITY -->
## Stage 13: Local Explanation Reliability

The repository now includes an outcome-stratified local explanation
audit for the selected XGBoost and LightGBM models.

Key findings:

- TreeSHAP reconstructs both tree-model outputs to numerical precision.
- LIME feature rankings are comparatively repeatable across seeds.
- LIME stability does not imply local faithfulness.
- Only 2 of 64 representative LIME explanations satisfy all
  study-specific fidelity and TreeSHAP-agreement criteria.
- TreeSHAP is the primary local explanation method.
- LIME is reported as a supplementary surrogate-reliability stress test.

Detailed findings are available in
[`docs/STAGE13_LOCAL_EXPLANATION_RELIABILITY.md`](docs/STAGE13_LOCAL_EXPLANATION_RELIABILITY.md).
Publication tables are under `tables/lime/`, figures under
`figures/lime/`, detailed results under `results/lime/`, and
reproducibility artifacts under `metadata/lime/`.
<!-- END STAGE 13 LOCAL EXPLANATION RELIABILITY -->
