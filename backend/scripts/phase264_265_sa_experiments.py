"""Phase 264-265: Expanded LM SA + CISI Cross-Corpus SA

Phase-264: Build expanded Dravidian LM from DEDR cognates CSV (3791 entries)
           + existing word symbols. Re-run SA with expanded LM.
Phase-265: Run SA on CISI corpus (178 inscriptions) with HIGH M-signs
           as anchors via the Parpola-Mahadevan crosswalk.

Output: outputs/phase264_265_sa_experiments.json
"""
from __future__ import annotations

import csv
import json
import os
import re
import sys
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "outputs" / "phase264_265_sa_experiments.json"
ANCHORS_F = REPO / "backend" / "reports" / "INDUS_FINAL_ANCHORS.json"
DEDR_CSV = REPO / "backend" / "glossa_lab" / "data" / "phase16_corpora" / "dedr_cognates.csv"

sys.path.insert(0, str(REPO / "backend"))
os.environ.setdefault("GLOSSA_DATA_DIR", str(REPO / "backend" / "data"))

N_SEEDS = 8
MAX_ITER = 30_000
RESTARTS = 5


def build_anchor_dict(anchors_raw, freq, min_conf="HIGH"):
    tier = {"HIGH": 3, "MEDIUM": 2, "LOW": 1, "CANDIDATE": 0}
    thr = tier.get(min_conf, 0)
    out = {}
    for aid, rec in anchors_raw.items():
        if not isinstance(rec, dict): continue
        if tier.get(rec.get("confidence",""),0) < thr: continue
        m77 = aid.lstrip("M")
        reading = rec.get("reading","").split("/")[0].strip()
        if m77 in freq and reading:
            out[m77] = reading
    return out


def run_sa(flat, lm, anchors, label, n_seeds=N_SEEDS):
    from glossa_lab.pipelines.decipher import decipher
    def _one(seed):
        r = decipher(flat, lm, seed=seed, max_iterations=MAX_ITER, restarts=RESTARTS,
                     cipher_inscriptions=None, ocp_weight=0.0,
                     positional_weight=0.0, surjective=True,
                     anchors=anchors or None)
        return r.get("proposed_mapping", {})
    with ThreadPoolExecutor(max_workers=min(n_seeds, 8)) as ex:
        maps = list(ex.map(_one, range(n_seeds)))
    all_signs = set().union(*[m.keys() for m in maps])
    modal, conss = {}, {}
    for s in all_signs:
        props = [m[s] for m in maps if s in m]
        if props:
            c = Counter(props); val, cnt = c.most_common(1)[0]
            modal[s] = val; conss[s] = cnt / len(props)
    mean_c = round(sum(conss.values()) / len(conss), 4) if conss else 0.0
    hci = sum(1 for v in conss.values() if v >= 0.75)
    print(f"  [{label}] mean_c={mean_c:.4f} hci={hci} n_signs={len(modal)}")
    return {"label": label, "mean_c": mean_c, "hci": hci, "modal": modal,
            "consistency": conss, "n_signs": len(modal)}


