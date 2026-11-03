# Final manuscript integration handoff

## Status

Phase 8 artifacts are isolated and validated. Integration is **not executed**. Do not modify the canonical JISA LaTeX, canonical manuscript, canonical bibliography, sections, figures, tables, supplementary source, author metadata, or declarations without separate authorization.

## Integration order

1. Preserve the canonical worktree and create an integration branch or separately authorized working copy.
2. Replace the canonical abstract body with `abstract.md`; retain one unstructured `abstract` environment. Do not insert citations unless final JISA instructions require them.
3. Replace canonical keyword content with the six terms in `keywords.md`, using the final journal-required separator and capitalization.
4. Add the five lines in `highlights.txt` to the separate Elsevier/JISA highlights submission field or file format required by the verified guide. Do not place Highlights inside the article body unless instructed.
5. Integrate Sections 1–8 in order. Use Phase 7B Sections 1–2, then the approved Sections 3–8. Preserve section numbering and subsection labels; resolve any existing duplicate headings only after comparing the canonical assembly.
6. Preserve the approved six main figures and six main tables from the Stage 29 registries. Do not regenerate or visually alter assets. Route all registry-marked supplement assets to existing supplementary material.
7. Retain existing supplementary source, labels, captions, cross-references, and figure/table numbering after explicit duplicate-label audit.
8. Reconcile bibliography and citations. Run citation-key, duplicate-key, BibTeX, undefined-reference, and unused-entry checks before PDF generation.
9. Fill author details, declarations, data availability, code/availability and reproducibility statements, funding, conflicts, acknowledgments, and the journal-required AI-assistance disclosure only from author-approved information. Do not infer or invent metadata.
10. Run document-level checks, including final PDF text extraction, page/section/figure/table cross-reference validation, bibliography and citation checks, and visual inspection of the generated PDF. Obtain separate authorization for PDF generation and submission packaging.

## Section and content hazards

- Canonical LaTeX currently contains a preliminary abstract and keywords. Replace, do not append.
- Canonical Introduction/Related Work are older drafts and must not be duplicated with Phase 7B Sections 1–2.
- Phase 7B uses Markdown citation keys such as `[@ring2019survey]`; conversion to canonical LaTeX citation commands must be explicit and complete.
- Phase 7B section headings include `# 1. Introduction` and `# 2. Related Work`; canonical LaTeX uses numbered `\section` and `\subsection` commands. Strip Markdown heading syntax during authorized conversion. Audit redundant methodological prose, inconsistent subsection numbering, converted citation labels, and conflicting figure/table/supplement cross-references before acceptance.
- Preserve the accepted positioning: “a bounded, source-faithful empirical validity audit of CSE-CIC-IDS2018 and a restricted CICIDS2017 bridge.”
- Do not reinstate unsupported claims `CLM29-017` or `CLM29-018`, or original formulations `CLM29-019` and `CLM29-020`.
- Keep the processed reference distinct from source-faithful temporal and transfer populations.
- Keep K79 exact-identity-only scope, historical target reuse, chronology/family confounding, bridge62/bridge70 distinction, and cancelled `GROUNDED_S4` cells visible in the body or limitations.
- Preserve LOAO eligibility: DOS and AUTH_BRUTE_FORCE are ineligible; Infiltration support 36 is descriptive; known-category `Infilteration` support 3,967 is separate.
- Label Stage25 values as analytic scenarios. Label Stage26 values as component-level measurements on recorded hardware/software.
- Preserve finite five-seed descriptive scope and incomplete historical reproduction.
- Do not convert internal evidence IDs (`E29-*`, `CLM29-*`, `LIM29-*`, `NUM29-*`) into reader-facing citations. Retain them in traceability artifacts or editorial notes where appropriate.

## Bibliography reconciliation

Canonical and Phase 7B key sets require explicit reconciliation:

- Canonical-only key: `dwork2015holdout`.
- Phase 7B-specific keys: `biswas2026drift`, `buriboyev2026protocol`.
- The remaining Phase 7B bibliography records overlap the canonical set by key according to the Phase 7B audit.

Do not drop `dwork2015holdout`; it remains cited in Related Work on adaptive analysis and repeated holdout feedback. Add the two Phase 7B-specific records only if their citations remain in the integrated Sections 1–2 and their bibliographic status is accepted by the author. Preserve Biswas as a non-peer-reviewed preprint. Preserve Buriboyev's unverified peer-review status. Retain Berhili's publication-year ambiguity and access qualification until the author resolves it; the authoritative DOI/publisher response reports volume-year 2027 while the acceptance/package context is 2026.

Canonical bibliography integration must also check whether any older keys remain cited by retained Sections 3–8. Do not replace entries solely because a Phase 7B duplicate has a similar title. Resolve duplicate source records by source identity, not string similarity.

## Main figures

The Stage 29 final figure registry marks six central main exhibits for later assembly:

1. `fig22r_1_validation_to_final_pr_auc` / paired temporal PR-AUC exhibit.
2. `fig22r_2_validation_to_final_roc_auc` / paired temporal ROC-AUC exhibit.
3. `figure_23_a_subset_split_interaction`.
4. `fig24_1_normalized_pr_auc_directionality`.
5. `fig25_a_ppv_cliff`.
6. `F26_CPU1_GPU_P95_SPEEDUP`.

The registry also marks the six main table candidates: `T29-01_REFERENCE_BENCHMARK`, `T29-02_VALIDITY_AXIS_MATRIX`, `T29-03_TEMPORAL_FIVE_SEED`, `T29-04_BIDIRECTIONAL_TRANSFER`, `T29-05_OPERATIONAL_TRANSLATION`, and `T29-06_LOAO_STABILITY`. Verify whether paired figure entries are assembled into one numbered figure or remain separate according to the approved figure plan. Preserve captions' population, metric, and boundary qualifiers.

## Supplement and declarations

Retain existing Supplement S1–S7 and Tables S1–S10, including detailed subset controls, bridge70 sensitivity, cancelled-cell governance, full operational translations, computational profiles, LOAO seed-level metrics, explanation diagnostics, and reproducibility records. Cross-reference rather than duplicate long tables in the main text.

Author details, affiliations, corresponding-author data, funding, conflicts of interest, acknowledgments, ethics statements, data availability, code availability, and declarations require author confirmation. Existing `AUTHOR_CONFIRMATION_REQUIRED` placeholders in `submission/jisa/manuscript.tex` remain intentionally untouched.

## Pre-submission integration checks

- All eight sections appear exactly once, in order.
- Abstract appears once; preliminary abstract removed.
- Keywords appear once; six terms match approved source.
- Highlights are supplied separately and each remains ≤85 characters.
- All section, figure, table, and supplement references resolve.
- No duplicate labels, captions, citation keys, bibliography entries, or heading numbers.
- All citations resolve, including `dwork2015holdout`, `biswas2026drift`, and `buriboyev2026protocol` where retained.
- No unsupported novelty, causal, universal, zero-day, deployment-readiness, or complete-reproduction language.
- `git diff --check` passes; only authorized integration files change.
- Author metadata and declarations are complete and approved.
- PDF generation occurs only after separate authorization.
