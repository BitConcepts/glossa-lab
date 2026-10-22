# Findings W4 — positional-grammar line (audit 2026-10-22)

Worker W4. Scope: the claims the preprint's three-slot grammar headline
rests on — Hunt's tripartite grammar claims, the three "Positional
analysis" stub claims (all merged into
`ancient_writing_and_modern_technologies_51831ac9_statisti_0004`), and
Wells' two sign-value claims (821, 297).

Every item is labelled **FULL TEXT** (the cited work's text was read —
for the four source dossiers, the in-worktree cleaned texts in
`glossa-indus/processed/cleaned_text/`; for arXiv neighbours, the
paper-search full-text reads saved in this directory) or
**at abstract level** (metadata/abstract only). Unreachable works are
recorded as gaps, never as "no prior art".

Sources used: arXiv (works), Crossref (works), CORE (worked once,
then empty), search_papers federation (works; includes Google Scholar
records). **OpenAlex returned empty for every query this session**
(including a control query "Indus script", max 5) despite the API-key
env being set — recorded as an unproductive source, a gap.
**Semantic Scholar returned empty** on its only call — same treatment.
**search_zenodo errored** (tool bug: `'str' object has no attribute
'isoformat'`). No 429 was received from any source; no source was
retry-looped. Sci-Hub not used.

Raw evidence in this directory: `W4_q01`–`W4_q18` query JSON,
`W4_yadav2009_extracted.txt`, `W4_sinha2010_extracted.txt` (full
texts), `W4_stage_*.log`, `W4_stage_runs.log`.

---

## 1. Source identification (task 3)

### 1.1 The "positional analysis" documents — all one work by Andreas Fuls

- **FULL TEXT** — `positional_analysis_of_indus_signs_a2bedc93` is
  Andreas Fuls, "Positional Analysis of Indus Signs", first published
  in *Voprosi Epigrafiki* (Вопросы эпиграфики / Problems of
  Epigraphy), Vol. VII (1): 253–275, 2013, Moscow: Russian Foundation
  for the Promotion of Education and Science / University of Dmitry
  Pozharsky, ISBN 978-5-91244-116-5 (proceedings of the I
  International Conference on Questions of Epigraphy). Venue, year,
  editor (A. G. Avdeev) and ISBN are on the volume's own front matter
  in the in-worktree text; the page range 253–275 is stated in the
  headnote of the reprint (below). The dossier's detected_year 2013
  is correct.
- **FULL TEXT** — The same work is reprinted, with terminology
  standardised, as **Appendix II of Wells & Fuls 2015** (below):
  "This research was first published in Voprosi Epigrafiki Vol. VII
  (1):253-275, 2013." Crossref verifies the appendix as a book
  chapter: Andreas Fuls, "Appendix II:", in *The Archaeology and
  Epigraphy of Indus Writing*, Archaeopress Publishing Ltd, 2015,
  DOI 10.2307/j.ctvr43jmf.16. This is why the Wells dossier
  (`the_archaeology_and_epigraphy_of_indus_w_27f45a68_statisti_0003`)
  also carries a "Positional Analysis" stub: the appendix is inside
  the Wells book (in-worktree text, appendix at pp. 119–132).
- **FULL TEXT** — `fuls2023_catalog_of_indussigns_searchins_1dbdecdb`
  is Andreas Fuls, *A Catalog of Indus Signs*, Mathematica
  Epigraphica No. 4, Berlin 2023, self-published, ISBN
  979-8-398-42230-6 (title page and imprint in the in-worktree text;
  the dossier's detected_year 2008 is wrong — 2008 is the year the
  ICIT database was built, per the book's foreword). Chapter 3 of the
  catalog (pp. 70 ff.) is again "Positional Analysis of Indus Signs",
  the same method extended; §3.3 classifies signs by positional
  behaviour (INS = initial sign, TMK = terminal marker). The catalog
  is the second volume of Fuls' series (Vol. 1: *Corpus of Indus
  Inscriptions*). Not found in Crossref or OpenAlex (self-published;
  OpenAlex was in any case unproductive this session) — identification
  rests on the book's own imprint, FULL TEXT.
