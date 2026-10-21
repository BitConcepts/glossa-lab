# Spec 046 — "Sign 297 Is the Horned Tiger": an Identification Concordance (Design D-18)

> ## FROZEN — 2026-10-21
>
> Frozen under the runnable-experiments
> campaign plan approved by the owner AS
> WRITTEN on 2026-10-21
> (`~/workspace/your_files/2026-10-21-runnable-experiments-campaign-plan.md`,
> Parts 1–4): campaign member 13, design
> D-18, drafted alongside D-05 (Spec 045)
> because its concordance resolutions FEED
> Asset A, the depicted-kind classification
> D-05 builds (campaign Part 3; decision
> E-6). The freeze decisions are recorded in
> `adjudication.md` §7 (DD-046-9 to
> DD-046-18), the AEE lifecycle hooks passed
> at the freeze gate over the recovered
> register 0.7-draft (`aee/freeze-aee-note.md`),
> and the freeze digest is in `freeze.json`.
> The spec's own OSF contract registration
> was filed at this freeze under campaign
> decision E-1 (record in `freeze.md`);
> execution awaits that registration's
> approval and the campaign's execution
> pass. **Execution is a separate later
> act.** Nothing in this spec has been run
> or computed.
>
> The execution phase number is
> **Phase-405**, allocated at this freeze
> (DD-046-17, resolving DD-046-7).

**Design source:** D-18 in the experiment-design
packet at PR #195
(`docs/research/experiment-designs-2026-10-13/03-fragments.md`,
§D-18, read in full at this draft).

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

The record is a fragment. Automatic extraction
pulled one sentence's claim out of a source
book and kept the sign number while losing
the sign list it belongs to. The claim record
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
The passage the extraction came from, read
first-hand at this draft (printed page 97 in
the held text, in the discussion headed
"Proto-Dravidian and the Indus Script"), says:

> "Sign 532 and sign 297 are positioned in
> such a way as to resemble the position of
> the graphic element and several of their
> features are repeated in the image field.
> It is proposed here that sign 532 is a
> logograph for the anthropomorphic figure
> and that sign 297 represents the horned
> tiger, or perhaps just 'tiger' generically."

Phase-104 evaluated this record and stopped
at the door (RULE-NUM): the sign number is
cited without a stated numbering system, no
matching entry was located in the program's
crosswalk registry (86 numeric IDs present
in that record), and the extraction carries
no falsification condition. The claim's own
adopted explanation states what is unknown:
which drawn sign this is, and whether its
identification as a horned tiger is agreed
or one scholar's call.

