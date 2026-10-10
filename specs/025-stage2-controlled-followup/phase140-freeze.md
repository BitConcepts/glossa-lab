# Spec 025 — Phase-140 Freeze Record (G1 controlled F3 re-test)

> ## FROZEN 2026-10-10 — before any Phase-140 code runs
>
> This record freezes the Phase-140 (G1) design at
> execution level, under the Phase-139 freeze record
> (`phase139-freeze.md`, merged with PR #130, main
> `9d917440`). It adds no design choice the frozen spec
> and the Phase-139 record do not already determine; it
> pins the remaining execution detail (stratum-key
> construction, the pre-run regression requirement, and
> the reporting obligations) so that no choice is left
> after an outcome is seen. Amendments append-only,
> dated, and committed before the execution they affect.

## 1. Basis

- Spec 025 as frozen 2026-10-10 (spec.md §11
  adjudication; PR #129, main `c3101cce`): all six asks
  answered with the recommended answers.
- Phase-139 freeze record (`phase139-freeze.md` §2–§3):
  final strata, seed, verdict rule, sensitivity panel.
- Phase-139 report (`reports/phase139_report.md`) and
  results (`reports/phase139_results.json`): the gate
  applied verbatim — preservation PRIMARY CONTROL
  (99.9% recorded; 7 sites ≥ 30; 5,404 permutable);
  chron_band and depth_band SENSITIVITY (41.9% / 51.1%
  recorded; arm (i) fails for both).
- Phase-137 execution (Spec 024 Stage 2(c), family
  member F3): the statistic family reused verbatim for
  comparability (`backend/scripts/
  phase137_site_repertoire.py`, results
  `reports/phase137_results.json`).

## 2. The G1 test — exactly

- **Population:** the Phase-137 F3 analysis population,
  reproduced by rule from the ICIT-lineage layer
  (horus84 `inscriptions.csv`, sha256
  `c368f290d8d784093d804243100de27ae6ad09df3ae37cab7432a0205d4ec9ef`):
  sites eligible under the Phase-137 rule (≥ 30
  inscriptions AND ≥ 100 parsed tokens) — Chanhu-daro,
  Dholavira, Harappa, Kalibangan, Lothal, Mohenjo-daro,
  Nausharo — and rows with ≥ 1 parsed token: **5,410
  inscriptions**. The population reproduction is
  asserted against `reports/phase137_results.json`
  (population counts, profile table, column set) before
  any permutation runs.
- **Covariate join:** per-inscription `preservation_class`,
  `chron_band`, and `depth_band` come from the committed
  Phase-139 harmonized dataset
  (`data/evidence_integration/
  phase139_harmonized_covariates.json`), joined on the
  layer's unique `id` column. The join must cover all
  5,410 population rows exactly (asserted); the joined
  `composition_stratum` in that file must equal the
  composition stratum computed from the layer for every
  row (asserted) — a mismatch is a stop condition, not
  a repair opportunity.
- **Profile table / statistic / effects:** exactly the
  Phase-137 F3 configuration. Sign columns = signs
  whose layer-wide token count within the population
  is ≥ 10; rarer signs pool into `OTHER`; placeholder
  codes `000` / `999` are excluded from profiles.
  Statistic: Pearson χ² of the site × sign profile
  table as a divergence statistic. Descriptive effects:
  Cramér's V; per-site total-variation distance to the
  pooled profile. Sparsity disclosure is mandatory
  (cells total, cells with expected < 5 and their
  share, minimum expected count, per-site token
  counts), carried from Phase-137 practice.
- **Inference:** permutation of site labels at
  inscription level **within strata** (below),
  B = 9,999, `random.Random(20261009)` (Fisher–Yates
  via `shuffle`), p = (1 + #{χ²_perm ≥ χ²_obs}) /
  (1 + B). No asymptotic p-value is reported anywhere.
- **Primary strata (final, from the Phase-139
  record):** composition (Phase-137 type class ×
  length class) × **preservation** (complete /
  fragment / damaged), with `UNRECORDED` retained as
  a stratum level (6 population rows). Stratum key:
  `{type_class}|{length_class}|{preservation_class}`.
  The primary-control set is exactly
  **{preservation}**; adding any other covariate to
  the primary strata contradicts Phase-139 and is
  forbidden.
- **Permutable N:** for every configuration, the
  report states the nominal N (5,410) and the
  permutable (effective) N — inscriptions in strata
  containing ≥ 2 distinct sites. Rows in single-site
  strata are constant under permutation and
  contribute nothing; they are counted and reported,
  never dropped silently. (Phase-139 projection for
  the primary strata: 5,404 of 5,410.)

## 3. Verdict rule (adjudication Q4(b))

- G1's verdict word is assigned from Benjamini–Hochberg
  over **G1 alone** at q = 0.05. With a family of one
  this is exactly the raw permutation p against 0.05,
  and every artifact states it in that plain form so
  nobody later mistakes it for a family correction
  across the LOSO members: **SUPPORTED under control
  iff raw p ≤ 0.05; NOT SUPPORTED under control
  otherwise.**
- §4.4's falsifier applies as frozen: a NOT SUPPORTED
  outcome is recorded as *"NOT SUPPORTED under
  confounder control on this layer"*, reported
  alongside — never instead of — the Phase-137
  composition-only result, with the design difference
  stated as the finding.
- **Mandatory headline rider.** Every G1 headline,
  abstract, ledger entry, and the release note states:
  (i) the **ICIT-lineage layer (horus84)** label;
  (ii) the preservation recorded coverage (99.9%);
  (iii) that **chronology is NOT controlled in the
  primary test** — period/phase (chronology) remain
  uncontrolled confounders — with the sensitivity
  panel reported alongside. A G1 number quoted
  without the rider is a misquote of this freeze.

## 4. Sensitivity panel (EXPLORATORY — pre-declared)

Computed alongside G1 in Phase-140, under the same
statistic, B, seed, and p formula; permutation within
the named strata. Labeled **EXPLORATORY** in every
artifact, reported as bounds on the controlled
result, never as the controlled verdict, and excluded
from every verdict word (§8.5–§8.6 apply):

- **S-chron:** strata = composition × `chron_band`
  (early / middle / late / UNRECORDED as a level;
  harmonization per the Phase-139 citation register,
  constructed context, Class C). Recorded coverage
  41.9% — stated wherever the bound appears.
- **S-depth:** strata = composition × `depth_band`
  (within-site relative tertiles: shallow / middle /
  deep / UNRECORDED as a level; the control is
  relative, never absolute — §11 Q3). Recorded
  coverage 51.1% — stated wherever the bound appears.

## 5. Pre-run regression requirement (comparability)

Before the controlled run is accepted, the Phase-140
machinery is run in the **uncontrolled configuration**
— strata = composition only, the Phase-137 F3
configuration — on the same population, and must
reproduce the committed Phase-137 F3 result **exactly**:
observed χ², #{χ²_perm ≥ χ²_obs}, permutation median
and 95th percentile, and raw p from
`reports/phase137_results.json`. Any mismatch is a
stop condition: the controlled run does not proceed
until the cause is found and recorded here as a dated
amendment. The regression outcome is reported in the
Phase-140 report.

## 6. Execution and reporting obligations

- Graph-first (H15/H23): the Phase-140 experiment-graph
  node is registered and verified before the run;
  foundation check (H21) 0 failures after the phase.
- Anchors asserted byte-identical (sha256
  `eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86ebb1fa3b602cfaed`)
  before and after the run; the layer file is consumed
  read-only and hash-asserted.
- Deliverables: `reports/phase140_results.json`
  (flow, per-configuration strata tables, permutable
  N, observed vs null distribution, V, per-site TV
  distances, sparsity disclosures, coverage
  statements, the regression record) and
  `reports/phase140_report.md` under the mandatory
  lineage headline with the §3 rider in its headline
  paragraph.
- Deviations, if any, are recorded in the phase report
  with the rule that resolved them; no silent
  adaptation. §8's epistemic limits bind every output:
  co-occurrence in a labeled lineage layer; no meaning
  claims; no PRED contact; no anchor movement.

*Freeze record ends. Amendments append-only, dated,
and committed before the execution they affect.*
