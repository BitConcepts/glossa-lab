# Phase-140 Report — Spec 025: G1, the controlled F3 re-test — ICIT-lineage layer (horus84); preservation recorded coverage 99.9%; chronology is NOT controlled in the primary test

**Test G1 (confirmatory, frozen):** the Phase-137 F3
site-repertoire test re-run on the **ICIT-lineage layer
(horus84)** population (5,410 inscriptions, 7 sites),
with site labels permuted **within composition
(Phase-137 type class × length class) × preservation
strata** — the primary-control set is exactly
{preservation}, whose recorded coverage on this
population is **99.9%** (5,404 of 5,410; 6 rows carry
preservation as UNRECORDED, retained as a stratum
level). **Chronology is NOT controlled in the primary
test: period/phase (chronology) remain uncontrolled
confounders.** The pre-declared sensitivity panel —
S-chron (composition × chron_band) and S-depth
(composition × depth_band), both EXPLORATORY — is
reported alongside in §4, never as the controlled
verdict.

**Verdict, as found: G1 is SUPPORTED under control.**
Observed χ² = 4,966.36; under the controlled
permutation null (B = 9,999, seed 20261009), **0 of
9,999 permutations** reached the observed statistic
(null median 2,684.74; 95th percentile 2,859.30), so
the raw permutation p = **0.0001**. Per adjudication
Q4(b), Benjamini–Hochberg is applied over G1 alone at
q = 0.05; with m = 1 the adjusted value equals the raw
p (0.0001 ≤ 0.05) — stated plainly: this is not a
family correction across the LOSO members. §8's
limits bind the reading: the result is co-occurrence
structure in the recorded data of this labeled lineage
layer; compilation-internal explanations (transcription
and compilation practice within one scholarly
tradition) remain live alternatives; no meaning claim
is made or implied.

Design: `specs/025-stage2-controlled-followup/spec.md`
(§4, §11), `phase139-freeze.md`, `phase140-freeze.md`.
Execution: `backend/scripts/phase140_g1_controlled.py`;
machine-readable results:
`reports/phase140_results.json`.

## 1. Population and join (reproduced by rule, asserted)

The Phase-137 F3 population was reproduced from the
layer (sha256
`c368f290d8d784093d804243100de27ae6ad09df3ae37cab7432a0205d4ec9ef`,
consumed read-only) by the frozen rule — sites with
≥ 30 inscriptions and ≥ 100 parsed tokens (Chanhu-daro
74, Dholavira 238, Harappa 2,717, Kalibangan 212,
Lothal 208, Mohenjo-daro 1,923, Nausharo 38), rows with
≥ 1 parsed token: **5,410 inscriptions**, 19,051 parsed
tokens, 17,257 profile tokens; profile table 7 × 187
(186 signs at layer-wide count ≥ 10, plus OTHER;
placeholders `000`/`999` excluded from profiles). All
reproduction quantities were asserted equal to the
committed Phase-137 F3 record before any permutation
ran. Covariates were joined from the committed
Phase-139 harmonized dataset on the layer's unique
`id` column: **5,410 of 5,410 rows joined**, and the
dataset's `composition_stratum` agreed with the
stratum computed from the layer for every row
(asserted).

## 2. Pre-run regression (freeze §5) — exact

Before the controlled configurations were accepted,
the machinery ran in the uncontrolled configuration
(composition-only strata — the Phase-137 F3
configuration) on the same population and reproduced
the committed Phase-137 F3 result **exactly**: observed
χ² 4,966.362228365138; 0 of 9,999 permutations ≥
observed; null median 2,667.87; p95 2,844.61; raw
p = 0.0001; permutable N 5,410 of 5,410. Comparability
of the controlled runs to F3 is therefore mechanical,
not assumed.

## 3. G1 — the controlled test

