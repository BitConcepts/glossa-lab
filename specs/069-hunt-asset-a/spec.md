# Spec 069 — Hunt Depicted-Kind Classification: The Asset A Build (Contract of Spec 045 §§2–3)

> ## DESIGN DRAFT — FOR FREEZE DECISION — 2026-10-22
>
> Drafted under the owner's readiness decisions
> of 2026-10-22, **decision 3** (the Hunt
> programme, re-scoped on the Shakti corpus):
> the owner commissioned three new specs in
> dependency order — this build first, then the
> opening-signs successor (Spec 070), then the
> sky-signs successor (Spec 071). Drafts are
> pre-approved standing in this programme;
> **the freeze, the registration, and the
> execution of Spec 069 are separate later
> owner acts.** No AEE lifecycle hooks have run
> on this draft; they are the freeze gate,
> applied in the substantive form of DD-038-10
> (zero correctness failure modes and no claim
> below the 0.70 threshold at after_specify,
> after_plan, and after_tasks). Nothing in this
> draft has been run, frozen, registered,
> joined, or computed — in particular, **Asset A
> does not exist yet**: this spec builds it at
> execution, and its first product is the
> classification itself, with its digest.
>
> The execution phase number is **unassigned**
> at this draft. It is allocated at the freeze
> act, from the merged record as it then
> stands.
>
> **Dependency chain (commissioned order):
> Spec 069 → Spec 070 → Spec 071.** Spec 069 is
> first in that order. Its frozen product —
> Asset A and its digest — is the asserted
> step-0 input of Spec 070 and of Spec 071.
> Neither successor can freeze before Asset A
> exists as a frozen product of this spec.

**Contract source:** Spec 045
(`specs/045-hunt-depicted-kinds/spec.md` on
`main`), frozen 2026-10-21 under freeze digest
`5d8254ddc03045b68a0819f870fc9ccc1b9848a58fef3862dae3e4ca21b43f0a`.
Sections 2 and 3 of that frozen text — the
Asset A contract and its build gates A1–A6 —
are quoted in full in §2 of this draft and are
the whole contract of this spec. Spec 045
itself closed **INVALID at its step-0 gate
0.2** (positional reproduction) at its
execution of 2026-10-21, before its step-1
Asset A build was reached, so no Asset A
digest exists on any record. That closure
stands untouched: this spec does not reopen,
amend, or re-run Spec 045, and it runs none of
Spec 045's test (its §§5–6 models and gates
are not part of this spec). What transfers —
as the readiness assessment of 2026-10-22
(`~/workspace/research_notes/shakti-readiness-proposals-2026-10-22.md`,
§1.5, Spec 045) established first-hand — is
the Asset A build alone, because that build is
corpus-independent: it is a classification
from held published sources, entered blind,
frozen before any join, and nothing in
§§2–3 names any corpus.

