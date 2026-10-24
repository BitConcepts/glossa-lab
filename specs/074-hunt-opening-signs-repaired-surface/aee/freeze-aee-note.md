# Spec 074 — AEE lifecycle hooks at the freeze (tasks L4) — 2026-10-24

The AEE lifecycle hooks ran at the freeze act, before any
freeze digest was computed (the deliberate ordering of
tasks L4, per DD-038-10): `aee assess` (lenient load —
the strict loader refuses the register's single-string
`boundary` form and even the lenient loader rejects the
as-drafted evidence kinds; evidence verification off; no
ledger) over
`specs/074-hunt-opening-signs-repaired-surface/claims.json`,
in the `glossa-aee153` environment
(applied-epistemic-engineering **1.5.3**).

Two recovery rounds were needed, each recorded in the
register's own `note`. Round 1 (register 0.5-draft →
0.6-draft) was loadability only: every evidence item's
`kind` restated `program-record` / `design-source` /
`record` → `observed` and its `source_quality` restated
`authoritative` / `program-record` → `artifact` (the
Spec 059/063/069/070/072 recovery form); no claim text
changed. Round 1's after_specify hook over 0.6-draft
returned 40 failure modes: 27 independence challenges
(one per evidence item but one, category
`independence_unmodeled`), 13 FR-2.3 draft-cap records,
and no irreducibility, negation-conflict, or
counterexample challenges, with no claim below the 0.70
threshold (minimum propagated 0.795). The draft heads
had been written as single propositions in the
recovered form, so the irreducibility restatement the
earlier freezes needed was unnecessary here. Round 2
(0.6-draft → 0.7-draft) gave each evidence item an
`independent_of` declaration naming the register's
other evidence sources within its claim (separate
documents, independently inspectable), with an empty
declaration on the two single-evidence claims, as in
Spec 070's frozen register; no proposition changed.

Final round, over the recovered register (**0.7-draft**),
all three hooks identical in shape: **13 failure modes,
every one an FR-2.3 draft-cap record; zero correctness
failure modes; no claim below the 0.70
propagated-confidence threshold (minimum 0.795)**. On
the DD-038-10 reading — the gate's "pass" is zero
correctness failure modes and no claim below threshold,
the engine's "iterate" word following from the FR-2.3
draft-cap records alone — **the freeze gate passes**.
This is the same end state as the programme's recent
freezes (Spec 052 at 0.8-draft, Spec 054 at 0.8-draft,
Spec 040 at 0.7-draft). One difference of record, stated
so the artifact sets are not compared naively: Spec
070's own freeze artifacts record zero failure modes
under methodology version 1.0, whose loader iterated
the register's string boundaries into character lists;
the current engine (methodology 2.0, lenient load) is
the standard this freeze is measured against, and
under it the draft-cap records are the standing pass
shape for a register whose claims stand at draft stage.

Artifacts of the final round:

- `aee-after_specify-20261024T232206Z.json` +
  `evaluator-aee-after_specify-20261024T232206Z.json`
- `aee-after_plan-20261024T232209Z.json` +
  `evaluator-aee-after_plan-20261024T232209Z.json`
- `aee-after_tasks-20261024T232212Z.json` +
  `evaluator-aee-after_tasks-20261024T232212Z.json`

(UTC stamps; the freeze act is 2026-10-24 owner-local.)
Intermediate recovery-round artifacts are not retained;
this note and the register's `note` are their record.
The freeze digest (`../freeze.json`) was computed over
the recovered register (0.7-draft) exactly once, after
this gate passed.

---

*AI disclosure: hooks run by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
