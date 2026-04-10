# Undeciphered Ancient Scripts and Languages
*Reference document for Glossa Lab research planning.*

This document catalogues all known undeciphered or partially deciphered ancient scripts and proto-writing systems, organised by region. It is maintained to:
- Drive experiment prioritisation (which scripts could benefit from computational analysis)
- Identify corpus acquisition targets
- Track the decipherment state of each script so we do not duplicate published work
- Note which scripts are plausible future Tier 5 hypothesis-test candidates

---

## European Scripts

| Script | Location | Date | Status | Corpus availability |
|---|---|---|---|---|
| Cretan Hieroglyphic | Crete | c. 2100 BCE | Completely undeciphered | ~300 inscribed objects; CHIC corpus published |
| Linear A | Aegean (Crete) | c. 1800–1450 BCE | Script signs known via Linear B correspondences; underlying language unknown | ~1,500 inscriptions; SigLA database |
| Phaistos Disc | Crete | c. 1850–1300 BCE | Completely undeciphered; no consensus on any reading | Single object, 242 signs; photographed |
| Cypro-Minoan | Cyprus | c. 1550 BCE | Undeciphered | ~230 inscribed objects; DĀMOS partial |
| Grakliani Hill Script | Georgia | c. 11th–10th century BCE | Undeciphered | Single inscription |
| SW Paleohispanic Script | Iberian Peninsula | c. 700 BCE | Partially deciphered; sign values proposed, language unknown | ~100 inscriptions; published corpora |
| Paleohispanic Scripts | Iberian Peninsula | c. 700 BCE onward | Several variants; some partially read | Varied; MLH / HESPERIA database |
| Sitovo Inscription | Bulgaria | c. 300–100 BCE | Undeciphered | Single inscription |
| Alekanovo Inscription | Russia | c. 10th–11th century CE | Undeciphered | Single object |
| Rohonc Codex | Hungary | 17th–19th centuries | Completely undeciphered; authorship and language unknown | ~450 pages; scanned |
| Voynich Manuscript | Medieval Europe | c. 1404–1438 (radiocarbon) | Completely undeciphered; possibly a hoax or cipher | ~240 pages; fully digitised at Beinecke Library |
| Pisa Baptistery Inscription | Italy | Medieval | Undeciphered religious text fragment | Single inscription |

---

## Near Eastern / Asian Scripts

| Script | Location | Date | Status | Corpus availability |
|---|---|---|---|---|
| Proto-Elamite | Iran (Susa) | c. 3200–2900 BCE | Completely undeciphered; one of the oldest writing systems | ~5,000 tablets; CDLI database |
| Linear Elamite | Iran | c. 2200–1850 BCE | Partially deciphered (2022 Desset et al. partial reading) | ~40 inscriptions |
| Indus / Harappan Script | Pakistan / India | c. 3500–2000 BCE | Completely undeciphered; possibly non-linguistic or Dravidian | ~4,000+ inscriptions; ICIT / Mahadevan M77 |
| Khitan Large Script | Manchuria / NE Asia | 10th–12th centuries CE | Largely undeciphered | Several hundred texts |
| Khitan Small Script | Manchuria | 10th–12th centuries CE | Mostly undeciphered; some morphological analysis done | Several hundred texts |
| Issyk Inscription | Kyrgyzstan | c. 5th–3rd century BCE | Undeciphered; Saka-Scythian context | Single gold vessel inscription |
| Ba–Shu Scripts | Ancient China (Sichuan) | Various | Undeciphered | Limited bronze inscriptions |
| Tujia Script | China | Various (folk script) | Undeciphered or unanalysed | Some museum holdings |

---

## Mesoamerican Scripts

| Script | Location | Date | Status | Corpus availability |
|---|---|---|---|---|
| Isthmian / Epi-Olmec | Mexico (southern coast) | c. 900–200 BCE | Largely undeciphered; some proposed readings | ~7 known inscriptions; Stela C, La Mojarra |
| Zapotec Writing | Oaxaca, Mexico | c. 600 BCE onward | Partially deciphered; calendar/day-signs readable, rest unclear | Several hundred inscriptions |
| Mixtec Writing | Oaxaca / Puebla, Mexico | c. 900–1600 CE | Partially deciphered; many codices and pictographic elements read | Several codices; pictographic rather than phonetic |
| Cascajal Block | Veracruz, Mexico | c. 900–800 BCE | Undeciphered; authenticity accepted but no consensus reading | Single object, 62 signs |

