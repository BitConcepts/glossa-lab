# Spec 027 Stage 0 — Gazetteer + Chronology Spine (CC BY 4.0 package)

Prepared under Spec 027 Ask 4 (owner adjudication, 2026-10-11):
CC BY 4.0 publication through the program release gate for
lawfully reusable rows only. **This package is deposit-ready;
no deposit has been made.**

## Contents

- `indus_gazetteer_stage0_ccby.csv` — source-asserted
  settlement gazetteer rows whose licence state is
  `verified_open` (XRONOS site assertions, CC BY 4.0).
  Derived from `data/movement/gazetteer_rows.jsonl` by the
  Phase-391 build (`backend/scripts/phase391_stage0_spine.py`);
  derivation is recorded in
  `specs/027-movement-culture-language/stage0-freeze.md`.
- `indus_chronology_spine_stage0_ccby.csv` — traced
  radiocarbon rows from verified-open sources only: XRONOS
  (CC BY 4.0) and Mutin et al. 2025 Supplementary Information
  Table S2 (CC BY 4.0), the latter flagged
  `scenario = CONTESTED` on every row. Derived from
  `data/movement/chronology_rows.jsonl` by the same build.
- `source_register.json` — the Stage 0 source register,
  verbatim from `data/movement/source_register.json`,
  including the sources that are catalogued only
  (Possehl, Law, TwoRains, c14bazAAR) and the licence
  evidence for every state.

## Exclusions (by rule, not by omission)

- CISI-catalogue-derived gazetteer rows are
  `open_access_read_only` (factual assertions from
  in-copyright published volumes) and are **excluded** from
  this CC BY package. They remain in the repository data
  products with their licence state recorded per row.
- Catalogue-only and permission-required sources contribute
  no rows under any circumstances (Spec 027 adjudication,
  Ask 4).
- No coordinate in this package is more precise than its
  source published it.

## Attribution

XRONOS (xronos.ch), CC BY 4.0. Mutin, B. et al. (2025),
Scientific Reports, DOI 10.1038/s41598-025-92621-5, CC BY
4.0 — cited with its chronology scenario status CONTESTED
(unreplicated revision; see the Stage 0 report,
`reports/phase391_stage0_report.md`, for the coverage and
fitness statements that bound this data).

Gazetteer/spine construction: Glossa Lab (BitConcepts),
Spec 027 Stage 0 (Phase-391), 2026-10-11.
