# Spec 051 — Roif: the Arrow Sign — Border Marker, or City Sign? (Design D-10)

> ## FROZEN — 2026-10-21
>
> Frozen under the runnable-experiments campaign
> plan approved by the owner AS WRITTEN on
> 2026-10-21 (campaign decisions E-1, E-2 and
> E-6, requirements R-2 and R-7). Design D-10 is
> campaign member 9 and a **consumer of Asset B**:
> the site-function classification built and
> frozen inside Spec 047 (design D-09) at its
> execution step 1. This spec does not build,
> re-derive, or repair Asset B. Its contract
> anchor is Spec 047's freeze digest
> `8501feabb7beee621e99ae48529e5a74c0788fb0619ac49c615912e13914cdc7`;
> the Asset B byte-digest does not exist at this
> freeze, because the asset is built later, at
> Spec 047's execution step 1 (Wave 3 group 1),
> so no byte-digest is stated here. The pin
> **source** is fixed instead: Spec 047's step-1
> outcome record,
> `specs/047-roif-ledger-distribution/outcome.md`
> (the outcome append in Spec 047's directory
> that its §4.6 freeze-point rule and §9
> reporting obligations specify), which will
> record the asset's SHA-256 digest with its row
> count, testable count, and per-status counts.
> Execution re-asserts that digest at its step 0
> (§3, gate 0.2): a mismatch stops this spec as
> **INVALID**, and an unfrozen or unsound asset
> closes it as **NOT-RUN** by dependency closure
> — Spec 047 §4.6's consumer rule, carried here
> in advance, with its fail-closed semantics
> unchanged (freeze ruling DD-051-14,
> `adjudication.md` §7). The freeze decisions
> DD-051-9 to DD-051-16 are recorded in
> `adjudication.md` §7; DD-051-1, DD-051-2,
> DD-051-3, DD-051-5, and DD-051-8 are confirmed
> there as drafted.
>
> **Roif gate (campaign R-7 / Part 8).** This is
> a Roif-claim experiment. Roif's preprint
> verification landed on 2026-10-21: Avishai
> Roif publicly posted the work on Academia.edu
> in 2025 and it is citable (citations in §2.1).
> Publication of this spec's results remains
> the owner's separate GATE act regardless.
> Until that act, this spec's records are
> internal, nothing derived from them is
> surfaced on any public surface, and campaign
> reporting names this member only as
> "executed — held under the Roif gate" (§9,
> §10 limit 1).
>
> Execution runs as **Phase-409** (allocated at
> this freeze, DD-051-15). Nothing in this
> contract has been run or computed: no site
> class has been read for a test, no arrow-sign
> share has been calculated, and the counting
> layer has not been exported. Execution awaits
> this freeze merging, the OSF registration's
> approval act, and a separate execution order.

