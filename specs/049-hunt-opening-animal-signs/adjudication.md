# Spec 049 — Adjudication Record

> ## ADJUDICATION INPUT — 2026-10-21
>
> This spec has two adjudication inputs,
> recorded here so the draft's basis is
> inspectable:
>
> 1. **The runnable-experiments campaign
>    plan, approved by the owner as written
>    on 2026-10-21**
>    (`~/workspace/your_files/2026-10-21-runnable-experiments-campaign-plan.md`,
>    Parts 1–4; decisions E-1…E-7 as written).
>    Under the plan, D-06 is member 5, a
>    dependent drafted in Wave 1 after the
>    asset builders, and it consumes Asset A
>    by the digest Spec 045 freezes (E-6,
>    requirement R-2).
> 2. **The portfolio triage of 2026-10-21**
>    (`~/workspace/research_notes/design-portfolio-triage-2026-10-21.md`):
>    design D-06 found **RIPE** — "The 40
>    opening-strong signs are on record
>    (Phase-43); the animal half needs only
>    the same shared published-identification
>    classification as D-05, then one join
>    and one exact test."
>
> These inputs commission this **draft**.
> They are not a freeze order and not an
> execution order for Spec 049: both remain
> separate later acts under the campaign's
> Waves 2 and 3.

## 1. The adopted basis (operative substance)

- **The design.** D-06 in the PR #195
  experiment-design packet
  (`docs/research/experiment-designs-2026-10-13/02-roif-and-hunt.md`,
  §D-06): one join (the shared classification
  against the 40 opening-strong signs) and one
  exact test (animal share among the 40 versus
  the animal share of all signs with at least
  30 occurrences), plus a pre-registered
  reversed arm; criteria SUPPORTED (ratio at
  least 1.5, exact test at the 5% level,
  primary arm) / NOT SUPPORTED (ratio at or
  below 1.0, or the test cannot reject
  equality) / INCONCLUSIVE (between, or the
  arms disagree); controls (the ≥30-occurrence
  restriction in both arms; contested-sign and
  unicorn sensitivities); the limit that
  position plus depiction is not meaning.
- **The claim.**
  `without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_003`:
  IN QUESTION, partially supported (positional
  half only); falsification condition of
  record: "Faunal signs not enriched in
  initial position above random baseline."
- **The asset.** Asset A, per Spec 045 §2 and
  campaign Part 3 / E-6: built and frozen
  inside Spec 045, consumed here by digest
  only. This spec's §2 restates the contract
  parts the test depends on; Spec 045's text
  governs in any difference.
- **The caution.** Spec 037's census:
  object-type labels diverging between
  compilations in 49% of matched cases —
  carried in spec §2.4, §8 limit 3, and claim
  F049-C16, as Spec 045's §8 requires of every
  consuming specification.

## 2. Verification record at draft

Verified first-hand at drafting, 2026-10-21,
via the GitHub API against `main` at
`83b6a563…` (the local checkout was not
touched, per the drafting order):

- **Design D-06** — read in full: the
  question, hypothesis, falsifier (animal
  signs at or below the inventory-predicted
  rate), data (the 40 from Phase-43; the
  shared classification), method (one join,
  one test, reversed arm), criteria, controls,
  and the not-established line (identity,
  guild, goods not established).
- **Designs D-05 and D-13, packet README** —
  read for the shared-asset description and
  the contracts either side of this one:
  D-05 builds the asset this spec consumes;
  D-13 consumes the same asset's sky class
  and is not this spec's business.
- **Spec 045's draft** — `spec.md` and
  `adjudication.md` read in full on branch
  `spec-045-hunt-depicted-kinds-draft`
  (PR #244): the Asset A contract (fields,
  hierarchy — held CISI Vols 1–2 govern,
  Parpola where CISI is silent — blind entry,
  dispute rule, D-18 input form, freeze point
  and `asset-a-freeze.json` digest pinning),
  and its direction that dependents quote the
  digest verbatim and assert it before any
  join. Spec §2 and gates 0.1–0.2 are written
  directly from that text. Spec 045's
  `claims.json` and `tasks.md` were read for
  register and lifecycle form.