One fact shapes the whole design and is
fixed here, not discovered at execution:
**the source author is Wells, and Wells's
sign list is also one of the four lists the
concordance compares.** A list cannot
corroborate itself. Wells's row in the
concordance is therefore scored in the role
SOURCE, and the agreement count that decides
CONSENSUS runs over the other three lists
only (§5, claim F046-C08, DD-046-2).

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
| Claim record (`glossa-indus/claims/extracted_claims/the_archaeology_and_epigraphy_of_indus_w_27f45a68.json`) | SHA-256 `bd0f7abddc9c26537f4ebe5f66f6a1fc69d394a4c2edbe745a8b7eb1ddc3333a` (recomputed at this draft from `main` at 82b29490; the §2 inputs are unchanged on current `main`) |
| Source book, held cleaned text (`glossa-indus/processed/cleaned_text/the_archaeology_and_epigraphy_of_indus_w_27f45a68.txt`) | SHA-256 `62acf855ac3ecf39fc7a7e6597dba9a3cb6e35948528f69e9424eb81308d261e` (recomputed at this draft) |
| Phase-104 evaluation (`glossa-indus/reports/phase104_claims_evaluation.json`) | SHA-256 `2d0b83e8055a04b96635007054cfadde472f605dc7e5b249a61c8f9ea89b858d` (recomputed at this draft) |
| Crosswalk registry (`data/crosswalks/canonical_sign_registry.csv`) | SHA-256 `8a0b2a82ac8d226d574ce01f5550c581efd91a97cab86201a62f7a7e435bd420` (recomputed at this draft; 803 rows as held today — the registry has grown since Phase-104's 86-numeric-ID record, and execution re-asserts this pin rather than inheriting either count) |
| Lane-2 adopted drafts (`specs/029-tao-claim-lifecycle/lane2-drafts/drafts.json`) | SHA-256 `3f645c9a4132ba5a0bc5fca4ca22810b8b6169a2f1f9f85f35990c7b72df33fb` (recomputed at this draft) |

The four concordance lists. The editions of
record were fixed at the freeze
(`adjudication.md` §7, DD-046-10 to
DD-046-12); the step-0 gate (§3, gate 0.2)
is where each list's posture is proven at
execution:

| List (list_id) | Role | Posture at this draft |
|---|---|---|
| Wells (`WELLS`) | SOURCE | HELD. List of record (freeze, DD-046-10, resolving OPEN-2): the sign apparatus of Wells 2015 itself — Chapter 2, "The Indus Sign List" (Figure 2.6, "An Indus Sign List"), in Bryan K. Wells, *The Archaeology and Epigraphy of Indus Writing* (Archaeopress, 2015; ISBN 978 1 78491 046 4), held as cleaned text (above). Locator form: chapter/figure plus the book's own sign number; the §1 passage (printed p. 97) is the identification of record under §5.1. |
| CISI (`CISI`) | INDEPENDENT | HELD. List of record (freeze, DD-046-11, resolving OPEN-3): the catalogue apparatus of the CISI volumes as held digitally and complete — Vol. 1 (Joshi & Parpola (eds.), *Corpus of Indus Seals and Inscriptions. 1: Collections in India*, 1987; MASI 86) and Vol. 2 (Shah & Parpola (eds.), *Corpus of Indus Seals and Inscriptions. 2: Collections in Pakistan*, 1991) — as catalogued in the program's Phase-124 catalogue layers (Spec 027 Stage 0 record; Spec 023 §2 scans-in-hand record). Locator form: volume plus catalogue/object entry plus page or plate. The CISI row scores an identification only where a volume entry itself gives one; otherwise the row is SILENT with its `entry_present` sub-state (§10). |
| Parpola (`PARPOLA`) | INDEPENDENT | HELD or CITABLE. List of record (freeze, DD-046-11): Parpola's published sign identifications in Asko Parpola, *Deciphering the Indus Script* (Cambridge University Press, 1994; the sign list of 386 signs), with the locator form P-number — the program's crosswalk registry is keyed to Parpola 1982 numbering, and the row's locator records that P-number with the 1994 identification quoted at it. |
| Mahadevan (`MAHADEVAN`) | INDEPENDENT | HELD or CITABLE. Edition of record (freeze, DD-046-12, resolving OPEN-4): Iravatham Mahadevan, *The Indus Script: Texts, Concordance and Tables* (Memoirs of the Archaeological Survey of India, No. 77, 1977) — the M77 sign list (419 signs). Locator form: M-number plus the concordance/tables page or entry. The program holds Mahadevan crosswalk data (registry `mahadevan_ids` coverage). |

No corpus, positional data, or classification
asset is an input to this spec. In
particular, Asset A (Spec 045) is **not** an
input: this spec feeds it and does not draw
on it (§7, claim F046-C12).

## 3. Step 0 — gates before any identification or scoring (fail-closed)

Execution runs these checks in order, before
step 1. A failure closes the execution in
the class named; nothing is repaired at run
time, and no list is substituted.

- **0.1 Input integrity.** Every §2 input
  hashes to its freeze-record value. A
  mismatch closes the run as **CLOSED AT
  STEP 0 — INPUT PIN MISMATCH**, naming the
  input.
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

## 4. Step 1 — identification (a gate before scoring)

As design D-15 step 1, applied to this
source:

1. **Name the source's sign list from the
   document itself** — from the book's own
   sign apparatus, headings, or citations.
   The reading this draft expects, from the
   held text, is that the passage's numbering
   is Wells's own (the passage stands in
   Wells 2015, and no other list is named at
   the passage); step 1 must confirm that
   from the document's apparatus, not assume
   it from this draft. If the list cannot be
   named from the document, the design closes
   as **IDENTIFICATION FAILED (list
   unnamed)**, and the record stays a stated
   gap.
