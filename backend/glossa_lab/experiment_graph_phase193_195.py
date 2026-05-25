"""Experiment Graph nodes for Phases 193-195."""
from __future__ import annotations
import json
import subprocess
import sys
from pathlib import Path
from glossa_lab.experiment_graph import AtomicNodeDef

_REPO    = Path(__file__).resolve().parent.parent.parent
_SCRIPTS = _REPO / "backend" / "scripts"
_OUTPUTS = _REPO / "outputs"


def _run(script, timeout=900):
    p = _SCRIPTS / script
    if not p.exists(): return {"error": f"Not found: {script}"}
    try:
        r = subprocess.run([sys.executable, str(p)], capture_output=True,
                           text=True, timeout=timeout, cwd=str(_REPO))
        if r.returncode != 0: return {"error": f"Exit {r.returncode}", "stderr": r.stderr[-400:]}
    except subprocess.TimeoutExpired: return {"error": f"Timeout {timeout}s"}
    except Exception as e: return {"error": str(e)}
    return {"status": "ok"}


def _load(name):
    p = _OUTPUTS / name
    if not p.exists(): return {"available": False}
    try: return json.loads(p.read_text(encoding="utf-8"))
    except Exception: return {"available": False}


def _sa_rerun(inputs, params):
    r = _load("phase193_sa_rerun_402anchors.json")
    if r.get("available") is False:
        res = _run("phase193_sa_rerun_402anchors.py", timeout=900)
        if "error" in res: return {**res, "number": 0.0, "text": "P193 error"}
        r = _load("phase193_sa_rerun_402anchors.json")
    agg = r.get("aggregate_confidence", 0.0)
    d3  = r.get("sa_all_anchors", {}).get("delta", 0.0)
    return {
        "aggregate_confidence": agg,
        "delta_all_vs_none": d3,
        "sa_runs": {k: v for k,v in r.items() if k.startswith("sa_")},
        "top_unanchored": r.get("top_unanchored_by_consistency", []),
        "p192_checks": r.get("p192_checks", []),
        "json": {"agg": agg, "delta": d3},
        "number": agg,
        "text": f"P193 SA rerun: aggregate={agg:.4f} ({agg*100:.1f}%) delta_all={d3:+.4f}",
    }


def _ssrn_fetch(inputs, params):
    r = _load("phase194_ssrn_fulltext.json")
    if r.get("available") is False:
        res = _run("phase194_ssrn_fulltext.py", timeout=180)
        if "error" in res: return {**res, "number": 0.0, "text": "P194 error"}
        r = _load("phase194_ssrn_fulltext.json")
    nn = r.get("total_new_proposals", 0)
    nc = r.get("total_confirms", 0)
    return {
        "total_new": nn, "total_confirms": nc,
        "papers": r.get("papers", []),
        "json": {"new": nn, "confirms": nc},
        "number": nn + nc,
        "text": f"P194 SSRN: {nn} new + {nc} confirms. {r.get('verdict','')}",
    }


def _grammar_reval(inputs, params):
    r = _load("phase195_grammar_revalidation.json")
    if r.get("available") is False:
        res = _run("phase195_grammar_revalidation.py", timeout=120)
        if "error" in res: return {**res, "number": 0.0, "text": "P195 error"}
        r = _load("phase195_grammar_revalidation.json")
    nc = r.get("p192_consistent", 0)
    fp = r.get("formula_pct", 0.0)
    return {
        "p192_consistent": nc, "formula_pct": fp,
        "positional_validation": r.get("positional_validation", []),
        "formula_coverage": r.get("formula_coverage", {}),
        "json": {"consistent": nc, "formula_pct": fp},
        "number": fp,
        "text": f"P195 grammar: {nc}/5 consistent. Formula coverage {fp}%. {r.get('verdict','')}",
    }


def _phase193_195_node_defs():
    S = [{"name":"json","type":"json"},{"name":"number","type":"number"},{"name":"text","type":"text"}]
    return [
        AtomicNodeDef("IndusSARerun193","SA Rerun 402-Anchors (P193)","Indus Decipherment",
            "Phase-193: SA with full 402-anchor set (correct M77 ID mapping). Reports aggregate confidence, deltas per tier, Phase-192 SA confirmation, top unanchored signs.",
            [],outputs=[{"name":"aggregate_confidence","type":"number"},{"name":"delta_all_vs_none","type":"number"},{"name":"sa_runs","type":"json"},{"name":"top_unanchored","type":"json"},{"name":"p192_checks","type":"json"},*S],
            params_schema={"type":"object","properties":{}},fn=_sa_rerun),
        AtomicNodeDef("IndusSSRNFetch194","SSRN Fulltext E17/E18 (P194)","Indus Decipherment",
            "Phase-194: Fetches SSRN papers E17 (fish-signs 2025) and E18 (pleonastic compounding 2025) and extracts sign-phoneme proposals. Compares with current anchor set.",
            [],outputs=[{"name":"total_new","type":"number"},{"name":"total_confirms","type":"number"},{"name":"papers","type":"json"},*S],
            params_schema={"type":"object","properties":{}},fn=_ssrn_fetch),
        AtomicNodeDef("IndusGrammarReval195","Grammar Revalidation 402-Anchors (P195)","Indus Decipherment",
            "Phase-195: Revalidates the Dravidian grammar model with 402 anchors. Checks Phase-192 new entries for positional consistency, bigram grammar, and formula coverage.",
            [],outputs=[{"name":"p192_consistent","type":"number"},{"name":"formula_pct","type":"number"},{"name":"positional_validation","type":"json"},{"name":"formula_coverage","type":"json"},*S],
            params_schema={"type":"object","properties":{}},fn=_grammar_reval),
    ]
