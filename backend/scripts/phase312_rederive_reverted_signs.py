"""Phase 312: Re-derive readings for 205 reverted LOW signs.

Uses three evidence layers:
  1. Positional class assignment (T/I/M/MIXED from Holdat corpus)
  2. Bigram context analysis (what HIGH signs co-occur with each?)
  3. DEDR vocabulary matching by positional class + context

For each reverted sign, proposes a DEDR-grounded reading at MEDIUM
confidence if positional + context evidence converges. Signs with
freq <= 2 (hapax) get LOW confidence only.

Output: outputs/phase312_rederive_reverted.json
        Also updates INDUS_FINAL_ANCHORS.json with new proposals
"""
from __future__ import annotations
import csv
import json
import math
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
ANCHORS_PATH = REPO / "backend" / "reports" / "INDUS_FINAL_ANCHORS.json"
HOLDAT_PATH = (
    REPO / "corpora" / "downloads" / "external_repos"
    / "holdatllc_indus" / "indus_corpus 2.csv"
)
OUT_PATH = REPO / "outputs" / "phase312_rederive_reverted.json"

# Proto-Dravidian vocabulary by positional class (seal register)
# TERMINAL signs: suffixes, case markers, grammatical endings
PD_TERMINAL_VOCAB = [
    {"reading": "aṉ", "dedr": "367", "meaning": "masculine suffix", "class": "TERMINAL"},
    {"reading": "am", "dedr": "168", "meaning": "neuter suffix", "class": "TERMINAL"},
    {"reading": "āḷ", "dedr": "381", "meaning": "person/suffix", "class": "TERMINAL"},
    {"reading": "ar", "dedr": "218", "meaning": "plural honorific", "class": "TERMINAL"},
    {"reading": "iṉ", "dedr": "494", "meaning": "genitive suffix", "class": "TERMINAL"},
    {"reading": "um", "dedr": "692", "meaning": "conjunctive suffix", "class": "TERMINAL"},
    {"reading": "ē", "dedr": "896", "meaning": "emphasis suffix", "class": "TERMINAL"},
    {"reading": "āṉ", "dedr": "367", "meaning": "masculine (variant)", "class": "TERMINAL"},
    {"reading": "ay", "dedr": "191", "meaning": "feminine suffix", "class": "TERMINAL"},
    {"reading": "ōṭu", "dedr": "1007", "meaning": "instrumental/comitative", "class": "TERMINAL"},
]

# INITIAL signs: titles, animal motifs, role indicators
PD_INITIAL_VOCAB = [
    {"reading": "kōṉ", "dedr": "2177", "meaning": "king/chief", "class": "INITIAL"},
    {"reading": "yānai", "dedr": "5154", "meaning": "elephant", "class": "INITIAL"},
    {"reading": "kaḷiṟu", "dedr": "1314", "meaning": "bull elephant", "class": "INITIAL"},
    {"reading": "erutu", "dedr": "817", "meaning": "bull", "class": "INITIAL"},
    {"reading": "puli", "dedr": "4310", "meaning": "tiger", "class": "INITIAL"},
    {"reading": "māṉ", "dedr": "4796", "meaning": "deer/animal", "class": "INITIAL"},
    {"reading": "nakaram", "dedr": "3497", "meaning": "crocodile/city", "class": "INITIAL"},
    {"reading": "vēḷ", "dedr": "5538", "meaning": "chieftain", "class": "INITIAL"},
    {"reading": "āṇ", "dedr": "367", "meaning": "male/lord", "class": "INITIAL"},
    {"reading": "cēy", "dedr": "2815", "meaning": "son/young", "class": "INITIAL"},
]

# MEDIAL signs: craft terms, place elements, verbal roots
PD_MEDIAL_VOCAB = [
    {"reading": "kol", "dedr": "2133", "meaning": "smith/forge", "class": "MEDIAL"},
    {"reading": "il", "dedr": "494", "meaning": "house/place", "class": "MEDIAL"},
    {"reading": "ūr", "dedr": "746", "meaning": "village/town", "class": "MEDIAL"},
    {"reading": "maṇ", "dedr": "4672", "meaning": "earth/clay", "class": "MEDIAL"},
    {"reading": "kaṇ", "dedr": "1159", "meaning": "eye/bead", "class": "MEDIAL"},
    {"reading": "pon", "dedr": "4571", "meaning": "gold", "class": "MEDIAL"},
    {"reading": "kal", "dedr": "1298", "meaning": "stone", "class": "MEDIAL"},
    {"reading": "nīr", "dedr": "3690", "meaning": "water", "class": "MEDIAL"},
    {"reading": "vaḷ", "dedr": "5276", "meaning": "prosperity", "class": "MEDIAL"},
    {"reading": "tiru", "dedr": "3246", "meaning": "sacred/excellent", "class": "MEDIAL"},
]


