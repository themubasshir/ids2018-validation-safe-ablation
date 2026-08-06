# Stage 15 Transformer Checkpoint

This package preserves Transformer feasibility, duplicate-safe
partitioning, preprocessing, GPU compatibility, architecture
screening, and convergence-extension results.

## Repository state

- Base commit: `21eb0854f2749562f2ba21255c59c8cc6f2f009b`
- Generated: `2026-08-06T10:43:13.949579+00:00`
- Branch: `main`

## Completed stages

### Stage 15.0

- Audited Transformer feasibility.
- Identified exact-pattern duplication and conflicting labels.
- Rejected unsupported temporal or spatial Transformer claims.

### Stage 15.1

- Created duplicate-safe train, validation, and holdout partitions.
- Training rows: 154,686
- Validation rows: 37,835
- Holdout rows: 46,849
- Cross-split exact-pattern overlap: zero
- Retained predictors: 70

### Stage 15.2

- Fit StandardScaler using training rows only.
- Implemented numerical FT-Transformer.
- Verified PyTorch 2.7.1 CUDA 11.8 on Tesla P100.
- Confirmed `sm_60`, CUDA forward/backward execution, and
  optimizer updates.

### Stage 15.3A

Compared three architectures using training and validation only:

- FT_COMPACT
- FT_BALANCED
- FT_DEEP_REGULARIZED

### Stage 15.3B

Extended the seed-42 checkpoints beyond the original 15-epoch
ceiling.

Convergence-adjusted provisional winner:

- Architecture: FT_BALANCED
- Best epoch: 28
- Validation threshold: 0.6599999999999997
- Validation F1: 0.8626812355536877
- Validation PR-AUC: 0.9272883071218994
- Validation recall: 0.7679573512906847

The deep model reached its best result at the 30-epoch ceiling.
The next standardized from-scratch multi-seed protocol should
therefore allow up to 40 epochs.

## Scientific boundary

The duplicate-safe holdout has not been used for architecture
selection, early stopping, threshold selection, probability
generation, or performance evaluation.

## Packaging correction

`__pycache__` directories and `.pyc` files are intentionally
excluded. They are runtime-generated files and are not scientific
artifacts.
