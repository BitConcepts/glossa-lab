# Spec 047 — Roif's Ledger Thesis: the Distribution Test (Design D-09)

> ## FROZEN — 2026-10-21
>
> Frozen at the freeze act of 2026-10-21 under
> the runnable-experiments campaign plan approved
> by the owner as written on 2026-10-21 (the
> campaign's Wave 2 freeze wave; campaign
> decision E-1 covers this spec's OSF contract
> registration, filed at this freeze —
> `osf-spec-registration.md`). The OPEN items of
> `adjudication.md` §5 are resolved on the
> record in `adjudication.md` §7 (DD-047-8 to
> DD-047-16); DD-047-1 and DD-047-2 are confirmed
> as drafted. The AEE lifecycle hooks ran over
> the register before this freeze
> (`aee/freeze-aee-note.md`), and the digest in
> `freeze.json` was computed exactly once over
> the frozen contract. Execution is
> **Phase-406**, run under this frozen contract
> only after the freeze has merged, the OSF
> registration's approval act has completed, and
> a separate execution order is given. At the
> freeze itself no site has been classified, no
> ledger-sign list has been extracted, and no
> inscription has been counted by site class.
>
> This spec builds Asset B — the site-function
> classification — inside its step 1 (campaign
> E-6). Section 4 is the asset's contract,
> written for the D-10 specification to be
> drafted against: the D-10 specification will
> pin Asset B's frozen digest at its own freeze.
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
> "executed — held under the Roif gate" (§10,
> §11 limit 1). The OSF registration filed at
> this freeze carries this frozen contract (a
> design text) only; it carries no result, and
> filing it clears nothing under the gate.

**Design source:** D-09 in the experiment-design
packet at PR #195
(`docs/research/experiment-designs-2026-10-13/02-roif-and-hunt.md`,
§D-09, read in full at this draft).

**Claim under test:**
`indus_valley_script_deciphered_from_myth_65ff0a26_manual_001`
— Roif's ledger thesis — standing **UNTESTED**:
Phase-104 found its stated test could not run
because the corpus carries site names but no
classification of sites by function (rule
RULE-SITE). This spec builds that classification
as cited data and runs the test the claim's own
record proposes.

**AI disclosure:** this specification is produced by an
AI agent (Muse Spark, via Muse) at the
direction of Tristen Pierson, per constitution
§VI.

---

## 1. The claim and the record it stands on

Roif's thesis bundles three components:

1. **the script is an economic ledger** — a
   notation for administration and trade;
2. **it served guild authority**;
3. **it was influenced by Akkadian practice**.

Only the first component makes a prediction this
program can test with data in hand: if the signs
are a ledger notation for administration and
trade, inscriptions and the ledger-candidate
sign classes should cluster at administrative,
trade, and gateway sites rather than domestic or
purely ritual ones. This spec tests **that
component only, and says so everywhere the
result is stated.** The guild-authority component
is an interpretation layered on the distribution,
not a separate measurement; the Akkadian-influence
component would need contact evidence the program
does not hold. Both are carried through this spec
as explicitly **not tested** (§11, limit 2).

The claim's record (Phase-104 evaluation,
`glossa-indus/reports/phase104_claims_evaluation.json`,
SHA-256 `2d0b83e8…`): verdict *stays untested*,
rule **RULE-SITE** — "Falsification condition
requires site-typology data (gateway/border,
fire-altar, palatial/royal, or trade-context
classification of excavation sites); no such
dataset exists in the repo — the Holdat corpus
carries site names only." The program's internal
hypothesis-model file
(`glossa-indus/hypotheses/models/roif_guild_ledger.yaml`)
records the same thesis and its planned
site-context tests as *pending data*. An earlier
internal validation (Phase-147) scored other
renderings of Roif's model; it did not run this
distribution test, it is not evidence for or
against this claim's distribution component, and
no output of this spec may cite it as such
(§11, limit 5).

### 1.1 The question, in plain words

Do inscriptions — and the signs Roif's text names
as ledger notation — turn up at the sites that
administered, traded, and controlled passage,
more than those sites' share of the map would
predict, once site size is handled by comparing
shares rather than raw counts? The missing piece
was never the inscriptions; it was a defensible,
frozen answer to "what kind of site is each
site?" — built from the excavation literature,
not from the inscriptions themselves. Step 1 of
this spec builds exactly that (§4), and the
build is a deliverable in its own right: it is
**Asset B**, shared with design D-10.

