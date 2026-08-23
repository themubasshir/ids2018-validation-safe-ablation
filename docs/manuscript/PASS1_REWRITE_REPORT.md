# Final Manuscript Reconstruction — Pass 1 Report

Status: **Pass 1 complete; manuscript not final.**

Branch: `manuscript-reproducibility-cleanup`  
Accepted starting point: `df3589d`  
Empirical authority: Stage28 final empirical wall; Stage29 synthesis package  
Primary manuscript: `manuscript/manuscript_reconstructed.md`

## 1. Commits

Pass 1 was divided into nine incremental commits and pushed individually:

1. `57efce7 docs: initialize evidence-governed manuscript reconstruction`
2. `25b81f5 docs: rewrite abstract introduction and related work`
3. `0ea3db8 docs: rewrite datasets provenance and methods`
4. `46e36b4 docs: rewrite integrated results`
5. `a5a0392 docs: rewrite discussion limitations and conclusion`
6. `a12fd4d docs: map manuscript claims numbers and sources`
7. `0b24fe5 docs: plan manuscript exhibits and reference gaps`
8. `c0ea664 test: enforce pass1 manuscript provenance`
9. `docs: close manuscript reconstruction pass1` (the closeout commit containing this report)

No force push or merge to `main` was performed.

## 2. Manuscript word count

The reconstructed Markdown manuscript contains **9,277 words** by the closeout Unicode word-token count (`letters`, `numbers`, underscores, apostrophes, and hyphens; Markdown punctuation excluded). The count includes the six main Markdown tables and supplementary-material plan.

## 3. Section and subsection structure

The manuscript contains **11 level-2 sections** and **39 level-3 subsections**:

- Abstract;
- 1. Introduction;
- 2. Related Work, with 4 conceptual subsections;
- 3. Datasets and Provenance, with 4 subsections;
- 4. Validation Framework and Methods, with 10 validation-axis subsections;
- 5. Results, with 9 question-organized subsections;
- 6. Discussion, with 6 synthesis subsections;
- 7. Limitations, with 6 grouped subsections;
- 8. Conclusion;
- References;
- Supplementary Material Plan.

Historical stage order is used only for provenance, not as the manuscript's scientific organization.

## 4. Number of scientific claims

The main narrative uses **14 unique retained Stage29 claim IDs**. The claim audit records **56 substantive claim occurrences** across the abstract, introduction, datasets, methods, results, discussion, and conclusion.

The two supplement-only claims (`CLM29-006`, `CLM29-007`) are excluded from the main scientific narrative. Removed and rewrite-only registry entries are not treated as retained claims.

## 5. Claim-resolution rate

**56/56 audited claim occurrences resolve (100%).** Every row maps to a valid Stage29 claim ID, supporting evidence IDs, explicit qualifier, limitation link, and `RESOLVED` status. All 14 eligible main-narrative claim IDs are represented; no orphan claim remains in the audit.

## 6. Scientific-number count

The number audit contains **110 scientific-number entries**, covering **87 unique frozen `NUM29` identifiers**. A further **10 entries** are explicitly classified `NON_RESULT_METADATA` for dataset/stage names, exhibit numbering, bridge names, dates, frozen design counts, and scenario labels.

## 7. Number-resolution rate

**110/110 scientific-number audit entries resolve (100%).** Each maps to the frozen Stage29 number registry, a source artifact, an evidence ID, and a manuscript location. No missing scientific value was calculated or silently filled.

## 8. Figures selected

The Stage29-approved nine main source assets are routed into **six conceptual main figures**:

1. temporal PR-AUC and ROC-AUC transfer (two existing assets; later panel assembly only);
2. shortcut-subset/split interaction;
3. bidirectional cross-dataset PR-AUC and ROC-AUC (two existing assets; later panel assembly only);
4. prevalence/PPV cliff;
5. hardware-specific CPU/GPU p95 comparison;
6. eligible-family ROC-AUC and balanced recall (two existing assets; later panel assembly only).

The plan records source stage, intended message, draft caption, evidence IDs, and mandatory interpretation boundaries. No scientific figure was regenerated, redrawn, or physically combined.

## 9. Tables selected

The main manuscript contains **six Stage29-approved tables**:

1. conventional processed-reference results;
2. five-seed temporal stability;
3. bidirectional bridge62 transfer;
4. selected 0.1% operational translations;
5. eligible-family conclusion stability;
6. integrated native-metric validity matrix.

The validity matrix does not normalize unlike metrics or create a composite robustness score.

