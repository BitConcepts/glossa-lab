"""
Repeat Fuls RTL study via graph experiment to verify consistent results.
Runs fuls_nw_semitic_decipher_run (RTL + 6 Fuls anchors) and compares to prior results.
Expected: mean consistency ~63.8% (with 6 Fuls anchors, RTL corrected).
"""
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from glossa_lab.experiment_graph import get_graph_experiment, execute_graph

spec = get_graph_experiment("fuls_nw_semitic_decipher_run")
print(f"Running: {spec['id']} ({len(spec['nodes'])} nodes)")
result = execute_graph(spec)
print("Result keys:", list(result.keys())[:10])
print(json.dumps({k: v for k, v in result.items() if not isinstance(v, (dict, list)) or len(str(v)) < 200}, indent=2, default=str)[:1000])
