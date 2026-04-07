"""TMK sign expansion: signs 845, 832, 501.

Computes real positional profiles from the ICIT corpus, ranks them against
known TMK assignments, finds M77 best matches, and proposes ranked Dravidian
suffix candidates based on profile similarity.
"""
from __future__ import annotations

import json
import math
from collections import Counter, defaultdict
from pathlib import Path

R = Path(__file__).parent.parent / "reports"

# ── Load corpus ────────────────────────────────────────────────────────────────

corpus_data = json.loads((R / "icit_extracted_corpus.json").read_text("utf-8"))
inscriptions_raw = corpus_data["inscriptions"]
inscriptions = [i["sequence"] for i in inscriptions_raw if i.get("sequence")]

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

left_ctx: dict[str, Counter] = defaultdict(Counter)
right_ctx: dict[str, Counter] = defaultdict(Counter)
for ins in inscriptions:
    for j, s in enumerate(ins):
        if j > 0:
            left_ctx[s][ins[j - 1]] += 1
        if j < len(ins) - 1:
            right_ctx[s][ins[j + 1]] += 1


def profile(s: str) -> dict:
    n = total_c.get(s, 0)
    if n == 0:
        return {"total": 0, "t_rate": 0.0, "i_rate": 0.0, "m_rate": 0.0, "solo": 0}
    return {
        "total": n,
        "solo": solo_c.get(s, 0),
        "t_rate": round(terminal_c.get(s, 0) / n, 3),
        "i_rate": round(initial_c.get(s, 0) / n, 3),
        "m_rate": round(medial_c.get(s, 0) / n, 3),
    }


def vec(p: dict) -> tuple[float, float, float]:
    return (p["t_rate"], p["i_rate"], p["m_rate"])


def cosine(a: tuple, b: tuple) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0 or nb == 0:
        return 0.0
    return round(dot / (na * nb), 4)


def l1_dist(a: tuple, b: tuple) -> float:
    return round(sum(abs(x - y) for x, y in zip(a, b)), 4)


# ── Known TMK assignments ──────────────────────────────────────────────────────
# Format: sign -> (value, language_tag, confidence)
KNOWN_SUFFIXES: dict[str, tuple[str, str]] = {
    "817": ("-um",  "additive enclitic"),
    "920": ("-e/-ē", "accusative/vocative"),
    "760": ("-il",  "locative 'in/at'"),
    "798": ("-ku",  "dative 'to/for'"),
    "752": ("-in",  "genitive/oblique"),
}

# Known Dravidian suffix inventory with expected positional profiles
# (t_rate, i_rate, m_rate) — all suffix slots should be near-exclusively terminal
DRAVIDIAN_SUFFIXES = [
    # suffix,  Tamil gloss,          expected_profile (t, i, m)
    ("-um",   "additive enclitic",  (0.85, 0.02, 0.10)),  # already 817
    ("-e/-ē", "acc/voc",            (0.80, 0.03, 0.12)),  # already 920
    ("-il",   "locative",           (0.82, 0.04, 0.10)),  # already 760
    ("-ku",   "dative",             (0.83, 0.03, 0.10)),  # already 798
    ("-in",   "genitive/oblique",   (0.78, 0.04, 0.13)),  # already 752
    ("-al",   "verbal noun",        (0.80, 0.03, 0.12)),  # unoccupied
    ("-an",   "masc. personal -an", (0.82, 0.03, 0.10)),  # unoccupied
    ("-ar",   "plural personal",    (0.80, 0.04, 0.12)),  # unoccupied
    ("-am",   "neuter nominal -am", (0.78, 0.04, 0.14)),  # unoccupied
    ("-ai",   "accusative -ai",     (0.76, 0.05, 0.14)),  # unoccupied
    ("-ān",   "long-form personal", (0.83, 0.02, 0.10)),  # unoccupied
    ("-van",  "agentive he-who",    (0.80, 0.03, 0.12)),  # unoccupied
    ("-vu",   "verbal noun alt",    (0.78, 0.04, 0.13)),  # unoccupied
    ("-tt-",  "past/intensifier",   (0.30, 0.10, 0.55)),  # medial morph
]

ALREADY_ASSIGNED = {"-um", "-e/-ē", "-il", "-ku", "-in"}

