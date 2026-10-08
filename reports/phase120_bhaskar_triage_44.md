# Phase-120 — Bhaskar (2024) triage of the 44 pending anchors

**Date:** 2026-10-08 · **Branch:** `phase/120-bhaskar-triage` · **Base:** main `cac0f646`
**Source:** Bhaskar, M. V. (2024), "Markers and agencies of anisotropy in the
Indus sign system", *Indian Journal of History of Science*,
doi:10.1007/s43539-023-00102-3, with Electronic Supplementary Materials
ESM1–ESM13 (article PDF + 12 ESM PDFs + ESM13 .xlsx, held in the research
notes sweep of 2026-10-08; the ESMs are external source material and are
not committed to this repo).
**AI disclosure:** executed by an AI agent (Muse Spark, via Muse)
at the direction of Tristen Pierson, per constitution §VI.

## Headline result

| Class | Count (of 44) |
|---|---|
| ALL-AGREE | **0** |
| CONTESTED | **1** (M402) |
| NOT-COVERED | **43** (16 mentioned behaviourally, 27 not mentioned) |

This is a **descriptive triage only**. It changes no anchor status,
validates nothing, and contains no PRED content (see NON-CLAIMS).

## 1. Scope finding — the ESMs are not what the commission assumed

The commission assumed the ESMs encode a per-sign disagreement table
between the Mahadevan (M77), ICIT, and CISI compilations — one row per
sign with each compilation's reading. **They do not.** Bhaskar (2024) is
a study of *anisotropy*: sign order, transposition, and the markers
(D1–D5, Dx) that signal it, built on a benchmark set of 33
frontal-sign objects (F3). Its stated method (article p. 2) is that
every sign and sign sequence *considered in the study* was subjected
to a three-way comparison between M77, ICIT, and CISI, with any
disagreement "noted in each case" — i.e. disagreements survive only
as case-level notes inside the anisotropy analysis, never as a
systematic per-sign table. What each ESM actually contains:

| ESM | Contents (verified by reading) |
|---|---|
| ESM1 (8 pp.) | F3 object catalogue: 33 objects, animal orientation, frontal/dorsal signs; Lists 1–4 (19 frontal signs, 39 dorsal signs, sign–symbol correspondence) |
| ESM2 (17 pp.) | Simulations from F3 sequences correlated with M77/ICIT; anisotropy results by D type; error type **E1** = "a corpus error, a misprint in M77 or a serious disagreement between M77 and ICIT that cannot be verified with CISI" |
| ESM3 (2 pp.) | Sign 99 as a D1 marker: its 86 base signs; signs flanking 267 |
| ESM4 (1 p.) | Behaviour of 267a and 99-267a (line-number lists) |
| ESM5 (1 p.) | 267 vs 267a against comparison signs |
| ESM6–ESM7 (2 pp. each) | Case studies: 99 infixed in 342 (→ 344) |
| ESM8 (5 pp.) | Sign doubles; base-sign lists for markers 123 (32 signs) and 97 |
| ESM9 (3 pp.) | Null simulation for sign 98 as a neutral marker |
| ESM10 (1 p.) | Sign 244 and its marked versions vs ICIT 629–642 |
| ESM11 (1 p.) | Intrinsic markers in the fish-sign family |
| ESM12 (1 p.) | Intrinsic markers outside the fish family |
| ESM13 (.xlsx) | Updated catalogue of Indus zoomorphism: 2,383 CISI object rows (animal behaviour), not sign data |

**Consequence for method.** A per-sign M77/ICIT/CISI "readings" grid
cannot be parsed from this material without fabricating it. This
phase therefore does the strongest honest version of the triage:

1. extract **every cross-source disagreement Bhaskar actually
   documents** into a machine-readable register (20 cases:
   `reports/phase120_bhaskar_disagreements.csv` / `.json`);
2. build a **mention index** recording which list-structured ESM
   contexts mention each sign number at all (behavioural attestation
   only);