### 1.2 The hypothesis and its falsifier

**Hypothesis** (the claim's distribution
component, restated). Inscription density and
the ledger-candidate sign classes concentrate
at sites classed as administrative / trade /
gateway, beyond what site size predicts.

**Falsifier.** The hypothesis fails if, with
site size controlled by the shares design of
§6, the administrative/trade/gateway class
shows no excess over domestic/ritual sites —
the outcome the claim's own record states as
its failure condition. §6.3 turns this into a
mechanical verdict partition fixed before any
count exists; §7 pre-writes the wording of
every outcome in that partition.

## 2. Inputs (pinned at draft; re-asserted at the freeze)

| Input | Pin / state |
|---|---|
| Gazetteer spine (`data/movement/gazetteer_rows.jsonl`) — Spec 027 Stage 0 | SHA-256 `5ac76a3031121a61fa39f87b1d2760855374d171ddd036988fee2820dca9b8b6` (recomputed at this draft from `main` at `82b29490`, the head when drafting began; the branch as pushed sits on `83b6a563`, PR #241 having merged in between — every §2 pin was re-verified identical at both heads, see adjudication.md §2); 36 source-assertion rows, **30 distinct `program_site_id` clusters** (both counts read at this draft) |
| Primary corpus layer (`backend/glossa_lab/data/yajnadevam_inscriptions.csv`) — the site-attributed layer of Specs 027/028, 5,679 records, with `site` and sign-sequence columns as held | SHA-256 `c02e3d7bb74cf5abb11cc94f88d8d469e6acc5d6fad4b7153c02c43428f58d98` (recomputed at this draft from the git blob; the same pin Spec 042's draft carries) |
| Sign crosswalk (`data/crosswalks/yajnadevam_to_parpola_crosswalk.csv`) — the mapping route from the primary layer's sign numbering to published sign identities, used only by the §5 ledger-list mapping | SHA-256 `e44b8b550155e3d071e7fc5f94e8c98e9755de437c99e2f5027e3d647b2950a2` (recomputed at this draft; corrected — see adjudication.md §2) |
| Phase-104 claims evaluation (`glossa-indus/reports/phase104_claims_evaluation.json`) — the claim's UNTESTED / RULE-SITE record | SHA-256 `2d0b83e8055a04b96635007054cfadde472f605dc7e5b249a61c8f9ea89b858d` (recomputed at this draft; corrected — see adjudication.md §2) |
| Citation record (`backend/scripts/seed_citations.py`, key `roif_indus_ledger`) — the program's citation of record for Roif's work: "Roif, A.", venue Academia.edu, year field empty, DOI empty, and the URL field carrying only the Academia.edu root — no document-level identifier | SHA-256 `39d28112e21151ccba0f5a370801c78d87575c6ff61695bb8fafc5c14c08b8f9` (recomputed at this draft; key read at this draft; corrected — see adjudication.md §2) |
| Roif hypothesis-model file (`glossa-indus/hypotheses/models/roif_guild_ledger.yaml`) — background only (see §2.2 defect note) | SHA-256 `c5f08461cc1a37b91cb5a17981e2e4d7c02958312e1e7b6b9a49618a154c9586` (recomputed at this draft) |
| Anchors file (`backend/reports/INDUS_FINAL_ANCHORS.json`) | SHA-256 `df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569` (recomputed at this draft). This spec moves no anchor; the file is asserted byte-identical before and after any execution. |

**Explicitly not an input:**
`data/movement/gazetteer_rows_assigned.jsonl`
(Spec 039's period-assignment product). A period
label is not a site function; nothing in Asset B
or in the test reads it.

**Freeze re-assertion (2026-10-21).** Every pin
in the table above was re-derived at the freeze
by two independent routes — the contents-API
raw route and the git-blob route, both at the
merged record (`main` at `83b6a563`) — and the
two routes agree byte-for-byte on every file,
with every hash equal to its pin (the full
record, including the Spec 027 spec pin
`7fff5d5a…` carried in the register's
evidence, is in `freeze.md` §2). The freeze
verifies the pins in exactly the two-route form
this spec's drafting required after its pin
incident (`adjudication.md` §2).

### 2.1 The Roif source of record for the §5 extraction

The program's held manuscript PDF of Roif's work
does not survive: it appears in the 2026-10-08
history-purge scope lists, and the verification
of 2026-10-21
(`~/workspace/research_notes/roif-preprint-check-2026-10-21.md`)
found no copy in any current checkout or
preserved backup. The verification establishes
that the identical-titled work is publicly
posted, in full, and citable:

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

These two postings are the **source of record**
for the §5 ledger-sign extraction (DD-047-3).
Academia.edu mints no DOIs; the URLs above are
the citable identifiers. Any later publication
of this spec's results cites Roif in this form
and remains a separate owner GATE act (§10).

### 2.2 Defect noted at draft (recorded, not repaired)

The hypothesis-model file's source metadata is
not reliable: its `document_id` is malformed
(it carries a stray quotation mark), and its
`doi` field carries a value that matches
neither Academia.edu posting (which have no
DOIs). This draft therefore cites that file for
nothing except the existence of the program's
earlier planned tests, and the §5 extraction
never reads it. The defect is recorded here and
in `adjudication.md`; repairing the file is not
part of this spec.

## 3. Step 0 — gates before anything is built or counted (fail-closed)

Execution runs these checks in order, before
Asset B's build begins. A failure stops the
execution in the class named; nothing is
repaired at run time.

- **0.1 Input integrity.** Every §2 input hashes
  to its freeze-record value. A mismatch stops
  the run as **INVALID**.
- **0.2 Spine reproduction.** The pinned
  gazetteer file reproduces exactly: 36 rows,
  30 distinct `program_site_id` clusters, the
  cluster list as frozen. A mismatch stops the
  run as **INVALID**.
- **0.3 Corpus join census (counts of records,
  not of signs).** Every record of the primary
  layer is accounted for in exactly one of:
  (a) *joined* — its `site` value, normalised
  by the rule in §6.1, equals a spine cluster's
  normalised name; (b) *non-spine site* — its
  site is not a spine cluster (listed, with its
  record count); (c) *no site value* (counted).
  The census is published with the outcome
  either way. A record that cannot be placed in
  exactly one class stops the run as
  **INVALID** — no record is silently dropped
  or hand-assigned to a site.

## 4. Asset B — the site-function classification (step 1; the contract)

This section is Asset B's contract. It is
written so that the D-10 specification can be
drafted against it without re-deciding any of
it, and so that the freeze of this spec can pin
the built asset by digest (campaign E-6, R-2).

### 4.1 Spine and unit

- The asset's universe is the **30 site
  clusters** of the Spec 027 Stage 0 gazetteer
  (§2 pin): one asset row per
  `program_site_id`, no more, no fewer. Corpus
  sites that are not spine clusters are outside
  the asset by rule (§3, gate 0.3 class (b));
  the asset never extends the spine.
- Each row classifies the **site**, not any
  source-assertion row: the gazetteer's 36 rows
  collapse to their 30 clusters for this asset,
  and the clustering of record is the
  gazetteer's own.
- The asset file is
  `specs/047-roif-ledger-distribution/asset-b/site-functions.jsonl`:
  one JSON object per cluster, rows sorted by
  `program_site_id`, fields exactly:
  `program_site_id`, `site_name_as_published`,
  `status`, `primary_class`, `source_a`,
  `source_b`, `notes`. Each of `source_a` /
  `source_b` is either null or an object with
  exactly: `citation`, `locator`,
  `stated_function`, `mapped_class`.

### 4.2 Function vocabulary (closed; six classes)

Every classification uses exactly these six
classes. A class is assigned from what a
published source **states about the site's
primary function**, mapped by the rule in the
right-hand column — never from inscription
content, inscription counts, or this program's
expectations (§4.5).

| Class | A published statement maps here when it describes the site's primary function as… |
|---|---|
| `gateway/border` | controlling or taxing passage — a border, river-crossing, pass, or route node where movement of goods or people was checked |
| `administrative` | a seat of administration or governance — central storage, redistribution, record-keeping, or civic authority exercised for a wider area |
| `port/trade` | a port, harbour, or trading station whose primary role is exchange — maritime or overland |
| `domestic` | a primarily residential settlement, with no specialised primary function stated |
| `ritual` | a primarily ceremonial or ritual centre |
| `mixed/unknown` | several co-primary functions with none stated as primary, or the site's function not stated in the source |

Two derived groupings, fixed here for the test
and for D-10's use: the **pooled class**
`ADMIN-TRADE-GATEWAY` = {`gateway/border`,
`administrative`, `port/trade`}; the **contrast
class** = {`domestic`, `ritual`}. `mixed/unknown`
belongs to neither and never enters the primary
test (§4.4).

### 4.3 The two-source agreement rule (mechanics)

For each cluster, the build seeks **two
independent published sources** from the
excavation and site literature:

- **Published** means a publication of record:
  an excavation report, a site monograph, or a
  peer-reviewed synthesis that states the site's
  function in its own words. Each entry carries
  its `citation` and a `locator` (page, chapter,
  or section) precise enough for a reader to
  find the statement.
- **Independent** means the two sources are
  distinct works by distinct authors or editors,
  and neither's function statement for this site
  merely repeats the other's. A reprint, or a
  textbook passage citing the same excavation
  report as its sole basis for the statement,
  does not count as a second source.
- Each source's statement is first mapped to
  the §4.2 vocabulary **on its own**
  (`mapped_class`), from the statement alone.
  A statement that names several functions with
  none primary maps to `mixed/unknown`.
- **Agreement:** if both sources exist and
  their `mapped_class` values are identical,
  the row's `status` is `AGREED`, and
  `primary_class` is that class. A row is
  **testable** iff it is `AGREED` and its class
  is one of the five non-`mixed/unknown`
  classes.

The mapping is done by the build worker from
the statements, and a second worker (or a
second pass by a worker who has not seen the
first mapping) verifies each `AGREED` row's
two citations actually state the function
mapped. A verification failure on any row
demotes that row under §4.4 before the freeze;
it is never repaired by re-reading a source
more favourably.

### 4.4 Dispute handling (by rule, never by judgement after the fact)

Every non-testable cluster is listed in the
asset by name, with its citations, in exactly
one of these statuses:

- `DISAGREED` — two independent sources exist
  and map to different classes. Both citations
  and both mapped classes are recorded.
- `SINGLE-SOURCE` — only one admissible
  published source was found. It is recorded;
  the row is still excluded.
- `NO-SOURCE` — no admissible published source
  stating the site's function was found. The
  search is recorded in `notes` (works
  consulted), so the absence is checkable.
- `AGREED` with `primary_class` =
  `mixed/unknown` — the sources agree the
  function is mixed or unstated. Recorded;
  excluded from the primary test by §4.2.

There is **no tiebreak**: no third source is
sought to break a disagreement, no majority
rule applies (there are exactly two sources),
and no worker adjudicates between sources.
Disagreement is a recorded property of the
literature, published with the asset in full —
for a thin classification outcome (§6.3), the
disagreement list **is** the finding.

### 4.5 Circularity and blindness (build discipline)

- Site classes come from the excavation
  literature only. No class, mapping, or
  status may be derived from inscription
  content, sign distributions, or per-site
  inscription counts.
- The build is carried out **without consulting
  the primary layer's per-site counts**: the
  join census of gate 0.3 counts records for
  accounting only, is computed by the machinery
  separately from the classification work, and
  its per-site figures are not available to the
  classification worker before the freeze.
- The build record carries a dated attestation
  of both points, naming the worker (agent or
  human) who entered the classifications.

### 4.6 Freeze point and digest pinning

- Asset B **freezes inside this spec's step 1**,
  before any step-2 counting of any kind — in
  particular before the §6 measures, before the
  §5 ledger list is joined to any count, and
  before D-10 or any other consumer reads a
  class for a test.
- The freeze act for Asset B consists of: the
  asset file committed in the form of §4.1;
  its **SHA-256 digest computed over the file
  bytes as committed** and recorded, with the
  row count (30), the testable count, and the
  per-status counts, in this spec's freeze
  record (`freeze.md` / `freeze.json`) and
  repeated in the step-1 outcome record; and
  the §4.5 attestation.
- **Dependents pin the digest.** The D-10 specification
  names Asset B by this digest in its
  own §2 inputs and re-asserts it at its step
  0; a mismatch at any consumer's step 0 stops
  that consumer as INVALID. "The same
  classification" is thereby a verifiable fact,
  not an intention (campaign R-2).
- After the freeze, the asset file changes
  only by dated, append-only errata that do
  not change any row's status or class. Any
  change to a status or class — including the
  discovery that a citation does not state what
  the row claims — makes the frozen asset
  **unsound**: the campaign cluster tripwire
  fires, this spec and its dependents close as
  not-run (dependency closure), and a corrected
  asset requires a successor spec. The asset is
  never quietly edited and re-digested inside
  this campaign.

### 4.7 Asset B build gates (fail-closed)

The build stops, the asset does **not** freeze,
and this spec closes at step 1 (wording §7) if
any of these fails:

- **B1 Coverage.** The asset carries exactly
  30 rows, one per spine cluster. A missing or
  extra row is a build failure, not an
  exclusion.
- **B2 Citation completeness.** Every `AGREED`
  row carries two sources, each with citation,
  locator, stated function, and mapped class;
  every non-`AGREED` row carries the record its
  §4.4 status requires. A row that cannot be
  completed is recorded under the status its
  evidence supports — if no status fits the
  record, the build fails.
- **B3 Verification.** The §4.3 citation
  verification passes for every `AGREED` row
  (after any demotions, which are themselves
  recorded in the asset's `notes`).
- **B4 Circularity.** The §4.5 attestation can
  be made truthfully. If inscription content or
  counts influenced any classification, the
  build fails; the influence is recorded, not
  laundered by re-entry.

A build failure is a statement about the build,
not about Roif's claim, and the outcome record
says so. Note what is **not** a build gate: the
*number* of testable sites. A honestly built
asset with few testable sites still freezes;
its thinness is adjudicated by the test gate
in §6.3, where the design puts it (DD-047-1).

## 5. The ledger-sign list (step 1, frozen with Asset B)

Measure (b) of §6 needs the sign classes Roif's
text names as ledger notation. The list is
built in step 1, before counting, as follows:

- **Source.** The two Academia.edu postings of
  §2.1, and nothing else — not the program's
  model file (§2.2), not Phase-147, not any
  summary.
- **Extraction rule.** A depicted sign or sign
  class enters the list iff Roif's text
  explicitly assigns it an economic function —
  trade, tribute, storage, accounting, guild,
  enforcement, or maritime trade — in a sign
  table or a case reading. Each entry records:
  the sign as Roif names or depicts it, the
  function his text assigns, a locator in the
  posting (section or table), and the mapped
  sign identifier(s) in the primary layer's
  numbering, mapped through the pinned §2
  crosswalk and the canonical sign registry.
- **Unmapped entries.** A named sign that
  cannot be mapped to the layer's numbering by
  the crosswalk or the registry is recorded as
  `UNMAPPED` and excluded from counting by
  rule. The extraction census — entries sought,
  entered, unmapped — is published with the
  outcome. If **no** entry maps, measure (b)
  cannot run. **Ruled at the freeze
  (DD-047-13):** the execution then proceeds on
  measure (a) alone — the SUPPORTED criterion's
  ledger clause is vacated for that run only,
  the vacated clause is stated openly in the
  outcome record beside the verdict, and the
  extraction census is published with the
  outcome as the reason (§6.3 carries the
  amended partition for that case). The case is
  never silently absorbed.
- **Freeze.** The list is committed as
  `specs/047-roif-ledger-distribution/asset-b/ledger-signs.jsonl`
  and frozen in the same step-1 freeze act as
  Asset B, with its own SHA-256 digest recorded
  alongside Asset B's. Extraction is done
  without consulting sign counts (§4.5 applies
  with the necessary changes).

## 6. Step 2 — the distribution test

### 6.1 Population and join

The test population is the set of **testable
sites** (§4.3) that carry at least one joined
inscription in the primary layer under gate
0.3's census. Testable sites with no joined
inscription are listed as `NO-CORPUS-COVERAGE`
with the classification counts; they enter
neither share. Site-name normalisation for the
join is mechanical: lowercase, whitespace and
punctuation collapsed, matched against the
gazetteer cluster's normalised name; no fuzzy
matching and no hand assignment (gate 0.3).

### 6.2 Measures (pre-registered)

With the classification and the ledger list
frozen:

- **(a) Inscription share.** The pooled class's
  share of all inscriptions at test-population
  sites, versus the pooled class's share of
  test-population sites. The headline statistic
  is the ratio **R** = (pooled inscription
  share) / (pooled site share). Comparing
  shares, not counts, **is** the size control
  the design specifies: a class holding many
  inscriptions only because it holds many or
  large sites yields R near 1.
- **(b) Ledger-sign share.** The same ratio
  computed over occurrences of the §5 ledger
  signs pooled: **R_ledger** = (pooled class's
  share of all ledger-sign occurrences at
  test-population sites) / (pooled class's
  share of test-population sites). Per-sign
  counts are reported alongside, so no single
  frequent sign carries the pooled figure
  silently.
- **Permutation test.** Site class labels are
  shuffled across the test-population sites
  **9,999 times**; the p-value is the share of
  shuffles whose R is at least the observed R.
  The random seed was fixed at this spec's
  freeze (2026-10-21) at **20261021** and is
  recorded in the freeze record (DD-047-10),
  before any count exists.

### 6.3 Criteria (the verdict partition, fixed in advance)

First, the **classification gate**: if fewer
than **12 sites** are testable (§4.3), or if
either the pooled class or the contrast class
is empty in the test population, the test does
not run and the outcome is **INCONCLUSIVE —
the classification is the finding**, reported
with its full disagreement list (§7). No
distribution quantity is computed in that case.

Otherwise exactly one of:

- **SUPPORTED** (bounded to the distribution
  component) iff R ≥ 1.5 **and** the permutation
  test rejects at the 5% level (p < 0.05)
  **and** the ledger-sign classes show the same
  direction (R_ledger > 1.0).
- **NOT SUPPORTED** iff R ≤ 1.0, **or** the
  permutation test does not reject (p ≥ 0.05)
  while R > 1.0 is the only clause in question —
  the design's own failure condition: no excess
  once size is controlled, or no excess the
  shuffling test can distinguish from chance.
- **INCONCLUSIVE** in every remaining case:
  1.0 < R < 1.5; or R ≥ 1.5 with p < 0.05 but
  R_ledger ≤ 1.0 (the two pre-registered
  measures disagree).

The partition is exhaustive and mechanical:
every (R, p, R_ledger) triple lands in exactly
one outcome, assigned from the recorded
quantities by any reader.

**The all-UNMAPPED case (DD-047-13).** If the
§5 extraction maps no entry, R_ledger is not
computed and the partition runs on (R, p)
alone: SUPPORTED iff R ≥ 1.5 and p < 0.05;
NOT SUPPORTED iff R ≤ 1.0 or p ≥ 0.05;
INCONCLUSIVE in every remaining case. The
outcome record states that the ledger clause
was vacated under this ruling and publishes
the extraction census as the reason.

### 6.4 Sensitivities (reported; never verdict-changing)

- **Each source alone.** The test recomputed
  under source A's classes alone, then source
  B's alone (each source's testable set being
  the sites that source maps to a
  non-`mixed/unknown` class), reported beside
  the primary.
- **Five largest sites.** Measures (a) and (b)
  recomputed descriptively over the classes of
  the five test-population sites with the most
  joined inscriptions, as the design's check on
  excavation and publication bias.
- **Exclusions restated.** The `DISAGREED`,
  `SINGLE-SOURCE`, `NO-SOURCE`, `mixed/unknown`,
  and `NO-CORPUS-COVERAGE` lists are republished
  with the outcome, so a reader can see exactly
  which sites the verdict does not cover.

## 7. Pre-written verdict wordings

The outcome record's headline paragraph uses
one of these forms, with the bracketed
quantities filled from the run. Under the Roif
gate these wordings appear in internal records
only (§10).

- SUPPORTED: "Checked for its distribution
  component only, Roif's ledger thesis is
  SUPPORTED: sites classed administrative,
  trade, or gateway in the frozen site-function
  classification (Asset B, digest [d]) carry
  [x]% of the inscriptions at testable sites
  against [y]% of the testable sites (ratio
  [R]), a concentration the label-shuffling
  test distinguishes from chance (p = [p],
  9,999 shuffles), and the sign classes Roif's
  text names as ledger notation show the same
  direction (ratio [R_ledger]). This supports
  the distribution component only. It does not
  establish that any inscription is a ledger
  entry, that guilds existed as Roif describes,
  or anything about Akkadian influence; the
  guild-authority and Akkadian components of
  the thesis remain untested."
- NOT SUPPORTED: "Checked for its distribution
  component only, Roif's ledger thesis is NOT
  SUPPORTED: with site size controlled by
  shares, the administrative/trade/gateway
  class shows no excess over domestic and
  ritual sites (ratio [R]; permutation p =
  [p]). The falsifier the claim's own record
  states has fired for the distribution
  component. The guild-authority and
  Akkadian-influence components remain
  untested, and this outcome says nothing
  about them either way."
- INCONCLUSIVE (measures): "Checked for its
  distribution component only, Roif's ledger
  thesis is INCONCLUSIVE: [the ratio [R] falls
  between the pre-registered bounds / the
  inscription share and the ledger-sign share
  point in different directions (R = [R],
  R_ledger = [R_ledger])]. The claim's
  distribution component stands neither
  supported nor falsified under the frozen
  criteria; the quantities are recorded so the
  inconclusiveness is inspectable."
- INCONCLUSIVE (classification): "The
  distribution test did not run: [n] of the
  gazetteer's 30 sites survived the two-source
  agreement rule as testable (floor 12), [or:
  one side of the comparison is empty in the
  test population]. The finding of this
  execution is the classification itself
  (Asset B, digest [d]): [status counts], with
  the disagreed and unclassifiable sites named
  in full. No distribution quantity was
  computed. The claim stands UNTESTED for its
  distribution component, now with the reason
  measured rather than asserted."
- CLOSED AT STEP 1: "The site-function
  classification could not be built as
  specified: gate [B1/B2/B3/B4] failed
  ([observed values]). Asset B did not freeze,
  no distribution quantity was computed, and
  the dependent design D-10 is not-run by
  dependency closure. This is a statement
  about the build, not about Roif's claim,
  which stands UNTESTED."
- INVALID: "The execution stopped at step 0,
  gate [0.1/0.2/0.3]: [observed values]. No
  classification was built and no quantity was
  computed. The claim stands UNTESTED."

## 8. Controls and named confounders

- **Excavation and publication bias.** Big,
  famous sites are more dug and more published,
  in both the corpus and the classification
  literature. The shares-not-counts design and
  the size control address corpus volume; the
  five-largest sensitivity (§6.4) exposes the
  classification side; neither is claimed to
  eliminate the bias, and the outcome wording
  carries the caveat.
- **Classification contestability.** Site
  function is a judgement the literature itself
  disputes. The two-source rule (§4.3), the
  no-tiebreak dispute handling (§4.4), and the
  each-source-alone sensitivity (§6.4) are the
  controls; the disagreement list is published,
  not averaged away.
- **Circularity.** Classes come from the
  excavation literature, never from inscription
  content (§4.5). A classification derived from
  the inscriptions could not then test the
  inscriptions' distribution; the build gates
  exist to keep that failure impossible rather
  than unlikely.
- **Spine coverage.** The gazetteer spine is
  the design's chosen universe, and it is not
  the corpus's universe: corpus sites absent
  from the spine (gate 0.3 class (b)) cannot
  enter the test, however many inscriptions
  they carry. The verdict is a statement about
  the spine's testable sites, and §10 requires
  every product to say so.
- **One corpus layer.** The primary test runs
  on the pinned primary layer; its lineage
  posture is as recorded in Specs 027/028.
  **Ruled at the freeze (DD-047-9):** no second
  site-attributed layer runs under this
  contract — not as a co-primary and not as a
  sensitivity. The pinned layer of §2 is the
  sole verdict-bearing corpus; the draft does
  not silently pluralise the design's "corpus
  layers" into two verdict-bearing runs, and
  the freeze does not either. A second-layer
  comparison is a successor act outside this
  campaign.

## 9. Reporting obligations

Every product of an execution carries, in its
headline paragraph:

1. the corpus label — the primary layer as
   pinned in §2, with its lineage posture as
   recorded in Specs 027/028;
2. the Asset B digest, the testable count, and
   the per-status counts of §4.4;
3. the join census of gate 0.3, including the
   non-spine sites by name with their counts;
4. R, the permutation p-value, R_ledger, and
   the per-sign ledger counts of §6.2;
5. the component fence: "This result concerns
   the distribution component of Roif's ledger
   thesis only; the guild-authority and
   Akkadian-influence components were not
   tested."

Deliverables at execution: the Asset B file
and ledger-sign list (§§4–5, frozen at step 1);
a results JSON (censuses, classification
counts, the primary quantities, permutation
record, sensitivities); a report under these
headline rules; the experiment-graph node
(H15/H23, registered and verified before the
run); the outcome append in this directory;
and the LEDGER entry (H1). Foundation check
(H21) after the execution phase: 0 failures,
or the outcome record says why not. Anchors
asserted byte-identical before and after.

## 10. The Roif gate (binding on every output)

1. **Held, not surfaced.** This spec's
   execution records, results JSON, report,
   and outcome append are internal program
   records. No summary, article draft, paper
   text, website text, or public register
   wording derived from them is produced by
   this spec or by the campaign.
2. **Reporting form.** Campaign and status
   reporting names this member only as
   **"executed — held under the Roif gate"**,
   with no result content, until the gate
   clears.
3. **Clearing the gate** requires both: the
   verification of 2026-10-21 standing on
   record (it does: Roif's work is publicly
   posted and citable, §2.1), **and** the
   owner clearing the specific publication act
   as its own GATE decision, with the §2.1
   citations carried in the published text.
   The verification alone clears nothing; this
   spec's freeze and execution clear nothing.
4. The daily-article process and every other
   public surface are barred from drawing on
   this spec's results absolutely, until the
   owner's act under point 3.

## 11. Epistemic limits (binding on all outputs)

1. **The Roif hold** (§10) governs every
   output's circulation, whatever the verdict.
2. **One component of three.** Even a SUPPORTED
   outcome checks the distribution component
   only. The guild-authority and
   Akkadian-influence components remain
   untested sub-claims, carried as such in the
   claim's record — never swept into this
   spec's verdict word.
3. **No ledger-entry conclusion.** A
   distribution that fits the ledger story does
   not establish that any inscription is a
   ledger entry, that guilds existed as Roif
   describes, or anything about Akkadian
   influence — the design's own limit, carried
   verbatim into §7's wordings.
4. **The claim's frozen record stands.** The
   Phase-104 UNTESTED record is a record of its
   own act. This spec's outcome appends to the
   claim
   `indus_valley_script_deciphered_from_myth_65ff0a26_manual_001`
   as a dated entry beside it; nothing is
   edited or re-adjudicated.
5. **Phase-147 is not evidence here.** The
   earlier internal validation of other Roif
   renderings neither supports nor undermines
   this test and may not be cited in its
   outputs as bearing on the distribution
   component.
6. Negative, inconclusive, thin, and
   closed-at-gate outcomes publish (internally,
   under §10) with the same prominence as a
   supported one.

## 12. Risks and honest weaknesses

- **The classification may honestly come out
  thin.** The Indus literature's site-function
  statements are uneven; if fewer than 12 of
  30 clusters survive two-source agreement, the
  execution's finding is the classification and
  its disagreements (§6.3). That outcome was
  designed in, not discovered.
- **The spine is small and partial.** Thirty
  clusters, of which only the testable subset
  with corpus coverage carries the test; major
  corpus sites outside the spine cannot
  contribute (§8). The verdict's population is
  correspondingly narrow, and §9 forces every
  product to show it.
- **Function is coarser than the thesis.** A
  site can host administration and domestic
  life at once; the primary-function rule
  (§4.2) forces one class per site because the
  design's test needs one, and `mixed/unknown`
  is where honest multiplicity goes — at the
  price of excluding those sites.
- **The ledger list depends on one author's
  text.** The extraction rule (§5) is mechanical,
  but the underlying naming is Roif's; a sign he
  does not name cannot enter measure (b),
  however ledger-like it looks to this program.

## 13. Stop conditions and outcome classes

Execution ends in exactly one of:

- **INVALID** — a §2 hash mismatches (0.1);
  the spine does not reproduce (0.2); or the
  join census cannot account for every record
  exactly once (0.3).
- **CLOSED AT STEP 1** — an Asset B build gate
  (§4.7) fails. The asset does not freeze;
  D-10 closes not-run by dependency closure.
- **INCONCLUSIVE (classification)** — the
  §6.3 classification gate fires. Asset B
  freezes; the classification is the finding.
- **SUPPORTED**, **NOT SUPPORTED**, or
  **INCONCLUSIVE (measures)** — per §6.3,
  after all gates pass.

## 14. Execution shape (gated; NOT run by this draft)

1. **Graph-first build** (H15/H23) — script,
   graph node, registration, verification.
2. **Step 0** (§3) — integrity, spine
   reproduction, join census.
3. **Step 1a — Asset B build** (§4) — cited-data
   entry under the two-source rule, verification
   pass, build gates, freeze with digest.
4. **Step 1b — Ledger-sign list** (§5) —
   extraction, mapping, freeze in the same act.
5. **Step 2** (§6) — classification gate, then
   the primary measures, permutation test, and
   sensitivities.
6. **Outcome** (§§7, 9, 10) — appended records
   only, held under the Roif gate; anchors
   asserted byte-identical; foundation check
   reported as measured.

## 15. What this spec is not

Not a test of Roif's thesis as a whole (two of
its three components are explicitly untested
here), not a decipherment, not a new corpus,
not a period assignment (Spec 039's product is
not read), not a site-function classification
for any purpose beyond this campaign's two
consumers (this test and D-10) without its own
act, not a publication of anything (§10), and
not an authorisation to execute. It is the
distribution test the claim's own record
proposed, plus the shared classification that
test always needed, designed so that its honest
outcomes — including closing at its own gates —
are written down before any site is classified
or any inscription is counted.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
