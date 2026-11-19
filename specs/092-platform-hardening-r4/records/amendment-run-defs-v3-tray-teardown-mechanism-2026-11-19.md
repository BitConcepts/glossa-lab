# Amendment — run-defs v3: the tray teardown mechanism recorded (2026-11-19)

**Spec 092 lineage.** This record is the amendment act
for the run definitions under D-092-3: it registers
**run-defs v3**, propagated in this same landing to
every registered copy (run-defs §9):
`glossa-indus/ledger/RUN-DEFINITIONS.md`, the library's
machine copy (`backend/glossa_lab/run_records.py`), and
the gate's V11 copies (`backend/glossa_lab/ledger_gate.py`).
Nothing else in the definitions changes: v3 carries v2
verbatim except §5's suite shape #1, which now records
the mechanism and the fixing stage, and the version
strings and citations in the copies. The shape's
definition — its confinement — is unchanged, and the
entry is not deleted (D-092-3). The comparability
judgment row (§4) is untouched. Citations that name an
earlier version as the origin of a rule or a record
(the claims ledger's entries, the study tools'
docstrings, `tools/ledger/build_legacy_index.py`'s
departed-generation origin citation, the legacy-index
tests' v2 case name) are historical and do not move.

## The mechanism (Spec 092 T301)

Shape #1's divergence — teardown ERROR entries of the
sqlite closed-database family on tray test ids — is the
application lifespan's shutdown racing the engine loop:

- The suite's session-scoped app context runs the real
  lifespan. At context exit the lifespan cancels its
  tasks and closes the database (`close_db()`).
- The engine loop is a fire-and-forget task. If it is
  still working a job when the database closes, its next
  store raised `sqlite3.ProgrammingError` ("Cannot
  operate on a closed database"); the loop task ended on
  the exception, unretrieved, and pytest attributed the
  session-fixture teardown error to the session's
  then-final test.
- In the first registered instance (2026-11-04) that
  final test was
  `test_tray_token_auth.py::test_copy_api_token_without_tkinter_is_named`.
  The tray test modules use no TestClient and no
  database; the attribution is pytest's, not the tray
  tests' doing.

## The fixing stage

The engine shutdown-race work of 2026-11-06/07, which
predates this registration: PR #541 (commit `df592cf9`)
made the engine loop stop cleanly when its database
closes under it, and PR #544 (commit `07cbad59`) made
the judgment against the loop's captured Database
instance rather than the replaceable global singleton,
after the failure's second face in the 2026-11-10 CI
runs (42729580150, 42731318567). `Database.close()` is
tolerant, and the lifespan's fire-and-forget tasks carry
broad exception guards.

## Evidence

- The regression battery
  `backend/tests/test_engine_shutdown_race.py` drives
  the exact interleavings. Run at Spec 092 Stage 3
  against the pre-fix tree (commit `62408c65`, the
  parent of the first fix): **2 failed, 1 passed**, the
  failures surfacing `sqlite3.ProgrammingError: Cannot
  operate on a closed database.` Run against the fixed
  tree: **3 passed**.
- A suite-order segment ending in the three tray test
  modules, six repetitions: 137 passed each, zero
  teardown ERRORs, zero closed-database text.
- The backend job logs of the three most recent
  completed CI runs before this amendment (44597736868,
  44611181092, 44613107408, 44615240763) contain zero
  "ERROR at teardown" and zero "Cannot operate on a
  closed database".
- Discharge (T302): five consecutive full-suite runs
  with zero teardown ERRORs of this family, named by
  run id in the Spec 092 stage-3 record.
