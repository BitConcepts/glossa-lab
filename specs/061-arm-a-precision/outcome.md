# Spec 061 / Phase-423 — Outcome record (EXECUTED 2026-10-21 — CANNOT BE RUN AS WRITTEN, gate 0.5)

> ## EXECUTED — 2026-10-21
>
> Executed under the frozen Spec 061 contract
> (freeze digest
> `41b1785cf7176a17e1cc8a9982fedcc913a32bfd66735cf13111ab29ba2a39f1`),
> as **Phase-423**, in Wave 3 Group 2 of the
> runnable-experiments campaign (plan approved
> AS WRITTEN on 2026-10-21; member 18, design
> D-27 arm A1 only). The execution gate was
> satisfied before the run: OSF registration
> **fza8c** is APPROVED + PUBLIC, DOI
> 10.17605/OSF.IO/FZA8C. Outcome: **CANNOT BE
> RUN AS WRITTEN** — gate 0.5 (construction
> calibration, added at the freeze by
> DD-061-13/DD-061-15) failed on recomputed
> values. Gates 0.1–0.4 passed, gate 0.3 with
> the recorded Arm A summary reproduced
> exactly. No trial ran, no world was built,
> and no target quantity was computed. Arm A2
> did not join this pass (campaign decision
> E-3) and nothing in this record arms it.

## Headline (spec §5.1 CANNOT BE RUN AS WRITTEN form, gate 0.5 substance per spec §3)

"The precision computation did not run: gate
0.5 (construction calibration) failed. Per
scenario, the frozen §4.7 calibration requires
bisection on the bracket [1, 3] to achieve
|A(b) − θ| ≤ 1e-6, where A(b) is the frozen
estimator on the constructed population in
expectation. Recomputed on the pinned record,
A(1) = −0.0025188916876574316 — the frozen
record's own value, 1 − 1592/1588 — and
A(b) = 1.0 exactly at every b > 1 evaluated
(b = 1.5, 2.0, 3.0). A takes no value between
−0.0025188916876574316 and 1.0, so no boost in
the bracket brings A(b) within 1e-6 of either
scenario's θ (θ₁ = 0.00878393455594817;
θ₂ = 0.015), and the bisection for Scenario 1
did not reach the tolerance within 100
iterations. The construction cannot impose
the scenario's θ, and no other construction
may be supplied at run time. No target
quantity was computed. Spec 028 Arm A stands
exactly as recorded: INCONCLUSIVE, median
adjusted R² 0.00878393455594817, interval
[0.004626892186724407, 0.01297407559730989],
rejection share 0.6231155778894473."

**Why A(b) is a step function (the mechanism,
in plain words).** The calibration applies the
frozen PERMANOVA estimator to a population in
which every inscription at a site carries that
site's *expected* composition — the same
proportion vector for every inscription at the
site. An estimator of site differences can
only see two kinds of variation: variation
inside a site and variation between sites. In
the constructed population the inside-a-site
variation is exactly zero, because the
expectation step has already averaged it away:
every inscription at a site is identical. So
all of the variation the estimator sees is
between sites, and its adjusted R² is 1.0 —
perfect separation — at any boost above 1,
however small. At b = 1 exactly, every site
shares the pooled composition, every distance
is zero, and the estimator returns its null
offset, −0.0025188916876574316. There is no
boost in between, because there is no
in-between state of the constructed
population. The recorded Spec 028 positive
control at the same boost 3.0 returned a
median adjusted R² of 0.023963353007570576 —
but that is a different quantity: a median
over *generated* worlds, where each
inscription's tokens are actually drawn from
its site's composition, inscription by
inscription. The drawing is what creates
inside-a-site variation, and that variation is
what holds the measured effect down to an
intermediate value. The frozen calibration
definition — the estimator applied to the
population *in expectation* — removes exactly
the variation that makes intermediate effects
possible. Gate 0.5, added at the freeze to
verify the calibration before any trial,
caught this on recomputed values; that is
what the gate is for. Nothing was repaired at
run time, no substitute construction was
supplied, and no trial ran on an uncalibrated
world.

