# Stage26 Paper-Facing Deployment Narrative

**Frozen scientific source:** `9e8354ecc9cfa72c28aa037e5d2053de422bf7a2`

**Status:** Derived manuscript-support artifact. This document does not replace
the frozen measurement tables and does not constitute a new experiment.

## Deployment Profiling Boundary

Deployment efficiency was evaluated independently of predictive discrimination.
Warm inference used frozen model artifacts and prepared model inputs, with the
timed boundary extending from prepared input to a materialized attack-probability
output. CPU profiling used fixed physical-core configurations, whereas GPU
profiling used a prospectively selected single NVIDIA Tesla T4 with device
synchronization before and after every timed region. Timing and memory runs were
separate. These measurements therefore describe **component-level inference**;
they are not complete extraction-to-decision IDS latency or throughput
measurements.

## Accuracy-Latency Context

Within the duplicate-safe 70-feature comparison group, XGBoost, LightGBM, and
CatBoost were descriptive CPU frontier members. Their frozen PR-AUC values were
0.945385, 0.946606, and
0.943045, respectively, with batch-1 CPU1 p95 inference
latencies of 0.593711,
0.648760, and
0.239195 ms. The five-checkpoint FT
Transformer ensemble had lower PR-AUC (0.929572) and higher
batch-1 CPU1 p95 latency (11.302716 ms)
and was not a Group-A frontier member.

The packet-image models form a separate comparison group. Within Group B, the
masked ViT achieved higher PR-AUC (0.606537) and lower batch-1
CPU1 p95 latency (2.105199 ms) than the
masked CNN (PR-AUC 0.489453; p95
9.532039 ms). The ViT was therefore the
descriptive Group-B frontier member. No cross-group Pareto comparison is made.

## CPU-GPU Deployment Behavior

GPU acceleration was architecture- and batch-dependent rather than universal.
At batch size 1, the masked CNN showed the largest immediate GPU benefit: p95
component-level latency decreased from 9.532039 ms on
CPU1 to 0.877846 ms on the T4, a
10.86x point-estimate ratio. The FT
Transformer ensemble also benefited at B=1, decreasing from
11.302716 to 5.821576 ms
(1.94x). The masked ViT was close
to parity, with CPU1 and GPU p95 latencies of
2.105199 and 2.007975 ms,
respectively (1.048x).

The profiled tree models showed the opposite low-batch pattern. XGBoost
recorded 0.593711 ms on CPU1 and
2.291162 ms on the T4, corresponding to approximately
3.86x lower p95
latency on CPU1. CatBoost recorded 0.239195 ms on
CPU1 versus 1.478441 ms on the T4, or approximately
6.18x lower p95
latency on CPU1.

Batching changed these relationships. XGBoost remained CPU-favorable at B=64
with a CPU1/GPU p95 ratio of
0.299, reached near crossover at
B=256 (1.023), and became
increasingly GPU-favorable at B=1024 and B=8192
(3.257x and
12.405x). CatBoost crossed much
later: its ratio remained 0.986
at B=1024 and reached
1.242 at B=8192.

The neural models benefited earlier from parallel execution. The FT ensemble
reached point-estimate p95 ratios of
34.52x,
37.89x, and
49.06x at B=64, B=256, and
B=1024. The masked CNN reached
89.90x at B=64 and
100.51x at B=256. The masked
ViT moved from near parity at B=1 to
26.75x,
42.40x, and
58.72x at B=64, B=256, and
B=1024. These hardware ratios are descriptive point estimates; ratio-level
confidence intervals were not computed.

## Memory and Backend Constraints

GPU feasibility also depended on accelerator memory. The masked ViT remained
measurable at B=8192 while reaching approximately
10770.00 MiB of maximum observed delta peak
GPU process memory. The masked CNN reached approximately
7810.00 MiB at its largest successful
condition, B=1024, and produced a genuine
`RESOURCE_LIMIT_OOM` at B=8192. The FT ensemble reached approximately
2462.00 MiB, whereas XGBoost and CatBoost
required only approximately 24.00 MiB
and 12.00 MiB of maximum observed delta
peak process memory, respectively.

The frozen LightGBM artifact did not expose a contract-approved native GPU
inference route under the no-conversion/no-substitution policy. Its GPU
conditions were therefore retained as `BACKEND_UNAVAILABLE`. Because the
operational LightGBM+XGBoost ensemble requires both constituent probability
outputs, that complete GPU ensemble path was also `BACKEND_UNAVAILABLE`.
Neither outcome should be interpreted as a latency comparison.

## Deployment Interpretation

The deployment results do not support a hardware-independent "fastest model."
Instead, they identify distinct operational regimes. The Group-A tree models
combine strong predictive discrimination with very low single-flow CPU latency,
making CPU execution attractive for low-batch online operation. XGBoost becomes
GPU-favorable as batching increases, whereas CatBoost crosses only at the
largest measured batch. The neural models exploit GPU parallelism much earlier,
but their deployment value must still be considered jointly with predictive
performance and memory demand. In Group B, for example, the masked CNN showed
stronger GPU acceleration but lower frozen PR-AUC than the masked ViT and
encountered an accelerator-memory ceiling at B=8192.

Accordingly, IDS deployment decisions should jointly consider model
representation, predictive performance, expected batching regime, backend
availability, latency requirements, and accelerator-memory budget rather than
accuracy or accelerator availability in isolation.

## Interpretation Boundaries

The following restrictions remain part of the frozen Stage26 interpretation:

1. Deployment measurements are component-level, not complete E2E IDS latency.
2. Group-A and Group-B Pareto results must remain separate.
3. CPU/GPU speedup ratios are point estimates; ratio CIs were not computed.
4. No missing deployment cost is imputed for OOM, timeout, or unavailable
   backends.
5. Frozen batch sizes are descriptive measurement conditions, not post-hoc
   optimized batch sizes.
6. The single-T4 measurements should not be generalized to other accelerator
   architectures without additional hardware-specific profiling.
