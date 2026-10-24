# Findings W3 — Parpola 2010 claims + Dravidian-reading-family positioning

Worker W3, Material Audit 2026-10-22, protocol: `docs/paper-search-mcp.md`.
Claims audited (from `glossa-indus/claims/extracted_claims/parpola_2010_dravidian_solution.json`,
read in full incl. `explanation_record` / `not_understood` / `status_correction` before searching):

- **001** "Indus script encodes Proto-Dravidian language using the rebus principle." (status: unsupported)
- **002** "The fish sign (meen in Dravidian) is the primary rebus sign in the Indus script." (status: partially_supported)

No claim file, dossier, status, or preprint text was modified. No scholar was contacted.
Nothing here adjudicates the decipherment; this reports the literature.

---

## 0. Source status this session (protocol rate discipline)

| Source | Status |
|---|---|
| Crossref | WORKED throughout (search + `get_crossref_paper_by_doi`). |
| CORE (keyed) | WORKED. |
| Europe PMC | WORKED but irrelevant (biomedical index; no Indus hits). |
| HAL | WORKED, returned empty for this topic. |
| OpenAlex | **429 on first call** (`W3_openalex_parpola2010.err`) → source closed for the session per protocol, not retried. The stage's own federated calls also record OpenAlex among requested sources; its merged output cannot be separated here. |
| Semantic Scholar | **429 (anonymous, no key configured)** (`W3_semantic_parpola2010.err`) → source closed for the session, not retried. |
| arXiv | Reached only inside the RESEARCH-CHECK stage (see §1). Keyword-trap hits present, as warned in the protocol doc. |
| BASE | Not called (expected empty from this VM per protocol doc). |
| Unpaywall | Disabled (no email configured) — noted in every stage log. |
| Sci-Hub | Hard-off; never invoked. |

Consequence: protocol rule 1 wants ≥2 concept phrasings × ≥2 independent sources including a
semantic index (Semantic Scholar/OpenAlex). Both semantic indexes 429'd, so the semantic-index leg
is an **open gap** for both claims; Crossref + CORE + Europe PMC + HAL carried the manual pass,
and the stage's federated `search_papers` ran its own source mix.

---

## 1. Stage records (RESEARCH-CHECK, spec 025)

Command shape (both runs): from `backend/`, env loaded from the research-keys file
(values never printed), `python -m glossa_lab.research_check --claim-file …parpola_2010_dravidian_solution.json
--claim-id <id> --alt-phrasing "<stranger phrasing>"`. **No `--doi` was passed** — see §3:
no DOI for Parpola 2010 could be resolved, so `citation_checks` is empty in both sidecars.
Logs: `raw/W3_stage_001.log`, `raw/W3_stage_002.log`.

### Claim 001 — sidecar `glossa-indus/claims/research_checks/parpola_2010_dravidian_solution__parpola_2010_dravidian_solution_manual_001.research_check.json`
- checked_at 2026-10-22T14:37:54Z; advisory; **verdict null** (by construction).
- Phrasings: claim text + caller alt "Harappan seal signs spell an ancestral Dravidian tongue
  through picture puns where a drawn object stands for a sound-alike word".
- Sources requested: arxiv, crossref, openalex, semantic, core, europepmc. source_errors: [].
- 24 neighbors. Read in FULL TEXT by the stage: Yadav et al., "Statistical analysis of the
  Indus script using n-grams" (arXiv 0901.3017, 9,723 words); Kalyanaraman, "Indus script
  corpora, archaeo-metallurgy and Meluhha (Mleccha)" (arXiv 1204.3800, 24,938 words);
  plus one arXiv keyword-trap item on Italian rebuses/LLMs (not a neighbor in substance).
  Several rel-0.0 arXiv hits are the protocol's known default-list trap (ATLAS/GW papers) —
  disregarded.
- Substantive neighbors at metadata/abstract level only (stage gap list): "Proto-Dravidian
  and the Indus Script" (Wells 2011 volume chapter, DOI 10.2307/j.ctvr43jmf.14); Brice's
  1970 JRAS review of Parpola et al. 1969 (DOI 10.1017/s0035869x00128461); the Soviet-school
  chapter "Prospects for the linguistic interpretation of the Proto-Indian texts (on the
  basis of the Dravidian languages)" (Gurov, DOI 10.1515/9783110800258.119, rel 0.0 in the
  stage's ranking but a true neighbor — see §4a); Mukhopadhyay fish-sign papers (§4d).

