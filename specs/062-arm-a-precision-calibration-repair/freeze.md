# Spec 062 — Freeze Record (Spec 028 Arm A: the Precision Computation, Calibration Repair; Successor to Spec 061)

> ## FROZEN — 2026-10-21
>
> This contract was frozen on 2026-10-21 under
> the owner's approval of the same date
> (amendment package Item 3: take Spec 062
> through freeze and OSF filing;
> `adjudication.md` §§5, 8). The AEE lifecycle
> hooks ran over the register first (register
> recovered to 0.6-draft;
> `aee/freeze-aee-note.md`), and the digest in
> `freeze.json` was then computed **exactly
> once** over the recovered register and the
> finalised freeze texts (the Spec 035 ordering).
> The freeze also files this spec's own OSF
> contract registration (DD-062-10;
> `osf-spec-registration.md`, completed by append
> after filing). Execution runs as **Phase-424**
> under this frozen contract, and only after the
> freeze has merged, the registration's approval
> act has completed — the parent's approval click
> on OSF's admin notification — and a separate
> execution order is given. At the freeze itself
> no trial has run, no calibration on the
> recorded population has run, and no target has
> been estimated.

## 1. Basis

The contract is the successor to Spec 061
(campaign member 18, design D-27, **arm A1
only**): a precision computation on Phase-393's
recorded resampling distribution for Spec 028's
Harappa-excluded Arm A, which stands
**INCONCLUSIVE** — median adjusted R²
0.00878393455594817, percentile interval
[0.004626892186724407, 0.01297407559730989]
straddling the family's 0.01 margin, rejection
share 0.6231155778894473, on 1,593 records at 5
sites. Spec 061 (Phase-423, executed 2026-10-21)
closed **CANNOT BE RUN AS WRITTEN** at its gate
0.5: its frozen calibration (candidate (b),
DD-061-13) applies the estimator to the
constructed population in expectation, so
within-site variation is exactly zero and the
calibration function is a step function —
A(1) = −0.0025188916876574316 exactly and
A(1.5) = A(2) = A(3) = 1.0 exactly — and no boost
in [1, 3] achieves |A(b) − θ| ≤ 1e-6 for either
scenario (defect DEF-062-1). This freeze repairs
exactly that definition and nothing else: the
precision question, both scenarios, the
composite pin, gates 0.1–0.4, the search frame,
the trial construction, the resolution and
target rules, and the outcome wordings are
carried from Spec 061 verbatim in substance;
the calibration is construction R-1 (spec
§4.7-R) and its gate is gate 0.5-R. Spec 061's
closed record is never patched. The computation
asks how much added non-Harappa material, of
the same kind, Arm A would need for its interval
to resolve at the 0.01 margin, under two stated
scenarios (true effect at the recorded point
estimate, resolving downward; true effect at
0.015, resolving upward). Its product is an
intake target. It establishes nothing about the
ancient world. Arm A2 — the decisive rerun — is
not in this spec (campaign decision E-3); Spec
061's operative target T* stays undefined on
Spec 061's record, and a successor target, if
one is ever returned, is this spec's own and
arms nothing by itself.

The freeze decided the draft's open points
(`adjudication.md` §8): **DD-062-7** (OP-062-1:
the calibration seed is 20261021, adopted
exactly as drafted — the calibration Generator
is a dedicated object, separate from both
per-scenario trial Generators); **DD-062-8**
(OP-062-2: Phase-424 allocated — verified
unallocated in the repo records at this freeze;
Phases 419–423 belong to Specs 057–061);
**DD-062-9** (OP-062-4: construction R-1 adopted
exactly as drafted — per-inscription Dirichlet
drawing around the imposed composition,
fixed-uniform coupling, κ_i = n_legible(i) − 1;
R-2, the verbatim redraw, is **not adopted** and
stays on the record as a non-adopted alternative
whose tolerance amendment is not taken; R-3 and
R-4 stand rejected on measurement);
**DD-062-10** (OP-062-3: the spec files its own
OSF contract registration at the freeze, under
campaign E-1); **DD-062-11** (OP-062-5: the
freeze and filing acts are taken under the
owner's approval; execution is a separate later
act, not authorised by the freeze); and
**DD-062-12** (the DD-038-10 AEE gate reading
adopted). DD-062-1 to DD-062-6 stand as drafted;
none is overturned.

