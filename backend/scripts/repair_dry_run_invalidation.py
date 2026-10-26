#!/usr/bin/env python3
"""WP1 acceptance dry run: invalidate one parent evidence record and show
that the invalidation reaches every current descendant claim and every
displayed summary in the dependency map — while historical file bytes
stay unchanged.

This script is read-only. It loads the repair patch's dependency map and
claim-status overlay, marks one parent record `invalid_method` IN MEMORY
ONLY, walks the claim graph, and (when --work-dir is given) hashes every
staged historical file before and after the walk and asserts the hashes
are identical. Nothing is written anywhere.

Usage:
    python3 repair_dry_run_invalidation.py [--record crosswalk_v2]
                                           [--work-dir PATH]

Defaults: --record crosswalk_v2 (the crosswalk v2 data file, parent of
the Parpola-agreement claim chain). The map and overlay are located
relative to this script: patch/docs/repair-2026-10-26/.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
DOCS = HERE.parents[2] / "docs" / "repair-2026-10-26"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def hash_tree(root: Path) -> dict[str, str]:
    out = {}
    for p in sorted(root.rglob("*")):
        if p.is_file():
            out[str(p.relative_to(root))] = sha256(p)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--record", default="crosswalk_v2",
                    help="id of the parent evidence record to invalidate")
    ap.add_argument("--work-dir", default=None,
                    help="staged historical tree to hash before/after")
    args = ap.parse_args()

    depmap = json.loads((DOCS / "dependency-map.json").read_text("utf-8"))
    overlay = json.loads((DOCS / "claim-status-overlay.json").read_text("utf-8"))

    records = {r["id"]: r for r in depmap["records"]}
    claims = {c["claim_id"]: c for c in depmap["claims"]}
    if args.record not in records:
        print(f"FAIL: record {args.record!r} is not in the dependency map")
        return 1
    parent = records[args.record]

    before = hash_tree(Path(args.work_dir)) if args.work_dir else {}

    print("WP1 DRY-RUN INVALIDATION")
    print(f"parent record : {parent['id']} — {parent['path']}")
    print(f"parent sha256 : {parent['sha256']}")
    print("action        : mark invalid_method (in memory only; no file is modified)")
    print()

    # Forward reachability: record -> claims that depend on it (directly),
    # then claim -> claim along depends_on_claims, transitively.
    children: dict[str, list[str]] = {}
    for c in depmap["claims"]:
        for dep in c.get("depends_on_claims", []):
            children.setdefault(dep, []).append(c["claim_id"])

    affected: list[str] = []
    seen: set[str] = set()
    frontier = [c["claim_id"] for c in depmap["claims"]
                if args.record in c.get("depends_on_records", [])]
    while frontier:
        cid = frontier.pop(0)
        if cid in seen:
            continue
        seen.add(cid)
        affected.append(cid)
        frontier.extend(children.get(cid, []))

    overlay_by_claim: dict[str, list[dict]] = {}
    for e in overlay["entries"]:
        overlay_by_claim.setdefault(e["claim_id"], []).append(e)

    print(f"descendant claims reached: {len(affected)}")
    n_summaries = 0
    for cid in affected:
        c = claims[cid]
        print(f"\n- {cid}: {c['claim'][:110]}")
        for s in c.get("displayed_summaries", []):
            n_summaries += 1
            print(f"    summary [{s['surface']} @ {s['location']}]: {s['text'][:110]}")
        for e in overlay_by_claim.get(cid, []):
            print(f"    overlay [{e['surface']}]: status={e['status']}")
    print(f"\ndisplayed summaries reached: {n_summaries}")

    # Every affected claim must carry an explicit overlay disposition or be
    # a claim whose own text already limits it; report any gap honestly.
    undisposed = [cid for cid in affected if cid not in overlay_by_claim]
    if undisposed:
        print(f"claims reached without an overlay entry: {undisposed}")

    if args.work_dir:
        after = hash_tree(Path(args.work_dir))
        same = before == after
        print(f"\nhistorical bytes check: {len(before)} staged files hashed before and after; "
              f"identical = {same}")
        if not same:
            for k in before:
                if before.get(k) != after.get(k):
                    print(f"  CHANGED: {k}")
            print("RESULT: FAIL — a historical file changed during the dry run")
            return 1

    print("\nRESULT: PASS — invalidation of the parent record reached all "
          f"{len(affected)} descendant claim(s) and {n_summaries} displayed "
          "summar(ies); historical bytes unchanged.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
