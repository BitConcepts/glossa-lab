# Spec 058 — Adjudication Record

> ## ADJUDICATION INPUT — 2026-10-21
>
> This spec has three adjudication inputs,
> recorded here so the draft's basis is
> inspectable:
>
> 1. **The runnable-experiments campaign plan,
>    approved by the owner AS WRITTEN on
>    2026-10-21**
>    (`~/workspace/your_files/2026-10-21-runnable-experiments-campaign-plan.md`).
>    Design D-21 arm A is campaign member 15
>    (Part 2), drafted in Wave 1 (Part 4). The
>    plan's standing terms bind this draft:
>    arm B stays blocked and no AI substitution
>    is made for the coders (Part 1); any new
>    engagement of people remains the owner's
>    gate (Part 6 item 4); a draft that cannot
>    state its falsifier, step-0 gates, and
>    pre-written verdict wordings is a drafting
>    failure, reported rather than improvised
>    around (Parts 4 and 7).
> 2. **The portfolio triage of 2026-10-21**
>    (`~/workspace/research_notes/design-portfolio-triage-2026-10-21.md`):
>    design D-21 found **RIPE (arm A)** — arm A
>    "runs today on the recorded Phase-132
>    passes and produces the mechanism account
>    the claim's record asks for"; arm B "stays
>    blocked inside the design: it needs paid,
>    M77-native human coders, and the
>    engagement letters remain under the
>    owner's hold of 2026-10-12 (not prepared
>    to pay)". §2 below records the one point
>    on which this draft's first-hand
>    verification qualifies the triage's
>    wording — what "on record" means for the
>    per-pass codings — and how the draft
>    handles it without changing the design.
> 3. **Design D-21 itself** (PR #195 packet,
>    `04-study-headlines.md`, §D-21), which
>    governs the substance: the hypothesis,
>    the falsifier, the re-analysis method,
>    the fixed sign criteria, and the limits.
>
> These inputs commission this **draft**.
> They are not a freeze order and not an
> execution order for Spec 058: both remain
> separate owner decisions.

## 1. The adopted basis (operative substance)

- **The design.** D-21, arm A only: re-analyse
  the recorded Phase-132 pilot passes; for
  every mismatched object, localise the first
  position of divergence and the signs
  involved; tabulate mismatch share by sign,
  by object type, and by divergence type
  (substitution, insertion/deletion,
  segmentation cut). Criteria fixed by the
  design for signs: CONCENTRATED if the top
  10 signs by mismatch involvement account
  for at least 50% of all mismatches; UNIFORM
  if their share is within 10 points of their
  frequency share; BETWEEN otherwise.
- **The claim.** `STUDY-SPEC-023/PHASE-132+383`:
  CONTRADICTED — pilot exact-sequence
  agreement 0.20 against the frozen 0.80
  floor; Phase-383 interval [0.10, 0.32].
  Every coder was an AI agent of a single
  model family; that disclosure is part of
  the verdict. The pilot still failed, and
  stays failed, whatever arm A finds.
- **The open point.** The claim's adopted
  lane-2 record: why the passes disagreed is
  not understood at the level of mechanism —
  no account exists of which signs, objects,
  or segmentation choices drive the
  disagreement. (The same text's other open
  points — the 0.80 floor's correctness, a
  clarified codebook — are excluded from
  this spec by claim F058-C16.)
- **Arm B.** Blocked-out-of-scope (§3 of the
  spec, claim F058-C06). The draft records
  the block, the hold that causes it
  (2026-10-12), and the unblocking act. It
  designs no part of arm B and no AI
  substitution for its human coders; the
  substitution is forbidden by the campaign
  plan, and the Spec 023 record is the proof
  it answers a different question.

## 2. Verification record at draft

Verified first-hand at drafting, 2026-10-21,
from `main` @ `83b6a563`:

