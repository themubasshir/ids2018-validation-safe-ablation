# Phase 9C.2 review decision

## Decision: SCIENTIFIC_PROVENANCE_PASS (numerical provenance scope)

- 207 numeric-bearing rows remain accounted for.
- 61 rows were corrected from the prior overbroad scientific classification and retained as `NOT_APPLICABLE_TO_STAGE29`.
- 67 valid scientific numerical rows remain.
- 67/67 have final verification statuses.
- No source conflicts, value mismatches, or unresolved scientific numerical rows remain.
- No fabricated NUM29 IDs or source locators used.

### Status counts

- `VERIFIED_SOURCE_FIELD`: 14
- `VERIFIED_ORIGINAL_REPORT`: 50
- `VERIFIED_PROTOCOL`: 3
- `VERIFIED_STAGE29_ONLY`: 0
- `SOURCE_UNAVAILABLE`: 0
- `SOURCE_CONFLICT`: 0
- `VALUE_MISMATCH`: 0
- `NOT_YET_VERIFIED`: 0

### Separate blockers

- Main PDF's original PyMuPDF (`fitz`) extraction reported 20 replacement-character occurrences. A later `pymupdf` import reported 0, but both use the same PyMuPDF/MuPDF backend and are not independent extractors. Independent text-extractor/font-mapping verification remains outstanding. Numerical provenance does not resolve this technical issue.
- Main/supplement underfull diagnostics remain from Phase 9C.
- Author identity, declarations, JISA guide/portal requirements remain unresolved.

Canonical submission untouched. No manuscript rewrite, experiment, recomputation, commit, push, merge, rebase, or submission performed.
