# Spec 042 — Adjudication Record

> ## ADJUDICATION INPUT — 2026-10-21
>
> This spec has two adjudication inputs,
> recorded here so the draft's basis is
> inspectable:
>
> 1. **The owner's order of 2026-10-21**:
>    "address all these remaining items now" —
>    the order under which the PR #195
>    experiment-design portfolio was triaged
>    in full and its top-ranked untaken ripe
>    design drafted.
> 2. **The portfolio triage of 2026-10-21**
>    (`~/workspace/research_notes/design-portfolio-triage-2026-10-21.md`):
>    design D-28 found **RIPE** — its inputs
>    (Phase-393's Arm B machinery, population,
>    and frozen family rules) are all on
>    record, it depends on no blocked asset,
>    and it is the highest-ranked packet
>    design never yet taken up (the packet's
>    top five — D-30, D-03, D-20, D-31, D-25 —
>    were all resolved by Specs 032/033/034/
>    038/040).
>
> These inputs commission this **draft**.
> They are not a freeze order and not an
> execution order for Spec 042: both remain
> separate owner decisions.

## 1. The adopted basis (operative substance)

- **The design.** D-28 in the PR #195
  experiment-design packet
  (`docs/research/experiment-designs-2026-10-13/04-study-headlines.md`,
  §D-28): Spec 028's Arm B test, machinery
  unchanged, run separately on the seal-only
  and tablet-only repertoire sets, with the
  full site jackknife per stratum, judged
  under the family's frozen verdict rules, and
  the headline pre-registered as a pattern
  (SPLIT / UNIFORM-PASS / UNIFORM-FAIL /
  THIN).
- **The claim.** `STUDY-SPEC-028/ARM-B`:
  INCONCLUSIVE — primary median adjusted R²
  0.0223721, interval [0.0122174, 0.0333271],
  rejection share 0.9548, with the frozen
  SUPPORTED rule's jackknife clause failed on
  the drop-Harappa cell (LOSO median
  0.0066068 against the 0.01 margin).
- **The hypothesis source.** Spec 028's
  exploratory Arm C: Harappa-vs-pooled
  dissimilarity 0.4952733 among tablets vs
  0.1113521 among seals. Exploratory then,
  exploratory now (ASM-ARMC-EXPLORATORY): it
  motivates the directional hypothesis and is
  cited as evidence for nothing.
- **The population.** The Phase-393 Arm B
  analysis population: 3,030 records at 6
  sites, produced by the frozen flow from the
  pinned corpus layer (spec §2). The strata
  partition it by recorded object type.

## 2. Verification record at draft

Verified first-hand at drafting, 2026-10-21:

- **Design D-28** — read in full on the PR #195
  branch: the question, hypothesis, falsifier
  (strata behave alike), method (machinery
  unchanged; exclusion by rule, counted),
  per-stratum rules carried from the frozen
  family, stratum floors (≥6 sites carrying
  ≥20 inscriptions of the type, else TOO THIN
  with counts), the four-word headline set,
  the named confounders, and the limits
  (Spec 027's fence; no mechanism).
- **Phase-393 results** — read on `main`:
  the population flow (5,679 / 4,531 / 4,505 /
  3,605 / 3,144 / 3,030), Arm B's primary
  quantities, and Arm C's per-type
  dissimilarities, all as stated in spec §1.
  Of the six Arm B LOSO cells, four medians
  were read individually at this draft
  (Harappa 0.0066068; Mohenjo-daro 0.0237627;
  Dholavira 0.0243568; Lothal 0.0247476);
  claim F042-C02's boundary states exactly
  that scope.
- **Spec 028's frozen rules** — read in
  `specs/028-harappa-robustness/spec.md`:
  SUPPORTED iff controls pass, primary median
  adjusted R² > 0.01, and every LOSO median
  > 0.01; CONTRADICTED iff controls pass and
  (≥95% of primary draws fail to reject or
  the adjusted-R² interval lies entirely at
  or below 0.01); margin 0.01; seed 20261012.
  Spec §4.1 and claim F042-C10 carry them
  verbatim.
- **Input pins** — recomputed at this draft
  from `main` and stated in spec §2: corpus
  layer `c02e3d7b…`, phase393_results.json
  `0a1657a8…`, pipeline393.py `6c2ff91c…`,
  margins-audit.json `15ae0281…`, Spec 028
  freeze.json `376cd8e7…`.
- **Anchors caution, recorded** — the anchors
  file recomputes at this draft to
  `df0cf620…`. Spec 040's draft pinned
  `eccea6d5…` for the same file and its gate
  record found that pin stale. This draft
  therefore pins from a fresh recompute and
  says so (spec §2), rather than inheriting
  any earlier draft's pin.
- **The period question** — Spec 040's
  dependency-gate record (read on `main`)
  establishes that no site × local-label →
  coarse-period mapping exists. That is the
  ground for spec §5's "period described, not
  controlled" and for keeping D-26 separate
  (claim F042-C14).
- **Phase-number state** — Phase-400 (Spec
  036), Phase-401 (Spec 038), Phase-402 (Spec
  037), Phase-403 (Spec 039) are allocated;
  Spec 040 allocated none. Spec 042 allocates
  none at draft (DD-042-5).
- **Not done at draft, by design** — the
  stratum census (gates 0.3/0.4) has **not**
  been computed: the per-type, per-site counts
  of the analysis population appear nowhere
  in this draft, and the Arm B quota table in
  the Phase-393 results is per-draw
  allocations, not the census. No repertoire
  quantity was calculated, no code was
  written or run, the AEE hooks have not run,
  and nothing was filed with OSF.

## 3. What the freeze decision is asked to decide

1. Freeze this contract as drafted (digest in
   `freeze.md` / `freeze.json`), with every
   §2 pin re-asserted against the merged
   record — or decline, leaving
   `STUDY-SPEC-028/ARM-B` with its pooled
   INCONCLUSIVE record as the program's word
   on the object-type question: unasked.
2. **DD-042-6 (proposal): whether the frozen
   spec files its own OSF registration** —
   proposal: yes, following the Spec 027/028
   study-design pattern, so the split's
   gates, floors, and pattern rules are
   timestamped outside the repo before
   execution. Nothing is filed at draft.
3. **DD-042-7 (open): whether execution
   requires a fresh synthetic calibration.**
   Spec 028 required a calibration run for
   its machinery before Phase-393 executed.
   This draft's gate 0.5 (exact reproduction
   of the recorded pooled quantities) may or
   may not suffice for the split machinery;
   the draft takes no position. The freeze
   decides, and the decision is recorded.
4. **DD-042-8 (open): whether a separate
   margins audit is required.** Spec 028 ran
   a standalone margins audit before
   execution. This variant's margins
   instrument is the gate-0.3/0.4 census.
   Proposal: the census suffices; the freeze
   confirms or requires the fuller audit.

## 4. Draft-fixed readings (stand unless the freeze overturns them openly)

Each is labelled **DECIDED-BY-DRAFT**:

- **DD-042-1 — The variant appends; the
  frozen verdict is untouched.** The claim
  under test is `STUDY-SPEC-028/ARM-B`; this
  spec's outcome appends to its record as a
  dated, stratum-resolved entry. Spec 028's
  files and pooled verdict are never edited
  (claim F042-C05).
- **DD-042-2 — THIN closes the whole
  execution.** If either stratum is below
  its floor, neither stratum is computed.
  D-28 fixes the floors and the THIN headline
  but does not say whether the surviving
  stratum runs alone; the draft reads the
  design's pattern-first logic as closing the
  execution, because a one-stratum result
  quoted alone would misstate a test whose
  headline is a pattern (claim F042-C08,
  spec §3 gate 0.4).
- **DD-042-3 — NOT ADJUDICATED is the
  control-failure class.** The frozen family
  rules condition every verdict on controls
  passing and name no word for the contrary
  case. The draft adds NOT ADJUDICATED as a
  stop class (never folded into INCONCLUSIVE,
  which is a verdict about the claim) —
  claim F042-C13, spec §9.
- **DD-042-4 — Evidence carries
  `observed_at` from the draft.** The cited
  facts were verified first-hand today;
  Spec 038's freeze had to retrofit this
  field as a factual completion. Including it
  now is the same completion, done at the
  act that actually observed the records.
- **DD-042-5 — No execution phase number at
  draft.** Allocated at the freeze act, from
  the merged record as it then stands.

## 5. Renumber note — 2026-10-21

This draft was authored as Spec 041, in
parallel with the site × local-label
period-mapping act, which was assigned
Spec 041 first and retains it (PR #239).
To resolve the collision, this draft is
renumbered **Spec 042** on 2026-10-21:
the directory, claim ids (now
F042-C01…C15), decision ids (now
DD-042-1…8), and every self-reference
are renumbered to match. No substance
changed — the design, gates, verdict
rules, pins (the anchors pin stands at
`df0cf620…`), and open items are exactly
as drafted.
---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
