# A Multi-Axis Validation Framework for Machine-Learning Intrusion Detection

> **Manuscript status:** Pass 2B evidence-governed submission candidate. Scientific results remain frozen at Stage28; Stage29 and later passes provide synthesis, literature verification, editorial integration, and static audit only.

## Abstract

Processed intrusion-detection benchmarks support controlled model comparison, but they do not establish capability across time, feature perturbations, datasets, rare-event prevalence, deployment constraints, or attacks withheld from development. We present a multi-axis framework that evaluates these validity questions separately while preserving native metrics, frozen operating rules, and claim-to-artifact provenance. On one shared forward target, mean PR-AUC across five registered seeds was 0.2599 after random-natural development and 0.6388 after chronological-natural development; the ordering held in all five realizations, although frozen thresholds transferred poorly and controls did not identify chronology as the sole mechanism. The processed CSE-CIC-IDS2018 reference condition provides a contrast: the selected balanced tree ensemble achieved F1 0.9285 and PR-AUC 0.9776. Cross-dataset ranking was directional, with IDS2018-to-CICIDS2017 PR-AUC 0.667483 and reciprocal PR-AUC 0.108176. At 0.1% assumed attack prevalence, one high-PPV projection required 33.5 analyst-hours per day, while a low-workload projection reflected negligible detection yield. Not every result deteriorated under stronger validation: several eligible attack families retained stable discrimination, whereas other outcomes depended on learner or support. Stronger validation instead narrowed the claims that the evidence could support. The conclusions remain conditional on two related benchmark families, frozen feature bridges and realizations, analytic operational assumptions, eligible attack families, and one measured hardware environment.

## 1. Introduction

Machine-learning intrusion detection is commonly summarized by predictive metrics on a benchmark test set [@ring2019survey; @sommer2010closed]. These metrics answer a useful but bounded question: under a specified representation, split, learner, and operating rule, how well does a fitted system distinguish the benchmark labels? Inferring that the same capability persists in later traffic, another collection pipeline, a rare-event population, or an attack family absent during development requires evidence under those conditions [@arp2022dos]. Benchmark performance and validated capability are therefore related, not interchangeable.

The gap arises through several distinct mechanisms. Random partitions can mix temporal regimes or attack-family composition that forward evaluation separates [@pendlebury2019tesseract; @arp2022dos]. Dataset or extraction artifacts can support discrimination without transporting to a new domain [@engelen2021troubleshooting]. Cross-dataset comparisons require defensible shared semantics rather than matching column names [@dhooge2020interdataset; @layeghy2023crossdomain]. Ranking metrics describe score ordering, whereas precision, recall, and false-positive rate describe a selected operating point [@saito2015precision]. At low attack prevalence, that point can yield sharply different precision and analyst workload [@axelsson2000baserate; @layman2023falsealarms]. Computational feasibility is specific to the measured inference path and hardware [@mattson2020mlperf], and attacks withheld from training remain conditional on the family, support, threshold, and unknown-class protocol [@zoppi2023unknown; @shin2023openset].

These problems should not be collapsed into a single degradation or robustness score. Temporal transfer, shortcut sensitivity, cross-dataset portability, operational utility, computational feasibility, and unseen-family behavior use different populations and native quantities. A ranking can remain informative while its frozen threshold fails; transfer can be substantial in one dataset direction and near baseline in the reverse; and high projected positive predictive value (PPV) can coincide with excessive workload. A connected evaluation must preserve such tensions rather than edit them into one success or failure narrative.

We reconstruct that evaluation around CSE-CIC-IDS2018 and CICIDS2017. A conventional processed-data reference is followed by source-faithful temporal contrasts, controlled shortcut-feature perturbations, bidirectional semantic bridges, prior-shift and workload projections, hardware-specific profiling, leave-one-attack-family-out (LOAO) evaluation, and frozen seed and control analyses. Target-facing decisions were locked before their corresponding evaluations. Claims are reported in their native metrics and linked to populations, source artifacts, configurations, code, and provenance records.

The evidence is heterogeneous. The reference result is strong, and chronological development retains substantially better forward ranking than random development across the evaluated seeds, but transferred operating thresholds remain poor. The forward cross-dataset bridge retains ranking signal while the reverse bridge does not. Shortcut interventions show split interactions, yet matched placebos prevent a causal leakage claim. Several withheld families remain discriminable, whereas others are learner-dependent, ineligible, or weakly supported. High projected PPV and manageable analyst workload also fail to align uniformly. These counterexamples identify which inference changes under each validity condition.

This study makes four contributions:

1. It applies a connected framework that evaluates temporal validity, operating-point behavior, shortcut sensitivity, bidirectional cross-dataset transfer, prevalence stress, deployment profiling, unseen-family behavior, and realization stability as distinct axes with native metrics.
2. It supplies a claim-to-provenance layer that traces manuscript statements and numbers to frozen evidence, protocols, artifacts, canonical source material, and explicitly classified reproducibility limits.
3. It shows that benchmark capability did not translate uniformly across stronger validation conditions. The observed effects varied across time, datasets, operating points, feature controls, families, learners, development regimes, and operational assumptions.
4. It distills the framework into an eight-item validation checklist that links each evaluation question to a native metric, a required control, and an interpretation boundary.

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

Recovered temporal provenance showed that the inherited membership was unsafe for temporal-window evaluation. Temporal analyses therefore use source-faithful dated exports and separately governed memberships. Here, source-faithful means that authenticated columns, cleaning rules, and temporal roles were recovered from the research lineage; it does not imply raw-packet availability or complete reconstruction of every historical environment. The shared forward target preserves collection order and is scientifically distinct from the processed holdout. High reference discrimination is not relabeled as temporal evidence, and the source-faithful analysis does not make the processed reference naturalistic.

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

## 5. Results

### 5.1 How strong was the conventional reference?

The processed reference condition produced strong within-table discrimination (Table 1). At the validation-selected balanced point, XGBoost achieved holdout F1 0.9285, FPR 0.0061, ROC-AUC 0.9802, and PR-AUC 0.9776. The LightGBM security point achieved F1 0.9178, F2 0.9112, FPR 0.0466, ROC-AUC 0.9802, and PR-AUC 0.9777. These values define the reference against which the remaining validation questions are interpreted.

Neither learner was declared the overall winner. The frozen balanced XGBoost-minus-LightGBM F1 difference was 0.000185, with a conditional interval from -0.000495 to 0.000862. At the security points, LightGBM missed 33 fewer attacks, with the paired conditional difference spanning 2 to 64 fewer misses. Brier scores were 0.04277 for XGBoost and 0.04275 for LightGBM, and the retained calibration-difference intervals included zero.

**Table 1. Conventional processed-reference holdout results.** Thresholds were selected on validation data. F1 and F2 are threshold-specific harmonic means; FPR is false-positive rate; ROC-AUC and PR-AUC are threshold-free ranking metrics. Dashes denote a metric not selected for this compact comparison.

| Operating role | Learner | Threshold | F1 | F2 | FPR | ROC-AUC | PR-AUC |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Balanced | XGBoost | 0.51 | 0.9285 | — | 0.0061 | 0.9802 | 0.9776 |
| Security | LightGBM | 0.26 | 0.9178 | 0.9112 | 0.0466 | 0.9802 | 0.9777 |

### 5.2 Did temporal development change forward validity?

On the common forward target, chronological-natural development ranked higher than random-natural development across all frozen seeds (Figure 1; Table 2). Random-natural models had mean ROC-AUC 0.5176 (SD 0.0073) and PR-AUC 0.2599 (SD 0.0034); chronological-natural models had mean ROC-AUC 0.8209 (SD 0.0085) and PR-AUC 0.6388 (SD 0.0322). Both metric orderings held in 5/5 seeds.

Threshold transfer contradicted a simple ranking narrative. Chronological thresholds almost never fired on the common target, whereas the two random security points reached final FPR values of 0.2870 and 0.2685, far above the development constraint. Family-aware controls were mixed across family and learner, so the result does not isolate chronology as the sole mechanism.

**Figure 1. Temporal ranking transfer on the shared forward IDS2018 target.** Existing panels report (a) [PR-AUC](../figures/stage22r_temporal_validation/fig22r_1_validation_to_final_pr_auc.png) and (b) [ROC-AUC](../figures/stage22r_temporal_validation/fig22r_2_validation_to_final_roc_auc.png) for frozen random and chronological development geometries. Stage28 seed summaries establish a 5/5 descriptive ordering, not a significance test; the target was historically opened, thresholds are evaluated separately, and chronology remains entangled with family composition.

**Table 2. Five-seed temporal stability on the shared forward target.** SD is training-seed standard deviation under the frozen recipe; the directional count is descriptive over the five registered seeds.

| Development geometry | Mean ROC-AUC | ROC-AUC SD | Mean PR-AUC | PR-AUC SD | Directional result |
| --- | ---: | ---: | ---: | ---: | --- |
| Random-natural | 0.5176 | 0.0073 | 0.2599 | 0.0034 | Lower than chronological in 5/5 seeds for both metrics |
| Chronological-natural | 0.8209 | 0.0085 | 0.6388 | 0.0322 | Higher than random in 5/5 seeds for both metrics |

