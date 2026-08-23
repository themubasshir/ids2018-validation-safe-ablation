# [Title to be selected after Pass 1]

> **Manuscript status:** Pass 1 evidence-governed reconstruction. This document is not final and has not undergone external reference verification.

## Abstract

Machine-learning intrusion detectors are commonly evaluated through discrimination metrics on processed benchmark splits, but such performance does not by itself establish that the same capability persists under temporal separation, feature perturbation, domain transfer, rare-event prevalence, deployment constraints, or novel attack families. We present an evidence-governed validation framework that evaluates these dimensions as distinct scientific questions while preserving their native metrics and frozen operating rules. Under the conventional processed CSE-CIC-IDS2018 reference condition, the selected balanced tree ensemble achieved F1 0.9285 and PR-AUC 0.9776. That result did not translate into a uniform robustness narrative. On a shared forward target, the mean PR-AUC across the frozen seed set was 0.2599 for random-natural development and 0.6388 for chronological-natural development, with the same ordering in all 5/5 evaluated seeds; nevertheless, frozen operating thresholds transferred poorly, and controls did not isolate chronology as the sole causal mechanism. Cross-dataset ranking was also directional: the IDS2018-to-CICIDS2017 bridge achieved PR-AUC 0.667483, whereas the reciprocal bridge achieved 0.108176. Operational projections supplied a further counterexample: at 0.1% assumed attack prevalence, one operating point retained PPV 0.965572 but required 33.5 analyst-hours per day, while another produced little workload because it projected only 0.0322 true alerts per day. Unseen-family results were selective rather than uniformly negative, with several eligible families retaining stable discrimination while other outcomes depended on the learner or had insufficient support. These findings show that benchmark discrimination and validated capability are related but non-equivalent claims. The framework therefore recommends axis-specific evaluation, locked target governance, separate reporting of ranking and operating-point behavior, explicit deployment assumptions, and claim-to-artifact provenance. Conclusions remain conditional on the evaluated benchmark families, frozen feature bridges, finite seed set, projected operational assumptions, eligible attack families, and measured hardware.

## 1. Introduction

Machine-learning intrusion detection is often summarized by a small set of predictive metrics measured on a benchmark test set. Those metrics answer an important question: under a specified representation, split, model, and operating rule, how well does the fitted system distinguish the benchmark labels? A stronger inference is frequently attached to the same result—that the detector will remain useful when traffic moves forward in time, when dataset-specific cues change, when a second collection pipeline is introduced, when attacks are rare, or when an attack family was absent during development. The first claim concerns benchmark performance. The second concerns validated capability. They are not interchangeable.

Several mechanisms can break the inference between them. Random partitions may mix temporal regimes or attack-family composition in ways that a forward evaluation does not. Predictors that are discriminative inside one split can act as unstable shortcuts under another. A common feature name need not have identical semantics across datasets or extractor versions. A threshold chosen on development data can fail even when its underlying score preserves useful ranking. Precision and workload can change sharply under low attack prevalence, and computational feasibility depends on the actual inference path and hardware. Finally, withholding an attack family introduces questions of eligibility, support, learner dependence, and the distinction between ranking a family and detecting it at a frozen operating point.

These concerns are usually discussed as separate evaluation problems. Treating them independently is scientifically appropriate because their outcomes are expressed in different quantities: PR-AUC and ROC-AUC characterize ranking; precision, recall, F1, and FPR characterize a selected operating point; PPV and alert volume translate rates under prevalence assumptions; and latency, throughput, and memory describe computational behavior. What is missing from a performance-centered account is a disciplined way to connect these questions without collapsing them into an artificial robustness score or assuming that failure on one axis explains failure on another.

This work reconstructs a connected empirical validation chain around two benchmark families, CSE-CIC-IDS2018 and CICIDS2017. The chain begins with a conventional processed-data reference evaluation and then asks what remains supported under stronger or different validity conditions: source-faithful temporal partitions, shortcut-feature perturbations and controls, bidirectional cross-dataset bridges, prior-shift prevalence scenarios, hardware-specific profiling, leave-one-attack-family-out evaluation, and seed/control stability. Each target-facing analysis was governed by a frozen protocol and an explicit anti-adaptation boundary. Each conclusion is reported in its native metric and linked to the population, source artifact, configuration, code, and provenance record that support it.

