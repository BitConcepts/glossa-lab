# Phase-423 — Spec 061: Spec 028 Arm A, the Precision Computation (D-27, arm A1)

**SIMULATION OVER RECORDED DATA.** This computation is a simulation over recorded data — Phase-393's recorded resampling distribution and the recorded site samples. Its added inscriptions are resamples of recorded inscriptions; they are not new data, and no part of this record describes them as data the program holds.

**Outcome: CANNOT BE RUN AS WRITTEN**

The precision computation did not run: gate 0.5 failed (scenario 1: bisection did not reach |A(b) - theta| <= 1e-06 within 100 iterations), and those values may not be supplied at run time. No target quantity was computed.

Both scenario values: theta_1 = 0.00878393455594817 (the recorded point estimate, stated as 0.00878 in the design; resolves downward) and theta_2 = 0.015 (resolves upward); the margin is adjusted R^2 0.01.

Frozen search frame in full: integer grid m = 1..25 (step 1); ceiling m = 25 (added total 38,232; world total 39,825); 199 trials per grid point; 199 draws and 499 permutations per trial; simulation seed 20261021; effect imposition by candidate (b), the frozen positive-control construction with the boost calibrated per scenario on [1, 3] to tolerance 1e-6 (gate 0.5).

This computation measures the resolution of a recorded test. It establishes nothing about the ancient world.
