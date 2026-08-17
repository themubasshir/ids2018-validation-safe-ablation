# Stage23 — Complete Placebo Boosted Block

This seal freezes the complete Stage23 matched-size placebo boosted-model
block.

## Fit accounting

- Primary boosted fits: 24 / 24
- Placebo boosted fits: 20 / 20
- Stage23 total after this seal: 44 / 50
- Remaining model fits: 6 depth-1 stump controls

The sealed placebo block contains:

1. PLACEBO_COUNTS
2. PLACEBO_VOLUME_DIRECTION
3. PLACEBO_IAT
4. PLACEBO_PACKET_SIZE
5. PLACEBO_ACTIVITY

Each placebo was evaluated under:

- RANDOM_NATURAL
- CHRONOLOGICAL_NATURAL

using the prospectively frozen Stage23 model specification.

No raw March 1 or March 2 data were accessed.
No threshold optimization, subset-specific tuning, rebalancing, or
placebo-definition changes were performed.

The next authorized model work is the six prospectively frozen
depth-1 stump controls.
