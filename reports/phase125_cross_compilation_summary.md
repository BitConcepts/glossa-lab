# Phase-125 — Cross-Compilation Positional Comparison (mayig/CISI vs Holdat)

**Spec:** specs/019-phase125-cross-compilation-positional (frozen before any results) · **Date:** 2026-10-08 · **GPU device:** cpu (torch absent)

Per-sign positional profiles (initial/medial/terminal rates) computed
**within** the mayig/CISI compilation and **within** the Holdat
compilation separately — inscriptions never pooled — and joined only
through the Phase-122 Parpola-Mahadevan crosswalk v1. The PRIMARY arm
is the high-confidence, unambiguous pair set (372 high pairs, 286
after the uniqueness rule); floor 8 tokens per sign per compilation;
the verdict is the PRIMARY arm's frozen spec-section-6 pattern only.

## Verdict

**FAIL — DISAGREEMENT** (section-6.3 falsifier pattern met). Primary arm:
16 judgeable pairs of 286;
median TV 0.636931 (PASS bound <= 0.35; FAIL bound
>= 0.50); Spearman rho initial -0.424758,
terminal 0.316034 (PASS bound >= 0.50);
pairing-shuffle null (B = 999, seed 125125) p_null
0.824000 (PASS requires <= 0.05; FAIL requires
> 0.05 together with median TV >= 0.50), null median-of-medians
0.556145.

## Arms (each computed and reported separately; never pooled)

| Arm | Pairs | Judgeable | Below floor | Median TV | Median W1 | rho initial | rho terminal | rho medial | Modal agree | p_null | Pattern |
|---|---|---|---|---|---|---|---|---|---|---|---|
| primary | 286 | 16 | 270 | 0.636931 | 0.658181 | -0.424758 | 0.316034 | -0.476874 | 0.187500 | 0.824000 | FAIL / DISAGREEMENT |
| sensitivity_a_medium_included | 286 | 16 | 270 | 0.636931 | 0.658181 | -0.424758 | 0.316034 | -0.476874 | 0.187500 | 0.824000 | FAIL / DISAGREEMENT |
| sensitivity_b_all_pairs | 762 | 28 | 734 | 0.636931 | 0.726396 | -0.245008 | 0.291861 | -0.244588 | 0.250000 | 0.737000 | FAIL / DISAGREEMENT |

Sensitivity notes: arm A (medium-included) — crosswalk v1 contains
zero medium pairs, so arm A's pair set coincides with the PRIMARY
arm's (judgeable 16 of 286;
pattern FAIL / DISAGREEMENT); this coincidence
is a registered design fact (spec section 3), and arm A is not an
independent sensitivity check. Arm B (all 762 pairs, judged
pair-by-pair, ambiguity included) — judgeable 28
pairs; pattern FAIL / DISAGREEMENT; arm B does
not change the verdict. The 4 unmapped P signs
(P000, P225, P261, P358)
have no pair in any arm and are counted non-judgeable.

## Primary judgeable pairs

