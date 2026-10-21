# Spec 056 — "Sign 821, Used in a Variety of Contexts": Recover the Argument, or Retire the Fragment (Design D-17)

> ## DESIGN DRAFT — FOR FREEZE DECISION — 2026-10-21
>
> Drafted under the runnable-experiments
> campaign plan approved by the owner AS
> WRITTEN on 2026-10-21
> (`~/workspace/your_files/2026-10-21-runnable-experiments-campaign-plan.md`,
> Parts 1–4): campaign member 12, design
> D-17, one of the three fragment recoveries
> (with D-15 and D-19), drafted in parallel
> throughout Wave 1 and consuming no shared
> asset. **The freeze and the execution of
> Spec 056 are separate later acts.** No AEE
> lifecycle hooks have run on this draft;
> they are a freeze gate. Nothing in this
> draft has been run, frozen, registered, or
> computed. Drafting merges nothing.
>
> This spec is a recovery and record-repair
> act by design. Its two pre-registered
> terminal outcomes are a recovered claim
> and a retirement recommendation; both are
> successes of the design, and the act —
> not this draft — decides which one the
> record gets.
>
> The execution phase number is **unassigned**
> at this draft. Spec 056 allocates its phase
> number at the freeze act, from the merged
> record as it then stands (DD-056-7).

**Design source:** D-17 in the experiment-design
packet at PR #195
(`docs/research/experiment-designs-2026-10-13/03-fragments.md`,
§D-17, read in full at this draft).

