# Stage22R-0I — Kaggle-Faithful Protocol Amendment

## Status

**LOCKED BEFORE STAGE22R DATA-ROW ACCESS**

Parent commit:

`5f8062935f67ca509a97101d126c0b6f3db39268`

Historical Kaggle source:

`solarmainframe/ids-intrusion-csv`

## Why this amendment exists

The intended Stage22 design requested exact S4 duplicate control and
5-tuple + attacker-source-IP group-disjoint control.

The preserved original Kaggle CSE-CIC-IDS2018 representation does not
uniformly contain the endpoint fields required to execute those rules.
Only the Feb-20 source preserves the four additional endpoint columns.

Stage22R therefore does **not** claim S4 equivalence or endpoint-group
disjointness.

Raw PCAP reconstruction and substitution with an improved/re-generated
IDS2018 corpus are both outside Stage22R.

## Executable four-cell design

1. RANDOM × NATURAL
2. RANDOM × REBALANCED
3. CHRONOLOGICAL × NATURAL
4. CHRONOLOGICAL × REBALANCED

All four cells share the same final holdout:

- `03-01-2018.csv`
- `03-02-2018.csv`

The holdout remains closed until one final reporting opening.

## Development split definitions

### Chronological

Train:

- 02-14
- 02-15
- 02-16
- 02-20
- 02-21
- 02-22
- 02-23

Validation:

- 02-28

### Random comparator

The development universe consists only of Feb-14 through Feb-28.

After K79 cleaning, it is split:

- 80% train
- 20% validation
- stratified by binary label
- random state 42

Mar-1 and Mar-2 never participate in this random split.

## K79 exact available-row control

K79 consists of:

- corrected timestamp at one-second resolution
- all 78 common Stage19 numeric predictors
- **no label**

It is explicitly a new Stage22R leakage-control rule.

It is **not** S4 and is **not** endpoint identity.

Exact conflicting-label signatures are excluded.
Exact same-label duplicates retain the earliest source-day / row-index
representative.

## Rebalancing

Rebalancing is training-only deterministic benign undersampling.

Historical final flagship counts are used only to define the target ratio:

`180000 : 120928 = 5625 : 3779`

All attack training rows are retained.

Target benign count:

`floor(n_attack * 5625 / 3779)`

Sampling is without replacement with seed 42.

Validation and final holdout are never resampled.

This does **not** claim recovery of the historical balancing operator.

## Models

Frozen Stage16 strategy:

`ENS_LGBM_XGB_EQUAL`

`0.5 * P_LIGHTGBM + 0.5 * P_XGBOOST`

Frozen Stage15 70-feature configuration is used.

No Stage22R feature or hyperparameter search is permitted.

## Thresholds

Grid:

`0.05, 0.06, ..., 0.95`

91 thresholds.

Standard:

`0.50`

Balanced:

maximize F1

`F1 = 2TP/(2TP+FP+FN)`

tie breaks:

1. lower FPR
2. higher recall
3. closer to 0.50
4. lower threshold

Security:

require `FPR <= 0.05`

maximize F2

`F2 = 5TP/(5TP+FP+4FN)`

tie breaks:

1. lower FPR
2. higher recall
3. lower threshold

No constraint relaxation.

## Final-test governance

Maximum authorized Mar1-Mar2 openings:

**1**

Openings consumed before this lock:

**0**

The one opening may occur only after all four development models and
all validation-selected operating points are frozen and Git-anchored.

After that opening, no scientific choice may change.
