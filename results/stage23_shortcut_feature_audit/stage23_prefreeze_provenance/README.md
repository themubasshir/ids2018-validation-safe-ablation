# Stage23 Pre-Freeze Provenance

This directory records the prospective provenance checks completed before
creation of the Stage23-0 shortcut-feature-audit protocol lock.

Verified before any Stage23 experiment:

- Stage22R scientific seal verified.
- Stage22R publication closeout verified.
- Eight authorized development cache files match the frozen Stage22R-1C
  byte sizes, SHA-256 hashes, row counts, and schemas exactly.
- The frozen 70-feature model input is present in all eight cache files.
- `RANDOM_NATURAL` was reconstructed exactly from the frozen
  `random_validation.packbits` membership.
- `CHRONOLOGICAL_NATURAL` was reconstructed exactly using development
  days 0-6 for training and day 7 (Feb28) for validation.
- Random and chronological partitions have zero train/validation overlap
  and zero unassigned development rows.
- No predictor feature was read during membership verification.
- No Stage23 model was fit.
- No Stage23 metric was calculated.
- Raw Mar1 and Mar2 were not opened.

## Important unresolved prospective design point

The frozen Stage22R 70-feature input contains `Dst Port` and `Protocol`,
but does not contain `Src Port`.

Therefore the exact operational definition of the requested Stage23
`NO_PORTS` subset must be resolved and frozen prospectively in Stage23-0.
It has not been defined by this checkpoint.

## Status

This is a provenance checkpoint only.

`Stage23-0` is **not yet frozen**.
