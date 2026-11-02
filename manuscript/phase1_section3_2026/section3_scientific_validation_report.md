# Section 3 Scientific Validation Report

## Scope

Section 3 audited the frozen dataset/provenance chain only. No manuscript integration was made into `submission/jisa/manuscript.tex`. Stage29 was treated as synthesis, not new evidence.

## Repository verification

- Repository: `themubasshir/ids2018-validation-safe-ablation`
- Worktree: `D:\ids2018-journal-revision`
- Branch: `manuscript-journal-revision-2026`
- HEAD: `2a6b689`
- Remote: `https://github.com/themubasshir/ids2018-validation-safe-ablation.git`
- Git status: clean before draft creation; new files are untracked draft deliverables only.
- Existing manuscript sources read: `manuscript/manuscript_journal_revision.md`, `submission/jisa/manuscript.tex`.

## Source files inspected

- `docs/STAGE29_MANUSCRIPT_SYNTHESIS.md`
- `docs/manuscript/MANUSCRIPT_SOURCE_MAP.csv`
- `docs/manuscript/MANUSCRIPT_FIGURE_TABLE_PLAN.md`
- `results/stage29_manuscript_synthesis/evidence/master_evidence_matrix.csv`
- `results/stage29_manuscript_synthesis/evidence/final_manuscript_numbers.csv`
- `results/stage29_manuscript_synthesis/evidence/validity_axis_matrix.csv`
- `results/stage29_manuscript_synthesis/evidence/source_artifact_registry.csv`
- `results/stage29_manuscript_synthesis/claims/final_claim_registry.csv`
- `results/stage29_manuscript_synthesis/manuscript/proposed_manuscript_structure.md`
- `results/stage29_manuscript_synthesis/manuscript/limitations_matrix.csv`
- `configs/stage01/protocol.json`
- `configs/stage18/protocol.json`
- `configs/stage22/protocol.json`
- `configs/stage24/protocol.json`
- `configs/stage27/protocol.json`
- `configs/stage28/protocol.json`
- `docs/STAGE22R_MANUSCRIPT_INTEGRATION.md`
- `docs/RESULTS_SUMMARY.md` and relevant stage integration/closeout records
- `docs/reproducibility/STAGE_REPRODUCIBILITY_STATUS.csv`
- `docs/reproducibility/MANUSCRIPT_CRITICAL_TRACEABILITY.csv`
- `docs/reproducibility/FINAL_REPRODUCIBILITY_AUDIT.md`
- Relevant archived notebooks and scripts listed by the Stage18, Stage22, Stage24, Stage27, and Stage28 protocol locks.

## Stages covered

Primary Section 3 coverage: Stages 01, 11, 18, 20, 22, 24, 27, and 28. Governance and reproducibility statements cover the Stage01–28 chain. Earlier representation and architecture work was retained through explicit provenance boundaries: Stage18 ViT feasibility is not presented as a performance result; Stage18 graph and Stage21 CNN/ViT evidence remain descriptive/supplement-only; Stage20 contributes CICIDS2017 source provenance.

## Populations distinguished

1. Processed, stratified CSE-CIC-IDS2018 reference: 192,593/48,149/60,186 memberships; 78 numeric predictors.
2. Timestamp-recovered Stage18 audit population: 192,521 rows, incomplete temporal provenance.
3. K79-clean Stage22R development and shared Mar1–Mar2 forward target: 1,374,133 target rows; exact identity control only.
4. IDS2018-to-CICIDS2017 bridge62 target: 2,830,743 effective rows.
5. CICIDS2017-to-IDS2018 February 28 target: 593,780 rows; attack prevalence 0.10484691299808009.
6. Processed known-category attack holdout: distinct from LOAO.
7. LOAO family populations: five eligible folds; two structurally ineligible families; Infiltration descriptive at 36 positives.
8. Repository artifact/provenance populations: source, corrected, published, source-faithful, reconstructed, hash-only, and closed-target states.

## Numerical claims checked