## 1. What was executed

Step 0 only (spec §3, gates in frozen order),
under the graph-first build (H15/H23):
experiment script
`backend/scripts/phase423_arm_a_precision.py`;
graph module
`backend/glossa_lab/experiment_graph_phase423.py`
(node `IndusPhase423ArmAPrecision`); registration
in `backend/glossa_lab/experiment_graph.py`;
the registration verified by import in the run
environment before the run (the node is present
in `ATOMIC_NODES`). The script imports the
pinned machinery itself
(`specs/028-harappa-robustness/pipeline393.py`,
pin-verified under gate 0.1) rather than a
copy, and builds the population by Spec 028's
frozen `build_margins_audit` flow on the
pinned store inputs (hashes asserted by that
machinery: `bbfdbcd5…` and `c368f290…`, both
recomputed at this run and matching).

The run of record executed on the owner's
desktop (TRISTEN-DESKTOP, WSL2) under the
program's standing practice for heavy
computation, in an environment matching the
freeze record (Python 3.12.3, NumPy 2.5.3);
the executed script is byte-identical to the
script committed on this branch (SHA-256
`693d4955…`, verified on the executing machine
against the committed file). Gate 0.3's exact
reproduction on that machine (§2) is the
identity proof of the run: the frozen
machinery, in that environment, reproduces
the recorded distribution digit-for-digit. The
run's base was `main` at
`3200b7b5b6841a7b9567a81368bf84004fd17255`
(the dispatch base), on branch
`spec-061-a1-precision`. The run's own
records: `reports/phase423_results.json`
(SHA-256
`f7007009e1d3c4beb0705ec6e4e737ce3bf1c38025c5910c7e871e422034ba57`)
and `reports/phase423_report.md` (SHA-256
`3669eb38512af1e3c24374fb178666b315911d5ae6c7274f40f8b86d4ea3ea80`)
— produced by the executing run on the
desktop, transferred back through the relay
repository, and verified byte-identical by
SHA-256 against the executing machine's
copies at both ends of the transfer.

Development disclosure: an earlier draft of
the script, run in the local VM during
development, exposed a floating-point residue
defect in the calibration's first form
(per-row renormalisation of the expected count
vectors left last-bit differences between
inscriptions at a site, so at b = 1 the
estimator divided one rounding residue by
another). The committed script takes the
expected proportion rows as the site
composition itself — exactly the frozen
definition's value in real arithmetic — under
which A(1) recomputes to the frozen record's
−0.0025188916876574316 exactly. That
development run is not the execution of
record; the execution of record is the
desktop run of the committed script, and its
gate sequence is §2 below.

## 2. Step 0, gate by gate

- **0.1 Composite pin integrity — PASS.**
  Every spec §2 input recomputes to its
  freeze-record value in the executing tree:
  Phase-393 results `0a1657a8…`, corpus layer
  `c02e3d7b…`, pipeline `6c2ff91c…`, margins
  audit `15ae0281…`, Spec 028 freeze record
  `376cd8e7…`, and the anchors file
  `df0cf620…`.
- **0.2 Population reproduction — PASS.**
  The frozen population flow, re-run on the
  pinned inputs, reproduces the recorded Arm A
  population exactly: 1,593 records at the
  five sites (Mohenjo-daro 1,302; Dholavira
  111; Lothal 74; Chanhu-daro 54; Kalibangan
  52), the margins audit's cell table, 6
  included cells, 294 inscriptions per draw.
- **0.3 Recorded-distribution reproduction —
  PASS, exact.** The frozen Arm A primary,
  re-run under the recorded machinery and
  seed (20261012; R = 199; B = 499),
  reproduces the recorded summary
  digit-for-digit: median adjusted R²
  **0.00878393455594817**, interval
  **[0.004626892186724407,
  0.01297407559730989]**, rejection share
  **0.6231155778894473**. (The gate passes
  only on exact equality of all three
  quantities; the recomputed values are
  therefore the recorded values, digit for
  digit.)
