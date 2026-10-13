# Spec 029 — Phase E2 Record: Lane-Separated Rendering

> Phase E2 of `tasks.md` (FR-029-09, FR-029-10, FR-029-05
> display rule; claims F029-C06, F029-C07; OD-4). Base: main
> `1533425b` (Phase E1 merged, PR #185). Branch:
> `impl/029-phase-e2-rendering`. Date: 2026-10-12.
>
> Scope discipline: this phase is **rendering plus additive
> serialization only**. It changes no scoring, no stage
> machinery, no record, and no verdict. It authors no
> `not_understood`, explanation, or digestion text for any live
> record — where a live record lacks that human text, the
> rendering shows the absence as a stated gap.

## E2.1 — Standing position + stage summary (completes E1.1)

`frontend/src/components/DeciphermentPanel.tsx` (both the
archived rendering, which is the live one, and the non-archived
rendering) now leads with:

- **Standing position** (`data-testid="standing-position"`):
  "The Indus script is not deciphered" — the repository
  description's standing line — followed by the plain statement
  that the program's readings are candidate readings standing at
  a lifecycle stage, that a reading is not settled by being
  recorded and checked, and that no count on the panel is a
  measure of decipherment.
- **Stage summary** (`data-testid="stage-summary"`): the anchor
  claims by stage, from the dashboard payload's Phase A
  `by_stage` counts, under the lane-2 label ("Anchor claims by
  stage — lane 2 (human-paced settlement)"), in the five
  verbatim stage names, with the unstamped count shown when
  non-zero, and the note that the counts are an index into the
  anchor records, not a measure of decipherment. Live at this
  head: created 193 · checked 94 · explained 0 · accepted 0 ·
  digested 0, `n_unstamped_stage` 0.
- **The OD-4 legend** (shared `StageLegend` component,
  `frontend/src/components/StageLegend.tsx`): the five stage
  names verbatim — created, checked, explained, accepted,
  digested — each with its plain one-line definition, including
  that being created and checked alone never settles a claim.

This completes the replacement rendering E1.1's frozen text
describes and E1 deliberately deferred to this phase
(`phase-e1-record.md`, "Deviations and honest limitations").

The legend also renders at the top of the Claims tab of
`IndusEvidenceView` (tasks E2.1 names that surface).

## E2.2 — Lane separation (tasks E2.1; FR-029-10)

`IndusEvidenceView`'s Claims tab now renders every expanded
claim as two distinct, labelled regions:

- **Lane 2 — human-paced settlement** (`data-testid=
  "lane2-region"`): the stage in Tao's verbatim name (stage
  colours live in this region alone), the stage's provenance
  (`stage_source`, `stage_as_of`, latest transition with actor
  and timestamp), the `verified_unexplained` risk flag where it
  fires (with its meaning stated), and the contest display
  (E2.3 below). A collapsed card also carries the stage as a
  labelled plain line ("Stage (lane 2): …") — never as a badge.
- **Lane 1 — machine-speed verification (checking only)**
  (`data-testid="lane1-region"`): the extraction status in a
  single neutral chip style (the per-status colour map
  `STATUS_COLORS` is deleted — lane-1 badges have lost stage
  colours and acceptance language), the retained per-claim AEE
  score object (requested via `?aee=true`) rendered **only**
  inside this region, with its band and its method context
  (AEE library scoring; the component values; "a score is a
  checking result only — it is not a stage and does not settle
  the claim"), the falsification condition (or "not stated in
  the record"), the source document, evidence note, proposed
  value, and source-stated confidence, and the not-understood
  statement (E2.4 below).

No lane-1 value renders inside the lane-2 region and no lane-2
value inside the lane-1 region; the Playwright spec
(`frontend/e2e/spec029-phase-e2.spec.ts`) asserts this on the
rendered DOM with synthetic fixtures (the lane-1 score value
absent from lane 2; the lane-2 contest content absent from
lane 1; no stage name inside a lane-1 region).

The claims fetch now requests AEE scoring (`aee: true` added to
`listIndusClaims` params in `frontend/src/api.ts`, with the
lane object types `ClaimStageObject` / `Lane1Score` /
`BundleSerialization` declared there). No score appears in any
summary or headline position; E1's withdrawals stay withdrawn
(pinned by the E1 tests and re-asserted in this phase's tests).

## E2.3 — Contest display (tasks E2.2; FR-029-05)

Backend (additive, `backend/glossa_lab/api/indus_evidence.py`,
`GET /claims`): each claim now also serializes `bundle` — the
Phase B `serialize_bundle` output for bundle parents, `None`
for non-bundle records — plus `bundle_serialization_error`
(`None` unless a malformed bundle failed serialization, in
which case the error string is serialized rather than hidden
and the listing does not fail).

Frontend (`ContestDisplay` in `StageLegend.tsx`), rendered in
the parent's lane-2 region wherever the parent renders:

- **Contested**: "Attribution contested — this claim's stage is
  capped at checked while the contest is active", the caps the
  parent-stage computation applied (`caps_applied`, e.g.
  `od3-contested-attribution-caps-at-checked`), and the contest
  record itself (contested by whom, on what date, on what
  evidence).
- **Bundle, not contested**: the attribution contest state is
  shown (`unexamined` / `uncontested`), with any applied caps.
- **Not a bundle parent**: the honest absence — "Attribution
  contest: none recorded — this claim is not a bundle parent,
  so it carries no attribution sub-claim and no contest state."

**Live state, stated plainly: no live record is a bundle
parent.** All 31 extracted claims serialize `bundle: null` at
this head (pinned by test), and anchors have not been
decomposed into bundles (decomposition is the ongoing lane-2
work queue named in plan §2.1, not a migration deliverable).
The contested rendering path is therefore exercised by
synthetic fixtures only — the backend test (a synthetic
contested bundle parent serializes `attribution_contested`,
the contest record, the computed stage capped at `checked`,
and the OD-3 cap string) and the Playwright spec (the same
shape rendered). Live records render their real state: the
no-bundle absence line above.

## E2.4 — Not understood with every verdict (tasks E2.3; FR-029-09)

Backend (additive, same endpoint): each claim serializes
`not_understood` — the record's own statement verbatim, or
`None` — and `not_understood_recorded`.

Frontend (`NotUnderstood` in `StageLegend.tsx`), rendered in
the lane-1 region with every verdict display:

- **Authored**: "What remains not understood: " + the record's
  own text, verbatim (`data-state="recorded"`).
- **Unauthored — the absence form**: a dashed amber box,
  `data-testid="not-understood"`, `data-state=
  "not-yet-recorded"`, reading: "What remains not understood:
  **not yet recorded — this record is incomplete.** Writing
  this statement is lane-2 human work; no machine-generated
  text is substituted for it."

**Live state: all 31 extracted claims are unauthored** — every
live claim renders the absence form (pinned by test against
the live store). No machine-generated statement was written
for any live record in this phase; that would be a
phase-failing defect, not a shortcut.

### The authoring queue (lane-2 human work, per tasks E2.3)

Authoring `not_understood` statements for the existing
verdict records is named-human lane-2 work. The queue, in
priority order (computed from the live store at this head):

1. **The 8 `verified_unexplained` claims** (stage `checked`,
   supported-class checking outcomes — the flagged risk state;
   a statement of what remains not understood is most owed
   exactly where checking looks strongest):
   `parpola_2010_dravidian_solution_manual_001`,
   `parpola_2010_dravidian_solution_manual_002`,
   `without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_001`,
   `without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_003`,
   `yadav_2009_arxiv_manual_001`, `yadav_2009_arxiv_manual_002`,
   `yadav_2010_ngrams_manual_001`, `yadav_2010_ngrams_manual_002`.
2. **The remaining 2 `checked` claims with verdicts**:
   `farmer_sproat_witzel_2004_manual_001` (contradicted),
   `indus_valley_script_deciphered_from_myth_65ff0a26_manual_002`
   (partially falsified).
3. **The 21 `created` / untested claims** — statements may be
   authored with their first checking, in the same pass.

Each statement must be written by a named human, in plain
language, at the time the verdict is reviewed; the field ships
as the record's own `not_understood` value and renders
verbatim under E2.4's recorded form.

## E2.5 — Verbatim-name guard

- Backend source guard (`test_spec029_phase_e2.py`): the
  legend source carries the five names verbatim and the
  never-settles line; none of the touched frontend sources
  (`StageLegend.tsx`, `IndusEvidenceView.tsx`,
  `DeciphermentPanel.tsx`) contains a stage-label synonym
  (`verified` / `proven` / `confirmed`) outside the governed
  `verified_unexplained` flag name.
- Rendered guard (Playwright): no stage name renders inside a
  lane-1 region on the claims surface, and the withdrawn
  "signs deciphered" headline stays absent from the rendered
  panel. Program-wide display guards remain Phase G's work
  (tasks G4), as scoped.

## Evidence (E2.4 gate)

- **Screenshots** (`phase-e2-evidence/`, served locally from
  this worktree's built frontend + backend on localhost port
  8002; port 8001 was held by a stale-tree backend, left
  untouched — same note as E1; pages scrolled through before
  capture):
  - `before-{desktop,mobile}-{dashboard,evidence-claims}-{viewport,full}.png`
    — the base head: panel with anchor count + token coverage
    only (no standing position, no stage summary, no legend);
    claim cards with flat coloured status badges and no lanes,
    no stage, no not-understood rendering.
  - `after-{desktop,mobile}-{dashboard,evidence-claims}-{viewport,full}.png`
    — the panel leading with the standing position, the stage
    summary (created 193 · checked 94 · explained 0 · accepted
    0 · digested 0) and the legend; the claims list under the
    legend, each card carrying its labelled lane-2 stage line.
  - `after-{desktop,mobile}-evidence-detail.png` — the expanded
    first live claim: lane-2 region (stage created, as of
    2026-10-12, stage source, latest transition, contest
    absence line) and lane-1 region (neutral `untested` chip,
    AEE score 0.289 · band low with method context, falsifier
    "not stated in the record", and the not-understood absence
    box) — verified visually at both widths.
- **Served-payload verification** (live local API, not
  source): `GET /indus-evidence/claims?aee=true` returns each
  claim with `stage` (lane-2 object), `lane1_score` (distinct
  lane-1 object), `not_understood: null`,
  `not_understood_recorded: false`, `bundle: null` for all 31
  live claims; `GET /dashboard/decipherment` keeps serving
  `by_stage = {checked: 94, created: 193}`,
  `n_unstamped_stage = 0`, with E1's withdrawn fields still
  absent.
- **New tests**: `backend/tests/test_spec029_phase_e2.py`
  (7 tests) pin the live absence serialization, the lane
  separation of the serialized objects, the synthetic
  contested-bundle serialization with the OD-3 cap, the
  authored-statement passthrough, and the frontend source
  guards; `frontend/e2e/spec029-phase-e2.spec.ts` (5 tests)
  pins the rendered legend, regions, contest + cap display,
  absence form, lane non-mixing, verbatim guard, and panel
  standing position.
- **Frontend tests run locally** (against the locally served
  backend on port 8002, Chromium from the local Playwright
  cache): the new E2 spec **5 passed**; the neighbouring
  specs for the touched surfaces (`evidence-graph.spec.ts`,
  `decipherment-actions.spec.ts`) **63 passed, 1 skipped**
  (the navigation-persistence test self-skips by design, as
  in E1). The full frontend suite is CI's Frontend tests
  (Playwright) job; its result is in the gate evidence below.
- **Foundation check**: 40 passed / 0 failed / 8 warnings —
  identical to the pre-change baseline (run with the
  gitignored Holdat CSVs copied in, never committed).
- **Full backend suite** (`pytest backend/tests`, CI's
  GPU-only files excluded as in CI; CI-parity venv, aee
  1.4.0): **1381 passed, 6 skipped, 0 failed** — the
  1374 passed / 6 skipped E1 baseline plus exactly this
  phase's 7 new tests.
- **PR / CI / merge**: PR: BitConcepts/glossa-lab
  **#186** (`impl/029-phase-e2-rendering` → `main`).
  CI on the implementation head `b2adf1b3` (workflow run
  38339672422): **all 7 checks success, read from the check
  runs' own conclusions** — Backend tests (pytest) pass;
  Frontend tests (Playwright) pass; Evidence Graph script
  smoke tests pass; Indus public validation checks pass;
  Shell wrappers (ubuntu-latest, macos-latest,
  windows-latest) pass. This record's gate-evidence
  completion commit re-verifies green on the final head
  before merging (same workflow, all 7 checks success on
  the final head — conclusions read again after that run).
  Merge: method `merge`; the merge commit SHA and the new
  main head were verified via the GitHub API immediately
  after merging (a merge commit cannot name itself in the
  content it merges; the SHAs are stated in the PR timeline
  and in this phase's delivery report).
- **Lint**: ruff clean on every authored/edited Python file.
- **Branding sweep**: no other-company or other-program
  names in any authored or edited file.
- **Frozen bytes**: nothing digest-covered under
  `specs/029-tao-claim-lifecycle/` was edited; this record,
  the evidence directory, the LEDGER entry, the new backend
  test file, and the new Playwright spec are the phase's
  additions. The tracked `frontend/dist` build output is
  rebuilt from the edited sources. Running the backend suite
  regenerates extraction timestamps in
  `glossa-indus/claims/extracted_claims/*.json` as a
  pre-existing side effect; those files were restored
  byte-identical before commit.

## Deviations and honest limitations

- **Worktree source**: the briefed `--shared` clone from the
  Phase E1 worktree failed (its alternates chain nests through
  the freeze worktree: "ignoring alternate object stores,
  nesting too deep" / an unreadable tree). Per the brief's
  fallback, the worktree was cloned `--shared` from the
  healthy 029I chain instead, the `github` remote added, and
  the branch cut from the fetched `github/main` at the exact
  brief head `1533425b`. No deviation in tree.
- **Tasks-text numbering**: this record follows the brief's
  E2.1–E2.5 mapping (standing position, lane separation,
  contest, not-understood, verbatim guard), which spans the
  frozen tasks.md items E2.1 (two regions), E2.2 (contest),
  and E2.3 (not-understood) plus E1.1's deferred replacement
  rendering. Every frozen item is covered; the mapping is
  noted here so the two numberings are never confused.
- **Anchor surfaces**: the anchor rendering this phase
  changes is the DeciphermentPanel's anchor summary (the
  surface that renders the anchor population's stage data).
  `SignsView`'s per-sign deciphered/undeciphered counts —
  inventoried in E1's record as an E2/G follow-up — are **not**
  covered by tasks.md E2's named surfaces (it renders per-sign
  flags from the signs API, not claim or anchor stage data)
  and are left to Phase G, as are the historical
  experiment-graph node schemas E1 inventoried.
- **Contest on live records**: none exists (E2.3 above) —
  the contested path is fixture-proven only, and the record
  says so rather than implying live coverage.
- **Port note**: local serving and verification ran on port
  8002 from this worktree; the stale-tree backend on port
  8001 was left untouched.
- **Local Playwright browser**: as in E1, local e2e and
  screenshots used the Chromium build already present in the
  local Playwright cache; CI installs its own browser and is
  the authoritative frontend gate.

---

*AI disclosure: executed by an AI agent (Muse Spark, via Muse)
at the direction of Tristen Pierson, per constitution §VI.*
