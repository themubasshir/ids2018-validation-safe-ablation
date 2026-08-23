# Zenodo Archive Rights and Safety Review

Status: **BASELINE INVENTORY COMPLETE; ARCHIVE CREATION NOT AUTHORIZED**

Inventory baseline: `9aa0d4a2a1dce51b2a54a88660271d97aa14c7a7`

Branch: `manuscript-reproducibility-cleanup`

Review date: 2026-08-23

This review is a conservative release-engineering inventory, not legal advice. It does not create a release tag, authorize a Zenodo deposit, or infer that existing GitHub availability establishes redistribution rights.

## Decision summary

The baseline contains 4,519 tracked files totaling 2,384,836,961 bytes (2.221 GiB). The proposed archive file list contains only `INCLUDE` and `INCLUDE_WITH_NOTICE` entries:

- proposed files: **3,617**;
- proposed archive size: **81,426,796 bytes** (77.65 MiB);
- files held out for manual review or exclusion: **902**;
- manual-rights-review files: **890**, totaling 2,245,983,952 bytes (2.092 GiB);
- clearly excluded files: **12**, totaling 57,426,213 bytes (54.77 MiB);
- unresolved `UNKNOWN` redistribution statuses: **0**.

No archive should be created until the manual-review disposition is approved and the inventory is regenerated against the eventual tag candidate. The four inventory/review outputs and their static test/readiness-count bookkeeping are administrative changes created after the frozen baseline and are intentionally not included in the baseline inventory; a final release-candidate inventory must add them without attempting a recursive self-hash.

## Authoritative rights context

The scoped repository MIT license covers repository-authored code and original documentation only. It does not grant rights to external datasets, third-party dependencies, fitted weights, record-level derivatives, or other artifacts whose rights are not owned by the author.

The official CSE-CIC-IDS2018 page states that redistribution is permitted when the dataset is cited and linked: <https://www.unb.ca/cic/datasets/ids-2018.html>. The official CICIDS2017 page identifies the PCAP, labeled-flow, and CSV distributions and requests citation of the associated paper: <https://www.unb.ca/cic/datasets/ids-2017.html>. The CIC dataset FAQ likewise describes redistribution subject to dataset/paper citation: <https://www.unb.ca/cic/datasets/>.

Those terms support an attribution notice for clearly aggregate outputs, but this review does not extend them into an automatic legal conclusion for every transformed record cache, packet-byte representation, fitted model, embedded notebook output, or third-party component. Git tracking and prior public availability are not rights evidence.

## Inventory scope and method

Every file tracked at the baseline was enumerated with `git ls-files`, including all required roots and the additional release-relevant roots:

| Tracked surface | Files |
| --- | ---: |
| `results/` | 3,885 |
| `models/` | 5 |
| `metadata/` | 39 |
| `figures/` | 104 |
| `manuscript/` | 6 |
| `src/` | 125 |
| `scripts/` | 56 |
| `configs/` | 34 |
| `docs/` | 184 |
| `environment/` | 13 |
| `notebooks/` | 10 |
| `tables/` | 34 |
| `tests/` | 15 |
| Root files | 9 |
| **Total** | **4,519** |

For each file, `ZENODO_RIGHTS_INVENTORY.csv` records path, extension, byte size, SHA-256, tracked status, stage, role, provenance class, static shape/row count where safely available, dimension basis, record-bound status, redistribution status, rights basis, and notes.

Static dimensional inspection was limited to metadata-safe operations:

- CSVs were streamed for row and maximum-column counts;
- JSONL files were line-counted;
- small non-model JSON files were parsed only for top-level type/key/array counts;
- NPY/NPZ files were read only through format/member headers for declared shapes and dtypes; numeric payloads were not loaded;
- PNG dimensions came from the IHDR header;
- notebooks were parsed only for top-level cell count;
- Parquet, model, checkpoint, and preprocessing payloads were not deserialized.

No statistic, model output, metric, record value, target, holdout, or scientific conclusion was computed.

## Provenance classification totals

| Provenance classification | Files | Bytes | Default disposition |
| --- | ---: | ---: | --- |
| `REPOSITORY_AUTHORED_CODE` | 213 | 10,854,108 | `INCLUDE` |
| `REPOSITORY_AUTHORED_DOCUMENTATION` | 347 | 67,666,234 | `INCLUDE`, except 13 executed notebooks |
| `AGGREGATE_DERIVED_RESULT` | 3,070 | 68,356,115 | `INCLUDE_WITH_NOTICE` |
| `MODEL_WEIGHT` | 269 | 887,461,657 | `MANUAL_RIGHTS_REVIEW` |
| `PER_RECORD_DERIVED_ARTIFACT` | 608 | 1,293,072,634 | `MANUAL_RIGHTS_REVIEW` |
| `RAW_OR_NEAR_RAW_DATA` | 9 | 57,407,905 | `EXCLUDE` |
| `THIRD_PARTY_ASSET` | 0 | 0 | none identified as a tracked standalone asset |
| `UNKNOWN` | 3 | 18,308 | `EXCLUDE` compiled caches |
| **Total** | **4,519** | **2,384,836,961** | |

## Record-bound totals

| `RECORD_BOUND` | Files | Bytes | Meaning |
| --- | ---: | ---: | --- |
| `YES` | 382 | 899,898,087 | dimensions/name/role tie content to flows, packets, records, cases, or source rows |
| `NO` | 3,886 | 968,888,453 | code, documentation, aggregate output, or fitted parameters rather than one row per source record |
| `UNKNOWN` | 251 | 516,050,421 | binary/notebook structure does not safely establish record binding |

