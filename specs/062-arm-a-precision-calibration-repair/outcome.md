# Spec 062 / Phase-424 — Outcome record (EXECUTED 2026-10-25 — NO TARGET UNDER EITHER SCENARIO)

> ## EXECUTED — 2026-10-25
>
> Executed under the frozen Spec 062 contract
> (freeze digest
> `1800de5337503d7c596642ae48d1dc2465809c653901fa6efe1ade781957f488`),
> as **Phase-424**, the successor to Spec 061
> (Phase-423, closed CANNOT BE RUN AS WRITTEN
> at its gate 0.5). The execution gate was
> satisfied before the run: OSF registration
> **4m27t** is APPROVED + PUBLIC, DOI
> 10.17605/OSF.IO/4M27T. Step 0 passed every
> gate, including the repaired gate 0.5-R:
> construction R-1 calibrates on the real
> recorded population at both venues (this VM
> and the owner's desktop, byte-identical
> calibration records). The full grid then ran
> on the owner's desktop (TRISTEN-DESKTOP,
> WSL2) as two detached, checkpointed
> processes, launched 2026-10-22T09:24:18Z and
> complete — all 25 checkpoints per scenario,
> both processes exited cleanly — by
> 2026-10-25. Outcome: **NO TARGET UNDER
> EITHER SCENARIO** — no grid point inside the
> frozen search frame qualified under either
> stated scenario. This is the falsifier's
> outcome (§1.2 / §5), scoped to the frozen
> search frame: it means no grid point inside
> the frame qualified, never that no amount of
> data could resolve Arm A in principle. Arm
> A2 was never armed, joined, or touched
> (campaign decision E-3); with no target
> returned, its trigger does not fire on this
> record, and nothing in this record arms it.

## Headline (spec §5.1 NEITHER form, carried from Spec 061 §5.1)

"From Phase-393's recorded resampling
distribution, the precision computation returns
**no intake target that resolves Arm A at the
0.01 margin under either stated scenario**,
within the frozen search frame (grid integer
multiples m = 1..25; ceiling m = 25; 199 trials
per point). The grid table is published with
this record so the near misses are visible.
Spec 028 Arm A stands INCONCLUSIVE with no
computed intake target; the contingent rerun
(Arm A2) has no target to arm on, and its
trigger (§6 of the adjudication) does not fire
on this record."

**The decisive quantities, in plain words.**
A grid point qualifies only if at least 80% of
its 199 trials resolve — the interval excludes
the 0.01 margin, strictly, in the scenario's
direction. No point came close. The highest
resolving share anywhere in the grid is at the
smallest scale, m = 1 (no added inscriptions):
0.0804 under Scenario 1 (16 of 199 trials) and
0.1759 under Scenario 2 (35 of 199). The next
highest is Scenario 2 at m = 4, 0.1005 (20 of
199). Every other point is at or below 0.0553,
and long runs of the grid — Scenario 1 from
m = 3 to m = 24 apart from a single trial at
m = 25 — resolve in zero trials. Adding
simulated inscriptions inside this frame did
not move the interval toward excluding the
margin; the resolving share is highest before
any are added and falls from there. The frozen
binomial standard deviation beside the 0.80
threshold is 0.0284 (DD-061-11, carried), so
these are not near misses at the bar: the best
point in the grid sits more than twenty of
those standard deviations below it under
Scenario 1 and more than twenty below it under
Scenario 2 as well. This computation measures
the resolution of a recorded test. It
establishes nothing about the ancient world.

## 1. What was executed

The computation (spec §4), after step 0 (§2
below), under the graph-first build (H15/H23):
experiment script
`backend/scripts/phase424_arm_a_precision_calibration_repair.py`
(SHA-256
`26d6da01831d6679b7f60bfb9a0eaa25bdd6fbf31feb326f82d0dd19c59d5483`);
graph module
`backend/glossa_lab/experiment_graph_phase424.py`
(node `IndusPhase424ArmAPrecisionRepair`);
registration in
`backend/glossa_lab/experiment_graph.py`,
verified by import in the run environment
before the run (the node is present in
`ATOMIC_NODES`). The script imports the pinned
machinery itself
(`specs/028-harappa-robustness/pipeline393.py`,
pin-verified under gate 0.1) rather than a
copy, and builds the population by Spec 028's
frozen `build_margins_audit` flow on the
pinned store inputs (hashes asserted by that
machinery: `bbfdbcd5…` and `c368f290…`, both
recomputed at this run and matching).

