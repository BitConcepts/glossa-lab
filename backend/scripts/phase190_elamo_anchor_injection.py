"""Phase 190 — Elamo-Dravidian Anchor Injection

Takes the 14 absent phonemes with Elamite support (Phase 186) and the
North Dravidian LM proposals (Phase 189), then:

  1. Fixes the M77 vs anchor ID mismatch ("047" vs "M047")
  2. Identifies truly unanchored M77 signs with North Dravidian proposals
     for absent phonemes
  3. Cross-validates each proposal with Elamite tier (Phase 186)
  4. Runs SA convergence under 3 conditions:
       A: Baseline — existing HIGH anchors only (using M77 IDs)
       B: + Elamite LOW candidates (absent phonemes from McAlpin)
       C: + Combined (Elamite + North Dravidian convergent)
  5. Reports per-condition consistency and ranks proposals by SA stability

This is the bridge from literature evidence → computational validation.
"""
from __future__ import annotations
import json
from pathlib import Path
from collections import Counter
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
OUTPUTS   = REPO_ROOT / "outputs"
REPORTS   = REPO_ROOT / "research" / "indus" / "phase_reports"
ANCHOR_F  = REPO_ROOT / "backend" / "reports" / "INDUS_FINAL_ANCHORS.json"
sys.path.insert(0, str(REPO_ROOT / "backend"))
OUTPUTS.mkdir(exist_ok=True)
REPORTS.mkdir(parents=True, exist_ok=True)

ABSENT_PHONEMES = [
    "su","li","shu","gu","ab","ba","du","zi","ga","mil","gi","en","ki","sum"
]

# ── Elamite evidence tier (from Phase 186) ───────────────────────────────────
ELAMITE_TIER = {
    "en":  "STRONG",   "ki":  "STRONG",  "du": "STRONG",
    "ga":  "STRONG",   "sum": "STRONG",
    "ab":  "MODERATE", "ba":  "MODERATE","zi": "MODERATE",
    "mil": "MODERATE", "gi":  "MODERATE","su": "MODERATE",
    "li":  "MODERATE", "gu":  "MODERATE","shu":"CANDIDATE",
}


def _m77_id_to_anchor_id(m77_id: str) -> str:
    """M77 uses "047" format; anchor set uses "M047" format."""
    return f"M{m77_id}"


def load_data():
    from glossa_lab.data.indus_m77 import get_corpus_inscriptions, get_corpus_symbols
    inscs = get_corpus_symbols()  # flat symbol list
    inscriptions = get_corpus_inscriptions()
    freq = Counter(inscs)
    anchors_raw = json.loads(ANCHOR_F.read_text())["anchors"]
    return inscriptions, freq, anchors_raw


def get_truly_unanchored(freq: Counter, anchors_raw: dict) -> set[str]:
    """Return M77 sign IDs that have no anchor entry (using M-prefix map)."""
    unanchored = set()
    for m77_id in freq:
        anchor_id = _m77_id_to_anchor_id(m77_id)
        if anchor_id not in anchors_raw:
            unanchored.add(m77_id)
    return unanchored


def load_phase189_proposals(unanchored: set[str]) -> list[dict]:
    """Load Phase 189 proposals, filter to truly unanchored signs + absent phonemes."""
    p189_path = OUTPUTS / "phase189_northern_dravidian_lm.json"
    if not p189_path.exists():
        print("  Phase 189 output not found — run phase189 first")
        return []
    data = json.loads(p189_path.read_text())
    novel = data.get("novel_north_proposals", [])
    valid = []
    for p in novel:
        sign = p["sign"]
        phoneme = p.get("north_dr_proposal", "")
        if sign not in unanchored:
            continue  # skip signs that ARE anchored (after fixing ID mapping)
        if not any(ap in phoneme.lower() for ap in ABSENT_PHONEMES):
            continue  # skip non-absent phonemes
        # Extract just the absent phoneme root
        absent_match = next((ap for ap in ABSENT_PHONEMES if ap in phoneme.lower()), None)
        if not absent_match:
            continue
        valid.append({
            "m77_sign_id":  sign,
            "anchor_sign_id": _m77_id_to_anchor_id(sign),
            "proposed_phoneme": absent_match,
            "north_dr_reading": phoneme,
            "elamite_tier": ELAMITE_TIER.get(absent_match, "UNKNOWN"),
        })
    return valid


