# Stage 26 Manuscript Draft
## Deployment-Efficiency Results, Discussion, and Limitations

> Draft generated exclusively from frozen Stage26 publication artifacts at
> commit `9e8354ecc9cfa72c28aa037e5d2053de422bf7a2`. No new inference, timing, memory profiling, model fitting,
> or corpus access was performed.

---

## A. Deployment Profiling Protocol and Claim Boundary

Deployment cost was evaluated separately from predictive discrimination.
Warm inference measurements used frozen model artifacts and prepared model
inputs, with the primary inference boundary defined as the interval from
prepared model input to a materialized attack-probability output. CPU profiling
was performed under fixed one- and two-physical-core conditions, while GPU
profiling used a prospectively selected single NVIDIA Tesla T4. GPU timing used
device synchronization before and after every timed region. Timing and memory
measurements were executed separately.

The deployment analysis is therefore **component-level rather than complete
end-to-end**. Raw packet extraction, representation construction, and model
inference were not combined into an additive full-pipeline latency estimate.
Accordingly, the results below should not be interpreted as measurements of
complete IDS throughput.

---

## B. CPU Accuracy–Latency Trade-off

Within the duplicate-safe 70-feature comparison group, the descriptive CPU
point-estimate frontier contained XGBoost, LightGBM, and CatBoost. LightGBM
provided the highest frozen PR-AUC (0.946606), followed closely by
XGBoost (0.945385) and CatBoost (0.943045). Their
batch-1 CPU1 p95 component-level latencies were
0.648760 ms,
0.593711 ms, and
0.239195 ms, respectively.

The five-checkpoint FT Transformer ensemble achieved a lower frozen PR-AUC
(0.929572) and a substantially higher batch-1 CPU1 p95 latency
(11.302716 ms); it was therefore not a member
of the Group-A descriptive frontier.

The packet-image models were evaluated only within their separate Group-B
comparison population. In this group, the masked ViT achieved both higher
frozen PR-AUC (0.606537) and lower batch-1 CPU1 p95 latency
(2.105199 ms) than the masked CNN
(PR-AUC 0.489453; p95
9.532039 ms). Thus, the masked ViT was the
Group-B descriptive frontier member, whereas the masked CNN was not.
No cross-group Pareto comparison is made.

---

## C. Batch-1 CPU-versus-GPU Inference

The batch-1 results show that GPU execution was **not universally beneficial**.

The largest immediate acceleration was observed for the masked CNN. Its p95
latency decreased from 9.532039 ms on CPU1 to
0.877846 ms on the T4, corresponding to a
10.86x point-estimate GPU advantage.
Median throughput increased from
132.04 to
1263.09 flows/s.

The five-checkpoint FT Transformer ensemble also benefited at batch size 1.
Its p95 latency decreased from 11.302716 ms to
5.821576 ms, a
1.94x point-estimate improvement.

The masked ViT was close to parity at batch size 1. CPU1 p95 latency was
2.105199 ms and GPU p95 latency was
2.007975 ms, yielding only a
1.048x point-estimate GPU advantage.

In contrast, the two profiled tree models favored CPU execution at batch size
1. XGBoost recorded 0.593711 ms on CPU1 versus
2.291162 ms on the T4, making CPU1 approximately
3.86x faster at the p95 point estimate. CatBoost showed an even
larger low-batch CPU advantage: 0.239195 ms on CPU1
versus 1.478441 ms on the T4, equivalent to
approximately 6.18x lower p95 latency on CPU1.

These results indicate that accelerator selection for online IDS inference
cannot be reduced to a universal CPU-versus-GPU rule.

---

## D. Batch-Dependent Hardware Crossover

The batchwise measurements reveal distinct hardware-scaling regimes.

XGBoost changed from a CPU-favorable regime at small batches to a GPU-favorable
regime as batching increased. Its CPU1/GPU p95 ratio was
0.259 at B=1 and remained below 1 at
B=64, but reached 1.023 at B=256,
3.257 at B=1024, and
12.405 at B=8192. The observed
point-estimate crossover therefore occurred between the matched B=64 and B=256
conditions.

CatBoost crossed later. Its p95 CPU1/GPU ratio remained
0.986 at B=1024 and increased to
1.242 at B=8192. Thus, for the
measured conditions, GPU execution became favorable only at the largest batch.

The neural models exhibited a different pattern. The FT ensemble was already
GPU-favorable at B=1 and its p95 advantage expanded to
34.52x at B=64,
37.89x at B=256, and
49.06x at B=1024.

The masked CNN similarly showed a strong GPU advantage across every matched
CPU/GPU condition, rising from
10.86x at B=1 to
89.90x at B=64 and
100.51x at B=256.

The masked ViT moved from near parity at B=1 to clearly GPU-favorable operation
at larger batches, with point-estimate p95 ratios of
26.75x,
42.40x, and
58.72x at B=64, B=256, and
B=1024, respectively.

These ratios are descriptive point estimates. Confidence intervals for derived
CPU/GPU ratios were not computed and should not be inferred from the separate
latency confidence intervals.

---

## E. GPU Memory and Resource Feasibility

GPU acceleration introduced architecture-specific memory constraints.

