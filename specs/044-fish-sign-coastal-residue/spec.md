# Spec 044 — The Fish Sign and the Ports, Tested Sign by Sign (Design D-02, Residue)

> ## FROZEN — 2026-10-21
>
> Frozen under the runnable-experiments campaign
> plan approved by the owner AS WRITTEN on
> 2026-10-21 (Wave 2 freeze wave, delegated;
> `adjudication.md` §7). The AEE lifecycle hooks
> ran over the register first (register recovered
> to 0.7-draft; `aee/freeze-aee-note.md`), and the
> digest in `freeze.json` was then computed
> **exactly once** over the recovered register
> and the finalised freeze texts. The freeze
> resolved OPEN-044-1…6 (layer of record
> identified and pinned; Asset F source, coastal
> scope, and test form confirmed; OSF contract
> registration filed under campaign E-1;
> `adjudication.md` §7) and corrected the draft's
> consumer name: Asset F's consumer is
> **Spec 048** (design D-04), not Spec 045
> (§7.1). Execution runs as **Phase-404** under
> this frozen contract, after the freeze merges
> and the OSF registration's approval verifies.
> At the freeze itself no sign has been counted,
> Asset F has not been built, and no coastal list
> has been enumerated beyond the two sites the
> record itself names.
>
> **Roif gate (campaign Part 8 / R-7).** This is
> a Roif-claim experiment. Post-plan verification
> (2026-10-21) established that Roif's preprint
> IS publicly posted on Academia.edu and citable
> — but publication of this experiment's results
> remains a standing GATE for the owner. Records
> under this spec are internal; nothing is
> published or surfaced from this spec's results
> under this campaign; reporting names this
> member only as "executed — held under the Roif
> gate" (§7, limit 1; claim F044-C14).

