# Build and Validation Report

**Date:** 2026-11-02
**Target:** Journal of Information Security and Applications
**Status:** Production source assembled; PDF and complete supplement blocked.

## Source conversion

- Authority: `manuscript/manuscript_journal_revision.md`
- Bibliography authority: `manuscript/references_journal_revision.bib`
- Output: `manuscript.tex`
- Class/configuration: `elsarticle`, `preprint,12pt`; standard packages only.
- Editable source generated without scientific recalculation.
- Author, affiliation, ORCID, email, funding, overlap, and public repository fields remain `AUTHOR_CONFIRMATION_REQUIRED`.

## Static checks

- Citation tokens extracted from authority: 32 unique tokens; bibliography-key check: PASS.
- Main figures: 6 registered outputs assembled from 9 registered panel/source assets.
- Main tables: 6 table blocks converted from the approved manuscript tables.
- Abstract: under the verified 250-word limit.
- Keywords: 5; within the verified 1–7 range.
- Canonical scientific files: unchanged.
- No experiments, target opening, model loading, inference, or scientific computation performed.

## Figure assembly

- Figure 1: lossless vertical assembly of registered PR-AUC and ROC-AUC PNG panels.
- Figure 2: source PNG copied unchanged.
- Figure 3: registered SVG panels rasterized for package compatibility and vertically assembled; source SVGs retained only during assembly, not in final package.
- Figure 4: registered SVG converted to PNG.
- Figure 5: source PNG copied unchanged.
- Figure 6: registered ROC-AUC and balanced-recall PNG panels vertically assembled.

Visual page-level inspection remains blocked without a PDF renderer. Asset dimensions and file presence were checked; no plot was regenerated.

## Tables

All six approved tables are present in the LaTeX source. Values originate from the approved revision manuscript. Table styling requires rendered-PDF inspection for width and readability.

## Supplement

S1–S7 directory created but not populated. The approved plan references many frozen artifacts and unavailable/restricted dependencies. No completeness claim is made. Assembly remains pending source-by-source verification and redistribution-rights review.

## Compilation

No supported LaTeX engine was detected in PATH: `pdflatex`, `xelatex`, `lualatex`, `latexmk`, and `tectonic`. PDF compilation, citation resolution by LaTeX, overfull-box inspection, figure-placement inspection, and visual page review are therefore pending.

## Unresolved requirements

1. Install or provide an approved Elsevier-compatible LaTeX engine and `elsarticle` class.
2. Compile and inspect every PDF page.
3. Resolve all author and declaration placeholders.
4. Assemble and verify S1–S7; do not include restricted data or unauthorized artifacts.
5. Confirm live JISA portal rules for article type, length, artwork, uploads, APC, waivers, and reference style.
6. Confirm public code/data links and overlap statement.

**Conclusion:** Source package is not finalized. No submission performed.
