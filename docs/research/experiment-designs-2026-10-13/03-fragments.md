# Designs 03 — the fragment records

Five records in the claim set are not whole claims. Automatic extraction pulled
single table cells or headings out of source documents, and the records kept the
cell and lost the context: a sign number with no sign list named, a heading with
no finding under it. Phase-104 stopped at the door on each (RULE-NUM: the sign
number matches nothing in the repository's 86-entry crosswalk registry;
RULE-NOCOND: no falsification condition and no stated proposition).

For a fragment, the honest first experiment is an **identification**: recover
what the fragment points at, from the source document itself, and only then ask
whether a test exists. These designs are desk work on documents the program
already holds (the extractions were made from them), plus, where identification
succeeds, the test the recovered claim actually carries. No design in this file
invents a proposition and credits it to the source.

---

## D-15 — "Sign 900 means six": identify the sign, then test it as a numeral

- **Claim:** `ancient_writing_and_modern_technologies_51831ac9_sign_val_0001`
  (UNTESTED fragment — in full: "Sign value: 900 / number six").
- **Feasibility:** RUNNABLE-TODAY (identification is desk work on the held
  source document; the test runs on in-hand corpora).

**Step 1 — identification (the experiment's first half).** Re-open the source
document the extraction came from and recover the full table the cell was
pulled from: which published sign list numbers its signs (the table's own
heading, introduction, or citations will say), and the drawn sign its number
900 labels. Success at step 1 is precise: the sign list is named from the
document's own text, and the sign is matched to an entry in the program's
crosswalk registry or to a drawn sign in a published list. Failure is also
precise: if the document does not name its list and the sign cannot be
matched, the design closes as IDENTIFICATION FAILED, and the record's honest
disposition is a stated gap (it already is one) — not a verdict on "six".

**Step 2 — the numeral test (only if step 1 succeeds).** Hypothesis: if the
identified sign means "six" (a numeral), it should behave like the script's
known numeral signs — the stroke-like signs that appear in counting patterns:
it should occur in short, repetitive sequences and in measure-like contexts,
and its positional profile should resemble the known numerals' more than it
resembles ordinary signs'. Falsifier: the sign's behaviour is indistinguishable
from frequency-matched ordinary signs, or unlike the known numeral set, on
the frozen measures. Method: compare the sign against (a) the known numeral
signs and (b) a frequency-matched ordinary-sign control set, on three
measures fixed in advance: share of occurrences in inscriptions of length
three or less; share of occurrences adjacent to another numeral-class sign;
positional entropy (how spread across positions it is). Criteria: NUMERAL-LIKE
if it sits inside the known numerals' range on at least two of the three
measures and outside the control set's median on the same measures; NOT
NUMERAL-LIKE if it sits inside the control range on at least two; MIXED
otherwise (reported as such). Data: the strict corpus; the known-numeral set
fixed from published identifications before counting.

**What it would move.** Step 1 alone converts the fragment from a pointer into
a claim (or closes it as unidentifiable). Step 2 can move the recovered claim
to checked on the numeral question.

**What it would NOT establish.** That the sign's value is *six* specifically,
as against four or seven. Distributional behaviour can support "this sign is a
numeral"; picking the exact number needs evidence of a different kind
(counted depictions, bilingual material) that this program does not hold, and
the design says so rather than pretending a distribution can count.

---

## D-16 — The two "sign 700" fragments: one sign, two values, one design

- **Claims:** `ancient_writing_and_modern_technologies_51831ac9_sign_val_0002`
  ("700 / a volumetric system with a unit of 40") and `…_sign_val_0003`
  ("700 / a unit of 4") (both UNTESTED fragments; Phase I kept them as separate
  propositions because they say different things — and both cannot be right
  as stated).
- **Feasibility:** BLOCKED on the same identification as D-15 step 1, applied
  to this table.

**The question in plain words.** Two cells from the same source assign sign
700 two different values. Before any archaeology: one of them may be a copying
or extraction error. The first test is therefore textual, not statistical —
recover the table and read what it actually says.

**Step 1 — identification and reconciliation.** Recover the source table in
full (same act as D-15 step 1). Three outcomes, each decisive in its own way:
(a) the table states one value — the other fragment is an extraction error,
and the fix is an appended, dated correction to the wrong record (never a
silent edit), leaving one claim to test; (b) the table states both values in
different rows or contexts — the two claims are about different things (for
example different periods or different measure systems), and each is
re-stated precisely before any test; (c) the table cannot be recovered or
does not resolve the conflict — both records stay as stated gaps, with the
conflict itself as the recorded finding. Until step 1 reports, no
distributional test is meaningful, because nobody knows which drawn sign
"700" is or what exactly is being claimed about it. That is the block, and it
is a block of hours of desk work, not of missing science.

**Step 2 — the discrimination test (only after step 1 leaves a testable
pair or a single volumetric claim).** Hypothesis space, stated in advance:
if the sign is a unit in a measure system, its occurrences should concentrate
on containers and measure-bearing objects and in tally-like groupings,
rather than spreading across all object types like an ordinary sign. Between
the two values: a unit-of-4 system and a unit-of-40 system predict different
*grouping* behaviour in repeated-sign sequences — counts of the sign within
one inscription should cluster at multiples and sub-units of the base. The
design states honestly that this discrimination is weak evidence at Indus
inscription lengths (most texts are under ten signs; a base of 40 may never
express itself in a single text), so the pre-registered outcome set includes
CANNOT DISCRIMINATE as a first-class result, not a failure. Method: object-type
distribution of the identified sign versus frequency-matched controls
(container/measure object classes from the catalogue metadata), plus the
within-inscription repetition profile. Criteria fixed in advance:
VOLUMETRIC-LIKE if the object-type concentration clears the control range at
the 5% level; the 4-versus-40 question is answered only if the repetition
profile separates the two bases by the pre-registered margin, else CANNOT
DISCRIMINATE is recorded. Data: the CISI-based corpus layer with object-type
metadata, as held.

**What it would move.** Step 1 resolves a standing contradiction in the claim
set — worth doing for record hygiene alone. Step 2 can move at most one
surviving claim to checked, and may honestly end at CANNOT DISCRIMINATE.

**What it would NOT establish.** A proven unit value. As with D-15, exact
values are beyond distributional evidence; this design can at best support
"measure sign, base unresolved".

**Unblocking act.** D-15 step 1's table recovery, extended to this table —
same source document family, same desk session pattern. If the source
document cannot be located in the program's library after a stated search,
both designs record that as the block (re-acquisition of the source is then
the unblocking act, through ordinary published-source channels).

---

## D-17 — "Sign 821, used in a variety of contexts": recover the argument, or retire the fragment

- **Claim:** `the_archaeology_and_epigraphy_of_indus_w_27f45a68_sign_val_0001`
  (UNTESTED fragment — and, unlike its siblings, it carries no testable
  proposition even if the sign is identified: almost any common sign is "used
  in a variety of contexts").
- **Feasibility:** RUNNABLE-TODAY (a recovery design; it may honestly produce
  no experiment).

**The design.** Re-extract the source passage in full (the document the
extraction came from, held by the program). Two outcomes, both pre-registered
as successes of the design: (a) the passage argues something specific — for
example, that the sign's spread across contexts rules out a narrow meaning, or
supports a specific classification — in which case that argument is extracted
as the claim, with the sign list named and the sign identified, and a test is
designed against it at that point (the test belongs to the recovered claim,
and designing it now, before the argument is known, would be inventing it);
(b) the passage is a catalogue observation with no argument attached — in
which case the design's output is a recommendation, recorded on the record,
to retire the fragment as an extraction artefact by an appended, dated
disposition. Either way the record stops presenting a non-proposition as a
claim awaiting a test it can never have.

**What it would move.** The fragment to a recovered claim with a designed
test, or to a retired artefact with the reason on record. Nothing about the
sign itself is decided by this design, and it does not pretend otherwise.

**What it would NOT establish.** Anything about sign 821. This is record
repair, honestly labelled.

---

## D-18 — "Sign 297 is the horned tiger": an identification concordance

- **Claim:** `the_archaeology_and_epigraphy_of_indus_w_27f45a68_sign_val_0002`
  (UNTESTED fragment — the kind of statement that *can* be checked, once the
  drawn sign can be located: identifications can be compared across published
  sign lists).
- **Feasibility:** RUNNABLE-TODAY.

**Step 1 — identification.** As D-15 step 1: recover the source's sign list
from the document, match its sign 297 to a drawn sign, and fix that sign's
identity in the program's crosswalk registry with the citation attached. If
the list cannot be named, the design closes as IDENTIFICATION FAILED (the
record stays a stated gap).

**Step 2 — the concordance test.** Hypothesis: the identification ("horned
tiger") is the published consensus for this drawn sign, not one scholar's
call. Method: compare the identification against every published sign list
the program holds or can lawfully cite (the CISI lists, Parpola's list,
Mahadevan's list, Wells's list — the last already witnessed in the
Phases 120–124 work), scoring each as AGREE (same animal identification),
DISAGREE (a different identification), or SILENT (the list does not identify
the sign's referent). Criteria fixed in advance: CONSENSUS if at least two
independent published lists agree and none disagrees; SINGLE-SOURCE if only
the original source identifies it so; CONTESTED if any held list disagrees —
with the disagreeing identification quoted. The outcome is recorded on the
claim as its first check: an identification claim is checked by concordance,
not by corpus statistics, and the verdict words are chosen accordingly.

**Why it matters beyond this fragment.** Animal identifications are raw
material for the shared classification behind D-05, D-06, and D-13. Each
fragment resolved this way either strengthens that asset (a consensus
identification, cited) or warns it (a contested one). The design feeds the
asset; it does not draw on it, so there is no circularity.

**What it would NOT establish.** That the sign *meant* a horned tiger in use,
or any role in inscriptions. It settles what the drawn sign depicts, as the
field's lists record it — the identification layer only.

---

## D-19 — The heading with five sources: re-extract what the findings actually were

- **Claim:** `ancient_writing_and_modern_technologies_51831ac9_statisti_0004`
  (UNTESTED fragment — in full, a heading: "Statistical finding: positional
  analysis." The same heading was extracted from five source documents;
  Phase I merged the five copies into this one record, with the four others
  kept as evidence instances: from the Fuls 2023 catalogue work, from a
  positional-analysis paper, from the archaeology-and-epigraphy source, and
  from Hunt's book.)
- **Feasibility:** RUNNABLE-TODAY.

**The design.** Re-extract, from each of the five source documents (all held —
they are the documents the original extractions ran on), the full passage
under that heading: the finding, its numbers, its corpus, and its stated
conditions. Each recovered passage becomes its own claim record through the
program's normal intake, with the proposition stated in plain words, its
numbers attached, and a falsifier written from the passage's own logic (or
the absence of one recorded, as D-08 had to do for a claim that lacked one).
The design's deliverable is up to five real claims where one empty heading
now stands; the checks those claims then need are designed per claim at
intake, not pre-invented here. The heading record itself is then dispositioned
by appended note: superseded by the recovered claims it pointed at, or
retired as an extraction artefact if a passage recovers nothing statable
(that outcome, per source, is pre-registered as acceptable and reportable).

**Criteria fixed in advance.** The design succeeds if every one of the five
passages is accounted for with one of three recorded outcomes: CLAIM
RECOVERED (proposition + numbers + falsifier status on record), PASSAGE
EMPTY (the section states no checkable finding — quoted evidence attached),
or SOURCE UNLOCATED (the document cannot be found in the program's library
after a stated search — the unblocking act is then named per source).
Anything less — a passage skipped without an outcome — is a failure of the
design, stated in advance so it cannot happen silently.

**What it would move.** One fragment out; up to five genuine claims in, each
entering at the *created* stage with a statable test — which is where the
lifecycle wants them. It also closes a standing embarrassment honestly: the
topic this heading points at (do signs occupy preferred positions?) is one of
the better-tested topics in the program on other records, and none of that
credit belongs on this record until a recovered claim earns its own.

**What it would NOT establish.** Any positional finding at all. Recovery is
not verification; the recovered claims start unchecked, and this design says
so on their records at creation.
