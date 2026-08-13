# Stage20-1E1-V — Thursday Raw Source Release Receipt

## Status

**THURSDAY RAW PCAP AND LABEL CACHE RELEASED AFTER VALIDATION CORPUS SCIENCE DURABILITY**

Science commit: `313f881319fab75a42c28cf271e042d26bb6f898`

Manifest SHA256: `93419837e38a7fea5ef9e183bdd78ceb9d719588c725bd2d1a3d91355cfffb04`

## Safety ordering

The Thursday raw PCAP and both validation-label parquets remained present until:

1. all three TRAIN corpora were already complete and remotely durable;
2. the frozen 1E0 representation, encoder, model definition, split policy, and
   exact S4 join rules were re-verified;
3. the Stage20-1E1-V-PRE Thursday source-ingestion erratum was already frozen
   and remotely durable before Thursday PCAP/join access;
4. all three Thursday source files passed their pinned SHA256 identities;
5. the Morning parquet physical/effective row counts matched the frozen erratum,
   yielding exactly 170366 Morning records plus 288602 Afternoon records;
6. full-Scapy reference-only execution was used; no optimized parser was
   exercised;
7. the descriptive first-50k Thursday internal invariants passed;
8. full Thursday reconstruction internal losslessness/lifecycle invariants
   passed;
9. exact validation S4 join completed without repair;
10. the compact validation corpus completed;
11. the first 128 validation flows round-tripped exactly;
12. every compact corpus file was hashed;
13. manifest + audit were committed and pushed;
14. remote SHA was verified and the worktree was clean;
15. all three Thursday source files were re-hashed against their pinned
    identities immediately before deletion.

Only then were raw Thursday cache objects released.

## Local validation corpus preserved

`/kaggle/working/stage20_compact_corpus/Thursday`

Validation flows: **8197**

Matched validation class counts:
**{0: 8155, 1: 42}**

## Workspace

- free bytes before release: **11031076864**
- free bytes after release: **19381186560**
- space reclaimed: **8350109696**
- remaining exact Thursday PCAP/label-size objects: **0**

## Scientific state

- Monday TRAIN corpus: **COMPLETE**
- Tuesday TRAIN corpus: **COMPLETE**
- Wednesday TRAIN corpus: **COMPLETE**
- Thursday VALIDATION corpus: **COMPLETE**
- Thursday model evaluation: **NO**
- Thursday threshold selection: **NO**
- Friday accessed: **NO**
- Friday status: **CLOSED**
- model training: **NO**
- optimizer steps: **0**

## Next

**Stage20-1E2 — train the single frozen Stage20MaskedCNNv1 for exactly 10 epochs
on Monday + Tuesday + Wednesday TRAIN corpora only.**

Receipt: `results/stage20_1e_training/stage20_1e1v_thursday_raw_source_release_receipt.json`

SHA256: `72e4457d2d56cf15e206022462f1b3e1cf5e77002a7002875cbb3d66032d5495`