### 5.3 Were shortcut and explanation conclusions stable?

Shortcut-subset effects varied by development geometry and learner (Figure 2). The behavior-restricted representation retained strong random-split discrimination but not the chronological result, and family composition was narrower in the chronological population. Matched-size placebo removals also produced non-zero split interactions, including frozen conditional intervals excluding zero. The observed interactions therefore establish feature-set sensitivity without identifying a named feature as leakage or a causal source of transfer behavior.

Local explanations supplied a related counterexample. LIME rankings were comparatively stable across perturbation seeds, but only 2 of 64 explanations met all prespecified fidelity and cross-method criteria, and 31 of 64 failed to reproduce the model's local classification decision. Mean SHAP-LIME top-10 Jaccard agreement was 0.304 for XGBoost and 0.360 for LightGBM. Stable explanations were not necessarily faithful explanations.

**Figure 2. Shortcut-subset sensitivity by validation geometry.** The [approved Stage23 asset](../results/stage23_shortcut_feature_audit/stage23_7_final_synthesis/figures/figure_23_a_subset_split_interaction.png) reports native ranking behavior across seven frozen feature subsets, random-natural and chronological-natural splits, and the evaluated tree learners. Conditional subset effects do not identify leakage or a transfer mechanism; matched-size placebo interactions remain part of the interpretation.

### 5.4 Was cross-dataset transfer symmetric?

Bridge62 transfer was strongly directional (Figure 3; Table 3). IDS2018-to-CICIDS2017 evaluation achieved PR-AUC 0.667483 and ROC-AUC 0.733946 on 2,830,743 effective target rows. In the reciprocal direction, target attack prevalence was 0.104847, PR-AUC was 0.108176, and ROC-AUC was 0.525167. The reverse PR-AUC was therefore close to its prevalence anchor, while the forward bridge retained substantial ranking signal.

A larger bridge did not yield one metric direction. Correcting aggregate-flag serialization in bridge70 changed PR-AUC by -0.007729, ROC-AUC by +0.002192, and Brier score by +0.005087; the frozen paired intervals excluded zero. The two `GROUNDED_S4` cells remained cancelled because exact membership was unavailable. Neither the metric-specific sensitivity nor the missing cells are hidden by averaging the directions.

**Figure 3. Bidirectional cross-dataset ranking under bridge62.** Existing panels report (a) [normalized PR-AUC](../figures/stage24_cross_dataset/fig24_1_normalized_pr_auc_directionality.svg) and (b) [ROC-AUC](../figures/stage24_cross_dataset/fig24_2_roc_auc_directionality.svg). Each point uses its frozen direction-specific source learner, target population, prevalence, and semantic feature contract; the panels do not define an average transfer score.

**Table 3. Primary bidirectional bridge62 transfer.** PR-AUC is interpreted against each target's attack prevalence; ROC-AUC is the direction-specific ranking metric. Different source and target protocols preclude pooling.

| Direction | Target scope | Target prevalence | PR-AUC | ROC-AUC |
| --- | --- | ---: | ---: | ---: |
| IDS2018 to CICIDS2017 | 2,830,743 effective rows | Target-specific | 0.667483 | 0.733946 |
| CICIDS2017 to IDS2018 | Frozen February 28 target | 0.104847 | 0.108176 | 0.525167 |

### 5.5 Did projected precision imply operational utility?

Projected PPV, workload, and yield did not align uniformly (Figure 4; Table 4). At 0.1% assumed attack prevalence, the Stage22 random STANDARD point retained PPV 0.965572 but required 33.5 analyst-hours per day under the frozen traffic and service-time scenario. The chronological STANDARD point projected PPV 0.000551068 and only 0.0322 true alerts per day: its small workload reflected negligible yield.

Directionality persisted under the same prior-shift translation. Forward STANDARD transfer points projected PPV 0.039233-0.060313, while reverse points projected 0.000257610-0.000287993. Under the frozen 1:100 relative-cost scenario, 15/24 operating points favored the model at 0.1% prevalence and 3/24 at 0.01%. These are analytic projections with fixed sensitivity and FPR, not observations from a security operations center.

**Figure 4. PPV under prevalence stress.** The [approved Stage25 curves](../figures/stage25_prevalence_stress/figure25_a_ppv_cliff.svg) translate frozen true- and false-positive rates across assumed attack prevalence. PPV is positive predictive value. The prior-shift model holds conditional rates fixed; traffic, service time, capacity, and relative costs are scenario assumptions rather than field measurements.

**Table 4. Selected operating-point translations at 0.1% assumed prevalence.** PPV and workload/yield are conditional on the frozen rates, daily traffic, and analyst service-time assumptions; STANDARD denotes the inherited standard operating role.

