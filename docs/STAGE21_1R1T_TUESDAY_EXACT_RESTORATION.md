# Stage21-1R1-T — Tuesday Exact Restoration and Durable Archive

## Status

**PASS — EXACT STAGE20 BYTE IDENTITY RESTORED**

Parent commit: `30f73ad7bdfd8e49270e7bdc33254c634e3c8c0e`

Restoration receipt SHA256: `282a6e06114d40b9203f43188734ca483d8d2029fafa1a7d1acf0cef0f6194fc`

## Exact compact corpus

- flows: **4170**
- benign: **4008**
- attack: **162**
- `encoded_bytes.bin`: `cbfe435fe612e1a5e6f8dc44e5a6694cf1ce6efbe0dc6e89c5c62e4dc5da4f48`
- `flow_offsets.npy`: `4b9334dc876362b8937d21de276a03654e275b94a2c6fc4b23e0881d4d518be9`
- `labels.npy`: `e8891a80aea004b84cffb3fa4c53a71d32ae96796ac052e7073530a1b0cc9fff`
- `packet_lengths.npy`: `058641aa2e24aa9a308fd553ecae571867c478063dfe1261551285d81965808c`

## Restoration result

The full Tuesday reconstruction reproduced all frozen Stage20 geometry,
lifecycle, exact-S4 join, class counts, export reasons, encoded-byte count, and
all four compact payload SHA256 identities exactly.

The frozen timestamp rule remained integer Unix epoch second. The Stage21
implementation converted the parquet `datetime64[us]` values explicitly to
`datetime64[s]` before integer conversion; this corrected a Stage21 diagnostic
unit bug without changing the frozen scientific rule.

EOF-current serialization used the Java-HashMap-compatible operational order
recovered byte-for-byte during Monday restoration.

No representation, join, label, exclusion, model, or training rule changed.

## Durable archive

- release tag: `stage20-compact-corpora-v1`
- asset: `stage20-Tuesday-compact-corpus-v1.tar`
- archive bytes: **4659200**
- archive SHA256: `8c5f431885e95aa10a623ddfaf59913924e5b54af2ea9444dca2d4729e71ed69`

The archive checksum is a transport identity; the four original payload hashes
remain the scientific corpus identity.

## Boundary

- PCAP read during this seal/archive step: **NO**
- label-source read during this seal/archive step: **NO**
- model forward: **NO**
- training: **NO**
- optimizer steps: **0**
