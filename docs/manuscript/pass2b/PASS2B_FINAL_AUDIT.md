# Pass 2B Final Editorial and Scientific Audit

Status: **PASS 2B COMPLETE; submission candidate not submitted or venue-formatted**  
Branch: `manuscript-reproducibility-cleanup`  
Accepted baseline: `dc03e1b`  
Candidate: `manuscript/manuscript_submission_candidate.md`  
Candidate SHA-256: `c4879bbc4ca6fa6b8d638984ae1cdd0ebfb25114471c9d7c58634a5a0996ca88`

## 1. Commits

Pass 2B used ten incremental commits, each pushed individually:

1. `8387d3d` — `docs: freeze Pass2B editorial protocol`
2. `a5d54f9` — `docs: finalize title abstract and introduction`
3. `a845541` — `docs: tighten related work datasets and methods`
4. `539f5c0` — `docs: tighten integrated results`
5. `eff0129` — `docs: finalize discussion limitations and conclusion`
6. `c001f2b` — `docs: finalize figure table and supplement plan`
7. `78187a8` — `docs: complete claim number citation and language audits`
8. `aa18dac` — `docs: create submission manuscript candidate`
9. `72641cb` — `test: validate final manuscript evidence integrity`
10. closeout commit containing this report — `docs: close Pass2B editorial audit`

No force push or merge to `main` occurred.

## 2. Title decision

Recommended title: **Beyond Benchmark Scores: A Multi-Axis Validation Framework for Intrusion Detection**.

Conservative alternative: **A Multi-Axis Validation Audit of Machine-Learning Intrusion Detection**.

Memorable alternative: **What Survives the Benchmark? A Multi-Axis Audit of Intrusion Detection**.

The recommended title centers evaluation, does not imply a new IDS architecture, avoids universal failure and priority claims, and remains consistent with all six contributions.

## 3. Word count and reduction

- Pass 2A reconstructed baseline: **9,305** whitespace-delimited words.
- Pass 2B candidate: **7,523** whitespace-delimited words.
- Reduction: **1,782 words (19.2%)**.
- Abstract: **222 words**, within the frozen 200-275 target.

The candidate is within the preferred 7,500-8,500 range. Compression removed repetition and project history without deleting key counterexamples, evidence tensions, claim ceilings, or essential methods.

## 4. Final structure

The candidate contains **11 level-2 sections** and **45 level-3 subsections**:

- Abstract;
- 1. Introduction;
- 2. Related Work: 4 thematic subsections;
- 3. Datasets and Provenance: 4 subsections;
- 4. Validation Framework and Methods: 9 validation/governance subsections;
- 5. Results: 9 scientific-question subsections;
- 6. Discussion: 6 synthesis subsections;
- 7. Limitations: 6 claim-ceiling groups;
- 8. Conclusion;
- References;
- Supplementary Material Plan: 7 subsections.

No Stage1-to-Stage28 chronology is used as manuscript architecture.

## 5. Claim audit

`FINAL_CLAIM_AUDIT.csv` records **115/115 resolved scientific claim occurrences (100%)**. The candidate uses all 14 main-narrative `KEEP`/`KEEP_WITH_QUALIFICATION` claim IDs. The two `SUPPLEMENT_ONLY` claims appear only in Supplement S2 and do not become headline results. No `REMOVE` or `REWRITE` registry row is treated as a retained claim.

Pass 2B removed no newly supported scientific claim. It removed duplicated formulations and maintained these scientific qualifications:

- `CLM29-017` (“The model generalizes”) and `CLM29-018` (“The model detects zero-day attacks”) remain absent;
- temporal evidence retains higher chronological ranking, poor frozen-threshold transfer, finite-seed scope, and mixed controls rather than catastrophic or causal wording;
- shortcut evidence retains split, learner, placebo, and family-composition context rather than a causal transfer-failure claim;
- operational quantities remain analytic projections;
- compute claims remain hardware and component specific;
- family conclusions remain eligibility-, learner-, metric-, threshold-, and support-specific.

## 6. Scientific-number audit

`FINAL_NUMBER_AUDIT.csv` records **137/137 resolved scientific-number occurrences (100%)**, mapping to **84 unique frozen `NUM29` identifiers**. Every occurrence resolves to its number ID, evidence ID, source artifact, allowed rounding, and candidate line. Every `(number ID, displayed value)` pair already existed in the Pass 1 audit; no new scientific value or unregistered rounding entered the candidate.

## 7. Citation and reference audit

- Unique bibliography entries: **27**.
- Unique cited keys: **27**.
- In-text citation-key uses: **46**.
- Citation audit: **27/27 resolved**, all `USED_AND_MAPPED` with verified Pass 2A scope preserved.
- Orphan citations: **0**.
- Unused bibliography entries: **0**.
- Reference gaps: **0**.
- New Pass 2B references: **0**.