Step 0 ran twice — once in this VM and once on
the owner's desktop — with byte-identical
calibration records (the desktop calibration
cache SHA-256 `2b7fa7e9…` equals the VM's), and
a third time as the `--assemble` step's gate
re-run on the desktop on 2026-10-25, again
digit-for-digit. The computation's identity is
therefore proven across venues: the same
script (SHA-256 above, read back from the
executing machine), the same pinned machinery,
and gate 0.3's exact reproduction (§2) at both
venues.

The grid itself ran on the owner's desktop
because the frozen frame is a multi-day
checkpointed computation (9,950 trials of the
frozen machinery; measured ≈2.6 s per draw
with permutations on this VM, and per-point
runtimes of ≈3,900–23,600 s on the desktop).
It launched 2026-10-22T09:24:18Z as two
detached processes — one per scenario, the
only stream-preserving parallelisation (each
scenario consumes its own Generator, seeded
20261021, in ascending grid order): Scenario 1
pid 956047 (log `~/p424-scen1.log`), Scenario 2
pid 956048 (log `~/p424-scen2.log`),
checkpointing after every grid point to
`~/glossa-lab-424/.glossa-state/phase424/scenario{1,2}/m{01..25}.json`
(+ `.state.pkl`), resume-exact. Environment of
record: Python 3.12.3, NumPy 2.5.3, SciPy
1.18.1 — matching the freeze record. The
completion watch verified the terminal state
first-hand on 2026-10-25: all m01–m25
checkpoints present for both scenarios, both
processes exited, both logs ending at m = 25
with no error. The `--assemble` step then ran
on the desktop (its step-0 re-run PASS, above)
and wrote the run's records:
`reports/phase424_results.json` (SHA-256
`cb144835117a6991dbb64b730b6ecc931993a518e2efd592348061400232d44b`)
and `reports/phase424_report.md` (SHA-256
`245b868d0ebb2dd3c6f123241d0acbd81c192102f17135401563f24e0f432b9c`)
— transferred back through the relay and
verified byte-identical by SHA-256 against the
executing machine's copies at both ends of the
transfer.

The build was secured to origin before the run
on branch `spec-062-execution` (head
`a847aa46`, via the git-data API: exactly the
four intended paths against its base). Because
`main` advanced substantially while the grid
ran, the execution record lands on current
`main` by a fresh branch carrying the same four
paths' contents — the script and the graph
module byte-identical to the executed build,
the `experiment_graph.py` registration applied
as the identical 10-line delta onto current
`main`'s file (never wholesale) — plus the
products of the run. Nothing executed differs
from what lands.

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
  seed, reproduces the recorded summary
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
  `1800de53…`) states the full frame of spec
  §4.7: integer grid m = 1…25, ceiling
  m = 25, 199 trials per point, 199 draws and
  499 permutations per trial (the pipeline's
  frozen constants), simulation seed
  20261021, and construction R-1 as the
  calibration of candidate (b) (DD-062-9).
- **0.5-R Construction calibration
  (repaired) — PASS.** On the pinned record,
  A_R is strictly increasing on the whole
  scan grid (A_R(1) =
  0.00022759124836990718, A_R(3) =
  0.028821884413380183; the full nine-point
  scan is in the results JSON), bracketing
  both scenario values, and bisection on
  [1, 3] reaches the 1e-6 tolerance for both:
  Scenario 1 b* = 1.8665771484375
  (|A_R(b*) − θ₁| = 8.216789396664481e-07,
  14 iterations); Scenario 2 b* =
  2.2470703125 (|A_R(b*) − θ₂| =
  1.6834981533819793e-08, 11 iterations).
  **The R-1 repair calibrates — Spec 061's
  step-function defect does not recur.** The
  calibration record reproduced digit-for-
  digit at both venues and again at assembly.

## 3. The grid (spec §4.5 — every point, both scenarios)

Frozen frame: integer multiples m = 1…25;
added total at m is (m − 1) × 1,593; ceiling
m = 25 (added total 38,232; world total
39,825); 199 trials per point; a point
qualifies at a resolving share ≥ 0.80 (the
binomial standard deviation at that threshold
is 0.0284). Per-point binomial SDs for every
share are in `reports/phase424_results.json`
and `reports/phase424_report.md`.

**Scenario 1** (θ₁ = 0.00878393455594817,
downward; boost b* = 1.8665771484375):

