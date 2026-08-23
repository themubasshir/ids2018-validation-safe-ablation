# Pass 2A Literature Verification Protocol

Status: **FROZEN BEFORE EXTERNAL SEARCH**  
Branch: `manuscript-reproducibility-cleanup`  
Accepted baseline: `8ae5cde`  
Primary manuscript: `manuscript/manuscript_reconstructed.md`  
Scientific boundary: Stage28 remains the final empirical wall; Stage29 remains synthesis-only.

## Purpose and sequence

Pass 2A builds a verified literature layer beneath the accepted Pass 1 manuscript. It inventories literature-dependent claims, freezes the ten gap requirements, verifies any existing citations, searches only for those defined needs, records candidate quality and directness, maps selected references to claims, and integrates citations with minimal wording changes.

External literature may contextualize the frozen evidence. It may not alter scientific results, numbers, claim status, figures, tables, limitations, or the Stage29 interpretation ceiling.

## Pre-search state

- Active reference-gap placeholders: **10**.
- Existing manuscript citation keys: **0**.
- Existing canonical bibliography entries: **0**.
- Existing bibliography format: **none located**.
- Canonical Pass 2A bibliography target: `manuscript/references.bib` in BibTeX format.
- Canonical in-text citation syntax: Pandoc-style `[@citation_key]`, with multiple sources written `[@key_one; @key_two]`.

The absence of existing references is a verified inventory result, not permission to populate the bibliography from memory.

## Source-selection criteria

A source may be selected only when all applicable criteria are met:

1. The work is identifiable through an authoritative publisher, venue, DOI, standards body, official dataset page, or stable institutional record.
2. The inspected source—not a search snippet or secondary summary—supports the mapped claim at the recorded level.
3. Bibliographic fields are verified against the publisher/venue or DOI record; no missing field is inferred.
4. The source's population, protocol, terminology, and conclusion match the claim closely enough to avoid scope inflation.
5. A primary source is preferred when the claim concerns a method, dataset, empirical result, or specific evaluation failure.
6. Reviews are used for field context or source discovery, not as substitutes for an available original method or dataset paper.
7. Sources selected for broad field statements must justify that breadth; otherwise the manuscript wording is narrowed.
8. Conflicting findings are retained in the candidate registry and reflected in wording when material.

## Preferred source hierarchy

1. Original peer-reviewed paper directly establishing the relevant point.
2. High-quality peer-reviewed systematic review or survey for synthesis-level context.
3. Official dataset, standards, or institutional source for provenance and definitions.
4. Peer-reviewed contextual source that supports only background framing.
5. Preprint only when no adequate peer-reviewed source is available, with explicit `PREPRINT` and `NON_PEER_REVIEWED` flags.

Publisher and venue reputation informs quality but does not replace source-level verification. IEEE, ACM, USENIX, NDSS, RAID, Springer, Elsevier, and Wiley are preferred where relevant; legitimate peer-reviewed sources from other venues remain eligible.

## Acceptable publication years

- Foundational method, metric, dataset, or reproducibility sources: no lower year bound when the source is original and still authoritative.
- Dataset provenance: prefer the official release documentation and original associated publications contemporaneous with CICIDS2017 or CSE-CIC-IDS2018; later sources may supplement but not overwrite historical documentation.
- Empirical IDS validation and cross-dataset work: prefer 2010–2026, with priority to directly relevant work from 2015–2026.
- Deployment and reproducibility guidance: prefer 2015–2026, while retaining older foundational guidance where necessary.
- Search cutoff: sources available and verifiable by **2026-08-23**.

Recency never overrides directness or primary-source status.

## Citation-verification rules

For each selected or existing reference:

1. Verify title, authors, year, venue, and publication status from an authoritative record.
2. Verify DOI through the publisher/DOI landing page when a DOI should exist; record `NO_DOI_ASSIGNED` only when that status is defensible.
3. Record volume, issue, pages, publisher, and URL only when explicitly verified.
4. Inspect the abstract plus the methods/results or official documentation needed to establish claim support. Metadata-only verification cannot yield `DIRECT_SUPPORT`.
5. Record the exact manuscript locations and literature claim IDs supported.
6. Use `DIRECT_SUPPORT`, `PARTIAL_SUPPORT`, `BACKGROUND_ONLY`, `DOES_NOT_SUPPORT`, or `UNVERIFIED` exactly as defined by the task.
7. A source marked `DOES_NOT_SUPPORT` or `UNVERIFIED` cannot remain attached to the claim.
8. When full text is inaccessible, use only claims supported by the accessible authoritative abstract/record and mark the limitation.
9. Do not cite search-engine snippets, AI summaries, blogs, unsourced repository prose, or citation lists not independently checked.

## Duplicate handling

