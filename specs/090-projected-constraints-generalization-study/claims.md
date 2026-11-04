# Spec 090 — Claims

Every claim carries at least one falsifier (a concrete observation that
would show it false) and a "does not establish" line (the over-reading it
forbids), per the program's claims discipline. The same set, normalized
into `aee-claims.json` without substantive change, was validated under
the pinned AEE (1.5.3) before any study task starts (Stage 0, T002;
`records/t002-aee-assessment.json`). Grounding for every factual
statement below: `records/commission-and-grounding-2026-11-04.md`,
counted and read first-hand from the repo at origin/main `c643500b` on
2026-11-04. The skeleton's terms (D1–D6, S1–S5, G1–G5) are as defined
in `records/GENERALIZATION-SKELETON-2026-11-04.md` (AXIOVEX/vexa commit
88839493, SHA-256 a66ffe4f…), which governs wherever this file and the
skeleton's usage differ.

## The G1 document

**C090-1 — The G1 document exists as a single standalone artifact,
written before results.** One document, in the spec's records
(decision D-090-1), states Glossa's record system (D1), projection
rule (D2), and primitive-absolute disposition (D3) in the skeleton's
terms. It is written and frozen before any G2 derivation is attempted,
and any later change to it is a new version under a recorded amendment
act, so the document the G2 stage and any independent reader cite is
identifiable by hash.
*Falsifier:* G2 work begun with no G1 document on record; or the G1
content scattered across stage prose such that no single document can
be handed to a reader; or a G1 document whose bytes changed after its
freeze with no amendment act recorded.
*Does not establish:* that the document's definitions are right — only
that exactly one citable document carries them, stated before results,
as G1 requires.

**C090-2 — The record-system definition covers the program's actual
record classes, each with its provenance rule.** The G1 document
defines the record system over the classes the program's verdicts
actually rest on — corpus records (the inscription files and their
loaders), anchor records (the anchors register), and ledger claim
lines — naming for each class what a record is, what provenance it
carries, and its population counted from the records at the state
read. A record that breaks its class's stated provenance rule is
accounted for by the definition (named as an exception class with its
count — as the anchors register's 3 `no_validation_record` entries
require), never silently absorbed.
*Falsifier:* a record class the program's verdicts rest on that the
definition omits; a provenance rule the class's actual records violate
with the violators unaccounted; or a population figure in the document
that the records at the cited state do not reproduce.
*Does not establish:* that the records are complete or correct — only
that the system the study reasons about is the system the program
actually has, provenance rules and exceptions stated.

**C090-3 — The projection rule is stated as a rule.** The G1 document
defines the candidate system state for the decipherment domain and
states a rule pi mapping a candidate state to the records it would
produce, precisely enough that, given two named candidate states,
whether pi distinguishes them is decidable from the stated rule
alone — not from the drafters' intuition about the states.
*Falsifier:* a stated "projection" that names no mapping from states
to records (a narrative about interpretation, a metaphor of
projection); or two states the document calls projection-equivalent
that produce different records under its own rule; or an equivalence
question the document's rule cannot decide either way.
*Does not establish:* that the stated rule is the right projection for
the domain — only that it is a rule in D2's sense, which is what makes
equivalence classes, and therefore G2, possible at all.

**C090-4 — The cannot-distinguish account is explicit and grounded in
the program's underdetermination record.** The G1 document states
what the records cannot distinguish, and every indistinguishability it
asserts is tied to a named record or count in the program's own
record: the signary's frame-dependence (Spec 077's frozen 557-sign
population against the 64 distinct signs attested in the M77 corpus
file and the 713 distinct codes of the ICIT frame); corpus-attested
signs and contexts carrying no anchor coverage; the anchors register's
44 `pending_non_sa_validation` readings, whose validation chain is
incomplete on the register's own face; and completions of the script
that differ only outside the surviving records.
*Falsifier:* an asserted indistinguishability that no cited record or
count supports; or a pair of states the account calls
indistinguishable that a cited record does distinguish; or a
distinguishable-on-the-record case, of a kind the account claims to
cover, that it omits.
*Does not establish:* that the indistinguishable states are equally
plausible — equivalence under pi is a fact about the records, not a
probability over decipherments, and the account assigns none.

