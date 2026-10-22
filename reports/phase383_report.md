# Phase-383 — C4 Rescoring of the Coding Pilots (Spec 026 Rerun)

**Rerun of:** Phases 132, 134, 135 (register rows PHASE-132 /
PHASE-134 / PHASE-135; SPEC-023 / SPEC-024 in part).
**Contract:** `specs/026-rcph-framework-transfer/reruns/
phase383-contract.md`, freeze digest `e94575c78f8e7a87…`
(verified on the execution tree before the run).
**Type:** C4 — rescoring from the complete on-disk coding
records. NO re-coding was performed. Headline statistics were
recomputed with the ORIGINAL metrics modules
(phase132/134/135_metrics, imported) and asserted equal to the
committed metrics JSONs before any new quantity was computed.
**Results:** `reports/phase383_results.json` (B = 9,999
bootstrap resamples over objects, seed 20261011).

## Original vs rerun

| Pilot | Original (verbatim) | Recomputed from records | New: bootstrap 95% CI |
|---|---|---|---|
| 132 | exact-seq agreement all-50 (P) **0.20**; per-token 0.4798 | 0.20; 0.4798 — exact match | exact-seq **[0.10, 0.32]**; per-token **[0.409, 0.556]** |
| 134 | agreement **0.84**, κ **0.7885**; ILLEGIBLE per-category 0.667 | 0.84, κ 0.788472; ILLEGIBLE 0.667 — exact match | agreement **[0.77, 0.91]**; κ **[0.689, 0.878]** |
| 135 | agreement **0.78**, κ **0.7129**; ILLEGIBLE per-category 0.368 | 0.78, κ 0.712869; ILLEGIBLE 0.368 — exact match | agreement **[0.70, 0.86]**; κ **[0.606, 0.819]** |

Same/different: **every original point value reproduces
exactly** from the on-disk records — the pilots' arithmetic
was sound. What the framework adds is (a) the intervals the
originals lacked and (b) the origin-group accounting below.

## Origin-group audit (framework correction)

All coding roles in all three pilots (pass A, pass B, gold,
adjudicator) were executed by AI agents of ONE model family
(Muse Spark, via Muse), as the pilots themselves
disclose. Effective independent coder origin groups = **1**.
The agreement statistics therefore measure **intra-origin
consistency**, not independent corroboration; any downstream
reading of 0.84/0.78 as two-coder reliability in the usual
sense is superseded by the Phase-383 historical assessment
(Spec 026 S5).

## Verdicts (Spec 026 taxonomy; each pilot's own frozen gates)

- **Phase-132: CONTRADICTED** (bounded claim: this AI coding
  basis at this protocol can produce a publishable keyed
  transcription layer). The frozen stop-rule fired at 0.20 vs
  the 0.80 floor; the bootstrap CI [0.10, 0.32] sits far below
  the floor — the failure is not sampling noise.
- **Phase-134: INCONCLUSIVE.** Proceed gate unmet (0.84 <
  0.85; κ 0.7885 ≥ 0.75), stop rule unfired — the middle band,
  as originally reported. Adjudication of the original
  report's "missed the proceed gate by one object" framing:
  the agreement CI [0.77, 0.91] **reaches 0.85**, so the
  near-miss characterization **cannot be excluded on sampling
  grounds** — but the gate is a fixed decision rule on the
  point estimate, so the original middle-band outcome stands
  unchanged. The CI spanning the gate is itself the finding:
  a 100-object pilot cannot resolve a 0.01 margin.
- **Phase-135: INCONCLUSIVE.** Same structure (0.78 / κ 0.7129;
  CIs span both gates' neighborhood).

No anchor implications. No finding of the originals is
overturned; two are re-anchored with intervals, and the
reliability interpretation of all three is narrowed by the
origin-group audit.
