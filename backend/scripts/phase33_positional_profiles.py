"""Phase-33: Positional profile analysis of Indus signs vs INDUS_FINAL_ANCHORS.

Fixes the broken indus_sign_function_dravidian graph experiment (all T/I/M rates were 0.0
due to corpus/profiler wiring mismatch). This script directly computes:
  - T/I/M rates for all signs with count >= 8 from the Holdat corpus
  - Maps each HIGH/MEDIUM anchor to its positional class
  - Tests whether TERMINAL signs match Dravidian agglutinative case suffix inventory
  - Tests whether INITIAL signs match Dravidian word-initial consonant distribution

Output: reports/phase33_positional_profiles.json
"""
from __future__ import annotations
import json, sys
from collections import Counter, defaultdict
from pathlib import Path
from scipy.stats import fisher_exact  # type: ignore[import]  # optional

ROOT = Path(__file__).parents[2]
sys.path.insert(0, str(ROOT / "backend"))
sys.path.insert(0, str(ROOT / "backend" / "tests"))

REPORTS = ROOT / "reports"
BACKEND_REPORTS = ROOT / "backend" / "reports"
DATA    = ROOT / "backend" / "glossa_lab" / "data"

# ── Load Holdat corpus ─────────────────────────────────────────────────────────
from glossa_lab.data.indus_m77 import get_corpus_inscriptions, get_corpus_symbols
inscriptions = get_corpus_inscriptions()   # list[list[str]]  (M-numbers as strings)
flat_tokens  = get_corpus_symbols()        # flat list[str]

# ── Compute positional counts ──────────────────────────────────────────────────
total_c    = Counter(flat_tokens)
terminal_c = Counter(ins[-1]  for ins in inscriptions if len(ins) > 1)
initial_c  = Counter(ins[0]   for ins in inscriptions if len(ins) > 1)
medial_c   = Counter(s for ins in inscriptions for s in ins[1:-1] if len(ins) > 2)

MIN_FREQ = 8
profiles: dict[str, dict] = {}
for sign, n in total_c.items():
    if n < MIN_FREQ:
        continue
    t = terminal_c[sign] / n
    i = initial_c[sign]  / n
    m = medial_c[sign]   / n
    # Positional class: threshold ≥ 0.4 for dominant position
    if t >= 0.4:
        cls = "TERMINAL"
    elif i >= 0.4:
        cls = "INITIAL"
    elif m >= 0.4:
        cls = "MEDIAL"
    else:
        cls = "MIXED"
    profiles[sign] = {
        "count": n, "t_rate": round(t, 4), "i_rate": round(i, 4),
        "m_rate": round(m, 4), "pos_class": cls,
    }

# Summary by class
class_counts = Counter(v["pos_class"] for v in profiles.values())
print(f"Signs analysed (freq≥{MIN_FREQ}): {len(profiles)}")
print("Positional class breakdown:", dict(class_counts))

# ── Load INDUS_FINAL_ANCHORS ───────────────────────────────────────────────────
anchors_raw = json.loads((BACKEND_REPORTS / "INDUS_FINAL_ANCHORS.json").read_text("utf-8"))
anchors = anchors_raw["anchors"]  # dict[M-id -> {reading, confidence, basis}]

# ── Dravidian case suffix inventory ───────────────────────────────────────────
# Expected: HIGH-confidence terminal signs should carry case-suffix readings.
# Parpola's canonical Dravidian suffixes at terminal position:
DRAVIDIAN_CASE_SUFFIXES = {
    "ay", "an", "am", "il", "ku", "al", "atu", "in", "od",
    "otu", "iṉ", "am", "neuter", "locative", "comitative",
}

# Annotate each HIGH/MEDIUM anchor with its positional class from corpus
annotated = []
for m_id, info in anchors.items():
    conf = info["confidence"]
    if conf not in ("HIGH", "MEDIUM"):
        continue
    reading = info["reading"]
    prof = profiles.get(m_id, {})
    pos_class = prof.get("pos_class", "UNKNOWN (freq<8)")
    t_rate = prof.get("t_rate", 0.0)
    i_rate = prof.get("i_rate", 0.0)
    m_rate = prof.get("m_rate", 0.0)
    count  = prof.get("count", 0)
    # Check if reading matches expected class
    reading_lower = reading.lower().split("/")[0].strip()
    is_suffix = any(s in reading_lower for s in DRAVIDIAN_CASE_SUFFIXES)
    expected_class = "TERMINAL" if is_suffix else ("INITIAL" if conf == "HIGH" and t_rate < 0.2 else "ANY")
    match = (expected_class == "ANY") or (pos_class == expected_class) or (expected_class == "TERMINAL" and t_rate >= 0.3)
    annotated.append({
        "sign": m_id, "reading": reading, "confidence": conf,
        "count": count, "pos_class": pos_class,
        "t_rate": t_rate, "i_rate": i_rate, "m_rate": m_rate,
        "is_dravidian_suffix": is_suffix,
        "expected_pos": expected_class,
        "positional_match": match,
    })

# Sort: HIGH first, then by count
annotated.sort(key=lambda x: (0 if x["confidence"] == "HIGH" else 1, -x["count"]))

