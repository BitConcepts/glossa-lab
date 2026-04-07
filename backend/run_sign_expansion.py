"""Sign expansion session.

  1. Identify signs 48, 503, 615 (dominate genitive patterns)
  2. Test 'maa-' as reading for sign 220 (too frequent for 'tree')
  3. Expand M77 inventory to map top-100 Fuls signs
  4. Comprehensive sign reading table
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

R = Path(__file__).parent.parent / "reports"
DI = Path(__file__).parent.parent / "data-import"

corpus_data = json.loads((R / "icit_extracted_corpus.json").read_text("utf-8"))
inscriptions_raw = corpus_data["inscriptions"]
inscriptions = [i["sequence"] for i in inscriptions_raw if i.get("sequence")]
freq_all = Counter(s for ins in inscriptions for s in ins)

terminal_c: Counter = Counter()
initial_c: Counter = Counter()
medial_c: Counter = Counter()
solo_c: Counter = Counter()
total_c: Counter = Counter()
for ins in inscriptions:
    total_c.update(ins)
    if len(ins) == 1:
        solo_c[ins[0]] += 1
    else:
        initial_c[ins[0]] += 1
        terminal_c[ins[-1]] += 1
        for s in ins[1:-1]:
            medial_c[s] += 1


def pp(s: str) -> dict:
    n = total_c.get(s, 0)
    if n == 0:
        return {"total": 0, "t_rate": 0.0, "i_rate": 0.0, "m_rate": 0.0, "solo": 0}
    return {"total": n, "solo": solo_c.get(s, 0),
            "t_rate": round(terminal_c.get(s, 0) / n, 3),
            "i_rate": round(initial_c.get(s, 0) / n, 3),
            "m_rate": round(medial_c.get(s, 0) / n, 3)}


left_ctx: dict[str, Counter] = defaultdict(Counter)
right_ctx: dict[str, Counter] = defaultdict(Counter)
for ins in inscriptions:
    for j, s in enumerate(ins):
        if j > 0:
            left_ctx[s][ins[j - 1]] += 1
        if j < len(ins) - 1:
            right_ctx[s][ins[j + 1]] += 1

# Full M77 reference — expanded from Mahadevan (1977) frequency tables
# These profiles are from M77 pp.727-755 (sign frequency statistics)
M77_FULL: dict[str, dict] = {
    # Stroke signs (numerals/counters)
    "001": {"t": 0.642, "i": 0.090, "m": 0.246, "n": 134, "desc": "Short stroke (TMK)"},
    "002": {"t": 0.333, "i": 0.333, "m": 0.333, "n": 21,  "desc": "Two strokes"},
    "003": {"t": 0.500, "i": 0.167, "m": 0.333, "n": 6,   "desc": "Three strokes"},
    "004": {"t": 1.000, "i": 0.000, "m": 0.000, "n": 2,   "desc": "Four strokes"},
    "005": {"t": 0.000, "i": 0.019, "m": 0.981, "n": 105, "desc": "Six strokes (MEDIAL)"},
    "006": {"t": 0.500, "i": 0.000, "m": 0.500, "n": 6,   "desc": "Vertical+horizontal"},
    "007": {"t": 0.500, "i": 0.083, "m": 0.417, "n": 12,  "desc": "Short+long stroke"},
    "008": {"t": 0.600, "i": 0.100, "m": 0.300, "n": 10,  "desc": "Three vertical strokes"},
    # Circle/ring signs
    "010": {"t": 0.600, "i": 0.200, "m": 0.200, "n": 5,   "desc": "Circle"},
    "012": {"t": 0.863, "i": 0.013, "m": 0.125, "n": 80,  "desc": "Small circle (TMK)"},
    "013": {"t": 0.730, "i": 0.008, "m": 0.262, "n": 126, "desc": "Large circle"},
    # Prickle/thorn signs
    "017": {"t": 0.045, "i": 0.045, "m": 0.909, "n": 22,  "desc": "Prickle/thorns"},
    "019": {"t": 0.059, "i": 0.118, "m": 0.824, "n": 17,  "desc": "Prickle variant"},
    # Arrow/stroke initial signs
    "026": {"t": 0.062, "i": 0.813, "m": 0.125, "n": 16,  "desc": "Arrow variant (initial)"},
    "028": {"t": 0.044, "i": 0.923, "m": 0.033, "n": 91,  "desc": "Arrow (strong initial)"},
    # Comb/rake signs (medial)
    "029": {"t": 0.030, "i": 0.101, "m": 0.869, "n": 168, "desc": "Comb/rake (medial)"},
    "030": {"t": 0.038, "i": 0.077, "m": 0.885, "n": 26,  "desc": "Comb variant"},
    "031": {"t": 0.052, "i": 0.052, "m": 0.897, "n": 58,  "desc": "Comb with base"},
    "032": {"t": 0.025, "i": 0.175, "m": 0.800, "n": 40,  "desc": "Comb+cross"},
    # Fish signs (medial family)
    "059": {"t": 0.047, "i": 0.094, "m": 0.812, "n": 381, "desc": "Fish (M059)"},
    "060": {"t": 0.062, "i": 0.046, "m": 0.831, "n": 130, "desc": "Fish+arrow tail"},
    "062": {"t": 0.036, "i": 0.071, "m": 0.893, "n": 28,  "desc": "Fish+2 strokes"},
    "063": {"t": 0.048, "i": 0.048, "m": 0.905, "n": 21,  "desc": "Fish+3 strokes"},
    "064": {"t": 0.048, "i": 0.095, "m": 0.857, "n": 21,  "desc": "Fish var D"},
    "065": {"t": 0.021, "i": 0.042, "m": 0.938, "n": 48,  "desc": "Fish+hook above"},
    "066": {"t": 0.040, "i": 0.040, "m": 0.920, "n": 25,  "desc": "Fish+stroke below"},
    "067": {"t": 0.038, "i": 0.038, "m": 0.923, "n": 26,  "desc": "Fish+two above"},
    "070": {"t": 0.019, "i": 0.029, "m": 0.876, "n": 105, "desc": "Fish+2 tails"},
    "072": {"t": 0.038, "i": 0.115, "m": 0.846, "n": 26,  "desc": "Fish var G"},
    "073": {"t": 0.030, "i": 0.121, "m": 0.848, "n": 33,  "desc": "Fish var H"},
    "074": {"t": 0.143, "i": 0.000, "m": 0.857, "n": 7,   "desc": "Fish+circle"},
    "075": {"t": 0.053, "i": 0.053, "m": 0.895, "n": 19,  "desc": "Fish+zigzag"},
    # Human figure / anthropomorphs
    "083": {"t": 0.059, "i": 0.588, "m": 0.353, "n": 17,  "desc": "Kneeling figure"},
    "086": {"t": 0.060, "i": 0.360, "m": 0.540, "n": 50,  "desc": "Standing figure"},
    "088": {"t": 0.056, "i": 0.333, "m": 0.611, "n": 18,  "desc": "Figure+staff"},
    # Jar / vessel signs
    "099": {"t": 0.660, "i": 0.057, "m": 0.283, "n": 53,  "desc": "Jar (TMK)"},
    "100": {"t": 0.622, "i": 0.027, "m": 0.351, "n": 37,  "desc": "Jar variant"},
    "101": {"t": 0.533, "i": 0.067, "m": 0.400, "n": 15,  "desc": "Jar+stroke"},
    # More medial signs
    "103": {"t": 0.034, "i": 0.069, "m": 0.897, "n": 29,  "desc": "Cross-like"},
    "104": {"t": 0.038, "i": 0.115, "m": 0.846, "n": 26,  "desc": "Grid/net sign"},
    "113": {"t": 0.029, "i": 0.235, "m": 0.706, "n": 34,  "desc": "Chevron"},
    "159": {"t": 0.048, "i": 0.095, "m": 0.857, "n": 21,  "desc": "Large fish"},
    # Bull/bovine
    "200": {"t": 0.038, "i": 0.811, "m": 0.151, "n": 53,  "desc": "Bull head (initial)"},
    "201": {"t": 0.050, "i": 0.750, "m": 0.200, "n": 20,  "desc": "Short-horned bull"},
    # Two circles / paired
    "306": {"t": 0.067, "i": 0.200, "m": 0.733, "n": 15,  "desc": "Two circles"},
    "307": {"t": 0.053, "i": 0.211, "m": 0.737, "n": 19,  "desc": "Three circles"},
    # Bracket / terminal
    "282": {"t": 0.730, "i": 0.016, "m": 0.254, "n": 126, "desc": "Bracket terminal"},
    "283": {"t": 0.667, "i": 0.033, "m": 0.300, "n": 30,  "desc": "Bracket+stroke"},
    # Short stroke medial
    "342": {"t": 0.138, "i": 0.241, "m": 0.517, "n": 29,  "desc": "Short stroke medial"},
    "343": {"t": 0.167, "i": 0.200, "m": 0.633, "n": 30,  "desc": "Short+dot"},
    # Deity/figure
    "400": {"t": 0.063, "i": 0.688, "m": 0.250, "n": 16,  "desc": "Figure raised arms"},
    "401": {"t": 0.071, "i": 0.571, "m": 0.357, "n": 14,  "desc": "Figure variant"},
    # Plant/tree
    "500": {"t": 0.125, "i": 0.250, "m": 0.625, "n": 8,   "desc": "Plant/tree"},
    "501": {"t": 0.100, "i": 0.300, "m": 0.600, "n": 10,  "desc": "Tree variant"},
    "502": {"t": 0.040, "i": 0.320, "m": 0.640, "n": 25,  "desc": "Large tree/plant"},
    # Tiger/animal
    "580": {"t": 0.077, "i": 0.615, "m": 0.308, "n": 13,  "desc": "Tiger/large animal"},
    "590": {"t": 0.029, "i": 0.029, "m": 0.941, "n": 34,  "desc": "Spiral or whorl"},
}


def best_m77_full(fuls_s: str) -> tuple[str, float, str]:
    p = pp(fuls_s)
    if p["total"] == 0:
        return "?", 99.0, "unknown"
    best = min(M77_FULL.items(),
               key=lambda kv: abs(p["t_rate"]-kv[1]["t"]) +
               abs(p["i_rate"]-kv[1]["i"]) +
               abs(p["m_rate"]-kv[1]["m"]))
    d = (abs(p["t_rate"]-best[1]["t"]) +
         abs(p["i_rate"]-best[1]["i"]) +
         abs(p["m_rate"]-best[1]["m"]))
    return best[0], round(d, 3), best[1]["desc"]


# ── 1. Identify signs 48, 503, 615 ────────────────────────────────────────────

print("=" * 65)
print("1. IDENTIFYING KEY PATTERN SIGNS: 48, 503, 615")
print("=" * 65)

for target in ["48", "503", "615"]:
    p = pp(target)
    m77, d, desc = best_m77_full(target)
    print(f"\n  Sign {target}:")
    print(f"    Profile: T={p['t_rate']:.3f} I={p['i_rate']:.3f} "
          f"M={p['m_rate']:.3f} n={p['total']} solo={p['solo']}")
    print(f"    Best M77: {m77} ({desc}) dist={d:.3f}")
    print(f"    Left context:  {dict(left_ctx[target].most_common(5))}")
    print(f"    Right context: {dict(right_ctx[target].most_common(5))}")

    # Find all M77 matches sorted
    dists_all = sorted([(k, abs(p["t_rate"]-v["t"]) +
                         abs(p["i_rate"]-v["i"]) +
                         abs(p["m_rate"]-v["m"]), v["desc"])
                        for k, v in M77_FULL.items()], key=lambda x: x[1])
    print("    Top 4 M77 matches:")
    for m77c, dc, descc in dists_all[:4]:
        print(f"      M77 {m77c} ({descc:30}) dist={dc:.3f}")

# Check bigrams-mapped for 48, 503, 615
bm = json.loads((R / "mahadevan_bigrams_mapped.json").read_text("utf-8"))
print("\n  M77 mappings from bigram data:")
for target in ["48", "503", "615"]:
    m77_hits = [e.get("sign_a_m77") for e in bm if e.get("sign_a_fuls") == target
                and e.get("sign_a_m77") != "?"]
    m77_hits += [e.get("sign_b_m77") for e in bm if e.get("sign_b_fuls") == target
                 and e.get("sign_b_m77") != "?"]
    if m77_hits:
        print(f"    Sign {target}: {Counter(m77_hits).most_common(3)}")
    else:
        print(f"    Sign {target}: no bigram mapping found")


# ── 2. Test 'maa-' as reading for sign 220 ────────────────────────────────────

print("\n" + "=" * 65)
print("2. SIGN 220: 'maa-' (GREAT/COW) vs 'maram' (TREE)")
print("=" * 65)

p220 = pp("220")

# Proto-Dravidian 'maa' words (highly productive)
MAA_WORDS = [
    ("maa",    "great/large", "prefix in many words: maadhu, maayam..."),
    ("maadu",  "cattle/cow",  "very common in agricultural seals"),
    ("maalai", "garland/evening", "ritual and personal name context"),
    ("maayan", "the great dark one / Vishnu", "divine epithet"),
    ("makkal", "people/children", "social/administrative context"),
    ("maatu",  "ox/bull (alt)", "alternative for bovine"),
]

print(f"\n  Sign 220: T={p220['t_rate']:.3f} I={p220['i_rate']:.3f} "
      f"M={p220['m_rate']:.3f} n={p220['total']} (10.5% of corpus)")

print("\n  Candidate Dravidian 'maa-' readings:")
for word, meaning, note in MAA_WORDS:
    print(f"    '{word}' = {meaning} -- {note}")

# Test: what sign follows 220 most?
print("\n  Signs following 220 (right context):")
for s, c in right_ctx["220"].most_common(10):
    p_s = pp(s)
    role = "TMK" if p_s["t_rate"] > 0.6 else "INIT" if p_s["i_rate"] > 0.5 else "MED"
    pct = c / max(p220["total"], 1) * 100
    print(f"    [{s:>5}]: {c:>4} ({pct:.1f}%)  [{role}]  "
          f"T={p_s['t_rate']:.3f} I={p_s['i_rate']:.3f}")

# [220][72] = maa+meen = 'great fish' or 'maa-meen' = name?
mm = sum(1 for ins in inscriptions
         for j in range(len(ins)-1) if ins[j] == "220" and ins[j+1] in {"70","72"})
print(f"\n  [220][fish]: {mm} times  (maa+meen = 'great fish'? or compound)")

# Does 220 appear as initial (like a determinative)?
init_220 = sum(1 for ins in inscriptions if ins[0] == "220")
print(f"  [220] as initial sign: {init_220}/{p220['total']} "
      f"({init_220/max(p220['total'],1)*100:.1f}%)")
print("  (For comparison, sign 400 as initial: I-rate=0.576)")

# Positional profile tells us something:
# M=0.667 means 220 is MOSTLY medial but not as medial as fish (M=0.857+)
# T=0.184 means 220 sometimes appears at end -- could be a noun/object
# I=0.080 means occasionally initial

# If maa = 'cow/cattle': common in agricultural inventories
# If maa = 'great': often seen as a prefix (great lord, great city)
# The T=0.184 (appears terminally) is interesting -- suffix -maa?
# In Tamil: -maa suffix = emphasis, "indeed"

print(f"""
  ASSESSMENT FOR SIGN 220:
  - T=0.184 (sometimes terminal -- could be noun ending or particle)
  - M=0.667 (mostly medial -- common noun/phoneme role)
  - 10.5% frequency -- must encode something very common in Dravidian
  
  TOP CANDIDATES:
  1. 'maa-' (prefix for 'great'): fits high frequency + medial position
     Tamil 'maa-meen' = great fish (star name!) = very plausible
  2. 'maadu/maatu' (cattle): fits agricultural seal context
     Cattle are the most common seal animal -- rebus for cattle sign
  3. 'maram' (tree): fits M500 visual but 10.5% seems too frequent
  
  REVISED HYPOTHESIS: Sign 220 = 'maa' (great/prefix)
  Evidence: 'maa-meen' ({mm} times) would mean 'great fish' or 'big fish'
  This is a known Tamil star name: 'Maa-meen' = Jupiter/great star