2. **Match the drawn sign.** Wells's sign
   297 is matched, by its drawn form in
   Wells's own list or figures, to an entry
   in the program's crosswalk registry, or —
   if the registry carries no entry for the
   drawn sign — fixed by a drawn-sign
   reference to Wells's published list entry
   itself. The citation is attached either
   way, and the match (registry id, or the
   Wells list locator) is recorded in the
   §6 output's `target_sign` block. If the
   drawn sign cannot be matched, the design
   closes as **IDENTIFICATION FAILED (sign
   unmatched)**.
3. **Numbers are not identities.** A sign
   number is meaningful only inside its own
   list. Matching across lists is by drawn
   sign (through the crosswalk registry or
   drawn-form comparison), never by number.
   The traps are on record in the registry
   itself, read at this draft: Parpola's
   P297 is described there as a "Ladder
   motif" — a different sign from Wells's
   297 — and the registry's `W297` value
   appears inside a multi-value `wells_ids`
   cell on the P205 row ("Prismed light
   rays…"), which does not by itself identify
   the passage's sign either. A run that
   matches by number is non-compliant on its
   face (claim F046-C07).

Only a sign identified under this step is
scored in step 2.

## 5. Step 2 — the concordance test

### 5.1 Scoring each list

For each of the four lists, the executor
locates that list's entry for the drawn sign
identified in step 1 (by drawn sign, §4.3),
quotes its identification **verbatim**, and
scores the row:

- **AGREE** — the list identifies the drawn
  sign as a tiger. The "horned" qualifier is
  recorded, not scored: the source itself
  hedges ("horned tiger, or perhaps just
  'tiger' generically"), so tiger with or
  without horns agrees at the kind level
  (DD-046-5). The normalised identification
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
  of the list, not a vote (DD-046-4).

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
  identification either. This outcome fills a
  gap in design D-18's three-word set, which
  maps no word onto this pattern; it is this
  draft's addition (DD-046-3), and the freeze
  may rename or re-map it openly, provided
  the mapping stays total.
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
material filled from the run:

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
  lineage (freeze note, DD-046-13). This settles what the
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
  concur in the sense Spec 046's hypothesis
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
  Wells's published list]. The record stays
  a stated gap. No statement about the sign
  is made, and nothing is fed to Asset A."
- CLOSED AT STEP 0: "Spec 046 closed before
  identification: [the source book could not
  be produced from the program's held copy /
  the published list [name] could be neither
  produced nor cited with a locator / input
  [name] did not hash to its frozen pin].
  No concordance was run and no statement
  about the sign is made."

## 6. The delivery form — what D-18 delivers, and in what form (the Asset A contract)

This section fixes the concordance output
exactly, so Spec 045's Asset A build can
consume it without a further agreement. The
delivery form is this draft's decision —
**DECIDED-BY-DRAFT (DD-046-1)** — coordinated
with Spec 045's stated acceptance form for
Asset A inputs: a sign-by-sign record whose
depicted-kind label carries its published
source, per sign (campaign plan Part 3;
design D-05's data statement).

**Deliverable of record:** a machine-readable
file `concordance-297.json`, produced at
execution in this spec's directory
(`specs/046-horned-tiger-concordance/`),
plus its human-readable rendering inside the
outcome record (§8). The JSON is the form
Asset A consumes; the rendering is for
readers and must not diverge from it.

**Top-level fields:**

- `producer_spec`: `"046"`;
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
  Wells list locator)}`.
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

- **Number collision (§4.3).** The standing
  trap of this fragment family: identical
  numbers naming different signs in different
  lists. Controlled by drawn-sign matching
  only, with the two registry traps named in
  advance.
- **Source self-agreement.** Wells is both
  the claim's source and a concordance list.
  Controlled structurally: the SOURCE role
  never counts toward CONSENSUS (§5.2,
  F046-C08).
- **List lineage.** "Independent" in §5.2
  means independently *published* lists,
  other than the source. It does not assert
  that the lists' scholarly traditions are
  unrelated — sign lists borrow from each
  other, and this concordance does not audit
  their genealogy. The limit is stated
  wherever CONSENSUS is stated, and the
  freeze may add a lineage note, openly,
  before any row is scored (OPEN-5); it may
  not re-weight rows after scoring.
  **Freeze note (DD-046-13, resolving
  OPEN-5):** the lineage note IS added, at
  this freeze, before any row is scored: it
  stands in the §5.3 CONSENSUS wording above
  and in this bullet — independence in §5.2
  is publication-level only, sign lists
  borrow from each other, and no output may
  present CONSENSUS as agreement between
  unrelated scholarly traditions. The
  counting rule is unchanged.
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
  pin is asserted (§3, gate 0.1), and a
  match that cannot be defended from the
  recorded reference fails step 1 rather
  than being argued at scoring time.
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
   the sign meant in use."

Deliverables at execution: `concordance-297.json`
(§6), the outcome append in this directory,
the appended first-check entry on the claim
`the_archaeology_and_epigraphy_of_indus_w_27f45a68_sign_val_0002`'s
record, the experiment-graph node (H15/H23,
registered and verified before the run), and
the LEDGER entry (H1). Foundation check
(H21) after the execution phase: 0 failures,
or the outcome record says why not.

Execution order within the campaign (plan
Part 4, Wave 3): **this spec executes in
group 1, before Asset A freezes**, so the
§6 file exists — in whatever terminal state
it reaches, including an empty-feed closure —
before Spec 045's step 1 build consumes it.
If this spec closes before scoring, Asset A
proceeds without this feed and records its
absence; the closure does not block the
asset, and the asset may not reconstruct the
feed from its own labels (§7).

## 9. Epistemic limits (binding on all outputs)

1. **Identification layer only.** Even a
   CONSENSUS settles what the drawn sign
   depicts, as the field's published lists
   record it. It does not establish that the
   sign *meant* a horned tiger in use, any
   role it played in inscriptions, or any
   reading of any text (design D-18's own
   limit, carried verbatim in substance).
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
5. Negative, single-source, partial, and
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
- **Drawn-form matching is the soft step.**
  §7 makes it inspectable; it does not make
  it mechanical. A contested match is a
  step-1 defect, surfaced as such, not a
  scoring dispute.
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
  name the source's list from the document,
  or cannot match the drawn sign.
- **CLOSED AT STEP 0** — SOURCE NOT
  PRODUCIBLE, LIST NOT PRODUCIBLE (list
  named), or INPUT PIN MISMATCH (input
  named).

## 12. Execution shape (gated; NOT run by this draft)

1. **Graph-first build** (H15/H23) — script,
   graph node, registration, verification.
2. **Step 0** (§3) — input integrity, source
   producible, four lists accounted for.
3. **Step 1** (§4) — list named from the
   document; drawn sign matched by form;
   citation attached.
4. **Step 2** (§5) — four rows quoted and
   scored; outcome by the §5.2 mapping.
5. **Delivery and outcome** (§§6, 8) —
   `concordance-297.json` written on every
   terminal outcome; outcome append; the
   claim's first-check append; LEDGER entry;
   foundation check reported as measured.
   In campaign order this lands in Wave 3
   group 1, before Asset A freezes.

## 13. What this spec is not

Not a decipherment, not a test of what any
sign means, not Asset A (that is Spec 045's
build — this spec supplies one input row to
it), not a corpus statistic of any kind, and
not an authorisation to execute. It is an
identification concordance for one fragment,
designed so that its honest outcomes —
including closing at its own gates — are
written down before any list is opened for
scoring.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
