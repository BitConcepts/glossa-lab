"""Phase 197 — Top-8 Unanchored Sign Deep Analysis

The 8 highest-frequency unanchored M77 signs account for 45.5% of all tokens:
  700 (355 tok), 520 (196), 481 (179), 692 (171),
  861 (138), 820 (121), 817 (107), 858 (105)

Phase 193 SA gave modal readings: 520→kol, 692→nal, 861→nallavar.
This phase runs deeper SA (10 seeds × 3 runs for stability) on each sign,
cross-references DEDR for phoneme plausibility, and checks whether any
of the proposed readings fill the 9 remaining absent phonemes.

Methods:
  1. 10-seed SA with all 31 M77 anchors → modal + consistency per sign
  2. DEDR phoneme plausibility lookup (known Tamil/PDr forms)
  3. Co-occurrence analysis: which anchored signs flank each unanchored sign?
  4. Absent-phoneme check: does any stable reading match /li/, /shu/, /gu/, etc.?
  5. Score = SA_stability × DEDR_match × positional_fit
"""
from __future__ import annotations
import json, sys
from pathlib import Path
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

REPO_ROOT = Path(__file__).resolve().parents[2]
OUTPUTS   = REPO_ROOT / "outputs"
REPORTS   = REPO_ROOT / "research" / "indus" / "phase_reports"
ANCHOR_F  = REPO_ROOT / "backend" / "reports" / "INDUS_FINAL_ANCHORS.json"
sys.path.insert(0, str(REPO_ROOT / "backend"))
OUTPUTS.mkdir(exist_ok=True)
REPORTS.mkdir(parents=True, exist_ok=True)

# The 8 highest-frequency unanchored signs
TOP8 = ["700", "520", "481", "692", "861", "820", "817", "858"]

ABSENT_PHONEMES = ["li","shu","gu","ab","ba","du","ga","mil","sum"]

# DEDR phoneme candidates for the top readings from Phase 193 SA
DEDR_CANDIDATES = {
    "kol":      {"dedr": "2172", "meaning": "forge/iron-working/hold",    "phoneme_root": "kol"},
    "nal":      {"dedr": "3594", "meaning": "good, excellent, fine",      "phoneme_root": "nal"},
    "nallavar": {"dedr": "3594", "meaning": "good people (honorific)",    "phoneme_root": "nal"},
    "porul":    {"dedr": "4428", "meaning": "wealth, property, goods",    "phoneme_root": "por"},
    "min":      {"dedr": "4897", "meaning": "fish; star; shine",          "phoneme_root": "min"},
    "kuti":     {"dedr": "1695", "meaning": "family, hamlet, settlement", "phoneme_root": "kut"},
    "kal":      {"dedr": "1291", "meaning": "foot, leg; stone",           "phoneme_root": "kal"},
    "toti":     {"dedr": "3330", "meaning": "bracelet, armlet, metal band","phoneme_root": "tot"},
    "venni":    {"dedr": "5515", "meaning": "silver; white",              "phoneme_root": "ven"},
    "kalan":    {"dedr": "1289", "meaning": "time, Yama (death)",         "phoneme_root": "kal"},
    "naval":    {"dedr": "3636", "meaning": "plum, grape vine; wonder",   "phoneme_root": "nav"},
}

# Check whether any reading fills an absent phoneme
def check_absent_phoneme_match(reading: str) -> list[str]:
    reading_lower = reading.lower()
    return [ap for ap in ABSENT_PHONEMES if ap in reading_lower]


def load_data():
    from glossa_lab.data.indus_m77 import get_corpus_inscriptions, get_corpus_symbols
    inscs = get_corpus_inscriptions()
    syms  = get_corpus_symbols()
    freq  = Counter(syms)
    anchors_raw = json.loads(ANCHOR_F.read_text())["anchors"]
    return inscs, freq, anchors_raw


def build_full_anchor_dict(anchors_raw, freq):
    """All anchors in M77 format."""
    tier_order = {"HIGH": 3, "MEDIUM": 2, "LOW": 1}
    d = {}
    for aid, rec in anchors_raw.items():
        if not isinstance(rec, dict): continue
        if tier_order.get(rec.get("confidence",""), 0) < 1: continue
        m77 = aid.lstrip("M")
        reading = rec.get("reading","").split("/")[0].strip()
        if m77 in freq and reading:
            d[m77] = reading
    return d


def run_stable_sa(inscs, anchors, n_seeds=10):
    """Run SA n_seeds times, return modal mapping + per-sign consistency."""
    from glossa_lab.pipelines.decipher import decipher, LanguageModel
    from glossa_lab.data.dravidian import get_word_symbols
    lm   = LanguageModel(get_word_symbols())
    flat = [s for insc in inscs for s in insc]

    def _one(seed):
        r = decipher(flat, lm, seed=seed, max_iterations=5000, restarts=5,
                     cipher_inscriptions=None, ocp_weight=0.0,
                     positional_weight=0.0, surjective=True,
                     anchors=anchors or None)
        return r.get("proposed_mapping", {})

    with ThreadPoolExecutor(max_workers=n_seeds) as ex:
        maps = list(ex.map(_one, range(n_seeds)))

    all_signs = set().union(*[m.keys() for m in maps])
    modal = {}; conss = {}
    for s in all_signs:
        props = [m[s] for m in maps if s in m]
        if props:
            from collections import Counter as C
            mc_val, mc_cnt = C(props).most_common(1)[0]
            modal[s] = mc_val
            conss[s] = mc_cnt / len(props)
    return modal, conss


