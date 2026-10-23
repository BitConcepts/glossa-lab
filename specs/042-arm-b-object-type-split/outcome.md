# Spec 042 / Phase-407 — Outcome record (EXECUTED 2026-10-21 — THIN, gate 0.4)

> ## EXECUTED — 2026-10-21
>
> Executed under the frozen Spec 042 contract
> (freeze digest
> `6be2988d7f4c290591d36f391ac84a772f18a9121e35ddd0e251956b5260f753`)
> as **Phase-407**, in Wave 3 of the
> runnable-experiments campaign (plan approved
> as written on 2026-10-21; campaign member 19,
> design D-28). The execution gate was satisfied
> before the run: OSF registration **tmyzg** is
> APPROVED + PUBLIC. Step 0 (spec §3) ran in the
> frozen order, fail-closed: gates 0.1–0.3
> passed, gate 0.4 found the tablet stratum
> TOO THIN, and the execution closed at that
> gate with headline **THIN**. Neither stratum
> was computed, gate 0.5 was not reached, and
> no verdict is recorded. Spec 028's Arm B
> stands exactly as recorded (INCONCLUSIVE).

## Headline (spec §4.3 wording, THIN form)

"The object-type split cannot be run as
designed: the tablet stratum carries fewer
than six sites with at least twenty
inscriptions of its type (Chanhu-daro 2;
Dholavira 15; Harappa 1076; Kalibangan 3;
Lothal 2; Mohenjo-daro 164). No stratum
quantity was computed. Spec 028 Arm B stands
exactly as recorded."

Corpus: the Phase-393 layer (the
Yajnadevam-compiled inscription file as held
by the program), with its lineage posture as
recorded in Specs 027/028. Headline outcome:
THIN. This result is about repertoire
association in recorded data. It is not
evidence that any population moved.

