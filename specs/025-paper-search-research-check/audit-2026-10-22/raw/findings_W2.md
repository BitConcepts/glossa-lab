# Findings — Worker W2 (Farmer/Sproat/Witzel non-linguistic thesis cluster)

Material audit 2026-10-22, spec 025, protocol `docs/paper-search-mcp.md`.
Worker: W2. Date of runs: 2026-10-22 (EDT). No dossiers, statuses, or
preprint files were modified. No adjudication of any decipherment is
performed here; this file reports what the published literature holds.

## Sources, failures, and rate discipline

- RESEARCH-CHECK stage run serially for all four claims (details per
  claim below). Sources requested by the stage: arXiv, Crossref,
  OpenAlex, Semantic Scholar, CORE, Europe PMC; `source_errors: []`
  in all four stage records.
- Manual paper-search queries: 24 saved as
  `raw/W2_q01…q24_*.json`; full-text attempts/reads saved as
  `raw/W2_ft01…ft10_*.json`. Web evidence index:
  `raw/W2_browser_sources.json`.
- **429s (source closed for this W2 session on first 429, per
  protocol; no retry loops):**
  - OpenAlex — 429 on first manual call (q02, q04 returned empty).
    The stage's own earlier federated calls reported no errors; the
    manual OpenAlex channel is recorded as a gap.
  - Semantic Scholar — 429 on first manual call (q05, empty).
  - CORE — 429 after its internal retries (q11, empty), even with
    the CORE key exported per the task recipe.
- Europe PMC returned empty (not an error) for Farmer 2004 (q12) and
  for Mukhopadhyay 2023 (q22): neither item is usefully indexed
  there. BASE not used (protocol: expected empty / unsearched).
- `download_with_fallback` failed for every Crossref-sourced DOI
  tried (ft01–ft07): the tool reports Crossref provides no PDF and
  the Unpaywall fallback is disabled (no Unpaywall email configured
  in this environment). OA full texts were therefore read through
  author/journal OA copies located by web search (indexed in
  `W2_browser_sources.json`) and through arXiv (`read_arxiv_paper`).
  This is a tooling gap, not a finding of non-existence.
- Stage-record noise warning: the stage's arXiv neighbors include
  the documented default-list trap (ATLAS / gravitational-wave
  papers sharing no vocabulary with the query) in all four records.
  Those are not neighbors and were not treated as such. The stage's
  genuinely relevant neighbors are noted per claim.

## Citation verification — Farmer, Sproat & Witzel (2004) (protocol rule 4)

Verified field by field:

| Field | Dossier / task statement | Verified value | Route |
|---|---|---|---|
| Authors | Farmer, Sproat & Witzel | Steve Farmer; Richard Sproat; Michael Witzel | Journal landing page (search rendering); PDF title page (FULL TEXT) |
| Title | "The Collapse of the Indus-Script Thesis" | "The Collapse of the Indus-Script Thesis: The Myth of a Literate Harappan Civilization" | Journal landing page; PDF title page (FULL TEXT) |
| Venue | Electronic Journal of Vedic Studies 11(2) | Electronic Journal of Vedic Studies (EJVS) 11-2 (2004), ISSN 1084-7561 (printed on p. 19 of the PDF) | PDF header (FULL TEXT) |
| Pages | 19–57 | pp. 19–57 | PDF header; multiple independent bibliographies (Parpola 2008 ref list; Sinha et al. 2010 ref [20], both read in FULL TEXT) |
| Year | 2004 | 2004 (issue dated December 13, 2004 in the EJVS announcement) | Journal announcement rendering |
| DOI | (task: EJVS may have none) | **10.11588/ejvs.2004.2.620 exists** (Heidelberg EJVS). Crossref lookup of this DOI returned an empty record (q13) — it is **not Crossref-registered**; the DOI landing page itself was bot-blocked on direct fetch, and its metadata were read from the search rendering of that page (title/authors/abstract match) — **at abstract level** for the landing-page fields, FULL TEXT for everything checkable in the PDF itself | q13; W2_browser_sources.json |

