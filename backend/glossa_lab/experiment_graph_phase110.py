"""Experiment Graph Nodes: Phase-110 (spec 008) — M222 / 'kur' adjudication.

Ledger-sequence Phase-110 (2026-10-06): adjudicates the tension
Phase-109 left flagged — 109 anchors restored to 'kur'/LOW from
Phase-111 allograph resolution, whose recorded bases inherit the
value from M222, while M222 itself stands at 'min'/MEDIUM on
crosswalk v2.1 (Parpola) support. Applies the pre-registered
spec-008 rule: a derived value may not cite as its basis a premise
that the anchor sign's own sourced record contradicts.

  IndusPhase110M222Dossier  Part A: evidence dossier (decide-only)
  IndusPhase110M222Apply    Part B: disposition + change register
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


def _run(script: str, args: list[str], report: str, timeout: int = 1800):
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


def _phase110_node_defs():
    from glossa_lab.experiment_graph import AtomicNodeDef

    specs = [
        ("IndusPhase110M222Dossier", "Phase-110 M222/'kur' Dossier",
         "phase110_m222_dossier.py", [], "phase110_m222_dossier.json",
         "Phase-110 Part A (spec 008): reconstructs the Phase-111 "
         "allograph mechanism, M222='kur' (Phase-87) and M222='min' "
         "(crosswalk v2.1) records from in-repo artifacts, and "
         "determines the verdict predicates. Decide mode — touches "
         "nothing. CPU."),
        ("IndusPhase110M222Apply", "Phase-110 M222/'kur' Disposition Apply",
         "phase110_m222_apply.py", [], "phase110_change_register.json",
         "Phase-110 Part B (spec 008): applies the pre-registered "
         "disposition branch from the dossier verdict to the cohort "
         "entries, writes reports/phase110_change_register.json, "
         "regenerates anchors bookkeeping, and self-verifies that "
         "the anchors diff equals the register. CPU."),
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
