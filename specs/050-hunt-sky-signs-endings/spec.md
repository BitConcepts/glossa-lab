# Spec 050 — Hunt: Sky Signs at the Ends of Texts (Design D-13; Consumer of Asset A)

> ## FROZEN — 2026-10-21
>
> Frozen under the runnable-experiments campaign
> plan approved by the owner AS WRITTEN on
> 2026-10-21
> (`~/workspace/your_files/2026-10-21-runnable-experiments-campaign-plan.md`,
> Parts 1–4; decisions E-1…E-7 as written;
> campaign Wave 2). Design D-13 is campaign
> member 10 and a **consumer of Asset A**: the
> depicted-kind classification built and frozen
> inside Spec 045 (design D-05) at its execution
> step 1. This spec does not build, extend, or
> re-derive any classification. Its contract
> anchor is Spec 045's freeze digest
> `5d8254ddc03045b68a0819f870fc9ccc1b9848a58fef3862dae3e4ca21b43f0a`;
> the Asset A byte-digest does not exist at this
> freeze, because the asset is built later, at
> Spec 045's execution step 1 (Wave 3), so no
> byte-digest is stated here. The pin **source**
> is fixed instead: Spec 045's
> `asset-a/asset-a-freeze.json`
> (`specs/045-hunt-depicted-kinds/asset-a/asset-a-freeze.json`),
> which will record the SHA-256 of the canonical
> `asset-a/depicted-kind-classification.csv`.
> Execution asserts that digest at its step 0
> (§3, gate 0.1): a mismatch closes the run as
> **CLOSED AT STEP 0 — ASSET PIN MISMATCH**, and
> an unfrozen or absent asset as **CLOSED AT
> STEP 0 — ASSET NOT FROZEN** — exactly as
> drafted (coordinator pin-timing ruling,
> DD-050-11, `adjudication.md` §7). The freeze
> decisions DD-050-9 to DD-050-15 are recorded
> in `adjudication.md` §7; DD-050-1 to DD-050-6
> are confirmed there as drafted, and DD-050-1
> is frozen there: the celestial class is Asset
> A's `sky_cycle` kind exactly, with the broader
> closing notion stated as an untested boundary
> (§2.2), never silently widened.
>
> Execution runs as **Phase-416** (allocated at
> this freeze, DD-050-10). Nothing in this
> contract has been run, joined, or computed:
> no sign has been classified under this spec,
> no class census has been taken, and no
> final-position quantity exists. Execution
> awaits this freeze merging, the OSF
> registration's approval act, Spec 045's
> execution building and freezing Asset A, and
> a separate execution order.

**Design source:** D-13 in the experiment-design
packet at PR #195
(`docs/research/experiment-designs-2026-10-13/02-roif-and-hunt.md`,
§D-13, read in full at this draft), with the
shared-asset description in that packet's
README and the D-05, D-06, and D-08 designs
read for the framework and asset contracts
they share with this design.

**Claim under test:**
`without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_004`
— Hunt's sky-signs-at-the-endings claim —
standing **UNTESTED**: Phase-104, RULE-CLASS —
the claim's falsifier requires a defined class
of celestial signs, and no such classification
existed in the repository's data; this is the
one part of Hunt's scheme where not even the
positional shadow has been measured.

**AI disclosure:** this draft is produced by an
AI agent (Muse Spark, via Muse) at the
direction of Tristen Pierson, per constitution
§VI.

---

## 1. The claim and the record it stands on

Hunt's three-part account of inscription
structure assigns the closing part to cycles
and calendars. Two of its positional parts have
designs of their own in this campaign: the
pattern as a whole (D-05, Spec 045) and the
opening signs (D-06). This spec is the third:
the endings.

No positional measurement of this claim exists
on the record. Phase-104 could not state its
test, because the claim's own falsifier turns
on a class — "celestial signs" — that no
in-hand classification defined. The campaign's
answer to that gap is not a classification
built inside this spec: it is Asset A, the
depicted-kind classification built once inside
Spec 045 from held published sources, entered
blind to positional results, and frozen before
any join (campaign Part 3, decision E-6). This
spec takes its celestial class from that asset
and from nowhere else (§2).

### 1.1 The question, in plain words

Hunt's closing part should be sky signs — sun,
star, moon — standing for cycles and calendars.
Which signs are sky signs is a visual judgement;
the published sign lists make it, and Asset A
records those judgements sign by sign. With
that class defined and frozen, does it actually
gather at the ends of inscriptions?

