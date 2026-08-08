# Stage 18 Manuscript Integration

This document contains manuscript-ready text derived exclusively from the frozen Stage 18 representation-feasibility study.

No result in this document should be interpreted as authorization to modify the frozen experiments.

---

# A. Proposed Contribution Text for the Introduction

A further contribution of this study is a representation-first assessment of modern neural architectures for intrusion detection. Rather than assuming that a model family is applicable whenever the available predictors can be reshaped into a compatible tensor, candidate representations were evaluated against the semantics retained in the original CSE-CIC-IDS2018 sources. Temporal, vision-based, and graph-based representations were therefore treated as distinct scientific hypotheses. Temporal modeling was found to be supportable only under a separately constructed chronological protocol; Vision Transformer training was rejected because the available flow artifacts did not provide defensible two-dimensional spatial locality; and graph modeling was supported only for the endpoint-rich 20 February capture. This procedure separates architectural novelty from representation validity and avoids introducing artificial temporal order, spatial adjacency, or graph topology.

---

# B. Methods — Representation-Feasibility Protocol

## Representation-First Architecture Assessment

Before extending the benchmark to additional architecture families, we evaluated whether the source artifacts contained the structural assumptions required by each candidate model. Model performance was not permitted to justify a representation retrospectively. A candidate representation was considered supportable only when its temporal, spatial, or relational organization could be traced to information genuinely retained in the original source data.

Three architecture families were examined: Temporal/MTemporal Transformers, Vision Transformers, and Graph Transformers. The assessment followed three general constraints. First, source metadata rather than processed row position was used to establish ordering or relationships. Second, labels, model outputs, and holdout observations could not be used to define representation structure. Third, an architecture could be rejected without model fitting when the required representation semantics were absent.

### Temporal representation

The original traffic sources retained timestamp metadata with one-second resolution, establishing an authentic temporal axis. However, flows sharing the same timestamp could not be assigned a finer within-second ordering because no independently authenticated ordering variable was available. Such flows were therefore treated as simultaneous observations.

The existing Stage-15 duplicate-safe train/validation membership was audited before any temporal-window construction. Approximately **85.37%** of the authorized patterns had unambiguous temporal-bin provenance. Nevertheless, **15.55%** of distinct temporal bins contained observations assigned across the existing train and validation partitions, and **99.77%** of validation bins occurred within 30 seconds of a training bin. Consequently, the Stage-15 split was retained for the existing tabular experiment but rejected for temporal-window modeling. No Temporal or MTemporal Transformer was trained in Stage 18. A future temporal experiment would require a separately precommitted chronological development split and representation rules fixed before model fitting.

### Vision representation

Vision Transformer feasibility was evaluated before constructing any traffic image. Seven candidate representations were audited, including native network images, packet-byte images, tabular feature grids, time-feature matrices, time-port matrices, time-endpoint matrices, and source-host-by-destination-host matrices. **0/7** candidates satisfied all precommitted semantic-locality requirements.

The available artifacts contained no native image or packet-byte representation. More importantly, arbitrary arrangement of heterogeneous flow predictors into a two-dimensional grid would create spatial neighborhoods that are not present in the source semantics. Although time provides an authentic ordered dimension, neither heterogeneous feature identity nor destination-port identity supplies an intrinsic spatial axis. Endpoint matrices preserve genuine relational information, but their geometry depends on arbitrary host ordering and is more naturally expressed as a graph. Vision Transformer training was therefore not performed.

### Graph representation

Authenticated source and destination host identities were retained only in the 20 February source. For this capture, each observed flow was represented as a directed source-host to destination-host edge in a temporal multigraph. Parallel flows were preserved as separate edge events, and each graph snapshot covered a fixed non-overlapping 60-second clock interval. No node-identity embedding, numeric IP encoding, feature-similarity edge construction, artificial reverse edge, or cross-snapshot message passing was permitted.

Because endpoint metadata was not retained equivalently across the complete source collection, the graph study was treated as a separate source-restricted experiment rather than a replacement for the full tabular benchmark. The chronological graph partition used 01:00--08:59 for training, 09:00--10:59 for validation, and 11:00--12:59 as a single final holdout. Preprocessing, model architecture, class weighting, ensemble construction, and threshold-selection rules were frozen before the final holdout was opened.

A three-seed EdgeAwareDirectedGraphTransformer was compared descriptively with a three-seed EdgeOnlyMLP control using the same 70 preprocessed flow predictors. The control was included to provide an edge-feature reference point; because the model architectures differ, the comparison was not interpreted as a causal estimate of graph context alone.

