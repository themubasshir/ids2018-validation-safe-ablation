# Stage20-1C16-B — Transition-Cohort TCP Packet Geometry

## Status

**OBSERVATIONAL PACKET GEOMETRY — NO RULE CHANGE**

Parent commit:

`ea8e5bf3b74eda2c0e7043817acb98eb50ba1bce`

## Frozen scientific state

- historical raw exact: **637/675**
- D5 source-faithful exact: **635/675**
- V1 exact: **318/675**

Transition cohorts:

- A exact -> exact: **295 total / 88 TCP**
- B exact -> absent: **340 TCP**
- C absent -> exact: **23 TCP**
- D absent -> absent: **17 total / 16 TCP**
- total analyzed TCP flows: **467**

## Geometry definitions

For each retained TCP packet:

- baseline = capture-oriented Scapy TCP payload length
- V1 = frozen declared IPv4/TCP geometry payload length

Classification:

- `declared_equals_capture`: baseline == V1
- `capture_gt_declared`: baseline > V1
- `capture_lt_declared`: baseline < V1

These classes are descriptive only. They do not authorize a new
reconstruction rule.

## Source-faithful packet direction

Historical BasicFlow semantics are preserved:

1. `firstPacket()` always records the first packet as forward.
2. For subsequent packets, direction follows stored source-IP equality.
3. This explicitly handles timeout-replacement cases **471** and **473**,
   whose first packets are recorded before prior endpoint orientation is
   restored.

## Cohort geometry

| Cohort | TCP flows | Packets | Equal | Capture>Declared | Capture<Declared | Disagreement packets | Disagreement rate | Affected flows | Affected-flow rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| A exact→exact | 88 | 7002 | 7002 | 0 | 0 | 0 | 0.0 | 0 | 0.0 |
| B exact→absent | 340 | 13198 | 8377 | 4821 | 0 | 4821 | 0.365282618579 | 340 | 1.0 |
| C absent→exact | 23 | 969 | 867 | 0 | 102 | 102 | 0.105263157895 | 23 | 1.0 |
| D absent→absent | 16 | 360 | 190 | 109 | 61 | 170 | 0.472222222222 | 16 | 1.0 |

## Global 467-flow geometry

- TCP flows: **467**
- packets: **21529**
- declared equals capture: **16436**
- capture > declared: **4930**
- capture < declared: **163**
- disagreement packets: **5093**
- disagreement packet rate: **0.23656463375**
- affected flows: **379**
- affected-flow rate: **0.811563169165**

## Special subsets

- **A_stable_exact_tcp_88**: 88 flows, 7002 packets, 0 disagreement packets (rate=0.0), 0 affected flows.
- **B_regressions_exact_to_absent_340**: 340 flows, 13198 packets, 4821 disagreement packets (rate=0.365282618579), 340 affected flows.
- **C_resolved_absent_to_exact_23**: 23 flows, 969 packets, 102 disagreement packets (rate=0.105263157895), 23 affected flows.
- **D_absent_to_absent_tcp_16**: 16 flows, 360 packets, 170 disagreement packets (rate=0.472222222222), 16 affected flows.
- **original_tcp_length_residuals_37**: 37 flows, 1325 packets, 270 disagreement packets (rate=0.203773584906), 37 affected flows.
- **resolved_23**: 23 flows, 969 packets, 102 disagreement packets (rate=0.105263157895), 23 affected flows.
- **remaining_14**: 14 flows, 356 packets, 168 disagreement packets (rate=0.47191011236), 14 affected flows.
- **duration_export_471_473**: 2 flows, 4 packets, 2 disagreement packets (rate=0.5), 2 affected flows.

## Geometry versus S4 signature change

Global:

`{'disagreement_and_signature_changed': 379, 'disagreement_without_signature_change': 0, 'signature_change_without_disagreement': 0}`

This records whether packet-level baseline/V1 disagreement and
flow-level S4 signature change coincide. It does not use label agreement
to choose packet semantics.

## Directional geometry

Forward:

`{'declared_equals_capture': 5804, 'capture_gt_declared': 4292, 'capture_lt_declared': 26}`

Backward:

`{'declared_equals_capture': 10632, 'capture_gt_declared': 638, 'capture_lt_declared': 137}`

## Duration/export cases

Flows **471** and **473** remain in cohort D.

Their source-faithful durations remain:

- 471: **224 µs**
- 473: **262 µs**

Both retain changed S4 positions:

`[9, 11]`

No published-label duration is substituted.

## Packet uniqueness

Packet references:

**21529**

Unique packet indices:

**21529**

Duplicate packet indices:

`[]`

## Artifact

`results/stage20_1c16_runtime_recovery/stage20_1c16b_transition_cohort_packet_geometry.json`

SHA256:

`b70e1bbdd296c96437ee9a31e01150571d6b019430c2cab06528d26d1f345451`

## Scientific boundary

This checkpoint does not authorize:

- selective payload semantics
- residual-only repair
- label-guided correction
- tolerance matching
- fuzzy matching
- nearest-neighbor matching
- lifecycle modification
- model training
- Friday access

## Holdout integrity

- Friday requests: **0**
- Friday reads: **0**
- Friday openings: **0/1**
- Friday status: **CLOSED**
