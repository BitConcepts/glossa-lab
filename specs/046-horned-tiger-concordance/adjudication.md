# Spec 046 — Adjudication Record

> ## ADJUDICATION INPUT — 2026-10-21
>
> This spec has two adjudication inputs,
> recorded here so the draft's basis is
> inspectable:
>
> 1. **The runnable-experiments campaign
>    plan, approved by the owner AS WRITTEN
>    on 2026-10-21**
>    (`~/workspace/your_files/2026-10-21-runnable-experiments-campaign-plan.md`,
>    Parts 1–4). D-18 is campaign member 13
>    (Part 2), with the falsifier stated
>    there in one line: the published sign
>    lists (CISI, Parpola, Mahadevan, Wells)
>    do not concur on the identification.
>    Part 4's drafting order places D-18
>    alongside D-05, "since its resolutions
>    feed Asset A and its draft fixes what it
>    will deliver, in what form." Part 4's
>    execution order (Wave 3, group 1) places
>    D-18's execution before Asset A freezes.
>    Decision E-6 places Asset A inside
>    D-05's specification (Spec 045);
>    decision E-1 settles that every
>    specification in the pass files its own
>    OSF contract registration at its freeze.
> 2. **The portfolio triage of 2026-10-21**
>    (`~/workspace/research_notes/design-portfolio-triage-2026-10-21.md`):
>    design D-18 found **RIPE** —
>    identification plus a concordance test
>    across the published sign lists the
>    program holds or can cite (CISI,
>    Parpola, Mahadevan, Wells), all
>    available; each resolution also feeds
>    the shared classification behind
>    D-05/D-06/D-13, without drawing on it.
>
> These inputs commission this **draft**.
> They are not a freeze order and not an
> execution order for Spec 046: both remain
> separate later acts under the campaign.
> UNDER the campaign's E-1, OSF registration
> at freeze is settled policy, not an open
> proposal — see §3.

## 1. The adopted basis (operative substance)

- **The design.** D-18 in the PR #195
  experiment-design packet
  (`docs/research/experiment-designs-2026-10-13/03-fragments.md`,
  §D-18): step 1 identification as D-15
  step 1 (recover the source's sign list
  from the document, match its sign 297 to a
  drawn sign, fix the identity in the
  crosswalk registry with the citation
  attached; if the list cannot be named,
  close as IDENTIFICATION FAILED); step 2 a
  concordance against every published sign
  list the program holds or can lawfully
  cite (CISI, Parpola, Mahadevan, Wells),
  each scored AGREE / DISAGREE / SILENT, with
  the outcomes CONSENSUS (at least two
  independent lists agree, none disagrees),
  SINGLE-SOURCE (only the original source
  identifies it so), CONTESTED (any held
  list disagrees, the disagreeing
  identification quoted).
- **The claim.**
  `the_archaeology_and_epigraphy_of_indus_w_27f45a68_sign_val_0002`:
  UNTESTED fragment, "Sign value: 297 / the
  horned tiger, or perhaps just 'tiger'
  generically", stopped at Phase-104 under
  RULE-NUM.
- **The source.** Bryan K. Wells, *The
  Archaeology and Epigraphy of Indus
  Writing* (Archaeopress, 2015), held as
  cleaned text in the repository. The
  passage stands at printed p. 97. This
  fact — that the source author is one of
  the four concordance authors — is not
  addressed in the design; this draft fixes
  its consequence (DD-046-2).
- **The feed.** Asset A, the depicted-kind
  classification built inside Spec 045
  (D-05) from held published sources only —
  per design D-05, sign-by-sign depicted-kind
  labels (animal, sky/cycle, object/goods,
  human, other), each label carrying its
  source, entered blind to positional
  results and frozen before any join. D-18's
  concordance output is an input to that
  build (campaign Part 3), gathered without
  drawing on it.

## 2. Verification record at draft

Verified first-hand at drafting, 2026-10-21:

- **Design D-18** — read in full in the
  packet file: the claim, RUNNABLE-TODAY
  feasibility, step 1 (identification as
  D-15 step 1; IDENTIFICATION FAILED if the
  list cannot be named), step 2 (the four
  named lists; AGREE / DISAGREE / SILENT
  scoring; the three outcome words with
  their criteria), the feeds-the-asset note
  with its no-circularity sentence, and the
  limit (identification layer only). D-15's
  step 1 and D-05's data statement were read
  in full alongside.
- **The claim record** — read on `main`
  (SHA-256 `bd0f7abd…`): the fragment's
  verbatim wording, its UNTESTED status and
  `created` stage, and its adopted
  not-understood text (which drawn sign, and
  agreed vs one scholar's call, both
  unknown; animal identifications are raw
  material for the shared classification).
- **The source book** — the held cleaned
  text (SHA-256 `62acf855…`) names the book,
  its author (Bryan K. Wells), publisher and
  year (Archaeopress, 2015; ISBN
  978 1 78491 046 4) on its title pages; the
  passage at printed p. 97 was read
  verbatim: sign 532 is proposed as a
  logograph for the anthropomorphic figure
  and sign 297 "represents the horned tiger,
  or perhaps just 'tiger' generically". The
  passage names no sign list at the passage
  itself — which is what step 1's apparatus
  check exists to settle.
- **Phase-104** — this claim's entry read in
  the pinned evaluation file (SHA-256
  `2d0b83e8…`): stays_untested, RULE-NUM,
  evidence "Crosswalk numeric IDs present in
  registry: 86".
- **The crosswalk registry** — read on
  `main` (SHA-256 `8a0b2a82…`, 803 rows as
  held today; the registry has grown since
  Phase-104's record, and the draft pins
  today's file rather than inheriting either
  count). Two cells ground claim F046-C07:
  Parpola P297 is described in the registry
  as "Ladder motif", and the value W297
  appears inside a multi-value `wells_ids`
  cell on the P205 row. Neither identifies
  the passage's sign; both are named in
  spec §4 so execution cannot fall into
  them silently.
- **Input pins** — recomputed at this draft
  from `main` at commit `82b29490` and
  stated in spec §2 (claim record, held
  cleaned text, Phase-104 evaluation,
  registry, lane-2 drafts file).
- **Branch base** — the §2 pins were
  recomputed from `main` at `82b29490`,
  re-read at the start of the drafting act.
  Before the branch was cut, `main` advanced
  to `83b6a563` (the PR #241 merge: a Spec
  030 record touching none of this spec's §2
  inputs, all of which re-assert unchanged);
  this draft branches from `83b6a563`. No specs
  041–045 directories exist on `main`; Spec
  042's draft stands at PR #240 and Spec
  043's at PR #242. Spec 045 (D-05) is being
  drafted in parallel and was **not**
  available to read at this draft — see
  defect D-4 in §6 and OPEN-6 in §3.
- **Not done at draft, by design** — no list
  was opened for scoring, no drawn-sign
  match was attempted, the step-0 gates were
  not run, no concordance row exists, no
  code was written or run, the AEE hooks
  have not run, and nothing was filed with
  OSF.

## 3. What the freeze decision is asked to decide

1. Freeze this contract as drafted (digest
   in `freeze.md` / `freeze.json`), with
   every §2 pin re-asserted against the
   merged record — or decline, leaving the
   fragment with its Phase-104 record: an
   untested pointer at a table in a book,
   and Asset A without this feed.
2. **OSF registration (settled, not open).**
   Campaign decision E-1 (approved
   2026-10-21) settles that every
   specification in the pass files its own
   OSF contract registration at its freeze.
   The freeze of Spec 046 therefore files
   one, following the Specs 036–039 pattern.
   Nothing is filed at draft.
3. **OPEN-1 — The PARTIAL CONCURRENCE word.**
   DD-046-3 adds it to make the outcome
   mapping total. The freeze confirms the
   word, renames it, or re-maps it — openly,
   and provided every score pattern still
   lands in exactly one outcome.
