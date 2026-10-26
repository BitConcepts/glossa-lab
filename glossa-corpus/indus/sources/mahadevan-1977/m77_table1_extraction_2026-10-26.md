# M77 Table I — occurrence extraction and adjudication (2026-10-26)

**Status: EXECUTED.** Table I of Mahadevan 1977 (MASI 77), the
per-sign occurrence counts by text position (SOL | INI | MED | FIN |
TOT), is extracted for all 417 signs. **405 rows are certain** under
the rule below; **12 rows stay uncertain** and are named in §5 — their
printed cells are too faded in the scan to read, and no value was
guessed or fitted. The dataset's certain TOT column sums to **12,325**
against the book's printed total of **13,372**; §4 accounts for the
1,047 difference as far as the printed pages support, and documents
the part no printed row supports.

## 1. Source, pages, dataset

- **Source scan (pinned):** the program's custody copy of *MASI 77
  Indus Script Texts Concordances & Tables* (Iravatham Mahadevan),
  full volume, SHA-256
  `ef68fe8dc25e94fe9cb75b418c5189a084383e72498560ef393372e90a27e110`
  — byte-identical to the intake pin.
- **Pages:** Table I is printed pp. 717–723 = PDF pp. 729–735 of the
  scan. Printed p. 723 carries signs 385–417 and the printed TOTALS
  row; Table II begins on printed p. 724.
- **Dataset (gitignored working files, canonical store = this
  directory):** `m77_table1_occurrences.csv` and
  `m77_table1_occurrences.json` here. Schema: `sign_no, occurrences,
  page_printed, raw_ocr, uncertain`; `occurrences` is the TOT column;
  `raw_ocr` is the five cell readings joined as
  `SOL|INI|MED|FIN|TOT`.
- **Hashes as updated by this record's work:**
  - CSV — 10,067 bytes, SHA-256
    `c047c2517474062db9eec508eccb62cd83cb2be045e1fc847fd426030f50b168`
  - JSON — 42,152 bytes, SHA-256
    `a210f6655873a5cd083fa450ebe26bf92900e3d21dd7f5ec14e5ab50a7673bb2`
  - Superseded Phase A hashes: CSV `aeec9cd1…` (9,482 bytes),
    JSON `7bf50d2a…`.
- **Certainty rule (both phases):** a row is certain only if all five
  cells read as clean digit strings AND TOT = SOL+INI+MED+FIN.
  Otherwise `uncertain=YES` and `occurrences` is empty.

## 2. Method

- **Phase A (first pass).** Tesseract per-cell OCR on 300-DPI renders;
  203 rows certain (sum 4,290), 214 uncertain. Printed pp. 718–719
  are pale, skewed scans and supplied almost no certain rows.
- **Phase B (this record).** Pages re-rendered at 400 DPI (PyMuPDF),
  deskewed and contrast-normalized per page; the pale pages were
  worked from these renders throughout.
  - *Second engine:* RapidOCR page-level passes at 300 and 400 DPI
    plus per-cell contact-sheet OCR, and Tesseract re-runs at
    alternate settings on the new crops. A cell settled only when at
    least two distinct sources agreed, at least one of them a
    400-DPI source. 48 further rows became certain this way.
  - *Visual adjudication:* every cell still doubtful was read from
    the page crops directly. 154 rows carry at least one visually
    read cell. Two print facts decided the fragment cases: a faded
    "0" survives as two thin arcs, and a faded "8" can survive only
    as its diagonal waist — an X shape (this settled signs 121 and
    128, whose MED cells hold exactly that X).
  - *Cautions recorded:* RapidOCR's page-token cell assignments on
    PDF pp. 730–731 misassign rows and columns in places; visual
    crops override any OCR majority there. A wide-crop RapidOCR
    audit of the finished certain set was tried and **rejected as an
    instrument** — it misread known-good rows (sign 99's TOT 649 read
    as 1) — so the certain set was verified visually instead (§6).

## 3. The printed TOTALS row

Phase A read the totals row's TOT as 3372 — its crop clipped the
leading digit. Re-read on wide crops from printed p. 723, the row is:

**SOL 190 | INI 3010 | MED 7196 | FIN 2976 | TOT 13,372**

The row is internally consistent (190 + 3010 + 7196 + 2976 =
13,372) and its TOT matches the §11.10 checksum of 13,372
occurrences over 417 signs. (TOT values in this table can print
with a thousands comma — sign 342 prints "1,395" — the totals row
prints none.)

## 4. Reconciliation

Certain rows (405) sum to:

| | SOL | INI | MED | FIN | TOT |
|---|---|---|---|---|---|
| Extracted (certain) | 177 | 2,886 | 6,695 | 2,567 | **12,325** |
| Printed totals | 190 | 3,010 | 7,196 | 2,976 | **13,372** |
| Residual | 13 | 124 | 501 | 409 | **1,047** |

By count the residual is exactly the 12 uncertain rows. The book's
own frequency distribution (§11.10) cross-checks the extraction:
its two largest bins match exactly — one sign at ≥1000 (sign 342,
1,395) and one at 500–999 (sign 99, 649). Against the remaining
bins the certain set is short 3 signs / 815 in the 100–499 bin,
1 / 76 at 50–99, 4 / 129 at 10–49, 3 / 26 at 2–9, and 1 / 1 among
the once-only signs.

What the uncertain rows can account for, from the pages: sign 102's
TOT is imaged at 151 and sign 162's at 212 (both in the 100–499
bin), sign 97's at 91; the other nine rows' legible cells cap their
totals well under 100 each. A generous maximum over all twelve
rows is ≈ 660 of the 1,047. The 100–499 bin still requires a third
sign of ≈ 452 that **no uncertain row can supply** — their TOTs are
imaged or component-capped far below it — and §6 shows the certain
set is not hiding it either. The remaining ≳ 390 of the printed
total, concentrated in the FIN, MED and INI residuals, is therefore
supported by no printed per-sign row in the scan: the book's
TOTALS row and its §11.10 distribution agree with each other but
exceed the sum of the printed per-sign rows as printed —
evidently tallied from the author's underlying counts rather than
from the printed rows. The dataset records the printed rows as
they stand; the 12 unsettled rows were left uncertain rather than
filled to fit the tally.

## 5. The 12 still-uncertain signs

All twelve sit on the two pale pages: signs 97 and 102 on printed
p. 718, the rest on printed p. 719. What survives on the page:

- **97** — SOL 11, INI 1, FIN 7 read; TOT reads 91. MED survives
  as a diagonal stroke plus top dashes: fits 27 or 72 (position
  favors 27; the arithmetic wants 72). No reading reconciles.
- **102** — INI 7, MED 70, FIN 3 and TOT 151 read clean. SOL shows
  only a 2-shaped fragment (top curve and base); the missing 71
  cannot sit in the SOL cell.
- **162** — SOL 3 and TOT 212 read. INI shows strokes beyond a
  plain 1 (10-like); MED reads 104-like; FIN holds only fragment
  strokes. No combination of the readings sums to 212.
- **167** — SOL 1, INI 1, MED 4, FIN 1 settled, but the TOT cell
  is blank in every render (an ink scan of the cell registers
  nothing where neighboring TOTs register). The implied 7 is not
  certified: a TOT digit with no ink is not a reading.
- **173** — SOL 0, INI 24, MED 0 read. FIN is a single dash
  fragment; TOT survives as two diagonal fragments favoring 28
  (FIN 4) over 25 (FIN 1); the FIN fragment does not decide it.
- **179** — SOL 0, INI 1, MED 1 read; FIN holds 1-like fragments;
  the TOT cell is blank in its own band in all renders. The
  implied 3 is not certified (same rule as sign 167).
- **180** — SOL 0, INI 2, MED 35 read; FIN blank. TOT shows a cut
  4-shaped glyph plus a speck; the components sum to 37 and no
  printed TOT reconciles with them.
- **181** — SOL 0 read. INI is a dotted stem, MED specks, FIN
  top-and-base fragments; TOT blank in its band.
- **182** — SOL 0. INI shows a 1 plus a 7-fragment; MED a
  2-fragment; FIN blank; TOT a dotted 1. No assembly reconciles.
- **183** — SOL 0. INI a 1-fragment; MED the remains of a 1
  (flag and base); FIN blank; TOT a single hook fragment.
- **184** — SOL survives as a 2-shaped fragment pair (top curve
  and base); INI broken ticks; MED, FIN and TOT fragments only.
- **185** — SOL two thin strokes (0 or 11 — ambiguous); INI 0;
  MED a faint 1; FIN a faint fragment; TOT fragments only.

## 6. Verification of the certain set

- Every certain row with any cell ≥ 40 was re-read visually on wide
  crops (signs 1, 12, 15, 59, 150, 211, 245, 254, 391, 402 and the
  two bin anchors 99 and 342): all read back exactly as recorded.
- A 26-row sample of the certain set (16 consensus rows, 10
  second-engine rows, spread across all seven pages) was re-read
  as full-row strips: **26 of 26 match** the recorded values.
- Dataset validation after the update: CSV re-read with Python's
  `csv` module — 417 rows, no empty-key rows; every certain row's
  five cells sum to its `occurrences`; the JSON file was verified
  row-by-row identical to the CSV.