- Reference memberships and class counts: `E29-001`, `NUM29-001`–`NUM29-009`.
- Stage18 temporal provenance: `E29-016`, `NUM29-060`–`NUM29-063`.
- Stage22R forward target counts/prevalence: `E29-020`, `NUM29-078`–`NUM29-081`.
- CICIDS2017 forward target and transfer population: `E29-024`, `NUM29-090`–`NUM29-092`.
- Reciprocal target population/prevalence: `E29-025`, `NUM29-093`–`NUM29-095`.
- Cancelled cells: `E29-027`, `NUM29-099`.
- Known-category versus LOAO support distinction: `E29-013`, `E29-035`, `NUM29-048`–`NUM29-052`, `NUM29-117`–`NUM29-118`.
- Stage28 closure: `E29-041`, `NUM29-132`–`NUM29-134`.

No new numerical values were computed. Values were transcribed from frozen registries, protocol locks, or authoritative stage integration artifacts.

## Assumptions and limitations preserved

- Processed reference data are not natural-prevalence or temporal evidence.
- Source-faithful does not mean raw-packet or byte-complete.
- K79 is not S4, session, endpoint, source-IP, or five-tuple independence.
- Stage22/Stage28 share a historically opened target; stability is not a fresh blind replication.
- Timestamp recovery and temporal bins do not identify concept drift.
- Bridge62/70 conclusions are direction-, bridge-, preprocessing-, and population-specific.
- `GROUNDED_S4` cancellations have no scientific result.
- Known-category results are not LOAO evidence.
- Infiltration LOAO support is 36 and descriptive only; DOS and AUTH_BRUTE_FORCE are ineligible.
- Hashes and static equivalence records do not establish full end-to-end rerun reproducibility.
- External raw data, some historical models/arrays/explanations, closed targets, and portions of software environments remain unavailable or restricted.

## Evidence conflicts and discrepancies

1. **K79 language conflict in historical Stage23 artifacts.** Some Stage23 audit text uses broad language such as “session independence” or “endpoint/IP/5-tuple disjointness.” The authoritative Stage22R protocol and integration records explicitly restrict K79 to exact timestamp-plus-78-predictor identity and prohibit those stronger interpretations. The draft follows the narrower authoritative boundary. Author review recommended for repository-wide harmonization; no frozen artifact was edited.
2. **Known-category `Infilteration` support 3,967 versus LOAO `Infiltration` support 36.** This is a population distinction, not treated as a numerical contradiction. Draft states both roles explicitly.
3. **Bridge70 versus bridge62 correction semantics.** Bridge62 published and flag-corrected are bitwise identical because excluded aggregate fields are absent; bridge70 published/corrected remain distinct. Draft preserves this distinction.
4. **Existing Section 3 wording.** The current manuscript describes the same broad roles but compresses provenance and does not fully state the K79 independence ceiling, bridge cancellation governance, or reproducibility boundaries. Draft is isolated; existing manuscript unchanged.

## Unsupported or unresolved statements

- Exact raw-source byte identity for all historical populations: unresolved/unavailable.
- Session, endpoint, source-IP, or five-tuple independence: unsupported by K79.
- Complete historical rerun equivalence for Stages01–24, 27, and 28: unsupported; static/partial status retained.
- Universal dataset portability or zero-day detection: unsupported and excluded.
- Any scientific result for the two cancelled `GROUNDED_S4` cells: nonexistent.

No verification markers were needed in the final draft for statements covered by the frozen source registries. Author review remains required for the discrepancy list above.

## Required supplementary cross-references

- Stage01–28 reproducibility status matrix.
- Stage21–24 and Stage25–28 source registries/reconciliation records.
- K79 cleaning and membership receipts.
- Bridge62/bridge70 semantic bridge specification and cancellation record.
- LOAO taxonomy, fold eligibility, and support tables.
- Stage28 seed/control closure and shared-holdout provenance.
- Full claim/evidence/number/source map and limitations matrix.

## Safety confirmation

- Frozen original research artifacts: unchanged.
- Canonical evidence registries: unchanged.
- Existing LaTeX manuscript, bibliography, figures, supplementary PDF, and declarations: unchanged.
- Training: not run.
- Inference: not run.
- Threshold optimization: not run.
- Bootstrap resampling: not run.
- Target-opening workflow: not run.
- Scientific recomputation: not run.