3. classify the 44 strictly from (1): a sign is CONTESTED only when
   a documented case names its identity/form class; **ALL-AGREE is
   never inferred from silent use**, because Bhaskar records no
   per-sign concordance statements (ESM2's concordance notes are
   sequence-level, for F3 strings, and concern sign *order*).

## 2. Method

- **Anchors.** `backend/reports/INDUS_FINAL_ANCHORS.json` was read
  (SHA-256 asserted unchanged after the run; the file was not
  modified). Anchors are keyed by Mahadevan number (`M###`); Bhaskar
  cites signs by the same Mahadevan numbers, so **no crosswalk is
  needed for sign identity**. The 44 with
  `validation_status == "pending_non_sa_validation"` were verified
  to number exactly 44 (43 HIGH + M293 MEDIUM), matching specs
  011/014/016/017.
- **Disagreement extraction.** Keyword sweep of the article + all
  ESM text layers for: `conflat*`, `disagree*`, `E1`, `misprint`,
  `normalis*`, `doubtful`, `proxy`, `stand-alone`, `omits`,
  "settles it in favour of", "vastly different", "does not have",
  `reckon*`. Every hit was hand-read in context; surviving cases
  were encoded as the register in
  `backend/glossa_lab/phase120_bhaskar.py` with exact locations
  (ESM + row/case + PDF page). Case summaries are in our own words;
  no passage of Bhaskar's text is reproduced beyond brief method
  description.
- **Mention index.** Sign numbers were extracted from the
  list-structured contexts (ESM1 Lists 1–2; ESM3 Lists 1–2; ESM5
  comparison rows; ESM8 doubling entries and Lists 1–2) where the
  text layer pairs each glyph with its Mahadevan number.
- **Classifier.** `classify_anchor` in the same module: dispute-kind
  case naming the sign → CONTESTED; else NOT-COVERED with subflag
  `mentioned_behaviourally` / `not_mentioned`. ALL-AGREE is
  unreachable by design (see §1).
- **H23.** Graph node `IndusPhase120BhaskarTriage` was registered in
  `ATOMIC_NODES` and asserted before the phase script ran.

### Mapping assumptions (complete list)

1. Anchor key `M###` ≡ Bhaskar's bare sign number `###` (both are
   Mahadevan 1977 numbering, per the article §1.1). No Wells/Parpola
   conversion is involved anywhere in this phase.
2. A disagreement "names" a sign only if the passage adjudicates
   that sign's own identity or form class. Sequence neighbours of a
   disputed reading are recorded as `context_signs` and never make a
   sign CONTESTED (e.g. M028 sits in the C-23 sequence of case
   BH-D12, an omission concerning an unnumbered element — M028 is
   NOT-COVERED).
3. Bhaskar's own form-reanalyses (fish family as marked versions of
   59; 343/344/345 as 342 + marker; 303 = 287 + 299; 172 as a marked
   171) are registered separately as `form_reanalysis` (BH-R01–R04),
   **not** as inter-compilation disputes: they are Bhaskar's thesis
   against both inventories, not a disagreement *between* M77, ICIT,
   and CISI. Two of the 44 fall under this note — **M072** (a putative
   marked version of 59 in BH-R01) and **M345** (342 + 102 in BH-R02)
   — and both are classified NOT-COVERED with this paragraph as the
   record, rather than inflating CONTESTED with a different kind of
   claim.
4. ESM13 (animal behaviour) carries no per-sign data and contributes
   no mentions.
5. The ESM8 base-of-97 list is used as extracted; the article itself
   flags that count as the less certain of the two marker lists —
   one more reason mention ≠ concordance here.

## 3. The one CONTESTED anchor: M402

**BH-D10 (coverage gap).** ESM1's note on object K-39 records that its
frontal sign — the flag/banner, sign 402 — waves *left*. No
left-waving variant of 402 exists in M77, in ICIT, or in the Indus
font package; the only other left-waving instance (object 7065,
L-115) is doubted by Bhaskar to be 402 at all, or even a variant of
it. What disagrees with what: **the CISI object's form vs. every
compilation's inventory of sign 402** — a unanimous coverage gap plus
a doubted attribution, *not* a source-vs-source split. It is the only
passage in the article + ESMs that contests the identity/form class
of any of the 44 signs.

