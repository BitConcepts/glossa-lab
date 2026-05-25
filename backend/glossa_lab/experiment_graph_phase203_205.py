"""Experiment Graph nodes for Phases 203-205.

Phase 203: Falsify E28 metrological hypothesis (Ledger of Meluhha)
Phase 204: McAlpin extended cognate extraction (E29/E30)
Phase 205: Bayesian Dravidian phylogenetics + Munda substrate timeline (E31/E32)
"""
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


def _metro203(i, p):
    r = _load("phase203_falsify_metrological.json")
    if r.get("available") is False:
        res = _run("phase203_falsify_metrological.py", timeout=120)
        if "error" in res: return {**res, "number": 0.0, "text": "P203 error"}
        r = _load("phase203_falsify_metrological.json")
    tests  = r.get("tests_run", 7)
    passed = r.get("tests_passed", 0)
    verdict = r.get("verdict", "")
    h1 = r.get("indus_metrics", {}).get("H1_entropy", 0)
    return {
        "tests_run":    tests,
        "tests_passed": passed,
        "indus_metrics": r.get("indus_metrics", {}),
        "benchmark_table": r.get("benchmark_table", []),
        "json":   {"tests": tests, "passed": passed, "h1": h1},
        "number": passed,
        "text":   f"P203: {passed}/{tests} falsification tests passed. {verdict}",
    }


def _cognates204(i, p):
    r = _load("phase204_mcalpin_extended_cognates.json")
    if r.get("available") is False:
        res = _run("phase204_mcalpin_extended_cognates.py", timeout=120)
        if "error" in res: return {**res, "number": 0.0, "text": "P204 error"}
        r = _load("phase204_mcalpin_extended_cognates.json")
    total   = r.get("total_cognates", 0)
    props   = r.get("new_proposals", [])
    n_med   = len([p for p in props if p.get("proposed_confidence") == "MEDIUM"])
    n_low   = len([p for p in props if p.get("proposed_confidence") == "LOW"])
    verdict = r.get("verdict", "")
    return {
        "total_cognates": total,
        "new_proposals": props,
        "absent_coverage": r.get("absent_coverage", {}),
        "json":   {"total": total, "medium": n_med, "low": n_low},
        "number": total,
        "text":   f"P204: {total} cognates, {n_med} MEDIUM upgrades, {n_low} LOW. {verdict}",
    }


def _phylo205(i, p):
    r = _load("phase205_bayesian_phylogenetics.json")
    if r.get("available") is False:
        res = _run("phase205_bayesian_phylogenetics.py", timeout=120)
        if "error" in res: return {**res, "number": 0.0, "text": "P205 error"}
        r = _load("phase205_bayesian_phylogenetics.json")
    fitness = r.get("ivc_fitness", {})
    nodes   = r.get("divergence_nodes", [])
    fit_str = fitness.get("overall_fit", "UNKNOWN")
    compat  = sum(1 for n in nodes if n.get("compatible"))
    verdict = r.get("verdict", "")
    return {
        "ivc_fitness":        fitness,
        "divergence_nodes":   nodes,
        "language_timeline":  r.get("language_timeline", []),
        "munda_substrate":    r.get("munda_substrate", []),
        "key_findings":       r.get("key_findings", []),
        "json":   {"fit": fit_str, "compatible_nodes": compat},
        "number": compat,
        "text":   f"P205: {compat}/{len(nodes)} nodes IVC-compatible, overall fit={fit_str}. {verdict}",
    }


def _phase203_205_node_defs():
    S = [{"name": "json", "type": "json"}, {"name": "number", "type": "number"}, {"name": "text", "type": "text"}]
    return [
        AtomicNodeDef(
            "IndusMetrological203",
            "Falsify E28 Metrological Hypothesis (P203)",
            "Indus Decipherment",
            ("Phase-203: 7-test statistical battery to falsify the 'Ledger of Meluhha' metrological "
             "hypothesis (E28). Tests H1 entropy, Zipf exponent, bigram diversity, positional entropy, "
             "sign inventory, grammar coverage, and Tamil H1 match. E28 FALSIFIED 7/7."),
            [],
            outputs=[
                {"name": "tests_run",     "type": "number"},
                {"name": "tests_passed",  "type": "number"},
                {"name": "indus_metrics", "type": "json"},
                {"name": "benchmark_table", "type": "json"},
                *S,
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_metro203,
        ),
        AtomicNodeDef(
            "IndusMcAlpinCognates204",
            "McAlpin Extended Cognate Extraction (P204)",
            "Indus Decipherment",
            ("Phase-204: Extracts all Elamo-Dravidian cognates from McAlpin 1981 APPENDIX II (E29) "
             "and McAlpin 1975 JAOS (E30). Covers all 9 remaining absent phonemes. Proposes MEDIUM "
             "confidence assignment for /du/ and /ga/ (combined score 11), LOW for /sum/, /gu/, "
             "/ab/, /ba/, /mil/. Confirms IVC absent-phoneme evidence is complete."),
            [],
            outputs=[
                {"name": "total_cognates", "type": "number"},
                {"name": "new_proposals",  "type": "json"},
                {"name": "absent_coverage","type": "json"},
                *S,
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_cognates204,
        ),
        AtomicNodeDef(
            "IndusBayesianPhylo205",
            "Bayesian Dravidian Phylogenetics + Munda Timeline (P205)",
            "Indus Decipherment",
            ("Phase-205: Kolipakam 2018 Bayesian analysis gives PDr origin ~4500 BCE — predates IVC "
             "by ~1900 years. Proto-Central Dravidian CI 2300–3800 BCE has 42.9% IVC overlap. Munda "
             "contact window 2000–4000 BCE has 85.7% IVC overlap. Overall IVC-Dravidian fit = EXCELLENT. "
             "Provides temporal framing for all E01-E29 linguistic evidence."),
            [],
            outputs=[
                {"name": "ivc_fitness",       "type": "json"},
                {"name": "divergence_nodes",  "type": "json"},
                {"name": "language_timeline", "type": "json"},
                {"name": "munda_substrate",   "type": "json"},
                {"name": "key_findings",      "type": "json"},
                *S,
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_phylo205,
        ),
    ]
