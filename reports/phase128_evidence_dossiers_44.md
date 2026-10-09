# Phase-128 — Integrated Evidence Dossiers for the 44 Pending Anchors

**Status:** descriptive synthesis. **Date:** 2026-10-08. **Phase:** 128.

**Framing (hard).** This report and its companion files join, per anchor, the Phase-120–127 evidence records that exist for the 44 `pending_non_sa_validation` anchors in `backend/reports/INDUS_FINAL_ANCHORS.json` (sha256 `eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86ebb1fa3b602cfaed`, read-only, unchanged). They are **descriptive only**: they contain no status recommendation, no adjudication, and no prediction (PRED) content. Where a source has no record for a sign, the dossier records the field as NOT-COVERED/missing; nothing is inferred to fill a gap.

**Artifacts.**

- Dossiers (JSON): `reports/phase128_evidence_dossiers_44.json`
- Dossiers (CSV, flat rendering): `reports/phase128_evidence_dossiers_44.csv`
- Builder: `backend/glossa_lab/phase128_dossiers.py` + `backend/glossa_lab/phase128_run.py`; entry `backend/scripts/phase128_evidence_dossiers.py`
- Tests: `backend/tests/test_phase128_evidence_dossiers.py`

## 1. Sources joined (per anchor, on M-number)

| Source | Per-sign content carried into the dossier |
|---|---|
| Anchor file | reading, confidence, basis, source, validation_status |
| Phase-120 Bhaskar triage (`reports/phase120_bhaskar_triage_44.{md,json}`) | classification (CONTESTED / NOT-COVERED), subflag, detail, mention sources, case ids |
| Phase-123 Wells witness (`data/crosswalks/wells_segmentation_witness_v1.*`; memo `reports/phase123_wells_segmentation_witness.md`) | treatment (SAME / SPLIT / MERGE / NOT-COVERED / INDETERMINATE), Wells graphemes, correspondence method, thesis source, hand-verification, implication note |
| Phase-126 (`reports/phase126_wells_split_candidates*`) | class vocabulary only (unit-same / split / merge / not-covered / indeterminate), applied as a label normalisation of the Phase-123 raw treatment; Phase-126's own analysis set was the 113 CANDIDATE anchors, so no Phase-126 record exists for any pending sign |
| Phase-122 crosswalk v1 (`data/crosswalks/parpola_mahadevan_crosswalk_v1.*`; memo `reports/phase122_crosswalk_mayig.md`) | every P↔M row asserted for the M-sign: Parpola id(s), relation type, confidence, conflict flag + detail, sources |
| Phase-125 (`reports/phase125_cross_compilation_results.json`) | PRIMARY-arm record per sign (paired Parpola id, token counts, profiles, TV/W1) and judgeability |
| Phase-127 (`reports/phase127_cross_compilation_diagnostic.md` + results JSON) | per-pair diagnostic values (bootstrap CI, split-half, matched-size, crosswalk decomposition) — these exist only for the 16 PRIMARY judgeable pairs; global diagnostic values are recorded once in the JSON (§4) |
| Spec 020 (`specs/020-soviet-pred-adjudication`) | uniform limitation field on every dossier (§5) |

Join integrity: **44 anchors in = 44 dossiers out** (asserted in code and in tests). Crosswalk coverage: 43/44 signs have ≥1 crosswalk row (M281 has none and is recorded NOT-COVERED there). Phase-125 PRIMARY records exist for 36/44 signs (the PRIMARY arm carries only high-confidence crosswalk pairs); 8 signs are recorded NOT-COVERED for Phase-125.

## 2. Bucket rules (stated before membership)

Derived per-anchor predicates over the dossier fields:

- `wells_determinate` — Wells treatment ∈ {SAME, SPLIT, MERGE}
- `wells_contested` — Wells treatment ∈ {SPLIT, MERGE} OR Wells hand-verification == `discrepancy`
- `cw_present` — ≥1 crosswalk v1 row for the M-sign
- `cw_conflict` — any crosswalk v1 row for the M-sign has conflict == true
- `p125_present` — the sign appears in the Phase-125 PRIMARY records
- `p127_present` — the sign is the M-side of one of the 16 Phase-125 PRIMARY judgeable pairs (a Phase-127 per-pair record exists)

