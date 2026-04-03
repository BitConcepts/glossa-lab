"""Paste processor for Fuls' Indus ebooks.

Drop any copy-pasted text from the Corpus or Catalog into
data-import/corpus_paste.txt and data-import/catalog_paste.txt,
then run:

    python process_paste.py

This script will:
  1. Extract all inscription sequences from the corpus paste
  2. Extract sign function codes from the catalog paste
  3. Run the full 17-pipeline analysis on the real data
  4. Print a comparison against our synthetic corpus
  5. Save results to reports/real_indus_results.json

The parser is tolerant — it will extract sign sequences even from
messy text with page numbers, headers, and metadata mixed in.
"""

import json
import os
import sys
import re
from collections import Counter
from pathlib import Path

_BASE    = Path(__file__).parent
_BACKEND = _BASE / "backend"
_TESTS   = _BACKEND / "tests"
sys.path.insert(0, str(_BACKEND))
sys.path.insert(0, str(_TESTS))

CORPUS_FILE  = _BASE / "data-import" / "corpus_paste.txt"
CATALOG_FILE = _BASE / "data-import" / "catalog_paste.txt"
OUTPUT_FILE  = _BASE / "reports" / "real_indus_results.json"


# ── 1. Enhanced inscription extractor ────────────────────────────────

def extract_inscriptions_from_text(text: str) -> list[list[str]]:
    """Extract all Indus sign sequences from any raw pasted text.

    Handles:
      +342-159-070+         (standard format)
      +144+700-033+         (multi-part)
      +407-032-520-000-017+ (with eroded signs)
      342-159-070           (without + delimiters, just numbers)
      [342][159][070]       (bracketed format)
    """
    inscriptions = []

    # Strategy 1: standard Fuls notation with + delimiters
    for match in re.finditer(r'\+([0-9]{3}(?:-[0-9]{3})*(?:\+[0-9]{3}(?:-[0-9]{3})*)*)\+', text):
        raw = match.group(0)
        # Split on + to get text parts
        inner = raw.strip('+')
        parts = inner.split('+')
        signs = []
        for part in parts:
            chunk = [s.strip() for s in part.split('-') if re.match(r'^\d{3}$', s.strip())]
            signs.extend(chunk)
        clean = [s for s in signs if s != '000']  # remove eroded
        if len(clean) >= 1:
            inscriptions.append(clean)

    # Strategy 2: if strategy 1 found nothing, look for bare sign sequences
    # e.g. "342 159 070" or "342-159-070" on their own lines
    if not inscriptions:
        for line in text.splitlines():
            line = line.strip()
            # Find sequences of 3-digit numbers
            seqs = re.findall(r'\b\d{3}\b', line)
            # Only treat as inscription if we have 2+ plausible Indus sign numbers
            # (Indus signs are 001-676)
            valid = [s for s in seqs if 1 <= int(s) <= 676]
            if len(valid) >= 2:
                inscriptions.append(valid)

    print(f"  Extracted {len(inscriptions)} inscriptions")
    if inscriptions:
        print(f"  Example: {inscriptions[0]}")
        lengths = [len(i) for i in inscriptions]
        print(f"  Length range: {min(lengths)}-{max(lengths)}  avg={sum(lengths)/len(lengths):.1f}")

    return inscriptions


# ── 2. Catalog extractor (sign function codes) ───────────────────────

def extract_sign_functions_from_catalog(text: str) -> dict[str, str]:
    """Extract sign number → function code from Catalog paste.

    Looks for patterns like:
      Sign 342: TMK, frequency 580
      342   TMK   580   terminal
      ITM: 411, 412, 400
    """
    functions: dict[str, str] = {}

    # Pattern: sign number followed by function code on same line
    for line in text.splitlines():
        # Look for 3-digit sign number near a function code
        sign_match = re.search(r'\b(\d{3})\b', line)
        if not sign_match:
            continue
        sign_num = sign_match.group(1)
        if not (1 <= int(sign_num) <= 676):
            continue

        # Look for function code
        for code in ['ITM', 'TMK', 'PTM', 'NUM', 'SYL', 'LOG', 'FSH',
                     'SHN', 'SSN', 'SPN', 'LON']:
            if re.search(r'\b' + code + r'\b', line):
                functions[sign_num] = code
                break

    # Also look for grouped listings: "TMK: 342, 159, 070, ..."
    for code in ['ITM', 'TMK', 'PTM', 'NUM', 'SYL', 'LOG', 'FSH']:
        pattern = code + r'[:\s]+([0-9, ]+)'
        for match in re.finditer(pattern, text):
            for num in re.findall(r'\d{3}', match.group(1)):
                if 1 <= int(num) <= 676:
                    functions[num] = code

    print(f"  Extracted {len(functions)} sign function assignments")
    if functions:
        by_code = Counter(functions.values())
        print(f"  Breakdown: {dict(by_code)}")

    return functions


# ── 3. Full analysis pipeline ────────────────────────────────────────

