# Findings — Worker W1 (Yadav claims + Rao citation deep check)
Material audit 2026-10-22, under `docs/paper-search-mcp.md` (protocol rules 1–5).
Worker: W1. Date of work: 2026-10-22. No dossier, claim status, or preprint was modified.

## Source papers resolved

| Dossier label | Resolved record |
|---|---|
| Yadav 2009 (arXiv) | Nisha Yadav, Hrishikesh Joglekar, Rajesh P. N. Rao, M. N. Vahia, Iravatham Mahadevan, R. Adhikari, "Statistical analysis of the Indus script using $n$-grams", **arXiv:0901.3017v1** [cs.CL], 20 Jan 2009. Resolved via `search_arxiv` (`raw/W1_arxiv_yadav_ngrams.json`). The arXiv record's DOI field points to the journal version below. |
| Yadav 2010 (journal) | Same author set (order: Yadav, Joglekar, Rao, Vahia, Adhikari, Mahadevan), "Statistical Analysis of the Indus Script Using n-Grams", **PLoS ONE 5(3): e9506, DOI 10.1371/journal.pone.0009506**, published 19 Mar 2010 (received 22 Aug 2009). Resolved via `search_crossref` + `get_crossref_paper_by_doi` (`raw/W1_crossref_yadav_ngrams.json`, `raw/W1_crossref_doi_10.1371_journal.pone.0009506.json`). This is the journal version of the 2009 arXiv n-grams study; the numbers are identical (see per-claim sections). PMID 20333254, PMCID PMC2841631. |

## Full texts actually read by W1 (with extent)

