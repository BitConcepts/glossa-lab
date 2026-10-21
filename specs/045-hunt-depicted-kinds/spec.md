# Spec 045 — Hunt's Three Parts: Pattern, or Meanings? (Design D-05; Builder of Asset A)

> ## FROZEN — 2026-10-21
>
> Frozen under the runnable-experiments campaign
> plan approved by the owner AS WRITTEN on
> 2026-10-21
> (`~/workspace/your_files/2026-10-21-runnable-experiments-campaign-plan.md`,
> Parts 1–4; decisions E-1…E-7 as written;
> campaign Wave 2). The freeze decisions are
> recorded in `adjudication.md` §7 (DD-045-9 to
> DD-045-21), including the three mandated
> pre-digest repairs: the D-18 consumption
> repair (DD-045-17, answering Spec 046's
> DD-046-14), the coverage restatement
> (DD-045-18), and the closing-measure
> disambiguation (DD-045-19). The AEE lifecycle
> hooks passed at the freeze gate over the
> recovered register 0.7-draft
> (`aee/freeze-aee-note.md`), and the freeze
> digest is in `freeze.json`. This spec's own
> OSF contract registration was filed at this
> freeze under campaign decision E-1
> (DD-045-20; `osf-spec-registration.md`);
> execution awaits that registration's approval
> and the campaign's execution pass.
> **Execution is a separate later act.**
> Nothing in this spec has been built, joined,
> or computed — in particular, **Asset A does
> not exist yet**: this spec defines its
> contract, and Asset A is BUILT at execution
> step 1, not at this freeze.
>
> The execution phase number is **Phase-411**,
> allocated at this freeze (DD-045-10,
> resolving DD-045-8).

**Design source:** D-05 in the experiment-design
packet at PR #195
(`docs/research/experiment-designs-2026-10-13/02-roif-and-hunt.md`,
§D-05, read in full at this draft), with the
shared-asset description in that packet's
README and the D-06, D-13, and D-18 designs
read for the contracts they consume or feed.

**Claim under test:**
`without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_001`
— Hunt's three-part account of inscription
structure — standing **IN QUESTION**: partially
supported for position only.

**AI disclosure:** this draft is produced by an
AI agent (Muse Spark, via Muse) at the
direction of Tristen Pierson, per constitution
§VI.

---

## 1. The claim and the record it stands on

The recorded positional result
(`glossa-indus/analysis/positional/hunt_tripartite_test.json`,
SHA-256 `0e546962…`, recomputed at this draft
from `main` at `83b6a563…`) is:

- 805 of 2,267 inscriptions of length ≥ 3 follow
  the opening–middle–ending structure: a formula
  rate of **0.355** against a null expectation of
  **0.006** (lift 59.09).
- The positional classes of record are 40
  initial-strong signs, 61 medial-strong signs,
  and 20 terminal-strong signs; the initial
  signs' mean initial rate is 0.757 against
  0.251 expected by chance.
- The test's own verdict, verbatim in substance:
  the structural pattern **exists**, and it is
  "consistent with BOTH Hunt model and Dravidian
  suffix model. Cannot distinguish between them
  without visual sign classification."

That last sentence is this spec. The pattern is
settled; what has never been tested is Hunt's
account *of* the pattern — that the three parts
carry different kinds of content — against the
rival grammar account, under which position is
driven by a sign's role in the sequence (above
all, word-ending behaviour in the closing part),
whatever the sign depicts.

### 1.1 The question, in plain words

Inscriptions fall into a three-part pattern.
Hunt says the parts *mean* different things:
identity and goods first, action in the middle,
cycles and jurisdiction last. The rival says the
pattern is just grammar — the closing part, in
particular, is where word endings sit. The two
accounts can be told apart if the signs are
classified by what they **depict**: Hunt's
account predicts the depicted kinds sort into
the parts; the grammar account predicts a sign's
sequence behaviour, not its picture, decides
where it sits.

### 1.2 The hypothesis and its falsifier

**Hypothesis.** Under a classification of signs
by depicted kind, taken from published sign
lists and frozen in advance (Asset A, §2), the
signs Hunt's model assigns to each part are
enriched in that part beyond what position
behaviour alone predicts — and the closing
part's membership is better predicted by
depicted kind (cycle/sky and jurisdiction
signs) than by word-ending behaviour.

**Falsifier (the task's one line, expanded only
as the design expands it).** The depicted kinds
fail to pattern positionally the way meanings
require. Operationally, the hypothesis fails
if **either**:

- depicted kind adds no predictive power over
  position behaviour alone (model PH does not
  beat model P by the frozen fit margin, §5), or
- the closing part is predicted as well or
  better by word-ending behaviour than by
  depicted kind (§5.2).

## 2. Asset A — the depicted-kind sign classification (the contract)

Asset A is built **once**, inside this spec
(campaign decision E-6), and consumed —
digest-pinned — by this spec's own test and by
Specs for D-06 (the animal half of the opening
signs) and D-13 (the celestial class at text
endings). This section is the contract those
drafts are written against. Any change to it
after this draft is a freeze-visible change,
recorded in `adjudication.md`, never a silent
edit.

### 2.1 Form and location

- One row per sign, in a single canonical file
  `asset-a/depicted-kind-classification.csv`
  in this spec's directory, with a machine
  record `asset-a/asset-a-freeze.json` carrying
  the freeze digest, the build record, and the
  input pins (§2.7). The CSV is generated with
  a CSV writer and round-trip validated (every
  row parses to exactly the field count of
  §2.2) before freezing — hand-edited CSV is
  not an asset.
- **Coverage scope (freeze restatement,
  DD-045-18).** "One row per sign" covers the
  **full pinned-crosswalk sign universe**:
  every distinct `registry_sign_id` in
  `data/crosswalks/sign_crosswalk_master.csv`
  as pinned in §4 — 205 crosswalk rows
  carrying **187 distinct sign keys** at the
  freeze census (recomputed at the freeze).
  This spec's §4 test population is a subset
  of that universe. Gate A3 is restated to
  this scope in §3, so the corpus-wide
  coverage consumer Spec 050 asserts at its
  own gate 0.3 rests on this scope, on the
  record.
- The sign key is the program's crosswalk
  identity: `sign_key` is the sign's identifier
  in `data/crosswalks/sign_crosswalk_master.csv`
  (pinned, §4), and each row also carries the
  CISI and Parpola numbers where the crosswalk
  records them, so a consumer never has to
  re-derive which drawn sign a row is about.

### 2.2 Classification fields (one row per sign)