---

# C. Results — Representation Feasibility

## Temporal and vision candidates

The representation audit produced different outcomes across architecture families. Temporal modeling was classified as **supported with constraints** because authentic timestamp information was available, but the existing random membership was unsuitable for leakage-safe temporal-window construction. No temporal model was fitted, and therefore no Temporal/MTemporal performance claim is made.

Vision Transformer modeling was classified as **not supported by the current artifacts**. None of the seven audited candidates provided the complete two-dimensional locality required to justify patch-based visual processing. No artificial feature image was constructed and no ViT performance experiment was conducted.

## Graph Transformer experiment

Graph modeling was classified as **supported with constraints** for the endpoint-rich 20 February source. The Graph Transformer achieved a validation PR-AUC of **0.983876**. On the untouched chronological holdout, PR-AUC remained **0.973595** and ROC-AUC reached **0.998677**. The validation-to-holdout PR-AUC change was therefore only **-0.010280**, indicating that the model retained strong ranking discrimination across the later chronological period.

The corresponding EdgeOnlyMLP control achieved a final-holdout PR-AUC of **0.429770**. The Graph Transformer therefore exceeded the control by **+0.543826** PR-AUC points on the same final period. This difference is reported descriptively rather than causally.

However, threshold-free ranking and operational classification diverged sharply. The validation-selected threshold for the Graph Transformer was 0.01, which was already the minimum of the precommitted threshold grid. When this frozen threshold was applied unchanged to the final holdout, the model produced **0 true positives among 151,773 attacks**, resulting in recall **0.000000** and F1 **0.000000**. In contrast, the EdgeOnlyMLP retained a final-holdout F1 of **0.655988** at its own frozen validation-selected operating point.

### Manuscript result table

| Representation/model | Stage-18 status | Final-holdout PR-AUC | Final-holdout ROC-AUC | Frozen-threshold F1 | Interpretation |
|---|---|---:|---:|---:|---|
| Temporal/MTemporal | Supported with constraints | -- | -- | -- | Feasible only with a new chronological leakage-safe protocol; not trained |
| Vision Transformer | Not supported by current artifacts | -- | -- | -- | No defensible native 2D representation; not trained |
| EdgeOnlyMLP control | Evaluated in graph experiment | 0.429770 | -- | 0.655988 | Weaker ranking but usable frozen operating point |
| Graph Transformer | Supported with constraints | **0.973595** | **0.998677** | 0.000000 | Strong ranking; frozen threshold did not transfer operationally |

---

# D. Discussion — Representation Validity and Model Performance

The representation-feasibility analysis demonstrates that architectural applicability should not be inferred merely from tensor compatibility. The temporal, vision, and graph candidates began from the same IDS corpus but led to three different scientific outcomes because the source data support different kinds of structure.

The temporal result illustrates the distinction between the presence of timestamps and the validity of a temporal learning protocol. Authentic time metadata was available, yet the existing train/validation allocation was strongly interleaved in time. Constructing overlapping or adjacent temporal windows from that membership would therefore risk transferring temporally neighboring information across the development partitions. Rejecting the existing split for temporal modeling avoids converting an otherwise validation-safe tabular benchmark into a leakage-prone sequential experiment.

The ViT result provides a complementary example. A 70-dimensional feature vector can mechanically be reshaped into a matrix, but doing so does not establish spatial locality. Adjacent cells in such a grid would reflect an implementation choice rather than an authenticated relationship in the network traffic. The decision not to train ViT should therefore be interpreted as a representation-validity result, not as evidence against Vision Transformers as a general model family.

The graph experiment provides the strongest positive example of representation-specific modeling. Source and destination hosts define authentic relational structure in the endpoint-rich capture, allowing graph edges to be constructed without similarity heuristics or synthetic adjacency. The Graph Transformer retained exceptionally strong ranking performance on the chronological holdout, with PR-AUC decreasing only from **0.9839** to **0.9736**. This stability is notable given the substantial chronological class-prior shift in the graph experiment.

At the same time, the experiment exposes an important distinction between ranking discrimination and operational decision performance. Despite PR-AUC **0.9736** and ROC-AUC **0.9987**, the frozen Graph Transformer operating point failed to identify any final-holdout attack. The result indicates that a model may order positive and negative examples very effectively while its absolute score scale remains unsuitable for a previously selected probability threshold. Reporting only ROC-AUC or PR-AUC would therefore give an incomplete view of deployment behavior.

