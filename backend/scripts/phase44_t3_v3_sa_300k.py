"""Phase-44 T3: V3 Corpus SA at 300K iterations — Convergence Verification.

Runs Simulated Annealing on the Holdat corpus (V3 = the cleaned Holdat LLC CSV)
using:
  - Dravidian Tamil LM (944 bigrams, TamilTB-expanded; phase44_rebuild_dravidian_lm.py)
  - Sanskrit syllable LM (comparison baseline)
  - 10 restarts × 30,000 iterations per seed = 300K total per language

Objective:
  Confirm that Phase-38/41 Dravidian advantage (1.056x lift) holds at
  higher iteration count. 300K is the convergence threshold for reliable
  replication per the research plan.

GPU: Uses BigramScorer from glossa_lab.pipelines.decipher, which auto-selects
  CuPy (GPU) > NumPy (CPU). Scoring is vectorized matrix lookup,
  50-200x faster than the Python loop on CPU.

Output: reports/phase44_t3_v3_sa_300k.json
"""
from __future__ import annotations

import csv
import json
import math
import random
import sys
import time
from collections import Counter
from pathlib import Path
from types import SimpleNamespace

REPO = Path(__file__).parents[2]
sys.path.insert(0, str(REPO / "backend"))

HOLDAT_CSV = REPO / "corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv"
DATA = REPO / "backend/glossa_lab/data"
REPORTS = REPO / "reports"
REPORTS.mkdir(exist_ok=True)

OUT_FILE = REPORTS / "phase44_t3_v3_sa_300k.json"

# ── SA parameters ──────────────────────────────────────────────────────────
N_RESTARTS = 10              # restarts per seed
MAX_ITER = 30_000            # iterations per restart → 300K per seed
SA_TEMP_START = 1.0
SA_COOLING = 0.9997          # slower cooling to match 30K budget
RANDOM_SEEDS = list(range(10))


# ── Corpus loading ───────────────────────────────────────────────────────────────

