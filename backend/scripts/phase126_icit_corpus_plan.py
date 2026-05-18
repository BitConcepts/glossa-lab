"""Phase-126: ICIT Corpus Building Plan & Access Strategy.

The Interactive Corpus of Indus Texts (ICIT) is maintained by Dr. Andreas Fuls
(fuls@epigraphica.de) — the same scholar we've been corresponding with.

ICIT contains:
  - 4,537 inscribed objects
  - 5,509 texts
  - 19,616 sign occurrences
  - Gulf sites: Failaka (Kuwait), Saar (Bahrain), Janabiyah (Bahrain)
  - Uses Wells 3-digit sign codes (different from Holdat M-numbers)

The Gulf assemblages are critical for Avishai's fish-sign polysemy test:
  - Failaka ~400 circular stamp seals, ca. 2000 BCE
  - Saar 200+ seals and sealings (Crawford 1997)
  - Janabiyah (Bahrain) — already in our Phase-46 analysis

CPU only. Output: reports/phase126_icit_corpus_plan.json
"""
from __future__ import annotations
import json, os, sys
from datetime import datetime
from pathlib import Path

REPO    = Path(__file__).parents[2]
REPORTS = REPO / "reports"
REPORTS.mkdir(exist_ok=True)
OUT     = REPORTS / "phase126_icit_corpus_plan.json"

sys.path.insert(0, str(REPO / "backend"))
os.environ.setdefault("GLOSSA_DATA_DIR", str(REPO / "backend/data"))


ICIT_SOURCES = {
    "icit_database": {
        "name": "ICIT (Interactive Corpus of Indus Texts)",
        "maintainer": "Dr. Andreas Fuls (fuls@epigraphica.de)",
        "url": "https://www.epigraphica.de/indus/",
        "size": "4,537 objects, 5,509 texts, 19,616 sign occurrences",
        "sign_system": "Wells 3-digit codes (676 signs)",
        "gulf_sites": ["Failaka", "Saar", "Janabiyah", "Dilmun"],
        "access": "Request from Dr. Fuls by email — he's our Phase-109 contact",
        "priority": "HIGH — Dr. Fuls is our primary outreach target",
        "crosswalk_needed": "Wells 3-digit ↔ Mahadevan M-number (partially done in Phase-51/71)",
    },
    "failaka_seals": {
        "name": "Failaka Island seals (Kuwait)",
        "source": "Kjaerum (1983, 1980), Tell F6 excavations (Hojlund 2012)",
        "size": "~400 circular stamp seals, ca. 2000 BCE",
        "relevance": "Dilmun-type seals with Indus inscriptions; maritime trade hub",
        "fish_sign_relevance": "HIGH — coastal/maritime context exactly where isolated fish commodity marks would appear",
        "access": "Published in Kjaerum 1983, Tell F6 in Hojlund 2012 (both available Academia.edu)",
        "download_needed": ["Kjaerum_1983_Failaka_seals.pdf", "Hojlund_2012_TellF6.pdf"],
    },
    "saar_seals": {
        "name": "Saar settlement seals (Bahrain)",
        "source": "Crawford 1997 'Early Dilmun Seals from Saar' (Academia.edu 28086707)",
        "size": "200+ seals and sealings",
        "relevance": "Largest single Bronze Age seal corpus from Bahrain; shows inland vs coastal distribution",
        "fish_sign_relevance": "MEDIUM — Saar is inland Dilmun, not coastal port",
        "access": "Available as free PDF on Academia.edu",
        "download_url": "https://www.academia.edu/28086707/",
    },
    "janabiyah_seal": {
        "name": "Janabiyah contact-zone seal (Bahrain Gulf coast)",
        "source": "Already in our corpus — Phase-46 analysis",
        "relevance": "Has all 7 HIGH anchor signs — key contact-zone artifact",
        "status": "ALREADY ANALYZED in Phase-46",
    },
    "cisi_vol3_gulf": {
        "name": "CISI Vol 3 Gulf material (Parpola)",
        "source": "Already partially ingested via Phase-28 OCR pipeline",
        "relevance": "Contains Gulf assemblage seals in Parpola P-numbering",
        "status": "PARTIALLY DONE — Phase-28 OCR extracted some data",
    },
}

