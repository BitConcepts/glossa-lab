# The derivation audit — Spec 090, Stage S2, task T202 (2026-11-04)

**Scope.** The audit of the G2 derivation record
(`records/g2-derivation.md`) and its declaration of the G2
outcome, executed by a worker other than the deriver under
the plan's separation rule, on branch
`feat/090-s2-g2-derivation` at the deriver's head `adbdf704`.
This record is the audit act: the five attacks, each driven
to a verdict on evidence; the independent re-verifications;
and the stage outcome declared on them. Broken candidates
are not repaired inside an audit (plan, Stage 2); none here
needed repair to be judged, and none was repaired.

**Basis, verified by the auditor before any attack.**
`records/g1-document.md` on this branch: SHA-256
**4f2018f40c9ccaf0811cd7661b0c9e1ebd840c7e014d954f778c42edef27efc2**,
34,226 bytes — recomputed by me from the committed file
and matched against `records/stage-s1-freeze-record.md`.
The derivation therefore runs against frozen G1 v1.1, as
C090-8 requires; every "§x.y" citation below is to that
frozen text, and every quotation was checked against it.
The skeleton copy hashes to its package pin (a66ffe4f…).
Read in full for this audit: spec.md, claims.md
(C090-8..11 govern; C090-13..15 bound), plan.md (Stage 2),
tasks.md (T201, T202), the skeleton (D1–D5), the frozen G1
document, the S1 records (adversarial and freeze, for the
F1 repair's exact scope and the F9 clause), the derivation
record, and the stage S2 record. The branch's diff against
origin/main is documents only (`g2-derivation.md`,
`stage-s2-record.md`, `tasks.md`); the ledger is untouched
(C090-13), verified from the diff, not from the records'
say-so.

---

## Attack 1 — premise tracing (the D-090-3 discipline, re-run independently)

**Method.** Every step of both completed chains re-walked;
the premise each step actually consumes identified and
located in D1–D3 or in the frozen G1 document. The
deriver's self-audit (§6 of the derivation record) was
treated as a claim to test, not as evidence; the
physics-premise check was re-run by reading both chains
end to end for any physics content.

**Candidate 1, step by step.**

- *Step 1* consumes D2 verbatim — "Everything the record
  system can ever know is a property of the equivalence
  classes of pi, never of the states inside a class" —
  carried into the domain at §2.4's preamble ("Everything
  the record system can ever know is a property of the
  equivalence classes of π"). Present.
- *Step 2* consumes §2.2 verbatim: "π(s) = T(s)"; "The
  projection does not depend on ρ or on λ"; "Every further
  record the state determines … is a function of T(s) and
  therefore of π(s), not an addition to the projection."
  Present.
- *Step 3* consumes §2.2 verbatim: anchor records and
  claim lines "are not outputs of π: they are assertions
  about states … their content is what is at issue between
  candidate states, never a projection of any one of them,"
  confirmed at §3.4 ("claim standing, not given standing").
  The step's gloss — that determination runs only through
  the projection — is the conjunction of that sentence, D2,
  and §1's class definitions (Classes I and V hold object
  and snapshot content; neither is a function of any
  candidate state). It is the chain's heaviest premise,
  exactly as the deriver's boundary 1 labels it; it is a
  stated rule of the frozen document, so it is inside
  D-090-3's discipline, and it is flagged here again so the
  outcome record inherits the flag.
- *Step 4* consumes §2.2 with §2.4β: "For fixed (Σ, γ),
  every (ρ, λ) variant of a state lies in one equivalence
  class: π does not depend on them (§2.2)." Present (its
  strength is attack 2's question, answered there).
- *Step 5* consumes §2.3 as frozen: a state "differing
  from another only by such an unexercised inventory
  member — an added sign, or a distinction no token on O
  draws — has the same exercised inventory and the same
  table, and is equivalent to it." The citation's "as
  repaired at the freeze" points at this frozen text (the
  F1 repair, freeze record); the premise lives in v1.1
  itself, not in the repair act. Present.
- *Step 6* consumes §2.2's operative O with §2.4δ:
  "States that agree on every object in O but differ on
  objects outside O … are equivalent, by the definition of
  π over O (§2.2)." Present.
- *Step 7* is assembly of steps 1–6 plus step 2's function
  clause; it imports nothing.

**Candidate 2, step by step.**

- *Step 1* consumes §2.2's closing paragraph verbatim:
  each coded corpus "is T computed under that frame's
  (Σ, γ), by that file's stated derivation, over that
  file's bounded object set," and "Comparing a candidate
  state to the records is therefore always a comparison
  under §2.3." Present.
