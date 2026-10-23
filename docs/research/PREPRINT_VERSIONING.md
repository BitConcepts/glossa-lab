# Preprint Versioning — Indus Decipherment Paper

## Canonical identifiers

| Field | Value |
|-------|-------|
| **Title** | A Falsifiable Computational Decipherment Hypothesis for the Indus Valley Script: 161 Candidate Proto-Dravidian Anchors and a Three-Slot Positional Grammar |
| **Author** | Tristen Kyle Pierson / BitConcepts LLC |
| **Contact** | tpierson@bitconcepts.tech |
| **DOI (Zenodo)** | https://doi.org/10.5281/zenodo.20379070 (concept DOI — resolves to the latest version; corrected 2026-10-23 from the stale v3 version DOI 10.5281/zenodo.20414696) |
| **SSRN submission** | ID 6827038 (status: check SSRN portal) |
| **Source file** | `glossa-corpus/indus/pierson_2026_indus_decipherment.tex` |
| **PDF (current)** | `glossa-corpus/indus/pierson_2026_indus_decipherment_preprint_v8.pdf` (v8 compiled artifact, regenerated 2026-10-23 — two clean XeLaTeX passes, 19 pages; supersedes the v7 PDF) |
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
| **v6 (.tex + PDF)** | 2026-10-22 | **Current.** Bibliography completion from the spec-025 audit fix commission: §8 gains the five Mahadevan works the text already relied on (1981 Place Signs; 1982 Terminal Ideograms; 1986 Towards a Grammar; 1989 What Do We Know; 2011 The Indus Fish Swam in the Great Bath), from records verified at published-bibliography level (the 2011 identification is inferred — see the audit fix addendum); the §3.23 paper counts are qualified in place as this program's own text-mining corpus counts (internal outputs, not externally sourced). The §8 Steinkeller 1982 entry is UNCHANGED and stands flagged as unverified (fix addendum, P10: positive evidence the titled article is JAOS 108(2):197–202 (1988); the 1988 record was not substituted, per the proposal's own rule). **The v6 PDF HAS been regenerated** (TinyTeX XeLaTeX provisioned under the workspace; two passes, zero errors, 18 pages; corrected entries spot-checked in the rendered output) and replaces the v4 PDF as the compiled artifact. Adversarial pass run on the v6 source and adjudicated (`specs/025-paper-search-research-check/audit-2026-10-22/adversarial_pass_2026-10-22.md`): one finding sustained in narrow form (the §2.1 Zipf exponent ~1.7 is the paper's own unreleased-corpus statistic, printed without a checkable derivation — an owner decision for submission time). Nothing has been submitted. |
| **v7 (.tex + PDF)** | 2026-10-22 | **Current.** Roif credit (owner-directed addenda to the spec-025 audit fix commission; record: `specs/025-paper-search-research-check/audit-2026-10-22/roif_credit_addendum_2026-10-22.md`). §8 gains both Roif citations (2025a, Academia.edu 12 June 2025, academia.edu/129921039; 2025b, 2 August 2025, academia.edu/143222807 — Academia mints no DOIs; the stable URLs are the identifiers). §3.5 and §3.19 now credit the fish-sign model to Avishai Roif in his own terms (fish read /mi/ (mīn) as value/divine marker and guild/title marker, 2025a; the "coastal controller" maritime-guild reading, 2025b) and state the division of labour: his model and predictions, this program's measurements. §7 Acknowledgments gains a Roif entry in the same terms. §3.32 (betweenness) is NOT restored: a marked restoration draft is filed with the package, HELD PENDING ROIF'S REPLY (owner is asking his Semiotica status and whether he wants the section restored as co-author). The v7 PDF HAS been regenerated (two clean XeLaTeX passes, zero errors, 18 pages; Roif entries, credit paragraphs, and acknowledgment spot-checked in the rendered output). Nothing has been submitted. |
| **v8 (.tex + PDF)** | 2026-10-23 | **Current.** F2 Zipf qualification + Spec 068 integration (record: `specs/025-paper-search-research-check/audit-2026-10-22/v8_version_note_2026-10-23.md`). §2.1's Zipf sentence is qualified in place: the ~1.7 exponent is the program's own statistic on the Holdat corpus with no published checkable derivation, and is no longer presented as evidence that the script is a language; Yadav et al. (2010) is cited for the published Zipf--Mandelbrot fit and its own stated limit, and the Yadav entry is added to §8 (after Wells & Fuls). New §2.1.1 reports the Spec 068 (Phase-430; OSF 3pbwe) registered test of what a frequency-curve fit can show: on the Shakti corpus (ICIT line; 3,045 documented-lineage rows; 11,805 tokens; 557 signs) the frozen Zipf--Mandelbrot rule gave α = 2.004, fit error 0.1584 (documented + corroborated rows: α = 1.96, error 0.1544), while Linear B — the one certain writing system among the four controls — fitted worst (0.9229); registered outcome COMPARISON UNINFORMATIVE. §3.10 applies the same qualification to Nair's Zipf slope. NOT changed: everything else from v7, including all Roif credit; §3.32 remains absent/held. The Spec 072 (Phase-431) fish-family result is NOT integrated — its insert is filed HELD at `glossa-corpus/indus/pierson_2026_indus_decipherment_spec072_insert_HELD.md`. **The v8 PDF HAS been regenerated** (TinyTeX XeLaTeX, two clean passes, zero errors, 19 pages — v7 was 18; SHA-256 0f70dece76d3cdd31fa2ccb5c9fdbc9c2953587a9895700b8cf4632cd81f6670; all v8 changes verified in the rendered output). An independent red-team pass on v8 is IN PROGRESS under the standing rule. Nothing has been submitted. **Post-closure correction (2026-10-23, owner-ruled):** the red-team loop later CLOSED at round 8 (record: the v8 version note); after closure, the printed DOI was corrected — it was the stale v3 version DOI (10.5281/zenodo.20414696), and the title block plus this file's canonical identifiers now give the concept DOI 10.5281/zenodo.20379070. The §6 pin advanced to revision commit 822f655d (branch `preprint-v8-doi-correction`) and the PDF was rebuilt (two clean XeLaTeX passes, 32 pages, SHA-256 6d5b1e7fc7627cfc5f861f8f285c6a765fee7eda31f710eed3c8cd38633b2ead). Record: the post-closure correction entry appended to the v8 version note. |

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

## Current version: v8 (.tex source + PDF, 2026-10-23)

v8 resolves the spec-025 audit's F2 finding on the §2.1 Zipf
sentence by qualifying it in place (the ~1.7 exponent is now
presented as this program's own uncheckable corpus statistic, no
longer as evidence the script is a language), adds §2.1.1
reporting the Spec 068 (Phase-430) registered frequency-curve
test with its registered outcome (COMPARISON UNINFORMATIVE),
applies the same qualification to Nair's Zipf slope in §3.10, and
adds the Yadav et al. (2010) entry to §8. The Spec 072
fish-family result is NOT integrated; its insert is filed as a
HELD document. Record:
`specs/025-paper-search-research-check/audit-2026-10-22/v8_version_note_2026-10-23.md`.
The v8 PDF has been regenerated (two clean XeLaTeX passes,
19 pages) and is the compiled artifact of record; the v7 PDF is
superseded. An independent red-team pass on v8 is in progress
under the standing rule. **Nothing has been submitted or deposited.**

v7 adds the Roif credit: both Roif 2025a/b citations in §8,
fish-sign model credit in §3.5 and §3.19 in Roif's own terms with
the division of labour stated (his model and predictions; this
program's measurements), and an acknowledgment entry naming him
as the source of the fish-sign model. §3.32 is not restored; its
restoration draft is filed with the package, held pending Roif's
reply. The v7 PDF has been regenerated (two clean XeLaTeX passes,
18 pages) and is the compiled artifact of record; the v6 PDF is
superseded. **Nothing has been submitted or deposited.**


v6 completes the bibliography the text already relied on (five
Mahadevan §8 entries, audit proposal P9) and qualifies the §3.23/§3.24
paper counts in place as the program's own text-mining outputs. The
§8 Steinkeller 1982 entry is unchanged and flagged as unverified in
the audit fix record (P10 — the 1988 same-title record was not
substituted). The v6 PDF has been regenerated (two clean XeLaTeX
passes, 18 pages) and is the compiled artifact of record; the v4 PDF
is superseded. An adversarial pass on the v6 source was run and
adjudicated (audit directory, `adversarial_pass_2026-10-22.md`): one
finding sustained in narrow form (the §2.1 Zipf exponent ~1.7 is the
paper's own unreleased-corpus statistic without a checkable
derivation — flagged for the owner's submission decision).
**Nothing has been submitted or deposited.**