Thesis as extracted — confirmed in FULL TEXT of the paper itself
(author-hosted PDF, 39 pp.; abstract, "The brevity of the
inscriptions", the lost-manuscript section, and the sign-frequency /
sign-repetition sections read): the paper argues (i) inscriptions are
extreme in brevity — longest on one surface 17 signs, average 4.6
signs over the 2,905 objects in Mahadevan's concordance, under 1% as
many as 10 signs; (ii) the "lost-manuscript" thesis (long texts on
perishable materials) is impossible — no archaeological markers of
manuscript production; (iii) sign frequencies cannot by themselves
distinguish scripts from non-scripts (their Fig. 2 heraldry
comparison), but within-inscription sign repetition is anomalously
low — 10 of the 20 highest-frequency signs have zero or near-zero
repetition across the whole corpus — which they take to show little
if any sound encoding; (iv) the symbols are therefore nonlinguistic
emblems comparable to Near Eastern nonlinguistic systems, not a
script encoding speech. The dossier's normalized claim ("not a
writing system encoding language but consists of non-linguistic
symbols") is a faithful compression of this. FULL TEXT.

Roif quote-fragment check (task 3): the two Roif critique fragments
are **title fragments of this 2004 paper**, not body propositions —
"myth of a literate Harappan" matches the subtitle "The Myth of a
Literate Harappan Civilization" and "collapse of the Indus script
thesis" matches the main title "The Collapse of the Indus-Script
Thesis" (hyphenation/casing differ in the fragments). Both fragments
verified against the paper's title page in FULL TEXT. The secondary
source's use of them as section headings is consistent with that.

## The challenge pass — strongest literature in both directions

### Against Farmer et al. (the program's recorded direction)