- *Step 2* is the chain's one assembly not quoted from a
  single text: D4's quantifier phrase ("classes consistent
  with the records") composed with step 1's comparison
  rule to define consistency as §2.3-agreement with each
  recorded coding. The deriver states the assembly openly
  in the chain and in self-audit premise P2.2 ("this
  derivation's assembly, labeled"). G1 defines no second
  consistency notion, and §2.2's comparison rule supports
  no other reading: the assembly is an inference over
  permitted sources, not an imported premise. (What the
  assembly makes the condition *worth* is attack 3's
  question, decided there — on strength, not on
  traceability.)
- *Step 3* consumes §2.3's definition plus arithmetic,
  and nothing else. I verified the arithmetic in both
  directions: β applied elementwise preserves each
  sequence's length; a bijection on types carries each
  type's token count to its image's, so the sorted
  multiplicity profile transfers; β's domain and codomain
  are the exercised inventories, so their counts agree.
  No corpus fact, frame fact, or crosswalk enters the
  step. Present, and exactly as strong as stated.
- *Step 4* consumes §1.2's record facts, re-counted by
  the deriver at the stage and re-counted again by me
  (verification annex below). Present, and exact.
- *Step 5* is assembly of steps 2–4. Its per-corpus form
  rests on §3.2/§2.4ε (P2.5), both present in the frozen
  text.

**Physics-premise check, re-run.** No step of either chain
cites a physics result. No F0 theorem, no causal-set
identifiability result, no separator constant, no
dimensionful scale appears anywhere in the chains. The
only physics-adjacent text in the derivation record is
the self-audit's occasion paragraph (the plan's hunting
grounds; the F0 pattern named as occasion) — outside both
chains, and removable without touching any step, which is
exactly what D-090-3 permits. No step cites the scoping
note, the plan, or any S1 stage record as a premise.

**Verdict: NOT SUSTAINED.** Every premise of both
completed chains traces to D1–D3 or to the frozen G1
document; the two labeled assemblies (step 3's gloss in
Candidate 1; P2.2 in Candidate 2) are inferences over
cited text, labeled in the record, not premises smuggled
from outside the basis.

---

## Attack 2 — Candidate 1's strength

**(a) The quantifier work.** The statement claims its
variation for *every* state. I tested each dimension
against the frozen definitions, pressing for a state of a
special shape where the variation fails.

- *(ρ, λ).* §2.1 defines the state as the four-tuple
  (Σ, γ, ρ, λ) with ρ "partial by definition" and no clause
  tying ρ to γ; λ is an independent component, including
  the value *no identification proposed*. For an arbitrary
  s, the tuples (Σ, γ, ρ′, λ) for any other partial ρ′ and
  (Σ, γ, ρ, λ′) for any other λ′ are therefore states
  under §2.1, and §2.4β places them in s's class. The
  counterexample the audit was charged to construct — a
  state "whose ρ is forced by its γ on the exercised
  inventory" — cannot be built inside G1's terms: forcing
  would require a stated rule deriving ρ from γ, §2.1
  contains none, and §2.2's independence of π from ρ is
  the system's own bar against importing one. (That in
  practice only one decipherment may have been *proposed*
  over a given γ is a fact about the history of proposals;
  the condition quantifies over states, not over proposed
  states.) The chain answers the counterexample at step 4,
  from the definition of the state space itself.
- *Unexercised inventory.* For an arbitrary s, adjoining
  to Σ a sign no object of O exercises yields a distinct
  state with the same exercised inventory and table,
  equivalent under §2.3's closing passage (the F1 repair,
  verified in the frozen text). The construction needs no
  property of s; it works even when s's exercised
  inventory exhausts every frame's.
- *Off-set classification.* For an arbitrary s, a state
  differing only in γ's assignments on glyph streams of
  objects outside the operative O has the same table
  (§2.2) and is equivalent (§2.4δ). This dimension is a
  genuine state difference because §2.1 defines γ over
  every inscribed object, not only over O; §2.4δ grounds
  O's being a proper survival subset ("the system holds
  15,508 snapshot object records … and no record of any
  class enumerates what did not survive").

