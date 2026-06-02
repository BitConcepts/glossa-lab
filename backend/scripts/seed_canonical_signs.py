#!/usr/bin/env python3
"""Seed the canonical_signs table from all available anchor sources.

Sources (in priority order):
  1. backend/reports/INDUS_FINAL_ANCHORS.json — authoritative anchor file
  2. anchor_sets DB table — user-created named anchor sets (pairs JSON)
  3. backend/outputs/anchor_staging_archive.json — archived/verified candidates
  4. backend/outputs/anchor_staging.json — approved staged candidates

Usage:
  python backend/scripts/seed_canonical_signs.py
"""
from __future__ import annotations

import json
import re
import sqlite3
import sys
from pathlib import Path

# Resolve paths relative to repo root
_SCRIPT_DIR = Path(__file__).resolve().parent
_BACKEND_DIR = _SCRIPT_DIR.parent
_REPO_ROOT = _BACKEND_DIR.parent
_REPORTS_DIR = _BACKEND_DIR / "reports"
_OUTPUTS_DIR = _BACKEND_DIR / "outputs"
_DB_PATH = _BACKEND_DIR / "data" / "glossa.db"


def _parse_phase(source_exp: str) -> int:
    """Extract phase number from experiment id."""
    m = re.search(r"[_pP](\d+)", source_exp or "")
    return int(m.group(1)) if m else 0


