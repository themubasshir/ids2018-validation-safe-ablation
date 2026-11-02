# Build and Validation Report

**Date:** 2026-11-02\n**Target:** Journal of Information Security and Applications\n**Status:** Compiled production package; visual inspection and author metadata remain blocked.

## Authority and preservation

- Manuscript authority: `manuscript/manuscript_journal_revision.md`.
- Bibliography authority: `manuscript/references_journal_revision.bib`.
- Supplement authority: `docs/manuscript/pass2b/FINAL_SUPPLEMENT_PLAN.md` plus frozen Stage 23–29 artifacts.
- Canonical research files unchanged.
- No experiments, model loading, inference, target opening, new metrics, thresholds, figures, or results performed.

## LaTeX repair

- Removed eight manually embedded section numbers; hierarchy preserved.
- Restored 13 lost bold labels, eight checklist headings, and five provenance terms: `Raw-exact`, `published`, `corrected`, `source-faithful`, `reconstructed`.
- Restored exact citation-key underscores.
- Corrected escaped identifiers and author placeholders.
- Removed duplicate manual References heading and removed the in-body supplement plan.
- Escaped literal percentage signs and repaired one malformed bibliography ampersand.
- Static checks: no `\\textbf{\\1}`, no numbered `\\section{N. ...}`, no duplicate manual References heading, no escaped underscores inside citation keys; eight checklist items present.

## Main compilation

MiKTeX 25.12 installed per-user from official `MiKTeX.MiKTeX` winget package. Commands used: three `pdflatex` passes with `--enable-installer`, one `bibtex` pass, then two further `pdflatex` passes. All final passes exited 0.

- Output: `submission/jisa/manuscript.pdf`.
- 31 pages; 1,916,579 bytes after table-layout repair.
- BibTeX: exit 0; three existing empty-page-field warnings only (`lundberg2017shap`, `yeh2019infidelity`, `mirsky2018kitsune`).
- Final logs: no fatal errors, unresolved citations, or missing-reference errors.
- Six figures and six tables retained.

## Main visual QA

Not complete. ImageMagick is installed, but PDF rasterization failed because its Ghostscript delegate (`gswin64c.exe`) is unavailable. Source/PDF metadata and compiler logs were checked; page-by-page figure, table, glyph, and page-break inspection remains blocked. Main source still requires human visual review, despite successful compilation.

## Supplement S1–S7 matrix

| Section | Status | Evidence / boundary |
|---|---|---|
| S1 | Populated | Reference population, metrics, uncertainty, explanation reliability; unavailable arrays remain dependencies. |
| S2 | Populated | Stage 23 subset artifact and shortcut/representation qualifications. |
| S3 | Populated | Directional bridge contract; Table S1 source record; cancelled `GROUNDED_S4` cells retained. |
| S4 | Populated | Frozen prior-shift operational translation and scenario qualifications. |
| S5 | Populated | Stage 26 deployment boundary, compatible paths, statuses, and exclusions. |
| S6 | Populated | LOAO eligibility, low-support Infiltration, ineligible DOS/AUTH_BRUTE_FORCE, two frozen figures, stability registry. |
| S7 | Populated with dependencies | Hash manifest, provenance/equivalence/reproduction boundary, redistribution restrictions. |

The supplement documents unavailable, restricted, cancelled, descriptive, and unsupported evidence as dependencies; it does not fabricate missing exhibits or redistribute restricted artifacts. `source-manifest.csv` records SHA-256 values for copied sources.

## Supplement compilation and QA

- Output: `submission/jisa/supplement/supplement.pdf`.
- 5 pages; final two `pdflatex` passes exited 0.
- No fatal errors, missing references, or unresolved citations.
- Final overfull-box warnings cleared after `microtype` and `\emergencystretch` adjustments.
- Page-by-page visual inspection remains blocked by the missing Ghostscript PDF renderer.

## Flattened Elsevier export

`submission/jisa/elsevier_export/` contains same-level source, bibliography, six figures, and processing dependencies. Figure paths were rewritten from `figures/...` to flattened filenames. Independent three-pass `pdflatex`/`bibtex` compilation exited 0 and produced a 31-page PDF. Build intermediates remain in this development export for audit and must be excluded from any final upload selection.

## Scientific integrity

- Approved values retained; no scientific recomputation.
- Seven evidence tensions, 18 limitations, LOAO qualifications, cancelled analyses, low-support families, and reproduction restrictions retained in source/supplement text.
- No new claims promoted from supplement-only evidence.

## Remaining blockers

1. Page-level visual inspection requires an approved PDF renderer/Ghostscript installation.
2. Author names, affiliations, corresponding-author email, ORCID, funding, conflicts, overlap, AI disclosure, and authorized public data/code URL remain `AUTHOR_CONFIRMATION_REQUIRED` or unresolved.
3. Venue portal/article-type/artwork/upload/APC rules require current author confirmation.
4. Supplement exhibits whose frozen source or redistribution permission is unavailable remain documented dependencies, not complete data releases.
5. No submission, release, DOI, Zenodo archive, merge, or force-push performed.

**Conclusion:** `SUBMISSION PACKAGE INCOMPLETE — SPECIFIC BLOCKERS`.
