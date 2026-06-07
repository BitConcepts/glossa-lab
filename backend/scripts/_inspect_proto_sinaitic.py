"""Inspect Proto-Sinaitic corpus to determine if splitting is needed."""
import sqlite3
import json
from pathlib import Path
from collections import Counter

DB = Path(__file__).resolve().parents[1] / "data" / "glossa.db"
conn = sqlite3.connect(str(DB))
conn.row_factory = sqlite3.Row

r = conn.execute(
    "SELECT id, name, content, alphabet_size, metadata, reading_direction "
    "FROM texts WHERE name LIKE '%Proto-Sinaitic%'"
).fetchone()

if not r:
    print("Proto-Sinaitic corpus not found!")
    exit()

content = json.loads(r["content"]) if isinstance(r["content"], str) else r["content"]
meta = json.loads(r["metadata"]) if isinstance(r["metadata"], str) else (r["metadata"] or {})

print(f"Name: {r['name']}")
print(f"Direction: {r['reading_direction']}")
print(f"Alphabet size: {r['alphabet_size']}")
print(f"Total tokens: {len(content)}")
print(f"Unique signs: {len(set(content))}")
print()

# Check if metadata has inscription-level data
inscriptions = meta.get("inscriptions") or meta.get("words") or []
if inscriptions:
    print(f"Inscriptions: {len(inscriptions)}")
    for i, insc in enumerate(inscriptions[:10]):
        if isinstance(insc, list):
            print(f"  [{i}] {insc[:8]}... (len={len(insc)})")
        elif isinstance(insc, dict):
            seq = insc.get("sequence", insc.get("signs", []))
            src = insc.get("source", insc.get("id", ""))
            print(f"  [{i}] {src}: {seq[:6]}... (len={len(seq)})")
else:
    print("No inscription-level data in metadata")
    # Try to infer inscriptions from token patterns
    # If content is a flat list, check for delimiters or patterns
    freq = Counter(content)
    print(f"\nTop 10 signs by frequency:")
    for sign, count in freq.most_common(10):
        print(f"  '{sign}': {count}")

print(f"\nMetadata keys: {list(meta.keys())}")
for k, v in meta.items():
    val_str = str(v)[:150]
    print(f"  {k}: {val_str}")

# Run Ashraf direction detection
print("\n=== Ashraf & Sinha Direction Detection ===")
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from glossa_lab.corpus_utils import run_ashraf_detection

if inscriptions and isinstance(inscriptions[0], list):
    words = inscriptions
elif inscriptions and isinstance(inscriptions[0], dict):
    words = [i.get("sequence", i.get("signs", [])) for i in inscriptions]
else:
    # Fall back to 4-token windows
    window = 4
    words = [content[i:i+window] for i in range(0, len(content)-window+1, window)]
    print(f"(Using {len(words)} sliding windows of {window} tokens)")

result = run_ashraf_detection(words)
print(f"Inferred direction: {result['inferred_direction']}")
print(f"Confidence: {result['confidence']}")
print(f"H(pos-0): {result['entropy_pos0']}")
print(f"H(pos-N1): {result['entropy_posN1']}")
print(f"Interpretation: {result['interpretation']}")

conn.close()
