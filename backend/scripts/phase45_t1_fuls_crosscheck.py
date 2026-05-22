"""Phase-45 T1: Wells/Fuls Positional Analysis Cross-Check.

Our 7 HIGH-confidence anchors carry functional readings (CLASSIFIER_PREFIX,
CASE_MARKER_SUFFIX).  Fuls' NWSP (Normalised Weighted Sign Position) method
independently classifies each sign as initial, terminal, medial, or constant.

This script:
  1. Loads the Holdat roles CSV (contains NWSP avg_position, semantic_role,
     is_starter, is_ending for 151 high-frequency signs).
  2. Cross-checks our 7 HIGH anchors: does their Holdat positional profile
     match the expected function implied by our reading?
  3. Tests whether the CLASSIFIER_PREFIX / CASE_MARKER_SUFFIX role mapping
     aligns with the Fuls positional classification.
  4. Computes a concordance score: what % of our anchors agree with Fuls.

Output: reports/phase45_t1_fuls_crosscheck.json
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

REPO   = Path(__file__).parents[2]
ROLES  = REPO / "corpora/downloads/external_repos/holdatllc_indus/all_symbol_semantic_roles 2.csv"
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
REPORTS = REPO / "reports"
REPORTS.mkdir(exist_ok=True)
OUT = REPORTS / "phase45_t1_fuls_crosscheck.json"

# Expected positional profile per reading class
# CLASSIFIER_PREFIX → initial sign → avg_position ≈ 0.0, is_starter=True
# CASE_MARKER_SUFFIX → terminal sign → avg_position ≥ 0.5, is_ending=True
EXPECTED = {
    "M006": {"fn": "CLASSIFIER_PREFIX", "exp_role": "initial", "exp_pos": (0.0, 0.2)},
    "M016": {"fn": "CLASSIFIER_PREFIX", "exp_role": "initial", "exp_pos": (0.0, 0.2)},
    "M045": {"fn": "CLASSIFIER_PREFIX", "exp_role": "initial", "exp_pos": (0.0, 0.2)},
    "M062": {"fn": "CLASSIFIER_PREFIX", "exp_role": "initial", "exp_pos": (0.0, 0.2)},
    "M099": {"fn": "CASE_MARKER_SUFFIX", "exp_role": "terminal", "exp_pos": (0.5, 1.0)},
    "M176": {"fn": "CASE_MARKER_SUFFIX", "exp_role": "terminal", "exp_pos": (0.5, 1.0)},
    "M342": {"fn": "CASE_MARKER_SUFFIX", "exp_role": "terminal", "exp_pos": (0.5, 1.0)},
}

def main() -> None:
    print("Phase-45 T1: Wells/Fuls Positional Cross-Check\n")

    # Load Holdat roles
    roles: dict[str, dict] = {}
    with open(ROLES, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            roles[r["symbol"]] = r

    # Load our anchors
    fa = json.loads(ANCHORS.read_text("utf-8"))
    anchors = fa["anchors"]
    high = {k: v for k, v in anchors.items() if v.get("confidence") == "HIGH"}

    results = []
    agreements = 0
    total = 0

    for sign, exp in EXPECTED.items():
        anchor = high.get(sign, {})
        role = roles.get(sign, {})
        if not role:
            print(f"  {sign}: NOT in Holdat roles CSV (count too low)")
            continue

        avg_pos = float(role.get("avg_position", -1))
        is_starter = role.get("is_starter", "") == "True"
        is_ending = role.get("is_ending", "") == "True"
        holdat_role = role.get("semantic_role", "?")
        reading = anchor.get("reading", "?")

        # Check agreement
        exp_lo, exp_hi = exp["exp_pos"]
        pos_ok = exp_lo <= avg_pos <= exp_hi
        starter_ok = (exp["fn"] == "CLASSIFIER_PREFIX") == is_starter
        ending_ok = (exp["fn"] == "CASE_MARKER_SUFFIX") == is_ending
        role_ok = holdat_role == exp["fn"]

        agree = pos_ok and starter_ok and ending_ok
        if agree:
            agreements += 1
        total += 1

        status = "AGREE" if agree else "DISAGREE"
        print(f"  {sign} = {reading}: avg_pos={avg_pos:.3f}, "
              f"starter={is_starter}, ending={is_ending}, "
              f"holdat_role={holdat_role} → {status}")

        results.append({
            "sign": sign,
            "reading": reading,
            "expected_fn": exp["fn"],
            "avg_position": avg_pos,
            "is_starter": is_starter,
            "is_ending": is_ending,
            "holdat_semantic_role": holdat_role,
            "pos_in_range": pos_ok,
            "starter_matches": starter_ok,
            "ending_matches": ending_ok,
            "role_matches": role_ok,
            "agrees": agree,
        })

    concordance = agreements / total if total > 0 else 0.0
    print(f"\nConcordance: {agreements}/{total} = {concordance:.1%}")

    if concordance >= 0.85:
        verdict = "STRONG_AGREEMENT"
        note = "Our HIGH anchor readings align strongly with Fuls NWSP positional categories"
    elif concordance >= 0.65:
        verdict = "PARTIAL_AGREEMENT"
        note = "Most anchors agree; some disagreements warrant investigation"
    else:
        verdict = "WEAK_AGREEMENT"
        note = "Significant discrepancies with Fuls positional categories"

    print(f"Verdict: {verdict}")

    # Load Fuls texts for qualitative comparison
    fuls_notes = []
    fuls_text = REPO / "glossa-indus/processed/cleaned_text/the_archaeology_and_epigraphy_of_indus_w_27f45a68.txt"
    if fuls_text.exists():
        text = fuls_text.read_text("utf-8", errors="replace")
        # Find sections about Proto-Dravidian and sign identification
        for line in text.split("\n"):
            if any(kw in line.lower() for kw in ["proto-dravidian", "sign list", "17 signs", "reading"]):
                stripped = line.strip()
                if 20 < len(stripped) < 200:
                    fuls_notes.append(stripped[:200])
                    if len(fuls_notes) >= 8:
                        break
        print(f"\nWells 2015 relevant passages ({len(fuls_notes)} found):")
        for note in fuls_notes[:5]:
            print(f'  "{note[:100]}..."')

    result = {
        "_citation": {"primary_sources": ["A.1", "A.13"], "fuls_sources": ["wells_2015"]},
        "summary": {
            "total_high_anchors": len(high),
            "checked_against_fuls": total,
            "agreements": agreements,
            "concordance_pct": round(concordance * 100, 1),
            "verdict": verdict,
            "note": note,
        },
        "anchor_results": results,
        "fuls_wells_passages": fuls_notes[:8],
        "methodology": (
            "Fuls NWSP (Normalised Weighted Sign Position): avg_position 0=initial, 1=terminal. "
            "is_starter/is_ending from Holdat all_symbol_semantic_roles CSV. "
            "Expected: CLASSIFIER_PREFIX signs avg_pos≈0 & is_starter=True; "
            "CASE_MARKER_SUFFIX signs avg_pos≥0.5 & is_ending=True."
        ),
    }

    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), "utf-8")
    print(f"\nReport: {OUT}")

if __name__ == "__main__":
    main()
