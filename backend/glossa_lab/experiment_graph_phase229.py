"""Experiment Graph node for Phase-229 (H23 compliance)."""
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path
from glossa_lab.experiment_graph import AtomicNodeDef

_REPO = Path(__file__).resolve().parent.parent.parent
_SCRIPTS = _REPO / "backend" / "scripts"
_OUTPUTS = _REPO / "outputs"
_S = [{"name": "json", "type": "json"}, {"name": "number", "type": "number"}, {"name": "text", "type": "text"}]


def _run(script, timeout=900):
    p = _SCRIPTS / script
    if not p.exists():
        return {"error": f"Not found: {script}"}
    try:
        r = subprocess.run([sys.executable, str(p)], capture_output=True, text=True,
                           timeout=timeout, cwd=str(_REPO))
        if r.returncode != 0:
            return {"error": f"Exit {r.returncode}", "stderr": r.stderr[-400:]}
    except subprocess.TimeoutExpired:
        return {"error": f"Timeout {timeout}s"}
    except Exception as e:  # noqa: BLE001
        return {"error": str(e)}
    return {"status": "ok"}


def _load(name):
    p = _OUTPUTS / name
    if not p.exists():
        return {"available": False}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return {"available": False}


def _p229(i, p):
    r = _load("phase229_cisi_anchor_sa.json")
    if r.get("available") is False:
        res = _run("phase229_cisi_anchor_sa.py", timeout=1800)
        if "error" in res:
            return {**res, "number": 0.0, "text": "P229 error"}
        r = _load("phase229_cisi_anchor_sa.json")
    verdict = r.get("verdict", "")
    p228 = r.get("phase228_cross_validation", {})
    rate = p228.get("cisi_tripartite_rate", 0)
    return {"json": r, "number": rate,
            "text": f"P229: {verdict[:80]} | CISI tripartite={rate:.1%}"}


def _phase229_node_defs():
    return [
        AtomicNodeDef("IndusPhase229CISIAnchorSA", "CISI Anchor SA Test (P229)",
                      "Indus Decipherment",
                      "Tests P122='pa' (Phase-226) as M122 anchor on Holdat SA. "
                      "Records Phase-228 CISI tripartite (46.5%, 3× null) as landmark. "
                      "Determines if M122 can be upgraded CANDIDATE→LOW.",
                      inputs=[], outputs=_S,
                      params_schema={"type": "object", "properties": {}}, fn=_p229),
    ]
