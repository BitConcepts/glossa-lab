# Feature Specification: Run-Scoped Results — Run Identity, Isolation, Comparability, and the Junction Rule

**Feature Branch**: `089-run-scoped-results` (build stages); this package
lands on `feat/089-spec-package`
**Created**: 2026-11-04
**Status**: Draft package — awaiting the owner's block approval (Stage 0, T003)
**Input**: The owner's instruction in this chat, 2026-11-04: "prevent
previous runs from impacting new runs when it comes to results. we must
lump results by the run and not allow contamination. if two similar
runs produce different results or one produces results and one doesn't,
we need extra scrutiny, perhaps an automatic red team analysis of the
junction" — routed fleet-wide by the main chat the same day; Glossa-Lab
takes it as this spec. The directive grows out of the fabricated-delivery
investigation closed the same morning (evidence pack:
`~/workspace/fabricated-delivery-redteam-2026-11-04/`, REPORT.md +
leakage-check addendum), whose subject was *presented* results; this
spec's subject is *recorded* executions (see §Non-goals for the
boundary, and claim C089-20).
**Evidence of record**: the grounding census in
`records/directive-and-grounding-2026-11-04.md`, counted and read
first-hand from the repo on 2026-11-04: the settling run store
(`glossa-indus/ledger/runs/` — 2 records, content-addressed filenames,
no run id, no execution timestamp, no code version in the record); the
dual-run comparison (`backend/glossa_lab/settling.py` `compare_runs`,
semantics §7 — refuses same-candidate and cross-build pairs by
construction); the gate (`backend/glossa_lab/ledger_gate.py`, classes
V1–V10; V11 is the next free class); the backend job store
(`jobs`/`job_results`, execution-minted uuid job ids, no repo-side run
record); the suite's in-tree rewrite behaviour and the tray-flake
divergence series (CI attempts 1 vs 2 over one head SHA on PRs #497,
#505, #509 and main's post-#503 run — five hand adjudications in three
days); the freeze-gate's C2 independent-recomputation precedent
(`tools/freeze-gate/`).
**Predecessors**: Spec 086 (the Winning Combination adoption: the
ledger, the gate, gated publication, settling semantics §7/§9 — this
spec's substrate), Spec 087 (registry discipline; the generated-layer
precedents), Spec 088 (the gate-extension pattern: a new class with its
own registered definitions, staged before the surface it guards; the
adoption-intake discipline this spec's C089-18 repeats).

## Problem statement

The program's results are not lumped by the run. They are lumped by
whoever cites them, from whatever mixture of executions happens to be
at hand — and the machinery permits it at every surface:

- **Settling.** A run record carries input pins but no identity: no run
  id, no execution time, no code version. Its store filename is a hash
  of its content basis, so a rerun of the same scenario over the same
  pins *overwrites its own record by design*. When the Spec 087 and 088
  adoption refreshes superseded the T405 pair, the superseded records
  left the store entirely; they survive only in git history, and the
  supersession is narrated in prose in `settling-canonical.json`.
- **Comparison.** The one comparison the program owns (semantics §7)
  compares two *candidates* over *one* build and refuses — by
  construction — both same-candidate pairs and cross-build pairs. Two
  executions of the same work returning different results is precisely
  the case it cannot speak to. The semantics already state the
  principle ("Two readings are never blended into one verdict"); the
  run-level machinery to honor it does not exist.
- **Backend experiments.** A job receives a real execution-minted id,
  and its results sit in the live database under that id — until a
  stage record cites the numbers in prose, at which point the binding
  to the execution and its inputs is lost.
- **Suite runs.** CI verdicts are bound to run ids by the delivery
  checker (that discipline works), but local evidence runs are cited
  as bare counts, and suite runs rewrite claim files inside the tree
  they are measuring — one run's outputs become the next run's inputs,
  controlled today only by a restore-by-convention step in stage
  records.
- **Divergence.** When two comparable runs do diverge, adjudication is
  a human remembering the precedent. The tray-flake family made CI
  attempt 1 and attempt 2 of the same head SHA disagree five times in
  three days (PRs #497, #505, #509; main post-#503); each time, a
  person read the job log, named the flake, and reran. Correct every
  time — and entirely unmechanized. The owner's directive names the
  general case: divergence between comparable runs, or results on one
  side and none on the other, gets extra scrutiny *before* either side
  is used, "perhaps an automatic red team analysis of the junction."

This spec builds the run level the program's other layers already
assume: identity for every result-bearing execution, records that
cannot be silently replaced, a registered definition of when two runs
are comparable, and an automatic junction analysis — with quarantine —
when comparable runs diverge.

## Scope — what this spec builds

- **S1 — run-defs v1, the run record, the run index.** A registered
  definitions document (`run-defs v1`, the matrix-defs/program-map-defs
  pattern): the run-id format and minting rule (D-089-1); the run-record
  header (run id, surface, comparability key, execution stamps, result
  block or named absence); the comparability key (run-key v1, D-089-4);
  per-surface determinism classes; the disposition vocabulary for
  junctions; the run index format — one index per run store, carrying
  the relations records cannot carry about themselves (supersedes /
  superseded-by, quarantine state with its junction reference, legacy
  entries). Note on stamps: a run record is a record of an *event*, not
  a generated artifact, so it carries wall-clock execution stamps; the
  Spec 086 input-derived-stamp discipline governs generated artifacts
  and is untouched.
- **S2 — Settling surface adoption.** `settling.py` / `run_settling.py`
  mint execution ids, write records under run-id filenames (the
  content-addressed overwrite retired), maintain the runs-store index,
  and record supersession as index links on refresh acts (the
  adoption-refresh pattern becomes a labeled relation, executed first
  over the standing T405 pair). `materialize-sets` becomes a run with a
  record; `assignment-sets.json` names its producing run.
  `verify-canonicals` behaviour is unchanged (same key + same result =
  the registered no-junction case, proven continuously).
- **S3 — The junction tool.** A standalone producer
  (`backend/glossa_lab/run_junction.py` + CLI, D-089-2): given two run
  records, or scanning a store's index for comparable pairs, it emits a
  **junction report** into the junction store
  (`glossa-indus/ledger/junctions/`): key diff, environment diff,
  first-divergent-output localization (generalizing
  `run_settling.py`'s `_first_divergences` to run-vs-run, including the
  one-side-empty case), and a disposition from the registered
  vocabulary. Automatic triggers: at run completion (against comparable
  predecessors in the index) and by store scan. The unexplained
  disposition appends the red-team tier (C089-14) and quarantines both
  runs in the index (C089-13).
- **S4 — Suite and experiment surfaces.** Suite runs cited as evidence
  get bindings (D-089-6): CI runs by their GitHub run id + head SHA
  (the delivery-checker discipline, extended from PR gates to any
  evidence citation); local evidence runs by a lightweight run record
  (command, tree SHA, input state, result summary, in-tree rewrite
  manifest + disposition). Backend experiment results get a repo-side
  citation record naming job id + recorded inputs at citation time
  (C089-8). Study re-executions mint run records in their spec's
  records under the same header (the freeze-gate C2 recomputation is
  registered as a junction precedent, not rebuilt).
- **S5 — Gate class V11 + legacy index.** The gate gains **V11 —
  run-binding**, with its own registered copies of run-defs v1's
  checkable rules: producing-binding presence and resolvability for
  published artifacts in the guarded set; no quarantined run cited as
  verdict support in the guarded set; store census == index census;
  supersession links resolve; every comparable divergent pair in a
  guarded store has a junction report with a registered disposition.
  The legacy index over all pre-spec run records is built in this stage
  (index-only, D-089-5), so V11's census legs have a complete
  population from their first run.

## Non-goals (explicit)

- **No retroactive re-adjudication.** Standing verdicts stand on their
  records. This spec governs new runs and new citations of old results;
  it re-opens nothing (C089-17).
- **No claim changes.** No stage adjudicates, reclassifies, annotates,
  or scores any claim. The spec's total ledger diff is its adoption
  intake append plus the regeneration that append forces (C089-18, the
  C088-15 pattern).
- **Not delivery integrity.** The fabricated-delivery protocol (owner
  order, 2026-11-04) is a separate, already-standing defense against
  fabricated *presentations*. This spec is run hygiene over *recorded
  executions*. A fabricated delivery is not a run; a run record does
  not certify a presentation. The boundary is claim C089-20, stated in
  the spec so neither defense is mistaken for the other.
- **No semantics change.** glossa-settle-1, matrix-defs v1, and
  program-map-defs v1 are untouched. Settling gains store discipline
  and identity; its rules do not move.
- **No CI replacement.** CI already mints run ids; this spec binds
  citations to them. No new CI job is proposed except where a stage's
  conformance tests join existing jobs (plan.md, per stage).
- **Not every command is a run.** Only result-bearing executions —
  output written to a store of record or cited in a record of record —
  mint ids and records. Exploratory commands remain exploratory.
- **No decipherment claim of any kind.** Run hygiene changes nothing
  about what any result means; the program's standing position (the
  Indus script is not deciphered) is untouched.

## Decisions

- **D-089-1 — Run-id format and minting point.** Options: (a)
  execution-minted opaque id, `<surface>-<UTC yyyymmddThhmmssZ>-<6 hex
  random>`, minted by the executing tool at start, before results
  exist; (b) content-addressed id (the settling store's current
  scheme); (c) sequential per-store counter.
  *Recommendation: (a).* Content addressing is the defect being removed
  (identical reruns collide; the id must name the execution, not the
  content). A counter fails across machines and stores (this program
  runs on two hosts). The timestamp-plus-random form is sortable,
  collision-safe at program scale, and — because it is minted at start
  — an empty or crashed run still has an id and a record, which the
  owner's one-side-empty case requires. Minting is by the executing
  tool (the surface's own runner), never assigned later by a citing
  record.
- **D-089-2 — Junction analysis: standalone tool, gate verifies.**
  Options: (a) the junction computed inside a new gate class; (b) a
  standalone junction tool producing junction reports as records, with
  gate class V11 verifying their existence, vocabulary, and the
  relations around them; (c) no tool — junctions as a manual stage-record
  duty.
  *Recommendation: (b).* It is the Winning Combination pattern: producers
  produce, the gate verifies by its own copies and never originates
  analysis (the V8/V10 recompute-vs-produce split; gated_publish's
  separation). (a) would make the gate an author, against its standing
  discipline (C089-16). (c) is today's state — the tray-flake series
  shows what it costs.
- **D-089-3 — Quarantine and relations live in a per-store run index.**
  Options: (a) a flag edited onto the run record; (b) one global
  quarantine list for all stores; (c) a per-store run index carrying
  every relation a record cannot carry about itself: supersedes /
  superseded-by links, quarantine state with its junction and
  adjudication references, and legacy entries for pre-spec records.
  *Recommendation: (c).* (a) violates record immutability (C089-2).
  (b) splits relations from the store they describe and gives the gate
  no per-store census to check. The index is append-only in the same
  act-based style as the ledger's reclassifications: relations change
  by appended acts, never by editing a record.
- **D-089-4 — The comparability key's constitutive components (the
  judgment row).** run-key v1's components: surface; command/tool +
  version; code version (tree git SHA); input pins; seed; environment
  class. Options: (a) all components constitutive — two runs are
  comparable only if *everything* agrees, code included; (b) surface,
  command/tool, input pins, and seed are constitutive; code version
  and environment class are recorded and diffed but do not break
  comparability.
  *Recommendation: (b).* Under (a), the commonest real case — the same
  study rerun after a code fix, producing a different result — would
  never trigger a junction, because the code difference would make the
  pair "not comparable" by definition; the owner's rule would exempt
  exactly the divergences it exists to catch. Under (b), a code or
  environment difference is what a junction *explains with*, and an
  input-pin difference is what makes a pair a different experiment
  (C089-10). This row is a judgment, settled by the owner's package
  ratification (human-as-oracle), thereafter changeable only as a
  run-defs amendment.
- **D-089-5 — Reach-back over existing run records: index-only.**
  Options: (a) migration — rewrite existing records with minted ids and
  full keys; (b) index-only — existing records receive index entries
  under legacy ids derived from their store paths, with the key
  components recoverable from the record (for settling: semantics,
  candidate, pins) and the label `legacy — key partial` where components
  are unrecoverable (execution time, code version); bytes untouched;
  (c) no reach-back — the spec governs new runs only, and old results
  become simply unusable as evidence.
  *Recommendation: (b).* (a) rewrites records of record to add facts
  nobody recorded — fabrication in the service of hygiene. (c) strands
  the program's cited history (including the standing T405 canonicals'
  run records). Index-only keeps every old result citable under an
  honest label and gives V11 a complete census from day one.
