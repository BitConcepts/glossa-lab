# Plan — Spec 084 POLICY-SYNC Conformance

**Date**: 2026-10-31
**Branch**: `spec/084-policy-sync`
**Proposal basis**: the owner's POLICY-SYNC standing directive
(2026-10-31) — in this repo's governance terms this spec is the
proposal (H2) and its Assumptions section carries the epistemic
boundaries (H13). The Phase 1 inventory precedes the build:
`files/2026-10-31-policy-sync-inventory.md` (goal workspace).

## Steps

1. **Inventory** (done, 2026-10-31): every claims-bearing text on
   the app SPA, the tray, the cloud edge + cloud SPA, and the
   public tracker, with approval status, existing coverage, and
   whether a falsifier executes today.
2. **Fixtures** for the six texts whose approval is on record and
   whose falsifier executes today (standing position, stage-count
   framing, edge robots, edge noindex, token-gate copy, tray
   status copy) — `fixtures/`, header carries the approval
   citation, body is the verbatim approved text after `# ---`.
3. **Conformance tests** —
   `backend/tests/test_policy_sync_conformance.py`, pytest, in the
   existing Backend tests CI job. Presence checks compare the
   fixture body against the surface source (exact for the seeder
   record, via import; whitespace-normalized substring for TSX /
   TS / tray sources; literal-decode for the edge robots body).
   Absence checks scan `frontend/src` + `cloud/` + backend served
   strings for the superseded 161 framing, and `frontend/src` for
   the D4-removed component files/imports and
   REAL_CATALOG_SUMMARY.
4. **HELD claims** entered in spec + `aee-claims.json` with
   reasons; no tests written for them.
5. **Records**: LEDGER.md entry (H1); coverage table filed in the
   goal workspace (`files/2026-10-31-policy-sync-coverage.md`).
6. **PR** on per-job CI green; the parent merges on green +
   delivery-checker RESOLVED. Main's pre-existing freeze-gate C4
   red (Spec 075 record defect, named 2026-10-31) is out of scope
   and untouched.

## Verification

- The new pytest module passes locally in the CI-faithful venv
  before push, and the Spec 029 E2 pin test still passes (the
  fixture regime extends its fragment assertion to the full text;
  it does not replace it).
- Each fixture was checked present verbatim in today's source
  before being written; each absence target was checked absent.
  The tests therefore pass on today's tree and fail on drift in
  either direction — the property the directive asks for.
