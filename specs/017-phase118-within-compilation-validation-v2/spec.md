# Spec 017 — Phase-118: Within-Compilation Validation Battery v2 (W1-Primary, Cross-Fit W3) for the 44 Flagged Anchors (pre-registration)

**Status:** DESIGN FROZEN 2026-10-07 on
`phase/118-within-compilation-battery-v2`, stacked on PR #75's
branch `phase/117-within-compilation-battery` (head `3ee5ee94`).
Owner authorization: Tristen Pierson, 2026-10-07 — commission
of spec 017 (the W1-primary redesign), covering **both this
design and its execution** in one authorization (contrast
spec 016, whose design and execution were approved in two
steps). This spec is committed before any Phase-118 battery
statistic exists: the only numbers computed at design stage
are the instrument feasibility statistics of Appendix A
(attestation counts and judgeability under the frozen
definitions — no sign is scored, no profile is compared, no
verdict is produced), per the program's pre-freeze
measurement precedent (spec 014 §§1–2, spec 016 Appendix A).

**Stacking note:** this branch is cut from PR #75's branch
head because Phase-117's pipeline code
(`phase117_battery.py`, `phase117_run.py`) is unmerged and
this phase reuses its machinery. This phase's PR is opened
with base = `phase/117-within-compilation-battery` and
retargets to main when PR #75 merges. HEAD tree content of
the stacked base is exactly PR #75's tree; nothing in this
spec depends on unmerged Phase-117 *results* beyond the
published calibration record used as design evidence in the
Context section.

**Phase-numbering note:** ledger-sequence **Phase-118**
(Phase-113 spec 011, Phase-114 spec 012, Phase-115 spec 014,
Phase-116 spec 015, Phase-117 spec 016 precede it). Artifact
names carry the phase number (`phase118_battery`,
`phase118_run`, graph node
`IndusPhase118WithinCompilationValidation`).

**AI disclosure:** this study is designed for execution by an
AI agent (Muse Spark, via Muse) at the direction of
Tristen Pierson, per constitution §VI.

## Context — why this phase exists, and what Phase-117 measured

Phase-117 (spec 016) executed the first within-compilation
battery. Its frozen gates (§6 of spec 016) rejected the
battery at calibration: STRICT94 leave-one-out VALIDATED
**2 of 94** (gate ≥ 47), KUR113 VALIDATED 0 of 113 (gate
≤ 5, passed). The per-instrument calibration record
(`reports/phase117_within_battery_results.json`) localizes
the failure, and this redesign is built on that record —
quoted here as design evidence, not re-derived:

- **W1 (split-half positional cross-fit) was sound:** PASS
  63 / FAIL 5 / INDETERMINATE 26 on STRICT94. The positional
  cross-fit leg judged the core the way a calibration
  instrument should.
- **W4 was serviceable:** PASS 44 / FAIL 10 / INDETERMINATE
  40 on STRICT94.
- **W3 (junction coherence) was the binding constraint, and
  its construction was self-defeating.** Spec 016's §8 rule
  made W3's PASS mandatory for every validation, and W3
  PASSED only **3 of 94** strict signs (FAIL 9, INDETERMINATE
  82). Two distinct defects, both visible in the recorded
  numbers:
  1. *The reference was leave-one-out-minus-self.* Each core
     sign was scored against a junction model built from the
     core minus itself — removing the sign removes its own
     junction evidence from the model against which its
     coherence is judged. φ (the 10th percentile of those
     LOO self-scores) settled at **−7.461366**.
  2. *The PASS band's donor leg was miscalibrated to the
     instrument's power.* PASS required p ≤ 0.05 — the
     sign's own reading beating ≥ 95% of frequency-band
     donor readings. Of the 81 judged core signs, 73 cleared
     the absolute leg (score ≥ φ) but only **3** attained
     p ≤ 0.05; core p-values centered at median **0.627**.
     At per-sign junction counts of ~10, a top-5%-of-donors
     demand is beyond the instrument's resolution.
- **The negative gate passed vacuously.** KUR113 returned
  INDETERMINATE on **every instrument for all 113 signs** —
  not one FAIL. Under spec 016's W3 FAIL band (p ≥ 0.50 ∧
  score < φ), the 24 judged kur signs met it **0 times**:
  every judged kur sign had p ≥ 0.50 (median 0.645) but
  also score ≥ φ (median score −4.863, above the core
  median −5.333), so the conjunctive FAIL never fired. The
  ≤ 5 gate therefore certified nothing about discrimination:
  it passed on universal indeterminacy. **A calibration gate
  that passes on universal indeterminacy is a failed design,
  and this spec's §6 is written so that it cannot happen
  again (§6, negative gate).**

