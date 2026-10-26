# WP9 — Bounded external and completeness studies: preparations

**Repair program:** Glossa Lab external-audit repair, 2026-10-26.
**Work package:** 9 of the governing brief (Work Package 9, “Prepare bounded external and completeness studies”).
**Status of this document:** Preparations only. All three studies below are **drafts, and remain drafts**. Nothing in this document is frozen, executed, or registered. Where a study is closed as unavailable, or gated on a named missing dependency, this document says so as its result — a preparation that honestly reports its gate is a completed preparation, not a failed one.
**Standing position, unchanged:** The script is not deciphered.

Method sources named by the brief are cited in §4, at title level from the brief only, with transfer assumptions. They are method sources. They are not evidence, and nothing in this document uses them to reopen any closed route.

---

## 1. Study A — Contact-zone: the sequence leg (the catalog leg already ran)

### 1.1 Reconciliation with the catalog leg that already ran — counts verified, not re-derived

The contact-zone work has two legs, and they have different standings. Confusing them is the main error this preparation exists to prevent.

**The catalog leg already ran** on 2026-10-26 (record: `2026-10-26-atlas-line1-catalog-leg.md`). This preparation verifies its stated headline counts against that leg record — it does not re-derive them, does not re-run the leg, and does not re-count the catalog:

- **121 rows — verified against the leg record.** The completed Laursen 2010 Table 1 catalog in program hands: **121 seals = 92 Gulf Type + 28 Gulf INDUS + 1 Gulf Linear-Elamite**, across 29 named sites.
- **28 Gulf INDUS — verified against the leg record.** The inscribed set: seals 1–27 and 56.
- The catalog’s shape, as the leg record states it: 93 of 121 seals (77%) come from Bahrain sites; the remaining 28 are spread across Mesopotamia (10), eastern Arabia / Kuwait (7), the Indus Valley (5), Iran (4), and 2 unlocated.

What the catalog leg established, filed at full strength in its own record and carried here without enlargement:

- the completed catalog’s composition and geography;
- a catalog-level size distinction: inscribed seals are larger in diameter (median 25.5 mm, n = 28, against 22.0 mm, n = 88, for uninscribed; Mann–Whitney p < 0.0001, surviving the record’s Bonferroni-corrected threshold of 0.01; the difference also holds within Bahrain alone: 27 against 22 mm, p = 0.0001). The record states plainly that this univariate check is consistent with — but does not test — the published multivariate shape separation it echoes;
- **both readings of the inscription geography, filed at full strength, because the catalog cannot decide between them:** (a) the *use reading* — the exemplars that traveled are the inscribed ones, the ones doing cross-cultural work; and (b) the *cataloging-bias reading* — an uninscribed round steatite seal found abroad is far less likely to be recognized, published, and gathered into such a catalog than an inscribed one, so the pattern’s strength is partly built into how the catalog was assembled. Any future citation of the geography pattern must carry both readings. Neither may be quoted alone as the leg’s result;
- the precise thinness of the western sign material actually held: the rebuilt seals-at-Mesopotamia file holds 11 inscribed records totaling 44 Indus sign tokens, but 10 of the 11 carry lengths only (placeholder sign identities), and exactly **one** record carries verbatim sign identities — the Janabiyah seal, 7 signs. The catalog contains no sign sequences beyond that one reading;
- the period shape of the cuneiform Meluhha record, including its learned tail (§1.3).

What the catalog leg does **not** establish, in its own record’s words: any sign-sequence statistic (the headline twins-sign rate remains a published claim by the catalog’s author, not a program measurement, and the different-language reading it supports remains contested); any language identity, sign value, or contact mechanism; and no step toward decipherment. Under the atlas’s own criteria, catalog-level co-occurrence is contact evidence, not a decipherment anchor.

**Catalog readiness and transcription readiness are separate standings, and this preparation keeps them separate throughout:** the catalog is complete and its leg has run — *catalog ready, leg closed*. The sequence material does not exist in program hands — *transcription not ready, leg gated* (§1.2).

### 1.2 What remains preparable: the sequence leg, and its precise missing dependency

