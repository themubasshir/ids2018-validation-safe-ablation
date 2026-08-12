# Stage 20.1C14 — TCP Payload Semantics Freeze

## Purpose

This checkpoint freezes the historical TCP packet-length semantics before applying them to the previously identified 37 TCP S4 length-only residuals.

Parent commit:

`4c991338ccdae8669d3a4b0461c4406fbc6bf3d3`

Friday holdout:

**CLOSED, 0/1**

## Independent derivation

Stage 20.1C12 compared pinned jNetPcap 1.4.r1425 with Scapy using only exactly identity-aligned TCP packet observations from the first 50,000 Monday packets.

Exactly aligned TCP packets:

**31,618**

TCP transport-header length:

**31,618/31,618 identical**

Payload length:

- identical: **23,067/31,618**
- different: **8,551/31,618**

No labels were read.

## Protocol geometry validation

For every aligned TCP packet, protocol-declared TCP payload was calculated as:

`IPv4.total_length - IPv4.header_length - TCP.header_length`

Results:

- jNetPcap equals protocol geometry: **31,618/31,618**
- Scapy equals protocol geometry: **23,067/31,618**
- negative declared payload geometry: **0**

Among the 8,551 decoder disagreements:

- jNetPcap matches declared geometry: **8,551/8,551**
- Scapy matches declared geometry: **0/8,551**
- neither matches declared geometry: **0**

For the 8,284 cases where Scapy reports more payload than the protocol-declared value, the excess equals bytes beyond `IPv4.total_length` in:

**8,284/8,284**

The remaining 267 cases have captured IPv4 extent shorter than the declared IPv4 total length; jNetPcap nevertheless continues to match the protocol-declared geometry exactly.

## Frozen rule

For the validated Stage 20 historical CICFlowMeter/jNetPcap reconstruction path:

`TCP_payload_length = IPv4.total_length - IPv4.header_length - TCP.header_length`

This rule is frozen because:

1. it follows IPv4/TCP protocol header geometry;
2. pinned jNetPcap reproduces it on **31,618/31,618** aligned TCP packets;
3. it was derived without CICIDS2017 labels;
4. it is frozen before evaluating its effect on the 37 known S4 residual flows.

## Scientific boundary

This checkpoint does not:

- read flow labels,
- evaluate the 37 residuals,
- recompute S4,
- fit a packet-length formula,
- change lifecycle,
- change timeout,
- change historical flag serialization,
- open full Monday,
- access Tuesday, Wednesday, Thursday, or Friday,
- train a model,
- generate images.

Any subsequent residual improvement or non-improvement must be treated as validation of this pre-frozen rule and must not be used to alter the rule.

## Decision

**PROTOCOL_DERIVED_JNETPCAP_TCP_PAYLOAD_SEMANTICS_FROZEN_BEFORE_RESIDUAL_VALIDATION**
