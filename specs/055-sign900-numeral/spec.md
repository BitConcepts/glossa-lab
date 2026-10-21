# Spec 055 — "Sign 900 Means Six": Identify the Sign, Then Test It as a Numeral (Design D-15)

> ## DESIGN DRAFT — FOR FREEZE DECISION — 2026-10-21
>
> Drafted under the runnable-experiments
> campaign plan approved by the owner AS
> WRITTEN on 2026-10-21
> (`~/workspace/your_files/2026-10-21-runnable-experiments-campaign-plan.md`,
> Parts 1–4): campaign member 11, design
> D-15, one of the fragment recoveries
> (independent members, drafted in parallel
> throughout Wave 1). **The freeze and the
> execution of Spec 055 are separate later
> acts.** No AEE lifecycle hooks have run
> on this draft; they are a freeze gate.
> Nothing in this draft has been run,
> frozen, registered, or computed.
> Drafting merges nothing.
>
> The execution phase number is **unassigned**
> at this draft. Spec 055 allocates its phase
> number at the freeze act, from the merged
> record as it then stands (DD-055-7).
>
> **Chain rule (campaign decision E-7).**
> Step 1 of this spec is a source-table
> recovery — the act that *would* unblock
> design D-16 (the rival "sign 700"
> fragments). Its output is preserved as a
> record of this spec (§6). **D-16 does not
> join this campaign even if the recovery
> succeeds; D-16 waits for its own planning
> gate.** This spec designs no part of
> D-16, tests no sign-700 claim, and makes
> no finding about sign 700 (§9, claim
> F055-C09).

**Design source:** D-15 in the experiment-design
packet at PR #195
(`docs/research/experiment-designs-2026-10-13/03-fragments.md`,
§D-15, read in full at this draft).

**Claim under test:**
`ancient_writing_and_modern_technologies_51831ac9_sign_val_0001`
— UNTESTED fragment, in full: "Sign value:
900 / number six".

**AI disclosure:** this draft is produced by an
AI agent (Muse Spark, via Muse) at the
direction of Tristen Pierson, per constitution
§VI.

---

## 1. The claim and the record it stands on

The record is a fragment. Automatic extraction
pulled a single cell out of a source document
and kept the sign number and the proposed
value while losing the sign list the number
belongs to. The claim record
(`glossa-indus/claims/extracted_claims/ancient_writing_and_modern_technologies_51831ac9.json`,
pinned in §2) states, verbatim:

> "Sign value: 900 / number six"

The source document is Andreas Fuls,
"Ancient Writing and Modern Technologies –
Structural Analysis of Numerical Indus
Inscriptions" (Technische Universität
Berlin), held by the program as cleaned text
(`glossa-indus/processed/cleaned_text/ancient_writing_and_modern_technologies_51831ac9.txt`).
Read first-hand at this draft, the held text
contains the material the fragment points
at, under headed sections rather than in a
single sign-value table (adjudication.md §6,
defect D-2):

- under **SPECIAL NUMERICAL SIGNS**, the
  section headed **"Sign 900"** (printed
  p. 68): "Sign 900 may well be regarded as
  a special numerical sign… The absence of
  numbers greater than five may indicate
  that Sign 900 represents number six",
  with repetitions of the sign (its signs
  904, 914, 908) read as multiples of six;
- under **NUMERICAL VALUES OF SIGNS**, the
  section headed **"Numerical value of Sign
  900"** (printed pp. 72–74), which derives
  the value from three two-sided tablets and
  a table of possible solutions (its
  Table 1), argues against Wells's rival
  value of five, and concludes for six;
- in the **SUMMARY** (printed p. 85): "The
  numerical value of Sign 900 is six as
  verified in Figures 16, 18, and 21."

The same text states, in its opening section
(printed p. 57) and under the heading **SIGN
LIST** (printed p. 59), that its signs "are
coded according to an extended sign list
with 702 distinct signs (Wells 2015)" and
that "the sign list by Wells (2011, 2015)
has been extended to currently 702 distinct
signs". That is the reading this draft
expects step 1 to confirm. It is **not** an
identification: the identification is the
execution's recovery act, performed on the
document and preserved as a record (§§4, 6),
because other work waits on that record —
not on this draft's reading.

