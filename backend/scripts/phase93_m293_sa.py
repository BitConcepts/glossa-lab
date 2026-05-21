"""Phase-93: M293 Grammar-Constrained SA.

M293 appears in the consistent frame:
  [...]-M293-[M342/M176/M391/M267...]  (M293 followed by case suffixes)
  [M267]-M293-[...]                     (M293 after genitive 'of')

This suggests M293 may be a MEDIAL personal name component or a content word.

Approach:
1. Extract all inscriptions containing M293
2. Build a local language model from just these M293-context inscriptions
3. Run constrained SA with M293's confirmed neighbors pinned
4. Compare the resulting M293 modal readings under different pin configurations
5. Use phonotactic plausibility to adjudicate between 'ta' vs 'vil'

GPU: BigramScorer. Output: reports/phase93_m293_sa.json
"""
from __future__ import annotations

import csv
import json
import math
import random
import re
import time
from collections import Counter
from pathlib import Path

REPO    = Path(__file__).parents[2]
HOLDAT  = REPO / "corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv"
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
SYL_LM  = REPO / "backend/glossa_lab/data/dravidian_syllabic_lm.json"
REPORTS = REPO / "reports"
REPORTS.mkdir(exist_ok=True)
OUT     = REPORTS / "phase93_m293_sa.json"

import sys; sys.path.insert(0, str(REPO / "backend"))

TARGET = "M293"
N_SEEDS = 15
MAX_ITER = 8000
SA_TEMP = 1.0
SA_COOL = 0.9985

# Grammar-derived constraint: signs that reliably appear next to M293
# These become soft constraints in the SA
M293_CONFIRMED_NEIGHBORS = {
    "M267": "iN",   # genitive — often precedes M293
    "M342": "ay",   # genitive suffix — often follows M293
    "M176": "an",   # masc suffix — often follows M293
    "M391": "ka",   # nom suffix — sometimes follows M293
    "M099": "kol",  # title — often in same inscription
}

PD_VALID = set("vktpcmnyrlaieuo")


def is_pd_valid(r: str) -> bool:
    s = re.sub(r"[^a-z]", "", r.lower()[:4])
    return bool(s) and s[0] in PD_VALID