""")


# ── 3. Expand M77 to top-100 Fuls signs ───────────────────────────────────────

print("=" * 65)
print("3. TOP-100 FULS SIGNS MATCHED TO M77")
print("=" * 65)

# Current known assignments from previous sessions
KNOWN_ASSIGNMENTS: dict[str, dict] = {
    "817": {"value": "-um",   "m77": "012", "conf": "HIGH",  "type": "suffix"},
    "72":  {"value": "meen",  "m77": "064", "conf": "MED",   "type": "phonetic"},
    "70":  {"value": "meen",  "m77": "070", "conf": "MED",   "type": "phonetic"},
    "920": {"value": "-e",    "m77": "TMK", "conf": "MED",   "type": "suffix"},
    "760": {"value": "-il",   "m77": "TMK", "conf": "MED",   "type": "suffix"},
    "798": {"value": "-ku",   "m77": "TMK", "conf": "MED",   "type": "suffix"},
    "752": {"value": "-in",   "m77": "TMK", "conf": "MED",   "type": "suffix"},
    "520": {"value": "a-",    "m77": "028", "conf": "MED",   "type": "initial"},
    "400": {"value": "a-",    "m77": "200", "conf": "MED",   "type": "initial"},
    "220": {"value": "maa?",  "m77": "500", "conf": "LOW",   "type": "logogram"},
    "32":  {"value": "ka",    "m77": "342", "conf": "MED",   "type": "phonetic"},
    "100": {"value": "meen-v","m77": "070", "conf": "LOW",   "type": "phonetic"},
    "2":   {"value": "ka-v",  "m77": "342", "conf": "LOW",   "type": "phonetic"},
    "806": {"value": "-al",   "m77": "TMK", "conf": "LOW",   "type": "suffix"},
    "900": {"value": "-an",   "m77": "TMK", "conf": "LOW",   "type": "suffix"},
    "904": {"value": "-ai",   "m77": "TMK", "conf": "LOW",   "type": "suffix"},
}

print("\n  Top 100 Fuls signs with profile match and known assignments:")
print(f"\n  {'Rank':>4}  {'Fuls':>5}  {'Count':>6}  "
      f"{'T':>5}  {'I':>5}  {'M':>5}  "
      f"{'M77':>5}  {'Dist':>5}  {'Conf':>5}  {'Value':>10}  M77 Desc")
print("  " + "-" * 90)

catalog_rows = []
for rank, (sign, count) in enumerate(freq_all.most_common(100), 1):
    p = pp(sign)
    if not p["total"]:
        continue
    m77, d, desc = best_m77_full(sign)
    known = KNOWN_ASSIGNMENTS.get(sign, {})
    conf = known.get("conf", "---")
    val = known.get("value", "?")
    print(f"  {rank:>4}  {sign:>5}  {count:>6}  "
          f"{p['t_rate']:>5.3f}  {p['i_rate']:>5.3f}  {p['m_rate']:>5.3f}  "
          f"{m77:>5}  {d:>5.3f}  {conf:>5}  {val:>10}  {desc[:18]}")
    catalog_rows.append({
        "rank": rank, "fuls": sign, "count": count,
        "t_rate": p["t_rate"], "i_rate": p["i_rate"], "m_rate": p["m_rate"],
        "best_m77": m77, "m77_dist": d, "m77_desc": desc,
        "known_value": val, "confidence": conf,
        "sign_type": known.get("type", "unknown"),
    })


# ── 4. Deep analysis of signs 48, 503, 615 context patterns ──────────────────

print("\n" + "=" * 65)
print("4. GENITIVE PATTERN [615][503][752] DEEP ANALYSIS")
print("=" * 65)

# Find all [615][503][752] occurrences
genpat: list[dict] = []
for ins_meta in inscriptions_raw:
    seq = ins_meta.get("sequence", [])
    for j in range(len(seq) - 2):
        if seq[j] == "615" and seq[j+1] == "503" and seq[j+2] == "752":
            genpat.append({
                "icit_id": ins_meta.get("icit_id"),
                "site": ins_meta.get("site", "?"),
                "seq": seq,
                "before": seq[j-1] if j > 0 else "START",
                "after": seq[j+3] if j+3 < len(seq) else "END",
            })

print(f"\n  [615][503][752] occurrences: {len(genpat)}")
if genpat:
    sites = Counter(g["site"] for g in genpat)
    befores = Counter(g["before"] for g in genpat)
    afters = Counter(g["after"] for g in genpat)
    lengths = Counter(len(g["seq"]) for g in genpat)
    print(f"  Sites: {dict(sites.most_common(5))}")
    print(f"  Inscription lengths: {dict(sorted(lengths.items()))}")
    print(f"  What precedes [615]: {dict(befores.most_common(5))}")
    print(f"  What follows [752]: {dict(afters.most_common(5))}")

# What does [615] alone look like?
p615 = pp("615")
p503 = pp("503")
m77_615, d615, desc615 = best_m77_full("615")
m77_503, d503, desc503 = best_m77_full("503")

print(f"\n  [615] profile: T={p615['t_rate']:.3f} I={p615['i_rate']:.3f} "
      f"M={p615['m_rate']:.3f} n={p615['total']}")
print(f"  [615] best M77: {m77_615} ({desc615}) dist={d615:.3f}")
print(f"\n  [503] profile: T={p503['t_rate']:.3f} I={p503['i_rate']:.3f} "
      f"M={p503['m_rate']:.3f} n={p503['total']}")
print(f"  [503] best M77: {m77_503} ({desc503}) dist={d503:.3f}")

# The pattern [615][503][-in] suggests:
# 615 = some content sign, 503 = some modifier, -in = genitive
# In Tamil: "X-in" = "of X" or "X's"
# So: [615][503] = a compound noun/phrase, then genitive marker
# Candidate: if 615 = 'eel' (kind of fish) and 503 = 'maa' then
# [615][503][-in] = 'eel-maa-in' = 'of the great eel'???
# OR: 615 and 503 are two phonetic signs: e.g. "ko" + "la" = "kola" + -in

print(f"""
  INTERPRETATION OF [615][503][752]:
  - This is a GENITIVE CONSTRUCTION: [something]-in = "of the [something]"
  - If 615 and 503 are phonetic signs, they spell a 2-syllable word
  - Sign 615 (M77 {m77_615}): {desc615}
  - Sign 503 (M77 {m77_503}): {desc503}
  
  Possible readings:
    If 615 = '{m77_615[:3].lower()}-', 503 = '{m77_503[:3].lower()}-':
    [615][503][-in] = phonetic compound + genitive
    
  This is likely a PROPER NAME + genitive: 'of [person's name]'
  Indus seals commonly show: [TITLE] [NAME] [CLAN-MARKER]
  Pattern [615][503][-in] = "[name-word]-in" = possessive on a name
