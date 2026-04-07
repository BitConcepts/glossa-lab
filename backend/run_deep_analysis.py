"""Deep follow-up analysis for Indus Script decipherment.

Covers:
  1. Sign 240 identity and M77 crosswalk
  2. [400][fish] site distribution test
  3. Full 544-pair equivalence classes
  4. [X][Y][240][405][501] formula decomposition
  5. Extended crosswalk via positional-profile matching
"""
from __future__ import annotations

import json
import math
from collections import Counter, defaultdict
from pathlib import Path

R = Path(__file__).parent.parent / "reports"
corpus_data = json.loads((R / "icit_extracted_corpus.json").read_text("utf-8"))
inscriptions_raw = corpus_data["inscriptions"]
inscriptions = [i["sequence"] for i in inscriptions_raw if i.get("sequence")]
freq_all = Counter(s for ins in inscriptions for s in ins)

# ── Compute positional profiles (needed throughout) ────────────────────────────
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


def pos_profile(sign: str) -> dict:
    n = total_c.get(sign, 0)
    if n == 0:
        return {}
    return {
        "total": n,
        "t_rate": round(terminal_c.get(sign, 0) / n, 4),
        "i_rate": round(initial_c.get(sign, 0) / n, 4),
        "m_rate": round(medial_c.get(sign, 0) / n, 4),
        "solo": solo_c.get(sign, 0),
        "solo_rate": round(solo_c.get(sign, 0) / n, 4),
    }


# ── 1. Sign 240 identity ───────────────────────────────────────────────────────

print("=" * 65)
print("1. SIGN 240 IDENTITY")
print("=" * 65)

pp240 = pos_profile("240")
print(f"\n  Sign 240 profile: {pp240}")

# Check bigram-mapped data for sign 240
bm = json.loads((R / "mahadevan_bigrams_mapped.json").read_text("utf-8"))
m77_for_240: list[str] = []
for entry in bm:
    if entry.get("sign_a_fuls") == "240":
        m77_for_240.append(entry.get("sign_a_m77", "?"))
    if entry.get("sign_b_fuls") == "240":
        m77_for_240.append(entry.get("sign_b_m77", "?"))

m77_counts_240 = Counter(m77_for_240)
print(f"\n  M77 codes mapped to Fuls 240 (from bigrams): {dict(m77_counts_240.most_common(5))}")

# Positional comparison with known M77 signs
# Most medial M77 signs: M029 (comb, freq=168), M059 (fish, freq=381)
# But sign 240 is neither fish nor comb -- it precedes the [405,501] formula
# Let's check: what signs appear BEFORE 240 and AFTER 240?
before_240: Counter = Counter()
after_240: Counter = Counter()
for ins in inscriptions:
    for j, s in enumerate(ins):
        if s == "240":
            if j > 0:
                before_240[ins[j - 1]] += 1
            if j < len(ins) - 1:
                after_240[ins[j + 1]] += 1

print(f"\n  Signs before 240: {dict(before_240.most_common(8))}")
print(f"  Signs after 240: {dict(after_240.most_common(8))}")

# In the formula [X][Y][240][405][501]:
# - 240 is in position 3 (of 5)
# - 405 ALWAYS follows 240 in that formula
# - So "after 240" should be dominated by "405"
print(f"\n  Times 240 is followed by 405: {after_240.get('405', 0)}")
print(f"  Total times 240 appears: {total_c.get('240', 0)}")
formula_fraction = after_240.get('405', 0) / max(total_c.get('240', 0), 1)
print(f"  Fraction where 240->405: {formula_fraction:.3f}")

