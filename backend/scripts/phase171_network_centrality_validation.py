"""Phase 171 — Network Centrality Validation (Roif × Pierson)

Independent validation of Avishai Roif's betweenness centrality claim:
that MEDIAL signs M099 and M267 function as structural bridge nodes in
the IVS co-occurrence network, with markedly higher betweenness than
flanking INITIAL/TERMINAL cluster signs.

Three analyses:
  A. Betweenness centrality on Roif's 22-node graph (his edge data)
  B. Betweenness centrality on our independent graph (phase142 bigrams,
     same 22 nodes, PMI > 1.5, n_seals >= 15)
  C. Edge cross-validation: Roif edges vs our phase142 ground truth
  D. Peripheral-sites proxy: KL divergence (phase151) as a proxy for
     network peripherality, framing the testable prediction for ICIT

Run:
    python backend/scripts/phase171_network_centrality_validation.py

Output:
    outputs/phase171_network_centrality_validation.json
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import networkx as nx

REPO_ROOT = Path(__file__).resolve().parents[2]
OUTPUTS   = REPO_ROOT / "outputs"
REPORTS   = REPO_ROOT / "research" / "indus" / "phase_reports"
OUTPUTS.mkdir(exist_ok=True)

# ── Roif's 22-node graph (extracted from ivs_sign_network.html) ─────────────

ROIF_NODES = [
    # (id, reading, confidence, slot, corpus_freq)
    ("M211", "kol",       "HIGH",   "initial",   180),
    ("M045", "yānai",     "HIGH",   "initial",   210),
    ("M062", "erutu",     "HIGH",   "initial",   165),
    ("M073", "kōṉ",       "HIGH",   "initial",   140),
    ("M060", "kāṇṭā",     "HIGH",   "initial",    95),
    ("M072", "mā",        "MEDIUM", "initial",    55),
    ("M261", "muruku",    "HIGH",   "initial",   110),
    ("M099", "kol/koḷ",   "HIGH",   "medial",    280),
    ("M233", "ūr",        "MEDIUM", "medial",    190),
    ("M162", "il/iḷ",     "HIGH",   "medial",    145),
    ("M264", "peN",       "HIGH",   "medial",    120),
    ("M328", "āl",        "HIGH",   "medial",    130),
    ("M149", "or",        "MEDIUM", "medial",     75),
    ("M185", "pul",       "MEDIUM", "medial",     65),
    ("M267", "iN/in",     "MEDIUM", "medial",    400),
    ("M374", "kul",       "MEDIUM", "medial",     50),  # Munda substrate
    ("M351", "vī",        "MEDIUM", "medial",     40),  # Munda substrate
    ("M047", "mīn",       "HIGH",   "medial",     13),
    ("M342", "ay/ā",      "HIGH",   "terminal",  584),
    ("M176", "an/aṇ",     "HIGH",   "terminal",  356),
    ("M367", "am",        "HIGH",   "terminal",  220),
    ("M336", "iṉ",        "HIGH",   "terminal",  175),
]

ROIF_EDGES = [
    # (source, target, n_seals, pmi_roif)
    ("M211", "M099",  84, 2.10), ("M211", "M342", 102, 2.30), ("M211", "M176",  78, 2.00),
    ("M045", "M099",  65, 1.90), ("M045", "M328",  55, 2.20), ("M045", "M342",  70, 1.80),
    ("M062", "M342",  88, 2.40), ("M062", "M176",  72, 2.10),
    ("M073", "M149",  30, 1.70), ("M073", "M162",  45, 1.90), ("M073", "M342",  55, 1.80),
    ("M060", "M099",  28, 1.60), ("M060", "M342",  33, 1.70),
    ("M072", "M264",  20, 1.70), ("M072", "M342",  18, 1.60),
    ("M261", "M099",  35, 1.80), ("M261", "M342",  42, 1.90),
    ("M099", "M342",  81, 2.30), ("M099", "M176",  74, 2.10), ("M099", "M267",  84, 2.30),
    ("M233", "M342",  48, 1.90), ("M233", "M176",  32, 1.70),
    ("M162", "M342",  40, 1.80),
    ("M267", "M099",  84, 2.30), ("M267", "M342",  60, 1.90),
    ("M328", "M342",  44, 1.80), ("M264", "M342",  38, 1.80),
    ("M176", "M099",  74, 2.10), ("M342", "M176", 122, 2.43),
    ("M185", "M328",  22, 1.60), ("M185", "M342",  19, 1.50),
    ("M374", "M099",  18, 1.60), ("M374", "M342",  16, 1.50),
    ("M047", "M267",  15, 1.70), ("M047", "M342",  18, 1.80),
]

# ── Phase142 ground-truth bigrams (top-30 H+M pairs) ───────────────────────

def load_phase142() -> list[dict]:
    path = REPORTS / "phase142_collocate_network.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    return data["results"]["A_collocate_network"]["top_30_hm_bigrams"]

# ── Graph construction helpers ───────────────────────────────────────────────

ROIF_IDS = {n[0] for n in ROIF_NODES}

def build_roif_graph() -> nx.DiGraph:
    G = nx.DiGraph()
    for nid, reading, conf, slot, freq in ROIF_NODES:
        G.add_node(nid, reading=reading, conf=conf, slot=slot, freq=freq)
    for src, tgt, seals, pmi in ROIF_EDGES:
        G.add_edge(src, tgt, seals=seals, pmi=pmi, weight=pmi)
    return G

def build_our_graph(bigrams: list[dict], pmi_threshold: float = 1.5,
                    seals_threshold: int = 15) -> nx.DiGraph:
    """Build directed graph from phase142 top-30 bigrams, restricted to
    nodes that appear in Roif's 22-node set (for fair comparison)."""
    G = nx.DiGraph()
    node_meta = {n[0]: n for n in ROIF_NODES}
    for n in ROIF_NODES:
        G.add_node(n[0], reading=n[1], conf=n[2], slot=n[3], freq=n[4])

    for b in bigrams:
        pair  = b["pair"]
        parts = pair.split("·")
        if len(parts) != 2:
            continue
        src, tgt = parts[0].strip(), parts[1].strip()
        count = b["count"]
        pmi   = b["pmi"]
        if src not in ROIF_IDS or tgt not in ROIF_IDS:
            continue
        if pmi < pmi_threshold or count < seals_threshold:
            continue
        G.add_edge(src, tgt, seals=count, pmi=pmi, weight=pmi)
    return G