Phase-104 evaluated this record and stopped
at the door (RULE-NUM): the sign number is
cited without a stated numbering system, no
matching entry was located in the program's
crosswalk registry (86 numeric IDs present in
that record), and the extraction carries no
falsification condition. The claim's own
adopted explanation states what is unknown:
which sign, in which published sign list,
this number refers to.

One trap is fixed here, at draft, because the
record has changed since Phase-104: the
crosswalk registry as held today (803 rows,
pinned in §2) **does** contain a `W900` value
— inside the `wells_ids` cell of the P154 row
("Right parenthesis (perhaps with a backward
curve at the bottom)"). A string search now
"finds" 900 where Phase-104 found nothing.
That cell is not an identification of this
fragment's sign: numbers and registry cells
are not identities, and §4 forbids matching
by number or by string. Whether the drawn
sign Fuls numbers 900 is the drawn sign on
that registry row is exactly what step 1
must establish by drawn form, or fail.

### 1.1 The question, in plain words

A paper assigns the value "six" to a sign it
numbers 900. Two questions, in order. First:
which drawn sign is that — can the source
document itself name its sign list and show
the sign its number labels? Second, only if
the first is answered: does that sign behave
the way a numeral behaves in the inscriptions
— in short texts, next to other numerals,
spread across positions the way the known
numeral signs are — or does it behave like an
ordinary sign?

### 1.2 The hypothesis and its falsifier

**Hypothesis.** The sign the source numbers
900 is a numeral sign: on the frozen measures
of §5, its behaviour resembles the script's
known numeral signs more than it resembles
frequency-matched ordinary signs'.

**Falsifier — two stages, by design.**
Either stage falsifies, and the first stage's
failure is a pre-registered outcome, not a
gap dressed up:

1. **Identification stage.** The source
   document does not identify the sign: its
   sign list cannot be named from the
   document's own text, or the drawn sign
   its number 900 labels cannot be matched.
   The design closes as **IDENTIFICATION
   FAILED**, and the record's honest
   disposition is a stated gap — not a
   verdict on "six".
2. **Behaviour stage** (only if stage 1
   succeeds). The identified sign's behaviour
   contradicts the numeral reading: on the
   §5 measures it is indistinguishable from
   frequency-matched ordinary signs, or
   unlike the known numeral set — recorded
   as **NOT NUMERAL-LIKE** (or **MIXED**,
   where the measures split).

**What even a full pass would NOT establish**
(design D-15's own limit, carried verbatim in
substance): that the sign's value is *six*
specifically, as against four or seven.
Distributional behaviour can support "this
sign is a numeral"; picking the exact number
needs evidence of a different kind (counted
depictions, bilingual material) that this
program does not hold. No output of this
spec may state the value six as established
(§9, claim F055-C15).

## 2. Inputs (pinned at this draft; re-asserted at the freeze)

