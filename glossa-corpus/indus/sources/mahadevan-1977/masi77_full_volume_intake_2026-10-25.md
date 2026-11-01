# Mahadevan (1977) — Full Volume (MASI No. 77): Intake Record

**Source work:** I. Mahadevan, *The Indus Script: Texts, Concordance and
Tables* (Memoirs of the Archaeological Survey of India No. 77,
Archaeological Survey of India, New Delhi, 1977). Printed extent 825 pp.

**This holding:** the complete volume as a single scanned PDF, held by
T. Pierson on TRISTEN-DESKTOP at
`C:\Users\trist\Downloads\MASI 77 Indus Script Texts Concordances & Tables Iravatham Mahadevan.pdf`
(WSL path `/mnt/c/Users/trist/Downloads/…`). Surfaced by the owner
2026-10-25. The PDF is **not** committed to this repository.

- Bytes: 16,445,165
- SHA-256: `ef68fe8dc25e94fe9cb75b418c5189a084383e72498560ef393372e90a27e110`
- PDF pages: 843 (1 Digital Library of India cover sheet + 842 leaves)
- PDF metadata: Title "memoirs of the archeological survey of india
  no.77"; Author "mahadevan, iravatham"; Producer iText 5.4.1;
  file dates 2013-06-25.
- Scan identity: Digital Library of India scan, barcode
  99999990041354; the scanned copy is the Central Archaeological
  Library (New Delhi) accession copy (library stamp, PDF p. 2;
  loan pastedown on the final leaf).

**Verification performed (2026-10-25, on the desktop, via relay;
pypdf 6.21.2 + Ghostscript renders + Tesseract 5.3.4 OCR samples):**

- *Identity — confirmed from the volume's own title page* (PDF p. 7):
  "MEMOIRS OF THE ARCHAEOLOGICAL SURVEY OF INDIA No. 77 / THE INDUS
  SCRIPT / Texts, Concordance and Tables / IRAVATHAM MAHADEVAN …
  Published by The Director General, Archaeological Survey of India,
  NEW DELHI, 1977." Copyright page (PDF p. 8): © ASI 1977, Tata Press
  Bombay, price Rs. 250 — the original 1977 edition; no reprint
  statement seen.
- *Pagination:* printed page = PDF page − 12, verified at printed
  folios 4, 6, 10 (Introduction), 32 and 39 (Sign List), 417 and 548
  (Concordance), 717 and 728 (Tables), with Appendix V content at
  printed p. 825.
- *Structure* (contents page, PDF p. 9, corroborated at the sampled
  pages): Map printed p. 29; Codes p. 30; Sign List from p. 32;
  Texts in the Indus Script pp. 163–416; Concordance to the Texts
  pp. 417–716; Tables I–IX from p. 717; Appendices I–V from p. 785.
- *Completeness:* every one of the 842 book leaves carries a page
  image (the only image-less page is the DLI cover sheet); sampled
  folios run continuously with no duplicated or out-of-order leaves
  found; the bibliographic final page (printed 825) is present inside
  the scan, followed by plate/library leaves. This is page-count
  arithmetic + image presence + sampled folios — **not** a
  leaf-by-leaf collation against the printed edition.
- *Text layer:* none. 842 of 843 pages carry zero extractable text
  (only the DLI cover sheet has any). Effective scan resolution
  ~150 dpi (min 140 / median 150 / max 176 across all pages).

**Known limitations:** at ~150 dpi, OCR (Tesseract samples, 2026-10-25)
reads Latin body text and the numeric scaffolding — sign numbers,
variant "+" markers, text numbers, tabular numerals — at
reference grade (best on clean lists: Appendix V page, mean word
confidence 72; dense glyph pages 39–55). The Indus sign glyphs
themselves are **not** OCR-recoverable (they emerge as noise); any
use that turns on a sign's drawn form must read the page image
visually. The Sign List's per-sign entries pair drawn forms with
occurrence text-number lists; the numbers are machine-legible with
human verification, the forms are not machine-legible at all.

