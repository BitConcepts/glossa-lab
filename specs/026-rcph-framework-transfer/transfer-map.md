# Spec 026 — RCPH Framework Transfer Map

**Purpose.** Record, principle by principle, what transfers from the
RCPH formalization program's research framework to the Indus
(Glossa) program, what Glossa already does, where the gap is, and
what change Spec 026 adopts. This document is a mapping, not a
result. It mints no reading, promotes no anchor, and changes no
prior verdict.

**Sources read for this map.**

RCPH (`~/workspace/rcph-formalization/`):

- `AGENTS.md` — claim discipline; Spec 022 framework feature;
  Spec 032 source-version rule.
- `.specify/memory/constitution.md` — Principles I–VIII.
- `docs/RESEARCH_METHOD.md` — Rules 1–5.
- `docs/GENERAL_RESEARCH_FRAMEWORK.md` — the domain-neutral
  framework manual, v1.1 (cited below as *Framework Manual*,
  by section and by CORE requirement).
- `docs/FRAMEWORK_REVISION_022.md` — cited as *Revision 022*.
- `docs/research/FRAMEWORK_APPLICATION_MIGRATION.md` — cited as
  *Migration*.
- `docs/research/FRAMEWORK_AUDIT_032.md` — cited as *Audit 032*.

Glossa (`~/workspace/glossa-lab-spec026/`):

- `.specify/memory/constitution.md` — §§I–VIII.
- `docs/governance/rules.md` — hard rules H13, H15, H21, H23,
  H26 in particular.
- `specs/024-evidence-integration/spec.md` — cited as *Spec 024*.
- `specs/025-stage2-controlled-followup/spec.md` — cited as
  *Spec 025*.

Style note: verdict words in capitals (INVALID, SUPPORTED, …)
are labels with defined meanings, not emphasis. Historical
Glossa labels are quoted exactly and are never rewritten
(Principle 6, Principle 12).

---

## Principle 1 — No target smuggling

### RCPH principle

No target-law smuggling. Known physics may be a theorem target
or an empirical checksum, but not an upstream axiom under
renamed notation (*RESEARCH_METHOD.md*, Rule 1). The core must
remain pre-physical: A0–A9 must not import a Lorentz metric,
proper time, Einstein equations, Hilbert space, particles, gauge
fields, thermodynamic entropy, or consciousness primitives
"merely to recover those same targets later" (RCPH
constitution, Principle I). A target quantity introduced as an
assumption is a **bridge assumption**, never a core theorem.
Physics is a checksum, not a premise (*AGENTS.md*, Claim
discipline).

### Indus adaptation — NO TARGET-READING / LANGUAGE SMUGGLING

A hypothesized reading, a simulated-annealing (SA) output, a
later-language outcome (for example a Proto-Dravidian form), or
a desired decipherment outcome may not appear as a premise, a
feature, a control, a label, or a tuning target in any test of
that same claim, or of a claim that depends on it. In
operational terms:

- A sign value under test may not be an input feature of the
  test that purports to validate it.
- A language model built from assumed readings may not score
  those same readings.
- A motif may not be coded using a hypothesized meaning of the
  motif or of an accompanying sign.