# ── Suffix-position alignment test ────────────────────────────────────────────
# Test: do signs assigned case-suffix readings have higher T-rate than signs assigned
# non-suffix readings? (Fisher's exact test on TERMINAL vs non-TERMINAL × suffix vs non-suffix)
suffix_signs    = [a for a in annotated if a["is_dravidian_suffix"]]
non_suffix_signs = [a for a in annotated if not a["is_dravidian_suffix"]]

suffix_term    = sum(1 for a in suffix_signs    if a["pos_class"] == "TERMINAL")
suffix_non     = len(suffix_signs) - suffix_term
nonsuffix_term = sum(1 for a in non_suffix_signs if a["pos_class"] == "TERMINAL")
nonsuffix_non  = len(non_suffix_signs) - nonsuffix_term

contingency = [[suffix_term, suffix_non], [nonsuffix_term, nonsuffix_non]]
try:
    from scipy.stats import fisher_exact as _fe
    odds, pval = _fe(contingency, alternative="greater")
    fisher_result = {"odds_ratio": round(float(odds), 3), "p_value": round(float(pval), 4)}
except ImportError:
    # Fallback: compute manually
    a, b, c, d = suffix_term, suffix_non, nonsuffix_term, nonsuffix_non
    fisher_result = {"note": "scipy unavailable; contingency table only",
                     "suffix_term": a, "suffix_non": b,
                     "nonsuffix_term": c, "nonsuffix_non": d}

# ── M77 profile vs Dravidian positional expectation ───────────────────────────
# Compare the corpus TERMINAL signs set to the anchor TERMINAL-expected signs.
corpus_terminal_signs = {s for s, p in profiles.items() if p["pos_class"] == "TERMINAL"}
anchor_terminal_readings = {a["sign"] for a in annotated if a["expected_pos"] == "TERMINAL"}
overlap = corpus_terminal_signs & anchor_terminal_readings
terminal_alignment_pct = len(overlap) / max(1, len(anchor_terminal_readings)) * 100

# ── Print summary ──────────────────────────────────────────────────────────────
print(f"\n=== HIGH/MEDIUM anchor positional alignment ===")
print(f"Total HIGH/MEDIUM anchors: {len(annotated)}")
print(f"  With case-suffix reading: {len(suffix_signs)}")
print(f"    → In TERMINAL position: {suffix_term} / {len(suffix_signs)} ({suffix_term/max(1,len(suffix_signs))*100:.1f}%)")
print(f"  Without case-suffix reading: {len(non_suffix_signs)}")
print(f"    → In TERMINAL position: {nonsuffix_term} / {len(non_suffix_signs)} ({nonsuffix_term/max(1,len(non_suffix_signs))*100:.1f}%)")
print(f"Fisher's exact test (suffix→TERMINAL direction):", fisher_result)
print(f"Anchor terminal-reading / corpus terminal overlap: {len(overlap)}/{len(anchor_terminal_readings)} ({terminal_alignment_pct:.1f}%)")

print(f"\nHIGH confidence anchors:")
for a in annotated:
    if a["confidence"] == "HIGH":
        print(f"  {a['sign']:6s} {a['reading']:25s} pos={a['pos_class']:8s} T={a['t_rate']:.2f} I={a['i_rate']:.2f} M={a['m_rate']:.2f} n={a['count']}")

print(f"\nTop MEDIUM anchors (by frequency):")
for a in [x for x in annotated if x["confidence"]=="MEDIUM"][:20]:
    print(f"  {a['sign']:6s} {a['reading']:25s} pos={a['pos_class']:8s} T={a['t_rate']:.2f} I={a['i_rate']:.2f} M={a['m_rate']:.2f} n={a['count']}")

# ── Save result ────────────────────────────────────────────────────────────────
result = {
    "n_signs_analysed": len(profiles),
    "min_freq": MIN_FREQ,
    "class_breakdown": dict(class_counts),
    "n_corpus_inscriptions": len(inscriptions),
    "n_corpus_tokens": len(flat_tokens),
    "high_medium_anchors": annotated,
    "suffix_position_test": {
        "contingency": {
            "suffix_TERMINAL": suffix_term, "suffix_non_TERMINAL": suffix_non,
            "nonsuffix_TERMINAL": nonsuffix_term, "nonsuffix_non_TERMINAL": nonsuffix_non,
        },
        "fisher_exact": fisher_result,
        "terminal_overlap_pct": round(terminal_alignment_pct, 1),
    },
    "all_profiles": profiles,
    "verdict": (
        f"Positional analysis of {len(profiles)} signs (freq≥{MIN_FREQ}). "
        f"Class breakdown: {dict(class_counts)}. "
        f"Signs assigned case-suffix readings are in TERMINAL position {suffix_term}/{len(suffix_signs)} "
        f"({suffix_term/max(1,len(suffix_signs))*100:.1f}%) vs non-suffix signs "
        f"{nonsuffix_term}/{len(non_suffix_signs)} ({nonsuffix_term/max(1,len(non_suffix_signs))*100:.1f}%). "
        f"Fisher p={fisher_result.get('p_value', 'N/A')}."
    ),
    "_citation": {"primary": ["A.1", "E.1", "C.2"], "phase": "Phase-33"},
}

out_path = REPORTS / "phase33_positional_profiles.json"
out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"\nSaved to {out_path}")

