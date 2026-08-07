# Stage 18.0 — Representation-Feasibility Protocol

## Status

**LOCKED BEFORE ARCHITECTURE AUDITS**

Stage 18 determines whether additional Transformer-family
architectures are scientifically supportable before any model
training occurs.

The candidates are:

1. Temporal / MTemporal Transformer
2. Vision Transformer (ViT)
3. Graph Transformer

A candidate may receive one of three outcomes:

- **SUPPORTED**
- **SUPPORTED WITH CONSTRAINTS**
- **NOT SUPPORTED BY CURRENT ARTIFACTS**

An architecture will not be forced into the experiment merely
because it was proposed.

---

## Universal rule

**Representation validity precedes architecture performance.**

Validation performance cannot rescue an unjustified
representation.

Neither the classical nor Transformer holdout may be used to
design, choose, or justify a Stage 18 representation.

---

## Temporal / MTemporal Transformer

A temporal architecture requires authentic ordering information.

The audit must establish:

- recoverable timestamps or documented capture order;
- meaningful sequence membership;
- past-to-future ordering;
- split-isolated sequence construction;
- no label-driven grouping;
- no future leakage.

Arbitrary balanced-dataset row order may not be treated as time.

---

## Vision Transformer

ViT requires a genuine two-dimensional traffic representation.

The audit must establish:

- meaningful image axes;
- semantically meaningful local adjacency;
- reproducible feature-to-image mapping;
- no label-driven or XAI-driven feature placement.

Simply reshaping 70 tabular features into a rectangular grid is
explicitly prohibited.

---

## Graph Transformer

A graph architecture requires defensible network entities and
relations.

The audit must establish:

- meaningful node definitions;
- meaningful observed edges;
- provenance for endpoint/session information;
- leakage-safe graph construction;
- handling of shared entities across splits.

Arbitrary k-nearest-neighbor feature graphs and arbitrary fully
connected graphs are prohibited.

---

## Audit sequence

1. Stage 18.1 — Temporal representation audit
2. Stage 18.2 — Vision representation audit
3. Stage 18.3 — Graph representation audit

Only candidates that pass their representation audit may proceed
to architecture implementation.

---

## Scientific boundary

Stage 18.0 performs:

- dataset reads: **0**
- dataset transformations: **0**
- sequence constructions: **0**
- image constructions: **0**
- graph constructions: **0**
- model fits: **0**
- model inference: **0**
- holdout openings: **0**

Stage 18.0 defines methodology only.
