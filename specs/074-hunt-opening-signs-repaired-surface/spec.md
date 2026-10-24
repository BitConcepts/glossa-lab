# Spec 074 — Hunt Opening Signs on the Repaired Keying Surface: The Opening Signs Are the Animal Signs, on the Shakti Corpus (Successor to Spec 070, Design D-06)

> ## DESIGN DRAFT — FOR FREEZE — 2026-10-24
>
> Drafted under the owner's order of
> 2026-10-24: **re-freeze and execute Spec
> 070's question on the repaired surface.**
> Spec 070 (Phase 433) closed at step 0 as
> POPULATION NOT KEYED: of the 31
> opening-strong signs its battery enumerated
> on the Shakti corpus, five — the ICIT codes
> 136, 298, 401, 617 and 824 — had no Wells
> identity in the pinned canonical sign
> registry, so no Asset A row could be keyed
> to them, and the disposition its freeze had
> fixed in advance (DD-070-11) closed the
> execution before any join. Spec 070's
> outcome record named what a successor
> would need: "a registry that carries Wells
> identities for these signs, or a different
> freeze-fixed route — and that is a new
> freeze decision, not a repair this
> execution was permitted to make at run
> time." Spec 073 (Phase 436, executed
> 2026-10-23, PR #354) built that repair:
> Registry v2, which keeps all 803 v1 rows
> byte-identical and adds 210 rows carrying
> `icit_wells` identities from the published
> ICIT sign list (Fuls 2023, *A Catalog of
> Indus Signs*, Ch. 2.3), and Asset A v2,
> which keeps all 187 v1 rows untouched and
> adds 365 rows entered blind under the same
> discipline — outcome REPAIRED WITH NAMED
> SHORTFALL. This spec is the new freeze
> decision Spec 070's record called for: the
> same question, the same claim, the same
> test, re-based on the repaired surface.
>
> **Spec 070's closure stands unamended.**
> Nothing in this spec reopens, edits, or
> completes Spec 070, Spec 049, or Spec 073;
> their records stand exactly as executed.
> This spec appends a successor beside them.
> Its own outcome, when an execution is
> separately ordered and run, appends to the
> claim's record by the same dated-append
> discipline Spec 070's design carried.
>
> **Dependency (satisfied at this draft).**
> This spec consumes Spec 073's two frozen
> products. Step 0 (§5, gate 0.1) asserts
> their digests from Spec 073's executed
> record; a missing or mismatched digest
> closes this spec at step 0. Unlike Spec
> 070 at its draft, the dependency exists:
> both products are frozen on the merged
> record, and their digests are quoted in §3
> from Spec 073's freeze records and
> re-verified first-hand at this draft.
>
> The execution phase number is
> **unassigned** at this draft. It is
> allocated at the freeze act, from the
> merged record as it then stands.
>
> **Honesty fence (binding on every product
> of this spec, and stated in its headline
> block).** This spec tests Hunt's claims
> against a positional framework **measured
> on the graded ICIT corpus** (the Shakti
> corpus, §3). It does not test them against
> the Phase-43 framework. The recorded
> Phase-43 quantities — **805/2,267** and the
> **40/61/20** strong-sign classes — are
> **never cited as this spec's basis**: not
> as its population, not as its reference
> points, and not as quantities it reproduces
> or corrects. They appear in this draft only
> as the record of the predecessor question
> (§1), in this fence, and nowhere else as a
> load-bearing number.

**Design source:** D-06 in the experiment-design
packet at PR #195
(`docs/research/experiment-designs-2026-10-13/02-roif-and-hunt.md`,
§D-06), as drafted in **Spec 049**, re-scoped
in **Spec 070** (frozen 2026-10-22; freeze
digest
`763108f89311ab2791827b347a155a8b4f9abad940ab59f921af129f79c73e3e`),
and executed as Phase 433 (closure record:
`specs/070-hunt-opening-signs-successor/outcome.md`;
machine record `reports/phase433_results.json`).
This spec carries Spec 070's design **verbatim
in substance** — the same claim, the same
falsifier, the same §2 battery, the same §4
test and §4.3 precedence, the same three
sensitivities, the same grade discipline — and
changes only what the repaired surface
requires. **§1.3 lists every change against
Spec 070, with its reason.** Anything not
listed there is carried unchanged.

**Claim under test:**
`without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_003`
— "Faunal signs function as identity/guild/
commodity prefixes (initial position)" —
standing **IN QUESTION**: partially supported
(positional half only). This spec tests the
claim's animal half, in its re-scoped form:
against a positional framework measured on
the graded ICIT corpus (§1.1).

**AI disclosure:** this draft is produced by an
AI agent (Muse Spark, via Muse) at the
direction of Tristen Pierson, per constitution
§VI.

---

## 1. The claim and the record it stands on

The claim's record states its animal half and
its falsification condition in its own words:
faunal signs are the opening signs, and the
claim fails if "Faunal signs not enriched in
initial position above random baseline." The
positional half was measured on the Phase-43
framework; the animal half has never been
tested at all, because the programme held no
classification of which signs depict animals.
That classification is Asset A — built by
Spec 069 under Spec 045's frozen §§2–3
contract, and extended to Asset A v2 by Spec
073 under the same contract — and the
positional framework this successor tests
against is measured on the Shakti corpus
under §2's battery.

