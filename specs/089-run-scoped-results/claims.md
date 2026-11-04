# Spec 089 — Claims

Every claim carries at least one falsifier (a concrete observation that
would show it false) and a "does not establish" line (the over-reading it
forbids), per the program's claims discipline. The same set, normalized
into `aee-claims.json` without substantive change, was validated under
the pinned AEE (1.5.3) before any build task starts (Stage 0, T002;
`records/t002-aee-assessment.json`). Grounding for every machinery
statement below: `records/directive-and-grounding-2026-11-04.md`,
counted and read first-hand from the repo on 2026-11-04.

## Run identity and lumping

**C089-1 — Every result-bearing execution carries a run id minted at
execution time.** An execution is result-bearing when its output is
written to a store of record or cited in a record of record. Every
result-bearing execution on the program's named surfaces (settling
runs, backend experiment jobs, study re-executions, suite runs cited
as evidence) carries a run id minted by the executing tool when the
execution starts, before its results exist, in the format registered
in run-defs v1 (decision D-089-1). The id names the execution, not its
content: two executions with identical inputs and identical results
carry different ids. An execution that produces no results (a crash,
an empty run, a refusal) still receives an id and a run record stating
the absence.
*Falsifier:* a result-bearing execution on a named surface whose
results are stored or cited with no run id, an id assigned after the
results existed, or an id derived from the results' content; or a
no-result execution with no run record.
*Does not establish:* that the run was honest or correct — only that
its results have exactly one execution to belong to.

**C089-2 — Run records are immutable; supersession is a labeled
relation, never a replacement.** A run record, once written, is never
edited or deleted by a later run. The settling run store's
content-addressed overwrite (settling.py's `run_record_filename`: a
same-basis rerun replaces its own record) is retired: a rerun writes a
new record under its own execution-minted id. Where a later run
supersedes an earlier one (the adoption-refresh pattern of Specs 087
and 088, where the superseded T405 pair left the store), the relation
is recorded as a labeled supersedes link in the run index (decision
D-089-3), and the superseded record remains in the store, addressable
under its own id, with its own results.
*Falsifier:* a run store whose census decreases outside a recorded
amendment act; a run record whose bytes change after its first commit;
or a superseded run reachable only through git history.
*Does not establish:* that superseded results are usable — a
superseded run's results carry their supersession wherever they are
cited (C089-4).

**C089-3 — Results are lumped by the run; pooling names its runs.**
Every verdict, census, stage record, report, and published number that
rests on run results rests on named runs. An aggregate over more than
one run names every run it pools and the comparability basis under
which pooling is claimed (C089-9); a figure that silently pools — a
pass count merged from two suite runs, a tally averaged over two
settling runs — is a defect on discovery and is withdrawn to its
per-run figures.
*Falsifier:* a verdict-bearing figure in a record of record that
aggregates multiple runs without naming them, or that names runs whose
comparability keys do not support the pooling claimed.
*Does not establish:* that pooling is never legitimate — only that it
is always declared, so a reader can unpick it.

**C089-4 — A cited number names its run.** Any number cited as
evidence in a record of record names the run that produced it (run id)
and that run's comparability key, or carries the legacy label of
C089-17 when the producing run predates the run record. A number whose
citation terminates in a summary of another summary — a stage record
citing a chat summary citing a run — does not satisfy this claim.
*Falsifier:* an evidence citation in a merged record that names no run
id and no legacy label, or whose named run record does not contain the
cited number.
*Does not establish:* that the cited run's number is right — only that
it is traceable to exactly one execution's record.

## Isolation

**C089-5 — A settling run's write surface is exactly its own run
record, and the store only grows.** Extending semantics §9: a settling
run reads only its pinned inputs, writes only its own run record
(under its execution-minted id) and its run-index entry, and cannot
modify, replace, or delete any earlier record. The run store's census
is monotonic under run operations: `materialize-sets` and any other
regeneration that today rewrites a shared artifact in place
(`assignment-sets.json`) becomes a run with a record, and the artifact
it produces names the producing run.
*Falsifier:* a settling or materialize-sets execution after which an
earlier run record's bytes differ, the store census fell, or
assignment-sets.json changed with no run record naming the
regeneration.
*Does not establish:* that the engine's semantics changed —
glossa-settle-1 is untouched; this is store discipline around it.