### 1.2 The falsifier, first

**Falsifier.** Celestial-class signs are not
enriched at text endings. Operationally, in
the design's own terms: the hypothesis fails
if the celestial class's final-position rate
is at or below the corpus-wide final-position
rate for signs of comparable frequency — the
test the claim's falsifier states (terminal
enrichment for the class).

Everything below is written so that this
falsifier can fire: the class is fixed by a
frozen external asset before any counting
(§2), the ending and enrichment measures are
defined before any counting (§4), the step-0
gates run before any final-position quantity
exists (§3), and every outcome — including the
falsifier's own word, NOT SUPPORTED — is
pre-written in §5.2 before any result can be
known.

### 1.3 The hypothesis

**Hypothesis.** Signs in the celestial class
are enriched in text-final position relative
to their overall frequency — stated precisely
in §4.3: the pooled final-position rate of the
celestial class exceeds the pooled
final-position rate of a frequency-matched
comparison class by a ratio of at least 1.5,
at the 5% level, with at least half the
class's occurrences coming from signs
individually above the corpus-wide final rate.

## 2. Asset A consumption — the celestial class (the pin this spec carries)

This spec **consumes** Asset A; it does not
build, extend, or re-derive any classification.
The contract it consumes is Spec 045's §2, as
frozen on `main` (Spec 045 freeze digest
`5d8254ddc03045b68a0819f870fc9ccc1b9848a58fef3862dae3e4ca21b43f0a`;
DD-050-11).

### 2.1 The class, exactly

- The **celestial class** under this spec is
  exactly the set of signs whose Asset A row
  carries `depicted_kind = sky_cycle`, keyed by
  the asset's primary key: the pinned crosswalk
  identity (`sign_key` in
  `data/crosswalks/sign_crosswalk_master.csv`,
  pinned in §6), one row per sign.
- Each member's standing in the class rests on
  the fields Spec 045 §2.2 fixes per row: the
  verbatim published label
  (`depicted_label_verbatim`), its citations
  (`source_citations`), the governing source
  under Spec 045 §2.3 (the CISI volumes govern;
  Parpola's published identifications govern
  where CISI is silent), the `agreement` value,
  and the `dispute_status`. Spec 045 §2.2's
  kinds are `animal`, `sky_cycle`,
  `object_goods`, `human`, `other`, plus the
  bookkeeping values `contested` and
  `unidentified`; only `sky_cycle` is a member
  of this spec's class.
- **Contested signs are excluded from the
  primary.** A sign recorded
  `depicted_kind = contested` (or
  `dispute_status = contested`) is not a
  celestial sign in the primary test, whatever
  either of its published labels says. Contested
  signs enter only in the pre-registered
  sensitivity of §4.5, under the rule stated
  there. `unidentified` signs are never
  celestial; they belong to the comparison
  population only as §4.2 states, and are
  counted and reported, never dropped silently.

### 2.2 The boundary this draft does not cross

Spec 045's adjudication left two things open
for its own freeze: a "jurisdiction" coding
question (Hunt's closing part also names
jurisdiction signs, for which Asset A has no
depicted kind — Spec 045 §5.2(b) codes that
subset at entry from verbatim labels), and the
narrower alternative of restricting its
closing test to `sky_cycle` alone.

**This spec takes the narrower reading, and
states it as a boundary, not as a silent
choice.** Design D-13's celestial notion is
the sky: signs the published identifications
describe as sun, star, moon, or celestial
bodies. That notion is Asset A's `sky_cycle`
kind as Spec 045 §2.2 defines it. This spec
does **not** widen the class to any
jurisdiction-coded subset, to any sign whose
verbatim label a reader might call celestial
while its Asset A kind is `object_goods`,
`human`, or `other`, or to any sign classified
by a worker's own visual judgement. If Hunt's
closing part is broader than the sky — if it
also carries jurisdiction signs — that broader
claim is **not tested here**; it is the
subject of Spec 045's closing comparison, not
of this spec. A verdict under this spec is a
verdict about `sky_cycle` signs at endings,
and its wording says so (§5.2, §7).

### 2.3 The digest pin

