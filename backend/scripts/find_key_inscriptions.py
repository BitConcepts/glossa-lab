"""Find key inscriptions: M-314 (17-sign seal), M-494/M-495 (26-sign amulet), Dholavira seals."""
import csv
from collections import defaultdict

path = r"C:\Users\trist\Development\BitConcepts\glossa-lab\corpora\downloads\external_repos\holdatllc_indus\indus_corpus 2.csv"
seals = defaultdict(list)
with open(path, encoding="utf-8") as f:
    for r in csv.DictReader(f):
        seals[r["cisi_number"]].append(r)

print(f"Total unique seals: {len(seals)}")

# Search for key inscriptions
targets = ["M-0314", "M-314", "M-0494", "M-494", "M-0495", "M-495"]
for t in targets:
    if t in seals:
        signs = seals[t]
        sign_str = " ".join(s["letters"] for s in signs)
        print(f"{t}: n={len(signs)} signs: {sign_str}  site={signs[0]['site']}  icon={signs[0]['iconography']}")
    else:
        print(f"{t}: NOT FOUND")

# Dholavira entries
dk_seals = {k: v for k, v in seals.items() if k.startswith("DK-")}
print(f"\nDholavira seals: {len(dk_seals)}")
dk_by_len = sorted(dk_seals.items(), key=lambda x: len(x[1]), reverse=True)
for cisi, signs in dk_by_len[:10]:
    sign_str = " ".join(s["letters"] for s in signs)
    print(f"  {cisi}: n={len(signs)} {sign_str}")

# Also search for any seal with 'signboard' or high sign count
print("\nAll seals with >= 7 signs:")
for cisi, signs in sorted(seals.items(), key=lambda x: len(x[1]), reverse=True):
    if len(signs) >= 7:
        sign_str = " ".join(s["letters"] for s in signs)
        print(f"  {cisi}: n={len(signs)} site={signs[0]['site']} {sign_str}")
