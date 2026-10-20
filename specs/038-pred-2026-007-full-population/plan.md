# Spec 038 — Plan

> ## PLAN — FOR FREEZE DECISION — 2026-10-20
>
> Written against the governing record: the
> PRED-2026-007 registration in
> `docs/PREDICTION_REGISTER.md` (2026-04-22),
> design **D-31** in the PR #195 portfolio
> (`docs/research/experiment-designs-2026-10-13/05-predictions.md`),
> and the freeze coordinator's Stage-0
> preparation record of 2026-10-20 (three
> design-integrity flags, disposed of in
> `adjudication.md` §3). The owner's draft
> order of 2026-10-20 commissions this draft;
> the freeze and the execution (Phase-401,
> provisional) are separate owner decisions,
> and no task in `tasks.md` is itself an
> execution.

**Governing documents:** `spec.md`,
`claims.json`, and `adjudication.md` in this
directory; the PRED-2026-007 entry in
`docs/PREDICTION_REGISTER.md`;
`reports/indus_cgsa_cluster_analysis.json`
(primary function-code source);
`data/crosswalks/canonical_sign_registry.csv`
(cross-check); `outputs/analysis/sign_clusters.json`
and `reports/cluster_characterization.md`
(recorded Phase 5 output);
`reports/cgsa_validation_report.md`
(corroboration); `specs/035-pred-2026-010-scoring/`
and `specs/036-pred-2026-011-scoring/` (house
draft/freeze precedent); the Glossa
constitution; governance H1, H2, H6, H13,
H15/H23, H21.

**Tooling record:** specify CLI 1.0.10 (setup
and extension management only); the freeze
gate runs the AEE lifecycle hooks under
**aee 1.5.0** (adoption in flight — DD-038-7);
this draft runs no hooks.

## 1. Sequence

1. **Design PR** (this draft) — `spec.md`,
   `claims.json`, `adjudication.md`, `plan.md`,
   `tasks.md`, `osf-registration.md` (the
   no-preregistration record and the DD-038-6
   proposal), `build_freeze.py` + `freeze.json`
   (the draft digest), `outcome.md` (the
   pre-written execution append skeleton — a
   skeleton only, nothing executed), the freeze
   test (`backend/tests/test_spec038_freeze.py`),
   the AEE note under `aee/`, and the LEDGER
   entry. Claims first. **AEE hooks have not
   run on this draft** (recorded in
   `aee/freeze-aee-note.md`): the hook pass is
   a freeze gate, below — a deliberate ordering,
   since any recovery round changes claim text
   and the digest must be computed over the
   recovered register exactly once, at freeze.
   The population is not enumerated at any
   point in this stage.
2. **Freeze PR** — on the owner's freeze
   order: AEE hook pass over the register under
   aee 1.5.0 (gate: **pass**, with any recovery
   rounds recorded in `aee/`), `freeze.md`
   finalised, `freeze.json` recomputed over
   the recovered register and the finalised
   freeze texts, DD-038-6 decided (the
   proposal: file the frozen spec's own OSF
   contract registration), and the Phase-401
   number confirmed (DD-038-8). The freeze PR
   merges on green house gates; it executes
   nothing and enumerates nothing.
3. **Execution (Phase-401, provisional)** — on
   the owner's separate execution order:
   graph-first build (H15/H23); step 0 in the
   frozen order (sources and provenance with
   the conflict rule; enumeration with its
   completeness checks; Phase 5 output
   verification), fail-closed, the step-0
   record written and hashed before any
   scoring; then the registered scoring and
   the per-sign table; the outcome (verdict,
   census completion, partial-scope record, or
   closure) appended to the PRED register —
   together with the provenance reconciliation
   note — and recorded in this directory,
   `outcome.md`, and the root LEDGER; the
   foundation check (H21) after the claim
   consequence lands.

## 2. What this plan never does

- It executes nothing and enumerates nothing at
  draft or at freeze; the enumeration and the
  execution are Phase-401, separately ordered.
- It edits no register text and no frozen Spec
  026–037 record; every register consequence
  lands only at execution, as dated appends
  (`spec.md` §7).
- It pre-writes no outcome for any branch
  (DD-038-1): no expected population, no
  expected share, no expected verdict appears
  in this package.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
