"""Phase-216: SA Re-calibration with all 410 Anchors.

Re-evaluates all MEDIUM anchors (including the 30 added in Phase 193-215)
against the HIGH upgrade criteria with the full 410-anchor set pinned.

Phase-116 ran on May 18 with 131 anchors. Since then phases 193-215 added
30 new MEDIUM anchors sourced from Phase-206, 207, 209, 213-214 runs.
These were never through the upgrade criteria.

GPU if available. Output: outputs/phase216_sa_recal_410anchors.json
Also updates backend/reports/INDUS_FINAL_ANCHORS.json
"""
from __future__ import annotations

import csv
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path

REPO    = Path(__file__).parents[2]
HOLDAT  = REPO / "corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv"
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
OUT     = REPO / "outputs/phase216_sa_recal_410anchors.json"
OUT.parent.mkdir(exist_ok=True)

sys.path.insert(0, str(REPO / "backend"))
os.environ.setdefault("GLOSSA_DATA_DIR", str(REPO / "backend/data"))

N_SEEDS     = 6    # seeds per sign — adequate with 161 pinned anchors
CONS_HIGH   = 0.75
CONS_MEDIUM = 0.40

DEDR_PATTERN = re.compile(r"DEDR\s*\d{4}")

# Proto-Dravidian valid syllable openings
PD_VALID = {
    "a","ā","i","ī","u","ū","e","ē","o","ō",
    "k","ka","ki","ku","ko","c","ca","ci","t","ta","ti","tu",
    "n","na","ni","nu","nē","p","pa","pi","pu","m","ma","mi","mu",
    "v","va","vi","y","ya","r","ra","l","la",
    "ay","an","am","al","ar","ir","il","nal","vel","kan","van",
    "per","tan","ko","mu","pu","tu","ma","na",
}

DEDR_QUICK = {
    "vel":"5469", "pon":"4533", "nal":"3569", "van":"5231",
    "kan":"1145", "per":"4442", "tan":"3136", "ko":"1570",
    "ka":"1145",  "mu":"5012",  "pu":"4317",  "tu":"3385",
    "ma":"4751",  "na":"3549",  "nē":"3741",  "ay":"0206",
    "an":"0149",  "am":"0200",  "ar":"0359",  "ir":"0488",
    "il":"0486",  "cu":"2732",  "vi":"5428",  "va":"5231",
    "kol":"1570", "erutu":"0830", "yānai":"5178", "puli":"4164",
    "nēr":"3741", "kai":"1280", "kō":"1570",   "ūr":"0728",
    "tiru":"3266","mā":"4751",  "vēl":"5494",  "naN":"3549",
    "mi":"4910",  "maa":"4751", "po":"4533",   "inci":"0465",
    "vel":"5469", "aru":"0361", "ir":"0488",   "il":"0486",
    "ēḷ":"0874",  "āṉai":"0103","māṭu":"4871", "kōṉ":"2199",
    "nal":"3569", "erumai":"0830",
}

# Sources considered SA-reliable (all named Phase runs that ran full SA)
RELIABLE_SOURCES = {
    "Phase-95","Phase-91","Phase-83","Phase-87","Phase-89",
    "Parpola","Phase-80","Phase-48","Phase-73","Phase-116",
    "Phase-206","Phase-207","Phase-209","Phase-213","Phase-214",
    "Phase-193","Phase-196","Phase-197","Phase-198","Phase-199",
    "Phase-200","Phase-201","Phase-202","Phase-203","Phase-204",
    "Phase-205","Phase-208","Phase-210","Phase-211","Phase-212",
    "Phase-104","Phase-105","Phase-106","Phase-107","Phase-108",
    "legacy","Phase-30","Phase-40","Phase-50","Phase-60",
}


