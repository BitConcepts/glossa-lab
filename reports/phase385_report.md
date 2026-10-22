# Phase-385 — C1 Margin Completion for Phase-140 G1 (Spec 026)

**Rerun of:** Phase-140 (register row PHASE-140; SPEC-025 in
part). **Margin declared before any run:** Cramér's V = 0.10.
**Results:** `reports/phase385_results.json` (v2, governing).
**Chronology rider (mandatory): chronology is NOT controlled
in the primary test — period/phase remain uncontrolled
confounders of G1.** This rider applies to every statement
below.

## What the original said (verbatim)

Phase-140: G1 (site × sign repertoire on the ICIT-lineage
population, composition × preservation controlled) permutation
p = 0.0001 (0/9,999), descriptive V = 0.2190 → **SUPPORTED
under control (chronology NOT controlled)**. No interval for
the controlled effect was reported — the C1 gap this rerun
closes.

## v1 execution (preserved)

v1 (frozen digest 8af60b985d9994bc…) verified the population
(5,410 inscriptions, 7 sites) and observed χ² 4966.362228
exactly, then computed a stratified (composition ×
preservation) inscription bootstrap percentile CI of
**[0.2282, 0.2537]** — which excluded the point estimate
0.2190, because V's plug-in bias grows under resampling.
The v1 interval is superseded by v2 (same design; governing
interval corrected to the BASIC bootstrap; B = 4,999, seed
20261012; freeze digest 9b20117a9ef1789d…, frozen before
execution).

## v2 results

| Design | Percentile CI | Basic CI (governing) |
|---|---|---|
| G1 primary: composition × preservation strata | [0.2278, 0.2542] | **[0.1838, 0.2102]** |
| S-chron: composition × chron_band (EXPLORATORY) | [0.2282, 0.2532] | [0.1848, 0.2098] |
| S-depth: composition × depth_band (EXPLORATORY) | [0.2284, 0.2539] | [0.1841, 0.2096] |

Bootstrap median 0.2403 in all three designs (resampling bias
≈ +0.021, consistent across designs — the coherence of the
primary and exploratory intervals is itself a stability
signal).

## Verdict

**G1: SUPPORTED under control stands at the declared
margin** — the governing basic CI [0.184, 0.210] lies entirely
above the V = 0.10 practical floor, and the exploratory
chronology/depth-stratified intervals (labeled EXPLORATORY;
they are not the controlled primary) sit in the same range.
Chronology remains NOT controlled in the primary test. The
recorded permutation result (0/9,999) was not recomputed and
is unaltered. Phase-384's F3 margin completion on the same
marginal table returned a near-identical basic CI
[0.182, 0.210] under within-site resampling — independent
resampling schemes agree.

Foundation check after the phase: see the S4 ledger entry.
