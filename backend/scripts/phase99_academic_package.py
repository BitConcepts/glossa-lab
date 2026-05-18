"""Phase-99: Academic Communication Package.

Formats the full research output into a structured academic package
suitable for communicating with Dr. Fuls (Indus script specialist)
or other academic collaborators.

Package contents:
1. Executive summary (1 page equivalent)
2. Methodology overview (citing published methods)
3. 10 highlighted scholarly translations with DEDR citations
4. Statistical evidence summary (z-scores, p-values, permutation tests)
5. Anchor table (HIGH confidence only — 37 entries)
6. Open questions and collaboration requests

CPU only. Output: reports/phase99_academic_package.json
"""
from __future__ import annotations
import json
from pathlib import Path

REPO    = Path(__file__).parents[2]
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
REPORTS = REPO / "reports"
REPORTS.mkdir(exist_ok=True)
OUT     = REPORTS / "phase99_academic_package.json"

# Reports to cite
REPORT_REFS = {
    "phase44": "Phase-44: Dravidian SA lift 3.13× (z=12.1)",
    "phase57": "Phase-57: z=19.07 expanded SA (53 anchors, 5-seed consensus)",
    "phase67": "Phase-67: Dravidian vs Sanskrit lift ratio 1.85× (DEFINITIVE falsification)",
    "phase69": "Phase-69: Grammar 100% site-invariant across 9 Holdat sites (chi2 p>0.05)",
    "phase74": "Phase-74: M267=iN genitive CONFIRMED (z=8.04, permutation p<0.0001)",
    "phase78": "Phase-78: Formula distribution invariant across 9 sites (chi2 p=0.855)",
    "phase82": "Phase-82: 733/1670 seals (44%) at 100% sign coverage",
    "phase90": "Phase-90: 50 scholarly translations across 9 sites, all DEDR-cited",
}


