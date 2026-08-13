# Stage20-1E1-W — Wednesday Supervised Compact Corpus

## Status

**WEDNESDAY SUPERVISED COMPACT CORPUS MATERIALIZED AND AUDITED**

Parent: `a01365bcc0fb0e142802b542697fa717199ae012`

## Scientific boundary

- Monday corpus complete: **YES**
- Wednesday split: **TRAIN**
- representation: **64 × 256 × 1**
- encoder SHA256: `9883fe2b27020aaff707a753123b35eb3223d21abf295d056ec233e532f94222`
- loader SHA256: `a1ba15881afeb1cf4de9225a06df9ae676b95f596c8ddced7734a445ba7624d0`
- join: **exact directed 21-field S4 only**
- architecture changed: **NO**
- model training: **NO**
- Thursday accessed: **NO**
- Friday accessed: **NO**
- Friday status: **CLOSED**

## Source identities

PCAP:
- `pcap/Wednesday-workingHours.pcap`
- revision: `e810c1cc98270ec271a1df917b9de0786c33f343`
- bytes: **13420789612**
- SHA256: `cd2674db7559a53f24bc03be3239b315700174ccaef72d10f5edc4c1a08f6186`

Traffic labels:
- `traffic_labels/Wednesday-workingHours.pcap_ISCX.csv.parquet`
- revision: `b7e532345512edcd530cb1770dc76636aeb52802`
- bytes: **76512727**
- SHA256: `d23a259820b16e1ad54f9f3b58d5727c5032d383015f90bc7c07cebbdf8a7140`
- rows observed from pinned parquet: **692703**

## Reference-only execution mode

Full Wednesday materialization used the **frozen Scapy 2.6.1 reference decoder
for every packet**, matching the successful Monday execution path.

No optimized parser is exercised in Stage20-1E1-W. The first-50k pilot
and the full Wednesday corpus materialization both use the same frozen
full-Scapy packet decoder.

- optimized parser exercised: **NO**
- fast-parser equivalence gate: **NOT APPLICABLE**
- decoder selection based on observed traffic or labels: **NO**

No timing or observed label coverage is used for scientific selection.

## Frozen first-50k Wednesday snapshot

- parser: **{'IPv4_UDP': 4172, 'NON_IPV4': 1031, 'IPv4_TCP': 44782, 'IPv4_OTHER_PROTOCOL_0': 15}**
- completed flows: **184**
- FIN: **129**
- FLOW_TIMEOUT: **55**
- active flows at boundary: **750**
- exact S4 set membership, descriptive: **1/184**
- exact S4 multiset, descriptive: **1/184**

All pre-existing D2-W first-50k anchors passed.

## Full Wednesday reconstruction

- raw packets: **13788878**
- valid IPv4 packets: **13705555**
- parser: **{'IPv4_UDP': 761639, 'NON_IPV4': 83323, 'IPv4_TCP': 12943316, 'IPv4_OTHER_PROTOCOL_0': 600}**
- exportable flows: **692389**
- retained packets: **13658697**
- FIN: **391925**
- FLOW_TIMEOUT: **123075**
- EOF_CURRENT: **177389**
- exportable flow protocol counts: **{6: 489442, 17: 202851, 0: 96}**
- retained packet protocol counts: **{6: 12896496, 17: 761611, 0: 590}**
- flow packet-count histogram exact D2-W match: **YES**
- timeout singleton discarded: **2059**
- EOF singleton discarded: **44799**
- max active flows: **222188**

All pre-existing full-Wednesday D2-W anchors passed.

## Exact supervised join

- matched reconstructed flows: **12951**
- unmatched reconstructed flows: **679438**
- unused published occurrences: **679752**
- exact join coverage: **0.018704803225**
- matched class counts: **{0: 8657, 1: 4294}**
- matched export reasons: **{'EOF_CURRENT': 3062, 'FIN': 7017, 'FLOW_TIMEOUT': 2872}**
- index-specific exclusions: **NONE**

No fuzzy, nearest, tolerance, reverse, label-guided repair, or post-hoc
signature modification was performed.

## Compact corpus

Local directory: `/kaggle/working/stage20_compact_corpus/Wednesday`

- flows: **12951**
- encoded authentic bytes: **13824937**
- first **128** supervised flows round-trip: **PASS**
- manifest SHA256: `42a8f3813a786751999c209dce323ba701d9c29cd19add09aaadbd3297921d62`

## Full-run parser optimization

- fast-path packets: **0**
- Scapy fallback packets: **13788878**
- fast-path share: **0.000000**

This is an operational implementation property only.

## Next

**Stage20-1E1-V — Thursday validation compact corpus**