- Asset A is frozen inside Spec 045's
  execution, in `asset-a/asset-a-freeze.json`
  in Spec 045's directory, recording the
  SHA-256 of the canonical
  `asset-a/depicted-kind-classification.csv`,
  its row count and per-kind counts, its input
  pins, and its freeze date (Spec 045 §2.7).
- **No Asset A digest exists at this freeze**
  (the asset is built at Spec 045's execution
  step 1, Wave 3), and none is asserted here.
  This freeze quotes **Spec 045's freeze digest**
  `5d8254ddc03045b68a0819f870fc9ccc1b9848a58fef3862dae3e4ca21b43f0a`
  as the contract anchor, and fixes the pin
  **source** as Spec 045's
  `asset-a/asset-a-freeze.json` (coordinator
  pin-timing ruling, DD-050-11). At execution,
  the digest is read from that source — copied,
  not recomputed into a new value, not
  paraphrased, not shortened beyond the full
  digest.
- Step 0 (§3, gate 0.1) recomputes the digest
  from the canonical CSV as presented at
  execution and asserts equality with the
  value recorded in the fixed pin source
  **before any join and before any counting**. A mismatch is a pre-written
  step-0 closure (§5.2), not a repair
  opportunity: nobody re-derives "the same"
  classification inside this spec (campaign
  requirement R-2).

## 3. Step 0 — gates before any final-position quantity (fail-closed)

Execution runs these gates in order, before
any final-position count, rate, or test is
computed. A failure stops the execution in the
class named; nothing is repaired at run time,
and no gate is skipped because its result
looks predictable.

- **0.1 Asset A digest assertion.** Asset A is
  frozen (Spec 045's execution record and
  `asset-a-freeze.json` are on record), the
  SHA-256 recorded in that fixed pin source
  (§2.3; DD-050-11) is read at step 0, and the
  recomputed SHA-256 of the canonical CSV
  equals the recorded value.
  - Asset A not frozen or not on record →
    **CLOSED AT STEP 0 — ASSET NOT FROZEN**:
    a dependency closure, not a verdict; the
    claim stands UNTESTED as recorded.
  - Digest mismatch → **CLOSED AT STEP 0 —
    ASSET PIN MISMATCH**: the asset presented
    is not the asset Spec 045 froze; no join
    is made and no quantity is computed.
- **0.2 Input integrity.** Every §6 input
  hashes to its freeze-record value. A mismatch
  stops the run as **INVALID**.
- **0.3 Coverage and join completeness.** Every
  sign occurring in the pinned corpus carries
  exactly one Asset A row, and every `sky_cycle`
  row's `sign_key` resolves in the pinned
  crosswalk. A corpus sign with no Asset A row
  stops the run as **INVALID** — an absent row
  is never treated as non-celestial by default,
  because that default would silently define
  the comparison class. (Spec 045's gate A3
  asserts coverage for its own test population;
  this gate asserts the coverage this spec's
  class-level test actually consumes, at the
  resolution it consumes it.)
- **0.4 Class census (totals only).** The
  census enumerates and publishes, before any
  positional quantity: the celestial class's
  member signs (each with its Asset A verbatim
  label, citations, agreement, and dispute
  status), each member's **total** occurrence
  count in the pinned corpus, the class's total
  occurrences, and the §4.2 comparison class's
  member signs and total occurrences. Totals
  are not positional quantities; no final count
  is taken at this gate.
  - Celestial class total occurrences below
    **30** → the execution closes here as
    **TOO THIN** (§4.3): the class itself is
    the finding, stated plainly, and no
    final-position rate is computed.
  - Comparison class total occurrences below
    **30** → **TOO THIN**, on the same terms
    (DD-050-3).
- **0.5 Positional reproduction.** The pinned
  positional record's quantities are reproduced
  from the pinned corpus under the recorded
  framework — the 805 / 2,267 formula count and
  the 40 / 61 / 20 initial- / medial- /
  terminal-strong classes of
  `hunt_tripartite_test.json` (§6). A mismatch
  stops the run as **INVALID**: the endings
  test does not proceed on a framework that
  cannot first reproduce its own recorded
  result.
- **0.6 Freeze-order proof.** The record shows,
  in order: this spec froze, quoting Spec 045's
  freeze digest as its contract anchor and
  fixing the pin source (§2.3; DD-050-11);
  Asset A froze (its freeze date in
  `asset-a-freeze.json`); and no join of Asset
  A to the corpus under this spec precedes
  either. Absent that proof
  → **INVALID**: a class joined before it was
  pinned is not a frozen class.

