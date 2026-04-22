"""Create the CISI Optimal Anchor Set directly in the SQLite database.

This creates the 5-anchor set (with corrected P324='o') so it's available
in the UI via AnchorSetLoader and the Anchor Set Editor.

Run via: shell.cmd python backend/scripts/create_anchor_set.py
"""
import sys, asyncio, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "tests"))

# Use settings to find the DB path
from glossa_lab.config import get_settings

ANCHOR_PAIRS = [
    {
        "cipher": "P385",
        "target": "n",
        "confidence": "high",
        "note": "TERMINAL sign T=0.83, n=35. Precedes: P122 in 83% of cases. "
                "Dravidian genitive suffix -in phoneme /n/. "
                "Cross-validated: SA consistency 0.8564 with this anchor. [VERIFIED structural]"
    },
    {
        "cipher": "P324",
        "target": "o",
        "confidence": "high",
        "note": "INITIAL sign I=0.78, n=99 (most frequent in CISI). "
                "NEVER precedes P122 ('a'): 0/98 occurrences. "
                "Therefore full syllable 'ko' (king/chief, DEDR 2147), not bare /k/. "
                "Mapped as 'o' (vowel component) in SA single-char model. "
                "M-5A koyil (temple) hypothesis pending P096 validation. [VERIFIED positional + REVISED from k]"
    },
    {
        "cipher": "P122",
        "target": "a",
        "confidence": "high",
        "note": "Pure MEDIAL sign M=1.00, n=76 (2nd most frequent). "
                "Never appears in initial or terminal position. "
                "Dravidian vowel carrier /a/. "
                "SA consistency 0.8591 with this anchor (optimal set). [VERIFIED structural]"
    },
    {
        "cipher": "P086",
        "target": "m",
        "confidence": "medium",
        "note": "INITIAL sign I=0.54, n=35. Second most common initial after P324. "
                "Dravidian initial consonant /m/ (man=earth, meen=fish, mul=thorn). "
                "M-165A: P086+P122+P385 = m+a+n = 'man' (earth) confirmed in inscriptions. [INFERRED]"
    },
    {
        "cipher": "P060",
        "target": "i",
        "confidence": "medium",
        "note": "MEDIAL sign M=0.95, n=20. Common inner vowel. "
                "Dravidian vowel /i/. Appears frequently between initials and terminals. "
                "SA consistency 0.8591 with this anchor (optimal set). [INFERRED]"
    },
]


async def main():
    settings = get_settings()
    db_path = settings.data_dir / "glossa.db"

    if not db_path.exists():
        print(f"ERROR: Database not found at {db_path}")
        print("The backend must have been run at least once to initialize the DB.")
        sys.exit(1)

    # Import DB after verifying it exists
    from glossa_lab.database import Database  # noqa: PLC0415
    from datetime import datetime, timezone  # noqa: PLC0415

    db = Database(db_path)
    await db.connect()

    now = datetime.now(timezone.utc).isoformat()

    # Check if it already exists
    existing = await db.list_anchor_sets()
    existing_names = [a["name"] for a in existing]
    if "CISI Optimal 5-Anchor Set (P385=n, P324=o, P122=a, P086=m, P060=i)" in existing_names:
        print("Anchor set already exists — skipping creation.")
    else:
        result = await db.create_anchor_set(
            name="CISI Optimal 5-Anchor Set (P385=n, P324=o, P122=a, P086=m, P060=i)",
            description=(
                "5 structurally-motivated anchor readings from CISI Mohenjo-daro corpus "
                "(178 inscriptions, Parpola numbering). These are the optimal anchors: "
                "adding more reduces SA consistency (peak at 5). "
                "CRITICAL: P324 revised from 'k' to 'o' based on cross-validation "
                "(P324 never precedes P122; must be full syllable 'ko', not bare /k/). "
                "Use with SADecipher + indus_cisi corpus for decipherment experiments. "
                "Reference corpus: data/indus_cisi_corpus.json"
            ),
            corpus_id=None,
            language="dravidian",
            pairs=ANCHOR_PAIRS,
            created_at=now,
        )
        print(f"Created anchor set: {result['id']}")
        print(f"  Name: {result['name']}")
        print(f"  Pairs: {len(result['pairs'])}")
        for p in result["pairs"]:
            print(f"    {p['cipher']} -> {p['target']} ({p['confidence']}) — {p['note'][:60]}...")

    await db.close()
    print("\nAnchor Set ready. Load in experiments via AnchorSetLoader node.")
    print("In the UI: Corpora -> Anchor Sets -> select this set.")


if __name__ == "__main__":
    asyncio.run(main())
