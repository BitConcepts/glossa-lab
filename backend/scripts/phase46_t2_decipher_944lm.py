"""Phase-46 T2: Decipher Pipeline Run — 944-LM + M267 Constraint.

Phase-44 T3 confirmed: Dravidian 3.13x lift over null (z=12.1) using 944-bigram LM.
M267 is now hypothesised as a GRAMMATICAL_PARTICLE (Phase-45 T2: entropy=0.852,
M267→M099 formula 84x).

This script tests whether pinning M267 to specific Proto-Dravidian function word
tokens IMPROVES the Dravidian SA lift — i.e., whether constraining the grammatical
particle reading makes the overall cipher alignment stronger.

Candidate M267 readings (medial grammatical particle, precedes kol/kol title):
  - 'in'  : genitive "of" → "[identity] of kol" = "[person]'s lord"
  - 'um'  : inclusive connective "and/also" → additive particle
  - 'e'   : emphatic particle → "[identity]-e kol" = "indeed kol"
  - 'an'  : masculine verbal suffix (but conflicts with M176=an)
  - 'al'  : negative/abstract suffix
  - 'atu' : neuter/abstract nominaliser
  - 'ir'  : 2nd person plural pronoun
  BASELINE: no constraint (free SA, same as Phase-44 T3)

GPU: uses BigramScorer (CuPy/NumPy vectorized) from glossa_lab.pipelines.decipher.
     torch checked first for CUDA availability.

Output: reports/phase46_t2_decipher_944lm.json
"""
from __future__ import annotations

import csv, json, math, random, sys, time
from collections import Counter
from pathlib import Path
from types import SimpleNamespace

REPO = Path(__file__).parents[2]
sys.path.insert(0, str(REPO / "backend"))

try:
    import torch
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"[GPU] torch {torch.__version__} — device: {DEVICE}")
except ImportError:
    DEVICE = "cpu"
    print("[GPU] torch not available — CPU only")

HOLDAT_CSV = REPO / "corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv"
DATA       = REPO / "backend/glossa_lab/data"
REPORTS    = REPO / "reports"
REPORTS.mkdir(exist_ok=True)
OUT        = REPORTS / "phase46_t2_decipher_944lm.json"
ANCHORS    = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"

# SA parameters (reduced from Phase-44 T3 for speed; enough for comparison)
N_RESTARTS = 5
MAX_ITER   = 20_000
SA_TEMP    = 1.0
SA_COOL    = 0.9997
N_SEEDS    = 5
RANDOM_SEEDS = list(range(N_SEEDS))

# M267 candidate readings
M267_CANDIDATES = {
    "BASELINE":  None,   # no constraint — free SA
    "in":  "in",         # genitive "of"
    "um":  "um",         # connective "and/also"
    "e":   "e",          # emphatic
    "al":  "al",         # negative/abstract
    "atu": "atu",        # neuter nominaliser
    "ir":  "ir",         # 2nd person plural
}


