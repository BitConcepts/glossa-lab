# Spec 035 — Plan

> ## PLAN — FOR FREEZE DECISION — 2026-10-20
>
> Written against the governing record: the
> PRED-2026-010 registration in
> `docs/PREDICTION_REGISTER.md` (2026-10-13), its
> derivation record
> (`reports/pred010_derivation_record.json`), and
> the Spec 032 / Phase-396 record set that
> produced the successor. The owner's draft order
> of 2026-10-20 commissions this draft; the freeze
> and the execution (Phase-399) are separate owner
> decisions, and no task in `tasks.md` is itself an
> execution.

**Governing documents:** `spec.md`, `claims.json`,
and `adjudication.md` in this directory; the
PRED-2026-010 entry and the 2026-10-13 §6 note in
`docs/PREDICTION_REGISTER.md`;
`reports/pred010_derivation_record.json`;
`backend/scripts/pred010_register_derivation.py`;
`backend/scripts/phase396_pred006_step0.py` (the
frozen build carrying the classification logic and
the crosswalk reading verbatim);
`specs/032-pred-2026-006-harappa-breakdown/`
(spec, freeze, outcome); Spec 033/034 freeze
records (house freeze precedent); the Glossa
constitution; governance H1, H2, H6, H13,
H15/H23, H21.

**Tooling record:** specify CLI 1.0.10 (setup and
extension management only); AEE extension v1.1.0;
evaluator extension v1.0.0; AEE package from the
Glossa venv first on PATH for every AEE invocation
(pinned `>=1.0.4,<1.5` per PR #181 — the 1.5.0
drift is a recorded, still-open owner decision
and is not touched by this draft).

## 1. Sequence

1. **Design PR** (this draft) — `spec.md`,
   `claims.json`, `adjudication.md`, `plan.md`,
   `tasks.md`, `osf-registration.md` (the
   verification record for the prediction's
   existing preregistration),
   `build_freeze.py` + `freeze.json` (the draft
   digest), the freeze test
   (`backend/tests/test_spec035_freeze.py`), the
   AEE note under `aee/`, and the LEDGER entry.
   Claims first. **AEE hooks have not run on this
   draft** (recorded in `aee/freeze-aee-note.md`):
   the hook pass (after_specify / after_plan /
   after_tasks) is a freeze gate, below — a
   deliberate ordering, not an omission, since
   any recovery round changes claim text and the
   digest must be computed over the recovered
   register exactly once, at freeze.
2. **Freeze PR** — on the owner's freeze order:
   AEE hook pass over the register (gate: **pass**
   at all three hooks; an outcome stricter than
   `warn` blocks until the recovery it names is
   complete and recorded — Spec 026 rule; Spec
   030/033/034 recovery patterns), `freeze.md`
   finalised, `freeze.json` recomputed if any
   covered text changed, freeze tests green.
   House gates: foundation check 0 failures, full
   backend suite green, branding sweep, CI
   verified from run conclusions. The freeze also
   decides DD-035-2 (if not already decided) and
   DD-035-4 (a spec-level OSF filing, the Spec
   032–034 pattern).
3. **Registration** — the prediction's
   preregistration (wjebq) already stands verified
   (`osf-registration.md`). If the freeze files a
   spec-level registration, its record PR is left
   open with the pending state and completed by
   append once the approval verifies (the Spec
   032 pattern).
4. **Execution** — not in this plan's performing
   scope. Phase-399's shape is frozen in spec §10
   for the execution that follows the owner's
   separate execution order; step 0 (§3 of the
   spec) re-verifies everything this draft
   verified, in the frozen order, before any
   Harappa content is touched.

## 2. Numbers discipline

Every number in the contract is the register's
or a cited record's, and each was verified
against its record at draft time
(`adjudication.md` §2): the four SHA-256 pins
(pool `b19cfe95…`, manifest `ab3b4c8a…`, crosswalk
`e44b8b55…`, withheld `c02e3d7b…` — the three file
pins recomputed from the bytes on `main` at
draft); the pool census (179 rows, all
Mohenjo-daro, 0 Yajnadevam) and class census (28
classifiable; INITIAL 3 / MEDIAL 19 / MIXED 3 /
TERMINAL 3) from the derivation record; the
withheld census (5,679 / 77 sites / 2,717
Harappa) from the Spec 032 freeze for the
byte-identical file; the disclosure counts (970
Harappa inscriptions; 1,013 occurrences; 11 of 12
signs) from the Spec 032 outcome; the neighboring
global figure (72.7%) named in spec
§8 as a different quantity, not evidence; the
crosswalk observation (P217 → Y0520; P324 →
Y0740; P000 best-match absent) read from the
pinned crosswalk at draft; the Spec 032 freeze
digest `34cd6230471c746878ab80110c4a07c3f3daeecef6c05bf222521b39054490ab`;
the OSF values (accepted, public, DOI
10.17605/OSF.IO/WJEBQ, date_registered
2026-10-13T12:45:55Z) from the API read-back. The
freeze tests pin the derivation record, the
register entry, and the crosswalk observation so
a later edit to a cited record is visible. This
draft opens no withheld content, counts no
Harappa occurrence, and computes no start rate.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