All other documented disputes concern signs outside the 44 —
notably 267 vs 267a (BH-D01), 97/98 and 99/100 conflations in ICIT
(BH-D02/03), the 244 normalisation split M77-vs-ICIT (BH-D05), two
labelled E1 corpus errors (BH-D07: 4827 vs ICIT 231; BH-D08: C-79),
the prose E1 at ESM7 case 7, the M77 misprint of 257 as 197
(BH-D06), and the classification dispute over 162 (BH-D11). The full
register (16 dispute cases + 4 reanalysis notes) is in
`phase120_bhaskar_disagreements.{csv,json}`.

## 4. Per-sign triage of the 44

Counts: **ALL-AGREE 0 · CONTESTED 1 · NOT-COVERED 43**
(NOT-COVERED = 16 mentioned behaviourally + 27 not mentioned).
"Mention sources" list only the parsed list contexts of §2; full
rationales per sign are in `phase120_bhaskar_triage_44.json`.

| Sign | Reading | Tier | Class | Subflag | Mention sources |
|---|---|---|---|---|---|
| M011 | kaḷiṟu | HIGH | NOT-COVERED | not_mentioned | — |
| M021 | kō | HIGH | NOT-COVERED | not_mentioned | — |
| M024 | nē | HIGH | NOT-COVERED | not_mentioned | — |
| M028 | cōḻ | HIGH | NOT-COVERED | mentioned_behaviourally | ESM1 list2 dorsal, ESM3 list1 base of 99 |
| M031 | kai | HIGH | NOT-COVERED | not_mentioned | — |
| M033 | puli | HIGH | NOT-COVERED | not_mentioned | — |
| M035 | po | HIGH | NOT-COVERED | not_mentioned | — |
| M036 | tiru | HIGH | NOT-COVERED | not_mentioned | — |
| M040 | ri | HIGH | NOT-COVERED | mentioned_behaviourally | ESM8 list2 base of 97 |
| M058 | ke | HIGH | NOT-COVERED | not_mentioned | — |
| M071 | nal | HIGH | NOT-COVERED | not_mentioned | — |
| M072 | mā | HIGH | NOT-COVERED | mentioned_behaviourally | ESM8 list2 base of 97 |
| M102 | ni | HIGH | NOT-COVERED | mentioned_behaviourally | ESM1 list2 dorsal |
| M103 | kol | HIGH | NOT-COVERED | not_mentioned | — |
| M127 | vē | HIGH | NOT-COVERED | mentioned_behaviourally | ESM3 list2 flanking 267, ESM5 comparison signs, ESM8 doubling signs, ESM8 list2 base of 97 |
| M149 | or | HIGH | NOT-COVERED | mentioned_behaviourally | ESM3 list2 flanking 267 |
| M153 | pu | HIGH | NOT-COVERED | not_mentioned | — |
| M155 | ka | HIGH | NOT-COVERED | mentioned_behaviourally | ESM3 list1 base of 99, ESM3 list2 flanking 267, ESM8 list2 base of 97 |
| M168 | inci | HIGH | NOT-COVERED | not_mentioned | — |
| M169 | rā | HIGH | NOT-COVERED | mentioned_behaviourally | ESM3 list1 base of 99, ESM8 list1 base of 123, ESM8 list2 base of 97 |
| M177 | na | HIGH | NOT-COVERED | mentioned_behaviourally | ESM3 list1 base of 99 |
| M178 | i | HIGH | NOT-COVERED | not_mentioned | — |
| M183 | vēḷ | HIGH | NOT-COVERED | not_mentioned | — |
| M223 | muḷ | HIGH | NOT-COVERED | mentioned_behaviourally | ESM3 list1 base of 99 |
| M235 | vē | HIGH | NOT-COVERED | not_mentioned | — |
| M237 | ce | HIGH | NOT-COVERED | mentioned_behaviourally | ESM8 doubling signs |
| M239 | il | HIGH | NOT-COVERED | not_mentioned | — |
| M254 | tēṉ | HIGH | NOT-COVERED | mentioned_behaviourally | ESM3 list1 base of 99 |
| M262 | i | HIGH | NOT-COVERED | not_mentioned | — |
| M270 | muḷ | HIGH | NOT-COVERED | mentioned_behaviourally | ESM3 list1 base of 99 |
| M272 | ma | HIGH | NOT-COVERED | not_mentioned | — |
| M281 | piLLai | HIGH | NOT-COVERED | not_mentioned | — |
| M293 | ta | MEDIUM | NOT-COVERED | mentioned_behaviourally | ESM3 list1 base of 99, ESM3 list2 flanking 267, ESM8 doubling signs, ESM8 list1 base of 123, ESM8 list2 base of 97 |
| M304 | vēṟ | HIGH | NOT-COVERED | not_mentioned | — |
| M332 | intu | HIGH | NOT-COVERED | not_mentioned | — |
| M345 | taṭ | HIGH | NOT-COVERED | not_mentioned | — |
| M350 | vē | HIGH | NOT-COVERED | mentioned_behaviourally | ESM3 list1 base of 99 |
| M355 | lu | HIGH | NOT-COVERED | not_mentioned | — |
| M365 | vāṉ | HIGH | NOT-COVERED | not_mentioned | — |
| M383 | kol | HIGH | NOT-COVERED | not_mentioned | — |
| M401 | vē | HIGH | NOT-COVERED | not_mentioned | — |
| M402 | vēḷ | HIGH | CONTESTED | coverage_gap | ESM1 list1 frontal, ESM3 list1 base of 99, ESM3 list2 flanking 267, ESM8 list1 base of 123, ESM8 list2 base of 97 |
| M412 | cūḷ | HIGH | NOT-COVERED | mentioned_behaviourally | ESM8 list1 base of 123 |
| M416 | na | HIGH | NOT-COVERED | not_mentioned | — |

