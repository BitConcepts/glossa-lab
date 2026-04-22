"""Compare SA results: P324='k' (original) vs P324='o' (corrected)."""
import json
from pathlib import Path

REPORTS = Path(__file__).parent.parent.parent / "reports"

def load(fname):
    p = REPORTS / fname
    if not p.exists(): return {}
    d = json.loads(p.read_text())
    return d.get("data", d)

k_result = load("indus_cisi_anchored_5.json")
o_result = load("indus_cisi_anchored_5_o.json")

k_cons = k_result.get("a", "?")
o_cons = o_result.get("a", "?")
k_hci  = k_result.get("b", "?")
o_hci  = o_result.get("b", "?")

print("COMPARISON: P324='k' vs P324='o'")
print("="*50)
print(f"  P324='k' (original)  consistency={k_cons}  HCI={k_hci}")
print(f"  P324='o' (corrected) consistency={o_cons}  HCI={o_hci}")
try:
    delta = float(o_cons) - float(k_cons)
    print(f"  Delta: {delta:+.4f} ({'P324=o better' if delta>0 else 'P324=k better'})")
except:
    pass

print()
print("Non-'a' mappings with P324='o':")
for k, v in o_result.items():
    if k.startswith("c__") and v != "a":
        print(f"  {k[3:]}: {v}")

# Interesting inscriptions with 'o' reading
print()
print("Inscriptions with 'on' pattern (P324+P385 = o+n = 'on'/genitive-of-ko):")
corpus_file = Path(__file__).parent.parent.parent / "data" / "indus_cisi_corpus.json"
corpus = json.loads(corpus_file.read_text())
anchor_o = {"P385":"n","P324":"o","P122":"a","P086":"m","P060":"i"}
for insc in corpus:
    signs = [g["id"] for g in insc.get("graphemes",[]) if g.get("id")]
    phonemes = [anchor_o.get(s,"?") for s in signs]
    ps = "".join(p for p in phonemes if p!="?")
    if "on" in ps or "om" in ps or "oi" in ps:
        full = "".join(phonemes)
        print(f"  {insc['id']:8s}  {signs}  -> '{full}'  (anchored: '{ps}')")
