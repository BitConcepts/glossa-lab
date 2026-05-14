"""Analyze the downloaded indusarrays Firestore collection."""
import json
from pathlib import Path
from collections import Counter

PROBE = Path(__file__).parents[2] / "glossa-corpus" / "indus" / "sources" / "rmrl" / "raw" / "indusscript-probe"

data = json.loads((PROBE / "firestore_indusarrays_full.json").read_text(encoding="utf-8"))
docs = data["documents"]

print(f"Total documents: {len(docs)}")
print(f"Fields: {data['fields']}")
print()

# Sample 5 documents
print("=== Sample documents ===")
for i in [0, 1, 100, 500, 3000]:
    d = docs[i]
    shown = {k: v for k, v in d.items() if v not in (None, "", [], {}) and not k.startswith("_")}
    print(f"Doc {d['_id']} textnum={d.get('textnum')} posnum={d.get('posnum')} signnum={d.get('signnum')}:")
    print(f"  {json.dumps(shown, ensure_ascii=False)[:500]}")
    print()

# Count unique textnums
textnums = [d.get("textnum") for d in docs if d.get("textnum")]
unique_textnums = set(textnums)
print(f"Unique textnums: {len(unique_textnums)}")
print(f"textnum range: {min(unique_textnums)} – {max(unique_textnums)}")

# Count docs with texts array
with_texts = [d for d in docs if d.get("texts") and any(t for t in d.get("texts", []) if t)]
print(f"Docs with non-empty texts array: {len(with_texts)}")

if with_texts:
    print(f"Sample texts arrays:")
    for d in with_texts[:3]:
        texts = [t for t in d.get("texts", []) if t]
        print(f"  textnum={d.get('textnum')} posnum={d.get('posnum')}: {texts}")

# Count docs with S1-S14 sign data
with_signs = [d for d in docs if any(d.get(f"S{i}") for i in range(1, 15))]
print(f"\nDocs with S1-S14 sign data: {len(with_signs)}")
if with_signs:
    d = with_signs[0]
    signs = {f"S{i}": d[f"S{i}"] for i in range(1, 15) if d.get(f"S{i}")}
    print(f"  Sample: {signs}")

# Count docs per textnum (to understand structure)
textnum_counts = Counter(d.get("textnum") for d in docs if d.get("textnum"))
most_common = textnum_counts.most_common(5)
print(f"\nMost repeated textnums: {most_common}")
single_docs = sum(1 for v in textnum_counts.values() if v == 1)
print(f"Textnums with exactly 1 doc: {single_docs} / {len(unique_textnums)}")

# Check posnum distribution
posnums = [d.get("posnum") for d in docs if d.get("posnum") is not None]
if posnums:
    print(f"\nposnum range: {min(posnums)} – {max(posnums)}")
    print(f"posnum distribution (value counts): {sorted(Counter(posnums).most_common(10))}")