**Why it is here — designated use:** (1) the Mahadevan arm of the
Spec 071 reopening-trigger census: this volume is one of the two
named candidate sources whose exhibition can reopen the retired
sky-signs question (see
`docs/decisions/2026-10-25-spec-071-retirement-decision.md`); this
intake record is the exhibition/pin record for that arm. (2) M77
sign-list reference for the programme's M-numbering. It complements,
and does not supersede, the 25-page Introduction transcription
recorded in `CITATIONS.md` §A.1 (a separate 400-dpi artifact).

**Census readiness (what remains before a count can run):**

1. ✅ Pinned artifact in hand and identity/hash verified (this record).
2. ☐ Sign-list extraction: transcribe printed pp. 32–162 (PDF
   pp. 44–174) — sign numbers and variant markers by OCR + human
   double-keying; candidate signs' drawn forms transcribed visually.
3. ☐ Identification determination under the census instrument's
   rules (Spec 071 §4.1 discipline): M77's list attaches no per-sign
   depictive labels, so any celestial identification must be sourced
   to Mahadevan's own statements and mapped to sign numbers first.
4. ☐ Occurrence counting in the primary population per the census
   instrument (M77's Concordance, pp. 417–716, and Table I,
   pp. 717 ff., serve as cross-checks).
5. ☐ Threshold application against the recorded trigger
   (≥5 celestially identified signs / ≥30 primary-population
   occurrences), reported as the pair: what the count establishes /
   what it does not.


---

## Correction and qualification — 2026-10-25 (programme red team, finding F-6)

Two statements in this record are qualified, dated today:

1. **Completeness.** The holding statement above ("the complete
   volume as a single scanned PDF") rests on the basis stated in
   this record's own completeness section: page-count arithmetic,
   image presence, and nine sampled folios — **not a leaf-by-leaf
   collation against the printed edition**. Cite the holding as
   "complete by page-count and sampling; not collated
   leaf-by-leaf." The provenance.yaml `confidence: "0.99"` figure
   carries no stated basis and should not be cited.
2. **Readiness item 3 vs the trigger-census instrument.** Item 3
   states that M77's sign list attaches no per-sign depictive
   labels. That is asserted before readiness item 2 (extraction
   of the sign list, printed pp. 32–162) has been done, and the
   trigger-census instrument describes its Mahadevan target as
   "the sign list (the M77 signary and its identifications)" —
   the two records cannot both describe the census's source.
   Until the item-2 extraction reads pp. 32–162, where Mahadevan
   identifications, if any, live is an open question, and no
   census arm should be designed against either description
   alone.


---

## Correction — 2026-10-25 (sign-list extraction)

Three statements above are corrected by the extraction recorded in
`m77_sign_list_extraction_2026-10-25.md` (same folder):

1. **Page map.** The structure line above ("Sign List from p. 32;
   Texts in the Indus Script pp. 163–416; Concordance to the Texts
   pp. 417–716") swapped the Texts and the Concordance. The volume's
   own contents leaf (PDF p. 9) reads: SIGN LIST 32 · TEXTS IN THE
   INDUS SCRIPT 39 · CONCORDANCE TO THE TEXTS 163. Correct map:
   Sign List printed pp. 32–35 (PDF pp. 44–47); Texts printed
   pp. 39–162; Concordance printed pp. 163–716; Tables from p. 717
   (unchanged).
2. **What the sign list contains.** The sentence "The Sign List's
   per-sign entries pair drawn forms with occurrence text-number
   lists" describes the Concordance, not the Sign List. The
   sign-list grid prints, per sign, its number, one drawn normal
   form, and the variant dagger where it applies — no occurrence
   lists, no frequencies.
3. **Readiness items 2 and 3 (and F-6) are resolved.** Item 2 is
   complete: the sign list is transcribed (417 signs; dataset and
   hashes in the extraction record). One method deviation is
   recorded there and must be read with the dataset: transcription
   was by machine consensus, not the human double-keying item 2
   specified, because a machine write restriction made landing page
   images for human keying impossible this session; 30 signs are
   named UNCERTAIN in the dataset, none guessed. Item 3 / F-6:
   M77 attaches no per-sign identifications; the Introduction's
   §11.5 classes are reported classification under the author's own
   disclaimer ("the classification is merely conventional and no
   stress is laid on any identification"), and no celestial class
   exists in M77 — so M77 cannot by itself exhibit the ≥5
   celestially identified signs the Spec 071 trigger requires.
