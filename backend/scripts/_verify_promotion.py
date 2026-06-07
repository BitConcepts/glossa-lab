"""Verify the anchor promotion was done correctly."""
import json, csv
from pathlib import Path
from collections import Counter

REPO = Path(__file__).resolve().parents[2]
fa = json.loads((REPO / "backend/reports/INDUS_FINAL_ANCHORS.json").read_text(encoding="utf-8"))
anchors = fa.get("anchors", {})
coverage = fa.get("corpus_token_coverage", 0)

by_conf = Counter(v.get("confidence", "?") for v in anchors.values())
hm = by_conf.get("HIGH", 0) + by_conf.get("MEDIUM", 0)
print(f"Anchors: {len(anchors)}")
print(f"By confidence: {dict(by_conf)}")
print(f"H+M total: {hm}")
print(f"Declared coverage: {coverage*100:.1f}%")

# Verify coverage independently
holdat = REPO / "corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv"
freq: Counter = Counter()
with open(holdat, encoding="utf-8") as f:
    for row in csv.DictReader(f):
        s = row.get("letters", "").strip()
        if s:
            freq[s] += 1

hm_signs = {sid for sid, info in anchors.items()
            if info.get("confidence", "").upper() in ("HIGH", "MEDIUM")}
total = sum(freq.values())
covered = sum(freq[s] for s in hm_signs if s in freq)
actual = covered / total if total else 0
print(f"Verified coverage: {actual*100:.1f}% ({covered}/{total} tokens)")

if abs(actual - coverage) > 0.01:
    print(f"  ⚠ MISMATCH: declared {coverage*100:.1f}% vs actual {actual*100:.1f}%")
else:
    print(f"  ✓ Coverage matches")

# Phantom check
corpus_signs = set(freq.keys())
phantoms = [s for s in anchors if s not in corpus_signs]
print(f"Phantom anchors: {len(phantoms)}")

# Empty readings
empty = [s for s, i in anchors.items() if not (i.get("reading") or "").strip()]
print(f"Empty readings: {len(empty)}")

# Recently promoted
promoted = [(s, i) for s, i in anchors.items()
            if "Promoted from anchor staging" in (i.get("basis") or "")]
print(f"\nRecently promoted: {len(promoted)}")
if promoted:
    p_conf = Counter(i.get("confidence", "?") for _, i in promoted)
    print(f"  By confidence: {dict(p_conf)}")
    scores = [float(i.get("basis", "").split("score=")[1].split(",")[0])
              for _, i in promoted if "score=" in (i.get("basis") or "")]
    if scores:
        print(f"  Score range: {min(scores):.2f} - {max(scores):.2f}")
        print(f"  Avg score: {sum(scores)/len(scores):.2f}")
        low = sum(1 for s in scores if s < 0.5)
        print(f"  Low score (<0.5): {low}")

print(f"\n{'='*50}")
if len(phantoms) == 0 and len(empty) == 0:
    print("✅ Promotion looks clean")
else:
    print(f"⚠ Issues: {len(phantoms)} phantoms, {len(empty)} empty")
