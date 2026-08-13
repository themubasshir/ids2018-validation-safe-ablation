# Stage20-1D1-S — Storage-Aware Sequential TRAIN Protocol

## Status

**STORAGE-AWARE SEQUENTIAL TRAIN PROTOCOL FROZEN**

Parent commit:

`89c9742a0a62d6d754dcc1a3d4f7810002079fd3`

## Purpose

Kaggle storage cannot hold the complete Monday, Tuesday, and Wednesday
raw-PCAP TRAIN corpus simultaneously.

This checkpoint changes **storage execution only**.

The Stage20-1D0 scientific representation-selection rule is unchanged.

## TRAIN population

TRAIN remains exactly:

1. Monday
2. Tuesday
3. Wednesday

Thursday remains validation and is excluded from representation sizing.

Friday remains closed.

## Sequential workflow

Only one complete TRAIN PCAP is required to be resident at a time.

For each day:

1. acquire or reuse the raw PCAP;
2. verify exact frozen source identity;
3. reconstruct source-faithful exportable flows;
4. compute the exact flow packet-count histogram;
5. compute the exact captured-IPv4-length histogram;
6. persist both histograms and provenance;
7. commit;
8. token-push;
9. verify remote SHA;
10. verify clean worktree;
11. delete that day's raw PCAP;
12. only then advance to the next TRAIN day.

A raw PCAP may not be deleted before the daily scientific profile is
remotely durable.

## Daily profile

Every day must preserve exact integer frequencies for:

- flow packet count;
- captured IPv4 packet length.

No daily P95 is used for dimension selection.

No daily image dimension is selected.

## Combined TRAIN distribution

The exact final flow histogram is the elementwise sum of:

- Monday
- Tuesday
- Wednesday

The exact final packet-length histogram is also the elementwise sum of
those three daily histograms.

The combined histogram is mathematically equivalent, for empirical
quantile calculation, to concatenating the underlying observations from
the three days.

## Final P95

The Stage20-1D0 nearest-rank rule remains unchanged:

rank = ceil(0.95 * N)

The P95 is computed exactly once, after all three daily profiles are
durably available, from the summed TRAIN histogram.

## Forbidden alternatives

The following are prohibited:

- averaging daily P95 values;
- weighting daily P95 values;
- averaging daily dimensions;
- choosing the most convenient day;
- changing the P95 after Monday;
- changing the P95 after Tuesday;
- changing the caps after Wednesday;
- validation-guided sizing;
- holdout-guided sizing.

## Frozen dimension rules

Packets per flow:

- combined TRAIN nearest-rank P95;
- round upward to smallest power of two;
- minimum 16;
- maximum 64.

Bytes per packet:

- combined TRAIN nearest-rank P95;
- round upward to smallest multiple of 32;
- minimum 64;
- maximum 256.

Maximum image area:

**16,384 byte-pixels**

## Planned checkpoints

- Stage20-1D2-M — Monday exact geometry profile
- Stage20-1D2-T — Tuesday exact geometry profile
- Stage20-1D2-W — Wednesday exact geometry profile
- Stage20-1D3 — combine histograms, compute one TRAIN P95, freeze numeric dimensions

## This checkpoint does not

- open a PCAP;
- read packet bytes;
- reconstruct flows;
- profile geometry;
- calculate any P95;
- select numeric dimensions;
- read labels;
- access Thursday;
- access Friday;
- delete Monday;
- download Tuesday;
- train a model.

## Artifact

`results/stage20_1d_representation/stage20_1d1s_storage_aware_sequential_train_protocol.json`

SHA256:

`3a17ae7361a6b072473bdfea70228650951323611f80b9c2f01ba6dd53f234f4`

## Holdout integrity

- Thursday requests: **0**
- Thursday reads: **0**
- Friday requests: **0**
- Friday reads: **0**
- Friday openings: **0/1**
- Friday status: **CLOSED**