# Most likely M77 identity based on profile:
# T-rate ~?, I-rate ~?, M-rate ~?
# Compare with M77 signs we know:
print("\n  Best M77 candidates for sign 240:")
m77_known = {
    "013": {"t": 0.73, "i": 0.008, "m": 0.238, "desc": "Large circle / jar"},
    "028": {"t": 0.044, "i": 0.923, "m": 0.033, "desc": "Arrow/stroke (initial)"},
    "029": {"t": 0.030, "i": 0.101, "m": 0.869, "desc": "Comb/rake (medial)"},
    "059": {"t": 0.047, "i": 0.094, "m": 0.812, "desc": "Fish"},
    "099": {"t": 0.660, "i": 0.057, "m": 0.283, "desc": "Jar with handles (TMK)"},
    "342": {"t": 0.138, "i": 0.241, "m": 0.517, "desc": "Short stroke (balanced)"},
}
n240 = pp240.get("total", 1)
t240 = pp240.get("t_rate", 0)
i240 = pp240.get("i_rate", 0)
m240 = pp240.get("m_rate", 0)
for m77, prof in sorted(m77_known.items(),
                         key=lambda kv: abs(kv[1]["t"] - t240) +
                                        abs(kv[1]["i"] - i240) +
                                        abs(kv[1]["m"] - m240)):
    dist = abs(prof["t"] - t240) + abs(prof["i"] - i240) + abs(prof["m"] - m240)
    print(f"    M77 {m77} ({prof['desc']:28}) dist={dist:.3f}  "
          f"T={prof['t']:.3f} I={prof['i']:.3f} M={prof['m']:.3f}")


# ── 2. [400][fish] site distribution ──────────────────────────────────────────

print("\n" + "=" * 65)
print("2. [400][FISH] SITE DISTRIBUTION TEST")
print("=" * 65)

fish_family = {"32", "33", "34", "16", "100"}
coastal_sites = {"lothal", "dholavira", "sutkagen-dor", "balakot",
                 "kuntasi", "desalpur", "shortugai", "sokhta koh"}
heartland_sites = {"harappa", "mohenjo-daro", "chanhu-daro", "rakhigarhi"}

pattern_400_fish: list[dict] = []
all_400_inss: list[dict] = []

for ins_meta in inscriptions_raw:
    seq = ins_meta.get("sequence", [])
    site = ins_meta.get("site", "Unknown").lower().strip()
    if not seq:
        continue
    if seq[0] == "400":
        all_400_inss.append(ins_meta)
        if len(seq) > 1 and seq[1] in fish_family:
            pattern_400_fish.append(ins_meta)

print(f"\n  All [400]-initial inscriptions: {len(all_400_inss)}")
print(f"  [400][fish] inscriptions: {len(pattern_400_fish)}")

# Site breakdown
site_all_400: Counter = Counter()
site_400_fish: Counter = Counter()
for ins_meta in all_400_inss:
    site = ins_meta.get("site", "Unknown").strip()
    site_all_400[site] += 1
for ins_meta in pattern_400_fish:
    site = ins_meta.get("site", "Unknown").strip()
    site_400_fish[site] += 1

print("\n  Top sites for ALL [400]-initial inscriptions:")
for site, count in site_all_400.most_common(8):
    total_site = sum(1 for ins in inscriptions_raw
                     if ins.get("site", "Unknown").strip() == site)
    rate = count / max(total_site, 1)
    marker = " [COASTAL]" if site.lower() in coastal_sites else \
             " [HEARTLAND]" if site.lower() in heartland_sites else ""
    print(f"    {site:<25} {count:>5}  ({rate*100:.1f}% of site inscriptions){marker}")

print("\n  Top sites for [400][FISH] inscriptions:")
for site, count in site_400_fish.most_common(8):
    all_400_at_site = site_all_400.get(site, 0)
    rate_in_400 = count / max(all_400_at_site, 1)
    marker = " [COASTAL]" if site.lower() in coastal_sites else \
             " [HEARTLAND]" if site.lower() in heartland_sites else ""
    print(f"    {site:<25} {count:>5}  ({rate_in_400*100:.1f}% of 400-inscriptions"
          f" at this site){marker}")

# Coastal vs heartland comparison
coastal_400 = sum(v for k, v in site_all_400.items() if k.lower() in coastal_sites)
coastal_400_fish = sum(v for k, v in site_400_fish.items() if k.lower() in coastal_sites)
heartland_400 = sum(v for k, v in site_all_400.items() if k.lower() in heartland_sites)
heartland_400_fish = sum(v for k, v in site_400_fish.items() if k.lower() in heartland_sites)

print(f"\n  Coastal sites:   {coastal_400_fish}/{coastal_400} [400][fish] "
      f"({coastal_400_fish/max(coastal_400,1)*100:.1f}%)")
print(f"  Heartland sites: {heartland_400_fish}/{heartland_400} [400][fish] "
      f"({heartland_400_fish/max(heartland_400,1)*100:.1f}%)")
