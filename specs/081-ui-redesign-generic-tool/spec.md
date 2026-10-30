# Feature Specification: UI Redesign — Glossa Lab as a Generic Program Tool

**Feature Branch**: `spec/081-ui-redesign`
**Created**: 2026-10-29
**Status**: APPROVED 2026-10-29 (see Amendments) — Phase 2 build unblocked. Claims frozen before code (spec-kit + AEE flow).
**Input**: Owner directive, 2026-10-29: "make wireframes for the entire ui then make fixes to make it more suitable for the work. and make sure it fully agrees with how we work and has a better layout. it must be set up as a generic tool, not tied exclusively for indus. indus is one use of it but it can be used for other things."
**Predecessor**: Spec 029 (TAO claim lifecycle — the two-lane discipline and the five stage names this design carries verbatim), Spec 079 (supervised backend + tray), Spec 080 (desktop host migration — the tray and installer behavior this design builds on).
**Design artifacts**: `wireframes/` in this folder (17 full-fidelity HTML renders + stylesheet + screenshots at desktop 1440 and mobile 390), `inventory.md` in this folder (the complete "before" record).

## Problem statement

The interface was built around one program and one moment in its life, and it shows in three ways.

**1. The shell is about Indus; the tool is not.** The sidebar's subtitle is "Indus Script Analysis". The claims surface — the center of the work — is named, routed, and API'd as the *Indus* Evidence Graph (`/indus-*` endpoints). The home screen embeds a decipherment panel. A second research program inside this tool would have to live inside another program's vocabulary. The requirement: **Glossa Lab is the tool; a program is the unit of work inside it; Indus is one program.** The shell (brand, navigation, home, program switcher, settings, tray) must be program-agnostic; program-specific concepts live inside the program's space, as data.

**2. The layout does not match the workflow it serves.** The program works the AEE loop: claims registered *with falsifiers* → evidence gathered → verdicts (stated as what they mean) → digestion in five named stages (created, checked, explained, accepted, digested) → records in an append-only ledger. In the current UI that loop has no home: claims sit inside an Indus-named view; digestion stages render only inside claim rows, with no queue for the human work that is the program's real bottleneck; a second, conflicting status vocabulary (hypotheses: confirmed/refuted) sits one tab away; the foundation check — the constitution's gate before anything leaves the program — is one of 21 peer tabs and blocks nothing; the research loop is a panel embedded at the bottom of a dashboard that mixes five purposes and offers no next action. The requirement: **the UI must agree with how we work** — one purpose per screen, one obvious next action, progressive disclosure, honest defaults, negative results at the same prominence as positive ones, and identity over liveness everywhere (a status shows *what* it is and *when* it was observed, never a bare green dot).

**3. History is presented as current state.** The tray's View Log opens the raw cumulative backend log (989 historical ERROR lines at the 2026-10-29 audit) in a text editor; the bottom panel streams the last 500 lines unframed; uptime is shown in raw seconds ("up 1803s"). The owner, reading the UI on 2026-10-29, saw "lots of failures and fallthroughs" — most of them history wearing the clothes of the present. The requirement: **every log or history surface states its window**; the present is framed as the present (this session), and the past is labelled the past.

The full before-record — every route, view, tray surface, the dead components, and the three call-out lists (Indus-in-shell, layout problems, workflow mismatches) — is `inventory.md` in this folder.

## User Scenarios & Testing

### User Story 1 — Land in the right program (Priority: P1)

The operator opens Glossa Lab and is offered the programs, not a global dashboard. Opening one lands on that program's home: where its loop stands, in its own words.

**Acceptance Scenarios**:

1. **Given** the tool with one program, **When** the operator opens it, **Then** the tool home lists the program with its question, its claim count, and its last verdict, and one primary action opens it.
2. **Given** no program exists, **When** the operator opens the tool, **Then** the first-run screen explains the program model and offers create (name + question only) or import.
3. **Given** two programs exist, **When** the operator switches program from any screen, **Then** every program surface shows the newly selected program's data and the switcher names it — no surface keeps showing the previous program.

