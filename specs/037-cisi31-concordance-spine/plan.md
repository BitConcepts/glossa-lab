# Spec 037 — Plan

> ## PLAN — FROZEN 2026-10-20
>
> Written against the governing record: the CISI
> 3.1 intake report (2026-10-20, restricted
> store), the Phase-130 gate record (restricted
> store PROVENANCE entry 22; in-repo pack
> `specs/021-phase130-intake-pack/`), the Spec 031
> outcome record (the Q7 fence), and the Spec 034
> freeze record (join-key discipline). The owner's
> draft order of 2026-10-20 commissioned the
> draft; the freeze and the execution (Phase-402)
> were ordered by the owner's standing pipeline
> authorisation of 2026-10-20 (freeze order 038,
> then 037, then 039, then 040), and no task in
> `tasks.md` is itself a data act beyond the
> frozen contract.

**Governing documents:** `spec.md`, `claims.json`,
and `adjudication.md` in this directory;
`specs/021-phase130-intake-pack/` (the Phase-130
gate pack); `specs/031-stage2-q7-provenance-networks/outcome.md`
(the Q7 record the annex must not move);
`specs/034-matched-object-attribution/` (the
join-key precedent: object ids only, Holdat
`cisi_number` prohibited); the CISI 3.1 intake
report and the PROVENANCE record (restricted
store, research notes — the census and gate of
record); `data/normalized/corpus_master.csv`
(SHA-256 `b19cfe95…`); the Glossa constitution;
governance H1, H2, H6, H13, H15/H23, H21.

**Tooling record:** specify CLI 1.0.10 (setup and
extension management only); AEE extension v1.1.0;
evaluator extension v1.0.0; AEE package from the
Glossa venv first on PATH for every AEE invocation.
At draft the package pin was `>=1.0.4,<1.5` (PR
#181); the adopted environment is aee 1.5.0 (PR
#231, pin `>=1.5.0,<1.6`), and the freeze gate ran
under it.

## 1. Sequence

1. **Design PR** (this draft) — `spec.md`,
   `claims.json`, `adjudication.md`, `plan.md`,
   `tasks.md`, `build_freeze.py` + `freeze.json`
   (the draft digest), `outcome.md` (the
   pre-written execution append skeleton — a
   skeleton only, nothing executed), the freeze
   test (`backend/tests/test_spec037_freeze.py`),
   the AEE note under `aee/`, and the LEDGER
   entry. Claims first. **AEE hooks have not run
   on this draft** (recorded in
   `aee/freeze-aee-note.md`): the hook pass
   (after_specify / after_plan / after_tasks) is
   a freeze gate, below — a deliberate ordering,
   not an omission, since any recovery round
   changes claim text and the digest must be
   computed over the recovered register exactly
   once, at freeze. No portion data is read,
   joined, or extracted by any part of this
   draft, and nothing portion-derived is in it:
   the draft cites only aggregates already in
   the intake record.
2. **Freeze PR** — executed 2026-10-20 under the
   owner's standing pipeline authorisation: AEE
   hook pass over the register under aee 1.5.0
   (gate passed under the DD-037-9 reading;
   three recovery rounds at after_specify,
   recorded in `aee/`), `freeze.md` finalised,
   `freeze.json` recomputed over the recovered
   register (0.7-draft) and the finalised freeze
   texts, and the DD-037 proposals decided
   (DD-037-4 confirmed; DD-037-5 stratum 60;
   DD-037-6 Workstream B inside Phase-402;
   DD-037-7 OSF registration filed; DD-037-8
   phase allocation Phase-402). The freeze PR
   merges on green house gates; it executes
   nothing and touches no portion data.
3. **Execution (Phase-402)** — under the same
   standing authorisation, after the freeze
   merges: graph-first build
   (H15/H23); step 0 in the frozen order (gate
   record; portion PDF hash; local table parse
   and census; corpus_master pin; repo
   cleanliness), fail-closed; the pilot (all 693
   candidates under the frozen ladder; the
   hand-check stratum); the spine build unless
   the halt rule fires; the annex per the
   freeze's DD-037-6 decision; the outcome
   recorded as aggregates in this directory's
   `outcome.md` and the root LEDGER, with the
   row-level products written only in the
   restricted local store. No PRED-register
   entry is created or changed; no anchor
   changes; nothing portion-derived enters the
   repo at any step (repo cleanliness re-checked
   before the outcome commit).

## 2. What this plan never does

- It executes nothing at draft or at freeze; the
  execution is Phase-402, ordered by the owner's
  standing pipeline authorisation of 2026-10-20.
- It reads no portion row content for any design
  purpose; the design rests on the intake's
  aggregates, the gate record, and byte-level
  integrity checks.
- It changes no PRED-register text, no anchor,
  no Spec 031 record, and no frozen Spec
  026–036 record; the study's consequences land
  only at execution, as the outcome record and
  the local products.
- It publishes nothing at row level, ever: the
  spine, the annex working files, and the build
  record live in the restricted local store;
  the repo receives aggregate statistics only.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
