"""Experiment Graph Nodes: Phase-116 (spec 015) — corpus-harmonization study.

Ledger-sequence Phase-116 (2026-10-07): the diagnostic study
Phase-115's recorded conclusion required — why do Holdat and
ICIT positional profiles disagree (T1 v2: 51 strict signs
judged, 43 FAIL, 40 on modal-class disagreement, median TV
0.789474)? Five frozen hypothesis families (composition,
segmentation, mapping, direction, definition), a matched-text
intersection built by a frozen wildcard matcher, verdicts by
frozen thresholds, and a harmonization recommendation assembled
mechanically from the verdicts. DIAGNOSTIC ONLY: no anchor
changes, no validation verdicts.

  IndusPhase116Harmonization  matcher + arms + verdicts + reports
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


def _phase116_node_defs():
    from glossa_lab.experiment_graph import AtomicNodeDef

    specs = [
        ("IndusPhase116Harmonization",
         "Phase-116 Corpus-Harmonization Study (Holdat vs ICIT)",
         "phase116_harmonization_study.py", [],
         "phase116_harmonization_results.json",
         "Phase-116 (spec 015): pre-registered diagnostic of the "
         "Holdat/ICIT positional disagreement left by Phase-115. "
         "Frozen matched-text matcher (tiers A/B/C) + five "
         "hypothesis families (composition, segmentation, mapping, "
         "direction, definition) with frozen verdict thresholds "
         "and a mechanically assembled harmonization recommendation. "
         "Diagnostic only — anchors untouched. CPU."),
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
