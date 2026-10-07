"""Experiment Graph Nodes: Phase-111 (spec 009) — blind language-affiliation study.

Ledger-sequence Phase-111 (2026-10-06): the pre-registered blind
study of spec 009. A frozen 28-feature vector + LDA classifies
blinded corpora; a validation gate on known corpora truncated to
Indus dimensions must pass before any Indus classification exists.

  IndusPhase111BlindGate      panel build + validation gate (stop rule)
  IndusPhase111BlindClassify  final classification + verdict (gate-gated)
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


def _phase111_node_defs():
    from glossa_lab.experiment_graph import AtomicNodeDef

    specs = [
        ("IndusPhase111BlindGate", "Phase-111 Blind Affiliation: Gate",
         "phase111_blind_gate.py", [], "phase111_blind_affiliation_results.json",
         "Phase-111 stage 1 (spec 009): custodian builds the blinded, "
         "size-matched panel (known corpora, synthetic controls, 3 "
         "anonymized Indus replicates); analyst evaluates the frozen "
         "validation gate on known corpora only (linguistic BA >= 0.85, "
         "family BA >= 0.70, permutation p < 0.001). Gate failure stops "
         "the study as INCONCLUSIVE. CPU."),
        ("IndusPhase111BlindClassify", "Phase-111 Blind Affiliation: Classify + Verdict",
         "phase111_blind_classify.py", [], "phase111_blind_affiliation_results.json",
         "Phase-111 stage 2 (spec 009): runs only if the gate passed. "
         "Trains the final LDA on all known draws + generator classes, "
         "classifies the blind IDs, unblinds (event logged), and "
         "computes the verdict strictly under the frozen support / "
         "refutation thresholds (posterior >= 0.90, BF >= 10, BF < 3 "
         "or TOST +/-0.05 = no discrimination). CPU."),
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