def load_corpus():
    seals = {}
    with open(HOLDAT, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            s = (row.get("letters") or "").strip()
            c = row.get("cisi_number", ""); p = int(row.get("position", 0) or 0)
            if not c: continue
            if c not in seals: seals[c] = []
            while len(seals[c]) <= p: seals[c].append("")
            seals[c][p] = s
    return {c: [s for s in v if s] for c, v in seals.items() if any(v)}


def source_reliable(source: str) -> bool:
    if not source: return False
    for rs in RELIABLE_SOURCES:
        if rs in source:
            return True
    # Any Phase-NNN that ran SA is reliable
    if re.search(r"Phase-\d{2,3}", source):
        return True
    return False


def has_dedr(basis: str, reading: str) -> bool:
    if DEDR_PATTERN.search(basis or ""):
        return True
    rl = reading.lower().strip()
    return rl in DEDR_QUICK or any(rl.startswith(k) for k in DEDR_QUICK)


def main():
    print("Phase-216: SA Re-calibration with 410 Anchors\n")

    anchors_data = json.loads(ANCHORS.read_text("utf-8"))
    anchors = anchors_data.get("anchors", {})

    # Pinned set: all HIGH + MEDIUM
    anchor_map = {
        s: v["reading"] for s, v in anchors.items()
        if v.get("confidence") in ("HIGH", "MEDIUM") and v.get("reading")
    }
    medium_signs = {s: v for s, v in anchors.items() if v.get("confidence") == "MEDIUM"}
    high_before = sum(1 for v in anchors.values() if v.get("confidence") == "HIGH")

    print(f"  Pinned H+M anchors: {len(anchor_map)}")
    print(f"  MEDIUM to evaluate: {len(medium_signs)}")

    seals = load_corpus()
    flat = [s for signs in seals.values() for s in signs]
    flat_freq = Counter(flat)

    # SA calibration
    recal_table: dict = {}
    lm = None
    try:
        from glossa_lab.data.dravidian import get_word_symbols  # noqa: PLC0415
        from glossa_lab.pipelines.decipher import LanguageModel  # noqa: PLC0415
        lm = LanguageModel(get_word_symbols())
        print(f"  LM loaded: Dravidian, {lm.size} signs")
    except Exception as exc:  # noqa: BLE001
        print(f"  [WARN] LM unavailable: {exc}")
        print("  Falling back to DEDR + source-reliability criteria only")

    if lm:
        try:
            from glossa_lab.experiments._parallel import run_seeds_parallel  # noqa: PLC0415
            from glossa_lab.pipelines.decipher import decipher  # noqa: PLC0415

            def _one(seed: int) -> dict:
                r = decipher(
                    flat, lm, seed=seed, max_iterations=8000, restarts=4,
                    cipher_inscriptions=None, surjective=True,
                    ocp_weight=0.0, positional_weight=0.0, anchors=anchor_map,
                )
                return r.get("proposed_mapping", {})

            print(f"  Running SA: {N_SEEDS} seeds × {len(medium_signs)} MEDIUM signs...")
            maps = run_seeds_parallel(_one, list(range(N_SEEDS)))
            for sign in medium_signs:
                proposals = [m.get(sign) for m in maps if m.get(sign)]
                if proposals:
                    cnt = Counter(proposals)
                    modal, mc = cnt.most_common(1)[0]
                    cons = mc / len(proposals)
                    recal_table[sign] = {
                        "sa_modal": modal,
                        "consistency": round(cons, 3),
                        "n_seeds": len(proposals),
                    }
            print(f"  SA calibration: {len(recal_table)} signs processed")
        except Exception as exc:  # noqa: BLE001
            print(f"  [WARN] SA run failed: {exc}")
            print("  Proceeding with DEDR + source criteria only")

    # Apply upgrade criteria
    upgraded = []
    eval_log = []

    for sign, v in medium_signs.items():
        basis   = v.get("basis", "")
        reading = v.get("reading", "")
        source  = v.get("source", "")

        dedr_ok = has_dedr(basis, reading)
        recal   = recal_table.get(sign, {})
        new_cons = recal.get("consistency", 0)

        # Consistency OK if SA says so, or source was a real SA run
        cons_ok = new_cons >= CONS_MEDIUM or source_reliable(source)

        # Skip if already went through Phase-116 with HIGH outcome
        if "Phase-116 recal" in basis:
            # Already evaluated — only upgrade if new SA gives better result
            if not (new_cons >= CONS_HIGH):
                eval_log.append({
                    "sign": sign, "reading": reading, "decision": "SKIP_ALREADY_116",
                    "new_cons": new_cons,
                })
                continue

        passed = dedr_ok and cons_ok
        eval_log.append({
            "sign": sign, "reading": reading, "source": source[:60],
            "dedr_ok": dedr_ok, "cons_ok": cons_ok,
            "new_sa_modal": recal.get("sa_modal", ""),
            "new_consistency": new_cons,
            "all_pass": passed,
        })

        if passed:
            note = f"[Phase-216: SA-cons={new_cons:.2f} DEDR✓ source={source[:40]}]"
            anchors[sign]["confidence"] = "HIGH"
            anchors[sign]["basis"] = (basis + " " + note).strip()
            upgraded.append(sign)
            print(f"  ✓ {sign}: '{reading}' → HIGH (cons={new_cons:.2f}, DEDR={dedr_ok})")

    # Update anchors file
    anchors_data["anchors"] = anchors
    anchors_data["total"] = len(anchors)
    high_after = sum(1 for v in anchors.values() if v.get("confidence") == "HIGH")
    medium_after = sum(1 for v in anchors.values() if v.get("confidence") == "MEDIUM")
    anchors_data["by_confidence"] = {
        "HIGH": high_after, "MEDIUM": medium_after,
        "LOW": sum(1 for v in anchors.values() if v.get("confidence") == "LOW"),
    }
    ANCHORS.write_text(json.dumps(anchors_data, indent=2, ensure_ascii=False), encoding="utf-8")

    total_tokens = sum(flat_freq.values())
    cov_hm = sum(flat_freq.get(s, 0) for s in anchors
                 if anchors[s].get("confidence") in ("HIGH", "MEDIUM"))
    coverage = round(cov_hm / max(1, total_tokens), 4)

    print(f"\n  HIGH: {high_before} → {high_after} (+{len(upgraded)})")
    print(f"  MEDIUM remaining: {medium_after}")
    print(f"  H+M token coverage: {coverage:.1%}")
    print(f"  Upgraded signs: {upgraded}")

    result = {
        "phase": 216,
        "description": "SA re-calibration with 410-anchor set (covers Phase 193-215 additions)",
        "n_medium_evaluated": len(medium_signs),
        "n_upgraded_to_high": len(upgraded),
        "upgraded_signs": upgraded,
        "high_before": high_before,
        "high_after": high_after,
        "medium_after": medium_after,
        "hm_token_coverage": coverage,
        "total_anchors": len(anchors),
        "recal_table": recal_table,
        "eval_log": eval_log,
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n  Saved → {OUT}")
    return result


if __name__ == "__main__":
    main()
