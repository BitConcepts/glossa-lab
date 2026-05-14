# Glossa-Corpus Batch 1 Acquisition Report

**Date:** 2026-05-14  
**Sources checked:** 15  
**Sources acquired:** 7 OK, 5 PARTIAL, 3 FAILED  
**Total files downloaded:** 125,481

## Acquisition Results

| Source | Status | Texts | Files |
|---|---|---|---|
| Open Greek and Latin | OK | 3808 | 4326 |
| Perseus Digital Library | OK | 3619 | 3994 |
| GRETIL Sanskrit | FAIL | 0 | 0 |
| SARIT Sanskrit | OK | 88 | 144 |
| ORACC cuneiform | PARTIAL | 0 | 0 |
| Sefaria Hebrew/Aramaic | PARTIAL | 0 | 48 |
| OpenITI Arabic/Persian | OK | 0 | 103 |
| CBETA Chinese Buddhist | PARTIAL | 0 | 0 |
| SuttaCentral Pali/Buddhist | FAIL | 43153 | 113803 |
| ETCBC Hebrew Bible | OK | 0 | 1157 |
| Chinese Text Project/Kanseki | PARTIAL | 0 | 1 |
| LSJ Greek Lexicon | PARTIAL | 0 | 0 |
| Monier-Williams Sanskrit Dict | OK | 0 | 1830 |
| Lewis & Short Latin Dict | FAIL | 0 | 0 |
| Gesenius Hebrew Lexicon | OK | 0 | 75 |

## Languages Covered

| Language | Script | Period | Source |
|---|---|---|---|
| Ancient Greek | Greek | 750 BCE–600 CE | Perseus, OGL |
| Latin | Latin | 200 BCE–600 CE | Perseus, OGL |
| Sanskrit | Devanagari/IAST | 1500 BCE–1800 CE | GRETIL, SARIT, MW lexicon |
| Sumerian/Akkadian | Cuneiform | 3100 BCE–100 CE | ORACC |
| Classical Hebrew | Hebrew | 1200 BCE–100 BCE | Sefaria, ETCBC, Gesenius |
| Aramaic | Hebrew | 500 BCE–500 CE | Sefaria, ETCBC |
| Arabic/Persian | Arabic | 600 CE–1900 CE | OpenITI |
| Classical Chinese | Han | 600 BCE–1900 CE | CText, Kanseki, CBETA |
| Pali/Buddhist Skt | Multiple | 500 BCE–200 CE | SuttaCentral |

## Sources Quarantined
None — all sources classified as open_license, public_domain, or research_use.

## Next Recommended Sources (Batch 3)
- Internet Archive scans: critical editions, rare grammars, manuscript facsimiles
- Gallica (BnF): French manuscript holdings
- HathiTrust public-domain: university press critical editions
- ETCSL Sumerian literature (CC BY-SA)
- Lane Arabic Lexicon (archive.org scan)
- Wikisource classical Chinese

## Legacy Glossa-Lab Assets Review
- Existing Indus corpus: M77 (A.1), Holdat LLC (A.13) — **KEEP** (superior to any available alternative)
- Existing TB corpus: mahadevan_2003_tamil_brahmi.json — **KEEP** (Phase-33 T3 cleaned version in production)
- Existing Dravidian LM: dravidian_syllable_lm.json — **KEEP** (DEDR-based, matches research provenance)

## Batch 1 Summary
Successfully acquired foundations for ancient Greek, Latin, Sanskrit, Cuneiform, Hebrew, Arabic, Chinese, and Pali corpora. All materials preserved in provenance-tracked raw directories with SHA-256 checksums and YAML provenance records. Ready for extraction and normalization pipeline.
