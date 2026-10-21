# Spec 050 — Adjudication Record

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
>    Under the plan, D-13 is member 10, a
>    dependent drafted in Wave 1 after its
>    asset builder (D-05, Spec 045), consuming
>    Asset A by digest pin (Part 3, E-6,
>    requirement R-2).
> 2. **The portfolio triage of 2026-10-21**
>    (`~/workspace/research_notes/design-portfolio-triage-2026-10-21.md`):
>    design D-13 found **RIPE** — the celestial
>    class comes from the same shared
>    published-identification classification
>    as D-05/D-06, frozen before counting; the
>    corpus and positional framework are in
>    hand; it completes the positional
>    measurement of Hunt's scheme (openings
>    D-06, pattern D-05, endings here).
>
> These inputs commission this **draft**.
> They are not a freeze order and not an
> execution order for Spec 050: both remain
> separate later acts under the campaign's
> Waves 2 and 3.

## 1. The adopted basis (operative substance)

- **The design.** D-13 in the PR #195
  experiment-design packet
  (`docs/research/experiment-designs-2026-10-13/02-roif-and-hunt.md`,
  §D-13): a class-level test — pooled
  final-position rate of the celestial class
  against a frequency-matched comparison
  class, per-sign results reported alongside —
  with its criteria fixed in advance
  (SUPPORTED at ratio ≥ 1.5 at the 5% level
  with at least half the class's occurrences
  from signs individually above the corpus
  rate; NOT SUPPORTED at ratio ≤ 1.0;
  INCONCLUSIVE between, or below 30 class
  occurrences).
- **The claim.**
  `without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_004`:
  UNTESTED (Phase-104, RULE-CLASS: its
  falsifier requires a defined celestial
  class, and none existed).
- **The asset.** Asset A, per campaign Part 3
  and decision E-6 and Spec 045 §2: built and
  frozen inside Spec 045, from held published
  sources only, entered blind, frozen before
  any join; consumed here as exactly its
  `sky_cycle` depicted kind, digest-pinned
  (spec §2). This spec builds nothing.
- **The caution.** Spec 037's census:
  object-type labels diverging between
  compilations in 49% of matched cases —
  carried in spec §7 limit 4 and claim
  F050-C15, on the same terms as Spec 045
  carries it.

## 2. Verification record at draft

Verified first-hand at drafting, 2026-10-21,
via the GitHub API against `main` at
`83b6a563…` (the local checkout was not
touched, per the drafting order):

- **Design D-13** — read in full: the
  question, hypothesis, falsifier (celestial
  class's final rate at or below the
  corpus-wide rate for signs of comparable
  frequency), data (celestial class from the
  shared classification — signs the published
  identifications describe as sun, star, moon,
  or celestial bodies, the list frozen before
  counting, each entry cited; corpus and
  positional framework as in D-06/D-08),
  method (pooled class test against a
  frequency-matched comparison; per-sign
  results alongside), criteria (the three
  words above plus the 30-occurrence floor),
  controls (published-source citation per
  sign; a named sensitivity with borderline
  signs removed; the list frozen before any
  positional number is computed), and the
  not-established line (no scheduling, ritual
  calendars, or cycle content).
- **Spec 045's draft** — read in full on its
  branch `spec-045-hunt-depicted-kinds-draft`
  (PR #244): `spec.md` §2 (the Asset A
  contract: fields, the seven `depicted_kind`
  values including `sky_cycle`, the §2.3
  source hierarchy — CISI Vols 1–2 govern,
  Parpola where silent — blind entry, the
  §2.5 dispute rule with contested excluded
  from the primary and included in a
  sensitivity under the CISI-governed label,
  the §2.7 freeze point with SHA-256 recorded
  in `asset-a-freeze.json`), its §3 build
  gates and §4 input pins, and its
  `adjudication.md` — including the two items
  it leaves OPEN-for-freeze that touch this
  spec: the **jurisdiction coding question**
  (its §5, item 2 / §6, item 4) and the
  **narrower `sky_cycle`-only alternative**.
  Spec 050 §2.2 and claim F050-C07 are written
  directly from those passages.
