# Spec 064 — "Sign 297 Is the Horned Tiger": an Identification Concordance, Successor to Spec 046 (Drawn-Form Reference Preserved)

> ## FROZEN — 2026-10-21
>
> Frozen under the owner's approval of
> 2026-10-21 (amendment package Item 5: build
> Spec 064, the successor to Spec 046, through
> freeze and OSF filing), on the
> amendment-queue commission of the same date
> (Item 5: drawn-form references for Wells's
> signs 821 and 297;
> `~/workspace/research_notes/amendment-queue-2026-10-21/item-5-drawn-form-references.md`,
> whose §6.2 is the reference record, §7 the
> identification protocol, and §8 the
> successor's charter, followed exactly).
> The freeze decisions are recorded in
> `adjudication.md` §7 (DD-064-14 to
> DD-064-18), the AEE lifecycle hooks passed
> at the freeze gate over the recovered
> register (`aee/freeze-aee-note.md`), and
> the freeze digest is in `freeze.json`. The
> spec's own OSF contract registration was
> filed at this freeze under campaign
> decision E-1 (record in `freeze.md`);
> execution awaits that registration's
> approval and a separate execution order.
> **Execution is a separate later act.**
> Nothing in this spec has been run or
> computed.
>
> The execution phase number is
> **Phase-426**, allocated at this freeze
> (DD-064-15).

**Design source:** Spec 046
(`specs/046-horned-tiger-concordance/`,
design D-18), carried as this successor's
contract except where §4 and §3 state the
successor's changes; and the amendment
draft Item 5, §§6.2, 7, 8.

**Claim under test:**
`the_archaeology_and_epigraphy_of_indus_w_27f45a68_sign_val_0002`
— UNTESTED fragment: "Sign value: 297 / the
horned tiger, or perhaps just 'tiger'
generically."

**AI disclosure:** this draft is produced by an
AI agent (Muse Spark, via Muse) at the
direction of Tristen Pierson, per constitution
§VI.

---

## 1. The claim and the record it stands on

The record is the same fragment Spec 046
tested. Automatic extraction pulled one
sentence's claim out of a source book and
kept the sign number while losing the sign
list it belongs to. The claim record
(`glossa-indus/claims/extracted_claims/the_archaeology_and_epigraphy_of_indus_w_27f45a68.json`,
pinned in §2) states, verbatim:

> "Sign value: 297 / the horned tiger, or
> perhaps just 'tiger' generically"

The source document is Bryan K. Wells, *The
Archaeology and Epigraphy of Indus Writing*
(Archaeopress, 2015; ISBN 978 1 78491 046 4;
technical appendices by Andreas Fuls), held
by the program as cleaned text
(`glossa-indus/processed/cleaned_text/the_archaeology_and_epigraphy_of_indus_w_27f45a68.txt`).
The passage the extraction came from
(printed page 97 in the held text, held text
lines 2938–2941, in the discussion headed
"Proto-Dravidian and the Indus Script"),
says:

> "Sign 532 and sign 297 are positioned in
> such a way as to resemble the position of
> the graphic element and several of their
> features are repeated in the image field.
> It is proposed here that sign 532 is a
> logograph for the anthropomorphic figure
> and that sign 297 represents the horned
> tiger, or perhaps just 'tiger' generically."

**What Spec 046 did, and why this successor
exists.** Spec 046 (Phase-405, executed
2026-10-21 under its frozen contract; OSF
registration dnts8, APPROVED + PUBLIC)
passed step 0 in full, named the source's
list from the book's own apparatus at step
1.1, and closed **IDENTIFICATION FAILED
(sign unmatched)** at step 1.2: Figure 2.6's
drawn forms did not survive the held copy's
text extraction (captions only, held text
lines 868–880), so no inspectable drawn-form
reference existed in the held record, and
the drawn sign could not be matched by drawn
form. Its closure delivery
(`specs/046-horned-tiger-concordance/concordance-297.json`,
SHA-256
`772db4df152ec4f1071bed088250677e55f69743532c9e89f339a8cf9134aaaf`)
stands unedited; Spec 046 is never patched
(DD-064-9). Its outcome named the unblocking
act: an inspectable drawn-form reference for
Wells's sign 297 preserved as a committed,
hashed record. This successor performs that
preservation act inside its own directory
(§2, the reference record) and re-runs the
concordance question with step 1.2
satisfiable through it, under the
identification protocol of §4.

One fact shapes the whole design and is
fixed here, not discovered at execution:
**the source author is Wells, and Wells's
sign list is also one of the four lists the
concordance compares.** A list cannot
corroborate itself. Wells's row in the
concordance is therefore scored in the role
SOURCE, and the agreement count that decides
CONSENSUS runs over the other three lists
only (§5, claim F064-C08, DD-064-2).

**The qualification this successor carries.**
The preserved reference's continuity status
is **QUALIFIED** (reference record,
`continuity_status`): no record the program
holds anchors the number 297 individually
from the 2015 side — the anchor is
family-level only (the P205 cell groups
W289–W306 as one Parpola sign's Wells
counterparts, under a bent-ray description;
the thesis plates show the whole 289–308
run as one bent-ray family). The QUALIFIED
status is load-bearing, not decorative:
step C of the identification protocol (§4)
is **mandatory** in this successor, and the
closure **IDENTIFICATION FAILED
(continuity/discrimination not sustained)**
is pre-registered if either independent
derivation cannot affirm that the
descriptor picks out plate 297 and no
neighbour in the 289–308 run. The QUALIFIED
status is carried into this spec's
reporting wherever its result would be
stated (§8).

### 1.1 The question, in plain words

A book says a particular drawn sign — its
number 297 — depicts a horned tiger. Is that
identification the field's published
consensus for that drawn sign, or is it one
scholar's call that the other published sign
lists do not share? The check is a
concordance: find the drawn sign, then ask
each published sign list what it says the
sign depicts, in its own words.

### 1.2 The hypothesis and its falsifier

**Hypothesis.** The identification "horned
tiger" is the published consensus for this
drawn sign, not one scholar's call: at least
two published lists independent of the
source agree on it, and no published list
the program holds or can cite disagrees.

**Falsifier.** The published sign lists
(CISI, Parpola, Mahadevan, Wells) do not
concur on the identification: any one of
them identifies the drawn sign as something
else, or the agreement the hypothesis needs
is not there — the identification stands on
the source alone, or on the source plus a
single corroboration.

## 2. Inputs (pinned at this draft; re-asserted at the freeze)

| Input | Pin / state |
|---|---|
| Claim record (`glossa-indus/claims/extracted_claims/the_archaeology_and_epigraphy_of_indus_w_27f45a68.json`) | SHA-256 `997fa33699ccce3feecfe0d09f6e6a1dbd165c05cd9f255939ad96e84bc99031` (recomputed at this freeze from `main` at e03f7832; the record now carries Spec 046's dated first-check append of Phase-405 beside the frozen entry — its bytes differ from Spec 046's draft pin for that recorded reason, and the fragment entry itself is unchanged: untested, stage created) |
| Source book, held cleaned text (`glossa-indus/processed/cleaned_text/the_archaeology_and_epigraphy_of_indus_w_27f45a68.txt`) | SHA-256 `62acf855ac3ecf39fc7a7e6597dba9a3cb6e35948528f69e9424eb81308d261e` (recomputed at this freeze, two routes) |
| Phase-104 evaluation (`glossa-indus/reports/phase104_claims_evaluation.json`) | SHA-256 `2d0b83e8055a04b96635007054cfadde472f605dc7e5b249a61c8f9ea89b858d` (recomputed at this freeze) |
| Crosswalk registry (`data/crosswalks/canonical_sign_registry.csv`) | SHA-256 `8a0b2a82ac8d226d574ce01f5550c581efd91a97cab86201a62f7a7e435bd420` (recomputed at this freeze, two routes; 803 rows) |
| Phase-123 Wells segmentation witness (`data/crosswalks/wells_segmentation_witness_v1.csv`) | SHA-256 `ecbc37a461553cd1d06fb7f88a27d2daf85bf53c40b7558f597cbc6735b3c0da` (recomputed at this freeze, two routes; 157 rows; carries no grapheme 297 — the string "297" appears in it only as the Mahadevan label M297, whose Wells grapheme is 924) |
| Lane-2 adopted drafts (`specs/029-tao-claim-lifecycle/lane2-drafts/drafts.json`) | SHA-256 `3f645c9a4132ba5a0bc5fca4ca22810b8b6169a2f1f9f85f35990c7b72df33fb` (recomputed at this freeze) |
| Spec 046 closure delivery (`specs/046-horned-tiger-concordance/concordance-297.json`) | SHA-256 `772db4df152ec4f1071bed088250677e55f69743532c9e89f339a8cf9134aaaf` (recomputed at this freeze, two routes; stands unedited — DD-064-9) |
| **Drawn-form reference for sign 297 (`specs/064-sign297-concordance-successor/drawn-form-reference-297.json`)** | **SHA-256 `33ee22ec182fdc416a6c0db6abbc0bc61b06b448f50defafd18fc856afd6ede4`** (computed at its commitment in this spec — the preservation act, DD-064-10; schema `glossa.drawn-form-reference/1`; contents exactly the amendment draft §6.2 record; no images) |
| Wells 2006 PhD thesis PDF (local research store only; **not committed**) | SHA-256 `4b39330c7f4ccf2770093318bfdaf4efaffa7fdf4a8cb5763a650351fffa4b4e`, 19,313,853 bytes (open deposit, Internet Archive item `epigraphicapproachestoinduswritingbryankennethwellsphd.thesis_230_Z`; asserted on the local file at step 0 before any plate is read — gate 0.4) |

The four concordance lists. The editions of
record are carried unchanged from Spec
046's freeze (DD-046-10 to DD-046-12,
carried by DD-064-18); the step-0 gate (§3,
gate 0.3) is where each list's posture is
proven at execution:

