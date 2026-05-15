"""Check Penn CSV columns for image URLs and inspect Firestore indusarrays."""
import csv, json
from pathlib import Path

ROOT = Path(__file__).parents[2]

# 1. Penn CSV columns
print("=" * 60)
print("PENN INDUS FILTERED CSV — columns & media fields")
print("=" * 60)
penn_csv = ROOT / "glossa-corpus/indus/sources/penn-museum/raw/2026-05-14/penn_indus_filtered.csv"
with open(penn_csv, encoding="utf-8", errors="replace") as f:
    reader = csv.DictReader(f)
    cols = reader.fieldnames or []
    print(f"Total columns: {len(cols)}")
    print("All columns:")
    for c in cols:
        print(f"  {c}")
    rows = []
    for i, row in enumerate(reader):
        rows.append(row)
        if i >= 4:
            break
print()
print("Media-like fields in first 3 rows:")
for row in rows[:3]:
    media = {k: v for k, v in row.items()
             if any(x in k.lower() for x in ["image", "media", "photo", "url", "thumb", "uri", "cdn"])}
    print(f"  {media}")
print()
print("First 3 rows — object_number + title:")
for row in rows[:3]:
    print(f"  {row.get('object_number','?')} | {row.get('title','?')[:60]}")

print()
print("=" * 60)
print("FIRESTORE INDUSARRAYS — structure")
print("=" * 60)
ia_path = ROOT / "glossa-corpus/indus/sources/rmrl/raw/indusscript-probe/firestore_indusarrays_full.json"
with open(ia_path, encoding="utf-8") as f:
    data = json.load(f)

dtype = type(data).__name__
dlen = len(data) if isinstance(data, (list, dict)) else "?"
print(f"Type: {dtype}, Length: {dlen}")

if isinstance(data, list) and data:
    print(f"First entry keys: {list(data[0].keys())[:20]}")
    print(f"First entry sample:")
    e = data[0]
    for k in list(e.keys())[:15]:
        print(f"  {k}: {str(e[k])[:80]}")
elif isinstance(data, dict):
    first_key = next(iter(data))
    print(f"First key: {first_key}")
    val = data[first_key]
    if isinstance(val, dict):
        print(f"First value keys: {list(val.keys())[:20]}")
        for k in list(val.keys())[:15]:
            print(f"  {k}: {str(val[k])[:80]}")
    else:
        print(f"First value type: {type(val).__name__}")
        print(f"Sample: {str(val)[:200]}")

print()
print("=" * 60)
print("FIRESTORE INDUSARRAYS JSONL — first 3 lines")
print("=" * 60)
ia_jsonl = ROOT / "glossa-corpus/indus/sources/rmrl/raw/indusscript-probe/firestore_indusarrays_full.jsonl"
with open(ia_jsonl, encoding="utf-8") as f:
    for i, line in enumerate(f):
        if i >= 3:
            break
        obj = json.loads(line)
        print(f"Line {i}: {list(obj.keys())[:15]}")
        for k in ["id", "seal_id", "inscription", "signs", "site", "m77", "holdat", "text"]:
            if k in obj:
                print(f"  {k}: {str(obj[k])[:100]}")
