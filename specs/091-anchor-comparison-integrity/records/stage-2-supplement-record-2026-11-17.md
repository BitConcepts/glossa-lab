# Spec 091 Stage 2 — Supplementary locator pass over the recovered texts

*Record of the supplementary pass commissioned by the owner on
2026-11-17 ("Commission the supplementary locator pass over the
recovered texts"), after the 2026-11-17 recovery hunt changed the
holdings the T202 locator pass had searched. This record supplements
`stage-2-record-2026-11-17.md` and `stage-2-t202-run-record-2026-11-17.md`;
it does not modify them, the T202 artifact, or any T202 record.*

- **Run**: `study-20261117T134331Z-7ca68f` (surface `study`), executed
  on the mini-server under run-defs v2. tasks.md names "run-defs v1"
  for the Stage 2 run; the landed T202 run was executed and recorded
  under run-defs v2, and this supplement notes the naming discrepancy
  the same way Stage 2 did (the run record carries the note in its
  input pins).
- **Artifact**: `backend/glossa_lab/data/mahadevan_parpola_crosswalk_v2_locators_supplement.json`,
  SHA-256 `610eeff1f9d8c64449cf040c6012e22b17c3506152076a4270bd836ff009c50c`.
- **Generator**: `backend/scripts/spec091_stage2_locator_supplement.py`
  (new; the T202 generator is unmodified — its behavior, the landed
  T202 artifact's reproducibility, and its tests are untouched).
- **Delta record**: `stage-2-supplement-delta.json`.
- **Sample verification**: `stage-2-supplement-sample-verification.json`.
- **Foundation check**: `stage-2-supplement-foundation-check-2026-11-17.json`.

**Consumer merge rule.** Read the T202 artifact and this supplement
together; per entry per field, the supplement's outcome wins. The
T202 artifact and records are not modified.

## 1. Holdings as recovered

| Source | State at T202 | State for this pass |
|---|---|---|
| Parpola 1994, *Deciphering the Indus Script* (CUP 1994, ISBN 0-521-43079-8) | not held | Held: OCR-scan PDF, 392 pp., SHA-256 `fd133822f9999c86178a32208465e847c5288b578ad14ca2cd643efe57f0e0b6`. Re-acquired 2026-11-17 under the owner's internet fallback (the repo-history hypothesis was disproven for this text: it was never a held file); identity verified from the file itself (title page, © 1994, ISBN, LoC 92-37773). Restricted custody outside the tracked tree; never committed. |
| Parpola 2010, *A Dravidian solution to the Indus script problem* | metadata record only | Held: born-digital PDF, 39 pp., SHA-256 `c58137e54cdde3f2acdcfaf05293dfc5f5ba33def3e0b12585c451f76bd4ba84`. Recovered from git history (the `develop` branch tip, `glossa-indus/raw/papers/parpola_2010_dravidian_solution.pdf`); byte-identical to the literature record's intake checksum and to a fresh publisher-side fetch. Restricted custody outside the tracked tree; never committed. |
| Mahadevan 1977 sign list | an unpinned backup copy (T202's run record pins CSV `ec26651f…`, JSON `774e8864…`) | The PINNED dataset, recovered byte-identical to the extraction pins: CSV SHA-256 `ce5dd5a59418132f54761324ca449aa0a7d37e0dad41013aca811049b36af3a4`, JSON SHA-256 `63059d6403898653600c3be3e2268c512550cc8f8906114ac712743f161e0ae3`, standing at the canonical source-store paths (gitignored). The generator refuses to run if the CSV at that path is not the pinned copy. |
| Wells 1998 sign list | held | Held, unchanged (JSON SHA-256 `bdcb8ef32f5172e4d1ddbb057e4344bccbc7aeacc1928d86c2175c12290a4bf0`). |
| Parpola phoneme compilation | held (pointer only) | Held, unchanged (SHA-256 `2aee1d0caf2130847075c9167fa4e707a911c79437a177f0744cec99810eefcc`). Still a pointer only; it can never ground a locator. |

The generator verifies both custody PDFs' SHA-256 against the
recovery pins before any use and refuses on mismatch.

## 2. Method

The pass re-ran the locator search for all 184 crosswalk entries ×
both reading fields (`phonetic_reading`, `semantic_reading`) under
the registered search order of the Stage 2 record — (1) the entry's
stated source, (2) Parpola 1994, (3) Parpola 2010, (4) Mahadevan 1977
sign list, (5) Wells 1998 sign list, (6) the phoneme compilation —
and under the same three-part locator test (eligibility-defs v1 §2):
a locator requires work + page/table/figure pinpoint + sign scheme,
all non-empty for that field, with the cited passage carrying the
field's value. Within the pass, the first grounding source in the
registered order supplies the locator (T202's outcome construction,
mirrored unchanged apart from the not-found basis text, which is
corrected for the recovered holdings).

**Text extraction.** Parpola 1994: the custody scan's text layer
(ABBYY FineReader 12 OCR, embedded in the PDF) extracted page by page
with PyMuPDF — 392 pages, 1,560,335 characters, 8 near-empty pages
(plates/blanks). Printed pagination = PDF page − 18 throughout the
body (verified against 7 folios and rendered pages). Parpola 2010:
the born-digital text layer extracted the same way — 39 pages,
69,004 characters; printed page = PDF page.

**Per-entry search.** For each entry and field, the staged value was
sought as a whole word under the normalization below across the full
extracted text of both works (candidate pages are recorded in the
artifact's search steps), and the sign-reading chapters and each
work's own summary of its interpretations (for 1994, Part IV,
printed pp. 177–272, and the Epilogue's fig. 15.2 table, printed
pp. 275–276) were read for a sign-level attribution to the entry.

**Value-match normalization** (a same-reading identification rule,
fixed before outcomes): lowercase; strip diacritics (NFD); collapse
doubled letters (the ASCII long-vowel doubling of the staged values
and of the 2010 text layer); resolve the 2010 text layer's
legacy-font capitals inside transliterated words (T/L/Z/N for the
retroflex letters — skeleton-neutral except Z, which the map
resolves to ḻ); staged values split on '/' into alternatives, any of
which may match; parenthetical material yields both the expanded
and the dropped form (e.g. staged `muu(n)-` meets cited `mu(m)` at
the common form `mu`).

**Locator adjudication rule** (fixed before outcomes). A locator is
filed only when (a) the passage attributes a specific phonetic value
to a specific sign; (b) the sign identification is overdetermined —
the work's pictorial designation is unique, and the program's own
records (the phoneme compilation's iconic record keyed by the
entry's Parpola number, or the crosswalk provenance's recorded
depiction) tie that designation to exactly this entry; and (c) the
attributed value matches the entry's staged value under the
normalization. Group attributions (a value for a sign family) do not
locate individual modified or other members. A passage attributing a
different value than the staged one is a near-miss, recorded as a
step fact, never a locator. Parpola 1994's fig. 5.1 sign list prints
no readings and its numbering was not equated with the crosswalk's
Parpola numbering, so fig. 5.1 is never used for identification.
Every locator in the artifact comes from the generator's
adjudication table (each row carrying its evidence quote and
verification method) and passed a mechanical cross-check at build
time: the cited value's normalized form and the sign's designation
keyword both occur on the cited pages of the extracted text. The
build refuses if a cross-check fails — no locator is manufactured
from a search hit alone. Every 1994 locator's candidate pages were
additionally verified against the rendered page image (200 dpi),
not the OCR text alone.

**The 1994 OCR caveat, measured.** A not-found in OCR text is weaker
than in born-digital text, and the artifact's 1994 search steps say
so per field outcome. The caveat is quantified on an image-verified
sample: the first paragraph of printed p. 3 (PDF p. 21), transcribed
from the rendered page image (107 words), against its OCR segment —
verbatim word error rate **13.1%** (14 substituted tokens, 0
deletions, 0 insertions), the errors concentrated in letter-spacing
of italic words ("T h e", "N o"), token splits ("19 21",
"2550 1900"), and diacritic loss (Ṛgveda-Saṁhitā → "J}gveda-Samhita"
— the single content-word skeleton loss in the sample). On the two
most load-bearing pages (the Epilogue table, printed pp. 275–276),
all 15 value words (mīn, mu(m), aṟu, eḻu, mey/may, pacu, poṭṭu, kaṇ,
muruku, piḷḷay, vēḷ(i), vaṭa, nāḷ, kōḷi, kōḷ) appear in the OCR with
their consonant skeletons intact; on the §14.1 page the OCR renders
vaṭa as "vafa" (ṭ misread), which is why every locator was verified
against the page image. Conclusion: the 1994 text **is** searchable
for this pass's purposes — consonant skeletons, the basis of the
value comparison, are reliable; diacritic detail is not. Outcomes
are therefore filed **not-found** (with the caveat), not
not-searchable. No source in this pass is filed not-searchable.

**The semantic field.** The crosswalk records no semantic value
separately for any entry (WP4 D5), so no passage can carry "the
entry's semantic reading". Both Parpola texts were nevertheless read
for meaning attributions; the meanings they discuss attach to the
phonetic proposals (e.g. for the plain 'fish' sign, 'fish' and
'star' as the homophones of mīn), not to a separately recorded
semantic field. All 184 semantic outcomes are not-found on that
documented basis, exactly as in T202.

## 3. Census

| Field | Located | Not-found |
|---|---|---|
| phonetic_reading | **9** | 175 |
| semantic_reading | 0 | 184 |

The 9 phonetic locators (all verified against the rendered page
image for the 1994 rows; the 2010 row read in the born-digital text
layer):

| Sign | Cited value | Grounding source and pinpoint |
|---|---|---|
| M047 | mīn | Parpola 1994, §10.4, pp. 194–195; Epilogue fig. 15.2 no. 1, p. 275 — the plain 'fish' sign in the 'number' + 'fish' sequences and doubled |
| M087 | veḷ | Parpola 1994, §13.2, pp. 230–231; fig. 15.2 nos. 14–15, p. 276 — the 'two long vertical strokes' sign |
| M088 | mu(m) | Parpola 1994, §10.4, p. 194; fig. 15.2 no. 3, p. 275 — the numeral sign '3' in the '3' + 'fish' sequence |
| M091 | aru | Parpola 1994, §10.4, p. 194; fig. 15.2 no. 4, p. 275 — the numeral sign '6' (aṟu-mīṉ, the Pleiades) |
| M092 | elu | Parpola 1994, §10.4, p. 195; fig. 15.2 no. 5, p. 275 — the numeral sign '7' (eḻu-mīn, Ursa Major) |
| M175 | katir | Parpola 2010, p. 24 — the spinner's-spindle sign (first sign of seal M-241); expressly "not included in my 1994 book", so the 1994 step is a documented not-found and the 2010 step grounds |
| M261 | muruku | Parpola 1994, §13.1, p. 229; fig. 15.2 no. 11, p. 276 — the 'two intersecting circles' sign |
| M281 | piḷḷai | Parpola 1994, §13.1, pp. 229–230; fig. 15.2 no. 13, p. 276 — the five-striped palm squirrel sign |
| M311 | vaṭa | Parpola 1994, §14.1, p. 240; fig. 15.2 no. 16, p. 276 — the three-branched 'fig tree' sign |

## 4. Delta against T202

Per entry per field (full table in `stage-2-supplement-delta.json`):
phonetic — **9 changed** (not-found → located: the 9 rows above),
175 unchanged; semantic — 0 changed, 184 unchanged. The T202 census
is superseded per field only where the delta records a change, under
the merge rule stated at the head of this record.

## 5. Named near-misses and discrepancies

- **The 'crab' sign and kōḷ (M032, M099, M124).** Parpola 1994 §13.3
  (p. 233) and fig. 15.2 no. 20 read the 'crab' sign kōḷ 'grasper,
  planet' — the value two entries stage (M032 `koL`, M099 `kol/koḷ`).
  No locator is filed for either: the program's records do not tie
  the 'crab' depiction to any single entry — the phoneme
  compilation's record for Parpola no. 99 is the 'bow' sign (read
  vil), the compilation's iconic record for no. 124 is a vessel (the
  kuTam entry), and the 2010 fig. 11 caption numbers the 'crab' sign
  124 in the work's own sign numbering, which the crosswalk does not
  use (see below). The identification is contradicted, not
  overdetermined. For M124 the attribution is additionally a value
  mismatch (staged kuTam ≠ kōḷ).
- **vaṭa and the fig tree (M123, M311).** Both Parpola works
  attribute vaṭa to the three-branched 'fig tree' sign (1994 §14.1;
  fig. 15.2 no. 16; 2010's 'Banyan fig and the pole star' section).
  The crosswalk provenance records that depiction for **M311**, whose
  staged value is vaṭa — M311 is located (§3). The 2010 fig. 11
  caption calls the fig-tree sign "no. 123" in the work's own
  numbering; crosswalk entry M123 stages no value and records no
  depiction, so no locator can be filed for it, and values are never
  moved between entries. The caption's numbering is Parpola's
  book-internal sign-list numbering, which the program's records do
  not equate with the crosswalk's Parpola numbering (at no. 47 the
  book's fig. 5.1 list does not show the plain 'fish' sign the
  crosswalk's no. 47 carries); this pass identifies signs
  pictorially, never by that numbering.
- **The compilation's P124 source label is not borne out.** The
  phoneme compilation labels its kuTam proposal "Parpola 2010 sec.
  'iconic shape…' + M-478 tablet". No passage in the recovered 2010
  text attributes kuTam to any sign. The label stands in the
  compilation as filed; the discrepancy is recorded here and in
  M124's 2010 search step.
- **kaṇ and the 'eye' sign (M128, M153, M391).** Fig. 15.2 no. 9
  reads the 'dot-in-circle = eye' sign kaṇ (§12.1 develops it). Three
  entries stage kaṇ-type values and no program record ties the
  depiction to exactly one; no locator is filed for any of the three.
- **nāḷ and the '4' sign (M071, M077).** Fig. 15.2 no. 18 and §14.1
  read the '4' sign nāḷ in the '4' + 'fig' compound. Two entries
  stage nal and no program record ties the four-stroke sign to
  exactly one; no locator is filed.
- **The fish family (M050, M053, M055, M056, M060, M145, M155,
  M222).** Both works attribute mīn to the plain 'fish' sign and
  specific values to specific modified signs (§10.5's 'halved fish'
  pacu and 'roof' + fish mey/may name signs no crosswalk entry
  stages). The family attribution does not single out these entries'
  signs; all remain not-found.
- **M088 in Parpola 2010.** The 2010 text gives the 'three long
  vertical strokes' sign an iconic interpretation only ('the three
  worlds', p. 30) and no phonetic value; its locator is the 1994
  attribution (§10.4; fig. 15.2 no. 3).
- **M001.** The compilation's proposal for the 'man' sign is āḷ, not
  the staged tōḷ; no passage found attributes tōḷ to the sign.

## 6. Sample verification

Rule (fixed before sampling, mirroring T202's registered rule as
the commission specified): **every** entry carrying a locator (a
census of locators, not a sample), plus every 12th entry in sign
order starting with the 1st (16), plus every entry whose
phoneme-compilation consultation hit (17). Drawn: **36 entries**;
every sampled outcome was re-derived from fresh reads of the held
copies (including the adjudication cross-checks) and matched the
filed outcome: **all_verified: true**, all 9 locators verified
(`stage-2-supplement-sample-verification.json`).

## 7. Boundary

This pass establishes locatability only. It files **no** eligibility
determination, **no** WP5 disposition, and **no** claim-standing
change. Eligibility re-derivation from the supplemented locator
record belongs to a later stage. The standing position is unchanged:
the Indus script is not deciphered; a located reading is a reading
whose primary-source passage can now be pointed to, not a reading
established as correct.

## 8. Gates

- Foundation check over the touched data: **17/17 PASS**
  (`stage-2-supplement-foundation-check-2026-11-17.json`).
- Ledger gates, standing profile held exactly: `--all` **29 PASS /
  0 FAIL / 1 NOT-RUN**; `--regen` **32 PASS / 0 FAIL / 0 NOT-RUN**;
  `--contamination` **PASS, 0 flags** (1,025 presentations scanned).
- Targeted tests: `test_spec091_stage2_locator_supplement.py` +
  `test_spec091_stage2_locator_pass.py` — 18 passed.
- Full backend suite (CI invocation, GPU files ignored,
  `test_phase392_q2_gate.py::test_pipeline_deterministic_under_seed`
  deselected by plain nodeid, two-part split at
  `test_spec086_ledger_gate.py`): part 1 — 2,244 passed, 94 skipped,
  1 deselected (exit 0); part 2 — 722 passed, 23 skipped (exit 0);
  **union 2,966 passed, 117 skipped, 1 deselected, 0 failed**. Suite
  side-effect files (extracted-claims JSONs, the claim report,
  `outputs/partial_loop_result.json`) were restored before committing.
