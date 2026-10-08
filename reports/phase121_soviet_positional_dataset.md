# Phase-121 — Soviet Positional Dataset: Extraction Memo

**DESCRIPTIVE DATASET ONLY — NO PREDICTION SCORED, NO ANCHOR VALIDATED**

Date: 2026-10-08. Sources are in-copyright research copies held
locally; only tables/counts (data) were extracted. No page images
and no text passages from either volume are committed to this repo.

## Sources

- **Zide & Zvelebil (eds) 1976**, *The Soviet Decipherment of the
  Indus Valley Script* (Mouton, Janua Linguarum Series Practica
  156) — English translations of the Soviet reports. The scan's
  bundled djvu OCR is unusable (wrong-script recognition) and was
  ignored. The PDF itself carries a usable publisher text layer,
  which was cross-checked against fresh OCR and visual reads.
- **Proto-Indica 1973** (Russian, Nauka, Moscow; imprint 1975),
  ed. Yu. V. Knorozov — scan with an embedded Acrobat OCR layer of
  mixed quality (Cyrillic body text broadly readable, diacriticised
  transliteration unreliable). Assessed, not trusted blindly: every
  extracted value was read visually off the rendered page.

## Tables located

### 1965 Preliminary Report — Kondratov, positional-statistical analysis

| id | printed p. | table | rows |
|---|---|---|---|
| K1965-T1 | 40 | Table 1, "Frequency of increase of new signs" — rows: cumulative text length in signs (25…1400 by 25); columns: new sign types first appearing per increment, Egyptian control vs Proto-Indian ("India") | 56 |
| K1965-T2 | 41 | Table 2, "Different classes of signs" — rows: sign frequency class (share of total absolute frequency, %); columns: Egyptian (n signs 195, frequency sums and functional shares, %) and India (morphology / determinatives / numerals shares %, n signs 315, frequency sum %) | 11 (incl. printed Total) |
| K1965-T3 | 43 | Table 3, "Polygrams of the hieroglyphic texts" — two stacked sub-tables (Egyptian, Proto-Indian); rows: total / genuine / errors and their % / relative-frequency forms, plus Egyptian referent breakdown; columns: polygram length 2–9 + total | 21 |
| K1965-T4 | 47 | Table 4, "Stable initials … in combination with stable finals" — rows: 8 stable-initial sign pairs (Marshall numbers; 232 subsumes 126, allographs per the printed note); columns: stable finals 87, 124, 68, 96, 97, the pair-final headed "87—", 66; cells: absolute frequencies; printed dash = no occurrence, encoded 0; plus the printed Total row | 9 (8 + printed Total) |

Sign coverage (K1965-T4, the only per-sign table): initial signs
99, 160, 232, 233 with second elements 118, 500, 501, 507;
final signs 66, 68, 87, 96, 97, 124. K1965-T2 covers the full
sign inventories in aggregate (315 Proto-Indian / 195 Egyptian
signs by frequency class) but names no individual signs.

### 1968 Brief Report — Knorozov, "The Formal Analysis of the Proto-Indian Texts" (printed pp. 97–112)

**Finding: there are no frequency or positional tables in the
1968 report.** It was searched in full: the report is prose plus
sign-glyph illustrations (segmented-inscription specimens,
circumgraph lists, pictorial sign identifications). Glyph forms
are not numeric data and were not extracted. The tasking premise
of "1968 formal-analysis tables (frequency/positional counts per
sign)" is not borne out by the volume; the per-sign positional
material in this corpus is Kondratov's 1965 Table 4 above, and
the aggregate frequency material is his Tables 1–2. Recorded as
table id KN1968 in the dataset JSON's `tables_not_extracted`.

### Proto-Indica 1973

**Finding: this volume contains no sign-frequency or positional
count tables at all.** Its contents are Knorozov's inscription
classification (pp. 4–17, prose + glyph illustrations — no count
tables, id PI73-K), Volchok's calendar/chronology article,
Gurov's two articles, and Misyugin on seafaring. The numeric
tables it does contain are calendrical, extracted here for
completeness and clearly labelled non-sign, non-positional:

| id | printed p. | table | rows |
|---|---|---|---|
| PI73-V1 | 42 | Volchok, unnumbered: yuga beginning/end festivals (after Swamikkannu Pillai 1922, 59) — rows: the four yugas in printed order (Krita, Dvapara, Treta, Kali); columns: "beginning of yuga" festival, "end of yuga" festival | 4 |
| PI73-V2 | 48 | Volchok, unnumbered running-text table: divine-chronology unit equivalences | 3 |
| PI73-V3 | 49 | Volchok, unnumbered: yuga durations in divine and human years (four yugas + Mahayuga) | 5 |

