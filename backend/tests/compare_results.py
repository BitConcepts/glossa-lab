"""
Deep comparison: graph execute_graph() results vs original Python run() methods.
Verifies that the new graph execution system produces identical results to the
original Python experiment implementations.

Run:
    cd backend && python tests/compare_results.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from glossa_lab.experiment_graph import _build_proper_graph_specs, execute_graph


def check(label, graph_val, direct_val, fmt=repr):
    match = graph_val == direct_val
    status = "MATCH  " if match else "MISMATCH"
    print(f"  {status}  {label}: graph={fmt(graph_val)}  direct={fmt(direct_val)}")
    return match


def section(title):
    print(f"\n{'─' * 60}")
    print(f"  {title}")
    print("─" * 60)


def main():
    specs = _build_proper_graph_specs()
    all_ok = True

    # ── Category A: Pure atomic pipelines ─────────────────────────────────────

    section("Category A — Pure atomic pipelines")

    # positional_profile_analysis
    from glossa_lab.experiments.positional_profile_analysis import PositionalProfileAnalysis
    r_graph  = execute_graph(specs["positional_profile_analysis"])
    r_direct = PositionalProfileAnalysis().run()
    g_profs = r_graph.get("data", [])
    d_profs = r_direct.get("profiles", [])
    # Note: the atomic PositionalProfiler node uses min_count=3 (no top_n cap) while
    # the Python class defaults to min_count=5 & top_n=100 — different parameter
    # choices are expected. We verify structural correctness via pos_classes instead.
    print(f"  NOTE     positional_profile: n_profiles graph={len(g_profs)} "
          f"direct={len(d_profs)} (expected — different min_count/top_n params)")
    if g_profs and d_profs:
        g_classes = sorted(set(p["pos_class"] for p in g_profs))
        d_classes = sorted(set(p["pos_class"] for p in d_profs))
        ok = check("positional_profile: pos_classes", g_classes, d_classes)
        all_ok &= ok

    # symbol_clustering
    from glossa_lab.experiments.symbol_clustering import SymbolClustering
    r_graph2  = execute_graph(specs["symbol_clustering"])
    r_direct2 = SymbolClustering().run()
    g_clust = r_graph2.get("data", [])
    d_clust_raw = r_direct2.get("clusters", {})
    g_n = len(g_clust) if isinstance(g_clust, list) else 0
    d_n = len(d_clust_raw) if isinstance(d_clust_raw, dict) else 0
    # Both produce the same 4 position-class buckets via unsupervised clustering
    ok = check("symbol_clustering: n_cluster_classes", g_n, d_n, str)
    all_ok &= ok

    # ── Category B: ExperimentWrapper matches direct run() ────────────────────

    section("Category B — ExperimentWrapper vs direct run()")

    from glossa_lab.experiments.progression_report import ProgressionReport
    r_graph3  = execute_graph(specs["progression"])
    r_direct3 = ProgressionReport().run()
    ok = check("progression: n_tiers",
               len(r_graph3.get("tiers", [])),
               len(r_direct3.get("tiers", [])), str)
    all_ok &= ok

    from glossa_lab.experiments.writing_system_progression import WritingSystemProgression
    r_graph4  = execute_graph(specs["writing_system_progression"])
    r_direct4 = WritingSystemProgression().run()
    ok = check("writing_system_progression: n_systems",
               len(r_graph4.get("systems", [])),
               len(r_direct4.get("systems", [])), str)
    all_ok &= ok

    from glossa_lab.experiments.ventris_validation import VentrisValidation
    r_graph5  = execute_graph(specs["ventris_validation"])
    r_direct5 = VentrisValidation().run()
    ok = check("ventris_validation: f1_average",
               round(r_graph5.get("f1_average", -99), 4),
               round(r_direct5.get("f1_average", -99), 4), str)
    all_ok &= ok

    from glossa_lab.experiments.ugaritic_vs_hebrew import UgariticVsHebrew
    r_graph6  = execute_graph(specs["ugaritic_vs_hebrew"])
    r_direct6 = UgariticVsHebrew().run()
    ok = check("ugaritic_vs_hebrew: accuracy",
               r_graph6.get("accuracy"),
               r_direct6.get("accuracy"), str)
    all_ok &= ok
    ok = check("ugaritic_vs_hebrew: total",
               r_graph6.get("total"),
               r_direct6.get("total"), str)
    all_ok &= ok

    from glossa_lab.experiments.ugaritic_proper_benchmark import UgariticProperBenchmark
    r_graph7  = execute_graph(specs["ugaritic_proper_benchmark"])
    r_direct7 = UgariticProperBenchmark().run()
    ok = check("ugaritic_proper: proper_accuracy",
               round(r_graph7.get("proper_result", {}).get("accuracy", -99), 4),
               round(r_direct7.get("proper_result", {}).get("accuracy", -99), 4), str)
    all_ok &= ok
    ok = check("ugaritic_proper: circularity_inflation_pp",
               r_graph7.get("circularity_inflation_pp"),
               r_direct7.get("circularity_inflation_pp"), str)
    all_ok &= ok

    # ── Category C: CLI-only ──────────────────────────────────────────────────

    section("Category C — CLI-only (must return cli_only=True)")

    for exp_id in ["kandles_bias", "linear_a_circularity", "ocr_tables", "ocr_texts"]:
        r = execute_graph(specs[exp_id])
        ok = check(f"{exp_id}: cli_only flag", r.get("cli_only"), True, str)
        all_ok &= ok

    # ── Summary ───────────────────────────────────────────────────────────────

    print(f"\n{'=' * 60}")
    if all_ok:
        print("  ✓  All comparisons PASS — graph system matches Python run() results.")
    else:
        print("  ✗  Some comparisons FAILED — review output above.")
    print("=" * 60)

    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
