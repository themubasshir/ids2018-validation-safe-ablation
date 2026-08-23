# [Title to be selected after Pass 1]

> **Manuscript status:** Pass 2A literature-verified integration. This document is not final and has not undergone the separate broad editorial pass.

## Abstract

Machine-learning intrusion detectors are often studied on processed benchmark splits [@ring2019survey; @sommer2010closed], but such performance does not by itself establish that the same capability persists under temporal separation, feature perturbation, domain transfer, rare-event prevalence, deployment constraints, or novel attack families. We present an evidence-governed validation framework that evaluates these dimensions as distinct scientific questions while preserving their native metrics and frozen operating rules. Under the conventional processed CSE-CIC-IDS2018 reference condition, the selected balanced tree ensemble achieved F1 0.9285 and PR-AUC 0.9776. That result did not translate into a uniform robustness narrative. On a shared forward target, the mean PR-AUC across the frozen seed set was 0.2599 for random-natural development and 0.6388 for chronological-natural development, with the same ordering in all 5/5 evaluated seeds; nevertheless, frozen operating thresholds transferred poorly, and controls did not isolate chronology as the sole causal mechanism. Cross-dataset ranking was also directional: the IDS2018-to-CICIDS2017 bridge achieved PR-AUC 0.667483, whereas the reciprocal bridge achieved 0.108176. Operational projections supplied a further counterexample: at 0.1% assumed attack prevalence, one operating point retained PPV 0.965572 but required 33.5 analyst-hours per day, while another produced little workload because it projected only 0.0322 true alerts per day. Unseen-family results were selective rather than uniformly negative, with several eligible families retaining stable discrimination while other outcomes depended on the learner or had insufficient support. These findings show that benchmark discrimination and validated capability are related but non-equivalent claims. The framework therefore recommends axis-specific evaluation, locked target governance, separate reporting of ranking and operating-point behavior, explicit deployment assumptions, and claim-to-artifact provenance. Conclusions remain conditional on the evaluated benchmark families, frozen feature bridges, finite seed set, projected operational assumptions, eligible attack families, and measured hardware.

## 1. Introduction

Machine-learning intrusion detection is often summarized by predictive metrics measured on a benchmark test set [@ring2019survey; @sommer2010closed]. Those metrics answer an important question: under a specified representation, split, model, and operating rule, how well does the fitted system distinguish the benchmark labels? A stronger inference—that the detector will remain useful when traffic moves forward in time, when dataset-specific cues change, when a second collection pipeline is introduced, when attacks are rare, or when an attack family was absent during development—requires separate validation across those conditions [@arp2022dos]. The first claim concerns benchmark performance. The second concerns validated capability. They are not interchangeable.

Several mechanisms can break the inference between them. Random partitions may mix temporal regimes or attack-family composition in ways that a forward evaluation does not [@arp2022dos; @pendlebury2019tesseract]. Predictors that are discriminative inside one split can act as unstable shortcuts under another [@engelen2021troubleshooting; @arp2022dos]. Cross-dataset evaluation therefore requires a defensible shared feature representation rather than nominal column-name equality [@dhooge2020interdataset; @layeghy2023crossdomain]. Ranking metrics and operating-point decisions also answer different questions when class priors or populations change [@saito2015precision; @saerens2002prior]. Precision and workload can change sharply under low attack prevalence [@axelsson2000baserate; @layman2023falsealarms], and computational feasibility depends on the actual inference path and hardware [@mattson2020mlperf; @mirsky2018kitsune]. Finally, evaluation with attacks absent from training depends on how unknown classes and success criteria are defined [@zoppi2023unknown; @shin2023openset].

These concerns are separate evaluation problems. Treating them independently is scientifically appropriate because their outcomes are expressed in different quantities: PR-AUC and ROC-AUC characterize ranking; precision, recall, F1, and FPR characterize a selected operating point; PPV and alert volume translate rates under prevalence assumptions; and latency, throughput, and memory describe computational behavior [@saito2015precision; @axelsson2000baserate; @mattson2020mlperf]. What is missing from this study's performance-centered account is a disciplined way to connect these questions without collapsing them into an artificial robustness score or assuming that failure on one axis explains failure on another.

This work reconstructs a connected empirical validation chain around two benchmark families, CSE-CIC-IDS2018 and CICIDS2017. The chain begins with a conventional processed-data reference evaluation and then asks what remains supported under stronger or different validity conditions: source-faithful temporal partitions, shortcut-feature perturbations and controls, bidirectional cross-dataset bridges, prior-shift prevalence scenarios, hardware-specific profiling, leave-one-attack-family-out evaluation, and seed/control stability. Each target-facing analysis was governed by a frozen protocol and an explicit anti-adaptation boundary. Each conclusion is reported in its native metric and linked to the population, source artifact, configuration, code, and provenance record that support it.

The resulting evidence is neither a monotonic collapse nor a model-success narrative. The conventional reference result is strong. Chronological development produces substantially better forward ranking than random development under the evaluated protocol, but its operating thresholds still transfer poorly. Forward cross-dataset transfer retains meaningful ranking while the reverse direction is near its prevalence anchor. Some shortcut perturbations reveal strong split interactions, yet placebo perturbations prevent those interactions from being read as proof of leakage. Some eligible attack families transfer strongly across learners and seeds; others are learner-dependent, ineligible, or too weakly supported for inferential claims. Operationally, high PPV can coexist with excessive workload, while low workload can reflect negligible detection yield rather than suitability. These counterexamples are central to the validation argument because they identify which inference failed, not merely whether a model score decreased.

The manuscript makes the following contributions:

1. It applies in this study a connected, validation-safe IDS evaluation framework in which benchmark, temporal, shortcut, cross-dataset, operational, computational, unseen-family, and realization validity remain distinct axes.
2. It provides a source-faithful temporal and operating-point audit, closed across a frozen seed set, that separates ranking stability from threshold transfer and from causal interpretation.
3. It combines a controlled shortcut-feature audit with bidirectional dataset transfer, preserving placebo evidence, directionality, bridge restrictions, and cancelled analyses.
4. It links prevalence, alert workload, relative cost, and measured computational profiles while keeping analytic assumptions and hardware boundaries explicit.
5. It evaluates zero-training-exposure attack families through eligibility-gated, family-specific results that retain learner dependence and low-support classifications rather than claiming universal zero-day detection.
6. It supplies a claim-to-provenance layer connecting manuscript statements and numbers to frozen artifacts, protocols, canonical implementations, archived sources, equivalence evidence, and known reproducibility gaps.

The contribution is therefore an evaluation discipline rather than a proposed detector. The study does not claim that machine-learning IDS is universally ineffective, that temporal splitting is always superior, that shortcut features cause all transfer failure, or that leave-one-family-out evaluation proves real-world zero-day detection. It asks a narrower and more useful question: which apparent benchmark capabilities survived each evaluated validity condition, which did not, and what remained unresolved?

## 2. Related Work

### 2.1 Benchmark-based intrusion detection

CICIDS-family releases provide documented flow-derived benchmark data for machine-learning evaluation. The original associated publication describes CICFlowMeter-derived features and evaluates multiple machine-learning algorithms; later dataset surveys situate these releases among network-IDS benchmarks [@sharafaldin2018toward; @ring2019survey; @cse_cic_ids2018_official]. Performance metrics remain conditional on dataset construction, class balance, split, representation, and evaluation protocol [@he2009imbalanced; @sommer2010closed]. The present study therefore treats its processed CSE-CIC-IDS2018 result as a reference condition rather than as direct evidence of operational portability.

