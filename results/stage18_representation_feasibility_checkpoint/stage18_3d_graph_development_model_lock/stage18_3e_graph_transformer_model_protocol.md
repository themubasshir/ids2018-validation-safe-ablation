# Stage 18.3E — Graph Transformer Model Protocol

## Status

**MODEL / PREPROCESSING PROTOCOL LOCKED**

The graph experiment remains limited to the endpoint-rich `02-20-2018.csv` source.

The chronological split defined before label inspection remains unchanged.

## Frozen class distribution

### Training

- Flow edges: 4,068,165
- Benign: 4,067,368
- Attack: 797
- Attack prevalence: 0.019591142%

### Validation

- Flow edges: 2,166,254
- Benign: 1,742,633
- Attack: 423,621
- Attack prevalence: 19.555463025%

This represents an extreme chronological class-prior/distribution shift.

The shift is retained exactly as observed.

No temporal boundary may be changed in response to these labels.

## Edge preprocessing

The frozen 70 retained numeric predictors are used as edge attributes.

Non-finite handling:

1. positive and negative infinity become missing values;
2. each missing value is imputed using the corresponding **training-only median**;
3. a `StandardScaler` is fitted using training only;
4. validation receives the frozen training medians and scaler;
5. the graph holdout later receives exactly the same frozen preprocessing.

Rows are not dropped because dropping flow events would alter authentic graph topology.

## Node features

Each host receives five label-independent snapshot-local features:

1. constant one;
2. log1p incoming flow degree;
3. log1p outgoing flow degree;
4. log1p incident flow count;
5. log1p unique peer count.

No node-ID or numeric-IP embedding is allowed.

## Graph Transformer

Model: **EdgeAwareDirectedGraphTransformer**

- node dimension: 64
- edge embedding dimension: 64
- graph layers: 2
- attention heads: 4
- head dimension: 16
- feed-forward dimension: 128
- dropout: 0.10
- activation: GELU

Attention operates only on observed directed incoming flow edges inside the current 60-second snapshot.

Parallel flow edges remain separate messages.

No reverse artificial edges are created.

No cross-snapshot message passing occurs.

## Edge prediction

Each individual flow edge is classified using:

- final source-node embedding;
- final destination-node embedding;
- encoded 70-feature edge embedding;
- destination-minus-source node embedding.

The classifier maps the 256-dimensional concatenation through:

- Linear(256, 128)
- GELU
- Dropout(0.10)
- Linear(128, 1)

## Extreme class imbalance

All chronological training edges are retained.

There is:

- no benign undersampling;
- no attack oversampling;
- no SMOTE;
- no synthetic graph traffic.

Training uses `BCEWithLogitsLoss`.

The positive weight is computed **only from training**:

`TRAIN benign / TRAIN attack = 5103.347553324968`

Validation and holdout prevalence do not influence the loss weight.

## Optimization

- AdamW
- learning rate: 0.0003
- weight decay: 0.0001
- maximum epochs: 20
- gradient clip: 1.0
- gradient accumulation: 8 chronological snapshots
- no training-snapshot shuffle
- mixed precision enabled

## Replication

Three independent seeds are frozen:

- 7
- 29
- 101

No architecture hyperparameter search is performed.

Validation probabilities from the three final seed checkpoints are averaged equally.

## Early stopping

Each seed is early-stopped using validation PR-AUC.

- maximize PR-AUC
- patience: 4 epochs
- minimum delta: 0.0001
- maximum: 20 epochs

The graph holdout is never used for early stopping.

## Threshold selection

The three-seed validation ensemble selects one threshold from:

`0.01, 0.02, ..., 0.99`

Primary rule:

**maximum validation F1**

Tie breaking:

1. higher recall;
2. lower threshold.

Metrics at fixed threshold 0.50 are also retained.

## Edge-only control

A paired non-graph MLP uses the exact same 70 preprocessed edge features, loss, seeds, optimizer and chronological partitions.

Architecture:

- Linear(70,128)
- GELU
- Dropout(0.10)
- Linear(128,64)
- GELU
- Dropout(0.10)
- Linear(64,1)

This control determines whether graph context adds information beyond the flow attributes themselves.

## Graph holdout

The `11:00–12:59` graph holdout remains **closed**.

It can be opened once only after:

- preprocessing is frozen;
- all six model checkpoints are frozen;
- validation ensembles are frozen;
- validation thresholds are frozen;
- development results are frozen in Git.

## Current boundary

At this stage:

- Graph Transformer models trained: 0
- Edge-only controls trained: 0
- Holdout openings: 0
- Holdout labels read: 0
- Holdout predictor vectors read: 0
- Holdout endpoints read: 0

## Next stage

Stage 18.3F may build the **training-only preprocessing artifacts** and deterministic train/validation graph tensors.

No model fitting is authorized yet.
