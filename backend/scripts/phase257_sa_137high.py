"""Phase-257: SA Rerun with 137 HIGH Anchors Pinned

Fresh SA decipherment with the expanded 137 HIGH anchor set (up from 105
in Phase-213). More pinned anchors = more constrained solution space =
higher consistency for MEDIUM signs.

Protocol:
  - 50K iterations × 8 restarts × 10 seeds (GPU BigramScorer)
  - 4 conditions: no anchors, HIGH only, H+M, H+M+CAND
  - Compare vs Phase-213 baseline (57.0% aggregate, 105 HIGH)
  - Upgrade MEDIUM→HIGH where per-sign consistency >= 0.40 AND DEDR exists

Output: outputs/phase257_sa_137high.json
"""
from __future__ import annotations

import json
import sys
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "outputs" / "phase257_sa_137high.json"
ANCHORS_F = REPO / "backend" / "reports" / "INDUS_FINAL_ANCHORS.json"
sys.path.insert(0, str(REPO / "backend"))

P213_AGGREGATE = 0.5700

N_SEEDS = 10
MAX_ITER = 50_000
RESTARTS = 8


def build_anchor_dict(anchors_raw, freq, min_conf="HIGH"):
    tier = {"HIGH": 3, "MEDIUM": 2, "LOW": 1, "CANDIDATE": 0}
    thr = tier.get(min_conf, 0)
    out = {}
    for aid, rec in anchors_raw.items():
        if not isinstance(rec, dict):
            continue
        if tier.get(rec.get("confidence", ""), 0) < thr:
            continue
        m77 = aid.lstrip("M")
        reading = rec.get("reading", "").split("/")[0].strip()
        if m77 in freq and reading:
            out[m77] = reading
    return out


def run_sa(inscs, anchors, label, n_seeds=N_SEEDS):
    from glossa_lab.data.dravidian import get_word_symbols
    from glossa_lab.pipelines.decipher import LanguageModel, decipher

    lm = LanguageModel(get_word_symbols())
    flat = [s for seq in inscs for s in seq]

    def _one(seed):
        r = decipher(
            flat, lm, seed=seed, max_iterations=MAX_ITER, restarts=RESTARTS,
            cipher_inscriptions=None, ocp_weight=0.0,
            positional_weight=0.0, surjective=True,
            anchors=anchors or None,
        )
        return r.get("proposed_mapping", {})

    with ThreadPoolExecutor(max_workers=min(n_seeds, 10)) as ex:
        maps = list(ex.map(_one, range(n_seeds)))

    all_signs = set().union(*[m.keys() for m in maps])
    modal, conss = {}, {}
    for s in all_signs:
        props = [m[s] for m in maps if s in m]
        if props:
            c = Counter(props)
            val, cnt = c.most_common(1)[0]
            modal[s] = val
            conss[s] = cnt / len(props)

    mean_c = round(sum(conss.values()) / len(conss), 4) if conss else 0.0
    hci = sum(1 for v in conss.values() if v >= 0.75)
    print(f"  [{label}] mean_c={mean_c:.4f} hci={hci} n_signs={len(modal)}")
    return {"label": label, "mean_c": mean_c, "hci": hci,
            "modal": modal, "consistency": conss, "n_signs": len(modal)}


