# Spec 025 Combined Report — Stage 2 Controlled Follow-Up (Phases 139–141)

**ICIT-lineage layer (horus84) — G1 headline, with its
mandatory rider: preservation recorded coverage 99.9%;
chronology is NOT controlled in the primary test
(period/phase remain uncontrolled confounders), with
the sensitivity panel reported alongside.**

Spec 025 asked the disciplined follow-up to Spec 024's
Stage 2: F3 — site repertoire differentiation on the
ICIT-lineage layer — was SUPPORTED under a
composition-only control, with period, preservation,
and excavation history named as uncontrolled
confounders. This spec's work, all of it under the
owner's 2026-10-10 adjudication (§11, all six asks
answered with the recommended answers), was: audit
what the layer can actually support as covariates
(Phase-139), re-test F3 under the one control the data
can bear (Phase-140, G1), bound the rest through a
pre-declared sensitivity panel, and stress the F1
result the same program had already published
(Phase-141, LOSO). Everything below is reported as
found; Spec 024's records are unedited, and G1 stands
alongside F3, never instead of it.

## 1. The not-freezable-as-sketched finding (Phase-139)

The spec as sketched named candidate controls —
excavation context, stratigraphy/depth, object
completeness/preservation, chronology — before anyone
had measured whether the layer records them. Phase-139
(cost: margins only; no association statistic was
computed) reproduced the §3 fill tables **exactly**
from the layer file and found the sketched versions
largely unusable: the layer's `unit` field is a locus
label, not an excavation unit (excavation-unit control:
impossible); `depth` is recorded on 51.1% of rows in
mixed and incommensurable forms (absolute cross-site
depth control: rejected as indefensible, Q3);
`context` is empty on 5,679 of 5,679 rows;
surface-collection rows do not exist on this layer;
and per-phase chronology per site exists only as
published-stratigraphy compilations of varying
granularity. The honest replacements, frozen before
any test ran: published-stratigraphy harmonization to
≤ 3 chronology bands with per-cell citations
(Class C constructed context, Q2(a)); within-site
relative depth tertiles (Q3(a)); a mechanical
preservation collapse (Class O). The frozen §4.2 gate
(≥ 70% recorded coverage; ≥ 3 eligible sites at ≥ 30
recorded; ≥ 1,000 permutable) then classified, and
the routing rule decided G1's design:

| Covariate | Recorded | Gate | Route |
|---|---|---|---|
| preservation | 5,404 / 5,410 (99.9%) | passes all arms | **PRIMARY CONTROL** |
| chron_band | 2,267 / 5,410 (41.9%) | fails arm (i) | sensitivity |
| depth_band | 2,765 / 5,410 (51.1%) | fails arm (i) | sensitivity |