def extract_dedr_words() -> list[str]:
    """Extract Tamil/Dravidian word forms from DEDR cognates CSV."""
    words = []
    with open(DEDR_CSV, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            text = row.get("raw_text", "")
            # Extract Tamil words (Ta. abbreviation marks Tamil entries)
            # Look for patterns like: Ta. word, word; or word (meaning)
            for match in re.finditer(r'Ta\.\s+([a-zāēīōūṭṇḷṟṉñḍṃ]+)', text, re.I):
                w = match.group(1).lower().strip()
                if len(w) >= 2 and w.isascii() is False:  # Keep Dravidian chars
                    words.append(w)
            # Also extract plain romanized Tamil words
            for match in re.finditer(r'\b([a-z]{2,12})\b', text):
                w = match.group(1).lower()
                if len(w) >= 2:
                    words.append(w)
    return words


def main():
    t0 = time.time()
    print("=" * 70)
    print("PHASE 264-265: EXPANDED LM SA + CISI CROSS-CORPUS SA")
    print("=" * 70)

    anchors_raw = json.loads(ANCHORS_F.read_text("utf-8"))["anchors"]

    # ── Phase 264: Expanded Dravidian LM ────────────────────────────────────
    print("\n=== PHASE-264: EXPANDED DRAVIDIAN LM SA ===")

    from glossa_lab.data.dravidian import get_word_symbols
    from glossa_lab.data.indus_m77 import get_corpus_inscriptions, get_corpus_symbols
    from glossa_lab.pipelines.decipher import LanguageModel

    base_words = get_word_symbols()
    dedr_words = extract_dedr_words()
    expanded = base_words + dedr_words
    print(f"  Base LM: {len(set(base_words))} unique ({len(base_words)} tokens)")
    print(f"  DEDR additions: {len(set(dedr_words))} unique ({len(dedr_words)} tokens)")
    print(f"  Expanded LM: {len(set(expanded))} unique ({len(expanded)} tokens)")

    lm_expanded = LanguageModel(expanded)
    lm_base = LanguageModel(base_words)

    m77_syms = get_corpus_symbols()
    m77_inscs = get_corpus_inscriptions()
    freq = Counter(m77_syms)
    flat = [s for seq in m77_inscs for s in seq]

    anch_high = build_anchor_dict(anchors_raw, freq, "HIGH")
    print(f"  M77 corpus: {len(freq)} distinct, {len(flat)} tokens")
    print(f"  HIGH anchors in M77: {len(anch_high)}")

    # Run SA with expanded LM vs base LM
    r_base = run_sa(flat, lm_base, anch_high, "264a_base_LM", n_seeds=5)
    r_expanded = run_sa(flat, lm_expanded, anch_high, "264b_expanded_LM", n_seeds=5)

    delta = round(r_expanded["mean_c"] - r_base["mean_c"], 4)
    print(f"\n  Base LM mean_c:     {r_base['mean_c']:.4f}")
    print(f"  Expanded LM mean_c: {r_expanded['mean_c']:.4f}")
    print(f"  Delta:              {delta:+.4f}")

    # ── Phase 265: CISI Cross-Corpus SA ─────────────────────────────────────
    print("\n=== PHASE-265: CISI CROSS-CORPUS SA ===")

    from glossa_lab.data.indus_cisi import get_corpus_inscriptions as cisi_inscs
    from glossa_lab.data.indus_cisi import get_corpus_symbols as cisi_syms

    cisi_s = cisi_syms()
    cisi_i = cisi_inscs()
    cisi_freq = Counter(cisi_s)
    cisi_flat = [s for seq in cisi_i for s in seq]
    print(f"  CISI corpus: {len(cisi_freq)} distinct, {len(cisi_flat)} tokens, {len(cisi_i)} inscriptions")

    # Build CISI anchors from HIGH M-signs via crosswalk
    # CISI uses P-codes; our anchors use M-codes. We need signs that appear in both.
    # For signs with P-prefix, use directly. For M-prefix signs that appear in CISI
    # corpus as their numeric IDs, map them.
    cisi_anchors = {}
    for aid, rec in anchors_raw.items():
        if rec.get("confidence") != "HIGH": continue
        reading = rec.get("reading","").split("/")[0].strip()
        if not reading: continue
        # Try direct P-code
        if aid.startswith("P"):
            p_num = aid.lstrip("P")
            if p_num in cisi_freq:
                cisi_anchors[p_num] = reading
        # Try M-code as numeric
        m_num = aid.lstrip("M")
        if m_num in cisi_freq:
            cisi_anchors[m_num] = reading

    print(f"  HIGH anchors mapped to CISI: {len(cisi_anchors)}")

    if len(cisi_anchors) >= 3:
        r_cisi = run_sa(cisi_flat, lm_base, cisi_anchors, "265_CISI_SA")
    else:
        print("  Too few CISI anchors — skipping SA run")
        r_cisi = {"label": "265_CISI_SA", "mean_c": 0, "hci": 0, "modal": {}, "consistency": {}, "n_signs": 0}

    elapsed = round(time.time() - t0, 1)
    print(f"\n  Elapsed: {elapsed}s")

    result = {
        "phase": "264_265",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "elapsed_s": elapsed,
        "phase264": {
            "base_lm_vocab": len(set(base_words)),
            "expanded_lm_vocab": len(set(expanded)),
            "dedr_additions": len(set(dedr_words)),
            "base_mean_c": r_base["mean_c"],
            "expanded_mean_c": r_expanded["mean_c"],
            "delta": delta,
            "base_hci": r_base["hci"],
            "expanded_hci": r_expanded["hci"],
        },
        "phase265": {
            "cisi_distinct": len(cisi_freq),
            "cisi_tokens": len(cisi_flat),
            "cisi_inscriptions": len(cisi_i),
            "n_cisi_anchors": len(cisi_anchors),
            "mean_c": r_cisi["mean_c"],
            "hci": r_cisi["hci"],
            "n_signs": r_cisi["n_signs"],
        },
    }
    OUT.write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")
    print(f"\n  Output: {OUT}")
    print(f"\n{'='*70}")
    print(f"PHASE 264-265 COMPLETE | LM delta: {delta:+.4f} | CISI mean_c: {r_cisi['mean_c']:.4f}")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()