The distinction between a useful benchmark and a representative deployment population is especially important for processed or rebalanced data. Rebalancing changes the experimental class distribution and can be useful for a defined learning comparison, but it does not make the evaluation population representative of the temporal or prevalence conditions of deployment [@he2009imbalanced; @sommer2010closed; @pendlebury2019tesseract]. Our framework therefore retains the conventional benchmark result while testing different validity dimensions in separate, source-governed populations.

### 2.2 Split, temporal, and shortcut validity

Random train/test partitioning assumes that sampled memberships adequately represent the intended future use. That assumption can be weakened when training and test records share collection artifacts, near-duplicate structure, or temporal and family dependencies [@engelen2021troubleshooting; @arp2022dos]. Security-ML work therefore recommends evaluation designs that respect the intended time and deployment direction; such designs can also change prevalence and class composition [@pendlebury2019tesseract]. A temporal contrast must therefore be interpreted as a change in evaluation geometry, not automatically as a clean estimate of concept drift.

Feature leakage and shortcut learning present a related but distinct problem. Dataset identifiers, collection artifacts, and features produced by flawed extraction or labeling pipelines can be predictive without encoding transportable attack behavior [@engelen2021troubleshooting; @arp2022dos]. Removing a feature and observing a metric change establishes sensitivity to the intervention; it does not by itself prove that the feature was leakage or that it caused later transfer failure. Controls that test competing explanations are needed before a leakage or causal-transfer claim.

Explainability methods add a second validity layer. LIME fits a local interpretable surrogate [@ribeiro2016lime], whereas SHAP defines additive feature attributions and TreeSHAP supplies tree-specific algorithms [@lundberg2017shap; @lundberg2020trees]. Explanation sensitivity or stability and fidelity are distinct evaluation properties; one cannot substitute for the other [@yeh2019infidelity].

### 2.3 Cross-dataset and operational evaluation

Cross-dataset evaluation directly tests performance when training and target traffic come from different benchmark domains. Published studies show that performance can depend strongly on dataset pairing, shared feature representation, and source-target direction, including marked asymmetry when the direction is reversed [@dhooge2020interdataset; @layeghy2023crossdomain; @cantone2024crossdataset]. The present framework therefore uses frozen semantic bridges and reports IDS2018-to-CICIDS2017 and CICIDS2017-to-IDS2018 transfer separately.

Operational evaluation introduces the base-rate problem. At rare attack prevalence, sensitivity and specificity alone do not determine PPV or false-alert burden [@axelsson2000baserate], and controlled IDS-alarm evidence shows that false-alarm rate can affect analyst precision and time on task [@layman2023falsealarms]. Prior-probability-shift calculations require explicit assumptions about unchanged conditional distributions [@saerens2002prior]. They are conditional analytic translations, not observed field performance; the cost and workload results in this study likewise remain scenario projections.

### 2.4 Deployment, novelty, and reproducibility

Predictive performance is only one part of deployability. System feasibility depends on the measured inference path, workload scenario, latency or throughput metric, resource boundary, software configuration, and hardware [@mattson2020mlperf]. IDS demonstrations on constrained devices also show why the feature-extraction and model-execution boundaries must remain explicit [@mirsky2018kitsune]. Benchmark values are interpretable only within those boundaries and must not be generalized as universal constants.

Open-set recognition formalizes evaluation in which unknown classes can appear at test time [@scheirer2013openset], and IDS studies have evaluated attacks withheld from model training under explicitly constructed unknown-attack protocols [@zoppi2023unknown; @shin2023openset]. Conclusions depend on what is withheld, how unknown classes and thresholds are defined, and which metrics are reported. This study's leave-one-attack-family-out design is a bounded benchmark analogue, not evidence of arbitrary future or live zero-day detection.

Finally, machine-learning reproducibility programs emphasize code, experimental details, reporting checklists, and independent attempts to regenerate results [@pineau2021reproducibility]. Separately, adaptive analysis shows that repeated use of holdout feedback can undermine ordinary validity guarantees [@dwork2015holdout]. Code release therefore does not by itself resolve data, environment, provenance, or adaptation limits. This study responds with protocol locks, immutable source archives, explicit target-opening ledgers, equivalence receipts, and claim-level mapping, while retaining limitations where raw data, historical environments, or closed artifacts prevent complete reruns.

## 3. Datasets and Provenance

### 3.1 CSE-CIC-IDS2018 reference and source-faithful roles

CSE-CIC-IDS2018 is a benchmark release documented by the Canadian Institute for Cybersecurity and associated dataset publication [@cse_cic_ids2018_official; @sharafaldin2018toward]. It serves two related but non-equivalent roles in this study. The conventional reference analysis uses a processed, rebalanced binary table preserved by the original experiment. Its frozen memberships contain 192,593 training rows, 48,149 validation rows, and 60,186 holdout rows. This representation supports controlled model selection, operating-point selection, and within-table holdout reporting. It is not presented as a natural-prevalence, session-independent, or forward-temporal population.

Later temporal analyses use source-faithful dated IDS2018 exports and independently governed membership artifacts. “Source-faithful” means that the representation follows authenticated source columns, cleaning rules, and temporal roles recovered from the original research lineage; it does not mean that every raw packet or historical execution environment is available. The temporal target is therefore scientifically distinct from the processed reference holdout even when both derive from the IDS2018 benchmark family. In particular, the source-faithful audit preserves collection order and a common forward target rather than treating rows as exchangeable samples.

This distinction prevents two common conflations. First, high discrimination on the processed reference table cannot be described as temporal validation. Second, a later source-faithful result does not retroactively make the original processed table naturalistic. The two populations answer different questions and remain separate throughout the manuscript.

### 3.2 CICIDS2017 cross-dataset role

CICIDS2017 is a distinct Canadian Institute for Cybersecurity benchmark with documented collection dates, attack scenarios, PCAPs, labeled flows, and CICFlowMeter-derived features [@cicids2017_official; @sharafaldin2018toward]. It supplies the second benchmark domain, the packet/flow provenance needed for selected representation audits, and the attack-family chronology used by the leave-one-family-out analysis. The primary cross-dataset direction trains on the frozen IDS2018 source representation and evaluates on an effective CICIDS2017 target containing 2,830,743 rows. The reciprocal direction trains under the frozen CICIDS2017 source protocol and evaluates on the IDS2018 February 28 target. Because source learners, target prevalence, feature availability, and extractor semantics differ by direction, the two transfers are never averaged.

Cross-dataset comparability is defined by frozen semantic bridges rather than by nominal column-name equality. The primary bridge62 contract retains the shared predictors whose semantics could be defended in both domains. A bridge70 variant adds the frozen aggregate-flag fields and supports a serialization-sensitivity audit. “Published” denotes the field interpretation present in the released feature artifact; “corrected” denotes the preregistered correction to the aggregate TCP-flag serialization. Both are retained because changing the interpretation after seeing target performance would erase an important provenance dependency.

Two planned GROUNDED_S4 target cells were cancelled before target opening. Exact durable physical-row membership could not be reconstructed without introducing a new post-freeze matching heuristic. The cells were neither approximated nor replaced, and their absence is treated as a limitation rather than an unfavorable result.