- **Design D-21** — read in full in the
  packet's `04-study-headlines.md` (§D-21)
  and in the packet README: the two open
  points (mechanism; the human question),
  arm A's hypothesis, falsifier, method, and
  fixed sign criteria, arm B's shape, bars,
  named block, and substitution bar, and the
  shared limit ("arm A cannot soften the
  contradicted verdict").
- **Spec 023** — read on `main`: the frozen
  protocol and the §5.6 freeze block
  (comparison space P primary / M secondary;
  primary-counterpart derivation; `UNK`
  compares as `UNK`; minimum-edit alignment,
  substitution preferred; gold estimator;
  stop-rule and release gates as adopted).
- **Phase-132 pilot report and metrics** —
  read on `main`: agreement 0.20 (10/50, P
  and M), per-token 0.4798 (95/198), gold
  estimator 0.05 (2/40), pass totals
  191 / 190 / 40 / 189, UNK shares
  (A 39.3%, B 38.9%), the adjudication
  taxonomy (162: identity 93, legibility 45,
  count 11, key 10, orientation 2, order 1),
  the frame as drawn (50 objects; sites
  25 / 15 / 6 / 4; types Seals 34, Tablets
  11, unrecorded 5; gold 10), and the §9
  artifact inventory.
- **Phase-383 report and results** — read on
  `main`: exact reproduction of the pilot's
  point values from the on-disk records,
  bootstrap interval [0.10, 0.32] (B = 9,999,
  seed 20261011), CONTRADICTED verdict, and
  the origin-group audit (one model family;
  effective independent coder origin
  groups = 1).
- **The lane-2 record** — the
  `STUDY-SPEC-023/PHASE-132+383` entry in
  Spec 029's adopted lane-2 drafts, read on
  `main`: the not-understood text quoted in
  spec §1, including its floor and codebook
  open points and its gated-reopening terms.
- **Input pins** — recomputed at this draft
  from `main` and stated in spec §2.1:
  Spec 023 spec `c2e5d166…`, pilot metrics
  `e864fca5…`, pilot report `e1df32da…`,
  frame `a967144b…`, dataset `adb596a1…`,
  dataset meta `b2c607fa…`, Phase-383 results
  `4e52942d…`, Phase-383 report `9f35f722…`,
  metrics module `238dfafa…`, rescoring
  module `b64b60de…`, crosswalk
  `4e7559df…` (identical to the value the
  pilot records themselves carry).
- **DEFECT FOUND — the design's premise
  about the record, qualified.** The design
  and the triage describe arm A as running
  "on the recorded Phase-132 pilot passes
  (both passes' codings are on record)".
  First-hand verification shows the record
  is split (spec §2.2): the committed
  repository holds the pilot's metrics
  (aggregates and per-object lengths / flags
  — no sequences), the frame, the
  adjudicated final dataset, and the
  reports; the per-pass codings, the gold
  pass, and the adjudication records exist
  only in the Phase-132 local store
  (gitignored), in the layout the frozen
  metrics module's `load_store` defines, as
  the module's own header and the pilot
  report's §§4(d), 9 state. Consequences
  the draft takes, none of them a design
  change:
  1. Sign-level, type-level (by events),
     and segmentation tabulations **cannot**
     be computed from committed files alone;
     the committed files support no arm A
     quantity beyond the already-published
     aggregates. Any draft pretending
     otherwise would be specifying an
     analysis of data it had not verified
     exists in hand.
  2. The draft therefore makes production
     of the store record set a fail-closed
     step-0 gate (spec §3 gate 0.2), proven
     by exact reproduction of the committed
     metrics (gate 0.4) and the adjudication
     taxonomy (gate 0.5), with the
     pre-written closure PILOT-PASS RECORDS
     NOT PRODUCIBLE naming the unblocking
     act (preserving the set as a committed,
     hashed record). This is the campaign
     plan's own step-0 pattern (plan Part 5,
     R-4: a step-0 failure is a result, not
     an interruption), applied to the one
     input whose posture the design's
     wording glosses.
  3. No substitute source is specified: the
     adjudicated dataset is not the passes,
     and the metrics flags are not sequences.
     Substituting either would silently
     change the design's data — forbidden by
     the campaign's discretion envelope
     (plan Part 9).
  The triage's RIPE finding stands under
  this handling: the passes are recorded,
  the machinery to load them is frozen and
  pinned, and the Phase-383 precedent shows
  the store route reproducing the pilot's
  numbers exactly. What the draft adds is
  the honest gate the record's split
  posture requires.
- **Anchors caution, recorded** — the
  anchors file recomputes at this draft to
  `df0cf620…`. The pilot report asserts
  `eccea6d5…` (the frozen value of
  2026-10-09) for the same file; that value
  no longer recomputes against the current
  file (the same stale-pin pattern Spec
  042's draft recorded for its own pin).
  This draft pins from a fresh recompute
  and says so (spec §2.1), rather than
  inheriting either earlier value.
- **Frame type values** — the frame records
  object type as `Seals` / `Tablets` / empty
  (5 objects). Spec §4.3 carries the empty
  value as the Unrecorded category, never
  back-filled (Spec 023 K3).
- **Not done at draft, by design** — no
  alignment, event, or share has been
  computed: the event total E is not stated
  anywhere in this draft (the committed
  metrics fix only the 95 matched pairs and
  the 198 denominator they sit in), the
  store has not been read under this draft,
  no code was written or run, the AEE hooks
  have not run, and nothing was filed with
  OSF. The per-object mismatch census (40
  keys) is likewise not enumerated here; it
  is gate 0.6's product at execution.

## 3. What the freeze decision is asked to decide

1. Freeze this contract as drafted (digest in
   `freeze.md` / `freeze.json`), with every
   §2 pin re-asserted against the merged
   record — or decline, leaving
   `STUDY-SPEC-023/PHASE-132+383` with its
   mechanism unaccounted, exactly as its
   record states today.
2. **DD-058-10 (proposal): whether the frozen
   spec files its own OSF registration** —
   proposal: yes, following the campaign
   plan's E-1 policy (every specification in
   the pass gets its own OSF contract
   registration at its freeze) and the
   Spec 027/028 study-design pattern, so the
   gates, criteria, and headline wordings are
   timestamped outside the repo before
   execution. Nothing is filed at draft.
3. **DD-058-11 (open): the execution venue
   for gate 0.2.** The store record set lives
   on the machine that holds the program's
   main checkout. The freeze/execution order
   names where production happens and how
   the produced set (or its manifest plus a
   preserved copy) reaches the execution —
   including whether preservation of the set
   as a committed, hashed record should be
   ordered as a separate act first, which
   would retire the NOT PRODUCIBLE outcome
   before execution rather than testing it.
   This draft takes no position; it records
   that the choice is the freeze's, and that
   silently assuming the store's survival is
   not one of the options.
4. **DD-058-12 (open): whether a separate
   margins/census audit is required** beyond
   gates 0.4–0.6. Proposal: the reproduction
   and census gates suffice — they are
   exact, not sampled. The freeze confirms
   or requires more.

## 4. Draft-fixed readings (stand unless the freeze overturns them openly)

Each is labelled **DECIDED-BY-DRAFT**:

- **DD-058-1 — The variant appends; the
  frozen verdict is untouched.** The claim
  under test is
  `STUDY-SPEC-023/PHASE-132+383`; this spec's
  outcome appends to its record as a dated
  mechanism account. Spec 023's files, the
  Phase-132 report, and the Phase-383
  verdict are never edited (claim F058-C05).
- **DD-058-2 — The gold pass and the
  adjudicated sequences are not primary
  inputs.** Design D-21 arm A's data is "the
  recorded Phase-132 pilot passes" — Pass A
  and Pass B. The gold pass is a third
  coding of 10 objects and the adjudicated
  sequences are the passes' adjudicated
  product; either would change the question
  from "why did the two passes disagree" to
  a three-way or post-adjudication question
  the design does not ask. The adjudication
  records serve one registered purpose:
  gate 0.5's identity cross-check.
- **DD-058-3 — Segmentation is typed from
  the pass alignment, not from the
  adjudication taxonomy.** The design lists
  divergence types "(substitution,
  insertion/deletion, segmentation cut)".
  The draft reads insertion/deletion events
  in the frozen A-vs-B alignment as the
  segmentation axis's mechanical form
  (§4.2/§4.3), because the adjudication
  taxonomy's `count` category (11 of 162)
  classifies adjudication-stage
  disagreements over all 50 objects — a
  different population and a different act
  from the pass-pair events over the
  mismatched 40. The taxonomy is used only
  as gate 0.5's cross-check. The proxy's
  limit is stated in spec §8(4).
