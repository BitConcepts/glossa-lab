# W6 — Citation verification findings (Material Audit 2026-10-22)

Worker: W6 (citations). Protocol: `docs/paper-search-mcp.md` (rule 4: verify
metadata independently; a search snippet is never a citation — only resolved
metadata records count). All 23 entries of §8 References of
`glossa-corpus/indus/pierson_2026_indus_decipherment.tex` were extracted from
the .tex as printed and checked field by field.

## Sources queried and their status this session

| Source | Status |
|---|---|
| Crossref (`search_crossref`, `get_crossref_paper_by_doi`) | WORKED — primary source |
| arXiv (`search_arxiv`, `read_arxiv_paper`) | WORKED — Nair record + full text |
| OpenAIRE (`search_openaire`) | WORKED — resolved EJVS items |
| OpenAlex (`search_openalex`) | **429 on first call — source closed for the session** (per protocol; key was supplied, quota still exhausted) |
| Semantic Scholar (`search_semantic`) | **429 after retries on every call — source closed for the session** (no S2 key configured) |
| CORE (`search_core`) | **Timed out on all 3 attempts × 8 calls — source unusable this session** |
| BASE (`search_base`) | Empty (expected per protocol doc) |
| HAL (`search_hal`) | Empty |
| Zenodo (`search_zenodo`) | Tool error (`'str' object has no attribute 'isoformat'`) |

Raw responses: `W6_*.json` in this directory (plus `.err` logs). Nair full
text: `W6_nair_fulltext.txt` (extracted by `read_arxiv_paper`) and
`W6_nair_2604.17828.pdf`.

Evidence-level labels used below: **FULL TEXT** = the work itself was read;
**metadata level** = a resolved metadata record (Crossref/OpenAIRE/arXiv)
was checked; **at abstract level** = only an abstract was available.

---

## 1. Per-entry verification table (§8 References, 23 entries)

