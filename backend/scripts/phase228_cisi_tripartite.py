"""Phase-228: CISI Tripartite Grammar Test.

Phase-115 ran the tripartite (I→M→T) grammar test on the Holdat corpus
and got 35.5% of 3+ sign inscriptions following the I→M→T formula
(59× lift over null baseline of 0.6%).

This phase runs the SAME test on the 178 CISI inscriptions.
If CISI also shows a significant tripartite rate, this is INDEPENDENT
cross-corpus validation of the Dravidian suffix grammar model.

The tripartite test uses positional profiles from CISI:
  - INITIAL signs (I ≥ 0.55): P324, P000, P217, P301
  - TERMINAL signs (T ≥ 0.55): P385, P378, P256, P095
  - MEDIAL (everything else): P122, P230, P316, etc.

Output: outputs/phase228_cisi_tripartite.json
"""
from __future__ import annotations

import json
import os
import random
import sys
from collections import Counter
from pathlib import Path

REPO    = Path(__file__).parents[2]
P220    = REPO / "outputs/phase220_parpola_cisi_crossref.json"
OUT     = REPO / "outputs/phase228_cisi_tripartite.json"
OUT.parent.mkdir(exist_ok=True)

sys.path.insert(0, str(REPO / "backend"))
os.environ.setdefault("GLOSSA_DATA_DIR", str(REPO / "backend/data"))

# Positional thresholds
I_THRESH = 0.55
T_THRESH = 0.55
MIN_LEN  = 3      # only test inscriptions with ≥3 signs
N_PERMS  = 5000   # null model permutations


def build_profiles(seqs):
    """Compute I/M/T rates for each P-sign across all sequences."""
    freq = Counter()
    initial = Counter()
    terminal = Counter()
    for seq in seqs:
        n = len(seq)
        for i, s in enumerate(seq):
            freq[s] += 1
            if i == 0:
                initial[s] += 1
            elif i == n - 1:
                terminal[s] += 1
    profiles = {}
    for sign, cnt in freq.items():
        i_rate = initial[sign] / cnt
        t_rate = terminal[sign] / cnt
        slot = "INITIAL" if i_rate >= I_THRESH else ("TERMINAL" if t_rate >= T_THRESH else "MEDIAL")
        profiles[sign] = {"slot": slot, "i_rate": round(i_rate, 3), "t_rate": round(t_rate, 3), "freq": cnt}
    return profiles


def count_tripartite(seqs, profiles):
    """Count inscriptions with at least one I-before-M-before-T pattern."""
    n_tripartite = 0
    n_eligible = 0
    examples = []
    for seq in seqs:
        if len(seq) < MIN_LEN:
            continue
        n_eligible += 1
        slots = [profiles.get(s, {}).get("slot", "MEDIAL") for s in seq]
        # Check if INITIAL appears before MEDIAL appears before TERMINAL
        has_i = "INITIAL" in slots
        has_t = "TERMINAL" in slots
        has_m = "MEDIAL" in slots
        if has_i and has_t and has_m:
            i_last = max(j for j, sl in enumerate(slots) if sl == "INITIAL")
            t_first = min(j for j, sl in enumerate(slots) if sl == "TERMINAL")
            m_any = any(j > i_last and j < t_first for j, sl in enumerate(slots) if sl == "MEDIAL")
            if m_any:
                n_tripartite += 1
                if len(examples) < 5:
                    examples.append({"seq": seq, "slots": slots})
    return n_tripartite, n_eligible, examples


def null_model_rate(seqs, profiles, n_perms=N_PERMS):
    """Shuffle each inscription's slots and compute average tripartite rate."""
    rng = random.Random(42)
    tripartite_rates = []
    for _ in range(min(n_perms, 1000)):  # cap at 1000 for speed
        shuffled = [rng.sample(seq, len(seq)) for seq in seqs if len(seq) >= MIN_LEN]
        n_tri, n_elig, _ = count_tripartite(shuffled, profiles)
        tripartite_rates.append(n_tri / max(1, n_elig))
    return sum(tripartite_rates) / len(tripartite_rates) if tripartite_rates else 0


