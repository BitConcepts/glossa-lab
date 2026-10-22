# Spec 033 — Plan

> ## PLAN — FOR FREEZE — 2026-10-13
>
> Written against the governing record: the adopted
> lane-2 record for
> `parpola_2010_dravidian_solution_manual_001`
> (explanation and not-understood texts adopted by the
> owner 2026-10-13) and design D-03 of the
> experiment-design portfolio of 2026-10-13 (draft
> PR #195). The owner's freeze order of 2026-10-13
> (06:39 EDT) commissions this freeze; execution
> (Phase-397) runs after the OSF registration of this
> frozen contract verifies public, and no task in
> `tasks.md` is itself an execution.

**Governing documents:** `spec.md`, `claims.json`, and
`adjudication.md` in this directory; the portfolio's
`01-language-and-position.md` (design D-03) and its
README (classification and priority record); the
Phase-41/43 margins as recorded in
`docs/ledger-archive.md`; the Phase-107 falsification
record; Spec 031/032 freeze records (house freeze
precedent); the Glossa constitution; governance H1,
H2, H6, H13, H15/H23, H21, H26.

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
   test_spec033_freeze.py`), and the freeze AEE note.
   House gates: foundation check 0 failures, full
   backend suite green, branding sweep, CI verified
   from run conclusions.
3. **OSF registration** — the frozen contract filed
   before any execution, mirroring the Stage 1
   (pnqrx), Phase-393 (7m35w), Spec 030 (bge3k),
   Spec 031 (jtwvc), and Spec 032 filings; the
   registration-record PR is left open with the
   pending state, and is completed by append once the
   approval verifies.
4. **Execution** — not in this plan's performing
   scope. Phase-397's shape is frozen in spec §9 for
   the execution that follows the verified approval.

## 2. Margins discipline

The verdict margins are the design's, set from the
recorded originals (Phase-41: 1.0566 to 1; Phase-43:
0.484 log units per sign) so the rerun can fail the
claim: the 0.10-log-unit bar and the 99th-percentile
rule were fixed in the design, not fitted at freeze
time. The one freeze-time fixing is the estimator
(spec §5), which the design itself prescribes. The
strict-set census (287 anchors; 94
`strict_sa_independent`) is counted from the anchors
file and pinned by the freeze tests. The freeze
computes no score.

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

- The rerun may return NOT SUPPORTED, replacing a
  six-month-old partial support. That outcome is the
  design working as intended, not a defect (spec §6).
- The Harappa-removed sensitivity may reverse the
  ranking; the frozen consequence is INCONCLUSIVE
  (F033-C12), not a negotiated verdict.
- The random-assignment distribution may reach
  Dravidian's range; the frozen consequence is NOT
  SUPPORTED (F033-C11), however the family ordering
  falls.