| m | Added | Share | Resolving |
|---|---|---|---|
| 1 | 0 | 0.0804 | 16/199 |
| 2 | 1,593 | 0.0101 | 2/199 |
| 3 | 3,186 | 0.0000 | 0/199 |
| 4 | 4,779 | 0.0000 | 0/199 |
| 5 | 6,372 | 0.0000 | 0/199 |
| 6 | 7,965 | 0.0000 | 0/199 |
| 7 | 9,558 | 0.0000 | 0/199 |
| 8 | 11,151 | 0.0000 | 0/199 |
| 9 | 12,744 | 0.0000 | 0/199 |
| 10 | 14,337 | 0.0000 | 0/199 |
| 11 | 15,930 | 0.0000 | 0/199 |
| 12 | 17,523 | 0.0000 | 0/199 |
| 13 | 19,116 | 0.0000 | 0/199 |
| 14 | 20,709 | 0.0000 | 0/199 |
| 15 | 22,302 | 0.0000 | 0/199 |
| 16 | 23,895 | 0.0000 | 0/199 |
| 17 | 25,488 | 0.0000 | 0/199 |
| 18 | 27,081 | 0.0000 | 0/199 |
| 19 | 28,674 | 0.0000 | 0/199 |
| 20 | 30,267 | 0.0000 | 0/199 |
| 21 | 31,860 | 0.0000 | 0/199 |
| 22 | 33,453 | 0.0000 | 0/199 |
| 23 | 35,046 | 0.0000 | 0/199 |
| 24 | 36,639 | 0.0000 | 0/199 |
| 25 | 38,232 | 0.0050 | 1/199 |

Target: **NO TARGET (within the frozen search
frame).**

**Scenario 2** (θ₂ = 0.015, upward; boost
b* = 2.2470703125):

| m | Added | Share | Resolving |
|---|---|---|---|
| 1 | 0 | 0.1759 | 35/199 |
| 2 | 1,593 | 0.0201 | 4/199 |
| 3 | 3,186 | 0.0352 | 7/199 |
| 4 | 4,779 | 0.1005 | 20/199 |
| 5 | 6,372 | 0.0302 | 6/199 |
| 6 | 7,965 | 0.0553 | 11/199 |
| 7 | 9,558 | 0.0251 | 5/199 |
| 8 | 11,151 | 0.0151 | 3/199 |
| 9 | 12,744 | 0.0201 | 4/199 |
| 10 | 14,337 | 0.0050 | 1/199 |
| 11 | 15,930 | 0.0101 | 2/199 |
| 12 | 17,523 | 0.0050 | 1/199 |
| 13 | 19,116 | 0.0000 | 0/199 |
| 14 | 20,709 | 0.0000 | 0/199 |
| 15 | 22,302 | 0.0050 | 1/199 |
| 16 | 23,895 | 0.0000 | 0/199 |
| 17 | 25,488 | 0.0000 | 0/199 |
| 18 | 27,081 | 0.0000 | 0/199 |
| 19 | 28,674 | 0.0000 | 0/199 |
| 20 | 30,267 | 0.0050 | 1/199 |
| 21 | 31,860 | 0.0050 | 1/199 |
| 22 | 33,453 | 0.0251 | 5/199 |
| 23 | 35,046 | 0.0101 | 2/199 |
| 24 | 36,639 | 0.0050 | 1/199 |
| 25 | 38,232 | 0.0000 | 0/199 |

Target: **NO TARGET (within the frozen search
frame).**

No operative target exists under this spec
(the DD-061-5 rule, carried: with no returned
target there is nothing to take the larger
of), and Spec 061's T* remains undefined on
Spec 061's record regardless of anything this
spec returns (§4 below).

## 4. What this outcome does and does not establish

It establishes that, inside the frozen search
frame — simulated worlds built by resampling
the recorded site samples at up to 25 times
their current size, with the scenario effects
imposed by the repaired calibration — no
amount of added inscriptions in the frame
makes Spec 028 Arm A's interval resolve at the
0.01 margin in at least 80% of trials, under
either stated scenario. The computation ran in
full: every gate passed, both scenarios
computed at all 25 grid points, all 9,950
trials. It also establishes that the repaired
calibration itself works as frozen: gate 0.5-R
passed on the real recorded population at two
venues with identical numbers, where Spec
061's frozen calibration could not impose
either θ at all — the repair Spec 062 was
written to test is confirmed as a piece of
machinery, and the question it was repaired to
answer is now answered: **no target**.

It does **not** establish that no amount of
data could resolve Arm A in principle: "no
target" is scoped to the frozen search frame
(§4.5), exactly as pre-written. It does not
establish anything about the ancient world —
not about site-linked repertoire structure,
not about movement of people, not about any
sign meaning (§7.1). It does not edit,
supersede, or re-adjudicate Spec 028 Arm A's
INCONCLUSIVE verdict, which stands exactly as
recorded (§7.2). It returns no intake target,
so no operative target exists under this spec
either; separately, Spec 061's T* remains
undefined on Spec 061's record. And because
Arm A2 was never armed — it is contingent,
trigger-armed, and no target exists for its
trigger to fire on — **nothing about Arm A2
may be claimed from this record**: no A2
quantity was computed, no A2 verdict exists,
and the contingent rerun has no target to arm
on. This computation measures the resolution
of a recorded test. It establishes nothing
about the ancient world.

