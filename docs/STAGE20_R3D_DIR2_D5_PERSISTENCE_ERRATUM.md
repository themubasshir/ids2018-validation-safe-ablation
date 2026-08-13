# Stage20-R3D-DIR2 — D5 Persistence Erratum

## Scope

This erratum corrects a persistence-layer mistake introduced in commit:

`8c531ae8da941e2dc928689215bfbeb225544dce`

The DIR2 directional diagnostic itself remains valid.

## Incorrect persisted statement

The prior generated checkpoint recorded:

**D5 source-faithful accepted: 637/675**

That statement was incorrect.

## Correct frozen distinction

- historical raw C9/C11 exact S4 membership: **637/675**
- D5 source-faithful exact accepted membership: **635/675**
- V1 corrected exact membership: **318/675**

The D5 difference consists exactly of reconstructed flow indices:

`[471, 473]`

These are independently frozen duration/export inconsistencies.

No reconstructed duration is replaced with the published label duration.

## Transition matrix

After applying the frozen D5 classification before V1:

- exact -> exact: **295**
- exact -> absent: **340**
- absent -> exact: **23**
- absent -> absent: **17**

## Directional diagnostic remains unchanged

The currently reconstructed V1 changed-position vector is:

`{9: 354, 10: 202, 11: 153, 12: 135, 13: 44, 14: 62}`

Changed signatures:

**379**

The two historical timeout-constructor orientation inversion flows are:

`[471, 473]`

They do not intersect the 90-flow `(9, 11, 12)` pattern population.

Therefore this erratum changes only the persisted D5 population summary,
not the DIR2 directional finding.

## Holdout integrity

- Friday requests: **0**
- Friday reads: **0**
- Friday openings: **0/1**
- Friday status: **CLOSED**
