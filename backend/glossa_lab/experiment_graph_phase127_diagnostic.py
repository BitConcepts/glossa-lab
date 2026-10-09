"""Experiment Graph Nodes: Phase-127 diagnostic (spec 021) —
cross-compilation disagreement diagnostic.

Ledger-sequence Phase-127 (2026-10-08): a diagnostic of
Phase-125's FINAL verdict (FAIL — DISAGREEMENT; median
TV 0.636931 over the 16 PRIMARY judgeable pairs). It
does NOT re-score Phase-125 and issues no verdict. Arms,
all frozen in spec 021: (a) Holdat split-half noise
floor, (b) matched-size subsampling null at the mayig
token counts, (c) inscription-level bootstrap CIs for
per-pair TVs and the median TV, (d) crosswalk
neighbourhood decomposition (ambiguity share +
attributable TV under the registered estimator),
(e) composition controls on the metadata strata that
exist on both sides (site = Mohenjo-daro; iconography
= unicorn; gaps stated, not improvised), (f) a power
statement: tokens-per-sign required for the frozen
Phase-125 gates to clear sampling noise. Profiles are
computed strictly within each compilation (never
pooled), joined only via the Phase-122 crosswalk, no
object-level join (spec 019 section 2.1), no anchor
modified, no PRED verdict issued.

Note: this module is NOT the legacy
experiment_graph_phase127.py node family (Gulf corpus /
Roif mining / fish site polysemy), which predates the
ledger-sequence numbering used here; the suffixed
filename follows the Phase-126 Wells precedent
(experiment_graph_phase126_wells.py).

  IndusPhase127CrossCompilationDiagnostic
      diagnostic arms + nulls + CIs + decomposition + reports
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


def _phase127_diagnostic_node_defs():
    from glossa_lab.experiment_graph import AtomicNodeDef

    specs = [
        ("IndusPhase127CrossCompilationDiagnostic",
         "Phase-127 Cross-Compilation Disagreement Diagnostic (spec 021)",
         "phase127_cross_compilation_diagnostic.py", [],
         "phase127_cross_compilation_diagnostic_results.json",
         "Phase-127 (spec 021): diagnostic of Phase-125's final "
         "FAIL/DISAGREEMENT verdict — split-half and matched-size "
         "sampling nulls, inscription bootstrap CIs, crosswalk "
         "neighbourhood decomposition, metadata-bounded "
         "composition controls (site/iconography), and a power "
         "statement for the frozen Phase-125 gates. No re-scoring, "
         "no verdict, no anchor changes, no PRED verdicts. CPU."),
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