- A bridge assumption (for example: "this compilation's
  positional classes reflect the script's grammar") must be
  named as a bridge, with its own claim record (Principle 2).
  It is never absorbed into a result as if it were observed.

### Existing Glossa equivalent

Partial, and strong where it exists. Rule **H26** (rules.md):
SA agreement — a modal reading, a consistency score, a z-score,
a consensus fraction — must not be a sufficient condition for
promotion, upgrade, or validation of any anchor; every promotion
must cite a recorded non-SA evidence reference. Basis recorded
in H26 itself: Phase-107 (Spec 005) recovered 0.000 held-out
anchor signs, with Sanskrit and scrambled controls statistically
identical to Dravidian. Spec 024 extends the same discipline to
context evidence: interpretive fields (a compilation's morpheme,
noun, verb, and "translation" annotations) are Class I and are
"excluded from context evidence by construction" (Spec 024,
Epistemic boundary 2 and §3.4), and its codebook "contains no
sign meanings, no reading hypotheses" (Spec 024 §4.3). Spec 024
§8 names the iconography-to-meaning leap as "the precise
circularity this program has already falsified once."

### Gap

H26 is a promotion gate for anchors. It is not a general
smuggling rule for tests. No current Glossa rule states, for an
arbitrary phase, that a hypothesized reading or a later-language
outcome may not be a feature, label, control, or tuning target
inside the phase's own test. Spec 024's Class I exclusion covers
the layers it inventories; it does not bind a future phase that
builds a new feature from reading-derived material under a new
name — the exact "renamed notation" failure RCPH Rule 1 is
written against. Bridge assumptions are declared in prose
(assumptions fields, H13) but are not labeled as a distinct
kind that a dependent claim may not silently inherit.

### Adopted change (Spec 026)

1. Adopt the rule as stated above, verbatim in scope, as a
   governance rule applying to every phase and spec, not only
   to anchor promotion. H26 remains in force as its
   enforcement point for promotions.
2. Every spec and phase proposal must carry a
   `forbidden_assumptions` list (Principle 2) that names, at
   minimum, the readings, SA outputs, and language outcomes
   the work is not permitted to use as premises. A proposal
   with an empty list must state why it has none.
3. Any assumption that supplies part of the target (a reading,
   a language identification, a decipherment outcome) is
   recorded as a **bridge** claim (kind: conjecture-bridge,
   Principle 2). Results conditional on it are reported as
   conditional on it, in the headline, not in a footnote.

---

## Principle 2 — Claim taxonomy and stable IDs

### RCPH principle

Every substantive claim has a stable identifier and a kind:
definition/axiom, kernel-checked theorem, conditional
reconstruction, empirical identification/checksum, or
conjecture/open bridge (RCPH constitution, Principle II;
*RESEARCH_METHOD.md*, Rule 2, classes P0–P4). The Framework
Manual (§ "Requirements and claim records"; CORE 03, CORE 04)
makes the record mechanical: a Claim carries `id`, `text`,
`kind`, `boundary`, `falsifier`, `assumptions`, `depends_on`,
and `forbidden_assumptions`. Claim kinds there are axiom,
mathematical, conditional, empirical, calibration, and
conjecture. The dependency checker follows every declared
ancestor, rejects cycles and unknown IDs, and compares
inherited assumptions against each claim's forbidden
assumptions. The Manual states the limit plainly: the checker
"cannot recognize an undeclared premise or a renamed equivalent
formula. Mathematical review is still required."

### Indus adaptation

Every substantive Indus claim carries a stable ID and one of
six kinds, stated in Indus terms:

| Kind | Indus meaning |
|---|---|
| definition | A stipulated term, sign-list convention, normalization rule, or coding category. True by stipulation, within its stated scope. |
| data observation | A count, coverage figure, or property read directly off a named, hash-pinned source (Principle 11), with no test applied. |
| computational result | An output of a named, replayable computation on named inputs (Principle 7): a statistic, an agreement rate, a permutation count. It asserts what the computation returned, nothing more. |
| conditional model result | A result that holds only under named model or bridge assumptions (for example, under a specified positional template or a harmonization, Spec 025 §8.5). The assumptions travel with the result. |
| empirical identification | An assignment of an observed object, sign, or pattern to a category on evidence independent of the claim-generating method — the strongest kind this program can issue, and the rarest. |
| conjecture-bridge | A proposed connection (reading, language affiliation, continuity claim) that no current test has discharged. May be registered, may not be used as a premise (Principle 1). |

Each claim record carries: `boundary` (corpus, layer, population,
and conditions in which the claim is meaningful), `assumptions`,
`depends_on` (claim IDs), `forbidden_assumptions`, `falsifier`
(a specific observation or computation that would defeat the
bounded claim), and `strongest_rival` (the strongest alternative
explanation the program can state — the Manual's operating
procedure: "list assumptions and identify the strongest
alternative").

### Existing Glossa equivalent

Fragments, in several places, with no common register.
Constitution §IV requires decipherment claims to be stated as
falsifiable hypotheses with falsification conditions, confidence
levels, and evidence basis. Rule H13 requires every proposal to
state its epistemic boundaries, the BeliefArtifact IDs it relies
on, its hidden assumptions made explicit, and the adversarial
challenge that could break it. Spec 024 §3.4 grades fields
(Class O / C / I), which is a taxonomy of evidence, not of
claims. Spec 025 §5 pre-specifies a robustness criterion and
names load-bearing strata in advance. PRED-2026-001/002/003 are
stable IDs for three registered predictions. There is no
program-wide claim register, no claim-kind field, no
`depends_on` graph, and no cycle or forbidden-assumption check
over claims.

### Gap

Claims live in spec prose, phase reports, and ledger entries,
under inconsistent names. Nothing mechanically prevents a claim
from depending, through a chain of prose references, on an
assumption it elsewhere forbids — the failure the RCPH checker
exists to catch. "Strongest rival" is practised in good specs
(Spec 025 §9, Spec 024 §10) but is not a required field, so a
weak spec can omit its rival entirely and still pass review.

### Adopted change (Spec 026)

1. Introduce a claim register for new work: one record per
   substantive claim, with the fields and six kinds above.
   Existing claims are not retro-registered by this spec;
   a claim enters the register when a new spec or phase
   depends on it, and is registered at that point with its
   original source cited.
2. Where tooling supports it, run two mechanical checks over
   the register before a freeze: (a) the `depends_on` graph is
   acyclic and every ID resolves; (b) no claim inherits, through
   its ancestors, an assumption on its own
   `forbidden_assumptions` list. A failed check blocks the
   freeze. The checks are structural only; per the Manual,
   they do not detect undeclared or renamed premises, and no
   report may claim they do.
3. `falsifier` and `strongest_rival` become required fields.
   A claim with no statable falsifier is registered as
   conjecture-bridge by default.

---

## Principle 3 — Computation / countermodel symmetry

### RCPH principle

Proof or Countermodel Symmetry (RCPH constitution, Principle
III). A research obligation is resolved by positive closure (a
proof under explicit assumptions) **or** by negative closure (a
rigorous countermodel or non-implication result showing the
assumptions do not force the target). "A negative closure is a
successful scientific result." A negative closure of a narrow
issue does not close a broader target; the broader obligation
stays open (*AGENTS.md*, Claim discipline; constitution, Issue
Closure Policy). The Framework Manual (§ "Experiment contracts
and verdicts"): "A counterexample can be a successful research
result even when it defeats the preferred hypothesis," and "No
verdict automatically changes a Claim kind or closes a broader
research obligation."

### Indus adaptation — COMPUTATION / COUNTERMODEL SYMMETRY

A bounded Indus question is resolved by either of two successes:

- **Positive closure:** a frozen computation (Principle 7) meets
  every declared rule on complete data, under controls that
  discriminate (Principle 5); or
- **Countermodel closure:** a discriminating null, control, or
  countermodel defeats the bounded claim — a grammar-free
  generator that matches the target statistic, a control
  language that scores as the target language scores, a
  composition-only model that reproduces the association.

Both are successes and are reported with the same prominence.
A narrow closure closes only the narrow question. A result
about one layer, one object class, or one sign class never
closes a question about the script as a whole, and never moves
a reading, an anchor, or PRED-2026 unless the frozen design
said, in advance, that it would (Spec 024 §7: no output of that
spec is an input to PRED-2026 in either direction).

### Existing Glossa equivalent

Practised, repeatedly, without a stated symmetry rule.
Phase-107 is a countermodel closure treated as a program-level
success: SA was falsified as evidence, and the consequence was a
governance rule (H26), a provenance audit (Spec 006), and a
headline re-base (Spec 007) — not a quiet burial. Spec 024 §12
("Results as found") requires every stage to report negatives,
NOT ESTIMABLE outcomes, and gate failures. Spec 025 §8.7 and
§11 Q6 require negative and NOT ESTIMABLE outcomes to publish
with the same prominence as positives. Spec 024 §0 records
closed routes as closed "by verdict or by owner decision," each
with its scope stated.

### Gap

The symmetry is a habit of the better specs, not a rule a weak
spec can be held to. No text states that a countermodel outcome
is a success rather than a failed run, and no text states the
narrow/broad rule for Indus questions: a narrow negative (for
example, no motif↔sequence association on one coded sample)
could be over-read, in a summary or a later spec, as closing
the broader question it bounded. RCPH states both halves in its
constitution; Glossa states neither half in its own.

### Adopted change (Spec 026)

1. Adopt the symmetry as a stated rule: positive closure and
   countermodel closure are both successful outcomes of a
   frozen design; neither is a failed experiment.
2. Every closure record states two scopes explicitly: the
   question closed, and the broader question that remains open.
   A closure record with no "remains open" line is incomplete
   unless the broader question is itself the one closed.
3. Summaries, headlines, and later specs must cite a closure at
   its recorded scope. Widening a closure's scope in citation
   is a defect to be corrected by a new record (Principle 12),
   not by editing the closure.

---

## Principle 4 — Evidence independence by origin group

### RCPH principle

Evidence records carry `direction` (supports / opposes /
neutral), `kind` (observation, proof artifact, literature,
generated assertion), `source`, `origin_group`, and an
independence note (Framework Manual, § "Evidence and
independence"; CORE 05). The origin group is the underlying
source of information: "Three reports generated from one run
count as one origin group." Support, opposition, and neutral
material are counted in distinct origin groups and retained
separately; the summary "does not turn their count into a
probability," and opposing evidence "is retained rather than
averaged away." Generated assertions must remain neutral:
"Text produced by a model is not converted into independent
evidence by placing it in another file." RCPH constitution
Principle II: model-generated prose must not be treated as
independent evidence.

### Indus adaptation

Independence is counted by origin, not by file, report, or
citation. For this program, one origin group includes, at
minimum:

- all layers derived from one underlying compilation (the
  ICIT-lineage layer and any derivative of the ICIT database
  are one origin group, however many files they arrive in);
- all reports generated from one run, one corpus build, or one
  coding pass;
- all values produced by one method from one input set — an SA
  run, a transcription pass, and a summary of that pass are one
  origin group, and the summary is generated assertion:
  neutral evidence, at any confidence wording.

Supporting, opposing, and neutral evidence for a claim are
listed separately, by origin group, in the claim's record.
They are never averaged, netted, or converted into a score that
hides an opposing group. Source reliability and version audits
(Principle 11) are part of the evidence record, not background
knowledge: a group whose source version has not been checked is
labeled unchecked.

### Existing Glossa equivalent

The lineage discipline exists and is enforced in the recent
specs. Spec 024 §2.4: the ICIT-lineage layer "is not an
independent witness for validation, and no Stage 2 result
computed on it may be reported without its lineage label
attached." Spec 025 §7 repeats the label as a mandatory
headline on every output, and §8.6 keeps "compilation-internal
explanations" as live alternatives for every association,
because "the layer's transcriptions and the harmonization's
sources sit inside overlapping scholarly traditions." Spec 024
§3.4 grades fields by recorder provenance. Constitution §I
requires a citation trace for every data file. What does not
exist: the origin-group unit itself, the
support/oppose/neutral separation as a reporting format, and a
rule that a generated assertion is neutral evidence.

### Gap

Without an origin-group unit, independence is asserted in
prose, per spec, and can be double-counted across specs: two
layers with different names and one ancestor can be cited as
two witnesses. Without the neutral rule stated generally, an
AI-generated summary, coding, or transcription can acquire
evidential weight by being filed, quoted, and re-quoted —
Glossa has the specific instance (Spec 024 §4.4: Stage 1
agreement numbers "are reported as properties of *this coding
pipeline*, never as properties of human expert coding") but not
the general rule.

### Adopted change (Spec 026)

1. `origin_group` becomes a required field on every evidence
   reference in a new spec, phase report, or claim record
   (Principle 2). Derivative corpora declare their ancestor;
   a derivative and its ancestor share a group.
2. Evidence summaries report three separate lists — supports,
   opposes, neutral — each as distinct origin groups. Averaged
   or netted evidence scores are not a permitted output for a
   claim.
3. Generated assertions (model prose, model coding, model
   transcription, summaries of any of these) are recorded as
   neutral evidence. They may be inputs to a designed test
   (as in Spec 024 Stage 1); they are never independent
   support for the claim they describe.

---

## Principle 5 — Discriminating controls

### RCPH principle

An experiment contract must declare at least one positive and
one negative control, with expected labels; every expected
control must be present, extra controls are rejected, and "a
failed positive or negative control returns invalid before
hypothesis metrics are considered" (Framework Manual,
§ "Experiment contracts and verdicts"; CORE 06). Revision 022
supplies the controlling failure: the frozen QD gate (specs 019
and 021) required a size-averaged mutual-information curve to
reach 0.9 H(S) by N/2 with no subsequent decline — a condition
that is automatic for any pure state once H(S) exceeds its
minimum, because complementary fragment informations sum to
2 H(S). A single Bell pair, with only one recording fragment,
passes it. "It cannot discriminate redundant records from
generic pure-state correlations." Both historical SURVIVES
labels stand in their files; their evidentiary status is
superseded as NON-DISCRIMINATING-GATE (Principle 12). The
replacement, QD-CONTROL-022, was frozen before execution, with
a positive control (GHZ records) and negative controls (a
single Bell pair, a product state, scrambled pure states), all
required to match their declared labels; "an invalid control
makes the experiment invalid."

### Indus adaptation

Every frozen Indus test declares at least one positive control
(a case the test must pass if it works) and at least one
negative control (a case it must fail if it works), each with
its expected label, before any confirmation data is examined. A
control discriminates only if it can, in principle, come out
differently from the target case. A control that cannot fail,
or cannot pass, differentially is a **non-discriminating gate**:
any run gated by it is INVALID (Principle 6), whatever its
headline statistic says. The local instances are recorded so
the pattern is recognizable:

- **RCPH QD defect** (above): a threshold that pure-state
  arithmetic satisfies automatically.
- **Indus grammar-free generator:** in the blind-affiliation
  line (Spec 012, Phase-114; report
  `reports/phase113_blind_affiliation_summary.md` under the
  pre-renumbering filename), the target was defeated in 100% of
  draws by a grammar-free generator — a trigram-dominated
  grammar-free mixture — and in Phase-112 by a grammar-free
  positional-bigram template. A test that a grammar-free
  process passes as readily as the hypothesized grammar is not
  evidence for the grammar.
- **SA controls, Phase-107:** Sanskrit and scrambled controls
  were statistically identical to Dravidian under the SA
  objective (held-out recovery 0.000). The objective therefore
  carried no information about sign values; every later use of
  SA agreement as evidence inherits that defect (H26).

### Existing Glossa equivalent

Controls are used well in individual designs — Phase-107's
Sanskrit and scrambled controls are the reason H26 exists, and
Spec 025's permutation designs hold composition fixed within
strata (Spec 025 §4.1) — but no rule requires a declared
positive **and** negative control pair, with expected labels,
in every frozen test; no rule makes a failed control invalidate
the run before its metrics are read; and "non-discriminating"
is not a recorded verdict on any Glossa gate, even where the
program has in fact discovered one (the battery lines closed by
owner decision, Spec 024 §0, are an adjacent but distinct
disposition).

### Gap

This is the largest operational gap in the map. Glossa's
control failures have so far been discovered by strong designs
or by accident and then governed case by case (H26 for SA,
owner closure for the batteries). A future phase can still
freeze a gate that cannot discriminate, run it, and report its
label, with no rule violated — exactly the QD history, which
RCPH only caught in a later framework revision.

### Adopted change (Spec 026)

1. Every frozen test declares its positive and negative
   controls and their expected labels in the freeze record.
   A freeze with no negative control, or with a control whose
   expected label cannot differ from the target's, does not
   proceed.
2. Controls are evaluated first. A control whose observed label
   differs from its declared label makes the run INVALID;
   hypothesis metrics from that run are not reported as a
   result (they may be reported, labeled, as diagnostics of
   the invalid run).
3. When a gate is later shown to be non-discriminating, the
   disposition is RCPH's: original labels stand in their files;
   a new assessment record (Principle 12) supersedes their
   evidentiary status as NON-DISCRIMINATING-GATE. The record
   states what the old run does and does not establish.

---

## Principle 6 — Verdict taxonomy and the historical mapping

### RCPH principle

Verdicts follow a fixed order and a bounded interpretation
(Framework Manual, § "Experiment contracts and verdicts";
CORE 08):

| Verdict | Trigger | Permitted interpretation |
|---|---|---|
| invalid | Malformed data, failed control, or broken provenance | The test cannot support a scientific conclusion |
| inconclusive | Incomplete sampling or missing required metrics | Collect the missing evidence under the same valid contract |
| contradicted | Valid, complete observations fail at least one rule | The bounded tested claim did not survive |
| supported | Valid, complete observations meet every rule | The bounded acceptance conditions were met |

"No verdict automatically changes a Claim kind or closes a
broader research obligation. In particular, calibration remains
calibration even if every threshold passes."

### Indus adaptation

Glossa adopts the four verdicts — **INVALID / INCONCLUSIVE /
CONTRADICTED / SUPPORTED** — for all new frozen tests, with the
triggers and permitted interpretations above, and maps its
historical labels onto them for reading only. The mapping is a
reading aid for old records. It is not a relabeling: original
labels stand, in their files, unchanged (Principles 11 and 12,
and constitution §II: historical ledger entries are never
rewritten).

### Mapping table (required)

| Historical Glossa label | Where it occurs | Maps to | Notes |
|---|---|---|---|
| FAIL (e.g. "FAIL — DISAGREEMENT") | Phase-125 cross-compilation positional comparison (Spec 019; recorded in Spec 024 §0 and Appendix B) | CONTRADICTED | A valid, complete comparison failed its declared agreement criterion. The bounded claim (the two compilations' positional profiles agree) did not survive. |
| REJECTED (at calibration / at its own gate) | Validation batteries, Phases 113 / 115 / 117 / 118 (Specs 011 / 014 / 016 / 017; Spec 024 §0) | INVALID | The battery was rejected at its calibration gate: the test setup did not qualify to judge the claims. No verdict on the claims themselves follows. |
| KILL | CSSR line (RCPH usage preserved in Revision 022: "Preserve the existing KILL as a result for its implementation, finite data and frozen criteria"); Glossa owner closures of lines of work | CONTRADICTED, bounded to the named implementation and criteria — plus a separate administrative closure | KILL closes the named line, not the broader question (Principle 3). Where KILL records an owner decision to stop a line rather than a test outcome, the test verdict and the decision are two records, not one. |
| NULL (e.g. HONEST-NULL; F2's null standing, Spec 025 §1) | Phase and spec results where a valid test found no effect beyond its null | INCONCLUSIVE or CONTRADICTED, by the frozen rule — see note | A null against a declared practical margin (Principle 8) with an interval excluding the margin is CONTRADICTED. A null whose interval crosses the margin is INCONCLUSIVE. Historical NULLs are read as "no support found under that design" and are not retro-classified beyond this sentence. |
| middle-band | Owner and program usage for results between a proceed gate and a stop-rule (pattern frozen in Spec 024 §4.5: between stop-rule and proceed gate, "the motif arm is reported as measured; any use requires a fresh owner decision") | INCONCLUSIVE | Measured, valid, and below the declared acceptance rule. Not support; not contradiction. Requires a fresh decision for any use; no silent middle path. |
| NOT ESTIMABLE | Spec 024 §5.1 estimability rule; Spec 025 §2, §4.2–§4.4 (G1), §5 (LOSO subsets) | INCONCLUSIVE, designed subtype | The contingency or covariate structure fell below its frozen minimum, so no test was run. Reported with the cell or coverage counts shown; never rescued by post-hoc collapsing (Spec 024 §5.1). Distinguished from an ordinary INCONCLUSIVE because no data is missing — the design itself does not support estimation on this population. |
| DESCRIPTIVE | Spec 024 §5.5 arm (d): graffiti comparison is descriptive only; Spec 025 §1: "Arm (d) stays descriptive" | No verdict — outside the taxonomy | A descriptive output (overlap and distribution statistics) makes no tested claim and receives no verdict word. Labeling a descriptive output SUPPORTED or CONTRADICTED is a category error and is prohibited. |

### Existing Glossa equivalent

The raw material is all present: NOT ESTIMABLE as a designed
outcome (Spec 024 §5.1; Spec 025 passim), a middle band with a
no-silent-path rule (Spec 024 §4.5), descriptive-only arms
quarantined from testing (Spec 024 §5.5), FAIL and battery
rejections recorded with their scopes (Spec 024 §0, Appendix B).
What is absent is the taxonomy itself: the same underlying
outcome carries different words in different specs, and no
order of precedence (invalid before inconclusive before
contradicted/supported) is stated anywhere.

### Gap

Without a fixed taxonomy and precedence order, a run with a
failed control and a passing headline metric has no governing
word — the QD history again (Principle 5). Without the mapping
table, a reader of the historical record cannot tell whether a
REJECTED battery contradicts the claims it was built to test
(it does not) or whether a NULL is a measured absence or an
under-powered silence (it depends on the margin, Principle 8).

### Adopted change (Spec 026)

1. The four verdicts, triggers, precedence order, and permitted
   interpretations above govern every new frozen test.
2. The mapping table above is the program's reading of its
   historical labels. Originals are never rewritten; new
   records that cite a historical result give both labels on
   first use (e.g. "Phase-125 FAIL — DISAGREEMENT
   [CONTRADICTED under the Spec 026 taxonomy]").
3. DESCRIPTIVE remains a permitted output class with no verdict
   word, and NOT ESTIMABLE is retained as the named designed
   subtype of INCONCLUSIVE.

---

## Principle 7 — Freeze and replay integrity

### RCPH principle

`freeze(experiment, root, sources)` records a canonical
experiment definition, source-file hashes, and a UTC freeze
time, and returns a digest over the whole payload. "Save it
before obtaining the new experiment data; do not regenerate it
to accommodate an unfavorable result." `verify_freeze` detects
changed definitions and sources; a repair means a new
experiment version and a new freeze, with the original freeze
and failed run retained. `record_run` binds the run to the
freeze digest; `verify_run` replays the decision and detects a
changed metric, decision, or frozen source. The Manual adds the
limit honestly: "A hash establishes that bytes match a recorded
digest. It establishes neither truth nor independent
timestamping… Publish or commit the freeze before collecting
data when chronological independence matters" (Framework
Manual, § "Preregistration and reproducibility"; CORE 07).

### Indus adaptation

Every confirmatory Indus test has a canonical experiment
definition — population and inclusion rule, statistic, null,
rules and margins (Principle 8), controls (Principle 5), seed,
sampling/permutation plan, family membership (Principle 9) —
frozen and committed before any confirmation data is examined.
The freeze records: the definition, SHA-256 hashes of every
input file and analysis source file, the seed(s), and
environment metadata (package version read dynamically, per
rule H10; relevant library versions; GPU device where H20
applies). A changed gate, threshold, population, or control is
a new version and a new freeze. The old freeze and any run
under it are retained.

### Existing Glossa equivalent

Strong in the recent specs, as procedure. Spec 024 §12: the
owner's values are written in, the banner flips to FROZEN, and
"the freeze is committed alone"; each stage freezes separately.
Spec 025: the layer file is consumed read-only from its recorded
path and hash (sha256 recorded in §3, the same hash as the
Phase-136 inputs); anchors are asserted byte-identical before
and after every run, by sha256 (§7); G1's seed is "to be named in
the freeze" (§4.1); adjudication answers are recorded as
governing text (§11). Graph-first registration (H15/H23) and
the foundation check (H21) gate execution. What the procedure
does not yet produce is a single canonical freeze artifact —
definition + all source hashes + environment — against which a
run can be replayed mechanically, and Spec 025 still leaves the
seed to be named at freeze time rather than recording the
replay bundle as one object.

### Gap

Replay in Glossa is currently reconstructive: a reader gathers
the spec, the plan's freeze record, the input hashes, and the
script from different places and judges whether they match.
RCPH's `verify_run` is mechanical: one payload, one digest,
decision replayed. The gap is not intent — Spec 024/025 freeze
discipline is genuine — it is the artifact: no freeze digest
over the whole definition, no recorded environment block, and
no single replay check that fails closed.

### Adopted change (Spec 026)

1. New freezes produce one freeze record containing: the
   canonical definition (serialized, keys sorted), SHA-256 of
   every input and source file, seeds, environment block, and
   a digest over the record. The freeze record is committed
   alone, before confirmation data is examined (Spec 024 §12
   pattern, retained).
2. Every run record carries its freeze digest. A result whose
   freeze digest cannot be verified against the current sources
   is reported as a replay failure, not as a result.
3. Repairs follow RCPH: retain the original freeze and run,
   state the reason, assign a new version, freeze again before
   any new confirmation data. Regenerating a freeze to
   accommodate an unfavorable result is prohibited in terms.

---

## Principle 8 — Practical margins and uncertainty

### RCPH principle

Acceptance rules are declared, finite, numeric thresholds, and
statistical uncertainty is computed by the adapter and encoded
in the metrics — for example as a confidence-bound margin: "The
package does not manufacture confidence intervals from point
estimates" (Framework Manual, § "Experiment contracts and
verdicts"). The worked example sets its threshold as "a declared
engineering margin, not a universal research default." Revision
022's CSSR successor makes the rule concrete: paired held-out
log losses, block-bootstrap 95% intervals, a proposed practical
margin of 0.01 nats per symbol, and — the operative sentence —
"An interval crossing the margin is inconclusive." A baseline
advantage smaller than the preregistered margin "is not an
automatic scientific kill."

### Indus adaptation

Every confirmatory Indus test pre-declares, in its freeze:

- a **practical margin**: the smallest effect that would count,
  for this question, as a finding (an odds ratio, a Cramér's V,
  a TV distance, an agreement rate — in the statistic's own
  units, with the reason for the number stated); and
- an **interval estimate** reported alongside any p-value
  (permutation intervals, bootstrap intervals, or exact
  intervals, as the design specifies).

An interval that crosses the practical margin is INCONCLUSIVE
by default (Principle 6), however small the p-value is. A
p-value is never reported without its effect size and interval.
Margins are domain decisions (the Manual: thresholds "are
domain decisions"); Spec 026 sets no universal margin.

### Existing Glossa equivalent

Half present. Spec 025 reports effect sizes with intervals as
facts of record (F1: common OR 2.384, 95% CI 1.847–3.077,
§1) and its LOSO robustness criterion is defined on estimates
and intervals, deliberately, "not new tests" (§5). Spec 024
§4.5 freezes numeric gates for the motif pilot (agreement
≥ 85% and κ ≥ 0.75 to proceed; < 70% or κ < 0.50 to stop).
Permutation p-values are computed with the (1 + count)/(1 + B)
convention (Spec 025 §4.1). What no Glossa freeze yet declares
is a practical margin distinct from the significance threshold:
q = 0.05 decides SUPPORTED/NOT SUPPORTED (Spec 025 §4.4, §6),
so a statistically detectable but trivially small effect and a
large effect receive the same verdict word.

### Gap

Significance is doing two jobs: detecting an effect and
certifying that the effect matters. With n in the thousands,
the first job is easy and the second is unexamined. The CSSR
history in Revision 022 is the warning from the other side:
an advantage below a practical margin was nearly recorded as a
kill. Both errors — trivial effect promoted, marginal effect
killed — come from the same missing field.

### Adopted change (Spec 026)

1. `practical_margin` and the interval method become required
   freeze fields for confirmatory tests (Principle 7).
2. Verdict rule: interval entirely beyond the margin in the
   claimed direction → eligible for SUPPORTED; interval
   entirely on the null side of the margin → eligible for
   CONTRADICTED; interval crossing the margin → INCONCLUSIVE,
   by default, regardless of the p-value. A freeze may adopt a
   different rule only by stating it and its reason in the
   freeze.
3. Reports give effect size and interval before the p-value.

---

## Principle 9 — Exploratory / confirmation separation

### RCPH principle

Freeze the definition and sources before new data; "Execute
without tuning on the held-out result" (Framework Manual,
§ "Operating procedure and review"). If a repair is necessary,
retain the original and preregister again "before confirmation
data" (§ "Preregistration and reproducibility"). Revision 022,
on measurement optimization: "Optimizing a measurement after
observing results requires a new exploratory branch and
held-out confirmation." Its successor designs separate training
calibration from held-out conditions and choose hyperparameters
only on validation (CSSR and Geometry successor definitions).

### Indus adaptation

Tuning — of thresholds, strata, collapses, codebooks, feature
sets, or statistics — happens on exploratory data only.
Confirmation runs once, on held-out or fresh data, under the
frozen contract (Principle 7), and its result is the verdict.
Anything computed outside the frozen family is labeled
EXPLORATORY in every artifact that reports it. If confirmation
results prompt an optimization, that optimization starts a new
exploratory branch; it does not amend the confirmation, and its
own confirmation requires new held-out data under a new freeze.

### Existing Glossa equivalent

The labeling half is already a rule: Spec 024 §5.1 — anything
outside the frozen family "is labeled EXPLORATORY in every
artifact that reports it, without exception" — with the family
under Benjamini–Hochberg control at q = 0.05. Spec 025 §6 is
the worked example: family F25 declared; the family-accounting
question (BH over G1 alone vs over all members) was put to the
owner and decided "at adjudication, before any Phase-139
margins or outcomes were seen," and "will not be revisited after
outcomes are known" (§11 Q4). Spec 025 §4.2 inspects covariate
margins only in Phase-139 — no outcome is computed — and §11 Q5
records that the estimability thresholds "will not be tuned
after Phase-139 margins are seen." Spec 024 Stage 1's coding is
blinded, with comparison labels "unblinded only afterwards, as
a comparison — never as a coding input" (§4.4).

### Gap

The separation is enforced at the level of families and labels,
but the exploratory side is unstructured: there is no register
of exploratory branches, so an exploratory result can be quoted
later without its exploratory provenance, and no rule states
that post-hoc optimization after a confirmation spawns a new
branch rather than a revision of the old one. RCPH states that
rule in one sentence; Glossa has not stated it.

### Adopted change (Spec 026)

1. Adopt the branch rule in terms: post-hoc optimization after
   observing confirmation results spawns a new exploratory
   branch, with its own record; the confirmation stands as run.
2. Exploratory results carry the EXPLORATORY label and their
   branch of origin in every artifact, including summaries and
   ledger entries that cite them. An exploratory result cited
   without its label is corrected by a new record (Principle 12).
3. Family membership and the correction method are freeze
   fields (Principle 7), decided before outcomes are seen, on
   the Spec 025 §11 pattern.

---

## Principle 10 — Completeness grids

### RCPH principle

The adapter "must validate its exact sample grid before setting
complete=True"; the core checks the completeness flag and metric
presence, and incomplete sampling is INCONCLUSIVE (Framework
Manual, § "Experiment contracts and verdicts"). Revision 022's
QD successor campaign states the operational form: a complete
grid (sizes × seeds × couplings × times) is frozen before any
run; "All sizes, seeds and coupling configurations must contain
all five samples; a missing row is inconclusive"; each
configuration must pass at each persistence time, with failures
reported individually — "rather than pooling them away."

### Indus adaptation

Every frozen Indus test declares its grid: the full cross of
the factors its verdict depends on (sites × object classes,
strata × subsets, coders × sample strata, sizes × seeds, as the
design requires). The grid is validated exactly — every declared
cell present, with its count — before any verdict is computed.
A missing cell makes the affected verdict INCONCLUSIVE
(Principle 6), with the missing cells named. Cells are never
pooled, collapsed, or reweighted after the fact to make a
missing cell disappear; a collapse is permitted only if the
freeze pre-declared it (Spec 024 §5.1 states this for
contingency cells; Spec 026 generalizes it).

### Existing Glossa equivalent

Present in pieces. Spec 024 §5.1's estimability rule refuses
post-hoc collapsing and reports NOT ESTIMABLE with cell counts
shown. Spec 025 §3 is a completeness audit in all but name: fill
rates by field and by site, with the structural finding that
complete-case analysis on all three covariates would keep 16.8%
of the population and "confound 'controlled' with 'recorded by
a particular tradition'" — and the §4.2 eligibility gate (≥ 70%
recorded coverage; ≥ 3 eligible sites at ≥ 30 inscriptions;
≥ 1,000 permutable inscriptions) converts that audit into a
pre-declared routing rule. Spec 024 §3.2's coverage matrix is a
declared grid for the inventory itself. What is missing is the
general rule binding an arbitrary phase: declare the grid,
validate it exactly, name the missing cells, no pooling away.

### Gap

A phase can currently report an aggregate over whatever cells
happened to be populated, with completeness discussed in prose
if at all. The Spec 025 covariate tables show why that is not a
formality in this corpus: missingness here is structural and
site-blocked, so an unexamined aggregate silently becomes a
statement about the best-recorded sites.

### Adopted change (Spec 026)

1. `sampling_grid` becomes a required freeze field: the declared
   cells, the minimum per-cell requirement, and the collapses
   (if any) pre-declared.
2. The run record reports the grid as executed — every declared
   cell, its count, and every missing or deficient cell by name.
   The verdict computation checks the grid before the metrics
   (with the controls, Principle 5).
3. Post-hoc pooling or collapsing to cure a deficient grid is
   prohibited. The permitted responses are INCONCLUSIVE /
   NOT ESTIMABLE as designed, or a new version and new freeze
   (Principle 7).

---

## Principle 11 — Source-version checking

### RCPH principle

Criticism of one version of a source is not criticism of
another. Audit 032 records the instance: a targeted check found
arXiv:2605.06848v2, revised 2026-07-03, whose recovery
discussion "uses existence/rotated-recovery language different
from the v1 criticism in the repository. Preserve the v1
reproduction and inspect v2 separately." Version checking is
recorded in `SOURCE_VERSION_AUDIT_032.json`. The RCPH agent
instructions generalize it: "Inspect source-version changes
independently of prior-version criticism" (*AGENTS.md*, Spec 032
section). The Framework Manual's adoption rule is the same in
contract form: preserve original definitions and result bytes;
record superseding assessments in new files.

### Indus adaptation

Every corpus, layer, compilation, and cited source is pinned to
a version: file hash for local files, edition/version and
access date for published sources. A finding, criticism, or
exclusion recorded against version 1 of a source asserts
nothing about version 2. When a source changes version, the new
version is inspected on its own — its fields, keys, and
provenance re-audited to the extent the claim depends on them —
before any prior verdict is carried over, and the carry-over, if
any, is a new record stating its basis. Corpus snapshots are
pinned by hash at freeze time (Principle 7) and consumed
read-only.

### Existing Glossa equivalent

Pinning is practised for files: Spec 025 §3 records the
ICIT-lineage layer by sha256 and byte count, "the same file hash
recorded in the Phase-136 inputs," and §7 forbids editing the
layer file. Constitution §I requires citation traceability for
every data file, and Spec 024 §6 rejects a dataset record
without provenance and license fields. Spec 024 §3.3's join-key
audit is version-sensitive in effect: keys are validated against
the files as they exist, not assumed from a source's reputation.
What does not exist is the version rule for *criticism*: no text
states that a verdict against one edition of a compilation, one
version of a sign list, or one release of a dataset does not
transfer to the next version without re-inspection.

### Gap

Indus sources are living objects — compilations are revised,
sign lists are renumbered, datasets are re-released. Glossa's
own record contains the hazard in miniature: studies have been
renumbered (Spec 012, Phase-113 → Phase-114) and layers rebuilt
with changed contents under the same lineage name (Spec 014's
v2 layer policy against the Phase-107 builder). A criticism
filed against the old object can be quoted against the new one
with no rule broken.

### Adopted change (Spec 026)

1. Evidence and claim records name the source version they rest
   on: hash for files, edition/version for publications.
   Unversioned source references are incomplete records.
2. A verdict, exclusion, or criticism is scoped to the version
   it was made against. Applying it to a different version
   requires a re-inspection record for that version, however
   brief, stating what was checked.
3. A version change in a source underlying a frozen test is a
   provenance break (Principle 6, INVALID trigger) for any run
   not yet executed under that freeze.

---

## Principle 12 — Historical-assessment discipline

### RCPH principle

When a later framework revision changes what an old result
establishes, the old result is not edited. Revision 022 is the
pattern: "Both historical SURVIVES labels remain in their
original result files, but their evidentiary status for
redundant objectivity is superseded as
NON-DISCRIMINATING-GATE." The Migration document repeats it:
"The historical results remain intact. An external assessment
record marks the old QD acceptance criterion non-discriminating,
CSSR as a bounded implementation failure, MERA as unestablished
reconstruction, the Page curve as calibration, and curved causal
scale as anchored robustness." Past verdicts are interpreted
through a separate `historical-assessments.json` (*AGENTS.md*,
framework feature); new results require new experiment IDs and
freezes. The Framework Manual: "Record superseding assessments
in new files… explain the change without retrospectively
relabeling the old run."

### Indus adaptation

A historical Glossa label stays exactly as recorded. When later
work changes what that result establishes — a gate found
non-discriminating (Principle 5), a source superseded
(Principle 11), a scope found narrower than its citations
assumed (Principle 3) — the change is made in a **new assessment
record**, never in the original. The assessment record states:

- the original result: phase/spec, label, file, and date;
- the new evidentiary status, in the Spec 026 taxonomy
  (Principle 6);
- exactly what the old run **does** establish, at its bounded
  scope;
- exactly what it **does not** establish, naming the broader
  claim it has been, or could be, cited for;
- the evidence and reasoning for the change, with its own
  provenance (Principle 4).

### Existing Glossa equivalent

The instinct is constitutional and the practice is recent and
good. Constitution §II: the ledger is append-only; "Historical
ledger entries are never rewritten… corrections and migrations
are recorded as new entries." Spec 024 §12: "Ledger entries and
stage reports are appended; corrections are new dated entries,
never edits of the record," and §13 keeps a standing deviations
section so changes have a named place to go. Spec 007's headline
re-base after Phase-107/108 was executed as a new record (a
dated "Re-based after Phase-107/108" note and a draft addendum),
leaving the v4 preprint as the citation of record — an
assessment in substance. What Glossa does not have is the
assessment as a *form*: a record whose defined content is what
an old run does and does not establish, kept in one place and
consulted before old verdicts are cited.

### Gap

Corrections are scattered across ledger entries, spec sections,
README notes, and addendum drafts. Each is honest; together
they are hard to consult, so a superseded status can be missed
by a later spec that cites the original label in good faith.
RCPH keeps one assessments file for exactly this reason.

### Adopted change (Spec 026)

1. Establish a single historical-assessments record for the
   program (file format and location set in the Spec 026 plan;
   append-only, on the constitution §II pattern).
2. Every supersession from Spec 026 onward is entered there in
   the form above, including the two standing cases this map
   identifies: gates later shown non-discriminating
   (Principle 5) and verdicts whose scope is narrowed
   (Principle 3).
3. A new spec that cites a historical result with a superseded
   status must cite the assessment alongside the original.
   Citing the original alone, once an assessment exists, is a
   defect correctable by a new record.

---

## What does NOT transfer

Two RCPH instruments have no Indus counterpart, and pretending
otherwise would itself be target smuggling (Principle 1).

**Lean / kernel-checked theorems.** RCPH's strongest claim kind
is a theorem checked by the Lean 4.33.1 kernel, compiled with
the pinned toolchain, with no `sorry` or `admit` (RCPH
constitution, Principles III and VIII; *AGENTS.md*: "Do not call
a source-level lemma kernel-checked until Lean builds").
Nothing in the Indus program is kernel-checked, and nothing can
be: there is no formal system in which "this sign has this
value" is a proposition with a proof. No Glossa claim may use
the words *proved*, *theorem*, or *kernel-checked*, in any
artifact, for any result. The RCPH claim kind "kernel-checked
theorem" (Principle 2) transfers as an empty slot — retained in
the taxonomy precisely so its emptiness is visible.

**Physics checksums.** RCPH can check a derivation against
independently established physics: known physics as "an external
checksum after an independent derivation" (constitution,
Principle I). The Indus program has no established body of
readings against which a new reading can be checksummed. The
nearest objects — published sign lists, other compilations —
are themselves claims inside overlapping scholarly traditions
(Spec 025 §8.6), not independent ground truth. Agreement with
them is evidence of a stated, limited kind (one origin group,
Principle 4); it is not a checksum, and no report may call it
validation by checksum.

**What "kernel-checked" honestly is, here.** The Indus analogue
of a kernel check is the strongest verification this program
can actually perform, stated without borrowing Lean's authority:

1. **Deterministic replay:** the frozen computation (Principle 7)
   is re-executed from its freeze record — same inputs by hash,
   same sources by hash, same seed — and must reproduce the
   recorded decision and metrics exactly. A result that does not
   replay is not a result.
2. **Independent recomputation:** a second implementation, or a
   second analyst path, computes the same quantity from the
   same frozen inputs without sharing code with the first, and
   the two outputs are compared. Disagreement is reported, not
   resolved silently. This is the analogue of RCPH's dual
   derivations (*RESEARCH_METHOD.md*, Rule 4) at the level this
   program can support: two funnels, one number, or an honest
   record of the difference.

A claim that has passed both may be labeled **replay-verified**.
That label asserts reproducibility of a computation. It asserts
nothing about whether the computation's premises are true —
the same limit RCPH states for its own ledger: "a valid ledger
proves record continuity only, never truth" (constitution,
Principle VII).

---

## Risks

**R1 — Taxonomy theater.** Adopting RCPH's vocabulary without
its enforcement produces records that look governed and are
not. The Framework Manual states the underlying limit for its
own checker: it cannot recognize an undeclared premise or a
renamed equivalent. Mitigation in this spec: the adopted
changes attach each principle to a mechanical or procedural
check that can fail (freeze digest, control-first evaluation,
grid validation, cycle/forbidden-assumption checks) rather
than to wording alone. Residual risk stands: review judgment
remains load-bearing, as it does in RCPH.

**R2 — Retroactive pressure on the historical record.** A
mapping table (Principle 6) and an assessments file
(Principle 12) create a standing temptation to "clean up" old
labels. That is prohibited by constitution §II and by this
map; the risk is noted because the temptation will recur at
every future supersession, not because it is permitted once.

**R3 — Margin arbitrariness.** Principle 8 requires a practical
margin but cannot supply its value; a margin chosen to be easily
crossed, or easily missed, manufactures the verdict. Mitigation:
the margin and its reason are freeze fields, fixed before
outcomes are seen (Spec 025 §11 pattern), and an interval
crossing the margin defaults to INCONCLUSIVE rather than to the
preferred side. A reviewer who cannot see why the margin is
what it is should treat the verdict as unestablished.

**R4 — Origin-group under-declaration.** Principle 4 works only
if derivatives declare their ancestors. A layer acquired under a
new name, with its lineage undocumented, silently counts as a
second witness. Spec 024 §3.3's empirical key audit and §6's
provenance-required intake reduce this risk; they do not remove
it. Lineage claims are themselves claims (Principle 2) and are
recorded with their evidence.

**R5 — Control invention after the fact.** Principle 5 requires
controls declared in the freeze. A control chosen after seeing
results, and presented as discriminating, is the QD defect with
extra steps. Mitigation: controls are freeze fields (Principle
7); a control first mentioned in a report is a diagnostic, not
a gate, and cannot invalidate or validate the run it follows.

**R6 — Scope widening in citation.** Principles 3 and 12 depend
on later writers citing closures and assessments at their
recorded scope. Summaries compress; compression widens. The
program's in-depth reporting rule — a change is reported with
its checked cause or labeled unexplained — applies here: a
citation that cannot be traced to a record at the scope claimed
is reported as unverified, not repeated.

**R7 — Freeze rigidity against genuine discovery.** Strict
freeze/replay and exploratory/confirmation separation can be
misread as forbidding mid-course learning. They do not: they
re-route it, into a new exploratory branch and a new freeze
(Principles 7 and 9). The cost is real — some follow-ups will
wait for held-out data that may never arrive (the program's
standing watch-and-respond posture, Spec 024 §0, is the honest
form of that cost) — and is accepted over the alternative,
which is verdicts that cannot be replayed.

**R8 — Transfer overreach.** RCPH is a proof-oriented program
with a formal core; Glossa is an empirical program over a small,
derivative, structurally incomplete corpus. Principles that
presuppose RCPH's instruments (kernel checking, checksum
validation, exhaustive finite models — Framework Manual, §
"Finite constraint models") transfer only in the weakened forms
stated in "What does NOT transfer." Any future spec that imports
an RCPH term stronger than this map's adaptation must name the
difference in its own epistemic boundaries (H13), or the import
is smuggling under Principle 1.

---

*End of transfer map. Companion artifacts (spec.md / plan.md /
tasks.md for Spec 026, the claim-register and
historical-assessments formats) are specified separately; this
document is the mapping they must implement.*
