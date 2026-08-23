# Beyond Benchmark Scores: A Multi-Axis Validation Framework for Intrusion Detection

> **Manuscript status:** Pass 2B evidence-governed submission candidate. Scientific results remain frozen at Stage28; Stage29 and later passes provide synthesis, literature verification, editorial integration, and static audit only.

## Abstract

Processed intrusion-detection benchmarks support controlled model comparison but do not establish that performance persists under temporal separation, feature perturbation, domain transfer, rare-event prevalence, deployment constraints, or attacks withheld from development. We present a multi-axis validation framework that evaluates these questions separately while preserving native metrics, frozen operating rules, and claim-to-artifact provenance. On the processed CSE-CIC-IDS2018 reference condition, the selected balanced tree ensemble achieved F1 0.9285 and PR-AUC 0.9776. On a shared forward target, mean PR-AUC across five frozen seeds was 0.2599 after random-natural development and 0.6388 after chronological-natural development, yet frozen thresholds transferred poorly and controls did not isolate chronology as the sole mechanism. Cross-dataset ranking was directional: IDS2018-to-CICIDS2017 transfer reached PR-AUC 0.667483, whereas the reciprocal bridge reached 0.108176. The evidence did not uniformly deteriorate under stronger validation. Several eligible attack families retained stable discrimination, while other outcomes depended on learner or support. Operational projections supplied a different qualification: at 0.1% assumed attack prevalence, high projected PPV could coexist with 33.5 analyst-hours per day, whereas little workload could reflect negligible detection yield. Benchmark discrimination and validated capability are therefore related but non-equivalent claims. Evaluation should report validity axes, ranking and operating-point behavior, deployment assumptions, counterexamples, and provenance separately. Conclusions remain conditional on two related benchmark families, frozen feature bridges and seeds, projected operational assumptions, eligible attack families, and one measured hardware environment.

## 1. Introduction

Machine-learning intrusion detection is commonly summarized by predictive metrics on a benchmark test set [@ring2019survey; @sommer2010closed]. These metrics answer a useful but bounded question: under a specified representation, split, learner, and operating rule, how well does a fitted system distinguish the benchmark labels? Inferring that the same capability persists in later traffic, another collection pipeline, a rare-event population, or an attack family absent during development requires evidence under those conditions [@arp2022dos]. Benchmark performance and validated capability are therefore related, not interchangeable.

The gap arises through several distinct mechanisms. Random partitions can mix temporal regimes or attack-family composition that forward evaluation separates [@pendlebury2019tesseract; @arp2022dos]. Dataset or extraction artifacts can support discrimination without transporting to a new domain [@engelen2021troubleshooting]. Cross-dataset comparisons require defensible shared semantics rather than matching column names [@dhooge2020interdataset; @layeghy2023crossdomain]. Ranking metrics describe score ordering, whereas precision, recall, and false-positive rate describe a selected operating point [@saito2015precision]. At low attack prevalence, that point can yield sharply different precision and analyst workload [@axelsson2000baserate; @layman2023falsealarms]. Computational feasibility is specific to the measured inference path and hardware [@mattson2020mlperf], and attacks withheld from training remain conditional on the family, support, threshold, and unknown-class protocol [@zoppi2023unknown; @shin2023openset].

These problems should not be collapsed into a single degradation or robustness score. Temporal transfer, shortcut sensitivity, cross-dataset portability, operational utility, computational feasibility, and unseen-family behavior use different populations and native quantities. A ranking can remain informative while its frozen threshold fails; transfer can be substantial in one dataset direction and near baseline in the reverse; and high projected positive predictive value (PPV) can coincide with excessive workload. A connected evaluation must preserve such tensions rather than edit them into one success or failure narrative.

