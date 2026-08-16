# Stage21-4R1 — Fast Exact Friday Restoration

## Status

**EXACT STAGE20 FRIDAY COMPACT CORPUS RESTORED AND DURABLY ARCHIVED**

## Frozen population

- flows: **12,088**
- BENIGN: **6,486**
- ATTACK: **5,602**

## Operational restoration path

The original Stage20 scientific target was not changed.

The restoration used:

- direct PCAPNG reader
- 20,000-packet raw/timestamp/wire-length equivalence gate against Scapy 2.6.1
- 20,000-packet packet-semantic equivalence gate against Scapy 2.6.1
- direct ordinary Ethernet/IPv4/TCP/UDP decoding
- Scapy 2.6.1 fallback for anomalous packets
- frozen directed 21-field S4 exact multiset join
- no fuzzy matching
- no nearest matching
- no tolerance matching
- no label-guided repair

Final acceptance required the already-frozen Stage20 historical reconstruction
geometry and all four exact compact-corpus SHA256 values.

## Exact compact identities

| File | Bytes | SHA256 |
|---|---:|---|
| encoded_bytes.bin | 8679226 | `f6dd1900f2767edc20a112b9f9875b3410667c3dace1dd2ff729cb3ce37952d2` |
| flow_offsets.npy | 96840 | `5e66ab4e85eb21eca8c7ea36c45461e1ac1f21d25acb0fb812c2221db02917aa` |
| labels.npy | 12216 | `239b124119824fac23cff9fdcfbc24bc46227a0b6d4b1ad2201e955c263347d8` |
| packet_lengths.npy | 1547392 | `f1790f6e9ddc9f24954cf72eb72359c7052e8736cdb97516afff74b7805ba878` |

## Durable archive

- release tag: `stage20-compact-corpora-v1`
- release ID: **371092195**
- archive asset ID: **516711485**
- bytes: **10342400**
- SHA256: `f69f09c096dc92e1c467a9f72873f54b1ddb9af739ff517d047ba6ee2c4402c8`
- remote stream byte identity: **PASS**

## Stage21 boundary

- Friday ViT constructed: **NO**
- Friday ViT inference: **NO**
- Friday probabilities: **NO**
- threshold search: **NO**
- threshold reselection: **NO**
- training: **NO**
- optimizer steps: **0**

## Next

Rebuild the frozen Torch 2.10.0+cu126 runtime and perform exactly one
Stage21 ViT Friday locked reuse-benchmark inference pass using only the frozen
thresholds **0.50 / 0.42 / 0.24**.
