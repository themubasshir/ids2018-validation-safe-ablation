# Stage 20.0 — Authentic Packet-Image ViT Protocol

## Status

**FROZEN**

Stage 20 evaluates Vision Transformer intrusion detection only
after establishing an authentic packet-level image
representation.

No ViT training is authorized at Stage 20.0.

## Dataset

Stage 20 uses **CICIDS2017** from the Canadian Institute for
Cybersecurity, University of New Brunswick.

The dataset is selected because its official release provides
raw PCAP traffic together with labeled flows containing the
metadata required for packet-to-flow association.

Stage 20 is a separate packet-representation experiment and is
not treated as a direct numerical comparison with the
CSE-CIC-IDS2018 models developed in earlier stages.

## Chronological split

### TRAIN

- Monday, 03 July 2017
- Tuesday, 04 July 2017
- Wednesday, 05 July 2017

### VALIDATION

- Thursday, 06 July 2017

### HOLDOUT

- Friday, 07 July 2017

The Friday holdout is closed and may be opened at most once
after the complete representation, model, ensemble and
operating-point protocol has been frozen.

## Task

Binary intrusion detection:

- BENIGN
- ATTACK

## Admissible image geometry

A Stage-20 image must represent authentic packet structure.

The intended candidate geometry is:

- image row = ordered packet position in one bidirectional flow
- image column = byte offset within a packet

The exact packet count, byte count, padding policy, channel
construction and header policy are intentionally NOT frozen at
Stage 20.0. They will be determined during Stage 20.1 using
TRAIN data and source-schema evidence only.

## Prohibited representations

The following are prohibited:

- reshaping CICFlowMeter feature vectors into squares
- arbitrary tabular feature grids
- correlation matrices used as sample images
- label-derived pixels
- day identifiers encoded into the image
- sample ordering based on labels
- holdout-guided image dimensions

## Packet-order rule

Packet ordering within a bidirectional flow is genuine temporal
structure and must be preserved.

Packets from unrelated flows may not be combined into one image.

Future or cross-flow packets may not be introduced.

## Identity-leakage audit

Packet headers may contain dataset-specific identity shortcuts,
including MAC addresses and IP addresses.

Stage 20.1 must audit header fields before the representation is
frozen.

Any masking or canonicalization rule must be fixed before model
training.

## Representation-first rule

Performance cannot justify an invalid representation.

If packet-to-label alignment cannot be reproduced reliably, the
ViT experiment must be rejected rather than rescued through
arbitrary preprocessing.

## Current authorization

Authorized next step:

**Stage 20.1 — packet and labeled-flow schema/source audit**

Not authorized:

- ViT training
- CNN training
- hyperparameter search
- threshold selection
- Friday holdout access
