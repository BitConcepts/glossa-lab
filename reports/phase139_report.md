# Phase-139 Report — Covariate Audit + Harmonization (Spec 025)

**Lineage:** ICIT-lineage layer (horus84) throughout; F3
population of Phase-137 (Spec 024 Stage 2(c)). **Phase-139
computes margins only** — no association statistic, no
repertoire comparison, no G1 quantity of any kind was
computed in this phase. Sign tokens were read only to
reproduce the Phase-137 population and its composition
strata.

**Design (frozen):** Spec 025, frozen 2026-10-10 on the
owner's adjudication (spec.md §11 — all six asks answered
with the recommended answers; freeze merged as PR #129,
main `c3101cce`). Audit script:
`backend/scripts/phase139_covariate_audit.py`; graph node
`IndusPhase139CovariateAudit` (H15/H23 order: script →
graph module → registration verified → run). Results:
`reports/phase139_results.json`. Harmonized dataset:
`data/evidence_integration/phase139_harmonized_covariates.json`;
citation register:
`data/evidence_integration/phase139_citation_register.json`.

**Inputs (hash-asserted before and after):** layer file
`inscriptions.csv` sha256
`c368f290d8d784093d804243100de27ae6ad09df3ae37cab7432a0205d4ec9ef`
(5,679 rows); anchors `INDUS_FINAL_ANCHORS.json` sha256
`eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86ebb1fa3b602cfaed`
— unchanged; no anchor or PRED movement in this phase.

## 1. Population

The Phase-137 F3 analysis population reproduces exactly:
sites eligible under the Phase-137 rule (≥ 30 inscriptions
AND ≥ 100 parsed tokens) are Chanhu-daro (74), Dholavira
(238), Harappa (2,717), Kalibangan (212), Lothal (208),
Mohenjo-daro (1,923), Nausharo (38); rows with ≥ 1 parsed
token: **5,410 inscriptions**.

## 2. Spec §3 reproduction (T1)

Counts for period / phase / both / preservation reproduce
the draft §3 tables **exactly**, full layer and F3
population:

| table | period | phase | both | union | all three | depth | preservation |
|---|---|---|---|---|---|---|---|
| full layer (5,679) | 2,318 (40.8%) | 2,652 (46.7%) | 1,799 | 3,171 | 921 | 2,808 (49.5%) | 5,670 (99.8%) |
| F3 population (5,410) | 2,266 (41.9%) | 2,638 (48.8%) | 1,788 (33.0%) | 3,116 (57.6%) | 916 (16.9%) | 2,770 (51.2%) | 5,404 (99.9%) |

Three printed draft percentages carry documented deltas
(recorded in the results JSON; none affects any §3
substantive claim or the gate):

1. **Union 57.7%** is the sum of rounded percentages
   (41.9 + 48.8 − 33.0); the exact union count is 3,116 =
   57.6%. Counts agree exactly.
2. **Depth 48.1% / 49.9%**: the draft's exact parse rule
   was not recoverable. This audit's documented parse
   (§4 below) gives 49.5% / 51.2%; a digit+unit-only rule
   gives 48.2% / 50.0%. The depth gate classification is
   SENSITIVITY under every definition in the bracket.
3. **All-three 16.8%** vs 16.9% here — a knock-on of the
   depth definition.

## 3. Chronology harmonization (T3, Q2(a))

`chron_band` was built under the adjudicated basis:
published-stratigraphy harmonization, three bands maximum
(early / middle / late) + `UNRECORDED`, per-cell citations
or `UNRECORDED`, time-boxed to the seven F3 sites'
published schemes. 35 mapped cells, 7 citations
(Kenoyer 2008 / Meadow & Kenoyer for Harappa and the
concordance; Bisht for Dholavira; Marshall 1931 / Mackay
1938 for Mohenjo-daro; Lal & Thapar for Kalibangan;
Rao 1979 for Lothal; Jarrige 1993 for Nausharo). Precedence:
a mapped period cell wins over a mapped phase cell;
disagreements counted as conflicts — **0 conflicts** in the
population. `chron_band` is constructed context, **Class
C** (§8.5); §8.6's condition (pre-declared, deterministic,
citable per cell) is met.