- **What Fuls' positional analysis actually is (FULL TEXT, all three
  versions):** a method that computes, for each sign, a histogram of
  *normalised weighted sign position* over complete texts (2,474
  complete, deduplicated texts; 9,700 signs; ICIT corpus), weighting
  short texts less than long ones, and classifies signs as **Initial,
  Early-Medial, Mid-Medial, Late-Medial, Terminal, Post-Terminal**
  (distinguishable only by structural analysis), or **constant**.
  Stated uses: distinguishing allographs from distinct signs
  (graphically similar signs with different positional histograms are
  distinct signs), and grouping signs that share a preferred position
  and " thereby the same syntactic position". Fuls is explicit that
  the classes are positional/syntactic, not semantic: the analysis
  "highlights syntagmatic but not paradigmatic relationships".
  Fuls also states the antecedents himself: "Many Indus signs are
  already recognised as initial or terminal signs (Mahadevan 1977;
  Parpola 1994; Wells 2006)" (Appendix II, FULL TEXT).

### 1.2 The "without kings" document

- **FULL TEXT** — `without_kings_or_conquests_the_indus_scr_ce9d98cc`
  is Treasure A. Hunt (Independent Researcher; "FelineMind Behavior
  Labs"), *Without Kings or Conquests: The Indus Script Deciphered
  and a Civilization Reconstructed*, "Draft Posted September 2025",
  with two supplements (Supplement B: *Indus Script Translation
  Atlas*, September 2025). It is a self-posted draft, not a
  peer-reviewed publication. Searches of OpenAlex (empty session-wide),
  the search_papers federation, and Zenodo (tool error) found **no
  indexed record** of it; identification rests on the document itself,
  FULL TEXT. The manual claims' recorded author ("Hunt, Treasure A.")
  matches.
- The tripartite grammar is Hunt's own framing, stated in the
  abstract: "a tripartite syntax: prefix (identity/commodity/office),
  medial (action/transaction/domain), and suffix
  (cycle/jurisdiction/logistics)", claimed stable across Harappa,
  Mohenjo-daro, Lothal, Kalibangan, Dholavira. The 24-cluster atlas
  (manual_005) is Supplement B: "24 semantic clusters (faunal,
  botanical, celestial, hydrological, governance, ritual,
  agricultural, craft, trade, etc.)", each with canonical forms,
  co-occurrence sets, syntax roles (prefix/medial/suffix) and
  confidence ratings — all FULL TEXT from the in-worktree document.

### 1.3 The Wells dossier

- **FULL TEXT + Crossref-verified metadata** —
  `the_archaeology_and_epigraphy_of_indus_w_27f45a68` is Bryan K.
  Wells (with Andreas Fuls), *The Archaeology and Epigraphy of Indus
  Writing*, Archaeopress Publishing Ltd, 2015, DOI
  10.2307/j.ctvr43jmf (JSTOR). Chapters verified by Crossref:
  Ch. 2 "The Indus Sign List" (.10), Ch. 3 "Patterns of Sign Use and
  the Syntactic Structure of Indus Texts" (.11), Ch. 6
  "Proto-Dravidian and the Indus Script" (.14), Appendix II Fuls
  (.16). The book builds on Wells' 2006 Harvard dissertation
  (*Epigraphic Approaches to Indus Writing*), whose sign list (676,
  later 695 signs) is the numbering the book — and Fuls' ICIT —
  use. The book is paywalled commercially, but the audit holds the
  full text in-worktree, so all Wells items below are FULL TEXT.

---

## 2. Challenge pass: is a three-part positional grammar prior art? (task 4)

**Answer: yes — the three-part positional structure of Indus
inscriptions was published, in those terms, well before Hunt's
September 2025 draft. The semantic relabelling
(identity/action/cycle) is Hunt's; the three-slot positional frame is
not.**

1. **Wells: Patterned texts consist of three fields — Initial,
   Medial, Terminal (FULL TEXT).** Wells 2015, Ch. 3, pp. 24–25:
   "Patterned texts consist of three fields (Initial, Medial and
   Terminal)… What all Patterned texts share is that their signs are
   arranged in three fields." The whole typology is built on the
   three slots: Segment texts "consist of one of the three syntactic
   elements identifiable in Patterned texts", Partial Patterned texts
   of two of the three. Wells cites his own earlier statement of the
   formulaic structure ("Wells 2011"; the framework goes back to his
   2006 dissertation). This is a published prefix/middle/suffix
   inscription structure in everything but Hunt's semantic labels.
