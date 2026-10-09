# Phase-131 — Source-of-Disagreement Attribution (spec 022)

**This study is attribution diagnostics ONLY. It does not
re-score Phase-125 and it issues no verdict.** **The Phase-125
verdict is FAIL — DISAGREEMENT, and it is FINAL** (spec 019,
PRIMARY arm: 16 judgeable pairs of 286; median TV 0.636931;
Spearman ρ initial −0.424758 / terminal 0.316034; shuffle null
p = 0.824). **Spec 020's adjudication outcome — NO — stands
untouched.** No finding below softens, qualifies, conditions,
or re-opens either outcome; no anchor, PRED verdict, or status
was changed by this phase. What follows attributes the
*observed disagreement* of that finished result to mechanisms —
segmentation, substitution, insertion/deletion, reading
direction, composition — under the estimators frozen in spec
022 before any Phase-131 statistic existed, and states the
residual unexplained share plainly. **Spec:** specs/022-phase131-attribution ·
**Date:** 2026-10-09 · **GPU device:** cpu (torch absent)

## Arm A — Matched-object alignment (spec §3)

### Join stages — all counted, as found

| Stage | Result |
|---|---|
| mayig objects / Holdat inscriptions | 179 / 1670 |
| S1 CISI-ID join: apparent zero-padded namesakes | 179 apparent / **0 validated** — REJECTED as non-identity: Holdat `cisi_number` is internal sequential numbering, not a CISI object ID (spec 019 §2.1). No S1 join was performed. |
| S2 catalogue cross-reference (Holdat key → CISI ID) | 0 usable cross-references found in the committed inputs |
| S3 shared artifact keys | 0 shared keys |
| S4 content matcher (§3.2): eligible mayig inscriptions | 32 / 179 (every token mapped by the 286-pair primary crosswalk map; primary-map token coverage over all mayig tokens 0.725823) |
| S4 matched pairs | **4** (tiers: {'NEAR': 1, 'NEAR-REV': 3}; ambiguous-orientation excluded: 0) |
| Matched coverage | mayig 0.022346 · Holdat 0.002395 |

Identity here is **textual, not artifactual** (spec A3): a
matched pair shows the same sign text occurs in both
compilations under the primary crosswalk map, within the
frozen matcher tolerance. The small matched set is a finding,
reported as found (spec A6): under the only legitimate join,
the two compilations' texts essentially do not coincide —
consistent with, and sharper than, Phase-125's profile-level
disagreement, and not a defect to paper over by loosening the
matcher.

### Difference classification (§3.3)

Pair-class counts over the matched set: {'insertion-deletion': 2, 'substitution': 2}.
Difference-block counts by class: {'insertion-deletion': 2, 'substitution': 2}.
Block token totals: {'substitution': 4, 'all_difference_blocks': 6, 'insertion-deletion': 2}.

Concrete examples per non-identical pair class (all pairs of a
class if fewer than 3 exist):

- **substitution** — mayig M-124 vs Holdat M-0357 (tier NEAR): mapped mayig `M342 M296 M059 M087` vs Holdat `M342 M410 M059 M087`; blocks: substitution (a: M296 → b: M410)
- **substitution** — mayig M-148 vs Holdat C-0001 (tier NEAR-REV): mapped mayig `M342 M267 M221` vs Holdat `M391 M267 M342` (aligned reversed: `M342 M267 M391`); blocks: substitution (a: M221 → b: M391)
- **insertion-deletion** — mayig M-37 vs Holdat M-0512 (tier NEAR-REV): mapped mayig `M211 M059 M171` vs Holdat `M059 M211` (aligned reversed: `M211 M059`); blocks: insertion-deletion (a: M171 → b: ∅)
- **insertion-deletion** — mayig M-87 vs Holdat H-0262 (tier NEAR-REV): mapped mayig `M176 M304 M041` vs Holdat `M041 M176` (aligned reversed: `M176 M041`); blocks: insertion-deletion (a: M304 → b: ∅)

### Matched-object positional TV (§3.4)

Matched-object median TV: **NOT ESTIMABLE**
(defined per-pair TVs: 5 of the 16 judgeable
pairs; unthresholded median over defined pairs:
0.500000; gate: requires MATCHED >= 10 pairs AND >= 4 of the 16 judgeable pairs with defined matched TVs (spec 3.4)).
Per-pair records are in the results JSON.

## Arm B — Reading direction (spec §4)

