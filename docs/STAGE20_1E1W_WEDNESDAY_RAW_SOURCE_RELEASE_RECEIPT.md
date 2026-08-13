# Stage20-1E1-W — Wednesday Raw Source Release Receipt

## Status

**WEDNESDAY RAW PCAP AND LABEL CACHE RELEASED AFTER CORPUS SCIENCE DURABILITY**

Science commit: `f79c19f131323ec70be6abbb7aebfbc90a9f512a`

Manifest SHA256: `42a8f3813a786751999c209dce323ba701d9c29cd19add09aaadbd3297921d62`

## Safety ordering

The Wednesday raw PCAP and traffic-label parquet remained present until:

1. pinned source hashes passed;
2. full-Scapy reference-only execution was used; optimized parser was not exercised;
3. frozen first-50k Wednesday snapshot passed;
4. full Wednesday D2-W lifecycle/geometry anchors passed;
5. exact supervised S4 join completed;
6. compact corpus completed;
7. first 128 supervised flows round-tripped exactly;
8. every compact corpus file was hashed;
9. manifest + audit were committed and pushed;
10. remote SHA was verified and the worktree was clean.

Only then were raw cache objects released.

## Local corpus preserved

`/kaggle/working/stage20_compact_corpus/Wednesday`

Supervised flows: **12951**

## Workspace

- free bytes before release: **5892820992**
- free bytes after release: **19390152704**
- space reclaimed: **13497331712**
- remaining exact Wednesday PCAP/label-size objects: **0**

## Scientific state

- Monday corpus: **COMPLETE**
- Tuesday corpus: **COMPLETE**
- Wednesday corpus: **COMPLETE**
- Thursday accessed: **NO**
- Friday accessed: **NO**
- Friday status: **CLOSED**
- model training: **NO**
- optimizer steps: **0**

## Next

**Stage20-1E1-V — Thursday validation compact corpus**

Receipt: `results/stage20_1e_training/stage20_1e1w_wednesday_raw_source_release_receipt.json`

SHA256: `e4862c88d8fcf3aff36225b599d1d386f25701836eb717074f96a3535b509c0b`
