"""Quick summary of Phase-30a sub-test outputs."""
from __future__ import annotations
import json
import sys
from pathlib import Path

ts = sys.argv[1] if len(sys.argv) > 1 else "20260501T114235"
ROOT = Path(__file__).resolve().parents[2]
REPORTS = ROOT / "reports"
files = ["p30_a1", "p30_a2", "p30_a3", "p30_a4", "p30_a5", "p30_a6",
         "p30_a7", "p30_a8", "p30_e7", "p30_g1", "p30_g8", "p30_g9"]

keep = [
    "p_value_one_sided", "rank_percentile", "rendering_set_size",
    "n_chronologically_compatible", "n_with_meluhha_cooccurrence",
    "n_meluhha_tablets_searched", "ci", "n_significant_after_bh",
    "cohens_d", "rate_delta", "ur3", "old_babylonian",
    "observed_anchor_score", "null_p95", "null_max",
    "observed_h1_phoneme", "null_h1_p95",
    "held_out_ppl_mean", "janabiyah_ppl_mean",
    "ppl_ratio_janabiyah_to_heldout",
    "n_distinct_cells_observed", "n_pns_with_any_cell_observation",
    "variants",
]

for f in files:
    p = REPORTS / f"indus_phase30a_{f}_{ts}.json"
    if not p.exists():
        print(f"MISSING: {p.name}")
        continue
    d = json.loads(p.read_text(encoding="utf-8"))
    print(f"=== {d.get('test_id', f)}: {d.get('test_name', '?')} ===")
    print(d.get("verdict", "(no verdict)"))
    for k in keep:
        if k in d:
            v = d[k]
            if isinstance(v, list) and len(v) > 5:
                print(f"  {k} = [{len(v)} items]")
            else:
                print(f"  {k} = {v}")
    print()
