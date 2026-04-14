"""Sign co-occurrence network pipeline.

Builds a graph where signs are nodes and edges represent co-occurrence
frequency. Applies a simple community detection algorithm (greedy
modularity) to identify functional sign groups.

This reveals sign communities that may correspond to:
  - Numeral clusters
  - Name/title components
  - Grammatical markers
  - Semantic domains
"""

from __future__ import annotations

import logging
from collections import Counter, defaultdict
from typing import Any

from glossa_lab.database import get_db
from glossa_lab.engine import register_pipeline

_log = logging.getLogger("glossa_lab.pipelines.cooccurrence")

# GPU/numpy detection (H10.1)
try:
    import numpy as _np
    _HAS_NUMPY = True
except ImportError:
    _HAS_NUMPY = False


def build_cooccurrence_network(
    symbols: list[str],
    window: int = 2,
    min_freq: int = 2,
    min_edge_weight: int = 2,
    top_n_nodes: int = 80,
) -> dict[str, Any]:
    """Build a co-occurrence network from a symbol sequence.

    Args:
        symbols: flat list of symbols.
        window: co-occurrence window size (default 2 = bigrams).
        min_freq: minimum symbol frequency to include as node.
        min_edge_weight: minimum co-occurrence count for an edge.
        top_n_nodes: maximum number of nodes to include.
    """
    freq: Counter[str] = Counter(symbols)

    # Select top nodes
    nodes = [s for s, _ in freq.most_common() if freq[s] >= min_freq]
    nodes = nodes[:top_n_nodes]
    node_set = set(nodes)

    # Count co-occurrences within window
    # Numpy fast path: encode symbols as integers then use vectorized diff (H10.1)
    edges: Counter[tuple[str, str]] = Counter()
    if _HAS_NUMPY and len(symbols) > 500:
        idx_map = {s: i for i, s in enumerate(nodes)}
        encoded = _np.array([idx_map.get(s, -1) for s in symbols], dtype=_np.int32)
        valid   = encoded >= 0
        pos     = _np.where(valid)[0]
        for k in range(1, window + 1):
            left_pos  = pos[pos + k < len(symbols)]
            right_pos = left_pos + k
            right_valid = encoded[right_pos] >= 0
            lp = left_pos[right_valid]
            rp = right_pos[right_valid]
            for li, ri in zip(encoded[lp].tolist(), encoded[rp].tolist()):
                a, b = (nodes[min(li, ri)], nodes[max(li, ri)])
                edges[(a, b)] += 1
    else:
        for i in range(len(symbols)):
            if symbols[i] not in node_set:
                continue
            for j in range(i + 1, min(i + window + 1, len(symbols))):
                if symbols[j] not in node_set:
                    continue
                pair = tuple(sorted([symbols[i], symbols[j]]))
                edges[pair] += 1  # type: ignore[arg-type]

    # Filter edges
    edge_list = [
        {"source": a, "target": b, "weight": w}
        for (a, b), w in edges.most_common()
        if w >= min_edge_weight
    ]

    # Build adjacency for community detection
    adj: dict[str, dict[str, int]] = defaultdict(dict)
    for e in edge_list:
        adj[e["source"]][e["target"]] = e["weight"]
        adj[e["target"]][e["source"]] = e["weight"]

    # Simple community detection: label propagation
    communities = _label_propagation(nodes, adj)

    # Compute node metrics
    node_list = []
    for n in nodes:
        degree = len(adj.get(n, {}))
        strength = sum(adj.get(n, {}).values())
        node_list.append(
            {
                "sign": n,
                "frequency": freq[n],
                "degree": degree,
                "strength": strength,
                "community": communities.get(n, -1),
            }
        )

    # Group by community
    comm_groups: dict[int, list[str]] = defaultdict(list)
    for n in node_list:
        comm_groups[n["community"]].append(n["sign"])

    community_list = [
        {"community_id": cid, "signs": signs, "size": len(signs)}
        for cid, signs in sorted(comm_groups.items())
    ]
    community_list.sort(key=lambda c: c["size"], reverse=True)

    return {
        "node_count": len(nodes),
        "edge_count": len(edge_list),
        "community_count": len(community_list),
        "nodes": node_list,
        "edges": edge_list[:200],  # Top 200 edges
        "communities": community_list,
    }


def _label_propagation(
    nodes: list[str],
    adj: dict[str, dict[str, int]],
    max_iter: int = 20,
) -> dict[str, int]:
    """Simple label propagation community detection.

    Each node starts with its own label. Iteratively, each node
    adopts the most frequent label among its weighted neighbors.
    """
    labels: dict[str, int] = {n: i for i, n in enumerate(nodes)}

    for _ in range(max_iter):
        changed = False
        for node in nodes:
            if node not in adj or not adj[node]:
                continue
            # Count weighted labels of neighbors
            label_weights: Counter[int] = Counter()
            for neighbor, weight in adj[node].items():
                label_weights[labels.get(neighbor, -1)] += weight

            if label_weights:
                best_label = label_weights.most_common(1)[0][0]
                if best_label != labels[node]:
                    labels[node] = best_label
                    changed = True

        if not changed:
            break

    # Renumber communities from 0
    unique_labels = sorted(set(labels.values()))
    remap = {old: new for new, old in enumerate(unique_labels)}
    return {node: remap[lbl] for node, lbl in labels.items()}


@register_pipeline("cooccurrence")
async def run_cooccurrence(params: dict[str, Any]) -> dict[str, Any]:
    """Pipeline entry point. Params: {text_id, window, min_freq, top_n_nodes}.

    Uses numpy-vectorized co-occurrence counting for corpora >500 tokens (H10.1).
    """
    try:
        from glossa_lab.experiments._parallel import compute_device_label  # noqa: PLC0415
        _log.info("cooccurrence device: %s", compute_device_label())
    except Exception:  # noqa: BLE001
        pass
    text_id = params.get("text_id")
    if not text_id:
        raise ValueError("Missing required param: text_id")

    db = get_db()
    if db is None:
        raise RuntimeError("Database not available")

    text = await db.get_text(text_id)
    if text is None:
        raise ValueError(f"Text not found: {text_id}")

    symbols = text["content"]

    result = build_cooccurrence_network(
        symbols,
        window=params.get("window", 2),
        min_freq=params.get("min_freq", 2),
        min_edge_weight=params.get("min_edge_weight", 2),
        top_n_nodes=params.get("top_n_nodes", 80),
    )
    result["text_id"] = text_id
    result["text_name"] = text["name"]
    return result
