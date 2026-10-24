# Spec 050 — AEE note

> ## FREEZE ACT — HOOKS RUN — 2026-10-21
>
> The AEE lifecycle hooks (after_specify /
> after_plan / after_tasks) ran over this
> register at the freeze act of 2026-10-21,
> under the gate reading DD-050-9
> (`adjudication.md` §7, the DD-038-10
> pattern). The recovery rounds below are
> the freeze record; the final artifacts are
> in this directory.

## The gate reading (DD-050-9)

The hooks PASS at the freeze when every hook
carries **zero correctness failure modes**
(no irreducibility, negation-conflict,
counterexample, or precision challenge, and
no shared-evidence independence record) and
**no claim below the 0.70 confidence
threshold**, with the engine outcome word
reading "iterate" solely because the
register is a draft: each claim carries one
FR-2.3 draft-cap record (15, one per claim),
which caps a draft bundle's outcome
regardless of score and is lifted only by
human ratification (a status change), not
by any recovery available at a freeze.

## Rounds (aee 1.5.0, threshold 0.70, lenient load, no ledger)

Environment: aee **1.5.0** from the venv
`~/workspace/venvs/glossa-aee150` (package
pinned >=1.5.0,<1.6). Assessments ran
through the `aee assess` invocation the
repo's `run_aee.py` harness wraps (evidence
verification off, lenient load, no ledger);
the direct `run_aee.py` entry point does not
pass the lenient flag the historical
register shape requires, so the wrapped
invocation was used, as in the Spec 045
freeze record.

Before the rounds, the freeze decisions
were applied to the register as a
freeze-stage edit recorded in
`adjudication.md` §7: the pin-timing ruling
DD-050-11 restated claim F050-C06 (the
freeze record quotes Spec 045's freeze
digest as contract anchor and fixes Spec
045's `asset-a-freeze.json` as the pin
source; gate 0.1 asserts the digest at
execution step 0).

- **Pre-round load failure** over register
  0.5-draft (as drafted, with the DD-050-11
  edit applied): the engine refused the
  register outright — evidence kinds
  `design-source` / `program-record` and
  source qualities `authoritative` /
  `program-record` (the Spec 042 draft
  conventions this register was written in)
  are not engine values in aee 1.5.0.
- **Test load** with the kind remap alone
  (kinds to `observed`, qualities to
  `artifact`): outcome iterate, 54 failure
  modes — 25 shared-evidence independence
  records, 14 irreducibility challenges, and
  15 draft-cap records — and no claim below
  the 0.70 threshold (minimum propagated
  0.72; the draft already carried
  `observed_at` on every evidence item,
  DD-050-8, so no freshness penalty fired).
- **Recovery to 0.6-draft:** evidence kinds
  remapped to `observed` and source
  qualities to `artifact` (refs, directions,
  descriptions, and `observed_at` values
  unchanged), and every evidence item in a
  multi-item claim gained an
  `independent_of` declaration naming the
  other sources in its claim (the Spec 039
  pattern). Round 1 over 0.6-draft at
  after_specify: 29 failure modes — all 25
  independence records cleared; 14
  irreducibility and 15 draft-cap remained;
  minimum propagated 0.72.
- **Recovery to 0.7-draft:** every
  challenged claim text was restated as a
  single head proposition, with its carried
  clauses moved into the boundary
  verbatim-in-substance (propositions,
  falsifiers, and verdict rules unchanged
  in substance). Round over 0.7-draft: 17
  failure modes — 15 draft-cap and 2
  remaining irreducibility challenges
  (F050-C04, whose head still carried the
  connective "or", and F050-C07).
- **Recovery to 0.8-draft:** the C04 and
  C07 heads were restated connective-free
  (single-clause forms, the Spec 039
  round-3 pattern; carried clauses in the
  boundaries unchanged in substance). One
  negation-conflict pair then surfaced
  (C01/C04 — the detector binds on a shared
  leading subject plus a negation in one
  head): C01 and C04 gained
  `boundary_confirmation` records stating
  why the paired claims govern different
  objects (outcome scope, and outcome
  wording on a stated condition) and do not
  negate each other, and C04's head was
  restated under its own subject; a C04/C06
  pair that surfaced next (with its own
  `boundary_confirmation` records added)
  cleared when C04's head was restated
  under the subject "Meeting the falsifier
  condition".
- **Final round** over 0.8-draft:
  after_specify, after_plan, and after_tasks
  each returned exactly 15 failure modes,
  all FR-2.3 draft-cap records; zero
  correctness failure modes; minimum
  propagated 0.72; no claim below threshold.
  The engine outcome word reads "iterate"
  at all three hooks solely from the
  draft-cap records.

Artifacts in this directory:
`aee-after_specify-20261021T110847Z.json` +
`evaluator-aee-after_specify-20261021T110847Z.json`;
`aee-after_plan-20261021T110850Z.json` +
`evaluator-aee-after_plan-20261021T110850Z.json`;
`aee-after_tasks-20261021T110852Z.json` +
`evaluator-aee-after_tasks-20261021T110852Z.json`
(engine timestamps are UTC; the freeze act
is dated 2026-10-21 local). The register's
own note carries the same recovery record
in summary. The freeze digest (`freeze.json`)
was computed over the recovered register
(0.8-draft) exactly once, after this note
and the other covered sources were final.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