### 3.3 Attack-family mapping and evaluation populations

The early reference analysis reports known attack categories within the processed IDS2018 holdout. Those categories describe error concentration under a familiar label distribution; they are not novelty tests. The later leave-one-attack-family-out protocol instead uses CICIDS2017 family/day structure and requires zero exposure to the target family in both training and validation.

Five families satisfied the frozen eligibility rules. DDoS, Port Scan, Web Attack, Bot, and Infiltration could be assigned to distinct development and target periods under the day-atomic chronology. DOS and AUTH_BRUTE_FORCE were structurally ineligible because the required training, validation, and target ordering could not be constructed without post hoc folds. Infiltration remained executable but its target contained only 36 positive examples, so it is descriptive throughout the manuscript. Family mappings, aliases, chronology, and support gates were locked before inferential reporting.

The principal target for each eligible family combines the held-out family with temporally matched benign traffic. A broader context target that also includes known attacks is secondary and descriptive. This separation allows the primary result to ask whether the score distinguishes a genuinely withheld family from benign traffic without converting the experiment into a claim about arbitrary future attacks.

### 3.4 Provenance states and target governance

The repository uses several provenance terms that must remain distinct. **Raw-exact** identifies immutable source bytes whose hashes and identities are preserved. **Published** identifies the semantics serialized in an originally released table or extractor output. **Corrected** identifies a frozen, documented correction applied without changing the raw source. **Source-faithful** identifies a derived representation whose construction follows authenticated source semantics and locked cleaning rules. **Reconstructed** identifies an artifact recovered from surviving lineage evidence; it is never treated as raw-exact unless byte identity is proven.

The Stage20 forensic program is relevant where it establishes source identities, packet/flow alignment boundaries, compact-corpus lineage, and the aggregate-flag serialization correction used by later bridge analyses. Detailed parser investigations, transport receipts, storage events, and failed mechanism searches remain repository or supplementary provenance rather than main-text scientific results.

Target governance is role-specific. Development data may support fitting, validation-based operating-point selection, or protocol checks only as declared by the frozen design. Final targets are opened under terminal ledgers, with no target-guided model fitting, feature search, calibration, or threshold reselection. Some target populations were historically opened in earlier phases and later reused for preregistered stability analysis; they are not relabeled as new blind holdouts. Current reproducibility interfaces verify identities, schemas, and receipts without reopening scientific targets or deserializing models.

## 4. Validation Framework and Methods

### 4.1 Reference Evaluation and Governance

**Question and population.** The reference evaluation asks what conventional validation-selected models and operating points achieve on the processed CSE-CIC-IDS2018 binary table. Frozen stratified memberships separate training, validation, and holdout roles. Scaling is fitted on training data and applied only to models whose historical protocol requires scaled inputs; tree boosting retains its recorded tabular preprocessing. A single universal preprocessing pipeline would be historically inaccurate.

**Protocol and learner scope.** A broad baseline inventory is narrowed through validation-only tuning to the recorded XGBoost and LightGBM reference learners. Validation selects two operating roles: a balanced XGBoost point at threshold 0.51 and a constrained-security LightGBM point at threshold 0.26. The holdout is descriptive after those decisions and is not used to revise the model or threshold.

**Metrics, uncertainty, and boundary.** Ranking is reported with ROC-AUC and PR-AUC; operating behavior is reported with F1, F2, precision, recall, FPR, and error counts. Historical paired uncertainty and calibration analyses compare the selected learners on the same frozen holdout. The security constraint belongs to the validation selection rule; later unconstrained cost analyses do not inherit it. The result establishes a conventional within-table reference, not natural prevalence, temporal validity, cross-dataset portability, or deployment utility.

### 4.2 Temporal Validation

**Question and population.** Temporal validation asks whether the development geometry changes ranking and operating-point transfer on one common forward IDS2018 target. Four frozen development cells cross random versus chronological membership with natural versus training-only rebalanced prevalence. All cells are evaluated on the same final population of 1,374,133 rows, containing 375,345 attack and 998,788 benign rows.

**Protocol and learner scope.** The temporal design uses the frozen tree-ensemble recipe, source-faithful cleaning, and predeclared development roles. Random cells estimate performance under exchangeable membership assumptions. Chronological cells preserve the source order and separate earlier development periods from later evaluation. Rebalancing applies only to training. No model, feature, calibration, or threshold is adapted after the shared target is opened.

**Metrics, uncertainty, and boundary.** PR-AUC and ROC-AUC quantify ranking because target prevalence differs across development cells; frozen-threshold precision, recall, F1, and FPR quantify operating-point transfer. The final stability layer repeats the designated random-natural and chronological-natural linkage across a fixed seed set and reports frozen means, standard deviations, and directional consistency. That analysis is descriptive conclusion stability, not a new significance test. Family-aware controls assess whether chronology alone explains the contrast. The axis establishes sensitivity to validation geometry under the evaluated source chronology; it does not establish session independence, universal temporal superiority, or concept drift as a sole cause.

### 4.3 Shortcut-Feature Audit

**Question and population.** The shortcut audit asks whether ranking changes when plausible identity-, protocol-, window-, or behavior-related predictors are removed from the frozen Stage22 development populations. The primary design contains seven preregistered feature subsets, evaluated separately under random-natural and chronological-natural geometry and across the frozen tree learners.

**Protocol and controls.** Primary removals are paired with matched-size placebo removals, depth-one single-feature controls, feature-importance redistribution checks, behavior-restricted representations, and attack-family composition tables. These controls distinguish sensitivity to a named removal from sensitivity to removing any similarly sized block. They also expose whether chronological outcomes coincide with a narrower attack-family population.

**Metrics, uncertainty, and boundary.** PR-AUC and ROC-AUC remain the primary ranking metrics, supplemented by frozen operating-point results and conditional paired intervals where available. Component-specific TreeSHAP summaries are descriptive proxies rather than exact attributions for an averaged-probability ensemble. A separate local-explanation audit evaluates LIME decision agreement, surrogate fidelity, perturbation stability, and agreement with exact TreeSHAP on a deterministic panel. No target-guided subset search occurs. The axis establishes feature and split sensitivity; it does not prove that a tested feature is leakage or that one shortcut causes cross-domain failure.

### 4.4 Cross-Dataset Transfer

**Question and population.** Cross-dataset evaluation asks how source-trained rankings and frozen operating points behave when transferred between IDS2018 and CICIDS2017 under explicit shared-feature contracts. Forward and reverse directions have separate source models, targets, prevalence anchors, and interpretation.

**Protocol and learner scope.** Bridge62 is the primary semantic intersection. Bridge70 is a preregistered sensitivity representation that includes aggregate-flag fields under both published and corrected serialization. Source training, validation-based thresholds, feature contracts, and target cleaning are frozen independently of target results. No target labels guide fitting, feature selection, thresholding, or calibration.

**Metrics, uncertainty, and boundary.** Direction-specific PR-AUC and ROC-AUC characterize ranking. Frozen threshold metrics characterize operating transfer, and Brier score is included in the serialization sensitivity. Conditional paired bootstrap intervals quantify within-target published-versus-corrected contrasts without converting them into an unconditional population claim. The two cancelled GROUNDED_S4 cells remain absent. This axis establishes bridge- and direction-specific transfer for two related benchmark families; it does not establish portability to arbitrary datasets or a unique causal mechanism.

