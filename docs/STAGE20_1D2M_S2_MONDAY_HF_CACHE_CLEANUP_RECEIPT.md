# Stage20-1D2-M-S2 — Monday HF Cache Cleanup

## Status

**MONDAY HF CACHE STORAGE RELEASED**

Parent:

`c3355498ea4a6529889a24888ab4ddb4d1bd12a4`

## Scientific state

The Monday exact geometry profile remains unchanged and remotely durable.

Scientific profile commit:

`b07153c7107a9dd0f875a88290ac418e9081d368`

Scientific profile SHA256:

`3a26d6499334c12ea4e9272aef4250761c6cf4399e7fb4d33ef236f12d0b7272`

## S1 finding

The dedicated Hugging Face cache retained the verified Monday source
after the original working-source pathname was deleted.

The following two paths resolved to the same underlying filesystem object:

- `/kaggle/working/stage20_hf_cache/datasets--bvsam--cic-ids-2017/blobs/f6eac599358f216b074338813a1cf7be3cc4e91d116e13efc0dc71f2cca11972`
- `/kaggle/working/stage20_hf_cache/datasets--bvsam--cic-ids-2017/snapshots/e810c1cc98270ec271a1df917b9de0786c33f343/pcap/Monday-WorkingHours.pcap`

## Cleanup

Removed:

1. Monday snapshot reference;
2. verified Monday blob.

No unrelated cache file was deleted.

Any parent directory was removed only with `rmdir()`, meaning it had to
already be empty.

## Storage

Free bytes before cleanup:

**9184653312**

Free bytes after cleanup:

**20007178240**

Increase:

**10822524928 bytes**

## Tuesday gate

Tuesday source:

**11048283608 bytes**

Operational headroom:

**1073741824 bytes**

Required:

**12122025432 bytes**

Available:

**20007178240 bytes**

Tuesday acquisition safe:

**True**

## Scientific boundary

This checkpoint:

- changed no Monday histogram;
- parsed no PCAP packets;
- computed no geometry;
- computed no P95;
- selected no dimensions;
- read no labels;
- did not download Tuesday;
- did not access Thursday;
- did not access Friday;
- performed no training.

## Next

**Stage20-1D2-T — Tuesday exact geometry profile**

## Artifact

`results/stage20_1d_representation/stage20_1d2m_s2_monday_hf_cache_cleanup_receipt.json`

SHA256:

`a657e4faac937822497a86a80a230f8165b995bde1aaa7932c2867b2534336da`
