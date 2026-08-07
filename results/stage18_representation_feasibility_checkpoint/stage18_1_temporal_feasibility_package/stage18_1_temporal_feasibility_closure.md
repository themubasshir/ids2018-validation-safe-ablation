# Stage 18.1 — Temporal / MTemporal Representation Feasibility

## Final decision

**SUPPORTED WITH CONSTRAINTS**

Stage 18.1 establishes that an authentic temporal representation is scientifically defensible for the original CSE-CIC-IDS2018 sources, but only through a **timestamp-bin / traffic-snapshot representation**. An arbitrary flow-by-flow temporal ordering is not supported.

No Temporal or MTemporal model was trained in Stage 18.1.

## Authentic temporal metadata

The original dated CSE-CIC-IDS2018 CSV files retain authentic timestamp metadata at one-second resolution.

The audit also established two important restrictions:

- raw CSV row order is not chronological order;
- flows sharing the same second do not have an authenticated within-second order.

Same-second flows therefore cannot be placed into an arbitrary sequential order.

## Raw-to-research provenance recovery

The processed research representation was successfully linked to the original timestamped source without labels, attack categories, predictions, or holdout access.

The original Stage-15 exact-pattern identity was recovered at the hash-set level using:

- original processed predictor count: **78**;
- native processed dtype contract: **37 float64 + 41 int64**;
- hash function: `pd.util.hash_pandas_object`;
- `index=False`.

The frozen train and validation hash universes were reproduced exactly as sets. The historical saved array ordering was not reproduced, but ordering is irrelevant for membership-based raw-source recovery.

## Temporal provenance coverage

Authorized duplicate-safe non-holdout feature patterns:

- train: **154,686**;
- validation: **37,835**;
- total: **192,521**.

Raw-source recovery:

- recovered: **192,521 / 192,521**;
- recovery rate: **100.000%**;
- unmatched: **0**.

Temporal provenance:

- exactly one authentic temporal bin: **164,351**;
- unambiguous rate: **85.367830003%**;
- multiple temporal bins: **28,170**;
- ambiguous rate: **14.632169997%**.

Ambiguous patterns were not force-resolved.

## Existing Stage-15 split is not temporal-safe

The provenance-safe subset contains:

- **131,381** Stage-15 training samples;
- **32,970** Stage-15 validation samples;
- **164,351** samples total.

Across this subset:

- distinct temporal bins: **63,278**;
- train-only bins: **44,508**;
- validation-only bins: **8,929**;
- mixed train+validation bins: **9,841**;
- mixed-bin rate: **15.552008597%**.

Same-bin leakage:

- train samples in mixed bins: **70,210** (53.439995129%);
- validation samples in mixed bins: **23,534** (71.380042463%).

All **9/9** source files containing both train and validation samples are chronologically interleaved.

Validation-bin proximity to training:

- same second: **52.429408631%**;
- within 1 second: **74.720298348%**;
- within 5 seconds: **94.432605221%**;
- within 30 seconds: **99.765583378%**.

Therefore:

> **CURRENT_STAGE15_SPLIT_NOT_SAFE_FOR_TEMPORAL_WINDOWS**

This conclusion does not invalidate the Stage-15 tabular FT-Transformer experiment. It means that its duplicate-safe random split cannot be reused for a temporal-window experiment.

## Temporal/MTemporal feasibility conclusion

A Temporal/MTemporal extension is scientifically supportable **only with the following constraints**:

1. Use only `UNIQUE_TEMPORAL_BIN` patterns.
2. Exclude all temporally ambiguous patterns.
3. Create a separate chronological leakage-safe development split.
4. Construct that development experiment only from the already-authorized non-holdout train+validation universe.
5. Keep both frozen holdouts closed.
6. Never use CSV row order to impose temporal order.
7. Never invent an order among flows sharing the same timestamp.
8. Precommit snapshot aggregation, split design, sequence grouping, and window construction before training.
9. Do not choose sequence/window length post-hoc from validation performance.

## Publication-safe interpretation

The evidence supports the claim that the original dataset contains authentic temporal structure and that a large majority of the duplicate-safe research patterns can be linked unambiguously back to that structure.

It also demonstrates why the existing random train/validation partition cannot simply be reused for temporal modeling: train and validation traffic is heavily interleaved at second-level resolution.

The scientifically appropriate extension is therefore a **separate chronological timestamp-bin/snapshot experiment**, not an artificial reordering of the existing tabular rows.

## Scientific boundary

Stage 18.1 performed:

- no temporal model fitting;
- no temporal model inference;
- no sequence construction;
- no temporal-window construction;
- no holdout reopening;
- no label-based temporal mapping;
- no forced ambiguity resolution.

## Closure

**Stage 18.1 is scientifically closed.**

Final candidate decision:

> **Temporal / MTemporal Transformer — SUPPORTED WITH CONSTRAINTS**

The future model implementation requires a separately precommitted chronological representation protocol and is outside the closed Stage 18.1 feasibility audit.
