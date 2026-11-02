# Section 5 Scientific Validation Report

## Gate and source verification

Repository: `themubasshir/ids2018-validation-safe-ablation`
Worktree: `D:\ids2018-journal-revision`
Branch: `manuscript-journal-revision-2026`
HEAD: `2a6b68969d7e8fb096504773b6676c145e1bb1af`

Git status before Phase 3 creation contained only untracked Phase 1 and Phase 2 isolated drafts. No canonical manuscript, LaTeX source, figure, table, notebook, protocol, result, registry, or bibliography was modified.

Reviewed before writing:

- All four Phase 1 deliverables.
- All four Phase 2 deliverables.
- `master_evidence_matrix.csv`.
- `final_manuscript_numbers.csv`.
- `final_claim_registry.csv`.
- `claim_figure_table_graph.csv`.
- `validity_axis_matrix.csv`.
- `final_figure_registry.csv` and `final_table_registry.csv`.
- `MANUSCRIPT_SOURCE_MAP.csv` and `MANUSCRIPT_FIGURE_TABLE_PLAN.md`.
- `submission/jisa/manuscript.tex` and `submission/jisa/supplement/supplement.tex`.
- Frozen Stage22R, Stage24, Stage25, Stage26, and Stage27 manuscript integration records.
- Original result tables for Stage23, Stage24, Stage25, and Stage28.
- Stage01–28 code inventory and final reproducibility audit.

## Stages inspected

Results coverage includes Stages 1–14, 18, 20–21, 22/22R, 23, 24, 25, 26, 27, and 28. Stages15–21 historical architecture and representation work is explicitly bounded: Stage18 tabular ViT feasibility is a zero-pass rejection, Stage18 graph results and Stage21 CNN/ViT comparison remain descriptive/supplement-only, and no architecture-superiority claim is promoted.

## Numerical verification

The traceability CSV contains **22 material numerical claim records**. Values were checked against the Stage29 number registry and, where available, canonical artifacts:

- `docs/RESULTS_SUMMARY.md` for reference metrics, uncertainty, calibration, category support, and seed context.
- `results/stage22r_training/stage22r_final_single_holdout/stage22r_final_holdout_result.json` and `docs/STAGE22R_MANUSCRIPT_INTEGRATION.md` for temporal ranking and threshold transfer.
- `results/stage23_shortcut_feature_audit/stage23_7_final_synthesis/tables/table_23_1_primary_subset_performance.csv` and `table_23_2_primary_removal_penalties_and_interactions.csv` for subset values and interactions.
- `results/stage24_cross_dataset/stage24_publication_package/tables/table24_1_bidirectional_generalization.csv` and Stage24 integration/closeout records for direction-specific transfer and cancellation.
- `results/stage25_prevalence_stress/stage25_publication_package/tables/table25_1_standard_operational_translation_0p1pct.csv` and Stage25 integration for projections.
- `results/stage26_deployment_profiling/stage26_publication_package/tables/T26_CPU1_GPU_BATCH1_ANCHOR.csv` and Stage26 integration for p95 ratios and boundaries.
- `results/stage27_loao_unseen_attack/stage27_4a_final_synthesis/stage27_final_primary_metrics.csv` and Stage27 integration for family metrics.
- Stage28 five-seed summary, LOAO stability registry, final synthesis, and closure artifacts.

No new confidence interval, p-value, bootstrap distribution, metric, or empirical comparison was calculated.

## Population separation checks

Preserved distinctions:

1. Processed, stratified CSE-CIC-IDS2018 reference: 78 predictors; reference holdout.
2. Source-faithful K79-clean IDS2018 temporal development and Mar1–Mar2 target: ordered 70-feature model representation.
3. IDS2018→CICIDS2017 and CICIDS2017→IDS2018 direction-specific transfer populations.
4. Bridge62 versus bridge70 published/corrected contracts.
5. Processed known-category `Infilteration` support 3,967 versus LOAO `Infiltration` support 36.
6. Eligible LOAO families versus structurally ineligible DOS and AUTH_BRUTE_FORCE.
7. Analytic Stage25 projections versus observed/frozen model metrics.
8. Stage26 component profiling versus end-to-end deployment.
9. Historical/descriptive Stage18 and Stage21 architecture evidence versus principal results.

K79 is described only as exact corrected-second-plus-78-predictor identity control. No session, endpoint, source-IP, five-tuple, or S4 independence claim appears.

## Cross-table and cross-source consistency

- Table 1 values match `docs/RESULTS_SUMMARY.md` and `NUM29-014`–`NUM29-029`.
- Table 2 values match the Stage28 seed summary and `NUM29-135`–`NUM29-144`.
- Table 3 values match `table24_1_bidirectional_generalization.csv` and `NUM29-090`–`NUM29-098`.
- Table 4 values match `table25_1_standard_operational_translation_0p1pct.csv` and `NUM29-100`–`NUM29-110`.
- Table 5 classifications match the Stage28 LOAO stability registry and `E29-034`–`E29-039`.
- Table 6 is transcribed from `validity_axis_matrix.csv`; no composite score was introduced.
- Figure mappings match `MANUSCRIPT_FIGURE_TABLE_PLAN.md`, `final_figure_registry.csv`, and `claim_figure_table_graph.csv`.

## Negative, cancelled, and unsupported results preserved

- Balanced learner difference unresolved; no equivalence claim.
- No resolved calibration winner.
- LIME frequently fidelity-limited despite perturbation stability.
- Stage18 seven tabular ViT representations: zero passed feasibility; no performance result.
- Reverse transfer near baseline.
- Bridge70 correction changed metrics in different directions.
- Two `GROUNDED_S4` cells cancelled before opening; no measurements.
- Chronological thresholds almost never fired; random security FPR exceeded development constraints.
- Unsupported Stage26 backends remain unsupported, not poor performers.
- DOS and AUTH_BRUTE_FORCE LOAO folds ineligible.
- Infiltration LOAO remains descriptive at 36 positives.
- Stage28 controls mixed/family-specific; no single mechanism isolated.

## Stage23 K79 wording treatment

The draft follows the authoritative Stage22R K79 definition. Historical broader Stage23 wording is not propagated. The discrepancy remains documented; no historical artifact was edited.

## Main/supplement routing

The six approved main figures and six approved main tables retain the Stage29 mapping. Stage23 detailed subsets/placebos, LIME/TreeSHAP/Integrated Gradients detail, Stage18 graph, Stage21 CNN/ViT comparison, transfer sensitivity, full operational grids, Stage26 detail, LOAO native metrics, and provenance records remain routed to S1–S7 and Tables S1–S10 per the existing supplement plan.

## Scientific discrepancies and unresolved issues

1. Historical Stage23 wording remains broader than authoritative K79 language.
2. `T29-06_LOAO_STABILITY` is a stability-classification table; native seed42 family metrics remain supplementary.
3. Stage26 registry marks `F26_CPU1_GPU_P95_SPEEDUP` as the approved main asset, while detailed deployment measurements remain supplement-only; no unsupported path was numerically filled.
4. The Stage29 six-figure architecture requires later panel assembly (`COMBINE_LATER`), which was not performed here.
5. Phase 2 traceability was adequate for method coverage, but Phase 3 uses an expanded 22-record numerical claim matrix for result-level traceability.

## Readiness

Section 5 is complete as an isolated, evidence-traced Results draft. Main/supplement boundaries remain intact. Section 6 requires a separate authorized phase. No scientific artifact was altered, and no new scientific computation was performed.
