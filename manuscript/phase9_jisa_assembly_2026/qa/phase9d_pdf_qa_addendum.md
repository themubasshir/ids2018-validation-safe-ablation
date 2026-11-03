# Phase 9D.1 PDF QA reconciliation addendum

## Extraction methods

- Original implementation: PyMuPDF Python binding imported as `fitz`; `page.get_text()` default text extraction. Reported 20 U+FFFD replacement characters in the 36-page main PDF.
- Second implementation: PyMuPDF Python binding imported as `pymupdf`; `page.get_text()` and `page.get_text("text")` default text extraction. Reported 0 U+FFFD replacement characters in the same PDF.
- Backend independence: **No**. `fitz` and `pymupdf` are two import APIs for the same PyMuPDF/MuPDF backend. The second result is not an independent extractor.
- Installed independent alternatives: no `pdftotext`, `mutool`, or `qpdf` executable was available. No software installed.

## Reconciled finding

The reviewed PDF has no observed visible glyph defects. Two extraction methods produced different replacement-character counts (20 and 0). The discrepancy appears method-dependent, but independent text-extractor or font-mapping verification remains outstanding.

- PDF compilation: **PASS**.
- Visual glyph inspection: **PASS** for inspected pages; no visible defect observed.
- Independent extraction verification: **NOT_COMPLETED**.
- Text extraction mapping: **CONDITIONAL**.
- Classification: `EXTRACTOR_SPECIFIC_ARTIFACT` for the observed extraction discrepancy; not a visible document defect.
- Overall submission readiness: **BLOCKED** by author/publisher requirements and unresolved mandatory verification items.

This addendum corrects the prior wording that described the second PyMuPDF API result as independent. It does not alter manuscript science, numerical provenance, or PDF bytes.