**Design source:** D-10 in the experiment-design
packet at PR #195
(`docs/research/experiment-designs-2026-10-13/02-roif-and-hunt.md`,
§D-10, read in full at this draft), with the
portfolio triage of 2026-10-21 (design D-10
found **RIPE**: "Sign 391's per-site counts are
on record, and its one shared input (D-09's
site-function classification) is cited-data desk
work buildable in the same programme").

**Claim under test:**
`indus_valley_script_deciphered_from_myth_65ff0a26_manual_003`
— "The arrow sign (tīr) encodes border
enforcement or guild authority" — standing
**UNTESTED**: Phase-104 held it untested under
rule **RULE-SITE**, because its falsification
condition — "If arrow sign does not cluster at
gateway/border sites" — needs a classification
of sites by function that did not exist in the
repository. Spec 047 builds that classification
as Asset B; this spec runs the test the claim's
own record proposes, against that frozen asset
and against no other classification.

**AI disclosure:** this draft is produced by an
AI agent (Muse Spark, via Muse) at the
direction of Tristen Pierson, per constitution
§VI.

---

## 1. The claim and the record it stands on

The claim says the arrow sign — Mahadevan sign
391, **M391** — marks border enforcement: a sign
for checkpoints, encoding "border enforcement
or guild authority" (proposed value in the
claim's record: *tīr*, enforcement at borders).
Its own proposed test is distributional: the
sign should cluster at gateway and border
sites.

The counts already on the record lean the other
way. Phase-104's evaluation of this claim
(`glossa-indus/reports/phase104_claims_evaluation.json`,
SHA-256 `2d0b83e8…`, pinned in §2) records the
M391 site distribution in the Holdat corpus, in
full:

| Site | M391 occurrences |
|---|---|
| Mohenjo-daro | 75 |
| Harappa | 52 |
| Dholavira | 16 |
| Lothal | 14 |
| Surkotada | 11 |
| Kalibangan | 10 |
| Chanhu-daro | 10 |
| Banawali | 3 |
| Rakhigarhi | 2 |
| **Total** | **193** |

The design text quotes the five largest of
these (Mohenjo-daro 75, Harappa 52, Dholavira
16, Lothal 14, Kalibangan 10) and reads them
plainly: "mostly the great cities." The full
nine-site record above is the census of record
for this spec; gate 0.4 re-derives it from the
counting layer and stops the run if it does not
reproduce (§3).

The same Phase-104 entry records the rival this
test must beat. The Holdat roles file
(`outputs/analysis/holdatllc_sign_roles.json`,
SHA-256 `3f1c24ed…`, pinned in §2) classes M391
as **CASE_MARKER_SUFFIX** (mapped to TERMINAL;
`is_ending` true; 193 occurrences — the same
total as the distribution above; average
position 0.6). If the sign is a case-ending
marker, its per-site distribution should track
text length and corpus size, not site function.
Both readings are scored in the same run (§5.3),
and the two scores are reported separately
rather than forced into one choice (§10,
limit 3).

Phase-104's verdict on the claim stands as
recorded — *stays untested*, rule RULE-SITE,
reason: "Falsification condition requires
site-typology data …; no such dataset exists in
the repo — the Holdat corpus carries site names
only." This spec's outcome appends to the
claim's record as a dated entry beside that
record; nothing is edited or re-adjudicated
(§10, limit 4).

### 1.1 The question, in plain words

The arrow sign's raw counts sit in the biggest
cities. Is that just because the big cities have
more of everything — more inscriptions, longer
texts — or is the sign genuinely a city sign
rather than the border marker the claim says it
is? The test compares the sign's *share* of each
site's inscriptions across the frozen site
classes, so site size is controlled by
construction, and then asks separately whether
size alone, with no class at all, explains what
remains.

### 1.2 The hypothesis and its falsifier

**Hypothesis** (the claim's). Relative to each
site's total inscriptions, the arrow sign's
share is higher at gateway/border sites than
elsewhere — operationalised under Asset B's
fixed groupings (§4.2) as: the pooled
administrative/trade/gateway share exceeds the
domestic/ritual contrast share, and within the
pooled class the gateway/border share itself
exceeds the administrative share, the great
cities' class under the classification (§4.2,
boundary note).

**Falsifier.** The hypothesis fails if the
arrow sign's per-site distribution fits the
rival readings instead: its pooled share is at
or below its contrast share once totals are
controlled; or its gateway/border share is at
or below its administrative (great-city) share
— the comparison the claim's own falsifier
states; or site size alone explains the shares
and site class adds nothing beyond size, which
is what the case-ending rival predicts. §5.4
turns this into a mechanical verdict partition
fixed before any share exists; §6 pre-writes
the wording of every outcome in that partition.

## 2. Inputs (pinned at this draft where a pin exists; re-asserted at the freeze)

| Input | Pin / state |
|---|---|
| Claim record (`glossa-indus/claims/extracted_claims/indus_valley_script_deciphered_from_myth_65ff0a26.json`) — claim `manual_003`: normalised claim, proposed value *tīr* (enforcement at borders), falsification condition "If arrow sign does not cluster at gateway/border sites", status untested | SHA-256 `bc22d6f010f800d608d6e3f620fb430b3cf8d3ccd3caadc6a989116fbfd125ed` (recomputed at this draft from `main`, head `83b6a563…`, by two independent routes — contents raw and git blob — agreeing byte-for-byte) |
| Phase-104 claims evaluation (`glossa-indus/reports/phase104_claims_evaluation.json`) — the claim's UNTESTED / RULE-SITE record, carrying the nine-site M391 Holdat distribution (75 / 52 / 16 / 14 / 11 / 10 / 10 / 3 / 2; total 193) and the CASE_MARKER_SUFFIX role note | SHA-256 `2d0b83e8055a04b96635007054cfadde472f605dc7e5b249a61c8f9ea89b858d` (recomputed at this draft by both routes; matches Spec 047's corrected pin for the same file) |
| Holdat sign-roles file (`outputs/analysis/holdatllc_sign_roles.json`) — M391: `holdatllc_role` CASE_MARKER_SUFFIX, `mapped_to` TERMINAL, count 193, `is_ending` true | SHA-256 `3f1c24ed03b6393c4d222b4794d27cce9cbeaf8e30938dd4e0db0fddadd2d08f` (recomputed at this draft by both routes) |
| Gazetteer spine (`data/movement/gazetteer_rows.jsonl`) — Spec 027 Stage 0; Asset B's universe: 36 source-assertion rows, **30 distinct `program_site_id` clusters** | SHA-256 `5ac76a3031121a61fa39f87b1d2760855374d171ddd036988fee2820dca9b8b6` (recomputed at this draft by both routes; matches the pins Specs 044/047 carry) |
| **Asset B** — the site-function classification, built and frozen inside Spec 047's execution step 1 under Spec 047 §4's contract: file `specs/047-roif-ledger-distribution/asset-b/site-functions.jsonl`, exactly 30 rows, fields `program_site_id` / `site_name_as_published` / `status` / `primary_class` / `source_a` / `source_b` / `notes` | **No byte-digest exists at this freeze, deliberately (DD-051-14).** Asset B does not exist until Spec 047's execution step 1 builds and freezes it. The contract anchor is Spec 047's freeze digest `8501feabb7beee621e99ae48529e5a74c0788fb0619ac49c615912e13914cdc7`. The pin **source** is fixed as Spec 047's step-1 outcome record, `specs/047-roif-ledger-distribution/outcome.md`, which will record the asset's SHA-256 digest over the file bytes as committed (Spec 047 §4.6); execution asserts that digest at gate 0.2, before any class is read for a test — mismatch closes the run as INVALID, an unfrozen or unsound asset as NOT-RUN. See §4. |
| Counting layer of record — the Holdat corpus layer Phase-104 counted, carrying per-inscription site attribution and sign sequences in M-numbering, "as held in the database" (the posture of Specs 044/048) | **No file pin is stated at this draft, deliberately.** The repository holds Holdat-derived files, but the one per-symbol site-distribution file on `main` (`data/raw/other_sites/holdatllc_core_symbol_site_distribution.csv`) covers five sites only and carries **no M391 row** — verified at this draft (adjudication.md §2, defect 1) — so it cannot be the layer of record and is **not** pinned as one. The layer is identified, exported in full, and pinned by digest at step 0, before any counting, under gate 0.4 — and the run closes if it cannot be, or if the exported layer does not reproduce the §1 census. Inventing a pin at draft would repeat the stale-pin failure Spec 040's gate record documents. **Confirmed at the freeze (DD-051-13):** this identify/export/pin-at-step-0 posture stands as drafted — the freeze names no file pin and no separate canonical export form; the step-0 record must state the export's file form and sort order as produced, and the digest plus the exact §1 census reproduction (193 total; 75 / 52 / 16 / 14 / 11 / 10 / 10 / 3 / 2) together are the layer's identity test. |
| Anchors file (`backend/reports/INDUS_FINAL_ANCHORS.json`) | SHA-256 `df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569` (recomputed at this draft by both routes). This spec moves no anchor; the file is asserted byte-identical before and after any execution. |