- **Input pins** — recomputed first-hand at
  this draft from `main` at `83b6a563…` and
  stated in spec §6: corpus layer
  `c02e3d7b…`, crosswalk master `4ace1a61…`,
  positional record `0e546962…` (805 / 2,267;
  40 / 61 / 20 strong-sign classes), Phase-43
  record `78a6c219…`, anchors `df0cf620…`.
  All five recompute equal to the values
  Specs 042 and 045 pin.
- **Numbering state** — Specs 044 (D-02),
  045 (D-05), 046 (D-18), and 047 (D-09) exist
  as draft PRs #243–#246; no Spec 050 branch
  or directory exists on `main` or in the
  open PRs at this draft. This draft takes
  050 as assigned by the campaign drafting
  order.
- **Phase-number state** — Phase-400…403 are
  allocated (Specs 036/038/037/039); Spec 040
  allocated none, and neither do the campaign
  drafts 042–047 at draft. Spec 050 allocates
  none at draft (DD-050-7).
- **Not done at draft, by design** — Asset A
  has **not** been built: no digest exists to
  quote, no sign's membership is asserted
  anywhere in this draft, no class census has
  been taken, no final-position quantity was
  calculated, no code was written or run, the
  AEE hooks have not run, and nothing was
  filed with OSF.

## 3. Doubly derived acceptance tests (doctrine record)

Per the autonomous-execution doctrine, each
claim's acceptance test was derived twice,
independently: **Derivation A** from the
requirement text of the claim alone, and
**Derivation B** from the design's falsifier,
gates, criteria, the Asset A contract, and
campaign requirements R-2/R-3, without
reference to A. Where A and B agreed, the
register carries the agreed test. Six
disagreements arose; each is recorded here
with its resolution, and the register and
spec follow the resolution:

