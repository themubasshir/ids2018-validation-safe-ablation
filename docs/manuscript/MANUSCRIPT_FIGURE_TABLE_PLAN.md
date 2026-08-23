# Pass 1 Figure and Table Plan

Status: evidence-governed assembly plan only. Pass 1 does not redraw, merge, crop, recolor, relabel, or recompute any scientific figure. Where Stage 29 says `COMBINE_LATER`, this file records the intended panel order for a later authorized production pass; the source assets remain separate and unchanged.

The authoritative inventories are:

- `results/stage29_manuscript_synthesis/figures/final_figure_registry.csv`
- `results/stage29_manuscript_synthesis/figures/final_table_registry.csv`
- `results/stage29_manuscript_synthesis/manuscript/claim_figure_table_graph.csv`

## Main figures

| Manuscript exhibit | Stage 29 candidate(s) | Frozen source asset(s) | Main-text purpose | Required caption boundary | Pass 1 action |
| --- | --- | --- | --- | --- | --- |
| Figure 1. Temporal ranking transfer | `fig22r_1_validation_to_final_pr_auc`; `fig22r_2_validation_to_final_roc_auc` | `figures/stage22r_temporal_validation/fig22r_1_validation_to_final_pr_auc.png`; `figures/stage22r_temporal_validation/fig22r_2_validation_to_final_roc_auc.png` | Keep PR-AUC and ROC-AUC transfer visible as separate native metrics | Same shared forward target; frozen development geometries; finite seed set; chronology and family composition remain entangled; 5/5 is descriptive | Record later panel order: PR-AUC as (a), ROC-AUC as (b). Do not combine in Pass 1. |
| Figure 2. Shortcut-subset and split interaction | `figure_23_a_subset_split_interaction` | `results/stage23_shortcut_feature_audit/stage23_7_final_synthesis/figures/figure_23_a_subset_split_interaction.png` | Show that feature-subset effects vary with split geometry | Seven frozen subsets and evaluated learners; sensitivity is not proof of leakage or a causal transfer mechanism; placebo controls remain relevant | Use the approved asset unchanged. |
| Figure 3. Bidirectional cross-dataset ranking | `fig24_1_normalized_pr_auc_directionality`; `fig24_2_roc_auc_directionality` | `figures/stage24_cross_dataset/fig24_1_normalized_pr_auc_directionality.svg`; `figures/stage24_cross_dataset/fig24_2_roc_auc_directionality.svg` | Preserve direction-specific PR-AUC and ROC-AUC rather than one average score | Frozen bridge62 contracts; source learners, target populations, prevalence, and feature semantics differ by direction | Record later panel order: normalized PR-AUC as (a), ROC-AUC as (b). Do not combine in Pass 1. |
| Figure 4. PPV under prevalence stress | `figure25_a_ppv_cliff` | `figures/stage25_prevalence_stress/figure25_a_ppv_cliff.svg` | Show the base-rate dependence of projected PPV | Analytic prior-probability shift with invariant TPR/FPR; workload and cost assumptions are frozen scenarios, not observed SOC outcomes | Use the approved asset unchanged. |
| Figure 5. Hardware-specific CPU/GPU p95 comparison | `F26_CPU1_GPU_P95_SPEEDUP` | `figures/stage26_deployment_profiling/F26_CPU1_GPU_P95_SPEEDUP.png` | Show that backend advantage varies by compatible model path | Batch, model group, timed component, hardware, software, and unsupported paths must remain explicit; no end-to-end or hardware-independent claim | Use the approved asset unchanged. |
| Figure 6. Eligible-family ranking and balanced recall | `stage27_primary_roc_auc_ci`; `stage27_balanced_recall_ci` | `results/stage27_loao_unseen_attack/stage27_4a_final_synthesis/figures/stage27_primary_roc_auc_ci.png`; `results/stage27_loao_unseen_attack/stage27_4a_final_synthesis/figures/stage27_balanced_recall_ci.png` | Separate family-specific ranking from frozen-threshold recall | Only eligible families; learners remain separate; Infiltration is descriptive with 36 positives; no aggregate zero-day score | Record later panel order: ROC-AUC as (a), balanced recall as (b). Do not combine in Pass 1. |