# ── M77 TMK reference profiles ─────────────────────────────────────────────────
M77_TMK = {
    "001": {"t": 0.642, "i": 0.090, "m": 0.246, "desc": "Short stroke TMK"},
    "012": {"t": 0.863, "i": 0.013, "m": 0.125, "desc": "Small circle TMK"},
    "013": {"t": 0.730, "i": 0.008, "m": 0.262, "desc": "Large circle TMK"},
    "099": {"t": 0.660, "i": 0.057, "m": 0.283, "desc": "Jar TMK"},
    "100": {"t": 0.622, "i": 0.027, "m": 0.351, "desc": "Jar variant"},
    "101": {"t": 0.533, "i": 0.067, "m": 0.400, "desc": "Jar+stroke"},
    "282": {"t": 0.730, "i": 0.016, "m": 0.254, "desc": "Bracket terminal"},
    "283": {"t": 0.667, "i": 0.033, "m": 0.300, "desc": "Bracket+stroke"},
    "006": {"t": 0.500, "i": 0.000, "m": 0.500, "desc": "Vertical+horizontal"},
    "008": {"t": 0.600, "i": 0.100, "m": 0.300, "desc": "Three vertical strokes"},
}


def best_m77_tmk(s: str) -> list[tuple[str, float, str]]:
    p = profile(s)
    pv = vec(p)
    ranked = sorted(
        [(k, l1_dist(pv, (v["t"], v["i"], v["m"])), v["desc"])
         for k, v in M77_TMK.items()],
        key=lambda x: x[1],
    )
    return ranked[:4]


def rank_suffix_candidates(s: str) -> list[tuple[str, str, float, str]]:
    """Return suffix candidates ranked by cosine similarity to sign profile."""
    p = profile(s)
    pv = vec(p)
    results = []
    for suffix, gloss, expected in DRAVIDIAN_SUFFIXES:
        sim = cosine(pv, expected)
        status = "OCCUPIED" if suffix in ALREADY_ASSIGNED else "OPEN"
        results.append((suffix, gloss, sim, status))
    return sorted(results, key=lambda x: -x[2])


# ── Analysis ───────────────────────────────────────────────────────────────────

TARGETS = ["845", "832", "501"]

print("=" * 70)
print("TMK SIGN EXPANSION: 845 / 832 / 501")
print(f"Corpus: {len(inscriptions)} inscriptions, {sum(total_c.values())} tokens")
print("=" * 70)

# First, show all known suffixes for comparison
print("\nKNOWN SUFFIX ASSIGNMENTS (reference):")
for sign, (val, gloss) in KNOWN_SUFFIXES.items():
    p = profile(sign)
    print(f"  Sign {sign:>4}: T={p['t_rate']:.3f} I={p['i_rate']:.3f} "
          f"M={p['m_rate']:.3f} n={p['total']:>4}  → {val}  ({gloss})")

# Calculate average known-suffix profile
known_vecs = [vec(profile(s)) for s in KNOWN_SUFFIXES]
avg_t = sum(v[0] for v in known_vecs) / len(known_vecs)
avg_i = sum(v[1] for v in known_vecs) / len(known_vecs)
avg_m = sum(v[2] for v in known_vecs) / len(known_vecs)
print(f"\n  Average known-suffix profile: T={avg_t:.3f} I={avg_i:.3f} M={avg_m:.3f}")
print(f"  → A good suffix candidate should have T > 0.70, I < 0.10")

print("\n" + "=" * 70)

