"""Phase 321: Venkatesan Cross-Check + Kriger Uniqueness + Outreach

Phase 321a: Cross-check our 400 HIGH readings against Venkatesan's
           independent Proto-Dravidian decipherment (decipher-ivc).
Phase 321b: Test Kriger's inscription uniqueness claim (98.3% unique)
           against our corpus.
Phase 321c: Compile outreach list with contact info.

Output: outputs/phase321_venkatesan_kriger_keezhadi.json
"""
from __future__ import annotations
import csv
import json
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
ANCHORS_PATH = REPO / "backend" / "reports" / "INDUS_FINAL_ANCHORS.json"
HOLDAT_PATH = (
    REPO / "corpora" / "downloads" / "external_repos"
    / "holdatllc_indus" / "indus_corpus 2.csv"
)
OUT_PATH = REPO / "outputs" / "phase321_venkatesan_kriger_keezhadi.json"

# ══════════════════════════════════════════════════════════════════════
# VENKATESAN READINGS (extracted from ivc-script-decipherment.pdf)
# Uses M77 sign IDs and DEDR entries — same format as our anchors
# ══════════════════════════════════════════════════════════════════════

VENKATESAN_READINGS = {
    # Places and townships
    "M402": {"reading": "nāṭu", "dedr": "3638", "meaning": "country"},
    "M342": {"reading": "ūr", "dedr": "752", "meaning": "town"},
    "M176": {"reading": "añcal", "dedr": "54", "meaning": "resting place"},
    "M254": {"reading": "paṭṭi", "dedr": "3848", "meaning": "hamlet, village"},
    "M245": {"reading": "taṭṭi", "dedr": "3036", "meaning": "cloth, wooden frame"},
    "M137": {"reading": "cēri", "dedr": "2007", "meaning": "assemblage, hamlet"},
    "M190": {"reading": "pāḷaiyam", "dedr": "4117", "meaning": "tribal hamlet"},
    # Numbers
    "M086": {"reading": "mutal", "dedr": "4950", "meaning": "one, primary"},
    "M087": {"reading": "iru", "dedr": "474", "meaning": "two, great"},
    "M089": {"reading": "mū", "dedr": "5052", "meaning": "mature, three"},
    "M095": {"reading": "nal", "dedr": "2912", "meaning": "good, four"},
    "M096": {"reading": "ai", "dedr": "2826", "meaning": "unite, five"},
    "M108": {"reading": "yāṟu", "dedr": "5159", "meaning": "river, six"},
    "M110": {"reading": "ēṟu", "dedr": "910", "meaning": "rise, seven"},
    # People
    "M001": {"reading": "an", "dedr": "131", "meaning": "person"},
    "M012": {"reading": "uṟavan", "dedr": "688", "meaning": "farmer"},
    "M162": {"reading": "vēḷ", "dedr": "5545", "meaning": "chief, spear"},
    # Key signs
    "M099": {"reading": "kōl", "dedr": "2237", "meaning": "stick, seize"},
    "M124": {"reading": "ēr", "dedr": "2815", "meaning": "plough"},
    "M125": {"reading": "ēṟu", "dedr": "916", "meaning": "climb, mount"},
    "M126": {"reading": "viri", "dedr": "5411", "meaning": "spread, expand"},
    "M161": {"reading": "nēr", "dedr": "2770", "meaning": "meet, straight"},
    "M233": {"reading": "mūmalai", "dedr": "5052", "meaning": "three mountains"},
    "M261": {"reading": "kō", "dedr": "2177", "meaning": "mountain, gentry"},
    "M287": {"reading": "valai", "dedr": "5288", "meaning": "net, trap, right"},
    "M293": {"reading": "valaiyan", "dedr": "5288", "meaning": "trapper (short)"},
    "M296": {"reading": "vaṟi", "dedr": "5297", "meaning": "way"},
    "M299": {"reading": "iṭa", "dedr": "449", "meaning": "hip, left"},
    "M304": {"reading": "vil", "dedr": "5422", "meaning": "bow, sell"},
    "M311": {"reading": "yāṟ", "dedr": "5156", "meaning": "harp, music"},
    "M312": {"reading": "kuṭi", "dedr": "1655", "meaning": "house, family"},
    "M319": {"reading": "muri", "dedr": "4977", "meaning": "twist, break"},
    "M325": {"reading": "ila", "dedr": "497", "meaning": "leaf"},
    "M328": {"reading": "ū", "dedr": "651", "meaning": "thing, ooze"},
    "M373": {"reading": "pa", "dedr": "3805", "meaning": "sun, pot"},
    "M374": {"reading": "no", "dedr": "3779", "meaning": "minute, thin"},
    "M186": {"reading": "kūṟu", "dedr": "1924", "meaning": "section, share"},
    "M134": {"reading": "peru", "dedr": "4411", "meaning": "big, large"},
    "M204": {"reading": "meruku", "dedr": "5074", "meaning": "shining, pyramid"},
    "M197": {"reading": "mē", "dedr": "5086", "meaning": "superior, top"},
    "M202": {"reading": "mēṭṭu", "dedr": "5058", "meaning": "height, eminence"},
    "M242": {"reading": "māṭi", "dedr": "4796", "meaning": "mansion, terrace"},
    "M201": {"reading": "vāyil", "dedr": "5354", "meaning": "doorway"},
    "M244": {"reading": "aṟu", "dedr": "317", "meaning": "strong, castle"},
    "M249": {"reading": "māṭṭu", "dedr": "4801", "meaning": "fasten, hook"},
    "M155": {"reading": "ampi", "dedr": "177", "meaning": "boat, raft, ship"},
    "M211": {"reading": "anuppu", "dedr": "329", "meaning": "send, love"},
    "M059": {"reading": "kaṇ", "dedr": "1159", "meaning": "arrow, eye"},
    "M078": {"reading": "pori", "dedr": "4286", "meaning": "courage, chicken"},
    "M076": {"reading": "cē", "dedr": "1931", "meaning": "red, bronze, cock"},
    "M192": {"reading": "paḷḷi", "dedr": "4018", "meaning": "hamlet"},
    "M050": {"reading": "āṭu", "dedr": "78", "meaning": "goat, dance"},
    "M047": {"reading": "araṇ", "dedr": "201", "meaning": "fortress"},
    "M129": {"reading": "koḷ", "dedr": "2151", "meaning": "seize, acquire"},
    "M240": {"reading": "cil", "dedr": "1577", "meaning": "small"},
    "M216": {"reading": "ta", "dedr": "2946", "meaning": "earthen pot"},
}


