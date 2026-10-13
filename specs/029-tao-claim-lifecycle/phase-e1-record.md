# Spec 029 — Phase E1 Record: Display Withdrawals

> Phase E1 of `tasks.md` (FR-029-08; claim F029-C06; audit
> §5-P5). Base: main `7528ddc5` (Phase J merged, PR #184).
> Branch: `impl/029-phase-e1-withdrawals`. Date: 2026-10-12.
>
> Scope discipline: this phase is **withdrawal only**. It
> removes the displays the audit found presenting graded
> tallies as decipherment or acceptance. It authors no
> replacement headline, no lane rendering, and no
> "not understood" statement — the honest replacement
> rendering is Phase E2's work.

## What was withdrawn, and where

**E1.1 — Panel headline (`frontend/src/components/DeciphermentPanel.tsx`,
archived-state rendering, the live one).**

- The status footer — "**{totalAnchors} signs deciphered** —
  all signs encountered in the publicly accessible Holdat +
  ICIT + Firestore corpora have Proto-Dravidian readings
  ({high} HIGH confidence)", plus its ICIT-catalogue
  continuation sentence — is removed entirely (audit
  §5-P5.1, verbatim). No replacement copy is authored.
- The "Signs Deciphered" metric tile is withdrawn as a
  headline. The count itself remains only as an index into
  the anchor records, under the neutral label "Anchor
  Records" (counts as indices into records are permitted by
  FR-029-08; a count presented as decipherment is not). Its
  inventory sublabel ("of {icitTotal} known · {gap} gap")
  is unchanged.
- The "Deciphered signs — {n}/{n} publicly accessible signs
  have readings (100%)" progress bar is removed.
- The token-coverage bar's label drops its trailing
  "decoded" ("Token coverage ({pct}% of 7,002 Holdat corpus
  tokens)"); the bar and the ICIT full-inventory bar (an
  inventory count, not a decipherment claim) remain.

**E1.2 — Dashboard payload (`backend/glossa_lab/api/dashboard.py`,
`GET /dashboard/decipherment`).**

- `sa_aggregate` is removed from the response, and the code
  that assembled it from the Phase-213/257 SA run files is
  deleted. The SA method was falsified in Phase-107; its
  aggregate must not be served (audit §5-P5.2). The
  underlying run files are untouched.
- `fully_decoded_pct` and `n_fully_decoded` are removed from
  the response, and the code that assembled them — including
  the hardcoded Phase-218 fallback values (0.691 / 1165)
  that were served when no data file was found — is deleted.
- The same-named per-round field inside `progression`
  entries is also removed, so no shape of the payload
  carries a "fully decoded" percentage.
- Consumers: `DeciphermentPanel` was the only consumer of
  all three fields. Its SA-confidence tile and its
  seals-decoded tile are deleted (above), and the
  non-archived rendering's "Inscriptions Fully Decoded" bar
  is deleted with them. The `DeciphermentRound` type in
  `frontend/src/api.ts` drops the field. The Playwright
  mock in `frontend/e2e/decipherment-actions.spec.ts` is
  updated to the served shape. `total_seals` (a corpus
  count) remains in the payload; it has no remaining
  display consumer in the panel and is recorded here as
  inventory, not withdrawn — E1.2 does not name it.
- Every other field is kept, including Phase A's additive
  lane-2 anchor fields `by_stage` / `n_unstamped_stage`
  (verified live below: `by_stage = {checked: 94,
  created: 193}`, `n_unstamped_stage = 0` at this head —
  Phase D has since stamped the population Phase A found
  unstamped).

**E1.3 — Mean score (`backend/glossa_lab/aee_core.py`,
`assessment_summary`, served by `GET /claims/aee-scores`).**

- `mean_propagated_score` (live value 0.497641 at this
  head; the audit recorded 0.484903 against the earlier
  claim set) is removed from the summary return, and the
  mean computation is deleted. It is **not retained
  anywhere**: the frozen text permits a retained
  program-level diagnostic only inside a lane-1-labelled
  block with method and falsifier context, and building
  that block is replacement rendering (Phase E2), so the
  compliant E1 disposition is full withdrawal from the
  summary with no re-presentation.
- Where the score remains: inside each per-claim detail
  entry of the same response (`aee_score` / `lane1_score`,
  with `propagated_score` and `band`), travelling with that
  claim's own falsifier (`falsification_condition`) and
  stage object — per-claim detail context, never a summary
  or headline. AEE scoring itself (`aee_core` scoring,
  the per-claim values) is untouched; the Phase A/I
  byte-identical per-claim score regressions still pass.
