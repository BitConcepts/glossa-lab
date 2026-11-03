# Tasks: Node-System Tightening (Spec 087)

Stages run under plan.md's dependency order: S1 before S2,
S2 before S3, S4 after S2's final palette set, S5 independent
(behind its wireframe approval), S6 independent (live DB).
Every task names its claim(s), its acceptance mode (**test** =
automated check decides; **human-as-oracle** = the owner or a
named human judges; **gate** = a recorded approval act must
exist first), and a *this does not establish* line that
survives into the stage report verbatim. **Every stage report
carries its gate/test output verbatim** — not a summary of it.

## Stage 0 — package adoption (PR: `feat/087-spec-package`)

- [x] T001 Spec package lands in
  `specs/087-node-system-tightening/`: spec.md, claims.md,
  tasks.md, plan.md, records/census-evidence.md, and the S5
  wireframes package under records/logs-view-wireframes/.
  Acceptance: test (documents present, internally consistent,
  records-only diff). *This does not establish that any part
  of the design is built or correct — only that the contract
  exists in the repo.*
- [x] T002 Claims normalized into `aee-claims.json`
  (C087-1…17) and verified under the pinned AEE (`aee
  validate` + `aee assess --no-ledger`), output recorded in
  plan.md and `records/t002-aee-assessment.json`. Acceptance:
  test. *This does not establish that the claims are true —
  only that they are well-formed and carry falsifiers.*
- [x] T003 Owner block approval of the package recorded at
  the head of spec.md (approval act, date, and any decision
  ruled against its recommendation). Acceptance: gate.
  *This does not establish that the design is right — only
  that the owner adopted it as the contract.*

## Stage S1 — Registry integrity (PR: `feat/087-s1-registry-integrity`)

- [x] T101 Fail-fast registry build: an environment-gated
  strict mode in the plugin import path (production keeps
  the warning; strict contexts raise). (C087-1) Acceptance:
  test — a seeded broken module fails the strict build
  loudly; the lenient build still registers the rest.
  *This does not establish that production should run strict
  — only that CI can no longer pass over a shrink.*
- [x] T102 Registry-completeness test: pins the 144 module
  names, the registered total (517), and per-category counts
  from records/census-evidence.md Table 1. (C087-1, C087-17)
  Acceptance: test. *This does not establish the counts are
  right — only that they are pinned and any change is an act.*
- [x] T103 Shadow resolution: behaviour-diff the three
  shadowed pairs (census Table 4) on their report fixtures;
  record the diff and the kept definition per pair; delete
  the three dead definitions; add the duplicate-id guard
  test. (C087-2) Acceptance: test + human-as-oracle (the
  behaviour-diff record is the evidence a reviewer judges).
  *This does not establish the kept definitions are
  scientifically right — only that one definition per id
  survives, chosen on recorded behaviour.*
- [x] T104 Palette failure surface: the builder renders a
  named error state (with retry) when the catalog fetch
  fails. (C087-3) Acceptance: test (component test with a
  failing fetch). *This does not establish endpoint
  reliability — only that failure is visible.*
- [x] T105 `node_registry.py` renamed to
  `study_node_registry.py` (importer `main.py`, tests, doc
  references); `/node-registry/` endpoint path unchanged;
  both-registries import test. (C087-16) Acceptance: test.
  *This does not establish the two systems should merge —
  only that they stop sharing a name.*
- [x] T106 S1 stage record: gate/test output verbatim
  (completeness pin, teeth runs, the shadow behaviour diffs),
  manual changes named. Acceptance: test (record present,
  outputs verbatim). *This does not establish S1's design
  choices were optimal — only that its evidence is on file.*

## Stage S2 — Palette curation (PR: `feat/087-s2-palette-curation`)

