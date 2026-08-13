# Stage20-1E1-V-PRE — Thursday Label Source-Ingestion Erratum

## Status

**THURSDAY LABEL SOURCE-INGESTION ERRATUM FROZEN BEFORE PCAP OR JOIN**

Parent: `0b8a7c9048ea84e7ddce99a5f23b9040204726e0`

This checkpoint records a narrow source-ingestion correction for the pinned
Thursday Morning validation-label parquet. It is frozen before any Thursday
PCAP access, flow reconstruction, exact S4 join, model inference, or threshold
selection.

## Pinned sources

Morning WebAttacks:

- rows physically present: **458968**
- physical columns: **85**
- SHA256: `d8110c04a7af91124ada1c5ad901c4210879df1af8882dc637767532e7165350`

Afternoon Infilteration:

- rows physically present: **288602**
- SHA256: `5da010354f0fc1040fd1fe65967096e1063475de8dd30ae4f657c07201d728a7`

## Structural proof

The Morning parquet contains:

- populated prefix: rows **1..170366**
- fully NULL suffix: rows **170367..458968**
- all-85-column NULL suffix rows: **288602**
- all-NULL rows before suffix: **0**
- non-NULL rows inside suffix: **0**

The all-NULL suffix is one exact contiguous suffix through EOF.

Its row count (**288602**) exactly equals the complete physical row
count of the pinned Afternoon parquet (**288602**).

The Morning populated prefix contains **0** NULL rows across the frozen E0 S4
fields plus Label. The Afternoon parquet also contains **0** such NULL rows.

## Frozen source-ingestion rule

For the pinned Thursday Morning parquet **only**:

> Physical rows 170367 through 458968, proven to be NULL across all 85 physical
> columns and to form one contiguous EOF suffix, are classified as
> `NON_RECORD_STRUCTURAL_NULL_PADDING` and excluded before E0 label-record
> validation and S4 signature construction.

Effective label records:

- Morning: **170366**
- Afternoon: **288602**
- Thursday total: **458968**

## What does not change

The Stage20-1E0 rule for actual records remains:

- NULL or empty Label: **FAIL**
- NULL frozen S4 field: **FAIL**
- fuzzy matching: **NO**
- nearest matching: **NO**
- tolerance matching: **NO**
- imputation: **NO**
- label-guided repair: **NO**

This rule is not generalized to Monday, Tuesday, Wednesday, Friday, or any
other file.

## Scientific boundary

- Thursday PCAP accessed: **NO**
- Thursday join run: **NO**
- Thursday model inference: **NO**
- threshold selection: **NO**
- model training: **NO**
- optimizer steps: **0**
- Friday accessed: **NO**
- Friday status: **CLOSED**

## Next

**Stage20-1E1-V — Thursday validation compact corpus**
