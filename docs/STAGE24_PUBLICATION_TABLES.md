# Stage24 Publication Tables

These tables are derived exclusively from the frozen Stage24 result artifacts.
No model fitting, inference, target threshold selection, calibration, feature
selection, or post-target adaptation is performed during publication packaging.

## Table 24-1. Bidirectional cross-dataset generalization

| direction             | target                               | bridge   | semantics                       |   target_prevalence |   pr_auc |   pr_excess |   pr_normalized |   roc_auc |    brier | note                                                                                                     |
|:----------------------|:-------------------------------------|:---------|:--------------------------------|--------------------:|---------:|------------:|----------------:|----------:|---------:|:---------------------------------------------------------------------------------------------------------|
| IDS2018 -> CICIDS2017 | CICIDS2017 full effective population | bridge62 | PUBLISHED                       |            0.196996 | 0.667483 |    0.470486 |        0.585908 |  0.733946 | 0.145756 |                                                                                                          |
| IDS2018 -> CICIDS2017 | CICIDS2017 full effective population | bridge62 | FLAG_CORRECTED                  |            0.196996 | 0.667483 |    0.470486 |        0.585908 |  0.733946 | 0.145756 | Bitwise identical to bridge62 PUBLISHED because bridge62 excludes all eight aggregate flag-count fields. |
| IDS2018 -> CICIDS2017 | CICIDS2017 full effective population | bridge70 | PUBLISHED                       |            0.196996 | 0.663981 |    0.466985 |        0.581547 |  0.741891 | 0.142912 |                                                                                                          |
| IDS2018 -> CICIDS2017 | CICIDS2017 full effective population | bridge70 | FLAG_CORRECTED                  |            0.196996 | 0.656252 |    0.459256 |        0.571923 |  0.744083 | 0.147998 |                                                                                                          |
| CICIDS2017 -> IDS2018 | IDS2018 02-28-2018                   | bridge62 | FLAG_CORRECTED source semantics |            0.104847 | 0.108176 |    0.003329 |        0.003719 |  0.525167 | 0.105758 |                                                                                                          |
| CICIDS2017 -> IDS2018 | IDS2018 02-28-2018                   | bridge70 | FLAG_CORRECTED source semantics |            0.104847 | 0.107419 |    0.002572 |        0.002874 |  0.525302 | 0.105652 |                                                                                                          |

**Interpretation note.** PR-AUC is reported together with each target
prevalence and normalized PR-AUC because the two directions use different
target prevalences. The two transfer directions are not averaged.

## Table 24-2. Paired stratified bootstrap contrasts

| direction             | comparison                                        | metric   |   point_difference |    ci_2_5 |   ci_97_5 | ci_excludes_zero   |   replicates |   seed |
|:----------------------|:--------------------------------------------------|:---------|-------------------:|----------:|----------:|:-------------------|-------------:|-------:|
| IDS2018 -> CICIDS2017 | bridge70 PUBLISHED - bridge62 PUBLISHED           | PR_AUC   |          -0.003502 | -0.003856 | -0.003152 | True               |         2000 |     42 |
| IDS2018 -> CICIDS2017 | bridge70 PUBLISHED - bridge62 PUBLISHED           | ROC_AUC  |           0.007945 |  0.007793 |  0.008096 | True               |         2000 |     42 |
| IDS2018 -> CICIDS2017 | bridge70 PUBLISHED - bridge62 PUBLISHED           | BRIER    |          -0.002844 | -0.002915 | -0.002766 | True               |         2000 |     42 |
| IDS2018 -> CICIDS2017 | bridge70 FLAG_CORRECTED - bridge62 FLAG_CORRECTED | PR_AUC   |          -0.01123  | -0.011619 | -0.010858 | True               |         2000 |     42 |
| IDS2018 -> CICIDS2017 | bridge70 FLAG_CORRECTED - bridge62 FLAG_CORRECTED | ROC_AUC  |           0.010137 |  0.009981 |  0.010303 | True               |         2000 |     42 |
| IDS2018 -> CICIDS2017 | bridge70 FLAG_CORRECTED - bridge62 FLAG_CORRECTED | BRIER    |           0.002243 |  0.002153 |  0.002336 | True               |         2000 |     42 |
| IDS2018 -> CICIDS2017 | bridge70 FLAG_CORRECTED - bridge70 PUBLISHED      | PR_AUC   |          -0.007729 | -0.007921 | -0.007534 | True               |         2000 |     42 |
| IDS2018 -> CICIDS2017 | bridge70 FLAG_CORRECTED - bridge70 PUBLISHED      | ROC_AUC  |           0.002192 |  0.002139 |  0.002246 | True               |         2000 |     42 |
| IDS2018 -> CICIDS2017 | bridge70 FLAG_CORRECTED - bridge70 PUBLISHED      | BRIER    |           0.005087 |  0.005023 |  0.005152 | True               |         2000 |     42 |
| CICIDS2017 -> IDS2018 | bridge70 - bridge62                               | PR_AUC   |          -0.000757 | -0.001058 | -0.000435 | True               |         2000 |     42 |
| CICIDS2017 -> IDS2018 | bridge70 - bridge62                               | ROC_AUC  |           0.000135 | -0.0009   |  0.001263 | False              |         2000 |     42 |
| CICIDS2017 -> IDS2018 | bridge70 - bridge62                               | BRIER    |          -0.000106 | -0.000124 | -8.9e-05  | True               |         2000 |     42 |

