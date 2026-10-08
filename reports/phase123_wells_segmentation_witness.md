# Phase-123 — Wells Segmentation Witness Memo

**Status:** witness statement. **Date:** 2026-10-08. **Phase:** 123 (Phase D of the
Glossa-Lab new-material program).

**Framing (hard).** This memo and its companion table are a *witness statement*,
not an adjudication. They record how Bryan K. Wells's grapheme segmentation — as
published in his two theses — treats each of the program's 157 Mahadevan-numbered
anchor signs, and what that treatment *would* bear on, stated strictly as a
conditional. They make **no** recommendation to adopt Wells's segmentation, assert
**no** implication for any anchor's status, and claim **no** position on whether
Wells's segmentation is right or wrong. Anything in this memo that resembles a
conclusion is recorded as an open question for a future spec (§9).

**Artifacts.**

- Table (CSV): `data/crosswalks/wells_segmentation_witness_v1.csv`
- Table (JSON): `data/crosswalks/wells_segmentation_witness_v1.json`
- Builder: `backend/scripts/phase123_build_wells_witness.py`
- Tests: `backend/tests/test_phase123_wells_witness.py` (6 tests)

**Headline numbers.**

- Signs in scope: **157** — the 113 CANDIDATE anchors plus the 44
  `pending_non_sa_validation` anchors in `backend/reports/INDUS_FINAL_ANCHORS.json`
  (verified disjoint; counts re-derived from the file, not assumed).
- Wells treatment determinable for **134 / 157 (85.4%)**.
- Treatment breakdown (all 157): **SAME 87 · SPLIT 40 · MERGE 5 · NOT-COVERED 2 ·
  INDETERMINATE 23**.
  - CANDIDATE (113): SAME 62 · SPLIT 27 · MERGE 4 · NOT-COVERED 1 · INDETERMINATE 19.
  - pending (44): SAME 25 · SPLIT 13 · MERGE 1 · NOT-COVERED 1 · INDETERMINATE 4.
- Hand verification: **20 table rows** hand-checked against the thesis plates —
  **17 glyph-consistent** (one, M389, consistent by glyph but carrying a recorded
  cross-source conflict), **2 partial** (M149, M401), **1 discrepancy** (M293).
  See §7; the discrepancy is preserved in the table, not smoothed over.

---

## 1. Sources

| Source | Form used | Method |
|---|---|---|
| Wells MA thesis 1998, *An Introduction to Indus Writing*, Univ. of Calgary (DOI 10.11575/PRISM/23641), ~295 pp. PDF | Repository PDF with a (noisy) embedded text layer | Text-layer extraction (`pymupdf`), plus direct visual reads of figure pages rendered at 170 dpi |
| Wells PhD thesis 2006, *Epigraphic Approaches to Indus Writing*, Harvard, 296 pp. deposited scan | Scanned-image PDF, **no text layer** | Fresh OCR (RapidOCR, `~/workspace/venvs/ocr`, the env used by the earlier Mahadevan/Phase-121 OCR work) over the front matter and Chapter 3 (PDF pp. 4–7, 72–122) at 150 dpi; the sign-list plates (Fig. 3.2) and Appendix I sheets were read **visually** from 200-dpi renders, since OCR does not recover glyphs |
| `backend/reports/INDUS_FINAL_ANCHORS.json` | The program's anchor file on `main` | Sign universe (113 + 44) re-derived programmatically |
| `data/crosswalks/canonical_sign_registry.csv` | Held crosswalk on `main` (mayig CISI digitisation, MIT licence; per-grapheme Wells (2015) cross-match) | Primary systematic Mahadevan ↔ Wells correspondence (§4) |
| Phase-122 crosswalk (PR #81, unmerged) | Consulted read-only only | **Not** depended on by any committed output; two rows (M033, M126) note a chain-only lead that runs through it, and are recorded INDETERMINATE for exactly that reason |
| Sweep report `indus-data-deep-sweep-20261008/report.md` | Program research record, 2026-10-08 | Framing of Wells's sign-count history (§2) |

Governance: the theses are research copies. This phase extracts Wells's inventory
*decisions* (facts) with page citations; it republishes no thesis text passages
and no page images in the repo.

## 2. Wells's sign-count history (framing)

The sweep resolved the apparent 676-vs-694 conflict in secondary citations as
chronological. The theses themselves confirm the thesis-era figures:

- **MA 1998: 587 signs**, with 802 varieties, organised in 63 Sets, over 7,121
  sign-location references (Mohenjo-daro 4,094; Harappa 2,154; Lothal 360; minor
  sites 523) — Wells's own statement, MA thesis p. 48 (thesis pagination).
- **PhD 2006: 676 signs.** Wells recounts the list's own history (PhD thesis
  pp. 67–68): a first version with more than 900 signs (allographic variants
  included), compressed to 610 after context study against CISI, then settled at
  676 for the list printed as Figure 3.2 — with Wells's own caveat that 676 is
  likely an over-estimate, doubtful graphs being kept separate in the absence of
  proof they are variants.
