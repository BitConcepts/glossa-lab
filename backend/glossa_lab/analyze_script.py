"""Full-corpus script analysis CLI.

Runs ALL Glossa Lab analysis pipelines on a corpus file and produces a
structured JSON report plus human-readable text summary.

This is the primary tool for demonstrating what Glossa Lab will do on
Dr. Fuls' ICIT corpus the day database access is granted.

USAGE:
    # Analyse a corpus file in Fuls +sign-sign-sign+ notation:
    python -m glossa_lab.analyze_script corpus.txt --format fuls

    # Analyse a simple one-sign-per-token flat file:
    python -m glossa_lab.analyze_script corpus.txt --format flat

    # Run on our built-in prototype corpora:
    python -m glossa_lab.analyze_script --demo ugaritic
    python -m glossa_lab.analyze_script --demo linear_b
    python -m glossa_lab.analyze_script --demo indus

    # Compare multiple corpora:
    python -m glossa_lab.analyze_script --compare ugaritic,linear_b,indus

OUTPUT FILES:
    <corpus_name>_report.json   — machine-readable full report
    <corpus_name>_report.txt    — human-readable summary (console too)

REPORT SECTIONS:
  §1  Corpus statistics (N, V, V/N, hapax, inscription length)
  §2  Block entropy profile (H1-H4, normalised, bias-corrected)
  §3  Character/sign frequency distribution (Zipf exponent)
  §4  Positional analysis (initial/medial/terminal preferences)
  §5  Sign cluster analysis (distributional clusters)
  §6  Co-occurrence network (community structure)
  §7  Paradigm detection (inflectional patterns)
  §8  Sign polyvalence (bimodal positional distributions)
  §9  Sign function estimation (numeral/determinative/logogram/phonetic)
  §10 Structural fingerprint (10-dim vector + comparison to known scripts)
  §11 Writing system tier classification
  §12 Kandles colour fingerprint
  §13 Ventris grid analysis (vowel/consonant affinity)
  §14 Word-structure typology match
  §15 Conclusions and open questions
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from typing import Any

_HERE = os.path.dirname(os.path.abspath(__file__))
_BACKEND = os.path.dirname(_HERE)
_TESTS = os.path.join(_BACKEND, "tests")
# Only insert tests/ for demo corpus imports — never insert glossa_lab/ itself
# because that would shadow stdlib 'logging' with our glossa_lab/logging.py.
if _TESTS not in sys.path:
    sys.path.insert(0, _TESTS)
if _BACKEND not in sys.path:
    sys.path.insert(0, _BACKEND)


# ── Corpus loaders ────────────────────────────────────────────────────

def _load_fuls_format(filepath: str) -> list[list[str]]:
    """Load a corpus in Fuls +sign-sign-sign+ notation."""
    from glossa_lab.data.fuls_parser import parse_corpus_file
    entries = parse_corpus_file(filepath)
    return [
        e["inscription"]["sign_ids"]
        for e in entries
        if "inscription" in e
    ]


def _load_flat_format(filepath: str) -> list[list[str]]:
    """Load a flat file: one sign per token, blank lines separate inscriptions."""
    inscriptions: list[list[str]] = []
    current: list[str] = []
    with open(filepath, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                if current:
                    inscriptions.append(current)
                    current = []
            else:
                current.extend(line.split())
    if current:
        inscriptions.append(current)
    return inscriptions


def _load_demo(corpus_name: str) -> tuple[list[list[str]], str]:
    """Load a built-in demo corpus."""
    if corpus_name == "ugaritic":
        import sys
        sys.path.insert(0, _TESTS)
        from corpora.ugaritic import get_undeciphered_corpus
        c = get_undeciphered_corpus()
        return c["inscriptions"], "Ugaritic Baal Cycle (KTU 1.1–1.6)"
    elif corpus_name == "linear_b":
        from pathlib import Path
        fixture = Path(_HERE).parent / "tests" / "corpora" / "fixtures" / "linear_b.txt"
        text = fixture.read_text(encoding="utf-8")
        inscriptions: list[list[str]] = []
        for line in text.splitlines():
            for word in line.strip().split():
                parts = word.replace("3", "").split("-")
                signs = [
                    p.strip().lower()
                    for p in parts
                    if p.strip() and p.strip().replace("*", "").replace("2", "").isalpha()
                ]
                if len(signs) >= 2:
                    inscriptions.append(signs)
        return inscriptions, "Mycenaean Linear B"
    elif corpus_name == "indus":
        from glossa_lab.data.indus_public_corpus import get_corpus_inscriptions
        return get_corpus_inscriptions(), "Indus (Synthetic — Yadav 2010 / Fuls 2014 parameters)"
    elif corpus_name == "hebrew":
        from glossa_lab.data.old_hebrew import get_corpus_inscriptions
        return get_corpus_inscriptions(), "Old Hebrew (consonantal)"
    else:
        raise ValueError(f"Unknown demo corpus: {corpus_name!r}")


# ── Analysis runner ───────────────────────────────────────────────────

def run_full_analysis(
    inscriptions: list[list[str]],
    system_name: str = "unknown",
    verbose: bool = True,
) -> dict[str, Any]:
    """Run all analysis pipelines and return structured report dict."""

    def _print(*a: Any, **kw: Any) -> None:
        if verbose:
            print(*a, **kw)

    flat = [s for insc in inscriptions for s in insc]
    report: dict[str, Any] = {
        "system": system_name,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }

    _print(f"\n{'='*70}")
    _print("  GLOSSA LAB — Full Script Analysis")
    _print(f"  Corpus: {system_name}")
    _print(f"  N={len(flat)}  inscriptions={len(inscriptions)}")
    _print(f"{'='*70}\n")

    # §1 Corpus statistics
    from collections import Counter
    freq = Counter(flat)
    lengths = [len(i) for i in inscriptions if i]
    report["§1_corpus"] = {
        "total_tokens":   len(flat),
        "n_inscriptions": len(inscriptions),
        "distinct_signs": len(freq),
        "type_token_ratio": round(len(freq) / len(flat), 4) if flat else 0,
        "hapax_count":    sum(1 for v in freq.values() if v == 1),
        "hapax_fraction": round(sum(1 for v in freq.values() if v == 1) / len(freq), 3),
        "rare5_fraction": round(sum(1 for v in freq.values() if v <= 5) / len(freq), 3),
        "avg_inscription_length": round(sum(lengths) / len(lengths), 2) if lengths else 0,
        "max_inscription_length": max(lengths) if lengths else 0,
    }
    _print(f"§1  Corpus: N={len(flat)}  V={len(freq)}  "
           f"V/N={len(freq)/len(flat):.3f}  "
           f"hapax={report['§1_corpus']['hapax_fraction']:.0%}  "
           f"avg_len={report['§1_corpus']['avg_inscription_length']:.1f}")

    # §2 Block entropy
    _print("§2  Block entropy...", end=" ", flush=True)
    try:
        from glossa_lab.pipelines.block_entropy import compute_block_entropies
        ent = compute_block_entropies(flat, max_n=4)
        report["§2_entropy"] = ent["block_entropies"]
        h1 = next((e for e in ent["block_entropies"] if e["n"] == 1), {})
        h2 = next((e for e in ent["block_entropies"] if e["n"] == 2), {})
        _print(f"H1_norm={h1.get('normalized', '?'):.3f}  "
               f"H2/H1={h2.get('normalized', 0)/h1.get('normalized', 1):.3f}")
    except Exception as e:
        report["§2_entropy"] = {"error": str(e)}
        _print(f"SKIP ({e})")

    # §3 Char frequency / Zipf
    _print("§3  Char frequency / Zipf...", end=" ", flush=True)
    try:
        from glossa_lab.pipelines.char_freq import compute_char_freq
        cf = compute_char_freq(flat)
        report["§3_freq"] = {
            "zipf_exponent": cf.get("zipf_exponent"),
            "top_10": cf.get("rank_frequency", [])[:10],
        }
        _print(f"Zipf α={cf.get('zipf_exponent', '?')}")
    except Exception as e:
        report["§3_freq"] = {"error": str(e)}
        _print(f"SKIP ({e})")

    # §4 Positional analysis
    _print("§4  Positional analysis...", end=" ", flush=True)
    try:
        from glossa_lab.pipelines.positional import compute_positional_freq
        pos = compute_positional_freq(inscriptions)
        n_initial_dominant = sum(
            1 for p in pos.get("profiles", [])
            if p.get("dominant_position") == "initial"
        )
        n_terminal_dominant = sum(
            1 for p in pos.get("profiles", [])
            if p.get("dominant_position") == "terminal"
        )
        report["§4_positional"] = {
            "initial_dominant_signs": n_initial_dominant,
            "terminal_dominant_signs": n_terminal_dominant,
            "top_initial": [
                p["sign"] for p in pos.get("profiles", [])
                if p.get("dominant_position") == "initial"
            ][:5],
            "top_terminal": [
                p["sign"] for p in pos.get("profiles", [])
                if p.get("dominant_position") == "terminal"
            ][:5],
        }
        _print(f"initial-dominant={n_initial_dominant}  terminal-dominant={n_terminal_dominant}")
    except Exception as e:
        report["§4_positional"] = {"error": str(e)}
        _print(f"SKIP ({e})")

    # §5 Sign clusters
    _print("§5  Sign clusters...", end=" ", flush=True)
    try:
        from glossa_lab.pipelines.sign_cluster import compute_sign_clusters
        sc = compute_sign_clusters(inscriptions, min_freq=3, top_n=20)
        report["§5_clusters"] = {
            "n_clusters": len(sc.get("clusters", [])),
            "clustered_signs": sc.get("clustered_signs", 0),
            "clusters": sc.get("clusters", [])[:5],
        }
        _print(f"clusters={len(sc.get('clusters', []))}  "
               f"signs_clustered={sc.get('clustered_signs', 0)}")
    except Exception as e:
        report["§5_clusters"] = {"error": str(e)}
        _print(f"SKIP ({e})")

    # §6 Co-occurrence network
    _print("§6  Co-occurrence network...", end=" ", flush=True)
    try:
        from glossa_lab.pipelines.cooccurrence import build_cooccurrence_network
        co = build_cooccurrence_network(flat, window=2, min_freq=3, min_edge_weight=2)
        report["§6_cooccurrence"] = {
            "nodes": co.get("node_count", 0),
            "edges": co.get("edge_count", 0),
            "communities": co.get("community_count", 0),
        }
        _print(f"nodes={co.get('node_count', 0)}  "
               f"edges={co.get('edge_count', 0)}  "
               f"communities={co.get('community_count', 0)}")
    except Exception as e:
        report["§6_cooccurrence"] = {"error": str(e)}
        _print(f"SKIP ({e})")

    # §7 Paradigm detection
    _print("§7  Paradigm detection...", end=" ", flush=True)
    try:
        from glossa_lab.pipelines.paradigm import detect_paradigms
        par = detect_paradigms(inscriptions, min_stem_freq=2, min_variants=2)
        report["§7_paradigms"] = {
            "paradigm_count": par.get("paradigm_count", 0),
            "top_paradigms": par.get("paradigms", [])[:3],
        }
        _print(f"paradigms={par.get('paradigm_count', 0)}")
    except Exception as e:
        report["§7_paradigms"] = {"error": str(e)}
        _print(f"SKIP ({e})")

    # §8 Sign polyvalence
    _print("§8  Sign polyvalence...", end=" ", flush=True)
    try:
        from glossa_lab.pipelines.sign_polyvalence import detect_polyvalent_signs
        pv = detect_polyvalent_signs(inscriptions, min_freq=3)
        summary = pv.get("summary", {})
        report["§8_polyvalence"] = {
            "candidates": summary.get("polyvalence_candidates", 0),
            "fraction": summary.get("candidate_fraction", 0),
            "top_5": [
                {"sign": c["sign"], "score": c["bimodality_score"]}
                for c in pv.get("candidates", [])[:5]
            ],
        }
        _print(f"candidates={summary.get('polyvalence_candidates', 0)}  "
               f"({summary.get('candidate_fraction', 0):.0%})")
    except Exception as e:
        report["§8_polyvalence"] = {"error": str(e)}
        _print(f"SKIP ({e})")

    # §9 Sign function estimation
    _print("§9  Sign function estimation...", end=" ", flush=True)
    try:
        from glossa_lab.pipelines.sign_function_estimator import estimate_sign_functions
        sf = estimate_sign_functions(inscriptions, min_freq=3)
        report["§9_sign_functions"] = {
            "system_summary": sf.get("system_summary", {}),
            "type_counts":    sf.get("type_counts", {}),
            "phonetic_inventory_estimate": sf.get("phonetic_inventory_estimate", 0),
            "likely_phonetics":      [s["sign"] for s in sf.get("likely_phonetics", [])[:10]],
            "likely_determinatives": [s["sign"] for s in sf.get("likely_determinatives", [])[:5]],
            "interpretation": sf.get("interpretation", ""),
        }
        summary_str = "  ".join(
            f"{k}={v:.0%}" for k, v in sf.get("system_summary", {}).items()
        )
        _print(f"{summary_str}")
    except Exception as e:
        report["§9_sign_functions"] = {"error": str(e)}
        _print(f"SKIP ({e})")

    # §10 Structural fingerprint
    _print("§10 Structural fingerprint...", end=" ", flush=True)
    try:
        from glossa_lab.pipelines.structural_fingerprint import (
            compare_scripts,
            compute_fingerprint,
            known_fingerprints_db,
        )
        fp = compute_fingerprint(inscriptions, system_name=system_name)
        ranking = compare_scripts(fp, known_fingerprints_db())
        report["§10_fingerprint"] = {
            "vector": fp.get("vector", []),
            "dimensions": fp.get("dimensions", {}),
            "notes": fp.get("notes", []),
            "nearest_known": ranking[:3],
        }
        if ranking:
            nearest = ranking[0]
            _print(f"nearest={nearest['system']} (dist={nearest['distance']:.3f})")
        else:
            _print("no comparison available")
    except Exception as e:
        report["§10_fingerprint"] = {"error": str(e)}
        _print(f"SKIP ({e})")

    # §11 Writing system tier
    _print("§11 Writing system tier classification...", end=" ", flush=True)
    try:
        from glossa_lab.experiments.writing_system_progression import (
            corpus_statistics as tier_stats,
        )
        stats = tier_stats(inscriptions, system_name=system_name)
        report["§11_tier"] = {
            "decipher_difficulty": stats.get("decipher_difficulty", "?"),
            "type_token_ratio": stats.get("type_token_ratio", 0),
            "hapax_fraction": stats.get("hapax_fraction", 0),
        }
        _print(stats.get("decipher_difficulty", "?")[:60])
    except Exception as e:
        report["§11_tier"] = {"error": str(e)}
        _print(f"SKIP ({e})")

    # §12 Kandles colour fingerprint
    _print("§12 Kandles colour fingerprint...", end=" ", flush=True)
    try:
        from glossa_lab.pipelines.kandles import generate_grid
        kg = generate_grid(flat[:200])
        report["§12_kandles"] = {
            "colour_distribution": kg.get("color_distribution", {}),
            "profile": kg.get("profile", "default"),
        }
        dist = kg.get("color_distribution", {})
        _print("  ".join(f"{k}={v}" for k, v in list(dist.items())[:5]))
    except Exception as e:
        report["§12_kandles"] = {"error": str(e)}
        _print(f"SKIP ({e})")

    # §13 Ventris grid (vowel/consonant affinity)
    _print("§13 Ventris grid analysis...", end=" ", flush=True)
    try:
        from glossa_lab.pipelines.logosyllabic import (
            classify_signs,
            compute_affinity,
        )
        sign_class = classify_signs(inscriptions, flat)
        syllabograms = [
            s for s, info in sign_class.items() if info["type"] == "syllabogram"
        ]
        affinity = compute_affinity(inscriptions, syllabograms, top_n=20)
        n_vowel_groups = len(affinity.get("vowel_clusters", []))
        n_cons_groups  = len(affinity.get("consonant_clusters", []))
        report["§13_ventris"] = {
            "n_syllabograms":    len(syllabograms),
            "n_logograms":       sum(1 for i in sign_class.values() if i["type"] == "logogram"),
            "n_determinatives":  sum(
                1 for i in sign_class.values() if i["type"] == "determinative"
            ),
            "vowel_affinity_groups":    n_vowel_groups,
            "consonant_affinity_groups": n_cons_groups,
            "sign_classification_sample": dict(list(sign_class.items())[:10]),
        }
        _print(f"syllabograms={len(syllabograms)}  "
               f"logograms={sum(1 for i in sign_class.values() if i['type']=='logogram')}  "
               f"vowel_groups={n_vowel_groups}")
    except Exception as e:
        report["§13_ventris"] = {"error": str(e)}
        _print(f"SKIP ({e})")

    # §14 Word-structure typology
    _print("§14 Word-structure typology...", end=" ", flush=True)
    try:
        from glossa_lab.pipelines.word_structure_hypothesis import rank_language_families
        wsh = rank_language_families(flat)
        report["§14_word_structure"] = {
            "ranking": wsh.get("ranked_families", [])[:5],
            "best_match": wsh.get("ranked_families", [{}])[0] if wsh.get("ranked_families") else {},
        }
        if wsh.get("ranked_families"):
            top = wsh["ranked_families"][0]
            _print(f"best_match={top.get('family', '?')} (KL={top.get('kl_divergence', '?'):.4f})")
        else:
            _print("no result")
    except Exception as e:
        report["§14_word_structure"] = {"error": str(e)}
        _print(f"SKIP ({e})")

    # §15 Conclusions
    _print("\n§15 Conclusions:")
    conclusions = _generate_conclusions(report, system_name)
    report["§15_conclusions"] = conclusions
    for line in conclusions:
        _print(f"  • {line}")

    return report


def _generate_conclusions(report: dict[str, Any], system_name: str) -> list[str]:
    """Derive key conclusions from the analysis results."""
    conclusions: list[str] = []

    # Corpus size assessment
    corpus = report.get("§1_corpus", {})
    N = corpus.get("total_tokens", 0)
    vn = corpus.get("type_token_ratio", 0)
    hapax = corpus.get("hapax_fraction", 0)
    if N < 1000:
        conclusions.append(
            f"Small corpus (N={N}): statistical signals are weak. More data needed."
        )
    elif vn < 0.05 and hapax < 0.10:
        conclusions.append(
            f"Low V/N ({vn:.3f}) + low hapax ({hapax:.0%}) → abjad/alphabet profile."
        )
    elif vn < 0.12:
        conclusions.append(
            f"Moderate V/N ({vn:.3f}) → consistent with a syllabary system."
        )
    else:
        conclusions.append(
            f"High V/N ({vn:.3f}) + hapax ({hapax:.0%}) → logo-syllabic profile. "
            f"Most signs are rare; 1:1 substitution cipher model is not appropriate."
        )

    # Entropy assessment
    ent = report.get("§2_entropy", [])
    if isinstance(ent, list) and len(ent) >= 2:
        h1 = next((e for e in ent if e.get("n") == 1), {})
        h1n = h1.get("normalized", 0)
        if 0.60 < h1n < 0.95:
            conclusions.append(f"Block entropy H1_norm={h1n:.3f}: firmly in linguistic range.")

    # Fingerprint nearest match
    fp = report.get("§10_fingerprint", {})
    nearest = fp.get("nearest_known", [{}])
    if nearest and nearest[0]:
        n = nearest[0]
        conclusions.append(
            f"Structural fingerprint: most similar to '{n.get('system', '?')}' "
            f"({n.get('writing_type', '?')}, dist={n.get('distance', '?'):.3f})."
        )

    # Sign function breakdown
    sf = report.get("§9_sign_functions", {})
    summary = sf.get("system_summary", {})
    if summary:
        phonetic_frac = summary.get("phonetic", 0)
        det_frac = summary.get("determinative", 0)
        log_frac = summary.get("logogram", 0)
        conclusions.append(
            f"Estimated sign functions: phonetic {phonetic_frac:.0%}, "
            f"logographic {log_frac:.0%}, determinative {det_frac:.0%}."
        )
        phonetic_n = sf.get("phonetic_inventory_estimate", 0)
        if phonetic_n > 0:
            conclusions.append(
                f"Estimated phonetic sign inventory: ~{phonetic_n} signs."
            )

    # Polyvalence
    pv = report.get("§8_polyvalence", {})
    pv_frac = pv.get("fraction", 0)
    if pv_frac > 0.15:
        conclusions.append(
            f"High polyvalence fraction ({pv_frac:.0%}): significant proportion of signs "
            f"serve dual positional roles. Consistent with logo-syllabic script."
        )

    # Word-structure match
    wsh = report.get("§14_word_structure", {})
    best = wsh.get("best_match", {})
    if best.get("family"):
        conclusions.append(
            f"Word-length typology best matches: {best['family']} "
            f"(KL={best.get('kl_divergence', '?'):.4f})."
        )

    if not conclusions:
        conclusions.append("Insufficient data for strong conclusions.")

    return conclusions


# ── Comparison mode ───────────────────────────────────────────────────

def run_comparison(
    corpus_names: list[str],
    verbose: bool = True,
) -> dict[str, Any]:
    """Run analysis on multiple corpora and generate a comparison table."""
    results: dict[str, dict[str, Any]] = {}
    fingerprints: dict[str, dict[str, Any]] = {}

    for name in corpus_names:
        print(f"\n{'─'*70}")
        print(f"Analysing: {name}")
        inscriptions, system_name = _load_demo(name)
        report = run_full_analysis(inscriptions, system_name, verbose=verbose)
        results[name] = report
        # Collect fingerprint for cross-comparison
        fp_section = report.get("§10_fingerprint", {})
        if fp_section.get("vector"):
            fingerprints[system_name] = {
                "system": system_name,
                "vector": fp_section["vector"],
                "writing_type": "computed",
            }

    # Cross-compare all pairs
    from glossa_lab.pipelines.structural_fingerprint import (
        compare_scripts,
        known_fingerprints_db,
    )
    db = known_fingerprints_db(include_computed=fingerprints)
    cross = {}
    for name, fp_data in fingerprints.items():
        cross[name] = compare_scripts(
            {"system": name, "vector": fp_data["vector"]},
            db=db,
        )[:3]

    return {
        "individual_results": results,
        "cross_comparison": cross,
    }


# ── Report serialisation ──────────────────────────────────────────────

def save_report(
    report: dict[str, Any],
    output_path: str,
    verbose: bool = True,
) -> None:
    """Save report as JSON and human-readable text."""
    base = output_path.replace(".json", "")

    # JSON
    json_path = base + ".json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, default=str)
    if verbose:
        print(f"\n  JSON  → {json_path}")

    # Text summary
    txt_path = base + ".txt"
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("GLOSSA LAB — Script Analysis Report\n")
        f.write(f"System:    {report.get('system', '?')}\n")
        f.write(f"Generated: {report.get('timestamp', '?')}\n")
        f.write("=" * 70 + "\n\n")

        for key in sorted(k for k in report if k.startswith("§")):
            section = report[key]
            f.write(f"\n{key.upper()}\n")
            f.write("-" * 40 + "\n")
            if isinstance(section, dict):
                for k, v in section.items():
                    if k not in ("error",) and not isinstance(v, (list, dict)):
                        f.write(f"  {k:<30}: {v}\n")
            elif isinstance(section, list):
                for item in section[:5]:
                    f.write(f"  • {item}\n")

    if verbose:
        print(f"  Text  → {txt_path}")


# ── CLI ───────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Glossa Lab — Full Script Analysis Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Analyse built-in demo corpora:
    python -m glossa_lab.analyze_script --demo ugaritic
    python -m glossa_lab.analyze_script --demo linear_b
    python -m glossa_lab.analyze_script --demo indus

  Compare multiple corpora:
    python -m glossa_lab.analyze_script --compare ugaritic,linear_b,indus

  Analyse a corpus file:
    python -m glossa_lab.analyze_script corpus.txt --format fuls
""",
    )
    parser.add_argument("file", nargs="?", help="Corpus file to analyse")
    parser.add_argument(
        "--format", choices=["fuls", "flat"], default="fuls",
        help="Input format (default: fuls)",
    )
    parser.add_argument(
        "--demo", choices=["ugaritic", "linear_b", "indus", "hebrew"],
        help="Run on a built-in demo corpus",
    )
    parser.add_argument(
        "--compare", type=str,
        help="Comma-separated list of demo corpora to compare",
    )
    parser.add_argument(
        "--output", type=str, default=None,
        help="Output file path (without extension). Defaults to <corpus>_report",
    )
    parser.add_argument("--quiet", action="store_true", help="Suppress output")
    args = parser.parse_args()

    verbose = not args.quiet

    if args.compare:
        names = [n.strip() for n in args.compare.split(",")]
        result = run_comparison(names, verbose=verbose)
        out = args.output or "_vs_".join(names) + "_comparison"
        save_report(result, out + ".json", verbose=verbose)
        return

    if args.demo:
        inscriptions, system_name = _load_demo(args.demo)
        out = args.output or f"{args.demo}_report"
    elif args.file:
        loader = _load_fuls_format if args.format == "fuls" else _load_flat_format
        inscriptions = loader(args.file)
        system_name = os.path.splitext(os.path.basename(args.file))[0]
        out = args.output or system_name + "_report"
    else:
        parser.print_help()
        return

    report = run_full_analysis(inscriptions, system_name, verbose=verbose)
    save_report(report, out + ".json", verbose=verbose)


if __name__ == "__main__":
    main()
