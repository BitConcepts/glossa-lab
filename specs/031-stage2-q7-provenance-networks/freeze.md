# Spec 031 — Freeze Record (Spec 027 Stage 2 / Q7: Provenanced-Material Networks)

> ## FROZEN at the Spec 031 freeze merge (2026-10-13)
>
> Basis: the Stage 2 / Q7 adjudication of 2026-10-12
> (`specs/027-movement-culture-language/
> stage2-q7-adjudication.md` — packet asks adopted as
> a block under the owner's "Freeze it", confirmed
> "correct, do it": **1B, 2B, 3A, 4A, 5A, 6A**) and
> the owner's order of 2026-10-13 commissioning this
> design and its freeze. The governed claim register
> enters this freeze as recovered at the design AEE
> pass (`aee/recovery-specify.md`) — the freeze
> digest below covers the recovered register, never
> the pre-recovery one. The machine freeze record is
> `freeze.json` (framework026 digest, built by
> `build_freeze.py`).

## 1. What is frozen

- **The design.** `spec.md`: the bounded Q7 test of
  Spec 027 §8.1 — two-tier provenance links (Law
  2011 instrumental determinations primary; Chapter
  4 reference-based assignments a separately labelled
  sensitivity, never pooled); Meluhha contributing no
  site-pair links; ceramic and bead/craft response
  arms each on its own eligible site set, never
  pooled; period eligibility from Stage 0 gazetteer
  labels only; the MRM/MRQAP partial-R² estimand with
  practical margin **0.02**, 9,999 permutations,
  9,999 bootstrap replicates, seed `20261013`,
  R = 199 discriminating controls per arm, and the
  site jackknife; verdict rules on the Spec 027 §7.6
  pattern, with NOT-YET-TESTABLE as a margins-step
  registration status.
- **The support rules, fixed from the D8 margins**
  (design decisions DD-1…DD-8, spec §10): site
  link-eligible at ≥ 3 primary-tier determinations;
  pair linked on ≥ 1 shared named source area;
  ceramic site floor 20 classified items; bead site
  floor 10 classified beads; arm viability ≥ 8
  eligible sites and ≥ 10 linked pairs.
- **The declared estimability limits.** The ceramic
  arm is conditionally estimable (DD-7): it closes
  NOT ESTIMABLE at the execution margins step if
  sources at audited postures cannot evidence ≥ 8
  eligible ceramic sites, and no ceramic response is
  computed in that case. Sub-period-resolution
  variants, a visual-tier primary test, and
  dose-response as a verdict-bearing test are
  declared untestable / sensitivity-only in advance.
- **The governed claim register.** `claims.json`,
  register_version `0.3-draft`: 12 claims
  (F031-C01…C12), recovered at the design AEE pass —
  the AEE hook pass over this register returns
  **pass** at after_specify, after_plan, and
  after_tasks (12 claims, 0 failure modes, 0 below
  the 0.70 threshold; `aee/` artifacts).
- **The margins the design rests on**, pinned by the
  freeze tests from their records: the D8 audit's
  Law margins (> 2,100 Harappa determinations, ~120
  at all other sites combined, ≈ 95% single-site
  concentration; 76 Meluhha citations naming a
  region, never a site) and the Stage 0 gazetteer
  (36 source-asserted rows over 30 program sites; 21
  `verified_open` / 15 `open_access_read_only`).
- **The phase assignment.** Execution, when separately
  ordered, is **Phase-395** (first free number after
  Phase-394).

## 2. Bookkeeping rule for the frozen bytes

The design sources (`spec.md`, `claims.json`,
`adjudication.md`) are digest-covered as frozen and
are not bookkeeping: any change to them after this
freeze is a design change requiring a new owner
adjudication and a new freeze. `plan.md` and
`tasks.md` are bookkeeping and are **not**
digest-covered (the Spec 029/030 rule): their
checkbox state may change at closeout without
drifting the freeze. Phase-395's records, when they
exist, are recorded in this directory and in the
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

- **It does not execute anything.** Adopted 6A makes
  OSF registration of this frozen contract a
  precondition of any execution, and execution
  itself requires a separate owner order. No link
  was digitised, no similarity computed, and no
  verdict exists under this freeze.
- **It changes no Spec 027, 028, 029, or 030
  record.** Q7's question, gate, and MUST-NOT list
  remain Spec 027's; Q6's state is untouched (Ask 4A
  independence).
- **It does not promise an estimable test.** The
  frozen consequences of sparse margins —
  NOT-YET-TESTABLE per arm, NOT ESTIMABLE for the
  ceramic arm — are valid closures under this
  freeze, not defects to be repaired by re-basing
  (F031-C07, C08).

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
