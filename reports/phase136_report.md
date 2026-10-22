# Phase-136 Report — Terminal-Class × Object Type (ICIT-lineage (horus84) joined subset) — Spec 024 Stage 2(a), Family Member F1

**Headline (lineage label mandatory):** On the **ICIT-lineage
(horus84)** catalogue-joined subset — results describe this lineage
layer's joined subset, not the Indus corpus in general — the
terminal sign's membership in the frozen TERMINAL14 class differs
between Seals and Tablets after within-site control: observed
Cochran–Mantel–Haenszel chi-square **47.0047**, permutation raw
**p = 0.0001** (the minimum attainable at B = 9,999; 0 of 9,999
permutations reached the observed statistic), Mantel–Haenszel
common odds ratio **2.384** (95% CI 1.847–3.077). The verdict word
is **deferred**: it is assigned only after the family
Benjamini–Hochberg correction (q = 0.05) in the combined Stage 2
report (freeze §§1–2). This raw p is an intermediate quantity.

Frozen protocol: `specs/024-evidence-integration/stage2a-freeze.md`
(merged before any Phase-136 analysis code ran). Builder:
`backend/scripts/phase136_terminal_type.py`; full record:
`reports/phase136_results.json`.

## Flow as run

| Step | Count |
|---|---|
| ICIT-lineage layer rows | 5,679 |
| Matched (cisi in exactly one volume) | 2,895 |
| Ambiguous (value `H-311`, in both volumes) | 2 |
| Unmatched | 2,782 |
| Unjoinable-or-ambiguous share | **49.0%** (2,784 of 5,679) |
| Typed (catalogue object_type filled) | 2,752 — Seals 1,588; Tablets 1,088; Graffiti 69; Objects 7 |
| Untyped (excluded, counted) | 143 |
| Restricted to {Seals, Tablets} | 2,676 |
| Terminal mapped (W→P, frozen machinery) | 2,195 |
| Terminal UNK (excluded, counted) | 481 |
| TERMINAL14 margin among mapped | 475 |

Every design-audit expectation in freeze §3 reproduced exactly;
no drift. Catalogue-site concordance for joined rows (descriptive
only, freeze §4; not a variable): concordant 1,377 / discordant
1,518.

## Strata and estimability

Eligible strata (analysis-population N ≥ 20, ≥5 Seals, ≥5
Tablets): **Mohenjo-daro, Harappa, Kalibangan** — analysis
population in eligible strata 2,062 of 2,195 mapped rows.

| Stratum | Seals (TERM / n) | Tablets (TERM / n) | Per-stratum OR |
|---|---|---|---|
| Mohenjo-daro | 258 / 859 (30.0%) | 48 / 292 (16.4%) | 2.182 |
| Harappa | 69 / 281 (24.6%) | 61 / 579 (10.5%) | 2.764 |
| Kalibangan | 5 / 40 (12.5%) | 1 / 11 (9.1%) | 1.429 |

Pooled eligible 2×2: Seals 332 TERMINAL14 / 848 not; Tablets 110 /
772. All four pooled expected counts ≥ 5 (minimum 189.06;
fraction ≥ 5 = 1.0) and ≥2 eligible strata — **ESTIMABLE** under
freeze §5.

## Results as found

- Observed CMH statistic (no continuity correction): **47.0047**.
- Permutation null (within-stratum shuffle of type labels,
  B = 9,999, seed 20261009, `random.Random(20261009)`): median
  0.455, 95th percentile 3.991; **0** permutations ≥ observed.
- Raw p = (1 + 0) / (1 + 9,999) = **0.0001**.
- MH common OR **2.384**, 95% CI (Robins–Breslow–Greenland)
  **1.847–3.077**.
- Crude (unstratified) OR **2.748** (95% Wald CI 2.169–3.481) —
  **uncontrolled**, reported only so the control's effect is
  visible: within-site control attenuates the association but
  does not remove it.
- Pooled TERMINAL14 shares: Seals 28.1% (332/1,180), Tablets
  12.5% (110/882).

**Verdict word: DEFERRED** to the combined Stage 2 report's
family BH correction (freeze §§1–2). No verdict is claimed here.

## Adversarial note (freeze §7)

The strongest alternative explanation for any association found
is compilation-internal: the lineage's transcription and the
catalogue's typing were both made within one scholarly tradition.
The within-site control does not imply more independence than
exists.

## Deviations

None. One implementation note, not a deviation: two descriptive
ineligible strata (Chanhu-daro, Banawali) have a zero cell, so
their per-stratum odds ratio is undefined; the results JSON
records `null` with an explanatory note rather than a
non-finite value, keeping the JSON strict. No eligible stratum,
table, statistic, or effect size is affected.

## Fences observed

- §8 language: associations describe **use, not meaning**. No
  result here can mint, promote, demote, or validate any sign
  reading, change any anchor's status, or move PRED-2026 in
  either direction.
- No PRED: the builder imports only the frozen mapping machinery
  (`build_sign_maps` / `SignMapper.map_w`) from
  `pred_harness`; it never imports or calls `evaluate`,
  `dry_run`, or any PRED scoring, and no Phase-136 output is an
  input to the PRED harness.
- Class I fields (horus84 `class`/`sanskrit`/`translation`/
  `notes`) entered nothing. The `text` field was used only as
  the text substrate (freeze §0).
- Anchors byte-identical: sha256
  `eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86ebb1fa3b602cfaed`.
- Input paths + sha256 for every input file are recorded in
  `reports/phase136_results.json`.

## AI disclosure

Produced by an AI agent (Muse Spark, via Muse) at the
direction of Tristen Pierson, per constitution §VI.