| List (list_id) | Role | Posture |
|---|---|---|
| Wells (`WELLS`) | SOURCE | HELD. List of record: the sign apparatus of Wells 2015 itself — Chapter 2, "The Indus Sign List" (Figure 2.6, "An Indus Sign List"), in Bryan K. Wells, *The Archaeology and Epigraphy of Indus Writing* (Archaeopress, 2015; ISBN 978 1 78491 046 4), held as cleaned text (above). Locator form: chapter/figure plus the book's own sign number; the §1 passage (printed p. 97) is the identification of record under §5.1. |
| CISI (`CISI`) | INDEPENDENT | HELD. List of record: the catalogue apparatus of the CISI volumes as held digitally and complete — Vol. 1 (Joshi & Parpola (eds.), *Corpus of Indus Seals and Inscriptions. 1: Collections in India*, 1987; MASI 86) and Vol. 2 (Shah & Parpola (eds.), *Corpus of Indus Seals and Inscriptions. 2: Collections in Pakistan*, 1991) — as catalogued in the program's Phase-124 catalogue layers. Locator form: volume plus catalogue/object entry plus page or plate. The CISI row scores an identification only where a volume entry itself gives one; otherwise the row is SILENT with its `entry_present` sub-state (§10). |
| Parpola (`PARPOLA`) | INDEPENDENT | HELD or CITABLE. List of record: Parpola's published sign identifications in Asko Parpola, *Deciphering the Indus Script* (Cambridge University Press, 1994; the sign list of 386 signs), with the locator form P-number — the program's crosswalk registry is keyed to Parpola 1982 numbering, and the row's locator records that P-number with the 1994 identification quoted at it. |
| Mahadevan (`MAHADEVAN`) | INDEPENDENT | HELD or CITABLE. Edition of record: Iravatham Mahadevan, *The Indus Script: Texts, Concordance and Tables* (Memoirs of the Archaeological Survey of India, No. 77, 1977) — the M77 sign list (419 signs). Locator form: M-number plus the concordance/tables page or entry. The program holds Mahadevan crosswalk data (registry `mahadevan_ids` coverage). |