The canonical `references.bib` SHA-256 remains `b42b3796eda26209d3296a0449b19a92291dd9b1579641c6ec91215d9f15c8ec`.

## 8. Figures and tables

The main manuscript contains **six conceptual figures** resolving to **nine unchanged Stage29-approved source assets**:

1. temporal PR-AUC and ROC-AUC transfer;
2. shortcut-subset/split interaction;
3. bidirectional normalized PR-AUC and ROC-AUC transfer;
4. PPV under prevalence stress;
5. hardware-specific p95 CPU/GPU comparison;
6. eligible-family ROC-AUC and balanced-threshold recall.

The main manuscript retains **six non-redundant tables**: processed-reference results, five-seed temporal stability, bidirectional bridge62 transfer, selected operational translations, family conclusion stability, and the native-metric validity matrix. No table is moved to the supplement because each answers a distinct main-text question. No scientific plot was altered or assembled; panel production remains deferred.

## 9. Supplement structure

The final supplement plan has seven sections:

1. reference evaluation, uncertainty, and explanation reliability;
2. shortcut, representation, and descriptive architecture diagnostics;
3. cross-dataset contracts and sensitivities;
4. prevalence, workload, capacity, and cost scenarios;
5. deployment profiling detail;
6. family eligibility and realization stability;
7. provenance, equivalence, and reproduction materials.

The plan points to frozen evidence without duplicating the repository. Cancelled, descriptive, low-support, conditional, supplement-only, and hardware-specific statuses remain intact.

## 10. High-risk language audit

The contextual scan covered all 20 requested terms. Nineteen have no occurrence. The sole occurrence is `proven` in Discussion 6.2, where the manuscript explicitly rejects treating a field as proven leakage. It is recorded as `YES_NEGATED_AND_BOUNDARY_PRESERVING` and `KEEP_REVIEWED`. No occurrence of catastrophic, unusable, real-world, zero-day, generalizes, deployment-ready, state-of-the-art, superiority, or unbounded causal language survives.

## 11. Limitations and evidence tensions

All **18/18 Stage29 limitations** remain represented under dataset/provenance, evaluation/protocol, statistical, operational, hardware/computational, and reproducibility groups. Every item states what it prevents the paper from claiming.

All **7/7 evidence tensions** are `PRESERVED`:

1. benchmark versus forward validity;
2. ranking versus thresholds;
3. cross-dataset transfer asymmetry;
4. shortcut-subset versus placebo interactions;
5. stable-but-unfaithful LIME;
6. PPV versus analyst workload and yield;
7. family and learner dependence.

No tension is `WEAKENED` or `LOST`.

## 12. Unresolved editorial issues

There is no unresolved scientific-evidence issue in the Pass 2B candidate. Intentionally deferred production items are:

- target venue and authoritative LaTeX template selection;
- author, affiliation, corresponding-author, funding, conflict-of-interest, data-availability, and venue-specific declarations;
- physical assembly of registered multi-panel figures and venue-specific conversion of SVG assets;
- final supplement artifact assembly and cross-reference numbering;
- venue word-count, reference-style, and graphical-size compliance.

These items require venue approval or author metadata and do not authorize scientific rewriting.

## 13. Static validation

- Focused Pass 2B suite: **13/13 PASS**.
- Full repository suite: **171/171 PASS** using `python -m unittest discover -s tests -v`.
- Failures: **0**.
- Skips: **0**.

The checks cover artifact presence, title/structure/word-count bounds, frozen baseline hashes, claim and number resolution, prohibited and supplement-only boundaries, citation completeness, figure/table source resolution, all limitations, all tensions, high-risk language, supplement/LaTeX stop conditions, and the Stage28 wall.

## 14. Scientific immutability and stop confirmation

**No scientific result changed.** The reconstructed manuscript remains byte-identical at SHA-256 `b0495f7aa48b1b30876cd5ef2b428a876f4020bb7641043a4a6a09bc33bcc8f8`, its frozen Methods-through-Conclusion decoded-text digest remains `ed4d2a278b4d5db7d1dbb9f7de45926cd7f6de9e64a13b0c785522005bd52ffe`, and all candidate scientific values resolve to the accepted number audit and Stage29 registry.

**Stage28 remains the final empirical wall.** Stage29 remains synthesis-only. Pass 2B did not create an empirical stage.

**No new scientific computation occurred.** Work was limited to reading frozen Markdown/CSV/BibTeX authorities; editorial writing; caption, registry, supplement, and migration planning; string/path/key/value checks; hashing; and static/unit tests. No model or scientific artifact was loaded or deserialized; no fit, inference, target opening, probability analysis, threshold selection, bootstrap, confidence interval, statistic, attribution, timing, profiling, prevalence analysis, LOAO analysis, seed analysis, feature analysis, model selection, dataset, architecture, hypothesis, result figure, result table, or composite metric was generated.

Pass 2B stops here. The manuscript has not been submitted, merged to `main`, converted to a venue template, or prepared for submission. Those actions require explicit approval.
