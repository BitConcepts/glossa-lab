"""Phase-117: Grammar Inferences → LOW Anchors.

Commits Phase-112 grammar-slot inferences (≥2 contexts, non-empty reading)
as LOW confidence anchors in INDUS_FINAL_ANCHORS.json.

CPU only. Output: reports/phase117_grammar_low_anchors.json
"""
from __future__ import annotations

import json
from pathlib import Path

REPO    = Path(__file__).parents[2]
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
P112    = REPO / "reports/phase112_grammar_slot_inference.json"
REPORTS = REPO / "reports"
REPORTS.mkdir(exist_ok=True)
OUT     = REPORTS / "phase117_grammar_low_anchors.json"

MIN_CONTEXTS = 2  # min grammar contexts to commit as LOW


def main():
    print("Phase-117: Grammar Inferences → LOW Anchors\n")

    if not P112.exists():
        print("  [ERROR] Phase-112 report not found. Run phase112 first.")
        return {"error": "phase112 not found"}

    anchors_data = json.loads(ANCHORS.read_text("utf-8"))
    anchors = anchors_data.get("anchors", {})
    existing_conf = {s for s, v in anchors.items()
                     if v.get("confidence") in ("HIGH","MEDIUM","LOW")}
    print(f"  Existing assigned signs: {len(existing_conf)}")

    p112 = json.loads(P112.read_text("utf-8"))
    table = p112.get("inference_table", [])
    print(f"  Phase-112 inference entries: {len(table)}")

    added = []
    skipped = 0

    for entry in table:
        sign = entry.get("sign", "")
        reading = entry.get("inferred_reading", "")
        n_ctx = entry.get("n_grammar_contexts", 0)

        if not sign or not reading or n_ctx < MIN_CONTEXTS:
            skipped += 1
            continue
        if sign in existing_conf:
            skipped += 1
            continue

        slot = entry.get("dominant_slot", "MEDIAL_BETWEEN_CONF")
        patterns = entry.get("sample_patterns", [])
        anchors[sign] = {
            "reading": reading,
            "confidence": "LOW",
            "basis": (
                f"Phase-117 grammar inference: slot={slot}, "
                f"n_contexts={n_ctx}, patterns={patterns[:3]}. "
                f"Inferred from Dravidian grammar slot model (Phases 74-112)."
            ),
            "source": "Phase-117",
        }
        added.append(sign)
        print(f"  + {sign}: '{reading}' (slot={slot}, n={n_ctx})")

    # Save
    anchors_data["anchors"] = anchors
    anchors_data["total"] = len(anchors)
    ANCHORS.write_text(json.dumps(anchors_data, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"\n  Added {len(added)} new LOW anchors (skipped {skipped})")

    result = {
        "phase": 117,
        "min_contexts": MIN_CONTEXTS,
        "n_added": len(added),
        "n_skipped": skipped,
        "added_signs": added,
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  Saved → {OUT}")
    return result


if __name__ == "__main__":
    main()
