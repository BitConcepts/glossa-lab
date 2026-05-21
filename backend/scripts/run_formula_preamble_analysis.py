"""Formula preamble analysis — authored by Glossa AI via glossa_chat.py.

Analyses the Indus seal formula:
  [PREAMBLE signs] [407=title] [CASE MARKER: 705/806/798] [845=category] ([900=seal mark])

Profiles preamble signs 235, 321, 850, 61, 240 plus context signs 415, 585.
Results saved to reports/formula_preamble_analysis.json.

Tooling fix applied by Oz: variable name collision s→sign in compute_contexts
(line was: ins.index(s) — should be: ins.index(sign))
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

R = Path(__file__).parent.parent / "reports"

# ── Load corpus ────────────────────────────────────────────────────────────────

data = json.loads((R / "icit_extracted_corpus.json").read_text("utf-8"))
inscriptions = [i["sequence"] for i in data["inscriptions"] if i.get("sequence")]

total_c    = Counter(s for ins in inscriptions for s in ins)
terminal_c = Counter(ins[-1] for ins in inscriptions if len(ins) > 1)
initial_c  = Counter(ins[0]  for ins in inscriptions if len(ins) > 1)
medial_c   = Counter(s for ins in inscriptions for s in ins[1:-1])

left_ctx: dict[str, Counter] = defaultdict(Counter)
right_ctx: dict[str, Counter] = defaultdict(Counter)
for ins in inscriptions:
    for j, s in enumerate(ins):
        if j > 0:
            left_ctx[s][ins[j - 1]] += 1
        if j < len(ins) - 1:
            right_ctx[s][ins[j + 1]] += 1

# ── Classification ────────────────────────────────────────────────────────────


def classify(sign: str) -> str:
    n = total_c.get(sign, 0)
    if n == 0:
        return "UNKNOWN"
    t = terminal_c.get(sign, 0) / n
    i = initial_c.get(sign, 0) / n
    m = medial_c.get(sign, 0) / n
    if t >= 0.60:
        return "TMK"
    if i >= 0.50:
        return "INITIAL"
    if m >= 0.65:
        return "MEDIAL"
    return "MIXED"


def profile(sign: str) -> dict:
    n = total_c.get(sign, 0)
    if n == 0:
        return {"total": 0, "t": 0.0, "i": 0.0, "m": 0.0}
    return {
        "total": n,
        "t": round(terminal_c.get(sign, 0) / n, 3),
        "i": round(initial_c.get(sign, 0) / n, 3),
        "m": round(medial_c.get(sign, 0) / n, 3),
    }


# ── Analyse preamble signs ────────────────────────────────────────────────────

# Signs to analyse: preamble + known formula context signs
SIGNS = ["235", "321", "850", "61", "240", "415", "585"]

results = {}
print("=" * 75)
print("FORMULA PREAMBLE ANALYSIS")
print("Formula: [PREAMBLE][407=title][CASE:705/806/798][845=category][900=seal]")
print("=" * 75)
print(f"{'Sign':>5}  {'n':>5}  {'T':>6}  {'I':>6}  {'M':>6}  {'Class':<9}  {'Top left ctx':<25}  {'Top right ctx'}")
print("-" * 100)

for sign in SIGNS:
    p = profile(sign)
    cat = classify(sign)
    lc = dict(left_ctx[sign].most_common(5))
    rc = dict(right_ctx[sign].most_common(5))
    lc_str = " ".join(f"{k}({v})" for k, v in list(lc.items())[:4])
    rc_str = " ".join(f"{k}({v})" for k, v in list(rc.items())[:4])
    print(f"{sign:>5}  {p['total']:>5}  {p['t']:>6.3f}  {p['i']:>6.3f}  {p['m']:>6.3f}  {cat:<9}  {lc_str:<25}  {rc_str}")
    results[sign] = {
        "profile": p,
        "classification": cat,
        "left_ctx": dict(left_ctx[sign].most_common(8)),
        "right_ctx": dict(right_ctx[sign].most_common(8)),
    }

# ── Frequency of full formula appearances ────────────────────────────────────

print("\nMOST COMMON INSCRIPTIONS CONTAINING SIGN 407:")
formula_ins = Counter(tuple(ins) for ins in inscriptions if "407" in ins)
for seq, cnt in formula_ins.most_common(12):
    print(f"  x{cnt:>3}  {list(seq)}")

# ── Save results ──────────────────────────────────────────────────────────────

out = R / "formula_preamble_analysis.json"
out.write_text(json.dumps(results, indent=2), "utf-8")
print(f"\nSaved → {out}")