No corpus, positional data, or classification
asset is an input to this spec. In
particular, Asset A (Spec 045) is **not** an
input: this spec feeds it and does not draw
on it (§7, claim F064-C12). Asset A consumes
only this successor's delivery if one is
produced (DD-064-9); Spec 046's closure
delivery is not an Asset A input under this
spec.

## 3. Step 0 — gates before any identification or scoring (fail-closed)

Execution runs these checks in order, before
step 1. A failure closes the execution in
the class named; nothing is repaired at run
time, and no list or artefact is substituted.

- **0.1 Input integrity.** Every §2 input
  hashes to its freeze-record value,
  including the preserved reference record
  at its pinned digest. A mismatch closes
  the run as **CLOSED AT STEP 0 — INPUT PIN
  MISMATCH**, naming the input.
- **0.2 Source producible.** The source book
  can be produced from the program's held
  copy and the §1 passage located in it
  verbatim. If it cannot, the run closes as
  **CLOSED AT STEP 0 — SOURCE NOT
  PRODUCIBLE**.
- **0.3 All four lists producible or
  citable.** Each of the four lists in §2 is
  accounted for as HELD (a copy the program
  can open) or CITABLE (a full bibliographic
  citation plus the list's own locator form
  — volume, page or table, and its sign
  numbering — specific enough that its entry
  for a named drawn sign can be quoted by a
  reader who holds the list). A list that is
  neither closes the run as **CLOSED AT STEP
  0 — LIST NOT PRODUCIBLE**, naming the
  list. There is no three-list concordance:
  the outcome rules in §5 count over the
  full named set, and a missing list would
  silently change what CONSENSUS means.