**Explicitly not inputs:** the Yajnadevam-compiled
layer of Specs 027/028/047 (its numbering is not
the M-numbering the §1 census is stated in, and
no crosswalked second run is registered in this
draft — and **ruled unused at the freeze**
(DD-051-12): no crosswalked second run or
sensitivity is registered under this contract);
Spec 039's
period-assignment product (a period label is not
a site function); and Phase-147's internal
validation of other Roif renderings (not evidence
for or against this claim, §10 limit 5).

### 2.1 The Roif source of record

The claim originates in Roif's work, and the
verification of 2026-10-21
(`~/workspace/research_notes/roif-preprint-check-2026-10-21.md`)
establishes that the work is publicly posted, in
full, and citable:

> Roif, Avishai (2025). *Deciphering the Indus
> Valley Script: A Phonetic-Mnemonic Akkadian
> Shorthand Approach.* Academia.edu, published
> 12 June 2025.
> https://www.academia.edu/129921039/Deciphering_the_Indus_Valley_Script_A_Phonetic_Mnemonic_Akkadian_Shorthand_Approach

> Roif, Avishai (2025). *Indus Valley Script
> deciphered — From Mythology to History using
> the Akkadian shorthand approach.* Academia.edu,
> published 2 August 2025.
> https://www.academia.edu/143222807/Indus_Valley_Script_deciphered_From_Mythology_to_History_using_the_Akkadian_shorthand_approach

Academia.edu mints no DOIs; the URLs above are
the citable identifiers. Any later publication
of this spec's results cites Roif in this form
and remains a separate owner GATE act (§9).

## 3. Step 0 — gates before any arrow-sign share (fail-closed)

Execution runs these gates in order, before any
per-site share, ratio, or regression quantity is
computed. A failure stops the execution in the
class named; nothing is repaired at run time,
and no quantity produced before a gate failure
is quotable.

- **0.1 Input integrity.** Every §2 input that
  carries a pin hashes to its freeze-record
  value. A mismatch stops the run as **INVALID**
  (§6 wording).
- **0.2 Asset B digest assertion.** The
  execution exhibits Asset B's file at its
  contract path, recomputes its SHA-256 over the
  file bytes as committed, and compares it to
  the digest recorded in Spec 047's step-1
  outcome record
  (`specs/047-roif-ledger-distribution/outcome.md`)
  — the pin source this freeze fixes
  (DD-051-14), anchored on Spec 047's freeze
  digest `8501feab…`. If Spec 047's step 1 has not frozen
  Asset B, or the asset has been shown unsound
  under Spec 047 §4.6, the run closes as
  **NOT-RUN — ASSET B NOT AVAILABLE** (§6
  wording) — a dependency closure, not a
  verdict. If the recomputed digest differs from
  the freeze pin, the run closes as **INVALID —
  ASSET B DIGEST MISMATCH** (§6 wording). The
  asset is never rebuilt, re-derived, or
  substituted under this spec, in either case.
- **0.3 Asset B form and testable set.** The
  exhibited file is checked against the contract
  (Spec 047 §4.1): exactly 30 rows, one per
  pinned gazetteer cluster, the seven contract
  fields, statuses in {AGREED, DISAGREED,
  SINGLE-SOURCE, NO-SOURCE}, classes in the six
  of §4.2. The **testable set** is derived by
  rule: rows with status AGREED and
  `primary_class` ≠ `mixed/unknown`. Any form
  failure stops the run as **INVALID** (§6
  wording) — a malformed asset is not repaired
  by interpretation.