- **DD-058-4 — P space is primary; M space
  is a descriptive sensitivity.** Per Spec
  023's §5.6 freeze block (P primary, M
  secondary). The pilot's two spaces agreed
  on every published aggregate (0.20 in
  both), but agreement on aggregates does
  not make M co-primary for a tabulation
  the freeze block never contemplated.
- **DD-058-5 — No execution phase number at
  draft.** Allocated at the freeze act, from
  the merged record as it then stands.
- **DD-058-6 — Sign involvement counts a
  substitution for both of its values.** The
  design's criterion is stated over "signs
  by mismatch involvement" and "the signs
  involved"; a substitution involves two
  signs. Shares are therefore taken over
  summed involvement (spec §4.3), and the
  design's "50% of all mismatches" is read
  on that basis. Recorded as a reading, not
  a quotation: the freeze may direct the
  per-event basis instead, openly.
- **DD-058-7 — UNK counts in the primary;
  the UNK-excluded tables are descriptive
  only.** Reasoned in claim F058-C15 and
  §5 of this record (dual derivation D-5).
- **DD-058-8 — The object-type locus rule
  (50% of events + 10-point enrichment;
  Unrecorded cannot fire).** The design
  fixes the tabulation but no numeric locus
  rule for types. The draft mirrors the
  design's own two numbers (50%, 10 points)
  rather than importing new ones, and bars
  the Unrecorded category from firing
  because it records an absence, not a type.