Spec 070 defined its population as **Shakti's
own opening-strong set**: derived on the
Shakti corpus under the §2 battery, enumerated
in full in Wells space, and published before
any join or test. Its size was whatever the
battery returned on that corpus; no count was
promised in advance. The battery returned 31
signs, enumerated in full in Spec 070's
machine record (`reports/phase433_results.json`,
SHA-256
`667560a5c185051ea7acc9afacf2f9c4bbf3f863e9d17851c634fa56eb3ad214`;
the population publication's own SHA-256,
recorded in that file ahead of any join, is
`30092b6fd64f221ee0808addeedd11e1e800cf3d79716ba26b3fb971f396a93b`).
Keying under Spec 070's route (DD-070-9, over
Registry v1) resolved 26 of the 31; the five
named in the banner could not be keyed, and
the execution closed at gate 0.4 under the
disposition DD-070-11 had fixed. Under the
repaired surface the same 31 signs all key
(§1.3, change 2; verified at this draft
against the pinned files, §5 gate 0.4's
reproduction assertion being the execution's
own proof).

### 1.1 The question, in plain words

Hunt says the signs that open inscriptions are
the animal signs — fish, unicorn, buffalo,
rhinoceros, tiger, elephant, in his naming.
Measured on the graded ICIT corpus: take the
signs that strongly prefer the opening of
inscriptions in that corpus, and the frozen
classification of which signs depict animals,
and ask whether the opening signs are the
animal signs at well above the rate the sign
inventory would predict. The positional
framework is this corpus's own, measured
under §2; the classification is Asset A v2,
frozen before any join; the join and one
exact test answer the question.

### 1.2 The hypothesis and its falsifier

**Hypothesis.** Animal signs — the signs the
frozen Asset A v2 classes `depicted_kind =
animal` — are enriched among Shakti's
opening-strong signs relative to their share
of the sign inventory, under the criteria of
§4.3.

**Falsifier.** Opening-strong signs are animal
signs at no better than the base rate: animal
signs appear among the opening-strong set at
or below the rate the inventory share predicts,
under the criterion of §4.3. If the falsifier
fires, the claim's animal half is recorded as
not supported **in this re-scoped form**, in
the pre-written words of §4.6, and the claim
stands on its positional half alone — stated
as such, not averaged away.

### 1.3 The named changes against Spec 070 (complete list)

Spec 070's design is carried verbatim in
substance except for the following. Each
change is named here, with its reason; no
other difference is intended, and any
further difference found between this text
and Spec 070's is a drafting defect, to be
recorded as such.

1. **The keying surface is re-based on Spec
   073's repaired products.** Registry v1
   (`data/crosswalks/canonical_sign_registry.csv`,
   SHA-256 `8a0b2a82…`, 803 rows) is replaced
   as the keying route's registry by
   **Registry v2**
   (`data/crosswalks/canonical_sign_registry_v2.csv`,
   SHA-256 `42ab09fb…`, 1,013 rows), and
   Asset A v1 (187 rows, SHA-256 `95231935…`)
   is replaced as the classification by
   **Asset A v2** (552 rows, SHA-256
   `681e017d…`). *Reason:* this is the repair
   Spec 070's outcome record named and Spec
   073 executed; on the v1 surface this test
   closes at its own keying gate for the
   already-recorded reason, without reaching
   the question. Gate 0.1 therefore asserts
   the v2 products' frozen state from Spec
   073's executed record, where Spec 070's
   gate 0.1 asserted Spec 069's.
2. **The keying route gains a second leg.**
   Spec 070's route (DD-070-9) is retained as
   the first leg: a Shakti sign's ICIT code is
   its Wells number, resolved through the
   registry's `parpola_1982` rows' `wells_ids`
   to exactly one Asset A `sign_key`. A sign
   the first leg cannot resolve is then
   resolved through Registry v2's
   `icit_wells` rows — the rows Spec 073
   appended for exactly the identities the
   first leg lacks — whose `sign_id` is the
   Wells id itself, to the Asset A v2 row of
   that `sign_key`. Zero or multiple
   resolutions across both legs is unkeyable,
   exactly as under DD-070-9. *Reason:* the
   five signs Spec 070 could not key carry
   no `parpola_1982` Wells identity at all;
   their identities exist in the published
   record only as ICIT sign-list entries,
   which is the form Registry v2's appended
   rows carry (each cited to Fuls 2023,
   *Catalog*, Ch. 2.3, with its printed
   page). Verified at this draft against the
   pinned files: over Registry v2 the two
   legs resolve all 31 of Spec 070's recorded
   signs to exactly one Asset A v2 row each,
   and the combined Wells map carries 708
   distinct Wells ids with zero resolving to
   more than one sign. The route's exact
   form is fixed at this spec's freeze
   (OPEN-074-2).
3. **A population-reproduction assertion is
   added at gate 0.4.** The corpus, the
   row-grades file, and the §2 battery are
   pinned identically to Spec 070's, so the
   battery's enumeration on the primary
   population is a recorded measurement, not
   a first one: gate 0.4 asserts that the
   enumerated opening-strong set equals Spec
   070's recorded 31 signs exactly — the sign
   set and each sign's I/M/T counts as
   published in `reports/phase433_results.json`
   — and that the full battery class census
   reproduces Spec 070's recorded census
   (220 signs at the floor: TERMINAL_STRONG
   42, MEDIAL_STRONG 81, TERMINAL_MODERATE
   37, INITIAL_MODERATE 6, MIXED 23,
   INITIAL_STRONG 31). A difference closes
   the execution as **POPULATION NOT
   REPRODUCED** (§4.6), a closure class Spec
   070 did not need and this spec adds.
   *Reason:* on identical pinned inputs a
   different enumeration is non-determinism
   or input drift, not a new measurement;
   the successor's question is the join Spec
   070 could not perform, and it is only
   Spec 070's question if the population is
   Spec 070's population. Spec 070's rule
   that its own set's size was no check
   against any *other* count (40, or any
   Phase-43 count) stands untouched.