1. **Rao et al. 2009, *Science* 324(5931):1165 — "Entropic Evidence
   for Linguistic Structure in the Indus Script."** DOI
   10.1126/science.1170391 verified in full via Crossref (q03/q14:
   title, all six authors, venue, volume/issue, page 1165, date
   2009-05-29). Crossref abstract is one line ("Analysis of the
   pattern of symbols confirms the linguistic role of ancient
   signs") — the paper itself is paywalled at AAAS and its full text
   was **not** read; **at abstract level** for the Science paper
   itself. Its method and result are, however, described in detail
   inside two FULL-TEXT sources below: bigram conditional entropy of
   the Indus corpus falls with linguistic systems and away from two
   artificial extremes.
2. **Rao et al. 2010, *Computational Linguistics* 36(4):795–805 —
   "Entropy, the Indus Script, and Language: A Reply to R. Sproat."**
   DOI 10.1162/coli_c_00030 verified via Crossref (q15/q17). **FULL
   TEXT read** (author's PDF, §§1–4 and references). What it actually
   says: (a) Rao et al. never claimed entropy similarity alone proves
   language; it is inductive evidence alongside other language-like
   properties; (b) Sproat (2010) used only their Fig. 1A and omitted
   Fig. 1B and the block-entropy extension, whose scaling (N=1…6,
   NSB estimator) tracks natural languages and separates from DNA,
   protein, music, and Fortran controls; (c) "barring a full
   decipherment, one cannot prove either the linguistic or
   nonlinguistic thesis" — i.e., Rao's own framing rejects the
   *proof* claim Farmer et al. made, it does not claim a proof of
   the opposite; (d) the scholarly reception: point-by-point rebuttals
   by Parpola (2005, 2008), Vidale (2007), McIntosh (2008), plus
   Possehl (2004), Kenoyer (2004), Mahadevan (2009) in disagreement.
3. **Parpola 2008, "Is the Indus script indeed not a writing
   system?", in *Airāvati* (Mahadevan felicitation volume),
   pp. 111–131** (enlarged version of Parpola 2005, Tokyo). **FULL
   TEXT read** (opening sections). Parpola enumerates Farmer et
   al.'s ten theses and answers them one by one: on frequencies, he
   quotes Farmer et al.'s own concession (p. 29) that sign-frequency
   studies cannot determine linguistic vs nonlinguistic, and records
   Sproat's April 2005 e-mail agreement with Koskenniemi that plain
   statistical tests can neither prove nor falsify writing status; on
   brevity, five signs suffice for noun phrases in a logo-syllabic
   script of the Sumerian type (Mesopotamian seal texts are comparably
   short name/office formulas); on "no random-looking repetition," he
   gives concrete counterexamples of within-inscription repetition in
   non-adjacent positions (M-682, M-634, M-1792, K-10, M-1169, M-357).
4. **Vidale 2007, "The collapse melts down: a reply to Farmer,
   Sproat and Witzel", *East and West* 57:333–366.** Citation
   verified via the FULL-TEXT reference lists of Rao et al. 2010 and
   Sproat 2014; Crossref keyword search did not surface it (q19 —
   recorded gap). The paper itself was **not** read in full; its
   verdict is known from Rao et al. 2010's quotation (p. 362: "I see
   no acceptable scientific demonstration of the non-scriptural
   nature of the Indus sign system; therefore, I see no collapse of
   such 'thesis'") — **at abstract level / quoted-in-full-text**
   for Vidale's own argumentation.
5. **Yadav et al. 2010, *PLoS ONE* 5(3):e9506 — "Statistical
   analysis of the Indus script using n-grams."** DOI
   10.1371/journal.pone.0009506; **FULL TEXT read** (arXiv:0901.3017
   version, ft08, 9,723 words). Conclusions table: beginners/enders
   are asymmetric (69 signs = 80% of beginners; 23 signs = 80% of
   text-enders in one corpus slice), bigram correlations are strongly
   non-random, perplexity falls monotonically to n=5 (long-range
   correlations), and a Markov model restores illegible signs at 74%
   cross-validated accuracy. This is the published basis closest to
   the program's own Phase-43 positional claims (beginner/ender
   asymmetry) — produced outside the program, on the same
   Mahadevan lineage.
6. **Sinha et al. 2010/2011, *Computer Speech & Language* 25:639–654
   — network analysis.** arXiv:1005.4997 **FULL TEXT read** (ft09):
   segmentation-tree recursion and network structure "suggest the
   existence of a grammar underlying these inscriptions."
7. **Rao, Lee, Yadav et al. 2015, *Language* 91(4):e198–e205 — "On
   statistical measures and ancient writing systems."** DOI
   10.1353/lan.2015.0055 verified via Crossref (q21). **At abstract
   level** for Rao et al.'s own text (abstract: Sproat 2014
   misrepresents their methods; its entropic results "seem to favor,
   rather than contradict" the inductive linguistic hypothesis; "we
   stand by our original findings"), supplemented by Sproat's
   FULL-TEXT reply (below), which quotes their pp. e199–e203.

### For Farmer et al. / against the entropy argument (partial vindication)

8. **Sproat 2010, *Computational Linguistics* 36(3):585–594 —
   "Ancient Symbols, Computational Linguistics, and the Reviewing
   Practices of the General Science Journals."** DOI
   10.1162/coli_a_00011 verified via Crossref (q17: volume 36(3),
   pp. 585–594). **FULL TEXT read** (author-uploaded PDF, §§1–2).
   Core argument: the Rao Type 1 / Type 2 "nonlinguistic" curves in
   the Science paper were artificially generated (random-equiprobable
   and rigid models), not real symbol systems; Vinča was not random
   and kudurru deity order was not rigid, contrary to the paper's
   glosses; statistical techniques had never before been claimed to
   *determine* that a system is linguistic, and only a verifiable
   decipherment can settle writing status affirmatively.
9. **Sproat 2014, *Language* 90(2):457–481 — "A Statistical
   Comparison of Written Language and Nonlinguistic Symbol
   Systems."** DOI 10.1353/lan.2014.0031 verified via Crossref
   (q07/q16, incl. full abstract). **FULL TEXT read** (LSA PDF:
   abstract, §1, §2 summary, §2.6–2.7 results as excerpted, §3
   Discussion). What it actually says: with seven real nonlinguistic
   corpora (Vinča, Pictish, kudurru deity symbols, totem poles, barn
   stars, weather icons, emoticons) against fourteen writing systems,
   **none of the previously proposed measures — Rao's conditional /
   block entropies included — discriminate as published**; all of
   Sproat's nonlinguistic systems fall inside the "linguistic"
   entropic middle range (memoryless systems with nonuniform
   distributions mimic it too). The two measures that do classify
   (a Lee et al. measure at a different cut-off, and a repetition
   measure) work largely because they correlate with **mean text
   length**, and both classify the Indus bar seals and Pictish as
   **nonlinguistic** (94 of 100 CART trees with heraldry/math corpora
   added). §3 restates the Farmer-side positive evidence: all texts
   very short with no lengthening over ~700 years, no manuscript-
   production markers, no cursive development. This is the strongest
   published form of the thesis's statistical defense, and it
   directly targets the dossier's contradicting evidence item 1
   (Rao 2009).
10. **Sproat 2015, *Language* 91(4):e206–e208 — "On
    misunderstandings and misrepresentations: A reply to Rao et
    al."** **FULL TEXT read** (LSA PDF). Sproat's closing position:
    an entropic value in the middle range shows a system is
    "consistent with being linguistic" but equally "consistent with
    being a nonlinguistic system"; he accuses the Rao camp's shifting
    interpretations of unfalsifiability. The published exchange thus
    ends (2015) **without either side conceding**, in the field's
    flagship linguistics journal.
11. **Mukhopadhyay 2023, *Humanities and Social Sciences
    Communications* 10:912 (38 pp.) — "Semantic scope of Indus
    inscriptions comprising taxation, trade and craft licensing,
    commodity control and access control…"** DOI
    10.1057/s41599-023-02320-7 verified via Crossref (q18, which also
    lists the OSF/SSRN preprint versions). **At abstract level**
    (full text OA at the publisher but not retrieved through any
    route available here — see gaps): building on her prior
    structural analyses, she argues the script was "semasiographic
    and/or logographic," that inscriptions encode **no proper nouns**
    (no personal/place/organization names), and that seals functioned
    as tax/trade/access-control instruments and tablets as licenses.
    This is a peer-reviewed 2023 position that vindicates Farmer et
    al.'s *functional* core (inscriptions do not spell out language
    the way decipherment claims assumed) while not adopting their
    emblem framing wholesale. Her 2019 companion paper
    (*HSS Communications* 6:49, "Interrogating Indus inscriptions to
    unravel their mechanisms of meaning conveyance") is bibliographic
    record only here.
12. **Nair 2026, arXiv:2604.17828 — "How Non-Linguistic Is the Indus
    Sign System? A Synthetic-Baseline Scorecard."** Preprint, single
    author, **not peer-reviewed on any record found**. **FULL TEXT
    read** (ft10). Directly re-tests the four Farmer et al. (2004)
    properties (brevity, phrase repetition, hapax rate, positional
    rigidity): no synthetic heraldic or administrative generator
    reproduces all four at once; Indus sits between the baselines
    (H_cond replicated at 3.23 bits; ordering far from random,
    percentile 0.000 vs 1,000 permutations); the author expressly
    does **not** claim to resolve the linguistic question. Mixed
    evidence: it sharpens, and partly supports, the Farmer-side
    demand that a nonlinguistic model must match all four properties,
    while showing current nonlinguistic models do not.
13. Also surfaced, **at abstract level** (Crossref record in q03):
    Bose 2026 (SSRN/OSF preprint), "Sequential Structure Without a
    Linguistic Diagnosis" — trigram-over-bigram gains in the Indus
    corpus **reverse** when duplicate sequences cannot leak between
    training and test folds, and the author concludes ordinary
    sequential-structure results "should not be read as established
    evidence" of generalizable structure. A 2026 preprint challenge
    to the n-gram line (item 5 above), not peer-reviewed on any
    record found.

### Current standing, as the literature presents it

No 2020s review located in this audit declares the Farmer thesis
either dead or victorious. The verifiable state of play is: (a) the
thesis's *proof* claim was rejected in print by the leading Indus
epigrapher (Parpola 2005/2008), a leading archaeologist (Vidale
2007), and the Rao group ("one cannot prove either thesis" without
decipherment); (b) the thesis's *statistical rebuttal* — that Rao
et al.'s entropy result does not discriminate — was sustained in
print by its own author in the field's flagship journal (Sproat
2014) and never withdrawn, with the exchange closing in mutual
non-concession (Rao et al. 2015 / Sproat 2015); (c) a peer-reviewed
2023 functional analysis (Mukhopadhyay) revives a non-phonetic,
semasiographic reading on archaeological grounds; (d) the script
remains undeciphered and the question open in every source read.
Sproat's own later syntheses (his 2023 book *Symbols: An
Evolutionary History…* and 2024 *Introduction to Writing Systems*,
Crossref q06) exist but were **not read** — bibliographic record
only. **Open gap:** no dedicated 2020s review article on the Indus
script problem was found through Crossref/arXiv/Europe PMC queries
(q10, q23, q24 returned mostly self-published decipherment claims
and older chapters); if a recent scholarly state-of-the-question
review exists, it was not reached by this audit's sources.

