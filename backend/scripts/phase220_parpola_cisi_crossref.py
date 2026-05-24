"""Phase-220: Parpola/CISI Sign Cross-Reference.

Expands the decipherment beyond the 64 Holdat/M77 signs by analysing the
181 distinct P-numbered signs in the CISI corpus (Parpola numbering).

Strategy:
  1. Load CISI corpus (P-numbers from mayig/CISI, 178 inscriptions)
  2. Build P-sign → M-sign mapping via mahadevan_parpola_crosswalk_v2.json
  3. Find P-signs that appear frequently in CISI but are NOT in our M77
     anchor set (i.e. outside Holdat coverage)
  4. Compute positional profiles (I/M/T rates) from CISI for all P-signs
  5. Cross-reference parpola_phonemes.json for Parpola's proposed reading
  6. Cross-validate our crosswalk anchor readings against CISI positional
     profiles to check consistency
  7. Propose new CANDIDATE anchors from high-frequency unread P-signs

Output: outputs/phase220_parpola_cisi_crossref.json
Does NOT modify INDUS_FINAL_ANCHORS.json (read-only analysis)
"""
from __future__ import annotations

import json
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPO     = Path(__file__).parents[2]
ANCHORS  = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
CROSSWALK = REPO / "backend/glossa_lab/data/mahadevan_parpola_crosswalk_v2.json"
PARPHON  = REPO / "backend/glossa_lab/data/parpola_phonemes.json"
OUT      = REPO / "outputs/phase220_parpola_cisi_crossref.json"
OUT.parent.mkdir(exist_ok=True)

sys.path.insert(0, str(REPO / "backend"))
os.environ.setdefault("GLOSSA_DATA_DIR", str(REPO / "backend/data"))

MIN_FREQ_NEW   = 5   # minimum CISI frequency to report a new candidate
CONS_THRESHOLD = 0.55  # I/M/T dominance threshold for positional classification


def load_cisi():
    from glossa_lab.data import indus_cisi  # noqa: PLC0415
    return indus_cisi.get_corpus_inscriptions()


def compute_positional_profiles(seqs: list[list]) -> dict:
    """Compute I/M/T rates for each sign across all sequences."""
    freq: Counter = Counter()
    initial: Counter = Counter()
    terminal: Counter = Counter()
    medial: Counter = Counter()

    for seq in seqs:
        if not seq:
            continue
        n = len(seq)
        for i, s in enumerate(seq):
            freq[s] += 1
            if i == 0:
                initial[s] += 1
            elif i == n - 1:
                terminal[s] += 1
            else:
                medial[s] += 1

    profiles = {}
    for sign, cnt in freq.items():
        i_rate = initial[sign] / cnt
        t_rate = terminal[sign] / cnt
        m_rate = medial[sign] / cnt
        slot = "MEDIAL"
        if i_rate >= CONS_THRESHOLD:
            slot = "INITIAL"
        elif t_rate >= CONS_THRESHOLD:
            slot = "TERMINAL"
        profiles[sign] = {
            "freq": cnt,
            "initial_rate": round(i_rate, 3),
            "medial_rate": round(m_rate, 3),
            "terminal_rate": round(t_rate, 3),
            "dominant_slot": slot,
        }
    return profiles