- Normalize DOI values to lowercase bare DOI form for comparison.
- Treat identical DOI values as one work.
- When DOI is absent, compare normalized title, first author, and year; inspect suspected matches manually.
- Prefer the final peer-reviewed version over a preprint when they represent the same work.
- Preserve one stable citation key and record all merges or key changes in `BIBLIOGRAPHY_CHANGELOG.csv`.
- Do not merge distinct conference and extended journal versions without verifying their relationship and selecting the version that supports the claim.

## Preprint handling

Preprints are admissible only if no adequate peer-reviewed or official source resolves the frozen gap. They must be labeled `PREPRINT`, `NON_PEER_REVIEWED`, and at most `TIER_4_CONTEXTUAL` unless the closeout explicitly justifies a different classification. A preprint cannot establish a broad priority or field-wide claim. If a peer-reviewed version exists, the final version replaces the preprint.

## Dataset-paper handling

- Pair official dataset documentation with the original associated publication when both are needed.
- Verify exact dataset name, institution, release context, dates, attack families, traffic-generation claims, and extraction tooling only from the relevant historical source.
- Do not infer CICIDS2017 facts from CSE-CIC-IDS2018 documentation or vice versa.
- Do not use later secondary studies to overwrite official historical terminology.
- Project-specific forensic findings remain supported by frozen internal evidence, not retroactively attributed to external literature.
- Official web documentation may be classified `TIER_3_OFFICIAL_SOURCE`; the associated peer-reviewed paper retains its peer-review tier.

## Survey and review handling

Reviews may support taxonomy, field context, or a carefully bounded synthesis. They may not replace an original dataset/method paper or be cited as direct evidence that a specific primary experiment used a stated protocol unless the underlying paper is checked. Statements such as “most studies” require a systematic, quantitatively adequate source and will otherwise be narrowed.

## Claim-strength rules

- `DIRECT_SUPPORT`: the source directly studies, defines, or documents the material claim with matching scope.
- `PARTIAL_SUPPORT`: the source supports only part of a compound claim; the claim must receive another source, be split, or be narrowed.
- `BACKGROUND_ONLY`: the source contextualizes the area but cannot substantiate the empirical or comparative assertion.
- `DOES_NOT_SUPPORT`: the inspected source conflicts with or fails to establish the claim; detach it.
- `UNVERIFIED`: identity or support could not be checked; do not integrate it.

Final coverage is `FULL` only when all material clauses of the literature claim have direct or appropriately combined support. `PARTIAL` requires visible qualification or an explicit unresolved record. `NONE` requires removal, non-assertive reframing, or a retained justified gap.

## Reference quality tiers

- `TIER_1_PRIMARY`: original peer-reviewed dataset, method, empirical, or evaluation study.
- `TIER_2_HIGH_QUALITY_REVIEW`: peer-reviewed systematic review or authoritative survey.
- `TIER_3_OFFICIAL_SOURCE`: official dataset, standards, publisher, or institutional documentation.
- `TIER_4_CONTEXTUAL`: legitimate but indirect contextual source.

Additional flags are `PREPRINT`, `NON_PEER_REVIEWED`, and `SECONDARY_FOR_PRIMARY_CLAIM`.

## Prohibited citation behavior

Pass 2A must not:

- invent citations, authors, titles, venues, pages, DOIs, URLs, or citation keys;
- cite a search result, snippet, AI answer, blog, or uninspected bibliography entry as scientific support;
- search first and reshape a gap around a convenient paper;
- attach a citation to clauses it does not support;
- cite one small sample as evidence for “most IDS studies,” “the literature generally,” or a field-wide absence;
- use a review when an original method/dataset paper is required and available;
- use an external paper to broaden or reinterpret a frozen Stage29 claim;
- imply that literature agreement validates this project's empirical result beyond its frozen population;
- conceal contradictory or null prior work;
- use `first`, `first comprehensive`, or `first framework` without evidence sufficient to establish priority;
- preserve a citation merely because it appeared in an archival fragment;
- replace an unresolved gap silently.

## Change-control rules

The literature registries must be complete before citation integration. Manuscript edits are limited to replacing gap markers, correcting literature facts or unsupported wording, adding narrowly necessary context, and correcting citation placement. Scientific numbers, results, tables, figures, and all 18 limitations are immutable in Pass 2A.

Every external source considered must enter `CANDIDATE_REFERENCE_REGISTRY.csv`, including rejected candidates. Every integrated key must resolve in `manuscript/references.bib`, map to at least one literature claim, and appear in the bibliography changelog.

This protocol is frozen by the first Pass 2A commit and may not be relaxed after search results are seen. Any necessary amendment must be explicit, justified, separately committed, and may only strengthen—not weaken—the verification standard.