## 10. Supplement recommendations

Seven supplement groups are retained in the exhibit plan:

1. reference membership, uncertainty, calibration, category support, and LIME reliability;
2. Stage23 subset, placebo, stump, proxy, family-support, and secondary interaction material;
3. Stage24 serialization contrasts, threshold transfer, population governance, and cancellation receipts;
4. Stage25 full prevalence, workload, capacity, break-even, cost, and sanity grids;
5. Stage26 warm/cold, batch, component, memory, capacity, Pareto, backend, and representation profiles;
6. Stage27/28 seed-level family metrics, eligibility detail, temporal realizations, and controls;
7. supplement-only Stage18 representation and Stage21 architecture chronology, with their descriptive restrictions.

Detailed forensic receipts, hashes, environments, notebook maps, and equivalence records remain repository/supplement material.

## 11. Reference-gap count

There are **10 active reference-gap placeholders**, all inventoried in `MANUSCRIPT_REFERENCE_AUDIT.md`. Existing verified references reused: **0**. Potentially obsolete references identified: **0**. Duplicate references identified: **0**. No bibliography entry or citation was invented, and no external browsing was performed.

## 12. Claims removed from old framing

Two Stage29 `REMOVE` formulations are absent:

- `CLM29-017`: “The model generalizes.”
- `CLM29-018`: “The model detects zero-day attacks.”

The manuscript also excludes claims of universal IDS failure, arbitrary zero-day detection, universal architecture superiority, and universal operational uselessness.

## 13. Claims materially rewritten

Two Stage29 rewrite targets were replaced with bounded interpretations:

- `CLM29-019`: the claim that temporal splitting causes catastrophic performance collapse was replaced by the observed direction-specific ranking contrast, poor frozen-threshold transfer, finite-seed qualification, and mixed causal controls;
- `CLM29-020`: the claim that shortcut features cause cross-dataset transfer failure was replaced by split-, learner-, subset-, and placebo-conditional sensitivity without causal attribution.

The overall framing changed from a model/ablation chronology to a validation framework that distinguishes benchmark performance from validated capability.

## 14. Limitations represented

**18/18 Stage29 limitations are present.** They are grouped under dataset/provenance, protocol/scope, statistical, operational assumptions, computational/hardware, and reproducibility. Each paragraph states what the limitation prevents the manuscript from claiming.

## 15. Unresolved evidence tensions

Pass 1 retains rather than edits away the following tensions:

- strong processed-reference discrimination versus conditional forward validity;
- stronger chronological ranking versus poor transferred threshold behavior;
- chronology versus attack-family composition as an unresolved mechanism;
- shortcut sensitivity versus placebo interactions and lack of causal identification;
- stable LIME rankings versus frequent local-fidelity failures;
- strong forward cross-dataset ranking versus near-baseline reciprocal transfer;
- high projected PPV versus excessive workload, and low workload versus negligible detection yield;
- strong withheld-family transfer for some families versus learner dependence, ineligibility, or low support for others;
- architecture- and hardware-specific deployment advantages rather than one universally faster backend.

## 16. Static manuscript-audit results

The new Pass 1 provenance suite passes **10/10 tests**. Combined with the Stage29 synthesis checks, the focused run passes **21/21 tests**. The full repository verification run passes **148/148 tests**.

The checks cover required files, manuscript structure, claim/evidence/limitation resolution, scientific-number resolution, removal and supplement-only boundaries, source-map coverage, all 18 limitation concepts, main exhibit sources, reference-gap accounting, citation syntax, and the no-new-science manuscript boundary. All source paths referenced by the main exhibit plan resolve.

## 17. Stage28 empirical-wall confirmation

**Confirmed. Stage28 remains the final empirical wall.** Stage29 is used only as the authoritative synthesis and governance layer. The reconstructed manuscript adds no empirical stage and makes no claim beyond the frozen Stage29 ceiling.

## 18. No-new-computation confirmation

**Confirmed. No new scientific computation occurred.** Pass 1 performed manuscript writing, registry/source inspection, identifier/path checks, and repository static/equivalence validation only. It performed no fit, model deserialization, inference, target opening, threshold optimization, bootstrap generation, confidence-interval generation, attribution computation, feature computation, profiling, prevalence analysis, LOAO analysis, seed analysis, new metric, composite score, experiment, or scientific figure generation.

Pass 2—external reference verification, bibliography construction, journal-specific formatting, and any later authorized panel assembly—has not begun.