### 4.5 Prevalence and Operational Stress

**Question and population.** Operational stress asks how frozen sensitivity and false-positive rates translate when the assumed attack prior, traffic volume, analyst service time, capacity, or relative error cost changes. It inherits operating points from the temporal and cross-dataset evaluations and performs no new fitting or target access.

**Protocol.** Under the frozen prior-probability-shift model, sensitivity and specificity remain fixed while prevalence varies over a preregistered grid. PPV and NPV are derived from the inherited rates and assumed prior. Alert counts translate those rates under frozen daily traffic scenarios; workload applies the declared analyst service-time and capacity assumptions; relative cost compares false alerts and missed attacks under scenario-specific weights.

**Metrics, uncertainty, and boundary.** PPV, NPV, true and false alerts, analyst-hours, capacity exceedance, required FPR, and relative cost are operational projections, not predictive ranking metrics. Their uncertainty is inherited from the frozen operating points and scenario definitions; no new bootstrap is introduced for the projections. The axis shows how the character of a fixed operating point changes under stated assumptions. It does not measure field performance under covariate, protocol, topology, attacker, or behavior shift, and it does not establish a universal SOC preference.

### 4.6 Deployment Profiling

**Question and population.** Deployment profiling asks which frozen, compatible model paths are computationally feasible on the recorded Stage26 hardware and software. The measurement boundary begins with prepared model input and ends with materialized model probabilities; it is not complete packet-capture-to-alert latency.

**Protocol and learner scope.** Eligible tree, ensemble, and packet-image artifacts are profiled under frozen batch schedules for warm inference, cold start, throughput, memory, package size, component timing, and matched CPU/GPU conditions. Groups with different representations remain separate. A missing backend, incompatible artifact, timeout, or resource-limit outcome is reported as a status rather than imputed as a latency value.

**Metrics, uncertainty, and boundary.** Latency percentiles, throughput, memory, and artifact size remain in their native units. Repeated measurements provide condition-level summaries; CPU/GPU ratios are descriptive point estimates without ratio-level confidence intervals. No batch is retrospectively selected as optimal. The axis establishes measured component feasibility for compatible paths on one recorded environment, not universal latency, complete end-to-end IDS cost, or performance on unsupported backends.

### 4.7 Leave-One-Attack-Family-Out Evaluation

**Question and population.** The leave-one-attack-family-out design asks whether a learner with zero training and validation exposure to an eligible target family can rank that family above temporally matched benign traffic and detect it at frozen operating points. Eligibility requires a day-atomic TRAIN < VALIDATION < TARGET ordering and sufficient target support.

**Protocol and learner scope.** XGBoost and LightGBM are evaluated independently for each eligible family. Source memberships, feature space, fitting recipes, validation thresholds, family aliases, and target roles are frozen before target evaluation. DOS and AUTH_BRUTE_FORCE remain ineligible; Infiltration is retained only as descriptive evidence because its target support is 36.

**Metrics, uncertainty, and boundary.** ROC-AUC and PR-AUC assess ranking relative to chance and target prevalence. Recall and related metrics at standard, balanced, and security thresholds assess operating-point transfer. Family-specific conditional intervals and support accompany the primary results; a behavioral-similarity analysis remains descriptive and non-causal. This axis tests eligible benchmark-family withholding. It does not demonstrate detection of arbitrary future exploits, establish universal zero-day capability, or authorize a pooled novelty score.

### 4.8 Seed and Control Stability

**Question and protocol.** Stability analysis asks whether the principal temporal direction and eligible-family conclusions are artifacts of one training realization. The frozen seed registry repeats the designated temporal and LOAO cells without selecting a best seed and without repeating the entire historical hyperparameter search. A random-split LOAO arm serves as a control for the additional difficulty associated with chronology.

**Metrics and boundary.** Seed-level PR-AUC, ROC-AUC, and operating-point outcomes are summarized with frozen means, standard deviations, directional counts, and family/learner stability classifications. Training-seed variation remains separate from sampling/bootstrap uncertainty. The control is not a deployment estimate and does not identify one causal temporal mechanism. Stability over the frozen seed set strengthens conclusions within scope but does not create a population guarantee over all model realizations.

### 4.9 Statistical Uncertainty and Anti-Adaptation Controls

Historical uncertainty analyses use paired, class-stratified resampling so compared learners or representations share each resampled population. Calibration, operating-point, feature-subset, and serialization contrasts retain the uncertainty type declared by their frozen protocols. Conditional intervals are described as conditional; intervals containing zero are not converted into evidence of equivalence, and intervals excluding zero do not broaden the target population.

Anti-adaptation rules are enforced at each evaluation boundary. Model families, hyperparameters, feature subsets, semantic bridges, operating points, target roles, and eligible families are frozen before their corresponding target result. No later target result is used to retune an earlier protocol. Cancelled analyses stay cancelled. Training-seed summaries are not combined with bootstrap distributions, and heterogeneous metrics are never normalized into a common degradation score.

### 4.10 Reproducibility and Provenance

Every substantive manuscript claim is mapped to a Stage29 claim identifier and supporting evidence identifiers. Every scientific number is mapped to a frozen number identifier, source artifact, and manuscript location. Source maps connect each scientific subsection to protocols, canonical code, archived notebooks or scripts, equivalence evidence, and the manuscript reproduction index.

Reproducibility classes remain explicit. The repository can verify source identities, configs, schemas, scalar values, hashes, toy formulas, and approved read-only equivalence checks. It does not claim that every historical environment can be reconstructed or every empirical stage can be rerun end to end. Raw datasets, some historical artifacts, and closed targets remain external, unavailable, or intentionally inaccessible through the validation-safe interface. This limitation is part of the paper's provenance claim rather than hidden behind a single requirements file.

## 5. Results

### 5.1 Conventional Benchmark Performance

The conventional reference condition produced strong within-table discrimination. At the validation-selected balanced operating point, XGBoost achieved holdout F1 0.9285, FPR 0.0061, ROC-AUC 0.9802, and PR-AUC 0.9776. The LightGBM security operating point traded a higher FPR of 0.0466 for its recall-oriented objective, with F1 0.9178, F2 0.9112, ROC-AUC 0.9802, and PR-AUC 0.9777. These results establish the benchmark reference that the remaining analyses interrogate; they do not establish temporal, cross-dataset, or deployment validity.

The apparent proximity of the learners was not converted into a winner claim. For the balanced comparison, the frozen XGBoost-minus-LightGBM F1 difference was 0.000185, with a conditional interval from −0.000495 to 0.000862. The interval includes zero, so the difference remained unresolved on the frozen holdout. At the security points, LightGBM missed 33 fewer attacks, with the conditional difference interval spanning 2 to 64 fewer misses. The result is specific to those frozen points rather than evidence of universal learner superiority.

Calibration likewise did not yield a resolved winner. XGBoost and LightGBM Brier scores were 0.04277 and 0.04275, respectively, and the paired calibration-difference intervals retained in the frozen analysis included zero. This is useful negative evidence: both probability outputs were adequate for the reference analysis, but neither learner acquired a general calibration advantage.

**Table 1. Conventional processed-reference holdout results.** Values are copied from the frozen number registry; thresholds were selected on validation data.

