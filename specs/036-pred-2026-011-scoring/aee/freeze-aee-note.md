# AEE at the Spec 036 freeze

The register was assessed at the freeze act
(`aee/recovery-specify.md`): **pass** at
after_specify, after_plan, and after_tasks over
register_version 0.9-draft (F036-C01…C15), after
five recorded rounds at after_specify (10, then
3, then 1, then 1, then 0 failure modes — atomic
rewrites, boundary trims, pairwise boundary
confirmations, and one pair separated by
truthful phrasing; propositions, falsifiers, and
verdict rules unchanged throughout). No claim
stood below the 0.70 confidence threshold in any
round (minimum confidence 0.845). Final passing
artifacts:
`aee-after_specify-20261020T200301Z.json`,
`aee-after_plan-20261020T200316Z.json`,
`aee-after_tasks-20261020T200318Z.json`, with
their evaluator counterparts. The register is
unchanged since that pass; this freeze adds no
claims and alters no claim text after it.

Execution note (environment): the hook passes
were computed by the pinned AEE engine itself
(applied-epistemic-engineering 1.0.4, the Glossa
venv build) through the repo's own adapter
(`.specify/extensions/aee/scripts/python/run_aee.py
assess`), which drives the engine's CLI assess
command; the artifacts committed here are the
engine's own serialisations, copied byte-exact
from the CLI's outputs. (At the Spec 035 freeze
the same passes were computed in-process because
that session's write restriction blocked the
CLI's file outputs; no such block applied here,
and no in-process substitution was needed.) The
.specify ledger is working-tree state and is not
part of any spec's committed record (the Spec
032–034 pattern); no ledger append is claimed.
The draft-stage dependency-integrity self-check
recorded at the draft was superseded by these
passes and by the framework026 machinery in CI.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