def load_corpus() -> tuple[list[str], list[list[str]]]:
    seals: dict[str, list[tuple[int, str]]] = {}
    with open(HOLDAT_CSV, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            sign = (row.get("letters") or "").strip()
            cisi = (row.get("cisi_number") or "").strip()
            pos = int(row.get("position") or 0)
            if cisi not in seals:
                seals[cisi] = []
            seals[cisi].append((pos, sign))
    inscriptions = []
    for cisi in sorted(seals):
        signs = [s for _, s in sorted(seals[cisi]) if s]
        if signs:
            inscriptions.append(signs)
    flat = [s for insc in inscriptions for s in insc]
    return flat, inscriptions


def load_lm(path: Path) -> dict[tuple[str, str], float]:
    raw = json.loads(path.read_text("utf-8"))
    bigrams = raw.get("bigrams", {})
    total = sum(bigrams.values()) or 1
    return {
        tuple(k.split(",", 1)): v / total
        for k, v in bigrams.items() if "," in k
    }


def build_scorer(bigram_prob: dict, flat: list[str]):
    from glossa_lab.pipelines.decipher import BigramScorer
    tc: Counter = Counter()
    for (a, b) in bigram_prob:
        tc[a] += 1; tc[b] += 1
    ranked = [t for t, _ in tc.most_common()]
    mock_lm = SimpleNamespace(ranked=ranked, bigram_freq=bigram_prob)
    return BigramScorer(mock_lm, flat)


def run_sa(
    flat: list[str],
    bigram_prob: dict,
    scorer,
    seed: int,
    pinned: dict[str, str] | None = None,
) -> dict:
    rng = random.Random(seed)
    cipher_alpha = sorted(set(flat))
    target_tokens = sorted(set(t for pair in bigram_prob for t in pair))

    # Extend target if smaller than cipher
    while len(target_tokens) < len(cipher_alpha):
        target_tokens.append(f"?{len(target_tokens)}")

    pinned = pinned or {}
    free_cipher = [c for c in cipher_alpha if c not in pinned]

    def _init(shuffle: bool) -> dict[str, str]:
        # Start with pinned mappings, then freely assign the rest
        mapping: dict[str, str] = dict(pinned)
        # Exclude pinned target tokens from free pool
        used_tgt = set(mapping.values())
        pool = [t for t in target_tokens[:len(cipher_alpha)] if t not in used_tgt]
        if shuffle:
            rng.shuffle(pool)
        for c, t in zip(free_cipher, pool):
            mapping[c] = t
        return mapping

    best_mapping: dict[str, str] = {}
    best_score = float("-inf")

    for restart in range(N_RESTARTS):
        mapping = _init(shuffle=(restart > 0))
        score = scorer.score_full(mapping)
        temp = SA_TEMP

        for _ in range(MAX_ITER):
            # Only swap FREE cipher symbols
            if len(free_cipher) < 2:
                break
            i, j = rng.sample(range(len(free_cipher)), 2)
            ca, cb = free_cipher[i], free_cipher[j]
            mapping[ca], mapping[cb] = mapping[cb], mapping[ca]
            new_score = scorer.score_full(mapping)
            delta = new_score - score
            if delta > 0 or (temp > 0 and rng.random() < math.exp(min(delta / temp, 0))):
                score = new_score
            else:
                mapping[ca], mapping[cb] = mapping[cb], mapping[ca]
            temp *= SA_COOL

        if score > best_score:
            best_score = score
            best_mapping = dict(mapping)

    return {"best_score": best_score, "best_mapping": best_mapping}


def null_score_estimate(flat: list[str], bigram_prob: dict, scorer, n: int = 50) -> tuple[float, float]:
    """Estimate null model score via random permutations."""
    cipher_alpha = sorted(set(flat))
    target_tokens = sorted(set(t for pair in bigram_prob for t in pair))
    while len(target_tokens) < len(cipher_alpha):
        target_tokens.append(f"?{len(target_tokens)}")
    scores = []
    rng = random.Random(42)
    for _ in range(n):
        tgt = list(target_tokens[:len(cipher_alpha)])
        rng.shuffle(tgt)
        m = dict(zip(cipher_alpha, tgt))
        scores.append(scorer.score_full(m))
    mu = sum(scores) / len(scores)
    std = math.sqrt(sum((s - mu)**2 for s in scores) / len(scores)) or 1.0
    return mu, std


def main() -> None:
    print("Phase-46 T2: Decipher Pipeline — 944-LM + M267 Constraint\n")

    flat, inscriptions = load_corpus()
    print(f"Corpus: {len(inscriptions)} inscriptions, {len(flat)} signs, "
          f"{len(set(flat))} unique")

    lm_path = DATA / "dravidian_tamil_lm.json"
    bigram_prob = load_lm(lm_path)
    print(f"LM: {len(bigram_prob)} bigrams ({json.loads(lm_path.read_text())['n_bigrams']} total)")

    scorer = build_scorer(bigram_prob, flat)

    # Load known HIGH anchors for M267 context
    anchors = json.loads(ANCHORS.read_text("utf-8"))["anchors"] if ANCHORS.exists() else {}

    # Null model estimate (done once, shared across conditions)
    print("\nEstimating null model (50 random permutations)…")
    null_mu, null_std = null_score_estimate(flat, bigram_prob, scorer, n=50)
    print(f"  Null: mean={null_mu:.1f}, std={null_std:.1f}")

    results_by_condition: dict[str, dict] = {}

    for cond_name, m267_token in M267_CANDIDATES.items():
        pinned: dict[str, str] | None = None
        if m267_token is not None:
            # Check if M267 exists in the cipher alphabet
            if "M267" in set(flat):
                # Map the Tamil token into the bigram LM's target vocabulary
                # Find the closest matching token in the LM vocabulary
                all_targets = sorted(set(t for pair in bigram_prob for t in pair))
                if m267_token in all_targets:
                    pinned = {"M267": m267_token}
                else:
                    # Use first token that starts with the candidate
                    match = next((t for t in all_targets if t.startswith(m267_token[:2])), m267_token)
                    pinned = {"M267": match}
                    m267_token = match
            else:
                print(f"  [SKIP] M267 not in corpus — cannot pin")
                pinned = None

        print(f"\n[{cond_name}] M267 → {m267_token or 'free'}, "
              f"{len(pinned or {})} pinned mappings")
        t0 = time.perf_counter()

        seed_scores = []
        seed_mappings = []
        for seed in RANDOM_SEEDS:
            r = run_sa(flat, bigram_prob, scorer, seed, pinned=pinned)
            seed_scores.append(r["best_score"])
            seed_mappings.append(r["best_mapping"])

        elapsed = time.perf_counter() - t0
        best_score = max(seed_scores)
        mean_score = sum(seed_scores) / len(seed_scores)
        z = (mean_score - null_mu) / null_std if null_std else 0
        lift = mean_score / null_mu if null_mu else 0

        print(f"  Best score: {best_score:.1f}, Mean: {mean_score:.1f}, "
              f"Z={z:.2f}, Lift={lift:.4f}x  ({elapsed:.1f}s)")

        results_by_condition[cond_name] = {
            "m267_token": m267_token,
            "pinned_mappings": pinned or {},
            "seed_scores": seed_scores,
            "best_score": round(best_score, 3),
            "mean_score": round(mean_score, 3),
            "z_score": round(z, 3),
            "lift": round(lift, 4),
            "elapsed_secs": round(elapsed, 1),
        }

    # Find best condition
    baseline = results_by_condition.get("BASELINE", {})
    baseline_lift = baseline.get("lift", 0)
    best_cond = max(
        ((c, r["lift"]) for c, r in results_by_condition.items()),
        key=lambda x: x[1],
    )
    best_cond_name, best_lift = best_cond
    improvement = (best_lift - baseline_lift) / abs(baseline_lift) if baseline_lift else 0

    print(f"\n=== M267 Constraint Results ===")
    print(f"Baseline lift: {baseline_lift:.4f}x")
    print(f"Best constraint: {best_cond_name} → {best_lift:.4f}x (+{improvement:.1%})")

    if best_cond_name != "BASELINE" and improvement > 0.01:
        verdict = "CONSTRAINT_IMPROVES_FIT"
        note = (f"Pinning M267 = '{best_cond_name}' improves Dravidian lift by {improvement:.1%} "
                f"({baseline_lift:.3f}x → {best_lift:.3f}x). Supports this as the M267 reading.")
    elif improvement < -0.01:
        verdict = "CONSTRAINT_DEGRADES_FIT"
        note = "All pin constraints degrade SA fit — M267's reading may be more complex."
    else:
        verdict = "CONSTRAINT_NEUTRAL"
        note = "Pinning M267 neither improves nor degrades fit significantly."

    print(f"Verdict: {verdict}")

    result = {
        "_citation": {"primary_sources": ["A.1"], "phase44_t3_lift": 3.13},
        "gpu_device": DEVICE,
        "corpus": {"n_inscriptions": len(inscriptions), "n_signs_flat": len(flat),
                   "n_unique_signs": len(set(flat))},
        "lm": {"n_bigrams": len(bigram_prob)},
        "null_model": {"mean": round(null_mu, 3), "std": round(null_std, 3)},
        "sa_params": {"n_restarts": N_RESTARTS, "max_iter": MAX_ITER,
                      "temp": SA_TEMP, "cooling": SA_COOL, "seeds": RANDOM_SEEDS},
        "conditions": results_by_condition,
        "best_condition": best_cond_name,
        "baseline_lift": round(baseline_lift, 4),
        "best_lift": round(best_lift, 4),
        "improvement_over_baseline": round(improvement, 4),
        "verdict": verdict,
        "verdict_note": note,
    }

    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), "utf-8")
    print(f"\nReport: {OUT}")


if __name__ == "__main__":
    main()