### Claim 002 — sidecar `…__parpola_2010_dravidian_solution_manual_002.research_check.json`
- checked_at 2026-10-22T14:41:36Z; advisory; **verdict null**.
- Phrasings: claim text + caller alt "Harappan fish pictogram read through a Dravidian
  homophone where the word for fish also means star, used as a phonetic pun in seal names".
- 26 neighbors. Stage full-text reads were mostly arXiv sign-language traps (irrelevant);
  one substantive read: "Network analysis of a corpus of undeciphered Indus civilization
  inscriptions…" (9,800 words).
- The closest fish-specific neighbors — Mukhopadhyay's maṇi / gemstone fish-sign papers
  (OSF DOI 10.31235/osf.io/ftdzc; SSRN DOI 10.2139/ssrn.4412558) — were surfaced but **not**
  read in full by the stage; they are recorded in the sidecar's gap list and are treated
  **at abstract level** in §4d below.

---

## 2. Are the two extracted claims actually Parpola 2010's positions, as worded?

**Yes for both — verified in FULL TEXT** of Parpola 2010 (see §3 for which version of
the text was read and the citation problem this creates).

Full text read: the complete text of "A Dravidian solution to the Indus script problem"
as reproduced online (the 2010 Coimbatore lecture text, 34 pp., running pagination 1–34;
mirrors: harappa.com PDF link; Scribd doc 36350863; full text embedded in the
134804.activeboard.com thread, read pp. 11–19 in detail). Independent corroboration of
its wording and pagination: Jyothibabu (2023) quotes "Parpola (2010: 13)" and
"Parpola (2010: 16)", matching this text's pages 13 and 16 exactly (§4d).

- Claim 001 — Parpola's elimination argument (pp. 11–13 of the lecture text): after
  excluding Indo-Iranian, Burushaski, Tibeto-Burman and Austro-Asiatic, "The only
  remaining alternative among the well-known potential linguistic relatives of the
  Harappan language is the Dravidian language family"; "Historical linguistics thus
  suggests that the Harappans probably spoke a Dravidian language." Script-type and
  method (pp. 13–14): the script is logo-syllabic (~400 signs); a pictogram's meaning
  "was extended from the word for the depicted object to comprise all its homophones";
  "phonetic decipherment is possible only in cases where the rebus principle has been
  employed"; four conditions for deciphering a sign, incl. "(2) the said pictogram has
  been used as a rebus" and "(4) acceptably homophonous words … exist in a historically
  likely known language", with Proto-Dravidian homophony strictness stated.
  → The claim's wording ("encodes Proto-Dravidian language using the rebus principle")
  is a fair compression of Parpola 2010's stated position. **FULL TEXT.**
- Claim 002 — the paper's own structure makes the fish sign its starting point and
  primary worked example: section "Starting point: the 'fish' signs of the Indus script"
  (pp. 15–16): fish signs "occur so frequently on Indus seals that almost every tenth
  sign belongs to this group", yet fish is never mentioned in Mesopotamian seal
  inscriptions, so "the 'fish' signs denote something else than 'fish' and are used as
  rebuses. The most commonly used word for 'fish' in Dravidian languages is miin, and
  has the homophone miin meaning 'star'." Compounds follow: '6'+fish = aru-miin
  (Pleiades), '7'+fish = eZu-miin (Ursa Major), vaTa-miin (pole star), pp. 16–19.
  → "Primary rebus sign" matches Parpola's presentation (his starting point; ~10% of
  signs; the rebus on which the subsequent readings are built). One nuance vs. the
  dossier: Parpola's argument is about the fish-sign *group* (plain + diacritic-modified
  variants) on *seals*; the dossier's own explanation record already notes the family
  does not behave uniformly in Glossa's Phase-43 test (sign 72 vs. sign 267). **FULL TEXT.**

---

## 3. Citation verification — Parpola (2010) [THE HEADLINE PROBLEM]

Preprint entry (`glossa-corpus/indus/pierson_2026_indus_decipherment.tex`, reference list):