All three dimensions hold for an arbitrary state, not
only for states of a special shape. One boundary, named
so the outcome record states the condition at its true
strength: the variation established is *existence inside
the class* — non-singling-out. The condition assigns no
plausibility to the variants, and neither does §2.4 ("this
account assigns no plausibility, likelihood, or standing
to any state inside a class"). That is a bound on what
the condition means, not a defect in its derivation.

**(b) The counted form, recounted independently.** The
deriver counted **0 of 3** Class II derivations taking a
reading assignment as an input. I re-read all three
derivations of record in full and recount:

- *M77* — loader of record `backend/glossa_lab/data/
  indus_m77.py`, header: the flat file was produced from
  Mahadevan (1977) "by OCR and a sign-rank-correlation
  glyph mapping"; the loader parses digit tokens from the
  file. Inputs: the concordance's glyph data and the M77
  frame. No reading assignment or language identification
  appears as an input anywhere in the file.
- *CISI subset* — loader of record `backend/glossa_lab/
  data/indus_cisi.py`, header and code: the subset is the
  mayig digitization of the CISI volumes in Parpola
  P-codes; the loader consumes the digitized grapheme ids.
  Inputs: the published texts and the Parpola frame. No
  (ρ, λ) input.
- *ICIT* — `backend/scripts/ocr_icit_corpus.py`, read in
  full: inputs are Fuls (2023)'s two PDF books, OCR'd
  (Tesseract); sign sequences are extracted as digit codes
  and, where reconstructed, ordered by the catalog's
  positional rates — the script's own method note states
  "Ordering is probabilistic (initial_rate -> first,
  terminal_rate -> last)" — which are statistics of the
  recorded data itself. Two near-misses examined and
  closed: the inscription headers carry a direction field
  (R/L), which is source metadata about glyph-stream
  order — frame-level record content, not a candidate
  state's ρ or λ; and the positional rates are functions
  of the records, not readings. No sign→value mapping and
  no language identification is an input anywhere in the
  script.

**Recount: 0 of 3, confirmed.** The forbidden combination
does not occur in the class as it stands. (The ICIT
reconstruction's fidelity is a §3.8 provenance property of
that record; the counted form asks about input types, and
on input types the count is exact.)

**(c) The falsifier's honesty.** The falsifier: a Class II
coded corpus record, admitted with its derivation named,
whose stated derivation computes its sequence table from
glyph streams *and* a reading assignment (the record's
instance: a corpus coded by syllabic values under a named
decipherment, its identity rule referencing that
decipherment's ρ). Three tests:

- *Admissible?* Class II's provenance rule (§1.2) admits a
  coded record that "exists only with its derivation
  named," its frame "a sign inventory with a segmentation
  and identity rule" (§2.1). Nothing in the admission rule
  requires the derivation to be ρ-free — ρ-freedom is what
  the condition asserts of the class's present members,
  not an admission criterion. A decipherment-keyed corpus
  has a named derivation and a frame; the system admits
  it. Yes.
- *Recognizable?* A derivation of record is a stated,
  inspectable text; one naming a decipherment's reading
  assignment as an input is recognizable on its face — by
  the same inspection that executed the 0-of-3 count. Yes.
- *Genuinely observable, or defined away?* Corpora coded
  under a proposed decipherment are a real genre of
  artifact, not a definitional phantom: nothing about the
  record kind is self-contradictory, and its production
  requires no permission from the framework. The
  through-the-basis character the deriver labels (§6,
  boundary 3) is real and I state it in the audit's own
  terms: the falsifier's observation would refute the
  derivation's *application* — D4's exact phrase — by
  showing §2.2's factoring failing for the record system
  as enlarged; it would not refute the condition as a
  statement about the system as frozen, because a system
  enlarged past the frozen projection is a new basis (a
  G1 amendment act under D-090-1), not a counterexample
  inside this one. For a condition whose content *is* the
  projection's factoring, this is the strongest falsifier
  D4's form admits: the stricter demand — a falsifier
  consistent with the whole frozen G1 that refutes the
  condition alone — would make every consequence of D2
  unfalsifiable by construction, and D4 does not ask for
  it. The deriver labeled the boundary instead of hiding
  it; the label is accurate.

**Verdict: NOT SUSTAINED.** The quantifier work covers
arbitrary states in all three named dimensions (the
pressed counterexample is answered from §2.1/§2.3/§2.4 as
frozen); the 0-of-3 count re-executes independently; the
falsifier is an admissible, recognizable, in-principle
observable record whose observation refutes the
derivation's application in D4's stated form.

---

## Attack 3 — Candidate 2's bite

**Verification legs first.** (i) *Recomputation.* I
recomputed the recorded profiles first-hand from the
files at this branch's tree state (full figures in the
annex): M77 — 1,669 inscriptions, 5,361 tokens, 64
exercised codes, maximum multiplicity 541, exactly one
hapax, and the full 64-component sorted multiplicity
vector identical to the stage record's; ICIT — 4,410
inscriptions, 14,213 tokens, 713 exercised codes, maximum
multiplicity 527, 218 codes occurring once; CISI subset —
179 inscription sides (178 multi-sign), 1,003 tokens, 182
exercised P-codes. Both flat files hash to §1.2's pins
(878fd223…, c8839fd3…). Every figure in step 4 of the
chain reproduces. (ii) *The preservation step.* Step 3 is
arithmetic on §2.3's β and nothing more — verified in
attack 1; no hidden import does work there.

