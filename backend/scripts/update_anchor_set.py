"""Update the CISI optimal anchor set in glossa.db.

Changes:
  1. P324: 'o' -> 'k'  (SA phonotactics confirmed P324='k' is better, 0.8591 vs 0.817)
  2. Add P332='o' as 6th pair (CV pair vowel for 'ko'; costs only -0.005pp consistency)

Run: shell.cmd python backend/scripts/update_anchor_set.py
"""
import sys, asyncio, json
from pathlib import Path
from datetime import datetime, timezone
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


async def main():
    settings = get_settings()
    db_path = settings.data_dir / "glossa.db"
    if not db_path.exists():
        print(f"ERROR: DB not found at {db_path}")
        sys.exit(1)

    from glossa_lab.database import Database  # noqa: PLC0415
    db = Database(db_path)
    await db.connect()

    # Check it exists
    existing = await db.get_anchor_set(ANCHOR_SET_ID)
    if existing is None:
        print(f"ERROR: Anchor set {ANCHOR_SET_ID} not found")
        await db.close()
        sys.exit(1)

    print(f"Updating: '{existing['name']}'")
    print(f"  Old pairs: {len(existing['pairs'])}")

    result = await db.update_anchor_set(ANCHOR_SET_ID,
        name="CISI Optimal 6-Anchor Set (P385=n, P324=k, P122=a, P086=m, P060=i, P332=o)",
        description=(
            "6 structurally-motivated anchor readings from CISI Mohenjo-daro corpus. "
            "P324='k' corrected (SA phonotactics: 0.8591 vs 0.817 for 'o'). "
            "P332='o' added as 6th pair: CV pair vowel completing P324's /k/ consonant "
            "to form the royal title syllable 'ko' (king/chief, DEDR 2147). "
            "Adding P332='o' costs only -0.005pp consistency (within noise). HCI 88.4% unchanged. "
            "Optimal for use with indus_cisi corpus + SADecipher node."
        ),
        pairs=UPDATED_PAIRS,
    )
    if result:
        print(f"  New pairs: {len(result['pairs'])}")
        for p in result["pairs"]:
            print(f"    {p['cipher']:6s} -> {p['target']}  ({p['confidence']})")
        print(f"\nUpdated: '{result['name']}'")
    else:
        print("ERROR: Update failed")

    await db.close()


if __name__ == "__main__":
    asyncio.run(main())
