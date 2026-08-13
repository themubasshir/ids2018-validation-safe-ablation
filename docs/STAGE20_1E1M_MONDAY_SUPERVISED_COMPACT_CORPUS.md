# Stage20-1E1-M — Monday Supervised Compact Corpus

## Status

**MONDAY SUPERVISED COMPACT CORPUS MATERIALIZED AND AUDITED**

Parent:

`a66be0b93b24a376b4032225b0b11e76fdf1d6d5`

## Frozen boundaries

- split: **TRAIN**
- day: **Monday**
- representation: **64 × 256 × 1**
- encoder SHA256: `9883fe2b27020aaff707a753123b35eb3223d21abf295d056ec233e532f94222`
- join: **exact directed 21-field S4 only**
- architecture changed: **NO**
- model training: **NO**
- Thursday accessed: **NO**
- Friday accessed: **NO**
- Friday status: **CLOSED**

## Source identities

PCAP:

- `pcap/Monday-WorkingHours.pcap`
- revision: `e810c1cc98270ec271a1df917b9de0786c33f343`
- bytes: **10822507416**
- SHA256: `f6eac599358f216b074338813a1cf7be3cc4e91d116e13efc0dc71f2cca11972`

Traffic labels:

- `traffic_labels/Monday-WorkingHours.pcap_ISCX.csv.parquet`
- revision: `b7e532345512edcd530cb1770dc76636aeb52802`
- bytes: **65465382**
- SHA256: `dfdcef4b8670e52af54dc4f82174834365a393473e877174cca46d17b12dfd02`
- rows: **529918**

## Frozen S4 timestamp semantics

The already-validated Stage20-R3D S4 Timestamp field is the integer Unix epoch
second:

`int(flow.start_us // 1_000_000)`

The pinned parquet label Timestamp is normalized to the same integer epoch
second.

The failed R0 attempt incorrectly transformed both sides into the historical
12-hour exporter display string. That many-to-one transformation caused false
exact S4 collisions and produced 674/675 instead of the frozen 635/675 anchor.

R1 removes that transformation completely.

No timezone shift, string formatting, timestamp tolerance, or nearest-time
matching is used.

## Frozen S4 packet decoder

R2 uses the exact already-validated Stage20-R3D Scapy decoder:

- `pkt = Ether(raw_bytes)`
- outer `ip = pkt[IP]`
- transport = `ip.payload`
- direct TCP only when `isinstance(transport, TCP)`
- direct UDP only when `isinstance(transport, UDP)`
- TCP baseline payload = `len(bytes(tcp.payload))`
- UDP baseline payload = `len(bytes(udp.payload))`
- otherwise protocol = 0, ports = 0, payload length = 0

Raw captured frame extent is **not** used to calculate S4 payload length.

The separate raw Ethernet/VLAN locator is used only to retain the authentic
captured IPv4 byte prefix for the already-frozen packet-image representation.

## Mandatory first-50k forensic anchor

Before full materialization the implementation reproduced both already-frozen
Monday membership layers:

### Historical raw exact S4

- parser IPv4 TCP: **31618**
- parser IPv4 UDP: **14334**
- parser IPv4 protocol-0: **84**
- non-IPv4: **3964**
- completed flows: **675**
- FIN exports: **432**
- timeout exports: **243**
- protocol distribution: **{0: 1, 6: 467, 17: 207}**
- raw exact set membership: **637/675**
- raw exact multiset membership: **637/675**
- raw absent indices: **[14, 25, 35, 36, 40, 43, 45, 50, 52, 54, 57, 59, 63, 66, 68, 71, 119, 123, 124, 147, 148, 197, 198, 199, 277, 279, 281, 307, 309, 324, 327, 333, 334, 336, 337, 445, 448, 454]**

Historical raw decision:

**PASS — 637/675**

### D5 source-faithful acceptance

The pre-existing D5 forensic erratum independently excludes only indices
**471** and **473** after raw exact membership:

- index 471 reconstructed duration: **224 µs**
- index 473 reconstructed duration: **262 µs**
- both terminate by **FIN**
- both remain raw exact matches
- neither is allowed to consume a label occurrence in the source-faithful corpus

D5 source-faithful accepted:

**635/675**

D5 absent indices:

**[14, 25, 35, 36, 40, 43, 45, 50, 52, 54, 57, 59, 63, 66, 68, 71, 119, 123, 124, 147, 148, 197, 198, 199, 277, 279, 281, 307, 309, 324, 327, 333, 334, 336, 337, 445, 448, 454, 471, 473]**

D5 decision:

**PASS — 635/675**

No label duration is substituted.

## Full Monday reconstruction

- raw packets: **11709971**
- valid IPv4 packets: **11626492**
- exportable flows: **529601**
- retained packets: **11573331**
- FIN: **216388**
- FLOW_TIMEOUT: **120017**
- EOF_CURRENT: **193196**
- EOF singleton discarded: **52890**

All pre-existing full-Monday geometry/lifecycle anchors passed.

## Published exact S4 multiset

- rows: **529918**
- unique signatures: **529884**
- duplicate occurrences: **34**
- ambiguous binary signatures: **0**
- published binary counts: **{0: 529918}**

## Exact supervised join

- matched reconstructed flows: **528509**
- raw unmatched reconstructed flows: **1090**
- pre-frozen D5 duration/export exclusions: **2**
- D5 excluded indices: **[471, 473]**
- unused published occurrences: **1409**
- exact join coverage: **0.997938070359**
- matched class counts: **{0: 528509}**
- matched export reasons: **{'EOF_CURRENT': 192520, 'FIN': 216140, 'FLOW_TIMEOUT': 119849}**

No fuzzy, nearest, tolerance, reverse, or label-guided repair was performed.

The only non-raw-match exclusion is the already-frozen D5 forensic correction
for Monday bounded flow indices 471 and 473. Their accidental raw exact label
occurrences are not consumed.

Raw-unmatched reconstructed flows remain excluded exactly as preregistered.

## Compact corpus

Local directory:

`/kaggle/working/stage20_compact_corpus/Monday`

The corpus persists no dense zero padding.

Files:

- `encoded_bytes.bin` — 522845159 bytes — SHA256 `27e6f730c9951075f500bedc96b91d215b74a995ee23e1f09e269eaa7a2bd82c`
- `flow_offsets.npy` — 4228208 bytes — SHA256 `3744c55767896e98f5691210d6820224d9ae8315130ce74bb5d4264c25e4326e`
- `labels.npy` — 528637 bytes — SHA256 `48792b8d6a127b35342cb0789baa6c54396f1100a60ce7225daf08d1c3530424`
- `packet_lengths.npy` — 67649280 bytes — SHA256 `16547aedafc3aaffcf9dca5ef50c7456cd823ed1ab59965a4c10520f11fb68f8`

Loader:

`scripts/stage20_compact_corpus.py`

Loader SHA256:

`a1ba15881afeb1cf4de9225a06df9ae676b95f596c8ddced7734a445ba7624d0`

First **128** supervised flows round-tripped exactly against
the already-verified packet-image encoder.

Roundtrip summary SHA256:

`b563f6df968e631f3e4eeccb52c95fe0391f23afe516223f63dad58ba1841b49`

## Manifest

`results/stage20_1e_training/stage20_1e1m_monday_compact_corpus_manifest.json`

SHA256:

`a726d87e044e56171282e9be2fc6220c47de0cd09b153624062713f1c3116892`

## Raw-source release rule

The Monday PCAP and traffic-label cache objects remain present until this
manifest, audit, and the tested compact-corpus loader are committed, pushed,
remote-SHA verified, and the repository is clean.

Only then may those raw cache objects be released.

## Next

**Stage20-1E1-T — Tuesday supervised compact corpus**
