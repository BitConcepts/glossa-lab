# Stage S1 record — Spec 089 (2026-11-04)

**Scope:** tasks.md Stage 1 (T101–T104): run-defs v1, the
run-record + run-index library, its teeth, and the legacy
dry-run over the standing settling store. Executed on
branch `feat/089-s1-run-identity` off origin/main
`0d23cb89`. No surface write path changes in this stage:
settling adoption is S2, the junction tool S3, the suite /
experiment bindings S4, gate class V11 + the legacy index
completion S5. The claims ledger is untouched (C089-18).

## What was built

- **`glossa-indus/ledger/RUN-DEFINITIONS.md`** — run-defs
  v1 (T101): the closed surface list (`settling`,
  `experiment`, `study`, `suite`) + the result-bearing
  test; the run-id format and minting rule (D-089-1); the
  run-record header incl. the absence block (closed kinds
  `empty` / `refused` / `crashed`); run-key v1 with the
  constitutive set of D-089-4 (surface, command/tool,
  input pins, seed constitutive; code version and
  environment class recorded-and-diffed) and the per-surface
  pin lists (settling: the record's existing `pins` block
  verbatim); the registered no-seed marker; per-surface
  determinism classes with the tray teardown flake
  registered as the suite's nondeterminism shape #1 (first
  registered instance
  `test_tray_token_auth.py::test_copy_api_token_without_tkinter_is_named`);
  the junction disposition vocabulary incl. the narrow
  mechanical explained case; the run-index act format
  (`entry` / `supersedes` / `quarantine` / `adjudication`)
  with its fold refusals; legacy id derivation
  (`legacy:<store-relative path stem>`) and the verbatim
  label `legacy — key partial`; the CI citation quadruple.
- **`backend/glossa_lab/run_records.py`** — the library
  (T102), the defs' machine copy: `_Minter` (remembers
  issued ids, redraws on collision) behind `mint_run_id` /
  `mint_junction_id`; header + key construction and
  validation per surface (`build_header`, `validate_header`,
  `build_key`, `validate_key`); record composition with
  exactly one outcome (`build_record`, `validate_record`,
  `validate_absence`); comparability by the key
  (`constitutive_diff`, `keys_comparable`); the index fold
  (`apply_act`, `fold_acts`, `fold_index`) and the single
  write entry point `append_act`, which validates an act
  against the folded state before writing — a refused act
  leaves the index byte-unchanged; legacy derivation +
  settling recovery (`legacy_run_id`,
  `legacy_entry_for_record`, `enumerate_legacy_entries`,
  read-only).
- **`backend/tests/test_run_records.py`** — the teeth
  (T103) and the dry run (T104): **52 tests**.

## Evidence

Targeted module (glossa-ci venv, TMPDIR on disk):
**52 passed**.

Full backend suite, no `-x`, read from its log file
(`~/workspace/glossa-run/tmp-suite/089-s1-fullsuite.log`),
deselecting only the documented phase392 local-stall test
(`test_phase392_q2_gate.py::test_pipeline_deterministic_under_seed`):

```text
1 failed, 2619 passed, 98 skipped, 1 deselected, 1 error in 252.72s
FAILED tests/test_phase133_stage0_inventory.py::test_builder_recomputation_skips_without_inputs
ERROR tests/test_tray_token_auth.py::test_copy_api_token_without_tkinter_is_named
```

The one failure is the phase133 environmental baseline.
The one ERROR is the tray-teardown flake family, on the
exact test id run-defs v1 registers as the suite's
nondeterminism shape #1 — named here per the standing
convention; it is a local-suite observation, not a CI
verdict. The passed count reconciles exactly: 2,567 (the
pre-stage enumeration of record) + 52 (this stage's module)
= 2,619. Ruff over `backend/`: **all checks passed**. The
suite's in-tree regenerations (`extracted_claims`,
`claim_reports`, `outputs/partial_loop_result.json`) were
restored before committing; the final tree carries only
this stage's files. No census literal moved; nothing was
re-pinned.