**The decision.** The attack's contention: the excluding
power is consistency's, so the candidate is a consistency
property of any record system wearing domain dress, not a
necessary condition *of this domain* under D4 — and its
falsifier polices file custody, not decipherment states.
Decided in three parts:

- *Form.* D4 defines a necessary condition *for a record
  system*: N "holds of every state in every
  projection-equivalence class consistent with the
  records." Candidate 2's statement has exactly that form
  and its chain proves it from §2.2/§2.3 for every member
  of those classes; no candidate state was sampled and no
  regularity was fitted — the corpus enters only at step
  4, as D1 content, which is where a condition *for this
  record system* must take its records from. This is the
  derivation Candidate 4 lacks (attack 4): the profile's
  components as standalone statements have enumeration as
  their only route, while the class-level statement has a
  proof. Form: D4-conformant (C090-9).
- *Where the bite comes from.* The contention's factual
  core is correct, and the deriver states it in the
  record's own bite paragraph: the excluding power *is*
  consistency's. But consistency here is not a definition
  chosen to make the theorem true: §2.2's closing
  paragraph fixes the only comparison between a candidate
  state and the records the frozen system affords
  ("always a comparison under §2.3"), so there is no
  second, weaker consistency notion the condition could
  be hiding behind. And the content is not domain-free:
  the enforced profile is this corpus's counted identity
  structure (64 exercised types under that multiplicity
  vector; 713 types with maximum 527; 182 P-codes), and
  the exclusions it makes are exclusions of decipherment
  hypotheses *as completions of these records* — a
  proposed γ exercising 63 or 65 types over the M77
  objects, or merging two codes the file distinguishes,
  is excluded mechanically, before any particular
  decipherment is proposed or examined. A consistency
  property of any record system whatsoever carries no
  domain numbers and excludes no domain hypothesis; this
  condition carries both. It is a necessary condition of
  the domain in D4's sense — with its strength exactly
  what consistency is worth, neither more nor less.
- *The falsifier.* Its observation — a faithful
  re-derivation of a corpus from its Class I sources, by
  its stated derivation, non-equivalent to the pinned
  file — would refute the derivation's application at
  step 4: the pinned file is, by §1.2's provenance rule,
  the derivation's output of record, and §3.8 makes
  fidelity "exactly what that provenance asserts and what
  a re-derivation against the Class I sources would
  check." So the observation strikes a premise that is
  itself a record of the system, not a claim about states
  directly; and its most natural reading on arrival would
  be a corpus-fidelity finding, after which the condition
  re-derives against the corrected table with its form
  intact. The falsifier is D4-conformant in form — a
  record the framework declares impossible, whose
  observation refutes the derivation's application — and
  the audit records its true weight: it guards the
  identity of the recorded tables, and through them the
  condition's application, rather than testing a state
  directly.

**Verdict: NOT SUSTAINED as a refutation of Candidate 2's
derivedness; the strength finding it presses is confirmed
and is carried into the declaration.** Candidate 2 stands
as derived — at *consistency strength*: its necessity is
the necessity of agreement with the recorded tables under
the frozen projection, made explicit, class-level, and
countable. The deriver's own caveat is the correct
statement of that strength, and the declaration below
adopts it verbatim in effect, so the outcome record
cannot over-read the candidate. (C090-9's "does not
establish" line anticipates exactly this: the claim binds
form and derivation; the bite is stated plainly, here and
in T301.)

---

## Attack 4 — the refusals