- **D-089-6 — Suite runs: bind at citation, CI ids for CI, light
  records for local runs.** Options: (a) every suite execution, local
  or CI, mints a full run record; (b) only suite runs *cited as
  evidence* are bound — CI runs by GitHub run id + head SHA via the
  delivery-checker discipline, local evidence runs by a lightweight run
  record (command, tree SHA, input state, result summary, rewrite
  manifest + disposition) written by the citing stage's worker.
  *Recommendation: (b).* (a) duplicates what CI already mints and
  burdens every exploratory test run; the defect is not unrecorded
  executions but unbound *citations*. (b) binds exactly where results
  enter records of record.

## Requirements (summary; the claims in claims.md are the normative text)

- **FR-089-01 — Run identity on every named surface** (S1–S4; C089-1).
  Every result-bearing execution on the settling, experiment-job,
  study-re-execution, and cited-suite surfaces carries an
  execution-minted run id (D-089-1), including no-result executions,
  which produce a run record stating the absence.
- **FR-089-02 — Immutable records; labeled supersession** (S1–S2;
  C089-2). Run records are never edited or deleted by later runs; the
  settling store's content-addressed overwrite is retired;
  supersession is an index relation and superseded records remain
  addressable in the store.
- **FR-089-03 — Declared pooling only** (all stages; C089-3). Every
  aggregate over multiple runs names the runs pooled and the
  comparability basis; silent pooling is a defect withdrawn to per-run
  figures on discovery.