- **The claim record** — read on `main`:
  `…_manual_003`'s normalised claim, evidence
  sentence, and falsification condition, as
  quoted in spec §1 (claim F049-C02).
- **Input pins** — recomputed at this draft
  from `main`: positional record `0e546962…`
  (805/2,267 formula context; 40/61/20 strong
  classes; mean initial rate 0.757 vs 0.251),
  Phase-43 record `78a6c219…`, corpus layer
  `c02e3d7b…` (the same value Specs 042 and
  045 pin), crosswalk master `4ace1a61…`,
  anchors `df0cf620…`.
- **The population-list search** — the two
  pinned records and the repository were
  searched for an enumerated list of the 40:
  `hunt_tripartite_test.json` stores counts
  only; `phase43_all.json` T2.2 stores counts
  (`initial_strong_count` 40,
  `total_signs_profiled` 201) plus a
  terminal-strong list, but no initial-strong
  list; the latent-class report in the repo is
  a different classification (45 members,
  Mohenjo-daro only, a different identity
  space); Phase-45's output is a different
  definition (75 initial-strong signs under
  Holdat-role thresholds). No enumerated
  Phase-43 list exists in the records
  checked. Recorded as a defect in §5,
  item 1 — the draft pins the population by
  definition and gates its enumeration
  (gate 0.4) rather than pretending a list
  was pinned.
- **The identity-space census** — the pinned
  crosswalk was read in full at this draft:
  205 rows, 187 distinct registry identities;
  `mahadevan_1977` mappings: **17 rows** only,
  against Phase-43 signs expressed as
  `m77_sign`. Recorded in §5, item 2.
- **Phase-number state** — as in Spec 042's
  and Spec 045's records: Phase-400…403 are
  allocated (Specs 036/038/037/039); Spec 040
  allocated none. Spec 049 allocates none at
  draft (DD-049-8).
- **Not done at draft, by design** — Asset A
  has **not** been built and no digest exists
  to quote; the 40 have **not** been
  enumerated; no occurrence count, join, or
  test quantity was computed; no code was
  written or run; the AEE hooks have not run;
  and nothing was filed with OSF.

## 3. Doubly derived acceptance tests (doctrine record)

Per the autonomous-execution doctrine, each
claim's acceptance test was derived twice,
independently: **Derivation A** from the
requirement text of the claim alone, and
**Derivation B** from the design's falsifier,
gates, the Asset A contract, and campaign
requirements (R-2, R-3) without reference to
A. Where A and B agreed, the register carries
the agreed test. Three disagreements arose;
each is recorded here with its resolution,
and the register follows the resolution:

1. **F049-C10's test table (primary arm).**
   A, from the design's wording alone, formed
   the exact test on the two stated shares
   directly — the 40 against all ≥30 signs —
   although the sets overlap (opening-strong
   signs with ≥30 occurrences sit in both),
   which no exact test on independent samples
   licenses. B, from test validity, required
   disjoint samples. **Resolution: B for the
   test, A for the ratio.** The enrichment
   ratio R1 keeps the design's stated baseline
   (the animal share of all of U); the exact
   test runs on the disjoint table (O versus
   U∖O). Both shares and every cell are
   published, so either construction is
   recomputable by any reader (DD-049-4).
2. **F049-C11 (contested signs).** A, from
   design D-06 alone, placed contested signs
   in the primary as classified, with a
   "rerun without them" sensitivity — the
   design's own words. B, from Spec 045 §2.5,
   excluded contested signs from the primary:
   the asset contract postdates the design,
   binds every consumer identically (campaign
   R-2), and a consumer that re-included
   contested signs in its primary would no
   longer be testing against the same asset
   as its siblings. **Resolution: B.** The
   design's sensitivity intent is preserved
   in inverted form as S-A (contested
   *included* under CISI-governed labels), so
   the exclusion's effect is still measured
   (DD-049-2).