- The three pre-existing assertions of the mean
  (`test_aee_core.py`, `test_spec029_phase_a.py`,
  `test_spec029_phase_i.py`) are updated to assert its
  absence, with the supersession noted at each site; the
  per-claim fixture comparisons those tests exist for are
  unchanged and green.

**E1.4 — Band placement.**

- Inventory: no frontend surface renders an AEE band at
  all. `IndusEvidenceView` renders no AEE score or band;
  the band exists only inside the per-claim score object
  of the `aee-scores` detail entries (E1.3 above), which
  no UI places beside a claim status. There was therefore
  no band-beside-status rendering to delete in the claims
  UI, and the band's data home (the per-claim lane-1 score
  object, alongside the score itself) is the placement
  E1.4 requires.
- In `DeciphermentPanel`'s non-archived rendering (not
  reachable against the current backend, which serves
  `archived: true` with `current_state: null`, but still a
  surface in the code): the header badge carrying the
  confidence level and weighted percentage in summary
  position is removed, and the "Weighted Confidence"
  summary bar is removed. The per-round progression
  sparkline (historical round data) remains; full
  lane-separated re-rendering of this branch is E2's work.

## Frontend inventory — "deciphered / decoded" phrasing

Grepped across `frontend/src` for the phase record:

- `DeciphermentPanel.tsx` — all volume-as-decipherment
  constructions withdrawn (above). The panel title "Indus
  Script Decipherment" is the program's name for the work,
  not a claim about its completion, and remains.
- `SignsView.tsx` — a "{deciphered} deciphered /
  {undeciphered} undeciphered" count line and an
  "Undeciphered" confidence filter, from the signs API's
  per-sign flags. A different surface from E1's named
  targets; **recorded as an E2/G follow-up**, not changed
  here (no scope creep).
- `CorporaView.tsx` / `CorpusAnalyticsPanel.tsx` —
  deciphered/undeciphered filters and badges over the
  cross-script corpus catalogue (whether a world script's
  reading is established — e.g. a deciphered benchmark
  script), not Indus decipherment claims. Out of E1 scope;
  inventoried only.
- `HelpView.tsx` / `StudiesView.tsx` — documentation and
  study-table uses of "undeciphered" for scripts in
  general. Out of E1 scope; inventoried only.

## Other surfaces serving the withdrawn equivalents

- `backend/glossa_lab/experiment_graph_phase257_294.py`
  declares an `sa_aggregate` output in its historical SA
  experiment-node schemas, and
  `experiment_graph_phase48_55.py` /
  `experiment_graph_phase56_61.py` declare `n_fully_decoded`
  outputs for their historical phase nodes. These are
  graph-node schemas describing historical phase reports
  (H15 machinery), not the dashboard payload or any panel;
  E1.2 covers the dashboard API and the panel's
  consumption only. **Recorded as an E2/G follow-up.**
- Historical phase scripts under `backend/scripts/`
  (phase114–phase278 era) compute or quote the same-named
  values into their own historical report files. They are
  not live serving surfaces; untouched, inventoried here.
- `backend/scripts/foundation_check.py` reads
  `fully_decoded_pct` from a phase summary file as one of
  its data-integrity checks. That is a check over a
  historical data file, not a served display; the
  foundation check is out of E1 scope and unchanged
  (40/0/8 below).

## Evidence (E1.5)

- **Screenshots** (`phase-e1-evidence/`, served locally
  from this worktree's built frontend + backend on
  localhost; the public internet is unreachable from this
  VM, and the panel was scrolled through before capture):
  - `before-desktop-full.png` (1280×800) — the panel as
    served at the base head: "Signs Deciphered 287",
    "SA Confidence 56% aggregate", "Seals Decoded 70%
    1,165/1,670", the "Deciphered signs — 287/287 … (100%)"
    bar, and the "287 signs deciphered" footer, all live.
  - `before-mobile-full.png` (390×844) — same constructions
    on mobile.
  - `after-desktop-full.png` (1280×800) — the panel after
    withdrawal: "Anchor Records 287 / of 713 known ·
    426 gap", "Token Coverage 92%", token-coverage and
    ICIT-inventory bars only; no SA tile, no seals tile,
    no deciphered bar, no footer. Panel structurally
    sound.
  - `after-mobile-full.png` (390×844) — same, mobile:
    tiles stack cleanly, no withdrawn string visible.
  - Viewport variants (`*-viewport.png`) are kept beside
    the full-page captures.
