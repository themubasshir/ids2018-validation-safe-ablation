# Stage 19.0 — MTemporal-IDS Protocol

## Status

**LOCKED BEFORE DATA ACCESS**

Stage 19 introduces a new experiment and does not modify the
scientifically closed Stage 18 results.

## Research question

Can a strictly causal multi-scale temporal Transformer detect
second-level intrusion activity under a fully chronological
CSE-CIC-IDS2018 protocol?

## Model definition

The model is called **MTemporal-IDS (Multi-Scale Temporal
Transformer for Intrusion Detection)**.

The name is defined explicitly by this study. It is not presented
as reproduction of a universally canonical external model named
"MTemporal Transformer."

## Prediction unit

The prediction unit is a one-second wall-clock traffic bin.

A bin is positive if at least one flow during that second is
labeled as an attack. Flows sharing the same timestamp are treated
as simultaneous; no artificial within-second ordering is created.

## Chronological split

### Train

- 02-14-2018
- 02-15-2018
- 02-16-2018
- 02-20-2018
- 02-21-2018
- 02-22-2018
- 02-23-2018

### Validation

- 02-28-2018

### Final holdout

- 03-01-2018
- 03-02-2018

The final holdout is currently **CLOSED** and may be opened exactly
once after every development decision has been frozen.

## Multi-scale temporal context

| Scale | Bin width | Tokens | Context |
|---|---:|---:|---:|
| Fine | 1 s | 60 | 60 s |
| Medium | 15 s | 20 | 5 min |
| Coarse | 60 s | 20 | 20 min |

All context is past-or-current only.

No temporal window may cross a source-day or partition boundary.

The first 20 minutes of each day are excluded before labels are
examined so every retained sample has the complete frozen context.

## Bin representation

For each valid temporal bin:

- common numeric flow predictors are aggregated by arithmetic mean;
- flow count is represented as log1p(count);
- occupancy is represented explicitly;
- empty temporal bins remain explicit;
- preprocessing is fitted on TRAIN only.

## MTemporal architecture

Each temporal scale has its own Transformer encoder:

- d_model = 64
- heads = 4
- encoder layers = 2
- feed-forward dimension = 128
- dropout = 0.10
- GELU activation
- causal attention
- deterministic temporal position encoding

Each branch is summarized by its final causal token state.

The three scale representations are fused using a learned softmax
gate and passed to the final binary classifier.

## Control

A SingleScaleTemporalTransformer uses only the 60-second fine-scale
branch under otherwise matched core Transformer settings.

The comparison is descriptive and not a causal estimate of
multi-scale context.

## Optimization

- seeds: 7, 29, 101
- AdamW
- learning rate: 3e-4
- weight decay: 1e-4
- maximum epochs: 20
- batch size: 256
- AMP: enabled
- gradient clipping: 1.0
- BCEWithLogitsLoss
- TRAIN-only positive class weighting
- validation PR-AUC early stopping
- no hyperparameter search

## Threshold policy

Validation-only threshold search:

- grid: 0.01 to 0.99
- step: 0.01
- maximize F1
- tie 1: higher recall
- tie 2: lower threshold

The frozen validation threshold will later be transferred unchanged
to the final chronological holdout.

## Scientific boundary

Stage 19 does not reuse the Stage-15 split.

Stage 19 does not reopen any earlier holdout.

The final Stage-19 holdout may be opened once only after the
representation, preprocessing, checkpoints, ensemble and validation
thresholds are frozen.

Stage-19 second-bin metrics are not directly comparable with the
earlier per-flow benchmark.
