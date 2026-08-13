# Stage20-1C16-C — Packet-Geometry Sign / Position Phenotype

## Status

**OBSERVATIONAL ONLY — NO RULE CHANGE**

Parent commit:

`f1e426c54718aaa5970ff63acbb87021c5701118`

## Frozen scientific state

- raw historical exact: **637/675**
- D5 source-faithful exact: **635/675**
- V1 exact: **318/675**
- TCP flows analyzed: **467**
- TCP flows whose S4 signature changes under V1: **379**

## Flow phenotype

- `NONE`: no baseline/V1 packet disagreement
- `GT_ONLY`: capture-oriented baseline exceeds declared V1 only
- `LT_ONLY`: capture-oriented baseline is below declared V1 only
- `MIXED`: both signs occur in the same flow

## Cohort phenotype

- **A exact→exact**: NONE=88, GT_ONLY=0, LT_ONLY=0, MIXED=0
- **B exact→absent**: NONE=0, GT_ONLY=340, LT_ONLY=0, MIXED=0
- **C absent→exact**: NONE=0, GT_ONLY=0, LT_ONLY=23, MIXED=0
- **D absent→absent**: NONE=0, GT_ONLY=5, LT_ONLY=0, MIXED=11

## Exact packet-geometry / S4-change equivalence

Disagreement without signature change:

`[]`

Signature change without packet disagreement:

`[]`

Therefore, within the 467 finished TCP flows:

**packet-geometry disagreement iff the V1 S4 signature changes.**

This is an observational statement only.

## D cohort phenotypes

`{'14': 'MIXED', '25': 'MIXED', '35': 'MIXED', '36': 'MIXED', '52': 'MIXED', '123': 'MIXED', '307': 'GT_ONLY', '309': 'MIXED', '324': 'MIXED', '327': 'MIXED', '333': 'GT_ONLY', '334': 'GT_ONLY', '336': 'MIXED', '337': 'MIXED', '471': 'GT_ONLY', '473': 'GT_ONLY'}`

## Disagreement position

Global:

`{'FIRST': 125, 'INTERIOR': 4642, 'LAST': 326}`

Positive baseline-minus-declared:

`{'FIRST': 125, 'INTERIOR': 4479, 'LAST': 326}`

Negative baseline-minus-declared:

`{'INTERIOR': 163}`

## Disagreement direction

Global:

`{'BWD': 775, 'FWD': 4318}`

Positive baseline-minus-declared:

`{'BWD': 638, 'FWD': 4292}`

Negative baseline-minus-declared:

`{'BWD': 137, 'FWD': 26}`

## Most frequent exact payload deltas

Global:

`[(6, 4597), (5, 301), (-28, 42), (-7, 40), (-6, 36), (-8, 32), (2, 23), (-185, 8), (1, 8), (-122, 4), (-178, 1), (3, 1)]`

B exact -> absent:

`[(6, 4496), (5, 301), (2, 23), (3, 1)]`

C absent -> exact:

`[(-28, 38), (-8, 28), (-7, 20), (-6, 8), (-185, 7), (-178, 1)]`

D absent -> absent:

`[(6, 101), (-6, 28), (-7, 20), (1, 8), (-122, 4), (-28, 4), (-8, 4), (-185, 1)]`

## Interpretation boundary

This checkpoint does not authorize:

- switching packet semantics based on sign
- choosing capture semantics for B-like flows
- choosing declared semantics for C-like flows
- residual-only repair
- hybrid signatures
- tolerance matching
- label-guided correction
- model training
- holdout access

The transition cohorts are used only to describe an already frozen global
V1 experiment.

## Artifact

`results/stage20_1c16_runtime_recovery/stage20_1c16c_packet_geometry_sign_position_phenotype.json`

SHA256:

`cd687b7f588aabcfb241cf79b5240984ff52ed39ddeb3ed36d28fa9ed8e4397a`

## Holdout integrity

- Friday requests: **0**
- Friday reads: **0**
- Friday openings: **0/1**
- Friday status: **CLOSED**