| Operating role | Learner | Threshold | F1 | F2 | FPR | ROC-AUC | PR-AUC |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Balanced | XGBoost | 0.51 | 0.9285 | — | 0.0061 | 0.9802 | 0.9776 |
| Security | LightGBM | 0.26 | 0.9178 | 0.9112 | 0.0466 | 0.9802 | 0.9777 |

### 5.2 Temporal Validity

The shared forward target changed the interpretation of the reference success, but not through a uniform collapse. Across the frozen seed set, random-natural development produced mean ROC-AUC 0.5176 (SD 0.0073) and PR-AUC 0.2599 (SD 0.0034). Chronological-natural development produced mean ROC-AUC 0.8209 (SD 0.0085) and PR-AUC 0.6388 (SD 0.0322). Random-natural ranking was below chronological-natural ranking for both metrics in 5/5 seeds. The direction was therefore not a seed-specific peculiarity within the preregistered realization set.

Ranking improvement did not imply usable transfer of the development operating point. The chronological thresholds almost never fired on the common forward target, despite retaining substantially stronger ranking. Conversely, the two random security operating points reached final FPR values of 0.2870 and 0.2685, far above the development-era security constraint. The appropriate conclusion is that development geometry affected both score ordering and score scale, and that those properties must be evaluated separately.

The family-aware controls prevent a single-mechanism interpretation. Random-versus-chronological contrasts varied by attack family and learner, and the random control was not a deployment estimate. The evidence is consistent with chronology compounding novelty difficulty in specific comparisons, but it does not identify temporal drift as the sole cause or establish that chronological training is universally preferable.

**Figure 1. Temporal ranking transfer.** Two-panel conceptual exhibit using the approved PR-AUC and ROC-AUC transfer figures; no panels are redrawn in Pass 1.

**Table 2. Five-seed temporal stability on the shared forward target.**

| Development geometry | Mean ROC-AUC | ROC-AUC SD | Mean PR-AUC | PR-AUC SD | Directional result |
| --- | ---: | ---: | ---: | ---: | --- |
| Random-natural | 0.5176 | 0.0073 | 0.2599 | 0.0034 | Lower than chronological in 5/5 seeds for both metrics |
| Chronological-natural | 0.8209 | 0.0085 | 0.6388 | 0.0322 | Higher than random in 5/5 seeds for both metrics |

### 5.3 Shortcut Sensitivity

The shortcut audit found strong sensitivity to feature-set and split geometry, but no universal removal benefit. Some preregistered removals changed random-natural ranking more than chronological ranking, while others produced the opposite interaction. The behavior-restricted representation retained strong discrimination under random membership but did not preserve the chronological result. Attack-family conditioning further showed that the chronological development population was compositionally narrower than the random population. These findings constrain the benchmark interpretation, but they do not isolate a single shortcut responsible for later transfer behavior.

Placebo evidence is important to that boundary. Matched-size placebo removals also produced non-zero split interactions, including conditional intervals that excluded zero in the frozen analysis. An interaction can therefore be real without identifying a named feature as leakage. Depth-one controls and component-specific attribution summaries support the presence of split-specific discriminative cues, while the placebo and composition results prevent a causal reading.

The local explanation audit provides a complementary tension. LIME feature rankings were comparatively stable across perturbation seeds, yet only 2 of 64 explanations met all prespecified fidelity and cross-method criteria, and 31 of 64 failed to reproduce the model's local classification decision. Mean local SHAP–LIME top-10 Jaccard agreement was 0.304 for XGBoost and 0.360 for LightGBM. Stability was therefore not sufficient evidence of local faithfulness. TreeSHAP remains the primary attribution method; LIME is retained as a supplementary surrogate-reliability stress test.

**Figure 2. Shortcut-subset and split interaction.** Approved existing figure showing feature-subset behavior by validation geometry, accompanied by the placebo and causal-interpretation caveat.

### 5.4 Cross-Dataset Transfer

Cross-dataset ranking was strongly asymmetric. Under the primary bridge62 contract, IDS2018-to-CICIDS2017 transfer achieved PR-AUC 0.667483 and ROC-AUC 0.733946 on 2,830,743 effective CICIDS2017 rows. In the reciprocal CICIDS2017-to-IDS2018 direction, the target attack prevalence was 0.104847 and bridge62 achieved PR-AUC 0.108176 and ROC-AUC 0.525167. The reverse PR-AUC was therefore only slightly above its prevalence anchor, whereas the forward direction retained substantial ranking signal.

The result cannot be summarized by averaging directions. The source learners, target populations, prevalence, and available feature semantics differ, and the asymmetry is itself the scientific finding. Nor did a larger bridge uniformly improve portability. In the aggregate-flag sensitivity, correcting the bridge70 serialization changed PR-AUC by −0.007729, ROC-AUC by +0.002192, and Brier score by +0.005087; the frozen paired intervals excluded zero. The metric directions differ, so the correction cannot be called a common degradation or improvement.

The two cancelled GROUNDED_S4 cells remain part of the cross-dataset result boundary. Their absence shows that exact membership governance can limit what is estimable. No fuzzy reconstruction was substituted, and no available transfer result is presented as if those cells had been completed.

**Figure 3. Bidirectional cross-dataset ranking.** Two-panel conceptual exhibit using the approved normalized PR-AUC and ROC-AUC directionality figures.

**Table 3. Primary bidirectional bridge62 transfer.**

| Direction | Target scope | Target prevalence | PR-AUC | ROC-AUC |
| --- | --- | ---: | ---: | ---: |
| IDS2018 → CICIDS2017 | 2,830,743 effective rows | target-specific | 0.667483 | 0.733946 |
| CICIDS2017 → IDS2018 | frozen February 28 target | 0.104847 | 0.108176 | 0.525167 |

### 5.5 Prevalence and Operational Consequences

The prevalence analysis shows why benchmark precision and F1 cannot be read as deployment utility without an explicit prior and workload model. At 0.1% assumed attack prevalence, the Stage22 random STANDARD point retained projected PPV 0.965572. Its high PPV did not imply a low-volume workflow: under the frozen traffic and service-time assumptions it required 33.5 analyst-hours per day. The chronological STANDARD point showed the opposite counterexample. It projected PPV 0.000551068 and only 0.0322 true alerts per day. The small workload reflected negligible detection yield rather than operational suitability.

The Stage24 directionality persisted after prior-shift translation. At 0.1% assumed prevalence, the forward STANDARD transfer points projected PPV from 0.039233 to 0.060313, whereas the reciprocal direction projected only 0.000257610 to 0.000287993. Under the frozen 1:100 relative-cost scenario, 15/24 operating points favored the model at 0.1% prevalence, but only 3/24 did so at 0.01%. Operational preference was thus conditional on prevalence, rates, traffic, capacity, service time, and relative cost—not an intrinsic property of the learner.

These quantities are projections under prior-probability shift. They do not incorporate changes to sensitivity or FPR caused by covariate, protocol, topology, user, or attacker shift, and they are not observations from a live security operations center.

**Figure 4. PPV under prevalence stress.** Approved existing PPV-cliff figure with prior-shift assumptions in the caption.

**Table 4. Selected frozen operating-point translations at 0.1% assumed prevalence.**

| Frozen condition | Projected PPV | Additional operational quantity | Interpretation boundary |
| --- | ---: | --- | --- |
| Stage22 random STANDARD | 0.965572 | 33.5 analyst-hours/day | High PPV does not guarantee manageable workload |
| Stage22 chronological STANDARD | 0.000551068 | 0.0322 true alerts/day | Low workload does not guarantee useful yield |
| Forward transfer STANDARD range | 0.039233–0.060313 | direction-specific | Conditional prior-shift projection |
| Reverse transfer STANDARD range | 0.000257610–0.000287993 | direction-specific | Conditional prior-shift projection |