We reconstruct that evaluation around CSE-CIC-IDS2018 and CICIDS2017. A conventional processed-data reference is followed by source-faithful temporal contrasts, controlled shortcut-feature perturbations, bidirectional semantic bridges, prior-shift and workload projections, hardware-specific profiling, leave-one-attack-family-out (LOAO) evaluation, and frozen seed and control analyses. Target-facing decisions were locked before their corresponding evaluations. Claims are reported in their native metrics and linked to populations, source artifacts, configurations, code, and provenance records.

The evidence is heterogeneous. The reference result is strong, and chronological development retains substantially better forward ranking than random development across the evaluated seeds, but transferred operating thresholds remain poor. The forward cross-dataset bridge retains ranking signal while the reverse bridge does not. Shortcut interventions show split interactions, yet matched placebos prevent a causal leakage claim. Several withheld families remain discriminable, whereas others are learner-dependent, ineligible, or weakly supported. High projected PPV and manageable analyst workload also fail to align uniformly. These counterexamples identify which inference changes under each validity condition.

This study makes six contributions:

1. It applies a connected, validation-safe framework in which benchmark, temporal, shortcut, cross-dataset, operational, computational, unseen-family, and realization validity remain distinct axes.
2. It provides a source-faithful temporal and operating-point audit across a frozen seed set, separating ranking stability, threshold transfer, and causal interpretation.
3. It combines controlled shortcut-feature evaluation with bidirectional dataset transfer while preserving placebo evidence, bridge restrictions, directionality, and cancelled analyses.
4. It links prevalence, alert workload, relative cost, and measured computational profiles while distinguishing analytic assumptions from hardware measurements.
5. It evaluates zero-training-exposure attack families through eligibility-gated, family-specific results that retain learner dependence and low-support classifications.
6. It supplies a claim-to-provenance layer linking manuscript statements and numbers to frozen artifacts, protocols, canonical implementations, archived sources, equivalence evidence, and known gaps.

The contribution is an evaluation discipline, not a new IDS architecture or a universal verdict on machine-learning detection. The study asks which benchmark capabilities survived each evaluated validity condition, which became conditional, and what remained unresolved.

## 2. Related Work

### 2.1 Benchmark and temporal validity

CICIDS-family releases provide documented, flow-derived data for machine-learning IDS evaluation [@sharafaldin2018toward; @cse_cic_ids2018_official; @cicids2017_official]. Their usefulness does not make a processed or rebalanced sample representative of a deployment population: performance remains conditional on construction, representation, class balance, and evaluation protocol [@ring2019survey; @he2009imbalanced; @sommer2010closed]. The present study therefore retains its processed CSE-CIC-IDS2018 result as a reference condition and evaluates other validity questions on separately governed populations.

Random partitioning can also obscure collection artifacts, near-duplicate structure, and temporal or family dependencies [@engelen2021troubleshooting; @arp2022dos]. Time-consistent security evaluation better matches a future-use direction but can simultaneously alter prevalence and class composition [@pendlebury2019tesseract]. A temporal contrast is consequently evidence about the chosen validation geometry, not by itself proof of concept drift.

### 2.2 Shortcut and explanation validity

Dataset identifiers, flawed extraction fields, and collection artifacts can be predictive without encoding transportable attack behavior [@engelen2021troubleshooting; @arp2022dos]. Removing a feature establishes sensitivity to that intervention; it does not establish leakage or a causal explanation for transfer failure. Placebos and composition controls are therefore essential to the interpretation here.

Explanation methods add a separate validity question. LIME fits a local surrogate [@ribeiro2016lime], while SHAP defines additive feature attributions and TreeSHAP supplies tree-specific algorithms [@lundberg2017shap; @lundberg2020trees]. Stability, decision agreement, and fidelity are different properties [@yeh2019infidelity]. The manuscript retains that distinction rather than using repeatability as a proxy for faithful local reconstruction.

### 2.3 Cross-domain and operational evaluation

Cross-dataset studies show that IDS performance depends on dataset pairing, shared representation, and source-to-target direction [@dhooge2020interdataset; @layeghy2023crossdomain; @cantone2024crossdataset]. This motivates separate bidirectional semantic bridges instead of one pooled portability score.

