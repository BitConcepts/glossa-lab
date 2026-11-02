# Feature Specification: Node-System Tightening — One Registry, a Primitive Palette, a Generated Manual (Spec 087)

**Feature Branch**: `feat/087-spec-package` (this package);
build stages take their own branches per stage.
**Created**: 2026-11-02
**Status**: APPROVED AS A BLOCK by the owner on 2026-11-02
(~10:39 EST, option tap in the Glossa-Lab chat: "Approve
Spec 087 as a block, D1-D5 and Q1-Q2 as recommended"). The
decisions D1–D5 stand as this package recommends; the S5
wireframes package (records/logs-view-wireframes/ in this
spec) is approved in the same act, with Q1 (placement: own
tab) and Q2 (purge: ship with confirmation) ruled as
recommended. Claims frozen before code (spec-kit + AEE
flow). The approval act is recorded in full at
records/adoption-2026-11-02.md.
**Input**: The owner's directive of 2026-11-02 (~09:56 EST):
check all logs and fix them; verify the manual work is intact;
make sure all experiments are properly registered as graphs and
the graphs are perhaps updated; make the whole system tightly
coupled — remove, add, or update palette nodes as needed; make
everything generic enough that Indus-specific work uses
primitives to define, with no custom plugins unless a case
demands it, and where it does, make the custom plugin a generic
primitive with enough customizability; keep spec-kit + AEE and
the tests updated; keep the user manual updated as work
changes; perform an audit of that and of all features and
functions.
**Evidence of record**: the system-coupling audit of
2026-11-02 — `AUDIT.md` (findings F1–F10 and the execution
plan this spec implements) and `CENSUS.md` (repo census with
the 517-node classification as Appendix A), held in the goal
workspace at `hidden_files/system-coupling-2026-11-02/`, with
the live reads (`experiments-live.json`,
`live-atomic-census.json`) from the same folder. The key
tables are snapshotted into this spec at
`records/census-evidence.md`; findings are cited below as
F1–F10 and every number traces to that snapshot.
**Predecessors**: Spec 001 (as-built baseline), Spec 003 (MCP
+ route surface), Spec 026 (framework transfer; its builder
node was removed in Spec 086 Stage 4), Spec 081 (the current
UI shell; the removal that orphaned the log viewer), Spec 084
(the conformance-test pattern Stage S4 follows), Spec 086
(the generated-layer discipline — one source of truth,
generated downstream, a gate on drift — applied here to the
registry and the manual).

## Problem statement

The experiment node system grew without a governing spec
(F9): 87 spec directories exist and none has the node palette
or the plugin mechanism as its primary subject. What grew in
that vacuum is inventoried by the audit:

- **The registry is large, fragile, and mostly not
  primitives.** 517 node types are registered in
  `ATOMIC_NODES` (F1). 475 of them arrive from 144
  `experiment_graph_*.py` phase modules, each imported in a
  try/except that logs only a warning on failure — a failed
  module silently shrinks the registry and the palette, and
  nothing else notices. Of the 517, 90 are GENERIC and 427
  DOMAIN; of the DOMAIN set, **359 are wrappers** — no input
  ports, empty params schema, each running one frozen phase
  script or reading one fixed report file (F3). The node *is*
  the study; there is no parameter surface a user could build
  with. Only 68 DOMAIN nodes are PARTIAL — real ports/params
  with the domain choice fixed in code — and are the
  genericization candidates.
- **Definitions silently shadow each other.** Three node
  classes are defined in two modules each; the later import
  silently wins and the earlier definitions are dead (F2).
  Whether the pairs compute the same thing is undetermined.
- **The live working set proves the primitive model works —
  and that the sprawl is unused.** All 27 experiments are
  registered as graphs with zero dangling references (F4).
  Across 189 node instances they use exactly **36 distinct
  atomicIds**, mostly generic primitives; 481 registered node
  types are used by no live graph, and none of the 359
  wrappers is used by any live graph.
- **The palette cannot drift, but it can silently empty.**
  The Experiment Builder fetches the registry live
  (`GET /experiment-graphs/catalog`), so palette and registry
  are one set by construction (F5) — but the fetch's failure
  handler swallows the error, rendering a silently empty
  palette indistinguishable from "no nodes exist".
  Separately, `node_registry.py` — the Study Builder's
  param-schema module — carries a name that collides with the
  experiment node registry it is not.
- **The logs work; the log viewer is gone.** Backend JSON
  logging, DB job/phase/notification records, and the cloud
  append-only audit log are all live (F6). The terminal-log
  endpoints (`/terminal/log`, `/terminal/stream`, `/purge`)
  are write-only in the current UI: the `api.ts` wrappers
  exist, no component references them since Spec 081 removed
  the bottom panel, and the manuals still describe a Logs
  panel. The events bus is in-memory only, never persisted,
  and that fact is documented nowhere as a decision.
- **The manuals describe a product that no longer exists.**
  The user-manual Node Reference lists 21 node names, **10 of
  which do not exist in the registry** (F7); the 11 real ones
  are 2.1% of the palette. HelpView's "Complete Node
  Reference" documents the same stale set. USER_GUIDE lists 8
  active graph experiments against 27 on disk. The manuals
  describe the pre-phase-module, pre-Spec-081 product.
- **The manual work is intact** (F8) — discovery triage,
  anchor sets, jobs, reports, and the foundation check are
  all present in the live database — with one named hygiene
  item: the 104 anchor sets are heavily duplicated (many
  identical "Fuls 6" copies and placeholder sets from the
  Oct 5–9 early-use period). The feature inventory (F10)
  found no other orphan surfaces: 53 routers / 321 routes,
  24 frontend screens, 33 MCP tools, the CLI families.

## Scope — stages S1–S6

The scope is exactly the audit plan's six stages. Stage order
and dependencies are in plan.md; claims are in claims.md /
`aee-claims.json` (C087-1…C087-17).

- **S1 — Registry integrity.** Fail-fast module imports
  outside production leniency: a CI registry-completeness
  test pins the plugin module list and the registered count
  by category, so a silent shrink fails CI. The 3 shadowed
  classes are resolved — the correct definition determined by
  diffing behaviour, the dead one deleted, a test pins one
  definition per id. The builder's palette load failure
  surfaces as an error state, never a silently empty palette.
  Includes the `node_registry.py` disposition (decision D5).
- **S2 — Palette curation.** The 359 wrapper nodes leave the
  palette under decision D1's mechanism: they stay resolvable
  for stored graphs but are no longer offered as buildable
  primitives. The palette becomes the primitive set — GENERIC
  nodes + parameterized PARTIAL nodes + the live working set.
  Registry count and category census re-pinned by test.
- **S3 — Genericization.** The 68 PARTIAL domain nodes are
  triaged under decision D3's bar, each to exactly one
  disposition: (a) converted to a generic primitive whose
  params carry the domain specifics; (b) re-expressed as a
  composition of existing primitives in the experiments that
  use it; or (c) retained as a domain primitive with a
  recorded reason that passes the bar, gaining the parameters
  that make it reusable. The domain-flavoured ids in live use
  (the audit's seven, plus the CGSA core loaders the census
  classes DOMAIN — records/census-evidence.md Table 2 note)
  are triaged first. Any surviving custom plugin follows the
  same rule: generic mechanism, domain content in parameters.
- **S4 — Generated manual.** The node reference in
  `docs/user-manual.md` and in HelpView is generated from the
  registry (one source of truth, the ledger→matrix→map
  discipline of Spec 086): a generator tool plus a CI
  conformance check in the Spec 084 pattern — the manual
  lists exactly the palette set, with each node's
  ports/params. USER_GUIDE's experiment list is generated the
  same way. Manual prose sections are updated for the
  post-081 screens and the F6 logs disposition. Generation
  scope per surface is decision D5.
- **S5 — Logs surface.** A Logs view is restored for the
  terminal-log endpoints and the DB record tables, built to
  the wireframes package in this spec
  (`records/logs-view-wireframes/`) after the owner's
  approval of that package — the one approval point in this
  program besides the spec package itself. The events-bus
  disposition is decided at D2 and implemented or documented
  in this stage.
- **S6 — Anchor-set dedupe (live DB).** Exact-duplicate
  removal only: group by (name, language, pairs content);
  keep the earliest canonical copy of each distinct content;
  record every removed id in the stage record. No distinct
  content is deleted. Execution path per decision D4. The
  owner's "fix them" directive of 2026-11-02 is the
  authority; the stage record is the proof.

## Non-goals

- **No change to any live graph's behaviour.** The 27 graphs'
  node instances, parameters, and results are untouched by
  every stage; S2/S3 must prove byte-identical results on the
  pinned comparison runs (claim C087-13). A stage that cannot
  prove this stops and reports; it does not adjust a graph to
  fit.
- **No verdict or claim-status changes.** This program moves
  no Indus claim's status, stage, or score, writes no ledger
  entry, and touches no frozen record. The freeze-gate (C4)
  regime is unaffected: this spec carries no `gate-records/`
  and no freeze records.
- **The `_archive/` graphs are untouched** — 130 archived
  graph JSONs stay exactly as they are; their resolvability
  is neither required nor broken deliberately.
- **No new plugin mechanism.** Atomic nodes remain
  compiled-in modules registered through `ATOMIC_NODES`
  (census §3); S1 pins and guards that mechanism, it does not
  replace it with entry-points discovery. Pipelines and
  ExperimentBase classes already have true plugin systems and
  are out of scope.
- **No study-graph editor work.** The Study Builder's surface
  questions (census open question 3) are not in scope; only
  its module's naming collision is (D5).
- **No data-lineage adjudication.** The Oct 30 VM snapshot
  divergence (F8 caveat) is a standing open question this
  program does not touch.

## Decisions

Each decision states the options and a marked recommendation.
The owner rules on the package as a block; a decision the
owner rules against is recorded as ruled, with the ruling, in
the stage record of the stage that implements it.

### D1 — Wrapper retirement mechanism (S2)

*The question.* By what mechanism do the 359 wrapper nodes
leave the palette while staying resolvable?

**Options.**

- **(a) Registry-level legacy flag (RECOMMENDED).** Each
  wrapper's `AtomicNodeDef` gains `legacy: true` (set at its
  registration site by the S2 migration, from the census's
  WRAPPER classification). `ATOMIC_NODES` keeps all 517
  entries and stays the one resolution table — stored graphs,
  the experiment ledger metadata, and `SubExperiment`
  resolution all keep working unchanged. The catalog endpoint
  filters `legacy` out of the palette response by default;
  the full registry remains available to the resolver and to
  an explicit `?include_legacy=true` catalog read for
  diagnostics. The S2 census test re-pins counts three ways:
  registered (517), palette (registered minus legacy), legacy
  (359).
