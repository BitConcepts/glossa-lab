# Spec 081 — Step 1 inventory: the entire current UI

Taken 2026-10-29 from `origin/main` @ `f8827fb2` (frontend `frontend/src`, tray
`tray/glossa_tray`). This inventory is the "before" record the redesign answers.
Line counts are source-file sizes, given so the weight of each surface is visible.

## The shell (`frontend/src/App.tsx`, 974 lines)

- Fixed left sidebar, 220 px, navy `#1e3a5f`. Brand block: gradient tile
  (#2563eb → #60a5fa, white "G") + "Glossa Lab" / subtitle **"Indus Script
  Analysis"** — one program's subject is the shell's subtitle.
- ProjectSelector dropdown at the top of the sidebar, defaulting to
  **"All Projects (Global)"**, with an "ACTIVE" chip and "⚙ Manage Projects…".
- Top bar: breadcrumb (Glossa Lab / project chip / view), back/forward/home
  buttons, ⌘K palette button, bottom-panel toggle (Ctrl+J), notification bell,
  dark-mode toggle (localStorage `glossa_dark`, light default).
- Bottom IDE panel (desktop only): tabs Logs | Jobs | Terminal | Chat.
- AI side panel ("Glossa AI"), dockable left/right; full-screen modal on mobile.
- Mobile (≤768 px): bottom nav = Home / Discovery / AI / Reports / More
  (☰ opens the sidebar as a slide-over); 44 px touch targets; iOS zoom guards.
- HealthBadge: liveness only — Healthy/Degraded/Offline dot, polls `/health`
  every 6 s. No identity (what is answering), no observed-at time.
- Nav state dots: amber = unsaved changes, pulsing green = running, solid
  green/red = last run success/fail, pulsing blue = active jobs count.
- 21 tabs (type `Tab` in App.tsx), plus a legacy `exp-builder` alias and
  AI-navigation aliases (`indus-data` → dashboard, `studies` → builder,
  `foundation` → foundation-check, …).

## The 21 tabs

| Group | Tab | View (size) | What it does |
|---|---|---|---|
| Overview | Dashboard | DashboardView (1,638) | Counts header; AI Insight narrative card (localStorage-cached); RSS/discovery feed (14 d); top kinds/topics/sources; **embeds DeciphermentPanel and ResearchLoopPanel (2,975)**. Intentionally read-only. |
| Workflow | Corpora | CorporaView (1,039) | Corpus CRUD, import/export/copy/benchmark, catalogue import; per-corpus tabs Browse/Edit/Stats/N-grams/Concordance/AI; **AnchorSetEditor buried inside at ~line 869** (list/create/delete; create takes name + language + pairs). |
| Workflow | Experiments | ExperimentBuilderView (1,555) | ReactFlow canvas, typed nodes with colored ports (sequences #059669, freq_map #2563eb, profiles #7c3aed, clusters #d97706, number #dc2626, text #0d9488, json #4f46e5, any #64748b); saved graphs feed the Study Builder palette. Full-height canvas. |
| Workflow | Pipelines | PipelinesView (623) | Gallery of registered pipelines from the backend catalog; create job; delete/duplicate/import pipeline. |
| Workflow | Projects (tab id `builder`) | ProjectsView (504) | Project list (active first) + detail (linked topics, experiments, hypotheses, corpora); create/edit/delete/activate via API. |
| Workflow | Reports | ReportsView (1,001) | Artifact browser (sort name/kind/size/updated), opens in a new window, download URL, open-folder; report + user templates; AI report synthesis; generate report. |
| Analysis | Entropy | EntropyDashboard | H1/H2/conditional entropy, TTR, Zipf correlation, sparklines; compare up to 3 corpora. |
| Analysis | Signs | SignsView (782) | Sign browser: confidence filters, search, glyph placeholders, cross-refs to experiments, DEDR entries, reports; sign-image processing status + triggers. Indus-signary-specific. |
| Analysis | Timeline | TimelineView | Chronological experiments + studies; entries navigate. |
| Research | Discovery | DiscoveryView (789) | Continuously fetched + classified items; topic chips with counts; kind/status filters; search; ▶ Run fetch, ✨ Run mine; item cards (title, source, kind chip, confidence bar, summary, link chips; Save / Dismiss / Reviewed / Open / Send to AI); email-digest toggle (SMTP). |
| Research | Evidence Graph | IndusEvidenceView (823) | Three tabs — Library (registered papers, PDF upload, URL import), Claims (extracted claims with filters; renders StageLegend's two-lane display, ContestDisplay, NotUnderstood), Sweep (sweep config editor, run sweep, import candidates). All APIs are `/indus-*`. |
| Research | Hypotheses | HypothesisTracker | Hypothesis CRUD; statuses **active → confirmed \| refuted \| paused**; links to experiments/studies; AI hypothesis generation + experiment chains. |
| Research | Notebooks | ResearchNotebook | Markdown scratchpads with live preview (own minimal renderer), linkable to a study, tags. |
| Research | Citations | CitationManager | Citation store; manual entry + BibTeX paste/import; links to experiments/studies. |
| Research | Correspondence | CorrespondenceView | Comms tracker cards; paste-to-import email parsing; project scoping; inbound/outbound coloring. |
| Research | AI Tools | AIToolsView (611) | Hub of backend AI endpoints — /ai/chat, /ai/decipher, /ai/sign-reading, /ai/hypotheses/generate, /ai/experiment-chain, /ai/draft-section, /ai/synthesize, /ai/report-synthesis. |
| Research | Foundation Check | FoundationCheckView (331) | GET /api/v1/research/foundation-check; per-check pass/fail/warn/auto_fix (one-click fix); header explicitly notes "Foundation Check ≠ Phase Unlocker" — failures do NOT block the research loop. |
| System | Status | StatusView (410) | SSE hardware metrics at 1 s (CPU/RAM/GPU/disk/network), gauges, sparklines, peak tracking + clear-peaks; backend health + catalog summary. |
| System | Jobs | JobsView (795) | Job list + lifecycle (cancel/pause/resume/pause-all/resume-all/clear); results via ResultsView; retry with runtime-param scrubbing. ResultsView (365, embedded): type renderers (block_entropy → chart+table; decipher → mapping table; hypothesis → comparison; logosyllabic → classification table; char_freq → frequency table; default → raw JSON). |
| System | Settings | SettingsView (496) + panels | System (env status, venv setup/rebuild/upgrade, package list, cache clear), AI Behavior, sequential run queue; ProvidersPanel, AIEndpointsPanel, AIProfilesPanel, ModelAssignmentsPanel, ModelHubPanel, AutoDiscoveryPanel (547). |
| System | Help | HelpView (2,574) | Built-in manual. Indus-heavy content. |

Supporting components: BottomPanel (1,179 — Logs tab = SSE stream, last 500
lines, filter, purge; Jobs tab = mini job list; Terminal tab = runs terminal
commands; Chat tab = docked AI chat; also parses job-completion events into
navigation actions), CommandPalette, NotificationCenter/Drawer +
NotificationsPanel (886), ResearchLoopPanel (2,975 — autonomous study-loop
dashboard: last-session insights, scheduler toggle, iteration presets, live SSE
progress, run history; APIs split across `/study-loop/*` and legacy
`/research-loop/*`), StageLegend (Spec 029 two-lane display doctrine).

**Orphaned/dead components** (referenced by 0 other files): StudiesView (397 —
displays Fuls 2023 catalog data from `/api/v1/reports/indus` **with bundled
fallback data baked in**: REAL_CATALOG_SUMMARY n_signs 713, n_tokens 17,990),
AG2Panel, AIChatView, CollaborationPanel, ExperimentRegistry,
PhaseAdvancerPanel (449), SignDictionary, PresetsView.

## The "project" (program) data model today

`api.ts` (~line 2078) + `hooks/useProject.tsx`: Project = { id, label,
description, prompt_context, topic_ids[], experiment_ids[], corpus_ids[],
is_active, created_at, updated_at }. ActiveProject null = "global" mode
(everything unfiltered); selection persisted in localStorage
(`glossa_active_project`, sentinel `__global__`); resolution order =
localStorage → backend is_active → auto-activate if exactly one project;
switching syncs to the backend and dispatches `glossa:project-changed`.
**A project is a filter over shared data, not a workspace boundary.**

## The claims doctrine in code (Spec 029, `components/StageLegend.tsx`)

Two-lane discipline — lane 1 = machine-speed verification (verdicts, AEE
scores/bands, extraction statuses; checking vocabulary only); lane 2 =
human-paced settlement (lifecycle stage, explanation, digestion records,
contest state); the lanes render in separate labelled regions, never in each
other's vocabulary. **Five stage names, verbatim (OD-4): created, checked,
explained, accepted, digested.** A sub-claim's stage is capped at its parent's,
and the cap is shown. Backend verdict vocabulary (`backend/glossa_lab/*.py`):
SUPPORTED (47 uses), INCONCLUSIVE (32), CONTRADICTED (5), NOT SUPPORTED (3),
plus CANNOT BE ADMINISTERED (Spec 078 close). `api.ts` also carries
`adverse_digestion` on claim records. Hypotheses use a different, weaker
vocabulary (confirmed/refuted) that conflicts with all of the above.

## The tray (`tray/glossa_tray/main.py`, 615 lines; pystray)

The tray's own header comment: the tray is "the single entry point" — it starts
the backend if not running and supervises it on Windows. Icon = packaged brand
tile + badge dot (green healthy / yellow degraded / red stopped / grey
unknown-starting); drawn-tile fallback if the asset is missing. Tooltip example:
"Glossa Lab - Healthy (v0.1.0)". Status text examples: "Backend: Healthy v0.1.0
up 1803s" (**raw seconds**), "Backend: Stopped (click to view log)", "Backend:
Stopped by user", "Backend: Stopped - auto-restart limit reached (click to view
log)", "Backend: Degraded (click to view log)". Menu: Open UI (default) /
status line (click opens log when errored) / Start–Stop Service toggle (greyed
while a start is in flight) / Restart Service / View Log (**opens raw
`logs/backend.log` in the default text editor**) / "Port: NNNN" (display-only)
/ Change Port… (tkinter dialogs; writes `~/.glossa-lab/config.json`; offers
restart) / autostart toggle / Quit. Polls health every 3 s (bounded ~24 h, then
the poller stops with a printed WARN). Windows supervision: auto-restart capped
at 3 per rolling hour, never overrides a user stop, cap surfaced in the status
text. Backend log rotation 10 MB × 3 backups, rotated by the tray at start.
**No program identity anywhere in the tray** — no active program, no
claim/verdict/digestion state. Spec 080 Amendment 3 (on main) added the
tray-accumulation evidence: start tests accumulated 3 trays (host run
40880047294).

## (a) Where Indus is baked into the SHELL vs legitimately data

Baked into the shell/framing (must go generic):

- Sidebar subtitle "Indus Script Analysis" — the tool's identity statement.
- The claims surface is named, routed, and API'd as the *Indus* Evidence Graph
  (`/indus-*` endpoints: listIndusClaims, listIndusLibrary, getIndusSweepConfig,
  runIndusSweep, intakeSweepCandidate…). The program's core loop cannot be
  reached under a generic name.
- Signs view is Indus-signary-specific as a top-level tab (DEDR cross-refs,
  sign-image pipeline).
- Dashboard embeds a DeciphermentPanel and calls `buildSaExperiment` (SA = the
  simulation the preprint's §2.4 records as falsified as evidence).
- AI Tools' headline endpoints are /ai/decipher and /ai/sign-reading.
- StudiesView's bundled Fuls-2023 fallback catalog data (dead code, but it is
  the shape of the sin: program data baked into the binary).
- `indus-data` navigation alias; Help content is Indus-heavy throughout.

Legitimately data (stays, inside the Indus program's space): the Indus corpora
and sign inventory as data views; the registered sources (Laursen, Mahadevan,
Wells, CDLI); the claims themselves; correspondence with Indus scholars.

## (b) Layout problems

- The Dashboard mixes five purposes (counts, AI narrative, RSS feed,
  decipherment, the research loop) with no single obvious next action.
- Anchor sets — first-class research objects — are an editor buried inside
  CorporaView (~line 869).
- Status = hardware liveness (SSE gauges) while the shell health badge is a
  bare colored dot: nowhere does the UI say *what* is serving or *when that
  was observed* (identity/freshness missing at shell level).
- Logs: the bottom panel shows a live 500-line stream; the tray's View Log
  opens the raw cumulative file. History is presented without session framing —
  the 2026-10-29 audit found the backend log carrying 989 cumulative ERROR
  lines, which surface to the user as if they were current state.
- The bottom panel duplicates the Jobs view and adds a Terminal to a research
  tool's shell.
- Eight orphaned components ship in the tree, one with live-looking bundled
  data (StudiesView).
- Settings mixes tool configuration (env repair, providers, models) with
  program configuration (AutoDiscovery sources) as peer panels.

## (c) Workflow mismatches vs how the program actually works

- The AEE loop's center — claims with falsifiers, verdicts, five-stage
  digestion — has **no top-level home**. Claims live inside an Indus-named
  view; digestion stages render only inside claim rows; there is no digestion
  board and no "what needs a human next" queue, even though explained/accepted
  are human-paced and are the program's real bottleneck.
- Hypotheses use a conflicting status vocabulary (confirmed/refuted) next to
  the verdict vocabulary (SUPPORTED / NOT SUPPORTED / INCONCLUSIVE /
  CONTRADICTED / CANNOT BE ADMINISTERED).
- Foundation Check — the constitution's gate before external communication
  and publication — is one of 21 peer tabs and explicitly blocks nothing in
  the UI.
- The Research Loop is embedded in the Dashboard instead of a first-class
  surface; its APIs are split across two endpoint families.
- Projects exist but the shell defaults to Global: the program is a filter,
  not the unit of work; ProjectsView is filed under "Workflow" with tab id
  `builder`.
- Mobile nav elevates Discovery + AI over the claims loop.