def main():
    print("Phase-220: Parpola/CISI Sign Cross-Reference\n")

    # Load data
    anchors_data = json.loads(ANCHORS.read_text("utf-8"))
    anchors = anchors_data.get("anchors", {})
    confirmed = {s for s, v in anchors.items()
                 if v.get("confidence") in ("HIGH", "MEDIUM")}
    print(f"  Current confirmed anchors (H+M): {len(confirmed)}")

    cw_data = json.loads(CROSSWALK.read_text("utf-8"))
    crosswalk = cw_data.get("crosswalk", {})  # M-ID -> {parpola_id, reading, ...}
    # Build reverse: P-number-string -> M-ID
    p_to_m: dict[str, str] = {}
    m_to_p: dict[str, str] = {}
    for m_id, entry in crosswalk.items():
        p_id = str(entry.get("parpola_id", "") or entry.get("parpola_num", ""))
        if p_id:
            # Normalise to 'PXXX' format
            if p_id.startswith("P"):
                pkey = p_id
            elif p_id.isdigit():
                pkey = f"P{int(p_id):03d}"
            else:
                pkey = p_id
            p_to_m[pkey] = m_id
            m_to_p[m_id] = pkey

    pp_data = json.loads(PARPHON.read_text("utf-8"))
    phoneme_map = pp_data.get("phoneme_map", {})  # key = int string e.g. "47"
    # Build P-key -> parpola reading
    parpola_readings: dict[str, dict] = {}
    for num_str, entry in phoneme_map.items():
        if isinstance(num_str, str) and num_str.isdigit():
            pkey = f"P{int(num_str):03d}"
            parpola_readings[pkey] = entry

    # Load CISI corpus
    try:
        seqs = load_cisi()
    except Exception as exc:  # noqa: BLE001
        print(f"  [ERROR] Failed to load CISI: {exc}")
        return {"error": str(exc)}

    print(f"  CISI inscriptions: {len(seqs)}")

    # Compute positional profiles
    profiles = compute_positional_profiles(seqs)
    all_cisi_signs = sorted(profiles.keys(),
                            key=lambda s: -profiles[s]["freq"])
    print(f"  Distinct CISI P-signs: {len(all_cisi_signs)}")

    # Categorise CISI signs
    # Category A: P-signs that map to M-signs with H+M readings (in our anchor set)
    # Category B: P-signs that map to M-signs but UNREAD in our system
    # Category C: P-signs with NO M-number mapping (new territory)
    cat_a = []  # mapped + confirmed
    cat_b = []  # mapped but unread/LOW
    cat_c = []  # not in crosswalk — potentially new

    for p_sign in all_cisi_signs:
        prof = profiles[p_sign]
        m_id = p_to_m.get(p_sign)
        our_reading = ""
        our_conf = "UNREAD"

        if m_id and m_id in anchors:
            our_conf = anchors[m_id].get("confidence", "UNREAD")
            our_reading = anchors[m_id].get("reading", "")
        elif m_id:
            our_conf = "UNREAD (in crosswalk)"

        par_entry = parpola_readings.get(p_sign, {})
        par_reading = par_entry.get("phoneme", "")
        par_conf = par_entry.get("confidence", "")

        record = {
            "p_sign": p_sign,
            "m_id": m_id or "",
            "freq_cisi": prof["freq"],
            "dominant_slot": prof["dominant_slot"],
            "initial_rate": prof["initial_rate"],
            "terminal_rate": prof["terminal_rate"],
            "our_reading": our_reading,
            "our_confidence": our_conf,
            "parpola_phoneme": par_reading,
            "parpola_confidence": par_conf,
        }

        if m_id and our_conf in ("HIGH", "MEDIUM"):
            cat_a.append(record)
        elif m_id:
            cat_b.append(record)
        else:
            cat_c.append(record)

    print(f"\n  Category A (mapped + H+M reading): {len(cat_a)} signs")
    print(f"  Category B (mapped but unread/LOW): {len(cat_b)} signs")
    print(f"  Category C (not in M77 crosswalk):  {len(cat_c)} signs")

    # --- Category A: Cross-validate our readings against CISI positions ---
    print("\n  Cross-validation: our reading vs CISI positional slot")
    slot_mismatches = []
    for rec in cat_a:
        p_sign = rec["p_sign"]
        our_slot = "TERMINAL" if rec["our_reading"].endswith(
            ("ay/ā", "an/aṇ", "am", "iṉ", "ōṭu", "il/iḷ", "ka/kaṇ", "tu/tū", "ā/āl")
        ) else ("INITIAL" if rec["our_reading"] in (
            "erutu", "yānai", "puli", "kāṇṭāmirukam", "māṭu", "āṉai",
            "kol/koḷ", "kōṉ",
        ) else "MEDIAL")
        cisi_slot = rec["dominant_slot"]
        match = (our_slot == cisi_slot) or cisi_slot == "MEDIAL"  # medial is flexible
        rec["slot_cross_validate"] = {
            "our_expected_slot": our_slot,
            "cisi_slot": cisi_slot,
            "consistent": match,
        }
        if not match:
            slot_mismatches.append(rec["p_sign"])
    print(f"    Slot mismatches (potential errors): {len(slot_mismatches)} — {slot_mismatches}")

    # --- Category B: Unread crosswalk signs — rank by CISI frequency + Parpola reading ---
    print("\n  Category B: Unread crosswalk signs with CISI data:")
    cat_b_candidates = []
    for rec in sorted(cat_b, key=lambda r: -r["freq_cisi"])[:20]:
        par = rec["parpola_phoneme"]
        slot = rec["dominant_slot"]
        print(f"    {rec['p_sign']} ({rec['m_id']}): freq={rec['freq_cisi']:3d}"
              f" slot={slot:8s} parpola='{par}'")
        if rec["freq_cisi"] >= MIN_FREQ_NEW and par:
            cat_b_candidates.append({
                "p_sign": rec["p_sign"],
                "m_id": rec["m_id"],
                "proposed_reading": par,
                "basis": (
                    f"Parpola (1994 App. B): '{par}' [{rec['parpola_confidence']}]. "
                    f"CISI freq={rec['freq_cisi']}, slot={slot}."
                ),
                "confidence": "CANDIDATE",
                "freq_cisi": rec["freq_cisi"],
                "dominant_slot": slot,
            })

    # --- Category C: P-signs with NO M-number — truly new territory ---
    print(f"\n  Category C: P-signs outside M77 crosswalk (top 20 by freq):")
    cat_c_new = []
    for rec in sorted(cat_c, key=lambda r: -r["freq_cisi"])[:20]:
        par = rec["parpola_phoneme"]
        slot = rec["dominant_slot"]
        print(f"    {rec['p_sign']:8s}: freq={rec['freq_cisi']:3d}"
              f" slot={slot:8s} parpola='{par}'")
        if rec["freq_cisi"] >= MIN_FREQ_NEW:
            cat_c_new.append({
                "p_sign": rec["p_sign"],
                "m_id": None,
                "proposed_reading": par or f"[{rec['p_sign']} unread]",
                "basis": (
                    f"Phase-220: CISI-only sign, freq={rec['freq_cisi']}, "
                    f"slot={slot}. "
                    + (f"Parpola reading: '{par}' [{rec['parpola_confidence']}]."
                       if par else "No Parpola reading available.")
                ),
                "confidence": "CANDIDATE",
                "freq_cisi": rec["freq_cisi"],
                "dominant_slot": slot,
                "note": "Not in Holdat/M77 corpus — CISI exclusive sign",
            })

    print(f"\n  New CANDIDATE anchors from Cat-B: {len(cat_b_candidates)}")
    print(f"  New CANDIDATE anchors from Cat-C: {len(cat_c_new)}")
    total_new = len(cat_b_candidates) + len(cat_c_new)
    print(f"  Total new candidates proposed: {total_new}")

    # Summary statistics
    cisi_freqs = [profiles[s]["freq"] for s in all_cisi_signs]
    result = {
        "phase": 220,
        "description": "Parpola/CISI cross-reference — expansion beyond M77 sign set",
        "cisi_stats": {
            "n_inscriptions": len(seqs),
            "n_distinct_signs": len(all_cisi_signs),
            "total_tokens": sum(cisi_freqs),
        },
        "crosswalk_stats": {
            "n_crosswalk_entries": len(crosswalk),
            "n_cisi_signs_in_crosswalk": len(cat_a) + len(cat_b),
            "n_cisi_signs_outside_crosswalk": len(cat_c),
        },
        "category_a_confirmed": cat_a,
        "category_b_unread": cat_b,
        "category_c_new": cat_c,
        "slot_mismatches": slot_mismatches,
        "new_candidates": {
            "from_crosswalk_unread": cat_b_candidates,
            "from_cisi_exclusive": cat_c_new,
            "total": total_new,
        },
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n  Saved → {OUT}")
    return result


if __name__ == "__main__":
    main()