2. **Sinha, Ashraf, Pan & Wells 2010 (FULL TEXT, arXiv
   1005.4997):** network analysis segmenting inscriptions into an
   "initial phrase", a "medial sequence" and a "terminal phrase"
   (worked example M-0355), with explicit lists of "beginner" signs
   (in-degree 0) and "ender" signs (out-degree 0), and segmentation
   trees presented as evidence of syntactic organisation. Journal
   version: *Pramana*? — no: published version is the 2009 ACL/IJCNLP
   workshop paper "Network analysis reveals structure indicative of
   syntax in the corpus of undeciphered Indus civilization
   inscriptions" (Sinha, Pan, Yadav, Vahia, Mahadevan), DOI
   10.3115/1708124.1708128 (Crossref/federation record, at abstract
   level). Wells is a co-author of the arXiv version.
3. **Yadav, Joglekar, Rao, Vahia, Mahadevan & Adhikari 2009 (FULL
   TEXT, arXiv 0901.3017; published in *PLoS ONE* 5(3): e9506, 2010 —
   publication venue at abstract level):** n-gram Markov analysis
   finding "specific text beginner and text ender signs",
   directionality, and "groups of signs which appear to have the
   same syntactic function"; ~82 beginner signs cover 80% of text
   beginnings but only ~23 enders cover 80% of endings. The paper
   itself notes the beginner/ender asymmetry "is consistent with
   previous analysis by Mahadevan for M77 corpus" — i.e. the
   positional asymmetry was already in Mahadevan's 1977 concordance
   data (attribution FULL TEXT in Yadav; Mahadevan's own text not
   read — gap, §5).
4. **Fuls 2013 / 2015 / 2023 (FULL TEXT, §1.1):** the
   initial/medial/terminal scheme refined into seven positional
   classes with a published method and per-sign classifications —
   the direct methodological ancestor of any positional-grammar
   claim, and the source of three of this audit's stub claims.
5. **Rao, Yadav, Vahia, Joglekar, Adhikari & Mahadevan 2009 (metadata
   verified, Crossref):** "A Markov model of the Indus script",
   *PNAS*, DOI 10.1073/pnas.0906237106 (2009-08-18); and Rao et al.
   2009, "Entropic Evidence for Linguistic Structure in the Indus
   Script", *Science*, DOI 10.1126/science.1170391 (2009-05-29) —
   sign-order structure modelled statistically a decade and a half
   before Hunt. At abstract level for content; neither claims a
   three-slot grammar, but both establish that positional/sequential
   structure was the field's standard object of study.
6. **Kondratov 1976 (Crossref metadata verified; content at abstract
   level — full text paywalled, gap §5):** A. M. Kondratov, "The
   Positional-Statistical Analysis of the Proto-Indian Texts", in
   the Knorozov-school volume, DOI 10.1515/9783110800258.39 (1976).
   The Soviet positional-statistical programme classified
   proto-Indian signs by text position in the 1960s–70s — the
   deepest prior art for positional classification as such.
7. **Korvink 2011 (bibliographic record only — at abstract level):**
   M. Korvink, *The Indus Script: A Positional-Statistical Approach*
   (2011), surfaced via the search_papers federation's Google Scholar
   records. A book-length positional-statistical treatment; full text
   not retrieved (gap §5).
8. **Mahadevan's positional observations (attribution FULL TEXT in
   Fuls and Yadav; Mahadevan's own texts not read — gap §5):**
   initial/terminal sign recognition is credited to Mahadevan 1977
   (*The Indus Script: Texts, Concordance and Tables*, ASI) by both
   Fuls (Appendix II) and Wells (Ch. 3 and sign-list discussion).
   Wells' sign list comparison (FULL TEXT) also records that
   Mahadevan's list is a reduced 387–419-sign list that "lumps"
   graphic variants — relevant to §3 below.

**Priority conclusion (FULL TEXT basis):** a three-part positional
grammar of Indus inscriptions — initial/medial/terminal fields with
position-defined sign classes — is prior art, published by Wells
(2006 diss.; 2011; book 2015), operationalised statistically by
Yadav et al. (2009), Sinha et al. (2009/2010) and Fuls (2013/2015/
2023), with roots in Mahadevan (1977) and the Knorozov school
(1960s–76). What is original to Hunt (2025) is only the *semantic*
assignment of the three slots (identity/office/commodity;
action/transaction/domain; cycle/jurisdiction/logistics) and the
civic-ritual interpretation built on it. Notably, the preprint's
own dossier record for manual_001 already concedes the positional
half is what was tested ("consistent with…" verdict, Phase-43);
the literature shows even that half was not new.

