# Spec 092 Stage 3 record — suite determinism (2026-11-19)

Stage 3 of Spec 092 (platform hardening R4): the four
suite-determinism legs. Each leg landed on its own PR
against main, merged only on per-job CI green (10 jobs,
read per job). The stage's evidence is stated per task;
the closeout record carries the per-claim dispositions.

## T301 — Tray teardown: reproduced, root-caused, fixing stage named

**Discharged (C092-9's mechanism leg).** The registered
shape (run-defs §5, suite shape #1) confined the family
to teardown ERROR entries of the sqlite closed-database
family on tray test ids. Established at this stage:

- The three tray test modules use no TestClient and no
  database. The registered first instance
  (`test_tray_token_auth.py::test_copy_api_token_without_tkinter_is_named`)
  sits at the end of its file — the attribution pattern
  of a session-fixture teardown error, which pytest
  reports against the session's then-final test.
- The mechanism is the application lifespan's shutdown
  racing the engine loop: on app-context exit the
  lifespan closes the database while the fire-and-forget
  engine loop is still working a job; the loop's next
  store raised `sqlite3.ProgrammingError` ("Cannot
  operate on a closed database"), the loop task ended on
  the unretrieved exception, and the error surfaced at
  session teardown.
- The fixing stage predates this spec: the engine
  shutdown-race work of 2026-11-06/07 (PR #541, commit
  `df592cf9`; PR #544, commit `07cbad59`), which made
  the loop judge closed-database signals against its
  captured Database instance and stop cleanly, made
  `Database.close()` tolerant, and guarded the
  lifespan's fire-and-forget tasks.
- Reproduction, on demand: the regression battery
  `backend/tests/test_engine_shutdown_race.py` run
  against the pre-fix tree (commit `62408c65`, the
  parent of the first fix) fails 2 of 3, the failures
  surfacing the ProgrammingError; against the current
  tree it passes 3 of 3.
- A suite-order segment ending in the tray modules, six
  repetitions: 137 passed each, zero teardown ERRORs,
  zero closed-database text. The backend logs of the
  four most recent completed CI runs before this stage
  (44597736868, 44611181092, 44613107408, 44615240763)
  contain zero "ERROR at teardown" and zero "Cannot
  operate on a closed database".

No residual source fix was identified at this stage:
the family's source was already fixed, and this stage's
work was the establishment, the amendment act (T302),
and the discharge battery. Nothing was changed on
speculation.

## T302 — Discharge + shape amendment (D-092-3 act)

**Discharged.** The §5 amendment landed as run-defs v3
(PR #600, merge `5ca4fcd745c219e674d395862daacdbe3f574020`),
propagated in the same motion to every registered copy
per §9 (RUN-DEFINITIONS.md; `run_records.py`;
`ledger_gate.py`), with the amendment record at
`records/amendment-run-defs-v3-tray-teardown-mechanism-2026-11-19.md`.
The shape entry is amended, not deleted; its confinement
is unchanged.

The discharge battery: five consecutive full-suite runs
on the final tree (commit `5ca4fcd7`), each in its own
worktree on the mini-server, standard enumeration, logs
preserved with this record's working papers:

| Run | Window (ET) | Result |
|---|---|---|
| discharge-1 | 2026-11-19 18:17:25 → 18:24:28 | 3085 passed, 23 skipped, 1 deselected, exit 0 (412.87 s) |
| discharge-2 | 2026-11-19 18:17:25 → 18:23:01 | 3085 passed, 23 skipped, 1 deselected, exit 0 (325.46 s) |
| discharge-3 | 2026-11-19 18:17:25 → 18:23:01 | 3085 passed, 23 skipped, 1 deselected, exit 0 (325.49 s) |
| discharge-4 | 2026-11-19 18:28:26 → 18:33:52 | 3085 passed, 23 skipped, 1 deselected, exit 0 (319.16 s) |
| discharge-5 | 2026-11-19 18:28:26 → 18:34:27 | 3085 passed, 23 skipped, 1 deselected, exit 0 (353.25 s) |

Each run: zero "ERROR at teardown" lines, zero "Cannot
operate on a closed database" lines. These same five
runs are T305's full-suite-order battery (below) and
T304's post-leg local enumeration (below).

## T303 — In-tree rewrites eliminated; the clean-tree guard removed

**Discharged (C092-10).** PR #596, merge
`8af69a6ff59c164a99a7eac89d600c67d5123cb1`; CI 10/10
per job on the merged run (44628251641).

Attribution (isolated module runs, tree restored before
each): `test_indus_evidence_api.py` rewrote all ten
`glossa-indus/claims/extracted_claims/*.json` plus the
batch4 claims report, because `POST /intake/run` queues
`_run_full_intake` as a background task and the runner
subprocess-ran the glossa-indus scripts over the real
tree (the experiment-graph intake runner is its twin);
`test_research_loop.py`, `test_research_loop_deep.py`
and `test_study_loop.py` each rewrote
`outputs/partial_loop_result.json` through the research
loop's partial-results writer.

The fix is two seams, each defaulting to the production
path when unset: `GLOSSA_INDUS_SCRIPTS_DIR` (honored by
both intake runners; the scripts locate their base from
their own path, so the suite's conftest fixture tree —
the real scripts symlinked under `scripts/`, the data
dirs empty temp dirs — absorbs every write) and
`GLOSSA_OUTPUTS_DIR` (honored by the partial-results
writer). The clean-tree precondition guard is removed
from the three run-scoped test files
(`test_settling_run_scoped.py`, `test_settling_canonical.py`,
`test_run_junction.py`); in `test_spec086_ledger_gate.py`
the same-named helper is a tested subject of that file's
own battery (its teeth test asserts it trips on a dirty
scratch tree) and stays, inert in-suite now that the
precondition holds by construction.

Verification at the leg: the rewriting modules plus the
three guard-carrying modules, 115 passed, 0 skipped,
post-run tree clean. At the stage: each discharge run's
post-run `git status` is empty over the whole tree, and
each run's count of "clean-tree precondition" skip
lines is zero.

## T304 — phase392 profile + registered outcome

**Discharged (C092-11).** PR #598, merge
`889f4363d3fd5482dc73901bce84c27a01fd975c`.

Profile (mini-server, standalone): the determinism test
completes in ~49 s (module total 49.32 s, 2 passed,
1 skipped). A stack dump at 45 s sits in `bray_curtis`
(`scripts/phase392_q2_gate.py`) under `permanova` under
`run_pipeline` — 49 cells, a 588×12 input matrix, 199
bootstrap draws, 499 permutations, the dissimilarity
materializing a 588×588×12 array per draw. The cost is
intrinsic compute: no accidental Python-loop quadratic,
no retry loop, no unbounded wait. The tens-of-minutes
stall was observed 2026-11-05 on the Muse VM (shared
CPU, ~8 GB RAM, no swap); the mini-server has been the
execution home since 2026-11-16.

Under D-092-4's branch rule (intrinsic cost → registered
environment-scoped deselection, CI authoritative), the
outcome landed: RUN-DEFINITIONS.md §11 registers the
deselection (a registration in the §10 form; it amends
no rule and does not move the run-defs version), and
`backend/tests/conftest.py` collection deselects the
one test where the `CI` variable is unset. Verified
three ways at the leg: local collection 2/3 with 1
deselected; local collection with the standing manual
`--deselect` flag unchanged (2/3, no error); `CI=1`
collection 3/3. After the leg, each discharge run's
summary shows the test deselected by the wiring (1
deselected) with no hand-supplied flag and no stall.

## T305 — Notifications ERROR battery

**Closed UNREPRODUCED (C092-12), with the
automatic-reopening term.** The battery fixed by the
claim: 50 standalone repetitions of
`backend/tests/test_notifications_api.py` plus 3
full-suite-order runs, watching
`test_mask_email_redacts_local_part` (single ERROR
sighting 2026-11-01).

- Standalone: 50 completed repetitions, every one
  9 passed, the target test passing in each. (One
  further repetition's process was disrupted under box
  load and produced no test outcome at all; it is
  recorded as disrupted, not counted, and a make-up
  repetition — also 9 passed — completes the fifty.)
- Suite order: the five discharge runs above each
  include the notifications module in full-suite order;
  the target test passed in all five, with no ERROR.
- No reproduction occurred, so there is nothing to
  classify and no fix under T301's pattern.
- **Automatic-reopening term:** this closure reopens
  automatically, without any new commission, if the
  target test (or the notifications module) ever
  records an ERROR again in any suite run, local or CI;
  on reopening, the sighting is classified under
  T301's pattern before any other suite-determinism
  work proceeds.

## Out-of-scope defect found and repaired on the way

`test_spec086_map.py::test_builder_refuses_a_run_pinned_to_another_build`
was failing independently of this spec: it corrupted
only the first `*.json` a glob returned in its fixture,
while the map builder carries only
candidate/scenario/result-shaped records (2 of the 10
stored records), so whenever the glob landed on another
record no refusal could fire. It fails standalone on
unmodified main and was the sole backend failure on
PR #596's first CI run. Repaired minimally on its own
PR #597 (merge `6c7256d09966ee89119cd5e762fe10cf8c697bc5`):
the test now re-pins every pinned record in the fixture;
the assertion is unchanged; standalone 17 passed (was
16 passed, 1 failed).

## Flag carried from Stages 1–2

`backend/glossa_lab/privacy_statement.py` §2 still
describes the settings store as not encrypted. That
text is owner-approved policy text with its own change
process (its §7); Stage 2's record flagged the same
leftover. This stage does not change it, and the
closeout report flags it again: it is the owner's call,
through that process, whether §2 is updated to describe
the store as it now is.