Russian headers/captions for PI73-V1–V3 were hand-translated by
the extractor from the rendered pages; both the Russian strings
and the English translations are stored in the CSVs.

**Defeated extraction — PI73-G1:** Gurov's Table 1 (printed
pp. 56–57), Dravidian terms derived from the "year" base, is a
two-page table of heavily diacriticised transliterated word
forms. Neither the embedded Acrobat OCR nor RapidOCR (the
available venv ships no Cyrillic/diacritic model) nor the scan
resolution supports reliable cell-level transcription.
Structure recorded only; **no values extracted and none guessed.**
Gurov's Tables 2 (p. 59) and 3 (pp. 63–64) are schematic
diagrams of the five-term year-counting system, not numeric
data (id PI73-G2, recorded, not extracted).

## Method

1. Rendered the table pages at 300 DPI with `pdftoppm` (images
   kept outside the repo; never committed).
2. Fresh image OCR with RapidOCR (rapidocr-onnxruntime 1.4.4)
   from the pre-existing venv `~/workspace/venvs/ocr` — the same
   tooling previously used for the Mahadevan 1977 introduction.
   On the English tables RapidOCR read numerals at ~99% token
   accuracy (two tokens misread in Table 1: the row label 900
   and one 6→9). On the Russian pages it reads digits correctly
   (e.g. 4800) but has no Cyrillic model, so Russian words are
   not OCR-extractable with this engine.
3. Values were curated by triangulating three reads — publisher
   text layer, RapidOCR output, and the extractor's own visual
   read of the rendered page — with the visual read decisive.
   One text-layer defect was caught this way: Table 1, row 1125,
   Egyptian value is printed "1" (text layer: "X").

## Accuracy (hand verification)

36 cells were sampled across all seven extracted tables and
re-read by eye from the rendered page images against the
extracted CSVs: Table 1 ×8, Table 2 ×8, Table 3 ×8, Table 4 ×8,
PI73 tables ×4. **Result: 36/36 cells match the printed page
(100% fidelity on the sample).** Per-table: K1965-T1 8/8,
K1965-T2 8/8, K1965-T3 8/8, K1965-T4 8/8, PI73-V1/V2/V3 4/4.
Verification measures fidelity to the printed page, including
where the printed page is itself internally inconsistent:

## Printed anomalies (extracted as printed; never repaired)

- **K1965-T3:** Egyptian "Errors" cells sum to 94 vs printed
  total 88 (the length-9 cell, 6, breaks genuine+errors=total);
  Proto-Indian "Errors" cells sum to 628 vs printed 626;
  "Total" cells sum to 1997 vs printed 1999; errors
  relative-frequency cells sum to 169 vs printed 168.
- **K1965-T4:** every row total matches its cells, but the
  printed column totals for finals 87 (102 vs computed 95),
  124 (28 vs 25) and 66 (2 vs 1) disagree with the cells;
  printed grand total 171 vs computed 160.

## Artifacts

- `data/soviet_positional/*.csv` — one CSV per table (7 tables,
  109 records), every record carrying (source, printed page,
  table id).
- `data/soviet_positional/phase121_soviet_positional_dataset.json`
  — combined dataset with per-table metadata, the
  not-extracted register, and the printed anomalies.
- `backend/glossa_lab/soviet_positional.py` — loader/validator;
  `backend/scripts/phase121_soviet_positional.py` — validation
  run writing `reports/phase121_soviet_positional_results.json`;
  `backend/tests/test_phase121_soviet_positional.py` — 7 tests.

## Non-claims

This is a descriptive dataset only. It scores no prediction,
validates no anchor, and changes no anchor, tier, or registry.
Whether the Soviet positional data can formally bear on
PRED-2026-001/002 is an open question for a future spec
adjudication (the registered PRED texts name specific corpora);
this phase takes no position on it.

**AI disclosure:** extraction and execution recorded by an AI
agent (Muse Spark, via Muse) at the direction of Tristen
Pierson, per constitution §VI.

## Verification runs

- New tests: 7 passed (`backend/tests/test_phase121_soviet_positional.py`).
- Full backend suite: **799 passed / 12 skipped / 0 failed**
  (baseline 792/12/0 + 7 new; corrected 2026-10-08 — an earlier partial-collection run was first misreported as 786/13).
- Foundation check: **40 passed / 0 failed / 8 warnings**
  (unchanged from baseline).