Phase-116's constraint still binds every instrument: no
cross-corpus gate on the Holdat/ICIT pair; validation
proceeds within Holdat or not at all. Governance rule
**H26** still frames the question: no SA output, SA score,
SA-derived language model, or SA modal reading is an input
to any instrument in this battery.

**Fate of the spec-016 components** (recorded so nothing is
silently dropped or silently kept):

| Spec-016 component | Fate in this spec | Basis |
|---|---|---|
| W1 split-half cross-fit (§4.1) | **Primary instrument**; construction, partition, and thresholds carried over **verbatim, unretuned** | Phase-117 calibration: 63/94 PASS on the core — the measured-sound leg; the commission names it primary |
| W2 iconographic co-occurrence | **Remains dropped** as a decision-bearing instrument (§4.2) | Spec 016 §4.2 / Appendix A.3 numbers stand unaltered |
| W3 junction coherence (§4.3) | **Rebuilt as cross-fit** (§4.3): junction model and φ both derived cross-half; LOO-minus-self reference abolished; donor null retained as the discrimination leg with bands re-frozen (§4.3) | The two recorded defects above |
| W4 stratum stability (§4.4) | Carried over **verbatim**; role narrowed to **FAIL-guard only** | Its PASS no longer substitutes for W1's in §8: the primary instrument's PASS is mandatory under the commission. Its FAIL (a positive contradiction at strong attestation) retains veto power |
| Calibration gates (§6) | **Replaced** (§6): positive gate over judgeable core signs with a frozen minimum judgeable count; negative gate requires demonstrated discrimination | The vacuous-pass defect recorded above |
| Decision rule (§8) | **W1-primary conjunction** (§8) | The commission; Phase-117's diagnosis |
| Claim scope (§9) | **Carried over verbatim in substance** (§9) | The status value and its limits are unchanged |

## 1. Data (frozen inputs)

Identical to spec 016 §1:

| Input | Path | Role |
|---|---|---|
| Anchors (287) | `backend/reports/INDUS_FINAL_ANCHORS.json` | target + calibration sets; the only file an execution may modify, and only per §8 |
| Provenance register | `reports/phase108_provenance_register.json` | set definitions (category, `sa_in_chain`) |
| Holdat corpus | `corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv` (gitignored; located in the main checkout) | the sole corpus for W1–W4; loaded with the `load_holdat_corpus` machinery of `glossa_lab/pipelines/sa_validation.py` (loader only — no SA code is executed) |

Holdat, as loaded: **1,670 inscriptions / 7,002 tokens**,
inscription lengths 2–8, 9 sites. **No other corpus is an
input to any instrument.** The anchors file on this stacked
branch is byte-identical to the one spec 016 executed
against: Phase-117 modified no anchor (its battery was
rejected at calibration), so every set assertion of spec 016
§2 is re-asserted unchanged in §2 below.

Holdat is used locally under its recorded terms (Phase-107
acquisition log); it is never committed or redistributed.
Published artifacts contain only counts, shares, distances,
scores, and verdicts.

## 2. Sets (frozen definitions; recomputed at run time and asserted — spec 016 §2 verbatim)

- **FLAGGED44** — anchors with
  `validation_status == "pending_non_sa_validation"`. Asserted:
  |FLAGGED44| = 44; equals register categories SA_DERIVED (24)
  ∪ SA_CONFIRMED_ONLY (20); tiers 43 HIGH + 1 MEDIUM (M293).
- **STRICT94** (the strict SA-independent core) — register
  category ∉ {SA_DERIVED, SA_CONFIRMED_ONLY} ∧ `sa_in_chain ==
  false` ∧ tier ∈ {HIGH, MEDIUM}. Asserted: |STRICT94| = 94
  (90 HIGH + 4 MEDIUM); disjoint from FLAGGED44; Holdat token
  coverage 5,159 / 7,002 = 0.7368 (tolerance ±0.001).
- **KUR113** (negative control) — anchors with
  `validation_status == "premise_superseded"`; asserted
  |KUR113| = 113, all readings `kur`, all Holdat counts ≤ 4.

Calibration sets are evaluated read-only; their anchors are
never modified by this phase.

### 2.1 Judgeability (frozen definitions; the §6 gate denominators)

Judgeability is a **count property**, determined by the
frozen floors of §§4–5 alone — never by any score, state, or
outcome. (Spec 016 Appendix A's precedent: "≥ 4 tokens in
both halves" defined W1 judgeability without reference to
verdicts; centroid-undefined and band outcomes are verdicts
*inside* the judgeable set, not exclusions from it.)

- **W1-scorable(s)** ⟺ s has ≥ **4** Holdat tokens in half A
  **and** ≥ 4 in half B (the §3 partition).
- **W3-scorable(s)** ⟺ in **each** direction of §4.3, s has
  ≥ **2** junction observations on the scoring half (other
  sign ∈ the evaluation core; for STRICT94 calibration, the
  core minus s) **and** s's donor band (§4.3) is non-empty.
