"""Phase-77: SA Agreement Rate Analysis.

Analyses the Phase-63 filtered SA decipherment table to understand:
  1. Which HIGH/MEDIUM anchor signs does SA consistently agree with?
     (Agreement = SA modal reading matches confirmed reading at first 2 chars)
  2. Which HIGH/MEDIUM signs does SA consistently get wrong?
  3. For unanchored signs, which SA proposals appear consistently across seeds
     (high consensus_pct) AND have plausible phonotactics?
     → These are "high-trust proposals" worth investigating for promotion

GPU: uses torch for statistical computation.
Output: reports/phase77_sa_agreement_analysis.json
"""
from __future__ import annotations
import json, sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))
from glossa_lab.gpu_utils import detect_device as _detect_device  # noqa: E402

try:
    import torch
except ImportError:
    torch = None

DEVICE = _detect_device()
if DEVICE == "cuda" and torch is not None:
    print(f"[GPU] torch {torch.__version__} — device: cuda")

REPO    = Path(__file__).parents[2]
P63     = REPO / "reports/phase63_filtered_decipherment_table.json"
P57     = REPO / "reports/phase57_decipherment_table.json"
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
REPORTS = REPO / "reports"
REPORTS.mkdir(exist_ok=True)
OUT     = REPORTS / "phase77_sa_agreement_analysis.json"

PD_INVALID_INITIAL = set("bdfgqwx")

def is_pd_valid(reading: str) -> bool:
    r = reading.lower().strip()
    if not r: return False
    return r[0] not in PD_INVALID_INITIAL


