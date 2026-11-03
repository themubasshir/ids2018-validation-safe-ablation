# LaTeX build report

Status: MAIN and SUPPLEMENT COMPILED.

## Toolchain

- OS: Windows.
- Distribution: MiKTeX 25.12, user-local.
- Engine: `pdflatex` MiKTeX-pdfTeX 4.23.
- Bibliography: `bibtex` 0.99e.
- `latexmk`: present but unusable because Perl is absent; manual sequence used.

## Commands

Executed from isolated source/build context with outputs under `build/main/` and `build/supplement/`:

```text
pdflatex -interaction=nonstopmode -halt-on-error -file-line-error
bibtex manuscript
pdflatex -interaction=nonstopmode -halt-on-error -file-line-error
pdflatex -interaction=nonstopmode -halt-on-error -file-line-error
```

Supplement: two `pdflatex` passes.

## Outputs

- `build/main/manuscript.pdf`: 36 pages.
- `build/supplement/supplement.pdf`: 7 pages.
- Bibliography generated successfully; BibTeX emitted three empty-pages-field warnings (`lundberg2017shap`, `yeh2019infidelity`, `mirsky2018kitsune`).

## Phase 9C/9D warnings and findings

- Main PDF: 0 overfull boxes; 8 underfull boxes.
- Supplement PDF: 0 overfull boxes; 7 underfull boxes.
- No undefined citations/references or fatal LaTeX errors detected.
- Original PyMuPDF binding imported as `fitz`, using `page.get_text()` default extraction, reported 20 replacement characters in the main PDF.
- `pymupdf` import using the same default extraction reported 0. Same PyMuPDF/MuPDF backend; not independent. Independent extractor/font-mapping verification remains outstanding.
- Visual inspection found no observed visible glyph defect. See `phase9d_pdf_qa_addendum.md` and `phase9c3_glyph_resolution.csv`.
- BibTeX retains three empty-pages-field warnings (`lundberg2017shap`, `yeh2019infidelity`, `mirsky2018kitsune`).
- `latexmk` was not used because Perl is unavailable; manual compilation succeeded.
