# Stage 20.1C11 — Pinned jNetPcap Decoder Forensic Checkpoint

## Status

This checkpoint freezes the bounded Stage 20 packet-to-flow reconstruction and decoder-forensic state after recovery from a Kaggle runtime reset.

- Parent commit: `8b34b13b39738e7ae16626a65b2de586af088c46`
- Development source: Monday CICIDS2017 PCAP only
- Packet forensic bound: first **50,000** Monday packets
- Full Monday: **not authorized**
- Tuesday / Wednesday / Thursday: **not authorized**
- Friday holdout: **CLOSED, 0/1**
- Image generation: **not authorized**
- ViT training: **not authorized**

## 1. Reproduced corrected S4 result

The pre-reset Stage 20.1C9 bounded reconstruction was reproduced exactly:

- completed exportable flows: **675**
- exact corrected S4 membership: **637/675 = 0.943703703704**
- exact corrected S4 multiset: **637/675 = 0.943703703704**
- unmatched reconstructed flows: **38**
- FIN exact: **399/432**
- flow-timeout exact: **238/243**

The Kaggle reset therefore introduced no scientific drift in the bounded reconstruction.

## 2. Residual localization

Stage 20.1C10 reproduced the pre-reset residual localization exactly:

- full exact S4 candidate: **637**
- anchor absent: **1**
- lifecycle absent after anchor: **0**
- corrected physical flags absent after lifecycle: **0**
- length-only residual: **37**

All 37 length-only residuals are TCP.

For these 37 flows:

- all lifecycle fields already match exactly;
- all corrected physical flag fields already match exactly;
- every post-lifecycle/flag label candidate is unambiguous;
- forward packet-length minimum is exact in **37/37**;
- backward packet-length minimum is exact in **37/37**;
- the disagreement is concentrated in total and maximum packet-length statistics.

The one anchor-absent flow is a separate protocol-0 timeout case and is not attributed to the packet-length issue.

## 3. Pinned jNetPcap runtime

The packet decoder path is derived from the historical CICFlowMeter source and its bundled jNetPcap runtime.

Pinned CICFlowMeter runtime snapshot:

`98a5ebad0df579cc8b43eedd3421b3ae87699901`

Bundled runtime:

`jNetPcap 1.4.r1425`

The initial runtime failure was environmental: `libpcap.so` was missing from the Kaggle system.

Installing the operating-system `libpcap-dev` dependency resolved the native dependency.

Critically:

- the pinned `jnetpcap.jar` was not modified;
- `libjnetpcap.so` was not modified;
- `libjnetpcap-pcap100.so` was not modified;
- Java was not changed;
- no alternate decoder was substituted.

The minimal initialization probe then succeeded and reported:

`libpcap version 1.10.1 (with TPACKET_V3)`

## 4. Packet-identity comparison

The first direct jNetPcap-vs-Scapy compound-key comparison was stopped because the emitted row populations differed.

A raw-PCAP packet-index forensic then established:

- jNetPcap transport-classified rows: **45,981**
- Scapy TCP/UDP rows: **45,952**
- shared raw packet indices: **45,952**
- jNetPcap-only raw packet indices: **29**
- Scapy-only raw packet indices: **0**

For every one of the **45,952 shared raw packet indices**, the following identity fields are exact:

- timestamp: **45,952/45,952**
- source IP: **45,952/45,952**
- destination IP: **45,952/45,952**
- source port: **45,952/45,952**
- destination port: **45,952/45,952**
- protocol: **45,952/45,952**

Thus there is no identity disagreement among the shared packet population.

## 5. Stage 20.1C11R5 — fragmentation hypothesis rejected

The 29 jNetPcap-only raw packet indices were inspected using only IPv4 header metadata.

The raw packet headers show:

- IPv4 protocol distribution: **{1: 29}**
- therefore all 29 packets are raw IPv4 **ICMP**, not UDP;
- fragment offset > 0: **0/29**
- MF set: **0/29**
- any IPv4 fragmentation signal: **0/29**
- Scapy UDP layer present: **0/29**
- Scapy TCP layer present: **0/29**

The 29 packets form 16 `(src, dst, IP.id, IP.proto)` groups:

- group member-count distribution: `{1: 3, 2: 13}`
- groups with offset-0 member: **16/16**
- groups with final `MF=0` member: **16/16**
- groups with a Scapy UDP-decoded member: **0/16**

Therefore the proposed explanation that these 29 extra jNetPcap rows are IPv4 UDP fragments is **rejected**.

The prior jNetPcap observation table exposed these raw packet indices as protocol 17 with transport ports, while direct raw IPv4 inspection establishes protocol 1. The mechanism behind this jNetPcap transport-classification discrepancy remains unresolved and must not be guessed.

## 6. Scientific boundary

This checkpoint does **not** adopt a new packet-length formula.

It does **not** authorize payload comparison on the 29 discrepant rows.

It does **not** modify:

- S4,
- lifecycle,
- timeout,
- timestamp rules,
- historical flag serialization,
- packet-length semantics,
- train/validation/holdout protocol.

The unresolved S4 packet-length population remains **37/37 TCP**, while no TCP packet-identity disagreement has been observed in the shared packet population.

A future TCP-only decoder comparison may be performed only on exactly identity-aligned raw TCP packet indices and must remain independent of label-guided fitting.

## 7. Holdout integrity

Friday holdout access remains:

**0 / 1 — CLOSED**

No Friday request, read, or opening occurred in any experiment frozen by this checkpoint.

## Decision

**SUPPORTED FORENSIC CHECKPOINT WITH UNRESOLVED JNETPCAP TRANSPORT-CLASSIFICATION DISCREPANCY.**

The IPv4-fragmentation hypothesis is rejected. The TCP payload-length question remains open and must be investigated independently without label-guided formula selection.
