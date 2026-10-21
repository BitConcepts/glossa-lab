# Spec 055 — Adjudication Record

> ## ADJUDICATION INPUT — 2026-10-21; FREEZE ACT — 2026-10-21 (§§7–8)
>
> This spec has three adjudication inputs,
> recorded here so the draft's basis is
> inspectable:
>
> 1. **The runnable-experiments campaign
>    plan, approved by the owner AS WRITTEN
>    on 2026-10-21**
>    (`~/workspace/your_files/2026-10-21-runnable-experiments-campaign-plan.md`,
>    Parts 1–4). D-15 is campaign member 11
>    (Part 2), with the falsifier stated
>    there in one line: the source document
>    does not identify the sign
>    (IDENTIFICATION FAILED is a
>    pre-registered outcome), or the
>    identified sign's behaviour contradicts
>    the numeral reading. Part 3 records the
>    chain that does not create a member:
>    D-15's step 1 (source-table recovery)
>    is the act that would unblock D-16; it
>    produces a preserved recovery record,
>    and under decision E-7 that is where
>    the chain stops inside this pass.
>    Part 4 places the fragment recoveries
>    (D-15, D-17, D-19) among the
>    independent members drafted in
>    parallel throughout Wave 1, and D-15's
>    execution in Wave 3 group 2, the
>    independent executions. Decision E-1
>    settles that every specification in the
>    pass files its own OSF contract
>    registration at its freeze.
> 2. **The portfolio triage of 2026-10-21**
>    (`~/workspace/research_notes/design-portfolio-triage-2026-10-21.md`):
>    design D-15 found **RIPE** — its first
>    half is identification desk work on
>    the source document the extraction
>    came from, it fails closed honestly,
>    and only if the sign is identified
>    does the numeral-behaviour test arise,
>    on in-hand corpora. The triage's block
>    note for D-16 is recorded there in
>    terms: D-16 is BLOCKED, and what
>    unblocks it is "D-15 step 1's table
>    recovery, extended to the sign-700
>    table" — the chain this spec's §4.3
>    and claim F055-C09 govern.
> 3. **Design D-15 itself** (PR #195 packet,
>    `03-fragments.md`, §D-15), which
>    governs the substance of this draft.
>
> These inputs commission this **draft**.
> They are not a freeze order and not an
> execution order for Spec 055: both remain
> separate later acts under the campaign.
> Under the campaign's E-1, OSF registration
> at freeze is settled policy, not an open
> proposal — see §3.

## 1. The adopted basis (operative substance)

- **The design.** D-15 in the PR #195
  experiment-design packet
  (`docs/research/experiment-designs-2026-10-13/03-fragments.md`,
  §D-15): step 1 identification — re-open
  the source document the extraction came
  from and recover the full table the cell
  was pulled from: which published sign
  list numbers its signs (the table's own
  heading, introduction, or citations will
  say), and the drawn sign its number 900
  labels; success is the list named from
  the document's own text and the sign
  matched to a crosswalk-registry entry or
  to a drawn sign in a published list;
  failure closes as IDENTIFICATION FAILED.
  Step 2, only if step 1 succeeds, the
  numeral test: the identified sign against
  (a) the known numeral signs and (b) a
  frequency-matched ordinary-sign control
  set, on three measures fixed in advance
  (share of occurrences in inscriptions of
  length three or less; share of
  occurrences adjacent to another
  numeral-class sign; positional entropy),
  with criteria NUMERAL-LIKE (inside the
  known numerals' range on at least two of
  the three measures and outside the
  control set's median on the same
  measures), NOT NUMERAL-LIKE (inside the
  control range on at least two), MIXED
  otherwise. Data: the strict corpus; the
  known-numeral set fixed from published
  identifications before counting.
- **The claim.**
  `ancient_writing_and_modern_technologies_51831ac9_sign_val_0001`:
  UNTESTED fragment, "Sign value: 900 /
  number six", stopped at Phase-104 under
  RULE-NUM (RULE-NOCOND also recorded for
  the fragment family in the packet: no
  falsification condition, no stated
  proposition beyond the cell).
