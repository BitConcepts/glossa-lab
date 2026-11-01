# M77 sign-list extraction — record (2026-10-25)

**Status: EXECUTED.** The Sign List of Mahadevan 1977 (MASI 77) has been
transcribed into a machine-readable dataset: one row for each of the
417 signs, carrying the sign's number, whether the printed list marks
it as having graphic variants (the dagger †), and the morphological
class the book assigns it. Transcription only — no census rules were
applied, no thresholds were tested, and no conclusion about any sign's
identity is drawn or implied.

**Source.** The pinned scan recorded in
`masi77_full_volume_intake_2026-10-25.md` (DLI scan of the original
1977 ASI edition, barcode 99999990041354; 16,445,165 bytes; SHA-256
`ef68fe8dc25e94fe9cb75b418c5189a084383e72498560ef393372e90a27e110`).
The hash was re-verified against the desktop copy at the start of this
extraction and matched exactly. The PDF itself stays on the desktop
and is not in git.

**Dataset (not in git — the sources store is gitignored):**
`glossa-corpus/indus/sources/mahadevan-1977/`

| file | bytes | SHA-256 |
|---|---|---|
| `m77_sign_list.csv` | 51,809 | `ce5dd5a59418132f54761324ca449aa0a7d37e0dad41013aca811049b36af3a4` |
| `m77_sign_list.json` | 116,769 | `63059d6403898653600c3be3e2268c512550cc8f8906114ac712743f161e0ae3` |
| `decision_report.txt` | 404 | `382d2e09ee442e1b041f96e0309988a323010ccbda53923918970a7537e71565` |

The CSV was built with Python's `csv` module and validated by parsing
it back: 417 data rows, exactly 8 columns per row, no missing keys,
sign numbers running 1–417 with no gap. The JSON file is the same 417
rows and was checked against the CSV row by row. The desktop build of
the CSV (before transfer) hashed to `caf0486d…`; the landed copy
differs only in line endings (CRLF→LF, normalised in transfer) — the
content is identical.

Columns: `sign_no`, `variant_marker` (Y = the list prints a dagger for
this sign, N = it does not, UNCERTAIN = the readings did not settle
it), `morph_class_no` and `morph_class_label` (the book's §11.5
classification, wording as printed), `page_printed`, `page_pdf`,
`status` (CLEAN or UNCERTAIN), `evidence` (every reading that went
into the decision, kept per sign).

---

## 1. Scope correction — the sign list is four pages, not 131

The intake record and the extraction brief both gave the sign list as
printed pp. 32–162 (PDF pp. 44–174). **That range is wrong**, and this
extraction corrects it from the pinned scan itself. The volume's own
contents leaf (PDF p. 9) lists: SIGN LIST 32 · TEXTS IN THE INDUS
SCRIPT 39 · CONCORDANCE TO THE TEXTS 163 · TABLES I at 717. The intake
record's structure line swapped the Texts and the Concordance: the
Texts begin at printed p. 39 and the Concordance at printed p. 163.

Verified layout of the pinned scan (printed page = PDF page − 12):

- **Sign List: printed pp. 32–35 (PDF pp. 44–47)** — a numbered grid,
  10 signs per row, signs 1–417, with two printed NOTES under the grid
  on p. 35. PDF p. 48 is blank; p. 49 is the Texts title page.
- Texts: PDF pp. 49–172 (text numbers 1001–9842).
- Concordance: PDF pp. 173–728. The per-sign occurrence text-number
  lists live here — which is also why the intake record's sentence
  "the Sign List's per-sign entries pair drawn forms with occurrence
  text-number lists" is corrected: that pairing describes the
  concordance arrangement, not the sign list. The sign-list grid
  prints, for each sign, its number, one drawn normal form, and the
  dagger where it applies. No occurrence lists and no frequency
  figures are printed in the grid.
- Tables from PDF p. 729. Appendix I (List of Sign Variants): PDF
  pp. 795–802 (printed 783–790). Appendix II (List of Field Symbols):
  PDF p. 803 onwards — field symbols, not script signs; out of scope.

The grid prints **one drawn form per sign**: §11.4 states the list is
a normalised signary and the most frequent variant was chosen as the
normal form. "Drawn forms per cell" is therefore 1 by the book's own
construction, recorded here as a book-level fact rather than per-cell
data.

**Signs 418 and 419 exist but are not in the list.** The Postscript
addendum (§16.3, printed p. 25 — outside the sign-list pages) adds two
signs "numbered 418 and 419 [which] could not be included in the Sign
List", attested in texts 8401 and 9222. Mahadevan's full sign universe
is therefore 419; the Sign List proper is 417. This dataset covers
the 417. Whether a future census counts 418/419 as part of its M77
witness is that census's decision, not this extraction's.

## 2. F-6 answered — where identifications live in M77

The red team's finding F-6 left open whether the sign list attaches
identifications. Read from the volume itself, the answer is:

- **The grid pages attach no per-sign labels of any kind** — only
  numbers, drawn forms, and daggers.
