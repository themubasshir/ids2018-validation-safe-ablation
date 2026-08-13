# Stage20-1C16-A — Source-Faithful Manifest Recovery

## Status

**SCIENTIFICALLY_RECOVERED_HISTORICAL_BYTES_NOT_RECOVERED**

Parent commit:

`9dd5e663caade7d4fa92e3222387edc82c23cc43`

## Authoritative scientific state

- historical raw exact S4: **637/675**
- D5 source-faithful exact: **635/675**
- V1 exact: **318/675**

Transition matrix:

- A exact -> exact: **295**
- B exact -> absent: **340**
- C absent -> exact: **23**
- D absent -> absent: **17**

## D-cohort source-faithful correction

D membership remains unchanged at **17 flows**:

`[14, 25, 35, 36, 52, 123, 199, 307, 309, 324, 327, 333, 334, 336, 337, 471, 473]`

Historical internal changed-position union:

`[9, 10, 12, 13, 14]`

Current source-faithful changed-position union:

`[9, 10, 11, 12, 14]`

The historical internal union is not forced into the recovered manifest.

The difference is localized to reconstructed flow indices **471** and
**473**, which under the inspected historical timeout-replacement
constructor semantics have changed positions:

`[9, 11]`

Their reconstructed durations remain:

- index 471: **224 µs**
- index 473: **262 µs**

No label duration is substituted.

## D changed-position counts

`{9: 14, 10: 12, 11: 2, 12: 12, 14: 11}`

## D pattern populations

- `[]`: 1 — `[199]`
- `[10,14]`: 2 — `[52,123]`
- `[9,10,12]`: 1 — `[36]`
- `[9,10,12,14]`: 9 — `[14,25,35,309,324,327,333,336,337]`
- `[9,11]`: 2 — `[471,473]`
- `[9,12]`: 2 — `[307,334]`

## Global V1 structural diagnostic

Changed signatures:

**379**

Current zero-based changed-position vector:

`{9: 354, 10: 202, 11: 153, 12: 135, 13: 44, 14: 62}`

## Lost historical manifest

Frozen historical SHA256:

`06082ffa231c105618c3702549edcbb68b91b8164361640d5c27a4fb5e73dcf3`

Recovered deterministic manifest SHA256:

`be965c1b4be3b5e535925bf2fbad4a8f9bdc84000c83e4232fabdfda6a7343fc`

Byte-exact match:

**False**

Because the historical serialization/schema bytes are unavailable, no
format guessing or hash-preimage search is performed.

Canonical historical naming is permitted only if the SHA256 matches exactly.

## Recovered manifest

`results/stage20_1c16_runtime_recovery/stage20_1c16a_transition_cohort_manifest_source_faithful_recovered.json`

## Recovery status

`results/stage20_1c16_runtime_recovery/stage20_1c16a_manifest_recovery_status.json`

SHA256:

`f77ad033c448f6bbbc104ed4c12eade912711a3db3ebbdfa22af57cf522dc4f4`

## Boundary

This checkpoint authorizes no change to:

- TCP payload V1
- D5 classification
- lifecycle rules
- flow matching
- timestamps
- flags
- model architecture
- training
- holdout access

## Holdout integrity

- Friday requests: **0**
- Friday reads: **0**
- Friday openings: **0/1**
- Friday status: **CLOSED**
