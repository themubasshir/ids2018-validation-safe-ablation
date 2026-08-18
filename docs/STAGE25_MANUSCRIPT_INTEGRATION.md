# Stage25 Manuscript Integration

## Stage25 Results — Prevalence and Operational Stress

Stage25 translated the already-frozen Stage22 and Stage24 operating
characteristics into deployment-stress quantities without model refitting,
new inference, target reopening, threshold re-selection, or calibration.
Twenty-four frozen operating points were evaluated across six
preregistered attack prevalences (10%, 3%, 1%, 0.3%, 0.1%, and 0.01%),
yielding 144 deterministic prior-shift projections.

At the preregistered 0.1% attack prevalence, the Stage22 random-natural
STANDARD operating point retained a PPV of
0.965572 despite the large reduction from its
observed prevalence of 0.136847. Its very
low FPR (0.00003457) produced only
34.6 false alerts per one million
benign flows/day, while the frozen TPR (0.968458)
projected 969.4 true alerts/day.
Nevertheless, the combined workload was
33.5
analyst-hours/day under the preregistered two-minute service-time
assumption. Thus, high PPV did not by itself imply low SOC workload.

The random-natural SECURITY operating point exposed the complementary
failure mode. Although its frozen recall increased to
0.984701, its FPR of
0.006817 generated
6817.1 false alerts/day at 0.1%
prevalence. PPV fell to 0.126325 and projected
workload rose to
260.1
hours/day. The result shows why a security-oriented recall objective does
not automatically satisfy a deployment-scale false-positive constraint.

Temporal validation produced a qualitatively different picture. The
Stage22 chronological STANDARD operating point fit easily within the
assumed analyst-capacity envelope, but only because its frozen TPR was
0.00003213. At 0.1% prevalence it projected
only 0.0322 true detections/day against
58.3 false alerts/day, yielding PPV
0.000551068. Capacity feasibility therefore cannot
be interpreted as evidence of operational usefulness when detection has
collapsed.

The cross-dataset direction retained the Stage24 asymmetry. For
IDS2018→CICIDS2017 STANDARD operating points, projected PPV at 0.1%
ranged from 0.039233 to
0.060313, while projected workload ranged from
123.4 to
144.0 analyst-hours/day. For the corresponding
BALANCED operating points, PPV ranged from
0.027685 to 0.034418 and
workload from 426.9 to
538.7 hours/day. Hence substantial ranking
signal in the primary transfer direction did not translate into a
low-volume alert stream under the frozen deployment scenario.

The reverse CICIDS2017→IDS2018 direction remained operationally collapsed.
Its STANDARD projected PPV was only
0.000257610–0.000287993 at
0.1% prevalence. Across all reverse-transfer frozen operating points,
projected true detections ranged only from 0.3859 to
1.3506 per day under the fixed one-million-benign-flow
scenario. This extends the Stage24 directional asymmetry from ranking
metrics to deployment-facing quantities.

The relative-cost analysis further demonstrated the importance of the
base rate. Under the preregistered relative cost ratio
C_FP:C_FN = 1:100, 15 of 24 operating points had lower projected model
cost than the simplified ignore reference at 0.1% prevalence, whereas
only 3 of 24 remained lower-cost at 0.01%. The latter three were the
Stage22 random-natural operating points; the chronological and both
cross-dataset families favored the simplified ignore reference at that
extreme prevalence. These are relative operational cost units, not
financial-loss estimates.

Across Stage25, all seven preregistered sanity tests passed, all five
preregistered figures were retained, and no result-dependent figure,
threshold, prevalence point, capacity tier, traffic assumption, or cost
ratio was changed.

## Stage25 Discussion

Stage25 separates two mechanisms that are frequently conflated in IDS
evaluation. Stage22 and Stage24 demonstrate that temporal and domain
shift can alter the class-conditional operating characteristics
themselves, including TPR and FPR. Stage25 instead holds each frozen
operating point fixed and changes only the attack prior. The resulting
PPV cliffs therefore quantify base-rate sensitivity conditional on the
empirically observed operating point; they do not claim that TPR and FPR
would remain invariant in a real future network.