## 2. Pin verification (two routes, at the freeze)

Every §2 pin was re-derived **in the
foreground** by two independent routes — the
contents-API raw route and the git-blob route —
both at the merged record (`main` at
`b7a8c8a42d4e1137c04ef4c0123fb4ba4dbc3736`), with
the merged working tree agreeing as a third
read. The routes agree byte-for-byte on every
file, and every recomputed hash equals its pin.
**The composite pin set carried from Spec 061
is complete: every component verifies.**

| Input | SHA-256 (both routes) | Bytes |
|---|---|---|
| `reports/phase393_results.json` | `0a1657a8af84615afbee95164cd1c10ea6fc5bc53d1b5a0a006b1862fa5ff607` | 19,753 |
| `backend/glossa_lab/data/yajnadevam_inscriptions.csv` | `c02e3d7bb74cf5abb11cc94f88d8d469e6acc5d6fad4b7153c02c43428f58d98` | 1,204,144 |
| `specs/028-harappa-robustness/pipeline393.py` | `6c2ff91c41bbb283a513127c6ab7157c1805b640ba0d846f9c7d3349ab8a7b0e` | 15,127 |
| `specs/028-harappa-robustness/margins-audit.json` | `15ae0281bb003f3b02742819349d3905004a282b28e9a2c00f433ac41c04bb6d` | 5,355 |
| `specs/028-harappa-robustness/freeze.json` | `376cd8e7ebc21ef7c31d43270607f475bb7e685cdcbe88205d7092e17fc526cc` | 4,212 |
| `backend/reports/INDUS_FINAL_ANCHORS.json` | `df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569` | 570,344 |

The facts the design rests on were re-read from
the pinned bytes in the same pass: the results
file's Arm A primary reads median adjusted R²
0.00878393455594817, interval
[0.004626892186724407, 0.01297407559730989],
rejection share 0.6231155778894473, 1,593
records, 294 inscriptions per draw, seed
20261012, R = 199, B = 499; the margins audit's
Arm A cells read Mohenjo-daro SEAL 1138 / TAB
164, Dholavira SEAL 96 / TAB 15, Lothal SEAL 72
/ TAB 2, Chanhu-daro SEAL 52 / TAB 2, Kalibangan
SEAL 49 / TAB 3 — 6 included cells at the frozen
49 threshold, 4 excluded TAB cells (15, 3, 2, 2);
the audit's Arm A positive-control sign sets
carry 10 signs per site, the sets the imposed
compositions of §4.7-R perturb toward. One
further record was read at the freeze (not a
step-0 pin): Spec 028's `calibration.json`
(SHA-256
`4198747b42121fea817db2e5ad82da10cca6118fef39bb14dc13cdf56ac204ff`,
2,404 bytes, both routes), whose Arm A positive
control at the frozen boost 3.0 returned median
adjusted R² 0.023963353007570576 over generated
worlds — the recorded quantity the repaired
calibration is levelled to (DD-062-5), and the
record Spec 061's outcome names as the repair
direction.
`backend/tests/test_spec062_freeze.py` pins all
of these facts so later drift fails loudly.

## 3. Machine record

`freeze.json` in this directory is the canonical
JSON record (framework026 `build_freeze`, computed
by `build_freeze.py` in this directory). Covered
sources (nothing else decides the question):

- `specs/062-arm-a-precision-calibration-repair/freeze.md` (this
  document)
