# Spec 060 — Adjudication Record

> ## ADJUDICATION INPUT — 2026-10-21
>
> This spec has three adjudication inputs,
> recorded here so the draft's basis is
> inspectable:
>
> 1. **The runnable-experiments campaign,
>    approved by the owner on 2026-10-21**
>    (`~/workspace/your_files/2026-10-21-runnable-experiments-campaign-plan.md`,
>    Parts 1–4). Spec 060 is member 17 of the
>    twenty: design D-23, drafted in the
>    campaign's drafting wave. The campaign
>    plan (Part 3) carries this member's
>    drafting correction in its own text.
> 2. **The portfolio triage of 2026-10-21**
>    (`~/workspace/research_notes/design-portfolio-triage-2026-10-21.md`):
>    design D-23 found **RIPE** — both layers
>    and the Phase-384 estimator in hand, no
>    verdict moves under the design — with the
>    correction recorded at §2 below.
> 3. **Design D-23 itself** (PR #195 packet,
>    `04-study-headlines.md` §D-23), which
>    governs this draft's substance in every
>    respect except the corrected hand-off.
>
> These inputs commission this **draft**.
> They are not a freeze order and not an
> execution order for Spec 060: both remain
> separate owner acts under the campaign's
> later waves.

## 1. The adopted basis (operative substance)

- **The design.** D-23: two arms on the
  residue of `STUDY-SPEC-024/F2-HOLDAT`.
  Arm 1 recomputes the bounded interval
  estimate (Phase-384 method, unchanged) and
  reports the verdict as a function of the
  margin on the fixed grid 0.05 / 0.075 /
  0.10 / 0.125 / 0.15 — a sensitivity display,
  explicitly not a verdict change. Arm 2
  restricts both layers to the sites and
  object types present in both, computes the
  site-effect size in each layer on that
  shared population with identical code, and
  compares the two intervals: overlap →
  COMPOSITION EXPLAINS THE GAP; still
  excluding → COMPOSITION DOES NOT; fewer
  than 5 shared sites or fewer than 500
  inscriptions in either layer → TOO THIN.
- **The claim.** `STUDY-SPEC-024/F2-HOLDAT`:
  SETTLED — CONTRADICTED at the declared
  margin 0.10 (Phase-384 v2 governing interval
  [0.0589, 0.0778]; descriptive V 0.1154;
  n = 1,670). Its family sibling F3-ICIT
  stands SUPPORTED at the same margin
  (interval [0.1823, 0.2104]; V 0.2190;
  n = 5,410). **No verdict moves under this
  design, by the design's own terms** — the
  limit is carried in spec §9 and claim
  F060-C06, exactly as written.
- **The estimator.** Phase-384 v2: the v1
  interval adjudication is INVALID (its own
  independence control showed the procedure
  non-discriminating); v2's inscription-level
  bootstrap with the basic interval governing
  is the estimator of record, frozen digest
  `4e6c78bc917c96a3…`.

## 2. The D-20 correction (mandatory; recorded openly)

**What the design said.** D-23's falsifier:
"On the shared population the two layers'
effect intervals still exclude each other —
the disagreement then lives in the
compilations' sign treatment, and **D-20's
attribution becomes the governing next
step** (the design says so in advance, so the
hand-off is pre-registered, not improvised)."

**What the record now is.** D-20 is
**complete**. Spec 034 (Phase-398, executed
2026-10-13) built the matched-object bridge,
passed its gate (169 matched objects against
a floor of 150), and returned **ATTRIBUTED
TO COMPOSITION**: matched-object median
distance 0.025694 against the frozen 0.20
line, the 0.32 transcription falsifier
nowhere near firing, residual 0.040340 of
the corpus-level distance. Its slice
description travels with it: the 169 matched
objects are all Mohenjo-daro seals. There is
no pending D-20 for a falsifier to hand off
to.

**What this draft does about it.** The
second arm is written against the finished
composition result, not against a pending
D-20:

1. Spec §2 states the correction in full —
   what the design said, what the record is,
   what the draft does — before the method.
2. Claim **F060-C05** registers the finished
   record as a pinned requirement; claim
   **F060-C04** registers the falsifier's
   outcome under the correction.
3. The pre-written COMPOSITION DOES NOT
   wording (spec §6.3) states the outcome
   **alongside** Spec 034's attribution —
   both statements stand, neither edits the
   other — names the unseparated candidate
   carriers without adjudicating among them,
   and expressly designs, registers, and
   implies **no successor study**: any
   successor enters through its own planning
   gate. The pre-registration the design
   wanted is preserved in form — the
   hand-off's destination is corrected to
   the record that actually exists.
4. A COMPOSITION EXPLAINS THE GAP outcome is
   reported as consonant with, and
   independent of, Spec 034's attribution
   (different question, different
   population), never as extending its
   slice.

No other part of D-23 is altered: hypothesis,
falsifier, margin grid, criteria words, and
TOO THIN floors are carried verbatim.

## 3. Verification record at draft

Verified first-hand at drafting, 2026-10-21,
from `main` at commit `83b6a563…` through the
repository's records (no local checkout was
used):

