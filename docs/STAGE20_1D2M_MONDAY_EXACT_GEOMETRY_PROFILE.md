# Stage20-1D2-M — Monday Exact Geometry Profile

## Status

**MONDAY EXACT GEOMETRY PROFILE COMPLETE**

Parent commit:

`c7882eb17be1ad8bb67d57fb7a20dbc578f9b9ea`

## Split

Monday is TRAIN.

Thursday was not accessed.

Friday remains closed.

## Source verification

- source: `Monday-WorkingHours.pcap`
- bytes: **10822507416**
- SHA256: `f6eac599358f216b074338813a1cf7be3cc4e91d116e13efc0dc71f2cca11972`
- frozen source revision: `e810c1cc98270ec271a1df917b9de0786c33f343`
- verified: **True**

## Source-faithful reconstruction

Parser:

`STAGE20_FROZEN_IPV4_DIRECT_TRANSPORT_TCP6_UDP17_OTHER0`

Lifecycle:

`CICFLOWMETER_FLOWGENERATOR_EAA853DD82F08BA5288BB7F295B471DE7313F883`

Flow-ID semantics:

`BASICPACKETINFO_JAVA_SIGNED_IPV4_FIRST_DIFFERING_BYTE_SWAP_IPS_AND_PORTS_TOGETHER`

Flow timeout:

**120000000 µs**

Historical EOF behavior is preserved: current flows with more than one
packet are included.

## First-50k forensic anchor

Parser population:

`{'IPv4_TCP': 31618, 'NON_IPV4': 3964, 'IPv4_OTHER_PROTOCOL_0': 84, 'IPv4_UDP': 14334}`

Completed exportable flows:

**675**

Termination:

- FIN: **432**
- FLOW_TIMEOUT: **243**

Status:

**PASS**

## Full Monday counts

- raw packets: **11709971**
- valid IPv4 packets: **11626492**
- exportable flows: **529601**
- retained packets in exportable flows: **11573331**
- timeout singleton flows discarded: **271**
- EOF current exportable flows: **193196**
- EOF singleton flows discarded: **52890**
- maximum simultaneously active flows: **246086**

## Export reasons

`{'EOF_CURRENT': 193196, 'FIN': 216388, 'FLOW_TIMEOUT': 120017}`

## Parser population

`{'IPv4_OTHER_PROTOCOL_0': 984, 'IPv4_TCP': 10718469, 'IPv4_UDP': 907039, 'NON_IPV4': 83479}`

## Lossless geometry statistics

The machine-readable artifact preserves the complete exact frequency
histograms for:

1. flow packet count;
2. captured IPv4 packet length.

No raw observation is approximated for the later empirical TRAIN P95.

Losslessness checks:

- flow histogram frequencies: **529601**
- exportable flows: **529601**
- weighted flow packet total: **11573331**
- retained packets: **11573331**
- packet-length histogram frequencies: **11573331**

All equalities:

**True**

## Critical selection boundary

This checkpoint does **not** calculate a Monday P95.

It does **not** choose Monday image dimensions.

The final P95 remains forbidden until Monday, Tuesday, and Wednesday exact
histograms are summed into one complete TRAIN histogram.

## Raw-PCAP deletion

This profile is committed and remotely verified **before** deletion.

Only after that remote durability checkpoint succeeds may the Monday raw
PCAP be removed.

A separate deletion receipt is created afterward.

## Artifact

`results/stage20_1d_representation/stage20_1d2m_monday_exact_geometry_profile.json`

SHA256:

`3a26d6499334c12ea4e9272aef4250761c6cf4399e7fb4d33ef236f12d0b7272`

## Holdout integrity

- labels read: **NO**
- Thursday accessed: **NO**
- Friday accessed: **NO**
- Friday status: **CLOSED**
- model training: **NO**