- **0.4 Search frame present — PASS.** The
  freeze record (digest verified,
  `41b1785c…`) states the full frame of spec
  §4.7: integer grid m = 1…25, ceiling
  m = 25, 199 trials per point, 199 draws and
  499 permutations per trial (the pipeline's
  frozen constants), simulation seed
  20261021, and the candidate (b)
  effect-imposition construction
  (DD-061-13).
- **0.5 Construction calibration — FAIL (the
  execution closes here).** Per scenario, the
  bracket recomputes in form — A(1) =
  −0.0025188916876574316 < θ and A(3) = 1.0 >
  θ for both scenario values — but the
  bisection cannot achieve |A(b) − θ| ≤ 1e-6
  within 100 iterations, for the reason the
  headline states: A(b) = 1.0 exactly at
  every b > 1 evaluated (b = 1.5, 2.0, 3.0;
  at each, the frozen estimator's between-site
  sum of squares equals its total sum of
  squares exactly, because the constructed
  population's expected proportion rows are
  constant within each site). The run closed
  at Scenario 1's bisection, the first
  calibration the gate reaches; Scenario 2's
  calibration was not separately attempted,
  and none was needed to close the gate: the
  function A(b) is the same for both
  scenarios (θ enters only as the bisection's
  target), and its step shape puts θ₂ = 0.015
  equally out of reach. The frozen
  consequence applies: the construction
  cannot impose a scenario's θ, and no other
  construction may be supplied at run time —
  the run stops as **CANNOT BE RUN AS
  WRITTEN**. No trial ran; the m = 1 grid
  point was not computed; no interval at
  scale exists.

## 3. What this outcome does and does not establish

It establishes that Spec 061 cannot be run as
written: its frozen calibration (DD-061-13)
defines A(b) as the frozen estimator applied
to the constructed population in expectation,
and that function — recomputed here from the
pinned record — takes only the two values
−0.0025188916876574316 (at b = 1) and 1.0 (at
every b > 1), so it cannot be calibrated to
either stated scenario. The defect is in the
freeze's calibration definition, surfaced by
the freeze's own gate 0.5 before any trial;
it is not a finding about the trial machinery
(gate 0.3 reproduced the recorded
distribution exactly), not a finding about
Phase-393's record (which stands exactly as
recorded, re-verified here), and not a
finding about Spec 028's positive control:
its recorded median at boost 3.0
(0.023963353007570576) is a median over
generated worlds and was never A(3); the
freeze cited it as bracket evidence, and
this record corrects that reading — A(3)
recomputes to 1.0. It does **not** establish
that no calibration of candidate (b) could
ever impose θ: a calibration defined over
generated worlds (for example, targeting the
median of the frozen estimator over
regenerated populations, the quantity the
positive control actually reports) is a
different definition, and adopting one is an
amendment act under a new planning gate —
never a run-time substitution inside this
frozen contract. No intake target exists
under this spec; the operative target T* of
DD-061-5 is **undefined** on this record, so
Arm A2's trigger cannot fire on it, and no
later act may quote a target from this
record. This computation measures the
resolution of a recorded test. It establishes
nothing about the ancient world.

## 4. Claim consequences (governed register)

Executed under register 0.7-draft (frozen);
one line per claim, F061-C01…C15.

- **F061-C01** (an outcome states only the
  intake target at which Arm A's interval
  would resolve): HELD in its closure branch
  — this record states no intake target,
  because none was computed; it records a
  runnability closure only, in the frozen
  outcome class.
- **F061-C02** (STUDY-SPEC-028/ARM-A stands
  INCONCLUSIVE on its recorded numbers):
  CHECKED — the recorded numbers were
  re-verified first-hand at gates 0.1–0.3 and
  reproduced exactly at gate 0.3; the claim
  stands as recorded.