### 5.6 Deployment Characteristics

Computational behavior was architecture-, batch-, backend-, and hardware-dependent. At batch one on the recorded system, the p95 CPU-over-GPU latency ratio was 1.94 for the five-checkpoint soft-voting ensemble and 1.58 for the single-resource reference, indicating a GPU advantage. The corresponding ratios for the Stage16 CatBoost and XGBoost paths were 0.16 and 0.26, indicating a CPU advantage under the same ratio convention. The packet-image CNN showed a ratio of 10.86, whereas the ViT ratio was 1.05. These contrasts rule out a general claim that one backend is faster across model families.

The profiles cover the prepared-input-to-probability component. They do not include packet capture, flow extraction, representation construction outside the declared boundary, alert aggregation, or analyst response. Unsupported LightGBM GPU execution and other unavailable paths are compatibility statuses, not slow measurements. Ratio values are descriptive point estimates, and the single recorded hardware environment bounds all timing claims.

**Figure 5. Hardware-specific CPU/GPU p95 comparison.** Approved existing Stage26 speedup figure; model groups and component boundaries remain explicit.

### 5.7 Unseen-Family Evaluation

Leave-one-family-out evaluation produced selective transfer rather than a universal result. DDoS transferred strongly for both learners: XGBoost reached ROC-AUC 0.9982 and PR-AUC 0.9925, while LightGBM reached ROC-AUC 0.9986 and PR-AUC 0.9940. Web Attack also retained strong ranking, with XGBoost ROC-AUC 0.9693 and PR-AUC 0.7206 and LightGBM ROC-AUC 0.9901 and PR-AUC 0.7605. These counterexamples matter because they show that withholding a family did not uniformly erase discrimination.

Other families were more conditional. For Bot, XGBoost produced ROC-AUC 0.3224 and PR-AUC 0.003256, whereas LightGBM produced ROC-AUC 0.5591; the family was therefore learner-dependent and neither frozen operating point yielded a broad capability claim. Port Scan also showed a substantial learner difference, with ROC-AUC 0.5506 for XGBoost and 0.7559 for LightGBM, even though its qualitative stability conditions were retained across the frozen seeds. Infiltration remained descriptive because its held-out positive support was 36. DOS and AUTH_BRUTE_FORCE were ineligible rather than counted as model failures.

Ranking and operating-point behavior again diverged. A family could rank above benign traffic while producing no useful recall at a transferred threshold, and family-specific prevalence changed the interpretation of PR-AUC. Results therefore remain family-, learner-, support-, metric-, and threshold-specific. They do not constitute a universal zero-day score.

**Figure 6. Eligible-family ranking and balanced-threshold recall.** Two-panel conceptual exhibit using the approved ROC-AUC interval and balanced-recall figures; Infiltration is labeled descriptive.

**Table 5. Frozen conclusion-stability classification for eligible families.**

| Family | Frozen synthesis | Required qualification |
| --- | --- | --- |
| DDoS | Strong ranking retained for both learners | Eligible benchmark family; not arbitrary zero-day proof |
| Web Attack | Ranking retained for both learners | Magnitude and threshold behavior remain learner-specific |
| Port Scan | Qualitative conditions retained across seeds | Ranking magnitude is learner-dependent |
| Bot | Learner-dependent | Threshold detection remains weak under frozen points |
| Infiltration | Descriptive only | Held-out positive support = 36 |

### 5.8 Seed and Control Stability

The final stability program completed all 108/108 preregistered new fits, reused 12 frozen artifacts as declared, and left no planned execution outstanding. Completion is a governance result, not an expansion of inferential scope. No best seed was selected, no seed-plus-bootstrap interval was manufactured, and the Stage22 target remained the historically opened shared population rather than a new blind holdout.

The principal temporal ordering survived all evaluated seeds, and DDoS, Port Scan, and Web Attack met the frozen qualitative conditions for both learners. Bot remained learner-dependent, and Infiltration remained descriptive. The random LOAO controls were mixed and family-specific. They strengthened the conclusion that novelty difficulty and chronology can interact, while preventing the stronger claim that chronology alone explains the observed results.

Across the program, seed stability therefore changed the status of some conclusions from single-realization observations to findings supported within a finite frozen seed set. It did not resolve bridge restrictions, prevalence assumptions, low support, unsupported backends, or causal mechanisms.

### 5.9 Integrated Validity Matrix

Table 6 integrates the validation chain without treating unlike quantities as commensurable. Each row identifies the question, the principal observation, what survived, what did not, and the interpretation ceiling. The table is a synthesis of frozen evidence rather than a new empirical score.

**Table 6. Integrated native-metric validity matrix.**

| Validity axis | What it tests | Principal observation | What survived | What did not survive | Establishes | Does not establish |
| --- | --- | --- | --- | --- | --- | --- |
| Benchmark/reference | Performance under the processed conventional split | Strong F1 and ranking for selected tree ensembles | Within-reference discrimination | Inference to chronology, transfer, or deployment | A credible benchmark reference | Validated operational capability |
| Duplicate/split | Whether evaluation roles are traceable and disjoint under frozen rules | Reference memberships were disjoint; later development/final roles were separately governed | Explicit membership separation | Proof of latent-session independence | Auditable role separation | Absence of all semantic dependence |
| Temporal | Whether ranking and thresholds transfer forward in time | Chronological ranking exceeded random ranking across the frozen seeds; thresholds transferred poorly | Directional ranking contrast | Operating-point transfer and a sole causal mechanism | Validation-geometry sensitivity | Universal temporal superiority or proven drift |
| Shortcut | Whether conclusions persist under feature interventions and controls | Subset effects depended on split and learner; placebos also interacted | Empirical sensitivity to representation | A universal removal benefit or identified leakage cause | Conditional shortcut sensitivity | Causal explanation of transfer failure |
| Cross-dataset | Whether evidence transfers between benchmark domains | Forward bridge retained ranking; reverse bridge was near baseline | Direction-specific forward signal | Symmetric portability and cancelled cells | Bridge-specific directional transfer | Generalization to arbitrary datasets |
| Prevalence/operational | Whether frozen rates remain useful under rare-event and workload assumptions | PPV, workload, yield, and cost preference diverged | Transparent scenario translation | A universal operational winner | Assumption-explicit decision consequences | Field-validated SOC utility |
| Computational | Whether compatible paths are feasible on recorded hardware | Backend advantage varied sharply by model path | Measured component feasibility | Complete backend coverage and universal timing | Hardware-specific deployment evidence | End-to-end or hardware-independent cost |
| Unseen family | Whether an eligible withheld family can be ranked/detected | Several families transferred; others were learner-dependent or low support | Selected family-specific capability | Uniform zero-day detection | Eligibility-gated novelty evidence | Detection of arbitrary future attacks |
| Seed/control | Whether central directions depend on one realization | Temporal direction and several family outcomes were stable; controls remained mixed | Selected conclusion stability | Population guarantees and one causal story | Finite-realization robustness | Universality beyond frozen seeds |

## 6. Discussion

### 6.1 Benchmark Performance Is Not Deployment Evidence

