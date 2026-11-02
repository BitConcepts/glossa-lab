# Plan — Spec 087 Node-System Tightening (Stages S0–S6)

**Date**: 2026-11-02
**Package branch**: `feat/087-spec-package`
**Proposal basis**: the owner's directive of 2026-11-02
(~09:56 EST) and the system-coupling audit executed under it
the same day (`AUDIT.md` findings F1–F10 + the S1–S6
execution plan, `CENSUS.md`, live reads; goal workspace
`hidden_files/system-coupling-2026-11-02/`). This spec
implements that plan without silent alteration; the audit's
key tables are snapshotted at `records/census-evidence.md`.
In this repo's governance terms the approved package is the
proposal (H2); its §Decisions items stand as recommended
unless the owner rules otherwise at the approval act, and its
non-goals carry the epistemic boundaries (H13): no live
graph's behaviour changes, no verdict/claim-status changes,
the `_archive/` graphs untouched.

## Stage 0 — package adoption (this PR, records only)

1. **Package lands** (T001):
   `specs/087-node-system-tightening/` with spec.md, claims.md,
   tasks.md, plan.md, records/census-evidence.md, and the S5
   wireframes package under records/logs-view-wireframes/.
   No code changes; no existing file modified.
2. **Claims normalized** (T002): `aee-claims.json` carries
   C087-1…17, statement, falsifier, and does-not-establish
   text normalized from claims.md without substantive change.
   Pinned AEE 1.5.3 verification, run 2026-11-02 by the
   drafting worker in the CI-faithful venv:
   - `aee validate` → `valid: 17 claim(s) in specs/087-node-system-tightening/aee-claims.json`
   - `aee assess --no-ledger` → outcome `iterate`; summary:
     "Assessed 17 claim(s); found 73 failure mode(s); 17
     claim(s) below the 0.70 confidence threshold." (Draft
     claims with a single shared asserted evidence source —
     the expected well-formedness result, the same shape as
     Spec 086's T002; full output in
     `records/t002-aee-assessment.json`.)
3. **Freeze-gate (C4) check, run locally 2026-11-02**:
   `tools/freeze-gate/check_freeze_gate.py --all` exits 0.
   Spec 087 carries no `gate-records/` and no freeze records,
   so the C4 PR-scope selection does not select it; the C4
   job is unaffected by this package and by every stage
   (no stage touches a frozen record — claim C087-14).
4. **Approval gate**: the owner approves the package as a
   block. S5's build additionally waits for the owner's
   approval of records/logs-view-wireframes/ (decisions Q1,
   Q2 in that package).

## Dependencies

- **S1 before S2** (hard): S2's legacy flag and re-pin rest
  on S1's completeness test and the resolved shadowed
  definitions; curating over a registry that can still shrink
  silently would pin the wrong baseline.
- **S2 before S3** (hard): triage dispositions are recorded
  against the curated palette; disposition (b) re-expression
  targets the post-S2 primitive set.
- **S4 depends on S2's final palette set** (hard): the
  generator enumerates registry-minus-legacy; generating
  before curation would bake the wrapper set into the manual
  it exists to correct. S3 may land before or after S4; if S3
  lands after, its own PRs regenerate the reference and the
  conformance gate keeps the manual true in either order
  (C087-8, C087-15).
- **S5 independent** of S1–S4 (its own approval gate is the
  wireframes package); the events-bus documentation leg of
  S5 (D2) touches the same manual surfaces as S4 only if S4
  has landed — otherwise S5 updates them itself (C087-15
  decides by PR, not by stage order).
- **S6 independent, live-DB**: no repo dependency; it runs
  against the live desktop backend when scheduled, under the
  owner's 2026-11-02 authority. It is the only stage whose
  primary evidence is a stage record rather than a merge.

## Stage S1 — Registry integrity

