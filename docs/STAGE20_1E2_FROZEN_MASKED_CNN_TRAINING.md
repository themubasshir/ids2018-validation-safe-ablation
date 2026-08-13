# Stage20-1E2 — Frozen Masked CNN Training

## Status

**FROZEN Stage20MaskedCNNv1 TRAINED FOR EXACTLY 10 EPOCHS ON M/T/W TRAIN ONLY**

Parent: `c0f3f65bef4ddf1b6cc18639b8ec9013b53ed229`

## Scientific boundary

- TRAIN: **Monday + Tuesday + Wednesday only**
- Thursday validation corpus included in training: **NO**
- Thursday model evaluation: **NO**
- Thursday probability generation: **NO**
- Thursday threshold selection: **NO**
- Friday accessed: **NO**
- Friday status: **CLOSED**
- architecture changed: **NO**
- representation changed: **NO**
- training protocol changed: **NO**

## TRAIN population

- flows: **545630**
- BENIGN: **541174**
- ATTACK: **4456**
- pos_weight: **541174/4456 = 121.448384201077**

Per day:

- Monday: **528509** flows; BENIGN **528509**; ATTACK **0**; manifest `a726d87e044e56171282e9be2fc6220c47de0cd09b153624062713f1c3116892`
- Tuesday: **4170** flows; BENIGN **4008**; ATTACK **162**; manifest `20f920b576b49a36131fb271e963ef2bd7900f3c7bfc5458b24991676b5515af`
- Wednesday: **12951** flows; BENIGN **8657**; ATTACK **4294**; manifest `42a8f3813a786751999c209dce323ba701d9c29cd19add09aaadbd3297921d62`

## Frozen training protocol

- model: **Stage20MaskedCNNv1**
- trainable parameters: **93025**
- seed: **42**
- epochs: **10 fixed**
- batch size: **256**
- drop_last: **NO**
- batches per epoch: **2132**
- final batch size: **94**
- optimizer steps: **21320**
- loss: **BCEWithLogitsLoss**
- optimizer: **AdamW**
- learning rate: **0.001**
- weight decay: **0.0001**
- gradient clip max norm: **5.0**
- scheduler: **NONE**
- early stopping: **NO**
- augmentation: **NONE**
- AMP: **NO**
- validation during training: **NO**

## Epoch audit

- Epoch 1: seed **42**; permutation `de1012063844a04591311c784c6c1584a9f2c793f3a4354490f6dca7a03a6ee4`; mean weighted BCE **0.274838773**; state `4ac102394db39cc7125fa10d571bb96792252e0e2a7f7a4d0e01f534e92f70a0`; optimizer steps cumulative **2132**
- Epoch 2: seed **43**; permutation `6b894f543574743120b96e9f4416f4776c32e1199290fb2028df268bba54fccb`; mean weighted BCE **0.033894974**; state `3c7c0f1b2333e24a79c89edbdcf333a91447150c6663e8ac5ce2d0442a645347`; optimizer steps cumulative **4264**
- Epoch 3: seed **44**; permutation `7f5637f40b719404e6b4c36c95f600ce177dcfe4c9dece2fc02f4066a9fa6e11`; mean weighted BCE **0.015609289**; state `c5dec6d17f2cd52b6ab6bce9bfa9c5a5e9408375654c05abf5bd4b14365d557f`; optimizer steps cumulative **6396**
- Epoch 4: seed **45**; permutation `45b0b51470f80057624b2b53952b82ea72740af39233262beba01a2e83f0d449`; mean weighted BCE **0.010198480**; state `6670865eb3ed5a75b86d89a01f7e1e3a3d1ed5a33b303e4e4780b24a0483ff90`; optimizer steps cumulative **8528**
- Epoch 5: seed **46**; permutation `2276345b5b7097fd7d591894ecaa5e20ad3fbc84b138459e1e7daaa63cb332c8`; mean weighted BCE **0.005890215**; state `ab1631b61b501924218ebfd54e73accab849b33233f458323b2f783643b2acaf`; optimizer steps cumulative **10660**
- Epoch 6: seed **47**; permutation `13b2aa847368c7cc50516cbb92c98a22bb4763e0a82649bddc7da49b1905c36a`; mean weighted BCE **0.007102119**; state `ea862f84e200806d5e7bb8cb3482e4edeb98d44885359b83e22707b00d32f6f1`; optimizer steps cumulative **12792**
- Epoch 7: seed **48**; permutation `4ac3216ab2e7e18c28ce74141f9329485f1d9f0a217c2bbf5ca5045719cb324a`; mean weighted BCE **0.006844145**; state `335328c50f4acc891743688d9019d5d52799d39234f5e6d205935c1eb29d4b9f`; optimizer steps cumulative **14924**
- Epoch 8: seed **49**; permutation `90d8d64698703698d24dee7ac0338dc5f3a7f68cad34fdb3a7f9fd325ef779dc`; mean weighted BCE **0.004251996**; state `4a848625255c5f2e9ffa0a33a3722e4a6a4291ba38977ecebb36a69b04a0c2ab`; optimizer steps cumulative **17056**
- Epoch 9: seed **50**; permutation `bd90520ca905011e7a68f282c1b9a8c78061fd7d496c9b74a792c487f982a250`; mean weighted BCE **0.002774820**; state `34fc1fc62a8e2cc93bd18f22e435df2dde0670d8bec40fb45654e73ec3ebdcb7`; optimizer steps cumulative **19188**
- Epoch 10: seed **51**; permutation `160a700ce25fbe9134b5ad2f86532b6d35d443f25dd9d234fa9781131a70705e`; mean weighted BCE **0.005671528**; state `ae9c913b13db62ab933198dd7721f0d1826b26a55773e3b560dc735cbb8c8092`; optimizer steps cumulative **21320**

## Final epoch-10 checkpoint

- state dict: `results/stage20_1e_training/stage20_1e2_epoch10_model_state_dict.pt`
- checkpoint SHA256: `3ebc71e579dc8e0e545981b2d60eea643148fe53e0902f8df8e47556243ad30b`
- checkpoint bytes: **376879**
- canonical tensor-state SHA256: `ae9c913b13db62ab933198dd7721f0d1826b26a55773e3b560dc735cbb8c8092`
- training manifest SHA256: `42ad8bb776972e03c716c2e41d7faca2ef7b4aa9d1ed0787c84c693284bc16a1`

Epoch 10 is final because the epoch count was frozen before training; no validation result selected an epoch.

## Next

**Stage20-1E3 — evaluate the fixed epoch-10 model on Thursday once and freeze the standard, balanced, and security operating points.**