- `specs/062-arm-a-precision-calibration-repair/spec.md`
- `specs/062-arm-a-precision-calibration-repair/claims.json`
- `specs/062-arm-a-precision-calibration-repair/adjudication.md`
- `specs/062-arm-a-precision-calibration-repair/aee/freeze-aee-note.md`
- `specs/062-arm-a-precision-calibration-repair/build_freeze.py`
- `backend/tests/test_spec062_freeze.py`

`tasks.md` is lifecycle bookkeeping and is not
digest-covered (the house rule since Spec 026:
plans change as work proceeds).
`osf-spec-registration.md` is the filing record
for DD-062-10: it is completed by append after
the filing exists, and the filing carries this
freeze's digest — so it cannot itself be a
digest-covered source.

## 4. What the freeze fixes

- **The claim and its fence** (spec §1 / F062-C01,
  C02, C15): the computation states only the
  intake target at which Arm A's interval would
  resolve at the 0.01 margin, under the two
  stated scenarios. No output states anything
  about the ancient world, and Spec 028's
  INCONCLUSIVE verdict stands unedited (F062-C05).
- **The predecessor fence** (spec header, §11 /
  F062-C05, C13): Spec 061's frozen record and
  its outcome stand exactly as executed; its T*
  stays undefined on its record; this spec is a
  successor contract in a new directory and
  patches nothing of Spec 061's.
- **The composite distribution pin** (spec §2 /
  F062-C06): identical to Spec 061's — summary
  plus the exact inputs and machinery that
  produced it; gate 0.3 requires its recorded
  summary to be reproduced exactly before any
  scaling, and the repair leaves gate 0.3's path
  untouched (spec §3, gate 0.3; F062-C07).
- **The step-0 gates** (spec §3 / F062-C06, C07,
  C08, C12): composite pin integrity (0.1),
  population reproduction (0.2), recorded-
  distribution reproduction (0.3), search frame
  present (0.4), and — replacing Spec 061's gate
  0.5 — construction calibration 0.5-R: per
  scenario, the bracket recomputes
  (A_R(1) < θ < A_R(3)), A_R is strictly
  increasing on the recorded 9-point scan grid,
  and the bisection achieves |A_R(b) − θ| ≤ 1e-6
  within 100 iterations. Each failure stops the
  run in its named class before any trial.
- **The repaired calibration** (spec §4.7-R /
  F062-C12; DD-062-9): construction R-1 — for
  each of 199 draws, every inscription's
  proportion row is a Dirichlet draw centred
  exactly on its site's imposed composition
  p_s(b), with κ_i = n_legible(i) − 1 so the
  row's per-column variance equals the frozen
  token drawing's multinomial proportion
  variance; draws are coupled across b by fixed
  uniforms (a dedicated calibration Generator,
  seed 20261021, DD-062-7) through the gamma
  quantile function, and the rarefaction
  selections are fixed before any b is
  evaluated, so A_R(b) is a deterministic
  continuous function of b; A_R is the median of
  the 199 draw statistics at the positive
  control's level (generated population, frozen
  rarefaction, adjusted R² per draw, permutations
  off). Bisection on [1, 3], tolerance 1e-6
  carried unchanged.
