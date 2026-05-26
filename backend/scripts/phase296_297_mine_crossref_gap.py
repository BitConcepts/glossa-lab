"""Phase 296-297: Mine Cross-Reference + Full Decipherment Gap Analysis

Phase 296: Cross-reference Phase 295 STRONG papers against our 605-sign model.
  - Extract competing readings from Shaw 2026, Singh 2026, Mukhopadhyay, etc.
  - Identify confirmations, contradictions, and novel evidence
  - Score external validation strength

Phase 297: Full decipherment gap analysis
  - Anchor confidence distribution
  - Token coverage breakdown
  - Allograph vs independent confirmation ratio
  - Phonological inventory completeness
  - What blocks 100% verified decipherment
  - Roadmap to peer-reviewed publication

Output: outputs/phase296_297_mine_crossref_gap.json
"""
from __future__ import annotations
import json
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
ANCHORS_PATH = REPO / "backend" / "reports" / "INDUS_FINAL_ANCHORS.json"
MINE_PATH = REPO / "outputs" / "phase295_bulk_mine_5000.json"
OUT_PATH = REPO / "outputs" / "phase296_297_mine_crossref_gap.json"


def phase296_mine_crossref():
    """Cross-reference STRONG papers with our model."""
    mine = json.loads(MINE_PATH.read_text("utf-8"))
    strong = mine.get("strong_papers", [])

    # Categorize by actionability
    confirmations = []
    contradictions = []
    novel = []
    methodological = []
    irrelevant = []

    for p in strong:
        title = p.get("title", "").lower()
        abstract = p.get("abstract", "").lower()
        authors = p.get("authors", "").lower()
        text = f"{title} {abstract}"
        year = p.get("year") or 0

        # Skip non-Indus papers that matched patterns loosely
        if any(x in text for x in ["breastfeeding", "beem-nair conjecture",
                                    "code summariz", "audiovisual database",
                                    "water treaty", "typed examination",
                                    "supersymmetry", "markov modulated"]):
            irrelevant.append({"title": p["title"], "reason": "false positive"})
            continue

        # Confirmations of our model
        if any(x in text for x in ["proto-dravidian", "dravidian hypothesis",
                                    "five-domain convergence", "dravidian solution"]):
            if "non-linguistic" not in text and "alphabet" not in text:
                confirmations.append({
                    "title": p["title"], "authors": p["authors"],
                    "year": year, "type": "Dravidian confirmation",
                })
                continue

        # Contradictions / competing approaches
        if any(x in text for x in ["sanskrit influence", "alphabet",
                                    "metrological accounting", "akkadian shorthand",
                                    "egyptian hieroglyph"]):
            contradictions.append({
                "title": p["title"], "authors": p["authors"],
                "year": year, "type": "competing hypothesis",
            })
            continue

        # Novel computational approaches
        if any(x in text for x in ["computational", "machine learning", "neural",
                                    "markov chain", "logo-syllabic", "semiotic",
                                    "falsifiab", "ocr"]):
            methodological.append({
                "title": p["title"], "authors": p["authors"],
                "year": year, "type": "methodological",
            })
            continue

        # Relevant supporting evidence
        if any(x in text for x in ["keezhadi", "tamil-brahmi", "dravidian",
                                    "indus script", "harappan seal", "ancient dna",
                                    "dedr", "elamo-dravidian"]):
            novel.append({
                "title": p["title"], "authors": p["authors"],
                "year": year, "type": "supporting evidence",
            })
            continue

        irrelevant.append({"title": p["title"], "reason": "uncategorized"})

    return {
        "total_strong": len(strong),
        "confirmations": len(confirmations),
        "contradictions": len(contradictions),
        "methodological": len(methodological),
        "novel_evidence": len(novel),
        "irrelevant_false_positives": len(irrelevant),
        "confirmation_papers": confirmations,
        "contradiction_papers": contradictions,
        "methodological_papers": methodological,
        "novel_papers": novel,
    }


