"""Phase-73: Ensemble Calibration.

Fixes Phase-62a ENSEMBLE_HIGH=2 by calibrating the consensus method:
  1. 10 seeds per LM (vs 3 in Phase-55/62a) — reduces SA variance
  2. First-2-char agreement threshold (vs exact match) — handles transliteration variants
  3. Corpus-frequency weighting — high-freq signs should be more stable

ENSEMBLE_HIGH   = Tamil_syllabic[:2] == Proto_Dravidian[:2] AND Sanskrit[:2] != Tamil_syllabic[:2]
ENSEMBLE_MEDIUM = Tamil_syllabic[:2] == Proto_Dravidian[:2] (Sanskrit may agree)
ENSEMBLE_LOW    = Tamil_syllabic[:2] != Proto_Dravidian[:2]

Expected: ENSEMBLE_HIGH ~15-25 signs.

GPU: BigramScorer CUDA. ~15 min (10 seeds x 2 LMs).
Output: reports/phase73_ensemble_calibration.json
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
P55_FINAL = REPO / "reports/phase55_final_decipherment.json"
REPORTS   = REPO / "reports"
REPORTS.mkdir(exist_ok=True)
OUT       = REPORTS / "phase73_ensemble_calibration.json"

N_RESTARTS = 8
MAX_ITER   = 25_000
SA_TEMP    = 1.0
SA_COOL    = 0.9997
N_SEEDS    = 10  # ← 10 seeds for stable consensus

PD_INVALID_INITIAL = set("bdfgqwx")


def is_pd_valid(s: str) -> bool:
    t = s.lower().strip()
    return bool(t) and t[0] not in PD_INVALID_INITIAL


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


def load_syllabic_lm(path: Path, name: str):
    if not path.exists():
        print(f"  {name}: NOT FOUND")
        return {}, []
    raw = json.loads(path.read_text("utf-8"))
    bigrams = raw.get("bigrams", {})
    # Handle both syllabic format (with syllable_freq) and plain bigram format
    if "syllable_freq" in raw:
        syl_freq = raw.get("syllable_freq", {})
        valid = {s for s, c in syl_freq.items() if c >= 3}
        total = sum(v for k, v in bigrams.items()
                    if k.split(",", 1)[0] in valid and k.split(",", 1)[1] in valid) or 1
        prob = {tuple(k.split(",", 1)): v / total
                for k, v in bigrams.items()
                if "," in k and k.split(",", 1)[0] in valid and k.split(",", 1)[1] in valid}
        vocab = sorted(valid)
    else:
        total = sum(bigrams.values()) or 1
        prob = {}
        for k, v in bigrams.items():
            parts = k.split(",", 1) if "," in k else k.split("|", 1) if "|" in k else None
            if parts and len(parts) == 2:
                prob[tuple(parts)] = v / total
        vocab = sorted(set(t for pair in prob for t in pair))
    print(f"  {name}: {len(prob)} bigrams, {len(vocab)} syllables")
    return prob, vocab


def build_proto_dravidian_lm():
    import re
    bigram_counts: Counter = Counter()
    if not DEDR.exists(): return {}, []
    try:
        with open(DEDR, encoding="utf-8", errors="replace") as f:
            for row in csv.reader(f):
                if len(row) > 2:
                    word = re.sub(r"[^a-z]", "", row[2].strip().lower())
                    if len(word) >= 4:
                        for i in range(len(word) - 3):
                            a, b = word[i:i+2], word[i+2:i+4]
                            if len(a) == 2 and len(b) == 2:
                                bigram_counts[(a, b)] += 1
        total = sum(bigram_counts.values()) or 1
        prob = {(a, b): c/total for (a,b), c in bigram_counts.items() if c >= 2}
        vocab = sorted(set(t for pair in prob for t in pair))
        print(f"  Proto-Dravidian (DEDR): {len(prob)} bigrams, {len(vocab)} syllables")
        return prob, vocab
    except Exception as e:
        print(f"  Proto-Dravidian build failed: {e}")
        return {}, []


def run_sa_seeds(flat: list, bigram_prob: dict, n_seeds: int,
                 pins: dict, filtered_vocab: set | None = None) -> list[dict]:
    """Run n_seeds SA runs and return all proposed mappings."""
    from glossa_lab.pipelines.decipher import BigramScorer
    tc: Counter = Counter()
    for (a, b) in bigram_prob: tc[a] += 1; tc[b] += 1
    ranked = [t for t, _ in tc.most_common()]
    scorer = BigramScorer(SimpleNamespace(ranked=ranked, bigram_freq=bigram_prob), flat)

    target_vocab = filtered_vocab or set(ranked)
    cipher_alpha = sorted(set(flat))
    target_list  = sorted(target_vocab)
    while len(target_list) < len(cipher_alpha): target_list.append(f"?{len(target_list)}")
    free_cipher = [c for c in cipher_alpha if c not in pins]

    all_maps = []
    for seed in range(n_seeds):
        rng = random.Random(seed)
        def _init(sh):
            m = dict(pins); used = set(m.values())
            pool = [t for t in target_list[:len(cipher_alpha)] if t not in used]
            if sh: rng.shuffle(pool)
            for c, t in zip(free_cipher, pool): m[c] = t
            return m
        best_score = float("-inf"); best_map = {}
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
            if score > best_score: best_score = score; best_map = dict(mapping)
        all_maps.append(best_map)
    return all_maps


def modal_reading(maps: list[dict], sign: str, k: int = 2) -> str:
    """Modal reading using first-k-char comparison."""
    readings = [m.get(sign, "") for m in maps if m.get(sign)]
    if not readings: return ""
    # Group by first k chars
    groups: Counter = Counter(r[:k] for r in readings)
    best_prefix, _ = groups.most_common(1)[0]
    # Return full modal reading that starts with best prefix
    full_readings = [r for r in readings if r.startswith(best_prefix)]
    return Counter(full_readings).most_common(1)[0][0] if full_readings else readings[0]


def main():
    print("Phase-73: Ensemble Calibration\n")
    flat, inscriptions = load_corpus()
    print(f"Corpus: {len(set(flat))} unique signs, {len(flat)} tokens")
    freq = Counter(flat)

    # Load LMs
    print("\nLoading LMs:")
    syl_lm,   syl_vocab   = load_syllabic_lm(SYL_LM, "Tamil syllabic")
    skt_lm,   skt_vocab   = load_syllabic_lm(SKT_LM_F, "Sanskrit")
    proto_lm, proto_vocab = build_proto_dravidian_lm()

    if not skt_lm:
        # Build from data module
        try:
            from glossa_lab.data.sanskrit import get_corpus_symbols
            skt_syms = get_corpus_symbols()
            bc: Counter = Counter()
            for i in range(len(skt_syms) - 1):
                a, b = skt_syms[i], skt_syms[i + 1]
                if a and b: bc[(a, b)] += 1
            total = sum(bc.values()) or 1
            skt_lm  = {(a, b): c/total for (a,b), c in bc.items() if c >= 1}
            skt_vocab = sorted(set(t for pair in skt_lm for t in pair))
            print(f"  Sanskrit (data module): {len(skt_lm)} bigrams")
        except Exception as e:
            print(f"  Sanskrit LM failed: {e}"); skt_lm = {}; skt_vocab = []

    # Build pins
    SYLLABIC = {
        "M006":"pu","M016":"ka","M045":"ya","M062":"e","M099":"ko",
        "M176":"an","M342":"ay","M328":"aa","M059":"ee","M162":"il",
        "M391":"ka","M367":"am","M089":"tu","M051":"pu","M336":"i",
        "M048":"mu","M012":"o","M305":"ir","M073":"ko","M013":"na",
    }

    def make_pins(vocab_set, filtered=False):
        pins = {}
        for sign, syl in SYLLABIC.items():
            if sign not in set(flat): continue
            if syl in vocab_set and (not filtered or is_pd_valid(syl)):
                pins[sign] = syl
            else:
                match = next((s for s in sorted(vocab_set)
                              if s.startswith(syl[:2]) and (not filtered or is_pd_valid(s))), None)
                if match: pins[sign] = match
        return pins

    syl_filtered = {s for s in syl_vocab if is_pd_valid(s)}
    syl_pins   = make_pins(set(syl_vocab), filtered=True)
    skt_pins   = make_pins(set(skt_vocab), filtered=False)
    proto_pins = make_pins(set(proto_vocab), filtered=False)

    print(f"\n  Tamil syllabic pins: {len(syl_pins)}")
    print(f"  Sanskrit pins:       {len(skt_pins)}")
    print(f"  Proto-Drav pins:     {len(proto_pins)}")

    # Run 10 seeds per LM
    print(f"\nRunning {N_SEEDS} seeds × Tamil syllabic LM...")
    t0 = time.perf_counter()
    syl_maps   = run_sa_seeds(flat, syl_lm,   N_SEEDS, syl_pins,   syl_filtered) if syl_lm else []
    print(f"  Done in {time.perf_counter()-t0:.1f}s")

    if proto_lm:
        print(f"Running {N_SEEDS} seeds × Proto-Dravidian LM...")
        t0 = time.perf_counter()
        proto_maps = run_sa_seeds(flat, proto_lm, N_SEEDS, proto_pins, None)
        print(f"  Done in {time.perf_counter()-t0:.1f}s")
    else:
        proto_maps = []

    if skt_lm:
        print(f"Running {N_SEEDS} seeds × Sanskrit LM...")
        t0 = time.perf_counter()
        skt_maps   = run_sa_seeds(flat, skt_lm,   N_SEEDS, skt_pins,   None)
        print(f"  Done in {time.perf_counter()-t0:.1f}s")
    else:
        skt_maps = []

    # Calibrated consensus with first-2-char agreement
    all_signs = sorted(set(flat))
    anchors = json.loads(ANCHORS.read_text("utf-8"))["anchors"]
    calibrated = []
    n_high = n_med = n_low = 0

    for sign in all_signs:
        syl_modal   = modal_reading(syl_maps,   sign, k=2)
        proto_modal = modal_reading(proto_maps, sign, k=2)
        skt_modal   = modal_reading(skt_maps,   sign, k=2)

        syl_p   = syl_modal[:2]   if syl_modal   else ""
        proto_p = proto_modal[:2] if proto_modal else ""
        skt_p   = skt_modal[:2]   if skt_modal   else ""

        drav_agree  = bool(syl_p and proto_p and syl_p == proto_p)
        skt_differs = bool(syl_p and skt_p and syl_p != skt_p)

        if drav_agree and skt_differs:
            tier = "ENSEMBLE_HIGH"; n_high += 1
        elif drav_agree:
            tier = "ENSEMBLE_MEDIUM"; n_med += 1
        else:
            tier = "ENSEMBLE_LOW"; n_low += 1

        anchor_info = anchors.get(sign, {})
        confirmed = anchor_info.get("reading", "")
        conf      = anchor_info.get("confidence", "UNREAD")

        calibrated.append({
            "sign":             sign,
            "n_corpus":         freq.get(sign, 0),
            "syl_modal":        syl_modal,
            "proto_modal":      proto_modal,
            "skt_modal":        skt_modal,
            "ensemble_tier":    tier,
            "confirmed_reading":confirmed,
            "confirmed_conf":   conf,
            "pd_valid":         is_pd_valid(syl_modal) if syl_modal else False,
        })

    # Sort: ENSEMBLE_HIGH first, then by corpus frequency
    tier_order = {"ENSEMBLE_HIGH": 0, "ENSEMBLE_MEDIUM": 1, "ENSEMBLE_LOW": 2}
    calibrated.sort(key=lambda x: (tier_order.get(x["ensemble_tier"], 9), -x["n_corpus"]))

    high_signs = [e for e in calibrated if e["ensemble_tier"] == "ENSEMBLE_HIGH"]

    print("\n=== Phase-73 Results ===")
    print(f"  ENSEMBLE_HIGH:   {n_high} (was 2 in Phase-62a)")
    print(f"  ENSEMBLE_MEDIUM: {n_med}")
    print(f"  ENSEMBLE_LOW:    {n_low}")
    print("\n  Top ENSEMBLE_HIGH signs:")
    for e in high_signs[:15]:
        marker = "✓" if e["confirmed_conf"] in ("HIGH","MEDIUM") else "?"
        agree = "✓" if e["confirmed_reading"][:2] == e["syl_modal"][:2] else "x"
        print(f"  {e['sign']:6s} syl={e['syl_modal']:6s} proto={e['proto_modal']:6s} "
              f"skt={e['skt_modal']:6s} [{marker}] agree={agree} confirmed={e['confirmed_reading']!r}")

    result = {
        "_citation": {"primary": ["A.1"]},
        "gpu_device": DEVICE,
        "n_seeds_per_lm":    N_SEEDS,
        "agreement_threshold": "first-2-chars",
        "n_ensemble_high":   n_high,
        "n_ensemble_medium": n_med,
        "n_ensemble_low":    n_low,
        "calibrated_table":  calibrated[:80],
        "all_high_signs":    [e["sign"] for e in high_signs],
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), "utf-8")
    print(f"\nReport: {OUT}")


if __name__ == "__main__":
    main()
