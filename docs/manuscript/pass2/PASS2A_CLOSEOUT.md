# Pass 2A Literature Verification Closeout

Status: **COMPLETE — STOP BEFORE PASS 2B**  
Branch: `manuscript-reproducibility-cleanup`  
Accepted baseline: `8ae5cde`  
Verified integration/test head before this closeout: `353a6e6`  
Search and verification cutoff: 2026-08-23

## Outcome

Pass 2A built a claim-level verified literature layer beneath the accepted Pass 1 manuscript. The work began with a committed pre-search protocol and ten frozen reference-gap specifications, audited the zero-reference baseline, evaluated 38 candidate sources, selected 27 references, built both directions of the citation-support graph, created the canonical BibTeX bibliography, and minimally integrated citations after the registries were complete.

The final bibliography contains 23 peer-reviewed Tier 1 primary sources, two Tier 2 high-quality reviews, and two Tier 3 official dataset sources. No preprint is integrated. The two non-peer-reviewed entries are the official Canadian Institute for Cybersecurity dataset pages required for historical provenance; both are paired with peer-reviewed sources where a scientific claim requires them.

All 40 inventoried literature claims have `FULL` coverage after the documented wording narrowings. All ten original reference gaps are fully resolved. No citation marked `DOES_NOT_SUPPORT` or `UNVERIFIED` remains attached to a manuscript claim, all 27 manuscript citation keys resolve to unique bibliography entries, and every bibliography entry maps back to at least one literature claim.

## Required report

1. **Commits created:** nine Pass 2A commits including this closeout: `32277a8`, `72068eb`, `4cb2751`, `74441ad`, `49073c9`, `db28f3c`, `5efd479`, `353a6e6`, and the closeout commit containing this report.
2. **Total existing references audited:** 0. The accepted manuscript and repository contained no citation keys or canonical bibliography entries.
3. **Existing references verified:** 0 of 0; the header-only verification registry preserves this audited result.
4. **Metadata corrections:** 0 existing-reference corrections. All 27 final entries are new verified additions; one disputed SHAP proceedings page range was deliberately omitted and documented rather than inferred.
5. **References removed:** 0 existing references. Eleven searched candidates were rejected from integration and remain documented in the candidate registry.
6. **Original reference-gap count:** 10.
7. **Gaps fully resolved:** 10.
8. **Gaps partially resolved:** 0.
9. **Unresolved gaps:** 0.
10. **New references added:** 27.
11. **Peer-reviewed primary-source count:** 23 Tier 1 primary sources. The final set also contains two peer-reviewed Tier 2 reviews and two Tier 3 official dataset sources.
12. **Literature claims inventoried:** 40.
13. **Literature claim coverage:** `FULL` 40, `PARTIAL` 0, `NONE` 0. Twenty claims required documented narrowing before receiving full coverage; twenty retained their audited scope.
14. **Related Work claims narrowed or removed:** all 10 paragraph-level audits required bounded narrowing; 10 were narrowed and 0 were removed.
15. **Contribution statements requiring narrower novelty wording:** 1 of 6. Contribution 1 now says the study “applies” its connected framework rather than implying invention of the component evaluation axes. The other five remain defensible as study-specific contributions.
16. **Bibliography duplicate corrections:** 0 duplicates existed at baseline and 0 duplicate keys or normalized DOIs remain. Preprint/final-version duplicates were rejected before bibliography integration.
17. **Remaining preprints/non-peer-reviewed sources:** 0 preprints; 2 non-peer-reviewed official dataset pages, both classified `TIER_3_OFFICIAL_SOURCE` and used only for provenance/documentation.
18. **Manuscript word count after minimal integration:** 9,305 whitespace-delimited words, including headings, captions, tables, and citation keys.
19. **Repository/static-test results:** `python -m unittest discover -s tests -v` passed 158/158 tests in 2.111 seconds with no failures or skips. Pass 2A checks cover artifact presence, candidate decisions, gap coverage, bibliography metadata, key/DOI uniqueness, two-way claim mapping, novelty bounds, the Stage28 wall, and empirical-text immutability.
20. **No scientific number or result changed:** confirmed. The decoded text from `## 4. Validation Framework and Methods` through the end of `## 8. Conclusion` has SHA-256 `ed4d2a278b4d5db7d1dbb9f7de45926cd7f6de9e64a13b0c785522005bd52ffe`, identical to accepted baseline `8ae5cde`. All six main figure references, six main table references, and all 18 limitation concepts remain represented.
21. **Stage28 remains the final empirical wall:** confirmed by the frozen Stage29 lock and the Pass 2A test suite. Stage29 remains synthesis-only.
22. **No new scientific computation occurred:** confirmed. Pass 2A performed literature search, metadata/source verification, CSV/Markdown/BibTeX editing, hashing, and static/unit tests only. It performed no fitting, model loading, inference, holdout opening, thresholding, bootstrap, metrics, profiling, dataset reconstruction, prevalence analysis, LOAO analysis, seed analysis, feature analysis, or scientific reinterpretation.

## Commit sequence

1. `32277a8` — `docs: freeze Pass2A literature verification protocol`
2. `72068eb` — `docs: inventory manuscript literature claims and gaps`
3. `4cb2751` — `docs: verify existing bibliography`
4. `74441ad` — `docs: research and resolve reference gaps`
5. `49073c9` — `docs: audit related-work support and novelty positioning`
6. `db28f3c` — `docs: build citation claim matrix and bibliography changelog`
7. `5efd479` — `docs: integrate verified citations into manuscript`
8. `353a6e6` — `test: validate Pass2A citation and evidence integrity`
9. closeout commit — `docs: close Pass2A literature verification`

Each completed commit was pushed individually to `origin/manuscript-reproducibility-cleanup`. No force push or merge to `main` occurred.

## Stop condition

Pass 2A is closed. No broad stylistic rewrite, journal-template conversion, title selection, or other Pass 2B editorial work has begun. Further manuscript editing requires explicit Pass 2B approval.