We intentionally did not extend the threshold grid below 0.01 or recalibrate the Graph Transformer after observing the final holdout. Either action would convert the held-out period into an additional development set. The resulting operating-point failure is consequently retained as part of the experimental finding rather than optimized away.

---

# E. Limitations

Several limitations constrain the interpretation of the representation study.

First, Stage 18 established temporal feasibility but did not train a Temporal or MTemporal Transformer. The temporal result therefore supports a future leakage-safe experiment, not a predictive-performance comparison.

Second, ViT was not evaluated empirically because representation validity was not established. The absence of ViT performance results should not be interpreted as evidence that Vision Transformers are generally unsuitable for network intrusion detection or that all traffic-image approaches are invalid.

Third, the graph experiment is restricted to the 20 February capture because equivalent authenticated source and destination endpoint metadata were not retained across the full set of source files. Its performance should therefore not be presented as directly interchangeable with the main ten-file tabular benchmark.

Fourth, all positive examples in both the graph validation period and the final chronological holdout occurred on hosts and directed communication pairs that had already appeared during training. Attack detection involving previously unseen hosts or unseen directed edges could therefore not be estimated.

Finally, the Graph Transformer and EdgeOnlyMLP differ architecturally as well as in their access to graph context. Their performance difference is consequently descriptive and does not isolate a causal effect attributable solely to relational message passing.

---

# F. Contribution Statement for Abstract or Introduction

The study further introduces a representation-first validation framework for extending intrusion-detection benchmarks to modern architectures. Temporal, vision, and graph candidates were accepted or rejected according to structure authenticated in the original traffic sources rather than according to downstream predictive performance. This analysis supported leakage-safe temporal modeling as future work, rejected artificial ViT feature-image construction, and validated a source-restricted graph formulation whose Graph Transformer achieved final chronological PR-AUC **0.9736**, while simultaneously revealing a complete failure of its frozen deployment threshold. The findings distinguish representation validity, ranking discrimination, and operational threshold behavior as separate dimensions of IDS evaluation.

---

# G. Shorter Contribution Bullet

- **Representation-aware architecture validation:** Temporal, vision, and graph extensions were audited against authentic source semantics before training. This prevented arbitrary temporal sequencing, feature-to-image reshaping, and synthetic graph construction, while identifying a valid source-restricted graph experiment with strong ranking but poor frozen-threshold transfer.

---

# H. Publication-Safe Claims

The following claims are supported by the frozen Stage 18 evidence:

1. Authentic second-resolution temporal metadata exists in the original sources.
2. The existing Stage-15 split is unsuitable for temporal-window modeling because of strong chronological interleaving.
3. Temporal/MTemporal modeling is scientifically feasible only under a separately precommitted chronological protocol.
4. No currently available artifact supports a defensible direct ViT representation.
5. Artificial reshaping of heterogeneous flow features into images was intentionally rejected.
6. Authentic host-to-host graph structure exists in the endpoint-rich 20 February source.
7. The Graph Transformer demonstrated strong threshold-free chronological ranking.
8. The frozen Graph Transformer threshold did not provide usable final-holdout attack detection.
9. Graph-versus-edge-only performance differences are descriptive rather than causal.
10. Attack generalization to unseen graph topology was not estimable.

---

# I. Claims That Must Not Appear in the Manuscript

1. The existing Stage-15 split is safe for Temporal/MTemporal sequence training.
2. Temporal/MTemporal predictive performance was established.
3. ViT was trained and performed poorly.
4. Vision Transformers are generally unsuitable for intrusion detection.
5. Arbitrarily reshaped flow features constitute a valid traffic image.
6. The Graph Transformer is deployment-ready.
7. The Graph Transformer achieved operational superiority at its frozen threshold.
8. Graph context causally produced the PR-AUC improvement.
9. The graph experiment demonstrates attack generalization to unseen hosts or unseen directed edges.
10. The endpoint-rich graph experiment replaces the full ten-file tabular benchmark.
11. A threshold below 0.01 would necessarily solve the Graph Transformer operating-point failure.
12. Post-hoc calibration using the final holdout would preserve the validity of the evaluation.

---

# J. Recommended Manuscript Placement

The material should be distributed across the paper rather than presented as one isolated appendix:

- **Introduction / Contributions:** Section A or F.
- **Methods:** Section B.
- **Results:** Section C and the result table.
- **Discussion:** Section D.
- **Limitations:** Section E.
- **Supplementary / reproducibility note:** Sections H and I may be retained internally to prevent claim drift during revision.

The graph experiment should remain clearly labeled as a **source-restricted chronological representation study**, separate from the primary ten-file tabular benchmark.