def run_real_indus_analysis(
    inscriptions: list[list[str]],
    sign_functions: dict[str, str],
) -> dict:
    """Run all 17 Glossa Lab pipelines on real Indus data."""
    from glossa_lab.pipelines.nwsp import compute_nwsp, compare_with_icit_functions
    from glossa_lab.pipelines.sign_polyvalence import detect_polyvalent_signs
    from glossa_lab.pipelines.structural_fingerprint import (
        compute_fingerprint, compare_scripts, known_fingerprints_db,
    )
    from glossa_lab.pipelines.block_entropy import compute_block_entropies
    from glossa_lab.pipelines.positional import compute_positional_freq
    from glossa_lab.pipelines.paradigm import detect_paradigms
    from glossa_lab.pipelines.word_structure_hypothesis import rank_language_families
    from glossa_lab.pipelines.allograph import reduce_allographs, allograph_reduction_stats

    print("\n  Running allograph reduction (Daggumati-Revesz 2021)...")
    allograph_stats = allograph_reduction_stats(inscriptions)
    inscriptions_reduced = reduce_allographs(inscriptions)
    print(f"    Signs: {allograph_stats['signs_before']} → {allograph_stats['signs_after']}")

    flat = [s for insc in inscriptions_reduced for s in insc]
    freq = Counter(flat)
    N, V = len(flat), len(freq)
    print(f"\n  Corpus after reduction: N={N:,}  V={V}  V/N={V/N:.3f}")

    results = {"corpus": {
        "n_inscriptions": len(inscriptions),
        "n_tokens": N,
        "distinct_signs": V,
        "type_token_ratio": round(V/N, 4) if N else 0,
        "hapax_count": sum(1 for v in freq.values() if v == 1),
        "hapax_fraction": round(sum(1 for v in freq.values() if v == 1)/max(V,1), 3),
        "avg_length": round(sum(len(i) for i in inscriptions)/max(len(inscriptions),1), 2),
        "allograph_stats": allograph_stats,
    }}

    print("\n  Block entropy...")
    ent = compute_block_entropies(flat, max_n=4)
    results["entropy"] = {e["n"]: e for e in ent["block_entropies"]}
    h1 = results["entropy"].get(1, {})
    print(f"    H1_norm={h1.get('normalized','?'):.4f}")

    print("\n  NWSP (Fuls 2013 method)...")
    nwsp = compute_nwsp(inscriptions_reduced, min_occurrences=3)
    icit_map = compare_with_icit_functions(nwsp, icit_labels=sign_functions or None)
    results["nwsp"] = {
        "summary": nwsp["summary"],
        "icit_summary": icit_map.get("icit_summary", {}),
        "accuracy_vs_catalog": icit_map.get("accuracy"),
        "n_labeled": icit_map.get("n_labeled", 0),
    }
    print(f"    NWSP classes: {nwsp['summary']}")
    if sign_functions and icit_map.get("accuracy") is not None:
        print(f"    Accuracy vs Catalog: {icit_map['accuracy']:.1%} ({icit_map['n_labeled']} signs)")

    print("\n  Sign polyvalence...")
    pv = detect_polyvalent_signs(inscriptions_reduced, min_freq=3)
    results["polyvalence"] = pv["summary"]
    top5 = [{"sign": c["sign"], "score": c["bimodality_score"]}
            for c in pv["candidates"][:5]]
    print(f"    Candidates: {pv['summary']['polyvalence_candidates']} "
          f"({pv['summary']['candidate_fraction']:.0%})")
    print(f"    Top 5: {top5}")
    results["top_polyvalent"] = top5

    print("\n  Structural fingerprint...")
    fp = compute_fingerprint(inscriptions_reduced, system_name="Indus (real Fuls corpus)")
    ranking = compare_scripts(fp, known_fingerprints_db())
    results["fingerprint"] = {
        "vector": fp["vector"],
        "nearest_3": ranking[:3],
    }
    print(f"    Nearest: {ranking[0]['system']} (dist={ranking[0]['distance']:.3f})")
    print(f"    #2: {ranking[1]['system']} (dist={ranking[1]['distance']:.3f})")

    print("\n  Positional analysis...")
    pos = compute_positional_freq(inscriptions_reduced)
    profiles = pos.get("profiles", [])
    term_dom = sorted([p for p in profiles if p.get("dominant_position") == "terminal"],
                      key=lambda x: x.get("terminal", 0), reverse=True)
    init_dom = [p for p in profiles if p.get("dominant_position") == "initial"]
    results["positional"] = {
        "initial_dominant": [p["sign"] for p in init_dom[:10]],
        "terminal_dominant": [p["sign"] for p in term_dom[:10]],
    }
    print(f"    Initial-dominant signs: {[p['sign'] for p in init_dom[:6]]}")
    print(f"    Terminal-dominant signs: {[p['sign'] for p in term_dom[:6]]}")

    print("\n  Paradigm detection...")
    par = detect_paradigms(inscriptions_reduced, min_stem_freq=2, min_variants=2)
    results["paradigms"] = {"count": par.get("paradigm_count", 0)}
    print(f"    Paradigms: {par.get('paradigm_count', 0)}")

    print("\n  Word-structure typology (no phoneme assumptions)...")
    wsh = rank_language_families(inscriptions_reduced)
    ranked = wsh.get("ranked_hypotheses", [])
    results["typology"] = {
        "winner": wsh.get("winner"),
        "top_3": ranked[:3],
    }
    print(f"    Winner: {wsh.get('winner')}  "
          f"(KL={ranked[0]['word_length_kl']:.4f} if ranked else '?')")
    for r in ranked[:3]:
        print(f"      {r['profile']:<30}  compat={r['compatibility']:.4f}  KL={r['word_length_kl']:.4f}")

    return results