Ledger gate on the final tree, verbatim summaries (the
pre-change baseline, run on the pristine branch first,
was identical in full mode):

```text
full:    summary: 25 PASS / 0 FAIL / 1 NOT-RUN   RESULT: PASS
--regen: summary: 28 PASS / 0 FAIL / 0 NOT-RUN   RESULT: PASS
```

Dry run (T104): the enumeration recomputes from the
standing store at test time — the store's 2 records fold
under legacy ids with semantics, candidate, and the pins
block recovered verbatim, `code_version` and the execution
stamps named in `missing`, and the real store's bytes
hash-verified unchanged by the derivation.

## Claims discharged at this stage (per plan.md Stage 1)

- **C089-1 (format side)** — the id format, minting rule,
  and header are registered and implemented; 10,000
  same-second mints unique; no-result executions have a
  registered record form (the absence block).
- **C089-2 (format side)** — supersession is an index
  relation in the registered format; the fold refuses
  duplicate entries and double supersession. (Retirement
  of the settling overwrite itself is S2's write-path act.)
- **C089-9** — run-key v1 is registered with the D-089-4
  constitutive set; comparability is computed from the key
  alone (code-version / environment differences shown
  non-constitutive; pin and seed differences named).
- **C089-17 (format side)** — legacy id derivation and the
  partial label are registered and proven over the standing
  store; legacy bytes are never written by the machinery.
- **C089-19** — determinism classes are registered per
  surface in run-defs v1 §5, the tray-flake shape first.

## Departures and judgments, stated plainly

1. **Branch name.** plan.md labels the S1 PR branch
   `feat/089-s1-run-defs`; this stage executed on
   `feat/089-s1-run-identity` as the stage brief directed.
   Stage content is the plan's, unchanged.
2. **The `study` surface's determinism class.** The plan's
   S1 determinism list names settling, the generated-layer
   builders, the suite, and backend jobs; the closed
   surface list also includes study re-executions, and
   C089-19 forbids citing a surface with no registered
   class. run-defs v1 §5 therefore registers `study` as
   **deterministic** under the freeze record's fixed pins
   (the freeze-gate C2 recomputation precedent). This is a
   registration completion, flagged for the stage
   reviewer's ruling under T101's human-as-oracle
   acceptance; it settles no judgment row.
3. **Mint uniqueness is a minter rule, not a property of
   the format.** Six hex characters cannot make 10,000
   same-second random mints unique by chance (the birthday
   bound gives ~3 expected collisions), so run-defs v1 §2
   registers the operative rule: the minter remembers the
   ids it has issued and redraws on collision (proven by a
   seeded-collision test), and cross-process uniqueness
   rests on the store write path's collision refusal,
   which is S2's act as the plan assigns.
4. **V9 writer census.** `run_records.py` carries a write
   entry point (`append_act`) but writes no gated artifact
   and matches none of the gate's V9.3 artifact patterns,
   so the gate's standing profile is unchanged (verified
   above, both modes). Registering the entry point with
   the census is S5's act, exactly as plan.md Stage 1
   assigns; run-defs v1 §9 names it as owed.

## Stage 1's "does not establish" lines (from tasks.md)

- T101: *This does not establish: that the key's
  constitutive set is right — only that it is the ratified
  one, registered where amendments must go.*
- T102: *This does not establish: that any surface uses it
  yet — adoption is S2–S4; this task proves the formats
  and the fold.*
- T103: *This does not establish: behaviour over real
  stores — that is T104's dry-run and S2's adoption.*
- T104: *This does not establish: the legacy treatment of
  records no longer in the store — that enumeration from
  git history is S5's completion.*

**AI disclosure:** executed by an AI agent (Muse, via
Muse) at the direction of Tristen Pierson, per
constitution sec. VI.