Permutation within composition × preservation strata:
**53 strata**; permutable (effective) N = **5,404 of
5,410** (the Phase-139 projection exactly; the 6
non-permutable rows are six singleton single-site
strata — 4 preservation-UNRECORDED rows and 2
`damaged` POT rows at Harappa; all are counted in the
results JSON's strata table, none dropped silently).

| Quantity | Value |
|---|---|
| Observed χ² (site × sign profile) | 4,966.36 |
| Null median (controlled) | 2,684.74 |
| Null 95th percentile | 2,859.30 |
| Permutations ≥ observed | 0 / 9,999 |
| Raw permutation p | 0.0001 |
| BH (G1 alone, m = 1, q = 0.05) | 0.0001 → **SUPPORTED under control** |
| Cramér's V (descriptive) | 0.2190 |
| Permutable N / nominal N | 5,404 / 5,410 |

Per-site total-variation distances to the pooled
profile (descriptive, unchanged from F3 — the observed
table is the same table; control acts on the null):
Nausharo 0.426, Chanhu-daro 0.349, Kalibangan 0.301,
Lothal 0.292, Dholavira 0.240, Harappa 0.165,
Mohenjo-daro 0.127.

**Sparsity disclosure (mandatory):** 1,309 cells;
887 cells (67.8%) with expected count < 5 under
independence; minimum expected count 0.075; per-site
profile tokens 325 / 637 / 7,168 / 508 / 681 / 7,809 /
129 (Chanhu-daro / Dholavira / Harappa / Kalibangan /
Lothal / Mohenjo-daro / Nausharo). As in Phase-137, the
χ² is used as a divergence statistic with inference
only by permutation; the asymptotic distribution is
not invoked anywhere.

**Reading, with the rider attached:** controlling
preservation — the one covariate that passed the
frozen Phase-139 gate — moves the permutation null
median from 2,667.87 (composition only) to 2,684.74
and does not bring any of 9,999 controlled permutations
to the observed statistic. On this layer, differential
preservation as recorded (complete / fragment /
damaged) does not account for the site-repertoire
association. **Chronology remains uncontrolled**: this
verdict is about preservation control only, and
period/phase differences across sites remain a live
alternative explanation, bounded — not settled — by
the EXPLORATORY S-chron sensitivity below.

## 4. Sensitivity panel (EXPLORATORY — bounds, never the verdict)

Same statistic, B, seed, and p formula; permutation
within composition × the named covariate's strata
(UNRECORDED retained as a level in both).

| Sensitivity | Recorded coverage | Permutable N | Strata | Null median | Null p95 | Perms ≥ obs | Raw p |
|---|---|---|---|---|---|---|---|
| S-chron (composition × chron_band) | 2,267 / 5,410 (41.9%) | 5,342 | 59 | 2,809.53 | 2,977.83 | 0 / 9,999 | 0.0001 |
| S-depth (composition × depth_band, within-site tertiles) | 2,765 / 5,410 (51.1%) | 5,406 | 63 | 2,682.78 | 2,851.01 | 0 / 9,999 | 0.0001 |

Read as bounds only: under the chronology-stratified
exploratory null — which constrains permutations
within harmonized period bands where recorded (41.9%
coverage; the unrecorded 58.1% permute within
UNRECORDED strata) — the null median rises to 2,809.53
and still no permutation reaches the observed
4,966.36. Under the depth-stratified exploratory null
the picture is the same (median 2,682.78). These
bounds say the association is not an artifact of the
recorded parts of either covariate under their
strata; they do **not** convert chronology into a
controlled variable, and no verdict word attaches to
either row. The harmonized covariates are constructed
context (Class C); their citations (Phase-139 citation
register) and coverage travel with these numbers.

## 5. Process record

- Graph-first (H15/H23): node `IndusPhase140G1Controlled`
  registered in `backend/glossa_lab/experiment_graph.py`
  (module `experiment_graph_phase140.py`) and verified
  before the run.
- Anchors asserted byte-identical before and after the
  run (sha256
  `eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86ebb1fa3b602cfaed`);
  the layer file was hash-asserted and consumed
  read-only.
- Determinism: the full configuration set re-executes
  from the seeded streams; the phase test file's
  recomputation test (local-store inputs present)
  re-runs the script and compares the committed
  permutation records exactly.
- Deviation (recorded, resolved by rule): the first
  launch of the execution script aborted on its own
  layer-hash assertion before any computation — the
  sha256 constant in the script had been mis-split
  across a line break, dropping one hex digit. The
  constant was corrected to the file's true hash
  (verified against the file and the Phase-139 record),
  and the run was relaunched; no design quantity was
  affected. The assertion did its job: nothing ran
  against an unverified input.
- No anchor was minted, promoted, demoted, or
  validated; no output of this phase is an input to
  PRED-2026-001/002/003; Class I fields entered
  nothing.

**AI disclosure:** produced by an AI agent (Muse
Spark, via Muse) at the direction of Tristen
Pierson, per constitution §VI.