## 4. Definitions and the primary test

### 4.1 Ending (text-final position), pinned

- A sign occurrence is in **text-final
  position** when it is the last sign of its
  inscription's recorded sequence in the pinned
  corpus, as counted by the pinned positional
  framework (§6). "The ends of texts" in the
  design is this position and no other: not the
  closing part of the tripartite formula, not
  the terminal-strong sign class, and not a
  suffix-like behaviour score — those are other
  designs' objects (D-05, D-08), named here so
  they cannot be conflated with this test.
- This spec introduces **no** new inscription-
  length floor, segmentation rule, sign
  ordering, or re-typing. Any length or
  segmentation convention the pinned framework
  itself applies is part of that framework,
  is restated in the gate-0.5 reproduction
  record, and applies identically to the
  celestial and comparison classes.
- A sign's **final-position rate** is its
  final-position occurrences divided by its
  total occurrences in the pinned corpus. A
  class's **pooled final-position rate** is
  the class's pooled final-position
  occurrences divided by its pooled total
  occurrences (occurrences pooled, not
  per-sign rates averaged — so a frequent sign
  carries its true weight, and §4.4's per-sign
  reporting exists precisely so that weight is
  visible).

### 4.2 The comparison class, pinned

- The **comparison class** is the set of signs
  that are (a) not celestial in the primary
  (their Asset A kind is not `sky_cycle`, and
  they are not `contested`), and (b) of
  **comparable frequency**: their total
  occurrence count in the pinned corpus lies
  between the smallest and the largest total
  occurrence count among the primary celestial
  members, inclusive (DD-050-2). `unidentified`
  signs inside the band are members of the
  comparison class and are counted and flagged
  as such in the census; they are never
  celestial.
- The **corpus-wide final-position rate** —
  pooled final-position occurrences of all
  signs in the pinned corpus divided by all
  occurrences — is computed and published as
  descriptive context, and is the rate the
  per-sign condition of §4.3 uses (the design
  states that condition against the corpus
  rate). It is not the primary denominator:
  the design's method paragraph fixes the
  primary comparison as the frequency-matched
  class, and the adjudication (§3 of
  `adjudication.md`) records why the two
  phrasings are not interchanged.

### 4.3 Enrichment, pinned (the criteria)

Let R_sky be the celestial class's pooled
final-position rate and R_cmp the comparison
class's pooled final-position rate. The
**enrichment ratio** is R_sky / R_cmp.
Significance is by **Fisher's exact test**
(two-sided, DD-050-4) on the pooled 2×2 table
(celestial / comparison × final / non-final
occurrences), at the **5% level**.

- **SUPPORTED** — enrichment ratio at least
  **1.5**, the exact test at the 5% level, **and**
  at least half the celestial class's total
  occurrences come from member signs whose
  individual final-position rates are above
  the corpus-wide final-position rate.
- **NOT SUPPORTED** — enrichment ratio at or
  below **1.0**. This is the falsifier's word:
  the class is not enriched at endings, at the
  rate signs of comparable frequency show.
- **INCONCLUSIVE** — anything else: a ratio
  between 1.0 and 1.5; or a ratio at or above
  1.5 that fails the exact test; or a ratio at
  or above 1.5 with the test passed but the
  half-of-occurrences condition failed.
- **TOO THIN** — the §3 gate-0.4 closure:
  the celestial class, or the comparison
  class, totals fewer than 30 occurrences.
  TOO THIN is the recorded form of
  INCONCLUSIVE for a class too small to test
  (DD-050-3); it is stated with its census and
  no rate.

### 4.4 Per-sign reporting (part of the primary)

Alongside the pooled result, every celestial
member sign is reported in full: its Asset A
verbatim label and citations, its total
occurrences, its final-position occurrences,
its individual final-position rate, and
whether that rate is above the corpus-wide
rate. One frequent sign cannot carry the
class silently: the half-of-occurrences
condition (§4.3) is computed from this table,
and the table is published whichever way the
verdict lands.

### 4.5 Sensitivities (pre-registered, two arms)

Both arms are run and reported beside the
primary with the same prominence; neither
replaces the primary's verdict word.

- **S1 — Borderline removed (the design's
  named sensitivity).** The primary is rerun
  with every celestial member whose Asset A
  `dispute_status = borderline` removed. The
  removed signs are named in the census.
