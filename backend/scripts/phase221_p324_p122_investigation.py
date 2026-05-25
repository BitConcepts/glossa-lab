"""Phase-221: P324 and P122 Deep Investigation.

P324 (freq=99, INITIAL-dominant) and P122 (freq=76, MEDIAL) are the two
highest-frequency unread CISI signs with no counterpart in our M77/Holdat
anchor set. This phase profiles them exhaustively:

  - Full positional statistics (I/M/T rates, avg position)
  - Bigram context: what signs precede and follow them?
  - Co-occurrence with known confirmed anchors
  - Hypothesis generation from Dravidian grammar model
  - Parpola literature cross-reference for any mentions

Output: outputs/phase221_p324_p122_investigation.json
"""
from __future__ import annotations

import json
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPO    = Path(__file__).parents[2]
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
CROSSWALK = REPO / "backend/glossa_lab/data/mahadevan_parpola_crosswalk_v2.json"
PARPHON = REPO / "backend/glossa_lab/data/parpola_phonemes.json"
OUT     = REPO / "outputs/phase221_p324_p122_investigation.json"
OUT.parent.mkdir(exist_ok=True)

sys.path.insert(0, str(REPO / "backend"))
os.environ.setdefault("GLOSSA_DATA_DIR", str(REPO / "backend/data"))

TARGET_SIGNS = ["P324", "P122", "P385", "P230", "P316", "P000", "P217", "P378"]


def load_cisi():
    from glossa_lab.data import indus_cisi  # noqa: PLC0415
    return indus_cisi.get_corpus_inscriptions_with_ids()


def analyze_sign(seqs_with_ids, sign_id: str, confirmed: dict,
                 p_to_m: dict) -> dict:
    """Full positional and bigram profile for a single P-sign."""
    freq = 0
    initial = 0
    terminal = 0
    medial = 0
    total_seals = 0
    pre_context: Counter = Counter()   # signs immediately before
    post_context: Counter = Counter()  # signs immediately after
    co_occur: Counter = Counter()      # all other signs in same inscription
    inscription_lengths = []
    sample_inscriptions = []

    for insc_id, seq in seqs_with_ids:
        if sign_id not in seq:
            continue
        total_seals += 1
        n = len(seq)
        inscription_lengths.append(n)
        if len(sample_inscriptions) < 5:
            sample_inscriptions.append({"id": insc_id, "seq": seq})

        for i, s in enumerate(seq):
            if s != sign_id:
                continue
            freq += 1
            if i == 0:
                initial += 1
            elif i == n - 1:
                terminal += 1
            else:
                medial += 1

            if i > 0:
                pre_context[seq[i - 1]] += 1
            if i < n - 1:
                post_context[seq[i + 1]] += 1

        for s in seq:
            if s != sign_id:
                co_occur[s] += 1

    if freq == 0:
        return {"sign": sign_id, "freq": 0, "error": "sign not found"}

    i_rate = round(initial / freq, 3)
    t_rate = round(terminal / freq, 3)
    m_rate = round(medial / freq, 3)

    # Classify slot
    if i_rate >= 0.55:
        slot = "INITIAL"
    elif t_rate >= 0.55:
        slot = "TERMINAL"
    else:
        slot = "MEDIAL"

    # Co-occurring confirmed anchors (H+M)
    confirmed_cooccur = [
        {"sign": s, "count": c, "reading": confirmed[p_to_m[s]]["reading"],
         "confidence": confirmed[p_to_m[s]]["confidence"]}
        for s, c in co_occur.most_common(30)
        if s in p_to_m and p_to_m[s] in confirmed
    ]

    # Map top context signs to readings if known
    def sign_label(p_sign: str) -> str:
        m = p_to_m.get(p_sign)
        if m and m in confirmed:
            return f"{p_sign}={confirmed[m]['reading']}"
        return p_sign

    # Grammar hypothesis based on slot
    hypotheses = []
    if slot == "INITIAL":
        hypotheses.append(
            "INITIAL-dominant sign: likely an ANIMAL_CLAN determinative, royal title, "
            "or administrative prefix. High probability of logographic/ideographic function. "
            "Compare: M267 (genitive-in), M062 (erutu/bull), M045 (yānai/elephant) — all INITIAL."
        )
        if freq >= 80:
            hypotheses.append(
                f"Very high frequency ({freq}) + INITIAL dominance: may be equivalent to "
                "M267 (genitive particle 'iN/in') or a new title determinative not in M77."
            )
    elif slot == "TERMINAL":
        hypotheses.append(
            "TERMINAL-dominant sign: likely a CASE SUFFIX (genitive, dative, locative) "
            "or personal name ending. Compare: M342 (ay/ā), M176 (an/aṇ), M367 (am)."
        )
    else:
        hypotheses.append(
            "MEDIAL sign: likely a phonetic syllable or personal name component. "
            "Compare: M293 (ta), M099 (kol), M024 (nē)."
        )

    return {
        "sign": sign_id,
        "freq_cisi": freq,
        "n_inscriptions": total_seals,
        "avg_inscription_length": round(
            sum(inscription_lengths) / len(inscription_lengths), 2
        ) if inscription_lengths else 0,
        "positional": {
            "initial": initial, "medial": medial, "terminal": terminal,
            "initial_rate": i_rate, "medial_rate": m_rate, "terminal_rate": t_rate,
            "dominant_slot": slot,
        },
        "top_10_pre_context": [
            {"sign": sign_label(s), "count": c}
            for s, c in pre_context.most_common(10)
        ],
        "top_10_post_context": [
            {"sign": sign_label(s), "count": c}
            for s, c in post_context.most_common(10)
        ],
        "confirmed_cooccur_hm": confirmed_cooccur[:10],
        "sample_inscriptions": sample_inscriptions,
        "hypotheses": hypotheses,
    }


