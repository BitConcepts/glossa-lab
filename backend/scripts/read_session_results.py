"""Read the latest session experiment results."""
import json
from pathlib import Path
REPORTS = Path(__file__).parent.parent.parent / "reports"

def get(fname):
    p = REPORTS / fname
    if not p.exists(): return {}
    d = json.loads(p.read_text())
    return d.get("data", d)

r5  = get("indus_cisi_anchored_5.json")
r6  = get("indus_cisi_anchored_6_ko.json")
rdb = get("indus_cisi_sa_anchorset.json")

print("ANCHOR CONVERGENCE TABLE:")
print(f"  {'Experiment':<40} cons    HCI%")
for label, r in [
    ("5-anchor (P385=n,P324=k,P122=a,P086=m,P060=i)", r5),
    ("6-anchor (+P332=o ko-vowel)",                   r6),
    ("AnchorSetLoader (DB, same 5 anchors)",           rdb),
]:
    print(f"  {label:<40} {r.get('a','?')}  {r.get('b','?')}")

print()
print("6-anchor non-'a' mappings:")
for k, v in r6.items():
    if k.startswith("c__") and v not in ("a",):
        print(f"  {k[3:]}: {v}")

# Reading attempt with 6-anchor map
corpus = json.loads((Path(__file__).parent.parent.parent / "data" / "indus_cisi_corpus.json").read_text())
map6 = {k[3:]:v for k,v in r6.items() if k.startswith("c__")}
anchor_known = {"P385":"n","P324":"k","P122":"a","P086":"m","P060":"i","P332":"o"}
for sign, ph in anchor_known.items():
    map6[sign] = ph

WORDS = {"kon":["kill/take Tamil koN"],"kan":["eye Tamil kan"],"man":["earth Tamil man"],
         "maan":["deer Tamil maan"],"pon":["gold Tamil pon"],"van":["sky Tamil van"],
         "koian":["cowherd?"],"koan":["related to ko"],"koman":["king's man?"],
         "ko":["king DEDR 2147"],"mako":["great king?"],"nako":["name?"],
         "kona":["angle Tamil koNam"],"koman":["Tamil name/title"],
         "oman":["?"],"ona":["one Tamil oru"],"iman":["this earth Tamil im+man"],
         "mana":["mind Tamil manas"],"maran":["tree Tamil maram"]}

print("\nTop inscriptions readable with 6-anchor map (P332=o):")
readable = []
for insc in corpus:
    signs = [g["id"] for g in insc.get("graphemes",[]) if g.get("id")]
    if len(signs) < 2: continue
    ph = [map6.get(s,"?") for s in signs]
    anchored = sum(1 for p in ph if p!="?")
    cov = anchored/len(signs)
    if cov < 0.45: continue
    ps = "".join(p for p in ph if p!="?")
    full = "".join(ph)
    matches = [f"{w}:{g[0][:25]}" for w,g in WORDS.items() if w in ps]
    readable.append((insc["id"], signs, full, ps, cov, matches))

readable.sort(key=lambda x: -x[4])
for iid, signs, full, ps, cov, matches in readable[:20]:
    mstr = f"  [{', '.join(matches[:2])}]" if matches else ""
    print(f"  {iid:8s}  {full:22s}  ({cov*100:.0f}%){mstr}")
