# Stage23 Deterministic Execution Cache V1

This directory freezes the verification metadata for the Stage23
execution-cache optimization introduced after Stage23-1I.

## Purpose

The cache removes repeated Parquet decompression and Python/PyArrow column
conversion from subsequent Stage23 execution.

The large binary cache itself is intentionally **not stored in Git**.

Runtime location:

`/kaggle/working/stage23_execution_cache_v1`

## Canonical corpus

- Development rows: 14,412,403
- Frozen features: 70
- Feature dtype: float64
- Source days: February 14 through February 28 only
- Raw March 1 access: no
- Raw March 2 access: no

## Exact semantic equivalence

Old Stage23 row-major 70-feature semantic SHA256:

`8c43ab0e36a65de1c095acb1ebf9e7d029a9e2b1cc353455a66617db8a899bb2`

New cache reconstructed row-major 70-feature semantic SHA256:

`8c43ab0e36a65de1c095acb1ebf9e7d029a9e2b1cc353455a66617db8a899bb2`

Therefore the cache is byte-equivalent to the previously used Stage23
float64 materialization semantics.

Verified:

- all 70 feature columns
- binary labels
- day IDs
- clean positions
- original row indices
- RANDOM_NATURAL membership
- CHRONOLOGICAL_NATURAL membership

## Frozen split counts

### RANDOM_NATURAL

- Train: 11,529,922
- Validation: 2,882,481

### CHRONOLOGICAL_NATURAL

- Train: 13,818,623
- Validation: 593,780
- Train day IDs: 0–6
- Validation day ID: 7

## Scientific governance

This optimization consumed **zero model fits**.

Stage23 fit accounting remains:

`18 / 50`

No change was made to:

- feature definitions
- feature order
- row membership
- input dtype
- model parameters
- model seeds
- thresholds
- ensemble definition
- Stage23-0 protocol

## Next authorized model cell

`Stage23-1J NO_SUSPICIOUS_GROUP × CHRONOLOGICAL_NATURAL`
