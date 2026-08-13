# Stage20-1D0 — Packet-Image Representation Selection Lock

## Status

**REPRESENTATION SELECTION PROTOCOL FROZEN BEFORE TRAIN PROFILING**

Parent commit:

`9d531d5c6bb7f0bde05a07cdae247af319affed1`

The Stage20 reconstruction-mechanism branch is closed. No additional
mechanism candidate may be introduced.

This checkpoint freezes the packet-image representation procedure before
the complete TRAIN geometry distribution is examined.

## Split boundary

Representation dimensions will be derived from:

- Monday
- Tuesday
- Wednesday

only.

Thursday validation data is excluded from dimension selection.

Friday remains closed.

## Image topology

Each flow is represented as a two-dimensional byte matrix:

- rows = packets in original capture order
- columns = byte offsets within each packet
- channels = **1**

No flow concatenation, tabular-feature rendering, RGB replication, future
context, or cross-day context is allowed.

## Packet byte origin

Representation begins at **IPv4 byte 0**.

Ethernet, VLAN, PCAP metadata, and packet timestamps are excluded.

Captured IPv4 geometry is retained.

## Header policy

Selected connection-identity fields are zero-masked in place while byte
positions and packet length remain unchanged.

Masked IPv4 fields:

- Identification
- header checksum
- source address
- destination address

Masked TCP fields:

- sequence number
- acknowledgement number
- checksum

Masked UDP field:

- checksum

Retained fields include:

- protocol
- TTL
- TCP/UDP ports
- TCP flags
- TCP window/options
- payload bytes

## Padding

- short packets: right-zero padding
- short flows: bottom zero-packet rows
- a deterministic padding mask must accompany model input

## Truncation

- long flows: keep earliest packets
- long packets: keep earliest IPv4 bytes
- no sampling
- no random crop
- no label-guided crop

## Frozen dimension-selection rule

Final numeric dimensions are not selected in this checkpoint.

Using TRAIN only:

### Packets per flow

1. Compute nearest-rank empirical 95th percentile of flow packet counts.
2. Round upward to the smallest power of two.
3. Minimum: **16**
4. Maximum: **64**

If TRAIN P95 exceeds 64, use 64 and report the exact truncation rate.

### Bytes per packet

1. Compute nearest-rank empirical 95th percentile of captured IPv4 packet lengths.
2. Round upward to the smallest multiple of 32.
3. Minimum: **64**
4. Maximum: **256**

If TRAIN P95 exceeds 256, use 256 and report the exact truncation rate.

Maximum byte-image area is therefore frozen at:

**16,384 byte-pixels per flow**

before channels/padding masks.

## Leakage controls

Representation selection may not use:

- labels
- class balance
- attack identity
- Thursday geometry
- Friday geometry
- published tabular flow features
- SHAP rankings
- predictions
- thresholds

The same fixed representation must be used for TRAIN, VALIDATION, and
eventually HOLDOUT.

## Training boundary

Training remains prohibited.

Before model training we still must:

1. verify complete TRAIN raw sources;
2. profile TRAIN geometry once;
3. apply this frozen dimension rule;
4. freeze numeric packets-per-flow;
5. freeze numeric bytes-per-packet;
6. verify the deterministic encoder.

## Artifact

`results/stage20_1d_representation/stage20_1d0_packet_image_representation_selection_lock.json`

SHA256:

`a1adb03bd5fa7bba0e7df97c0c4ee5695cd6f92d3f49f4d0fbe0e69171df6407`

## Holdout integrity

- Friday requests: **0**
- Friday reads: **0**
- Friday openings: **0/1**
- Friday status: **CLOSED**
