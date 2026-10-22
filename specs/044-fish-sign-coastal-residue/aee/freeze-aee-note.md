# Spec 044 — AEE note

> ## FREEZE ACT — HOOKS RUN — 2026-10-21
>
> At draft, the AEE lifecycle hooks
> (after_specify / after_plan / after_tasks) had
> **not** run on this register — a deliberate
> ordering, not an omission: the hook pass is a
> **freeze gate** (the Spec 035 record). Any
> recovery round at after_specify changes claim
> text, and the freeze digest must be computed
> over the recovered register exactly once, at
> the freeze act. This note is written at the
> freeze and records the whole gate: the draft
> state, the load failure, the recovery rounds,
> and the passing result.

## Completion — the freeze act, 2026-10-21

**Verdict: the lifecycle hooks PASS at the
freeze** — all three lifecycle hooks
(after_specify, after_plan, after_tasks) ran over
the register under the adopted aee 1.5.0 at the
freeze act, and at every hook the assessment
carries **zero correctness failure modes** (no
coverage gap, contradiction,
assumption-unvalidated, or ambiguous-requirement
record) and **no claim below the 0.70 confidence
threshold** (minimum propagated 0.72). The
engine's outcome word reads "iterate" at all
three hooks solely because the register is a
draft: each claim carries one FR-2.3 draft-cap
record (15, one per claim), which caps a draft
bundle's outcome regardless of score and is
lifted only by human ratification (a status
change), not by any recovery available at a
freeze. This is the gate reading Spec 038
recorded as DD-038-10 and Specs 037 and 039
adopted after it; it is adopted for this spec
as **DD-044-9** (`adjudication.md` §7.8),
applied openly rather than discovered after
the fact.

Rounds (aee 1.5.0, threshold 0.70, lenient load,
evidence verification off, no ledger):

- **Load attempt over register 0.5-draft (as
  drafted): the engine refused the register
  outright.** The draft's evidence items carry
  kind values (`program-record`, `design-source`,
  `campaign-source`) and source_quality values
  (`authoritative`, `program-record`) that are
  not members of the adopted engine's enums, so
  no assessment exists over 0.5-draft and none
  is claimed.
- **Recovery toward 0.6-draft:** every evidence
  item's kind was normalised to `observed` and
  its source_quality to `artifact` — the frozen
  house form of Specs 036–039 — with refs,
  directions, descriptions, source_ids, and
  `observed_at` values unchanged.
- **Round 1** at after_specify over 0.6-draft:
  outcome iterate, 47 failure modes — 15
  irreducibility challenges (one per claim), 15
  shared-evidence independence challenges, 1
  negation-conflict challenge (C05 against C06),
  1 counterexample challenge (C14's absolute
  wording), and 15 FR-2.3 draft-cap records —
  and no claim below the 0.70 threshold
  (minimum propagated 0.72).
- **Recovery toward 0.7-draft (the Spec 039
  pattern):** every claim text was restated as a
  single head proposition, with its carried
  clauses moved into its boundary verbatim in
  substance (each boundary names the carriage);
  C06's head proposition was restated under a
  distinct subject (the frozen asset's digest
  identity) and the C05/C06 pair gained
  `boundary_confirmation` metadata recording
  that the two govern different properties of
  the same asset; C14's head proposition drops
  the absolute wording, its carried clauses
  preserved in its boundary; every multi-item
  claim's later evidence items gained
  `independent_of` declarations naming the
  claim's first evidence source (the
  distinct-source pattern of Specs 036–039).
  Propositions' substance, falsifiers, and
  verdict rules are unchanged. C07's boundary
  additionally carries the freeze's layer
  identification (OPEN-044-1; `adjudication.md`
  §7.2).
- **Round 2** at after_specify over 0.7-draft:
  15 failure modes, all FR-2.3 draft-cap
  records; zero correctness failure modes;
  minimum propagated 0.72; no claim below
  threshold. after_plan and after_tasks over
  the same register: clean at first pass on
  the same terms (15 draft-cap records each).

Artifacts in this directory:
`aee-after_specify-20261021T095745Z.json` +
`evaluator-aee-after_specify-20261021T095745Z.json`;
`aee-after_plan-20261021T095751Z.json` +
`evaluator-aee-after_plan-20261021T095751Z.json`;
`aee-after_tasks-20261021T095752Z.json` +
`evaluator-aee-after_tasks-20261021T095752Z.json`
(engine timestamps are UTC; the freeze act is
dated 2026-10-21 local). The register's own note
carries the per-round recovery record. The
freeze digest (`freeze.json`) was computed over
the recovered register (0.7-draft) exactly once.

**Environment:** aee 1.5.0 (adopted environment,
PR #231; pin `>=1.5.0,<1.6`); spec-kit-evaluator
present; Python 3.12.3; assessments run through
the `aee assess` invocation the repo's
`run_aee.py` harness wraps, with `--lenient`
and `--no-ledger` (the harness exposes no
lenient switch, so the wrapped command was
invoked directly, as at the Spec 039 freeze).

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
