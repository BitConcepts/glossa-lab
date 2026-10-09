"""Experiment Graph Nodes: Phase-131 attribution (spec 022) —
source-of-disagreement attribution for Phase-125/127.

Ledger-sequence Phase-131 (2026-10-09): a mechanism
attribution of Phase-125's FINAL verdict (FAIL —
DISAGREEMENT; median TV 0.636931 over the 16 PRIMARY
judgeable pairs). It does NOT re-score Phase-125, issues
no verdict, and does not touch spec 020's NO. Arms, all
frozen in spec 022: (A) matched-object alignment — object
identity established only by inscription content in the
shared M-sign space (no CISI-ID join exists: Holdat's
cisi_number is internal sequential numbering, spec 019
section 2.1), with every pairwise difference classified
identical / segmentation split / segmentation merge /
substitution / insertion-deletion / order-only, plus the
positional-profile TV on matched objects only;
(B) reading-direction arms (mayig reversed / Holdat
reversed) judged against the Phase-127 matched-size noise
band; (C) stratification by site, object type, and text
length (period NOT ESTIMABLE — no metadata) plus a
length-composition-adjusted comparison; (D) a synthesis
attribution table with per-mechanism frozen estimators,
NOT ESTIMABLE rows where an arm cannot estimate, and the
residual unexplained share stated plainly. No anchor
modified, no PRED verdict issued.

  IndusPhase131Attribution
      attribution arms + synthesis + reports
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


def _phase131_attribution_node_defs():
    from glossa_lab.experiment_graph import AtomicNodeDef

    specs = [
        ("IndusPhase131Attribution",
         "Phase-131 Source-of-Disagreement Attribution (spec 022)",
         "phase131_attribution.py", [],
         "phase131_attribution_results.json",
         "Phase-131 (spec 022): mechanism attribution of Phase-125's "
         "final FAIL/DISAGREEMENT result — matched-object alignment "
         "and difference classification (content matcher only; no "
         "CISI-ID join exists), reading-direction arms vs the "
         "Phase-127 noise band, site/object-type/length "
         "stratification plus composition adjustment, and a "
         "synthesis attribution table with NOT ESTIMABLE rows. "
         "Diagnostics only: no re-scoring, no verdict, no anchor "
         "changes, no PRED verdicts. CPU."),
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
