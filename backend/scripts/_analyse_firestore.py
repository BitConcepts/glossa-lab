"""Analyse Firestore indusarrays for inscription reconstruction potential."""
import json
from pathlib import Path
from collections import defaultdict, Counter

ROOT = Path(__file__).parents[2]
ia = ROOT / "glossa-corpus/indus/sources/rmrl/raw/indusscript-probe/firestore_indusarrays_full.jsonl"
records = [json.loads(l) for l in ia.open(encoding="utf-8") if l.strip()]

# Group by dockey to reconstruct inscriptions
by_doc = defaultdict(list)
for r in records:
    by_doc[r.get("dockey", "?")].append(r)

print(f"Total records: {len(records)}")
print(f"Unique dockeys: {len(by_doc)}")

# *NNN sign analysis
s_fields = ["S1","S2","S3","S4","S5","S6","S7","S8","S9","S10","S11","S12","S13","S14"]
numeric = star = empty = 0
for r in records:
    for sf in s_fields:
        v = r.get(sf, "")
        if not v or v == "0":
            empty += 1
        elif str(v).startswith("*"):
            star += 1
        else:
            numeric += 1

print(f"\nSign value types:")
print(f"  Numeric (Mahadevan): {numeric}")
print(f"  Asterisk (*NNN):     {star}")
print(f"  Empty:               {empty}")
print(f"  *NNN fraction:       {star/(numeric+star)*100:.1f}%")

# How many dockeys have ZERO *NNN signs?
clean_docs = 0
mixed_docs = 0
for dockey, recs in by_doc.items():
    has_star = any(
        str(r.get(sf,"")).startswith("*")
        for r in recs for sf in s_fields
    )
    if has_star:
        mixed_docs += 1
    else:
        clean_docs += 1

print(f"\nDockeys with ZERO *NNN signs (clean): {clean_docs}/{len(by_doc)}")
print(f"Dockeys with some *NNN signs (mixed): {mixed_docs}/{len(by_doc)}")

# Reconstruct sample inscriptions (clean ones only)
print("\nSample reconstructed sequences (filter *NNN, first 10 dockeys):")
count = 0
for dockey in sorted(by_doc.keys())[:50]:
    recs = sorted(by_doc[dockey], key=lambda r: int(r.get("posnum",0) or 0))
    # Use 'texts' field (full sequence stored per record)
    texts_row = recs[0].get("texts", [])
    if texts_row:
        clean = [str(v) for v in texts_row if v and str(v) and not str(v).startswith("*") and str(v) != "0"]
        if len(clean) >= 2:
            print(f"  dockey={dockey}: {clean}")
            count += 1
        if count >= 10:
            break

# Dockey 1001 in detail (Mahadevan concordance M1001)
print("\nDockey 1001 (should be M1001 in Mahadevan concordance):")
docs_1001 = sorted(by_doc.get("1001", []), key=lambda r: int(r.get("posnum",0) or 0))
for r in docs_1001:
    texts = r.get("texts", [])
    clean = [str(v) for v in texts if v and str(v) and str(v) != "0" and not str(v).startswith("*")]
    print(f"  sideline={r.get('sideline')}, posnum={r.get('posnum')}, signnum={r.get('signnum')}")
    print(f"    texts={texts}")
    print(f"    clean={clean}")

# Dockey range
dockeys = [int(d) for d in by_doc.keys() if str(d).isdigit()]
print(f"\nDockey range: {min(dockeys)} - {max(dockeys)}")
print(f"  (Mahadevan 1977 concordance: 1001-8009 approximately)")
