# Stage21-1R1-M — Monday First-50k Forensic Restoration Gate

**STATUS: PASS — RAW 637 / D5 SOURCE-FAITHFUL 635**

Parent commit:

`ca8152c90068712f704dea7065767e6637452cc8`

Exact Kaggle forensic receipt SHA256:

`21f8edc521830979a7859a3c8ace8a5bcc3413671ca86d6023878be4f43a3f97`

## Source identity

Monday PCAP:

- bytes: `10822507416`
- SHA256: `f6eac599358f216b074338813a1cf7be3cc4e91d116e13efc0dc71f2cca11972`
- revision: `e810c1cc98270ec271a1df917b9de0786c33f343`

Monday labels:

- rows: `529918`
- bytes: `65465382`
- SHA256: `dfdcef4b8670e52af54dc4f82174834365a393473e877174cca46d17b12dfd02`
- revision: `b7e532345512edcd530cb1770dc76636aeb52802`

Both sources passed exact byte-size and SHA256 verification before packet parsing.

## Corrected frozen parser gate

An initial Stage21 restoration implementation incorrectly classified
some IPv4 packets from the IPv4 protocol number and force-decoded
non-direct payloads as UDP.

That implementation stopped at the geometry gate before S4 membership.

Observed incorrect attempt:

- TCP: `31618`
- UDP: `14366`
- protocol-0: `52`
- non-IPv4: `3964`

The implementation was corrected to the already-frozen Stage20 rule:

- outer IPv4 only;
- direct `ip.payload` TCP -> protocol 6;
- direct `ip.payload` UDP -> protocol 17;
- otherwise protocol/ports/payload -> 0.

This was an implementation correction only.
No scientific protocol, timeout, join rule, representation,
label, or exclusion was changed.

Corrected exact parser anchors:

- TCP: `31618`
- UDP: `14334`
- protocol-0: `84`
- non-IPv4: `3964`

## Frozen lifecycle anchors

First exactly 50,000 packets:

- completed exportable flows: `675`
- FIN: `432`
- FLOW_TIMEOUT: `243`
- protocol 6: `467`
- protocol 17: `207`
- protocol 0: `1`

All reproduced exactly.

## Raw S4 gate

- exact set membership: `637 / 675`
- exact multiset membership: `637 / 675`

Raw absent indices:

`[14, 25, 35, 36, 40, 43, 45, 50, 52, 54, 57, 59, 63, 66, 68, 71, 119, 123, 124, 147, 148, 197, 198, 199, 277, 279, 281, 307, 309, 324, 327, 333, 334, 336, 337, 445, 448, 454]`

Decision:

**RAW 637 GATE PASS**

## D5 source-faithful gate

Pre-frozen exclusions:

- index `471`: raw exact, `224 us`, protocol 6, FIN
- index `473`: raw exact, `262 us`, protocol 6, FIN

No new exclusion was inferred.

Final D5 accepted:

`635 / 675`

Decision:

**D5 635 GATE PASS**

## Scientific boundary

At this checkpoint:

- full Monday reconstruction: **NOT STARTED**
- compact corpus: **NOT MATERIALIZED**
- Stage21 model forward: **NO**
- training: **NO**
- optimizer steps: **0**
- join rule changed: **NO**
- representation changed: **NO**
- new forensic exclusions inferred: **NO**

## Next authorized action

**Full Monday source-faithful reconstitution only.**

The target remains the sealed Stage20 Monday compact corpus of
`528509` supervised flows.

Stage21 model forward/training remains prohibited until the required
Monday, Tuesday, Wednesday, and Thursday corpora are restored exactly.
