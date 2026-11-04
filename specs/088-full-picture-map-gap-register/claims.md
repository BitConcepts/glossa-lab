# Spec 088 — Claims

Every claim carries at least one falsifier (a concrete observation that
would show it false) and a "does not establish" line (the over-reading it
forbids), per the program's claims discipline. The same set, normalized
into `aee-claims.json` without substantive change, was validated under the
pinned AEE (1.5.3) before any build task starts (Stage 0, T002;
`records/t002-aee-assessment.json`).

## The generated map (S1)

**C088-1 — The program map is generated, never hand-edited.** The program
map JSON, the find list, and the page are produced only by the builder from
the ledger, the taxonomy, program-map-defs, and the spec tree. A committed
output that differs from a fresh build over the same inputs is caught by
the CLI's `--check` mode, which exits nonzero naming the drifted output and
writes nothing; no stage edits a generated output by hand.
*Falsifier:* a committed program-map output that `--check` accepts while
differing from a fresh build over the same inputs; or a merged Spec 088 PR
whose diff edits a generated output without the corresponding input change.
*Does not establish:* that the map's content is right — only that it is
derived, and that drift is a failure, not an edit.

**C088-2 — Coverage is total and exact, and the builder fails closed.**
Every ledger claim id (857 today) is assigned to exactly one claim node and
every spec directory (88 today) to exactly one study node, under the
taxonomy. Duplicates, omissions, unknown ids, and unassigned directories
each fail the build, with nothing written.
*Falsifier:* a build that succeeds with a claim id or spec directory
missing, duplicated, or assigned to two nodes; or a taxonomy entry naming
an id or directory that does not exist, accepted silently.
*Does not establish:* that the taxonomy's assignments are the right
groupings — only that they are total, singular, and enforced.

## Standing derivation (S2)

**C088-3 — Claim standings derive mechanically from ledger fields under
program-map-defs v1.** A claim node's status class and standing text are
computed from its governing ledger entry's fields (status, stage, falsifier
presence) under the derivation table registered in program-map-defs v1,
with reclassification chains resolved in ledger order before deriving. The
builder reads no prose — no spec text, stage record, or narrative — for any
standing, and a status string outside the registered table fails the build.
*Falsifier:* a claim node whose class differs from the table's output for
its governing entry; a standing computed from a prose source; or an
unregistered status string classified by inference instead of failing the
build.
*Does not establish:* that the derivation table is the right semantics —
only that it is registered, total over the observed vocabulary, and the
only route to a class.

**C088-4 — Study standings are a registered roll-up over their claims, and
underdetermined cases are named, not smoothed.** A study node's class is
computed from its member claims' classes under program-map-defs v1's
roll-up precedence. A study whose members are mixed positive and negative
is emitted in the build record's judgment-call list with its member counts
and the registered default class it is displayed under; no study class is
assigned by hand.
*Falsifier:* a study node whose class contradicts the roll-up over its
members; a mixed study absent from the build record's judgment-call list;
or a study class traceable to an editor's choice rather than the precedence
or the recorded default.
*Does not establish:* that the roll-up captures a study's importance or
quality — only that its shown class is the mechanical consequence of its
claims' standings, with the hard cases listed.

**C088-5 — A study with no ledger claims classes as unjudged and generates
a register find.** A spec directory with no bundle claims in the ledger
(28 today: the 001–025 directories and `026-core-research-source`) receives
a study node of class unjudged — no derivation exists — and the builder
emits one machine-generated find per such study into the build's find list,
which the register stage consumes. The node shows no standing beyond the
fact.
*Falsifier:* a bundle-less study shown with a derived class or a prose
standing; or a bundle-less study missing from the emitted find list.
*Does not establish:* that bundle-less studies are unimportant — several
are load-bearing history; only that the ledger carries no claims to derive
a standing from, which is GAP-C13's shape stated per study.

**C088-6 — Every node cites the record it derives from.** Every claim node
carries its ledger id and every study node its spec directory name.
Citations resolve against the ledger and the spec tree at build time and at
gate time; a node whose citation does not resolve fails both.
*Falsifier:* a node in program-map.json with no citation, or whose ledger
id or spec directory does not exist in the inputs.
*Does not establish:* that the cited record carries the standing's weight —
only that every standing names the record it was derived from, so a reader
can open it.

## Gate extension (S3)