def main():
    print("Phase-228: CISI Tripartite Grammar Test\n")

    from glossa_lab.data import indus_cisi  # noqa: PLC0415
    seqs = indus_cisi.get_corpus_inscriptions()
    print(f"  CISI inscriptions: {len(seqs)}")

    # Build positional profiles from CISI
    profiles = build_profiles(seqs)
    initial_signs = [s for s, p in profiles.items() if p["slot"] == "INITIAL"]
    terminal_signs = [s for s, p in profiles.items() if p["slot"] == "TERMINAL"]
    medial_signs = [s for s, p in profiles.items() if p["slot"] == "MEDIAL"]
    print(f"  INITIAL signs (I≥{I_THRESH}): {len(initial_signs)} — {initial_signs[:5]}")
    print(f"  TERMINAL signs (T≥{T_THRESH}): {len(terminal_signs)} — {terminal_signs[:5]}")
    print(f"  MEDIAL signs: {len(medial_signs)}")

    # Count tripartite inscriptions
    n_tri, n_elig, examples = count_tripartite(seqs, profiles)
    formula_rate = n_tri / max(1, n_elig)
    print(f"\n  3+ sign inscriptions (eligible): {n_elig}")
    print(f"  Tripartite (I→M→T): {n_tri} ({formula_rate:.1%})")

    # Null model
    print(f"  Running null model ({min(N_PERMS, 1000)} permutations)...")
    null_rate = null_model_rate(seqs, profiles)
    lift = formula_rate / max(0.001, null_rate)
    print(f"  Null rate: {null_rate:.1%}")
    print(f"  Lift: {lift:.0f}×")

    # Compare to Holdat
    holdat_formula_rate = 0.355  # Phase-115
    holdat_null_rate = 0.006    # Phase-115
    holdat_lift = 59.0          # Phase-115
    print()
    print("  COMPARISON vs Holdat (Phase-115):")
    print(f"    Holdat: {holdat_formula_rate:.1%} formula rate, {holdat_lift:.0f}× null lift")
    print(f"    CISI:   {formula_rate:.1%} formula rate, {lift:.0f}× null lift")

    if lift > 2.0:
        verdict = f"SUPPORTED ({lift:.0f}× null). CISI confirms tripartite grammar independently."
    elif lift > 1.5:
        verdict = f"MARGINAL ({lift:.0f}× null). Weak support from CISI."
    else:
        verdict = f"NOT SUPPORTED ({lift:.0f}× null). CISI tripartite rate consistent with null."

    print(f"\n  VERDICT: {verdict}")

    if examples:
        print(f"\n  Sample tripartite inscriptions:")
        for ex in examples[:3]:
            print(f"    {ex['seq']} -> {ex['slots']}")

    result = {
        "phase": 228,
        "n_inscriptions": len(seqs),
        "n_eligible_3plus": n_elig,
        "n_tripartite": n_tri,
        "formula_rate": round(formula_rate, 4),
        "null_rate": round(null_rate, 4),
        "lift_vs_null": round(lift, 2),
        "positional_profiles": {
            "n_initial": len(initial_signs),
            "n_terminal": len(terminal_signs),
            "n_medial": len(medial_signs),
            "initial_signs": initial_signs,
            "terminal_signs": terminal_signs,
        },
        "holdat_comparison": {
            "holdat_formula_rate": holdat_formula_rate,
            "holdat_lift": holdat_lift,
            "cisi_formula_rate": round(formula_rate, 4),
            "cisi_lift": round(lift, 2),
        },
        "verdict": verdict,
        "sample_inscriptions": examples[:5],
        "significance": (
            "LANDMARK: If CISI tripartite rate is significantly above null (>3×), "
            "this constitutes independent cross-corpus validation of the Dravidian "
            "suffix grammar model — a finding publishable in the arXiv paper."
            if lift > 3.0 else
            "Insufficient CISI size (178 inscriptions) may limit statistical power. "
            "Holdat result (35.5%, 59× null) remains primary evidence."
        ),
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n  Saved → {OUT}")
    return result


if __name__ == "__main__":
    main()
