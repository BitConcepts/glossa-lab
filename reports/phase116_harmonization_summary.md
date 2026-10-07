# Phase-116 — Corpus-Harmonization Study: Why Holdat and ICIT Positional Profiles Disagree

**Spec:** specs/015-phase116-corpus-harmonization (frozen before any results) · **Date:** 2026-10-07 · **GPU device:** cpu (torch absent)

**Diagnostic only.** No anchor was changed, no validation verdict was issued; all 44 anchors remain `pending_non_sa_validation`.

## Baseline (recomputed; asserted against the Phase-115 record)

T1 v2 over STRICT94: judged 51 (8 PASS / 43 FAIL), 40 modal-disagreement failures, median TV over failures 0.789474, mean TV over judged 0.657011, full-layer modal agreement A_full = 0.2157.

## Matcher yield (spec section 4)

Tier A (direct, mutually unique): **13** pairs. Tier B (reversed): **17**. Tier C (containment): **1**. Ambiguous-orientation candidate pairs: 0 (excluded from A/B). Raw compatible pairs before uniqueness: 135 direct / 240 reversed.

## Verdicts (frozen rules, spec section 5)

| Hypothesis | Verdict | Headline numbers |
|---|---|---|
| H-COMPOSITION | **UNRESOLVED** | restricted: A 1.0 / TV 0.0 on 3 paired signs vs full-layer A 0.6667 / TV 0.33 (powered: False) |
| H-SEGMENTATION | **UNRESOLVED** | S1 sentinel-strip: FAIL 43 → 45 (REFUTED); S2 artifact-units: TV 0.1042 vs row-units 0.0917 (UNRESOLVED) |
| H-MAPPING | **REFUTED** | top-10 TV share 0.2956; chain-heavy minus clean mean TV Δ = 0.0598 (groups ok: False) |
| H-DIRECTION | **UNRESOLVED** | D1 reversed share 0.5667 (UNRESOLVED); D2 flip: A 0.3137 vs 0.2157 (UNRESOLVED) |
| H-DEFINITION | **REFUTED** | median W1 0.451927; material-displacement share 0.6863; 5-bin agreement 0.1373; Spearman ρ -0.0826 |

Permutation context (BH q = 0.05, token-level): 43 of 51 judged signs disagree beyond sampling noise on the full layers; 0 of 3 on the matched restriction.

## Harmonization recommendation (assembled mechanically, spec section 6)

- R-NONE: No harmonization transformation is justified by this study. Cross-corpus positional validation between Holdat and the ICIT converted layer is not viable on this pair of compilations under any convention alignment tested. A future validation battery must not use a conjunctive cross-corpus positional gate on this pair; validation must proceed within a single compilation or await a genuinely independent corpus.

## What a future validation battery may / may not assume

- MAY NOT assume the anchors' validation status changed: this study is diagnostic only and all 44 anchors remain pending_non_sa_validation.
- MAY NOT assume the disagreement is crosswalk error: it is not concentrated in crosswalk-risky signs.
- MAY NOT assume the disagreement is a binning artifact: genuine positional displacement survives continuous relative-position measurement.
- UNRESOLVED (no assumption licensed either way): segmentation, composition, direction.

## Limitations

Registered in spec section 8: identity is textual, not artifactual; sentinel wildcard asymmetry (15.0% of kept positions); token-level permutation ignores inscription clustering; site-mix matching is string-normalized only; `dir.` label semantics never assumed. Full per-sign records, the matcher tier decomposition, and the section 5.3 crosswalk audit table are in `phase116_harmonization_results.json`.

## Verification

Recorded in the phase ledger entries and the PR body (full backend suite; foundation check per H21 — anchors untouched, reports added). Conversion audit: every population token (16141) recomputed from its stored source code matches the keyed layer.

**AI disclosure:** executed by an AI agent (Muse Spark, via Muse) at the direction of Tristen Pierson, per constitution section VI.