### User Story 2 — Register a claim the way the doctrine requires (Priority: P1)

The operator registers a claim. The register refuses a claim with no falsifier. The claim's page shows its falsifier, its machine verdict lane, and its human digestion lane, in separate labelled regions.

**Acceptance Scenarios**:

1. **Given** the claims register, **When** the operator submits a claim without a falsifier, **Then** registration is refused with the reason stated — the claim is not stored.
2. **Given** a registered claim, **When** the operator opens it, **Then** the falsifier is visible without scrolling past it, the verdict lane uses checking words only, and the digestion lane shows the stage track (created, checked, explained, accepted, digested — verbatim) with any sub-claim cap shown.
3. **Given** a claim whose checks returned NOT SUPPORTED, **When** it appears on the program home and in the register, **Then** it renders at the same size and weight as a SUPPORTED claim.

### User Story 3 — Work the human queue (Priority: P1)

The operator opens the digestion board and sees which claims wait on which human act, oldest first, each row naming exactly what is missing.

**Acceptance Scenarios**:

1. **Given** claims at stage *checked*, **When** the operator opens the board, **Then** they appear under "Needs explanation", each with its missing-act line.
2. **Given** the board, **When** the operator follows "Start with the longest-waiting claim", **Then** they land on that claim with the explanation-record action as its primary action.
3. **Given** any count shown anywhere for digestion, **When** the operator reads it, **Then** it is attached to the claims and acts it counts — never a bare progress score.

### User Story 4 — Believe the status (Priority: P2)

The operator (or the tray, at a glance) can tell what is serving, since when, and how that was verified — and can read this session's log without mistaking history for the present.

**Acceptance Scenarios**:

1. **Given** the Status screen, **When** it opens, **Then** it shows the application's identity (name, version, host, data location, database verification) with the time the check was made, before any performance metrics.
2. **Given** the tray, **When** the operator reads its status line, **Then** it names the open program and gives uptime in human units.
3. **Given** the session log panel, **When** it opens, **Then** it states its window ("this session, since HH:MM") and labels the full file as history.

### User Story 5 — Start a second program (Priority: P2)

The operator creates a program on an unrelated subject. Nothing in the flow asks for, or shows, anything about the first program's subject.

**Acceptance Scenarios**:

1. **Given** the tool home, **When** the operator creates a program, **Then** the form asks for a name, a question, and an optional description — nothing else.
2. **Given** the new program with data but no claims, **When** its home opens, **Then** it teaches the claim discipline in the program's own terms and offers "Register the first claim" as the primary action.

## Requirements

