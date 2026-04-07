import json
from collections import Counter
from pathlib import Path

R = Path(__file__).parent.parent / "reports"
corpus_data = json.loads((R / "icit_extracted_corpus.json").read_text("utf-8"))
inscriptions = [i["sequence"] for i in corpus_data["inscriptions"] if i.get("sequence")]

KNOWN = {
    "817": "-um", "920": "-e", "760": "-il", "798": "-ku", "752": "-in",
    "72": "meen(fish)", "70": "meen(fish)", "400": "a-(bull)",
    "520": "a-(arrow)", "32": "ka/stroke", "220": "maa?",
}

total_c    = Counter(s for ins in inscriptions for s in ins)
terminal_c = Counter(ins[-1] for ins in inscriptions if len(ins) > 1)
initial_c  = Counter(ins[0]  for ins in inscriptions if len(ins) > 1)
medial_c   = Counter(s for ins in inscriptions for s in ins[1:-1])


def profile(sign):
    n = total_c.get(sign, 0)
    if not n:
        return None
    t = terminal_c.get(sign, 0) / n
    i = initial_c.get(sign, 0) / n
    m = medial_c.get(sign, 0) / n
    lc, rc = Counter(), Counter()
    for ins in inscriptions:
        for j, s in enumerate(ins):
            if s == sign:
                if j > 0:
                    lc[ins[j - 1]] += 1
                if j < len(ins) - 1:
                    rc[ins[j + 1]] += 1
    solo = sum(1 for ins in inscriptions if ins == [sign])
    return {"n": n, "t": round(t, 3), "i": round(i, 3), "m": round(m, 3),
            "solo": solo, "left": dict(lc.most_common(8)), "right": dict(rc.most_common(8))}


for sign in ["806", "705", "900"]:
    p = profile(sign)
    if not p:
        print(f"Sign {sign}: not in corpus")
        continue
    known = KNOWN.get(sign, "UNASSIGNED")
    cat = ("TMK" if p["t"] >= 0.60 else
           "INIT" if p["i"] >= 0.50 else
           "MED"  if p["m"] >= 0.65 else "MIXED")
    print(f"Sign {sign} ({known}): n={p['n']}  T={p['t']}  I={p['i']}  M={p['m']}  solo={p['solo']}  cat={cat}")
    print(f"  Left:  {p['left']}")
    print(f"  Right: {p['right']}")
    print()

print("--- Inscriptions with 806 immediately before 845 ---")
found = 0
for ins in inscriptions:
    for j in range(len(ins) - 1):
        if ins[j] == "806" and ins[j + 1] == "845":
            print(f"  {ins}")
            found += 1
            if found >= 8:
                break
    if found >= 8:
        break
print(f"  Total bigrams: {found}")

print()
print("--- Inscriptions with 705 immediately before 845 ---")
found2 = 0
for ins in inscriptions:
    for j in range(len(ins) - 1):
        if ins[j] == "705" and ins[j + 1] == "845":
            print(f"  {ins}")
            found2 += 1
            if found2 >= 8:
                break
    if found2 >= 8:
        break
print(f"  Total bigrams: {found2}")

print()
print("--- Inscriptions with 798 immediately before 845 ---")
found3 = 0
for ins in inscriptions:
    for j in range(len(ins) - 1):
        if ins[j] == "798" and ins[j + 1] == "845":
            print(f"  {ins}")
            found3 += 1
            if found3 >= 8:
                break
    if found3 >= 8:
        break
print(f"  Total bigrams: {found3}")