- **The search frame** (spec §4.7 / F062-C03,
  C12): carried from Spec 061 in full — integer
  grid m = 1…25; ceiling m = 25 (added total at
  ceiling 38,232; world total 39,825); 199 trials
  per point; 199 draws and 499 permutations per
  trial (the pipeline's frozen constants); seed
  20261021 with the stated stream discipline. At
  integer multiples the per-site added counts are
  exactly (m − 1) × the recorded site totals —
  proportional with no rounding.
- **The scenarios and the resolution rule**
  (spec §§4.2, 4.4 / F062-C09, C10): θ₁ =
  0.00878393455594817 resolving downward, θ₂ =
  0.015 resolving upward, margin 0.01, strict
  exclusion, a grid point qualifies at ≥ 80% of
  trials resolving.
- **The target rule and outcomes** (spec §§4.5,
  5 / F062-C03, C04, C11): the smallest
  qualifying total per scenario, the full grid
  table published either way, exactly one of
  the four pre-written headlines — including
  NO TARGET UNDER EITHER SCENARIO, the
  falsifier's outcome, frame-scoped as spec
  §7.4 states. The operative target rule is
  carried (the larger returned target; a single
  returned target operative with its scenario
  condition) as this spec's own; whether it
  arms A2 is the owner's mini-planning-gate
  decision under E-3, never this spec's act.
- **The simulation fence** (spec §§4.3, 6, 7 /
  F062-C09, C13, C14): every output labels the
  computation a simulation over recorded data;
  simulated additions are resamples, never held
  data or evidence; Arm A2's contingent status
  stands exactly as `adjudication.md` §4
  (DD-062-6) records it.

## 5. What the freeze does not do

- **It computes nothing.** No trial has run, no
  world has been built under this contract, no
  boost has been calibrated on the recorded
  population, and no target has been estimated
  or peeked at. Gate 0.5-R has not run: whether
  A_R brackets θ on the recorded population is
  an execution-time check. The computation is
  execution work under Phase-424, not a freeze
  act.
- **It does not patch Spec 061, re-run,
  re-adjudicate, or edit Arm A.** Spec 061's
  record and Spec 028's frozen records and
  INCONCLUSIVE verdict stand exactly as
  recorded.
- **It does not arm Arm A2.** A successor
  target, if one is ever returned, arms
  nothing by itself; arming is the owner's
  mini-planning-gate act under E-3.
- **It supplies no run-time discretion.** Every
  value gate 0.4 reads is in spec §4.7/§4.7-R
  and this record; gate 0.5-R verifies the
  frozen construction can impose each
  scenario's θ before any trial. Anything
  missing or failing closes the run in its
  named class — nothing is repaired at run
  time, and no other construction may be
  supplied.
- **Execution has not begun and is not
  authorised by the freeze alone.** Execution
  (Phase-424) awaits the freeze merge, the OSF
  registration's approval act, and a separate
  execution order (DD-062-11).

## 6. Able-to-fail proof (the freeze tests)

The freeze tests in
`backend/tests/test_spec062_freeze.py` were
proven able to fail at the freeze act, before
the digest was relied on: with the assembled
freeze in place, the register file in the
working tree was mutated in exactly one place
(its `register_version` string, `0.6-draft` →
`0.6-MUTATED`) and the suite was run — the
freeze-replay test and the register-integrity
test went red, as they must, because a covered
source no longer matched its frozen hash and
the register no longer carried its frozen
version. The file was then restored
byte-identically (its SHA-256 re-verified
against the value recorded in `freeze.json`'s
sources) and the full freeze suite was run
again green. The mutation touched no committed
byte; the frozen record replays exactly over
the restored tree.

## 7. OSF registration and the execution gate

Under DD-062-10 (campaign E-1), this freeze
files the spec's own OSF contract registration
carrying the frozen contract — freeze digest,
execution Phase-424, the falsifier, the
composite pin and gate 0.3's exact-reproduction
standard with its fencing argument, the two
scenarios and the strict-exclusion resolution
rule, the complete frozen search frame (integer
grid to the m = 25 ceiling, 199 trials per
point, 199 draws and 499 permutations per trial,
seed 20261021), the repaired calibration
(construction R-1 with its dedicated
calibration Generator, seed 20261021, verified
at gate 0.5-R), the carried operative-target
rule, the predecessor fence (Spec 061's record
unpatched, its T* undefined), and the simulation
fence: added inscriptions are resamples of
recorded inscriptions, never data the program
holds. The filing record is
`osf-spec-registration.md`, completed by append
after filing. The registration stands **pending
approval** after filing; its approval act is
the parent's approval click on OSF's
admin-notification email, and no mail is
handled by this freeze. Execution (Phase-424)
does not begin while the registration stands
pending: it awaits that approval act and a
separate execution order.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