- **2011: 673; 2015: 694** — as recorded in the sweep report's synthesis
  (report.md, "decisive field is LINEAGE" follow-up list, item 7). The 2015 form
  of the list is the one the held registry's Wells cross-match uses.

## 3. The two thesis inventories, and how they differ

**MA 1998.** The sign list is presented as Table 3.1 (signs sorted by Set and by
frequency; thesis pp. 60–66) and Table 3.2 = Appendix 1 (PDF pp. 145–295):
one entry per sign giving the sign graph, its varieties, its Set, and the
attestations (artifact numbers by site) for each variety. Chapter 3
(thesis pp. 42–59) states the method: Parpola's three grapheme criteria,
expanded with artifact-type and provenience context; Figure 3.6 (thesis p. 77)
is a direct Mahadevan (1977) ↔ Fairservis (1992) ↔ Parpola (1994) ↔
Wells (1997) concordance for the grapheme groups Wells redefined.

**PhD 2006.** The list is presented as Figure 3.2, "The Indus signs by sign
number" (thesis pp. 90–92): three plates of glyphs numbered to **958**, the gaps
being numbers retired during the >900 → 676 compression. Appendix I
(thesis pp. ~207–284) gives a per-sign data sheet for each sign (graph, Set,
Type, Class, composition, frequency by site, positional distribution, artifact
types, field symbols). The corpus basis is the ECIT database (5,643 artifacts
with texts and/or iconography; 3,835 with at least one recognizable sign —
abstract, thesis p. ii) analysed with the ICIT program (v1.59).

**Differences that matter for using the theses as witnesses.**

1. **Size:** 587 (MA) → 676 (PhD), on a much larger corpus (the MA list is built
   on the Mahadevan-era published corpus; the PhD list on ECIT/CISI).
2. **Numbering is reorganised, not extended.** The same grapheme carries
   different numbers in the two theses, and the number blocks mean different
   things: in the MA list the stroke signs sit in the 190s–230s (MA thesis
   pp. 47–48) while in the PhD list the stroke signs open the list
   (001–067, Fig. 3.2, thesis p. 90). Any MA↔PhD number comparison must go
   through a concordance or glyphs, never through the bare number.
3. **Worked examples of the reorganisation** (all verifiable in the theses):
   the carrying-pole figure that Mahadevan lists as one sign (#15, nine
   varieties) is divided by Wells in the MA thesis into his signs **5, 8 and
   11** (MA thesis pp. 51–54, Figs. 3.2–3.3); in the PhD list the corresponding
   bearer family occupies the 150–161 block (Fig. 3.2, thesis p. 90). The
   inverted-triangle-on-stem sign is Wells **48** in the MA concordance
   (Fig. 3.6) and **092** in the PhD plates. Mahadevan 178's dotted-A family is
   Wells **436–446** in the MA numbering (Fig. 3.6) and Wells **465–475**
   (with 467) in the PhD/ICIT numbering (registry).
4. **Presentation:** MA argues segmentation case-by-case in prose with
   attestation lists; the PhD argues through numbered Examples 1–5
   (thesis pp. 68–76: signs 175/176/177 kept separate; signs 920 vs 921 kept
   separate, Table 3.1; signs 525/526/527 — 526 the mirror of 527 — kept
   separate under an explicitly stated "policy of caution", Tables 3.2–3.3;
   signs 705/706 kept separate) and then presents the whole list as plates +
   data sheets.

