# Corrections log — Material Audit 2026-10-22 (spec 025)

Corrections landed by this audit, each with its evidence and evidence
level. Raw outputs are in `raw/` in this directory. Worker findings:
`raw/findings_W1.md` … `raw/findings_W6.md` (plus
`raw/findings_W5_part2.md`, the coordinator reconstruction of W5's
truncated remainder, and `raw/findings_W4.md` §6/addendum for stage
records). Items that need a program gate the audit cannot run are NOT
here — they are in `correction_proposals.md`, marked gate-pending.

## Batch 1 — Preprint v5 (`glossa-corpus/indus/pierson_2026_indus_decipherment.tex`)

Version bumped v4 → v5 per `docs/research/PREPRINT_VERSIONING.md`
(version lines + date line; version table and `AGENTS.md` updated).
The v5 PDF was not regenerated (no xelatex in the audit environment);
the v4 PDF remains the compiled artifact of record. Nothing was
submitted anywhere. **Adversarial pass required before submission.**

1. **§8 Wells entry — year, co-author.** Was: "Wells, B. (2011).
   *The Archaeology and Epigraphy of Indus Writing*. Oxford:
   Archaeopress." Now: "Wells, B. & Fuls, A. (2015). …
   Archaeopress." Also §1.2 "Wells (2011)" → "Wells & Fuls (2015)".
   Evidence: Crossref/JSTOR monograph record DOI 10.2307/j.ctvr43jmf
   (Bryan K. Wells & Andreas Fuls, Archaeopress, 2015-02-06) —
   metadata level, resolved record (`raw/W6_*`); independently
   corroborated in full text by W4's held copy of the book and by
   Nair 2026's reference list (FULL TEXT). The preprint's own
   §3.20/§3.24 already cited the book as "Wells (2015)".

2. **§8 Parpola, Parpola & Brunswig entry — year, volume, author
   order.** Was: 1975, JESHO 18(2), Asko Parpola first. Now: 1977,
   JESHO 20(2), 129–165, Simo Parpola first. Evidence: Crossref DOI
   record 10.2307/3631775 (Simo Parpola; Asko Parpola; Robert H.
   Brunswig; published 1977-05-01; volume 20, issue 2, start page
   129) — metadata level, resolved record (`raw/W6_crossref_parpola1975.json`),
   re-read first-hand by the coordinator. Bound: the resolved record
   gives the start page only; the end page 165 is carried over from
   the printed entry, unverified.

3. **§8 Crawford entry — publication type.** Was: cited as an article
   in *Archaeology International*. Now: the monograph *Early Dilmun
   Seals from Saar: Art and Commerce in Bronze Age Bahrain* (2001).
   Evidence: Crossref-resolved review records of the monograph (AJA
   2003, DOI 10.1086/ajs40025410; JNES 2002, DOI 10.2307/3087532) —
   metadata level (`raw/W6_*`). Bound: the monograph's publisher was
   not resolved this session, so the corrected entry carries no
   publisher rather than an unverified one.

4. **§8 Parpola 2010 entry — venue.** Was: "*World Archaeology*,
   42(2), 178–193." Now: "World Classical Tamil Conference lecture,
   Coimbatore, 25 June 2010. Chennai: Central Institute of Classical
   Tamil." Evidence: the lecture text itself read in FULL TEXT (W3;
   34 pp., front matter of the CICT publication), plus a HAL record
   for the CICT publication. The *World Archaeology* attribution was
   not verified: seven Crossref searches (four phrasings by W3, three
   by W6) plus CORE/Europe PMC/OpenAIRE searches returned no such
   record. Bound: this is "not found in the sources searched", not
   proof no such article exists — OpenAlex and Semantic Scholar were
   429-unavailable all session, and a DOI for the lecture publication
   could neither be confirmed nor ruled out. Open gap, recorded in
   the audit report.

5. **§1.2 Rao attribution + §8 addition.** The entropy result was
   attributed to "Rao et al. (2009)" citing the PNAS Markov paper.
   The entropy result is the *Science* paper. §1.2 now cites "Rao et
   al. (2009, *Science* 324:1165)", and §8 gains the entry: Rao et
   al. (2009), "Entropic Evidence for Linguistic Structure in the
   Indus Script", *Science* 324(5931), 1165. Evidence: Crossref DOI
   record 10.1126/science.1170391 (title, six authors, venue, page)
   — metadata level (`raw/W1_crossref_doi_10.1126_science.1170391.json`),
   re-read first-hand by the coordinator. Bound: the *Science* full
   text was not read this session (the connector's download chain
   failed; the paper is paywalled) — the attribution correction rests
   on the resolved record plus the paper's abstract, i.e. the
   content check is **at abstract level**.

6. **§2.1 Zipf exponent — attribution removed.** The sentence
   "Frequency distribution follows Zipf's law (exponent ~1.7),
   consistent with a natural language writing system (Rao et al.
   2009)" no longer carries the Rao citation: no text read this
   session reports a ~1.7 exponent for Rao 2009. Yadav 2010's fit
   (FULL TEXT, filed as `raw/W1_yadav2010_plosone_fulltext.txt`,
   re-verified first-hand by the coordinator) gives the
   Zipf–Mandelbrot parameter b = 2.59 on the EBUDS subset of
   Mahadevan's M77 corpus — a different corpus and statistic. The
   PNAS paper's Zipf content was checked **at abstract level** (its
   abstract reports no Zipf fit; its full text was not read). The
   ~1.7 figure stands as the preprint's own corpus statistic, like
   its other Holdat-derived numbers (see the reliance map in the
   audit report).

7. **Nair 2026 characterizations (§1.3 bullet, §3.10, Acknowledgments).**
   "Independent replication" wording replaced with "independent
   scorecard study"; §3.10 now states that Nair's corpus is a
   separate digitization of the same published inscription
   assemblage, that his permutation test is a different statistic
   from the Phase-134 F1 test, and that his own conclusion is
   hedged — the corpus sits in an intermediate position, matches the
   administrative baseline on only two of four metrics, and does not
   settle the linguistic question. Evidence: Nair 2026 read in FULL
   TEXT (W6; arXiv:2604.17828; full text filed as
   `raw/W6_nair_fulltext.txt`). All three statistics the preprint
   quotes from Nair (Zipf slope −1.49, conditional entropy 3.23
   bits, permutation percentile 0.000, n = 1,000) were verified
   exact against the full text.

## Batch 2 — Audit records committed (no claim records altered)

- RESEARCH-CHECK stage sidecars for all 31 extracted claims
  (`glossa-indus/claims/research_checks/`), each advisory with
  verdict null by construction, plus the audit directory itself
  (plan, this log, proposals, report, and all raw outputs).
- One pre-existing sidecar (yadav_2009 manual_001, the spec-025
  smoke record) was regenerated by the stage during the audit; its
  content is the stage's own output, as before.

## What was deliberately NOT changed

- No claim status, anchor, score, or verdict anywhere: the audit is
  advisory; status changes go through the program's gates (see
  `correction_proposals.md`).
- §8 entries that could not be resolved (Højlund & Abu-Laban 2012;
  Mitchell 1986; Steinkeller 1982 as cited; the chapter-level
  records for Lubotsky 2001, Kjaerum 1983, Potts 1994) were left
  exactly as printed and are recorded as open gaps — absence of a
  record was not treated as error. In particular the Steinkeller
  entry was NOT "corrected" to the different 1988 same-title record
  that Crossref returned.
- The v5 addendum draft of 2026-10-06 (`addendum_v5.md`) was not
  renumbered; that is an owner decision, noted in the version table.
