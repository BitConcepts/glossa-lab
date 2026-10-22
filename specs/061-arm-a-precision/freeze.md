# Spec 061 — Freeze Record (Spec 028 Arm A: the Precision Computation; Design D-27, Arm A1 Only)

> ## FROZEN — 2026-10-21
>
> This contract was frozen on 2026-10-21 under
> the runnable-experiments campaign plan
> approved by the owner as written on 2026-10-21
> (the campaign's Wave 2 freeze wave;
> `adjudication.md` §§1, 9). The AEE lifecycle
> hooks ran over the register first (register
> recovered to 0.7-draft;
> `aee/freeze-aee-note.md`), and the digest in
> `freeze.json` was then computed **exactly
> once** over the recovered register and the
> finalised freeze texts (the Spec 035 ordering).
> The freeze also files this spec's own OSF
> contract registration (DD-061-14;
> `osf-spec-registration.md`, completed by append
> after filing). Execution runs as **Phase-423**
> under this frozen contract, and only after the
> freeze has merged, the registration's approval
> act has completed — the parent's approval click
> on OSF's admin notification — and a separate
> execution order is given. At the freeze itself
> no trial has run, no interval at scale has been
> computed, and no target has been estimated.

## 1. Basis

The contract implements design D-27, **arm A1
only** (campaign member 18): a precision
computation on Phase-393's recorded resampling
distribution for Spec 028's Harappa-excluded
Arm A, which stands **INCONCLUSIVE** — median
adjusted R² 0.00878393455594817, percentile
interval [0.004626892186724407,
0.01297407559730989] straddling the family's
0.01 margin, rejection share 0.6231155778894473,
on 1,593 records at 5 sites. The computation
asks how much added non-Harappa material, of
the same kind, Arm A would need for its
interval to resolve at the 0.01 margin, under
two stated scenarios (true effect at the
recorded point estimate, resolving downward;
true effect at 0.015, resolving upward). Its
product is an intake target. It establishes
nothing about the ancient world. Arm A2 — the
decisive rerun — is not in this pass (campaign
decision E-3); its trigger is recorded in
`adjudication.md` §6 and claim F061-C14 exactly
as drafted (DD-061-5 confirmed, §2 below).

