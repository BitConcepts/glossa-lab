"""Phase-33: TB correlation significance test (permutation null).

The V24 TB phoneme correlation of 0.907 (random baseline 0.470) has never
been given a rigorous p-value. This script:
  1. Computes the observed Pearson r between Indus sign-frequency ranks and
     Tamil-Brahmi phoneme-frequency ranks using the INDUS_FINAL_ANCHORS mapping.
  2. Runs 10,000 permutations of the anchor assignment (shuffling which signs
     get which phoneme) and recomputes r each time.
  3. Reports: p-value, Z-score, 95% CI, effect size.

Output: reports/phase33_tb_corr_significance.json
"""
from __future__ import annotations
import json, random, sys, math
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).parents[2]
sys.path.insert(0, str(ROOT / "backend"))

REPORTS = ROOT / "reports"
BACKEND_REPORTS = ROOT / "backend" / "reports"
DATA    = ROOT / "backend" / "glossa_lab" / "data"

# ── Load Holdat corpus ─────────────────────────────────────────────────────────
from glossa_lab.data.indus_m77 import get_corpus_symbols, get_corpus_inscriptions
flat_tokens  = get_corpus_symbols()
inscriptions = get_corpus_inscriptions()
indus_freq   = Counter(flat_tokens)   # M-sign → raw count

# ── Load TB phoneme frequencies ────────────────────────────────────────────────
# mahadevan_papers_phonemes.json has phoneme → frequency data from Tamil-Brahmi
tb_phon_path = DATA / "mahadevan_papers_phonemes.json"
tb_lm_path   = DATA / "mahadevan_2003_tb_lm_clean.json"

# Try to load TB phoneme frequencies
tb_phon_freq: dict[str, int] = {}
if tb_phon_path.exists():
    raw = json.loads(tb_phon_path.read_text("utf-8"))
    # Could be a list of {phoneme, count} or a dict
    if isinstance(raw, dict):
        tb_phon_freq = {k: int(v) for k, v in raw.items() if isinstance(v, (int, float))}
    elif isinstance(raw, list):
        for item in raw:
            if isinstance(item, dict):
                p = item.get("phoneme") or item.get("symbol") or item.get("token", "")
                c = item.get("count") or item.get("freq") or item.get("n", 0)
                if p:
                    tb_phon_freq[str(p)] = int(c)

if not tb_phon_freq and tb_lm_path.exists():
    raw = json.loads(tb_lm_path.read_text("utf-8"))
    # Extract unigram frequencies from the LM
    if isinstance(raw, dict):
        for key in ("unigram_freq", "phoneme_freq", "symbols", "vocab"):
            if key in raw:
                entry = raw[key]
                if isinstance(entry, dict):
                    tb_phon_freq = {k: float(v) for k, v in entry.items()}
                    break
        if not tb_phon_freq:
            # Try bigram keys to extract vocabulary
            bigrams = raw.get("bigrams", {})
            freq: Counter = Counter()
            for bg_key, cnt in bigrams.items():
                parts = bg_key.split("|") if "|" in bg_key else bg_key.split(",")
                for p in parts:
                    freq[p.strip()] += abs(float(cnt))
            tb_phon_freq = dict(freq)

# If still empty, use mahadevan_parpola_crosswalk for phoneme list
if not tb_phon_freq:
    crosswalk_path = DATA / "mahadevan_parpola_crosswalk_v2.json"
    if crosswalk_path.exists():
        cw = json.loads(crosswalk_path.read_text("utf-8"))
        # Build synthetic uniform TB phoneme freqs
        phonemes = set()
        for entry in (cw if isinstance(cw, list) else cw.values()):
            if isinstance(entry, dict):
                p = entry.get("tb_phoneme") or entry.get("reading", "")
                if p:
                    phonemes.add(str(p).strip())
        tb_phon_freq = {p: 1 for p in phonemes if p}

print(f"TB phoneme vocabulary: {len(tb_phon_freq)} items")
print(f"Indus corpus: {len(flat_tokens)} tokens, {len(indus_freq)} signs")

# ── Load INDUS_FINAL_ANCHORS ───────────────────────────────────────────────────
anchors_raw = json.loads((BACKEND_REPORTS / "INDUS_FINAL_ANCHORS.json").read_text("utf-8"))
anchors = anchors_raw["anchors"]

# Build the anchor mapping: sign_M-id → phoneme (use HIGH + MEDIUM only)
valid_phonemes = set(tb_phon_freq.keys())

anchor_pairs: list[tuple[str, str, str]] = []  # (sign_id, reading, confidence)
for m_id, info in anchors.items():
    conf = info["confidence"]
    if conf not in ("HIGH", "MEDIUM"):
        continue
    reading = info["reading"].split("/")[0].strip()
    anchor_pairs.append((m_id, reading, conf))

print(f"Anchor pairs (HIGH+MEDIUM): {len(anchor_pairs)}")

