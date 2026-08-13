# Stage20-1E1-T — Tuesday Raw Source Release Receipt

## Status

**TUESDAY RAW PCAP AND LABEL CACHE RELEASED AFTER CORPUS SCIENCE DURABILITY**

Science commit: `ad70187d1a58ff55fdd36543333b5880dc7e3478`

Manifest SHA256: `20f920b576b49a36131fb271e963ef2bd7900f3c7bfc5458b24991676b5515af`

## Recovery note

R3 had already materialized and atomically finalized the Tuesday compact corpus,
then failed in reporting because it referenced the removed staging path.
Recovery did **not** rematerialize packets or rematch labels. The finalized
corpus and durable manifest were re-verified before the science commit.

## Safety ordering

The Tuesday raw PCAP and traffic-label parquet remained present until:

1. the finalized compact corpus and repository manifest matched byte-for-byte;
2. all frozen first-50k and full-Tuesday anchors were re-verified from the
   durable manifest;
3. every compact corpus file was re-hashed against the manifest;
4. the finalized corpus was successfully opened by the frozen loader;
5. manifest + audit were committed and pushed;
6. remote SHA was verified and the worktree was clean;
7. the exact raw PCAP and label cache were re-hashed against their pinned source
   identities.

Only then were raw cache objects released.

## Local corpus preserved

`/kaggle/working/stage20_compact_corpus/Tuesday`

Supervised flows: **4170**

Matched class counts: **{0: 4008, 1: 162}**

## Workspace

- free bytes before release: **8304869376**
- free bytes after release: **19405881344**
- space reclaimed: **11101011968**
- remaining exact Tuesday PCAP/label-size objects: **0**

## Scientific state

- Monday corpus: **COMPLETE**
- Tuesday corpus: **COMPLETE**
- Wednesday corpus: **PENDING**
- Thursday accessed: **NO**
- Friday accessed: **NO**
- Friday status: **CLOSED**
- model training: **NO**
- optimizer steps: **0**

## Next

**Stage20-1E1-W — Wednesday supervised compact corpus**

Receipt: `results/stage20_1e_training/stage20_1e1t_tuesday_raw_source_release_receipt.json`

SHA256: `bd3ce6fc365a59a07c6e6c592533a03406d17ffac49f5a9452c60e99b8ce2b02`