- **0.4 Reference producible.** The §2
  reference record exists at its pinned
  digest, and the thesis plate page it cites
  (thesis p. 90 / PDF p. 102) is produced
  from the local thesis file after that
  file's digest is asserted against its §2
  pin (`4b39330c…`). A reference that cannot
  be produced, or a local file that does not
  hash to its pin, closes the run as
  **CLOSED AT STEP 0 — REFERENCE NOT
  PRODUCIBLE**. No substitute artefact is
  admitted.

## 4. Step 1 — identification (a gate before scoring)

Step 1.1 is Spec 046's step 1.1, carried.
Step 1.2 is performed by the identification
protocol of the amendment draft §7, frozen
here as steps D, C, and M.

1. **Name the source's sign list from the
   document itself** — from the book's own
   sign apparatus, headings, or citations.
   The reading this draft expects, from the
   held text, is that the passage's numbering
   is Wells's own (the list-naming evidence
   is held text lines 414 and 665, recorded
   in the reference record's `target` block);
   step 1 must confirm that from the
   document's apparatus, not assume it from
   this draft. If the list cannot be named
   from the document, the design closes as
   **IDENTIFICATION FAILED (list unnamed)**,
   and the record stays a stated gap.
2. **Step D — descriptor derivation, twice.**
   Two independent derivations of the
   drawn-form descriptor from the thesis
   plate (Figure 3.2, thesis p. 90 / PDF
   p. 102), each performed without sight of
   the other and without sight of the
   reference record's drafted descriptor
   wording, each recording: the plate
   locator, the feature list it read (stroke
   count, bend, splay), and the neighbour set
   it discriminated against. Reconciliation
   is by the recorded features; an unsettled
   disagreement is recorded verbatim and
   resolves **against** identification. The
   reconciled descriptor is then compared
   with the reference record's descriptor:
   agreement is required; a material
   difference closes the run as
   **IDENTIFICATION FAILED (reference not
   sustained)**, naming the difference. (The
   preserved descriptor is thereby *checked*,
   not inherited.)
3. **Step C — continuity/discrimination
   (MANDATORY in this successor).** The run
   states, from the record, what anchors the
   plate number to the 2011/2015 numbering:
   the family anchor (reference record,
   `family_anchor_2015`) carried with its
   frozen status — corroboration only, NOT
   an identification. The two step-D
   derivations must **each** affirm that the
   reconciled descriptor picks out the
   plate's 297 and no neighbour in the
   289–308 run. If either derivation cannot
   affirm the discrimination, the run closes
   as **IDENTIFICATION FAILED
   (continuity/discrimination not
   sustained)** — a pre-registered closure,
   not a defect discovered at scoring time.
4. **Step M — the match.** The drawn sign is
   identified by exactly one of:
   - **Route 1 (registry, by drawn form):** a
     registry row whose drawn description
     matches the reconciled descriptor —
     never by number, and the frozen traps
     (below) asserted as traps in the run
     record.
   - **Route 2 (the list's own entry, quoted
     with its locator):** the §2 reference
     record itself, cited as the preserved
     drawn-form reference for the source
     list's entry — the route Spec 046's
     step 1.2 already admitted, now
     satisfiable because the reference exists
     as a committed, hashed, inspectable
     record.
   No route may be constructed at run time;
   the composition route of the amendment
   draft §7 is sign-821-only and is **not**
   a route under this spec (no formation
   text for 297 exists). A run that finds
   neither frozen route satisfiable closes
   as **IDENTIFICATION FAILED (sign
   unmatched)**. The citation is attached
   either way, and the match (registry id,
   or the reference record with its digest)
   is recorded in the §6 output's
   `target_sign` block.
5. **Numbers are not identities.** A sign
   number is meaningful only inside its own
   list. Matching across lists is by drawn
   sign, never by number. The traps are on
   record in the reference record's
   `traps_named` and are asserted in every
   run record: P205's `wells_ids` cell used
   as an identification; P297 "Ladder motif";
   witness M297 (whose Wells grapheme is
   924); P205's Mahadevan crosswalk M180 used
   as W297's identity; any number-only match,
   including a plate number read without
   step C. A run that matches by number is
   non-compliant on its face (claim
   F064-C07).

Only a sign identified under this step is
scored in step 2.

## 5. Step 2 — the concordance test

### 5.1 Scoring each list

For each of the four lists, the executor
locates that list's entry for the drawn sign
identified in step 1 (by drawn sign, §4.5),
quotes its identification **verbatim**, and
scores the row:

- **AGREE** — the list identifies the drawn
  sign as a tiger. The "horned" qualifier is
  recorded, not scored: the source itself
  hedges ("horned tiger, or perhaps just
  'tiger' generically"), so tiger with or
  without horns agrees at the kind level
  (DD-064-5). The normalised identification
  records the exact kind term the list uses.
- **DISAGREE** — the list identifies the
  drawn sign as something other than a
  tiger: a different animal, a non-animal
  referent, or a functional/graphic
  description offered as its identification.
  The disagreeing identification is quoted,
  never paraphrased.
- **SILENT** — the list gives no referent
  identification for the drawn sign. The row
  records the sub-state `entry_present`:
  `true` (an entry exists but names no
  referent) or `false` (the drawn sign has
  no entry in the list). Silence is a state
  of the list, not a vote (DD-064-4).

The Wells row is scored from the book's own
sign apparatus where it states one, with the
§1 passage as its identification of record;
its role is SOURCE. If Wells's own apparatus
contradicts his passage, that divergence is
quoted in the row and the outcome cannot be
CONSENSUS (it is recorded under CONTESTED,
with the divergence named as Wells-internal).

### 5.2 Outcome rules (fixed in advance; total over all score patterns)

Let A = the number of INDEPENDENT lists
(CISI, Parpola, Mahadevan) scored AGREE, and
D = the number of lists of any role scored
DISAGREE (including a Wells-internal
divergence under §5.1):

- **CONSENSUS** — A ≥ 2 and D = 0. The
  hypothesis (§1.2) stands: the
  identification is the published consensus.
- **CONTESTED** — D ≥ 1, whatever A is. The
  falsifier fires in its active form: the
  lists do not concur, and the disagreeing
  identification is quoted in the outcome.
- **PARTIAL CONCURRENCE** — A = 1 and D = 0.
  The falsifier fires in its weaker form:
  the lists do not concur in the hypothesis's
  sense — one independent corroboration is
  not a consensus — but no list disputes the
  identification either.
- **SINGLE-SOURCE** — A = 0 and D = 0. Only
  the source identifies the sign so; every
  independent list is silent. The falsifier
  fires: the identification is one scholar's
  call on the published record.

CONSENSUS is the only outcome that supports
the hypothesis. The other three are the
falsifier's outcomes, in three distinct
shapes, and each is recorded with the same
prominence (§8).

### 5.3 Pre-written verdict wordings

The outcome record's headline paragraph uses
one of these forms, with the bracketed
material filled from the run. Every wording
that states a result of this successor
carries the qualification sentence appended:
"**Qualification (carried from the preserved
reference, Spec 064 §1): the identification
of Wells's 297 rests on a drawn-form
reference whose continuity status is
QUALIFIED — anchored at family level only;
its step C discrimination check is part of
this run's record.**"

- CONSENSUS: "The drawn sign that Wells
  (2015) numbers 297 and identifies as the
  horned tiger is identified as a tiger by at
  least two published sign lists independent
  of the source ([lists, with locators]), and
  no held or citable published list
  identifies it otherwise. On the published
  record, 'horned tiger' is the field's
  identification for this sign, not one
  scholar's call. The lists counted are
  independent as published lists; this
  concordance does not audit their scholarly
  lineage (DD-064-18, carrying Spec 046's
  DD-046-13). This settles what the
  drawn sign depicts, as the field's lists
  record it — the identification layer only.
  It does not establish what the sign meant
  in use."
- PARTIAL CONCURRENCE: "The drawn sign that
  Wells (2015) numbers 297 and identifies as
  the horned tiger is corroborated by
  exactly one independent published list
  ([list, with locator]); the remaining
  independent lists are silent, and none
  disagrees. The published lists do not
  concur in the sense Spec 064's hypothesis
  requires: the identification stands on the
  source plus a single corroboration, and is
  fed to Asset A flagged as such."
- SINGLE-SOURCE: "No independent published
  list identifies the drawn sign that Wells
  (2015) numbers 297 as a tiger, and none
  identifies it as anything else: every
  independent list is silent ([silent lists,
  with entry states]). 'Horned tiger' is, on
  the published record the program holds or
  can cite, Wells's identification alone."
- CONTESTED: "The published lists do not
  concur on the drawn sign that Wells (2015)
  numbers 297. [List] identifies it as
  '[quoted identification]' ([locator]),
  against the source's 'horned tiger'. The
  identification is contested on the
  published record, and the contest — not
  either identification — is what is fed to
  Asset A."