The resulting evidence is neither a monotonic collapse nor a model-success narrative. The conventional reference result is strong. Chronological development produces substantially better forward ranking than random development under the evaluated protocol, but its operating thresholds still transfer poorly. Forward cross-dataset transfer retains meaningful ranking while the reverse direction is near its prevalence anchor. Some shortcut perturbations reveal strong split interactions, yet placebo perturbations prevent those interactions from being read as proof of leakage. Some eligible attack families transfer strongly across learners and seeds; others are learner-dependent, ineligible, or too weakly supported for inferential claims. Operationally, high PPV can coexist with excessive workload, while low workload can reflect negligible detection yield rather than suitability. These counterexamples are central to the validation argument because they identify which inference failed, not merely whether a model score decreased.

The manuscript makes the following contributions:

1. It defines a connected, validation-safe IDS evaluation framework in which benchmark, temporal, shortcut, cross-dataset, operational, computational, unseen-family, and realization validity remain distinct axes.
2. It provides a source-faithful temporal and operating-point audit, closed across a frozen seed set, that separates ranking stability from threshold transfer and from causal interpretation.
3. It combines a controlled shortcut-feature audit with bidirectional dataset transfer, preserving placebo evidence, directionality, bridge restrictions, and cancelled analyses.
4. It links prevalence, alert workload, relative cost, and measured computational profiles while keeping analytic assumptions and hardware boundaries explicit.
5. It evaluates zero-training-exposure attack families through eligibility-gated, family-specific results that retain learner dependence and low-support classifications rather than claiming universal zero-day detection.
6. It supplies a claim-to-provenance layer connecting manuscript statements and numbers to frozen artifacts, protocols, canonical implementations, archived sources, equivalence evidence, and known reproducibility gaps.

The contribution is therefore an evaluation discipline rather than a proposed detector. The study does not claim that machine-learning IDS is universally ineffective, that temporal splitting is always superior, that shortcut features cause all transfer failure, or that leave-one-family-out evaluation proves real-world zero-day detection. It asks a narrower and more useful question: which apparent benchmark capabilities survived each evaluated validity condition, which did not, and what remained unresolved?

## 2. Related Work

### 2.1 Benchmark-based intrusion detection

CICIDS-family datasets have supported extensive comparisons of classical learners, gradient-boosted trees, neural networks, and hybrid architectures. This literature has made benchmark experimentation accessible and has enabled controlled comparisons under shared label spaces and flow-derived features. At the same time, headline accuracy, F1, ROC-AUC, or PR-AUC values are meaningful only relative to the dataset construction, split rule, class balance, feature semantics, and target-opening protocol used to obtain them. The present study treats its processed CSE-CIC-IDS2018 result as a reference condition rather than as direct evidence of operational portability. [REFERENCE GAP: primary CSE-CIC-IDS2018 dataset citation and representative peer-reviewed benchmark-modeling studies]

The distinction between a useful benchmark and a representative deployment population is especially important for processed or rebalanced data. Rebalancing can improve experimental control and make model comparisons tractable, but it changes the class prior and does not recreate the temporal or organizational structure of live network traffic. Our framework therefore retains the conventional benchmark result while testing different validity dimensions in separate, source-governed populations. [REFERENCE GAP: methodological work on class balance, benchmark construction, and external validity in intrusion detection]

### 2.2 Split, temporal, and shortcut validity

Random train/test partitioning assumes that sampled memberships adequately represent the intended future use. In network traffic, that assumption can be weakened by repeated flows, temporally adjacent events, collection sessions, or attack families concentrated in particular periods. Chronological and session-aware evaluation have consequently been proposed as stronger tests of forward validity, although they may also change class prevalence and family composition. A temporal contrast must therefore be interpreted as a change in evaluation geometry, not automatically as a clean estimate of concept drift. [REFERENCE GAP: IDS studies on temporal splitting, session-aware validation, duplicate leakage, and chronological generalization]

Feature leakage and shortcut learning present a related but distinct problem. Ports, protocol indicators, initial-window values, timing fields, or extractor artifacts can be highly predictive without necessarily encoding transportable attack behavior. Removing a feature and observing a metric change establishes sensitivity to the intervention; it does not by itself prove that the feature was leakage or that it caused later transfer failure. Matched-size placebo removals, simple controls, family-composition checks, and attribution audits can narrow the interpretation, but causal attribution remains demanding. [REFERENCE GAP: primary studies on leakage, shortcut learning, spurious correlation, and feature-ablation methodology in network intrusion detection]

Explainability methods add a second validity layer. Global importance agreement does not guarantee reliable local explanations, and perturbation stability does not guarantee that a surrogate faithfully represents the underlying model. Exact decomposition methods and surrogate methods answer different questions and require separate fidelity checks. [REFERENCE GAP: authoritative TreeSHAP and LIME citations plus peer-reviewed work on explanation fidelity and stability]

