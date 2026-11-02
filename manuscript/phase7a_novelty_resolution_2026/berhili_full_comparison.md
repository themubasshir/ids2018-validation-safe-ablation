# Phase 7A — Berhili comparison

## Decision status

**Material overlap confirmed. Phase 7 writing remains gated pending review of this report.** Berhili, Chaieb, and Benabdellah directly occupy much of the protocol-bias and multi-axis evaluation space. The manuscript must not claim first, only, or most comprehensive status.

## Source and verification boundary

**Article:** Mohammed Berhili, Omar Chaieb, and Mohammed Benabdellah, “How Evaluation Protocol Choices Inflate Intrusion Detection Accuracy: A Three-Dataset Systematic Study,” *Computers & Security*, article 105218; DOI `10.1016/j.cose.2026.105218`. DOI/article metadata are verified. Publisher page retrieval returned HTTP 400 during this review. The DOI record exposed a volume-173 bibliographic record reporting 2027, while the reproducibility record and repository describe 2026 acceptance/publication context. The year discrepancy is retained rather than silently normalized.

**Package:** “Reproducibility package for ‘How Evaluation Protocol Choices Inflate Intrusion Detection Accuracy: A Three-Dataset Systematic Study,’” Zenodo DOI `10.5281/zenodo.23630499`, published October 25, 2026. Package metadata and contents were inspected. It contains code, scripts, indices, seeds, and result CSVs; source datasets are not redistributed. Package availability is not independent reproduction.

**Code inspected read-only:** repository README plus `run_bias_analysis.py`, `run_cross_dataset_aligned.py`, `run_ablation.py`, `run_benchmark.py`, `run_statistical_tests.py`, and `preprocessing.py`. Experiments were not run.

**Article-level limitation:** full ScienceDirect text and supplementary material were not independently inspected. Claims based only on README, scripts, package metadata, or accessible excerpts are marked accordingly. Missing material is not treated as absence.

## Verified implementation facts

- Three datasets are named in the implementation: UNSW-NB15, NSL-KDD, and CIC-IDS2017.
- The benchmark script documents seven model families and stratified five-fold CV; the package README also documents benchmark, AWE-IDS, bias, leakage, ablation, cross-dataset, grid-sensitivity, and statistical workflows.
- `run_bias_analysis.py` documents validation-split versus proper stratified evaluation, seed sensitivity, and preprocessing leakage.
- `run_cross_dataset_aligned.py` documents semantic feature alignment using UNSW-NB15 as a pivot, bidirectional transfer, and threshold/weight optimization.
- `run_ablation.py` documents weight-only, threshold-only, combined, and CNN-augmented ensemble conditions.
- `run_statistical_tests.py` documents Friedman, Nemenyi, and pairwise Wilcoxon procedures over fold scores.
- README metadata state fixed `random_state=42` for most workflows, with TensorFlow nondeterminism bounded rather than eliminated.
- Results are supplied as CSV artifacts. Dataset files are expected locally and are not included.

## Dimension-by-dimension comparison

