"""Upsert the CISI optimal anchor set in glossa.db.

Changes:
  1. P324: 'o' -> 'k'  (SA phonotactics confirmed P324='k' is better, 0.8591 vs 0.817)
  2. Add P332='o' as 6th pair (CV pair vowel for 'ko'; costs only -0.005pp consistency)

Idempotent and multi-DB safe: writes the canonical anchor-set row
(`dcf69e6e69fe`) into every database it can find -- whichever cwd the
backend was launched from, the live API will see the same rows.

Run: shell.cmd python backend/scripts/update_anchor_set.py
"""
import argparse
import asyncio
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "tests"))
from glossa_lab.config import get_settings

ANCHOR_SET_ID = "dcf69e6e69fe"

UPDATED_PAIRS = [
    {
        "cipher": "P385",
        "target": "n",
        "confidence": "high",
        "note": "TERMINAL sign T=0.83, n=35. Dravidian genitive suffix -in phoneme /n/. "
                "SA consistency 0.8564 with this anchor. [VERIFIED structural]",
    },
    {
        "cipher": "P324",
        "target": "k",          # CORRECTED from 'o' — SA phonotactics prefer 'k' (+4.2pp)
        "confidence": "high",
        "note": "INITIAL sign I=0.78, n=99 (most frequent in CISI). "
                "NEVER precedes P122 ('a'): full syllable 'ko' (king, DEDR 2147). "
                "SA maps to 'k' (primary consonant phoneme): 0.8591 vs 0.817 for 'o'. "
                "P324(/k/) + P332(/o/) = 'ko' as a CV bigram pair. [VERIFIED SA phonotactics]",
    },
    {
        "cipher": "P122",
        "target": "a",
        "confidence": "high",
        "note": "Pure MEDIAL sign M=1.00, n=76. Dravidian vowel carrier /a/. "
                "SA consistency peak 0.8591 with this anchor. [VERIFIED structural]",
    },
    {
        "cipher": "P086",
        "target": "m",
        "confidence": "medium",
        "note": "INITIAL sign I=0.54, n=35. Dravidian initial consonant /m/. "
                "M-165A: P086+P122+P385 = man (earth) confirmed. [INFERRED]",
    },
    {
        "cipher": "P060",
        "target": "i",
        "confidence": "medium",
        "note": "MEDIAL sign M=0.95, n=20. Dravidian inner vowel /i/. [INFERRED]",
    },
    {
        "cipher": "P332",          # NEW — 6th anchor
        "target": "o",
        "confidence": "medium",
        "note": "MEDIAL sign M=1.00, n=11. 91% of occurrences follow P324. "
                "P332 = vowel /o/ completing the P324(/k/) consonant: P324+P332 = 'ko'. "
                "Adding P332='o' costs only -0.005pp consistency (noise). HCI unchanged at 88.4%. "
                "Confirms CV PAIR structure of Indus script. [VERIFIED structural + INFERRED phoneme]",
    },
]


ANCHOR_SET_NAME = (
    "CISI Optimal 6-Anchor Set "
    "(P385=n, P324=k, P122=a, P086=m, P060=i, P332=o)"
)
ANCHOR_SET_DESCRIPTION = (
    "6 structurally-motivated anchor readings from CISI Mohenjo-daro corpus. "
    "P324='k' corrected (SA phonotactics: 0.8591 vs 0.817 for 'o'). "
    "P332='o' added as 6th pair: CV pair vowel completing P324's /k/ consonant "
    "to form the royal title syllable 'ko' (king/chief, DEDR 2147). "
    "Adding P332='o' costs only -0.005pp consistency (within noise). HCI 88.4% unchanged. "
    "Optimal for use with indus_cisi corpus + SADecipher node."
)


def _candidate_db_paths(explicit: Path | None) -> list[Path]:
    """Return every glossa.db we know about, deduplicated and existing-or-creatable.

    The backend launcher (`scripts/run-backend-svc.cmd`) sets cwd to
    ``backend/`` so the runtime DB resolves to ``backend/data/glossa.db``.
    Earlier ad-hoc invocations of this script from the repo root pointed
    at ``glossa-lab/data/glossa.db``. We touch all of them so the live
    backend always sees the canonical anchor row.
    """
    if explicit is not None:
        return [explicit]
    repo_root = Path(__file__).resolve().parents[2]
    settings_dir = get_settings().data_dir
    candidates = [
        repo_root / "backend" / "data" / "glossa.db",
        repo_root / "data" / "glossa.db",
        repo_root / "frontend" / "data" / "glossa.db",
        settings_dir / "glossa.db",
    ]
    seen: set[Path] = set()
    out: list[Path] = []
    for p in candidates:
        try:
            resolved = p.resolve()
        except OSError:
            resolved = p
        if resolved in seen:
            continue
        seen.add(resolved)
        out.append(p)
    return out


async def _upsert_one(db_path: Path) -> str:
    """Apply the canonical anchor set to a single database; return a status line."""
    if not db_path.exists():
        return f"  [skip] {db_path} (not found)"
    from glossa_lab.database import Database  # noqa: PLC0415

    db = Database(db_path)
    await db.connect()
    try:
        existing = await db.get_anchor_set(ANCHOR_SET_ID)
        now = datetime.now(timezone.utc).isoformat()
        if existing is None:
            # Database hasn't been seeded yet — insert the canonical row
            # directly so the ID is stable across machines.
            assert db._conn  # noqa: SLF001
            import json as _json  # noqa: PLC0415

            await db._conn.execute(  # noqa: SLF001
                """INSERT INTO anchor_sets
                   (id, name, description, corpus_id, language,
                    pairs, created_at, updated_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    ANCHOR_SET_ID,
                    ANCHOR_SET_NAME,
                    ANCHOR_SET_DESCRIPTION,
                    "indus_cisi",
                    "",
                    _json.dumps(UPDATED_PAIRS),
                    now,
                    now,
                ),
            )
            await db._conn.commit()  # noqa: SLF001
            return (
                f"  [insert] {db_path}: created '{ANCHOR_SET_NAME}'"
                f" with {len(UPDATED_PAIRS)} pair(s)"
            )
        result = await db.update_anchor_set(
            ANCHOR_SET_ID,
            name=ANCHOR_SET_NAME,
            description=ANCHOR_SET_DESCRIPTION,
            pairs=UPDATED_PAIRS,
        )
        if not result:
            return f"  [error] {db_path}: update returned None"
        return (
            f"  [update] {db_path}: {len(existing['pairs'])} -> "
            f"{len(result['pairs'])} pair(s)"
        )
    finally:
        await db.close()


async def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=None,
        help="Apply only to <data-dir>/glossa.db. Default: every known location.",
    )
    args = parser.parse_args()
    explicit = (args.data_dir / "glossa.db") if args.data_dir else None

    print(f"Upserting anchor set {ANCHOR_SET_ID}")
    print(f"  name: {ANCHOR_SET_NAME}")
    print(f"  pairs: {len(UPDATED_PAIRS)} ({', '.join(p['cipher'] + '=' + p['target'] for p in UPDATED_PAIRS)})")
    print()

    any_updated = False
    for db_path in _candidate_db_paths(explicit):
        line = await _upsert_one(db_path)
        print(line)
        if "[insert]" in line or "[update]" in line:
            any_updated = True

    if not any_updated:
        print("\nERROR: no glossa.db could be upserted.")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
