"""Phase-222: CISI Candidate Anchor Injection.

Uses Phase-221 analysis + Phase-220 Phase-221 data to inject the highest-quality
CISI-derived candidates into INDUS_FINAL_ANCHORS.json as CANDIDATE or LOW entries.

Injection criteria:
  - CISI frequency >= 10
  - Clear dominant slot (I >= 0.65 or T >= 0.65 or M >= 0.80)
  - Either a Parpola reading exists OR positional slot is unambiguous enough
    to propose a Dravidian reading from grammar model
  - Not already in anchor set

Key injections from Phase-221:
  P324 (INITIAL 0.78, freq=99): Title/administrative determinative
  P122 -> M122 (MEDIAL 1.00, freq=76): Pure phonetic syllable
  P385 (TERMINAL 0.83, freq=35): Case suffix marker
  P332 (MEDIAL, from prior analysis): Known "o" candidate

Output: outputs/phase222_cisi_anchor_injection.json
Also updates backend/reports/INDUS_FINAL_ANCHORS.json
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

REPO    = Path(__file__).parents[2]
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
P221    = REPO / "outputs/phase221_p324_p122_investigation.json"
P220    = REPO / "outputs/phase220_parpola_cisi_crossref.json"
CROSSWALK = REPO / "backend/glossa_lab/data/mahadevan_parpola_crosswalk_v2.json"
OUT     = REPO / "outputs/phase222_cisi_anchor_injection.json"
OUT.parent.mkdir(exist_ok=True)

sys.path.insert(0, str(REPO / "backend"))
os.environ.setdefault("GLOSSA_DATA_DIR", str(REPO / "backend/data"))

# Manually curated candidates from Phase-221 analysis + grammar model
# These are the best hypotheses based on positional profiling
CANDIDATES = [
    {
        "p_sign": "P324",
        "m_id": None,  # Not in M77/Holdat
        "reading": "[TITLE_PREFIX]",
        "confidence": "CANDIDATE",
        "basis": (
            "Phase-221: INITIAL-dominant (I=0.78, freq=99 in CISI). "
            "Pre-context: nakaram (place), kāṇṭāmirukam (rhinoceros), kaḷiṟu (elephant). "
            "Post-context: P332 (ko-vowel candidate), P086=oru. "
            "Hypothesis: administrative title prefix or high-status determinative. "
            "Function parallel to M267 (genitive prefix) but appears at inscription start. "
            "CISI-exclusive sign — not in Holdat M77 corpus. "
            "Epistemic status: CANDIDATE (slot clear; phonetic value uncertain)."
        ),
        "source": "Phase-222 CISI injection",
        "cisi_freq": 99,
        "slot": "INITIAL",
    },
    {
        "p_sign": "P385",
        "m_id": None,  # Not in Holdat
        "reading": "[TERMINAL_SUFFIX]",
        "confidence": "CANDIDATE",
        "basis": (
            "Phase-221: TERMINAL-dominant (T=0.83, freq=35 in CISI). "
            "Pre-context: P122 (medial syllable), P324 (initial prefix). "
            "Post-context: P073=kōṉ (king), P147. "
            "Hypothesis: case suffix or personal name terminal marker. "
            "Pattern [P122][P385][kōṉ] consistent with [name_syllable][suffix][title]. "
            "CISI-exclusive sign. Epistemic status: CANDIDATE (slot very clear)."
        ),
        "source": "Phase-222 CISI injection",
        "cisi_freq": 35,
        "slot": "TERMINAL",
    },
    {
        "p_sign": "P122",
        "m_id": "M122",  # In crosswalk as M122 but UNREAD
        "reading": "[MEDIAL_SYLLABLE_UNREAD]",
        "confidence": "CANDIDATE",
        "basis": (
            "Phase-221: MEDIAL 100% (M=1.00, I=0.00, T=0.00, freq=76 in CISI). "
            "Pure phonetic syllable — never initial, never terminal. "
            "Pre-context: P364 (or?), P145=miṭ. Post-context: P385 (terminal suffix). "
            "Pattern [P122][P385] = phonetic syllable + case marker (35+ occurrences). "
            "In Holdat crosswalk as M122 but no reading assigned. "
            "Phonetic value TBD: candidates from DEDR include 'pa', 'cē', 'kā'. "
            "Epistemic status: CANDIDATE (medial slot certain; reading unknown)."
        ),
        "source": "Phase-222 CISI injection",
        "cisi_freq": 76,
        "slot": "MEDIAL",
    },
    {
        "p_sign": "P332",
        "m_id": None,
        "reading": "o/ko",
        "confidence": "CANDIDATE",
        "basis": (
            "Phase-221/old analysis: Post-context of P324 (INITIAL). "
            "Pattern [P324][P332] = [title_prefix][ko?] consistent with old Phase-22 "
            "hypothesis P332='o' (ko syllable vowel). CISI freq=11 (Phase-220). "
            "Also appeared in CISI SA experiments as anchor P332='o'. "
            "Epistemic status: CANDIDATE (reading from prior CISI SA experiments)."
        ),
        "source": "Phase-222 CISI injection",
        "cisi_freq": 11,
        "slot": "MEDIAL",
    },
]


def main():
    print("Phase-222: CISI Candidate Anchor Injection\n")

    anchors_data = json.loads(ANCHORS.read_text("utf-8"))
    anchors = anchors_data.get("anchors", {})
    existing_signs = set(anchors.keys())

    # Load Phase-220 Cat-C new candidates for additional injections
    p220_candidates = []
    if P220.exists():
        p220 = json.loads(P220.read_text("utf-8"))
        cat_b = p220.get("new_candidates", {}).get("from_crosswalk_unread", [])
        cat_c = p220.get("new_candidates", {}).get("from_cisi_exclusive", [])
        # Filter to freq>=10 and has a Parpola reading or is a Category-B with M-ID
        for c in cat_b + cat_c:
            if c.get("freq_cisi", 0) >= 10 and c.get("proposed_reading", "").strip():
                p220_candidates.append(c)
        print(f"  Phase-220 candidates with freq>=10 and reading: {len(p220_candidates)}")

    added = []
    skipped_existing = []
    skipped_no_mid = []

    # Inject manually curated candidates
    for cand in CANDIDATES:
        p_sign = cand["p_sign"]
        m_id = cand.get("m_id") or f"P{p_sign[1:]}"  # Use P-sign as key if no M-ID

        # Use P-sign as the key in anchors (for CISI-only signs without M equivalent)
        anchor_key = m_id if m_id and not m_id.startswith("P") else p_sign

        if anchor_key in existing_signs:
            existing_conf = anchors[anchor_key].get("confidence", "")
            if existing_conf in ("HIGH", "MEDIUM", "LOW"):
                skipped_existing.append(f"{anchor_key} (existing {existing_conf})")
                continue
            # Upgrade from UNREAD or CANDIDATE
            print(f"  Upgrading {anchor_key}: UNREAD → {cand['confidence']}")
        else:
            print(f"  Injecting {anchor_key} ({p_sign}): {cand['confidence']} '{cand['reading']}'")

        anchors[anchor_key] = {
            "reading": cand["reading"],
            "confidence": cand["confidence"],
            "basis": cand["basis"],
            "source": cand["source"],
            "p_sign": p_sign,
            "cisi_freq": cand["cisi_freq"],
            "dominant_slot": cand["slot"],
        }
        added.append(anchor_key)

    # Also inject from Phase-220 Cat-B (crosswalk unread signs with Parpola reading)
    p220_injected = []
    for c in p220_candidates:
        m_id = c.get("m_id") or c.get("p_sign", "")
        if not m_id:
            continue
        if m_id in existing_signs:
            existing_conf = anchors.get(m_id, {}).get("confidence", "")
            if existing_conf in ("HIGH", "MEDIUM", "LOW"):
                continue  # Already have a real reading
        proposed = c.get("proposed_reading", "")
        if not proposed or proposed.startswith("["):
            continue  # Skip non-meaningful readings
        anchors[m_id] = {
            "reading": proposed,
            "confidence": "CANDIDATE",
            "basis": c.get("basis", f"Phase-222 CISI injection from Phase-220"),
            "source": "Phase-222 CISI P220",
            "p_sign": c.get("p_sign", ""),
            "cisi_freq": c.get("freq_cisi", 0),
            "dominant_slot": c.get("dominant_slot", ""),
        }
        p220_injected.append(m_id)
        print(f"  Injecting {m_id}: CANDIDATE '{proposed}' (CISI freq={c.get('freq_cisi',0)})")

    # Save
    anchors_data["anchors"] = anchors
    anchors_data["total"] = len(anchors)
    conf_count = {}
    for v in anchors.values():
        c = v.get("confidence", "?")
        conf_count[c] = conf_count.get(c, 0) + 1
    anchors_data["by_confidence"] = conf_count
    ANCHORS.write_text(json.dumps(anchors_data, indent=2, ensure_ascii=False), encoding="utf-8")

    total_added = len(added) + len(p220_injected)
    print(f"\n  Injected (manual): {len(added)}")
    print(f"  Injected (P220):   {len(p220_injected)}")
    print(f"  Total new:         {total_added}")
    print(f"  Skipped (existing): {skipped_existing}")
    print(f"  New total anchors: {len(anchors)}")

    result = {
        "phase": 222,
        "injected_manual": added,
        "injected_p220": p220_injected,
        "total_injected": total_added,
        "skipped_existing": skipped_existing,
        "new_total_anchors": len(anchors),
        "by_confidence": conf_count,
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n  Saved → {OUT}")
    return result


if __name__ == "__main__":
    main()
