# Section 4 Scientific Validation Report

## Scope and safety

Section 4 was drafted as an isolated Methods artifact. Phase 1 deliverables were reviewed first. No original notebook, script, config, frozen result, registry, or canonical manuscript was modified. No fitting, inference, target opening, threshold search, resampling, model comparison, or scientific recomputation was performed. Static/document inspection only.

## Coverage

Covered stages: 1–14 reference governance, uncertainty, calibration, operational cost, known-category, and explanation methods; 15–21 architecture and representation diagnostics; 22/22R temporal validation; 23 shortcut audit; 24 transfer; 25 prevalence and operational stress; 26 deployment profiling; 27 LOAO; 28 seed/control stability. Stage29 was treated as synthesis and traceability, not scientific computation.

## Files and source classes inspected

- Phase 1: `manuscript/phase1_section3_2026/section3_datasets_and_provenance.md`, `section3_evidence_traceability.csv`, `section3_scientific_validation_report.md`, `section4_methods_handoff_outline.md`.
- Authoritative notebooks: `notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb`, `stage21_stage22_research_continues.ipynb`, `stage23_research_executed.ipynb`, `stage24_cross_dataset_executed.ipynb`, `stage26_deployment_profiling_executed.ipynb`, `stage27_loao_unseen_attack_executed.ipynb`, `stage28_stability_novelty_control_executed.ipynb`.
- Canonical/recovered scripts: Stage23, Stage24, Stage25, Stage26 archival export, Stage27, and Stage28 archival linearization.
- Protocols: `configs/stage01/` through `configs/stage28/`, including Stage20 scoped subconfigs.
- Reproducibility: `docs/reproducibility/STAGE_CODE_INVENTORY.csv`, `MANUSCRIPT_CRITICAL_TRACEABILITY.csv`, and `FINAL_REPRODUCIBILITY_AUDIT.md`.
- Integration/evidence: `docs/STAGE22R_MANUSCRIPT_INTEGRATION.md`, Stage29 registries, result manifests, and `submission/jisa/supplement/supplement.tex`.

## Verified methodological parameters

- Early reference representation: 78 numeric predictors; frozen stratified memberships; training-only scaling where applicable; seed 42.
- Stage22R: K79 exact corrected-second timestamp plus 78 common numeric predictors; ordered 70-feature model representation; four random/chronological × natural/rebalanced cells; equal-weight LightGBM/XGBoost; validation-only thresholds; one shared forward holdout.
- Stage23: seven registered subsets, matched placebos, stump/depth controls, proxy diagnostics, and explanation/uncertainty closure.
- Stage24: bridge62 excludes eight aggregate flag fields; bridge62 published/corrected bitwise identical; bridge70 published/corrected distinct; four fits, six evaluable openings, two cancelled `GROUNDED_S4` cells; 2,000 paired bootstrap replicates where applicable.
- Stage25: prevalence `[0.1, 0.03, 0.01, 0.003, 0.001, 0.0001]`; one million benign flows/day; two minutes/alert; analyst tiers `[1,3,10]`; 240 alerts/analyst/day; `C_FP=1`, `C_FN=100`.
- Stage26: batch sizes `[1,64,256,1024,8192]`; CPU/Tesla T4 component profiling; prepared-input boundary.
- Stage27: seven-family taxonomy; five eligible folds; DOS and AUTH_BRUTE_FORCE ineligible; Infiltration descriptive at 36 positives; 2,000-replicate stratified row bootstrap; known-family validation thresholds.
- Stage28: seeds `[42,43,44,45,46]`; 108 new fits and 12 reuses; no best-seed selection or new significance tests; shared Stage22R holdout reused under frozen governance.

## Population and representation separation

The draft separates the processed reference population, source-faithful IDS2018 temporal populations, CICIDS2017 transfer populations, Stage15–21 architecture/representation populations, Stage24 bridge contracts, Stage25 scalar projections, and Stage27 LOAO populations. It does not pool metrics across these estimands. It preserves the distinction between 78-predictor early reference methods, duplicate-safe 70-feature methods, K79 identity, packet/time representations, bridge62, and bridge70.

## Governance verification

Frozen-target governance is preserved. The draft states validation-only threshold selection, training-only preprocessing/rebalancing, source-only transfer, known-family LOAO thresholds, one-time historical openings, cancelled `GROUNDED_S4` cells, permanent closure, and Stage28 final-wall status. It does not claim fresh blind holdout access or post-holdout adaptation.

## Supplement audit

Cross-references were checked against `submission/jisa/supplement/supplement.tex`. The draft uses S1–S7 and Tables S1–S10 as publication references. Stage29 IDs (`E29-*`, `C*`, `F*`, `T29-*`) remain evidence identifiers and are not substituted for supplement labels. Stage15–21 descriptive/supplement-only methods are routed to S2 or bounded as diagnostics.

## Discrepancies and limitations

1. Historical Stage23 material contains broader K79 wording in places; this draft follows the authoritative Stage22R definition and explicitly rejects S4/session/endpoint/source-IP/five-tuple independence.
2. Stage24 `GROUNDED_S4` cells are cancelled before target opening; no result is implied.
3. Stage18 tabular ViT feasibility rejection and Stage20/21 packet-image ViT work are chronologically and methodologically distinct.
4. Stage26 methodology is reproducible, but historical timings are hardware/software-specific archival measurements.
5. Stage27 `Infiltration` support is 36 in the LOAO population and remains descriptive; this is distinct from known-category `Infilteration` artifact labels and support.
6. Full executable replication is incomplete for most stages because external data, closed targets, unavailable arrays/checkpoints, hash-only artifacts, or unproven historical environments remain.

## Readiness

Section 4 is methodologically ready as an isolated draft and traceability package. It is not a replacement for the canonical manuscript and requires author review of population wording, supplement placement, and the retained Stage23 historical discrepancy before integration. Section 5 remains unwritten and requires separate authorization.
