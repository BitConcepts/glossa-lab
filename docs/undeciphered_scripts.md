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

*Last updated: 2026-04-10. See `AGENT.md` for experiment-addition procedures and `LEDGER.md` for research history.*
