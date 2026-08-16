# Stage22-2B — Development/Validation Model Input Seal

## Status

**SEALED AFTER DEVELOPMENT/VALIDATION LABEL ACCESS AND PREPROCESSING FIT, BEFORE ANY MODEL FIT OR INFERENCE**

Scientific parent:

`f22fb0d931be6c3ca0e4314939d4b584a0161116`

Manifest SHA256:

`bfb26edeaf4e29225b38b0c804994abfa292b748155c991ead705cba65612bdb`

## First Stage22 non-final label opening

Stage22-2B is the first Stage22 step that semantically reads `binary_label`.

The semantic access boundary is strictly:

- DEVELOPMENT: **156,821 rows**
- VALIDATION: **15,245 rows**

FINAL_TEST remains sealed:

- FINAL_TEST membership: **68,867 rows**
- FINAL_TEST lines decoded: **0**
- FINAL_TEST predictor fields parsed: **0**
- FINAL_TEST `binary_label` fields parsed: **0**
- final outcome openings consumed: **0**

The flagship CSV was traversed as opaque bytes only to preserve the frozen physical row ordinal. Only DEVELOPMENT and VALIDATION lines were copied into temporary extraction files and parsed.

## Observed frozen class composition

### DEVELOPMENT

- benign: **103,052**
- attack: **53,769**
- total: **156,821**
- attack rate: **0.342868620912**

### VALIDATION

- benign: **15,245**
- attack: **0**
- total: **15,245**
- attack rate: **0.000000000000**
- both binary classes present: **NO**

No day or role was changed after observing these labels.

## Transformer scaler

A new `StandardScaler(copy=True, with_mean=True, with_std=True)` was fit on DEVELOPMENT predictors only.

- DEVELOPMENT rows in fit: **156,821**
- VALIDATION rows in fit: **0**
- FINAL_TEST rows in fit: **0**
- clipping: **NO**
- imputation: **NO**

Scaler artifact:

`results/stage22_temporal_session_safe/stage22_2b_development_standard_scaler.joblib`

SHA256:

`06509ba01d930f3bbbe2682c584812df5a8e1f68014532d81eaa7551d026c995`

Canonical scaler-stat hashes:

- mean_: `b379e81a9c2905cd18f90eba9918128981c8986671b46df55af8d09d955347c0`
- var_: `6380db428723f944ffb14741fe3130412ecd789cc6b436fabf4bad5115e2dc35`
- scale_: `6d313eaa24efc0a8fd56f03888abffbc02db67bc0b2fabc18a67147f107f60b6`

## Transformer positive-class weight

Frozen formula:

`development benign / development attack`

Value:

`1.9165690267626327`

Only DEVELOPMENT labels contributed to this statistic.

## Classical inputs

The Stage16 classical family receives the exact raw float32 70-feature matrices.

No scaler is used.

## Sealed local model-input cache

Cache root:

`/kaggle/working/stage22_model_cache/stage22_2b`

The cache is intentionally outside Git. The repository stores its exact SHA256 manifest.

- `development_row_ids_int64.npy` — shape `[156821]`, dtype `int64`, SHA256 `e714e7a0a817b14dfe2e9049a89829cc85cfb704e9c6c1f81cc10adc9f29e3ff`
- `validation_row_ids_int64.npy` — shape `[15245]`, dtype `int64`, SHA256 `ff5746166ffdb42848b5d52aaf0502b6c2148977ecc969f818234bd8492a664e`
- `X_development_raw_float32.npy` — shape `[156821, 70]`, dtype `float32`, SHA256 `49ec0992f2dbd7248e810b341f6de9c74031434841a721cc0a374414f87f789a`
- `X_validation_raw_float32.npy` — shape `[15245, 70]`, dtype `float32`, SHA256 `60bef1bb8b28d6f4ac2996cdc172763de274512dc0d242c12bcfb719ae9aeee0`
- `X_development_scaled_float32.npy` — shape `[156821, 70]`, dtype `float32`, SHA256 `afa37c433fd099e9c532d3860e2c2238843a58c866274202b0b0c23704b0a3fb`
- `X_validation_scaled_float32.npy` — shape `[15245, 70]`, dtype `float32`, SHA256 `e240be68ba3fcca3fdd23d192fe8f1510ed54cb2bafb97b6cba02305ca18e71b`
- `y_development_int8.npy` — shape `[156821]`, dtype `int8`, SHA256 `a4e1269d2400d5b8b5803204465e4e296d762ec5b34ed8c95de1439bbe66b615`
- `y_validation_int8.npy` — shape `[15245]`, dtype `int8`, SHA256 `a7c2acfdee6c4fcdffcce91aa6e846c60822dd28a2f0e70f99dfdc95b18da09b`


Any later model-training cell must verify these exact hashes before fitting.

If the local cache is ever lost, it may only be deterministically rematerialized from the same frozen parent artifacts and must reproduce every sealed hash before training.

## Model activity

Stage22-2B performed:

- model fit: **NO**
- optimizer step: **NO**
- inference: **NO**
- validation model metric: **NO**
- threshold selection: **NO**
- final-test metric: **NO**

## Next scientific boundary

Training authorized next: **NO**

The frozen partition does not provide the class support required by the inherited training/checkpoint recipe.

This is a scientific hard stop. No split repair, day reassignment, threshold relaxation, feature change, or model substitution is allowed.