- **0.4 Counting-layer identification, pin, and
  census reproduction.** The Holdat layer of
  record is identified from the database as the
  layer Phase-104 counted (site-attributed,
  M-numbered), exported in full, and pinned by
  SHA-256 in the step-0 record. The gate then
  re-derives, from the pinned export: the M391
  per-site counts, which must reproduce the §1
  census **exactly** (Mohenjo-daro 75, Harappa
  52, Dholavira 16, Lothal 14, Surkotada 11,
  Kalibangan 10, Chanhu-daro 10, Banawali 3,
  Rakhigarhi 2; total 193, agreeing with the
  pinned roles file's count for M391); the
  per-site inscription totals (the exposure
  denominators of §5.2); and the per-site mean
  inscription lengths the §5.3 rival score
  needs. If the layer cannot be uniquely
  identified, cannot be exported whole, does not
  carry site attribution and sequence lengths,
  or the census does not reproduce, the run
  closes as **INVALID — COUNTING LAYER NOT
  PINNABLE / CENSUS NOT REPRODUCED** (§6
  wording) and nothing is counted.
- **0.5 Join census (counts of records, not of
  shares).** Every record of the pinned export
  is accounted for in exactly one of: (a)
  *joined* — its site value, normalised by the
  rule in §5.1, equals a spine cluster's
  normalised name; (b) *non-spine site* — its
  site is not a spine cluster (listed, with its
  record count and its M391 count); (c) *no site
  value* (counted). The census is published with
  the outcome either way. A record that cannot
  be placed in exactly one class stops the run
  as **INVALID** — no record is silently dropped
  or hand-assigned to a site. On the record as
  it stands, the non-spine class is expected to
  carry three of the §1 census sites —
  Dholavira (16 M391), Chanhu-daro (10), and
  Rakhigarhi (2), 28 of 193 occurrences — because
  the gazetteer spine carries no cluster for
  them (verified at this draft, adjudication.md
  §2); the step-0 record states what it observes,
  and any difference from that expectation is
  reported, not absorbed.
- **0.6 Test-population census and floors
  (counts only).** From the testable set
  (gate 0.3) and the join census (gate 0.5), the
  census reports, per Asset B class and per
  site: testable sites, joined inscriptions, and
  M391 occurrences — occurrence counts only, no
  share. The floors of §5.4 are then checked:
  at least **3 testable gateway/border sites
  carry M391 at all** (the design's floor), and
  neither the pooled side nor the contrast side
  of §4.2 is empty in the test population. A
  floor failure closes the execution as
  **INCONCLUSIVE — THE CLASSIFICATION IS THE
  FINDING** (§6 wording) with the full census as
  its finding; no share is computed. Note what
  is **not** a floor here: Spec 047's 12-testable-
  site gate governs Spec 047's own test only.
  This spec proceeds against a frozen Asset B of
  any testable count under its own floors
  (DD-051-5) — the question Spec 047's
  adjudication (§5, item 3) left to this draft,
  answered here and confirmed or overturned at
  the two freezes, openly.

## 4. Asset B — the consumed contract (Spec 047 §4, restated for the consumer)

This spec consumes Asset B exactly as Spec 047
froze it; this section restates the contract
only so the consumer's obligations are in one
place. Spec 047's text governs in any conflict.

### 4.1 Form and identity

- The asset file is
  `specs/047-roif-ledger-distribution/asset-b/site-functions.jsonl`:
  one JSON object per gazetteer cluster, exactly
  30 rows, rows sorted by `program_site_id`,
  fields exactly: `program_site_id`,
  `site_name_as_published`, `status`,
  `primary_class`, `source_a`, `source_b`,
  `notes`. Each of `source_a` / `source_b` is
  either null or an object with exactly:
  `citation`, `locator`, `stated_function`,
  `mapped_class`.
- The asset's identity is its **SHA-256 digest
  over the file bytes as committed**, recorded
  in Spec 047's step-1 outcome record
  (`specs/047-roif-ledger-distribution/outcome.md`).
  That record is the pin source this freeze
  fixes (DD-051-14); gate 0.2 asserts the digest
  it records, at execution. No byte-digest is
  stated at this freeze, because the asset is
  built later (Spec 047 execution step 1); the
  contract anchor quoted at this freeze is Spec
  047's freeze digest `8501feab…`.
  "The same classification" is thereby a
  verifiable fact, not an intention (campaign
  R-2).

### 4.2 Classes and groupings (fixed by Spec 047 §4.2, for this test too)

The six classes are: `gateway/border`,
`administrative`, `port/trade`, `domestic`,
`ritual`, `mixed/unknown`. The groupings fixed
in Spec 047 §4.2 "for the test and for D-10's
use" are carried verbatim: the **pooled class**
`ADMIN-TRADE-GATEWAY` = {`gateway/border`,
`administrative`, `port/trade`}; the **contrast
class** = {`domestic`, `ritual`};
`mixed/unknown` belongs to neither and never
enters the primary test.

**Boundary — where the design's wording and the
contract's groupings differ, stated, not
silently re-mapped.** The design (D-10) states
its comparison in words the asset does not
contain: gateway/border sites against "the
great-city sites," and its hypothesis as
gateway/border against "elsewhere." Asset B has
no great-city class and no size class, and this
spec invents none. The design's comparison is
therefore operationalised in the only form the
frozen asset supports, and the translation is
part of the frozen contract, visible to any
reader:

- the design's "elsewhere" is the §4.2 contrast
  class {domestic, ritual}, with the pooled side
  as fixed above (the primary ratio, §5.2);
- the design's "great-city sites" is the
  `administrative` class — the class the
  excavation literature's primary-function
  statements place the great centres in, *if*
  the two-source rule so classifies them. This
  draft pre-assigns no site to any class:
  whether Mohenjo-daro and Harappa are
  `administrative`, `mixed/unknown`, or anything
  else is Asset B's frozen output, not this
  spec's assumption. The gateway-versus-city
  discrimination is carried by the pre-registered
  ratio R_city (§5.2) as a verdict clause (§5.4),
  not by a re-grouping;
- site *size* is never a class in this test.
  Size is the rival explanation (§5.3); defining
  a comparison class by size and then testing
  whether size explains the pattern would be
  circular. The five largest test-population
  sites are reported descriptively as a
  sensitivity (§5.5), never as a verdict class.

If the freeze judges this translation wrong, it
overturns DD-051-1 openly in the frozen text; it
does not amend the design or the asset to fit.

### 4.3 Testable rule

A site enters the test only if its Asset B row
is `AGREED` and its class is one of the five
non-`mixed/unknown` classes. `DISAGREED`,
`SINGLE-SOURCE`, `NO-SOURCE`, and
AGREED-`mixed/unknown` sites are excluded by
rule and listed in full with the outcome, with
their M391 counts where the join census carries
them — a reader can see exactly which sites, and
how much of the sign, the verdict does not cover.

### 4.4 Consumer obligations

- Classes come from the frozen asset only. No
  class, status, or grouping is re-derived,
  adjusted, or supplemented under this spec,
  from inscription content or from any other
  source.
- After Spec 047's freeze, the asset file changes
  only by dated, append-only errata that change
  no row's status or class. Discovery that a row
  is wrong — a citation that does not state what
  the row claims, a status or class error — makes
  the frozen asset **unsound** under Spec 047
  §4.6: the campaign cluster tripwire fires, this
  spec closes as not-run (dependency closure,
  §6 wording), and a corrected asset requires a
  successor spec. The asset is never quietly
  edited and re-digested inside this campaign.

## 5. The test

### 5.1 Population and join

The test population is the set of **testable
sites** (§4.3) that carry at least one joined
inscription in the pinned counting layer under
gate 0.5's census. Testable sites with no joined
inscription are listed as `NO-CORPUS-COVERAGE`
with the census counts; they enter no share.
Non-spine sites (§3, gate 0.5 class (b)) are
outside the population by rule, however many
M391 occurrences they carry — on the present
record, 28 of the sign's 193 occurrences
(§3, gate 0.5). Site-name normalisation for the
join is mechanical, as in Spec 047 §6.1:
lowercase, whitespace and punctuation collapsed,
matched against the gazetteer cluster's
normalised name; no fuzzy matching and no hand
assignment.

### 5.2 Measures (pre-registered)

For each test-population site *i*: the arrow
share **s_i** = (M391 occurrences at *i*) /
(inscriptions at *i*), with site totals as the
exposure control — comparing shares, not counts,
is the size control the design specifies.

- **Primary ratio R.** The pooled class's
  aggregate arrow share over the contrast
  class's: **R** = (M391 at pooled sites /
  inscriptions at pooled sites) / (M391 at
  contrast sites / inscriptions at contrast
  sites).
- **City ratio R_city.** The gateway/border
  class's aggregate arrow share over the
  administrative class's: **R_city** = (M391 at
  gateway/border sites / inscriptions there) /
  (M391 at administrative sites / inscriptions
  there). This is the design's literal
  border-versus-city comparison (§4.2). Per-class
  aggregate shares for all five testable classes
  are reported alongside, so no pooled figure
  carries a class silently.
