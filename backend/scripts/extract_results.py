"""Quick extraction: SA consistency scores for South Dravidian, Sanskrit, Pali, Tamil."""
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / "tests"))

from glossa_lab.experiment_graph import ATOMIC_NODES

# Load corpus
print("Loading Indus corpus (min_freq=8)...")
corpus_r = ATOMIC_NODES["BuiltinCorpus"].fn({}, {"corpus": "indus"})
filter_r = ATOMIC_NODES["TokenFilter"].fn({"sequences": corpus_r["sequences"]}, {"min_freq": 8})
seqs = filter_r["sequences"]
n_tokens = sum(len(s) for s in seqs)
print(f"  filtered: {len(seqs)} seqs, {n_tokens} tokens")

freq_r = ATOMIC_NODES["FreqCounter"].fn({"sequences": seqs}, {})
ent_r = ATOMIC_NODES["EntropyCalc"].fn({"freq_map": freq_r["freq_map"]}, {})
print(f"  H1={ent_r['h1']}")

# WSC
wsc_r = ATOMIC_NODES["WritingSystemClassifier"].fn({
    "distinct_symbols": freq_r["distinct_symbols"],
    "h1": ent_r["h1"],
}, {})
print(f"  WSC tier: {wsc_r.get('tier_classification')}")

results = {}
for lang, label in [
    ("dravidian", "Tamil Dravidian (baseline)"),
    ("south_dravidian", "South Dravidian Tam+Kan+Tel"),
    ("sanskrit", "Sanskrit Rigveda"),
    ("pali", "Pali MIA"),
]:
    print(f"\nRunning SA vs {label}...", flush=True)
    t0 = time.time()
    lm_r = ATOMIC_NODES["BuiltinLM"].fn({}, {"language": lang})
    lm = lm_r["lm"]
    print(f"  LM size={lm.size}, n_tokens={lm_r['n_tokens']}")
    # 3 seeds, 4000 iter for reasonable accuracy
    sa_r = ATOMIC_NODES["SADecipher"].fn(
        {"sequences": seqs, "lm": lm},
        {"n_seeds": 3, "max_iterations": 4000, "restarts": 2, "surjective": True, "ocp_weight": 0.0},
    )
    cons_r = ATOMIC_NODES["ConsistencyScorer"].fn({"all_mappings": sa_r["all_mappings"]}, {})
    elapsed = time.time() - t0
    result = {
        "language": lang,
        "label": label,
        "lm_size": lm.size,
        "lm_tokens": lm_r["n_tokens"],
        "mean_consistency": cons_r["mean_consistency"],
        "hci_pct": cons_r["hci_pct"],
        "hci_count": cons_r["hci_count"],
        "elapsed_s": round(elapsed, 1),
    }
    results[lang] = result
    print(f"  -> consistency={cons_r['mean_consistency']:.4f}  hci%={cons_r['hci_pct']:.1f}  ({elapsed:.0f}s)")

# Save
out = Path(__file__).parent.parent / "reports" / "indus_language_comparison.json"
out.write_text(json.dumps({
    "indus_h1": ent_r["h1"],
    "indus_distinct_signs": freq_r["distinct_symbols"],
    "indus_tokens_filtered": n_tokens,
    "wsc_tier": wsc_r.get("tier_classification"),
    "language_results": results,
}, indent=2))
print("\nSaved to reports/indus_language_comparison.json")

print("\n=== FINAL SUMMARY ===")
for lang, r in sorted(results.items(), key=lambda x: -x[1]["mean_consistency"]):
    print(f"  {r['label']:<38} consistency={r['mean_consistency']:.4f}  hci%={r['hci_pct']:.1f}")
