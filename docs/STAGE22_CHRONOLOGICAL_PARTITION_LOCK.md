# Stage22 Chronological Capture-Day Partition Lock

## Status

**FROZEN BEFORE DUPLICATE EXCLUSION AND BEFORE MODEL EXECUTION**

Scientific parent:

`f53c2872024456d8d93b94c149a34cfe81f3f333`

Stage22-0 protocol SHA256:

`df9654a1bcff9ff02404e6b2cf6dde5d1ac1bf679d6a5884509427ef1b0fc062`

Stage22-1D provenance evidence seal SHA256:

`6d2f40d1915e131ceffca723848f5270a9ee8887acb13fe035a0d8c86d27b8b8`

Stage22-1E duplicate evidence seal SHA256:

`1db4e574b1b6c858152b9977c0dcb206dac46cd8110ef465ff332803a9b3bc00`

## Usable capture-day operationalization

A source capture day is Stage22-usable if and only if at least one flagship
row remains **uniquely attributable** to that day after the already-frozen
provenance admissibility rules.

This definition is applied before duplicate sanitization.

It does not use labels, class balance, attack-family composition, model
predictions, validation performance, or final-test performance.

## Source-day evidence

| Source day | Unique attributable rows | Stage22 usable |
|---|---:|---|
| 2018-02-14 | 18,813 | YES |
| 2018-02-15 | 35,664 | YES |
| 2018-02-16 | 29,783 | YES |
| 2018-02-20 | 0 | NO |
| 2018-02-21 | 39,962 | YES |
| 2018-02-22 | 15,721 | YES |
| 2018-02-23 | 16,878 | YES |
| 2018-02-28 | 15,245 | YES |
| 2018-03-01 | 30,737 | YES |
| 2018-03-02 | 38,130 | YES |

`2018-02-20` remains preserved in the source/provenance evidence, but it has
zero uniquely attributable flagship rows after the frozen ambiguous-provenance
exclusion and therefore cannot instantiate a non-empty Stage22 row group.

## Frozen chronological roles

### Development

- `2018-02-14`
- `2018-02-15`
- `2018-02-16`
- `2018-02-21`
- `2018-02-22`
- `2018-02-23`

### Validation

- `2018-02-28`

### Final test

- `2018-03-01`
- `2018-03-02`

The final test is the pooled latest-two-day set and will also be reported
separately for each final capture day.

## Pre-duplicate row counts

- Development: **156,821**
- Validation: **15,245**
- Final test: **68,867**
- Ambiguous provenance excluded: **59,995**

## Critical immutability rule

The usable-day list and chronological role assignment are now frozen.

Later duplicate sanitization may not:

- replace a day;
- reassign a day;
- change development/validation/final roles;
- repair an empty day;
- modify the chronology because of class balance or performance.

If duplicate sanitization later creates a limitation, it must be reported.

## Duplicate boundary

No duplicate row was excluded in Stage22-1F.

The next step applies the previously frozen rule using the exact Stage22-1E
70-feature groups:

**retain occurrences in the earliest chronological role and exclude
occurrences from every later role.**

Within-role duplicates remain.

## Outcome governance

Stage22-1F did not read `Label` or `binary_label`, run any model, select any
threshold, or compute any validation/final metric.

The final-test role is now identified, but its class labels remain sealed.
