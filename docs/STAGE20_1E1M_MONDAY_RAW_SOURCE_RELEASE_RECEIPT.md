# Stage20-1E1-M — Monday Raw Source Release Receipt

## Status

**MONDAY RAW PCAP AND LABEL CACHE RELEASED AFTER CORPUS SCIENCE DURABILITY**

Science commit:

`962849617a6f9afb4a04a6b1791393e8b8c7f63f`

Manifest SHA256:

`a726d87e044e56171282e9be2fc6220c47de0cd09b153624062713f1c3116892`

## Safety ordering

The Monday raw PCAP and traffic-label parquet remained present until:

1. pinned source hashes passed;
2. the first-50k forensic S4 anchor passed;
3. full Monday lifecycle/geometry anchors passed;
4. exact supervised S4 join completed;
5. compact corpus completed;
6. first 128 supervised flows round-tripped exactly;
7. every compact corpus file was hashed;
8. manifest + audit + exact loader were committed;
9. the commit was pushed and remote-SHA verified;
10. the repository worktree was clean.

Only then were raw cache objects released.

## Local corpus preserved

`/kaggle/working/stage20_compact_corpus/Monday`

Supervised flows:

**528509**

## Workspace

Free bytes before release:

**8588140544**

Free bytes after release:

**19410673664**

Space reclaimed:

**10822533120**

Remaining exact Monday PCAP/label-size objects:

**0**

## Scientific state

- Monday corpus: **COMPLETE**
- Tuesday corpus: **PENDING**
- Wednesday corpus: **PENDING**
- Thursday accessed: **NO**
- Friday accessed: **NO**
- Friday status: **CLOSED**
- model training: **NO**
- optimizer steps: **0**

## Next

**Stage20-1E1-T — Tuesday supervised compact corpus**

## Receipt

`results/stage20_1e_training/stage20_1e1m_monday_raw_source_release_receipt.json`

SHA256:

`624feff7c9ba1d612322a61cd3d303014f48d7fb001569d3e06953cf623051bb`