| # | Entry as printed | Resolved metadata | Verdict per field |
|---|---|---|---|
| 1 | Burrow, T. & Emeneau, M.B. (1984). *A Dravidian Etymological Dictionary* (2nd ed.). Oxford: Clarendon Press. [DEDR] | Crossref review record (J. C. Wright, JRAS 1984, DOI 10.1017/s0035869x0016383x): "A Dravidian Etymological Dictionary. By T. Burrow and M. B. Emeneau. pp. xli, 853. Second edition. Oxford, Clarendon Press" | Title MATCH · Authors MATCH · Edition (2nd) MATCH · Publisher MATCH · Year 1984 MATCH (metadata level, via contemporary review record) |
| 2 | Crawford, H. (2001). *Early Dilmun Seals from Saar*. Archaeology International. | Crossref records show *Early Dilmun Seals from Saar: Art and Commerce in Bronze Age Bahrain* is a **monograph** by Harriet Crawford (reviewed AJA 2003, DOI 10.1086/ajs40025410; JNES 2002, DOI 10.2307/3087532). *Archaeology International* is a journal in which Crawford published a different piece ("Dilmun revisited: excavations at Saar, Bahrain", 1997, DOI 10.5334/ai.0111) | Title MATCH (subtitle dropped) · Author MATCH · **Venue/type MISMATCH** — book title cited as a journal article in *Archaeology International*; no volume/pages printed or resolvable · Year 2001 consistent with the book, not independently resolved |
| 3 | Farmer, S., Sproat, R. & Witzel, M. (2004). The Collapse of the Indus-Script Thesis. *Electronic Journal of Vedic Studies*, 11(2), 19–57. | OpenAIRE record: "The Collapse of the Indus-Script Thesis: The Myth of a Literate Harappan Civilization" with abstract. EJVS 11(2), 19–57 corroborated identically by the reference list of Nair 2026 (FULL TEXT read, ref [2]) | Title MATCH (subtitle omitted in preprint) · Authors MATCH · Venue/vol/pages/year MATCH (metadata level, two independent records) |
| 4 | Hojlund, F. & Abu-Laban, A. (2012). *Tell F6 on Failaka Island: Kuwaiti-Danish Excavations 2008–2012*. Jutland Archaeological Society. | No record resolved. Crossref returned only the later *Tell F3* volume (2022, DOI 10.2307/j.ctv33jb55h); CORE timed out; OpenAlex/S2 closed (429) | **NOT RESOLVED — open gap.** No field verified; nothing asserted either way |
| 5 | Lubotsky, A. (2001). The Indo-Iranian substratum. In C. Carpelan et al. (eds.), *Early Contacts between Uralic and Indo-European*. Helsinki: Suomalais-Ugrilainen Seura. | Crossref resolved the container volume: *Early Contacts between Uralic and Indo-European*, Suomalais-Ugrilainen Seura, 2001 (DOI 10.33341/sus.1242). Chapter-level record not in results | Container title/publisher/year MATCH · Chapter title/author NOT individually resolved — partial, metadata level |
| 6 | Mahadevan, I. (1977). *The Indus Script: Texts, Concordance and Tables*. New Delhi: Archaeological Survey of India. | No Crossref book record (ASI memoirs are not Crossref-indexed). Corroborated at metadata level by Nair 2026's reference list (FULL TEXT): "Mahadevan, I. (1977). The Indus Script: Texts, Concordance and Tables. Memoirs of the Archaeological Survey of India, No. 77" | Title MATCH · Author MATCH · Year MATCH · Publisher MATCH (ASI, Memoirs No. 77) — metadata level |
| 7 | McAlpin, D.W. (1981). *Proto-Elamo-Dravidian: The Evidence and Its Implications*. Philadelphia: American Philosophical Society. | Crossref: book record DOI 10.70249/9798893981803 (1981) and JSTOR record DOI 10.2307/1006352, David W. McAlpin, 1981 | Title MATCH · Author MATCH · Year MATCH · Publisher MATCH (metadata level) |
| 8 | Miller, W. (2025). Holdat LLC Indus Corpus v3. Dataset. Not publicly released at time of writing. | No public record exists: Crossref search for the corpus returned no Holdat/Miller record; Zenodo tool errored | **UNVERIFIABLE by design** — see §4 reliance map. The entry is honestly labelled in the preprint itself |
| 9 | Parpola, A. (1994). *Deciphering the Indus Script*. Cambridge: Cambridge University Press. | Four independent Crossref review records (JSTOR 10.2307/416809; JRAS 10.1017/s1356186300006829; AA 10.1525/aa.1996.98.1.02a00470; BSOAS 10.1017/s0041977x00031980) all: Asko Parpola, *Deciphering the Indus Script*, CUP, 1994, xxii + 374 pp | All fields MATCH (metadata level) |
| 10 | Parpola, A. (2010). A Dravidian solution to the Indus script problem. *World Archaeology*, 42(2), 178–193. | **Not resolved.** Three Crossref searches returned only Parpola's 1986 *World Archaeology* article (DOI 10.1080/00438243.1986.9979979, 17(3):399–419); a candidate DOI lookup (10.1080/00438241003605324) returned an empty record; OpenAIRE empty; OpenAlex/S2 closed | **NOT RESOLVED — open gap.** No field verified this session; nothing asserted either way |
| 11 | Nair, A. (2026). How Non-Linguistic Is the Indus Sign System? A Synthetic-Baseline Scorecard. arXiv:2604.17828. | arXiv record 2604.17828v1 resolved; FULL TEXT read — see §2 | Title MATCH · Author MATCH (Ashish Nair) · arXiv ID MATCH · Year (April 2026) MATCH |
| 12 | Rao, R.P.N. et al. (2009). A Markov model of the Indus Script. *PNAS*, 106(33), 13685–13690. | Crossref DOI record 10.1073/pnas.0906237106: Rao, Yadav, Vahia, Joglekar, Adhikari, Mahadevan; PNAS 106(33):13685–13690, 2009 | All fields MATCH (metadata level, DOI record) |
| 13 | Southworth, F. (2005). *Linguistic Archaeology of South Asia*. London: Routledge. | Crossref book record DOI 10.4324/9780203412916, Franklin Southworth, Routledge; e-book record dated 2004-08-02 | Title/author/publisher MATCH · Year: print edition 2005 as cited; Crossref's electronic record is dated 2004 — minor edition-date nuance, not a mismatch |
| 14 | Krishnamurti, Bh. (2003). *The Dravidian Languages*. Cambridge: Cambridge University Press. | Crossref DOI 10.1017/cbo9780511486876: Bhadriraju Krishnamurti, *The Dravidian Languages*, CUP, 2003-01-16 | All fields MATCH (metadata level) |
| 15 | Laursen, S. (2010). The Westward Transmission of Indus Valley Sealing Technology. *Arabian Archaeology and Epigraphy*, 21, 96–134. | Crossref DOI record 10.1111/j.1600-0471.2010.00329.x: Steffen Terp Laursen; AAE 21(2):96–134, 2010; full title continues "…: origin and development of the 'Gulf Type' seal and other administrative technologies in Early Dilmun, c.2100–2000 BC" | Venue/volume/pages/year MATCH · Title in preprint is a **shortened form** of the published title (subtitle dropped) · Issue (2) not printed in preprint, record confirms it |
| 16 | Wells, B. (2011). *The Archaeology and Epigraphy of Indus Writing*. Oxford: Archaeopress. | Crossref/JSTOR monograph record DOI 10.2307/j.ctvr43jmf: **Bryan K. Wells & Andreas Fuls**, *The Archaeology and Epigraphy of Indus Writing*, **Archaeopress Publishing Ltd, 2015-02-06**, ISBN 9781784910471 / 9781784910464 | **Year MISMATCH: 2015, not 2011** · **Author MISMATCH: co-author Andreas Fuls omitted** · Title MATCH · Publisher MATCH (Archaeopress). The preprint's own §3.20/§3.24 cite the same book as "Wells (2015)" — §8 contradicts the preprint's body text |
| 17 | Witzel, M. (1999). Substrate Languages in Old Indo-Aryan. *Electronic Journal of Vedic Studies*, 5(1), 1–67. | OpenAIRE/Heidelberg record DOI 10.11588/ejvs.1999.1.828: "Substrate Languages in Old Indo-Aryan (Ṛgvedic, Middle and Late Vedic)", abstract field: "Electronic Journal of Vedic Studies, Bd. 5 Nr. 1 (1999)" | Title MATCH · Author MATCH · Venue/vol/issue/year MATCH (5(1), 1999) · Pages 1–67 not present in the resolved record — unverified field (metadata level) |
| 18 | Kjaerum, P. (1983). *Failaka/Dilmun: The Second Millennium Settlements, Vol. 1: The Stamp and Cylinder Seals*. Aarhus: Jutland Archaeological Society. | Crossref resolved the series record (JSTOR j.ctv33jb493, *Danish Archaeological Investigations on Failaka, Kuwait — Failaka/Dilmun: The Second Millennium Settlements*, JAS reissue) | Series title/publisher MATCH at series level · The 1983 seals volume itself not individually resolved — partial, metadata level |
| 19 | Mitchell, T.C. (1986). Indus and other seals from the Gulf. In Al-Khalifa & Rice (Eds.), *Bahrain Through the Ages: The Archaeology*. London: Kegan Paul International, pp. 278–282. | No record resolved in Crossref (results were unrelated chapters of other Gulf volumes); other sources closed/unusable | **NOT RESOLVED — open gap.** Chapter, editors, and pages unverified this session |
| 20 | Parpola, A., Parpola, S. & Brunswig, R.H. (1975). The Meluḫḫa village: evidence of acculturation of Harappan traders in late third-millennium Mesopotamia? *Journal of the Economic and Social History of the Orient*, 18(2), 129–165. | Crossref DOI record 10.2307/3631775 (JSTOR): "The Meluhha Village: Evidence of Acculturation of Harappan Traders in Late Third Millennium Mesopotamia?", **Simo Parpola; Asko Parpola; Robert H. Brunswig**, JESHO **volume 20, issue 2, page 129–**, **published 1977-05-01** | Title MATCH · Journal MATCH · Start page 129 MATCH · **Year MISMATCH: 1977, not 1975** · **Volume MISMATCH: 20, not 18** · **Author order MISMATCH: Simo Parpola is first author in the record; preprint lists A. Parpola first** · End page (165) unverified (record gives start page only) |
| 21 | Potts, D.T. (1994). South and Central Asian elements at Tell Abraq (Emirate of Umm al-Qaiwain, UAE), c. 2200–1000 BC. In Parpola & Koskikallio (Eds.), *South Asian Archaeology 1993*. Helsinki: Suomalainen Tiedeakatemia, pp. 615–628. | Crossref corroborates the proceedings volume exists (*South Asian Archaeology 1993*, Helsinki, published 1994; cf. PIA record DOI 10.5334/pia.56). Chapter-level record not resolved | Container/year/editors plausible and partially corroborated · Chapter title/pages NOT individually resolved — partial, metadata level |
| 22 | Reade, J.E. (2001). Assyrian king-lists, the royal tombs of Ur, and Indus origins. *Journal of Near Eastern Studies*, 60(1), 1–29. | Crossref DOI record 10.1086/468883: Julian Reade, JNES 60(1):1–29, 2001 | All fields MATCH (metadata level, DOI record) |
| 23 | Steinkeller, P. (1982). On the identity of the toponym LÚ.SU(.A). *Journal of the American Oriental Society*, 102(2), 299–309. | The only same-title record resolved is a **different item**: Crossref DOI 10.2307/603646 = JAOS **108(2):197, 1988**, same title/author. The cited JAOS 102(2):299–309 (1982) article was not resolved in any reachable source | **NOT RESOLVED as cited — open gap, flagged.** Either the preprint's year/volume/pages are wrong or the 1982 article lacks a Crossref/JSTOR record under this title; this session's evidence cannot distinguish. Do not cite the 1988 record as confirmation |

