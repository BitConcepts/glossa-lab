"""Phase-55: Multi-LM Ensemble Decipherment.

Run SA against 4 language models:
  1. Dravidian Tamil char LM (944 bigrams — current baseline)
  2. Dravidian syllabic LM (Phase-49 — new, syllable-level)
  3. Proto-Dravidian LM (built from DEDR *reconstructions — sound changes)
  4. Sanskrit syllable LM (adversarial negative — should diverge)

Signs whose SA assignments converge across all 4 Tamil/Dravidian LMs
(LM1, LM2, LM3 agree, LM4 disagrees) → HIGH CONFIDENCE decipherment.
Signs where LM1-LM3 agree but LM4 also agrees → ambiguous (may be shared).
Signs where LM1-LM3 disagree → UNCERTAIN.

This produces the FINAL confidence-stratified decipherment table.

GPU: BigramScorer on CUDA for all 4 runs.

Output: reports/phase55_ensemble.json
        reports/phase55_final_decipherment.json  ← THE main output
"""
from __future__ import annotations

import csv
import json
import math
import random
import sys
import time
from collections import Counter, defaultdict
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

HOLDAT_CSV   = REPO / "corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv"
CHAR_LM      = REPO / "backend/glossa_lab/data/dravidian_tamil_lm.json"
SYLLABIC_LM  = REPO / "backend/glossa_lab/data/dravidian_syllabic_lm.json"
SANSKRIT_LM  = REPO / "backend/glossa_lab/data/sanskrit_syllable_lm.json"
DEDR         = REPO / "reports/jambu-dedr/data/dedr/dedr_new.csv"
ANCHORS      = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
REPORTS      = REPO / "reports"
REPORTS.mkdir(exist_ok=True)
OUT          = REPORTS / "phase55_ensemble.json"
OUT_FINAL    = REPORTS / "phase55_final_decipherment.json"

# Reduced SA params for ensemble (4 runs, keep manageable)
N_RESTARTS = 5
MAX_ITER   = 20_000
SA_TEMP    = 1.0
SA_COOL    = 0.9997
N_SEEDS    = 3


def load_corpus():
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
    return [s for insc in inscriptions for s in insc], inscriptions


def load_lm(path: Path, name: str) -> dict | None:
    if not path.exists():
        print(f"  {name}: NOT FOUND at {path}")
        return None
    raw = json.loads(path.read_text("utf-8"))
    bigrams = raw.get("bigrams", {})
    total = sum(bigrams.values()) or 1
    prob = {}
    for k, v in bigrams.items():
        parts = k.split(",", 1) if "," in k else k.split("|", 1) if "|" in k else None
        if parts and len(parts) == 2:
            prob[tuple(parts)] = v / total
    print(f"  {name}: {len(prob)} bigrams")
    return prob if prob else None


def build_proto_dravidian_lm() -> dict | None:
    """Build a simple Proto-Dravidian LM from DEDR *reconstructed forms."""
    import re
    bigram_counts: Counter = Counter()
    try:
        with open(DEDR, encoding="utf-8", errors="replace") as f:
            for row in csv.reader(f):
                if len(row) > 2:
                    word = row[2].strip()
                    # Proto-Dravidian reconstructions often start with * or are in DEDR entry
                    # Extract romanized syllables
                    word = re.sub(r"[^a-zāīūēōḍṭṇṅñḷṟṉ]", "", word.lower())
                    if len(word) >= 4:
                        # Simple bigram: consecutive 2-char windows
                        for i in range(len(word)-3):
                            a = word[i:i+2]
                            b = word[i+2:i+4]
                            if re.match(r"[a-z]{2}", a) and re.match(r"[a-z]{2}", b):
                                bigram_counts[(a, b)] += 1
        total = sum(bigram_counts.values()) or 1
        prob = {(a, b): c/total for (a,b),c in bigram_counts.items() if c >= 2}
        print(f"  Proto-Dravidian LM (from DEDR): {len(prob)} bigrams")
        return prob if prob else None
    except Exception as e:
        print(f"  Proto-Dravidian LM build failed: {e}")
        return None


def build_scorer(bigram_prob: dict, flat: list):
    from glossa_lab.pipelines.decipher import BigramScorer
    tc: Counter = Counter()
    for (a, b) in bigram_prob: tc[a] += 1; tc[b] += 1
    ranked = [t for t, _ in tc.most_common()]
    return BigramScorer(SimpleNamespace(ranked=ranked, bigram_freq=bigram_prob), flat)