if coastal_400 > 0 and heartland_400 > 0:
    coastal_rate = coastal_400_fish / coastal_400
    heartland_rate = heartland_400_fish / heartland_400
    if coastal_rate > heartland_rate * 1.5:
        print(f"\n  *** CONFIRMED: [400][fish] enriched at coastal sites "
              f"({coastal_rate*100:.1f}% vs {heartland_rate*100:.1f}%)!")
        print("  This supports FISHERMAN as a coastal trade-site title.")
    else:
        print("\n  Site distribution does not show coastal enrichment.")


# ── 3. Full 544-pair equivalence classes ──────────────────────────────────────

print("\n" + "=" * 65)
print("3. FULL 544-PAIR EQUIVALENCE CLASSES")
print("=" * 65)

# Recompute substitution pairs on the FULL corpus
left_ctx: dict[str, Counter] = defaultdict(Counter)
right_ctx: dict[str, Counter] = defaultdict(Counter)

for ins in inscriptions:
    for j, s in enumerate(ins):
        if j > 0:
            left_ctx[s][ins[j - 1]] += 1
        if j < len(ins) - 1:
            right_ctx[s][ins[j + 1]] += 1


def cosine(a: Counter, b: Counter) -> float:
    if not a or not b:
        return 0.0
    keys = set(a) | set(b)
    dot = sum(a.get(k, 0) * b.get(k, 0) for k in keys)
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    return dot / max(na * nb, 1e-10)


candidates = [s for s, n in freq_all.items() if n >= 6]
print(f"\n  Computing pairwise similarity for {len(candidates)} signs (n>=6)...")

all_pairs = []
for i, s1 in enumerate(candidates):
    for s2 in candidates[i + 1:]:
        ls = cosine(left_ctx[s1], left_ctx[s2])
        rs = cosine(right_ctx[s1], right_ctx[s2])
        combined = (ls + rs) / 2
        if combined > 0.40:
            all_pairs.append({
                "sign_a": s1, "sign_b": s2,
                "left_sim": round(ls, 3), "right_sim": round(rs, 3),
                "combined": round(combined, 3),
            })

all_pairs.sort(key=lambda x: -x["combined"])
print(f"  Total substitution pairs (sim > 0.40): {len(all_pairs)}")

# Union-Find for equivalence classes
parent: dict[str, str] = {}


def find(x: str) -> str:
    if parent.setdefault(x, x) != x:
        parent[x] = find(parent[x])
    return parent[x]


def union(x: str, y: str) -> None:
    px, py = find(x), find(y)
    if px != py:
        parent[px] = py


# Build at multiple thresholds
for thresh in [0.50, 0.55, 0.60, 0.70]:
    parent = {}
    for pair in all_pairs:
        if pair["combined"] >= thresh:
            union(pair["sign_a"], pair["sign_b"])
    groups: dict[str, set[str]] = defaultdict(set)
    for s in list(parent.keys()):
        groups[find(s)].add(s)
    non_trivial = [g for g in groups.values() if len(g) >= 2]
    sizes = sorted([len(g) for g in non_trivial], reverse=True)
    print(f"  threshold={thresh}: {len(non_trivial)} classes, "
          f"sizes={sizes[:10]}")

# Use threshold=0.55 for the final classes
parent = {}
for pair in all_pairs:
    if pair["combined"] >= 0.55:
        union(pair["sign_a"], pair["sign_b"])
groups_final: dict[str, set[str]] = defaultdict(set)
for s in list(parent.keys()):
    groups_final[find(s)].add(s)
classes_full = sorted(
    [g for g in groups_final.values() if len(g) >= 2],
    key=lambda x: -len(x)
)
print(f"\n  Full equivalence classes at 0.55 ({len(classes_full)} classes):")
for i, cls in enumerate(classes_full[:15]):
    print(f"  Class {i:2d} ({len(cls):>2} signs): {sorted(cls)}")

# Save all pairs for future use
(R / "full_substitution_pairs.json").write_text(
    json.dumps({"pairs": all_pairs[:200], "total": len(all_pairs)}, indent=2),
    encoding="utf-8"
)
print("\n  Saved top-200 substitution pairs to full_substitution_pairs.json")


# ── 4. Formula [X][Y][240][405][501] decomposition ───────────────────────────

print("\n" + "=" * 65)
print("4. FORMULA [X][Y][240][405][501] DECOMPOSITION")
print("=" * 65)

