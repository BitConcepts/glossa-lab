"""Read and print the latest fuls_rtl_corrected results."""
import json, sys, glob, os
from pathlib import Path

REPORTS = Path(__file__).resolve().parent.parent.parent / "reports"
files = sorted(glob.glob(str(REPORTS / "fuls_rtl_corrected*.json")), reverse=True)
if not files:
    print("No results found."); sys.exit(1)

data = json.loads(Path(files[0]).read_text("utf-8"))
print(f"File: {Path(files[0]).name}")
print()

# Ashraf directional analysis
ashraf = data.get("ashraf_directional_analysis", {})
print("=== ASHRAF DIRECTIONAL ANALYSIS ===")
print(f"  H(pos-0, leftmost):  {ashraf.get('entropy_position_0_leftmost',0):.4f} bits")
print(f"  H(pos-N1, rightmost): {ashraf.get('entropy_position_N1_rightmost',0):.4f} bits")
print(f"  Inferred direction:  {ashraf.get('inferred_direction','?')}")
print(f"  Confirms RTL:        {ashraf.get('confirms_rtl','?')}")
print()

# Condition A
cond_a = data.get("condition_a_no_anchors_rtl", {})
print("=== CONDITION A — No anchors, RTL corrected ===")
print(f"  N seeds:             {cond_a.get('n_seeds','?')}")
print(f"  Mean consistency:    {cond_a.get('mean_consistency',0):.1%}")
print(f"  HCI (>=75%):         {cond_a.get('hci_count','?')}/78")
print(f"  Bigram plausibility: {cond_a.get('bigram_plausibility',0):.4f}")
print()

# Condition B
cond_b = data.get("condition_b_fuls_anchors_rtl", {})
print("=== CONDITION B — Dr. Fuls' verified anchors ===")
print(f"  Anchors used:        {list(cond_b.get('anchors_used',{}).items())}")
print(f"  N seeds:             {cond_b.get('n_seeds','?')}")
print(f"  Mean consistency:    {cond_b.get('mean_consistency',0):.1%}")
print(f"  HCI (>=75%):         {cond_b.get('hci_count','?')}/78")
print(f"  Bigram plausibility: {cond_b.get('bigram_plausibility',0):.4f}")
print()

# Comparison
cmp = data.get("comparison", {})
print("=== COMPARISON ===")
print(f"  Original LTR (no anchors):    {cmp.get('original_ltr_no_anchors_mc',0):.1%}")
print(f"  RTL corrected (no anchors):   {cmp.get('rtl_corrected_no_anchors_mc',0):.1%}")
print(f"  RTL corrected + anchors:      {cmp.get('rtl_corrected_with_anchors_mc',0):.1%}")
print(f"  Improvement from RTL:         {cmp.get('improvement_from_rtl_correction_pp',0):+.1f} pp")
print(f"  Anchor amplification:         {cmp.get('anchor_amplification_pp',0):+.1f} pp")
print()

# Top signs in Condition B
print("=== TOP SIGNS BY CONSISTENCY (Condition B) ===")
cons_b = cond_b.get("consistency_per_sign", {})
anchors = cond_b.get("anchors_used", {})
top = sorted(cons_b.items(), key=lambda x: -x[1].get("consistency", 0))[:15]
print(f"  {'Sign':>5}  {'Modal':>9}  {'Cons':>6}  {'Runs':>5}  {'Anchored'}")
print("  " + "-" * 50)
for sign, v in top:
    a = anchors.get(sign, "")
    print(f"  {sign:>5}  {v.get('modal','?'):>9}  {v.get('consistency',0)*100:>5.0f}%  {v.get('n_runs',0):>5}  {'<-- ' + a if a else ''}")