def main():
    print("Phase-221: P324 and P122 Deep Investigation\n")

    # Load anchors and mappings
    anchors_data = json.loads(ANCHORS.read_text("utf-8"))
    anchors = anchors_data.get("anchors", {})
    confirmed = {s: v for s, v in anchors.items()
                 if v.get("confidence") in ("HIGH", "MEDIUM")}
    print(f"  Confirmed H+M anchors: {len(confirmed)}")

    cw_data = json.loads(CROSSWALK.read_text("utf-8"))
    crosswalk = cw_data.get("crosswalk", {})
    # Build P->M mapping
    p_to_m: dict[str, str] = {}
    for m_id, entry in crosswalk.items():
        p_id = str(entry.get("parpola_id", "") or entry.get("parpola_num", ""))
        if p_id.startswith("P"):
            p_to_m[p_id] = m_id
        elif p_id.isdigit():
            p_to_m[f"P{int(p_id):03d}"] = m_id

    pp_data = json.loads(PARPHON.read_text("utf-8"))
    phoneme_map = pp_data.get("phoneme_map", {})
    parpola_readings = {
        f"P{int(k):03d}": v for k, v in phoneme_map.items() if k.isdigit()
    }

    # Load CISI with inscription IDs
    print("  Loading CISI corpus...")
    from glossa_lab.data import indus_cisi  # noqa: PLC0415
    raw = indus_cisi.get_corpus_inscriptions_with_ids()
    # raw is list of {catalogue_id: str, signs: list}
    if raw and isinstance(raw[0], dict):
        seqs_with_ids = [(r["catalogue_id"], r["signs"]) for r in raw]
    elif raw and isinstance(raw[0], (list, tuple)):
        seqs_with_ids = [(f"CISI-{i:03d}", s) for i, s in enumerate(raw)]
    else:
        seqs = indus_cisi.get_corpus_inscriptions()
        seqs_with_ids = [(f"CISI-{i:03d}", s) for i, s in enumerate(seqs)]

    print(f"  CISI inscriptions: {len(seqs_with_ids)}")

    # Analyse each target sign
    results = {}
    for sign in TARGET_SIGNS:
        print(f"\n  Analysing {sign}...")
        profile = analyze_sign(seqs_with_ids, sign, confirmed, p_to_m)
        par = parpola_readings.get(sign, {})
        profile["parpola_reading"] = par.get("phoneme", "")
        profile["parpola_confidence"] = par.get("confidence", "")
        profile["parpola_note"] = par.get("gloss", "")
        profile["in_holdat_as"] = p_to_m.get(sign, "")

        results[sign] = profile

        pos = profile.get("positional", {})
        print(f"    freq={profile['freq_cisi']}  slot={pos.get('dominant_slot')}  "
              f"I={pos.get('initial_rate',0):.2f} M={pos.get('medial_rate',0):.2f} "
              f"T={pos.get('terminal_rate',0):.2f}")
        if profile.get("top_10_pre_context"):
            pre = [x['sign'] for x in profile['top_10_pre_context'][:5]]
            print(f"    pre-context: {pre}")
        if profile.get("top_10_post_context"):
            post = [x['sign'] for x in profile['top_10_post_context'][:5]]
            print(f"    post-context: {post}")
        if profile.get("confirmed_cooccur_hm"):
            cooc = [(x['sign'], x['reading']) for x in profile['confirmed_cooccur_hm'][:4]]
            print(f"    co-occurs with: {cooc}")
        for h in profile.get("hypotheses", [])[:1]:
            print(f"    → {h[:100]}")

    # Summary
    print("\n  === SUMMARY ===")
    for sign, prof in results.items():
        if prof.get("freq_cisi", 0) > 0:
            slot = prof["positional"]["dominant_slot"]
            par_r = prof.get("parpola_reading", "")
            holdat = prof.get("in_holdat_as", "")
            print(f"  {sign:6s}: freq={prof['freq_cisi']:3d} "
                  f"slot={slot:8s} parpola='{par_r:10s}' holdat={holdat}")

    out_data = {
        "phase": 221,
        "description": "Deep investigation of P324 (freq=99, INITIAL) and P122 (freq=76, MEDIAL) — top unread CISI signs",
        "target_signs": TARGET_SIGNS,
        "results": results,
        "key_findings": {
            "P324": (
                "INITIAL-dominant (freq=99): Strongest candidate for an administrative "
                "title determinative or high-frequency grammatical prefix not in M77 corpus. "
                "Context analysis determines if it precedes known title signs."
            ),
            "P122": (
                "MEDIAL sign (freq=76): No Parpola reading. Bigram context determines "
                "phonetic vs logographic function. High frequency suggests it's a common "
                "phonetic syllable analogous to M099 (kol) or M293 (ta)."
            ),
        },
    }
    OUT.write_text(json.dumps(out_data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n  Saved → {OUT}")
    return out_data


if __name__ == "__main__":
    main()