def main():
    print("Phase-77: SA Agreement Rate Analysis\n")

    anchors = json.loads(ANCHORS.read_text("utf-8"))["anchors"]

    # Load filtered SA table (Phase-63 is preferred; fall back to Phase-57)
    table_path = P63 if P63.exists() else P57
    if not table_path.exists():
        print("ERROR: No SA decipherment table found")
        result = {"error": "no SA table", "overall_agreement_pct": 0, "high_trust_proposals": []}
        OUT.write_text(json.dumps(result, indent=2), "utf-8")
        return

    table = json.loads(table_path.read_text("utf-8"))
    print(f"  SA table: {table_path.name} ({len(table)} signs)")

    # Separate confirmed vs unanchored signs
    confirmed = [e for e in table if e.get("confirmed_confidence") in ("HIGH", "MEDIUM")]
    unanchored = [e for e in table if e.get("confirmed_confidence") not in ("HIGH", "MEDIUM", "LOW")]

    print(f"  Confirmed HIGH/MEDIUM signs: {len(confirmed)}")
    print(f"  Unanchored signs:           {len(unanchored)}")

    # Agreement analysis for confirmed signs
    # Agreement: SA modal reading[:2] == confirmed reading[:2]
    agree_signs  = []
    disagree_signs = []

    for entry in confirmed:
        sa_reading  = (entry.get("sa_reading") or "")[:2].lower()
        conf_reading = (entry.get("confirmed_reading") or "")[:2].lower()
        sa_pct = entry.get("sa_consensus_pct", 0)

        if sa_reading and conf_reading:
            agrees = sa_reading == conf_reading
            record = {
                "sign":             entry["sign"],
                "n_corpus":         entry.get("n_corpus", 0),
                "sa_reading":       entry.get("sa_reading",""),
                "sa_consensus_pct": sa_pct,
                "confirmed_reading":entry.get("confirmed_reading",""),
                "confirmed_conf":   entry.get("confirmed_confidence","?"),
                "agrees":           agrees,
            }
            if agrees:
                agree_signs.append(record)
            else:
                disagree_signs.append(record)

    agree_rate = len(agree_signs) / max(len(confirmed), 1) * 100
    print(f"\n  Agreement rate: {len(agree_signs)}/{len(confirmed)} = {agree_rate:.1f}%")

    # GPU: compute weighted agreement by corpus frequency
    if torch is not None and DEVICE == "cuda":
        all_signs = agree_signs + disagree_signs
        if all_signs:
            freqs  = torch.tensor([s["n_corpus"] for s in all_signs], dtype=torch.float, device=DEVICE)
            agrees = torch.tensor([1.0 if s["agrees"] else 0.0 for s in all_signs], device=DEVICE)
            weighted_agree_rate = float((agrees * freqs).sum() / freqs.sum().clamp(min=1)) * 100
            print(f"  Weighted agreement rate: {weighted_agree_rate:.1f}% (by corpus frequency)")
        else:
            weighted_agree_rate = agree_rate
        print(f"[GPU:{DEVICE}] Computed weighted agreement statistics")
    else:
        weighted_agree_rate = agree_rate

    # High-trust proposals from unanchored signs
    # Criteria: consensus_pct >= 0.6, phonotactically valid, not already anchored
    high_trust = []
    for entry in unanchored:
        sa_reading  = entry.get("sa_reading", "")
        consensus   = entry.get("sa_consensus_pct", 0)
        n_corpus    = entry.get("n_corpus", 0)

        if (consensus >= 0.6 and
                is_pd_valid(sa_reading) and
                len(sa_reading) >= 2 and
                n_corpus >= 10):
            high_trust.append({
                "sign":         entry["sign"],
                "n_corpus":     n_corpus,
                "sa_reading":   sa_reading,
                "consensus_pct":consensus,
                "pd_valid":     True,
                "priority":     round(consensus * n_corpus / 100, 2),
            })

    # Sort by priority (consensus * frequency)
    high_trust.sort(key=lambda x: -x["priority"])

    print(f"\n  High-trust SA proposals (consensus>=60%, PD-valid, freq>=10):")
    for p in high_trust[:15]:
        print(f"  {p['sign']:6s} sa={p['sa_reading']:8s} consensus={p['consensus_pct']:.0%} freq={p['n_corpus']}")

    # Disagreement pattern
    print(f"\n  Signs where SA consistently disagrees with confirmed:")
    disagree_signs.sort(key=lambda x: -(x["n_corpus"] * x["sa_consensus_pct"]))
    for d in disagree_signs[:8]:
        print(f"  {d['sign']:6s} sa={d['sa_reading'][:8]:8s} vs confirmed={d['confirmed_reading'][:8]:8s} "
              f"(consensus={d['sa_consensus_pct']:.0%})")

    print(f"\n=== Phase-77 Results ===")
    print(f"  Overall SA agreement:   {agree_rate:.1f}%")
    print(f"  Weighted agreement:     {weighted_agree_rate:.1f}%")
    print(f"  High-trust proposals:   {len(high_trust)}")
    print(f"  Disagree signs:         {len(disagree_signs)}")
    print(f"\n  Key insight: SA agrees with confirmed readings {agree_rate:.0f}% of the time.")
    print(f"  Signs where SA disagrees may indicate:")
    print(f"    - Sign is multi-syllabic (like M267 — SA assigns single syllable)")
    print(f"    - Sign has a reading that's rare in the syllabic LM")
    print(f"    - Classifier signs (appear initial, SA doesn't know they're classifiers)")

    result = {
        "_citation": {"primary": ["A.1"]},
        "gpu_device": DEVICE,
        "n_confirmed_tested":      len(confirmed),
        "n_agree":                 len(agree_signs),
        "n_disagree":              len(disagree_signs),
        "overall_agreement_pct":   round(agree_rate, 1),
        "weighted_agreement_pct":  round(weighted_agree_rate, 1),
        "n_high_trust_proposals":  len(high_trust),
        "high_trust_proposals":    high_trust[:30],
        "disagree_signs":          disagree_signs[:20],
        "agree_signs":             agree_signs[:20],
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), "utf-8")
    print(f"\nReport: {OUT}")


if __name__ == "__main__":
    main()
