"""Phase-224: Slot Mismatch Investigation.

Phase-220 flagged 19 P-signs where our expected positional slot (derived from
semantic reading category) doesn't match the observed CISI positional behavior.

For each mismatch, this phase:
  1. Computes the actual CISI I/M/T rate
  2. Computes the Holdat I/M/T rate for the corresponding M-sign
  3. Evaluates whether the mismatch is:
     (a) A reading error — our assigned reading is wrong
     (b) A corpus difference — CISI and Holdat have different usage patterns
     (c) A classification error — our expected_slot was wrong

Output: outputs/phase224_slot_mismatch_investigation.json
"""
from __future__ import annotations

import json
import os
import sys
import csv
from collections import Counter
from pathlib import Path

REPO    = Path(__file__).parents[2]
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
P220    = REPO / "outputs/phase220_parpola_cisi_crossref.json"
CROSSWALK = REPO / "backend/glossa_lab/data/mahadevan_parpola_crosswalk_v2.json"
HOLDAT  = REPO / "corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv"
OUT     = REPO / "outputs/phase224_slot_mismatch_investigation.json"
OUT.parent.mkdir(exist_ok=True)

sys.path.insert(0, str(REPO / "backend"))
os.environ.setdefault("GLOSSA_DATA_DIR", str(REPO / "backend/data"))

# Expected slots based on reading category (from Phase-220 logic)
TERMINAL_READINGS = {
    "ay/ā", "an/aṇ", "am/neuter", "iṉ/locative",
    "ōṭu/comitative", "il/iḷ", "ka/kaṇ", "tu/tū", "ā/āl",
}
INITIAL_READINGS = {
    "erutu", "yānai", "puli", "kāṇṭāmirukam", "māṭu", "āṉai",
    "kol/koḷ", "kōṉ",
}


def get_holdat_positional(sign: str) -> dict:
    """Get positional stats for a sign from Holdat CSV."""
    freq = 0; initial = 0; terminal = 0; medial = 0
    seals = {}
    try:
        with open(HOLDAT, encoding="utf-8") as f:
            for row in csv.DictReader(f):
                s = (row.get("letters") or "").strip()
                c = row.get("cisi_number", "")
                p = int(row.get("position", 0) or 0)
                if not c: continue
                if c not in seals: seals[c] = []
                while len(seals[c]) <= p: seals[c].append("")
                seals[c][p] = s
        for signs in seals.values():
            signs_clean = [s for s in signs if s]
            n = len(signs_clean)
            for i, s in enumerate(signs_clean):
                if s != sign: continue
                freq += 1
                if i == 0: initial += 1
                elif i == n - 1: terminal += 1
                else: medial += 1
    except Exception:  # noqa: BLE001
        pass
    if not freq:
        return {}
    return {
        "freq": freq,
        "initial_rate": round(initial / freq, 3),
        "medial_rate": round(medial / freq, 3),
        "terminal_rate": round(terminal / freq, 3),
        "holdat_slot": (
            "INITIAL" if initial / freq >= 0.55 else
            "TERMINAL" if terminal / freq >= 0.55 else
            "MEDIAL"
        ),
    }


def get_cisi_positional(sign: str, seqs) -> dict:
    freq = 0; initial = 0; terminal = 0; medial = 0
    for seq in seqs:
        n = len(seq)
        for i, s in enumerate(seq):
            if s != sign: continue
            freq += 1
            if i == 0: initial += 1
            elif i == n - 1: terminal += 1
            else: medial += 1
    if not freq:
        return {}
    return {
        "freq": freq,
        "initial_rate": round(initial / freq, 3),
        "medial_rate": round(medial / freq, 3),
        "terminal_rate": round(terminal / freq, 3),
        "cisi_slot": (
            "INITIAL" if initial / freq >= 0.55 else
            "TERMINAL" if terminal / freq >= 0.55 else
            "MEDIAL"
        ),
    }


def classify_mismatch(our_reading: str, expected_slot: str,
                      cisi_slot: str, holdat_stats: dict) -> dict:
    """Classify the nature of the mismatch."""
    holdat_slot = holdat_stats.get("holdat_slot", "UNKNOWN")

    # Case 1: Both CISI and Holdat agree but differ from our expected
    if cisi_slot == holdat_slot and cisi_slot != expected_slot:
        return {
            "verdict": "READING_ERROR",
            "confidence": "HIGH",
            "note": (
                f"Both CISI ({cisi_slot}) and Holdat ({holdat_slot}) agree against "
                f"our expected slot ({expected_slot}). Our reading '{our_reading}' "
                f"may be wrong — the sign behaves as {cisi_slot} in both corpora."
            ),
        }
    # Case 2: CISI and Holdat disagree
    elif cisi_slot != holdat_slot:
        return {
            "verdict": "CORPUS_DIFFERENCE",
            "confidence": "MEDIUM",
            "note": (
                f"CISI slot ({cisi_slot}) ≠ Holdat slot ({holdat_slot}). "
                f"Expected: {expected_slot}. "
                "Different corpus composition or site-specific variation. "
                "Not necessarily a reading error."
            ),
        }
    # Case 3: CISI matches our expected but Holdat doesn't
    elif cisi_slot == expected_slot:
        return {
            "verdict": "HOLDAT_OUTLIER",
            "confidence": "LOW",
            "note": (
                f"CISI matches expected ({expected_slot}) but Holdat disagrees ({holdat_slot}). "
                "Possibly Holdat has unusual usage for this sign. Reading likely OK."
            ),
        }
    else:
        return {
            "verdict": "CLASSIFICATION_ERROR",
            "confidence": "LOW",
            "note": (
                f"Our expected slot classification ({expected_slot}) may be wrong. "
                f"CISI={cisi_slot}, Holdat={holdat_slot}. Reading '{our_reading}' "
                "needs re-evaluation of slot expectation."
            ),
        }


