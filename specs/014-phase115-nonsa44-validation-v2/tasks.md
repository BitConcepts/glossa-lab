# Tasks — Spec 014 / Phase-115

- [x] T1 Diagnosis of v1 layer loss (corpus-level; spec §1) — leading-zero
      key mismatch 4,014 tokens; all-or-nothing rule; placeholders 1,898;
      residual unmapped 1,524
- [x] T2 Spec 014 (spec/plan/tasks) frozen in its own commit (`fddd4dbf`)
- [x] T3 Layer builder `phase115_build_layer_v2.py`; layer built —
      4,531 inscriptions / 13,492 mapped tokens / 91.554% coverage,
      asserted vs spec §2; byte-identical rebuild verified
      (sha256 f837a15a333f44f4261955fda626d372b23b1b10082fe9afb9b6268b6f8aa99f)
- [x] T4 `phase115_battery.py` (T1 v2 over spec-011 machinery)
      + `phase115_run.py` orchestration (`59e7b6fa`)
- [x] T5 Unit tests incl. toy end-to-end controls + H23 assertion (24 passed)
- [x] T6 H23: graph module + registration + ATOMIC_NODES assertion
- [x] T7 Runner `phase115_nonsa_battery_v2.py`
- [x] T8 Calibration executed; gate outcome recorded verbatim —
      **STRICT94 gate FAILED (VALIDATED 1/94, required ≥ 57); KUR113 gate
      passed (0/113, ≤ 5). Battery REJECTED per spec §5.**
- [ ] T9 Main run on FLAGGED44 — **NOT EXECUTED (frozen stop rule: a
      rejected battery never runs on the 44; anchors file untouched)**
- [x] T10 Results JSON + summary MD (incl. post-hoc diagnosis, labeled)
- [x] T11 Full suite (697 passed / 11 skipped / 0 failed) + foundation check (40 / 0 / 8); ruff clean
- [x] T12 Ledger entries (both files, AI disclosure)
- [ ] T13 PR opened (no merge)
