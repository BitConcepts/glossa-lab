"""Experiment Graph Nodes: Phase-120 — Bhaskar (2024) triage.

Ledger-sequence Phase-120 (2026-10-08): descriptive triage of the
44 anchors flagged pending_non_sa_validation against the
disagreement cases documented in Bhaskar (2024) + ESM1-ESM13.
The ESMs are anisotropy datasets, not a per-sign concordance
table; the phase reports only documented disagreements and
changes no anchor status.

  IndusPhase120BhaskarTriage
      disagreement register + 44-anchor triage reports
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent.parent
_SCRIPTS = _REPO / "backend/scripts"
_REPORTS = _REPO / "reports"


def _get_device():
    from glossa_lab.gpu_utils import detect_device
    return detect_device()


def _run(script: str, args: list[str], report: str, timeout: int = 3600):
    s = _SCRIPTS / script
    rp = _REPORTS / report
    if not s.exists():
        return {"error": f"Not found: {script}"}
    try:
        r = subprocess.run([sys.executable, str(s), *args], capture_output=True,
                           text=True, timeout=timeout, cwd=str(_REPO))
        if r.returncode != 0:
            return {"error": f"exit {r.returncode}", "stderr": r.stderr[-400:]}
    except subprocess.TimeoutExpired:
        return {"error": f"timeout {timeout}s"}
    except Exception as e:  # noqa: BLE001
        return {"error": str(e)}
    if rp.exists():
        try:
            return json.loads(rp.read_text("utf-8"))
        except Exception:  # noqa: BLE001
            pass
    return {"ok": True}


def _phase120_node_defs():
    from glossa_lab.experiment_graph import AtomicNodeDef

    specs = [
        ("IndusPhase120BhaskarTriage",
         "Phase-120 Bhaskar Triage (descriptive)",
         "phase120_bhaskar_triage.py", [],
         "phase120_bhaskar_triage_44.json",
         "Phase-120: descriptive triage of the 44 anchors flagged "
         "pending_non_sa_validation against Bhaskar (2024) and its "
         "ESM1-ESM13. The ESMs are anisotropy (sign-order) datasets, "
         "not a per-sign M77/ICIT/CISI concordance table; this node "
         "regenerates the documented-disagreement register (CSV + "
         "JSON) and the per-sign triage from the curated register "
         "in glossa_lab/phase120_bhaskar.py. It changes no anchor "
         "status, validates nothing, and contains no PRED content. CPU."),
    ]
    nodes = []
    for nid, name, script, args, report, desc in specs:
        def fn(i, p, s=script, a=args, r=report):
            return {**_run(s, a, r), "gpu_device": _get_device()}

        nodes.append(AtomicNodeDef(
            id=nid, name=name, category="Indus Decipherment",
            description=desc, inputs=[],
            outputs=[{"name": "result", "type": "json"},
                     {"name": "gpu_device", "type": "text"}],
            params_schema={"type": "object", "properties": {}}, fn=fn))
    return nodes
