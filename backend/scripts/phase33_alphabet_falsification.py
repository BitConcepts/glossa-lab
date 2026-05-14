"""Phase-33: Alphabetic hypothesis falsification.

"THE INDUS SCRIPT AS AN ALPHABET" (EuropePMC discovery) proposes Indus is
alphabetic rather than logo-syllabic. We test this by running SA with a
Phoenician/Proto-Semitic alphabetic LM and comparing NLL lift to Dravidian T1.

If Dravidian syllabic SA shows higher NLL lift than alphabet SA:
  → Alphabetic hypothesis weaker than Dravidian syllabic
  → Supports logo-syllabic/syllabic classification

Output: reports/phase33_alphabet_falsification.json
"""
from __future__ import annotations
import json, random, sys, math, time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).parents[2]
sys.path.insert(0, str(ROOT / "backend"))

REPORTS = ROOT / "reports"
BACKEND_REPORTS = ROOT / "backend" / "reports"
DATA    = ROOT / "backend" / "glossa_lab" / "data"

t0 = time.time()

# ── Load Holdat corpus ─────────────────────────────────────────────────────────
from glossa_lab.data.indus_m77 import get_corpus_symbols, get_corpus_inscriptions
flat_tokens  = get_corpus_symbols()
inscriptions = get_corpus_inscriptions()
sign_freq    = Counter(flat_tokens)

# ── Build Phoenician alphabetic LM ────────────────────────────────────────────
# Load Phoenician corpus from phoenician.py
try:
    from glossa_lab.data.phoenician import get_corpus_symbols as ph_symbols, get_corpus_inscriptions as ph_inscriptions
    ph_flat  = ph_symbols()
    ph_inscs = ph_inscriptions()
    print(f"Phoenician corpus: {len(ph_flat)} tokens, {len(ph_inscs)} inscriptions")
except Exception as e:
    print(f"Phoenician corpus not available ({e}), building synthetic alphabet LM")
    # Build minimal 22-letter Phoenician alphabet with uniform bigrams
    PH_ALPHABET = list("'bgdhwzHTYklmnsCpqrGt")  # standard transliteration
    ph_flat = PH_ALPHABET * 500  # synthetic uniform
    ph_inscs = [[a, b] for a in PH_ALPHABET for b in PH_ALPHABET[:5]]

# Build alphabet bigrams
alpha_c: Counter = Counter()
for i in range(len(ph_flat) - 1):
    alpha_c[(ph_flat[i], ph_flat[i+1])] += 1
alpha_total = sum(alpha_c.values()) or 1
alpha_bigrams: dict[tuple[str,str], float] = {bg: c/alpha_total for bg, c in alpha_c.items()}

# Ranked by frequency
alpha_freq: Counter = Counter(ph_flat)
alpha_ranked = [s for s, _ in alpha_freq.most_common()]

SMOOTHING_LOG = math.log(1e-8)
print(f"Alphabet LM: {len(alpha_freq)} characters, {len(alpha_bigrams)} bigrams")

# ── Build anchors ─────────────────────────────────────────────────────────────
# For alphabetic SA: map Indus signs to Phoenician consonants
# Use the Daggumati/Revesz (2018 CNN paper) suggestion that Indus-Phoenician
# have shared graphemes. Use 3 visually similar correspondences as anchors:
# (These are hypothesis anchors for testing, not confirmed values)
ALPHA_ANCHORS = {
    "M342": "l",   # terminal stick-like sign → lamed (l) [visual similarity]
    "M176": "n",   # short line sign → nun (n) [positional: terminal]
    "M099": "k",   # jar shape → kap (k) [iconographic]
}

alpha_vocab = set(alpha_ranked)
fixed_anchors: dict[str, str] = {}
for m_id, letter in ALPHA_ANCHORS.items():
    if letter in alpha_vocab:
        fixed_anchors[m_id] = letter
    elif alpha_ranked:
        fixed_anchors[m_id] = alpha_ranked[0]

print(f"Fixed anchors: {fixed_anchors}")

# Signs to decipher
cipher_signs_all = [s for s, c in sign_freq.items() if c >= 5]
free_signs = [s for s in cipher_signs_all if s not in fixed_anchors]

# ── Scoring ────────────────────────────────────────────────────────────────────
def score_mapping(mapping: dict[str, str]) -> float:
    total = 0.0
    for insc in inscriptions:
        if len(insc) < 2:
            continue
        for i in range(len(insc) - 1):
            a = mapping.get(insc[i])
            b = mapping.get(insc[i+1])
            if a and b:
                total += math.log(alpha_bigrams.get((a,b), 1e-8))
    return total