## 5. Sanity check (hand-reading vs parse)

Fourteen items were hand-read in the ESM/article PDFs (page images'
text layer read in full context, locations verified by in-document
search) and compared against the parsed register/index:

| # | Item hand-read | Location | Parse agrees? |
|---|---|---|---|
| 1 | E1 definition ("corpus error… M77… ICIT… CISI") | ESM2 p. 1 | yes |
| 2 | E1 block, 4827 vs ICIT 231 (row 14c) | ESM2 p. 5 | yes |
| 3 | E1 block, C-79 "vastly different readings" (row 28f1) | ESM2 p. 15 | yes |
| 4 | Misprint: 2518 reports 257 as 197 (row 25) | ESM2 p. 14 | yes |
| 5 | 162 stand-alone (M77) vs proxy (ICIT), M-223 (row 13) | ESM2 p. 2 | yes |
| 6 | Prose E1 at 1125; CISI settles 1090 for M77 | ESM7 p. 1 | yes |
| 7 | 402 left-waving note, K-39 / 7065 | ESM1 p. 4 | yes |
| 8 | Row 23: ICIT 002 taken as M77 100 | ESM1 p. 5 | yes |
| 9 | ESM3 List 1 membership: 155, 169, 177, 223, 254, 270, 293, 350, 402 | ESM3 p. 1 | yes (9 numbers) |
| 10 | ESM8 entry 26 (sign 293 doubles) + List 1 membership of 293/402 | ESM8 pp. 3–4 | yes |
| 11 | ESM10 rows: 244 family vs ICIT 629–642; 244k compound note | ESM10 p. 1 | yes |
| 12 | ESM5 comparison row for 59 (267 vs 267a) | ESM5 p. 1 | yes |
| 13 | Article §8.1: M77 normalises two distinct forms to 244 | Article p. 21 | yes |
| 14 | ESM13 structure: CISI-ID rows, animal-behaviour columns | ESM13 .xlsx | yes |