The projections show that very low FPR is the dominant prerequisite for
maintaining useful PPV when attacks are rare. This is visible even for
the strongest random-natural operating points: a threshold with high
recall but an FPR in the order of 10^-3 to 10^-2 can generate thousands
of false alerts per million benign flows and sharply reduce PPV. The
operational consequence is stronger than a benchmark F1 or ROC-oriented
summary alone suggests.

SOC capacity introduces a second distinction. An operating point may
have high PPV and still exceed a small analyst team because true alerts
also require service. Conversely, an operating point may fit comfortably
within capacity because it detects almost no attacks. Therefore,
capacity feasibility and detection usefulness are separate requirements,
and neither should be inferred from the other.

The Stage24 cross-dataset asymmetry remains visible after operational
translation. IDS2018→CICIDS2017 retained materially greater detection
utility than CICIDS2017→IDS2018, yet its frozen FPR still produced a heavy
false-alert workload at low prevalence. The reverse direction combined
weak TPR with non-negligible FPR, creating the least favorable
deployment-facing profile. This reinforces the need for bidirectional
cross-dataset testing rather than a single portability result.

Finally, the exact PPV and relative-cost break-even calculations provide
interpretable operating boundaries rather than grid-dependent graphical
approximations. They identify the prior-prevalence regimes in which a
frozen operating point changes character under the stated assumptions.
They should be read as conditional decision-analysis tools rather than
claims of universal deployment suitability.

## Stage25 Limitations and Threats to Validity

Stage25 is an analytic deployment-stress audit, not empirical production
validation. The primary assumption is prior-probability shift: within
each frozen operating point, TPR and FPR are held constant while attack
prevalence changes. Real networks may also exhibit covariate, concept,
protocol, topology, user-behavior, attacker, and extractor shift, all of
which can alter TPR and FPR.

The traffic scenario fixes benign volume at one million flows/day. This
is a transparent reference scale rather than a claim that one million
benign flows represents every enterprise. Likewise, two minutes per
alert and analyst tiers of one, three, and ten analyst-days are
preregistered reference scenarios rather than universal SOC constants.

The relative cost model uses C_FP=1 and C_FN=100 in dimensionless
relative operational cost units. These values are not currency, are not
financial-loss estimates, and do not imply that each malicious flow is
an independent compromise or breach. The simplified ignore comparator
is intentionally limited.

Stage25 projections are deterministic conditional transformations of
frozen empirical estimates. No complete joint TPR/FPR sampling
distribution was available for every inherited operating point, so
uncertainty in those empirical rates was not propagated through the
deployment projections and no new bootstrap was introduced.

The source datasets remain benchmark traffic captures rather than live
production SOC telemetry. Their age, traffic generation, attack mix,
feature-extractor semantics, and class structure constrain external
validity. Stage24 additionally could not evaluate the preregistered
GROUNDED_S4 cells because exact durable physical membership could not be
recovered without introducing a new heuristic; Stage25 correctly does
not manufacture a substitute for those cancelled cells.

No target-specific or prevalence-specific threshold optimization was
performed. Consequently, Stage25 evaluates the deployment implications
of the frozen validation-selected operating points, not the best
threshold that could be obtained after observing a deployment target.

## Stage25 Contributions

Stage25 contributes a validation-safe operational translation layer for
intrusion-detection evaluation. First, it converts frozen TPR/FPR
operating points into exact Bayesian PPV/NPV projections across a
predeclared low-prevalence grid without reopening targets or retuning
thresholds. Second, it translates the same operating points into
false-alert volume, true-alert volume, analyst workload, and explicit
SOC-capacity exceedance under a reproducible reference scenario. Third,
it derives analytic PPV, required-FPR, and relative-cost break-even
boundaries rather than relying on visually selected grid crossings.
Fourth, it links random, chronological, and bidirectional cross-dataset
results in one audit trail, showing how base-rate stress and
temporal/domain shift produce distinct but interacting deployment risks.
Finally, every assumption, operating point, figure, sanity test, and
artifact is preregistered or hash-frozen, preserving the study's
validation-safe governance through publication closeout.
