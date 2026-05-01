"""Summarize Phase-30c results."""
from __future__ import annotations
import json
import sys
from pathlib import Path

ts = sys.argv[1] if len(sys.argv) > 1 else "20260501T130625"
ROOT = Path(__file__).resolve().parents[2]
REP = ROOT / "reports"

# T1.1-v3
d = json.loads((REP / f"indus_phase30c_t1_1_v3_whole_rendering_{ts}.json").read_text(encoding="utf-8"))
print("=== T1.1-v3 Whole-rendering matcher ===")
print(f"Position-matched: {d['n_position_matched']}, Enmenanak={d['enmenanak_score']}, A1 p={d['a1_p_value']}")
print("Top 10:")
for r in d["top_10_scores"]:
    print(f"  {r['headword']:30s} score={r['score']:5.2f}  form={r['best_form']:30s} pos={r['position_match']} free={r['free_miin']} icount={r['icount']:4d} periods={r['periods']}")
print()

# T1.2-v3
d = json.loads((REP / f"indus_phase30c_t1_2_v3_tiered_meluhha_{ts}.json").read_text(encoding="utf-8"))
print("=== T1.2-v3 Tiered Meluhha ===")
print(f"tier_a (3-seg contig)={d['n_tier_a_3seg_contiguous']}, tier_b (2-seg contig)={d['n_tier_b_2seg_contiguous']}, tier_c (bag 70%)={d['n_tier_c_bag_70pct']}")
print("Top 10 by total hits:")
for r in d["top_results"][:10]:
    print(f"  {r['headword']:30s} form={r['best_form']:25s} a={r['tier_a_3seg_hits']:3d} b={r['tier_b_2seg_hits']:3d} c={r['tier_c_bag_hits']:4d} icount={r['icount']:4d} periods={r['periods']}")
print()

# T3-v2
d = json.loads((REP / f"indus_phase30c_t3_v2_four_way_falsification_{ts}.json").read_text(encoding="utf-8"))
print("=== T3-v2 4-way falsification ===")
for r in d["ranked"]:
    print(f"  {r['map']:35s} observed={r['observed']:5.1f}  p={r['p_value']:.4f}  null_max={r['null_max']:5.1f}")
print(f"Leader: {d['leader']} (score {d['leader_score']}, gap {d['gap_first_to_second']})")
