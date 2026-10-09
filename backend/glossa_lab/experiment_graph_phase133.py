"""Experiment Graph Nodes: Phase-133 (spec 024, FROZEN Stage 0) —
evidence-integration context-field inventory.

Ledger-sequence Phase-133 (2026-10-09): the Stage 0 build under
frozen spec 024 — a (layer x field) coverage matrix over every
machine-readable layer in hand, a join-key audit with empirical
collision counts, field-provenance grading (O / C / I), a mayig
description parseability measurement under a stated rule, and a
descriptive pass over the non-machine-readable material. Facts
only: coverage and joinability, no associations, no anchor or
PRED evaluation. This node exposes the inventory summary only;
the full inventory is the committed dataset at
data/evidence_integration/phase133_stage0_inventory.json.

  IndusPhase133Stage0Inventory
      Stage 0 inventory summary (coverage / keys / grades)
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent.parent
_SCRIPTS = _REPO / "backend/scripts"
_INVENTORY = (_REPO / "data" / "evidence_integration"
              / "phase133_stage0_inventory.json")


def _get_device():
    from glossa_lab.gpu_utils import detect_device
    return detect_device()


def _summary(inventory: dict, source: str) -> dict:
    ja = inventory["join_key_audit"]
    return {
        "source": source,
        "phase": inventory["phase"],
        "n_layers": len(inventory["layers"]),
        "n_coverage_rows": len(inventory["coverage_matrix"]),
        "layers": [
            {"layer_id": layer["layer_id"],
             "row_count": layer["row_count"],
             "n_fields": layer["n_fields"]}
            for layer in inventory["layers"]],
        "distinct_objects_vol1": ja["distinct_objects_vol1"],
        "distinct_objects_vol2": ja["distinct_objects_vol2"],
        "mayig_key": ja["mayig_cisi_object_id"],
        "museum_cross_references": ja["museum_cross_references"],
        "grade_counts": inventory["provenance_grading"]["counts"],
        "class_i_count": inventory["provenance_grading"][
            "class_i_count"],
        "mayig_parseability": {
            k: inventory["mayig_description_parseability"][k]
            for k in ("n_descriptions", "with_both", "with_neither",
                      "with_at_least_one_motif_term",
                      "with_at_least_one_object_type_term")},
    }


def _run_inventory():
    """Recompute via the builder when the local store is present;
    otherwise serve the committed inventory (the builder's inputs
    are local-store files that never enter git)."""
    script = _SCRIPTS / "phase133_stage0_inventory.py"
    if script.exists():
        try:
            r = subprocess.run(
                [sys.executable, str(script)], capture_output=True,
                text=True, timeout=7200, cwd=str(_REPO))
            if r.returncode == 0 and _INVENTORY.exists():
                return _summary(
                    json.loads(_INVENTORY.read_text("utf-8")),
                    "builder_recomputed")
        except Exception:  # noqa: BLE001
            pass
    if _INVENTORY.exists():
        return _summary(json.loads(_INVENTORY.read_text("utf-8")),
                        "committed_inventory")
    return {"error": "phase133 inventory not found"}


def _phase133_node_defs():
    from glossa_lab.experiment_graph import AtomicNodeDef

    specs = [
        ("IndusPhase133Stage0Inventory",
         "Phase-133 Stage 0 Inventory (spec 024, facts only)",
         "Phase-133 (spec 024, FROZEN Stage 0): context-field "
         "inventory — (layer x field) coverage matrix, join-key "
         "audit with empirical collision counts, field-provenance "
         "grading (O / C / I), mayig description parseability "
         "under a stated rule, and the non-machine-readable "
         "descriptive pass. Coverage and joinability only: no "
         "associations computed, no PRED evaluation, no anchor "
         "changes. Recomputes from the local store when present "
         "and otherwise serves the committed inventory JSON. "
         "CPU."),
    ]
    nodes = []
    for nid, name, desc in specs:
        def fn(i, p):
            return {**_run_inventory(), "gpu_device": _get_device()}

        nodes.append(AtomicNodeDef(
            id=nid, name=name, category="Indus Decipherment",
            description=desc, inputs=[],
            outputs=[{"name": "result", "type": "json"},
                     {"name": "gpu_device", "type": "text"}],
            params_schema={"type": "object", "properties": {}},
            fn=fn))
    return nodes
