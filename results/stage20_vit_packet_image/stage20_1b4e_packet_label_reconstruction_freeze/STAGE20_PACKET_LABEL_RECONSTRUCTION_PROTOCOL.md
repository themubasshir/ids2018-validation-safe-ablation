# Stage 20.1B4E — Packet-to-Label Reconstruction Protocol

## Status

**FROZEN**

This protocol closes the metadata-side design required before
raw CICIDS2017 packet acquisition.

## Why the earlier temporal-envelope method is rejected

Canonicalizing a flow into an undirected or bidirectional tuple
created substantial label-side ambiguity.

Across development data:

- 706,745 flow rows share an exact bidirectional tuple and
  timestamp with another row.
- 971,050 rows overlap another same-tuple temporal envelope.
- 9,024 exact tuple+timestamp groups contain both BENIGN and
  ATTACK labels.

Therefore direct packet assignment by a canonical bidirectional
tuple and time interval is prohibited.

## Direction must be preserved

CICFlowMeter defines forward direction from the first packet of
a bidirectional flow.

Stage 20 therefore preserves the directed source/destination
orientation produced by reconstructed flow formation.

No endpoint sorting or bidirectional tuple canonicalization is
permitted for label matching.

## Frozen reconstruction parameters

The Monday pilot uses CICFlowMeter-compatible flow semantics with:

- Flow Timeout: 120,000,000 microseconds
- Activity Timeout: 5,000,000 microseconds

These values are fixed before raw PCAP evaluation.

They may not be searched or adjusted after observing Monday
matching performance.

## Frozen S4 packet-reproducible signature

Binary labels are assigned from an exact directed-flow signature
containing:

1. Source IP
2. Source Port
3. Destination IP
4. Destination Port
5. Protocol
6. Timestamp
7. Flow Duration
8. Total Fwd Packets
9. Total Backward Packets
10. Total Length of Fwd Packets
11. Total Length of Bwd Packets
12. Fwd Packet Length Min
13. Fwd Packet Length Max
14. Bwd Packet Length Min
15. Bwd Packet Length Max
16. FIN Flag Count
17. SYN Flag Count
18. RST Flag Count
19. PSH Flag Count
20. ACK Flag Count
21. URG Flag Count

All of these fields are packet-reproducible flow properties.

Across all 2,127,498 development labeled flows, the S4
signature produced:

- mixed binary-label groups: 0
- mixed binary-label rows: 0
- binary deterministic rate: 1.000000000000

## Duplicate signatures

A small number of exact S4 duplicate rows remain.

These do not prevent binary label assignment because every exact
duplicate signature maps to the same binary class.

Stage 20 does not claim recovery of a unique original CSV row.

If any signature maps to both BENIGN and ATTACK, execution must
abort.

## Nonpositive duration flows

Negative and zero Flow Duration values remain unchanged.

They are not:

- converted with abs()
- clipped
- changed to zero
- removed
- used through an invented temporal-envelope repair

This is necessary because 952 development attack flows have
nonpositive Flow Duration.

## Prohibited matching

The following are prohibited:

- nearest-timestamp matching
- nearest-neighbor signature matching
- numeric tolerance search
- timeout search
- label-guided matching
- attack-guided disambiguation
- majority voting across conflicting binary labels
- posthoc signature modification after the Monday PCAP is read

## Monday pilot

The next stage may download only Monday's raw PCAP.

It will test whether the frozen flow reconstruction procedure
generates S4 signatures that reproduce the development label
index.

No images or models are created during that pilot.

If reconstruction fails materially, Stage 20 must report the
failure rather than tune reconstruction parameters after seeing
the result.

## Holdout

Friday remains closed at 0 / 1.
