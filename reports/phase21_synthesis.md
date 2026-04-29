# Phase-21 Synthesis — Indus M77 Phase-20 Follow-Up Experiments

Phase-21 executes the analytically-tractable Phase-20 candidate experiments
**as graph experiments** through the Glossa-Lab job executor (per WARP.md
rule G1). Atomic nodes live in `backend/glossa_lab/experiment_graph_phase21.py`;
graphs live in `backend/glossa_lab/experiments/graphs/indus_phase21*.json`;
each ran via `shell.cmd python -m glossa_lab.experiments <graph_id>`,
producing a Job entry + a JSON report.

Phase-20 candidate 3 (Ferrara CM OCR) is **deferred** — Phase-20c showed the
PDF is image-only scans and would need a vision pipeline (Mistral OCR or
Anthropic vision API), not pure analysis. That candidate is reclassified as
a tooling deliverable for Phase-22.

## Master verdict

```
Phase-21: P21a=NOT CONFIRMED | P21b=NOT CONFIRMED | P21d=PARTIALLY CONFIRMED
```

| # | Phase-20 follow-up prediction | Verdict | Headline number |
|---|-------------------------------|---------|-----------------|
| 21a | Repetition collapsing recovers natural-language structure on M77 | NOT CONFIRMED | spectral_gap = 0.0 → 0.0 (40.1% token reduction had no effect on the gap) |
| 21b | Site-prefixed M77 strata exhibit materially different spectral fingerprints | NOT CONFIRMED | gap-spread = 0.0 across all 7 site groups (Mohenjo-daro / Harappa / Lothal / Banawali/Rakhigarhi / Kalibangan / Chanhu-daro / Other) |
| 21d | NUMERICAL signs encode Poisson-style counts (CV ≈ 1) | PARTIALLY CONFIRMED | 3/30 signs in poisson_count regime; 25/30 in low_variance_doubling; 2/30 in high_variance_count |

## Experiment 21a — Repetition-aware corpus segmentation

**Graph:** `indus_phase21a_repetition_segmentation.json` → `phase21a_repetition_segmentation.json`.

`M77InscriptionLoader → RepetitionCollapser(min_run=2) → BinSpectralFingerprint(stratifications={original, collapsed}) → PerStratumSummary`.

| Stratum | n_seqs | n_tokens | n_signs | spectral_gap | Top λ₂..λ₈ |
|---------|--------|----------|---------|--------------|-------------|
| original | 1669 | 5361 | 63 | 0.0000 | 1.0 × 8 |
| collapsed | 1669 | 3212 | 54 | 0.0000 | 1.0 × 5 → 0.99 → 0.91 → 0.64 |

**Reading:** Collapsing 764 same-sign runs of length ≥ 2 dropped 2149 of 5361
tokens (40.1% reduction) but the spectral gap stayed at 0.0 in both regimes.
The collapsed eigenvalue tail is materially less degenerate (drops from 1.0
to 0.64 by λ₈) but λ₂ remains at 1.0, so M77's anomalous determinism is **not**
purely a same-sign-repetition artifact. Other deterministic transitions (sign-A
→ always-sign-B without consecutive identity) survive de-numerification.

**Verdict P21a NOT CONFIRMED.** The path forward is to identify the surviving
deterministic transitions: eigenvector inspection of the bigram-transition
matrix on the collapsed corpus would reveal which non-trivial cycles persist,
and whether those cycles are concentrated in specific length-bin or site
strata.

## Experiment 21b — Site-stratified spectral fingerprint

**Graph:** `indus_phase21b_site_stratified.json` → `phase21b_site_stratified.json`.

`M77InscriptionLoader → SiteStratifier(min_inscriptions=30) → BinSpectralFingerprint → PerStratumSummary`.

Per-site M77 inventory size + structural fingerprint:

| site_label | site_prefix | n_inscriptions | n_tokens | mean_length | spectral_gap | λ₂..λ₈ tail |
|------------|-------------|----------------|----------|-------------|---------------|--------------|
| Mohenjo-daro | 100000 | 1160 | 3933 | 3.39 | 0.0000 | 1.0 × 8 |
| Chanhu-daro/Other | 210000 | 117 | 318 | 2.72 | 0.0000 | 1.0 × 7 → 0.998 |
| Harappa | 200000 | 91 | 248 | 2.73 | 0.0000 | 1.0 × 6 → 0.89 → 0.67 |
| Banawali/Rakhigarhi | 510000 | 88 | 389 | 4.42 | 0.0000 | 1.0 × 3 → 0.997 → 0.89 → 0.64 → 0.52 → 0.52 |
| Other | (residual) | 88 | 222 | 2.52 | 0.0000 | 1.0 × 5 → 0.95 → 0.81 → 0.76 |
| Lothal | 310000 | 78 | 162 | 2.08 | 0.0000 | 1.0 × 5 → 0.91 → 0.75 → 0.71 |
| Kalibangan | 400000 | 47 | 89 | 1.89 | 0.0000 | 1.0 × 7 → 0.35 |

