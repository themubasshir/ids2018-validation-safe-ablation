# PDF visual QA

## Scope

Rendered and inspected every generated page at 150% scale using PyMuPDF.

- Main: `build/main/manuscript.pdf`, pages 1--36; renders in `build/main/rendered/page-01.png` through `page-36.png`.
- Supplement: `build/supplement/supplement.pdf`, pages 1--7; renders in `build/supplement/rendered/page-01.png` through `page-07.png`.

## Final findings

- Main: 36 pages; supplement: 7 pages.
- Main six figure assets appear on pages 17, 19, 20, 21, 23, and 24; Figure 6 is present as the LOAO exhibit.
- Main six table captions appear; table pages/float placement remain readable.
- Supplement S1--S7 and Tables S1--S10 appear across all seven pages.
- No unexpected blank page or missing figure asset observed.
- Main overfull boxes: 0. Supplement overfull boxes: 0.
- Main underfull boxes: 8; supplement underfull boxes: 7, primarily bibliography URL composition.
- Visual glyph inspection: PASS; no observed visible glyph defect.
- Text extraction: original `fitz` PyMuPDF binding reported 20 replacement characters; `pymupdf` import reported 0. Same PyMuPDF/MuPDF backend; not independent. Independent extractor/font-mapping verification remains incomplete.

## Decision

Compilation and visual inspection pass. Text-extraction mapping remains conditional. Overall submission readiness remains blocked by unresolved author/publisher requirements and independent extraction verification. See `phase9d_pdf_qa_addendum.md`.