for sign in TARGETS:
    p = profile(sign)
    pv = vec(p)

    # Similarity to each known suffix
    known_sims = {
        f"{v} ({s})": cosine(pv, vec(profile(s)))
        for s, (v, _) in KNOWN_SUFFIXES.items()
    }

    print(f"\nSIGN {sign}")
    print(f"  Profile: T={p['t_rate']:.3f}  I={p['i_rate']:.3f}  "
          f"M={p['m_rate']:.3f}  total={p['total']}  solo={p['solo']}")

    # Profile verdict
    if p["t_rate"] >= 0.70:
        verdict = "STRONG TERMINAL — excellent suffix candidate"
    elif p["t_rate"] >= 0.55:
        verdict = "MODERATE TERMINAL — possible suffix"
    else:
        verdict = "MIXED — may not be a pure suffix"
    print(f"  Verdict: {verdict}")

    # Similarity to known suffixes
    print(f"  Cosine similarity to known suffixes:")
    for label, sim in sorted(known_sims.items(), key=lambda x: -x[1]):
        bar = "█" * int(sim * 20)
        print(f"    {label:<25} {sim:.4f}  {bar}")

    # M77 best matches
    m77_matches = best_m77_tmk(sign)
    print(f"  Best M77 TMK matches:")
    for m77, dist, desc in m77_matches:
        print(f"    M77 {m77} ({desc:<30}) L1={dist:.3f}")

    # Top unoccupied suffix candidates
    candidates = rank_suffix_candidates(sign)
    print(f"  Top suffix candidates (cosine similarity to profile):")
    for suffix, gloss, sim, status in candidates[:6]:
        marker = "  ← OPEN" if status == "OPEN" else "  (taken: 817/920/760/798/752)"
        bar = "█" * int(sim * 20)
        print(f"    {suffix:<8} {gloss:<25} {sim:.4f} {bar}{marker}")

    # Context analysis
    left_top = left_ctx[sign].most_common(8)
    right_top = right_ctx[sign].most_common(5)
    print(f"  Left context  (what precedes this sign, top 8): {dict(left_top)}")
    print(f"  Right context (what follows,  top 5):           {dict(right_top)}")

    # Check if this sign co-occurs with other known TMK signs (stacking)
    stacking = sum(
        1 for ins in inscriptions
        if sign in ins and any(k in ins for k in KNOWN_SUFFIXES if k != sign)
    )
    total_with_sign = sum(1 for ins in inscriptions if sign in ins)
    stack_rate = round(stacking / total_with_sign, 3) if total_with_sign else 0
    print(f"  Co-TMK stacking rate: {stack_rate:.3f} "
          f"({stacking}/{total_with_sign} inscriptions with sign also have a known suffix)")
    if stack_rate > 0.15:
        print(f"  ⚠ High stacking — sign may NOT be a final suffix "
              f"(suffixes rarely stack with each other)")
    else:
        print(f"  ✓ Low stacking — consistent with independent suffix slot")

    # Inscriptions where sign appears
    insc_with = [ins for ins in inscriptions if sign in ins]
    insc_solo = [ins for ins in inscriptions if ins == [sign]]
    print(f"  Appears in {total_with_sign} inscriptions, "
          f"{len(insc_solo)} solo, {total_with_sign - len(insc_solo)} multi-sign")

    # Position stats in multi-sign inscriptions
    positions = []
    for ins in inscriptions:
        if sign in ins and len(ins) > 1:
            idx = ins.index(sign)
            positions.append(idx / (len(ins) - 1))  # 0.0=initial, 1.0=terminal
    if positions:
        avg_pos = sum(positions) / len(positions)
        print(f"  Average relative position: {avg_pos:.3f} (0=initial, 1.0=terminal)")

    print()

# ── Unoccupied suffix slot summary ────────────────────────────────────────────
print("=" * 70)
print("UNOCCUPIED DRAVIDIAN SUFFIX SLOTS (candidates for 845/832/501)")
print("=" * 70)

dravidian_open = [
    ("-al",  "verbal noun",         "e.g. ceyal (action), ural (dwelling)"),
    ("-an",  "masc. personal noun", "e.g. mīnavan (fisherman), koṭṭan (fort-man)"),
    ("-ar",  "plural person",       "e.g. āḷar (people), maṉḏar (lords)"),
    ("-am",  "neuter nominal",      "e.g. nilam (land), vīram (heroism)"),
    ("-ai",  "accusative/abstract", "e.g. neñcai (heart-ACC), āmai (turtle)"),
    ("-ān",  "long-form personal",  "e.g. maṉṉāṉ (king), āḷān (ruler)"),
    ("-van", "agentive 'he who'",   "e.g. ceyvān (one who does), ūrvān"),
]

print("\n  The 5 occupied slots: -um(817) -e(920) -il(760) -ku(798) -in(752)")
print("\n  Remaining open slots:")
for suffix, gloss, examples in dravidian_open:
    print(f"    {suffix:<8} {gloss:<25} {examples}")

print("\n  Best fit hypothesis (needs field validation):")
p845 = profile("845")
p832 = profile("832")
p501 = profile("501")

for sign, p in [("845", p845), ("832", p832), ("501", p501)]:
    cands = [r for r in rank_suffix_candidates(sign) if r[3] == "OPEN"][:2]
    top = cands[0][0] if cands else "?"
    sim = cands[0][2] if cands else 0.0
    print(f"  Sign {sign}: best unoccupied slot = {top}  (cosine={sim:.4f})")

# ── Save results ───────────────────────────────────────────────────────────────
results = {}
for sign in TARGETS:
    p = profile(sign)
    candidates = rank_suffix_candidates(sign)
    m77 = best_m77_tmk(sign)
    stacking = sum(
        1 for ins in inscriptions
        if sign in ins and any(k in ins for k in KNOWN_SUFFIXES if k != sign)
    )
    total_with = sum(1 for ins in inscriptions if sign in ins)
    results[sign] = {
        "profile": p,
        "m77_best": [{"code": c, "dist": d, "desc": desc} for c, d, desc in m77],
        "suffix_candidates": [
            {"suffix": s, "gloss": g, "cosine": c, "status": st}
            for s, g, c, st in candidates[:8]
        ],
        "co_tmk_stack_rate": round(stacking / total_with, 3) if total_with else 0,
        "left_context": dict(left_ctx[sign].most_common(8)),
        "right_context": dict(right_ctx[sign].most_common(5)),
    }

out = R / "tmk_expansion_845_832_501.json"
out.write_text(json.dumps(results, indent=2), "utf-8")
print(f"\nResults saved → {out}")
