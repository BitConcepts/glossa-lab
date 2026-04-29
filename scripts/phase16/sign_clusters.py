"""Phase-16 sign clustering: Daggumati & Revesz 2021 allograph detection on M77,
plus loader for the Kee2u Segmentation_tree, plus pairwise agreement matrix.

Daggumati & Revesz 2021 method (simplified):
    Two signs s1, s2 are candidate allographs if BOTH:
        (a) Their position distributions {initial, medial, final, standalone}
            have low Jensen-Shannon divergence (< THR_POS).
        (b) Their bigram-context vectors (concatenation of normalized predecessor
            and successor distributions over a shared sign vocabulary) have
            cosine similarity >= THR_CTX.
    We cluster candidate-allograph pairs by transitive closure (connected
    components of the similarity graph) to produce sign groups.

Outputs:
    reports/phase16_sign_clusters.json
        - daggumati_clusters: list of clusters from M77
        - kee2u_clusters: list of clusters extracted from the Kee2u dendrogram
                          (cut at distance threshold)
        - phase15_anchor_groups: legacy comparison if anchor-merge groups can
                                 be loaded from existing reports
        - pairwise_agreement: Jaccard / overlap statistics

Run:
    py scripts/phase16/sign_clusters.py
"""
from __future__ import annotations

import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
M77_PATH = ROOT / "reports" / "mahadevan_corpus_flat.txt"
KEE2U_TREE = ROOT / "corpora" / "downloads" / "external_repos" / "Kee2u_Indus_Decipherment" / "Statistical_Analysis" / "Segmentation_tree.json"
OUT_PATH = ROOT / "reports" / "phase16_sign_clusters.json"

# Daggumati thresholds. M77 is small (1669 inscriptions / 5361 signs / 64
# distinct signs after the project's rank-corr mapping) so we use
# moderately permissive thresholds. With the strict (0.10, 0.80) values used
# in Daggumati & Revesz 2021 on the larger ICIT corpus, no allograph
# candidates survive on M77; the loosened (0.25, 0.55) values surface
# distributional cousins that are good starting points for hand review.
THR_POS_JS = 0.25
THR_CTX_COS = 0.55
MIN_OCCURRENCE = 5
KEE2U_CUT_DISTANCE = 1.5


# ---------------------------------------------------------------------------
# JS divergence + cosine
# ---------------------------------------------------------------------------

def js_distance(p: list[float], q: list[float]) -> float:
    """sqrt of Jensen-Shannon divergence (a metric in [0, 1] for log2)."""
    assert len(p) == len(q)
    s = sum(p)
    if s > 0: p = [x / s for x in p]
    s = sum(q)
    if s > 0: q = [x / s for x in q]
    m = [(pi + qi) / 2 for pi, qi in zip(p, q)]
    def kl(a, b):
        out = 0.0
        for ai, bi in zip(a, b):
            if ai > 0 and bi > 0:
                out += ai * math.log2(ai / bi)
        return out
    js = 0.5 * kl(p, m) + 0.5 * kl(q, m)
    return math.sqrt(max(0.0, js))


def cosine(a: dict[str, float], b: dict[str, float]) -> float:
    keys = set(a) | set(b)
    dot = sum(a.get(k, 0.0) * b.get(k, 0.0) for k in keys)
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


# ---------------------------------------------------------------------------
# Daggumati position + context features on M77
# ---------------------------------------------------------------------------

