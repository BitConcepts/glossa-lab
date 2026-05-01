"""Inspect phase32 extractions: contexts for top signs + DEDR cases."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
d = json.loads((ROOT / "backend" / "glossa_lab" / "data"
                  / "mahadevan_papers_extracted.json").read_text(encoding="utf-8"))

print("=== Top sign 48 contexts (first 3) ===")
for ev in d["sign_evidence"]["48"][:3]:
    print(f"[{ev['paper_id']} p{ev['page']}]")
    print(f"  {ev['context'][:400]}")
    print()

print("=== Top sign 47 contexts (first 2) ===")
for ev in d["sign_evidence"]["47"][:2]:
    print(f"[{ev['paper_id']} p{ev['page']}]")
    print(f"  {ev['context'][:400]}")
    print()

print("=== Sample DEDR contexts (first 5 cases) ===")
for did, items in list(d["dedr_word_index"].items())[:5]:
    for it in items[:1]:
        print(f"DEDR {did} -> word={it['word']}")
        print(f"  ctx: {it['context'][:400]}")
        print()
