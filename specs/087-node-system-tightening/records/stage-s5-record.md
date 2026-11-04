# Spec 087 — Stage S5 record (Logs surface)

- Stage: S5 — Logs surface (tasks T501–T505)
- Branch: `feat/087-s5-logs` (tasks.md names the PR
  `feat/087-s5-logs-surface`; the parent's build brief directed
  `feat/087-s5-logs` and the brief governs), base main `7131a43a`
- Date: 2026-11-03
- Seat: build worker (parent gates and merges)
- Claims answered: C087-10, C087-11, and the S5 leg of C087-15

## 1. What was built

The Logs view Spec 081 removed, restored against the endpoints
that never went away (audit F6). No new backend endpoint, no new
storage, no persistence added.

- `frontend/src/components/LogsView.tsx` — the view, two tabs:
  - **Live stream.** First load `getLog(200)`; then the SSE tail
    via the new `streamLogLines` wrapper in `api.ts`
    (fetch-streamed with the stored token, never EventSource —
    Spec 082). The endpoint's 100-line backfill is buffered and
    merged into the first load by suffix/prefix overlap
    (`mergeLogLines`) so no line is doubled. Level filter is
    client-side over the fetched/streamed lines (All / DEBUG /
    INFO / WARNING / ERROR; CRITICAL rides the ERROR chip; the
    file's frontend-intake vocabulary WARN is normalized to
    WARNING — the file carries both spellings for one level).
    Pause buffers live lines and resumes flush them; autoscroll
    follows the tail while live and unpaused. The toolbar
    carries the source-file state from the `getLog` response
    (file name, exists, total lines) plus the rotation fact
    from `log_setup.py` (10 MB × 5 backups). The viewer holds
    at most 5,000 lines (an implementation bound, named here;
    the file is untouched). "Download last 200 lines" saves the
    held tail as text.
  - **Purge (Q2 as ruled: ship with confirmation).** "Purge
    log…" opens the confirmation state before anything is
    sent; opening it refreshes the line count (`getLog(1)`).
    Confirming calls `purgeLog()` exactly once; the result is
    reported and the view reloads. Cancel sends nothing. The
    e2e spec counts the endpoint calls through the whole
    sequence (0 on open, 0 on cancel, 1 on confirm).
  - **Job & phase records.** One read-only log over the
    existing API surface: `listJobs` + `getJobResults` (lazy,
    on expansion), `listPhaseActions` (new thin wrapper over
    `GET /phase/actions`), `listNotificationLog`. Unified
    rows (Started UTC / Record / Kind / Status / Duration /
    Summary), kind chips per the wireframe (All records,
    Experiment graphs, Pipelines, Studies, Phase actions,
    Notifications), status chips (Any status / Completed /
    Failed / Running), the most recent 50 shown, and
    per-record detail expansion rendering the record's own
    stored fields — a failed phase action's `error_message`
    verbatim, a job's params + the `job_results` payload
    excerpt, a notification's fields with the recipient
    masked. No control on this tab mutates a record.
  - **Error states (the S1/F5 lesson, from birth).** A failed
    first load on either tab renders a named error state
    (`data-testid="logs-error"`, role=alert) with Retry —
    never a silently empty surface. The stream's later
    disconnect degrades to a "Not live" indicator with the
    fetched lines intact.
- `frontend/src/App.tsx` — Q1 as ruled: a "Logs" entry
  (icon ≣) in the Tool home group between Jobs and Status;
  tab id `logs`, tab label, render switch. The command
  palette picks it up from the same item list.
- `frontend/src/api.ts` — `streamLogLines` (above) and
  `listPhaseActions` + the `PhaseAction` type.
  `getLog`/`getLogStreamUrl`/`purgeLog` were already present
  (F6) and are unchanged.
- T503 leg — `backend/glossa_lab/api/events.py`: the D2
  documented-ephemeral statement now stands in the module
  docstring (the user-manual and HelpView statements landed
  with S4). `backend/tests/test_spec087_events_doc.py` pins
  the statement's phrases on all three surfaces and the emit
  behaviour (no replay to a later subscriber; drop on a full
  queue).
- Manual (C087-15) — `docs/user-manual.md` and HelpView's
  mirrored text: the Logs sections rewritten from "no in-app
  log viewer" to the shipped view (both tabs, the purge
  confirmation's true contents, read-only records), a Logs
  row added to each view table, and the D2 statement carried
  unchanged in both.

