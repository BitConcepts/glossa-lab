"""Experiment Graph Nodes: Phase-132 (spec 023, FROZEN) —
Stage P pilot of the keyed transcription layer.

Ledger-sequence Phase-132 (2026-10-09): the Stage P pilot
build under frozen spec 023 — a 50-object deterministic
frame over CISI Vols. 1–2, two blinded passes plus a
10-object gold pass and adjudication, measured against
the section 5.6 freeze-block gates and the section 3.1
stop-rule. Outcome of record: the stop-rule FIRED
(exact-sequence agreement all-50, P = 0.20 < 0.80) and
all three gold-scope release gates failed, so no
tranche is proposed and no dataset publication occurs.
This node exposes the pilot metrics JSON only; it
evaluates no prediction and changes no anchor.

  IndusPhase132PilotMetrics
      pilot metrics (agreement / estimator / effort)
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


def _phase132_node_defs():
    from glossa_lab.experiment_graph import AtomicNodeDef

    specs = [
        ("IndusPhase132PilotMetrics",
         "Phase-132 Stage P Pilot Metrics (spec 023, stop-rule fired)",
         "phase132_metrics.py", [],
         "phase132_pilot_metrics.json",
         "Phase-132 (spec 023, FROZEN): Stage P pilot metrics "
         "for the keyed transcription layer — exact-sequence "
         "and per-token inter-pass agreement, the frozen "
         "three-way gold error estimator, UNK / crosswalk-"
         "unmapped shares, attestation checks, and measured "
         "per-object effort, computed from the local-store "
         "pass records. Stop-rule fired (exact-seq all-50 "
         "P = 0.20 < 0.80); release gates all fail; no "
         "publication. Metrics only: no PRED evaluation, "
         "no anchor changes. CPU."),
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