**Claim under repair:**
`the_archaeology_and_epigraphy_of_indus_w_27f45a68_sign_val_0001`
— UNTESTED fragment: "Sign value: 821 / it is
used in a variety of contexts (Figure 6".

**AI disclosure:** this draft is produced by an
AI agent (Muse Spark, via Muse) at the
direction of Tristen Pierson, per constitution
§VI.

---

## 1. The claim and the record it stands on

The record is a fragment, and — unlike its
siblings in the fragment family — it carries
no testable proposition even if its sign is
identified: almost any common sign is "used
in a variety of contexts". The claim record
(`glossa-indus/claims/extracted_claims/the_archaeology_and_epigraphy_of_indus_w_27f45a68.json`,
pinned in §2) states, verbatim:

> "Sign value: 821 / it is used in a variety
> of contexts (Figure 6"

The record's own text is truncated
mid-reference — the extraction cut the
sentence it was pulling (defect D-3 in
adjudication.md). The full sentence stands
in the source (§2): "Whatever sign 821 reads
it is used in a variety of contexts (Figure
6.13)."

The source document is Bryan K. Wells, *The
Archaeology and Epigraphy of Indus Writing*
(Archaeopress, 2015; ISBN 978 1 78491 046 4;
technical appendices by Andreas Fuls), held
by the program as cleaned text
(`glossa-indus/processed/cleaned_text/the_archaeology_and_epigraphy_of_indus_w_27f45a68.txt`).

Phase-104 evaluated this record and stopped
at the door (RULE-NUM): the sign number is
cited without a stated numbering system, no
matching entry was located in the program's
crosswalk registry (86 numeric IDs present
in that record), and the extraction carries
no falsification condition. The claim's own
adopted not-understood text states what
would change the picture: "the source
passage in full. If the passage argues
something specific (for example, that the
sign's spread rules out a narrow meaning),
that argument should be extracted as the
claim, with the sign list named."

That is the whole of this spec. It runs no
test on any sign, corpus, or reading. It
re-extracts one pinned passage under a fixed
protocol (§§4–5) and lets the passage decide
between the two outcomes the design
pre-registered (§6).

### 1.1 The question, in plain words

A table cell was pulled out of a book and
kept as a claim, and the cell by itself says
nothing that could ever be tested. Does the
passage the cell came from actually argue
something specific about this sign — an
argument that can be stated as a claim, with
a way to be wrong — or is the passage only a
catalogue observation, in which case the
honest act is to retire the fragment on the
record as an extraction artefact and stop
presenting a non-proposition as a claim
awaiting a test it can never have?

### 1.2 The hypothesis and its falsifier

**Hypothesis.** The pinned passage argues
something specific about sign 821 that can
be recovered as a claim in the program's
claim form (§5): a proposition stated from
the passage's own argument, about an
identified sign in a named sign list, with a
falsification condition statable from the
passage's own logic.

**Falsifier.** Re-extraction under the §4
protocol recovers no such proposition — the
passage is a catalogue observation with no
argument attached that passes the §5 test —
in which case the fragment is retired on the
record as an extraction artefact (§7). The
falsifier is the design's own, carried
verbatim in substance: "Re-extraction
recovers no claim — the fragment is retired
on the record as an extraction artefact"
(campaign plan, Part 2, member 12).

## 2. Inputs (pinned at this draft; re-asserted at the freeze)

| Input | Pin / state |
|---|---|
| Claim record (`glossa-indus/claims/extracted_claims/the_archaeology_and_epigraphy_of_indus_w_27f45a68.json`) | SHA-256 `bd0f7abddc9c26537f4ebe5f66f6a1fc69d394a4c2edbe745a8b7eb1ddc3333a` (recomputed at this draft from `main` at 83b6a563) |
| Source book, held cleaned text (`glossa-indus/processed/cleaned_text/the_archaeology_and_epigraphy_of_indus_w_27f45a68.txt`) | SHA-256 `62acf855ac3ecf39fc7a7e6597dba9a3cb6e35948528f69e9424eb81308d261e` (recomputed at this draft) |
| Phase-104 evaluation (`glossa-indus/reports/phase104_claims_evaluation.json`) | SHA-256 `2d0b83e8055a04b96635007054cfadde472f605dc7e5b249a61c8f9ea89b858d` (recomputed at this draft) |
| Lane-2 adopted drafts (`specs/029-tao-claim-lifecycle/lane2-drafts/drafts.json`) | SHA-256 `3f645c9a4132ba5a0bc5fca4ca22810b8b6169a2f1f9f85f35990c7b72df33fb` (recomputed at this draft) |
| Crosswalk registry (`data/crosswalks/canonical_sign_registry.csv`) | SHA-256 `8a0b2a82ac8d226d574ce01f5550c581efd91a97cab86201a62f7a7e435bd420` (recomputed at this draft; 803 rows as held today — consulted at §5 only as one identification route; it carries no entry with `wells_ids` = W821, verified at this draft) |
| Anchors file (`backend/reports/INDUS_FINAL_ANCHORS.json`) | SHA-256 `df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569` (recomputed at this draft). This spec moves no anchor; the file is asserted byte-identical before and after any execution. |

**The passage of record (the pin this spec
exists to fix).** The design says "the
source passage" without bounding it
(defect D-2 in adjudication.md). This draft
fixes the passage mechanically
(**DECIDED-BY-DRAFT, DD-056-1**):

- **Document:** the held cleaned text above.
  Its SHA-256 is the governing pin; every
  locator below is subordinate to it.
- **Start anchor:** the line consisting
  solely of `The Dholavira signboard, revisited`
  (cleaned-text line 2783; unique as a
  standalone line; printed p. 90).
- **End anchor:** the next line consisting
  solely of `The Mohenjo-daro bangle pot`
  (cleaned-text line 2872; printed p. 94).
  The passage ends immediately before it.
  The phrase occurs elsewhere in the book as
  running text; only the standalone heading
  line after the start anchor bounds the
  passage.
- **Passage:** cleaned-text lines 2783–2871
  inclusive — the headed section that
  contains the anchor sentence. Draft-observed
  size 5,354 bytes; draft-observed SHA-256 of
  the byte slice from the start of the start
  anchor line to the start of the end anchor
  line: `51d6fb3a460d94abc98c2ff735b17c5131a68c203e4d16692a21725790c0c604`.
  The freeze re-computes this digest byte-exactly
  and pins it in the freeze record
  (OPEN-1 in adjudication.md).
- **Anchor sentence (verbatim, unique in the
  document, occurrence count 1, verified at
  this draft):** "Whatever sign 821 reads it
  is used in a variety of contexts (Figure
  6.13)." — printed p. 93, in the passage's
  final discussion paragraph, followed by the
  Figure 6.13 caption.

No other text is the passage. The same book
discusses sign 821 elsewhere (a Chapter 3
discussion of the Dholavira toponym, and an
appendix discussion of doubled signs 820/821);
those passages exist, are noted here so their
exclusion is a recorded decision rather than
an oversight, and are **not** inputs to this
spec (claim F056-C07). An argument recovered
from anywhere else in the book is not a
recovery under this spec; it is scope creep,
recorded as a defect if it appears.

**A limit of the held text, stated at draft.**
The cleaned text drops the book's sign
glyphs (sentences contain blank slots where
glyphs stood) and Figure 6.13 itself is a
graphic, present only as its caption. The
passage of record is therefore the passage
*as held*: the protocol in §4 judges the
passage's propositional argument in its
text. Anything carried only by the figure's
images is outside the passage of record
(OPEN-4 in adjudication.md).

## 3. Step 0 — gates before any re-extraction (fail-closed)

Execution runs these checks in order, before
any extraction pass reads the passage for
argument. A failure closes the execution in
the class named; nothing is repaired at run
time, and no substitute document, edition, or
passage is admitted.

- **0.1 Input integrity.** Every §2 input
  hashes to its freeze-record value. A
  mismatch closes the run as **CLOSED AT
  STEP 0 — INPUT PIN MISMATCH**, naming the
  input.
- **0.2 Passage producible.** The source
  document can be produced from the program's
  held copy, and both anchor lines and the
  anchor sentence are located in it verbatim.
  If any of the three cannot be located, the
  run closes as **CLOSED AT STEP 0 — PASSAGE
  NOT PRODUCIBLE**, naming what was not
  found. A passage that cannot be produced
  cannot be re-extracted, and a run that
  proceeded from memory or from another
  edition would be repairing the record with
  a different book.
- **0.3 Passage pinnable.** The byte slice
  defined in §2 is cut from the produced
  document and its SHA-256 recomputes to the
  freeze-pinned passage digest. A mismatch
  closes the run as **CLOSED AT STEP 0 —
  PASSAGE PIN MISMATCH**. This is the
  fail-closed form of the task this spec was
  drafted under: a passage that is not
  producible *and* pinnable closes the run;
  it is never approximated.

## 4. Step 1 — re-extraction (the protocol)

Re-extraction is two independent passes over
the pinned passage, followed by a recorded
reconciliation (**DECIDED-BY-DRAFT,
DD-056-4**). The judgement this spec turns
on — argument versus catalogue observation —
is a judgement, and the protocol makes it
inspectable instead of leaving it to one
unrecorded reading.

1. **Pass A and Pass B, independently.** Each
   pass reads only the pinned passage (and
   §5's recovery test) and produces an
   **extraction sheet**: every candidate
   proposition the pass finds the passage
   asserting or arguing about sign 821, each
   candidate carried as (a) a verbatim quote
   of the passage sentence(s) it rests on,
   with printed-page locator; (b) the
   proposition stated in plain words, in the
   pass's own words, claiming nothing the
   quote does not say; and (c) the pass's
   §5 checklist result for that candidate.
   A pass that finds no candidate says so on
   its sheet, in words; an absent sheet is a
   failed protocol, not a negative result.
2. **Quote discipline.** No candidate exists
   without its quote. Paraphrase is never
   credited as the passage's argument, a
   proposition assembled from sentences in
   different parts of the book is not a
   candidate (the §2 bounds bind both
   passes), and neither pass may consult the
   claim record's adopted explanation, the
   design packet, this spec's §1, or any
   corpus or positional result while
   extracting — the passes read the passage,
   not the program's hopes for it.
3. **Reconciliation.** The candidate set of
   record is the union of the two sheets.
   Where the passes disagree on a candidate —
   one lists it and the other does not, or
   their §5 checklists differ — the
   reconciliation entry quotes the passage
   text that settles the point, or records
   the disagreement as unsettled. An
   unsettled disagreement on the decisive
   candidate is not resolved by vote or by
   seniority: the candidate is treated as
   **not recovered**, and the disagreement is
   carried into the outcome record verbatim.
   (A recovery that only one reading can see,
   and quotation cannot settle, is not a
   recovery the record can stand on.)
4. **The sheet is the evidence.** Both
   sheets and the reconciliation are
   deliverables of the execution (§8),
   whatever the outcome. A RECOVERED outcome
   whose sheet does not show its work, and a
   RETIREMENT RECOMMENDED outcome whose
   sheets do not show the search, are both
   non-compliant on their face.

## 5. Step 2 — the recovery test (what counts as recovering a claim)

A candidate proposition from the reconciled
sheet is a **recovered claim** if and only if
it passes every condition below. The
conditions are the program's claim form,
applied to a passage: a proposition, an
identified subject, and a statable way to be
wrong.

- **R-1 Stated from the passage's own
  argument.** The proposition is something
  the passage asserts or argues — not a
  topic it mentions, not a figure it prints,
  and not the bare fragment restated. "Sign
  821 is used in a variety of contexts" fails
  R-1 as a recovery in its own right: it is
  the fragment, and re-extracting the
  fragment is not recovering a claim.
- **R-2 A specific contention.** The
  proposition takes a position that a
  contrary finding could oppose — for
  example (the design's own illustrations,
  not findings of this draft) that the sign's
  spread across contexts rules out a narrow
  meaning, or that the sign carries a
  specific classification or reading in a
  stated context. A catalogue observation —
  a listing of occurrences, forms, or
  contexts with no contention drawn from
  them — fails R-2 however detailed it is.
- **R-3 Identified subject.** The sign list
  the passage's numbering belongs to is
  named **from the document itself** (its
  sign apparatus, headings, or citations),
  and the drawn sign its 821 labels is
  identified by one of two routes: an entry
  in the program's crosswalk registry
  matched by drawn form (never by number
  alone), or the source list's own published
  entry for the sign, quoted with its
  locator. Numbers are not identities: the
  registry's `Yunmapped_0821` row is a
  Yajnadevam glyph identifier, not Wells's
  821, and a run that treats it as the
  passage's sign is non-compliant on its
  face. If R-1 and R-2 pass but R-3 cannot
  be satisfied, the run does **not** retire
  the fragment and does **not** recover the
  claim; it closes as **IDENTIFICATION
  FAILED** (**DECIDED-BY-DRAFT, DD-056-2**;
  the fragment family's standing closure —
  design D-15 step 1, design D-18 step 1 —
  applied to the one case the design's
  binary outcome set does not map, defect
  D-1 in adjudication.md).
- **R-4 A statable falsification condition,
  from the passage's own logic.** The
  recovered claim carries, in words, an
  observation or result that would count
  against it, derived from what the passage
  itself claims — not a generic "further
  evidence might disagree". A proposition
  for which no such condition can be written
  without inventing one fails R-4: inventing
  a falsifier for a passage that argues
  nothing falsifiable is the failure mode
  this whole act exists to end.
- **R-5 Numbers and conditions attached.**
  Where the passage states quantities,
  contexts, or conditions for its contention,
  they are carried into the recovered claim
  verbatim or by exact reference. A recovery
  that keeps the contention and drops its
  stated conditions has manufactured a
  stronger claim than the source made, and
  fails R-5.

**Designing the recovered claim's test.**
Following the design, where a claim is
recovered a test is *designed* against it at
that point, as part of the recovery output:
the test-design note states what would be
checked, on what named data, against the
R-4 condition. Designing that test now,
before the argument is known, would be
inventing it, and this spec does not. The
note is a design, not a run: **no test is
executed under this spec** (§7, claim
F056-C11).

## 6. Outcomes (fixed in advance; exactly one is reached)

- **RECOVERED** — at least one reconciled
  candidate passes R-1 through R-5. The
  recovered claim is recorded in the form
  §7 fixes. If several candidates pass, each
  is recorded; the headline outcome is
  RECOVERED and names the count.
- **RETIREMENT RECOMMENDED** — no reconciled
  candidate passes R-1, R-2, R-4, or R-5
  (the identification condition R-3 is not
  reached, or is reached and satisfied, but
  no proposition survives the argument
  conditions). The retirement is recorded in
  the mechanical form §7 fixes.
- **IDENTIFICATION FAILED** — a candidate
  passes the argument conditions but R-3
  cannot be satisfied. A closure, not a
  retirement and not a recovery (§5, R-3).
- **CLOSED AT STEP 0** — a §3 gate fails, in
  its named class (INPUT PIN MISMATCH /
  PASSAGE NOT PRODUCIBLE / PASSAGE PIN
  MISMATCH).

The mapping is total over the protocol's
results: every reconciled sheet lands in
exactly one outcome, and no outcome word
exists outside this section.

### 6.1 Pre-written outcome wordings

The outcome record's headline paragraph uses
one of these forms, with the bracketed
material filled from the run:

- RECOVERED: "Re-extraction of the passage
  of record (Wells 2015, 'The Dholavira
  signboard, revisited', printed pp. 90–94;
  passage digest [digest]) recovers a claim
  the fragment did not state. The passage
  argues: '[recovered proposition, in plain
  words]' (passage: '[verbatim quote]',
  printed p. [page]). The sign list is
  [list, named from the document at
  locator], and the sign is identified as
  [identification, by route]. Falsification
  condition, from the passage's own logic:
  [condition]. The claim enters the
  lifecycle at the created stage, untested,
  as an appended restatement on the
  fragment's own record; a test design is
  recorded with it and no test has been run.
  Recovery establishes that the passage
  argues this — it establishes nothing about
  whether the argument is right, and nothing
  about sign 821 beyond it."
- RETIREMENT RECOMMENDED: "Re-extraction of
  the passage of record (Wells 2015, 'The
  Dholavira signboard, revisited', printed
  pp. 90–94; passage digest [digest])
  recovers no claim. Two independent
  extraction passes over the full passage
  found [no candidate proposition / only
  candidates failing the recovery test at
  R-[n], named on the sheets]: the passage
  is a catalogue observation with no
  argument attached that states a testable
  proposition about sign 821. The fragment
  'sign 821, used in a variety of contexts'
  is an extraction artefact — a table cell
  presenting as a claim a proposition the
  source never made — and its retirement is
  recommended and recorded by the appended,
  dated disposition in §7's form. The
  fragment's prior records stand unedited
  as its history. Nothing about sign 821 is
  decided by this outcome."
- IDENTIFICATION FAILED: "Re-extraction
  found a specific argument in the passage
  of record ('[verbatim quote]', printed
  p. [page]), but the claim cannot be
  recovered in the program's form: [the
  document does not name the sign list its
  numbering belongs to / the drawn sign
  could not be identified by either route
  §5 R-3 allows]. The fragment is neither
  recovered nor retired; it stays a stated
  gap, with this closure as the record of
  why, and the unblocking act is [named act:
  the identification evidence that would
  satisfy R-3]."
- CLOSED AT STEP 0: "Spec 056 closed before
  re-extraction: [input [name] did not hash
  to its frozen pin / the passage could not
  be produced from the program's held copy —
  [anchor or sentence] not located / the
  passage slice did not recompute to its
  frozen digest]. No extraction pass was
  run, the fragment stands exactly as
  recorded, and no statement about the
  passage, the fragment, or the sign is
  made."

## 7. What the outcomes write (the mechanical form)

Outcomes append records. Nothing under this
spec edits, deletes, or rewrites any prior
record — not the extracted-claims file, not
the Phase-104 evaluation, not the lane-2
adopted texts, not this spec's own frozen
text.

**On RECOVERED, execution writes:**

1. the outcome record in this directory
   (§8), carrying the §6.1 wording;
2. an appended, dated **restatement entry**
   on the fragment's own claim record
   (**DECIDED-BY-DRAFT, DD-056-3**): the
   recovered proposition in plain words, its
   verbatim passage quote and locator, the
   named sign list and the identification
   (route and reference), the R-4
   falsification condition, the R-5 numbers
   and conditions, and the test-design note
   (§5). The fragment's original entry stands
   above the append, unedited, as the record
   of what was recovered *from*;
3. the LEDGER entry (H1) and the
   experiment-graph node record (H15/H23).

The recovered claim's lifecycle position is
fixed here and is part of the outcome's
meaning: it enters at the **created** stage,
status **untested**. Recovery is not
checking, not explanation, not acceptance.
The claim has been *stated properly for the
first time*; everything the lifecycle asks
after creation still lies ahead of it, under
its own future acts. No output may present
the recovered claim as supported, checked,
or digested, and the restatement entry says
so in its own text.

**On RETIREMENT RECOMMENDED, execution
writes — and "retired on the record" means
exactly these entries, no more and no less:**

1. the outcome record in this directory
   (§8), carrying the §6.1 wording and both
   extraction sheets with the reconciliation;
2. an appended, dated **disposition entry**
   on the fragment's own claim record,
   stating: disposition RETIREMENT
   RECOMMENDED — EXTRACTION ARTEFACT; the
   passage of record (document, anchors,
   digest); the recovery test result in
   summary (candidates found, the condition
   each failed); and the sentence "This
   fragment is retired as a claim awaiting a
   test: it states no proposition, and none
   was recovered from its source passage.
   This entry appends a disposition; it does
   not alter the fragment's original record,
   which stands above as history.";
3. the LEDGER entry (H1) recording the
   recommendation as the fragment's terminal
   disposition under this spec, and the
   experiment-graph node record (H15/H23).

That is the mechanical content of retirement
here: from the disposition entry onward, the
fragment's live reading is *retired
artefact, on the recommendation this spec
records* — it is no longer presented, in any
program surface that reads the claim record
with its appends, as a claim awaiting a
test. The fragment is not deleted; its
extracted record, its Phase-104 evaluation,
and its adopted lane-2 explanation all stand
unedited, and any reader can still see
exactly what was retired and why. The
execution *recommends and records* the
retirement by these appends; it performs no
deletion, no withdrawal of any public
registration, and no edit to any other
claim's record. If a further program act is
required to strike the fragment from a
listing this spec does not name, that act is
outside this spec and is named in the outcome
record as outstanding rather than performed
silently (OPEN-6 in adjudication.md).

**On IDENTIFICATION FAILED or CLOSED AT
STEP 0,** execution writes the outcome
record with its §6.1 wording, the LEDGER
entry, and — for IDENTIFICATION FAILED only —
an appended, dated closure entry on the
fragment's claim record stating the gap and
the unblocking act. The fragment's stage and
status are unchanged by a closure.

## 8. Reporting obligations

Every product of an execution carries:

1. the passage of record identified in full:
   document, start and end anchor lines,
   printed pages, and the passage digest —
   with the anchor sentence quoted verbatim;
2. both extraction sheets and the
   reconciliation, in full (on a step-0
   closure: the gate record instead, naming
   the failed gate and the observed values);
3. for every reconciled candidate: its
   verbatim quote, its plain-words
   proposition, and its R-1…R-5 checklist
   result with the failing condition named
   where one fails;
4. the outcome word of §6 and the §6.1
   headline wording for the outcome reached;
5. on RECOVERED: the recovered claim exactly
   as appended (§7), including its lifecycle
   position (created, untested) and its
   test-design note; on RETIREMENT
   RECOMMENDED: the disposition entry exactly
   as appended (§7);
6. the fence sentence: "This act is record
   repair. It establishes, at most, what the
   source passage argues — never whether the
   argument is right, and nothing about sign
   821 itself."

Deliverables at execution: the extraction
record (sheets, reconciliation, checklists)
as a file in this directory, the outcome
append in this directory, the §7 append(s)
to the claim record, the experiment-graph
node (H15/H23, registered and verified
before the run), and the LEDGER entry (H1).
Foundation check (H21) after the execution
phase: 0 failures, or the outcome record
says why not. Anchors asserted byte-identical
before and after.

Execution order within the campaign (plan
Part 4, Wave 3): **this spec executes in
group 2, the independent executions.** It
consumes no shared asset and no other
member's output, and no member consumes its
output inside the pass: a recovered claim
queues for its own later acts, exactly as
the campaign plan provides for work a pass
surfaces but does not contain.

## 9. Controls and named confounders

- **Importing an argument from elsewhere in
  the book.** The book argues about sign 821
  in at least two other places (§2). Crediting
  one of those arguments to this fragment
  would repair the record with a proposition
  its extraction never pointed at. Controlled
  by the §2 bounds, the §4 quote discipline,
  and claim F056-C07.
- **The drafter's and executor's prior
  knowledge.** Anyone who has read the book
  knows it contains a suggested reading for
  this sign in signboard contexts. That
  knowledge is not evidence under this spec:
  the recovery test runs on the pinned
  passage's text, through two independent
  sheets, and a candidate that cannot be
  quoted from the passage does not exist for
  this act — in either direction. Prior
  knowledge may not rescue a candidate, and
  it may not bury one either.
- **Number collision.** Identical numbers
  name different signs in different systems
  (the registry's `Yunmapped_0821` is the
  standing trap, §5 R-3). Controlled by
  R-3's drawn-form / list-entry routes and
  its number-matching ban.
- **The truncated fragment.** The claim
  record's quote is cut mid-reference
  ("(Figure 6"). Controlled by pinning the
  passage from the source document (§2),
  never from the record's fragment text.
- **Single-reader judgement.** Argument
  versus catalogue observation is the act's
  one real judgement call. Controlled
  structurally: two independent passes,
  a union candidate set, reconciliation by
  quotation, and unsettled disagreement
  resolving *against* recovery (§4.3) — the
  bias of the protocol runs toward the
  outcome that claims less.
- **Glyph loss in the held text.** The
  cleaned text drops sign glyphs and the
  figure is graphic-only (§2). A contention
  carried only by a glyph or by Figure
  6.13's images cannot be quoted from the
  passage of record and cannot be recovered
  under §5; the limit is stated wherever the
  outcome is stated, and the freeze is asked
  whether the figure joins the passage of
  record (OPEN-4).

## 10. Epistemic limits (binding on all outputs)

1. **Nothing about sign 821.** This is
   record repair, honestly labelled (the
   design's own limit, carried verbatim in
   substance). Neither outcome decides
   anything about the sign: not its reading,
   not its classification, not its
   distribution, not its meaning.
2. **Recovery is not verification.** A
   RECOVERED outcome establishes that a
   passage argues a proposition statable in
   the program's claim form. The proposition
   enters at created, untested (§7), and no
   output may borrow for it any credit from
   the act of recovering it.
3. **Retirement is not refutation.** A
   RETIREMENT RECOMMENDED outcome establishes
   that the *fragment* states no recoverable
   proposition. It does not establish that
   anything the source book says about sign
   821 elsewhere is false, and it reaches no
   passage outside §2's bounds.
4. **The passage as held.** All findings are
   findings about the held cleaned text —
   glyph slots blank, figure graphic-only
   (§2, §9). A finding about the printed
   book beyond its held text is outside this
   spec.
5. **Closures are not outcomes about the
   fragment.** IDENTIFICATION FAILED and
   CLOSED AT STEP 0 state why the deciding
   act could not complete; neither may be
   reported as evidence for recovery or for
   retirement.
6. Negative, retirement, and closure
   outcomes publish with the same prominence
   as a recovery.

## 11. Risks and honest weaknesses

- **RETIREMENT RECOMMENDED is a live, real
  possibility the design prices in.** The
  fragment's sentence, on its face, is a
  catalogue observation; whether the
  surrounding section argues more is exactly
  what execution decides. A retirement is a
  result the record needs, not a failure of
  the run.
- **The recovery test's centre is a
  judgement.** R-2 (specific contention
  versus catalogue observation) cannot be
  made mechanical. §9's controls make the
  judgement inspectable and bias it toward
  claiming less; they do not eliminate it,
  and the outcome record must not pretend
  otherwise.
- **The passage bounds are this draft's
  reading.** The design did not bound "the
  source passage" (defect D-2). The headed
  section is the smallest unit that contains
  the anchor sentence's full discussion; a
  narrower bound would repeat the extraction
  error, a wider one would import other
  discussions. The freeze confirms or
  re-bounds openly (OPEN-1) — before any
  extraction pass runs, never after.
- **Identification may fail on a real
  argument.** The registry carries no W821
  entry (verified at draft), so R-3's
  registry route may be unavailable and the
  list-entry route carries the weight. If
  both fail, IDENTIFICATION FAILED is the
  honest outcome and is pre-written.

## 12. Stop conditions and outcome classes

Execution ends in exactly one of:

- **RECOVERED** — §6, after all gates pass
  and at least one candidate passes R-1…R-5.
- **RETIREMENT RECOMMENDED** — §6, after all
  gates pass and no candidate survives the
  argument conditions.
- **IDENTIFICATION FAILED** — a candidate
  passes the argument conditions and R-3
  cannot be satisfied.
- **CLOSED AT STEP 0** — INPUT PIN MISMATCH,
  PASSAGE NOT PRODUCIBLE, or PASSAGE PIN
  MISMATCH (§3).

## 13. Execution shape (gated; NOT run by this draft)

1. **Graph-first build** (H15/H23) — script,
   graph node, registration, verification.
2. **Step 0** (§3) — input integrity, passage
   producible, passage pinnable. Fail-closed:
   any failure ends the execution in its
   named closure class.
3. **Step 1** (§4) — two independent
   extraction passes over the pinned passage;
   extraction sheets; reconciliation.
4. **Step 2** (§5) — the recovery test over
   the reconciled candidate set, including
   the R-3 identification routes where a
   candidate reaches them; on RECOVERED, the
   test-design note.
5. **Outcome** (§§6–8) — the outcome record
   under the pre-written wording, the §7
   append(s), the LEDGER entry; anchors
   asserted byte-identical; foundation check
   reported as measured.

## 14. What this spec is not

Not a test of any reading of sign 821, not a
corpus statistic, not an identification
concordance (that is design D-18's shape, for
a fragment that states an identification),
not a decipherment, and not an authorisation
to execute. It is a recovery act for one
fragment, designed so that its two honest
outcomes — a claim recovered in proper form,
or a fragment retired on the record with the
reason written down — are both written in
advance, and the passage, not the program,
chooses between them.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