- **Design D-23** — read in full in the
  packet file: the two residues, hypothesis,
  falsifier (with the §2 hand-off), both
  arms' methods, the margin grid, the three
  arm-2 criteria words with their floors, the
  named confounders (site mix, period mix,
  sign numbering), and the limits (no verdict
  moves; does not establish no site effect).
- **Phase-384 record** — `phase384_results.json`
  and `phase384_report.md` read: F2 and F3
  point values, percentile and governing basic
  intervals, B = 9,999, seed 20261012; the v1
  INVALID adjudication and its independence
  control ([0.1115, 0.1242] on F2's margins
  under exact independence).
- **Phase-384 contract v2 and freeze v2** —
  read: the population-rebuild rule (Phase-137
  loaders, tables asserted equal to the
  record) that spec §4 gate 0.2 adopts; the
  freeze's sources record **matches** this
  draft's recomputed hashes for both the
  contract (`f0a67bd7…`) and the estimator
  script (`3313394e…`) — the estimator pin is
  therefore verified two ways.
- **Phase-137 record** — read: both layers'
  analysis populations (1,670 / 5,410),
  eligible-site lists (9 / 7; intersection of
  six sites, listed in spec §5.2), table
  dimensions (9 × 98 / 7 × 187), χ² and V,
  both layer-input hashes, and the strata
  definitions — including the record's own
  statement that **the Holdat layer carries
  no object-type field and its type mix is a
  constant**, the fact DD-060-3 rests on.
- **Phase-137 and Phase-384 machinery** —
  the loaders' fields read in source: Holdat
  loader uses `letters, position, seal_id,
  site`; ICIT loader uses `text, site, type`
  (type class from the `type` prefix). **No
  period field is read by either loader** —
  the fact DD-060-4 rests on.
- **Spec 034's record** — outcome read in
  full (§2 above): verdict, gate arithmetic
  (169 ≥ 150), median 0.025694, residual
  0.040340, slice description; freeze digest
  `696fd185…` read from its freeze record.
- **Input pins** — recomputed at this draft
  and stated in spec §3: phase137_results
  `18f86f45…`, phase384_results `dda6092d…`,
  phase137 machinery `e00dacf4…`, estimator
  `3313394e…`, contract v2 `f0a67bd7…`,
  freeze-v2 file `5749c6b8…`, Spec 034 outcome
  `c0cc615d…`, Spec 024 spec `a817f698…`,
  anchors `df0cf620…` (the same fresh value
  Spec 042's draft pinned; no earlier stale
  pin inherited).
- **The layers' pins are recorded, not
  recomputed** — the two layer files are not
  in this repository; their hashes in spec
  §3 are the values the Phase-137 results
  record for them, and gate 0.1 re-asserts
  them against the held files at the
  execution venue. This draft does not claim
  to have hashed the layer files themselves.
- **Not done at draft, by design** — the
  shared-population census (gate 0.4) has
  **not** been computed: the ICIT SEAL-only
  counts on the six shared sites appear
  nowhere in this draft. No shared-population
  quantity, no margin cell beyond the
  recorded 0.10 adjudication, and no code was
  written or run; the AEE hooks have not run;
  nothing was filed with OSF.

## 4. Acceptance tests — derived twice, independently

Per the campaign doctrine, each claim's
acceptance test was derived **twice**:
**Derivation A** from the design text and the
spec's requirement alone, and **Derivation B**
independently from the claim register and the
underlying records, without reference to A.
The register's `falsification_tests` carry the
resolved tests. Agreements and the five
disagreements, with their resolutions:

**Agreed on both derivations (no change):**
C01 (scope inspection), C03 (arm-2 overlap
test), C06 (file inspection + sentence
presence), C07 (gate-0.3 reproduction as the
operative test), C11 (gate-order inspection),
C12 (word derivable from published intervals),
C14 (code-path inspection), C15 (output
inspection).

**Disagreements and resolutions:**

- **DIS-060-1 (C02 — what tests the record
  claim).** A proposed re-deriving both
  intervals from the layer files. B objected:
  the layers are not in the repository, so
  that test cannot run at draft or freeze;
  the claim is a statement *about the record*.
  **Resolution:** the test is the record test
  (hash + read the pinned results file); the
  machinery-level reproduction is gate 0.3's
  job at execution, under C07/C11. A's intent
  (the numbers must be reproducible, not just
  quoted) is preserved there, not lost.
- **DIS-060-2 (C08 — the cell words).** A,
  following the F2 rule literally, derived
  two words (CONTRADICTED AT m / STRADDLES m).
  B noted the interval could in principle sit
  entirely above a small grid margin (0.05),
  leaving a cell with no word. **Resolution:**
  the symmetric third word SUPPORTED AT m is
  adopted, mirroring the family's F3 rule;
  the curve in fact fires it at 0.05 on the
  recorded interval — a completeness the
  design's grid requires and its text leaves
  implicit. Recorded here so the freeze sees
  the addition as a drafting act, not a
  quotation.
