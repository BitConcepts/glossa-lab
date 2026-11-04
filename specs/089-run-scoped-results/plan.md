# Spec 089 — implementation plan

**Date**: 2026-11-04. **Package branch**: `feat/089-spec-package` (this
package; repo home on adoption: `specs/089-run-scoped-results/`).
**Proposal basis**: the owner's run-scoped-results directive
(2026-11-04; `records/directive-and-grounding-2026-11-04.md`), carrying
the Winning Combination build order as its design rule: definitions
before machinery, producers before the gate that verifies them, the
gate before any publication that claims its coverage.

Build order:

**run-defs + record/index formats → settling adoption → junction tool
→ suite/experiment surfaces → GATE (V11) + legacy index.**

## Stage 0 — package adoption (precondition for every build stage)

- The package (spec.md, claims.md, aee-claims.json, plan.md, tasks.md,
  records/) lands in the repo as `specs/089-run-scoped-results/` on the
  package branch, PR'd and merged on the owner's block approval.
- **T002 (done at drafting, re-verified at adoption)** — the C089 bundle
  was run through the pinned assessor in the CI-faithful venv, the same
  invocation as Spec 088's T002:

  ```
  ~/workspace/venvs/glossa-ci/bin/aee validate aee-claims.json
  → valid: 20 claim(s) in aee-claims.json   (exit 0)
  ~/workspace/venvs/glossa-ci/bin/aee assess --no-ledger \
      --input aee-claims.json --output records/t002-aee-assessment.json
  → exit 1; outcome: iterate
  ```

  Verbatim summary of record: "Assessed 20 claim(s); found 91 failure
  mode(s); 20 claim(s) below the 0.70 confidence threshold. Shared
  evidence: 1 supporting source(s) shared across 20 of 20 claim(s)…
  Draft cap: 20 draft claim(s) capped at gather_evidence/iterate
  (FR-2.3). Stage cap: 20 claim(s) below stage 'explained'; the outcome
  cannot be 'pass' (Spec 004 R1.4)…" (full text: `records/t002-note.md`;
  the assessment itself: `records/t002-aee-assessment.json`). `iterate`
  is the expected outcome for a draft bundle on a single asserted
  source; the owner's approval (T003) is the human act. The bundle was
  generated from claims.md by script; the generator reproduces Spec
  088's committed bundle byte-identically from its claims.md, and this
  bundle's set identity (20 ids, in order, one falsifier each) was
  verified mechanically (t002-note.md).
- **Pre-append gate check (the freeze discipline)**: before the intake
  append, the adoption PR runs the gate CLI on the un-appended tree and
  records ALL PASS, so any post-append failure is attributable to the
  append and not to drift (the Spec 088 adoption shape).
- **T003 — owner block approval** of spec + 20 claims + this plan +
  decisions D-089-1..6 (including the comparability judgment row,
  D-089-4). No build task starts before it.
- **T004 — adoption intake**: the claims enter the ledger through
  `tools/ledger/import_bundle.py --spec specs/089-run-scoped-results
  --date <adoption date>` — never a hand-edit of claims.jsonl —
  followed, in the same motion, by regeneration of the generated layers
  over the grown ledger and the settling-chain refresh the pin move
  forces (canonicals verified 6/6 over the new build before the pin
  refresh, per the re-derivation discipline), exactly the Spec 087/088
  adoption shape. **Named transition**: that refresh is executed under
  the *old* content-addressed discipline — it is the last pre-spec
  refresh — and both the pair it replaces and the pair it produces are
  first-class legacy-index population for S5. Claim C089-18 bounds the
  whole spec's ledger diff to this append.

## Dependencies

- Spec 086 complete (ledger, gate V1–V9, gated publish, settling
  semantics + engine + canonicals) — landed 2026-11-02. Spec 087
  complete — landed 2026-11-03. Spec 088 complete through S5 with S6
  (register ratification) the owner's act; this spec depends only on
  088's landed machinery (gate V10, program-map artifacts' stamp
  discipline), not on the register.
- The gate's registered-copies pattern (`ledger_gate.py`: matrix-defs,
  settle copies, program-map-defs copies) as the V11 pattern — in the
  tree.
