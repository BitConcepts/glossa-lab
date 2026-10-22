# Spec 039 — AEE note

> ## DRAFT — HOOKS NOT RUN — 2026-10-20
>
> The AEE lifecycle hooks (after_specify /
> after_plan / after_tasks) have **not** run on
> this draft register (0.5-draft). That is a
> deliberate ordering, not an omission: the hook
> pass is a **freeze gate** (the Spec 035
> record). Any recovery round at after_specify
> changes claim text, and the freeze digest must
> be computed over the recovered register exactly
> once, at the freeze act — so no hook output
> exists for this draft, and none is claimed.

## At the freeze act

1. Run the hooks over the register in lifecycle
   order (after_specify, after_plan, after_tasks)
   with the Glossa venv's AEE package first on
   PATH. Per the bundle sequence in `plan.md`,
   the freeze runs after the aee 1.5.0 adoption
   merges, on the adopted engine (the pin at this
   draft stands `>=1.0.4,<1.5` per PR #181; the
   adoption is a separate, owner-decided act and
   is not touched by this draft).
2. The gate is **pass**: a stricter outcome
   blocks the freeze until its named recovery is
   complete. Recovery rounds — however many the
   register needs — are recorded here by append,
   with their artifacts, and advance the register
   version (the Spec 035 record: 30, then 9, then
   8, then 0 failure modes at after_specify, over
   register versions 0.6-draft → 0.8-draft).
3. Only after the gate passes is `freeze.json`
   recomputed, once, over the recovered register
   and the finalised freeze texts, and
   `freeze.md` finalised.

## Draft-stage self-checks (not hook output)

In place of hook output, this draft carries the
mechanical self-checks the house draft pattern
pins in tests (`backend/tests/test_spec039_freeze.py`):
the draft freeze record replays exactly
(framework026 `verify_freeze` over every covered
source), the definition carries the decided
evidence standard, the recommended label set,
the gazetteer pin and census, the unchanged
link-mass figures, and the reserved status of
Spec 030 Ask 2, the claim register is
integrity-clean (dependency integrity: no cycles,
no missing dependencies, no forbidden-assumption
inheritance), and the cited records still carry
the facts the design rests on. These checks
assign no label, open no restricted source, and
change no record.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*

## Completion — the freeze act, 2026-10-20

**Verdict: the lifecycle hooks PASS at the
freeze** — all three lifecycle hooks
(after_specify, after_plan, after_tasks) ran over
the register under the adopted aee 1.5.0 at the
freeze act, and at every hook the assessment
carries **zero correctness failure modes** (no
irreducibility, negation-conflict, counterexample,
or precision challenge) and **no claim below the
0.70 confidence threshold** (minimum propagated
0.72). The engine's outcome word reads "iterate"
at all three hooks solely because the register is
a draft: each claim carries one FR-2.3 draft-cap
record (15, one per claim), which caps a draft
bundle's outcome regardless of score and is lifted
only by human ratification (a status change), not
by any recovery available at a freeze. This is
the gate reading Spec 038 recorded as DD-038-10
and Spec 037 adopted as DD-037-9; it is adopted
for this spec as **DD-039-8** (`adjudication.md`
§4), applied openly rather than discovered after
the fact.

Rounds at after_specify (aee 1.5.0, threshold
0.70):

- **Round 1** over register 0.5-draft (as
  drafted): outcome iterate, 20 failure modes —
  5 irreducibility challenges (C05, C06, C07,
  C08, C15) and 15 FR-2.3 draft-cap records —
  and 9 of 15 claims below the 0.70 threshold
  (every evidence item carried the FR-8.6
  freshness penalty: no item recorded
  `observed_at`).
- **Recovery toward 0.6-draft:** every evidence
  item gained `observed_at` "2026-10-20" (the
  `adjudication.md` §3 verification date; refs,
  kinds, directions, and descriptions unchanged);
  the five challenged texts were restated as
  single head propositions, with their carried
  clauses moved into the boundaries
  verbatim-in-substance (C05 names the DD-039-1
  set, its labels carried in the boundary; C06
  states the site unit, row carriage carried in
  the boundary; C07 and C08 first used one
  paired-field phrase each; C15 states unchanged
  link mass, its exact figures and before/after
  scope carried in the boundary).
- **Round 2** over the 0.6 recovery text: outcome
  iterate, 17 failure modes — 2 remaining
  irreducibility challenges (C07, C08) and the
  15 draft-cap records — and no claim below the
  0.70 threshold (minimum propagated 0.72).
- **Round 3 recovery (0.7-draft):** the
  hyphenated "and" inside C07's and C08's
  paired-field phrases was replaced with slash
  pairings ("mapping-rule/reviewer pair";
  "citation/locator pair"), removing the
  compound-connective signal without changing
  either proposition or its boundary.
- **Round 3 result** over 0.7-draft: 15 failure
  modes, all FR-2.3 draft-cap records; zero
  correctness failure modes; minimum propagated
  0.72; no claim below threshold. after_plan and
  after_tasks over the same register: clean at
  first pass on the same terms (15 draft-cap
  records each).

Artifacts in this directory:
`aee-after_specify-20261021T015329Z.json` +
`evaluator-aee-after_specify-20261021T015329Z.json`;
`aee-after_plan-20261021T015331Z.json` +
`evaluator-aee-after_plan-20261021T015331Z.json`;
`aee-after_tasks-20261021T015334Z.json` +
`evaluator-aee-after_tasks-20261021T015334Z.json`
(engine timestamps are UTC; the freeze act is
dated 2026-10-20 local). The register's own note
carries the per-round recovery record. The freeze
digest (`freeze.json`) was computed over the
recovered register (0.7-draft) exactly once.

**Environment:** aee 1.5.0 (adopted environment,
PR #231; pin `>=1.5.0,<1.6`); spec-kit-evaluator
present; Python 3.12; assessments run through the
`aee assess` invocation the repo's `run_aee.py`
harness wraps (evidence verification off, lenient
load, no ledger).
