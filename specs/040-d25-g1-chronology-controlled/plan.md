# Spec 040 — Plan

> ## PLAN — FOR FREEZE DECISION — 2026-10-20
>
> Written against the governing record: design
> D-25 (PR #195 portfolio), Spec 025 with its
> Phase-139/140 freeze records, the Phase-385
> margin completion (Spec 026), the Spec 030
> extended spine, and Spec 027 §6.2. The
> owner's bundle and evidence-standard
> decisions of 2026-10-20 are recorded in
> `adjudication.md`. The freeze of this
> contract is barred until Spec 039 has
> executed (spec §1); the execution is a
> separate later order still. No task in
> `tasks.md` is itself a data act.

**Governing documents:** `spec.md`,
`claims.json`, and `adjudication.md` in this
directory; design D-25 in
`docs/research/experiment-designs-2026-10-13/04-study-headlines.md`
(PR #195); `specs/025-stage2-controlled-followup/`
(spec and freeze records);
`reports/phase140_results.json`;
`reports/phase385_results.json`;
`specs/030-q6-chronology-spine-extension/outcome.md`
(the 205-row spine and its limits);
`specs/027-movement-culture-language/spec.md`
§6.2 (the gazetteer act's basis); the Spec 039
record, once merged (the dependency of spec
§1); the Glossa constitution; governance H1,
H2, H6, H13, H15/H23, H16, H21.

**Tooling record:** specify CLI 1.0.10 (setup
and extension management only); AEE extension
v1.1.0; evaluator extension v1.0.0; AEE package
from the Glossa venv first on PATH for every
AEE invocation (the pin in force at the freeze
act governs — the aee 1.5.0 adoption is a
separate in-flight owner decision and is not
touched by this draft).

## 1. Sequence

1. **Design PR** (this draft) — `spec.md`,
   `claims.json`, `adjudication.md`, `plan.md`,
   `tasks.md`, `build_freeze.py` + `freeze.json`
   (the draft digest), `outcome.md` (the
   pre-written skeleton — a skeleton only,
   nothing executed), the freeze test
   (`backend/tests/test_spec040_freeze.py`),
   the AEE note under `aee/`, and the LEDGER
   entry. Claims first. **AEE hooks have not
   run on this draft** (recorded in
   `aee/freeze-aee-note.md`): the hook pass is
   a freeze gate, below. No label is joined,
   no margin computed, no quantity calculated
   by any part of this draft.
2. **Dependency wait** — Spec 039 executes
   under its own freeze and execution orders.
   Spec 040 does not draft its way around the
   wait: if Spec 039's product cannot support
   spec §4's interface, the recorded state is
   NOT-YET-TESTABLE at the dependency gate and
   this plan stops there.
3. **Freeze PR** — on the owner's freeze
   order, with §1's gate verified against the
   merged Spec 039 record: AEE hook pass over
   the register (gate: **pass**, recovery
   rounds recorded in `aee/`), `freeze.md`
   finalised with the Spec 039 artifact's
   path, version, and SHA-256 named in,
   `freeze.json` recomputed over the recovered
   register and finalised texts, the execution
   phase number allocated, and the DD-040
   proposals decided (DD-040-1, DD-040-5,
   DD-040-6, DD-040-9). The freeze PR merges on
   green house gates; it executes nothing.
4. **Execution** — on the owner's separate
   execution order, under the phase number the
   freeze allocated: graph-first build
   (H15/H23); dependency re-verification;
   margins gate (spec §5, margins only);
   comparability regression (spec §7, exact or
   INVALID); primary (§6) and sensitivities
   (§8); outcome appended in this directory
   and the root LEDGER, anchors asserted
   byte-identical, foundation check reported
   as measured.

## 2. What this plan never does

- It never places an inscription in a period
  from its site's label, its site's dates, or
  analyst judgement (spec §4.3).
- It never recomputes, extends, or re-grades
  the chronology spine, and never reopens
  Spec 030's Q6 closure or its reserved Ask 2.
- It never edits a frozen record: every
  consequence for G1 lands by dated append
  (spec §10, F040-C15).
- It never lets a sensitivity — contested,
  LOSO, or drop-Harappa — move the primary
  outcome.
- It touches no PRED-2026 entry and no anchor.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
