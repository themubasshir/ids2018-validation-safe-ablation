# Stage20-1C16-D0 — Mechanism Search Stopping-Rule Lock

## Status

**PRE-TEST MECHANISM SEARCH BUDGET FROZEN**

Parent commit:

`6d1c0189f0ff53304a6d2abe2c70a87b6d76edee`

This checkpoint is frozen **before** either remaining mechanism candidate
is tested.

## Basis

Stage20-1C16-C established, over the 467 finished TCP flows:

- geometry-affected flows: **379**
- packet-geometry disagreements: **5093**
- capture > declared packets: **4930**
- capture < declared packets: **163**

Flow phenotype partition:

- NONE: **88**
- GT_ONLY: **345**
- LT_ONLY: **23**
- MIXED: **11**

The packet disagreement population is exhaustively partitioned by sign.
A MIXED flow contains both packet classes; MIXED is not a third
packet-level disagreement class.

## Remaining mechanism-test budget

Exactly **2** candidates remain.

No third candidate may be introduced in this Stage 20 reconstruction branch.

### M1 — GT_CAPTURE_BEYOND_DECLARED_IPV4

Frozen population:

**4930 packets**

Hypothesis:

For every GT disagreement packet, the positive capture-minus-declared
payload difference is produced by captured IPv4 material extending beyond
the declared IPv4 total length.

Acceptance requires, for **all 4930 packets**:

1. captured IPv4 extent > declared IPv4 total length;
2. excess byte count exactly equals the payload-length difference;
3. no label value, tolerance, nearest match, or cohort outcome is needed.

Any failing packet rejects M1 as a complete mechanism.

### M2 — LT_CAPTURE_SHORTER_THAN_DECLARED_IPV4

Frozen population:

**163 packets**

Hypothesis:

For every LT disagreement packet, the negative capture-minus-declared
payload difference is produced by the captured IPv4 extent ending before
the declared IPv4 total length.

Acceptance requires, for **all 163 packets**:

1. captured IPv4 extent < declared IPv4 total length;
2. missing byte count exactly equals the payload-length difference;
3. no label value, tolerance, nearest match, or cohort outcome is needed.

Any failing packet rejects M2 as a complete mechanism.

## Frozen order

1. M1 — GT_CAPTURE_BEYOND_DECLARED_IPV4
2. M2 — LT_CAPTURE_SHORTER_THAN_DECLARED_IPV4

## Stopping rule

After these two candidates have been tested exactly once:

**Stage 20 reconstruction-mechanism search stops regardless of outcome.**

This applies if:

- both candidates pass;
- only one passes;
- neither passes;
- unexplained packets remain.

Any unresolved remainder is recorded as unresolved rather than generating
another mechanism candidate.

Candidate substitution and candidate expansion are prohibited.

## Important interpretation boundary

Mechanism confirmation does **not** constitute adoption of V1 or any
selective capture/declared hybrid as a reconstruction rule.

The following remain prohibited:

- label-guided packet semantics
- cohort-guided packet semantics
- sign-guided hybrid semantics
- residual-only correction
- fuzzy or nearest matching
- duration substitution
- model training before representation freeze
- Friday access

## After the stopping rule fires

The next phase is representation freeze:

- packets per flow
- bytes per packet
- channels
- padding / truncation
- header policy
- leakage controls

Only after those are frozen may the architecture/training protocol proceed.

## Artifact

`results/stage20_1c16_runtime_recovery/stage20_1c16d0_mechanism_search_budget_lock.json`

SHA256:

`fd0ba8efe09ebc7c253a60c5ffa0609fcb4946c1e3930ab7f77912ef35b0513c`

## Holdout integrity

- Friday requests: **0**
- Friday reads: **0**
- Friday openings: **0/1**
- Friday status: **CLOSED**
