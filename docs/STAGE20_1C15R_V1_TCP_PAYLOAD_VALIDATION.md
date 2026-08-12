# Stage 20.1C15-R-V1 — Frozen TCP Payload Validation

## Scope

This checkpoint records the first global S4 validation of the independently frozen TCP payload semantics against the source-faithful bounded Monday reconstruction.

Parent commit:

`692dbf35a61724f0d2d4f8eede3e6b50dcaaa32a`

Friday holdout:

**CLOSED — 0/1**

## Frozen rule

Before residual validation, the packet-level TCP payload rule had been frozen as:

`IPv4.total_length - IPv4.header_length - TCP.header_length`

The rule was derived independently of flow labels from protocol geometry and direct pinned jNetPcap 1.4.r1425 behavior.

No label information was used to derive or modify the rule.

## Source-faithful pre-validation baseline

The source-faithful bounded first-50k Monday baseline was frozen before payload evaluation:

- population: **675 flows**
- exact S4 membership: **635/675**
- exact S4 multiset: **635/675**
- TCP length-only residuals: **37**
- duration/export inconsistencies: **2**
- protocol-0 anchor inconsistency: **1**

## Structural validation

Applying the frozen TCP payload rule changed **379** flow signatures.

All changes were restricted to the six S4 packet-length fields:

- Total Length of Fwd Packets
- Total Length of Bwd Packets
- Fwd Packet Length Min
- Fwd Packet Length Max
- Bwd Packet Length Min
- Bwd Packet Length Max

There were:

- non-length S4 changes: **0**
- non-TCP signature changes: **0**

Therefore the observed outcome is attributable specifically to the frozen TCP packet-length semantics rather than lifecycle, timestamps, orientation, flags, or non-TCP behavior.

## Global validation result

S4 transition matrix:

- exact -> exact: **295**
- exact -> absent: **340**
- absent -> exact: **23**
- absent -> absent: **17**

Corrected global result:

- baseline exact: **635/675**
- corrected exact: **318/675**
- exact-S4 net change: **-317**
- corrected absent signatures: **357**

## Frozen 37 TCP length-only residuals

Of the previously isolated 37 length-only TCP residuals:

- resolved: **23**
- remaining: **14**

All 14 remaining residuals are FIN-terminated flows.

Although the frozen rule resolves 23 residuals, it simultaneously invalidates 340 previously exact signatures.

Therefore applying the rule only to the residual subset, or selectively choosing between baseline and corrected lengths using label agreement, is prohibited as post-hoc label-guided correction.

## Scientific conclusion

The following two observations are both supported:

1. In the independently tested packet population, pinned jNetPcap 1.4.r1425 TCP payload length follows IPv4/TCP declared protocol geometry.
2. Those packet-length semantics do **not** globally reproduce the packet-length fields contained in the published CICIDS2017 Monday flow-label artifact.

Therefore the pinned jNetPcap/protocol-derived rule is rejected as a global correction for reconstruction of this published label artifact.

This result suggests an unresolved divergence between the tested packet-decoder/runtime semantics and the pipeline that generated the published flow-label artifact.

Potential mechanisms require separate source-derived investigation and must not be selected using label agreement.

## Prohibited interpretation

This checkpoint does not authorize:

- applying the corrected rule only to the 23 successful residuals,
- choosing packet semantics per flow from label agreement,
- hybrid baseline/corrected signatures,
- tolerance matching,
- nearest-neighbor matching,
- formula fitting to residuals,
- modifying the frozen rule after observing this result.

## Decision

**PRE_FROZEN_TCP_PAYLOAD_SEMANTICS_REJECTED_AS_GLOBAL_PUBLISHED_LABEL_RECONSTRUCTION_RULE**

## Holdout integrity

Friday requests: **0**

Friday reads: **0**

Friday openings: **0/1**

Friday status: **CLOSED**