- **The list is arranged by a morphological classification printed in
  the Introduction (§11.5, printed pp. 15–16; verified against the
  pinned scan, PDF p. 28):**

  | class | label (as printed) | signs |
  |---|---|---|
  | I | Human beings (including parts of human body) | 1–49 |
  | II | Other living beings (and parts of their bodies) | 50–85 |
  | III | Strokes and 'numerals' | 86–122 |
  | IV | Other linear signs | 123–203 |
  | V | Triangular signs | 204–235 |
  | VI | Rectangular and rhomboid signs | 236–286 |
  | VII | Curves | 287–327 |
  | VIII | Cups | 328–372 |
  | IX | Ovals and circles | 373–417 |

- **Mahadevan expressly disclaims identification weight for it.** The
  sentence immediately following the table reads: *"It needs to be
  emphasised that the classification is merely conventional and no
  stress is laid on any identification, even in respect of signs
  included in the first two categories of 'living beings.'"*
- **There is no celestial class anywhere in the classification.** The
  nine classes are shape classes; the first two carry depictive names
  under the disclaimer above.

So the earlier flat statement "M77's list attaches no depictive
labels" is wrong at class level and right at sign level. Under the
trigger-census instrument's reported-speech rule, §11.5 membership is
**reported, not adopted** classification evidence: Mahadevan grouped
signs 1–49 as human-shaped and 50–85 as other-living-being-shaped
while telling the reader not to rest any identification on it. And
because no class is celestial, **M77 cannot be the exhibited list that
reopens Spec 071's trigger on its own terms** — the trigger needs a
published list identifying at least 5 celestial signs, and M77
identifies none, celestial or otherwise, at sign level.

## 3. Method, and one deviation that must be read with the dataset

The brief specified OCR plus human double-keying over rendered pages,
reconciled entry by entry. **The human double-keying was not
performed, and the reason is mechanical, not a judgement call.** A
write restriction was active on this machine for most of the session:
files written by scripts or shell commands landed as zero bytes
(repeatedly tested), so rendered page images could not be brought
onto this machine as files at all. The one fallback channel — carrying
an image through the conversation itself — was tried twice with
calibration crops; both arrived corrupted (the first decoded only its
top ~15%, the second showed block artefacts and duplicated bands), and
both checkers reported the corruption rather than guessing. The
renders and all OCR output remain on the desktop
(`~/m77extract/` in the desktop's WSL home), so a visual pass can
still be added later; §6 below names exactly which cells it should
look at first.

In its place, each of the 417 cells was read by **machine consensus**:
up to nine readings per cell from two independent OCR engines
(Tesseract 5.3.4 and RapidOCR), taken at page level and from cell
crops at several settings, plus membership in the Appendix I list as
printed evidence. Sign numbers themselves were never in doubt — the
grid's order fixes each cell's number (pages begin at signs 1, 111,
220, 330), and both engines read the number sequences cleanly; the
only per-cell question was the dagger. The decision rule, set before
it was applied: engines under-read the small dagger far more often
than they invent one, so a "dagger seen" reading is strong evidence
and a "no dagger seen" reading is weak. A sign is Y when the Appendix
lists it (unless at least three grid readings unanimously say no —
those become named conflicts, §5), or when at least two dagger
readings span both engine families; N when it is not in the Appendix,
has no dagger reading, and at least two plain readings; otherwise
UNCERTAIN. Every cell's readings are preserved in the dataset's
`evidence` column.

Two checks hold the result to the book's own numbers:

- **The 179 checksum.** §11.4 states that of the 417 signs, **179 have
  variants** — exactly the daggered set, since the printed note under
  the grid (p. 35) reads: "1. Signs marked † in the Sign List have
  graphic variants recorded in the List of Sign Variants… 2. See
  Postscript (p. 25) for addendum to the Sign List." The dataset's
  counts bracket it: **156 Y, 231 N, 30 UNCERTAIN; 156 ≤ 179 ≤ 186.**
  The bracket holding is necessary, not sufficient — it shows the
  counts are consistent with the book's total, not that every flag is
  right.
- **The Appendix I cross-check.** The appendix lists exactly the
  daggered signs, so its sign set should equal the Y set. Parsing it
  from this scan proved unstable (two parse methods recovered 106 and
  112–115 unique signs of 179; the first appendix page is faint and
  its columns defeat the geometry parsers), so appendix membership was
  used as positive evidence only — presence counts, absence proves
  nothing. This weakness is named here rather than hidden: the
  appendix parse is corroboration, not a pillar.

**Agreement figures (the double-keying analog, honestly labelled).**
Where both engine families produced readings, they were unanimous on
290 of 417 cells (76 daggered, 214 plain) before any adjudication.
Under the strictest merge tried first (a cell settled only on ≥3
agreeing readings with none against), 205 cells were contested; the
final evidence model settled all but 30. There is no human keying
rate to report, because there was no human keying — see the deviation
above.

**Spot-check.** A seeded random 5% sample (21 signs; seed 1977) was
re-read by a separate script from the 150-dpi page renders — a scale
no decision pass used — with both engines. 14 of 21 agreed outright.
The 7 disagreements were all *absences* (the lower-resolution re-read
could not see a dagger, or read nothing); none was a positive
contradiction. Those 7 were re-read again at 300 dpi from wider
crops: 4 confirmed the dataset (signs 151 N, 297 Y, 371 Y, 406 N) and
3 stayed unconfirmed (signs **182, 391, 403**, all dataset-Y: their
daggers rest on the page-level readings and, for 391/403, appendix
membership; the crop re-reads could not see them). Net: **18 of 21
sampled entries confirmed (85.7%), 3 unconfirmed and named, 0
contradicted.** The decision rule was not changed after the
spot-check; the three names are carried here and in §6.

## 4. Reference data carried with the extraction

Mahadevan's printed frequency summary (§11.10) — recorded here
because the census will want it as a checksum when the Concordance or
Table I is ever extracted; it is *not* part of the dataset, and no
per-sign frequencies exist in the sign list:

| occurrences | signs | total occurrences |
|---|---|---|
| ≥1000 | 1 | 1,395 |
| 500–999 | 1 | 649 |
| 100–499 | 31 | 6,344 |
| 50–99 | 34 | 2,381 |
| 10–49 | 86 | 1,833 |
| 2–9 | 152 | 658 |
| once | 112 | 112 |
| **total** | **417** | **13,372** |

Per-sign frequencies live in Table I (printed pp. 717 ff.), not
extracted here.

## 5. Conflicts and gaps — named, never guessed

**UNCERTAIN signs (30):** 3, 4, 9, 10, 11, 13, 15, 19, 22, 29, 41, 69,
137, 141, 150, 159, 167, 171, 177, 214, 217, 219, 224, 244, 267, 341,
373, 379, 384, 409. Each keeps its full reading set in the dataset.

**Appendix/grid conflicts (6):** signs 3, 4, 10, 11, 13, 22 are listed
in the Appendix I parse but every grid reading says plain. All six sit
in the faint first grid page's range. They are inside the UNCERTAIN
30 and are the first cells a visual adjudication pass should settle.

**Spot-check unconfirmed (3):** signs 182, 391, 403 (dataset-Y; see
§3).

**Known weak cells:** sign 41 produced no reading from any engine on
the first passes (a faint patch on printed p. 32) and only conflicting
readings on targeted re-reads; it is UNCERTAIN. Sign 220 was briefly
double-measured by an early script (a page-boundary bug, caught and
discarded); the landed row rests on the correct page's readings.

## 6. What this establishes / what it does not

**Establishes:**
- A machine-readable transcription of the complete M77 sign list
  exists in the programme's store: 417 signs, each with its
  variant-dagger flag (156 Y / 231 N / 30 named UNCERTAIN) and its
  §11.5 class, the flags bracket-validated against the book's own
  printed total of 179 variant-bearing signs.
- F-6 is answered from the volume: no per-sign identifications exist
  in M77; the §11.5 classes are reported classification under the
  author's own no-identification disclaimer; no celestial class
  exists in M77.
- The intake record's page map is corrected (appended to that record,
  same date): Sign List printed 32–35; Texts 39–162; Concordance
  163–716.