- **The source.** Andreas Fuls, "Ancient
  Writing and Modern Technologies –
  Structural Analysis of Numerical Indus
  Inscriptions" (Technische Universität
  Berlin), held as cleaned text in the
  repository, with its literature record
  (original PDF; DOI as detected there,
  10.13109/hisp.2015.128.1.42; license
  status "unclear"). Unlike Spec 046's
  source, this source *argues* for the
  value its fragment carries — a fact that
  shapes §7's control: the argument is
  preserved by the recovery and is evidence
  at no stage of this spec's test.
- **The chain.** D-15 step 1's recovery is
  the act that would unblock D-16 (triage
  block note; campaign Part 3). Campaign
  decision E-7: D-16 stays out of this
  campaign even if D-15 unblocks it; it
  enters only through a future planning
  gate. This spec therefore (a) specifies
  the recovery as a preserved record —
  spec §6 fixes its form, and its output
  is a record of this spec — and (b)
  states the E-7 rule explicitly (spec
  header, §4.3, §8 item 5, §9 limit 5,
  claim F055-C09). No part of D-16 is
  designed here.

## 2. Verification record at draft

Verified first-hand at drafting, 2026-10-21:

- **Design D-15** — read in full in the
  packet file: the claim, RUNNABLE-TODAY
  feasibility, step 1 (identification with
  its precise success and failure
  conditions), step 2 (hypothesis, the
  design's falsifier in its own words, the
  three measures, the criteria, the strict
  corpus and the before-counting rule for
  the known-numeral set), what it would
  move, and what it would NOT establish
  (the value six specifically). D-16's
  design was read alongside for the chain
  boundary only — to state what this spec
  must not design — not as drafting
  material.
- **The claim record** — read on `main`
  (SHA-256 `e9819089…`): the fragment's
  verbatim wording, its UNTESTED status and
  `created` stage, and its adopted
  not-understood text (which sign, in which
  published sign list, this number refers
  to; the record would become checkable
  once the source table is re-extracted
  with its sign list named and the sign
  image attached).
- **The source document** — the held
  cleaned text (SHA-256 `1275b795…`) read
  at the relevant sections: the opening
  statement (printed p. 57) that the signs
  "are coded according to an extended sign
  list with 702 distinct signs (Wells
  2015)"; the SIGN LIST section (p. 59),
  "the sign list by Wells (2011, 2015) has
  been extended to currently 702 distinct
  signs"; the SPECIAL NUMERICAL SIGNS
  sections on signs 415, 900, and 70
  (pp. 67–69), including the "Sign 900"
  section's reasoning and its Figures 11
  and 12 captions; the SIGN 700 WITH
  NUMBERS section (p. 70) — located for
  the recovery record's locator block, its
  content not adjudicated; NUMERICAL
  VALUES OF SIGNS, including "Numerical
  value of Sign 900" and its Table 1
  (pp. 71–74); and the SUMMARY statement
  (p. 85), "The numerical value of Sign 900
  is six as verified in Figures 16, 18, and
  21." The held text carries figure
  captions only, not the drawn figures —
  spec §2 records the consequence for
  step 1's matching.
- **Phase-104** — this claim's entry read
  in the pinned evaluation file (SHA-256
  `2d0b83e8…`): stays_untested, RULE-NUM,
  evidence "Crosswalk numeric IDs present
  in registry: 86".
- **The crosswalk registry** — read on
  `main` (SHA-256 `8a0b2a82…`, 803 rows as
  held today). One cell grounds claim
  F055-C07 and spec §4.2: a `W900` value
  sits inside a `wells_ids` cell on the
  P154 row, whose description is "Right
  parenthesis (perhaps with a backward
  curve at the bottom)", corpus frequency
  93. The draft records the cell's
  existence and neither adopts it as the
  identification nor treats its description
  as a refutation: which drawn sign the
  source's 900 is, is step 1's drawn-form
  question.
