# Stage25 Final Scientific Synthesis

**Status: CLOSED AND SEALED**

Final synthesis SHA256:

`befa5e6b2ec893d0892963f34e16dbbb622ecf630c6b46b33421e1ca45a723a7`

Publication manifest SHA256:

`0fd825da7326841268fc6dc6f8bf135377bec77f1fef8ea261cdb0f7bb6585cf`

## Completion

- Stage25-0 protocol lock: PASS
- Stage25-1 Bayesian projection: PASS
- Stage25-2 traffic/SOC capacity projection: PASS
- Stage25-3 exact break-even analysis: PASS
- Stage25-4 benchmark→operational translation: PASS
- preregistered figures: 5/5 complete
- preregistered sanity tests: 7/7 PASS
- publication package: COMPLETE
- notebook/script export: COMPLETE

## Scientific Accounting

- new model fits: 0
- new model inference: 0
- new probability arrays: 0
- target reopenings: 0
- threshold searches: 0
- calibration runs: 0

## Central Result

Stage25 shows that deployment interpretation changes materially under rare
attack prevalence even when each empirical operating point is frozen.
Very low FPR is required to preserve positive-alert precision, SOC
capacity and detection usefulness must be evaluated separately, and the
Stage24 bidirectional transfer asymmetry persists in deployment-facing
PPV and workload projections.

At 0.1% attack prevalence, the Stage22 random STANDARD operating point
projects PPV 0.965572 with
34.6 FP/day and
969.4 TP/day, but still requires
33.5
analyst-hours/day.

The Stage22 chronological STANDARD operating point projects PPV
0.000551068 and only
0.0322 TP/day, demonstrating that low
workload may reflect detection collapse rather than operational success.

IDS2018→CICIDS2017 STANDARD PPV at 0.1% ranges from
0.039233 to 0.060313;
CICIDS2017→IDS2018 STANDARD PPV ranges only from
0.000257610 to 0.000287993.

Under the frozen relative-cost ratio C_FP:C_FN=1:100, 15/24 operating
points favor the model at 0.1% prevalence but only 3/24 at 0.01%.

## Final Governance Rule

**Stage25 must not be scientifically reopened.**

No further Stage25 fitting, inference, target opening, threshold tuning,
calibration, assumption modification, or result-dependent figure
selection is authorized.
