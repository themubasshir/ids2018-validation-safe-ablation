# Stage21-3 — Thursday ViT Validation

## Status

**Stage21MaskedViTv1 evaluated on Thursday exactly once and all Stage21
operating points are now frozen.**

Parent commit:

`7f63e836609aa63939d01929b33fd4ccfa897a44`

## Model

- candidate: `Stage21MaskedViTv1`
- fixed checkpoint: epoch 10
- checkpoint SHA256: `221e9c805fb663acacf2f0f2ca95dba7cb4b2ec4c4de5a3650cf4adeb99b5ef8`
- canonical state SHA256: `9da47df6cd5c821eef3d2c8a501296cd6070b835c719999f572f3dec2d560771`

## Thursday population

- flows: **8,197**
- BENIGN: **8,155**
- ATTACK: **42**

## Score metrics

- ROC-AUC: **0.973370120580**
- PR-AUC: **0.234770598524**

## Frozen operating points

### Standard

- threshold: **0.50**
- F1: **0.000000000000**
- Recall: **0.000000000000**
- FPR: **0.001348865727**

### Balanced

- threshold: **0.42**
- F1: **0.035714285714**
- Recall: **0.023809523810**
- FPR: **0.001594114040**

### Security

- threshold: **0.24**

## Probability source-of-truth

- dtype: **float32**
- count: **8,197**
- SHA256: `db73defd588de532ee1bd29e941ddc55989620c7ef63d340b7109a947981826f`

## Scientific boundary

- Thursday ViT inference passes: **1**
- validation during training: **NO**
- model retraining: **NO**
- optimizer steps after Stage21-2: **0**
- Friday accessed: **NO**
- thresholds are now immutable.

## Next

**Stage21-4 — one ViT inference pass on the locked Friday reuse benchmark.
No threshold search and no model changes are permitted.**