def run_sa_seeds(flat: list, scorer, bigram_prob: dict,
                 pinned: dict, n_seeds: int) -> list[dict]:
    cipher_alpha = sorted(set(flat))
    target_tokens = sorted(set(t for pair in bigram_prob for t in pair))
    while len(target_tokens) < len(cipher_alpha):
        target_tokens.append(f"?{len(target_tokens)}")
    free_cipher = [c for c in cipher_alpha if c not in pinned]

    all_mappings = []
    for seed in range(n_seeds):
        rng = random.Random(seed)
        def _init(sh):
            m = dict(pinned); used = set(m.values())
            pool = [t for t in target_tokens[:len(cipher_alpha)] if t not in used]
            if sh: rng.shuffle(pool)
            for c, t in zip(free_cipher, pool): m[c] = t
            return m
        mapping = _init(sh=False); score = scorer.score_full(mapping)
        temp = SA_TEMP
        best_score = score; best_map = dict(mapping)
        for restart in range(N_RESTARTS):
            if restart > 0: mapping = _init(sh=True); score = scorer.score_full(mapping); temp = SA_TEMP
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
            if score > best_score: best_score = score; best_map = dict(mapping)
        all_mappings.append(best_map)
    return all_mappings


def build_pins(flat: list, vocab_set: set) -> dict:
    HIGH_SYLL = {"M006":"pu","M016":"ka","M045":"ya","M062":"e","M099":"ko","M176":"an","M342":"ay"}
    pins = {}
    for sign, syl in HIGH_SYLL.items():
        if sign in set(flat):
            if syl in vocab_set: pins[sign] = syl
            else:
                match = next((s for s in sorted(vocab_set) if s.startswith(syl[:2])), None)
                if match: pins[sign] = match
    return pins


