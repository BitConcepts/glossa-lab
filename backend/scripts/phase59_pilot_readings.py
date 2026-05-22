"""Phase-59: Full Inscription Pilot Readings.
Generates complete human-readable candidate translations for top-50 formulas.
Uses Phase-57 decipherment table + all confirmed anchors.
GPU: torch for formula clustering. Output: reports/phase59_pilot_readings.json
"""
from __future__ import annotations

import csv
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))  # add backend/ to sys.path
from glossa_lab.gpu_utils import detect_device as _detect_device  # noqa: E402

try:
    import torch
except ImportError:
    torch = None

DEVICE = _detect_device()
if DEVICE == "cuda" and torch is not None:
    print(f"[GPU] torch {torch.__version__} — device: cuda")

REPO    = Path(__file__).parents[2]
CORPUS  = REPO / "corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv"
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
P57     = REPO / "reports/phase57_decipherment_table.json"
P52     = REPO / "reports/phase52_full_decipherment_table.json"
REPORTS = REPO / "reports"; REPORTS.mkdir(exist_ok=True)
OUT     = REPORTS / "phase59_pilot_readings.json"

CONF_SYM = {"HIGH": "✓✓", "MEDIUM": "✓", "LOW": "~", "UNCERTAIN": "??", "UNREAD": "?", "SA_CANDIDATE": "(?)"}

GRAMMATICAL_ROLES = {
    "CLASSIFIER_PREFIX": "classifier/title-class",
    "CASE_MARKER_SUFFIX": "grammatical-suffix",
    "PERSON_OR_OWNER": "identity/owner",
    "STRONG_PERSON_OR_OWNER": "identity/owner",
}


def load_readings() -> dict:
    anchors = json.loads(ANCHORS.read_text("utf-8"))["anchors"]
    readings = {}
    for sign, info in anchors.items():
        r = info.get("reading", "")
        if r: readings[sign] = {"reading": r, "confidence": info.get("confidence","?"), "gloss": info.get("gloss","")}
    # Supplement with Phase-57 SA table
    sa_path = P57 if P57.exists() else (P52 if P52.exists() else None)
    if sa_path:
        table = json.loads(sa_path.read_text("utf-8"))
        for entry in table:
            sign = entry["sign"]
            if sign not in readings and entry.get("sa_reading") and entry["sa_reading"] != "?":
                readings[sign] = {"reading": entry["sa_reading"], "confidence": "SA_CANDIDATE", "gloss": "SA-derived"}
    return readings


def parse_morphology(signs: list, readings: dict) -> dict:
    """Parse inscription structure: classify each slot."""
    parsed = []
    for i, sign in enumerate(signs):
        r = readings.get(sign, {})
        reading = r.get("reading", "?")
        conf = r.get("confidence", "UNREAD")
        gloss = r.get("gloss", "")
        # Determine slot role based on position + reading
        if i == 0 and conf in ("HIGH","MEDIUM"):
            slot_role = "initial-classifier"
        elif i == len(signs)-1 and conf in ("HIGH","MEDIUM"):
            slot_role = "terminal-suffix"
        elif conf == "UNREAD":
            slot_role = "unknown"
        else:
            slot_role = "medial"
        parsed.append({
            "sign": sign, "reading": reading, "confidence": conf,
            "gloss": gloss, "position": i, "slot_role": slot_role,
            "symbol": CONF_SYM.get(conf, "?"),
        })
    return {"slots": parsed}


def render_formula(parsed: dict) -> tuple[str, str, float]:
    """Return (rendered_string, morphological_parse, coverage_pct)."""
    slots = parsed["slots"]
    parts = [f"{s['reading']}[{s['symbol']}]" for s in slots]
    rendered = " · ".join(parts)
    morph_parts = []
    for s in slots:
        if s["confidence"] in ("HIGH","MEDIUM"): morph_parts.append(s["reading"])
        elif s["confidence"] == "SA_CANDIDATE": morph_parts.append(f"({s['reading']})")
        else: morph_parts.append(f"[{s['sign']}]")
    morph = "-".join(morph_parts)
    n_known = sum(1 for s in slots if s["confidence"] in ("HIGH","MEDIUM"))
    coverage = n_known / len(slots) if slots else 0
    return rendered, morph, coverage


