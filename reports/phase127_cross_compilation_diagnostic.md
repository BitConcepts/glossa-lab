# Phase-127 — Cross-Compilation Disagreement Diagnostic (spec 021)

**The Phase-125 verdict is FAIL — DISAGREEMENT, and it is FINAL.**
**This diagnostic does not re-score Phase-125, does not issue any
verdict, and no finding below softens, qualifies, or re-opens that
verdict.** Phase-125 (spec 019, PRIMARY arm): 16 judgeable pairs of
286; median TV 0.636931; Spearman ρ initial −0.424758 / terminal
0.316034; pairing-shuffle null p = 0.824. What follows decomposes
the *observed distances* of that finished result — how much of
them sampling noise, crosswalk ambiguity, and population
composition can account for, at the observed sizes — under the
estimators frozen in spec 021 before any diagnostic statistic
existed. **Spec:** specs/021-phase127-cross-compilation-diagnostic · **Date:** 2026-10-08 · **GPU device:** cpu (torch absent)

## Headline decomposition

| Component | Figure | Reading |
|---|---|---|
| Observed median TV (Phase-125, of record) | 0.636931 | the quantity being decomposed |
| (a) Split-half noise floor, raw (median of per-sign medians) | 0.059538 | TV between two halves of the *same* Holdat sign pool |
| (a) Split-half noise floor, full-size estimate (÷ √2) | 0.042100 | within-Holdat sampling noise at full Holdat sizes |
| (b) Matched-size expected median TV (Holdat at mayig sizes) | 0.082613 (95% interval 0.046665–0.131316) | pure Holdat-internal sampling, at the token counts mayig actually has |
| (b) Share of matched-size replicates with median TV ≥ observed | 0.000000 | how often sampling alone reaches the observed median |
| (c) Bootstrap CI for the median TV | 0.548638–0.722042 (bootstrap median 0.643877) | inscription-level resampling of *both* compilations |
| (d) Median ambiguity share per judgeable pair | 0.666667 | share of each pair's crosswalk neighbourhood that is not the primary pair (primary TVs themselves contain zero ambiguity by construction — §(d)) |
| (d) Median attributable TV (spec §6 estimator) | 0.000000 (share -0.185664) | primary TV minus neighbourhood median TV |
| (f) Power | tokens-per-sign required for the median-TV gate to clear the noise criterion (95th percentile of the replicate median TV ≤ 0.35): **8** (grid maximum 256; reached within the grid); per-sign criterion (pooled per-sign 95th percentile ≤ 0.35): **8** | derived from arm (b)'s machinery, spec §8 method |

## (a) Holdat split-half noise floor (spec §3; B = 999 per sign, seed 127001)

Per-sign medians and intervals are in the results JSON. The
split-half statistic compares two halves (≈ n/2 tokens each) of a
single Holdat sign pool, so it prices a comparison at half size;
the full-size estimate divides by √2 (registered multinomial
scaling approximation). Token-level caveat (spec A3): tokens
within an inscription are not independent, so token-level nulls
understate clustered noise; arm (c) is the cluster-respecting
statement.

## (b) Matched-size subsampling null (spec §4; B = 999, seed 127002)

For each pair, Holdat tokens are subsampled without replacement
to exactly the mayig token count for that sign; the primary
statistic is TV(subsample, disjoint remainder). Expected median
TV under pure Holdat-internal sampling at mayig's sizes:
**0.082613**, vs the observed cross-compilation
median 0.636931; sampling alone reached or exceeded the observed
median in a share 0.000000 of
replicates. Registered limitation: this arm prices Holdat-side
noise only; mayig-side noise is priced by arm (c). The arms are
reported together and never averaged.

## (c) Inscription bootstrap CIs (spec §5; B = 999, seed 127003)

Inscriptions of each compilation were resampled with
replacement, independently (179 mayig / 1,670 Holdat per
replicate), profiles recomputed within each resampled
compilation, and the fixed 16-pair set re-evaluated. Per-pair
CIs are in the results JSON. The median-TV bootstrap CI is
**0.548638–0.722042**.
Pairs excluded from a replicate only when a resampled sign had
0 tokens; exclusion counts are recorded per pair in the JSON.

## (d) Crosswalk arm decomposition (spec §6)