# Strategy for building the corpus
CORPUS_BUILD_STRATEGY = {
    "step_1_icit_request": {
        "action": "Email Dr. Fuls for ICIT data access",
        "email": "fuls@epigraphica.de",
        "template": (
            "Dear Dr. Fuls,\n\n"
            "Following our earlier correspondence (Phase-109 package, May 2026), "
            "we are now specifically working on the fish-sign polysemy question raised "
            "by Avishai Roif (Ben Gurion University). In the Holdat corpus, both M047 "
            "and M001 appear exclusively in compound sequences — no isolated occurrences. "
            "This suggests the commodity-tally usage predicted by the polysemy model "
            "would appear in Gulf assemblages (Failaka, Saar) rather than formal seals.\n\n"
            "Would it be possible to obtain access to the ICIT database, specifically "
            "for the Gulf-site inscriptions? We are particularly interested in:\n"
            "1. Failaka and Saar seal data (sign sequences + site attribution)\n"
            "2. Any isolated single-sign inscriptions at coastal Gulf sites\n"
            "3. Fish-sign (Wells code for M047/M001) occurrence data by site\n\n"
            "We would be happy to share our current decipherment results "
            "(95.7% token coverage, 263 H+M anchors) in exchange.\n\n"
            "Best regards,\nTristen Pierson\nGlossa Lab"
        ),
        "priority": "CRITICAL — this is the fastest path to Gulf corpus data",
    },
    "step_2_failaka_pdfs": {
        "action": "Download Kjaerum 1983 and Tell F6 2012 from Academia.edu",
        "urls": [
            "https://www.academia.edu/126123726/Failaka_Seals_Catalogue_Volume_2",
            "https://www.academia.edu/34669398/Tell_F6_on_Failaka_Island",
        ],
        "then": "OCR sign sequences using Phase-104 Mistral pipeline",
    },
    "step_3_saar_pdf": {
        "action": "Download Crawford 1997 Saar seals from Academia.edu",
        "url": "https://www.academia.edu/28086707/",
        "then": "Extract sign sequences using Mistral OCR",
    },
    "step_4_crosswalk": {
        "action": "Map Wells 3-digit codes to Mahadevan M-numbers",
        "status": "Phase-51/71 did 45/390 entries. ICIT uses Wells codes.",
        "tool": "mahadevan_parpola_crosswalk.json + Wells (2011) Appendix",
    },
    "step_5_integration": {
        "action": "Integrate Gulf corpus into Holdat-compatible format",
        "add_site_field": "Gulf sites: Failaka/Dilmun, Saar/Bahrain, Janabiyah",
        "enables": "Fish-sign isolated vs compound test with Gulf assemblages",
    },
}


def main():
    print("Phase-126: ICIT Corpus Building Plan\n")

    print("  ICIT database (Dr. Fuls) — the critical gap:")
    print(f"    Size: {ICIT_SOURCES['icit_database']['size']}")
    print(f"    Gulf sites: {ICIT_SOURCES['icit_database']['gulf_sites']}")
    print(f"    Access: {ICIT_SOURCES['icit_database']['access']}")

    print("\n  Why ICIT matters for the fish-sign polysemy test:")
    print("    Holdat: 0 isolated fish signs (M047=13 compound, M001=14 compound)")
    print("    ICIT Gulf: ~2000 inscriptions from Gulf sites — likely has solo fish marks")
    print("    Failaka 400 circular seals: maritime hub, different format than Holdat")

    print("\n  Key insight from Martini (2025):")
    print("    Egypt ostracon (sailors' record) = commodity list format")
    print("    Gulf assemblages are closer to ostracon-type records than formal seals")
    print("    Isolated fish signs would be on short Gulf tablets, not formal stamp seals")

    print(f"\n  Draft ICIT access email (to: {ICIT_SOURCES['icit_database']['maintainer']}):")
    print("    " + CORPUS_BUILD_STRATEGY["step_1_icit_request"]["template"][:400] + "...")

    print("\n  Required user downloads:")
    print("    1. https://www.academia.edu/126123726/ (Failaka Vol 2 — 225 pages)")
    print("    2. https://www.academia.edu/34669398/ (Tell F6 Failaka — 270 pages)")
    print("    3. https://www.academia.edu/28086707/ (Saar seals — 56 pages)")

    result = {
        "phase": 126,
        "status": "PLAN",
        "generated_at": datetime.now().isoformat(),
        "icit_sources": ICIT_SOURCES,
        "build_strategy": CORPUS_BUILD_STRATEGY,
        "critical_insight": (
            "ICIT is maintained by Dr. Andreas Fuls — our primary outreach contact. "
            "The fastest path to Gulf corpus data is to request ICIT access from him directly, "
            "citing the fish-sign polysemy question and our existing research relationship. "
            "His email is fuls@epigraphica.de (epigraphica.de/indus/)."
        ),
        "avishai_connection": (
            "The Failaka seals are exactly where Avishai's isolated-fish-commodity hypothesis "
            "would be testable. Failaka was a maritime trading hub (2000 BCE Dilmun) — "
            "the kind of site where short administrative records on perishable media "
            "(now lost) would have existed alongside the circular stamp seals that survived."
        ),
        "user_action_needed": [
            "Download: https://www.academia.edu/126123726/ (Failaka seals Vol 2)",
            "Download: https://www.academia.edu/34669398/ (Tell F6 Failaka)",
            "Download: https://www.academia.edu/28086707/ (Saar seals — Crawford 1997)",
            "Email Dr. Fuls: fuls@epigraphica.de — request ICIT Gulf data access",
            "Download Avishai's other papers: Academia.edu 129921039 and 129046130",
        ],
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n  Saved → {OUT}")
    print("  Phase-126 complete: ICIT access strategy documented")
    return result


if __name__ == "__main__":
    main()
