# Stage21-1R1-V — Thursday Exact Restoration and Durable Archive

## Status

**PASS — EXACT STAGE20 BYTE IDENTITY RESTORED**

Parent commit: `ea60c4425db47752cb0a5ce00eb33334123c2445`

Source reacquisition receipt SHA256: `18e4114ebe72f7790ee1767c60e43059732082110145adb72d5cf2d9b400d7a1`

Hybrid equivalence receipt SHA256: `910533898258bc8295635f92eadc781055efa51b97708fc3ab6d54b16c9add7b`

Full restoration receipt SHA256: `3f0404832eec581b45452fc0716110c32ca02e2530bac7c21b71fd4755799767`

## Exact compact corpus

- role: **VALIDATION**
- flows: **8197**
- benign: **8155**
- attack: **42**
- encoded authentic bytes: **7586531**
- `encoded_bytes.bin`: `2593b328839ecf28d901242b6850474fa028484656c7235ff78ef2b437c01ca0`
- `flow_offsets.npy`: `137d38b8bfdcd22986e954f7b39ae4383da33b6194998ebb8fc8b63b3259e522`
- `labels.npy`: `cb1c6b3bf716ed9244029b5866ac3d0ca8da8b9bc152f8e89d5b1d6c78e5ec6e`
- `packet_lengths.npy`: `db195558d0a12f74e8d4ba8c1ccd7ee4b322993b42575793761c6991fdb1f21c`

## Restoration result

The Stage21 Thursday reconstruction reproduced the frozen Stage20 validation
geometry, lifecycle, exact directed 21-field S4 join, class counts, export
reasons, encoded-byte count, Java-HashMap-compatible EOF ordering, and all four
compact payload SHA256 identities exactly.

The recovery-only hybrid decoder was first checked packet-by-packet against
Scapy 2.6.1 for the first 50,000 packets. After conservatively adding TCP/3268
to the exact Scapy application-binding fallback, the equivalence gate produced
zero mismatched fields.

The full replay then reproduced the historical Stage20 Thursday byte identities
exactly.

No representation, label, join, architecture, threshold, model, or training
rule changed.

## Durable archive

- release tag: `stage20-compact-corpora-v1`
- asset: `stage20-Thursday-compact-corpus-v1.tar`
- archive bytes: **8714240**
- archive SHA256: `63cfb6d9dc4aa22317e4f847a43e6d1c72490ee8a3aab50e2e47ce6a437bdd4f`
- format: **deterministic uncompressed USTAR**
- internal root: `Thursday/`

The archive checksum is a transport identity. The four compact payload SHA256
values remain the scientific corpus identity.

## Boundary

- Friday accessed: **NO**
- model forward: **NO**
- training: **NO**
- optimizer steps: **0**
