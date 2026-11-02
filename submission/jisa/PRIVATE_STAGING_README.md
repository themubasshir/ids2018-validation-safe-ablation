# Private JISA Submission Staging

Create the actual staging directory locally, outside the Git worktree, only after author approval data is available. Recommended location:

`%LOCALAPPDATA%\Temp\opencode\jisa_submission_staging\`

Do not place personal names, addresses, phone numbers, emails, signatures, ORCID records, or unpublished approval records in this repository.

## Required contents

- `manuscript.pdf` and editable `manuscript.tex`
- `supplement.pdf` and editable `supplement.tex`
- `highlights.txt`
- `cover_letter.md` or portal-ready cover letter
- `author_metadata_private.csv`
- `declarations_final.md`
- `data_availability_final.md`
- `figures/`
- `references.bib`
- `submission_checklist.md`
- final approval record stored privately

## Metadata template fields

Use explicit placeholders until contributors supply verified values:

- `AUTHOR_NAME_01`, `AUTHOR_ORDER`
- `AFFILIATION_01`
- `CORRESPONDING_AUTHOR`
- `CORRESPONDING_EMAIL`
- `ORCID`
- `FUNDING_STATEMENT`
- `COMPETING_INTERESTS`
- `CRediT_ROLES`
- `OVERLAP_STATEMENT`
- `ETHICS_CONFIRMATION`
- `PUBLIC_DATA_CODE_URL`
- `FINAL_APPROVAL_RECORD`

This file is a handling instruction, not an authorization to copy private data into Git.
