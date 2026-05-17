"""Phase-46 T5: SA Parameter Sweep — Optimise Dravidian Cipher Alignment.

Phase-44 T3 used: temp=1.0, cooling=0.9997, max_iter=30K, 10 restarts.
Result: Dravidian lift=3.13x, z=12.1 (CONFIRMED, medium confidence).

This sweep tests whether different SA hyperparameters yield significantly
higher lifts or more stable convergence, providing a tighter confidence
interval on the Dravidian advantage.

Grid:
  temp_start:  [0.5, 1.0, 2.0]
  cooling:     [0.9995, 0.9997, 0.9999]
  max_iter:    [15_000, 30_000, 50_000]
  restarts:    3 per config (for speed; Phase-44 T3 used 10)
  = 27 configurations, 3 seeds each = 81 SA runs total

GPU: BigramScorer (CuPy or NumPy) + torch for result tensor operations.

Output: reports/phase46_t5_sa_param_sweep.json
"""
from __future__ import annotations

import csv, json, math, random, sys, time
from collections import Counter
from itertools import product
from pathlib import Path
from types import SimpleNamespace

REPO = Path(__file__).parents[2]
sys.path.insert(0, str(REPO / "backend"))

try:
    import torch
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"[GPU] torch {torch.__version__} — device: {DEVICE}")
except ImportError:
    torch = None
    DEVICE = "cpu"
    print("[GPU] torch not available — CPU only")

HOLDAT_CSV = REPO / "corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv"
DATA       = REPO / "backend/glossa_lab/data"
REPORTS    = REPO / "reports"
REPORTS.mkdir(exist_ok=True)
OUT        = REPORTS / "phase46_t5_sa_param_sweep.json"

# Sweep grid
TEMP_START_VALS = [0.5, 1.0, 2.0]
COOLING_VALS    = [0.9995, 0.9997, 0.9999]
MAX_ITER_VALS   = [15_000, 30_000, 50_000]
N_RESTARTS      = 3     # per config
N_SEEDS         = 3     # seeds per config


