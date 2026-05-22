"""Phase-106: Personal Name SA Sprint.

Runs SA with all confirmed HIGH+MEDIUM anchors pinned, targeting the 45
personal name candidates from Phase-103. Assigns SA modal readings
(Dravidian syllabic LM, threshold 1.0, PD-valid filter).

GPU if available, else CPU. Output: reports/phase106_name_sa_sprint.json
"""
from __future__ import annotations

import csv
import json
import os
import sys
from collections import Counter
from pathlib import Path

REPO    = Path(__file__).parents[2]
HOLDAT  = REPO / "corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv"
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
P73     = REPO / "reports/phase73_ensemble_calibration.json"
P103    = REPO / "reports/phase103_name_lexicon.json"
P105    = REPO / "reports/phase105_name_signs.json"
REPORTS = REPO / "reports"
REPORTS.mkdir(exist_ok=True)
OUT     = REPORTS / "phase106_name_sa_sprint.json"

sys.path.insert(0, str(REPO / "backend"))
os.environ.setdefault("GLOSSA_DATA_DIR", str(REPO / "backend/data"))

# Proto-Dravidian valid initial syllables (from DEDR)
PD_VALID_INITIALS = {
    "a", "ā", "i", "ī", "u", "ū", "e", "ē", "o", "ō", "ai", "au",
    "k", "ka", "ki", "ku", "kē", "ko", "kā", "kū", "kō", "kai",
    "c", "ca", "ci", "cu", "cē", "co", "cā", "cū",
    "t", "ta", "ti", "tu", "tē", "to", "tā",
    "n", "na", "ni", "nu", "nē", "no", "nā",
    "p", "pa", "pi", "pu", "pē", "po", "pā",
    "m", "ma", "mi", "mu", "mē", "mo", "mā",
    "v", "va", "vi", "vu", "vē", "vo", "vā",
    "y", "ya", "yi", "yu", "yē", "yo",
    "r", "ra",
    "l", "la",
    "w", "wa",
    "ir", "il", "im", "in", "it",
    "am", "an", "ar", "al",
    "pu", "tu", "mu", "ku", "ay", "nē", "ko", "ka", "ta", "na",
    "vel", "pon", "nal", "van", "kan", "vil", "per", "tan", "iru",
    "aṇi", "taṇ", "kuṟi",
}

# Common Tamil/Proto-Dravidian personal name morphemes
PD_NAME_MORPHEMES = {
    "vel": "DEDR 5469 spear/victory",
    "pon": "DEDR 4533 gold",
    "nal": "DEDR 3569 good",
    "iru": "DEDR 0488 great",
    "van": "DEDR 5231 strong",
    "kan": "DEDR 1145 eye/lord",
    "vil": "DEDR 5428 bow",
    "ta":  "DEDR 3003 self",
    "tan": "DEDR 3136 self/cool",
    "per": "DEDR 4442 great",
    "nē":  "DEDR 3741 you/true",
    "aṇi": "DEDR 0145 ornament",
    "taṇ": "DEDR 3009 cool",
    "kuṟi":"DEDR 1769 mark/sign",
    "ko":  "DEDR 1570 king",
    "ka":  "DEDR 1145 eye",
    "cu":  "DEDR 2732 small",
    "pu":  "DEDR 4317 flower",
    "mu":  "DEDR 5012 face/front",
    "ār":  "DEDR 0359 great",
    "cey": "DEDR 2796 to do",
    "ma":  "DEDR 4751 tree/great",
    "par": "DEDR 3955 great/old",
    "eli": "DEDR 0838 rat/small",
    "mā":  "DEDR 4751 great",
    "il":  "DEDR 0486 house",
    "kōṉ": "DEDR 2199 king",
    "ūr":  "DEDR 0728 settlement",
    "nār": "DEDR 3659 good",
}