| Input | Pin / state |
|---|---|
| Claim record (`glossa-indus/claims/extracted_claims/ancient_writing_and_modern_technologies_51831ac9.json`) | SHA-256 `e98190894202a2a1c0e314229dcb585c62a0f5c12c059bcabd63b055c42959e8` (recomputed at this draft from `main` at 83b6a563) |
| Source document, held cleaned text (`glossa-indus/processed/cleaned_text/ancient_writing_and_modern_technologies_51831ac9.txt`) | SHA-256 `1275b795903260221f5226bada352de27471c010e2ad8ace556c548c20da1fc4` (recomputed at this draft) |
| Source literature record (`glossa-indus/literature/documents/ancient_writing_and_modern_technologies_51831ac9.json`) | SHA-256 `92e19e6def7eccb42ba0e9f53f5ef3bf9dbb0b9717aa3d675cecb971f5ab0e5c` (recomputed at this draft; records the original PDF, file size 3,565,316 bytes, intake checksum `51831ac9…`, license status "unclear" — see §7) |
| Phase-104 evaluation (`glossa-indus/reports/phase104_claims_evaluation.json`) | SHA-256 `2d0b83e8055a04b96635007054cfadde472f605dc7e5b249a61c8f9ea89b858d` (recomputed at this draft) |
| Crosswalk registry (`data/crosswalks/canonical_sign_registry.csv`) | SHA-256 `8a0b2a82ac8d226d574ce01f5550c581efd91a97cab86201a62f7a7e435bd420` (recomputed at this draft; 803 rows as held today — the registry has grown since Phase-104's 86-numeric-ID record, and execution re-asserts this pin rather than inheriting either count) |
| Lane-2 adopted drafts (`specs/029-tao-claim-lifecycle/lane2-drafts/drafts.json`) | SHA-256 `3f645c9a4132ba5a0bc5fca4ca22810b8b6169a2f1f9f85f35990c7b72df33fb` (recomputed at this draft) |
| Anchors file (`backend/reports/INDUS_FINAL_ANCHORS.json`) | SHA-256 `df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569` (recomputed at this draft). This spec moves no anchor; the file is asserted byte-identical before and after any execution. |
| Strict corpus (behaviour test, §5) | **No file pin is stated at this draft, deliberately.** As Spec 048's draft records for the same layer, the strict corpus is "the program's V3 / Mahadevan-lineage corpus as held in the database" — a database posture, not a pinnable repository file on `main`. The layer is therefore identified, exported, and pinned by digest at the step-2 gate (§3, gate 0.4), before any counting, and the run closes if it cannot be (DD-055-5; OPEN-4). Inventing a pin at draft would repeat the stale-pin failure Spec 040's gate record documents. |

The drawn-sign figures of the source (its
Figures 11 and 12, examples of sign 900 and
of its repetitions 904/908/914; Figure 29,
the signs used in the analysis) exist in the
original PDF, not in the held cleaned text,
which carries captions only. Step 1's
drawn-sign matching (§4.2) therefore works
from the published sign list the document
names and from the crosswalk registry, with
the PDF's figures as a cited check where the
held PDF can be produced (§3, gate 0.2).

## 3. Step 0 — gates before any identification or counting (fail-closed)

Execution runs these checks in order, before
step 1. A failure closes the execution in
the class named; nothing is repaired at run
time, and no source is substituted.

- **0.1 Input integrity.** Every §2 input
  that carries a pin hashes to its
  freeze-record value. A mismatch closes
  the run as **CLOSED AT STEP 0 — INPUT PIN
  MISMATCH**, naming the input.
- **0.2 Source producible.** The source
  document can be produced from the program's
  held copy and the §1 material located in
  it verbatim (the "Sign 900" section, the
  "Numerical value of Sign 900" section with
  its Table 1, and the summary statement).
  If it cannot, the run closes as **CLOSED
  AT STEP 0 — SOURCE NOT PRODUCIBLE**. The
  recovery record (§6) is still produced,
  in its closure form.
- **0.3 Recovery before verdict.** No
  identification wording, in either
  direction, is recorded anywhere before
  the §6 recovery record exists. The
  recovery is the first product of the
  execution, not a summary written after
  it.
- **0.4 Corpus gate (before step 2 only).**
  If step 1 succeeds, and before any
  counting: the strict-corpus layer of
  record is identified, exported, and pinned
  by SHA-256 in the step-0 record, and the
  identified sign's representation in that
  layer is established by its crosswalked
  corpus identifier (§4.2). If the layer
  cannot be pinned, the run closes as
  **CLOSED AT STEP 0 — CORPUS NOT
  PINNABLE**. If the identified sign is not
  represented in the pinned layer, or is
  represented by fewer than **5 occurrences**,
  the run closes as **IDENTIFIED — TOO FEW
  OCCURRENCES TO TEST**, with the count
  named (DD-055-4; OPEN-3). No measure is
  computed past a failed gate.

## 4. Step 1 — identification and the source-table recovery

Step 1 is a recovery, performed on the source
document itself, and preserved as a record
in the fixed form of §6. Its success and
failure conditions are precise, and both are
pre-registered outcomes.

### 4.1 Name the sign list from the document itself

From the document's own text — its headings,
introduction, sign-list section, or
citations — name the published sign list
that numbers the document's signs. The
reading this draft expects, from the held
text, is the extended Wells (2011, 2015)
list of 702 distinct signs (§1). Step 1 must
confirm that from the document's own
statements, quoting each naming statement
verbatim with its locator, not assume it
from this draft. If the document does not
name its list, the design closes as
**IDENTIFICATION FAILED (list unnamed)**,
and the record stays a stated gap.

### 4.2 Match the drawn sign

The sign the document numbers 900 is matched,
by its drawn form, to an entry in the
program's crosswalk registry, or — if the
registry carries no entry for the drawn
sign — fixed by a drawn-sign reference to
the named published list's own entry for
900. The citation is attached either way,
and the match (registry id, or the list
locator) is recorded in the §6 recovery
record's `target_sign` block. If the drawn
sign cannot be matched, the design closes
as **IDENTIFICATION FAILED (sign
unmatched)**.

**Numbers are not identities.** A sign number
is meaningful only inside its own list.
Matching is by drawn sign (through the
crosswalk registry or drawn-form comparison
against the named list), never by number and
never by a registry string. The trap is on
record in the registry itself, read at this
draft: a `W900` value sits inside a
`wells_ids` cell on the P154 row ("Right
parenthesis…"). That cell neither identifies
nor excludes this fragment's sign; a run that
treats it as the identification — or that
treats its drawn description as a refutation
without drawn-form comparison against the
named list's sign 900 — is non-compliant on
its face (claim F055-C07).

### 4.3 The recovery's scope — and where it stops

The recovery recovers, verbatim and with
locators, the full material the extracted
cell was pulled from, as it stands in this
source (§6 fixes the form): the document's
sign-list naming statements; the complete
"Sign 900" section; the complete "Numerical
value of Sign 900" section, including its
Table 1; the summary statement; and the
figure captions that carry the drawn sign
(Figures 11, 12, 29). Because the same
document's numerical-signs discussion also
carries the sign-700 statements the D-16
fragments were extracted from, the recovery
record notes where those statements stand
in the recovered material (locators only).
It adjudicates nothing about them. That is
the whole of the chain: the recovered record
is preserved (§6), and under campaign
decision E-7 **D-16 does not join this
campaign even if the recovery succeeds**
(§9, claim F055-C09).

Only a sign identified under this step is
tested in step 2.

## 5. Step 2 — the numeral-behaviour test (only if step 1 succeeds)

### 5.1 The reference sets, fixed before counting

Before any measure is computed, two sets are
fixed in a pre-counting record, from
published identifications only:

- **The known-numeral set.** The script's
  known numeral signs — the stroke-like
  signs that appear in counting patterns and
  the special numerical signs identified as
  such in published sources (the source
  document's own SPECIAL NUMERICAL SIGNS
  discussion is one such source, not the
  only one) — each member listed with its
  published source and its identifier in the
  pinned corpus layer. **The target sign is
  not a member of this set.** Its published
  identification is the claim under test;
  including it would let the claim stock its
  own reference range (DD-055-3). A numeral
  candidate whose published identification
  is itself hedged in its source is recorded
  as hedged in the set record; the freeze
  decides whether hedged members enter the
  set (OPEN-5).
- **The control set.** Ordinary signs —
  members of neither the numeral set nor the
  target — frequency-matched to the target
  under a fixed rule. This draft fixes the
  rule as: the **10 ordinary signs whose
  occurrence counts in the pinned layer are
  closest to the target's count**, ties
  broken by corpus identifier in ascending
  order; if fewer than 10 ordinary signs
  exist, all of them (DD-055-6; OPEN-2).
  Fixing the set requires the target's
  occurrence count and the layer's frequency
  table — a census, taken after gate 0.4 and
  recorded in the pre-counting record. No
  §5.2 measure is computed before the
  pre-counting record exists.

### 5.2 The three measures (fixed in advance)

Computed identically for the target, for
every known-numeral set member, and for
every control sign, on the pinned layer:

1. **Short-text share** — the share of the
   sign's occurrences that stand in
   inscriptions of length three or less.
2. **Numeral adjacency share** — the share
   of the sign's occurrences immediately
   adjacent (on either side, in the corpus's
   stored sequence order) to another
   numeral-class sign. Numeral-class here
   means the known-numeral set of §5.1.
   Adjacency to another occurrence of the
   target itself does not count: the
   target's class is what is under test
   (DD-055-3).
3. **Positional entropy** — the Shannon
   entropy, in bits, of the sign's
   distribution over positions (position as
   stored in the corpus sequence), computed
   by the identical formula for every sign
   compared (DD-055-6; OPEN-6).

### 5.3 Outcome rules (fixed in advance; total)

For each measure, the target is:

- **numeral-side** if its value lies inside
  the known-numeral set's range (minimum to
  maximum) on that measure **and** its value
  differs from the control set's median on
  that measure in the direction of the
  known-numeral set's median (the design's
  "outside the control set's median", given
  an operational form at DD-055-6; OPEN-2);
