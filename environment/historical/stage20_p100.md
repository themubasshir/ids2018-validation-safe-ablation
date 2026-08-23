# Stage20 P100 Environment

The isolated Stage20 CNN training and Thursday evaluation runtime proves:

- Python 3.12.13
- NumPy 2.4.6
- PyTorch 2.10.0+cu126
- CUDA 12.6
- cuDNN 9.1.0.2
- Tesla P100-PCIE-16GB with `sm_60`

This record applies to the isolated CNN/Thursday path only. Early Java,
jNetPcap, Python and Scapy forensic versions remain independently unproven.
The Scapy 2.6.1 compact-corpus decoder record is also a separate lineage.

Source: `docs/reproducibility/STAGE20_ENVIRONMENT_PROVENANCE.md`.
