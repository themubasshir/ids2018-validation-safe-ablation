# Stage20-1E1-V — Thursday Validation Compact Corpus

## Status

**THURSDAY VALIDATION COMPACT CORPUS MATERIALIZED AND AUDITED**

Parent: `e3de311ad54b82810d339aca54fa1b83664adb23`

## Scientific boundary

- Monday TRAIN corpus complete: **YES**
- Tuesday TRAIN corpus complete: **YES**
- Wednesday TRAIN corpus complete: **YES**
- Thursday role: **VALIDATION**
- representation: **64 × 256 × 1**
- encoder SHA256: `9883fe2b27020aaff707a753123b35eb3223d21abf295d056ec233e532f94222`
- loader SHA256: `a1ba15881afeb1cf4de9225a06df9ae676b95f596c8ddced7734a445ba7624d0`
- join: **exact directed 21-field S4 only**
- architecture changed: **NO**
- representation changed: **NO**
- join rule changed: **NO**
- model training: **NO**
- optimizer steps: **0**
- Thursday model evaluation: **NO**
- Thursday threshold selection: **NO**
- Friday accessed: **NO**
- Friday status: **CLOSED**

## Source identities

PCAP:
- `pcap/Thursday-WorkingHours.pcap`
- revision: `e810c1cc98270ec271a1df917b9de0786c33f343`
- bytes: **8302500180**
- SHA256: `38f8b1bb276849bf1721f7c4de22bebfa7f59a74e52286d4c0a37edbb118fe01`

Traffic labels:

- `traffic_labels/Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv.parquet`
  - revision: `b7e532345512edcd530cb1770dc76636aeb52802`
  - bytes: **19674280**
  - SHA256: `d8110c04a7af91124ada1c5ad901c4210879df1af8882dc637767532e7165350`
  - physical rows: **458968**
  - effective label records: **170366**
  - structural NULL padding rows: **288602**
- `traffic_labels/Thursday-WorkingHours-Afternoon-Infilteration.pcap_ISCX.csv.parquet`
  - revision: `b7e532345512edcd530cb1770dc76636aeb52802`
  - bytes: **27901448**
  - SHA256: `5da010354f0fc1040fd1fe65967096e1063475de8dd30ae4f657c07201d728a7`
  - physical rows: **288602**
  - effective label records: **288602**
  - structural NULL padding rows: **0**

Physical parquet rows across both pinned label files: **747570**

Effective Thursday label records after the frozen source-ingestion erratum:
**458968**

## Frozen Thursday label source-ingestion erratum

Artifact:
`results/stage20_1e_training/stage20_1e1v_thursday_label_source_ingestion_erratum.json`

The erratum was frozen and remotely durable before this Stage20-1E1-V run
opened the Thursday PCAP or executed any exact S4 join.

For the pinned Morning WebAttacks parquet only:

- physical rows: **458968**
- effective records: **170366** (physical ordinals 1..170366)
- verified all-85-column-NULL contiguous EOF suffix:
  **288602** rows (physical ordinals 170367..458968)
- classification of that suffix: `NON_RECORD_STRUCTURAL_NULL_PADDING`

The pinned Afternoon Infilteration parquet contributes all **288602** records.

The E0 rule for actual records is unchanged: NULL/empty Label or NULL frozen S4
field is a checkpoint failure. No imputation, repair, fuzzy, nearest, or
tolerance matching is introduced.

## Reference-only execution mode

Full Thursday materialization used the **frozen Scapy 2.6.1 reference decoder
for every packet**, matching the successful Monday/Tuesday/Wednesday
scientific materialization semantics.

No optimized parser is exercised in Stage20-1E1-V.

- optimized parser exercised: **NO**
- fast-parser equivalence gate: **NOT APPLICABLE**
- decoder selection based on observed traffic or labels: **NO**
- observed validation coverage used to modify protocol: **NO**

## First-50k Thursday snapshot

Thursday has no pre-existing Stage20-1D2 validation geometry profile because
Stage20-1D representation geometry was selected from TRAIN only. Therefore this
snapshot is descriptive and is not an external anchor.

- parser: **{'NON_IPV4': 2345, 'IPv4_TCP': 38640, 'IPv4_UDP': 8966, 'IPv4_OTHER_PROTOCOL_0': 49}**
- completed flows: **518**
- FIN: **460**
- FLOW_TIMEOUT: **58**
- active flows at boundary: **1642**
- exact S4 set membership, descriptive: **10/518**
- exact S4 multiset, descriptive: **10/518**
- internal invariants: **PASS**

## Full Thursday reconstruction

- raw packets: **9322025**
- valid IPv4 packets: **9240723**
- parser: **{'NON_IPV4': 81302, 'IPv4_TCP': 8538148, 'IPv4_UDP': 700922, 'IPv4_OTHER_PROTOCOL_0': 1653}**
- exportable flows: **458596**
- retained packets: **9205108**
- FIN: **142952**
- FLOW_TIMEOUT: **95384**
- EOF_CURRENT: **220260**
- exportable flow protocol counts: **{6: 274688, 17: 183758, 0: 150}**
- retained packet protocol counts: **{6: 8502564, 17: 700900, 0: 1644}**
- timeout singleton discarded: **76**
- EOF singleton discarded: **35539**
- max active flows: **255800**
- external pre-existing Thursday D2 anchors: **NONE BY DESIGN**
- internal losslessness/lifecycle invariants: **PASS**

## Exact validation join

- matched reconstructed flows: **8197**
- unmatched reconstructed flows: **450399**
- unused published occurrences: **450771**
- exact join coverage: **0.017874120141**
- matched class counts: **{0: 8155, 1: 42}**
- matched export reasons: **{'EOF_CURRENT': 4226, 'FIN': 2395, 'FLOW_TIMEOUT': 1576}**
- index-specific exclusions: **NONE**

No fuzzy, nearest, tolerance, reverse, label-guided repair, or post-hoc
signature modification was performed.

This corpus is materialized before training as frozen Stage20-1E0 requires.
No model inference or threshold selection is performed in Stage20-1E1-V.

## Compact corpus

Local directory: `/kaggle/working/stage20_compact_corpus/Thursday`

- flows: **8197**
- encoded authentic bytes: **7586531**
- first **128** validation flows round-trip: **PASS**
- manifest SHA256: `93419837e38a7fea5ef9e183bdd78ceb9d719588c725bd2d1a3d91355cfffb04`

## Next

**Stage20-1E2 — train the single frozen Stage20MaskedCNNv1 for exactly 10 epochs
using TRAIN corpora only (Monday + Tuesday + Wednesday).**