Operational interpretation is constrained by the base-rate problem: sensitivity and specificity do not determine positive predictive value or false-alert burden when attacks are rare [@axelsson2000baserate]. Prior-probability-shift analysis further assumes stable class-conditional behavior [@saerens2002prior], while controlled alarm studies show that false-alarm rate can affect analyst precision and time on task [@layman2023falsealarms]. The present workload and cost quantities are therefore scenario projections, not measured field outcomes.

### 2.4 Computational, unknown-family, and reproducibility scope

Computational feasibility depends on the inference path, batch, software, and hardware [@mattson2020mlperf]; constrained-device IDS demonstrations also show why feature-extraction and model-execution boundaries must be explicit [@mirsky2018kitsune]. Open-set recognition formalizes test-time unknown classes [@scheirer2013openset], and IDS studies have evaluated attacks withheld from development under study-specific protocols [@zoppi2023unknown; @shin2023openset]. Such results depend on eligibility, support, metric, and threshold and do not establish arbitrary future-attack detection.

Reproducibility programs emphasize code, experimental detail, and independent regeneration [@pineau2021reproducibility], while adaptive-analysis results show that repeated holdout feedback can weaken ordinary guarantees [@dwork2015holdout]. Our contribution is not priority over these practices; it is their study-specific integration through frozen protocols, target-opening records, equivalence receipts, and claim-level provenance, with unresolved rerun gaps kept explicit.

## 3. Datasets and Provenance

### 3.1 CSE-CIC-IDS2018 roles

CSE-CIC-IDS2018 serves two non-equivalent roles [@cse_cic_ids2018_official; @sharafaldin2018toward]. The conventional reference uses the original processed, rebalanced binary table, with frozen memberships of 192,593 training, 48,149 validation, and 60,186 holdout rows. It supports controlled model and operating-point selection but is not a natural-prevalence, session-independent, or forward population.

Temporal analyses instead use source-faithful dated exports and separately governed memberships. Here, source-faithful means that authenticated columns, cleaning rules, and temporal roles were recovered from the research lineage; it does not imply raw-packet availability or complete reconstruction of every historical environment. The shared forward target preserves collection order and is scientifically distinct from the processed holdout. High reference discrimination is therefore not relabeled as temporal evidence, and the source-faithful analysis does not make the processed reference naturalistic.

### 3.2 CICIDS2017 and semantic bridges

CICIDS2017 supplies a second benchmark domain, selected packet/flow provenance, and the family/day chronology used for LOAO evaluation [@cicids2017_official; @sharafaldin2018toward]. The primary forward bridge trains on IDS2018 and evaluates 2,830,743 effective CICIDS2017 rows; the reverse bridge trains under the frozen CICIDS2017 source protocol and evaluates the IDS2018 February 28 target. The directions are not averaged because their learners, prevalence, representations, and target roles differ.

Cross-dataset comparability follows frozen semantic contracts. Bridge62 contains the defensible shared predictors. Bridge70 adds aggregate-flag fields and retains both the published serialization and a preregistered correction. The correction changes an identified representation dependency; it is not selected after target performance. Two planned `GROUNDED_S4` cells were cancelled before target opening because exact durable physical-row membership could not be reconstructed without a new heuristic. They were neither approximated nor replaced.

### 3.3 Attack-family populations

Known categories in the processed reference holdout describe error concentration, not novelty. LOAO evaluation instead requires zero exposure to the target family in training and validation, a day-atomic `TRAIN < VALIDATION < TARGET` ordering, and sufficient target support. DDoS, Port Scan, Web Attack, Bot, and Infiltration were eligible. DOS and AUTH_BRUTE_FORCE were structurally ineligible, while Infiltration remained descriptive because its target contained 36 positives. The primary family target pairs the withheld family with temporally matched benign traffic; a context target that includes known attacks remains secondary.

### 3.4 Provenance and target governance

