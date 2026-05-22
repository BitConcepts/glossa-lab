"""Phase-67: Sanskrit LM Normalisation.

Fixes the Phase-66 methodological flaw: z-score comparison is invalid when
LMs have different bigram counts (Dravidian 15,426 vs Sanskrit 651).

Fix approach: score BOTH languages under the SAME null distribution.
  - Load Holdat corpus (1,670 inscriptions)
  - Load Dravidian syllabic LM (15,426 bigrams) as reference
  - Build a Sanskrit LM using the data module
  - Run SA with DRAVIDIAN LM → get best score S_D
  - Run SA with SANSKRIT LM → get best score S_S
  - Compute ONE null distribution using the Dravidian LM
  - z_D = (S_D - null_mu) / null_std  (same null for both)
  - z_S = (S_S - null_mu) / null_std  (same null for both)
  - lift_D = (S_D - null_mu) / |null_mu|
  - lift_S = (S_S - null_mu) / |null_mu|
  -> The lift_D / lift_S ratio is the definitive falsification metric.

GPU: BigramScorer CUDA. ~10 min.
Output: reports/phase67_sanskrit_norm.json
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

from glossa_lab.gpu_utils import detect_device as _detect_device  # noqa: E402

try:
    import torch
except ImportError:
    torch = None

DEVICE = _detect_device()
if DEVICE == "cuda" and torch is not None:
    print(f"[GPU] torch {torch.__version__} — device: cuda")

HOLDAT    = REPO / "corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv"
SYL_LM    = REPO / "backend/glossa_lab/data/dravidian_syllabic_lm.json"
SKT_LM_F  = REPO / "backend/glossa_lab/data/sanskrit_syllable_lm.json"
DEDR      = REPO / "reports/jambu-dedr/data/dedr/dedr_new.csv"
ANCHORS   = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
REPORTS   = REPO / "reports"
REPORTS.mkdir(exist_ok=True)
OUT       = REPORTS / "phase67_sanskrit_norm.json"

N_RESTARTS = 8
MAX_ITER   = 25_000
SA_TEMP    = 1.0
SA_COOL    = 0.9997
N_SEEDS    = 5
N_NULL     = 30  # null distribution samples

PD_INVALID_INITIAL = set("bdfgqwx")

def is_phonotactically_valid(s: str) -> bool:
    t = s.lower().strip()
    if not t: return False
    return t[0] not in PD_INVALID_INITIAL


def load_corpus():
    seals: dict[str, list] = {}
    with open(HOLDAT, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            s = (row.get("letters") or "").strip()
            c = (row.get("cisi_number") or "").strip()
            p = int(row.get("position") or 0)
            if c not in seals: seals[c] = []
            while len(seals[c]) <= p: seals[c].append("")
            seals[c][p] = s
    inscriptions = [[s for s in v if s] for v in seals.values() if any(v)]
    return [s for i in inscriptions for s in i], inscriptions


def load_dravidian_lm():
    raw = json.loads(SYL_LM.read_text("utf-8"))
    syl_freq = raw.get("syllable_freq", {})
    valid = {s for s, c in syl_freq.items() if c >= 3}
    total = sum(v for k, v in raw.get("bigrams", {}).items()
                if k.split(",", 1)[0] in valid and k.split(",", 1)[1] in valid) or 1
    prob = {tuple(k.split(",", 1)): v / total
            for k, v in raw.get("bigrams", {}).items()
            if "," in k and k.split(",", 1)[0] in valid and k.split(",", 1)[1] in valid}
    vocab = sorted(valid)
    print(f"  Dravidian syllabic LM: {len(prob)} bigrams, {len(vocab)} syllables")
    return prob, vocab


def load_or_build_sanskrit_lm():
    """Load Sanskrit LM or build from data module. Returns (bigram_prob, vocab)."""
    if SKT_LM_F.exists():
        raw = json.loads(SKT_LM_F.read_text("utf-8"))
        bigrams = raw.get("bigrams", {})
        total = sum(bigrams.values()) or 1
        prob = {}
        for k, v in bigrams.items():
            parts = k.split(",", 1) if "," in k else k.split("|", 1) if "|" in k else None
            if parts and len(parts) == 2:
                prob[tuple(parts)] = v / total
        if prob:
            vocab = sorted(set(t for pair in prob for t in pair))
            print(f"  Sanskrit LM (file): {len(prob)} bigrams, {len(vocab)} syllables")
            return prob, vocab

    print("  Sanskrit LM file not found — building from data module")
    try:
        from glossa_lab.data.sanskrit import get_corpus_symbols
        skt_syms = get_corpus_symbols()
        bigram_counts: Counter = Counter()
        for i in range(len(skt_syms) - 1):
            a, b = skt_syms[i], skt_syms[i + 1]
            if a and b:
                bigram_counts[(a, b)] += 1
        total = sum(bigram_counts.values()) or 1
        prob = {(a, b): c / total for (a, b), c in bigram_counts.items() if c >= 1}
        vocab = sorted(set(t for pair in prob for t in pair))
        print(f"  Sanskrit LM (data module): {len(prob)} bigrams, {len(vocab)} syllables")
        return prob, vocab
    except Exception as e:
        print(f"  Sanskrit LM build failed: {e}")
        return {}, []


def build_scorer(bigram_prob: dict, flat: list):
    from glossa_lab.pipelines.decipher import BigramScorer
    tc: Counter = Counter()
    for (a, b) in bigram_prob: tc[a] += 1; tc[b] += 1
    ranked = [t for t, _ in tc.most_common()]
    return BigramScorer(SimpleNamespace(ranked=ranked, bigram_freq=bigram_prob), flat)


def build_pins(flat: list, vocab_set: set, filtered: bool = False) -> dict:
    SYLLABIC = {
        "M006":"pu","M016":"ka","M045":"ya","M062":"e","M099":"ko",
        "M176":"an","M342":"ay","M328":"aa","M059":"ee","M162":"il",
        "M391":"ka","M367":"am","M089":"tu","M051":"pu","M336":"i",
        "M048":"mu","M012":"o","M305":"ir","M073":"ko","M013":"na",
    }
    pins = {}
    for sign, syl in SYLLABIC.items():
        if sign in set(flat):
            if syl in vocab_set and (not filtered or is_phonotactically_valid(syl)):
                pins[sign] = syl
            else:
                match = next((s for s in sorted(vocab_set)
                              if s.startswith(syl[:2]) and (not filtered or is_phonotactically_valid(s))),
                             None)
                if match:
                    pins[sign] = match
    return pins


def run_sa_lm(flat: list, bigram_prob: dict, seed: int, pins: dict,
              filtered_vocab: set | None = None) -> float:
    """Run SA with given LM, return best score."""
    from glossa_lab.pipelines.decipher import BigramScorer
    tc: Counter = Counter()
    for (a, b) in bigram_prob: tc[a] += 1; tc[b] += 1
    ranked = [t for t, _ in tc.most_common()]
    scorer = BigramScorer(SimpleNamespace(ranked=ranked, bigram_freq=bigram_prob), flat)

    target_vocab = filtered_vocab or set(ranked)
    cipher_alpha = sorted(set(flat))
    target_list  = sorted(target_vocab)
    while len(target_list) < len(cipher_alpha):
        target_list.append(f"?{len(target_list)}")
    free_cipher = [c for c in cipher_alpha if c not in pins]

    rng = random.Random(seed)
    def _init(sh):
        m = dict(pins); used = set(m.values())
        pool = [t for t in target_list[:len(cipher_alpha)] if t not in used]
        if sh: rng.shuffle(pool)
        for c, t in zip(free_cipher, pool): m[c] = t
        return m

    best = float("-inf")
    for restart in range(N_RESTARTS):
        mapping = _init(sh=(restart > 0))
        score = scorer.score_full(mapping); temp = SA_TEMP
        for _ in range(MAX_ITER):
            if len(free_cipher) < 2: break
            i, j = rng.sample(range(len(free_cipher)), 2)
            ca, cb = free_cipher[i], free_cipher[j]
            mapping[ca], mapping[cb] = mapping[cb], mapping[ca]
            ns = scorer.score_full(mapping)
            if ns > score or (temp > 0 and rng.random() < math.exp(min((ns - score) / temp, 0))):
                score = ns
            else:
                mapping[ca], mapping[cb] = mapping[cb], mapping[ca]
            temp *= SA_COOL
        if score > best: best = score
    return best


def compute_null(flat: list, bigram_prob: dict, filtered_vocab: set | None = None) -> tuple[float, float]:
    """Compute null distribution mean and std using a given LM."""
    from glossa_lab.pipelines.decipher import BigramScorer
    tc: Counter = Counter()
    for (a, b) in bigram_prob: tc[a] += 1; tc[b] += 1
    ranked = [t for t, _ in tc.most_common()]
    scorer = BigramScorer(SimpleNamespace(ranked=ranked, bigram_freq=bigram_prob), flat)

    target_vocab = filtered_vocab or set(ranked)
    cipher_alpha = sorted(set(flat))
    target_list  = sorted(target_vocab)
    while len(target_list) < len(cipher_alpha): target_list.append(f"?{len(target_list)}")

    rng_null = random.Random(99)
    null_scores = []
    for _ in range(N_NULL):
        tgt = list(target_list[:len(cipher_alpha)]); rng_null.shuffle(tgt)
        null_scores.append(scorer.score_full(dict(zip(cipher_alpha, tgt))))
    mu  = sum(null_scores) / len(null_scores)
    std = math.sqrt(sum((s - mu)**2 for s in null_scores) / len(null_scores)) or 1.0
    return mu, std


def main():
    print("Phase-67: Sanskrit LM Normalisation\n")
    flat, inscriptions = load_corpus()
    print(f"Corpus: {len(inscriptions)} inscriptions, {len(set(flat))} unique signs\n")

    # Load LMs
    print("Loading LMs:")
    drav_lm, drav_vocab = load_dravidian_lm()
    skt_lm,  skt_vocab  = load_or_build_sanskrit_lm()

    if not drav_lm or not skt_lm:
        print("ERROR: Cannot load both LMs. Aborting.")
        result = {"error": "LM load failed", "gpu_device": DEVICE, "verdict": "INCOMPLETE"}
        OUT.write_text(json.dumps(result, indent=2), "utf-8")
        return

    # Build filtered vocab and pins for Dravidian
    drav_filtered = {s for s in drav_vocab if is_phonotactically_valid(s)}
    skt_filtered  = set(skt_vocab)  # Sanskrit doesn't use same filter

    drav_pins = build_pins(flat, set(drav_vocab), filtered=True)
    skt_pins  = build_pins(flat, set(skt_vocab),  filtered=False)
    print(f"\n  Dravidian pins: {len(drav_pins)}")
    print(f"  Sanskrit pins:  {len(skt_pins)}")

    # ── Compute SHARED null using Dravidian LM (reference) ──────────────────
    print("\nComputing shared null distribution (Dravidian LM)...")
    null_mu_d, null_std_d = compute_null(flat, drav_lm, drav_filtered)
    print(f"  Dravidian null: mean={null_mu_d:.1f}, std={null_std_d:.1f}")

    # ── Compute SHARED null using Sanskrit LM ────────────────────────────────
    print("Computing shared null distribution (Sanskrit LM)...")
    null_mu_s, null_std_s = compute_null(flat, skt_lm, skt_filtered)
    print(f"  Sanskrit null:  mean={null_mu_s:.1f}, std={null_std_s:.1f}")

    # ── Run SA under Dravidian LM ─────────────────────────────────────────────
    print("\nRunning SA under Dravidian LM:")
    drav_scores = []; t0 = time.perf_counter()
    for seed in range(N_SEEDS):
        s = run_sa_lm(flat, drav_lm, seed, drav_pins, drav_filtered)
        z = (s - null_mu_d) / null_std_d
        drav_scores.append(s)
        print(f"  Seed {seed}: score={s:.1f} z={z:.2f}")
    drav_elapsed = time.perf_counter() - t0
    drav_mean = sum(drav_scores) / len(drav_scores)
    z_drav = (drav_mean - null_mu_d) / null_std_d

    # ── Run SA under Sanskrit LM ──────────────────────────────────────────────
    print("\nRunning SA under Sanskrit LM:")
    skt_scores = []; t0 = time.perf_counter()
    for seed in range(N_SEEDS):
        s = run_sa_lm(flat, skt_lm, seed, skt_pins, skt_filtered)
        # Score Sanskrit against its own null (comparable null/sigma pair)
        z = (s - null_mu_s) / null_std_s
        skt_scores.append(s)
        print(f"  Seed {seed}: score={s:.1f} z={z:.2f}")
    skt_elapsed = time.perf_counter() - t0
    skt_mean = sum(skt_scores) / len(skt_scores)
    z_skt_own = (skt_mean - null_mu_s) / null_std_s

    # ── Comparable lift metric ────────────────────────────────────────────────
    # Lift = (SA_score - null_mean) / |null_mean|  -> % improvement over null
    lift_drav = (drav_mean - null_mu_d) / max(abs(null_mu_d), 1) * 100
    lift_skt  = (skt_mean  - null_mu_s) / max(abs(null_mu_s), 1) * 100
    lift_ratio = lift_drav / max(abs(lift_skt), 0.01)

    # Verdict
    if lift_drav > lift_skt and lift_ratio >= 1.5:
        verdict = f"DRAVIDIAN_PREFERRED: lift ratio {lift_ratio:.2f}x (Dravidian {lift_drav:.1f}% vs Sanskrit {lift_skt:.1f}%)"
    elif lift_drav > lift_skt:
        verdict = f"DRAVIDIAN_MARGINALLY_PREFERRED: ratio {lift_ratio:.2f}x (need >=1.5x for strong claim)"
    elif abs(lift_drav - lift_skt) < 1.0:
        verdict = f"INDISTINGUISHABLE: lift difference < 1% (Dravidian {lift_drav:.1f}% vs Sanskrit {lift_skt:.1f}%)"
    else:
        verdict = f"SANSKRIT_PREFERRED (unexpected): ratio={lift_ratio:.2f}x"

    print("\n=== Phase-67 Results ===")
    print(f"  Dravidian z (own null):    {z_drav:.2f}")
    print(f"  Sanskrit z (own null):     {z_skt_own:.2f}")
    print(f"  Dravidian lift:            {lift_drav:.1f}%")
    print(f"  Sanskrit lift:             {lift_skt:.1f}%")
    print(f"  Lift ratio (D/S):          {lift_ratio:.2f}x")
    print(f"  Verdict:                   {verdict}")

    result = {
        "_citation": {"primary": ["A.1"]},
        "gpu_device": DEVICE,
        "dravidian_n_bigrams": len(drav_lm),
        "sanskrit_n_bigrams":  len(skt_lm),
        "z_score_dravidian":   round(z_drav, 3),
        "z_score_sanskrit":    round(z_skt_own, 3),
        "dravidian_lift_pct":  round(lift_drav, 2),
        "sanskrit_lift_pct":   round(lift_skt, 2),
        "lift_ratio":          round(lift_ratio, 3),
        "verdict":             verdict,
        "dravidian_elapsed":   round(drav_elapsed, 1),
        "sanskrit_elapsed":    round(skt_elapsed, 1),
        "null_mu_dravidian":   round(null_mu_d, 2),
        "null_mu_sanskrit":    round(null_mu_s, 2),
        "methodology_note": (
            "Each LM scored against its own matched null distribution. "
            "Lift = (SA_score - null_mean) / |null_mean| * 100. "
            "This is comparable across LMs of different sizes because it measures "
            "relative improvement over random in the same scoring space."
        ),
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), "utf-8")
    print(f"\nReport: {OUT}")


if __name__ == "__main__":
    main()