`RECORD_BOUND=NO` does not itself grant redistribution rights. In particular, fitted model parameters remain under manual review.

## Clearly includable

`INCLUDE` contains 547 files totaling 13,070,681 bytes (12.47 MiB): repository-authored code, tests, safe wrappers, configs, manuscript content, release metadata, and original documentation covered by the scoped MIT license.

The machine-exact paths are the `INCLUDE` rows in `ZENODO_RIGHTS_INVENTORY.csv` and appear in `PROPOSED_ZENODO_FILELIST.txt`.

## Includable with notice

`INCLUDE_WITH_NOTICE` contains 3,070 aggregate-derived files totaling 68,356,115 bytes (65.19 MiB). These include aggregate metrics, summaries, manifests, receipts, figures, tables, checksum records, and stage-level publication artifacts.

A future archive must retain:

1. the scoped license boundary;
2. CSE-CIC-IDS2018 and CICIDS2017 attribution and official links;
3. the statement that aggregate inclusion does not license underlying datasets;
4. scientific-stage provenance and claim ceilings; and
5. the Stage 28 final empirical boundary.

All exact paths are in `PROPOSED_ZENODO_FILELIST.txt`.

## Needs supervisor or manual rights decision

All **890** `MANUAL_RIGHTS_REVIEW` items are listed individually in `ZENODO_EXCLUSION_LIST.txt` and in the inventory CSV. None appears in the proposed archive file list.

| Manual-review role | Files | Bytes | Decision required |
| --- | ---: | ---: | --- |
| `FITTED_MODEL_WEIGHT` | 265 | 887,452,093 | confirm author ownership, upstream dataset implications, model-format notices, and whether weights may be deposited |
| `PREPROCESSOR_CHECKPOINT` | 4 | 9,564 | confirm fitted preprocessing artifacts may be redistributed with the same rights basis as weights |
| `RECORD_LEVEL_ARRAY_OR_TABLE` | 462 | 1,179,623,153 | determine whether arrays/tables reproduce or encode flow-, target-, holdout-, label-, membership-, or prediction-level information |
| `RECORD_LEVEL_TABLE_OR_METADATA` | 111 | 68,642,317 | review CSV/JSON/JSONL record granularity, identifiers, hashes, labels, cases, and source linkage |
| `PACKET_OR_BYTE_DERIVED_CACHE` | 28 | 43,903,714 | review packet-byte, packet-length, label, offset, membership, or image-source derivation |
| `RECORD_LEVEL_VISUAL` | 7 | 903,450 | review case-specific integrated-gradient/disagreement figures for record-derived disclosure and dataset obligations |
| `EXECUTED_NOTEBOOK` | 13 | 65,449,661 | review embedded outputs, record excerpts, historical credentials/paths, and third-party display content |
| **Total** | **890** | **2,245,983,952** | |

The largest manual-review concentrations are Stage 23 probability/model artifacts, Stage 28 seed/model/target arrays, Stage 27/28 operational-target artifacts, Stage 16 fitted models and holdout matrices, and Stage 22 memberships/probabilities. The path-level list, sizes, hashes, dimensions, stage labels, and reasons are authoritative in the inventory; group summaries do not replace that enumeration.

No fitted model was upgraded from manual review. No record- or packet-bound derivative was upgraded based solely on repository authorship or dataset availability.

## Clearly excluded

`EXCLUDE` contains 12 files totaling 57,426,213 bytes:

- nine raw/near-raw scientific arrays totaling 57,407,905 bytes: the Stage 16 raw holdout feature matrix and eight Stage 19 `one_second_raw` NPZ materializations;
- three tracked Python bytecode caches totaling 18,308 bytes, which are unnecessary for a source release and lack a defensible release role.

No raw PCAP is tracked at the baseline. If a PCAP or raw CIC dataset appears in a later release candidate, it must default to `EXCLUDE` regardless of Git history until separately reviewed.

## Third-party assets

No tracked standalone file was positively identified as a third-party asset during static license/header inspection, so the `THIRD_PARTY_ASSET` class has zero rows. This is not a blanket conclusion that every artifact is free of third-party rights. External dependencies remain separately licensed and are not vendored; executed notebooks, fitted formats, and uncertain embedded content remain under manual review.

## Proposed archive

`PROPOSED_ZENODO_FILELIST.txt` is the exact baseline-derived allowlist: 3,617 paths and 81,426,796 bytes. It contains no `MANUAL_RIGHTS_REVIEW`, `EXCLUDE`, or `UNKNOWN` entry.

`ZENODO_EXCLUSION_LIST.txt` is the exact holdback ledger: 902 paths comprising all 890 manual-review items and all 12 clear exclusions. It records status, provenance class, record-bound flag, size, path, and rights basis.

The proposed archive size excludes ZIP/TAR container overhead or compression and excludes post-baseline inventory administration. No scientific file was copied, archived, transformed, or deleted to calculate it.

## Required decisions before release authorization

1. Supervisor/rights owner must disposition all 890 manual-review paths, preferably by coherent groups plus documented exceptions.
2. Any approved record-bound or model group must receive a written rights basis and required notices before its status changes.
3. The eventual tag candidate must be re-inventoried, including these administrative documents and any subsequent changes.
4. The proposed file list and archive byte total must be regenerated from that final candidate.
5. A separate explicit approval is required before creating a release tag or Zenodo deposit.

Until those decisions are complete, the current allowlist is a proposal only.