- **control-side** if its value lies inside
  the control set's range (minimum to
  maximum) on that measure.

Let N be the number of measures on which the
target is numeral-side and O the number on
which it is control-side:

- **NUMERAL-LIKE** — N ≥ 2 and O < 2. The
  hypothesis (§1.2) stands at the behaviour
  stage: the sign behaves as a numeral sign
  behaves, on this layer, under these
  measures.
- **NOT NUMERAL-LIKE** — O ≥ 2 and N < 2.
  The falsifier fires at the behaviour
  stage: the sign's behaviour is
  indistinguishable from frequency-matched
  ordinary signs', or unlike the known
  numeral set's.
- **MIXED** — every other pattern, including
  N ≥ 2 with O ≥ 2 (the ranges overlap and
  the measures split) and patterns where
  neither side reaches two. Reported as
  such, with the per-measure table.

NUMERAL-LIKE is the only outcome that
supports the hypothesis, and it supports
only the numeral reading — never the value
six (§1.2, §9).

### 5.4 Pre-written verdict wordings — the full outcome set

The outcome record's headline paragraph uses
one of these forms, with the bracketed
material filled from the run:

- NUMERAL-LIKE: "The sign that Fuls's paper
  numbers 900 in the extended Wells (2011,
  2015) sign list — matched by drawn form to
  [crosswalk registry id / list locator] in
  Spec 055's recovery record — behaves as a
  numeral sign behaves in the pinned strict
  corpus: on [k] of the three frozen
  measures it sits inside the known numeral
  signs' range and away from the
  frequency-matched ordinary signs' median
  ([per-measure table]). The recovered claim
  is checked on the numeral question: this
  sign is a numeral sign. This does not
  establish that its value is six; a
  distribution can support 'numeral', it
  cannot count."