## 5. Claim consequences (governed register)

Executed under register 0.6-draft (frozen);
one line per claim, F062-C01…C15.

- **F062-C01** (an outcome states only the
  intake target at which Arm A's interval
  would resolve): HELD in its no-target
  branch — this record states no intake
  target, because none was returned; it
  records the pre-written no-target outcome
  within the frozen frame, and no statement
  outside the intake-target scope.
- **F062-C02** (STUDY-SPEC-028/ARM-A stands
  INCONCLUSIVE on its recorded numbers):
  CHECKED — the recorded numbers were
  re-verified first-hand at gates 0.1–0.3 and
  reproduced exactly at gate 0.3; the claim
  stands as recorded.
- **F062-C03** (within the frozen frame, the
  computation returns a smallest target
  resolving Arm A under at least one
  scenario): NOT SUPPORTED — the full frame
  ran and no grid point qualified under
  either scenario (§3); this is the claim's
  falsifier branch, recorded as the §5
  headline NO TARGET UNDER EITHER SCENARIO,
  scoped to the frozen frame and to nothing
  beyond it.
- **F062-C04** (no target under either
  scenario inside the frame is recorded as
  NO TARGET UNDER EITHER SCENARIO): HELD —
  FIRED as written: that headline is this
  record's headline, with the same prominence
  as any target returned, and the full grid
  table is published with it (§3) so the near
  misses are visible.
- **F062-C05** (Spec 062 is a precision
  computation beside the frozen Arm A test):
  HELD — Arm A was not re-run,
  re-adjudicated, or edited; its INCONCLUSIVE
  verdict stands exactly as recorded.
- **F062-C06** (execution stops before any
  precision quantity if any composite-pin
  component mismatches): HELD vacuously —
  gate 0.1 passed on every component; no stop
  fired, and the grid ran only after all
  gates passed.
- **F062-C07** (gate 0.3 reproduces the
  recorded distribution summary exactly):
  CHECKED, PASS — median, interval, and
  rejection share reproduced digit-for-digit
  (§2), at both venues and again at assembly.
- **F062-C08** (the Arm A population
  reproduces exactly before any precision
  quantity): CHECKED, PASS — 1,593 records,
  the five site totals, the cell table, 6
  included cells, 294 per draw (§2).
- **F062-C09** (the computation runs exactly
  two scenarios): HELD — exactly the two
  stated scenarios were computed (θ₁ downward,
  θ₂ upward; no third scenario, no other θ),
  and every output carries the simulation
  label: the results JSON and the Phase-424
  report carry it in their first fields, and
  this record repeats it — added inscriptions
  are resamples of recorded inscriptions,
  never held data.
- **F062-C10** (trial resolution is strict
  exclusion of the 0.01 margin): HELD —
  APPLIED as written in every one of the
  9,950 trials: a trial resolved only where
  its interval excluded 0.01 strictly in its
  scenario's direction (an interval touching
  0.01 did not resolve); the shares in §3 are
  counts under exactly that rule.
- **F062-C11** (each scenario's target is the
  smallest added total at a qualifying grid
  point): HELD in its no-target branch — the
  rule was applied in ascending order over
  the whole frame for both scenarios; no
  point qualified, so no smallest target
  exists inside the frame for either, and
  none is stated.
- **F062-C12** (the computation searches
  only the frame the freeze fixes): HELD —
  the search ran m = 1…25 exactly as frozen,
  with the frozen trials, draws, permutations,
  seed, and the R-1 calibration; nothing
  outside the frame was searched and no
  construction was supplied at run time.
- **F062-C13** (Arm A2 is not part of Spec
  062): HELD — A2 was not designed into this
  execution, armed, joined, or executed; with
  no target returned, its trigger does not
  fire on this record (§4).
