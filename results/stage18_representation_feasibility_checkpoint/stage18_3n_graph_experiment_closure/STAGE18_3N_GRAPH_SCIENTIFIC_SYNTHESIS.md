# Stage 18.3N — Graph Experiment Scientific Synthesis

## Final representation decision

**SUPPORTED_WITH_CONSTRAINTS**

The graph representation is scientifically supportable only for the endpoint-rich **20 February 2018** capture. It is a separate source-restricted experiment and is not a replacement for the full ten-file tabular benchmark.

## Chronological protocol

| Partition | Period | Attack examples |
|---|---|---:|
| Train | 01:00–08:59 | 797 |
| Validation | 09:00–10:59 | 423,621 |
| Final holdout | 11:00–12:59 | 151,773 |

The final holdout was opened exactly **once** and is now permanently closed.

## Final model comparison

| Metric | EdgeOnlyMLP | Graph Transformer |
|---|---:|---:|
| Validation PR-AUC | 0.674118865 | 0.983875570 |
| Final holdout PR-AUC | 0.429769732 | 0.973595392 |
| Validation ROC-AUC | 0.911349895 | 0.998209858 |
| Final holdout ROC-AUC | 0.908980904 | 0.998676640 |
| Frozen threshold | 0.01 | 0.01 |
| Validation F1 | 0.809961389 | 0.002173667 |
| Final holdout F1 | 0.655987784 | 0.000000000 |
| Final holdout recall | 0.868975378 | 0.000000000 |

## Validation-to-holdout stability

### EdgeOnlyMLP

- PR-AUC delta: -0.244349133
- ROC-AUC delta: -0.002368990
- F1 delta: -0.153973605
- Recall delta: +0.004858632

### Graph Transformer

- PR-AUC delta: -0.010280179
- ROC-AUC delta: +0.000466782
- F1 delta: -0.002173667
- Recall delta: -0.001088237

## Scientific interpretation

The Graph Transformer retained exceptionally strong threshold-free discrimination on the untouched final chronological holdout. Its PR-AUC declined only from **0.9839** on validation to **0.9736** on holdout, while ROC-AUC remained approximately **0.999**.

However, ranking performance and operational classification performance diverged sharply. The precommitted validation-selected threshold was **0.01**, the minimum of the frozen search grid. At that unchanged threshold, the final Graph Transformer ensemble produced **zero true-positive detections among 151,773 holdout attacks**.

This discrepancy must be preserved as a result. Thresholds below 0.01, probability recalibration, retraining, or architecture changes after the holdout are not scientifically permissible within this experiment.

The EdgeOnlyMLP showed substantially weaker threshold-free ranking on the final holdout but retained useful thresholded detection, with final F1 **0.6560** and recall **0.8690**.

The Graph Transformer therefore demonstrates substantial **ranking utility**, but this experiment does not support a claim of **deployment-ready operational superiority**.

## Topology-generalization limitation

All attack examples in the final holdout occurred on hosts and directed host pairs previously observed during training.

- Attacks involving an unseen host: **0**
- Attacks on an unseen directed edge: **0**

Attack generalization to unseen topology is therefore **not estimable** from this experiment.

## Comparison boundary

The Graph Transformer exceeds the EdgeOnlyMLP on final-holdout PR-AUC by **+0.543825660**.

This difference is descriptive rather than causal. The models differ architecturally as well as in their access to graph context, so the result must not be presented as a causal estimate of graph structure alone.

## Publication-safe primary conclusion

For the endpoint-rich 20 February 2018 capture, an authentic host-communication graph representation was scientifically supportable and produced strong threshold-free discrimination under a separately frozen chronological protocol. The three-seed Graph Transformer achieved a validation PR-AUC of 0.9839 and retained a final-holdout PR-AUC of 0.9736, compared with 0.4298 for the edge-only control on the same final period. However, the Graph Transformer's frozen validation-selected operating threshold did not transfer operationally: at threshold 0.01 it detected none of the 151,773 holdout attacks. Accordingly, the experiment supports graph-based ranking utility but does not support a claim of deployment-ready thresholded superiority.

## Publication-safe limitation

This graph experiment is restricted to the 20 February capture because the remaining source files do not retain equivalent authenticated endpoint metadata. Furthermore, all positive examples in both validation and final holdout occurred on host identities and directed communication pairs already observed during training, so attack detection on unseen topology could not be estimated. The paired Graph Transformer/edge-only comparison is therefore descriptive and must not be interpreted as a causal estimate of graph context alone.

## Prohibited interpretations

- The Graph Transformer is deployment-ready.
- The Graph Transformer provides superior operational attack detection at its frozen threshold.
- Graph context causally caused the PR-AUC improvement.
- The experiment demonstrates attack generalization to unseen hosts.
- The experiment demonstrates attack generalization to unseen directed edges.
- The 02-20 graph experiment directly replaces the full ten-file Stage-15/16 benchmark.
- A threshold below 0.01 would solve the Graph Transformer operating-point problem.
- Post-hoc probability calibration would preserve the validity of the frozen holdout evaluation.


## Scientific closure

- Graph Transformer models: frozen
- EdgeOnlyMLP models: frozen
- Final graph holdout openings: 1 / 1
- Future graph holdout openings: 0
- Holdout status: permanently closed
- Post-hoc threshold search: prohibited
- Post-hoc recalibration: prohibited
- Post-hoc retraining: prohibited
- Post-hoc architecture changes: prohibited
- Further Stage 18.3 performance experiments: prohibited

Stage 18.3 is scientifically complete.