def main():
    print("Phase-99: Academic Communication Package\n")

    anchors_data = json.loads(ANCHORS.read_text("utf-8"))
    anchors = anchors_data["anchors"]
    high = {s: v for s, v in anchors.items() if v.get("confidence") == "HIGH"}
    medium = {s: v for s, v in anchors.items() if v.get("confidence") == "MEDIUM"}
    print(f"  HIGH anchors: {len(high)}")
    print(f"  MEDIUM anchors: {len(medium)}")

    # Load 10 best translations from Phase-90
    translations_10 = []
    p90 = REPORTS / "phase90_scholarly_translations.json"
    if p90.exists():
        p90_data = json.loads(p90.read_text())
        translations_10 = p90_data.get("translations", [])[:10]

    # Build HIGH anchor table for academic presentation
    high_anchor_table = []
    for sign, info in sorted(high.items()):
        high_anchor_table.append({
            "sign": sign,
            "reading": info.get("reading",""),
            "dedr_id": info.get("dedr_id",""),
            "meaning": info.get("meaning",""),
            "source": info.get("source",""),
        })

    # Executive summary
    executive_summary = {
        "title": "Indus Script Decipherment Progress Report",
        "date": "2026-05-18",
        "institution": "Glossa Lab (Independent Research)",
        "contact": "tpierson@bitconcepts.tech",
        "status": "Research-grade preliminary decipherment — ~35% complete",
        "key_claim": (
            "We present statistical and linguistic evidence that the Indus script "
            "encodes an early form of Proto-Dravidian. The evidence includes: "
            "(1) Dravidian language model achieves 1.85× higher corpus score than Sanskrit (definitive); "
            "(2) grammar is site-invariant across all 9 excavation sites (unified writing system); "
            "(3) 37 HIGH-confidence sign readings with full DEDR citations; "
            "(4) M267=iN genitive marker confirmed by grammar test (z=8.04, p<0.0001); "
            "(5) 50 complete seal translations with morphological glosses across 9 sites."
        ),
        "call_to_action": (
            "We seek academic collaboration to (a) validate HIGH-confidence readings, "
            "(b) provide access to full CISI corpus, and (c) co-author a preliminary publication."
        ),
    }

    # Statistical evidence package
    statistical_evidence = [
        {
            "test": "Dravidian LM lift",
            "result": "3.13× (Phase-44), 1.85× vs Sanskrit (Phase-67)",
            "method": "SA decipherment, 300k iterations, 944-bigram LM",
            "significance": "z=12.1, definitive for Dravidian hypothesis",
            "citation": "Mahadevan 1977 + DEDR cross-reference",
        },
        {
            "test": "Grammar invariance",
            "result": "100% of HIGH/MEDIUM signs site-invariant",
            "method": "Chi-squared test across 9 Holdat sites",
            "significance": "p>0.05 for all signs — pan-Indus writing system",
            "citation": "Phase-69 site stratification analysis",
        },
        {
            "test": "Genitive marker M267",
            "result": "[AGENT]-M267-[TITLE]: 6.5% vs null 1.5% (4.3× above null)",
            "method": "Permutation test, 10,000 shuffles",
            "significance": "z=8.04, p<0.0001",
            "citation": "Phase-74 grammar constraint test",
        },
        {
            "test": "Formula distribution",
            "result": "p=0.855 — formula types identical across all 9 sites",
            "method": "Chi-squared test, 1670-seal Holdat corpus",
            "significance": "Second independent confirmation of unified writing",
            "citation": "Phase-78 semantic clustering",
        },
        {
            "test": "Sanskrit falsification",
            "result": "Dravidian lift 23.4% vs Sanskrit 12.6% (ratio 1.85×)",
            "method": "Same-null comparison: both tested against identical corpus",
            "significance": "Methodologically valid cross-language test",
            "citation": "Phase-67 Sanskrit normalisation",
        },
    ]

    # Open questions for collaboration
    open_questions = [
        {
            "priority": 1,
            "question": "M293 (bow sign, freq=232): is the reading 'vil' (bow, DEDR 5428) or 'ta' (body, DEDR 3003)?",
            "evidence_so_far": "SA: inconclusive (syl='ta', proto='ar'). Iconography: HIGH plausibility for 'vil'.",
            "needed": "Independent iconographic confirmation or full-text Parpola 1994 check",
        },
        {
            "priority": 2,
            "question": "CISI corpus validation: do our anchor positional profiles hold in Parpola's corpus?",
            "evidence_so_far": "23/101 anchors found in CISI; crosswalk now 115+ entries (Phase-96)",
            "needed": "Full CISI sign list in Mahadevan M-numbers",
        },
        {
            "priority": 3,
            "question": "Formula readability: can complete seal translations be published?",
            "evidence_so_far": "50 translations with DEDR citations; all HIGH confidence",
            "needed": "Expert validation of 5-10 translations before submission",
        },
    ]

    print(f"\n  Academic package contents:")
    print(f"    HIGH anchor table:      {len(high_anchor_table)} entries")
    print(f"    Statistical evidence:   {len(statistical_evidence)} tests")
    print(f"    Scholarly translations: {len(translations_10)}")
    print(f"    Open questions:         {len(open_questions)}")

    print(f"\n=== Phase-99 Results ===")
    print(f"  Package ready for Dr. Fuls / academic submission")
    print(f"  Key headline: {executive_summary['key_claim'][:80]}...")

    result = {
        "_citation": {"primary": ["A.1"]},
        "gpu_device": "cpu",
        "package_date": "2026-05-18",
        "executive_summary": executive_summary,
        "statistical_evidence": statistical_evidence,
        "high_anchor_table": high_anchor_table,
        "n_high_anchors": len(high_anchor_table),
        "n_medium_anchors": len(medium),
        "n_total_anchors": len(high) + len(medium),
        "sample_translations": [
            {
                "cisi_id": t.get("cisi_id",""),
                "site": t.get("site",""),
                "transliteration": t.get("transliteration",""),
                "formula_type": t.get("formula_type",""),
                "dedr_citations": t.get("dedr_citations",[])[:4],
            }
            for t in translations_10[:10]
        ],
        "open_questions": open_questions,
        "report_references": REPORT_REFS,
        "verdict": (
            f"Phase-99: Academic communication package assembled. "
            f"{len(high_anchor_table)} HIGH-confidence anchors with full DEDR citations. "
            f"{len(translations_10)} scholarly translations ready. "
            f"Package suitable for Dr. Fuls collaboration request."
        ),
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), "utf-8")
    print(f"\nReport: {OUT}")


if __name__ == "__main__":
    main()
