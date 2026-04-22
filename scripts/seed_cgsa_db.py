"""Seed canonical sign registry and cluster assignments into glossa.db (V12)."""
import asyncio
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


async def main() -> None:
    from glossa_lab.database import init_db  # noqa: PLC0415
    db = await init_db(ROOT / "data")

    # Seed canonical signs from registry CSV
    csv_path = ROOT / "crosswalks" / "canonical_sign_registry.csv"
    with open(csv_path, newline="", encoding="utf-8") as f:
        signs = list(csv.DictReader(f))
    for s in signs:
        s["in_corpus"] = s.get("in_corpus", "False").lower() in ("true", "1", "yes")
    n1 = await db.seed_canonical_signs(signs)
    print(f"Seeded {n1} canonical signs")

    # Seed cluster assignments from sign_clusters.json
    json_path = ROOT / "analysis" / "sign_clusters.json"
    cluster_data = json.loads(json_path.read_text("utf-8"))
    best_k = cluster_data["best_k"]
    sil = cluster_data.get("k_results", {}).get(str(best_k), {}).get("silhouette", 0.0)
    s2c: dict = cluster_data["sign_to_cluster"]
    assignments = [
        {
            "sign_id": sid,
            "cluster_label": lbl,
            "cluster_k": best_k,
            "method": "hierarchical_ward",
            "silhouette": sil,
            "dominant_pos": "",
        }
        for sid, lbl in s2c.items()
    ]
    n2 = await db.seed_cluster_assignments(assignments, "2026-04-22T18:49:47Z")
    print(f"Seeded {n2} cluster assignments (k={best_k}, silhouette={sil})")

    summary = await db.get_clusters_summary()
    print(f"Cluster summary: {summary}")
    await db.close()


if __name__ == "__main__":
    asyncio.run(main())
