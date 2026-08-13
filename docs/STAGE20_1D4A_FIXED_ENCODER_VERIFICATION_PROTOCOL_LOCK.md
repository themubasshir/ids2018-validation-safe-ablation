# Stage20-1D4-A — Fixed Packet-Image Encoder Verification Protocol Lock

## Status

**FIXED PACKET-IMAGE ENCODER VERIFICATION PROTOCOL FROZEN**

Parent:

`314c128a0fe2091bd0784a8e904efe6435af925c`

## Frozen numeric geometry

- rows: **64**
- columns: **256**
- channels: **1**
- area: **16384**

These values are inherited from Stage20-1D3 and cannot change.

## Encoder input

Each encoder input is one source-faithful exportable flow.

Packets remain in original capture order.

Each packet begins at authentic captured IPv4 byte 0.

Ethernet, VLAN, PCAP metadata, and timestamps are not encoded.

## Fixed truncation

Flow truncation:

**earliest 64 packets**

Packet truncation:

**earliest 256 captured IPv4 bytes**

No sampling, random crop, center crop, label-guided crop, or validation-guided crop is permitted.

## Fixed padding

- packet byte padding: right-zero
- flow row padding: bottom-zero
- padding mask: required Boolean matrix of shape `64 x 256`

`True` means an authentic retained captured IPv4 byte position.

`False` means right padding or bottom flow padding.

An authentic source byte whose value is already zero remains `mask=True`.

A masked identity/header field is set to zero but remains `mask=True` because its position is authentic rather than padding.

## Fixed IPv4 masks

Offsets relative to IPv4 byte 0:

| Field | Bytes |
|---|---|
| Identification | 4:6 |
| Header checksum | 10:12 |
| Source address | 12:16 |
| Destination address | 16:20 |

Protocol, TTL, and fragmentation fields remain unchanged.

## Fixed TCP masks

For direct TCP only, offsets relative to TCP start (`IHL * 4`):

| Field | Relative bytes |
|---|---|
| Sequence number | 4:8 |
| Acknowledgement number | 8:12 |
| Checksum | 16:18 |

TCP ports, flags, window, options, and payload remain unchanged.

## Fixed UDP masks

For direct UDP only:

| Field | Relative bytes |
|---|---|
| Checksum | 6:8 |

UDP ports and payload remain unchanged.

## Real-source verification sample

Source:

`pcap/Monday-WorkingHours.pcap`

Revision:

`e810c1cc98270ec271a1df917b9de0786c33f343`

Bytes:

`10822507416`

SHA256:

`f6eac599358f216b074338813a1cf7be3cc4e91d116e13efc0dc71f2cca11972`

Selection:

**FIRST 16 EXPORTABLE FLOWS IN HISTORICAL EXPORT ORDER**

This sample cannot be replaced after observing encoded data.

It is not selected by label, protocol, size, truncation status, padding status, pixel content, or model result.

## Synthetic verification

Frozen fixture set:

- **SYN_TCP_STANDARD_IHL** — Verify IPv4 ID/checksum/address masks plus TCP seq/ack/checksum masks while ports/flags/window/payload remain unchanged.
- **SYN_UDP_STANDARD_IHL** — Verify IPv4 masks plus UDP checksum mask while ports and payload remain unchanged.
- **SYN_IPV4_OTHER_PROTOCOL** — Verify only IPv4 fixed masks apply when there is no direct TCP/UDP transport.
- **SYN_NONINITIAL_TCP_FRAGMENT** — Verify IPv4 protocol 6 in a non-initial fragment does not trigger TCP transport masking.
- **SYN_TCP_IPV4_OPTIONS_IHL24** — Verify TCP mask offsets are derived dynamically from IPv4 IHL.
- **SYN_AUTHENTIC_ZERO_VS_PADDING** — Verify an authentic zero-valued byte has mask=True while right/bottom padding has mask=False.
- **SYN_BYTE_TRUNCATION_300_TO_256** — Verify earliest 256 IPv4 bytes are retained and later bytes are excluded.
- **SYN_ROW_TRUNCATION_70_TO_64** — Verify earliest 64 packets are retained in original order and final six are excluded.

## Acceptance

Every synthetic fixture must pass.

For all 16 real TRAIN flows:

- repeated encoding must be byte-identical;
- repeated mask generation must be identical;
- masked retained fields must be exactly zero;
- retained unmasked positions must equal authentic source bytes;
- padding must be zero with mask `False`;
- masked/authentic zero positions remain mask `True`.

Any failure stops encoder freeze.

Architecture selection and model training remain prohibited.

## Storage execution

Stage20-1D4-B will reacquire Monday only.

The Hugging Face cache object is used directly.

No second full copy is created.

Packet scanning stops after the frozen first 16 exportable flows have been collected.

Verification artifacts are committed, pushed, and remote-SHA verified before the Monday raw cache is released again.

## Scientific boundary

This checkpoint:

- opened **0** PCAP files;
- read **0** PCAP packet bytes;
- downloaded **nothing**;
- observed **0** real sample flows;
- read **no labels**;
- accessed **no Thursday data**;
- accessed **no Friday data**;
- selected **no architecture**;
- trained **no model**.

## Next

**Stage20-1D4-B — Execute Fixed Encoder Verification**

## Artifact

`results/stage20_1d_representation/stage20_1d4a_fixed_encoder_verification_protocol_lock.json`

SHA256:

`3401ffe0d63c27ce3fb4b4535a64a8f4e3194da177cbd34798c39cb7c0615cdb`

## Holdout integrity

- Thursday accessed: **NO**
- Friday accessed: **NO**
- Friday status: **CLOSED**
