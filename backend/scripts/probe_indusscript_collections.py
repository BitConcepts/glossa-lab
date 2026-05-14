"""Extract Firestore collection names and data paths from indusscript.in Flutter bundle."""
import json
import re
from pathlib import Path

PROBE = Path(__file__).parents[2] / "glossa-corpus" / "indus" / "sources" / "rmrl" / "raw" / "indusscript-probe"
dart_js = PROBE / "main.dart.js"

if not dart_js.exists():
    print("ERROR: main.dart.js not found")
    exit(1)

print(f"Reading {dart_js.name} ({dart_js.stat().st_size:,} bytes)...")
dart = dart_js.read_text(encoding="utf-8", errors="ignore")

# === Pattern 1: .collection("name") calls ===
coll_calls = re.findall(r'\.collection\(["\'](\w+)["\']\)', dart)
print(f"\n=== .collection() calls ({len(coll_calls)}) ===")
for x in sorted(set(coll_calls)):
    print(f"  {x}")

# === Pattern 2: CollectionReference near string literals ===
coll_refs = re.findall(r'CollectionReference[^"\']{0,100}["\']([\w_]{3,50})["\']', dart)
print(f"\n=== CollectionReference-adjacent strings ({len(coll_refs)}) ===")
for x in sorted(set(coll_refs)):
    print(f"  {x}")

# === Pattern 3: LaunchDocuments or similar ===
launch = re.findall(r'LaunchDocuments\w*', dart)
print(f"\n=== LaunchDocuments ({len(launch)}) ===")
for x in sorted(set(launch)):
    print(f"  {x}")

# === Pattern 4: Any string near 'collection' keyword ===
near_coll = re.findall(r'["\'](\w{3,40})["\'][^"\']{0,30}collection', dart, re.IGNORECASE)
near_coll2 = re.findall(r'collection[^"\']{0,30}["\'](\w{3,40})["\']', dart, re.IGNORECASE)
all_near = set(near_coll + near_coll2)
print(f"\n=== Strings near 'collection' keyword ({len(all_near)}) ===")
for x in sorted(all_near):
    print(f"  {x}")

# === Pattern 5: Firestore doc paths ===
doc_paths = re.findall(r'projects/theindusscript/databases[^"\']{0,200}', dart)
print(f"\n=== Firestore project paths ({len(doc_paths)}) ===")
for x in sorted(set(doc_paths)):
    print(f"  {x}")

# === Pattern 6: All text strings that look like Firestore collection names ===
# Firestore collection names are typically snake_case or camelCase lowercase
potential_colls = re.findall(r'["\']([a-z][a-z_]{2,29})["\']', dart)
indus_colls = [c for c in set(potential_colls) if any(kw in c for kw in [
    "text", "sign", "seal", "site", "symbol", "concordance", "inscription",
    "mahadevan", "script", "record", "corpus", "artifact", "object"
])]
print(f"\n=== Potential domain collection names ({len(indus_colls)}) ===")
for x in sorted(indus_colls):
    print(f"  {x}")

# === Summary: all unique short alpha strings that appear frequently (Firestore collection names tend to be reused) ===
alpha_strings = re.findall(r'["\']([a-z][a-zA-Z_0-9]{2,30})["\']', dart)
from collections import Counter
freq = Counter(alpha_strings)
# Firestore collection names appear repeatedly in the bundle
print(f"\n=== Most frequent short alpha strings (potential collection names) ===")
for word, count in freq.most_common(50):
    if count > 5 and len(word) > 3:
        print(f"  {word}: {count}")

# Save full analysis
out = {
    "collection_calls": sorted(set(coll_calls)),
    "collection_ref_adjacent": sorted(set(coll_refs)),
    "near_collection": sorted(all_near),
    "indus_domain_strings": sorted(indus_colls),
    "launch_documents": sorted(set(launch)),
    "top_frequent": [(w, c) for w, c in freq.most_common(100) if c > 5 and len(w) > 3],
}
out_path = PROBE / "firestore_collection_analysis.json"
out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
print(f"\nSaved: {out_path}")
