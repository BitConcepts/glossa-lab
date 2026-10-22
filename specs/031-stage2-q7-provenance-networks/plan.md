# Spec 031 — Plan

> ## PLAN — FOR FREEZE — 2026-10-13
>
> Written against the governing record: Spec 027
> §8.1 and the Stage 2 / Q7 adjudication
> (`stage2-q7-adjudication.md`, adopted 1B/2B/3A/4A/
> 5A/6A, 2026-10-12) plus the completed D8 audit
> (`stage2-d8-audit.md`). The owner's order of
> 2026-10-13 commissions the design and its freeze;
> execution (Phase-395) is not ordered and no task in
> `tasks.md` is an execution authorisation.

**Governing documents:** `spec.md`, `claims.json`,
and `adjudication.md` in this directory; Spec 027's
spec, stage1-freeze (statistics and NOT ESTIMABLE
precedent), stage2-q7-adjudication-packet,
stage2-q7-adjudication, and stage2-d8-audit;
Spec 030's freeze record (house freeze precedent);
the Glossa constitution; governance H1, H2, H6,
H13, H15/H23, H21.

**Tooling record:** specify CLI 1.0.10 (setup and
extension management only); AEE extension v1.1.0;
evaluator extension v1.0.0; AEE package 1.0.4 from
the Glossa venv first on PATH for every AEE
invocation (the spec-kit venv carries 1.0.2; PATH is
stated and pinned per invocation, per the Spec 028
precedent).

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
   test_spec031_freeze.py`), and the freeze AEE note.
   House gates: foundation check 0 failures, full
   backend suite green, branding sweep, CI verified
   from run conclusions.
3. **OSF registration** — the frozen contract filed
   per adopted 6A, mirroring the Stage 1 (pnqrx),
   Phase-393 (7m35w), and Spec 030 (bge3k) filings;
   the registration record is filed after the
   approval verifies (a separate record PR).
4. **Execution** — not in this plan's scope.
   Phase-395's shape is frozen in spec §7 for the
   later owner order.

## 2. Margins discipline

Every quantitative rule in the design traces to a
margin in the D8 audit or the Stage 0 record (spec
§2). The design computes no link, no similarity, and
no response; digitisation begins only under the
later execution order (D8 audit's closing boundary).
Design decisions forced by the margins are recorded
as DD-1…DD-8 (spec §10, adjudication §2), each
flagged as taken under the adopted 5A mandate.

## 3. Freeze sources

The freeze digest covers `freeze.md`, `spec.md`,
`claims.json`, `adjudication.md`, the AEE recovery
record (if any) and freeze note under `aee/`,
`build_freeze.py`, and the freeze test. `plan.md`
and `tasks.md` are bookkeeping and are **not**
digest-covered (the Spec 029/030 bookkeeping rule):
their checkbox state may change at closeout without
drifting the freeze.

## 4. Risks named in advance

- The primary link mass may prove too sparse at
  execution's margins step; the frozen consequence
  is NOT-YET-TESTABLE per arm (spec §4.3), which is
  a valid negative closure, not a defect.
- The ceramic arm may close NOT ESTIMABLE at
  margins (spec §4.2); that outcome is pre-registered
  by DD-7, not a surprise.
- The drop-Harappa jackknife cell is the expected
  pressure point (spec §2); the verdict rules route
  a Harappa-dependent effect to INCONCLUSIVE.