**The sequence leg is the only part of this study that remains to prepare.** It would measure sign-sequence statistics on the Gulf inscribed material — the material the twins-sign question and any positional comparison actually need.

> **Precise missing dependency: a transcription of the CISI Vol. 3 inscription material — the sign sequences themselves, transcribed from the Vol. 3 plates and the associated inscription discussions.**

The completed catalog, like every version before it, contains no sign sequences beyond the single Janabiyah reading. No preparation, however complete, can substitute for the sequences. Until that transcription exists in a form the program may lawfully use, the sequence leg cannot be specified to freeze standard, because its input does not exist to be pinned.

**ACCESS STATUS: GATED — restricted material.** The CISI Vol. 3 material is restricted. This preparation records only what the fences allow: that the material exists, and that the leg’s access condition is **lawful access to that material for transcription, in the custody arrangement the program already uses for restricted material**. No restricted content is reproduced, summarized, or characterized here, and no access route is asserted beyond that condition. A second blocker from the catalog leg record is carried alongside: re-measuring the 121 catalog seals would be a replication of the catalog author’s count, not an independent test — the discriminating population named in that record is the wider Dilmun seal corpus (the catalog author’s later, larger corpus, approximately 800 seals), which this catalog does not contain. Any future freeze of the sequence leg must specify that wider corpus as its held-out arm, or state why its design does not need one.

### 1.3 Preparation specification (draft — to be completed only when the dependency lands)

**Exact inputs.**

Inputs that exist and are pinned (the catalog leg’s inputs, fetched from the repository main on 2026-10-26; the local checkout was not touched, and the restricted author copy was not used — the public rebuilt table on main is the input):

| Input | SHA-256 (as recorded in the leg record) | Content |
|---|---|---|
| `laursen_2010_table1.json` | `877f62b8…` (recorded in the leg record as matching the completion record’s post-merge pin exactly) | 121 rows — the completed catalog |
| `seals_at_mesopotamia.json` | `7fd04715…` | 14 records (rebuilt 2026-10-25) |
| `meluhha_tablets.json` | `b123c59e…` | 1,462 keyword hits among 135,255 ATF texts (rebuilt 2026-10-25) |

Input that does **not** exist yet, and must be pinned before any freeze:

| Input | Status |
|---|---|
| CISI Vol. 3 transcription (sign sequences for the Gulf inscribed material, with per-sequence provenance) | **Missing — the gating dependency (§1.2).** No hash can be given for an input that does not exist; inventing one is barred |

**Preconditions for any paired-name proposal** (a proposal pairing a name or term from the cuneiform record with Gulf / Indus material). All four must be established, per object, **before** any such proposal is drafted — they are preconditions, not supporting arguments assembled afterward:

1. **Object identity** — the object is one identified object, resolved under the object-family rules of Work Package 8, §2.1 (repeat impressions, duplicate publications, and duplicate transcriptions collapsed to their family, not counted as separate support);
2. **Manufacture and deposition dates** — both stated, with their sources, and their uncertainty carried (§1.4); a pairing whose dates cannot both be stated is not proposed;
3. **Pseudo-Indus status** — whether the object’s marks are Indus signs, pseudo-Indus marks, or unresolved, stated explicitly; unresolved status blocks a pairing that needs the marks to be Indus;
4. **Source quality** — the quality and revision of each source the pairing rests on, stated on the face of the proposal.

**Reference strings and attestation classes.** Every textual reference used by this study retains its **full reference string and its uncertainty** — no reference is shortened to a bare count in any working file or report. Attestations are classed, and the classes are never pooled:

- **Direct Meluhha attestations** — texts whose reference is to Meluhha itself, in a context of the contact period;
- **Broad contact-term hits** — keyword hits on the wider contact vocabulary, including later and learned uses.

The catalog leg record shows why pooling is barred: the rebuilt survey layer’s stored keyword tallies (dilmun 924, gu2-ab-ba 613, ma2-gan 371, me-luh-ha 215, among 135,255 ATF texts) support a count of **178 tablets carrying a me-luh-ha match**, of which the Neo-Assyrian group (53, overwhelmingly from Nineveh) is a learned lexical tradition roughly a millennium after contact ended, from a period when the term had come to designate a different region. The leg record’s own summary, carried verbatim in force: a raw count of Meluhha mentions overstates contact by roughly a third unless the first-millennium learned tail is separated out. Every count in any future sequence-leg or paired-name work must state its period profile and its attestation class beside the count.

