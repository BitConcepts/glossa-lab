"""Phase 193 — SA Rerun with 402-Anchor Set

Runs SA (5 seeds) with the full updated anchor set against the M77 corpus,
using the correct M77 ID mapping ('047' vs 'M047'). Reports:

  - Per-condition consistency (no anchors / HIGH only / HIGH+MEDIUM / all)
  - HCI count (high-consistency signs ≥ 0.75)
  - Which of the 5 Phase-192 new entries are SA-confirmed
  - Top 10 unanchored signs by consistency (candidate upgrades)
  - Aggregate confidence estimate
"""
from __future__ import annotations
import json, sys
from pathlib import Path
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

REPO_ROOT = Path(__file__).resolve().parents[2]
OUTPUTS   = REPO_ROOT / "outputs"
REPORTS   = REPO_ROOT / "research" / "indus" / "phase_reports"
ANCHOR_F  = REPO_ROOT / "backend" / "reports" / "INDUS_FINAL_ANCHORS.json"
sys.path.insert(0, str(REPO_ROOT / "backend"))
OUTPUTS.mkdir(exist_ok=True)
REPORTS.mkdir(parents=True, exist_ok=True)


def build_anchor_dict(anchors_raw: dict, freq: Counter,
                      min_conf: str = "HIGH") -> dict[str, str]:
    """Build anchor dict in M77 format from INDUS_FINAL_ANCHORS."""
    tier_order = {"HIGH": 3, "MEDIUM": 2, "LOW": 1, "CANDIDATE": 0}
    min_tier   = tier_order.get(min_conf, 0)
    out: dict[str, str] = {}
    for anchor_id, rec in anchors_raw.items():
        if not isinstance(rec, dict):
            continue
        conf = rec.get("confidence", "")
        if tier_order.get(conf, 0) < min_tier:
            continue
        m77_id  = anchor_id.lstrip("M")
        reading = rec.get("reading", "").split("/")[0].strip()
        if m77_id in freq and reading:
            out[m77_id] = reading
    return out


def run_sa(inscs, anchors: dict, label: str, n_seeds: int = 5) -> dict:
    from glossa_lab.pipelines.decipher import decipher, LanguageModel
    from glossa_lab.data.dravidian import get_word_symbols
    lm   = LanguageModel(get_word_symbols())
    flat = [s for insc in inscs for s in insc]

    def _one(seed):
        r = decipher(flat, lm, seed=seed, max_iterations=5000, restarts=5,
                     cipher_inscriptions=None, ocp_weight=0.0,
                     positional_weight=0.0, surjective=True,
                     anchors=anchors or None)
        return r.get("proposed_mapping", {})

    with ThreadPoolExecutor(max_workers=n_seeds) as ex:
        maps = list(ex.map(_one, range(n_seeds)))

    all_signs = set().union(*[m.keys() for m in maps])
    modal: dict[str, str] = {}
    conss: dict[str, float] = {}
    for s in all_signs:
        props = [m[s] for m in maps if s in m]
        if props:
            from collections import Counter as C
            mc_val, mc_cnt = C(props).most_common(1)[0]
            modal[s] = mc_val
            conss[s] = mc_cnt / len(props)

    mean_c = round(sum(conss.values()) / len(conss), 4) if conss else 0.0
    hci    = sum(1 for v in conss.values() if v >= 0.75)
    print(f"  [{label}] mean_c={mean_c:.4f} hci={hci} n_signs={len(modal)}")
    return {"label": label, "mean_c": mean_c, "hci": hci,
            "modal": modal, "consistency": conss, "n_signs": len(modal)}


