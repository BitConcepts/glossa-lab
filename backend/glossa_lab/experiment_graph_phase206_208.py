"""Experiment Graph nodes for Phases 206-208.

Phase 206: Anchor injection M692=nal (MEDIUM) + M861=nallavar (LOW) + absent-phoneme audit
Phase 207: SA rerun with 404-anchor set vs Phase 193 baseline (50.3% -> 55.2%)
Phase 208: Bulk mine 5000 (fifth run: Brahui/IVC, computational 2025/2026, aDNA 2025/2026)
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


def _run(script, timeout=1800):
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


def _anchor206(i, p):
    r = _load("phase206_anchor_injection_m692_m861.json")
    if r.get("available") is False:
        res = _run("phase206_anchor_injection_m692_m861.py", timeout=60)
        if "error" in res: return {**res, "number": 0.0, "text": "P206 error"}
        r = _load("phase206_anchor_injection_m692_m861.json")
    new_t = r.get("new_total", 0)
    new_e = r.get("new_entries_added", [])
    verdict = r.get("verdict", "")
    return {
        "old_total": r.get("old_total", 0),
        "new_total": new_t,
        "new_entries_added": new_e,
        "confidence_after": r.get("confidence_after", {}),
        "absent_phoneme_status": r.get("absent_phoneme_status", {}),
        "json": {"new_total": new_t, "new_entries": len(new_e)},
        "number": new_t,
        "text": f"P206: {len(new_e)} new anchors added (total {new_t}). {verdict}",
    }


def _sa207(i, p):
    r = _load("phase207_sa_rerun_404anchors.json")
    if r.get("available") is False:
        res = _run("phase207_sa_rerun_404anchors.py", timeout=1800)
        if "error" in res: return {**res, "number": 0.0, "text": "P207 error"}
        r = _load("phase207_sa_rerun_404anchors.json")
    agg = r.get("aggregate_confidence", 0)
    delta = r.get("delta_vs_p193", 0)
    verdict = r.get("verdict", "")
    return {
        "aggregate_confidence": agg,
        "delta_vs_p193": delta,
        "sa_all_anchors": r.get("sa_all_anchors", {}),
        "new_anchor_checks": r.get("new_anchor_checks", []),
        "top_unanchored_by_consistency": r.get("top_unanchored_by_consistency", []),
        "anchor_counts": r.get("anchor_counts", {}),
        "json": {"aggregate": agg, "delta_vs_p193": delta},
        "number": agg,
        "text": f"P207: aggregate={agg:.4f} ({agg*100:.1f}%). Delta P193={delta:+.4f}. {verdict}",
    }


def _mine208(i, p):
    r = _load("phase208_bulk_mine_5000.json")
    if r.get("available") is False:
        res = _run("phase208_bulk_mine_5000.py", timeout=1800)
        if "error" in res: return {**res, "number": 0.0, "text": "P208 error"}
        r = _load("phase208_bulk_mine_5000.json")
    ns = r.get("n_strong_evidence", 0)
    nm = r.get("n_moderate_evidence", 0)
    total = r.get("total_papers_fetched", 0)
    return {
        "n_strong": ns,
        "n_moderate": nm,
        "total_fetched": total,
        "strong_papers": r.get("strong_papers", [])[:20],
        "json": {"strong": ns, "moderate": nm, "total": total},
        "number": ns,
        "text": f"P208: {ns} STRONG, {nm} MODERATE, {total} total. {r.get('verdict','')}",
    }


def _phase206_208_node_defs():
    S = [{"name": "json", "type": "json"}, {"name": "number", "type": "number"}, {"name": "text", "type": "text"}]
    return [
        AtomicNodeDef(
            "IndusAnchorInjection206",
            "Anchor Injection M692/M861 + Absent-Phoneme Audit (P206)",
            "Indus Decipherment",
            ("Phase-206: Adds M692=nal/nall [MEDIUM] (SA cons=0.40, INITIAL, DEDR 3594) and "
             "M861=nallavar [LOW] (SA cons=0.50, DEDR 3594 honorific) to INDUS_FINAL_ANCHORS. "
             "402 -> 404 anchors. Both entries SA-confirmed at cons=1.000 in Phase 207. "
             "Reconciles /du/ and /ga/ absent phonemes via existing HIGH anchors "
             "(M089=tu/tū, M391=ka/kaṇ through Elamite voiced alternation)."),
            [],
            outputs=[
                {"name": "old_total",              "type": "number"},
                {"name": "new_total",              "type": "number"},
                {"name": "new_entries_added",      "type": "json"},
                {"name": "confidence_after",       "type": "json"},
                {"name": "absent_phoneme_status",  "type": "json"},
                *S,
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_anchor206,
        ),
        AtomicNodeDef(
            "IndusSARerun207",
            "SA Rerun 404 Anchors vs P193 Baseline (P207)",
            "Indus Decipherment",
            ("Phase-207: SA rerun (4 conditions x 5 seeds) with 404-anchor set. "
             "Aggregate confidence 55.2% (+4.86pp vs Phase 193 baseline of 50.3%). "
             "M692=nal confirmed cons=1.000; M861=nallavar confirmed cons=1.000. "
             "D_ALL condition: mean_c=0.4844, hci=20, delta=+0.1906 vs no-anchor."),
            [],
            outputs=[
                {"name": "aggregate_confidence",          "type": "number"},
                {"name": "delta_vs_p193",                 "type": "number"},
                {"name": "sa_all_anchors",                "type": "json"},
                {"name": "new_anchor_checks",             "type": "json"},
                {"name": "top_unanchored_by_consistency", "type": "json"},
                {"name": "anchor_counts",                 "type": "json"},
                *S,
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_sa207,
        ),
        AtomicNodeDef(
            "IndusMine208",
            "Bulk Mine 5000 Fifth Run (P208)",
            "Indus Decipherment",
            ("Phase-208: Fifth bulk mine (4466 papers). 62 STRONG, 207 MODERATE. "
             "Key finds: 'Brahui and Oraon: Tracing Northern Dravidian to Balochistan' (2025), "
             "5+ computational Indus AI papers (2025/2026), 'Evidence for Scale-Free Commercial "
             "Network in IVC' (2026). Targeting Brahui/IVC NW corridor, computational AI, "
             "aDNA 2025/2026, McAlpin extensions."),
            [],
            outputs=[
                {"name": "n_strong",    "type": "number"},
                {"name": "n_moderate",  "type": "number"},
                {"name": "total_fetched", "type": "number"},
                {"name": "strong_papers", "type": "json"},
                *S,
            ],
            params_schema={"type": "object", "properties": {}},
            fn=_mine208,
        ),
    ]