- IDENTIFICATION FAILED: "The fragment
  'sign 297 is the horned tiger' cannot be
  carried to a concordance: [the source
  document does not name its sign list / the
  drawn sign could not be matched from
  Wells's published list / the preserved
  reference was not sustained by the two
  independent derivations / the descriptor's
  discrimination of 297 from its neighbours
  in the 289–308 run was not sustained by
  both independent derivations]. The record
  stays a stated gap. No statement about the
  sign is made, and nothing is fed to
  Asset A." The closure class recorded
  names the limb that failed, including —
  where it is the continuity limb — the
  class **IDENTIFICATION FAILED
  (continuity/discrimination not
  sustained)** verbatim.
- CLOSED AT STEP 0: "Spec 064 closed before
  identification: [the source book could not
  be produced from the program's held copy /
  the published list [name] could be neither
  produced nor cited with a locator / input
  [name] did not hash to its frozen pin / the
  preserved drawn-form reference could not be
  produced at its pinned digest, or the
  thesis file did not hash to its pin]. No
  concordance was run and no statement about
  the sign is made."

## 6. The delivery form — what the successor delivers, and in what form (the Asset A contract)

The delivery form is carried from Spec 046
§6 (DD-064-1), coordinated with Spec 045's
stated acceptance form for Asset A inputs: a
sign-by-sign record whose depicted-kind label
carries its published source, per sign.

**Deliverable of record:** a machine-readable
file `concordance-297.json`, produced at
execution in **this spec's directory**
(`specs/064-sign297-concordance-successor/`),
plus its human-readable rendering inside the
outcome record (§8). The JSON is the form
Asset A consumes; the rendering is for
readers and must not diverge from it. Asset
A consumes only this successor's delivery if
one is produced (DD-064-9); Spec 046's
closure delivery stands unedited in its own
directory and is not overwritten, replaced,
or re-issued by this spec.

**Top-level fields:**

- `producer_spec`: `"064"`;
  `producer_claim_id`: the claim id in the
  header of this spec; `schema`:
  `"glossa.concordance/1"`.
- `signs`: an array of sign records. This
  spec produces exactly one element; the
  array shape is the asset-facing form, so a
  future concordance of the same shape needs
  no new contract.
- On a closure before scoring (step 0 or
  IDENTIFICATION FAILED), `signs` is an empty
  array and the top level carries
  `closure`: `{class, wording}` with the
  §5.3 wording used. An empty feed is a
  stated state, never an absent file: the
  file is produced on every terminal
  outcome.

**Each sign record carries:**

- `target_sign`: `{source_document_id,
  source_list_named, source_sign_no: "297",
  source_passage_quote (verbatim),
  source_locator, crosswalk_registry_id
  (string or null), drawn_sign_match_basis
  ("crosswalk-registry" or "wells-list-entry"),
  drawn_sign_ref (the registry id or the
  Wells list locator), drawn_form_reference
  (the §2 reference record's path and its
  pinned digest, recorded on every outcome
  in which identification was attempted)}`.
- `lists`: exactly four rows, one per list,
  each `{list_id (CISI | PARPOLA | MAHADEVAN
  | WELLS), role (SOURCE | INDEPENDENT),
  bibliographic_citation,
  availability (HELD | CITABLE),
  locator {volume, page, table_or_figure,
  list_sign_no (that list's own number for
  the drawn sign, or null)},
  entry_present (boolean),
  identification_verbatim (quoted string or
  null), identification_normalised (the
  depicted-kind term, or null),
  concurrence_state (AGREE | DISAGREE |
  SILENT)}`.
- `concurrence_state` (the per-sign state):
  one of `CONSENSUS | PARTIAL CONCURRENCE |
  SINGLE-SOURCE | CONTESTED`, computed by
  §5.2 from the four rows and shown beside
  them.
