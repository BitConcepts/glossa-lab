# Spec 032 — Plan

> ## PLAN — FOR FREEZE — 2026-10-13
>
> Written against the governing record: the PRED
> register entry for PRED-2026-006
> (`docs/PREDICTION_REGISTER.md`, registered
> 2026-04-22) and design D-30 of the experiment-design
> portfolio of 2026-10-13 (draft PR #195). The owner's
> freeze order of 2026-10-13 (06:39 EDT) commissions
> this freeze; execution (Phase-396) runs after the OSF
> registration of this frozen contract verifies
> public, and no task in `tasks.md` is itself an
> execution.

**Governing documents:** `spec.md`, `claims.json`, and
`adjudication.md` in this directory; the PRED register;
the portfolio's `05-predictions.md` (design D-30) and
its README (classification and priority record);
Spec 031's freeze record (house freeze precedent);
the Glossa constitution; governance H1, H2, H6, H13,
H15/H23, H21, H26.

**Tooling record:** specify CLI 1.0.10 (setup and
extension management only); AEE extension v1.1.0;
evaluator extension v1.0.0; AEE package 1.0.4 from the
Glossa venv first on PATH for every AEE invocation
(the spec-kit venv carries 1.0.2; PATH is stated and
pinned per invocation, per the Spec 028 precedent).

## 1. Sequence

1. **Design PR** — `spec.md`, `claims.json`,
   `adjudication.md`, `plan.md`, `tasks.md`, the AEE
   lifecycle artifacts under `aee/`, and the LEDGER
   entry. Claims first; the AEE hook pass
   (after_specify / after_plan / after_tasks) must
   return **pass** before the design PR merges; an
   outcome stricter than `warn` blocks until the
   recovery it names is complete and recorded
   (Spec 026 rule; Spec 030 recovery pattern).
2. **Freeze PR** — `freeze.md`, `freeze.json`
   (framework026 digest via `build_freeze.py`), the
   freeze tests (`backend/tests/
   test_spec032_freeze.py`), and the freeze AEE note.
   House gates: foundation check 0 failures, full
   backend suite green, branding sweep, CI verified
   from run conclusions.
3. **OSF registration** — the frozen contract filed
   before any execution, mirroring the Stage 1
   (pnqrx), Phase-393 (7m35w), Spec 030 (bge3k), and
   Spec 031 (jtwvc) filings; the registration-record
   PR is left open with the pending state, and is
   completed by append once the approval verifies.
4. **Execution** — not in this plan's performing
   scope. Phase-396's shape is frozen in spec §10 for
   the execution that follows the verified approval.

## 2. Margins discipline

Every quantitative rule in this design is the
register's (the 70 percent share; the 0.40 start-rate
bar) or the design's own stated constant (the 20
percent unmappable-coverage reporting rule). No number
was fitted at freeze time; the withheld-data census
(5,679 inscriptions; 77 sites; 2,717 Harappa) is
counted from the data file and pinned by the freeze
tests. The freeze computes no start rate and no share.

## 3. Freeze sources

The freeze digest covers `freeze.md`, `spec.md`,
`claims.json`, `adjudication.md`, the AEE recovery
record (if any) and freeze note under `aee/`,
`build_freeze.py`, and the freeze test. `plan.md` and
`tasks.md` are bookkeeping and are **not**
digest-covered (the Spec 029/030 bookkeeping rule):
their checkbox state may change at closeout without
drifting the freeze.

## 4. Risks named in advance

- Step 0.1 may fail: the exact trained set may not be
  reproducible from the record. The frozen consequence
  is the closure CANNOT BE RUN AS WRITTEN — a valid
  negative closure, not a defect to be repaired by
  substitution (F032-C04).
- Step 0.2 may fail on the same terms (F032-C05).
- Unmappable coverage may exceed 20 percent; the
  frozen consequence is the first-sentence coverage
  statement, not a re-based denominator (F032-C07).