Provenance labels retain narrow meanings. **Raw-exact** denotes preserved source bytes; **published** denotes released artifact semantics; **corrected** denotes a frozen documented correction; **source-faithful** denotes a derived representation following authenticated semantics and locked cleaning; and **reconstructed** denotes recovery from surviving lineage evidence without claiming byte identity. Detailed parser investigations, transport receipts, storage events, and failed mechanism searches are routed to the supplement or repository unless needed to interpret a main result.

Development data support fitting, validation selection, and protocol checks only within declared roles. Target-facing model scope, features, thresholds, and cleaning were frozen before the corresponding target result. No target-guided fitting, feature search, calibration, or threshold reselection occurred. Some targets were historically opened and later reused for preregistered stability analysis; they are not presented as fresh blind holdouts. Current validation-safe interfaces verify identities, schemas, values, and receipts without opening scientific targets or deserializing models.

## 4. Validation Framework and Methods

### 4.1 Reference evaluation

The reference question is conventional within-table discrimination on the processed CSE-CIC-IDS2018 binary data. Stratified training, validation, and holdout memberships are frozen and disjoint. Scaling is fitted on training data only for historically scaled learners; tree boosting retains its recorded preprocessing. Validation narrows the baseline inventory to XGBoost and LightGBM and selects a balanced XGBoost threshold of 0.51 and a recall-oriented LightGBM threshold of 0.26. The holdout cannot revise either decision. ROC-AUC and PR-AUC report ranking; F1, F2, precision, recall, false-positive rate (FPR), and error counts report operating behavior. Historical paired, class-stratified analyses describe conditional uncertainty on the same holdout. This axis does not estimate natural prevalence, temporal validity, domain transfer, or deployment utility.

### 4.2 Temporal validation

Temporal validation asks whether development geometry changes ranking and threshold transfer on one common forward IDS2018 target. Four cells cross random or chronological membership with natural or training-only rebalanced prevalence. The target contains 1,374,133 rows: 375,345 attack and 998,788 benign. The tree-ensemble recipe, cleaning, memberships, and operating points are frozen; rebalancing applies only to training.

PR-AUC and ROC-AUC describe ranking, while frozen-threshold precision, recall, F1, and FPR describe operating transfer. The stability layer repeats the designated random-natural and chronological-natural cells over five frozen seeds and reports means, standard deviations, and directional counts without best-seed selection. Family-aware controls test whether chronology alone explains the contrast. The result is conditional on the recovered chronology and finite seed set; it is not a significance test, a session-independence guarantee, or a causal estimate of drift.

### 4.3 Shortcut-feature and explanation audit

The shortcut audit removes seven preregistered identity-, protocol-, window-, or behavior-related subsets from the frozen random-natural and chronological-natural populations across the frozen tree learners. Matched-size placebos, depth-one controls, feature-importance redistribution, behavior-restricted inputs, and family-composition tables test competing interpretations. PR-AUC and ROC-AUC are primary; operating-point results and conditional paired intervals retain their frozen roles. No subset is selected from target performance.

Component TreeSHAP summaries are descriptive proxies for the averaged-probability ensemble. A deterministic local panel separately evaluates LIME decision agreement, surrogate fidelity, perturbation stability, and top-feature agreement with exact TreeSHAP. The audit establishes representation and split sensitivity; it cannot identify a feature as leakage or a cause of cross-domain failure.

### 4.4 Cross-dataset transfer

Cross-dataset evaluation fits separate source models for IDS2018-to-CICIDS2017 and CICIDS2017-to-IDS2018 transfer. Bridge62 is primary; bridge70 is a preregistered serialization sensitivity. Source training, validation thresholds, feature contracts, and target cleaning are direction-specific and frozen independently of target results. Target labels do not guide fitting, feature selection, calibration, or thresholding.

