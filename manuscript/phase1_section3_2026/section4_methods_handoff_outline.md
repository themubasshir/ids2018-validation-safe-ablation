# Section 4 Methods Handoff Outline

Section 4 should follow validity questions, not stage chronology. Each subsection must preserve the population, native metric, frozen decision, authoritative implementation/protocol, result artifact, and interpretation ceiling.

## 4.1 Reference evaluation and governance

- Question: within-reference discrimination under processed CSE-CIC-IDS2018.
- Population: Stage01 stratified memberships; Stage05 frozen holdout.
- Methods: training-only scaling where applicable; tree preprocessing; Stage02 baseline inventory; Stage03 validation-only tuning; Stage04 threshold rules.
- Authoritative sources: `configs/stage01/protocol.json`, `configs/stage02/protocol.json`, `configs/stage03/protocol.json`, `configs/stage04/protocol.json`, `configs/stage05/protocol.json`, `docs/RESULTS_SUMMARY.md`.
- Results needed: `E29-001`–`E29-007`; `T29-01`; `final_manuscript_numbers.csv`.
- Boundary: no temporal, transfer, prevalence, deployment, or unseen-family inference.

## 4.2 Temporal validation and split integrity

- Question: ranking and operating-point transfer under forward chronology.
- Population: K79-clean Stage22R development; shared Mar1–Mar2 forward target.
- Methods: exact K79 definition; duplicate/conflict ordering; random/chronological × natural/rebalanced factorial; training-only rebalancing; equal-weight LightGBM/XGBoost; validation-only thresholds; one target opening.
- Authoritative sources: `configs/stage18/protocol.json`, `configs/stage22/protocol.json`, `docs/STAGE22R_MANUSCRIPT_INTEGRATION.md`, Stage22R membership/model-input/final-holdout receipts, `src/ids_validation/stages/stage22/registry.py`.
- Results needed: `E29-016`, `E29-020`, `E29-021`; `C22-001`–`C22-009`; `F22R-01`–`F22R-03`; `T29-03`.
- Boundary: K79 is not S4/session/endpoint/five-tuple independence; chronology and family composition remain entangled; target historically opened.

## 4.3 Shortcut-feature and explanation audit

- Question: sensitivity to plausible shortcut subsets and explanation fidelity.
- Population: frozen Stage22 random-natural and chronological populations.
- Methods: seven preregistered subsets; matched-size placebos; stump/depth controls; proxy absorption; TreeSHAP descriptive component analysis; deterministic LIME local panel.
- Authoritative sources: `configs/stage23/protocol.json`, `scripts/stage23_shortcut_feature_audit_kaggle.py`, Stage23 protocol lock, uncertainty and closure artifacts, Stage13 integration document.
- Results needed: `E29-008`, `E29-015`, `E29-022`, `E29-023`; `C23-001`–`C23-008`; `F23-01`; `T29-S05`–`T29-S11`.
- Boundary: ablation/attribution establish sensitivity; they do not prove leakage, causality, or transfer mechanism.

## 4.4 Bidirectional cross-dataset transfer

- Question: directional ranking transfer under frozen semantic bridges.
- Populations: IDS2018→CICIDS2017 and CICIDS2017→IDS2018 February 28.
- Methods: bridge62 primary; bridge70 published/corrected sensitivity; source-only fitting; direction-specific source validation thresholds; no target adaptation; paired uncertainty inherited from frozen artifacts; cancelled `GROUNDED_S4` cells.
- Authoritative sources: `configs/stage24/protocol.json`, `scripts/stage24/stage24_cross_dataset_generalization.py`, executed Stage24 notebook, semantic bridge spec, final synthesis JSON, publication tables.
- Results needed: `E29-024`–`E29-027`; `C24-001`–`C24-012`; `F24-01`–`F24-02`; `T29-04`, `T29-S12`–`T29-S14`.
- Boundary: directions cannot be averaged; bridge and preprocessing restrict scope; cancelled cells have no results.

## 4.5 Prevalence and operational stress

- Question: how frozen rates translate under lower assumed prevalence and workload/cost scenarios.
- Population: inherited Stage22/Stage24 operating-point scalars; analytic prior-shift grid.
- Methods: hold TPR/FPR fixed; vary prior; calculate PPV/NPV, alerts, analyst hours, capacity, and relative-cost preference.
- Authoritative sources: `configs/stage25/protocol.json`, `scripts/stage25/stage25_prevalence_operational_stress.py`, `docs/STAGE25_MANUSCRIPT_INTEGRATION.md`, `docs/STAGE25_PUBLICATION_TABLES.md`.
- Results needed: `E29-028`–`E29-031`; `C25-001`–`C25-005`; `F25-01`; `T29-05`, `T29-S15`–`T29-S18`.
- Boundary: deterministic projections, not observed SOC outcomes; fixed-rate, traffic, service-time, capacity, and cost assumptions.