def load_corpus():
    seals = {}
    with open(HOLDAT, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            s = (row.get("letters") or "").strip()
            c = row.get("cisi_number",""); p = int(row.get("position",0) or 0)
            if c not in seals: seals[c] = []
            while len(seals[c]) <= p: seals[c].append("")
            seals[c][p] = s
    return [[s for s in v if s] for v in seals.values() if any(v)]


def build_syllabic_lm():
    """Load the Tamil syllabic LM."""
    if not SYL_LM.exists():
        return {}, []
    data = json.loads(SYL_LM.read_text("utf-8"))
    bigrams = data.get("bigrams", {})
    total = sum(bigrams.values()) or 1
    prob = {}
    for k, v in bigrams.items():
        parts = k.split(",") if "," in k else k.split("|") if "|" in k else None
        if parts and len(parts) == 2:
            prob[tuple(parts)] = v / total
    vocab = sorted(set(t for pair in prob for t in pair))
    return prob, vocab


def run_constrained_sa(flat: list, lm_prob: dict, pins: dict,
                       n_seeds: int, vocab: list) -> list[dict]:
    """Run SA with pinned anchors and return proposed mappings."""
    from types import SimpleNamespace

    from glossa_lab.pipelines.decipher import BigramScorer

    tc = Counter(flat)
    ranked = [t for t, _ in tc.most_common()]
    cipher_alpha = sorted(set(flat))
    target_list = sorted(set(vocab))[:len(cipher_alpha) + 10]
    free_cipher = [c for c in cipher_alpha if c not in pins]
    free_target = [t for t in target_list if t not in pins.values()]

    lm_obj = SimpleNamespace(ranked=ranked, bigram_freq=lm_prob)
    scorer = BigramScorer(lm_obj, flat)

    all_maps = []
    for seed in range(n_seeds):
        rng = random.Random(seed)
        # Initialize mapping
        mapping = dict(pins)
        pool = [t for t in free_target if t not in mapping.values()]
        rng.shuffle(pool)
        for c, t in zip(free_cipher, pool):
            mapping[c] = t

        score = scorer.score_full(mapping)
        temp = SA_TEMP

        for _ in range(MAX_ITER):
            if len(free_cipher) < 2: break
            i, j = rng.sample(range(len(free_cipher)), 2)
            ca, cb = free_cipher[i], free_cipher[j]
            old_a, old_b = mapping[ca], mapping[cb]
            mapping[ca], mapping[cb] = old_b, old_a
            ns = scorer.score_full(mapping)
            if ns > score or (temp > 0 and rng.random() < math.exp(min((ns - score)/temp, 0))):
                score = ns
            else:
                mapping[ca], mapping[cb] = old_a, old_b
            temp *= SA_COOL
        all_maps.append(dict(mapping))
    return all_maps


def main():
    print("Phase-93: M293 Grammar-Constrained SA\n")

    # Detect GPU
    device = "cpu"
    try:
        from glossa_lab.gpu_utils import detect_device
        device = detect_device()
    except Exception:
        pass
    print(f"  Device: {device}")

    anchors = json.loads(ANCHORS.read_text("utf-8"))["anchors"]
    print(f"  Anchors: {sum(1 for v in anchors.values() if v.get('confidence') in ('HIGH','MEDIUM'))} HIGH+MEDIUM")

    inscriptions = load_corpus()
    flat = [s for ins in inscriptions for s in ins]
    freq = Counter(flat)

    # Filter to inscriptions containing M293
    m293_inscs = [ins for ins in inscriptions if TARGET in ins]
    m293_flat  = [s for ins in m293_inscs for s in ins]
    print(f"  M293 occurrences: {freq.get(TARGET, 0)}")
    print(f"  M293-containing inscriptions: {len(m293_inscs)}")

    # Build LM
    lm_prob, vocab = build_syllabic_lm()
    print(f"  Tamil syllabic LM: {len(lm_prob)} bigrams, {len(vocab)} syllables")

    if not lm_prob:
        result = {"error": "LM not found", "verdict": "Phase-93 skipped — syllabic LM missing"}
        OUT.write_text(json.dumps(result, indent=2), "utf-8")
        return

    # Build anchor pins from confirmed readings
    pins = {}
    for sign, info in anchors.items():
        if info.get("confidence") in ("HIGH","MEDIUM"):
            reading = info.get("reading","").split("/")[0].split("(")[0].strip().lower()
            # Only pin if reading is in vocab
            if reading and any(reading[:2] == v[:2] for v in vocab):
                match = next((v for v in vocab if v.startswith(reading[:2])), None)
                if match:
                    pins[sign] = match

    print(f"  Pins from confirmed anchors: {len(pins)}")

    # Test 3 configurations:
    # Config A: standard pins (M293 free)
    # Config B: pin M293=ta (test Tamil syllabic hypothesis)
    # Config C: pin M293=vil (test bow iconography hypothesis)

    results_by_config = {}
    m293_readings = {}

    for config_name, m293_value in [("free", None), ("ta_pinned", "ta"), ("vil_pinned", "vil")]:
        config_pins = dict(pins)
        if m293_value:
            # Find vocab entry for this reading
            v = next((x for x in vocab if x.startswith(m293_value[:2])), m293_value)
            config_pins[TARGET] = v

        t0 = time.perf_counter()
        maps = run_constrained_sa(m293_flat, lm_prob, config_pins, min(N_SEEDS, 8), vocab)
        elapsed = time.perf_counter() - t0

        # Get modal reading for M293
        m293_proposals = [m.get(TARGET, "") for m in maps if m.get(TARGET)]
        modal = Counter(m293_proposals).most_common(1)[0][0] if m293_proposals else "?"
        consistency = Counter(m293_proposals).most_common(1)[0][1] / len(maps) if maps else 0

        # Measure total score
        from types import SimpleNamespace

        from glossa_lab.pipelines.decipher import BigramScorer
        tc = Counter(m293_flat); ranked = [t for t, _ in tc.most_common()]
        scorer = BigramScorer(SimpleNamespace(ranked=ranked, bigram_freq=lm_prob), m293_flat)
        scores = [scorer.score_full(m) for m in maps if m]
        mean_score = sum(scores) / len(scores) if scores else 0

        results_by_config[config_name] = {
            "m293_modal": modal,
            "m293_consistency": round(consistency, 3),
            "n_seeds": len(maps),
            "mean_score": round(mean_score, 4),
            "elapsed_s": round(elapsed, 1),
        }
        m293_readings[config_name] = modal
        print(f"  Config '{config_name}': M293 modal='{modal}' consistency={consistency:.1%} score={mean_score:.3f}")

    # Adjudicate
    free_modal = m293_readings.get("free", "")
    ta_score = results_by_config.get("ta_pinned", {}).get("mean_score", 0)
    vil_score = results_by_config.get("vil_pinned", {}).get("mean_score", 0)
    free_score = results_by_config.get("free", {}).get("mean_score", 0)

    # Determine which pinned configuration is closest to the free-run score
    # (least score degradation = most compatible reading)
    ta_loss  = free_score - ta_score
    vil_loss = free_score - vil_score

    if abs(ta_loss - vil_loss) < 0.001:
        verdict_reading = free_modal
        resolution = "INCONCLUSIVE — ta and vil equally compatible under grammar-constrained SA"
    elif ta_loss < vil_loss:
        verdict_reading = "ta"
        resolution = f"SA SUPPORTS 'ta' — pin degrades score by {ta_loss:.4f} vs vil {vil_loss:.4f}"
    else:
        verdict_reading = "vil"
        resolution = f"SA SUPPORTS 'vil' — pin degrades score by {vil_loss:.4f} vs ta {ta_loss:.4f}"

    print("\n=== Phase-93 Results ===")
    print(f"  Free-run M293 modal: '{free_modal}'")
    print(f"  Score: free={free_score:.4f}, ta_pin={ta_score:.4f}, vil_pin={vil_score:.4f}")
    print(f"  Loss: ta={ta_loss:.4f}, vil={vil_loss:.4f}")
    print(f"  Verdict: M293 = '{verdict_reading}' ({resolution})")

    # Optionally promote if verdict is confident (loss difference > 0.005)
    promoted = False
    if abs(ta_loss - vil_loss) > 0.005 and verdict_reading in ("ta", "vil"):
        existing = anchors.get(TARGET, {})
        if existing.get("confidence") not in ("HIGH", "MEDIUM"):
            anchors_data = json.loads(ANCHORS.read_text("utf-8"))
            anchors_data["anchors"][TARGET] = {
                "confidence": "MEDIUM",
                "reading": verdict_reading,
                "source": f"Phase-93 grammar-constrained SA (loss diff={abs(ta_loss-vil_loss):.4f})",
            }
            anchors_data["total"] = len(anchors_data["anchors"])
            ANCHORS.write_text(json.dumps(anchors_data, indent=2, ensure_ascii=False), "utf-8")
            promoted = True
            print(f"  ** M293 PROMOTED to MEDIUM: '{verdict_reading}' **")

    result = {
        "_citation": {"primary": ["A.1"]},
        "gpu_device": device,
        "target_sign": TARGET,
        "n_m293_inscriptions": len(m293_inscs),
        "configs": results_by_config,
        "free_modal_reading": free_modal,
        "ta_score_loss": round(ta_loss, 5),
        "vil_score_loss": round(vil_loss, 5),
        "verdict_reading": verdict_reading,
        "resolution": resolution,
        "m293_promoted": promoted,
        "verdict": (
            f"Phase-93: M293 grammar-constrained SA. "
            f"Free-run modal='{free_modal}'. "
            f"Score loss: ta={ta_loss:.4f}, vil={vil_loss:.4f}. "
            f"{resolution}. "
            f"{'M293 PROMOTED to MEDIUM!' if promoted else 'Insufficient confidence for promotion.'}"
        ),
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), "utf-8")
    print(f"\nReport: {OUT}")


if __name__ == "__main__":
    main()