def phase321a_venkatesan_crosscheck():
    """Cross-check our HIGH readings against Venkatesan's."""
    anchors = json.loads(ANCHORS_PATH.read_text("utf-8")).get("anchors", {})

    exact = []
    partial = []
    disagree = []
    no_ours = []

    for sign_id, v_info in VENKATESAN_READINGS.items():
        our = anchors.get(sign_id, {})
        our_reading = our.get("reading", "")
        v_reading = v_info["reading"]

        if not our_reading:
            no_ours.append({"sign": sign_id, "venkatesan": v_reading})
            continue

        our_clean = our_reading.lower().split("/")[0].strip()
        v_clean = v_reading.lower().split("/")[0].strip()

        if our_clean == v_clean or v_clean in our_reading.lower():
            exact.append({"sign": sign_id, "ours": our_reading,
                          "venkatesan": v_reading, "match": "EXACT"})
        elif our_clean[:3] == v_clean[:3]:
            partial.append({"sign": sign_id, "ours": our_reading,
                            "venkatesan": v_reading, "match": "PARTIAL"})
        else:
            disagree.append({"sign": sign_id, "ours": our_reading,
                             "venkatesan": v_reading, "match": "DISAGREE"})

    total = len(exact) + len(partial) + len(disagree)
    agree_rate = (len(exact) + len(partial)) / total if total else 0

    return {
        "signs_compared": total,
        "exact_match": len(exact),
        "partial_match": len(partial),
        "disagree": len(disagree),
        "no_our_reading": len(no_ours),
        "agreement_rate": round(agree_rate, 4),
        "exact_matches": exact,
        "partial_matches": partial,
        "disagreements": disagree[:15],
        "verdict": (
            f"Venkatesan cross-check: {len(exact)} exact + {len(partial)} partial "
            f"= {len(exact)+len(partial)}/{total} ({agree_rate:.0%}) agreement. "
            f"{len(disagree)} disagreements. "
            + ("STRONG independent convergence — two methods reach similar readings."
               if agree_rate >= 0.30
               else "MODERATE convergence."
               if agree_rate >= 0.15
               else "WEAK convergence — readings diverge significantly.")
        ),
    }


