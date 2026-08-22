# Stage28 — Final robustness and novelty-control synthesis

## Empirical closure

Stage28 closed the preregistered robustness program with **108/108 authorized
new fits consumed and zero remaining fits**. The experiment included 12
historical model reuses in addition to the 108 new fits. After fitting was
permanently closed, Stage28 performed only preregistered zero-fit synthesis and
the authorized Stage22 shared-final-holdout robustness inference. No Stage29
empirical stage is authorized.

The Stage22 shared holdout contained **1,374,133 flows**, including **998,788
benign** and **375,345 attack** flows. Ten frozen Stage22 ensemble realizations
(two validation geometries × five training seeds) were evaluated on this same
holdout. No threshold or model selection was performed on the holdout.

## Stage22 training-seed robustness on the shared final holdout

| Geometry | Metric | Mean | SD | Min | Max |
| --- | --- | --- | --- | --- | --- |
| RANDOM_NATURAL | ROC_AUC | 0.5176 | 0.0073 | 0.5063 | 0.5250 |
| RANDOM_NATURAL | PR_AUC | 0.2599 | 0.0034 | 0.2546 | 0.2628 |
| CHRONOLOGICAL_NATURAL | ROC_AUC | 0.8209 | 0.0085 | 0.8086 | 0.8312 |
| CHRONOLOGICAL_NATURAL | PR_AUC | 0.6388 | 0.0322 | 0.5875 | 0.6769 |

The preregistered directional comparison was stable for every frozen seed.
`PR_AUC_RANDOM_NATURAL < PR_AUC_CHRONOLOGICAL_NATURAL` held for **5/5 seeds**,
and `ROC_AUC_RANDOM_NATURAL < ROC_AUC_CHRONOLOGICAL_NATURAL` also held for
**5/5 seeds**. This is descriptive conclusion-stability analysis rather than a
new significance test.

| Metric | Mean Δ (R-C) | SD | Min | Max | Random<Chrono |
| --- | --- | --- | --- | --- | --- |
| PR_AUC | -0.3788 | 0.0308 | -0.4140 | -0.3290 | 5/5 |
| ROC_AUC | -0.3033 | 0.0090 | -0.3133 | -0.2934 | 5/5 |

These results show that the Stage22 direction was not a seed-42 artifact: the
same random-versus-chronological ranking persisted across seeds 42–46.

## Leave-one-attack-family-out seed stability

The LOAO analysis remained family-specific. The table below reports the number
of frozen seeds (out of five) satisfying each preregistered qualitative
condition. Infiltration is retained only as a descriptive result because its
held-out positive support is 36.

| arm | family | learner | status | ROC>0.5 | PR>chance | Std recall>0 | Bal recall>0 | Sec recall>0 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CHRONOLOGY | BOT | XGBOOST | INFERENTIAL_ELIGIBLE | 0/5 | 0/5 | 0/5 | 0/5 | 0/5 |
| CHRONOLOGY | BOT | LIGHTGBM | INFERENTIAL_ELIGIBLE | 5/5 | 5/5 | 0/5 | 0/5 | 0/5 |
| CHRONOLOGY | DDOS | XGBOOST | INFERENTIAL_ELIGIBLE | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 |
| CHRONOLOGY | DDOS | LIGHTGBM | INFERENTIAL_ELIGIBLE | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 |
| CHRONOLOGY | INFILTRATION | XGBOOST | DESCRIPTIVE_ONLY | 5/5 | 5/5 | 0/5 | 0/5 | 0/5 |
| CHRONOLOGY | INFILTRATION | LIGHTGBM | DESCRIPTIVE_ONLY | 5/5 | 5/5 | 0/5 | 0/5 | 0/5 |
| CHRONOLOGY | PORT_SCAN | XGBOOST | INFERENTIAL_ELIGIBLE | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 |
| CHRONOLOGY | PORT_SCAN | LIGHTGBM | INFERENTIAL_ELIGIBLE | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 |
| CHRONOLOGY | WEB_ATTACK | XGBOOST | INFERENTIAL_ELIGIBLE | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 |
| CHRONOLOGY | WEB_ATTACK | LIGHTGBM | INFERENTIAL_ELIGIBLE | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 |
| RANDOM_CONTROL | BOT | XGBOOST | INFERENTIAL_ELIGIBLE | 5/5 | 5/5 | 0/5 | 0/5 | 0/5 |
| RANDOM_CONTROL | BOT | LIGHTGBM | INFERENTIAL_ELIGIBLE | 5/5 | 5/5 | 0/5 | 0/5 | 0/5 |
| RANDOM_CONTROL | DDOS | XGBOOST | INFERENTIAL_ELIGIBLE | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 |
| RANDOM_CONTROL | DDOS | LIGHTGBM | INFERENTIAL_ELIGIBLE | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 |
| RANDOM_CONTROL | INFILTRATION | XGBOOST | DESCRIPTIVE_ONLY | 5/5 | 5/5 | 0/5 | 0/5 | 0/5 |
| RANDOM_CONTROL | INFILTRATION | LIGHTGBM | DESCRIPTIVE_ONLY | 5/5 | 5/5 | 0/5 | 0/5 | 0/5 |
| RANDOM_CONTROL | PORT_SCAN | XGBOOST | INFERENTIAL_ELIGIBLE | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 |
| RANDOM_CONTROL | PORT_SCAN | LIGHTGBM | INFERENTIAL_ELIGIBLE | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 |
| RANDOM_CONTROL | WEB_ATTACK | XGBOOST | INFERENTIAL_ELIGIBLE | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 |
| RANDOM_CONTROL | WEB_ATTACK | LIGHTGBM | INFERENTIAL_ELIGIBLE | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 |

