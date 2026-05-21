# Data Attribution and License Compliance

All materials in `research/indus/` are released under **CC BY 4.0**
(see `LICENSE-CC-BY-4.0`). This document records the upstream data sources,
their licenses, and how they are used in the released outputs.

---

## Source data dependencies

| Source | License | Used in | How |
|--------|---------|---------|-----|
| **Holdat LLC Indus Corpus v3** (Miller 2025) | Proprietary — not publicly available | All released outputs | Statistical analysis only; no raw corpus data committed or released |
| **Mahadevan 1977** — M-number sign system | Public domain (ASI / Govt. of India) | anchor_table, all phase reports | Sign numbering conventions (M001–M397); no text reproduction |
| **DEDR** (Burrow & Emeneau 1984) | © Clarendon Press — reference use | anchor_table (DEDR column) | DEDR entry numbers cited as phonetic evidence; no verbatim text |
| **Parpola 1994 / 2010** | © CUP / open conference paper | anchor_table, iconographic_formula_pairs.csv | Phoneme map cross-validation (44/75 HIGH readings compared); no text reproduced |
| **Laursen 2010** | © Wiley / AAE journal — reference use | phase127, phase156 | Gulf seal catalog mined for fish-sign occurrences; no text reproduced |
| **Nair 2026** (arXiv:2604.17828) | CC BY / arXiv | phase_reports (external validation) | Independent replication study cited; not included in outputs |

---

## Data files committed to this repository

### Files with third-party data content

| File | Location | License | Attribution required |
|------|----------|---------|----------------------|
| `epsd2_names_subset.json` | `backend/glossa_lab/data/` | **CC BY-SA** (ePSD2, Penn) | Yes — any work using this file must also be CC BY-SA |
| `mahadevan_2003_tamil_brahmi.json` | `backend/glossa_lab/data/` | © HUP / Cre-A — **fair use** | Reference-only; not for redistribution |
| `mahadevan_2003_tb_names.json` | `backend/glossa_lab/data/` | © HUP / Cre-A — **fair use** | Reference-only; not for redistribution |
| `mahadevan_parpola_crosswalk*.json` | `backend/glossa_lab/data/` | Derived — © Mahadevan/Parpola/CUP | Reference-only crosswalk; not for redistribution |
| `parpola_phonemes.json` | `backend/glossa_lab/data/` | Derived — © Parpola/CUP | Reference-only; not for redistribution |
| `cisi_findspots.json` | `backend/glossa_lab/data/` | Derived from CISI — © Suomalainen Tiedeakatemia | Reference-only; not for redistribution |
| `iconographic_anchors.json` | `backend/glossa_lab/data/` | Derived from Parpola 2010 (open) + CISI (©) | Reference-only for CISI portions |
| `indus_cisi_corpus.json` | `data/`, `data/raw/` | Derived from CISI — © Suomalainen Tiedeakatemia | Research pipeline use only; not for redistribution |
| Rigveda corpus (`rv*.txt`) | `data/` | Public domain (ancient text) | Free to use |
| `mahadevan_m77_raw.txt` | `data/`, `data/raw/`, `data/import/` | © Internet Archive upload, original ASI (Govt. of India, public domain) | Attribution required |

### Glossa-Lab generated data (no third-party restrictions)

| File | License |
|------|---------|
| `backend/glossa_lab/data/dravidian_tamil_lm.json` | MIT — Glossa-Lab generated from DEDR + Sangam literature (public domain sources) |
| `backend/glossa_lab/data/dravidian_syllabic_lm*.json` | MIT — Glossa-Lab generated |
| All `backend/glossa_lab/experiments/graphs/*.json` | MIT — Glossa-Lab experiment definitions |

---

## Key license concerns and status

### ePSD2 (CC BY-SA) — ⚠️ ShareAlike
`backend/glossa_lab/data/epsd2_names_subset.json` is CC BY-SA. The ShareAlike clause
means any work that incorporates this file must also be CC BY-SA.

**Status: HANDLED** — The ePSD2 data was used only for Phase-28/29 Meluhhan name
matching experiments (all of which produced null results). None of the released
research outputs (`anchor_table`, `phase_reports`, supplemental CSVs) incorporate
ePSD2 data. The CC BY 4.0 license on `research/indus/` is therefore valid.

The `epsd2_names_subset.json` file has an explicit `_license: "CC BY-SA"` header.
Users who incorporate that file in derivative works must comply with CC BY-SA.

### CDLI (CC BY-NC-SA 3.0) — ⚠️ Non-commercial
CDLI tablets were consulted for Phase-22 Meluhha corpus research. No CDLI tablet
text data is committed to this repository. All CDLI references are bibliographic only.

**Status: CLEAN** — No CDLI data in the committed codebase.

### Copyrighted academic books (CISI, Parpola 1994, Mahadevan 2003)
Several JSON files in `backend/glossa_lab/data/` are derivative compilations from
copyrighted publications. These are labeled "reference use only" and are used
exclusively in the internal research pipeline. They are not included in the
`research/indus/` public release.

**Status: FAIR USE** — Academic research use of these derivations is defensible
under fair use / fair dealing. The files contain no verbatim text reproduction,
only structured analytical data (sign numbers, phoneme assignments, crosswalk
mappings).

### Holdat LLC Indus Corpus v3 (proprietary)
The primary corpus is not in this repository and is not redistributed. The
released anchor table and phase reports are statistical derivatives (sign
frequency counts, positional probabilities, candidate readings), not raw corpus data.

**Status: CLEAN** — No proprietary corpus data committed.

### PyMuPDF / fitz (AGPL)
PyMuPDF is listed as a dependency for OCR research scripts. It is not imported
in the deployed backend application (`backend/glossa_lab/`), only in standalone
research scripts. AGPL network-use requirements do not apply.

**Status: CLEAN** — AGPL library not in the deployed service code.

---

## Summary: Released outputs are license-clean

The files in `research/indus/` (preprint PDF, anchor table, phase reports,
supplemental CSVs) are all either:
1. Glossa-Lab original analysis (CC BY 4.0 ✅), or
2. Statistical derivatives of the Holdat corpus not subject to redistribution
   restrictions since no raw corpus data is included (CC BY 4.0 ✅)

No CC BY-SA, CC BY-NC, or proprietary data appears in the released outputs.

---

*Last reviewed: 2026-05-21. Maintained by Tristen Kyle Pierson / BitConcepts LLC.*
*Open an issue at https://github.com/BitConcepts/glossa-lab for corrections.*