- **The strict-corpus posture** — Spec
  048's draft (PR #248, read at this draft)
  records for the same layer that Spec 033
  states it as a database posture, not a
  pinnable repository file. Spec §2 and
  gate 0.4 follow that precedent exactly
  (DD-055-5) rather than inventing a pin.
- **Input pins** — recomputed at this draft
  from `main` at commit `83b6a563` (re-read
  at the start of this drafting act) and
  stated in spec §2: claim record
  `e9819089…`, held cleaned text
  `1275b795…`, literature record
  `92e19e6d…`, Phase-104 evaluation
  `2d0b83e8…`, registry `8a0b2a82…`, lane-2
  drafts `3f645c9a…`, anchors `df0cf620…`.
- **Branch base** — this draft branches
  from `main` at `83b6a563` (the PR #241
  merge). No specs 041–054 directories
  exist on `main`; the campaign's earlier
  drafts stand at their own PRs (Spec 042
  at PR #240, Spec 043 at PR #242, Specs
  044–050 at PRs #243–#248 as of this
  draft).
- **Not done at draft, by design** — the
  recovery was not performed (the §1
  readings above are the draft's
  verification of its basis, not an
  identification: no naming statement was
  entered into a recovery record, no
  drawn-form match was attempted, no
  registry row was adopted), the step-0
  gates were not run, the corpus layer was
  not exported or pinned, no sign was
  counted, no code was written or run, the
  AEE hooks have not run, and nothing was
  filed with OSF.

## 3. What the freeze decision is asked to decide

1. Freeze this contract as drafted (digest
   in `freeze.md` / `freeze.json`), with
   every §2 pin re-asserted against the
   merged record — or decline, leaving the
   fragment with its Phase-104 record: an
   untested pointer at a section in a
   paper, and the recovery unmade.
2. **OSF registration (settled, not open).**
   Campaign decision E-1 (approved
   2026-10-21) settles that every
   specification in the pass files its own
   OSF contract registration at its freeze.
   The freeze of Spec 055 therefore files
   one, following the Specs 036–039
   pattern. Nothing is filed at draft.
3. **OPEN-1 — The recovery-record form.**
   DD-055-1 fixes `source-table-recovery.json`
   and its field set. The freeze confirms
   the form, or amends it openly — before
   execution, since D-16's future gate and
   the campaign's record both rely on the
   form being fixed in advance.
4. **OPEN-2 — The control-set rule and the
   median clause.** DD-055-6 fixes the
   nearest-10 frequency-matching rule and
   the directional reading of "outside the
   control set's median". The freeze
   confirms both, or substitutes others
   openly; either way the mapping of
   §5.3 must stay total.
5. **OPEN-3 — The occurrence floor.**
   DD-055-4 sets the step-2 gate floor at
   5 occurrences. The design names no
   floor. The freeze confirms the value,
   sets another, or removes the floor
   openly (in which case MIXED absorbs the
   thin cases, and the §5.4 wording set
   loses a member by the freeze's own
   recorded act).
6. **OPEN-4 — The corpus-pinning
   procedure.** The exact act by which the
   strict-corpus layer is identified,
   exported, and pinned at gate 0.4 —
   following the precedent Spec 048's
   freeze will set for the same layer, if
   that freeze lands first — is fixed at
   this freeze and recorded.
7. **OPEN-5 — Hedged numeral-set
   members.** Whether published numeral
   candidates whose sources hedge the
   identification (the source document
   itself hedges sign 70: "may also be
   regarded as a numerical sign… a
   non-numerical interpretation… is
   possible as well") enter the
   known-numeral reference set, and under
   what recording.
8. **OPEN-6 — Positional entropy.**
   DD-055-6's construction (Shannon entropy
   in bits over positions as stored,
   identical for every sign compared). The
   freeze confirms it or substitutes a
   normalised construction openly, before
   any counting.