The freeze decided the draft's open points
(`adjudication.md` §9): **DD-061-8** (DEF-061-1:
the composite resampling-distribution pin is
confirmed as the remedy — summary file plus
corpus, pipeline, margins audit, and Spec 028
freeze record, every pin re-verified by two
independent routes at this freeze, with gate
0.3's exact-reproduction standard standing);
**DD-061-9** (OP-061-1: the multiplier grid is
the integer multiples m = 1, 2, …, 25, step 1 —
the design's own word is "multiples", and at
integer multiples the per-site distribution of
DD-061-3 is exact in integers, so no rounding
rule is needed or supplied); **DD-061-10**
(OP-061-2: the search ceiling is m = 25, the
smallest multiple at which every recorded
site×type cell reaches the frozen 49-member
inclusion threshold — the binding cells are
the two 2-record TAB cells, reaching 50 — so at
the ceiling the frozen draw design reaches its
maximum size, 10 cells × 49 = 490 inscriptions
per draw, and no larger multiple changes which
cells the machinery includes or how many
inscriptions a draw contains); **DD-061-11**
(OP-061-3: 199 trials per grid point — the
frozen replication count of the machinery
itself — with draws and permutations per trial
inherited from the frozen design, 199 and 499;
the binomial standard deviation of a grid
point's resolution share at the 0.80
qualification threshold is 0.0284 and is
reported beside every share); **DD-061-12**
(OP-061-4: the simulation seed is 20261021, a
fresh seed fixed in this record, following the
Spec 053 freeze-date-seed precedent, with the
RNG stream discipline stated in spec §4.7);
**DD-061-13** (OP-061-5: the
effect-imposition construction is candidate
(b) — each site's composition is the pooled
composition perturbed toward its
site-specific components **in the frozen
positive-control manner** (the margins audit's
pinned per-site sign sets, multiplied by a
boost factor and renormalised, exactly as
`build_calibration.py` constructs the frozen
positive control), with the boost calibrated
per scenario so the frozen estimator applied
to the constructed population in expectation
returns the scenario's θ; candidates (a) and
(c) are not adopted, for the reasons recorded
in `adjudication.md` §9); **DD-061-14**
(OP-061-6: the spec files its own OSF contract
registration at the freeze, under campaign
E-1); **DD-061-15** (OP-061-7: calibration of
the imposed worlds is required in three
mechanical forms — gate 0.3's exact
reproduction at the recorded scale, the
DD-061-13 calibration verification recorded
per scenario before any trial (new gate 0.5),
and the m = 1 grid point computed and
published like every other point); **DD-061-16**
(Phase-423 allocated — verified unallocated in
the repo records at this freeze; the campaign
tracker assigns Phases 419–422 to Specs
057–060); and **DD-061-17** (the DD-038-10 AEE
gate reading adopted). DD-061-1 to DD-061-7
stand as drafted; **DD-061-2** (strict
exclusion), **DD-061-3** (proportional
per-site distribution), and **DD-061-5** (the
operative target is the larger returned
target) are **confirmed** at the freeze, as
§5 of the draft adjudication asked.

## 2. Pin verification (two routes, at the freeze)

Every §2 pin was re-derived **in the
foreground** by two independent routes — the
contents-API raw route and the git-blob route —
both at the merged record (`main` at
`a3509525fab64e22a4c053d7bbed14c7083a14d3`).
The two routes agree byte-for-byte on every
file, and every recomputed hash equals its pin.
**The DEF-061-1 composite pin set is complete:
all five components verify.**

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
49 threshold, 4 excluded TAB cells (15, 3, 2, 2),
which is the record DD-061-10's ceiling derives
from; the audit's Arm A positive-control sign
sets carry 10 signs per site, the sets
DD-061-13's construction perturbs toward. One
further record was read at the freeze (not a
step-0 pin): Spec 028's `calibration.json`
(SHA-256
`4198747b42121fea817db2e5ad82da10cca6118fef39bb14dc13cdf56ac204ff`,
2,404 bytes, both routes), whose Arm A positive
control at the frozen boost 3.0 returned median
adjusted R² 0.023963353007570576 — above both
scenario values, which is the recorded evidence
that DD-061-13's calibration bracket [1, 3]
reaches θ₂ = 0.015.
`backend/tests/test_spec061_freeze.py` pins all
of these facts so later drift fails loudly.

## 3. Machine record

`freeze.json` in this directory is the canonical
JSON record (framework026 `build_freeze`, computed
by `build_freeze.py` in this directory). Covered
sources (nothing else decides the question):

- `specs/061-arm-a-precision/freeze.md` (this
  document)
- `specs/061-arm-a-precision/spec.md`
- `specs/061-arm-a-precision/claims.json`
- `specs/061-arm-a-precision/adjudication.md`
- `specs/061-arm-a-precision/aee/freeze-aee-note.md`
- `specs/061-arm-a-precision/build_freeze.py`
- `backend/tests/test_spec061_freeze.py`

`tasks.md` is lifecycle bookkeeping and is not
digest-covered (the house rule since Spec 026:
plans change as work proceeds).
`osf-spec-registration.md` is the filing record
for DD-061-14: it is completed by append after
the filing exists, and the filing carries this
freeze's digest — so it cannot itself be a
digest-covered source.

## 4. What the freeze fixes

- **The claim and its fence** (spec §1 / F061-C01,
  C02, C15): the computation states only the
  intake target at which Arm A's interval would
  resolve at the 0.01 margin, under the two
  stated scenarios. No output states anything
  about the ancient world, and Spec 028's
  INCONCLUSIVE verdict stands unedited (F061-C05).
- **The composite distribution pin** (spec §§2,
  2.1 / F061-C06; DD-061-1, DD-061-8): the
  recorded distribution is pinned as summary
  plus the exact inputs and machinery that
  produced it; gate 0.3 requires its recorded
  summary to be reproduced exactly before any
  scaling. DEF-061-1 is remedied in this form
  and in no other.
- **The step-0 gates** (spec §3 / F061-C06, C07,
  C08, C12): composite pin integrity (0.1),
  population reproduction (0.2), recorded-
  distribution reproduction (0.3), search frame
  present (0.4), and — added at this freeze —
  construction calibration (0.5, DD-061-13/15).
  Each failure stops the run in its named class
  before any trial.
- **The search frame** (spec §4.7 / F061-C03, C12;
  DD-061-9…DD-061-13): integer grid m = 1…25;
  ceiling m = 25 (added total at ceiling
  38,232; world total 39,825); 199 trials per
  point; 199 draws and 499 permutations per
  trial (the pipeline's frozen constants);
  seed 20261021 with the stated stream
  discipline; effect imposition by the frozen
  positive-control construction with the boost
  calibrated per scenario to the frozen
  estimator's value on the constructed
  population in expectation (bracket [1, 3],
  tolerance 1e-6, achieved boost and effect
  recorded). At integer multiples the per-site
  added counts are exactly (m − 1) × the
  recorded site totals — proportional
  (DD-061-3) with no rounding.
- **The scenarios and the resolution rule**
  (spec §§4.2, 4.4 / F061-C09, C10): θ₁ =
  0.00878393455594817 resolving downward, θ₂ =
  0.015 resolving upward, margin 0.01, strict
  exclusion (DD-061-2 confirmed), a grid point
  qualifies at ≥ 80% of trials resolving.
- **The target rule and outcomes** (spec §§4.5,
  5 / F061-C03, C04, C11): the smallest
  qualifying total per scenario, the full grid
  table published either way, exactly one of
  the four pre-written headlines — including
  NO TARGET UNDER EITHER SCENARIO, the
  falsifier's outcome, frame-scoped as spec
  §7.4 states. The operative trigger target
  T* follows DD-061-5 as confirmed.
- **The simulation fence** (spec §§4.3, 6, 7 /
  F061-C13): every output labels the computation
  a simulation over recorded data; simulated
  additions are resamples, never held data or
  evidence; Arm A2's trigger and consequence
  stand exactly as `adjudication.md` §6 records
  them (F061-C14).

## 5. What the freeze does not do

- **It computes nothing.** No trial has run, no
  world has been built, no boost has been
  calibrated, no interval at scale exists, and
  no target has been estimated or peeked at.
  The computation is execution work under
  Phase-423, not a freeze act.
- **It does not re-run, re-adjudicate, or edit
  Arm A.** Spec 028's frozen records and its
  INCONCLUSIVE verdict stand exactly as
  recorded; a returned target appends beside
  the claim, never over it.
- **It does not arm Arm A2.** The trigger
  definition is recorded; a fired trigger
  queues a mini planning gate under E-3 and
  joins nothing automatically.
- **It supplies no run-time discretion.** Every
  value gate 0.4 reads is in spec §4.7 and this
  record; gate 0.5 verifies the construction
  can impose each scenario's θ before any
  trial. Anything missing or failing closes
  the run in its named class — nothing is
  repaired at run time.
- **Execution has not begun and is not
  authorised by the freeze alone.** Execution
  (Phase-423) awaits the freeze merge, the OSF
  registration's approval act, and a separate
  execution order, in campaign Wave 3 group 2.

## 6. Able-to-fail proof (the freeze tests)

The freeze tests in
`backend/tests/test_spec061_freeze.py` were
proven able to fail at the freeze act, before
the digest was relied on: with the assembled
freeze in place, the register file in the
working tree was mutated in exactly one place
(its `register_version` string, `0.7-draft` →
`0.7-MUTATED`) and the suite was run — the
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

Under DD-061-14 (campaign E-1), this freeze
files the spec's own OSF contract registration
carrying the frozen contract — freeze digest,
execution Phase-423, the falsifier, the
composite pin and gate 0.3's exact-reproduction
standard, the two scenarios and the strict-
exclusion resolution rule, the complete frozen
search frame (integer grid to the m = 25
ceiling, 199 trials per point, 199 draws and
499 permutations per trial, seed 20261021), the
effect-imposition construction (the frozen
positive-control manner with the boost
calibrated per scenario, gate 0.5), the
operative-target rule DD-061-5, and the
simulation fence: added inscriptions are
resamples of recorded inscriptions, never data
the program holds. The filing record is
`osf-spec-registration.md`, completed by append
after filing. The registration stands **pending
approval** after filing; its approval act is
the parent's approval click on OSF's
admin-notification email, and no mail is
handled by this freeze. Execution (Phase-423)
does not begin while the registration stands
pending: it awaits that approval act and a
separate execution order.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
