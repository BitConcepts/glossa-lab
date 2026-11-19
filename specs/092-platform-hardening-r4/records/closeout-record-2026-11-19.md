# Spec 092 closeout record (T401) — 2026-11-19

Spec 092 (platform hardening R4) closes here. Per-claim
dispositions C092-1..14 at stage-evidence strength, with
stage and PR pointers; the standing gate profile
restated verbatim from the gate's own output on the
final tree; C092-14 verified by diff census over the
spec's stage branches. Nothing below states a claim at
more than the strength its stage earned.

## Per-claim dispositions

- **C092-1 — Discharged** (Stage 1; PR #569, merge
  `3cb7382c`). Store format v2: credential values are
  AES-256-GCM envelope objects at rest; the plaintext
  settings file carries no credential value.
- **C092-2 — Discharged** (Stage 1; PR #569). Key
  custody per D-092-1: a 32-byte key in a 0600 file
  outside `{data_dir}`, operator-created, never logged.
- **C092-3 — Discharged** (Stage 1; PR #569). Named
  error states replace the legacy loader's silent empty
  store on a missing or corrupt store.
- **C092-4 — Discharged** (Stage 1; PR #569). First-load
  migration re-saves through the verified-write
  construction and compares value-by-value before the
  load returns; the original stays byte-untouched on
  any failure.
- **C092-5 — Discharged** (Stage 1; PR #569). The
  consumer contract battery passes identically against
  v1 and v2 stores, with no consumer diffs beyond the
  authorized database-init tolerance.
- **C092-6 — Discharged** (Stage 2; PR #572, merge
  `cc9f132a`). The verified-write library: a save either
  lands verifiably or leaves the prior state readable,
  under the fault-injection battery (T202).
- **C092-7 — Discharged, both legs** (store leg Stage 1,
  PR #569; library leg Stage 2, PR #572). A failed write
  never destroys the previous good target: the settings
  save path and the library's adopters keep the prior
  readable state on any failure, under the
  fault-injection battery.
- **C092-8 — Discharged** (Stage 2; PR #572). The write
  failure classes the fleet actually met are the seeded
  classes of the T202 fault-injection battery, and the
  battery passes against the library in CI.
- **C092-9 — Discharged** (Stage 3; PR #600, merge
  `5ca4fcd7`). The tray teardown family: mechanism
  established (lifespan shutdown racing the engine
  loop), fixing stage named (the 2026-11-06/07 engine
  shutdown-race work, PR #541/#544), reproduction
  battery failing 2 of 3 pre-fix and passing 3 of 3
  post-fix, and the T302 discharge — five consecutive
  full-suite runs with zero teardown ERRORs of the
  family. Detail: the stage-3 record and the run-defs
  v3 amendment record.
- **C092-10 — Discharged** (Stage 3; PR #596, merge
  `8af69a6f`). In-tree rewrites eliminated at the source
  (two env seams with production defaults; conftest
  fixture tree); the clean-tree guard removed from the
  run-scoped test files; each discharge run's post-run
  tree is empty and its guard-skip count is zero.
- **C092-11 — Discharged** (Stage 3; PR #598, merge
  `889f4363`). phase392: profiled (~49 s standalone,
  intrinsic compute in the Bray–Curtis dissimilarity
  under PERMANOVA); the registered outcome under
  D-092-4 landed — RUN-DEFINITIONS.md §11 plus the
  conftest collection wiring; CI remains the
  authoritative run of the test.
- **C092-12 — Closed UNREPRODUCED** (Stage 3; battery
  in the stage-3 record). 50 standalone repetitions and
  five full-suite-order runs produced no reproduction
  of the 2026-11-01 ERROR sighting. The closure carries
  the automatic-reopening term stated in the stage-3
  record: any future ERROR on the target test or the
  notifications module reopens it without a new
  commission.
- **C092-13 — Discharged** (Stage 2; PR #572; final
  form here). Every writer Stages 1–2 created or moved
  stands in the gate's V9 writer census, and the census
  the gate computes finds exactly the registered set —
  the V9 arm passes inside the standing profile
  restated verbatim below, which is this claim's final
  form.
- **C092-14 — Discharged, by diff census** (this
  closeout). Census over the spec's stage merges —
  Stage 1: `3cb7382c` (7 files) and `1c7c12e9` (3 files);
  Stage 2: `cc9f132a` (6 files); Stage 3: `8af69a6f`
  (8 files), `889f4363` (3 files), `5ca4fcd7` (7 files).
  No stage diff touches a claim's status, stage, or
  score; no verification token and no claim edge is
  touched; the Spec 082 install-token file is untouched;
  no UI surface changes. The one LEDGER.md diff in the
  census (Stage 1's record merge) is a pure append of
  that stage's dated journal entry — no existing entry
  edited. The adoption merge (#548) appended the C092
  claims themselves at intake, before any stage branch.
  The out-of-scope Spec 086 test repair (PR #597)
  touched one test file and nothing else.

## Standing gate profile on the final tree

From the gate's own output on the final tree (commit
`5ca4fcd745c219e674d395862daacdbe3f574020`), run
2026-11-19 through `tools/ledger/check_ledger_gate.py`:

- Header: "run definitions: run-defs v3 (the gate's
  registered copies)".
- `--all`: "summary: 29 PASS / 0 FAIL / 1 NOT-RUN" —
  "RESULT: PASS".
- `--regen`: "summary: 32 PASS / 0 FAIL / 0 NOT-RUN" —
  "RESULT: PASS".

The profile is the standing profile exactly as Stage
2's record restated it; the run-defs v3 amendment moved
no arm.

## Undischarged items and flags

- No claim is left undischarged. C092-12 closes
  UNREPRODUCED under its own terms (the claim's second
  named end state), with the automatic-reopening term
  in force.
- **Privacy statement flag (owner's call, unchanged by
  this spec):** `backend/glossa_lab/privacy_statement.py`
  §2 still describes the settings store as not
  encrypted — stale since Stage 1 landed credential
  encryption on 2026-11-14. The text is owner-approved
  policy text with its own change process (its §7);
  Stages 2 and 3 both flagged it rather than change it.
  Whether §2 is updated to describe the store as it now
  is remains the owner's decision through that process.
- The Muse VM full-suite stall that motivated C092-11
  is answered by the registered deselection (§11): the
  VM enumeration no longer needs a hand-supplied flag,
  and the CI backend job remains the authoritative run
  of the deselected test.

## Landing

This record, the stage-3 record, and the T302/T305/
T401 task ticks land on the closeout PR; the spec's
work is complete when that PR merges on per-job CI
green.