- NOT NUMERAL-LIKE: "The sign that Fuls's
  paper numbers 900, identified in Spec
  055's recovery record as [crosswalk
  registry id / list locator], does not
  behave as a numeral sign behaves in the
  pinned strict corpus: on [k] of the three
  frozen measures it sits inside the range
  of frequency-matched ordinary signs
  ([per-measure table]). The numeral reading
  the fragment carries is contradicted at
  the behaviour stage. The identification
  itself stands as recovered; what fails is
  the behaviour the reading predicts."
- MIXED: "The sign that Fuls's paper numbers
  900, identified in Spec 055's recovery
  record as [crosswalk registry id / list
  locator], splits the frozen measures in
  the pinned strict corpus ([per-measure
  table]): neither numeral-like nor
  ordinary-like on at least two. The
  numeral question is recorded as MIXED —
  the measures this design froze do not
  settle it, and no other measure may be
  substituted after the fact."
- IDENTIFICATION FAILED: "The fragment
  'sign 900 means six' cannot be carried to
  a behaviour test: [the source document
  does not name its sign list from its own
  text / the drawn sign its number 900
  labels could not be matched by drawn form
  to the crosswalk registry or to the named
  list's entry]. The record stays a stated
  gap — not a verdict on 'six', and not a
  verdict on the sign. Spec 055's recovery
  record preserves what the source does
  say, in full."
- IDENTIFIED — TOO FEW OCCURRENCES TO TEST:
  "The sign that Fuls's paper numbers 900 is
  identified in Spec 055's recovery record
  as [crosswalk registry id / list
  locator], and the fragment is thereby
  converted from a pointer into a claim. In
  the pinned strict corpus the sign is
  [not represented / represented by [n]
  occurrences, below the frozen floor of
  5], so the behaviour test cannot run as
  written. No measure was computed. The
  numeral question stands untested on this
  layer."
- CLOSED AT STEP 0: "Spec 055 closed before
  identification: [the source document could
  not be produced from the program's held
  copy / input [name] did not hash to its
  frozen pin / the strict-corpus layer could
  not be identified and pinned]. No
  identification was recorded and no
  statement about the sign is made. The
  recovery record carries the closure."

## 6. The recovery record — form fixed at draft (the preserved output of step 1)

This section fixes the recovery's output
exactly. The form is this draft's decision —
**DECIDED-BY-DRAFT (DD-055-1)**.

**Deliverable of record:** a machine-readable
file `source-table-recovery.json`, produced
at execution in this spec's directory
(`specs/055-sign900-numeral/`), plus its
human-readable rendering inside the outcome
record (§8). The JSON is the preserved
record; the rendering is for readers and
must not diverge from it. **The file is
produced on every terminal outcome** — on a
step-0 or identification closure it carries
its `closure` block and whatever recovery
material was established before the closure,
so the recovery's partial state is itself
preserved rather than lost.

**Top-level fields:**

- `producer_spec`: `"055"`;
  `producer_claim_id`: the claim id in the
  header of this spec; `schema`:
  `"glossa.source-table-recovery/1"`.
- `source_document`: `{document_id,
  title, author, held_text_ref,
  held_text_sha256, literature_record_ref,
  original_file (name, size, intake
  checksum, from the literature record)}`.
- `sign_list_naming`: `{list_named (string
  or null), naming_statements: [{quote
  (verbatim), locator (printed page and
  heading, as held)}]}`. `list_named` may be
  non-null only where a naming statement is
  quoted that supports it.
- `recovered_material`: an array of
  `{section_heading, locator,
  text_verbatim}` covering, at minimum, the
  "Sign 900" section, the "Numerical value
  of Sign 900" section with its Table 1
  rendered as text, and the summary
  statement; plus `figure_refs`: the
  captions (Figures 11, 12, 29) that carry
  the drawn sign, each `{figure, caption
  verbatim, locator}`.
- `target_sign`: `{source_sign_no: "900",
  drawn_sign_match_basis
  ("crosswalk-registry" | "named-list-entry"
  | null), crosswalk_registry_id (string or
  null), named_list_locator (string or
  null), match_citation}`. On an
  identification failure, `target_sign`
  records the basis attempted and the
  failure class.
- `sign_700_material`: `{present (boolean),
  locators: [...]}` — locators only, where
  the recovered document's numerical-signs
  discussion carries the sign-700 statements.
  No text is adjudicated, no value is
  recorded as a finding, and no D-16
  material is designed (§4.3, §9).
- `recovery_outcome`: one of
  `IDENTIFIED | IDENTIFICATION FAILED (list
  unnamed) | IDENTIFICATION FAILED (sign
  unmatched) | CLOSED AT STEP 0`, with the
  §5.4 wording used, in `closure` where the
  outcome is not IDENTIFIED.

**Locator form** (used in every field and in
every outcome product): printed page and
heading as they stand in the held cleaned
text — in shape, `p. 68, 'Sign 900' (SPECIAL
NUMERICAL SIGNS)`. A recovered item that
cannot be written with a locator is not a
recovered item; it is a step-1 failure,
recorded as such.

## 7. Controls and named confounders

- **Number collision (§4.2).** The standing
  trap of this fragment family: identical
  numbers naming different signs in
  different lists, and registry strings that
  now contain the number where Phase-104
  found none. Controlled by drawn-sign
  matching only, with the `W900` cell named
  in advance.
- **The source argues for its own value.**
  The source document does not merely state
  "six"; it argues for it, from counted
  objects and equations, and against a rival
  value of five. That argument is **not**
  this spec's test, and no part of it is
  evidence at the behaviour stage: step 2
  runs on corpus behaviour alone. A run
  that cites the source's derivation as
  support for NUMERAL-LIKE is non-compliant
  (claim F055-C15). The recovery preserves
  the argument verbatim because the
  recovery is a record of the source, not
  because the argument is adopted.
- **Self-stocking reference sets.** The
  target is excluded from the known-numeral
  set, and target-to-target adjacency does
  not count as numeral adjacency (§5.1,
  §5.2). Without both exclusions the test
  could pass the sign by comparing it with
  itself.
- **Corpus numbering is not source
  numbering.** The pinned strict corpus
  counts signs in its own lineage's
  numbering; the identified sign reaches it
  only through the §4.2 drawn-sign match and
  its recorded crosswalk. A count taken
  under any other identifier is a count of
  a different sign.
- **Frequency matching is a control, not a
  cure.** Rare signs have unstable shares on
  every §5.2 measure; the occurrence floor
  (gate 0.4) and the MIXED outcome exist
  because the design prices that in rather
  than arguing around it.
- **Rights posture of the source.** The
  literature record states the source's
  license status as "unclear" and its
  access as user-uploaded. The recovery
  quotes the held document inside the
  program's internal records, as the
  program's extraction already does; nothing
  in this spec publishes the source's text,
  and any later publication act carries its
  own rights check (campaign R-6).

## 8. Reporting obligations

Every product of an execution carries:

1. the §6 recovery record, or its closure
   form, exactly as produced;
2. the identification outcome before any
   behaviour quantity: the list named with
   its quoted naming statements, or the
   IDENTIFICATION FAILED class;
3. where step 2 ran: the pre-counting record
   (both reference sets, with sources), the
   per-measure table for target, numeral
   set, and control set, and the §5.4
   headline wording for the outcome reached;
4. the fence sentence: "This result is about
   how one identified sign behaves in
   recorded data. It is not evidence of what
   any sign means, and it does not establish
   the value six."
5. the chain sentence, verbatim in
   substance: "Design D-16 does not join
   this campaign even though this recovery
   is the act that would unblock it; D-16
   waits for its own planning gate (campaign
   decision E-7)."

Deliverables at execution:
`source-table-recovery.json` (§6, on every
terminal outcome), the results JSON of §5
where step 2 ran, the outcome append in
this directory, the appended entry on the
claim
`ancient_writing_and_modern_technologies_51831ac9_sign_val_0001`'s
record (identification outcome, and the
behaviour outcome where reached), the
experiment-graph node (H15/H23, registered
and verified before the run), and the
LEDGER entry (H1). Foundation check (H21)
after the execution phase: 0 failures, or
the outcome record says why not. Anchors
asserted byte-identical before and after.

Execution order within the campaign (plan
Part 4, Wave 3): **this spec executes in
group 2, the independent executions.** Its
recovery record is a record of this spec;
no member of this campaign consumes it, and
D-16 — outside the campaign — takes nothing
from this execution except through its own
future planning gate.

## 9. Epistemic limits (binding on all outputs)

1. **Not the value six.** Even NUMERAL-LIKE
   establishes only that the identified sign
   behaves as a numeral behaves. The exact
   value — six against four, five, or seven
   — is beyond distributional evidence, and
   the design says so rather than pretending
   a distribution can count (design D-15's
   own limit).
2. **Identification is not decipherment.**
   Step 1 fixes which drawn sign the fragment
   points at. It establishes nothing about
   what the sign meant in use beyond the
   numeral question step 2 tests.
3. **IDENTIFICATION FAILED is a result.**
   It is a statement about the source
   document and the record, pre-registered
   and reported with the same prominence as
   a pass. It is not a verdict on "six" and
   not a verdict on the sign.
4. **One corpus layer, as pinned.** The
   behaviour outcome is a statement about
   the identified sign's behaviour in the
   pinned strict corpus under the frozen
   measures. It is not claimed for any other
   layer or compilation.
5. **The chain stops here.** The recovery is
   preserved as this spec's record. It does
   not draft, test, adjudicate, or advance
   D-16 in any way; the sign-700 statements
   are located, not judged (§4.3).
6. Negative, mixed, thin, and closure
   outcomes publish with the same prominence
   as numeral-like.

## 10. Risks and honest weaknesses

- **IDENTIFICATION FAILED is a live
  outcome.** The document's naming
  statements are prose in a cleaned text,
  and its drawn signs survive only as
  captions there; the drawn-form match may
  rest on the named list's published entry
  alone. If that cannot be defended from
  the recorded reference, step 1 fails
  honestly and is pre-written.
- **The registry's `W900` cell cuts both
  ways.** It may be the target sign's row —
  or a different list's 900, or a Wells
  numbering from a different edition. The
  draft names it precisely so execution
  cannot quietly take either shortcut.
- **The target may be rare in the strict
  corpus.** The source's corpus is the ICIT
  lineage; the strict corpus is another
  compilation's lineage, reached through
  one crosswalk row. Few or zero
  occurrences there close the behaviour
  test at its gate with the identification
  intact — a priced-in outcome, worded in
  §5.4.
- **The measures are coarse.** Three shares
  and an entropy, on a short-text corpus,
  can split (MIXED) without either side
  being wrong. MIXED is pre-written so it
  cannot be softened into a near-pass after
  the fact.

## 11. Stop conditions and outcome classes

Execution ends in exactly one of:

- **NUMERAL-LIKE**, **NOT NUMERAL-LIKE**, or
  **MIXED** — per §5.3, after all gates pass
  and step 1 succeeds.
- **IDENTIFIED — TOO FEW OCCURRENCES TO
  TEST** — gate 0.4: the identified sign is
  absent from the pinned layer, or below
  the occurrence floor.
- **IDENTIFICATION FAILED** — step 1 cannot
  name the source's list from the document
  (list unnamed), or cannot match the drawn
  sign (sign unmatched).
- **CLOSED AT STEP 0** — SOURCE NOT
  PRODUCIBLE, INPUT PIN MISMATCH (input
  named), or CORPUS NOT PINNABLE.

The §6 recovery record is produced in every
class.

## 12. Execution shape (gated; NOT run by this draft)

1. **Graph-first build** (H15/H23) — script,
   graph node, registration, verification.
2. **Step 0** (§3) — input integrity; source
   producible; recovery-before-verdict
   ordering asserted.
3. **Step 1** (§4) — the recovery: list named
   from the document; drawn sign matched by
   form; `source-table-recovery.json`
   written. A failure closes the run as
   IDENTIFICATION FAILED with the
   closure-form record.
4. **Step 2 gate** (§3, gate 0.4) — corpus
   identified and pinned; occurrence census;
   pre-counting record fixing both reference
   sets.
5. **Step 2** (§5) — the three measures for
   target, numeral set, and controls;
   outcome by the §5.3 mapping alone.
6. **Outcome** (§8) — appended records only;
   anchors asserted byte-identical;
   foundation check reported as measured.
   In campaign order this lands in Wave 3
   group 2.

## 13. What this spec is not

Not a decipherment, not a test of the value
six, not design D-16 or any part of it (the
rival sign-700 fragments wait for their own
planning gate under E-7, whatever this
spec's recovery finds), not a re-extraction
of the source's argument as evidence, and
not an authorisation to execute. It is a
two-stage fragment test — identify the sign,
then test it as a numeral — designed so that
its honest outcomes, including failing
closed at identification, are written down
before the source is opened for recovery.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