4. **The asset facts are Asset A v2's.**
   Where Spec 070's text quotes Asset A's
   per-kind counts (animal 20, sky_cycle 0,
   object_goods 14, human 25, other 127,
   contested 0, unidentified 1; 187 rows),
   this spec quotes Asset A v2's (animal 30,
   sky_cycle 0, object_goods 22, human 43,
   other 246, contested 0, unidentified 211;
   552 rows), as recorded in Spec 073's
   `asset-a-v2-freeze.json`. *Consequence,
   stated at draft so it cannot be mistaken
   for a design change:* the five formerly
   unkeyable signs are classified
   `unidentified` in Asset A v2 (Spec 073's
   outcome record states it per sign: no
   ruled published source gives any of them
   a verbal depiction). They therefore key,
   and under §4.1's carried classification
   discipline they are counted, listed, and
   excluded from the primary's numerator and
   denominator, like every unidentified
   member. Keying is not classification.
5. **The pre-written wordings of §4.6 are
   re-pointed, and one is added.** The
   verdict wordings are Spec 070's, with the
   spec number, the asset name (Asset A v2),
   and the digest slot updated; the gate 0.1
   closure wordings name Spec 073's records
   where Spec 070's named Spec 069's; the
   POPULATION NOT KEYED wording names both
   keying legs; and a POPULATION NOT
   REPRODUCED wording is added for change 3.
   No verdict wording's substance — its
   criteria, its claims about what an
   outcome establishes, or its fences —
   changes.

## 2. The positional battery — the Phase-43 rules, applied new to an ICIT corpus

