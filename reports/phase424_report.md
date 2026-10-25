# Phase-424 — Spec 062: Spec 028 Arm A, the Precision Computation, Calibration Repair (D-27, arm A1)

**SIMULATION OVER RECORDED DATA.** This computation is a simulation over recorded data — Phase-393's recorded resampling distribution and the recorded site samples. Its added inscriptions are resamples of recorded inscriptions; they are not new data, and no part of this record describes them as data the program holds.

**Outcome: NO TARGET UNDER EITHER SCENARIO**

From Phase-393's recorded resampling distribution, the precision computation returns **no intake target that resolves Arm A at the 0.01 margin under either stated scenario**, within the frozen search frame (grid integer multiples m = 1..25; ceiling m = 25; 199 trials per point). The grid table is published with this record so the near misses are visible. Spec 028 Arm A stands INCONCLUSIVE with no computed intake target; the contingent rerun (Arm A2) has no target to arm on, and its trigger (section 6 of the adjudication) does not fire on this record.

Both scenario values: theta_1 = 0.00878393455594817 (the recorded point estimate, stated as 0.00878 in the design; resolves downward) and theta_2 = 0.015 (resolves upward); the margin is adjusted R^2 0.01.

## Step 0 gates

- Gate 0.1: PASS
- Gate 0.2: PASS
- Gate 0.3: PASS
- Gate 0.4: PASS
- Gate 0.5-R: PASS

## Grid — scenario_1 (theta = 0.00878393455594817; boost b = 1.8665771484375, A_R(b) = 0.008783112877008503)

| m | Added total | Share resolving | Binomial SD | Qualifies |
|---|---|---|---|---|
| 1 | 0 | 0.0804 | 0.0193 | no |
| 2 | 1593 | 0.0101 | 0.0071 | no |
| 3 | 3186 | 0.0000 | 0.0000 | no |
| 4 | 4779 | 0.0000 | 0.0000 | no |
| 5 | 6372 | 0.0000 | 0.0000 | no |
| 6 | 7965 | 0.0000 | 0.0000 | no |
| 7 | 9558 | 0.0000 | 0.0000 | no |
| 8 | 11151 | 0.0000 | 0.0000 | no |
| 9 | 12744 | 0.0000 | 0.0000 | no |
| 10 | 14337 | 0.0000 | 0.0000 | no |
| 11 | 15930 | 0.0000 | 0.0000 | no |
| 12 | 17523 | 0.0000 | 0.0000 | no |
| 13 | 19116 | 0.0000 | 0.0000 | no |
| 14 | 20709 | 0.0000 | 0.0000 | no |
| 15 | 22302 | 0.0000 | 0.0000 | no |
| 16 | 23895 | 0.0000 | 0.0000 | no |
| 17 | 25488 | 0.0000 | 0.0000 | no |
| 18 | 27081 | 0.0000 | 0.0000 | no |
| 19 | 28674 | 0.0000 | 0.0000 | no |
| 20 | 30267 | 0.0000 | 0.0000 | no |
| 21 | 31860 | 0.0000 | 0.0000 | no |
| 22 | 33453 | 0.0000 | 0.0000 | no |
| 23 | 35046 | 0.0000 | 0.0000 | no |
| 24 | 36639 | 0.0000 | 0.0000 | no |
| 25 | 38232 | 0.0050 | 0.0050 | no |

Target: NO TARGET (within the frozen search frame).

## Grid — scenario_2 (theta = 0.015; boost b = 2.2470703125, A_R(b) = 0.015000016834981533)

| m | Added total | Share resolving | Binomial SD | Qualifies |
|---|---|---|---|---|
| 1 | 0 | 0.1759 | 0.0270 | no |
| 2 | 1593 | 0.0201 | 0.0099 | no |
| 3 | 3186 | 0.0352 | 0.0131 | no |
| 4 | 4779 | 0.1005 | 0.0213 | no |
| 5 | 6372 | 0.0302 | 0.0121 | no |
| 6 | 7965 | 0.0553 | 0.0162 | no |
| 7 | 9558 | 0.0251 | 0.0111 | no |
| 8 | 11151 | 0.0151 | 0.0086 | no |
| 9 | 12744 | 0.0201 | 0.0099 | no |
| 10 | 14337 | 0.0050 | 0.0050 | no |
| 11 | 15930 | 0.0101 | 0.0071 | no |
| 12 | 17523 | 0.0050 | 0.0050 | no |
| 13 | 19116 | 0.0000 | 0.0000 | no |
| 14 | 20709 | 0.0000 | 0.0000 | no |
| 15 | 22302 | 0.0050 | 0.0050 | no |
| 16 | 23895 | 0.0000 | 0.0000 | no |
| 17 | 25488 | 0.0000 | 0.0000 | no |
| 18 | 27081 | 0.0000 | 0.0000 | no |
| 19 | 28674 | 0.0000 | 0.0000 | no |
| 20 | 30267 | 0.0050 | 0.0050 | no |
| 21 | 31860 | 0.0050 | 0.0050 | no |
| 22 | 33453 | 0.0251 | 0.0111 | no |
| 23 | 35046 | 0.0101 | 0.0071 | no |
| 24 | 36639 | 0.0050 | 0.0050 | no |
| 25 | 38232 | 0.0000 | 0.0000 | no |

Target: NO TARGET (within the frozen search frame).

Frozen search frame in full: integer grid m = 1..25 (step 1); ceiling m = 25 (added total 38,232; world total 39,825); 199 trials per grid point; 199 draws and 499 trial, seed 20261021; effect imposition by candidate (b)'s imposed compositions with the boost calibrated per scenario under construction R-1 (per-inscription Dirichlet drawing, fixed uniforms, calibration seed 20261021) on [1, 3] to tolerance 1e-6 (gate 0.5-R).

This computation measures the resolution of a recorded test. It establishes nothing about the ancient world.
