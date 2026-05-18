"""Phase-112: Grammar-Driven Slot Inference.

For seals with pattern [CONFIRMED]-[X]-[CONFIRMED], infers X from
Dravidian phonotactics + grammar slot constraints. The 6-slot grammar
derived from Phases 74-108:

  INITIAL  → animal classifier or personal name prefix
  MEDIAL   → personal name body or title
  TERMINAL → case suffix or classifier suffix

CPU only. Output: reports/phase112_grammar_slot_inference.json
"""
from __future__ import annotations
import csv, json
from collections import Counter, defaultdict
from pathlib import Path

REPO    = Path(__file__).parents[2]
HOLDAT  = REPO / "corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv"
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
P73     = REPO / "reports/phase73_ensemble_calibration.json"
REPORTS = REPO / "reports"
REPORTS.mkdir(exist_ok=True)
OUT     = REPORTS / "phase112_grammar_slot_inference.json"

# Grammar slot definitions (from Phases 74-108)
TERMINAL_SIGNS = {"M342", "M176", "M367", "M391", "M336", "M089", "M328",
                  "M162", "M305", "M012", "M233"}
INITIAL_SIGNS  = {"M006", "M016", "M045", "M062", "M047", "M039", "M040",
                  "M001", "M007", "M057", "M060", "M080", "M013"}
GENITIVE_SIGNS = {"M267"}
TITLE_SIGNS    = {"M099", "M073", "M059", "M030", "M077", "M018", "M017",
                  "M020", "M041"}