def main():
    print("Phase-55: Multi-LM Ensemble Decipherment\n")

    flat, inscriptions = load_corpus()
    print(f"Corpus: {len(set(flat))} unique signs, {len(flat)} tokens")

    # Load all 4 LMs
    print("\nLoading LMs:")
    lm1 = load_lm(CHAR_LM, "Tamil char (944-bigram)")
    lm2_raw = json.loads(SYLLABIC_LM.read_text("utf-8")) if SYLLABIC_LM.exists() else {}
    if lm2_raw:
        syl_freq = lm2_raw.get("syllable_freq", {})
        valid = {s for s, c in syl_freq.items() if c >= 3}
        total2 = sum(v for k, v in lm2_raw.get("bigrams", {}).items()
                     if k.split(",",1)[0] in valid and k.split(",",1)[1] in valid) or 1
        lm2 = {tuple(k.split(",",1)): v/total2
               for k, v in lm2_raw.get("bigrams", {}).items()
               if "," in k and k.split(",",1)[0] in valid and k.split(",",1)[1] in valid}
        print(f"  Tamil syllabic LM: {len(lm2)} bigrams")
    else:
        lm2 = None; print("  Tamil syllabic LM: NOT FOUND")
    lm3 = build_proto_dravidian_lm()
    lm4 = load_lm(SANSKRIT_LM, "Sanskrit syllable (adversarial)")

    lm_configs = [
        ("Tamil_char",     lm1),
        ("Tamil_syllabic", lm2),
        ("Proto_Dravidian", lm3),
        ("Sanskrit",       lm4),
    ]
    lm_configs = [(name, lm) for name, lm in lm_configs if lm is not None]
    print(f"\nRunning SA on {len(lm_configs)} LMs")

    # Per-LM results
    per_lm_mappings: dict[str, list[dict]] = {}
    per_lm_stats: dict[str, dict] = {}
    for lm_name, lm in lm_configs:
        vocab_set = set(t for pair in lm for t in pair)
        pins = build_pins(flat, vocab_set)
        scorer = build_scorer(lm, flat)
        print(f"\n  [{lm_name}] {len(lm)} bigrams, {len(pins)} pinned signs")
        t0 = time.perf_counter()
        mappings = run_sa_seeds(flat, scorer, lm, pins, N_SEEDS)
        elapsed = time.perf_counter() - t0
        per_lm_mappings[lm_name] = mappings
        print(f"    Done in {elapsed:.1f}s")
        per_lm_stats[lm_name] = {"n_bigrams": len(lm), "n_pinned": len(pins), "elapsed": round(elapsed,1)}

    # Build consensus across Dravidian LMs (LM1+LM2+LM3)
    dravidian_lm_names = [n for n, _ in lm_configs if n != "Sanskrit"]
    sanskrit_lm_name = "Sanskrit" if any(n == "Sanskrit" for n, _ in lm_configs) else None

    # Vote per sign per LM
    sign_lm_votes: dict[str, dict[str, Counter]] = defaultdict(lambda: defaultdict(Counter))
    for lm_name, mappings in per_lm_mappings.items():
        for m in mappings:
            for sign, reading in m.items():
                sign_lm_votes[sign][lm_name][reading] += 1

    freq = Counter(flat)
    final_table = []
    anchors = json.loads(ANCHORS.read_text("utf-8"))["anchors"]

    for sign in sorted(sign_lm_votes, key=lambda s: -freq.get(s, 0)):
        per_lm_best: dict[str, str] = {}
        for lm_name in [n for n, _ in lm_configs]:
            votes = sign_lm_votes[sign].get(lm_name, Counter())
            if votes: per_lm_best[lm_name] = votes.most_common(1)[0][0]

        # Do Dravidian LMs agree?
        drv_readings = [per_lm_best.get(n) for n in dravidian_lm_names if per_lm_best.get(n)]
        n_agree = sum(1 for r in drv_readings[1:] if r and r[:2] == drv_readings[0][:2]) if drv_readings else 0
        n_drv = len(drv_readings)
        drv_consensus = n_agree >= (n_drv - 1) and n_drv >= 2  # majority agreement
        best_drv = drv_readings[0] if drv_readings else "?"
        skt_reading = per_lm_best.get(sanskrit_lm_name, "") if sanskrit_lm_name else ""
        skt_differs = skt_reading and skt_reading[:2] != best_drv[:2]

        if drv_consensus and skt_differs:
            ensemble_confidence = "ENSEMBLE_HIGH"
        elif drv_consensus:
            ensemble_confidence = "ENSEMBLE_MEDIUM"
        elif drv_readings:
            ensemble_confidence = "ENSEMBLE_LOW"
        else:
            ensemble_confidence = "ENSEMBLE_UNRESOLVED"

        existing = anchors.get(sign, {})
        final_table.append({
            "sign": sign,
            "n_corpus": freq.get(sign, 0),
            "ensemble_reading": best_drv,
            "ensemble_confidence": ensemble_confidence,
            "dravidian_consensus": drv_consensus,
            "sanskrit_differs": bool(skt_differs),
            "per_lm": per_lm_best,
            "confirmed_reading": existing.get("reading", ""),
            "confirmed_confidence": existing.get("confidence", "UNREAD"),
        })

    n_ens_high = sum(1 for t in final_table if t["ensemble_confidence"] == "ENSEMBLE_HIGH")
    n_ens_med  = sum(1 for t in final_table if t["ensemble_confidence"] == "ENSEMBLE_MEDIUM")
    n_ens_low  = sum(1 for t in final_table if "LOW" in t["ensemble_confidence"])

    print("\n=== Ensemble Results ===")
    print(f"  ENSEMBLE_HIGH   (Dravidian agree, Sanskrit differs): {n_ens_high}")
    print(f"  ENSEMBLE_MEDIUM (Dravidian agree, Sanskrit also):    {n_ens_med}")
    print(f"  ENSEMBLE_LOW    (Dravidian disagree):                {n_ens_low}")

    print("\nTop ENSEMBLE_HIGH signs:")
    for t in [tt for tt in final_table if tt["ensemble_confidence"] == "ENSEMBLE_HIGH"][:15]:
        conf = t["confirmed_reading"]
        print(f"  {t['sign']:6s} n={t['n_corpus']:4d} SA={t['ensemble_reading']!r:10s} confirmed={conf!r}")

    # Save final decipherment
    OUT_FINAL.write_text(json.dumps(final_table, indent=2, ensure_ascii=False), "utf-8")
    print(f"\nFinal decipherment table: {OUT_FINAL}")

    result = {
        "_citation": {"primary": ["A.1"]},
        "gpu_device": DEVICE,
        "lm_configs": [n for n, _ in lm_configs],
        "per_lm_stats": per_lm_stats,
        "ensemble_summary": {
            "ENSEMBLE_HIGH": n_ens_high,
            "ENSEMBLE_MEDIUM": n_ens_med,
            "ENSEMBLE_LOW": n_ens_low,
        },
        "top_high_confidence": [t for t in final_table if t["ensemble_confidence"] == "ENSEMBLE_HIGH"][:30],
        "full_table_path": str(OUT_FINAL),
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), "utf-8")
    print(f"Report: {OUT}")


if __name__ == "__main__":
    main()