9. **OPEN-7 — Synthetic / dry-run check.**
   Whether execution requires a worked
   dry-run of the §5 measures and mapping
   on a sign other than the target (to
   prove the machinery before it touches
   the identified sign). This draft takes
   no position; the freeze decides and
   records it.

## 4. Draft-fixed readings (stand unless the freeze overturns them openly)

Each is labelled **DECIDED-BY-DRAFT**:

- **DD-055-1 — The recovery-record form is
  this draft's decision.** Spec §6 fixes
  the recovery output exactly: file
  (`source-table-recovery.json`), top-level
  fields, the naming-statements array with
  verbatim quotes and locators, the
  recovered-material sections, the
  target-sign block, the sign-700 locator
  block, the closure form (the file is
  produced on every terminal outcome), and
  the locator string form.
- **DD-055-2 — Identification is an
  execution act, not a draft finding.**
  This draft read the document's naming
  statements and records the reading it
  expects step 1 to confirm (the extended
  Wells 2011/2015 list). The identification
  verdict rests on the execution's recovery
  record alone (claim F055-C06): a draft's
  reading has no standing at execution, and
  a run that inherited it without the
  recovery act would produce no preserved
  record — the very output the chain rule
  exists to preserve.
- **DD-055-3 — The target is excluded from
  its own reference sets.** The target is
  not a member of the known-numeral set,
  and target-to-target adjacency does not
  count as numeral adjacency (claims
  F055-C11). The design fixes the numeral
  set "from published identifications" and
  the target's identification *is*
  published — in the claim's own source —
  so a naive reading stocks the set with
  the sign under test (see §5, X-3).
- **DD-055-4 — An occurrence floor gates
  step 2.** An identified sign absent from
  the pinned layer, or below 5
  occurrences, closes as IDENTIFIED — TOO
  FEW OCCURRENCES TO TEST with the count
  named (spec §3 gate 0.4, §5.4). The
  design names no floor; without one,
  shares computed on one or two occurrences
  would be forced into the §5.3 mapping as
  if they were measurements. Flagged
  OPEN-3.
- **DD-055-5 — No corpus pin at draft.**
  The strict corpus is a database posture,
  per the Spec 048 precedent read at this
  draft; the layer is identified, exported,
  and pinned at gate 0.4, and the run
  closes if it cannot be. No pin is
  invented at draft.
- **DD-055-6 — Two of the design's phrases
  are given operational forms.**
  "Frequency-matched" becomes the
  nearest-10 rule of spec §5.1 (ties by
  corpus identifier, ascending).
  "Outside the control set's median"
  becomes the directional clause of spec
  §5.3 (the target's value lies on the
  known-numeral median's side of the
  control median, and differs from it).
  Positional entropy is Shannon entropy in
  bits over positions as stored. All three
  are flagged OPEN-2 / OPEN-6.
- **DD-055-7 — No execution phase number
  at draft.** Allocated at the freeze act,
  from the merged record as it then
  stands.
- **DD-055-8 — Evidence carries
  `observed_at` from the draft.** The cited
  facts were verified first-hand today; the
  completion Spec 038's freeze had to
  retrofit is done here at the act that
  actually observed the records.

## 5. Double derivation of the acceptance tests (doctrine record)

Per the autonomous-execution doctrine, each
claim's acceptance test was derived twice,
independently, from the requirement alone,
before the register was written:

- **Derivation A** worked from the
  requirement text forward: for each
  claim, what observable record, produced
  by the run itself, would show the
  requirement held?
- **Derivation B** worked from the
  falsifier and the pre-written outcome
  wordings backward: for each claim, what
  would a hostile reader check in the
  outcome record to show the requirement
  had *not* held?

The two derivations agreed on the gate and
inspection tests for F055-C02, C05, C08,
C10, C12, C13, C14, and C15 without
amendment: in each case A's "record
produced in order" and B's "absence or
disorder of that record falsifies" are the
same check read from the two directions,
and the register states it once.