4. **OPEN-2 — The Wells list of record.**
   This draft proposes the 2015 book's own
   sign apparatus (the matching witnessed in
   Phases 120–124 was against Wells 2015).
   The freeze names the edition and
   apparatus of record, or substitutes
   another Wells list openly.
5. **OPEN-3 — The CISI list of record.**
   Which sign-list apparatus in the held
   CISI volumes counts as "the CISI list",
   its edition, and its locator form. The
   design names "the CISI lists" without
   fixing this; the freeze fixes it, before
   any row is scored.
6. **OPEN-4 — The Mahadevan edition of
   record.** The design names "Mahadevan's
   list" without an edition. The freeze
   names the edition and locator form.
7. **OPEN-5 — List lineage.** Whether a
   lineage note (the published lists'
   scholarly interdependence) is appended
   to the CONSENSUS wording's limits before
   scoring. The counting rule itself is not
   open: it is DD-046-2 / F046-C08.
8. **OPEN-6 — The Spec 045 cross-check.**
   Before either spec freezes, this draft's
   §6 delivery form is read against Spec
   045's Asset A acceptance form as finally
   drafted, and any field mismatch is
   resolved openly at the later freeze.
   D-18 executes first (Wave 3, group 1), so
   a mismatch discovered at execution would
   be a campaign tripwire, not a drafting
   fix — it belongs at the freezes.
9. **OPEN-7 — Synthetic / dry-run check.**
   Whether execution requires a worked
   dry-run of the §5 scoring on a sign other
   than 297 (to prove the mapping machinery
   before it touches the target sign). This
   draft takes no position; the freeze
   decides and records it.

## 4. Draft-fixed readings (stand unless the freeze overturns them openly)

Each is labelled **DECIDED-BY-DRAFT**:

