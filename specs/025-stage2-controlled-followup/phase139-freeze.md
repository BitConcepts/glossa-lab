# Spec 025 — Phase-139 Freeze Record (for Phase-140 / Phase-141)

> ## FROZEN at the Phase-139 merge (2026-10-10)
>
> This record is the freeze gate of plan.md (Phase-139,
> step 5). It names the final strata definition, the seed,
> and the decision thresholds that Phase-140 (G1) and
> Phase-141 (LOSO) inherit. Phase-140 code is written only
> against this record. Any deviation is recorded here as a
> dated amendment BEFORE Phase-140 executes; nothing in
> this record is tuned after a G1 outcome is seen.

## 1. Basis

- Spec 025 as frozen 2026-10-10 (spec.md §11 adjudication;
  PR #129, main `c3101cce`).
- Phase-139 audit (this PR): `reports/phase139_report.md`,
  `reports/phase139_results.json`, harmonized dataset +
  citation register in `data/evidence_integration/`
  (`phase139_*`). Gate applied verbatim (§4.2 step 3):
  chron_band SENSITIVITY (41.9% recorded — arm (i) fails);
  depth_band SENSITIVITY (51.1% — arm (i) fails);
  preservation PRIMARY CONTROL (99.9%; 7 sites ≥ 30;
  5,404 permutable).

## 2. G1 design as inherited (Phase-140)

- **Population:** the Phase-137 F3 analysis population,
  reproduced by Phase-139 (5,410 inscriptions, 7 eligible
  sites, ICIT-lineage layer, sha256
  `c368f290d8d784093d804243100de27ae6ad09df3ae37cab7432a0205d4ec9ef`).
- **Profile table / statistic / inference:** exactly the
  Phase-137 F3 configuration (sign columns = layer-wide
  count ≥ 10 within the population, rarer → OTHER;
  placeholders `000`/`999` excluded; Pearson χ² as
  divergence statistic; permutation of site labels at
  inscription level within strata, B = 9,999,
  p = (1 + #{χ²_perm ≥ χ²_obs}) / (1 + B)).
- **Seed:** `20261009` (the Phase-136/137 seed; named here
  so no later choice exists).
- **Primary strata (final):** composition (Phase-137 type
  class × length class) × **preservation** (complete /
  fragment / damaged), with `UNRECORDED` retained as a
  stratum level (6 population rows). Projected permutable
  inscriptions under these strata: 5,404 of 5,410.
- **Verdict rule:** SUPPORTED under control iff G1's raw
  permutation p ≤ 0.05 — Benjamini–Hochberg over G1 alone
  at q = 0.05 (adjudication Q4(b)); NOT SUPPORTED under
  control otherwise. §4.4's falsifier and §7's claim
  ceiling apply as frozen.
- **Mandatory headline content:** the ICIT-lineage label;
  the preservation recorded coverage (99.9%); and the
  statement that **chronology is NOT controlled** in the
  primary test (period/phase remain uncontrolled
  confounders), with the sensitivity panel reported
  alongside.

## 3. Sensitivity panel (EXPLORATORY — pre-declared)

Routed by the §4.2 routing rule at Phase-139; computed in
Phase-140 alongside G1, labeled EXPLORATORY in every
artifact, reported as bounds, never as the controlled
verdict, and excluded from any verdict word:

- **S-chron:** the G1 statistic under composition ×
  chron_band strata (chron_band per the Phase-139 citation
  register, Class C; UNRECORDED retained as a level).
- **S-depth:** the G1 statistic under composition ×
  depth_band strata (within-site relative tertiles;
  UNRECORDED retained as a level).

## 4. Phase-141 (LOSO) as inherited

- Members L-MD / L-HA / L-KA in the §5 configuration
  (stratum odds ratios + Fisher exact per stratum,
  Phase-136 machinery), verdict-relevant only through the
  §5 robustness criterion, verbatim.
- Reported with raw permutation p-values where applicable;
  **no q-values are computed for LOSO members** (Q4(b)).

## 5. Publication

Per adjudication Q6: the Spec 025 outcome record (this
freeze + G1 executed, or a NOT ESTIMABLE closeout had the
gate gone the other way) publishes through the standing
release path at family completion. NOT ESTIMABLE and NOT
SUPPORTED outcomes publish with the same prominence as
positive ones (§8.7).

*Freeze record ends. Amendments append-only, dated, and
committed before the execution they affect.*
