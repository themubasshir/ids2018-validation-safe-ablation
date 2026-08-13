# Stage20-1D3 — Combined TRAIN Geometry and Numeric Dimension Freeze

## Status

**COMBINED TRAIN GEOMETRY AND NUMERIC DIMENSIONS FROZEN**

Parent commit:

`6bc24033d781975df7edd924f432dbfb66107183`

## TRAIN population

Representation sizing uses exactly:

1. Monday
2. Tuesday
3. Wednesday

Thursday was not accessed.

Friday remains closed.

## Durable daily inputs

| Day | Exportable flows | Retained packets | Artifact SHA256 |
|---|---:|---:|---|
| Monday | 529601 | 11573331 | `3a26d6499334c12ea4e9272aef4250761c6cf4399e7fb4d33ef236f12d0b7272` |
| Tuesday | 445769 | 11429532 | `5ee3c4fdfbc9d0be8112bdc636f02efae7fb6e476bf0092f6e5909e17e7adaeb` |
| Wednesday | 692389 | 13658697 | `57cda832e0b329a4f5ec108949ed979662ed762b7d82c9049d68eba0ea3506f0` |

## Exact combined TRAIN population

Raw packets:

**37050803**

Valid IPv4 packets:

**36801783**

Exportable flows:

**1667759**

Retained packets:

**36661560**

The three daily exact histograms were summed elementwise before any
quantile was evaluated.

No daily P95 was calculated for representation selection.

No daily P95 values were averaged.

No daily dimensions were averaged.

Combined histogram SHA256:

`4f983148ae4c025d20c127057e9018e6ac8b7b1e9ef9ef392d529f493a690c69`

## Frozen nearest-rank definition

The preregistered rule is:

`rank = ceil(0.95 * N)`

The selected value is the smallest integer whose cumulative frequency
reaches or exceeds that rank.

## Flow packet-count P95

Population:

**1667759 flows**

Nearest-rank position:

**1584372**

Cumulative immediately below selected value:

**1581879**

Frequency at selected value:

**3017**

Cumulative at selected value:

**1584896**

Raw combined TRAIN P95:

**38 packets per flow**

Frozen rounding:

- next power of two: **64**
- minimum: **16**
- maximum: **64**
- cap triggered: **False**

## Final packets per flow

**64**

## Captured IPv4-length P95

Population:

**36661560 retained packets**

Nearest-rank position:

**34828482**

Cumulative immediately below selected value:

**31628802**

Frequency at selected value:

**4174987**

Cumulative at selected value:

**35803789**

Raw combined TRAIN P95:

**2960 captured IPv4 bytes**

Frozen rounding:

- next multiple of 32: **2976**
- minimum: **64**
- maximum: **256**
- cap triggered: **True**

## Final bytes per packet

**256**

## Final packet-image geometry

```text
rows     = 64
columns  = 256
channels = 1
area     = 16384
```

Maximum permitted area:

**16384**

## Exact truncation consequences

These are descriptive consequences of the preregistered rule.

They do not authorize changing the dimensions.

### Packet-row truncation

Maximum observed flow packet count:

**511681**

Flows requiring packet-row truncation:

**35836 / 1667759**

Flow truncation rate:

**0.021487517081**

Packet rows removed:

**21475547**

Fraction of retained packet rows removed:

**0.585778319308**

### Packet-byte truncation

Maximum observed captured IPv4 length:

**24860**

Packets requiring byte truncation:

**15723864 / 36661560**

Packet byte-truncation rate:

**0.428892387558**

Total authentic captured IPv4 bytes:

**33504144134**

Captured IPv4 bytes removed beyond frozen width:

**28195739221**

Captured-byte loss rate:

**0.841559751780**

## Frozen representation

The numeric representation is now immutable:

- rows: **64**
- columns: **256**
- channels: **1**
- area: **16384**

Stage20-1D0 masking rules remain unchanged.

Padding remains:

- packet bytes: right-zero;
- missing flow rows: bottom-zero;
- padding mask: required.

Truncation remains:

- earliest packets first;
- earliest IPv4 bytes first.

Byte storage remains `uint8`.

Model scaling remains `byte / 255`.

## Immutability

After this checkpoint:

- P95 cannot change;
- packet cap cannot change;
- byte cap cannot change;
- rounding cannot change;
- padding cannot change;
- truncation cannot change;
- Thursday cannot alter dimensions;
- Friday cannot alter dimensions;
- model performance cannot alter dimensions.

## Scientific boundary

This checkpoint:

- opened **0** PCAP files;
- read **0** source packet bytes;
- read **no labels**;
- accessed **no Thursday data**;
- accessed **no Friday data**;
- selected **no architecture**;
- trained **no model**.

## Next checkpoint

**Stage20-1D4 — Fixed Packet-Image Encoder Verification**

Architecture selection and model training remain prohibited until encoder
verification succeeds.

## Machine-readable artifact

`results/stage20_1d_representation/stage20_1d3_combined_train_geometry_numeric_dimension_freeze.json`

SHA256:

`2f28cc55fd545bd16e9f823b7f8a455d52b798d1cbae007ac72ef939815bc471`

## Holdout integrity

- Thursday accessed: **NO**
- Friday accessed: **NO**
- Friday status: **CLOSED**