- **DD-046-1 — The delivery form is this
  draft's decision.** Spec §6 fixes the
  concordance output exactly: file
  (`concordance-297.json`), top-level fields,
  the one-sign record's fields, the four
  list rows' fields and concurrence states,
  the `asset_a_feed` block and its
  per-outcome rules, and the citation/locator
  string form. It is coordinated with Spec
  045's stated acceptance form for Asset A
  inputs — a sign-by-sign record whose
  depicted-kind label carries its published
  source per sign (campaign plan Part 3;
  design D-05's data statement) — and the
  coordination is recorded here because Spec
  045's draft is being written in parallel
  (OPEN-6 carries the cross-check).
- **DD-046-2 — Wells never counts toward
  CONSENSUS.** Design D-18 lists Wells among
  the concordance lists and requires "at
  least two independent published lists" for
  CONSENSUS, without noting that the source
  is Wells 2015. A source cannot corroborate
  itself; the Wells row is scored as SOURCE
  and the agreement count runs over CISI,
  Parpola, and Mahadevan (claim F046-C08).
- **DD-046-3 — PARTIAL CONCURRENCE completes
  the outcome set.** The design's three
  words leave exactly-one-independent-
  agreement unmapped (see §6, defect D-1).
  The draft adds the fourth word rather
  than letting execution improvise one.
- **DD-046-4 — SILENT carries
  `entry_present`.** A list that has the
  sign but names no referent, and a list
  that does not carry the sign at all, are
  different states of the published record;
  the design's single SILENT word is kept,
  and the sub-state is recorded per row so
  the difference is not lost.
- **DD-046-5 — Agreement is scored at the
  tiger-kind level.** The source hedges its
  own qualifier ("horned tiger, or perhaps
  just 'tiger' generically"); a list saying
  plain "tiger" therefore agrees, with the
  qualifier recorded verbatim rather than
  scored.
- **DD-046-6 — A list that can be neither
  produced nor cited with a locator closes
  the run at step 0.** The design's test set
  is "every published sign list the program
  holds or can lawfully cite", named as four
  lists in the campaign's falsifier. A
  three-list concordance would change what
  CONSENSUS means; the gate makes the full
  set a precondition instead (claim
  F046-C05), and CITABLE is defined by a
  quotable-locator standard, not by a list's
  fame.
- **DD-046-7 — No execution phase number at
  draft.** Allocated at the freeze act, from
  the merged record as it then stands.
- **DD-046-8 — Evidence carries
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
  requirement text forward: for each claim,
  what observable record, produced by the
  run itself, would show the requirement
  held?
- **Derivation B** worked from the falsifier
  and the pre-written outcome wordings
  backward: for each claim, what would a
  hostile reader check in the outcome record
  to show the requirement had *not* held?

The two derivations agreed on the gate and
inspection tests for F046-C02, C05, C06,
C11, C12, C13, and C15 without amendment:
in each case A's "record produced in order"
and B's "absence or disorder of that record
falsifies" are the same check read from the
two directions, and the register states it
once.

Disagreements, and their resolutions:

- **X-1 — Does Wells count toward
  CONSENSUS?** A, reading design D-18's list
  set naively, counted all four lists as
  potential agreers. B, reading the
  hypothesis ("not one scholar's call"),
  noted the source *is* Wells and a
  self-agreement would satisfy A's count
  with one real corroboration. **Resolution:**
  B governs; the design's own word
  "independent" carries it. Recorded as
  DD-046-2 / F046-C08, and the hypothesis
  claim F046-C03 is stated over independent
  lists only.
- **X-2 — Is the outcome mapping total?**
  A mapped rows to the design's three
  words directly. B enumerated the score
  patterns (independent agreements 0, 1, or
  ≥2, crossed with disagreement present or
  absent) and found the pattern (1, absent)
  mapped by no word: it is not CONSENSUS
  (needs ≥2), not SINGLE-SOURCE (the design
  says "only the original source identifies
  it so", and here another list does), not
  CONTESTED (nothing disagrees).
  **Resolution:** the gap is a defect in
  the design's outcome set (§6, D-1); the
  draft adds PARTIAL CONCURRENCE
  (DD-046-3 / F046-C10) and flags it
  OPEN-1 for the freeze. The alternative —
  folding (1, absent) into SINGLE-SOURCE —
  was rejected because it would misstate a
  real corroboration as its absence.
- **X-3 — What is a silent list?** A scored
  "sign absent from the list" and "entry
  present, no referent named" both as
  SILENT and stopped there. B held the two
  states support different conclusions
  about the published record (a list that
  never catalogued the sign vs a list that
  catalogued it and declined a referent).
  **Resolution:** the design's SILENT word
  is kept as the scored state; the
  distinction is preserved as the mandatory
  `entry_present` sub-state (DD-046-4 /
  F046-C09).
- **X-4 — Must agreement include the
  horns?** A required the identification
  "horned tiger" in full. B quoted the
  source against A: the source itself is
  unsure of the qualifier ("or perhaps just
  'tiger' generically"), so A's rule would
  score the source's own hedged wording as
  a partial disagreement with any plain
  "tiger" list. **Resolution:** agreement
  at the tiger-kind level, qualifier
  recorded verbatim (DD-046-5 / F046-C09).
- **X-5 — How producible must a list be?**
  A allowed a list to enter the concordance
  on a bibliographic citation alone. B
  required the citation to carry a locator
  form specific enough to quote an entry
  from — otherwise the step-0 gate passes a
  list whose row can never actually be
  written, and the failure surfaces
  mid-scoring instead of at the gate.
  **Resolution:** B's standard is the gate's
  (DD-046-6 / F046-C05): HELD, or CITABLE
  with citation plus locator form; anything
  less closes the run at step 0.
- **X-6 — Prose table or machine-readable
  delivery?** A proposed the outcome record's
  prose table as the delivery to Asset A.
  B, working from Spec 045's side, held
  that a prose delivery forces the asset
  build to re-interpret the concordance —
  an unrecorded second scoring, at exactly
  the hand-off the campaign wants pinned.
  **Resolution:** the JSON file in spec §6
  is the deliverable of record; the prose
  rendering is required to match it
  (DD-046-1 / F046-C11).

## 6. Defects found at drafting

- **D-1 — Design D-18's outcome set is not
  total.** CONSENSUS / SINGLE-SOURCE /
  CONTESTED map no word onto exactly one
  independent agreement with no
  disagreement (see X-2). Repaired at draft
  by DD-046-3, flagged OPEN-1; the design
  itself is not edited.
- **D-2 — The design does not address the
  source being a concordance list.** D-18
  names Wells among the four lists and
  requires "independent" agreement for
  CONSENSUS, without stating that the
  fragment's source book is Wells 2015.
  Left unfixed, the naive reading
  manufactures consensus out of
  self-agreement plus one corroboration.
  Repaired at draft by DD-046-2.
- **D-3 — The design's identification step
  does not warn that sign numbers collide
  across lists.** In the program's own
  registry, Parpola's 297 is a ladder motif
  and the Wells-297 registry cell sits
  inside a range on an unrelated row; a
  number-match would silently identify the
  wrong sign and every later row would
  score a concordance about a different
  drawing. Repaired at draft by F046-C07
  and spec §4.3's named traps.
- **D-4 — Spec 045 was not readable at this
  draft.** The two drafts are written in
  parallel by design (campaign Part 4), so
  the §6 delivery form is coordinated with
  Spec 045's *stated* acceptance form (the
  campaign plan's and D-05's description of
  Asset A inputs), not with Spec 045's draft
  text. The cross-check is carried as
  OPEN-6 at both freezes; if the forms
  mismatch, that is a freeze-gate finding,
  not something execution may paper over.
- **D-5 — Two of the four lists are named
  without editions in the design.** "The
  CISI lists" and "Mahadevan's list" do not
  fix editions or locator forms. Carried as
  OPEN-3 / OPEN-4 for the freeze; the
  step-0 gate (DD-046-6) is written so an
  unfixed list cannot slip through at
  execution either.

No defect was found that prevents stating
the falsifier, the step-0 gates, or the
pre-written wordings for the full outcome
set; the draft therefore advances as a
draft. Nothing in this section amends
design D-18, which stands as written in
the packet.

## 7. Freeze decisions — 2026-10-21

> ## FREEZE ACT — 2026-10-21
>
> This spec was frozen on 2026-10-21 under
> the runnable-experiments campaign plan
> approved by the owner AS WRITTEN on
> 2026-10-21 (campaign Wave 2; decision
> E-1). Every OPEN item in §3 is resolved
> here, on the record. DD-046-1, DD-046-2,
> DD-046-3, and DD-046-6 are CONFIRMED as
> drafted and stand unchanged. The AEE
> lifecycle hooks passed at the freeze gate
> over the recovered register 0.7-draft
> (DD-046-16; `aee/freeze-aee-note.md`), and
> the freeze digest in `freeze.json` was
> computed exactly once over the recovered
> register and the finalised freeze texts.

- **DD-046-9 — OPEN-1 RESOLVED: PARTIAL
  CONCURRENCE is confirmed.** The word
  stands as drafted (DD-046-3), in the
  space form "PARTIAL CONCURRENCE" used in
  spec §§5.2, 5.3, and 11 and in claim
  F046-C10. The one hyphenated spelling in
  draft spec §6 (`PARTIAL-CONCURRENCE`) is
  aligned to the space form at this freeze;
  that is a spelling alignment, not a
  rename and not a re-mapping. The §5.2
  mapping stays total: every pattern of
  scored rows lands in exactly one of
  CONSENSUS, CONTESTED, PARTIAL
  CONCURRENCE, or SINGLE-SOURCE.
- **DD-046-10 — OPEN-2 RESOLVED: the Wells
  list of record.** The 2015 book's own
  sign apparatus, as proposed at draft:
  Chapter 2, "The Indus Sign List"
  (Figure 2.6), in Bryan K. Wells, *The
  Archaeology and Epigraphy of Indus
  Writing* (Archaeopress, 2015; ISBN
  978 1 78491 046 4), held as cleaned text
  in the repository (SHA-256 `62acf855…`,
  spec §2). Named from held records with
  locators: the held text's Chapter 2
  (its contents listing and Figure 2.6)
  and the program's citation record
  (CITATIONS.md §A.7, Wells 2015, with
  technical appendices by Andreas Fuls).
  Locator form: chapter/figure plus the
  book's own sign number. Recorded in
  spec §2 at this freeze.
- **DD-046-11 — OPEN-3 RESOLVED: the CISI
  list of record (the Parpola list is named
  in the same decision, for completeness).**
  CISI: the catalogue apparatus of the
  CISI volumes as held digitally and
  complete — Vol. 1 (Joshi & Parpola
  (eds.), *Corpus of Indus Seals and
  Inscriptions. 1: Collections in India*,
  1987; Memoirs of the Archaeological
  Survey of India, vol. 86) and Vol. 2
  (Shah & Parpola (eds.), *Corpus of Indus
  Seals and Inscriptions. 2: Collections
  in Pakistan*, 1991) — as catalogued in
  the program's Phase-124 catalogue layers.
  Named from held records with locators:
  CITATIONS.md §§A.2–A.3 (full citations
  for both volumes); Spec 023 §2
  (scans in hand: Vol. 1, 431 scan pages;
  Vol. 2, 486 scan pages); Spec 027
  Stage 0 record (the Phase-124 catalogue
  layers `cisi_vol1_catalogue.csv` and
  `cisi_vol2_catalogue.csv`). Locator
  form: volume plus catalogue/object entry
  plus page or plate. A CISI row scores an
  identification only where a volume entry
  itself gives one; otherwise SILENT with
  `entry_present` (spec §10 prices this
  in). Parpola: Asko Parpola, *Deciphering
  the Indus Script* (Cambridge University
  Press, 1994; CITATIONS.md §C.1), the sign
  list of 386 signs, locator form P-number
  (the registry is keyed to Parpola 1982
  numbering). Recorded in spec §2 at this
  freeze.
- **DD-046-12 — OPEN-4 RESOLVED: the
  Mahadevan edition of record.** Iravatham
  Mahadevan, *The Indus Script: Texts,
  Concordance and Tables* (Memoirs of the
  Archaeological Survey of India, No. 77;
  New Delhi: Archaeological Survey of
  India, 1977) — the M77 sign list
  (419 signs). Named from held records with
  locators: CITATIONS.md §A.1 (full
  citation, pp. 825, and the §11 signary
  note); the program's Mahadevan–Parpola
  crosswalk records, which cite the same
  edition. Locator form: M-number plus
  concordance/tables page or entry.
  Recorded in spec §2 at this freeze.
- **DD-046-13 — OPEN-5 RESOLVED: the
  lineage note IS added.** Before any row
  is scored, openly, at this freeze: the
  note stands in spec §5.3's CONSENSUS
  wording and in spec §7 — independence
  is publication-level only, the lists'
  scholarly traditions borrow from each
  other, and this concordance does not
  audit their genealogy. The counting rule
  (DD-046-2 / F046-C08) is unchanged, and
  no row may be re-weighted after scoring.
- **DD-046-14 — OPEN-6 CROSS-CHECK:
  Spec 045-side repair recorded.** Spec
  046's §6 delivery form was read in full
  against Spec 045's draft text (PR #244,
  branch `spec-045-hunt-depicted-kinds-draft`,
  spec §2.6, "What Asset A accepts from
  D-18"). Verdict: **aligned in form,
  NOT aligned in outcome vocabulary —
  a FREEZE-stage finding for Spec 045's
  freeze to repair on its side.** Aligned:
  a machine-readable JSON file is an
  accepted input form; the per-list
  verdicts (AGREE / DISAGREE / SILENT, with
  verbatim identifications) match §2.6's
  row requirements; the file is produced
  on every terminal outcome, with an empty
  signs array plus a closure block on a
  closure, which satisfies §2.6's timing
  rule in substance (Asset A freezes when
  the table is landed or a closure record
  is on record); a CONTESTED feed forces
  a dispute record instead of picking a
  side, matching §2.6's CONTESTED rule;
  CONSENSUS and SINGLE-SOURCE rows can be
  consumed as corroborating citations.
  Not aligned, in Spec 045's draft text
  as written: (1) §2.6 enumerates the
  D-18 outcomes it accepts as CONSENSUS,
  SINGLE-SOURCE, CONTESTED, or
  IDENTIFICATION FAILED — **PARTIAL
  CONCURRENCE has no consumption rule
  there**, so a PARTIAL CONCURRENCE feed
  (depicted kind "animal", source plus a
  single corroboration, flagged as such
  under spec 046 §6) cannot be ingested
  as drafted; (2) §2.6 does not name the
  CLOSED AT STEP 0 outcome class that
  spec 046 §11 can end in; (3) §2.6
  rejects a row whose crosswalk key does
  not resolve in the pinned crosswalk,
  while spec 046 §6 lawfully produces a
  sign matched by Wells-list entry with
  `crosswalk_registry_id` null. Per the
  freeze instruction, **Spec 046's outcome
  vocabulary is NOT changed to fit**: the
  total outcome set is the design repair
  of record (DD-046-3, defect D-1). The
  repair belongs to Spec 045's freeze,
  which is also a draft-stage act: its
  §2.6 enumeration and consumption rules
  must be extended there to ingest
  PARTIAL CONCURRENCE, to name the
  closure-file form (concordance produced
  on every terminal outcome; closures =
  empty signs plus a closure block), and
  to state how a Wells-list-entry match
  with a null registry id is keyed.
- **DD-046-15 — OPEN-7 RESOLVED: no
  separate dry-run sign is required.** A
  worked dry-run of §5 scoring on a sign
  other than 297 would require opening the
  lists for scoring work outside the
  registered test, and the §5.2 mapping
  needs no such proof: it is a total
  function of the four published rows, and
  the outcome record must show its
  derivation from those rows alone
  (F046-C10's falsifier). The mapping's
  totality over every score pattern is
  pinned mechanically in
  `backend/tests/test_spec046_freeze.py`
  at this freeze. If execution cannot
  derive its state from its own rows, the
  run is non-compliant on its face.
- **DD-046-16 — The AEE gate reading.**
  The DD-038-10 / DD-039-8 reading is
  adopted for this spec: the lifecycle
  hooks PASS at the freeze when every hook
  carries zero correctness failure modes
  and no claim below the 0.70 threshold,
  with the engine outcome word reading
  "iterate" solely from the FR-2.3
  draft-cap records. At this freeze, over
  the recovered register 0.7-draft under
  aee 1.5.0: after_specify, after_plan,
  and after_tasks each carry exactly 15
  failure modes, all draft-cap; minimum
  propagated confidence 0.72. The recovery
  rounds are recorded in
  `aee/freeze-aee-note.md` and in the
  register's own note.
- **DD-046-17 — Phase allocation
  (resolving DD-046-7).** The execution
  phase number is **Phase-405**, allocated
  at this freeze from the merged record as
  it stands (Phase-403 was Spec 039's
  execution; the campaign's Wave 2 freeze
  allocation for this spec is Phase-405).
- **DD-046-18 — OSF registration and the
  execution gate.** Under campaign decision
  E-1, this spec's own OSF contract
  registration is filed at this freeze
  (record in `freeze.md` and
  `osf-spec-registration.md`). Execution
  does NOT run at the freeze, and it
  awaits the registration's approval:
  approval proceeds via the token link in
  OSF's admin-notification email, which is
  the parent agent's act — this freeze
  act does not touch Gmail.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
