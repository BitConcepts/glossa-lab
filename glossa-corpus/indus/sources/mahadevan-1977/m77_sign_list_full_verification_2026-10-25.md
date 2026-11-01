# M77 sign list — full visual verification of the remaining 384 cells (2026-10-25)

**Status: EXECUTED.** Every dagger (†) flag in the M77 sign-list
dataset that still rested on the extraction's machine consensus —
the 384 cells dataset v2 carried as status CLEAN — has now been
read visually, cell by cell, under the adjudication's protocol
(records: `m77_sign_list_extraction_2026-10-25.md`, PR #405;
`m77_sign_list_visual_adjudication_2026-10-25.md`, PR #407). One
cell changes: **sign 381 is daggered** (dataset said plain). Dataset
v3 is issued. The dataset's dagger total is now **179**, the figure
§11.4 of the book itself prints — reached by the readings, not by
adjustment (§3 gives the evidence for that distinction, including
the arbitration that removed a second apparent change).

## 1. Method

- **Source images.** New 300-dpi renders of PDF pp. 44–47, made on
  this machine from the programme's custody copy of the pinned
  scan (SHA-256 `ef68fe8d…e110`, byte-identical to the intake pin)
  after the desktop renders' equivalence was tested, not assumed:
  all 37 preserved adjudication cell crops were re-cut from the new
  renders at the fixed geometry and compared — every one frames the
  same cell content; 2.39% of pixels differ at all, mean absolute
  difference 1.66 grey levels, the differences confined to
  stroke-edge antialiasing between renderers; the worst cell
  (sign 384) was inspected side by side and shows the same glyph,
  number and dagger in the same position. Page frame 4963×7017,
  identical to the desktop renders.
- **Crops.** The adjudication's fixed grid geometry and crop boxes,
  unchanged: a tight 2×-enlarged number crop, a native whole-cell
  crop, and a wide context crop per cell — 384 cells × 3 = 1,152
  crops, every file verified to decode before any reading. Images
  were read directly from files throughout; the
  conversation-carried route is not used.
- **Two independent blind passes.** Pass A read the enlarged number
  crops (cell/wide consulted where the number fell outside the
  tight frame); pass B read the whole-cell crops and reported the
  printed number it saw in each cell alongside its verdict, so a
  crop framing the wrong cell would expose itself. It did, once
  (§2). Each pass was split across two readers by code range
  (V001–V192, V193–V384); no reader had access to the dataset, to
  the code→sign mapping, or to any other reader's results, and no
  reader was told any running total, the dataset's values, or the
  §11.4 figure — each brief was a plain verification of every cell
  on its own merits. Cells were neutral-coded (V001–V384, shuffled)
  and the mapping stayed sealed until both passes were complete.
- **Calibration.** The four cells the extraction's spot-check had
  already confirmed from 300-dpi wide crops (151 N, 297 Y, 371 Y,
  406 N) sat inside the 384 as ordinary coded cells. Both passes
  read all four correctly (8 of 8 reads).
- **Arbitration rule.** A pass disagreement, or any code whose
  reported number did not match the cell the crop was cut for, went
  to a coordinator third look at the wide crop; a cell no look
  could settle would have stayed flagged. No verdict was taken from
  the running dagger total at any point.

## 2. Results

- **Coverage:** 384 of 384 cells read by both passes.
  **Pass agreement: 384 of 384 verdicts (100%).** No cell was
  returned ILLEGIBLE by either pass. Agreement is recorded as it
  stands — including the one case below where the agreeing pair
  proved to be reading the same neighbouring cell, which is what
  the number reports and the arbitration rule exist to catch.
- **Framing integrity.** The two passes' reported numbers match
  the mapped sign on 382 of 384 codes. The exceptions:
  - **Sign 191 (V130).** Pass A read the bottom-clipped tight crop
    as "101"; pass B read the cell crop as "191"; both returned N.
    Third look (cell crop): the number is 191 — the clipped 9
    misread as 0 — plainly printed, no dagger. **Final: N**
    (unchanged).
  - **Sign 218 (V261).** Both passes reported number 217 and
    verdict Y. Third look (wide crop, which shows both cells in
    full): 217 at left carries a clear dagger — the cell both
    passes read, and the sign the adjudication already settled as
    Y — and the target 218 at right is **plain**: no dagger after
    its number. **Final: N** (unchanged). This is the mirror image
    of the adjudication's sign-219 case: there the neighbour's
    plainness masked the target's dagger; here the neighbour's
    dagger masked the target's plainness.
- **The one change — sign 381 (V146).** Both passes returned Y
  from the wide crop (the tight and cell crops clip the number's
  left digits). Because the agreed verdict changes the dataset,
  the coordinator took a confirmatory look at the wide crop:
  "381" with a clear dagger; neighbour 382 plain at right.
  **Final: Y — dataset v2's N was a machine-consensus error.**
- **Finals for the 384** (the two passes' agreed verdict everywhere
  except sign 218, which takes the third look's): **154 Y, 230 N.**
  - Y: 1, 2, 8, 12, 14, 17, 28, 32, 35, 38, 40, 48, 49, 50, 51,
    53, 54, 55, 56, 57, 59, 60, 67, 68, 70, 72, 73, 74, 76, 78,
    81, 84, 86, 87, 89, 90, 91, 94, 96, 98, 102, 103, 104, 106,
    107, 109, 111, 112, 119, 120, 121, 123, 124, 125, 127, 128,
    130, 132, 136, 142, 143, 146, 149, 155, 158, 162, 169, 173,
    175, 176, 178, 180, 181, 184, 186, 190, 193, 194, 197, 198,
    201, 202, 204, 205, 206, 210, 213, 216, 228, 229, 230, 245,
    247, 252, 253, 254, 258, 259, 261, 264, 272, 275, 277, 278,
    284, 286, 287, 289, 290, 292, 294, 295, 296, 297, 298, 302,
    303, 305, 307, 312, 322, 324, 326, 327, 328, 330, 331, 332,
    334, 336, 337, 338, 340, 342, 343, 345, 347, 348, 358, 359,
    365, 367, 371, 374, 375, 381, 387, 389, 393, 394, 395, 400,
    402, 417.
  - N: 5, 6, 7, 16, 18, 20, 21, 23, 24, 25, 26, 27, 30, 31, 33,
    34, 36, 37, 39, 42, 43, 44, 45, 46, 47, 52, 58, 61, 62, 63,
    64, 65, 66, 71, 75, 77, 79, 80, 82, 83, 85, 88, 92, 93, 95,
    97, 99, 100, 101, 105, 108, 110, 113, 114, 115, 116, 117,
    118, 122, 126, 129, 131, 133, 134, 135, 138, 139, 140, 144,
    145, 147, 148, 151, 152, 153, 154, 156, 157, 160, 161, 163,
    164, 165, 166, 168, 170, 172, 174, 179, 183, 185, 187, 188,
    189, 191, 192, 195, 196, 199, 200, 203, 207, 208, 209, 211,
    212, 215, 218, 220, 221, 222, 223, 225, 226, 227, 231, 232,
    233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 246,
    248, 249, 250, 251, 255, 256, 257, 260, 262, 263, 265, 266,
    268, 269, 270, 271, 273, 274, 276, 279, 280, 281, 282, 283,
    285, 288, 291, 293, 299, 300, 301, 304, 306, 308, 309, 310,
    311, 313, 314, 315, 316, 317, 318, 319, 320, 321, 323, 325,
    329, 333, 335, 339, 344, 346, 349, 350, 351, 352, 353, 354,
    355, 356, 357, 360, 361, 362, 363, 364, 366, 368, 369, 370,
    372, 376, 377, 378, 380, 382, 383, 385, 386, 388, 390, 392,
    396, 397, 398, 399, 401, 404, 405, 406, 407, 408, 410, 411,
    412, 413, 414, 415, 416.
- Against dataset v2, 383 of the 384 finals match the carried
  value; the single change is sign 381 (N → Y).

## 3. The one-sign difference — closed, as an accounting matter

The adjudication (§3) left the dataset at 178 against the book's
printed 179 and named three candidate homes for the difference:
(i) an error in one of the 384 machine-consensus cells; (ii) one
of the six appendix-conflict cells; (iii) a difference in what the
printed total counts. This pass tested home (i) directly, and that
is where the difference lived: exactly one machine-consensus error
existed in the 384 (sign 381). Home (ii) was already resolved for
the grid by the adjudication's two visual passes, and home (iii)
no longer needs to be posited: the grid as now visually verified
in full — all 417 cells by two independent passes, with
arbitration — totals exactly the printed figure.

That the total was not fitted is itself evidenced by this pass:
the same number-report safeguard and third-look discipline that
confirmed sign 381 also struck down the only other apparent
change (sign 218), which would have carried the total to 180. A
pass willing to adjust cells to meet a printed total does not
report the removal of its own second change. Had the readings
landed on 178 or 180, that figure would stand in this record
instead.

**Dataset v3 counts: 179 Y / 238 N / 0 UNCERTAIN** — in exact
agreement with §11.4. What is closed is the accounting: no open
dagger discrepancy remains between the dataset and the book's
printed total. Nothing follows from it about the addendum signs
418/419, which sit outside the grid this dataset transcribes, or
about the Appendix I text itself.

## 4. Dataset v3

Same store, same files (not in git — the sources store is
gitignored): `glossa-corpus/indus/sources/mahadevan-1977/`

| file | bytes | SHA-256 |
|---|---|---|
| `m77_sign_list.csv` | 54,520 | `9c619bfe2520e63e2968be0ab4ddc9cef1f9aff7dfa3f8eddbf58f21fb414f7e` |
| `m77_sign_list.json` | 121,983 | `4d385e340cc780c9d59598894e73ec22887898c66b29965f632a63879d2f6976` |

The change against v2 is confined to sign 381's row (verified by
raw-line diff: exactly one data line differs): `variant_marker`
N → Y, `status` CLEAN → VERIFIED, and the `evidence` column
extended — the v2 evidence string is preserved verbatim as a
prefix, with the visual-verification entry appended (passes, third
look, final, crop names). The other 416 rows are byte-identical
to v2. The verification of the remaining 383 cells of this pass
lives in this addendum (§2), not in per-row evidence entries. v1
and v2 hashes remain in the extraction and adjudication records;
v2's files are additionally backed up in this pass's run folder.
The v3 files were rebuilt with Python's `csv` module and validated
by parsing back: 417 rows, exactly the 8 columns, no missing
keys, sign numbers 1–417 unbroken, JSON row-consistent with the
CSV.

## 5. What this establishes / what it does not

**Establishes:**

- The dagger state of all 417 sign-list cells now rests on visual
  evidence: the 33 adjudicated cells (PR #407) plus the 384 cells
  of this pass, each read by two independent blind passes with
  number-report framing checks, disagreements and framing cases
  arbitrated on wide crops. No cell in the dataset rests on
  machine consensus alone, and no UNCERTAIN flags remain.
- The extraction's machine consensus was wrong in exactly 1 of the
  384 cells it carried (sign 381) — a per-cell error rate of about
  0.26% for the consensus procedure as applied, now measured rather
  than assumed.
- The dataset's dagger total agrees with the book's printed total
  (§11.4: 179), closing the discrepancy the adjudication left open
  — as an accounting matter, per §3.

**Does not establish:**

- Anything about the Appendix I variant lists themselves (their
  unstable parse stands as the extraction record left it), the
  addendum signs 418/419, any occurrence count, or any
  identification, reading, or meaning for any sign. (As the
  extraction record §2 establishes, M77 prints no per-sign
  identifications.)

---

*Provenance of this addendum: full verification executed
2026-10-25. Run records (renders, crops, pass files, sealed
mapping, reconciliation, third looks, finals, scripts
`verify_crops.py` / `reconcile.py` / `rebuild_v3.py`, and the v2
file backup) preserved in `~/workspace/glossa-run/m77-verify/` on
the VM; source renders also reproducible at will from the pinned
scan (SHA-256 `ef68fe8d…e110`).*
