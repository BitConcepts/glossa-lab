"""Deep inspection: Penn CSV identifiers + Firestore indusarrays catalog alignment."""
import csv, json
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).parents[2]

# ─── 1. Penn CSV identifier format ────────────────────────────────────────────
print("=" * 60)
print("PENN CSV — identifier column samples")
print("=" * 60)
penn_csv = ROOT / "glossa-corpus/indus/sources/penn-museum/raw/2026-05-14/penn_indus_filtered.csv"
penn_rows = []
with open(penn_csv, encoding="utf-8", errors="replace") as f:
    reader = csv.DictReader(f)
    for row in reader:
        penn_rows.append(row)

print(f"Total Indus rows: {len(penn_rows)}")
# Show identifier samples
ids = [r.get("identifier","") for r in penn_rows[:20]]
print(f"identifier samples: {ids}")
urls = [r.get("Record URL","") for r in penn_rows[:5]]
print(f"Record URL samples: {urls}")
# Check if identifier matches the object ID in Record URL
mismatches = 0
for r in penn_rows[:100]:
    url = r.get("Record URL","")
    ident = r.get("identifier","")
    url_id = url.rstrip("/").split("/")[-1] if url else ""
    if url_id and ident and url_id != ident:
        mismatches += 1
print(f"identifier vs URL_id mismatches (first 100 rows): {mismatches}")

print()
# ─── 2. Firestore full JSON — all top-level keys ───────────────────────────────
print("=" * 60)
print("FIRESTORE INDUSARRAYS JSON — all keys")
print("=" * 60)
ia_json = ROOT / "glossa-corpus/indus/sources/rmrl/raw/indusscript-probe/firestore_indusarrays_full.json"
with open(ia_json, encoding="utf-8") as f:
    data = json.load(f)

print(f"Top-level keys ({len(data)}): {list(data.keys())}")
for k, v in data.items():
    if isinstance(v, list):
        print(f"  '{k}': list of {len(v)} items")
        if v:
            print(f"    First item keys: {list(v[0].keys()) if isinstance(v[0], dict) else type(v[0]).__name__}")
    elif isinstance(v, dict):
        print(f"  '{k}': dict with {len(v)} keys: {list(v.keys())[:10]}")
    else:
        print(f"  '{k}': {type(v).__name__} = {str(v)[:100]}")

print()
# ─── 3. JSONL — sign field analysis ──────────────────────────────────────────
print("=" * 60)
print("FIRESTORE INDUSARRAYS JSONL — sign field analysis")
print("=" * 60)
ia_jsonl = ROOT / "glossa-corpus/indus/sources/rmrl/raw/indusscript-probe/firestore_indusarrays_full.jsonl"
records = []
with open(ia_jsonl, encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line:
            records.append(json.loads(line))

print(f"Total JSONL records: {len(records)}")
all_keys = set()
for r in records:
    all_keys.update(r.keys())
print(f"All field names: {sorted(all_keys)}")

# Sample sign values from S1..S14 and signnum
print("\nSample S-field values (first 10 records):")
s_fields = sorted([k for k in all_keys if k.startswith("S") and k[1:].isdigit()])
print(f"  Sign position fields: {s_fields}")
for r in records[:5]:
    signs = {k: r[k] for k in s_fields if k in r}
    signnum = r.get("signnum")
    dockey = r.get("dockey")
    inscobj = r.get("inscobj")
    print(f"  signnum={signnum}, dockey={dockey}, inscobj={str(inscobj)[:30]}, signs={signs}")

# Count unique sign values
print("\nSign value distribution (S1..S14 across all records):")
sign_vals = []
for r in records:
    for k in s_fields:
        v = r.get(k)
        if v is not None and v != "" and v != 0:
            sign_vals.append(v)
cnt = Counter(sign_vals)
print(f"  Total sign instances: {len(sign_vals)}")
print(f"  Unique sign values: {len(cnt)}")
print(f"  Top-20 most frequent signs: {cnt.most_common(20)}")
print(f"  Min/max sign value: {min(sign_vals)}, {max(sign_vals)}")

print()
# ─── 4. Compare with Holdat sign IDs from indus_research.jsonl ───────────────
print("=" * 60)
print("CATALOG ALIGNMENT: Holdat vs indusarrays sign IDs")
print("=" * 60)
jl = ROOT / "glossa-corpus/indus/exports/indus_research.jsonl"
holdat_signs = set()
with open(jl, encoding="utf-8") as f:
    for line in f:
        obj = json.loads(line)
        ids_list = obj.get("canonical_grapheme_ids", [])
        for s in ids_list:
            try:
                holdat_signs.add(int(s))
            except (ValueError, TypeError):
                pass

ia_signs = set(sign_vals) if isinstance(list(cnt.keys())[0], int) else set()
print(f"Holdat unique sign IDs: {len(holdat_signs)}, range: {min(holdat_signs)}-{max(holdat_signs)}")
print(f"indusarrays unique sign vals: {len(set(sign_vals))}, sample: {sorted(set(sign_vals))[:20]}")
if ia_signs:
    overlap = holdat_signs & ia_signs
    print(f"Overlap (same integer ID): {len(overlap)}/{max(len(holdat_signs),len(ia_signs))}")
    print(f"In Holdat but not indusarrays: {len(holdat_signs - ia_signs)}")
    print(f"In indusarrays but not Holdat: {len(ia_signs - holdat_signs)}")