The reference experiment answers a legitimate but limited question. Given the processed binary representation, frozen stratified memberships, validation-selected models, and validation-selected operating points, the selected tree ensembles discriminate the held-out benchmark labels well. That result survives as the reference condition; later evidence does not invalidate its arithmetic or make benchmark evaluation useless.

What changes is the scope of the inference. The forward temporal target, feature-subset controls, reciprocal dataset bridge, low-prevalence projections, hardware profiles, and withheld-family tests each alter a different part of the claim. A ranking may survive while its threshold does not. A model may transfer in one dataset direction but not the reverse. A projected stream may have high PPV but exceed analyst capacity. A family withheld from development may remain easy for both learners, while a different family becomes learner-dependent. “Benchmark performance” is therefore an observed property of a specified evaluation system; “validated capability” requires evidence under the validity condition named in the claim.

This distinction also prevents a universal negative reading. The evidence includes strong reference performance, high forward ranking under chronological development, meaningful IDS2018-to-CICIDS2017 transfer, and strong withheld-family discrimination for DDoS and Web Attack. The contribution is not that the detector ceased to work whenever validation became harder. It is that the conclusions became axis-, population-, metric-, and operating-rule-specific.

### 6.2 Temporal and Shortcut Effects

The temporal result reverses a simplistic expectation that random membership must provide an optimistic but still directionally similar estimate. Under the shared forward target, chronological development produced stronger ranking across every evaluated seed. Yet that result coexisted with poor threshold transfer. The likely scientific lesson is not “chronological is always better,” but that validation geometry can change both which patterns are learned and how score scales move between development and target populations.

The shortcut audit narrows, but does not eliminate, possible explanations. Feature removals, behavior-restricted inputs, and depth-one controls show that some predictors carry split-specific discrimination. However, matched-size placebo removals also interact with split geometry, and chronological family composition differs from random composition. Those counterexamples block a claim that a named shortcut caused the temporal or cross-dataset result. Temporal separation and shortcut sensitivity are connected evaluation concerns, but neither is a proven causal explanation for the other.

Explanation reliability reinforces the same discipline. LIME perturbation stability was compatible with poor local surrogate fidelity. A stable account of a local decision can therefore remain inaccurate. The implication is methodological: explanation studies should report reconstruction or fidelity diagnostics, distinguish exact decompositions from surrogate approximations, and avoid interpreting consistency alone as validity.

### 6.3 Transferability Is Conditional and Asymmetric

The bidirectional bridge shows why cross-dataset validity should be a directional statement. IDS2018-trained models retained useful ranking on the CICIDS2017 target under the primary shared-feature contract, whereas reciprocal models evaluated on the IDS2018 target were close to their baseline anchors. This is not a software discrepancy to be averaged away. The directions use different source models, prevalence, collection periods, and target roles; their asymmetry is evidence about portability under those contracts.

Feature semantics further condition the result. Correcting aggregate-flag serialization changes PR-AUC, ROC-AUC, and Brier score in different directions. A larger bridge is therefore not automatically a better bridge, and nominally matching columns do not guarantee matching semantics. The two cancelled GROUNDED_S4 cells add a governance constraint: when durable exact membership is unavailable, refusing a post-freeze heuristic protects interpretation at the cost of an incomplete sensitivity analysis.

Accordingly, the transfer result supports neither universal compatibility nor universal incompatibility between the benchmark families. It supports substantial forward ranking, weak reverse ranking, metric-specific serialization sensitivity, and explicit uncertainty about unexecuted cells. External validity beyond these datasets remains open.

### 6.4 Ranking Quality and Operating-Point Utility Are Distinct

Ranking and operating-point utility diverge repeatedly across the evidence chain. Chronological tree ensembles ranked the shared forward population substantially better than random ensembles but almost never fired at the transferred development thresholds. Cross-dataset and leave-one-family-out analyses produced similar cases in which useful ranking did not imply useful recall or FPR at a fixed operating point.

The distinction follows from what each quantity measures. ROC-AUC and PR-AUC describe ordering across thresholds. Precision, recall, F1, and FPR describe one selected point on a score scale. PPV and workload then place that operating point inside a prevalence and traffic scenario. A change in score calibration or prevalence can therefore leave ranking intact while rendering a threshold unsuitable, or produce manageable alert volume only because true detection is negligible.

This layered interpretation is more actionable than a single performance verdict. A system with transportable ranking may support recalibration or threshold governance in a prospective deployment, but such adaptation must be evaluated on new, appropriately governed data. The present study did not perform target-guided recalibration and therefore does not claim the performance that adaptation might achieve.

### 6.5 Novel-Family Performance Is Family- and Learner-Dependent

Withholding an attack family did not yield one novelty outcome. DDoS and Web Attack retained strong ranking for both learners. Port Scan met the frozen stability conditions but showed a large learner difference. Bot was learner-dependent and weak at the frozen operating points. Infiltration remained too weakly supported for inferential use, and two additional families could not satisfy the chronological eligibility rule. This heterogeneity is scientifically preferable to an aggregate zero-day score because it reveals where the conclusion changes.

Zero training exposure is a controlled benchmark condition, not a definition of real-world zero-day detection. Related families, shared infrastructure, extractor cues, and benchmark construction may still provide transferable information. Conversely, novelty can be confounded with chronology, support, and target prevalence. The random LOAO controls help separate some of these factors, but their mixed family-specific outcomes do not identify a universal mechanism.

Future novelty evaluations should therefore publish eligibility before model results, preserve family-level support, report ranking and frozen-threshold behavior separately, include more than one learner or realization where feasible, and distinguish descriptive from inferential families. Strong transfer for some families should remain visible because it prevents an exaggerated claim that supervised models cannot recognize any unseen category.

### 6.6 Implications for IDS Evaluation Practice

The framework suggests a sequence of claim checks rather than a mandatory model architecture. First, define the reference population and show how preprocessing, rebalancing, duplicate handling, and operating-point selection affect the benchmark claim. Second, evaluate chronology and target roles without treating temporal contrasts as automatically causal. Third, audit plausible shortcut features with placebos or other controls. Fourth, test domain transfer in both directions under explicit semantic bridges. Fifth, translate fixed rates under realistic prevalence, traffic, workload, and cost assumptions. Sixth, profile the actual inference component on declared hardware. Seventh, gate novelty evaluation by family eligibility and support. Finally, test whether central conclusions survive multiple model realizations and appropriate controls.

These checks should remain modular. A temporal result cannot substitute for cross-dataset evidence; a deployment profile cannot validate PPV; a feature ablation cannot prove causality; and a family-withholding result cannot establish detection of arbitrary attacks. Native metrics and uncertainty types should remain visible, especially when they point in different directions.

Protocol governance is equally important. Feature contracts, model scope, operating points, target roles, and interpretation rules should be fixed before target evidence is used. Cancelled analyses should be reported rather than silently replaced. Reused targets should not be presented as fresh blind holdouts. Finally, every paper-facing number and substantive claim should resolve to a frozen artifact and a disclosed limitation. These practices do not eliminate benchmark constraints, but they make the resulting claims auditable and appropriately bounded.

## 7. Limitations

The study has material limitations that constrain both its empirical scope and its reproducibility claim.

### 7.1 Dataset and provenance limitations