**C089-6 — Suite runs do not contaminate the tree they measure.** A
suite run's in-tree rewrites (the `extracted_claims` and
`claim_reports` regenerations) are part of that run's record: the run
record for a cited suite run states the tree state before and after,
names any regenerated paths, and states their disposition (restored
byte-identical to the committed inputs, or retained with the reason
recorded). A check whose pristine-tree precondition is destroyed
mid-run is reported not-run with the cause named — as today's records
already do by convention — never passed. Suite evidence is citable
only from a run whose record satisfies this claim.
*Falsifier:* a stage record citing suite results where the run left
the tree dirty with regenerated claim files and no run record names
the rewrite and its disposition; or a mid-run-precondition failure
reported as a pass.
*Does not establish:* that the suite is deterministic — the tray-flake
family is a named nondeterminism (C089-19); this claim governs the
tree, not the outcomes.

**C089-7 — A regenerated or cached artifact names its producing run
or build.** An artifact that is read as current (a generated layer, an
assignment set, a cached extraction) carries or is accompanied by the
identity of the run or build that produced it, in the stamp discipline
the generated layers already use (input-derived pins). An artifact
with no producing-run/build binding is labeled unbound wherever it is
cited, and an unbound artifact cannot ground a verdict.
*Falsifier:* a verdict grounded on a regenerated artifact that
carries no producing binding and no unbound label; or an artifact
whose stated binding names a run that did not produce it.
*Does not establish:* freshness — a bound artifact can still be
stale; staleness is detectable because the binding names what produced
it and over which inputs.

**C089-8 — Backend experiment results are citable only under their
job id, with inputs recorded.** A backend job already receives an
execution-minted id (uuid-based, `create_job`). When a job's results
are cited in a record of record, the citation names the job id and the
inputs the job ran over (graph id and version, parameters, data pins
where the graph reads data), recorded in a repo-side run record at
citation time. A result drawn from the live database with no job id,
or from a job whose inputs were not recorded, is unbound and cannot
ground a verdict.
*Falsifier:* a merged record citing experiment results with no job
id; or a citation whose named job's recorded inputs do not match the
inputs the cited result depends on.
*Does not establish:* that the backend must change — the identity
exists at execution; this claim binds it at citation, which is where
it is currently lost.

## Comparability