**C088-7 — The gate gains a program-map equivalence class with its own
registered definitions.** The Spec 086 gate gains class V10 (program-map
equivalence): it recomputes the program map from the ledger and taxonomy
by an independent route under the gate's own registered copies of
program-map-defs v1 — not imported from the builder — and fails unless the
recomputation equals the published artifacts, coverage is exact, citations
resolve, and the as-of stamp matches the current ledger. A red V10 blocks
publication of the map artifacts exactly as a red class blocks the matrix
today.
*Falsifier:* a published program-map artifact that differs from the gate's
recomputation while the gate reports ALL PASS; a definitions change made
in the builder's copy only that the gate accepts; or map artifacts
published under a red gate.
*Does not establish:* that the builder is correct — the gate is a second
route to the same derivation, and agreement is consistency, not truth.

## Page and taxonomy (S4, S1)

**C088-8 — Filters and search act only on generated fields.** The page's
class filters and text search operate exclusively on fields present in
program-map.json (title, standing, class, citations, domain, subdomain).
The page computes no standing, class, or count that is not in the generated
data; the per-domain counts it displays are the generated coverage block's.
*Falsifier:* page behaviour — a filter result, a search hit, a displayed
count — that cannot be reproduced from program-map.json's fields alone; or
standings logic in the page's script beyond filtering and searching the
generated fields.
*Does not establish:* that the page is usable or attractive — only that it
is a view of the generated data and nothing else.

**C088-9 — The taxonomy is curated, versioned, and changes only by
amendment acts.** Claim and study assignments live in one curated file,
versioned program-map-taxonomy v1. The builder fails on a node whose
domain or subdomain is not in the taxonomy's declared lists, and any change
to an assignment is a new taxonomy version recorded in the spec's stage
record in the same motion — never an unrecorded edit.
*Falsifier:* a build accepting an undeclared domain or subdomain; or an
assignment change in git history with no version bump and no stage-record
entry in the same motion.
*Does not establish:* that v1's groupings are final — only that grouping
changes are acts with versions, not edits.

## Scans and register (S5, S6)

**C088-10 — Gap scans use the four-kind template only, and every candidate
carries a falsifier.** Each scan's finds are classified as exactly one of
missing node, missing edge, thin evidence, or stale bookkeeping. Every
candidate study a scan proposes carries a one-line falsifier. A scan output
containing a fifth kind, an unclassified find, or a falsifier-less
candidate fails the register stage's completeness check.
*Falsifier:* a scan report with a find outside the four kinds, or a
candidate with no falsifier, accepted into the register.
*Does not establish:* that the scans found everything — only that what
they found is in the registered shapes, each with its test stated.

**C088-11 — Register v1 consolidates the standing named gaps, checked
against their source lists.** Gap register v1 contains at least one entry,
or a recorded not-a-gap disposition, for every item on the registered
source lists: GAP-C07; the GAP-C12 remnant; GAP-C13 (consolidating the
per-study finds of C088-5); the repair brief's WP2 (linguist
certification), WP3 (recomputation blockers), and WP5 (anchor-support
residuals: 37 requires-revalidation, 3 expert-pending, 2 insufficient)
items; Spec 086's residuals (matrix edges for the live population; the
two-graph-worlds join at population one); the T201 mahadevan:64 derivation
divergence; the 9-null-falsifier disposition question; the tracker llms.txt
staleness; the desktop-clone sync state; the data-lineage owner question;
and the 44 pending anchor readings. The consolidation task runs a
completeness check that enumerates the source lists and fails on an
unmapped item.
*Falsifier:* an item on a named source list with no register entry and no
recorded disposition when register v1 is presented for ratification.
*Does not establish:* that the register is complete in nature — only that
it is complete against the program's own already-named lists, which is
checkable.

**C088-12 — In-house re-derivation and independent confirmation are
different edge types, and neither is recorded as the other.** In the map
and the register, a relation or candidate is typed as in-house
re-derivation or independent confirmation. A study or candidate that only
re-derives in-house is never recorded as closing an outside-reproduction
gap; the standing instance is WP4, whose eligible independent Parpola
comparisons number 0 of 184 because the comparisons are circular.
*Falsifier:* a register entry marking an outside-reproduction gap closed,
or a map edge typed independent, whose cited evidence is this program's own
re-derivation; or an in-house result rendered without its type.
*Does not establish:* that in-house re-derivation is worthless — it is
most of what the program has; only that it is not the other thing.

