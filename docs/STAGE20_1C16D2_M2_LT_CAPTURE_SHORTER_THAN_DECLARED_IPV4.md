# Stage20-1C16-D2 — M2 LT Capture Shorter Than Declared IPv4

## Status

**PASS_COMPLETE_MECHANISM**

Parent commit:

`8a6e6320bc8420124cbf79e2c87b0e58ab8d605e`

Candidate:

`M2_LT_CAPTURE_SHORTER_THAN_DECLARED_IPV4`

## Pre-registered population

Frozen before testing:

**163 LT disagreement packets**

## Independent measurement

The first 50,000 packets of the local Monday development PCAP were re-read.

For each frozen LT packet:

- captured IPv4 extent = captured bytes represented by the IPv4 layer
- declared IPv4 extent = `IP.len`
- raw IPv4 deficit = declared extent - captured extent

That independently measured raw deficit was compared against the frozen
C16-C V1-minus-baseline payload deficit.

No published label value was used.

## Coverage

- expected: **163**
- tested: **163**
- parse failures: **0**
- missing: **0**
- identity failures: **0**

Full frozen population observed:

**True**

## Requirement 1

Captured IPv4 extent must be strictly shorter than declared IPv4 length.

- pass: **163**
- fail: **0**
- all pass: **True**

## Requirement 2

Declared-minus-captured IPv4 deficit must exactly equal the frozen
V1-minus-baseline payload deficit.

- pass: **163**
- fail: **0**
- all pass: **True**

## Exact deficit distribution

Raw IPv4 deficit:

`{6: 36, 7: 40, 8: 32, 28: 42, 122: 4, 178: 1, 185: 8}`

Frozen payload deficit:

`{6: 36, 7: 40, 8: 32, 28: 42, 122: 4, 178: 1, 185: 8}`

Distribution equality:

**True**

## Descriptive position

`{'INTERIOR': 163}`

## Descriptive direction

`{'BWD': 137, 'FWD': 26}`

## Descriptive cohort packet counts

`{'C_absent_to_exact': 102, 'D_absent_to_absent': 61}`

These descriptive strata do not affect acceptance.

## Frozen decision

**PASS_COMPLETE_MECHANISM**

A PASS means only that M2 exactly explains the entire bounded LT
packet population.

It does not authorize V1, a hybrid rule, sign-based selection, or
label-guided reconstruction.

## Mechanism budget

- candidate: **2 of 2**
- consumed: **True**
- third candidate allowed: **False**

## Artifact

`results/stage20_1c16_runtime_recovery/stage20_1c16d2_m2_lt_capture_shorter_than_declared_ipv4.json`

SHA256:

`c09a2ecc61da6848918ad2304b3d3718fe3d1d94e24b434c26c13a0ec87400d3`

## Holdout integrity

- Friday requests: **0**
- Friday reads: **0**
- Friday openings: **0/1**
- Friday status: **CLOSED**
