# Tasks — Spec 014 / Phase-115

- [ ] T1 Diagnosis of v1 layer loss (corpus-level; spec §1)
- [ ] T2 Spec 014 (spec/plan/tasks) frozen in its own commit
- [ ] T3 Layer builder `phase115_build_layer_v2.py`; layer built,
      stats asserted vs spec §2, byte-identical rebuild verified
- [ ] T4 `phase115_battery.py` (T1 v2 over spec-011 machinery)
      + `phase115_run.py` orchestration
- [ ] T5 Unit tests incl. toy end-to-end controls + H23 assertion
- [ ] T6 H23: graph module + registration + ATOMIC_NODES assertion
- [ ] T7 Runner `phase115_nonsa_battery_v2.py`
- [ ] T8 Calibration executed; gate outcome recorded verbatim
- [ ] T9 Main run on FLAGGED44 — ONLY if both gates pass
- [ ] T10 Results JSON + summary MD (+ change register iff T9 ran)
- [ ] T11 Full suite + foundation check; ruff clean
- [ ] T12 Ledger entries (both files, AI disclosure)
- [ ] T13 PR opened (no merge)