**C089-9 — Comparability is a registered key (run-key v1).** run-defs
v1 registers the comparability key: surface; command/tool and its
version; code version (the git SHA of the tree executed); input pins
(the per-surface hash list — for settling, the record's existing pins
block); seed, where the surface has one; environment class (host/venue
and runtime class). Every run record carries its full key. Two runs
are comparable (the owner's "similar") exactly when their keys agree
on the components run-defs v1 marks comparable-constitutive (decision
D-089-4): surface, command/tool, input pins, and seed. Code version
and environment class are recorded and diffed, and do not by
themselves break comparability.
*Falsifier:* a comparability judgment in any record that rests on
components outside the registered key, or a run record whose key omits
a registered component its surface has.
*Does not establish:* that comparable runs must agree — agreement is
the expectation the junction rule polices (C089-11), not a property of
the key.

**C089-10 — Similarity is decided by the key, never by names.** The
same scenario name, the same test file, the same job or graph name
does not make two runs comparable, and different names do not make
them incomparable. Where two runs' keys differ on a
comparable-constitutive component, the pair is reported as different
experiments (with the differing component named), never as a
divergence and never pooled.
*Falsifier:* a junction report or a pooled figure over a pair whose
keys differ on a constitutive component; or a comparability refusal
that cites a name rather than a key component.
*Does not establish:* that name-identical runs are usually comparable
— usually they are; the claim is that the key, not the name, is what
decides.

## The junction rule

**C089-11 — Divergence between comparable runs triggers a junction
analysis before any verdict use.** When two comparable runs (C089-9)
differ in any verdict-bearing result field, or one yields results and
the other yields none (absent, empty, refused, or crashed), a junction
report (C089-12) is produced before either run's results are used for
a verdict, a merge gate, a published number, or a claim adjudication.
Use first and analysis later is the defect this spec exists to remove;
the standing tray-flake adjudications (CI attempt 1 vs attempt 2 over
one head SHA, five instances in three days) are the pattern this claim
mechanizes.
*Falsifier:* a verdict, gate decision, or published number resting on
one of two comparable divergent runs with no junction report in the
record at the time of use.
*Does not establish:* that divergence implies a defect in either run
— it implies a question, and the junction is where the question is
answered or quarantined (C089-13).

**C089-12 — A junction report is mechanical first: key diff,
environment diff, first divergent output, disposition.** A junction
report names both runs by id; diffs their comparability keys component
by component; diffs their environment stamps; localizes the first
divergent output field (the `_first_divergences` discipline of
`run_settling.py`, generalized from expectation-comparison to
run-vs-run, including the one-side-empty case, where the first
divergence is the first result the non-empty side produced); and ends
in exactly one disposition: explained-by-named-difference (naming the
differing component and the evidence it caused the divergence),
not-comparable (a constitutive component differs; the pair is
reclassified under C089-10), identical-after-all (the reported
difference was in presentation, not in the records — the report names
the presentation artifact), or unexplained.
*Falsifier:* a junction report missing a named section, or carrying a
disposition outside the registered vocabulary, or an
explained-by-named-difference disposition that names a difference
without evidence connecting it to the divergence.
*Does not establish:* that the mechanical diff finds the cause — it
bounds the search; the unexplained disposition exists precisely for
when it does not.

**C089-13 — Unexplained junctions quarantine both runs.** While a
junction's disposition is unexplained, both runs' results are
quarantined: they may be cited only as quarantined (naming the
junction report), never as support for a verdict, a gate, or a
published number. Quarantine is a relation recorded in the run index,
not a flag edited into either run record (C089-2). It is lifted or
confirmed only by a recorded adjudication act: a named human's ruling
on the junction report, or a further run under a stated key whose
junction against the quarantined pair resolves the question.
*Falsifier:* a verdict resting on a run under an open unexplained
quarantine; or a quarantine lifted with no adjudication act in the
record.
*Does not establish:* that quarantined results are wrong — only that
their divergence is unexplained, which is disqualifying for verdict
use until it is not.

**C089-14 — Junction analysis is automatic; the unexplained
disposition escalates to a red-team pass.** The junction report is
produced by tooling when divergence is detected — at run completion
against the run index's comparable predecessors, and by store scan at
gate time — not by an operator remembering to ask. This is the owner's
"extra scrutiny, perhaps an automatic red team analysis of the
junction," operationalized in two tiers: the automatic mechanical
junction (C089-12), produced for every triggering pair; and, for any
junction whose disposition is unexplained, an adversarial red-team
section appended to the junction report (candidate causes attacked in
turn: input drift, code drift, environment drift, nondeterminism,
record corruption, presentation artifact), each marked sustained or
not on evidence. A comparable divergent pair with no junction report
falsifies this claim whether or not anyone noticed the divergence.
*Falsifier:* a comparable divergent pair in a run store with no
junction report; or an unexplained junction with no red-team section
and no recorded scheduling of one.
*Does not establish:* that software red-teams itself — the mechanical
tier is automatic; the red-team tier is a structured adversarial
record produced under the doctrine's standing red-team practice, and
its depth is a human judgment the disposition records.

## Gate integration

**C089-15 — The gate gains V11, run-binding.** After the run-record
machinery (S1–S3), the Spec 086 gate gains class V11 with its own
registered copies of run-defs v1's checkable rules (never imported
from the run tooling): it fails when (a) a published artifact in its
guarded set lacks a producing-run/build binding or names a run that
does not exist; (b) any record in its guarded set cites a run under an
open unexplained quarantine as verdict support; (c) a run store's
census disagrees with its run index, or a supersession link in the
index does not resolve; (d) two comparable runs in a guarded store
diverge with no junction report, or a junction report's disposition
is outside the registered vocabulary. No run-produced artifact
publishes around V11 once V11 is live over it (the C1 pattern of
Spec 088).
*Falsifier:* a published artifact or a gate ALL PASS coexisting with
any of (a)–(d) in the guarded set; or a run-defs change made in the
tooling's copy only that the gate accepts.
*Does not establish:* that the gate adjudicates junctions — it
detects missing bindings, missing reports, and forbidden citations;
adjudication stays a recorded act (C089-16).

