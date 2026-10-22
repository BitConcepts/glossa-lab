# Fix execution addendum — Material Audit 2026-10-22 (batches A and B)

Owner order 2026-10-22: "fix all of these and make all the corrections
and get back on track." This addendum records what the fix commission
executed against `correction_proposals.md` (P1–P10) and the audit's
open gaps. Batch C (P9, P10, preprint v6, adversarial pass) is recorded
in `fix_completion_2026-10-22.md`. Plain language; evidence levels are
marked on every item, and abstract-level bounds are carried verbatim.

## Per-proposal execution (batch A — PR #334)

- **P1 — LANDED.** Dated framing note (`audit_note_2026_10_22`)
  appended to the Farmer dossier's claim: the literature position is
  contested and unresolved (Sproat 2014 and Rao et al. 2010, FULL
  TEXT). The claim's status was not changed — a status change belongs
  to the program's adjudication gate, and the proposal asked for none.
- **P2 — LANDED.** fuls2023 literature record: `detected_year`
  2008 → 2023, title and author corrected in place; old values
  preserved in an appended `metadata_correction` record.
- **P3 — LANDED.** Roif literature record: `detected_doi` removed (it
  was a Sarton 1955 bibliography hyperlink); the record now states,
  via `metadata_correction`, that the document is a self-published
  manuscript with no venue, date, or identifier of its own.
- **P4 — LANDED.** Fuls chapter literature record: author (Andreas
  Fuls), year (2020), and full title corrected; the removed DOI
  belongs to Fuls 2015, *Historical Linguistics* 128(1):42–58
  (Crossref-verified); the chapter's venue (Studies on Indus Script,
  Mohenjodaro 2020, pp. 57–88 plus appendix) is in the correction
  record. Aligned with Spec 065's earlier identity resolution.
- **P5 — LANDED.** `docs/research/DECIPHERMENT_DOSSIER_v1.md`: both
  occurrences of "Nair (2026) scorecard: 4/4 linguistic-consistent"
  corrected to Nair's own framing — 4/4 against the heraldic baseline,
  2/4 against the administrative baseline, an intermediate conclusion
  that does not settle the linguistic question (Nair 2026, FULL TEXT).
- **P6 — LANDED.** Priority/critique note appended to both Parpola
  dossier claims: the fish = mīn rebus is Heras's (1930s); Parpola
  2010 is a synthesis; Mahadevan 2011's "run out of steam" critique
  and the rival fish values are on the note, with the Mukhopadhyay
  item bounded at abstract level.
- **P7 — LANDED.** Yadav dossiers (both files, all four claims):
  corpus-scope note on the Zipf claims (the fit ran on the pruned
  EBUDS subset of M77; b = 2.59 is not the Phase-43 ~1.35) and
  priority note on the beginner/ender claims (Soviet 1965, Finnish
  1969, Kondratov 1976 at metadata level, Mahadevan 1977).
- **P8 — LANDED.** Hunt dossier: prior-art notes on the tripartite
  claim and on the faunal-initial / celestial-terminal
  characterisations (the structure is Wells 2015 ch. 3 and earlier;
  the characterisations have no published support in the texts read).
  Fuls source-identification notes on all five "Positional Analysis"
  stub claims, and the positional literature record gained its author.
- **P9, P10 — executed in batch C** on the WS3 evidence below.

No claim status, stage, anchor, or score was changed by any batch-A
edit; every claim edit is one appended key, and each file's statuses
were asserted identical before and after editing. H26 is satisfied by
construction (nothing was promoted; the audit records are the cited
non-SA evidence). The H21 foundation check is asserted in the batch-C
completion record.

## WS2 — Unpaywall tooling fix: CONFIGURED AND PROVEN, with one defect standing

Full record: `raw/fix_ws2_unpaywall_proof.md`. In short: the connector
doc's mechanism is an environment variable set at call time (no address
is baked into files); with `PAPER_SEARCH_MCP_UNPAYWALL_EMAIL` set to
the program contact address, `search_unpaywall` returns full OA data,
and the audit session's failed DOI (Yadav 2010, 10.1371/journal.
pone.0009506) downloads end-to-end **via the Europe PMC route** — the
artifact identity-checked first-hand (correct title, authors, and DOI
printed on page 1; SHA-256 `b3e79817…`). **Standing defect:** the
`crossref` source route of `download_with_fallback` served a second
distinct wrong paper for the same DOI and the server's stat stage then
crashed. Downloads from that route must be identity-checked before any
use; the europepmc/pmc routes with explicit paper ids are the proven
path.

## WS3 — Open gaps: what a fresh session closed, and what stays open

Full evidence: `raw/fix_ws3_evidence_notes.md` (a transcription of the
worker's in-session tool outputs — the original raw JSONs were lost in
a service restart; the file records the exact regeneration arguments,
and `raw/fix_ws3_handoff.md` documents the interruption). Items the
coordinator re-verified first-hand are marked ◆.

