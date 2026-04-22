"""Read all new experiment results for this session."""
import json
from pathlib import Path

REPORTS = Path(__file__).parent.parent.parent / "reports"

def get(fname):
    p = REPORTS / fname
    if not p.exists(): return {}
    d = json.loads(p.read_text())
    return d.get("data", d)

# 10-anchor SA
d10 = get("indus_cisi_anchored_10.json")
print("10-ANCHOR SA:")
print(f"  consistency (a): {d10.get('a', '?')}")
print(f"  HCI% (b):        {d10.get('b', '?')}")
print(f"  Non-'a' mappings: {len({k:v for k,v in d10.items() if k.startswith('c__') and v!='a'})}")

# Dravidian vs Pali on CISI
dpali = get("indus_cisi_dravidian_vs_pali.json")
print("\nDRAVIDIAN vs PALI (CISI real bigrams):")
print(f"  H1 (a):              {dpali.get('a','?')}")
print(f"  Dravidian cons (b):  {dpali.get('b','?')}")
print(f"  Pali cons (c):       {dpali.get('c','?')}")
if 'b' in dpali and 'c' in dpali:
    try: print(f"  Gap:                 +{float(dpali['b'])-float(dpali['c']):.4f}pp")
    except: pass

# cas_sign_roles
roles = get("indus_cas_sign_roles.json")
print("\nCAS SIGN ROLES (CPSC engine):")
inner = roles.get("json", roles)
for k,v in inner.items():
    if k in ("a","b","c","d","e"):
        print(f"  {k}: {str(v)[:80]}")

print("\nSUMMARY TABLE (all CISI decipherment experiments):")
print(f"  {'Experiment':<42} consistency  HCI%")
for label, fname, ck, hk in [
    ("Baseline (0 anchors)",      "indus_cisi_dravidian_vs_sanskrit.json", "b", None),
    ("Anchored 2 (P385=n,P324=k)","indus_cisi_anchored_2.json",            "a", "b"),
    ("Anchored 5 (+P122,P086,P060)","indus_cisi_anchored_5.json",          "a", "b"),
    ("Anchored 10 (max evidence)", "indus_cisi_anchored_10.json",           "a", "b"),
]:
    d = get(fname)
    c = d.get(ck, "?")
    h = d.get(hk, "-") if hk else "-"
    print(f"  {label:<42} {c}   {h}")