**Parse accuracy: 14/14 hand-checked items correct.** Known error
modes, stated honestly: (i) the ESM glyphs live in a private-use
font, so sign *numbers* (not glyph shapes) are what the text layer
yields — every register claim rests on numbers + prose, both
hand-verified above; (ii) automated label-pattern extraction finds
only 2 of the 3 E1 cases (`E1 (1):` blocks in ESM2) — the third
(ESM7 case 7) is stated in prose and was recovered by the keyword
sweep and hand reading, which is why the register is curated data
with the sweep as its method, not raw regex output; (iii) ESM2 is
image-heavy and its white-row text interleaves in extraction order
— row attribution was confirmed against the excerpted tables in the
article for the cases used.

## 6. Verification

- New unit tests: 17 passed (`tests/test_phase120_bhaskar.py`:
  register integrity, classifier contract incl. "silent use is never
  ALL-AGREE", real-44 counts 0/1/43, CSV round-trip, H23 node).
- Full backend suite: **808 passed / 13 skipped / 0 failed**
  (Phase-119 baseline 779/13/0; +17 Phase-120 tests and +12 tests
  already on main since that count). Run in a fresh venv built from
  this branch (`pip install -e backend[dev]`).
- Foundation check: **40 passed / 0 failed / 8 warnings** (baseline
  held). Note: the check needs the gitignored Holdat corpus, which
  lives only in the main checkout; it was run in this worktree with
  `corpora/downloads` symlinked from the main checkout (gitignored
  path, nothing committed).
- Ruff: clean on all Phase-120 files.
- Side-effect note: running the full suite in a fresh worktree
  rewrites several tracked claim/output JSONs (the same files that
  sit dirty in the main checkout); those were restored untouched
  (`git checkout --`) and are not part of this phase's commit.
- Anchors file: SHA-256 identical before/after the triage run;
  287 anchors, tier counts unchanged (166/5/3/113). No anchor was
  modified by this phase.

## 7. NON-CLAIMS

- This phase is a **descriptive triage only**. It changes **no**
  anchor status: all 44 remain `pending_non_sa_validation`, and
  `INDUS_FINAL_ANCHORS.json` is untouched.
- It **validates nothing**. CONTESTED does not mean an anchor's
  reading is wrong, and NOT-COVERED does not mean it is right;
  ALL-AGREE being empty is a property of Bhaskar's publication
  (no per-sign concordance statements exist in it), **not** evidence
  that the compilations disagree about the other 43 signs.
- Mention in an ESM list is behavioural attestation inside an
  anisotropy study. It is not independent corroboration of any
  sign's value, and no part of this report may be cited as such.
- Bhaskar's D-type anisotropies concern sign *order*. Nothing here
  bears on any anchor's phonetic reading.

## 8. Open questions for a future spec (not decided here)

- Bhaskar explicitly calls the M77 and ICIT sign lists subjective
  and argues a new sign list is needed, starting from frontal signs
  (article, closing sections). Whether a genuine per-sign
  M77/ICIT/CISI concordance should be *built* (from the compilations
  themselves, not from Bhaskar) is a question for a future spec; this
  phase only establishes that Bhaskar (2024) does not already
  contain one.
- The M402 coverage gap (BH-D10) and the 267/267a split (BH-D01)
  are the two documented form-class disputes nearest the anchor
  set. Whether either should feed any future adjudication is an
  open question, recorded here without recommendation.

## Artifacts

- `reports/phase120_bhaskar_triage_44.md` (this report)
- `reports/phase120_bhaskar_triage_44.json` (per-sign triage)
- `reports/phase120_bhaskar_disagreements.json` / `.csv` (20-case register)
- `backend/glossa_lab/phase120_bhaskar.py` (register + classifier)
- `backend/glossa_lab/experiment_graph_phase120.py` (H23 node)
- `backend/scripts/phase120_bhaskar_triage.py` (runner)
- `backend/tests/test_phase120_bhaskar.py` (17 tests)
