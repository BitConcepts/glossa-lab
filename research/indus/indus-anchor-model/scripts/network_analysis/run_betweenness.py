#!/usr/bin/env python3
"""
run_betweenness.py — Betweenness centrality for the Indus sign network
======================================================================
Builds a weighted directed graph from a bigram edge-list CSV, computes
betweenness centrality (weighted and unweighted), and ranks signs.

This analysis supports the structural claim (Tier 1) that a small set
of high-frequency grammatical signs act as network hubs bridging
professional-title formulas.

Usage
-----
    python run_betweenness.py \
        --bigrams-file ../../data/public/formula_bigram_table.csv \
        --hm-signs-file ../../data/public/anchor_table_161_HM.csv \
        --output-dir ../../outputs/

Requirements
------------
    - Python 3.10+
    - networkx (pip install networkx)

If networkx is not installed the script exits gracefully with a
descriptive error message.
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Dependency check
# ---------------------------------------------------------------------------
try:
    import networkx as nx  # type: ignore[import-untyped]
except ImportError:
    print(
        "ERROR: networkx is required but not installed.\n"
        "       Install it with:  pip install networkx\n"
        "       Then re-run this script.",
        file=sys.stderr,
    )
    sys.exit(2)


# ---------------------------------------------------------------------------
# Graph construction
# ---------------------------------------------------------------------------

def build_graph(bigrams_path: Path) -> nx.DiGraph:
    """
    Build a weighted directed graph from a bigram CSV.

    Expected columns: sign_a, sign_b, count
    Optional columns: pmi (used as an alternative weight)
    """
    G = nx.DiGraph()

    with open(bigrams_path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            src = row.get("sign_a", "").strip()
            tgt = row.get("sign_b", "").strip()
            if not src or not tgt:
                continue
            try:
                count = int(row.get("count", 1))
            except (ValueError, TypeError):
                count = 1
            try:
                pmi = float(row.get("pmi", 0.0))
            except (ValueError, TypeError):
                pmi = 0.0

            if G.has_edge(src, tgt):
                G[src][tgt]["weight"] += count
                G[src][tgt]["pmi"] = max(G[src][tgt].get("pmi", 0.0), pmi)
            else:
                G.add_edge(src, tgt, weight=count, pmi=pmi)

    return G


# ---------------------------------------------------------------------------
# H+M sign set
# ---------------------------------------------------------------------------

def load_hm_signs(hm_path: Optional[Path]) -> set[str]:
    """
    Load the set of HIGH+MEDIUM sign IDs.
    If the file is an anchor table with a Confidence column, filter by H/M.
    If it is a simple list (one sign per row), take all.
    Returns an empty set if the file is missing (non-fatal).
    """
    if hm_path is None or not hm_path.is_file():
        return set()

    signs: set[str] = set()
    with open(hm_path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        fieldnames = reader.fieldnames or []
        has_confidence = "Confidence" in fieldnames
        sign_col = "Sign" if "Sign" in fieldnames else (
            "sign" if "sign" in fieldnames else None
        )
        if sign_col is None:
            # Fallback: assume first column
            sign_col = fieldnames[0] if fieldnames else None

        for row in reader:
            if sign_col is None:
                break
            sid = row.get(sign_col, "").strip()
            if not sid:
                continue
            if has_confidence:
                conf = row.get("Confidence", "").strip().upper()
                if conf in {"HIGH", "MEDIUM"}:
                    signs.add(sid)
            else:
                signs.add(sid)

    return signs


# ---------------------------------------------------------------------------
# Dominant positional slot heuristic
# ---------------------------------------------------------------------------

def infer_dominant_slot(G: nx.DiGraph, node: str) -> str:
    """
    Heuristic to classify a node's dominant positional slot based on
    in-degree vs out-degree balance.

    - High out-degree, low in-degree → INITIAL (opens formulas)
    - High in-degree, low out-degree → TERMINAL (closes formulas)
    - Balanced → MEDIAL (bridge/hub)
    """
    in_w = sum(d.get("weight", 1) for _, _, d in G.in_edges(node, data=True))
    out_w = sum(d.get("weight", 1) for _, _, d in G.out_edges(node, data=True))
    total = in_w + out_w
    if total == 0:
        return "UNKNOWN"
    ratio = out_w / total  # proportion of outgoing
    if ratio > 0.65:
        return "INITIAL"
    elif ratio < 0.35:
        return "TERMINAL"
    else:
        return "MEDIAL"


# ---------------------------------------------------------------------------
# Main computation
# ---------------------------------------------------------------------------

def compute_betweenness(
    G: nx.DiGraph,
    hm_signs: set[str],
) -> List[Dict]:
    """
    Compute weighted and unweighted betweenness centrality.
    Returns a list of dicts sorted by weighted BC descending.
    """
    # Weighted BC: use inverse weight so that high-count edges are "short"
    # (betweenness uses shortest paths)
    weight_attr = "weight"
    bc_weighted = nx.betweenness_centrality(G, weight=weight_attr, normalized=True)
    bc_unweighted = nx.betweenness_centrality(G, weight=None, normalized=True)

    results = []
    for node in G.nodes():
        results.append({
            "sign": node,
            "bc_weighted": round(bc_weighted.get(node, 0.0), 6),
            "bc_unweighted": round(bc_unweighted.get(node, 0.0), 6),
            "in_hm_set": node in hm_signs if hm_signs else "",
            "dominant_slot": infer_dominant_slot(G, node),
        })

    # Sort by weighted BC descending
    results.sort(key=lambda r: r["bc_weighted"], reverse=True)

    # Add rank
    for i, r in enumerate(results, 1):
        r["rank"] = i

    return results


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def write_results(results: List[Dict], output_dir: Path) -> Path:
    """Write bc_rankings.csv to the output directory."""
    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / "bc_rankings.csv"

    fieldnames = ["sign", "bc_weighted", "bc_unweighted", "rank",
                  "dominant_slot", "in_hm_set"]

    with open(out_path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow({k: row[k] for k in fieldnames})

    return out_path


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Compute betweenness centrality for the Indus sign bigram network"
    )
    parser.add_argument(
        "--bigrams-file",
        type=Path,
        required=True,
        help="Path to bigram CSV (e.g. formula_bigram_table.csv). "
             "Required columns: sign_a, sign_b, count",
    )
    parser.add_argument(
        "--hm-signs-file",
        type=Path,
        default=None,
        help="Path to H+M anchor CSV (optional). Used to flag which ranked "
             "signs are in the HIGH+MEDIUM anchor set.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parent.parent.parent / "outputs",
        help="Output directory (default: ../../outputs/)",
    )
    args = parser.parse_args(argv)

    bigrams_path: Path = args.bigrams_file.resolve()
    output_dir: Path = args.output_dir.resolve()

    if not bigrams_path.is_file():
        print(f"ERROR: Bigram file not found: {bigrams_path}", file=sys.stderr)
        return 1

    print(f"Building graph from: {bigrams_path}")
    G = build_graph(bigrams_path)
    print(f"  Nodes: {G.number_of_nodes()}  Edges: {G.number_of_edges()}")

    hm_signs = load_hm_signs(args.hm_signs_file)
    if hm_signs:
        print(f"  H+M signs loaded: {len(hm_signs)}")
    else:
        print("  No H+M signs file provided (in_hm_set column will be empty)")

    print("Computing betweenness centrality …")
    results = compute_betweenness(G, hm_signs)

    out_path = write_results(results, output_dir)
    print(f"\nOutput: {out_path}")

    # Print top 10
    print("\nTop 10 by weighted betweenness centrality:")
    print(f"  {'Rank':<6} {'Sign':<8} {'BC(w)':<12} {'BC(u)':<12} {'Slot':<10}")
    print(f"  {'-'*6} {'-'*8} {'-'*12} {'-'*12} {'-'*10}")
    for r in results[:10]:
        print(
            f"  {r['rank']:<6} {r['sign']:<8} "
            f"{r['bc_weighted']:<12.6f} {r['bc_unweighted']:<12.6f} "
            f"{r['dominant_slot']:<10}"
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
