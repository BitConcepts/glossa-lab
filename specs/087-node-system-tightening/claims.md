# Claims — Spec 087 (C087-1 … C087-17)

Every claim carries at least one falsifier executable against
the built system and a "this does not establish" line. This
list is normalized into the spec bundle's `aee-claims.json` in
the repo's established format and validated under the pinned
AEE (1.5.3) before any build task starts (tasks.md T002).
Claims are grouped by stage; C087-13…C087-15 are cross-cutting
and bind every stage.

---

**C087-1 — Registry completeness is pinned, and a silent
shrink fails CI.**
A CI registry-completeness test pins the plugin module list
(all 144 `experiment_graph_*.py` modules) and the registered
node count by category; outside production leniency, a plugin
module that fails to import fails the test loudly instead of
shrinking the registry behind a log warning.
*Falsifier:* a seeded broken plugin module (import error in a
fixture copy of the registry build) under which the suite
still passes; or a registered count by category in the running
system that differs from the pinned count while CI is green.
*Does not establish:* that the pinned counts are the right
counts — only that any change to them is a visible, recorded
act rather than an accident.

**C087-2 — No node id has two live definitions.**
Exactly one definition of each node id is reachable in the
built registry; the three shadowed classes of census Table 4
(`IndusPhase254SemanticConstraint`,
`IndusPhase255CommodityPhonemes`, `IndusPhase256LEExtension`)
are resolved to the behaviour-verified definition, the dead
definition is deleted, and a duplicate-id registration in a
test fixture fails the suite.
*Falsifier:* two importable definitions of one id in the
tree; a fixture registering an already-registered id that the
suite accepts; or fixture outputs showing the deleted
definition's behaviour where the kept definition's was
recorded as correct.
*Does not establish:* that the kept definition computes the
right science — only that there is one of it, chosen by a
recorded behaviour diff, where before there were two and the
choice was an import order.

**C087-3 — A failed palette load is visible, never a silent
empty.**
When the Experiment Builder's catalog fetch fails, the
builder renders an error state that names the failure; it
never renders an empty palette indistinguishable from "no
nodes exist".
*Falsifier:* a component test (or manual run) with the
catalog endpoint failing in which the builder shows an empty
palette with no error surface.
*Does not establish:* that the catalog endpoint is reliable —
only that its failure can no longer masquerade as an empty
registry.

**C087-4 — The palette is the registry minus legacy,
mechanically.**
The catalog endpoint's default response contains exactly the
registered nodes not flagged legacy: GENERIC nodes,
parameterized PARTIAL nodes, and the live working set. The
palette set is computed from the registry and the flag, never
maintained as a separate list.
*Falsifier:* a node in the default catalog response that is
flagged legacy; a non-legacy registered node missing from
it; or a palette-only id that exists in no registry.
*Does not establish:* that the legacy classification of any
individual node is correct — the classification of record is
the census's, and reclassifying a node is a recorded stage
act, not a consequence of this claim.

**C087-5 — Legacy nodes stay resolvable; nothing stored
dangles.**
Every node id resolvable before Stage S2 remains resolvable
after it, through the same `ATOMIC_NODES` table; the full
registry (including legacy) is what graph loading, the
metadata merge, and resolution consult.
*Falsifier:* a stored graph, ledger metadata entry, or test
fixture referencing a wrapper id that resolved before S2 and
fails to resolve after it.
*Does not establish:* that legacy nodes produce current or
correct results — only that history stays loadable. The
`_archive/` graphs are outside this claim (spec non-goals).

