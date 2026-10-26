# Wells 1998 sign-list extraction — record (2026-10-25)

**Status: EXECUTED** (commissioned 2026-10-25 as the second witness
extraction for the Spec 071 trigger census / M7 preparation, sibling of
the M77 extraction, PR #405; extraction completed 2026-10-26). The sign
list of Bryan K. Wells' 1998 MA thesis — Appendix I, Table 3.2 "Signs
Sorted by Sign Number" — has been transcribed into a machine-readable
dataset: one row for each of the 588 sign numbers, carrying Wells'
printed total, varieties count, set, class, type, and the four site
frequencies, plus his printed Mahadevan cross-references (Figure 3.6)
and every per-sign identification he states. Transcription only — no
census rules were applied, no thresholds were tested, and no
conclusion about any sign's identity is drawn or implied.

**Source.** The pinned scan recorded in this directory's
`provenance.yaml` (UMI scan, Dissertation # MQ31309, of the University
of Calgary MA thesis "An Introduction To Indus Writing," January
1998; 12,298,934 bytes; 295 PDF pages; SHA-256
`5720dc010acc68d6b50827fa89fb7bf3c4c0eb0aee67597e7662e5fd74508906`).
The hash was re-verified at the start of this extraction and again
after a virtual-machine replacement during the work, and matched
exactly both times. The PDF itself is held in the research-notes
store and is not in git. Printed page = PDF page − 10 throughout.

**Dataset (not in git — the sources store is gitignored):**
`glossa-corpus/indus/sources/wells-1998/`

| file | bytes | SHA-256 |
|---|---|---|
| `wells1998_sign_list.csv` | 241,828 | `22bde128551adbd6d91cd76bb41b4f40199ab3e45af76d500a1008d27c5bea95` |
| `wells1998_sign_list.json` | 518,824 | `bdcb8ef32f5172e4d1ddbb057e4344bccbc7aeacc1928d86c2175c12290a4bf0` |
| `wells1998_fig36_crossrefs.csv` | 1,125 | `b0ef40da7cd65cdcb6910fd2b1e6aeae4eac47cb31cbe2b2c6205f2ac5da270d` |

The CSV was built with Python's `csv` module and validated by parsing
it back: 588 data rows, exactly 17 columns per row, no missing keys,
sign numbers running 1–588 with no gap (sign 407 is present as a row
and marked NOT PRINTED — see §1). The JSON file is the same 588 rows
plus two fields the CSV flattens (`attestation_ocr_raw`,
`identifications_full`), checked consistent with the CSV. The Fig.
3.6 file carries the 24 cross-reference rows of §4.

Columns: `sign_no`, `total`, `varieties`, `set`, `class_code`,
`type_code`, `freq_mohenjo_daro`, `freq_harappa`, `freq_lothal`,
`freq_other_sites`, `percent_by_site` (recomputed from the
frequencies against Wells' printed site totals; Wells' own printed
percent row is the validation source, kept in the evidence),
`page_pdf`, `page_printed`, `status` (CLEAN / CLEAN-DERIVED /
UNCERTAIN / NOT PRINTED), `mahadevan_xref_fig36`, `identifications`,
`evidence` (every reading that went into the row's values, kept per
sign).

Result counts: 587 printed entries — total, class and page present
for all 587; complete four-site frequency rows for 562; varieties for
451; set for 519. Statuses: CLEAN 250, CLEAN-DERIVED 182, UNCERTAIN
155, NOT PRINTED 1.

---

## 1. The list as printed — 588 numbers, 587 entries, one gap

Appendix I (PDF pp. 146–295, printed pp. 136–285) reprints Chapter 3's
Table 3.2, "Signs Sorted by Sign Number." Each entry prints a glyph
row (drawn forms, lettered a, b, c … where more than one form is
drawn), a header (Sign #, Total, Varieties, Set), a frequency table
(counts for Mohenjo-Daro, Harappa, Lothal and Other sites, with a
percent row giving each count as a percentage of that site's
reference total), a Class code box and a Type code box at the right,
and the attestation list (artefact numbers by site and variety)
below. Cells with a zero count are printed blank. The longest entries
are printed twice — once in sequence and again full-width at the end
of the appendix (signs 288, 193, 112 on printed pp. 283–285; sign
193's in-sequence entry carries the diagonal instruction "see end
table"). All three duplicate printings were captured independently
and agree (see §5).

**Sign 407 has no entry.** The numbering runs 406 → 408 on PDF
p. 247; the neighbouring pages (PDF pp. 246–248, holding signs
401–413) were read visually in full, and the thesis text layer
contains no "Sign # 407" header (its six "407" strings are artefact
numbers M-407 / H-407 inside other entries). The dataset therefore
carries sign 407 as an explicit row marked NOT PRINTED. The table as
printed carries 587 entries over the numbers 1–588, which matches
Wells' Chapter 3 count of 587 signs; sign 588 (printed p. 282) is
itself marked in the table as a late addition ("see Parpola
1994:111-2 — Late addition"), total 10, Class CMP, Set 21.

Wells' own Chapter 3 checksum figures (printed p. 48–49) are: 587
signs, 802 varieties, 7,121 references, broken down as Mohenjo-Daro
4094 / Harappa 2154 / Lothal 360 / Minor sites 523, and 284 signs
occurring once. The four site figures sum to 7,131, not 7,121 — a
printed inconsistency in the thesis itself; the table's percent rows
are computed on 4094 for Mohenjo-Daro (verified on multiple entries),
so 4094/2154/360/523 are the denominators used here. §5 reports the
extraction against every one of these figures.

## 2. The celestial question — answered from the thesis

The trigger census's live question for this witness is whether Wells
1998 identifies any signs as celestial (sun / star / sky / planet
class) in his own voice. **He does not. No sign in the thesis is
identified as celestial by Wells.**

The only celestial identification anywhere in the thesis is
**Parpola's** proposal for **sign 112**, which Wells reports in order
to reject it (printed p. 99, PDF p. 109; verified verbatim on the
page image). Parpola "proposes that its primary meaning in the Indus
inscriptions is 'star' (Parpola 1994:182)" and reads seal H-9 as
"seven star," equating "seven stars" with the Pleiades. Wells:
*"I agree that sign 112 is most likely a representation of a fish…
in this case a fish is just a fish."* Under the census instrument's
binding reported-speech amendment, sign 112's "star" is coded
**REPORTED-NOT-ADOPTED** and is excluded from both census totals;
Wells' own adopted identification for 112 is "fish."

So Wells 1998, like Mahadevan 1977, cannot be the exhibited list that
reopens Spec 071's trigger on celestial identifications: neither
named witness identifies a single celestial sign in its own voice.

For completeness, every per-sign identification Wells states is in
the dataset's `identifications` column (full wording in the JSON
twin's `identifications_full`), each with its printed page and its
status under the reported-speech rule:

| sign | identification as printed | status | page |
|---|---|---|---|
| 112 | a fish (representation) | ADOPTED | printed 99 |
| 112 | 'star' — Parpola 1994:182; "seven stars" = the Pleiades (seal H-9) | REPORTED-NOT-ADOPTED (expressly rejected by Wells) | printed 99 |
| 338 | 'hare', *keviyan (the sign alternating with the hare picture; components 306 + 342) | ADOPTED-TENTATIVE | printed 117 |
| 306 | *kev(i) 'ear' | ADOPTED-TENTATIVE | printed 118–119 |
| 342 | *yan, first-person oblique ending / pronoun 'I' (also possible verbal case marker) | ADOPTED-TENTATIVE | printed 99, 118–119 |
| 288 | *-ay / *-ai case ending (syllabic value) | ADOPTED-TENTATIVE | printed 120 |
| 345 | 'drum / drummer' (parai, DED 3319); phonetic value stated unknown | ADOPTED-TENTATIVE | printed 120 |
| 412 | rhinoceros horn, a logograph of an item of trade | ADOPTED | printed 121 |
| 414 | 'crown' (Knorozov, Albedil & Volchok 1981:82); 'mountains' (Parpola 1994:58); one drawn variety "more like a group of tents (Ta. Kutaram)" is Wells' own tentative remark on the form | REPORTED (both); form remark ADOPTED-TENTATIVE | printed 54 |
| 2 | a deity, predecessor of Yama (Knorozov 1968:21, quoted; Wells dismisses Knorozov's readings) | REPORTED-NOT-ADOPTED | printed 87 |
| 195 | *ir 'two' (McAlpin 1981:42) | REPORTED | printed 120 |

Class-level positions, for the record: Wells argues the stroke signs
carry weights-and-measures values, "not numerals per se" (printed
pp. 47–48) — his own argued position about a class, not a per-sign
identification. He groups signs 193, 196 and 231 functionally as
"markers" (after Parpola); note that Table 3.2 itself classes 196 as
SIM (Type Str) — the table's class governs the dataset, and the
prose/table divergence is recorded here rather than reconciled. A
"calendric (lunar) function" remark at printed p. 35 concerns ivory
rod **artefacts**, is attributed to Fairservis 1992, and is not a
sign identification; it was checked and excluded.

## 3. Method, and the deviations that must be read with the dataset

The thesis's embedded text layer (Acrobat Paper Capture, 1999) could
not carry this extraction: it drops the frequency tables and the
class/type boxes entirely, covers headers for only 252 of 587
entries, and scrambles the header token order — its Varieties and Set
assignments fail validation outright (e.g. sign 276's "set" comes out
as 276, its own sign number; sign 538's "varieties" as 37 against the
printed 802-variety bracket). Those two UMI fields were therefore
**not used**; the UMI total was retained as one cross-check among
several, since totals are independently validated by the frequency
arithmetic.

Primary engine: fresh OCR (RapidOCR) over new 300-dpi page renders,
with a second, targeted strip re-OCR (521 entry crops at 1.5×–2×) for
every entry whose first pass left a field missing or conflicted.
Values were settled by per-field consensus across all captures of an
entry — including both printings of the three duplicated entries —
with three arithmetic completion rules, each flagged **DERIVED** in
the row's evidence wherever it fires: (i) a frequency cell printed
blank is zero, entered only when the cell is unoccupied in every
capture **and** the row then closes exactly on the printed total;
(ii) a missing cell is the residual of the printed total over the
known cells; (iii) a raw cell that contradicts its own printed
percent is replaced by the percent-derived value (this is what
corrects sign 112's in-sequence Mohenjo-Daro cell, OCR'd "811," to
the printed 118, confirmed by its printed percent 2.88 and by the
duplicate printing). One further deduction is flagged wherever used:
a sign with total 1 has varieties 1 (a single attestation has a
single form).

**Glyph-row letters were tested as a varieties source and rejected
on the thesis's own evidence**: sign 149 prints Varieties 3 under
four lettered drawings (a–d); sign 420 prints Varieties 1 under two
lettered forms (the second is noted in its entry as an intermediate
form); sign 543 prints Varieties 6 under five lettered drawings.
Letters label drawings, not distinct forms. The printed Varieties
digit is the only authority used (plus the total-1 deduction above).

**Deviation (named, as in the M77 record):** no independent human
double-keying was performed. In its place: multi-capture machine
consensus under the arithmetic brackets of §5, plus visual
adjudication by the extractor reading the page images directly —
40 signs adjudicated from 22 pages (PDF pp. 152, 164, 166, 168, 174,
183, 188, 194, 196, 218, 230, 232, 246–251, 280, 281, 285, 288),
including every structural problem the machine passes left behind
(the two anchor-less entries 89 and 172, the misplaced record of
152, the sign-407 gap, sign 414's row, sign 84's header, sign 560's
Mohenjo-Daro cell). As a control, 52 further entries on those same
pages that needed no adjudication were read visually in full and
compared against the dataset: **52 of 52 confirmed** on total and
all four frequencies, none contradicted. The page renders and all
OCR captures are preserved in the extraction workdir, so any future
pass can re-adjudicate from the same images.

## 4. Reference data carried with the extraction

**Cross-references to Mahadevan.** Table 3.2 prints no Mahadevan
numbers — the M-/H-/L- numbers inside its entries are artefact
numbers (e.g. "Mohenjo-daro: M-262"), not sign numbers. The only
Mahadevan cross-references Wells 1998 prints are in **Figure 3.6**
(printed p. 77, PDF p. 87): 24 example glyph rows comparing the
Mahadevan 1977, Fairservis 1992, Parpola 1994 and Wells 1997
divisions of the same material. Expanding Wells' ranges gives 55
Wells→M77 pairings over 17 distinct Mahadevan targets, carried in the
dataset's `mahadevan_xref_fig36` column and in
`wells1998_fig36_crossrefs.csv`. They are worked examples, not a
concordance: they include "352?" exactly as printed, and one row
(Wells 382) with no Mahadevan counterpart. One further printed
cross-note exists inside an entry: sign 338 — "see Parpola
(1992:112; fig. 7.14) Class C2, cf. B7 for replacement set."

**Registry join.** Wells-1998 sign numbers do **not** join to
Registry v2's `wells_ids`: those tokens (W001–W958) key Wells 2015,
not this thesis (see the repository's Phase-122 crosswalk report;
the same phase recorded that no machine-readable Parpola↔Mahadevan
table is extractable from Wells 1998/2006). 436 of the thesis
numbers 1–587 share a number with a W-token and 272 W-tokens exceed
587, but numeric coincidence does not establish identity. For census
purposes, Wells-1998 signs are **UNMAPPED** to Registry v2 except
through Figure 3.6's 55 glyph-anchored pairings (via M77).

**Wells' classes** (Chapter 3, printed p. 46, and Fig. 3.1): SIM
Simple 127 (Mirror 9, Stroke 24, Other 94), CMX Complex 175, CMP
Compound 135, MKD Marked 146, MKR Marker 3 — the printed class
counts sum to 586 against 587 signs, Wells' own arithmetic again not
fully reconciled; reported as printed. "Set" is Wells' gross-
resemblance grouping (defined printed p. 50): 63 sets, including
fractional values (1, 1.5, …) and at least some three-part values
(21.5.3 is printed for signs 291 and 292; the dataset's set column
carries the machine-read leading value there).

## 5. Bracket checks, conflicts and gaps — named, never guessed

**Bracket checks against Wells' printed figures:**

- **Entries:** 587 printed entries extracted (every one with total,
  class and page) over the 588 numbers — Wells' printed count: 587.
- **Totals:** the 587 totals sum to 7,158. Wells prints 7,121
  (prose) and site totals summing to 7,131. The three figures
  disagree by ≤ 0.5 %; Wells' own two already disagree by 10. Every
  complete frequency row in the dataset sums exactly to its printed
  total (562 rows, no exceptions after adjudication).
- **Site columns:** over the 562 complete rows the columns sum to
  Mohenjo-Daro 4102 / Harappa 2107 / Lothal 356 / Other 511 against
  Wells' site totals 4094 / 2154 / 360 / 523. Harappa, Lothal and
  Other fall short by amounts consistent with the 25 incomplete
  rows' missing cells; **Mohenjo-Daro exceeds its printed site total
  by 8** — a named residual, within Wells' own inter-figure
  disagreement and not resolvable from the printed material (the
  52-entry visual control found no over-read cell).
- **Single-occurrence signs:** the dataset yields 291 against Wells'
  printed 284. The +7 excess sits in the known failure mode of this
  source — a faint second frequency cell, with its percent, missed
  in every capture, closing as a singleton under the blank-equals-
  zero rule — and is reported, not adjusted away.
- **Varieties:** 451 of 587 entries carry the printed count, summing
  to 639; the 136 entries without one must contribute 163 for Wells'
  printed 802 (an average of 1.20, consistent with the recovered
  distribution). Sign 4's varieties = 16, the maximum Wells names,
  is recovered exactly.
- **Classes:** dataset SIM 127 / CMX 174 / CMP 137 / MKD 147 / MKR 2
  against printed 127 / 175 / 135 / 146 / 3 — every class within 2
  of the printed count, over a printed distribution that itself sums
  to 586 for 587 signs.
- **Anchors:** sign 113 total 179 with distribution 85/78/6/10 —
  exact against Chapter 3 prose. Signs 112 (187; 118/46/8/15), 193
  (481; 278/117/42/44) and 288 (855; 472/291/34/58) — exact in both
  of their printings. (Chapter 3's prose marker counts — 193 n=180,
  196 n=82, 231 n=120 — match the table only for 196 and 231; for
  193 the prose figure conflicts with the table's 481 and was not
  used. The table as printed governs throughout.)

**Named conflicts:**

- **Sign 414.** The printed table entry (PDF p. 249) gives total 33,
  varieties 4, frequencies 26/5/1/1 with a single Kalibangan
  attestation (K-18). A Chapter 3 passage (printed p. 54) was read
  during this programme's intake work as giving Kalibangan 11 for
  this sign. The two do not reconcile; the dataset follows the table,
  and this note is the record of the divergence.
- **Sign 196's class** is SIM in the table, "marker" in the prose
  (§2). Dataset follows the table.
- **Sign 407** is not printed (§1).

**Named gaps** (all carried per-sign in the dataset's status and
evidence; nothing below was guessed):

- **Varieties unrecovered for 136 entries** (the faint serif "1" of
  the Varieties column is the single hardest glyph in this scan; it
  defeats both OCR engines in a minority of entries even at 2×):
  signs 10, 12, 13, 18, 21, 22, 23, 26, 30, 37, 68, 79, 86, 96, 99,
  107, 118, 119, 120, 121, 124, 125, 126, 127, 128, 129, 148, 160,
  161, 163, 173, 175, 176, 177, 178, 179, 180, 188, 197, 205, 207,
  209, 210, 212, 232, 233, 234, 235, 237, 238, 239, 243, 247, 248,
  249, 253, 254, 255, 256, 267, 269, 270, 283, 284, 295, 296, 298,
  306, 307, 308, 310, 311, 316, 341, 349, 350, 352, 353, 354, 355,
  356, 357, 358, 359, 361, 362, 363, 364, 367, 368, 375, 376, 389,
  392, 393, 395, 396, 397, 398, 418, 421, 422, 424, 436, 438, 448,
  451, 452, 456, 457, 469, 471, 485, 491, 492, 499, 500, 502, 506,
  510, 517, 519, 529, 530, 532, 533, 546, 548, 561, 562, 574, 575,
  576, 577, 578, 580.
- **Frequency rows incomplete for 25 entries:** signs 11, 60, 68,
  107, 122, 164, 173, 191, 229, 234, 245, 305, 309, 313, 317, 352,
  369, 435, 458, 512, 520, 528, 531, 563, 577. In each case some
  cells are present and percent-validated; the missing cells are
  named in the row's evidence.
- **Set unrecovered for 68 entries; type for 320.** The type column
  is the least-verified field in the dataset (OCR-grade values,
  including truncated forms such as "At" where engines clipped the
  code box); neither the census nor M7 consumes it, and it is
  flagged here rather than repaired by inference. The JSON twin's
  `attestation_ocr_raw` is partial for PDF pp. 260–295 (the capture
  route for those pages kept header and table boxes only); the
  dataset's fields are unaffected.
- 155 rows carry status UNCERTAIN, driven by the gaps above; 182
  rows are CLEAN-DERIVED, meaning at least one value rests on a
  flagged arithmetic completion or the total-1 deduction.

## 6. What this establishes / what it does not

**Establishes:**

- A machine-readable Wells 1998 signary exists and is bracket-
  validated against every checksum Wells prints: 587 entries, totals
  summing within 0.5 % of his figures under either of his two
  inconsistent counts, class distribution within 2 per class, the
  named anchors (4, 112, 113, 193, 288) exact.
- Wells 1998 states **no celestial identification in his own voice**
  for any sign; the thesis's only celestial identification is
  Parpola's "star" for sign 112, reported and expressly rejected
  (printed p. 99). Coded REPORTED-NOT-ADOPTED.
- Wells' complete stated-identification catalogue (11 rows, §2) is
  captured with printed pages and reported-speech statuses.
- Wells' only printed Mahadevan cross-references are Figure 3.6's
  55 example pairings; Wells-1998 numbers do not join Registry v2's
  Wells-2015 `wells_ids`. The Wells arm's census join is therefore
  UNMAPPED except through those 55 pairings.

**Does not establish:**

- That any identification Wells (or Parpola, or anyone) states is
  correct. This is a transcription of what the thesis prints.
- Anything about the census outcome. Applying the trigger census to
  either witness remains a separate owner act; this record prepares
  the second witness and reports what it contains.
- The missing fields named in §5. They are gaps in this extraction,
  recoverable by a future visual pass over the preserved renders —
  they are not zeros and were not filled by inference beyond the
  flagged rules of §3.

## 7. Readiness — what can now be consumed, and what remains

Both named witnesses for the Spec 071 trigger census are now
extracted: Mahadevan 1977 (PR #405) and Wells 1998 (this record). The
Wells dataset is consumable now, keyed by Wells-1998 sign number,
with per-sign identifications and their reported-speech statuses,
Figure 3.6's Mahadevan pairings, and full per-sign evidence.

What still stands before the census can be **applied** (application
remains the owner's separate act; nothing here applies it):

1. The joined picture is negative in a specific, reportable way:
   **neither witness identifies any celestial sign in its own
   voice** — M77 has no celestial class at all, and Wells 1998's
   only celestial identification is Parpola's, reported-and-rejected.
   Under the instrument as amended, an exhibited-list trigger claim
   cannot be built from these two witnesses' own identifications.
2. The Wells join is UNMAPPED to Registry v2 except via Figure
   3.6's 55 pairings (through M77). Under the instrument's binding
   amendment, a DOES NOT FIRE outcome is blocked while any
   identified sign is UNMAPPED or AMBIGUOUS — the census design must
   say how it treats a witness whose signs are unmapped by
   construction.
3. The instrument's occurrence conjunct (F-5: the ≥30 total is weak
   as designed; drop it or replace with a per-sign minimum, and
   record source-concordance occurrences as cross-check) still has
   to be resolved in the census design. Wells' table frequencies
   are his 1998 corpus counts and are **not** the instrument's
   primary-population occurrences; they are available as the
   source-concordance cross-check F-5 names.
4. From the M77 side, unchanged: the 30 UNCERTAIN dagger flags still
   await visual adjudication, and whether signs 418/419 belong to
   the M77 witness remains the census's call.