- **(b) A separate legacy registry.** Wrappers move to a
  second dict; resolvers consult both. Rejected: every
  resolution path (graph loader, metadata merge, catalog,
  SubExperiment, tests) grows a union lookup, and the two
  tables can drift — the exact failure class this program
  exists to remove (F5's one good property, palette ==
  registry by construction, is weakened to palette == a
  join).
- **(c) Deletion.** Wrappers are deleted outright. Rejected:
  stored graphs outside the live 27 — user graphs in the
  live database, the experiment ledger's 68 metadata entries,
  any graph JSON not in the repo — may reference wrapper ids;
  deletion turns those into dangling references, the failure
  F4 verified absent today. It is also irreversible without
  git archaeology per node.

**Recommendation: (a).** The argument is F3 + F4 together:
the wrappers carry no parameter surface, so nothing is lost
by removing them from the *offer*; and the live working set
uses none of them, so nothing live changes when the palette
shrinks. What must not break is *resolution*, and (a) is the
only option that changes exactly one thing (the catalog
filter) while leaving the one resolution table intact. The
flag lives on the definition, so the census test can count
legacy nodes from the same source the catalog filters —
palette == registry-minus-legacy becomes a mechanical
identity (claim C087-4), not a maintained list.

### D2 — Events-bus disposition (S5)

