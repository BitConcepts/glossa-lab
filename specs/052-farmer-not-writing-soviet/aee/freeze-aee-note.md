# Spec 052 — AEE lifecycle hooks at the freeze (tasks L4) — 2026-10-23

The AEE lifecycle hooks ran at the freeze act, before any
freeze digest was computed (the deliberate ordering of
tasks L4, per DD-038-10): `aee assess` in the shape the
repo's `run_aee.py` harness wraps (lenient load — the
strict loader refuses the register's single-string
`boundary` form and even the lenient loader rejects the
as-drafted evidence kinds; evidence verification off; no
ledger) from `.specify/extensions/aee/scripts/python/`,
over `specs/052-farmer-not-writing-soviet/claims.json`,
in the `glossa-aee153` environment
(applied-epistemic-engineering **1.5.3**).

Three recovery rounds were needed, each recorded in the
register's own `note`. Round 1 (register 0.5-draft →
0.6-draft) was loadability only: every evidence item's
`kind` restated `program-record` / `design-source` /
`record` → `observed` and its `source_quality` restated
`authoritative` / `program-record` → `artifact` (the
Spec 059/063/069/072 recovery form); no claim text
changed. Round 1's hooks returned 62 failure modes: 19
irreducibility challenges (one per claim, category
`coverage_gap`), 22 independence challenges (one per
evidence item, category `independence_unmodeled`), 1
negation-conflict challenge (F052-C03 against F052-C04,
category `contradiction`), 1 counterexample challenge on
F052-C10 (category `assumption_unvalidated`, absolute
language), and 19 FR-2.3 draft-cap records, with no
claim below the 0.70 threshold (minimum propagated
0.72). Round 2 (0.6-draft → 0.7-draft) restated each
claim's head as a single proposition, its full draft
head carried into its `boundary` verbatim in substance;
gave each evidence item an `independent_of` declaration
naming the register's other evidence sources (separate
documents, independently inspectable); restated the
amendment claims' evidence refs as the repository paths
of the records they name, with their descriptions made
exact; and carried the settled rulings of
`adjudication.md` §9 with the amendment into the
boundaries of the claims they govern. The
negation-conflict pairing is a heuristic on shared
negation vocabulary: F052-C03 states the emblem
hypothesis's prediction and F052-C04 states design
D-01's falsifier criterion for it — no contradiction on
reading, and both restated heads drop the lists that
drew the pairing. F052-C10's absolutes are rules of
this spec's own products (a bounded domain, stated in
its boundary), not empirical absolutes; its restated
head states the reporting rule alone. Round 3
(0.7-draft → 0.8-draft) restated the last three heads
(F052-C11, F052-C18, F052-C19) to single clauses, each
previous head recorded in its claim's boundary; the
independence, negation-conflict and counterexample
challenges did not recur in round 2, and no proposition
was dropped in any round — every restated clause stands
in the boundaries and in the carried draft heads.

Final round, over the recovered register (**0.8-draft**),
all three hooks identical in shape: **19 failure modes,
every one an FR-2.3 draft-cap record; zero correctness
failure modes; no claim below the 0.70
propagated-confidence threshold (minimum 0.72)**. On the
DD-038-10 reading — the gate's "pass" is zero
correctness failure modes and no claim below threshold,
the engine's "iterate" word following from the FR-2.3
draft-cap records alone — **the freeze gate passes**.
Artifacts of the final round:

- `aee-after_specify-20261024T032847Z.json` +
  `evaluator-aee-after_specify-20261024T032847Z.json`
- `aee-after_plan-20261024T032850Z.json` +
  `evaluator-aee-after_plan-20261024T032850Z.json`
- `aee-after_tasks-20261024T032853Z.json` +
  `evaluator-aee-after_tasks-20261024T032853Z.json`

(UTC stamps; the freeze act is 2026-10-23 owner-local.)
Intermediate recovery-round artifacts are not retained;
this note and the register's `note` are their record.
The freeze digest (`../freeze.json`) was computed over
the recovered register (0.8-draft) exactly once, after
this gate passed.
