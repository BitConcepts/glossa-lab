# Spec 039 — Plan

> ## PLAN — FOR FREEZE DECISION — 2026-10-20
>
> Written against the governing record: Spec 027
> §§5–6 (`specs/027-movement-culture-language/spec.md`),
> the Stage 0 gazetteer on `main`
> (`data/movement/gazetteer_rows.jsonl`), Spec
> 031's frozen period rule and Phase-395 outcome,
> Spec 030's adjudication (Ask 2 reserved), and
> the owner's decisions of 2026-10-20 (act
> authorised, bundled with D-25, evidence standard
> Option 1), recorded in `adjudication.md`. The
> freeze and the execution are later acts in the
> bundle sequence (§2); no task in `tasks.md` is
> itself an execution, and this draft assigns
> nothing.

**Governing documents:** `spec.md`, `claims.json`,
and `adjudication.md` in this directory;
`specs/027-movement-culture-language/spec.md`
(§§5.1, 5.2, 6.2, 6.3, 6.5) and its Stage 0 freeze
and release records;
`specs/031-stage2-q7-provenance-networks/spec.md`
(F031-C10) and `outcome.md` (the Phase-395 margins
record); `reports/phase395_results.json`;
`specs/030-q6-chronology-spine-extension/adjudication.md`
(Ask 2); `reports/phase394_results.json` (the
preserved Masudpur extraction); the D-25 design in
the PR #195 portfolio; the Glossa constitution;
governance H1, H2, H6, H13, H15/H23, H21.

**Tooling record:** specify CLI 1.0.10 (setup and
extension management only); AEE extension v1.1.0;
evaluator extension v1.0.0; AEE package from the
Glossa venv first on PATH for every AEE invocation
(pin at this draft `>=1.0.4,<1.5` per PR #181; the
owner-decided aee 1.5.0 adoption is a separate act
in the bundle sequence, §2, and is not touched by
this draft).

## 1. Sequence inside this spec

1. **Design PR** (this draft) — `spec.md`,
   `claims.json`, `adjudication.md`, `plan.md`,
   `tasks.md`, `build_freeze.py` + `freeze.json`
   (the draft digest), `outcome.md` (the
   pre-written execution append skeleton — a
   skeleton only, nothing executed), the freeze
   test (`backend/tests/test_spec039_freeze.py`),
   the AEE note under `aee/`, and the LEDGER
   entry. Claims first. **AEE hooks have not run
   on this draft** (recorded in
   `aee/freeze-aee-note.md`): the hook pass
   (after_specify / after_plan / after_tasks) is a
   freeze gate, below — a deliberate ordering, not
   an omission, since any recovery round changes
   claim text and the digest must be computed over
   the recovered register exactly once, at freeze.
2. **Freeze PR** — at the bundle step in §2: AEE
   hook pass over the register (gate: **pass**,
   with any recovery rounds recorded in `aee/`),
   `freeze.md` finalised, `freeze.json`
   recomputed over the recovered register and the
   finalised freeze texts, DD-039-1…DD-039-6
   decided in the freeze record, and the execution
   phase number fixed (DD-039-7). The freeze PR
   merges on green house gates; it executes
   nothing and assigns nothing.
3. **Execution** — on the bundle sequence reaching
   this act: graph-first build (H15/H23); input
   integrity against the gazetteer pin; evidence
   assembly under the frozen hierarchy and the
   DD-039-3 rule; mapping under the frozen table;
   contested flagging; outputs A (the assigned
   gazetteer) and B (the assignment report)
   written and hashed; the margins verification
   step (spec §8); output C (the Zenodo
   new-version deposit through the release gate);
   the outcome record, the root LEDGER entry, and
   the foundation check (H21).

## 2. The bundle sequence (owner instruction, 2026-10-20)

The owner authorised this act bundled with D-25
and directed that the program be planned and
executed "at the right time". The standing
sequence, each step gated as recorded in its own
spec:

1. Spec 036 freeze → execution (PRED-2026-011
   scoring) — in flight.
2. The aee 1.5.0 adoption (owner-decided
   2026-10-20) — lands after the Spec 036 freeze.
3. Spec 038 freeze → execution (D-31,
   PRED-2026-007 full-population scoring) — on the
   adopted engine.
4. Spec 037 execution (the CISI concordance), as
   its own order admits.
5. **This act's freeze** — its gate runs on the
   adopted engine, its adjudication cycle shared
   with the D-25 spec's (step 6).
6. **This act's execution**, then the D-25 spec's
   freeze and execution consuming Output A as a
   hash-pinned input.

The order is a plan, not a freeze condition: if
the owner re-sequences the bundle, this plan is
amended by dated note and no claim in the register
changes.

## 3. What this plan never does

- It assigns no period label at draft or at
  freeze; assignments are execution work under
  the frozen mapping table.
- It derives no label from chronology-spine
  dates, at any stage (the owner's Option 1).
- It changes no Spec 027, 030, or 031 record, no
  spine row, and no published deposit; the
  Stage 0 deposit is superseded only by a new
  version at execution.
- It admits no Masudpur determination and
  establishes no new site (DD-039-4's recommended
  default), and it decides nothing about Spec
  030 Ask 2.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
