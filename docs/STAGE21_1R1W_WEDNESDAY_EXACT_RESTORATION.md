# Stage21-1R1-W — Wednesday Exact Restoration and Durable Archive

## Status

**PASS — EXACT STAGE20 BYTE IDENTITY RESTORED**

Parent commit: `20ad127e1cf4fd43804160de74386abbe1f0e04d`

Restoration receipt SHA256: `f335dcc7f8ddb381befb6061e4378dcb48ca60b0db080599b6d99238a9b82c43`

Hybrid execution receipt SHA256: `015967ab55e94b6c49a7dec0857aa6b1fa4339866a584460e7b0bc96ff62fce5`

## Exact compact corpus

- flows: **12951**
- benign: **8657**
- attack: **4294**
- encoded authentic bytes: **13824937**
- `encoded_bytes.bin`: `b4ba9a059a2df6a1b85546b4d92c1fdf5b80feb61de6c3e56eae458c628f8889`
- `flow_offsets.npy`: `9ef83af5b03f9284beed50cbe2587bbbb8cac1ac524aa5505e44d262a8d8cf0a`
- `labels.npy`: `9d10b0264487ab4689a77f0101f22496786a7eb453236c2fb8bfe53d33f9ca7c`
- `packet_lengths.npy`: `9bba88e143d4c5c5388c450b1f7d7c9aa1cd83592c4c6e1a153651e70131d2ab`

## Restoration result

The full Wednesday reconstruction reproduced the frozen Stage20 packet geometry,
flow lifecycle, Java-HashMap-compatible EOF ordering, exact directed 21-field S4
join, class counts, export reasons, encoded-byte count, and all four compact
payload identities exactly.

The historical packet-image representation was recovered without changing the
frozen representation: authentic captured IPv4-layer bytes begin at IPv4 byte
zero, are capped at 256 bytes, and are not clipped to the IPv4 declared Total
Length.

A recovery-only hybrid implementation was used for the final replay after a
50,000-packet packet-by-packet equivalence gate against Scapy 2.6.1 produced
zero mismatched fields. The final frozen compact hashes are identical to the
historical Stage20 targets.

No representation, join, label, exclusion, model, threshold, or training rule
changed.

## Durable archive

- release tag: `stage20-compact-corpora-v1`
- asset: `stage20-Wednesday-compact-corpus-v1.tar`
- archive bytes: **15605760**
- archive SHA256: `4e89c85fbb537795ff93472b52fb7ceb21407111b1adceb0df9117d2c3d13a74`
- format: **deterministic uncompressed USTAR**
- internal root: `Wednesday/`

The archive SHA is a transport identity. The four original compact payload
SHA256 values remain the scientific corpus identity.

## Boundary

- PCAP read during seal/archive step: **NO**
- label-source read during seal/archive step: **NO**
- Thursday accessed: **NO**
- Friday accessed: **NO**
- model forward: **NO**
- training: **NO**
- optimizer steps: **0**
