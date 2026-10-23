"""Experiment Graph Nodes: Phase 419 (Spec 057 —
the heading carried by five sources: re-extract the
five passages; design D-19).

  IndusPhase419FiveSourcesHeading    Phase-419:
  step-0 gates, heading location under the
  heading-form rule, verbatim passage artifacts,
  and the five-row accounting of spec section 6.

The node serves the phase's committed results JSON
(reports/phase419_results.json), recomputing via the
phase script when that script's pinned inputs are
present locally. Freeze: specs/
057-five-sources-heading/freeze.md (digest
237b923a...); the frozen spec's contract registration
is OSF https://osf.io/chq5e/.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent.parent
_SCRIPTS = _REPO / "backend/scripts"


def _get_device():
    from glossa_lab.gpu_utils import detect_device
    return detect_device()


def _serve(script_name: str, results_name: str) -> dict:
    script = _SCRIPTS / script_name
    results = _REPO / "reports" / results_name
    if script.exists():
        try:
            r = subprocess.run(
                [sys.executable, str(script)],
                capture_output=True, text=True, timeout=1200,
                cwd=str(_REPO))
            if r.returncode == 0 and results.exists():
                return {"source": "script_recomputed",
                        **json.loads(results.read_text("utf-8"))}
        except Exception:  # noqa: BLE001
            pass
    if results.exists():
        return {"source": "committed_results",
                **json.loads(results.read_text("utf-8"))}
    return {"error": f"{results_name} not found"}


_NODE_SPECS = [
    ("IndusPhase419FiveSourcesHeading",
     "phase419_five_sources_heading.py",
     "phase419_results.json",
     "Phase-419 Five Sources Heading (spec 057)",
     "Phase-419 (spec 057): execution of the frozen Spec "
     "057 contract — the heading 'Statistical finding: "
     "positional analysis', merged in Phase I from five "
     "source documents, is accounted for source by "
     "source: step-0 gates (input integrity under the "
     "Spec 038 claims-store form; source-set integrity), "
     "heading location under the heading-form rule, "
     "verbatim passage artifacts for located passages, "
     "and exactly one outcome per source. Outcome "
     "(2026-10-21): headline class C — PARTIAL RECOVERY "
     "WITH UNLOCATED SOURCES (r=2, e=1, u=2): S-3 (Fuls "
     "2013) and S-4 (Wells 2015, Appendix II) each state "
     "a checkable positional classification finding, "
     "recovered as a claim at the created stage, "
     "unchecked; S-2's held chapter excerpt states the "
     "method and its classification definitions and no "
     "checkable finding (PASSAGE EMPTY); S-1 and S-5 "
     "carry no heading-form occurrence in their held "
     "texts (SOURCE UNLOCATED, sub-state HEADING NOT "
     "PRESENT IN HELD TEXT, with the stated search and "
     "the unblocking act on each row). The heading "
     "record is superseded by the two recovered claims "
     "by appended note. This act recovered what five "
     "passages state. It checked none of it. CPU."),
]


def _phase419_node_defs():
    from glossa_lab.experiment_graph import AtomicNodeDef

    nodes = []
    for nid, script_name, results_name, name, desc in _NODE_SPECS:
        def fn(i, p, _s=script_name, _r=results_name):
            return {**_serve(_s, _r), "gpu_device": _get_device()}

        nodes.append(AtomicNodeDef(
            id=nid, name=name, category="Indus Decipherment",
            description=desc, inputs=[],
            outputs=[{"name": "result", "type": "json"},
                     {"name": "gpu_device", "type": "text"}],
            params_schema={"type": "object", "properties": {}},
            fn=fn))
    return nodes