# ── Betweenness centrality ───────────────────────────────────────────────────

def centrality_table(G: nx.DiGraph) -> list[dict]:
    bc = nx.betweenness_centrality(G, normalized=True, weight="weight")
    bc_uw = nx.betweenness_centrality(G, normalized=True)
    out = []
    for nid, _, _, slot, freq in ROIF_NODES:
        if nid not in G:
            continue
        meta = dict(G.nodes[nid])
        out.append({
            "sign":         nid,
            "reading":      meta.get("reading", "?"),
            "slot":         slot,
            "freq":         freq,
            "betweenness_w":   round(bc.get(nid, 0.0), 4),
            "betweenness_uw":  round(bc_uw.get(nid, 0.0), 4),
        })
    return sorted(out, key=lambda x: -x["betweenness_w"])

# ── Edge cross-validation ────────────────────────────────────────────────────

def cross_validate(bigrams: list[dict]) -> list[dict]:
    our_index = {}
    for b in bigrams:
        parts = b["pair"].split("·")
        if len(parts) == 2:
            key = (parts[0].strip(), parts[1].strip())
            our_index[key] = b

    results = []
    for src, tgt, roif_seals, roif_pmi in ROIF_EDGES:
        key    = (src, tgt)
        our    = our_index.get(key)
        status = "NOT_IN_TOP30"
        our_seals, our_pmi, pmi_delta = None, None, None
        if our:
            our_seals = our["count"]
            our_pmi   = our["pmi"]
            pmi_delta = round(abs(roif_pmi - our_pmi), 3)
            if pmi_delta < 0.1:
                status = "MATCH"
            elif pmi_delta < 0.5:
                status = "MINOR_DISCREPANCY"
            else:
                status = "SIGNIFICANT_DISCREPANCY"
            if roif_seals != our_seals:
                status = status.replace("MATCH", "SEALS_MISMATCH")
        results.append({
            "edge":       f"{src}→{tgt}",
            "roif_seals": roif_seals,
            "our_seals":  our_seals,
            "roif_pmi":   roif_pmi,
            "our_pmi":    our_pmi,
            "pmi_delta":  pmi_delta,
            "status":     status,
        })
    return results

# ── Peripheral-sites proxy (phase151 KL as peripherality metric) ─────────────

