"""Verify the downloaded CISI corpus statistics."""
import json
from collections import Counter
from pathlib import Path
from statistics import mean

data = json.loads(Path("C:/Users/trist/Development/BitConcepts/glossa-lab/data/indus_cisi_corpus.json").read_text())
print(f"Total inscription sides: {len(data)}")

for insc in data[:3]:
    signs = [g["id"] for g in insc.get("graphemes", [])]
    print(f"  {insc['id']:8s}  {insc['description'][:30]:30s}  signs={signs}")

all_signs = [g["id"] for insc in data for g in insc.get("graphemes", [])]
sign_freq = Counter(all_signs)
print(f"Total sign tokens: {len(all_signs)}")
print(f"Distinct signs (Parpola): {len(sign_freq)}")

lengths = [len(insc.get("graphemes", [])) for insc in data]
print(f"Inscription lengths: mean={mean(lengths):.1f}, min={min(lengths)}, max={max(lengths)}")
multi = [l for l in lengths if l >= 2]
print(f"Multi-sign inscriptions (>=2): {len(multi)} ({100*len(multi)/len(lengths):.0f}%)")
print(f"Top 10 most frequent Parpola signs: {sign_freq.most_common(10)}")

sites = Counter(insc["id"].split("-")[0] for insc in data)
print(f"Sites: {dict(sites)}")
