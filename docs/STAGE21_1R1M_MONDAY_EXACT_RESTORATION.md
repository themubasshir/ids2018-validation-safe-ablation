# Stage21-1R1-M — Monday Exact Restoration and Durable Archive

## Status

**PASS — EXACT STAGE20 BYTE IDENTITY RESTORED**

Parent commit: `969eaf81c10fb8cf1e311c103b0bf5301500bbec`

Restoration receipt SHA256: `75ac58356cd03c6a6a3b1ca4fa778a0075defeb1154be53256ffe59562274362`

## Exact compact corpus

- flows: **528509**
- `encoded_bytes.bin`: `27e6f730c9951075f500bedc96b91d215b74a995ee23e1f09e269eaa7a2bd82c`
- `flow_offsets.npy`: `3744c55767896e98f5691210d6820224d9ae8315130ce74bb5d4264c25e4326e`
- `labels.npy`: `48792b8d6a127b35342cb0789baa6c54396f1100a60ce7225daf08d1c3530424`
- `packet_lengths.npy`: `16547aedafc3aaffcf9dca5ef50c7456cd823ed1ab59965a4c10520f11fb68f8`

## EOF restoration forensic result

The initial reconstruction matched all frozen scientific geometry and exact-S4
join counts but serialized the EOF-current tail in Python insertion order.
A bounded in-memory ordering test found that only `JAVA_HASHMAP_BUCKET_START`
reproduced all three order-dependent Stage20 hashes exactly. The corrected tail
then reproduced all four original compact payload hashes.

No representation, join, label, exclusion, model, or training rule changed.

## Durable archive

- release tag: `stage20-compact-corpora-v1`
- asset: `stage20-Monday-compact-corpus-v1.tar`
- archive bytes: **595261440**
- archive SHA256: `4f0b1a4a93df86fad5b11632da50dc12d3d4392b65f48b5e7bdefeea31706a20`

The archive checksum is a transport identity; the four original payload hashes
remain the scientific corpus identity.

## Boundary

- PCAP reread during correction: **NO**
- label source reread during correction: **NO**
- model forward: **NO**
- training: **NO**
- optimizer steps: **0**
