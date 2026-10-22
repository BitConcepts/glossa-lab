# FREEZE — Spec 033 (SA-Free Language Comparison)

- **Spec:** specs/033-sa-free-language-comparison/
- **Freeze date:** 2026-10-13
- **Freeze digest:** recorded in `freeze.json` (framework026 digest, built by `build_freeze.py` from the DEFINITION and SOURCES it carries)
- **Governed claim register:** claims.json,
  register_version 0.4-draft — **15 claims**
  (F033-C01…C15), recovered through three AEE rounds
  (9, then 5, then 1 failure modes; record in
  `aee/recovery-specify.md`) and passed at
  after_specify, after_plan, and after_tasks
  (0 failure modes; `aee/assess-specify.json`).
- **Adjudication:** `adjudication.md` — the design
  commission of 2026-10-13, the owner's freeze order
  of 2026-10-13 06:39 EDT ("Freeze D-30, D-03, and
  D-20 for execution"), and the freeze-time estimator
  fixing the design prescribes (§2). Design merged as
  PR #203 (`c1cad78e`).

## 1. What is frozen

The contract that scores
`parpola_2010_dravidian_solution_manual_001` again
without the machinery that produced its partial
support: Proto-Dravidian word-values against
Indo-Aryan (Sanskrit), Munda, and a no-language
baseline on the strict sign set, with 999 random
assignments as the no-information control — no
semantic anchoring, no anchor promotion, and no
SA-derived quantity anywhere in the pipeline (H26).
The estimator fixed at freeze time (counted
conditional model, add-one smoothing, mean log
probability per sign, identical for every family and
control) is part of the frozen text (spec §5).

## 2. Frozen sources

`freeze.md`, `spec.md`, `claims.json`,
`adjudication.md`, `aee/recovery-specify.md`,
`aee/freeze-aee-note.md`, `build_freeze.py`, and
`backend/tests/test_spec033_freeze.py`. `plan.md` and
`tasks.md` are bookkeeping and are NOT digest-covered
(Spec 029/030 rule).

## 3. The frozen rules (definition constants)

| Constant | Value |
|---|---|
| Execution phase | Phase-397 |
| Claims | 15 (F033-C01…C15) |
| SUPPORTED margin | ≥ 0.10 log units per sign over the best rival |
| Random-distribution bar | above the 99th percentile |
| Random controls | 999 assignments, same pass |
| Sign set | strict set only (94 of 287 anchors, `strict_sa_independent`) |
| Estimator | counted conditional model, add-one smoothing, spec §5 |
| Verdict basis | the primary run; the Harappa-removed sensitivity can only route to INCONCLUSIVE |

## 4. House gates at freeze

- AEE: pass at all three lifecycle phases over the
  frozen register (see `aee/freeze-aee-note.md`).
- Freeze tests: digest replay + definition constants
  + register integrity + the strict-set census
  counted from the anchors file (287 total, 94
  strict) + the recorded original margins (Phase-41
  1.0566; Phase-43 0.484) — `backend/tests/
  test_spec033_freeze.py`.
- Foundation check: 0 failures (foundation report
  verified at the freeze PR).
- Full backend suite: green at the freeze PR (CI
  verified from run conclusions).

## 5. What this freeze does NOT do

- It computes no score and runs no family. Execution
  is Phase-397, gated on the OSF registration of this
  frozen contract verifying public.
- It does not alter the claim's existing record: the
  lane-2 explanation and not-understood texts adopted
  2026-10-13 stand; the status consequence of the
  rerun, when it exists, is appended as a dated entry
  at execution.
- It does not touch the Spec 026–032 frozen records
  or the sibling fish-sign claim (design D-04).

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