### 2.3 Cross-dataset and operational evaluation

Cross-dataset evaluation is a common response to concerns that strong within-dataset scores reflect collection-specific structure. Yet transfer is not a single property: source and target roles, feature intersections, extractor semantics, label mappings, prevalence, and model scope can differ by direction. Reporting one direction, or averaging opposite directions with different target populations, can obscure the scientific result. The present framework therefore uses frozen semantic bridges and reports IDS2018-to-CICIDS2017 and CICIDS2017-to-IDS2018 transfer separately. [REFERENCE GAP: peer-reviewed cross-dataset IDS studies, semantic feature-alignment methods, and bidirectional transfer evaluations]

Operational evaluation introduces the base-rate problem. Sensitivity and specificity measured at benchmark prevalence do not determine deployment PPV, false-alert volume, analyst workload, or economic preference when attacks are rare. Prior-probability-shift analysis can translate frozen rates to alternative prevalence scenarios, but only under the explicit assumption that the conditional rates remain invariant. Such projections are decision-analysis tools rather than field trials. [REFERENCE GAP: intrusion-detection base-rate literature, alert-workload studies, and operational cost-sensitive evaluation]

### 2.4 Deployment, novelty, and reproducibility

Predictive performance is only one part of deployability. Latency, throughput, memory, artifact size, preprocessing boundaries, batch size, backend compatibility, and hardware can change which model is feasible in a given environment. Comparisons are most informative when the timed component and unsupported paths are explicit and when hardware-specific measurements are not generalized as universal constants. [REFERENCE GAP: peer-reviewed IDS deployment-profiling studies and reporting guidance for ML systems performance]

Evaluation on attacks absent from training is often described using novelty or zero-day terminology. Leave-one-attack-family-out protocols provide a controlled benchmark analogue, but their conclusions depend on whether a family can be separated chronologically, how many target positives exist, which learner is evaluated, and whether success is defined by ranking or a frozen threshold. They cannot establish detection of arbitrary future attacks. [REFERENCE GAP: primary IDS studies on leave-one-attack-family-out, open-set recognition, novelty detection, and zero-day evaluation]

Finally, reproducibility work in machine learning emphasizes executable methods, environment capture, provenance, target governance, and the separation of code availability from full result regeneration. Long-running empirical programs also face repeated-holdout and researcher-adaptation risks that cannot be eliminated merely by publishing code after the fact. This study addresses those risks through protocol locks, immutable source archives, explicit target-opening ledgers, equivalence receipts, and claim-level mapping, while retaining limitations where raw data, historical environments, or closed artifacts prevent complete reruns. [REFERENCE GAP: established reproducibility guidelines for machine learning and empirical cybersecurity evaluation]

## 3. Datasets and Provenance

### 3.1 CSE-CIC-IDS2018 reference and source-faithful roles

### 3.2 CICIDS2017 cross-dataset role

### 3.3 Attack-family mapping and evaluation populations

### 3.4 Provenance states and target governance

## 4. Validation Framework and Methods

### 4.1 Reference Evaluation and Governance

### 4.2 Temporal Validation

### 4.3 Shortcut-Feature Audit

### 4.4 Cross-Dataset Transfer

### 4.5 Prevalence and Operational Stress

### 4.6 Deployment Profiling

### 4.7 Leave-One-Attack-Family-Out Evaluation

### 4.8 Seed and Control Stability

### 4.9 Statistical Uncertainty and Anti-Adaptation Controls

### 4.10 Reproducibility and Provenance

## 5. Results

### 5.1 Conventional Benchmark Performance

### 5.2 Temporal Validity

### 5.3 Shortcut Sensitivity

### 5.4 Cross-Dataset Transfer

### 5.5 Prevalence and Operational Consequences

### 5.6 Deployment Characteristics

### 5.7 Unseen-Family Evaluation

### 5.8 Seed and Control Stability

### 5.9 Integrated Validity Matrix

## 6. Discussion

### 6.1 Benchmark Performance Is Not Deployment Evidence

### 6.2 Temporal and Shortcut Effects

### 6.3 Transferability Is Conditional and Asymmetric

### 6.4 Ranking Quality and Operating-Point Utility Are Distinct

### 6.5 Novel-Family Performance Is Family- and Learner-Dependent

### 6.6 Implications for IDS Evaluation Practice

## 7. Limitations

## 8. Conclusion

## References

## Supplementary Material Plan