### Additional finding — in-text citations with no §8 entry
The body text relies on works that never appear in §8 References:
Mahadevan (1982) *Terminal Ideograms in the Indus Script* and Mahadevan
(1986) *Towards a Grammar of the Indus Texts* (§3.21); Mahadevan's "Place
Signs" (1981), "What Do We Know" (1989), and the akam–puram paper (2011)
(§3.23); and the aggregate claims "10 Mahadevan papers (1972–2018)"
(§1.3/§3.23) and "38 Mahadevan papers (1970–2018)" (§3.24). None is in §8.
§3.20/§3.24 cite "Wells (2015)" while §8 lists only "Wells (2011)" — the
same book (see #16), so one of the two year forms in the preprint is wrong;
the resolved record says 2015.

---

## 2. Nair 2026 — full-text report (FULL TEXT, `read_arxiv_paper`)

**Record verification.** arXiv:2604.17828v1 exists exactly as cited: Ashish
Nair, "How Non-Linguistic Is the Indus Sign System? A Synthetic-Baseline
Scorecard", April 2026, Independent Researcher. The preprint's citation
metadata is accurate.

**What Nair actually concludes** (from the full text, not the abstract
alone):
- Method: a four-metric "scorecard" (text brevity, repeated formulaic
  phrases, hapax legomenon rate, positional rigidity — the four
  Farmer–Sproat–Witzel 2004 objections) comparing the ICIT/Yajnadevam
  corpus against two *synthetic non-linguistic generators* (heraldic,
  administrative) plus seven attested non-linguistic corpora.
- Corpus: 1,916 deduplicated inscriptions, 584 unique signs (G### codes),
  11,110 tokens, 52 sites; 595 exact duplicates (24%) removed.
- Headline result (Abstract + §6 + §8, stated three times): the Indus
  corpus "**occupies an intermediate position relative to the two
  baseline families, matching neither cleanly**"; it discriminates from
  the heraldic baseline on all metrics and from the administrative
  baseline on **only two of four** metrics. "This does not settle the
  linguistic question. A more carefully tuned non-linguistic model might
  eventually match the full Indus profile."
- Replication component: Zipf slope −1.492 (R²=0.956), conditional
  entropy 3.232 bits, within-inscription permutation null percentile
  0.000 (n=1,000) — presented as replicating Mahadevan 1977 / Rao et al.
  2009 descriptive results, with Sproat's caveat quoted: non-random
  ordering "does not by itself prove the symbols encode language".
- Nair's paper contains **no decipherment, no positional grammar, no
  Dravidian hypothesis, and no reference to Pierson's work**. Its sign
  coding (G###) is explicitly *not* cross-validated against Mahadevan
  M### or Parpola P### ("No fully validated cross-concordance exists").

**Accuracy of the preprint's characterizations** (§3.10 and Acknowledgments;
§3.10 quoted verbatim from the .tex):

1. *"Applying a multi-metric discrimination framework to 1,916
   deduplicated ICIT inscriptions (584 unique signs, 11,110 tokens)"* —
   **ACCURATE** (matches Nair's abstract verbatim figures).
2. *"Nair reports Zipf slope −1.49, conditional entropy 3.23 bits, and
   permutation null percentile 0.000 against 1,000 permutation trials"* —
   **ACCURATE** (Nair: −1.492, 3.232 bits, percentile 0.000, n=1,000).
3. *"This is an independent corpus (G-prefix ICIT coding) with an
   independent methodology, replicating the key structural result of our
   Phase-134 F1 test (z = 10.3; 0/2000 permutations…) on an entirely
   separate dataset"* — **OVERSTATED.** Nair's permutation test is a
   within-inscription shuffle null on conditional entropy — a different
   statistic from the preprint's positional test; Nair frames his
   replication as being of Mahadevan/Rao results, not of any Pierson
   test. The corpora are separate *digitizations* (ICIT/Yajnadevam
   G-codes vs Holdat M-codes) but of substantially the **same underlying
   published inscription assemblage**, so "entirely separate dataset"
   overstates the independence.
4. *"The two independent analyses … provide strong converging evidence
   for non-random sequential structure of the Indus sign system"* —
   **DIRECTIONALLY CONSISTENT BUT STRONGER THAN THE SOURCE.** Nair does
   establish non-random sequential structure, but his stated conclusion
   is the hedged "intermediate position… matching neither cleanly" plus
   "does not settle the linguistic question"; the preprint omits the
   intermediate/2-of-4 result and both of Nair's caveats. Nothing in
   Nair bears on the preprint's three-slot grammar, its 161 anchors, or
   any Dravidian reading.
5. Acknowledgments: *"Ashish Nair for the independent replication
   study"* — **MISLEADING LABEL.** Nair's paper is an independent
   scorecard study of the FSW critique; it does not describe itself as a
   replication of this preprint's work.
6. Related internal artifact (outside the preprint): the dossier's
   "Nair (2026) scorecard: 4/4 linguistic-consistent metrics"
   (DECIPHERMENT_DOSSIER_v1.md) is **not supported by the full text** —
   Nair's scorecard is 4 metrics on which Indus *discriminates from the
   heraldic baseline*, matches the administrative baseline on 2 of 4,
   and is nowhere scored "4/4 linguistic-consistent".

**Nair verdict:** citation metadata exact; all three quoted statistics
exact; the interpretive framing ("independent replication", "strong
converging evidence") materially overstates a deliberately hedged,
intermediate-result paper, and omits that Nair's framework tests
linguistic-vs-non-linguistic discrimination only — it neither confirms
nor addresses any decipherment claim.

---

## 3. In-text reliance spot checks

### Wells (8 mentions) — metadata level (book closed; no OA full text)
- §1.2: *"Wells (2011) produced an independent sign list and catalogue."*
  The resolved book record (Crossref, DOI 10.2307/j.ctvr43jmf) confirms a
  sign-list chapter exists ("The Indus Sign List", ch. 10 of the JSTOR
  record) — claim directionally correct, but the year is wrong (2015)
  and co-author Andreas Fuls is omitted. **Metadata level.**
- §3.20: *"Mining Wells (2015) The Archaeology and Epigraphy of Indus
  Writing (161 pages): 284 sign references, 96 Dravidian language
  claims, 403-reference positional analysis appendix (Appendix II).
  Wells independently argues proto-Dravidian language and consistent
  sign positional classes."* The in-text year 2015 matches the resolved
  record (contradicting §8's 2011). The mining counts (284 / 96 / 403),
  the "161 pages" figure, and the claims about Wells's argument are
  internal phase outputs / content claims **not checkable at metadata
  level** and no OA full text of the book was reachable — recorded as an
  open gap, not as confirmed or refuted. Nair 2026 (FULL TEXT) cites
  "Wells 2015" for allograph conflation, independently corroborating the
  2015 date and the book's sign-list role. **Metadata level.**
- §3.24: Wells (2015) mined for sign-reading proposals, "0 new direct
  M-number reading assignments" — an internal null result; externally
  unverifiable. **Metadata level.**

### Mahadevan (21 mentions) — metadata level / at abstract level
- §1.2: *"Mahadevan (1977) produced the standard sign concordance and
  M-number catalogue."* Corroborated: the book's title is *Texts,
  Concordance and Tables* (ASI Memoirs No. 77), and the M### coding
  scheme is the one Nair 2026 (FULL TEXT) attributes to "Mahadevan's
  M### (1977)". **Metadata level.**
- §2.1/§3.1/Appendix C: *"397 signs in the Mahadevan catalogue; 390
  attested in the corpus; 7 catalogue-only"* — program-internal counts.
  Published sign counts vary by coding scheme and Nair explicitly warns
  counts are not comparable across schemes; the 397 figure was **not
  independently verifiable** at metadata level. Open gap.
- §3.21/§3.23: claims resting on Mahadevan (1982), (1986), (1981),
  (1989), (2011) and on "10 papers (1972–2018)" / "38 papers
  (1970–2018)" consistency counts — none of these works is in §8, and
  none was resolvable through this session's reachable sources (books/
  journal backfiles; OpenAlex and Semantic Scholar closed). All such
  checks are **metadata level at best and mostly open gaps**; the
  hit-counts (61/8/7/6 "grammar structure agreement hits") are internal
  text-mining outputs, not published quantities.

---

## 4. Miller 2025 (Holdat LLC Indus Corpus v3) — reliance map

**Verifiability status:** the dataset is not publicly released (the
preprint says so in §8, §6, and the AI Disclosure). No public metadata
record for it was found: Crossref search returned no Holdat/Miller
record; no DOI, repository record, or catalogue entry exists to check.
**Every statement below is therefore unverifiable against any
independent record.** No record has been invented for it.

**Where the preprint relies on it** (all corpus-level numbers trace to
Holdat v3 and to nothing else):
- Abstract/§1.3: "Holdat LLC Indus Corpus V3 (1,670 seals, 9 sites, 390
  distinct signs, 7,002 sign tokens; Mahadevan M-numbers)".
- §2.1 (primary corpus definition): 7,002 tokens; 1,670 seals; per-site
  counts — Mohenjo-daro 606, Harappa 492, Kalibangan 110, Dholavira 106,
  Lothal 124, Chanhu-daro 78, Surkotada 61, Banawali 60, Rakhigarhi 33.
- Every downstream corpus statistic: positional test z = 10.3; token
  coverage 90.96%; seal coverage (69.8% fully covered); the 161 H+M
  anchor set; fish-sign 0/113 corpus contexts (0/140 with Gulf);
  Zipf exponent ~1.7; the 18 irresolvable signs' token share (3.8%).
- §2.1 crosswalk (45-entry Mahadevan–Parpola) and §3.10's contrast with
  the public CISI corpus are computed *against* Holdat counts.
- §4.4 Limitations concedes the single-corpus dependence; §6 states
  reproduction requires Holdat access "under agreement" or re-running
  on a public corpus after crosswalking.

In short: the preprint's entire quantitative edifice rests on a dataset
no reader can inspect. The preprint discloses this accurately; the
audit can neither confirm nor refute any Holdat-derived number.

---

## 5. Anchor-dossier reliance (phase128 + DECIPHERMENT_DOSSIER_v1.md)

`reports/phase128_evidence_dossiers_44.json` `sources` are **internal
artifacts**, which themselves rest on:
- `data/crosswalks/wells_segmentation_witness_v1.json` (Wells
  segmentation witness) — rests on **Wells, *An Introduction to Indus
  Writing*, MA thesis, University of Calgary, 1998 (DOI
  10.11575/PRISM/23641)** and **Wells, *Epigraphic Approaches to Indus
  Writing*, PhD thesis, Harvard University, 2006**, cross-matched
  against the "Wells 2015 form of the Wells/ICIT list" (i.e. the 2015
  Wells & Fuls book verified in #16). The thesis DOI was **not
  resolvable via Crossref this session** (empty record) and OpenAIRE
  returned nothing — thesis metadata rests on the program's own file:
  open gap. The 2015 book is fully verified (#16).
- `data/crosswalks/parpola_mahadevan_crosswalk_v1.json`
  (Parpola–Mahadevan crosswalk) — rests on the canonical sign registry
  built from the **mayig CISI digitization** and on Mahadevan 1977
  (verified #6) and Parpola's CISI numbering. CISI itself: Crossref
  review records confirm *Corpus of Indus Seals and Inscriptions, Vol. 1:
  Collections in India*, eds. Joshi & Parpola, Suomalainen
  Tiedeakatemia, 1987 (reviews DOI 10.2307/604450; 10.1086/373580) —
  the dossier's "CISI corpus (Parpola 1987)" is corroborated at
  metadata level. The preprint §3.10's "179 inscriptions, Parpola
  P-numbers, mayig digitization" is consistent with this record.
- DECIPHERMENT_DOSSIER_v1.md additionally rests on: Rao et al. 2009
  (verified #12), Parpola 1994 (verified #9), Nair 2026 (verified #11 —
  but see the "4/4" mischaracterization in §2.6 above), the Yajnadevam
  corpus (2,543 inscriptions — the same digitization Nair used; no
  independent publication record resolved, and none was sought beyond
  Nair's full text, which describes it as "ICIT/Yajnadevam
  digitization"), and the Holdat corpus (unverifiable, §4).

---

## 6. Open gaps (explicit)

1. **OpenAlex and Semantic Scholar were unavailable all session**
   (429). Several book/chapter records (Højlund & Abu-Laban 2012;
   Mitchell 1986; Potts 1994 chapter; Kjaerum 1983 volume; Lubotsky
   2001 chapter; Parpola 2010; Steinkeller 1982 as cited; Wells theses
   1998/2006) could not be resolved and are recorded as gaps, **not**
   as absences or mismatches — except where a resolved record
   positively contradicts the printed entry (#16 Wells, #20
   Parpola et al.).
2. CORE timed out throughout; BASE/HAL returned nothing (BASE expected
   empty from this network per protocol doc).
3. No OA full text was reachable for Wells 2015 or Mahadevan 1977
   (closed books); all Wells/Mahadevan content claims beyond the
   metadata facts noted are checked at metadata level only and labelled
   as such above.
4. Wells (2015) "161 pages" and the Phase-157/158/160 mining counts,
   and the Mahadevan catalogue count of 397 signs, remain unverified.
5. Parpola 2010 (*World Archaeology* 42(2):178–193) is a load-bearing
   citation (§1.2, §2.1 supplementary sources, four-decade framework)
   that this session could not resolve in any reachable source;
   re-check when OpenAlex/S2 quota is available.
