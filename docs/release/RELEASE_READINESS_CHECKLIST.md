# Release-Readiness Checklist

Status: **PREPARED, NOT READY TO TAG OR ARCHIVE**  
Date: 2026-08-23  
Branch: `manuscript-reproducibility-cleanup`

`PASS` means the current repository evidence satisfies the check. `PENDING` is reserved for the final pre-release test commit. `BLOCKED` requires a governance or rights decision before a release tag/Zenodo archive.

| # | Check | Status | Evidence or action |
| ---: | --- | --- | --- |
| 1 | Canonical manuscript is unambiguous | PASS | `manuscript/README.md` identifies only `manuscript/manuscript_final_content.md` as canonical. |
| 2 | LICENSE present or blocker documented | PASS, SCOPED | Root `LICENSE` applies MIT only to repository-authored code/original documentation; exclusions are in `docs/release/LICENSE_AUDIT.md`. |
| 3 | `CITATION.cff` valid | PENDING | YAML and required-field checks pass; final pre-release integrity test will make this durable. |
| 4 | README points to canonical manuscript | PASS | Root `README.md` links the canonical file and canonicalization record. |
| 5 | `REPRODUCE.md` current | PASS | Declares Stage 28 terminality, Stage 29 non-experimental status, safe modes, classifications, setup, and verification commands. |
| 6 | `references.bib` current | PASS | 27 unique entries; SHA-256 `b42b3796eda26209d3296a0449b19a92291dd9b1579641c6ec91215d9f15c8ec`. |
| 7 | All JSON configs parse | PENDING | Final static validation will parse every tracked JSON configuration. |
| 8 | All CSV registries parse | PENDING | Final static validation will parse every governed CSV registry. |
| 9 | All tests pass | PENDING | Final count will be recorded after the pre-release integrity test is added. |
| 10 | No internal draft-status prose in canonical manuscript | PASS | Static scan finds no manuscript/pass/status metadata targeted by Pass 2C. |
| 11 | No unresolved reference gaps | PASS | 27/27 citation-audit rows are resolved; no new reference was added. |
| 12 | No scientific-value drift | PASS WITH ROUNDING BLOCKER | 137/137 number occurrences resolve and frozen values are unchanged. Two-decimal abstract displays are not authorized. |
| 13 | Stage 28 wall intact | PASS | `docs/reproducibility/SCIENTIFIC_EXECUTION_BOUNDARY.md` remains binding. |
| 14 | Stage 29 synthesis-only status intact | PASS | Stage 29 and later work remain non-experimental. |
| 15 | No target reopening | PASS | No dataset, target, holdout, prediction array, or model was opened during pre-release work. |
| 16 | No scientific execution mode exposed | PASS | Stage wrappers require `--dry-run` or `--verify-only`; configs declare scientific execution false. |
| 17 | Repository branch clean and synchronized | PENDING | Verify after the final commit and push. |
| 18 | Release tag not yet created | PASS | This task created no tag. Existing historical scientific tags are not a pre-release publication tag. |
| 19 | Zenodo DOI not yet minted | PASS | No DOI or Zenodo identifier is asserted in release metadata. |

## Blocking items before tag/archive

1. **Abstract rounding governance:** `NUM29-091` and `NUM29-094` permit six-decimal display only. The requested `0.67` and `0.11` cannot appear until an explicit registry amendment is approved. Current canonical displays remain `0.667483` and `0.108176`.
2. **Archive rights scope:** before depositing a Zenodo archive, review the archive file list against `docs/release/LICENSE_AUDIT.md`. Exclude artifacts whose redistribution/relicensing rights are not established or add their independently verified terms.
3. **Publication metadata:** confirm the final manuscript author list and any release version/date. DOI, venue, volume, issue, pages, and preferred manuscript citation must remain absent until real.

## Finalization gate

Do not create a publication release tag, mint a Zenodo DOI, merge to `main`, or submit while any `PENDING` item remains or either governance/rights blocker is unresolved. The final static validation commit may close only the dynamic test/cleanliness items; it cannot waive the rounding or archive-rights blocks.
