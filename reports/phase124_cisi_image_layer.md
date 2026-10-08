# Phase-124 — CISI Image Layer (enabling asset)

**ENABLING ASSET ONLY — NO SIGN IDENTIFICATIONS, NO COMPARISON STUDY**

Date: 2026-10-08. Sources: CISI Vol. 1 (= MASI 86, Collections in
India, 431 scan pages) and CISI Vol. 2 (Collections in Pakistan, 486
scan pages), held locally as in-copyright research copies
(`cisi-1-ia-scan/`, `cisi-2-ia-scan/` in the research downloads).
Branch `phase/124-cisi-image-layer`. This phase builds the image
layer that later phases may consume: a structured catalogue table
keyed by CISI object ID, and a documented sign-crop pipeline with a
worked sample. It asserts nothing about what any sign means or which
sign any crop depicts.

## Storage governance (read first)

The scans are in-copyright research copies. The derived catalogue
table, the page renders, the per-page OCR checkpoints and every crop
image live **only** in the gitignored local store:

```
~/workspace/glossa-lab/corpora/downloads/cisi_image_layer/
  catalogue/   cisi_vol1_catalogue.csv, cisi_vol2_catalogue.csv,
               coverage_summary.json
  crops/       *.png sign-region crops + crop_manifest.csv
  ocr/         per-page RapidOCR checkpoints (v1/, v2/)
  page_cache/  rendered page PNGs (140 dpi working cache)
```

Verified with `git check-ignore -v` from the main checkout: every
path above is matched by `.gitignore:176:corpora/`. Before the
Phase-124 commit, `git status` was checked to confirm no crop image,
render, OCR checkpoint or catalogue CSV is staged. This PR contains
only: pipeline code, driver scripts, tests, this memo, the local-store
manifest (`reports/phase124_cisi_local_store_manifest.json`, counts
and schema only — no images, no catalogue rows), and ledger entries.
Regeneration: render → OCR → assemble, using the commands in the
manifest; the pipeline is deterministic given the same scans, venv
(`~/workspace/venvs/ocr`, RapidOCR 1.4.4) and parameters below.

## 1. Catalogue table

### What the volumes actually print

CISI is a photographic corpus. There is **no per-object prose
catalogue**: each plate page carries a header (printed page number,
site, object-ID range, object type, and the motif chapter in single
quotes) and, under each photograph, a caption of the form
`<ID> <side>` — e.g. `M-67 A` (original object), `M-67 a` (its modern
impression), with `bis` for a second exemplar and an occasional
photographic scale note (`H-382 A (50 %)`). Per-object museum,
material and dimensions are **not printed** on the plates; the
collection scope is stated only at volume level (Vol. 1: collections
in India; Vol. 2 preface: National Museum Karachi, Mohenjo-daro
Museum, Harappa Museum, Lahore Museum). The table therefore records
`material_basis` / `dimensions_basis` = "not printed per object in
CISI plates" with the fields empty, rather than importing values from
outside sources. Fields captured per row (22 columns): volume, CISI
ID, photo key (ID + side + bis), side, bis flag, raw caption text,
caption OCR score, PDF page, printed page, site, object type, motif
chapter, scale %, collection scope (volume-level), material +
basis, dimensions + basis, photo box (x;y;w;h at 140 dpi), extraction
basis, confidence, notes.

### Extraction method and OCR assessment

