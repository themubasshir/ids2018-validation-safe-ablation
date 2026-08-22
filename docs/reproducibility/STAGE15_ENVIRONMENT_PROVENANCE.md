# Stage 15 Environment Provenance

This note scopes runtime evidence to the duplicate-safe FT-Transformer work in
physical notebook cells 162-170 and 172-189. It is not a repository-wide
environment claim and does not apply to any other stage.

## Proven preprocessing/runtime receipt

`results/stage15_transformer_checkpoint/stage15_2_preprocessing_and_compatibility_metadata.json`
records Python 3.12.13, NumPy 2.4.6, pandas 2.3.3 and scikit-learn 1.6.1.
That receipt also records a system PyTorch 2.10.0+cu128 binary on a Tesla
P100-PCIE-16GB. Its compiled architecture list omitted the P100-required
`sm_60` target, so GPU training readiness was not passed. The recorded CPU
smoke test does not make that system CUDA binary a valid Stage15 GPU runtime.

## Proven isolated GPU runtime

`results/stage15_transformer_checkpoint/stage15_2g_isolated_environment.json`
records the corrective isolated environment:

- PyTorch: `2.7.1+cu118`
- PyTorch CUDA runtime: `11.8`
- device: `Tesla P100-PCIE-16GB`
- device capability: `6.0`
- required compiled architecture: `sm_60`
- required architecture present: `true`
- system PyTorch modified: `false`

The isolated receipt records successful matrix multiplication, FT-Transformer
forward pass, backward pass and optimizer step. It also records the expected
159,169 parameters, input shape 256x70 and output shape 256. The holdout was
untouched during this compatibility verification.

The later one-time holdout metadata independently records PyTorch
`2.7.1+cu118`, CUDA 11.8 and the same P100 capability. This is corroboration of
the Stage15 runtime, not permission to repeat the holdout event.

## Checkpoint provenance

The Stage15.5B pre-holdout lock freezes five `FT_BALANCED` checkpoints:

| Seed | Checkpoint suffix | Bytes | SHA256 |
|---:|---|---:|---|
| 7 | `stage15_4b_models/FT_BALANCED_seed_7_best_extended.pt` | 1,968,137 | `07ab2289b41ae933ce28f3d19a92cf44bb863439209c607254e400c6b0732c31` |
| 29 | `stage15_4a_models/FT_BALANCED_seed_29_best.pt` | 1,966,137 | `b4f8fd466133fd519273bffd9a9db0fa486e77aadf1b3037887491de4415610c` |
| 101 | `stage15_4a_models/FT_BALANCED_seed_101_best.pt` | 1,966,315 | `0b93392ad23440818dd9f10ad4005f452331e3b52ff119fced4cf126e2f2a552` |
| 313 | `stage15_4c_models/FT_BALANCED_seed_313_best.pt` | 1,966,315 | `51bc59b0d894ce4395a0c6cf0e54090daec4d132c358092263ba4f408c59a739` |
| 997 | `stage15_4c_models/FT_BALANCED_seed_997_best.pt` | 1,966,315 | `c0564a47ad4d1f7bd6ce91b06086c41043646b31aa3d751c24d8f44083114b66` |

Verify-only streams these files solely to calculate byte counts and SHA256.
It does not call PyTorch, deserialize a checkpoint, construct a model or run
inference.

## Scientific boundary

The historical receipt sequence is:

1. architecture, threshold 0.73 and checkpoint set locked;
2. holdout unopened, evaluation count zero;
3. one locked five-checkpoint inference event;
4. holdout status `EVALUATED_ONCE`, evaluation count one;
5. no architecture, checkpoint, threshold, calibration or training change.

This extraction preserves that sequence. It did not train the FT-Transformer,
load checkpoints, infer probabilities, select a threshold, reconstruct the
duplicate-safe scientific split or open the holdout.