The positional classes of this spec are
derived on the Shakti corpus under the rules
of the Phase-43 battery, recovered in full in
the battery record
(`~/workspace/research_notes/amendment-queue-2026-10-21/item-2-phase43-battery.md`,
§2, read first-hand at Spec 070's draft) and
stated here as a battery **applied new to an
ICIT corpus** — a first measurement on this
corpus, not a reproduction of any Phase-43
quantity. (The successor's gate 0.4
reproduction assertion is against Spec 070's
recorded measurement on this corpus under
this battery — §1.3, change 3 — never against
any Phase-43 quantity.)

- **Position rule.** For each sequence of
  length ≥ 2, each sign occurrence is counted
  once: position 0 → initial (I); last
  position → terminal (T); any position
  between → medial (M). A two-sign sequence
  contributes one I and one T and no M.
  Sequence order is the corpus's recorded
  order; no reversal is applied. Per sign:
  `total` = I + M + T; `i_rate` = I / total,
  `m_rate` = M / total, `t_rate` = T / total.
- **Count floor.** A sign enters classification
  only if `total` ≥ **5**.
- **Strength cascade.** First match wins, in
  this order: (1) `t_rate` ≥ **0.60** →
  TERMINAL_STRONG; (2) `i_rate` ≥ **0.55** →
  INITIAL_STRONG; (3) `m_rate` ≥ **0.65** →
  MEDIAL_STRONG; (4) `t_rate` ≥ 0.40 →
  TERMINAL_MODERATE; (5) `i_rate` ≥ 0.40 →
  INITIAL_MODERATE; (6) otherwise MIXED. The
  cascade order is part of the rule: a sign
  with `t_rate` ≥ 0.60 is TERMINAL_STRONG even
  if its `i_rate` also clears 0.55.
- **G5 attestation (binding wording).** The
  Phase-43 battery is **threshold-only**: it
  contains **no chance-baseline step** — no
  permutation, shuffle, or expected-rate
  baseline for its positional classes was ever
  part of it (battery record §2). This spec
  claims to restore none. Its baseline is the
  inventory-share comparison of §4, which is
  this design's own test construction (carried
  from design D-06 and Spec 049's draft), not
  a Phase-43 element, and no product may
  describe it as one.

Sequences are the primary population's
sequences (§3): inscriptions of the
documented-lineage rows, in ICIT sign codes,
counted in Wells space. The all-`000`
placeholder rows enter no sign analysis, per
the grade discipline of §3.

## 3. Inputs (pinned at this draft; re-asserted at the freeze)

| Input | Pin / state |
|---|---|
| **Asset A v2** (Spec 073, under Spec 045 §§2–3 as executed for v1 by Spec 069 and extended by Spec 073 §5) | The canonical CSV `specs/073-keying-surface-repair/asset-a-v2/depicted-kind-classification.csv`, SHA-256 `681e017da8b3f93aeade7e85361565fa8f3f4178b167dfa2448f5b4c239a8193`, 552 rows (187 carried from v1 untouched + 365 new-entry), per-kind counts animal 30, sky_cycle 0, object_goods 22, human 43, other 246, contested 0, unidentified 211. **Pin source:** `specs/073-keying-surface-repair/asset-a-v2/asset-a-v2-freeze.json`, quoted from Spec 073's executed record; step 0 (gate 0.1) asserts it. Re-verified first-hand at this draft by recomputation on the merged tree. |
| **Registry v2** (Spec 073) | `data/crosswalks/canonical_sign_registry_v2.csv`, SHA-256 `42ab09fb06750098dc8cc0370c4ba4c1a538353d943a49f983d7347f52e8ef71`, 1,013 rows (803 carried from v1 byte-identical + 210 `icit_wells` rows appended; completions applied: 0). **Pin source:** `specs/073-keying-surface-repair/registry-v2/registry-v2-freeze.json`. The keying route of §4.1 runs over this file. Its NO PUBLISHED IDENTITY schedule (`specs/073-keying-surface-repair/registry-v2/no-published-identity.json`) names one attested code — token 999 — with no published identity; §7 carries its consequence. |
| **Spec 070's executed record** (the population source) | `reports/phase433_results.json`, SHA-256 `667560a5c185051ea7acc9afacf2f9c4bbf3f863e9d17851c634fa56eb3ad214` on the merged tree, with `specs/070-hunt-opening-signs-successor/outcome.md` and Spec 070's freeze digest `763108f89311ab2791827b347a155a8b4f9abad940ab59f921af129f79c73e3e`. Gate 0.4's reproduction assertion runs against the enumeration published in this record. |
| Shakti corpus (`sanitized_corpus.json`) | SHA-256 `345241b13fedada87b4783c24cd241123491bbd7edaf5bf636f9cdb36c01da68`. Held restricted-local under its GPL-3.0 terms; cited only through the intake record (next row) and the row-grades file. 5,704 rows; 5,536 analyzable. Re-verified first-hand at this draft by direct hash at its restricted-local path. |
| Shakti intake record | `docs/decisions/2026-10-22-shakti-corpus-intake-record.md` — the record that adopts proposal P-F1's intake gates (S1–S4) for this corpus, landed by PR #339. The row-grades file of the 2026-10-22 provenance audit is pinned there and here: SHA-256 `02394241773cf8700f49ba19c30cdbaa589cf119d2c97c35e15e0447434dd739` (re-verified first-hand at this draft). Grade counts: 3,212 documented-lineage / 2,087 undocumented-corroborated / 405 undocumented-uncorroborated rows. |
| Sign crosswalk of record (`data/crosswalks/sign_crosswalk_master.csv`) | SHA-256 `4ace1a617f40afe8d0bbb82e5461d98a675296152e7577b04fb67b00f4f5dfcf` (as pinned by Specs 045/049/070). Carried as a record of the identity layer; the keying route of this spec runs over Registry v2 (§1.3, change 2), and no Mahadevan keying is used anywhere in this spec. |
| Claim record (`glossa-indus/claims/extracted_claims/without_kings_or_conquests_the_indus_scr_ce9d98cc.json`) | Read at this draft: claim `…_manual_003`, its normalised claim, status, and falsification condition as quoted in §1. Spec 070's execution made no append to it (its §4.6 closure wordings carry the claim forward unchanged); it stands as it stood at Spec 070's freeze. |
| Anchors file (`backend/reports/INDUS_FINAL_ANCHORS.json`) | SHA-256 `df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569`. This spec moves no anchor; the file is asserted byte-identical before and after any execution. |

**Grade discipline (P-F1 S4, binding).** The
**primary population is documented-lineage
rows only** (3,212 rows; 3,045 analyzable, as
graded — the step-0 census governs over these
derived figures). Rows graded
undocumented-uncorroborated (405) enter no
count, statistic, or argument. The
documented + corroborated population (5,299
rows; 5,131 analyzable, as graded) enters only
in the pre-registered corroborated sensitivity
of §4.4, reported beside the primary under
S4's both-ways rule: a result that changes
between the two populations is reported as
grade-sensitive wherever it is cited.

**Lineage statement (P-F1 S3, binding).**
Every product of this spec states, in its
headline block: "This corpus is an ICIT-lineage
corpus. Agreement between it and the program's
earlier ICIT-lineage layer is consistency
within one tradition, not independent
corroboration." A product without the statement
does not cite the corpus.

## 4. The test (runs only after every §5 gate passes)

### 4.1 Populations

- **O — Shakti's own opening-strong set.** The
  signs classed INITIAL_STRONG by the §2
  battery over the primary population
  (documented-lineage rows only). O is
  enumerated in full **in Wells space** and
  published as the execution's first product
  at gate 0.4 — before any join to Asset A v2
  and before any test quantity. Under this
  successor the enumeration is also a
  **reproduction**: the corpus, grades, and
  battery are Spec 070's pinned inputs, and
  gate 0.4 asserts the enumerated set equals
  Spec 070's recorded 31 signs exactly
  (§1.3, change 3). No count from any other
  corpus, framework, or predecessor design —
  not 40, not any Phase-43 count — stands as
  its check.
- **Keying.** Every enumerated sign in O is
  keyed to **exactly one Asset A v2 row in
  Wells space**, under the two-leg keying
  route the freeze fixes (OPEN-074-2;
  §1.3, change 2): the `parpola_1982` leg of
  DD-070-9 first, then Registry v2's
  `icit_wells` leg for the signs the first
  leg cannot resolve. A sign that cannot be
  so keyed is a **named step-0 finding**
  (gate 0.4): it is listed by its Wells
  identity, with the reason it cannot be
  keyed, and it is disposed of exactly as the
  freeze stated in advance — it is **never
  quietly replaced**, dropped, or hand-keyed.
- **U — the comparison inventory.** Every sign
  with **at least 30 occurrences** in the
  primary population, counted under the
  counting rule carried from DD-070-10 (every
  occurrence in sequences of length ≥ 2,
  counted once under the battery's own
  counting, on the population in question).
  U is enumerated and published at gate 0.5
  with per-sign counts.
- **Classification.** Each sign in O and in U
  is animal, non-animal, contested, or
  unidentified **exactly as the frozen Asset
  A v2 records it**. This spec uses exactly
  one field value as its animal set:
  `depicted_kind = animal`. Whatever the
  frozen asset classes animal is the animal
  set, and whatever it does not is not; no
  sign is added or removed by this spec, by
  Hunt's list, or by any worker's judgement.
- **Contested rows (Spec 045's rule).**
  Contested Asset A v2 rows are **excluded
  from the primary** and **reported** —
  counted, listed with both verbatim labels,
  and their effect measured in sensitivity
  S-A (§4.4). Primary shares are computed
  over classified members only (animal vs
  non-animal); contested and unidentified
  members are counted, listed, and excluded
  from both numerator and denominator of the
  primary, and the raw counts over the full
  sets are published beside them so nothing
  the exclusion does is invisible. (Asset A
  v2 carries zero contested rows; the rule
  stands as written because the asset, not
  this spec, is where a dispute would be
  recorded.)

### 4.2 The two arms

- **Primary arm.** The share of animal signs
  among O versus the animal share of U:
  enrichment ratio **R1 = (animal share of O)
  / (animal share of U)**, with an exact test
  (Fisher's exact test on the disjoint 2×2
  table — O versus U∖O, animal versus
  non-animal). The criterion p is the
  one-sided p in the enrichment direction;
  the two-sided p is published alongside it.
  Counts published in full: every cell, both
  sets' sizes, and the excluded counts of
  §4.1.
- **Reversed arm (pre-registered).** Among all
  animal signs in U, the share that are in O,
  versus the same share for non-animal signs
  in U: ratio **R2** with its exact test on
  the corresponding table. The reversed arm
  is verdict-bearing only as §4.3 orders it;
  it is computed and published whatever the
  primary finds.

### 4.3 Verdict criteria (fixed in advance; precedence as ordered)

Each arm's exact test is at the **5% level**.
The headline is decided by these rules, in
this order (carried from Spec 049's draft,
DD-049-3, through Spec 070 unchanged; the
freeze may re-order openly):

1. **NOT SUPPORTED** — if R1 ≤ 1.0, or the
   primary exact test cannot reject equality
   (p ≥ 0.05). This is the falsifier of §1.2,
   and it fires on the primary arm regardless
   of the reversed arm; a reversed-arm result
   against it is reported in the outcome's
   first paragraph as a recorded asymmetry,
   not as a headline change.
2. **SUPPORTED** — if R1 ≥ 1.5 with p < 0.05
   in the primary arm **and** the reversed
   arm does not contradict the direction
   (R2 > 1.0).
3. **INCONCLUSIVE** — in every other
   adjudicated case: 1.0 < R1 < 1.5 with
   p < 0.05; or R1 ≥ 1.5 with p < 0.05 but
   R2 ≤ 1.0 (the arms disagree); or the
   baseline is empty (no animal signs in U's
   classified members — the ratio is then
   undefined and the census is the finding).

The verdict word, whichever it is, is a word
about the **re-scoped** test: Hunt's claim
against a positional framework measured on
the graded ICIT corpus (the §0 honesty
fence). No wording under this spec presents
it as a verdict on the Phase-43 framework.

### 4.4 Sensitivities (pre-registered, three)

Reported beside the primary with the same
prominence; none replaces the headline word.

- **S-A — contested included.** The primary
  arm rerun with contested signs included
  under their CISI-governed labels (the
  inclusion rule of Spec 045 §2.5), so the
  effect of the dispute rule's exclusion is
  measured, not assumed away. (Asset A v2
  carries zero contested rows, so on this
  asset S-A is expected to equal the primary;
  it is run and reported as such, not
  assumed.)
- **S-B — the unicorn removed.** The primary
  arm rerun without the unicorn sign(s): the
  sign(s) whose frozen Asset A v2 verbatim
  label identifies the unicorn — the commonest
  "animal" of Hunt's naming, and a composite
  creature whose identification is
  conventional. The removed sign(s) are named
  at gate 0.5 from the frozen asset's labels,
  before any test quantity exists. If no sign
  carries such a label, S-B is recorded as
  not applicable, with that fact stated.
- **S-C — corroborated sensitivity (P-F1
  S4).** The primary arm rerun over the
  documented + corroborated population
  (§3), with the battery classes re-derived
  on that population and every quantity
  recomputed; both populations' results are
  reported, and a verdict-relevant change
  between them is reported as grade-sensitive
  wherever the result is cited. (The
  reproduction assertion of gate 0.4 applies
  to the primary population only; S-C's
  classes are a re-derivation on a different
  population, as in Spec 070.)

### 4.5 Controls and named confounders

- **Frequency.** Common signs are more often
  classifiable as position-strong: the
  comparison inventory is restricted to signs
  with at least 30 occurrences, in both arms
  (the design's control, carried from Spec
  049's draft verbatim in substance).
- **Grade sensitivity by construction.** The
  corroborated stratum is systematically
  different material — more incomplete, more
  `000` placeholders, shorter, concentrated
  in different artefact types (provenance
  audit of 2026-10-22, §2) — so positional
  rates computed over it describe a different
  population, not a larger sample of the
  same one. Controlled by the
  documented-only primary and sensitivity
  S-C, never by pooling silently.
- **Classification disputes.** Contested
  signs are named and listed with both
  verbatim labels; the primary excludes them
  by the asset's rule and S-A measures the
  exclusion.
- **The unicorn problem.** Handled by S-B,
  pre-registered here, not improvised after
  a result is seen.
- **Keying.** A sign that cannot be keyed in
  Wells space under either leg of the frozen
  route is a named step-0 finding with its
  freeze-stated disposition (gate 0.4),
  never a silent drop or a hand-keyed row.
- **One battery, second use on this corpus.**
  The §2 battery was applied to this corpus
  once before, by Spec 070, and its classes
  are on record; the successor's enumeration
  is asserted against that record at gate
  0.4 (change 3), and the step-0 census
  publishes the full class counts so the
  derivation is inspectable in full.

### 4.6 Pre-written verdict wordings

The outcome record's headline paragraph uses
one of these forms, with the bracketed
quantities filled from the run. **Every form
carries the §3 lineage statement (P-F1 S3)
in its headline block**, and every form
states the framework it measured on, in the
fence's words.

- SUPPORTED: "Measured on the graded ICIT
  corpus — a positional framework measured on
  that corpus, not the Phase-43 framework —
  of the [n] opening-strong signs Shakti's
  own battery returns, [a] are animal signs
  under the frozen published-identification
  classification (Asset A v2, SHA-256
  [digest]) — a share of [s1] against the
  animal share [s2] of the [N] signs with at
  least 30 occurrences: enrichment ratio
  [R1], exact test p = [p]. The reversed arm
  agrees in direction (ratio [R2]). The
  animal half of Hunt's opening-sign claim
  is supported in its re-scoped form: on
  this corpus, the opening signs are the
  animal signs, at well above the base rate.
  This does not establish that animal signs
  marked identity, guild, or goods — position
  plus depiction is still not meaning."
- NOT SUPPORTED: "Measured on the graded
  ICIT corpus, of the [n] opening-strong
  signs Shakti's own battery returns, [a]
  are animal signs under the frozen
  classification (Asset A v2, SHA-256
  [digest]) — a share of [s1] against the
  animal share [s2] of the comparison
  inventory: enrichment ratio [R1], exact
  test p = [p]. Animal signs appear among
  the opening-strong signs at no better than
  the base rate. The animal half of the claim
  `without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_003`
  is not supported in its re-scoped form;
  the claim stands on its positional half
  alone, exactly as its record is amended to
  say by the dated append that carries this
  outcome."
- INCONCLUSIVE: "Classified under the frozen
  Asset A v2 (SHA-256 [digest]) and measured
  on the graded ICIT corpus, the
  opening-strong signs are animal at ratio
  [R1] against the inventory base rate
  (exact test p = [p]; reversed arm ratio
  [R2]) — [the band / disagreement /
  empty-baseline reason, in the words of
  §4.3]. The test does not settle the
  claim's animal half in its re-scoped form;
  the claim stands IN QUESTION with this
  attempt on its record, its counts published
  in full."
- ASSET PIN MISMATCH (gate 0.1 closure):
  "Spec 074 closed at step 0: the repaired
  surface presented at execution hashes to
  [observed], which is not the digest
  [frozen] quoted verbatim in this spec's
  freeze record from Spec 073's executed
  record. No join was performed and no
  quantity was computed. The claim stands as
  recorded."
- ASSET NOT FROZEN (gate 0.1 closure): "Spec
  074 closed at step 0: the repaired surface
  is not frozen on record — Spec 073's
  [registry-v2-freeze.json /
  asset-a-v2-freeze.json] [does not exist /
  is not landed] at this execution. No join
  was made and no quantity was computed. The
  claim stands as recorded. This is a
  dependency closure on Spec 073's executed
  record, not a verdict on the claim."
- SHAKTI INTAKE NOT REPRODUCED (gate 0.2
  closure): "Spec 074 closed at step 0:
  the Shakti intake did not reproduce —
  [the S1 identity failure / the S2 census
  failure, with observed values]. No
  positional quantity was computed and no
  join was made. The claim stands as
  recorded."
- POPULATION NOT REPRODUCED (gate 0.4
  closure): "Spec 074 closed at step 0: the
  battery's enumeration on the primary
  population does not reproduce Spec 070's
  recorded enumeration — [the differing
  signs / census cells, with observed
  values, published with this closure]. The
  corpus, grades, and battery are pinned
  identically to Spec 070's, so the
  difference is non-determinism or input
  drift, not a new measurement. No join was
  performed and no test quantity was
  computed. The claim stands as recorded."
- POPULATION NOT KEYED (gate 0.4 closure):
  "Spec 074 closed at step 0: Shakti's
  opening-strong set was enumerated in full
  ([n] signs, published with this closure),
  and the signs that could not be keyed to
  exactly one Asset A v2 row in Wells space
  under either leg of the frozen keying
  route are listed with their reasons; under
  the disposition the freeze stated, the
  execution closes here. No join was
  performed and no test quantity was
  computed. The claim stands as recorded."
- INVALID (gates 0.3 / 0.5 closure): "Spec
  074 stopped before any test quantity:
  [the failed gate and observed values]. No
  verdict is recorded; the claim stands as
  recorded."
- NOT-RUN (dependency closure): "Spec 074
  was not run: the repaired surface was
  never frozen under Spec 073 ([Spec 073's
  closure / state, as recorded]), so the
  registry and classification this test
  consumes do not exist in frozen form. No
  step-0 gate was run. The claim stands as
  recorded."

## 5. Step 0 — gates before any test quantity (fail-closed)

Execution runs these gates in order, before
any §4 quantity is computed. A failure stops
the execution in the class named; nothing is
repaired at run time.

- **0.1 Repaired-surface assertion.** Two
  assertions, in order:
  (a) **Dependency state.** Spec 073's
  executed record shows both products frozen
  (`registry-v2-freeze.json` and
  `asset-a-v2-freeze.json` present in its
  merged execution record under
  `specs/073-keying-surface-repair/`). If
  Spec 073 closed without either product
  frozen, this spec closes **NOT-RUN** (no
  gate run) or **CLOSED AT STEP 0 — ASSET
  NOT FROZEN** (the execution was ordered
  and reached this gate), in the words of
  §4.6; no further gate runs.
  (b) **Digest assertion.** The SHA-256 of
  Registry v2 and of the Asset A v2 canonical
  CSV, as presented, recompute to the
  digests this spec's freeze record quotes
  verbatim from Spec 073's executed record
  (its two freeze records), and the freeze
  record's per-kind counts for Asset A v2
  match the presented file's. A mismatch
  closes the execution as **ASSET PIN
  MISMATCH** (§4.6) before any join.
- **0.2 Shakti intake assertion (P-F1 S1 and
  S2).** Against the intake record of §3:
  **S1 — Identity:** the corpus file's
  SHA-256 recomputes to
  `345241b13fedada87b4783c24cd241123491bbd7edaf5bf636f9cdb36c01da68`
  and the row-grades file's SHA-256
  recomputes to
  `02394241773cf8700f49ba19c30cdbaa589cf119d2c97c35e15e0447434dd739`.
  **S2 — Census:** the corpus counts
  reproduce the audit's census: 5,704 rows;
  5,536 analyzable; grade counts 3,212
  documented-lineage / 2,087
  undocumented-corroborated / 405
  undocumented-uncorroborated; 4,904 of
  5,536 analyzable rows (88.6%) carrying a
  CISI identifier. Failure of S1 or S2
  closes the citing spec at step 0 as
  **SHAKTI INTAKE NOT REPRODUCED** (§4.6).
  S3/S4 failures are integrity findings,
  reported as such, not repaired silently.
- **0.3 Input integrity.** Every §3 input
  hashes to its freeze-record value —
  including `reports/phase433_results.json`,
  the recorded enumeration gate 0.4 runs
  against. A mismatch stops the run as
  **INVALID**.
- **0.4 Population enumeration, reproduction,
  and keying.** The §2 battery is run over
  the primary population (documented-lineage
  rows only); the opening-strong set O is
  enumerated in full in Wells space and
  **published as the execution's first
  product, before any join or test**; the
  enumeration is asserted against Spec 070's
  recorded enumeration — the same 31 signs,
  each with the same I/M/T counts as
  published in `reports/phase433_results.json`,
  and the full battery class census equal to
  Spec 070's recorded census (§1.3, change
  3). A difference in either closes the
  execution as **POPULATION NOT REPRODUCED**
  (§4.6), with the differing signs or census
  cells published. Every enumerated sign is
  then keyed to exactly one Asset A v2 row
  in Wells space under the two-leg keying
  route the freeze fixed (OPEN-074-2). A
  sign that cannot be keyed is a named
  finding of this gate, listed with its
  Wells identity and the reason; its
  disposition is the one the freeze stated
  in advance (OPEN-074-4) — either this gate
  closes the execution as **POPULATION NOT
  KEYED** (§4.6) with the observed list
  published, or the gate records the sign
  under the stated disposition and continues,
  with the finding carried into every
  product. The population is never quietly
  replaced by a nearby set — not by the
  Mahadevan set of Spec 049's replaced gate
  0.4, not by any other corpus's set, and
  not by a hand-completed version of its
  own list.
- **0.5 Comparison census and coverage.** U
  is enumerated with per-sign occurrence
  counts under the frozen counting rule; the
  unicorn sign(s) of S-B are named from the
  frozen asset's verbatim labels; the full
  battery class counts on the primary
  population are published; and every sign
  in O and in U is shown to carry an Asset
  A v2 row (keyed under the same two-leg
  route). A population sign with no Asset
  A v2 row stops the run as **INVALID** —
  an absent row is never treated as
  non-animal by default. The census (both
  sets, counts, classification tallies
  including contested and unidentified) is
  published with the outcome either way.
- **0.6 Freeze-order proof.** The record
  shows, in order: this spec froze, quoting
  the v2 digests from Spec 073's executed
  record and the recorded enumeration from
  Spec 070's; the population of gate 0.4 was
  published; and no join of Asset A v2 to
  the population precedes either. Absent
  that proof → **INVALID**: a population
  joined before it was published is not a
  frozen population.

## 6. Reporting obligations

Every product of an execution carries, in
its headline paragraph:

1. the claim identifier;
2. the **honesty fence** of the banner, in
   its own words: the framework measured on
   is the graded ICIT corpus, and the
   Phase-43 quantities (805/2,267;
   40/61/20) are not this spec's basis;
3. the **lineage statement** of §3 (P-F1
   S3), verbatim;
4. the Asset A v2 digest and its per-kind
   counts;
5. the gate 0.4 reproduction record (the
   enumerated set against Spec 070's
   recorded 31, sign by sign);
6. the full counts of §4.2 (every cell of
   both arms, both sets' sizes, the
   contested and unidentified tallies, and
   the per-sign classification table for O
   and for U);
7. R1, its exact-test p, R2, its p, and the
   headline word of §4.3 or the closure
   class of §9;
8. all three sensitivities' ratios and p
   values (or S-B's not-applicable
   statement), with the S-C grade-sensitivity
   statement where it applies; and
9. the fence sentence: "This result is about
   depiction and position in recorded data.
   It is not evidence that any sign marked
   identity, a guild, or goods."

Deliverables at execution: a results JSON
(censuses, the enumerated keyed population
list as the first product, both arms' tables
and tests, all sensitivities, the §5 gate
record), a report under these headline rules,
the experiment-graph node (H15/H23,
registered and verified before the run), the
outcome append in this directory, the dated
animal-half append to the claim's record,
and the LEDGER entry (H1). Foundation check
(H21) after the execution phase: 0 failures,
or the outcome record says why not. Anchors
asserted byte-identical before and after.

## 7. Risks and honest weaknesses

- **The population is a recorded measurement,
  and the successor stands or falls on
  reproducing it.** Gate 0.4's reproduction
  assertion is deliberately strict: on
  identical pinned inputs, any difference —
  one sign, one count, one census cell —
  closes the run as POPULATION NOT
  REPRODUCED. That is the conservative
  reading of what a successor on the same
  inputs is; a looser gate would let the
  join proceed on a population that is not
  demonstrably Spec 070's.
- **Keying may still fail.** The two-leg
  route resolved all 31 recorded signs at
  this draft, verified against the pinned
  files — but the execution re-derives the
  enumeration and re-runs the route, and a
  sign the draft-time check did not see
  (because the enumeration differed) is
  disposed of by gate 0.4's frozen rules,
  not by this paragraph.
- **Token 999 is named, not dropped.** Spec
  073's NO PUBLISHED IDENTITY schedule names
  one attested code, token 999, attested in
  the documented stratum, that no ruled
  published sign list identifies. It was not
  in Spec 070's recorded opening-strong set.
  If it enters O in a future enumeration it
  is unkeyable under both legs and gate 0.4's
  disposition governs; if it enters U with
  no Asset A v2 row, gate 0.5 stops the run
  as INVALID. Either way it is named in the
  gate record, never silently excluded from
  a set it belongs to.
- **Most of the repaired surface is
  unidentified.** Asset A v2 classes 211 of
  its 552 rows `unidentified` — the published
  record simply does not say what most signs
  depict. The primary's shares are computed
  over classified members only (§4.1), with
  the excluded tallies published; a small
  classified base can land the verdict
  INCONCLUSIVE on middling truths, as the
  bands of §4.3 say in advance. That is the
  design working, not a defect.
- **The documented population is smaller.**
  3,045 analyzable documented rows is the
  honest primary; the corroborated stratum's
  different composition is exactly why it is
  a sensitivity and not the primary.
- **One join, one layer.** The verdict is a
  statement about the published
  identification layer (§8, limit 2) on one
  positional framework measured on one
  graded corpus. It does not speak to the
  Phase-43 framework in either direction.

## 8. Epistemic limits (binding on all outputs)

1. **No meaning conclusion.** Even a clean
   SUPPORTED shows depiction and position
   coincide on this corpus; that animal
   signs marked identity, guild, or goods
   remains Hunt's reading, not a measurement
   of this test.
2. **Depiction is the field's published
   identification, not ground truth.** Asset
   A v2 records what the published lists say
   a sign depicts, with citations. A verdict
   under this spec is a statement about
   that layer.
3. **The 49% caution travels with the
   result.** Spec 037's census (object-type
   labels diverging in 49% of matched cases
   between compilations) is restated
   wherever this spec's result is stated.
   The asset's construction is the answer
   to it, not a refutation of it.
4. **The honesty fence is a limit, not a
   preface.** The re-scoped programme tests
   Hunt's claims against a positional
   framework measured on the graded ICIT
   corpus; it does not test them against
   the Phase-43 framework, and its outcome
   wordings must not cite 805/2,267 or
   40/61/20 as their basis (banner; §6).
5. **The lineage limit.** This corpus is an
   ICIT-lineage corpus; agreement with the
   programme's earlier ICIT-lineage layer is
   consistency within one tradition, not
   independent corroboration (P-F1 S3,
   stated in every headline block).
6. **The predecessors' records stand
   untouched.** Spec 049's draft and
   freeze-failure record, Spec 070's frozen
   contract and its POPULATION NOT KEYED
   closure, and Spec 073's executed record
   are records of what was decided and what
   happened; this spec appends a successor
   beside them and edits none of them. In
   particular, no outcome of this spec
   rewrites Spec 070's closure: the claim's
   record carries both attempts, each under
   its own spec, and a verdict under this
   spec is a verdict of this spec. The
   frozen outcome of Spec 045 is likewise
   untouched.
7. Negative, inconclusive, step-0-closed,
   and not-run outcomes publish with the
   same prominence as a supported one.

## 9. Stop conditions and outcome classes

Execution ends in exactly one of:

- **NOT-RUN** — gate 0.1(a): the repaired
  surface never frozen (dependency closure).
- **ASSET NOT FROZEN** — gate 0.1(a), the
  execution having been ordered.
- **ASSET PIN MISMATCH** — gate 0.1(b).
- **SHAKTI INTAKE NOT REPRODUCED** — gate
  0.2 (P-F1 S1 or S2).
- **POPULATION NOT REPRODUCED** — gate 0.4
  (the enumeration or the class census
  differs from Spec 070's recorded
  measurement).
- **POPULATION NOT KEYED** — gate 0.4, where
  the freeze-stated disposition so directs.
- **INVALID** — gates 0.3, 0.5, or 0.6.
- **SUPPORTED**, **NOT SUPPORTED**, or
  **INCONCLUSIVE** — per §4.3, after all
  gates pass.

## 10. Execution shape (gated; NOT run by this draft)

1. **Graph-first build** (H15/H23) — script,
   graph node, registration, verification.
2. **Step 0** (§5) — repaired-surface
   assertion, Shakti intake assertion, input
   integrity, population enumeration,
   reproduction and keying (the enumerated
   list is the first product), comparison
   census and coverage, freeze-order proof.
3. **Primaries** (§4) — the primary arm, the
   reversed arm, all three sensitivities.
4. **Outcome** (§6) — appended records only;
   anchors asserted byte-identical;
   foundation check reported as measured.

## 11. What this spec is not

Not a re-opening, amendment, or completion
of Spec 070 (its closure stands), not a
re-run of Spec 049 (its Mahadevan population
rule stays replaced, as Spec 070 replaced
it), not a reproduction of any Phase-43
quantity, not a build or re-derivation of
Registry v2 or Asset A v2 (those are Spec
073's, consumed here by digest), not a test
of the celestial half of Hunt's scheme (that
is Spec 071's successor question, which
stands on its own record), not a
decipherment, and not an authorisation to
execute. It is the one join and one exact
test the claim's record has always named as
its missing half — asked a second time, on
the surface Spec 073 repaired for exactly
this purpose, against the population Spec
070 measured and published.

---

*AI disclosure: drafted by an AI agent (Muse
Spark, via Muse) at the direction of Tristen
Pierson, per constitution §VI.*
