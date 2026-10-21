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