def compute_features(inscriptions: list[list[str]]) -> dict[str, dict]:
    """Return per-sign {pos: [init, med, final, alone], pred: dict, succ: dict, count: int}."""
    feats: dict[str, dict] = defaultdict(
        lambda: {"pos": [0, 0, 0, 0], "pred": Counter(), "succ": Counter(), "count": 0}
    )
    for ins in inscriptions:
        n = len(ins)
        for i, sign in enumerate(ins):
            f = feats[sign]
            f["count"] += 1
            if n == 1:
                f["pos"][3] += 1  # standalone
            elif i == 0:
                f["pos"][0] += 1
            elif i == n - 1:
                f["pos"][2] += 1
            else:
                f["pos"][1] += 1
            if i > 0:
                f["pred"][ins[i - 1]] += 1
            if i < n - 1:
                f["succ"][ins[i + 1]] += 1
    # Normalize
    out = {}
    for sign, f in feats.items():
        total = max(1, f["count"])
        pos = [c / total for c in f["pos"]]
        pred_total = max(1, sum(f["pred"].values()))
        succ_total = max(1, sum(f["succ"].values()))
        pred = {k: v / pred_total for k, v in f["pred"].items()}
        succ = {k: v / succ_total for k, v in f["succ"].items()}
        # Combined context: predecessor with prefix + successor with prefix
        ctx = {}
        for k, v in pred.items():
            ctx[f"P:{k}"] = v
        for k, v in succ.items():
            ctx[f"S:{k}"] = v
        out[sign] = {"count": f["count"], "pos": pos, "ctx": ctx}
    return out


def daggumati_clusters(features: dict[str, dict]) -> list[dict]:
    """Return list of clusters (each = list of signs) detected as allograph
    candidates by Daggumati & Revesz 2021 criteria on M77 features."""
    eligible = [s for s, f in features.items() if f["count"] >= MIN_OCCURRENCE]
    eligible.sort()
    print(f"  {len(eligible)} signs with count >= {MIN_OCCURRENCE}", file=sys.stderr)

    edges = []
    for i in range(len(eligible)):
        for j in range(i + 1, len(eligible)):
            s1, s2 = eligible[i], eligible[j]
            f1, f2 = features[s1], features[s2]
            jsd = js_distance(f1["pos"], f2["pos"])
            cos = cosine(f1["ctx"], f2["ctx"])
            if jsd <= THR_POS_JS and cos >= THR_CTX_COS:
                edges.append((s1, s2, jsd, cos))

    # Connected components
    parent: dict[str, str] = {s: s for s in eligible}
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
    for a, b, _, _ in edges:
        union(a, b)
    groups: dict[str, list[str]] = defaultdict(list)
    for s in eligible:
        groups[find(s)].append(s)
    clusters = [
        {"members": sorted(g), "size": len(g)}
        for g in groups.values() if len(g) >= 2
    ]
    return sorted(clusters, key=lambda c: -c["size"])


# ---------------------------------------------------------------------------
# Kee2u dendrogram clusters
# ---------------------------------------------------------------------------

def collect_leaves(node, prefix=""):
    """Recursively yield (sign_id, distance_from_root_path)."""
    if "name" in node:
        # leaf
        sid = node["name"].replace("SIGN ", "").lstrip("0") or "0"
        try:
            sid = f"{int(sid):03d}"
        except ValueError:
            pass
        yield sid
        return
    for child in node.get("children", []):
        yield from collect_leaves(child)


def kee2u_clusters_from_tree(tree_path: Path, cut_distance: float) -> list[dict]:
    if not tree_path.exists():
        return []
    with tree_path.open("r", encoding="utf-8") as fh:
        tree = json.load(fh)
    # Cut: walk top-down, whenever a node's tname > cut, descend; otherwise
    # collect all leaves below as one cluster.
    out_clusters: list[list[str]] = []

    def walk(node):
        if "name" in node:
            out_clusters.append(list(collect_leaves(node)))
            return
        d = float(node.get("tname", "0") or 0)
        if d > cut_distance:
            for ch in node.get("children", []):
                walk(ch)
        else:
            out_clusters.append(list(collect_leaves(node)))

    walk(tree)
    clusters = [
        {"members": sorted(set(c)), "size": len(set(c))}
        for c in out_clusters if len(set(c)) >= 2
    ]
    return sorted(clusters, key=lambda c: -c["size"])


# ---------------------------------------------------------------------------
# Agreement metrics
# ---------------------------------------------------------------------------

def jaccard(a: list[str], b: list[str]) -> float:
    sa, sb = set(a), set(b)
    u = sa | sb
    if not u:
        return 0.0
    return len(sa & sb) / len(u)


