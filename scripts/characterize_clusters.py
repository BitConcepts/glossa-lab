"""
Characterize the 40 CGSA sign clusters structurally.

For each cluster:
- dominant positional class (INITIAL/MEDIAL/TERMINAL/BIMODAL/MIXED)
- top ICIT function codes (ITM, TMK, LOG, NUM, SYL)
- mean end_rate, start_rate, internal_rate across members
- top 3 member signs (with descriptions from mayig features)

Output: reports/cluster_characterization.md
"""

from __future__ import annotations

import csv
import json
import math
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_registry() -> dict[str, dict]:
    path = ROOT / "crosswalks" / "canonical_sign_registry.csv"
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    return {r["sign_id"]: r for r in rows}


def load_clusters() -> tuple[dict[str, int], int]:
    data = json.loads((ROOT / "analysis" / "sign_clusters.json").read_text("utf-8"))
    return data["sign_to_cluster"], data["best_k"]


def load_corpus() -> list[dict]:
    with open(ROOT / "data_normalized" / "corpus_master.csv", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def positional_profile(records: list[dict], sign_ids: set[str]) -> dict:
    freq: Counter = Counter()
    sf: Counter = Counter()
    ef: Counter = Counter()
    mf: Counter = Counter()
    for r in records:
        seq = r["sign_sequence_raw"].split()
        for i, s in enumerate(seq):
            if s not in sign_ids:
                continue
            freq[s] += 1
            if i == 0: sf[s] += 1
            elif i == len(seq) - 1: ef[s] += 1
            else: mf[s] += 1
    total = sum(freq.values()) or 1
    return {
        "total_tokens": total,
        "start_rate": round(sum(sf.values()) / total, 4),
        "end_rate": round(sum(ef.values()) / total, 4),
        "internal_rate": round(sum(mf.values()) / total, 4),
    }


def classify_cluster(end_rate: float, start_rate: float, internal_rate: float) -> str:
    if end_rate >= 0.55: return "TERMINAL"
    if start_rate >= 0.55: return "INITIAL"
    if internal_rate >= 0.65: return "MEDIAL"
    if start_rate >= 0.30 and end_rate >= 0.30: return "BIMODAL"
    return "MIXED"


def main() -> None:
    registry = load_registry()
    s2c, best_k = load_clusters()
    records = load_corpus()

    # Group signs by cluster
    clusters: dict[int, list[str]] = defaultdict(list)
    for sign_id, lbl in s2c.items():
        clusters[lbl].append(sign_id)

    # Characterize each cluster
    lines = [
        "# Cluster Characterization Report (Phase 5 — CGSA)",
        f"Generated: {NOW}",
        f"Total clusters: {best_k} | Signs clustered: {len(s2c)} (P-signs only)",
        "",
        "**RULE**: No phonetic assignments. Labels are structural descriptors only.",
        "",
        "---",
        "",
    ]

    cluster_rows = []
    for lbl in sorted(clusters.keys()):
        members = sorted(clusters[lbl])
        sign_ids_set = set(members)
        pos = positional_profile(records, sign_ids_set)

        # Collect registry metadata
        icit_fns: Counter = Counter()
        descriptions = []
        wells_all = []
        for m in members:
            r = registry.get(m, {})
            fn = r.get("icit_function", "")
            if fn: icit_fns[fn] += 1
            desc = r.get("description", "").strip()
            if desc: descriptions.append(f"{m}: {desc[:50]}")
            for w in (r.get("wells_ids", "") or "").split("|"):
                if w: wells_all.append(w)

        dominant = classify_cluster(pos["end_rate"], pos["start_rate"], pos["internal_rate"])
        top_icit = ", ".join(f"{fn}({n})" for fn, n in icit_fns.most_common(3)) or "—"

        cluster_rows.append({
            "label": lbl,
            "size": len(members),
            "dominant": dominant,
            "end_rate": pos["end_rate"],
            "start_rate": pos["start_rate"],
            "internal_rate": pos["internal_rate"],
            "total_tokens": pos["total_tokens"],
            "icit": top_icit,
            "members": members,
            "descriptions": descriptions[:3],
        })

    # Sort by structural class then size
    _order = {"TERMINAL": 0, "INITIAL": 1, "MEDIAL": 2, "BIMODAL": 3, "MIXED": 4}
    cluster_rows.sort(key=lambda r: (_order.get(r["dominant"], 5), -r["size"]))

    # Summary table
    class_dist = Counter(r["dominant"] for r in cluster_rows)
    lines += [
        "## Summary",
        "",
        f"| Class | Clusters | Notes |",
        f"|-------|----------|-------|",
        f"| TERMINAL | {class_dist['TERMINAL']} | High end_rate — candidate suffix/case markers |",
        f"| INITIAL | {class_dist['INITIAL']} | High start_rate — candidate determinatives |",
        f"| MEDIAL | {class_dist['MEDIAL']} | High internal_rate — candidate roots/stems |",
        f"| BIMODAL | {class_dist['BIMODAL']} | Both initial and terminal bias |",
        f"| MIXED | {class_dist['MIXED']} | Flexible position — likely phonetic syllables |",
        "",
        "---",
        "",
        "## Per-Cluster Detail",
        "",
    ]

    for row in cluster_rows:
        lines += [
            f"### Cluster {row['label']} — {row['dominant']} ({row['size']} signs, {row['total_tokens']} tokens)",
            f"- **end_rate**: {row['end_rate']} | **start_rate**: {row['start_rate']} | **internal_rate**: {row['internal_rate']}",
            f"- **ICIT functions**: {row['icit']}",
            f"- **Members**: {', '.join(row['members'][:10])}{'...' if len(row['members']) > 10 else ''}",
        ]
        for desc in row["descriptions"][:2]:
            lines.append(f"  - {desc}")
        lines.append("")

    out = ROOT / "reports" / "cluster_characterization.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"Written: {out}")

    # Print summary
    print(f"\nCluster structural breakdown:")
    for cls, n in sorted(class_dist.items(), key=lambda x: _order.get(x[0], 5)):
        print(f"  {cls:10s}: {n} clusters")


if __name__ == "__main__":
    main()