| Frozen condition | Projected PPV | Operational quantity | Interpretation boundary |
| --- | ---: | --- | --- |
| Stage22 random STANDARD | 0.965572 | 33.5 analyst-hours/day | High PPV does not ensure manageable workload |
| Stage22 chronological STANDARD | 0.000551068 | 0.0322 true alerts/day | Low workload does not ensure useful yield |
| Forward transfer STANDARD range | 0.039233-0.060313 | Direction-specific | Conditional prior-shift projection |
| Reverse transfer STANDARD range | 0.000257610-0.000287993 | Direction-specific | Conditional prior-shift projection |

### 5.6 Was one compute backend consistently faster?

Backend advantage depended on architecture and measurement path (Figure 5). At batch one, the p95 CPU-over-GPU latency ratio was 1.94 for the five-checkpoint soft-voting ensemble and 1.58 for the single-resource reference, indicating a GPU advantage. Ratios of 0.16 for CatBoost and 0.26 for XGBoost indicated a CPU advantage under the same convention. The packet-image CNN ratio was 10.86, while the ViT ratio was 1.05. Unsupported LightGBM GPU execution and unavailable paths remained compatibility statuses rather than timing values.

**Figure 5. Hardware-specific p95 CPU/GPU comparison.** The [approved Stage26 asset](../figures/stage26_deployment_profiling/F26_CPU1_GPU_P95_SPEEDUP.png) compares batch-one p95 latency ratios for compatible prepared-input-to-probability paths on the recorded hardware and software. Values are descriptive point estimates; unsupported backends, capture, flow extraction, alert aggregation, and analyst response are outside the comparison.

### 5.7 Did eligible withheld families behave uniformly?

LOAO results were selective (Figure 6; Table 5). DDoS ranking was strong for XGBoost (ROC-AUC 0.9982; PR-AUC 0.9925) and LightGBM (ROC-AUC 0.9986; PR-AUC 0.9940). Web Attack also retained ranking for XGBoost (ROC-AUC 0.9693; PR-AUC 0.7206) and LightGBM (ROC-AUC 0.9901; PR-AUC 0.7605).

Other families were more conditional. Bot produced XGBoost ROC-AUC 0.3224 and PR-AUC 0.003256 but LightGBM ROC-AUC 0.5591. Port Scan ROC-AUC was 0.5506 for XGBoost and 0.7559 for LightGBM. Infiltration remained descriptive at 36 positives, and DOS and AUTH_BRUTE_FORCE were ineligible rather than model failures. Ranking and frozen-threshold recall could also disagree, so no pooled novelty score was formed.

**Figure 6. Eligible-family ranking and balanced-threshold recall.** Existing panels report (a) [ROC-AUC with frozen conditional intervals](../results/stage27_loao_unseen_attack/stage27_4a_final_synthesis/figures/stage27_primary_roc_auc_ci.png) and (b) [balanced-threshold recall](../results/stage27_loao_unseen_attack/stage27_4a_final_synthesis/figures/stage27_balanced_recall_ci.png) for separate eligible families and learners. Infiltration is descriptive at support 36; ineligible families are absent; the panels do not constitute an aggregate future-attack score.

**Table 5. Frozen conclusion-stability classification for eligible families.** Classifications combine family-specific ranking, frozen-threshold behavior, support, learner contrast, and the five-seed stability rules; they are not pooled metrics.

| Family | Frozen synthesis | Required qualification |
| --- | --- | --- |
| DDoS | Strong ranking for both learners | Eligible benchmark family only |
| Web Attack | Ranking retained for both learners | Magnitude and thresholds remain learner-specific |
| Port Scan | Qualitative conditions retained across seeds | Ranking magnitude is learner-dependent |
| Bot | Learner-dependent | Frozen-threshold detection remains weak |
| Infiltration | Descriptive only | Held-out positive support is 36 |

### 5.8 Did central conclusions survive the frozen realizations?

All 108/108 preregistered new fits in the frozen stability program completed, with 12 artifacts reused as declared and no planned execution outstanding. Completion did not enlarge inferential scope: no best seed was selected, seed variation was not combined with bootstrap uncertainty, and the shared temporal target remained historically opened.

The chronological-over-random ranking direction held in all evaluated seeds. DDoS, Port Scan, and Web Attack met the registered qualitative conditions for both learners; Bot remained learner-dependent and Infiltration descriptive. Random LOAO controls were mixed and family-specific. The controls support an interaction between novelty difficulty and chronology in some comparisons but do not identify one mechanism.

### 5.9 What survived across the validation axes?