---

## Per-claim findings

### 1. `farmer_sproat_witzel_2004_manual_001` — "The Indus script is not a writing system encoding language but consists of non-linguistic symbols." (recorded: contradicted)

- **Stage record:**
  `glossa-indus/claims/research_checks/farmer_sproat_witzel_2004__farmer_sproat_witzel_2004_manual_001.research_check.json`
  (25 neighbors, 3 full texts read by the stage — all three are
  arXiv false neighbors, see noise warning; 0 source errors;
  verdict null). Phrasings: the claim's own words + caller phrasing
  "predictability of next symbol in short Bronze Age seal
  inscriptions measured by conditional entropy compared to
  linguistic and emblem systems." Stage log:
  `raw/W2_stage_farmer.log`.
- **Stage neighbors of actual relevance (abstract level in the stage
  record):** "Indus valley script is linguistic" (*Nature India*
  news, 2009, DOI 10.1038/nindia.2009.128); "A Taxonomy of
  Non-linguistic Symbol Systems" (2023, Crossref). The rest are
  off-topic.
- **Extraction fidelity — HELD.** The claim faithfully compresses
  the 2004 paper (citation verification above, thesis confirmed in
  FULL TEXT, including the brevity statistics and the repetition
  paradox). The dossier's falsification condition (entropy in
  linguistic range; positional pattern above random baseline) is
  the test the literature actually fought over.
