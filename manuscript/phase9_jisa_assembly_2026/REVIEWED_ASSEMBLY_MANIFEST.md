# Reviewed JISA assembly manifest

## Checkpoint

- Repository: `the mubasshir/ids2018-validation-safe-ablation`
- Branch: `manuscript-journal-revision-2026`
- Base/local/remote Git commit: `228e8c94f2c16abd138b775917f2069e91c06107`
- Assembly root: `manuscript/phase9_jisa_assembly_2026/`
- Canonical `submission/jisa/*`: untouched.

## Reviewed source

- Main LaTeX: `source/manuscript.tex`
- Integrated bibliography: `source/references.bib`
- Highlights: `source/highlights.txt`
- Main figures: `source/figures/figure1.png`, `figure3.png`, `figure4.png`, `figure6.png`, `fig2.png`, `fig5.png`
- Supplement LaTeX: `source/supplement/supplement.tex`
- Supplement manifest: `source/supplement/source-manifest.csv`
- Supplement figures: `source/supplement/figures/stage27_primary_roc_auc_ci.png`, `stage27_balanced_recall_ci.png`
- Supplement source artifacts: `source/supplement/source/`

## QA evidence

- Scientific provenance: `qa/complete_numerical_claim_audit.csv`, `qa/phase9c1_source_field_ledger.csv`, `qa/phase9c2_source_verification_receipts.csv`, `qa/phase9c3_reclassification_audit.csv`, `qa/phase9c3_independent_receipt_audit.csv`, `qa/phase9c3_scientific_validation_report.md`
- Final review: `qa/phase9c3_final_review_decision.md`, `qa/final_submission_blockers.md`
- Visual/build QA: `qa/pdf_visual_qa.md`, `qa/latex_build_report.md`, `qa/phase9c3_latex_diagnostics.md`, `qa/toolchain_verification.md`
- PDF extraction evidence: `qa/phase9c_pdf_glyph_diagnostics.csv`, `qa/phase9c3_glyph_resolution.csv`, `qa/phase9d_pdf_qa_addendum.md`
- Integration history: `qa/integration_change_log.md`

## Scientific and technical status

- Numeric-bearing rows: 207.
- Corrected scientific numerical rows: 67.
- Scientific verification: 14 `VERIFIED_SOURCE_FIELD`; 50 `VERIFIED_ORIGINAL_REPORT`; 3 `VERIFIED_PROTOCOL`; 0 unresolved.
- Reclassification review: 61/61 accepted; 0 reversed.
- Main PDF: 36 pages. Supplement PDF: 7 pages.
- Main/supplement overfull boxes: 0/0.
- Underfull boxes: main 8; supplement 7; reviewed as harmless bibliography URL composition.
- Figures/tables: six main figures and six main tables retained.
- Supplement: S1–S7 and Tables S1–S10 retained.
- Visual glyph inspection: no observed visible defect.
- Extraction verification: original `fitz` PyMuPDF binding reported 20 replacements; `pymupdf` import reported 0. Same PyMuPDF/MuPDF backend, not independent. Independent text-extractor/font-mapping verification remains outstanding.

## Build instructions and reviewed PDFs

Manual sequence documented in `qa/latex_build_report.md`; `latexmk` unavailable because Perl is absent. Local reviewed PDFs:

- `build/main/manuscript.pdf` — SHA-256 `00abf3e55a3e6ca3cd08df500873de6c309a531f2f08eb8e35bdc9defaed6fe1`
- `build/supplement/supplement.pdf` — SHA-256 `43d5c68ec0235d88f7daf2faf5527f30580359f17769af70f3f66e5c63f7bf25`

Checksums identify the reviewed builds; they do not establish byte-for-byte reproducibility or independently establish scientific correctness. PDFs remain local and are excluded from the Git checkpoint.

## Exclusions

Build outputs, auxiliary files, logs, extracted text, rendered previews, temporary scripts/caches, private author metadata, credentials, and unapproved declarations are excluded. Canonical submission and frozen experiments remain untouched.

## Outstanding decisions

- Author names, affiliations, corresponding author, ORCID, funding, conflicts, ethics, acknowledgments, CRediT, data/code, and AI-use disclosures.
- JISA article type, current Guide for Authors, artwork/length, portal, access/APC, and other publisher requirements.
- Independent PDF text-extractor or font-mapping verification.
- Overall submission readiness remains blocked; this manifest does not mark the assembly submission-ready.

## Official publisher URLs

- Elsevier AI policy: `https://www.elsevier.com/about/policies-and-standards/generative-ai-policies-for-journals`
- JISA Guide for Authors: `https://www.sciencedirect.com/journal/journal-of-information-security-and-applications/publish/guide-for-authors`
