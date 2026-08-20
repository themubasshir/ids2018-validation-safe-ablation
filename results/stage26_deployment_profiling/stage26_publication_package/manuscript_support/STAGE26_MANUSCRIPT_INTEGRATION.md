
# Stage26 Manuscript Integration

## Scientific identity

- Final Stage26 scientific anchor:
  `9e8354ecc9cfa72c28aa037e5d2053de422bf7a2`
- CPU closure anchor:
  `304e5613627a744cbd5d369857f8ac5667a520eb`
- G1 GPU profiling anchor:
  `79b9c23c91ef7185d35b700e6f6f84aefb54ab35`

Stage26 deployment profiling is complete and frozen. This document is a
post-closure manuscript integration guide and does not introduce new
measurements.

## Main-paper assets

Recommended core deployment assets:

1. `F26_CPU1_GPU_P95_SPEEDUP`
   - primary CPU1/GPU deployment comparison;
   - demonstrates architecture- and batch-dependent acceleration.

2. `T26_CPU1_GPU_BATCH1_ANCHOR`
   - low-batch / online inference anchor.

3. `F26_PARETO`
   - predictive-performance versus CPU1 batch-1 latency;
   - Group A and Group B must remain scientifically separate.

4. `F26_GPU_DELTA_PEAK_MEMORY`
   - GPU memory/resource feasibility.

## Supplementary deployment assets

The canonical publication package also contains:

- complete CPU warm-inference table;
- CPU cold-start table;
- CPU memory/package table;
- component measurement table;
- capacity/scaling table;
- representation sensitivity table;
- Group-B representation/inference-ratio table;
- full matched CPU1/GPU comparison table;
- GPU warm inference/memory table;
- GPU backend/resource-status table;
- all CPU and GPU deployment figure families in PNG and PDF form.

## Claim boundaries

The following restrictions are mandatory:

1. Use **component-level inference**, not complete end-to-end IDS latency.
2. Complete extraction-to-inference E2E measurement is unavailable.
3. Do not compare Pareto frontiers across Group A and Group B.
4. CPU/GPU speedup ratios are descriptive point estimates; ratio-level
   confidence intervals were not computed.
5. Do not impute cost for `RESOURCE_LIMIT_OOM`, timeout, or
   `BACKEND_UNAVAILABLE`.
6. Do not describe frozen batch sizes as retrospectively optimized.
7. LightGBM GPU backend unavailability is not a latency result.
8. The single-T4 results are hardware-specific.

## Canonical publication locations

Tables:

`results/stage26_deployment_profiling/stage26_publication_package/tables/`

Figures:

`results/stage26_deployment_profiling/stage26_publication_package/figures/`

Top-level figure mirror:

`figures/stage26_deployment_profiling/`

Final synthesis:

`results/stage26_deployment_profiling/stage26_12_final_synthesis/`
