# Spec 040 — AEE note (draft)

The AEE lifecycle hooks (after_specify /
after_plan / after_tasks) have **not run** on
this draft's claim register (F040-C01…C15),
deliberately: the hooks are a **freeze gate**,
not a drafting step (tasks L4). Any recovery
round at the freeze act changes claim text, so
the freeze digest is computed over the
recovered register exactly once, at freeze —
the ordering Spec 035 established and Specs
036/037 carried. At this draft the register
carries only the draft-stage self-checks
pinned by `backend/tests/test_spec040_freeze.py`
(dependency integrity; the definition
constants; the cited-record facts: the
Phase-140 and Phase-385 quantities, the spine
and covariate pins, and the Spec 025 rider).

The freeze act for this spec has a second gate
in front of the hooks (tasks L5): spec §1's
dependency gate on the executed Spec 039
record. The hooks run only when that gate is
satisfied; a hook pass over a register whose
dependency has failed would freeze a contract
that cannot execute.

At the freeze act, the hook outputs and any
recovery rounds are recorded in this directory
(`aee/`), and this note is completed by append
with their record.

---

## Freeze-act record — appended 2026-10-24

The second gate named above is satisfied at
this act: spec §1's dependency gate is judged
satisfied by the openly recorded
successor-artifact substitution of Spec 041's
artifact (`adjudication.md` §5; `freeze.md`
§1–§2). The hooks therefore ran, at the freeze
act and before any freeze digest was computed
(tasks L4, the Spec 035 ordering): `aee assess`
in the shape the repo's `run_aee.py` harness
wraps (lenient load — the register's
single-string `boundary` form; evidence
verification off; no ledger), over
`specs/040-d25-g1-chronology-controlled/claims.json`,
in the `glossa-aee153` environment
(applied-epistemic-engineering **1.5.3**).

Two recovery rounds were needed, each recorded
in the register's own `note`. The draft run
(register 0.5-draft) returned **41 failure
modes**: 22 `independence_unmodeled` (one per
evidence item — no item carried an independence
declaration), 4 `coverage_gap` irreducibility
challenges (F040-C03, C05, C06, C11), and 15
FR-2.3 draft-cap records; minimum propagated
confidence **0.695**, with eight claims below
the 0.70 threshold. Round 1 (0.5-draft →
0.6-draft) gave every evidence item an
`independent_of` declaration naming the
register's other evidence sources (separate
documents, independently inspectable) and
restated the four challenged heads as single
propositions, each draft head carried verbatim
into its claim's boundary with its remaining
clause governed there; no proposition was
dropped. The round-1 run returned **16 failure
modes**: the 15 draft-cap records and one
remaining `coverage_gap` challenge on
F040-C11; eight claims still stood at 0.695 —
the seven single-evidence claims on their
direct scores ("fewer than two independent
supporting sources") and F040-C11 by
propagation from F040-C08. Round 2 (0.6-draft →
0.7-draft) restated F040-C11's head a second
time as the single upper-bound condition spec
§6.4 states (the first restated head is carried
in its boundary), and gave each of F040-C07,
C08, C09, C10, C12, C14 and C15 a second
evidence item from a distinct record that
states the claimed proposition — the Phase-385
report, the Spec 025 design record, the D-25
design source, and the Spec 025 Phase-140
freeze record — recomputing every
`independent_of` declaration against the
enlarged source set.

Final round, over the recovered register
(**0.7-draft**), all three hooks identical in
shape: **15 failure modes, every one an FR-2.3
draft-cap record; zero correctness failure
modes; no claim below the 0.70
propagated-confidence threshold (minimum
0.8445)**. On the DD-038-10 reading — the
gate's "pass" is zero correctness failure modes
and no claim below threshold, the engine's
"iterate" word following from the FR-2.3
draft-cap records alone — **the freeze gate
passes**. Artifacts of the final round:

- `aee-after_specify-20261024T150459Z.json` +
  `evaluator-aee-after_specify-20261024T150459Z.json`
- `aee-after_plan-20261024T150502Z.json` +
  `evaluator-aee-after_plan-20261024T150502Z.json`
- `aee-after_tasks-20261024T150506Z.json` +
  `evaluator-aee-after_tasks-20261024T150506Z.json`

(UTC stamps; the freeze act is 2026-10-24
owner-local.) Intermediate recovery-round
artifacts are not retained; this note and the
register's `note` are their record. The freeze
digest (`../freeze.json`) was computed over
the recovered register (0.7-draft) exactly
once, after this gate passed.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