*The question.* The events bus (`api/events.py`) is in-memory
pub/sub over SSE: events emitted with no live subscriber are
lost, and slow subscribers drop messages. Persist it, or
document it as ephemeral?

**Options.**

- **(a) Documented-ephemeral (RECOMMENDED).** The bus is
  declared, in the module docstring, the user manual, and
  HelpView, as a live-notification channel with no delivery
  guarantee: anything that must survive is already recorded
  in the durable surfaces (jobs/job_results, phase_actions,
  notification_log, the cloud audit log). A test pins the
  declaration's presence so the fact cannot silently
  un-document itself.
- **(b) Persist events.** A new table, a retention rule, and
  a read surface. Rejected for this program: it builds a
  second, weaker audit trail beside the four durable record
  surfaces that already exist, its drop-on-`QueueFull`
  semantics cannot honour a persistence promise without a
  redesign of the emit path (backpressure into job execution
  — a behaviour change to running experiments, outside this
  program's non-goals), and no finding names a lost event
  that mattered: every F6/F10 record a user needs is already
  in a durable table.

**Recommendation: (a).** The defect in F6 is not that events
are ephemeral — it is that the ephemerality is an accident
nobody decided. (a) makes it a decision, stated in exactly
the places a user or a maintainer would look, with the
durable alternatives named. Claim C087-11 is written
disposition-neutrally (the statement exists in one documented
place and the code matches it) so the claim survives either
ruling; if the owner rules (b), S5's plan gains the
persistence build and this spec is amended before S5 starts.

### D3 — The S3 triage bar: what counts as "a case that demands" a domain node (S3)

*The question.* S3 disposition (c) lets a node stay
domain-specific "with a recorded reason (a case that demands
it)". Without a falsifiable bar, (c) becomes the path of
least resistance and the triage ratifies the status quo.