## 4.6 Deployment profiling

- Question: computational feasibility at the measured prepared-input-to-probability boundary.
- Population: compatible frozen model paths on recorded Stage26 environments.
- Methods: warm/cold latency, throughput, memory, artifact size, component timing, batch schedules, CPU/GPU matched rows; preserve unsupported statuses.
- Authoritative sources: `configs/stage26/protocol.json`, `scripts/stage26/stage26_deployment_profiling_kaggle.py`, `docs/STAGE26_MANUSCRIPT_INTEGRATION.md`, Stage26 native publication tables.
- Results needed: `E29-032`, `E29-033`; `C26-001`–`C26-005`; `F26-01`; `T29-S19`–`T29-S24`, `T29-M02`.
- Boundary: hardware/software/batch/component-specific; excludes capture, extraction, alert aggregation, analyst response; unsupported paths are not poor performers.

## 4.7 LOAO unseen-family evaluation

- Question: ranking and frozen-threshold behavior with zero held-out-family train/validation exposure.
- Population: eligible family folds and temporally matched benign targets.
- Methods: frozen seven-family taxonomy; day-atomic `TRAIN < VALIDATION < TARGET`; support gate; XGBoost/LightGBM; known-family validation thresholds; ranking/operating metrics separate; 2,000-replicate frozen bootstrap inherited from Stage27.
- Authoritative sources: `configs/stage27/protocol.json`, `notebooks/archive/stage27_loao_unseen_attack_executed.ipynb`, `scripts/stage27/stage27_loao_unseen_attack.py`, fold receipts, threshold receipt, final metrics.
- Results needed: `E29-034`–`E29-036`; `C27-001`–`C27-005`; `F27-01`–`F27-02`; `T29-06`, `T29-S25`, `T29-S27`.
- Boundary: five eligible families only; DOS/AUTH_BRUTE_FORCE ineligible; Infiltration descriptive at 36 positives; no universal zero-day claim.

## 4.8 Seed and control stability

- Question: whether central temporal and family conclusions depend on one realization.
- Population: Stage22 shared holdout and Stage27 family folds under frozen seeds.
- Methods: seeds 42, 43, 44, 45, 46; fixed recipe; no full HPO repetition; no best-seed selection; random LOAO control; separate seed spread from bootstrap intervals; shared historical holdout.
- Authoritative sources: `configs/stage28/protocol.json`, Stage28 seed spec, component execution manifest, seed summaries, closure receipt, final synthesis manuscript results.
- Results needed: `E29-037`–`E29-041`; `C28-001`–`C28-005`; `T29-03`, `T29-06`, `T29-S26`, `T29-S27`.
- Boundary: five-seed ordering is descriptive; no population guarantee/significance test; controls do not isolate one causal mechanism.

## 4.9 Statistical uncertainty and anti-adaptation controls

- State each uncertainty type: historical paired class-stratified bootstrap, frozen paired transfer intervals, deterministic analytic translation, and training-seed variation.
- Keep bootstrap and seed uncertainty separate.
- Explain interval interpretation: zero-containing intervals do not prove equivalence; exclusion does not broaden the population.
- Document frozen target openings, no target-driven fitting/feature search/calibration/threshold reselection, cancelled cells, and closed targets.
- Authoritative sources: `docs/reproducibility/MANUSCRIPT_CRITICAL_TRACEABILITY.csv`, `docs/reproducibility/FINAL_REPRODUCIBILITY_AUDIT.md`, `docs/reproducibility/STAGE_REPRODUCIBILITY_STATUS.csv`, all stage protocol locks.

## 4.10 Reproducibility and provenance

- Define source states: raw-exact, published, corrected, source-faithful, reconstructed.
- Describe config, canonical code/notebook, result, hash, equivalence, and manuscript traceability chain.
- Separate static verification from full rerun reproducibility.
- Identify external datasets, unavailable models/arrays, unproven environments, closed targets, and Stage28 final-wall status.
- Cross-reference `MANUSCRIPT_SOURCE_MAP.csv`, `source_artifact_registry.csv`, `EQUIVALENCE_MATRIX.csv`, `STAGE_REPRODUCIBILITY_STATUS.csv`, and the final audit.

## Section 4 writing constraints

- Never call K79 S4, session, endpoint, source-IP, or five-tuple independent.
- Never combine incompatible populations or metrics.
- Preserve PR-AUC/ROC-AUC versus threshold metrics.
- Preserve cancelled, unsupported, descriptive-only, and supplement-only outcomes.
- Do not claim target adaptation or fresh blind holdout where absent.
- Do not run or authorize training, inference, target opening, threshold search, or resampling during Methods drafting.