## 4. Correspondence method (how each table row was produced)

Wells uses his own numbering in both theses; neither thesis prints a complete
Mahadevan ↔ Wells concordance. The table therefore combines four routes, in
descending order of strength; every row names its route in the
`correspondence_method` column.

1. **REGISTRY (127 of 157 rows).** The held `canonical_sign_registry.csv`
   (mayig CISI digitisation; per-grapheme Wells (2015) cross-match) aggregated
   in both directions. Wells graphemes for a Mahadevan sign = its registry set.
   Treatment follows from the cardinalities: ≥2 Wells graphemes → SPLIT;
   exactly 1, shared with other Mahadevan signs → MERGE; exactly 1, unshared →
   SAME. The registry's Wells numbering is the Wells/ICIT list in its 2015
   form; its thesis-era ancestor is the PhD Figure 3.2 list, and the table's
   `thesis_source` column cites the Fig. 3.2 plate page for each row's Wells
   number(s) (≤308 → thesis p. 90; 309–681 → p. 91; ≥683 → p. 92).
2. **MA-FIG36 (3 rows carry it as a second citation: M178, M213, M400).**
   Wells's own Fig. 3.6 concordance (MA thesis p. 77), read visually. For these
   rows the MA-era treatment is recorded in the row note alongside the
   registry route (M178: SPLIT in both numberings; M213: SAME in both;
   M400: SAME in both).
3. **GLYPH (7 rows: M153, M213, M274, M369, M378, M389, M396).** For signs the
   registry does not reach, the Mahadevan glyph (repo sign images) was matched
   by hand against the PhD Fig. 3.2 plates / Appendix I sheets. Each such row
   cites the plate or sheet and describes the glyph. One (M389) collides with a
   registry assignment (W805 is also assigned to M387): the collision is
   recorded in the row as a cross-source disagreement, and the row is classed
   MERGE on the combined evidence — the disagreement itself is *not* resolved
   here.
4. **GLYPH-SEARCH-NEGATIVE (2 rows: M312, M365).** Distinctive glyphs (a plain
   wide arch; a plain open V) searched across all three Fig. 3.2 plates and
   Fig. 3.6 and not found; rows classed NOT-COVERED with the search described.
   This is a statement about the searched plates, at the stated scope.

**Assumptions, stated.**

- A1. *Numbering continuity, PhD → ICIT → 2015.* The registry's Wells numbers
  are treated as the same list as the PhD Fig. 3.2 numbers. Support: the ICIT
  conversion layer's positional codes agree with the PhD's own frequency table
  (PhD Table 3.6's most frequent sign, 740, is the conversion layer's most
  frequent code, 1,928 tokens, aligned to M342, the jar sign whose glyph is
  plate sign 740); and the §7 glyph checks, which would have exposed a
  systematic shift, instead found glyph agreement at the stated numbers in
  17 of 20 rows. Continuity is *not* assumed for the MA numbering (see §3.2).
- A2. *The registry's Wells cross-match is a faithful record of the Wells
  list's groupings* (it derives from the mayig digitisation's per-grapheme
  Wells (2015) matching). Phase-123 did not re-derive it from the 2015 book,
  which the program does not hold in machine-readable form.
- A3. *Not used:* the `wells_id` column of
  `backend/glossa_lab/data/mahadevan_parpola_crosswalk.json`. Its values do
  not survive glyph comparison with the PhD plates (e.g. it gives M001 → W001,
  but plate sign 001 is a single stroke sign and M001 is the raised-arm man;
  it gives M047 → W008, also a stroke sign). Recorded here so a future phase
  does not silently build on it.
- A4. *Attempted and rejected:* attestation co-occurrence (MA Appendix 1
  per-sign artifact lists vs ICIT per-artifact Mahadevan sign sets, Jaccard
  similarity). The MA text layer's attestation digits are too corrupt and the
  surviving signal too weak (best Jaccard 0.22 across only 6 candidate signs)
  to support per-sign claims. The method, and its negative result, are
  recorded so the attempt is not repeated on the same inputs.