- `asset_a_feed`: `{depicted_kind,
  specific_identification, concurrence_state,
  flagged_disputed, disputed_identifications}`.
  Rules: on CONSENSUS, PARTIAL CONCURRENCE,
  or SINGLE-SOURCE, `depicted_kind` is
  `"animal"`, `specific_identification` is
  `"horned tiger"` (the source's term, with
  the generic-tiger hedge carried in
  `identification_verbatim` rows),
  `flagged_disputed` is `false`, and the
  concurrence state travels with the label so
  Asset A's dispute rule can weigh a
  single-source or partial label differently
  from a consensus one. On CONTESTED,
  `depicted_kind` and
  `specific_identification` are `null`,
  `flagged_disputed` is `true`, and
  `disputed_identifications` carries every
  verbatim identification on record (source's
  and dissenter's), so the asset records the
  dispute instead of silently picking a side.

**Citation/locator form** (used in every row
and in every outcome product): a single line
of the form
`<list_id> — <author/editor, short title,
year> — <volume>:<page or table>, sign
<list_sign_no>; quoted: '<verbatim
identification>'` — e.g. in shape,
`WELLS — Wells, The Archaeology and
Epigraphy of Indus Writing, 2015 — p. 97,
sign 297; quoted: 'the horned tiger, or
perhaps just 'tiger' generically'`. A row
that cannot be written in this form is not
a scored row; it is a step-0 or step-1
failure, recorded as such.

## 7. Controls and named confounders

- **Number collision (§4.5).** The standing
  trap of this fragment family: identical
  numbers naming different signs in different
  lists. Controlled by drawn-sign matching
  only, with the traps named in advance in
  the reference record and in §4.5 —
  including the successor's own new surface
  for the same trap: a plate number read
  without step C.
- **Source self-agreement.** Wells is both
  the claim's source and a concordance list.
  Controlled structurally: the SOURCE role
  never counts toward CONSENSUS (§5.2,
  F064-C08).
- **List lineage.** "Independent" in §5.2
  means independently *published* lists,
  other than the source. It does not assert
  that the lists' scholarly traditions are
  unrelated — sign lists borrow from each
  other, and this concordance does not audit
  their genealogy. The limit is stated
  wherever CONSENSUS is stated (the lineage
  note carried from Spec 046's freeze,
  DD-046-13, stands in the §5.3 CONSENSUS
  wording). The counting rule is unchanged,
  and no row may be re-weighted after
  scoring.
- **No drawing on the asset it feeds.** The
  scorer works from the published lists
  only. Asset A, D-05's labels, and all
  positional results are excluded from the
  matching and scoring work, so the feed
  cannot be circular.
- **Matching judgement.** Drawn-form matching
  across differently drawn published lists is
  a judgement. It is controlled by making it
  inspectable: the match basis and reference
  are recorded per sign (§6), the registry
  pin is asserted (§3, gate 0.1), both
  step-D derivation sheets and the step C
  statement are part of the run record (§8),
  and a match that cannot be defended from
  the recorded reference fails step 1 rather
  than being argued at scoring time.
- **The QUALIFIED reference.** The reference
  this successor runs on is weaker than a
  list-anchored reference, and the weakness
  is priced into the contract rather than
  noted beside it: step C is mandatory, its
  failure closure is pre-registered (§4.3),
  and the QUALIFIED status travels with
  every statement of the result (§§5.3, 8).
  A run may not present an identification
  under this spec as unqualified.
- **The source's own hedge.** "Horned tiger,
  or perhaps just 'tiger' generically" is
  one identification with a qualifier in
  doubt, not two identifications. Scoring at
  the kind level (§5.1) is the control; the
  verbatim hedge is quoted in every product
  so the doubt travels with the result.

## 8. Reporting obligations

Every product of an execution carries:

1. the §1 passage, quoted, with its locator;
2. all four list rows, each in the §6
   citation/locator form, with the verbatim
   identification (or its SILENT state and
   `entry_present` sub-state);
3. the per-sign concurrence state and the
   §5.3 headline wording for the outcome
   reached;
4. the `asset_a_feed` block, exactly as
   delivered;
5. the fence sentence: "This result settles
   what the published lists say the drawn
   sign depicts. It is not evidence of what
   the sign meant in use.";
6. **the successor's identification record:**
   the §2 reference record's digest; both
   step-D derivation sheets and their
   reconciliation; the step C statement with
   the family anchor carried at its frozen
   status; the route used at step M and the
   traps asserted; and the reference's
   QUALIFIED continuity status, stated
   wherever the run's result is stated.

Deliverables at execution: `concordance-297.json`
(§6, in this spec's directory), the outcome
append in this directory, the appended
first-check entry on the claim
`the_archaeology_and_epigraphy_of_indus_w_27f45a68_sign_val_0002`'s
record, the experiment-graph node (H15/H23,
registered and verified before the run), and
the LEDGER entry (H1). Foundation check
(H21) after the execution phase: 0 failures,
or the outcome record says why not.

Execution order: this successor executes
only under a separate execution order, after
its OSF registration's approval act. Spec
046's closure already satisfied Asset A's
timing rule in closure form; if this
successor closes before scoring, Asset A
proceeds on the record it already has and
records this successor's closure; the asset
may not reconstruct any feed from its own
labels (§7).

## 9. Epistemic limits (binding on all outputs)

1. **Identification layer only.** Even a
   CONSENSUS settles what the drawn sign
   depicts, as the field's published lists
   record it. It does not establish that the
   sign *meant* a horned tiger in use, any
   role it played in inscriptions, or any
   reading of any text.
2. **Concordance is not correctness.** Lists
   can concur and be wrong together; this
   test measures agreement on the published
   record, which is the claim the fragment
   actually makes available. No output may
   present CONSENSUS as proof about the
   ancient sign beyond the identification
   layer.
3. **One sign.** The feed is one sign's
   record. It strengthens or warns Asset A
   by exactly one row, and no output may
   generalise it to other animal
   identifications.
4. **Silence is not disagreement, and
   disagreement is not error.** SILENT rows
   and the CONTESTED outcome are recorded as
   states of the published record, with the
   same prominence as CONSENSUS.
5. **The frozen reference is QUALIFIED.** It
   does not establish that 297's
   identification will survive its own step C
   discrimination check; Spec 046's
   IDENTIFICATION FAILED stands until a
   successor execution produces its own
   outcome. No output of this spec may state
   its identification without the
   qualification where the identification is
   stated before step C has run and been
   recorded.
6. Negative, single-source, partial, and
   closure outcomes publish with the same
   prominence as consensus.

## 10. Risks and honest weaknesses

- **SINGLE-SOURCE is a live, likely outcome.**
  Referent identifications are unevenly
  published across the four lists; several
  may be silent on this sign. The design
  prices that in: a single-source finding is
  a result the claim's record needs, not a
  failure of the run.
- **The CISI row may be structurally
  silent.** A corpus volume's sign apparatus
  may present drawn signs without referent
  identifications for most entries. That is
  recorded as SILENT with its sub-state, not
  argued around.
- **Discrimination within the bent-ray run
  is fine-grained.** Neighbouring plate
  signs (295, 296, 299, 300–306) are the
  same family, differing in stroke count,
  bend position, and splay. This is the
  successor's soft step, and it is exactly
  what step C exists to check with a
  pre-registered failure closure; §7 makes
  the check inspectable, it does not make
  it mechanical.
- **The thesis list is an earlier state of
  the list.** The plates print the 2006 form
  (676 signs); the fragment's numbering is
  the 2011 form as given in 2015 (694
  signs). The plate number therefore
  identifies nothing by itself in this
  successor: continuity is a checked claim
  (step C), anchored where the 2015-side
  record independently fixes the family —
  and, for 297, only the family.
- **The book's apparatus may not name its
  list at the passage.** Step 1 reads the
  apparatus as a whole; if the naming is
  genuinely absent, IDENTIFICATION FAILED is
  the honest outcome and is pre-written.

## 11. Stop conditions and outcome classes

Execution ends in exactly one of:

- **CONSENSUS**, **PARTIAL CONCURRENCE**,
  **SINGLE-SOURCE**, or **CONTESTED** —
  per §5.2, after all gates pass.
- **IDENTIFICATION FAILED** — step 1 cannot
  name the source's list from the document
  (list unnamed); the preserved reference is
  not sustained by the two derivations
  (reference not sustained); the step C
  discrimination is not affirmed by both
  derivations (**continuity/discrimination
  not sustained**); or no frozen route at
  step M is satisfiable (sign unmatched).
- **CLOSED AT STEP 0** — SOURCE NOT
  PRODUCIBLE, LIST NOT PRODUCIBLE (list
  named), INPUT PIN MISMATCH (input named),
  or REFERENCE NOT PRODUCIBLE.

## 12. Execution shape (gated; NOT run by this draft)

1. **Graph-first build** (H15/H23) — script,
   graph node, registration, verification.
2. **Step 0** (§3) — input integrity
   (including the reference record at its
   pinned digest), source producible, four
   lists accounted for, reference producible
   (thesis file digest asserted, plate page
   produced).
3. **Step 1** (§4) — list named from the
   document; step D derivations and
   reconciliation; step C continuity /
   discrimination; step M match by a frozen
   route; traps asserted; citation attached.
4. **Step 2** (§5) — four rows quoted and
   scored; outcome by the §5.2 mapping.
5. **Delivery and outcome** (§§6, 8) —
   `concordance-297.json` written in this
   spec's directory on every terminal
   outcome; outcome append; the claim's
   first-check append; LEDGER entry;
   foundation check reported as measured.

## 13. What this spec is not

Not a decipherment, not a test of what any
sign means, not Asset A (that is Spec 045's
build — this spec supplies one input row to
it), not a patch to Spec 046 (its frozen
record, its outcome, and its closure
delivery stand exactly as executed), not a
corpus statistic of any kind, and not an
authorisation to execute. It is an
identification concordance for one fragment,
run on a preserved drawn-form reference
whose continuity status is QUALIFIED by its
own record, designed so that its honest
outcomes — including closing again as
IDENTIFICATION FAILED on the continuity
limb — are written down before any list is
opened for scoring.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
