# Stage20-1C16-D1 — M1 GT Capture Beyond Declared IPv4

## Status

**PASS_COMPLETE_MECHANISM**

Parent commit:

`238f8583043bcd227869cdddb1c4c4336f869bd3`

Candidate:

`M1_GT_CAPTURE_BEYOND_DECLARED_IPV4`

## Pre-registered population

Frozen before testing:

**4930 GT disagreement packets**

## Independent measurement

The first 50,000 packets of the local Monday development PCAP were
re-read.

For each frozen GT packet:

- captured IPv4 extent = exact captured bytes represented by the IPv4 layer
- declared IPv4 extent = `IP.len`
- raw IPv4 excess = captured extent - declared extent

This raw excess was then compared with the independently frozen C16-C
baseline-minus-V1 payload difference.

No published label value was used.

## Coverage

- expected: **4930**
- tested: **4930**
- parse failures: **0**
- missing: **0**
- runtime identity failures: **0**

Full frozen population observed:

**True**

## Requirement 1

Captured IPv4 extent must be strictly greater than declared IPv4 length.

- pass: **4930**
- fail: **0**
- all pass: **True**

## Requirement 2

Raw captured IPv4 excess must exactly equal the frozen positive payload
difference.

- pass: **4930**
- fail: **0**
- all pass: **True**

## Exact excess distribution

Raw IPv4 excess:

`{1: 8, 2: 23, 3: 1, 5: 301, 6: 4597}`

Frozen payload delta:

`{1: 8, 2: 23, 3: 1, 5: 301, 6: 4597}`

Distribution equality:

**True**

## Descriptive position

`{'FIRST': 125, 'INTERIOR': 4479, 'LAST': 326}`

## Descriptive direction

`{'BWD': 638, 'FWD': 4292}`

## Descriptive cohort packet counts

`{'B_exact_to_absent': 4821, 'D_absent_to_absent': 109}`

These strata do not affect acceptance.

## Frozen decision

**PASS_COMPLETE_MECHANISM**

A PASS means only that the pre-registered M1 mechanism exactly explains
the entire bounded GT packet population.

It does **not** authorize adoption of V1, selective declared-length
semantics, or a hybrid reconstruction rule.

## Mechanism budget

Candidate number:

**1 of 2**

Candidate consumed:

**True**

Remaining after successful evaluation:

**1**

If consumed, the only remaining candidate is:

`M2_LT_CAPTURE_SHORTER_THAN_DECLARED_IPV4`

## Artifact

`results/stage20_1c16_runtime_recovery/stage20_1c16d1_m1_gt_capture_beyond_declared_ipv4.json`

SHA256:

`522b7c2b1e326bdbc7c689b6091bc7ac73a89793b4b97e13a88523ac5d5de455`

## Holdout integrity

- Friday requests: **0**
- Friday reads: **0**
- Friday openings: **0/1**
- Friday status: **CLOSED**
