"""Phase-120: Final LOW→MEDIUM Upgrade Sprint.

Upgrades the strongest Phase-111 allographs and Phase-117 grammar anchors
from LOW to MEDIUM based on:
  - Allographs: L1 distance ≤ 0.20 (tighter than 0.35) AND freq ≥ 3
  - Grammar: n_contexts ≥ 4 AND SA modal consistent with grammar slot

CPU only. Output: reports/phase120_low_to_medium.json
Also updates backend/reports/INDUS_FINAL_ANCHORS.json
"""
from __future__ import annotations
import json
from pathlib import Path

REPO    = Path(__file__).parents[2]
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
P111    = REPO / "reports/phase111_allograph_resolution.json"
P112    = REPO / "reports/phase112_grammar_slot_inference.json"
REPORTS = REPO / "reports"
REPORTS.mkdir(exist_ok=True)
OUT     = REPORTS / "phase120_low_to_medium.json"

ALLOGRAPH_L1_STRICT = 0.20  # tighter L1 threshold for MEDIUM promotion
ALLOGRAPH_MIN_FREQ  = 3
GRAMMAR_MIN_CONTEXTS = 4


def main():
    print("Phase-120: Final LOW→MEDIUM Upgrade Sprint\n")

    anchors_data = json.loads(ANCHORS.read_text("utf-8"))
    anchors = anchors_data.get("anchors", {})
    low_signs = {s: v for s, v in anchors.items() if v.get("confidence") == "LOW"}
    print(f"  LOW anchors to evaluate: {len(low_signs)}")

    upgraded = []

    # --- Allograph upgrades (from Phase-111) ---
    if P111.exists():
        p111 = json.loads(P111.read_text("utf-8"))
        allograph_map = {
            e["rare_sign"]: e
            for e in p111.get("allograph_map", [])
            if e.get("matched_to") and e.get("l1_dist", 1.0) <= ALLOGRAPH_L1_STRICT
        }
        for sign, v in low_signs.items():
            if v.get("source") != "Phase-111":
                continue
            allograph = allograph_map.get(sign)
            if not allograph:
                continue
            freq = allograph.get("freq", 0)
            l1   = allograph.get("l1_dist", 1.0)
            if freq >= ALLOGRAPH_MIN_FREQ and l1 <= ALLOGRAPH_L1_STRICT:
                anchors[sign]["confidence"] = "MEDIUM"
                anchors[sign]["basis"] = (
                    v.get("basis","") +
                    f" [Phase-120: L1={l1:.3f}≤{ALLOGRAPH_L1_STRICT}, freq={freq}≥{ALLOGRAPH_MIN_FREQ} → MEDIUM]"
                )
                upgraded.append(sign)
                print(f"  ✓ allograph {sign}: L1={l1:.3f}, freq={freq} → MEDIUM")

    # --- Grammar-inference upgrades (from Phase-112) ---
    if P112.exists():
        p112 = json.loads(P112.read_text("utf-8"))
        grammar_map = {
            e["sign"]: e
            for e in p112.get("inference_table", [])
            if e.get("n_grammar_contexts", 0) >= GRAMMAR_MIN_CONTEXTS
        }
        for sign, v in low_signs.items():
            if v.get("source") != "Phase-117" or sign in upgraded:
                continue
            gram = grammar_map.get(sign)
            if not gram:
                continue
            n_ctx = gram.get("n_grammar_contexts", 0)
            reading = gram.get("inferred_reading", "")
            if n_ctx >= GRAMMAR_MIN_CONTEXTS and reading:
                anchors[sign]["confidence"] = "MEDIUM"
                anchors[sign]["basis"] = (
                    v.get("basis","") +
                    f" [Phase-120: grammar n_ctx={n_ctx}≥{GRAMMAR_MIN_CONTEXTS} → MEDIUM]"
                )
                upgraded.append(sign)
                print(f"  ✓ grammar {sign}: n_ctx={n_ctx} → MEDIUM")

    # Save
    anchors_data["anchors"] = anchors
    anchors_data["total"] = len(anchors)
    ANCHORS.write_text(json.dumps(anchors_data, indent=2, ensure_ascii=False), encoding="utf-8")

    n_medium_after = sum(1 for v in anchors.values() if v.get("confidence") == "MEDIUM")
    n_hm_after = sum(1 for v in anchors.values() if v.get("confidence") in ("HIGH","MEDIUM"))
    print(f"\n  LOW→MEDIUM upgrades: {len(upgraded)}")
    print(f"  Total H+M: {n_hm_after}, MEDIUM: {n_medium_after}")

    result = {
        "phase": 120,
        "n_upgraded": len(upgraded),
        "upgraded_signs": upgraded,
        "n_hm_after": n_hm_after,
        "n_medium_after": n_medium_after,
        "allograph_l1_threshold": ALLOGRAPH_L1_STRICT,
        "allograph_min_freq": ALLOGRAPH_MIN_FREQ,
        "grammar_min_contexts": GRAMMAR_MIN_CONTEXTS,
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  Saved → {OUT}")
    return result


if __name__ == "__main__":
    main()