- **DD-058-9 — MULTIPLE LOCI is a headline
  class.** The campaign's outcome set names
  four wordings (signs / object types /
  segmentation / not localised); the three
  locus rules are not mutually exclusive,
  so a forced single name on a multi-locus
  result would misstate the tables. The
  draft adds the combination wording; the
  four named outcomes are its single-locus
  and empty-set members, unchanged.
- **DD-058-13 — Evidence carries
  `observed_at` from the draft.** The cited
  facts were verified first-hand today; the
  Spec 038/042 precedent carries the field
  from the act that actually observed the
  records.

## 5. Acceptance tests derived twice (doctrine record)

Per the autonomous-execution doctrine, the
acceptance test behind each claim's
`falsification_tests` was derived twice,
independently, from the claim's requirement
alone: derivation A working from the
operational side (what a run must show), and
derivation B working from the reader's side
(what a checker with only the published
products must be able to recompute or
inspect). Agreements were adopted silently;
every disagreement, and its resolution, is
recorded here.

| Claim | Derivation A (operational) | Derivation B (reader-side) | Outcome |
|---|---|---|---|
| F058-C01 | Reject any output whose conclusions exceed the pilot-pass locus statement | Inspect every output against the claim boundary | Agree — inspection test adopted |
| F058-C02 | Hash the two results files and read the quantities | Hash all §2.1 pilot records | Agree in substance — A adopted (the claim names two files); full pin set is C09's test |
| F058-C03 | Supported iff the tabulations concentrate | Supported iff the headline is a localisation | **Disagreed** — B would count a SEGMENTATION-only headline as support; the design's hypothesis names signs or object types. Resolution: A's locus terms govern; C03's verdict_rule names SIGNS or OBJECT TYPES firing, and a segmentation-only result is recorded under C13/C14, not as support |
| F058-C04 | Headline NOT LOCALISED iff no locus fires | Headline NOT LOCALISED iff sign state is UNIFORM | **Disagreed** — B read the design's UNIFORM as the falsifier's only form; the design also admits BETWEEN (neither uniform nor concentrated). Resolution: the falsifier fires on the empty locus set; UNIFORM and BETWEEN are both reported as the sign sub-state inside the NOT LOCALISED wording (spec §5.2) |
| F058-C05 | Compare Spec 023 tree hashes before/after execution | Inspect products for any restated verdict | Agree — both required; A's hash check rides on C09's gate record, B is the stated test |
| F058-C06 | Fail if any arm-B artefact exists in the spec's products | Fail if any output reads as a calibration or human-performance claim | Agree — inspection test adopted, covering both |
| F058-C07 | Hash the store files at draft and pin them like §2.1 | Require production + manifest + exact reproduction at execution | **Disagreed** — A is impossible at draft (the set is uncommitted local-store material; pinning it would assert values this drafting act has not verified and cannot re-assert from the repository) and insufficient at execution (hashes alone do not prove the set is the pilot's). Resolution: B adopted (gates 0.2/0.4/0.5); A survives only as DD-058-11's option, if the owner orders preservation first |
| F058-C08 | Diff the analysis code's derivation/alignment against the pinned module | Require gate 0.4 exact reproduction | Agree in substance — B adopted as the operative test (identity proven by reproduction, per the Phase-383 precedent); import provenance is also recorded |
| F058-C09 | Each gate self-tests; stop on first failure | The execution record must show gate verdicts before any quantity | Agree — both stated; B is the falsification test, A is its mechanism |
| F058-C10 | Assert event typing in code against hand-checked objects | Recompute the event table from published per-object alignments | Agree — B adopted; it requires §6 to publish the alignments' event table, which the spec obliges |
| F058-C11 | Assert the top-10 share in code | Recompute from the full published T1 table | Agree — B adopted; A is subsumed |
| F058-C12 | Fire on event share ≥ 50% alone (mirroring the sign rule) | Fire only with enrichment over the type's object share | **Disagreed** — A imports a composition artefact: Seals hold 68% of the frame, so a bare share rule localises to Seals even if mismatches are exactly proportional. Resolution: B adopted (both conditions, §5.1); A is recorded as the rejected simpler rule in claim F058-C12's alternatives |
| F058-C13 | Type segmentation from the adjudication taxonomy's `count` category | Type segmentation as the indel share of alignment events | **Disagreed** — A's source classifies a different population (adjudication disagreements, all 50 objects) than the design's data (pass pairs, mismatched objects). Resolution: B adopted as the primary; A demoted to gate 0.5's identity cross-check (DD-058-3) |
| F058-C14 | Headline = the firing locus with the largest share | Headline = a mechanical function of the firing set, incl. a combination class | **Disagreed** — A needs a tie/priority rule the design never states and would drop firing loci from the headline. Resolution: B adopted (DD-058-9); the four campaign-named wordings are preserved as the single-locus and empty-set cases |
| F058-C15 | Exclude UNK-involved events from the primary (UNK ≈ 39% of tokens would swamp named signs) | Count the recorded values as recorded in the primary; UNK-excluded tables descriptive only | **Disagreed** — A redefines the pilot after the fact and contradicts the design's instruction to tabulate the mismatches produced; B risks an UNK-driven headline. Resolution: B adopted for the primary, A preserved entire as the pre-registered descriptive secondary, and the residual risk closed by wording — the mandatory UNK sentence in spec §5.2 (DD-058-7) |
| F058-C16 | Reject outputs containing movement/meaning claims (house fences) | Reject outputs containing human-performance, floor, or codebook claims (this claim's actual boundary) | Agree in substance — B adopted (it is the claim's boundary); A's fences bind via C01/C05 independently |

No other disagreements arose. Where the two
derivations agreed, the register carries the
reader-side form, because a test a reader
cannot re-run from the published products is
not an acceptance test in this program.

## 6. OPEN for the freeze (consolidated)

1. DD-058-10 — OSF registration (proposal:
   yes, per campaign E-1). Not filed at
   draft.
2. DD-058-11 — Execution venue and the
   store-preservation question for gate 0.2.
3. DD-058-12 — Whether gates 0.4–0.6 suffice
   without a separate margins/census audit
   (proposal: they suffice).
4. Confirmatory — DD-058-8 (object-type
   rule), DD-058-3 (segmentation proxy),
   DD-058-6 (involvement basis), DD-058-9
   (MULTIPLE LOCI class): each is a
   DECIDED-BY-DRAFT reading on a point the
   design leaves open; the freeze confirms
   or overturns each openly, and any
   overturn is recorded before the freeze
   digest is computed.
5. The execution phase number (DD-058-5),
   allocated at freeze.
6. The AEE lifecycle hooks themselves
   (tasks L4) — not run on this draft; any
   recovery round they force changes claim
   text before the freeze digest exists.

## 7. Freeze decisions (2026-10-21)

> ## FREEZE ACT — DECIDED — 2026-10-21
>
> The freeze act of 2026-10-21, under the
> campaign plan approved AS WRITTEN the same
> date (Wave 2 freeze wave), decided the
> items §3 and §6 left open. Each resolution
> is recorded here on the record; the register
> rulings were carried into `claims.json`
> before the AEE hooks ran, and the hooks
> passed over the recovered register
> (0.8-draft; `aee/freeze-aee-note.md`).

- **DD-058-14 — OSF registration at the
  freeze (E-1).** This spec files its own
  OSF contract registration at the freeze,
  under campaign decision E-1, following
  the Specs 036–039 pattern. This resolves
  DD-058-10 as proposed (yes). The filing
  record is `osf-spec-registration.md`.
  Execution awaits the registration's
  approval act and a separate execution
  order; no mail is handled by the freeze.
- **DD-058-15 — DD-058-11 resolved: the
  store survives; production stays at
  execution gate 0.2.** The freeze act
  inspected the record first-hand. The
  Phase-132 local store survives complete
  on the machine holding the program's main
  checkout, at
  `corpora/downloads/cisi_image_layer/phase132_pilot/`
  (gitignored, exactly as §2 of this record
  describes): `frame.json`; 50 Pass A
  records; 50 Pass B records; 10 gold-pass
  records; 50 adjudication records; and
  `effort_log.csv` with 320 data events —
  the pilot report's §9 inventory, complete,
  counted read-only at the freeze. Three
  proofs that the surviving set is the
  pilot's record set were run read-only at
  the freeze with the pinned machinery (the
  stale checkout's copies of the pinned
  files hash to their §2.1 freeze values, so
  the run used the record of record, not a
  copy of convenience): (1) the pinned
  metrics module's `compute_metrics` over
  the surviving store reproduces the
  committed metrics file **exactly** — the
  computed record equals the committed
  record in full, not only on the headline
  values gate 0.4 names; (2) the
  disagreement taxonomy recomputed from the
  surviving adjudication records equals the
  pilot report's §4(c) counts exactly
  (identity 93, legibility 45, count 11,
  key 10, orientation 2, order 1; total
  162 — gate 0.5's values); (3) the store's
  `frame.json` frame list equals the
  committed pilot frame's frame list in
  full (gate 0.3's identity). A per-file
  SHA-256 manifest of the 162-file set was
  computed at the freeze as inspection
  evidence; it is **not** a freeze pin and
  asserts nothing at execution. On that
  evidence the freeze **proceeds**, and the
  production question is answered under the
  draft's own design: production is
  **deferred to execution gate 0.2**,
  fail-closed exactly as drafted, with its
  pre-written PILOT-PASS RECORDS NOT
  PRODUCIBLE closure standing. The freeze
  produces, preserves, copies, and pins **no**
  store bytes; preserving the set as a
  committed, hashed record is **not** ordered
  as a separate act first, because the
  design's gate is the honest test of the
  record at execution, the store's survival
  is now a freeze-verified fact rather than
  an assumption, and a preservation act
  remains available as the named unblocking
  act if gate 0.2 ever fires. The execution
  venue for gate 0.2 is the machine holding
  the program's main checkout — the machine
  whose store this section verifies — or
  whatever venue the execution order names
  with the store produced there; silently
  assuming survival was never an option, and
  after this section it is not an assumption
  at all for the venue named. The freeze's
  reproduction check is freeze evidence for
  this adjudication only: it computed no
  localisation quantity (no alignment, event,
  or share of §4), and execution still runs
  every step-0 gate in order on the produced
  set.
- **DD-058-16 — DD-058-12 resolved: gates
  0.4–0.6 suffice.** No separate margins or
  census audit is required beyond gates
  0.4–0.6, as proposed: the reproduction,
  taxonomy cross-check, and census gates are
  exact, not sampled, and gate 0.6 publishes
  the census every share is taken over.
- **DD-058-17 — Phase-420 allocated.** The
  execution phase number (DD-058-5) is
  allocated at this freeze as **Phase-420**,
  from the merged record as it stands: the
  campaign's freeze order allocated
  Phase-404 to Phase-418 to the members
  frozen before this one (Phase-412,
  Phase-415, and Phase-417 stand as
  unallocated tombstones of the three freeze
  failures), Phase-419 stands allocated to
  Spec 057 in the campaign record, and no
  repository record allocates Phase-420 —
  verified at the freeze by search of the
  merged record.
- **DD-058-18 — The DD-038-10 AEE gate
  reading adopted.** The gate is: at every
  lifecycle hook, zero correctness failure
  modes and no claim below the 0.70
  threshold; FR-2.3 draft-cap records alone
  do not block a freeze, because they are
  lifted only by human ratification (a
  status change), not by any recovery
  available at a freeze. The hooks passed
  on that reading (`aee/freeze-aee-note.md`).
- **DD-058-19 — Draft readings confirmed.**
  DD-058-1 to DD-058-9 and DD-058-13 are
  **confirmed** as drafted, including the
  four confirmatory items of §6: DD-058-3
  (segmentation typed from the pass
  alignment, the indel-share proxy),
  DD-058-6 (sign involvement counts a
  substitution for both of its values;
  shares over summed involvement), DD-058-8
  (the object-type locus rule: at least 50%
  of events plus a 10-point enrichment
  margin; Unrecorded cannot fire), and
  DD-058-9 (LOCALISED TO MULTIPLE LOCI as
  the combination headline class). No draft
  reading is overturned.

Every §2.1 pin was re-asserted at this freeze
against the merged record (`main` at
`770155dea66c5d5dde194728560aacf83c7514d0`,
after Spec 050's freeze merge) by two
independent routes — the contents-API route
and the git-blob route — both recomputed in
the foreground, agreeing byte-for-byte on
every file, and every recomputed hash equal
to its draft pin (`freeze.md` §2). No pin
moved between the draft's base and the freeze.


---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