formula_instances: list[dict] = []
for ins_meta in inscriptions_raw:
    seq = ins_meta.get("sequence", [])
    if len(seq) == 5:
        if seq[2] == "240" and seq[3] == "405" and seq[4] == "501":
            formula_instances.append({
                "icit_id": ins_meta.get("icit_id"),
                "site": ins_meta.get("site", "Unknown"),
                "X": seq[0],
                "Y": seq[1],
                "full": seq,
            })

print(f"\n  Formula instances [X][Y][240][405][501]: {len(formula_instances)}")

# All unique [X][Y] pairs
xy_pairs: Counter = Counter()
x_signs: Counter = Counter()
y_signs: Counter = Counter()
for inst in formula_instances:
    xy_pairs[(inst["X"], inst["Y"])] += 1
    x_signs[inst["X"]] += 1
    y_signs[inst["Y"]] += 1

print(f"\n  Unique [X] signs (position 1): {len(x_signs)}")
print(f"  Unique [Y] signs (position 2): {len(y_signs)}")
print(f"  Unique [X][Y] combinations: {len(xy_pairs)}")
print("\n  Top [X] signs:")
for s, c in x_signs.most_common(8):
    pp = pos_profile(s)
    print(f"    {s:>5}: {c:>3} times  T={pp.get('t_rate',0):.3f} "
          f"I={pp.get('i_rate',0):.3f}")
print("\n  Top [Y] signs:")
for s, c in y_signs.most_common(8):
    pp = pos_profile(s)
    print(f"    {s:>5}: {c:>3} times  T={pp.get('t_rate',0):.3f} "
          f"I={pp.get('i_rate',0):.3f}")
print("\n  Top [X][Y] pairs:")
for (x, y), c in xy_pairs.most_common(8):
    print(f"    [{x}][{y}]: {c} times")

# Site breakdown
formula_sites: Counter = Counter()
for inst in formula_instances:
    formula_sites[inst["site"]] += 1
print("\n  Site breakdown:")
for site, c in formula_sites.most_common(6):
    marker = " [COASTAL]" if site.lower() in coastal_sites else \
             " [HEARTLAND]" if site.lower() in heartland_sites else ""
    print(f"    {site:<25}: {c}{marker}")

# Does [X] show fish-family affinity?
x_is_fish = sum(v for k, v in x_signs.items() if k in fish_family)
x_is_initial = sum(v for k, v in x_signs.items() if pos_profile(k).get("i_rate", 0) > 0.5)
print(f"\n  [X] positions with fish-family signs: {x_is_fish}/{len(formula_instances)}")
print(f"  [X] positions with initial-bias signs: {x_is_initial}/{len(formula_instances)}")


# ── 5. Extended crosswalk (positional profile matching) ───────────────────────

print("\n" + "=" * 65)
print("5. EXTENDED CROSSWALK (positional profile matching)")
print("=" * 65)

# Mahadevan M77 positional profiles (from frequency tables, M77 pp.727-755)
# Format: m77_code -> (T-rate, I-rate, M-rate, total, description)
M77_PROFILES: dict[str, dict] = {
    "001": {"t": 0.642, "i": 0.090, "m": 0.246, "n": 134, "desc": "Short stroke"},
    "002": {"t": 0.333, "i": 0.333, "m": 0.333, "n": 21, "desc": "Two strokes"},
    "005": {"t": 0.000, "i": 0.019, "m": 0.981, "n": 105, "desc": "Six strokes"},
    "012": {"t": 0.863, "i": 0.013, "m": 0.125, "n": 80, "desc": "Small circle"},
    "013": {"t": 0.730, "i": 0.008, "m": 0.262, "n": 126, "desc": "Large circle"},
    "028": {"t": 0.044, "i": 0.923, "m": 0.033, "n": 91, "desc": "Arrow (initial)"},
    "029": {"t": 0.030, "i": 0.101, "m": 0.869, "n": 168, "desc": "Comb/rake"},
    "059": {"t": 0.047, "i": 0.094, "m": 0.812, "n": 381, "desc": "Fish"},
    "060": {"t": 0.062, "i": 0.046, "m": 0.831, "n": 130, "desc": "Fish+arrow"},
    "070": {"t": 0.019, "i": 0.029, "m": 0.876, "n": 105, "desc": "Fish+strokes"},
    "086": {"t": 0.060, "i": 0.360, "m": 0.540, "n": 50, "desc": "Standing figure"},
    "099": {"t": 0.660, "i": 0.057, "m": 0.283, "n": 53, "desc": "Jar"},
    "159": {"t": 0.048, "i": 0.095, "m": 0.857, "n": 21, "desc": "Large fish"},
    "200": {"t": 0.038, "i": 0.811, "m": 0.151, "n": 53, "desc": "Bull head"},
    "282": {"t": 0.730, "i": 0.016, "m": 0.254, "n": 126, "desc": "Bracket/jar term"},
    "342": {"t": 0.138, "i": 0.241, "m": 0.517, "n": 29, "desc": "Short stroke"},
}