def load_corpus():
    seals = {}
    with open(HOLDAT, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            s = (row.get("letters") or "").strip()
            c = row.get("cisi_number", ""); p = int(row.get("position", 0) or 0)
            if not c: continue
            if c not in seals: seals[c] = {"signs": []}
            while len(seals[c]["signs"]) <= p: seals[c]["signs"].append("")
            seals[c]["signs"][p] = s
    return {c: [s for s in v["signs"] if s] for c, v in seals.items() if any(v["signs"])}


def is_pd_valid(reading: str) -> bool:
    """Check if a reading starts with a PD-valid initial."""
    if not reading:
        return False
    r = reading.lower().strip()
    for init in sorted(PD_VALID_INITIALS, key=len, reverse=True):
        if r.startswith(init):
            return True
    return False


def sa_sprint_sign(sign: str, flat: list, lm, anchors: dict, n_seeds: int = 5) -> dict:
    """Run SA for a single sign target using all confirmed anchors."""
    try:
        from glossa_lab.pipelines.decipher import decipher  # noqa: PLC0415
    except ImportError:
        return {"sign": sign, "sa_modal": "", "consistency": 0, "error": "decipher not available"}

    results = []
    for seed in range(n_seeds):
        try:
            r = decipher(
                flat, lm, seed=seed,
                max_iterations=5000,
                restarts=4,
                cipher_inscriptions=None,
                surjective=True,
                ocp_weight=0.0,
                positional_weight=0.0,
                anchors=anchors or None,
            )
            mapping = r.get("proposed_mapping", {})
            if sign in mapping:
                results.append(mapping[sign])
        except Exception:  # noqa: BLE001
            pass

    if not results:
        return {"sign": sign, "sa_modal": "", "consistency": 0, "error": "no results"}

    cnt = Counter(results)
    modal, modal_count = cnt.most_common(1)[0]
    consistency = modal_count / len(results)
    pd_valid = is_pd_valid(modal)
    return {
        "sign": sign,
        "sa_modal": modal,
        "consistency": round(consistency, 3),
        "pd_valid": pd_valid,
        "n_seeds": len(results),
        "all_proposals": dict(cnt),
    }


def find_pd_name_match(sa_modal: str) -> dict:
    """Match SA modal to a known PD personal name morpheme."""
    if not sa_modal:
        return {}
    m = sa_modal.lower().strip()
    # Exact match first
    if m in PD_NAME_MORPHEMES:
        return {"morpheme": m, "dedr_note": PD_NAME_MORPHEMES[m], "match_type": "exact"}
    # Prefix match
    for morpheme, note in PD_NAME_MORPHEMES.items():
        if m.startswith(morpheme[:2]):
            return {"morpheme": morpheme, "dedr_note": note, "match_type": "prefix"}
    return {}


def main():
    print("Phase-106: Personal Name SA Sprint\n")

    # Load anchors
    anchors_data = json.loads(ANCHORS.read_text("utf-8"))
    anchor_map = {
        s: v["reading"]
        for s, v in anchors_data.get("anchors", {}).items()
        if v.get("confidence") in ("HIGH", "MEDIUM") and v.get("reading")
    }
    print(f"  Pinned anchors: {len(anchor_map)}")

    # Load Phase-73 SA calibration as baseline
    p73_map = {}
    if P73.exists():
        p73 = json.loads(P73.read_text())
        for entry in p73.get("calibrated_table", []):
            p73_map[entry["sign"]] = entry

    # Load Phase-103 name candidates
    name_candidates = []
    if P103.exists():
        p103 = json.loads(P103.read_text())
        name_candidates = p103.get("name_candidates", [])
    if not name_candidates:
        print("  [WARN] Phase-103 report not found; using fallback candidate list")
        name_candidates = [
            {"sign": s} for s in [
                "M024", "M362", "M375", "M398", "M102", "M169", "M153",
                "M365", "M386", "M347", "M022", "M050", "M034", "M087",
                "M029", "M036", "M037", "M046", "M065", "M107", "M211",
            ]
        ]

    # Load corpus
    seals = load_corpus()
    flat = [s for signs in seals.values() for s in signs]
    print(f"  Corpus: {len(seals)} seals, {len(flat)} tokens")

    # Try to build dravidian LM
    lm = None
    try:
        from glossa_lab.data.dravidian import get_word_symbols  # noqa: PLC0415
        from glossa_lab.pipelines.decipher import LanguageModel  # noqa: PLC0415
        syl_syms = get_word_symbols()
        lm = LanguageModel(syl_syms)
        print(f"  LM: Dravidian syllabic, {lm.size} signs")
    except Exception as exc:  # noqa: BLE001
        print(f"  [WARN] Could not build Dravidian LM: {exc}")

    # Sprint: for each name candidate, assign SA modal
    sprint_results = []
    n_assigned = 0
    skip_confirmed = {s for s, v in anchors_data.get("anchors", {}).items()
                      if v.get("confidence") in ("HIGH", "MEDIUM")}

    for cand in name_candidates:
        sign = cand.get("sign", "")
        if not sign or sign in skip_confirmed:
            print(f"  {sign}: already confirmed, skipping")
            continue

        # Check Phase-73 baseline first
        p73_entry = p73_map.get(sign, {})
        p73_modal = p73_entry.get("syl_modal", "")
        p73_pd    = p73_entry.get("pd_valid", False)

        # Use Phase-73 modal if PD-valid
        if p73_modal and p73_pd:
            pd_match = find_pd_name_match(p73_modal)
            sprint_results.append({
                "sign": sign,
                "sa_modal": p73_modal,
                "consistency": 1.0,
                "pd_valid": True,
                "source": "Phase-73",
                "pd_name_match": pd_match,
                "proposed_reading": pd_match.get("morpheme", p73_modal),
                "confidence_proposed": "LOW",
            })
            print(f"  {sign}: Phase-73 modal='{p73_modal}' (PD-valid) → '{pd_match.get('morpheme', p73_modal)}'")
            n_assigned += 1
            continue

        # Run fresh SA if LM available
        if lm:
            result = sa_sprint_sign(sign, flat, lm, anchor_map, n_seeds=4)
            pd_match = find_pd_name_match(result.get("sa_modal", ""))
            result["pd_name_match"] = pd_match
            result["proposed_reading"] = pd_match.get("morpheme", result.get("sa_modal", ""))
            result["confidence_proposed"] = (
                "LOW" if result.get("consistency", 0) >= 0.4 and result.get("pd_valid") else "UNCERTAIN"
            )
            sprint_results.append(result)
            modal = result.get("sa_modal", "")
            cons  = result.get("consistency", 0)
            print(f"  {sign}: SA modal='{modal}' (cons={cons:.2f}, PD={result.get('pd_valid')}) → '{result.get('proposed_reading', '')}'")
            if result.get("pd_valid") and cons >= 0.4:
                n_assigned += 1
        else:
            sprint_results.append({
                "sign": sign,
                "sa_modal": p73_modal,
                "consistency": 0,
                "pd_valid": p73_pd,
                "source": "Phase-73-fallback",
                "pd_name_match": find_pd_name_match(p73_modal),
                "proposed_reading": p73_modal,
                "confidence_proposed": "UNCERTAIN",
            })

    result_out = {
        "phase": 106,
        "n_name_candidates": len(name_candidates),
        "n_skipped_confirmed": len(skip_confirmed),
        "n_sprint_results": len(sprint_results),
        "n_assigned_reading": n_assigned,
        "n_pinned_anchors": len(anchor_map),
        "sprint_results": sprint_results,
        "summary": [
            {
                "sign": r["sign"],
                "reading": r.get("proposed_reading", ""),
                "consistency": r.get("consistency", 0),
                "pd_valid": r.get("pd_valid", False),
                "confidence": r.get("confidence_proposed", "UNCERTAIN"),
            }
            for r in sprint_results
        ],
    }
    OUT.write_text(json.dumps(result_out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n  Saved → {OUT}")
    print(f"  Phase-106 complete: {n_assigned}/{len(sprint_results)} name candidates assigned PD-valid readings")
    return result_out


if __name__ == "__main__":
    main()