- **Yadav 2009, arXiv:0901.3017v1 — FULL TEXT.** PDF in `glossa-indus/claims/research_checks/full_text/0901.3017v1.pdf`; extracted text (9,468 words) saved as `raw/W1_yadav2009_arxiv0901.3017_fulltext.txt`. Sections read: abstract; §1 introduction (statistical-approach history); §2 corpus (Mahadevan M77 → EBUDS); §2.1 Zipf-Mandelbrot law; §2.2 cumulative distribution incl. text beginners/enders; conditional-probability passages on beginners/enders; Table 9 (major conclusions); references.
- **Yadav 2010, PLoS ONE — FULL TEXT.** PDF saved as `raw/W1_yadav2010_epmc/europepmc_PMID20333254_Statistical_analysis_of_the_Indus_script_using_n-g.pdf` (downloaded via `download_with_fallback`, source europepmc, paper_id PMID:20333254); extracted text (9,451 words) saved as `raw/W1_yadav2010_plosone_fulltext.txt`. Sections read: abstract; Zipf-Mandelbrot passage and Fig. 3 caption; cumulative-distribution / beginner–ender passages (incl. Fig. 4 and Fig. 6 captions).
- **Rao et al. 2009, PNAS (Markov model) — AT ABSTRACT LEVEL only.** Full text could not be retrieved through this connector (see gaps). The complete abstract was read from two independent records (Crossref DOI record and Europe PMC, PMID 19666571, PMCID PMC2721819).
- **Rao et al. 2009, Science (entropy) — AT ABSTRACT LEVEL only.** Abstract read from Europe PMC (PMID 19389998) and Crossref. Full text not retrieved (paywalled route failed).
- **Sproat 2014, Language — AT ABSTRACT LEVEL only.** Full abstract read from the Crossref record. Full text not retrieved.
- **Rao et al. 2010 reply to Sproat — METADATA ONLY** (Crossref). Full text not retrieved.
- **Kak 1988; Kondratov 1976 — METADATA ONLY** (Crossref; Kak's Crossref record carries no abstract).

Stage-run full-text reads (recorded inside the RESEARCH-CHECK sidecars, not re-read by W1): Sinha et al. 2010 network analysis (9,800 words), Yadav n-grams (9,723 words, in the 002 runs), Palaniappan & Adhikari "Deep Learning the Indus Script" (7,474 words), Rao 2018 Indus economics (3,654 words), Nair 2026 synthetic-baseline scorecard (4,604 words).

## RESEARCH-CHECK stage records (all advisory, verdict null, exit 0)

Alt-phrasing used for both Zipf claims: "rank frequency power law fit for sign counts in the Mahadevan Indus corpus undeciphered script". For both positional claims: "signs occurring disproportionately at the start or end of short Indus inscriptions positional frequency analysis". DOI passed for all four: 10.1371/journal.pone.0009506 (the journal DOI linked from the 2009 arXiv record; the arXiv paper has no separate DOI).

| Claim | Stage record | Neighbors | Citation check in record |
|---|---|---|---|
| yadav_2009_arxiv_manual_001 | `glossa-indus/claims/research_checks/yadav_2009_arxiv__yadav_2009_arxiv_manual_001.research_check.json` (checked 2026-10-22T14:33Z) | 24 | DOI resolved to Yadav et al. 2010, PLoS ONE |
| yadav_2009_arxiv_manual_002 | `glossa-indus/claims/research_checks/yadav_2009_arxiv__yadav_2009_arxiv_manual_002.research_check.json` (2026-10-22T14:36Z) | 22 | same |
| yadav_2010_ngrams_manual_001 | `glossa-indus/claims/research_checks/yadav_2010_ngrams__yadav_2010_ngrams_manual_001.research_check.json` (2026-10-22T14:38Z) | 23 | same |
| yadav_2010_ngrams_manual_002 | `glossa-indus/claims/research_checks/yadav_2010_ngrams__yadav_2010_ngrams_manual_002.research_check.json` (2026-10-22T14:42Z) | 22 | same |

Run log: `raw/W1_stages.log`. Stage-internal source failures seen in that log: OpenAlex returned 429 during federated search; Semantic Scholar and CORE also hit 429 retries inside the server during stage runs. The stage still completed from arXiv/Crossref/Europe PMC results.

---

## Claim 1 — Zipf-Mandelbrot (yadav_2009_arxiv_manual_001 and yadav_2010_ngrams_manual_001; same proposition, 2010 record merged into 2009)

Claim as recorded: "Indus script sign frequencies follow a Zipf-Mandelbrot distribution." Status: strongly_supported.

### Does the claim appear in its source papers? YES — full text, both papers.
- 2009 arXiv, §2.1: "the data can be fit very well to the Zipf-Mandelbrot law, log fr = a − b log(r + c)". Fit values (Fig. 4 and Table 9): **a = 15.39, b = 2.59, c = 44.47** (Table 9 adds "95% Confidence interval").
- 2010 journal, abstract: "We find that unigrams follow a Zipf-Mandelbrot distribution." Body gives the identical fit (Fig. 3 caption: a = 15.39, b = 2.59, c = 44.47).
- Corpus (both papers, full text): Mahadevan's electronic concordance **M77** (417 signs, 3,573 lines, 2,906 texts), pruned to the **EBUDS** corpus (1,548 texts) after removing outliers, duplicates, damaged/illegible and multi-line texts. The fit is on EBUDS.

### Wording mismatches / qualifications
1. The claim does not name the corpus. The result is a fit on the pruned EBUDS subset of one concordance (Mahadevan lineage), not on "the Indus corpus" in general.
2. The papers' support is a visual/parametric fit ("fit very well", parameters + confidence interval in a summary table). No formal goodness-of-fit test statistic against rival distributions was found in the sections read.
3. The 2010 paper itself limits the inference, in plain words: "since distributions of city sizes, incomes and several other quantities also follow a Zipf distribution, the presence of a Zipf-Mandelbrot distribution is not sufficient to declare a sequence as linguistic." The fit therefore cannot, by the source's own statement, distinguish writing from non-writing.
4. The dossier's Glossa evidence ("Phase-43: V3 Zipf exponent ~1.35") uses a different number from the source papers' b = 2.59. Different corpus (V3) and possibly different parametrization; the audit does not adjudicate this, but the two numbers should not be cited interchangeably.

### Prior art (protocol rule 3, challenge pass)
Queries: Crossref "Indus script sign frequency distribution Zipf law" (`raw/W1_challenge_zipf_prior.json`), arXiv "Indus script Zipf frequency distribution signs" (`raw/W1_zipf_prior_arxiv.json`), Europe PMC "Indus script Zipf-Mandelbrot" (`raw/W1_europepmc_indus_zipf.json`), plus the stage's two-phrasing searches.
- **No Zipf or Zipf-Mandelbrot fit for the Indus script earlier than Yadav 2009 was found** in arXiv, Crossref, or Europe PMC. The earliest hit in every source is Yadav 2009 itself.
- Frequency analysis of the Indus script did exist earlier: **Subhash C. Kak, "A Frequency Analysis of the Indus Script", Cryptologia 12(3), 129–143, 1988, DOI 10.1080/0161-118891862873** (Crossref metadata only; the record has no abstract and the full text was not retrieved). Whether Kak fitted a Zipf-type law is an **open gap** — it is not established either way by this audit.
- Yadav 2009's own introduction (full text) traces the statistical approach to a Soviet team (1965), a Finnish team (1969), and Siromoney (1980s), and cites the same group's 2008 papers (Yadav, Vahia, Mahadevan & Joglekar, Int. J. Dravidian Linguistics 37, pp. 39–52 and 53–72) on statistical pattern search and segmentation. No Zipf fit is cited from any of those in the text read.
- Plain-words conclusion: in the sources searched, Yadav 2009 is the first published Zipf-Mandelbrot fit for Indus sign frequencies; the only unexamined earlier candidate is Kak 1988 (metadata level).

### Critiques since (challenge pass)
- **Richard Sproat, "A Statistical Comparison of Written Language and Nonlinguistic Symbol Systems", Language 90(2), 457–481, 2014, DOI 10.1353/lan.2014.0031 — at abstract level.** Sproat tests the statistical methods used to argue the Indus system is linguistic (his abstract names Rao et al. 2009a and Lee et al. 2010a, both entropy-based) on larger linguistic and nonlinguistic corpora and concludes the published measures do not discriminate as claimed; his two working measures classify the Indus inscriptions as nonlinguistic. This is a critique of the entropy/discrimination programme around Yadav/Rao, not a re-fit of the Zipf-Mandelbrot curve itself; no paper that directly re-fits or refutes Yadav's Zipf-Mandelbrot parameters was found.
- **Direct exchange on Rao et al.:** Rao, Yadav, Vahia, Joglekar, Adhikari & Mahadevan, "Entropy, the Indus Script, and Language: A Reply to R. Sproat", Computational Linguistics 36(4), 795–805, Dec 2010, DOI 10.1162/coli_c_00030 (Crossref metadata only; `raw/W1_challenge_sproat_crossref.json`). Its existence proves a published Sproat critique of the Rao group's entropy work and a published reply, both within ~1 year of the Science paper.
- Also surfaced (metadata level): Wu, Solman, Linehan et al., "Corpora of Non-Linguistic Symbol Systems" (2012), from Sproat's nonlinguistic-corpora project; Sproat, "A Taxonomy of Non-linguistic Symbol Systems" (2023).
- Semantic Scholar challenge queries (Sproat/Zipf, Zipf critique, Rao-entropy critique) all returned **429** and empty results (server log in `raw/W1_challenge_sproat_zipf.err` etc.). Per protocol that source was not retried; the critique picture above rests on Crossref + arXiv + Europe PMC.

### Verdict-relevant summary for Claim 1
The claim as extracted **is in both source papers, in full text, with identical numbers**. What the papers establish is a good-looking Zipf-Mandelbrot fit on the EBUDS subset of the Mahadevan corpus. What they do not establish (their own caveat, 2010) is that the script is linguistic. No earlier Indus Zipf fit was found (Kak 1988 unexamined — gap).

---

## Claim 2 — Beginning/ending signs (yadav_2009_arxiv_manual_002 and yadav_2010_ngrams_manual_002; same proposition, 2010 merged into 2009)

Claim as recorded: "There are specific text-beginning and text-ending signs in the Indus corpus." Status: strongly_supported. (The 2009 record's explanation notes this record carries no falsification condition — a paperwork defect already on the dossier; the audit does not change it.)

### Does the claim appear in its source papers? YES — full text, both papers.
- 2009 arXiv, abstract: "the script has well-defined signs which begin and end texts". §2.2: "Approximately 82 text beginners account for 80% of the text beginner usage, but only 23 text enders are needed to account for the same percentage of text ender usage… both text beginners and text enders are well-defined, with text enders being more strictly defined." Later sections name the most frequent beginners (signs 267, 391, 293) and enders (342, 176, 211) and analyse their conditional probabilities.
- 2010 journal, abstract: "Text beginner and ender distributions are unequal, providing internal evidence for syntax." Body: identical counts — 82 beginners / 23 enders account for ~80% (Fig. 4 caption repeats them).

### Wording qualifications
1. As with Claim 1, the counts come from EBUDS/M77 only; the claim's wording does not say so.
2. The papers frame the result as evidence of directionality/syntax; the extracted claim is the weaker, purely positional statement, which the papers support directly.

### Prior art — positional work long predates Yadav
Queries: Crossref "positional statistical analysis Indus proto-Indian texts sign position" (`raw/W1_positional_prior_crossref.json`), arXiv positional query (`raw/W1_positional_arxiv.json`); Semantic Scholar positional query returned 429/empty (gap).
- **A. M. Kondratov, "The Positional-Statistical Analysis of the Proto-Indian Texts", in The Soviet Decipherment of the Indus Valley Script (De Gruyter, 1976), pp. 39–54, DOI 10.1515/9783110800258.39** — Crossref metadata; full text not retrieved (book chapter). The same 1976 volume carries companion chapters "The Formal Analysis of the Proto-Indian Texts" and "Machine Methods of Investigation of the Proto-Indian Texts". At title/metadata level: positional-statistical analysis of Indus texts was published ~33 years before Yadav 2009.
- Yadav 2009 itself (full text) acknowledges the Soviet (1965) and Finnish (1969) statistical programmes and Siromoney's 1980s work, and its cumulative-frequency observation is explicitly "consistent with previous analysis by Mahadevan for M77 corpus" — i.e. the positional/frequency picture rests on Mahadevan's 1977 concordance statistics.
- The same group's 2008 segmentation paper (Yadav et al., IJDL 37, pp. 53–72, cited as ref [13] in the 2009 paper) also precedes it.
- Plain-words conclusion: **the beginner/ender claim was not new with Yadav.** Yadav 2009/2010 gave it a precise modern form — named beginner/ender sets, the 82-vs-23 asymmetry, and bigram conditional probabilities — but positional statistics on Indus signs go back at least to the Soviet work of the 1960s–1970s and to Mahadevan's concordance.

### Confirmations / critiques since
- Sinha, Ashraf, Pan & Wells, "Network analysis of a corpus of undeciphered Indus civilization inscriptions indicates syntactic organization", Computer Speech & Language (2011; arXiv:1005.4997, DOI 10.1016/j.csl.2010.05.007) — read in full by the stage (9,800 words, per the 002 sidecars); an independent method finding syntactic organization, consistent with positional structure. Surfaced in every positional search.
- Bryan K. Wells, "Patterns of Sign Use and the Syntactic Structure of Indus Texts" (2015, in Wells, The Archaeology and Epigraphy of Indus Writing) — metadata level; later positional/syntactic treatment.
- No published refutation of the beginner/ender asymmetry was found in the sources searched. Sproat 2014 (at abstract level) disputes what such statistics prove about linguistic status, not the positional counts themselves.

### Verdict-relevant summary for Claim 2
The claim as extracted **is in both source papers, in full text, with identical numbers (82/23)**. It is a real, reproducible feature of the M77/EBUDS corpus. It is **not a Yadav novelty**: positional-statistical analysis of Indus texts exists from 1976 (Kondratov) and, per Yadav's own text, from Mahadevan 1977 and the Soviet/Finnish programmes of the 1960s.

---

## Citation deep check — Rao et al. 2009 in the preprint

Citing text (`glossa-corpus/indus/pierson_2026_indus_decipherment.tex`, bibliography): "Rao, R.P.N. et al. (2009). A Markov model of the Indus Script. PNAS, 106(33), 13685–13690." Rao is mentioned 3 times in the preprint (body §1.2, sign-catalogue paragraph, bibliography), matching the task description.

### Bibliographic verification — MATCH on every field
Resolved DOI: **10.1073/pnas.0906237106** (`search_crossref`, `raw/W1_crossref_rao_markov.json`; `get_crossref_paper_by_doi`, `raw/W1_crossref_doi_10.1073_pnas.0906237106.json`).

| Field | Preprint | Crossref record | Result |
|---|---|---|---|
| Title | A Markov model of the Indus Script | A Markov model of the Indus script | match |
| Authors | Rao, R.P.N. et al. | Rao; Yadav; Vahia; Joglekar; Adhikari; Mahadevan | match |
| Venue | PNAS | Proceedings of the National Academy of Sciences | match |
| Year | 2009 | 2009 (published 18 Aug 2009) | match |
| Volume/issue | 106(33) | 106(33) | match |
| Pages | 13685–13690 | 13685–13690 | match |

Europe PMC independently gives the same paper: PMID 19666571, PMCID PMC2721819 (`raw/W1_europepmc_rao_markov.json`).

### Content check — AT ABSTRACT LEVEL (full text = open gap)
The abstract (read in full from Crossref and Europe PMC) confirms the paper does what its title says: a Markov chain model of sign sequences, trained on the corpus; generation of new sample texts showing recurring sign patterns; a quantitative test of whether a string belongs to the modelled system, applied to seals from Mesopotamia/West Asia (different content suggested); and prediction of missing/illegible signs. Those Markov-model results are therefore in the paper **at abstract level**. The beginner/ender distributions are **not** part of the PNAS abstract; they are Yadav 2009/2010 results (verified in full text above). Any preprint reliance on Rao PNAS specifically for beginner/ender signs is not supported by the abstract; the full text would be needed to say more, and it could not be retrieved (gaps below).

### Two mismatches in how the preprint uses "Rao et al. 2009"
1. **Entropy claim points at the wrong Rao paper.** Preprint §1.2: "Rao et al. (2009) demonstrated that IVS sign entropy is consistent with a linguistic system rather than a random or purely symbolic one." The entropy result is the **Science** paper (below), not the PNAS Markov paper. The bibliography contains only the PNAS entry; there is no Science entry. At abstract level, the PNAS abstract contains no entropy result.
2. **Zipf exponent ~1.7 is unverified against the cited source.** Sign-catalogue paragraph: "Frequency distribution follows Zipf's law (exponent ~1.7), consistent with a natural language writing system (Rao et al. 2009)." Neither Yadav paper reports 1.7 (full text: Zipf-Mandelbrot b = 2.59), and the PNAS abstract (at abstract level) reports no Zipf fit or exponent. The source of "~1.7" was not found in any text read in this audit — **open gap / likely misattribution**, flagged for correction through the programme's own gates (this audit changes nothing).

### Rao et al. 2009, Science — metadata verified
DOI **10.1126/science.1170391** (`get_crossref_paper_by_doi`, `raw/W1_crossref_doi_10.1126_science.1170391.json`): "Entropic Evidence for Linguistic Structure in the Indus Script", Rao; Yadav; Vahia; Joglekar; Adhikari; Mahadevan, **Science 324(5931), p. 1165, 29 May 2009**. Europe PMC (PMID 19389998, `raw/W1_europepmc_rao_science.json`) abstract, at abstract level: the script's conditional entropy is closer to those of natural languages than to various nonlinguistic systems — this is the result the preprint's §1.2 sentence describes. Full text not retrieved (download failed; paywalled route) — **at abstract level**.

---

## Open gaps (unread full texts are gaps, never "no prior art")

1. **Rao et al. 2009 PNAS full text not read.** Attempts, all saved in `raw/W1_dl*.json`: Crossref-source fallback (Crossref supplies no PDF; Unpaywall disabled, see 5); Europe PMC source, PMID:19666571 (first attempt "Response ended prematurely"; second hit a 403 from the PNAS reprint URL); PMC source, PMC2721819 (read timeout). The paper is open access in principle (PMC2721819) — the failure is in this connector chain, not in the paper's availability.
2. **Rao et al. 2009 Science full text not read** (download_with_fallback failed the same way). Abstract level only.
3. **Sproat 2014 (Language) full text not read** (download failed). Abstract level only.
4. **Rao et al. 2010 reply to Sproat full text not read** (download failed). Metadata only.
5. **Unpaywall was disabled** throughout (no `PAPER_SEARCH_MCP_UNPAYWALL_EMAIL` in the run environment), which removed one OA fallback route for items 1–4.
6. **Semantic Scholar: 429 for the whole W1 session.** All four Semantic queries (three challenge queries + one positional query) returned empty after the server's internal retries; per protocol the source was abandoned, not retried. OpenAlex also returned 429 inside the stage's federated searches. The audit's searches therefore rest on arXiv, Crossref, and Europe PMC.
7. **Kak 1988 full text not read** — whether an Indus Zipf-type fit predates Yadav by 21 years is unresolved.
8. **Kondratov 1976 full text not read** — the prior-art conclusion for the positional claim rests on the chapter title/metadata plus Yadav's own acknowledgement of the Soviet programme, not on the chapter's contents.
9. **One Europe PMC keyword query returned 0 results** ("Indus script entropy Zipf critique nonlinguistic", `raw/W1_challenge_indus_entropy_europepmc.json`) — a phrasing null, recorded as such; a differently phrased Europe PMC query did return the Rao and Yadav records.

## Tooling incident worth recording
The first `download_with_fallback` call for the Yadav 2010 DOI (source "crossref", before `paper_id` was supplied in the form the server requires, and again in a form it accepted) returned a PDF of a **completely unrelated paper** — Kumar et al. 2019, "Transcriptome analysis of a nematode resistant and susceptible upland cotton line…", PLoS ONE 14(9): e0221328, PMID 31504059 (2,330,962 bytes). Identity was checked against the title page before any use; the file was **deleted** and the download repeated via Europe PMC with paper_id PMID:20333254, which returned the correct paper (verified by title page and citation line). Lesson recorded for the audit: a "successful" download is not evidence of identity — verify the served artifact's title/DOI before reading. (Failed-call outputs: `raw/W1_dl_yadav2010.json`, `raw/W1_dl2_yadav2010.json`; correct download: `raw/W1_dl3_yadav2010_epmc.json`.)

## Raw evidence index (all under this audit's `raw/`, prefix W1_)
Stage run: `W1_run_stages.sh`, `W1_stages.log`. Resolution: `W1_arxiv_yadav_ngrams.json`, `W1_crossref_yadav_ngrams.json`, `W1_crossref_rao_markov.json`, `W1_crossref_doi_10.1371_journal.pone.0009506.json`, `W1_crossref_doi_10.1073_pnas.0906237106.json`, `W1_crossref_doi_10.1126_science.1170391.json`. Challenge: `W1_challenge_zipf_prior.json`, `W1_zipf_prior_arxiv.json`, `W1_challenge_sproat_crossref.json`, `W1_challenge_sproat_arxiv.json`, `W1_challenge_sproat_zipf_crossref.json`, `W1_challenge_zipf_nonlinguistic_crossref.json`, `W1_positional_prior_crossref.json`, `W1_positional_arxiv.json`, `W1_europepmc_indus_zipf.json`, `W1_europepmc_rao_markov.json`, `W1_europepmc_rao_science.json`, plus the 429-emptied Semantic files (`W1_challenge_sproat_zipf.json`, `W1_challenge_zipf_critique.json`, `W1_challenge_rao_entropy_critique.json`, `W1_positional_semantic.json`) and the 0-result Europe PMC file (`W1_challenge_indus_entropy_europepmc.json`), each with its `.err` server log. Downloads: `W1_dl*.json` series and `W1_read_rao_pnas_crossref.json`. Full texts: `W1_yadav2009_arxiv0901.3017_fulltext.txt`, `W1_yadav2010_plosone_fulltext.txt`, `W1_yadav2010_epmc/` (PDF).