def score_proposals(proposals: list[dict], freq: Counter,
                    inscriptions: list) -> list[dict]:
    """Score each proposal by Elamite tier + corpus frequency + position."""
    from collections import Counter as C
    for p in proposals:
        m77_id = p["m77_sign_id"]
        f = freq.get(m77_id, 0)
        # Positional analysis
        pos = C()
        for insc in inscriptions:
            for i, s in enumerate(insc):
                if s == m77_id:
                    if i == 0:             pos["INITIAL"] += 1
                    elif i == len(insc)-1: pos["TERMINAL"] += 1
                    else:                  pos["MEDIAL"] += 1
        total = sum(pos.values()) or 1
        t_rate = round(pos.get("TERMINAL", 0) / total, 3)
        i_rate = round(pos.get("INITIAL",  0) / total, 3)
        m_rate = round(pos.get("MEDIAL",   0) / total, 3)

        # Score tiers
        elamite_score = {"STRONG": 3, "MODERATE": 2, "CANDIDATE": 1}.get(
            p["elamite_tier"], 0)
        pos_score = 1.0 - abs(t_rate - 0.33)  # penalise pure terminal (likely suffix)
        freq_score = min(1.0, f / 200)         # normalise by 200

        total_score = round(elamite_score * 0.5 + pos_score * 0.3 + freq_score * 0.2, 3)
        p.update({
            "corpus_freq": f,
            "t_rate": t_rate, "i_rate": i_rate, "m_rate": m_rate,
            "elamite_score": elamite_score,
            "position_score": round(pos_score, 3),
            "total_score": total_score,
        })
    proposals.sort(key=lambda x: -x["total_score"])
    return proposals


def build_anchor_dicts(proposals: list[dict], anchors_raw: dict,
                       freq: Counter) -> tuple[dict, dict, dict]:
    """Build three anchor dicts (A/B/C) in M77 sign ID format (without M prefix)."""
    # Condition A: existing HIGH anchors (ID remapped to M77 format)
    cond_a: dict[str, str] = {}
    for anchor_id, rec in anchors_raw.items():
        if not isinstance(rec, dict):
            continue
        if rec.get("confidence") != "HIGH":
            continue
        # Strip M prefix to get M77 format
        m77_id = anchor_id.lstrip("M")
        if m77_id in freq:  # only include signs that appear in M77
            reading = rec.get("reading", "").split("/")[0]
            if reading:
                cond_a[m77_id] = reading

    # Condition B: A + top Elamite STRONG/MODERATE proposals (one per phoneme)
    cond_b: dict[str, str] = dict(cond_a)
    seen_phonemes: set[str] = set()
    for p in proposals:
        ph = p["proposed_phoneme"]
        if ph in seen_phonemes:
            continue
        if p["elamite_tier"] in ("STRONG", "MODERATE"):
            cond_b[p["m77_sign_id"]] = ph
            seen_phonemes.add(ph)

    # Condition C: A + ALL proposals (best per phoneme regardless of tier)
    cond_c: dict[str, str] = dict(cond_a)
    seen_phonemes_c: set[str] = set()
    for p in proposals:
        ph = p["proposed_phoneme"]
        if ph in seen_phonemes_c:
            continue
        cond_c[p["m77_sign_id"]] = ph
        seen_phonemes_c.add(ph)

    return cond_a, cond_b, cond_c


def run_sa(inscriptions, anchor_dict: dict, label: str,
           n_seeds: int = 5, max_iter: int = 4000) -> dict:
    """Run SA with given anchors, return consistency stats."""
    try:
        from glossa_lab.pipelines.decipher import decipher, LanguageModel
        from glossa_lab.data.dravidian import get_word_symbols
        lm   = LanguageModel(get_word_symbols())
        flat = [s for insc in inscriptions for s in insc]

        from concurrent.futures import ThreadPoolExecutor
        def _run(seed):
            r = decipher(flat, lm, seed=seed, max_iterations=max_iter, restarts=4,
                         cipher_inscriptions=None, ocp_weight=0.0, positional_weight=0.0,
                         surjective=True, anchors=anchor_dict or None)
            return r.get("proposed_mapping", {})

        with ThreadPoolExecutor(max_workers=n_seeds) as ex:
            maps = list(ex.map(_run, range(n_seeds)))

        from collections import Counter as C
        all_signs = set().union(*[m.keys() for m in maps])
        modal: dict[str, str] = {}
        conss: dict[str, float] = {}
        for s in all_signs:
            props = [m[s] for m in maps if s in m]
            if props:
                mc_item, mc_count = C(props).most_common(1)[0]
                modal[s] = mc_item
                conss[s] = mc_count / len(props)

        mean_c = round(sum(conss.values()) / len(conss), 4) if conss else 0.0
        hci    = sum(1 for v in conss.values() if v >= 0.75)
        print(f"  SA [{label}]: mean_c={mean_c:.4f} hci={hci} n_signs={len(modal)}")
        return {"label": label, "mean_consistency": mean_c, "hci_count": hci,
                "modal_mapping": modal, "consistency_per_sign": conss,
                "n_seeds": n_seeds, "n_signs": len(modal)}
    except Exception as exc:
        print(f"  SA [{label}] failed: {exc}")
        return {"label": label, "mean_consistency": 0.0, "error": str(exc)}


