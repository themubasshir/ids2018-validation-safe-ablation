# Stage 15 Transformer Checkpoint

This directory preserves the completed Stage 15 work before a
Kaggle session reset required to release an orphaned Tesla P100
CUDA context.

## Repository state

- Base commit: `15a5e8add4eb40c64ddc31cd5e545e449c78ddaa`
- Branch: `main`
- Checkpoint generated: `2026-08-06T09:21:37.743119+00:00`

## Completed work

### Stage 15.0

- Audited Transformer feasibility and leakage risk.
- Detected exact-pattern duplication across the original split.
- Confirmed that no validated temporal sequence metadata exists.
- Selected an FT-Transformer-style numerical feature tokenizer.

### Stage 15.1

- Removed globally conflicting binary-label patterns.
- Deduplicated each split deterministically.
- Removed cross-split exact-pattern overlap.
- Produced duplicate-safe split sizes:
  - Training: 154,686
  - Validation: 37,835
  - Holdout: 46,849
- Removed eight constant predictors.
- Retained 70 predictors.

### Stage 15.2

- Fit a StandardScaler using duplicate-safe training rows only.
- Derived positive-class weight from training labels only.
- Implemented `NumericFTTransformer`.
- Passed CPU forward, backward, and optimizer-step tests.
- Preserved the holdout without transformation or evaluation.

## CUDA environment finding

The Kaggle system PyTorch build was incompatible with the Tesla
P100 because it lacked `sm_60`. An isolated PyTorch 2.7.1 CUDA
11.8 environment successfully:

- imported from the isolated directory;
- detected the Tesla P100 with capability `(6, 0)`;
- exposed `sm_60`;
- executed basic CUDA tensor operations;
- executed a small FT-Transformer GPU forward pass.

The full batch verification was prevented by an orphaned CUDA
process holding approximately 15.8 GB of GPU memory. The isolated
PyTorch installation itself is not included in this repository
checkpoint because it is several gigabytes and can be recreated.

## Resume procedure

1. Start a fresh Kaggle GPU session.
2. Clone or pull this repository.
3. Restore this directory to `/kaggle/working/stage15_transformer`.
4. Reinstall PyTorch 2.7.1 CUDA 11.8 in an isolated target directory.
5. Run the preserved P100 CUDA verification script.
6. Begin Stage 15.3 training/validation-only architecture benchmarking.
7. Do not inspect the duplicate-safe holdout until the architecture,
   early-stopping rule, and operating threshold are frozen.