# ── Pearson r helper ───────────────────────────────────────────────────────────
def pearson_r(xs: list[float], ys: list[float]) -> float:
    n = len(xs)
    if n < 2:
        return 0.0
    mx = sum(xs) / n
    my = sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    dx  = math.sqrt(sum((x - mx) ** 2 for x in xs) or 1)
    dy  = math.sqrt(sum((y - my) ** 2 for y in ys) or 1)
    return num / (dx * dy)

# ── Build rank vectors ─────────────────────────────────────────────────────────
# Indus sign frequency rank (1 = most frequent)
sorted_indus = sorted(indus_freq, key=lambda s: -indus_freq[s])
indus_rank = {s: i + 1 for i, s in enumerate(sorted_indus)}

# TB phoneme frequency rank (1 = most frequent)
sorted_tb = sorted(tb_phon_freq, key=lambda p: -float(tb_phon_freq[p]))
tb_rank = {p: i + 1 for i, p in enumerate(sorted_tb)}

def compute_corr(pairs: list[tuple[str, str]]) -> float:
    """Pearson r between Indus rank and TB phoneme rank for a set of sign→phoneme pairs."""
    xs = []
    ys = []
    for sign, phoneme in pairs:
        ir = indus_rank.get(sign)
        tr = tb_rank.get(phoneme)
        if ir is not None and tr is not None:
            xs.append(float(ir))
            ys.append(float(tr))
    if len(xs) < 3:
        return 0.0
    return pearson_r(xs, ys)

# ── Observed correlation ───────────────────────────────────────────────────────
obs_pairs = [(m, r) for m, r, _ in anchor_pairs]
observed_r = compute_corr(obs_pairs)
print(f"\nObserved Pearson r (Indus freq rank vs TB phoneme rank): {observed_r:.4f}")

# Also compute just HIGH anchors
high_pairs = [(m, r) for m, r, c in anchor_pairs if c == "HIGH"]
high_r = compute_corr(high_pairs)
print(f"HIGH-only correlation: {high_r:.4f}")

# ── Permutation test ───────────────────────────────────────────────────────────
N_PERMS = 10_000
rng = random.Random(42)

signs   = [m for m, _, _ in anchor_pairs]
phonemes = [r for _, r, _ in anchor_pairs]

perm_rs = []
for _ in range(N_PERMS):
    shuffled = phonemes[:]
    rng.shuffle(shuffled)
    r = compute_corr(list(zip(signs, shuffled)))
    perm_rs.append(r)

perm_rs.sort()

# p-value: fraction of permutations with r ≥ observed (one-sided, positive direction)
# Note: high NEGATIVE correlation is also interesting (inverse mapping)
pval_pos = sum(1 for r in perm_rs if r >= observed_r) / N_PERMS
pval_neg = sum(1 for r in perm_rs if r <= observed_r) / N_PERMS
pval = min(pval_pos, pval_neg) * 2  # two-sided

null_mean = sum(perm_rs) / len(perm_rs)
null_std  = math.sqrt(sum((r - null_mean)**2 for r in perm_rs) / len(perm_rs))
z_score   = (observed_r - null_mean) / null_std if null_std > 0 else 0.0

# 95% CI of null distribution
ci_lo = perm_rs[int(0.025 * N_PERMS)]
ci_hi = perm_rs[int(0.975 * N_PERMS)]

print(f"\nPermutation test ({N_PERMS} permutations):")
print(f"  Null mean r = {null_mean:.4f} ± {null_std:.4f}")
print(f"  95% CI: [{ci_lo:.4f}, {ci_hi:.4f}]")
print(f"  Z-score: {z_score:.2f}")
print(f"  p-value (two-sided): {pval:.4f}")
print(f"  Significance: {'YES (p<0.05)' if pval < 0.05 else 'NO'}")

# ── Save ──────────────────────────────────────────────────────────────────────
result = {
    "observed_r": round(observed_r, 6),
    "high_only_r": round(high_r, 6),
    "n_pairs": len(obs_pairs),
    "n_high_pairs": len(high_pairs),
    "n_permutations": N_PERMS,
    "null_mean": round(null_mean, 6),
    "null_std": round(null_std, 6),
    "null_95pct_ci": [round(ci_lo, 4), round(ci_hi, 4)],
    "z_score": round(z_score, 3),
    "p_value_two_sided": round(pval, 6),
    "p_value_positive": round(pval_pos, 6),
    "significant_at_05": pval < 0.05,
    "verdict": (
        f"Observed Pearson r = {observed_r:.4f} between Indus sign frequency ranks and "
        f"Tamil-Brahmi phoneme frequency ranks (n={len(obs_pairs)} pairs). "
        f"Permutation null (n={N_PERMS}): mean={null_mean:.4f} ± {null_std:.4f}, "
        f"Z={z_score:.2f}, p={pval:.4f} (two-sided). "
        f"{'SIGNIFICANT' if pval < 0.05 else 'NOT SIGNIFICANT'} at α=0.05."
    ),
    "_citation": {"primary": ["A.1", "A.12", "C.2"], "phase": "Phase-33"},
}

out_path = REPORTS / "phase33_tb_corr_significance.json"
out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"\nSaved to {out_path}")

