# Introduction and Related Work Handoff Outline

This handoff is an outline only. Introduction and Related Work were not drafted in Phase 6.

## 1. Research problem

- IDS studies often report strong benchmark discrimination without aligning claims to population, chronology, operating threshold, attack-family novelty, deployment conditions, or artifact availability.
- The central problem is not whether benchmark metrics are useful, but whether their interpretation survives changed evaluation contracts.

## 2. Research questions

1. How does conventional processed-benchmark performance relate to temporal forward evaluation?
2. Do ranking and frozen operating-point behavior transfer together under chronology?
3. How sensitive are results and explanations to feature subsets, split geometry, and learner realization?
4. Is cross-dataset transfer symmetric under explicit semantic bridges?
5. How do prevalence, workload, cost, and computational constraints alter operational interpretation?
6. What survives eligible leave-one-attack-out evaluation, registered seed variation, and reproducibility auditing?

## 3. Scientific gap

- Fragmented validity checks are often reported separately; the manuscript evaluates linked validity axes within one evidence-governed empirical chain.
- The gap concerns interpretation and evidence boundaries, not the absence of another classifier architecture.
- Avoid framing SHAP, temporal splitting, LOAO, or prevalence analysis as inventions of this study.

## 4. Verified contribution boundaries

- Multi-axis empirical audit across benchmark/reference, split/duplicate, temporal, shortcut sensitivity, cross-dataset, prevalence/operational, computational, unseen-family, and realization-stability dimensions.
- Explicit distinction between ranking, threshold transfer, calibration, workload, and deployment profiling.
- Claim-level provenance, cancellation governance, eligibility gates, and reproducibility-status classification.
- No universal model, zero-day detector, deployment system, causal shortcut explanation, or composite robustness score.

## 5. Evidence anchors for later drafting

- Conventional reference: `CLM29-001`–`CLM29-003`; `E29-004`–`E29-011`.
- Explanation and shortcut validity: `CLM29-004`, `CLM29-010`; `E29-015`, `E29-022`, `E29-023`.
- Temporal validity: `CLM29-005`, `CLM29-008`, `CLM29-009`, `CLM29-016`; `E29-016`, `E29-020`–`E29-023`, `E29-037`–`E29-040`.
- Transfer and cancellation: `CLM29-011`, `CLM29-012`; `E29-024`–`E29-027`.
- Operational and computational validity: `CLM29-013`, `CLM29-014`; `E29-028`–`E29-033`.
- Unseen-family validity: `CLM29-015`; `E29-034`–`E29-036`, `E29-039`.
- Limitations and provenance: `LIM29-001`–`LIM29-018`; `FINAL_REPRODUCIBILITY_AUDIT.md`.

## 6. Narrative constraints

- Define benchmark evidence as conditional, not worthless.
- Preserve K79 exact-identity ceiling.
- Preserve `Infilteration` known-category support 3967 versus LOAO `Infiltration` support 36.
- State DOS and AUTH_BRUTE_FORCE LOAO ineligibility.
- State Stage28 historical-target reuse.
- Avoid universal portability, zero-day, SOC, latency, architecture, and complete-reproduction claims.
- Add literature only after separate source verification; no citations are authorized by this handoff.

## 7. Suggested manuscript logic

- Introduce the interpretation problem.
- Position existing IDS validation practices as useful but incomplete when isolated.
- State the research questions.
- Present the audit as an evidence-governed integration of established evaluation dimensions.
- Preview the bounded contribution and claim discipline.
- Defer all numerical findings to Sections 5–8.