- **What the audit does to the recorded framing:** the dossier's
  contradicting-evidence list leads with "Rao et al. 2009:
  conditional entropy falls in linguistic range." That result is
  real and verified — but as a *settled refutation* it **failed to
  survive the challenge pass**: Sproat (2014, FULL TEXT) shows the
  entropy measures do not discriminate linguistic from real
  nonlinguistic systems, and Rao et al. themselves (2010, FULL TEXT)
  frame the result as inductive evidence only and expressly deny
  that either thesis can be proved without a decipherment. The
  explanation record's own caution ("specialists still debate the
  entropy result itself") is, on the literature read, an
  understatement of how contested the result is: the debate ended
  in print stalemate (2015), not in a Rao victory.
- **What held:** the thesis was *not* accepted by the field either —
  Parpola (FULL TEXT), Vidale (quoted in FULL TEXT), Possehl,
  Kenoyer, McIntosh, Mahadevan all rejected its proof claim; the
  program's Phase-43-type positional findings have published
  external analogues (Yadav et al. 2010 n-grams, FULL TEXT; Sinha
  et al., FULL TEXT). The accurate literature framing is "strongly
  contested, unresolved," with published support on both sides —
  narrower than a plain reading of "contradicted" suggests, and
  the dossier's `not_understood` field already says much of this.