Disagreements, and their resolutions:

- **X-1 — Is the sign already identified by
  the registry?** A, reading Phase-104
  against today's registry, noted the
  registry now contains a `W900` cell where
  Phase-104 located no matching entry, and
  proposed the identification could be
  discharged by that cell. B held that a
  registry cell is a string in a
  multi-value column on a Parpola-keyed
  row: the cell's own row describes a
  different drawn form ("Right
  parenthesis…"), the fragment's list is
  an *extended* Wells list whose numbering
  need not coincide with the registry's
  Wells column, and the design's success
  condition is a drawn-sign match, not a
  string hit. **Resolution:** B governs.
  The cell is named in spec §1 and §4.2 as
  a trap in both directions; matching is
  by drawn form only (DD-055-2-adjacent;
  claim F055-C07).
- **X-2 — Has step 1 already happened at
  draft?** A proposed that this draft's
  first-hand reading of the naming
  statements (extended Wells 2011/2015,
  702 signs) *is* the identification, and
  execution could proceed to counting. B
  held that the campaign's chain rule
  makes the recovery an act whose *output
  is a preserved record*: a drafting
  reading produces no such record, names
  no drawn sign, and would leave D-16's
  future gate with nothing preserved to
  stand on. **Resolution:** B governs
  (DD-055-2). The draft states its expected
  reading openly, as Spec 046's draft does
  for its source, and assigns it no
  standing.
- **X-3 — Does the target belong in the
  numeral set?** A, reading the design's
  "known-numeral set fixed from published
  identifications", included sign 900: its
  source publishes it as a special
  numerical sign. B noted the consequence:
  the target would help define the range it
  must sit inside and the adjacency counts
  it must score, and with repetitions of
  the sign counting as numeral adjacency
  the adjacency measure would be
  near-tautological for a sign whose source
  itself cites its repetitions as the
  numeral evidence. **Resolution:** B
  governs (DD-055-3; claim F055-C11).
- **X-4 — What does "outside the control
  set's median" mean?** A could not state a
  check: a median is a point, and a value
  is trivially "outside" a point unless it
  equals it, which would make the clause
  fire on almost every measure and carry
  almost no information. B proposed the
  directional reading — the clause does
  discriminating work only if it requires
  the target to depart the control median
  *toward* the numeral side. **Resolution:**
  B's reading is adopted as the operational
  form (DD-055-6), the design's wording is
  carried in spec §5.3 beside it, and the
  gap is recorded as defect D-1 and
  flagged OPEN-2.
- **X-5 — How much of the document does
  the recovery recover?** A scoped the
  recovery to the sign-900 material alone.
  B, working from the chain rule, held
  that a recovery which walks past the
  sign-700 statements in the same
  discussion without even locating them
  preserves less than the act D-16 waits
  on — while a recovery that *adjudicates*
  them designs D-16 inside D-15's spec,
  against E-7. **Resolution:** the middle
  course is the draft's: the sign-700
  statements are located in the recovery
  record (locators only, no finding, no
  design), and the E-7 boundary is stated
  in every product (DD-055-1; claim
  F055-C09).
- **X-6 — Prose recovery or
  machine-readable record?** A proposed the
  outcome record's prose as the preserved
  recovery. B held that prose forces any
  later consumer — D-16's gate first among
  them — to re-interpret the recovery, an
  unrecorded second recovery at exactly the
  hand-off the campaign wants pinned.
  **Resolution:** the JSON file in spec §6
  is the deliverable of record; the prose
  rendering is required to match it
  (DD-055-1; claim F055-C08).

## 6. Defects found at drafting

- **D-1 — The design's NUMERAL-LIKE
  criterion is not self-operationalising.**
  "Outside the control set's median on the
  same measures" names a point, not a
  range, and "frequency-matched" names no
  matching rule. Left unfixed, execution
  would have to invent both at counting
  time — after the target's behaviour was
  visible. Repaired at draft by DD-055-6,
  flagged OPEN-2; the design itself is not
  edited.
- **D-2 — The design says "table"; this
  source carries the material in headed
  sections.** D-15 step 1 speaks of
  recovering "the full table the cell was
  pulled from". In the held source, the
  sign-900 value stands in headed prose
  sections ("Sign 900"; "Numerical value of
  Sign 900", with its Table 1 of possible
  solutions) and a summary sentence — there
  is no single sign-value table in the held
  text for the cell to have been pulled
  from. The draft therefore defines the
  recovery over the headed sections, the
  one table the value's derivation actually
  uses, and the summary statement (spec
  §4.3, §6). If the original PDF carries a
  tabular sign list the cleaned text lost,
  gate 0.2's verbatim-location check is
  where that surfaces, and the recovery
  record is where it would be recorded.
- **D-3 — The design's outcome set has no
  word for an identified sign the corpus
  cannot test.** Step 2 presumes the
  identified sign is in the strict corpus
  with countable occurrences. The source's
  corpus is the ICIT lineage and the
  design's data is the strict corpus of a
  different lineage, reached through one
  crosswalk row; absence or near-absence
  is a realistic pattern the three
  behaviour words cannot honestly cover.
  Repaired at draft by DD-055-4's gate and
  the IDENTIFIED — TOO FEW OCCURRENCES TO
  TEST wording, flagged OPEN-3.
- **D-4 — Phase-104's "no matching entry"
  is no longer true as a string statement,
  and nothing on the record says so.** The
  registry's growth (86 numeric IDs at
  Phase-104; 803 rows today, a `W900` cell
  among them) silently changed what a
  naive re-check would conclude. The draft
  records the change and the trap (spec
  §1, §4.2; §5, X-1) rather than leaving
  the next reader to discover it by
  falling into it. The Phase-104 record
  itself is not edited; it stands as a
  true statement of the registry as it
  then was.