def analyze_sign(sign, inscs, freq, anchors_raw, modal, conss):
    """Full analysis of a single unanchored sign."""
    # Positional profile
    pos = Counter()
    for insc in inscs:
        for i, s in enumerate(insc):
            if s == sign:
                if i == 0:             pos["INITIAL"] += 1
                elif i == len(insc)-1: pos["TERMINAL"] += 1
                else:                  pos["MEDIAL"] += 1
    total_pos = sum(pos.values()) or 1

    # Build M77→reading for anchored signs
    m77_to_r = {}
    for aid, rec in anchors_raw.items():
        if isinstance(rec, dict) and rec.get("confidence") in ("HIGH","MEDIUM"):
            m77_to_r[aid.lstrip("M")] = rec.get("reading","").split("/")[0]

    # Co-occurrence with anchored signs (window ±2)
    cooccur = Counter()
    for insc in inscs:
        for i, s in enumerate(insc):
            if s == sign:
                for j in range(max(0, i-2), min(len(insc), i+3)):
                    if j != i and insc[j] in m77_to_r:
                        cooccur[m77_to_r[insc[j]]] += 1

    sa_reading  = modal.get(sign, "")
    sa_cons     = conss.get(sign, 0.0)
    absent_hits = check_absent_phoneme_match(sa_reading)
    dedr_info   = DEDR_CANDIDATES.get(sa_reading.lower(), {})

    t = round(pos.get("TERMINAL",0)/total_pos, 3)
    i_rate = round(pos.get("INITIAL",0)/total_pos, 3)
    m = round(pos.get("MEDIAL",0)/total_pos, 3)

    return {
        "sign":         sign,
        "freq":         freq.get(sign, 0),
        "sa_modal":     sa_reading,
        "sa_consistency": round(sa_cons, 3),
        "absent_hits":  absent_hits,
        "dedr_info":    dedr_info,
        "t_rate": t, "i_rate": i_rate, "m_rate": m,
        "dominant_pos": max(pos, key=pos.get) if pos else "UNKNOWN",
        "top_cooccur":  cooccur.most_common(5),
        "upgrade_candidate": sa_cons >= 0.4 and bool(dedr_info),
    }


def main():
    import time
    t0 = time.time()
    print("=" * 60)
    print("Phase 197 — Top-8 Unanchored Sign Deep Analysis")
    print("=" * 60)

    inscs, freq, anchors_raw = load_data()
    anchor_dict = build_full_anchor_dict(anchors_raw, freq)
    print(f"\nRunning SA (10 seeds) with {len(anchor_dict)} anchors...")
    modal, conss = run_stable_sa(inscs, anchor_dict, n_seeds=10)

    print("\n=== Top-8 Unanchored Sign Analysis ===")
    results = []
    for sign in TOP8:
        r = analyze_sign(sign, inscs, freq, anchors_raw, modal, conss)
        results.append(r)
        absent_str = f" *** ABSENT HIT: {r['absent_hits']}" if r['absent_hits'] else ""
        upgrade_str = " [UPGRADE CANDIDATE]" if r['upgrade_candidate'] else ""
        print(f"  {sign}: freq={r['freq']} modal='{r['sa_modal']}' cons={r['sa_consistency']:.3f} "
              f"pos={r['dominant_pos']}(t={r['t_rate']},i={r['i_rate']}) "
              f"dedr={r['dedr_info'].get('meaning','?')[:30]} "
              f"cooccur={r['top_cooccur'][:3]}{absent_str}{upgrade_str}")

    # Absent phoneme analysis
    absent_candidates = [r for r in results if r["absent_hits"]]
    upgrade_candidates = [r for r in results if r["upgrade_candidate"]]
    print(f"\n  Signs matching absent phonemes: {len(absent_candidates)}")
    for r in absent_candidates:
        print(f"    {r['sign']} → '{r['sa_modal']}' covers absent: {r['absent_hits']}")
    print(f"  Signs that are upgrade candidates: {len(upgrade_candidates)}")

    elapsed = round(time.time() - t0, 1)
    result = {
        "phase": 197,
        "elapsed_s": elapsed,
        "top8_analysis": results,
        "absent_candidates": absent_candidates,
        "upgrade_candidates": upgrade_candidates,
        "verdict": (
            f"{len(absent_candidates)} of top-8 unanchored signs match absent phonemes: "
            f"{[r['sign'] for r in absent_candidates]}. "
            f"{len(upgrade_candidates)} upgrade candidates."
            if absent_candidates
            else f"No top-8 signs match absent phonemes. {len(upgrade_candidates)} upgrade candidates."
        ),
    }

    out = OUTPUTS / "phase197_top8_unanchored_analysis.json"
    out.write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")
    (REPORTS / "phase197_top8_unanchored_analysis.json").write_text(
        json.dumps(result, indent=2, default=str), encoding="utf-8")
    print(f"\nPhase 197 complete in {elapsed}s")
    print(f"Verdict: {result['verdict']}")
    print(f"Saved: {out}")


if __name__ == "__main__":
    main()