**Design source:** D-02 in the experiment-design
packet at PR #195
(`docs/research/experiment-designs-2026-10-13/02-roif-and-hunt.md`,
§D-02, read in full at this draft), with the
portfolio triage of 2026-10-21 (design D-02
found RIPE: "The CISI-based layer and the
gazetteer are in hand, and Spec 039 put
published site geography further on record. The
fish-family list it shares with D-04 can be
frozen at its own step 0 from Parpola's
published list; it need not wait for D-04's
freeze.").

**Claim under test:**
`indus_valley_script_deciphered_from_myth_65ff0a26_manual_002`
— "The fish sign encodes a coastal guild
controller or maritime trader identity
(Lothal-linked)" — standing **SETTLED,
partially falsified**: the claim's own
family-level coastal-enrichment test came back
against it. This spec tests only the residue
its not-understood text names.

**AI disclosure:** this draft is produced by an
AI agent (Muse Spark, via Muse) at the
direction of Tristen Pierson, per constitution
§VI.

---

## 1. The claim and the record it stands on

The claim says the fish sign marked coastal
traders. The program counted fish signs across
sites in its CISI-based data and found no
enrichment at coastal sites (Lothal, Dholavira):
the Phase-45 T6 test recorded NO_ENRICHMENT for
the fish sign M047 at coastal sites (n = 13,
p = 0.685, as recorded in the Phase-46 script
header, read at this draft), and the claim's
explanation record states the family-level
result in the same terms. That verdict stands
and is not re-opened by this spec.

The claim's not-understood text names the
residue exactly: "The fish family covers several
distinct signs, and the test treated them
together and used the site types as published
in the CISI data; a finer test, sign by sign and
with better site classifications, has not been
run." A finer test could sharpen the
falsification or find the one member it does
not cover; it cannot quietly resurrect the
family-level claim (§7, limit 2).

### 1.1 The question, in plain words

The family failed together. Did every member
fail, or is one individual fish sign actually
concentrated at coastal sites while its
relatives are not? Test each fish sign on its
own, against the corpus's own coastal base
rate, with the coastal list and the family list
both frozen before anyone counts.

### 1.2 The hypothesis and its falsifier

**Hypothesis (the claim's, restated at sign
level).** At least one individual fish sign is
enriched at coastal/maritime sites relative to
inland sites, at the criterion in §5.

**Falsifier.** No fish sign with at least 30
total occurrences shows coastal enrichment at
the §5 criterion — in which case the partial
falsification is recorded as covering the
family member by member, and the residue
closes.

## 2. Inputs (pinned at this draft where a pin exists; re-asserted at the freeze)

| Input | Pin / state |
|---|---|
| Claim record (`glossa-indus/claims/extracted_claims/indus_valley_script_deciphered_from_myth_65ff0a26.json`) | SHA-256 `bc22d6f010f800d608d6e3f620fb430b3cf8d3ccd3caadc6a989116fbfd125ed` (recomputed at this draft from `main`, head `82b29490…`; re-asserted at the freeze against `main` head `83b6a563…`, unchanged) |
| Spec 027 Stage 0 gazetteer (`data/movement/gazetteer_rows.jsonl`) — 36 rows, 30 site clusters; the site spine for §3 gate 0.3 | SHA-256 `5ac76a3031121a61fa39f87b1d2760855374d171ddd036988fee2820dca9b8b6` (recomputed at this draft; matches the pin Spec 039's spec carries) |
| CISI-based corpus layer of record — the layer the original family-level test used, keyed by CISI object number, carrying per-inscription site attribution, "as held in the database" (design D-02) | **Identified and pinned at the freeze (OPEN-044-1; `adjudication.md` §7.2).** The layer is the Holdat corpus file the Phase-45/46/54 scripts of record read: `corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv`, SHA-256 `62d14d2bebf7c2c80d98a2958e75ec52bff3f240ff3f5e85d1f7f40cbe28218e` (593,253 bytes; 7,002 sign-token rows; 1,670 inscriptions keyed by `cisi_number` over 9 sites). The identification reproduces the original test's population exactly (M047 at 13 tokens in 13 inscriptions; Fisher p = 0.685, the recorded Phase-45 T6 result). The file is a downloads-tree file held by the program, not a repository file on `main`; no bulk copy is committed. Gate 0.1 re-asserts this pin at step 0, before any counting — and the run closes if the re-assertion fails (DD-044-3 as completed by the freeze). The repository's other CISI-derived layers cannot carry a site test (e.g. the 179-inscription, Mohenjo-daro-only CISI corpus) and are not this layer. |
| Parpola's published fish-sign list — the source of Asset F (§4) | Bibliographic pin: Parpola, Asko. 1994. *Deciphering the Indus Script*. Cambridge: CUP — the published sign list (fig. 5.1, pp. 70–78), as cited in the program's own Mahadevan–Parpola crosswalk file (`backend/glossa_lab/data/mahadevan_parpola_crosswalk.json`, SHA-256 `9ebd7723472d888dc8a127ff840a108d4fbd546f7f8ed28ccc6e06444a2dc69b`, recomputed at this draft and re-asserted at the freeze). Per-sign locators within that list are recorded in Asset F itself at step 0 (gate 0.2). The freeze confirmed the edition and locator form (OPEN-044-2; `adjudication.md` §7.3). |
| Spec 039's gazetteer product | Spec 039 assigned published period labels to 11 of 30 gazetteer sites (triage of 2026-10-21). Period is **not** a variable in this test; Spec 039 is cited here only because its record further fixed the gazetteer's published geography on the record. No period label is consumed. |
| Anchors file (`backend/reports/INDUS_FINAL_ANCHORS.json`) | SHA-256 `df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569`, asserted at the freeze from a fresh recompute against `main` (the Spec 042 draft precedent: never inherit an earlier draft's pin). This spec moves no anchor; the file is asserted byte-identical before and after any execution. |

## 3. Step 0 — gates before any coastal count (fail-closed)

Execution runs these gates in order, before any
fish sign is counted at any site. A failure
stops the execution in the class named; nothing
is repaired at run time, and no count produced
before a gate failure is quotable.

- **0.1 Corpus layer identification and pin.**
  The CISI-based corpus layer of record is
  identified from the database as the layer the
  original family-level test used (CISI-keyed,
  site-attributed), exported in full, and
  pinned by SHA-256 digest in the step-0
  record. The gate also re-derives the original
  test's population description from the pinned
  layer (inscription count, site set, the
  family-level coastal result's inputs) and
  checks it against the claim record. If the
  layer cannot be uniquely identified, cannot
  be exported whole, or does not reproduce the
  original population description, the run
  closes as **LAYER NOT PINNABLE** (§6 wording)
  and nothing is counted.
- **0.2 Asset F freeze.** The fish-family list
  is built and frozen under the §4 contract —
  from Parpola's published list only, every
  member carrying its per-sign source locator,
  the canonical file hashed and its digest
  recorded in the step-0 record — **before**
  any coastal count exists. If no published
  Parpola list held or citable by the program
  yields an enumerable family, or any member's
  locator cannot be stated, the run closes as
  **ASSET F FREEZE FAILED** (§6 wording).
- **0.3 Coastal list freeze.** The
  coastal/maritime site list is frozen in the
  step-0 record: every site in the pinned
  layer's site set is classed coastal/maritime
  or inland from the Spec 027 Stage 0 gazetteer
  (pinned in §2) and published site geography,
  under the design's rule — a site is
  coastal/maritime if its published location is
  a port or within the coastal zone. Lothal and
  Dholavira, the original test's coastal set,
  are members by name. Every site whose coastal
  status is contested in the literature is
  listed as contested in the frozen list. A
  site that cannot be classed from the
  gazetteer and published geography closes the
  run as **COASTAL LIST FAILED** (§6 wording);
  no site is classed by its fish counts, ever.
- **0.4 Census (margins only).** Per Asset F
  member, the total occurrence count in the
  pinned layer is computed — occurrence counts
  only, no site split. Members below 30 total
  occurrences are recorded TOO THIN per member,
  with counts, and excluded from the §5 test.
  If fewer than two members clear the floor,
  the execution closes as **TOO THIN** (§6
  wording) with the full census as its finding.
- **0.5 Baseline statement.** The corpus-wide
  coastal share (gate §5's base rate) is
  computed from the pinned layer and the frozen
  coastal list and stated in the step-0 record
  before any per-sign test runs. If the coastal
  share is zero or the coastal site set carries
  no inscriptions, the run closes as
  **COASTAL LIST FAILED** — there is no base
  rate to test against.

## 4. Asset F — the fish-family list (the contract D-04 is drafted against)

Asset F is built once, here, at step 0
(campaign decision E-6). Spec 048 (design D-04)
consumes it by digest and does not re-derive
it; D-02 does not wait for D-04.

**4.1 List form.** A single canonical JSON file,
`asset-f-fish-family.json`, created in this
spec's directory at step 0 and preserved as a
record. Canonical form: UTF-8, keys sorted,
members sorted by `sign_key`, one member object
per sign, no fields beyond §4.2. The file's
SHA-256 digest over its exact bytes is the
asset's identity.

**4.2 Fields (per member, all required).**

| Field | Content |
|---|---|
| `sign_key` | The sign's identifier **in the pinned corpus layer of record** — the key the counts join on. This, not any publication's numbering, is the member's identity inside the program. |
| `mahadevan_number` | The sign's Mahadevan number (e.g. 72, 64, 70 — the numbers the claim records use), or null with a note if the crosswalk gives none. A locator, never a membership criterion. |
| `parpola_number` | The sign's number in Parpola's published list, as printed there. A locator, never a membership criterion. |
| `depiction_note` | What the published list depicts the sign as, in the list's own terms (fish / fish variant / modified fish form), quoted or closely paraphrased. |
| `source_citation` | The published source relied on: Parpola 1994, *Deciphering the Indus Script*, sign list (fig. 5.1, pp. 70–78), the freeze named no different published Parpola list (OPEN-044-2 confirmed; `adjudication.md` §7.3). |
| `source_locator` | The per-sign locator within that source (page / figure entry / list position) at which this member appears. A member without a locator does not enter the asset (gate 0.2). |
| `inclusion_basis` | The rule under which this sign is in the family: `parpola-list-fish` (listed as a fish sign) or `parpola-list-fish-variant` (listed as a modified/variant fish form). No other basis exists. |
| `contested` | Boolean: whether the sign's fish-family membership or identification is contested in the published sources the entry relied on; if true, `notes` names the contest. |
| `notes` | Free text for crosswalk remarks and contests; empty string if none. |

File-level fields: `asset` ("F"), `built_by`
("Spec 044 step 0"), `source` (the §2
bibliographic pin), `frozen_at` (the step-0
record's date), `member_count`, and `digest`
(the SHA-256 of the canonical file with the
`digest` field itself excluded from the hashed
bytes — the exclusion rule is part of the
contract, so any consumer hashes identically).

**4.3 The step-0 freeze rule.** Membership is
decided **solely** from Parpola's published
list, entered before any coastal count exists
for any sign (gate 0.2 precedes gate 0.4's
census and all of §5). No sign is added,
removed, or re-based after any count — census,
baseline, or test — has been seen. A
post-freeze discovery that a member was
mis-entered does not edit the asset in place:
it is recorded as a dated defect note, the
affected results are marked, and any corrected
list is a **new asset version with a new
digest**, usable only under a new freeze
(campaign Part 7, cluster tripwire; claim
F044-C06).

**4.4 Digest pinning for consumers.** A
consuming spec (D-04) states Asset F's digest
in its own freeze record and asserts it at its
own step 0 before counting. A digest mismatch
in a consumer is that consumer's step-0
closure, never a reason to rebuild the asset
to fit. The digest recorded in this spec's
step-0 record is the only authoritative
statement of Asset F's identity.

## 5. The primary test

For each Asset F member clearing gate 0.4's
floor (at least 30 total occurrences):

- **Measure.** The member's coastal share: of
  the member's total occurrences in the pinned
  layer, the share occurring at sites on the
  frozen coastal list — against the corpus-wide
  coastal share of all sign tokens in the
  pinned layer (the base rate, gate 0.5). The
  counting unit is the **sign token** on both
  sides of the comparison (DD-044-2). The
  inscription-level version (share of
  inscriptions carrying the member that are
  coastal, against the coastal share of all
  inscriptions) is computed and reported as a
  stated sensitivity, never as the primary.
- **Test.** An exact test per sign (Fisher's
  exact test, one-sided in the enrichment
  direction, on the 2×2 table: this member's
  tokens × coastal/inland, against all other
  tokens × coastal/inland), with a family-wise
  correction across the members tested —
  **Bonferroni**, at the 5% family level
  (DD-044-4).
- **Criterion.** A member is **ENRICHED** iff
  its corrected exact-test result is below
  0.05 **and** its coastal share ratio (member
  coastal share ÷ corpus coastal share) is at
  least **1.5**. Both clauses are required;
  these are the design's fixed values, carried
  verbatim.
- **Reporting.** Every member's counts are
  reported — coastal tokens, inland tokens,
  total, coastal share, base rate, ratio,
  uncorrected and corrected p — not only
  significant ones. TOO THIN members are
  reported with their counts beside the tested
  members.

**Sensitivities (reported alongside, never
verdict-changing).** (a) The inscription-level
version of the measure, above. (b)
Site-size-matched sensitivity: each coastal
site's fish share versus its own total (the
design's excavation-size control, beside the
base-rate comparison). (c) Contested-site
sensitivity: the full §5 test rerun with every
site listed contested at gate 0.3 removed. A
sensitivity that contradicts the primary is
reported as contradicting it, in the outcome
record's first section — it does not silently
replace the primary, and the primary does not
silently bury it.

## 6. Outcome set and pre-written verdict wordings

The execution ends in exactly one headline
outcome. The outcome record's headline
paragraph uses one of these forms, with the
bracketed quantities filled from the run.
These wordings are written before any data is
touched; no other headline wording may be
used.

- **ENRICHED MEMBER FOUND:** "Tested sign by
  sign against the corpus-wide coastal share
  ([b]%), [k] of the [m] fish signs clearing
  the 30-occurrence floor is enriched at
  coastal sites at the frozen criterion:
  [sign_key(s)], coastal share [s]% against the
  base rate, ratio [r], corrected p [p]. The
  claim's record gains a dated note naming the
  member(s). The family-level verdict —
  partially falsified — does not change: the
  family test already failed, and this residue
  test covers members, not the family. What the
  fish sign meant is not established by this
  result; enrichment at ports is consistent
  with several stories, and the claim's
  guild-badge story remains untested."
- **NO MEMBER ENRICHED:** "Tested sign by sign
  against the corpus-wide coastal share
  ([b]%), no fish sign clearing the
  30-occurrence floor ([m] tested) is enriched
  at coastal sites at the frozen criterion.
  [Per-member counts.] The partial
  falsification of [the claim] is recorded as
  covering the fish family member by member,
  and the residue named in its not-understood
  text is closed. The family-level verdict
  stands exactly as recorded."
- **TOO THIN:** "The sign-by-sign residue test
  cannot be run as designed: fewer than two
  fish signs clear the 30-occurrence floor in
  the pinned corpus layer ([census]). No
  per-sign coastal test was computed. The
  family-level verdict — partially falsified —
  stands exactly as recorded, and the residue
  remains open only in the sense this census
  states: the surviving record is too thin to
  test it sign by sign."
- **ASSET F FREEZE FAILED (step-0 closure):**
  "Spec 044 closed at step 0, gate 0.2: the
  fish-family list could not be frozen from
  Parpola's published list as the §4 contract
  requires ([reason]). No count was computed.
  This closure is a statement about
  runnability, not about the claim; the
  family-level verdict stands exactly as
  recorded."
- **LAYER NOT PINNABLE (step-0 closure):**
  "Spec 044 closed at step 0, gate 0.1: the
  CISI-based corpus layer of record could not
  be uniquely identified and pinned as the
  layer the original test used ([reason]). No
  count was computed. This closure is a
  statement about runnability, not about the
  claim; the family-level verdict stands
  exactly as recorded."
- **COASTAL LIST FAILED (step-0 closure):**
  "Spec 044 closed at step 0, gate [0.3/0.5]:
  the coastal site list could not be frozen
  under the design's rule ([reason]). No
  per-sign test was computed. This closure is
  a statement about runnability, not about the
  claim; the family-level verdict stands
  exactly as recorded."
- **INVALID (integrity closure):** "Spec 044
  closed as INVALID: [the named §2 pin
  mismatched / the anchors assertion failed /
  the step-0 record does not precede the first
  count]. No result is recorded under this
  spec."

## 7. Epistemic limits (binding on all outputs)

1. **The Roif hold.** This spec's records are
   internal. Nothing derived from this spec's
   results — no summary, article draft, status
   line, paper or website text, or public
   register wording — is published or surfaced
   under this campaign, in any form, until the
   owner clears the specific publication act
   under campaign R-7 / Part 8. Campaign
   reporting names this member only as
   "executed — held under the Roif gate,"
   without result content. (The verification
   that Roif's preprint is publicly posted and
   citable does not lift this hold; it is one
   of the gate's two conditions, and the
   owner's cleared act is the other.)
2. **No resurrection.** An ENRICHED member does
   not change, soften, or re-open the
   family-level verdict (partially falsified).
   The outcome appends to the claim's record as
   a dated note naming the member; the family
   verdict's own text is never edited.
3. **No meaning conclusion.** Even if a member
   is enriched, this test does not establish
   what the fish sign meant. Enrichment at
   ports is consistent with several stories;
   the claim's specific guild-badge /
   coastal-trader story remains untested by
   any distributional test, and no output may
   present enrichment as evidence for it.
4. **Compilation-relativity.** Site types and
   sign identities are as recorded in one
   compilation layer. The original test's
   limit — site types as published in the CISI
   data — is mitigated here by the frozen
   gazetteer-based coastal list, not removed:
   a different compilation's site set or sign
   identities could give a different per-sign
   picture, and no output claims otherwise.
   Spec 037's census (compilations diverging
   on matched objects) is the standing caution.
5. **The coastal list is a published-geography
   judgement, frozen — not a fact of the
   corpus.** Contested sites are named, and
   the no-contested-sites sensitivity travels
   with every statement of the result.
6. Negative, thin, and step-0-closure outcomes
   publish (internally, under limit 1) with the
   same prominence as an enriched finding.

## 8. Controls and named confounders

- **Excavation-size bias.** Big coastal sites
  produce more of everything. The comparison is
  against the corpus-wide coastal share, not
  raw counts, and the site-size-matched
  sensitivity (§5) is reported alongside.
- **Site classification disputes.** Contested
  sites are listed at gate 0.3 and the test is
  rerun without them as a stated sensitivity
  (§5).
- **Family-definition discretion.** Asset F is
  frozen from the published list at step 0,
  before counting (§4.3); the list, its
  locators, and its digest are part of the
  record, so the discretion is inspectable
  rather than hidden.
- **Multiple comparisons.** The family-wise
  Bonferroni correction across tested members
  is part of the criterion, not an afterthought
  (§5).
- **Small counts.** The 30-occurrence floor,
  exact tests, and full per-member counts —
  a member cannot carry the headline on a
  handful of tokens.

## 9. Reporting obligations

Every product of an execution carries, in its
headline section:

1. the corpus label — the CISI-based layer of
   record as pinned at gate 0.1, with its
   digest and its lineage posture as recorded;
2. Asset F's digest and member count, and the
   frozen coastal list with its contested
   sites named;
3. per member: coastal tokens, inland tokens,
   total, coastal share, base rate, ratio,
   uncorrected and corrected p, and the
   ENRICHED / not-enriched word — for every
   member, not only significant ones;
4. the headline outcome word of §6, in §6's
   pre-written wording;
5. the Roif-hold sentence: "This record is
   internal under the campaign's Roif gate
   (R-7); it is not a publication."

Deliverables at execution: a results JSON
(step-0 record with all pins and the Asset F
digest, census, baseline, per-member tables,
sensitivities), a report under these headline
rules, Asset F's canonical file (§4.1), the
experiment-graph node (H15/H23, registered and
verified before the run), the outcome append
in this directory, and the LEDGER entry (H1).
Foundation check (H21) after the execution
phase: 0 failures, or the outcome record says
why not. Anchors asserted byte-identical
before and after.

## 10. Stop conditions and outcome classes

Execution ends in exactly one of:

- **ENRICHED MEMBER FOUND**, **NO MEMBER
  ENRICHED**, or **TOO THIN** — per §§3–5,
  after all gates pass (TOO THIN is also gate
  0.4's closure).
- **ASSET F FREEZE FAILED** — gate 0.2.
- **LAYER NOT PINNABLE** — gate 0.1.
- **COASTAL LIST FAILED** — gates 0.3 / 0.5.
- **INVALID** — a §2 pin mismatches, the
  anchors assertion fails, or any count is
  shown to precede its gate.

## 11. Execution shape (gated; NOT run by this draft)

1. **Graph-first build** (H15/H23) — script,
   graph node, registration, verification.
2. **Step 0** (§3) — layer pin; Asset F freeze;
   coastal list freeze; census; baseline.
3. **Primary** (§5) — per-member exact tests
   with the family-wise correction; all
   members reported.
4. **Sensitivities** (§5) — inscription-level,
   site-size-matched, contested-sites-removed.
5. **Outcome** (§9) — appended records only;
   anchors asserted byte-identical; foundation
   check reported as measured; the claim's
   record gains its dated append (member note
   or residue closure) — under the Roif hold,
   as an internal record.

## 12. What this spec is not

Not a re-run of the family-level test, not a
re-adjudication of the partially falsified
verdict, not a test of what any fish sign
meant, not a new corpus, not a period control,
not D-04 (the fish family's positional test,
which consumes Asset F under its own spec),
and not an authorisation to execute or to
publish anything. It is the sign-by-sign
residue of one settled claim, plus the
one-time build of the fish-family list two
specs share, designed so that its honest
outcomes — including closing at its own
step 0 — are written down before any sign is
counted.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