## 5. Results

The full table is the artifact; this section only summarises its contents.

- **SAME (87).** For these signs Wells's list carries exactly one grapheme,
  unshared. The conditional implication recorded per row is narrow: token
  identity would carry over by name if Wells's segmentation were adopted,
  though the corpora differ.
- **SPLIT (40).** Wells divides one Mahadevan sign among two or more
  graphemes. The largest cases in the table: M178 → 10 graphemes
  (465, 467–475; MA-era: 436–446), M168 → 7, M169 → 6, M120 → 5 (025–029),
  M011 → 3 (159–161, shared in part with M014). A visible pattern in the
  stroke-sign block: Mahadevan stroke signs M102–M120 correspond to *pairs*
  of Wells stroke graphemes (e.g. M112 → 007 + 017; M103 → 003 + 013, shared
  with M102's MERGE — see below), i.e. Wells separates stroke arrangements
  that Mahadevan pools. This is a description of the table's contents, not a
  judgement about either list.
- **MERGE (5).** M102 → 003 (shared with M103's split set), M115 and M116 →
  019 (the pair pooled into one Wells grapheme), M245 → 615 (shared),
  M389 → 805 (glyph route; conflict recorded, §4.3).
- **NOT-COVERED (2).** M312, M365 — §4.4.
- **INDETERMINATE (23).** Listed in the table with the reason per row. Two
  (M033, M126) carry the chain-only lead described in §1/§4; the remaining 21
  are signs whose glyphs could not be located with confidence in the plates
  and which no held committed crosswalk reaches.

## 6. Worked witness instances (from the theses' own discussions)

These are the segmentation decisions Wells argues explicitly in prose; they
illustrate what the table's SPLIT/SAME labels mean in his method. They are
quoted as facts about the theses (with pages), not endorsed.

- **Mahadevan 15 (not itself an anchor target).** MA thesis pp. 51–54:
  Mahadevan's nine varieties are divided on visual grouping into Wells 5
  (arms + carrying pole), 8 (pole, no arms) and 11 (neither), and the three
  are shown to have different context and artifact-type distributions
  (Figs. 3.2–3.3). In the PhD list the family is renumbered into the
  150–161 block; the registry records five Wells graphemes (153–156, 158)
  against M015 in the 2015 form.
- **Signs 175/176/177 (PhD Example 1, thesis pp. 68–69).** Three graphically
  close signs are kept as three graphemes on mutually-exclusive-context
  evidence; left-to-right (mirror) occurrences are subsumed under 176. In the
  registry these correspond to the M047/M048 area — the PhD's worked example
  of refusing a merge.
- **Signs 525/526/527 (PhD Example 4, thesis pp. 72–75).** 526 is the mirror
  image of 527; the evidence is stated by Wells to be inconclusive, and the
  pair is kept separate under a stated policy of caution. The table's
  M254 row (→ 526 + 527, SPLIT) sits exactly on this pair.
- **Signs 920/921 (PhD Table 3.1, thesis pp. 70–71).** Kept separate on
  mutually exclusive contexts. This pair is where the table's one
  verification discrepancy sits (§7).
- **Internal hatching (MA thesis pp. 57–58).** Sign pairs differing only by
  internal hatching (MA signs 497/498; 469/470; 475/477) are kept as separate
  graphemes on mutually exclusive contexts — the MA-era instance of the same
  refusal-to-merge policy.

## 7. Verification (hand-checks against the thesis pages)

Twenty rows were hand-verified by comparing the Mahadevan sign image
(`backend/static/signs/`) with the glyph printed at the row's Wells number
in the PhD Fig. 3.2 plates (thesis pp. 90–92) or, for M262/M274, the
Appendix I per-sign sheets (thesis p. 278). Outcomes, also recorded per row
in the table's `verification` column:

- **Glyph-consistent (17):** M127 (→440), M213 (→092), M254 (→526/527),
  M262 (→860), M274 (→866), M287 (→900), M304 (→890), M332 (→732/734),
  M345 (→745–747), M369 (→782), M378 (→837), M383 (→815/816), M396 (→372),
  M405 (→841), M416 (→217), M153 (→520), and M389 (→805, glyph-consistent but
  see the conflict below).
- **Verified with a recorded conflict (counted in the 17):** M389 — the glyph
  at plate sign 805 matches M389, yet the held registry assigns 805 to M387
  (which it also splits to 803/806). Both records stand in the table; the
  conflict is flagged, not resolved.
- **Partial (2):** M149 (→690: correct X-family; the Mahadevan glyph's
  chevron end-treatment is simplified in the Wells font) and M401 (→375:
  correct paired-loop family; the barred knot form is not reproduced exactly).
- **Discrepancy (1):** M293 — the registry assigns W920, whose plate glyph is
  a plain thin arc; the Mahadevan glyph carries a closed loop on the arc.
  Wells's own discussion (thesis pp. 70–71) keeps 920 and 921 apart on
  contextual grounds, and the plate rendering does not settle which of the
  pair carries the looped form. The row is kept as the registry states it
  (SAME → 920) with `verification = discrepancy` and the full note.

Verification accuracy, stated plainly: of 20 hand-checked rows, 17 (85%) were
glyph-consistent with the printed thesis plates, 2 (10%) were
family-consistent but not glyph-exact, and 1 (5%) is a recorded discrepancy
between the held registry and the plate glyph. No row's treatment was
changed on the basis of a partial or discrepancy outcome; those outcomes are
carried in the table as flags for a future spec.

## 8. Reproducibility

```
python3 backend/scripts/phase123_build_wells_witness.py   # deterministic; two runs byte-identical (md5-verified)
~/workspace/venvs/glossa-lab/bin/python -m pytest backend/tests/test_phase123_wells_witness.py
```

The builder reads only committed inputs (`INDUS_FINAL_ANCHORS.json`,
`canonical_sign_registry.csv`) plus its embedded hand-verification and
glyph-match records, each of which cites the thesis page it was read from.

## 9. Open questions (for a future spec — no conclusions drawn here)

1. **M293:** which of Wells 920/921 carries the looped arc form? Resolving it
   needs the Appendix I data sheets for 920/921 (frequency/context) read
   against the Mahadevan attestations of M293 — or the Wells (2015) sign-list
   concordance page.
2. **M389 / M387 / W805:** the registry and the plate glyph disagree about
   what 805 covers. A future spec could adjudicate from the Appendix I
   sheets for 803–807.
3. **M033, M126:** the chain-only correspondences (codes 143; 016/006) that
   run through the unmerged Phase-122 crosswalk — to be re-derived or
   confirmed once that chain is on `main`, or from the 2015 concordance.
4. **The 21 remaining INDETERMINATE signs:** most are rare or compound forms.
   Candidate routes: the Wells (2015) printed concordance (program holds
   only the registry extract), Fuls's sign catalog, or a cleaner scan of the
   MA appendix for an attestation-based attempt (§4, A4) with better digits.
5. **MA attestation lists:** Appendix 1's per-variety attestations are a
   potentially independent correspondence source that the current scan's
   text layer cannot support; a re-scan/re-OCR of the appendix at plate
   quality is a precondition for any future use.
6. Whether Wells's **673 (2011)** list renumbered anything relative to the
   PhD (676) list is not recorded in the theses and was not investigated;
   the table's Wells numbers are the PhD/2015-lineage numbers throughout.

## 10. What this memo does not do

It does not rank Wells's segmentation against Mahadevan's or Parpola's; it
does not propose adopting, rejecting, or hybridising any of them; it does not
touch any anchor's tier, value, or validation status; and it draws no
PRED-2026 qualification from the Wells material. It is a witness statement:
what Wells's two theses record, where they record it, how the record was
carried into the program's numbering, and where the record runs out.

---

**AI disclosure:** research and drafting by an AI agent (Muse Spark, via
Muse) at the direction of Tristen Pierson, per constitution §VI. All
thesis facts above were extracted from the deposited thesis PDFs held by the
program; glyph verifications were performed by the agent from rendered
thesis pages and are recorded per row so they can be re-checked by hand.
