# Spec 032 — Freeze Record (PRED-2026-006: The Harappa Breakdown)

> ## FROZEN at the Spec 032 freeze merge (2026-10-13)
>
> Basis: design **D-30** of the experiment-design
> portfolio of 2026-10-13 (draft PR #195), commissioned
> by the owner's order of 2026-10-13 ("Design
> experiments for all of the 35 that remain in question
> or inconclusive") and adjudicated for freeze by the
> owner's order of 2026-10-13 06:39 EDT, verbatim
> **"Freeze D-30, D-03, and D-20 for execution"**
> (`adjudication.md`). The governed claim register
> enters this freeze as recovered at the design AEE
> pass (`aee/recovery-specify.md`) — the freeze digest
> below covers the recovered register, never the
> pre-recovery one. The machine freeze record is
> `freeze.json` (framework026 digest, built by
> `build_freeze.py`).

## 1. What is frozen

- **The registered test, exactly as registered.**
  `spec.md`: PRED-2026-006 (registered 2026-04-22) is
  scored on its own criterion — at least **70%** of
  the CISI-trained INITIAL signs show a start rate of
  at least **0.40** at Harappa — computed on the
  withheld Harappa-site Yajnadevam sequences only.
  Nothing is substituted, adjusted, or re-based.
- **Step 0, failing closed.** The trained INITIAL set
  is reconstructed from the recorded
  `global_class_stability.py` lineage and frozen; the
  withholding is verified as CISI Mohenjo-daro only;
  sign identity is carried by the existing crosswalks
  under `data/crosswalks/`, fixed before counting. A
  failed check closes the study as **CANNOT BE RUN AS
  WRITTEN**, reported as itself, never as a verdict.
- **The unmappable rule.** Trained signs with no
  crosswalk counterpart are counted and reported as
  UNMAPPABLE; coverage above **20 percent** of the
  trained set is stated in the verdict's first
  sentence.
- **The verdict mapping, the register's own.**
  CONFIRMED at a share of at least 70 percent; NOT
  CONFIRMED below it. No inconclusive band exists in
  the registered criterion and none is invented. The
  per-sign table is pre-registered as a descriptive
  addition only; it carries no criterion.
- **The governed claim register.** `claims.json`,
  register_version `0.4-draft`: 12 claims
  (F032-C01…C12), recovered at the design AEE pass —
  the AEE hook pass over this register returns
  **pass** at after_specify, after_plan, and
  after_tasks (12 claims, 0 failure modes, 0 below
  the 0.70 threshold; `aee/` artifacts).
- **The inputs the design rests on**, pinned by the
  freeze tests from their records: the withheld-data
  census (`yajnadevam_inscriptions.csv`: 5,679
  inscriptions, 77 sites, 2,717 Harappa) and the PRED
  register entry as registered (criterion text; the
  recorded PARTIALLY CONFIRMED outcome; the 72.7
  percent global INITIAL figure; "Harappa-specific
  breakdown pending").
- **The phase assignment.** Execution, after the OSF
  registration of this contract verifies public, is
  **Phase-396** (first free number after Phase-395).

## 2. Bookkeeping rule for the frozen bytes

The design sources (`spec.md`, `claims.json`,
`adjudication.md`) are digest-covered as frozen and
are not bookkeeping: any change to them after this
freeze is a design change requiring a new owner
adjudication and a new freeze. `plan.md` and
`tasks.md` are bookkeeping and are **not**
digest-covered (the Spec 029/030 rule): their
checkbox state may change at closeout without
drifting the freeze. Phase-396's records, when they
exist, are recorded in this directory, in the PRED
register (by appended dated entry only), and in the
program ledgers (root `LEDGER.md`), never by editing
the frozen files. The freeze itself is never
regenerated (Spec 026 §4.7).

## 3. Tooling pins

- AEE package **1.0.4** (Glossa venv, PATH-pinned for
  every AEE run); AEE extension v1.1.0; evaluator
  extension v1.0.0; specify CLI 1.0.10; Python 3.12.3.
- Freeze machinery: `glossa_lab.framework026`
  (`build_freeze` / `verify_freeze` /
  `check_dependency_integrity`).

## 4. What this freeze does not do

- **It does not execute anything.** The registered
  computation has never been run. OSF registration of
  this frozen contract is a precondition of any
  execution, and execution follows the verified
  approval under the owner's order of 2026-10-13.
- **It changes no existing record.** The PRED
  register (including PRED-2026-006's PARTIALLY
  CONFIRMED entry and PRED-2026-007's state), the
  global stability record, and every Spec 026–031
  record stand exactly as they stood.
- **It does not promise a computable test.** The
  frozen step-0 closures (CANNOT BE RUN AS WRITTEN;
  the UNMAPPABLE coverage statement) are valid
  closures under this freeze, not defects to be
  repaired by substitution (F032-C04, C12).

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