- **FR-089-04 — Citations name their run** (all stages; C089-4). An
  evidence number in a record of record names its run id + key, or
  carries the legacy label (FR-089-15).
- **FR-089-05 — Settling store discipline** (S2; C089-5). A settling
  run writes only its own record + index entry; the store census is
  monotonic; in-place regenerations (materialize-sets) become runs and
  their artifacts name the producing run.
- **FR-089-06 — Suite tree hygiene** (S4; C089-6). A cited suite run's
  record carries the rewrite manifest (regenerated paths + disposition)
  and tree state before/after; mid-run precondition destruction is
  reported not-run with cause, never passed.
- **FR-089-07 — Artifact producing-binding** (S2, S4; C089-7). An
  artifact read as current carries its producing run/build binding or
  the unbound label; unbound artifacts do not ground verdicts.
- **FR-089-08 — Experiment-job citation binding** (S4; C089-8).
  Repo-side citation records name job id + recorded inputs; results
  without them are unbound.
- **FR-089-09 — run-key v1 registered** (S1; C089-9, C089-10).
  Comparability is decided by the key's constitutive components
  (D-089-4) only; names never decide; constitutive differences are
  reported as different experiments with the component named.
- **FR-089-10 — Junction trigger before verdict use** (S3; C089-11).
  Comparable runs that differ in a verdict-bearing field, or where one
  side yields nothing, produce a junction report before either side's
  results are used for a verdict, gate, publication, or adjudication.