- **DIS-060-3 (C09 — object types).** A read
  "same object types" as a symmetric
  restriction on both layers. B found, in the
  Phase-137 record and loader source, that
  the Holdat layer has **no object-type
  field at all** — a symmetric restriction
  is unimplementable as written. **Resolution:**
  DD-060-3's SEAL-constant reading (Holdat
  whole; ICIT restricted to its recorded
  SEAL class). This is a defect in the
  design's wording found at drafting,
  resolved by the only reading the record
  supports, and flagged OPEN-adjacent: the
  freeze confirms or replaces it openly.
- **DIS-060-4 (C10 — THIN's scope).** A,
  reasoning from pattern-headline designs
  (compare Spec 042's DD-042-2), closed the
  whole execution on a thin census. B noted
  the arms here are independent — arm 1 uses
  the full Holdat population and answers a
  different residue — so a whole-execution
  closure would destroy a product the gate
  does not touch. **Resolution:** TOO THIN
  closes arm 2 only (DD-060-2); the freeze
  may overturn it, and tasks L5 puts the
  question to it explicitly.
- **DIS-060-5 (C13 — period mix).** A assumed
  the design's "period mix described per
  layer" could be met from the program's
  chronology assets. B found neither loader
  reads a period field and no frozen mapping
  assigns periods to these layers'
  inscriptions; importing one would change
  the design's inputs unregistered.
  **Resolution:** DD-060-4's
  stated-unavailability wording, per layer,
  with the freeze permitted to replace it
  only by naming a source and rule openly.

## 5. What the freeze decision is asked to decide

1. Freeze this contract as drafted (digest in
   `freeze.md` / `freeze.json`), with every
   §3 pin re-asserted against the merged
   record — the two layer pins re-asserted
   against the held files at the freeze's
   venue — or decline, leaving F2's residue
   with its recorded state: margin-dependence
   unpublished, layer disagreement located
   only by Spec 034's different question.
2. **DD-060-6 (proposal): whether the frozen
   spec files its own OSF registration** —
   proposal: yes, following the campaign's
   E-1 policy (every specification in the
   pass registers at its freeze) and the
   Spec 027/028/034 study pattern. Nothing
   is filed at draft.
3. **DD-060-7 (open): whether execution
   requires a fresh synthetic calibration.**
   This draft's gate 0.3 (exact reproduction
   of both recorded governing intervals) may
   or may not suffice for the estimator on
   the *restricted* shared population, whose
   tables are smaller and sparser. The draft
   takes no position. The freeze decides,
   and the decision is recorded.
4. **DD-060-8 (open): the execution venue
   for the held layers.** The layers live
   outside the repository (the Phase-137
   loaders' default paths name two different
   checkouts). The freeze names the venue
   and the copies whose hashes gate 0.1
   will assert.

## 6. Draft-fixed readings (stand unless the freeze overturns them openly)

Each is labelled **DECIDED-BY-DRAFT**:

- **DD-060-1 — This spec appends; the frozen
  verdicts are untouched.** Outcomes append
  to `STUDY-SPEC-024/F2-HOLDAT`'s record as
  dated entries. Spec 024's, Phase-137's, and
  Phase-384's files and verdicts are never
  edited (claims F060-C06, F060-C15).
- **DD-060-2 — TOO THIN closes arm 2 only.**
  Arm 1's margin curve is independent of the
  shared census and still reports (claim
  F060-C10; DIS-060-4).
- **DD-060-3 — The shared type is SEAL, the
  Holdat layer's constant.** The design's
  "same object types" is read against the
  record: Holdat carries no type field, so
  the type present in both layers is SEAL;
  Holdat enters whole, ICIT is restricted
  to its recorded SEAL class (claim
  F060-C09; DIS-060-3).
- **DD-060-4 — Period mix is described only
  from what the layers carry.** Where a
  layer carries no period field in its
  loader's fields, the outcome states the
  unavailability in the frozen words of
  claim F060-C13 rather than importing an
  assignment (DIS-060-5).
- **DD-060-5 — No execution phase number at
  draft.** Allocated at the freeze act, from
  the merged record as it then stands.
- **DD-060-9 — Evidence carries
  `observed_at` from the draft.** The cited
  facts were verified first-hand today; the
  layer-hash evidence states, in its own
  text, that those two pins are recorded
  values re-asserted at step 0, not hashes
  recomputed at this draft.

## 7. OPEN items for the freeze (consolidated)

- **OPEN-060-1** — DD-060-6: OSF registration
  at freeze (proposal: yes, per campaign E-1).
- **OPEN-060-2** — DD-060-7: synthetic
  calibration for the restricted-population
  estimator, beyond gate 0.3.
- **OPEN-060-3** — DD-060-8: execution venue
  and authoritative copies of the two held
  layers.
- **OPEN-060-4** — Confirm or overturn
  DD-060-2 (TOO THIN closes arm 2 only) and
  DD-060-3 (SEAL-constant shared type) and
  DD-060-4 (period stated-unavailability).
- **OPEN-060-5** — AEE lifecycle hooks (tasks
  L4): not run on this draft; any recovery
  they force changes claim text before the
  freeze digest is computed.
- **OPEN-060-6** — Execution phase number
  (DD-060-5), allocated at freeze.
---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