- **F061-C03** (within the frozen frame, the
  computation returns a smallest target
  resolving Arm A under at least one
  scenario): NOT REACHED — gate 0.5 closed
  the run before any trial; the hypothesis is
  unjudged, neither supported nor falsified.
  No target was returned, and this record
  does not convert the closure into the
  falsifier's outcome (see F061-C04).
- **F061-C04** (no target under either
  scenario inside the frame is recorded as
  NO TARGET UNDER EITHER SCENARIO): HELD in
  its distinguishing branch — that headline
  is **not** recorded, because it is an
  outcome *after all gates pass* (spec §9);
  this run closed at a gate, in the distinct
  pre-written class CANNOT BE RUN AS
  WRITTEN, and the two are not
  interchangeable.
- **F061-C05** (Spec 061 is a precision
  computation beside the frozen Arm A test):
  HELD — Arm A was not re-run,
  re-adjudicated, or edited; its INCONCLUSIVE
  verdict stands exactly as recorded.
- **F061-C06** (execution stops before any
  precision quantity if any composite-pin
  component mismatches): HELD vacuously —
  gate 0.1 passed on every component; the
  stop that fired was gate 0.5's, under
  F061-C12.
- **F061-C07** (gate 0.3 reproduces the
  recorded distribution summary exactly):
  CHECKED, PASS — median, interval, and
  rejection share reproduced digit-for-digit
  (§2).
- **F061-C08** (the Arm A population
  reproduces exactly before any precision
  quantity): CHECKED, PASS — 1,593 records,
  the five site totals, the cell table, 6
  included cells, 294 per draw (§2).
- **F061-C09** (the computation runs exactly
  two scenarios): HELD in its closure
  branch — no scenario was computed; gate
  0.5's calibration was attempted for
  Scenario 1 and closed the run, and no
  third scenario or other θ value was
  computed at any point.
- **F061-C10** (trial resolution is strict
  exclusion of the 0.01 margin): NOT REACHED
  — no trial ran, so no interval was judged;
  the rule was neither applied nor varied.
- **F061-C11** (each scenario's target is
  the smallest added total at a qualifying
  grid point): NOT REACHED — no grid point
  was computed and no target exists.
- **F061-C12** (the computation searches
  only the frame the freeze fixes): HELD —
  FIRED as written: when the frozen frame's
  own calibration could not impose θ, the
  run stopped in the frame's named class
  rather than searching outside it or
  supplying a construction at run time.
- **F061-C13** (every output labels the
  computation a simulation over recorded
  data): HELD — the results JSON and the
  Phase-423 report both carry the simulation
  label in their first fields, and this
  record's headline repeats it: added
  inscriptions in this design are resamples,
  and none were generated.
- **F061-C14** (Arm A2 is not part of Spec
  061): HELD — A2 was not designed, armed, or
  executed; with no target returned, T* is
  undefined on this record and its trigger
  does not fire (§3).