---

## African Scripts

| Script | Location | Date | Status | Corpus availability |
|---|---|---|---|---|
| Meroitic Script | Sudan (Kingdom of Kush) | c. 300 BCE – 350 CE | Sign values known; underlying language poorly understood | ~1,200 inscriptions; REM database |
| Wadi el-Hol Inscriptions | Egypt (Western desert) | c. 1900–1800 BCE | Early proto-Sinaitic / early alphabetic; proposed readings, no consensus | 2 main inscriptions |
| Nsibidi | Nigeria / Cameroon | Origin uncertain | Ideographic; not phonetic writing; indigenous use continues | Some collected by ethnographers |
| Proto-Saharan / Tifinar precursors | Sahara | Neolithic onward | Disputed as true writing; related to modern Tifinagh? | Rock art corpora |

---

## Oceanic Scripts

| Script | Location | Date | Status | Corpus availability |
|---|---|---|---|---|
| Rongorongo (Kōhau Rongorongo) | Easter Island (Rapa Nui) | Attested by 19th century | Completely undeciphered; oral tradition lost after 1862 slave raids | ~25 surviving objects; photographed; Fischer 1997 corpus |
| Kohi Script | Polynesia (claimed) | Various | Disputed authenticity; largely unknown | Very limited |

---

## Neolithic / Proto-Writing Systems *(Disputed as true writing)*

These are disputed as constituting true writing rather than decorative or counting symbols.