def agreement_matrix(name_a: str, clusters_a: list[dict],
                     name_b: str, clusters_b: list[dict]) -> list[dict]:
    """For every pair (cluster_a, cluster_b), record Jaccard if > 0."""
    out = []
    for i, ca in enumerate(clusters_a):
        for j, cb in enumerate(clusters_b):
            j_score = jaccard(ca["members"], cb["members"])
            if j_score > 0:
                out.append({
                    f"{name_a}_idx": i,
                    f"{name_b}_idx": j,
                    f"{name_a}_members": ca["members"],
                    f"{name_b}_members": cb["members"],
                    "jaccard": round(j_score, 4),
                    "shared": sorted(set(ca["members"]) & set(cb["members"])),
                })
    return out


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    if not M77_PATH.exists():
        print(f"ERROR: M77 not found: {M77_PATH}", file=sys.stderr)
        return 1
    print(f"Loading M77: {M77_PATH}", file=sys.stderr)
    inscriptions = []
    with M77_PATH.open("r", encoding="utf-8") as fh:
        for line in fh:
            tokens = line.strip().split()
            if tokens:
                inscriptions.append(tokens)
    print(f"  {len(inscriptions)} inscriptions", file=sys.stderr)

    print("Computing per-sign Daggumati features ...", file=sys.stderr)
    features = compute_features(inscriptions)
    print(f"  {len(features)} distinct signs", file=sys.stderr)

    print("Detecting allograph clusters ...", file=sys.stderr)
    clusters_dagg = daggumati_clusters(features)
    print(f"  {len(clusters_dagg)} multi-sign clusters", file=sys.stderr)
    if clusters_dagg[:5]:
        print("  Top 5 clusters by size:", file=sys.stderr)
        for c in clusters_dagg[:5]:
            print(f"    size={c['size']}: {c['members']}", file=sys.stderr)

    print(f"Loading Kee2u Segmentation_tree at cut distance {KEE2U_CUT_DISTANCE} ...", file=sys.stderr)
    clusters_kee2u = kee2u_clusters_from_tree(KEE2U_TREE, KEE2U_CUT_DISTANCE)
    print(f"  {len(clusters_kee2u)} clusters from Kee2u tree", file=sys.stderr)
    for c in clusters_kee2u:
        print(f"    size={c['size']}: {c['members']}", file=sys.stderr)

    # Agreement
    agreement = agreement_matrix(
        "daggumati_m77", clusters_dagg,
        "kee2u_dendrogram", clusters_kee2u,
    )

    n_pairs = len(agreement)
    print(f"\nAgreement: {n_pairs} cluster-pair overlaps with shared signs", file=sys.stderr)
    if agreement:
        for a in sorted(agreement, key=lambda x: -x["jaccard"])[:5]:
            print(f"  jaccard={a['jaccard']:.3f}  daggumati[{a['daggumati_m77_idx']}]"
                  f" \u2229 kee2u[{a['kee2u_dendrogram_idx']}]"
                  f" = {a['shared']}", file=sys.stderr)

    out = {
        "phase": "phase16",
        "purpose": "M77 Daggumati allograph clustering vs. Kee2u Segmentation_tree clustering",
        "thresholds": {
            "daggumati_pos_js": THR_POS_JS,
            "daggumati_ctx_cos": THR_CTX_COS,
            "min_occurrence": MIN_OCCURRENCE,
            "kee2u_cut_distance": KEE2U_CUT_DISTANCE,
        },
        "n_inscriptions": len(inscriptions),
        "n_signs_total": len(features),
        "n_signs_eligible": sum(1 for f in features.values() if f["count"] >= MIN_OCCURRENCE),
        "daggumati_m77_clusters": clusters_dagg,
        "kee2u_dendrogram_clusters": clusters_kee2u,
        "pairwise_agreement": agreement,
    }
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUT_PATH.open("w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2)
    print(f"\nWrote {OUT_PATH}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
