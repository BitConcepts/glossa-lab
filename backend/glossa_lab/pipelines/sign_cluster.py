"""Distributional sign clustering pipeline.

Implements the computational equivalent of Alice Kober's method:
signs that appear in similar distributional contexts (same neighbors,
same positions) likely belong to the same functional category.

For each sign, builds a context vector encoding:
  - What signs appear immediately before it (left context)
  - What signs appear immediately after it (right context)
  - Positional preferences (initial/medial/terminal)

Then clusters signs by cosine similarity of their context vectors.
"""

from __future__ import annotations

import math
from collections import Counter, defaultdict
from typing import Any

from glossa_lab.database import get_db
from glossa_lab.engine import register_pipeline


def _cosine_sim(a: dict[str, float], b: dict[str, float]) -> float:
    """Cosine similarity between two sparse vectors (dicts)."""
    keys = set(a) | set(b)
    dot = sum(a.get(k, 0) * b.get(k, 0) for k in keys)
    mag_a = math.sqrt(sum(v * v for v in a.values()))
    mag_b = math.sqrt(sum(v * v for v in b.values()))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)


def compute_sign_clusters(
    inscriptions: list[list[str]],
    min_freq: int = 3,
    top_n: int = 50,
) -> dict[str, Any]:
    """Cluster signs by distributional similarity.

    Args:
        inscriptions: list of inscriptions, each a list of sign IDs.
        min_freq: minimum total frequency to include a sign.
        top_n: number of top signs to cluster.

    Returns dict with context vectors, similarity matrix, and clusters.
    """
    # Count frequencies and build context vectors
    freq: Counter[str] = Counter()
    left_ctx: dict[str, Counter[str]] = defaultdict(Counter)
    right_ctx: dict[str, Counter[str]] = defaultdict(Counter)
    pos_ctx: dict[str, Counter[str]] = defaultdict(Counter)

    for insc in inscriptions:
        for i, sign in enumerate(insc):
            freq[sign] += 1
            if i > 0:
                left_ctx[sign][insc[i - 1]] += 1
            if i < len(insc) - 1:
                right_ctx[sign][insc[i + 1]] += 1
            # Position features
            if i == 0:
                pos_ctx[sign]["POS_INITIAL"] += 1
            if i == len(insc) - 1:
                pos_ctx[sign]["POS_TERMINAL"] += 1
            if 0 < i < len(insc) - 1:
                pos_ctx[sign]["POS_MEDIAL"] += 1

    # Select top signs by frequency
    eligible = [s for s, c in freq.most_common() if c >= min_freq][:top_n]

    if not eligible:
        return {
            "total_signs": sum(freq.values()),
            "unique_signs": len(freq),
            "clustered_signs": 0,
            "signs": [],
            "similarity_pairs": [],
            "clusters": [],
        }

    # Build combined context vectors
    vectors: dict[str, dict[str, float]] = {}
    for sign in eligible:
        vec: dict[str, float] = {}
        total = freq[sign]
        for ctx_sign, cnt in left_ctx[sign].items():
            vec[f"L_{ctx_sign}"] = cnt / total
        for ctx_sign, cnt in right_ctx[sign].items():
            vec[f"R_{ctx_sign}"] = cnt / total
        for pos_key, cnt in pos_ctx[sign].items():
            vec[pos_key] = cnt / total
        vectors[sign] = vec

    # Compute pairwise similarities
    sim_pairs = []
    for i, s1 in enumerate(eligible):
        for s2 in eligible[i + 1:]:
            sim = _cosine_sim(vectors[s1], vectors[s2])
            if sim > 0.1:  # Only store meaningful similarities
                sim_pairs.append({
                    "sign_a": s1, "sign_b": s2,
                    "similarity": round(sim, 4),
                })

    sim_pairs.sort(key=lambda x: x["similarity"], reverse=True)

    # Simple greedy clustering: merge most similar pairs
    clusters: list[set[str]] = []
    assigned: set[str] = set()

    for pair in sim_pairs:
        if pair["similarity"] < 0.3:
            break
        a, b = pair["sign_a"], pair["sign_b"]

        # Find existing cluster for a or b
        cluster_a = next((c for c in clusters if a in c), None)
        cluster_b = next((c for c in clusters if b in c), None)

        if cluster_a and cluster_b:
            if cluster_a is not cluster_b:
                cluster_a.update(cluster_b)
                clusters.remove(cluster_b)
        elif cluster_a:
            cluster_a.add(b)
        elif cluster_b:
            cluster_b.add(a)
        else:
            clusters.append({a, b})
        assigned.add(a)
        assigned.add(b)

    # Add singletons (unclustered signs)
    for sign in eligible:
        if sign not in assigned:
            clusters.append({sign})

    cluster_list = [
        {"cluster_id": i, "signs": sorted(c), "size": len(c)}
        for i, c in enumerate(clusters)
    ]
    cluster_list.sort(key=lambda x: x["size"], reverse=True)

    return {
        "total_signs": sum(freq.values()),
        "unique_signs": len(freq),
        "clustered_signs": len(eligible),
        "signs": [
            {"sign": s, "frequency": freq[s],
             "left_context_size": len(left_ctx[s]),
             "right_context_size": len(right_ctx[s])}
            for s in eligible
        ],
        "similarity_pairs": sim_pairs[:100],  # Top 100
        "clusters": cluster_list,
    }


@register_pipeline("sign_cluster")
async def run_sign_cluster(params: dict[str, Any]) -> dict[str, Any]:
    """Pipeline entry point. Params: {text_id, min_freq, top_n}."""
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
    # Treat as one long inscription for context analysis
    inscriptions = [symbols]

    result = compute_sign_clusters(
        inscriptions,
        min_freq=params.get("min_freq", 3),
        top_n=params.get("top_n", 50),
    )
    result["text_id"] = text_id
    result["text_name"] = text["name"]
    return result