> Parpola, A. (2010). A Dravidian solution to the Indus script problem. *World Archaeology*, 42(2), 178–193.

Field-by-field:

| Field | Preprint | Verified record | Verdict |
|---|---|---|---|
| Author | Parpola, A. | Asko Parpola | MATCH |
| Year | 2010 | 2010 | MATCH |
| Title | A Dravidian solution to the Indus script problem | Identical title | MATCH |
| Venue | *World Archaeology* | **No Crossref record found** for this title in *World Archaeology* across 4 Crossref query phrasings (5/10/20/20 results; files `W3_crossref_parpola2010_search/_b/_c/_d.json`). Every secondary source found cites the work as the **Kalaignar M. Karunanidhi Classical Tamil Research Endowment Lecture, World Classical Tamil Conference, Coimbatore, 25 June 2010, published Chennai: Central Institute of Classical Tamil (2010), 34 pp.** — harappa.com ("presented … June 25, 2010 in Coimbatore and published by the Central Institute for Classical Tamil. Download 34 page PDF"); the thetbs.org bibliography ("delivered at the World Classical Tamil Conference, Coimbatore, in June 25, 2010 (Chennai: Central Institute of Classical Tamil)"); Jyothibabu 2023's in-text citations to its pp. 13/16 (lecture pagination). | **MISMATCH / UNVERIFIED** |
| Volume/issue | 42(2) | No record located that attaches this title to *World Archaeology* 42(2). (Parpola's actual *World Archaeology* Indus article is the 1986 "The Indus script: A challenging puzzle", *WA* 17(3):399–419, DOI 10.1080/00438243.1986.9979979 — Crossref-verified in `W3_crossref_parpola2010_b.json`.) | **UNVERIFIED** |
| Pages | 178–193 | The citable text's pagination is 1–34 (lecture volume); all located scholarly quotations use that pagination (pp. 13, 16). No 178–193 pagination located. | **MISMATCH / UNVERIFIED** |
| DOI | (preprint gives none) | **UNRESOLVED.** No DOI surfaced via Crossref (×4 queries), CORE, Europe PMC, HAL, or the federated search. OpenAlex and Semantic Scholar could not be tried (429, §0). If a *World Archaeology* version exists, its DOI remains an **open gap**, not a proven absence. | **GAP** |

Reading of the evidence: the title/author/year are real and the *content* attributed to
"Parpola 2010" in the preprint and in the claim dossier is genuinely Parpola's 2010 text
(§2, FULL TEXT). But the journal/volume/pages fields of the preprint's entry could not
be verified against any index, and all located evidence points to the CICT lecture
publication instead. This is filed as a **citation-field mismatch requiring a correction
proposal** (gate-pending per the audit plan; nothing was edited). It is not asserted
that no *World Archaeology* version exists — Crossref search is a search, not a
registry dump — only that (a) four phrasings found no such record, and (b) every
secondary citation located gives the lecture publication.

Full-text route note: the *World Archaeology* text, if it exists, was not reached
(paywalled/unlocated → gap). The full text actually read is the author's 2010 lecture
text, which is the version the field quotes (Jyothibabu 2023, FULL TEXT). The MCP
`download_with_fallback` route could not be exercised for this item because it keys
off a DOI/paper_id and no DOI could be resolved.

### Neighboring preprint entries verified in passing
- **Parpola (1994)** *Deciphering the Indus Script*. Cambridge: Cambridge University
  Press — **MATCHES**. Six independent review records in Crossref all carry
  "Cambridge: Cambridge University Press, 1994, pp. xxii + 374" (see §4b;
  `W3_crossref_parpola1994book.json`).
- **McAlpin (1981)** — preprint: "McAlpin, D.W. (1981). *Proto-Elamo-Dravidian: The
  Evidence and Its Implications*. Philadelphia: American Philosophical Society."
  Crossref: David W. McAlpin, *Transactions of the American Philosophical Society*
  71(3), 1981, DOI 10.2307/1006352; book form, American Philosophical Society Press,
  DOI 10.70249/9798893981803 (`W3_crossref_mcalpin1981.json`). Title/author/year/
  publisher **MATCH** (the preprint cites the APS monograph form; the journal-of-record
  is Trans. APS 71(3)). A review by Zvelebil exists: JAOS 105(2):364 (1985),
  DOI 10.2307/601741 — metadata only.

### Preprint reliance count
"Parpola" occurs exactly **26 times** in the .tex (grep count, this session), the most
of any source (next: Mahadevan-lineage references). In-text reliance includes the
Phase-159 cross-validation section ("44/75 HIGH-confidence H+M readings appear in
Parpola's [1994] text"), the 45-entry Mahadevan–Parpola crosswalk, and the framing
"Parpola (1994, 2010) assembled the most comprehensive Dravidian rebus decipherment"
(§1.2). The Dravidian-family positioning of the preprint therefore stands or falls
with Parpola 1994 (verified) + Parpola 2010 (content verified, citation fields not).

---

## 4. Challenge pass — prior art and rivals for the Dravidian reading family

### (a) Earlier Dravidian decipherment attempts — who published fish/mīn and rebus first?

Priority for the fish = mīn rebus is **not** Parpola's, and not 2010's or 1994's:

1. **Father Henry Heras (1930s–1953)** — first publisher of the fish = mīṉ ('fish' =
   'star') reading, per Mahadevan (1998b) as quoted in Jyothibabu 2023, §11, **FULL
   TEXT**: "it was the brilliant idea of Father Heras that the 'fish' sign in the Indus
   script represented the word mīṉ, which means 'fish' as well as 'star' or 'planet'
   in all the Dravidian languages." Corroborated (secondary) by harappa.com: "Like
   the Jesuit priest Father Heras in the 1930s, he [Parpola] proposed … that the fish
   sign represented the word *min*". Heras's own texts (e.g. *Studies in Proto-Indo-
   Mediterranean Culture*, 1953) were not retrieved — attribution is FULL TEXT at one
   remove (a peer-reviewed review quoting Mahadevan), the Heras primary text is a gap.
2. **The Soviet school (Knorozov et al., 1965ff.)** — Proto-Dravidian readings by
   computer/positional analysis, independent of and parallel to Helsinki. Crossref-
   verified corpus (`W3_crossref_knorozov.json`): the Soviet team's chapters in the
   1976 English volume (De Gruyter/Mouton, DOI stem 10.1515/9783110800258): Knorozov,
   "The formal analysis of the Proto-Indian texts"; **Gurov, "Prospects for the
   linguistic interpretation of the Proto-Indian texts (on the basis of the Dravidian
   languages)"**; Kondratov (positional-statistical analysis); Probst (machine
   methods); Alekseev; Volčok. Their 1965 *Preliminary report* was reviewed by
   Zide & Zvelebil (1970), DOI 10.2307/412267. Metadata level for content; but see
   Jyothibabu (FULL TEXT): **Gurov (1976)** evaluated Dravidian fish words and read
   the 'twinkling fish' (sign 67) as **kay** (carp) — i.e. the Soviet school published
   on the fish sign, with a *different* Dravidian value, in the 1970s.
