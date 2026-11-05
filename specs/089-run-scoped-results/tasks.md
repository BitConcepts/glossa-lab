# Spec 089 — Tasks

Acceptance modes per the Autonomous Execution Doctrine: **test** (a named
automated check decides), **gate** (the Spec 086 gate / CI decides),
**human-as-oracle** (a named human reads a named artifact and rules).
Every task carries the *This does not establish* line that must survive
into its stage report.

## Stage 0 — Package adoption

- [ ] **T001 — Package lands.** spec.md, claims.md, aee-claims.json,
  plan.md, tasks.md, records/ (directive-and-grounding record, T002
  assessment + note) committed as `specs/089-run-scoped-results/` on
  `feat/089-spec-package`. Claims: package-level. Acceptance: **test**
  (the package verification of record: aee-claims.json parses; claims.md
  and aee-claims.json carry the same 20 claim ids; every claim has a
  falsifier and a DNE line; the grounding record's census numbers are
  reproducible from the repo at the package's base commit).
  *This does not establish:* that the package is approved — only that it
  is complete and internally consistent.
- [ ] **T002 — AEE verification of the claims.** The C089 bundle run
  through the pinned assessor (aee 1.5.3, CI-faithful venv), exactly as
  Spec 088's T002: `aee validate` → `valid: 20 claim(s)`; `aee assess
  --no-ledger` → **outcome: iterate** (91 failure modes; draft cap and
  stage cap binding by construction). Assessment of record:
  `records/t002-aee-assessment.json`; commands and verbatim outcome:
  `records/t002-note.md`. Acceptance: **test** (the assessor ran and its
  outcome is recorded verbatim).
  *This does not establish:* claim quality — `iterate` is the expected
  reading for a draft bundle on one asserted source; the owner's approval
  is the human act (T003).
- [x] **T003 — Owner block approval.** The owner ratifies the package as
  a block: spec, 20 claims, plan, and decisions D-089-1..6 (including
  the comparability judgment row D-089-4 and the index-only reach-back
  D-089-5). Acceptance: **human-as-oracle** (the owner).
  *This does not establish:* approval of any later stage's output — each
  lands on its own evidence.
- [x] **T004 — Adoption intake + generated-layer regeneration.** After
  T003: (a) record the pre-append gate run (gate CLI on the un-appended
  tree, ALL PASS); (b) append the C089 bundle through
  `tools/ledger/import_bundle.py --spec specs/089-run-scoped-results
  --date <adoption date>` — the only sanctioned path, never a hand-edit;
  (c) regenerate the generated layers over the grown ledger, republish
  through `tools/ledger/gated_publish.py`, and run the settling-chain
  refresh the pin move forces (canonicals verified 6/6 over the new
  build before the pin refresh), recording that this refresh executes
  under the old content-addressed discipline as the last pre-spec
  refresh; (d) the bundle-reconciliation test passes (ledger bundle
  population == bundles on disk). Claims: C089-18. Acceptance: **gate**
  (the ledger-gate job green incl. the reconciliation test; the ledger
  diff is exactly the append).
  *This does not establish:* anything about the appended claims' truth —
  only that the ledger grew by the sanctioned path and the generated
  layers match it.

## Stage 1 — run-defs v1, run record, run index (PR: feat/089-s1-run-defs)

- [x] **T101 — run-defs v1 registered.** `glossa-indus/ledger/
  RUN-DEFINITIONS.md`: closed surface list + the result-bearing test;
  run-id format and minting rule (D-089-1); run-record header (incl. the
  absence block); run-key v1 with the constitutive set of D-089-4;
  per-surface determinism classes with the tray-flake shape registered
  as the suite's known nondeterminism #1; the junction disposition
  vocabulary incl. the narrow mechanical explained case; the run-index
  act format; legacy id derivation; the CI citation form. Claims:
  C089-1, C089-9, C089-19 (defs side). Acceptance: **human-as-oracle**
  (the owner settled the judgment row at T003; the stage reviewer rules
  the document says exactly what T003 approved — any deviation returns
  to the owner).
  *This does not establish:* that the key's constitutive set is right —
  only that it is the ratified one, registered where amendments must go.
- [x] **T102 — Run-record + index library.** `backend/glossa_lab/
  run_records.py`: id minting; header construction/validation per
  surface; index act application (append + fold) for entry / supersedes
  / quarantine / adjudication acts; legacy id derivation. Claims:
  C089-1, C089-2 (format side), C089-17 (format side). Acceptance:
  **test** (the teeth of T103 pass against this library).
  *This does not establish:* that any surface uses it yet — adoption is
  S2–S4; this task proves the formats and the fold.
- [x] **T103 — Library teeth.** Tests: 10,000 same-second mints unique
  and format-conformant; header validation refuses a missing key
  component per surface and an absence block with an unregistered kind;
  index fold applies supersede/quarantine/adjudicate sequences in act
  order and refuses an act naming an unknown run id; legacy derivation
  stable and collision-free over generated store paths. Claims: C089-1,
  C089-2, C089-9. Acceptance: **test**.
  *This does not establish:* behaviour over real stores — that is T104's
  dry-run and S2's adoption.
- [x] **T104 — Dry-run index over the standing store.** On a tmp copy of
  `glossa-indus/ledger/runs/`: the fold enumerates exactly the 2 standing
  records under legacy ids, with the recoverable key components
  (semantics, candidate, pins) and the `legacy — key partial` label (no
  execution stamp or code version exists to recover). Claims: C089-17.
  Acceptance: **test** (the enumeration is recomputed from the store at
  test time, not asserted from this plan's numbers).
  *This does not establish:* the legacy treatment of records no longer
  in the store — that enumeration from git history is S5's completion.

## Stage 2 — Settling surface adoption (PR: feat/089-s2-settling)

- [x] **T201 — Run-id write path.** `settling.py` run records gain the
  run-defs header (run id an input minted by the caller; the function
  stays pure); `write_run_record` writes under run-id-derived filenames;
  the content-addressed overwrite is retired (a colliding write refuses);
  `run_settling.py` mints on `run` and appends the index `entry` act.
  Claims: C089-1, C089-2, C089-5. Acceptance: **test** (the teeth of
  T203 pass; a rerun of a registered scenario yields a second record,
  not a replaced one).
  *This does not establish:* that the engine's results changed — result
  blocks are byte-compared against the pre-stage canonical expectations
  throughout (T202).
- [x] **T202 — Canonicals + gate unchanged.** `verify-canonicals`
  reproduces 6/6 (5 scenarios + 1 comparison); the gate CLI over the
  real tree reports ALL PASS with V8's legs comparing result blocks as
  before; the standing T405 pair is neither renamed nor rewritten, and
  the stage's index covers it by legacy entries. Claims: C089-5,
  C089-17. Acceptance: **gate** (gate CLI + CI green).
  *This does not establish:* that canonical expectations are correct —
  only that the store discipline changed nothing they measure.
- [x] **T203 — Regenerations become runs; adoption teeth.**
  `materialize-sets` writes a run record + index entry and
  `assignment-sets.json` names its producing run. Teeth on tmp copies:
  same scenario twice → two records, distinct ids, byte-equal result
  blocks, no junction trigger; a mutated-pin run's key diff against the
  standing pair is exactly the pin; a forced id collision refuses; the
  store census is monotonic across the sequence. Claims: C089-5,
  C089-7. Acceptance: **test**.
  *This does not establish:* junction behaviour — S3 consumes the key
  diffs proven here; this task proves the raw material exists.

## Stage 3 — The junction tool (PR: feat/089-s3-junction)

- [x] **T301 — The comparator + junction store.** `backend/glossa_lab/
  run_junction.py` (pure) + `tools/ledger/run_junction.py` (compare /
  scan / adjudicate): key diff (constitutive marked), environment diff,
  first-divergent-output localization generalized to run-vs-run incl.
  the one-side-empty case; dispositions in the registered order
  (not-comparable → identical (no report) → shape-explained →
  unexplained + red-team section + quarantine acts). Reports land in
  `glossa-indus/ledger/junctions/` under minted junction ids, immutable.
  Claims: C089-11, C089-12, C089-14. Acceptance: **test** (the teeth of
  T302 pass).
  *This does not establish:* that the comparator finds causes — it
  localizes divergence and applies the registered dispositions; the
  unexplained state is a first-class outcome, not a failure of the tool.
- [x] **T302 — Junction teeth + the tray-flake worked example.** Fixture
  pairs: identical (listed, no report); divergent deterministic (report;
  first-divergence path is the seeded one; quarantine acts for both
  runs); one-side-empty (localization = first present result);
  constitutive-diff (not-comparable; no quarantine); flake-shape pair
  (explained-by-named-difference citing the registered shape);
  adjudication lifts one quarantine and confirms another, as acts, with
  both run records' hashes unchanged across the whole sequence. Plus
  the worked example: the PR #509 attempt-1/attempt-2 recorded summaries
  (from the CI job logs of record) entered as two suite-surface fixture
  records and junctioned to explained-by-named-difference. Claims:
  C089-11, C089-12, C089-13, C089-14. Acceptance: **test**.
  *This does not establish:* coverage of divergence shapes nobody has
  seeded — the vocabulary's unexplained state is the catch-all, and its
  honesty is the point.
- [x] **T303 — Automatic trigger on the settling surface.**
  `run_settling.py run` ends with a scan of the new record against its
  comparable predecessors in the index: a divergent rerun produces its
  junction report (+ quarantine, if unexplained) in the same invocation
  that created the run; an identical rerun reports the pair identical
  and writes nothing. Claims: C089-14. Acceptance: **test** (a seeded
  divergent rerun in a tmp store produces the report with no further
  command; a seeded identical rerun produces none).
  *This does not establish:* triggers on the other surfaces — the suite
  and experiment surfaces trigger at citation time (S4), and the gate's
  scan (S5) is the backstop for every surface.

## Stage 4 — Suite and experiment surfaces (PR: feat/089-s4-surfaces)

- [x] **T401 — Suite light-record helper.** `tools/runs/
  suite_run_record.py` over `run_records.py`: writes the local
  evidence-run record (command; tree SHA + dirty flag; result summary
  parsed from the run's own output file; the rewrite manifest over
  `glossa-indus/claims/` + `glossa-indus/reports/` with per-path
  disposition — restored (hash-verified against HEAD) or retained
  (reason required)). Teeth: a dirty-tree fixture yields the manifest;
  a retained path without a reason refuses; a fixture whose
  presentation text disagrees with its output file is recorded from the
  file. Claims: C089-6. Acceptance: **test**.
  *This does not establish:* that future stage workers will use it —
  from this stage, Spec 089's own stage records cite suite evidence
  only under this binding or the CI quadruple, and S5's gate checks the
  citation forms it can resolve.
- [x] **T402 — CI citation application + self-application.** The S4
  stage record cites its own PR's CI by {run id, head SHA, job,
  conclusion} for every job it relies on, and its local suite evidence
  by T401 records. Claims: C089-3, C089-4. Acceptance:
  **human-as-oracle** (the stage reviewer resolves every citation in
  the record to its run before merge).
  *This does not establish:* a fleet-wide citation habit — it binds this
  spec's records and gives S5 a real population to verify.
- [x] **T403 — Experiment citation records.** `tools/runs/
  job_citation.py`: given a backend job id, read job + results via the
  backend API and write the repo-side run record (header; graph id +
  registered version; parameters; job-recorded fields; result payload
  hash + quotable summary). Exercised once against the live backend on
  an existing completed job (read-only; no new experiment run),
  hash-checked against a second read of the same job; the record filed
  in the stage record's annex. The freeze-gate C2 form is registered in
  run-defs as a junction precedent (no freeze-gate code change).
  Claims: C089-8. Acceptance: **test** (record format + hash check) +
  **human-as-oracle** (the reviewer confirms the cited job is the job
  the record names).
  *This does not establish:* that past experiment citations can be
  recovered — jobs whose inputs were never recorded stay unbound
  (C089-8's falsifier is prospective).

## Stage 5 — Gate class V11 + legacy index (PR: feat/089-s5-gate-v11)

- [ ] **T501 — Legacy index completion.** Every run record that has
  ever stood in the settling store, enumerated from git history (the
  T403 originals; the 087, 088, and T004 adoption-refresh generations),
  receives its legacy index entry; entries for records no longer in the
  store name the superseding commit + blob hash; the two
  `re_derivations` entries in `settling-canonical.json` are indexed as
  legacy run events. Claims: C089-17. Acceptance: **test** (the folded
  census is checked against an independent hand enumeration of the
  store's git history, quoted in the stage record).
  *This does not establish:* that legacy results are bound — the label
  says the opposite, permanently; completeness of the census is the
  claim.
- [ ] **T502 — Gate class V11.** `ledger_gate.py` gains V11
  (run-binding) with the gate's own registered copies of run-defs v1's
  checkable rules: legs (a) producing-bindings resolve, (b) no
  quarantined citation as verdict support in the guarded set, (c)
  census equality + act references resolve, (d) divergent comparable
  pairs carry junction reports in the registered vocabulary and
  unexplained junctions are quarantined. V9 registration in the same
  PR: `run_records` / `run_junction` join the writer census; the run
  stores, indexes, and junction store join the artifact patterns.
  Claims: C089-15, C089-16. Acceptance: **gate** (the gate CLI over the
  real tree reports ALL PASS with V11 in the per-class list).
  *This does not establish:* that V11 makes run results true — it makes
  missing bindings, missing junctions, and forbidden citations
  unpublishable, which is the gate's whole office.
- [ ] **T503 — V11 teeth.** Seeded cases on tmp copies, one per leg: an
  unbound artifact fails (a); a quarantined citation fails (b); a
  dropped record (census mismatch) and a dangling supersedes link fail
  (c); a divergent pair with no junction report, and a report with an
  out-of-vocabulary disposition, fail (d). Each failure names V11.
  Claims: C089-15. Acceptance: **test** (each seeded case fails the gate
  for the stated reason; the clean tree passes).
  *This does not establish:* that no unseeded run-binding defect can
  pass — only that the named failure modes are caught, which is what
  teeth means.

## Closeout

- [ ] **T601 — Closeout record.** Per-claim dispositions for C089-1..20
  (discharged / carried, with the evidence pointer for each); the run
  census at close (stores; records by surface; index acts by kind;
  junction reports by disposition; open quarantines — expected zero, or
  named with their adjudication state); the explicit statements that no
  standing verdict was re-adjudicated by this spec, no claim's
  status/stage/score moved, and the delivery-protocol boundary held (no
  junction opened over a presentation; no run record cited as
  certifying one). Acceptance: **human-as-oracle** (the stage reviewer
  against the stage records).
  *This does not establish:* that run contamination is now impossible —
  it establishes that the named surfaces carry identity, isolation,
  comparability, and a junction rule with a gate behind them, and that
  every remaining gap is a named carry, not a silent one.