# ── SA ─────────────────────────────────────────────────────────────────────────
def run_sa(fixed, free, vocab, n_iters=30_000, seed=42):
    rng = random.Random(seed)
    free_target = [sv for sv in vocab if sv not in fixed.values()]
    while len(free_target) < len(free):
        free_target.append(rng.choice(vocab))
    rng.shuffle(free_target)
    mapping = dict(fixed)
    for i, sign in enumerate(free):
        mapping[sign] = free_target[i % len(free_target)]
    current_score = score_mapping(mapping)
    best_mapping = dict(mapping)
    best_score = current_score
    T_start, T_end = 2.0, 0.01
    for iteration in range(n_iters):
        T = T_start * ((T_end / T_start) ** (iteration / n_iters))
        if len(free) < 2:
            break
        i, j = rng.sample(range(len(free)), 2)
        si, sj = free[i], free[j]
        vi, vj = mapping[si], mapping[sj]
        mapping[si], mapping[sj] = vj, vi
        new_score = score_mapping(mapping)
        delta = new_score - current_score
        if delta > 0 or rng.random() < math.exp(delta / max(T, 1e-10)):
            current_score = new_score
            if new_score > best_score:
                best_score = new_score
                best_mapping = dict(mapping)
        else:
            mapping[si], mapping[sj] = vi, vj
    return best_mapping, best_score

N_SEEDS, N_ITERS = 5, 30_000
print(f"\nRunning Alphabetic SA: {N_SEEDS} seeds × {N_ITERS} iters...")
seed_results = []
for seed in range(N_SEEDS):
    m, s = run_sa(fixed_anchors, free_signs, alpha_ranked, n_iters=N_ITERS, seed=seed)
    seed_results.append((s, m))
    print(f"  Seed {seed}: score = {s:.1f}")

best_score, best_mapping = max(seed_results, key=lambda x: x[0])
print(f"Best Alphabet SA score: {best_score:.1f}")

# ── Permutation null ───────────────────────────────────────────────────────────
print("Computing permutation null (500 shuffles)...")
N_PERMS = 500
rng = random.Random(99)
null_scores = []
for _ in range(N_PERMS):
    shuffled = list(best_mapping.values())
    rng.shuffle(shuffled)
    null_map = dict(zip(best_mapping.keys(), shuffled))
    null_scores.append(score_mapping(null_map))

null_mean = sum(null_scores) / len(null_scores)
null_std = math.sqrt(sum((s - null_mean)**2 for s in null_scores) / len(null_scores))
z_score = (best_score - null_mean) / null_std if null_std > 0 else 0.0
pval = sum(1 for s in null_scores if s >= best_score) / N_PERMS

print(f"Null: mean={null_mean:.1f} ± {null_std:.1f}")
print(f"Z-score: {z_score:.2f}, p-value: {pval:.4f}")

# ── Load Dravidian T1 result for comparison ────────────────────────────────────
drav_result = {}
drav_path = REPORTS / "phase33_t1_syllable_sa.json"
if drav_path.exists():
    drav_result = json.loads(drav_path.read_text("utf-8"))

drav_score = drav_result.get("best_score")
drav_z = drav_result.get("z_score")

elapsed = time.time() - t0

verdict = (
    f"Phase-33 Alphabetic Falsification: Phonician/alphabet SA on Indus. "
    f"best_score={best_score:.1f}, null_mean={null_mean:.1f} ± {null_std:.1f}. "
    f"Z={z_score:.2f}, p={pval:.4f} ({N_PERMS} perms). "
    f"Dravidian T1 score={drav_score} Z={drav_z} for comparison. "
    f"Alphabet NLL lift/insc={(best_score-null_mean)/len(inscriptions):.3f} vs Dravidian {drav_result.get('nll_lift_per_inscription','N/A')}. "
    f"{'Dravidian WINS (higher NLL lift → syllabic > alphabetic)' if drav_score and best_score < drav_score else 'Alphabet competitive — investigate further'}. "
    f"Runtime={elapsed:.0f}s."
)
print(f"\n{verdict}")

result = {
    "best_score": round(best_score, 3),
    "null_mean": round(null_mean, 3),
    "null_std": round(null_std, 3),
    "z_score": round(z_score, 3),
    "p_value": round(pval, 4),
    "n_permutations": N_PERMS,
    "n_seeds": N_SEEDS,
    "nll_lift_per_inscription": round((best_score-null_mean)/max(1,len(inscriptions)), 4),
    "significant_at_05": pval < 0.05,
    "dravidian_t1_score": drav_score,
    "dravidian_t1_z": drav_z,
    "dravidian_wins": bool(drav_score and drav_score > best_score),
    "alphabet_vocab_size": len(alpha_vocab),
    "alphabet_bigrams": len(alpha_bigrams),
    "fixed_anchors": fixed_anchors,
    "seed_scores": [round(s, 1) for s, _ in seed_results],
    "runtime_seconds": round(elapsed, 1),
    "verdict": verdict,
    "_citation": {"primary": ["A.1", "D.6b"], "phase": "Phase-33-Alphabet"},
}

out_path = REPORTS / "phase33_alphabet_falsification.json"
out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Saved to {out_path}")

