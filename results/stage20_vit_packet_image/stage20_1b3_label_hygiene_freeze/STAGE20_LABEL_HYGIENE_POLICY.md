# Stage 20.1B3 — Development Label Hygiene Freeze

## Status

**FROZEN**

The Stage-20 CICIDS2017 development label sources contain
2,416,100 source records.

Exactly 288,602 records are structurally empty across
all 85 source fields. These occur in the Thursday-morning
Web-Attacks source.

Only these fully structural-empty records are removed.

No partially populated row is removed.

## Frozen sanitation rule

A source row may be removed only when every one of its 85
fields is NULL, NaN, or an empty/whitespace-only string.

A partially populated record with missing Label causes the
pipeline to abort.

A partially populated record with missing packet-alignment
metadata causes the pipeline to abort.

## Canonical retained development metadata

Valid flows: 2,127,498

BENIGN: 1,858,775

ATTACK: 268,723

The original multiclass label text remains preserved.

The Stage-20 binary mapping remains:

- BENIGN = negative
- every non-BENIGN label = positive

## Thursday morning

Source rows: 458,968

Structurally empty rows: 288,602

Valid retained flows: 170,366

BENIGN: 168,186

ATTACK: 2,180

## Canonical schema

The packet-alignment metadata is frozen to eight fields with
explicit types:

- Flow ID — UTF-8
- Source IP — UTF-8
- Source Port — int64
- Destination IP — UTF-8
- Destination Port — int64
- Protocol — int64
- Timestamp — UTC timestamp at nanosecond representation
- Label — UTF-8

Explicit Arrow types are used to prevent batch-dependent schema
inference.

## Current state

No raw PCAP has been downloaded.

No packet-to-flow matching has been executed.

No packet count, byte width, image dimensions, padding,
truncation, channel construction, or header masking rule is
frozen.

Friday remains closed at 0 / 1.

The next authorized step is the Monday-only packet-to-flow
alignment pilot.