The PDFs are image-only scans (no embedded text layer). The bundled
`djvu.txt` OCR layer was assessed first: it is a single continuous
text stream with **no page breaks** (0 form feeds in either volume),
heavily garbled in the front matter and unusable for page-anchored
extraction; it is used only to corroborate that a parsed CISI ID
occurs somewhere in the same volume (`+djvu_sequence_corroborated` in
the row's extraction basis — it can never corroborate a page). All
plate rows therefore rest on **fresh per-page OCR** (RapidOCR,
140 dpi renders), which reads captions and headers at high confidence
(probe page: caption scores 0.87–1.00). Header fields are parsed
against the vocabulary the volumes print; caption parsing is strict
(regex over the printed caption forms) so OCR garbage from the Indus
signs themselves (e.g. `TOYAUF`, `XIKOT`) is rejected, never mistaken
for a caption. Rows are flagged `confidence = low` — and kept, not
cleaned — when the caption score is < 0.90, no site could be read
from the header, or no photograph could be associated.

### Coverage

All 917 scan pages were OCR'd (Vol. 1: 431/431; Vol. 2: 486/486).

| | Vol. 1 | Vol. 2 | Total |
|---|---|---|---|
| pages with catalogue rows | 359 | 413 | 772 |
| catalogue rows (one per photographed side) | 3,320 | 4,385 | **7,705** |
| distinct CISI object IDs | 1,475 | 2,019 | 3,494 |
| rows with an associated photo box | 3,200 (96.4 %) | 4,220 (96.2 %) | 7,420 |
| low-confidence rows (kept, flagged) | 413 (12.4 %) | 568 (13.0 %) | 981 |
| non-plate caption-like lines dropped (sign-index entries etc.) | 1,401 | 1,755 | 3,156 |

Sites keyed: Vol. 1 — Mohenjo-daro, Harappa, Lothal, Kalibangan,
Banawali, Rangpur, Rojdi, Surkotada, Desalpur, Jhukar, Amri, Addenda;
Vol. 2 — Mohenjo-daro, Harappa, Jhukar, Amri, Addenda.

Two honest caveats. (1) The distinct-ID counts exceed the prefaces'
photographed-object counts (Vol. 1: 1,378 photographed in India;
Vol. 2: 1,341 photographed in the four Pakistani museums): the
volumes also carry addenda and objects documented outside those
campaigns, and an unknown share of the excess is OCR digit-misread
phantoms (e.g. a misread digit creates a spurious singleton ID).
Rows are never silently corrected, so the table preserves those
phantoms, flagged only by OCR score / DJVU corroboration. (2) The
bundled djvu layer corroborates only a minority of parsed IDs
(Vol. 1: 344 of 1,475 distinct IDs; Vol. 2: 794 of 2,019) — a
measure of its garbling (Cyrillic-substituted glyphs, merged runs),
not of the fresh OCR, whose caption scores are typically 0.95+.

### Hand verification

Ground truth was read visually from rendered pages *before*
extraction, on four pages spanning both volumes and both sparse and
dense layouts: Vol. 1 PDF pp. 46 / 66 / 91 (printed 10 / 30 / 55)
and Vol. 2 PDF p. 66 (printed 31) — 36 caption rows in total
(4 + 6 + 19 + 7). Field-by-field results:

| field | correct | notes |
|---|---|---|
| CISI ID | **36/36** | 2 rows needed the I/l→1 normalisation (`M-IIA`, `M-1la` for M-11); both are flagged in the table |
| side (A/a/bis) | **35/36** | one miss: M-69 (Vol. 1 p. 66) — the `a` of the impression caption was not OCR'd; the row stands with side empty |
| printed page | 4/4 pages | |
| site | 4/4 pages | after fixing merged-run header parsing (`SEALSMOHENJO-DARO209-217`) |
| object type | 4/4 pages | |
| motif chapter | 4/4 pages | |
| photo association | 36/36 rows paired | one degenerate box: M-667 a (Vol. 2 p. 66) received a merged multi-photo box from the grid fallback after the anchored search failed; its crops were skipped (see §2) |

Overall field accuracy on the checked sample: 87/88 field values
(98.9 %). This is a 36-row sample on four pages, reported as such —
not a whole-table guarantee. The 36 rows carry
`+hand_verified` in their extraction basis.

## 2. Sign-crop pipeline

Code: `backend/glossa_lab/cisi_image_layer.py` (pure logic, unit
tested), drivers in `scripts/phase124_cisi/` (`render_pages.py`,
`ocr_pages.py`, `build_catalogue_and_crops.py`).

1. **Photo location (primary)** — caption-anchored search: captions
   OCR reliably, photographs sit directly above them. From the
   caption centre, walk up while the per-row dark-pixel fraction in
   a ±17 %-of-width window stays above 0.28 (dark threshold is
   page-adaptive: corner-patch median − 22 grey levels, because
   Vol. 2's paper tone, ~234, defeats any fixed threshold), with the
   photo required to start within 4.5 % of page height above the
   caption; then walk left/right on the per-column dark fraction
   (> 0.30, blank-gap tolerance 3 px). A grid texture segmentation
   (per-row/column grey-level std, threshold 20.0) remains as
   fallback for captions the anchored search misses.
2. **Caption association** — the anchored box belongs to its caption
   by construction; fallback pairs a caption with the photo whose
   x-range contains its centre and whose bottom edge is nearest
   above it (gap ≤ 7 % of page height).
3. **Sign regions** — within a seal photograph (sides A/a), the
   inscription band is the top 42 % of the photo. The per-column
   grey-level **std** (contrast) — not darkness, since the
   raking-light photographs render signs as pale grooves with dark
   shadow edges, and a dark-pixel projection mostly finds the animal
   motif — is smoothed (moving average, 4.5 % of photo width) and
   segmented at an adaptive threshold halfway between the median
   and the 95th-percentile column, minimum region width 4.5 % of
   photo width, gap merging 1.5 %, padding 2 %. Each region is saved
   as one crop PNG at 200 dpi.

**Failure modes (all observed in the worked sample):** touching
signs merge into one region; signs split at low-contrast strokes;
motif elements intruding into the top band (horns, the 'manger'
standard) add spurious regions; the boss/back side of a seal and
blank seal edges yield empty regions; one photo (M-213 A, Vol. 1
printed p. 55) is so dark that all four of its regions are
fragments; multi-row inscriptions are truncated at the band edge;
the impression side (a) is a mirror image, as printed. Crops are
*region proposals* for later human/machine study — the pipeline
does not count signs and does not identify them.

### Worked sample

Four plate pages were cropped: Vol. 1 PDF pp. 66 and 46 (printed
30, 10), Vol. 1 PDF p. 91 (printed 55), Vol. 2 PDF p. 66 (printed
31) — 32 catalogue photos, sides A/a. The pipeline wrote **82
crops**; one further photo (M-667 a, Vol. 2 p. 66) was skipped
because its only photo box was the degenerate merged fallback box.
Every crop was then inspected visually on contact sheets and
classified: **38 good** (substantially frames one sign), **29
partial** (a sign cut, or two signs merged), **15 bad** (motif,
photo edge, blank or fragment with no sign content). The good
yield (38/82 = 46 %) is the honest single-pass rate of the
heuristic on these pages. The 38-crop verified sample — CISI ID,
side, printed page, PDF page, photo box and crop box for each — is
listed in `reports/phase124_cisi_local_store_manifest.json`; the
crops themselves, the full 82-crop manifest and the per-crop
verdicts (`crops/verification.csv`, `crops/verified_sample.csv`)
live only in the local store.

## 3. Verification

- New unit tests: `backend/tests/test_phase124_cisi_image_layer.py`
  — **24 passed** (caption forms incl. I/l normalisation and junk
  rejection, header parsing incl. OCR-merged runs, texture/photo/
  sign segmentation on synthetic arrays, association, row assembly
  with the not-printed fields).
- Full backend suite: **816 passed / 12 skipped / 0 failed**
  (includes the 24 new tests).
- Foundation check (`backend/scripts/foundation_check.py`, corpora
  symlinked from the main checkout): **40 passed / 0 failed /
  8 warnings** — unchanged from the Phase-119 baseline.
- Ruff: clean on all new files.
- Test side-effect modifications (claims JSONs, outputs/) were
  reverted before commit; `git status` shows only the intended
  Phase-124 files.

## 4. Non-claims

- This is an **enabling asset**: a catalogue table and a crop
  pipeline. No sign identifications are asserted by any crop; crop
  file names carry object IDs and geometry only.
- No comparison study was run; no anchor, tier, or corpus statistic
  was changed by this phase.
- Catalogue fields the volumes do not print per object (museum,
  material, dimensions) are recorded as not printed, not filled in.
- Low-confidence rows are flagged in the table, not silently
  corrected; the hand-verification accuracy above is the honest
  field-level rate on the checked sample, not a whole-table claim.
- No in-copyright image or derived table is in this PR (see Storage
  governance).

**AI disclosure:** execution recorded by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.
