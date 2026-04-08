"""
Validate all 14 canonical graph experiment specs:
  1. Every sourcePort exists in the source node's defined outputs.
  2. Every targetPort exists in the target node's defined inputs.
  3. execute_graph() runs without an unexpected error.

CLI-only experiments (kandles_bias, linear_a_circularity, ocr_tables, ocr_texts)
return {"error": "...", "cli_only": True} — this is intentional and counted as OK.

Run:
    cd backend && python tests/validate_graphs.py
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from glossa_lab.experiment_graph import (
    ATOMIC_NODES,
    _build_proper_graph_specs,
    _node_type_and_params,
    execute_graph,
)


def _port_sets(nodes):
    """Return {node_id: (output_names, input_names)} for every node."""
    out = {}
    for nd in nodes:
        atomic_id, _ = _node_type_and_params(nd)
        atom = ATOMIC_NODES.get(atomic_id)
        if atom:
            out[nd["id"]] = (
                {p["name"] for p in atom.outputs},
                {p["name"] for p in atom.inputs},
            )
        else:
            out[nd["id"]] = (set(), set())
    return out


def validate_and_run(exp_id, spec):
    nodes = spec["nodes"]
    edges = spec["edges"]
    port_sets = _port_sets(nodes)

    # ── 1. Edge validity ──────────────────────────────────────────────────────
    edge_issues = []
    for e in edges:
        src, tgt = e["source"], e["target"]
        sp = e.get("sourcePort", "")
        tp = e.get("targetPort", "")

        if sp and src in port_sets:
            src_outputs = port_sets[src][0]
            if sp not in src_outputs:
                edge_issues.append(
                    f"  edge {e['id']}: sourcePort={sp!r} not in {src!r} "
                    f"outputs={sorted(src_outputs)}"
                )
        if tp and tgt in port_sets:
            tgt_inputs = port_sets[tgt][1]
            if tp not in tgt_inputs:
                edge_issues.append(
                    f"  edge {e['id']}: targetPort={tp!r} not in {tgt!r} "
                    f"inputs={sorted(tgt_inputs)}"
                )

    # ── 2. Execution ──────────────────────────────────────────────────────────
    t0 = time.time()
    try:
        result = execute_graph(spec)
        elapsed = round(time.time() - t0, 2)
    except Exception as exc:
        return edge_issues, False, {}, round(time.time() - t0, 2), str(exc)

    # CLI-only experiments intentionally return {"error": "...", "cli_only": True}
    is_cli_only = result.get("cli_only") is True
    has_unexpected_error = "error" in result and not is_cli_only

    return edge_issues, not has_unexpected_error, result, elapsed, None


def main():
    specs = _build_proper_graph_specs()

    print("=" * 72)
    print(f"  Validating {len(specs)} graph experiment specs")
    print("=" * 72)

    total_edge_issues = 0
    total_exec_failures = 0

    for exp_id, spec in specs.items():
        edge_issues, exec_ok, result, elapsed, exc = validate_and_run(exp_id, spec)

        edge_status = "OK" if not edge_issues else f"EDGE FAIL ({len(edge_issues)})"
        exec_status = "OK" if exec_ok else "EXEC FAIL"

        is_cli = result.get("cli_only") is True
        result_summary = (
            "CLI-only (expected)"
            if is_cli
            else (
                f"error: {result.get('error', '')[:60]}"
                if "error" in result
                else f"keys={list(result.keys())[:4]}"
            )
        )

        node_count = len(spec["nodes"])
        edge_count = len(spec["edges"])
        print(
            f"\n{'  ' if (not edge_issues and exec_ok) else '! '}"
            f"{exp_id}"
        )
        print(
            f"    nodes={node_count}  edges={edge_count}  "
            f"edges:{edge_status}  exec:{exec_status}  ({elapsed}s)"
        )
        print(f"    {result_summary}")

        for issue in edge_issues:
            print(f"    {issue}")
            total_edge_issues += 1

        if not exec_ok:
            total_exec_failures += 1
            if exc:
                print(f"    exception: {exc[:80]}")

    print()
    print("=" * 72)
    if total_edge_issues == 0 and total_exec_failures == 0:
        print("  ✓  All experiments: edges valid, execution successful.")
    else:
        print(f"  ✗  {total_edge_issues} edge issue(s), "
              f"{total_exec_failures} execution failure(s).")
    print("=" * 72)

    return 0 if (total_edge_issues == 0 and total_exec_failures == 0) else 1


if __name__ == "__main__":
    sys.exit(main())