| Symbol System | Location | Date | Status |
|---|---|---|---|
| Vinča / Old European Script | Southeast Europe (near Belgrade) | c. 6000–4500 BCE | Highly disputed; many researchers consider these non-linguistic marks |
| Jiahu Symbols | China (Henan) | c. 8600–7600 BCE | Questioned whether truly writing or decorative; possibly proto-numerals |
| Banpo Symbols | China (Xi'an region) | c. 4500–3750 BCE | Possibly proto-writing; no linguistic interpretation accepted |
| Dispilio Tablet | Greece | c. 5260 BCE | Early symbols; tablet submerged and partially damaged; status debated |
| Megalithic Graffiti | Various European sites | Neolithic | Cup marks and carved symbols; status as writing not established |

---

## Three Categories of Decipherment Difficulty

Scholars recognise three primary challenge types, which drive different experimental strategies:

### 1 — Unknown Script, Known Language
The underlying language is related to a known language but the sign system is unfamiliar.
- **Examples:** Rongorongo (likely Polynesian), Zapotec (related to modern Zapotec languages), Cypro-Minoan (likely related to Mycenaean Greek)
- **Strategy:** Use modern/attested relative as language model; apply phoneme-substitution / bigram matching. This is the Ugaritic→Hebrew pattern (Tier 1a/1b) and is where our beam engine has the highest expected yield.

### 2 — Known Script, Unknown Language
The script has been deciphered (sign values known), but the language it encodes remains obscure.
- **Examples:** Etruscan (uses Greek alphabet, language unrelated to known families), Meroitic (sign values known since 1909, language only partially understood)
- **Strategy:** Use known phoneme inventory to test language-family hypotheses via Z-score / KL-divergence method. This is the Tier 5 pattern.

### 3 — Unknown Script, Unknown Language
Both the sign system and the underlying language are completely opaque.
- **Examples:** Indus script, Linear A, Proto-Elamite, Cretan Hieroglyphic, Phaistos Disc
- **Strategy:** Structural analysis (entropy, sign classification, Ventris affinity) + multi-hypothesis testing with many candidate language families simultaneously. Most difficult category; Tiers 3–5 of our programme apply here.

---

## Why These Remain Undeciphered

The fundamental obstacle is the **absence of a Rosetta Stone equivalent** — a bilingual or multilingual text that allows symbols to be anchored to a known language. Additional barriers:

1. **Small corpus** — Limited surviving texts make statistical pattern recognition unreliable. The Phaistos Disc (242 signs total) is essentially impossible to decipher computationally.
2. **Unknown language** — The underlying language may be extinct with no surviving relatives (e.g. Minoan, Proto-Elamite).
3. **Loss of context** — Slave raids (Rongorongo), deliberate destruction (Maya codices, partially), and site destruction remove crucial usage context.
4. **Disputed authenticity** — Vinča symbols, Jiahu marks, and the Cascajal Block have contested status as writing.
5. **No anchorpoints** — No identifiable proper names, numerals, calendrical dates, or other recognisable elements to bootstrap readings.
6. **Logo-syllabic complexity** — Scripts mixing logograms with phonetic signs (Indus, Proto-Elamite, Isthmian) resist pure phonological analysis.

---

## Glossa Lab Research Priority Map

Based on the criteria: *corpus size ≥ 200 inscriptions* · *known or plausible language family* · *digitised corpus available*

| Priority | Script | Rationale |
|---|---|---|
| **Active (Tier 5)** | Indus / Harappan | Large corpus (4,000+), Dravidian hypothesis strong, ICIT data held |
| **Active (Tier 4)** | Linear A | SigLA corpus; Linear B correspondences give partial anchor |
| **Next target** | Meroitic | Script readable; ~1,200 inscriptions; Nilo-Saharan / Cushitic LMs available |
| **Next target** | Linear Elamite | Partial decipherment (2022) gives anchor points; ~40 inscriptions |
| **Future** | Cretan Hieroglyphic | ~300 objects; language unknown but Minoan = likely substrate |
| **Future** | Rongorongo | ~25 objects; corpus tiny but Polynesian LM excellent |
| **Future** | Proto-Elamite | 5,000 tablets; completely undeciphered; numeric/administrative context only |
| **Future** | Cypro-Minoan | 230 objects; possible Greek link gives phonological anchor |
| **Research only** | Voynich, Phaistos Disc | Corpus too small or authenticity/language too uncertain for statistical approach |

---

## Data Sources and Corpora

| Script | Primary Source | URL / Notes |
|---|---|---|
| Linear A | SigLA (Signary of Linear A) | sigla.classics.ox.ac.uk |
| Linear A raw | tylerlengyel.com phase1 data | Used in current experiments |
| Indus | ICIT (Fuls 2023) | Physical corpus; Dr. Fuls collaboration |
| Indus | Mahadevan M77 concordance | Mahadevan (1977); OCR'd in experiments |
| Proto-Elamite | CDLI (Cuneiform Digital Library Initiative) | cdli.ucla.edu |
| Meroitic | REM (Répertoire d'épigraphie méroïtique) | Published; digital version in progress |
| Rongorongo | Fischer (1997) corpus | 25 objects catalogued |
| Cretan Hieroglyphic | CHIC (Corpus Hieroglyphicarum Inscriptionum Cretae) | Published 1996 |
| Cypro-Minoan | DĀMOS (Oslo) | Partial; work in progress |
| Linear Elamite | Desset et al. (2022) | Recent partial decipherment publication |

---

---

## Glossa Lab Implementation Status

The following scripts have **active corpus modules** implemented in `backend/glossa_lab/data/`:

| Script | Module | Corpus size | Benchmark | Status |
|---|---|---|---|---|
| **Proto-Sinaitic** | `proto_sinaitic.py` | 576 tokens, 22 signs | Tier 1e | ✅ Active — 19/22 = 86.4% with anchors |
| **Meroitic** | `meroitic.py` | 551 tokens, 19 signs | Tier 1f | ✅ Active — graceful degradation test |
| **Indus / Harappan** | `indus_public_corpus.py` | 14,213 tokens, 713 signs | Tier 5 | ✅ Active — primary research target |

The following are implemented as **test fixtures** or **language model corpora**:

| Script | Usage | Location |
|---|---|---|
| **Ugaritic** | Tier 1a/1b/1c cipher text | `tests/corpora/ugaritic.py` |
| **Old Hebrew** | Tier 1a/1b/1c target LM | `data/old_hebrew.py` |
| **Phoenician** | Tier 1c target LM | `data/phoenician.py` |
| **Linear B** | Tier 4 (Ventris) | `tests/corpora/fixtures/linear_b.txt` |
| **Tamil/Dravidian** | Tier 5 comparison LM | `data/dravidian.py` |
| **Sumerian** | Tier 3 logographic reference | `tests/corpora/fixtures/sumerian.txt` |

---

## Digital Corpus Availability — Detailed Notes

### High-priority scripts with substantial digital corpora

**Indus / Harappan Script**
- ICIT corpus (Fuls 2023): ~4,410 inscriptions, 14,213 tokens — held by Dr. Fuls, TU Berlin
- Mahadevan concordance M77: ~3,700 inscriptions; partially OCR'd in `reports/`
- IVC Digital Database (BSOAS): available to academic subscribers
- Format: sign ID sequences (Fuls numbering or Mahadevan M-codes)
- Current Glossa Lab status: full pipeline active on ICIT corpus

**Proto-Elamite**
- CDLI (Cuneiform Digital Library Initiative): ~5,000 tablets at cdli.ucla.edu
- Accessible via API: `https://cdli.ucla.edu/search/`
- Format: cuneiform sign sequences in ATF transliteration
- Token estimate: ~200,000 sign tokens across all tablets
- Note: purely administrative (numerals + commodities), no phonetic reading possible
- Glossa Lab status: not yet implemented; high priority for structural analysis

**Linear A**
- SigLA (Signary of Linear A): sigla.classics.ox.ac.uk — ~1,500 inscriptions
- GORILA (Recueil des inscriptions en linéaire A): published 1985–2003
- Digital: DĀMOS (Oslo) partial; tylerlengyel.com Phase 1 data (used in experiments)
- Format: sign code sequences (AB01, AB02, etc.)
- Token estimate: ~7,500–10,000 sign tokens
- Glossa Lab status: statistical model in `tests/corpora/linear_a_corpus.py`

**Meroitic**
- REM (Répertoire d'épigraphie méroïtique): ~1,200 inscriptions; publication ongoing
- Digital: partial transcriptions at academia.edu; Rilly (2007) appendix
- Format: sign sequences (Griffith values: a, e, i, b, t, k, n, r, s, l, m, w, y, d, q, h, ne, se, te)
- Token estimate: ~15,000–20,000 sign tokens from attested corpus
- Glossa Lab status: active in `data/meroitic.py` (551-token sample corpus)

**Rongorongo**
- Fischer (1997) catalogue: 25 surviving objects, ~14,000 glyphs total
- Digital: Hochenburger database; Fischer 1997 ISBN 978-0-252-02349-9
- Format: glyph ID sequences (Fischer numbering)
- Token estimate: ~3,000–4,000 unique glyph types; 14,000 total tokens
- Note: corpus is very small per inscription; ~25 objects means ~25 sequences
- Glossa Lab status: not yet implemented; blocked by small per-inscription corpus

**Cretan Hieroglyphic**
- CHIC (Corpus Hieroglyphicarum Inscriptionum Cretae, Olivier & Godart 1996)
- ~300 inscribed objects; digitised from CHIC publication
- Token estimate: ~800–1,200 sign tokens
- Glossa Lab status: too small for statistical methods; pending

**Cypro-Minoan**
- DĀMOS (Database of Mycenaean at Oslo): partial
- Steele (2018) corpus: most comprehensive
- ~230 inscriptions; ~2,000 sign tokens
- Glossa Lab status: candidate for Tier 1 if Linear B phoneme overlap is used as anchor

### Scripts needing corpus acquisition

**Proto-Sinaitic (expanded)**
- Current Glossa Lab corpus: 576 tokens (research-quality reconstruction)
- Full attested corpus: ~40 inscriptions, ~500 sign tokens
- Available: Sass (1988), Hamilton (2006), Darnell et al. (2005)
- Status: ADEQUATE — our 576-token corpus exceeds the attested material

**Linear Elamite (newly partially deciphered)**
- Desset et al. (2022) partial decipherment — Nature paper
- ~40 inscriptions; ~500 sign tokens
- Acquisition: the paper appendices and supplementary material
- Status: high priority — partial anchor points now available

**Khitan (Large and Small)**
- Several hundred texts; some catalogued in Chinese academic databases
- Format: character sequences with some known morphological markers
- Status: difficult acquisition; Chinese academic partnerships needed

---

## Corpora Planned for Future Implementation

Based on acquisition feasibility and research priority:

| Script | Priority | Blocker | Expected Tier |
|---|---|---|---|
| Proto-Elamite | High | Format conversion from CDLI ATF | Tier 3 (structural only) |
| Linear Elamite | High | Acquire Desset 2022 supplement | Tier 1 (with partial anchors) |
| Rongorongo | Medium | Acquire Fischer 1997 digital | Tier 5 (Polynesian LM) |
| Cypro-Minoan | Medium | DĀMOS access | Tier 1 (Linear B anchors) |
| Vinca symbols | Low | Disputed writing status | Structural only |
| Khitan Large | Low | Chinese database access | Structural only |

---

*Last updated: 2026-04-10. See `AGENTS.md` for experiment-addition procedures,
`LEDGER.md` for research history, and `docs/FINETUNING_GUIDE.md` for AI model
tuning. Cross-reference: `backend/glossa_lab/data/` for implemented corpus modules.*
