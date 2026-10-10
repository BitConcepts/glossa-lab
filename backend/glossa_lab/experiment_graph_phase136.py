"""Experiment Graph Nodes: Phase-136 (spec 024, Stage 2(a)) —
terminal-class x object type permutation test.

Ledger-sequence Phase-136 (2026-10-09): family member F1 under
the frozen Stage 2(a) freeze record
(specs/024-evidence-integration/stage2a-freeze.md). On the
ICIT-lineage (horus84) catalogue-joined subset, restricted to
Seals/Tablets, the terminal sign's membership in the frozen
TERMINAL14 class is tested against catalogue object type with a
Cochran-Mantel-Haenszel statistic and a within-site permutation
null (B = 9,999, seed 20261009). This node exposes the committed
results summary only; the full record is
reports/phase136_results.json and the report is
reports/phase136_report.md. The verdict word is deferred to the
combined Stage 2 report's family Benjamini-Hochberg correction.
Reliability of the label: results describe this lineage layer's
joined subset, not the Indus corpus in general. No PRED
evaluation, no anchor changes.

  IndusPhase136TerminalType
      Stage 2(a) terminal-class x object type summary
"""
from __future__ import annotations

import json
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent.parent
_RESULTS = _REPO / "reports" / "phase136_results.json"


def _get_device():
    from glossa_lab.gpu_utils import detect_device
    return detect_device()


def _summary(results: dict, source: str) -> dict:
    test = results.get("test") or {}
    return {
        "source": source,
        "phase": results["phase"],
        "family_member": results["family_member"],
        "lineage_label": results["lineage_label"],
        "flow": results["flow"],
        "eligible_strata": results["eligible_strata"],
        "estimability": results["estimability"],
        "statistic_observed": test.get("statistic_observed"),
        "raw_p": test.get("raw_p"),
        "effect_sizes": results["effect_sizes"],
        "ai_disclosure": results["ai_disclosure"],
    }


def _run_results():
    """Serve the committed results JSON. The builder's inputs are
    local-store files that never enter git, and the permutation
    run is a governed phase execution — not a node recomputation —
    so this node never recomputes."""
    if _RESULTS.exists():
        return _summary(json.loads(_RESULTS.read_text("utf-8")),
                        "committed_results")
    return {"error": "phase136 results not found"}


def _phase136_node_defs():
    from glossa_lab.experiment_graph import AtomicNodeDef

    specs = [
        ("IndusPhase136TerminalType",
         "Phase-136 Terminal-Class x Object Type (spec 024 Stage 2(a), F1)",
         "Phase-136 (spec 024, FROZEN Stage 2(a); family member "
         "F1): terminal-class (TERMINAL14) x catalogue object "
         "type (Seals vs Tablets) Cochran-Mantel-Haenszel test "
         "with within-site permutation null (B = 9,999, seed "
         "20261009) on the ICIT-lineage (horus84) joined subset — "
         "lineage label mandatory; results describe this lineage "
         "layer's joined subset, not the Indus corpus in "
         "general. Serves the committed results JSON. No PRED "
         "evaluation, no anchor changes. CPU."),
    ]
    nodes = []
    for nid, name, desc in specs:
        def fn(i, p):
            return {**_run_results(), "gpu_device": _get_device()}

        nodes.append(AtomicNodeDef(
            id=nid, name=name, category="Indus Decipherment",
            description=desc, inputs=[],
            outputs=[{"name": "result", "type": "json"},
                     {"name": "gpu_device", "type": "text"}],
            params_schema={"type": "object", "properties": {}},
            fn=fn))
    return nodes
