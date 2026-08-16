# Stage21-2 — Frozen Masked ViT Training

## Status

**Stage21MaskedViTv1 trained for exactly 10 preregistered epochs on
Monday + Tuesday + Wednesday TRAIN only.**

Parent commit:

`de15ff09907c5a0fdecbd51cc457a28adb80bb3f`

## Scientific boundary

- TRAIN: Monday + Tuesday + Wednesday only
- Thursday model forward during Stage21-2: **NO**
- Thursday probabilities generated: **NO**
- Thursday threshold selection: **NO**
- Friday accessed: **NO**
- validation during training: **NO**
- epoch selection: **NO**
- architecture search: **NO**
- additional ViT candidate: **NO**

Epoch 10 is final because the epoch count was frozen before training.

## TRAIN population

- flows: **545,630**
- BENIGN: **541,174**
- ATTACK: **4,456**
- frozen positive-class weight: **121.448384201077**

## Frozen optimization

- model: `Stage21MaskedViTv1`
- trainable parameters: **91,969**
- seed: **42**
- epochs: **10**
- batch size: **256**
- batches per epoch: **2,132**
- optimizer steps: **21,320**
- AdamW learning rate: **0.001**
- weight decay: **0.0001**
- betas: **(0.9, 0.999)**
- eps: **1e-8**
- BCEWithLogitsLoss
- gradient clipping: **5.0**
- AMP: **NO**
- scheduler: **NONE**
- augmentation: **NONE**
- early stopping: **NO**

## Runtime

- Python: **3.12.13**
- NumPy: **2.4.6**
- Torch: **2.10.0+cu126**
- CUDA build: **12.6**
- GPU: **Tesla T4**
- TF32: **OFF**
- deterministic algorithms: **ON**

## Epoch audit

| Epoch | Seed | Mean weighted BCE | Canonical model-state SHA256 | Cumulative steps |
|---:|---:|---:|---|---:|
| 1 | 42 | 0.123155996 | 5290fef51ad70d6a90d8635a6218880fb03912170978d737449317711565dcb3 | 2132 |
| 2 | 43 | 0.039344824 | a3ca744d3615ef40d100fafd1191dfcccdfa5b1342bb0470528657c0226eaaa1 | 4264 |
| 3 | 44 | 0.034530769 | 53d6fc86b89a920f09358d10c6ca5c44aa7eb0ea50573eb614ce7520ddc3f79c | 6396 |
| 4 | 45 | 0.025429313 | 85dbbbde3e733476ec7d7a73c2f1690b538878f697677d7f7c31d560de7c2830 | 8528 |
| 5 | 46 | 0.022264535 | 151f29182164643a85a53ec7a5e408b73c47678ed05dc55762480907ea526a2e | 10660 |
| 6 | 47 | 0.019566440 | df13bb24db326b908d0affc2d9162edaf1d5bb2365c9a5f6c75ff5e111ed1ec7 | 12792 |
| 7 | 48 | 0.021019568 | 85ee0da913e946e0f4078fd7456d4c7af5157b89c4a805321d1a4db7b52e5e1d | 14924 |
| 8 | 49 | 0.018091114 | 8ce70c59fbc5bec19078ea3c20e6b4cafc010a79522057481b935f6b09aa3e99 | 17056 |
| 9 | 50 | 0.015329003 | 73848ec91dd5093e1de3e43c03772fe3c512e80bf82242a4f32b98985ebf880f | 19188 |
| 10 | 51 | 0.012896694 | 9da47df6cd5c821eef3d2c8a501296cd6070b835c719999f572f3dec2d560771 | 21320 |

## Frozen epoch-10 checkpoint

- file: `results/stage21_architecture/stage21_2_epoch10_model_state_dict.pt`
- file SHA256: `221e9c805fb663acacf2f0f2ca95dba7cb4b2ec4c4de5a3650cf4adeb99b5ef8`
- canonical tensor-state SHA256: `9da47df6cd5c821eef3d2c8a501296cd6070b835c719999f572f3dec2d560771`

## Provenance

- training manifest SHA256: `e6e92f961052d1900539b5a5cefb90eaac335e73deecf6ae7af22fd0e25211b8`
- exact runtime preflight SHA256: `b730b0b16175828ce299f1b5021048516e436c032532c55ccd68827141817d81`
- executed training harness SHA256: `fd56d6e89527e542618e37168a7df658540c324384bb22e722f9a82ef9eb7cf3`
- recovery release: `stage21-2-training-recovery-v1`
- recovery release ID: `371280600`
- epoch-10 recovery asset ID: `516652935`
- epoch-10 recovery SHA256: `38a3c75c4c46d3758f6a3a3c38190b68a23037947dff03fea5a7fac6162a4ff2`

All ten completed epoch boundaries were durably uploaded before the final
Stage21-2 seal.

## Next checkpoint

**Stage21-3 — evaluate the fixed epoch-10 ViT on Thursday exactly once and
freeze the standard, balanced, and security operating points.**