Table 6 synthesizes the frozen chain without treating unlike quantities as commensurable. Strong benchmark discrimination, chronological forward ranking, forward bridge signal, selected family transfer, and compatible computational paths survived within their declared scopes. Frozen thresholds, symmetric portability, simple shortcut causality, universal operational preference, and uniform family conclusions did not.

**Table 6. Integrated native-metric validity matrix.** Each row preserves its population, metric family, and interpretation ceiling. The table summarizes frozen evidence and is not a normalized degradation, generalization, or composite performance score.

| Validity axis | Principal observation | What survived | What remained conditional or unsupported | Claim ceiling |
| --- | --- | --- | --- | --- |
| Benchmark/reference | Strong F1 and ranking on the processed split | Within-reference discrimination | Inference to chronology, transfer, or deployment | Processed reference only |
| Duplicate/split | Frozen memberships and target roles were auditable | Explicit role separation | Latent-session independence | Traceable memberships only |
| Temporal | Chronological ranking exceeded random ranking across five seeds | Directional ranking contrast | Threshold transfer and sole mechanism | Evaluated chronology and recipe |
| Shortcut | Subset effects depended on split and learner; placebos interacted | Representation sensitivity | Universal removal benefit or causal leakage | Preregistered subsets and controls |
| Cross-dataset | Forward ranking signal contrasted with near-baseline reverse transfer | Direction-specific forward signal | Symmetry, arbitrary datasets, cancelled cells | Frozen bridges and targets |
| Prevalence/operational | PPV, workload, yield, and cost preference diverged | Assumption-explicit translation | Field performance or universal preference | Frozen prior-shift scenarios |
| Computational | Backend advantage varied by compatible model path | Measured component feasibility | Unsupported paths and end-to-end cost | Recorded hardware/software |
| Unseen family | Several families transferred; others depended on learner or support | Selected eligible-family capability | Uniform future-attack detection | Eligible benchmark families |
| Seed/control | Central directions survived selected seeds; controls were mixed | Finite-realization stability | Population guarantee or one causal account | Frozen seed registry |

## 6. Discussion

### 6.1 Stronger validation changed the claim, not every result

The reference experiment remains a credible answer to a narrow question: selected tree ensembles discriminated the processed holdout labels well under frozen validation choices. Stronger validation did not erase that arithmetic or make benchmark evaluation uninformative. Instead, each axis changed the population, operating rule, representation, or resource assumption to test a broader inference.

The resulting pattern was not monotonic. Chronological development retained substantially stronger forward ranking than random development; the forward semantic bridge retained cross-dataset signal; DDoS and Web Attack remained discriminable when withheld; and compatible model paths were computationally feasible on the measured system. At the same time, frozen thresholds transferred poorly, reverse cross-dataset ranking was near its anchor, and other family outcomes depended on learner or support. Benchmark performance is thus an observed property of one evaluation system. A capability claim must name the additional condition under which it was validated.

### 6.2 Temporal, shortcut, and explanation evidence constrain mechanism claims

The temporal evidence separates ranking from score-scale transfer. Chronological development ranked the shared forward population more effectively in every frozen realization, yet its inherited thresholds almost never fired. This is not evidence that chronological development is universally preferable; it shows that validation geometry can change both ordering and operating behavior. Family-aware controls remain mixed, preventing attribution to chronology or drift alone.

Shortcut controls reinforce that restraint. Named removals altered results, but matched placebos also interacted with split geometry, and chronological family composition differed from random composition. The study can therefore report subset sensitivity without treating a particular field as proven leakage or as the cause of domain transfer. LIME supplies the same methodological lesson at a different level: perturbation rankings could be stable while local decision reconstruction and cross-method fidelity failed. Explanation reports should evaluate fidelity and agreement explicitly rather than equating repeatability with validity.

### 6.3 Transfer is directional and threshold utility is a separate decision

The bidirectional bridge makes dataset portability a source-to-target statement. IDS2018-trained models retained useful ranking on CICIDS2017 under bridge62, while the reciprocal evaluation was close to its target anchor. The directions use different source learners, prevalence, collection periods, and target roles; averaging them would remove the finding. Metric-specific responses to the aggregate-flag correction further show that a larger feature intersection is not automatically a better semantic bridge. The cancelled cells preserve an additional boundary: exact membership governance can leave a planned comparison unestimable.

Ranking and operating utility also diverged across temporal, cross-dataset, and LOAO results. ROC-AUC and PR-AUC integrate score order across thresholds; precision, recall, F1, and FPR describe one selected point. A transported ranking can coexist with an unsuitable threshold when score scale or prevalence changes. Prospective recalibration might be useful, but it would require new governed data and evaluation; target-guided recalibration was not performed here.

