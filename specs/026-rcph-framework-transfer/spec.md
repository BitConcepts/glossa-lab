# Spec 026 — RCPH Framework Transfer, Impact Audit, and Reruns

> ## PROPOSAL — FOR OWNER ADJUDICATION RECORD
>
> Directed by the owner (Tristen Pierson) on 2026-10-10: *"Take
> notes from how the RCPH study framework works and see what we
> can apply here to make this more powerful. And rerun all things
> that are impacted and improved by this framework. … make sure
> the framework uses spec-kit + AEE extension and epistemic
> stuff."* This spec is the proposal (H2) for that program. No
> rerun executes before the classification criteria (§5) and the
> impact register (§6) are frozen and merged, and no rerun
> executes before its own rerun contract is frozen (§7).

**Phases:** 142–145 reserved for reruns (final assignment in the
frozen register) · **Parent:** the full Indus program, Specs
001–025 · **Date of proposal:** 2026-10-10.

**AI disclosure:** this spec is produced by an AI agent (Muse
Spark, via Muse) at the direction of Tristen Pierson, per
constitution §VI.

---

## 1. Why this spec exists

The RCPH formalization program (`~/workspace/rcph-formalization`)
runs its research under a general constraint-research framework
(`docs/GENERAL_RESEARCH_FRAMEWORK.md`, v1.1; `docs/
RESEARCH_METHOD.md`; `docs/FRAMEWORK_REVISION_022.md`) whose
discipline caught real defects in that program's own history —
most instructively the QD gate of Specs 019/021 there: a frozen
acceptance rule that *could not discriminate* the target property
from generic cases, so two historical SURVIVES labels stand in
their files while their evidentiary status is superseded in a
separate assessment record. Glossa has local instances of the
same defect class: the Phase-114 blind-affiliation generator
(grammar-free system won 100% of draws — a non-discriminating
instrument discovered only in execution), the Phase-107 SA
controls (Sanskrit and scrambled controls statistically
identical to the target condition), and calibration-rejected
batteries (Phases 113, 115–118) whose negative labels are
routinely at risk of being read as contradictions of the claims
they never validly tested.

Glossa already practices much of the framework piecemeal —
per-spec freezes (Specs 024/025), lineage labels, designed NOT
ESTIMABLE outcomes, BH families declared in advance, append-only
ledgers. What it lacks is the *general* machinery: a claim
register with stable IDs and mechanical dependency checks, a
canonical freeze record a run can be replayed against, a verdict
taxonomy with precedence, origin-group evidence accounting as a
program-wide unit, and practical margins next to p-values. This
spec builds that machinery, audits every prior Indus analysis
against it, and reruns what the audit shows to be rerun-able.

## 2. Scope

IN: (a) the framework transfer (§4) as standing Glossa
methodology documents + machinery; (b) an impact audit of ALL
specs 001–025 and ALL numbered Indus phase artifacts 52–141
(§§5–6); (c) reruns of every item the frozen register classifies
RERUN-REQUIRED (§7); (d) historical assessments for every item
whose evidentiary status changes (§8).

OUT: anchor changes (forbidden in this program — a rerun that
undermines an anchor's support is flagged for owner adjudication,
never actioned); PRED-2026 scoring (no qualifying independent
corpus exists; the readiness adjudication is at most reproduced /
reinterpreted); SA rehabilitation (H26 stands); re-coding of the
Phases 132/134/135 pilots (rerun = rescoring from on-disk records
only); publication (changed findings go to the owner first — no
Zenodo/OSF action in this program); any new data acquisition.

## 3. Tooling (verified 2026-10-10, Step A)

Full record: `working/tooling.md`. Facts that govern execution:

- specify CLI 1.0.10; AEE extension v1.1.0; evaluator extension
  v1.0.0; both enabled in `.specify/extensions.yml`.
- The `aee` package is 1.0.4 in the Glossa venv and 1.0.2 in the
  spec-kit venv — **all AEE invocations in this spec run with the
  Glossa venv on PATH**, and the version is recorded in every
  assessment artifact.
- Extension commands are agent-executed markdown driving
  `.specify/extensions/aee/scripts/python/run_aee.py`
  (`assess` at specify/plan/tasks/implement stages; `gaps` after
  verify). The gate scale is `pass | warn | iterate | clarify |
  gather_evidence | block` (exit 0 / 1 / 2). **Governing
  threshold (RCPH rule, adopted): any outcome stricter than
  `warn` blocks closure until recovery work is done.** Glossa's
  extensions.yml marks the hooks optional; this spec treats them
  as mandatory for Spec 026 and saves every output under
  `aee/` in this spec directory — Specs 024/025 left no saved
  assessment artifacts, and that gap is itself a finding.