- **Significance.** Site class labels are
  shuffled across the test-population sites
  **9,999 times**; the p-value is the share of
  shuffles whose R is at least the observed R.
  The random seed is fixed at this freeze as
  **20261021** (DD-051-10) and recorded in the
  freeze record, before any share exists. A
  Fisher exact test on the pooled
  2 × 2 table (M391 / all other sign occurrences
  × pooled / contrast inscriptions) is computed
  and reported beside the permutation result;
  **ruled at the freeze (DD-051-11): it is not
  verdict-bearing** — the draft position is
  confirmed.

### 5.3 The rival score — size and text length (the case-ending reading)

Scored in the same run, reported separately
(§10, limit 3):

- **Size-only fit.** The per-site shares s_i are
  regressed on site size alone (log inscription
  total), sites weighted equally (DD-051-8).
- **Size-plus-class fit.** The same regression
  with the pooled/contrast class added.
- **Class-addition outcome**, exactly one of:
  **ADDS** — the class term is positive and its
  permutation p-value (class labels shuffled
  9,999 times, at the freeze-recorded seed
  20261021, DD-051-10) is < 0.05;
  **SIZE-ONLY** — the size slope is itself
  significant (permutation p < 0.05) and the
  class-addition p-value is ≥ 0.05; **NEITHER**
  — neither the size slope nor the class
  addition reaches the 5% level.
