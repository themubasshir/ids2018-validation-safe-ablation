# Stage20-1D2-W — Wednesday Raw Cache Release Receipt

## Status

**WEDNESDAY RAW CACHE RELEASED AFTER REMOTE PROFILE DURABILITY**

Scientific Wednesday profile commit:

`ff03dbce080c5e51bd9e859f7098080727c1ef09`

Scientific profile SHA256:

`57cda832e0b329a4f5ec108949ed979662ed762b7d82c9049d68eba0ea3506f0`

## Safe ordering

Wednesday raw storage was retained until the exact Wednesday profile was:

1. written;
2. committed;
3. pushed;
4. remote-SHA verified;
5. followed by a clean-worktree check.

Only then was the Wednesday raw cache released.

## Wednesday source

- object: `pcap/Wednesday-workingHours.pcap`
- revision: `e810c1cc98270ec271a1df917b9de0786c33f343`
- bytes: **13420789612**
- SHA256: `cd2674db7559a53f24bc03be3239b315700174ccaef72d10f5edc4c1a08f6186`

## Storage release

Free before:

**6585872384**

Free after:

**20006690816**

Space reclaimed:

**13420818432 bytes**

Remaining Wednesday-size raw objects:

**0**

## Complete TRAIN daily-profile state

Monday:

**DURABLE**

Tuesday:

**DURABLE**

Wednesday:

**DURABLE**

All three exact daily profiles are now available.

Combined TRAIN histogram built:

**NO**

Combined TRAIN P95 computed:

**NO**

Numeric dimensions frozen:

**NO**

## Next checkpoint

**Stage20-1D3**

Stage20-1D3 may now:

1. load the three durable daily profiles;
2. sum exact flow-packet-count histograms;
3. sum exact captured-IPv4-length histograms;
4. verify aggregate losslessness;
5. calculate the single frozen nearest-rank TRAIN P95 for each distribution;
6. mechanically apply the Stage20-1D0 rounding/cap rules;
7. freeze final numeric packet-image dimensions.

Thursday remains untouched.

Friday remains closed.

## Artifact

`results/stage20_1d_representation/stage20_1d2w_wednesday_raw_cache_release_receipt.json`

SHA256:

`24086a98fc15e880fa8ad058de40ed937c77908621cc106001d9289ec950516c`