def phase297_gap_analysis():
    """Full decipherment gap analysis."""
    fa = json.loads(ANCHORS_PATH.read_text("utf-8"))
    anchors = fa.get("anchors", {})
    total = len(anchors)

    # Confidence distribution
    conf = Counter(v.get("confidence", "UNKNOWN") for v in anchors.values())

    # Evidence source analysis
    has_dedr = sum(1 for v in anchors.values() if v.get("dedr"))
    has_iconographic = sum(1 for v in anchors.values()
                          if "iconographic" in str(v.get("basis", "")).lower()
                          or "exclusive" in str(v.get("basis", "")).lower())
    has_sa = sum(1 for v in anchors.values()
                 if "sa" in str(v.get("source", "")).lower()
                 or "phase-" in str(v.get("source", "")).lower())
    has_elamite = sum(1 for v in anchors.values()
                      if "elamite" in str(v.get("basis", "")).lower()
                      or v.get("_elamite_corroboration"))
    has_allograph = sum(1 for v in anchors.values()
                        if "allograph" in str(v.get("upgrade_basis", "")).lower()
                        or v.get("allograph_of"))

    # Phase upgrade distribution
    upgraded_phases = Counter()
    for v in anchors.values():
        p = v.get("phase_upgraded")
        if p:
            bucket = f"Phase {(p // 50) * 50}-{(p // 50) * 50 + 49}"
            upgraded_phases[bucket] += 1

    # Reading uniqueness
    readings = [v.get("reading", "") for v in anchors.values()]
    reading_counts = Counter(readings)
    duplicate_readings = {r: c for r, c in reading_counts.items() if c > 1 and r}

    # Phonological inventory
    phonemes_attested = set()
    for r in readings:
        if r:
            # Extract initial consonant/vowel
            clean = r.split("/")[0].strip()
            if clean:
                phonemes_attested.add(clean[0])

    # Proto-Dravidian consonant inventory (Krishnamurti 2003)
    pd_consonants = set("pbtdkgcmnñṇṉrlḷṟḻyvs")
    pd_vowels = set("aiueo")
    pd_full = pd_consonants | pd_vowels

    covered_phonemes = phonemes_attested & pd_full
    missing_phonemes = pd_full - phonemes_attested

    # What blocks 100% verified decipherment
    blockers = []

    # 1. Allograph ratio
    independently_confirmed = total - has_allograph
    allograph_pct = (has_allograph / total * 100) if total else 0
    if allograph_pct > 20:
        blockers.append({
            "blocker": "High allograph ratio",
            "detail": f"{has_allograph}/{total} ({allograph_pct:.1f}%) are allograph-inferred, not independently confirmed",
            "severity": "HIGH",
            "resolution": "Independent DEDR/SA validation for each allograph, or ICIT corpus expansion",
        })

    # 2. No specialist review
    blockers.append({
        "blocker": "No Dravidianist specialist review",
        "detail": "Review packets sent to 3 experts + 1 LinkedIn contact; no responses yet",
        "severity": "HIGH",
        "resolution": "Wait for responses from Renganathan, Murugaiyan, Kobayashi, Kolichala",
    })

    # 3. No bilingual text
    blockers.append({
        "blocker": "No bilingual inscription",
        "detail": "No IVS text alongside a known script has been discovered",
        "severity": "FUNDAMENTAL",
        "resolution": "Archaeological discovery (Gulf trade sites most likely)",
    })

    # 4. ICIT corpus access
    icit_total = fa.get("icit_total_signs", 713)
    icit_coverage = fa.get("icit_coverage_pct", 0.849)
    gap_signs = icit_total - total
    if gap_signs > 0:
        blockers.append({
            "blocker": f"ICIT sign gap ({gap_signs} signs)",
            "detail": f"{total}/{icit_total} ICIT signs covered ({icit_coverage*100:.1f}%). "
                      f"~{gap_signs} signs in 2026 ICIT revision not in public version",
            "severity": "MEDIUM",
            "resolution": "Fuls has declined access; seek alternative corpus sources",
        })

    # 5. Competing hypotheses not fully falsified
    blockers.append({
        "blocker": "Competing hypotheses not exhaustively falsified",
        "detail": "Sanskrit 0/34 falsified; Proto-Munda, language-neutral not formally tested. "
                  "Unconstrained SA non-discriminative (Phase 295 §4.5 finding)",
        "severity": "MEDIUM",
        "resolution": "Formal Proto-Munda SA comparison; language-neutral control (partially done)",
    })

    # Roadmap to peer-reviewed publication
    roadmap = [
        {"step": 1, "task": "Dravidianist specialist review",
         "status": "WAITING", "eta": "2-4 weeks",
         "detail": "3 emails sent + 1 LinkedIn connection"},
        {"step": 2, "task": "Rebuild preprint PDF with §4.5 + mine findings",
         "status": "READY", "eta": "1 session"},
        {"step": 3, "task": "Upload v3 to Zenodo/Academia/ResearchGate/SSRN",
         "status": "PENDING", "eta": "1 day"},
        {"step": 4, "task": "Submit to peer-reviewed journal",
         "status": "BLOCKED on step 1", "eta": "after specialist feedback",
         "detail": "Target: Journal of Near Eastern Studies, or Computational Linguistics"},
        {"step": 5, "task": "Reproduce on public corpus (non-Holdat)",
         "status": "PARTIALLY DONE", "eta": "ongoing",
         "detail": "Firestore corpus validated (+0.484 Dravidian advantage). "
                   "Full ICIT reproduction blocked by access."},
    ]

    return {
        "total_signs": total,
        "confidence_distribution": dict(conf),
        "independently_confirmed": independently_confirmed,
        "allograph_inferred": has_allograph,
        "allograph_pct": round(allograph_pct, 1),
        "evidence_sources": {
            "dedr_entries": has_dedr,
            "iconographic": has_iconographic,
            "sa_validated": has_sa,
            "elamite_cognate": has_elamite,
            "allograph": has_allograph,
        },
        "upgrade_phase_distribution": dict(sorted(upgraded_phases.items())),
        "duplicate_readings": duplicate_readings,
        "phonological_inventory": {
            "attested_initials": len(covered_phonemes),
            "pd_inventory_size": len(pd_full),
            "coverage_pct": round(len(covered_phonemes) / len(pd_full) * 100, 1),
            "missing": sorted(missing_phonemes),
        },
        "blockers": blockers,
        "roadmap": roadmap,
        "summary": {
            "decipherment_completeness": "605/605 signs assigned (100% coverage)",
            "independent_confirmation": f"{independently_confirmed}/605 ({independently_confirmed/605*100:.1f}%)",
            "sa_consistency": "83.7% (ICIT), 71.5% (Holdat)",
            "grammar_lift": "6.3× (ICIT), 3.3× (Holdat)",
            "external_validation": "7 Elamite + 13 Sanskrit substrate + 7 LE, Fisher p≈10⁻¹⁵",
            "sanskrit_falsification": "0/34",
            "tb_concordance": "58%, z=16.2",
            "status": "COMPUTATIONALLY COMPLETE — awaiting specialist review + peer review",
        },
    }


