# Spec 087, Stage S5 — wireframes for the restored Logs view

**Status: DRAFT for Tristen's approval.** Nothing in this package
is approved until Tristen approves it in the Glossa-Lab chat.
This is the one approval point inside Spec 087 besides the spec
package itself (audit plan, S5). The S5 build does not start
before this approval; if the built surface later deviates from
the approved screens, the build stops and the deviation is
reported — it is never absorbed silently.

Format precedent: the Spec 086 Stage 5 wireframes package
(`specs/086-winning-combination-adoption/records/stage-5-wireframes/`).
Screens are static HTML wireframes sharing
`wireframes/wireframes.css` (copied unchanged from that package);
every screen carries an annotation block at the bottom (purpose ·
primary action · what changed and why · spec claims). Everything
on the screens is plain language, US English.

## What this package is

Audit finding F6: the terminal-log endpoints
(`GET /terminal/log`, `GET /terminal/log/stream`,
`POST /terminal/log/purge`, plus the frontend error intake
`POST /terminal/log/frontend`) are live and working, and
`frontend/src/api.ts` already carries the wrappers (`getLog`,
`getLogStreamUrl`, `purgeLog`) — but no component references
them since Spec 081 removed the bottom panel. The endpoints are
write-only in the current UI: the manuals still describe a Logs
panel the app no longer has. Stage S5 restores the viewer
against the existing endpoints; it builds no new backend.

The view has two tabs:

1. **Live stream** — the backend's JSON log (`glossa.log`,
   structured logging via `log_setup.py`, UTC timestamps),
   first loaded as the last 200 lines and then tailed over the
   SSE stream endpoint, with a level filter and the purge
   control behind a confirmation.
2. **Job & phase records** — the persistent records the
   database already keeps (`jobs` / `job_results`,
   `phase_actions`, `notification_log`; census §6.3), read as
   one log with per-record detail expansion. Read-only: Jobs
   remains the surface that acts on records.

Every number and label on the screens is real-shaped from the
2026-11-02 census: endpoint paths and response shapes from
`backend/glossa_lab/api/terminal.py` and `frontend/src/api.ts`
(`getLog` returns `{lines, total_lines?, exists}`; purge returns
`{cleared, file}`), the 10 MB × 5 backup rotation from
`log_setup.py`, the 18-jobs / 1,230-reports live counts from
audit finding F8, and the record fields from
`backend/glossa_lab/database.py`.

## Contents

| File | What it is |
|---|---|
| `wireframes/wireframes.css` | Shared wireframe stylesheet (the 086 package stylesheet, unchanged). |
| `wireframes/01-logs-stream.html` | Logs view, Live stream tab: live tail, level filter, source-file state, purge control with its confirmation state. |
| `wireframes/02-logs-records.html` | Logs view, Job & phase records tab: unified record list over the DB tables, one record shown expanded to its stored detail. |
| `wireframes/render-shots.py` | Render script (Playwright; desktop 1440 + mobile 390 screenshots into `wireframes/shots/`). |
| `wireframes/shots/` | The four renders, visually verified by the drafting worker before inclusion. |
| `decisions.md` | The two design questions the owner must rule on (Q1 placement, Q2 purge), each with a recommendation. Approval is by name, on these questions. |
| `conformance.md` | How each wireframe satisfies Spec 087's S5 scope and claims C087-10/C087-11, and what the S5 build will verify against these screens. |

## The decisions the owner is asked to make

Two questions, in `decisions.md`, each with a recommendation:

- **Q1 — Placement:** Logs as its own tab in the Tool home nav
  group (recommended) vs a panel inside the existing System /
  Status area.
- **Q2 — Purge:** ship the purge control in the UI behind its
  confirmation (recommended) vs make the view read-only and
  leave purge to the API.
