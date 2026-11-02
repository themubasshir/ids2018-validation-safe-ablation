# Section 6 Scientific Validation Report

## Scope and repository gate

Repository: `themubasshir/ids2018-validation-safe-ablation`
Worktree: `D:\ids2018-journal-revision`
Branch: `manuscript-journal-revision-2026`
HEAD before Phase 4 edits: `ab0440696d1ca9a7e4d804f172ac10df30e10943`
Working tree was clean before the isolated Phase 4 package was created.

Phase 4 remained isolated. No canonical manuscript, submission LaTeX, supplement source, figure, table, notebook, configuration, frozen result, registry, or experimental artifact was modified. No training, inference, target opening, tuning, resampling, metric recomputation, or new scientific computation was performed.

## Source verification

Reviewed directly:

- Phase 1 Section 3, evidence traceability, and provenance/reproducibility boundaries.
- Phase 2 Section 4, 15-record method traceability matrix, and method scope.
- Phase 3 Section 5, 22-record result traceability matrix, figure/table crosswalk, and scientific validation report.
- Phase 3 Discussion handoff outline.
- `results/stage29_manuscript_synthesis/claims/final_claim_registry.csv`.
- `results/stage29_manuscript_synthesis/claims/claims_to_rewrite.csv`.
- `results/stage29_manuscript_synthesis/claims/claims_to_remove.csv`.
- `results/stage29_manuscript_synthesis/claims/claim_to_artifact_map.csv`.
- `results/stage29_manuscript_synthesis/manuscript/claim_figure_table_graph.csv`.
- `results/stage29_manuscript_synthesis/evidence/validity_axis_matrix.csv`.
- `results/stage29_manuscript_synthesis/manuscript/limitations_matrix.csv`.
- `results/stage29_manuscript_synthesis/evidence/final_manuscript_numbers.csv`.
- `results/stage29_manuscript_synthesis/evidence/master_evidence_matrix.csv`.
- `submission/jisa/manuscript.tex`.
- `submission/jisa/supplement/supplement.tex`.

Material Discussion claims were checked against the authoritative Stage29 claims, evidence IDs, source artifacts, and the Sections 3–5 population boundaries. No material scientific contradiction was discovered.

## Supplement cross-reference correction

The actual supplement captions establish:

- Table S7: `Representative approved CPU warm-inference measurements` — deployment profiling.
- Table S8: `Family-level LOAO primary metrics` — LOAO primary metrics.
- Table S9: `Five-seed Stage 22 stability summary` — temporal stability.
- Table S10: `Evidence classification and reproduction boundary` — provenance/reproduction.

Corrected in the isolated Phase 3 Results draft:

1. Section 5.6 now cites Supplement S5 and Table S7 for deployment detail rather than Tables S7–S10.
2. Section 5.7 now cites Supplement S6 and Table S8 for LOAO metrics, with temporal stability explicitly assigned to Table S9.

Full errata: `phase3_cross_reference_errata.md`.

## Discussion claim verification

The claim-evidence matrix contains 18 substantive Discussion records covering Sections 6.1–6.10. The records map each statement to approved claim IDs, evidence IDs or provenance records, source artifacts, exhibits, support class, and interpretation limit.

Verified boundaries preserved:

- Strong reference discrimination remains within-reference evidence, not deployment evidence.
- Temporal ranking and operating-point transfer remain separate.
- Five-seed ordering remains descriptive, not significance or population-level evidence.
- Chronology and family composition remain entangled.
- K79 is limited to exact corrected-second-plus-predictor identity control.
- Shortcut effects remain sensitivity evidence, not leakage or causal proof.
- TreeSHAP, LIME, Integrated Gradients, and attention evidence retain their model/context limits.
- Bridge62 and bridge70 remain separate semantic contracts.
- Direction-specific transfer is not averaged or generalized to arbitrary datasets.
- Cancelled `GROUNDED_S4` cells remain missing evidence, not negative results.
- Stage25 quantities remain analytic prior-shift projections, not SOC observations.
- Stage26 remains component-, hardware-, software-, backend-, and batch-specific.
- Historical architecture branches remain separate, descriptive, negative, or supplement-only as registered.
- LOAO remains selective family transfer, not universal zero-day detection.
- DOS and AUTH_BRUTE_FORCE remain ineligible; Infiltration remains descriptive at 36 positives.
- Known-category `Infilteration` support 3967 remains separate from LOAO `Infiltration` support 36.
- Stage28 controls do not identify a unique causal mechanism.
- Reproducibility claims distinguish deterministic scalar reproduction, archival methodology, static evidence, hashes, closed targets, unavailable inputs, and unavailable environments.
- Stage29 is treated as synthesis, not empirical computation.

## Unsupported or excluded claims

No external-paper comparison was introduced. No new metric, p-value, confidence interval, causal mechanism, robustness score, deployment claim, zero-day claim, or architecture ranking was introduced. Prohibited claims CLM29-017 and CLM29-018 and rewrite constraints CLM29-019 and CLM29-020 were respected.

## Phase 2 operation-level traceability review

The 15 Phase 2 records cover the major method families and their principal protocols, but they do not provide exhaustive one-record-per-operation coverage. Explicit gaps requiring author awareness:

1. Reference operations are grouped across Stages 1–5 and 8–12; scaler fitting, learner inventory, validation search, threshold-grid/tie-breaking, holdout locking, uncertainty, calibration, cost, category, and seed procedures are not each represented as separate traceability records.
2. Temporal cleaning, K79 canonicalization, duplicate/conflict handling, factorial cell construction, equal-weight ensemble formation, threshold roles, and one-time target opening are grouped under S4-003 rather than individually recorded.
3. Stage23's seven-subset construction, matched-size placebo design, stump probes, proxy diagnostics, family-support accounting, interaction estimation, and explanation panel are grouped under S4-006.
4. Stage24 bridge construction, direction-specific source/target contracts, serialization correction, paired bootstrap, threshold transfer, and cancellation governance are grouped under S4-007.
5. Stage25 equations, prevalence grid, traffic, analyst service time, capacity, and relative-cost calculations are grouped under S4-008.
6. Stage26 warm/cold profiling, p95 extraction, throughput, memory, artifact size, batch grid, backend status, and component boundary are grouped under S4-009.
7. Stage27 eligibility, day-atomic ordering, support gate, known-family threshold selection, family metrics, and bootstrap are grouped under S4-011.
8. Stage28 seed linkage, artifact reuse, temporal summary, LOAO stability registry, matched random-LOAO controls, and empirical closure are grouped under S4-012.

These are traceability granularity gaps, not confirmed scientific contradictions. The Discussion does not claim that the 15 records are exhaustive. Phase 3's 22-record matrix covers material numerical result claims, not every implementation operation.

## Consistency with Sections 3–5

- Population distinctions remain aligned with Section 3.
- Methodological interpretation remains aligned with Section 4.
- Numerical and exhibit references remain aligned with the corrected Section 5.
- Processed known-category `Infilteration` and LOAO `Infiltration` remain distinct.
- Supplement references now match the actual S7–S10 captions.
- No canonical manuscript or LaTeX integration was performed.

## Deliverables and readiness

Created:

- `section6_discussion.md`
- `section6_claim_evidence_matrix.csv`
- `section6_scientific_validation_report.md`
- `section7_limitations_handoff_outline.md`
- `phase3_cross_reference_errata.md`

Section 6 is complete as an isolated Discussion draft. Section 7 remains an outline only. Readiness: suitable for author review and separate Section 7 authorization, subject to review of the documented Phase 2 traceability granularity gaps. No push, commit, merge, rebase, or canonical manuscript modification was performed.