No new framework schematic is authorized in Pass 1. The integrated validity matrix is a table, not a newly plotted composite score.

### Caption and evidence ledger

| Manuscript figure | Source stage | Intended message | Caption draft | Evidence IDs |
| --- | --- | --- | --- | --- |
| Figure 1 | Stage22, with Stage28 stability closure | Ranking depends on frozen development geometry, while threshold transfer and causal attribution remain separate questions | **Temporal ranking transfer on the shared forward target.** Existing PR-AUC (a) and ROC-AUC (b) assets compare frozen development geometries. The chronological-over-random direction is stable in the finite Stage28 seed set, but the target was historically opened and chronology remains entangled with family composition. | `E29-020;E29-037;E29-038;E29-040` |
| Figure 2 | Stage23 | Shortcut-removal effects depend on split, learner, and control context | **Shortcut-subset sensitivity by validation geometry.** The approved Stage23 interaction asset reports native ranking metrics across the frozen feature subsets and split cells. Differences establish conditional sensitivity, not that a removed field is leakage or that it caused cross-dataset transfer behavior; matched-size placebos constrain interpretation. | `E29-022;E29-023` |
| Figure 3 | Stage24 | Cross-dataset transfer is directional under frozen semantic bridges | **Bidirectional cross-dataset ranking under bridge62.** Existing normalized PR-AUC (a) and ROC-AUC (b) assets retain the two source-to-target directions separately. Source learners, target populations, prevalence, and feature semantics differ, so the panels do not define one average transfer score. | `E29-024;E29-025` |
| Figure 4 | Stage25 | Projected PPV changes with prevalence and does not alone determine workload or yield | **Projected PPV under frozen prevalence stress.** Curves apply prior-probability shift while holding TPR and FPR fixed. They are analytic scenario translations—not observed SOC outcomes—and must be interpreted with the frozen traffic, analyst-time, capacity, and relative-cost assumptions. | `E29-028;E29-029;E29-030;E29-031` |
| Figure 5 | Stage26 | CPU/GPU advantage varies across compatible model paths | **Hardware-specific p95 CPU/GPU comparison at the frozen profiling boundary.** Ratios describe compatible probability-generation paths on the recorded hardware/software and batch conditions. Unsupported backends and capture-to-alert processing are outside the measurement boundary. | `E29-032;E29-033` |
| Figure 6 | Stage27, with Stage28 stability closure | Withheld-family ranking and balanced-threshold recall are family- and learner-specific | **Eligible-family LOAO ranking and balanced-threshold recall.** Existing ROC-AUC (a) and recall (b) assets retain learners and families separately. DOS and AUTH_BRUTE_FORCE were ineligible; Infiltration has 36 positives and remains descriptive; the exhibit is not an aggregate zero-day score. | `E29-034;E29-035;E29-036;E29-039` |

## Main tables

