# Stage S3 record — Spec 089 (2026-11-04)

**Scope:** tasks.md Stage 3 (T301–T303): the junction
tool — the comparator, its CLI, the junction store, and
the automatic trigger on the settling surface. Executed
on branch `feat/089-s3-junction` off origin/main
`137aa738`. The suite / experiment bindings are S4; gate
class V11 + the legacy index completion are S5. The
claims ledger is untouched (C089-18).

## What was built

- **`backend/glossa_lab/run_junction.py`** — the
  comparator and its thin store layer. `compare_sides`
  is pure: two loaded run sides → the key diff (every
  run-key v1 component, constitutive marked; a
  component absent from either key is `unrecoverable`,
  never silently agreed), the environment diff
  (code version + environment class, recorded-and-
  diffed per D-089-4), the first divergent output
  localized by recursive descent over the outcome
  blocks (the `run_settling.py` `_first_divergences`
  path format and cap, generalized to run-vs-run; the
  one-side-empty case localizes as the absence plus
  the first result present on the non-empty side), and
  exactly one disposition, in the registered order:
  constitutive difference → `not-comparable` (no
  report, no acts — the pair is refused as a junction,
  the differing components named); outcome blocks
  equal → identical (listed, no report), or
  `identical-after-all` where a presentation asserted
  a divergence the byte-stable records do not carry
  (a report naming the presentation artifact);
  divergence wholly inside a registered
  nondeterminism shape → `explained-by-named-
  difference`, citing the shape, its itemized
  evidence, and the divergent lines; otherwise →
  `unexplained`, the report carrying the red-team
  section (the six registered causes, each pre-filled
  with the mechanical evidence bearing on it and the
  question the red team must answer, every marking
  left to the red-team act) and both runs quarantined
  by index act. The store layer loads sides from the
  index's entry acts (hashing the stored bytes and
  re-reading them for the byte-stability check), files
  reports into the junction store
  (`glossa-indus/ledger/junctions/<junction-id>.json`,
  minted ids, immutable — an existing target refuses),
  and appends quarantine / adjudication acts only
  through `run_records.append_act`, so the fold's
  refusals bind this tool as they bind every writer.
  The shape matcher for suite shape #1
  (`tray-teardown-flake`) requires every registered
  element present in the records — teardown ERROR
  entries only, sqlite closed-database family, tray
  test ids, pass and fail counts equal, failure lists
  identical, all other summary counts equal, and the
  error-count delta exactly the differing entries; a
  missing element is a named reason, recorded in the
  red-team section's nondeterminism evidence when the
  pair falls through to unexplained. An explained
  classification is never asserted without its
  evidence.
