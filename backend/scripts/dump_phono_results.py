"""Dump key phonological analysis data for value assignment."""
import json
from pathlib import Path

R = Path(__file__).parent.parent / "reports"

phono = json.loads((R / "indus_phonological_analysis.json").read_text("utf-8"))
study = json.loads((R / "indus_decipherment_study.json").read_text("utf-8"))

vv = phono["ventris_validation"]
print("=== VALIDATED RIGHT GROUPS (same vowel?) ===")
for g in vv["validated_right_groups"]:
    print(f"  coh={g['cohesion']:.3f} tok={g['total_tokens']:>5}  {g['group']}")

print("\n=== VALIDATED LEFT GROUPS (same consonant?) ===")
for g in vv["validated_left_groups"]:
    print(f"  coh={g['cohesion']:.3f} tok={g['total_tokens']:>5}  {g['group']}")

print("\n=== EQUIVALENCE CLASSES ===")
for i, c in enumerate(phono["equivalence_classes"]):
    print(f"  Class {i:2d}: {c}")

print("\n=== TOP TMK SIGNS ===")
for p in study["positional"]["top_tmk"][:15]:
    print(f"  Sign {p['sign']:>4}  total={p['total']:>4}  T-rate={p['terminal_rate']:.3f}")

print("\n=== TOP INITIAL SIGNS ===")
for p in study["positional"]["top_initial"][:10]:
    print(f"  Sign {p['sign']:>4}  total={p['total']:>4}  I-rate={p['initial_rate']:.3f}")

print("\n=== TOP 20 FREQ SIGNS ===")
for r in study["char_freq"]["top_30"][:20]:
    print(f"  Sign {r['sign']:>4}  count={r['count']:>5}  freq={r['freq']:.5f}")

print("\n=== TOP SUFFIX CHAINS ===")
for r in phono["suffix_analysis"]["top_suffix_chains"][:12]:
    print(f"  {r['suffix']}  count={r['count']}")

print("\n=== COMPOUND CANDIDATES (high-PMI bigrams) ===")
for r in study["bigrams"]["compound_candidates"][:15]:
    print(f"  {r['pair']}  PMI={r['pmi']:.3f}")

print("\n=== CONTACT-EXCLUSIVE SIGNS ===")
contact = json.loads((R / "contact_zone_results.json").read_text("utf-8"))
print(f"  {contact['contact_exclusive_signs']}")