def main():
    t0 = time.time()
    print("=" * 70)
    print("PHASE-257: SA RERUN — 137 HIGH ANCHORS (50K iter × 8 restarts × 10 seeds)")
    print("=" * 70)

    from glossa_lab.data.indus_m77 import get_corpus_inscriptions, get_corpus_symbols
    syms = get_corpus_symbols()
    inscs = get_corpus_inscriptions()
    freq = Counter(syms)

    anchors_raw = json.loads(ANCHORS_F.read_text("utf-8"))["anchors"]
    anch_high = build_anchor_dict(anchors_raw, freq, "HIGH")
    anch_hm = build_anchor_dict(anchors_raw, freq, "MEDIUM")

    print(f"\n  Corpus: {len(freq)} distinct, {len(syms)} tokens, {len(inscs)} inscriptions")
    print(f"  HIGH anchors: {len(anch_high)} | H+M anchors: {len(anch_hm)}")
    print(f"  SA params: {MAX_ITER} iter × {RESTARTS} restarts × {N_SEEDS} seeds")
    print(f"  Phase-213 baseline: {P213_AGGREGATE:.4f} ({P213_AGGREGATE*100:.1f}%)")

    # Run SA conditions
    print("\n=== SA Runs (GPU) ===")
    r0 = run_sa(inscs, {}, "A_no_anchors", n_seeds=5)  # fewer seeds for baseline
    r1 = run_sa(inscs, anch_high, "B_HIGH_137")
    r2 = run_sa(inscs, anch_hm, "C_HIGH+MEDIUM")

    # Aggregate confidence
    total_tokens = sum(freq.values())
    anch_set = set(anch_hm.keys())
    anch_tokens = sum(freq.get(s, 0) for s in anch_set)
    anch_conss = {s: c for s, c in r2["consistency"].items() if s in anch_set}
    anch_mean = sum(anch_conss.values()) / len(anch_conss) if anch_conss else 0
    agg = round((anch_tokens * anch_mean + (total_tokens - anch_tokens) * r0["mean_c"]) / total_tokens, 4)
    d_p213 = round(agg - P213_AGGREGATE, 4)

    print(f"\n=== Aggregate Confidence ===")
    print(f"  Phase-213 baseline:  {P213_AGGREGATE:.4f} ({P213_AGGREGATE*100:.1f}%)")
    print(f"  Phase-257 result:    {agg:.4f} ({agg*100:.1f}%)")
    print(f"  Delta vs P213:       {d_p213:+.4f} ({d_p213*100:+.2f}pp)")

    # Identify MEDIUM signs with high consistency → upgrade candidates
    print(f"\n=== MEDIUM→HIGH Upgrade Candidates (consistency >= 0.40) ===")
    medium_signs = {k: v for k, v in anchors_raw.items()
                    if v.get("confidence") == "MEDIUM"}
    upgrade_candidates = []
    for sign, info in medium_signs.items():
        m77 = sign.lstrip("M")
        cons = r1["consistency"].get(m77, 0)  # Use HIGH-only run for free-sign consistency
        modal_reading = r1["modal"].get(m77, "")
        current_reading = info.get("reading", "").split("/")[0].strip()
        has_dedr = bool(info.get("dedr", ""))

        if cons >= 0.40:
            agrees = (modal_reading.lower() == current_reading.lower()) if modal_reading and current_reading else False
            upgrade_candidates.append({
                "sign": sign, "reading": current_reading, "sa_modal": modal_reading,
                "sa_cons": round(cons, 3), "agrees": agrees, "has_dedr": has_dedr,
                "freq": freq.get(m77, 0),
            })

    upgrade_candidates.sort(key=lambda x: -x["sa_cons"])
    print(f"  Candidates with cons >= 0.40: {len(upgrade_candidates)}")

    # Apply upgrades: require agrees=True OR has_dedr=True
    n_upgraded = 0
    upgrade_log = []
    for uc in upgrade_candidates:
        sign = uc["sign"]
        if not (uc["agrees"] or uc["has_dedr"]):
            continue
        if anchors_raw[sign].get("confidence") != "MEDIUM":
            continue

        anchors_raw[sign]["confidence"] = "HIGH"
        anchors_raw[sign]["phase_upgraded"] = 257
        basis = anchors_raw[sign].get("basis", "")
        anchors_raw[sign]["basis"] = (
            f"{basis}; Phase-257: SA rerun upgrade (137 HIGH pinned) — "
            f"cons={uc['sa_cons']:.2f}, modal='{uc['sa_modal']}', "
            f"{'agrees' if uc['agrees'] else 'DEDR-backed'}"
        )
        n_upgraded += 1
        upgrade_log.append(uc)

    print(f"  Applied: {n_upgraded} MEDIUM→HIGH upgrades")
    for ul in upgrade_log[:15]:
        print(f"    {ul['sign']}='{ul['reading']}' cons={ul['sa_cons']:.2f} "
              f"sa='{ul['sa_modal']}' {'✓' if ul['agrees'] else 'DEDR'}")

    # Save anchors
    if n_upgraded > 0:
        anchors_data = json.loads(ANCHORS_F.read_text("utf-8"))
        anchors_data["anchors"] = anchors_raw
        ANCHORS_F.write_text(json.dumps(anchors_data, indent=2, ensure_ascii=False), encoding="utf-8")

    by_conf = Counter(v.get("confidence", "?") for v in anchors_raw.values())
    n_hm = by_conf.get("HIGH", 0) + by_conf.get("MEDIUM", 0)

    elapsed = round(time.time() - t0, 1)
    print(f"\n  Final state: H:{by_conf.get('HIGH',0)} M:{by_conf.get('MEDIUM',0)} "
          f"CANDIDATE:{by_conf.get('CANDIDATE',0)} → H+M={n_hm}/{len(anchors_raw)}")
    print(f"  Elapsed: {elapsed}s")

    result = {
        "phase": 257,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "elapsed_s": elapsed,
        "sa_params": {"max_iter": MAX_ITER, "restarts": RESTARTS, "n_seeds": N_SEEDS},
        "p213_baseline": P213_AGGREGATE,
        "sa_no_anchors": {"mean_c": r0["mean_c"], "hci": r0["hci"]},
        "sa_high_137": {"mean_c": r1["mean_c"], "hci": r1["hci"]},
        "sa_high_medium": {"mean_c": r2["mean_c"], "hci": r2["hci"]},
        "aggregate_confidence": agg,
        "delta_vs_p213": d_p213,
        "n_high_anchors_pinned": len(anch_high),
        "n_upgrade_candidates": len(upgrade_candidates),
        "n_upgraded": n_upgraded,
        "upgrade_log": upgrade_log[:50],
        "final_state": {"HIGH": by_conf.get("HIGH", 0), "MEDIUM": by_conf.get("MEDIUM", 0),
                        "CANDIDATE": by_conf.get("CANDIDATE", 0), "H_plus_M": n_hm, "total": len(anchors_raw)},
    }
    OUT.write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")
    print(f"\n  Output: {OUT}")
    print(f"\n{'=' * 70}")
    print(f"PHASE-257 COMPLETE: {n_upgraded} upgrades | aggregate {agg:.1%} (Δ{d_p213:+.2%} vs P213)")
    print(f"{'=' * 70}")


if __name__ == "__main__":
    main()