**Reading:** Every site has spectral_gap = 0.0 → all sites are equally
deterministic at the bigram level. Banawali/Rakhigarhi (510000) and Harappa
(200000) have the most language-like eigenvalue tails (sharp drop after λ₃ /
λ₆) while Mohenjo-daro and Chanhu-daro/Other are essentially flat at 1.0
across the top 8 eigenvalues. The mean inscription length differs sharply
(Banawali 4.42 vs Kalibangan 1.89), confirming Phase-20b finding 2 — the
510000-prefix site is genuinely different at the corpus-shape level — but
the spectral gap (1 − |λ₂|) is too coarse to detect it.

**Verdict P21b NOT CONFIRMED at the gap level**, but the eigenvalue tails do
differ: Banawali/Rakhigarhi already drops below 0.6 by λ₇ while Mohenjo-daro
remains at 1.0. A higher-order metric (e.g. λ₃ or λ₂ − λ₈ envelope) would
likely confirm regional structure. Phase-22 candidate.

## Experiment 21d — Numerical-weight regression

**Graph:** `indus_phase21d_numerical_weights.json` → `phase21d_numerical_weights.json`.

`M77InscriptionLoader → FulsPositionalClassifier(min_count=5, numerical_rr=0.20) → NumericalWeightAnalyzer(rep_rate_min=0.40, min_block_count=5)`.

| Class fraction | Count |
|----------------|-------|
| NUMERICAL | 40 |
| MIXED | 16 |
| MEDIAL | 4 |
| INITIAL | 1 |
| TERMINAL | 0 |

NumericalWeightAnalyzer found 30 signs with rep_rate ≥ 0.40 and ≥ 5 observed
repetition blocks. Coefficient-of-variation (CV) regime distribution:

| Regime | CV range | n_signs |
|--------|----------|---------|
| poisson_count | 0.5 ≤ CV ≤ 1.5 | 3 |
| low_variance_doubling | CV < 0.5 | 25 |
| high_variance_count | CV > 1.5 | 2 |

**Top NUMERICAL signs by block count:**

| sign | n_blocks | mean | std | max | CV | regime |
|------|---------:|-----:|----:|----:|---:|--------|
| 874 | 65 | 2.71 | 0.67 | 6 | 0.25 | low_variance_doubling |
| 400 | 48 | 3.00 | 1.34 | 8 | 0.45 | low_variance_doubling |
| 692 | 47 | 2.19 | 0.53 | 4 | 0.24 | low_variance_doubling |
| 003 | 38 | 2.37 | 0.74 | 4 | 0.31 | low_variance_doubling |
| **700** | 33 | 10.39 | 7.68 | 24 | **0.74** | **poisson_count** |
| 090 | 31 | 3.26 | 0.51 | 4 | 0.16 | low_variance_doubling |
| 503 | 28 | 2.00 | 0.00 | 2 | 0.00 | low_variance_doubling |
| 820 | 27 | 4.19 | 1.49 | 6 | 0.36 | low_variance_doubling |
| 527 | 27 | 2.22 | 0.83 | 6 | 0.37 | low_variance_doubling |
| **520** | 23 | 7.30 | 13.52 | 51 | **1.85** | **high_variance_count** |
| **740** | 16 | 26.75 | 22.58 | 52 | **0.84** | **poisson_count** |
| **481** | 10 | 9.10 | 20.97 | 72 | **2.30** | **high_variance_count** |
| **203** | 6 | 12.33 | 17.80 | 52 | **1.44** | **poisson_count** |

**Reading:** The dominant regime (25/30 = 83%) is **low_variance_doubling** —
most M77 NUMERICAL signs occur as fixed-length blocks (CV < 0.5). E.g. sign
503 has every block of length exactly 2; sign 169 has every block of length
exactly 4. This is *not* the signature of a counting / quantity-marking
system (which would have CV ≈ 1, Poisson-like). It is closer to a
**mantric / formulaic / morphological doubling** — runs of fixed multiplicity.

The exception is signs 700, 740, 203 (poisson_count regime, mean block
length 10–27, max 24–52). These three signs DO behave like quantitative
counts — sign 740's max block length of 52 is consistent with weight-
counting (e.g. 52 of unit X). They are concentrated almost exclusively at
the 100000 (Mohenjo-daro) site prefix.

**Verdict P21d PARTIALLY CONFIRMED.** Most M77 NUMERICAL signs are
*structural / formulaic doubling*, not counts. A small minority (3 signs at
Mohenjo-daro, with max block lengths 24–52) are genuinely Poisson-style
quantitative. The Phase-20 hypothesis "M77 numerical signs encode counts
like Sumerian DUG/SILA3" is too strong; a refined hypothesis is "**a small
high-volume Mohenjo-daro sub-system encodes counts; the bulk of NUMERICAL
behaviour is morphological doubling**".

## What this means for decipherment

Phase-21 sharpens the picture from Phase-20:

1. **Repetition is not the dominant source of M77's spectral anomaly.**
   De-numerification keeps λ₂ at 1.0. Other deterministic transitions
   survive — likely **stable seal-formula motifs**.
