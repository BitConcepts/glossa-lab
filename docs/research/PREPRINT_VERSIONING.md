# Preprint Versioning — Indus Decipherment Paper

## Canonical identifiers

| Field | Value |
|-------|-------|
| **Title** | A Falsifiable Computational Decipherment Hypothesis for the Indus Valley Script: 161 Candidate Proto-Dravidian Anchors and a Three-Slot Positional Grammar |
| **Author** | Tristen Kyle Pierson / BitConcepts LLC |
| **Contact** | tpierson@bitconcepts.tech |
| **DOI (Zenodo)** | https://doi.org/10.5281/ZENODO.20414696 |
| **SSRN submission** | ID 6827038 (status: check SSRN portal) |
| **Source file** | `glossa-corpus/indus/pierson_2026_indus_decipherment.tex` |
| **PDF (current)** | `glossa-corpus/indus/pierson_2026_indus_decipherment_preprint_v4.pdf` |
| **Research anchor** | `research/indus/indus-anchor-model/` |

## Filename convention

- **Source `.tex`**: `pierson_2026_indus_decipherment.tex` (stable — never rename)
- **PDF**: `pierson_2026_indus_decipherment_preprint_v{N}.pdf` — rename the PDF on each
  new version so the version is visible in the filename

The version number is also declared inside the document (title block and footer).

## Version history

| Version | Date | Description |
|---------|------|-------------|
| **v1** | May 2026 | Initial draft. 161 H+M anchors, 90.96% coverage. Included §3.32 betweenness centrality analysis and fish-sign polysemy framing. |
| **v2** | May–June 2026 | Added Zenodo DOI. Corrected §3.5 attribution issue. |
| **v3** | June 2026 | Interim revision (attribution cleanup, internal). |
| **v4** | June 2026 | **Current.** Removed all uncited correspondence material. §3.5 renamed "Fish Sign Isolation Test" (was "Polysemy Test"). §3.32 removed entirely. Zero third-party unconsented content. Abstract and all references to fish-sign analysis updated to use neutral structural language. |

## How to bump the version

1. Edit `glossa-corpus/indus/pierson_2026_indus_decipherment.tex`:
   - Line ~81: `Version: Preprint vN --- Not peer-reviewed`
   - Last line before `\end{document}`: `\emph{End of Preprint vN}`
2. If distributing, also update the date line: `Date: Month YYYY (revised Month YYYY)`
3. Recompile: `xelatex -interaction=nonstopmode pierson_2026_indus_decipherment.tex` (run twice)
4. If PDF is locked: compile with `-jobname=preprint_tmp`, copy over when viewer is closed
5. Rename the PDF: `git mv pierson_2026_indus_decipherment_preprint_v{N-1}.pdf pierson_2026_indus_decipherment_preprint_vN.pdf`
6. Update this file's version table
7. Update `AGENTS.md` **Source**, **PDF**, and **Current version** fields
8. If publishing: upload new PDF to Zenodo as a **new version**; update SSRN with "Submit a Revision"
9. Commit: `git add glossa-corpus/indus/ docs/research/PREPRINT_VERSIONING.md AGENTS.md && git commit -m "preprint: bump to vN"`

## Attribution policy (enforced)

- **No private correspondence material** may appear in any version without explicit
  written consent from the originating researcher, regardless of attribution.
- **No uncited hypothesis, framing, or analysis** from a third party may appear even
  in paraphrase. If in doubt, remove it.
- Any attribution concern → email `tpierson@bitconcepts.tech` immediately.
- See `ATTRIBUTION.md` for full data-source licensing.

## Current version: v4

Confirmed clean as of 2026-06-09. Zero references to Avishai Roif or any
unconsented correspondence material. Verified by full PDF read-through.