**Explicit falsifier (sequence leg).** The sequence leg’s claim form, to be stated exactly in its own draft once its input exists, is that a named sequence statistic on the Gulf inscribed material differs from its stated comparison at a pre-committed bar. Its falsifier is the direct one: **the measured statistic, on the pinned transcription, does not differ from the comparison at that bar — or the transcription’s coverage is too thin for the statistic’s pre-stated precision floor, in which case the leg files INSUFFICIENT DATA rather than a result in either direction.** No sequence claim may be filed from the catalog leg’s material: the sequences are not in it (beyond the one 7-sign reading, which carries no statistical weight alone, as the leg record states for its single Linear-Elamite counterpart in the same terms).

**Statistical unit.** The inscription (one object-family-resolved inscribed object), with sign tokens nested inside it. Tokens are never the unit: tokens from one inscription are not independent observations, and any statistic must account for clustering by inscription and by object family (Work Package 8, §2.1).

**Controls.** Comparison material and nulls to be specified in the leg’s own draft before freezing, under Work Package 8’s suite where a discrimination claim is made — including, at minimum, the cataloging-bias reading of §1.1 carried as a standing rival explanation for any geography-based sequence claim, and the wider-corpus held-out arm of §1.2 where the design needs an independent test population.

**Thresholds.** None are frozen by this preparation, and none may be set after any sequence count is seen. The sequence leg’s draft — writable only once the transcription exists to be pinned — must state its statistic, its comparison, its bar, its precision floor, and its family-wise error treatment before its freeze. The catalog leg’s own practice is the model for the reporting standard: effect sizes with their sample sizes, raw and multiplicity-corrected readings both reported (the catalog leg tested five measurement variables at a corrected threshold of 0.01), and suggestive-but-uncorrected results filed as not established.

**Precision rationale (in place of a power rationale).** This is a bounded external study on a fixed, small, already-existing population — there is no sampling design to power. What can be stated in advance, and must be, is precision: the sequence population is at most the 28 Gulf INDUS catalog seals plus whatever the wider held-out corpus adds; per-statistic precision floors must be derived from that ceiling in the leg’s draft, and any statistic whose achievable precision at the real coverage falls below its floor files INSUFFICIENT DATA (per the falsifier above). The catalog leg’s measurement layer is the standing warning: disc height is missing for 47 of 121 rows, boss diameter for 39, grooves for 36 — catalog completeness is not measurement completeness, and sequence coverage will have the same structure.

**Stop rule.** The preparation stops here: **no further sequence-leg work until the CISI Vol. 3 transcription exists and is lawfully accessible.** Within any future execution, the stop rules are those of its own frozen draft, plus this package’s standing rule — a coverage or precision shortfall stops the leg at INSUFFICIENT DATA, and no threshold is adjusted after a count is seen.

**Registration plan.** No registration is filed by this preparation. If the sequence leg reaches a freeze, it is registered before execution by the program’s standing route, with the transcription’s pin, the catalog pins above, the statistic, the bar, and the precision floor in the registration. Until the dependency lands, there is nothing registrable, and this preparation does not pretend otherwise.

---

## 2. Study B — Numeral pilot: reconciled with the S2 draft as filed

### 2.1 The S2 draft as filed — what it actually proposes

The draft of record is `2026-10-26-spec-draft-s2-numeral-stroke-tally.md` — **DRAFT — NOT FROZEN; design only; nothing in it has been executed.** Its claim (S2-C01), in its own terms: the stroke-run forms — sign types whose glyph is a run of one to seven short strokes, enumerated at its Step 0 from Registry v2 forms cross-checked against the Mahadevan list, the set generated by script, hash-pinned at freeze, and never tuned afterward — constitute an additive tally subsystem: forms that encode quantity, combine additively, and are used where quantities are recorded. **One stroke family** is in scope: that single run-of-strokes family, lengths 1 to 7. No other sign family is tested, and the draft’s boundary is explicit and carried here in full force: the test touches stroke forms only, it does not touch the fish-sign area, and nothing from it may be phrased as a fish reading.

