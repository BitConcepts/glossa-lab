"""
Fast edge-only validation: no experiment execution.
Checks that every sourcePort/targetPort references a real port handle.

Run:  cd backend && python tests/validate_edges.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from glossa_lab.experiment_graph import (
    ATOMIC_NODES,
    _build_proper_graph_specs,
    _node_type_and_params,
)

specs = _build_proper_graph_specs()
issues = []

for exp_id, spec in specs.items():
    port_map = {}
    for nd in spec["nodes"]:
        aid, _ = _node_type_and_params(nd)
        atom = ATOMIC_NODES.get(aid)
        if atom:
            port_map[nd["id"]] = (
                {p["name"] for p in atom.outputs},
                {p["name"] for p in atom.inputs},
            )
        else:
            port_map[nd["id"]] = (set(), set())
            issues.append(f"{exp_id}: unknown atomicId={aid!r} on node {nd['id']!r}")

    for e in spec["edges"]:
        src, tgt = e["source"], e["target"]
        sp = e.get("sourcePort", "")
        tp = e.get("targetPort", "")
        if sp and src in port_map and sp not in port_map[src][0]:
            issues.append(
                f"{exp_id}  edge={e['id']!r}  "
                f"sourcePort={sp!r} not in {src!r} outputs={sorted(port_map[src][0])}"
            )
        if tp and tgt in port_map and tp not in port_map[tgt][1]:
            issues.append(
                f"{exp_id}  edge={e['id']!r}  "
                f"targetPort={tp!r} not in {tgt!r} inputs={sorted(port_map[tgt][1])}"
            )

print(f"Checked {len(specs)} specs  |  {sum(len(s['edges']) for s in specs.values())} edges")
if not issues:
    print("ALL EDGES VALID — every sourcePort and targetPort references a real handle.")
else:
    print(f"{len(issues)} ISSUE(S):")
    for i in issues:
        print(" ", i)

sys.exit(0 if not issues else 1)
