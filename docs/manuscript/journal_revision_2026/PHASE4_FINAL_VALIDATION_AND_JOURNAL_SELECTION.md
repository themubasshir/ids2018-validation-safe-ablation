# Phase 4 Final Editorial Validation and Journal Selection

Date: 2026-11-01
Branch: `manuscript-journal-revision-2026`
Base: `76e31c52d8a854703c3164fe46d0971cc1bf5494`

## Verification

PASS. Revision files contain only authorized editorial changes: title, abstract descriptor, four contribution statements, Related Work literature comparison, revision bibliography, ledgers, and receipts. No source-worktree changes occurred.

Citation-key audit: PASS; all revision citations resolve. Six added records: Elangovan, Mishra, Mishra correction, Ha Thanh, Berhili, and Berhili Zenodo package.

Canonical byte audit:

| File | Git LF SHA-256 | Local CRLF SHA-256 |
|---|---|---|
| `manuscript/manuscript_final_content.md` | `6e2960155e7749a917fcdeb7afa3a2fd70a4b7882dacb59ce83796b392af731b` | `f62cfce62f31c9e668b4c884aa7e5dc9bec18e5066f3a1b165446fe4b5b4b412` |
| `manuscript/references.bib` | `b42b3796eda26209d3296a0449b19a92291dd9b1579641c6ec91215d9f15c8ec` | `ee31ced9bc7ad5e7616a517a1a2ecf311812001fe2bdd9ffdd02fdec8289fa8b` |

The local hashes match the requested CRLF values; the Git hashes match `git show` object content. Difference: line endings only. Historical records untouched.

Preserved: eight principal sections; six figures; six tables; S1-S7; Stage 28 boundary; frozen thresholds and populations; seven evidence tensions; 18 limitation IDs; cancelled `GROUNDED_S4`; ineligible DOS/AUTH_BRUTE_FORCE; low-support Infiltration; reproducibility restrictions.

## Literature closure

- **Mishra:** correction DOI `10.1371/journal.pone.0349626` verified as a funding-statement correction. No result or methodology correction described.
- **Berhili:** publisher/indexed text and Zenodo metadata independently checked. Zenodo package DOI `10.5281/zenodo.23630499` identifies code, scripts, dataset indices, random seeds, and result files reproducing the paper experiments. Verified overlap includes validation-split bias, seed sensitivity, preprocessing leakage, semantic feature alignment, cross-dataset transfer, target/test-set calibration, and deployable-versus-oracle calibration. Full publisher article access remains incomplete; the manuscript explicitly limits claims to accessible excerpts and does not assert absent methods.
- No unresolved citation-support defect found.

## Final title

**A Multi-Axis Empirical Audit of Machine-Learning Intrusion Detection**

## Confirmed contributions

1. Evidence-governed multi-axis evaluation design using separate native metrics.
2. Claim-to-provenance mapping with explicit static-verification and rerun limits.
3. Heterogeneous empirical findings across temporal, transfer, operating-point, operational, computational, and held-out-family conditions.
4. Study-derived eight-item checklist linking questions, metrics, controls, and interpretation ceilings; no priority claim.

## Final outline

1. Introduction
2. Related Work
3. Datasets and Provenance
4. Validation Framework and Methods
5. Results
6. Discussion
7. Limitations and Threats to Validity
8. Conclusion

Question-driven Results and S1-S7 supplementary plan retained.

## Journal comparison

| Venue | Fit | Novelty/defensibility | Metrics | Access/charges | Format and evidence |
|---|---|---|---|---|---|
| **Journal of Information Security and Applications (JISA)** | Best: information-security application, IDS evaluation, practice-facing validity | Strong fit for a bounded empirical audit; avoid priority/framework novelty | SCImago 2025: best Q1; publisher 2026 page lists CiteScore 8.7, Impact Factor 4.4. JCR quartile not independently accessible; do not infer it from SCImago | Subscription route available; no author fee stated for subscription. OA APC listed by publisher insights: USD 2,970, excluding taxes; verify at submission | Guide: abstract <=250 words; references must match citations; supplementary files supported; Editorial Manager submission; declarations, funding, data availability, permissions required; author biographies requested by guide |
| **Journal of Network and Computer Applications (JNCA)** | Strong network/IDS fit; broader network applications scope | Higher novelty/selectivity pressure; manuscript must foreground network-application impact, not only audit governance | Publisher page: Impact Factor 7.7, CiteScore 16.6. SCImago 2025: Q1 reported by public SCImago-linked record. Exact JCR quartile not independently accessible | Subscription route: no publication fee. OA APC publisher page currently reports USD 3,080 excluding taxes; other page snapshot reports USD 3,420, so confirm current quote | Guide: supplementary files submitted with manuscript, cited in text, captioned; original work only; declarations/funding; online submission; no reliable fixed word limit found |
| **The Computer Journal** | Acceptable computer-science/security fit; less directly application/security-focused | Lower direct fit; novelty threshold still substantial for a broad CS journal | SCImago 2025: best Q2. Current JCR quartile not independently accessible; public sources report 2025 IF 1.6, not treated as official verification | OUP hybrid/subscription model; current APC and optional-charge details require author portal/institution check | Official instructions provide LaTeX package/class and BST, online licensing, self-archiving policy link; inspect current article-type, length, figure, data, and supplementary rules before submission |

Rank: JISA first; JNCA fallback; The Computer Journal third. Rankings are fit/defensibility, not prestige or acceptance probability. JCR values unavailable without authenticated Clarivate access; no invented quartiles.

## Venue checklist

### JISA primary

- Convert to JISA article template and article type.
- Reduce abstract to <=250 words.
- Confirm title, keywords, author affiliations, corresponding author, funding, conflicts, ethics, data/code availability.
- Ensure every citation has a reference and vice versa.
- Prepare S1-S7 as clearly named, cited supplementary files with captions.
- State closed-data, historical-target, static-verification, and hardware-boundary restrictions.
- Prepare editable manuscript, figures, tables, supplementary files, cover letter, and author biographies if required by the current guide.

### JNCA fallback

- Reframe cover letter and introduction toward network-application significance.
- Confirm current APC quote and subscription terms.
- Submit all supplements concurrently; cite and caption each file.
- Check figure formats, declarations, funding, originality, and generative-AI disclosure rules.

### The Computer Journal

- Use official OUP LaTeX class and bibliography style.
- Confirm article type and length restrictions through the current author portal.
- Check figure/table production rules, licensing, self-archiving, data availability, and supplementary policy.

## Decision

**READY WITH DOCUMENTED LIMITATIONS**

Editorial validation complete. Remaining limitations are transparent: Berhili full article access is incomplete; JCR quartile details and some venue-specific length/charge fields require authenticated/current portal confirmation. No scientific integrity blocker. No submission performed.

## Expanded publisher-neutral assessment

The comprehensive international search, discovery matrix, finalist analysis, weighted ranking, shortlists, ethics checks, and updated recommendation are recorded in `COMPREHENSIVE_INTERNATIONAL_JOURNAL_ASSESSMENT.md`. It supersedes the earlier three-venue comparison for selection purposes. Current recommendation: **Computers & Security** primary; **JISA** cost-conscious target; **ACM TOPS** ambitious target; **IEEE Access** fallback.
