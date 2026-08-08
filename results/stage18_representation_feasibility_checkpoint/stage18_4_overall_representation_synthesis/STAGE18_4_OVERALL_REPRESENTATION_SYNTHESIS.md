# Stage 18.4 — Overall Representation-Feasibility Synthesis

## Objective

Stage 18 evaluated whether additional modern model families could be supported by representations that genuinely exist in the CSE-CIC-IDS2018 source artifacts.

The governing rule was **representation before performance**. Predictive accuracy could not be used to rescue an invalid representation.

## Final decision matrix

| Representation | Decision | Training in Stage 18 | Performance established? |
|---|---|---:|---:|
| Temporal / MTemporal Transformer | **SUPPORTED WITH CONSTRAINTS** | No | No |
| Vision Transformer (ViT) | **NOT SUPPORTED BY CURRENT ARTIFACTS** | No | No |
| Graph Transformer | **SUPPORTED WITH CONSTRAINTS** | Yes | Yes, source-restricted |

---

## 18.1 Temporal / MTemporal Transformer

### Decision

**SUPPORTED WITH CONSTRAINTS**

Authentic timestamp metadata exists across the raw IDS2018 sources at one-second resolution.

However, the existing Stage-15 duplicate-safe train/validation split cannot be reused for temporal-window modeling.

Key evidence:

- Unique temporal-bin provenance rate: **85.3678%**
- Mixed Stage-15 train/validation temporal-bin rate: **15.5520%**
- Validation bins within 30 seconds of a training bin: **99.7656%**
- Same-second flow ordering: **not authenticated**
- Temporal models trained in Stage 18.1: **0**

A future temporal experiment therefore requires a separately precommitted chronological development split, simultaneous treatment of same-second flows, and exclusion of ambiguous multi-bin provenance.

No Stage-18 temporal-performance claim is permitted.

---

## 18.2 Vision Transformer

### Decision

**NOT SUPPORTED BY CURRENT ARTIFACTS**

Seven candidate representations were audited and **0/7** passed all precommitted semantic-locality requirements.

The available artifacts contain:

- no native network images,
- no packet-byte image tensors,
- no native PCAP-derived image representation,
- no defensible two-dimensional geometry among the heterogeneous 70 flow predictors.

Time provides an authentic ordered dimension, but feature identity, endpoint ordering and destination-port identity do not provide intrinsic spatial neighborhoods suitable for arbitrary ViT patch geometry.

Consequently, no feature-grid image, endpoint image or other artificial spatial representation was constructed.

ViT models trained: **0**.

This is a representation-feasibility result, not evidence that Vision Transformers generally perform poorly for intrusion detection.

---

## 18.3 Graph Transformer

### Decision

**SUPPORTED WITH CONSTRAINTS**

Graph representation is authentic only for the endpoint-rich **20 February 2018** capture.

Each observed flow was represented as a directed source-host to destination-host edge within an independent 60-second temporal snapshot.

### Final chronological evidence

| Metric | EdgeOnlyMLP | Graph Transformer |
|---|---:|---:|
| Final holdout PR-AUC | 0.429769732 | **0.973595392** |
| Final holdout ROC-AUC | 0.908980904 | **0.998676640** |
| Frozen-threshold F1 | **0.655987784** | 0.000000000 |
| Frozen-threshold recall | **0.868975378** | 0.000000000 |

The Graph Transformer retained extremely strong threshold-free discrimination from validation to the untouched final holdout:

- Validation PR-AUC: **0.983875570**
- Holdout PR-AUC: **0.973595392**
- PR-AUC change: **-0.010280179**

However, the frozen validation-selected threshold of **0.01** failed operationally on the final holdout:

- Holdout attacks: **151,773**
- True positives: **0**
- Recall: **0.000000000**
- F1: **0.000000000**

The Graph Transformer therefore provides strong evidence of **ranking utility**, but not deployment-ready thresholded superiority.

No post-hoc threshold search, recalibration or retraining is scientifically permitted.

---

## Cross-representation conclusion

The representation-feasibility study showed that modern IDS architectures must be matched to structure genuinely present in the source data rather than imposed through arbitrary transformation. Temporal modeling was supported with constraints because authentic second-resolution timestamps exist, although a new chronological leakage-safe development split is required. Vision Transformer training was not supported because no available artifact provided defensible two-dimensional patch locality. Graph modeling was supported with constraints for the endpoint-rich 20 February capture, where a frozen Graph Transformer retained very strong final-holdout ranking (PR-AUC=0.9736, ROC-AUC=0.9987) but failed at its precommitted threshold, producing zero true-positive holdout detections. These results demonstrate why representation validity, ranking discrimination and operational threshold performance should be evaluated as distinct scientific questions.

## Methods implication

Candidate representation families were evaluated before performance-based experimentation. A representation was authorized only when its temporal, spatial or relational structure could be traced to authentic source semantics. Artificial tabular-to-image reshaping, invented endpoint ordering, feature-similarity graphs and leakage-prone temporal reuse were prohibited. This representation-first procedure allowed architectures to be accepted, constrained or rejected without using predictive performance to justify the representation itself.

## Limitations

The temporal feasibility result does not constitute a temporal-model benchmark because Stage 18.1 intentionally performed no model fitting. The ViT result is likewise a representation-feasibility rejection rather than evidence that Vision Transformers generally perform poorly for intrusion detection. The graph experiment is restricted to the 20 February source and is not directly interchangeable with the full ten-file tabular benchmark. In addition, positive examples on unseen hosts or unseen directed edges were absent from the graph validation and final holdout, preventing estimation of attack generalization to unseen topology.

## Central methodological contribution

Stage 18 demonstrates that architecture selection in IDS research should not begin with the question:

> “Can this tensor be fed into the model?”

The relevant question is:

> “Does the source data contain the structure that the architecture assumes?”

Under that criterion:

- temporal structure was **real but required a new leakage-safe protocol**;
- image structure was **not established and was therefore rejected**;
- graph structure was **real only in the endpoint-rich source and was evaluated separately**.

This prevents model novelty from being obtained by fabricating temporal order, spatial adjacency or graph topology.

## Prohibited interpretations

- The existing Stage-15 split is safe for MTemporal sequence training.
- Temporal/MTemporal predictive performance was established in Stage 18.
- ViT was trained and performed poorly.
- Vision Transformers are generally unsuitable for intrusion detection.
- Artificial feature grids are valid images because they can be processed by ViT.
- The Graph Transformer is deployment-ready.
- Graph context causally caused the observed PR-AUC difference.
- The graph experiment demonstrates attack generalization to unseen topology.
- The source-restricted graph experiment replaces the full IDS2018 tabular benchmark.
- Ranking superiority implies thresholded operational superiority.


## Stage 18 scientific closure

- Stage 18.1 Temporal feasibility: closed
- Stage 18.2 ViT feasibility: closed
- Stage 18.3 Graph experiment: closed
- Graph holdout: permanently closed
- Further Stage 18.3 holdout access: prohibited
- Further Stage 18.3 model training: prohibited
- Stage 18 representation decisions: frozen

The next activity is manuscript integration only.