All differences use the stated left-minus-right orientation. Confidence
intervals are percentile 95% intervals from 2,000 paired class-stratified
bootstrap replicates with seed 42.

## Table 24-3. Source-selected threshold transfer to IDS2018 Feb-28

| bridge   | operating_point   |   threshold |   tp |     tn |   fp |    fn |   precision |   recall |       f1 |       f2 |      fpr |      fnr |
|:---------|:------------------|------------:|-----:|-------:|-----:|------:|------------:|---------:|---------:|---------:|---------:|---------:|
| bridge62 | STANDARD          |        0.5  |   24 | 530728 |  796 | 62232 |    0.029268 | 0.000386 | 0.000761 | 0.00048  | 0.001498 | 0.999614 |
| bridge62 | BALANCED          |        0.17 |   38 | 530458 | 1066 | 62218 |    0.03442  | 0.00061  | 0.001199 | 0.00076  | 0.002006 | 0.99939  |
| bridge62 | SECURITY          |        0.05 |   84 | 529914 | 1610 | 62172 |    0.049587 | 0.001349 | 0.002627 | 0.001675 | 0.003029 | 0.998651 |
| bridge70 | STANDARD          |        0.5  |   24 | 530812 |  712 | 62232 |    0.032609 | 0.000386 | 0.000762 | 0.00048  | 0.00134  | 0.999614 |
| bridge70 | BALANCED          |        0.18 |   38 | 530481 | 1043 | 62218 |    0.035153 | 0.00061  | 0.0012   | 0.00076  | 0.001962 | 0.99939  |
| bridge70 | SECURITY          |        0.05 |   51 | 530194 | 1330 | 62205 |    0.03693  | 0.000819 | 0.001603 | 0.001018 | 0.002502 | 0.999181 |

Thresholds were selected exclusively on CICIDS2017 Thursday source validation.
No IDS2018 target threshold search was performed.

## Table 24-4. Governance and evaluation populations

| item                                    |   value | detail                                                                     |
|:----------------------------------------|--------:|:---------------------------------------------------------------------------|
| Primary target population               | 2830743 | CICIDS2017: 2,273,097 benign / 557,646 attack / prevalence=0.196996336298  |
| Secondary target population             |  593780 | IDS2018 Feb-28: 531,524 benign / 62,256 attack / prevalence=0.104846912998 |
| Scientific fits                         |       4 | 4/4 completed; no additional fits authorized                               |
| Evaluable target openings               |       6 | 6/6 completed                                                              |
| Administratively cancelled target cells |       2 | bridge62/bridge70 GROUNDED_S4; not reallocated                             |
| Bootstrap replicates                    |    2000 | Paired stratified bootstrap; seed 42                                       |

## Frozen artifact identities

- Stage24 final synthesis SHA256: `785bbcb00140f4d7e07e9b49ad33924166b5995e66a229c986d5b1abcbcaee4b`
- Primary bootstrap SHA256: `96732023e0a1c9b52a79fafa59ea4b851ef7f8bae1814e4b4b4fde0ef0df09aa`
- Secondary bootstrap SHA256: `28005e0f13d86658ba81e6b19dc154b94eedb316ea5ce0348287265c00541953`