**Candidate 3 (register-certification).** Two checks.
(i) *The bridge premise is absent.* I searched the frozen
G1 document and D1–D3 for any premise equating
certification of a reading with a completed validation
record in the register. None exists. D1–D3 do not mention
validation. G1 places the register in the assertion layer:
§1.3 defines its validation statuses as register content;
§2.2 holds anchor records to be "assertions about states
… never a projection of any one of them"; §3.4 gives
imported identifications "claim standing, not given
standing." A probe for the bridge in §3.4's audit
dispositions — the one place it could hide — finds
standings of assertions, which is the assertion layer
again. The premise the chain needs at its step 2 is
supplied by neither the skeleton nor the frozen document.
(ii) *§2.4γ's character.* The frozen text closes item γ:
"Item γ is an indistinguishability of the record system —
of its validation records — not a π-class statement: item
β already places every reading difference inside one
π-class, and γ names what the register's validation
chain, as distinct from the projection, cannot separate."
(The clause is the freeze's F9 clarification, present in
v1.1 as frozen.) The deriver's reading is the document's
own. The deriver's form argument also holds on my check:
the register's statuses change by appended acts over the
same records (§1.3's stage histories record transitions;
§1.4 states the append discipline for the ledger), so the
attempted statement's truth-maker is the register's
bookkeeping at a date, not the states its quantifiers
range over — and its derivable core is, exactly as the
record says, Candidate 1's step 4 at the π level, for all
signs rather than only the unvalidated ones. The break is
real, at the step named, for the reason named.

**Candidate 4 (standalone regularities).** Each named
regularity is a component of Candidate 2's recorded
profile, verified against my own recount: "exactly one
sign occurring once over the M77 objects" is the profile
vector's hapax count (1, recomputed); "the most frequent
sign accounts for 541 of 5,361 tokens" is its head (541
of 5,361, recomputed). As corollaries of Candidate 2 they
inherit its derivation; as standalone necessary
conditions their only route is enumeration of the
observed table, which is the shape C090-9's falsifier
names. The refusal on form is correct.

**Verdict: NOT SUSTAINED.** Both refusals are right on
the frozen basis: Candidate 3's break is a genuinely
absent premise (not a step the deriver failed to find),
and Candidate 4's disposition (corollaries, not
derivations) is exact. A refusal that should have been a
derivation would be a defect of the same order as the
reverse; neither is present.

---

## Attack 5 — form

- *No verdict beyond the audit's declaration.* The
  derivation record speaks in the deriver's voice
  (chains complete / not derived), expressly defers the
  outcome ("the G2 outcome (DERIVED / NOT YET) is
  declared on that audit, not here"), and closes with
  what it does not establish. No INSTANTIATES or ANALOGY
  language, no G1 verdict, no study-level outcome appears
  in it. The stage record's claim assessments are
  expressly "deriver's side … for T202's audit and T301
  to settle," not dispositions of record.
- *Counted forms in the skeleton's terms.* Candidate 1:
  record class (Class II coded corpus records), forbidden
  combination (a member whose stated derivation takes a
  reading assignment or language identification as an
  input — equivalently, a sequence table not computable
  from glyph streams under a frame alone), counting rule
  (enumerate the class's members; inspect each derivation
  of record for its inputs; count). Candidate 2: record
  class (Class II), forbidden combination (a named
  consistent state whose induced table over a corpus's
  object set deviates in exercised-type count, sorted
  multiplicity profile, or sequence-length profile),
  counting rule (compute the named state's restricted
  table; count the components differing from the recorded
  profile). Both state class, combination, and rule.
- *No S3 content.* No outcome record material, no report
  act, no per-claim dispositions of record; no G3
  administration (both counted forms were executed only
  on their recorded side, as the stage record's departure
  2 states — input inspections and profile recomputations,
  which are the derivations' own input verifications);
  no G4 or G5 content; no machinery, no gate class, no
  ledger line (diff verified: documents only).

**Verdict: NOT SUSTAINED.** The record keeps the form
the spec requires; the declaration below is this audit's
act and the first verdict the stage carries.

---

## Verification annex — profiles recomputed first-hand

From the files at this branch's tree state (both flat
files hash to §1.2's pins: M77 878fd223…, ICIT
c8839fd3…), counted by me at the audit:

| Corpus | Inscriptions / sides | Tokens | Exercised codes | Max multiplicity | Hapax | Other checks |
|---|---|---|---|---|---|
| M77 | 1,669 | 5,361 | 64 | 541 | 1 | ≤3 tokens: 3 codes; single-token inscriptions 564; lines >14 tokens: 25; codes run 003–920; full sorted multiplicity vector identical to the stage record's 64-component vector |
| ICIT | 4,410 | 14,213 | 713 | 527 | 218 | ≤3 tokens: 386 codes; single-token inscriptions 946 |
| CISI subset | 179 (178 multi-sign) | 1,003 | 182 | — | — | computed from `indus_cisi_corpus.json`'s inscription list; the file's own header figures agree (179 / 1,003 / 182) |

Every figure the chains consume from §1.2 and from the
stage record's recount reproduces exactly.

## Gate on the final tree

The audit touches no ledger line and no gate input. The
gate was run both modes on this PR's final tree (this
record and the T202 tick included) and the settling
canonicals verified:

- full: `summary: 25 PASS / 0 FAIL / 1 NOT-RUN   RESULT: PASS`
- --regen: `summary: 28 PASS / 0 FAIL / 0 NOT-RUN   RESULT: PASS`
- `run_settling.py verify-canonicals`: **6/6 registered
  canonicals reproduce**

— identical to the adoption's, S1's, and T201's gate of
record; the standing profile is unchanged.

---

## The declaration — G2 outcome

On the audit above, the stage outcome is declared:

### G2: DERIVED

Two necessary conditions survive the audit, each stated
in D4's form with its falsifier:

**Condition 1 — the non-certification condition**
(Candidate 1, derived in 7 steps; attacks 1 and 2 not
sustained). *Statement:* every state in the domain is
projection-equivalent to states that differ from it in
reading assignment and language identification, in
sign-inventory members that no object of the record
system exercises, and in classification of objects
outside the surviving record set — so no record of the
system, and no test computed from the records,
distinguishes a state from every other member of its
projection-equivalence class. *Falsifier:* a Class II
coded corpus record, admitted to the record system with
its derivation named, whose stated derivation computes
its sequence table from glyph streams *and* a reading
assignment; its observation would refute the derivation's
application (the factoring of π through γ alone, §2.2) in
D4's form. *Strength, as audited:* the domain's
no-determination theorem under the frozen projection —
its load-bearing premise is §2.2's disposition that
assertions never determine (attack 1, step 3), and its
falsifier refutes through that basis (attack 2c); both
bounds are on the record, not smoothed.

**Condition 2 — the recorded-profile condition**
(Candidate 2, derived in 5 steps; attacks 1 and 3 not
sustained). *Statement:* every state consistent with the
records induces, over the object set of each coded corpus
in the record system, that corpus's recorded identity
structure: the same number of exercised signs, the same
token-multiplicity profile, and the same sequence-length
profile, up to relabeling. *Falsifier:* a faithful
re-derivation of a coded corpus from its Class I sources,
by that corpus's stated derivation, whose table is not
§2.3-equivalent to the pinned file; its observation would
refute the derivation's application at its recorded-
profile premise. *Strength, as audited:* **consistency
strength** — the condition's necessity is the necessity
of agreement with the recorded tables under the frozen
projection, made explicit, class-level, and countable
(attack 3). It is declared derived at exactly that
strength; the outcome record must not state it stronger.

Candidates 3 and 4 stand **NOT DERIVED**, their
obstructions verified by attack 4: Candidate 3's bridge
premise (certification as a completed validation record)
is absent from D1–D3 and the frozen G1 document, and its
derivable core is Condition 1's reading clause;
Candidate 4's regularities are corollaries of Condition
2's profile, refused as standalone conditions on
C090-9's form ground. No candidate was repaired inside
this audit; no obstruction was softened.

**Claims on this audit's evidence** (dispositions of
record are T301's act): C090-8 holds (attack 1); C090-9
holds for both declared conditions, with Condition 2's
strength as stated (attack 3); C090-10 holds for both
(attack 2c for Condition 1; attack 3 for Condition 2);
C090-11 is executed for Candidates 3 and 4 with the
obstructions named and verified (attack 4); C090-13
holds (documents-only diff, ledger untouched).

*T202's "does not establish" line (from tasks.md), which
survives into this record:* that a DERIVED outcome makes
the conditions important — the audit settles soundness
and form; the bite is stated above at its audited
strength (Condition 1's is the no-determination theorem;
Condition 2's is consistency made countable), and the
outcome record (T301) states it plainly for the study.
This declaration is the per-stage outcome G2: DERIVED;
the study-level outcome and the independent reader's
verdict over the full G1–G5 bar are not this record's to
give (spec.md, judging protocol; C090-16).

**AI disclosure:** executed by an AI agent (Muse, via
Muse) at the direction of Tristen Pierson, per
constitution sec. VI.