The masked ViT reached a maximum observed delta peak GPU process memory of
approximately 10770.00 MiB at B=
8192, while remaining measurable at B=8192.

The masked CNN reached approximately
7810.00 MiB of delta peak GPU process memory
at its largest successful condition, B=1024. At B=8192
the CNN failed with a genuine CUDA out-of-memory resource-limit outcome. This
condition was retained as `RESOURCE_LIMIT_OOM`; no latency, throughput, or
memory value was imputed.

The five-checkpoint FT ensemble reached approximately
2462.00 MiB of maximum observed delta peak
GPU process memory. In comparison, the tree models required much smaller
incremental GPU process memory in the measured conditions: approximately
24.00 MiB for XGBoost and
12.00 MiB for CatBoost.

Memory feasibility therefore constitutes a separate deployment dimension from
latency acceleration. A configuration with high GPU throughput can still be
constrained by accelerator-memory capacity at large batches.

---

## F. Backend Availability as a Deployment Constraint

Not every frozen model exposed a contract-approved native GPU inference path.

The frozen LightGBM deployment artifact did not provide a native GPU inference
route under the Stage26 no-conversion/no-substitution policy. LightGBM GPU
conditions were therefore recorded as `BACKEND_UNAVAILABLE`, rather than being
executed through CPU prediction and mislabeled as GPU measurements.

Because the operational LightGBM+XGBoost ensemble requires probability outputs
from both frozen members, the absence of a valid LightGBM GPU inference path
also made the complete ensemble GPU backend unavailable.

This distinction is important: `BACKEND_UNAVAILABLE` describes deployment-path
availability and should not be interpreted as evidence that LightGBM GPU
inference is slower than CPU inference.

---

## G. Deployment Implications

The combined CPU/GPU profile supports three practical observations.

First, **low-latency online inference and high-throughput batched inference can
favor different hardware choices**. At B=1, CPU1 was substantially faster for
XGBoost and CatBoost, whereas GPU execution strongly benefited the masked CNN
and materially benefited the FT ensemble.

Second, **the point at which GPU execution becomes advantageous is
architecture-dependent**. XGBoost crossed into a GPU-favorable regime by
B=256, whereas CatBoost did not do so until B=8192 in the measured conditions.
The neural architectures generally benefited from GPU execution much earlier.

Third, **deployment selection should jointly consider predictive performance,
latency, batching behavior, backend availability, and memory requirements**.
For example, the masked CNN achieved strong GPU acceleration but had lower
frozen predictive discrimination than the masked ViT within Group B and reached
a GPU memory limit at B=8192. Conversely, the Group-A tree models combined
strong frozen PR-AUC with very low CPU batch-1 latency, making CPU deployment
competitive for low-batch operation even when GPU acceleration became useful
at larger batches.

These observations argue against reporting a single hardware-independent
"fastest model." Instead, the appropriate deployment choice depends on the
operational regime and the scientifically comparable model group.

---

## H. Limitations of the Deployment Study

Several boundaries should constrain interpretation.

1. The measurements represent **component-level inference**, not a complete
   end-to-end IDS pipeline.

2. A scientifically compatible complete extraction-to-inference measurement
   was unavailable. Raw extraction, representation construction, and isolated
   inference measurements must therefore remain separate.

3. The duplicate-safe 70-feature models and packet-image models were evaluated
   on different scientifically defined comparison populations; Pareto
   frontiers must remain within their respective groups.

4. CPU/GPU speedup ratios are descriptive point estimates. Ratio-level
   confidence intervals were not computed.

5. Resource-limit outcomes and unavailable backends were retained explicitly;
   missing deployment costs were not imputed.

6. Batch sizes were frozen before profiling. No post-hoc "best batch" or
   "optimal batch size" claim is made.

7. GPU results were obtained on a single Tesla T4 deployment profile. They
   should not be generalized to all GPU architectures without additional
   hardware-specific measurement.

---

## I. Recommended Main-Paper Presentation

### Main deployment figure
**F26_CPU1_GPU_P95_SPEEDUP**

Recommended message:
> GPU acceleration is architecture- and batch-dependent rather than universal.

### Main deployment table
**T26_CPU1_GPU_BATCH1_ANCHOR**

Recommended message:
> Low-batch online deployment can favor CPU inference for tree models while
> GPU execution benefits packet-image and transformer models.

### Accuracy–cost figure
**F26_PARETO**

Use separate Group-A and Group-B panels only.

Recommended message:
> Predictive discrimination and deployment cost must be interpreted within
> scientifically comparable representation groups.

### GPU resource figure
**F26_GPU_DELTA_PEAK_MEMORY**

Recommended message:
> Accelerator memory becomes a practical deployment constraint for large
> packet-image batches.

---

## J. Suggested Section-Level Takeaway

The principal deployment finding is not that GPU execution is universally
faster. Rather, the frozen models exhibit **architecture-dependent and
batch-dependent hardware regimes**. Tree models provide extremely low
single-flow CPU latency, while neural architectures derive much larger benefits
from GPU parallelism. Consequently, deployment decisions for an IDS should be
based on the expected batching regime, model representation, predictive
performance, backend availability, and memory budget rather than on model
accuracy or accelerator availability alone.