def main():
    print("Phase-224: Slot Mismatch Investigation\n")

    # Load data
    anchors_data = json.loads(ANCHORS.read_text("utf-8"))
    anchors = anchors_data.get("anchors", {})

    cw_data = json.loads(CROSSWALK.read_text("utf-8"))
    crosswalk = cw_data.get("crosswalk", {})
    p_to_m = {}
    for m_id, entry in crosswalk.items():
        p_id = str(entry.get("parpola_id", "") or entry.get("parpola_num", ""))
        if p_id.startswith("P"):
            p_to_m[p_id] = m_id
        elif p_id.isdigit():
            p_to_m[f"P{int(p_id):03d}"] = m_id

    # Load Phase-220 mismatches
    if not P220.exists():
        print("  [ERROR] Phase-220 output not found")
        return {}

    p220 = json.loads(P220.read_text("utf-8"))
    mismatch_psigns = p220.get("slot_mismatches", [])
    cat_a = p220.get("category_a_confirmed", [])
    # Build lookup for cat-A
    cat_a_map = {r["p_sign"]: r for r in cat_a}

    print(f"  Slot mismatches to investigate: {len(mismatch_psigns)}")

    # Load CISI
    from glossa_lab.data import indus_cisi  # noqa: PLC0415
    seqs = indus_cisi.get_corpus_inscriptions()

    print("  Computing mismatch classifications...\n")

    investigations = []
    reading_errors = []
    corpus_differences = []

    for p_sign in mismatch_psigns:
        rec = cat_a_map.get(p_sign, {})
        m_id = p_to_m.get(p_sign, "")
        our_reading = rec.get("our_reading", anchors.get(m_id, {}).get("reading", ""))
        expected_slot = rec.get("slot_cross_validate", {}).get("our_expected_slot", "MEDIAL")
        cisi_slot = rec.get("slot_cross_validate", {}).get("cisi_slot", rec.get("dominant_slot", "?"))

        # Get Holdat positional if available
        holdat_stats = {}
        if m_id:
            holdat_stats = get_holdat_positional(m_id)

        cisi_stats = get_cisi_positional(p_sign, seqs)

        classification = classify_mismatch(our_reading, expected_slot,
                                           cisi_slot, holdat_stats)

        inv = {
            "p_sign": p_sign,
            "m_id": m_id,
            "our_reading": our_reading,
            "our_confidence": anchors.get(m_id, {}).get("confidence", "?"),
            "expected_slot": expected_slot,
            "cisi_slot": cisi_slot,
            "holdat_slot": holdat_stats.get("holdat_slot", "NO_HOLDAT_DATA"),
            "cisi_stats": cisi_stats,
            "holdat_stats": holdat_stats,
            "classification": classification,
        }
        investigations.append(inv)

        verdict = classification["verdict"]
        print(f"  {p_sign:6s} ({m_id:5s}): '{our_reading}'")
        print(f"    Expected={expected_slot} CISI={cisi_slot} Holdat={holdat_stats.get('holdat_slot','N/A')}")
        print(f"    → {verdict}: {classification['note'][:80]}")

        if verdict == "READING_ERROR":
            reading_errors.append(p_sign)
        elif verdict == "CORPUS_DIFFERENCE":
            corpus_differences.append(p_sign)

    print(f"\n  READING_ERROR verdicts: {len(reading_errors)} — {reading_errors}")
    print(f"  CORPUS_DIFFERENCE verdicts: {len(corpus_differences)}")
    print(f"  Other: {len(investigations) - len(reading_errors) - len(corpus_differences)}")

    # Summary: which reading errors are most actionable?
    actionable = [inv for inv in investigations
                  if inv["classification"]["verdict"] == "READING_ERROR"
                  and inv["our_confidence"] in ("HIGH", "MEDIUM")]
    if actionable:
        print(f"\n  ACTIONABLE (H+M reading errors): {len(actionable)}")
        for inv in actionable:
            print(f"    {inv['p_sign']}/{inv['m_id']}: '{inv['our_reading']}' "
                  f"expected={inv['expected_slot']} actual={inv['cisi_slot']}")

    result = {
        "phase": 224,
        "n_mismatches_investigated": len(investigations),
        "reading_errors": reading_errors,
        "corpus_differences": corpus_differences,
        "actionable_hm_errors": [inv["p_sign"] for inv in actionable],
        "investigations": investigations,
        "summary": {
            "READING_ERROR": len(reading_errors),
            "CORPUS_DIFFERENCE": len(corpus_differences),
            "OTHER": len(investigations) - len(reading_errors) - len(corpus_differences),
        },
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n  Saved → {OUT}")
    return result


if __name__ == "__main__":
    main()