### 6.4 Operational projections and compute profiles answer different questions

Prior-shift translation demonstrates that PPV alone does not determine workflow. Under the frozen scenarios, high projected PPV coexisted with analyst demand exceeding one day, while low demand could result from almost no true detections. Relative-cost preference also changed with assumed prevalence. Evaluation protocols should therefore report the rates inherited by the projection, prevalence, traffic, service time, capacity, and error-cost assumptions rather than label an operating point operationally useful in isolation.

Stage26 answers a complementary systems question: can a compatible prepared-input-to-probability path run under a declared environment? CPU/GPU advantage varied by model family, and unsupported paths remained statuses. These measurements neither validate PPV nor cover capture-to-alert latency. Operational analysis and computational profiling belong in the same decision chain but retain separate evidence boundaries.

### 6.5 Withheld-family evidence must remain heterogeneous

Zero exposure during training and validation did not produce one family outcome. DDoS and Web Attack transferred strongly across learners; Port Scan retained qualitative stability but differed in magnitude; Bot was learner-dependent; Infiltration was descriptive; and two families were ineligible. Collapsing these outcomes into one novelty score would hide support, threshold, and learner dependence.

This heterogeneity is informative. Strong family results prevent a universal negative conclusion, while weak and ineligible cases prevent a universal positive one. A withheld benchmark family can share infrastructure, extraction cues, or behavior with known classes and is not equivalent to an arbitrary future exploit. Future IDS evaluations should preregister eligibility, retain family support, report ranking and frozen-threshold behavior separately, and distinguish descriptive from inferential outcomes.

### 6.6 Implications for IDS evaluation

The evidence supports a sequence of claim checks rather than a prescribed architecture. Studies should define the reference population and duplicate or membership handling; test time direction and operating-point transfer; probe plausible shortcuts with controls; evaluate domain transfer in both directions under semantic contracts; translate fixed rates under explicit prevalence and workload assumptions; profile the declared inference boundary; gate unknown-family evaluation by eligibility and support; and examine realization stability without selecting favorable seeds.

The axes remain modular. Temporal evidence cannot substitute for cross-dataset transfer; a feature ablation cannot establish causality; a deployment profile cannot validate PPV; and a withheld-family result cannot establish arbitrary future-attack capability. Choices that can adapt to target evidence should be fixed before evaluation, cancelled analyses should remain visible, and reused targets should not be relabeled as fresh blind holdouts. Claim-level provenance then makes these boundaries auditable without implying that every historical computation is locally rerunnable.

The retained tensions are also a practical reporting device. Benchmark and forward evidence should appear together so a strong reference result is neither discarded nor overextended. Ranking and threshold metrics should be paired because they can support different operational conclusions. Both cross-dataset directions should remain visible because one-way success does not imply reciprocal transportability. Named feature interventions should be reported beside placebo interventions, and explanation stability beside fidelity, to prevent an appealing diagnostic from acquiring causal or reconstructive meaning it has not earned. Likewise, projected PPV should be accompanied by workload and true-alert yield, while family summaries should retain learner and support strata. Presenting these contrasts adjacently makes disagreement interpretable instead of treating it as editorial noise.

This structure also clarifies the role of uncertainty. Conditional resampling, training-seed variation, direction counts, scenario sensitivity, and hardware repetitions arise from different sources and should not be pooled into a common confidence statement. A five-seed ordering can strengthen a fixed-recipe conclusion without becoming a significance test; a paired interval can resolve a within-target contrast without describing external population variation; and a hardware ratio can compare compatible paths without establishing a deployment constant. Reviewers can then evaluate the evidence actually available for each claim rather than infer precision from an unrelated axis.

Finally, the claim-to-artifact layer should be viewed as part of scientific communication rather than an appendix-only software feature. A concise main paper can point to the population, frozen decision, evidence source, and claim ceiling, while the supplement and repository retain hashes, configs, complete grids, and equivalence receipts. That division supports editorial compression without weakening auditability. It also exposes genuine gaps—cancelled cells, unavailable artifacts, uncertain environments, or low support—instead of smoothing them into narrative completeness.

## 7. Limitations

The following 18 limitations define the manuscript's claim ceilings. Grouping removes repeated caveats but does not merge distinct evidence constraints.

### 7.1 Dataset and provenance

