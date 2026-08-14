# Stage20-1E4-COLAB-XET-RECOVERY-PRE

**OPERATIONAL INTERRUPTION RECOVERY FROZEN BEFORE RESUME**

Parent Colab-PRE commit: `b70ef87fddafae4803531a617d2e074cac988ad5`

Recovery lock JSON SHA256: `634ec686e421aa9638e07e4d8e47fe0095bb7df3d92c855eb67218dd148f72eb`

## Observed interruption boundary

- Friday source access had started: **YES**
- all three pinned Friday label files reached full expected size: **YES**
- label contents parsed: **NO**
- full Friday PCAP materialized: **NO**
- Friday PCAP SHA256 verified: **NO**
- source SHA verification completed: **NO**
- Stage20 `RawPcapReader` reconstruction pass started: **NO**
- `.Friday.staging`: **empty (0 files / 0 bytes)**
- final Friday compact corpus: **NO**
- model inference: **NO**
- probabilities/metrics: **NO**

## Authorized operational recovery

The scientific protocol is unchanged.

The only transport-level change authorized is:

`HF_HUB_DISABLE_XET=1`

The already-materialized label cache entries may be reused, but their frozen
SHA256 identities must still be verified before label parsing. The Friday PCAP
must reach its exact frozen size and SHA256 before the one authorized
`RawPcapReader` reconstruction pass begins.

The empty interrupted staging directory may be removed only because it is
verified to contain exactly zero files and zero bytes.

Frozen thresholds remain **0.50 / 0.17 / 0.17**. No Friday threshold search,
retraining, architecture change, representation change, join change, or
source-ingestion semantics change is authorized.