def main():
    import time
    t0 = time.time()
    print("=" * 60)
    print("Phase 193 — SA Rerun with 402-Anchor Set")
    print("=" * 60)

    from glossa_lab.data.indus_m77 import get_corpus_symbols, get_corpus_inscriptions
    syms  = get_corpus_symbols()
    inscs = get_corpus_inscriptions()
    freq  = Counter(syms)
    anchors_raw = json.loads(ANCHOR_F.read_text())["anchors"]

    print(f"\nM77: {len(freq)} distinct signs, {len(syms)} tokens, {len(inscs)} inscriptions")

    # Build 4 anchor tiers
    anch_high   = build_anchor_dict(anchors_raw, freq, "HIGH")
    anch_medium = build_anchor_dict(anchors_raw, freq, "MEDIUM")
    anch_low    = build_anchor_dict(anchors_raw, freq, "LOW")

    print(f"  Anchors HIGH:        {len(anch_high)}")
    print(f"  Anchors HIGH+MEDIUM: {len(anch_medium)}")
    print(f"  Anchors ALL (incl LOW): {len(anch_low)}")

    print("\n=== SA Runs ===")
    r0 = run_sa(inscs, {},          "A_no_anchors")
    r1 = run_sa(inscs, anch_high,   "B_HIGH_only")
    r2 = run_sa(inscs, anch_medium, "C_HIGH+MEDIUM")
    r3 = run_sa(inscs, anch_low,    "D_ALL_anchors")

    d1 = round(r1["mean_c"] - r0["mean_c"], 4)
    d2 = round(r2["mean_c"] - r0["mean_c"], 4)
    d3 = round(r3["mean_c"] - r0["mean_c"], 4)
    print(f"\n  Δ HIGH vs none:      {d1:+.4f}")
    print(f"  Δ H+M  vs none:      {d2:+.4f}")
    print(f"  Δ ALL  vs none:      {d3:+.4f}")

    # Phase-192 new entry SA confirmation
    p192 = {k.lstrip("M"): k for k, v in anchors_raw.items()
            if isinstance(v, dict) and v.get("_phase192_absent_phoneme")}
    print("\n=== Phase-192 Absent-Phoneme Entry SA Check ===")
    p192_results = []
    modal_all = r3["modal"]
    conss_all  = r3["consistency"]
    for m77_id, anchor_id in p192.items():
        expected = anchors_raw[anchor_id].get("reading", "")
        sa_read  = modal_all.get(m77_id, "")
        sa_cons  = conss_all.get(m77_id, 0.0)
        agrees   = expected.lower() in sa_read.lower() if sa_read else False
        print(f"  {anchor_id} ({m77_id}): expected=/{expected}/ SA={sa_read} cons={sa_cons:.3f} {'✓' if agrees else '✗'}")
        p192_results.append({"sign": anchor_id, "expected": expected,
                              "sa_reading": sa_read, "sa_cons": sa_cons, "agrees": agrees})

    # Top unanchored signs in ALL-anchor SA run (potential upgrades)
    anch_set = set(anch_low.keys())
    unanchored_conss = {s: c for s, c in conss_all.items() if s not in anch_set}
    top_unanch = sorted(unanchored_conss.items(), key=lambda x: -x[1])[:15]
    print("\n=== Top Unanchored Signs by SA Consistency (ALL run) ===")
    for sign, c in top_unanch:
        reading = modal_all.get(sign, "")
        f = freq.get(sign, 0)
        print(f"  {sign}: modal={reading} cons={c:.3f} freq={f}")

    # Estimate aggregate confidence
    # weighted by token coverage
    total_tokens = sum(freq.values())
    anch_tokens  = sum(freq.get(s, 0) for s in anch_set)
    unanch_tokens = total_tokens - anch_tokens
    # Anchored token confidence = mean_c of anchored signs
    anch_conss = {s: c for s, c in conss_all.items() if s in anch_set}
    anch_mean  = sum(anch_conss.values()) / len(anch_conss) if anch_conss else 0
    # Combined aggregate
    agg = round((anch_tokens * anch_mean + unanch_tokens * r0["mean_c"]) / total_tokens, 4)
    print(f"\n=== Aggregate Confidence Estimate ===")
    print(f"  Anchored tokens ({anch_tokens}/{total_tokens} = {anch_tokens/total_tokens*100:.1f}%): mean_c={anch_mean:.4f}")
    print(f"  Unanchored tokens: mean_c={r0['mean_c']:.4f}")
    print(f"  Weighted aggregate: {agg:.4f} ({agg*100:.1f}%)")

    elapsed = round(time.time() - t0, 1)
    result = {
        "phase": 193,
        "elapsed_s": elapsed,
        "sa_no_anchors":    {"mean_c": r0["mean_c"], "hci": r0["hci"]},
        "sa_high_only":     {"mean_c": r1["mean_c"], "hci": r1["hci"], "delta": d1},
        "sa_high_medium":   {"mean_c": r2["mean_c"], "hci": r2["hci"], "delta": d2},
        "sa_all_anchors":   {"mean_c": r3["mean_c"], "hci": r3["hci"], "delta": d3},
        "p192_checks":      p192_results,
        "top_unanchored_by_consistency": [{"sign": s, "modal": modal_all.get(s,""), "consistency": c, "freq": freq.get(s,0)} for s,c in top_unanch],
        "aggregate_confidence": agg,
        "anchor_counts": {"high": len(anch_high), "high_medium": len(anch_medium), "all": len(anch_low)},
    }

    print(f"\nPhase 193 complete in {elapsed}s")
    print(f"Aggregate confidence: {agg:.4f} ({agg*100:.1f}%)")

    out = OUTPUTS / "phase193_sa_rerun_402anchors.json"
    out.write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")
    (REPORTS / "phase193_sa_rerun_402anchors.json").write_text(
        json.dumps(result, indent=2, default=str), encoding="utf-8")
    print(f"Saved: {out}")


if __name__ == "__main__":
    main()