- `speckit.evaluator.run` has no registered evaluators in this
  repo (no `evaluators.yml`); its honest output is a `pass`
  noting none configured, and the operative evaluator result is
  the Evaluator Contract result produced inside AEE assess. This
  is recorded, not papered over.
- `backend/glossa_lab/aee_core.py` (constitution §IV: the same
  engine) provides `ClaimGraph.cycles()` (verified live) and
  `missing_dependencies()` / `conflicts()`, but **no
  forbidden-assumption inheritance check exists** in the `aee`
  package or `aee_core.py`. Building it is FR-026-2.

## 4. The transfer

`transfer-map.md` (this directory) is the governing transfer
document: each of the twelve RCPH principles with its source,
its Indus adaptation, the existing Glossa equivalent, the gap,
and the adopted change. Headline adaptations:

1. **No target-reading/language smuggling** (RCPH Rule 1):
   hypothesized readings, SA outputs, later-language outcomes,
   or the desired decipherment may not serve as premises,
   features, controls, labels, or tuning targets in a test of
   those same claims. Bridge assumptions are named records,
   never absorbed. (H26 is the promotion-gate instance; this
   generalizes it to all test design.)
2. **Claim taxonomy + stable IDs**: kinds = definition / data
   observation / computational result / conditional model result
   / empirical identification / conjecture-bridge. Every
   governed claim carries boundary, assumptions, `depends_on`,
   `forbidden_assumptions`, falsifier, strongest rival.
3. **Computation/countermodel symmetry**: positive closure or a
   discriminating countermodel/null defeating the bounded claim
   are both successful outcomes; a narrow closure never closes
   a broader target.
4. **Evidence independence by origin group**: derivative
   corpora (ICIT-lineage layers) count once; generated
   assertions are neutral evidence; support/oppose/neutral are
   retained separately, never averaged away.
5. **Discriminating controls**: positive AND negative controls
   declared in every freeze; a control that cannot fail/pass
   differentially makes the run INVALID, not caveated.
6. **Verdict taxonomy**: INVALID / INCONCLUSIVE / CONTRADICTED /
   SUPPORTED, with the §8 mapping onto historical labels.
7. **Freeze + replay integrity**: canonical freeze record
   (definition + source/data hashes + seeds + environment)
   committed BEFORE confirmation data is examined; a changed
   gate = new version + new freeze, never a regenerated digest
   over an old run.
8. **Practical margins + uncertainty**: effect margins declared
   in the freeze; intervals accompany p-values; an interval
   crossing the margin is INCONCLUSIVE by default.
9. **Exploratory/confirmation separation**: confirmation only
   on held-out or fresh data under the frozen contract; post-hoc
   readout optimization spawns a new exploratory branch.
10. **Completeness grids**: declared grids validated exactly;
    missing cells = INCONCLUSIVE, never pooled away.
11. **Source-version checking**: criticism of v1 asserts
    nothing about v2; snapshots pinned by hash.
12. **Historical-assessment discipline**: originals are never
    rewritten; superseding interpretations live in new records
    (§8) stating exactly what an old run does and does not
    establish.

What does NOT transfer: kernel-checked proof (Lean). The honest
Indus analogue of "kernel-checked" is *deterministic replay +
independent recomputation*; the transfer map says so in terms.

## 5. Classification criteria (frozen before the register)

Criteria are keyed to method features only — never to whether
the original result was welcome. The criteria document
(`classification-criteria.md`) is committed and merged BEFORE
the register that applies it; reclassification afterwards
requires a dated amendment with reason. Classes:

- **RERUN-REQUIRED** — a framework correction is specifiable
  without inventing new data AND could materially change the
  estimate, verdict, or evidentiary status. Named correction
  types: (C1) verdict rested on a p-value alone where an effect
  estimate + interval + the §4.8 margin rule are computable from
  recorded data; (C2) derivative layers were counted as
  independent corroboration and an origin-group-collapsed
  recomputation is possible from recorded data; (C3) a declared
  control was non-discriminating and a discriminating control is
  constructible from recorded data; (C4) scores/verdicts are
  recomputable from complete on-disk records under the taxonomy
  (rescoring-type rerun, e.g. coding pilots).
- **REPRODUCE-ONLY** — deterministic replay of the recorded
  computation suffices to establish what the run shows.
- **REINTERPRET-ONLY** — no rerun can cure the defect (missing
  independent data, invalid instrument basis, unrepeatable coder
  basis); the historical assessment changes instead.
- **UNAFFECTED** — the framework was already satisfied; the
  register cites the evidence.
- **NOT-RERUNNABLE** — source/code/data for the original
  experiment definition are not recoverable from the record;
  preserve + label.

## 6. Impact register