| Dimension | Classification | Evidence and interpretation |
|---|---|---|
| Scientific problem | SUBSTANTIAL_OVERLAP | Both treat benchmark protocol choices as threats to IDS inference, not merely as model-selection problems. Berhili explicitly studies inflation from validation, leakage, seeds, alignment, and calibration. |
| Dataset population | DIFFERENT_EMPIRICAL_PROTOCOL | Berhili implementation: UNSW-NB15, NSL-KDD, CIC-IDS2017. This manuscript: CSE-CIC-IDS2018 with a restricted CICIDS2017 bridge. Dataset difference is empirical, not methodological novelty by itself. |
| Validation and temporal development | PARTIAL_OVERLAP | Berhili README/scripts document biased validation versus proper stratified evaluation and seed sensitivity. A temporal forward-development design was not verified in inspected scripts; article/supplement section remains NOT_VERIFIED. This manuscript has source-faithful chronological development and a common forward target. |
| Duplicate/session independence | NOT_VERIFIED | No sufficiently complete Berhili article/supplement inspection established treatment of latent sessions, duplicate-safe membership, or source-faithful row identity. No absence claim made. This manuscript's claim is limited to its own receipts and does not imply Berhili omission. |
| Model fitting and architectures | PARTIAL_OVERLAP | Both include tree ensembles and multiple learners. Berhili implementation includes XGBoost, LightGBM, RF, SVM and CNN-BiLSTM; this manuscript evaluates frozen study-specific realizations. Procedures and populations differ. |
| Threshold selection and transfer | SUBSTANTIAL_OVERLAP | Berhili scripts document deployable versus oracle calibration, threshold optimization, and AWE-IDS ablations. This manuscript separately evaluates frozen operating-point transfer under chronology and scenario-bound operating projections. The conceptual question overlaps; empirical protocols differ. |
| Shortcut-feature controls | PARTIAL_OVERLAP | Berhili documents preprocessing leakage analysis. Direct equivalence to this manuscript's registered feature subsets, placebo/stump controls, or proxy-absorption controls was not verified. |
| Explanation reliability | NOT_VERIFIED | Inspected Berhili README/scripts did not establish a comparable LIME/SHAP local-fidelity analysis. Full article/supplement not available; no absence claim. This manuscript's LIME/TreeSHAP findings remain study-specific. |
| Semantic cross-dataset bridges | SUBSTANTIAL_OVERLAP | Berhili explicitly documents semantic alignment and bidirectional aligned transfer. This manuscript also uses frozen semantic bridges, with different source/target populations, bridge contracts, and two cancelled GROUNDED_S4 cells. |
| Prevalence/workload/cost | NOT_VERIFIED | No comparable prevalence-grid, alert-volume, analyst-hours, or relative-cost analysis was established from inspected Berhili artifacts. Full article/supplement uncertainty remains. |
| Hardware-specific profiling | NOT_VERIFIED | Package README contains runtime/hardware notes, but no verified counterpart to this manuscript's component-level CPU/T4 latency, throughput, memory, artifact-size, and backend-status audit. Treat as unresolved, not absent. |
| Eligible-family LOAO | NOT_VERIFIED | No LOAO procedure was found in the inspected scripts. Full article/supplement remains incomplete; absence is not asserted. |
| Seed stability and causal controls | SUBSTANTIAL_OVERLAP / PARTIAL_OVERLAP | Berhili documents 100-seed sensitivity in its bias analysis and fixed-seed workflows. This manuscript has five registered seeds, family-aware controls, and an explicit failure to isolate one causal mechanism. Seed questions overlap; controls and estimands differ. |
| Reproducibility artifacts | SUBSTANTIAL_OVERLAP | Both provide claim/evidence documentation and reproducibility-oriented artifacts. Berhili provides code, indices, seeds, and result files. This manuscript adds claim-level provenance, frozen-artifact status, cancellation governance, and explicit availability boundaries. Documentation is not methodological novelty by itself. |
| Negative findings and cancellations | NOT_VERIFIED | Berhili result files document several protocol effects, but inspected artifacts did not establish a counterpart to this manuscript's administratively cancelled cells and unsupported-path governance. Full supplementary inspection is required. |

## Direct overlap versus supported difference

**Substantial overlap:** protocol bias; validation-split effects; seed sensitivity; preprocessing leakage; semantic cross-dataset transfer; calibration/threshold behavior; statistical testing; reproducibility artifacts; protocol-dependent ranking.

**Supported empirical differences:** this manuscript evaluates source-faithful CSE-CIC-IDS2018 chronology, frozen operating-point transfer on a common forward target, direction-specific IDS2018/CICIDS2017 bridge results, registered shortcut/placebo controls, prevalence/workload projections, measured hardware paths, eligibility-gated LOAO, and explicit cancelled-cell/evidence-state reporting. These are differences in evaluated population, protocol, and findings. They do not establish broad methodological priority over Berhili.

**Not safe to claim:** that Berhili omitted temporal evaluation, explanations, prevalence, hardware, LOAO, or cancellation governance. Those dimensions remain `NOT_VERIFIED` where inspection was incomplete.

## Required positioning change

Replace any generic “integrated multi-axis framework” novelty implication with a bounded statement: **a source-faithful empirical audit of CSE-CIC-IDS2018 and a restricted CICIDS2017 bridge, using frozen contracts and evidence-state governance to report how selected conclusions change across chronology, operating-point transfer, feature sensitivity, transfer direction, prevalence/workload projections, measured computational paths, eligible withheld families, and finite model realizations.**

The scientific contribution is the bounded empirical pattern and its interpretation ceilings—not invention of temporal validation, semantic alignment, calibration, LOAO, hardware profiling, or reproducibility practice.

## Verification conclusion

Berhili is a direct high-overlap comparator. The additional Biswas (2026) preprint further establishes temporal-protocol sensitivity on CSE-CIC-IDS2018, cross-dataset behavior, calibration limits, and unseen-family framing. It therefore removes any defensible conceptual-priority claim for temporal or attack-family evaluation. The manuscript remains potentially publishable only after narrowing claims, explicitly acknowledging overlap, and demonstrating why its completed empirical chain yields useful bounded observations beyond these comparators. Phase 7B prose is unsafe until this decision is reviewed.