- **Benchmark-family scope (`LIM29-001`).** The empirical chain covers CSE-CIC-IDS2018 and a restricted CICIDS2017 bridge, not live enterprise, cloud, industrial, ISP, or IoT traffic. It cannot support portability claims for arbitrary operational networks or current attacks.
- **Processed reference (`LIM29-002`).** The rebalanced binary reference and stratified split do not reproduce natural prevalence, session structure, or forward chronology. Its high metrics cannot serve as deployment evidence.
- **Semantic bridge (`LIM29-004`).** Cross-dataset results depend on frozen bridge62/70 semantics, preprocessing, learners, direction, and targets. They cannot establish bridge-independent or symmetric portability.
- **Cancelled memberships (`LIM29-005`).** Two `GROUNDED_S4` cells lacked recoverable exact physical-row membership and were cancelled before target opening. The study cannot claim that every preregistered cross-dataset sensitivity was executed.
- **Unavailable artifacts (`LIM29-015`).** Raw datasets and some historical models, probabilities, explanation arrays, or source relationships are external, unavailable, or intentionally closed. Early metrics and exact relationships cannot all be regenerated through the safe interface.
- **Source-restricted graph evidence (`LIM29-016`).** The graph experiment uses an endpoint-authenticated February 20 source, and unseen topology was not estimable. It cannot support graph deployment, unseen-host, or full-reference equivalence claims.
- **Descriptive architecture comparison (`LIM29-017`).** The CNN/ViT comparison is one frozen restored-target contrast rather than a replicated architecture study. It cannot establish universal architecture superiority.

### 7.2 Evaluation and protocol

- **Temporal/family entanglement (`LIM29-003`).** Chronological memberships also change family composition, and controls are mixed. The temporal contrast cannot be attributed solely to chronology or concept drift.
- **LOAO eligibility (`LIM29-006`).** DOS and AUTH_BRUTE_FORCE cannot satisfy the day-atomic ordering, and eligible-family support is heterogeneous. The results cannot cover every benchmark family or define uniform unknown-family capability.
- **Low-support Infiltration (`LIM29-007`).** Infiltration has 36 held-out positives and remains descriptive. It cannot carry family-level inference or pooled primary evidence.
- **Historically reused target (`LIM29-018`).** Stage28 re-evaluates the already opened Stage22 target under a frozen stability protocol. This supports conclusion stability, not independent blind replication.

### 7.3 Statistical

- **Conditional resampling (`LIM29-008`).** Historical paired intervals are conditional on frozen samples, arrays, and implementations. They cannot provide unconditional deployment uncertainty or population-wide significance.
- **Finite seed scope (`LIM29-009`).** Five seeds test the frozen recipe without repeating full hyperparameter optimization. The 5/5 ordering is descriptive and cannot establish a population guarantee or optimization-process stability.

### 7.4 Operational

- **Prior-probability shift (`LIM29-012`).** Stage25 holds true- and false-positive rates fixed while prevalence changes. It characterizes sensitivity to prevalence, not measured performance under simultaneous covariate, protocol, topology, user, or attacker shift.
- **Workload and cost assumptions (`LIM29-013`).** Traffic, analyst service time, capacity, and relative costs are scenarios rather than organization-specific measurements. They cannot establish universal workload, utility, or economic preference.

### 7.5 Hardware and computation

- **Measured component boundary (`LIM29-011`).** Stage26 covers compatible inference components on one hardware/software environment and omits complete capture-to-alert processing. It cannot establish universal latency, throughput, speedup, energy, or end-to-end deployment cost.

### 7.6 Reproducibility

- **Historical environment ambiguity (`LIM29-010`).** Some dependencies and execution environments remain `VERSION_NOT_PROVEN`; adjacent receipts are not generalized. Bit-for-bit reconstruction of every historical environment is not supported.
- **Incomplete full reruns (`LIM29-014`).** Static provenance, scalar evidence, configurations, canonical methods, archives, and equivalence tests make the manuscript chain auditable, but missing data or closed artifacts prevent some end-to-end reruns. The repository cannot claim that every result is locally regenerable.

## 8. Conclusion

A processed benchmark score is a necessary reference, not a complete capability claim. Across the frozen validation chain, strong reference discrimination survived; chronological development retained higher forward ranking across five seeds; the forward cross-dataset bridge retained signal; several eligible withheld families remained discriminable; and compatible inference paths were feasible on the recorded hardware.

Other conclusions remained conditional. Frozen thresholds transferred poorly even when ranking survived, reverse cross-dataset transfer was near its anchor, shortcut and placebo interactions did not isolate one mechanism, operational projections depended on prevalence and workload assumptions, and withheld-family behavior varied by learner and support.

Future IDS evaluations should therefore name the validity condition, population, metric, operating rule, uncertainty, and adaptation boundary attached to each claim. Reporting benchmark, temporal, shortcut, domain, operational, computational, unknown-family, and realization evidence separately preserves both failures and non-collapse findings. The resulting account is narrower than a universal performance verdict, but it is more useful: it states which capability was observed, where it survived, and what the available evidence does not establish.

