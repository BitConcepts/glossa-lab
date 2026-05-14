"""Phase-33 T1: Syllable-level SA decipherment of Indus script.

Phase-32 T4 was NEUTRAL because signs were mapped to full Dravidian WORDS (e.g.,
"nalam", "erutu") and scored against a word-bigram LM — a vocabulary mismatch.
The correct approach: map each Indus sign → ONE Dravidian SYLLABLE and score
with the syllable-bigram LM (already built: dravidian_syllable_lm.json).

Method:
  1. Build a LanguageModel-compatible object from dravidian_syllable_lm.json.
  2. Build anchors: HIGH-confidence monosyllabic signs fixed (M342→ay, M176→an, M099→kol).
  3. Run SA on the ~57 free (non-fixed) signs to find optimal syllable assignments.
  4. Score: compute NLL under syllable LM for observed mapping vs 1000 random permutations.
  5. Verdict: if p < 0.05 and NLL lift > 0, the syllable SA is discriminative.

Output: reports/phase33_t1_syllable_sa.json
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
print(f"Holdat: {len(flat_tokens)} tokens, {len(sign_freq)} distinct signs, {len(inscriptions)} inscriptions")

# ── Load syllable LM ───────────────────────────────────────────────────────────
syll_lm_raw = json.loads((DATA / "dravidian_syllable_lm.json").read_text("utf-8"))
# bigrams: {"syll1|syll2": logprob}
syll_bigrams: dict[tuple[str,str], float] = {}
for key, logp in syll_lm_raw["bigrams"].items():
    parts = key.split("|")
    if len(parts) == 2:
        syll_bigrams[(parts[0], parts[1])] = float(logp)

syll_vocab: list[str] = syll_lm_raw.get("vocab", [])
if not syll_vocab:
    # Reconstruct from bigrams
    vocab_set: set[str] = set()
    for (a, b) in syll_bigrams:
        vocab_set.add(a); vocab_set.add(b)
    syll_vocab = sorted(vocab_set)

# Unigram freq from bigrams
syll_unigram: Counter = Counter()
for (a, b) in syll_bigrams:
    syll_unigram[a] += 1
    syll_unigram[b] += 1
syll_ranked = [s for s, _ in syll_unigram.most_common()]

SMOOTHING_LOG = math.log(1e-8)
print(f"Syllable LM: {len(syll_vocab)} syllables, {len(syll_bigrams)} bigrams")

# ── Build anchor map ───────────────────────────────────────────────────────────
anchors_raw = json.loads((BACKEND_REPORTS / "INDUS_FINAL_ANCHORS.json").read_text("utf-8"))
all_anchors = anchors_raw["anchors"]

# Only use monosyllabic HIGH-confidence anchors as fixed constraints
# (Multi-syllable words like "erutu" are ambiguous for 1-sign→1-syllable mapping)
MONOSYLLABIC_RE_CHARS = set("aeiouāīūṛḷ")

def is_monosyllabic(reading: str) -> bool:
    """Rough check: a syllable has exactly one vowel cluster."""
    s = reading.split("/")[0].strip().lower()
    # Remove diacritics for counting
    clean = ""
    for ch in s:
        if ch.isalpha():
            clean += ch
    # Count vowel nuclei
    vowels = "aeiouāīūṛḷṉṟ"
    n_vowels = sum(1 for ch in clean if ch in vowels)
    return 1 <= n_vowels <= 2  # 1-2 vowel positions = monosyllabic or short bisyllabic

# Build syllable anchors: sign → syllable from HIGH/MEDIUM anchors
# Only use readings that exist in the syllable vocabulary (exact or substring match)
fixed_anchors: dict[str, str] = {}   # sign_id → syllable
for m_id, info in all_anchors.items():
    conf = info["confidence"]
    if conf not in ("HIGH", "MEDIUM"):
        continue
    reading = info["reading"].split("/")[0].strip()
    # Check: is reading itself in vocab?
    if reading in syll_vocab:
        if conf == "HIGH" or (conf == "MEDIUM" and m_id in ["M342","M176","M099","M062","M006","M045","M016","M367","M336"]):
            fixed_anchors[m_id] = reading
    else:
        # Try truncating to first syllable pattern (CV, CVC, V, VC)
        # Simple: take first 2-3 chars if vowel is present
        s = reading[:3].rstrip("ṇṭṉṟ")
        if s in syll_vocab:
            if conf == "HIGH":
                fixed_anchors[m_id] = s

# At minimum, use the 3 core HIGH monosyllabic anchors that are well-established
CORE_ANCHORS = {
    "M342": "ay",    # terminal marker (HIGH, Parpola)
    "M176": "an",    # masculine suffix (HIGH, Parpola)
    "M099": "kol",   # jar/vessel sign (HIGH)
}
for m_id, syll in CORE_ANCHORS.items():
    if syll in syll_vocab:
        fixed_anchors[m_id] = syll
    else:
        # Find closest syllable
        for sv in syll_vocab:
            if sv.startswith(syll[:2]):
                fixed_anchors[m_id] = sv
                break

print(f"Fixed anchors: {len(fixed_anchors)} (HIGH/MEDIUM with syllable readings)")
print(f"  Core: {[(k,v) for k,v in fixed_anchors.items() if k in CORE_ANCHORS]}")

# Signs to decipher (only those in corpus with freq >= 5)
cipher_signs_all = [s for s, c in sign_freq.items() if c >= 5]
free_signs = [s for s in cipher_signs_all if s not in fixed_anchors]
print(f"Free signs (not anchored, freq≥5): {len(free_signs)}")

# ── Scoring function ───────────────────────────────────────────────────────────
def score_mapping(mapping: dict[str, str]) -> float:
    """Compute total syllable bigram log-prob for inscriptions under this mapping.
    Signs not in mapping get SMOOTHING_LOG for any bigram they participate in.
    """
    total = 0.0
    for insc in inscriptions:
        if len(insc) < 2:
            continue
        for i in range(len(insc) - 1):
            a = mapping.get(insc[i])
            b = mapping.get(insc[i+1])
            if a and b:
                total += syll_bigrams.get((a, b), SMOOTHING_LOG)
    return total

# ── Simulated Annealing ────────────────────────────────────────────────────────
def run_sa(
    fixed: dict[str, str],
    free: list[str],
    target_vocab: list[str],
    n_iters: int = 30_000,
    seed: int = 42,
    T_start: float = 2.0,
    T_end: float = 0.01,
) -> tuple[dict[str, str], float]:
    """Simple SA over syllable assignments for free signs."""
    rng = random.Random(seed)
    # Initial mapping: fixed + frequency-rank seed for free signs
    free_target = [sv for sv in target_vocab if sv not in fixed.values()]
    rng.shuffle(free_target)
    # Pad or truncate to len(free)
    while len(free_target) < len(free):
        free_target.append(rng.choice(target_vocab))

    mapping = dict(fixed)
    for i, sign in enumerate(free):
        mapping[sign] = free_target[i % len(free_target)]

    current_score = score_mapping(mapping)
    best_mapping  = dict(mapping)
    best_score    = current_score

    for iteration in range(n_iters):
        T = T_start * ((T_end / T_start) ** (iteration / n_iters))
        # Pick two random free signs and swap their assignments
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
                best_score   = new_score
                best_mapping = dict(mapping)
        else:
            mapping[si], mapping[sj] = vi, vj  # revert

    return best_mapping, best_score

# ── Run SA with multiple seeds ─────────────────────────────────────────────────
N_SEEDS = 5
N_ITERS = 30_000
print(f"\nRunning SA: {N_SEEDS} seeds × {N_ITERS} iterations...")

seed_results = []
for seed in range(N_SEEDS):
    m, s = run_sa(fixed_anchors, free_signs, syll_ranked,
                  n_iters=N_ITERS, seed=seed)
    seed_results.append((s, m))
    print(f"  Seed {seed}: score = {s:.1f}")

best_score, best_mapping = max(seed_results, key=lambda x: x[0])
print(f"\nBest SA score: {best_score:.1f}")

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
null_std  = math.sqrt(sum((s - null_mean)**2 for s in null_scores) / len(null_scores))
z_score   = (best_score - null_mean) / null_std if null_std > 0 else 0.0
pval      = sum(1 for s in null_scores if s >= best_score) / N_PERMS

print(f"Null: mean={null_mean:.1f} ± {null_std:.1f}")
print(f"Z-score: {z_score:.2f}")
print(f"p-value: {pval:.4f}")
print(f"NLL lift (per inscription): {(best_score - null_mean) / len(inscriptions):.3f}")

# ── Top decoded inscriptions ───────────────────────────────────────────────────
def decode_inscription(insc: list[str], mapping: dict[str, str]) -> str:
    return "-".join(mapping.get(s, f"?{s}") for s in insc)

# Show best/longest decodable inscriptions (those with most mapped signs)
sample_decoded = []
for insc in sorted(inscriptions, key=len, reverse=True)[:20]:
    decoded = decode_inscription(insc, best_mapping)
    n_mapped = sum(1 for s in insc if s in best_mapping)
    sample_decoded.append({
        "signs": insc,
        "syllables": decoded,
        "n_mapped": n_mapped,
        "coverage": round(n_mapped / len(insc), 2),
    })

elapsed = time.time() - t0
verdict = (
    f"Phase-33 T1 Syllable SA: best_score={best_score:.1f}, null_mean={null_mean:.1f} ± {null_std:.1f}. "
    f"Z={z_score:.2f}, p={pval:.4f} ({N_PERMS} perms). "
    f"NLL lift per inscription={(best_score-null_mean)/len(inscriptions):.3f}. "
    f"{'SIGNIFICANT (p<0.05)' if pval < 0.05 else 'NOT SIGNIFICANT'}. "
    f"Fixed anchors={len(fixed_anchors)}, free={len(free_signs)}, seeds={N_SEEDS}. "
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
    "n_iters_per_seed": N_ITERS,
    "n_fixed_anchors": len(fixed_anchors),
    "n_free_signs": len(free_signs),
    "nll_lift_per_inscription": round((best_score - null_mean) / max(1, len(inscriptions)), 4),
    "significant_at_05": pval < 0.05,
    "fixed_anchors": fixed_anchors,
    "best_mapping_sample": {k: v for k, v in list(best_mapping.items())[:40]},
    "sample_decoded": sample_decoded[:10],
    "seed_scores": [round(s, 1) for s, _ in seed_results],
    "runtime_seconds": round(elapsed, 1),
    "verdict": verdict,
    "_citation": {"primary": ["A.1", "E.1", "C.2"], "phase": "Phase-33-T1"},
}

out_path = REPORTS / "phase33_t1_syllable_sa.json"
out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Saved to {out_path}")