| Pair (P-M) | mayig n | Holdat n | mayig profile (I/M/T) | Holdat profile (I/M/T) | TV | W1 |
|---|---|---|---|---|---|---|
| P011-M017 | 10 | 18 | 0.0000/0.5000/0.5000 | 1.0000/0.0000/0.0000 | 1.000000 | 1.500000 |
| P013-M001 | 9 | 14 | 1.0000/0.0000/0.0000 | 1.0000/0.0000/0.0000 | 0.000000 | 0.000000 |
| P050-M059 | 32 | 222 | 0.0312/0.9688/0.0000 | 0.1937/0.4685/0.3378 | 0.500282 | 0.500282 |
| P056-M070 | 9 | 17 | 0.0000/1.0000/0.0000 | 1.0000/0.0000/0.0000 | 1.000000 | 1.000000 |
| P058-M072 | 15 | 12 | 0.0000/0.9333/0.0667 | 1.0000/0.0000/0.0000 | 1.000000 | 1.066667 |
| P060-M065 | 20 | 154 | 0.0000/0.9500/0.0500 | 0.2338/0.2208/0.5455 | 0.729221 | 0.729221 |
| P062-M067 | 21 | 15 | 0.0000/1.0000/0.0000 | 1.0000/0.0000/0.0000 | 1.000000 | 1.000000 |
| P073-M051 | 8 | 163 | 0.0000/0.8750/0.1250 | 0.2025/0.2822/0.5153 | 0.592791 | 0.592791 |
| P145-M087 | 27 | 130 | 0.0000/0.8519/0.1481 | 0.1077/0.4077/0.4846 | 0.444160 | 0.444160 |
| P147-M089 | 14 | 171 | 0.0714/0.8571/0.0714 | 0.0994/0.4620/0.4386 | 0.395155 | 0.395155 |
| P194-M048 | 8 | 157 | 0.0000/0.8750/0.1250 | 0.1975/0.3439/0.4586 | 0.531051 | 0.531051 |
| P217-M211 | 18 | 249 | 0.7778/0.1111/0.1111 | 0.0482/0.6827/0.2691 | 0.729585 | 0.887550 |
| P316-M336 | 19 | 161 | 0.0526/0.8421/0.1053 | 0.0807/0.4472/0.4721 | 0.394900 | 0.394900 |
| P324-M342 | 99 | 584 | 0.7778/0.2121/0.0101 | 0.0205/0.8596/0.1199 | 0.757230 | 0.866992 |
| P378-M391 | 17 | 193 | 0.1176/0.2941/0.5882 | 0.1140/0.5751/0.3109 | 0.281012 | 0.281012 |
| P385-M267 | 35 | 400 | 0.0000/0.1714/0.8286 | 0.0425/0.8100/0.1475 | 0.681071 | 0.723571 |

## Inputs and guards

- mayig layer: 179
  inscriptions / 1003 tokens /
  182 distinct P signs,
  179 CISI objects.
- Holdat: 1670 inscriptions /
  7002 tokens /
  390 distinct M signs.
- Object join: **none performed** (spec section 2.1: Holdat's
  cisi_number is internal sequential numbering — contiguous 1..N per
  site — not a CISI object ID; the zero-padded coincidence with mayig
  CISI IDs is not an identity join and was not used).
- Anchors file unchanged: sha256 eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86ebb1fa3b602cfaed
  before and after (asserted in code).

## Claim scope (spec section 7)

A PASS supports exactly: for the judgeable high-confidence
unambiguous crosswalk pairs, the two compilations' within-compilation
positional profiles agree at the frozen thresholds, beyond
shuffled-pairing chance. A FAIL supports exactly: crosswalk-joined
positional agreement is refuted at the frozen thresholds on the
judgeable primary pairs — the pairing carries no positional agreement
beyond shuffled pairings at median TV >= 0.50; it does not identify
which side produces the disagreement. Neither outcome says anything
about any individual sign's identity or reading, about below-floor /
ambiguous / low-confidence pairs, or about Holdat vs the ICIT lineage
(Phase-116 R-NONE stands untouched). Population caveat: the mayig
layer (179 inscriptions) and Holdat (1,670 inscriptions) cover
substantially the same artefact population but not the same
inscription set, so disagreement can arise from population mix as
well as transcription; the verdict is a statement about the
well-attested minority of pairs (16 judgeable
of 286 primary pairs), never about the script as a
whole. No PRED verdict is issued and no
anchor status changes under this phase.

## Deviations

None in the frozen definitions, thresholds, floor, arms, null, or
verdict rule. The object-join discipline of spec section 2.1 is
implemented as specified: because no legitimate CISI object-ID join
between Holdat and mayig exists, no object-matched arm is run; the
comparison is sign-level over full within-compilation profiles, as
registered in the frozen spec.

## Verification

Full backend suite: 866 passed / 13 skipped / 0 failed (main
baseline 854 passed / 12 skipped, plus this phase's 12 new tests —
12 passed in isolation, 0 skipped; the one additional suite-level
skip is in the pre-existing suite, not in Phase-125 tests).
Foundation check (H21): 40 passed / 0 failed / 8 warnings
(baseline unchanged). Ruff clean on all new/changed files.
Test side effects (glossa-indus/ claims, outputs/) reverted
before commit, per precedent.

**AI disclosure:** executed by an AI agent (Muse Spark, via
Muse) at the direction of Tristen Pierson, per constitution
section VI.