- **D-5 — The source's drawn signs are not
  in the held text.** Step 1's drawn-form
  match works from the named published
  list and the registry, with the PDF's
  figures available only if the held PDF
  can be produced at execution. The draft
  states this in spec §2 rather than
  letting the match quietly become a
  caption-matching exercise.

No defect was found that prevents stating
the falsifier, the step-0 gates, or the
pre-written wordings for the full outcome
set; the draft therefore advances as a
draft. Nothing in this section amends
design D-15, which stands as written in
the packet.

## 7. Freeze decisions (2026-10-21)

The freeze was executed on 2026-10-21 under
the campaign plan approved AS WRITTEN the
same date (Wave 2 freeze wave). The OPEN
items of §3 are resolved here, on the
record. Draft decisions DD-055-1 to
DD-055-8 are **confirmed** as drafted,
including DD-055-3 (target excluded from
its own reference sets), DD-055-4 (the
occurrence floor), and DD-055-6 (the
operational forms).

- **DD-055-9 — OSF registration (E-1).**
  This freeze files the spec's own OSF
  contract registration under campaign
  decision E-1, following the Specs
  036–039 pattern (OPEN item §3.2, settled
  at draft). The filing record is
  `osf-spec-registration.md`, completed by
  append after filing. Execution awaits the
  registration's approval act and a
  separate execution order.
- **DD-055-10 — OPEN-1, the recovery-record
  form: CONFIRMED.** The preserved record is
  `source-table-recovery.json` under schema
  `glossa.source-table-recovery/1`, in the
  field set spec §6 fixes (DD-055-1),
  produced on **every terminal outcome**
  including step-0 and identification
  closures, carrying its closure block and
  whatever recovery material was established
  before the closure. The freeze does not
  adjudicate sign 700 in confirming this
  form: the record's `sign_700_material`
  block carries locators and a presence
  flag only (DD-055-9's chain boundary;
  claim F055-C09).
