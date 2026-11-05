# Stage S2 record — Spec 089 (2026-11-04)

**Scope:** tasks.md Stage 2 (T201–T203): the settling
surface adopts run identity — the engine write path,
the CLI, and the run index over the standing store.
Executed on branch `feat/089-s2-settling` off
origin/main `0c8815ec`. The junction tool is S3, the
suite / experiment bindings S4, gate class V11 + the
legacy index completion S5. The claims ledger is
untouched (C089-18).

## What was built

- **`backend/glossa_lab/settling.py`** — `run_record`
  gains the run-defs header (T201): the header is an
  *input* the executing tool builds over the same
  state (`settling_run_header`: the key's input pins
  are the record's pins block verbatim, the seed is
  the registered no-seed marker, the tool version
  comes from the package metadata per governance H10);
  a header whose pins are not the state's is refused.
  With no header supplied, the record carries an
  **ephemeral** header marked non-store — the
  in-memory recomputation case (verify-canonicals,
  the canonical oracle) — and `write_run_record`
  refuses ephemeral and headerless records by name.
  Stored records land under a filename derived from
  their run id, never from content; a target that
  already exists refuses (the cross-process half of
  mint uniqueness, deferred here by S1). The
  content-addressed `run_record_filename` is retired
  as a write path and kept importable as a
  legacy-path resolver. `materialize-sets` support:
  `stamp_assignment_sets_binding` names the artifact's
  producing run in its header block (C089-7);
  `write_assignment_sets` refuses an unbound artifact;
  `materialization_record` composes the execution's
  run record.