The draft tests the claim on three separately falsifiable legs, all of them **corpus-internal**:

- **Leg 1 — Frequency profile:** token frequencies fall monotonically as run length grows, among run lengths meeting a 30-token scoring floor; bar: zero inversions among scored lengths.
- **Leg 2 — Additivity of contexts:** each scored run length’s context distribution (adjacent-sign identities, left and right pooled, plus positional slot) matches the pooled contexts of the shorter runs, at or below the 5th percentile of a 9,999-draw permutation null (Bonferroni-adjusted within the family); plus a neighbor-diversity sub-leg at or above the 95th percentile.
- **Leg 3 — Object-class concentration:** stroke-run tokens concentrate on quantity-bearing object classes (tablet, pot, sealing — the Harappa miniature tablets the pre-declared primary sub-corpus) above the 99th percentile of a label-shuffling permutation distribution **and** at an odds ratio of at least 2.0 against the corpus-wide baseline; Leg 3 is scored only if object-class labels exist for at least 80% of inscriptions carrying stroke-run tokens, else it files INSUFFICIENT DATA and the claim cannot be filed SUPPORTED on two legs.

Its instrument pilot, pre-committed in the draft before any S2 number exists: planted tally recovery in at least **17 of 20** seeded synthetic corpora built at the pinned population’s scale; frequency-matched negative controls producing the full signature in at most **1 of 20**; and a structured-generator leg (the draft answers its applicability question explicitly: **yes, it applies**) in which the instrument must refuse the full signature in at least **19 of 20** seeded generator runs — a pilot without that leg is INCOMPLETE — S4 LEG OUTSTANDING and licenses no freeze. Its population is the pinned census frame (as of the draft: 3,045 inscriptions / 557 signs / 11,805 tokens), with a re-derivation rule if a successor registry changes the signary before S2 freezes. Its scoping-count log records that no real-corpus stroke-run token frequency was inspected in drafting and no bar derives from one.

**Claims separation, as the draft supports it and no further.** The draft’s three legs, if passed under a validated instrument, could support a **quantity** claim only: that these forms encode quantity and combine additively. They support no **unit** claim (what is being counted *in* — no leg tests a unit), no **commodity** claim (what is being counted — object-class concentration shows where tallies are used, not what they tally), and no **pronunciation** claim (how any form sounded — no leg touches sound). Any future proposal asserting a unit, a commodity, or a pronunciation is a separate claim needing its own evidence, and may not cite an S2 pass as its support.

**Alternative systems and accidental fits, as the draft provides them.** The draft’s rival analysis names the non-numeral processes its legs are chosen against (decorative hatch / filler; a pure scratch-tally without arithmetic use; stroke-shaped ownership or workshop marks), and its controls include frequency-matched non-stroke sign sets and the structured-generator leg. A fuller alternative-systems treatment — stating, as explicit rival numerical systems (for example, a non-additive stroke code, a bundled/grouped tally, a length-as-identity system in which each run length is simply a different sign), what each rival predicts on each leg — is **not** in the draft as filed. It is recorded here as a gap a validation design would have to close, which matters because of §2.2.

### 2.2 The hard rule applied: independent constraints — do they currently exist?

The brief’s rule for this study is a hard rule, not a preference:

> Choose independent quantitative constraints **before** fitting. If no independent constraints exist, close the validation pilot as **unavailable** and retain exploratory proposals separately, labeled exploratory.

An independent quantitative constraint, in the sense this rule needs, is a quantity known from outside the corpus-fitting exercise itself — a number the tally system, if real, must match, known before and independently of counting stroke runs: for example, an independently established count, capacity, or total associated with the objects the tallies appear on, against which the tally reading can be checked arithmetically. That is what made tallies in the regional precedent checkable: the arithmetic could be tested against something that was not itself the tally.

**Finding, stated from the S2 draft as filed: no such independent constraints currently exist in the draft, and none are named in it.**