- **DD-055-11 — OPEN-2, the control-set
  rule and the median clause: CONFIRMED as
  drafted.** The control set is the 10
  ordinary signs whose occurrence counts in
  the pinned layer are closest to the
  target's count, ties by corpus identifier
  ascending, all of them if fewer than 10
  exist (DD-055-6). "Outside the control
  set's median" keeps its directional
  operational form: the target's value lies
  on the known-numeral median's side of the
  control median and differs from it. The
  §5.3 mapping stays total under both.
- **DD-055-12 — OPEN-3, the occurrence
  floor: CONFIRMED at 5.** An identified
  sign absent from the pinned layer, or
  represented by fewer than 5 occurrences,
  closes as IDENTIFIED — TOO FEW
  OCCURRENCES TO TEST with the count named
  (gate 0.4). The floor is not removed; the
  §5.4 wording set keeps all six members.
- **DD-055-13 — OPEN-4, the corpus-pinning
  procedure: the draft posture is
  CONFIRMED, and no pin is stated at this
  freeze.** The strict corpus is the
  program's V3 / Mahadevan-lineage corpus
  as held in the database — a database
  posture, not a pinnable repository file
  on `main` (the Spec 048 precedent for the
  same layer, read at draft and re-checked
  at this freeze). The exact act is gate
  0.4's, unchanged: before any counting,
  the layer of record is identified from
  the database, exported in full, and
  pinned by SHA-256 in the step-0 record,
  which states the export's file form and
  sort order as produced; the identified
  sign's representation is established by
  its crosswalked corpus identifier; if the
  layer cannot be pinned the run closes as
  CLOSED AT STEP 0 — CORPUS NOT PINNABLE.
  Reason for not pinning now: there is no
  file on `main` whose hash is the layer,
  so a freeze-time pin would name a
  different object than the one execution
  counts — the stale-pin failure Spec 040's
  gate record documents.
- **DD-055-14 — OPEN-5, hedged numeral-set
  members: hedged members do NOT enter the
  set.** A numeral candidate whose published
  identification is hedged in its source is
  recorded as hedged in the pre-counting
  record and is excluded from every range,
  median, and adjacency computation; hedged
  candidates are listed separately there.
  A hedged identification must not stock
  the reference range the target is judged
  against.
- **DD-055-15 — OPEN-6, positional entropy:
  CONFIRMED as drafted.** Shannon entropy
  in bits over positions as stored in the
  corpus sequence, computed by the
  identical formula for every sign compared
  (DD-055-6). No normalised construction is
  substituted.
- **DD-055-16 — OPEN-7, dry-run check:
  REQUIRED.** Execution requires a worked
  dry-run of the §5 measures and the §5.3
  mapping on a sign other than the target,
  recorded in the pre-counting record,
  proving the machinery before it touches
  the identified sign. The dry-run produces
  no target quantity and changes no rule.