| Field | Content |
|---|---|
| `sign_key` | Crosswalk identity of the sign (above). Unique; the asset's primary key. |
| `cisi_no`, `parpola_no` | The sign's numbers in each list, as recorded in the pinned crosswalk; empty only with `crosswalk_status` stating why. |
| `depicted_kind` | Exactly one of: `animal`, `sky_cycle`, `object_goods`, `human`, `other`, `contested`, `unidentified`. The first five are the design's kinds (animal; sky/cycle; object/goods; human; other). `contested` and `unidentified` are bookkeeping values, never silently pooled into a kind (§2.5, §3). |
| `depicted_label_verbatim` | The words the governing source itself uses for what the sign depicts (e.g. its published identification), copied, not paraphrased. |
| `governing_source` | The source that governs the label under the hierarchy of §2.3 (a citation key from §2.3). |
| `source_citations` | Every source consulted for this sign, each as volume/list + page or entry, with its own verbatim label where it gives one. No row exists without at least one citation, except an `unidentified` row, which instead records the sources searched. |
| `agreement` | `agree` (two or more independent published sources give the same depicted kind), `single_source` (only one published source identifies the sign), `disagree` (sources give different kinds), or `silent` (a consulted source does not identify the sign; recorded per source in `source_citations`). |
| `dispute_status` | `none`, `contested` (mirrors `agreement = disagree` or a D-18 CONTESTED input, §2.6), or `borderline` (the enterer's recorded note that the published identification is hedged in its own source). |
| `d18_input` | The D-18 concordance outcome consumed for this sign (§2.6), or `none`. |
| `entered_blind` | `yes` for every row: the attestation of §2.4, per build, not per row by exception. |

No other fields. A consumer needing more opens
its own planning gate; it does not extend the
asset inside this campaign.

### 2.3 Source hierarchy (fixed in advance)

Labels come **only** from held published
sources, in this order of governing authority:

1. **The CISI volumes** (Corpus of Indus Seals
   and Inscriptions, Vol. 1 and Vol. 2, held
   digitally and complete) — the field's
   catalogue of record for what a sign depicts.
2. **Parpola's published sign identifications**
   — governing where CISI is silent on a sign.
3. **A D-18 concordance input** (§2.6) — never
   governing on its own; it can corroborate
   (raising `agreement`) or contest (forcing
   `dispute_status = contested`), because its
   own sources are the lists above plus
   Mahadevan's and Wells's lists, which enter
   Asset A **only** through a D-18 row, cited
   there.

Where CISI and Parpola both identify a sign and
agree, the row is `agree` and CISI governs the
verbatim label. Where they disagree, neither
governs by rank: the row is `contested` (§2.5).
Program-internal classifications, earlier phase
outputs, and any worker's own visual judgement
are **not sources** and may not appear in
`source_citations`.

### 2.4 The blind-entry rule

- Entry is done **blind to positional
  results**: the enterer works from the source
  volumes and the sign inventory only, and does
  not see — and the build record must show they
  were not given — the part-membership classes
  (initial/medial/terminal-strong sets), any
  inscription's part assignment, or any output
  of the §5 models.
- The build runs in this order, and the order
  is itself a gate (§3): sources consulted →
  rows entered → dispute coding completed →
  D-18 input incorporated or its absence
  recorded → freeze digest computed → **only
  then** any join to corpus or positional data.
- A breach of blind entry, discovered at any
  point, is an asset failure (§3, gate A5): the
  asset is not repaired inside the campaign;
  this spec and its Asset A dependents close
  as not-run under the campaign's cluster rule.

### 2.5 The dispute rule

- A sign whose governing sources disagree on
  depicted kind is `depicted_kind = contested`,
  `dispute_status = contested`, with **both**
  verbatim labels and citations recorded. No
  tie is broken by the enterer, by frequency,
  or by which label would suit any test.
- Contested signs are **excluded from the
  primary** (§5) and **included, under the
  CISI-governed label, in one pre-registered
  sensitivity** (§5.3) — so their exclusion can
  never be the quiet reason a result lands as
  it does.
- `borderline` signs stay in the primary under
  their governing label and are removed in the
  same sensitivity's second arm (§5.3).
- Disputes are coded **before** the freeze and
  before any join; a dispute first noticed
  after the freeze is recorded as an asset
  defect, not resolved into the frozen asset.

### 2.6 What Asset A accepts from D-18 (Spec 046)

D-18's concordance output feeds Asset A; it
never writes into it. Asset A accepts exactly
one input form from D-18, in the form Spec
046 froze (its §6 delivery form, read in full
at this freeze; the repair of this section is
DD-045-17, answering Spec 046's DD-046-14 —
Spec 046's vocabulary is consumed as frozen
and is not changed here):

- **The concordance file** `concordance-297.json`
  (schema `glossa.concordance/1`), pinned by
  its own SHA-256 digest in
  `asset-a-freeze.json` at Asset A's freeze,
  and **produced on every terminal outcome**
  of Spec 046. Each sign record in it carries:
  `target_sign` (including
  `crosswalk_registry_id`, a string or null,
  `drawn_sign_match_basis` —
  `crosswalk-registry` or `wells-list-entry` —
  and `drawn_sign_ref`); exactly four list
  rows (CISI, Parpola, Mahadevan, Wells), each
  with its verdict `AGREE`, `DISAGREE`, or
  `SILENT` and its verbatim identification
  quoted for every non-SILENT verdict; the
  per-sign `concurrence_state`, one of
  Spec 046's total outcome set — `CONSENSUS`,
  `PARTIAL CONCURRENCE`, `SINGLE-SOURCE`, or
  `CONTESTED`; and the `asset_a_feed` block
  (depicted kind, specific identification,
  concurrence state, disputed flag, and any
  disputed identifications).
- Consumption rules, by concurrence state:
  a `CONSENSUS` sign record adds its cited
  lists as corroborating entries in
  `source_citations` (it may raise
  `agreement`; it never overrides a CISI or
  Parpola label already entered). A
  **`PARTIAL CONCURRENCE`** sign record is
  consumed the same way, with its state
  recorded verbatim in `d18_input`: it counts
  as exactly the one independent corroboration
  it carries (one independent list scored
  AGREE, none DISAGREE), it may raise
  `agreement` only to that extent, and no
  record may present it as consensus. A
  `SINGLE-SOURCE` record is consumed as
  corroboration of the same kind, carrying
  its single source. A `CONTESTED` record
  forces `dispute_status = contested`, and
  its verbatim identifications travel in the
  feed's `disputed_identifications` — the
  asset records the dispute and never picks
  a side.
- Closure deliveries: an `IDENTIFICATION
  FAILED` closure contributes no sign record
  and is recorded as such in the build
  record. A **`CLOSED AT STEP 0`** outcome is
  an acceptable D-18 terminal delivery
  satisfying the timing rule below: its
  delivery is the same concordance file with
  `signs` an empty array and a top-level
  `closure` block `{class, wording}`. An
  empty feed is a stated state, never an
  absent file; Asset A proceeds without this
  feed and records its absence, and may not
  reconstruct the feed from its own labels.
- Unresolved-key disposition: a sign record
  whose `crosswalk_registry_id` is **null**
  (Spec 046 lawfully produces a sign matched
  by Wells-list entry, with
  `drawn_sign_match_basis` =
  `wells-list-entry`), or whose registry id
  does not resolve in Asset A's pinned
  crosswalk, is **not rejected**. It is
  accepted and recorded in the build record
  under its Wells-list-entry reference
  (`drawn_sign_ref` plus the source sign
  number); it creates no crosswalk key and is
  never re-keyed by hand. Its `asset_a_feed`
  attaches to an Asset A row only where blind
  entry independently entered that same drawn
  sign under a crosswalk key and the build
  record states that linkage explicitly; if
  no such row exists, the feed stands in the
  build record as an **unattached D-18
  input**, named as such, and neither gate A2
  nor gate A3 fails on it.
- Timing rule: Asset A freezes only when
  **either** D-18's concordance file is landed
  and pinned (in any terminal state, including
  a closure file) **or** D-18's closure record
  is on record (campaign Part 4, Wave 3 group
  1: D-18 lands before Asset A freezes). Asset
  A does not wait indefinitely and does not
  proceed on an unpinned or partial D-18
  output.

### 2.7 Freeze point and digest pinning

- **Freeze point:** the moment the §3 build
  gates A1–A5 all pass — entry complete,
  disputes coded, D-18 input resolved under
  §2.6, blind-entry record complete — and
  **before any join** of the classification to
  the corpus or to any positional result.
- At the freeze point, `asset-a-freeze.json`
  records: the SHA-256 of the canonical CSV;
  the row count and the per-kind counts; the
  pins of every input (§4, plus the D-18 file
  digest or the D-18 closure reference); the
  build order attestation; and the freeze date.
- **The D-18 producing contract, as pinned
  here (DD-045-21):** Spec 046 stands frozen
  on 2026-10-21. Its record, as its
  `osf-spec-registration.md` presents it,
  carries **two** digests: the freeze-act
  digest
  `80c3be31e5af5236f71cb2c1894b2946f9b8ad47b12bdeab9d03cd76468af405`
  (the digest in the OSF registration filed at
  Spec 046's freeze, https://osf.io/dnts8/)
  and its successor digest
  `e0d7add84b9d28ae5f6a6b392dca578b727ad4d99a117360a57d39f3b94b01c6`
  (the value in Spec 046's `freeze.json` as
  merged, after the pre-merge freeze-test
  correction its record describes). Both are
  quoted here, as Spec 046's record presents
  them; neither is Asset A's input pin. The
  input pin is the concordance file's own
  SHA-256, recorded at Asset A's freeze under
  §2.6.
- **Dependents pin the digest, not the idea:**
  the freeze records of D-06's and D-13's specs
  must quote Asset A's SHA-256 verbatim, and
  their executions compare it before any join.
  A mismatch closes the dependent as not-run
  (campaign cluster rule); nobody re-derives
  "the same" classification.
- After the freeze point the asset changes
  only by dated, append-only record entries
  that the freeze itself permits (a defect
  notice), never by editing a row. A defect
  that reaches a produced verdict marks that
  verdict; it does not rewrite it.

## 3. Asset A build gates (fail-closed; before any join)

Execution of this spec runs these gates in
order. A failure stops the build in the class
named; nothing is repaired at run time, and no
§5 quantity is computed past a failed gate.

- **A1 — Source availability.** The CISI
  volumes and Parpola's published
  identifications named in §2.3 are in hand and
  identified by edition in the build record.
  Missing → **ASSET FAILED**.
- **A2 — D-18 input resolved.** Either the
  D-18 concordance file is landed and pinned
  (in any terminal state, including a
  `CLOSED AT STEP 0` or IDENTIFICATION FAILED
  closure file under §2.6), or D-18's closure
  record is on record (§2.6).
  Neither → the build does not start; this is a
  sequencing stop, recorded, not a verdict.
- **A3 — Coverage completeness (scope
  restated at this freeze, DD-045-18).** Every
  sign in the **full pinned-crosswalk sign
  universe** (§2.1: every distinct
  `registry_sign_id` in the pinned crosswalk —
  187 distinct sign keys at the freeze census)
  carries a row in the asset — a kind,
  `contested`, or `unidentified` with its
  searched sources recorded. The §4 test
  population is a subset of that universe and
  is covered by the same rule. A sign with no
  row stops the build as **ASSET
  FAILED**: an absent row is never treated as
  `other` by default.
- **A4 — Citation completeness.** Every
  non-`unidentified` row carries at least one
  §2.3 citation with a verbatim label; every
  row carries an `agreement` value. A row
  failing either stops the build as **ASSET
  FAILED**.
- **A5 — Blind entry and order.** The build
  record attests the §2.4 order and blindness,
  with the entry log preserved. A breach or a
  missing attestation stops the build as
  **ASSET FAILED** and fires the campaign's
  cluster rule for D-06 and D-13.
- **A6 — Freeze recorded.** `asset-a-freeze.json`
  exists with the §2.7 contents and its digest
  recomputes from the canonical CSV. A mismatch
  stops the build as **ASSET FAILED** before
  any join.

## 4. Inputs (pinned at this draft; re-asserted at the freeze)

| Input | Pin / state |
|---|---|
| Positional record of the claim (`glossa-indus/analysis/positional/hunt_tripartite_test.json`) | SHA-256 `0e546962c1b72b929c87d4ce40c97633e8e3e340737f32f5dd3eae9f04759e48` (recomputed at this draft from `main` at `83b6a563…`): 805/2,267 formula inscriptions; 40/61/20 strong-sign classes. |
| Phase-43 battery record (`outputs/phase43_all.json`) | SHA-256 `78a6c21908b9362854c54dd3d820d717be22feab3af11135663fa14aaf554fe4` (recomputed at this draft). The source of the recorded effect sizes from which the freeze sets the §5 fit margin. |
| Corpus layer of record (`backend/glossa_lab/data/yajnadevam_inscriptions.csv`) — the strict/programme corpus layer the positional framework runs on | SHA-256 `c02e3d7bb74cf5abb11cc94f88d8d469e6acc5d6fad4b7153c02c43428f58d98` (recomputed at this draft; the same layer pinned by Spec 042's draft). |
| Sign crosswalk of record (`data/crosswalks/sign_crosswalk_master.csv`) | SHA-256 `4ace1a617f40afe8d0bbb82e5461d98a675296152e7577b04fb67b00f4f5dfcf` (recomputed at this draft; re-asserted at the freeze, DD-045-18). Defines `sign_key` and the CISI/Parpola numbering of §2.1. Census at the freeze: 205 rows carrying 187 distinct `registry_sign_id` values — the full sign universe of §2.1. |
| Anchors file (`backend/reports/INDUS_FINAL_ANCHORS.json`) | SHA-256 `df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569` (recomputed at this draft). This spec moves no anchor; the file is asserted byte-identical before and after any execution. |
| Held published sources for Asset A | The CISI volumes (Vol. 1 and Vol. 2, held digitally and complete) and Parpola's published sign identifications — held, per the design; their editions are named in the build record at gate A1, and no label may cite a source not so named. |
| D-18 concordance output (Spec 046) | Spec 046 stands **FROZEN** at this freeze (2026-10-21; DD-045-21): freeze-act digest `80c3be31e5af5236f71cb2c1894b2946f9b8ad47b12bdeab9d03cd76468af405`, successor digest `e0d7add84b9d28ae5f6a6b392dca578b727ad4d99a117360a57d39f3b94b01c6`, both quoted as its `osf-spec-registration.md` presents them (§2.7). The concordance file itself does not exist yet: consumed only in the §2.6 frozen form, pinned by its own digest at Asset A's freeze, or replaced by its closure file under gate A2. |

The **test population** is fixed from the
record, not re-derived at run time: the signs
carrying recorded part-membership in the
positional framework (the 40 initial-strong,
61 medial-strong, and 20 terminal-strong signs
of the pinned positional record, overlaps as
recorded), together with every sign the §5
models score — each of which must satisfy
gate A3 before any model runs. Asset A's
coverage under gate A3 is wider than this
population — the full pinned-crosswalk sign
universe (DD-045-18) — because the asset is
consumed corpus-wide by its dependents.

## 5. The test (runs only after Asset A is frozen)

### 5.1 The two models

Two pre-registered predictive models of
part-membership (opening / middle / closing
sign classes, as recorded in the pinned
positional framework):

- **Model P** — position behaviour only: each
  sign's recorded positional profile.
- **Model PH** — model P **plus** depicted kind
  from the frozen Asset A.

Fit is compared **out of sample** on the
design's pre-registered split — odd versus
even inscription IDs — by the **fit margin
frozen at this spec's freeze** and recorded in
the freeze record **before the classification
is joined to the corpus** (the design's own
ordering). **Fit form and margin (frozen,
DD-045-11):** fit is out-of-sample predictive
accuracy — the share of held-out
part-membership predictions the model gets
right — and the margin is **0.05** (five
accuracy points, PH minus P). The value is
derived from the recorded Phase-43 effect
sizes: the positional record's initial-strong
signs carry a mean initial rate of 0.757
against 0.251 expected by chance, an
advantage of 0.506; one tenth of that
advantage is 0.0506, frozen as 0.05 — depicted
kind must add at least about a tenth of
position's own recorded advantage over chance
before it counts as discriminating (the
derivation is recorded in `adjudication.md`
§7). Contested
signs are excluded from the primary fit;
`unidentified` signs enter model P only and
are counted and reported, never dropped
silently.

### 5.2 The closing part, head-on

For each closing-strong sign of record, two
scores are computed from the pinned corpus:

- **(a) Suffix-like behaviour — Spec 045's
  closing distinct-predecessor measure** — the
  grammar signature, defined here operationally
  so this spec does not depend on any other
  spec having run: the rate at which the sign
  follows many different signs as a final
  element (its **closing distinct-predecessor
  rate** in final position, with its
  final-position count). That name —
  *closing distinct-predecessor rate* — is
  this measure's name wherever the shared
  vocabulary of closing-sign behaviour appears
  in this spec.
  **Measure disambiguation (DD-045-19, the
  DD-045-4 reconciliation, mirroring Spec
  054's OPEN-054-6):** this measure is a
  **different measure** from Spec 054's
  (design D-08's) closing measure, which is
  **Phase-43 terminal-strong set membership**
  — a set-membership state under the Phase-43
  battery, not a rate. A sign can sit in the
  terminal-strong set without a high closing
  distinct-predecessor rate, and the reverse.
  Neither spec adopts the other's form; no
  output of this spec may quote Spec 054's
  measure or result as this measure, and no
  output of Spec 054 may quote this spec's
  closing result as its own. At this freeze
  Spec 054 stands as a draft (PR #260), not a
  frozen text, so no frozen D-08 definition
  exists to reconcile against: this spec's
  operational definition governs for Spec
  045, and Spec 054's freeze will mirror this
  note (its OPEN-054-6).
- **(b) Depicted-kind membership** — whether
  the frozen Asset A classes the sign in the
  cycle/sky or jurisdiction-bearing kinds (in
  Asset A's field values: `sky_cycle`, and any
  `object_goods`/`other` row whose verbatim
  published label is a jurisdiction term as
  coded at entry — the coding rule for that
  subset is stated in the build record before
  the freeze, never after a score is seen).
  **Jurisdiction coding rule (frozen,
  DD-045-14):** entry-time coding as drafted
  is confirmed. A row is jurisdiction-coded
  exactly when its `depicted_label_verbatim`
  itself names an office, a holder of
  authority, or a governed place — king,
  chief, ruler, lord, district, province, or
  a city or town as a governed unit, or the
  verbatim equivalent in the source's own
  words. Coding is from the verbatim label
  alone: never from the row's depicted kind,
  never from the sign's position, and never
  from Hunt's text. The per-row coding is
  stated in the build record before the asset
  freeze. The alternative — restricting this
  score to `sky_cycle` alone — is rejected at
  this freeze: Hunt's closing prediction
  names jurisdiction signs expressly, and
  Asset A has no jurisdiction kind, so the
  restriction would silently halve the
  prediction under test.

**Comparison rule (frozen, DD-045-12).** The
two scores' agreement with recorded closing
membership is compared directly, as follows.
Over every sign in the test population with a
recorded positional profile, each score is
read as a ranking of closing membership —
score (b) by its binary membership value,
score (a) by its closing distinct-predecessor
rate — and agreement is the area under the
receiver-operating curve (AUC) of that score
against recorded terminal-strong membership.
Depicted kind predicts closing membership
better exactly when its AUC is **strictly
greater**; equal AUCs count as suffix-like
behaviour predicting at least as well, under
§5.4. The per-sign scores for the 20
closing-strong signs of record are published
beside the two pooled AUCs (§7).

### 5.3 Sensitivity (pre-registered, one)

The §5.1 primary and the §5.2 comparison are
rerun once, as a stated sensitivity: contested
signs included under their CISI-governed
labels, and `borderline` signs removed. The
sensitivity is reported beside the primary
with the same prominence; it does not replace
the primary's verdict word.

### 5.4 Verdict criteria (fixed in form; margins fixed at freeze)

- **DISCRIMINATED FOR HUNT** — model PH beats
  model P by the frozen fit margin **and**
  depicted kind predicts closing membership
  better than suffix-like behaviour under the
  frozen comparison rule.
- **DISCRIMINATED FOR THE GRAMMAR ACCOUNT** —
  suffix-like behaviour predicts closing
  membership at least as well as depicted kind
  **and** PH adds less than the frozen margin
  over P.
- **NOT DISCRIMINATED** — anything else. This
  outcome leaves the claim exactly as it
  stands, with the attempt recorded; it is a
  verdict, not a failure of the run.

### 5.5 Pre-written verdict wordings

The outcome record's headline paragraph uses
one of these forms, with the bracketed
quantities filled from the run:

- DISCRIMINATED FOR HUNT: "Classified by what
  they depict — from published identifications,
  entered blind and frozen before any join
  (Asset A, SHA-256 [digest]) — the signs sort
  into Hunt's three parts beyond what position
  alone predicts: the kind-aware model beats
  the position-only model by [margin observed]
  against the frozen margin of [margin], and
  depicted kind predicts closing membership
  better than word-ending behaviour ([scores]).
  The three parts pattern by depicted kind, the
  way Hunt's account requires. This does not
  establish that Hunt's specific readings of
  any sign or part are correct."
- DISCRIMINATED FOR THE GRAMMAR ACCOUNT:
  "Classified by what they depict (Asset A,
  SHA-256 [digest]), depicted kind adds
  [observed] over position alone — less than
  the frozen margin of [margin] — and
  word-ending behaviour predicts closing
  membership at least as well as depicted kind
  ([scores]). The depicted kinds fail to
  pattern positionally the way meanings
  require; the closing part behaves as grammar
  predicts. Hunt's three parts stand as a
  positional pattern only, as recorded."
- NOT DISCRIMINATED: "Classified by what they
  depict (Asset A, SHA-256 [digest]), the test
  does not separate the two accounts:
  [the model comparison and the closing
  comparison, with quantities]. The claim
  `without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_001`
  stands IN QUESTION exactly as recorded, now
  with a discrimination attempt on its record."
- ASSET FAILED (a §3 gate): "Asset A was not
  built as designed: gate [A#] failed —
  [observed values]. No model was fitted and
  no verdict is recorded under Spec 045.
  Specs for D-06 and D-13, which consume Asset
  A, are not-run under the campaign's cluster
  rule. The claim stands as recorded."
- INVALID (a §6 gate): "Spec 045 stopped
  before any model quantity: [the failed gate
  and observed values]. No verdict is recorded;
  the claim stands as recorded."
- NOT ADJUDICATED (a §5 control failure):
  "Spec 045's models ran but their controls
  failed: [the failing control]. No verdict
  word is recorded; the quantities are
  published as a machinery finding, not as
  evidence about the claim."

## 6. Step-0 gates before any model (fail-closed)

After Asset A is frozen (§3), execution runs
these checks in order, before any §5 quantity:

- **0.1 Input integrity.** Every §4 input
  hashes to its freeze-record value, and Asset
  A's digest recomputes. Mismatch → **INVALID**.
- **0.2 Positional reproduction.** The pinned
  positional record's quantities are reproduced
  from the pinned corpus under the recorded
  framework — the 805/2,267 formula count and
  the 40/61/20 strong-sign classes. Mismatch →
  **INVALID**: the test does not proceed on a
  framework that cannot first reproduce its own
  recorded result.
- **0.3 Population census.** The §4 test
  population is enumerated and published, with
  its Asset A coverage restated (kinds,
  contested, unidentified counts) — over the
  test population and, under gate A3's
  restated scope (DD-045-18), over the full
  pinned-crosswalk sign universe. Any sign in
  the population without an Asset A row →
  **INVALID** (gate A3 should have caught it;
  its appearing here is a machinery finding).
- **0.4 Freeze-order proof.** The freeze record
  shows the fit margin and the §5.2 comparison
  rule were recorded before the first join.
  Absent that proof → **INVALID**: a margin set
  after a join is not a frozen margin.

## 7. Controls and named confounders

- **Classification circularity** — the central
  confounder, controlled by construction:
  published identifications made for other
  purposes, entered blind (§2.4), disputed by
  rule (§2.5), frozen before any join (§2.7).
- **Frequency** — rare depicted kinds are
  pooled as `other` by the rule frozen at
  this freeze (DD-045-13: a kind with fewer
  than **5 signs** in the primary population
  is pooled as `other` for the §5.1 model;
  contested and unidentified rows are never
  pooled); per-kind counts before pooling are
  published with every result so pooling can
  never hide a kind.
- **Object-type divergence between
  compilations** — Spec 037's census found
  object-*type* labels diverging between the
  CISI volumes and the programme's corpus in
  **49% of matched cases**. Asset A classifies
  **signs by what they depict**, not objects by
  type, and takes every label from the
  published sources named in §2.3 — but the
  census is the standing warning that
  compilation labels are not interchangeable,
  and §8 carries it as a limit on every use of
  the asset.
- **The pattern's weakness as evidence** —
  many record systems develop fixed field
  orders. This spec does not test whether a
  pattern exists (settled); it tests only
  which account of it fits better.
- **One frequent kind carrying a class** —
  per-sign closing scores are published beside
  the pooled §5.2 comparison, so no single
  sign's behaviour can carry the head-on test
  silently.

## 8. Epistemic limits (binding on all outputs)

1. **No gloss is established.** Even a clean
   DISCRIMINATED FOR HUNT shows the parts sort
   by depicted kind; Hunt's specific readings
   (this sign = guild, that part = tribute)
   remain readings, not measurements.
2. **Depiction is the field's published
   identification, not ground truth.** Asset A
   records what the published lists say a sign
   depicts, with citations. A verdict under
   this spec is a statement about the published
   identification layer, exactly as the
   D-18 design states for its own layer.
3. **The 49% caution travels with the asset.**
   Spec 037's census (object-type labels
   diverging in 49% of matched cases between
   compilations) is restated wherever Asset A
   or a verdict under this spec is stated. The
   asset's answer to it is its construction —
   held published sources only, blind entry,
   dispute by rule, freeze before join — not a
   claim that the divergence does not exist.
4. **The frozen positional record stands.**
   The 805/2,267 pattern and its IN QUESTION
   status are records of their own test; this
   spec appends a discrimination record beside
   them and edits neither.
5. Negative, undiscriminated, asset-failed,
   and not-adjudicated outcomes publish with
   the same prominence as a discrimination.

## 9. Reporting obligations

Every product of an execution carries, in its
headline paragraph: the claim identifier; the
Asset A digest and its per-kind counts; the
model comparison (both fits, the frozen
margin, the observed difference); the closing
comparison (both scores); the verdict word of
§5.4 or the closure class of §10; and limit 1
of §8 in plain words.

Deliverables at execution: the built Asset A
(CSV + `asset-a-freeze.json` + build record);
a results JSON (censuses, both models' fits,
the closing scores per sign and pooled, the
sensitivity, control outcomes, the §6 gate
record); a report under these headline rules;
the experiment-graph node (H15/H23, registered
and verified before the run); the outcome
append in this directory; and the LEDGER entry
(H1). Foundation check (H21) after the
execution phase: 0 failures, or the outcome
record says why not. Anchors asserted
byte-identical before and after.

## 10. Stop conditions and outcome classes

Execution ends in exactly one of:

- **ASSET FAILED** — a §3 gate A1, A3, A4, A5,
  or A6 fails. (Gate A2 is a sequencing stop:
  the build has not started, and no outcome
  class is recorded until it resolves or the
  campaign closes the member.)
- **INVALID** — a §6 gate fails.
- **NOT ADJUDICATED** — a §5 control fails.
- **DISCRIMINATED FOR HUNT**,
  **DISCRIMINATED FOR THE GRAMMAR ACCOUNT**,
  or **NOT DISCRIMINATED** — per §5.4, after
  all gates pass.

## 11. Execution shape (gated; NOT run by this draft)

1. **Asset build** (§§2–3) — source entry
   blind, dispute coding, D-18 input, freeze.
2. **Graph-first build** (H15/H23) — script,
   graph node, registration, verification.
3. **Step 0** (§6) — integrity, reproduction,
   census, freeze-order proof.
4. **Primaries** (§5) — models P and PH, the
   closing head-on comparison, the sensitivity.
5. **Outcome** (§9) — appended records only;
   anchors asserted byte-identical; foundation
   check reported as measured.

## 12. What this spec is not

Not a re-run of the positional test (its result
is the premise, not the subject), not a
decipherment, not a test of any single sign's
meaning, not a construction of any other asset
(Asset B is D-09's; Asset F is D-02's), and not
an authorisation to execute. It is the
discrimination test the positional record's own
verdict said was missing, plus the one
classification build three Hunt designs share —
designed so that its honest outcomes, including
failing to build its own asset, are written
down before any sign is classified.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
