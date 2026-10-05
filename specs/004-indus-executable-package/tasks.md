# Tasks 004 — Indus executable package

## Proposal
- [x] T001 Read AGENTS.md, constitution, governance rules
- [x] T002 Create branch `feat/indus-executable-package` from main d9613595
- [x] T003 Write specs/004 (spec / plan / tasks)

## WS1 — Phase-52 syllabic SA run
- [ ] T010 Verify `IndusConstrainedSA` node registration
- [ ] T011 Execute node via experiment-graph machinery (timeout-bounded)
- [ ] T012 Verify result artifacts at `reports/phase52_syllabic_sa.json`
- [ ] T013 Re-run foundation check; CHECK NEW-F passes, warning gone
- [ ] T014 Ledger Phase-106 (glossa-indus) with actual SA findings

## WS2 — Crosswalk expansion
- [ ] T020 Audit v2 crosswalk composition (evidence vs identity-inferred)
- [ ] T021 Mine in-repo equivalence sources (phase51/56 outputs, phase65/71 tables, v1, iconographic anchors, phase220, Yajnadevam bridge)
- [ ] T022 Add evidence-backed entries (each with `evidence` field)
- [ ] T023 Write candidates file for identity-only / plausible pairs
- [ ] T024 Regenerate v2 `stats`; verify loader + API check count
- [ ] T025 Phase-104 blocked-claims addressability report (no re-adjudication)

## WS3 — Anchors reconciliation
- [ ] T030 Hash `anchors` mapping (before)
- [ ] T031 Regenerate all summary/bookkeeping fields from entries
- [ ] T032 Record canonical count definitions in metadata
- [ ] T033 Hash `anchors` mapping (after) — identical
- [ ] T034 Foundation check anchors checks pass

## WS4 — Discovery triage
- [ ] T040 Read discovery pipeline conventions/status vocabulary
- [ ] T041 Pull the status=new queue (expect 78) via API
- [ ] T042 Disposition every item via pipeline mechanisms
- [ ] T043 Report counts by topic × disposition + unprocessable items

## Close-out
- [ ] T050 Full backend test suite (exact counts)
- [ ] T051 Foundation check full run (exact result)
- [ ] T052 Ruff on changed Python files
- [ ] T053 Root LEDGER.md summary entry (AI disclosure)
- [ ] T054 Push branch, open PR (do NOT merge)