def peripheral_sites_proxy() -> dict:
    """
    Roif predicts: peripheral sites in the Harappan trade network should show
    higher relative betweenness for MEDIAL bridge nodes (M099, M267) vs
    INITIAL classifier nodes.

    We cannot directly test this without per-site bigram networks (the Holdat
    corpus is not accessible for site-stratified analysis). However, phase151
    provides KL divergence for all 36 site pairs as a proxy for peripherality:
    higher KL from the primary centers (Mohenjo-daro, Harappa) ≈ more peripheral.

    Peripherality ranking (KL from Mohenjo-daro, descending):
      Rakhigarhi: 0.509 (most peripheral, n=33)
      Surkotada:  0.255 (n=61)
      Chanhu-daro: 0.253 (n=78)
      Banawali:   0.255 (n=60)
      Dholavira:  0.158 (n=106)
      Lothal:     0.144 (coastal gateway, n=124)
      Kalibangan: 0.168 (n=110)
      Harappa:    0.070 (primary center, n=492)

    The prediction is directional: as KL from Mohenjo-daro increases,
    the relative frequency of MEDIAL bridge signs (M099, M267) in
    compound positions should increase relative to INITIAL classifier signs.

    VERDICT: TESTABLE WITH ICIT.
    Rakhigarhi (n=33 in Holdat) has insufficient tokens for reliable
    per-site betweenness. ICIT (5,318 inscriptions) would provide the
    sample sizes needed at peripheral sites.
    """
    return {
        "prediction": (
            "Peripheral Harappan sites (high KL from Mohenjo-daro) should show "
            "higher relative betweenness for M099/M267 vs INITIAL classifier nodes, "
            "consistent with protocol-based authority encoding at the network frontier "
            "(Roif, under review)."
        ),
        "peripherality_proxy_kl_from_mohenjo_daro": {
            "Rakhigarhi":  {"kl": 0.509, "n_seals": 33,  "peripherality": "HIGHEST"},
            "Surkotada":   {"kl": 0.255, "n_seals": 61,  "peripherality": "HIGH"},
            "Banawali":    {"kl": 0.255, "n_seals": 60,  "peripherality": "HIGH"},
            "Chanhu-daro": {"kl": 0.253, "n_seals": 78,  "peripherality": "HIGH"},
            "Kalibangan":  {"kl": 0.168, "n_seals": 110, "peripherality": "MEDIUM"},
            "Dholavira":   {"kl": 0.158, "n_seals": 106, "peripherality": "MEDIUM"},
            "Lothal":      {"kl": 0.144, "n_seals": 124, "peripherality": "MEDIUM",
                            "note": "Coastal gateway — different peripherality type"},
            "Harappa":     {"kl": 0.070, "n_seals": 492, "peripherality": "PRIMARY_CENTER"},
        },
        "testability": "REQUIRES_ICIT",
        "note": (
            "Rakhigarhi has n=33 seals in Holdat — insufficient for per-site bigram "
            "network analysis. ICIT corpus (5,318 inscriptions) is required. "
            "This is the primary empirical target for v3 of the paper."
        ),
        "intermediate_test_available": (
            "Compare M099/M267 compound frequency at Rakhigarhi vs Mohenjo-daro "
            "in the Holdat corpus as a weak proxy. Low statistical power (n=33) "
            "but directionally informative."
        ),
    }

