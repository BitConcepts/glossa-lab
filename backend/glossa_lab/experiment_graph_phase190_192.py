"""Experiment Graph nodes for Phases 190-192: anchor injection, validation, update."""
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path
from typing import Any
from glossa_lab.experiment_graph import AtomicNodeDef

_REPO    = Path(__file__).resolve().parent.parent.parent
_SCRIPTS = _REPO / "backend" / "scripts"
_OUTPUTS = _REPO / "outputs"


def _run(script: str, timeout: int = 900) -> dict[str, Any]:
    p = _SCRIPTS / script
    if not p.exists(): return {"error": f"Not found: {script}"}
    try:
        r = subprocess.run([sys.executable, str(p)], capture_output=True,
                           text=True, timeout=timeout, cwd=str(_REPO))
        if r.returncode != 0: return {"error": f"Exit {r.returncode}", "stderr": r.stderr[-500:]}
    except subprocess.TimeoutExpired: return {"error": f"Timeout after {timeout}s"}
    except Exception as exc: return {"error": str(exc)}
    return {"status": "ok"}


def _load(name: str) -> dict[str, Any]:
    p = _OUTPUTS / name
    if not p.exists(): return {"available": False}
    try: return json.loads(p.read_text(encoding="utf-8"))
    except Exception: return {"available": False}


def _elamo_anchor_injection(inputs, params):
    r = _load("phase190_elamo_anchor_injection.json")
    if r.get("available") is False:
        res = _run("phase190_elamo_anchor_injection.py", timeout=900)
        if "error" in res: return {**res, "number": 0.0, "text": "Phase-190 error"}
        r = _load("phase190_elamo_anchor_injection.json")
    db = r.get("delta_b_vs_a", 0.0)
    dc = r.get("delta_c_vs_a", 0.0)
    nc = r.get("n_sa_confirmed", 0)
    return {
        "delta_b": db, "delta_c": dc, "n_sa_confirmed": nc,
        "proposals": r.get("proposals", []),
        "sa_confirmed": r.get("sa_confirmed_proposals", []),
        "json": {"delta_b": db, "delta_c": dc},
        "number": db, "text": f"Phase-190: delta_b={db:+.4f} delta_c={dc:+.4f} SA-confirmed={nc}. {r.get('verdict','')}",
    }


def _grammar_validation(inputs, params):
    r = _load("phase191_grammar_validation.json")
    if r.get("available") is False:
        res = _run("phase191_grammar_validation.py", timeout=120)
        if "error" in res: return {**res, "number": 0.0, "text": "Phase-191 error"}
        r = _load("phase191_grammar_validation.json")
    med = r.get("medium_count", 0)
    low = r.get("low_count", 0)
    return {
        "medium_count": med, "low_count": low,
        "candidate_count": r.get("candidate_count", 0),
        "by_confidence": r.get("by_confidence", {}),
        "best_per_phoneme": r.get("best_per_phoneme", {}),
        "json": {"medium": med, "low": low},
        "number": med + low,
        "text": f"Phase-191 grammar: {med} MEDIUM + {low} LOW proposals validated.",
    }


def _anchor_update_proposal(inputs, params):
    r = _load("phase192_anchor_update_proposal.json")
    if r.get("available") is False:
        res = _run("phase192_anchor_update_proposal.py", timeout=60)
        if "error" in res: return {**res, "number": 0.0, "text": "Phase-192 error"}
        r = _load("phase192_anchor_update_proposal.json")
    nn = r.get("n_new_proposed", 0)
    na = r.get("n_after_update", 0)
    return {
        "n_new_proposed": nn, "n_after_update": na,
        "absent_filled":  r.get("absent_filled", []),
        "still_absent":   r.get("still_absent", []),
        "diff":           r.get("diff", {}),
        "json": {"new": nn, "total": na},
        "number": nn,
        "text": f"Phase-192: {nn} new anchor candidates proposed. Total anchors: {na}. {r.get('verdict','')}",
    }


def _phase190_192_node_defs() -> list[AtomicNodeDef]:
    _S = [{"name":"json","type":"json"},{"name":"number","type":"number"},{"name":"text","type":"text"}]
    return [
        AtomicNodeDef(
            id="IndusElamoAnchorInjection190",
            name="Elamo-Dravidian Anchor Injection (P190)",
            category="Indus Decipherment",
            description=(
                "Phase-190: Injects 14 absent phoneme candidates (from McAlpin Elamo-Dravidian + "
                "Brahui North Dravidian) as anchors and runs SA convergence in 3 conditions. "
                "Fixes M77/anchor ID mismatch. Reports delta_b (Elamite), delta_c (combined), "
                "and SA-confirmed proposals."
            ),
            inputs=[], outputs=[
                {"name":"delta_b","type":"number"},{"name":"delta_c","type":"number"},
                {"name":"n_sa_confirmed","type":"number"},{"name":"proposals","type":"json"},
                {"name":"sa_confirmed","type":"json"},*_S],
            params_schema={"type":"object","properties":{}}, fn=_elamo_anchor_injection),
        AtomicNodeDef(
            id="IndusGrammarValidation191",
            name="Grammar + Phonotactic Validation (P191)",
            category="Indus Decipherment",
            description=(
                "Phase-191: Validates Phase-190 proposals against Dravidian positional grammar, "
                "bigram collocation strength with HIGH anchors, phonotactic rules, and frequency "
                "rank consistency. Assigns MEDIUM/LOW/CANDIDATE confidence to each proposal."
            ),
            inputs=[], outputs=[
                {"name":"medium_count","type":"number"},{"name":"low_count","type":"number"},
                {"name":"by_confidence","type":"json"},{"name":"best_per_phoneme","type":"json"},*_S],
            params_schema={"type":"object","properties":{}}, fn=_grammar_validation),
        AtomicNodeDef(
            id="IndusAnchorUpdateProposal192",
            name="Anchor Update Proposal (P192)",
            category="Indus Decipherment",
            description=(
                "Phase-192: Synthesizes Phases 186-191 into a proposed INDUS_FINAL_ANCHORS.json "
                "extension. Produces a diff file and proposed merged anchor set for review. "
                "Does NOT modify anchors in place — outputs to outputs/ for human review."
            ),
            inputs=[], outputs=[
                {"name":"n_new_proposed","type":"number"},{"name":"n_after_update","type":"number"},
                {"name":"absent_filled","type":"json"},{"name":"still_absent","type":"json"},
                {"name":"diff","type":"json"},*_S],
            params_schema={"type":"object","properties":{}}, fn=_anchor_update_proposal),
    ]
