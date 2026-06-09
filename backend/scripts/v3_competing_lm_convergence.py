"""V3 Preprint — Competing LM SA Convergence Test.

Tests SA convergence behavior on the Indus corpus with three LMs:
  1. Dravidian (TamilTB) — the hypothesis LM
  2. Hebrew (Old Testament consonantal) — a known non-Dravidian LM
  3. Uniform — language-neutral baseline (all bigrams equally likely)

If the Dravidian LM produces meaningfully different convergence (more distinct
modals, higher consistency) than BOTH Hebrew and Uniform, that's evidence of
genuine language-family compatibility, not just SA overfitting to any LM.

Method: For each LM, run SA 5 seeds × 5K iterations on the IVS corpus.
Report: n_distinct_modals, mean_consistency, top-3 modals, degenerate flag.

Output: reports/v3_competing_lm_convergence.json
"""
from __future__ import annotations

import json
import math
import random
import sys
from collections import Counter
from pathlib import Path

_BACKEND = str(Path(__file__).resolve().parent.parent)
if _BACKEND not in sys.path:
    sys.path.insert(0, _BACKEND)


def _load_indus_corpus():
    try:
        from glossa_lab.data.indus_corpus_v2 import load_corpus
        seqs = load_corpus()
        return [s for seq in seqs for s in seq], seqs
    except Exception:
        pass
    try:
        from glossa_lab.data.indus_corpus_firestore import load_corpus
        seqs = load_corpus()
        return [s for seq in seqs for s in seq], seqs
    except Exception:
        pass
    print("ERROR: No Indus corpus loader found")
    sys.exit(1)


def _build_dravidian_lm():
    lm_path = Path(_BACKEND) / "glossa_lab" / "data" / "dravidian_tamil_lm.json"
    lm_data = json.loads(lm_path.read_text(encoding="utf-8"))
    bigrams_raw = lm_data.get("bigrams", {})
    symbols = []
    for key, count in bigrams_raw.items():
        for sep in (",", "|", "_"):
            if sep in key:
                parts = key.split(sep)
                break
        else:
            continue
        if len(parts) == 2:
            for _ in range(max(1, int(count))):
                symbols.extend(parts)
    from glossa_lab.pipelines.decipher import LanguageModel
    return LanguageModel(symbols), "Dravidian (TamilTB)"


def _build_hebrew_lm():
    from glossa_lab.data.old_hebrew import _HEBREW_LINES
    symbols = []
    inscriptions = []
    for line in _HEBREW_LINES:
        word_signs = [s for s in line.split() if s != "."]
        if word_signs:
            symbols.extend(word_signs)
            inscriptions.append(word_signs)
    from glossa_lab.pipelines.decipher import LanguageModel
    return LanguageModel(symbols, inscriptions), "Hebrew (OT consonantal)"


def _build_uniform_lm(alphabet_size=40):
    """Build a uniform LM: all bigrams equally likely over a synthetic alphabet."""
    alphabet = [f"S{i:02d}" for i in range(alphabet_size)]
    # Generate uniform text: random sequences
    rng = random.Random(42)
    symbols = [rng.choice(alphabet) for _ in range(5000)]
    from glossa_lab.pipelines.decipher import LanguageModel
    return LanguageModel(symbols), "Uniform (language-neutral)"


def _run_sa_convergence(corpus_flat, corpus_seqs, lm, lm_name, n_seeds=5, n_iters=5000):
    """Run SA with the given LM and measure convergence behavior."""
    from glossa_lab.pipelines.decipher import decipher

    print(f"\n  Running SA: {lm_name} ({n_seeds} seeds × {n_iters} iters)...")

    all_mappings = []
    for seed in range(n_seeds):
        result = decipher(
            cipher_signs=corpus_flat,
            target_model=lm,
            seed=seed * 7 + 1,
            max_iterations=n_iters,
            restarts=3,
            cipher_inscriptions=corpus_seqs,
        )
        all_mappings.append(result["proposed_mapping"])

    # Compute per-sign modals and consistency
    cipher_signs = sorted(set(corpus_flat))
    sign_stats = {}
    for sign in cipher_signs:
        readings = [m.get(sign, "?") for m in all_mappings]
        freq = Counter(readings)
        modal, modal_count = freq.most_common(1)[0]
        consistency = modal_count / len(readings)
        sign_stats[sign] = {
            "modal": modal,
            "consistency": consistency,
            "n_readings": len(readings),
        }

    # Aggregate
    consistencies = [s["consistency"] for s in sign_stats.values()]
    modals = [s["modal"] for s in sign_stats.values()]
    modal_dist = Counter(modals)
    n_distinct = len(modal_dist)
    mean_cons = sum(consistencies) / len(consistencies) if consistencies else 0

    # Degenerate = >80% of signs map to <=3 phonemes
    top3_count = sum(c for _, c in modal_dist.most_common(3))
    degenerate = top3_count / len(cipher_signs) > 0.80

    result = {
        "lm_name": lm_name,
        "n_seeds": n_seeds,
        "n_iters": n_iters,
        "n_signs": len(cipher_signs),
        "n_distinct_modals": n_distinct,
        "mean_consistency": round(mean_cons, 4),
        "top3_modals": [
            {"phoneme": p, "count": c, "pct": round(c / len(cipher_signs) * 100, 1)}
            for p, c in modal_dist.most_common(3)
        ],
        "degenerate": degenerate,
        "modal_distribution_size": len(modal_dist),
    }

    status = "DEGENERATE" if degenerate else "NON-DEGENERATE"
    print(f"    {lm_name}: {n_distinct} distinct modals, "
          f"mean consistency {mean_cons:.3f}, {status}")
    print(f"    Top-3: {', '.join(f'{p}({c})' for p, c in modal_dist.most_common(3))}")

    return result


def main():
    print("=" * 68)
    print("  Competing LM SA Convergence Test: Dravidian vs Hebrew vs Uniform")
    print("=" * 68)

    flat, seqs = _load_indus_corpus()
    print(f"\n  Corpus: {len(flat)} tokens, {len(seqs)} inscriptions, "
          f"{len(set(flat))} distinct signs")

    results = []

    # 1. Dravidian
    drav_lm, drav_name = _build_dravidian_lm()
    results.append(_run_sa_convergence(flat, seqs, drav_lm, drav_name))

    # 2. Hebrew
    heb_lm, heb_name = _build_hebrew_lm()
    results.append(_run_sa_convergence(flat, seqs, heb_lm, heb_name))

    # 3. Uniform
    uni_lm, uni_name = _build_uniform_lm()
    results.append(_run_sa_convergence(flat, seqs, uni_lm, uni_name))

    # Summary
    print(f"\n{'=' * 68}")
    print(f"  {'LM':<30} {'Modals':>7} {'Cons':>6} {'Status'}")
    print(f"  {'-' * 58}")
    for r in results:
        status = "DEGEN" if r["degenerate"] else "OK"
        print(f"  {r['lm_name']:<30} {r['n_distinct_modals']:>7} "
              f"{r['mean_consistency']:>6.3f} {status}")
    print(f"{'=' * 68}")

    output = {
        "test": "Competing LM SA Convergence",
        "corpus_tokens": len(flat),
        "corpus_signs": len(set(flat)),
        "results": results,
    }

    out_path = Path(_BACKEND).parent / "reports" / "v3_competing_lm_convergence.json"
    out_path.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(f"\nSaved to {out_path}")


if __name__ == "__main__":
    main()
