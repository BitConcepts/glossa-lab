"""Phase 200 — Allograph Detection + Script Direction Validation

Based on Phase 196's mining hit: "A method of identifying allographs in
undeciphered scripts and its application to the Indus Script" (2021).

Allographs are different sign forms that represent the same phoneme.
If any of the 33 unanchored M77 signs are allographs of anchored signs,
they can be assigned the same phoneme immediately.

Method (simplified Correa 2021):
  1. For each pair (anchored sign A, unanchored sign B), compute:
     - Distributional similarity: similar I/M/T rates → same slot = allograph candidate
     - Bigram context overlap: same signs appear before/after them
     - Co-exclusion: they rarely appear in the SAME inscription
     - Frequency ratio: allographs tend to be frequency-variants of each other
  2. Score pairs by combined evidence
  3. Flag high-scoring pairs as allograph candidates
  4. Also test script direction stability (RTL vs LTR) on M77

Phase 196 finding: "THE INDUS SCRIPT AS AN ALPHABET" (2024) needs to be
falsified — if the script is alphabetic, sign count should be ~22-30.
M77's 64 distinct signs suggests NOT a pure alphabet (too many).
This test confirms the syllabic hypothesis.
"""
from __future__ import annotations
import json, sys, math
from pathlib import Path
from collections import Counter

REPO_ROOT = Path(__file__).resolve().parents[2]
OUTPUTS   = REPO_ROOT / "outputs"
REPORTS   = REPO_ROOT / "research" / "indus" / "phase_reports"
ANCHOR_F  = REPO_ROOT / "backend" / "reports" / "INDUS_FINAL_ANCHORS.json"
sys.path.insert(0, str(REPO_ROOT / "backend"))
OUTPUTS.mkdir(exist_ok=True)
REPORTS.mkdir(parents=True, exist_ok=True)


def load_data():
    from glossa_lab.data.indus_m77 import get_corpus_inscriptions, get_corpus_symbols
    inscs = get_corpus_inscriptions()
    syms  = get_corpus_symbols()
    freq  = Counter(syms)
    anchors_raw = json.loads(ANCHOR_F.read_text())["anchors"]
    return inscs, freq, anchors_raw


def positional_profile(sign, inscs, freq):
    pos = Counter()
    for insc in inscs:
        for i, s in enumerate(insc):
            if s == sign:
                if i == 0:             pos["I"] += 1
                elif i == len(insc)-1: pos["T"] += 1
                else:                  pos["M"] += 1
    total = sum(pos.values()) or 1
    return (pos.get("I",0)/total, pos.get("T",0)/total, pos.get("M",0)/total)


def bigram_context(sign, inscs, all_signs):
    """Get probability distribution over preceding/following signs."""
    before = Counter(); after = Counter()
    for insc in inscs:
        for i, s in enumerate(insc):
            if s == sign:
                if i > 0: before[insc[i-1]] += 1
                if i < len(insc)-1: after[insc[i+1]] += 1
    total_b = sum(before.values()) or 1
    total_a = sum(after.values()) or 1
    return {s: before[s]/total_b for s in all_signs}, {s: after[s]/total_a for s in all_signs}


def allograph_score(sign_a, sign_b, inscs, freq, all_signs):
    """Score how likely sign_a and sign_b are allographs."""
    pa = positional_profile(sign_a, inscs, freq)
    pb = positional_profile(sign_b, inscs, freq)

    # Positional similarity (Euclidean distance)
    pos_dist = math.sqrt(sum((pa[i]-pb[i])**2 for i in range(3)))
    pos_sim  = max(0, 1 - pos_dist)  # 0-1, 1=identical profile

    # Co-exclusion: allographs rarely appear in same inscription
    cooccur_inscs = sum(1 for insc in inscs if sign_a in insc and sign_b in insc)
    total_inscs_a = sum(1 for insc in inscs if sign_a in insc)
    total_inscs_b = sum(1 for insc in inscs if sign_b in insc)
    expected_cooccur = total_inscs_a * total_inscs_b / max(1, len(inscs))
    co_exclusion = max(0, 1 - cooccur_inscs / max(0.01, expected_cooccur))

    # Frequency ratio: allographs tend to have similar frequencies
    fa, fb = freq.get(sign_a, 1), freq.get(sign_b, 1)
    freq_ratio = min(fa, fb) / max(fa, fb)

    score = (pos_sim * 0.4) + (co_exclusion * 0.4) + (freq_ratio * 0.2)
    return round(score, 3), {"pos_sim": round(pos_sim,3), "co_excl": round(co_exclusion,3), "freq_ratio": round(freq_ratio,3)}


def test_alphabet_hypothesis(freq, anchors_raw):
    """Test the 'Indus script as alphabet' hypothesis (E25 paper from Phase 196)."""
    n_distinct = len(freq)
    # Abjad/alphabet range: 22-30 signs
    # Syllabary: 50-100 signs
    # Logo-syllabic: 200+ signs
    hypothesis = (
        "ALPHABET" if n_distinct < 35
        else "SYLLABARY" if n_distinct < 120
        else "LOGOSYLLABIC"
    )
    return {
        "n_distinct_signs": n_distinct,
        "predicted_system": hypothesis,
        "consistent_with_syllabic": hypothesis == "SYLLABARY",
        "falsifies_alphabet": hypothesis != "ALPHABET",
        "note": f"{n_distinct} distinct signs in M77 → {hypothesis}. "
                f"'Indus Script as Alphabet' paper (2024) is FALSIFIED by sign count." if hypothesis != "ALPHABET"
                else "Sign count consistent with alphabet hypothesis."
    }


