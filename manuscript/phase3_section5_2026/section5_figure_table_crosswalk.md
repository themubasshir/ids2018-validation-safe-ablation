# Section 5 Figure/Table Crosswalk

All assets remain frozen. No figure was regenerated, merged, redrawn, cropped, relabeled, or numerically altered. `T29-*` and `E29-*` identifiers are registry identifiers, not final LaTeX numbering.

## Approved main figures

| Manuscript figure | Frozen source asset(s) | Results text | Evidence | Caption qualification |
|---|---|---|---|---|
| Figure 1. Temporal ranking transfer | `figures/stage22r_temporal_validation/fig22r_1_validation_to_final_pr_auc.png`; `figures/stage22r_temporal_validation/fig22r_2_validation_to_final_roc_auc.png` | 5.2 | E29-020; E29-037; E29-038; E29-040 | PR-AUC and ROC-AUC remain separate panels; shared historically opened target; 5/5 descriptive; chronology/family composition entangled |
| Figure 2. Shortcut-subset and split interaction | `results/stage23_shortcut_feature_audit/stage23_7_final_synthesis/figures/figure_23_a_subset_split_interaction.png` | 5.3 | E29-022; E29-023 | Seven frozen subsets; sensitivity is not leakage or causal proof; placebo controls remain relevant |
| Figure 3. Bidirectional cross-dataset ranking | `figures/stage24_cross_dataset/fig24_1_normalized_pr_auc_directionality.svg`; `figures/stage24_cross_dataset/fig24_2_roc_auc_directionality.svg` | 5.4 | E29-024; E29-025; E29-026 | Direction-specific bridge62 results; source learners, target populations, prevalence, and semantics differ; no average transfer score |
| Figure 4. PPV under prevalence stress | `figures/stage25_prevalence_stress/figure25_a_ppv_cliff.svg` | 5.5 | E29-028; E29-029; E29-030; E29-031 | Analytic fixed-TPR/FPR prior shift; traffic, service time, capacity, and cost assumptions; not SOC observation |
| Figure 5. Hardware-specific CPU/GPU p95 comparison | `figures/stage26_deployment_profiling/F26_CPU1_GPU_P95_SPEEDUP.png` | 5.6 | E29-032; E29-033 | Compatible prepared-input-to-probability paths only; batch/hardware/software-specific; unsupported paths are statuses; no E2E latency |
| Figure 6. Eligible-family ranking and balanced recall | `results/stage27_loao_unseen_attack/stage27_4a_final_synthesis/figures/stage27_primary_roc_auc_ci.png`; `results/stage27_loao_unseen_attack/stage27_4a_final_synthesis/figures/stage27_balanced_recall_ci.png` | 5.7–5.8 | E29-034; E29-035; E29-036; E29-039 | Learners/families separate; DOS and AUTH_BRUTE_FORCE ineligible; Infiltration 36 positives, descriptive; no zero-day aggregate |

## Approved main tables

| Manuscript table | Frozen source artifact | Results text | Evidence | Caption qualification |
|---|---|---|---|---|
| Table 1. Conventional processed-reference holdout | `docs/RESULTS_SUMMARY.md`; scalar resolution through `results/stage29_manuscript_synthesis/evidence/final_manuscript_numbers.csv` | 5.1 | E29-004; E29-005; E29-006; E29-007; E29-009; E29-010; E29-011 | Validation-selected thresholds; processed/rebalanced reference only; uncertainty/calibration supplementary |
| Table 2. Five-seed temporal stability | `results/stage28_stability_novelty_control/stage28_final_synthesis/stage28_final_stage22_shared_holdout_five_seed_summary.csv` | 5.2, 5.8 | E29-037; E29-038 | Mean/SD over five frozen realizations; shared historical target; 5/5 descriptive, not significance |
| Table 3. Primary bidirectional bridge62 transfer | `results/stage24_cross_dataset/stage24_publication_package/tables/table24_1_bidirectional_generalization.csv` | 5.4 | E29-024; E29-025 | Directions and populations not pooled; prevalence contextualizes PR-AUC |
| Table 4. Selected 0.1% operating-point translations | `results/stage25_prevalence_stress/stage25_publication_package/tables/table25_1_standard_operational_translation_0p1pct.csv` | 5.5 | E29-028; E29-029; E29-030; E29-031 | Conditional analytic projections; one-million-flow, service-time, capacity, and cost assumptions |
| Table 5. Eligible-family conclusion stability | `results/stage28_stability_novelty_control/stage28_final_synthesis/stage28_final_loao_stability_registry.csv` | 5.7, 5.8 | E29-034; E29-035; E29-036; E29-039 | Stability classification, not pooled novelty score; support and eligibility boundaries |
| Table 6. Integrated native-metric validity matrix | `results/stage29_manuscript_synthesis/evidence/validity_axis_matrix.csv` | 5.9 | CLM29-001; CLM29-008; CLM29-010; CLM29-011; CLM29-013; CLM29-014; CLM29-015 | Synthesis only; unlike metrics not normalized or combined |

## Supplement routing

- S1: reference uncertainty, calibration, known-category support, LIME reliability.
- S2: Stage23 subsets, interactions, placebos, stumps, proxies, Stage18/21 descriptive representation and architecture diagnostics.
- S3: bridge62/bridge70 sensitivity, threshold transfer, paired contrasts, cancellation governance.
- S4: full prevalence, workload, capacity, and cost grids.
- S5: detailed Stage26 latency, throughput, memory, package, component, backend, and Pareto records.
- S6: full LOAO metrics, intervals, seed-level family stability, and controls.
- S7: provenance, equivalence, and reproduction boundaries.

Stage29 candidate IDs are retained for traceability only. Published supplement references use S1–S7 and Tables S1–S10.