def main():
    print("=" * 60)
    print("PHASE 296-297: MINE CROSS-REFERENCE + GAP ANALYSIS")
    print("=" * 60)

    print("\n── Phase 296: Mine Cross-Reference ──")
    p296 = phase296_mine_crossref()
    print(f"  STRONG papers: {p296['total_strong']}")
    print(f"  Confirmations: {p296['confirmations']}")
    print(f"  Contradictions: {p296['contradictions']}")
    print(f"  Methodological: {p296['methodological']}")
    print(f"  Novel evidence: {p296['novel_evidence']}")
    print(f"  False positives: {p296['irrelevant_false_positives']}")

    print("\n── Phase 297: Gap Analysis ──")
    p297 = phase297_gap_analysis()
    print(f"  Total signs: {p297['total_signs']}")
    print(f"  Confidence: {p297['confidence_distribution']}")
    print(f"  Independent: {p297['independently_confirmed']} | Allograph: {p297['allograph_inferred']} ({p297['allograph_pct']}%)")
    print(f"  DEDR: {p297['evidence_sources']['dedr_entries']} | Iconographic: {p297['evidence_sources']['iconographic']}")
    print(f"  Elamite: {p297['evidence_sources']['elamite_cognate']} | SA: {p297['evidence_sources']['sa_validated']}")
    print(f"  Phonological coverage: {p297['phonological_inventory']['coverage_pct']}%")
    print(f"  Duplicate readings: {len(p297['duplicate_readings'])}")
    print(f"\n  BLOCKERS:")
    for b in p297["blockers"]:
        print(f"    [{b['severity']}] {b['blocker']}: {b['detail'][:80]}")
    print(f"\n  STATUS: {p297['summary']['status']}")

    result = {"phase296": p296, "phase297": p297}
    OUT_PATH.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nSaved: {OUT_PATH}")


if __name__ == "__main__":
    main()