- `run_settling.py`'s `_first_divergences` as the localization seed —
  in the tree.
- The delivery checker (`tools/delivery-check/check_delivery.py`) as
  the CI-citation discipline S4 generalizes — in the tree.
- S2 depends on S1 (formats). S3 depends on S1+S2 (junctions are
  computed over indexed run records). S4 depends on S1 (header format);
  its junction trigger depends on S3. S5 depends on S1–S4 (V11 verifies
  the whole machinery; the legacy index needs the stores in their final
  shape).

## Stage 1 — run-defs v1, run record, run index

**PR**: `feat/089-s1-run-defs` → one PR (defs document + record/index
library + tests).

**Contents**:

- `glossa-indus/ledger/RUN-DEFINITIONS.md` — **run-defs v1**, registered
  exactly as matrix-defs and program-map-defs were: a version header,
  the statement that amendment is a new version propagated to every
  registered copy in the same motion, and the rules:
  - *Surfaces (closed list)*: settling runs; backend experiment jobs
    (cited); study re-executions; suite runs cited as evidence. An
    execution is result-bearing iff its output is written to a store of
    record or cited in a record of record.
  - *Run id*: `<surface>-<yyyymmddThhmmssZ>-<6 lowercase hex>`, minted
    by the executing tool at execution start (D-089-1). Ids name
    executions, never content.
  - *Run record header*: run_id; surface; tool + tool version;
    started/finished execution stamps (wall clock — a run record is an
    event record, not a generated artifact; the input-derived stamp
    discipline for generated artifacts is untouched); comparability key
    (below); result block, or an absence block `{kind:
    empty|refused|crashed, detail}` for no-result executions.
  - *run-key v1*: components {surface, command/tool + version, code
    version (tree git SHA), input pins (per-surface list; settling:
    the existing pins block verbatim), seed (or the registered
    no-seed marker), environment class}. **Constitutive** (agreement
    required for comparability): surface, command/tool, input pins,
    seed (D-089-4). Recorded-and-diffed: code version, environment
    class.
  - *Determinism classes*: settling = deterministic; generated-layer
    builders = deterministic; suite = named-nondeterministic, known
    shape #1 registered (tray teardown flake: divergence confined to
    teardown ERROR entries on the registered test ids, pass/fail counts
    otherwise equal); backend jobs = per-graph registration, default
    named-nondeterministic for LM-bearing graphs, deterministic only by
    a per-graph registration act.
  - *Junction dispositions*: explained-by-named-difference /
    not-comparable / identical-after-all / unexplained. The mechanical
    explained case is registered narrowly: a divergence wholly inside a
    registered nondeterminism shape for that surface is
    explained-by-named-difference citing the shape + the divergent
    lines; every other explanation is an adjudication act (S3).
  - *Run index*: one `run-index.jsonl` per run store, append-only act
    lines — `entry` (run id, record path, key, legacy flag where
    applicable), `supersedes` (new id, old id, act reference),
    `quarantine` (run ids, junction id), `adjudication` (junction id,
    ruling, actor, resulting state). Legacy ids:
    `legacy:<store-relative path stem>`.
  - *CI citation form* (for S4): a CI suite run is cited as {GitHub run
    id, head SHA, job name, per-job conclusion} — the delivery-checker
    quadruple.