**The bar (RECOMMENDED).** A PARTIAL node may be retained as
a domain primitive only if its triage record demonstrates
**all three** legs, each with evidence filed in the stage
record:

1. **Non-composability, demonstrated — not asserted.** A
   recorded attempt expresses the node as a composition of
   existing primitives plus parameter data (corpus, language,
   code table, weights) and runs it against the node's own
   pinned fixtures. The attempt must fail output-equivalence,
   and the failure must be *structural* — it names a mechanism
   the primitive set lacks — not a matter of effort or
   convenience. If the composition matches on the fixtures,
   the node takes disposition (a) or (b); the bar is not met.
2. **Parameter reality.** The node has, or gains in S3, a
   real parameter surface: at least one meaningful parameter
   or input port through which a second caller could vary
   its behaviour. A node with no ports and no params is a
   wrapper by definition (F3) and belongs to S2's legacy set,
   never to (c).
3. **Independent demand.** At least two distinct consumers —
   live graphs, registered experiments, or a registered
   claim/study naming the mechanism as its subject — need
   this mechanism, not merely this study's frozen instance of
   it. A node exactly one study uses is that study's wrapper
   wearing a PARTIAL classification.

A retained node's record cites: the composition attempt and
its fixture diff (leg 1), the parameter/port list (leg 2),
and the demand instances (leg 3). A record missing any leg
fails the stage gate — the node is re-triaged, not waved
through. The same bar applies to any *new* custom plugin
proposed after S3: generic mechanism, domain content in
parameters, or a triage record that passes all three legs.

*This bar does not establish* that a retained node is
well-designed — only that its domain specificity is a
demonstrated necessity with a reuse surface, which is the
property the owner's directive asks for.

### D4 — S6 dedupe execution path (S6)

*The fact, checked during drafting (2026-11-02).* An API
delete path exists: `DELETE /anchor-sets/{anchor_set_id}` is
implemented at `backend/glossa_lab/api/anchor_sets.py:108`
(returns `{"deleted": true, "id": …}`; backed by
`db.delete_anchor_set`), alongside GET/POST/PUT on the same
router.

**Decision (RECOMMENDED, on that fact).** S6 executes through
the API surface: each confirmed exact duplicate is deleted by
its id through the authenticated API against the live desktop
backend (the same surface the MCP `list_anchor_sets` /
`get_anchor_set` tools read), never by direct database
writes. The grouping pass reads every set's (name, language,
pairs content) through the API first; the earliest canonical
copy of each distinct content is kept; every deleted id,
with its group's canonical id, is recorded in the stage
record before the stage is reported. Fallback, only if the
endpoint refuses in the live environment (for example a
cloud-scope restriction): stop, record the refusal, and
bring the named procedure back for the owner's ruling —
S6 does not improvise a direct-DB path on its own authority.

