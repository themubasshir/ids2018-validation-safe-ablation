# Pass 2B Editorial Protocol

Status: **FROZEN before broad editorial editing**  
Branch: `manuscript-reproducibility-cleanup`  
Accepted baseline: `dc03e1b8776092fe49aa98cf9bf737e6774390bc`  
Frozen reconstructed manuscript: `manuscript/manuscript_reconstructed.md`  
Editorial output: `manuscript/manuscript_submission_candidate.md`  
Canonical bibliography: `manuscript/references.bib`

## Scientific wall and scope

Stage28 remains the final empirical wall. Stage29 remains synthesis-only. Pass 2A is the frozen literature baseline except where a verified editorial-consistency defect requires correction. Pass 2B is limited to title selection, editorial compression, structural revision, exhibit integration, claim/number/citation/language auditing, and static validation.

No model fitting, model or scientific-artifact deserialization, inference, target opening, probability analysis, threshold selection, bootstrap generation, confidence-interval generation, statistics, attribution analysis, timing or profiling, prevalence analysis, LOAO or seed recomputation, feature analysis, model selection, new dataset, new architecture, new hypothesis, new result figure, new result table from recomputation, composite metric, or literature expansion is authorized. A literature search is permitted only if an integrated Pass 2A citation is found invalid or insufficient; any such exception must be documented before use.

## Frozen authorities

Editorial decisions must resolve through the following layers:

1. Stage29 claim, number, limitation, evidence, figure, and table registries under `results/stage29_manuscript_synthesis/`;
2. Pass 1 manuscript maps and audits under `docs/manuscript/`;
3. Pass 2A literature registries and closeout under `docs/manuscript/pass2/`;
4. the reconstructed manuscript and canonical bibliography named above.

The request's shorthand path `results/stage29_manuscript_synthesis/claim_figure_table_graph.csv` resolves in the accepted repository to `results/stage29_manuscript_synthesis/manuscript/claim_figure_table_graph.csv`.

Baseline integrity markers:

- reconstructed-manuscript SHA-256: `b0495f7aa48b1b30876cd5ef2b428a876f4020bb7641043a4a6a09bc33bcc8f8`;
- bibliography SHA-256: `b42b3796eda26209d3296a0449b19a92291dd9b1579641c6ec91215d9f15c8ec`;
- Pass 2A Methods-through-Conclusion decoded-text SHA-256: `ed4d2a278b4d5db7d1dbb9f7de45926cd7f6de9e64a13b0c785522005bd52ffe`;
- baseline whitespace-delimited manuscript count: 9,305 words;
- baseline bibliography: 27 unique integrated references;
- Stage29 governance: 20 claim rows, 144 manuscript-eligible frozen numbers, 18 limitations, six conceptual main figures from nine approved source assets, and six main tables.

`manuscript/manuscript_reconstructed.md` is immutable in Pass 2B. All editorial changes go to the submission candidate.

## Claim and evidence lock

Every scientific claim occurrence in the candidate must map to a governed Stage29 claim ID and supporting evidence. The 14 `KEEP` or `KEEP_WITH_QUALIFICATION` claims eligible for the main narrative remain available. `CLM29-017` and `CLM29-018` remain removed. `CLM29-019` and `CLM29-020` may appear only as their bounded replacements. `CLM29-006` and `CLM29-007` remain supplement-only and may not become headline claims.

Seven tensions must remain explicit:

1. benchmark performance versus forward validity;
2. ranking versus frozen-threshold behavior;
3. cross-dataset transfer asymmetry;
4. shortcut-subset interactions versus placebo interactions;
5. stable but frequently unfaithful LIME explanations;
6. PPV versus analyst workload and detection yield;
7. family and learner dependence.

Negative, cancelled, contradictory, low-support, ineligible, unsupported-backend, and unresolved evidence may be compressed but not hidden or converted into favorable evidence.

## Number-preservation rules