The draft’s tests are, by its own construction, corpus-internal signatures (frequency shape, context additivity, object-class concentration), validated by synthetic planted controls and by controls drawn from the same corpus family. Those are instrument controls — they test whether the instrument can find a tally it planted and refuse ones it did not. They are not independent quantitative constraints on the Indus material: nothing outside the stroke-run counts themselves states a quantity that a real tally reading must reproduce. The draft names no external quantity, no associated count, and no arithmetic check against an independently known total. This preparation does not invent one, and does not re-describe a corpus-internal leg as an independent constraint to avoid the rule’s consequence.

### 2.3 Disposition

> **The numeral validation pilot is CLOSED AS UNAVAILABLE** under the brief’s hard rule, for the stated reason: no independent quantitative constraints, chosen before fitting, currently exist against which a tally validation could be run.

This closure is a disposition of the *validation pilot*, on the *constraint* ground. It is not a verdict on the stroke-run forms: it establishes nothing about whether they are numerals, and it must not be reported as a failure of the tally claim, any more than as support for it. The claim was not validated because the kind of check that validates tally claims — an arithmetic match against an independently known quantity — cannot currently be set up.

Everything else is retained, separately and labeled:

- **Exploratory proposals retained, labeled EXPLORATORY:** the S2 draft in full — its claim form, its three corpus-internal legs, its bars, its pilot design, its scoping-count log — is retained exactly as filed, as an exploratory proposal. Corpus-internal exploratory work under that draft, if the owner separately authorizes any, must be reported as exploratory signature description, never as validation, and its outputs must carry the label and this section’s reason with them.
- **What would reopen the validation pilot:** a future design note that names at least one independent quantitative constraint — its source, its pin or revision, why it is independent of the stroke-run counts, and why it was chosen before any fitting — and adds the alternative-systems treatment noted in §2.1. Reopening is a new draft act by the owner’s word, judged on that note. It is not effected by this preparation.

For completeness, the preparation fields the brief requires are recorded for the (closed) validation pilot, so the closure is auditable rather than asserted:

- **Exact inputs (as the draft pins them):** the pinned census frame (3,045 inscriptions / 557 signs / 11,805 tokens as of the draft); Registry v2, SHA-256 `42ab09fb06750098dc8cc0370c4ba4c1a538353d943a49f983d7347f52e8ef71`; the stroke-run set to be enumerated and hash-pinned at the draft’s Step 0 (not yet enumerated — no hash exists, and none is invented here).
- **Explicit falsifier:** as drafted, any of the three legs failing at its pre-committed bar files the claim NOT SUPPORTED with the failing leg named. That falsifier belongs to the validation pilot and is inoperative while the pilot is closed as unavailable — an inoperative falsifier is not a failed claim, and the distinction must be preserved in every summary.
- **Statistical unit:** the inscription for object-class and context statistics; the run-length class (lengths 1–7, subject to the 30-token scoring floor) for the frequency leg. Tokens nested in inscriptions are not independent units.
- **Controls:** as drafted — planted synthetic recovery, frequency-matched non-stroke negative controls, permutation nulls, and the structured-generator leg (§2.1). Alternative numerical systems as explicit rivals: not in the draft as filed (§2.1, gap recorded).
- **Thresholds:** as drafted and pre-committed in the draft (§2.1) — recorded here as the draft’s numbers, not adopted as operative bars for any validation, because the validation pilot is closed.
- **Power / precision rationale:** as drafted — the 30-token floor is the draft’s stated precision floor (below about 30 tokens, a single inscription’s presence or absence reverses an inversion judgment, so the length is reported but not scored), and the planted-recovery convention (17 of 20) is the draft’s adopted house convention, not a fit to this problem. No independent-constraint power rationale exists, because no independent constraint exists — that absence is the closure ground, restated here so the field is not left blank.
- **Stop rule:** the closure itself is the stop: **no validation run, no freeze preparation, and no registration step for the numeral validation pilot until the reopening condition in this section is met.**
- **ACCESS STATUS: NOT ACCESS-GATED.** The draft’s inputs are held, non-restricted corpus material. This study is gated on evidence (no independent constraints), not on access, not on human review, and not on any owner decision other than the reopening act itself.
- **Registration plan:** none, while closed. A reopened validation design registers before execution by the program’s standing route, per the S2 draft’s own freeze requirements (owner’s freeze word; registration before any execution; the freeze record containing the hash-pinned stroke-run set, the pinned census, the object-class list, the permutation seeds, and the family’s numerical error rates — plus, on reopening, the named independent constraint and its pin).

