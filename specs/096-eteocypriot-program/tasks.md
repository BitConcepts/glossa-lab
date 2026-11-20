# Spec 096 — tasks

## Adoption (this PR)

- [x] **T001 — the package lands.** spec.md, claims.md,
  aee-claims.json (C096-1..C096-4, each with a falsifier),
  plan.md, tasks.md, and the adoption record, on branch
  `feat/096-eteocypriot-program-setup`. The founding Spec 095
  scoping documents are cited as provenance and not edited.
- [x] **T002 — AEE assessment of the package.** The bundle is
  validated and assessed under the pinned assessor; the output
  is filed verbatim at `records/adoption-aee-assessment.json`
  and read in the adoption record, never edited.
- [x] **T003 — owner direction.** The owner directed the
  program's setup as its own separate program, and lifted the
  pilot's execution gate, in chat on 2026-11-20.
  `records/adoption-record-2026-11-20.md`.
- [x] **T004 — claims-ledger intake and program-map
  assignment, inside this PR (D-096-2, D-096-4).** (a) the
  program-map assignment is entered in
  `glossa-indus/map/program-map-taxonomy.json` (Program
  infrastructure / Governance, lifecycle & generated layers);
  (b) C096-1..C096-4 are appended to
  `glossa-indus/ledger/claims.jsonl` through
  `tools/ledger/import_bundle.py`, the only sanctioned path,
  never a hand-edit; (c) the generated layers the intake feeds
  are regenerated with the plain generators and the ledger
  validated, with the numbers recorded in the adoption record.

## Stage 1 — Corpus assembly and freeze (D-096-3)

- [ ] **T101 — corpus-availability survey.** Every item of the
  preregistration draft §3.1 resolved or carried as a named
  gap, per inscription, in the freeze record.
- [ ] **T102 — corpus intake and identity record.** The held
  corpus filed at `corpus/corpus.json` under a C095-3 identity
  record: per-inscription SHA-256 pins, counting basis,
  normalization rules, licensing basis.
- [ ] **T103 — freeze.** Census, split, signary frame, frozen
  E1 procedure, rival alignment assumptions, floors
  instantiated (closures at freeze recorded as TOO THIN where
  a floor cannot be met), step-0 closure check. Committed
  before any analysis runs.

## Stage 2 — Registered analysis (D-096-3)

- [ ] **T201 — E1 driver and run.** The driver implements the
  frozen procedure exactly, verifies the corpus pin
  fail-closed, and files its run record verbatim.
- [ ] **T202 — E2/E3 as the freeze provides.** E2 only on its
  precondition and floor; E3 only for survivors; the held-out
  seal is broken only by the preregistration's own procedure.

## Stage 3 — Outcome and adjudication package (D-096-3, D-096-5)

- [ ] **T301 — outcome record.** Per-claim verdicts with
  precision basis, read from the run records; sensitivities
  dispositioned.
- [ ] **T302 — adjudication package preparation.** Prepared
  for the named human approver if the outcome warrants it; no
  external contact (D-096-5).