| Manuscript exhibit | Stage 29 candidate | Frozen source | Principal contents | Required boundary | Pass 1 treatment |
| --- | --- | --- | --- | --- | --- |
| Table 1. Conventional processed-reference holdout results | `T29-01_REFERENCE_BENCHMARK` | `docs/RESULTS_SUMMARY.md`, with every displayed scalar resolved through `final_manuscript_numbers.csv` | Validation-selected thresholds and holdout F1, F2, FPR, ROC-AUC, and PR-AUC | Processed/rebalanced reference membership; no temporal, cross-dataset, prevalence, or deployment inference | Compact main table; full uncertainty and calibration remain supplementary. |
| Table 2. Five-seed temporal stability | `T29-03_TEMPORAL_FIVE_SEED` | `results/stage28_stability_novelty_control/stage28_final_synthesis/stage28_final_stage22_shared_holdout_five_seed_summary.csv` | Mean, SD, and directional consistency for PR-AUC and ROC-AUC | Frozen Stage22/Stage28 protocol; shared historically opened target; 5/5 is descriptive | Main table supersedes single-seed emphasis. |
| Table 3. Primary bidirectional bridge62 transfer | `T29-04_BIDIRECTIONAL_TRANSFER` | `results/stage24_cross_dataset/stage24_publication_package/tables/table24_1_bidirectional_generalization.csv` | Direction-specific target population, prevalence, PR-AUC, and ROC-AUC | Do not average directions; bridge and target restrictions remain adjacent | Compact main table; flag sensitivity and thresholds remain supplementary. |
| Table 4. Selected 0.1% operating-point translations | `T29-05_OPERATIONAL_TRANSLATION` | `results/stage25_prevalence_stress/stage25_publication_package/tables/table25_1_standard_operational_translation_0p1pct.csv` | PPV, workload, and detection-yield counterexamples | Frozen prior-shift, traffic, service-time, capacity, and cost assumptions; projections are not observations | Selected main rows; full grids remain supplementary. |
| Table 5. Eligible-family conclusion stability | `T29-06_LOAO_STABILITY` | `results/stage28_stability_novelty_control/stage28_final_synthesis/stage28_final_loao_stability_registry.csv` | Family-specific stability classification and support boundary | No pooled novelty metric; DOS and AUTH_BRUTE_FORCE are ineligible; Infiltration remains descriptive | Compact main table; native seed42 and seed-level metrics remain supplementary. |
| Table 6. Integrated native-metric validity matrix | `T29-02_VALIDITY_AXIS_MATRIX` | `results/stage29_manuscript_synthesis/evidence/validity_axis_matrix.csv` | Question, principal observation, what survived, what failed, and interpretation ceiling by axis | Synthesis only; unlike metrics are not normalized or combined into a robustness score | Main framework table, transcribed without adding empirical results. |

## Supplement routing

All entries marked `SUPPLEMENT` in the final Stage 29 registries remain available but outside the main scientific narrative. The planned groups are:

1. Reference and historical audit: `T29-S01` through `T29-S05`, including split counts, conditional uncertainty, calibration, known-category support, and LIME reliability.
2. Shortcut audit: `T29-S06` through `T29-S11` plus the Stage 23 secondary subset, penalty, stump, proxy, placebo, and family-support figures. `T29-M01` is an assembly source only.
3. Cross-dataset audit: `T29-S12` through `T29-S14` plus the paired-effects and secondary-threshold figures. Cancelled cells remain administrative records, not negative scientific results.
4. Operational audit: `T29-S15` through `T29-S18` plus any approved secondary Stage 25 prevalence/cost figures.
5. Deployment audit: `T29-S19` through `T29-S24`, `T29-M02`, and the approved Stage 26 capacity, cold-start, component, memory, Pareto, representation, warm-latency, and warm-throughput figures. Model groups remain separate in any later merged table.
6. Novelty and stability audit: `T29-S25` through `T29-S27`, the Stage 27 PR-AUC figure, and frozen Stage 28 seed/control details.
7. Representation and architecture chronology: the Stage 18 graph and Stage 21 architecture figures remain supplement-only and retain their source and descriptive limitations. They do not support the main Results or Discussion narrative.

Assets classified `REMOVE` or `EXCLUDED` by Stage 29 are not planned for either the main paper or its core supplement. They remain in the repository for historical traceability.

## Later production checklist

A later, separately authorized manuscript-production pass may assemble paired panels, but it must:

- use the exact registered source assets;
- preserve panel-native metrics, legends, axes, and uncertainty conventions;
- add only layout-level panel labels and a scope-qualified caption;
- record the output hash and the source-to-panel mapping;
- avoid recomputing, redrawing, smoothing, normalizing, or rescaling scientific content;
- re-run the claim, number, figure, and table traceability checks before release.
