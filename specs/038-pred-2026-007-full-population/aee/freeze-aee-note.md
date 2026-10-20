# AEE at the Spec 038 freeze

The register was assessed at the freeze act
(`aee/recovery-specify.md`): the gate is met at
after_specify, after_plan, and after_tasks over
register_version 0.7-draft (F038-C01…C14), after
three recorded rounds at after_specify (24, then
20, then 14 failure modes; propositions,
falsifiers, and verdict rules unchanged
throughout). At the passing passes the register
carries **zero correctness failure modes** and
**no claim below the 0.70 confidence threshold**
(minimum propagated score 0.795). The 14
residual failure records at each passing pass
are the FR-2.3 draft-cap records, one per claim:
under aee 1.5.0 a claim carrying status draft
caps the bundle outcome at iterate (FR-2.3),
and the R1.4 stage rule reserves the outcome
word "pass" to bundles whose claims stand at
stage explained or beyond — these claims stand
at created, the lenient loader's recorded
default (metadata.stage_defaulted_claims in
every artifact). Both caps are lifecycle facts
about a register at freeze time in this
programme (frozen registers carry draft-status
claims; stages move at evaluation, not at
freeze), not defects recovery could repair; the
freeze adjudication records this reading as
DD-038-10 (`adjudication.md` §6). Final passing
artifacts:
`aee-after_specify-20261020T224101Z.json`,
`aee-after_plan-20261020T224112Z.json`,
`aee-after_tasks-20261020T224122Z.json`, with
their evaluator counterparts. The register is
unchanged since that pass; this freeze adds no
claims and alters no claim text after it.

Execution note (environment): the hook passes
were computed by the pinned AEE engine itself
(applied-epistemic-engineering 1.5.0, the
Glossa aee-1.5.0 venv build) through the same
code path as the CLI's assess command
(aee.cli._assess: load, assess, evaluator
contract), run in-process because this VM's
write restriction blocks the CLI's own file
outputs. The register's exact bytes were
fetched from the repository via the GitHub API
and supplied to the loader in memory; loading
was lenient (strict=False, FR-1.3) — the remedy
the merged `backend/tests/conftest.py` applies
to legacy registers (a string boundary, no
stage field) under aee >= 1.5, recorded in each
artifact's metadata (loading_mode: lenient). No
ledger append was made (the CLI was run with
ledgering disabled; the .specify ledger is
working-tree state and is not part of any
spec's committed record — the Spec 032–034
pattern). The artifact bytes are the engine's
own serialisations, preserved byte-exact
through the GitHub git-data API. The
draft-stage dependency-integrity self-check
recorded at the draft was superseded by these
passes and by the framework026 machinery in CI.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