1. **F050-C03/C10 (the denominator).** A,
   from the falsifier's first phrasing,
   derived the corpus-wide final-position
   rate as the primary denominator ("at or
   below the corpus-wide final-position rate
   for signs of comparable frequency"); B,
   from the design's method paragraph,
   derived the frequency-matched comparison
   class ("all non-celestial signs in the
   same frequency band"), noting the falsifier
   phrase itself qualifies its rate with
   "for signs of comparable frequency".
   **Resolution: B as primary.** The matched
   class is the denominator (§4.2–4.3); the
   corpus-wide rate is published beside it
   and is the rate for the per-sign
   half-of-occurrences condition, which is
   exactly where the design's criteria use a
   corpus rate. Interchanging them would
   re-admit the frequency confounder the
   design names.
2. **F050-C07 (the breadth of "celestial").**
   A, from Hunt's closing part as D-05 states
   it ("cycles/jurisdiction last"), derived a
   class of cycle/sky **and jurisdiction**
   signs; B, from D-13's own data paragraph
   (sun, star, moon, celestial bodies) and
   the Asset A contract it consumes, derived
   `sky_cycle` only — jurisdiction has no
   Asset A kind, and coding it inside this
   spec would re-derive a classification.
   **Resolution: B.** Spec §2.2 states the
   difference as an explicit boundary: the
   broader closing form is not tested here,
   in either direction. This also answers, for
   this consumer, the question Spec 045 left
   OPEN-for-freeze — without purporting to
   settle it for Spec 045's own closing test.
3. **F050-C08 (the sensitivity's shape).** A,
   from D-13 alone, derived one sensitivity
   (borderline signs removed — the design's
   named arm); B, from Asset A's dispute rule
   (Spec 045 §2.5), derived one sensitivity
   of the opposite motion (contested signs
   included under CISI-governed labels).
   **Resolution: both, as separate arms**
   (S1, S2, §4.5). Each answers a different
   question — whether the result depends on
   hedged identifications, and whether it
   depends on excluding disputed ones — and
   collapsing them into one rerun would make
   either dependence unattributable.
4. **F050-C11 (the thin class).** A derived
   TOO THIN as a step-0 closure class of the
   same kind as INVALID, by analogy to Spec
   042's THIN headline; B derived it from
   D-13's criteria text, which places the
   below-30 case **inside INCONCLUSIVE**
   ("INCONCLUSIVE: between, or the class
   totals fewer than 30 occurrences").
   **Resolution: B, with A's recording
   discipline.** TOO THIN is the recorded
   form of INCONCLUSIVE for this case (§4.3),
   stated with its census and with no rate
   computed — the gate-0.4 census is
   totals-only, so the closure needs no
   positional quantity, exactly as a step-0
   closure should not.
5. **F050-C03/C11 (the exact test's
   sidedness).** A derived a one-sided
   enrichment test from the hypothesis's
   direction; B derived a two-sided Fisher
   exact test from the criteria's symmetric
   form (a ratio at or below 1.0 falsifies,
   so both tails carry verdicts) and from the
   family practice of stating tests
   conservatively at draft. **Resolution: B**
   (DD-050-4) — two-sided, at the 5% level,
   on the pooled 2×2 table; the freeze may
   overturn it only openly.
6. **F050-C09 (a length floor for endings).**
   A imported the tripartite record's
   length-≥3 population (the 2,267
   inscriptions of the formula test) as the
   population for final position; B objected
   that D-13 registers no length floor — its
   counts are class occurrences in the corpus
   under the positional framework of D-06 /
   D-08 — and importing the formula test's
   population would silently change the
   estimand from "ends of texts" to "ends of
   formula-eligible texts". **Resolution:
   B.** This spec introduces no floor of its
   own (§4.1); whatever convention the pinned
   framework itself applies is part of that
   framework, restated in the gate-0.5
   reproduction record and applied identically
   to both classes.

## 4. Draft-fixed readings — DECIDED-BY-DRAFT

Each stands unless the freeze overturns it
openly:

- **DD-050-1 — The celestial class is
  `sky_cycle`, exactly.** See §3,
  disagreement 2. The draft takes the
  narrower reading Spec 045's adjudication
  names, states the untested remainder as a
  boundary (spec §2.2, claim F050-C07), and
  widens nothing.
- **DD-050-2 — The frequency band is the
  class's own count range.** The design says
  "the same frequency band" and fixes no
  numeric band. The draft operationalises it
  as: comparison signs whose total counts lie
  between the primary celestial members'
  smallest and largest total counts,
  inclusive — derived from the census at
  gate 0.4, before any positional quantity,
  so the band can never be tuned to a result
  (spec §4.2, claim F050-C10).
- **DD-050-3 — TOO THIN covers the comparison
  class too, and is INCONCLUSIVE's form.**
  The design fixes the 30-occurrence floor
  for the celestial class only. A matched
  denominator below the same floor cannot
  carry a 5%-level comparison either, so
  gate 0.4 applies the floor symmetrically;
  and per §3, disagreement 4, TOO THIN is
  recorded as the INCONCLUSIVE form the
  design's criteria name, not as a separate
  verdict.
- **DD-050-4 — Fisher's exact test,
  two-sided.** See §3, disagreement 5. The
  design says "at the 5% level" and names no
  test for this pooled 2×2 comparison; the
  sibling designs' "exact test" practice
  (D-06) fixes the family, and this draft
  fixes the member and its sidedness so the
  freeze inherits a decision, not a gap.
- **DD-050-5 — NOT ADJUDICATED is the
  reconciliation-failure class.** The
  design's three criteria words assume the
  pooled and per-sign counts agree and name
  no word for the contrary case. The draft
  adds NOT ADJUDICATED as a stop class
  (never folded into INCONCLUSIVE, which is
  a verdict about the claim) — claim
  F050-C13, spec §5.1. (The same addition
  Specs 042's and 045's drafts made, for the
  same reason.)
- **DD-050-6 — Coverage is asserted at the
  resolution this test consumes.** Gate 0.3
  requires an Asset A row for **every sign
  occurring in the pinned corpus**, because
  the comparison class is defined over all
  non-celestial signs; an absent row may not
  default to non-celestial. See §5, item 2,
  for the tension this creates with Spec
  045's gate A3 and how it is handled.
- **DD-050-7 — No execution phase number at
  draft.** Allocated at the freeze act, from
  the merged record as it then stands.
- **DD-050-8 — Evidence carries
  `observed_at` from the draft.** As in Spec
  042's DD-042-4 and Spec 045's DD-045-7:
  the cited facts were verified first-hand
  today; including the field now is the
  completion Spec 038's freeze otherwise had
  to retrofit.

## 5. Defects and ambiguities found in the sources, and their handling

1. **The design states its denominator two
   ways.** D-13's falsifier says "the
   corpus-wide final-position rate for signs
   of comparable frequency"; its method says
   the comparison is a frequency-matched
   class. Handled by §3, disagreement 1:
   matched class primary, corpus-wide rate
   published and used where the criteria use
   it. Recorded here so the reading is
   freeze-visible, not silent.
2. **Asset A's coverage gate is scoped to
   Spec 045's population; this test consumes
   corpus-wide coverage.** Spec 045's gate A3
   asserts a row for every sign in **its**
   test population (the strong-sign classes
   and the signs its models score). D-13's
   comparison class is defined over every
   non-celestial sign in the corpus, which
   may reach signs outside that population.
   This is a genuine contract gap between the
   builder's draft and this dependent's
   design — **not** papered over: gate 0.3
   asserts the coverage this spec consumes
   and closes INVALID without it, and the
   freeze of either spec may resolve the gap
   openly (for example by Spec 045's build
   covering the full crosswalk inventory, as
   its §2.1 "one row per sign" form suggests).
   If neither freeze resolves it, this spec
   closes honestly at its own gate rather
   than testing on a silently narrowed
   comparison class.
3. **Spec 045's jurisdiction question is
   open, and D-13 does not need it answered.**
   Handled by DD-050-1 / §3, disagreement 2:
   this consumer takes `sky_cycle` only and
   states the boundary. No defect in D-13;
   the ambiguity lives in the builder's
   closing test, and this draft does not let
   it leak into the endings test.
4. **"Borderline" in D-13 vs Asset A's
   `dispute_status`.** D-13's sensitivity
   removes "borderline signs" without naming
   a field; Asset A records exactly that
   notion as `dispute_status = borderline`
   (the published identification hedged in
   its own source). Mapped one-to-one in
   spec §4.5 (S1) and claim F050-C08; no
   substance changed.
5. **No defect in the falsifier or the
   criteria values.** The falsifier, the
   1.5 / 1.0 ratio lines, the 5% level, the
   half-of-occurrences condition, and the
   30-occurrence floor are all stated in the
   design; this draft invented none of them.
   The values it did have to fix — the band
   rule and the exact test's identity — are
   recorded as DD-050-2 and DD-050-4.

## 6. OPEN-for-freeze items

The freeze decision is asked to decide:

1. **The Asset A digest itself.** Asset A
   does not exist at this draft. This spec's
   freeze quotes its SHA-256 verbatim from
   Spec 045's `asset-a-freeze.json` (§2.3),
   after Spec 045 has executed its asset
   build and frozen — campaign freeze order:
   builders before dependents. Nothing can
   substitute for that record.
2. **The coverage question (§5, item 2).**
   Whether Asset A as built covers every
   corpus sign (gate 0.3 passes as built), or
   the freeze narrows this spec's comparison
   population openly with the narrowing
   recorded as a design change — never as a
   run-time default.
3. **DD-050-1…DD-050-6** — the freeze
   confirms or openly overturns the
   `sky_cycle`-only boundary, the band rule,
   the symmetric TOO THIN floor, the
   two-sided Fisher test, the NOT
   ADJUDICATED class, and the coverage
   resolution. In particular DD-050-1: if the
   freeze judges D-13's celestial notion
   broader than `sky_cycle`, the widening is
   a recorded design amendment with its own
   classification source named — it does not
   enter by re-reading §2.2.
4. **OSF registration (campaign E-1)** —
   under the approved campaign policy, this
   spec files its own OSF contract
   registration at its freeze. Nothing is
   filed at draft.
5. **Whether execution requires any
   calibration beyond gate 0.5's
   reproduction.** The draft takes no
   position; the positional machinery here is
   counting and an exact test, and gate 0.5
   plus the §4.4 reconciliation may suffice.
   The freeze decides and records the
   decision either way.

## 7. What the freeze is asked to decide, in one paragraph

Freeze this contract as drafted — with the
Asset A digest quoted verbatim from Spec
045's freeze record, every §6 pin
re-asserted against the merged record, and
§6's items decided — or decline, leaving
`without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_004`
UNTESTED as recorded, its endings unmeasured,
exactly as they have stood since Phase-104.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
