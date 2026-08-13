# Stage20-1E1-T — Tuesday Supervised Compact Corpus

## Status

**TUESDAY SUPERVISED COMPACT CORPUS MATERIALIZED AND AUDITED**

Recovery note: the original R3 execution completed full materialization,
finalized the local compact corpus, and wrote the durable manifest, then failed
before the science commit because its Markdown summary attempted to `stat()` the
pre-rename `.Tuesday.staging/encoded_bytes.bin` path. This resume checkpoint
does **not** rematerialize or rematch any data. It re-verifies the finalized
corpus from its durable manifest and uses
`Tuesday/encoded_bytes.bin` for post-rename size reporting.

Parent: `4dfbed195bf98e2dc2f28c218728f4fc3d77670a`

## Scientific boundary

- Monday corpus complete: **YES**
- Tuesday split: **TRAIN**
- representation: **64 × 256 × 1**
- encoder SHA256: `9883fe2b27020aaff707a753123b35eb3223d21abf295d056ec233e532f94222`
- loader SHA256: `a1ba15881afeb1cf4de9225a06df9ae676b95f596c8ddced7734a445ba7624d0`
- join: **exact directed 21-field S4 only**
- architecture changed: **NO**
- representation changed: **NO**
- join rule changed: **NO**
- model training: **NO**
- optimizer steps: **0**
- Thursday accessed: **NO**
- Friday accessed: **NO**
- Friday status: **CLOSED**

## Source identities

PCAP:

- `pcap/Tuesday-WorkingHours.pcap`
- revision: `e810c1cc98270ec271a1df917b9de0786c33f343`
- bytes: **11048283608**
- SHA256: `080c2250154c5a174c03660ed0f75a3858d41a27511ba716e780d7bcb1ec4c57`

Traffic labels:

- `traffic_labels/Tuesday-WorkingHours.pcap_ISCX.csv.parquet`
- revision: `b7e532345512edcd530cb1770dc76636aeb52802`
- bytes: **52701751**
- SHA256: `27e83d518cb093faefd0f883cb4df3ad8b353f150934004f28d0e7962f9f31c4`
- rows: **445909**

Published binary row counts:

**{'0': 432074, '1': 13835}**

## Reference-only execution mode

Full Tuesday materialization used the frozen **Scapy 2.6.1 reference decoder
for every packet**, matching the successful Monday execution path.

The optimized decoder was retained only behind a bounded diagnostic
fast-vs-reference equivalence gate over the first
**250000** Tuesday packets and was not used
for the pilot lifecycle reconstruction or full corpus materialization.

- bounded diagnostic packet equality: **PASS**
- diagnostic IPv4 packets: **244430**
- diagnostic fast-path packets: **185730**
- diagnostic Scapy-fallback packets: **64270**
- diagnostic semantic digest: `6420d690048a7cd8448ec4c9a909df0454e3fd193640bdb24520823b3fe28939`

No timing, path share, or observed label coverage was used for scientific
selection.

## Frozen first-50k Tuesday snapshot

- parser: **{'IPv4_OTHER_PROTOCOL_0': 80, 'IPv4_TCP': 30626, 'IPv4_UDP': 15412, 'NON_IPV4': 3882}**
- completed flows: **928**
- FIN: **792**
- FLOW_TIMEOUT: **136**
- active flows at boundary: **3370**
- exact S4 set membership, descriptive: **2/928**
- exact S4 multiset membership, descriptive: **2/928**

All pre-existing D2-T first-50k anchors passed.

## Full Tuesday reconstruction

- raw packets: **11551954**
- valid IPv4 packets: **11469736**
- parser: **{'IPv4_OTHER_PROTOCOL_0': 750, 'IPv4_TCP': 10710230, 'IPv4_UDP': 758756, 'NON_IPV4': 82218}**
- exportable flows: **445769**
- retained packets: **11429532**
- FIN: **168634**
- FLOW_TIMEOUT: **108474**
- EOF_CURRENT: **168661**
- exportable flow protocol counts: **{'0': 197, '6': 245769, '17': 199803}**
- retained packet protocol counts: **{'0': 739, '6': 10670059, '17': 758734}**
- flow packet-count histogram exact D2-T match: **YES**
- timeout singleton discarded: **65**
- EOF singleton discarded: **40139**
- max active flows: **208800**

All pre-existing full-Tuesday D2-T anchors passed.

## Exact supervised join

- matched reconstructed flows: **4170**
- unmatched reconstructed flows: **441599**
- unused published occurrences: **441739**
- exact join coverage: **0.009354620891**
- matched class counts: **{0: 4008, 1: 162}**
- matched export reasons: **{'EOF_CURRENT': 1721, 'FIN': 1088, 'FLOW_TIMEOUT': 1361}**
- index-specific exclusions: **NONE**

No fuzzy, nearest, tolerance, reverse, label-guided repair, or post-hoc
signature modification was performed.

Observed exact coverage is descriptive and does not authorize modification of
the pre-registered join.

## Compact corpus

Local directory: `/kaggle/working/stage20_compact_corpus/Tuesday`

- flows: **4170**
- encoded authentic bytes: **4078271**
- first **128** supervised flows round-trip: **PASS**
- manifest SHA256: `20f920b576b49a36131fb271e963ef2bd7900f3c7bfc5458b24991676b5515af`
- finalized corpus re-hash from resume checkpoint: **PASS**

## Recovery integrity

The resume operation:

- did **not** read or parse the Tuesday PCAP for materialization;
- did **not** reconstruct flows again;
- did **not** re-run label matching;
- did **not** change any scientific count;
- did **not** change the manifest;
- did **not** access Thursday;
- did **not** access Friday.

Only the stale post-rename reporting path was corrected by reading
`/kaggle/working/stage20_compact_corpus/Tuesday/encoded_bytes.bin` instead of the removed staging path.

## Next

**Stage20-1E1-W — Wednesday supervised compact corpus**
