# Phase 8 abstract, highlights, and keywords validation report

## Scope and protection

Phase 8 artifacts were drafted in the isolated `manuscript/phase8_abstract_highlights_2026/` directory. No canonical manuscript, LaTeX, bibliography, Sections 1–8, figures, tables, supplementary source, code, notebooks, configurations, datasets, frozen results, or Stage 29 registries were modified. No fitting, inference, target opening, threshold search, resampling, metric recomputation, PDF generation, or Git operation was performed.

## Publisher-guidance verification

The official JISA Guide for Authors URL was attempted:

`https://www.elsevier.com/journals/journal-of-information-security-and-applications/2214-2126/guide-for-authors`

Access redirected to a ScienceDirect error response and did not expose usable JISA-specific instructions. Web search also returned no usable result. Therefore, JISA-specific abstract word-limit, keyword-count, and separate-highlights requirements remain **unverified**. The draft follows the requested working targets and Elsevier-general convention: unstructured abstract, approximately 200–250 words, six focused keywords, and five separate highlights with each highlight no longer than 85 characters.

## Counts

- Abstract: **218 words**, body only; heading excluded.
- Highlights: **5**.
- Highlight lengths, including spaces and punctuation:
  1. 79 — `Benchmark discrimination was conditional on the processed reference population.`
  2. 79 — `Chronological ranking exceeded random, but frozen thresholds transferred poorly.`
  3. 68 — `Cross-dataset ranking was directional under frozen semantic bridges.`
  4. 72 — `Projected PPV, workload, and detection yield diverged at low prevalence.`
  5. 81 — `Eligible-family results and computational feasibility were selective and bounded.`
- Keywords: **6**.

All highlights satisfy the 85-character ceiling. Keywords use established terms and avoid treating concept drift as a demonstrated mechanism.

## Numerical verification

- Processed reference balanced XGBoost F1 **0.9285** and PR-AUC **0.9776**: `NUM29-017`, `NUM29-020`; `E29-006`; Results §5.1.
- Five-seed forward mean PR-AUC: chronological-natural **0.6388**, random-natural **0.2599**: `NUM29-137`, `NUM29-141`; `E29-037`; Results §5.2. The wording states descriptive five-realization ordering, not significance or population generalization.
- Chronological-over-random ordering in all five realizations: `NUM29-143`–`NUM29-144`; `E29-038`; Results §§5.2 and 5.8.
- Bridge62 PR-AUC: IDS2018→CICIDS2017 **0.667483**, reciprocal **0.108176**: `NUM29-091`, `NUM29-094`; `E29-024`–`E29-025`; Results §5.4. Direction-specific populations are retained.
- At assumed **0.1%** attack prevalence, random-natural STANDARD projected PPV **0.965572** and **33.5 analyst-hours/day**: `NUM29-100`–`NUM29-102`; `E29-028`; Results §5.5. The abstract identifies this as a projected scenario, not an observed SOC result.

No incompatible populations or metrics were combined. Numerical claims use frozen manuscript-approved rounding.

## Claim mapping

`abstract_claim_evidence_matrix.csv` contains 12 material claim rows. Each maps to Stage 29 claim IDs, evidence IDs, actual Results subsections, population, and interpretation restriction. Coverage includes benchmark, temporal ranking, threshold transfer, directional bridge transfer, operational projections, LOAO eligibility, and component profiling. The conclusion row preserves the main evidence ceilings.

## Scientific consistency

The abstract preserves:

- processed reference versus source-faithful temporal/transfer populations;
- descriptive five-of-five stability, finite seeds, and historical forward-target reuse;
- chronology/attack-family confounding;
- bridge62 directionality and frozen semantic-contract scope;
- analytic, assumption-bound prevalence/workload projections;
- component-level hardware/software profiling;
- selective eligible-family behavior, with DOS and AUTH_BRUTE_FORCE ineligible and Infiltration support 36 descriptive;
- no universal deployment, zero-day, temporal-causation, or complete-reproduction claim.

The package does not state a K79 detail in the abstract because the 218-word limit makes the abstract clearer; the integration handoff requires that K79's exact-identity-only boundary remain in Sections 3, 5, 6, and 7. Likewise, cancelled `GROUNDED_S4` cells remain documented in the matrix and handoff, not compressed into a headline result.

## Novelty and overlap compliance

No citation or priority claim appears in the abstract or highlights. The wording presents a bounded source-faithful empirical audit, not a new evaluation framework. It does not claim invention of temporal validation, semantic bridging, shortcut analysis, LOAO, reproducibility, or multi-axis evaluation. Berhili and Biswas overlap remains acknowledged in Phase 7B materials; no competing-work omission or originality claim is introduced here.

## Unsupported claims found and corrected

- Preliminary abstract language implying a general multi-axis framework was replaced by bounded audit language.
- Deployment-oriented wording was constrained to analytic scenarios and measured compatible component paths.
- Universal generalization and zero-day implications were excluded.
- Five-seed ordering was explicitly qualified as descriptive.
- Directional transfer was reported without averaging incompatible directions.
- Abstract citations were omitted, consistent with the requested format and absence of a verified JISA citation requirement.

## Unresolved author decisions

1. Confirm JISA-specific abstract, keyword, and highlights rules when the official guide becomes accessible.
2. Confirm whether the final submission should use the six proposed keywords or journal-system metadata limits.
3. During authorized integration, reconcile the canonical bibliography key set: canonical-only `dwork2015holdout`; Phase 7B-specific `biswas2026drift` and `buriboyev2026protocol`.
4. Confirm author details, declarations, availability statement, and disclosures; placeholders remain in the canonical LaTeX and were not changed.
5. Confirm final figure/table selection against the Stage 29 registries; no assets were copied or altered in Phase 8.

## Gate

**Phase 8 editorial validation: PASS with JISA-guidance access limitation.** Abstract, Highlights, Keywords, claim mapping, and integration handoff are ready for author review. Canonical integration remains intentionally unexecuted.
