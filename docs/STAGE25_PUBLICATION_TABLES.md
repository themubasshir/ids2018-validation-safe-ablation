# Stage25 Publication Tables

## Table 25-I — STANDARD Operating Point: Benchmark to 0.1% Deployment Stress

| Evaluation cell | Observed F1 | Observed precision | TPR | FPR | PPV @ 0.1% | FP/day | TP/day | Hours/day |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Stage22 Random | 0.9839 | 0.9998 | 0.9685 | 0.000035 | 0.9656 | 34.6 | 969.4 | 33.5 |
| Stage22 Chronological | 0.0001 | 0.0606 | 0.0000 | 0.000058 | 0.0006 | 58.3 | 0.0 | 1.9 |
| IDS2018→CICIDS2017 B62 Published | 0.3463 | 0.9271 | 0.2129 | 0.004106 | 0.0493 | 4106.3 | 213.1 | 144.0 |
| IDS2018→CICIDS2017 B62 Corrected | 0.3463 | 0.9271 | 0.2129 | 0.004106 | 0.0493 | 4106.3 | 213.1 | 144.0 |
| IDS2018→CICIDS2017 B70 Published | 0.3668 | 0.9402 | 0.2278 | 0.003553 | 0.0603 | 3553.3 | 228.1 | 126.0 |
| IDS2018→CICIDS2017 B70 Corrected | 0.2502 | 0.9092 | 0.1450 | 0.003556 | 0.0392 | 3555.5 | 145.2 | 123.4 |
| CICIDS2017→IDS2018 B62 | 0.0008 | 0.0293 | 0.0004 | 0.001498 | 0.0003 | 1497.6 | 0.4 | 49.9 |
| CICIDS2017→IDS2018 B70 | 0.0008 | 0.0326 | 0.0004 | 0.001340 | 0.0003 | 1339.5 | 0.4 | 44.7 |

The complete 24-operating-point version is stored in
`table25_2_all_operating_points_0p1pct.csv`.

## Table 25-II — Exact Cost Break-Even Coverage

All 24 exact analytic cost break-even points are stored in
`table25_3_exact_cost_break_even.csv`.

Family ranges:

| Family | Minimum break-even | Maximum break-even |
| --- | ---: | ---: |
| Stage22 Random | 0.000036% | 0.006923% |
| Stage22 Chronological | 1.783102% | 7.757369% |
| IDS2018→CICIDS2017 | 0.015593% | 0.035144% |
| CICIDS2017→IDS2018 | 2.195650% | 3.739456% |

## Table 25-III — Governance and Sanity

All seven preregistered sanity tests passed. No Stage25 model fitting,
model inference, probability-array generation, target reopening,
threshold search, or calibration was performed.
