#!/usr/bin/env python3
"""Delete 6 noise hypotheses from glossa.db.

These are LLM-generated meta-action entries (e.g. "Plan chain",
"Create Hypothesis Chain") that pollute the hypothesis tracker.

Usage:
    python backend/scripts/cleanup_hypotheses.py [--db PATH]

Defaults to backend/data/glossa.db relative to repo root.
"""
from __future__ import annotations

import argparse
import sqlite3
import sys
from pathlib import Path

NOISE_PREFIXES = [
    "e6ab5842",  # Plan chain
    "b8d69b0b",  # Create Hypothesis Chain
    "0660e244",  # Create Hypothesis for Dravidian
    "4e25f46c",  # Plan experiment chain for Indus
    "bf24fa5e",  # Propose experiment chain for Indus
    "b1f04723",  # Plan an experiment chain for astronomical
]

DEFAULT_DB = Path(__file__).resolve().parents[1] / "data" / "glossa.db"


def main() -> int:
    parser = argparse.ArgumentParser(description="Delete noise hypotheses")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB,
                        help="Path to glossa.db")
    args = parser.parse_args()

    db_path: Path = args.db
    if not db_path.exists():
        print(f"ERROR: database not found at {db_path}", file=sys.stderr)
        return 1

    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA journal_mode=WAL")
    cur = conn.cursor()

    # Confirm rows exist before deleting
    print("=== Pre-delete check ===")
    found_ids: list[str] = []
    for prefix in NOISE_PREFIXES:
        rows = cur.execute(
            "SELECT id, substr(title, 1, 80) FROM hypotheses WHERE id LIKE ?",
            (prefix + "%",),
        ).fetchall()
        for row in rows:
            found_ids.append(row[0])
            print(f"  FOUND: {row[0]}  |  {row[1]}")
        if not rows:
            print(f"  NOT FOUND: {prefix}%")

    if not found_ids:
        print("\nNo matching rows — nothing to delete.")
        conn.close()
        return 0

    # Delete
    placeholders = ",".join("?" for _ in found_ids)
    cur.execute(f"DELETE FROM hypotheses WHERE id IN ({placeholders})", found_ids)
    deleted = cur.rowcount
    conn.commit()

    # Verify
    print(f"\n=== Deleted {deleted} row(s) ===")
    for prefix in NOISE_PREFIXES:
        remaining = cur.execute(
            "SELECT COUNT(*) FROM hypotheses WHERE id LIKE ?",
            (prefix + "%",),
        ).fetchone()[0]
        if remaining:
            print(f"  WARNING: {prefix}% still has {remaining} row(s)")

    total = cur.execute("SELECT COUNT(*) FROM hypotheses").fetchone()[0]
    print(f"Total hypotheses remaining: {total}")

    conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
