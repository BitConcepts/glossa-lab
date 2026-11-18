# FORMAT.md — Indus paper v11 reformatted to the RCPH paper's LaTeX format

Date: 2026-11-18. Status: DRAFT. Nothing published.

## 1. Where the RCPH format source was found

The RCPH paper is "Exact finite-size corrections for spacelike-volume estimators in causal
diamonds: preregistered tests in 1+1 and 2+1 dimensions", Zenodo DOI
10.5281/zenodo.23604642. The Zenodo record carries only the PDF (single version, created
2026-10-23; no .tex in the record or its version chain).

The LaTeX source was found on tower-compute at:

    /home/tpierson/rcph/projected-constraints-program/papers/separator-counting-law/main.tex

(71,049 bytes; copied into this working directory as `rcph-format/rcph-main.tex`.)
Identity check: the RCPH PDF downloaded from Zenodo has MD5 `626c3a72…`, exactly the
Zenodo file's MD5 — so `main.tex` is the source of the deposited version of record.

Not the format: the same tree's `prd/main.tex` is a REVTeX 4.2 two-column rebuild made
for journal submission. It is NOT the deposited paper's format and was not used.

## 2. The RCPH format fingerprint (from main.tex)

- `\documentclass[11pt]{article}`, letter paper
- geometry margin 2.5 cm
- Packages: amsmath, amssymb, booktabs, tabularx, graphicx, hyperref (hidelinks)
- `\emergencystretch 1.5em`
- Front matter: `\maketitle` with author block
  `T.~Pierson\\ Axiovex Systems, LLC\\ \texttt{research@axiovexsystems.com}`,
  date line "Revised draft — October 2026", then an `abstract` environment
- Numbered `\section` / `\subsection` hierarchy, Computer Modern fonts throughout
  (pdfTeX output: CMR17 title, CMR12 headings/body at 11pt, CMBX10, CMR10)
- Bibliography: `\bibliographystyle{plain}` + `\bibliography{references}`
  (numbered reference list)
- Appendices via `\appendix` + `\section`
- No running headers; page number centred in the footer (article class default)
- RCPH paper length in this format: 19 pages

## 3. What the Indus v11 draft looked like before

The v11 draft .tex was Pandoc-generated: `\documentclass{article}` at 10pt, Noto Serif
via unicode-math under LuaLaTeX, parskip paragraph spacing, section numbering off, the
title set as a `\section`, empty author/date, manual numbers typed into heading titles
("1. Introduction" as a subsection), references as an itemize list (35 items),
9 longtables, 0 figures, geometry margin 1in. Visually unrelated to the RCPH paper.

## 4. Every change made to produce the formatted variant

File: `pierson_2026_indus_decipherment_v11_formatted.tex`, produced from the v11 draft
by `transform_format.py` (asserts at every step; content text untouched).

Format mechanics only:

1. Preamble replaced with the RCPH fingerprint above (11pt article, geometry 2.5 cm,
   amsmath/amssymb/booktabs/tabularx/graphicx/hyperref hidelinks, emergencystretch).
   Kept from the draft preamble only what the content needs: longtable, array,
   multirow, etoolbox, ulem, xcolor, footnotehyper, and the macron-below composites
   (see build notes).
2. Front matter rebuilt as `\title` / `\author` / `\date` / `\maketitle` in the RCPH
   shape (same author block: T. Pierson, Axiovex Systems, LLC,
   research@axiovexsystems.com), followed by the draft's DOI/version lines and its
   headline note, then the abstract in an `abstract` environment.
3. Heading structure rebuilt from the draft's manual numbering: 7 `\section`s,
   44 `\subsection`s (from x.y titles), 4 `\subsubsection`s (from x.y.z titles);
   the typed-in numbers removed (numbering now comes from the counters, as in RCPH).
4. References converted from the 35-item itemize list to a numbered `thebibliography`
   list in the plain style's shape (the draft carries no .bib file, so the list is
   inlined; rendering matches `\bibliographystyle{plain}` output).
5. The three appendices placed under `\appendix` as `\section`s.
6. Nine Pandoc separator-rule blocks (horizontal rules used as section decoration)
   dropped — the RCPH format has no such decoration.

No sentence, number, table value, or claim was changed. The only words that moved are
format mechanics (heading numbers are now counter-generated; the reference list is now
numbered instead of bulleted).

## 5. Build

- Engine: LuaLaTeX (durable TeX Live 2026, `~/workspace/tools/texlive/2026/bin/x86_64-linux/`),
  two passes. Exit 0, 0 errors, 0 missing characters, 0 warnings.
  2 overfull + 7 underfull hboxes remain (typographic only).
- Output: `pierson_2026_indus_decipherment_preprint_v11_formatted_DRAFT.pdf`,
  39 pages, letter size.
- Build notes: the tables use Pandoc's `\LTcaptype{none}` trick, which needs
  `\newcounter{none}` in this preamble. Latin Modern lacks three macron-below letters
  used in the Tamil transliteration (ṉ U+1E49, ṟ U+1E5F, ḻ U+1E3B); they are composed
  with the `\b` accent via active-character definitions. (The `newunicodechar` package
  is not in the basic TeX Live scheme; CTAN fetches from this VM returned 0 bytes on
  2026-11-18 and were abandoned in favour of the in-tree solution.)

## 6. Content-identity check

pdftotext word diff, unformatted v11 draft vs formatted variant: 22,560 vs 22,554
words, 212 diff hunks — every hunk classified as an extraction artifact (line-break
hyphenation joins, "1." vs "1" heading numbers, math-glyph codepoint variants,
the "Date:" label dropped by the `\date` mechanic, longtable cell reordering in
extraction). No content difference found.

The v11 §5 updates verified present and identical in both extractions, including:
"71 of the 94 as supported at all, 6 of them on outside evidence and 65 on the
program's internal…" and "The six were tested one by one against the evidence of
record, and none of the six is identifiable at that standard…".

## 7. Visual comparison

Page 1 and page 4 of both PDFs rendered to PNG (in `compare/`):
`rcph-p1-01.png`, `rcph-p4-04.png`, `indus-fmt-p1-01.png`, `indus-fmt-p4-04.png`.

Verdict: the formats visibly match — centred Computer Modern title, the same author
block shape, date line, narrow centred abstract with bold "Abstract", indented body
paragraphs, bold numbered section/subsection headings, centred footer page number,
same margins and page feel. The Indus page 1 carries extra front-matter content
(the DOI block and the headline note) between the date and the abstract — that is
content the RCPH paper does not have, not a format difference.

## 8. Hashes

- Formatted .tex: SHA-256 `a0270b67abd9deccd8cde9c454c7d4d183bbb8e6895f1a1bb3d2a31c3f20efab`
- Formatted PDF: SHA-256 `47d2c10a927161c99862cca2eb2c2845bc2685dd27d34525c6403acf8a636707`
- Source v11 draft .tex (unchanged): SHA-256 `42ed3cbd822410460af5459b1faea4c6af0dc681023b855721a61878a1a643f7`
