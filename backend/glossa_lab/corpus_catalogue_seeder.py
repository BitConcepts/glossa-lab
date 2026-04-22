"""World Language Corpus Catalogue seeder.

Populates the corpus_catalogue DB table with ~50 entries covering:
  - Undeciphered scripts (active research)
  - Deciphered ancient scripts (reference/comparator)
  - Modern language typological comparators

Entries with `local_module` can be imported in one click.
Entries without a local_module require manual upload from the source URL.

Run on startup: called from glossa_lab/main.py after DB init.
"""
from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger("glossa_lab.corpus_catalogue_seeder")

# ─── Catalogue entries ────────────────────────────────────────────────────────
# Fields: id, name, language, language_family, script_type, period,
#         tokens_approx, source_url, license, description,
#         local_module (empty = manual upload required), is_undeciphered

CATALOGUE: list[dict[str, Any]] = [

    # ── Undeciphered scripts ──────────────────────────────────────────────────
    {
        "id": "cat-indus",
        "name": "Indus Script (Mahadevan 1977 synthetic)",
        "language": "Unknown",
        "language_family": "Undeciphered",
        "script_type": "unknown",
        "period": "2600–1900 BCE",
        "tokens_approx": 14213,
        "source_url": "https://www.harappa.com/script/",
        "license": "Research use",
        "description": "Synthetic Indus Script corpus from the ICIT sign catalogue (Mahadevan 1977). Primary research target for Glossa Lab.",
        "local_module": "indus_public_corpus",
        "is_undeciphered": True,
    },
    {
        "id": "cat-linear-a",
        "name": "Linear A (DĀMOS database)",
        "language": "Minoan (unknown)",
        "language_family": "Undeciphered",
        "script_type": "syllabary",
        "period": "1800–1450 BCE",
        "tokens_approx": 7000,
        "source_url": "https://damos.hf.uio.no/",
        "license": "Academic use (DĀMOS)",
        "description": "Bronze Age Minoan script; related to Linear B but not yet deciphered. 7000+ tokens from tablets and inscriptions.",
        "local_module": "",
        "is_undeciphered": True,
    },
    {
        "id": "cat-proto-sinaitic",
        "name": "Proto-Sinaitic (Serabit el-Khadim + Wadi el-Hol)",
        "language": "Proto-Semitic",
        "language_family": "Semitic",
        "script_type": "abjad",
        "period": "1900–1500 BCE",
        "tokens_approx": 576,
        "source_url": "https://en.wikipedia.org/wiki/Proto-Sinaitic_script",
        "license": "Public domain",
        "description": "Earliest known alphabet ancestor. 576 tokens from Egyptian turquoise mines. Partially deciphered.",
        "local_module": "proto_sinaitic",
        "is_undeciphered": True,
    },
    {
        "id": "cat-meroitic",
        "name": "Meroitic (Kushite inscriptions)",
        "language": "Meroitic (unknown language)",
        "language_family": "Northeast African",
        "script_type": "abjad",
        "period": "300 BCE – 400 CE",
        "tokens_approx": 551,
        "source_url": "https://en.wikipedia.org/wiki/Meroitic_alphabet",
        "license": "Public domain",
        "description": "Script of the Kushite kingdom. Deciphered phonetically but language not fully understood. 551 tokens.",
        "local_module": "meroitic",
        "is_undeciphered": True,
    },
    {
        "id": "cat-rongorongo",
        "name": "Rongorongo (Easter Island)",
        "language": "Rapa Nui (unknown)",
        "language_family": "Undeciphered",
        "script_type": "unknown",
        "period": "Pre-1722 CE",
        "tokens_approx": 14000,
        "source_url": "https://rongorongo.org/",
        "license": "Academic use",
        "description": "Undeciphered glyphic script from Easter Island. ~14,000 tokens across 26 tablets.",
        "local_module": "",
        "is_undeciphered": True,
    },
    {
        "id": "cat-zapotec",
        "name": "Zapotec Script (Monte Albán)",
        "language": "Zapotec (proto-Zapotecan)",
        "language_family": "Oto-Manguean",
        "script_type": "logosyllabic",
        "period": "500 BCE – 700 CE",
        "tokens_approx": 3000,
        "source_url": "https://en.wikipedia.org/wiki/Zapotec_writing",
        "license": "Academic use",
        "description": "Mesoamerican hieroglyphic script from Monte Albán. Partially deciphered.",
        "local_module": "",
        "is_undeciphered": True,
    },
    {
        "id": "cat-voynich",
        "name": "Voynich Manuscript",
        "language": "Unknown",
        "language_family": "Undeciphered",
        "script_type": "unknown",
        "period": "~1400–1500 CE",
        "tokens_approx": 38000,
        "source_url": "https://www.voynich.nu/",
        "license": "Public domain",
        "description": "Medieval illustrated manuscript; language/script unknown. ~38,000 word tokens. Structural analysis candidate.",
        "local_module": "",
        "is_undeciphered": True,
    },

    # ── Deciphered ancient scripts ─────────────────────────────────────────────
    {
        "id": "cat-ugaritic",
        "name": "Ugaritic Baal Cycle (KTU 1.1–1.6)",
        "language": "Ugaritic",
        "language_family": "Semitic",
        "script_type": "abjad",
        "period": "1400–1200 BCE",
        "tokens_approx": 945,
        "source_url": "https://en.wikipedia.org/wiki/Ugaritic_alphabet",
        "license": "Public domain",
        "description": "Ugaritic cuneiform abjad. 29 signs. Test corpus for NW Semitic decipherment benchmarks.",
        "local_module": "nw_semitic",
        "is_undeciphered": False,
    },
    {
        "id": "cat-old-hebrew",
        "name": "Old Hebrew (Gen-Prov, consonantal)",
        "language": "Biblical Hebrew",
        "language_family": "Semitic",
        "script_type": "abjad",
        "period": "1000–400 BCE",
        "tokens_approx": 1455,
        "source_url": "https://www.tanakh.us/",
        "license": "Public domain",
        "description": "Consonantal Biblical Hebrew from Genesis and Proverbs. 22-sign abjad. Primary LM for NW Semitic experiments.",
        "local_module": "old_hebrew",
        "is_undeciphered": False,
    },
    {
        "id": "cat-phoenician",
        "name": "Phoenician KAI Inscriptions",
        "language": "Phoenician",
        "language_family": "Semitic",
        "script_type": "abjad",
        "period": "1050–150 BCE",
        "tokens_approx": 5000,
        "source_url": "https://en.wikipedia.org/wiki/Phoenician_alphabet",
        "license": "Public domain",
        "description": "KAI corpus: Ahiram sarcophagus, Mesha Stele, Siloam Inscription, Baal Cycle fragments. 22 signs.",
        "local_module": "phoenician",
        "is_undeciphered": False,
    },
    {
        "id": "cat-linear-b",
        "name": "Linear B / Mycenaean Greek (Pylos tablets)",
        "language": "Mycenaean Greek",
        "language_family": "Indo-European",
        "script_type": "syllabary",
        "period": "1450–1200 BCE",
        "tokens_approx": 9258,
        "source_url": "https://dāmos.hf.uio.no/",
        "license": "Academic use",
        "description": "Ventris-deciphered Bronze Age Greek syllabary. 87 syllabic signs. Pylos PY administrative tablets.",
        "local_module": "linear_b_language",
        "is_undeciphered": False,
    },
    {
        "id": "cat-geez",
        "name": "Ge'ez Genesis (Ethiopic syllabic, Dr. Fuls)",
        "language": "Ge'ez / Classical Ethiopic",
        "language_family": "Semitic",
        "script_type": "syllabary",
        "period": "4th century CE – present",
        "tokens_approx": 85699,
        "source_url": "https://en.wikipedia.org/wiki/Ge%CA%BDez_script",
        "license": "Provided by Dr. Andreas Fuls",
        "description": "Syllabic Ethiopic corpus from the Book of Genesis. 153 syllabic signs. Primary self-decipherment benchmark.",
        "local_module": "geez",
        "is_undeciphered": False,
    },
    {
        "id": "cat-sumerian",
        "name": "Sumerian Ur III (CDLI statistics)",
        "language": "Sumerian",
        "language_family": "Language isolate",
        "script_type": "logosyllabic",
        "period": "2112–2004 BCE",
        "tokens_approx": 39287,
        "source_url": "https://cdli.mpiwg-berlin.mpg.de/",
        "license": "CDLI open data",
        "description": "Ur III administrative tablets from CDLI. Logosyllabic cuneiform. Tier 3 decipherment benchmark.",
        "local_module": "sumerian_ur3",
        "is_undeciphered": False,
    },
    {
        "id": "cat-coptic",
        "name": "Coptic Reference Corpus (Meroitic comparison)",
        "language": "Coptic",
        "language_family": "Afro-Asiatic",
        "script_type": "abjad",
        "period": "2nd–17th century CE",
        "tokens_approx": 537,
        "source_url": "https://en.wikipedia.org/wiki/Coptic_language",
        "license": "Public domain",
        "description": "Coptic reference corpus used as LM for Meroitic decipherment benchmarks. Closest deciphered relative to Meroitic.",
        "local_module": "meroitic",   # get_coptic_symbols() is in the meroitic module
        "is_undeciphered": False,
    },
    {
        "id": "cat-egyptian",
        "name": "Egyptian Hieroglyphic (Middle Egyptian)",
        "language": "Egyptian",
        "language_family": "Afro-Asiatic",
        "script_type": "logosyllabic",
        "period": "2000–1350 BCE",
        "tokens_approx": 50000,
        "source_url": "https://www.egyptianhieroglyphs.net/",
        "license": "Academic use",
        "description": "Middle Egyptian hieroglyphic text corpus. ~700 hieroglyphs. Reference system for logosyllabic comparison.",
        "local_module": "",
        "is_undeciphered": False,
    },
    {
        "id": "cat-akkadian",
        "name": "Akkadian Cuneiform (Old Babylonian)",
        "language": "Akkadian",
        "language_family": "Semitic",
        "script_type": "logosyllabic",
        "period": "2350–600 BCE",
        "tokens_approx": 40000,
        "source_url": "https://cdli.mpiwg-berlin.mpg.de/",
        "license": "CDLI open data",
        "description": "Akkadian Old Babylonian tablets from CDLI. Semitic logosyllabic cuneiform. Comparator for Sumerian Tier 3.",
        "local_module": "",
        "is_undeciphered": False,
    },
    {
        "id": "cat-hittite",
        "name": "Hittite Cuneiform (KBo corpus)",
        "language": "Hittite",
        "language_family": "Indo-European",
        "script_type": "logosyllabic",
        "period": "1650–1200 BCE",
        "tokens_approx": 30000,
        "source_url": "https://www.hethport.uni-wuerzburg.de/",
        "license": "Academic use (Hethitologie Portal)",
        "description": "Hittite cuneiform tablets from KBo corpus. Oldest attested Indo-European language. Anatolian language family.",
        "local_module": "",
        "is_undeciphered": False,
    },
    {
        "id": "cat-greek",
        "name": "Ancient Greek (Homer, Iliad)",
        "language": "Ancient Greek",
        "language_family": "Indo-European",
        "script_type": "alphabet",
        "period": "800–400 BCE",
        "tokens_approx": 100000,
        "source_url": "https://www.perseus.tufts.edu/",
        "license": "Public domain (Perseus Digital Library)",
        "description": "Homeric Greek from the Iliad and Odyssey. 24-letter Greek alphabet. Indo-European reference corpus.",
        "local_module": "",
        "is_undeciphered": False,
    },
    {
        "id": "cat-latin",
        "name": "Classical Latin (Caesar, Cicero, Virgil)",
        "language": "Latin",
        "language_family": "Indo-European",
        "script_type": "alphabet",
        "period": "100 BCE – 100 CE",
        "tokens_approx": 200000,
        "source_url": "https://www.perseus.tufts.edu/",
        "license": "Public domain (Perseus Digital Library)",
        "description": "Classical Latin prose and poetry corpus from Caesar, Cicero, and Virgil. 23-letter Latin alphabet.",
        "local_module": "",
        "is_undeciphered": False,
    },
    {
        "id": "cat-old-chinese",
        "name": "Oracle Bone Script (Shang dynasty)",
        "language": "Old Chinese",
        "language_family": "Sino-Tibetan",
        "script_type": "logographic",
        "period": "1250–1046 BCE",
        "tokens_approx": 15000,
        "source_url": "https://hd.yifat.com/oracle/",
        "license": "Academic use",
        "description": "Chinese oracle bone inscriptions from the Shang dynasty. ~4,000 distinct signs (1,200 deciphered). Logographic.",
        "local_module": "",
        "is_undeciphered": False,
    },
    {
        "id": "cat-sanskrit",
        "name": "Sanskrit (Rigveda, Devanagari transliteration)",
        "language": "Sanskrit",
        "language_family": "Indo-European",
        "script_type": "syllabary",
        "period": "1500 BCE – 500 CE",
        "tokens_approx": 728000,
        "source_url": "https://sanskritdocuments.org/doc_veda/",
        "license": "Academic use (Vedic Tradition / Detlef Eichler via sanskritdocuments.org)",
        "description": (
            "Complete Rigveda all 10 mandalas in ITRANS-simplified Roman transliteration. "
            "728K character tokens from Aufrecht/van Nooten/Holland Samhita edition. "
            "Simplified bigram LM for Indus Script A/B hypothesis test (Dravidian vs Sanskrit)."
        ),
        "local_module": "sanskrit",
        "is_undeciphered": False,
    },

    # ── Additional Indus corpus sources (no bundled module — link only) ─────────
    {
        "id": "cat-indus-cisi",
        "name": "Indus Script (CISI corpus — Parpola 1987)",
        "language": "Unknown",
        "language_family": "Undeciphered",
        "script_type": "unknown",
        "period": "2600–1900 BCE",
        "tokens_approx": 30000,
        "source_url": "https://www.harappa.com/script/indus-script-sign-concordance",
        "license": "Academic use (Parpola et al.)",
        "description": (
            "Corpus of Indus Signs and Inscriptions (CISI) by Asko Parpola, Seppo Koskenniemi, "
            "Simo Parpola and Pentti Aalto (1987–1996). 3 volumes covering most known inscriptions. "
            "Larger than the Mahadevan 1977 corpus. Download from Harappa.com or contact "
            "the Finnish Oriental Society. See also: Wells (2011) for a digitized subset."
        ),
        "local_module": "",
        "is_undeciphered": True,
    },
    {
        "id": "cat-indus-yadav",
        "name": "Indus Script (Yadav et al. 2010 — TIFR corpus)",
        "language": "Unknown",
        "language_family": "Undeciphered",
        "script_type": "unknown",
        "period": "2600–1900 BCE",
        "tokens_approx": 14000,
        "source_url": "https://www.tifr.res.in/~mayank/indus.html",
        "license": "Academic use (TIFR)",
        "description": (
            "Indus corpus used by Yadav, Vahia, Mahadevan and Joglekar (2010) for the "
            "block entropy analysis (Science 2009 paper). Subset of the Mahadevan 1977 corpus "
            "with ~7,000 sign occurrences. Available via the TIFR Astrophysics group website. "
            "Rao et al. 2009 PNAS Markov model paper used the same corpus."
        ),
        "local_module": "",
        "is_undeciphered": True,
    },
    {
        "id": "cat-indus-wells",
        "name": "Indus Script (Wells 2011 — Sign Catalogue)",
        "language": "Unknown",
        "language_family": "Undeciphered",
        "script_type": "unknown",
        "period": "2600–1900 BCE",
        "tokens_approx": 25000,
        "source_url": "https://archaeopress.com/ArchaeopressShop/Public/displayProductDetail.asp?id={B4C0FE13-FF56-401E-9E28-3D9B21AD2EF0}",
        "license": "Academic use (Archaeopress)",
        "description": (
            "B.K. Wells (2011) \"The Archaeology and Epigraphy of Indus Writing.\" "
            "Systematic sign catalogue with digitized inscription sequences. "
            "One of the most complete modern catalogues. Contact Archaeopress or "
            "use the partial digital release at the Harappa.com archive."
        ),
        "local_module": "",
        "is_undeciphered": True,
    },
    {
        "id": "cat-indus-kenoyer",
        "name": "Indus Script (Harappa.com digital archive)",
        "language": "Unknown",
        "language_family": "Undeciphered",
        "script_type": "unknown",
        "period": "2600–1900 BCE",
        "tokens_approx": 5000,
        "source_url": "https://www.harappa.com/script/",
        "license": "Academic use (Harappa.com)",
        "description": (
            "J.M. Kenoyer\'s Harappa.com digital archive of Indus seals and tablet images. "
            "Partial corpus of ~700 photographed objects with sign readings. "
            "Not as comprehensive as CISI but freely browsable online. "
            "Best source for high-resolution seal images with context."
        ),
        "local_module": "",
        "is_undeciphered": True,
    },

    # ── Modern typological comparators ─────────────────────────────────────────
    {
        "id": "cat-arabic",
        "name": "Modern Standard Arabic (news corpus)",
        "language": "Arabic",
        "language_family": "Semitic",
        "script_type": "abjad",
        "period": "Modern",
        "tokens_approx": 500000,
        "source_url": "https://opus.nlpl.eu/",
        "license": "CC BY (OPUS)",
        "description": "Modern Standard Arabic abjad. RTL. 28 consonantal signs. Typological comparator for Semitic studies.",
        "local_module": "",
        "is_undeciphered": False,
    },
    {
        "id": "cat-english",
        "name": "English (Brown Corpus)",
        "language": "English",
        "language_family": "Indo-European",
        "script_type": "alphabet",
        "period": "Modern",
        "tokens_approx": 1000000,
        "source_url": "https://en.wikipedia.org/wiki/Brown_Corpus",
        "license": "Academic use",
        "description": "English Brown Corpus. 26-letter Latin alphabet. Benchmark for entropy and Zipf analysis.",
        "local_module": "",
        "is_undeciphered": False,
    },
    {
        "id": "cat-mandarin",
        "name": "Mandarin Chinese (CC-CEDICT)",
        "language": "Mandarin Chinese",
        "language_family": "Sino-Tibetan",
        "script_type": "logographic",
        "period": "Modern",
        "tokens_approx": 80000,
        "source_url": "https://cc-cedict.org/",
        "license": "CC BY-SA",
        "description": "Mandarin Chinese characters. ~50,000 distinct characters in use; high-entropy logographic system.",
        "local_module": "",
        "is_undeciphered": False,
    },
    {
        "id": "cat-hindi",
        "name": "Hindi (Devanagari, news corpus)",
        "language": "Hindi",
        "language_family": "Indo-European",
        "script_type": "syllabary",
        "period": "Modern",
        "tokens_approx": 300000,
        "source_url": "https://opus.nlpl.eu/",
        "license": "CC BY (OPUS)",
        "description": "Hindi in Devanagari script. 48 primary characters. Syllabic (abugida) typological comparator.",
        "local_module": "",
        "is_undeciphered": False,
    },
    {
        "id": "cat-japanese",
        "name": "Japanese (Hiragana corpus)",
        "language": "Japanese",
        "language_family": "Japonic",
        "script_type": "syllabary",
        "period": "Modern",
        "tokens_approx": 200000,
        "source_url": "https://opus.nlpl.eu/",
        "license": "CC BY (OPUS)",
        "description": "Japanese Hiragana syllabary. 46 base characters. Phonetically transparent syllabic system.",
        "local_module": "",
        "is_undeciphered": False,
    },
    {
        "id": "cat-korean",
        "name": "Korean (Hangul corpus)",
        "language": "Korean",
        "language_family": "Koreanic",
        "script_type": "alphabet",
        "period": "Modern",
        "tokens_approx": 200000,
        "source_url": "https://opus.nlpl.eu/",
        "license": "CC BY (OPUS)",
        "description": "Korean Hangul. Featural alphabet, 24 basic jamo. High-entropy typological comparator.",
        "local_module": "",
        "is_undeciphered": False,
    },
    {
        "id": "cat-finnish",
        "name": "Finnish (FiWaC corpus)",
        "language": "Finnish",
        "language_family": "Uralic",
        "script_type": "alphabet",
        "period": "Modern",
        "tokens_approx": 300000,
        "source_url": "https://opus.nlpl.eu/",
        "license": "CC BY (OPUS)",
        "description": "Finnish. Agglutinative language, Latin alphabet. Low type-token ratio; reference for information density studies.",
        "local_module": "",
        "is_undeciphered": False,
    },
    {
        "id": "cat-turkish",
        "name": "Turkish (news corpus)",
        "language": "Turkish",
        "language_family": "Turkic",
        "script_type": "alphabet",
        "period": "Modern",
        "tokens_approx": 300000,
        "source_url": "https://opus.nlpl.eu/",
        "license": "CC BY (OPUS)",
        "description": "Turkish. Agglutinative, Latin alphabet with dotless-i. SOV word order. Typological comparator.",
        "local_module": "",
        "is_undeciphered": False,
    },
    {
        "id": "cat-swahili",
        "name": "Swahili (news corpus)",
        "language": "Swahili",
        "language_family": "Niger-Congo",
        "script_type": "alphabet",
        "period": "Modern",
        "tokens_approx": 200000,
        "source_url": "https://opus.nlpl.eu/",
        "license": "CC BY (OPUS)",
        "description": "Swahili Bantu language, Latin script. Agglutinative. Sub-Saharan African reference corpus.",
        "local_module": "",
        "is_undeciphered": False,
    },
    {
        "id": "cat-basque",
        "name": "Basque (Elhuyar corpus)",
        "language": "Basque",
        "language_family": "Language isolate",
        "script_type": "alphabet",
        "period": "Modern",
        "tokens_approx": 100000,
        "source_url": "https://opus.nlpl.eu/",
        "license": "CC BY (OPUS)",
        "description": "Basque. Language isolate (no known relatives). Latin script. Reference for language isolate studies alongside Sumerian.",
        "local_module": "",
        "is_undeciphered": False,
    },
    {
        "id": "cat-tamil",
        "name": "Tamil/Dravidian (classical corpus)",
        "language": "Tamil",
        "language_family": "Dravidian",
        "script_type": "syllabary",
        "period": "300 BCE – present",
        "tokens_approx": 18500,
        "source_url": "https://www.tamildigitallibrary.in/",
        "license": "Public domain",
        "description": "Classical Tamil in Romanized transliteration: Tirukkural (∼300 BCE), Sangam poetry (Akananuru, Purananuru), and Dravidian phonotactic text. Expanded Tier 5 LM for Indus Script Dravidian hypothesis testing.",
        "local_module": "dravidian",
        "is_undeciphered": False,
    },
    {
        "id": "cat-syriac",
        "name": "Classical Syriac (Peshitta)",
        "language": "Syriac",
        "language_family": "Semitic",
        "script_type": "abjad",
        "period": "1st–13th century CE",
        "tokens_approx": 80000,
        "source_url": "https://syriaccorpus.org/",
        "license": "Academic use",
        "description": "Classical Syriac from the Peshitta Bible. 22 Aramaic-derived consonants, RTL. Comparator for NW Semitic.",
        "local_module": "",
        "is_undeciphered": False,
    },
    {
        "id": "cat-russian",
        "name": "Russian (Cyrillic, news corpus)",
        "language": "Russian",
        "language_family": "Indo-European",
        "script_type": "alphabet",
        "period": "Modern",
        "tokens_approx": 500000,
        "source_url": "https://opus.nlpl.eu/",
        "license": "CC BY (OPUS)",
        "description": "Russian in Cyrillic script. 33 characters. Slavic Indo-European comparator for alphabetic entropy analysis.",
        "local_module": "",
        "is_undeciphered": False,
    },
    {
        "id": "cat-old-persian",
        "name": "Old Persian Cuneiform (Achaemenid inscriptions)",
        "language": "Old Persian",
        "language_family": "Indo-European",
        "script_type": "syllabary",
        "period": "522–330 BCE",
        "tokens_approx": 10000,
        "source_url": "https://www.livius.org/sources/content/achaemenid-royal-inscriptions/",
        "license": "Public domain",
        "description": "Achaemenid royal inscriptions. 41 signs (semi-alphabetic cuneiform). Deciphered via Behistun trilingual.",
        "local_module": "",
        "is_undeciphered": False,
    },
]


