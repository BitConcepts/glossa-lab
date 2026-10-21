# Spec 049 — Hunt: The Opening Signs Are the Animal Signs (Design D-06; Consumer of Asset A)

> ## DESIGN DRAFT — FOR FREEZE DECISION — 2026-10-21
>
> Drafted under the runnable-experiments campaign
> approved by the owner **as written** on
> 2026-10-21
> (`~/workspace/your_files/2026-10-21-runnable-experiments-campaign-plan.md`,
> Parts 1–4; decisions E-1…E-7 as written).
> The campaign approval is the commissioning
> basis for this **draft**. It is not a freeze
> order and not an execution order: the freeze
> and the execution of Spec 049 remain separate
> later acts under the campaign's Waves 2 and 3.
> No AEE lifecycle hooks have run on this draft;
> they are a freeze gate. Nothing in this draft
> has been run, frozen, registered, joined, or
> computed.
>
> This spec is campaign member 5 (design D-06),
> a **dependent**: it consumes **Asset A**, the
> depicted-kind sign classification built and
> frozen inside Spec 045 (design D-05, PR #244).
> It does not build, extend, or re-derive that
> asset. Asset A does not exist yet at this
> draft; §2 states the consumption contract and
> §5 makes its digest the first step-0 gate.
>
> The execution phase number is **unassigned**
> at this draft and is allocated at the freeze
> act, from the merged record as it then stands
> (DD-049-8).

**Design source:** D-06 in the experiment-design
packet at PR #195
(`docs/research/experiment-designs-2026-10-13/02-roif-and-hunt.md`,
§D-06, read in full at this draft), with the
packet README's shared-asset description, the
D-05 design (the asset's builder design), and
Spec 045's draft (§2 and adjudication, read in
full on branch `spec-045-hunt-depicted-kinds-draft`)
for the Asset A contract this draft is written
against.

**Claim under test:**
`without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_003`
— "Faunal signs function as identity/guild/
commodity prefixes (initial position)" —
standing **IN QUESTION**: partially supported
(positional half only), in the record's own
words: "40 INITIAL_STRONG signs identified;
faunal-initial enrichment not yet
sign-classified [STRUCTURAL SUPPORT ONLY]".

**AI disclosure:** this draft is produced by an
AI agent (Muse Spark, via Muse) at the
direction of Tristen Pierson, per constitution
§VI.

---

## 1. The claim and the record it stands on

The positional half of this claim is already
tested and stands. The program's Phase-43 work
found **40 signs that strongly prefer the
opening of inscriptions** (initial-strong
signs; mean initial rate **0.757** against
**0.251** expected by chance, over **201 signs
profiled**), recorded in the pinned positional
record
(`glossa-indus/analysis/positional/hunt_tripartite_test.json`,
SHA-256 `0e546962…`, recomputed at this draft
from `main` at `83b6a563…`) and in the Phase-43
battery record (`outputs/phase43_all.json`,
SHA-256 `78a6c219…`, recomputed at this draft).

The animal half has never been tested at all.
Hunt's claim says the opening signs **are** the
animal signs — fish, unicorn, buffalo,
rhinoceros, tiger, elephant, in his naming.
Nobody has ever checked whether the 40 are the
animals, because the program held no
classification of which signs depict animals.
That classification is Asset A, built by
Spec 045 from published identifications. With
it frozen, this claim's own test can finally
run — exactly as the claim's record states it.

The claim's recorded falsification condition,
verbatim: "Faunal signs not enriched in
initial position above random baseline."

### 1.1 The question, in plain words

Forty signs strongly prefer the opening of
inscriptions. Are those forty the animal signs?
One join — the frozen classification against
the forty — and one exact test answer it. The
positional half is not re-run; this spec tests
only the half that has always been missing.

### 1.2 The hypothesis and its falsifier

**Hypothesis.** Animal signs — the signs the
frozen Asset A classes `depicted_kind = animal`
— are enriched among the opening-strong signs
relative to their share of the sign inventory.

**Falsifier.** Opening-strong signs are animal
signs at no better than the base rate: animal
signs appear among the opening-strong set at
or below the rate the inventory share predicts,
under the criterion of §4.3. If the falsifier
fires, the claim's animal half is recorded as
not supported, in the pre-written words of
§4.6, and the claim stands on its positional
half alone — stated as such, not averaged away.

## 2. What this spec consumes: Asset A (the contract, restated)

Asset A is defined by Spec 045 §2; this section
restates the parts this spec's test depends on,
so a reader of this draft need not take any of
them on trust. If this restatement and
Spec 045's text ever differ, Spec 045's text
governs and the difference is a defect in this
draft, recorded as such.

### 2.1 The asset's form

- One row per sign, in a single canonical file
  `asset-a/depicted-kind-classification.csv` in
  Spec 045's directory, keyed by the pinned
  crosswalk identity (`sign_key`, from
  `data/crosswalks/sign_crosswalk_master.csv`,
  pinned §3), each row also carrying the sign's
  CISI and Parpola numbers where the crosswalk
  records them.
- Fields include: `depicted_kind` ∈ {`animal`,
  `sky_cycle`, `object_goods`, `human`, `other`,
  `contested`, `unidentified`}; the governing
  source's verbatim published label
  (`depicted_label_verbatim`); the governing
  source and every source consulted, with
  citations (`governing_source`,
  `source_citations`); `agreement`; and
  `dispute_status`.
- This spec uses exactly one field value as its
  animal set: **`depicted_kind = animal`**. The
  design's naming of Hunt's animals (fish,
  unicorn, buffalo, rhinoceros, tiger, elephant,
  and any further faunal signs the published
  sources identify) is Hunt's claim, not a
  second classification: whatever the frozen
  asset classes animal is the animal set, and
  whatever it does not is not. No sign is added
  to or removed from the animal set by this
  spec, by Hunt's list, or by any worker's
  judgement.

### 2.2 Sources, blind entry, and disputes (Spec 045 §§2.3–2.5)

- Labels come only from held published sources:
  the **CISI volumes (Vols 1–2) govern**;
  **Parpola's published identifications govern
  where CISI is silent**; Mahadevan's and
  Wells's lists enter only through a D-18
  (Spec 046) concordance row.
- Entry is **blind to positional results** and
  the asset is **frozen before any join** to
  corpus or positional data.
- A sign whose governing sources disagree is
  `depicted_kind = contested`,
  `dispute_status = contested`, with both
  verbatim labels recorded. Contested signs
  are **excluded from primary analyses** and
  included, under the CISI-governed label, in
  a pre-registered sensitivity. `borderline`
  signs (the published identification hedged in
  its own source) stay in the primary under
  their governing label. `unidentified` signs
  carry the sources searched and no label.

### 2.3 The freeze and the digest pin

- Spec 045 freezes Asset A at its freeze point
  and records the SHA-256 of the canonical CSV
  in `specs/045-hunt-depicted-kinds/asset-a/asset-a-freeze.json`,
  with the row count, per-kind counts, input
  pins, and the build-order attestation.
- **This spec's freeze quotes that digest
  verbatim.** No digest value exists at this
  draft and none is asserted here: the freeze
  act copies the SHA-256 from
  `asset-a-freeze.json` into this spec's freeze
  record character for character, and step 0
  (§5, gate 0.2) asserts it against the asset
  as presented at execution. A mismatch is a
  pre-written step-0 closure (§4.6), never a
  re-derivation: nobody rebuilds "the same"
  classification inside this campaign
  (campaign requirement R-2).
- After its freeze the asset changes only by
  dated, append-only defect notices in
  Spec 045's record. A defect that reaches a
  verdict produced under this spec marks that
  verdict; it does not rewrite it.

### 2.4 The caution that travels with the asset

Spec 037's census found **object-type labels
diverging between compilations in 49% of
matched cases**. Asset A classifies **signs by
what they depict**, not objects by type, and
takes every label from the published sources
of §2.2 — but the census is the standing
warning that compilation labels are not
interchangeable. Asset A's published-source,
blind-entry, dispute-by-rule, freeze-before-join
construction is the design's answer to that
caution, and §8 carries the caution as a limit
on every statement of this spec's result: the
answer is the construction, not a claim that
the divergence does not exist.

## 3. Inputs (pinned at this draft; re-asserted at the freeze)

| Input | Pin / state |
|---|---|
| Positional record of the claim (`glossa-indus/analysis/positional/hunt_tripartite_test.json`) | SHA-256 `0e546962c1b72b929c87d4ce40c97633e8e3e340737f32f5dd3eae9f04759e48` (recomputed at this draft from `main` at `83b6a563…`): 40 initial-strong / 61 medial-strong / 20 terminal-strong signs; mean initial rate 0.757 vs 0.251 by chance. |
| Phase-43 battery record (`outputs/phase43_all.json`) | SHA-256 `78a6c21908b9362854c54dd3d820d717be22feab3af11135663fa14aaf554fe4` (recomputed at this draft): T2.2 records `initial_strong_count` 40, `medial_strong_count` 61, `terminal_strong_count` 20, `total_signs_profiled` 201; signs in T2.2 are expressed as `m77_sign` (Mahadevan numbers). |
| Corpus layer of record (`backend/glossa_lab/data/yajnadevam_inscriptions.csv`) — the pinned programme corpus layer (5,679 records), the source of the §4 occurrence counts under the draft reading of adjudication §5, item 3 | SHA-256 `c02e3d7bb74cf5abb11cc94f88d8d469e6acc5d6fad4b7153c02c43428f58d98` (recomputed at this draft; the same layer pinned by Specs 042 and 045). |
| Sign crosswalk of record (`data/crosswalks/sign_crosswalk_master.csv`) | SHA-256 `4ace1a617f40afe8d0bbb82e5461d98a675296152e7577b04fb67b00f4f5dfcf` (recomputed at this draft): 205 rows; 187 distinct registry identities; **only 17 rows carry a `mahadevan_1977` mapping** — the identity-space fact behind §5 gate 0.4 and OPEN item 1. |
| Claim record (`glossa-indus/claims/extracted_claims/without_kings_or_conquests_the_indus_scr_ce9d98cc.json`) | Read at this draft: claim `…_manual_003`, normalised claim, status, and falsification condition as quoted in §1. |
| Anchors file (`backend/reports/INDUS_FINAL_ANCHORS.json`) | SHA-256 `df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569` (recomputed at this draft). This spec moves no anchor; the file is asserted byte-identical before and after any execution. |
| **Asset A** (Spec 045, §2) | **Not yet in existence at this draft.** Consumed only as frozen: the canonical CSV plus `asset-a-freeze.json`. This spec's freeze quotes the asset's SHA-256 verbatim from that record (§2.3); step 0 asserts it (gate 0.2). No other form of the classification is an input. |

The **opening-strong population** is pinned as
the Phase-43 set of record: the 40
initial-strong signs whose count and rates the
two pinned records above state. The records
state the set's size and strength; they do not
store its member list (adjudication §5, item
1). The population is therefore pinned by
identity of definition — the Phase-43
initial-strong set, reproduced and enumerated
at step 0 under the keying and reproduction
rules the freeze fixes (gate 0.4) — and the
enumerated, keyed list is the execution's
first published product, before any join.

## 4. The test (runs only after every §5 gate passes)

### 4.1 Populations

- **O — the opening-strong set.** The 40 signs
  of §3, as enumerated and keyed at gate 0.4.
- **U — the comparison inventory.** Every sign
  with **at least 30 occurrences** in the
  pinned corpus layer, counted under the
  counting rule the freeze fixes
  (adjudication §6, item 2). U is enumerated
  and published at gate 0.5 with per-sign
  counts.
- **Classification.** Each sign in O and in U
  is animal, non-animal, contested, or
  unidentified **exactly as the frozen Asset A
  records it** (§2.1). Primary shares are
  computed over classified members only
  (animal vs non-animal); contested and
  unidentified members are counted, listed,
  and excluded from both numerator and
  denominator of the primary (DD-049-2), and
  the raw counts over the full sets are
  published beside them so nothing the
  exclusion does is invisible.

### 4.2 The two arms

- **Primary arm.** The share of animal signs
  among O versus the animal share of U:
  enrichment ratio **R1 = (animal share of O)
  / (animal share of U)**, with an exact test
  (Fisher's exact test on the disjoint 2×2
  table — O versus U∖O, animal versus
  non-animal — DD-049-4). The criterion p is
  the one-sided p in the enrichment direction;
  the two-sided p is published alongside it.
  Counts published in full: every cell, both
  sets' sizes, and the excluded counts of
  §4.1.
- **Reversed arm (pre-registered).** Among
  all animal signs in U, the share that are
  in O, versus the same share for non-animal
  signs in U: ratio **R2** with its exact test
  on the corresponding table. The reversed arm
  is verdict-bearing only as §4.3 orders it;
  it is computed and published whatever the
  primary finds.

### 4.3 Verdict criteria (fixed in advance; precedence as ordered)

Each arm's exact test is at the **5% level**.
The headline is decided by these rules, in
this order (the ordering is this draft's
reconciliation of the design's clauses,
DD-049-3; the freeze may re-order openly):

1. **NOT SUPPORTED** — if R1 ≤ 1.0, or the
   primary exact test cannot reject equality
   (p ≥ 0.05). This is the falsifier of §1.2,
   and it fires on the primary arm regardless
   of the reversed arm; a reversed-arm result
   against it is reported in the outcome's
   first paragraph as a recorded asymmetry,
   not as a headline change.
2. **SUPPORTED** — if R1 ≥ 1.5 with p < 0.05
   in the primary arm **and** the reversed arm
   does not contradict the direction (R2 > 1.0).
3. **INCONCLUSIVE** — in every other
   adjudicated case: 1.0 < R1 < 1.5 with
   p < 0.05; or R1 ≥ 1.5 with p < 0.05 but
   R2 ≤ 1.0 (the arms disagree); or the
   §4.1 baseline is empty (no animal signs in
   U's classified members — the ratio is then
   undefined and the census is the finding).

### 4.4 Sensitivities (pre-registered, two)

Reported beside the primary with the same
prominence; neither replaces the headline word.

- **S-A — contested included.** The primary
  arm rerun with contested signs included
  under their CISI-governed labels (the
  inclusion rule of Spec 045 §2.5), so the
  effect of the dispute rule's exclusion is
  measured, not assumed away.
- **S-B — the unicorn removed.** The primary
  arm rerun without the unicorn sign(s): the
  sign(s) whose frozen Asset A verbatim label
  identifies the unicorn — the commonest
  "animal" of Hunt's naming, and a composite
  creature whose identification is
  conventional. The removed sign(s) are named
  at gate 0.5 from the frozen asset's labels,
  before any test quantity exists. If no sign
  carries such a label, S-B is recorded as
  not applicable, with that fact stated.

### 4.5 Controls and named confounders

- **Frequency.** Common signs are more often
  classifiable as position-strong: the
  comparison inventory is restricted to signs
  with at least 30 occurrences, in both arms
  (the design's control, carried verbatim).
- **Classification disputes.** Contested signs
  are named and listed with both verbatim
  labels; the primary excludes them by the
  asset's rule and S-A measures the exclusion.
- **The unicorn problem.** Handled by S-B,
  pre-registered here, not improvised after a
  result is seen.
- **Identity keying.** The Phase-43 signs are
  expressed in Mahadevan numbers and Asset A
  is keyed by crosswalk identity; a sign that
  cannot be keyed under the frozen rule is a
  gate failure (§5), never a silent drop or a
  hand-keyed row.

### 4.6 Pre-written verdict wordings

The outcome record's headline paragraph uses
one of these forms, with the bracketed
quantities filled from the run:

- SUPPORTED: "Of the 40 opening-strong signs
  of record, [a] are animal signs under the
  frozen published-identification
  classification (Asset A, SHA-256 [digest]) —
  a share of [s1] against the animal share
  [s2] of the [N] signs with at least 30
  occurrences: enrichment ratio [R1], exact
  test p = [p]. The reversed arm agrees in
  direction (ratio [R2]). The animal half of
  Hunt's opening-sign claim is supported: the
  opening signs are the animal signs, at well
  above the base rate. This does not establish
  that animal signs marked identity, guild, or
  goods — position plus depiction is still not
  meaning."
- NOT SUPPORTED: "Of the 40 opening-strong
  signs of record, [a] are animal signs under
  the frozen classification (Asset A, SHA-256
  [digest]) — a share of [s1] against the
  animal share [s2] of the comparison
  inventory: enrichment ratio [R1], exact
  test p = [p]. Animal signs appear among the
  opening-strong signs at no better than the
  base rate. The animal half of the claim
  `without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_003`
  is not supported; the claim stands on its
  positional half alone, exactly as its record
  is amended to say by the dated append that
  carries this outcome."
- INCONCLUSIVE: "Classified under the frozen
  Asset A (SHA-256 [digest]), the opening-
  strong signs are animal at ratio [R1]
  against the inventory base rate (exact test
  p = [p]; reversed arm ratio [R2]) —
  [the band / disagreement / empty-baseline
  reason, in the words of §4.3]. The test does
  not settle the claim's animal half; the
  claim stands IN QUESTION with this attempt
  on its record, its counts published in
  full."
- ASSET PIN MISMATCH (gate 0.2 closure): "Spec
  049 closed at step 0: the Asset A file
  presented at execution hashes to [observed],
  which is not the digest [frozen] quoted
  verbatim in this spec's freeze record from
  Spec 045's `asset-a-freeze.json`. No join was
  performed and no quantity was computed. The
  claim stands as recorded."
- POPULATION NOT REPRODUCED (gate 0.4
  closure): "Spec 049 closed at step 0: the
  opening-strong population could not be
  pinned as designed — [the enumeration
  returned [n] signs against the recorded 40 /
  the signs that could not be keyed under the
  frozen rule are listed]. No join was
  performed and no quantity was computed. The
  claim stands as recorded."
- INVALID (gates 0.3 / 0.5 closure): "Spec 049
  stopped before any test quantity: [the
  failed gate and observed values]. No verdict
  is recorded; the claim stands as recorded."
- NOT-RUN (dependency closure): "Spec 049 was
  not run: Asset A was never frozen under
  Spec 045 ([Spec 045's closure / state, as
  recorded]), so the classification this test
  consumes does not exist in frozen form. No
  step-0 gate was run. The claim stands as
  recorded."

## 5. Step 0 — gates before any test quantity (fail-closed)

Execution runs these gates in order, before
any §4 quantity is computed. A failure stops
the execution in the class named; nothing is
repaired at run time.

- **0.1 Dependency state.** Spec 045's record
  shows Asset A frozen (`asset-a-freeze.json`
  present in its merged execution record). If
  Spec 045 closed ASSET FAILED or Asset A was
  never frozen, this spec closes **NOT-RUN**
  under the campaign's cluster rule; no
  further gate runs.
- **0.2 Asset A digest assertion.** The
  SHA-256 of the Asset A canonical CSV as
  presented recomputes to the digest this
  spec's freeze record quotes verbatim from
  `asset-a-freeze.json`, and the freeze
  record's per-kind counts match the presented
  file's. A mismatch closes the execution as
  **ASSET PIN MISMATCH** (§4.6) before any
  join.
- **0.3 Input integrity.** Every §3 input
  hashes to its freeze-record value. A
  mismatch stops the run as **INVALID**.
- **0.4 Population enumeration and keying.**
  The opening-strong set is reproduced from
  the pinned records under the reproduction
  rule the freeze fixed, enumerated in full,
  and every enumerated sign is keyed to
  exactly one Asset A row under the keying
  rule the freeze fixed (OPEN item 1). The
  enumerated, keyed list is published as the
  execution's first product. A count other
  than 40, or any sign that cannot be keyed,
  closes the execution as **POPULATION NOT
  REPRODUCED** (§4.6) with the observed list
  published — the population is never quietly
  replaced by a nearby set (not by Phase-45's
  75-sign Holdat set, not by any latent-class
  list: those are different definitions, and
  adjudication §5, item 1 records them as
  such).
- **0.5 Comparison census and coverage.** U
  is enumerated with per-sign occurrence
  counts under the frozen counting rule; the
  unicorn sign(s) of S-B are named from the
  frozen asset's verbatim labels; and every
  sign in O and in U is shown to carry an
  Asset A row. A population sign with no
  Asset A row stops the run as **INVALID** —
  an absent row is never treated as
  non-animal by default. The census (both
  sets, counts, classification tallies
  including contested and unidentified) is
  published with the outcome either way.

## 6. Reporting obligations

Every product of an execution carries, in its
headline paragraph:

1. the claim identifier;
2. the Asset A digest and its per-kind counts;
3. the full counts of §4.2 (every cell of both
   arms, both sets' sizes, the contested and
   unidentified tallies, and the per-sign
   classification table for O and for U);
4. R1, its exact-test p, R2, its p, and the
   headline word of §4.3 or the closure class
   of §9;
5. both sensitivities' ratios and p values
   (or S-B's not-applicable statement);
6. the fence sentence: "This result is about
   depiction and position in recorded data. It
   is not evidence that any sign marked
   identity, a guild, or goods."

Deliverables at execution: a results JSON
(censuses, the keyed population list, both
arms' tables and tests, both sensitivities,
the §5 gate record), a report under these
headline rules, the experiment-graph node
(H15/H23, registered and verified before the
run), the outcome append in this directory,
the dated animal-half append to the claim's
record, and the LEDGER entry (H1). Foundation
check (H21) after the execution phase: 0
failures, or the outcome record says why not.
Anchors asserted byte-identical before and
after.

## 7. Risks and honest weaknesses

- **The population pin is this spec's real
  risk.** The 40 are on record as a count and
  as rates, not as a list, and the battery
  code that produced them is not in the
  repository under Phase-43. Gate 0.4 may
  honestly close this spec unrun; that closure
  is a designed outcome, written in advance,
  not a failure of nerve at run time.
- **Keying may fail even if enumeration
  succeeds.** The pinned crosswalk carries
  only 17 Mahadevan mappings; if the frozen
  keying rule cannot carry the enumerated
  signs into Asset A's identity space, gate
  0.4 closes the spec. The freeze is asked to
  face this directly (OPEN item 1) rather
  than let execution discover it.
- **Forty is a small numerator.** The exact
  test on 40 signs can certify a strong
  enrichment and can certify flatness; a
  middling truth will land INCONCLUSIVE, and
  the design's bands say so in advance.
- **One join, one layer.** The verdict is a
  statement about the published-identification
  layer (§8, limit 2) on one positional
  framework. A different compilation's
  identifications could sort the forty
  differently; the asset's dispute rule is
  the design's answer, and S-A prices it.

## 8. Epistemic limits (binding on all outputs)

1. **No meaning conclusion.** Even a clean
   SUPPORTED shows depiction and position
   coincide; that animal signs marked
   identity, guild, or goods remains Hunt's
   reading, not a measurement of this test.
2. **Depiction is the field's published
   identification, not ground truth.** Asset A
   records what the published lists say a sign
   depicts, with citations. A verdict under
   this spec is a statement about that layer.
3. **The 49% caution travels with the
   result.** Spec 037's census (object-type
   labels diverging in 49% of matched cases
   between compilations) is restated wherever
   this spec's result is stated (§2.4). The
   asset's construction is the answer to it,
   not a refutation of it.
4. **The positional half stands untouched.**
   The 40-sign positional result and the
   claim's partially supported status are
   records of their own test; this spec
   appends an animal-half record beside them
   and edits neither. The frozen outcome of
   Spec 045 is likewise untouched: this spec
   consumes its asset and adjudicates nothing
   of its test.
5. Negative, inconclusive, step-0-closed, and
   not-run outcomes publish with the same
   prominence as a supported one.

## 9. Stop conditions and outcome classes

Execution ends in exactly one of:

- **NOT-RUN** — gate 0.1: Asset A never
  frozen (dependency closure).
- **ASSET PIN MISMATCH** — gate 0.2.
- **POPULATION NOT REPRODUCED** — gate 0.4.
- **INVALID** — gates 0.3 or 0.5.
- **SUPPORTED**, **NOT SUPPORTED**, or
  **INCONCLUSIVE** — per §4.3, after all
  gates pass.

## 10. Execution shape (gated; NOT run by this draft)

1. **Graph-first build** (H15/H23) — script,
   graph node, registration, verification.
2. **Step 0** (§5) — dependency state, asset
   digest assertion, input integrity,
   population enumeration and keying,
   comparison census and coverage.
3. **Primaries** (§4) — the primary arm, the
   reversed arm, both sensitivities.
4. **Outcome** (§6) — appended records only;
   anchors asserted byte-identical;
   foundation check reported as measured.

## 11. What this spec is not

Not a re-run of the positional test (its
result is the premise, not the subject), not
a build or re-derivation of Asset A (that is
Spec 045's, consumed here by digest), not a
test of the celestial half of Hunt's scheme
(that is D-13), not a decipherment, and not
an authorisation to execute. It is the one
join and one exact test the claim's record
has always named as its missing half —
designed so that its honest outcomes,
including closing at its own population gate,
are written down before any sign is joined.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
