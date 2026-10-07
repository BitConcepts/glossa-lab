"""Experiment Graph Nodes: Phase-115 (spec 014) — non-SA validation battery v2.

Ledger-sequence Phase-115 (2026-10-07): successor to Phase-113,
whose battery was rejected at calibration when T1 starved on the
sparse Phase-107 ICIT layer (STRICT94 validated 3/94). Battery v2
rebuilds T1 on the expanded v2 converted layer (key-normalized
conversion, sentinel positions, partial inscriptions retained;
4,531 inscriptions / 13,492 mapped tokens) with attestation
floors scaled to each sign's measured opportunity-to-attest.
T2/T3, the calibration gates, and the decision rule are spec 011
unchanged. A failed gate rejects the battery and leaves the
anchors file untouched.

  IndusPhase115NonSaValidation  calibration + (gated) main run + reports
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


def _run(script: str, args: list[str], report: str, timeout: int = 7200):
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


def _phase115_node_defs():
    from glossa_lab.experiment_graph import AtomicNodeDef

    specs = [
        ("IndusPhase115NonSaValidation",
         "Phase-115 Non-SA Validation Battery v2 (44 flagged anchors)",
         "phase115_nonsa_battery_v2.py", [], "phase115_nonsa44v2_results.json",
         "Phase-115 (spec 014): non-SA battery v2 (T1 cross-corpus "
         "consistency on the expanded ICIT v2 layer with "
         "opportunity-scaled attestation floors, T2 positional-"
         "grammar fit vs the strict SA-independent core, T3 "
         "compositional co-occurrence) for the 44 anchors Phase-109 "
         "flagged pending_non_sa_validation. Calibration gates run "
         "first (strict-94 leave-one-out VALIDATED >= 57; kur-113 "
         "negative control VALIDATED <= 5); a rejected battery stops "
         "the phase with anchors untouched. Outcomes: "
         "VALIDATED_NON_SA / DEMOTE to CANDIDATE / UNRESOLVED. CPU."),
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