- **`tools/ledger/run_junction.py`** — the CLI,
  mirroring `run_settling.py`: `compare RUN_A RUN_B`
  (run ids or store-relative record filenames; prints
  the pair's line and, on a triggering pair, the filed
  report; `--presented-artifact NAME` names a
  presentation of the pair for the identical-after-all
  case), `scan [--store PATH] [--run RUN_ID]` (every
  comparable pair in the index analyzed; identical
  pairs listed; pairs that cannot pair — legacy sides,
  constitutive differences — listed with their reason),
  `adjudicate JUNCTION_ID --ruling ... --actor ...
  [--resulting-state ...]` (appends the adjudication
  act; lifts or confirms the quarantine; never edits
  the report or the run records). On an unexplained
  pair the compare/scan output states the citation
  consequence in words: neither run's results may be
  cited as verdict support while the quarantine stands
  open (enforcement at citation points is S5's gate
  leg, not this stage's).
- **The automatic trigger (T303)** —
  `tools/ledger/run_settling.py run` now ends with a
  scan of the new record against its comparable
  predecessors in the index (comparability decided by
  the keys alone): a divergent rerun produces its
  junction report (+ quarantine, if unexplained) in
  the same invocation that created the run; an
  identical rerun prints the pair identical and writes
  nothing. The scan covers the run's no-result paths
  too (a refused or crashed execution whose absence
  record entered the index is scanned the same way —
  the one-side-empty junction of C089-11); a scan
  refusal is named on stderr, and on the success path
  exits 1 with the run's record and entry standing.
- **`backend/tests/test_run_junction.py`** — the
  stage's teeth (T301–T303): **18 tests**, on tmp
  stores and tmp mirror trees throughout.

## Evidence

Targeted modules on the clean tree (glossa-ci venv,
TMPDIR on disk): test_run_records 52 +
test_settling_canonical 13 + test_settling_run_scoped
13 + test_run_junction 18 = **96 passed** — S1/S2 teeth
intact with the trigger live on the settling CLI.

The worked example, from the tool's own CLI output
over fixture records built from the CI job logs of
record (below):

```text
suite-20261104T133531Z-a11001 vs suite-20261104T134045Z-a22002: explained-by-named-difference
disposition: explained-by-named-difference
shape evidence:
  - shape consulted: run-defs v1 §5, suite nondeterminism shape #1 (tray-teardown-flake) — every element of the registered shape is present in the records
  - pass counts equal: 2549 in both runs
  - fail counts equal: 0 in both runs
  - failure lists identical (0 failure(s) in both runs)
  - error entry 'tests/test_tray_token_auth.py::test_copy_api_token_without_tkinter_is_named': teardown ERROR, sqlite closed-database family, tray test id — recorded error: sqlite3.ProgrammingError: Cannot operate on a closed database.
  - summary error counts differ by exactly the 1 differing entry
divergent lines:
  - result.summary.errors: 0 in run B, 1 in run A
  - result.errors: length 0 in run B, length 1 in run A
```

The fixture pair is PR #509's real comparable-run
pair: CI run `41839490370` (Spec 088 S5, head
`a0fbdf97`), Backend tests (pytest) job — attempt 1
(job 126606956437, 13:35:31Z–13:40:13Z): *2549 passed,
98 skipped, 1 error*, the single mark the teardown
ERROR on the registered test id with the sqlite
closed-database text; attempt 2 (job 126609751508,
13:40:45Z–13:44:39Z, the failed-jobs rerun): *2549
passed, 98 skipped*, no error — read first-hand from
the two jobs' logs this stage, and matching the Spec
088 closeout record's summary of the same pair (2,549
passed; rerun green). The manual adjudication of
2026-11-04 (flake family; rerun is the remedy) is
reproduced mechanically, with the evidence chain the
manual act never had to produce. The CI runs are not
store runs: the fixture records are constructed from
those recorded facts and are labeled as fixture
records in the test module (their header fields are
the executions' recorded facts — the workflow's
invocation, the head SHA as code version, `ci/linux`;
the pytest version is not pinned in the job log, so
`tool_version` carries a fixture value stating that,
identical for both records; the result blocks carry
the outcome fields the registered shape is stated
over — the counts and the error entries — and not
the logs' durations or warning counts, which are
presentation detail of the log, not result content).

The scan over the standing settling store (the real
tree, this stage): *0 comparable pairs analyzed, 1
pair not paired* — the T405 pair's legacy entries pair
with nothing, a direct compare of the two legacy ids
dispositions `not-comparable` naming `command`,
`tool_version`, `seed` as the unrecoverable
constitutive components, and the store is byte-
unchanged by all of it (run-index.jsonl SHA-256
`2f01f33e…` before and after; no `junctions/`
directory created — no real junction has occurred
under the machinery yet, and the store comes into
existence with the first filed report).

Full backend suite, no `-x`, read from its log file
(`~/workspace/glossa-run/tmp-suite/089-s3-fullsuite.log`),
deselecting only the documented phase392 local-stall
test:

```text
1 failed, 2640 passed, 108 skipped, 1 deselected, 29 warnings in 264.77s
FAILED tests/test_phase133_stage0_inventory.py::test_builder_recomputation_skips_without_inputs
```

- The one failure is the phase133 environmental
  baseline, the acceptable non-pass of record.