3. **The Finnish team itself (1969–70)** — Parpola, Koskenniemi, S. Parpola & Aalto,
   *Decipherment of the Proto-Dravidian Inscriptions of the Indus Civilization: A
   First Announcement* + *Progress/Further Progress* (Scandinavian Institute of Asian
   Studies, 1969–70): fish signs as divine names of planetary deities / personal
   names / planetary conjunctions (summarized in Mahadevan 1970 via Jyothibabu 2023,
   FULL TEXT). Contemporary reviews located: Marr, BSOAS 34(1):160–164 (1971),
   DOI 10.1017/s0041977x00141837; Brice, JRAS (1970), DOI 10.1017/s0035869x00128461;
   Clauson & Chadwick, "The Indus Script Deciphered?" (in `W3_crossref_jha_rajaram.json`
   returns — a skeptical contemporary review of the 1969 announcement; abstract in file).
4. **Mahadevan (1970)** — adopted mīn/mīṉ with modifications (argued the form is
   mīṇ/*mīḷ, 'lord/chieftain' via mīḷi), and disputed the Finnish planetary-conjunction
   reading of fish clusters (composite personal names instead). FULL TEXT via
   Jyothibabu 2023 §11.
5. **Fairservis (1992)** — *The Harappan Civilization and its Writing: A Model for
   Decipherment* (Brill; Crossref-verified, DOI 10.1163/9789004676756;
   `W3_crossref_fairservis1992.json`). A Dravidian reading independent of Parpola's
   system; his rebus explanation of fish = 'star' via Old Tamil min- homophony was
   already in his 1985 *Scientific American* article, as quoted in Elst's survey
   (web full text, secondary). Fairservis thus published the fish/star rebus in
   popular-scientific form in 1985 and in book form in 1992 — after Heras and the
   1969 announcements, before Parpola 1994's book synthesis.
   Wikipedia's summary (secondary) states the convergence plainly: the Finnish team
   "proposed readings of many signs, some agreeing with the suggested readings of
   Heras and Knorozov (such as equating the 'fish' sign with the Dravidian word for
   fish 'min')".

**Priority finding:** fish/mīn and the rebus method for it were published by Heras
(1930s), taken up in print by both the Soviet and Finnish teams in 1965–70, and by
Mahadevan (1970) and Fairservis (1985/1992), all before Parpola 2010. Parpola 2010 is
a restatement/synthesis, not the origin — the preprint does not claim otherwise
explicitly, but its "Parpola (1994, 2010) assembled the most comprehensive Dravidian
rebus decipherment" framing should not be read as priority for the fish reading.

### (b) Published reception of Parpola (1994) *Deciphering the Indus Script*

Six peer-reviewed-journal reviews, all **metadata-verified via Crossref**
(`W3_crossref_parpola1994book.json`, `W3_crossref_review_*.json`); none read in full
(all paywalled — JSTOR/Wiley/SAGE; recorded as a gap, no content claims made):

| Reviewer | Venue | DOI |
|---|---|---|
| Dilip K. Chakrabarti | *JRAS* (1995) | 10.1017/s1356186300006829 |
| Florian Coulmas | *Language* 72 (1996), 167–170 | 10.2307/416809 |
| Thomas Oberlies | *BSOAS* (1996) | 10.1017/s0041977x00031980 |
| Stuart Blackburn | *South Asia Research* 16 (1996) | 10.1177/026272809601600114 |
| Jonathan Mark Kenoyer | *American Anthropologist* 98(1) (1996), 198–199 | 10.1525/aa.1996.98.1.02a00470 |
| Richard Salomon | *JAOS* 116(4) (1996), 745 | 10.2307/605446 |

Substantive reception readable in full text this session: Jyothibabu (2023) treats
Parpola 1994 as one of the main Dravidian-framework attempts and notes (with Mahadevan
2015 and Levitt 2009) that "there is no conclusive evidence to support the argument
that the language in the Harappan script is Dravidian. Still, there is a definite
possibility that the language is Dravidian." (**FULL TEXT.**) The Farmer–Sproat–
Witzel non-linguistic challenge (2004) was aimed substantially at Parpola-style
decipherment (harappa.com summary, secondary; the EJVS original is not in Crossref —
`W3_crossref_farmer2004.json` returns instead Lawler's *Science* news report,
DOI 10.1126/science.306.5704.2026, and Rao et al.'s reply to Sproat, *Computational
Linguistics*, DOI 10.1162/coli_c_00030 — both metadata level here).

### (c) Rival language-family proposals in the peer-reviewed literature

- **Indo-Aryan / Sanskrit readings:** Jha & Rajaram, *The Deciphered Indus Script*
  (2000) — the preprint itself labels it "widely rejected". The book has **no
  Crossref record** in the top-5 for its query (`W3_crossref_jha_rajaram.json`);
  metadata gap recorded (Aditya Prakashan, New Delhi — outside Crossref's core
  coverage). Newer Indo-Aryan-claim items do circulate via SSRN (e.g. a 2026
  "Comparative Linguistic Model … Proto-Indo-Aryan" preprint in the same file) —
  preprint-server level, not peer-reviewed verification.
- **Munda / substrate proposals:** Witzel (1999), "Substrate Languages in Old
  Indo-Aryan", *EJVS* 5(1):1–67 — cited by the preprint for proto-Munda. **No
  Crossref record surfaced** for it (`W3_crossref_witzel1999.json`, EJVS carries no
  Crossref DOIs) — metadata gap, not a non-existence finding. Its argument (a
  prefixing "Para-Munda" substrate in the Punjab, distinct from both Dravidian and
  Indo-Aryan) is the main peer-reviewed rival *substrate* account; Southworth (2005)
  *Linguistic Archaeology of South Asia* (also preprint-cited) is its book-length
  companion. Content here is from the preprint's own usage + general record —
  **at abstract level** for W3 purposes (full texts not retrieved).
- **Elamo-Dravidian (McAlpin 1981):** metadata-verified in §3. Note the direction of
  support: McAlpin links Elamite to Dravidian, which would put a Dravidian relative
  on the Iranian plateau — used by the Dravidian family as external support, and by
  Parpola 2010's own text (Proto-Elamite stimulus diffusion for writing, p. 13 of the
  lecture text) as background. Zvelebil's 1985 JAOS review (metadata only) is the
  located peer-reviewed reception. McAlpin's hypothesis remains contested in
  historical linguistics; no full text read → reception detail is a gap.
- **Non-linguistic / semasiographic:** Farmer, Sproat & Witzel (2004) (above);
  Mukhopadhyay's mercantile-semasiographic variant (§4d) — a rival *within* a
  broadly Dravidian-linked frame.
- Parpola 2010's own rival-elimination (FULL TEXT, §2) is itself a useful map: he
  argues *against* Indo-Iranian (horse/chariot chronology), BMAC-substrate words
  (Lubotsky/Kuiper lists reassigned to a pre-Indus BMAC language), Burushaski,
  Tibeto-Burman, and Austro-Asiatic — leaving Dravidian "the only remaining
  alternative". The preprint's rival list (proto-Munda per Witzel; Indo-Aryan per
  Jha & Rajaram; non-linguistic per Farmer et al.) matches the published field.

### (d) Published critiques of the fish-sign reading specifically

**FULL TEXT — Jyothibabu, C. (2023). "Iravatham Mahadevan's Reading of Indus Script:
A Critical Review." *Studia Orientalia Electronica* 11(1):1–63, DOI
10.23993/store.85246** (CC BY-NC-SA; read in full via its academia.edu copy; §11
"Sign 59 'Fish'", pp. 16–19 of the article). Points that bear directly on claim 002:

- Mahadevan (2011: 5) himself concluded the fish = mīṉ = 'star' theory "**had run
  out of steam and needed reappraisal**": (1) a bulky 'fish' sign is an unlikely
  choice to write 'star' if space mattered; (2) number + fish sequences belong to a
  larger number + sign system and need not be constellations; (3) unexplained
  affinities of fish signs with the four-stroke modifier, 'arrow', and 'mortar and
  pestle' signs.
- Wells (1998): possibly another sign for 'star' exists; fish as a major mercantile
  item (an economic, not astral, reading of fish frequency).
- Alternative Dravidian values published for the same sign: Gurov (1976) **kay**
  (carp); Jyothibabu's own proposal **kaḻ** ('fish/fire/star/great' chain); Mahadevan's
  *mīḷ/vēḷ* line. The fish sign thus has multiple mutually exclusive published
  Dravidian readings — the mīn reading is not the field's only Dravidian candidate.
- The review also notes Mahadevan's observation that mīṉ does not occur as an element
  in ancient Dravidian personal/clan names — awkward for the astral-name theory built
  on it.

**At abstract level — Mukhopadhyay (2023/2025)**, "Can the semasiographic/logographic
Indus script answer the Dravidian question? Insights from Indus script's gemstone
related fish-signs, and Indus gemstone-word 'maṇi'" (OSF DOI 10.31235/osf.io/ftdzc;
SSRN DOI 10.2139/ssrn.4412558): reads certain fish-like signs as *logograms* tied to
gemstone symbolism (maṇi) in a mercantile script — i.e. the fish signs' prominence is
explained without the mīn phonetic rebus. Abstract only; full text not read (stage gap).

Also in the preprint's own eco-system: Possehl is reported (harappa.com, secondary)
as not accepting Parpola's interpretations; and the dossier's Phase-125
cross-compilation caveat (sign-list disagreement) applies to any fish-sign claim —
internal record, noted in claim 002's explanation record.

---

## 5. Per-claim summary

### Claim 001 (Proto-Dravidian + rebus; status: unsupported)
- **Held:** As a statement of *Parpola 2010's position*, the claim is accurate —
  verified in FULL TEXT (§2). The Dravidian+rebus family is a real, long-published
  research program (Heras → Soviet & Finnish teams 1965–70 → Mahadevan, Fairservis,
  Parpola 1994/2010), not a fringe or invented attribution.
- **Failed / challenged in the literature:** the claim as a statement about the
  script itself has no consensus: Jyothibabu 2023 (FULL TEXT) — "no conclusive
  evidence" for Dravidian; rival families/substrates (Para-Munda per Witzel 1999,
  Indo-Aryan per Jha & Rajaram 2000, Elamo-Dravidian per McAlpin 1981) and the
  non-linguistic thesis (Farmer et al. 2004) are all in the peer-reviewed/ scholarly
  record. This is consistent with the dossier's own Spec-033-driven correction to
  *unsupported* (internal record, not re-adjudicated here).
- **Gaps:** semantic-index leg (OpenAlex/Semantic Scholar 429); Parpola 2010 DOI
  unresolved; Witzel 1999 and Farmer et al. 2004 full texts not retrieved (no
  Crossref records; EJVS).

### Claim 002 (fish = mīn, primary rebus sign; status: partially_supported)
- **Held:** As Parpola 2010's position — accurate, FULL TEXT (§2): fish is his
  "starting point", ~1 in 10 seal signs, mīn 'fish' = mīn 'star' homophony, with
  external support argued from fish/star co-occurrence on Mature Harappan pottery
  and the absence of a separate 'star' sign.
- **Failed / qualified:** **Priority** — the reading is Heras's (1930s), published by
  both 1960s teams and Mahadevan/Fairservis decades before 2010 (§4a). **Critiques**
  — Mahadevan's own 2011 reappraisal ("run out of steam"), Wells 1998, and rival
  published values for the same sign (Gurov's kay, Jyothibabu's kaḻ, Mukhopadhyay's
  maṇi logograms at abstract level) mean "the fish sign = mīn" is one contested
  candidate among several, including within Dravidian readings (§4d). The claim's
  word "primary" is Parpola's framing, not a field consensus.
- **Gaps:** Heras primary texts not retrieved; Mukhopadhyay fish papers not read in
  full (abstract level); Parpola 1994's fish chapters not re-read (book paywalled/
  print only).

### Citation verdicts (preprint reference list)
- Parpola 2010: author/year/title MATCH; **venue/volume/pages MISMATCH-UNVERIFIED**
  (*World Archaeology* 42(2):178–193 not found in any index searched; located record
  = CICT Coimbatore lecture, Chennai 2010, 34 pp.); DOI UNRESOLVED → correction
  proposal candidate, gate-pending.
- Parpola 1994: MATCHES (CUP, 1994, xxii+374 pp., six review records concur).
- McAlpin 1981: MATCHES (APS; journal form Trans. APS 71(3), DOI 10.2307/1006352).

---

## 6. Raw evidence filed (all under this `raw/` directory, prefix W3_)

Stage logs: `W3_stage_001.log`, `W3_stage_002.log`; sidecars in
`glossa-indus/claims/research_checks/` (see §1).
Manual queries: `W3_crossref_parpola2010_search.json` (5), `…_b.json` (10),
`…_c.json` (20), `…_d.json` (20), `W3_federated_parpola2010.json`,
`W3_openalex_parpola2010.json` (empty + 429 err), `W3_semantic_parpola2010.json`
(empty + 429 err), `W3_core_parpola2010.json`, `W3_europepmc_parpola2010.json`,
`W3_hal_parpola2010.json` (empty), `W3_crossref_review_10.1525_aa.1996.98.1.02a00470.json`,
`W3_crossref_review_10.2307_605446.json`, `W3_crossref_review_10.2307_416809.json`,
`W3_crossref_mcalpin1981.json`, `W3_crossref_knorozov.json`,
`W3_crossref_fairservis1992.json`, `W3_crossref_witzel1999.json`,
`W3_crossref_farmer2004.json`, `W3_crossref_parpola1994book.json`,
`W3_core_fish_heras.json`, `W3_crossref_jha_rajaram.json` (each with a `.err` log).
Full texts read via browser (not MCP): Parpola 2010 lecture text (activeboard
reproduction + Scribd mirror + harappa.com record); Jyothibabu 2023 (academia.edu
copy of the CC-licensed journal article).