---

## 3. Sign readings 821 and 297 (task 5)

Numbering warning (FULL TEXT): sign numbers are list-specific.
Mahadevan's list has 419 signs (387 in Wells' count of it) and
Parpola's 386, so **no sign 821 exists in Mahadevan or Parpola**;
numbers in the 800s belong to the Wells (2006) list as extended in
Fuls' ICIT, which is the numbering Wells 2015 and Fuls 2023 both use.
A "sign 297" in Mahadevan's list is not thereby the same glyph as
Wells' 297; cross-list identity needs the graphic crosswalk, which
was not performed — gap §5.

### Sign 821 (Wells sign_val_0001: "used in a variety of contexts")

- **FULL TEXT (Wells 2015, Ch. 6, p. 93):** the claim's quote is
  Wells verbatim: "Whatever sign 821 reads it is used in a variety
  of contexts (Figure 6.13)." In context, Wells *suggests* (his
  word) that in the Dholavira signboard contexts 821 means 'city'
  (proto-Dravidian *eyil* 'fortress, wall, city' preferred; DEDR
  752 *ūr*, 808 *eyil*, 3568 *nakar*, 4112 *pāri* all listed), while
  explicitly noting "we really do not have a firm reading for sign
  821". The dossier claim keeps only the "variety of contexts"
  fragment; the tentative 'city' reading it attaches to is Wells'
  own suggestion, presented by him as unverified.
- **FULL TEXT (Fuls, Appendix II, pp. 128–129):** sign 821 is the
  *doubled form* of sign 820. Sign 820 is "typically in the initial
  position" (cf. Fuls 2023 §3.15 "Comparison of Sign 820 and Sign
  821", and Fig. 3.26: initial cluster 002-820 on seal M-1088);
  "the doubled sign 821 is still often initial, but also frequently
  in late medial or terminal position" — i.e. the published
  positional record supports "variety of contexts" positionally:
  doubling broadens 820's initial-only profile across all three
  zones. Wells' Ch. 6 distribution discussion agrees (821 replaced
  by 002 in some medial contexts; signboard-final behaviour of
  neighbours discussed).
- **Verdict on the match:** Wells' characterisation matches the
  published positional record (Fuls) — FULL TEXT both sides. No
  independent sign list contradicts it; Mahadevan/Parpola lists
  cannot speak to "821" at all (numbering, above).

### Sign 297 (Wells sign_val_0002: "the horned tiger")

- **FULL TEXT (Wells 2015, Ch. 6, p. 97):** the claim's quote is
  Wells verbatim and hedged in the original: on seal M-1919, "sign
  532 and sign 297 are positioned in such a way as to resemble the
  position of the graphic element… it is proposed here that sign
  532 is a logograph for the anthropomorphic figure and that sign
  297 represents the horned tiger, or perhaps just 'tiger'
  generically." It is an iconographic-correspondence *proposal*,
  not a sign-list identification: the argument is that the sign's
  placement beside the tablet's image field mirrors the depicted
  horned tiger.
- **Published lists:** Fuls 2023's catalog (SearchInside text held
  in-worktree) contains no "tiger" discussion of 297 in the portions
  present, and the catalog's per-sign entries for 297 were not in
  the extracted preview text — **gap**: whether Fuls' catalog entry
  for sign 297 describes a tiger-like glyph could not be checked
  from the held text (the full catalog is a paid print book).
  Mahadevan/Parpola 297 cannot be equated without a graphic
  crosswalk (numbering warning above) — **gap**.
- **Verdict on the match:** the claim faithfully reproduces Wells'
  own hedged proposal (FULL TEXT). No published list retrieved in
  this audit independently confirms or contradicts "297 = horned
  tiger"; it stands as Wells' proposal only.

---

## 4. Per-claim findings

Stage-record summaries (record path, sources that answered, closest
neighbours the stage returned) are appended in §6 once the serial
stage batch finished; the judgements below rest on the challenge
pass and full-text reads above.

