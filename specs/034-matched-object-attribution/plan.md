# Spec 034 — Plan

> ## PLAN — FOR FREEZE — 2026-10-13
>
> Written against the governing record: the settled
> Phase-125/127/131 record set and design D-20 of the
> experiment-design portfolio of 2026-10-13 (draft
> PR #195). The owner's freeze order of 2026-10-13
> (06:39 EDT) commissions this freeze; execution
> (Phase-398) runs after the OSF registration of this
> frozen contract verifies public, and no task in
> `tasks.md` is itself an execution.

**Governing documents:** `spec.md`, `claims.json`, and
`adjudication.md` in this directory; the portfolio's
`04-study-headlines.md` (design D-20) and its README
(classification and priority record);
`reports/phase125_cross_compilation_summary.md`,
`reports/phase127_cross_compilation_diagnostic.md`,
`reports/phase131_attribution.md`,
`reports/phase124_cisi_image_layer.md`, and
`reports/phase128_evidence_dossiers_44.csv`;
Spec 031/032/033 freeze records (house freeze
precedent); the Glossa constitution; governance H1,
H2, H6, H13, H15/H23, H21.

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
   test_spec034_freeze.py`), and the freeze AEE note.
   House gates: foundation check 0 failures, full
   backend suite green, branding sweep, CI verified
   from run conclusions.
3. **OSF registration** — the frozen contract filed
   before any execution, mirroring the Stage 1
   (pnqrx), Phase-393 (7m35w), Spec 030 (bge3k),
   Spec 031 (jtwvc), and Spec 032 (3htn8) filings;
   the registration-record PR is left open with the
   pending state, and is completed by append once the
   approval verifies.
4. **Execution** — not in this plan's performing
   scope. Phase-398's shape is frozen in spec §9 for
   the execution that follows the verified approval.

## 2. Numbers discipline

Every number in the contract is the design's, and
each was verified against its record at design time:
286 pairs / 16 judgeable / median TV 0.636931
(Phase-125 summary); noise 0.083 (Phase-127); 6.1%
attributed and 0 shared artifact keys (Phase-131);
7,705 catalogue rows (Phase-124 report); 44 dossiers
(the dossiers CSV row count); 762 crosswalk pairs
with 383 conflict pairs (the portfolio record and
the Phase-125 sensitivity arm). The freeze tests pin
the record files so a later edit to a cited record
is visible. The freeze matches no objects and
computes no distance.

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

- The bridge may come in under the gate; the frozen
  consequence is the census closure (F034-C05), which
  is a designed outcome — the first measured account
  of the join's limits — and not a defect.
- The matched subset may be strongly selected; the
  frozen mitigation is the mix comparison carried in
  the verdict statement (F034-C12), not a correction
  factor invented at outcome time.