def load_corpus() -> tuple[list[str], list[list[str]]]:
    seals: dict[str, list[tuple[int, str]]] = {}
    with open(HOLDAT_CSV, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            sign = (row.get("letters") or "").strip()
            cisi = (row.get("cisi_number") or "").strip()
            pos  = int(row.get("position") or 0)
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


def load_lm() -> dict[tuple[str, str], float]:
    raw = json.loads((DATA / "dravidian_tamil_lm.json").read_text("utf-8"))
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


def run_sa_config(
    flat: list[str],
    scorer,
    bigram_prob: dict,
    temp: float,
    cooling: float,
    max_iter: int,
    seed: int,
    n_restarts: int = N_RESTARTS,
) -> float:
    """Run SA and return best score."""
    rng = random.Random(seed)
    cipher_alpha = sorted(set(flat))
    target_tokens = sorted(set(t for pair in bigram_prob for t in pair))
    while len(target_tokens) < len(cipher_alpha):
        target_tokens.append(f"?{len(target_tokens)}")

    best_score = float("-inf")

    for restart in range(n_restarts):
        tgt = list(target_tokens[:len(cipher_alpha)])
        if restart > 0:
            rng.shuffle(tgt)
        mapping = dict(zip(cipher_alpha, tgt))
        score = scorer.score_full(mapping)
        t = temp

        for _ in range(max_iter):
            i, j = rng.sample(range(len(cipher_alpha)), 2)
            ca, cb = cipher_alpha[i], cipher_alpha[j]
            mapping[ca], mapping[cb] = mapping[cb], mapping[ca]
            new_score = scorer.score_full(mapping)
            delta = new_score - score
            if delta > 0 or (t > 0 and rng.random() < math.exp(min(delta / t, 0))):
                score = new_score
            else:
                mapping[ca], mapping[cb] = mapping[cb], mapping[ca]
            t *= cooling

        if score > best_score:
            best_score = score

    return best_score


def estimate_null(flat: list[str], scorer, bigram_prob: dict, n: int = 50) -> tuple[float, float]:
    cipher_alpha = sorted(set(flat))
    target_tokens = sorted(set(t for pair in bigram_prob for t in pair))
    while len(target_tokens) < len(cipher_alpha):
        target_tokens.append(f"?{len(target_tokens)}")
    rng = random.Random(42)
    scores = []
    for _ in range(n):
        tgt = list(target_tokens[:len(cipher_alpha)])
        rng.shuffle(tgt)
        scores.append(scorer.score_full(dict(zip(cipher_alpha, tgt))))
    mu = sum(scores) / len(scores)
    std = math.sqrt(sum((s - mu)**2 for s in scores) / len(scores)) or 1.0
    return mu, std


def main() -> None:
    print("Phase-46 T5: SA Parameter Sweep\n")

    flat, inscriptions = load_corpus()
    bigram_prob = load_lm()
    scorer = build_scorer(bigram_prob, flat)

    print(f"Corpus: {len(inscriptions)} inscriptions, {len(flat)} signs")
    print(f"LM: {len(bigram_prob)} bigrams")
    print(f"Grid: {len(TEMP_START_VALS)}×{len(COOLING_VALS)}×{len(MAX_ITER_VALS)} = "
          f"{len(TEMP_START_VALS)*len(COOLING_VALS)*len(MAX_ITER_VALS)} configs × {N_SEEDS} seeds")

    # Null baseline
    print("\nEstimating null model…")
    null_mu, null_std = estimate_null(flat, scorer, bigram_prob, n=30)
    print(f"  Null: mean={null_mu:.1f}, std={null_std:.1f}")

    # Reference: Phase-44 T3 baseline
    phase44_lift = 3.1334

    # Run sweep
    sweep_results = []
    n_configs = len(TEMP_START_VALS) * len(COOLING_VALS) * len(MAX_ITER_VALS)
    config_num = 0
    t_total = time.perf_counter()

    for temp, cooling, max_iter in product(TEMP_START_VALS, COOLING_VALS, MAX_ITER_VALS):
        config_num += 1
        t0 = time.perf_counter()

        seed_scores = [
            run_sa_config(flat, scorer, bigram_prob, temp, cooling, max_iter, seed)
            for seed in range(N_SEEDS)
        ]
        elapsed = time.perf_counter() - t0

        mean_score = sum(seed_scores) / len(seed_scores)
        best_score = max(seed_scores)
        z = (mean_score - null_mu) / null_std
        lift = mean_score / null_mu if null_mu else 0

        sweep_results.append({
            "config": f"t{temp}_c{cooling}_i{max_iter}",
            "temp_start": temp,
            "cooling": cooling,
            "max_iter": max_iter,
            "seed_scores": [round(s, 2) for s in seed_scores],
            "mean_score": round(mean_score, 2),
            "best_score": round(best_score, 2),
            "z_score": round(z, 3),
            "lift": round(lift, 4),
            "elapsed_secs": round(elapsed, 1),
        })

        print(f"  [{config_num:2d}/{n_configs}] temp={temp}, cool={cooling}, "
              f"iter={max_iter:,}: lift={lift:.4f}x z={z:.2f} ({elapsed:.1f}s)")

    total_elapsed = time.perf_counter() - t_total

    # Torch tensor operations for analysis
    if torch is not None:
        lifts = torch.tensor([r["lift"] for r in sweep_results], device=DEVICE)
        zs    = torch.tensor([r["z_score"] for r in sweep_results], device=DEVICE)

        best_idx = int(lifts.argmax().item())
        worst_idx = int(lifts.argmin().item())
        mean_lift = float(lifts.mean().item())
        std_lift  = float(lifts.std().item())
        mean_z    = float(zs.mean().item())

        # Correlation: max_iter vs lift
        iters = torch.tensor([r["max_iter"] for r in sweep_results], dtype=torch.float32, device=DEVICE)
        iters_n = (iters - iters.mean()) / iters.std()
        lifts_n = (lifts - lifts.mean()) / lifts.std()
        iter_lift_corr = float((iters_n * lifts_n).mean().item())

        print(f"\n[GPU:{DEVICE}] Tensor analysis complete")
    else:
        lifts_list = [r["lift"] for r in sweep_results]
        best_idx = max(range(len(lifts_list)), key=lambda i: lifts_list[i])
        worst_idx = min(range(len(lifts_list)), key=lambda i: lifts_list[i])
        mean_lift = sum(lifts_list) / len(lifts_list)
        std_lift  = math.sqrt(sum((l - mean_lift)**2 for l in lifts_list) / len(lifts_list))
        mean_z    = sum(r["z_score"] for r in sweep_results) / len(sweep_results)
        iter_lift_corr = 0.0

    best_config = sweep_results[best_idx]
    worst_config = sweep_results[worst_idx]

    print(f"\n=== SA Parameter Sweep Results ===")
    print(f"Total time: {total_elapsed:.1f}s")
    print(f"Best config:  {best_config['config']} — lift={best_config['lift']:.4f}x z={best_config['z_score']:.2f}")
    print(f"Worst config: {worst_config['config']} — lift={worst_config['lift']:.4f}x z={worst_config['z_score']:.2f}")
    print(f"Mean lift: {mean_lift:.4f}x ± {std_lift:.4f}")
    print(f"Mean z-score: {mean_z:.2f}")
    print(f"Phase-44 T3 reference lift: {phase44_lift:.4f}x")
    print(f"Max_iter↔lift correlation: {iter_lift_corr:.3f}")

    # Overall verdict on parameter sensitivity
    lift_range = best_config["lift"] - worst_config["lift"]
    if lift_range < 0.05:
        sensitivity = "LOW_SENSITIVITY"
        note = "Results are stable across the parameter grid — the 3.13x lift is robust."
    elif lift_range < 0.15:
        sensitivity = "MEDIUM_SENSITIVITY"
        note = "Some parameter sensitivity. Optimal config gives marginal improvement over Phase-44 T3."
    else:
        sensitivity = "HIGH_SENSITIVITY"
        note = f"High parameter sensitivity (range={lift_range:.2f}x). Optimal tuning matters."

    # Best vs Phase-44 T3 comparison
    improvement_vs_baseline = (best_config["lift"] - phase44_lift) / phase44_lift

    result = {
        "_citation": {"primary_sources": ["A.1"], "phase44_t3_lift": phase44_lift},
        "gpu_device": DEVICE,
        "corpus": {"n_inscriptions": len(inscriptions), "n_signs_flat": len(flat)},
        "lm": {"n_bigrams": len(bigram_prob)},
        "null_model": {"mean": round(null_mu, 3), "std": round(null_std, 3)},
        "sweep_grid": {
            "temp_start": TEMP_START_VALS,
            "cooling": COOLING_VALS,
            "max_iter": MAX_ITER_VALS,
            "n_restarts": N_RESTARTS,
            "n_seeds": N_SEEDS,
            "n_configs": n_configs,
        },
        "sweep_results": sweep_results,
        "summary": {
            "best_config": best_config["config"],
            "best_lift": best_config["lift"],
            "best_z": best_config["z_score"],
            "worst_config": worst_config["config"],
            "worst_lift": worst_config["lift"],
            "mean_lift": round(mean_lift, 4),
            "std_lift": round(std_lift, 4),
            "mean_z": round(mean_z, 3),
            "lift_range": round(lift_range, 4),
            "iter_lift_correlation": round(iter_lift_corr, 3),
            "sensitivity": sensitivity,
            "improvement_vs_phase44_t3": round(improvement_vs_baseline, 4),
        },
        "total_elapsed_secs": round(total_elapsed, 1),
        "parameter_sensitivity": sensitivity,
        "sensitivity_note": note,
        "improvement_vs_baseline": round(improvement_vs_baseline, 4),
    }

    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), "utf-8")
    print(f"\nReport: {OUT}")


if __name__ == "__main__":
    main()
