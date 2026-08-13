# Stage20-1D2-M — Monday Raw-PCAP Deletion Receipt

## Status

**MONDAY RAW PCAP DELETED AFTER REMOTE PROFILE DURABILITY**

Scientific Monday profile commit:

`b07153c7107a9dd0f875a88290ac418e9081d368`

The raw Monday PCAP was not deleted until:

1. the exact Monday histogram artifact was written;
2. the human-readable checkpoint was written;
3. both were committed;
4. the commit was token-pushed;
5. remote `main` SHA matched local HEAD;
6. the worktree was clean.

## Deleted source

`/kaggle/working/stage20_development_sources/pcap/Monday-WorkingHours.pcap`

Frozen bytes:

**10822507416**

Frozen SHA256:

`f6eac599358f216b074338813a1cf7be3cc4e91d116e13efc0dc71f2cca11972`

Exists after deletion:

**False**

## Workspace

Free bytes before deletion:

**9184768000**

Free bytes after deletion:

**9184768000**

Change:

**0 bytes**

These disk values have no scientific role.

## Scientific state

- Monday daily P95 computed: **NO**
- numeric dimensions selected: **NO**
- labels read: **NO**
- Thursday accessed: **NO**
- Friday accessed: **NO**
- model training: **NO**

## Next checkpoint

**Stage20-1D2-T — Tuesday exact geometry profile**

Tuesday may now be acquired because Monday's exact lossless geometry
statistics are remotely durable and its raw PCAP has been removed.

## Receipt artifact

`results/stage20_1d_representation/stage20_1d2m_monday_raw_pcap_deletion_receipt.json`

SHA256:

`22dff3ab0ba7b130f3e004f0af5f987c7173c65041f067e081952d42f5b39f2f`
