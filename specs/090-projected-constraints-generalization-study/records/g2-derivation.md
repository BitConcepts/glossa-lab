# The G2 derivation record — Spec 090, Stage S2 (2026-11-04)

**Scope.** Tasks T201 (candidate derivations). Executed on
branch `feat/090-s2-g2-derivation` from origin/main
`8d8e470a3d14eaee59794d2bc6b2e1dcf88f7cc8` (the Spec 090 S1
merge, PR #514). The audit of this record (T202) is a
separate worker's act under the plan's separation rule; the
G2 outcome (DERIVED / NOT YET) is declared on that audit,
not here. This record is the deriver's side: the candidates,
their chains, their falsifiers, their bite statements, and
the derivation-provenance self-audit the audit will check.

**Basis, and nothing else.** The frozen G1 document,
`records/g1-document.md` **v1.1, SHA-256
4f2018f40c9ccaf0811cd7661b0c9e1ebd840c7e014d954f778c42edef27efc2**
— recomputed from the file on this branch before any
derivation step was taken, and matched against
`records/stage-s1-freeze-record.md`. Citations below of the
form "§2.2" are to that document. Skeleton citations (D1–D5)
are to `records/GENERALIZATION-SKELETON-2026-11-04.md`.
Per decision D-090-3 and claim C090-8, every step of every
chain follows from D1–D3 and the G1 document's stated
projection, record system, and absolute disposition — no
physics result is a premise anywhere in this record. Where
the physics instantiation occasioned a candidate, that is
named as occasion, in the self-audit, and the chain is
written to stand with the occasion removed.

**Conventions.** A class is *consistent with the records*
in D4's sense when the class's projection agrees with the
recorded codings — operationally, per G1 §2.2's closing
paragraph, a state s is consistent when, for each coded
corpus of §1.2, T(s) restricted to that corpus's object
set is projection-equivalent (§2.3) to the corpus's
recorded table. The consistent classes are non-empty: each
frame of §1.2 is itself a named state (§2.1: the frames
are named states' (Σ, γ) components, presented as coded
corpora), and its own class is consistent by identity.
"Named state" is used in §2.1's sense throughout.

**Outcome of this record, in summary.**

| Candidate | Statement (short form) | Chain |
|---|---|---|
| 1 | Non-certification: no state is singled out by the records within its class | **Complete** (§2) |
| 2 | Recorded-profile: every consistent state induces each corpus's recorded identity structure | **Complete** (§3) |
| 3 | Register-certification over the unvalidated readings | **Not derived** — obstruction named (§4) |
| 4 | Standalone corpus regularities as necessary conditions | **Not derived** as stated — obstruction named; content is Candidate 2's corollaries (§5) |

---

## 2. Candidate 1 — the non-certification condition

**Statement (D4 form, one sentence).** *Every state in the
domain is projection-equivalent to states that differ from
it in reading assignment and language identification, in
sign-inventory members that no object of the record system
exercises, and in classification of objects outside the
surviving record set — so no record of the system, and no
test computed from the records, distinguishes a state from
every other member of its projection-equivalence class.*

The quantifiers range over states and their classes, as
C090-9 requires: the statement is claimed for every state
in every class (a fortiori for every class consistent with
the records), not read off the surviving corpus.

**Derivation chain.**

1. *The records determine states only through the
   projection.* D2: everything the record system can ever
   know is a property of the equivalence classes of π,
   never of the states inside a class. G1 §2.4's preamble
   carries the same sentence for this domain. What a record
   can determine about a state is therefore exactly what is
   constant across the state's class.
2. *The projection factors through the classification
   alone.* G1 §2.2: π(s) = T(s), the sequence table of γ
   over the operative object set O; "The projection does
   not depend on ρ or on λ"; and every further record the
   state determines is a function of T(s).
3. *Assertions are not determinations.* G1 §2.2: anchor
   records (§1.3) and claim lines (§1.4) "are not outputs
   of π: they are assertions about states… their content
   is what is at issue between candidate states, never a
   projection of any one of them." The absolute audit
   confirms the disposition from the practice side (§3.4:
   imported identifications stand at "claim standing, not
   given standing"). So the only channel by which a record
   determines anything about a state is step 1's channel:
   the projection.
4. *Readings vary inside the class.* From step 2 and G1
   §2.4β: for fixed (Σ, γ), every (ρ, λ) variant of a state
   lies in one equivalence class. Hence every state has
   class-mates realizing every other reading assignment
   and language identification over its own classification,
   and no record determines any part of a state's (ρ, λ).
5. *Unexercised inventory varies inside the class.* G1
   §2.3, as repaired at the freeze: a state differing from
   another only by an inventory member no token on O
   exercises "has the same exercised inventory and the
   same table, and is equivalent to it." Hence no record
   determines a state's inventory beyond its exercised
   part.
6. *Off-record behavior varies inside the class.* G1 §2.2
   defines π over the operative O and §2.4δ draws the
   consequence: states agreeing on every object in O but
   differing on objects outside O are equivalent. Hence
   no record determines a state's classification of
   anything outside the surviving record set.
7. *Assembly.* From steps 1 and 3, determination runs only
   through the class; from steps 4–6, the class of every
   state contains states differing from it in (ρ, λ), in
   unexercised inventory, and off O. Therefore no record,
   and no test computed from records (a function of π by
   step 2), distinguishes a state from every other member
   of its class. ∎

**Counted form.** Record class: Class II coded corpus
records — the system's projection-bearing derived records
(the M77 coded corpus, the ICIT coded corpus, the CISI
coded subset; §1.2). *Forbidden combination:* a member of
the class whose stated derivation takes a reading
assignment or a language identification as an input —
equivalently, whose sequence table is not computable from
glyph streams under a frame (Σ, γ) alone; such a record's
content would vary between two states of one class, which
is the combination the condition excludes. *Counting
rule:* enumerate the class's members; for each, inspect
its derivation of record for its inputs; count the members
whose derivation takes (ρ, λ) as an input. *Count at the
frozen state, executed at this stage:* **0 of 3** — the
M77 derivation (loader of record
`backend/glossa_lab/data/indus_m77.py`: OCR and a
sign-rank-correlation glyph mapping from Mahadevan 1977)
takes glyph data and its frame; the CISI subset's
derivation (loader of record
`backend/glossa_lab/data/indus_cisi.py`: a digitization of
the CISI volumes in Parpola P-codes) takes the published
texts and its frame; the ICIT file's derivation
(`backend/scripts/ocr_icit_corpus.py`: OCR extraction from
Fuls 2023) takes the published books' glyph data and its
frame. The rule extends to the remaining classes by their
definitions, not by enumeration: Class I and Class V
records carry object content (provenance fields, text
codes) that takes no candidate state as input at all
(§1.1, §1.5), so no member can separate class-mates;
Classes III and IV are outside the count because their
content is assertion, and step 3 — a stated rule of the
frozen G1 document, not an inspection result — is what
denies assertions determining force. That boundary is
labeled for the audit in §6.

**Falsifier (D4 form).** A Class II coded corpus record,
admitted to the record system with its derivation named,
whose stated derivation computes its sequence table from
glyph streams *and* a reading assignment — for instance a
corpus file coded by syllabic values under a named
decipherment, whose segmentation or sign-identity rule
references that decipherment's ρ. Such a record is of a
kind the record system admits (a coded corpus with a named
derivation, §1.2); its content would separate states that
§2.2 places in one class; and its observation would refute
this derivation's application, because step 2 — the
factoring of π through γ alone — would fail for the record
system as enlarged. The falsifier's force runs through the
G1 basis in exactly the way D4 phrases it ("the
observation that would refute the derivation's
application"); §6 labels this rather than hiding it.

**Bite.** The condition excludes, as record-determined,
every statement of the form "the inscription records show
that sign X reads as v" or "the corpus establishes
language L" — including any future decipherment presented
as proven by the records rather than asserted with grounds.
It bounds every statistic computed from the coded corpora
(all are functions of T, step 2) to conclusions about
classifications, never about readings. It does not rank
decipherments against each other, and it does not touch
the assertion layer: anchor records can be supported or
refuted *as assertions*, on their stated grounds, without
engaging this condition. Its content is the domain's
no-determination theorem: not a caution about the present
state of scholarship, but a consequence of the stated
projection — true of every state, in every class, whatever
records of the admitted kinds are added.

---

## 3. Candidate 2 — the recorded-profile condition

**Statement (D4 form, one sentence).** *Every state
consistent with the records induces, over the object set
of each coded corpus in the record system, that corpus's
recorded identity structure: the same number of exercised
signs, the same token-multiplicity profile, and the same
sequence-length profile, up to relabeling.*

The statement is per-corpus by necessity, not by
convenience: cross-frame identity is crosswalk-mediated
and partial (§2.4ε), and the absolute audit names no frame
as the frame (§3.2), so no frame-free profile exists to
state. The condition's form is itself a consequence of the
none-needed disposition.

**Derivation chain.**

1. *The recorded corpora are projections.* G1 §2.2: each
   coded corpus of §1.2 "is T computed under that frame's
   (Σ, γ), by that file's stated derivation, over that
   file's bounded object set," and "Comparing a candidate
   state to the records is therefore always a comparison
   under §2.3."
2. *Consistency is projection-agreement.* By D4's
   quantifier ("classes consistent with the records") read
   through step 1's comparison rule: a state s is
   consistent exactly when T(s), restricted to each
   corpus's object set, is §2.3-equivalent to that
   corpus's recorded table. The assembly of D4's phrase
   with §2.2's rule is this derivation's, and is stated
   openly here (and in §6) rather than attributed to a
   single text.
3. *Equivalence preserves the identity structure.* Let s
   and s′ be equivalent over a corpus's object set, with
   β : Σ_O → Σ′_O the bijection of §2.3, β(γ(o)) = γ′(o)
   for every object o. β applied elementwise preserves
   each sequence's length; and the multiplicity of a type
   t′ = β(t) in s′ — its token count summed over the
   object set — equals the multiplicity of t in s, since
   β is a bijection on types carrying each sequence to its
   image. Hence equivalent tables have the same exercised
   type count |Σ_O|, the same sorted token-multiplicity
   profile, and the same sequence-length profile. This
   step is arithmetic on §2.3's definition; nothing else
   is imported.
4. *The recorded profiles.* From §1.2, re-counted at this
   stage from the files at this branch's tree state
   (hashes matching §1.2's pins; full output in the stage
   record): the M77 corpus — 1,669 inscriptions, 5,361
   tokens, 64 exercised codes, sorted multiplicities
   headed 541, 432, 355 and ending 5, 3, 2, 1 (one code
   occurring once; three occurring three times or fewer),
   564 single-token inscriptions; the ICIT corpus — 4,410
   inscriptions, 14,213 tokens, 713 exercised codes,
   maximum multiplicity 527, 218 codes occurring once; the
   CISI coded subset — 179 inscription sides (178
   multi-sign), 1,003 tokens, 182 exercised P-codes.
5. *Assembly.* From steps 2 and 3, every consistent
   state's table over each corpus's object set has that
   corpus's recorded identity structure; from step 4, that
   structure is the counted profile. Therefore every state
   in every class consistent with the records satisfies
   the statement. ∎

**Counted form.** Record class: Class II coded corpus
records. *Forbidden combination:* a named consistent
state whose induced table over a corpus's object set
exhibits an exercised-type count, a sorted multiplicity
profile, or a sequence-length profile different from the
recorded table's. *Counting rule:* for a named state
(§2.1), compute its table restricted to the corpus's
object set; count distinct exercised types, the sorted
multiplicity vector, and the length histogram; count the
components differing from the recorded profile. The
condition asserts the deviation count is 0 for every
consistent state. *Executed at this stage:* the recorded
side of the count — the profiles of step 4 recomputed from
the pinned files (the derivation's inputs verified at the
state read). Bringing external candidate states to the
count one by one is administration against named states,
not part of the derivation; the held-out administration of
a computed test belongs to G3's bar, which this study does
not attempt (C090-15).

**Falsifier (D4 form).** A Class II record over a corpus's
own object set, produced by that corpus's stated
derivation from its Class I sources, whose table is not
§2.3-equivalent to the pinned file — concretely, a
re-derivation of the 1,669 M77 inscriptions from Mahadevan
(1977) by the loader's stated derivation (OCR and the
sign-rank-correlation glyph mapping) that exercises 65
sign types, or that separates two tokens the pinned file
codes identically. Under the record system as pinned, the
file *is* the derivation's output (§1.2's provenance rule;
§3.8: fidelity is the derivation's assertion, checkable
against its sources); a faithful re-derivation disagreeing
with it is a record the framework declares impossible, and
its observation would refute this derivation's
application at step 4.

**Bite, stated plainly.** The condition excludes any
candidate state — any proposed sign inventory or
segmentation offered as a completion of these records —
whose classification of the surviving objects differs in
identity structure from the recorded codings: a
decipherment whose γ, applied to the M77 objects, exercises
63 or 65 signs, merges two codes the file distinguishes,
or splits one it identifies, is not a completion of the
records at all, and the count says so mechanically. The
caveat is stated as plainly: the condition's excluding
power is exactly the excluding power of consistency,
made explicit, class-level, and countable. Whether that
clears C090-9's bar — a derivation, not a regularity
fitted to the observed corpus — rests on the chain: the
statement quantifies over classes and is proved from
§2.2/§2.3 for every member of them; the corpus enters only
as D1's content (step 4), which is where a necessary
condition *for this record system* must take its records
from. This is the candidate's known pressure point, and it
is labeled here for the audit rather than argued away.

---

## 4. Candidate 3 — register-certification over the unvalidated readings: NOT DERIVED

**Attempted statement.** *Every state in the domain
leaves the readings of the signs standing at
`pending_non_sa_validation` (44), `no_validation_record`
(3), and `premise_superseded` (113) on the anchor register
uncertified by any completed validation record.*

**The chain, as far as it honestly goes.** Step 1 is a
record fact: §1.3 counts those populations at those
statuses on the register's face, and §2.4γ grounds the
indistinguishability of states differing only in those
readings in the register's incomplete validation chains.
Step 2 would require the premise that certification of a
reading consists in a completed validation record in the
register. That premise is not in D1–D3 and not in the G1
document: G1 places validation in the assertion layer
(§2.2), and §2.4γ marks its own item, in terms, "an
indistinguishability of the record system — of its
validation records — not a π-class statement." The chain
breaks at step 2: **the premise the domain does not supply
is a bridge from the register's bookkeeping state to a
property of states in projection-equivalence classes.**

**The obstruction, in full.** (a) *Form.* The attempted
statement's truth is carried by the assertion layer's
current contents, not by the states it quantifies over:
appending one completed validation record tomorrow — a
sanctioned ledger/register act over the same records —
flips the statement while every state and π stand
unchanged. D4's quantifier is over states in classes
consistent with the records; a statement whose truth-maker
is R's bookkeeping at a date is a report about R, not a
necessary condition on completions. (b) *Subsumption.*
The derivable core of the attempt — that no reading of
any sign is record-determined — is Candidate 1's clause
(step 4 there), which derives at the π level for all
signs, not only the unvalidated ones. What Candidate 3
adds beyond Candidate 1 is exactly the part that does not
derive. **NOT YET at this strength:** a necessary
condition stated over the register's validation statuses
is not derivable under the frozen G1 document, and the
missing premise is named above; what would have to change
is the G1 document itself (an amendment making validation
outcomes part of the projection), which would contradict
§2.2's frozen separation and is not this stage's to make.

---

## 5. Candidate 4 — standalone corpus regularities: NOT DERIVED as stated

**Attempted statements.** Regularities of the recorded
tables promoted directly to necessary conditions: e.g.,
"every state in the domain has exactly one sign occurring
once over the M77 objects"; "in every state, the most
frequent sign over the M77 objects accounts for 541 of
5,361 tokens."

**Obstruction.** As standalone statements, their only
derivation is enumeration of the observed corpus: they
are established over the records that happen to survive,
which is the shape C090-9's falsifier names (an empirical
regularity with a class-level label). No chain from
D1–D3 and the projection reaches them except through
Candidate 2, of which they are corollaries — each is one
component of Candidate 2's recorded profile, and inherits
its derivation there, not a derivation of its own.
Recorded here so the candidate space shows them attempted
and refused on form, not overlooked.