- **Text-length description.** Per-site mean
  inscription length is reported beside each
  site's share, and the correlation of share
  with mean length is stated descriptively. A
  case-ending sign should grow commoner where
  texts run longer; the description is published
  so the rival's second leg is inspectable, but
  no verdict clause turns on it at this draft —
  the verdict-bearing rival test is the
  size/class comparison above, as the design
  states it ("if size explains the shares and
  class adds nothing, the rival wins").

### 5.4 Criteria (the verdict partition, fixed in advance)

First, the **floors** of gate 0.6: fewer than 3
testable gateway/border sites carrying M391, or
an empty pooled or contrast side, closes the
execution as **INCONCLUSIVE — the classification
is the finding**, with counts stated and no share
computed.

Otherwise exactly one of:

- **SUPPORTED** iff **R ≥ 1.5** **and** the
  permutation test rejects at the 5% level
  (p < 0.05) **and** the class-addition outcome
  is **ADDS** **and** **R_city > 1.0** — the
  pooled excess exists, is distinguishable from
  chance, is not explained by size alone, and
  points at the border class rather than the
  great-city class.
- **NOT SUPPORTED** iff **R ≤ 1.0**, **or**
  **R_city ≤ 1.0**, **or** the class-addition
  outcome is **SIZE-ONLY** — in each case the
  claim's own falsifier, or the rival it names,
  fits the distribution better than the border
  reading does.
- **INCONCLUSIVE** in every remaining case:
  1.0 < R < 1.5; or R ≥ 1.5 with p ≥ 0.05; or
  the class-addition outcome is NEITHER with
  R > 1.0 and R_city > 1.0.

The partition is exhaustive and mechanical:
every (R, p, class-addition, R_city) outcome
lands in exactly one verdict, assigned from the
recorded quantities by any reader. One clause
diverges from Spec 047's partition, openly:
there, permutation non-rejection with R > 1.0 is
NOT SUPPORTED, because D-09's text says so.
D-10's text fixes NOT SUPPORTED as ratio at or
below 1.0, or size alone explaining the pattern;
non-rejection alone is neither, so it lands in
INCONCLUSIVE here (DD-051-3). The design governs
substance; the divergence is recorded, not
smoothed over.

### 5.5 Sensitivities (reported; never verdict-changing)

- **Per-class shares.** The aggregate arrow
  share of each of the five testable classes,
  with site and inscription counts, beside the
  primary — the pooled figure never stands
  alone.
- **Five largest sites.** The test-population
  sites with the most joined inscriptions,
  listed with their classes, shares, and M391
  counts, as the design's check on excavation
  and publication bias.
- **Each source alone.** Where Asset B's rows
  permit (each AGREED row carries both sources'
  mapped classes), R and R_city recomputed
  descriptively under source A's classes alone,
  then source B's alone, reported beside the
  primary.
- **Exclusions restated.** The `DISAGREED`,
  `SINGLE-SOURCE`, `NO-SOURCE`,
  `mixed/unknown`, `NO-CORPUS-COVERAGE`, and
  non-spine lists are republished with the
  outcome, with M391 counts, so a reader can see
  exactly what the verdict does not cover.

## 6. Pre-written verdict wordings

The outcome record's headline paragraph uses
one of these forms, with the bracketed
quantities filled from the run. Under the Roif
gate these wordings appear in internal records
only (§9).

- SUPPORTED: "Roif's arrow-sign reading is
  SUPPORTED as a distribution: at the testable
  sites of the frozen site-function
  classification (Asset B, digest [d]), the
  arrow sign's share of inscriptions at
  administrative, trade, and gateway sites is
  [R] times its share at domestic and ritual
  sites (permutation p = [p], 9,999 shuffles),
  site class adds predictive power beyond site
  size, and the gateway/border share itself
  exceeds the administrative (great-city) share
  (ratio [R_city]). This supports the border
  reading's distribution only. It does not
  establish that the sign meant border
  enforcement, and it does not falsify the
  sign's recorded case-ending role; both roles
  could coexist."
- NOT SUPPORTED: "Roif's arrow-sign reading is
  NOT SUPPORTED: [the pooled ratio is [R], at or
  below 1.0 / the gateway/border share does not
  exceed the administrative (great-city) share
  (ratio [R_city]) / site size alone explains
  the per-site shares and site class adds
  nothing beyond size — the pattern the
  case-ending rival predicts]. The falsifier
  the claim's own record states has fired: the
  arrow sign's per-site distribution fits the
  rival reading. This is a statement about
  distribution in the Holdat layer of record at
  Asset B's testable sites; it does not
  establish what the sign meant, and the
  descriptive city lean of the raw counts
  (Mohenjo-daro 75, Harappa 52 of 193 recorded
  occurrences) is now a controlled result, not
  an impression."
- INCONCLUSIVE (measures): "Roif's arrow-sign
  reading is INCONCLUSIVE: [the pooled ratio
  [R] falls between the pre-registered bounds /
  the pooled ratio [R] reaches the bound but
  the permutation test does not distinguish it
  from chance (p = [p]) / neither site size nor
  site class accounts for the shares at the
  frozen level (R = [R], R_city = [R_city])].
  The claim stands neither supported nor
  falsified under the frozen criteria; the
  quantities are recorded so the
  inconclusiveness is inspectable."
- INCONCLUSIVE (classification): "The
  arrow-sign test did not run: [n] testable
  gateway/border sites carry the arrow sign
  (floor 3) [or: one side of the comparison is
  empty in the test population]. The finding of
  this execution is the classification and the
  census themselves (Asset B, digest [d]):
  [status and class counts; per-site M391
  counts], with the excluded and non-spine sites
  named in full — including, on the record,
  Dholavira, Chanhu-daro, and Rakhigarhi, which
  carry 28 of the sign's 193 recorded occurrences
  outside the gazetteer spine. No share was
  computed. The claim stands UNTESTED, now with
  the reason measured rather than asserted."
- INVALID — ASSET B DIGEST MISMATCH: "The
  execution stopped at step 0, gate 0.2: Asset
  B as exhibited hashes to [observed digest],
  which differs from the digest recorded in
  Spec 047's step-1 outcome record
  ([pinned digest], the pin source fixed at
  this spec's freeze, DD-051-14). No
  class was read for a test and no quantity was
  computed. Under Spec 047 §4.6's consumer rule
  this spec closes as INVALID; the asset is not
  rebuilt or substituted under this spec. The
  claim stands UNTESTED."
- INVALID (other step-0 gates): "The execution
  stopped at step 0, gate [0.1/0.3/0.4/0.5]:
  [observed values]. No share was computed. The
  claim stands UNTESTED."
- NOT-RUN — ASSET B NOT AVAILABLE (dependency
  closure): "This execution did not run: Asset B
  [has not frozen inside Spec 047's step 1 / has
  been shown unsound under Spec 047 §4.6]. The
  builder and its dependents close as not-run by
  dependency closure (campaign Part 7). No
  quantity was computed, and this closure is a
  statement about the asset, not about Roif's
  claim, which stands UNTESTED."

## 7. Controls and named confounders

- **Small counts at small sites.** Shares at
  sites with few inscriptions are noisy by
  construction. The controls are the design's:
  exact and permutation machinery (§5.2), the
  floors stated in advance (gate 0.6), and every
  per-site count published with its share. No
  site is dropped for smallness after the fact.
- **Classification disputes.** Asset B's
  two-source rule carries over unchanged (§4);
  disagreed sites are excluded by rule and
  listed, and the each-source-alone sensitivity
  (§5.5) shows what either source would say on
  its own.
- **The descriptive city lean already on the
  record.** The raw counts lean toward the great
  cities (§1), and this spec says so before any
  result exists, so the result — whichever way it
  lands — is read against that lean honestly: a
  SUPPORTED outcome must beat it through the
  controlled shares, and a NOT SUPPORTED outcome
  confirms it as a controlled finding rather
  than discovering it.
- **Excavation and publication bias.** Big,
  famous sites are more dug and more published,
  in the corpus and in the classification
  literature alike. Shares control corpus volume;
  the five-largest sensitivity (§5.5) exposes the
  concentration; neither is claimed to eliminate
  the bias, and the outcome wording carries the
  population it actually covers.
- **Spine coverage.** The gazetteer spine is the
  asset's universe and therefore this test's:
  sites outside it (gate 0.5) cannot enter,
  however many arrow signs they carry. The
  verdict is a statement about the spine's
  testable sites, and §8 requires every product
  to say so.
- **One corpus layer.** The verdict-bearing
  counts come from the Holdat layer of record
  alone (§2). Its lineage posture is as recorded
  in the program's Holdat records; no second
  layer silently shares the verdict (the
  second layer is ruled unused at the freeze,
  DD-051-12).

## 8. Reporting obligations

Every product of an execution carries, in its
headline paragraph:

1. the corpus label — the Holdat layer of record
   as pinned in the step-0 record, with its
   lineage posture as recorded;
2. the Asset B digest, the testable count, and
   the per-status counts of §4.3;
3. the join census of gate 0.5, including the
   non-spine sites by name with their M391
   counts;
4. per-site shares with their counts, R, the
   permutation p-value, R_city, the per-class
   shares, and the class-addition outcome with
   both regression fits' quantities (§5.3);
5. the fence sentence: "This result is about
   the arrow sign's distribution. It is not
   evidence of what the sign meant."

Deliverables at execution: a results JSON
(censuses, classification counts, per-site and
per-class shares, the primary quantities,
permutation record, rival-score record,
sensitivities); a report under these headline
rules; the experiment-graph node (H15/H23,
registered and verified before the run); the
outcome append in this directory; and the
LEDGER entry (H1). Foundation check (H21) after
the execution phase: 0 failures, or the outcome
record says why not. Anchors asserted
byte-identical before and after.

## 9. The Roif gate (binding on every output)

1. **Held, not surfaced.** This spec's execution
   records, results JSON, report, and outcome
   append are internal program records. No
   summary, article draft, paper text, website
   text, or public register wording derived from
   them is produced by this spec or by the
   campaign.
2. **Reporting form.** Campaign and status
   reporting names this member only as
   **"executed — held under the Roif gate"**,
   with no result content, until the gate clears.
3. **Clearing the gate** requires both: the
   verification of 2026-10-21 standing on record
   (it does: Roif's work is publicly posted and
   citable, §2.1), **and** the owner clearing the
   specific publication act as its own GATE
   decision, with the §2.1 citations carried in
   the published text. The verification alone
   clears nothing; this spec's freeze and
   execution clear nothing.
4. The daily-article process and every other
   public surface are barred from drawing on
   this spec's results absolutely, until the
   owner's act under point 3.

## 10. Epistemic limits (binding on all outputs)

1. **The Roif hold** (§9) governs every output's
   circulation, whatever the verdict.
2. **No meaning conclusion.** Even a SUPPORTED
   outcome establishes only that a distribution
   fits the border story. It does not establish
   that the sign *meant* border enforcement or
   guild authority — the design's own limit,
   carried into §6's wordings.
3. **The case-ending role is not falsified by
   distribution.** The border reading and the
   recorded CASE_MARKER_SUFFIX role could both
   be true, or neither. This spec scores both
   predictions (§§5.2, 5.3) and reports the two
   scores separately; a verdict for one is not a
   verdict against the other, except where
   §5.4's SIZE-ONLY clause fires — and that
   clause states a distributional preference,
   not a disproof of either gloss.
4. **The claim's frozen record stands.** The
   Phase-104 UNTESTED record is a record of its
   own act. This spec's outcome appends to the
   claim
   `indus_valley_script_deciphered_from_myth_65ff0a26_manual_003`
   as a dated entry beside it; nothing is edited
   or re-adjudicated. Design D-09's claim
   (`manual_001`, Spec 047) is a different claim
   and is untouched by anything this spec finds.
5. **Phase-147 is not evidence here.** The
   earlier internal validation of other Roif
   renderings neither supports nor undermines
   this test and may not be cited in its outputs
   as bearing on the arrow sign.
6. Negative, inconclusive, thin, and
   closed-at-gate outcomes publish (internally,
   under §9) with the same prominence as a
   supported one.

## 11. Risks and honest weaknesses

- **The gateway/border class may be empty or
  thin.** The Indus literature's functional
  statements may class few spine sites as
  gateway/border, and fewer still may carry the
  sign. The gate-0.6 floor exists because this
  design may honestly close unrun; if it runs,
  the border class is small by construction of
  the surviving record, and every count shows
  it.
- **A quarter of the sign sits outside the
  test.** On the present record, 28 of 193
  occurrences (Dholavira, Chanhu-daro,
  Rakhigarhi) are at non-spine sites and cannot
  enter (§5.1). Dholavira in particular is one
  of the great centres the city reading points
  to; its exclusion is a property of the asset's
  universe, stated wherever the verdict is
  stated, not a detail.
- **The administrative operationalisation of
  "great-city" is a translation** (§4.2). If
  Asset B classes a great centre as
  `mixed/unknown`, that centre leaves the test
  entirely; R_city then compares the border
  class against whichever administrative sites
  survive — a narrower comparison than the
  design's words suggest, and the outcome record
  names the sites on both sides so the narrowing
  is visible.
- **Shares at the smallest sites are
  load-bearing.** With nine recorded M391 sites
  before exclusions, each surviving site's share
  matters; the permutation machinery prices
  that, and the per-site table (§8) shows it.
- **The counting layer is database-held.** Its
  identity is fixed at step 0 by export and
  digest (gate 0.4), not at draft; a freeze that
  wants a file-pinned layer instead must say so
  openly and name the file.

## 12. Stop conditions and outcome classes

Execution ends in exactly one of:

- **INVALID** — a §2 hash mismatches (0.1); the
  Asset B digest mismatches the freeze pin
  (0.2, §6 wording); Asset B's form fails the
  contract (0.3); the counting layer cannot be
  pinned or the §1 census does not reproduce
  (0.4); or the join census cannot account for
  every record exactly once (0.5).
- **NOT-RUN (dependency closure)** — Asset B has
  not frozen, or has been shown unsound
  (gate 0.2, §6 wording).
- **INCONCLUSIVE (classification)** — the
  gate-0.6 floors fire. Asset B stands frozen;
  the classification and census are the finding.
- **SUPPORTED**, **NOT SUPPORTED**, or
  **INCONCLUSIVE (measures)** — per §5.4, after
  all gates pass.

## 13. Execution shape (gated; NOT run by this draft)

1. **Graph-first build** (H15/H23) — script,
   graph node, registration, verification.
2. **Step 0** (§3) — input integrity, Asset B
   digest and form, counting-layer pin and
   census reproduction, join census,
   test-population census and floors.
3. **Primary** (§§5.2–5.4) — per-site shares,
   R, permutation test, R_city, the rival score,
   verdict by the frozen partition.
4. **Outcome** (§§6, 8, 9) — appended records
   only, held under the Roif gate; anchors
   asserted byte-identical; foundation check
   reported as measured.

## 14. What this spec is not

Not a build or re-derivation of Asset B (that is
Spec 047's step 1), not a test of Roif's ledger
thesis (that is Spec 047, on a different claim),
not a decipherment of the arrow sign, not a new
corpus, not a period assignment, not a second
classification of any site for any purpose, not
a publication of anything (§9), and not an
authorisation to execute. It is the clustering
test the claim's own falsifier states, run
against the one frozen classification both Roif
distribution tests share, designed so that its
honest outcomes — including closing at its own
gates — are written down before any share is
computed.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
