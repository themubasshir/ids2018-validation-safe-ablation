# Stage 20 substage and evidence map

## Scope and evidence rule

This map is the required boundary checkpoint before Stage 20 methodology extraction. It covers physical notebook cells 312–461 only. Cells 462–488 belong to Stage 21 and are not mapped or extracted here.

The mapping was reconstructed from four evidence layers, in descending priority:

1. the code and recorded outputs in `notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb`;
2. frozen Stage 20 JSON/CSV/checksum artifacts in `results/`;
3. commit and protocol identifiers embedded in those cells and artifacts;
4. current repository folder names, used only after the historical label was established.

Folder names alone were not treated as proof of notebook provenance. The per-cell evidence is in `docs/reproducibility/STAGE20_CELL_MAP.csv`.

## Historical program structure

| Physical cells | Historical branch | Scientific role | Principal frozen artifact family |
|---:|---|---|---|
| 312 | Stage20-0 | Authentic packet-image/ViT representation protocol lock | `results/stage20_vit_packet_image/stage20_0_representation_protocol_lock/` |
| 313–315 | Stage20-1A | Mounted-source/acquisition preflight and Scapy runtime repair | Protocol/output evidence; no durable scientific result family |
| 316–325 | Stage20-1B | Label acquisition, Thursday source hygiene, alignment sufficiency, duration/timestamp/signature audits, and packet-to-label reconstruction freeze | `results/stage20_vit_packet_image/stage20_1b3_label_hygiene_freeze/`; `stage20_1b4e_packet_label_reconstruction_freeze/` |
| 326–335 | Stage20-1C1/C2 | Monday PCAP integrity, bounded alignment, original label serialization, and source-faithful timestamp canonicalization | Notebook outputs and later reconstruction receipts |
| 336–346 | Stage20-1C3–C10 | Exact-S4 pilots, discrepancy localization, historical-source replay, flag serialization correction, and corrected replay | `results/stage20_flag_serialization_correction/`; `results/stage20_jnetpcap_forensic/` |
| 347–367 | Stage20-1C11–C14 | Direct jNetPcap/Scapy packet and payload forensics, reset recovery, TCP geometry, and frozen TCP payload semantics | `results/stage20_jnetpcap_forensic/`; `results/stage20_tcp_payload_semantics/` |
| 368–378 | Stage20-1C15 | Reconstruction runtime preflight, reproduction drift, timestamp/lifecycle localization, D5 source-faithful baseline erratum, and negative global TCP-payload validation | `results/stage20_c15_baseline_erratum/`; `results/stage20_c15_payload_validation/` |
| 379–411 | Stage20-1C16 | Transition-cohort freeze, repeated runtime/source recovery, authoritative source reconciliation, D-cohort directional semantics, bounded packet-geometry phenotype, and stopped mechanism search | `results/stage20_1c16_runtime_recovery/` |
| 412–422 | Stage20-1D | Packet-image selection, storage-aware daily geometry profiling, train-only geometry freeze, and fixed encoder verification | `results/stage20_1d_representation/` |
| 423–434 | Stage20-1E0/E1 | CNN/training protocol, Monday–Wednesday TRAIN compact corpora, Thursday VALIDATION compact corpus, and Thursday all-NULL-suffix erratum | `results/stage20_1e_training/stage20_1e0_*`; `stage20_1e1*` manifests/receipts |
| 435–448 | Stage20-1E2 | Frozen CNN training attempts, auxiliary Thursday diagnostics, CUDA incompatibility diagnosis, isolated cu126 runtime, and exact worker launch | `results/stage20_1e_training/stage20_1e2_*` |
| 449–454 | Stage20-1E3 | One-pass Thursday validation execution, frozen operating points, and hash-only durability recovery | `results/stage20_1e_training/stage20_1e3_*` |
| 455–461 | Stage20-1E4 | Friday pre-opening lock, one Kaggle opening attempt, storage diagnostics, constrained cleanup, and CUDA dependency audit | `results/stage20_1e_training/stage20_1e4_friday_holdout_execution_lock.json` only maps directly to these notebook cells |

## Critical chronology and negative-result boundaries

- Stage 18's historical ViT conclusion remains `NOT_SUPPORTED_BY_CURRENT_ARTIFACTS`. Stage 20 later recovered packet-level evidence; it does not retroactively change what was known in Stage 18.
- Stage 20 distinguishes historical raw-exact reconstruction from the D5 source-faithful accepted baseline. These quantities must not be collapsed.
- C8 freezes flag-serialization semantics. C15-D5 freezes the timestamp/lifecycle baseline erratum. C16 records exact/absent transition cohorts and closes its bounded mechanism search with a negative result.
- The 1D packet-image representation is fixed at `64 x 256 x 1`; daily TRAIN profiling precedes its numeric-dimension freeze.
- The 1E CNN uses Monday–Wednesday for TRAIN, Thursday for VALIDATION, and Friday only after a remotely verified pre-opening lock.
- The Kaggle E4 worker in cell 455 stopped after the Friday authorization/opening sequence because of an operational storage gate. Cells 456–461 are diagnostics and cleanup/dependency audits, not final Friday inference.

## Artifacts not directly produced by notebook cells 312–461

The following current artifacts record a later Colab/Xet recovery and completed Friday evaluation, but no physical cell in the accepted Stage 20 notebook boundary directly executes that recovery:

- `results/stage20_1e_training/stage20_1e4_colab_execution_environment_amendment.json`
- `results/stage20_1e_training/stage20_1e4_colab_xet_fixed4_transport_lock.json`
- `results/stage20_1e_training/stage20_1e4_colab_xet_interruption_recovery_lock.json`
- `results/stage20_1e_training/stage20_1e4_friday_holdout_compact_corpus_manifest.json`
- `results/stage20_1e_training/stage20_1e4_friday_probabilities.npy`
- `results/stage20_1e_training/stage20_1e4_friday_holdout_evaluation.json`
- `results/stage20_1e_training/stage20_1e4_friday_raw_source_release_receipt.json`

They may be verified as frozen repository evidence, but their execution provenance must be reported as `NOTEBOOK_CELL_NOT_MAPPED` rather than assigned to a guessed cell.
