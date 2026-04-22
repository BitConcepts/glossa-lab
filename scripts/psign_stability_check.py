"""Quick P-sign-only cross-site class stability check."""
import csv
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def classify(er, sr, ir, f, min_f):
    if f == 1: return "HAPAX"
    if f < min_f: return "LOW_FREQ"
    if er >= 0.55: return "TERMINAL"
    if sr >= 0.55: return "INITIAL"
    if ir >= 0.70: return "MEDIAL"
    if sr >= 0.30 and er >= 0.30 and ir < 0.30: return "BIMODAL"
    return "MIXED"

with open(ROOT / "data_normalized" / "corpus_master.csv", newline="", encoding="utf-8") as f:
    records = list(csv.DictReader(f))

by_site: dict = defaultdict(list)
for r in records:
    by_site[r["site"]].append(r)

SITES = {s: recs for s, recs in by_site.items() if len(recs) >= 20}
sign_classes: dict = defaultdict(dict)

print("Per-site P-sign class distribution:")
for site, recs in sorted(SITES.items(), key=lambda x: -len(x[1])):
    n = len(recs)
    min_f = max(2, n // 30)
    freq: Counter = Counter()
    sf: Counter = Counter()
    ef: Counter = Counter()
    intf: Counter = Counter()
    for r in recs:
        seq = r["sign_sequence_raw"].split()
        for i, s in enumerate(seq):
            if not s.startswith("P"):
                continue
            freq[s] += 1
            if i == 0: sf[s] += 1
            elif i == len(seq)-1: ef[s] += 1
            else: intf[s] += 1
    classes: Counter = Counter()
    for sign, f in freq.items():
        cls = classify(ef[sign]/f, sf[sign]/f, intf[sign]/f, f, min_f)
        classes[cls] += 1
        sign_classes[sign][site] = cls
    print(f"  {site:20s} N={n:4d} min_f={min_f:2d} P-signs={len(freq):3d}: {dict(classes)}")

multi_site = {s: d for s, d in sign_classes.items() if len(d) >= 2}
stable = sum(1 for d in multi_site.values() if len(set(d.values())) == 1)
rate = round(100*stable/len(multi_site), 1) if multi_site else 0
print(f"\nP-sign-only multi-site signs: {len(multi_site)}")
print(f"Stable class across all sites: {stable}")
print(f"Stability rate (P-signs only): {rate}%")

# Show which classes are stable
stable_classes: Counter = Counter()
for d in multi_site.values():
    cls_set = set(d.values())
    if len(cls_set) == 1:
        stable_classes[list(cls_set)[0]] += 1
print(f"Stable class breakdown: {dict(stable_classes)}")