- **Rao et al. 2009, *Science* (DOI 10.1126/science.1170391) — CLOSED,
  upgraded from abstract level to FULL TEXT** (main text + Supporting
  Online Material, read from the author's posted copy stamped
  "Downloaded from www.sciencemag.org on May 30, 2009"). Nothing in the
  preprint is falsified by it: the paper's own claim is a probability
  increase, not a proof ("our results increase the probability that the
  script represents language"). The Zipf–Mandelbrot parameters
  (a = 15.39, b = 2.59, c = 44.47) are located precisely: they are in
  the paper's Supporting Online Material, citing Yadav et al.
  (arXiv:0901.3017), and in Yadav et al. 2010, Fig. 3 — not in the
  PNAS paper, and b is 2.59, not ~1.7.
- **Rao et al. 2009, PNAS (DOI 10.1073/pnas.0906237106) — CLOSED, FULL
  TEXT** (PMC2721819, read in full). **"Zipf" appears nowhere in the
  paper** — audit correction #6, which removed the Rao attribution
  for the ~1.7 exponent on abstract-level checking, is now confirmed
  at full-text level. Verified title: "A Markov model of the Indus
  script", PNAS 106(33), 13685–13690. ◆ The Crossref record for this
  DOI was re-fetched by the coordinator and matches (`raw/fix_ws3_rao_
  pnas_crossref.json`).
- **Wells 1998 thesis (DOI 10.11575/PRISM/23641) — RESOLVED at record
  level.** Bryan Wells, "An Introduction to Indus Writing", MA thesis,
  Department of Archaeology, University of Calgary, January 1998;
  hdl 1880/25900 — consistent across the thesis title page (quoted in
  a secondary work) and two independent records. The coordinator's one
  direct fetch of the DOI landing page failed at the tool level and was
  not retried; the record-level resolution stands on the title page
  and the secondary records, and the direct repository fetch remains a
  small open item.
- **Kak 1988 — EXAMINED; stays open, narrowed.** Crossref metadata
  verified (Cryptologia 12(3):129–143, DOI 10.1080/0161-118891862873;
  no abstract in the record). At secondary level (Kak's own later
  summary): a computer-concordance frequency/probability comparison of
  Indus vs Brahmi — the most frequent signs looked almost identical and
  in the same frequency order. **No source seen reports Kak fitting a
  Zipf-type law or a Zipf exponent**; a Zipf attribution to Kak 1988
  would be unsupported at this evidence level. The full text (Taylor &
  Francis) was not reached and no lawful open-access copy was found,
  so outright falsification stays open.
- **The five in-text Mahadevan works — VERIFIED at published-
  bibliography level** (Jyothibabu 2023, *Studia Orientalia Electronica*
  11(1), DOI 10.23993/store.85246, bibliography; not direct Crossref/
  WorldCat records — the level is stated, per the abstract-bound
  rule's spirit): 1981 "Place Signs in the Indus Script", Proc. Fifth
  Int. Conf.-Seminar of Tamil Studies 1(2):91–107 (Madurai: IATR);
  1982 "Terminal Ideograms in the Indus Script", in Possehl (ed.),
  *Harappan Civilization*, pp. 311–317 (Oxford & IBH) — independently
  corroborated verbatim; 1986 "Towards a Grammar of the Indus Texts",
  *Tamil Civilization* 4(3&4):15–30 — corroborated by Mukhopadhyay
  2019; 1989 "What Do We Know about the Indus Script?", *Journal of
  the Institute of Asian Studies* 7(1):1–38 (a possible 1988
  *Proceedings of the Indian History Congress* version is flagged, not
  merged); 2011 "The Indus Fish Swam in the Great Bath", *Bulletin of
  the Indus Research Centre* 2:1–73 — corroborated twice; the
  identification of this work as the preprint's 2011 citation is
  **inferred** (it is the only 2011 Mahadevan Indus work found), and
  that bound travels with the entry wherever it is used. These records
  feed P9 in batch C. **The two aggregate counts ("10 Mahadevan papers
  1972–2018"; "38 Mahadevan papers 1970–2018") could not be tied to
  any verifiable source** — batch C qualifies them in the text as the
  program's own text-mining outputs.
- **Steinkeller 1982 — NARROWED; stays open (P10).** Positive evidence
  that the titled article is the 1988 one: "On the identity of the
  toponym LÚ.SU(.A)", JAOS 108(2):197–202, DOI 10.2307/603646 —
  corroborated by PhilPapers, a scholarly citation, and a footnote in
  JAOS 108.1 (1988) calling it "JAOS 108.2, forthcoming", i.e. in early
  1988 the titled article did not yet exist. A genuine 1982
  Steinkeller demonstration that "Su-people" = Shimashki is attested
  secondarily (*The Sumerian World*; a "Steinkeller (1982:261 n. 7)"
  citation), so the preprint most likely conflated a real 1982 item
  with the 1988 article's title and venue — but the 1982 item's venue
  and pages were **not** verified, and the contents of JAOS 102(2)
  pp. 299–309 were never directly inspected. Per P10's own text, the
  1988 record is **not** substituted; the entry stays flagged as
  unverified (batch C carries the flag into the version record).

No source returned a fresh 429 this session; no retry loops were run;
Sci-Hub was never used.

## WS5 — Public surface: NO MUST-FIX; one clarifying draft filed

`public_surface_check_2026-10-22.md` (this directory) holds the full
check and the draft. In short: neither `bitconcepts.tech/research/`
nor `bitconcepts.tech/research/indus-script/` states any of the four
corrected items. The Indus page's Registered predictions section
presents the 3-slot pattern without attribution, so a clarifying
prior-art note is drafted there for the owner's approval through the
website chat's process — **nothing was published or pushed**. One
limitation is recorded: the page's "Study papers & key links"
bibliography entries were not present in the fetched text, so that
section should be re-checked before the page's next edit.
