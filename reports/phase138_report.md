# Phase-138 Report — Graffiti Descriptive Protocol (Spec 024, Stage 2(d))

> **DESCRIPTIVE ONLY.** This arm computes counts, proportions,
> medians and interquartile ranges — nothing else. No test, no
> p-value, no inference was computed, and this arm is **not a
> member of the Stage 2 family** (freeze §1, §4). Graffiti
> material is never pooled with seal texts.

**Phase:** 138 · **Spec:** 024 §5.5 (arm (d)) · **Freeze:**
`specs/024-evidence-integration/stage2d-freeze.md` (FROZEN
2026-10-09, merged on `origin/main` at ad665b05 before any
Phase-138 code ran) · **Date of this report:** 2026-10-09 ·
**Results:** `reports/phase138_results.json` (computed by
`backend/scripts/phase138_graffiti_descriptive.py`, never
hand-written).

**AI disclosure:** this execution and this report were produced
by an AI agent (Muse Spark, via Muse) at the direction
of Tristen Pierson, per constitution §VI.

---

## 1. Mandatory statements (freeze §3)

- The Tamil Nadu graffiti corpus (tngraffiti.in) is **not in hand — 0 records** (access requested 2026-10-08; no reply on record). No number in this arm describes it.
- **Dating-gap caveat:** the Tamil Nadu graffiti material is
  separated from the Indus material by **≥ 1,000 years** on the
  published rebuttal of the continuity claims (the Harappa.com
  critique of Rajan & Sivanantham). Any resemblance ever noted
  across that gap is formal resemblance across a
  millennium-plus separation — nothing more. This caveat
  attaches to every comparative statement in this arm.
- A permitted output of this arm is **"resemblance described"**;
  a prohibited output is any continuity, descent, or survival
  claim (spec §5.5).

## 2. Population as run (freeze §2.1)

All Phase-124 catalogue rows (CISI Vols. 1–2) with
`object_type` exactly `Graffiti`; distinct objects are
volume-scoped (canonical key `cisi:v{volume}:{cisi_id}`).
Execution recomputed the population and it matches the freeze
§1 design audit exactly.

| Volume | Photo rows | Distinct objects |
|---|---|---|
| 1 | 119 | 100 |
| 2 | 298 | 295 |
| **Total** | **417** | **395** |

Inputs (local store, gitignored; paths and hashes recorded in
the results JSON): `cisi_vol1_catalogue.csv` sha256
`e0d698f991fbd7cf26c491a2b25906b422903a0e2a26ea7b8c690420ca51dc1e`;
`cisi_vol2_catalogue.csv` sha256
`e751244e2d51bda3181d98e56af691c0d24099d76d035b54f0888504204bc7d9`.

## 3. Distinct objects by catalogue site (freeze §2.2)

Site is a Class O field (as printed in the catalogue).
**Catalogue-selection caveat (freeze §5, D2):** these
distributions describe the catalogue's record of the objects,
which is a **publication-selection** of the excavated
material, not the excavated population itself. That caveat
applies to every site distribution in this report, including
the context table in §7.

Pooled:

| Site | Distinct objects |
|---|---|
| Harappa | 262 |
| Lothal | 44 |
| Mohenjo-Daro | 42 |
| Kalibangan | 26 |
| Banawali | 8 |
| *(no site printed)* | 8 |
| Rangpur | 3 |
| Amri | 2 |
| **Total** | **395** |

By volume — Vol. 1: Lothal 44, Kalibangan 26, Banawali 8,
Harappa 6, Mohenjo-Daro 6, no site 5, Rangpur 3, Amri 2
(total 100). Vol. 2: Harappa 256, Mohenjo-Daro 36, no site 3
(total 295).

## 4. Photo-rows-per-object distribution (freeze §2.3)

| Rows per object | Vol. 1 objects | Vol. 2 objects | Pooled objects |
|---|---|---|---|
| 1 | 82 | 292 | 374 |
| 2 | 17 | 3 | 20 |
| 3 | 1 | 0 | 1 |

The modal (most common) value is 1 row per object in both
volumes and pooled: most graffiti objects carry a single
photographed side/view in the catalogue.

## 5. `side` and `bis` values as printed (freeze §2.4)

`side` — pooled: `A` 412, `B` 4, `C` 1. By volume: Vol. 1
`A` 116, `B` 2, `C` 1; Vol. 2 `A` 296, `B` 2.

`bis` — pooled: *(empty)* 399, `yes` 18. By volume: Vol. 1
*(empty)* 103, `yes` 16; Vol. 2 *(empty)* 296, `yes` 2.

Values are recorded exactly as printed; nothing was recoded.

## 6. `motif_chapter` (freeze §2.5) — Class C field

`motif_chapter` is a **Class C field** (the CISI editors'
chapter organization), labeled as such here and in the results
JSON. As printed — spelling variants and heading strings
recorded, never cleaned (Phase-133 §6.4 discipline):

- Filled rows: **0 of 417** (filled rate **0.0**) — Vol. 1:
  0 of 119; Vol. 2: 0 of 298.
- Distinct values: **none** (the field is empty on every
  graffiti row in the catalogue as extracted).

That is the descriptive finding as found: the catalogue's
chapter organization, as extracted by Phase-124, assigns no
`motif_chapter` value to any Graffiti row.

## 7. Extraction-quality descriptors (freeze §2.6)

Median and interquartile range (IQR; inclusive quartiles) of
the catalogue's own extraction-quality fields, with
present-counts:

| Field | Present | Median | Q1 | Q3 | IQR |
|---|---|---|---|---|---|
| `caption_ocr_score` (pooled) | 417 | 0.943 | 0.928 | 0.957 | 0.029 |
| `caption_ocr_score` (Vol. 1) | 119 | 0.968 | 0.9425 | 0.981 | 0.0385 |
| `caption_ocr_score` (Vol. 2) | 298 | 0.9385 | 0.924 | 0.949 | 0.025 |
| `scale_pct` (pooled) | 332 | 100.0 | 50.0 | 100.0 | 50.0 |
| `scale_pct` (Vol. 1) | 38 | 100.0 | 50.0 | 100.0 | 50.0 |
| `scale_pct` (Vol. 2) | 294 | 100.0 | 50.0 | 100.0 | 50.0 |

These describe the catalogue extraction itself, not the
objects' archaeology.

## 8. Context table (freeze §2.7) — catalogue composition only

> **Label (verbatim in effect from the results JSON):**
> catalogue-composition description only — the graffiti
> subset's catalogue shape read against the corpus it sits
> in. This is **not a comparison of repertoires** and
> licenses no inference. Graffiti rows are never pooled with
> seal or tablet rows in any joint repertoire. The §3
> catalogue-selection caveat (publication-selection, freeze
> §5 D2) applies here as in §3.

Distinct objects by site (pooled volumes):

| Site | Seals | Tablets |
|---|---|---|
| Mohenjo-Daro | 1,057 | 362 |
| Harappa | 551 | 479 |
| *(no site printed)* | 170 | 3 |
| Lothal | 124 | 0 |
| Kalibangan | 65 | 16 |
| Banawali | 22 | 6 |
| Jhukar | 15 | 0 |
| Desalpur | 7 | 0 |
| Rojdi | 4 | 0 |
| Surkotada | 1 | 0 |
| **Total distinct objects** | **2,016** | **866** |
| **Photo rows** | **4,778** | **2,180** |

Rows-per-object distribution (pooled): Seals — 1: 195,
2: 1,229, 3: 318, 4: 220, 5: 41, 6: 8, 7: 3, 8: 1, 9: 1.
Tablets — 1: 35, 2: 546, 3: 141, 4: 112, 5: 12, 6: 18, 7: 2.
By-volume rows/objects and site tables are in the results
JSON.

## 9. Kodumanal — qualitative paragraph (freeze §2.8)

The Kodumanal volume is a trench-organized excavation report
whose Graffiti Marks section describes marks by ware and by
vessel position (shoulder near the rim), and as pre-firing vs
surface marks (Phase-133 Stage 0 report §6.1). Its printed
tallies are quoted as prose only, with their internal
inconsistency stated: the section states "Out of 175 graffiti
marks 75 in Black and Red ware, 70 Red ware, 70 Russet Coated
ware and 10 Black ware were noticed" — subtotals summing to
225 against a stated 175 — and separately that "41 Brahmi
sherds were observed and 99 Graffiti marks were collected".
**No tally from the volume is used as a count anywhere in
this arm.** The §1 dating-gap caveat attaches to any
comparative reading of this material: a permitted output is
"resemblance described"; continuity, descent, or survival
claims are prohibited.

## 10. What was NOT computed (freeze §4)

- No association test, significance statement, or p-value, in
  any form.
- No pooling of graffiti rows with seal or tablet texts in
  any table presenting itself as a joint repertoire.
- No overlap statistic against the seal-text sign repertoire:
  **no machine-readable sign-form repertoire of the catalogue
  graffiti objects exists in hand** (the catalogue records
  photographs and captions, not transcriptions; Phase-132
  closed the program's attempt to manufacture transcriptions
  from plates). The §5.5 sketch's "overlap and distribution
  statistics" are therefore not computable from material in
  hand; the freeze narrowed the arm to the descriptives of §2
  rather than substituting another layer's transcriptions
  under the graffiti label.
- No continuity, descent, or survival claim.

## 11. Deviations

None. Execution followed the freeze as written; the
recomputed population matched the freeze §1 design audit
(417 rows; Vol. 1: 119, Vol. 2: 298; 395 distinct
volume-scoped objects) with no discrepancy to resolve.

## 12. Epistemic fences (spec 024 §8)

This arm produces description only. Per spec 024 §8 and
freeze §5: associations describe use, not meaning — and this
arm computes no associations at all. No result in this arm
can support any claim about what graffiti marks mean, whether
they are writing, or how they relate historically to the
Indus script; it cannot mint, promote, demote, or validate
any sign reading, change any anchor's status, or move
PRED-2026 in either direction. Anything this description
suggests is hypothesis-grade and waits for genuinely
independent data and a registered test.

## 13. Deliverables and disposition

- Script: `backend/scripts/phase138_graffiti_descriptive.py`
  (deterministic; input paths + sha256 recorded in the
  results JSON).
- Graph module: `backend/glossa_lab/experiment_graph_phase138.py`
  (node `IndusPhase138GraffitiDescriptive`), registered in
  `experiment_graph.py` (try/except, Phase-133/134 pattern)
  and verified registered **before** the run.
- Tests: `backend/tests/test_phase138_graffiti_descriptive.py`
  — committed-JSON internal consistency, absence of any
  p-value / test-statistic keys, mandatory statements,
  median/IQR unit tests, and a recomputation test that skips
  cleanly when the local-store inputs are absent.
- Results: `reports/phase138_results.json`; this report.
- No anchor changes: anchors sha256
  `eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86ebb1fa3b602cfaed`
  asserted unchanged in the Phase-138 tests. No PRED
  evaluation was run or implied. No publication, external
  send, or outreach of any kind was made.
