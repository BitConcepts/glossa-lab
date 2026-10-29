# Plan: UI Redesign — Glossa Lab as a Generic Program Tool (Spec 081)

Phase 1 (this plan's current state) is design only: inventory, spec, wireframes,
owner approval on the renders. Phase 2 executes the spec's build outline in ten
sequenced steps, each landing green on its own. No step starts before the
owner's wireframe approval is recorded as an amendment to spec.md.

## Phase 1 — design (this branch)

1. Inventory the entire current UI from `origin/main` (frontend routes/views,
   shell, tray surfaces, served structure) → `inventory.md`.
2. Draft spec.md (problem, stories, FR-001…020, claims summary, build outline,
   open questions with recommendations) + aee-claims.json (C081-1…12 with
   evidence + falsifiers).
3. Build 17 full-fidelity wireframes (HTML/CSS, shared stylesheet) with
   per-screen annotations; Indus as the labeled specimen program; a second
   specimen program proving the shell is subject-free.
4. Render screenshots at desktop 1440 and mobile 390 for every screen
   (Playwright) → `wireframes/shots/`.
5. Owner review on the renders → rulings on open questions Q1–Q10 recorded as
   spec amendments → phase 2 unblocked.

## Phase 2 — build (after approval; mirrors spec.md's outline)

| Step | Work | Primary risk | Guard |
|---|---|---|---|
| 1 | Shell & routing (switcher, two-space nav, service chip, aliases redirect) | Deep links / AI-navigation aliases break | Alias redirect tests against the current alias table |
| 2 | Program model presentation (tool home, first-run, import) | Legacy projects mis-imported | Import report lists every item + destination; nothing renamed silently |
| 3 | Claims surface + endpoint generalization (`/indus-*` → program-scoped, shim one release) | External/MCP callers of old paths | Shim + deprecation note in CHANGELOG; MCP tool tests |
| 4 | Digestion board (missing-act derivation over existing records) | Derivation disagrees with Spec 029 stage rules | Derivation table reviewed against StageLegend semantics; contract tests per stage |
| 5 | Program home (Dashboard retired; loop panel extracted; SA/decipher panels off home) | Embedded-panel state (loop scheduler) lost in extraction | Loop state read from backend at the new route; no localStorage-only state |
| 6 | Evidence & Data consolidation (tabs merge; anchors promoted; Analysis route) | Deep links into old tabs | Tab-state deep links mapped to new tab ids |
| 7 | Jobs/Status/Settings/Loop surfaces (BottomPanel removed; identity-first status) | Log consumers of the bottom panel | Session-log SSE endpoint reused by Status; panel removal noted in CHANGELOG |
| 8 | Tray amendments (program name, humanized uptime, single instance, status door) | Supervision regression on Windows | Spec 079/080 tray contract tests extended, not replaced; desktop verify markers re-run |
| 9 | Dead-code removal (8 orphaned components) | A hidden dynamic import | Repo-wide reference search in CI before merge |
| 10 | Verification (claims C081-1…12 → tests/screenshot checks; CI parity; foundation check; LEDGER) | Renders drift from build | Screenshot diff pass filed in this spec folder (Spec 029 evidence pattern) |

## Sequencing notes

- Steps 1–2 are pure presentation over the existing data model and can ship
  before any backend change; step 3 is the only step that touches API shape.
- The tray (step 8) ships with the desktop installer discipline of Specs
  079/080: contract tests first, desktop verify markers after.
- If the owner rules against Q7 (hypotheses fold-in), step 3 keeps the tracker
  as a separate surface with its vocabulary aligned to the verdict set — the
  rest of the plan is unaffected.