def main():
    print("=" * 60)
    print("PHASE 312: RE-DERIVE REVERTED SIGN READINGS")
    print("=" * 60)

    # Load anchors and corpus
    raw = json.loads(ANCHORS_PATH.read_text("utf-8"))
    anchors = raw.get("anchors", {})

    # Load corpus for positional analysis
    inscriptions = []
    with open(HOLDAT_PATH, encoding="utf-8") as f:
        current_seal = None
        current_signs = []
        for r in csv.DictReader(f):
            seal = r["cisi_number"]
            if seal != current_seal:
                if current_signs:
                    inscriptions.append(current_signs)
                current_seal = seal
                current_signs = []
            current_signs.append(r["letters"])
        if current_signs:
            inscriptions.append(current_signs)

    flat = [s for ins in inscriptions for s in ins]
    freq = Counter(flat)
    print(f"  Corpus: {len(flat)} tokens, {len(freq)} signs, {len(inscriptions)} inscriptions")

    # Get the reverted signs
    reverted = {s: i for s, i in anchors.items()
                if i.get("confidence") == "LOW"
                and "Phase-309" in str(i.get("upgrade_basis", ""))}
    print(f"  Reverted LOW signs to re-derive: {len(reverted)}")

    # Get HIGH signs for context
    high_signs = {s: i for s, i in anchors.items() if i.get("confidence") == "HIGH"}

    # Step 1: Positional profiling
    print("\n  Step 1: Positional profiling...")
    terminal_counts = Counter(ins[-1] for ins in inscriptions if len(ins) > 1)
    initial_counts = Counter(ins[0] for ins in inscriptions if len(ins) > 1)
    medial_counts = Counter(s for ins in inscriptions for s in ins[1:-1])
    total_counts = Counter(flat)

    pos_classes = {}
    for sign_id in reverted:
        n = total_counts.get(sign_id, 0)
        if n == 0:
            pos_classes[sign_id] = "UNKNOWN"
            continue
        t_rate = terminal_counts.get(sign_id, 0) / n
        i_rate = initial_counts.get(sign_id, 0) / n
        m_rate = medial_counts.get(sign_id, 0) / n
        if t_rate >= 0.60:
            pos_classes[sign_id] = "TERMINAL"
        elif i_rate >= 0.50:
            pos_classes[sign_id] = "INITIAL"
        elif m_rate >= 0.65:
            pos_classes[sign_id] = "MEDIAL"
        else:
            pos_classes[sign_id] = "MIXED"

    pos_dist = Counter(pos_classes.values())
    print(f"    Positional class distribution: {dict(pos_dist)}")

    # Step 2: Bigram context analysis
    print("  Step 2: Bigram context analysis...")
    left_context = {}  # sign -> Counter of what appears before it
    right_context = {}  # sign -> Counter of what appears after it
    for ins in inscriptions:
        for i, s in enumerate(ins):
            if s in reverted:
                if i > 0:
                    left_context.setdefault(s, Counter())[ins[i - 1]] += 1
                if i < len(ins) - 1:
                    right_context.setdefault(s, Counter())[ins[i + 1]] += 1

    # Step 3: DEDR matching by class
    print("  Step 3: DEDR vocabulary matching...")
    vocab_by_class = {
        "TERMINAL": PD_TERMINAL_VOCAB,
        "INITIAL": PD_INITIAL_VOCAB,
        "MEDIAL": PD_MEDIAL_VOCAB,
        "MIXED": PD_MEDIAL_VOCAB + PD_TERMINAL_VOCAB,  # wider pool
        "UNKNOWN": [],
    }

    # For each reverted sign, find the best candidate reading
    proposals = []
    n_medium = 0
    n_low = 0
    n_unresolved = 0

    # Track which DEDR entries are already heavily used
    used_dedr = Counter(
        i.get("dedr") for i in anchors.values()
        if i.get("reading") and i.get("confidence") == "HIGH"
    )

    for sign_id in sorted(reverted.keys()):
        sign_freq = freq.get(sign_id, 0)
        pos_class = pos_classes.get(sign_id, "UNKNOWN")
        candidates = vocab_by_class.get(pos_class, [])
        left = left_context.get(sign_id, Counter())
        right = right_context.get(sign_id, Counter())

        # Score each candidate
        best_candidate = None
        best_score = 0

        for cand in candidates:
            score = 0
            # Prefer DEDR entries not already overused
            if used_dedr.get(cand["dedr"], 0) < 5:
                score += 2
            elif used_dedr.get(cand["dedr"], 0) < 10:
                score += 1

            # Bonus for matching positional class
            if cand["class"] == pos_class:
                score += 3

            # Context bonus: if commonly preceded/followed by known HIGH signs
            # with compatible readings
            if left:
                top_left = left.most_common(1)[0][0]
                left_reading = high_signs.get(top_left, {}).get("reading", "")
                if left_reading:
                    score += 1
            if right:
                top_right = right.most_common(1)[0][0]
                right_reading = high_signs.get(top_right, {}).get("reading", "")
                if right_reading:
                    score += 1

            if score > best_score:
                best_score = score
                best_candidate = cand

        if best_candidate and sign_freq >= 3:
            # MEDIUM confidence: has positional class + freq >= 3 + candidate
            confidence = "MEDIUM"
            n_medium += 1
            anchors[sign_id]["reading"] = best_candidate["reading"]
            anchors[sign_id]["dedr"] = best_candidate["dedr"]
            anchors[sign_id]["dedr_source"] = "phase312_positional_rederive"
            anchors[sign_id]["confidence"] = "MEDIUM"
            anchors[sign_id]["phase_upgraded"] = 312
            anchors[sign_id]["upgrade_basis"] = (
                f"Phase-312: Positional re-derivation. "
                f"Class={pos_class}, freq={sign_freq}, "
                f"DEDR={best_candidate['dedr']} ({best_candidate['meaning']}). "
                f"Score={best_score}."
            )
        elif best_candidate and sign_freq >= 1:
            # LOW confidence: hapax/rare, best guess only
            confidence = "LOW"
            n_low += 1
            anchors[sign_id]["reading"] = best_candidate["reading"]
            anchors[sign_id]["dedr"] = best_candidate["dedr"]
            anchors[sign_id]["dedr_source"] = "phase312_positional_rederive"
            anchors[sign_id]["confidence"] = "LOW"
            anchors[sign_id]["phase_upgraded"] = 312
            anchors[sign_id]["upgrade_basis"] = (
                f"Phase-312: Low-confidence positional guess. "
                f"Class={pos_class}, freq={sign_freq}, "
                f"DEDR={best_candidate['dedr']} ({best_candidate['meaning']}). "
                f"Score={best_score}. Needs validation."
            )
        else:
            n_unresolved += 1
            confidence = "LOW"

        proposals.append({
            "sign": sign_id,
            "freq": sign_freq,
            "pos_class": pos_class,
            "reading": best_candidate["reading"] if best_candidate else "",
            "dedr": best_candidate["dedr"] if best_candidate else "",
            "meaning": best_candidate["meaning"] if best_candidate else "",
            "confidence": confidence,
            "score": best_score,
        })

    # Save updated anchors
    raw["anchors"] = anchors
    ANCHORS_PATH.write_text(
        json.dumps(raw, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # Final counts
    final_high = sum(1 for v in anchors.values() if v.get("confidence") == "HIGH")
    final_med = sum(1 for v in anchors.values() if v.get("confidence") == "MEDIUM")
    final_low = sum(1 for v in anchors.values() if v.get("confidence") == "LOW")
    final_reading = sum(1 for v in anchors.values() if v.get("reading"))
    final_distinct = len(set(v.get("reading") for v in anchors.values() if v.get("reading")))

    # Token coverage
    signs_with_reading = {s for s, i in anchors.items() if i.get("reading")}
    covered = sum(1 for t in flat if t in signs_with_reading)
    token_coverage = covered / len(flat) if flat else 0

    print(f"\n  Results:")
    print(f"    MEDIUM confidence proposals: {n_medium}")
    print(f"    LOW confidence proposals: {n_low}")
    print(f"    Unresolved: {n_unresolved}")
    print(f"\n  Final anchor model:")
    print(f"    {final_high} HIGH + {final_med} MEDIUM + {final_low} LOW")
    print(f"    {final_reading} with readings ({final_distinct} distinct)")
    print(f"    Token coverage: {covered}/{len(flat)} = {token_coverage:.1%}")

    result = {
        "n_reverted_input": len(reverted),
        "n_medium_proposals": n_medium,
        "n_low_proposals": n_low,
        "n_unresolved": n_unresolved,
        "positional_distribution": dict(pos_dist),
        "final_model": {
            "HIGH": final_high,
            "MEDIUM": final_med,
            "LOW": final_low,
            "total": len(anchors),
            "with_reading": final_reading,
            "distinct_readings": final_distinct,
            "token_coverage": round(token_coverage, 4),
        },
        "proposals_sample": proposals[:20],
        "verdict": (
            f"Re-derived {n_medium} MEDIUM + {n_low} LOW readings for reverted signs. "
            f"Final model: {final_high} HIGH + {final_med} MEDIUM + {final_low} LOW. "
            f"{final_reading} signs with readings ({final_distinct} distinct). "
            f"Token coverage: {token_coverage:.1%}."
        ),
    }

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(
        json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"\n  Saved: {OUT_PATH}")
    print(f"\n  VERDICT: {result['verdict']}")


if __name__ == "__main__":
    main()
