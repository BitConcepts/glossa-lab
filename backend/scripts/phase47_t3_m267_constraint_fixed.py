"""Phase-47 T3: M267 Constraint SA — Fixed Token Matching.

Phase-46 T2 had a token-matching bug: candidates 'in', 'um', 'col', 'al',
'atu', 'ir' are multi-character strings but the 944-LM vocabulary is SINGLE
characters (a-z, Tamil Unicode chars). Only 'e' matched correctly (+15.9%).

This script fixes the bug by:
  1. Printing the full LM vocabulary (68 single chars) before running
  2. Mapping each candidate reading to the correct single LM character:
       iṉ (genitive)  → 'i'   (vowel i, initial of iṉ)
       um (connective) → 'u'   (vowel u, initial of um)
       ē (emphatic)   → 'e'   (already worked: ASCII e)
       Tamil ē        → 'எ'   (Tamil vowel ē, DEDR emphatic)
       Tamil i        → 'இ'   (Tamil vowel i, genitive)
       Tamil u        → 'உ'   (Tamil vowel u, connective um)
       col (to say)   → 'c'   (initial of col)
       an (suffix)    → 'a'   (initial of an/aṇ — BUT conflicts with M176)
  3. Runs SA for each single-char pin and compares Dravidian lift.
  4. Also tests pinning M267 to Tamil Unicode chars directly.

BASELINE from Phase-46 T2: lift=0.7302 (z=3.68) — no constraint.
Best from Phase-46 T2: 'e' → lift=0.8466 (+15.9%) — but sign was 'e' as char.

This run uses 5 seeds × 20K iterations (same as T2) for direct comparison.

GPU: BigramScorer (CuPy/NumPy) + torch CUDA.

Output: reports/phase47_t3_m267_constraint_fixed.json
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
OUT        = REPORTS / "phase47_t3_m267_constraint_fixed.json"

# SA params (same as Phase-46 T2 for direct comparison)
N_RESTARTS = 5
MAX_ITER   = 20_000
SA_TEMP    = 1.0
SA_COOL    = 0.9997
N_SEEDS    = 5

# Correct single-char LM token mappings for each M267 candidate
# The LM has 68 tokens: ASCII a-z (minus some) + Tamil Unicode chars
M267_FIXED_CANDIDATES = {
    "BASELINE": None,        # no constraint (Phase-46 T2 baseline: lift=0.7302)
    # ASCII single-char mappings
    "e_emphatic": "e",       # emphatic ē (already tested, +15.9%, works)
    "i_genitive": "i",       # initial i- of genitive iṉ
    "u_connective": "u",     # initial u- of connective um
    "c_col": "c",            # initial c- of col (to say/call)
    "k_kol": "k",            # initial k- of kol — but M099 already assigned k
    "a_suffix": "a",         # initial a- of aṇ/ay — but M176/M342 already use a
    # Tamil Unicode mappings (check if in LM vocabulary)
    "tamil_e": "எ",          # Tamil ē (emphatic vowel)
    "tamil_i": "இ",          # Tamil i (genitive vowel)
    "tamil_u": "உ",          # Tamil u (connective vowel)
}

# Phase-46 T2 reference (baseline with no constraint)
PHASE46_T2_BASELINE_LIFT = 0.7302
PHASE46_T2_BEST_LIFT     = 0.8466  # 'e' gave this
PHASE46_T2_NULL_MU       = -72152.3


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


def load_lm() -> tuple[dict, list[str]]:
    raw = json.loads((DATA / "dravidian_tamil_lm.json").read_text("utf-8"))
    bigrams = raw.get("bigrams", {})
    total = sum(bigrams.values()) or 1
    prob = {
        tuple(k.split(",", 1)): v / total
        for k, v in bigrams.items() if "," in k
    }
    vocab = sorted(set(t for pair in prob for t in pair))
    return prob, vocab


def build_scorer(bigram_prob: dict, flat: list[str]):
    from glossa_lab.pipelines.decipher import BigramScorer
    tc: Counter = Counter()
    for (a, b) in bigram_prob:
        tc[a] += 1; tc[b] += 1
    ranked = [t for t, _ in tc.most_common()]
    mock_lm = SimpleNamespace(ranked=ranked, bigram_freq=bigram_prob)
    return BigramScorer(mock_lm, flat)


def run_sa(flat: list[str], scorer, bigram_prob: dict, seed: int,
           pinned: dict[str, str] | None = None) -> float:
    rng = random.Random(seed)
    cipher_alpha = sorted(set(flat))
    target_tokens = sorted(set(t for pair in bigram_prob for t in pair))
    while len(target_tokens) < len(cipher_alpha):
        target_tokens.append(f"?{len(target_tokens)}")

    pinned = pinned or {}
    free_cipher = [c for c in cipher_alpha if c not in pinned]

    def _init(shuffle: bool) -> dict[str, str]:
        mapping: dict[str, str] = dict(pinned)
        used = set(mapping.values())
        pool = [t for t in target_tokens[:len(cipher_alpha)] if t not in used]
        if shuffle:
            rng.shuffle(pool)
        for c, t in zip(free_cipher, pool):
            mapping[c] = t
        return mapping

    best_score = float("-inf")
    for restart in range(N_RESTARTS):
        mapping = _init(shuffle=(restart > 0))
        score = scorer.score_full(mapping)
        temp = SA_TEMP
        for _ in range(MAX_ITER):
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
    return best_score


def estimate_null(flat: list[str], scorer, bigram_prob: dict, n: int = 30) -> tuple[float, float]:
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
    print("Phase-47 T3: M267 Constraint SA — Fixed Token Matching\n")

    flat, inscriptions = load_corpus()
    bigram_prob, vocab = load_lm()

    print(f"LM vocabulary ({len(vocab)} tokens):")
    print(f"  {vocab}")
    print(f"\nCorpus: {len(inscriptions)} inscriptions, {len(flat)} signs, {len(set(flat))} unique")
    print(f"M267 in corpus: {'M267' in set(flat)}")

    # Check which candidates are in the LM vocabulary
    print("\nCandidate→LM token resolution:")
    resolved: dict[str, str | None] = {}
    for cond, token in M267_FIXED_CANDIDATES.items():
        if token is None:
            resolved[cond] = None
            print(f"  {cond}: BASELINE (no constraint)")
        elif token in vocab:
            resolved[cond] = token
            print(f"  {cond}: '{token}' ✓ IN vocabulary")
        else:
            resolved[cond] = None
            print(f"  {cond}: '{token}' ✗ NOT in vocabulary — SKIP")

    scorer = build_scorer(bigram_prob, flat)

    # Null estimate
    print("\nEstimating null model (30 permutations)…")
    null_mu, null_std = estimate_null(flat, scorer, bigram_prob, n=30)
    print(f"  Null: mean={null_mu:.1f}, std={null_std:.1f}")

    # Run SA for each valid condition
    results: dict[str, dict] = {}
    for cond, token in resolved.items():
        if token is not None and cond != "BASELINE":
            # Only run valid (in-vocab) constraints
            pinned = {"M267": token} if "M267" in set(flat) else None
        elif cond == "BASELINE":
            pinned = None
        else:
            continue  # skip out-of-vocab

        tok_str = repr(token) if token else 'free'
        print(f"\n[{cond}] M267→{tok_str}")
        t0 = time.perf_counter()
        seed_scores = [run_sa(flat, scorer, bigram_prob, s, pinned) for s in range(N_SEEDS)]
        elapsed = time.perf_counter() - t0
        mean_s = sum(seed_scores) / len(seed_scores)
        z = (mean_s - null_mu) / null_std
        lift = mean_s / null_mu if null_mu else 0
        print(f"  Mean={mean_s:.1f}, z={z:.2f}, lift={lift:.4f}x ({elapsed:.1f}s)")
        results[cond] = {
            "token": token, "seed_scores": [round(s, 2) for s in seed_scores],
            "mean_score": round(mean_s, 2), "z_score": round(z, 3),
            "lift": round(lift, 4), "elapsed_secs": round(elapsed, 1),
        }

    # Find best
    valid = {c: r for c, r in results.items() if c != "BASELINE"}
    if valid:
        best_cond = max(valid, key=lambda c: valid[c]["lift"])
        best_lift = valid[best_cond]["lift"]
        baseline_lift = results.get("BASELINE", {}).get("lift", PHASE46_T2_BASELINE_LIFT)
        improvement = (best_lift - baseline_lift) / abs(baseline_lift) if baseline_lift else 0

        print(f"\n=== Fixed M267 Constraint Results ===")
        print(f"Baseline lift: {baseline_lift:.4f}x")
        print(f"Best: {best_cond} (token={valid[best_cond]['token']!r}) → {best_lift:.4f}x (+{improvement:.1%})")
        print(f"Phase-46 T2 reference best ('e'): {PHASE46_T2_BEST_LIFT:.4f}x")

        if best_cond != "BASELINE" and improvement > 0.01:
            verdict = "CONSTRAINT_IMPROVES_FIT"
            note = (f"Token '{valid[best_cond]['token']}' as M267 improves lift "
                    f"by {improvement:.1%}. This is the best single-char candidate.")
        elif improvement < -0.01:
            verdict = "CONSTRAINT_DEGRADES_FIT"
            note = "No valid single-char token improves SA fit when pinned to M267."
        else:
            verdict = "CONSTRAINT_NEUTRAL"
            note = "Pinning M267 to any single LM char gives ~baseline performance."

        print(f"Verdict: {verdict}")
    else:
        verdict = "NO_VALID_CANDIDATES"
        note = "No candidates resolved to in-vocabulary LM tokens."
        best_cond = "BASELINE"
        best_lift = PHASE46_T2_BASELINE_LIFT
        improvement = 0.0
        baseline_lift = PHASE46_T2_BASELINE_LIFT

    result = {
        "_citation": {"primary": ["A.1"], "phase46_t2_reference": PHASE46_T2_BEST_LIFT},
        "gpu_device": DEVICE,
        "lm_vocabulary": vocab,
        "n_lm_tokens": len(vocab),
        "m267_in_corpus": "M267" in set(flat),
        "null_model": {"mean": round(null_mu, 2), "std": round(null_std, 2)},
        "conditions": results,
        "best_condition": best_cond,
        "best_token": results.get(best_cond, {}).get("token"),
        "best_lift": results.get(best_cond, {}).get("lift", best_lift),
        "baseline_lift": results.get("BASELINE", {}).get("lift", PHASE46_T2_BASELINE_LIFT),
        "improvement": round(improvement, 4),
        "phase46_t2_best": PHASE46_T2_BEST_LIFT,
        "verdict": verdict,
        "verdict_note": note,
        "fix_explanation": (
            "Phase-46 T2 bug: multi-char candidates ('in','um','col','al','atu','ir') "
            "did not exist in the 944-LM single-char vocabulary. "
            "This script uses correct single-char mappings: "
            "'e'=emphatic ē, 'i'=genitive iṉ-initial, 'u'=connective um-initial, "
            "'c'=col-initial, Tamil 'எ','இ','உ' if in vocabulary."
        ),
    }

    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), "utf-8")
    print(f"\nReport: {OUT}")


if __name__ == "__main__":
    main()