Verdict at Phase-139: **G1 ESTIMABLE**, primary strata
= composition (Phase-137 type class × length class) ×
preservation, UNRECORDED retained as a stratum level.
Freeze records: `phase139-freeze.md` (PR #130),
`phase140-freeze.md` + `phase141-freeze.md` (PR #131).

## 2. G1 — the controlled re-test (Phase-140)

Population reproduced by rule and asserted against
the committed F3 record (5,410 inscriptions, 7 sites);
the uncontrolled configuration first reproduced
Phase-137 F3 **exactly** (χ² 4,966.362228365138;
0/9,999; null median 2,667.87), so comparability is
mechanical. G1 permutes site labels within composition
× preservation strata (53 strata; permutable
5,404/5,410; B = 9,999; seed 20261009):

- Observed χ² 4,966.36 vs controlled null median
  2,684.74 (p95 2,859.30); **0 of 9,999 permutations ≥
  observed; raw p = 0.0001**.
- BH over G1 alone (Q4(b), m = 1, q = 0.05): adjusted
  0.0001 → **G1 SUPPORTED under control** — stated
  plainly, this is the raw p against 0.05 for a
  one-member family, not a family correction across
  the LOSO members.
- Cramér's V 0.2190 (descriptive); sparsity disclosed
  (887/1,309 cells expected < 5, 67.8%).

**Headline, with rider:** on the **ICIT-lineage layer
(horus84)**, with preservation recorded coverage
**99.9%**, the site-repertoire association survives
preservation control (raw p = 0.0001). **Chronology is
NOT controlled in the primary test** — differential
preservation as recorded does not account for the
association; period/phase differences across sites
remain a live alternative explanation, bounded in §3.

## 3. Sensitivity panel (EXPLORATORY — bounds, never the verdict)

Same statistic, B, seed; permutation within
composition × the named strata; UNRECORDED as a level:

| Sensitivity | Coverage | Permutable | Null median | Perms ≥ obs | Raw p |
|---|---|---|---|---|---|
| S-chron (× chron_band) | 41.9% | 5,342 | 2,809.53 | 0 / 9,999 | 0.0001 |
| S-depth (× depth_band) | 51.1% | 5,406 | 2,682.78 | 0 / 9,999 | 0.0001 |

Under the chronology-stratified exploratory null the
median rises (2,809.53) and still no permutation
reaches the observed statistic; the depth-stratified
bound is the same. These bounds say the association is
not an artifact of the recorded parts of either
covariate under their strata; they do not convert
chronology into a controlled variable, and no verdict
word attaches to either.

## 4. LOSO — F1 robustness (Phase-141)

Phase-136 machinery unchanged plus the stratum-drop
parameter only; the no-drop configuration reproduced
Phase-136 **exactly** before subsets were accepted.
All three subsets ESTIMABLE (§5 rule):

| Subset | CMH | Raw p | MH common OR | 95% CI |
|---|---|---|---|---|
| L-MD (drop Mohenjo-daro) | 28.5198 | 0.0001 | 2.706 | 1.858–3.940 |
| L-HA (drop Harappa) | 20.5927 | 0.0002 | 2.162 | 1.541–3.033 |
| L-KA (drop Kalibangan) | 47.1515 | 0.0001 | 2.400 | 1.857–3.103 |

**Robustness statement (§5 criterion, outcome
verbatim):** *F1 is STABLE under leave-one-site-out:
every estimable subset's Mantel-Haenszel common OR
remains > 1 with its 95% CI excluding 1, so no single
site is load-bearing for the F1 result.* Raw p-values
only; no q-values (Q4(b)); LOSO minted no verdicts and
changed no Spec 024 record.

## 5. What this program does and does not establish

Established, on the labeled layer and under the named
controls: the F3 site-repertoire association is not
accounted for by composition (Phase-137), nor by
preservation as recorded (G1), nor — as exploratory
bounds — by the recorded parts of harmonized
chronology or relative depth; and F1's terminal-class
× object-type association does not rest on any single
site (LOSO). Not established: anything about meaning;
anything layer-free (the Holdat layer's F2 null stands
beside these positives, and the contrast is not itself
a test); and not a chronology-controlled result —
chronology enters only as a partial-coverage
exploratory bound. Compilation-internal explanations
(transcription and compilation practice within one
scholarly tradition) remain live alternatives for every
number here. No anchor moved; PRED-2026-001/002/003
untouched; the strict core (94 readings) is exactly
where it was.

## 6. Record

- Phase-139: PR #130 (merge `9d917440`) —
  `reports/phase139_report.md`, `phase139_results.json`,
  harmonized covariates + citation register in
  `data/evidence_integration/`.
- Freezes: PR #129 (spec, merge `c3101cce`); PR #130
  (Phase-139 freeze record); PR #131
  (`phase140-freeze.md`, `phase141-freeze.md`, merge
  `2ca98d05`).
- Phase-140: PR #132 (merge `f7f1292b`) —
  `reports/phase140_report.md`, `phase140_results.json`.
- Phase-141: PR #133 (merge `fdfb0b39`) —
  `reports/phase141_report.md`, `phase141_results.json`.
- Publication: Spec 025 outcome record, Zenodo v4.9.0
  (Q6 standing release path), with the Phase-139/140/
  141 results JSONs deposited alongside this report's
  program note.

**AI disclosure:** produced by AI agents (Muse Spark,
via Muse) at the direction of Tristen Pierson,
per constitution §VI.