The Phase-125 PRIMARY arm admits only pairs unambiguous within
the high-confidence set, so **ambiguous mappings contribute
exactly zero to the primary TVs by construction**; this arm
prices the counterfactual — the same signs under the ambiguous
mappings the primary arm excluded. Estimator (frozen in spec
§6): attributable TV = TV_primary − median TV of the pair's
judgeable neighbourhood comparisons; a positive value means the
primary mapping disagrees *more* than the ambiguous
alternatives typically do (ambiguity is not what produces that
pair's disagreement, under this estimator); a negative value
means the alternatives disagree more. Pairs with no judgeable
neighbourhood comparison: 9.

| Pair | Neighbourhood | Ambiguity share | TV primary | Neighbourhood median TV | Attributable TV | Attributable share |
|---|---|---|---|---|---|---|
| P011-M017 | 3 | 0.666667 | 1.000000 | 1.000000 | 0.000000 | 0.000000 |
| P013-M001 | 3 | 0.666667 | 0.000000 | 0.000000 | 0.000000 | null |
| P050-M059 | 3 | 0.666667 | 0.500282 | 0.968750 | -0.468468 | -0.936410 |
| P056-M070 | 3 | 0.666667 | 1.000000 | 1.000000 | 0.000000 | 0.000000 |
| P058-M072 | 3 | 0.666667 | 1.000000 | 1.000000 | 0.000000 | 0.000000 |
| P060-M065 | 3 | 0.666667 | 0.729221 | 1.000000 | -0.270779 | -0.371327 |
| P062-M067 | 2 | 0.500000 | 1.000000 | null | null | null |
| P073-M051 | 3 | 0.666667 | 0.592791 | 1.000000 | -0.407209 | -0.686934 |
| P145-M087 | 3 | 0.666667 | 0.444160 | null | null | null |
| P147-M089 | 3 | 0.666667 | 0.395155 | null | null | null |
| P194-M048 | 3 | 0.666667 | 0.531051 | null | null | null |
| P217-M211 | 2 | 0.500000 | 0.729585 | null | null | null |
| P316-M336 | 3 | 0.666667 | 0.394900 | null | null | null |
| P324-M342 | 3 | 0.666667 | 0.757230 | null | null | null |
| P378-M391 | 3 | 0.666667 | 0.281012 | null | null | null |
| P385-M267 | 3 | 0.666667 | 0.681071 | null | null | null |

## (e) Composition controls (spec §7)

Holdat-side restrictions only — the mayig side (all 179
inscriptions Mohenjo-daro, all unicorn seals) is already
entirely inside every stratum. The frozen floor 8 is re-applied
to the restricted Holdat counts; medians are over each
control's own judgeable set. Phase-125 median of record:
0.636931 over 16 judgeable.

| Control | Holdat inscriptions | Judgeable | Median TV |
|---|---|---|---|
| site_mohenjo_daro | 606 | 13 | 0.599138 |
| iconography_unicorn | 514 | 13 | 0.650510 |
| site_and_iconography | 190 | 11 | 0.602896 |

Stratum-inconsistent inscriptions (rows disagreeing on the
stratum value; counted and excluded from the affected control,
never silently assigned): site 0,
iconography 0.

**Gaps (stated, not improvised):**

- mayig unicorn variants (I–V) have no counterpart granularity
  in Holdat's iconography column (single 'unicorn' value):
  variant-level composition cannot be controlled.
- The mayig layer has no non-Mohenjo-daro site, no non-seal
  object type, and no non-unicorn iconography: no mayig-side
  stratum restriction is possible, and no stratum beyond site
  and iconography exists on both sides.
- Provenience finer than site, artefact material, and find
  context are absent from the mayig layer metadata and cannot
  be controlled.
- Inscription-length composition is token data, not layer
  metadata; it is outside this arm's registered scope and is
  not controlled.

## (f) Power statement (spec §8; B = 499 per grid point, seed 127004)

tokens-per-sign required for the median-TV gate to clear the noise criterion (95th percentile of the replicate median TV ≤ 0.35): **8** (grid maximum 256; reached within the grid); per-sign criterion (pooled per-sign 95th percentile ≤ 0.35): **8**. Method: for each grid size, TV(subsample,
disjoint remainder) over the judgeable Holdat pools — pure
sampling noise at that size; the criterion is the size at
which that noise's 95th percentile falls to the frozen
Phase-125 PASS bound 0.35. The full grid is in the results
JSON. This statement is about the gates' informativeness at
the observed effect scale; it re-opens no gate and re-judges
no pair. Grid-shape note: the pooled per-sign 95th
percentile is not monotone at the largest grid points
(128–256), where few signs contribute (pools no larger than
the grid size are excluded) and the disjoint remainder —
the comparison reference — becomes small, so remainder-side
noise dominates; the registered criterion is the *smallest*
qualifying grid size, which is reached at the grid's first
point on both criteria, so the tail shape does not affect
the statement.

## Claim scope (spec §9)

Every figure above is a statement about the 16 judgeable
primary pairs and the frozen Phase-125 design — never about
the script as a whole, any individual pair's crosswalk
correctness, any below-floor or ambiguous pair's identity, or
Holdat vs the ICIT lineage (Phase-116 R-NONE stands
untouched). "Genuine" in this report's vocabulary means
exactly: not accounted for by the §§3–5 sampling nulls, the
§6 mapping-choice estimator, or the §7 controls, at the
observed sizes; it does not attribute the residual to any
side or mechanism. **The Phase-125 verdict — FAIL —
DISAGREEMENT — is unchanged by anything in this report.**

## Inputs and guards

- mayig layer: 179 inscriptions / 1,003 tokens / 182 P signs;
  Holdat: 1,670 inscriptions / 7,002 tokens / 390 M signs;
  crosswalk v1: 762 pairs (high 372 / medium 0 / low 390) —
  all asserted in code against the frozen totals.
- No object-level join was performed; no inscriptions were
  pooled across compilations; Phase-125 artifacts were read,
  never modified.
- Anchors file unchanged: sha256 eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86ebb1fa3b602cfaed
  before and after (asserted in code).

## Deviations

None in the frozen arms, estimators, seeds, replicate counts,
grids, or interval methods. One filename deviation, recorded
per spec §11: the graph module is
`backend/glossa_lab/experiment_graph_phase127_diagnostic.py`
(not `experiment_graph_phase127.py` as listed in spec §10.4),
because that filename is already taken by a legacy
experiment-graph node family (Gulf corpus / Roif mining /
fish site polysemy) that predates the ledger-sequence
numbering — the Phase-126 Wells precedent
(`experiment_graph_phase126_wells.py`). The registered node
id is exactly as specified:
`IndusPhase127CrossCompilationDiagnostic`. (Verification
counts are recorded in the ledger entries for this phase.)

**AI disclosure:** executed by an AI agent (Muse Spark, via
Muse) at the direction of Tristen Pierson, per constitution
section VI.
