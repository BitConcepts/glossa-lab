"""Experiment Graph Node: Phase-104 claims evaluation.

  IndusClaimsEval   Phase-104: evaluate the untested extracted claims
                    against in-repo evidence (see
                    specs/003-mcp-and-test-gaps and
                    backend/scripts/phase104_claims_evaluation.py).

Registered separately from experiment_graph_phase104_109.py: that module
holds the previously planned Phase-104-109 nodes (IndusOCR etc.), while
this node is the claims-evaluation phase directed in spec 003.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent.parent
_SCRIPT = _REPO / "backend/scripts/phase104_claims_evaluation.py"
_REPORT = _REPO / "glossa-indus" / "reports" / "phase104_claims_evaluation.json"


def _run_claims_eval(timeout: int = 900) -> dict:
    if not _SCRIPT.exists():
        return {"error": f"Not found: {_SCRIPT}"}
    try:
        r = subprocess.run(
            [sys.executable, str(_SCRIPT)],
            capture_output=True, text=True, timeout=timeout, cwd=str(_REPO),
        )
        if r.returncode != 0:
            return {"error": f"exit {r.returncode}", "stderr": r.stderr[-400:]}
    except subprocess.TimeoutExpired:
        return {"error": f"timeout {timeout}s"}
    except Exception as e:  # noqa: BLE001
        return {"error": str(e)}
    if _REPORT.exists():
        try:
            return json.loads(_REPORT.read_text("utf-8"))
        except Exception:  # noqa: BLE001
            pass
    return {"ok": True}


def _phase104_claims_node_defs():
    from glossa_lab.experiment_graph import AtomicNodeDef

    def fn(i, p):
        return _run_claims_eval()

    return [
        AtomicNodeDef(
            id="IndusClaimsEval",
            name="Phase-104 Untested Claims Evaluation",
            category="Indus Decipherment",
            description=(
                "Phase-104: Evaluate every untested extracted claim against "
                "in-repo evidence using its own falsification condition. "
                "CPU only; writes glossa-indus/reports/phase104_claims_evaluation.json."
            ),
            inputs=[],
            outputs=[{"name": "result", "type": "json"}],
            params_schema={"type": "object", "properties": {}},
            fn=fn,
        )
    ]
