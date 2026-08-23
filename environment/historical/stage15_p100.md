# Stage15 Isolated P100 Environment

The accepted Stage15 runtime is PyTorch 2.7.1+cu118 with CUDA 11.8 on a Tesla
P100-PCIE-16GB. The environment proved required `sm_60` kernel availability
and passed matrix, forward, backward and optimizer probes.

A system PyTorch 2.10.0+cu128 receipt is retained as a superseded incompatible
state because it lacked the required P100 architecture. It must not be called
the Stage15 training environment.

Source: `docs/reproducibility/STAGE15_ENVIRONMENT_PROVENANCE.md` and
`configs/stage15/protocol.json`.