def check_proposal_sa_consistency(proposals: list[dict],
                                   sa_combined: dict) -> list[dict]:
    """Check whether the SA run under combined anchors assigns the proposed phoneme."""
    modal = sa_combined.get("modal_mapping", {})
    conss = sa_combined.get("consistency_per_sign", {})
    for p in proposals:
        m77_id = p["m77_sign_id"]
        sa_reading = modal.get(m77_id, "")
        sa_cons    = conss.get(m77_id, 0.0)
        proposed   = p["proposed_phoneme"]
        # Did SA agree with the proposed phoneme?
        sa_agrees  = proposed in sa_reading.lower() if sa_reading else False
        p.update({
            "sa_reading": sa_reading,
            "sa_consistency": round(sa_cons, 3),
            "sa_agrees": sa_agrees,
        })
    return proposals


def main():
    import time
    t0 = time.time()
    print("=" * 60)
    print("Phase 190 — Elamo-Dravidian Anchor Injection")
    print("=" * 60)

    inscriptions, freq, anchors_raw = load_data()
    unanchored = get_truly_unanchored(freq, anchors_raw)
    print(f"\nM77: {len(freq)} distinct signs, {sum(freq.values())} tokens")
    print(f"Truly unanchored in M77: {len(unanchored)} signs")

    # Load and filter Phase 189 proposals
    proposals = load_phase189_proposals(unanchored)
    print(f"Phase 189 proposals for absent phonemes (unanchored only): {len(proposals)}")

    if not proposals:
        print("No valid proposals found — check Phase 189 output")
        return

    # Score proposals
    proposals = score_proposals(proposals, freq, inscriptions)

    print("\n=== Scored Proposals ===")
    for p in proposals[:20]:
        print(f"  {p['m77_sign_id']} → /{p['proposed_phoneme']}/ "
              f"[Elamite:{p['elamite_tier']}] "
              f"freq={p['corpus_freq']} t={p['t_rate']} i={p['i_rate']} "
              f"score={p['total_score']:.3f}")

    # Build anchor dicts
    cond_a, cond_b, cond_c = build_anchor_dicts(proposals, anchors_raw, freq)
    print(f"\nCondition A (HIGH baseline): {len(cond_a)} anchors")
    print(f"Condition B (+ Elamite):      {len(cond_b)} anchors (+{len(cond_b)-len(cond_a)})")
    print(f"Condition C (+ combined):     {len(cond_c)} anchors (+{len(cond_c)-len(cond_a)})")

    # Run SA
    print("\n=== SA Convergence Test ===")
    result_a = run_sa(inscriptions, cond_a, "A_baseline_HIGH")
    result_b = run_sa(inscriptions, cond_b, "B_plus_elamite")
    result_c = run_sa(inscriptions, cond_c, "C_plus_combined")

    delta_b = round(result_b["mean_consistency"] - result_a["mean_consistency"], 4)
    delta_c = round(result_c["mean_consistency"] - result_a["mean_consistency"], 4)
    print(f"\n  Delta B (Elamite): {delta_b:+.4f}")
    print(f"  Delta C (combined): {delta_c:+.4f}")

    # Check per-proposal SA agreement
    proposals = check_proposal_sa_consistency(proposals, result_c)
    sa_confirmed = [p for p in proposals if p.get("sa_agrees")]
    print(f"\n  SA agrees with {len(sa_confirmed)}/{len(proposals)} proposals")
    for p in sa_confirmed[:10]:
        print(f"    {p['m77_sign_id']} → /{p['proposed_phoneme']}/ "
              f"SA={p['sa_reading']} cons={p['sa_consistency']:.3f} "
              f"Elamite={p['elamite_tier']}")

    elapsed = round(time.time() - t0, 1)
    result = {
        "phase":        190,
        "elapsed_s":    elapsed,
        "n_unanchored": len(unanchored),
        "proposals":    proposals,
        "sa_a":         {k: v for k, v in result_a.items() if k != "modal_mapping"},
        "sa_b":         {k: v for k, v in result_b.items() if k != "modal_mapping"},
        "sa_c":         {k: v for k, v in result_c.items() if k != "modal_mapping"},
        "delta_b_vs_a": delta_b,
        "delta_c_vs_a": delta_c,
        "sa_confirmed_proposals": sa_confirmed,
        "n_sa_confirmed": len(sa_confirmed),
        "verdict": (
            f"ELAMITE ANCHORS IMPROVE CONVERGENCE: delta_b={delta_b:+.4f}, "
            f"{len(sa_confirmed)} proposals SA-confirmed"
            if delta_b > 0.001
            else f"NEUTRAL/NEGATIVE: delta_b={delta_b:+.4f}"
        ),
    }

    print(f"\nPhase 190 complete in {elapsed}s")
    print(f"Verdict: {result['verdict']}")

    out = OUTPUTS / "phase190_elamo_anchor_injection.json"
    out.write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")
    (REPORTS / "phase190_elamo_anchor_injection.json").write_text(
        json.dumps(result, indent=2, default=str), encoding="utf-8")
    print(f"Saved: {out}")


if __name__ == "__main__":
    main()
