# Stage 20.1C8 — Historical CICFlowMeter Flag Serialization Correction

## Status

**SOURCE-DERIVED CORRECTION FROZEN**

Parent repository commit:

`40a9eaa26fcc53a1ea8e9f7c2b12f2b28d2a58f9`

Historical CICFlowMeter source snapshot:

`eaa853dd82f08ba5288bb7f295b471de7313f883`

This snapshot is treated as the earliest public implementation inspected.
It is **not claimed to be byte-identical to the private/build version used
to generate CICIDS2017 in July 2017**.

---

## Finding

Historical `BasicFlow` stores aggregate TCP flag counters in a
`java.util.HashMap` and serializes the values using iteration over
`flagCounts.keySet()`.

The exporter therefore does not explicitly serialize the counters according
to the fixed CSV header order.

For the historical key set and Java-8-style HashMap bucket ordering, the
serialized semantic order is:

`RST, PSH, ECE, SYN, ACK, FIN, URG, CWR`

whereas the physical CICIDS2017 CSV header positions are:

`FIN, SYN, RST, PSH, ACK, URG, CWE, ECE`

Therefore the frozen physical-column interpretation is:

| Physical CICIDS2017 column | Semantic flag emitted into position |
|---|---|
| FIN Flag Count | RST |
| SYN Flag Count | PSH |
| RST Flag Count | ECE |
| PSH Flag Count | SYN |
| ACK Flag Count | ACK |
| URG Flag Count | FIN |
| CWE Flag Count | URG |
| ECE Flag Count | CWR |

---

## Independent validation

The mapping was derived from source behavior **before adoption** and was
not obtained through permutation search.

On 484 uniquely identifiable Monday flow anchors:

- Literal header-semantic interpretation:
  **254 / 484 = 0.524793388430**
- Source-derived positional interpretation:
  **484 / 484 = 1.000000000000**

No permutation search, best-mapping search, nearest-neighbor matching,
timestamp tolerance, reverse matching, or timeout search was performed.

---

## Protocol consequence

The original CICIDS2017 files remain immutable.

The Stage 20 S4 physical fields remain unchanged.

Future packet reconstruction will:

1. reconstruct the actual semantic TCP flag state;
2. reproduce the historical exporter positional serialization;
3. compare those serialized values against the original physical
   CICIDS2017 columns.

This is a correction of **export semantics**, not a modification of
ground-truth labels or a reduction of the S4 signature.

---

## Boundaries

The following remain unchanged:

- directed flow reconstruction;
- 120-second frozen flow timeout;
- source-derived whole-second timestamp serialization;
- transport-payload packet-length semantics;
- physical S4 field count and positions;
- original CICIDS2017 label files.

The following remain prohibited:

- label-guided flag permutation search;
- feature dropping;
- timeout tuning;
- timestamp tolerance;
- nearest-neighbor label assignment;
- reverse matching;
- holdout-guided reconstruction changes.

---

## Holdout

Friday requests: **0**

Friday reads: **0**

Friday openings: **0 / 1**

Friday remains **CLOSED**.

---

## Next authorized action

Repeat the bounded first-50,000-packet exact S4 pilot using this now-frozen
historical flag-position serialization.

Full Monday processing remains unauthorized until that pilot is interpreted.