---

## 3. Study C — Completeness: three coverages, reported separately

### 3.1 Design principle and the absolute bar

“How complete is the record?” is three different questions, and this design reports them as three different numbers, from three different calculations, under three different assumptions. It never merges them.

> **Absolute bar: no single global completeness percentage, and no decipherment percentage, may be output by this design — or quoted from it — without defensible population and sampling assumptions stated beside the number. A number produced without those assumptions is not a conservative estimate; it is an invented one, and this design does not produce it.**

This is a descriptive / estimation design. Following Work Package 8, §4, it requires accurate provenance and stated uncertainty. It does **not** require a fake-language control, and no power requirement is imposed on it in the validation sense; what it requires instead is the precision discipline of §3.4.

### 3.2 The three coverages

**Coverage 1 — Catalog digitization coverage.** Of the objects in a named catalog frame, what share are digitized in the program’s holdings, at what level (catalog row only / measurements / image / transcription)?

- Numerator and denominator both come from the named catalog frame, and the frame is named in every report: a coverage figure “of the Laursen catalog” and a figure “of the wider Dilmun corpus” are different figures about different frames, and neither stands in for the other.
- Reported by level: an object counted as digitized at the transcription level is also counted at each lower level, and the levels are reported as a table, never collapsed to one share. The catalog leg’s measurement gaps (§1.3: disc height missing for 47 of 121 rows, and so on) are this coverage’s texture, reported with it.
- This coverage is a holdings fact. It carries counting uncertainty only (disputed identity, duplicate records), resolved under Work Package 8’s object-family rules, and that resolution is reported with the figure.

**Coverage 2 — Within-stratum sampling coverage.** Within each named stratum — **site, period, and medium**, as the brief specifies — what share of the stratum’s digitized material has actually been sampled into the program’s analyzed populations?

- Reported **per stratum**, as a table of stratum, frame size, sampled size, and share. A pooled share across strata is not reported: pooling hides exactly the imbalance this coverage exists to show (a catalog that is 77% one island’s sites, as in §1.1, would pool into a reassuring number that describes no real stratum).
- Strata with no sampled material are reported as empty strata, by name. An empty stratum is a finding about where the analyzed population cannot speak; it is never dropped from the table to make the remaining coverage look complete.
- Alternate sign inventories are applied at this level too (§3.3): a stratum’s sampled sign count is stated under each inventory in force, where they differ.

**Coverage 3 — Historical missingness.** Of the material that once existed, what share is estimated not to survive, or to survive unrecovered — and therefore cannot be in any catalog, digitized or not?

- This is the only one of the three that is an **estimate about an unobserved population**, and it is labeled as such wherever it appears. Its inputs are the attested frequency structure (how many signs are seen once, twice, and so on — the frequency-of-frequencies), and its method family is the unseen-items estimation family cited in §4 (Chao & Jost 2012, as a method source).
- Reported as an **interval, with its assumptions named**: the estimator used, the population definition assumed, and the sensitivity of the interval to that definition. A point estimate of historical missingness, reported without its interval and its assumed population, violates the absolute bar of §3.1 and is not produced.
- Historical missingness is never added to, subtracted from, or averaged with Coverages 1 and 2. The three answer different questions about different denominators, and any combined figure would inherit none of their meanings.

### 3.3 Resampling and alternate inventories

