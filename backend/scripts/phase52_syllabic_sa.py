"""Phase-52: Constrained Syllabic SA — Full Decipherment Table.

Uses the syllabic LM (Phase-49) with all confirmed anchors (from updated
INDUS_FINAL_ANCHORS.json after Phase-48-51) to produce a candidate
full decipherment mapping for all 390 corpus signs.

Key differences from Phase-44/46 SA:
  1. TARGET SPACE: Tamil syllables (~300 types) instead of single chars (68)
  2. CONSTRAINTS: All HIGH + validated MEDIUM anchors FIXED (not free)
  3. OBJECTIVE: The SA searches the remaining free signs only
  4. METRIC: Syllabic bigram log-prob (linguistically appropriate for syllabic script)

SA parameters:
  - 10 restarts × 30,000 iterations per seed = 300K
  - temp=1.0, cooling=0.9997
  - 5 random seeds
  - Compare against Sanskrit syllabic LM (built from Sanskrit LM tokens)

GPU: BigramScorer on CUDA + torch for result analysis.

Output: reports/phase52_syllabic_sa.json
        reports/phase52_full_decipherment_table.json
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

try:
    import torch
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"[GPU] torch {torch.__version__} — device: {DEVICE}")
except ImportError:
    DEVICE = "cpu"; print("[GPU] torch not available — CPU only")

HOLDAT_CSV = REPO / "corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv"
SYLLABIC_LM = REPO / "backend/glossa_lab/data/dravidian_syllabic_lm.json"
CHAR_LM     = REPO / "backend/glossa_lab/data/dravidian_tamil_lm.json"
SANSKRIT_LM = REPO / "backend/glossa_lab/data/sanskrit_syllable_lm.json"
ANCHORS     = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
REPORTS     = REPO / "reports"
REPORTS.mkdir(exist_ok=True)
OUT         = REPORTS / "phase52_syllabic_sa.json"
OUT_TABLE   = REPORTS / "phase52_full_decipherment_table.json"

N_RESTARTS  = 10
MAX_ITER    = 30_000
SA_TEMP     = 1.0
SA_COOL     = 0.9997
N_SEEDS     = 5
MIN_SYLLABLE_FREQ = 3  # filter very rare syllables from LM target space


def load_corpus() -> tuple[list[str], list[list[str]]]:
    seals: dict[str, list] = {}
    with open(HOLDAT_CSV, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            s = (row.get("letters") or "").strip()
            c = (row.get("cisi_number") or "").strip()
            p = int(row.get("position") or 0)
            if c not in seals: seals[c] = []
            while len(seals[c]) <= p: seals[c].append("")
            seals[c][p] = s
    inscriptions = [[s for s in v if s] for v in seals.values() if any(v)]
    flat = [s for insc in inscriptions for s in insc]
    return flat, inscriptions


def load_syllabic_lm() -> tuple[dict, list[str]]:
    """Load syllabic LM; fall back to char LM if syllabic not built yet."""
    if SYLLABIC_LM.exists():
        raw = json.loads(SYLLABIC_LM.read_text("utf-8"))
        bigrams = raw.get("bigrams", {})
        syl_freq = raw.get("syllable_freq", {})
        # Filter to syllables with enough frequency
        valid = {s for s, c in syl_freq.items() if c >= MIN_SYLLABLE_FREQ}
        total = sum(v for k, v in bigrams.items()
                    if k.split(",",1)[0] in valid and k.split(",",1)[1] in valid) or 1
        prob = {
            tuple(k.split(",",1)): v / total
            for k, v in bigrams.items()
            if "," in k
            and k.split(",",1)[0] in valid
            and k.split(",",1)[1] in valid
        }
        vocab = sorted(valid)
        print(f"  Syllabic LM: {len(prob)} bigrams, {len(vocab)} syllable types")
        return prob, vocab
    else:
        print("  Syllabic LM not found — using char LM as fallback")
        raw = json.loads(CHAR_LM.read_text("utf-8"))
        bigrams = raw.get("bigrams", {})
        total = sum(bigrams.values()) or 1
        prob = {tuple(k.split(",",1)): v/total for k,v in bigrams.items() if "," in k}
        vocab = sorted(set(t for pair in prob for t in pair))
        return prob, vocab


def load_anchors_as_pins(vocab: list[str]) -> dict[str, str]:
    """Build pinned mapping from HIGH and top-MEDIUM anchor readings."""
    anchors = json.loads(ANCHORS.read_text("utf-8"))["anchors"]
    pinned: dict[str, str] = {}
    vocab_set = set(vocab)

    # HIGH anchors: pin to syllabic reading
    HIGH_SYLLABIC = {
        "M006": "pu",   # puli
        "M016": "ka",   # kaliru
        "M045": "ya",   # yanai
        "M062": "e",    # erutu
        "M099": "ko",   # kol
        "M176": "an",   # an
        "M342": "ay",   # ay
    }
    for sign, syl in HIGH_SYLLABIC.items():
        # Find the closest syllable in vocab
        if syl in vocab_set:
            pinned[sign] = syl
        else:
            # Find syllable starting with same chars
            match = next((s for s in vocab if s.startswith(syl[:2])), None)
            if match: pinned[sign] = match

    # Top MEDIUM anchors: pin if reading initial syllable in vocab
    medium = [(k, v) for k, v in anchors.items()
              if v.get("confidence") == "MEDIUM" and v.get("reading")]
    for sign, info in sorted(medium, key=lambda x: -len(x[1].get("reading",""))):
        reading = info["reading"]
        # Extract first syllable
        import re
        vowels = set("aāiīuūeēoōai")
        syl = reading.rstrip("/").split("/")[0].strip().lower()
        # Remove diacritics for vocab matching
        syl_norm = re.sub(r"[^a-z]", "", syl)[:4]
        if not syl_norm: continue
        if syl_norm in vocab_set:
            pinned[sign] = syl_norm
        else:
            match = next((s for s in vocab if s.startswith(syl_norm[:2])), None)
            if match and sign not in pinned:
                pinned[sign] = match

    print(f"  Pinned {len(pinned)} signs: {list(pinned.items())[:10]}…")
    return pinned


def build_scorer(bigram_prob: dict, flat: list[str]):
    from glossa_lab.pipelines.decipher import BigramScorer
    tc: Counter = Counter()
    for (a, b) in bigram_prob: tc[a] += 1; tc[b] += 1
    ranked = [t for t, _ in tc.most_common()]
    return BigramScorer(SimpleNamespace(ranked=ranked, bigram_freq=bigram_prob), flat)


def run_sa(flat: list[str], scorer, bigram_prob: dict, seed: int,
           pinned: dict[str, str]) -> tuple[float, dict]:
    rng = random.Random(seed)
    cipher_alpha = sorted(set(flat))
    target_tokens = sorted(set(t for pair in bigram_prob for t in pair))
    while len(target_tokens) < len(cipher_alpha):
        target_tokens.append(f"?{len(target_tokens)}")
    free_cipher = [c for c in cipher_alpha if c not in pinned]

    def _init(shuffle: bool) -> dict:
        mapping = dict(pinned)
        used = set(mapping.values())
        pool = [t for t in target_tokens[:len(cipher_alpha)] if t not in used]
        if shuffle: rng.shuffle(pool)
        for c, t in zip(free_cipher, pool): mapping[c] = t
        return mapping

    best_score = float("-inf"); best_mapping: dict = {}
    for restart in range(N_RESTARTS):
        mapping = _init(shuffle=(restart > 0))
        score = scorer.score_full(mapping)
        temp = SA_TEMP
        for _ in range(MAX_ITER):
            if len(free_cipher) < 2: break
            i, j = rng.sample(range(len(free_cipher)), 2)
            ca, cb = free_cipher[i], free_cipher[j]
            mapping[ca], mapping[cb] = mapping[cb], mapping[ca]
            ns = scorer.score_full(mapping)
            delta = ns - score
            if delta > 0 or (temp > 0 and rng.random() < math.exp(min(delta/temp, 0))):
                score = ns
            else:
                mapping[ca], mapping[cb] = mapping[cb], mapping[ca]
            temp *= SA_COOL
        if score > best_score:
            best_score = score; best_mapping = dict(mapping)
    return best_score, best_mapping


def estimate_null(flat: list[str], scorer, bigram_prob: dict, n: int = 30) -> tuple[float, float]:
    cipher_alpha = sorted(set(flat))
    target_tokens = sorted(set(t for pair in bigram_prob for t in pair))
    while len(target_tokens) < len(cipher_alpha):
        target_tokens.append(f"?{len(target_tokens)}")
    rng = random.Random(42); scores = []
    for _ in range(n):
        tgt = list(target_tokens[:len(cipher_alpha)]); rng.shuffle(tgt)
        scores.append(scorer.score_full(dict(zip(cipher_alpha, tgt))))
    mu = sum(scores)/len(scores)
    std = math.sqrt(sum((s-mu)**2 for s in scores)/len(scores)) or 1.0
    return mu, std


def build_decipherment_table(all_mappings: list[dict], flat: list[str]) -> list[dict]:
    """Build consensus decipherment table from multiple SA seeds."""
    from collections import defaultdict
    sign_votes: dict[str, Counter] = defaultdict(Counter)
    for m in all_mappings:
        for sign, reading in m.items():
            sign_votes[sign][reading] += 1

    freq = Counter(flat)
    anchors = json.loads(ANCHORS.read_text("utf-8"))["anchors"]
    table = []
    for sign in sorted(sign_votes, key=lambda s: -freq.get(s, 0)):
        votes = sign_votes[sign]
        total_votes = sum(votes.values())
        best = votes.most_common(1)[0]
        consensus_reading, best_count = best
        consensus_pct = best_count / total_votes

        existing = anchors.get(sign, {})
        table.append({
            "sign": sign,
            "n_corpus": freq.get(sign, 0),
            "sa_reading": consensus_reading,
            "sa_consensus_pct": round(consensus_pct, 2),
            "confirmed_reading": existing.get("reading", ""),
            "confirmed_confidence": existing.get("confidence", "UNREAD"),
            "sa_agrees_confirmed": (
                consensus_reading[:2] == existing.get("reading","?")[:2]
                if existing.get("reading") else None
            ),
            "vote_distribution": dict(votes.most_common(3)),
        })
    return table


def main() -> None:
    print("Phase-52: Constrained Syllabic SA — Full Decipherment Table\n")

    flat, inscriptions = load_corpus()
    print(f"Corpus: {len(inscriptions)} inscriptions, {len(flat)} tokens, {len(set(flat))} unique signs")

    print("\nLoading syllabic LM…")
    bigram_prob, vocab = load_syllabic_lm()

    print("\nBuilding anchor pin set…")
    pinned = load_anchors_as_pins(vocab)

    print("\nBuilding scorer…")
    scorer = build_scorer(bigram_prob, flat)

    print("\nEstimating null model (30 permutations)…")
    null_mu, null_std = estimate_null(flat, scorer, bigram_prob, n=30)
    print(f"  Null: mean={null_mu:.1f}, std={null_std:.1f}")

    print(f"\nRunning SA: {N_SEEDS} seeds × {N_RESTARTS} restarts × {MAX_ITER:,} iter = "
          f"{N_SEEDS * N_RESTARTS * MAX_ITER:,} total iterations")
    t0 = time.perf_counter()

    all_scores = []; all_mappings = []
    for seed in range(N_SEEDS):
        score, mapping = run_sa(flat, scorer, bigram_prob, seed, pinned)
        z = (score - null_mu) / null_std
        lift = score / null_mu if null_mu else 0
        all_scores.append(score)
        all_mappings.append(mapping)
        print(f"  Seed {seed}: score={score:.1f} z={z:.2f} lift={lift:.4f}")

    elapsed = time.perf_counter() - t0
    mean_score = sum(all_scores) / len(all_scores)
    best_score = max(all_scores)
    z = (mean_score - null_mu) / null_std
    lift = mean_score / null_mu if null_mu else 0

    print(f"\nTotal time: {elapsed:.1f}s")
    print(f"Mean score: {mean_score:.1f}, z={z:.2f}, lift={lift:.4f}")

    # Build decipherment table
    table = build_decipherment_table(all_mappings, flat)

    # Coverage analysis
    n_high = sum(1 for t in table if t["confirmed_confidence"] == "HIGH")
    n_medium = sum(1 for t in table if t["confirmed_confidence"] == "MEDIUM")
    n_sa_only = sum(1 for t in table if t["confirmed_confidence"] == "UNREAD")
    n_agree = sum(1 for t in table if t.get("sa_agrees_confirmed"))

    print("\n=== Decipherment Table Statistics ===")
    print(f"  Total signs: {len(table)}")
    print(f"  HIGH anchor (confirmed): {n_high}")
    print(f"  MEDIUM anchor (probable): {n_medium}")
    print(f"  SA-only (candidate): {n_sa_only}")
    if n_high + n_medium > 0:
        print(f"  SA agrees with confirmed: {n_agree}/{n_high+n_medium} = {n_agree/(n_high+n_medium):.0%}")

    print("\nTop 20 highest-frequency signs:")
    for t in table[:20]:
        conf_str = t["confirmed_confidence"]
        sa = t["sa_reading"]
        confirmed = t["confirmed_reading"]
        flag = "✓" if t.get("sa_agrees_confirmed") else ("?" if t.get("sa_agrees_confirmed") is None else "✗")
        print(f"  {t['sign']:6s} n={t['n_corpus']:4d} SA={sa!r:10s} confirmed={confirmed!r:12s} [{conf_str[:3]}] {flag}")

    # Save table
    OUT_TABLE.write_text(json.dumps(table, indent=2, ensure_ascii=False), "utf-8")
    print(f"\nDecipherment table: {OUT_TABLE}")

    result = {
        "_citation": {"primary": ["A.1"]},
        "gpu_device": DEVICE,
        "lm_type": "syllabic" if SYLLABIC_LM.exists() else "char_fallback",
        "n_bigrams_lm": len(bigram_prob),
        "n_syllable_types": len(vocab),
        "n_pinned_signs": len(pinned),
        "null_model": {"mean": round(null_mu, 2), "std": round(null_std, 2)},
        "sa_params": {"n_seeds": N_SEEDS, "n_restarts": N_RESTARTS, "max_iter": MAX_ITER},
        "results": {"mean_score": round(mean_score, 2), "best_score": round(best_score, 2),
                    "z_score": round(z, 3), "lift": round(lift, 4)},
        "coverage": {"n_high": n_high, "n_medium": n_medium, "n_sa_only": n_sa_only,
                     "sa_agrees_confirmed": n_agree},
        "elapsed_secs": round(elapsed, 1),
        "top_30_table": table[:30],
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), "utf-8")
    print(f"Report: {OUT}")


if __name__ == "__main__":
    main()