### D5 — Manual generation scope; and the `node_registry.py` sub-decision (S4, S1)

*Generation scope (RECOMMENDED).* Generate exactly the
enumerable, drift-prone content; keep everything else prose:

- **Generated:** the Node Reference section of
  `docs/user-manual.md` (a delimited generated block listing
  exactly the palette set — post-S2, registry-minus-legacy —
  with each node's category, ports, and params); the node
  reference data rendered by HelpView (a generated data
  module the component renders, so the in-app reference and
  the markdown reference are one generation, not two); and
  the active-experiments table in `docs/USER_GUIDE.md`
  (generated from the graph files on disk: the 27, not 8).
- **Conformance:** the Spec 084 pattern — a generator tool, a
  committed generated output, and a CI test that regenerates
  and diffs (drift in either direction fails the Backend job)
  plus absence checks for the 10 phantom names of census
  Table 3: a manual that names a nonexistent node fails CI
  by name.
- **Stays prose:** all narrative sections (concepts,
  walkthroughs, troubleshooting, interpretation). S4 updates
  the prose where the audit shows it false — the post-081
  screens, the Logs panel description (rewritten to the S5
  disposition), the Study Builder palette confusion (census
  §2.3) — as ordinary reviewed edits in the S4 PR, outside
  the generated blocks. Generated blocks are delimited and
  the generator refuses to write outside them.

*The `node_registry.py` sub-decision (S1) (RECOMMENDED:
rename).* The module is the Study Builder's param-schema
lookup (`_BUILTIN_SCHEMAS`; endpoint
`GET /node-registry/{node_type}/{ref_id}`), not the
experiment node registry (census §1.1). Options: **(a)
rename** the module to `study_node_registry.py` — the blast
radius is one importer (`backend/glossa_lab/main.py:75`, the
router mount at :456), its own tests, and doc references;
the endpoint path is unchanged, so no client breaks;
**(b) document-only** — a header comment and a docs note,
leaving the collision in place for the next reader.
Recommendation: **(a)** — the collision is a standing
invitation to edit the wrong file (it misdirected this
audit's own census pass before the census corrected itself),
the cost is one import line, and S1 is the stage whose whole
subject is registry integrity. The rename lands in S1 with a
test that both registries import and the endpoint still
answers.

## Requirements (summary; the claims carry the contract)

- **FR-087-01** — Registry completeness is pinned in CI:
  module list, per-category counts, one definition per id.
  (S1; C087-1, C087-2)
- **FR-087-02** — Palette load failure is a visible error
  state in the builder. (S1; C087-3)
- **FR-087-03** — The palette is the primitive set:
  registry-minus-legacy, mechanically. Stored graphs still
  resolve every id. (S2; C087-4, C087-5)
- **FR-087-04** — Every PARTIAL domain node carries exactly
  one evidenced triage disposition; retained nodes pass the
  D3 bar on the record. (S3; C087-6, C087-7)
- **FR-087-05** — The manual node reference and the
  experiment list are generated and CI-conformant; no manual
  names a nonexistent node. (S4; C087-8, C087-9)
- **FR-087-06** — The Logs view is restored to the approved
  wireframes; the events-bus disposition is stated once and
  true. (S5; C087-10, C087-11)
- **FR-087-07** — Anchor-set dedupe removes exact duplicates
  only, through the API, with every removed id recorded.
  (S6; C087-12)
- **FR-087-08** — Cross-cutting: every live graph still
  resolves and runs with byte-identical results; no verdict,
  claim status, or ledger content changes; the manual updates
  land with the stage that changes the behaviour.
  (C087-13, C087-14, C087-15)

## Governance

Spec-kit + AEE flow, as Specs 084/086: claims frozen in this
package before code; every stage its own PR; full CI green
(all jobs, including C4 and the ledger/matrix/map equivalence
gate) before merge; branch and worktree/clone removed in the
merge motion; the user manual updated in the same PR as the
stage that changes the behaviour (C087-15). Stage reports
carry their gate/test output verbatim. The standing position
is untouched by this program: the Indus script is not
deciphered, and nothing in any stage's output may be read as
changing that — the node system is the tool, not the result.