- **DD-055-17 — Execution phase allocated:
  Phase-414** (DD-055-7's allocation act).
- **DD-055-18 — The AEE gate reading.**
  The DD-038-10 reading is adopted: the
  lifecycle hooks pass at the freeze when
  every hook carries zero correctness
  failure modes and no claim below the
  0.70 threshold, the residual records
  being the FR-2.3 draft-cap records a
  draft register carries by construction.
  Outcome at this freeze: PASS — register
  recovered to 0.7-draft in adjudicated
  rounds (loadability recovery from
  0.5-draft; 53 failure modes over
  0.6-draft: 14 irreducibility, 22
  independence-unmodelled, 2
  negation-conflict, 15 draft-cap; a
  further restatement of F055-C13's head
  cleared the last two correctness records);
  at every hook, draft-cap records only,
  minimum propagated 0.72. Record:
  `aee/freeze-aee-note.md`.

**The chain rule, carried verbatim in
substance (E-7).** The recovery this spec
performs is the act that would unblock
design D-16. It does not: **the recovery
output does NOT admit D-16 to this
campaign, in whole or in part, even if the
recovery fully succeeds.** The sign-700
statements in the recovered document are
located by locator only and are adjudicated
in no way by this freeze or by the spec;
sign 700 was not adjudicated at the freeze.
D-16 waits for its own planning gate.

**The registry trap, carried (F055-C07).**
The crosswalk registry as held today (803
rows) contains a `W900` cell inside the
`wells_ids` cell of the P154 row. That cell
neither identifies nor excludes this
fragment's sign; matching is by drawn form
only. The freeze confirms the trap is
carried in spec §§1, 4.2 and claim
F055-C07 exactly as drafted.

## 8. Pin verification at the freeze (two routes)

Every spec §2 pin was re-derived in the
foreground by two independent routes — the
contents-API raw route and the git-blob
route — both at the merged record (`main`
at `3af269f660a9368e898cdece41132200d31b87cc`).
The two routes agree byte-for-byte on every
file, and every recomputed hash equals its
pin:

| Input | SHA-256 (both routes) | Bytes |
|---|---|---|
| Claim record (`glossa-indus/claims/extracted_claims/ancient_writing_and_modern_technologies_51831ac9.json`) | `e98190894202a2a1c0e314229dcb585c62a0f5c12c059bcabd63b055c42959e8` | 22,894 |
| Held cleaned text (`glossa-indus/processed/cleaned_text/ancient_writing_and_modern_technologies_51831ac9.txt`) | `1275b795903260221f5226bada352de27471c010e2ad8ace556c548c20da1fc4` | 48,904 |
| Literature record (`glossa-indus/literature/documents/ancient_writing_and_modern_technologies_51831ac9.json`) | `92e19e6def7eccb42ba0e9f53f5ef3bf9dbb0b9717aa3d675cecb971f5ab0e5c` | 1,261 |
| Phase-104 evaluation (`glossa-indus/reports/phase104_claims_evaluation.json`) | `2d0b83e8055a04b96635007054cfadde472f605dc7e5b249a61c8f9ea89b858d` | 17,475 |
| Crosswalk registry (`data/crosswalks/canonical_sign_registry.csv`) | `8a0b2a82ac8d226d574ce01f5550c581efd91a97cab86201a62f7a7e435bd420` | 111,583 |
| Lane-2 drafts (`specs/029-tao-claim-lifecycle/lane2-drafts/drafts.json`) | `3f645c9a4132ba5a0bc5fca4ca22810b8b6169a2f1f9f85f35990c7b72df33fb` | 127,338 |
| Anchors (`backend/reports/INDUS_FINAL_ANCHORS.json`) | `df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569` | 570,344 |

The strict corpus carries no pin in this
table, deliberately (DD-055-13). The claim
record's hash is carried in the freeze
definition as a constant in the Spec 038
form: the extracted-claims store is
regenerated by the backend suite, so the
freeze tests assert the constant plus the
fragment's facts on the live file, never a
live-file hash on that store. The same form
is applied to any other suite-regenerated
file the freeze tests touch: the Phase-104
evaluation and the lane-2 drafts are not
regenerated and carry live-file hashes in
the tests; the registry, the held text, the
literature record, and the anchors are not
regenerated either.

The facts the design rests on were re-read
from the pinned bytes in the same pass: the
claim entry reads "Sign value: 900 / number
six", status untested, stage created; the
Phase-104 entry reads stays_untested under
RULE-NUM with evidence "Crosswalk numeric
IDs present in registry: 86"; the registry
carries 803 rows, and the `W900` cell sits
on the P154 row ("Right parenthesis
(perhaps with a backward curve at the
bottom)", corpus frequency 93); the
literature record carries file size
3,565,316 bytes, intake checksum
`51831ac9…`, license status "unclear"; the
held text carries the "702 distinct signs"
naming statements, the "Sign 900" section,
the "Numerical value of Sign 900" section,
and the summary statement that the
numerical value of Sign 900 is six.
`backend/tests/test_spec055_freeze.py` pins
these facts so later drift fails loudly.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