Stronger validation thus narrows or qualifies a claim; it does not require a monotonic performance decline, a single failure label, or a universal deployment verdict.

## References

The canonical bibliography for the Pandoc citation keys in this candidate is `manuscript/references.bib`. Its 27 entries and claim-level support boundaries were verified in Pass 2A; Pass 2B introduced no reference or literature expansion.

## Supplementary Material Plan

The supplement is organized into seven evidence groups. Its purpose is to preserve reviewer-facing detail without reproducing the repository or changing evidence status.

### S1. Reference evaluation, uncertainty, and explanation reliability

This section contains frozen membership and duplicate checks; full baseline inventories and tuning records; validation threshold curves; holdout confusion matrices; known-category support; paired operating-point and calibration uncertainty; and fixed-recipe seed tables. It also contains the complete deterministic LIME panel, representative local cases, surrogate-fidelity and decision-agreement diagnostics, and TreeSHAP comparisons. These materials support Table 1 and the stable-but-unfaithful explanation result. Conditional intervals remain conditional, and the supplementary detail does not create a general learner-winner claim.

### S2. Shortcut, representation, and architecture diagnostics

This section provides all seven Stage23 feature subsets, secondary metrics, matched-size placebos, depth-one controls, component attribution summaries, behavior-restricted representations, and attack-family composition tables. It also routes the detailed Integrated Gradients sensitivity, attention diagnostics, source-restricted graph evidence, and descriptive CNN/ViT comparison outside the main narrative. The latter items retain their supplement-only claim status: source restriction, zero frozen-threshold detection, or single-comparison design prevents them from supporting architecture or deployment conclusions. Figure 2 remains the sole main shortcut exhibit.

### S3. Cross-dataset contracts and sensitivities

This section documents bridge62 and bridge70 semantics, direction-specific source and target populations, full ranking and frozen-threshold tables, and the published-versus-corrected aggregate-flag contrasts. It includes their conditional paired intervals, population-governance records, and the exact cancellation receipts for both `GROUNDED_S4` cells. The material supports Figure 3 and Table 3 while keeping directions separate, preserving metric-specific changes, and refusing replacement of missing membership with a post-freeze heuristic.

### S4. Prevalence, workload, capacity, and cost

This section contains the complete prevalence grids, PPV and NPV thresholds, true- and false-alert volumes, analyst-time and capacity scenarios, required-FPR calculations, break-even conditions, relative-cost decisions, and formula checks. It supports Figure 4 and Table 4. Every quantity remains a prior-shift scenario that holds sensitivity and FPR fixed; none is labeled as measured field, organization-specific economic, or live analyst performance.

### S5. Deployment profiling

This section reports warm and cold inference, throughput, memory, package size, component timing, batch schedules, capacity, representation comparisons, Pareto summaries, and all compatible CPU/GPU profiles. Hardware, software, and timing-boundary receipts accompany the tables, while unsupported, incompatible, timed-out, and resource-limited paths retain their statuses. It supports Figure 5 but does not extend the prepared-input-to-probability boundary to capture, feature extraction, alert aggregation, or analyst response.

### S6. Family eligibility and realization stability

This section preserves family aliases, day-atomic chronology, eligibility decisions, support, target construction, full LOAO native metrics, frozen operating points, conditional intervals, and descriptive similarity diagnostics. It includes all seed-level family tables, registered stability classifications, random-split LOAO controls, and the detailed temporal seed and family-aware controls behind Table 2. DDoS, Port Scan, Web Attack, Bot, and Infiltration remain separate; Infiltration remains descriptive at support 36; DOS and AUTH_BRUTE_FORCE remain ineligible; and no aggregate novelty score is formed.

### S7. Provenance, equivalence, and reproduction

This section collects the minimum configs, source maps, archived notebooks and scripts, hashes, environment records, target-opening ledgers, canonical implementation links, equivalence matrices, reproduction indexes, execution boundaries, and static validation reports needed to audit the manuscript. Detailed Stage20 forensic records appear only when they explain a scientific artifact, source identity, or bridge restriction. External datasets, closed artifacts, `VERSION_NOT_PROVEN` environments, and non-rerunnable paths remain disclosed. Repository links carry the full inventory; the supplement does not duplicate it.

Supplementary figures and tables should receive `S` numbering only after a venue template is approved. Existing scientific assets remain unchanged, and later panel assembly must follow the frozen Pass 2B figure registry. No supplementary item may introduce a new claim, number, comparison, metric, or analysis.