Rules:

1. **evidence-complete** — `wells_determinate` AND `cw_present` AND `p125_present` AND `p127_present`.
2. **segmentation-contested** — `wells_contested`.
3. **crosswalk-contested** — `cw_conflict`.
4. **not-covered** — Bhaskar classification == NOT-COVERED AND Wells treatment ∈ {NOT-COVERED, INDETERMINATE} AND NOT `p125_present` AND NOT `p127_present`.
5. **evidence-thin** — the defined residual: in none of buckets 1–4.

**Multi-membership (explicit).** Buckets 1–4 are independent predicates: an anchor may sit in several of them at once, and §3 lists it under each. Bucket 5 is exclusive of buckets 1–4 by construction (it is exactly the residual). Every anchor is in at least one bucket.

## 3. Bucket membership (exact)

### evidence-complete — 1

M072

### evidence-thin — 10

M183, M223, M235, M262, M270, M272, M304, M355, M365, M416

### segmentation-contested — 15

M011, M028, M102, M103, M155, M168, M169, M178, M237, M254, M293, M332, M345, M383, M402

### crosswalk-contested — 25

M011, M021, M024, M028, M031, M035, M036, M040, M058, M071, M072, M102, M103, M127, M149, M153, M155, M168, M169, M177, M239, M293, M350, M401, M412

### not-covered — 3

M033, M058, M281

## 4. Phase-127 diagnostic weight (global, recorded once)

The Phase-127 diagnostic is a property of the 16-pair judgeable set, not of individual pending anchors (only one pending anchor, M072, is in that set). Its global findings, carried into the JSON dossiers document verbatim: matched-size sampling at mayig token counts gives an expected median TV of 0.082613 (95% 0.046665–0.131316); 0.0 of 999 replicates reach the observed Phase-125 median TV of 0.636931 — matched-size sampling explains ~0 of the observed median TV. The inscription-bootstrap 95% CI for the median TV is 0.548638–0.722042. The Holdat split-half noise floor is 0.059538 (full-size estimate 0.0421). The Phase-125 verdict of record (FAIL — DISAGREEMENT) is final and unchanged by Phase-127 and by this phase.

## 5. The spec-020 limitation (uniform field)

Every dossier carries the same limitation field: `NOT-EVALUABLE-VIA-SOVIET-DATASET`. Spec 020 adjudicated the Soviet positional dataset (Phase-121, Kondratov 1965) non-qualifying as an evaluation source for PRED-2026-001/002 (verdict NO, spec.md §5). The Soviet route therefore cannot evaluate these anchors' predictions. This is recorded as a uniform limitation on the dossier set, not as per-sign evidence about any anchor.

## 6. What this dossier cannot do

- **Bhaskar covers 1 of 44.** The Phase-120 triage records 43 of the 44 anchors as NOT-COVERED by Bhaskar (2024); only M402 carries a documented contest (case BH-D10, a coverage gap: the left-waving frontal form on K-39 has no counterpart in any compilation's inventory of 402). For the other 43, the dossier records an absence, not a concordance — the triage never infers agreement from silent use.
- **The Phase-125 judgeable subset is small.** Of 286 PRIMARY cross-compilation pairs, 16 are judgeable; of the 44 pending anchors, exactly one (M072, paired P058) is among them. For the other 43 anchors there is no judgeable cross-compilation measurement, and the dossier manufactures none.
- **The Soviet route is closed.** Per spec 020 (§5 above), the one additional evaluation source examined by this program cannot evaluate these anchors' predictions.
- **A dossier is not a verdict.** These files assemble what each source records about each sign, with provenance. They weigh nothing against anything else, and no anchor's status, reading, or confidence is changed, recommended, or implied by anything here.

**AI disclosure:** executed by an AI agent (Muse Spark, via Muse) at the direction of Tristen Pierson, per constitution §VI.