# ── Reading direction for every catalogue entry ────────────────────────────────
# ltr = left-to-right, rtl = right-to-left, bidi = boustrophedon/alternating,
# unknown = direction uncertain or not applicable (logographic vertical etc.)
READING_DIRECTIONS: dict[str, str] = {
    # Undeciphered — Indus direction is debated (possibly RTL or boustrophedon)
    "cat-indus":          "unknown",   # Indus: RTL and boustrophedon both proposed
    "cat-linear-a":       "ltr",       # Linear A tablets: left-to-right
    "cat-proto-sinaitic": "rtl",       # Ancestor of Semitic abjads; RTL
    "cat-meroitic":       "ltr",       # Meroitic: left-to-right
    "cat-rongorongo":     "bidi",      # Boustrophedon (alternating)
    "cat-zapotec":        "ltr",       # Columnar / LTR horizontal
    "cat-voynich":        "ltr",       # Appears left-to-right
    # Deciphered ancient — Semitic abjads are RTL
    "cat-ugaritic":       "rtl",
    "cat-old-hebrew":     "rtl",
    "cat-phoenician":     "rtl",
    "cat-linear-b":       "ltr",
    "cat-geez":           "ltr",
    "cat-sumerian":       "ltr",       # Cuneiform LTR
    "cat-coptic":         "ltr",
    "cat-egyptian":       "ltr",       # Standard horizontal Egyptian is LTR
    "cat-akkadian":       "ltr",       # Cuneiform LTR
    "cat-hittite":        "ltr",       # Cuneiform LTR
    "cat-greek":          "ltr",
    "cat-latin":          "ltr",
    "cat-old-chinese":    "ltr",       # Oracle bone: vertical columns but horizontal LTR
    "cat-sanskrit":       "ltr",       # Devanagari LTR
    # Additional Indus sources
    "cat-indus-cisi":     "unknown",
    "cat-indus-yadav":    "unknown",
    "cat-indus-wells":    "unknown",
    "cat-indus-kenoyer":  "unknown",
    # Modern
    "cat-arabic":         "rtl",
    "cat-english":        "ltr",
    "cat-mandarin":       "ltr",       # Horizontal modern Chinese is LTR
    "cat-hindi":          "ltr",       # Devanagari LTR
    "cat-japanese":       "ltr",       # Horizontal Japanese is LTR
    "cat-korean":         "ltr",
    "cat-finnish":        "ltr",
    "cat-turkish":        "ltr",
    "cat-swahili":        "ltr",
    "cat-basque":         "ltr",
    "cat-tamil":          "ltr",
    "cat-syriac":         "rtl",
    "cat-russian":        "ltr",
    "cat-old-persian":    "ltr",       # Cuneiform LTR
}


