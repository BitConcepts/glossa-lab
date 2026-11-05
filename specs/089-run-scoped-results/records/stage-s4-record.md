# Stage S4 record — suite and experiment surfaces (T401–T403)

Status: S4 built and exercised end-to-end; PR open for the
seat's gate. Discharge map: C089-6 (suite light records with
the manifest and per-path dispositions), C089-8 (experiment
citation records with determinism classes), C089-3 and
C089-4 on the surface side (the suite and experiment
surfaces' self-application; their claim-level discharge
completes at S5, which registers them in the index). The
stage record cites every run it relied on by the quadruple
{run id, head SHA, job name, conclusion} per its own T402,
below.

## What the stage built

**Suite light-record writer (T401, C089-6).**
`run_records.py` gains `parse_pytest_output`,
`rewrite_manifest`, `apply_rewrite_dispositions`, and
`build_suite_record`; the CLI is
`tools/runs/suite_run_record.py`. The parser reads a suite
run's *own output file* — the record comes from the log,
never from a presentation — taking the **last** line that
carries the count segments and a duration as the verdict
line (a `tail`'s echo of an earlier summary inside the
output cannot outrank the file's own ending), the summary
in exactly the Stage 3 fixture shape
(`{passed, failed, errors, skipped}` — extra count keys
such as deselections would break the fixture matcher's
cross-run count-equality, so they are refused by
construction, not carried), failures parsed from the
"short test summary info" block, and errors from the
ERROR headers ("ERROR at <phase> of <fn>" and
"ERROR collecting <path>") matched back to the summary's
error ids, with unmatched ids recorded at phase "unknown"
rather than dropped. The tree block names the exact tree
(`sha`, `dirty`) and the rewrite manifest: every path the
run rewrote under the watched roots
(`glossa-indus/claims/`, `glossa-indus/reports/`) with
head/worktree hashes and status (modified, new,
deleted-in-worktree). Dispositions are enforced before any
byte moves — validation completes first, so a refusal
leaves the tree exactly as the run left it: an undisposed
path refuses; a stale disposition name refuses; "retained"
without a reason refuses; "restored" puts HEAD's bytes back
(git blob bytes, no text round-trip) and re-hashes them —
or deletes a tracked-as-new file — before the record may
say so. The manifest names the regenerated artifacts; it
does not hide them.

**Experiment citation (T403, C089-8).** `run_records.py`
gains `canonical_payload_sha256`,
`mechanical_result_summary`, `build_job_citation_record`,
and `cite_job` (the backend read injected as a callable so
the binding is testable without a live backend); the CLI is
`tools/runs/job_citation.py`, reading job + results (+ the
graph record, where the job names a graph) through the
backend API, read-only. The citation record binds the job:
its key pins carry the **job id**, the graph id with its
registered version **or** the graph definition's SHA-256
(the backend carries no version field for graph records —
Departure 2), and the job's recorded parameters verbatim;
its result block carries the `job_results` payload hash
over canonical JSON plus the quotable summary (top-level
scalars verbatim; collections reduced to type+count — the
payload itself is not copied into the repo). The run id is
minted in the ratified format with its stamp taken from
the job's recorded start — the id the reader resolves from
the citation to the record (Departure 1). Absences follow
the absence block: a failed or cancelled job leaves a
`crashed` absence record; a completed job with no stored
results leaves an `empty` absence record; neither is a
citable result (their key's `result` is null, so no
junction can take them as a side); a job still pending or
running **refuses** — no citation, no absence, no store.
Determinism class defaults to
`named-nondeterministic` (§5's default); a citation names
`deterministic` only when the caller asserts it.
RUN-DEFINITIONS.md §10 registers the freeze-gate C2
spot-check form (`c2-spotcheck`) as the study surface's
junction precedent, exactly as T403 prescribes — the C2
form's outcomes map to the junction outcomes (agreement:
identical; mismatch-resolved with its note:
explained-by-named-difference; mismatch-unresolved:
unexplained, and the freeze does not proceed — the
precedent's form of the C089-13 quarantine).

**Store writer.** Both writers (and Stage 2's precedent)
needed one act, so `write_run_record` is the library's
generic store writer: validate the record, refuse on a
run-id collision with different bytes, write verified, and
append the `entry` act to the store index — the write-side
of C089-7, shared by suite and experiment stores.

**Self-application (T402).** This stage's own evidence is
bound under the new forms, in
`specs/089-run-scoped-results/records/` (the two surfaces'
store of record for Stage 4):

- the stage's full-suite evidence run (below) as light
  record **`suite-20261105T015754Z-9b193c`**, key
  `{command: "python -m pytest tests/ --tb=short -q
  --deselect
  tests/test_phase392_q2_gate.py::test_pipeline_deterministic_under_seed",
  selection ["tests/"], code_version
  edf081584fae326e1440d8548253e7f3360c3b20}`, result
  summary `{passed 2665, failed 1, errors 0, skipped
  108}`, its one failure the phase133 baseline (named in
  `failures`), its rewrite manifest naming the 11
  regenerated paths under the watched roots — all
  `restored`, hash-verified;
- the live-backend citation
  **`experiment-20261102T073847Z-8f6df8`** for completed
  job **`1762fa5137f0`** (`discovery_fetch`, executed
  2026-11-02 on the desktop backend), summary
  `{fetched 548, merged 548, new 0, errors 0}` — the
  quotable form of that job's result, reached from the
  citation record alone — with the payload hash
  `715478168b2af32cbf1a00177605ccdb8f4f757578deb9baed155a3a0692b377`
  **verified against a second read** of the job through
  the backend API (the T403 hash check, run first-hand).

Both records stand `entry`-acted in the store's
`run-index.jsonl`.

## Evidence runs relied on (T402 citation discipline)

CI is cited by the quadruple {CI run id, head SHA, job
name, per-job conclusion}; the local suite run by its
light record; the local enumeration and the backend
exercise are named with their evidence.

- **CI, PR #520, final head at this record's writing:**
  run **41952592680**, head **844289166d8636a4065197e99cd29fee164626b8**,
  attempt 1 — Backend tests (pytest): **success**;
  Frontend tests (Playwright): **success**; Indus public
  validation checks: **success**; Evidence Graph script
  smoke tests: **success**; Freeze gate records check
  (C4): **success**; Ledger/matrix/map equivalence gate:
  **success**; Cloud image smoke (Spec 083): **success**;
  Shell wrappers (ubuntu-latest): **success**; Shell
  wrappers (windows-latest): **success**; Shell wrappers
  (macos-latest): **success**. The Backend tests job is
  the C089-6/C089-8 discharging job for this stage; the
  equivalence gate job is the C089-18 guard (no ledger
  diff in this stage) and the C4 job the freeze-gate
  records' guard (no freeze record touched; the §10
  registration is documentation in RUN-DEFINITIONS.md, not
  a freeze-gate code change).
- **Local suite (the stage's enumeration), cited as the
  light record `suite-20261105T015754Z-9b193c`** (above):
  full backend suite in the glossa-ci venv **without
  `-x`**, log
  `~/workspace/glossa-run/tmp-suite/089-s4-fullsuite.log`:
  **1 failed, 2665 passed, 108 skipped, 1 deselected in
  245.75s** — the one failure is the standing phase133
  environmental baseline
  (`test_phase133_stage0_inventory.py::test_builder_recomputation_skips_without_inputs`,
  missing local download, fails locally everywhere and
  does not fail CI); the tray-teardown ERROR did not
  appear in this run; the one deselection is the standing
  phase392 local stall, named in the record's command.
  Targeted modules on the final code: 121 passed
  (`test_run_records`, `test_settling_canonical`,
  `test_settling_run_scoped`, `test_run_junction`,
  `test_run_surfaces`). Ruff over `backend/`: clean.
- **Ledger gate on the stage's final tree** (verbatim):
  full — `summary: 25 PASS / 0 FAIL / 1 NOT-RUN`,
  `RESULT: PASS`; `--regen` — `summary: 28 PASS / 0 FAIL
  / 0 NOT-RUN`, `RESULT: PASS`; `verify-canonicals` —
  6/6. No census literal moved: this stage adds no claim,
  study, or anchor (C089-18), and the gate profile is the
  standing one.

## Teeth

`backend/tests/test_run_surfaces.py`, 25 tests, names
carrying the claims:

- **Parser teeth (C089-6):** a faithful captured output
  (the PR #509 shape — 2549 passed, 98 skipped, one
  teardown ERROR, sqlite capture text) parses to counts,
  failure ids, and the error's `{test_id, phase: teardown,
  error}`; pytest's own "ERROR collecting" report (run at
  subprocess against a broken module) parses to the
  collection phase; **a presentation line inside the
  output loses to the file's final verdict line** (an
  echoed "3 passed, 9 failed in 0.50s" earlier in the file
  does not outrank the true ending); an output with no
  verdict line refuses.
- **Writer-built records feed the junction matcher
  (C089-6, C089-11):** two real pytest subprocess runs (a
  pass and a teardown-error fixture, each written by
  `build_suite_record`) load through `load_side` and
  compare to **unexplained**, first divergences naming
  `result.errors` and `result.summary.errors` — Stage 3's
  worked example rerun with writer-built records in place
  of the hand-built fixtures; and the PR #509 flake pair,
  re-entered as pytest *outputs*, writes two records the
  matcher junctions to
  **explained-by-named-difference** with the citation
  `tray-teardown-flake`.
- **Manifest teeth (C089-6):** a tmp git tree with a
  suite-style regeneration manifests the rewrite with
  head/worktree hashes; an undisposed rewrite refuses;
  `restored` returns the worktree to HEAD's bytes; a
  retained rewrite without a reason refuses, and with one
  keeps the bytes and carries the reason; a stale
  disposition name refuses.
- **Store writer (C089-7 write side):** a second write of
  the same run id with different bytes refuses and the
  index is byte-unchanged; an identical re-write is a
  no-op with no second act.
- **Citation binding (C089-8):** on a fake backend, a
  completed job's citation record resolves — record → run
  id → the exact job id in body and pins — and its
  payload hash equals an independent second read's hash
  (the T403 hash check as a test); a job naming a graph
  pins the definition hash when no registered version
  exists; the mechanical summary's shape is asserted
  exactly (scalars verbatim, collections as type+count,
  nothing else).
- **Absences (C089-8):** a failed job leaves a `crashed`
  absence whose key carries `result: null` — not a
  citable result; a completed job with no results leaves
  an `empty` absence; a running job refuses and **no store
  is created**.
- **Quarantine detectability (C089-13's binding):** with a
  citation in the same store, appending the junction
  record's quarantine act makes the citation mechanically
  detectable as quarantined from the folded index
  (`fold_index(...).open_quarantine`) — detection only;
  the gate's enforcement is S5's V11.
- **CLI teeth:** `suite_run_record.py` end-to-end on a tmp
  tree (a real mini run's record lands in the store with
  its regenerated file restored and its index act
  appended) and its undisposed-rewrite refusal on stderr;
  `job_citation.py` against an unreachable backend exits
  refused and writes no store.

## Departures

1. **The citation record's run id is minted by the
   citation writer, not at execution.** The grounding
   diagnosis for this stage held that backend jobs "mint
   execution ids" — they mint *job ids*
   (`uuid4().hex[:12]`, `database.create_job`), which are
   not run ids in the ratified format, and no execution-
   side hook writes repo-side records (the backend's
   results live in its database behind the API;
   `run_experiment_graph` writes its outputs into
   job-result JSON). A run record is therefore written at
   citation time (D-089-6's binding act) with its stamp
   taken from the job's recorded start: the run id's
   timestamp *is* the execution's start, and the job id
   is bound in the record body and the key's pins, so the
   binding run ↔ job is two-way and mechanical. Minting at
   execution would require backend-side store writes on
   every job — deferred to an owner decision if ever
   wanted; the plan's text ("the citation record binds the
   run to its job") is what this stage builds, and T403's
   parenthetical ("or the job result JSON's run context")
   is honored by binding through the job record, the only
   run context the backend persists.
2. **Graph identity pins the definition hash.** The
   backend's graph records carry no registered version
   field (they are `GraphDefinition` JSON), so the pin is
   the graph id plus the definition's SHA-256 wherever no
   version exists — §5's own "or the definition hash where
   the surface carries no version field," applied
   verbatim. The exercised live job carried no graph
   (its `exp_id` was null); the graph-pin path is proven
   by the fake-backend tests, not by a live graph job —
   none exists in the backend's job history to exercise
   (of 18 jobs, 17 are `discovery_fetch` and 1 is a
   `study_loop` with no stored results).
3. **RUN-DEFINITIONS.md §10 is a registration, not an
   amendment.** T403 names the C2 registration as this
   stage's act under §5/§6; the registration adds §10
   prose only — no rule, table, or vocabulary changes,
   the version stands at v1, and §5's study row already
   forward-referenced the C2 precedent. No freeze-gate
   code was touched.
4. **The suite summary carries exactly four count keys.**
   Pytest's verdict line can carry `deselected` and
   `warnings` segments; carrying them in `summary` would
   break the fixture matcher's count-equality against
   records that lack them, so the parser accepts those
   segments in the line but does not record them — the
   deselection this stage's own enumeration makes is
   named in the record's command and in this record,
   which is where a reader looks for it.
5. **The repository-root regeneration stands outside the
   manifest.** The stage's enumeration also regenerated
   `outputs/partial_loop_result.json` (repo root, outside
   the watched roots §4.2 names); it was restored by
   convention (`git checkout`), and the manifest's
   silence about it is the watched-root definition
   working as written — extending the watched set is a
   run-defs act, not this stage's.

## Census re-pin

None. No claim, study, anchor, or program-map count moves
in this stage (C089-18); the gate summaries above are the
standing profile, unchanged.
