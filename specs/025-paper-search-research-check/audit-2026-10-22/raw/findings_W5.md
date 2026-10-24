# Findings — Worker W5 (Glossa Lab material audit, 2026-10-22)

Scope: 8 claims from two dossiers. RESEARCH-CHECK stage run for all 8
(records in `glossa-indus/claims/research_checks/`, all exit 0, verdict
null by construction). Manual protocol queries saved as
`raw/W5_q01…q27_*.json` (+ `.err` logs); stage log at
`raw/W5_stage_runs.log`.

Evidence-level labels: **FULL TEXT** = the source's full text was read
(held source documents, or OA full text via the client). **At abstract
level** = metadata/abstract only; such lines establish nothing about
novelty or its absence by themselves.

Sources searched: federated `search_papers` (arXiv, Crossref, CORE,
Europe PMC, bioRxiv/medRxiv, …), Crossref (search + DOI lookup),
CORE, SSRN (search timed out; DOI lookup via Crossref worked),
arXiv full text. **Source failures / rate limits (recorded, not
retried):** Semantic Scholar returned 429 during the stage runs (see
stage log) and on manual query q02 — treated as done for the session;
its later queued single attempts (q06, q09, q12) also returned empty.
OpenAlex returned 429 from q07 onward — done for the session.
BASE not searched (expected-empty per protocol doc). Zenodo sub-source
errored inside federated searches (`'str' object has no attribute
'isoformat'`). SSRN search timed out (q16); SSRN PDF download timed
out twice (q25, q27 fallback chain; Unpaywall had no OA URL).

---

## Source status of the two documents (Task 4)

### 1. `indus_valley_script_deciphered_from_myth_65ff0a26` — Roif

- The held document's own first page (**FULL TEXT**): "Indus Valley
  Script deciphered — From Mythology to History using the Akkadian
  shorthand approach. By: Avishai Roif. Edited and Abbreviated using
  the assistance of AI." No journal, publisher, venue, date, or DOI
  appears anywhere in the document text (grep over the held cleaned
  text: every DOI string in it belongs to its bibliography).
- The intake record's `detected_doi` 10.2307/595168 is a bibliography
  hyperlink inside the document (held text line 532, under the
  Oppenheim 1954 entry). Verified by Crossref DOI lookup (q14):
  10.2307/595168 is George Sarton, "Chaldaean Astronomy of the Last
  Three Centuries B. C.", *Journal of the American Oriental Society*
  75(3):166, 1955 — **not** a Roif publication.
- No bibliographic record for an Avishai Roif Indus paper was found in
  the sources searched: Crossref author/title search (q04) returned
  only an unrelated Indonesian author named Roif; the federated search
  on the paper's title/author (q03) returned no Roif item among its
  results; Semantic Scholar and OpenAlex were 429-unavailable (gap,
  below).
- Conclusion the sources support: as far as Crossref, the federated
  indexes, and the document itself show, this is a **self-published /
  unpublished manuscript (user-uploaded PDF), with no venue, no
  identifier of its own, and no evidence of peer review**. Dossiers
  should describe it that way, not as a published paper.

### 2. `ancient_writing_and_modern_technologies_51831ac9` — not Roif

- **Correction to the audit tasking:** this document is not a Roif
  paper. Its held full text is headed (**FULL TEXT**): "Ancient
  Writing and Modern Technologies – Structural Analysis of Numerical
  Indus Inscriptions — Dr. Andreas Fuls, Technische Universität
  Berlin."
- Venue, from the held volume's own front matter (**FULL TEXT**,
  printed pp. III–IV, bound into the same PDF): *Studies on Indus
  Script — Conference on Indus Script, Mohenjodaro 2020*, publisher
  National Fund for Mohenjodaro, Culture, Tourism, Antiquities and
  Archives Department, Government of Sindh; "Published Provisionally
  2020". The chapter runs pp. 57–88 plus Appendix A (the 702-sign ICIT
  sign list). So: a **conference-proceedings chapter (2020)**, not a
  journal article; no DOI for the chapter was found in Crossref
  (title searches q11/q17 returned instead Fuls's appendices in Wells
  2015 — see below).
- The intake record's `detected_doi` 10.13109/hisp.2015.128.1.42 is a
  bibliography self-citation inside the chapter. Verified by Crossref
  DOI lookup (q15): Andreas Fuls, "Classifying Undeciphered Writing
  Systems", *Historical Linguistics* 128(1):42–58, 2015, Walter de
  Gruyter — a different, peer-reviewed Fuls article, **not** this
  chapter.
- Fuls's related scholarly record verified at metadata level
  (Crossref, q11/q17): Appendix I (pp. 100–118, DOI
  10.2307/j.ctvr43jmf.15) and Appendix II (pp. 119–133, DOI
  10.2307/j.ctvr43jmf.16) in Bryan K. Wells, *The Archaeology and
  Epigraphy of Indus Writing*, Archaeopress, 2015. His bibliography
  in the held chapter also lists Fuls 2013, "Positional Analysis of
  Indus Signs", *Voprosi Epigrafiki* 7(1):253–275 (**FULL TEXT** as
  cited in the chapter's own literature list; no Crossref record for
  it surfaced in the searches).

---

## Prior-art question (a): Akkadian/mnemonic or guild-ledger readings

- **Roif's specific package** (Akkadian trade mnemonics + Proto-
  Dravidian phonetics → script as guild/tribute ledger): **no
  scholarly prior art found in the sources searched** (federated
  search q01/q03, Crossref q04; Semantic Scholar/OpenAlex 429 —
  gap). Nothing in the retrieved literature proposes an
  Akkadian-mnemonic decipherment mechanism. This is a statement about
  the sources searched, not proof the claim is false.
- **Nearest neighbor 1 — the guild/economic-function family, at
  metadata level:** Bahata A. Mukhopadhyay, "Guild-Based Trading,
  Taxation, Tax Farming, Trade and Craft
...[truncated 10309 chars]