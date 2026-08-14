# Stage20-1E4-COLAB-XET-FIXED4-PRE

**AUTHENTICATED XET FIXED-CONCURRENCY TRANSPORT FROZEN BEFORE RESUME**

Parent recovery commit: `1c15d614e2f79f9bb209cc607f93c0da5249be64`

Transport lock JSON SHA256: `ea7f8501681fe9271fcb2524d1467317f2d3814269e1a967ecb7489e399da2e8`

## Scientific boundary

The scientific protocol is unchanged.

At this lock:

- Friday PCAP full-size materialized: **NO**
- Friday PCAP SHA256 verified: **NO**
- Friday label contents parsed: **NO**
- Stage20 `RawPcapReader` scientific pass started: **NO**
- final Friday compact corpus: **NO**
- model inference: **NO**
- probabilities/metrics observed: **NO**

Exactly one Friday PCAP scientific reconstruction pass and exactly one model
inference pass remain.

## Frozen transport recovery

The next source-materialization attempt must use authenticated Hugging Face XET
with the following operational configuration:

- `HF_HUB_DISABLE_XET`: **unset / false**
- `HF_XET_FIXED_DOWNLOAD_CONCURRENCY=4`
- `HF_XET_NUM_CONCURRENT_RANGE_GETS=4`
- `HF_XET_HIGH_PERFORMANCE`: **unset / false**
- `HF_XET_CHUNK_CACHE_SIZE_BYTES=0`
- `HF_XET_RECONSTRUCT_WRITE_SEQUENTIALLY`: **unset / false**
- Hugging Face authentication credential: **required**
- token value persisted or printed: **NO**

The exact pinned Friday PCAP size and SHA256 remain unchanged and must be
verified before `RawPcapReader` begins.

No threshold search, retraining, architecture change, representation change,
join change, or source-ingestion semantics change is authorized.
