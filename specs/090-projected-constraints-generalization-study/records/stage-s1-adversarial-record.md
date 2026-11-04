# Stage S1 adversarial-pass record (T102) — Spec 090 (2026-11-04)

**Scope:** tasks.md T102 — the adversarial pass on the G1
draft, executed by a worker other than the drafter, on
branch `feat/090-s1-g1-document` at head
`f43447bb4e717bd3354ebfb9b99bb71259cbadd3` (PR #514). The
artifact under attack: `records/g1-document.md` v1,
SHA-256
974d5043ab463d0e6a33912b6e1136bcac288cd679827edade3c81d7af858d5b
— **recomputed by this pass and matched** against the hash
recorded in `records/stage-s1-record.md`; the document is
31,376 bytes, as the stage record states. This record does
not edit the G1 document: revisions are T103's, made with
this record in hand.

## Verdict summary

| Attack | Verdict |
|---|---|
| (i) Second absolute smuggled into the none-needed disposition | **NOT SUSTAINED** — every hunted candidate is disposed of on evidence located in the document and the records; the none-needed disposition survives the pass intact |
| (ii) Projection: rule or metaphor | **SUSTAINED IN PART** — π is a rule (the §2.3 finite check was executed and decides), but three located defects stand against the text: §2.3's equivalence clause contradicts §2.4α on unexercised inventory (F1); §2.4α's split/merger examples contradict §2.3 and §2.4α's own criterion (F2); §2.1's second naming mode invokes glyph data no record class supplies (F3). All three are repairable by revision; none shows π is a metaphor |
| (iii) Cannot-distinguish items α–ε: empirical content | **NOT SUSTAINED** — every item's grounding was opened and re-counted first-hand; the invalid M77-codes-minus-register-keys join the drafter flagged is nowhere committed in the document |
| (iv) Separation and form | **NOT SUSTAINED** on separation (the drafter's self-check independently verified); **SUSTAINED (minor)** on one citation: §1.5's "535 distinct values" attaches a correct count to the wrong unit (F4), with two further low-severity citation precisions (F5, F6) |

**Consequence for the stage.** No attack sustains a second
absolute, and no attack shows the projection cannot be
stated as a rule. The absolute disposition is not split,
so D-090-2's owner-oracle rule does not fire. T103 is a
**revision** act, not the NOT YET exit: findings F1–F4 are
required repairs before the freeze; F5–F9 are precisions
and clarities the freeze should carry.

---

## Attack (i) — second-absolute smuggling

**Method.** Re-run the audit's own test (§3.1: a quantity
is a primitive absolute exactly when (i) the system's
reasoning about candidate states uses it as given, (ii) it
is not a record nor record content with provenance in R,
(iii) it is not derived from R by a stated rule) against
the three dispositions the brief names, plus a hunt for
practice absolutes the audit never lists. For each
disposed candidate, construct the use §2 actually makes of
it and check whether that use is the disposed form.

**The ostensive extent (§3.3).** The strongest form of
this attack: §2.2 defines π over the object set O, so every
equivalence statement in the document is relativized to a
set whose extent is simply stipulated — the stipulation
functions as an absolute under the name "the record
system's own definition." The attack fails on the audit's
own test. §2.2 does not merely stipulate O; it derives it:
"O is the object set of the record system … — operatively,
the line sets of the coded corpora (1,669 inscriptions in
the M77 frame; 4,410 in the ICIT frame) and the snapshot's
object records carrying text codes" (line 308). O is
therefore the content of records (Class II files, the
Class V snapshot — hashes recomputed by this pass, §4
below), obtained by a stated operative rule: clauses (ii)
and (iii) of §3.1's test fail for O, so O is not an
absolute under the test the document set itself. And
§2.4δ carries the extent's one real consequence openly
rather than spending it as a premise: states differing
only outside O are equivalent *because* O is a survival
subset. What survives of this attack is a clarity point,
recorded as finding F7: §3.3 argues from "the boundary of
the system itself" (line 504: "R is defined by the pinned
artifacts of §1 … stated ostensively") without citing
§2.2's operative derivation, and §2.2's operative narrowing
— objects in the held Class I volumes that appear in no
coded corpus and not in the snapshot are outside π's
domain — is left implicit. A hostile reader can misread
the disposition as the audit exempting itself. The repair
is citation, not re-disposition.

**The anchor disposition (§3.4).** The attack in its
strong form: §3.4 grades imported identifications as
"assertion content with provenance … claim standing, not
given standing," but if any reasoning in the document — or
any step the study-to-come is set up to take — consumes an
imported identification as settled, the grading is a label
over a given. Constructing the uses: (a) §2 never uses a
reading at all — π is defined over (Σ, γ) and "does not
depend on ρ or on λ" (§2.2), so no equivalence statement in
the document rests on any anchor's content. (b) The one
place imported identifications appear as worked examples
is §3.4 itself, and this pass verified both against the
register at its pinned hash: the pending record's basis
(M071, `pending_non_sa_validation`) reads "Round 1:
INITIAL position (freq=16), distributional assignment; …"
— distributional, derived from the coded corpora by the
counting the basis cites, as §3.4(i) disposes; the strict
record M342's basis reads "Terminal marker, Dravidian case
suffix" — an imported identification, and it stands in the
system exactly as §3.4(ii) grades it: as the content of an
anchor record whose standing is its recorded validation
status, inside a strict set whose support census the
document itself prints against any settled reading of it
(§1.3, §3.4: of the 94 strict records, 6 supported by
evidence independent of the program, 46 internal only, 37
requiring revalidation, 2 insufficient, 3 expert-pending —
re-verified in the audit of record, whose own input pin is
this register's current SHA-256 df0cf620…). (c) The
study-to-come cannot consume an anchor as a premise
either: S2's derivation is bound by D-090-3/C090-8 to
D1–D3 and the G1 document's stated projection, and the
projection has no ρ-input to consume one through. (d) The
strict set's name is the one place a reader could mistake
claim standing for settled standing — `strict_sa_independent`
— but §1.3 defines the term on its face as independence
from the program's own SA derivation chain (the canonicals'
strict rule, verified in `settling-canonical.json`:
"confidence in {HIGH, MEDIUM} AND register category not in
{SA_DERIVED, SA_CONFIRMED_ONLY} AND register sa_in_chain is
false," applying the Phase-108 strict definition), and
§3.4 immediately sets the 6-of-94 independent-support
figure beside it. The disposition is the use, everywhere
the document uses the candidate. **Not sustained.**

**The framework constants (§3.7).** The attack: Spec
077's bar (502 of 557), glossa-settle-1, and matrix-defs
v1 are taken as given by every verdict they govern, so
they function as absolutes whatever §3.7 calls them; and
the S2 derivation ahead might need one as given. On the
record: §2.4α quotes the bar only as content of Spec 077's
frozen outcome record ("399 of 557 witnessed, 71.63%,
against a frozen bar of 502"); α's grounding is the
399/158 witnessed split, which this pass re-derived from
the outcome record — the bar's value does no work in α,
which stands unchanged for any bar. glossa-settle-1 and
matrix-defs v1 appear only in §1.4, as the ledger's
provenance machinery (and matrix-defs v1 is named inside
the settling canonicals' pin block — itself a record). No
step of §2's reasoning about candidate states takes any of
the three as a premise; and a derivation step that needed
one would be a category error on its face under D-090-3
(they are machinery over claim lines; π's classes are
defined over (Σ, γ) tables). Whether T201's chains in fact
stay clear of them is T202's audit question; at G1,
§3.7's disposition — "they figure in verdicts about
claims, not in the projection or in any premise about the
script" — is accurate as written. **Not sustained.**

**Candidates the audit omits — hunted, none found.**
Reading direction: per-record content of Class III (this
pass counted the field: carried on 171 of 287 records,
value `rtl` where carried, absent on 116), and sequence
order enters π only through Class II derivations'
transcription conventions (§1.2), which §3.8's fidelity
disposition covers. Transcription fidelity itself: §2's
only executed comparisons (§2.3) run between named states'
tables, never against raw glyphs, so no application of the
document consumes fidelity as a premise about the script —
§3.8's disposition matches the use. The pinning instrument
(SHA-256 hashes): contents of records (the canonicals' pin
block), instruments of citation rather than quantities of
the domain; covered in substance by §3.7. Cross-source
object identity: never asserted — O is defined operatively
per record set, and snapshot rows stand as their sources'
records with nulls on their face (§1.1). No quantity in
the program's practice was found functioning as
taken-as-given outside the audit's enumeration.

**Verdict (i): NOT SUSTAINED.** Defense located at §2.2
(operative derivation of O; ρ-independence), §3.4 with the
register records M071/M342 and the WP5 census, §3.7 with
§2.4α's use of the frozen bar. The none-needed disposition
(§3.9) survives this pass; the residue is clarity finding
F7, not a split.

---

## Attack (ii) — projection or metaphor

**Method.** Implement §2.3's decision procedure exactly as
written — *s ~ s′ exactly when there exists a bijection
β : Σ → Σ′ with β(γ(o)) = γ′(o) for every object o in O*
(line 340) — as a finite forced-correspondence check over
sequence tables, and run it on the document's two
illustration cases, on two attacker-constructed cases over
the actual M77 table (A: 1,669 objects, |Σ| = 64), and on
the brief's three named suspicions. A rule that decides
every well-posed case put to it is a rule; a place where
the document's statements answer the same question
oppositely, or where a needed input is nowhere defined, is
located and quoted.

**The document's illustrations decide as stated.**
(ii) C = A with code 047 relabeled throughout: the check
returns equivalent — as §2.3 says. (i) B = A with code 047
split by position in inscription (initial vs non-initial):
the split is non-degenerate on the records (047 occurs 541
times: 375 initial, 166 non-initial — counted by this
pass), |Σ_B| = 65, no bijection exists, the check returns
distinguished — as §2.3 says.

**Attacker's cases decide.** (a) E = A with the two most
frequent codes interchanged in exactly one inscription
(same cardinality, purely structural difference): the
forced correspondence contradicts itself (β(x) = x from
untouched inscriptions, β(x) = y from the altered one), the
check returns distinguished. §2.3's rule decides
same-cardinality structural questions mechanically, with
no appeal to plausibility. (b) A ρ-variant of A (identical
(Σ, γ), different (ρ, λ)): equivalent, as §2.4β requires.
On states presented as explicit assignments over O, π is a
decidable mapping in D2's sense. The "metaphor" charge in
its general form fails.

**Defect F1 — §2.3 contradicts §2.4α on unexercised
inventory.** Let Z be identical to A on every object in O,
except that Σ_Z adds one sign z that γ_Z never assigns to
any token on O. Then T(Z) = T(A) exactly: π, as §2.2
defines it and as D2 states it ("Two states are
projection-equivalent when pi cannot distinguish them"),
cannot distinguish Z from A. §2.4α says the same: states
are equivalent "however their inventories differ in
distinctions no surviving token exercises." But §2.3's
letter declares Z ≁ A, because its β must be a bijection
between the *full* inventories and |Σ_Z| = 65 ≠ 64 = |Σ_A|
(the check, run as written, returns not-equivalent). The
document answers one equivalence question two opposite
ways. This is C090-3's falsifier in its second form — an
equivalence question the document's rule cannot decide
either way, because its two statements decide it both
ways. *Repair for T103:* quantify β over the exercised
inventories (the signs γ and γ′ assign somewhere on O), or
normalize a state by deleting unexercised inventory
members before §2.3 applies. The repair is local: both
illustrations survive it (B's split subtypes are both
exercised; C's relabeling is), and the swap case still
decides.

**Defect F2 — §2.4α's examples contradict §2.3 (and
§2.4α's own criterion).** α's sentence runs: "States whose
(Σ, γ) induce the same identity structure over the
surviving tokens are equivalent, however their inventories
differ in distinctions no surviving token exercises — a
split of one sign into two whose token sets are separated
only by stipulation, or a merger of two signs no surviving
context separates." A *realized* split (the stipulation
assigns actual tokens to two types) and a *realized*
merger both change the identity structure over the
surviving tokens — that is what they are — and under §2.3
both defeat the bijection (demonstrated by this pass:
merging codes 748 and 781 in A yields |Σ| = 63 and a
forced correspondence that fails injectivity; the check
returns distinguished), and §2.3's own illustration (i)
concludes that a realized split *is* distinguished. So
α's examples fail α's stated criterion and §2.3's rule
simultaneously. The true statement α reaches for is an
epistemic one about the unobserved state of the script —
the records do not determine *which* classification is the
script's own — which is a claim about states not presented
as assignments over O, not a claim about π-equivalence of
named states. *Repair for T103:* re-state α so its
equivalence claims are exactly the ones §2.3 decides (as
repaired under F1), and carry the epistemic point as what
it is — the inventory of the script itself is not fixed by
the records, because any frame's coding is one named state
among rivals — without listing realized splits and mergers
as equivalences. α's *counts* are untouched by this defect
(see attack (iii)); its equivalence wording is.

**Defect F3 — §2.1's second naming mode invokes data the
record system does not define.** "A state is **named** in
this system's sense when its γ is presented as an explicit
assignment over the object set O (§2.2), or as a total rule
the system can execute over the recorded glyph data to
obtain that assignment" (line 300). §1 defines five record
classes; none of them is glyph data. Glyphs reach the
system only already coded (Class II derivations; the
snapshot's diplomatic codes) or as published Class I
entries, and the one glyph-level holding the document
names — the CISI page scans — is expressly withheld: "the
scans are not records this document hands to a reader"
(§1.1). For a state named only in the second mode, the
document therefore does not suffice to compute its
sequence table, and §2.3's "decidable from this rule
alone" does not hold for it — not because the check is
unmechanical, but because its input is nowhere in R.
*Repair for T103:* restrict "named" to the first mode
(explicit assignments over O — coded corpora and their
transforms), or define the glyph-data class, name the
records that supply it, and show they suffice to execute a
presented rule over O.

**Verdict (ii): SUSTAINED IN PART.** π is a rule:
decidable, executed, and correct on every well-posed case
put to it, including both of the document's illustrations
and two attacker cases. The three defects are real and
located, and all three are repairable by revision at T103
(F1 and F2 touch the equivalence definition and α's
wording; F3 touches the naming definition). None of them
shows the projection is a metaphor, and none blocks S2 in
principle — S2 derives over the classes of named states,
which the repaired §2.3 defines. Unrepaired, however, F1
leaves the class definition ambiguous exactly where S2
will quantify over it, so F1–F3 are required freeze
repairs, not optional polish.

---

## Attack (iii) — cannot-distinguish: empirical content

**Method.** Every grounding cited by §2.4 items α–ε was
opened and, where the document counts, re-counted from the
record at the branch head (the tree state the document
names, a7db3cfb). Separately, the document was searched
for the invalid join the stage record flags — any coverage
or identity conclusion drawn by joining the M77 file's
code space to the Mahadevan key space (numerical
coincidence treated as sign identity).

**α — grounded.** 64 distinct M77 codes and 713 distinct
ICIT codes re-counted from the two files (SHA-256s
recomputed and matched, §4). The 557-sign population, 399
witnessed, 158 without a Mahadevan counterpart, 71.63%,
and the frozen bar of 502 were verified in Spec 077's
frozen outcome record (`specs/077-signary-triangulation/
outcome.md`; freeze digest a9d10a2ba4… as §1.5 cites), and
the outcome record states the witnessed definition the
document quotes: "a population sign is witnessed exactly
when Registry v2's crosswalk gives it at least one
Mahadevan number." That join runs through the registry's
own crosswalk — a record — which is exactly the mediation
item ε requires; it is not the invalid join. The
within-file counts (564 of 1,669 single-token inscriptions;
one code, 047, supplying 541 of 5,361 tokens) re-counted
exactly. (α's equivalence *wording* is defect F2 under
attack (ii); its empirical content stands.)

**β — grounded.** β is in the first instance a
consequence of §2.2 (π does not depend on ρ or λ), and its
record ground is as stated: the coded corpora are bare
code sequences (re-counted as such), no coded record
carries a reading, and readings exist in the system only
as Class III assertions with provenance.

**γ — grounded.** Register re-counted at its pinned hash:
44 `pending_non_sa_validation`, 3 `no_validation_record`,
113 `premise_superseded`. The cross-tabulation this pass
ran is stronger than the document needed: all 44 pending
records stand at lifecycle stage `created`, and the only
records at stage `checked` in the register are the 94
strict ones — so no pending sign carries a completed
validation anywhere in the register, on its face, as γ
asserts.

**δ — grounded.** Definitional over O (§2.2), with its
counts re-verified (15,508 snapshot object records; the
coded corpora's bounded line sets 1,669 / 4,410), and the
class inspection confirms no record class enumerates what
did not survive.

**ε — grounded.** The Fuls–Mahadevan crosswalk file
exists and its header states what §2.4ε says it states
("Fuls (2023) ICIT codes <-> Mahadevan (1977) M77 codes").
The snapshot's crosswalk coverage re-counted: above zero
on 3,021 records, zero on 12,487 (§1.5's figures). The 158
of 557 figure is Spec 077's (above). The "81 of
the 94 carry a crosswalk identity entry" of §1.3 was
traced to the anchor-support audit's own summary field
(`records_with_a_crosswalk_identity_entry: 81`) — the
document cites the audit's count as the audit's, which is
the correct form for a frozen record.

**The invalid join — not committed.** §1.2's frame note
states the two number spaces differ (file codes run 3 to
920, re-counted; register keys run M001–M416, re-counted)
and draws *no* coverage conclusion from the comparison;
§1.3's populations are counted inside the register;
§2.4's coverage items rest on validation statuses (γ) and
crosswalk records (α, ε), never on subtracting one number
space from the other. The naive computation the stage
record warns against appears nowhere in the document,
including in its §3.2 frame disposition.

**Verdict (iii): NOT SUSTAINED.** Each item α–ε is tied to
a record this pass opened, and every count reproduced.
One observation is carried to the findings as a note (F9):
γ's distinguishing instrument is the validation record
chain, not π — β already places all reading differences
inside one π-class — so γ is a record-system
indistinguishability, which §2.4's own preamble ("what the
records of §1 cannot distinguish") licenses; the freeze
may say so in a clause, but no grounding fails.

---

## Attack (iv) — separation and form

**Separation — the drafter's self-check independently
verified.** This pass grepped the frozen bytes for the
verdict vocabulary and its near neighbors (instantiat-,
ANALOGY, NOT YET, separator, necessary condition, verdict,
outcome, succeed, conclud-, demonstrat-, G2, D4/D5/S4/S5
outside hashes): no occurrence of instantiat-, ANALOGY,
NOT YET, or separator anywhere; "necessary condition"
(line 17), "outcome language" (line 18), and "verdict"
(line 17) occur only in the header's boundary statement —
the one permitted place; the remaining "verdict" hits are
§3.2/§3.7's descriptions of the program's machinery
("frozen verdict bars," lines 490-491, 596, 600, 610) and
the remaining "outcome" hits name Spec 077's frozen
outcome record. No necessary condition, no separator, no
S2/S3 content, no sentence asserting that any skeleton
element is met. Two borderlines were read closely and
stand: §1.4's account of the ledger's generated layers is
C090-12's mandated accounting, stated as standing fact
with this study credited with none of it; and §3.9's "The
at-most-one bound is satisfied with none named" (line
658) states the audit's *disposition* — Appendix B item
3's required content — rather than a verdict that an
element is met (carried as clarity finding F8, not a
separation breach).

**Hash and state.** SHA-256 recomputed:
974d5043ab463d0e6a33912b6e1136bcac288cd679827edade3c81d7af858d5b
— matches the stage record. All document counts were
re-derived from the records at the branch head; the full
verification table is §4 of this record. Every figure
reproduces exactly except the three citation defects
below.

**Defect F4 — §1.5's 535 attaches to the wrong unit
(moderate).** "Diplomatic text codes appear across the
file in 535 distinct values" (line 246). Counted as
written — distinct values of the snapshot's
`text_code_diplomatic` field — the figure is **2,465**,
not 535. The number 535 is real: it is the count of
distinct *sign tokens* appearing inside those codes
(splitting the codes on their separators), which this pass
reproduced exactly (535). As written, the sentence does
not reproduce from the record it cites — the shape of
C090-2's falsifier at the level of one figure. *Repair
for T103:* reword to name the unit counted (e.g. "the
diplomatic text codes draw on 535 distinct sign codes"),
or state the distinct code-string count (2,465) — and say
which.

**Defect F5 — §1.2's CISI count (minor).** "179 multi-sign
inscriptions" (line 99) repeats the loaders' summary
language; the CISI loader of record's own detail states
179 inscription sides of which 178 have ≥ 2 signs (one
single-sign side). *Repair:* "179 inscription sides (178
multi-sign)," or a footnote to the loader's detail.

**Defect F6 — §1.2's reading-direction coverage (minor).**
"the anchor register (§1.3) records a reading direction
per anchor (the value carried is `rtl`)" — the field is
carried on 171 of 287 records; 116 carry none (counted by
this pass). *Repair:* "where carried, `rtl` (171 of 287)."

**Verdict (iv): NOT SUSTAINED on separation; SUSTAINED
(minor, F4) with F5–F6 on citation precision.** The
document contains definitions and the audit only; the
freeze repairs are wording-and-unit corrections, none of
which touches a disposition.

---

## Findings list for T103

| # | Severity | Location | Repair the freeze must make (or why the draft stands) |
|---|---|---|---|
| F1 | **High — required** | §2.3 (line 340) vs §2.4α | Quantify the bijection β over the exercised inventories, or normalize unexercised inventory members away before §2.3 applies, so §2.3 and §2.4α answer the unused-inventory question the same way (equivalent). Demonstrated defect: Case Z in attack (ii) |
| F2 | **High — required** | §2.4α | Remove realized splits and mergers from α's equivalence examples; re-state α's point as the epistemic one (the script's own inventory is not fixed by the records) and confine its equivalence claims to what repaired §2.3 decides |
| F3 | **Medium — required** | §2.1 (line 300) | Restrict "named" to explicit assignments over O, or define the glyph-data record class and show the records supply it; until then §2.3's decidability claim holds only for the first naming mode |
| F4 | **Medium — required** | §1.5 (line 246) | Correct the 535 figure's unit (distinct sign tokens inside the diplomatic codes) or replace with the distinct code-string count, 2,465 |
| F5 | Low | §1.2 (line 99) | CISI subset: "179 inscription sides (178 multi-sign)" per the loader of record's detail |
| F6 | Low | §1.2 | Reading direction: "where carried, `rtl` (171 of 287 records)" |
| F7 | Low — clarity | §3.3 (line 504); §2.2 (line 308) | Cite §2.2's operative derivation of O inside §3.3 as the audit-test clause failure, and make §2.2's operative narrowing of O explicit (Class I objects in no coded corpus and not in the snapshot are outside π's domain; §2.4δ reads over the operative O). The disposition stands; only its argument needs the citation |
| F8 | Low — clarity | §3.9 (line 658) | Prefer the disposition's own test language ("no candidate satisfies the test of §3.1") over "the at-most-one bound is satisfied," to keep the separation line bright. The draft stands if unamended; this is polish, not a breach |
| F9 | Note | §2.4γ | γ is a record-system indistinguishability (validation-chain), not a π-class statement — licensed by §2.4's preamble, but a clause saying so would prevent a reader mistaking it for one. No repair required |

No finding changes the audit's disposition (§3.9
none-needed), and none requires the owner as oracle. If
T103's revision on F1 or F2 changes the equivalence
definition's *substance* beyond the repairs above, that is
a new draft act, and this pass's attack (ii) stands to be
re-run against it.

---

## Verification annex — every document figure, re-derived

All counts below were recomputed or opened by this pass
from the records at branch head f43447bb (tree state
a7db3cfb for the underlying records), read from the pass's
own count outputs, not from the stage record.

- **Hashes**: g1-document.md 974d5043… ✓ (stage record);
  M77 file 878fd223… ✓; ICIT file c8839fd3… ✓; anchor
  register df0cf620…, 570,344 bytes ✓; ledger 15a5fbad… ✓;
  corpus snapshot 08fc96c8… ✓.
- **M77 file**: 1,669 inscriptions; 5,361 tokens; 64
  distinct codes; code range 3–920; mean length 3.21; 564
  single-token inscriptions; one code occurring exactly
  once; exactly three codes occurring ≤ 3 times; most
  frequent code 047 with 541 tokens; 25 lines longer than
  14 tokens (against the loader header's stated 1–14 range,
  April 2026 — the document's §1.2 discrepancy note is
  accurate; the loader's derivation statement, "OCR +
  sign-rank-correlation glyph mapping," verified in
  `backend/glossa_lab/data/indus_m77.py`). ✓ all
- **ICIT file**: 4,410 inscriptions; 14,213 tokens; 713
  distinct codes. ✓
- **CISI subset**: 179 inscription sides, Mohenjo-daro
  only, Parpola P-codes (`backend/glossa_lab/data/
  indus_cisi.py`); 178/179 multi-sign — see F5.
- **Anchor register**: 287 records; 286 Mahadevan keys
  (numbers 1–416) + H003; tiers HIGH 166 / MEDIUM 5 /
  LOW 3 / CANDIDATE 113; validation statuses
  strict_sa_independent 94 (HIGH 90 + MEDIUM 4),
  sa_in_provenance_chain 33, pending_non_sa_validation 44,
  no_validation_record 3, premise_superseded 113; stages
  checked 94 / created 193. ✓ all
- **Anchor-support audit** (`docs/repair-2026-10-26/
  anchor-support-audit.json`): audit id
  repair-2026-10-26-wp5-anchor-support-audit; input pin =
  the register's current hash; dispositions 6 independent
  / 46 internal only / 37 revalidation / 2 insufficient /
  3 expert-pending, the three being M222, M362, M398;
  summary field records_with_a_crosswalk_identity_entry
  81. ✓ all
- **Ledger**: 943 lines; 912 claims (bundle 889, extracted
  23) + 31 annotations; falsifier on 903/912, the 9
  nulls all extracted; statuses draft 888, untested 12,
  partially_supported 3, strongly_supported 2, contradicted
  4, partially_falsified 1, unsupported 1, superseded 1. ✓
  all
- **Matrix**: 912 rows × 644 columns, 1,435 cells
  (`glossa-indus/matrix/matrix.json`); program-map coverage
  agrees (912 claims; open 903 / negative 6 / positive 2 /
  closed_other 1). ✓
- **Settling**: canonicals' strict rule and pin block
  verified in `settling-canonical.json` (pin block names
  the current ledger, register, and snapshot hashes);
  `tools/ledger/run_settling.py verify-canonicals` run by
  this pass: **6/6 registered canonicals reproduce**
  (exit 0). ✓
- **Snapshot**: 15,508 rows; sources PennMuseum 7,515,
  MetOpenAccess 4,904, indusscript-m77 2,906, mayig-cisi
  179, ClevelandArtOpenAccess 4; schemes Mahadevan1977
  2,906, Parpola1982 179, none stated 12,423; crosswalk
  coverage > 0 on 3,021, zero on 12,487. ✓ all — except the
  diplomatic-code figure, F4.
- **Gate**: `ledger_gate.py`'s header states "The gate
  never writes" (verified, line 38). ✓
- **Spec 077**: 557 population; 399 witnessed (71.63%)
  under the frozen crosswalk-based definition; frozen bar
  502 (90%); freeze digest a9d10a2ba4… ✓

## T102's "does not establish" line (from tasks.md)

*This does not establish:* that an unsustained attack
means the draft is sound — only that these four attacks,
worked on evidence, did not land; the independent reader's
judgment stands after this study regardless. (And where
attacks did land — F1–F4 — the finding is that the text as
written fails there, not that the elements it defines are
unfixable: each carries its repair.)

**Process note.** Every result above was read from the
pass's own process logs or the records themselves; no
background-completion notice was relied on for any figure
or verdict, and no divergence between a notice and a
record was encountered.

**AI disclosure:** executed by an AI agent (Muse, via
Muse) at the direction of Tristen Pierson, per
constitution sec. VI. The drafter of the G1 document was a
different worker, per the plan's separation rule.