**C089-16 — The gate never writes, never adjudicates, and never
lifts a quarantine.** V11 follows the gate's standing discipline: it
imports no write entry point (V9 audits this), produces only its
report, and its red state blocks publication. Lifting a quarantine,
ruling a junction explained, or reclassifying a pair as
not-comparable are acts recorded in the run index by their named
actors; the gate verifies the acts exist and are well-formed, and
never performs them.
*Falsifier:* a gate run that mutates any store; or a quarantine whose
only lifting evidence is a gate report.
*Does not establish:* that blocked publication is costless — it is
the intended cost; the alternative is verdicts on unexplained
divergence.

## Cross-cutting invariants and boundaries

**C089-17 — No retroactive re-adjudication; legacy runs are labeled,
not rewritten.** Standing verdicts stand on their records: this spec
re-opens none of them. Pre-spec run records are covered by index-only
reach-back (decision D-089-5): each receives a run-index entry under
a legacy id derived from its store path, carrying its recoverable key
components and the label legacy — key partial where components
(execution time, code version) are unrecoverable. A legacy run's
results may be cited only under that label, and a citation that
presents legacy results as fully bound falsifies this claim. The
spec's force is prospective: new runs, and new citations of old
results.
*Falsifier:* a pre-spec verdict re-opened by appeal to this spec; a
legacy run record whose bytes were rewritten to add a key; or a
post-spec citation of legacy results without the legacy label.
*Does not establish:* that legacy results are suspect — most are the
program's history; only that their binding is partial and must be
shown as such.

**C089-18 — The spec's only ledger change is its adoption intake
append.** Across the whole spec, the claims ledger's diff is exactly
the append of this spec's own claim bundle through
`tools/ledger/import_bundle.py` at adoption, plus the regeneration of
the generated layers that append forces (the C088-15 pattern). Run
records, run indexes, and junction reports live in their own stores;
no stage adds a run kind to the ledger, and no claim's status, stage,
or score moves as a consequence of any stage.
*Falsifier:* a ledger diff attributable to a Spec 089 PR beyond the
adoption append's lines; or a run, index, or junction record written
into claims.jsonl.
*Does not establish:* anything about the appended claims' truth —
only that the ledger's one-way flow survives this spec intact.

**C089-19 — Determinism is claimed per surface, in the key, or not
at all.** run-defs v1 registers each named surface's determinism
class: deterministic (settling under fixed pins; the generated-layer
builders under fixed inputs), where comparable runs must agree
byte-for-byte in their result blocks and any difference is a junction
by definition; or named-nondeterministic (the suite, with the
tray-flake family registered as a known nondeterminism; LM-bearing
experiment jobs), where divergence is expected to occur and the
junction's job is to show the divergence is inside the registered
nondeterminism's shape — a teardown-error-only difference, a sampling
difference — or quarantine the pair. A surface with no registered
determinism class cannot have its runs cited as evidence until the
class is registered.
*Falsifier:* a divergence on a deterministic surface dispositioned as
benign variation without a named difference; or evidence cited from a
surface with no registered determinism class.
*Does not establish:* that registered nondeterminism excuses any
divergence — the junction must still show the divergence matches the
registered shape; a new shape is unexplained.

**C089-20 — The boundary with the fabricated-delivery protocol is
explicit.** That protocol (owner order, 2026-11-04) governs presented
results: a background-delivery presentation is a claim, never a
result, and gate-deciding reads run in the foreground. This spec
governs recorded executions. A fabricated delivery is not a run,
creates no run record, and enters no junction; a run record certifies
what an execution recorded, never that a presentation of it was
honest. Where a presented result and a run record disagree, the
record governs (standing rule) and the disagreement is a presentation
defect under that protocol, not a junction under this spec.
*Falsifier:* a junction report opened over a delivery-versus-record
disagreement; or a run record cited as proof that a delivery was
faithful.
*Does not establish:* that the two defenses overlap in coverage —
they are complementary by construction, and the gap between them (an
honest delivery of a contaminated run) is exactly what this spec
exists to close.
