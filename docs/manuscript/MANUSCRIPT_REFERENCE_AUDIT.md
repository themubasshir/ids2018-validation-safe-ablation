# Pass 1 Reference Audit

Status: intentionally unresolved. No web search, bibliography lookup, citation invention, or external reference verification was performed in Pass 1.

The reconstructed manuscript contains ten active `[REFERENCE GAP: <specific requirement>]` placeholders, all in Section 2. The References section contains no asserted external citations. This preserves the distinction between frozen repository evidence and literature claims that require a later, explicitly authorized search-and-verification pass.

## Gap inventory

| Gap ID | Manuscript location | Specific reference requirement | Preferred source class | Verification needed before replacement | Pass 1 status |
| --- | --- | --- | --- | --- | --- |
| REF-GAP-001 | 2.1, paragraph 1 | Primary CSE-CIC-IDS2018 dataset citation and representative peer-reviewed benchmark-modeling studies | Original dataset paper or official dataset documentation; peer-reviewed empirical studies | Confirm dataset naming, provenance, release context, and that selected studies actually use the stated benchmark and model classes | OPEN |
| REF-GAP-002 | 2.1, paragraph 2 | Methodological work on class balance, benchmark construction, and external validity in IDS | Peer-reviewed methods or evaluation papers | Verify that each source directly supports the distinction among rebalancing, deployment prevalence, chronology, and external validity | OPEN |
| REF-GAP-003 | 2.2, paragraph 1 | IDS research on temporal splitting, session-aware validation, duplicate leakage, and chronological generalization | Primary peer-reviewed IDS evaluation studies | Verify protocol details; do not cite a paper as temporal or session-aware merely because it reports a time-based dataset | OPEN |
| REF-GAP-004 | 2.2, paragraph 2 | Primary studies on leakage, shortcut learning, spurious correlation, and feature-ablation methodology in IDS | Primary empirical or methodological studies | Confirm whether claims concern leakage, shortcut sensitivity, causation, or only feature importance; retain those distinctions | OPEN |
| REF-GAP-005 | 2.2, paragraph 3 | Authoritative TreeSHAP and LIME citations plus work on explanation fidelity and stability | Original method papers and peer-reviewed evaluation studies | Verify method identity and distinguish perturbation stability, surrogate fidelity, local-decision reproduction, and exact decomposition | OPEN |
| REF-GAP-006 | 2.3, paragraph 1 | Cross-dataset IDS studies, semantic feature alignment, and bidirectional transfer evaluation | Primary peer-reviewed empirical studies | Confirm source/target direction, feature bridge, label mapping, target prevalence, and whether both directions were actually evaluated | OPEN |
| REF-GAP-007 | 2.3, paragraph 2 | IDS base-rate literature, alert-workload studies, and operational cost-sensitive evaluation | Foundational and recent peer-reviewed work; authoritative operational studies | Verify that sources support PPV/base-rate reasoning and distinguish projected workload or cost from observed SOC outcomes | OPEN |
| REF-GAP-008 | 2.4, paragraph 1 | IDS deployment profiling and ML-systems performance-reporting guidance | Peer-reviewed systems/evaluation work or authoritative reporting standards | Confirm measurement boundary, batch size, hardware/software specificity, backend compatibility, and end-to-end versus inference-only timing | OPEN |
| REF-GAP-009 | 2.4, paragraph 2 | LOAO, open-set recognition, novelty detection, and zero-day evaluation in IDS | Primary peer-reviewed empirical and methodological studies | Verify family-exposure rules, chronology, support, learner scope, and whether the source actually justifies zero-day terminology | OPEN |
| REF-GAP-010 | 2.4, paragraph 3 | Reproducibility guidance for machine learning and empirical cybersecurity | Authoritative guidelines, standards, or peer-reviewed reproducibility studies | Verify requirements for code, data, environments, provenance, target governance, repeated holdout, and researcher adaptation | OPEN |

## Replacement rules for Pass 2

Each placeholder should be replaced only after a source has been opened and checked. The future audit should record at least: citation key, title, authors, venue, year, DOI or stable URL, source type, exact manuscript sentence supported, verification date, and any scope caveat.

The following rules apply:

- Prefer original papers, official dataset documentation, standards, and peer-reviewed primary studies over secondary summaries.
- Do not use a citation merely because its abstract contains a matching keyword; verify the relevant methods and conclusions in the source.
- Do not attach one citation to a compound sentence unless it supports every material clause, or split the sentence and cite clauses separately.
- Do not use the repository's empirical findings as literature citations, and do not use external literature to expand the frozen Stage 29 empirical claim ceiling.
- Preserve directional, population, metric, support, hardware, and projection qualifiers when the cited literature has a narrower scope.
- Record disagreement among sources rather than selecting only literature that reinforces the manuscript narrative.
- Keep uncited any statement that remains common framing only if the target journal permits it; otherwise retain an explicit gap until verified.

## Pass 1 closure

- Active reference-gap placeholders in Related Work: **10**.
- Verified external references added: **0**.
- Invented or unverified citations added: **0**.
- Bibliography entries added: **0**.
- External browsing performed: **no**.

Reference verification and bibliography construction remain outside Pass 1 authorization.