Notable unmapped classes (full register in the citation
register file): Harappa Vats-era `Stratum I–VII` phase
labels (837 rows — exactly Harappa's phase-only rows; no
correlation to the HARP periodization was citable);
Lothal `Layer N` period labels (105 rows); Mohenjo-daro
phase labels (never needed: every phase-informative
Mohenjo-daro row carries a period value); Harappa `2/3`
and `3/4` (band-spanning); Dholavira `5/6`, `5?`;
Nausharo `4` (no Period IV exists in Jarrige's scheme);
Chanhu-daro (no informative values in the layer at all).

**`chron_band` margins (F3 population):** early 85,
middle 1,774, late 408, UNRECORDED 3,143 — **recorded
2,267 (41.9%)**, exactly the §3.3 arithmetic bound.
Decomposition: 2,162 rows map through period cells and
105 through phase cells (all at Lothal, whose period cells
are layer numbers); the remaining 849 informative
chronology rows stay UNRECORDED because their cells are
unmapped (§3 above) — the harmonization recovers nothing
beyond the union the fields contain, as §3.3 predicted.
Per site (recorded): Harappa 1,024, Mohenjo-daro 803,
Kalibangan 158, Dholavira 137, Lothal 108, Nausharo 37,
Chanhu-daro 0.

## 4. Depth bands (T4, Q3(a))

Parse rules (documented in the audit script; categories
counted as margins): VALUE 2,684; SURFACE 50 (all at
Kalibangan; depth 0.0 in the site's primary unit group);
RANGE 10 (midpoint); DECIMAL_DOTDOT 9 (the layer's `X..Y`
notation read as decimal X.Y); UNITLESS 16; COLON_FT_IN 1
(`-4:0 ft`, feet:inches); UNPARSED 1; MISSING 2,639.
Bands are tertiles by rank **within (site × unit) groups**
of n ≥ 9 (8 groups banded; 5 rows in small groups left
UNRECORDED); 145 rows sit on tertile boundary ties (equal
values split across a band boundary by rank — disclosed,
not hidden). The bands are within-site **relative** by
construction; no absolute cross-site depth claim is made
anywhere (Q3 option (c) was rejected at adjudication as
indefensible from this file).

**`depth_band` margins:** shallow 924, middle 922, deep
919, UNRECORDED 2,645 — **recorded 2,765 (51.1%)**. Per
site (recorded): Mohenjo-daro 1,386, Harappa 1,055, Lothal
101, Dholavira 96, Chanhu-daro 70, Kalibangan 57, Nausharo
0.

## 5. Preservation

Collapse rule (original spellings retained per row in the
dataset): complete → complete; fragment → fragment;
chipped / slightly chipped / partly damaged → damaged;
`-`/blank → UNRECORDED. **Margins:** complete 3,046,
fragment 1,761, damaged 597, UNRECORDED 6 — **recorded
5,404 (99.9%)**, all 7 sites ≥ 30 recorded.

## 6. Gate application (T2) — verbatim

Frozen gate (§4.2 step 3; thresholds approved as drafted,
Q5): a candidate covariate is eligible iff (i) recorded
coverage ≥ 70% of the F3 population; (ii) ≥ 3 eligible
sites contribute ≥ 30 recorded inscriptions each;
(iii) permutable inscriptions under composition × covariate
strata (UNRECORDED retained as a stratum level) ≥ 1,000.

| covariate | recorded | coverage | sites ≥30 | permutable | (i) | (ii) | (iii) | classification |
|---|---|---|---|---|---|---|---|---|
| chron_band | 2,267 | 41.9% | 6 | 5,342 | FAIL | pass | pass | **SENSITIVITY** |
| depth_band | 2,765 | 51.1% | 6 | 5,406 | FAIL | pass | pass | **SENSITIVITY** |
| preservation | 5,404 | 99.9% | 7 | 5,404 | pass | pass | pass | **PRIMARY CONTROL** |

(Recorded-only permutable counts, for the record:
chron_band 2,199; depth_band 2,761; preservation 5,402.)

Routing rule (§4.2, adjudication amendment): both
gate-failing covariates route automatically to the
sensitivity panel (EXPLORATORY, reported as bounds, never
as the controlled verdict). Exactly one covariate passes,
so the primary strata are composition × that covariate.

## 7. Verdict (T5)

> **G1 is ESTIMABLE** under the §4.2 routing rule: exactly
> one covariate (preservation) passes the frozen
> eligibility gate, so the primary strata are composition
> (Phase-137 type class × length class) × preservation,
> with UNRECORDED retained as a stratum level.
> Gate-failing approved covariates route to the sensitivity
> panel (EXPLORATORY, reported as bounds, never as the
> controlled verdict). Chronology is NOT controlled in the
> primary test and must be named as an uncontrolled
> confounder in every G1 headline.

In plain terms: the F3 result's preservation confounder —
the one F2's falsifier showed can manufacture a repertoire
pattern unaided — **can** be controlled at 99.9% recorded
coverage. Its period confounder cannot (41.9%), and depth
cannot (51.1%); both become pre-declared exploratory
sensitivities rather than silent gaps. The freeze record
for Phase-140/141 is committed with this PR
(`specs/025-stage2-controlled-followup/phase139-freeze.md`),
naming the final strata, the seed (20261009), and the
decision thresholds (BH q = 0.05 over G1 alone, Q4(b);
§5 criterion for the LOSO members).

## 8. Publication note

Per adjudication Q6 and the executing instruction for
this run, publication rides with the Spec 025 outcome
record (G1 executed, or the NOT ESTIMABLE closeout) —
Phase-139 alone triggers no release.

## 9. Fence

No chi-square, odds ratio, permutation, or any other
association quantity was computed in this phase. The
audit code contains no association machinery; a unit test
pins the absence of any association key in the results
JSON.

**AI disclosure:** Produced by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution section VI.