- The tray-teardown ERROR did not appear in this run.
- 2 of the 108 skips are this stage's trigger tests,
  under the same clean-tree precondition guard as
  S2's 8 (verified by reproduction: on the suite-
  dirtied tree the junction module runs 16 passed +
  2 skipped with the cause named; on the restored
  clean tree, 18 passed). The skipped delta against
  S2's enumeration (106 → 108) is exactly those 2.
- The suite's in-tree regenerations
  (`extracted_claims`, `claim_reports`,
  `outputs/partial_loop_result.json`) were restored
  before committing; the final tree carries only this
  stage's files. No census literal moved (no spec,
  claim, or artifact count changes in this stage), so
  no re-pin was owed.

Ruff over `backend/`: **all checks passed**. The new
CLI under tools/ carries the one EXE001-class finding
its `tools/ledger/` siblings carry (the directory's
files are mode 100644 by repo convention, and the
gate's ruff scope is `backend/`); `run_settling.py`'s
2 findings are its pre-existing ones, unchanged —
this stage added none to it. `verify-canonicals`
through the CLI still reproduces **6/6**.

Ledger gate on the final tree, verbatim summaries —
the standing profile, unchanged:

```text
full:    summary: 25 PASS / 0 FAIL / 1 NOT-RUN   RESULT: PASS
--regen: summary: 28 PASS / 0 FAIL / 0 NOT-RUN   RESULT: PASS
```

Teeth of record, beyond the counts above: an
identical pair leaves the index byte-identical and
creates no junction directory; a divergent pair's
report localizes the seeded path (`result.verdict`)
as its first divergence; a result-vs-absence pair
localizes the absence (kind `crashed`) plus the first
present result (`result.assignments[0].sign`); four
mutations of the worked-example pair (non-sqlite
error text, unequal pass counts, non-tray test id,
non-teardown phase) each refuse the explained
classification and go unexplained + quarantined, with
the shape's unmet element named in the red-team
evidence; adjudication lifts one quarantine and
confirms another while every run record's SHA-256
stands unchanged across the whole sequence, and an
adjudication naming an unknown junction refuses with
the index byte-unchanged; a seeded divergent rerun
through the settling CLI produces its junction +
quarantine in the same invocation (report's first
divergence = the seeded mutation's path), and an
identical rerun produces neither a report nor an act.

## Claims discharged at this stage (per plan.md Stage 3)

- **C089-11** — divergence between comparable runs
  now produces the junction mechanically before any
  verdict use: at run completion, against the index's
  comparable predecessors (the settling trigger), and
  by store scan; the one-side-empty case is a
  first-class trigger, localized as prescribed.
- **C089-12** — the junction report is mechanical
  first, in the registered form: both runs named by
  id with their records' hashes, the key diff
  component by component (constitutive marked), the
  environment diff, the first divergent output
  localized (incl. the one-side-empty rule), and
  exactly one disposition from the registered
  vocabulary; `explained-by-named-difference` names
  the difference and carries the evidence connecting
  it to the divergence (the shape's itemized
  evidence chain).
- **C089-13** — an unexplained junction quarantines
  both runs by index act in the same act that files
  the report; the tool states the citation
  consequence on its face, and quarantine is lifted
  or confirmed only by a recorded adjudication act
  (the CLI's `adjudicate`, a named actor), never by
  an edit — asserted by hash across the teeth
  sequence. (Gate enforcement of the citation ban
  over published artifacts is V11's leg (b), S5.)
- **C089-14** — the analysis is automatic in both
  tiers the claim names: the mechanical junction
  fires at run completion and by scan without an
  operator asking; an unexplained disposition
  carries the red-team section — the six registered
  causes attacked in turn on pre-filled mechanical
  evidence, with the questions the red team must
  answer — as part of the filed report. The
  sustained / not-sustained markings remain the
  red-team act's, by design (D-089-2).

## Departures and judgments, stated plainly

1. **Where the brief's summary and the plan differ,
   the plan governs.** The stage brief described
   identical and explained junctions as appending
   adjudication acts to the index. Run-defs v1
   §7.1's fold refuses an adjudication act naming a
   junction no quarantine act introduced, and plan.md
   T303 states an identical rerun "writes nothing".
   Implemented per plan + run-defs: identical pairs
   write nothing and append nothing; explained pairs
   file the junction report with its evidence cited
   (the mechanical adjudication of record, in the
   junction store); `adjudication` acts exist only
   for quarantined junctions, appended by the named
   actor's CLI act. Likewise the brief's red-team
   "brief" is the report's red-team **section** (the
   plan's form), carrying the brief's contents: the
   two runs and their record hashes, their keys
   (the key diff), the localized diff, the
   determinism registry entries consulted, and the
   questions the red team must answer.
2. **Not-comparable pairs file no report.** The
   disposition is printed with the differing
   components named (the refusal), and scan does not
   pair non-comparable entries at all — the junction
   store holds reports for pairs that *are*
   junctions (explained, identical-after-all,
   unexplained), per plan.md's disposition logic
   ("not-comparable (no result diff claimed)").
3. **"Tray test ids", machine reading.** Run-defs
   registers the shape over "tray test ids" with one
   named instance (`test_tray_token_auth.py::…`).
   The matcher reads it as: the test id's module
   basename contains `tray`. A future tray module
   named otherwise would fall outside the mechanical
   case and go unexplained until a run-defs
   amendment names it — the conservative direction.
4. **The suite result schema the matcher reads** —
   `result.summary` counts (passed / failed /
   errors / skipped), `result.failures`,
   `result.errors` entries of `{test_id, phase,
   error}` — is the fixture schema of this stage's
   teeth and worked example. S4's suite light-record
   writer must emit this shape for live suite
   junctions to be mechanically explainable; the
   binding is stated here so S4 inherits it by
   record, not by discovery.
5. **Identical-after-all needs its presentation
   named.** The disposition fires only when a caller
   names the presentation that asserted the
   divergence (CLI: `--presented-artifact`) and both
   stored records are byte-stable on re-read — an
   unstable record defeats it (the pair is then
   identical on its records, and the instability is
   the corruption question, not a presentation
   finding). Without a named presentation, equal
   records are simply identical and nothing is
   filed: the tool does not invent presentations to
   disposition against.
6. **Re-analysis is a new report.** Per plan.md, a
   re-analysis of a pair mints a new junction id and
   files a new report (and, if unexplained, a new
   quarantine act under that id); neither scan nor
   the trigger dedupes against earlier reports. The
   fold keeps every junction's quarantine state
   separately, and adjudication addresses one
   junction at a time.
7. **The trigger's scope is the `run` command.**
   Plan.md names `run_settling.py run`; the trigger
   rides its success and absence paths.
   `materialize-sets` carries no trigger in this
   stage (its runs enter the same index and are
   covered by any later scan, and by S5's gate scan).
   A trigger scan refusal on the success path exits
   1 (the run's record and entry stand, the refusal
   named on stderr); on the refusal/crash paths the
   execution's own refusal governs and the scan's
   outcome is reported on stderr only.
8. **V9 writer census.** `run_junction.py` writes
   junction reports and (through `run_records`) index
   acts; its paths match none of the gate's artifact
   patterns, and registering the run machinery's
   write entry points with the V9 census remains
   S5's act, exactly as plan.md Stages 1 + 5 assign.
   The gate's standing profile is verified unchanged
   above.

## Stage 3's "does not establish" lines (from tasks.md)

- T301: *This does not establish: that the comparator
  finds causes — it localizes divergence and applies
  the registered dispositions; the unexplained state
  is a first-class outcome, not a failure of the
  tool.*
- T302: *This does not establish: coverage of
  divergence shapes nobody has seeded — the
  vocabulary's unexplained state is the catch-all,
  and its honesty is the point.*
- T303: *This does not establish: triggers on the
  other surfaces — the suite and experiment surfaces
  trigger at citation time (S4), and the gate's scan
  (S5) is the backstop for every surface.*

**AI disclosure:** executed by an AI agent (Muse, via
Muse) at the direction of Tristen Pierson, per
constitution sec. VI.
