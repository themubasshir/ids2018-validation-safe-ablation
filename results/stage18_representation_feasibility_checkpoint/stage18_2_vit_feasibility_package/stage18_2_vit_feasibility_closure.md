# Stage 18.2 — Vision Transformer Representation Feasibility

## Final decision

**NOT_SUPPORTED_BY_CURRENT_ARTIFACTS**

Stage 18.2 evaluated whether the available CSE-CIC-IDS2018 research artifacts support a scientifically defensible Vision Transformer representation.

The answer is **no under the current artifacts**.

This is a representation-level decision. No ViT model was trained and no performance comparison was used.

## Source inventory

The mounted source universe contains:

- no PCAP or PCAPNG files;
- no packet-byte tensors;
- no native traffic images;
- no pre-existing authenticated 2D matrices.

All ten raw CSV files retain an authentic timestamp field.

Only `02-20-2018.csv` retains complete source/destination endpoint identifiers.

## Candidate representations

Seven possible representation routes were audited.

### Packet-byte image

**Not supported by current artifacts.**

No packet capture or raw packet-byte representation is mounted.

### Native network image

**Not supported by current artifacts.**

No authenticated native traffic-image representation exists.

### Tabular feature grid

**Prohibited.**

The 70/78 heterogeneous flow predictors do not possess authentic two-dimensional geometry. Reshaping them into a rectangular image would create artificial adjacency.

### Time × feature matrix

**Not justified for ViT.**

Time is intrinsically ordered, but feature-column order is not spatial. Reordering feature columns changes ViT patch neighborhoods without changing the underlying tabular observation.

### Time × destination-port matrix

**Not justified for ViT.**

Time is intrinsically ordered. Destination-port numbers, however, are protocol/service identifiers rather than coordinates in a metric spatial domain.

For example, numerical closeness between port identifiers does not establish semantic proximity between services.

### Source-host × destination-host matrix

**Not justified for ViT.**

This matrix has genuine relational meaning, but host ordering is arbitrary. Permuting node indices leaves the network relationship unchanged while completely altering image patch neighborhoods.

This structure is more naturally evaluated under graph-based architectures.

### Time × endpoint matrix

**Not justified for ViT.**

Time provides valid locality, but endpoint identity has no intrinsic linear spatial ordering.

Endpoint metadata is also available in only one of the ten original source files.

## Hard admissibility criteria

Seven candidate representations were evaluated against the precommitted ViT requirements.

Candidates audited: **7**

Candidates passing every hard criterion: **0**

Therefore no ViT representation is scientifically admissible under the current artifacts.

## Architecture distinction

| Architecture | Stage-18 status |
|---|---|
| Tabular Transformer | Supported and already completed |
| Temporal / MTemporal Transformer | Supported with constraints |
| Vision Transformer | **Not supported by current artifacts** |
| Graph Transformer | Deferred to Stage 18.3 |

## Scientific interpretation

The rejection of ViT does **not** mean that Vision Transformers are universally unsuitable for intrusion detection.

It means that this research dataset, in its currently available form, does not contain a representation with sufficiently defensible two-dimensional spatial locality for ViT patch construction.

Creating an arbitrary feature image merely to run ViT would weaken rather than strengthen the experiment.

## Scientific boundary

Stage 18.2 performed:

- no ViT fitting;
- no model inference;
- no holdout access;
- no label-based representation design;
- no image generation;
- no matrix construction;
- no arbitrary feature-grid construction;
- no performance-based representation selection.

## Closure

**Stage 18.2 is scientifically closed.**

Final decision:

> **Vision Transformer — NOT_SUPPORTED_BY_CURRENT_ARTIFACTS**

The endpoint relationships identified in `02-20-2018.csv` are carried forward to Stage 18.3 because their semantics are relational rather than spatial.