---

## 6. Derivation-provenance self-audit (for T202)

Every premise used in the completed chains, traced.
"Traced" means: the premise is a sentence of the frozen
G1 document (by section) or of the skeleton's D1–D3, or a
record fact counted at this stage from the records the G1
document names. No other source is used.

**Candidate 1.**

| # | Premise | Source |
|---|---|---|
| P1.1 | Knowledge of a state is exhausted by properties of its π-class | D2; G1 §2.4 preamble |
| P1.2 | π(s) = T(s) over O; π does not depend on ρ or λ; state-determined records are functions of T(s) | G1 §2.2 |
| P1.3 | Anchor and claim records are assertions about states, not π outputs; their content is what is at issue between states | G1 §2.2; confirmed §3.4 |
| P1.4 | All (ρ, λ) variants over fixed (Σ, γ) lie in one class | G1 §2.2 via §2.4β |
| P1.5 | Unexercised-inventory variants are equivalent | G1 §2.3 (as repaired, freeze F1) |
| P1.6 | Variants differing only outside O are equivalent | G1 §2.2 (operative O); §2.4δ |
| P1.7 | Class II members' derivations take glyph data + frame only (counted form) | Inspection at this stage: the two loaders of record and the ICIT OCR script, headers read first-hand |

**Candidate 2.**