- **Open gaps:** Rao et al. 2009 *Science* full text not read
  (paywalled; abstract level + FULL-TEXT secondary descriptions).
  Vidale 2007 full text not read. Sproat's 2010 "Reply to Rao et
  al. and Lee et al." (DOI 10.1162/coli_c_00031) and Lee et al.'s
  response (DOI 10.1162/coli_c_00029) verified bibliographically
  via Crossref (q17) but not read; their positions are known via
  the FULL-TEXT Rao reply and Sproat 2014/2015.

### 2. `without_kings_or_conquests_the_indus_scr_ce9d98cc_language_0001` — "Language hypothesis: non-linguistic symbol" (recorded: contradicted, by Phase-104 RULE-DUP carry-over from claim 1)

- **Stage record:**
  `glossa-indus/claims/research_checks/without_kings_or_conquests_the_indus_scr_ce9d98cc__without_kings_or_conquests_the_indus_scr_ce9d98cc_language_0001.research_check.json`
  (25 neighbors, 3 stage full texts — all false neighbors
  (language-model papers); 0 source errors; verdict null).
  Caller phrasing: "Harappan stamp seal sign sequences length
  distribution and positional rigidity as test of spoken language
  encoding in a Bronze Age urban society." Log:
  `raw/W2_stage_language0001.log`.
- **Neighbors:** none of the stage's 25 neighbors is a true
  neighbor (the fragment's wording gives the indexes almost nothing
  to match); the true neighbors are exactly claim 1's, established
  by the manual pass (items 1–13 above). Recorded as a stage-quality
  gap for fragment-type claims, not as absence of literature.
- **Substance:** this record is a category label restating claim
  1's thesis; every finding for claim 1 applies unchanged. Its
  quote fragment "non-linguistic symbol" is consistent with the
  2004 paper's terminology (FULL TEXT: "nonlinguistic symbol
  systems" passim). The carry-over logic is therefore substantively
  sound; the literature-framing caveat is claim 1's (the "settled
  refutation" reading of Rao 2009 does not survive Sproat 2014).
- **Open gaps:** same as claim 1. Nothing claim-specific was left
  unsearched: the fragment carries no independent content to check.

### 3. `indus_valley_script_deciphered_from_myth_65ff0a26_critique_0001` — "Critique: myth of a literate Harappan" (recorded: contradicted, carry-over)

- **Stage record:**
  `glossa-indus/claims/research_checks/indus_valley_script_deciphered_from_myth_65ff0a26__indus_valley_script_deciphered_from_myth_65ff0a26_critique_0001.research_check.json`
  (20 neighbors, **0 full texts read by the stage**, 0 source
  errors; verdict null). Caller phrasing: "archaeological absence
  of long texts manuscripts and monumental inscriptions in Indus
  Valley cities as evidence against widespread literacy." Log:
  `raw/W2_stage_critique0001.log`.
- **Stage neighbors of actual relevance:** Sinha et al. network
  analysis (arXiv:1005.4997 — read in FULL TEXT manually, ft09);
  Mukhopadhyay's semantic-scope paper (Crossref, 2023 — the q18
  item, abstract level). Remainder off-topic (incl. the arXiv
  default-list trap).
- **Extraction fidelity — HELD, with a classification note.** The
  quote fragment "myth of a \nliterate Harappan" is a verbatim
  fragment of the 2004 paper's **subtitle** ("The Myth of a
  Literate Harappan Civilization"), verified on the paper's title
  page in FULL TEXT. It is a title, not a proposition; treating it
  as a restatement of the thesis (as Phase-104 did) is defensible
  because the subtitle names the paper's target, but the record is
  a bibliographic fragment, and the audit confirms the dossier's
  own `not_understood` bookkeeping concern is well founded.
- **Substance / framing:** identical to claim 1 — the "myth" the
  title names is the literate-Harappan assumption Farmer et al.
  attacked; the literature's verdict on that attack is contested
  stalemate (see challenge pass), not a clean refutation of the
  attack nor acceptance of it.
- **Open gaps:** the stage read no full text for this claim (gap
  in the stage record itself; closed manually by W2 via ft08/ft09
  and the web full texts). All claim-1 gaps apply.