- **J94** = {s ∈ STRICT94 : W1-scorable(s) ∧ W3-scorable(s)}.
  Design-stage count (Appendix A): **|J94| = 67**. An
  execution recomputes J94 under these definitions and
  asserts equality with 67 before calibrating; a mismatch is
  an execution error and stops the run.
- **JKUR** = {s ∈ KUR113 : W3-scorable(s)}. (No kur sign is
  W1-scorable — all Holdat counts ≤ 4 cannot reach ≥ 4 in
  both halves — or W4-judgeable, so W3 is the only instrument
  that can judge the negative control at all; §6's negative
  gate is defined on W3's set.) Design-stage count:
  **|JKUR| = 29**. Asserted as for J94.

## 3. Conventions (frozen)

Positional profiles, modal class, tie order (INITIAL,
TERMINAL, MEDIAL), TV distance, reading normalization, the
phoneme inventory, and the syllable canon are spec 011 §3
verbatim, implemented by reusing `phase113_battery`
machinery (profiles, `normalize_reading`, `canon_legal`),
exactly as spec 016 §3. A sign's **initial phoneme** /
**final phoneme** are the first / last phonemes of its
normalized reading under the §3 tokenizer.

**The frozen partition.** Identical to spec 016 §3 — the
same partition, not a re-draw: strata are the 15 cells of
(length bin ∈ {2, 3, 4, 5, 6+} × site group ∈ {Mohenjo-daro,
Harappa, OTHER}); within each stratum, inscriptions in
loader order are shuffled with Python `random.Random(117)`
(strata in sorted key order, one stream) and dealt
alternately A, B, A, B, … beginning with A. Design-stage
totals A = 3,531 / B = 3,471 tokens; an execution must
reproduce and assert them before any instrument runs. W1's
construction *is* this partition (§4.1 carries spec 016
verbatim); re-drawing it would silently replace the primary
instrument.

**Seeded streams.** (i) The partition shuffle (§3), seed
117, as above. (ii) The W3 donor stream: one
`random.Random(118)` for the whole execution, instantiated
separately from the partition stream, consumed in
sorted-sign order across the evaluation sets in the frozen
order STRICT94 calibration → KUR113 → FLAGGED44, and within
each sign in direction order modelA→scoreB, then
modelB→scoreA. (The new seed is this spec's own constant,
frozen here; Phase-117's draws are not reused.) (iii) No
other randomness exists in the battery. Determinism:
re-running an execution on the same inputs reproduces its
reports byte-identically except timestamps.

## 4. The battery (frozen)

Every instrument returns one state per tested sign from
{PASS, FAIL, INDETERMINATE}. Guards gate PASS and FAIL alike:
an instrument that cannot judge returns INDETERMINATE and
records its reason; no instrument consults any SA artifact,
any anchor's `basis` text, any ICIT artifact, or any prior
phase's verdict about the tested sign.

### 4.1 W1 — Split-half positional cross-fit (PRIMARY; spec 016 §4.1 verbatim)

For direction A→B: the positional model is derived on half
A and the tested sign is scored on half B; direction B→A
symmetrically.

- **Model (per half).** For each modal class k, the centroid
  is the token-weighted mean Holdat positional profile of
  STRICT94 signs whose modal class **on that half** is k,
  over core signs with ≥ 1 token on that half. Under
  leave-one-out (STRICT94 calibration), the tested sign is
  excluded from its own model.
- **Per-direction state** for sign s, scoring half S, model
  half M: if n_S(s) < **4** → INDETERMINATE
  (`half_count_below_floor`). Else let m = modal class of
  s's profile on S; if no core sign has modal class m on M
  (no centroid exists) → INDETERMINATE
  (`centroid_undefined`). Else PASS iff
  TV(profile_S(s), centroid^M_m) ≤ **0.35** and modal
  share_S(s) ≥ **0.45**; else FAIL. (Thresholds are
  spec-011 T2a's, carried through spec 016 unchanged and
  unchanged here: the instrument was measured sound at
  these numbers, and they are not re-tuned.)
- **Combination.** W1 = FAIL iff either direction FAILs;
  PASS iff both directions PASS; else INDETERMINATE.

### 4.2 W2 — Iconographic co-occurrence: REMAINS DROPPED

Spec 016 §4.2's frozen decision stands unaltered: W2 is not
an instrument of this battery; it produces no state, gates
nothing, and appears in no decision rule. Its statistics
(partner support, context counts, composed legality) are
recorded descriptively in the W3 record (§4.3), never
gated, exactly as in Phase-117.

### 4.3 W3 — Distributional-neighborhood coherence, REBUILT as cross-fit

Tests whether the tested sign's observed Holdat bigram
neighborhood is better explained under its proposed
reading's sequential profile than under readings donated by
comparably-attested anchored signs — with **every**
reference quantity (junction model and φ alike) derived on
the opposite partition half from the observations scored,
mirroring W1's cross-fit discipline. The spec-016
leave-one-out-minus-self reference is abolished: a core sign
is never in its direction's model (below), but the model is
built from a full half of the corpus rather than from the
core with the sign's own evidence surgically removed from
the same inscriptions it is scored on.

**Directions.** Two, named for W1's convention:
modelA→scoreB (model on half A's inscriptions, observations
on half B's) and modelB→scoreA (the mirror).

- **Junction observations (per direction).** Over the
  **scoring half's** inscriptions: every ordered adjacent
  pair (x, s) and (s, y) with the other sign ∈ the
  evaluation core (STRICT94 as-is; under STRICT94
  calibration, STRICT94 minus the tested sign).
  n_{j,d}(s) = their count in direction d. Guard:
  n_{j,d}(s) < **2** → that direction is INDETERMINATE
  (`junction_floor_half`); no directional FAIL is possible
  below the floor. (Floor basis: Appendix A.1 — floor 3
  collapses JKUR to 4 signs and floor 4 to 1, silencing the
  negative control exactly as spec 016's floor table warned
  against; floor 2 is the largest per-direction floor at
  which the negative control (29), the judgeable core (67),
  and the flagged cohort (34/44 W3-scorable) all remain
  testable. The cost — a directional score may average as
  few as 2 junction observations — is registered in §10,
  not hidden.)
- **Junction model (per direction).** Over the **model
  half's** inscriptions: counts C(f, i) of (final phoneme
  of u's reading, initial phoneme of v's reading) over all
  ordered adjacent pairs (u, v) with u, v ∈ the model core
  (the evaluation core; under STRICT94 calibration, minus
  the tested sign — a tested core sign's pairs appear in
  neither direction's model). P(f, i) = (C(f, i) + 0.5) /
  (N + 0.5·|G|), N = the model half's core junction count,
  G = (attested final phonemes of model-core readings) ×
  (attested initial phonemes of model-core readings). (The
  smoothing and grid construction are spec 016 §4.3's,
  applied per direction.)
- **Score (per direction).** score_d(s) = mean over s's
  direction-d junction observations of log P(final phoneme
  of the left reading, initial phoneme of the right
  reading), with s's proposed reading supplying its own
  initial/final phonemes and each core neighbor its core
  reading — spec 016 §4.3's score, computed cross-half.
- **Absolute floor φ_d (per direction).** φ_d = the
  **10th percentile** of STRICT94 **cross-fit self-scores**
  in direction d: for each core sign t scorable in d
  (n_{j,d}(t) ≥ 2 against core minus t), score_d(t) under
  the model built without t. The percentile is the
  linear-interpolation (type-7) percentile — the convention
  Phase-117 disclosed for spec 016's φ, stated here in the
  frozen text rather than left to the summary. Design-stage
  self-score set sizes: |S_{A→B}| = 83, |S_{B→A}| = 89
  (Appendix A). φ_{A→B} and φ_{B→A} are computed inside the
  calibration run, before the §6 gates are evaluated, and
  recorded in the results. φ is a property of the core's
  cross-fit score distribution in each direction, computed
  once over all scorable core signs (a core sign's own
  self-score is a member of its direction's set, exactly as
  in spec 016's φ construction).
- **Donor-permutation null (per direction; the
  discrimination leg).** B = **999** replicates. Each
  replicate draws one donor reading uniformly (donor stream
  (ii), §3) from the readings of anchored signs t ≠ s (all
  287 anchor entries) with Holdat count n_H(t) ∈
  [⌈n_H(s)/3⌉, 3·n_H(s)] — the band is on the sign's
  **total** Holdat count, as in spec 016 — and recomputes
  score_d(s) with the donor's initial/final phonemes
  substituted for s's own (neighbors, positions, and the
  direction's model unchanged). If the donor band is empty
  → the direction is INDETERMINATE (`donor_band_empty`).
  p_d(s) = (1 + #{b : score_b ≥ score_d(s)}) / (1 + B).
- **Bands (per direction, frozen).**
  PASS_d ⟺ score_d(s) ≥ φ_d **and** p_d(s) ≤ **0.50**.
  FAIL_d ⟺ score_d(s) < φ_d **and** p_d(s) ≥ **0.50**.
  Else INDETERMINATE_d.
  *Basis, recorded at freeze:* spec 016's PASS leg
  (p ≤ 0.05) demanded the sign's reading beat ≥ 95% of
  frequency-band donors; Phase-117 measured that demand
  attained by 3 of 81 judged core signs (core p median
  0.627) — a threshold beyond the instrument's per-sign
  resolution at these junction counts, so it functioned as
  a near-universal veto rather than a coherence criterion.
  The 0.50 leg is the median-donor criterion: the sign's own
  reading must explain its held-out junctions at least as
  well as the median comparably-attested alternative
  reading, in both directions, and must additionally clear
  the direction's absolute core floor φ_d. The FAIL leg is
  its exact mirror (below the core floor **and** worse
  than the median donor). These bands are frozen knowing
  Phase-117's geometry; if the cross-fit geometry does not
  in fact produce core validation and kur discrimination,
  §6's gates reject this battery and that rejection is the
  recorded answer — the bands are not adjusted after this
  freeze under any outcome (§12).
- **Combination.** W3 = FAIL iff either direction FAILs;
  PASS iff both directions PASS; else INDETERMINATE —
  W1's combination rule, mirrored.
- **Recorded descriptively (never gated):** partner support
  and context counts and the composed-legality fraction
  (§4.2), computed against the evaluation core over the
  full inscription list, as in Phase-117.

### 4.4 W4 — Stratum stability (spec 016 §4.4 verbatim; FAIL-guard only)

Holdat carries site per inscription and no material field;
the frozen strata are **sites**.

- **Qualifying stratum** for s: a site with n_site(s) ≥
  **4** tokens of s. Guard: fewer than 2 qualifying strata
  → INDETERMINATE (`strata_below_two`).
- **PASS** iff the modal class of s is identical across all
  qualifying strata and every pairwise TV between
  qualifying-stratum profiles ≤ **0.40**.
- **FAIL** iff two qualifying strata with n_site(s) ≥ **8**
  each disagree in modal class.
- Else INDETERMINATE.

Role in this spec: W4's state is computed and recorded
exactly as in Phase-117, and its FAIL demotes (§8), but its
PASS has **no positive effect** — it cannot substitute for
W1's PASS, which §8 makes mandatory. (Spec 016 §8 admitted
W4's PASS as an alternative positional leg; the commission
makes W1 the primary instrument, and the substitution is
removed on that basis, recorded here.)

## 5. Sparsity rules (frozen; consolidated)

Insufficient data maps to INDETERMINATE per instrument (per
direction for W1/W3), mechanically, with the recorded
reason — never to a judgment call, never post-hoc:

| Instrument | Insufficient-data condition | State |
|---|---|---|
| W1 | n < 4 in a scoring half, or centroid undefined for the direction | direction INDETERMINATE (`half_count_below_floor` / `centroid_undefined`) |
| W3 | n_{j,d}(s) < 2 in a direction, or donor band empty | direction INDETERMINATE (`junction_floor_half` / `donor_band_empty`) |
| W4 | < 2 sites with ≥ 4 tokens | INDETERMINATE (`strata_below_two`) |

Design-stage expectations under these rules (Appendix A):
W1 fully judges (both directions scorable) 13/44 flagged
anchors, 68/94 STRICT94, 0/113 KUR113; W3 (both directions)
judges 34/44, 80/94, 29/113; W4 judges 9/44, 57/94, 0/113.
**37/44 flagged anchors are judgeable by at least one
instrument**; the §8 VALIDATED conjunction is reachable by
at most **11/44** (the W1-scorable ∧ W3-scorable flagged
signs) — a registered property of this design, stated
before any run. M235, M254, M402 are judgeable by **no**
instrument (W1: a half below 4 tokens; W3: a direction
below 2 junction observations; W4: no qualifying stratum)
and are therefore UNRESOLVED by construction under §8 —
recorded now, under this spec as under spec 016, so their
outcome is a property of the frozen design, not a result.

## 6. Calibration gates (frozen; evaluated BEFORE the 44 are run)

The battery is applied, unchanged, to the two calibration
sets, with φ_{A→B} and φ_{B→A} computed from STRICT94
cross-fit self-scores first (§4.3). Judgeability is
recomputed under §2.1 and asserted (J94 = 67, JKUR = 29)
before either gate is evaluated.

- **Positive gate.** Denominator J94 (§2.1). A sign outside
  J94 cannot reach §8's VALIDATED (an unscorable W1 or W3
  direction is INDETERMINATE, and §8 requires both PASS),
  so the validated count over J94 is the validated count
  over STRICT94; the denominator is what this gate fixes.
  Acceptance: **|J94| ≥ 50** (met at design stage: 67) and
  **VALIDATED(J94) / |J94| ≥ 0.50**. Basis: Phase-117's W1 —
  the primary instrument — PASSED 63/94 core signs under
  its own discipline, and §8 additionally requires the
  rebuilt W3's PASS in both directions; one-half of the
  judgeable core validating under a two-instrument
  cross-fit conjunction is the demanding bar, set at the
  same 50% level spec 016 set over its (sparsity-inflated)
  full-core denominator.
- **Negative gate.** Denominator JKUR (§2.1): the 29 kur
  signs W3 can judge — the only judgeable members of the
  negative control under any instrument. Acceptance:
  **|JKUR| ≥ 8** (met at design stage: 29) and
  **VALIDATED(JKUR) = 0** and **DEMOTE(JKUR) / |JKUR| ≥
  0.25**. For kur signs a DEMOTE can arise only from W3's
  FAIL (W1 and W4 are structurally INDETERMINATE for the
  whole cohort — §2.1), so the failed-share clause is a
  direct measurement of the discrimination leg: at least
  one in four judgeable known-bad readings must be
  **actively failed**, not merely unvalidated. A gate that
  passes on universal indeterminacy is a failed design
  (the spec-016 negative gate's recorded defect); under
  this gate, universal indeterminacy among JKUR yields
  DEMOTE share 0 and the battery is rejected.

If either gate fails, the battery is **rejected**: the
execution stops, FLAGGED44 is never run, the anchors file
is not modified, and the results/summary/ledger record the
rejection with the calibration numbers — including the
judgeable counts and the kur discrimination tallies
(validated / demoted / unresolved within JKUR). A rejected
battery may not be re-tuned and re-run under this spec; a
redesigned battery requires a new spec. No threshold,
floor, band, or gate in §§3–8 is adjustable after this
freeze.

## 7. (Reserved)

Numbering note: calibration gates are §6; the decision rule
is §8; anti-circularity and claim scope are §9. (Sections
numbered to keep gates adjacent to the instruments they
govern; no content is omitted.)

## 8. Decision rule (frozen; applied mechanically to FLAGGED44, only if both §6 gates pass)

Per anchor, from (W1, W3, W4) ∈ {PASS, FAIL, INDETERMINATE}:

- **VALIDATED** ⟺ W1 = PASS ∧ W3 = PASS ∧ no instrument =
  FAIL. Action: `validation_status` :=
  `validated_within_compilation` (§9 defines this value);
  `evidence_ref` appended (Phase-118, spec 017); tier
  unchanged; `phase118_annotation` records the outcome and
  per-instrument states and statistics.
- **DEMOTE** ⟺ any instrument = FAIL. Action: `confidence`
  := CANDIDATE; `validation_status` :=
  `failed_within_compilation_validation`; annotation records
  which instrument(s) failed and their statistics.
- **UNRESOLVED** ⟺ otherwise (no FAIL; the VALIDATED
  conjunction unmet — including all-INDETERMINATE).
  Action: no tier change; `validation_status` stays
  `pending_non_sa_validation`; annotation records UNRESOLVED
  with per-instrument states and reasons.

The conjunction's shape is the commission's, and the reason
is frozen with it: W1 is the primary instrument — the leg
Phase-117 measured sound on the core — so its PASS is
mandatory; the rebuilt W3's PASS, in both cross-fit
directions against the retained donor null, is the second,
independent instrument family; and every instrument
(including the FAIL-guard W4) holds veto power, so each
demotion is supported by a positive contradiction and each
validation by two families with none contradicting. Spec
016's (W1 ∨ W4) positional alternation is removed (§4.4).

Every action (and every UNRESOLVED non-action) is one record
in the change register. No other anchor-file field is
modified; no anchor outside FLAGGED44 is modified under any
outcome; **this phase never promotes any anchor's tier**.

## 9. Anti-circularity and claim scope (frozen; load-bearing; spec 016 §9 carried over verbatim in substance)

Within-compilation validation is **not** independence. The
44 anchors' SA lineage was derived against this same
compilation; STRICT94's readings — the reference fabric for
W1's centroids, W3's junction model, and W4's strata — are
themselves decipherment claims carried in the same anchor
table. Split-half discipline (W1) and cross-fit calibration
(W3, rebuilt under this spec on the same principle) remove
the mechanical self-agreement of
derive-and-test-on-identical-tokens; they cannot manufacture
an independent witness. This section defines, immutably for
this spec, what outcomes mean:

- The success status value is
  **`validated_within_compilation`** — the value coined in
  spec 016 §9, carried unchanged. It must not be shortened
  to `validated`, must not be conflated with spec 011/014's
  `validated_non_sa` (a status no battery has ever awarded),
  and must not be described in any report, summary, ledger,
  paper, or preprint as "independent validation", "external
  validation", or "confirmation" of a reading.
- A VALIDATED outcome supports exactly this claim: **the
  anchor's reading and positional behavior are internally
  coherent with the strict SA-independent core's
  distributional and sequential fabric inside Holdat, under
  split-half and permutation-null discipline, at the frozen
  thresholds.** It supports no claim about the reading's
  phonetic correctness, and no claim of independence from
  the derivation compilation.
- The anchors' provenance categories (SA_DERIVED /
  SA_CONFIRMED_ONLY) are **not** altered by any outcome of
  this phase: the register's record that these values arrived
  via the SA lineage stands permanently. A
  `validated_within_compilation` anchor remains an SA-lineage
  anchor that has additionally passed an internal-coherence
  battery — both facts travel together in any publication.
- A DEMOTE outcome supports exactly: the anchor's claims
  contradict Holdat-internal evidence (cross-half positional
  fit, null-tested neighborhood coherence, or stratum
  stability) at the frozen thresholds. It demotes to
  CANDIDATE; it does not declare the reading false.
- Any genuinely independent corpus test (e.g. RMRL or Mitra
  data, when and if obtained) **supersedes** this battery's
  outcomes for any anchor it can judge: within-compilation
  statuses are explicitly provisional against independent
  evidence, and a future spec must say how conflicts resolve
  before it runs. This battery's outcomes never satisfy
  governance rule H26's non-SA-evidence bar for promotion —
  and this phase promotes nothing in any case.

## 10. Limitations (registered at freeze)

- **Single-compilation ceiling (§9):** every instrument
  measures coherence inside one modern compilation of the
  same published catalogues. Systematic error in Holdat, or
  in STRICT94's readings, is invisible to this battery by
  construction; the calibration gates check discrimination,
  not truth.
- **Cross-fit halves the evidence twice over:** W1's model
  and scoring halves are disjoint (as in spec 016), and
  W3's rebuilt construction now derives its junction model
  and its score from disjoint halves as well. Each
  directional W3 score therefore averages the sign's
  junction observations in one half only, under a model
  built from the other half's core pairs. This is the
  discipline the redesign was commissioned to impose; its
  power cost is real and is part of what calibration
  measures.
- **Per-direction junction floor 2:** a directional score
  may average as few as 2 junction observations. The floor
  is the largest at which the negative control remains
  testable (Appendix A.1), but directional scores at the
  floor are high-variance; the both-directions PASS
  requirement and the donor null computed on the same
  observations are the registered mitigations, not a cure.
- **Negative gate rests on one instrument family and 29
  signs:** JKUR is judgeable only by W3 (§2.1); the
  discrimination clause (§6) measures W3's FAIL behavior on
  29 rare signs. It cannot speak to the 84 unjudgeable kur
  signs, and a pass certifies discrimination on exactly the
  judgeable minority — no more.
- **Validation cap:** §8's conjunction is reachable by at
  most 11/44 flagged anchors (§5); 26 further anchors can be
  demoted or left unresolved but cannot validate under this
  design, however coherent their readings. M235, M254, M402
  cannot be judged at all (§5).
- **Junction-model dependence on core readings:** W3's
  models are built from STRICT94 *readings* — if core
  readings were systematically wrong in a phoneme-class-
  preserving way, W3 would reward conformity to that
  wrongness. The donor null bounds the effect to
  frequency-band-typical readings, not to zero. (Phase-117's
  record adds a sharper caution: under spec 016's geometry,
  judged kur signs' W3 p-values (median 0.645) nearly
  coincided with the core's (median 0.627) — the phoneme-pair
  fabric is coarse evidence, and this battery's W3 legs are
  interpreted accordingly: a coherence floor and a median-
  donor criterion, not a fine discriminator.)
- **Strata:** W4 uses site only (no material field exists
  in Holdat); site is confounded with excavation/publication
  history. FAIL-capability is nearly confined to M293
  among the 44 (§4.4).
- **Assumptions declared:** reading order = corpus sequence
  order; the Phase-69 I/M/T convention; the §3 syllable
  canon as the operative phonotactic frame (used only via
  the tokenizer's phoneme segmentation); STRICT94 as a
  valid reference core (established by the Phase-108/109
  provenance audit, not by this phase).

## 11. Execution order (frozen; covered by the owner's single commission of 2026-10-07)

1. This spec committed alone (design pre-registration), on
   the stacked branch; Appendix A finalized in the
   following commit (§13).
2. Implementation — `backend/glossa_lab/phase118_battery.py`
   (pure machinery: W1 carried from Phase-117, W3 cross-fit,
   W4 carried, decision rule),
   `backend/glossa_lab/phase118_run.py` (orchestration +
   report writing), runner
   `backend/scripts/phase118_within_battery.py`; unit tests
   `backend/tests/test_phase118_battery.py` (including toy
   end-to-end controls: a synthetic core-coherent reading
   validates; a synthetic incoherent reading does not).
3. H23 gate, in order: script written → graph module
   `backend/glossa_lab/experiment_graph_phase118.py` (node
   `IndusPhase118WithinCompilationValidation`) → registration
   in `experiment_graph.py` → registration asserted in
   `ATOMIC_NODES` → only then any run. Partition totals and
   judgeability counts asserted (§§3, 2.1) before calibration.
4. Calibration (§6): φ_{A→B}, φ_{B→A} computed; STRICT94
   (leave-one-out models throughout) and KUR113 evaluated;
   gates checked — positive over J94, negative over JKUR
   with its discrimination tallies. If rejected: write
   reports + ledgers, stop (no step 5).
5. Main run on FLAGGED44; apply §8; write reports + change
   register; update the anchors file (changed entries ==
   change-register signs, asserted).
6. Full backend suite + foundation check (H21: anchors file
   and phase reports change). Ruff clean before push.
7. Ledger entries (root `LEDGER.md` and
   `glossa-indus/LEDGER.md`, AI disclosure) and one PR —
   stacked, base `phase/117-within-compilation-battery`,
   retargeting to main when PR #75 merges. No merge without
   the owner's explicit say-so.

## 12. Deviations

Any deviation from this spec discovered during the execution
is recorded in the summary and the ledger, not absorbed.
Thresholds, floors, bands, the partition, the seeds, and the
decision rule are not adjustable after the freeze commit; a
substantive design error voids the design and requires a new
spec (Phase-111/112 precedent).

## 13. Deliverables (frozen)

- `specs/017-phase118-within-compilation-validation-v2/{spec,plan,tasks}.md`
  (spec freeze commit, then Appendix A finalized in the
  following commit)
- `backend/glossa_lab/phase118_battery.py`,
  `backend/glossa_lab/phase118_run.py`,
  `backend/glossa_lab/experiment_graph_phase118.py`
  (+ registration in `experiment_graph.py`)
- `backend/scripts/phase118_within_battery.py`
- `backend/tests/test_phase118_battery.py`
- `reports/phase118_within_battery_results.json` (sets,
  partition assertion, judgeability assertions, φ per
  direction, calibration incl. JKUR discrimination tallies,
  per-anchor instrument states + statistics, outcomes)
- `reports/phase118_within_battery_change_register.json`
  (iff the main run executes)
- `reports/phase118_within_battery_summary.md`
- Anchors-file changes per §8 (iff calibration passes)
- Ledger entries in `LEDGER.md` and `glossa-indus/LEDGER.md`
  (AI disclosure); suite + foundation results recorded in
  the summary
- One stacked PR; no merge without the owner's explicit
  say-so

## Appendix A — Design-stage feasibility (instrument statistics only)

*Finalized in the commit following the freeze; the
floor-choice table (A.1) and the set-level counts the frozen
text cites are part of the freeze commit, and the per-anchor
tables (A.2) are finalized in the following commit. Preamble
and boundary: every number in this appendix is an attestation
count or a judgeability determination under the frozen
definitions of §§2–5, computed from the Holdat corpus and the
anchors file at design stage. No instrument scored any sign;
no profile was compared to any model; no verdict exists in
this appendix. Per-anchor rows are counts, not results.*

### A.1 The per-direction junction floor (W3 cross-fit scorability by floor)

Per-direction junction counts split each sign's spec-016
junction total across the two partition halves, so the
floor choice trades directly against the negative control's
existence. Counts below are both-directions W3-scorable
signs (§2.1, donor band included — every candidate sign's
band is non-empty at these attestation levels; pool sizes
are ~195–205 for the rare-sign cohorts):

| Per-direction floor | STRICT94 W3-scorable | J94 (W1 ∧ W3) | KUR113 W3-scorable (JKUR) | FLAGGED44 W3-scorable |
|---|---|---|---|---|
| 2 (frozen) | **80 / 94** | **67** | **29** | **34 / 44** |
| 3 | 69 / 94 | 64 | 4 | 23 / 44 |
| 4 | 59 / 94 | 58 | 1 | 11 / 44 |

Floor 2 is frozen: it is the largest floor at which all
three sets remain testable — floor 3 leaves a 4-sign
negative control (a gate over 4 signs is not a control) and
floor 4 a 1-sign one. Spec 016 rejected its own floor 8 on
the same principle ("floor 8 would silence the negative
control"). At floor 2: W1-scorable 68/94 STRICT94, 13/44
flagged, 0/113 kur; W4-judgeable 57/94, 9/44, 0/113
(identical to spec 016 Appendix A — same corpus, same
definitions); flagged judgeable-by-any-instrument **37/44**;
flagged W1 ∧ W3 (the §8 validation cap) **11/44**.
Per-direction φ self-score set sizes at floor 2:
|S_{A→B}| = 83 (core signs scorable scoring on B),
|S_{B→A}| = 89 (scoring on A).

### A.2 Per-anchor attestation tables (finalized in the following commit)

FLAGGED44 rows (nH; half token counts; per-direction
junction counts; W1/W3/W4 scorability) and the JKUR 29-sign
list, computed under the frozen definitions.
