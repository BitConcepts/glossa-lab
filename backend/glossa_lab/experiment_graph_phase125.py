"""Experiment Graph Nodes: Phase-125 (spec 019) —
cross-compilation positional comparison.

Ledger-sequence Phase-125 (2026-10-08): per-sign
positional profiles (initial/medial/terminal rates)
computed WITHIN the mayig/CISI compilation (Phase-122
layer, P-space) and WITHIN the Holdat compilation
(M-space) separately — inscriptions never pooled —
joined only through the Phase-122 Parpola-Mahadevan
crosswalk v1. PRIMARY arm: high-confidence pairs that
are unambiguous within the high set (286 pairs), floor
8 tokens per sign per compilation (16 judgeable).
Verdict (spec section 6, PRIMARY arm only): PASS iff
median TV <= 0.35 and Spearman rho >= 0.50 on both
initial and terminal rates and the pairing-shuffle
null (B = 999, seed 125125) gives p <= 0.05; FAIL iff
median TV >= 0.50 and p_null > 0.05; NULL-STARVED iff
judgeable < 12; otherwise NULL-INCONCLUSIVE.
Sensitivity arms (medium-included — v1 has zero medium
pairs, so it coincides with PRIMARY by construction;
all-pairs, judged pair-by-pair) are reported
separately and never pooled. No object-level join is
performed: Holdat cisi_number is internal sequential
numbering, not a CISI object ID (spec section 2.1).
No anchor is modified and no PRED verdict is issued.

Note: this module is NOT the legacy
experiment_graph_phase124_125.py node family (fish
polysemy / Arthasastra mining), which predates the
ledger-sequence numbering used here.

  IndusPhase125CrossCompilationPositional
      arms + profiles + statistics + null + verdict + reports
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


def _phase125_node_defs():
    from glossa_lab.experiment_graph import AtomicNodeDef

    specs = [
        ("IndusPhase125CrossCompilationPositional",
         "Phase-125 Cross-Compilation Positional Comparison (mayig/CISI vs Holdat)",
         "phase125_cross_compilation.py", [],
         "phase125_cross_compilation_results.json",
         "Phase-125 (spec 019): cross-compilation positional "
         "comparison — per-sign initial/medial/terminal profiles "
         "computed within the mayig/CISI layer and within Holdat "
         "separately (never pooled), joined only via the Phase-122 "
         "crosswalk v1. PRIMARY arm: high-confidence unambiguous "
         "pairs, floor 8; verdict by the frozen rule (median TV, "
         "Spearman rho on initial/terminal rates, pairing-shuffle "
         "null B = 999 seed 125125). Sensitivity arms reported "
         "separately, never pooled. No object-level join (spec "
         "section 2.1); no anchor changes; no PRED verdicts. CPU."),
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