- **Object-family resampling.** Uncertainty for Coverages 2 and 3 is computed by resampling **object families** (Work Package 8, §2.1), not individual rows or tokens: repeat impressions and duplicate records of one object move together in every resample. Row-level resampling would understate uncertainty by treating copies as independent evidence.
- **Strata in every resample.** Resampling is done within the site / period / medium strata of Coverage 2, so that interval widths reflect the actual stratified structure rather than a pooled fiction.
- **Alternate sign inventories.** Every sign-count output of this design is computed under each sign inventory in force and reported side by side where they differ. The program’s own record shows why this is not optional: substantially the same excavated material yields **527** distinct sign ids in the Mahadevan-frame subset of the pinned export, **535** in the whole multi-source export, **557** in the primary population, and **584** in an external 2026 digitization named in the program’s records. Signary size is a property of the carving, not a constant of the script. A completeness figure computed under one inventory and quoted without naming it has hidden its largest assumption.

### 3.4 Preparation specification (draft)

- **Exact inputs.** The pinned census frame (3,045 inscriptions / 557 signs / 11,805 tokens); Registry v2, SHA-256 `42ab09fb06750098dc8cc0370c4ba4c1a538353d943a49f983d7347f52e8ef71`; the completed contact-zone catalog inputs of §1.3 (pins as recorded there), for Coverage 1’s catalog frame; and each alternate inventory named with its source and pin where one exists in the staged records (the Mahadevan-frame and whole-export counts above are carried from the program’s rerun-invalidation audit record, with their frame definitions, and must be re-pinned from source in the study’s own Step 0 before any computation — a count carried from an audit record is a scoping figure, not an input pin).
- **Explicit falsifier.** This is an estimation design, and its falsifier is a backtest, stated before any headline estimate is computed: **fit the estimator on a stated fraction of the inscriptions (the originating scan’s design used a random 80%, with split-half checks by site), and the number of genuinely new signs in the held-out remainder must fall inside the predicted interval. If it does not, the estimate is withdrawn and the method is reported unfit at this scale.** A withdrawn estimate is a result and is filed as one.
- **Statistical unit.** The object-family-resolved inscription. Signs are the items whose unseen count is estimated; inscriptions (grouped by family) are the sampling units resampled.
- **Controls.** The backtest above is the design’s control. Split-half checks by site guard against one site’s habits masquerading as the script’s inventory. No fake-language control is required or imposed (Work Package 8, §4; §3.1).
- **Thresholds.** The backtest’s interval-coverage requirement (the held-out new-sign count inside the predicted interval) is the design’s pass/fail threshold, stated per estimator before fitting. Interval widths are reported, not thresholded into a verdict: a wide interval that honestly covers is a usable result; a narrow one that fails its backtest is withdrawn.
- **Precision rationale.** Precision is the design’s currency: every estimate is reported with its family-resampled interval, per stratum where the design is stratified, and the report must state the achieved interval width beside each estimate so that a reader can see what the data actually bought. Estimates whose intervals are too wide to distinguish the stated alternatives are reported as uninformative — a named outcome, not a failure to be repaired by pooling strata or inventories after the fact.
- **Stop rule.** If the backtest fails for every estimator the draft names, the study stops and files **METHOD UNFIT AT THIS SCALE** with the backtest numbers, and produces no headline completeness estimate. If a stratum or inventory cannot be pinned from source at Step 0, that stratum or inventory is reported as unpinned and excluded by name — the study does not proceed on a carried scoping figure as if it were an input.
- **ACCESS STATUS: AVAILABLE.** The design’s inputs are held program material. No restricted content is needed for the design as specified; if a future draft extends Coverage 1 to a restricted catalog frame, it records that frame’s existence and access conditions only, under the standing fences.
- **Registration plan.** As a descriptive / estimation study, this design registers its protocol (inputs and pins, strata, inventories, estimators, backtest rule, and the §3.1 absolute bar) by the program’s standing route before computation, if its draft names a registration — and in any case freezes its Step 0 pins and its backtest rule in its own record before any estimate is computed, so that the backtest cannot be re-aimed after the held-out count is known. **Draft remains draft until those conditions are met.**

---

## 4. Method and benchmark sources — cited as method sources only

The brief names six method / benchmark sources. They are cited here **as method sources, with transfer assumptions documented**, exactly as the brief directs. Nothing beyond the brief’s naming — author, year, and the brief’s own short characterization — was fetched or summarized for this preparation. Any fact about these sources beyond that naming is an **open gap**, recorded as such, to be closed by reading the source in full before any study that rests on it is frozen.