- **FR-001 Program model.** The UI's top-level unit is the *program* (the existing backend Project entity, renamed in UI language; the data model is unchanged in phase 2 beyond presentation). The tool home is the program list. The shell contains no program's subject matter — in brand text, navigation labels, settings, or tray strings.
- **FR-002 Navigation.** Program space: Home, Claims, Digestion, Evidence & sources, Data, Analysis, Experiments, Discovery, Research loop, Reports & ledger — in loop order. Tool space: Jobs, Status, Settings, Help. Mobile bottom nav: Home, Claims, Digestion, Jobs, More. The program switcher is always visible in program space and names the program + its question.
- **FR-003 Claims.** Register + claim detail as wired (wireframes 03–04). Registration requires a falsifier. The detail renders lane 1 (verdict, scores, extraction state) and lane 2 (stage, explanation/digestion records, contest state) in separate labelled regions; the five stage names appear verbatim; a contested sub-claim displays on the parent and caps its stage; the verdict vocabulary includes SUPPORTED, NOT SUPPORTED, INCONCLUSIVE, CONTRADICTED, CANNOT BE ADMINISTERED, plus the honest non-verdicts *insufficient evidence* and *awaiting expert adjudication*, stated plainly.
- **FR-004 Digestion board.** Columns by the act owed (needs explanation / needs acceptance / ready to digest); every card names its missing act; the primary action enters at the longest-waiting claim (wireframe 05).
- **FR-005 Program home.** Loop status first: claims by verdict (negative verdicts unfiltered, un-greyed), the digestion queue as a count with its doorway, foundation-check state with its checked-at time, data counts; exactly one primary action — register a claim (wireframe 02).
- **FR-006 Foundation check.** Its state shows on the program home; report generation and other external-facing outputs surface a failing gate in the open, with the reason, at the point of action (per constitution §III) — replacing the current "one of 21 tabs, blocks nothing" posture. (The check remains distinct from experiment gating; it is not a phase unlocker.)
- **FR-007 Status.** Identity before metrics: application, version, host, bind, data folder, database verification, serving-since, checked-at. All durations humanized, in the web UI and the tray (wireframe 14).
- **FR-008 Log framing.** Every log/history surface states its window. The default view is the current session; the full cumulative file opens only as a labelled record (wireframes 14–15).
- **FR-009 Jobs.** One tool-level queue (the bottom-panel duplicate is removed). Every row names its program; results render meaning-first (a verdict, a table) with the raw structured record one click deeper; failures render at full prominence with a what-happened line and a retry that states what it will do (wireframe 09).
- **FR-010 Research loop.** A first-class program surface: state as identity (state, since, ended-by, scheduler state), session shape chosen at start, staged findings that cannot auto-register as claims or promote anchors, and the loop's ceiling — it can advance a claim to *checked*, never beyond — stated on the surface (wireframe 11).
- **FR-011 Discovery.** An inbox with an explicit fence (inbox ≠ evidence); fetch time and source list stated on the surface; per item, "Save to sources" is the promoted act; machine confidence labelled a sorting hint (wireframe 10).
- **FR-012 Evidence & sources.** Library, Citations, Correspondence, and Notebooks in one surface. Entry requires citation + provenance; limits and restrictions render on the item; each item links the claims that use it (wireframe 06).
- **FR-013 Data.** Corpora and anchor sets as peers. Anchor grading (recorded / strict / pending) visible at the surface. Restricted material is labelled at import and cannot be exported (wireframe 07).
- **FR-014 Experiments.** Listed by the claim they test, with outcomes in verdict language. A draft cannot run until its claim and falsifier are registered. Pipelines fold in as reusable experiment graphs. The canvas craft (typed nodes, port colors) is unchanged (wireframe 08).
- **FR-015 Reports & ledger.** Reports carry their publication state, including *prepared — awaiting approval*. The ledger is readable in-app and append-only by construction: a correction is a new entry naming the old one (wireframe 12).
- **FR-016 Settings.** Tool settings and program settings in two labelled groups. The port is one setting with two doors (Settings and the tray's Change Port), named as such. No accounts or permissions surface is created (wireframe 13).
- **FR-017 Tray.** Status line and tooltip name the open program; uptime humanized; single-instance enforced (starting a second tray focuses the first); "View status & session log" replaces "View Log" and opens the framed Status screen. Supervision semantics unchanged: auto-restart capped at 3 per rolling hour, a user stop never overridden, the cap stated in the status text (wireframe 15).
- **FR-018 De-hardcoding.** Indus leaves the shell: generic shell strings; the claims surface renamed and its endpoints generalized from `/indus-*` to program-scoped (with a compatibility shim during migration); the Dashboard's decipherment/SA panels removed from the home (the SA experiment remains in the record as data — its §2.4 status is not hidden, it is simply not furniture); dead components removed, including StudiesView with its bundled fallback data.
- **FR-019 Empty states.** No-program and no-claims states as wired (wireframes 16–17): they teach the model, name what exists and what does not, and offer exactly one primary action each.
- **FR-020 Quality floor.** WCAG 2.2 AA for the new shell; 44 px touch targets retained; at 390 px every screen's primary action is reachable without horizontal scrolling; every wireframe claim in `aee-claims.json` is covered by a phase-2 contract test or a screenshot check against the approved renders.

## Claims (summary — machine-readable record in `aee-claims.json`)

| ID | Claim | Check |
|---|---|---|
| C081-1 | No subject-matter string of any program appears in the shell (brand block, tool home, settings, tray) in the wireframes. | Read the renders; falsifier: any shell surface naming a program's subject. |
| C081-2 | Every screen has exactly one primary-styled action, named in its annotation. | Count primary buttons per render. |
| C081-3 | Every status surface shows identity + observation time, not liveness alone. | Service chip, Status screen, tray tooltip/status line in renders 01/14/15. |
| C081-4 | Claims are ≤2 clicks from program home; claim detail shows falsifier + both lanes in separate labelled regions. | Renders 02/03/04. |
| C081-5 | Negative verdicts render with the same weight as positive ones, unfiltered by default. | Renders 02/03/08/09. |
| C081-6 | A second program fits the same shell; the create form requires only name + question. | Renders 01/16/17. |
| C081-7 | Every log/history surface states its window; none presents cumulative history as current state. | Renders 09/12/14/15. |
| C081-8 | Every digestion-board row names the human act it is missing; no bare stage counts. | Render 05. |
| C081-9 | The five stage names appear verbatim wherever stages render. | Renders 03/04/05/17; falsifier: any synonym. |
| C081-10 | At 390 px, every screen's primary action is on-canvas without horizontal scrolling. | Mobile screenshots, all screens. |
| C081-11 | Program-space navigation labels contain no subject terms; subject content appears only as data inside a program. | Renders 02–14 sidebars. |
| C081-12 | The tray names the open program in its status line and tooltip, and is single-instance by construction. | Render 15 (single-instance is a phase-2 contract test; the render specifies the behavior). |

## Phase-2 build outline (executes only after the owner approves the renders)

Sequenced so each step lands green on its own; the frontend's Indus-hardcoding is removed in steps 1–3 and 8, not by a big-bang rewrite.

1. **Shell & routing.** New shell: program switcher card, two-space navigation (program/tool), service chip with identity + checked-at, mobile bottom nav per FR-002. Legacy tab ids and AI-navigation aliases redirect to the new routes (`indus-data` → program home of the Indus program, `studies` → claims, etc.). No view internals change in this step.
2. **Program model presentation.** Project → "program" in all UI language (API field names unchanged); tool home (program list + first-run state) per wireframes 01/16; "global" mode demoted to an explicit cross-program scope on Jobs and Reports only — it is never the default landing state again. Legacy projects import as programs with an import report.
3. **Claims surface.** IndusEvidenceView's Claims/Library/Sweep material splits: Claims becomes the program-scoped claims register + detail (wireframes 03–04); Library moves to Evidence & sources (step 6); the sweep configuration moves under the research loop, where it belongs. Backend: `/indus-*` claim/library endpoints gain program-scoped equivalents; the old paths shim to the Indus program for one release, then retire. The hypotheses fold-in (open question Q7) executes here if approved.
4. **Digestion board.** New surface over the existing stage/explanation/digestion records; missing-act derivation: stage *checked* → explanation record absent → "needs explanation"; *explained* → acceptance absent → "needs acceptance"; *accepted* → digestion record absent → "ready to digest". Contest caps display per Spec 029.
5. **Program home.** New home per wireframe 02 replaces DashboardView as the program landing. ResearchLoopPanel is extracted to its own route (step 7 shares the work); DeciphermentPanel and the SA panel leave the home — the SA experiment record stays in Experiments/Reports as data. The AI Insight narrative card does not carry over; interpretation lives on claims.
6. **Evidence & Data consolidation.** Library/Citations/Correspondence/Notebooks merge into Evidence & sources (tab state deep-linkable). AnchorSetEditor is promoted out of CorporaView into Data as a peer tab. Entropy/Signs/Timeline move under one Analysis route as views over data, reachable from a corpus or a claim.
7. **Jobs, Status, Settings, Research loop surfaces.** Jobs: single queue; BottomPanel removed (its log stream becomes the Status session log; its chat becomes the assistant panel; the Terminal does not carry over). Status: identity-first per wireframe 14. Settings: tool/program split per wireframe 13; AutoDiscoveryPanel becomes a program setting. Research loop: surface per wireframe 11; the `/study-loop/*` vs `/research-loop/*` split is unified behind the new surface.
8. **Tray amendments.** Program name in status line + tooltip; humanized uptime; single-instance guard (second launch focuses the first); "View status & session log" opens the web Status screen; log rotation unchanged. Contract tests extend the Spec 079/080 tray tests; icon hashes unchanged.
9. **Dead-code removal.** StudiesView (with its bundled Fuls fallback data), AG2Panel, AIChatView, CollaborationPanel, ExperimentRegistry, PhaseAdvancerPanel, SignDictionary, PresetsView — deleted with a ledger note; nothing imports them today (verified in the inventory pass).
10. **Verification.** One contract test or screenshot check per claim C081-1…12; Playwright screenshot pass at 1440 + 390 against the approved wireframes (the Spec 029 evidence pattern: renders filed in this spec folder); ruff + full backend suite in CI-parity conditions; foundation check; CHANGELOG + LEDGER entry. Any deviation from an approved wireframe is an amendment to this spec, recorded below — not an improvisation.

## Assumptions / epistemic boundaries (H13)

- **Specimen data.** Wireframe figures are the Indus program's real recorded counts as of 2026-10-29 (94 strict-core claims with the repair audit's 6/46/37/3/2 disposition; 287/94/44 anchors; foundation check 39/0/9; signary witnessed 399/557), labeled specimen on every render where a number could be mistaken for a live readout. Specimen *wording* (e.g. the M222 falsifier's standard form) is illustrative; no wireframe asserts a new research fact.
- **The signary stays an explicitly untested assumption** (the M14 granularity line is parked by its own kill criterion). The UI shows signary-dependent counts as program data with their provenance, never as settled ground truth.
- **Single operator.** The generic-ness is framing and structure — many programs, one operator. No accounts, roles, or tenancy are designed or implied.
- **Design only in phase 1.** This spec's branch changes no file under `frontend/`, `tray/`, or `backend/`. Approval of the renders is the phase-2 gate.
- **What this does not establish.** A better-organized UI does not strengthen any claim, verdict, or stage in the register. The redesign changes how honestly the work is presented; the work's standing is whatever the records say it is.

## Open design questions for the owner (each with the designer's recommendation)

1. **Program-switcher placement.** Sidebar card (as wired — always visible, carries the program's question) vs a top-bar dropdown vs tool-home-only switching. **Recommendation: the sidebar card.** The current failure mode was a program selector that faded into filter furniture; the switcher should read as the workspace itself.
2. **Digestion board shape.** Three columns by act owed (as wired) vs a single oldest-first queue vs a per-stage list. **Recommendation: columns by act.** Explanation, acceptance, and digestion are different sittings of work; a single queue hides which kind of attention is owed, and the columns still sort oldest-first inside themselves.
3. **Density.** Comfortable density (as wired) vs a compact register mode. **Recommendation: comfortable everywhere, with a compact toggle on the claims register only** — registers are scanned; everything else is read.
4. **Tray scope.** Status + program name (as wired) vs adding live claim/digestion counts to the tray menu. **Recommendation: status + program name only.** A count in a tray menu would be read without its caveats (which claims, which stage, contested or not); the tray's job is the service, and it opens the UI for anything more.
5. **Analysis surfaces.** One Analysis item with Entropy / Signs / Timeline as tabs (as wired) vs keeping three peer tabs. **Recommendation: one item.** They are views over data, opened from data or a claim — destinations of their own only by historical accident.
6. **AI assistant placement.** Utility button + side panel (as wired) vs a navigation destination. **Recommendation: utility only.** The assistant advises and drafts; it holds no state of record, and a nav destination would imply otherwise. "Send to AI" as a triage act is demoted for the same reason (wireframe 10).
7. **Hypotheses.** Fold into Claims (a hypothesis is a claim whose falsifier is not yet sharp — shown in the register as an early state) vs keep a separate tracker with its vocabulary aligned to the verdict set. **Recommendation: fold in.** Two claim-shaped objects with two vocabularies is how the confirmed/refuted conflict happened; one register, one vocabulary.
8. **Bottom panel.** Remove entirely (as wired — Jobs is a page, the session log lives on Status, the Terminal does not carry over) vs keep a logs-only panel. **Recommendation: remove.** Every element of the panel has a better home in the redesign; a terminal inside a research tool's shell serves no step of the loop.
9. **Dark mode.** Keep the existing toggle (light default; wireframes are light) vs light-only. **Recommendation: keep the toggle** — it already exists and costs the redesign nothing; the approval renders are light because review and print are light.
10. **Notebooks.** Fourth tab of Evidence & sources (as specced in FR-012) vs dropped. **Recommendation: keep as the fourth tab.** Notebooks are working notes toward sources and claims; filed with the source record, they stop being a peer destination.

## Amendments

### Amendment 1 — Owner approval + Q1–Q10 rulings (2026-10-29)

The owner approved the wireframe package as recommended on 2026-10-29
("Approve the wireframes as recommended (Q1–Q10) — start Phase 2"),
on the HTML package. The recommendations are therefore DECIDED, not open:

- Q1 program switcher: sidebar card.
- Q2 digestion board: columns by act owed.
- Q3 density: comfortable, with a compact toggle on the claims register only.
- Q4 tray scope: status + open-program name, no counts.
- Q5 analysis: one nav item, three tabs (Entropy / Signs / Timeline).
- Q6 AI assistant: utility only (button + side panel, not a nav destination).
- Q7 hypotheses: fold into Claims.
- Q8 bottom panel: removed.
- Q9 dark mode: toggle kept.
- Q10 notebooks: fourth tab of Evidence & sources.

The wireframe PNG renders (T011) remain owed as a record but are superseded
as an approval gate by the built-UI screenshot verification in phase 2
(step 10): every built screen is screenshot at desktop 1440 and mobile 390
and compared against its approved wireframe before it is claimed done.

### Amendment 2 — D2.2 refinement: the standing position and stage summary are program data on the program home (2026-10-30)

D2.2 removed the embedded DeciphermentPanel from the home. The panel,
however, was the surface carrying two things that are not panel
furniture: the program's **standing position** (Spec 029 Phase E2) and
the **lane-2 stage summary** over the anchor records, guarded on the
home surface by the Spec 029 Phase E2/G e2e guards
(`standing-position` / `stage-summary` testids). PR-4's CI exposed the
collision: the guards failed because their surface had been removed
under them. Adjudicated 2026-10-29 (parent decision on the worker's
three options; the claims-surface placement and the retire-the-guards
options were rejected — the standing position is the program's lead
verdict, and a guard is not retired because the furniture moved):

- The standing position and the stage summary live on the **program
  home** (wireframe 02's surface), directly under the program title,
  rendered as **program data**:
  - the standing position is a field of the program's own record
    (`projects.standing_position`, schema v25), rendered verbatim
    when the record states one; a program that states none shows
    none — the generic shell carries no subject-matter text, and no
    shell component supplies a position the record does not state.
    The seeded default program carries Spec 029's standing position
    on its record; the seeder backfills an existing default record
    whose position is still empty, and never overwrites a stated one.
  - the stage summary renders the decipherment payload's `by_stage`
    anchor counts under the FR-029-08 framing (an index into the
    anchor records, not a measure of decipherment) with the OD-4
    legend — the same data and framing the panel rendering carries.
- The Spec 029 E2/G guards are re-pointed at the program-home surface
  with their assertions' text and intent unchanged (the guard specs'
  mocked program record now carries the position, as the record it
  guards); the amendment is recorded on the Spec 029 side in
  `specs/029-tao-claim-lifecycle/guard-surface-amendment-2026-10-30.md`.
- DeciphermentPanel is untouched: it keeps its own rendering (and its
  backend source pin) for the surfaces that still mount it, until
  step 9 (T021) removes the unrendered files with their own record.
- D3 is unchanged: the stat cards still print only endpoint-exposed
  figures, and the stage summary's counts are the payload's published
  `by_stage` index — never the unexposed strict/pending split.

### Step 3 as-built note (2026-10-30, PR-5)

- The claims surface shipped as scoped: the register and detail
  consume `/api/v1/programs/{program_id}/…`; the `/indus-evidence`
  paths are the one-release shim (FR-018). Scope semantics: the
  program that owns the evidence store resolves to it; any other
  existing program resolves to its own honest empty surfaces;
  unknown ids 404.
- Two outline items deferred, recorded here rather than silently
  dropped: (a) IndusEvidenceView keeps its claims tab — and its
  Spec 029 source pin — until step 6 consolidates Evidence &
  sources and owns that pin's amendment; (b) the sweep tab's move
  under the research loop lands with the step 6/7 surface work for
  the same reason. The sweep CONFIG endpoints are unchanged.
- The wireframe-03 primary ("Register a claim") ships as a
  doorway, not a form: claims enter by registering their source in
  Evidence & sources, where extraction states the falsifier — the
  register has no direct-entry write path, and none was invented
  for this step.
- The digestion doorway deep link deferred by PR-4 lands here:
  a board card click opens that claim's detail on this surface.

### Step 6/7 as-built note (2026-10-30, PR-6)

- Steps 6 and 7 shipped together (T018 + T019), with T018's
  remainder included: the Analysis wrapper (Entropy / Signs /
  Timeline as its three tabs) and the AnchorSetEditor's promotion
  out of CorporaView into the Data surface's second tab. The PR-7/
  PR-8/PR-9 sequence left them no other home (PR-9 is
  verification-only).
- Consolidation: Evidence & sources is one tabbed surface —
  Library (extracted verbatim from the retired IndusEvidenceView),
  Citations, Correspondence, Notebooks (Q10) — mounting the three
  legacy components the old shell never mounted at all. Data is
  Corpora + Anchor sets. The two deferrals from the step-3 note
  are CLOSED: (a) IndusEvidenceView and its claims tab are deleted;
  the Spec 029 source pins moved to ClaimsView with the amendment
  record `specs/029-tao-claim-lifecycle/pin-surface-amendment-2026-10-30.md`
  (one wording change: a header comment's "provenance" became
  "source record" — the frozen synonym scan reads substrings, and
  ClaimsView otherwise satisfies every pin assertion verbatim);
  (b) the sweep moved under the Research loop as SweepPanel, its
  content verbatim plus the fence lede (importing stages a source;
  it changes no claim by itself). The Spec 029 e2e guards moved
  with the pins: they had asserted on IndusEvidenceView's claims
  tab all along, and now assert on ClaimsView; the three tests
  that expanded two claims side-by-side were re-expressed as
  sequential detail visits (register → detail → back) with the
  same assertions, plus the second claim's lanes now scanned too.
- Spec 082's frontend half landed to `ui-contract.md`: fragment
  read-once in main.tsx before the router exists →
  sessionStorage `glossa_api_token` → fragment stripped; Bearer
  on every API call (api.ts request + all fetch streams; both
  remaining EventSources — system metrics and the ollama pull —
  converted to fetch-streaming); query-string tokens never read;
  401 clears the token and raises the named "API token needed"
  gate (Settings stays reachable — its paste field is the second
  door, showing present/absent + SHA-256 first-8 fingerprint,
  never the value); health `auth: "disabled"` treats the token as
  unnecessary. T010 is done with it: CI's frontend-tests backend
  now runs with a throwaway `GLOSSA_API_TOKEN`, and the e2e
  fixtures seed it per the contract's manual-seeding path. New
  `frontend/e2e/auth-token.spec.ts` proves the contract end to
  end (gate, fragment intake + strip, query refusal, 401 clear,
  paste-to-enter, Settings fingerprint).
- One real defect found by the token-mode probe and fixed in this
  PR: the auth/feReport stores returned a fresh snapshot object
  per call, which loops `useSyncExternalStore` forever (React
  error #185) and crashed the shell at boot. Snapshots are cached
  and rebuilt only on state change now.
- A second gap, found by the Spec 029 *rendered* guards during
  this PR's verification (the source pins had passed): step 3's
  ClaimsView rendered neither the OD-4 StageLegend nor the
  governed ContestDisplay — lane 2 paraphrased the contest state
  with no data-state and no explicit no-bundle absence. The
  retired surface had carried both components, masking the gap
  until the pin move. ClaimsView now renders the legend above
  the register and on the detail, and ContestDisplay in lane 2;
  the guards pass against it unchanged. Recorded in the Spec 029
  amendment's rendered-guard addendum.
- feReport landed (C-09 frontend half): reports count as
  confirmed ONLY on the backend's 200 `{"ok":"logged"}`; the
  Status screen states never-fired / last-confirmed / last-FAILED
  from the shared store; ErrorBoundary and main.tsx's feLog both
  delegate to it.
- Jobs: program column (submit/retry stamp `params.project_id`
  from the open program; unstamped rows read "Not recorded" —
  never inferred, never a hardcoded store id in shell code),
  Finished column, "+ New job", failed jobs carry a full-width
  "What happened" row fed once from the job's own result record,
  and a details modal that leads with the record's meaning fields
  and keeps the raw JSON behind a disclosure. Named gap:
  backend-originated jobs (loop/discovery) carry no program field
  at all — stamping those server-side is a backend change outside
  this frontend step; the column states the absence honestly.
- Settings (wireframe 13): the tab machinery is gone; rows carry
  name + state + Manage disclosures grouped Tool — service /
  Tool — environment & AI / Program — {open program}. Four
  recorded deviations: (i) the Port row shows the served origin's
  port — the settings API exposes no port and the tray owns
  Change Port (the row says so: two doors, one setting); (ii)
  wireframe 14's "Restart service" primary is not implemented —
  no backend restart endpoint exists, and restart belongs to the
  tray/supervisor (Spec 079); not invented in a UI step; (iii)
  no global "Save changes" primary — the underlying panels
  persist per-section, as they always have; (iv) Discovery
  sources is presented as a program setting per the wireframe;
  its store is unchanged this step.
- Status (wireframe 14): identity first (application, version +
  build, host + serving origin, data folder + database-verified
  state, serving-since with humanized uptime, API-token mode),
  health strip with humanized uptime, the FE-reporting card, the
  foundation section keeping the canonical record and the
  API-native set in separate labelled boxes (D2.1), the machine
  sections unchanged below, and the session log last (this
  session only by default; full history behind a labelled toggle
  that warns it is not this session's record).
- Research loop (wireframe 11): ceiling lede, one state line
  (state · last session · scheduler, named as a program setting
  also in Settings), the D5 meta line naming the /study-loop vs
  /research-loop split, and the staging fence copy. All 18 raw
  fetches in the panel now carry the token. Q8 closed: BottomPanel
  deleted with its App wiring, palette command and Ctrl+J.
- Verification: Spec 029 pin tests 33/33; the full Playwright
  suite was run locally against a build-tree backend (:8021,
  token auth enforcing) — its first clean-tree run exposed the
  stale spec re-points fixed in this PR, and after those fixes
  the affected files (backend-integration, navigation, the two
  Spec 029 guard files, status, study-loop) pass locally
  (127 passed in that set), with the guard files re-verified
  16/16 after the legend/contest fix above. The authoritative
  full-suite run for this PR is CI's frontend-tests job (the
  local full run's tally was initially misread against a prior
  PR's CI count — recorded here so the record does not carry the
  error). Screenshots desktop 1440 + mobile 390 for every touched
  screen filed with the program records and visually checked. One
  process incident, recorded honestly: the first local run tested
  a stale dist (a checkpoint commit's dist restore reverted the
  bundle on disk) and its failures were the stale artifact's, not
  the code's; the run was discarded, the bundle rebuilt and
  identity-verified by asset hash, and the suite rerun clean.
  Backend-run corpus mutations were restored by exact path before
  commit (the untracked graph-experiment outputs were removed by
  exact name — the reports directory carries tracked files of the
  same pattern).
