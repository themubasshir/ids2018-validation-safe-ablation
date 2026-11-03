# Phase 10A PDF extraction verification

## Result

Independent extraction verification: **NOT_COMPLETED**.

Available methods were:

1. `fitz` import, PyMuPDF/MuPDF backend, `page.get_text()` default extraction: 20 replacement characters in the main PDF.
2. `pymupdf` import, same PyMuPDF/MuPDF backend, `page.get_text()` and `page.get_text("text")`: 0 replacement characters.

These are different Python import APIs, not independent extraction implementations. No installed `pdftotext`, `mutool`, `qpdf`, `pypdf`, `pdfplumber`, or `pdfminer.six` backend was available. No software installed.

## Visual/source comparison

Rendered pages containing all 20 reported occurrences were inspected. No visible glyph defect was observed. The affected contexts are ordinary prose, headings, table text, and bibliography text; no scientific mathematical symbol was identified as visibly corrupted. Source LaTeX is ASCII-clean in the affected passages. Figure and caption review found no visible text defect relevant to the replacement-character report.

## Consistent classification

- PDF compilation: **PASS**.
- Visual glyph inspection: **PASS**.
- Independent text extraction: **NOT_COMPLETED**.
- Text mapping: **CONDITIONAL**.
- Observed discrepancy: `EXTRACTOR_SPECIFIC_ARTIFACT`, not a demonstrated visible document defect.

## Manual verification procedure

Before submission, an author should open the local reviewed PDFs in two distinct viewers/extractors, export page text, search for U+FFFD/replacement glyphs, inspect pages 2, 4, 15, 16, 19, 22, 23, 24, 27, 32, and 33 at high zoom, and compare each affected context against `source/manuscript.tex` and `source/references.bib`. Record application name/version, extraction mode, count, affected pages, and any font-substitution warning. Do not alter PDF bytes solely to satisfy extraction output.

Reviewed PDFs:

- `build/main/manuscript.pdf` — SHA-256 `00abf3e55a3e6ca3cd08df500873de6c309a531f2f08eb8e35bdc9defaed6fe1`
- `build/supplement/supplement.pdf` — SHA-256 `43d5c68ec0235d88f7daf2faf5527f30580359f17769af70f3f66e5c63f7bf25`