**PR**: `feat/087-s1-registry-integrity` (one PR).
**Contents**: fail-fast registry build outside production
leniency (an environment-gated strict mode: production keeps
its warning, every other context raises); a completeness
test pinning the 144-module list and per-category counts
(517 total; 66 categories; counts of record in
records/census-evidence.md Table 1); the shadow resolution —
behaviour diff of the three pairs on their report fixtures,
the losing definitions deleted, a duplicate-id guard test;
the builder palette error state (catalog fetch failure
renders a named error, with retry); the `node_registry.py`
rename to `study_node_registry.py` (D5 sub-decision: one
importer, `main.py:75` + mount :456, plus tests and doc
references; the `/node-registry/` endpoint path unchanged);
manual notes for the rename (C087-15).
**Verification**: new backend tests — completeness pin,
seeded-broken-module teeth (the strict build fails),
duplicate-id teeth, both-registries-import test, endpoint
test for `/node-registry/`; frontend component test for the
palette error state. **CI jobs**: Backend tests (pytest),
Frontend tests (Playwright) for the component test; the
completeness test runs inside the Backend job — no new job.
**Claims**: C087-1, C087-2, C087-3, C087-16.

## Stage S2 — Palette curation

**PR**: `feat/087-s2-palette-curation` (one PR).
**Contents**: the `legacy` flag on `AtomicNodeDef` (default
false); the S2 migration setting it on exactly the census's
359 WRAPPER ids (the list is generated from the census
classification and committed as the migration's data, so the
act is reviewable id by id); the catalog endpoint filters
legacy by default and serves the full registry under
`?include_legacy=true`; the completeness test re-pinned
three ways (registered 517 / legacy 359 / palette 158) with
per-category counts; a resolution sweep test importing every
stored graph fixture and resolving every atomicId against
the full registry; the pinned comparison runs over the 27
live graphs executed pre- and post-change (C087-13 evidence,
filed in the stage record); manual update naming the legacy
namespace in the builder docs (C087-15).
**Verification**: backend tests — catalog filter (default
excludes every legacy id, includes every non-legacy id),
`include_legacy` completeness, resolution sweep, byte-compare
of comparison-run outputs. **CI jobs**: Backend tests; the
Indus public validation checks job (graph fixtures load
through the same registry paths). No frontend change beyond
the manual-level copy; if the builder UI gains a legacy
affordance it is out of this stage's scope by design.
**Claims**: C087-4, C087-5, C087-17, and the S2 leg of
C087-13.

## Stage S3 — Genericization triage

**PR shape**: a sequence, not one PR — a triage-record PR
first (`feat/087-s3-triage-record`: the 68 dispositions with
their evidence, no code), then conversion PRs grouped by
node family (`feat/087-s3-convert-<family>`), each carrying
its fixtures and output-equivalence proofs. The grouping is
set by the triage record, which is the stage's reviewable
contract; the parent gates the record before any conversion
PR opens.
**Contents**: the 7 live domain-flavoured ids plus the CGSA
core loaders first (records/census-evidence.md Table 2 note),
then the remaining PARTIAL set; disposition (a) conversions
move domain content into params (corpus, language, code
table, weights as data); disposition (b) re-expressions land
as graph edits in the consuming experiments with the
comparison runs re-proved; disposition (c) retentions file
the D3 bar's three legs per node. Any genuinely new
primitive a conversion needs is added through the registry
with the completeness pin updated in the same PR (C087-17).
**Verification**: per-node fixture equivalence (converted
node's outputs vs the original's on pinned fixtures,
byte-identical); a domain-branch lint test over converted
sources (no branch on a domain identity — C087-7's
falsifier, mechanized as far as a source scan honestly can,
with the residual named in the stage record); the C087-13
comparison runs after each conversion PR. **CI jobs**:
Backend tests; Indus public validation checks.
**Claims**: C087-6, C087-7, and the S3 leg of C087-13.

## Stage S4 — Generated manual