**Attribution diagnostics, not a re-score of Phase-125.** No
Phase-125 gate is applied to any number in this section; the
Phase-125 FAIL verdict stands untouched. Criterion (frozen):
an arm supports direction as a mechanism iff its median TV ≤
0.131316 — the upper bound of the Phase-127 matched-size noise
band (median 0.082613, 95% interval [0.046665, 0.131316]).

| Arm | Median TV | Reduction vs 0.636931 | Supports direction? |
|---|---|---|---|
| B1 mayig reversed | 0.582205 | 0.054726 | False |
| B2 Holdat reversed | 0.582205 | 0.054726 | False |

Note, as found and as the algebra requires: B1 and B2 coincide
exactly, per pair and therefore in the median. Reversal swaps
the INITIAL and TERMINAL shares of one side's profiles, and TV
is symmetric in that swap — TV(p with I/T swapped, q) equals
TV(p, q with I/T swapped) — so the two arms cannot differ under
the Phase-125 statistic. Either way the answer is the same:
reversing one compilation's orientation reduces the median TV
only slightly, from 0.636931 to the value above, nowhere near
the noise band. Reading direction is **not** a supported
mechanism for the observed disagreement under the frozen
criterion.

## Arm C — Stratification + composition adjustment (spec §5)

A stratum's median TV is estimable iff ≥ 4 pairs are judgeable
within the stratum under floor 8 re-applied on both sides;
otherwise the row is marked NOT ESTIMABLE with its counts.
Stratum-inconsistent Holdat inscriptions (counted, excluded
from the affected stratum): site
0, iconography
0.

### Site

| Stratum | mayig inscr. | Holdat inscr. | Judgeable | Median TV | Status |
|---|---|---|---|---|---|
| Mohenjo-daro | 179 | 606 | 13 | 0.599138 | ESTIMABLE |
| Banawali | 0 | 60 | 0 | null | NOT ESTIMABLE |
| Chanhu-daro | 0 | 78 | 0 | null | NOT ESTIMABLE |
| Dholavira | 0 | 106 | 0 | null | NOT ESTIMABLE |
| Harappa | 0 | 492 | 0 | null | NOT ESTIMABLE |
| Kalibangan | 0 | 110 | 0 | null | NOT ESTIMABLE |
| Lothal | 0 | 124 | 0 | null | NOT ESTIMABLE |
| Rakhigarhi | 0 | 33 | 0 | null | NOT ESTIMABLE |
| Surkotada | 0 | 61 | 0 | null | NOT ESTIMABLE |

### Object type (mayig unicorn variants vs Holdat unicorn; other Holdat iconographies are mayig-empty)

| Stratum | mayig inscr. | Holdat inscr. | Judgeable | Median TV | Status |
|---|---|---|---|---|---|
| unicorn I | 9 | 514 | 0 | null | NOT ESTIMABLE |
| unicorn II | 19 | 514 | 1 | null | NOT ESTIMABLE |
| unicorn III | 45 | 514 | 5 | 0.663366 | ESTIMABLE |
| unicorn IV | 96 | 514 | 6 | 0.628981 | ESTIMABLE |
| unicorn V | 10 | 514 | 0 | null | NOT ESTIMABLE |
| holdat_only:buffalo | 0 | 72 | 0 | null | NOT ESTIMABLE |
| holdat_only:elephant | 0 | 200 | 0 | null | NOT ESTIMABLE |
| holdat_only:geometric | 0 | 93 | 0 | null | NOT ESTIMABLE |
| holdat_only:gharial | 0 | 64 | 0 | null | NOT ESTIMABLE |
| holdat_only:rhinoceros | 0 | 170 | 0 | null | NOT ESTIMABLE |
| holdat_only:script only | 0 | 138 | 0 | null | NOT ESTIMABLE |
| holdat_only:tiger | 0 | 72 | 0 | null | NOT ESTIMABLE |
| holdat_only:zebu bull | 0 | 347 | 0 | null | NOT ESTIMABLE |

### Text length

| Bin | mayig inscr. | Holdat inscr. | Judgeable | Median TV | Status |
|---|---|---|---|---|---|
| 1 | 1 | 0 | 0 | null | NOT ESTIMABLE |
| 2-3 | 34 | 599 | 1 | null | NOT ESTIMABLE |
| 4-5 | 55 | 745 | 2 | null | NOT ESTIMABLE |
| 6+ | 89 | 326 | 9 | 0.512903 | ESTIMABLE |