Claim: `STUDY-SPEC-028/ARM-B` — INCONCLUSIVE
on its recorded numbers (median adjusted R²
0.0223721, interval [0.0122174, 0.0333271],
rejection share 0.9548, drop-Harappa
leave-one-site-out median 0.0066068 against
the 0.01 margin), unchanged. No stratum
verdict, no split direction, and no
exoneration is recorded: the test the split
was registered to run could not be run as
designed, because in this corpus layer the
tablet record survives at scale at only two
of the six analysis sites — Harappa (1,076
of the stratum's 1,262 records) and
Mohenjo-daro (164) — while Dholavira (15),
Kalibangan (3), Lothal (2), and Chanhu-daro
(2) fall below the frozen per-site floor of
20. That is a statement about the recorded
population's shape, not about the claim: the
hypothesis of §1.2 (the Harappa dependence
localised to tablets) is unjudged, neither
supported nor falsified. Spec 037's census
caution — object-type labels diverging
between compilations in 49% of matched cases
— is restated here, as it travels with every
statement under this spec; the split uses
type only as recorded within the Phase-393
layer.

## 1. What was executed

Step 0 only (spec §3 gates 0.1–0.4 reached,
in the frozen order), under the graph-first
build (H15/H23): experiment script
`backend/scripts/phase407_arm_b_object_type_split.py`;
graph module
`backend/glossa_lab/experiment_graph_phase407.py`
(node `IndusPhase407ArmBObjectTypeSplit`);
registration in
`backend/glossa_lab/experiment_graph.py`; the
registration verified by import in the run
environment before the phase ran (the node is
present in `ATOMIC_NODES`). The script also
carries the gate-0.5 pooled regression and
the §4 primaries in the frozen form; neither
was reached or run, and no repertoire
quantity of any kind was computed. The run's
own records: `reports/phase407_results.json`
(SHA-256
`6f0f5a4f37918d7acb2e899b916131d133d13fc6cecd3b2f4b03662d96919d72`)
and `reports/phase407_report.md` (SHA-256
`67f0cc005508e52e304bff03c277834558abc06c25d299e587b2bb4898a6c37e`)
— both digests derived twice by independent
routes (`sha256sum` and a Python `hashlib`
recomputation, identical), and the script is
deterministic: a second run reproduced both
output files byte-identically. The run's base
was `main` at
`3200b7b5b6841a7b9567a81368bf84004fd17255`.

Every spec §2 pin was also re-derived in the
foreground before the run, by two independent
routes — the fresh clone's working-tree files
hashed with `sha256sum`, and the git blobs at
the base commit hashed with Python `hashlib` —
and both routes agreed with the freeze record
on all six inputs (corpus layer `c02e3d7b…`,
Phase-393 results `0a1657a8…`, pipeline
`6c2ff91c…`, margins audit `15ae0281…`, Spec
028 freeze `376cd8e7…`, anchors `df0cf620…`).
The Phase-393 machinery's own store inputs
(the M77-keyed layer and the Horus layer,
gitignored downloads) were supplied from the
program's existing local downloads and
verified the same way against their frozen
hashes (`bbfdbcd5…`, `c368f290…`).

## 2. Step 0, gate by gate

- **0.1 Input integrity — PASS.** Every §2
  input recomputes to its freeze-record
  value (all six pins, in the results JSON).
- **0.2 Population reproduction — PASS.** The
  frozen population flow, re-run on the
  pinned machinery inputs, reproduces the
  recorded flow counts exactly (5,679 /
  4,531 / 4,505 / 3,605 / 3,144 / 3,030), the
  recorded flow dict of both the Phase-393
  results and the Spec 028 margins audit, the
  recorded Arm B analysis set (3,030 records
  at the 6 recorded sites), the recorded
  site × type cell table (identical to the
  margins audit's analysis-population cells,
  cell for cell), and the 125 sign columns.
- **0.3 Partition census — PASS.** The
  analysis population partitions by recorded
  object type with no record of any other
  type; the strata sum to 3,030:

  | Site | SEAL | TAB | Total |
  |---|---|---|---|
  | Chanhu-daro | 52 | 2 | 54 |
  | Dholavira | 96 | 15 | 111 |
  | Harappa | 361 | 1,076 | 1,437 |
  | Kalibangan | 49 | 3 | 52 |
  | Lothal | 72 | 2 | 74 |
  | Mohenjo-daro | 1,138 | 164 | 1,302 |
  | **Total** | **1,768** | **1,262** | **3,030** |

- **0.4 Stratum floors — SEAL PASS, TAB TOO
  THIN (the execution closes here).** The
  seal stratum clears the floor at all 6
  sites (minimum: Kalibangan, 49). The tablet
  stratum carries at least 20 inscriptions
  at only 2 of the 6 sites (Harappa 1,076;
  Mohenjo-daro 164; Dholavira 15; Lothal 2;
  Chanhu-daro 2; Kalibangan 3) and is
  recorded TOO THIN with its counts. Under
  DD-042-2 (confirmed at the freeze), either
  stratum below its floor closes the whole
  execution with headline THIN and neither
  stratum is computed: the headline under
  this spec is the pattern across strata, and
  a one-stratum result quoted alone would
  misstate the test. The seal stratum was
  therefore not computed either, although it
  clears its own floor.
- **0.5 Pooled regression — NOT REACHED.**
  The execution closed at gate 0.4; the
  pooled-regression machinery check did not
  run, and this record claims no reproduction
  under it. (Gates 0.1–0.2 re-asserted the
  machinery's inputs and population; the
  machinery itself is the pinned pipeline,
  byte-identical to the calibrated pipeline
  of record.)

**Per-stratum descriptions (spec §5;
described, not controlled).** Period is not
controlled under this spec (that is design
D-26, blocked); the recorded mixes are
published so a reader can see the population
the closure sits on. From the pinned layer,
joined by inscription id with full coverage
(1,768 of 1,768 seal records; 1,262 of 1,262
tablet records): the seal stratum's period
field is unrecorded ("-") for 1,005 records,
with Intermediate 302, Late 248, and the
remainder in numbered and layer labels; its
preservation is complete 1,101, fragment
388, slightly chipped 98, chipped 97, partly
damaged 82. The tablet stratum's period
field is unrecorded for 698 records, with
495 carrying the label "3", Intermediate 32,
Late 21; its preservation is complete 955,
fragment 191, chipped 59, slightly chipped
45, partly damaged 12. The full
distributions are in `reports/phase407_results.json`.

## 3. What this outcome does and does not establish

It establishes that the object-type split
cannot be run as designed on the Phase-393
analysis population: one of its two strata
fails the frozen floor the design itself
set, on observed counts stated above. The
frozen pooled Arm B result stands exactly as
recorded — this closure neither edits,
supersedes, nor re-adjudicates it, and the
INCONCLUSIVE verdict remains the program's
word on Arm B. It does **not** establish
anything about the §1.2 hypothesis: no
stratum quantity was computed, so whether the
Harappa dependence is localised to tablets,
is a whole-corpus property, or behaves any
other way remains untested under this
variant — unjudged, not failed on its
merits. It does not exonerate object type
(the falsifier's outcome requires both
strata adjudicated alike, which did not
occur), and it does not support the reverse
reading either. What would unblock a
successor is a design decision outside this
frozen run: a population in which the tablet
record survives at more sites, or an owner
amendment re-scoping the floors or the
stratum definition, honestly labelled as a
new test. This record does not commission
that act, and nothing was repaired in-pass.

## 4. Claim consequences (governed register)

Executed under register 0.7-draft (frozen);
one line per claim, F042-C01…C15.

- **F042-C01** (an outcome states only how the
  Arm B association behaves within the
  strata): HELD — this record states no
  stratum behaviour at all; it records a
  runnability closure only, within the
  claim's scope.
- **F042-C02** (`STUDY-SPEC-028/ARM-B` stands
  INCONCLUSIVE on its recorded numbers):
  CHECKED — the pinned results file
  hash-verified at gate 0.1 and read at the
  run; the recorded numbers and the verdict
  stand exactly as stated.
- **F042-C03** (the hypothesis: the seal
  stratum satisfies the SUPPORTED rule in
  full, the tablet stratum does not): NOT
  JUDGED — no stratum was computed; the
  hypothesis is neither supported nor
  falsified.
- **F042-C04** (uniform outcomes exonerate
  object type): NOT REACHED — the uniform
  condition did not arise; no exoneration is
  recorded in either direction.
- **F042-C05** (the variant appends; the
  frozen verdict is untouched): HELD — this
  outcome appends as a dated, stratum-census
  entry beside the frozen record; no Spec
  028 file was modified (its pins re-verified
  at gate 0.1 and unchanged).
- **F042-C06** (each stratum computed with
  the machinery unchanged): HELD in its gate
  form — the machinery of record was pinned
  and its population reproduced (gates
  0.1–0.2); no stratum computation occurred
  for the requirement to govern, and gate
  0.5's operational reproduction was not
  reached (recorded plainly in §2).
- **F042-C07** (the strata partition the
  3,030 records by recorded type): CHECKED —
  the gate-0.3 census partitions the
  population exactly (1,768 + 1,262 =
  3,030), with no record of any other type.
- **F042-C08** (stratum entry gated by the
  frozen floor; THIN closes the execution):
  FIRED as written — the tablet stratum is
  below its floor, recorded TOO THIN with
  its counts, and the whole execution
  closed THIN with neither stratum computed
  (DD-042-2).
- **F042-C09** (execution stops before any
  stratum quantity on any step-0 gate
  failure): FIRED as written — gates ran in
  order, the failure fired at 0.4, and no
  stratum quantity exists.
- **F042-C10** (per-stratum verdicts follow
  the frozen family rules verbatim): NOT
  REACHED — no verdict was assigned to
  either stratum.
- **F042-C11** (the headline is exactly one
  of SPLIT, UNIFORM-PASS, UNIFORM-FAIL,
  THIN): HELD — the headline is THIN, the
  gate-0.4 member of the frozen set.
- **F042-C12** (a tablet-supported split is
  SPLIT REVERSED): NOT REACHED — no split
  occurred.
- **F042-C13** (control failure is NOT
  ADJUDICATED): NOT REACHED — no stratum's
  controls ran.
- **F042-C14** (period mix described per
  stratum in every outcome product): HELD —
  each stratum's recorded period and
  preservation distributions are published
  in §2 of this record, in the phase report,
  and in the results JSON; period is
  described, not controlled, and no product
  claims control.
- **F042-C15** (no outcome establishes a
  mechanism, movement, or meaning): HELD —
  no such statement appears in any product
  of this execution; genre, administration,
  and chronology remain live rival
  explanations, named as such, for any
  future test.

**Anchors.** `backend/reports/INDUS_FINAL_ANCHORS.json`
recomputed before and after the run: SHA-256
`df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569`
at both points — byte-identical, asserted.

## 5. Records

- Results: `reports/phase407_results.json`;
  report: `reports/phase407_report.md`
  (digests in §1).
- Graph node: `IndusPhase407ArmBObjectTypeSplit`
  (registered and verified by import before
  the run).
- Execution tests:
  `backend/tests/test_spec042_execution.py`
  (the delivered form pinned: outcome, gate
  facts, census, the absence of stratum
  quantities, the frozen THIN wording).
- Root LEDGER entry: "Spec 042 EXECUTED
  (Phase-407): THIN at gate 0.4" added with
  this record.
- Tasks: E1 (graph-first build), E2 (step 0,
  gates 0.1–0.3), E3 (step 0, gate 0.4 — with
  the THIN closure noted; its gate-0.5 part
  not reached), and E5 (outcome) stand ticked
  in `tasks.md`; E4 (primaries) stands open
  in form and is closed in substance by this
  record — it cannot run under this frozen
  contract, and any successor is a new act
  under a new freeze or an amendment.
- `adjudication.md`, `spec.md`, `claims.json`,
  `freeze.md`, and `freeze.json` were **not**
  edited: they are digest-covered sources of
  the freeze (`test_spec042_freeze.py`
  enforces the pins), and the executed-spec
  form records execution here, in
  `outcome.md`.
- CI and foundation check (H21) at the record
  merge: appended below after the record PR
  merges — this section is completed by
  append, not edited.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*

---

## Landing record — 2026-10-21 (appended at merge; append-only)

- Execution PR: **#276** (branch
  `spec-042-phase407-execution`), merged to
  `main` as merge commit
  **`68c31046a3bdcaf015629b738ed595db58983045`**.
  The PR head at merge was `3c0ade7c` (the
  execution commit `3fbb5a32` plus two merges
  of advancing `main` and one empty
  CI-retrigger commit: two synchronize events
  produced no run — a platform event-dropping
  incident — and a genuine run was obtained
  before merging, per the standing rule).