- [ ] T201 `legacy` flag on `AtomicNodeDef` + the S2
  migration data file listing exactly the census's 359
  WRAPPER ids, generated from the classification and
  reviewable id by id. (C087-4) Acceptance: test (migration
  set == census WRAPPER set, counted both ways). *This does
  not establish any single node's classification is beyond
  argument — only that the set applied is the census's set,
  named.*
- [ ] T202 Catalog filtering: default response excludes
  legacy; `?include_legacy=true` returns the full registry.
  (C087-4, C087-5) Acceptance: test (filter + completeness,
  both directions). *This does not establish the builder UI
  needs no other change — only that the API contract is the
  mechanical identity the claim states.*
- [ ] T203 Resolution sweep: every stored graph fixture
  resolves every atomicId against the full registry.
  (C087-5) Acceptance: test. *This does not establish the
  graphs run correctly — only that nothing dangles.*
- [ ] T204 Pinned comparison runs over the 27 live graphs,
  pre-change outputs already on file from the audit baseline
  (or re-pinned at stage start with the act recorded);
  post-change outputs byte-compared. (C087-13) Acceptance:
  test. *This does not establish the outputs are correct —
  only that S2 did not change them.*
- [ ] T205 Completeness test re-pinned three ways
  (registered 517 / legacy 359 / palette 158, per-category).
  (C087-17) Acceptance: test. *This does not establish the
  registry will not change again — only that its next change
  is equally visible.*
- [ ] T206 S2 stage record: the migration id list, the
  re-pin diff, comparison-run output verbatim, manual
  changes named. Acceptance: test. *This does not establish
  curation was the right call — only that it happened as
  specified.*

## Stage S3 — Genericization triage (PRs: `feat/087-s3-triage-record`, then `feat/087-s3-convert-<family>`…)

- [ ] T301 Triage record: all 68 PARTIAL nodes dispositioned
  exactly once ((a)/(b)/(c)) with per-disposition evidence;
  live domain-flavoured ids and the CGSA core loaders first.
  (C087-6) Acceptance: gate (parent/owner reviews the record
  before conversion PRs open) + test (a completeness check
  over the 68: exactly one disposition each). *This does not
  establish the dispositions are optimal — only that each is
  singular and evidenced.*
- [ ] T302 Retention files for disposition (c): per node, the
  D3 bar's three legs — the composition attempt with its
  fixture diff, the parameter/port list, the demand
  instances. (C087-6) Acceptance: human-as-oracle on the
  filed evidence; a missing leg re-triages the node.
  *This does not establish a retained node is well-designed —
  only that its domain specificity is demonstrated necessity.*
- [ ] T303 Conversion PRs (disposition (a)): domain content
  moved to params/ports; per-node fixture equivalence,
  byte-identical, against the original node. (C087-7)
  Acceptance: test. *This does not establish the primitive is
  complete — only that the replaced behaviours reproduce.*
- [ ] T304 Re-expression PRs (disposition (b)): consuming
  experiments rebuilt as compositions of existing
  primitives; C087-13 comparison runs re-proved per PR.
  Acceptance: test. *This does not establish the composition
  is the best expression — only that the domain node is no
  longer load-bearing.*
- [ ] T305 Domain-branch scan over converted sources + the
  S3 leg of the comparison runs; S3 stage record with the
  full 68-row disposition table. (C087-7, C087-13)
  Acceptance: test (scan clean or its residual named in the
  record). *This does not establish no domain logic remains
  anywhere — only that the converted set carries none in code.*

## Stage S4 — Generated manual (PR: `feat/087-s4-generated-manual`)

- [ ] T401 Generator tool (`tools/manual/`): emits the
  user-manual Node Reference block, the HelpView
  node-reference data module, and the USER_GUIDE experiments
  table, from the live registry and the graph files;
  refuses to write outside its delimited blocks. (C087-8,
  C087-9) Acceptance: test (delete-and-regenerate is
  byte-identical). *This does not establish the generated
  content is readable — only that it is the registry's truth,
  regenerated.*
