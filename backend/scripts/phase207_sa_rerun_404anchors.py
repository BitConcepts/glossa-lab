"""Phase 207 — SA Rerun with 404-Anchor Set
         Compare delta improvement vs Phase 193 baseline (50.3%)

Phase 193 ran SA with 402 anchors and reported aggregate confidence 50.3%.
Phase 206 added M692=nal (MEDIUM) and M861=nallavar (LOW) => 404 anchors.

This phase reruns the exact same SA protocol (4 conditions x 5 seeds each)
with the updated anchor set and reports:
  - Per-condition consistency (no anchors / HIGH only / HIGH+MEDIUM / ALL)
  - Delta vs Phase 193 for each condition
  - New unanchored top-15 by consistency (candidates for Phase 209+)
  - Whether M692 and M861 are SA-confirmed in the ALL-anchor condition
  - Updated aggregate confidence estimate
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

P193_AGGREGATE = 0.503


def build_anchor_dict(anchors_raw, freq, min_conf="HIGH"):
    tier_order = {"HIGH": 3, "MEDIUM": 2, "LOW": 1, "CANDIDATE": 0}
    min_tier = tier_order.get(min_conf, 0)
    out = {}
    for anchor_id, rec in anchors_raw.items():
        if not isinstance(rec, dict):
            continue
        conf = rec.get("confidence", "")
        if tier_order.get(conf, 0) < min_tier:
            continue
        m77_id = anchor_id.lstrip("M")
        reading = rec.get("reading", "").split("/")[0].strip()
        if m77_id in freq and reading:
            out[m77_id] = reading
    return out


def run_sa(inscs, anchors, label, n_seeds=5):
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
    modal = {}
    conss = {}
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
    print("Phase 207 - SA Rerun with 404-Anchor Set (vs P193 baseline)")
    print("=" * 60)

    from glossa_lab.data.indus_m77 import get_corpus_symbols, get_corpus_inscriptions
    syms  = get_corpus_symbols()
    inscs = get_corpus_inscriptions()
    freq  = Counter(syms)
    anchors_raw = json.loads(ANCHOR_F.read_text())["anchors"]

    print(f"\nM77: {len(freq)} distinct signs, {len(syms)} tokens, {len(inscs)} inscriptions")

    anch_high   = build_anchor_dict(anchors_raw, freq, "HIGH")
    anch_medium = build_anchor_dict(anchors_raw, freq, "MEDIUM")
    anch_low    = build_anchor_dict(anchors_raw, freq, "LOW")

    print(f"  Anchors HIGH:          {len(anch_high)}")
    print(f"  Anchors HIGH+MEDIUM:   {len(anch_medium)}")
    print(f"  Anchors ALL (incl LOW): {len(anch_low)}")
    print(f"  M692 in HIGH+MEDIUM: {'692' in anch_medium}")
    print(f"  M861 in ALL:         {'861' in anch_low}")

    print("\n=== SA Runs ===")
    r0 = run_sa(inscs, {},          "A_no_anchors")
    r1 = run_sa(inscs, anch_high,   "B_HIGH_only")
    r2 = run_sa(inscs, anch_medium, "C_HIGH+MEDIUM")
    r3 = run_sa(inscs, anch_low,    "D_ALL_anchors")

    d1 = round(r1["mean_c"] - r0["mean_c"], 4)
    d2 = round(r2["mean_c"] - r0["mean_c"], 4)
    d3 = round(r3["mean_c"] - r0["mean_c"], 4)
    print(f"\n  Delta HIGH vs none:  {d1:+.4f}")
    print(f"  Delta H+M  vs none:  {d2:+.4f}")
    print(f"  Delta ALL  vs none:  {d3:+.4f}")

    modal_all = r3["modal"]
    conss_all  = r3["consistency"]
    new_checks = []
    for m77_id, anchor_id in [("692", "M692"), ("861", "M861")]:
        expected = anchors_raw.get(anchor_id, {}).get("reading", "")
        sa_read  = modal_all.get(m77_id, "")
        sa_cons  = conss_all.get(m77_id, 0.0)
        agrees   = expected.split("/")[0].lower() in sa_read.lower() if sa_read else False
        mark = "Y" if agrees else "N"
        print(f"  {anchor_id} ({m77_id}): expected=/{expected}/ SA={sa_read} cons={sa_cons:.3f} [{mark}]")
        new_checks.append({"sign": anchor_id, "expected": expected,
                           "sa_reading": sa_read, "sa_cons": sa_cons, "agrees": agrees})

    anch_set = set(anch_low.keys())
    unanchored_conss = {s: c for s, c in conss_all.items() if s not in anch_set}
    top_unanch = sorted(unanchored_conss.items(), key=lambda x: -x[1])[:15]
    print("\n=== Top Unanchored Signs by SA Consistency (ALL run) ===")
    for sign, c in top_unanch:
        reading = modal_all.get(sign, "")
        f = freq.get(sign, 0)
        print(f"  {sign}: modal={reading} cons={c:.3f} freq={f}")

    total_tokens = sum(freq.values())
    anch_tokens  = sum(freq.get(s, 0) for s in anch_set)
    unanch_tokens = total_tokens - anch_tokens
    anch_conss = {s: c for s, c in conss_all.items() if s in anch_set}
    anch_mean  = sum(anch_conss.values()) / len(anch_conss) if anch_conss else 0
    agg = round((anch_tokens * anch_mean + unanch_tokens * r0["mean_c"]) / total_tokens, 4)
    delta_p193 = round(agg - P193_AGGREGATE, 4)

    print(f"\n=== Aggregate Confidence ===")
    print(f"  Phase 193 baseline: {P193_AGGREGATE:.4f} ({P193_AGGREGATE*100:.1f}%)")
    print(f"  Phase 207 result:   {agg:.4f} ({agg*100:.1f}%)")
    print(f"  Delta vs P193:      {delta_p193:+.4f} ({delta_p193*100:+.2f}pp)")

    elapsed = round(time.time() - t0, 1)
    m692_ok = new_checks[0]["agrees"] if new_checks else False
    m861_ok = new_checks[1]["agrees"] if len(new_checks) > 1 else False
    result = {
        "phase": 207,
        "elapsed_s": elapsed,
        "phase193_baseline": P193_AGGREGATE,
        "sa_no_anchors":  {"mean_c": r0["mean_c"], "hci": r0["hci"]},
        "sa_high_only":   {"mean_c": r1["mean_c"], "hci": r1["hci"], "delta": d1},
        "sa_high_medium": {"mean_c": r2["mean_c"], "hci": r2["hci"], "delta": d2},
        "sa_all_anchors": {"mean_c": r3["mean_c"], "hci": r3["hci"], "delta": d3},
        "new_anchor_checks": new_checks,
        "top_unanchored_by_consistency": [
            {"sign": s, "modal": modal_all.get(s,""), "consistency": c, "freq": freq.get(s,0)}
            for s, c in top_unanch
        ],
        "aggregate_confidence": agg,
        "delta_vs_p193": delta_p193,
        "anchor_counts": {"high": len(anch_high), "high_medium": len(anch_medium), "all": len(anch_low)},
        "verdict": (
            f"Phase 207 (404 anchors): aggregate={agg:.4f} ({agg*100:.1f}%). "
            f"Delta vs Phase 193 ({P193_AGGREGATE*100:.1f}%): {delta_p193:+.4f} ({delta_p193*100:+.2f}pp). "
            f"M692 SA-confirmed: {m692_ok}. M861 SA-confirmed: {m861_ok}."
        ),
    }

    out = OUTPUTS / "phase207_sa_rerun_404anchors.json"
    out.write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")
    (REPORTS / "phase207_sa_rerun_404anchors.json").write_text(
        json.dumps(result, indent=2, default=str), encoding="utf-8")
    print(f"\nPhase 207 complete in {elapsed}s | Saved: {out}")
    print(f"Verdict: {result['verdict']}")


if __name__ == "__main__":
    main()
