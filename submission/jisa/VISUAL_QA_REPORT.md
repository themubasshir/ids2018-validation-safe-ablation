# PDF Visual QA Report

**Date:** 2026-11-02

## Method

PyMuPDF 2.0 installed with `py -m pip install --user pymupdf`. PDFs rendered at 160 DPI to temporary storage outside the repository:
`C:\Users\Cyb3r\AppData\Local\Temp\opencode\jisa_visual_qa`.

Contact sheets plus individual page images were inspected. Ghostscript/ImageMagick was not used.

## Main manuscript

- File: `submission/jisa/manuscript.pdf`
- Pages: 31
- Rendered pages: 31/31
- Contact sheet: temporary `jisa/manuscript-contact.png`
- Visual result: no clipped text, blank unexpected pages, missing glyphs, or cut-off figures observed. Figures, captions, tables, references, and page numbering present. Dense tables and small figure labels require normal reviewer zoom; no source-level overflow warning remained after the table sizing repair.

## Supplement

- File: `submission/jisa/supplement/supplement.pdf`
- Pages: 7
- Rendered pages: 7/7
- Contact sheet: temporary `supplement/supplement-contact.png`
- Visual result: tables remain within page bounds; captions and section breaks visible; no clipped text, missing glyphs, unexpected blank pages, or broken figure/table placements observed. Dense quantitative tables require reviewer zoom but remain readable at full-resolution render.

## Flattened export

The flattened export source was independently compiled in Phase 5B. Its PDF was not retained in the production tree; source path and figure-path checks remain valid. Recompilation should be repeated after any source change before upload.

## Residual QA

- Historical BibTeX warnings remain limited to empty page fields for `lundberg2017shap`, `yeh2019infidelity`, and `mirsky2018kitsune`; metadata was not invented.
- Visual inspection confirms presentation only; it does not replace scientific-author approval or redistribution-rights review.
