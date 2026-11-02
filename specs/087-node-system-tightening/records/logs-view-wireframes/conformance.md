# Conformance — Spec 087 Stage S5 wireframes vs the spec

How each wireframe satisfies Spec 087's Stage S5 scope
(spec.md §S5, claims C087-10 and C087-11), and what the S5
build tasks will verify against these screens.

## Wireframe 01 — Live stream

- **Endpoints named on the surface are the real ones.**
  `GET /terminal/log?lines=200` (the `getLog` contract:
  `{lines, total_lines?, exists}`), `GET /terminal/log/stream`
  (SSE tail), `POST /terminal/log/purge` (returns
  `{cleared, file}`), and the frontend error intake
  `POST /terminal/log/frontend` appears as a log line, which is
  where its output actually lands. Source: census §6.1–6.2.
- **Log lines are real-shaped.** Structured JSON logging with
  UTC timestamps, level, logger name, and message
  (`backend/glossa_lab/log_setup.py`); the rotation fact on
  the toolbar (10 MB × 5 backups) is the `log_setup.py`
  constant pair. The sample WARNING line is labelled on the
  screen as what it is — an illustration of the only signal a
  registration failure gives today, which Stage S1 addresses.
- **The purge confirmation is part of the design** (decision
  Q2), drawn in its shown state, not described in prose only.
- **Level filter is a client-side filter over the fetched /
  streamed lines**; no endpoint parameter is invented for it.

## Wireframe 02 — Job & phase records

- **The record kinds are the census's tables** (§6.3):
  `jobs` + `job_results` (experiment-graph, pipeline, and
  study runs), `phase_actions` (with its `status`,
  `error_message`, `started_at`, `completed_at`, `job_id`
  fields), and `notification_log` (status/error, recipient
  masked by the API). The expanded detail shows the `jobs`
  row's fields and an excerpt of the stored `job_results`
  payload — the record's own content, not a summary invented
  for the screen.
- **Counts are the live census's** (audit F8): 18 jobs, all
  completed; 1,230 reports, with the screen itself pointing at
  the Reports view for those.
- **Read-only is stated on the surface.** Acting on records
  stays in Jobs; this view never mutates a record (claim
  C087-10's boundary).

## What the S5 build verifies against these screens

Per Spec 087 tasks.md (Stage S5): Playwright renders of the
built Logs view at desktop 1440 and mobile 390 compared
against these wireframes screen by screen, with served
identity asserted before screenshots (the Stage 5 / Spec 086
precedent); component tests that the stream tab consumes
`getLog` + the SSE URL and that a failed fetch renders an
error state (the Stage S1 lesson of F5 applies to this new
surface from birth — no silent empty state); and an endpoint
test that purge is reachable only through the confirmation
state if Q2 is ruled (a).

## Explicit non-claims

- These wireframes do not establish that the endpoints behave
  under load, or that the SSE tail survives the cloud edge —
  S5's build verification covers the desktop surface these
  screens draw; the cloud surface is Spec 083's territory.
- Nothing here designs the events bus. Its disposition is
  Spec 087 decision D2 in spec.md; wireframe 01's sample line
  only states the current fact (in-memory only) so the owner
  sees it where it belongs.
