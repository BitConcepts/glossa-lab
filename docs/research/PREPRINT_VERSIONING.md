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
| **PDF (current)** | `glossa-corpus/indus/pierson_2026_indus_decipherment_preprint_v4.pdf` (v4 compiled artifact; the source `.tex` is at v5 since 2026-10-22 — v5 PDF regeneration pending) |
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
| **v5** | — | **DRAFT ADDENDUM — NOT PUBLISHED.** Addendum drafted in-repo 2026-10-06 (Phase-109, spec 007) recording the post–Phase-107/108 headline re-base (strict SA-independent set: 94 H+M, 73.68% coverage). Draft: `glossa-corpus/indus/pierson_2026_indus_decipherment_addendum_v5.md`. (This addendum draft predates the v5 `.tex` bump below; renumbering it is an owner decision.) |
| **v5 (.tex)** | 2026-10-22 | **Current source.** Citation corrections from the spec-025 material audit (`specs/025-paper-search-research-check/audit-2026-10-22/`): §8 entries corrected for Wells & Fuls (2015, not Wells 2011), Parpola/Parpola/Brunswig (1977, JESHO 20(2), Simo Parpola first author), Crawford 2001 (monograph, not a journal article), and Parpola 2010 (CICT conference lecture, Coimbatore — the *World Archaeology* 42(2) attribution was not verified in any reachable index); Rao *Science* 2009 entry added and the §1.2 entropy result attributed to it; the §2.1 Zipf exponent no longer attributed to Rao 2009; Nair 2026 characterizations in §1.3/§3.10/Acknowledgments corrected to match Nair's full text (independent scorecard study, hedged intermediate result — not a replication of this paper's tests). **The v5 PDF has NOT been regenerated** (no xelatex in the audit environment); the v4 PDF remains the compiled artifact of record. Nothing has been submitted. **Adversarial pass required before submission.** |

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

## Current version: v5 (.tex source, 2026-10-22)

v5 carries citation corrections only (spec-025 material audit; see the
version table). The v4 text was confirmed clean as of 2026-06-09: zero
references to Avishai Roif or any unconsented correspondence material,
verified by full PDF read-through. The v5 PDF has not been regenerated
yet; the v4 PDF remains the compiled artifact of record. **Adversarial
pass required before submission of any new version.**