## 2. Wireframe comparison (T504)

Served identity asserted first, from the serving backend
itself: `GET /api/v1/health` →
`{"status":"healthy","version":"0.1.0","component":
"glossa-lab-backend","build":"2557214-s5-worktree",
"auth":"token"}` — the build stamp is this branch's head
commit at capture time, served by a throwaway backend (own
data dir on port 8011; port 8001 on this VM is the live
desktop forwarder and was never touched by this stage).
Seed data: two jobs created and completed through the API,
one phase-action row and one notification row inserted into
the throwaway DB, log lines from the backend's own logging
plus three frontend-intake posts. Shots in
`records/stage-s5-shots/` (stream/records × desktop1440/
mobile390), compared screen by screen against
`records/logs-view-wireframes/wireframes/shots/`.

Matches: Logs entry between Jobs and Status; page head and
per-tab ledes as drawn; both tabs; live indicator + tailing
line naming the SSE endpoint; Pause / Download / Purge
controls; level chips; source-file state line (the endpoint
returns `logs/glossa.log` and the built toolbar shows exactly
the drawn facts); dark stream panel with timestamp / level /
logger / message columns in the drawn colours; records
filter chips (both rows); the census line's shape with live
numbers; the six-column table; detail expansion under the
row; status colours; read-only stated on the surface;
mobile: the surface reachable through the shell's drawer,
toolbar and chips wrap, the records table scrolls
horizontally as the wireframe's own table does at 390.

Differences, named (data governs):
1. **Purge facts.** The wireframe's confirmation says purge
   returns `{cleared: <lines>}` and "lines already rotated
   into backups are not touched". The endpoint's truth
   (`backend/glossa_lab/api/terminal.py::purge_log`):
   `cleared` is the truncated byte count, and purge DELETES
   all rotated backups. The shipped confirmation states the
   true behaviour (current file truncated, rotated backups
   deleted, cannot be undone); the confirm button keeps the
   drawn "Purge N lines" form with N the current line count
   from the API. A confirmation that misstates a destructive
   action was not shippable as drawn; the design (control +
   confirmation naming the effects + count before the act)
   is otherwise exactly as approved.
2. **Kind labels for jobs** are derived from the API's
   fields (id suffixes `-graph-run` / `-pipeline-run` /
   `-study-run`, else the `pipeline` value — JobsView's
   `exp_run` precedent). A job matching none of the three
   kinds shows its pipeline name as its kind label and
   appears under All records (the live shots show a real
   `discovery_fetch` job labelled so).