""")


# ── 5. Summary sign catalog ───────────────────────────────────────────────────

print("=" * 65)
print("5. COMPREHENSIVE SIGN READING SUMMARY")
print("=" * 65)

# Count signs by category
by_conf: dict[str, list] = defaultdict(list)
for row in catalog_rows:
    by_conf[row["confidence"]].append(row)

print(f"\n  Total signs in top-100 catalog: {len(catalog_rows)}")
print(f"  HIGH confidence: {len(by_conf.get('HIGH', []))}")
print(f"  MED  confidence: {len(by_conf.get('MED',  []))}")
print(f"  LOW  confidence: {len(by_conf.get('LOW',  []))}")
print(f"  Unknown (---):   {len(by_conf.get('---',  []))}")

# Signs still unknown by function type
tmk_unknown = [r for r in catalog_rows
               if r["confidence"] == "---" and r["t_rate"] > 0.6]
init_unknown = [r for r in catalog_rows
                if r["confidence"] == "---" and r["i_rate"] > 0.5]
med_unknown  = [r for r in catalog_rows
                if r["confidence"] == "---" and r["m_rate"] > 0.7]

print(f"\n  Unknown TMK signs (likely suffixes): "
      f"{[r['fuls'] for r in tmk_unknown[:8]]}")
print(f"  Unknown INITIAL signs (likely dets): "
      f"{[r['fuls'] for r in init_unknown[:8]]}")
print(f"  Unknown MEDIAL signs (likely phonemes): "
      f"{[r['fuls'] for r in med_unknown[:8]]}")

# The full coverage
known_tokens = sum(count for sign, count in freq_all.most_common()
                   if sign in KNOWN_ASSIGNMENTS)
total_tokens = sum(freq_all.values())
print(f"\n  TOKEN COVERAGE: {known_tokens}/{total_tokens} "
      f"({known_tokens/max(total_tokens,1)*100:.1f}%) tokens have known values")
print(f"  (Based on {len(KNOWN_ASSIGNMENTS)} sign assignments)")

# Save
results = {
    "sign_48":  {"m77": best_m77_full("48")[0],  "desc": best_m77_full("48")[2],
                 "dist": best_m77_full("48")[1],  "profile": pp("48")},
    "sign_503": {"m77": best_m77_full("503")[0], "desc": best_m77_full("503")[2],
                 "dist": best_m77_full("503")[1], "profile": pp("503")},
    "sign_615": {"m77": best_m77_full("615")[0], "desc": best_m77_full("615")[2],
                 "dist": best_m77_full("615")[1], "profile": pp("615")},
    "sign_220_revised": {
        "best_candidate": "maa (great/prefix)",
        "alternatives": ["maram (tree)", "maadu (cattle)", "maalai (garland)"],
        "maa_meen_count": mm,
    },
    "genitive_pattern": {
        "count": len(genpat),
        "sites": dict(Counter(g["site"] for g in genpat).most_common()),
    },
    "token_coverage": {
        "known_tokens": known_tokens,
        "total_tokens": total_tokens,
        "pct": round(known_tokens / max(total_tokens, 1) * 100, 1),
    },
    "top100_catalog": catalog_rows,
}
(R / "sign_expansion.json").write_text(
    json.dumps(results, indent=2), encoding="utf-8"
)
print("\nSaved: reports/sign_expansion.json")
print("\nDone.")
