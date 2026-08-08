# Stage 18.3C — Graph Transformer Development Protocol

## Feasibility decision

**SUPPORTED WITH CONSTRAINTS**

The endpoint-rich `02-20-2018.csv` source contains authentic network entities and observed communication relations suitable for a separate Graph Transformer experiment.

This experiment is not a dataset-wide replacement for the existing benchmark.

## Graph representation

The primary representation is a **directed temporal multigraph**.

- Nodes: authenticated network hosts from `Src IP` and `Dst IP`.
- Edge events: individual observed flows from source host to destination host.
- Parallel flow edges are preserved.
- Edge direction is preserved.
- Host ordering has no semantic meaning.
- The model must be permutation-compatible.

No feature-similarity, fully connected, label-defined, prediction-defined, or numeric-feature-node graph is allowed.

## Prediction unit

The prediction unit is an **individual flow edge**.

The existing binary flow label will later serve as the target, but labels were not inspected during this protocol lock and cannot influence graph topology.

## Snapshot definition

Graphs are divided into fixed, non-overlapping **60-second snapshots**, aligned to recorded clock-minute boundaries.

The dataset timestamps are used as recorded; no timezone is inferred.

Flows sharing the same second are treated as simultaneous. CSV row order is never used to invent within-second chronology.

The 60-second snapshot duration is frozen before label inspection or performance measurement and will not be tuned.

## Chronological split

### Training
`2018-02-20 01:00:00` through `08:59:59`

### Validation
`2018-02-20 09:00:00` through `10:59:59`

### Graph-specific final holdout
`2018-02-20 11:00:00` through `12:59:59`

The boundaries are based only on source time.

No label stratification or performance-driven boundary selection is permitted.

The old Stage-15 duplicate-safe membership is not reused.

## Graph holdout

The final two hours form a new graph-specific chronological holdout.

It remains closed during:

- architecture selection;
- representation selection;
- preprocessing selection;
- hyperparameter selection;
- early stopping;
- threshold selection.

It may be opened once after the graph pipeline is frozen.

## Edge features

The primary edge attributes are the frozen **70 retained numeric predictors** from the Stage-15 feature schema.

The following are not predictive numeric features:

- Src IP;
- Dst IP;
- Flow ID;
- target label;
- attack category.

Preprocessing is fitted on chronological training data only.

## Node features

No learned node-identity or IP-address embedding is permitted.

Permitted label-independent node information includes:

- constant node feature;
- snapshot-local in-degree;
- snapshot-local out-degree;
- snapshot-local incident-flow count;
- snapshot-local unique-peer count.

Full-day or future-derived structural statistics are prohibited.

## Message-passing isolation

The primary model may message-pass **only inside the current 60-second snapshot**.

No message passing is allowed:

- across snapshots;
- across train/validation boundaries;
- from future to past;
- from validation into training;
- from holdout into training or validation.

A global full-day graph cannot be used.

## Persistent hosts and edges

A host may legitimately appear in training and later validation/holdout periods.

Likewise, a host pair may communicate repeatedly over time.

This is not automatically leakage because they are persistent real network entities.

However, all results must separately report performance for:

- seen hosts;
- unseen hosts;
- seen host pairs;
- unseen host pairs.

No future data may influence earlier embeddings or structural features.

## Duplicate and repeated traffic

Repeated raw traffic events are preserved.

The graph experiment models authentic chronological events and therefore does not reuse the Stage-15 duplicate-safe row membership.

Parallel host-to-host edges remain distinct flow events.

## Current scientific boundary

At this protocol-lock stage:

- labels read: 0;
- graphs constructed: 0;
- snapshots materialized: 0;
- models trained: 0;
- graph holdout openings: 0.

## Next stage

Stage 18.3D may materialize the frozen partitions and verify their graph statistics and class distributions.

The protocol cannot be changed in response to those results.
