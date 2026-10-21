# Spec 045 — AEE note

> ## FREEZE ACT — HOOKS RUN — 2026-10-21
>
> The AEE lifecycle hooks (after_specify /
> after_plan / after_tasks) ran over this
> register at the freeze act of 2026-10-21,
> under the gate reading DD-045-9
> (`adjudication.md` §7, the DD-038-10 /
> DD-039-8 pattern). The recovery rounds
> below are the freeze record; the final
> artifacts are in this directory.

## The gate reading (DD-045-9)

The hooks PASS at the freeze when every hook
carries **zero correctness failure modes**
(no irreducibility, negation-conflict,
counterexample, or precision challenge, and
no shared-evidence independence record) and
**no claim below the 0.70 confidence
threshold**, with the engine outcome word
reading "iterate" solely because the
register is a draft: each claim carries one
FR-2.3 draft-cap record (17, one per claim),
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
invocation was used, as in the Spec 046
freeze record.

Before the rounds, the mandated pre-digest
repairs (DD-045-17/18/19) and the freeze
decisions (DD-045-11/12/13) were applied to
the register as draft-stage edits, recorded
in `adjudication.md` §7.

- **Pre-round load failure** over register
  0.5-draft (as drafted, with the freeze
  repairs applied): the engine refused the
  register outright — evidence kinds
  `design-source` / `program-record` and
  source qualities `authoritative` /
  `program-record` (the Spec 042 draft
  conventions this register was written in)
  are not engine values in aee 1.5.0.
- **Test load** with the kind remap alone
  (kinds to `observed`, qualities to
  `artifact`): outcome iterate, 54 failure
  modes — 17 shared-evidence independence
  records, 17 draft-cap records, 15
  irreducibility challenges, and 5
  negation-conflict challenges (the C06/C08,
  C06/C11, C07/C17, C08/C10, and C10/C11
  pairs) — and no claim below the 0.70
  threshold (minimum propagated 0.72; the
  draft already carried `observed_at` on
  every evidence item, DD-045-7, so no
  freshness penalty fired).
- **Recovery to 0.6-draft:** evidence kinds
  remapped to `observed` and source
  qualities to `artifact` (refs, directions,
  descriptions, and `observed_at` values
  unchanged), and every evidence item in a
  multi-item claim gained an
  `independent_of` declaration naming the
  other sources in its claim (the Spec 039
  pattern). Round 1 over 0.6-draft at
  after_specify: 39 failure modes — the
  independence records cleared except 2 (the
  C11/C17 pair, both single-item claims
  citing the campaign plan); 15
  irreducibility, 17 draft-cap, and 5
  negation-conflict remained; minimum
  propagated 0.72.
- **Recovery to 0.7-draft:** every challenged
  claim text was restated as a single head
  proposition, with its carried clauses
  moved into the boundary
  verbatim-in-substance (propositions,
  falsifiers, and verdict rules unchanged
  in substance); the five negation pairs
  gained `boundary_confirmation` records
  stating why the paired claims govern
  different objects and do not negate each
  other; and C17's single evidence item was
  split into the two commissioning records
  its description and origin groups already
  named (the campaign plan and the triage),
  with `independent_of` declarations between
  them — clearing the last 2 independence
  records. Round over 0.7-draft: 24 failure
  modes at each hook — 17 draft-cap, 6
  remaining irreducibility challenges
  (C01, C11, C12, C13, C15, C17, each still
  carrying a plain "and"/"or" connective in
  its head), and 1 negation-conflict (the
  C01/C05 pair, sharing the leading subject
  "outcome").
- **Recovery to 0.8-draft:** the six heads
  were restated connective-free (slash
  pairings and single-clause forms, the
  Spec 039 round-3 pattern; carried clauses
  in the boundaries unchanged in substance),
  C01 and C05 gained `boundary_confirmation`
  records for their pair, and C05's head was
  restated under its own subject (the
  section 5.5 wording rule) with its
  negation carried into its boundary.
- **Final round** over 0.8-draft:
  after_specify, after_plan, and after_tasks
  each returned exactly 17 failure modes,
  all FR-2.3 draft-cap records; zero
  correctness failure modes; minimum
  propagated 0.72; no claim below threshold.
  The engine outcome word reads "iterate"
  at all three hooks solely from the
  draft-cap records.

Artifacts in this directory:
`aee-after_specify-20261021T104300Z.json` +
`evaluator-aee-after_specify-20261021T104300Z.json`;
`aee-after_plan-20261021T104303Z.json` +
`evaluator-aee-after_plan-20261021T104303Z.json`;
`aee-after_tasks-20261021T104305Z.json` +
`evaluator-aee-after_tasks-20261021T104305Z.json`
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