**Benchmark-family scope.** The empirical chain centers on CSE-CIC-IDS2018 and a restricted CICIDS2017 bridge, both from the same broad research ecosystem. It does not include live enterprise, cloud, ISP, industrial, or IoT traffic. This prevents claims of portability to arbitrary operational networks.

**Processed reference condition.** The initial reference uses a processed, rebalanced binary IDS2018 table and a stratified split. It supports controlled comparison but does not reproduce natural prevalence, session structure, or forward chronology. This prevents the high reference metrics from serving as direct deployment evidence.

**Bridge restriction.** Cross-dataset conclusions depend on frozen shared-feature contracts, preprocessing, source learners, and direction-specific target roles. Nominally similar fields can differ in extractor semantics. This prevents bridge-independent or symmetric portability claims.

**Cancelled membership cells.** Two GROUNDED_S4 cells were cancelled because exact physical-row membership could not be recovered without a new heuristic. Governance avoided an adapted substitute but left the intended sensitivity incomplete. This prevents a claim that every preregistered cross-dataset cell was executed.

**Unavailable external artifacts.** Raw datasets are not redistributed, and some historical models, probabilities, explanation arrays, or source relationships are unavailable or intentionally closed. Frozen summaries, hashes, schemas, and provenance mitigate but do not eliminate this gap. This prevents complete regeneration of every early result.

**Source-restricted graph evidence.** The graph experiment is limited to an endpoint-authenticated February 20 source; equivalent topology is not available across the main tabular benchmark, and unseen topology was not estimable. This prevents claims of graph deployment readiness, general unseen-host transfer, or interchangeability with the full reference evaluation.

**Descriptive architecture comparison.** The Stage21 CNN/ViT result is one frozen comparison under a shared restored target, not a replicated architecture trial. This prevents universal claims that either architecture is superior.

### 7.2 Protocol and scope limitations

**Temporal/family entanglement.** Chronological memberships also change attack-family composition, and the available controls are mixed and family-specific. This prevents attribution of the temporal contrast solely to concept drift or chronology.

**LOAO eligibility.** DOS and AUTH_BRUTE_FORCE cannot satisfy the frozen day-atomic development/target ordering. Their ineligibility narrows the family scope and prevents uniform claims across the benchmark taxonomy.

**Low-support Infiltration.** The Infiltration target contains 36 positives. It remains descriptive even though the fold is executable. This prevents inferential claims for that family and prevents its use as primary pooled evidence.

**Historically reused target.** The Stage28 temporal stability analysis re-evaluates the already historically opened Stage22 shared target. The reuse was preregistered and governed, but the population is not a new blind external holdout. This prevents a claim of independent blind replication.

### 7.3 Statistical limitations

**Conditional resampling uncertainty.** Historical paired bootstrap intervals are conditional on frozen samples, arrays, and implementations. They describe uncertainty within those target populations, not unconditional deployment variation. This prevents broad population significance claims.

**Finite seed scope.** Stability is evaluated over a finite frozen seed set, and the full hyperparameter search is not repeated for every seed. The results support fixed-recipe realization stability, not HPO-process robustness or a population guarantee. Directional 5/5 results are descriptive rather than significance tests.

### 7.4 Operational-assumption limitations

**Prior-probability shift.** Stage25 holds sensitivity and FPR fixed while prevalence changes. Real deployments may also change features, protocols, topology, users, attackers, and extraction behavior. This prevents the projections from being interpreted as observed field performance.

**Workload and cost scenarios.** Traffic volume, analyst service time, capacity, and relative error costs are frozen analytic assumptions rather than organization-specific measurements. This prevents universal workload, utility, or economic recommendations.

### 7.5 Computational limitations

**Hardware and component boundary.** Stage26 measures compatible inference components on one recorded hardware/software environment. It omits complete capture-to-alert latency, and some backends are unsupported. This prevents universal speed, throughput, energy, or end-to-end deployment claims.

### 7.6 Reproducibility limitations

**Historical environment ambiguity.** Some dependencies and execution environments remain `VERSION_NOT_PROVEN`; adjacent receipts are not generalized to unrecorded runs. This prevents bit-for-bit historical environment reconstruction for every stage.

**Incomplete full-rerun reproducibility.** The repository provides strong static provenance, scalar evidence, configs, canonical methods, archived sources, and equivalence tests, but many scientific paths cannot be rerun end to end without external data or closed artifacts. This prevents a claim that all results are locally regenerable even though the manuscript evidence chain is auditable.

## 8. Conclusion

The progressively stronger validation chain produced a bounded answer rather than a universal verdict. Strong discrimination survived under the processed reference condition. The central chronological-over-random ranking direction survived across the frozen model realizations, meaningful ranking survived in the forward cross-dataset bridge, several eligible withheld families transferred strongly, and compatible inference paths were computationally feasible on the measured hardware.

Other inferences did not survive uniformly. Frozen operating thresholds transferred poorly even when ranking remained useful. Cross-dataset portability was asymmetric. Shortcut interventions were split- and learner-dependent and did not identify one causal leakage mechanism. Low-prevalence PPV, workload, yield, and relative-cost preference diverged under the frozen operational assumptions. Unseen-family outcomes varied by family, learner, support, metric, and threshold.

The resulting discipline is straightforward: define the population and target roles; separate benchmark, temporal, shortcut, domain, prevalence, computational, novelty, and realization validity; report ranking and operating-point behavior independently; preserve native metrics and negative results; lock target-facing choices before evaluation; disclose cancelled and low-support analyses; and connect every claim to frozen evidence and limitations. This does not show that machine-learning intrusion detection is useless or that benchmark research is invalid. It shows that deployable capability is a stronger, more conditional claim than benchmark performance, and it specifies the evidence needed to make that claim responsibly.

## References

The canonical verified bibliography for the Pandoc-style citation keys used in this manuscript is `manuscript/references.bib`. Claim-level citation coverage, source quality, and bibliography changes are recorded in `docs/manuscript/pass2/`.

## Supplementary Material Plan

The supplementary package should preserve the evidence required for audit without reproducing the repository in the main paper:

- complete baseline inventories, tuning records, threshold curves, holdout confusion matrices, paired uncertainty, calibration, known-category support, and fixed-recipe seed tables;
- full explanation-reliability analyses, representative local cases, Integrated Gradients sensitivity, attention diagnostics, source-restricted graph evidence, and descriptive CNN/ViT comparison;
- temporal membership, duplicate-sanitization, development-cell, frozen-threshold, and target-opening receipts;
- all shortcut subsets, matched placebos, stump controls, component attribution summaries, family composition, and secondary operating metrics;
- bridge specifications, direction-specific cross-dataset tables, flag-serialization sensitivity, threshold transfer, population/governance tables, and GROUNDED_S4 cancellation receipts;
- complete prevalence grids, PPV/NPV thresholds, alert/workload/capacity scenarios, relative-cost decisions, and sanity checks;
- full warm/cold inference, throughput, memory, package, capacity, representation, Pareto, CPU/GPU, and backend-status profiles, with hardware receipts;
- complete LOAO family metrics, conditional intervals, similarity diagnostics, eligibility records, seed-level stability, and random-control tables;
- configs, environment records, immutable notebook/script archives, source maps, hashes, equivalence matrices, reproduction indexes, execution boundaries, and static validation reports.

Supplementary inclusion does not change evidence status. Cancelled analyses remain cancelled, descriptive results remain descriptive, hardware measurements remain hardware-specific, and conditional uncertainty remains conditional.
