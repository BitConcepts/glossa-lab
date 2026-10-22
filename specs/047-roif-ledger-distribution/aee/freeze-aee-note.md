# Spec 047 — AEE note

> ## FREEZE ACT — HOOKS RUN — 2026-10-21
>
> The AEE lifecycle hooks (after_specify /
> after_plan / after_tasks) ran on this register
> at the freeze act of 2026-10-21, as the freeze
> gate the draft recorded (tasks L4). No hook
> output existed for the draft, by the deliberate
> ordering the program keeps (the Spec 035
> record): any recovery round changes claim text,
> and the freeze digest is computed over the
> recovered register exactly once, at the freeze.

## Completion — the freeze act, 2026-10-21

**Verdict: the lifecycle hooks PASS at the
freeze** — all three lifecycle hooks
(after_specify, after_plan, after_tasks) ran over
the register under aee 1.5.0 at the freeze act,
and at every hook the assessment carries **zero
correctness failure modes** (no irreducibility,
negation-conflict, counterexample, or precision
challenge) and **no claim below the 0.70
confidence threshold** (minimum propagated
0.72). The engine's outcome word reads "iterate"
at all three hooks solely because the register is
a draft: each claim carries one FR-2.3 draft-cap
record (19, one per claim), which caps a draft
bundle's outcome regardless of score and is
lifted only by human ratification (a status
change), not by any recovery available at a
freeze. This is the gate reading Spec 038
recorded as DD-038-10 and Spec 037 adopted as
DD-037-9; it is adopted for this spec as
**DD-047-16** (`adjudication.md` §7), applied
openly rather than discovered after the fact.

Before the hooks ran, the freeze's own rulings
were carried into the register: DD-047-13's
all-UNMAPPED exception into the boundaries of
F047-C13 and F047-C16, and DD-047-10's
permutation seed (20261021) into F047-C16's
boundary.

Rounds at after_specify (aee 1.5.0, threshold
0.70):

- **Round 0 (loadability).** The register as
  drafted (0.5-draft) does not load under aee
  1.5.0: its evidence items carry free-form
  `kind` labels (`program-record`,
  `design-source`, `campaign-record`,
  `verification-record`) and `source_quality`
  labels (`authoritative`, `program-record`) that
  are not engine values, and the loader refuses
  them before any assessment exists. **Recovery
  to 0.6-draft:** every evidence item was
  normalised to kind `observed` and
  source_quality `artifact` — the frozen-register
  form of Specs 036–039. Refs, source_ids,
  directions, descriptions, and `observed_at`
  values are unchanged.
- **Round 1** over register 0.6-draft: outcome
  iterate, 67 failure modes — 18 irreducibility
  challenges (every claim except F047-C07), 27
  shared-evidence independence-unmodelled
  records, 3 negation-conflict challenges
  (C06/C10, C07/C18, C10/C12), and 19 FR-2.3
  draft-cap records — and no claim below the
  0.70 threshold (minimum propagated 0.72).
- **Recovery to 0.7-draft:** the 18 challenged
  claim texts were restated as single head
  propositions, with their carried clauses moved
  into the boundaries verbatim-in-substance
  (propositions, falsifiers, and verdict rules
  unchanged; F047-C07's text was not challenged
  and stands as drafted); and every multi-item
  claim's evidence gained mutual `independent_of`
  declarations naming the claim's other evidence
  source_ids — the within-claim pairs are
  distinct records (the Phase-104 evaluation, the
  design packet, the gazetteer, Spec 027's spec,
  the campaign plan, the Roif verification), and
  the declarations state that fact.
- **Round 2** over 0.7-draft: 19 failure modes,
  all FR-2.3 draft-cap records; zero correctness
  failure modes; minimum propagated 0.72.
  after_plan and after_tasks over the same
  register: clean at first pass on the same
  terms (19 draft-cap records each).

Artifacts in this directory:
`aee-after_specify-20261021T095753Z.json` +
`evaluator-aee-after_specify-20261021T095753Z.json`;
`aee-after_plan-20261021T095802Z.json` +
`evaluator-aee-after_plan-20261021T095802Z.json`;
`aee-after_tasks-20261021T095804Z.json` +
`evaluator-aee-after_tasks-20261021T095804Z.json`
(engine timestamps are UTC; the freeze act is
dated 2026-10-21 local). The register's own note
carries the per-round recovery record. The freeze
digest (`freeze.json`) was computed over the
recovered register (0.7-draft) exactly once.

**Environment:** aee 1.5.0 (the adopted
environment; package pin `>=1.5.0,<1.6`). The
hooks ran in the `glossa-aee150` venv: the
`glossa-aee153` venv on this machine stands
empty (its `bin/` carries no interpreter), so the
adopted 1.5.x engine of record for this freeze is
1.5.0, recorded here rather than assumed.
spec-kit-evaluator present; Python 3.12;
assessments run through the `aee assess`
invocation the repo's `run_aee.py` harness wraps
(lenient load — the program's registers carry
`boundary` as a single string, which the strict
loader refuses — evidence verification off, no
ledger).

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