**C087-6 — Every PARTIAL domain node is triaged exactly
once, on evidence.**
Each of the 68 PARTIAL domain nodes of the census carries
exactly one Stage S3 disposition — (a) converted to a generic
primitive, (b) re-expressed as a composition of primitives in
its consuming experiments, or (c) retained under the D3 bar —
recorded in the triage record with its evidence; the
domain-flavoured ids in live use are triaged first.
*Falsifier:* a PARTIAL node with no disposition, with two,
or whose disposition record lacks the evidence its class
requires (for (c), any of the bar's three legs).
*Does not establish:* that the dispositions are the best
possible — only that each one exists, is singular, and is
backed by the evidence its class demands.

**C087-7 — A converted node carries its domain content in
parameters, not in code.**
For every node converted under disposition (a), the domain
specifics (corpus, language, code table, weights) arrive as
parameter or port data; the node's code contains no branch on
a domain identity (a named language, corpus, scholar map, or
sign list).
*Falsifier:* a converted node whose source still branches on
a domain identity; or two parameter settings of a converted
node that cannot reproduce the behaviours of the domain
variants it replaced, on their pinned fixtures.
*Does not establish:* that the primitive is elegant or
complete — only that the domain content moved from code to
data, which is the coupling property the owner directed.

**C087-8 — The manual's node reference is the palette set,
mechanically.**
The generated node reference (user-manual block and the
HelpView data module) lists exactly the palette set of claim
C087-4, with each node's category, ports, and params as the
registry states them; the CI conformance test of Stage S4
regenerates and diffs, failing on drift in either direction.
*Falsifier:* a node in the manual reference that is not in
the palette set; a palette node missing from it; a port or
param in the manual that differs from the registry's; or a
hand edit inside a generated block that CI accepts.
*Does not establish:* that the surrounding prose is clear or
complete — the claim covers the enumerable reference, the
part that was mechanically false.

**C087-9 — No manual names a node or experiment that does
not exist.**
No manual surface (user-manual, USER_GUIDE, HelpView) names
any of the 10 phantom node names of census Table 3, enforced
by absence checks in the same CI conformance test; and
USER_GUIDE's active-experiments list is generated from the
graph files on disk (27 today), neither more nor fewer.
*Falsifier:* any of the 10 phantom names appearing in a
manual surface while CI is green; or a generated experiment
list whose count differs from the graph files on disk.
*Does not establish:* that the manuals are well written —
only that their enumerable claims about what exists are true.

**C087-10 — The Logs view is restored, to the approved
wireframes.**
The app carries a Logs surface with the two tabs of the
owner-approved S5 wireframes package: a live stream tab
consuming `GET /terminal/log` and `GET /terminal/log/stream`,
and a records tab reading the `jobs`/`job_results`,
`phase_actions`, and `notification_log` tables, read-only,
with per-record detail expansion. The build matches the
approved wireframes screen by screen under Playwright
verification.
*Falsifier:* a shipped Logs surface missing a tab, a control,
or a field the approved wireframes carry; a records tab that
can mutate a record; or a Playwright comparison against the
approved screens that fails while the stage is reported done.
*Does not establish:* that the terminal endpoints scale or
that the SSE tail survives the cloud edge — the claim covers
the desktop surface the wireframes draw.

**C087-11 — The events bus's persistence semantics are
stated once, and the code matches the statement.**
Exactly one documented statement (module docstring, user
manual, and HelpView, in agreement) declares whether events
are persisted or ephemeral-by-design and what a subscriber
can rely on; the emit path's behaviour matches the statement,
and the statement's presence is pinned by a test.
*Falsifier:* documentation surfaces disagreeing about the
bus's semantics; behaviour contradicting the statement (for
the documented-ephemeral ruling: any surface promising
delivery or replay; for a persistence ruling: an event
emitted with no subscriber that is not later retrievable);
or the pinning test removed while the statement remains.
*Does not establish:* that the ruled disposition is the ideal
one — only that it is a decision, stated where a reader
looks, and true of the code.

**C087-12 — Anchor-set dedupe removes exact duplicates only,
through the API, on the record.**
Stage S6 deletes an anchor set only when another set with
identical (name, language, pairs content) is kept; the
earliest canonical copy of each distinct content survives;
every deletion goes through `DELETE /anchor-sets/{id}`; and
every removed id, with its group's kept id, is recorded in
the stage record.
*Falsifier:* a deleted set whose (name, language, pairs
content) differs from its group's kept set in any element; a
distinct content with no surviving copy; a deletion performed
by direct database write; or a removed id absent from the
stage record.
*Does not establish:* that the surviving sets are good data —
placeholder content that is distinct survives this stage by
design; judging it is a separate act.

**C087-13 — Every live graph still resolves and runs with
byte-identical results.**
After each of S2 and S3, all 27 live graphs resolve every
atomicId they reference, and the pinned comparison runs
produce results byte-identical to their pre-stage records.
*Falsifier:* a live graph with a dangling atomicId after any
stage; or a comparison run whose output bytes differ from
its pinned pre-stage record in any field.
*Does not establish:* that the graphs' results are correct —
only that this program did not change them, which is the
non-goal the owner set.

**C087-14 — This program changes no verdict, claim status,
or ledger content.**
No stage of Spec 087 alters an Indus claim's status, stage,
or score, appends or edits a ledger entry, or modifies a
frozen record; the claims ledger and the freeze records are
byte-identical before and after the program.
*Falsifier:* a diff in `glossa-indus/ledger/claims.jsonl` or
any freeze record attributable to a Spec 087 PR; or a claim
status/stage in the app database changed by a stage's
execution (S6 touches anchor sets only).
*Does not establish:* anything about the truth of any claim —
the program is about the tool, not the decipherment.

**C087-15 — Manual updates land with the behaviour.**
Every stage PR that changes user-visible behaviour updates
the affected manual surfaces (user-manual, USER_GUIDE,
HelpView as applicable) in the same PR; no stage merges with
its manual update deferred to a later PR.
*Falsifier:* a merged stage PR whose behaviour change has no
corresponding manual change in the same PR, where the stage
record does not name why no manual surface is affected.
*Does not establish:* that the updates are well written —
only that they are not late, which is the failure F7
documents at scale.

**C087-16 — The Study Builder's schema module no longer
impersonates the node registry.**
After Stage S1, the module formerly named `node_registry.py`
is renamed (`study_node_registry.py`) or, if the owner rules
otherwise, carries a header and a docs entry stating it is
the Study Builder's param-schema module; its endpoint
(`GET /node-registry/{node_type}/{ref_id}`) answers unchanged,
and both registries import in one process without ambiguity.
*Falsifier:* a module named `node_registry.py` in the tree
after S1 without the recorded owner ruling for option (b); a
broken `/node-registry/` endpoint; or a document that still
points a reader at the old name for the experiment registry.
*Does not establish:* that the two node systems should be
merged — only that they stop sharing a name.

**C087-17 — The registry changes only by recorded acts.**
After S2's re-pin, the registered count and the per-category
census in the completeness test change only through a Spec
087 stage PR that names the change in its stage record; the
count never moves as a side effect of an unrelated change.
*Falsifier:* a merged PR that alters the pinned counts
without a stage record naming the alteration; or runtime
counts differing from the pin while CI is green.
*Does not establish:* that the registry should never grow —
new primitives are welcome; this claim makes their arrival
an act, not an accident.