def profile_dist(p1: dict, p2: dict) -> float:
    return (abs(p1.get("t_rate", 0) - p2["t"]) +
            abs(p1.get("i_rate", 0) - p2["i"]) +
            abs(p1.get("m_rate", 0) - p2["m"]))


# Match top-50 ICIT signs to their best M77 counterpart
print("\n  Matching top-50 ICIT signs to M77 by positional profile:")
print(f"  {'Fuls':>5}  {'Count':>6}  {'T':>5}  {'I':>5}  {'M':>5}  "
      f"{'Best M77':>8}  {'Dist':>5}  Desc")
print("  " + "-" * 72)

crosswalk_extended: list[dict] = []
for sign, count in freq_all.most_common(50):
    pp = pos_profile(sign)
    if not pp:
        continue
    best_m77 = min(M77_PROFILES.items(), key=lambda kv: profile_dist(pp, kv[1]))
    dist = round(profile_dist(pp, best_m77[1]), 3)
    crosswalk_extended.append({
        "fuls": sign, "count": count,
        "best_m77": best_m77[0], "dist": dist,
        "m77_desc": best_m77[1]["desc"],
        "t": pp.get("t_rate", 0), "i": pp.get("i_rate", 0), "m": pp.get("m_rate", 0),
    })
    print(f"  {sign:>5}  {count:>6}  {pp.get('t_rate',0):>5.3f}  "
          f"{pp.get('i_rate',0):>5.3f}  {pp.get('m_rate',0):>5.3f}  "
          f"{best_m77[0]:>8}  {dist:>5.3f}  {best_m77[1]['desc'][:20]}")

# Save extended crosswalk
(R / "fuls_m77_extended_crosswalk.json").write_text(
    json.dumps(crosswalk_extended, indent=2), encoding="utf-8"
)
print("\n  Saved extended crosswalk (50 entries)")


# ── Synthesis ─────────────────────────────────────────────────────────────────

print("\n" + "=" * 65)
print("SESSION SYNTHESIS")
print("=" * 65)

# What is sign 240?
best_240 = min(M77_PROFILES.items(), key=lambda kv: profile_dist(pp240, kv[1]))
dist_240 = round(profile_dist(pp240, best_240[1]), 3)
print(f"""
SIGN 240 IDENTITY:
  Profile: T={pp240.get('t_rate',0):.3f} I={pp240.get('i_rate',0):.3f} M={pp240.get('m_rate',0):.3f}
  Best M77 match: {best_240[0]} ({best_240[1]['desc']}) dist={dist_240}
  M77 candidates from bigrams: {dict(m77_counts_240.most_common(3))}
  Formula fraction (240->405): {formula_fraction:.3f}

  INTERPRETATION: Sign 240 appears before 405 in {formula_fraction*100:.0f}% of its occurrences.
  This means [240][405][501] is a near-fixed 3-sign terminal cluster.
  Best M77 match ({best_240[0]}) suggests sign 240 = {best_240[1]['desc']}.
  Dravidian candidate: see M77 description.

FISHERMAN TITLE ([400][FISH]) SITE DISTRIBUTION:
  Coastal:  {coastal_400_fish}/{max(coastal_400,1)} ({coastal_400_fish/max(coastal_400,1)*100:.1f}%)
  Heartland: {heartland_400_fish}/{max(heartland_400,1)} ({heartland_400_fish/max(heartland_400,1)*100:.1f}%)

FULL EQUIVALENCE CLASSES:
  {len(all_pairs)} total pairs found (vs 25 used previously)
  {len(classes_full)} equivalence classes at threshold 0.55

FORMULA [X][Y][240][405][501]:
  {len(formula_instances)} instances, {len(xy_pairs)} unique [X][Y] combinations
  Sign 240 -> 405 rate: {formula_fraction:.1%}
""")

print("Done.")
