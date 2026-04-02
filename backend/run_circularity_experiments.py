"""Run all 7 anti-circularity experiments.
Run: shell.cmd python backend/run_circularity_experiments.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tests'))

from glossa_lab.experiments.linear_a_circularity import run_all_experiments
import json, pathlib

results = run_all_experiments(n_mc_trials=30, verbose=True)

out = pathlib.Path(__file__).parent.parent / "reports" / "circularity_results.json"
out.parent.mkdir(exist_ok=True)
with open(out, "w") as f:
    json.dump(results, f, indent=2)
print(f"\nResults saved: {out}")