3. **Job duration and detail fields** come from the jobs
   table's actual columns: duration is `updated_at −
   created_at`; the detail line shows created/updated, not
   the wireframe's started/completed/error_message (the jobs
   table has no such columns; `phase_actions` does, and its
   detail shows them).
4. **Timestamps** render in the file's stored format
   (`2026-11-04 02:24:13,888`, UTC per `log_setup.py`) rather
   than the wireframe's ISO-Z sample format; record times
   render as UTC `YYYY-MM-DD HH:MM:SS` as drawn.
5. **Status filter mapping** across record kinds: Completed
   matches `completed` and `sent`; Failed matches `failed`;
   Running matches `running` and `pending`; `cancelled` /
   `skipped` appear under Any status only. The wireframe
   draws the chips but does not specify the cross-kind
   mapping.
6. **The seeded graph job's stored result** in the shots is
   the job runner's own error payload ("Unknown pipeline:
   exp_run") — the throwaway backend executed the API-created
   job and stored its result, which the detail renders
   verbatim. That is the surface working as specified
   (stored records, unedited), not a view defect.
7. The stream tab's secondary "Open Status" affordance sits
   under the stream panel (the PageHead's primary slot
   carries the drawn per-tab button: Open Status on the
   stream tab, Open Jobs on the records tab, as drawn).

## 3. Tests

- Backend, Spec 087 + Spec 086 + terminal targeted set:
  **429 passed, 2 skipped, 2185 deselected** (includes the
  5 new pin tests).
- Backend, full suite, one run: **2,530 passed, 84 skipped,
  1 failed, 1 deselected** in 285.32s. The deselection is
  the named phase392 determinism test. The one failure is
  the named phase133 local-only baseline,
  `test_phase133_stage0_inventory.py::
  test_builder_recomputation_skips_without_inputs`
  (missing local download; green in CI). No other failure;
  no tray teardown error in this run.
- Frontend build: `npm ci` + `npm run build` green (tsc
  clean, vite built); `frontend/dist` rebuilt and committed
  per repo convention.
- Playwright, local, against the served app on the
  throwaway backend (CI-mode env): `e2e/logs.spec.ts`
  **5 passed**; `e2e/navigation.spec.ts` **24 passed** (its
  tool-group enumeration gained Logs — the approved surface
  addition, not a weakened assertion); `status.spec.ts` +
  `program-home.spec.ts` + `jobs.spec.ts` **25 passed, 1
  flaky** (a status loading-timing test, passed on retry;
  the spec is untouched by this stage). CI runs the full
  e2e suite; locally the remaining specs were not run.

**Correction (2026-11-03, post-delivery, before merge).**
As first written, this section reported a targeted-set
figure of 761 passed and a full-suite result of 2,517
passed with the single failure in
`test_indus_evidence_api.py::
test_hypotheses_carry_the_governing_record_citation`,
attributed to the in-tree rewrite interaction, the file
green standalone at 29 passed, and the phase133 baseline
absent. Those figures were taken from a background
completion delivery instead of the run's own process log
and are wrong; the failure they describe never occurred
in the suite run. The build worker caught the error on
re-reading the process log and reported it before merge.
The figures above are the log's: targeted 429 passed,
2 skipped, 2185 deselected; full suite 2,530 passed, 84
skipped, 1 failed (the phase133 baseline named above), 1
deselected, in 285.32s. The correction pass then
independently re-verified both, from its own runs: the
targeted set re-ran to the identical result (429 passed,
2 skipped, 2185 deselected), and a full-suite re-run
reproduced the same single failure (phase133 baseline)
with 2,531 passed, 84 skipped, 1 deselected, plus one
ERROR — the known tray teardown flake,
`test_tray_token_auth.py::
test_copy_api_token_without_tkinter_is_named` at teardown
— in 1745.57s on a heavily loaded VM. The standalone
29-passed re-run of `test_indus_evidence_api.py` was
real, but it was diagnosing a failure the suite run never
had; that narrative is withdrawn. No other section of
this record is affected, and no claim assessment rests on
the corrected figures.

## 4. Claim assessments

- **C087-10 — SUPPORTED AS SPECIFIED.** The Logs surface
  ships with both wireframe tabs over the named endpoints,
  read-only records with detail expansion, placement and
  purge as ruled, verified by the Playwright comparison in
  §2 and the e2e spec. Its falsifier's terms — a missing
  tab, control, or field; a records tab that can mutate; a
  failed comparison reported as done — do not hold: the
  comparison's differences are the seven named items in §2,
  of which item 1 is a correction of the wireframe's own
  factual error against the endpoint it names, recorded
  here rather than absorbed.
- **C087-11 — SUPPORTED AS SPECIFIED.** One statement, three
  surfaces in agreement (events docstring, user manual,
  HelpView), pinned by `test_spec087_events_doc.py`
  including the two behaviour legs (no replay; drop on
  full). The emit path's code matches the statement —
  in-memory queues, `QueueFull` dropped in `emit_event`.
- **C087-15 (S5 leg) — SUPPORTED AS SPECIFIED.** The manual
  updates ride this PR: Logs sections in both manual
  surfaces describe the shipped view; no manual surface
  still describes a Logs panel that does not exist or a
  viewer that has not landed.

## 5. Departures and residuals, stated plainly

1. The purge-confirmation text correction (§2 item 1) is
   the one place the build departs from the wireframes'
   literal text. It is a factual correction forced by the
   endpoint the wireframe itself names, and it is the
   parent's to send back if they judge otherwise.
2. Branch name: the build brief directed
   `feat/087-s5-logs`; tasks.md/plan.md name
   `feat/087-s5-logs-surface`. The brief governed.
3. Port 8001 on this VM is the live desktop forwarder, so
   local verification ran on port 8011 against a throwaway
   data dir; the live backend was only ever read (one health
   payload) and received no seeded data.
4. Deeper manual prose beyond the Logs sections was not
   re-audited in this stage (S4's standing residual, not
   enlarged by S5).
5. The full e2e suite and the full CI battery are the
   parent's gate; §3 states exactly what ran locally.

**AI disclosure:** executed by an AI agent (Muse, via
Muse) at the direction of Tristen Pierson, per
constitution sec. VI.