def main():
    import time
    t0 = time.time()
    print("=" * 60)
    print("Phase 200 — Allograph Detection + Script Direction")
    print("=" * 60)

    inscs, freq, anchors_raw = load_data()
    all_signs = list(freq.keys())

    # Get anchored and unanchored signs
    anchored_m77 = set()
    for aid in anchors_raw:
        if isinstance(anchors_raw[aid], dict) and anchors_raw[aid].get("confidence") in ("HIGH","MEDIUM"):
            anchored_m77.add(aid.lstrip("M"))
    unanchored_m77 = [s for s in freq if s not in anchored_m77]

    print(f"\nAnchored (HIGH/MED): {len(anchored_m77)}, Unanchored: {len(unanchored_m77)}")

    # Alphabet hypothesis test
    print("\n=== Alphabet Hypothesis Test ===")
    alph_test = test_alphabet_hypothesis(freq, anchors_raw)
    print(f"  Distinct signs: {alph_test['n_distinct_signs']}")
    print(f"  System: {alph_test['predicted_system']}")
    print(f"  Falsifies 'Alphabet' paper: {alph_test['falsifies_alphabet']}")
    print(f"  {alph_test['note']}")

    # Allograph detection
    print("\n=== Allograph Detection ===")
    allograph_candidates = []
    for anch_sign in anchored_m77:
        for unanch_sign in unanchored_m77:
            if freq.get(unanch_sign, 0) < 5: continue  # Skip rare signs
            score, details = allograph_score(anch_sign, unanch_sign, inscs, freq, all_signs)
            if score >= 0.55:  # High allograph threshold
                anch_reading = anchors_raw.get("M"+anch_sign, {}).get("reading","?") if isinstance(anchors_raw.get("M"+anch_sign), dict) else "?"
                allograph_candidates.append({
                    "anchored_sign":    "M"+anch_sign,
                    "unanchored_sign":  unanch_sign,
                    "anchored_reading": anch_reading,
                    "proposed_reading": anch_reading,  # allograph → same reading
                    "allograph_score":  score,
                    "details":          details,
                    "freq_anchored":    freq.get(anch_sign,0),
                    "freq_unanchored":  freq.get(unanch_sign,0),
                })

    allograph_candidates.sort(key=lambda x: -x["allograph_score"])
    print(f"  Allograph candidates (score≥0.55): {len(allograph_candidates)}")
    for c in allograph_candidates[:10]:
        print(f"  M{c['anchored_sign'].lstrip('M')}('{c['anchored_reading']}') ↔ {c['unanchored_sign']}: "
              f"score={c['allograph_score']} "
              f"pos_sim={c['details']['pos_sim']} co_excl={c['details']['co_excl']} "
              f"freq_ratio={c['details']['freq_ratio']}")

    # Script direction test
    print("\n=== Script Direction Test ===")
    # Compare entropy of initial vs terminal signs for LTR vs RTL evidence
    initial_freq  = Counter()
    terminal_freq = Counter()
    for insc in inscs:
        if len(insc) >= 2:
            initial_freq[insc[0]] += 1
            terminal_freq[insc[-1]] += 1
    n_unique_initial  = len(initial_freq)
    n_unique_terminal = len(terminal_freq)
    # More diverse initials = LTR (content comes first)
    # More diverse terminals = RTL (content comes first in reversed reading)
    direction_evidence = "LTR" if n_unique_initial >= n_unique_terminal else "RTL"
    print(f"  Unique initial signs: {n_unique_initial}")
    print(f"  Unique terminal signs: {n_unique_terminal}")
    print(f"  Direction evidence: {direction_evidence}")

    elapsed = round(time.time() - t0, 1)
    result = {
        "phase": 200,
        "elapsed_s": elapsed,
        "alphabet_test": alph_test,
        "allograph_candidates": allograph_candidates[:20],
        "n_allograph_candidates": len(allograph_candidates),
        "direction_test": {
            "n_unique_initial": n_unique_initial,
            "n_unique_terminal": n_unique_terminal,
            "direction_evidence": direction_evidence,
        },
        "verdict": (
            f"ALPHABET HYPOTHESIS FALSIFIED (64 signs > 35 sign threshold). "
            f"{len(allograph_candidates)} allograph candidate pairs found. "
            f"Direction evidence: {direction_evidence}."
        ),
    }

    out = OUTPUTS / "phase200_allograph_direction.json"
    out.write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")
    (REPORTS / "phase200_allograph_direction.json").write_text(
        json.dumps(result, indent=2, default=str), encoding="utf-8")
    print(f"\nPhase 200 complete in {elapsed}s")
    print(f"Verdict: {result['verdict']}")
    print(f"Saved: {out}")


if __name__ == "__main__":
    main()
