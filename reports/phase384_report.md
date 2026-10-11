# Phase-384 — C1 Margin Completion for Phase-137 F2/F3 (Spec 026)

**Rerun of:** Phase-137 (register row PHASE-137; SPEC-024 in
part). **Margin declared before any run (v1 contract):**
Cramér's V = 0.10 practical floor. **Results:**
`reports/phase384_results.json` (v2, governing).

## What the originals said (verbatim)

Combined Stage 2 report (`phase136_137_138_stage2_report.md`):
F2 (Holdat) composition-controlled permutation raw p =
**0.7354** → **NOT SUPPORTED**; F3 (ICIT-lineage) raw p =
**0.0001** (BH 0.00015) → **SUPPORTED**. Point Cramér's V
(descriptive, uncontrolled): F2 0.1154, F3 0.2190 — reported
without intervals or a practical margin. That gap (class C1)
is what this rerun closes.

## v1 execution — and its INVALID interval (preserved)

v1 (frozen digest bf4356440ea035f3…) recomputed χ²/V from the
recorded profile tables exactly (F2 χ² 745.953, V 0.11540; F3
χ² 4966.362, V 0.21901) and computed parametric-bootstrap CIs
over table cells: F2 [0.1526, 0.1733], F3 [0.2309, 0.2526].

The framework's own discriminating-control rule was then
applied to the procedure: on an independence table with F2's
exact margins (true V = 0) the v1 procedure returns CI
**[0.1115, 0.1242]**; with F3's margins, **[0.0984, 0.1095]**.
A procedure that finds V ≈ 0.11 under exact independence is
non-discriminating at these dimensions (tables 9×98 / 7×187;
tokens are not independent draws — inscriptions are the
sampling unit). **The v1 interval adjudication is INVALID**
(Spec 026 principle 5) — not caveated, not used. The v1
verification step (χ²/V reproduced from the recorded tables)
stands.

## v2 execution (frozen before execution, digest 4e6c78bc917c96a3…)

Populations rebuilt with the Phase-137 module's own loaders
and frozen population rule; rebuilt profile tables asserted
EQUAL to the recorded tables (F2: 1,670 inscriptions; F3:
5,410). Inscription-level bootstrap within site (B = 9,999,
seed 20261012); governing interval = BASIC bootstrap.

| Member | V (point) | Percentile CI | Basic CI (governing) | Margin adjudication |
|---|---|---|---|---|
| F2 Holdat | 0.1154 | [0.1530, 0.1719] | **[0.0589, 0.0778]** | upper bound < 0.10 → **CONTRADICTED at the declared margin** (bounded marginal claim) |
| F3 ICIT-lineage | 0.2190 | [0.2276, 0.2557] | **[0.1823, 0.2104]** | lower bound > 0.10 → **SUPPORTED stands at the declared margin** |

Notes on method honesty: Cramér's V carries a large positive
resampling bias on these sparse wide tables (bootstrap median
− point = +0.046 F2 / +0.022 F3); that is precisely why the
percentile interval does not govern and the bias-correcting
basic interval does (declared in the v2 contract before
execution). The basic interval need not contain the point
estimate; its F2 placement below the floor is corroborated
independently by the original composition-controlled
permutation (p = 0.7354), which rejected the F2 claim on the
controlled estimand.

## Verdicts (framework status after this rerun)

- **F2: CONTRADICTED** for the bounded claim of practically-
  sized site-repertoire differentiation on the Holdat layer.
  The original NOT SUPPORTED (controlled permutation) is
  untouched; the rerun adds that the marginal effect size
  itself falls below the declared practical floor under the
  bias-corrected interval. Two routes converge; no reversal.
- **F3: SUPPORTED stands**, now with a bias-corrected interval
  [0.182, 0.210] entirely above the practical floor. The
  original confessions stand unchanged: period, preservation,
  and excavation history were uncontrolled in Phase-137
  (preservation was later controlled for this population by
  Phase-140 / Phase-385, where the effect also stands).

Foundation check after the phase: see the S4 ledger entry.