- **S2 — Contested included (Asset A's rule).**
  The primary is rerun with contested signs
  whose **CISI-governed** label (Spec 045
  §§2.5 and 5.3's inclusion rule) is a `sky_cycle`
  identification included in the celestial
  class under that label. Signs whose
  CISI-governed label is not `sky_cycle` do
  not enter. The included signs are named,
  with both of their published labels.

## 5. Outcome classes and pre-written verdict wordings

### 5.1 Outcome classes

Execution ends in exactly one of:

- **SUPPORTED**, **NOT SUPPORTED**, or
  **INCONCLUSIVE** — per §4.3, after all
  gates pass.
- **TOO THIN** — gate 0.4 (§4.3).
- **CLOSED AT STEP 0 — ASSET NOT FROZEN** or
  **CLOSED AT STEP 0 — ASSET PIN MISMATCH** —
  gate 0.1.
- **INVALID** — gate 0.2, 0.3, 0.5, or 0.6.
- **NOT ADJUDICATED** — the §4 primary's
  machinery reconciliation fails (the pooled
  counts do not reconcile exactly with the
  per-sign table of §4.4, or the comparison
  census does not reconcile with the corpus
  census): a machinery finding, not a verdict
  (DD-050-5).

### 5.2 Pre-written verdict wordings

The outcome record's headline paragraph uses
one of these forms, with the bracketed
quantities filled from the run:

- SUPPORTED: "Classified by what they depict —
  from published identifications, entered blind
  and frozen before any join (Asset A, SHA-256
  [digest]) — the sky signs gather at the ends
  of texts: the celestial class's pooled
  final-position rate is [R_sky] on [n]
  occurrences, against [R_cmp] for signs of
  comparable frequency, an enrichment ratio of
  [ratio] with the exact test at [p]; and
  [share] of the class's occurrences come from
  signs individually above the corpus-wide
  final rate of [rate]. The claim
  `without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_004`
  is SUPPORTED in its positional form only:
  sky signs cluster at endings. This does not
  establish that they marked calendars, cycles,
  or any content — position is not meaning."
- NOT SUPPORTED: "Classified by what they
  depict (Asset A, SHA-256 [digest]), the sky
  signs do not gather at the ends of texts:
  the celestial class's pooled final-position
  rate is [R_sky] on [n] occurrences, against
  [R_cmp] for signs of comparable frequency —
  an enrichment ratio of [ratio], at or below
  1.0. Celestial-class signs are not enriched
  at text endings. The claim
  `without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_004`
  is NOT SUPPORTED, and Hunt's scheme stands
  measured at its endings as it has been at
  its openings and its pattern: [the per-sign
  table is published with this wording]."
- INCONCLUSIVE: "Classified by what they
  depict (Asset A, SHA-256 [digest]), the sky
  signs' ending rate falls between the
  design's fixed words: pooled final-position
  rate [R_sky] on [n] occurrences against
  [R_cmp] matched — ratio [ratio], exact test
  [p], half-of-occurrences condition
  [met / not met]. The claim
  `without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_004`
  is INCONCLUSIVE under Spec 050: the attempt
  is on its record, with every count
  published, and the claim is neither
  supported nor falsified by it."
- TOO THIN: "The celestial class as frozen in
  Asset A (SHA-256 [digest]) totals [n]
  occurrences in the pinned corpus [or: the
  frequency-matched comparison class totals
  [n] occurrences] — fewer than the design's
  floor of 30. The class is itself the
  finding: too small to test. No
  final-position rate was computed. The claim
  `without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_004`
  stands UNTESTED in substance, recorded
  INCONCLUSIVE (TOO THIN) under Spec 050,
  with the class census published in full."
- CLOSED AT STEP 0 — ASSET NOT FROZEN: "Spec
  050 closed at step 0: Asset A is not frozen
  on record — Spec 045's `asset-a-freeze.json`
  [does not exist / is not landed] at this
  execution. No join was made and no quantity
  was computed. The claim stands UNTESTED as
  recorded. This is a dependency closure
  under the campaign's cluster rule, not a
  verdict on the claim."
- CLOSED AT STEP 0 — ASSET PIN MISMATCH:
  "Spec 050 closed at step 0: the Asset A
  presented at execution recomputes to
  SHA-256 [observed], which is not the digest
  recorded in Spec 045's `asset-a-freeze.json`
  — the pin source this spec's freeze record
  fixes (DD-050-11) — [recorded]. The asset
  presented is not the
  asset that was frozen. No join was made and
  no quantity was computed. The claim stands
  UNTESTED as recorded."
- INVALID: "Spec 050 stopped at step 0,
  gate [0.#]: [the failed gate and the
  observed values]. No final-position quantity
  was computed and no verdict is recorded; the
  claim stands UNTESTED as recorded."
- NOT ADJUDICATED: "Spec 050's primary ran
  but its machinery reconciliation failed:
  [the unreconciled counts]. No verdict word
  is recorded; the counts are published as a
  machinery finding, not as evidence about
  the claim."

## 6. Inputs (pinned at this draft; re-asserted at this freeze)

| Input | Pin / state |
|---|---|
| Asset A — depicted-kind classification (Spec 045, design D-05) | **Not yet in existence at this freeze.** Consumed only in Spec 045 §2's frozen form: canonical CSV `specs/045-hunt-depicted-kinds/asset-a/depicted-kind-classification.csv` with `specs/045-hunt-depicted-kinds/asset-a/asset-a-freeze.json` recording its SHA-256. Contract anchor: Spec 045's freeze digest `5d8254ddc03045b68a0819f870fc9ccc1b9848a58fef3862dae3e4ca21b43f0a`. Pin source fixed at this freeze: `asset-a-freeze.json` (§2.3; DD-050-11); at execution gate 0.1 reads the digest from that source and asserts it. No Asset A digest is asserted here. |
| Corpus layer of record (`backend/glossa_lab/data/yajnadevam_inscriptions.csv`) — the corpus the positional framework runs on | SHA-256 `c02e3d7bb74cf5abb11cc94f88d8d469e6acc5d6fad4b7153c02c43428f58d98` (recomputed at this draft from `main` at `83b6a563…`; the same value Specs 042's and 045's drafts pin; re-asserted at this spec's freeze). |
| Positional record (`glossa-indus/analysis/positional/hunt_tripartite_test.json`) | SHA-256 `0e546962c1b72b929c87d4ce40c97633e8e3e340737f32f5dd3eae9f04759e48` (recomputed at this draft from `main` at `83b6a563…`): 805 / 2,267 formula inscriptions; 40 / 61 / 20 strong-sign classes. The framework of record for §4.1's final position and gate 0.5's reproduction. |
| Phase-43 battery record (`outputs/phase43_all.json`) | SHA-256 `78a6c21908b9362854c54dd3d820d717be22feab3af11135663fa14aaf554fe4` (recomputed at this draft). The positional framework's battery of record, shared with D-06 / D-08. |
| Sign crosswalk of record (`data/crosswalks/sign_crosswalk_master.csv`) | SHA-256 `4ace1a617f40afe8d0bbb82e5461d98a675296152e7577b04fb67b00f4f5dfcf` (recomputed at this draft). Defines `sign_key`, Asset A's primary key (§2.1). |
| Anchors file (`backend/reports/INDUS_FINAL_ANCHORS.json`) | SHA-256 `df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569` (recomputed at this draft). This spec moves no anchor; the file is asserted byte-identical before and after any execution. |

Every pin in this table was re-asserted at
this freeze against `main` at `e3399961…` by
two routes (contents API and git-data blob
API), agreeing byte-for-byte. The censuses
were recomputed at the freeze: the crosswalk
carries 205 rows with 187 distinct
`registry_sign_id` values; the corpus layer
carries 5,679 rows; the anchors file carries
287 anchors.

## 7. Epistemic limits (binding on all outputs)

1. **Position is not meaning.** Even a clean
   SUPPORTED shows sky signs cluster at
   endings. It does not establish scheduling,
   ritual calendars, cycle content, or any
   reading of any sign. The verdict wordings
   of §5.2 carry this sentence in substance,
   and no output may drop it.
2. **The class is the sky only.** Per §2.2, no
   jurisdiction-coded or otherwise
   celestial-adjacent sign outside Asset A's
   `sky_cycle` kind is tested. A verdict here
   neither supports nor falsifies Hunt's
   closing part in any broader form.
3. **Depiction is the published-identification
   layer, not ground truth.** Asset A records
   what the published lists say a sign depicts,
   with citations. A verdict under this spec is
   a statement about that layer, on this
   corpus.
4. **The 49% caution travels with the asset.**
   Spec 037's census found object-*type* labels
   diverging between the CISI volumes and the
   programme's corpus in 49% of matched cases.
   Asset A classifies signs by what they
   depict, not objects by type, and its
   construction (held published sources only,
   blind entry, dispute by rule, freeze before
   join) is the design's answer to that
   caution — restated wherever Asset A or a
   verdict under this spec is stated, never
   presented as a refutation of the census.
5. **One corpus layer.** Every rate is a rate
   in the pinned corpus layer of §6, under its
   recorded lineage posture. Nothing here is a
   statement about any other compilation's
   numbering or counts; a cross-compilation
   arm is not part of design D-13 and is not
   added here.
6. **Contested signs are a stated exclusion.**
   The primary's class is the uncontested
   `sky_cycle` set. What contested signs would
   do to the result is answered only by
   sensitivity S2 (§4.5), reported beside the
   primary, never folded into it.
7. Negative, inconclusive, too-thin, closed,
   invalid, and not-adjudicated outcomes
   publish with the same prominence as a
   supported one.

## 8. Controls and named confounders

- **Classification discretion — the whole
  ballgame, in the design's words.** Controlled
  by construction, and only by construction:
  the class comes from a frozen external asset
  built from published sources, blind, with a
  per-sign citation (§2); the sensitivities of
  §4.5 name the borderline and contested
  margins explicitly. No sign's membership is
  decided inside this spec.
- **Frequency confounding.** Sky signs may be
  rare or common as a class; final-position
  rates move with frequency. Controlled by the
  frequency-matched comparison class (§4.2)
  and by publishing the corpus-wide rate beside
  it, so the matching itself is inspectable.
- **One frequent sign carrying the class.**
  Controlled by the half-of-occurrences
  condition (§4.3) and the full per-sign table
  (§4.4).
- **Excavation and corpus composition.** The
  pinned corpus is one compilation's surviving
  record; site and object mix are described in
  the outcome record for the celestial and
  comparison occurrences, never adjusted away
  silently. This spec does not stratify by site
  or object type: design D-13 registers a
  class-level test, and adding strata would
  change its estimand.
- **Segmentation dependence.** Final position
  is defined on recorded sequences (§4.1); a
  differently segmented corpus could give a
  different answer, which is limit 5 stated
  from the other side. The reproduction gate
  (0.5) binds this run to the recorded
  framework's conventions exactly.

## 9. Reporting obligations

Every product of an execution carries, in its
headline paragraph: the claim identifier; the
Asset A digest as recorded in the fixed pin
source (`asset-a-freeze.json`) and asserted at
gate 0.1, and the celestial class's census (member
signs, total occurrences); the pooled rates
R_sky and R_cmp, the enrichment ratio, the
exact test's result, and the
half-of-occurrences share; the verdict word of
§5.1 or the closure class; and limit 1 of §7
in plain words.

Deliverables at execution: a results JSON
(gate record, censuses, the pooled 2×2 table,
per-sign table, both sensitivity arms' full
quantities, control / reconciliation outcomes);
a report under these headline rules; the
experiment-graph node (H15/H23, registered and
verified before the run); the outcome append in
this directory; and the LEDGER entry (H1).
Foundation check (H21) after the execution
phase: 0 failures, or the outcome record says
why not. Anchors asserted byte-identical
before and after.

## 10. Execution shape (gated; NOT run by this draft)

1. **Graph-first build** (H15/H23) — script,
   graph node, registration, verification.
2. **Step 0** (§3) — Asset A digest assertion,
   input integrity, coverage, class census
   (TOO THIN closes here), positional
   reproduction, freeze-order proof.
3. **Primary** (§4) — pooled test, per-sign
   table, both sensitivity arms,
   reconciliation.
4. **Outcome** (§9) — appended records only;
   anchors asserted byte-identical; foundation
   check reported as measured.

## 11. What this spec is not

Not a classification build (Asset A is Spec
045's; this spec re-derives nothing), not a
test of Hunt's closing part in any form
broader than the sky (§2.2), not a rerun of
the tripartite pattern test or of D-08's
closing-sign battery, not a decipherment, and
not an authorisation to execute. It is the
terminal-enrichment test the claim's own
falsifier states, written so that its honest
outcomes — including closing at its own first
gate because its asset is absent or mis-pinned
— are written down before any sign is counted.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
