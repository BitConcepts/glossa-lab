# M77 sign list — visual adjudication addendum (2026-10-25)

**Status: EXECUTED.** The 30 UNCERTAIN dagger flags left open by the
sign-list extraction (record: `m77_sign_list_extraction_2026-10-25.md`,
PR #405), together with the 3 spot-check-unconfirmed dataset-Y signs
(182, 391, 403), have been read visually from the preserved 300-dpi
page renders. All 33 are settled. This addendum reports the outcome
cell by cell and issues dataset v2. It applies no census rules and
draws no conclusion about any sign's identity.

## 1. Method

- **Source images.** The extraction's 300-dpi renders of PDF
  pp. 44–47 (printed pp. 32–35), preserved on TRISTEN-DESKTOP under
  `~/m77extract/render300/`. Cells were located with the extraction's
  fixed grid geometry (column anchors, row origin and spacing, page
  ranges), and three crops were cut per cell: a tight 2×-enlarged
  number crop, a native whole-cell crop, and a wide context crop
  showing the neighbouring cells. The crops were transferred as files
  (desktop → relay repository commit
  `5363b3e6c12f78a3daefbb267bfcec5899f53b2b` → contents API) and all
  111 crop files were verified to decode before any reading. Images
  were read directly from files — the conversation-carried route
  whose corruption forced the extraction's deviation is not used
  anywhere in this pass, and the renders proved crisp: every target
  number was legible.
- **Two independent visual passes.** Pass A read the enlarged number
  crops, consulting the whole-cell or wide crop where the number fell
  outside the tight frame. Pass B, by a second reader working blind —
  no access to pass A, to the dataset, or to the code→sign mapping —
  read the whole-cell crops and reported the printed number it saw in
  each cell alongside its verdict, so that a crop framing the wrong
  cell would expose itself. It did, once (§2).
- **Calibration.** Four cells whose values the extraction's
  spot-check had already confirmed from 300-dpi wide crops (151 N,
  297 Y, 371 Y, 406 N) were mixed into both passes under the same
  neutral codes. Both passes read all four correctly (8 of 8 reads).
- **Disagreement rule.** A disagreement between the passes is settled
  by a third look at the wide context crop; a cell no look can settle
  stays UNCERTAIN. No verdict was taken from the running dagger
  total: the §11.4 comparison in §3 is reported after the fact, as it
  fell out.
- **Framing note.** Printed numbers sit roughly centred under their
  drawn forms rather than on a strict left edge, so a tight crop can
  frame a neighbour's number. In every adjudicated cell the number
  actually read is on record (dataset evidence entries name the
  crops); where the tight crops framed the neighbour (sign 219), the
  wide crop is the cited evidence.

## 2. Results

The passes agreed on every cell where both read the intended sign
(36 of 37 coded cells). The one exception was framing, not judgement:
for sign 219 the tight and whole-cell crops framed the neighbouring
cell 218, which pass B duly read and reported as "218, plain" — its
own number report exposed the framing. The third look at the wide
crop shows both cells: 218 plain, and 219 with a clear dagger. Sign
219's final is Y.

| sign | v1 | pass A | pass B | final |
|---|---|---|---|---|
| 3 | UNCERTAIN | N | N | **N** |
| 4 | UNCERTAIN | N | N | **N** |
| 9 | UNCERTAIN | Y | Y | **Y** |
| 10 | UNCERTAIN | N | N | **N** |
| 11 | UNCERTAIN | N | N | **N** |
| 13 | UNCERTAIN | N | N | **N** |
| 15 | UNCERTAIN | Y | Y | **Y** |
| 19 | UNCERTAIN | Y | Y | **Y** |
| 22 | UNCERTAIN | N | N | **N** |
| 29 | UNCERTAIN | Y | Y | **Y** |
| 41 | UNCERTAIN | N | N | **N** |
| 69 | UNCERTAIN | Y | Y | **Y** |
| 137 | UNCERTAIN | Y | Y | **Y** |
| 141 | UNCERTAIN | Y | Y | **Y** |
| 150 | UNCERTAIN | Y | Y | **Y** |
| 159 | UNCERTAIN | Y | Y | **Y** |
| 167 | UNCERTAIN | Y | Y | **Y** |
| 171 | UNCERTAIN | Y | Y | **Y** |
| 177 | UNCERTAIN | Y | Y | **Y** |
| 182 | Y (unconfirmed) | Y | Y | **Y** |
| 214 | UNCERTAIN | Y | Y | **Y** |
| 217 | UNCERTAIN | Y | Y | **Y** |
| 219 | UNCERTAIN | Y | N (neighbour 218) | **Y** (third look) |
| 224 | UNCERTAIN | Y | Y | **Y** |
| 244 | UNCERTAIN | Y | Y | **Y** |
| 267 | UNCERTAIN | Y | Y | **Y** |
| 341 | UNCERTAIN | Y | Y | **Y** |
| 373 | UNCERTAIN | Y | Y | **Y** |
| 379 | UNCERTAIN | Y | Y | **Y** |
| 384 | UNCERTAIN | Y | Y | **Y** |
| 391 | Y (unconfirmed) | Y | Y | **Y** |
| 403 | Y (unconfirmed) | Y | Y | **Y** |
| 409 | UNCERTAIN | N | N | **N** |

**The appendix/grid conflicts are resolved for the grid.** All six
signs the Appendix I parse listed but every grid reading called plain
(3, 4, 10, 11, 13, 22) were read as plain by both visual passes on
crisp images: no dagger is printed for any of them. The appendix
parse — the extraction record's named-weak witness, recovered
unstably at 106–115 of 179 — is not sustained for these six.

**The spot-check three are confirmed.** 182, 391 and 403 all carry
clearly printed daggers, visible at 300 dpi once the full cell is
framed; their dataset-Y values stand, now on visual evidence.

**Sign 41**, which no OCR engine could read on the first passes, is
visually unremarkable: "41" plainly printed, no dagger (the
horizontal stroke at the digit's left is the crossbar of this
typeface's 4, as in 244 and 409).

## 3. Totals, and the one-sign difference — reported as it fell out

- Adjudicated: **33 of 33 settled — 25 Y, 8 N, 0 still illegible.**
  Of the 30 UNCERTAIN: 22 resolved Y, 8 resolved N. No UNCERTAIN
  flags remain in the dataset.
- **Dataset v2 counts: 178 Y / 239 N / 0 UNCERTAIN.**
- §11.4 states 179 signs have variants. The v1 dataset bracketed
  that total (156 ≤ 179 ≤ 186); with every open flag now settled by
  two agreeing visual passes, the dataset's dagger total is **178 —
  one short of the book's printed 179.** This is stated as an open
  discrepancy, not absorbed: no cell was adjusted to meet the
  printed total. Where the one sign lives is not established by this
  pass. The named possibilities are: (i) an error in one of the 384
  unadjudicated machine-consensus cells (this pass re-read only the
  33 open/unconfirmed cells plus 4 calibrators); (ii) one of the six
  appendix-conflict cells, if the appendix witness is right against
  both the grid readings and both visual passes; (iii) a difference
  in what the printed total counts (its basis is the book's own, and
  the two addendum signs 418/419 sit outside the grid this dataset
  transcribes). A future pass that wants the missing dagger knows
  exactly where to look; this one reports the grid as it reads.

## 4. Dataset v2

Same store, same files (not in git — the sources store is
gitignored): `glossa-corpus/indus/sources/mahadevan-1977/`

| file | bytes | SHA-256 |
|---|---|---|
| `m77_sign_list.csv` | 54,349 | `ec26651f1bcbb3081ee4cc4e0ce3c5c4b6e4aed104c6a581397947c6cf75caff` |
| `m77_sign_list.json` | 121,812 | `774e886457771d0be4e0c81dbfb800f8abc0846c93d251217577999efa25516d` |

Changes against v1 are confined to the 33 adjudicated rows (verified
by row diff): `variant_marker` set to the final verdict for the 30
resolved signs (the 3 confirmations keep their Y), `status` set to
ADJUDICATED for all 33, and the `evidence` column extended — the v1
evidence string is preserved verbatim as a prefix, with the visual
entry appended (passes, third look where taken, final, and the crop
names). The other 384 rows are byte-identical to v1. v1's hashes
remain in the extraction record; nothing there is rewritten. The v2
files were rebuilt with Python's `csv` module and validated by
parsing back: 417 rows, exactly the 8 columns, no missing keys,
sign numbers 1–417 unbroken, JSON row-consistent with the CSV.

## 5. What this establishes / what it does not

**Establishes:**

- The dagger state of all 30 formerly UNCERTAIN signs is settled by
  two independent, agreeing visual passes (22 Y, 8 N); the dataset
  carries no UNCERTAIN flags.
- The 3 spot-check-unconfirmed Y signs (182, 391, 403) are visually
  confirmed.
- The six appendix/grid conflicts resolve for the grid: no dagger is
  printed for 3, 4, 10, 11, 13 or 22.
- The extraction §7's remaining visual item is done for the sign
  list: the preserved renders support direct visual reading, and the
  deviation that forced machine consensus is remedied for these
  cells.

**Does not establish:**

- The location of the one-sign difference between the dataset's
  dagger total (178) and the book's printed 179 (§3) — open, named,
  not absorbed.
- The dagger state of the 384 unadjudicated cells beyond the
  extraction's machine consensus; they were not re-read here.
- Any identification, reading, or meaning for any sign; any
  occurrence count; anything about decipherment. (As the extraction
  record §2 establishes, M77 prints no per-sign identifications.)

---

*Provenance of this addendum: adjudication executed 2026-10-25.
Renders and crops preserved on TRISTEN-DESKTOP (`~/m77extract/`,
crops under `~/m77extract/adjudicate/`); run records (pass files,
mapping, verdicts, scripts `adj_crops.py` / `rebuild_v2.py`) in
`~/workspace/glossa-run/m77-adjudicate/` on the VM.*
