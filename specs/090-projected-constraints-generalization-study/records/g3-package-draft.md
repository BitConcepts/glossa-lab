# Stage G3 package (DRAFT) — one computed separator, validated on held-out records

**Spec:** 090 — Projected-Constraints Generalization Study.
**Stage:** G3, proposed as a stage amendment to Spec 090
(decision D-090-5 in this package).
**Status: DRAFT — prepared 2026-11-05 under the owner's
commission of 2026-11-05 ("Commission G3 now"). Not ratified.
No separator has been computed; no profile has been computed
over any held-out record; nothing in this package is a result.**
On ratification this package is amended into the spec's records
with the ratification act recorded beside it, in the pattern of
the ratification record of 2026-11-04.

**Basis.** The skeleton document of record in this spec's
records (AXIOVEX/vexa commit 88839493, SHA-256 a66ffe4f…):
definition D5 (a separator) and the G3 item of the bar —
"At least one separator is computed in that domain and shown
to distinguish cases the domain's practitioners agree are
distinct, on data not used to design the separator." The G1
document, frozen at v1.1, SHA-256
4f2018f40c9ccaf0811cd7661b0c9e1ebd840c7e014d954f778c42edef27efc2
(`records/stage-s1-freeze-record.md`). The G2 derivation
record and its audit (Condition 1 DERIVED at full strength;
Condition 2 DERIVED at consistency strength; Candidates 3
and 4 not derived, obstructions verified). The study outcome
record (`records/study-outcome-2026-11-04.md`), §4 of which is
this stage's design constraint, quoted in §1 below. Decisions
D-090-1..4 bind this stage as they bound G1/G2: in particular
D-090-3 (derivation provenance — steps from the G1 document's
terms and D1–D3 only; physics may occasion, never premise)
and D-090-4 (the outcome is reported to the VEXA chat
whatever it is; extended to this stage as decision D-090-10).

**Source-version note.** VEXA Amendment A2 (ratified
2026-11-05) folds skeleton clarifications from IMP-0011/0012
into the framework's skeleton copy. This package is drafted
against the skeleton copy of record in this spec's records
(commit 88839493), the version the G1 document and the G2
derivation answered to; per the study's source discipline a
revision is a new source version and the study records which
version it answered. The clarifications reinforce this
package's design (IMP-0011 names the bookkeeping species of
statement — Candidate 3's refusal generalized; IMP-0012
grades derived conditions — G2's practice). If ratification
directs this stage to answer to the A2-amended skeleton
instead, that direction is recorded and the package's
citations are re-pointed before the freeze; nothing in the
separator's definition turns on the difference as far as
this draft can determine.

---

## 1. What G3 must do, and the trap it must not fall into

G3 is the first bar item that asks the skeleton's machinery
to *do* something measurable in the domain: compute a
quantity over records and show it distinguishing cases. The
study outcome record (§4) states the trap precisely, and
this package takes it as a design constraint, not a remark:

> "Condition 2's counted form is a template for a
> separator's administration (compute a named state's
> restricted table; count deviations from the recorded
> profile) — but it is **not** a separator: for every
> consistent state its deviation count is zero by
> construction, so it separates nothing among consistent
> states. A G3 attempt must find a quantity that actually
> varies across classes and validate it on records the
> derivation did not use. Candidate 3's refusal is its
> standing warning: quantities computed over register
> bookkeeping vary with the bookkeeping, not across
> π-classes, and will not be separators."

Three consequences, all binding on §2:

1. The separator is a function of a *table* (G1 §2.2's T),
   never of the register, the ledger, or any bookkeeping
   state. Any component whose value can change when a
   validation record is appended, over the same tables, is
   disqualified in advance.
2. The separator must be *constant on each
   projection-equivalence class* (D5's invariance clause)
   and *non-constant across the classes it claims to
   separate*. Both directions are mechanical, and the
   administration tests both (§5's controls test the
   first; §5's distinct cases test the second).
3. The validation records must be records no G1/G2 step
   computed over. §3 enumerates them and the exclusions,
   with the boundary of "used" stated exactly.

## 2. The separator, defined from the G1 document's terms

**Definitions used, and nothing else.** A *coded record
set* C is a bounded set of objects together with, for each
object, its recorded sequence under a named frame — a
recorded table in the sense of G1 §2.2, of the same kind as
the Class II corpora of §1.2. A *named state over C* is a
state in G1 §2.1's sense presented in the naming mode
§2.1 admits for record-based rules: a relabeling, a split
or merger of codes, or a re-segmentation, stated as a rule
over C's recorded sequences, computing the (Σ, γ)
assignment itself. For a named state s over C, T_C(s) is
the table the rule induces on C's objects; for the recorded
coding itself, T_C is the table as recorded.

**The profile.** For a table T over an object set O, the
*identity-structure profile* P(T) is the tuple

> P(T) = ( |Σ_O(T)| , M(T) , L(T) , X(T) , B(T) )

where, with all counts taken over O:

- **|Σ_O(T)|** — the exercised inventory size: the number
  of types γ assigns to at least one token on O (G1 §2.3's
  Σ_O, counted).
- **M(T)** — the sorted token-multiplicity vector: the
  multiset of per-type token counts, sorted descending
  (G2 Candidate 2's "sorted token-multiplicity profile").
- **L(T)** — the sequence-length histogram: the multiset
  of per-object sequence lengths, as a count per length.
- **X(T)** — the positional spectrum: the multiset, over
  exercised types t, of the triple (initial(t), final(t),
  medial(t)) counting t's tokens in first, last, and
  interior positions of their sequences (a token in a
  one-token sequence is both initial and final and counts
  in both; the rule is stated here so the freeze does not
  improvise it).
- **B(T)** — the adjacent-pair spectrum: the multiset of
  counts of adjacent ordered type pairs (t, u) over all
  sequences, zero counts excluded.

**The separator.** The separator S is the profile map P
together with its comparison: two named states s, s′ over
the same record set C are **separated over C** exactly
when P(T_C(s)) ≠ P(T_C(s′)), componentwise; a record set's
own separator value is P of its recorded table. S is a
computable test over records in D5's sense: every component
is a finite count over a finite table.

**Why S is a separator in D5's form, and not Condition 2
restated.** (i) *Invariance inside a class.* If s ~ s′
under G1 §2.3, the bijection β of §2.3 carries each
sequence of T_C(s) to the corresponding sequence of
T_C(s′); β therefore preserves each sequence's length,
each type's multiplicity (β is a bijection on types),
each type's positional triple (β carries positions with
tokens), and each adjacent pair's count (β carries pairs
to pairs). So P(T_C(s)) = P(T_C(s′)): P is constant on
every π-class. This is G2 Candidate 2 step 3's arithmetic,
extended componentwise; it imports nothing else.
(ii) *Variation across classes.* P is defined from a
table, not against one: unlike Candidate 2's deviation
count — which measures a state against a recorded profile
and is zero for every consistent state — P takes whatever
value a table's identity structure gives it, and two
tables whose identity structures differ in any component
have different profiles. The classes S separates are
exactly the classes whose identity structures differ in
exercised count, multiplicity shape, length shape,
positional shape, or adjacency shape. (iii) *No
bookkeeping.* Every component is a function of T alone;
appending a validation record, a claim line, or a
crosswalk changes no component over the same table.

**The named limit (coarsening).** P is a coarsening of the
identity structure, not the structure itself: two
non-equivalent tables can share a profile (their identity
structures differing only in which specific types carry
which multiplicities, in arrangements all five components
are blind to). S therefore does **not** separate every
pair of distinct classes, and this package does not claim
it does. What the bar asks is that S be *shown to
distinguish* the frozen agreed-distinct cases of §4 — a
claim about those cases, discharged or refuted by the
administration, not a claim about all class pairs. If a
frozen distinct-case pair lands inside the coarsening
(same profile), the stage outcome is NOT YET with that
obstruction named (§6); the components may not be extended
mid-run to catch it (claim C090-21).

**Provenance (D-090-3).** Every definition above is G1
v1.1's (§2.1, §2.2, §2.3) or an arithmetic consequence of
§2.3 stated in place; the skeleton contributes D5's form
alone. No physics result — no F0 theorem, no separator
constant, no counting law — is a premise anywhere in this
section. The physics instantiation's separator counting
law is the *occasion* for attempting G3 at all; S has no
counting law, and this package says so in D5's own terms:
the domain, at this stage, has a separator without a
counting law, and whether the number of independent
profile components grows with the record system is not
claimed, tested, or needed for the bar as stated.

## 3. The held-out discipline

**The untouched criterion, stated exactly.** A record set
is *held out* for this stage when no step of the G1
document's drafting, the adversarial pass, the G2
derivation, or the G2 audit computed a table, a profile,
or a per-record quantity over it. Aggregate census lines
that G1 §1.5 states about a file as a whole (its record
count, its source-system counts, its distinct-code-string
count) are *named uses*, bounded here: they are population
facts about the file, not computations over the records
the stage will extract, and §3.1's freeze must state the
extraction rule so the extracted set is identified by rule,
not by the census. Where a set's status under this
criterion is doubtful, the set is excluded, not argued in.

### 3.1 Primary set H1 — the snapshot's indusscript-m77 text-code records

The corpus snapshot (Class V, G1 §1.5;
`glossa-corpus/indus/exports/indus_research.jsonl`,
canonical SHA-256 08fc96c8…) holds 15,508 object records
from five source systems. H1 is the subset of records
whose source system is `indusscript-m77` (2,906 records at
the G1 census) and whose `canonical_grapheme_ids` list is
non-empty — that list, as recorded, is the record's sign
sequence in the Mahadevan 1977 scheme, and it (not the
diplomatic text string, and not the file's
`sign_instance_count` field, which disagrees with the
list's length on sampled records) is what the extraction
takes as the sequence. *Why it qualifies:* the G1 document cites the
snapshot only in §1.5's census lines (record counts,
source-system counts, 2,465 distinct code strings, 535
distinct sign codes, crosswalk coverage) — file-level
populations, none computed over H1 as a table; the G2
derivation does not mention the snapshot's records at
all, and the G2 audit mentions them only to quote
§1.5's census line and §1's class definitions (the
derivation's counted forms run over the three
Class II corpora only). No G1/G2 step has seen H1's
sequence table, its multiplicities, or its lengths.
*Named weakness, carried openly:* H1's objects may overlap
the M77 flat file's 1,669 inscriptions (both descend from
the 1977 concordance). The untouched criterion above is
about computation, not object identity, and it holds
either way; but the overlap is a quantity a reader will
weigh, so the freeze (T402) must measure and publish the
object overlap between H1 and the flat file's object set,
by the records' own identifiers, and the outcome record
must carry the number.

### 3.2 Considered and excluded — the Laursen corpus

The Laursen (2010) Table 1 corpus as held by the program
(intake of record 2026-10-26; 121 rows: Gulf Type 92,
Gulf INDUS 28, Linear-Elamite 1 — the source publication's
own typology) was this draft's first corroboration
candidate: the name Laursen appears nowhere in the G1
document, the G2 derivation, the G2 audit, or the study
outcome record, so no study step has touched it in any
form. **It is excluded on direct inspection during this
drafting** (a schema inspection — the row keys of
`glossa-corpus/indus/sources/contact-zone-rebuilt-2026-10-25/laursen_2010_table1.json`
enumerated; no profile was computed): the in-repo file
carries seal metadata and typology (seal number,
reference, Gulf type, site, dimensions) and *no
per-inscription sign sequence in any field*. Its header's
"28 inscribed with Indus text" is a class-membership count,
not a set of transcriptions this file holds. A record set
with no sequences has no table, and a typology label is
not a named state over records; there is nothing for a
separator to compute over. The contact-zone seals file
(`seals_at_mesopotamia.json`, same directory) does carry
sign lists, for 14 seals and 44 tokens, but its sign IDs
are hand-curated and partly placeheld pending CISI Vol. 3
plate ingestion, on its own face — too small and too
provisional to carry a bar arm, and cross-referenced
against Laursen rows besides. Both are excluded, and H1
stands as the sole held-out set. Naming the exclusion
here, rather than discovering it at the freeze, is the
drafting doing its work.

### 3.3 Exclusions, with reasons

- **The three Class II corpora** (M77 flat file, ICIT flat
  file, CISI coded subset): design data. G1 §1.2 states
  their profiles; G2 step 4 re-counted them. Any separator
  validated on them would be validated on the data that
  designed it — the exact failure G3's bar names.
- **The snapshot's `mayig-cisi` subset** (179 records):
  the same objects as the Class II CISI coded subset
  under the same scheme family; its profile was counted
  in G1 §1.2 / G2 step 4 (179 sides, 1,003 tokens, 182
  exercised P-codes). Not held out in any sense.
- **Wells 1998 / Registry v2 populations**: G1 §2.4α
  grounds the cannot-distinguish account in the registry's
  frozen witnessed count (399 of 557). Registry-keyed
  record sets are derivation-touched.
- **The anchor register and the claims ledger**: not
  tables; and any quantity over them is bookkeeping in
  Candidate 3's sense. Disqualified by §1, not merely
  unused.

### 3.4 The freeze

Before any profile is computed over H1 — before the
extraction is run for any purpose beyond the freeze's own
counts — a **freeze record** is committed to this spec's
records, carrying: the SHA-256 of the snapshot file as it
stands; the extraction rules (source-system filter; the
`canonical_grapheme_ids` list as the recorded sequence,
per §3.1) stated exactly; the counts the
freeze itself is permitted (H1's extracted record count
and token total; the H1↔flat-file object overlap); the case list
of §4 verbatim, including the split/merger rules in
executable form and the relabeling seed for control C1;
the verification that no adjacent frozen record (Spec
077's, the anchor-support audit) computed a profile over
H1, checked against those records and stated; the
skeleton version this stage answers to (the note in this
package's basis); and the bar text of §5 verbatim. The
freeze is the stage's T402 act. **Any change to a frozen
item after the freeze is an amendment act; an amendment
that touches the case list, the profile definitions, or
the bar voids the administration, which must then
re-freeze and re-run from zero under Spec 089's run
discipline.** Profiles computed before the freeze lands
are a falsifier event for claim C090-19, not a head start.

## 4. The cases (frozen by §3.4; stated here in full)

All cases are named states over H1 in §2's naming mode.
All share H1's object set and, except where a rule changes
them, its token total — separation here cannot be produced
by record counts, because the counts are the same by
construction; only identity structure varies.

- **A0 — the recorded coding.** The identity rule: H1's
  table as recorded. A0's profile is H1's separator value.
- **A1 — the positional split.** The most frequent code of
  H1's recorded table is split into two types by the
  token's position: occurrences in initial position of
  their sequence form one type, all other occurrences the
  second. (G1 §2.3's illustration (i) constructs its
  distinct case by exactly this rule form — a split "by
  the token's position in its inscription.") Expected
  structural effect: exercised count +1; multiplicity,
  positional, and adjacency spectra redistributed.
- **A2 — the tail merger.** The two least frequent codes
  of H1's recorded table whose multiplicity is at least
  10 are merged into one type. (The floor is a design
  parameter of this package, fixed here, applied
  mechanically at the freeze; it exists so the merged
  types are exercised enough for the merger to be a
  classification claim, not a hapax bookkeeping act.)
- **A3 — the head merger.** The two most frequent codes
  of H1's recorded table are merged into one type: a
  coarse classification of the same objects, of the kind
  the field's frame disagreements actually contain.
- **C1 — the relabeling control.** A0's codes permuted by
  a seeded random bijection (the seed is in the freeze).
  By §2's invariance argument, P must be identical to
  A0's in every component. If it is not, the separator as
  implemented is not the separator as defined, and the
  administration stops (§6).
- **C2 — the identity control.** A0 against A0. Must not
  separate.

**Practitioner agreement, stated as the judgment it is.**
The bar requires the separated cases to be ones "the
domain's practitioners agree are distinct." The agreement
this package relies on is about *classifications of the
same objects*: that a script coded under a split inventory,
a merged inventory, and its recorded inventory are three
different classifications is the decipherment field's
standing practice — it is the substance of the signary
disagreement G1 §2.4α measures inside this very record
system (64 attested codes in one frame, 713 in another, a
557-sign registry population, none of them interchangeable
in the field's own literature), and G1 §2.3's illustration
treats a positional split as producing a state π
distinguishes from the unsplit state. The package does
*not* claim practitioners agree any of A1–A3 is a *good*
classification; agreement that they are *distinct cases*
is what the bar names, and it is the claim the outcome
record must defend or the stage must concede. This is the
package's central judgment call, and it is labeled here so
ratification can strike it if it does not hold.

## 5. The bar

The administration is run once, under the freeze, by a
computer who did not draft this package, and audited by a
second worker who recomputes every profile independently
from the frozen inputs (the program's drafter/auditor
separation). Runs are run-scoped under Spec 089: each
computation mints its run id, writes its run record, and a
divergence between the computer's and the auditor's
profiles over the same frozen inputs is a junction, not a
discrepancy to be averaged away.

**The stage outcome is SEPARATED if and only if all three
hold, on the audited profiles:**

1. **Distinctness.** For each pair (A0, A1), (A0, A2),
   (A0, A3): the profiles differ in at least one named
   component.
2. **Invariance.** For each pair (A0, C1), (A0, C2): the
   profiles are identical in every component.
3. **No count separation.** No component counted toward
   (1) differs through a difference in object count or
   token total between the compared tables. (By §4's
   construction the compared tables share both, so (3) is
   a checkable property of the run records, included
   because a bar that cannot state its own confound
   control does not have one.)

## 6. Outcome vocabulary and the honest stops

Per-stage outcomes for G3, in the skeleton's discipline:

- **SEPARATED** — the bar of §5 met in full on the audited
  profiles. The stage's claim is exactly that: one
  separator, defined from the G1 document's terms,
  computed over records the derivation did not use,
  distinguishing the frozen agreed-distinct cases and
  refusing the controls. The study-level outcome remains
  **INSTANTIATES-path** (now with G3 attempted at stage
  strength), and the bare verdict INSTANTIATES stays
  reserved to the independent reader over the full G1–G5
  bar. This stage does not issue it, does not approach
  it, and does not soften the reservation.
- **NOT YET** — the administration ran and the bar was not
  met, or could not be met as frozen, with the obstruction
  named: which pair failed to separate (the coarsening of
  §2 made concrete), or which control separated (the
  definition or its implementation fails D5's invariance
  clause — the more serious finding, recorded as such).
  A NOT YET here is a complete stage outcome, publishable
  as it stands; no component is added, no case is
  re-chosen, and no second administration is run under
  this package to repair it. A successor attempt is a new
  package.
- **CANNOT BE ADMINISTERED** — the frozen administration
  cannot be run as specified: the freeze finds H1's
  sequence-bearing records too few or too short to carry
  the cases (a floor the freeze record must state
  numerically when it fires: fewer than 300
  sequence-bearing records, or fewer than 1,000 tokens —
  draft floors, ratified with this package), or H1's
  `canonical_grapheme_ids` lists prove unusable as
  recorded sequences under the
  frozen extraction rule, or the held-out verification of
  §3.4 fails (an adjacent record is found to have computed
  over H1). CANNOT BE ADMINISTERED is a finding about the
  record system's present contents, recorded with the
  counts that forced it; it is not a euphemism for a
  result the stage disliked, and the outcome record must
  show the forcing counts.
- **ANALOGY pressure, named in advance.** If the
  administration's honest reading is that profile
  differences of this kind are bookkeeping about codings
  rather than distinctions between candidate states of
  the script — the §4 judgment call collapsing — the
  outcome record says so in those terms and the
  study-level outcome moves to ANALOGY with the element
  named (the separator element, S4's D5 leg), for the
  reader and the registry. The stage does not grade its
  own judgment call; it records the evidence and the
  pressure, and the vocabulary above is where it lands.

The outcome — SEPARATED, NOT YET, or CANNOT BE
ADMINISTERED — is reported to the VEXA chat for the
improvement registry either way (decision D-090-10), in
the outcome record's own words.

## 7. Claims this stage would register (draft; not appended)

Ratification of this package approves the following claims
for intake at the stage's adoption (decision D-090-9),
through `tools/ledger/import_bundle.py` — the stage's only
ledger diff, renewing C090-13's boundary for this stage.
They are drafted here in claims.md normative form; the
aee-claims.json bundle is generated from them by the
adoption task's script, assessed under the pinned AEE,
and appended only on ratification. **Nothing below is in
the ledger as of this draft.**

**C090-17 — The separator is defined from the G1
document's terms only.** The separator of this stage (the
identity-structure profile P and its comparison) is
defined using only the frozen G1 document v1.1's terms
(the candidate state, the projection π and its sequence
table T, projection-equivalence under §2.3, the exercised
inventory) and the skeleton's D5 form. No physics result,
no register or ledger quantity, and no quantity defined
against a recorded corpus's profile is a component or a
premise of the definition.
*Falsifier:* a component of P, or a step of its invariance
argument, that cites a physics result, a bookkeeping
quantity, or a recorded profile as its ground; or a
component whose value over a fixed table can change
without the table changing.
*Does not establish:* that P is a good separator — only
that its definition stands on the G1 document's terms, as
D-090-3 requires of everything this study derives.

**C090-18 — The held-out set is untouched by G1 and
G2.** No step of the G1 drafting, the adversarial pass,
the G2 derivation, or the G2 audit computed a table, a
profile, or a per-record quantity over H1 (the snapshot's
`indusscript-m77` text-code records). The uses that exist
are named and bounded: G1 §1.5's file-level census lines
about the snapshot as a whole. The freeze record states
the extraction rules, the permitted freeze counts, and
the H1↔M77-flat-file object overlap it measured.
*Falsifier:* a G1/G2-era record, or a record they cite as
computed grounding, that contains a table, profile, or
per-record computation over H1; or an extraction
rule in the freeze that selects records by any property a
G1/G2 computation produced.
*Does not establish:* that H1's objects are disjoint from
the design corpora's — the claim is about computation,
and the overlap number is published with the freeze so
its weight is the reader's to judge.

**C090-19 — The freeze precedes every computation.** A
freeze record carrying the items §3.4 enumerates is
committed before the first profile over H1 is
computed by anyone, for any purpose including
exploration. Post-freeze changes are recorded amendment
acts; an amendment touching the case list, the profile
definitions, or the bar voids the administration.
*Falsifier:* a profile, spectrum, or exploratory
computation over H1 dated before the freeze
record's commit; or a frozen item changed with no
amendment act recorded.
*Does not establish:* that the frozen design is wise —
only that it was fixed before it met the data, which is
what makes the administration a test rather than a fit.

**C090-20 — Invariance inside a class is mechanical, and
is tested, not assumed.** For the frozen controls (the
seeded relabeling C1; the identity C2), the audited
profiles equal A0's in every component. A control that
separates refutes the separator as implemented (and, if
the implementation is faithful, as defined) under D5's
invariance clause, and the stage records that as its
finding.
*Falsifier:* an audited control profile differing from
A0's in any component, with the administration
nevertheless reported as meeting the bar.
*Does not establish:* invariance for arbitrary
equivalences beyond the controls — the controls are the
test the bar sets; the general invariance is §2's
arithmetic, which the controls sample at its most
failure-prone point (a full relabeling).

**C090-21 — The bar is the bar.** The stage outcome is
adjudged exactly by §5's three conditions over the frozen
case list and the frozen profile definitions. No
component is added, dropped, or re-weighted after any
profile is seen; no case is substituted; no second
administration under this package repairs a miss. A miss
is recorded as NOT YET or CANNOT BE ADMINISTERED, with
the obstruction named.
*Falsifier:* an outcome record whose SEPARATED rests on a
component, case, or threshold absent from the freeze; or
a re-run under this package following a recorded miss.
*Does not establish:* that §5's bar is the only fair bar —
only that it is the one this stage froze and answered to.

**C090-22 — No restricted material enters the stage's
records.** The held-out set contains no CISI scans and no
restricted material of any class; H1 enters the
stage's records as statistics and computed profiles only.
CISI-derived material plays no part in this stage's
design (the `mayig-cisi` subset is excluded at §3.3), and
nothing restricted is copied into the repository by any
stage act.
*Falsifier:* a CISI scan, or any restricted source
material, present in the stage's records or outputs; or
a stage output that redistributes restricted content
rather than statistics computed from records the
repository already holds openly.
*Does not establish:* anything about the CISI restriction
itself — only that this stage's design never needs to
touch it.

**C090-23 — This stage's ledger diff is its intake
append.** Across the whole G3 stage, the claims ledger's
diff is exactly the append of this stage's claim bundle
(C090-17..24) through the sanctioned intake at adoption,
plus the generated-layer regeneration that append forces.
No stage act adjudicates, reclassifies, annotates, or
scores any claim; no claim about the Indus script changes
status, stage, or score; the program's standing position
(the Indus script is not deciphered) is untouched, and
nothing in this stage is a decipherment claim or evidence
for one.
*Falsifier:* a ledger diff attributable to a G3 stage PR
beyond the adoption append's lines; or an Indus claim
reclassified, annotated, or re-scored citing this stage.
*Does not establish:* anything about the appended claims'
truth — only that the ledger's one-way flow survives the
stage intact (C090-13's boundary, renewed).

**C090-24 — The outcome is recorded in the skeleton's
vocabulary and reported, either way.** The stage closes
with an outcome record stating the G3 outcome (SEPARATED,
NOT YET with the obstruction named, or CANNOT BE
ADMINISTERED with the forcing counts shown), the audited
profiles,
and the study-level outcome in the study's vocabulary
(INSTANTIATES-path at most; ANALOGY if §6's pressure is
the honest reading, with the element named). The outcome
is reported to the VEXA chat for the improvement registry
as a stage deliverable. The formal verdict over the full
G1–G5 bar belongs to the independent reader under the
judging protocol; this stage does not issue it.
*Falsifier:* the stage closing with no outcome record; an
outcome stated in vocabulary the skeleton does not define
without mapping to its terms; a SEPARATED reported to the
registry in stronger words than the outcome record's own;
or no report delivered after the outcome record lands.
*Does not establish:* that the reported outcome is the
final verdict on the domain — the reader's verdict, and
G4/G5, stand after it.

## 8. Draft task list (for the tasks.md amendment at adoption)

Acceptance modes per the Autonomous Execution Doctrine.
Each task's *does not establish* line survives into the
stage record.

- **T401 — Adoption.** This package, as ratified, is
  recorded in the spec's records with the ratification
  act; the spec's claims.md and aee-claims.json gain
  C090-17..24 (bundle generated by script, assessed under
  the pinned AEE, outcome recorded verbatim); the bundle
  is appended through the sanctioned intake; the
  generated layers regenerate; the pre-append gate check
  runs first (the Spec 090 adoption shape). Acceptance:
  **gate**. *This does not establish:* that the package's
  design is sound — only that it was ratified, recorded,
  and entered by the sanctioned path.
- **T402 — The freeze.** The extraction rules of §3.4
  are implemented as a script over the pinned snapshot;
  the permitted counts are taken (H1's extracted record
  and token counts; the H1↔flat-file object overlap); the held-out
  verification against adjacent frozen records is run and
  stated; the freeze record is committed with every item
  §3.4 enumerates. Acceptance: **test** (the freeze
  record's items each present and recomputable from the
  pinned files; the CANNOT BE ADMINISTERED floors of §6
  checked against the counts and the result stated).
  *This does not establish:* that the held-out sets are
  large enough to be interesting — the floors are the
  minimum the administration needs to be a test at all.
- **T403 — The computation.** Profiles for A0, A1, A2,
  A3, C1, C2 over H1, computed from
  the frozen inputs only, each as a Spec 089 run with its
  run record. Acceptance: **test** (every frozen case has
  exactly one run record; every profile recomputable from
  the frozen extraction by the profile definitions).
  *This does not establish:* the outcome — computation
  produces profiles, not verdicts.
- **T404 — The audit and the outcome record.** A worker
  other than T403's computer recomputes every profile
  independently; divergences are junctions under Spec
  089, resolved from the frozen inputs, never averaged;
  the bar of §5 is adjudged mechanically on the audited
  profiles; the outcome record states the outcome in §6's
  vocabulary with the profiles and
  the boundary statements (no claim moved; no convergence
  step; the reader's verdict reserved). Acceptance:
  **human-as-oracle** (the stage reviewer against the
  freeze, the run records, and the bar). *This does not
  establish:* the verdict on the domain — it establishes
  what the administration produced and what it did not.
- **T405 — The report to the VEXA chat.** The outcome,
  in the outcome record's words, delivered to the VEXA
  chat for the improvement registry, with evidence
  pointers; the send recorded in the outcome record
  (date, destination, text or its hash). Acceptance:
  **test** (the recorded send matches the outcome
  record's outcome word). *This does not establish:*
  that the registry entry closes anything — G4, G5, and
  the reader's verdict stand after it.

## 9. Decisions this package asks the owner to ratify

- **D-090-5 — G3's home**: a stage amendment to Spec 090,
  superseding spec.md's G3 non-goal line for this stage
  only; C090-15 continues to bar G4/G5 to this stage, and
  its "unattempted" statement is amended to read "G3
  attempted under the stage amendment of 2026-11-05" if
  and when the stage runs. *Recommendation: adopt the
  stage amendment.*
- **D-090-6 — The separator definition**: P as defined in
  §2, five components, coarsening limit named.
  *Recommendation: adopt as defined.*
- **D-090-7 — The held-out set**: H1 as the sole held-out
  set and bar arm; the §3.2/§3.3 exclusions, Laursen
  among them. *Recommendation: adopt.*
- **D-090-8 — The bar and outcome vocabulary**: §5's
  three conditions; §6's outcomes including NOT YET and
  CANNOT BE ADMINISTERED as first-class, with no repair
  administration under this package. *Recommendation:
  adopt.*
- **D-090-9 — Ledger intake**: C090-17..24 appended at
  adoption through the sanctioned intake, the stage's
  only ledger diff. *Recommendation: adopt.*
- **D-090-10 — The report**: the outcome reported to the
  VEXA chat either way, extending D-090-4 to this stage.
  *Recommendation: adopt.*

## 10. Grounding gaps in this draft, named plainly

1. **H1's sequence coverage is not re-counted here.** The
   2,906 figure is G1 §1.5's census line for the
   `indusscript-m77` source system; how many of those
   records carry a non-empty `canonical_grapheme_ids`
   list, and their token
   total, are unknown to this draft. T402 exists to count
   them, and §6's floors exist because the answer might
   fail them. This is the package's largest open quantity.
2. **The H1↔flat-file object overlap is unmeasured.**
   §3.1 argues the untouched criterion holds either way;
   the number itself is owed by the freeze, and a reader
   may weigh a large overlap against the stage's
   held-out claim in a way this draft cannot pre-answer.
3. **H1's sequence representation rests on one field
   choice.** Sampled H1 records carry a diplomatic text
   string, a `canonical_grapheme_ids` list, and a
   `sign_instance_count` that disagrees with the list's
   length on samples (5 ids against a count of 4; 3 ids
   against a count of 2). §3.1 rules the list governs;
   why the count field disagrees (a null-code convention
   is the visible candidate: the discrepant samples
   contain code `000`) is not established by this draft,
   and the freeze must verify the choice against the
   snapshot's derivation record before relying on it.
4. **Adjacent-record verification is owed, not done.**
   That no Spec 077-era or audit record computed a
   profile over H1 is argued from what those records
   contain as cited in G1 (a registry-crosswalk witnessed
   count; a register audit), not from a fresh search of
   the frozen records. T402 runs the verification before
   the freeze lands; if it fails, §6's CANNOT BE
   ADMINISTERED fires honestly.
5. **No profile was computed over H1 for this draft.**
   Consistent with the stage's own discipline: computing
   a profile over H1 before ratification and freeze would
   be the contamination C090-19 exists to forbid. The
   corpus files were opened only for schema-level
   inspection (record structure, field presence — the
   §3.2 exclusion and §3.1's field ruling rest on it);
   every population quantity above is cited from the
   study's records, and no multiplicity, length, position,
   or adjacency count over H1 exists anywhere in this
   package.

**AI disclosure:** drafted by an AI agent (Muse, via
Muse) at the direction of Tristen Pierson, per
constitution sec. VI. Drafting only: no computation over
any held-out record was performed for this package.