**Claim this build serves:** the Hunt claims
whose tests consume Asset A by digest —
`without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_001`
(Spec 045's three-part claim, standing
IN QUESTION),
`without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_003`
(the opening/animal claim, Spec 070's subject),
and
`without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_004`
(the sky-signs claim, Spec 071's subject).
This spec adjudicates none of them. It builds
the one classification all three tests need,
so that its honest outcomes — including
failing to build the asset — are written down
before any sign is classified.

**AI disclosure:** this draft is produced by an
AI agent (Muse Spark, via Muse) at the
direction of Tristen Pierson, per constitution
§VI.

---

## 1. What this spec is, in plain words

Three Hunt tests all turn on one thing nobody
has ever built: a list that says, sign by sign,
what each sign depicts — animal, sky or cycle,
object or goods, human, or other — taken from
the published sign lists, not from anyone's
guess at the moment of testing. Spec 045
wrote the contract for that list (its §§2–3)
and froze it, but its own execution stopped at
an earlier gate, so the list was never built.

This spec is the build, and only the build.
It takes Spec 045's frozen §§2–3 as its whole
contract — quoted in full below, not
paraphrased — builds the classification from
the held published sources (the CISI volumes
and Parpola's published identifications),
entered blind to any positional result, with
disputes coded by rule, and freezes it before
any join to any corpus. The product is the
classification file and its SHA-256 digest,
published as this spec's first product. That
digest is what Specs 070 and 071 assert at
their step 0.

### 1.1 The build's falsifier, first

**Falsifier.** The build fails, and says so,
if any build gate of §3 (gates A1–A6, quoted
verbatim from Spec 045) fails: a governing
source not in hand (A1), the D-18 input
unresolved (A2), a sign of the full
pinned-crosswalk universe left without a row
(A3), a row without its citation (A4), blind
entry breached or unattested (A5), or the
freeze record's digest not recomputing from
the canonical file (A6). A failed build is
recorded as **ASSET FAILED** with the gate
named; the asset is not repaired inside this
spec, and Specs 070 and 071 are not-run in
their turn under their own step-0 rules.
Nothing below is written so that this
falsifier cannot fire: the gates run in
order, before any join, and no quantity of
any dependent test exists in this spec at all.

### 1.2 What this spec does not consume

This spec has **no corpus gate and no Shakti
input**. It reads no inscription corpus,
computes no positional quantity, and cites
the Shakti corpus nowhere as an input. Its
inputs are the held published sources, the
pinned sign crosswalk that defines the sign
universe and the sign keys, and the D-18
concordance input in the form Spec 045 §2.6
froze (§4). A reader who finds a corpus
quantity in an execution product of this spec
has found a defect, not a result.

## 2. The contract — Spec 045 §§2–3, quoted in full

The text between the two markers below is
Spec 045 §§2–3 **verbatim**, as frozen on
`main` under freeze digest
`5d8254ddc03045b68a0819f870fc9ccc1b9848a58fef3862dae3e4ca21b43f0a`
(read first-hand at this draft from
`origin/main` at
`2a0eb854982f52453bcd76fd4a5bcbb088eb21e8`).
Section numbers inside the quotation are
Spec 045's own. Where the quoted text speaks
of "this spec", of Spec 045's own test (§5),
or of the campaign that froze Spec 045, the
words stand as written: the quotation is the
contract, and §2.1 after the quotation states
exactly how each such reference is read for
this build — openly, never by silent edit of
the quoted text. If any part of this draft
outside the quotation and Spec 045's quoted
text ever differ, Spec 045's text governs and
the difference is a defect in this draft,
recorded as such.

> **[BEGIN VERBATIM QUOTATION — Spec 045 §§2–3]**

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

> **[END VERBATIM QUOTATION — Spec 045 §§2–3]**

### 2.1 How the quoted contract is read for this build (stated, not silent)

- **Location of the asset.** The quoted §2.1
  places the canonical file in "this spec's
  directory". Spec 045's execution never built
  it, so no such file exists in Spec 045's
  directory, and Spec 045's record is frozen
  and closed and is not edited. For this
  build, the canonical file is
  `specs/069-hunt-asset-a/asset-a/depicted-kind-classification.csv`
  in **this** spec's directory, with its
  machine record at
  `specs/069-hunt-asset-a/asset-a/asset-a-freeze.json`
  carrying exactly the §2.7 contents. Specs
  070 and 071 pin **this** location and the
  digest recorded in it. The form, fields,
  and freeze contents are the quoted ones,
  unchanged; only the directory is this
  spec's, and that is stated here so no
  reader has to guess it.
- **References to Spec 045's own test.** The
  quoted text mentions Spec 045's §5 test,
  its §4 test population, and its step-0
  gates. None of that test is part of this
  spec. Those references are read as the
  contract's own record of why the asset's
  rules are as strict as they are — above
  all the freeze-before-any-join order of
  §2.4 and the coverage scope of §2.1
  (restated by Spec 045's DD-045-18) — and
  they impose no act on this spec beyond the
  build itself. Coverage under gate A3 is
  the full pinned-crosswalk sign universe,
  exactly as quoted: every distinct
  `registry_sign_id` in the pinned crosswalk
  — 187 distinct sign keys in 205 crosswalk
  rows at Spec 045's freeze census, the
  census re-asserted at this spec's freeze.
- **The D-18 input (§2.6, gate A2).** The
  quoted timing rule is satisfied on the
  record as it stands: Spec 046 reached a
  terminal outcome and its delivery is on
  record — the concordance file
  `specs/046-horned-tiger-concordance/concordance-297.json`,
  SHA-256
  `772db4df152ec4f1071bed088250677e55f69743532c9e89f339a8cf9134aaaf`,
  schema `glossa.concordance/1`, with an
  empty `signs` array and the `closure`
  block of its IDENTIFICATION FAILED
  outcome — the frozen §2.6 closure form, an
  **empty feed** (re-verified in Spec 045's
  execution record of 2026-10-21). Under the
  quoted §2.6, Asset A therefore proceeds
  without this feed and records its absence;
  the feed is never reconstructed from the
  asset's own labels. Gate A2 still runs at
  execution and re-asserts this state
  against the record as it then stands; if
  the state has changed, the quoted rules
  govern what the build may consume.
- **The campaign cluster rule.** The quoted
  §2.4 and gate A5 speak of the campaign's
  cluster rule for the asset's dependents.
  For this programme the dependents are
  Specs 070 and 071: an ASSET FAILED closure
  here means their step-0 Asset A assertions
  fail in their turn, in their own words.
  No other consequence is imported from the
  2026-10-21 campaign.

### 2.2 The product, and what "published" means here

The build's first product — published before
any other product of this spec and before any
product of Spec 070 or Spec 071 — is:

1. the canonical classification
   `asset-a/depicted-kind-classification.csv`,
   generated with a CSV writer and
   round-trip validated (every row parses to
   exactly the field count of the quoted
   §2.2) — hand-edited CSV is not an asset;
2. `asset-a/asset-a-freeze.json` with the
   quoted §2.7 contents: the SHA-256 of the
   canonical CSV; the row count and the
   per-kind counts; the pins of every input
   (§4, plus the D-18 state of §2.1); the
   build-order attestation; and the freeze
   date; and
3. the build record: the entry log, the
   editions of the sources named at gate A1,
   the dispute coding, the D-18 disposition,
   and the gate-by-gate record of §3.

After the freeze point the asset changes only
by dated, append-only defect notices, never
by editing a row (quoted §2.7). A defect that
reaches a verdict produced by a dependent
marks that verdict; it does not rewrite it.

## 3. Build gates (fail-closed; before any join)

Execution of this spec runs gates **A1–A6
exactly as quoted in §2** (Spec 045 §3), in
order. A failure stops the build in the class
named there — **ASSET FAILED** for A1, A3,
A4, A5, and A6; gate A2 is the quoted
sequencing stop (the build does not start,
recorded, not a verdict). Nothing is repaired
at run time, and no dependent quantity is
computed past a failed gate — this spec
computes no dependent quantity in any case.

## 4. Inputs (pinned at this draft; re-asserted at the freeze)

| Input | Pin / state |
|---|---|
| The contract (Spec 045 §§2–3) | Frozen text on `main`; Spec 045 freeze digest `5d8254ddc03045b68a0819f870fc9ccc1b9848a58fef3862dae3e4ca21b43f0a` (from `specs/045-hunt-depicted-kinds/freeze.json`, read first-hand at this draft). Quoted in full in §2. |
| Sign crosswalk of record (`data/crosswalks/sign_crosswalk_master.csv`) | SHA-256 `4ace1a617f40afe8d0bbb82e5461d98a675296152e7577b04fb67b00f4f5dfcf` (as pinned by Spec 045 §4; re-asserted at this spec's freeze). Defines `sign_key` and the CISI/Parpola numbering of the quoted §2.1. Census: 205 rows carrying 187 distinct `registry_sign_id` values — the full sign universe of gate A3. |
| Held published sources for the build | The CISI volumes (Vol. 1 and Vol. 2, held digitally and complete) and Parpola's published sign identifications — held, per the quoted §2.3; their editions are named in the build record at gate A1, and no label may cite a source not so named. |
| D-18 concordance output (Spec 046) | Terminal delivery on record: `specs/046-horned-tiger-concordance/concordance-297.json`, SHA-256 `772db4df152ec4f1071bed088250677e55f69743532c9e89f339a8cf9134aaaf`, an empty feed under its IDENTIFICATION FAILED closure (§2.1). Consumed only in the quoted §2.6 form. |
| Anchors file (`backend/reports/INDUS_FINAL_ANCHORS.json`) | SHA-256 `df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569` (as pinned by Spec 045 §4). This spec moves no anchor; the file is asserted byte-identical before and after any execution. |

No corpus of any kind is an input to this
spec — not the programme's corpus layers, not
the Phase-43 records, and not the Shakti
corpus. The positional records that Spec 045
§4 pinned for its own test are not pinned
here, because no positional quantity is
computed here.

## 5. Outcome classes and pre-written wordings

Execution ends in exactly one of:

- **ASSET BUILT AND FROZEN** — gates A1–A6
  all pass, in order, before any join; the
  §2.2 product is published.
- **ASSET FAILED** — a gate A1, A3, A4, A5,
  or A6 fails, in the quoted words of §2.
- **BUILD NOT STARTED (gate A2)** — the D-18
  input state is neither a landed, pinned
  concordance file in a terminal state nor a
  closure record on record: a sequencing
  stop, recorded, not a verdict, in the
  quoted words of gate A2.

The outcome record's headline paragraph uses
one of these forms, with the bracketed
quantities filled from the run:

- ASSET BUILT AND FROZEN: "Asset A is built
  and frozen under Spec 045's §§2–3 contract
  as quoted and executed by Spec 069: [row
  count] rows over the full pinned-crosswalk
  sign universe — [per-kind counts] — entered
  blind from the held published sources, with
  disputes coded by rule and the D-18 input
  recorded as [state]. Asset A, SHA-256
  [digest], is published as this spec's first
  product and is the asserted step-0 input of
  Spec 070 and Spec 071. This does not
  establish what any sign means: the asset
  records what the published lists say a sign
  depicts, with citations."
- ASSET FAILED: "Asset A was not built as
  designed: gate [A#] failed — [observed
  values]. No classification is published as
  a frozen product, no digest is asserted by
  Spec 070 or Spec 071, and no verdict is
  recorded under this spec. The Hunt claims
  stand as recorded."
- BUILD NOT STARTED (gate A2): "Spec 069's
  build did not start: the D-18 input is
  neither a landed, pinned concordance file
  in a terminal state nor a closure record on
  record — [observed state]. This is a
  sequencing stop, recorded, not a verdict."

## 6. Epistemic limits (binding on all outputs)

1. **No gloss is established.** The asset
   records depicted kinds; it does not
   establish that any sign means anything,
   and no product of this spec may present a
   depicted kind as a reading.
2. **Depiction is the field's published
   identification, not ground truth.** Asset
   A records what the published lists say a
   sign depicts, with citations. Every use
   of the asset, here and in its dependents,
   is a statement about the published
   identification layer.
3. **The 49% caution travels with the
   asset.** Spec 037's census found
   object-*type* labels diverging between
   the CISI volumes and the programme's
   corpus in 49% of matched cases. Asset A
   classifies signs by what they depict, not
   objects by type, and takes every label
   from the published sources of the quoted
   §2.3 — but the census is restated wherever
   Asset A is stated, as the standing warning
   that compilation labels are not
   interchangeable. The asset's construction
   — held published sources only, blind
   entry, dispute by rule, freeze before
   join — is the answer to it, not a claim
   that the divergence does not exist.
4. **Spec 045's closure stands.** This spec
   neither reopens nor repairs Spec 045's
   INVALID closure at gate 0.2, and no
   product of this spec is a verdict under
   Spec 045. The contract was frozen; the
   build was never reached; this spec
   reaches it, under a new spec number and
   its own freeze and registration.
5. Asset-failed and not-started outcomes
   publish with the same prominence as a
   built asset.

## 7. Reporting obligations

Every product of an execution carries, in its
headline paragraph: the contract anchor (Spec
045's freeze digest); the Asset A digest and
its per-kind counts, or the failed gate and
its observed values; the D-18 input state; and
limit 1 of §6 in plain words.

Deliverables at execution: the §2.2 product
(the built Asset A — CSV + `asset-a-freeze.json`
+ build record) as the first product; the
§3 gate record; a report under these headline
rules; the experiment-graph node (H15/H23,
registered and verified before the run); the
outcome append in this directory; and the
LEDGER entry (H1). Foundation check (H21)
after the execution phase: 0 failures, or the
outcome record says why not. Anchors asserted
byte-identical before and after.

## 8. Execution shape (gated; NOT run by this draft)

1. **Graph-first build** (H15/H23) — script,
   graph node, registration, verification.
2. **Asset build** (the quoted §§2–3) —
   source entry blind, dispute coding, D-18
   input disposition, gates A1–A6 in order,
   freeze before any join.
3. **Publication** (§2.2) — the classification
   and its digest published as the first
   product.
4. **Outcome** (§7) — appended records only;
   anchors asserted byte-identical;
   foundation check reported as measured.

## 9. What this spec is not

Not a test of any Hunt claim, not a re-run or
reopening of Spec 045, not a corpus study of
any kind (no corpus gate, no Shakti input),
not a construction of any other asset, not a
decipherment, and not an authorisation to
execute. It is the one classification build
three Hunt designs share, commissioned on its
own so that the asset exists — frozen, with a
digest its dependents can assert — before any
successor test is frozen against it.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