Direction-specific PR-AUC and ROC-AUC describe ranking; frozen-threshold metrics describe operating transfer; Brier score accompanies the aggregate-flag sensitivity. Published-versus-corrected paired intervals are conditional on the target and frozen implementation. Cancelled `GROUNDED_S4` cells remain absent. The axis supports bridge- and direction-specific conclusions for two related benchmark families, not portability to arbitrary datasets or a unique transfer mechanism.

### 4.5 Prevalence and operational stress

Operational stress translates inherited temporal and cross-dataset operating points without fitting or target access. Under prior-probability shift, sensitivity and specificity remain fixed while prevalence varies on a preregistered grid. PPV and negative predictive value follow from those rates and the assumed prior. Frozen traffic, analyst service time, capacity, and relative error weights produce alert, workload, capacity, and cost scenarios.

These outputs are conditional projections. Their uncertainty is inherited from the operating points and assumptions; no new bootstrap is added. They show how a fixed operating point behaves under stated prevalence and resource scenarios, not how it would behave under simultaneous covariate, protocol, topology, user, or attacker shift.

### 4.6 Deployment profiling

Profiling asks which frozen, compatible model paths are computationally feasible on the recorded hardware and software. The timed boundary begins with prepared model input and ends with materialized probabilities. Eligible tree, ensemble, and packet-image paths use frozen warm-inference, cold-start, throughput, memory, package-size, component, batch, and CPU/GPU schedules. Different representations remain separate, and unavailable, incompatible, timed-out, or resource-limited paths remain statuses rather than imputed timings.

Latency percentiles, throughput, memory, and size retain native units; CPU/GPU ratios are descriptive point estimates. No batch is retrospectively chosen as optimal. The measurements exclude capture, flow extraction, external representation construction, alert aggregation, and analyst response and do not define hardware-independent constants.

### 4.7 Leave-one-attack-family-out evaluation

LOAO evaluation asks whether XGBoost or LightGBM, with zero training and validation exposure to an eligible family, can rank that family above temporally matched benign traffic and detect it at frozen operating points. Family aliases, chronology, memberships, features, fits, and validation thresholds are fixed before target evaluation. DOS and AUTH_BRUTE_FORCE are ineligible; Infiltration is descriptive at support 36.

ROC-AUC and PR-AUC report ranking relative to chance and target prevalence. Recall and related metrics at standard, balanced, and security thresholds report operating transfer. Family-specific conditional intervals and support accompany the results, and behavioral-similarity analysis remains descriptive. This benchmark-family withholding design does not establish arbitrary future-attack detection or authorize a pooled novelty score.

### 4.8 Seed and control stability

The stability program tests whether the central temporal ordering and eligible-family conclusions depend on one training realization. A frozen seed registry repeats designated temporal and LOAO cells without repeating the full historical hyperparameter search or selecting the best seed. Random-split LOAO is a control for chronology-related difficulty, not a deployment estimate. Seed-level PR-AUC, ROC-AUC, and operating outcomes are summarized separately from bootstrap uncertainty. Stability over five frozen seeds strengthens fixed-recipe conclusions within scope but supplies neither a population guarantee nor one causal account.

### 4.9 Uncertainty, anti-adaptation, and reproducibility

Paired historical resampling keeps compared learners or representations on the same class-stratified draw. Each contrast retains its declared uncertainty type. An interval containing zero is not evidence of equivalence; an interval excluding zero does not broaden the population. Training-seed variation is not combined with bootstrap distributions, and unlike metrics are not normalized into a composite score.

At each boundary, model families, hyperparameters, subsets, bridges, operating points, targets, and eligible families are frozen before the corresponding result. Later target evidence cannot retune an earlier protocol, and cancelled analyses remain cancelled. Manuscript claims and numbers map to Stage29 claim, evidence, number, source-artifact, limitation, and exhibit registries. The repository verifies source identities, configurations, schemas, scalar values, hashes, toy formulas, and approved read-only equivalence checks. It does not claim complete end-to-end reruns where raw data, historical environments, models, arrays, or closed targets are unavailable.