# PD name elements by slot type
SLOT_CANDIDATES = {
    "NAME_AFTER_ANIMAL":    ["vel", "nal", "van", "kan", "per", "tan", "nē", "aṇi", "taṇ", "kuṟi"],
    "NAME_AFTER_GENITIVE":  ["vel", "nal", "van", "per", "ko", "ma", "iru"],
    "MEDIAL_BETWEEN_CONF":  ["ka", "mu", "pu", "tu", "na", "va", "cu", "ta"],
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


def infer_from_context(prev: str, nxt: str, confirmed: set) -> dict:
    """Infer grammar slot and candidate readings from surrounding confirmed signs."""
    prev_is_animal   = prev in INITIAL_SIGNS
    prev_is_genitive = prev in GENITIVE_SIGNS
    prev_is_title    = prev in TITLE_SIGNS
    nxt_is_suffix    = nxt in TERMINAL_SIGNS
    nxt_is_genitive  = nxt in GENITIVE_SIGNS

    if prev_is_animal and nxt_is_suffix:
        return {"slot": "NAME_AFTER_ANIMAL", "confidence": "INFERRED",
                "candidates": SLOT_CANDIDATES["NAME_AFTER_ANIMAL"],
                "pattern": f"[ANIMAL]-[X]-[SUFFIX]"}
    elif prev_is_genitive and nxt_is_suffix:
        return {"slot": "NAME_AFTER_GENITIVE", "confidence": "INFERRED",
                "candidates": SLOT_CANDIDATES["NAME_AFTER_GENITIVE"],
                "pattern": f"[GENITIVE]-[X]-[SUFFIX]"}
    elif prev in confirmed and nxt in confirmed:
        return {"slot": "MEDIAL_BETWEEN_CONF", "confidence": "INFERRED",
                "candidates": SLOT_CANDIDATES["MEDIAL_BETWEEN_CONF"],
                "pattern": f"[CONF]-[X]-[CONF]"}
    return {}


def main():
    print("Phase-112: Grammar-Driven Slot Inference\n")

    anchors_data = json.loads(ANCHORS.read_text("utf-8"))
    anchors = anchors_data.get("anchors", {})
    confirmed = {s for s, v in anchors.items() if v.get("confidence") in ("HIGH", "MEDIUM")}
    print(f"  Confirmed signs: {len(confirmed)}")

    p73_map = {}
    if P73.exists():
        for entry in json.loads(P73.read_text()).get("calibrated_table", []):
            p73_map[entry["sign"]] = entry

    seals = load_corpus()
    flat_freq = Counter(s for signs in seals.values() for s in signs)
    print(f"  Corpus: {len(seals)} seals")

    # For each unread sign in a grammatical context, collect inferences
    sign_inferences: dict[str, list] = defaultdict(list)

    for cisi_id, signs in seals.items():
        n = len(signs)
        for i, sign in enumerate(signs):
            if sign in confirmed or sign not in flat_freq:
                continue
            prev = signs[i - 1] if i > 0 else ""
            nxt  = signs[i + 1] if i < n - 1 else ""
            inf  = infer_from_context(prev, nxt, confirmed)
            if inf:
                inf["prev"] = prev; inf["next"] = nxt
                sign_inferences[sign].append(inf)

    print(f"  Signs with grammar-slot inference: {len(sign_inferences)}")

    # Build final inference table
    inference_table = []
    for sign, infs in sign_inferences.items():
        freq = flat_freq.get(sign, 0)
        slots = Counter(i["slot"] for i in infs)
        dominant_slot = slots.most_common(1)[0][0] if slots else "UNKNOWN"
        all_candidates: Counter = Counter()
        for inf in infs:
            for cand in inf.get("candidates", []):
                all_candidates[cand] += 1
        top_candidates = [c for c, _ in all_candidates.most_common(5)]

        # Cross-reference with Phase-73 SA modal
        p73 = p73_map.get(sign, {})
        sa_modal = p73.get("syl_modal", "")
        sa_pd    = p73.get("pd_valid", False)

        # Inferred reading = SA modal if PD-valid and in candidates, else top candidate
        inferred = ""
        if sa_modal and sa_pd:
            for cand in top_candidates:
                if sa_modal.startswith(cand[:2]) or cand.startswith(sa_modal[:2]):
                    inferred = cand
                    break
            if not inferred:
                inferred = sa_modal
        elif top_candidates:
            inferred = top_candidates[0]

        inference_table.append({
            "sign": sign,
            "freq": freq,
            "n_grammar_contexts": len(infs),
            "dominant_slot": dominant_slot,
            "slot_counts": dict(slots),
            "top_candidates": top_candidates,
            "inferred_reading": inferred,
            "sa_modal": sa_modal,
            "sa_pd_valid": sa_pd,
            "sample_patterns": list(set(f"{i['prev']}-[{sign}]-{i['next']}"
                                         for i in infs[:5])),
        })

    inference_table.sort(key=lambda x: -x["n_grammar_contexts"])
    print(f"  Total inferences: {sum(e['n_grammar_contexts'] for e in inference_table)}")

    # Stats
    have_reading = [e for e in inference_table if e["inferred_reading"]]
    print(f"  Signs with inferred reading: {len(have_reading)}")

    # Coverage estimate including inferred
    inferred_tokens = sum(flat_freq.get(e["sign"], 0) for e in have_reading)
    total_tokens = sum(flat_freq.values())
    conf_tokens  = sum(flat_freq.get(s, 0) for s in confirmed)
    print(f"  Additional tokens from grammar inference: {inferred_tokens}")
    print(f"  Potential coverage (H+M + inferred): {(conf_tokens+inferred_tokens)/total_tokens:.1%}")

    result = {
        "phase": 112,
        "n_signs_inferred": len(inference_table),
        "n_with_reading": len(have_reading),
        "additional_token_coverage": round(inferred_tokens / max(1, total_tokens), 4),
        "potential_total_coverage": round((conf_tokens + inferred_tokens) / max(1, total_tokens), 4),
        "inference_table": inference_table,
        "top_20": inference_table[:20],
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n  Saved → {OUT}")
    print(f"  Phase-112 complete: {len(have_reading)} grammar-inferred readings, potential {result['potential_total_coverage']:.1%} coverage")
    return result


if __name__ == "__main__":
    main()