# ── Main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    print("Phase 171 — Network Centrality Validation")
    print("=" * 50)

    bigrams = load_phase142()
    print(f"Loaded {len(bigrams)} phase142 bigrams")

    # A. Roif graph
    G_roif = build_roif_graph()
    ct_roif = centrality_table(G_roif)
    print(f"\n[A] Roif graph: {G_roif.number_of_nodes()} nodes, "
          f"{G_roif.number_of_edges()} edges")
    print("  Top-10 by betweenness (weighted):")
    for row in ct_roif[:10]:
        marker = " ◀ BRIDGE" if row["sign"] in ("M099", "M267") else ""
        print(f"    {row['sign']:5s} ({row['slot']:8s}) "
              f"BC={row['betweenness_w']:.4f}{marker}")

    # B. Our graph
    G_ours = build_our_graph(bigrams)
    ct_ours = centrality_table(G_ours)
    print(f"\n[B] Our graph (phase142, PMI>1.5, seals>=15): "
          f"{G_ours.number_of_nodes()} nodes, {G_ours.number_of_edges()} edges")
    print("  Top-10 by betweenness (weighted):")
    for row in ct_ours[:10]:
        marker = " ◀ BRIDGE" if row["sign"] in ("M099", "M267") else ""
        print(f"    {row['sign']:5s} ({row['slot']:8s}) "
              f"BC={row['betweenness_w']:.4f}{marker}")

    # C. Cross-validate edges
    xv = cross_validate(bigrams)
    matches     = [r for r in xv if r["status"] == "MATCH"]
    not_in_top  = [r for r in xv if r["status"] == "NOT_IN_TOP30"]
    discrepant  = [r for r in xv if "DISCREPANCY" in r["status"] or "MISMATCH" in r["status"]]
    print(f"\n[C] Edge cross-validation ({len(xv)} Roif edges):")
    print(f"    Confirmed match:      {len(matches)}")
    print(f"    Not in top-30 window: {len(not_in_top)}  (may still be valid, below top-30)")
    print(f"    PMI/count discrepancy:{len(discrepant)}")
    for r in discrepant:
        print(f"    ! {r['edge']}: Roif PMI={r['roif_pmi']} vs ours={r['our_pmi']} "
              f"(Δ={r['pmi_delta']}) seals Roif={r['roif_seals']} ours={r['our_seals']}")

    # Verdict on M099 and M267
    roif_ranks = {row["sign"]: i + 1 for i, row in enumerate(ct_roif)}
    our_ranks  = {row["sign"]: i + 1 for i, row in enumerate(ct_ours)}
    print("\n[VERDICT] Bridge node ranking:")
    for sign in ("M099", "M267"):
        print(f"  {sign}: rank {roif_ranks.get(sign,'—')} (Roif graph) | "
              f"rank {our_ranks.get(sign,'—')} (our graph)")

    m099_confirmed = our_ranks.get("M099", 99) <= 5
    m267_confirmed = our_ranks.get("M267", 99) <= 5
    bridge_claim = "CONFIRMED" if (m099_confirmed and m267_confirmed) else \
                   "PARTIAL"   if (m099_confirmed or m267_confirmed) else \
                   "NOT_CONFIRMED"
    print(f"  Bridge-node claim: {bridge_claim}")

    # D. Peripheral sites
    proxy = peripheral_sites_proxy()

    # ── Assemble output ──────────────────────────────────────────────────────
    report = {
        "phase":  171,
        "date":   "2026-05-21",
        "title":  "Network Centrality Validation — Roif × Pierson (2026)",
        "description": (
            "Independent validation of Roif's betweenness centrality claim: "
            "that MEDIAL signs M099 and M267 are structural bridge nodes in "
            "the IVS co-occurrence network. Three-way analysis: Roif graph, "
            "our independent graph, edge cross-validation, and peripheral-sites "
            "proxy for the ICIT-testable prediction."
        ),
        "A_roif_graph": {
            "n_nodes": G_roif.number_of_nodes(),
            "n_edges": G_roif.number_of_edges(),
            "centrality_ranked": ct_roif,
            "M099_rank": roif_ranks.get("M099"),
            "M267_rank": roif_ranks.get("M267"),
        },
        "B_our_graph": {
            "n_nodes": G_ours.number_of_nodes(),
            "n_edges": G_ours.number_of_edges(),
            "pmi_threshold": 1.5,
            "seals_threshold": 15,
            "centrality_ranked": ct_ours,
            "M099_rank": our_ranks.get("M099"),
            "M267_rank": our_ranks.get("M267"),
        },
        "C_edge_cross_validation": {
            "total_roif_edges": len(xv),
            "confirmed_match": len(matches),
            "not_in_top30_window": len(not_in_top),
            "discrepancies": discrepant,
            "note": (
                "Edges not in top-30 window are valid; phase142 only stores top 30. "
                "Discrepancies likely reflect different PMI formulas or corpus tokenisation."
            ),
        },
        "D_peripheral_sites_proxy": proxy,
        "verdict": {
            "bridge_node_claim": bridge_claim,
            "M099_bridge_confirmed": m099_confirmed,
            "M267_bridge_confirmed": m267_confirmed,
            "summary": (
                f"Roif's claim that M099 and M267 are top-5 betweenness bridge nodes "
                f"is {bridge_claim} by independent computation on our phase142 bigram data. "
                f"M099 rank: {our_ranks.get('M099','—')}. M267 rank: {our_ranks.get('M267','—')}. "
                f"The peripheral-sites prediction requires ICIT corpus to test properly."
            ),
        },
    }

    out_path = OUTPUTS / "phase171_network_centrality_validation.json"
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nReport written to: {out_path.relative_to(REPO_ROOT)}")

    # ── Copy to phase_reports ────────────────────────────────────────────────
    pr_path = REPORTS / "phase171_network_centrality_validation.json"
    pr_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Phase report:      {pr_path.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