One row per spec (001–025, with 021's duplication recorded) and
per phase (52–141 as present in the record), machine-readable
(JSON + CSV + MD rendering): claims, data origin groups,
controls + discriminating status, independence structure,
freeze/replay status, uncertainty/margin status, completeness
status, classification, rationale, rerun specification where
any. The extraction base is `working/inventory.json` (116
items); the register is a freeze point merged before reruns
begin.

## 7. Rerun discipline

Each rerun: new phase number (142+), new experiment ID, the
H15/H23 five-step gate in order (script → graph module →
registration → registration verified → run), data read from
registered/database sources (H16), a frozen rerun contract
(committed before the run) naming exactly which framework
correction is applied and what original-vs-rerun comparison will
be reported, deterministic seeds, timeouts on all commands (H9).
Reruns never tune toward the original answer. Each rerun report
carries: original result (verbatim values), rerun result,
same/different and why, verdict under the §4.6 taxonomy, and its
historical-assessment entry.

## 8. Verdict taxonomy + historical assessments

Mapping (historical label → framework reading; the label in the
original file never changes):

| Historical | Framework reading |
|---|---|
| SUPPORTED (with frozen gates met) | SUPPORTED (bounded claim only) |
| NOT SUPPORTED / NULL / FAIL (valid test, pre-declared margin met by the null side) | CONTRADICTED (bounded claim) |
| FAIL / NULL from a valid test WITHOUT a pre-declared practical margin | INCONCLUSIVE unless the register's margin rule adjudicates otherwise |
| REJECTED at calibration / middle-band / NOT ESTIMABLE / DESCRIPTIVE | INCONCLUSIVE (no valid confirmation test completed) |
| INVALID RUN / control-validity failure | INVALID |
| KILL (program-level disposition) | disposition, not a verdict: the underlying bounded verdict is recorded separately |

`historical-assessments.md` (+ JSON) holds one entry per item
whose evidentiary status changes: item, original label
(verbatim), superseding framework status, what the old run does
establish, what it does not establish, and the rerun link where
one exists.

## 9. Epistemic boundaries (H13)

Assumptions: (i) the on-disk record (reports, ledgers, frozen
specs) is the authoritative history — where it is silent, fields
are `unknown`, never reconstructed from memory; (ii) margins
adopted in rerun contracts are conventions declared in advance
(e.g. an effect-size floor), not discoveries; (iii) the AEE gate
score is a governance signal, not a probability a claim is true
(RCPH manual, in terms).

Adversarial challenges that could break this program: a rerun
that quietly re-derives the original pipeline's hidden tuning
(survivorship in correction choice — countered by §5's frozen
criteria + §7's no-tuning rule); a register classification chosen
to make the rerun set small (countered by criteria-first freeze
+ per-row rationale); taxonomy relabeling mistaken for new
evidence (countered by §8: assessments state what did NOT
change).

BeliefArtifacts relied on: the program's claim records in
`glossa-indus/claims/` and the phase artifacts themselves; no P1
belief artifact below MEDIUM confidence is load-bearing for any
rerun verdict — rerun inputs are recorded data files, not claim
scores.

## 10. Requirements

- **FR-026-1** Transfer document (§4) covering all twelve
  principles + the non-transfer section.
- **FR-026-2** Claim-register machinery on `aee_core`: stable-ID
  claim records for Spec 026's governed claims; mechanical
  cycle detection + forbidden-assumption inheritance check
  (new); unit tests incl. a planted-cycle and a planted
  forbidden-inheritance case that must fail loudly.
- **FR-026-3** Freeze/replay machinery: canonical freeze record
  builder + verifier (digest over canonical definition JSON +
  source hashes + environment), used by every Spec 026 rerun;
  unit tests incl. a tampered-payload case.
- **FR-026-4** AEE + evaluator assessments actually run and
  saved at specify / plan / tasks / implement stages, and `gaps`
  after verify; any outcome stricter than `warn` blocks closure
  until recovery work is recorded.
- **FR-026-5** Classification criteria (§5) committed + merged
  before the register; register (JSON+CSV+MD) covering specs
  001–025 + phases 52–141, committed + merged before reruns.
- **FR-026-6** Every RERUN-REQUIRED item rerun under §7, or
  carrying an evidenced hard-stop (why a rerun is impossible
  without changing the historical experiment).
- **FR-026-7** Historical assessments (§8) for every item whose
  evidentiary status changes; originals untouched (verified by
  diff discipline: no edits to historical report files).
- **FR-026-8** Closeout: full suite + foundation check on
  merged main (0 failures), anchors byte-identical, both
  ledgers appended, no publication.

## 11. Decision asks

None outstanding at proposal time: the owner's directive
authorizes the transfer, the audit, and the reruns it identifies.
Anchor changes and PRED scoring stay outside this spec whatever
the reruns show (§2); anything of that kind returns to the
owner as a flagged assessment.