Every scientific number retained in the candidate must map to `final_manuscript_numbers.csv` through a number ID, evidence ID, source artifact, and allowed rounding. Values may be removed when prose or an existing table already carries the necessary evidence. Values may not be added, recomputed, averaged, normalized, pooled, or changed outside registered rounding. Exhibit numbers, section numbers, citation years, dataset names, bridge labels, frozen design counts, and scenario labels must be classified separately from scientific-result numbers.

The final audit will compare candidate values with the Pass 1 number audit and the Stage29 registry. A number absent from both must be treated as an error unless it is documented non-result metadata.

## Bibliography and citation lock

The 27-entry Pass 2A bibliography is the frozen baseline. Every manuscript citation key must resolve uniquely, every cited source must remain within the claim scope verified by `CITATION_CLAIM_MATRIX.csv`, and every bibliography entry must remain used. Citation dumping and support-strength inflation are prohibited. No new citation is permitted merely to improve style or breadth.

## Editorial-compression rules

The candidate should use conventional journal prose and a scientific-question architecture. Compression priorities are duplicated stage history, repeated metric definitions, repeated governance mechanics, repeated limitations, redundant interpretation, and values already legible in tables. Stage1-to-Stage28 development chronology is not a narrative structure. Detailed locks, hashes, forensics, full controls, complete grids, and secondary evidence should route to the supplement or repository when the main claim remains understandable and reproducible.

Compression must preserve the six distinct contributions, each validation axis's question/data/split/model scope/frozen decisions/metrics/uncertainty/anti-adaptation boundary, key counterexamples, native metrics, claim ceilings, and all 18 limitations. Target band: approximately 7,500–8,500 whitespace-delimited words, with scientific clarity taking precedence over the numeric target. Abstract target: approximately 200–275 words.

## Figure and table rules

No scientific plot may be changed. The six conceptual main figures must resolve to the nine Stage29-approved source assets and receive final numbering, placement, and self-contained captions defining population or split, metric, learner when needed, uncertainty semantics, and important qualifications. Panel assembly is only a future production action; this pass records source paths and panel order.

The six Stage29-approved main tables remain the evidence baseline. A table may be proposed for the supplement if redundant, but its evidence may not be deleted. Captions must define abbreviations and metric semantics. The integrated validity matrix must not become a composite score.

## Prohibited language and interpretation

The final language audit must review every contextual occurrence of: `prove`, `proves`, `proven`, `catastrophic`, `useless`, `unusable`, `real-world`, `zero-day`, `generalizes`, `robust`, `secure`, `deployment-ready`, `state-of-the-art`, `superior`, `causes`, `because of`, `driven by`, `field-wide`, `most studies`, and `all models`.

Unbounded claims, universal failure/success language, priority claims not established in Pass 2A, causal claims not isolated by controls, observed-field language for Stage25 projections, hardware-independent language for Stage26, pooled transfer or novelty scores, and fresh-blind-holdout language for the reused Stage22 target are prohibited.

## Limitation lock

All 18 Stage29 limitations must remain represented and grouped under dataset/provenance, evaluation/protocol, statistical, operational, hardware/computational, and reproducibility headings. Each material limitation must state its claim ceiling. Compression may merge related sentences but may not merge distinct limitation IDs out of the audit.

## Required outputs and validation

Pass 2B will create the submission candidate plus the title decision, evidence-tension audit, final figure and table registries, supplement plan, language audit, final claim and number audits, LaTeX migration plan, changelog, final audit, and static tests. Static validation must establish complete claim, number, citation, main-exhibit, limitation, and tension resolution; absence of prohibited and removed claims; unique bibliography keys; absence of reference gaps and new scientific values; and preservation of frozen scientific values.

The full repository test suite must pass. Pass 2B stops after the final audit: no submission, merge to `main`, venue-template conversion, scientific panel redrawing, or venue formatting is authorized.