### Period

**NOT ESTIMABLE in every cell.** Neither the mayig layer
metadata nor the Holdat CSV carries a period / dating field;
no period stratum is improvised from a proxy.

### Composition adjustment (§5.2)

Holdat per-sign profiles reweighted to the mayig text-length
composition (mayig bin weights:
{'1': 0.005587, '2-3': 0.189944, '4-5': 0.307263, '6+': 0.497207}).
Adjusted median TV: **0.597874**
(ESTIMABLE; pairs included:
16 of 16), vs the
unadjusted Phase-125 median of record 0.636931. Site adjustment
is the Mohenjo-daro stratum itself (mayig is entirely
Mohenjo-daro) and is not double-counted here.

## Arm D — Synthesis: the attribution table (spec §6)

| Mechanism | Supported share | Status | Basis |
|---|---|---|---|
| segmentation | null | NOT ESTIMABLE | Arm A difference-block tokens over the MATCHED set |
| substitution | null | NOT ESTIMABLE | Arm A difference-block tokens over the MATCHED set |
| insertion_deletion | null | NOT ESTIMABLE | Arm A difference-block tokens over the MATCHED set |
| order_direction | 0.000000 | ESTIMABLE | Arm B median-TV scale vs Phase-125 observed median TV |
| composition | 0.061321 | ESTIMABLE | Arm C length-composition-adjusted median TV |
| matched_object_residual | null | NOT ESTIMABLE | Arm A matched-object median TV (persistence measure, not an explained share) |

Sum of credited explained shares: 0.061321.
**Residual unexplained share: 0.938679** —
stated plainly: this is the share of the observed disagreement
that no arm's registered estimator accounts for.

Overlap caveat (binding): Order/direction and composition shares both act on the median-TV scale and may overlap; Arm A shares act on matched-pair token differences, a different denominator. Shares are not forced to sum to 100%; if credited shares exceed 1 the residual is 0 and the overlap is stated, never rescaled away.

The matched-object residual row is a *persistence* measure
(how much disagreement survives on matched objects), not an
explained share, and is excluded from the explained sum.

## Claim scope (spec §7)

Every figure above is a statement about the frozen inputs, the
16 judgeable primary pairs, and the Arm A matched set as
found — never about the script as a whole, any individual
pair's crosswalk correctness, or Holdat vs the ICIT lineage
(Phase-116 R-NONE stands untouched). The matcher-eligible
subset (32 of 179) is biased toward
inscriptions built from well-attested, unambiguously mapped
signs; Arm A findings describe that subset. **The Phase-125
verdict — FAIL — DISAGREEMENT — and spec 020's NO are
unchanged by anything in this report.**

## Inputs and guards

- mayig layer: 179 inscriptions / 1,003 tokens / 182 P signs;
  Holdat: 1,670 inscriptions / 7,002 tokens / 390 M signs;
  crosswalk v1: 762 pairs, primary map 286 pairs — all asserted
  in code against the frozen totals; the Phase-125 judgeable
  set and observed median TV (0.636931) and the Phase-127
  noise band ([0.046665, 0.131316]) were read from the results
  of record and asserted.
- Arm B's unreversed control evaluation reproduced the
  Phase-125 median TV of record exactly (0.636931) through
  this phase's own code path — a machinery check, not a
  re-score.
- No key join between Holdat and mayig was performed;
  inscriptions were never pooled across compilations;
  Phase-125/127 artifacts were read, never modified.
- Anchors file unchanged: sha256 eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86ebb1fa3b602cfaed
  before and after (asserted in code).

## Deviations

One implementation clarification, recorded per spec §9 (no
frozen quantity changes): spec §3.2's NEAR tier says "mutual
best"; the implementation reads a tie for best similarity on
either side as disqualifying the pairing (a tied best is not
*the* best), rather than picking the first tied candidate.
Threshold (0.60), tiers, eligibility, and gates are exactly as
frozen. One presentational note: spec Appendix A's design-stage
coverage figure (0.717) is the mean of per-inscription mapped
fractions; the run reports the token-weighted coverage
(0.725823) — same eligibility set (32/179), two averagings.
(Verification counts — suite and foundation — are recorded in
the ledger entries for this phase.)

**AI disclosure:** executed by an AI agent (Muse Spark, via
Muse) at the direction of Tristen Pierson, per constitution
section VI.
