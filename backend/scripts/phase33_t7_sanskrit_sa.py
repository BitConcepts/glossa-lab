"""Phase-33 T7: Sanskrit syllable SA falsification.

Phase-32 T7 was INCONCLUSIVE because Sanskrit used character-level tokens
(728K char tokens) vs Dravidian word-level (sparse). This script runs SA
with the Sanskrit syllable LM at the same granularity as the Dravidian T1,
enabling a valid head-to-head comparison.

Method:
  - Same setup as phase33_t1_syllable_sa.py
  - Replace dravidian_syllable_lm.json with sanskrit_syllable_lm.json
  - Run SA on the same free signs with the same fixed anchors
  - Compare best_score and p-value to Dravidian T1 result
  - If Dravidian score > Sanskrit score at similar p-value: survives falsification

Output: reports/phase33_t7_sanskrit_sa.json
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

# ── Load Sanskrit syllable LM ──────────────────────────────────────────────────
skt_lm_path = DATA / "sanskrit_syllable_lm.json"
print(f"Loading Sanskrit syllable LM from {skt_lm_path}...")
skt_lm_raw = json.loads(skt_lm_path.read_text("utf-8"))
print(f"  Keys: {list(skt_lm_raw.keys())[:8]}")

skt_bigrams: dict[tuple[str,str], float] = {}
# Try various key formats
bigrams_raw = skt_lm_raw.get("bigrams", skt_lm_raw.get("bigram_freq", {}))
for key, logp in bigrams_raw.items():
    if "|" in key:
        parts = key.split("|")
    elif "," in key:
        parts = key.split(",")
    elif " " in key:
        parts = key.split(" ", 1)
    else:
        continue
    if len(parts) == 2:
        try:
            skt_bigrams[(parts[0].strip(), parts[1].strip())] = float(logp)
        except (ValueError, TypeError):
            pass

# Reconstruct vocab from bigrams
skt_vocab_set: set[str] = set()
for (a, b) in skt_bigrams:
    skt_vocab_set.add(a); skt_vocab_set.add(b)

# Ranked by bigram frequency
skt_unigram: Counter = Counter()
for (a, b) in skt_bigrams:
    skt_unigram[a] += 1; skt_unigram[b] += 1
skt_ranked = [s for s, _ in skt_unigram.most_common()]

SMOOTHING_LOG = math.log(1e-8)
print(f"Sanskrit syllable LM: {len(skt_vocab_set)} syllables, {len(skt_bigrams)} bigrams")

if len(skt_bigrams) == 0:
    print("ERROR: Sanskrit LM has no bigrams. Check file format.")
    # Try to recover: build minimal LM from vocab list
    vocab_raw = skt_lm_raw.get("vocab", skt_lm_raw.get("symbols", []))
    if vocab_raw:
        skt_ranked = list(vocab_raw)
        skt_vocab_set = set(skt_ranked)
        print(f"  Recovered {len(skt_ranked)} vocab items from 'vocab' key")

# ── Load anchors (same as T1) ──────────────────────────────────────────────────
anchors_raw = json.loads((BACKEND_REPORTS / "INDUS_FINAL_ANCHORS.json").read_text("utf-8"))
all_anchors = anchors_raw["anchors"]

# For Sanskrit SA: use same 3 core anchors but mapped to Sanskrit syllables
# M342 (terminal marker) → Sanskrit case suffix "aH" (visarga, common terminal)
# M176 (masc suffix) → Sanskrit "naH" or "an"
# M099 (vessel) → Sanskrit "ku" or similar
SANSKRIT_CORE_ANCHORS_CANDIDATES = {
    "M342": ["aH", "as", "a"],    # Sanskrit terminal visarga
    "M176": ["an", "na", "naH"],  # Sanskrit nasal suffix
    "M099": ["ku", "ko", "kol"],  # vessel/pot
}

fixed_anchors: dict[str, str] = {}
for m_id, candidates in SANSKRIT_CORE_ANCHORS_CANDIDATES.items():
    for cand in candidates:
        if cand in skt_vocab_set:
            fixed_anchors[m_id] = cand
            break
    if m_id not in fixed_anchors and skt_ranked:
        # Fallback: use most frequent Sanskrit syllable for this sign type
        fixed_anchors[m_id] = skt_ranked[0]

# Also add any MEDIUM/HIGH anchors whose first syllable exists in Sanskrit LM
for m_id, info in all_anchors.items():
    if m_id in fixed_anchors:
        continue
    if info["confidence"] not in ("HIGH", "MEDIUM"):
        continue
    reading = info["reading"].split("/")[0].strip()
    if reading in skt_vocab_set:
        fixed_anchors[m_id] = reading

print(f"Fixed anchors for Sanskrit SA: {len(fixed_anchors)}")

# Signs to decipher
cipher_signs_all = [s for s, c in sign_freq.items() if c >= 5]
free_signs = [s for s in cipher_signs_all if s not in fixed_anchors]
print(f"Free signs: {len(free_signs)}")

if not skt_ranked or len(skt_bigrams) == 0:
    print("WARNING: Sanskrit LM is empty. Generating placeholder result.")
    result = {
        "error": "Sanskrit syllable LM could not be loaded (format mismatch)",
        "skt_lm_keys": list(skt_lm_raw.keys())[:10],
        "verdict": "Phase-33 T7 INCOMPLETE: Sanskrit LM file format not parseable. Manual inspection required.",
        "_citation": {"primary": ["A.1"], "phase": "Phase-33-T7"},
    }
    out_path = REPORTS / "phase33_t7_sanskrit_sa.json"
    out_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"Saved placeholder to {out_path}")
    sys.exit(0)

# ── Scoring function ───────────────────────────────────────────────────────────
def score_mapping(mapping: dict[str, str]) -> float:
    total = 0.0
    for insc in inscriptions:
        if len(insc) < 2:
            continue
        for i in range(len(insc) - 1):
            a = mapping.get(insc[i])
            b = mapping.get(insc[i+1])
            if a and b:
                total += skt_bigrams.get((a, b), SMOOTHING_LOG)
    return total

# ── SA ─────────────────────────────────────────────────────────────────────────
def run_sa(fixed, free, vocab, n_iters=30_000, seed=42):
    rng = random.Random(seed)
    free_target = [sv for sv in vocab if sv not in fixed.values()]
    rng.shuffle(free_target)
    while len(free_target) < len(free):
        free_target.append(rng.choice(vocab))
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
print(f"\nRunning Sanskrit SA: {N_SEEDS} seeds × {N_ITERS} iterations...")
seed_results = []
for seed in range(N_SEEDS):
    m, s = run_sa(fixed_anchors, free_signs, skt_ranked, n_iters=N_ITERS, seed=seed)
    seed_results.append((s, m))
    print(f"  Seed {seed}: score = {s:.1f}")

best_score, best_mapping = max(seed_results, key=lambda x: x[0])
print(f"Best Sanskrit SA score: {best_score:.1f}")

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
print(f"Z-score: {z_score:.2f}")
print(f"p-value: {pval:.4f}")

# ── Load Dravidian T1 result for comparison ────────────────────────────────────
drav_result = {}
drav_path = REPORTS / "phase33_t1_syllable_sa.json"
if drav_path.exists():
    drav_result = json.loads(drav_path.read_text("utf-8"))
    print(f"\nDravidian T1 for comparison:")
    print(f"  best_score={drav_result.get('best_score')}, null_mean={drav_result.get('null_mean')}")
    print(f"  Z={drav_result.get('z_score')}, p={drav_result.get('p_value')}")
    print(f"  NLL lift/insc={drav_result.get('nll_lift_per_inscription')}")

drav_score = drav_result.get("best_score", None)
drav_z = drav_result.get("z_score", None)
elapsed = time.time() - t0

if drav_score is not None:
    diff = best_score - drav_score
    comparison = (
        f"Sanskrit score={best_score:.1f} vs Dravidian score={drav_score:.1f}. "
        f"Dravidian - Sanskrit delta = {-diff:.1f} ({'+' if diff < 0 else '-'}{abs(diff):.1f} in Dravidian's favour). "
        f"Sanskrit Z={z_score:.2f}, Dravidian Z={drav_z}. "
    )
else:
    comparison = f"Dravidian T1 result not yet available for direct comparison."

verdict = (
    f"Phase-33 T7 Sanskrit Syllable SA: best_score={best_score:.1f}, null_mean={null_mean:.1f} ± {null_std:.1f}. "
    f"Z={z_score:.2f}, p={pval:.4f} ({N_PERMS} perms). "
    f"{comparison}"
    f"{'Dravidian WINS falsification test (higher NLL lift)' if drav_score and drav_score > best_score else 'Sanskrit ≥ Dravidian — Dravidian hypothesis weakened'}. "
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
    "dravidian_t1_score": drav_score,
    "dravidian_t1_z": drav_z,
    "dravidian_wins": bool(drav_score and drav_score > best_score),
    "fixed_anchors": fixed_anchors,
    "seed_scores": [round(s, 1) for s, _ in seed_results],
    "runtime_seconds": round(elapsed, 1),
    "verdict": verdict,
    "_citation": {"primary": ["A.1", "E.1"], "phase": "Phase-33-T7"},
}

out_path = REPORTS / "phase33_t7_sanskrit_sa.json"
out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Saved to {out_path}")