## Cross-cutting invariants

**C088-13 — Generation is deterministic and the as-of stamp is
input-derived.** Identical inputs (ledger bytes, taxonomy version, defs
version, spec tree) produce byte-identical program-map.json and page. The
stamp carries only input-derived values — the ledger canonical hash, the
ledger line count, the ledger's own latest entry date, and the defs and
taxonomy versions — and no wall-clock time, per the Spec 086 stamp
discipline.
*Falsifier:* two builds over identical inputs differing in any byte; or a
stamp field that varies with build time.
*Does not establish:* that the inputs are current — only that the outputs
are a pure function of them, so staleness is detectable by stamp
comparison.

**C088-14 — Counts are published per domain; no cross-domain aggregate
progress score exists.** The builder's summary output and the artifacts'
coverage blocks report node counts per domain, and per class within a
domain. No output of the builder, gate, page, or register computes or
displays a single cross-domain aggregate progress figure — no program-wide
percent-supported, no single progress number.
*Falsifier:* any Spec 088 surface showing one aggregate progress number
spanning domains.
*Does not establish:* that per-domain counts summarize a domain's health —
they are counts of nodes by class, nothing more.

**C088-15 — The spec's only ledger change is its adoption intake append.**
Across the whole spec, the ledger's diff is exactly the append of this
spec's own claim bundle through `tools/ledger/import_bundle.py` at
adoption, plus the regeneration of the generated layers that append
forces. No stage appends, edits, or reclassifies any other entry, and no
claim's status, stage, or score moves as a consequence of any stage: the
map derives standings and never writes them back.
*Falsifier:* a ledger diff attributable to a Spec 088 PR beyond the
adoption append's lines; or a pre-existing entry whose fields differ after
any stage.
*Does not establish:* anything about the truth of the appended claims —
only that the ledger's one-way flow (Spec 086) survives this spec intact.

## The adoption constraints and standing rules

**C088-16 — The gate extension lands before the page can publish (C1).**
No program-map page or JSON is published — committed as a live artifact or
served — before the gate's V10 class is live in CI over those artifacts.
The build order in plan.md (defs, builder, gate extension, page) is a
dependency, not a preference, and the page stage's record cites the V10
gate output over the page's own artifacts.
*Falsifier:* a published program-map artifact whose stage record lacks a
passing V10 run over it, or that predates V10's landing in CI.
*Does not establish:* that the gate makes the page true — only that the
wider population never travels around the verification the narrower one
has.

**C088-17 — Prose-only standings never become map data (C2).** Where a
study's standing exists only in prose — a stage record, a report, a spec's
narrative — the builder does not read it: the study classes by derivation
(C088-4) or as unjudged (C088-5), and the shortfall is emitted as a
stale-bookkeeping find for the register. There is no curated-standing
mechanism in the taxonomy format and no code path that accepts one;
RCPH's source-and-token curated standings are expressly not adopted.
*Falsifier:* a taxonomy entry carrying a standing or status-class field
for a node; or a study node whose standing text quotes or paraphrases a
prose source rather than its derivation inputs.
*Does not establish:* that prose standings are wrong — several are the
program's real history; only that they enter the picture through the
register, where a human can judge them, not through the builder.

**C088-18 — The in-flight class is registered with an empty v1
population, and says why.** Program-map-defs v1 registers the in_flight
class with no derivation rule, because no record of record in the
repository carries study run-state — job state lives in the live backend,
outside the builder's inputs. No node carries in_flight in v1, and a build
emitting one fails; running work is visible through the scans and the
register, not the map, until a registered run-state source exists.
*Falsifier:* a v1 program-map node with class in_flight; or in-flight
status inferred from prose dates or stage-record language.
*Does not establish:* that nothing is running — work is; only that the map
does not claim to know it from records it cannot read.

**C088-19 — Restricted records render name-only.** A study under a
standing owner restriction (in v1: Spec 072, whose public naming is
"executed — held under the Roif gate") appears in the generated artifacts
as a node carrying its directory name, the restricted flag, and that
registered name-only form — no derived standing text and no class chip.
The restriction list lives in the taxonomy; adding a study to it is an
amendment act.
*Falsifier:* any rendered standing, class, or summary text for a
restricted study beyond its name, its flag, and the registered name-only
form.
*Does not establish:* anything about the restricted study — that is
precisely its function.