- **manual_001 (tripartite grammar; partially_supported).** The
  positional skeleton (three fields; position-defined sign classes)
  is prior art: Wells 2015 Ch. 3 FULL TEXT (§2.1), with Yadav 2009,
  Sinha et al. 2010 and Fuls 2013 FULL TEXT behind it. Hunt's
  semantic slot-labels are the only novel element, and they are the
  element the dossier record itself says was never tested.
- **manual_003 (faunal signs as initial prefixes;
  partially_supported).** Neighbours: Fuls' initial-sign class and
  Wells' Initial field are position-defined, not faunal-defined —
  no retrieved work (FULL TEXT: Fuls 2013/2015/2023; Wells 2015)
  classifies the initial-position signs as animal signs, and Fuls
  is explicit that positional groups share syntactic position, not
  meaning. The faunal characterisation has no published support in
  what was read; the positional half is prior art per §2. Hunt's
  own text (FULL TEXT) asserts faunal triads (fish, bull, unicorn)
  in prefix position as her finding, without a sign-classification
  crosswalk — the same gap the dossier's not_understood records.
- **manual_004 (celestial signs as terminal markers; untested).**
  Same structure as manual_003: terminal classes are published
  (Fuls TMK class; Wells Terminal field; Yadav enders — FULL TEXT),
  but no read work identifies the terminal class as *celestial*.
  Mahadevan's terminal-sign observations are the natural neighbour;
  his own text is a gap (§5), so this item's neighbour statement is
  at abstract level beyond the Fuls/Yadav attributions.