def load_holdat() -> tuple[list[str], list[list[str]]]:
    """Load Holdat corpus. Returns (flat_signs, inscriptions)."""
    seals: dict[str, list[tuple[int, str]]] = {}
    with open(HOLDAT_CSV, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            sign = row.get("letters", "").strip()
            cisi = row.get("cisi_number", "").strip()
            pos = int(row.get("position", 0))
            if cisi not in seals:
                seals[cisi] = []
            seals[cisi].append((pos, sign))

    inscriptions: list[list[str]] = []
    for cisi_no in sorted(seals):
        pairs = sorted(seals[cisi_no])
        signs = [s for _, s in pairs if s]
        if signs:
            inscriptions.append(signs)

    flat = [s for insc in inscriptions for s in insc]
    return flat, inscriptions


# ── LM loading ────────────────────────────────────────────────────────────────────

def load_dravidian_lm() -> dict[tuple[str, str], float]:
    """Load Dravidian Tamil bigram LM (944 bigrams, TamilTB-expanded)."""
    lm_data = json.loads((DATA / "dravidian_tamil_lm.json").read_text("utf-8"))
    bigrams_raw = lm_data.get("bigrams", {})
    total = sum(bigrams_raw.values()) or 1
    # Keys use comma separator: "a,k" -> ("a", "k")
    return {
        tuple(k.split(",", 1)): v / total  # type: ignore[misc]
        for k, v in bigrams_raw.items()
        if "," in k
    }


def load_sanskrit_lm() -> dict[tuple[str, str], float]:
    """Load Sanskrit syllable bigram LM."""
    lm_data = json.loads((DATA / "sanskrit_syllable_lm.json").read_text("utf-8"))
    bigrams_raw = lm_data.get("bigrams", {})
    if not bigrams_raw:
        bigrams_raw = lm_data.get("bigram_freq", {})
    if not bigrams_raw:
        symbols = lm_data.get("symbols", [])
        if symbols:
            counts: Counter = Counter()
            for i in range(len(symbols) - 1):
                counts[(symbols[i], symbols[i + 1])] += 1
            total = sum(counts.values()) or 1
            return {k: v / total for k, v in counts.items()}
        return {}
    total = sum(bigrams_raw.values()) or 1
    result = {}
    for k, v in bigrams_raw.items():
        if "|" in k:
            parts = tuple(k.split("|", 1))
        elif isinstance(k, (list, tuple)) and len(k) == 2:
            parts = tuple(k)
        else:
            continue
        result[parts] = v / total  # type: ignore[assignment]
    return result


# ── GPU-backed scorer via BigramScorer ───────────────────────────────────────────

def build_scorer(bigram_prob: dict[tuple[str, str], float], flat: list[str]):
    """Build a BigramScorer (GPU if CuPy available, otherwise NumPy).

    BigramScorer expects a model with .ranked (frequency-ranked token list)
    and .bigram_freq (dict of (a,b)->probability, NOT log-prob).
    """
    from glossa_lab.pipelines.decipher import BigramScorer  # noqa: PLC0415

    # Rank target tokens by frequency across all bigrams
    token_counts: Counter = Counter()
    for (a, b), p in bigram_prob.items():
        token_counts[a] += p
        token_counts[b] += p
    ranked = [t for t, _ in token_counts.most_common()]

    # Build mock model namespace (BigramScorer only needs .ranked + .bigram_freq)
    mock_lm = SimpleNamespace(
        ranked=ranked,
        bigram_freq=bigram_prob,  # probabilities, not log-probs
    )
    return BigramScorer(mock_lm, flat)


# ── SA engine (GPU-accelerated via BigramScorer) ───────────────────────────────

SMOOTHING = math.log(1e-8)


def run_sa(
    flat: list[str],
    bigram_prob: dict[tuple[str, str], float],
    scorer,  # BigramScorer instance (shared across seeds for this LM)
    seed: int,
) -> dict:
    """Run SA on the flat sign sequence using GPU-backed scorer."""
    rng = random.Random(seed)
    cipher_alphabet = sorted(set(flat))
    target_tokens = sorted(set(t for pair in bigram_prob for t in pair))

    # Extend target if smaller than cipher
    while len(target_tokens) < len(cipher_alphabet):
        target_tokens.append(f"?{len(target_tokens)}")

    def _init(shuffle: bool) -> dict[str, str]:
        tgt = list(target_tokens[: len(cipher_alphabet)])
        if shuffle:
            rng.shuffle(tgt)
        return dict(zip(cipher_alphabet, tgt))

    best_mapping: dict[str, str] = {}
    best_score = float("-inf")

    for restart in range(N_RESTARTS):
        mapping = _init(shuffle=(restart > 0))
        score = scorer.score_full(mapping)  # vectorized GPU/NumPy scoring
        temp = SA_TEMP_START

        for _ in range(MAX_ITER):
            i, j = rng.sample(range(len(cipher_alphabet)), 2)
            ca, cb = cipher_alphabet[i], cipher_alphabet[j]
            mapping[ca], mapping[cb] = mapping[cb], mapping[ca]
            new_score = scorer.score_full(mapping)
            delta = new_score - score
            if delta > 0 or (temp > 0 and rng.random() < math.exp(delta / temp)):
                score = new_score
            else:
                mapping[ca], mapping[cb] = mapping[cb], mapping[ca]
            temp *= SA_COOLING

        if score > best_score:
            best_score = score
            best_mapping = dict(mapping)

    return {"best_score": best_score, "best_mapping": best_mapping}


# ── Null model for lift calculation ─────────────────────────────────────────────

def null_score(
    flat: list[str],
    bigram_prob: dict[tuple[str, str], float],
    scorer,
    n_perms: int = 200,
    seed: int = 0,
) -> tuple[float, float]:
    """Compute mean and std of random-mapping scores (null distribution)."""
    rng = random.Random(seed)
    cipher_alphabet = sorted(set(flat))
    target_tokens = sorted(set(t for pair in bigram_prob for t in pair))
    while len(target_tokens) < len(cipher_alphabet):
        target_tokens.append(f"?{len(target_tokens)}")
    tgt = target_tokens[: len(cipher_alphabet)]
    scores = []
    for _ in range(n_perms):
        rng.shuffle(tgt)
        m = dict(zip(cipher_alphabet, tgt))
        scores.append(scorer.score_full(m))
    mu = sum(scores) / len(scores)
    std = math.sqrt(sum((s - mu) ** 2 for s in scores) / len(scores)) or 1.0
    return mu, std


# ── Main ──────────────────────────────────────────────────────────────────

def main() -> None:
    print("Phase-44 T3: V3 Corpus SA 300K iterations (10 × 30K)\n")

    # Load corpus
    print("Loading Holdat corpus...")
    flat, inscriptions = load_holdat()
    n_signs = len(set(flat))
    n_tokens = len(flat)
    n_inscriptions = len(inscriptions)
    print(f"  {n_inscriptions} inscriptions, {n_tokens} tokens, {n_signs} distinct signs")

    # Load LMs
    print("Loading language models...")
    drav_lp = load_dravidian_lm()
    skt_lp = load_sanskrit_lm()
    print(f"  Dravidian bigrams: {len(drav_lp)}")
    print(f"  Sanskrit bigrams:  {len(skt_lp)}")

    if not drav_lp:
        print("ERROR: Dravidian LM empty — cannot run")
        sys.exit(1)
    if not skt_lp:
        print("WARNING: Sanskrit LM empty — Sanskrit comparison will be skipped")

    # Build GPU-backed scorers (one per LM, reused across all seeds)
    print("\nBuilding GPU scorers...")
    try:
        import cupy as _cp  # noqa: PLC0415
        _cp.cuda.is_available()  # probe
        device_label = "GPU (CuPy)"
    except Exception:
        try:
            import numpy as _np  # noqa: PLC0415,F401
            device_label = "CPU (NumPy)"
        except Exception:
            device_label = "CPU (Python fallback)"
    print(f"  Device: {device_label}")
    drav_scorer = build_scorer(drav_lp, flat)
    skt_scorer = build_scorer(skt_lp, flat) if skt_lp else None
    print(f"  Dravidian scorer: {drav_scorer.n_valid} valid bigram pairs in corpus")

    # Compute null distributions (200 random perms each)
    print("\nComputing null distributions (200 perms each)...")
    t0 = time.time()
    drav_null_mu, drav_null_std = null_score(flat, drav_lp, drav_scorer, n_perms=200)
    skt_null_mu, skt_null_std = (
        null_score(flat, skt_lp, skt_scorer, n_perms=200)
        if skt_scorer else (-9999, 1.0)
    )
    print(f"  Null computed in {time.time()-t0:.1f}s")
    print(f"  Dravidian null: mu={drav_null_mu:.1f}, std={drav_null_std:.1f}")
    if skt_scorer:
        print(f"  Sanskrit null:  mu={skt_null_mu:.1f}, std={skt_null_std:.1f}")

    # Run SA for each seed
    drav_results = []
    skt_results = []

    for seed in RANDOM_SEEDS:
        t0 = time.time()
        print(f"\n  Seed {seed}: Dravidian SA ({N_RESTARTS}×{MAX_ITER:,})...", end=" ", flush=True)
        dr = run_sa(flat, drav_lp, drav_scorer, seed=seed)
        print(f"score={dr['best_score']:.1f} ({time.time()-t0:.1f}s)", flush=True)
        drav_results.append(dr["best_score"])

        if skt_scorer:
            t0 = time.time()
            print(f"  Seed {seed}: Sanskrit  SA ({N_RESTARTS}×{MAX_ITER:,})...", end=" ", flush=True)
            sr = run_sa(flat, skt_lp, skt_scorer, seed=seed)
            print(f"score={sr['best_score']:.1f} ({time.time()-t0:.1f}s)", flush=True)
            skt_results.append(sr["best_score"])

    # Summary statistics
    def stats(scores: list[float]) -> dict:
        if not scores:
            return {}
        n = len(scores)
        mu = sum(scores) / n
        std = math.sqrt(sum((s - mu) ** 2 for s in scores) / n)
        return {"mean": round(mu, 3), "std": round(std, 3),
                "min": round(min(scores), 3), "max": round(max(scores), 3),
                "all": [round(s, 3) for s in scores]}

    drav_stats = stats(drav_results)
    skt_stats = stats(skt_results)

    # Z-score: (best_SA - null_mu) / null_std
    drav_z = (drav_stats["mean"] - drav_null_mu) / drav_null_std if drav_null_std else 0
    skt_z = (skt_stats["mean"] - skt_null_mu) / skt_null_std if skt_null_std and skt_stats else 0

    # Lift = (SA_mean - null_mu) / |null_mu|  — how much the SA improved over random,
    # expressed as a fraction of the null score magnitude.  Higher = better optimisation.
    # (SA scores are negative; SA_mean > null_mu means improvement.)
    drav_lift = (drav_stats["mean"] - drav_null_mu) / abs(drav_null_mu) if drav_null_mu else 0
    skt_lift = ((skt_stats["mean"] - skt_null_mu) / abs(skt_null_mu)
                if skt_null_mu and skt_stats else 0)
    dravidian_wins = drav_lift > skt_lift if skt_lift else True
    ratio = round(drav_lift / skt_lift, 4) if skt_lift else None

    print(f"\n{'='*60}")
    print(f"RESULTS (300K SA iterations, {len(RANDOM_SEEDS)} seeds)")
    print(f"{'='*60}")
    print(f"Dravidian: Z={drav_z:.2f}, lift={drav_lift:.4f}, mean_score={drav_stats['mean']:.1f}")
    if skt_stats:
        print(f"Sanskrit:  Z={skt_z:.2f}, lift={skt_lift:.4f}, mean_score={skt_stats['mean']:.1f}")
    print(f"Dravidian wins: {dravidian_wins}  (ratio {ratio}x)")
    print(f"Convergence std (Dravidian): {drav_stats['std']:.3f}")

    # Verdict
    if dravidian_wins and drav_z > 3.0:
        verdict = "CONFIRMED"
        epistemic = "[VERIFIED, medium confidence]"
    elif dravidian_wins:
        verdict = "SUPPORTED"
        epistemic = "[SUPPORTED, medium confidence]"
    elif not skt_stats:
        verdict = "DRAVIDIAN_ONLY"
        epistemic = "[INCONCLUSIVE, Sanskrit LM unavailable]"
    else:
        verdict = "NOT_CONFIRMED"
        epistemic = "[UNCERTAIN] Sanskrit competitive at 300K"

    result = {
        "_citation": {
            "primary_sources": ["A.1", "A.13", "E.1", "E.2", "E.3"],
            "derivation": (
                f"Phase-44 T3: V3 corpus SA {N_RESTARTS}x{MAX_ITER}=300K iters. "
                "Dravidian Tamil LM (944 bigrams, TamilTB-expanded). "
                "Sanskrit syllable LM (comparison). Holdat LLC corpus."
            ),
        },
        "corpus": {
            "n_inscriptions": n_inscriptions,
            "n_tokens": n_tokens,
            "n_distinct_signs": n_signs,
        },
        "sa_params": {
            "n_restarts": N_RESTARTS,
            "max_iterations_per_restart": MAX_ITER,
            "total_iterations": N_RESTARTS * MAX_ITER,
            "sa_temp_start": SA_TEMP_START,
            "sa_cooling": SA_COOLING,
            "seeds": RANDOM_SEEDS,
        },
        "dravidian": {
            **drav_stats,
            "null_mu": round(drav_null_mu, 3),
            "null_std": round(drav_null_std, 3),
            "z_score": round(drav_z, 3),
            "lift": round(drav_lift, 4),
            "n_bigrams_lm": len(drav_lp),
        },
        "sanskrit": (
            {
                **skt_stats,
                "null_mu": round(skt_null_mu, 3),
                "null_std": round(skt_null_std, 3),
                "z_score": round(skt_z, 3),
                "lift": round(skt_lift, 4),
                "n_bigrams_lm": len(skt_lp),
            }
            if skt_stats else None
        ),
        "comparison": {
            "dravidian_wins": dravidian_wins,
            "lift_ratio": ratio,
            "verdict": verdict,
            "epistemic_status": epistemic,
        },
    }

    OUT_FILE.write_text(json.dumps(result, indent=2, ensure_ascii=False), "utf-8")
    print(f"\nReport: {OUT_FILE}")
    print(f"Verdict: {verdict} — {epistemic}")


if __name__ == "__main__":
    main()