- CI: GitHub Actions run **39634601098** on
  the PR head `3c0ade7c` — **7 of 7 jobs
  success**, verified from the head commit's
  own check-runs (Backend tests (pytest);
  Frontend tests (Playwright); Indus public
  validation checks; Evidence Graph script
  smoke tests; Shell wrappers ubuntu / macos
  / windows). (The first head, `3fbb5a32`,
  also ran 7 of 7 green in run 39628823142.)
- Run digests re-verified on `main` at the
  merge commit by two routes (the contents
  API download hashed with `sha256sum` and
  with Python `hashlib`):
  `reports/phase407_results.json`
  `6f0f5a4f37918d7acb2e899b916131d133d13fc6cecd3b2f4b03662d96919d72`,
  `reports/phase407_report.md`
  `67f0cc005508e52e304bff03c277834558abc06c25d299e587b2bb4898a6c37e`
  — identical to the values in §1 of this
  record.
- Foundation check (H21) at the merge
  commit, on a fresh worktree of
  `68c31046` with the two Holdat CSVs copied
  from the existing local downloads (corpus
  CSV SHA-256
  `62d14d2bebf7c2c80d98a2958e75ec52bff3f240ff3f5e85d1f7f40cbe28218e`
  verified first, by two routes): **40
  checks passed, 0 failed, 8 warnings** —
  the standing figure.
- Local-environment disclosure (carried
  from the execution): in this VM's
  glossa-aee150 venv, one unrelated frozen
  test (`test_spec040_freeze.py::test_spec040_freeze_register_lenient`)
  fails locally; it was verified to fail
  identically on the pristine `main` tree at
  the run's base with no execution changes
  present — the known pre-existing local
  AEE-loader issue class (the same class
  disclosed on Spec 045's record). The PR's
  CI run is the figure of record, and it is
  green.
- Terminal outcome stands as recorded
  above: **THIN** at gate 0.4. Neither
  stratum was computed, no verdict exists
  under this spec, and Spec 028 Arm B stands
  exactly as recorded.

*AI disclosure: appended by an AI agent (Muse Spark, via Muse) at the direction of
Tristen Pierson, per constitution §VI.*