**Does not establish:**
- The dagger state of the 30 UNCERTAIN signs (a short visual pass
  over the preserved desktop renders can settle them; it has not been
  done).
- Any identification, reading, or meaning for any sign. None was
  extracted, because M77 prints none at sign level.
- Any occurrence count or frequency for any sign (Table I and the
  Concordance were not extracted).
- That classes I/II are identifications of human or animal signs —
  Mahadevan says the opposite (§2).
- Anything about whether the script is deciphered.

## 7. Readiness — what can now be consumed, and what remains

For the **trigger census** and **M7's witness census**, this dataset
supplies the M77 witness as far as M77 goes: the 417-sign signary,
which signs carry recorded variants, and the §11.5 class of every
sign, all keyed by M77 sign number for the many-to-many join the
instrument specifies. The census can now also record, from source,
that the M77 witness contains **no celestial identifications**, and
that its human/other-living classes arrive under an authorial
disclaimer and therefore enter, if at all, as reported-not-adopted.
What remains before the census can be **applied** (its application is
a separate owner act, not part of this extraction): the Wells 1998
witness extraction is still outstanding; the 30 UNCERTAIN flags and
the 6 appendix/grid conflicts should be visually adjudicated (the
renders are preserved for exactly this); the census must decide
whether signs 418/419 belong to its M77 witness; and occurrence
counting per the instrument still requires the primary-population
work the instrument specifies — this dataset carries no occurrences.

---

*Provenance of this record: extraction executed 2026-10-25 on
TRISTEN-DESKTOP (renders and OCR under `~/m77extract/`), relay channel
`m77extract`; dataset transferred via tbitcs/desktop-relay commit
`bc126760a7791eefc7f8a676e954dd6c9ea26531` and hash-verified on
landing. Scripts preserved in the run folder
(`~/workspace/glossa-run/m77-extract/scripts/` on the VM).*