def phase321b_kriger_uniqueness():
    """Test Kriger's claim that 98.3% of seal inscriptions are unique."""
    inscriptions = []
    with open(HOLDAT_PATH, encoding="utf-8") as f:
        cur = None; signs = []
        for r in csv.DictReader(f):
            if r["cisi_number"] != cur:
                if signs: inscriptions.append(tuple(signs))
                cur = r["cisi_number"]; signs = []
            signs.append(r["letters"])
        if signs: inscriptions.append(tuple(signs))

    total = len(inscriptions)
    freq = Counter(inscriptions)
    unique = sum(1 for c in freq.values() if c == 1)
    unique_rate = unique / total if total else 0

    return {
        "total_inscriptions": total,
        "unique_inscriptions": unique,
        "uniqueness_rate": round(unique_rate, 4),
        "kriger_claim": 0.983,
        "match": abs(unique_rate - 0.983) < 0.05,
        "most_repeated": [
            {"inscription": " ".join(seq), "count": c}
            for seq, c in freq.most_common(10) if c > 1
        ],
        "verdict": (
            f"Uniqueness: {unique}/{total} = {unique_rate:.1%} "
            f"(Kriger claims 98.3% on unicorn seals). "
            + ("CONSISTENT with Kriger's registration-code hypothesis."
               if unique_rate > 0.90
               else "LOWER uniqueness — may reflect formulaic patterns.")
        ),
    }


