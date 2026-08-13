# Stage20-1C16-D3 — Mechanism Search Closure

## Status

**MECHANISM SEARCH CLOSED**

The pre-registered Stage20-1C16-D0 stopping rule has fired.

## Candidate budget

Frozen total candidates:

**2**

Consumed:

**2**

Remaining:

**0**

Third candidate allowed:

**NO**

## Candidate 1

`M1_GT_CAPTURE_BEYOND_DECLARED_IPV4`

Decision:

**PASS_COMPLETE_MECHANISM**

Population:

**4930 packets**

Requirement 1:

**True**

Requirement 2:

**True**

## Candidate 2

`M2_LT_CAPTURE_SHORTER_THAN_DECLARED_IPV4`

Decision:

**PASS_COMPLETE_MECHANISM**

Population:

**163 packets**

Requirement 1:

**True**

Requirement 2:

**True**

## Closure outcome

**BOTH_PRE_REGISTERED_MECHANISMS_PASS**

Within the bounded first-50,000-packet Monday development reconstruction, every packet-level baseline/V1 TCP payload disagreement is exactly accounted for by captured IPv4 extent being either beyond or shorter than the declared IPv4 total length.

## Scientific boundary

Mechanism explanation is not reconstruction-rule adoption.

This closure does **not** authorize:

- V1 adoption
- sign-dependent packet semantics
- capture/declared hybrid signatures
- residual-only correction
- label-guided correction
- fuzzy matching
- nearest matching
- further reconstruction-mechanism candidates
- model training

## Next phase

**PACKET-IMAGE REPRESENTATION FREEZE**

Before any model training, freeze:

1. packets per flow
2. bytes per packet
3. channels
4. padding policy
5. truncation policy
6. header policy
7. leakage controls

## Artifact

`results/stage20_1c16_runtime_recovery/stage20_1c16d3_mechanism_search_closure.json`

SHA256:

`3864abccf95a93eb7a9930836c4d8c9ac9430b8a2eb663dd1b0aa32f35cafdaa`

## Holdout integrity

- Friday requests: **0**
- Friday reads: **0**
- Friday openings: **0/1**
- Friday status: **CLOSED**