| Source (as named in the brief) | Used in this preparation as | Transfer assumptions — what must be true for the transfer to hold, stated so a freeze review can judge them | Open gap |
|---|---|---|---|
| Born et al. 2023 (clustering and numeral work) | Method source for image-and-context clustering of sign inventories, and for subsystem (numeral) treatment | That a clustering method validated on scripts with known inventories transfers to a script with no known inventory only through a known-inventory control at the new scale; that numeral-subsystem precedents from other scripts state a possibility, not an expectation, for this corpus | Full text not read for this preparation; the method’s stated operating conditions are unverified here |
| Born et al. 2022 (structural work) | Method source for structural analysis of undeciphered material | That structural statistics carry the same meaning at this corpus’s scale and inscription lengths as at the source’s; that scale difference is itself a stated risk in Work Package 7, §3, and Work Package 8, §5 | Full text not read for this preparation |
| Dahl 2005 | Method / benchmark source for the contact-zone and numerical-administrative context, as named in the brief | That administrative and numerical practices documented for the source’s material and period are comparable to the Gulf contact setting only where period, medium, and object class match — each pairing must argue comparability, not assume it | Full text not read for this preparation; which specific claims transfer is unadjudicated |
| Luo et al. 2021 | Method source for decipherment-against-a-relative approaches | **The transfer assumption fails by default and must be argued, not assumed:** this method family presupposes a known related language, and for this script the related language is the very thing in dispute. The program’s scan record already killed neural decipherment against a posited relative on exactly this ground. This citation therefore functions as a boundary marker — a named method whose precondition this program does not have — not as a design resource for any study in this package | Full text not read for this preparation |
| Dwork et al. 2015 | Method source for disciplined reuse of held-out data (the exposure / adaptive-analysis problem that Work Package 8’s registry addresses) | That the source’s account of overfitting through repeated adaptive reuse applies to this program’s reuse of its census frames and coding files — the registry design of Work Package 8 is this program’s operational answer, and does not depend on any specific theorem of the source | Full text not read for this preparation; no specific result of the source is relied on |
| Chao & Jost 2012 | Method source for unseen-items / coverage estimation (Study C, Coverage 3) | That frequency-of-frequencies estimation developed for sampled populations transfers to a historical corpus only under a stated population definition and sampling assumption — which is why Study C reports an interval with its assumptions named, per stratum, and never a single global figure | Full text not read for this preparation; the estimator’s exact form must be taken from the source, in full, before Study C’s draft can be frozen |

> **Fence, stated once and binding on all three studies:** these sources are **not** evidence reopening the closed simulated-annealing (SA), M1, or M2 routes. A method source can inform how a future study is designed. It cannot rehabilitate a closed route’s verdict, supply the independent evidence a closed pilot lacked, or stand in for a control a future study must run itself. Any draft that cites one of these sources in a way that has that effect has misused it, and its freeze review must catch the misuse.

---

## 5. Package status

| Study | Status |
|---|---|
| A — Contact-zone sequence leg | **Prepared, gated.** Catalog leg verified as already run (121 rows / 28 Gulf INDUS, both geography readings carried). Sequence leg gated on the **CISI Vol. 3 transcription** — the precise missing dependency; restricted material, existence and access conditions only. Catalog readiness and transcription readiness kept separate |
| B — Numeral pilot | **Validation pilot CLOSED AS UNAVAILABLE** — no independent quantitative constraints, chosen before fitting, exist in or are named by the S2 draft as filed. The S2 draft is retained separately, labeled **EXPLORATORY**. Not access-gated. Reopening requires a new design note naming an independent constraint, by the owner’s word |
| C — Completeness | **Prepared, draft.** Three coverages designed to be reported separately (catalog digitization / within-stratum sampling / historical missingness), with object-family resampling, site-period-medium strata, alternate inventories, a backtest falsifier, and the absolute bar on any single global completeness or decipherment percentage. Inputs available; draft remains draft until its Step 0 pins and backtest rule are frozen in its own record |

**No study was executed, frozen, or registered by this work package.**
