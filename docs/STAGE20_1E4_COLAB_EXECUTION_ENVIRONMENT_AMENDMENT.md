# Stage20-1E4-COLAB-PRE — Execution Environment Amendment

**FROZEN AND REMOTELY DURABLE BEFORE ANY FRIDAY ACCESS**

Parent E4-PRE commit: `df6a13158651c2b5e7d1f69b7341ac15af01394e`

Kaggle GPU quota was unavailable before the authorized Friday holdout execution. The execution host is migrated to Google Colab **before any Friday source access**.

## Scientific protocol — UNCHANGED

- representation: **64 × 256 × 1**
- model: **fixed epoch-10 Stage20MaskedCNNv1**
- checkpoint SHA256: `3ebc71e579dc8e0e545981b2d60eea643148fe53e0902f8df8e47556243ad30b`
- canonical state SHA256: `ae9c913b13db62ab933198dd7721f0d1826b26a55773e3b560dc735cbb8c8092`
- exact directed 21-field S4 join only
- decoder: **Scapy 2.6.1 reference only**
- Friday PCAP reconstruction passes: **1**
- Friday first-50k pilot: **NO**
- Friday model inference passes: **1**
- thresholds: **0.50 / 0.17 / 0.17**
- Friday threshold search/reselection: **NO**
- retraining/adaptation: **NO**

## Colab environment

- torch: `2.10.0+cu126`
- CUDA build: `12.6`
- GPU: `Tesla T4`
- capability: `[7, 5]`
- deterministic algorithms: **True**
- cuDNN deterministic: **True**
- TF32 disabled: **True**
- synthetic fixed-probe exact repeatability: **YES**

Friday accessed at amendment: **NO**

Amendment JSON SHA256: `8fd22f9a71c649a5f443b137b096e0f36fd06bea2beb1cbb10ef8c7b784cfc1a`