**PR**: `feat/087-s4-generated-manual` (one PR).
**Contents**: a generator tool (`tools/manual/generate_node_reference.py`,
following the tools/ledger precedent) that emits, from the
live registry: the delimited Node Reference block for
`docs/user-manual.md`, the HelpView node-reference data
module (`frontend/src/components/help/nodeReference.generated.ts`
or the path the build establishes), and the USER_GUIDE
active-experiments table from the graph files on disk; the
generated outputs committed; a conformance test in the
Spec 084 pattern (`backend/tests/test_manual_conformance.py`):
regenerate-and-diff in both directions, plus absence checks
naming the 10 phantom node names of census Table 3; prose
updates in the same PR — post-081 screens, the Logs panel
description rewritten to the S5/D2 disposition, the Study
Builder palette confusion (census §2.3) corrected, the
phantom example pipeline redrawn from real nodes.
**Verification**: the conformance test (Backend job), a
teeth check in the stage record (a seeded phantom name and a
seeded stale port each fail the test by name); frontend
build/tests over the generated data module (Frontend job).
**CI jobs**: Backend tests, Frontend tests. The generator
runs in CI only as the test's regeneration; no new job.
**Claims**: C087-8, C087-9.

## Stage S5 — Logs surface

**PR**: `feat/087-s5-logs-surface` (one PR), opening only
after the owner approves records/logs-view-wireframes/.
**Contents**: the Logs view per the approved wireframes
(placement and purge per decisions Q1/Q2 as ruled): a
`LogsView` component with the stream tab (getLog first load,
SSE tail via getLogStreamUrl, level filter, purge behind its
confirmation if Q2 rules (a)) and the records tab (jobs /
job_results / phase_actions / notification_log read through
the existing API surface, detail expansion, read-only); tab
registration in App.tsx per the Q1 ruling; the D2
events-bus leg — under the recommended ruling, the
documented-ephemeral statement lands in the events module
docstring, the user manual, and HelpView, with its pinning
test; manual updates in the same PR (C087-15).
**Verification**: frontend component tests (stream consumes
the wrappers; a failed log fetch renders an error state —
the F5 lesson applied from birth; records tab renders table
rows + expansion; purge reachable only through the
confirmation state if Q2(a)); Playwright renders of the
built surface at desktop 1440 + mobile 390 compared against
the approved wireframes, served identity asserted before
screenshots (the Spec 086 Stage 5 precedent); backend tests
unchanged except the events-doc pin. **CI jobs**: Frontend
tests, Backend tests.
**Claims**: C087-10, C087-11.

## Stage S6 — Anchor-set dedupe (live DB)

**PR**: none — this stage executes against the live system;
its deliverable is the stage record
(`stage-s6-record.md` in this spec) plus a records-only PR
landing it (`records/087-s6-stage-record`).
**Contents**: the grouping pass over all 104 live anchor sets
through the API (name, language, pairs content); the
duplicate groups and kept canonicals listed in the record
*before* any deletion; deletions by id through
`DELETE /anchor-sets/{id}` (the path verified to exist at
`backend/glossa_lab/api/anchor_sets.py:108` during drafting);
the post-pass census (sets remaining, distinct contents
before/after — the distinct count must not move).
**Verification**: before/after API reads: distinct-content
count identical, total count reduced by exactly the recorded
removals, every removed id present in the record with its
kept id; foundation check re-run after the pass (the F8
baseline surface). If the endpoint refuses in the live
environment, the stage stops and returns under D4's fallback
— it does not improvise a database path.
**Claims**: C087-12.

## Closeout

When S1–S6 land, the spec closes with a closeout record in
this directory: per-claim dispositions against the stage
records, the final registry census (registered / palette /
legacy counts), and the audit's six gap statements (F1–F10
dispositions) re-scored. The user manual's generated blocks
are the standing proof surface thereafter — drift between
the registry, the palette, and the manual is a CI failure,
not a finding waiting for the next audit.
