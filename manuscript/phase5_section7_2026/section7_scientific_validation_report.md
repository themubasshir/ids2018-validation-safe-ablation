# Section 7 Scientific Validation Report

## Scope and source verification

Repository: `themubasshir/ids2018-validation-safe-ablation`
Worktree: `D:\ids2018-journal-revision`
Branch: `manuscript-journal-revision-2026`
HEAD before Phase 5 creation: `ab0440696d1ca9a7e4d804f172ac10df30e10943`

The working tree contained the authorized Phase 4 package and the Phase 3 editorial correction before Phase 5. Those changes were preserved. Phase 5 was created under a new isolated directory. No commit, push, branch change, reset, rebase, or merge was performed.

Read and checked:

- Phase 1 Section 3, evidence matrix, scientific validation report, and Methods handoff.
- Phase 2 Section 4, 15-record method matrix, scientific validation report, and Results handoff.
- Phase 3 Section 5, 22-record numerical matrix, figure/table crosswalk, scientific validation report, and corrected supplement references.
- Phase 4 Section 6, 18-record claim matrix, scientific validation report, Discussion handoff, and Section 7 handoff.
- `limitations_matrix.csv` and all Stage 29 limitation IDs LIM29-001 through LIM29-018.
- `final_claim_registry.csv`, `master_evidence_matrix.csv`, `validity_axis_matrix.csv`, and `claim_figure_table_graph.csv`.
- `MANUSCRIPT_SOURCE_MAP.csv`.
- `FINAL_REPRODUCIBILITY_AUDIT.md`.
- `submission/jisa/manuscript.tex` and `submission/jisa/supplement/supplement.tex`.

No material scientific contradiction was found. The limitation registry was treated as authoritative, with its scope checked against the underlying evidence and the Sections 3–6 drafts.

## Complete limitation coverage

All 18 IDs are explicitly mapped in `section7_limitation_evidence_matrix.csv`:

- LIM29-001: benchmark-family and live-network external scope.
- LIM29-002: processed/rebalanced reference population.
- LIM29-003: chronology/family-composition confounding.
- LIM29-004: direction-specific semantic bridges and source/target contracts.
- LIM29-005: cancelled `GROUNDED_S4` cells.
- LIM29-006: LOAO eligibility exclusions.
- LIM29-007: descriptive 36-positive Infiltration fold.
- LIM29-008: conditional historical bootstrap uncertainty.
- LIM29-009: finite seeds and fixed hyperparameter recipes.
- LIM29-010: partially proven historical environments.
- LIM29-011: Stage26 hardware/backend/batch/component boundary.
- LIM29-012: fixed-rate prior-probability-shift assumption.
- LIM29-013: hypothetical workload, capacity, and cost scenarios.
- LIM29-014: incomplete repository-wide end-to-end reproduction.
- LIM29-015: unavailable or restricted external artifacts.
- LIM29-016: source-restricted Stage18 graph evidence and unseen topology.
- LIM29-017: descriptive single Stage21 CNN/ViT comparison.
- LIM29-018: reuse of the historically opened Stage22 target in Stage28.

Each record includes affected stages, claims, Section 7 location, source evidence, mitigation, remaining uncertainty, prohibited interpretation, and routing to Sections 3–6 or the supplement.

## Threats-to-validity classification

The prose uses five editorial categories without introducing a new framework:

- **Internal validity:** temporal/family confounding, K79 identity scope, cancelled cells, target reuse, frozen thresholds, and source/target governance.
- **Construct validity:** processed benchmark construction, semantic bridges, representation differences, ranking versus operating metrics, prior-shift projections, and prepared-input profiling boundaries.
- **External validity:** benchmark-family scope, live-network absence, direction-specific transfer, ineligible families, low-support Infiltration, restricted graph topology, and hardware portability.
- **Statistical conclusion validity:** conditional bootstrap intervals, finite seed scope, fixed recipes, heterogeneous support, and separation of seed variation from bootstrap uncertainty.
- **Reproducibility/evidence availability:** unavailable source data, closed targets, hash-only arrays/checkpoints, unproven environments, partial static status, and the distinction between verification and rerun.

Classifications describe existing evidence limits; they are not additional empirical findings.

## Consistency checks

- Section 3 population distinctions are preserved: processed reference, source-faithful temporal target, direction-specific transfer targets, known-category support 3967, LOAO support 36, eligible/ineligible families, and provenance states.
- Section 4 methods boundaries are preserved: training-only preprocessing/rebalancing, validation-only thresholds, K79 exact identity control, bridge separation, fixed prior-shift equations, prepared-input profiling, LOAO eligibility, and target closure.
- Section 5 results are interpreted without changing values or status classifications. The corrected Table S7/S8/S9 cross-references remain intact.
- Section 6 conclusions are narrowed rather than contradicted: no universal generalization, zero-day, causal, SOC, architecture, or full-reproduction claim is introduced.
- `GROUNDED_S4` remains cancelled, not measured.
- K79 is not described as session, endpoint, source-IP, five-tuple, or S4 independence.
- Stage28 is not described as a new blind holdout.

## Main-text and supplement routing

Section 7 carries the high-severity boundaries needed to interpret the main Results and Discussion: benchmark scope, temporal confounding, target reuse, LOAO eligibility/support, prior-shift assumptions, workload scenarios, deployment boundary, and reproducibility status. Detailed source receipts, bridge tables, operational grids, Stage26 profiles, LOAO metrics, stability records, and provenance classifications remain routed to S1–S7 and Tables S1–S10. Stage18 graph and Stage21 CNN/ViT details remain supplement-only.

## Reproducibility and holdout boundaries

The repository has 28 protocol files, safe verify-only wrappers, archived notebooks, source registries, 112/112 equivalence rows, and 127/127 static tests at the audited checkpoint. These facts support provenance and claim-level verification. Only Stage25 is classified `FULL_SCALAR`; Stage26 is `METHOD_ARCHIVAL_TIMING`; the remaining historical stages are partial/static. Raw datasets, some processed corpora, models, probability/explanation arrays, dependencies, historical environments, and closed targets remain unavailable or restricted. No holdout was reopened.

## Unresolved issues

1. The Phase 2 15-record method matrix remains grouped rather than one-record-per-operation. Phase 4 documented the gap; Phase 5 retains it as a traceability limitation rather than claiming exhaustive operation-level coverage.
2. Historical Stage23 K79 wording remains broader than the authoritative Stage22R boundary; the drafts consistently use the narrower wording.
3. The Stage29 six-figure paired-panel assembly remains unperformed and unauthorized.
4. No new editorial cross-reference issue was discovered after the verified S7–S10 correction.

These are documentation or evidence-boundary issues, not newly discovered scientific contradictions.

## Protection and readiness

Created only the isolated Phase 5 package. No frozen code, notebooks, configurations, result files, registries, canonical manuscript, LaTeX, figures, tables, supplement source, or author declarations were modified. No training, inference, resampling, target opening, threshold optimization, metric recomputation, or scientific computation was performed.

Section 7 is complete as an isolated draft with all 18 limitations mapped. Section 8 remains an outline only. Readiness: Section 8 may be drafted only after separate authorization and author review of the documented reproducibility and traceability boundaries.