def main() -> None:
    signs: dict[str, dict] = {}  # sign_id → sign data

    # ── 1. INDUS_FINAL_ANCHORS.json ─────────────────────────────────────
    fa_path = _REPORTS_DIR / "INDUS_FINAL_ANCHORS.json"
    fa_count = 0
    if fa_path.exists():
        data = json.loads(fa_path.read_text(encoding="utf-8"))
        anchors = data.get("anchors") or {}
        for sid, info in anchors.items():
            reading = info.get("reading", "")
            confidence = (info.get("confidence") or "LOW").upper()
            dedr = str(info.get("dedr", ""))
            phase = info.get("phase_upgraded", 0) or _parse_phase(info.get("source", ""))
            signs[sid] = {
                "internal_id": sid,
                "sign_id": sid,
                "numbering_system": "wells",
                "description": reading,
                "wells_ids": "",
                "mahadevan_ids": "",
                "parpola_allographs": "",
                "icit_function": info.get("gloss", ""),
                "corpus_freq": 0,
                "start_rate": 0.0,
                "end_rate": 0.0,
                "internal_rate": 0.0,
                "in_corpus": 1,
                "n_feature_dims": 0,
                "_confidence": confidence,
                "_reading": reading,
                "_dedr": dedr,
                "_phase": phase,
                "_source": info.get("source", ""),
                "_basis": info.get("basis", ""),
            }
            fa_count += 1
        print(f"  INDUS_FINAL_ANCHORS.json: {fa_count} signs")
    else:
        print(f"  INDUS_FINAL_ANCHORS.json: not found at {fa_path}")

    # ── 2. anchor_sets DB table ─────────────────────────────────────────
    db_count = 0
    if _DB_PATH.exists():
        conn = sqlite3.connect(str(_DB_PATH))
        conn.row_factory = sqlite3.Row
        try:
            rows = conn.execute("SELECT * FROM anchor_sets").fetchall()
            for row in rows:
                pairs_raw = row["pairs"]
                try:
                    pairs = json.loads(pairs_raw) if isinstance(pairs_raw, str) else pairs_raw
                except Exception:
                    continue
                if not isinstance(pairs, list):
                    continue
                for pair in pairs:
                    cipher = pair.get("cipher", "")
                    target = pair.get("target", "")
                    if not cipher or cipher in signs:
                        continue
                    conf = (pair.get("confidence") or "medium").upper()
                    signs[cipher] = {
                        "internal_id": cipher,
                        "sign_id": cipher,
                        "numbering_system": "wells",
                        "description": target,
                        "wells_ids": "",
                        "mahadevan_ids": "",
                        "parpola_allographs": "",
                        "icit_function": "",
                        "corpus_freq": 0,
                        "start_rate": 0.0,
                        "end_rate": 0.0,
                        "internal_rate": 0.0,
                        "in_corpus": 1,
                        "n_feature_dims": 0,
                        "_confidence": conf,
                        "_reading": target,
                        "_dedr": "",
                        "_phase": 0,
                        "_source": f"anchor_set:{row['id']}",
                        "_basis": f"From anchor set: {row['name']}",
                    }
                    db_count += 1
            print(f"  anchor_sets table: {db_count} new signs ({len(rows)} sets scanned)")
        except Exception as exc:
            print(f"  anchor_sets table: error — {exc}")
        finally:
            conn.close()
    else:
        print(f"  Database not found at {_DB_PATH}")

    # ── 3. Staging files ────────────────────────────────────────────────
    for fname in ("anchor_staging_archive.json", "anchor_staging.json"):
        path = _OUTPUTS_DIR / fname
        if not path.exists():
            print(f"  {fname}: not found (skipped)")
            continue
        try:
            items = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(items, list):
                print(f"  {fname}: not a list (skipped)")
                continue
            stg_count = 0
            for item in items:
                sid = item.get("sign") or item.get("sign_id", "")
                if not sid or sid in signs:
                    continue
                status = (item.get("review_status") or "").lower()
                if status not in ("approved", "verified", "accepted"):
                    continue
                signs[sid] = {
                    "internal_id": sid,
                    "sign_id": sid,
                    "numbering_system": "wells",
                    "description": item.get("proposed_reading", ""),
                    "wells_ids": "",
                    "mahadevan_ids": "",
                    "parpola_allographs": "",
                    "icit_function": "",
                    "corpus_freq": 0,
                    "start_rate": 0.0,
                    "end_rate": 0.0,
                    "internal_rate": 0.0,
                    "in_corpus": 1,
                    "n_feature_dims": 0,
                    "_confidence": (item.get("confidence") or "LOW").upper(),
                    "_reading": item.get("proposed_reading", ""),
                    "_dedr": "",
                    "_phase": _parse_phase(item.get("source_experiment", "")),
                    "_source": item.get("source_experiment", ""),
                    "_basis": item.get("evidence_type", ""),
                }
                stg_count += 1
            print(f"  {fname}: {stg_count} new signs")
        except Exception as exc:
            print(f"  {fname}: error — {exc}")

    # ── Insert into DB ──────────────────────────────────────────────────
    if not _DB_PATH.exists():
        print(f"\nERROR: Database not found at {_DB_PATH}")
        sys.exit(1)

    conn = sqlite3.connect(str(_DB_PATH))
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=5000")

    # Count existing
    try:
        existing_count = conn.execute("SELECT COUNT(*) FROM canonical_signs").fetchone()[0]
    except Exception:
        existing_count = 0

    inserted = 0
    updated = 0
    for sid, s in signs.items():
        try:
            existing = conn.execute(
                "SELECT internal_id FROM canonical_signs WHERE internal_id=? OR sign_id=?",
                (sid, sid),
            ).fetchone()
            if existing:
                conn.execute(
                    """UPDATE canonical_signs SET
                       description=?, icit_function=?, in_corpus=?
                       WHERE internal_id=? OR sign_id=?""",
                    (s["description"], s["icit_function"], s["in_corpus"], sid, sid),
                )
                updated += 1
            else:
                conn.execute(
                    """INSERT INTO canonical_signs
                       (internal_id, sign_id, numbering_system, description,
                        wells_ids, mahadevan_ids, parpola_allographs, icit_function,
                        corpus_freq, start_rate, end_rate, internal_rate,
                        in_corpus, n_feature_dims)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (
                        s["internal_id"], s["sign_id"], s["numbering_system"],
                        s["description"], s["wells_ids"], s["mahadevan_ids"],
                        s["parpola_allographs"], s["icit_function"],
                        s["corpus_freq"], s["start_rate"], s["end_rate"],
                        s["internal_rate"], s["in_corpus"], s["n_feature_dims"],
                    ),
                )
                inserted += 1
        except Exception as exc:
            print(f"  Warning: failed to insert/update {sid}: {exc}")

    conn.commit()
    total = conn.execute("SELECT COUNT(*) FROM canonical_signs").fetchone()[0]
    conn.close()

    print(f"\n{'=' * 50}")
    print(f"Inserted {inserted} signs, updated {updated}, total {total}")
    print(f"Previously in DB: {existing_count}")
    print(f"{'=' * 50}")


if __name__ == "__main__":
    print("Seeding canonical_signs from available sources...\n")
    main()
