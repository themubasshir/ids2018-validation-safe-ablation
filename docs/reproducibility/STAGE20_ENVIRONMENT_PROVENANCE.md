# Stage 20 environment provenance

## Scope rule

Stage 20 did not run in one stable environment. The records below remain
separate because they prove different historical operations. They must not be
merged with one another, with Stage15 PyTorch 2.7.1+cu118, or with later-stage
runtimes. A package-install intention is not treated as proof of the runtime
that produced a scientific artifact.

## Environment ledger

| Scope | Notebook/artifact evidence | Proven | Not proven / limitation |
|---|---|---|---|
| Historical Java/jNetPcap/CICFlowMeter forensics | Cells 330-367; C8 and jNetPcap forensic artifacts | `ahlashkari/CICFlowMeter` commit `eaa853dd82f08ba5288bb7f295b471de7313f883` was inspected; Java 8 `HashMap` positional order was source-derived | Java runtime version and jNetPcap version are `VERSION_NOT_PROVEN`; inspected public source is not claimed byte-identical to the July 2017 build |
| Early Python reconstruction/recovery sessions | Cells 315 and 348-411 | Multiple recovery sessions and their scientific boundaries are preserved | Python, NumPy, PyArrow and Scapy versions for the complete C1-C16 chain are `VERSION_NOT_PROVEN` |
| Compact-corpus reference decoder | Cells 423-434; 1E1 manifests | Scapy 2.6.1 reference-only decoding is named by the frozen manifests | Other package versions for every daily materialization session are not generalized from adjacent receipts |
| Initial incompatible Stage20 CNN environment | Cell 446 diagnostic output | Python 3.12.13; PyTorch 2.10.0+cu128; CUDA build 12.8; cuDNN integer version 91002; Tesla P100-PCIE-16GB; driver 580.159.04; compute capability 6.0 | Compiled architectures began at `sm_70`; the minimal CUDA kernel probe failed because `sm_60` was absent. No training or Thursday/Friday access occurred in this diagnostic |
| Isolated CNN training and Thursday validation | Cells 447-449; E2 manifest; E3 prelock/evaluation | Python 3.12.13; NumPy 2.4.6; PyTorch 2.10.0+cu126; CUDA 12.6; cuDNN integer version 91002; Tesla P100-PCIE-16GB; compute capability 6.0; compiled `sm_60`; deterministic algorithms enabled; AMP and TF32 disabled | Versions not present in the E2/E3 receipts remain unproven |
| Later Colab final-holdout amendment | Current E4 Colab/Xet/final artifacts | Python 3.12.13; PyTorch 2.10.0+cu126; CUDA build 12.6; Tesla T4; compute capability 7.5; deterministic synthetic probe passed | No physical cell in 312-461 executes this later path; status is `NOTEBOOK_CELL_NOT_MAPPED` |

## Isolated CNN runtime chronology

Cell 446 is a read-only failure diagnostic. The installed PyTorch
2.10.0+cu128 build reported CUDA 12.8 and did not contain an `sm_60` kernel.
The P100 capability was 6.0 and the tensor/add/synchronize probe failed before
model transfer, training, optimizer construction, or Thursday/Friday access.

Cell 447 installed PyTorch 2.10.0+cu126 into an isolated target rather than
restarting or replacing the notebook interpreter. That build listed `sm_60`
and passed the P100 CUDA probe. Cell 448 launched the exact frozen E2 worker in
an isolated subprocess. The resulting E2 manifest separately records Python
3.12.13, NumPy 2.4.6, PyTorch 2.10.0+cu126, CUDA 12.6, cuDNN 91002 and the P100.
Cell 449 reused the frozen epoch-10 state for the one-pass Thursday evaluation.

The later Colab record changes the execution host to a T4 without changing the
scientific protocol. Its existence is frozen evidence, but the accepted
notebook has no corresponding execution cell. The E4 cells in the notebook
must therefore not be cited as the source of the completed Colab artifacts.

## Verification boundary

Extraction verified repository artifact size and SHA-256 values only. It did
not import PyTorch, load the checkpoint, inspect tensors, run a model forward,
open compact corpora, or access Thursday/Friday scientific data. Unknowns
remain `VERSION_NOT_PROVEN`.
