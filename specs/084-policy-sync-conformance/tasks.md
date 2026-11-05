# Tasks — Spec 084 POLICY-SYNC Conformance

- [x] T001 Phase 1 inventory of all claims-bearing web-surface
      texts, with approval status and falsifier executability
      (goal-workspace `files/2026-10-31-policy-sync-inventory.md`).
- [x] T002 Fixtures F1–F5 (six files) with approval citations in
      headers: standing position, stage-count framing, edge
      robots, edge noindex, token-gate copy, tray status copy.
- [x] T003 Conformance tests (presence) in
      `backend/tests/test_policy_sync_conformance.py` for
      C084-1…C084-5.
- [x] T004 Absence tests for C084-6 (superseded 161 framing) and
      C084-7 (D4-removed surfaces + REAL_CATALOG_SUMMARY).
- [x] T005 HELD claims C084-8…C084-11 entered in spec.md and
      aee-claims.json with reasons; no tests invented for them.
- [x] T006 aee-claims.json for Spec 084 (C084-1…C084-11, each with
      a falsifier or a recorded hold).
- [x] T007 LEDGER.md entry for the spec's landing.
- [x] T008 Coverage table filed in the goal workspace
      (`files/2026-10-31-policy-sync-coverage.md`).
- [ ] T009 PR merged on per-job CI green + delivery-checker
      RESOLVED (parent's act).
- [x] T010 Fixtures + tests for the cloud anonymous-surface copy
      (C084-8 activation). Condition met: `frontend/src/cloud/`
      landed on main in PR #476 (2026-11-01). Activated on the
      owner's approval act, 2026-11-05: fixture
      `fixtures/cloud-anonymous-surface-copy.txt` (7 approved
      strings; approval citations in its header — Spec 083
      wireframe package PR #463; the 2026-10-31 parent decisions
      on Phase 3 deviations 1 and 6, Spec 083 BUILD-RECORD) and
      tests `test_cloud_anonymous_surface_copy_matches_fixture` +
      `test_superseded_reset_link_promise_absent` in
      `backend/tests/test_policy_sync_conformance.py`. FR-084-09
      added; C084-8 recorded ACTIVATED in spec.md (the
      aee-claims.json bundle stands as intaken, per the intake
      discipline).
- [ ] T011 (owner-gated follow-on) Privacy / data-handling text
      for the app (inventory gap A4) — enters this regime when an
      owner-approved text exists.
