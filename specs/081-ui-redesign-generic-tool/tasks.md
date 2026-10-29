# Tasks: UI Redesign — Glossa Lab as a Generic Program Tool

## Phase 1 — design package (this branch; no application code)

- [x] T001 Inventory the entire current UI from origin/main @ f8827fb2: shell, all 21 tabs + supporting components, orphaned components, project data model, claims doctrine in code, tray surfaces → `inventory.md`
- [x] T002 Spec 081 draft: spec.md (problem, stories, FR-001…020, claims summary, phase-2 outline, assumptions, open questions Q1–Q10 with recommendations), plan.md, tasks.md, aee-claims.json (C081-1…12, each with evidence + falsifier)
- [x] T003 Wireframe design system: `wireframes/wireframes.css` (brand navy/accent carried over; verdict + stage chip vocabularies; framed-log and missing-act patterns; responsive shell with mobile bottom nav)
- [x] T004 Wireframes 01–03: tool home / program list; program home (Indus specimen); claims register
- [x] T005 Wireframes 04–05: claim detail (two-lane, falsifier, contest cap); digestion board (columns by act owed, missing-act on every card)
- [x] T006 Wireframes 06–08: evidence & sources; data (corpora + anchor sets as peers); experiments (canvas craft kept, framing changed)
- [x] T007 Wireframes 09–11: jobs (single tool-level queue, failures at full prominence); discovery inbox (epistemic fence); research loop (first-class, ceiling stated, staging fenced)
- [x] T008 Wireframes 12–14: reports & ledger (append-only, publication states honest); settings (tool vs program split); status (identity first, session-framed log)
- [x] T009 Wireframe 15: tray spec sheet (icon states, menu, tooltip, status lines incl. stopped-by-user and limit-reached; single-instance; program named)
- [x] T010 Wireframes 16–17: empty states — no program yet (create/import); program with data but no claims (teach + first claim)
- [ ] T011 Screenshots: Playwright renders of all 17 screens at desktop 1440 + mobile 390 → `wireframes/shots/` *(blocked at first attempt 2026-10-29 by the VM's browser-launch state — headless Chromium/Firefox processes die under the current platform write restriction; `wireframes/render-shots.py` is the ready-to-run script; re-run when browser launches work)*
- [x] T012 Owner review: APPROVED as recommended (Q1–Q10) 2026-10-29 on the HTML package; rulings recorded as spec.md Amendment 1; phase 2 unblocked. (T011 PNG renders owed as a record; superseded as a gate by phase-2 built-UI screenshot verification.)

## Phase 2 — build (starts only after T012)

- [x] T013 Shell & routing per FR-001/002/018 (spec outline step 1) — PR-2 (feat/081-shell-programs): two-space nav, switcher card (Q1), service chip, hash deep links, legacy alias resolution
- [x] T014 Program model presentation + import (step 2) — PR-2: ProgramsView tool home + first run (wireframes 01/16), question field (backend, schema V24)
- [ ] T015 Claims surface + endpoint generalization with one-release shim (step 3; Q7 ruling applied)
- [ ] T016 Digestion board (step 4)
- [ ] T017 Program home; Dashboard retired (step 5)
- [ ] T018 Evidence & Data consolidation; Analysis route (step 6)
- [ ] T019 Jobs / Status / Settings / Research-loop surfaces; BottomPanel removed (step 7)
- [ ] T020 Tray amendments + extended contract tests + desktop verify (step 8)
- [ ] T021 Dead-code removal with ledger note (step 9)
- [ ] T022 Verification: C081-1…12 checks, screenshot pass vs approved wireframes, CI-parity suite, foundation check, CHANGELOG + LEDGER (step 10)