| # | Premise | Source |
|---|---|---|
| P2.1 | Each coded corpus is T under its frame over its object set; record comparison is under §2.3 | G1 §2.2 |
| P2.2 | Consistency = §2.3-agreement with each recorded coding | D4's phrase, assembled with P2.1 — **this derivation's assembly, labeled** |
| P2.3 | §2.3-equivalence preserves exercised count, multiplicities, lengths | G1 §2.3 + the arithmetic shown at step 3 |
| P2.4 | The recorded profiles (step 4's figures) | G1 §1.2; re-counted at this stage from the pinned files, hashes matching |
| P2.5 | No frame is the absolute frame; cross-frame identity is partial and crosswalk-mediated (the condition's per-corpus form) | G1 §3.2, §2.4ε |

**Physics-premise check.** No step in either chain cites
a physics result. The occasion for Candidate 1 was the
plan's own third hunting ground ("what a record system
with this provenance structure cannot certify about its
own completions") and the skeleton's D4/D5 shape; the F0
no-estimator theorems were not consulted as premises and
no step needs one — remove the physics instantiation
entirely and both chains stand as written. Candidate 2's
occasion was the plan's first hunting ground. Occasion is
not premise, per D-090-3.

**Labeled boundaries (not gaps in the chains; the places
the audit should press).**

1. *Candidate 1's certification clause rests on P1.3* —
   the frozen document's architectural disposition that
   assertions never determine. That is a stated rule of
   the G1 document and so within D-090-3's discipline;
   it is also the premise doing the most work in the
   chain, and it is flagged as such.
2. *Candidate 1's counted form does not enumerate
   Classes III/IV* — by P1.3's disposition, stated in §2,
   not by inspection. An auditor who holds that the count
   must run over all five classes will find the assertion
   classes' separation behavior governed by a rule rather
   than a count; the rule and its source are named.
3. *Candidate 1's falsifier refutes through the basis* —
   its observation would show §2.2's factoring failing
   for the enlarged record system, which is D4's "refute
   the derivation's application." A stricter reading —
   a falsifier consistent with the whole G1 document that
   refutes the condition alone — is not available for a
   condition whose content is the projection's factoring,
   and the difference is recorded, not smoothed.
4. *Candidate 2's consistency assembly (P2.2)* and its
   *bite caveat* (§3) are the candidate's pressure
   points, labeled in place.

**What this record does not establish.** That the G2
outcome is DERIVED — that declaration is T202's, on the
audit this record is written to face. That either
condition is important beyond its stated bite. Anything
about the Indus script itself: no claim's status, stage,
or score is touched by this stage, and the ledger is
untouched (C090-13).