- **Served-payload verification** (against the live
  locally served API, not source): before, `GET
  /dashboard/decipherment` carried `sa_aggregate: 0.561`,
  `fully_decoded_pct: 0.6976`, `n_fully_decoded: 1165` and
  `GET /indus-evidence/claims/aee-scores` carried
  `mean_propagated_score: 0.497641`. After: all four keys
  are **absent** from the served responses; `by_stage` /
  `n_unstamped_stage` are present (above); per-claim
  `aee_score` objects remain with score and band.
- **New tests**: `backend/tests/test_spec029_phase_e1.py`
  (6 tests) pin the payload withdrawals, the kept Phase A
  fields, the summary-mean absence, the per-claim detail
  retention, and the panel-source purge.
- **Frontend tests**: the Playwright decipherment-actions
  spec was run locally against the real locally served
  backend + new build: **24 passed, 1 skipped** (the
  navigation-persistence test self-skips when its target
  view is unavailable, as designed). The full frontend
  suite is CI's Frontend tests (Playwright) job; its
  result is in the gate evidence below.
- **Foundation check**: 40 passed / 0 failed / 8 warnings
  — identical to the pre-change baseline run the same day.
- **Full backend suite** (`pytest backend/tests`, CI's
  GPU-only files excluded as in CI; CI-parity venv, aee
  1.4.0): **1374 passed, 6 skipped, 0 failed** (8m52s) —
  the 1368 passed / 6 skipped merged baseline plus exactly
  this phase's 6 new tests.
- **PR / CI / merge**: PR: BitConcepts/glossa-lab
  **#185** (`impl/029-phase-e1-withdrawals` → `main`).
  CI on the implementation head `ecadd4c8` (workflow run
  38335464696): **all 7 checks success, read from the
  check runs' own conclusions** — Backend tests (pytest)
  pass; Frontend tests (Playwright) pass; Evidence Graph
  script smoke tests pass; Indus public validation
  checks pass; Shell wrappers (ubuntu-latest,
  macos-latest, windows-latest) pass. This record's
  gate-evidence completion commit re-verifies green on
  the final head before merging (same workflow, all 7
  checks success on the final head — conclusions read
  again after that run). Merge: method `merge`; the
  merge commit SHA and the new main head were verified
  via the GitHub API immediately after merging (a merge
  commit cannot name itself in the content it merges;
  the SHAs are stated in the PR timeline and in this
  phase's delivery report).
- **Lint**: ruff clean on every authored/edited Python
  file.
- **Branding sweep**: no other-company or other-program
  names in any authored or edited file.
- **Frozen bytes**: nothing digest-covered under
  `specs/029-tao-claim-lifecycle/` was edited; this record,
  the evidence directory, the LEDGER entry, and the new
  test file are the phase's additions. The tracked
  `frontend/dist` build output is rebuilt from the edited
  sources (the repo tracks it and the backend serves it).
  Running the backend suite regenerates extraction
  timestamps in `glossa-indus/claims/extracted_claims/*.json`
  as a pre-existing side effect; those files were restored
  byte-identical before commit.

## Deviations and honest limitations

- **Worktree source**: cloned `--shared` from the Phase J
  worktree as briefed; its local `main` was behind, so the
  branch was cut from the GitHub-fetched `origin/main` at
  the exact brief head `7528ddc5`. No deviation in tree.
- **E1.1's frozen text** also describes the replacement
  ("leads with the standing position and the lifecycle
  stage summary under lane-2 labels, with the OD-4
  one-line legend"). Under the phase split the owner
  directed (E1 = withdrawals, E2 = lane-separated
  rendering), that replacement is **not** built here; the
  panel keeps its remaining honest content under a neutral
  structural label. This is recorded as the phase's one
  deliberate partial reading of the frozen task text, for
  E2 to complete.
- **Port note**: port 8001 on this VM was already held by
  a backend serving a different (stale) tree, left
  untouched; all local serving and verification for this
  phase ran on port 8002 from this worktree.
- **Local Playwright browser**: the browser download for
  this repo's Playwright version is unreachable from this
  VM; local e2e and screenshots used the Chromium build
  already present in the local Playwright cache. CI
  installs its own browser and is the authoritative
  frontend gate.

---

*AI disclosure: executed by an AI agent (Muse Spark, via Muse)
at the direction of Tristen Pierson, per constitution §VI.*