- **FR-089-11 — Junction report format** (S3; C089-12). Both run ids;
  component-by-component key diff; environment diff; first divergent
  output localized; exactly one disposition from the registered
  vocabulary (explained-by-named-difference / not-comparable /
  identical-after-all / unexplained).
- **FR-089-12 — Quarantine** (S3; C089-13). An unexplained junction
  quarantines both runs in the index; quarantined results are citable
  only as quarantined; lifting requires a recorded adjudication act.
- **FR-089-13 — Automatic production; red-team tier** (S3; C089-14).
  Junctions are produced by tooling at run completion and by store
  scan, not on request; unexplained dispositions gain the adversarial
  red-team section (input drift, code drift, environment drift,
  nondeterminism, record corruption, presentation artifact — each
  sustained or not, on evidence).
- **FR-089-14 — Gate class V11** (S5; C089-15, C089-16). The gate
  verifies run-binding with its own registered run-defs copies
  (producing-bindings resolvable; no quarantined citation as verdict
  support; census equality; links resolve; divergent pairs carry
  junction reports in the registered vocabulary) and never writes,
  adjudicates, or lifts.
- **FR-089-15 — Legacy index** (S5; C089-17). Every pre-spec run record
  receives an index entry under a legacy id with its recoverable key
  and the `legacy — key partial` label where components are
  unrecoverable; legacy bytes are never rewritten.
- **FR-089-16 — The ledger does not move** (all stages; C089-18).
  Beyond the adoption intake append, no stage writes to the ledger; no
  run kind is added to it.
- **FR-089-17 — Determinism classes registered per surface** (S1;
  C089-19). run-defs v1 registers each named surface's determinism
  class; deterministic surfaces treat any comparable difference as a
  junction by definition; named-nondeterministic surfaces register
  their known nondeterminism shapes (the tray-flake family first).
- **FR-089-18 — The delivery-protocol boundary is stated wherever the
  two defenses meet** (all stages; C089-20). Junction machinery never
  ingests deliveries; run records never certify presentations;
  record-vs-presentation disagreements route to the fabricated-delivery
  protocol, not to a junction.

## Governance

Claims first (this package's `claims.md` / `aee-claims.json`,
C089-1..20), assessed under the pinned AEE before any build task starts
(Stage 0, T002 — the assessment is in
`records/t002-aee-assessment.json`, its invocation and verbatim outcome
in `records/t002-note.md`). Verdicts and citations follow program
doctrine: numbers only from records read first-hand; assessments by
actually running the assessor; CI green or the work is not done. The
owner's block approval of this package (T003) is the ratification act
for the spec, run-defs v1's registered choices, and decisions
D-089-1..6 (including the comparability judgment row, D-089-4). The
spec ends with its closeout record (T601); no separate register
ratification applies — the junction dispositions and quarantine acts
the machinery produces are operational records under the ratified
defs, not owner acts, except where a junction's adjudication is itself
an owner gate (named per junction when it occurs).
