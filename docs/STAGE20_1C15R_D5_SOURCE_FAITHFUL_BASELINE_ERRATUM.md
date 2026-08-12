# Stage 20.1C15-R-D5 — Source-Faithful Baseline Erratum

## Purpose

This checkpoint freezes a source-faithful correction to the bounded Stage 20 Monday reconstruction before the frozen TCP payload rule is evaluated against the 37 length-only residuals.

Parent commit:

`bbf3f9ffe4d49ea32a29342a987fa3de254a7a49`

Friday holdout:

**CLOSED — 0/1**

## Corrected bounded baseline

First 50,000 Monday packets:

- exportable reconstructed flows: **675**
- exact S4 membership: **635/675**
- exact S4 multiset: **635/675**
- TCP length-only residuals: **37**
- duration/export inconsistencies: **2**
- protocol-0 anchor inconsistency: **1**

The 37 TCP length-only residual population is unchanged.

## Timestamp serialization

The published Monday label timestamps have whole-second resolution.

Reconstruction timestamps are therefore serialized to whole seconds for the S4 Timestamp field.

This restores 635 exact flows and isolates only two additional lifecycle discrepancies beyond the previously known 37 TCP length residuals and one protocol-0 anchor case.

## Two duration/export cases

### TCP destination port 1113

Relevant raw packet sequence:

- packet 38276: server → client, PA
- packet 38277: client → server, FIN/ACK
- duration between these packets: **224 µs**
- packet 38287: server → client, FIN/ACK
- packet 38288: client → server, ACK
- duration between these later packets: **58 µs**

The published label candidate contains duration **58 µs**.

### TCP destination port 1112

Relevant raw packet sequence:

- packet 38278: server → client, PA
- packet 38279: client → server, FIN/ACK
- duration between these packets: **262 µs**
- packet 38289: server → client, FIN/ACK
- packet 38290: client → server, ACK
- duration between these later packets: **26 µs**

The published label candidate contains duration **26 µs**.

## Historical FlowGenerator interpretation

The inspected historical CICFlowMeter FlowGenerator behavior is:

1. If a matching current flow exists and the flow timeout is exceeded, the old flow is emitted when exportable and the current packet seeds a new BasicFlow.
2. If a matching current flow exists and the packet has FIN, the packet is added, the flow is emitted, and the flow is removed.
3. If no matching current flow exists, a new BasicFlow is created. A FIN packet used as the first packet is not immediately emitted by this branch.
4. Flow Duration is `flowLastSeen - flowStartTime`.

This state machine explains why the later FIN-first + ACK pairs have durations **58 µs** and **26 µs**.

It does not justify replacing the independently reconstructed **224 µs** and **262 µs** completed-flow durations with the label values.

## Scientific handling

The two cases are therefore treated as **duration/export inconsistencies**, not as parameters to fit.

No duration value is substituted from a label.

The previously frozen C9/C10 records remain preserved as historical checkpoints, but their 637/675 exactness is not used as the source-faithful post-forensic baseline after this audit.

The source-faithful pre-payload-validation baseline is:

**635/675 exact + 37 TCP length-only residuals + 2 duration/export inconsistencies + 1 protocol-0 anchor inconsistency.**

## Boundary

This checkpoint occurs before the frozen TCP payload semantics are evaluated against the 37 length-only residuals.

No corrected payload signature has been evaluated in this checkpoint.

## Holdout integrity

Friday requests: **0**

Friday reads: **0**

Friday openings: **0/1**

Friday status: **CLOSED**

## Decision

**SOURCE_FAITHFUL_BASELINE_FROZEN_BEFORE_TCP_RESIDUAL_VALIDATION**