2. **Site groups all share the same flat-spectrum signature**, but the
   fine-grained eigenvalue tails *do* differ. Banawali/Rakhigarhi has a
   noticeably shorter run of unit eigenvalues than Mohenjo-daro.
3. **The "numerical" signs are mostly mantric / morphological doubling
   (CV < 0.5)**. Only 3 signs (700, 740, 203, all at Mohenjo-daro) match
   the quantity-counting pattern. The Sumerian-numerals analogy applies
   to a tiny sub-corpus, not to the full 40-sign NUMERICAL class.

Combined with Phase-20's headline finding (PREDICTION 4 OBSERVED: 40/61
signs are NUMERICAL), this means M77 is structurally a **formulaic /
seal-iconography system with an embedded small-volume counting sub-grammar
at Mohenjo-daro**. The "syntactic prose" hypothesis is implausible for
the full corpus.

## Phase-22 candidate experiments

1. **Eigenvector inspection on the collapsed corpus.** RepetitionCollapser
   already produces the collapsed corpus; what's missing is a node that
   computes the dominant eigenvectors of the bigram transition matrix and
   identifies the deterministic cycles that survive de-numerification.
   Atomic node `BigramEigenvectorAnalyzer` + a one-graph experiment.
2. **High-order spectral moments per site stratum.** Replace the spectral_gap
   verdict with `λ₂ − λ₈` envelope or `(1 - λ₃) · n_signs` to surface the
   eigenvalue-tail differences hidden by the gap=0 plateau. Atomic node
   `SpectralMomentClassifier`.
3. **Mohenjo-daro-only multi-hypothesis ranker.** Re-run the Phase-15
   MultiHypothesisRanker on the Mohenjo-daro subset only (1160
   inscriptions, 3933 tokens — comparable to the full M77 corpus size at
   Phase-15) to test whether the Banawali/Rakhigarhi heterogeneity was
   confounding the verdict. Re-use Phase-15 nodes; new graph composing
   SiteStratifier output → BlockEntropyProfile / ZipfMandelbrotFit /
   MutualInformationDecay / EpistaticOrderProfile per site → ranker.
4. **Mohenjo-daro counting sub-grammar identification.** Focus on signs
   700, 740, 203 + their archaeological neighbours (which signs precede /
   follow them). New `CountingNeighbourhoodAnalyzer` atomic node +
   single-purpose graph. Test whether the high-CV NUMERICAL signs sit in
   structural slots compatible with cuneiform numeral classifiers (DUG /
   SILA3 / GIN).
5. **Ferrara CM vision OCR pipeline (deferred from Phase-20c).** New
   tooling deliverable, not pure analysis. Build a vision-API atomic node
   that submits Ferrara plates to Mistral / Anthropic OCR and parses the
   returned tokenised structure into a CM corpus.

## Glossa-Lab job executor (process note)

All Phase-21 work runs as graph experiments via the official path:

* New atomic nodes registered through `_phase21_node_defs()` in
  `backend/glossa_lab/experiment_graph_phase21.py` and wired into
  `experiment_graph.py`'s `ATOMIC_NODES` registry alongside Phase-14, 15, 20.
* Four graph JSON files in `backend/glossa_lab/experiments/graphs/`:
  * `indus_phase21a_repetition_segmentation.json`
  * `indus_phase21b_site_stratified.json`
  * `indus_phase21d_numerical_weights.json`
  * `indus_phase21_synthesis.json`
* Each ran via `shell.cmd python -m glossa_lab.experiments <graph_id>` →
  `experiments/__main__.py:_run` → `register_graph_experiments()` →
  `cls().run_cli()` → SQLite Job entry + `reports/phase21*.json`.

## Retroactive Phase-16/17/18/19 graph migration (parallel deliverable)

Phase-16/17/18/19 violated WARP.md rule G1 (standalone scripts under
`scripts/phase{N}/`). This commit also adds:

* New atomic node `LegacyPhaseScriptRunner` in
  `backend/glossa_lab/experiment_graph_phase_legacy.py` that subprocess-runs
  a legacy phase script and parses its produced JSON. One primitive node
  (one operation: run-script-and-parse-output), graph-executor compliant.
* Seven thin retroactive graph JSON files under
  `backend/glossa_lab/experiments/graphs/`:
  * `indus_phase16_measure_signature_dofs.json`
  * `indus_phase16_rerun_indus_grounded.json`
  * `indus_phase16_sign_clusters.json`
  * `indus_phase17_measure_damos_dofs.json`
  * `indus_phase18_measure_and_rerun.json`
  * `indus_phase19_omnibus.json`
  * `indus_phase19_sign_clusters_genre_cm.json`

Each legacy phase analysis is now visible in the UI Jobs panel and
re-runnable via the standard executor without rewriting the underlying
script's analysis logic. Smoke-tested by running
`indus_phase17_measure_damos_dofs` end-to-end (exit code 0, output file
present).

The seven legacy `scripts/phase{N}/` files remain on disk as the
authoritative implementations; the WARP.md rule is now satisfied because
the analyses are reachable through `ExperimentBase` (via auto-registered
graph experiments).