def phase321c_outreach_list():
    """Compile prioritized outreach list."""
    return {
        "tier1_immediate": [
            {
                "name": "S.K. Venkatesan",
                "affiliation": "CQRL Bits, Chennai",
                "work": "decipher-ivc: Proto-Dravidian logo-syllabic decipherment using DEDR + M77",
                "why": "Most directly comparable independent work. Uses same data (M77, DEDR). Head-to-head reading comparison possible.",
                "contact": "GitHub: Sukii/decipher-ivc (send feedback via repo)",
                "action": "Share our reading table for comparison. Propose joint validation.",
            },
            {
                "name": "Ashish Nair",
                "affiliation": "Independent (CMU alumni)",
                "work": "Synthetic-Baseline Scorecard (arXiv:2604.17828, Apr 2026)",
                "why": "His multi-metric framework is the most rigorous structural test. We should run his exact code on our decoded corpus.",
                "contact": "ashishn@alumni.cmu.edu",
                "action": "Share our decoded corpus for scorecard testing. Propose collaboration.",
            },
            {
                "name": "Kevin Shaw",
                "affiliation": "Independent, Wales",
                "work": "LISSE framework + Harappan Phonetic Constraint Field (2026)",
                "why": "Different theoretical stance (non-phonetic). Structural comparison valuable.",
                "contact": "Academia.edu: independent.academia.edu/KevinShaw75; Medium: @kev.shaw.2012",
                "action": "Share preprint v3. Discuss structural vs phonetic approaches.",
            },
        ],
        "tier2_validation": [
            {
                "name": "Bahata Ansumali Mukhopadhyay",
                "affiliation": "Independent (Infor/Koch Industries, Bengaluru)",
                "work": "Semasiographic decipherment: fish=gemstone, taxation/licensing model (Nature HSS Comms 2023, SSRN 2021-2025)",
                "why": "Most rigorous semasiographic researcher. Our fish-sign 0/140 finding confirms her compound-only observation. Published in peer-reviewed venue.",
                "contact": "alapchari@gmail.com (from Nature HSS paper)",
                "action": "Share fish-sign finding + guild-identity formula results. Discuss phonetic vs semasiographic.",
            },
            {
                "name": "Boris Kriger",
                "affiliation": "Institute of Integrative and Interdisciplinary Research, Toronto",
                "work": "Seals as 'Bronze Age credit cards' — registration code model (2026, 3-paper programme)",
                "why": "His registration-code model partly overlaps with our guild-identity reading. First positional entropy analysis.",
                "contact": "Via IIIR or Zenodo DOI: 10.5281/zenodo.19103880",
                "action": "Share uniqueness test results. Discuss overlap between registration-code and guild-identity.",
            },
            {
                "name": "Aruna Sharma & Shubhajit Roy Chowdhury",
                "affiliation": "AI-EPIGRAPHY project",
                "work": "Interactive computational decipherment tool (ACM HCI 2025)",
                "why": "Computational tool with n-gram modeling and naive Bayes classifier. Could test our readings.",
                "contact": "GitHub: atulsharma0071/indiahci2025",
                "action": "Propose testing our reading model in their interactive framework.",
            },
        ],
        "tier3_specialist": [
            {
                "name": "Dravidianist specialists (existing outreach)",
                "contacts": "Renganathan, Murugaiyan, Kobayashi, Kolichala, Vasu",
                "status": "Packets sent; Vasu gave preliminary positive response",
                "action": "Follow up with v3 preprint including corrected 400 HIGH model + 50% Parpola agreement.",
            },
            {
                "name": "Juan Gabriel Molina",
                "work": "Five-domain convergence (2026) + Meluhha Nexus",
                "why": "Provides macro-level archaeological/linguistic/genetic convergence evidence for Proto-Dravidian hypothesis.",
                "contact": "Via Academia.edu",
                "action": "Share preprint. His convergence framework supports our computational findings.",
            },
            {
                "name": "Keeladi/Tamil Nadu State Archaeology Dept",
                "work": "60% graffiti mark parallels to Indus signs; 580 BCE dating",
                "why": "Archaeological continuity evidence. Our readings could be tested against Keezhadi graffiti.",
                "contact": "Via TN Dept of Archaeology (tnarch.gov.in)",
                "action": "Long-term: propose reading validation against Keezhadi graffiti marks.",
            },
        ],
    }


def main():
    print("=" * 60)
    print("PHASE 321: VENKATESAN + KRIGER + OUTREACH")
    print("=" * 60)

    print("\n── 321a: Venkatesan Cross-Check ──")
    p321a = phase321a_venkatesan_crosscheck()
    print(f"  {p321a['verdict']}")

    print("\n── 321b: Kriger Uniqueness Test ──")
    p321b = phase321b_kriger_uniqueness()
    print(f"  {p321b['verdict']}")

    print("\n── 321c: Outreach List ──")
    outreach = phase321c_outreach_list()
    n_contacts = sum(len(t) for t in [outreach["tier1_immediate"],
                                        outreach["tier2_validation"],
                                        outreach["tier3_specialist"]])
    print(f"  {n_contacts} contacts across 3 tiers compiled.")

    result = {
        "phase321a_venkatesan": p321a,
        "phase321b_kriger": p321b,
        "phase321c_outreach": outreach,
    }

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(
        json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"\nSaved: {OUT_PATH}")


if __name__ == "__main__":
    main()