**C090-5 — At most one primitive absolute is taken, or none — and
this package does not prejudge which.** The G1 document either (a)
names exactly one primitive absolute in D3's sense — a quantity taken
as given in absolute terms, not relative to the records — with the
audit showing every other absolute-looking input to be record-relative
or derived from the named one; or (b) proves none is needed, by
exhibiting each candidate absolute as record-relative or derived. If
the audit finds the domain requires two, the document says so, and
the study records a skeleton mismatch (under D3 the domain then does
not instantiate this skeleton); it does not force a fit by demoting
one absolute without argument.
*Falsifier:* two quantities in the G1 document both taken as given in
absolute terms, whether or not both are called absolutes; a
none-needed claim coexisting with an input the document uses
absolutely and never derives; or a demotion of a candidate absolute
with no derivation or record-relative account behind it.
*Does not establish:* which outcome obtains — the claim binds the
discipline (at most one, audited), and binds it identically whether
the answer is one, none, or a mismatch.

**C090-6 — The absolute disposition is reached by audit over the
candidates the practice actually uses.** The G1 document enumerates
the candidate absolutes in the program's real practice — at minimum:
the corpus frame a record set is read under (which sign inventory a
corpus file's codes answer to); the anchor readings' external
identifications (readings imported from named scholarship rather
than derived from the records); and the surviving corpus's extent
(what counts as the complete record set) — and disposes of each on
the record: record-relative (shown to vary with the records, with
the variation exhibited), derived (from the named absolute or from
the records), or the named primitive absolute itself.
*Falsifier:* a candidate absolute in the program's practice that the
audit never considers — in particular an audit that never raises the
frame question; or a disposition asserted without the exhibited
variation or derivation it claims.
*Does not establish:* that the enumerated candidates are the only
conceivable absolutes — only that the ones the practice demonstrably
uses were each faced and disposed of, which is what an audit is.

**C090-7 — The G1 document carries definitions only.** Per the
judging protocol, the G1 document contains the record system's
definition, the projection rule, the cannot-distinguish account, and
the absolute disposition — and no conclusions: no claim that the
domain instantiates or fails any skeleton element, no G2 material, no
outcome language. The study's conclusions live in the derivation
record and the outcome record, which are separate artifacts.
*Falsifier:* a sentence in the G1 document asserting an outcome (that
an S element is met, that a necessary condition holds, that the study
succeeded or failed at anything); or G2 content appearing in the G1
document's frozen version.
*Does not establish:* that a definitions-only document is neutral in
effect — definitions decide what can be derived; the claim is only
that the protocol's separation is kept, so a reader judges the
definitions without the team's conclusions in hand.

## The G2 derivation

**C090-8 — The necessary condition is derived from D1–D3 and the
stated projection, not imported from physics.** The G2 derivation
record shows its chain step by step, and every step follows from the
skeleton's definitions and the G1 document's stated projection rule,
record-system definition, and absolute disposition. No step cites a
physics result — no F0 theorem, no separator result, no
identifiability result about causal sets or order-and-count
observables — as a premise. A candidate whose chain needs such a
premise is recorded as not derived, with the step named.
*Falsifier:* a derivation step whose justification is a physics
theorem or the physics instantiation's example; or a chain step that
follows from nothing stated (a gap presented as a step).
*Does not establish:* that a physics-*suggested* candidate is barred —
the analogy may occasion a candidate; the claim binds the derivation,
which must stand with the physics premise removed.

**C090-9 — The necessary condition is stated over projection-
equivalence classes, in D4's form.** The derived statement N is
claimed for every state in every projection-equivalence class
consistent with the records, as the G1 document's projection defines
the classes — a statement about what must hold in every completion
of the records, not a regularity observed in the records that happen
to survive.
*Falsifier:* a "necessary condition" whose derivation establishes it
only over the observed corpus (an empirical regularity with a
class-level label); or a statement whose quantifiers range over
records rather than over states in classes.
*Does not establish:* that N is interesting — a true but trivial N
(an artifact of the definitions with no bite over candidate
decipherments) satisfies the letter of this claim; whether N bites
is part of what the derivation record must show and the outcome
record must say plainly.

**C090-10 — The necessary condition carries its falsifier in D4's
form.** The derivation record states the observation that would
refute the derivation's application: a record, of a kind the G1
record system admits, that the framework — the stated projection
plus the derived condition — declares impossible, whose observation
would falsify the derivation. The refuter is concrete enough that
its occurrence would be recognizable in the record system (a named
record kind with named properties), not a gesture at future evidence.
*Falsifier:* a derived condition with no stated refuter; or a stated
refuter that is not a record the record system admits (a scholarly
consensus, a statistical trend, a document the system cannot hold).
*Does not establish:* that the condition is true — only that it is
exposed to the records in the way D4 requires, so its standing can
change on evidence.

**C090-11 — A failed derivation is recorded as NOT YET, with the
obstruction named.** If no candidate's chain completes at S2, the
stage record states the G2 outcome as NOT YET and names the
obstruction: which premise fails, which step does not follow, or
what the stated projection cannot support — specifically enough that
a successor study knows what would have to change. No weaker
statement is substituted and called derived, and no candidate is
carried as "essentially derived."
*Falsifier:* a closed S2 with neither a completed derivation nor a
named obstruction; or an obstruction stated so generally ("the
domain is too hard") that no successor could act on it.
*Does not establish:* that the obstruction is permanent — NOT YET
names missing work, and the skeleton records it as a publishable
outcome, not as a refutation of the domain or the skeleton.

## Boundaries

**C090-12 — The executable-matrix element is accounted exactly as it
stands, and this study builds none of it.** Where the study's records
address D6/S5, they cite the standing machinery as it operates: the
append-only ledger; the matrix and maps generated from it by script;
the gate (classes V1–V10) recomputing by an independent route and
never writing, with publication only on ALL PASS; settling under
glossa-settle-1. The account claims the machinery's existence and
operation only as the Specs 086–089 records establish them, and
credits Spec 090 with no part of building, extending, or repairing
any of it.
*Falsifier:* an outcome or stage record crediting this study with
machinery from Specs 086–089; or describing the gate as adjudicating
claims, writing artifacts, or doing anything its own header and the
stage records do not support.
*Does not establish:* that D6's presence advances the instantiation
question by itself — the scoping note already grants the element and
still finds G1/G2 open; the matrix is the study's substrate, not its
result.

**C090-13 — The study's only ledger change is its adoption intake
append.** Across the whole spec, the claims ledger's diff is exactly
the append of this spec's own claim bundle through
`tools/ledger/import_bundle.py` at adoption, plus the regeneration of
the generated layers that append forces (the C088-15 / C089-18
pattern). No stage adjudicates, reclassifies, annotates, or scores
any claim; no claim about the Indus script changes status, stage, or
score as a consequence of any stage; and the program's standing
position (the Indus script is not deciphered) is untouched.
*Falsifier:* a ledger diff attributable to a Spec 090 PR beyond the
adoption append's lines; or an Indus claim reclassified, annotated,
or re-scored citing this study.
*Does not establish:* anything about the appended claims' truth —
only that the ledger's one-way flow survives this study intact.

**C090-14 — The study implies no convergence step.** Nothing in this
study enters the program into VEXA convergence Stage 1, alters the
program's local stack, or contributes a convergence-dashboard item.
The study runs beside the program's stack as a registered study
about the skeleton; if convergence later adopts the skeleton as a
maintained form, that is a separate program act under its own gates,
not a consequence recorded here.
*Falsifier:* any record of this study describing it as a convergence
step, a Stage 1 entry, or a dashboard item; or a stack change made
in this study's name.
*Does not establish:* that convergence will or will not happen — only
that this study is not it, per the commission's own boundary.

**C090-15 — G3, G4, and G5 remain unattempted by this spec.** No
separator is computed or validated for G3 credit; no gate refusal or
kill is staged or claimed for G4 credit; no reproduction materials
are assembled or claimed for G5. Where the study's records touch
standing instances from the program's history (the gate's recorded
refusals, the matrix's regeneration checks), they cite them as
program history with their own records, never as this study's
G3/G4/G5 evidence.
*Falsifier:* an outcome record claiming any of G3–G5 as attempted,
partially met, or met by this study; or program-history instances
presented without their own records as though produced under this
spec.
*Does not establish:* that G3–G5 are unattemptable later — they are
commissioned in principle by the same order and sequenced after this
study; this claim binds only what this spec does.

**C090-16 — The outcome is recorded in the skeleton's vocabulary and
reported to the VEXA chat, either way.** The study closes with an
outcome record stating the per-stage outcomes (G1: STATED or NOT YET
with the missing element named; G2: DERIVED or NOT YET with the
obstruction named) and the study-level outcome as spec.md defines it
(INSTANTIATES-path, ANALOGY with the metaphorical element named, or
NOT YET with the missing work stated), each with evidence pointers to
the stage records. The outcome — or, if a stage cannot run, the
blocker — is reported to the VEXA chat for the improvement registry,
as the commission requires. The formal verdict over the full G1–G5
bar belongs to the independent reader under the judging protocol;
this study does not issue it.
*Falsifier:* the study closing with no outcome record; an outcome
stated in vocabulary the skeleton does not define (a "partial
instantiation," a percentage) without mapping to its terms; or no
report delivered to the VEXA chat after the outcome record lands.
*Does not establish:* that the reported outcome is the final verdict
on the domain — the reader's verdict under the protocol, and the
G3–G5 follow-on, both stand after it.
