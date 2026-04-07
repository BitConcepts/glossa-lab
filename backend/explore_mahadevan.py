"""Explore Mahadevan data to understand what's available for crosswalk."""
import json
from pathlib import Path

R = Path(__file__).parent.parent / "reports"

for fname in ["mahadevan_bigrams.json", "mahadevan_frequencies.json",
              "mahadevan_bigrams_mapped.json", "mahadevan_texts.json"]:
    path = R / fname
    if not path.exists():
        print(f"MISSING: {fname}")
        continue
    data = json.loads(path.read_text("utf-8"))
    print(f"\n{'='*50}")
    print(f"FILE: {fname}")
    if isinstance(data, dict):
        print(f"  Dict keys ({len(data)}): {list(data.keys())[:8]}")
        for k, v in list(data.items())[:3]:
            print(f"  [{k!r}] => {str(v)[:80]}")
    elif isinstance(data, list):
        print(f"  List length: {len(data)}")
        for item in data[:3]:
            print(f"  {str(item)[:100]}")