- **F061-C15** (no outcome establishes Arm
  A's rerun verdict in advance): HELD — no
  verdict, target, or resolution quantity
  exists in any product of this execution.

**Anchors.** `backend/reports/INDUS_FINAL_ANCHORS.json`
recomputed before and after the run: SHA-256
`df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569`
at both points — byte-identical, asserted.

## 5. Records

- Machine records: `reports/phase423_results.json`;
  report: `reports/phase423_report.md`
  (digests in §1).
- Graph node: `IndusPhase423ArmAPrecision`
  (registered and verified by import before
  the run; the node serves the committed
  results and does not recompute on call —
  the frozen computation is a multi-day
  checkpointed run, and this closure is now
  its terminal record in any case).
- Root LEDGER entry: "Spec 061 EXECUTED
  (Phase-423)" entry added with this record.
- Tasks: E1 (graph-first build), E2 (step 0,
  gates 0.1–0.2), and E3 (gates 0.3–0.4,
  with gate 0.5's closure recorded there)
  stand ticked in `tasks.md`; E4 (the
  computation) stands open in form and is
  closed in substance by this record — it
  cannot run under this frozen contract,
  because its calibration gate fails on the
  frozen definition itself; E5 is this
  record. Any successor calibration is a
  new act under a new freeze or an
  amendment, never a repair inside this one.
- `adjudication.md`, `spec.md`, `claims.json`,
  `freeze.md`, and `freeze.json` were **not**
  edited: they are digest-covered sources of
  the freeze (`test_spec061_freeze.py`
  enforces the pins), and the executed-spec
  form records execution here, in
  `outcome.md`.
- Local-environment disclosure: in this VM's
  existing glossa-lab venv, the freeze tests'
  `test_register_integrity` fails with a
  TypeError from the venv's AEE loader version
  (the conftest's `strict` keyword). The
  failure was verified to occur identically
  on the pristine `main` tree at the run's
  base (`3200b7b5`) with no execution changes
  present — it pre-exists this execution, the
  frozen files are byte-identical to `main`,
  and the remaining freeze and graph tests
  pass locally (50 passed, 1 skipped). The
  PR's CI run is the figure of record.
- CI and foundation check (H21) at the record
  merge: appended below after the record PR
  merges, in the house completion pattern —
  this section is completed by append, not
  edited.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*

---

## Landing record — 2026-10-21 (appended at merge; append-only)

- Execution PR: **#286** (branch
  `spec-061-a1-precision`), merged to `main`
  as merge commit
  **`abdcac190d79edb75078649b82309df505843b93`**.
- CI: GitHub Actions run **39648236254** on the
  PR head `95afda56` — **7 of 7 jobs success**,
  verified from the run's own job conclusions
  (Backend tests (pytest); Frontend tests
  (Playwright); Indus public validation checks;
  Evidence Graph script smoke tests; Shell
  wrappers ubuntu / macos / windows). The road
  to that run is recorded plainly: the PR's
  first check run was lost to a GitHub Actions
  event-delivery stall that also left sibling
  campaign PRs (287, 290) without runs for a
  time — an absent run, not a failing one
  (campaign plan Part 7) — and while the stall
  lasted, `main` advanced through the other
  Group 2 merges until the PR stood conflicted
  ("dirty": LEDGER.md appends and
  experiment-graph registrations). The branch
  was merged up to the then-current `main`
  (merge commit `95afda56`; both conflicts
  resolved by keeping every entry and every
  registration — the resolved LEDGER carries
  all 166 of main's section headers plus this
  spec's one, and the resolved graph file
  registers every phase node, Phase-423's
  included, verified by import), and the
  genuine run above then completed on the
  merged head before the PR merged.
- Run digests re-verified on `main` at the
  merge commit by two routes (the working
  tree and the contents API):
  `reports/phase423_results.json`
  `f7007009e1d3c4beb0705ec6e4e737ce3bf1c38025c5910c7e871e422034ba57`,
  `reports/phase423_report.md`
  `3669eb38512af1e3c24374fb178666b315911d5ae6c7274f40f8b86d4ea3ea80`
  — identical to the values in §1 of this
  record.
- Foundation check (H21) at the merge
  commit, on a fresh checkout of `abdcac19`
  in the prepared foundation clone (Holdat
  corpus CSV SHA-256
  `62d14d2bebf7c2c80d98a2958e75ec52bff3f5e85d1f7f40cbe28218e`
  verified first): **40 checks passed, 0
  failed, 8 warnings** — the standing figure.
- Terminal outcome stands as recorded above:
  **CANNOT BE RUN AS WRITTEN** at gate 0.5.
  No target was computed; the operative
  target T* is undefined on this record and
  Arm A2's trigger does not fire on it. Spec
  028 Arm A stands INCONCLUSIVE exactly as
  recorded.

*AI disclosure: appended by an AI agent (Muse Spark, via Muse) at the direction of
Tristen Pierson, per constitution §VI.*
