# Tasks 004 — Indus executable package

## Proposal
- [x] T001 Read AGENTS.md, constitution, governance rules
- [x] T002 Create branch `feat/indus-executable-package` from main d9613595
- [x] T003 Write specs/004 (spec / plan / tasks)

## WS1 — Phase-52 syllabic SA run
- [x] T010 Verify `IndusConstrainedSA` node registration
- [x] T011 Execute node via experiment-graph machinery (timeout-bounded)
- [x] T012 Verify result artifacts at `reports/phase52_syllabic_sa.json`
- [x] T013 Re-run foundation check; CHECK NEW-F passes, warning gone
- [x] T014 Ledger Phase-106 (glossa-indus) with actual SA findings

## WS2 — Crosswalk expansion
- [x] T020 Audit v2 crosswalk composition (evidence vs identity-inferred)
- [x] T021 Mine in-repo equivalence sources (phase51/56 outputs, phase65/71 tables, v1, iconographic anchors, phase220, Yajnadevam bridge)
- [x] T022 Add evidence-backed entries (each with `evidence` field)
- [x] T023 Write candidates file for identity-only / plausible pairs
- [x] T024 Regenerate v2 `stats`; verify loader + API check count
- [x] T025 Phase-104 blocked-claims addressability report (no re-adjudication)

## WS3 — Anchors reconciliation
- [x] T030 Hash `anchors` mapping (before)
- [x] T031 Regenerate all summary/bookkeeping fields from entries
- [x] T032 Record canonical count definitions in metadata
- [x] T033 Hash `anchors` mapping (after) — identical
- [x] T034 Foundation check anchors checks pass

## WS4 — Discovery triage
- [x] T040 Read discovery pipeline conventions/status vocabulary
- [x] T041 Pull the status=new queue (expect 78) via API
- [x] T042 Disposition every item via pipeline mechanisms
- [x] T043 Report counts by topic × disposition + unprocessable items

## Close-out
- [x] T050 Full backend test suite (exact counts)
- [x] T051 Foundation check full run (exact result)
- [x] T052 Ruff on changed Python files
- [x] T053 Root LEDGER.md summary entry (AI disclosure)
- [x] T054 Push branch, open PR (do NOT merge)