### 4. `indus_valley_script_deciphered_from_myth_65ff0a26_critique_0002` — "Critique: collapse of the Indus script thesis" (recorded: contradicted, carry-over)

- **Stage record:**
  `glossa-indus/claims/research_checks/indus_valley_script_deciphered_from_myth_65ff0a26__indus_valley_script_deciphered_from_myth_65ff0a26_critique_0002.research_check.json`
  (23 neighbors, 3 stage full texts; 0 source errors; verdict
  null). Caller phrasing: "frequency of sign repetition brevity
  and rigid ordering of Indus inscriptions undermining decipherment
  as a full writing system encoding speech." Log:
  `raw/W2_stage_critique0002.log`.
- **Stage neighbors of actual relevance:** Yadav et al. n-grams
  (arXiv:0901.3017 — stage-read and manually read in FULL TEXT,
  ft08; its Table 9 is the closest published analogue of the
  program's positional battery); Sinha et al. network analysis
  (FULL TEXT, ft09); Rao 2018 "The Indus Script and Economics"
  (arXiv:1812.00049, abstract level here).
- **Extraction fidelity — HELD, same classification note.** Quote
  fragment "collapse of the Indus script thesis" is a verbatim
  fragment of the 2004 paper's **main title** ("The Collapse of
  the Indus-Script Thesis"), verified in FULL TEXT. Note the
  direction of the title: the "collapse" Farmer et al. announce is
  the collapse of the *pro-writing* thesis — a reader of the
  fragment alone could invert it. The dossier's carry-over reads
  the direction correctly.
- **Substance / framing:** identical to claim 1. One addition from
  the challenge pass bears directly on this fragment's wording:
  Vidale's 2007 reply is titled "The collapse melts down" and
  concludes there was "no collapse of such 'thesis'" (quoted in
  Rao et al. 2010, FULL TEXT) — i.e., the collapse claim itself
  was answered in print, by name, within three years; and Sproat
  (2014/2015, FULL TEXT) continued to defend the underlying
  position in the field's flagship journal a decade later.
- **Open gaps:** all claim-1 gaps apply.

## Summary of what held, what failed

- **Held:** all four extractions faithfully point at Farmer,
  Sproat & Witzel (2004); the citation is real and now carries a
  verified DOI (10.11588/ejvs.2004.2.620, non-Crossref); the thesis
  as extracted matches the paper's full text; the Rao et al. 2009
  entropy result exists exactly as the dossiers cite it; positional
  / n-gram structure results from outside the program (Yadav 2010,
  Sinha 2010) exist in full text and point the program's way.
- **Failed:** the implied framing that Rao et al. 2009 *settled*
  the matter against Farmer et al. In the published record the
  entropy argument was answered by Sproat (2010, FULL TEXT) and
  Sproat (2014, FULL TEXT — the measures do not discriminate; the
  measures that do classify Indus as nonlinguistic, largely via
  text length), Rao et al. (2010, FULL TEXT) themselves claim only
  inductive evidence and deny either thesis is provable, and the
  exchange closed in 2015 without concession on either side. A
  peer-reviewed 2023 semasiographic/functional reading
  (Mukhopadhyay, abstract level) partially vindicates the Farmer
  side. The thesis's current standing in the literature is
  **contested and unresolved**, with its *proof* claim rejected
  and its *statistical defense* unrefuted-in-print — a materially
  different picture from an unqualified "contradicted," though the
  dossiers' own `not_understood` fields already record most of
  this nuance.
- **Open gaps (recorded, not papered over):** OpenAlex, Semantic
  Scholar, CORE all 429-closed for manual queries; Rao 2009
  *Science* full text, Vidale 2007 full text, Mukhopadhyay 2023
  full text, Sproat 2010 reply / Lee et al. 2010 response full
  texts, and Sproat's 2023/2024 book syntheses not read (each
  labelled at abstract level or bibliographic where used); no
  dedicated 2020s state-of-the-question review of the Indus script
  problem was reached through Crossref/arXiv/Europe PMC;
  `download_with_fallback` is non-functional for Crossref DOIs in
  this environment (Unpaywall disabled).
