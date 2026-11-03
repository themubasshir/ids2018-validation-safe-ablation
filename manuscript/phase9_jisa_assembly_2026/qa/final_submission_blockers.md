# Final submission blockers

- AUTHOR_APPROVAL_REQUIRED: author identity, affiliation, corresponding information, ORCID, funding, competing interests, ethics, acknowledgments, data/code availability, CRediT, AI disclosures.
- JISA-specific author-guide and portal requirements remain unverified.
- Main and supplement compile; overfull boxes 0/0; underfull diagnostics remain (main 8, supplement 7), reviewed as harmless bibliography URL composition.
- Phase 9C.2 numerical provenance closed: 207 numeric-bearing rows retained; 67 valid scientific numerical rows all verified (`VERIFIED_SOURCE_FIELD` 14, `VERIFIED_ORIGINAL_REPORT` 50, `VERIFIED_PROTOCOL` 3). 61 non-result numeric rows retained as `NOT_APPLICABLE_TO_STAGE29`.
- Main PDF extraction discrepancy remains conditional: original `fitz` PyMuPDF extraction reported 20 replacement characters; `pymupdf` import reported 0. Both use the same PyMuPDF/MuPDF backend, so independent extractor/font-mapping verification is not completed.
- Visual inspection found no observed visible glyph defect. See `phase9d_pdf_qa_addendum.md` and `phase9c3_glyph_resolution.csv`.
- Numerical provenance is a scientific-pass component only; it does not establish final submission readiness.
- Figure/table source-level registry comparison is substantially checked by inventory, but underlying panel provenance still needs final manual confirmation.
- No submission package generated or submitted.