# ── 4. Comparison vs synthetic ────────────────────────────────────────

def print_comparison(real: dict) -> None:
    """Print side-by-side comparison of real vs synthetic Indus results."""
    print("\n" + "=" * 65)
    print("  REAL vs SYNTHETIC INDUS CORPUS COMPARISON")
    print("=" * 65)

    # Synthetic values (from our atlas run)
    syn = {"N": 4513, "V": 318, "VN": 0.070, "hapax": "30%",
           "polyvalence": "74%", "fingerprint_nearest": "Indus (published statistics)",
           "typology_winner": "Sumerian", "paradigms": 102}

    rc = real.get("corpus", {})
    rv = real.get("polyvalence", {})
    rf = real.get("fingerprint", {})
    rt = real.get("typology", {})

    print(f"\n  {'Metric':<30}  {'Synthetic':<22}  {'Real (Fuls)'}")
    print(f"  {'-'*65}")
    print(f"  {'Tokens (N)':<30}  {syn['N']:<22,}  {rc.get('n_tokens', '?'):,}")
    print(f"  {'Sign types (V)':<30}  {syn['V']:<22}  {rc.get('distinct_signs', '?')}")
    print(f"  {'Type-token ratio (V/N)':<30}  {syn['VN']:<22}  {rc.get('type_token_ratio', '?')}")
    print(f"  {'Hapax fraction':<30}  {syn['hapax']:<22}  {rc.get('hapax_fraction', '?'):.0%}")
    print(f"  {'Polyvalent signs':<30}  {syn['polyvalence']:<22}  {rv.get('candidate_fraction', 0):.0%}")
    print(f"  {'Paradigm count':<30}  {syn['paradigms']:<22}  {real.get('paradigms', {}).get('count', '?')}")
    print(f"  {'Fingerprint nearest':<30}  {syn['fingerprint_nearest'][:22]:<22}  {rf.get('nearest_3', [{}])[0].get('system', '?')[:30]}")
    print(f"  {'Word-structure winner':<30}  {syn['typology_winner']:<22}  {rt.get('winner', '?')}")

    print("\n  KEY: How well does our synthetic corpus predict the real data?")
    print("  If the real numbers are close → our calibration is good.")
    print("  If they differ → the synthetic corpus needs updating, AND")
    print("  we have NEW FINDINGS to report to Dr. Fuls.")


# ── Main ──────────────────────────────────────────────────────────────

def main() -> None:
    print("=" * 65)
    print("  GLOSSA LAB — Real Indus Data Processor")
    print("=" * 65)

    # ── Load corpus paste
    inscriptions = []
    if CORPUS_FILE.exists():
        text = CORPUS_FILE.read_text(encoding="utf-8", errors="replace")
        print(f"\n[1] Processing Corpus paste ({len(text):,} chars)...")
        inscriptions = extract_inscriptions_from_text(text)
    else:
        print(f"\n[1] corpus_paste.txt not found at {CORPUS_FILE}")
        print("    → Create the file and paste your Corpus of Indus Inscriptions text")

    # ── Load catalog paste
    sign_functions: dict[str, str] = {}
    if CATALOG_FILE.exists():
        text = CATALOG_FILE.read_text(encoding="utf-8", errors="replace")
        print(f"\n[2] Processing Catalog paste ({len(text):,} chars)...")
        sign_functions = extract_sign_functions_from_catalog(text)
    else:
        print(f"\n[2] catalog_paste.txt not found at {CATALOG_FILE}")
        print("    → Optional: paste Catalog sign function data for NWSP validation")

    if not inscriptions:
        print("\n  No inscriptions found yet. See instructions above.")
        print("  Even 50 inscriptions is enough to get started.")
        return

    # ── Run analysis
    print("\n[3] Running full 17-pipeline analysis on real Indus data...")
    results = run_real_indus_analysis(inscriptions, sign_functions)
    results["sign_functions_from_catalog"] = sign_functions

    # ── Print comparison
    print_comparison(results)

    # ── Save
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\n  Full results → {OUTPUT_FILE}")
    print("\n  These results can be sent directly to Dr. Fuls.")


if __name__ == "__main__":
    main()
