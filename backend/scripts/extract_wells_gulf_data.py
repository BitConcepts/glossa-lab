"""Extract Gulf-context seal data from Wells PhD thesis."""
import json
from pathlib import Path

import fitz

PDF = Path(r"C:\Users\trist\Development\BitConcepts\glossa-lab\corpora\downloads\external_repos\wells_epigraphic_approaches_phd.pdf")
OUT = Path(r"C:\Users\trist\Development\BitConcepts\glossa-lab\corpora\downloads\external_repos\wells_gulf_excerpts.json")

doc = fitz.open(str(PDF))
total = len(doc)
print(f"Loaded: {total} pages")

TERMS = ["Gulf","Bahrain","Dilmun","Ur ","Susa","Failaka","Persian Gulf",
         "fish sign","fish-sign","isolated","sign 55","maritime","Meluhha",
         "Mesopotamia","trade seal","W55","W-55","miin","mi-in","inscription"]

results = []
for pn in range(total):
    text = doc[pn].get_text()
    for term in TERMS:
        if term.lower() in text.lower():
            idx = text.lower().find(term.lower())
            ctx = text[max(0,idx-120):idx+300].replace("\n"," ").strip()
            results.append({"page": pn+1, "term": term, "context": ctx[:350]})

# Deduplicate by (page, term)
seen = set()
unique = []
for r in results:
    k = (r["page"], r["term"])
    if k not in seen:
        seen.add(k)
        unique.append(r)

unique.sort(key=lambda x: x["page"])
print(f"Relevant hits: {len(unique)}")
for r in unique[:60]:
    print(f"  P{r['page']:03d} [{r['term']}]: {r['context'][:120]}")

OUT.write_text(json.dumps(unique, ensure_ascii=False, indent=2))
print(f"\nSaved {len(unique)} excerpts → {OUT}")
doc.close()