- **F062-C14** (no outcome establishes Arm
  A's rerun verdict in advance): HELD — no
  rerun verdict, target, or resolution
  quantity for Arm A2 exists in any product
  of this execution.
- **F062-C15** (the drafting-stage
  demonstration establishes nothing about the
  real corpus): HELD — the planted-data
  demonstration stands as a drafting record
  only; this outcome rests entirely on the
  execution of record (step 0 at both venues,
  the desktop grid, and the assembly), which
  computed the real recorded population's
  quantities under the frozen contract.

**Anchors.** `backend/reports/INDUS_FINAL_ANCHORS.json`
recomputed before and after the run: SHA-256
`df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569`
at both points — byte-identical, asserted
(the results JSON carries the after-hash; the
executing machine's anchors file was
recomputed at assembly with the same value).

## 6. Records

- Machine records: `reports/phase424_results.json`;
  report: `reports/phase424_report.md`
  (digests in §1).
- Graph node: `IndusPhase424ArmAPrecisionRepair`
  (registered and verified by import before
  the run; the node serves the committed
  results and does not recompute on call —
  the frozen computation is a multi-day
  checkpointed run, and this outcome is now
  its terminal record).
- Root LEDGER entry: "Spec 062 EXECUTED
  (Phase-424)" entry added with this record.
- Tasks: E2 (graph-first build) and E3 (step
  0) stand ticked from the build act; E4 (the
  computation, both scenarios, full grid) and
  E5 (this record) stand ticked with this
  record.
- `adjudication.md`, `spec.md`, `claims.json`,
  `freeze.md`, and `freeze.json` were **not**
  edited: they are digest-covered sources of
  the freeze (`test_spec062_freeze.py`
  enforces the pins), and the executed-spec
  form records execution here, in
  `outcome.md`. Spec 061's frozen texts and
  outcome record were likewise not patched —
  this outcome is appended on Spec 062's own
  record only.
- CI and foundation check (H21) at the record
  merge: appended below after the record PR
  merges, in the house completion pattern —
  this section is completed by append, not
  edited.

---

*AI disclosure: executed by an AI agent (Muse,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*

---

## Landing record — 2026-10-25 (appended at merge; append-only)

- Execution PR: **#379** (branch
  `spec-062-phase424-execution`), merged to `main`
  as merge commit
  **`26111dc4648a643dd99e2c5fb9cab98fc2eba159`**.
  The build of record was first secured on branch
  `spec-062-execution` (head `a847aa46`, via the
  git-data API) before the grid launched; because
  `main` advanced 195 commits while the grid ran,
  the record landed from a fresh branch off
  current `main` carrying the identical contents —
  script and graph module byte-identical to the
  secured build, the `experiment_graph.py`
  registration applied as the same 10-line delta
  onto current `main`'s file.
- CI: GitHub Actions run **40188371361** on the
  PR head `b4e7e68f` — **7 of 7 jobs success**,
  verified from the run's own job conclusions
  (Backend tests (pytest) — 1777 passed, 20
  skipped; Frontend tests (Playwright); Indus
  public validation checks; Evidence Graph script
  smoke tests; Shell wrappers ubuntu / macos /
  windows).
- Run digests re-verified on `main` at the
  merge commit by the contents API:
  `reports/phase424_results.json`
  `cb144835117a6991dbb64b730b6ecc931993a518e2efd592348061400232d44b`,
  `reports/phase424_report.md`
  `245b868d0ebb2dd3c6f123241d0acbd81c192102f17135401563f24e0f432b9c`,
  script
  `26d6da01831d6679b7f60bfb9a0eaa25bdd6fbf31feb326f82d0dd19c59d5483`
  — identical to the values in §1 of this
  record, and the anchors file at the merge
  commit recomputes to `df0cf620…`.
- Foundation check (H21) at the merge
  commit, on a fresh checkout of `26111dc4`
  in the prepared foundation clone (Holdat
  corpus CSV SHA-256
  `62d14d2bebf7c2c80d98a2958e75ec52bff3f240ff3f5e85d1f7f40cbe28218e`
  verified first; its counts verified exact —
  1,670 seals, 7,002 tokens): **39 checks
  passed, 0 failed, 9 warnings**, read from
  the generated report JSON. The figure
  differs from the standing 40/0/8 for a
  recorded reason that is not a defect of
  this execution: the realignment merged
  earlier the same day (PR #376) deliberately
  stopped the foundation check certifying the
  withdrawn Phase-169 aggregate-confidence
  figure — that check now reports a warning
  ("does not certify it") instead of a pass.
  Zero failures stands, and no check this
  execution touches changed state.
- Terminal outcome stands as recorded above:
  **NO TARGET UNDER EITHER SCENARIO**. No
  target was returned under either scenario;
  no operative target exists under this spec;
  Spec 061's T* is undefined on its record;
  Arm A2's trigger does not fire and nothing
  about Arm A2 is claimed. Spec 028 Arm A
  stands INCONCLUSIVE exactly as recorded.

*AI disclosure: appended by an AI agent (Muse, via Muse) at the direction of
Tristen Pierson, per constitution §VI.*
