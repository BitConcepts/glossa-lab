"""Read and interpret the 4 CISI decipherment experiment results."""
import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

REPORTS = Path(__file__).parent.parent.parent / "reports"

def read(fname):
    p = REPORTS / fname
    if not p.exists():
        print(f"  MISSING: {fname}"); return {}
    return json.loads(p.read_text())

def flatten(d, depth=0):
    """Recursively flatten nested dicts, stopping at primitives."""
    if depth > 3: return
    for k, v in d.items():
        if isinstance(v, (str, int, float, bool)):
            print(f"  {k}: {v}")
        elif isinstance(v, dict):
            # Inline small dicts
            if len(v) <= 6 and all(isinstance(vv, (str,int,float,bool)) for vv in v.values()):
                print(f"  {k}: {dict(list(v.items())[:6])}")
            else:
                print(f"  {k}:")
                flatten(v, depth+1)
        elif isinstance(v, list) and v:
            first = str(v[0])[:80]
            print(f"  {k}: [n={len(v)}] {first}")

def show(name, d):
    print(f"\n{'='*60}\n  {name}\n{'='*60}")
    if not d:
        print("  (empty)"); return
    # Saved files have top-level keys from the Merger's inputs - navigate 'data' if present
    top = d.get("data", d) if isinstance(d, dict) else d
    if not isinstance(top, dict):
        print(f"  raw: {str(d)[:200]}"); return
    flatten(top)

# 1. SA A/B: Dravidian vs Sanskrit on CISI
d1 = read("indus_cisi_dravidian_vs_sanskrit.json")
show("SA A/B: Dravidian vs Sanskrit (CISI real bigrams)", d1)

# 2. Anchored 2
d2 = read("indus_cisi_anchored_2.json")
show("Anchored SA 2 (P385=n, P324=k)", d2)

# 3. Anchored 5
d3 = read("indus_cisi_anchored_5.json")
show("Anchored SA 5 (P385=n,P324=k,P122=a,P086=m,P060=i)", d3)

# 4. CAS bigram
d4 = read("indus_cas_bigram_phoneme.json")
show("CAS Bigram Phoneme (P122->P385 genitive)", d4)

print("\n" + "="*60)
print("SUMMARY TABLE")
print("="*60)
for name, d in [
    ("SA A/B Dravidian",   d1),
    ("Anchored 2",         d2),
    ("Anchored 5",         d3),
    ("CAS Bigram",         d4),
]:
    inner = d.get("json", d) if isinstance(d, dict) else {}
    b = inner.get("b", inner.get("b__dravidian_score", "?"))
    c = inner.get("c", inner.get("c__classification", "?"))
    print(f"  {name:<38} b={b}  c={c}")