def main():
    print("Phase-59: Full Inscription Pilot Readings\n")
    readings = load_readings()
    print(f"  Signs with readings: {len(readings)}")
    seals: dict[str, dict] = {}
    with open(CORPUS, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            c = row["cisi_number"]; p = int(row.get("position",0) or 0)
            if c not in seals: seals[c] = {"signs": [], "site": row.get("site",""), "icon": (row.get("iconography") or "").lower()}
            while len(seals[c]["signs"]) <= p: seals[c]["signs"].append("")
            seals[c]["signs"][p] = row["letters"]
    inscriptions = [{"id": k, "signs": [s for s in v["signs"] if s], "site": v["site"], "icon": v["icon"]}
                    for k,v in seals.items() if any(v["signs"])]
    formula_counter: Counter = Counter(tuple(ins["signs"]) for ins in inscriptions)
    top50 = formula_counter.most_common(50)
    # GPU clustering
    if torch is not None:
        all_signs = sorted(set(s for pattern,_ in top50 for s in pattern))
        sidx = {s: i for i,s in enumerate(all_signs)}
        n_forms = len(top50); n_s = len(all_signs)
        mat = torch.zeros(n_forms, n_s, device=DEVICE)
        for i,(pattern,_) in enumerate(top50):
            for s in pattern:
                if s in sidx: mat[i, sidx[s]] = 1.0
        norms = mat.norm(dim=1, keepdim=True).clamp(min=1e-8)
        sim = ((mat/norms) @ (mat/norms).T).cpu()
        print(f"[GPU:{DEVICE}] Formula clustering done ({n_forms}×{n_forms})")

    decoded = []
    for pattern, count in top50:
        parsed = parse_morphology(list(pattern), readings)
        rendered, morph, coverage = render_formula(parsed)
        # Attempt a natural-language gloss for well-decoded formulas
        slot_readings = [s["reading"] for s in parsed["slots"] if s["confidence"] in ("HIGH","MEDIUM")]
        gloss_attempt = ""
        if coverage >= 0.8 and slot_readings:
            gloss_attempt = " ".join(slot_readings)
        decoded.append({
            "pattern": list(pattern), "count": count, "n_signs": len(pattern),
            "coverage_pct": round(coverage*100, 1),
            "rendered": rendered, "morphological": morph,
            "gloss_attempt": gloss_attempt,
            "slots": parsed["slots"],
        })
    decoded.sort(key=lambda x: (-x["coverage_pct"], -x["count"]))
    # Fully decoded (≥80%) pilot readings
    fully_decoded = [d for d in decoded if d["coverage_pct"] >= 80]
    print("\n=== Phase-59 Results ===")
    print(f"  Total unique formulas: {len(formula_counter)}")
    print(f"  Top-50 coverage: {len(fully_decoded)} formulas ≥80% decoded")
    print("\n  BEST PILOT READINGS:")
    for d in fully_decoded[:15]:
        print(f"  [{d['count']:3d}×] ({d['coverage_pct']:.0f}%) {d['morphological']}")
    result = {
        "_citation": {"primary": ["A.1"]},
        "gpu_device": DEVICE,
        "n_signs_with_readings": len(readings),
        "n_unique_formulas": len(formula_counter),
        "top_50_formulas": decoded,
        "fully_decoded_gte_80pct": fully_decoded[:20],
        "n_fully_decoded": len(fully_decoded),
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), "utf-8")
    print(f"Report: {OUT}")


if __name__ == "__main__":
    main()