- **manual_002 (civic-ritual continuity system; untested).** This is
  Hunt's interpretive frame (FULL TEXT, her abstract). Its
  literature neighbourhood is the linguistic-vs-non-linguistic
  debate: Farmer, Sproat & Witzel 2004 (the dossier's own
  language_0001 restates their thesis and is marked contradicted by
  carry-over) against Rao et al. 2009 *Science*/*PNAS* (metadata
  verified; content at abstract level). Nothing retrieved tests —
  or could test, from sign statistics — the civic-ritual social
  reading; it remains an interpretation layered on the positional
  frame.
- **manual_005 (24-cluster Translation Atlas; untested).** The
  atlas exists as Hunt's Supplement B (FULL TEXT, §1.2) — a
  self-published supplement, unindexed. Published sign
  classifications differ in kind: Fuls' positional classes (7),
  Wells' sign list (676–695 signs), Mahadevan (419), Parpola (386).
  No published 24-cluster semantic atlas was found; the claim's
  object is Hunt's own supplement, so "prior art" is not the issue
  — independent existence/verification is: the atlas's cluster
  definitions are not in any indexed source retrieved.
- **statisti_0002 / positional statisti_0001 / Wells statisti_0003
  (the three "Positional Analysis" stubs).** All three are section
  titles, not findings, and all three point at the same work:
  Fuls' positional analysis (§1.1) — as the 2013 *Voprosi
  Epigrafiki* article, as Wells 2015 Appendix II, and as Fuls 2023
  Catalog Ch. 3. Grounded in the source author's actual content,
  the finding the stub stands for is: *signs can be classified by
  normalised weighted positional histograms into Initial,
  Early-Medial, Mid-Medial, Late-Medial, Terminal, Post-Terminal
  and constant classes, and the classes separate allographs from
  distinct signs* (FULL TEXT). All three stubs are already merged
  into `ancient_writing…statisti_0004`, consistently with this
  identification.
- **fuls2023 statisti_0001.** Stage record already existed
  (coordinator smoke run, 2026-10-22T14:26Z); per instructions only
  challenge + source identification done: the source is Fuls 2023
  *A Catalog of Indus Signs* (§1.1); its Ch. 3 is the positional
  analysis (§1.1, FULL TEXT). Note the smoke record's neighbours
  are keyword false-positives (machine-tool tolerancing papers) —
  the stub phrasing retrieves nothing relevant without the alt
  phrasing, which is the protocol's phrasing-sensitivity trap in
  action.

---

## 5. Open gaps

1. **Mahadevan 1977** (*The Indus Script: Texts, Concordance and
   Tables*) — not open-access; his terminal-sign and positional
   observations are known here only through FULL-TEXT attributions
   in Fuls, Wells and Yadav. Recorded as a gap, not as absence.
2. **Kondratov 1976** full text (De Gruyter) — paywalled; metadata
   Crossref-verified, content at abstract level.
3. **Korvink 2011**, *The Indus Script: A Positional-Statistical
   Approach* — bibliographic record only (Google Scholar via the
   federation); no OA full text retrieved.
4. **Fuls 2023 catalog per-sign entries** (incl. sign 297's entry
   and §3.15's full 820/821 comparison) — the held SearchInside
   text is partial (front matter, Ch. 3 in part, occurrence lists);
   the print book is paywalled.
5. **Cross-list graphic crosswalk** for sign 297 (Wells no. vs
   Mahadevan/Parpola nos.) — not performed; number-only comparison
   would be invalid.
6. **OpenAlex and Semantic Scholar unproductive this session**
   (empty responses throughout, incl. a control query); BASE not
   attempted (expected empty per protocol doc); Zenodo tool
   errored. Novelty statements above therefore rest on arXiv +
   Crossref + CORE + the federation, plus the in-worktree full
   texts — which include the two load-bearing books (Wells 2015;
   Fuls 2023 partial) and Fuls 2013 in full.
7. **Hunt 2025** has no indexed record in any working source; if it
   was posted to a repository (e.g. ResearchGate/OSF), that posting
   was not reachable — the identification is from the document
   itself.

## 6. Stage records (RESEARCH-CHECK)

All ten assigned stage runs completed 2026-10-22 (14:33–15:10 UTC,
serial, script + log: `W4_stage_runs.sh`, `W4_stage_runs.log`,
per-run logs `W4_stage_*.log`). Sidecars are in
`glossa-indus/claims/research_checks/` under the standard
`<document>__<claim>.research_check.json` names; every record has
`verdict: null` as designed. Six queries per record (claim phrasing,
mechanical variant, and the stranger alt-phrasing grounded in §1)
across arxiv/crossref/openalex/semantic/core/europepmc.

Honest limitation, consistent with the coordinator's fuls2023 smoke
record: **the stage's automated neighbour ranking returned mostly
keyword false-positives for this line** (machine-tool tolerancing,
fMRI statistics, celestial mechanics; relevance 0.11–0.75 driven by
the stub phrasings "Statistical finding: Positional Analysis" and
"Sign value: …"). Two records logged a `read_arxiv_paper`
ExceptionGroup error and fell into the protocol's documented arXiv
trap (an ATLAS detector paper surfaced as a "neighbour" for
sign_val_0001). sign_val_0002 surfaced zero neighbours — the record
itself flags this as "a search outcome, not evidence of no prior
art". No stage record read a true neighbour in full text. The
load-bearing neighbour identification and full-text reads for this
line are therefore the manual challenge pass in §§2–3 (Yadav 2009,
Sinha et al. 2010 read in full via the same client; Fuls 2013/2015/
2023 and Wells 2015 read in full from the in-worktree texts), which
is the protocol's intended division of labour: the stage is
advisory, the audit supplies the judgement.

Per-record notes:

| Claim | Checked (UTC) | Stage outcome |
|---|---|---|
| manual_001 | 14:33 | 16 neighbours, all keyword-level; top hit (Mukhopadhyay, "Semantic scope of Indus inscriptions…") is a genuine field neighbour at abstract level, not read by the stage |
| manual_003 | 14:34 | neighbours are affix-position linguistics + noise; no faunal-positional work surfaced |
| manual_004 | 14:37 | one intriguing hit, "Chapter Nine: Terminal Signs" (Crossref), unidentified by the stage; rest noise |
| manual_002 | 14:41 | noise (incl. the Wells-book chapter "The Buddhist Indus Script") |
| manual_005 | 14:44 | noise; one full-text read error logged |
| statisti_0002 (Hunt doc) | 14:51 | identical tolerancing/fMRI false-positive set as the other stubs |
| statisti_0001 (Fuls 2013 doc) | 14:53 | same false-positive set |
| statisti_0003 (Wells doc) | 14:55 | same false-positive set |
| sign_val_0001 | 14:56 | 20 neighbours, all noise; ATLAS-trap gap logged by the stage itself |
| sign_val_0002 | 15:03 | 0 neighbours; record self-flags the gap |

The fuls2023 statisti_0001 record (coordinator smoke run,
2026-10-22T14:26Z) was not re-run, per instructions.