- [ ] T402 Conformance test (Spec 084 pattern):
  regenerate-and-diff both directions + absence checks for
  the 10 phantom names; teeth seeded in the stage record.
  (C087-8, C087-9) Acceptance: test. *This does not establish
  the prose around the blocks is true — only the enumerable
  reference is pinned.*
- [ ] T403 Prose pass in the same PR: post-081 screens, the
  Logs description rewritten to the S5/D2 disposition, the
  Study Builder palette confusion corrected, the phantom
  example pipeline redrawn from real nodes. (C087-15)
  Acceptance: human-as-oracle (reviewed diff). *This does
  not establish the prose is finished forever — only that it
  is true at this merge.*
- [ ] T404 S4 stage record: generator + conformance output
  verbatim, teeth results, the before/after phantom census.
  Acceptance: test. *This does not establish the manuals are
  complete — only that their enumerable claims are now
  machine-kept.*

## Stage S5 — Logs surface (PR: `feat/087-s5-logs-surface`)

- [ ] T501 Wireframe approval gate: the owner approves
  records/logs-view-wireframes/ by name, ruling Q1
  (placement) and Q2 (purge). No S5 build task starts before
  this act. Acceptance: gate. *This does not establish the
  built surface will match — only that the target is fixed.*
- [ ] T502 LogsView build: stream tab (getLog first load,
  SSE tail, level filter, purge behind its confirmation if
  Q2 rules (a)) + records tab (four record tables, detail
  expansion, read-only), placed per Q1's ruling; a failed
  fetch renders an error state. (C087-10) Acceptance: test
  (component tests per plan.md). *This does not establish
  the endpoints scale — only that the surface exists as
  approved.*
- [ ] T503 Events-bus leg: the D2 disposition as ruled —
  under (a), the documented-ephemeral statement in the
  module docstring, user-manual, and HelpView + its pinning
  test; under (b), the persistence build the amended plan
  specifies. (C087-11) Acceptance: test. *This does not
  establish the disposition is ideal — only that it is
  decided, stated, and true.*
- [ ] T504 Playwright verification: built surface rendered
  at 1440 + 390 against the approved wireframes, served
  identity asserted first; differences named, data governs.
  (C087-10) Acceptance: test. *This does not establish the
  cloud surface — only the desktop surface the wireframes
  draw.*
- [ ] T505 S5 stage record: Q1/Q2 rulings as built,
  comparison output, manual changes named. Acceptance:
  test. *This does not establish the surface will not evolve
  — only that this restore landed as approved.*

## Stage S6 — Anchor-set dedupe (live DB; record PR: `records/087-s6-stage-record`)

- [ ] T601 Grouping pass: all live anchor sets read through
  the API; groups by (name, language, pairs content); the
  duplicate groups and kept canonicals (earliest per
  content) listed in the stage record before any deletion.
  (C087-12) Acceptance: human-as-oracle (the group list is
  reviewed before execution). *This does not establish the
  kept sets are good — only that the grouping is exact.*
- [ ] T602 Deletions by id through
  `DELETE /anchor-sets/{id}` only; any refusal stops the
  stage under D4's fallback. (C087-12) Acceptance: test
  (API responses on file per id). *This does not establish
  the endpoint is the only safe path — only that it is the
  path this stage is authorized to use.*
- [ ] T603 Post-pass verification: distinct-content count
  unchanged; total reduced by exactly the recorded removals;
  foundation check re-run; stage record completed with every
  removed id and its kept id. (C087-12) Acceptance: test.
  *This does not establish the surviving sets are curated —
  only that no distinct content was lost.*

## Closeout

- [ ] T701 Closeout record: per-claim dispositions against
  the stage records; the final registry census (registered /
  palette / legacy); F1–F10 re-scored. (All claims)
  Acceptance: human-as-oracle. *This does not establish the
  system is finished — only that this program's contract is
  discharged on its evidence.*