- **`tools/ledger/run_settling.py`** — `run` mints the
  id at execution start, before any results exist
  (D-089-1), writes the record, appends the index
  `entry` act, and — where the run re-derives a stored
  record's basis — appends a `supersedes` act naming
  the latest non-superseded same-basis predecessor
  (basis = scenario + candidate + scope, what the
  retired filename hashed; chains stay linear under
  the fold's single-successor rule). `materialize-sets`
  executes as a run (binding + materialization record
  + entry act). An execution that **refuses** or
  **crashes** writes an absence record (run-defs
  §3.2: kind `refused` / `crashed`, the detail naming
  the defect) plus its entry act — never a half-written
  result. `compare` and `verify-canonicals` are
  behaviour-unchanged; the canonical recomputations
  carry ephemeral headers in memory and write nothing.
- **`glossa-indus/ledger/runs/run-index.jsonl`** — the
  store's run index, built in this stage over the
  standing T405 pair by legacy entries (the pair is
  neither renamed nor rewritten, C089-17; their bytes
  carry no header — pre-spec records stay pre-spec).
  The full legacy enumeration from git history is
  S5's completion (T501); S2's index covers what
  stands in the store.
- **`backend/tests/test_settling_run_scoped.py`** —
  the stage's teeth (T201–T203): **13 tests**, on tmp
  mirror trees throughout.

## Evidence

Targeted modules on the clean tree (glossa-ci venv,
TMPDIR on disk): test_run_records 52 + test_settling_
canonical 13 + test_settling_run_scoped 13 = **78
passed**.

Full backend suite, no `-x`, read from its log file
(`~/workspace/glossa-run/tmp-suite/089-s2-fullsuite.log`),
deselecting only the documented phase392 local-stall
test:

```text
2 failed, 2624 passed, 106 skipped, 1 deselected, 1 error in 704.36s
FAILED tests/test_phase133_stage0_inventory.py::test_builder_recomputation_skips_without_inputs
FAILED tests/test_run_records.py::test_t104_dry_run_over_standing_store
ERROR tests/test_tray_token_auth.py::test_copy_api_token_without_tkinter_is_named
```

- The phase133 failure is the environmental baseline.
- The ERROR is the tray-teardown flake family, on the
  exact test id run-defs v1 registers as the suite's
  nondeterminism shape #1 — a local-suite observation,
  not a CI verdict.
- The T104 failure is this stage's own doing, found by
  the enumeration and repaired in this PR: S1's dry-run
  test closed by asserting the copied store contains
  exactly the standing record files, a premise that
  expired when this stage built the store's run index.
  The enumeration itself is unchanged; the assertion
  now states the invariant it always meant — the copy
  gains no file from the derivation — and the module
  passes 52/52 after the repair (in the 78 above).
- 8 of this stage's 13 tests carry the clean-tree
  precondition guard the canonical oracle uses (the
  recorded-source-hash arm); in the full-suite process
  the evidence-API tests ran first and rewrote mirrored
  sources in-tree, so those 8 **skipped with the cause
  named** (verified by a two-module reproduction run:
  34 passed, 8 skipped, the skip reason naming the
  rewritten files). Standalone on the clean tree all
  13 pass. The skipped delta against S1's enumeration
  (98 → 106) is exactly those 8.

Ruff over `backend/`: **all checks passed**. (The CLI
file under tools/ carries its 2 pre-existing findings,
unchanged; this stage added none.) The suite's in-tree
regenerations were restored before committing;
`verify-canonicals` through the CLI still reproduces
**6/6** and writes nothing (a tooth asserts the store,
index included, is hash-unchanged across it).

Ledger gate on the final tree, verbatim summaries —
the standing profile, unchanged, with the index
present and V8's legs comparing result blocks as
before:

```text
full:    summary: 25 PASS / 0 FAIL / 1 NOT-RUN   RESULT: PASS
--regen: summary: 28 PASS / 0 FAIL / 0 NOT-RUN   RESULT: PASS
```

Teeth of record (tmp mirrors): the same scenario run
twice → two records, distinct ids, byte-equal result
blocks, the first record byte-identical after the
second run, the index folding 2 entries + exactly 1
supersedes act; a third run supersedes the second
(linear chain, census 3); a mutated ledger pin → the
constitutive key diff against the unmutated run is
exactly `input_pins`, and within it exactly the
ledger component (sha differs, lines +1, the other
three pins equal); a repeated minted-id write and a
hand-placed colliding file both refuse with the
existing bytes preserved; a refusal before state load
leaves an absence record with an empty input-pins key
(no pins exist to record), a refusal after load
carries the state's pins verbatim, a crash
(malformed-JSON candidate) leaves a `crashed` absence
record and no result block; materialize-sets stamps
the binding, lands its run record naming the artifact
and its bytes' SHA-256, and leaves the artifact's
content (modulo the binding) byte-equal to the prior
materialization.

## Claims discharged at this stage (per plan.md Stage 2)

- **C089-1 (write-path side)** — settling executions
  mint at start (a refusal/crash still receives its
  id and its absence record); ids name executions —
  two identical-basis runs carry different ids.
- **C089-2** — the content-addressed overwrite is
  retired on the write path: a same-basis rerun
  writes a new record under its own id, the prior
  record is preserved byte-untouched, and the
  supersession is a labeled index act with the
  superseded record remaining in the store.
- **C089-5** — a settling run's writes are exactly
  its run record (under its run id) and its index
  acts; the store census is monotonic across the
  seeded sequence; materialize-sets is a run whose
  record names the regeneration.
- **C089-7 (assignment-sets side)** — the artifact
  names its producing run in its header block, and
  the write path refuses an unbound artifact.
- **C089-17 (standing-pair side)** — the T405 pair is
  covered by legacy index entries under the partial
  label; its bytes are untouched and headerless, and
  the retired filename function still resolves its
  standing paths.

## Departures and judgments, stated plainly

1. **Supersession trigger.** plan.md Stage 2 assigns
   `supersedes` acts to "canonical re-derivation acts
   that supersede a stored record" without naming the
   trigger mechanically. This stage registers the
   trigger as: any `run` execution whose basis
   (scenario + candidate + scope) equals a stored
   result record's basis supersedes the latest
   non-superseded such record, with the executing run
   named in `ref`. A plain rerun is therefore a
   re-derivation act on this surface; runs over new
   bases supersede nothing. The adoption-refresh
   pattern (a rerun over moved pins superseding the
   T405 pair, under their legacy ids) is the same
   rule reaching the legacy entries.
2. **The standing assignment-sets.json is not
   re-materialized in this stage.** Its bytes feed the
   gate's derived stamps; stamping a binding onto it
   now would move those stamps and force a republication
   this stage does not otherwise need. It gains its
   producing-run binding at the next materialize-sets
   execution, and stands until then as a pre-machinery
   artifact — the same index-only honesty the T405
   pair carries, stated here rather than silently.
   The byte-determinism test now compares the artifact
   modulo the binding, which is the post-S2 invariant.
3. **Comparison records carry no run header in S2.**
   `compare_runs` output is a comparison record, not
   a run record; no write path stores one in this
   stage, and its sides' identities remain the
   candidate ids + pins as before. If a later stage
   stores comparisons, they bind then.
4. **Absence records before state load.** Where an
   execution refuses inside `load_state`, no pins
   exist; the absence record's key carries the empty
   input-pins object and the record carries no `pins`
   block. That is a degenerate key by necessity, named
   in the record's absence detail via the refusal
   itself — the alternative (no record) is the one
   C089-1's falsifier names.
5. **code_version fallback.** The CLI derives the
   key's code version from `git rev-parse HEAD` at
   the executed root; a non-git tree (a tmp mirror)
   records `unknown` — recorded, never invented.
   Code version is recorded-and-diffed, never
   constitutive (D-089-4), so the fallback cannot
   manufacture or mask comparability.
6. **Existing tests updated for the header contract:**
   the canonical module's determinism test now passes
   one fixed header to both evaluations (determinism
   is over identical inputs including the header);
   its write-surface test builds its record under a
   minted non-ephemeral header; its materialization
   test compares modulo the binding (item 2); S1's
   T104 test's store-shape assertion is restated
   (Evidence, above). No assertion was weakened: each
   restated form asserts the invariant the original
   named, under the store discipline this stage adds.
7. **V9 writer census.** `run_records.append_act` is
   now exercised by the settling CLI (a tools/ module,
   outside the gate's settling/scenario import audit);
   registering the library's write entry points with
   the census remains S5's act, exactly as plan.md
   Stage 1 assigns. The gate's standing profile is
   verified unchanged above.

## Stage 2's "does not establish" lines (from tasks.md)

- T201: *This does not establish: that the engine's
  results changed — result blocks are byte-compared
  against the pre-stage canonical expectations
  throughout (T202).*
- T202: *This does not establish: that canonical
  expectations are correct — only that the store
  discipline changed nothing they measure.*
- T203: *This does not establish: junction behaviour —
  S3 consumes the key diffs proven here; this task
  proves the raw material exists.*

**AI disclosure:** executed by an AI agent (Muse, via
Muse) at the direction of Tristen Pierson, per
constitution sec. VI.
