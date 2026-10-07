# Tasks — Spec 009 / Phase-111

- [ ] T001 Spec 009 written and FROZEN in its own commit before any pipeline output exists (pre-registration)
- [ ] T002 Ledger entries recording the freeze: root `LEDGER.md` + `glossa-indus/LEDGER.md` (Phase-111, AI disclosure)
- [ ] T003 Panel acquisition: in-repo inventory + openly-licensed downloads only; `reports/phase111_acquisition_log.json` complete incl. gaps (Elamite, SCA heraldry)
- [ ] T004 Graph module `experiment_graph_phase111.py` + registration in `experiment_graph.py`; node IDs `IndusPhase111BlindGate` / `IndusPhase111BlindClassify` verified in `ATOMIC_NODES` (H23, before any run)
- [ ] T005 `phase111_features.py`: frozen 28-feature extractor (spec §4), numpy-only, deterministic
- [ ] T006 `phase111_custodian.py`: panel build, token remap, synthetics S1–S4, anonymized panel file, key held in gitignored runtime state
- [ ] T007 `phase111_analyst.py`: LDA + gate + verdict logic (spec §§6–10); imports nothing from the custodian
- [ ] T008 `phase111_run.py` orchestrator (panel → gate → stop-or-classify)
- [ ] T009 Unit tests `backend/tests/test_phase111_blind.py` (features, blinding, resampling exactness, gate branches, determinism); full suite green
- [ ] T010 Gate run on known corpora; outcome recorded exactly (pass → continue; fail → STOP, inconclusive path)
- [ ] T011 If gate passed: classification + control validity + unblinding; verdict strictly per spec §9 V6 vocabulary
- [ ] T012 Results: `reports/phase111_blind_affiliation_results.json` + `reports/phase111_blind_affiliation_summary.md`
- [ ] T013 Foundation check 0 failures (H21); ruff clean on new Python
- [ ] T014 Ledger entries with gate outcome + verdict verbatim; PR opened (NOT merged)