Among inferentially eligible families, the families for which both learners
satisfied both preregistered ranking conditions in all five seeds under both
chronological LOAO and the random-LOAO control were: **DDOS, PORT_SCAN, WEB_ATTACK**.

BOT remained distinctly learner-dependent under chronological LOAO. The
frozen condition counts are preserved directly in the accompanying claim
registry rather than collapsed into a single family score.

## Random-split LOAO control versus chronological LOAO

The random control is not interpreted as a deployment-realistic estimate.
The comparison below reports **continuous paired contrasts only**, defined as
`random - chronological`. No post-result threshold was introduced to classify
a contrast as "large", "small", "collapse", or "survival".

The sign notation is `+N/-N/=N`, where `+` means the random-control value was
numerically greater than the chronological value for that frozen seed.

| family | learner | status | ΔROC | ΔROC sign | ΔPR-excess | ΔPR-excess sign | ΔStd-recall | ΔStd-recall sign |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BOT | XGBOOST | INFERENTIAL_ELIGIBLE | 0.5117 | +5/-0/=0 | 0.0158 | +5/-0/=0 | 0.0000 | +0/-0/=5 |
| BOT | LIGHTGBM | INFERENTIAL_ELIGIBLE | 0.3079 | +5/-0/=0 | 0.0242 | +5/-0/=0 | 0.0000 | +0/-0/=5 |
| DDOS | XGBOOST | INFERENTIAL_ELIGIBLE | -0.0337 | +0/-5/=0 | -0.0736 | +0/-5/=0 | 0.0041 | +5/-0/=0 |
| DDOS | LIGHTGBM | INFERENTIAL_ELIGIBLE | -0.0909 | +0/-5/=0 | -0.1429 | +0/-5/=0 | 0.4630 | +5/-0/=0 |
| INFILTRATION | XGBOOST | DESCRIPTIVE_ONLY | 0.0434 | +5/-0/=0 | 0.0002 | +5/-0/=0 | 0.0000 | +0/-0/=5 |
| INFILTRATION | LIGHTGBM | DESCRIPTIVE_ONLY | 0.2270 | +5/-0/=0 | 0.0019 | +5/-0/=0 | 0.0000 | +0/-0/=5 |
| PORT_SCAN | XGBOOST | INFERENTIAL_ELIGIBLE | 0.3176 | +5/-0/=0 | 0.2991 | +5/-0/=0 | 0.0003 | +5/-0/=0 |
| PORT_SCAN | LIGHTGBM | INFERENTIAL_ELIGIBLE | 0.1910 | +5/-0/=0 | 0.3800 | +5/-0/=0 | 0.0003 | +4/-1/=0 |
| WEB_ATTACK | XGBOOST | INFERENTIAL_ELIGIBLE | 0.0294 | +5/-0/=0 | 0.0140 | +4/-1/=0 | 0.3646 | +5/-0/=0 |
| WEB_ATTACK | LIGHTGBM | INFERENTIAL_ELIGIBLE | 0.0091 | +5/-0/=0 | -0.0653 | +0/-5/=0 | 0.7788 | +5/-0/=0 |

Accordingly, random-versus-chronological differences may be described as
**consistent with chronology compounding novelty difficulty** where the
numerical contrasts support that wording, but they do not establish temporal
drift as the sole causal explanation.

## Reproducibility and interpretation constraints

Training-seed uncertainty is reported separately from sampling/bootstrap
uncertainty. No best seed was selected. No synthetic seed-plus-bootstrap
confidence interval was created. No aggregate zero-day score was created:
family-specific LOAO outcomes remain primary.

Infiltration remains descriptive only because its positive support is 36
(<50). Random LOAO is a control rather than a deployment estimate. The final
Stage22 shared-holdout evaluation is a preregistered robustness re-evaluation
of the already historically opened Stage22R population and is not represented
as a new blind external holdout.

## Manuscript-safe conclusion

The five-seed analysis shows that the principal Stage22 validation-geometry
direction is highly stable to training-seed variation: chronological-natural
models exceeded random-natural models in both PR-AUC and ROC-AUC on the shared
final holdout for all five frozen seeds. In the unseen-family experiments,
however, robustness remains family- and learner-specific. Several families
retain stable ranking and operating-point detection across seeds, whereas BOT
shows marked learner dependence and Infiltration cannot support inferential
claims because of its small positive sample. The random-split LOAO control
provides a complementary benchmark for separating novelty difficulty from the
additional challenge associated with chronological evaluation, without
supporting a causal claim that chronology alone explains the observed
differences.