- `backend/glossa_lab/run_records.py` — the shared library: id minting,
  header construction/validation per surface, index act application
  (append + fold to current state), legacy id derivation. The write
  entry points register with gate V9's writer census when S5 lands
  (the registration act is S5's; S1 names it as owed).
- Library tests with teeth: id format + 10,000 same-second mints
  unique; header validation refuses a missing key component per
  surface; index fold applies supersede/quarantine/adjudicate sequences
  and refuses an act naming an unknown run id; legacy derivation stable
  over the standing store's real paths.

**Verification**: library test module green; a dry-run fold over a tmp
copy of the standing runs store enumerates exactly its 2 records under
legacy ids with the recoverable key components (semantics, candidate,
pins) and `legacy — key partial` (no execution stamp, no code version
exists to recover).

**CI jobs**: the library tests join the existing **Backend tests** job.
No new CI job.

**Claims**: C089-1 (format side), C089-2 (format side), C089-9,
C089-17 (format side), C089-19.

## Stage 2 — Settling surface adoption

**PR**: `feat/089-s2-settling` → one PR (engine write path + CLI +
index over the standing store + teeth).

**Contents**:

- `settling.py`: `run_record` gains the run-defs header — the run id is
  an *input* minted by the caller (the function stays pure; in-memory
  recomputations such as verify-canonicals carry ephemeral ids marked
  non-store and are never written). `write_run_record` writes under a
  filename derived from the run id, never from content; the
  content-addressed `run_record_filename` is retired (kept importable
  for one release as a legacy-path resolver, its overwrite behaviour
  removed). A write that would collide with an existing store path
  refuses (id collision = a named refusal, not an overwrite).
- `run_settling.py`: `run` mints + writes the index `entry` act;
  `materialize-sets` becomes a run (record + entry act) and the
  assignment-sets artifact gains the producing-run binding in its
  header block; canonical re-derivation acts that supersede a stored
  record append a `supersedes` act and leave the superseded record in
  the store.
- The standing T405 pair is **not** renamed or rewritten (C089-17); the
  index built in this stage covers it by legacy entries (full legacy
  enumeration incl. git-history generations is S5's completion; S2's
  index covers what stands in the store).
- Teeth (tmp copies throughout): the same scenario run twice produces
  two records with distinct ids and byte-equal result blocks, the index
  folds both, and no junction trigger fires (identical); a run over a
  mutated pin produces a record whose key diff against the standing
  pair is exactly the pin (the S3 junction's raw material, proven to
  exist); a forced id collision refuses; the store census is monotonic
  across the whole seeded sequence.

**Verification**: `verify-canonicals` still reproduces 6/6; the gate's
V8 legs pass unchanged (the gate's own settle copies and expectations
are untouched — the header addition is additive to store records, and
canonical expectations compare result blocks); full gate CLI ALL PASS
on the real tree with the index present.

**CI jobs**: Backend tests (engine + CLI tests); the ledger-gate job
unchanged (V8's expectations are result-block comparisons).

**Claims**: C089-2, C089-5, C089-7 (assignment-sets side).

## Stage 3 — The junction tool

**PR**: `feat/089-s3-junction` → one PR (comparator + CLI + junction
store + automatic triggers + teeth).

**Contents**:

- `backend/glossa_lab/run_junction.py` — the pure comparator: two run
  records (+ their index context) → a junction report record: both run
  ids; the component-by-component key diff (constitutive components
  marked); the environment diff; the first divergent output localized
  by recursive descent over the result blocks (dict/list/scalar; the
  divergence cap and path format follow `_first_divergences`' precedent
  in `run_settling.py`), with the one-side-empty case localized as the
  first result present on the non-empty side; the disposition.
  Disposition logic, in order: constitutive key difference →
  not-comparable (no result diff claimed); result blocks equal →
  no report (the pair is identical; the scan lists it as such);
  divergence wholly inside a registered nondeterminism shape for the
  surface → explained-by-named-difference citing the shape and the
  divergent lines; otherwise → unexplained, and the report carries the
  red-team section (below) and the tool appends `quarantine` acts for
  both runs to the store index.
- The **red-team section**: the six registered candidate causes (input
  drift, code drift, environment drift, nondeterminism, record
  corruption, presentation artifact), each pre-filled by the tool with
  the mechanical evidence that bears on it (pin diff lines for input
  drift; code-version diff for code drift; the presentation-artifact
  cause is checked against the record store itself — if both records
  are byte-stable and the divergence exists only in a presentation of
  them, the disposition is identical-after-all instead). The
  sustained/not-sustained markings are completed by the red-team act
  (an agent or human working the junction under the standing red-team
  practice); the tool's automation claim is exactly C089-14's: the
  report, the evidence pack, and the quarantine exist without anyone
  having to remember to ask.
- `tools/ledger/run_junction.py` — CLI mirroring `run_settling.py`:
  `compare RUN_A RUN_B` (prints + writes the report on a triggering
  pair), `scan --store PATH` (every comparable pair in the index:
  identical pairs listed, triggering pairs reported + written),
  `adjudicate JUNCTION_ID --ruling ... --actor ...` (appends the
  adjudication act; lifts or confirms quarantine; never edits the
  report or the run records).
- Junction store: `glossa-indus/ledger/junctions/<junction-id>.json`,
  junction ids minted like run ids (`junction-<UTC>-<6 hex>`); reports
  immutable; a re-analysis is a new report naming the same pair.
- Automatic trigger, settling surface: `run_settling.py run` ends with
  a scan of the new record against its comparable predecessors in the
  index (same scenario or same candidate+scope family per the key), so
  a divergent rerun produces its junction + quarantine in the same
  invocation that created the run.

**Verification**: fixture-pair teeth — identical pair (no report,
listed identical); divergent deterministic pair (report + quarantine
acts; the first divergence path is the seeded one); one-side-empty
pair (absence block vs result block; localization = first present
result); constitutive-diff pair (not-comparable, no quarantine);
flake-shape pair on the suite determinism registration
(explained-by-named-difference citing the registered shape);
adjudication lifts a quarantine and a second adjudication confirms one
(both as acts; the run records' bytes unchanged throughout — asserted
by hash). The standing tray-flake instance is replayed as a worked
example in the stage record: the PR #509 attempt-1/attempt-2 pair's
recorded summaries (from the CI job logs of record) entered as two
suite-surface fixture records, junctioned, disposition
explained-by-named-difference — the manual adjudication of 2026-11-04,
reproduced mechanically.

**CI jobs**: Backend tests (comparator + CLI teeth). No new CI job.

**Claims**: C089-11, C089-12, C089-13, C089-14.

## Stage 4 — Suite and experiment surfaces

**PR**: `feat/089-s4-surfaces` → one PR (suite run-record helper + CI
citation application + experiment citation records + the worked
examples in the stage record).

**Contents**:

- Suite surface: `backend/glossa_lab/run_records.py` gains the suite
  light-record writer, driven by a CLI (`tools/runs/suite_run_record.py`):
  given a pytest invocation's output file and the tree, it writes the
  run record (command; tree SHA + dirty flag; result summary parsed
  from the run's own output — counts and the failed/errored test ids,
  never from a presentation of the run; the **rewrite manifest**: paths
  under `glossa-indus/claims/` and `glossa-indus/reports/` whose bytes
  differ from HEAD after the run, with the disposition — restored
  (bytes verified equal to HEAD after restore) or retained (reason
  required)); the record's key carries the suite determinism class
  from run-defs v1. From this stage, Spec 089's own stage records cite
  suite evidence only under this binding or the CI quadruple
  (self-application).
- CI citation application: the stage record for S4 cites its own PR's
  CI by {run id, head SHA, job, conclusion} for every job it relies on
  (the delivery-checker discipline, generalized from merge gates to
  evidence citations — no code change; the checker already resolves
  the quadruple).
- Experiment surface: a citation-record writer
  (`tools/runs/job_citation.py`): given a backend job id, it reads the
  job + results through the backend API, and writes the repo-side run
  record (header format; inputs = graph id + registered version,
  parameters, and the job's own recorded fields; result block = the
  job_results payload hash + the summary the citing record will quote).
  Exercised once against the live backend on an existing completed job
  (read-only; no new experiment is run for the stage), the citation
  record filed in the stage record's annex. New citations of experiment
  results in stage records use this form from this stage.
- Study re-executions: run-defs v1's header applied by convention in
  spec records (no tooling); the freeze-gate C2 record form is
  registered in run-defs as a junction precedent — a C2 pair
  (frozen values vs independent recomputation) is a junction whose
  disposition vocabulary this spec's S3 tool shares. No freeze-gate
  code changes.

**Verification**: helper teeth on fixtures (a fabricated dirty-tree
fixture produces the manifest + a retained-with-reason refusal when no
reason is given; summary parsing reads the output file, proven by a
fixture whose presentation text disagrees with its output file — the
record follows the file); the live-backend citation exercise's record
hash-checked against a second read of the same job; the stage record's
own citations conform (checked by the reviewer against this plan's
forms).

**CI jobs**: Backend tests (helper teeth; the live-backend read is not
a CI act — CI has no backend; the stage record carries that evidence).

**Claims**: C089-6, C089-8, C089-3, C089-4 (surface side).

## Stage 5 — Gate class V11 + legacy index

**PR**: `feat/089-s5-gate-v11` → one PR (gate class + registered copies
+ teeth + the legacy index build + writer-census registration).

**Contents**:

- `backend/glossa_lab/ledger_gate.py` gains **class V11 — run-binding**,
  following the V8/V10 pattern exactly: the gate carries its **own
  registered copies** of run-defs v1's checkable rules (the header
  required-fields list, the constitutive component set, the disposition
  vocabulary, the registered nondeterminism shapes) — not imported from
  `run_records` or `run_junction` — and checks, over the guarded set
  (the settling runs store + its index, the junction store, the
  generated layers' producing bindings, and citation records under
  `specs/*/records/` matching the run-record header format):
  (a) every published artifact in the set carries a producing run/build
  binding that resolves to an existing record;
  (b) no record in the set cites a run under an open unexplained
  quarantine as verdict support (the citation form of S4 makes this
  mechanically checkable: citations name run ids; the gate resolves
  them against the index's quarantine state);
  (c) each guarded store's census equals its index's folded census, and
  every supersedes/quarantine/adjudication act names run ids that
  resolve;
  (d) every comparable pair in a guarded store with divergent result
  blocks has a junction report whose disposition is in the registered
  vocabulary, and every unexplained junction's runs are quarantined in
  the index.
- **V9 registration**: `run_records` and `run_junction` join the
  registered-writer census; the run stores, index files, and junction
  store join the artifact path patterns, so an unregistered write to
  them is itself a gate failure.
- **Legacy index completion**: every run record that has ever stood in
  the settling store, enumerated from git history (the T403 originals
  and the 087/088/089-adoption refresh generations), receives its
  legacy index entry; entries for records no longer in the store name
  the superseding commit and the record's blob hash. The two
  `re_derivations` entries in `settling-canonical.json` are indexed as
  legacy run events pointing at that file. After this stage the index's
  folded census covers the store's whole history, and V11's census leg
  runs over it.
- **Teeth tests** (`backend/tests/test_ledger_gate.py` additions): one
  seeded case per leg on tmp copies — an unbound artifact fails (a); a
  quarantined citation fails (b); a dropped record (census mismatch)
  and a dangling supersedes link fail (c); a divergent pair with no
  junction report, and a report with an out-of-vocabulary disposition,
  fail (d). Seeded means seeded: the tests mutate copies, never the
  tree.

**Verification**: gate CLI over the real tree reports ALL PASS with V11
present in the per-class list; the teeth tests pass; V1–V10 behaviour
unchanged (full gate test module green); the legacy index's folded
census is quoted in the stage record against a hand enumeration of the
store's git history (the independent-path check).

**CI jobs**: the existing **ledger-gate** job runs the gate CLI — V11
joins its report with no workflow change (the Spec 088 S3 argument: the
job's contract is "the gate, whole").

**Claims**: C089-15, C089-16, C089-17.

## Closeout

- **T601 — closeout record**: per-claim dispositions for C089-1..20
  (discharged / carried, with the evidence pointer for each); the run
  census at close (stores, records by surface, index acts, junction
  reports by disposition, open quarantines — expected zero, or named);
  and the explicit statements that no standing verdict was
  re-adjudicated by this spec, no claim's status/stage/score moved, and
  the fabricated-delivery protocol's boundary held throughout (no
  junction was opened over a presentation, and no run record was cited
  as certifying one).

## Design rules carried through every stage

- **Producers before the gate**: S1–S4 build the machinery and use it
  under their own stage discipline; V11 (S5) verifies it with
  independent copies before any artifact claims gate coverage as
  run-bound. Nothing in S2–S4 is a published program surface; the
  stores are internal records, and the first verdicts that cite runs
  as *gate-verified* bindings are post-S5 verdicts.
- **Records are never edited to fix relations**: supersession,
  quarantine, and adjudication are index acts. A stage that finds
  itself editing a run record has found a defect, not a shortcut.
- **Verdicts and counts come from records** (run records, index folds,
  junction reports, gate reports), quoted in stage records — never from
  summaries of them, and never from background-delivery presentations
  (the fabricated-delivery protocol applies to this spec's own work
  throughout).
