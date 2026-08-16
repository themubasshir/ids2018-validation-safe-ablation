# Stage22 Source Provenance Recovery Procedure

## Status

**FROZEN BEFORE ROW-LEVEL PROVENANCE MATCHING**

Scientific parent:

`77beddbd7ae82aa53f703fe9441cc473d064ca2b`

Stage22-0 protocol SHA256:

`df9654a1bcff9ff02404e6b2cf6dde5d1ac1bf679d6a5884509427ef1b0fc062`

Stage22-1A runtime discovery SHA256:

`792a05cde245d35579eb6153546de75f795451c5171128859aa41f830bbe69c8`

Stage22-1B procedure lock SHA256:

`2966b0cf2a197fefdd7eda1fda3bac665a3581c182eccab917bc2775b553a061`

## Flagship analysis universe

The Stage22 flagship remains the exact 300,928-row processed corpus.

Flagship SHA256:

`cca1121da5542ef58029acbd4ceafb741734f9c38b815f9ce2625fe2a4479a7d`

The provenance matcher uses all 78 frozen original numeric predictors only.
Neither `Label` nor `binary_label` may be parsed during provenance recovery.

## Candidate source universe

All 10 Stage22-1A feature-compatible non-flagship source files are mandatory
inputs to the provenance scan. No source day may be removed based on labels,
attack coverage, class balance, ambiguity rate, or model performance.

| Capture day | File | Rows | Columns | SHA256 |
|---|---|---:|---:|---|
| 2018-02-14 | `02-14-2018.csv` | 1,048,575 | 80 | `acff8bc61376ee031d80878ee6099e0b1a87a1bd711d8068298421418c9f8147` |
| 2018-02-15 | `02-15-2018.csv` | 1,048,575 | 80 | `fa2947a8256d81ee9103ae16139d62d0e17aa23e696ee80d9e76fb51c01c9c4b` |
| 2018-02-16 | `02-16-2018.csv` | 1,048,575 | 80 | `1a4919faa0c49c7af97230b0c2d076eba23ee6dd81103a3801d51ac316355d8b` |
| 2018-02-20 | `02-20-2018.csv` | 7,948,748 | 84 | `7287a4d7740a1dddbf330ceb2beb6a4889d33ba63674558a68b5eb50d16711df` |
| 2018-02-21 | `02-21-2018.csv` | 1,048,575 | 80 | `a5f4a1c2689e0aa6566c03a58466de9c407c0be0cbd3cc69306544026611be04` |
| 2018-02-22 | `02-22-2018.csv` | 1,048,575 | 80 | `da33c927018274f9d49b145baa00e4ce0526c25b3b890b34c489e247b5e24544` |
| 2018-02-23 | `02-23-2018.csv` | 1,048,575 | 80 | `d0a7f5059d9823b6e9b392b759e306481a3502d190dea7a1b5502ae079ea069b` |
| 2018-02-28 | `02-28-2018.csv` | 613,104 | 80 | `f15e2a12304446058a0186c8ad67de2bd15735a9ba5c70c9a1f4c4242ab06771` |
| 2018-03-01 | `03-01-2018.csv` | 331,125 | 80 | `b0534c5d7d8b41e03df71c6966c995d116a8ed28e61f377c8b14cdf5d28f4edf` |
| 2018-03-02 | `03-02-2018.csv` | 1,048,575 | 80 | `d96f38e7496aba83475031e6fb8c6fdf1abf6aa1b71325a917798f3c7de93de1` |

## Capture-date convention

The candidate files share one source directory.

Unambiguous siblings such as `02-14-2018.csv`, `02-15-2018.csv`,
`02-16-2018.csv`, `02-20-2018.csv`, `02-21-2018.csv`,
`02-22-2018.csv`, `02-23-2018.csv`, and `02-28-2018.csv` force
the directory convention to **MM-DD-YYYY**, because their second numeric
component is greater than 12.

Therefore, without inspecting labels or outcomes:

- `03-01-2018.csv` -> `2018-03-01`
- `03-02-2018.csv` -> `2018-03-02`

## Frozen numeric representation

The exact provenance matcher uses the complete 78-predictor vector.

Numeric values are coerced with:

`pandas.to_numeric(errors='coerce')`

Positive/negative infinity become NaN.

The comparison representation is IEEE-754 float64. Signed numerical zero is
canonicalized to `+0.0` before exact byte comparison.

No decimal rounding, tolerance, nearest-neighbor matching, fuzzy matching, or
imputation is allowed.

## Frozen exact matching rule

A deterministic pandas 64-bit row hash may be used only as a lookup
accelerator.

A candidate is accepted only after exact equality of the complete canonical
78-value float64 vector.

A hash collision can never establish provenance.

For every exact flagship vector, Stage22-1C collects the set of source capture
days containing an exactly equal source row.

- one distinct day -> UNIQUE provenance;
- more than one distinct day -> AMBIGUOUS provenance and later exclusion;
- zero days -> UNMAPPED and Stage22 hard-stop before model fitting.

Multiple source rows on the same capture day do not create day-level
ambiguity.

## Label governance

Whole-file SHA256 is an opaque integrity operation. Label fields are not parsed
or inspected by the provenance matcher.

Stage22-1C may request only the frozen predictor columns.

Development, validation, and final-test roles are not constructed during
Stage22-1B or Stage22-1C.

## Next authorized step

`STAGE22-1C — EXECUTE_FROZEN_EXACT_ROW_TO_CAPTURE_DAY_PROVENANCE_RECOVERY`

No model training, model inference, threshold search, or outcome metric is
authorized.
