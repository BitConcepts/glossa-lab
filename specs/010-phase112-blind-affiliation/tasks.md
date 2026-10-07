# Tasks — Spec 010 / Phase-112

- [ ] T001 Design stage: candidate order-carrying features (`phase112_features.py`), toy permutation-sensitivity tests, permutation-sensitivity audit on known corpora only (`reports/phase112_feature_audit.json`); drops recorded
- [ ] T002 Spec 010 written and FROZEN in its own commit (with ledger freeze entries) after the audit, before any panel build, gate run, or Indus statistic (pre-registration)
- [ ] T003 Acquisition record: `reports/phase112_acquisition_log.json` — panel inherited from spec 009 as assembled; sources staged locally under gitignored `sources/phase112/`; gaps restated (K6, N2, Elamite, SCA heraldry)
- [ ] T004 Graph module `experiment_graph_phase112.py` + registration in `experiment_graph.py`; node IDs `IndusPhase112BlindGate` / `IndusPhase112BlindClassify` verified in `ATOMIC_NODES` (H23, before any run)
- [ ] T005 `phase112_features.py` restricted to the admitted set frozen in spec §4 (definitions unchanged from the audited candidates)
- [ ] T006 `phase112_custodian.py`: panel build (frozen spec-009 loaders/chunking/resampling reused by import), token remap, synthetics S1–S5 (S5 per spec §5), anonymized panel file, key in gitignored runtime state
- [ ] T007 `phase112_analyst.py`: LDA + gate + control validity (S1–S5) + verdict logic (spec §§6–10); imports nothing from any custodian
- [ ] T008 `phase112_run.py` orchestrator (panel → gate → stop-or-classify)
- [ ] T009 Unit tests extended in `backend/tests/test_phase112_blind.py` (blinding, resampling exactness, gate branches, S5 determinism/shape, determinism); full suite green
- [ ] T010 Gate run on known corpora; outcome recorded exactly (pass → continue; fail → STOP, inconclusive path)
- [ ] T011 If gate passed: classification + control validity over S1–S5 + unblinding; verdict strictly per spec §9 V6 vocabulary
- [ ] T012 Results: `reports/phase112_blind_affiliation_results.json` + `reports/phase112_blind_affiliation_summary.md` (incl. feature permutation-sensitivity audit table)
- [ ] T013 Foundation check 0 failures (H21); ruff check clean on new Python
- [ ] T014 Ledger entries with gate outcome + verdict verbatim; PR opened (NOT merged)