3. **F049-C05/C10 (the reversed arm's role).**
   A, from the design's criteria alone, read
   SUPPORTED as a primary-arm-only judgement
   and the reversed arm as published
   description. B, from the design's
   INCONCLUSIVE clause ("or the arms
   disagree"), read the reversed arm as
   verdict-bearing. **Resolution: B, with the
   falsifier's precedence.** The reversed arm
   can veto a SUPPORTED into INCONCLUSIVE,
   but it cannot create a SUPPORTED, and it
   cannot override the falsifier: a primary
   ratio at or below 1.0 (or a primary test
   that cannot reject equality) is NOT
   SUPPORTED however the reversed arm lands,
   because the claim's own falsification
   condition is stated on the primary
   direction. The ordered criteria of spec
   §4.3 encode exactly this (DD-049-3).

## 4. Draft-fixed readings — DECIDED-BY-DRAFT

Each stands unless the freeze overturns it
openly:

- **DD-049-1 — Consumption only.** This spec
  never builds, extends, or re-derives
  Asset A; the animal set is the frozen
  asset's `depicted_kind = animal` rows
  (claim F049-C06).
- **DD-049-2 — Contested signs are out of
  the primary.** Per §3, disagreement 2: the
  asset contract governs over the design's
  older sensitivity phrasing; S-A measures
  the exclusion (claims F049-C11, F049-C12).
- **DD-049-3 — The criteria are ordered.**
  The design lists its SUPPORTED / NOT
  SUPPORTED / INCONCLUSIVE clauses without
  ordering them for mixed cases, and gives
  the reversed arm no bands of its own. Spec
  §4.3 orders them (falsifier first, then
  SUPPORTED with the reversed arm's
  non-contradiction, then INCONCLUSIVE) and
  §3, disagreement 3 records why.
- **DD-049-4 — "Exact test" is Fisher's.**
  The design says "exact test" and names no
  test and no sidedness. The draft
  operationalises it as Fisher's exact test
  on the disjoint tables of §4.2, the
  criterion p one-sided in the enrichment
  direction, the two-sided p published
  alongside. The freeze confirms or replaces
  this openly (§6, item 3).
- **DD-049-5 — Counts come from the pinned
  corpus layer.** The design does not name
  the corpus its ≥30-occurrence counts are
  taken from (§5, item 3). The draft reads it
  as the pinned corpus layer of record — the
  only corpus layer both sibling drafts
  (042, 045) already pin — with the counting
  rule itself fixed at the freeze (§6,
  item 2).
- **DD-049-6 — No floor is invented.** The
  design names no minimum size for U and no
  THIN outcome; the draft adds none. The one
  degenerate case (no animal signs among U's
  classified members, so the ratio is
  undefined) is an INCONCLUSIVE sub-case with
  the census as its finding (spec §4.3,
  rule 3), not a new outcome class.
- **DD-049-7 — Evidence carries
  `observed_at` from the draft.** As in Spec
  042's DD-042-4 and Spec 045's DD-045-7: the
  cited facts were verified first-hand
  today.
- **DD-049-8 — No execution phase number at
  draft.** Allocated at the freeze act, from
  the merged record as it then stands.

## 5. Defects and ambiguities found in the design and record, and their handling

1. **The 40 are on record as a count, not as
   a list.** D-06's data line says "the 40
   opening-strong signs from the recorded
   Phase-43 result", and the triage repeats
   "on record" — true of the count, the
   rates, and the profiled total (201), but
   no record checked at this draft (§2)
   enumerates the members, and the Phase-43
   battery code that produced T2.2 is not in
   the repository. Handled by pinning the
   population by definition (spec §3) and by
   gate 0.4 (reproduce, enumerate, key,
   publish — or close POPULATION NOT
   REPRODUCED). **The freeze must fix the
   reproduction rule** (§6, item 1); if no
   rule can be fixed from records of record,
   this spec cannot honestly freeze, and
   that is a freeze outcome, not a drafting
   improvisation. Not a drafting failure: the
   design's test, criteria, and falsifier are
   all fully stated; Spec 045's gate 0.2
   already presupposes the same reproduction
   of the 40/61/20 classes.
2. **The identity spaces do not meet
   cleanly.** Phase-43 expresses signs as
   Mahadevan numbers; Asset A is keyed by
   crosswalk identity; the pinned crosswalk
   carries only 17 `mahadevan_1977` rows.
   Keying the enumerated 40 into the asset's
   space is therefore a substantive act, not
   a clerical one. Handled by making keying
   part of gate 0.4 under a rule the freeze
   fixes (§6, item 1) — candidate routes the
   freeze may weigh include the CISI/Parpola
   numbers Asset A rows themselves carry —
   with failure closing the spec rather than
   being hand-keyed around.
3. **The count corpus is unnamed.** D-06
   fixes the ≥30-occurrence restriction but
   not the corpus the occurrences are counted
   in; Phase-43's own profiled corpus was a
   Firestore-sourced layer, while the
   programme's pinned layer of record is the
   corpus Specs 042/045 pin. Handled by
   DD-049-5 (draft reading) and OPEN item 2
   (the freeze confirms the corpus and fixes
   the counting rule, or substitutes a pin).
4. **The design's criteria are un-ordered
   for mixed cases, and its "exact test" is
   unspecified.** Handled by DD-049-3 and
   DD-049-4, both flagged for the freeze to
   confirm or overturn openly (§6, item 4).
5. **No defect in the falsifier.** The
   falsifier is the claim record's own
   sentence; the thresholds (1.5 / 1.0 / 5%)
   and both sensitivities are the design's.
   This draft invented none of them.

## 6. OPEN-for-freeze items

The freeze decision is asked to decide:

1. **The population rules (the freeze's main
   work).** The reproduction rule by which
   gate 0.4 re-derives the Phase-43
   initial-strong set from records of record,
   and the keying rule by which enumerated
   signs resolve to Asset A rows (§5,
   items 1–2). Neither rule exists at draft;
   both must be recorded in the freeze record
   before any execution.
2. **The count corpus and counting rule.**
   Confirm DD-049-5 (the pinned corpus layer)
   or substitute a named, pinned corpus; fix
   what counts as an occurrence (the draft
   proposes sign-token occurrences in the
   layer's text field) and record it.
3. **The exact test's form.** Confirm
   DD-049-4 (Fisher's exact; one-sided
   criterion p; two-sided p published) or
   replace it openly.
4. **DD-049-2, DD-049-3** — the freeze
   confirms or openly overturns the
   contested-sign reading and the criteria
   precedence.
5. **The unicorn naming procedure.**
   Confirm that S-B's sign(s) are named at
   gate 0.5 from the frozen asset's verbatim
   labels alone (the draft's rule), and what
   happens if more than one sign carries a
   unicorn label (the draft removes all such
   signs in S-B and names each).
6. **Freeze sequencing and the digest pin.**
   This spec's freeze record must quote
   Asset A's SHA-256 verbatim, so this
   spec's freeze act is sequenced **after**
   Spec 045's Asset A freeze (campaign Wave 3
   group 1), even though this draft is
   written in Wave 1. The freeze confirms the
   sequencing and performs the verbatim
   quote; nothing about the pin is completable
   at draft.
7. **OSF registration (campaign E-1)** —
   under the approved campaign policy, this
   spec files its own OSF contract
   registration at its freeze. Nothing is
   filed at draft.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*

## 7. Freeze-stage adjudication — 2026-10-21: FREEZE FAILURE (OPEN-1 / gate 0.4 — POPULATION NOT REPRODUCED)

This section records a freeze attempt and its outcome. It is a
campaign bookkeeping act only: it is not a freeze, and it repairs
nothing.

- **Freeze attempt.** On 2026-10-21 the freeze for Spec 049
  (D-06, draft PR #250, branch
  `spec-049-hunt-opening-animal-signs-draft`, head `06fb4299`)
  attempted §6 item 1 (OPEN-1): fix, from records of record on
  `main`, the reproduction rule by which gate 0.4 re-derives the
  Phase-43 initial-strong set, and the keying rule by which
  enumerated signs resolve to Asset A rows — precisely enough
  that step 0 is a mechanical check.
- **Outcome: FREEZE FAILURE — POPULATION NOT REPRODUCED at the
  freeze stage.** No element of the reproduction rule is fixable
  from any record of record, and the keying rule fails
  independently. No threshold was invented, no list was
  borrowed, and no nearby set was substituted. Under this
  draft's own terms (§5 item 1; claim F049-C08), the spec
  therefore cannot freeze. **Phase-415 was NOT allocated.**
  No AEE hooks ran, no digest was computed, no OSF filing was
  made (E-1 files at a freeze; there is none).

### 7.1 The missing-rule findings (condensed)

1. **No member list exists.** The two pinned records state the
   count (40), the mean initial rate (0.757 against 0.251 by
   chance), and the profiled total (201) — and nothing else
   about membership. Across the full tree of `main` (5,908
   entries; exactly one `phase43` path) and every
   `INITIAL_STRONG` code-search path (21 unique files), exactly
   **5 of the 40 members are labelled anywhere**: 267 and 391
   (`outputs/phase43_all.json` §T2_1) and 201, 398, 6 (the
   Batch-5 / contact-zone records, as Harappa-exclusive signs
   with subset frequencies and no rates). The other 35 are
   named in no record. Only 30 distinct signs carry any
   per-sign data in the battery record, of 201 profiled.
2. **Position rules, count floor, and profiled-set rule — none
   stated.** No Phase-43 record states which occurrence is
   initial/medial/terminal, how length-1/2 sequences are
   classed, any count floor, or the rule selecting the 201
   profiled signs (the same absence Spec 052's freeze failure
   established for this battery's terminal side).
3. **The strength threshold cannot be located.** The only
   labelled signs with published initial rates bracket it
   without fixing it: labelled MODERATE signs carry 0.416 (87)
   and 0.445 (89); labelled STRONG signs carry 0.71 (391) and
   0.806 (267) (`phase43_all.json` §§T2_1+T2_3). Any threshold
   in (0.445, 0.71] fits; the four unlabelled candidate rates
   (0.44, 0.534, 0.797, 0.917) cannot narrow it, and the repo
   constants inside the interval (0.50, 0.55) belong to other
   batteries on other corpora. The recorded mean (0.757) is an
   aggregate over the unknown set, not a criterion.
4. **No loadable corpus.** The Phase-43 corpus is the
   Firestore V3 reconstruction; its data file is absent from
   `main` and the corpus-v3 loader returns an empty corpus
   without it. The pinned programme corpus layer is a
   different corpus whose text field is in Yajnadevam glyph
   numbers — not the Phase-43 corpus and not Mahadevan space.
5. **Keying fails independently.** Asset A is keyed by the
   pinned crosswalk's `registry_sign_id`, and frozen Spec 045
   §2.2 takes each row's numbers from that same crosswalk.
   The crosswalk carries 17 `mahadevan_1977` rows (5 exact,
   7 approximate, 4 uncertain, 1 marked incorrect M342→P122).
   **Neither certain member — M267, M391 — has a Mahadevan row
   at all**, so keying fails on the known members alone. The
   fuller Phase-122 v1 crosswalk (766 rows) is many-to-many
   with flagged conflicts (M001→P001 and M012→P001 both
   stand) and is not the pinned record; the Phase-71 map
   (115 entries) is partial and rests on a numeric-identity
   principle the pinned rows contradict (M059→P064).

### 7.2 Searches performed

- The full recursive tree of `main` at `e3399961…`: searched
  for any phase43 / phase_43 / phase-43 path (exactly one hit,
  the results file), for the loader's Firestore data file
  (absent), and for every `specs/` directory (no later spec
  deposits a member list).
- Full-structure parses of both pinned records and of the
  claim record for `…_manual_003` (its entire Phase-43
  evidence is the single count string; `signs_involved`
  names Hunt's animal kinds, not signs).
- GitHub code search for `INITIAL_STRONG` / `initial_strong`
  (21 unique paths each): every path inspected; the hits are
  the count string repeated, the fragments of §7.1 item 1,
  or neighbouring batteries.
- Spec 045's frozen text on `main` (population/crosswalk
  census; §2.2 keying contract; gate 0.2 noted at §7.4).
- The pinned crosswalk read in full (205 rows, 187 distinct
  registry identities, 17 Mahadevan rows as itemised in
  §7.1 item 5), plus every other crosswalk on `main`
  (Phase-122 v1, Phase-71, the 10-entry Mahadevan–Parpola
  file, the Fuls map, the canonical registry, the protocol
  profiles) — none supplies the frozen keying rule.
- Neighbouring batteries, each verified as a different
  definition on a different corpus: latent classes (45,
  start_rate ≥ 0.55, freq ≥ 4, Mohenjo-daro only), Phase-45
  (75, avg_position ≤ 0.25 on Holdat roles), Phase-33
  (INITIAL 7 of 61, no STRONG grade), the legacy positional
  analysis (i_rate ≥ 0.50, no STRONG grade).

### 7.3 The pin-timing ruling, and the other OPEN items

- **Asset A pin timing (coordinator's ruling, recorded).**
  Asset A is built at Spec 045's EXECUTION step 1 (Wave 3),
  so `asset-a-freeze.json` does not exist yet. Had this spec
  frozen, its freeze would have (a) quoted Spec 045's freeze
  digest `5d8254dd…` (verified in full at this pass:
  `5d8254ddc03045b68a0819f870fc9ccc1b9848a58fef3862dae3e4ca21b43f0a`)
  as the contract anchor, (b) fixed the pin SOURCE as Spec
  045's `asset-a-freeze.json` produced at its step 1, and
  (c) ruled gate 0.2 asserts that SHA-256 at EXECUTION
  step 0 — mismatch → ASSET PIN MISMATCH, exactly as
  drafted. The ruling is not the blocker; OPEN-1 is
  antecedent, and no digest quote was performed because
  there is no freeze to quote it in.
- OPEN-2 to OPEN-5 and OPEN-7 were **not decided**: they are
  freeze acts and there is no freeze. They remain as drafted.
  One fact is recorded under OPEN-2 without deciding it: the
  draft's proposed count corpus is in Yajnadevam glyph
  numbers, so the comparison inventory would face the same
  class of keying problem as the opening-strong set.

### 7.4 What would unblock it; a note for the coordinator

Unblocking records (any one of items 1–2, plus item 3, or
item 4), as records of record on `main`: (1) the enumerated
member list itself — the 40 Mahadevan numbers; (2) the
original Phase-43 battery script or methods record (position
rules, floor, threshold, profiled-set rule) together with
the V3 Firestore dump restored; (3) for keying,
`mahadevan_1977` mappings in the pinned crosswalk covering
the enumerated 40, or an owner amendment adopting a named
fuller crosswalk reconciled with Spec 045's frozen §2.2;
(4) an amendment re-scoping this spec to a new, explicitly
defined battery, honestly labelled as a new test.

Note, for wave planning only (no act taken here): frozen
Spec 045's step-0 gate 0.2 requires the same 40/61/20
classes to be reproduced at its execution. This pass took no
position on what framework that gate denotes; if it denotes
the Phase-43 battery, Spec 045's execution faces the same
absence, with INVALID as its designed closure.

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