async def seed_corpus_catalogue() -> int:
    """Seed the corpus_catalogue table from the CATALOGUE list.

    Upserts all entries (idempotent on repeated startup).  Also runs an
    explicit UPDATE pass for any rows where tokens_approx = 0 (can happen
    when the table was first seeded before token counts were added to the
    CATALOGUE dict, since SQLite DEFAULT 0 fills the column on the first
    INSERT if the column wasn't present in older code).
    Returns the number of entries processed.
    """
    from glossa_lab.database import get_db  # noqa: PLC0415
    db = get_db()
    if db is None:
        logger.warning("corpus_catalogue_seeder: database not available, skipping seed")
        return 0

    assert db._conn  # noqa: SLF001
    count = 0
    for entry in CATALOGUE:
        try:
            # Inject reading_direction from the lookup table if not already set
            enriched = dict(entry)
            enriched.setdefault("reading_direction", READING_DIRECTIONS.get(entry["id"], "unknown"))
            await db.upsert_corpus_catalogue_entry(enriched)
            count += 1
        except Exception as exc:  # noqa: BLE001
            logger.warning("Failed to seed catalogue entry '%s': %s", entry.get("id"), exc)

    # Explicit fix-up: if any rows still have tokens_approx = 0 (legacy DB),
    # force-update them from the CATALOGUE dict values.
    try:
        fixed = 0
        for entry in CATALOGUE:
            tokens = entry.get("tokens_approx", 0)
            if tokens > 0:
                await db._conn.execute(  # noqa: SLF001
                    "UPDATE corpus_catalogue SET tokens_approx = ? WHERE id = ? AND tokens_approx = 0",
                    (tokens, entry["id"]),
                )
                # rowcount not easily accessible on aiosqlite; just commit all
        await db._conn.commit()
        # Also ensure description, source_url, and reading_direction are fresh
        for entry in CATALOGUE:
            rd = READING_DIRECTIONS.get(entry["id"], "unknown")
            await db._conn.execute(
                "UPDATE corpus_catalogue SET description = ?, source_url = ?, tokens_approx = ?, reading_direction = ? WHERE id = ?",
                (entry.get("description", ""), entry.get("source_url", ""),
                 entry.get("tokens_approx", 0), rd, entry["id"]),
            )
        await db._conn.commit()
        logger.debug("Corpus catalogue token fixup complete")
    except Exception as exc:  # noqa: BLE001
        logger.warning("Corpus catalogue token fixup failed: %s", exc)

    logger.info("Corpus catalogue seeded: %d entries", count)
    return count
