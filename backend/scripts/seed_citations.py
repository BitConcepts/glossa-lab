"""Seed the Citation Manager (citations table in DB) with all known research citations.

Sources:
  1. Evidence Graph papers (16 registered docs) — with correct bibliographic data
  2. Key CITATIONS.md entries (corpus and methodology references)

Run:
    python backend/scripts/seed_citations.py
"""
from __future__ import annotations

import asyncio
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).parents[2]
sys.path.insert(0, str(REPO / "backend"))

# ── Curated citation data ──────────────────────────────────────────────────
# Format: key, title, authors, year, venue, doi, url, notes
CITATIONS: list[dict] = [

    # ── Evidence Graph Papers ──────────────────────────────────────────────

    {
        "key": "farmer_sproat_witzel_2004",
        "title": "The Collapse of the Indus-Script Thesis: The Myth of a Literate Harappan Civilization",
        "authors": "Farmer, S.; Sproat, R.; Witzel, M.",
        "year": "2004",
        "venue": "Electronic Journal of Vedic Studies (EJVS) 11(2)",
        "doi": "",
        "url": "https://www.ejvs.laurasianacademy.com/ejvs1102/ejvs1102article.pdf",
        "notes": "Non-linguistic hypothesis for Indus signs. Contradicted by Phase-43 positional structure evidence.",
    },
    {
        "key": "rao_2009_pnas_markov",
        "title": "A Markov Model of the Indus Script",
        "authors": "Rao, R.P.N.; Yadav, N.; Vahia, M.N.; Joglekar, H.; Adhikari, R.; Mahadevan, I.",
        "year": "2009",
        "venue": "Proceedings of the National Academy of Sciences (PNAS) 106(33)",
        "doi": "10.1073/pnas.0906237106",
        "url": "https://www.pnas.org/doi/10.1073/pnas.0906237106",
        "notes": "First-order Markov model. Shows conditional entropy in linguistic range. Supports linguistic hypothesis.",
    },
    {
        "key": "rao_2009_science_entropic",
        "title": "Entropic Evidence for Linguistic Structure in the Indus Script",
        "authors": "Rao, R.P.N.; Yadav, N.; Vahia, M.N.; Joglekar, H.; Adhikari, R.; Mahadevan, I.",
        "year": "2009",
        "venue": "Science 324(5931): 1165",
        "doi": "10.1126/science.1170391",
        "url": "https://science.sciencemag.org/content/324/5931/1165",
        "notes": "Conditional entropy analysis. Definitively places Indus script in linguistic range vs random/rigid systems.",
    },
    {
        "key": "yadav_2009_arxiv",
        "title": "Statistical Analysis of the Indus Script",
        "authors": "Yadav, N.; Joglekar, H.; Rao, R.P.N.; Vahia, M.N.; Adhikari, R.; Mahadevan, I.",
        "year": "2009",
        "venue": "arXiv cs.CL 0901.3017",
        "doi": "",
        "url": "https://arxiv.org/abs/0901.3017",
        "notes": "N-gram statistical analysis. Sign frequency follows Zipf-Mandelbrot. Confirms linguistic structure.",
    },
    {
        "key": "yadav_2010_ngrams",
        "title": "Statistical Analysis of the Indus Script Using n-Grams",
        "authors": "Yadav, N.; Joglekar, H.; Rao, R.P.N.; Vahia, M.N.; Adhikari, R.; Mahadevan, I.",
        "year": "2010",
        "venue": "PLOS ONE 5(3): e9506",
        "doi": "10.1371/journal.pone.0009506",
        "url": "https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0009506",
        "notes": "Full n-gram study. Confirms Zipf-Mandelbrot, text-beginner/ender signs, bigram correlations.",
    },
    {
        "key": "parpola_2010_dravidian_solution",
        "title": "A Dravidian Solution to the Indus Script Problem",
        "authors": "Parpola, A.",
        "year": "2010",
        "venue": "World Archaeology Congress 6, Dublin",
        "doi": "",
        "url": "",
        "notes": "Fish-sign rebus approach. meen (fish/star) as phonetic core. Proto-Dravidian language hypothesis.",
    },
    {
        "key": "sinha_2010_network_arxiv",
        "title": "Network Analysis of a Corpus of Undeciphered Inscriptions Indicates Syntactic Organization",
        "authors": "Sinha, S.; Izhar, A.M.; Pan, R.K.; Wells, B.K.",
        "year": "2010",
        "venue": "arXiv cond-mat 1005.4997",
        "doi": "",
        "url": "https://arxiv.org/abs/1005.4997",
        "notes": "Network/graph analysis shows recursive syntactic structures. Supports linguistic interpretation.",
    },
    {
        "key": "mahadevan_2009_signs",
        "title": "The Indus Non-Linear Script",
        "authors": "Mahadevan, I.",
        "year": "2009",
        "venue": "Antiquity 83(320)",
        "doi": "",
        "url": "",
        "notes": "Response to Farmer et al. Defends linguistic interpretation. Discusses sign frequencies.",
    },
    {
        "key": "roif_indus_ledger",
        "title": "Indus Valley Script Deciphered: From Mythology to History using the Akkadian Shorthand Approach",
        "authors": "Roif, A.",
        "year": "",
        "venue": "Academia.edu",
        "doi": "",
        "url": "https://www.academia.edu/",
        "notes": "Trade-ledger / Akkadian shorthand model. Economic/guild interpretation. Fish sign = coastal trader. PARTIALLY FALSIFIED by our coastal enrichment analysis.",
    },
    {
        "key": "hunt_without_kings",
        "title": "Without Kings or Conquests: The Indus Script and Civic-Ritual Governance",
        "authors": "Hunt, T.A.",
        "year": "2025",
        "venue": "Independent publication",
        "doi": "",
        "url": "",
        "notes": "Tripartite grammar model. Prefix (faunal/identity) + medial (action) + suffix (celestial/cycle). Phase-43: formula_rate=35.5%, 59× lift. STRUCTURALLY SUPPORTED.",
    },
    {
        "key": "wells_2015_archaeology_epigraphy",
        "title": "The Archaeology and Epigraphy of Indus Writing",
        "authors": "Wells, B.K.",
        "year": "2015",
        "venue": "Archaeopress, Oxford. ISBN 9781784910464",
        "doi": "",
        "url": "https://archaeopress.com",
        "notes": "Comprehensive Indus script analysis. 17 signs identified with confidence. Dravidian syntax match (Ch. 6). Fuls appendices: NWSP method, sign classification, writing system comparison.",
    },
    {
        "key": "fuls_2013_positional_analysis",
        "title": "Positional Analysis of Indus Signs",
        "authors": "Fuls, A.",
        "year": "2013",
        "venue": "Epigrafika, Vol. 7(1): 253–275",
        "doi": "",
        "url": "https://www.academia.edu/6710518/Positional_Analysis_of_Indus_Signs",
        "notes": "NWSP (Normalised Weighted Sign Position) method. Classifies all signs as initial/terminal/medial. Foundation for Phase-45 T1 crosscheck.",
    },
    {
        "key": "fuls_2020_ancient_writing",
        "title": "Ancient Writing and Modern Technologies: Structural Analysis of Numerical Indus Inscriptions",
        "authors": "Fuls, A.",
        "year": "2020",
        "venue": "Studies on Indus Script, National Fund for Mohenjodaro: 57–90",
        "doi": "",
        "url": "https://www.academia.edu/41952485",
        "notes": "Multivariate segmentation method. ICIT corpus 5318 texts. Logographic-syllabic classification. Right-to-left reading direction.",
    },
    {
        "key": "fuls_2023_corpus_indus",
        "title": "Corpus of Indus Inscriptions (Mathematica Epigraphica vol. 3)",
        "authors": "Fuls, A.",
        "year": "2022",
        "venue": "Independently published, Berlin. ISBN 978-1-671-80486-4",
        "doi": "",
        "url": "https://www.amazon.com/dp/1671804864/",
        "notes": "5500+ texts from all sites. ICIT numbering system. Nearest open-access equivalent to full ICIT corpus.",
    },
    {
        "key": "fuls_2023_catalog_signs",
        "title": "A Catalog of Indus Signs (Mathematica Epigraphica vol. 4)",
        "authors": "Fuls, A.",
        "year": "2023",
        "venue": "Independently published, Berlin. ISBN 979-8-398-42230-6",
        "doi": "",
        "url": "https://www.researchgate.net/publication/373522673_A_Catalog_of_Indus_Signs",
        "notes": "700+ signs with positional stats. Entropic redundancy method. Sign-list for Glossa Lab sign crosswalk.",
    },

    # ── Key Research Data Citations (from CITATIONS.md) ───────────────────

    {
        "key": "mahadevan_1977_concordance",
        "title": "The Indus Script: Texts, Concordance and Tables",
        "authors": "Mahadevan, I.",
        "year": "1977",
        "venue": "ASI Memoirs 77, Archaeological Survey of India",
        "doi": "",
        "url": "",
        "notes": "M77 concordance. 417 unique signs in 3573 lines / 2906 texts. Foundation corpus for all statistical studies.",
    },
    {
        "key": "holdat_indus_corpus",
        "title": "Holdat LLC Indus Corpus",
        "authors": "Holdat LLC",
        "year": "2024",
        "venue": "Dataset: indus_corpus 2.csv + all_symbol_semantic_roles 2.csv",
        "doi": "",
        "url": "https://holdatllc.com",
        "notes": "1670 seals, 7002 tokens, 390 signs. With semantic roles (CLASSIFIER_PREFIX, CASE_MARKER_SUFFIX). Primary corpus for Glossa Lab SA experiments.",
    },
    {
        "key": "parpola_1994_deciphering",
        "title": "Deciphering the Indus Script",
        "authors": "Parpola, A.",
        "year": "1994",
        "venue": "Cambridge University Press",
        "doi": "",
        "url": "",
        "notes": "Standard reference. P-number sign system. Phoneme map for iconographic anchors.",
    },
    {
        "key": "mahadevan_parpola_crosswalk",
        "title": "M↔P Sign Crosswalk (Glossa Lab internal)",
        "authors": "Pierson, T. / Glossa Lab",
        "year": "2024",
        "venue": "backend/glossa_lab/data/mahadevan_parpola_crosswalk_v2.json",
        "doi": "",
        "url": "",
        "notes": "38 HIGH/MEDIUM confidence M↔P sign mappings. Used for fish sign identification (M047=P47=mīn).",
    },
    {
        "key": "dedr_burrow_emeneau",
        "title": "A Dravidian Etymological Dictionary (2nd ed.)",
        "authors": "Burrow, T.; Emeneau, M.B.",
        "year": "1984",
        "venue": "Oxford University Press",
        "doi": "",
        "url": "",
        "notes": "DEDR. Primary source for Dravidian phoneme matching. Phase-44 T2: kol/koḷ (DEDR 2173/2174) for M099.",
    },
    {
        "key": "tamiltb_v01",
        "title": "TamilTB v0.1: Tamil TreeBank",
        "authors": "Tamil TreeBank project",
        "year": "2012",
        "venue": "CC-SA 3.0. via Kee2u_Indus_Decipherment repository",
        "doi": "",
        "url": "https://github.com/Kee2u/Indus_Decipherment",
        "notes": "3489 morphologically annotated Tamil words. Used to expand Dravidian LM from 184→944 bigrams in Phase-44.",
    },
    {
        "key": "tamburini_2025_csa",
        "title": "Automatic Decipherment of Ancient Scripts Using Coupled Simulated Annealing",
        "authors": "Tamburini, F.",
        "year": "2025",
        "venue": "Frontiers in AI",
        "doi": "10.3389/frai.2025.1581129",
        "url": "https://doi.org/10.3389/frai.2025.1581129",
        "notes": "CSA (Coupled Simulated Annealing) for script decipherment. k-permutations. Used in Phase-37 CSA experiments.",
    },
    {
        "key": "fuls_email_contact",
        "title": "Correspondence: Dr. Andreas Fuls (TU Berlin / ICIT)",
        "authors": "Fuls, A.",
        "year": "2026",
        "venue": "Direct correspondence",
        "doi": "",
        "url": "https://www.user.tu-berlin.de/fuls/",
        "notes": "ICIT database access request. Phase-38 T1 Dravidian 1.056× advantage result shared. Email sent 2026-05-11.",
    },
]


async def seed() -> None:
    from glossa_lab.config import get_settings
    from glossa_lab.database import close_db, init_db

    settings = get_settings()
    db = await init_db(settings.data_dir)
    now = datetime.now(timezone.utc).isoformat()

    # Check existing
    existing = await db.list_citations()
    existing_keys = {c["key"] for c in existing}
    print(f"Existing citations: {len(existing)}")

    created = 0
    skipped = 0
    for c in CITATIONS:
        if c["key"] in existing_keys:
            skipped += 1
            continue
        await db.create_citation(
            key=c["key"],
            title=c["title"],
            authors=c["authors"],
            year=c["year"],
            venue=c["venue"],
            doi=c["doi"],
            url=c["url"],
            notes=c["notes"],
            created_at=now,
        )
        created += 1
        print(f"  ✓ {c['key']}: {c['title'][:60]}")

    print(f"\nDone: {created} created, {skipped} already existed")
    total = await db.list_citations()
    print(f"Total citations in DB: {len(total)}")
    await close_db()


if __name__ == "__main__":
    asyncio.run(seed())
