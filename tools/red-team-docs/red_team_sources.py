"""Source reading for the derived red-team documents (Spec 095, T406).

This module is the READER half of the document generator: it
reads the canonical artifacts and records and computes the facts
the documents state. It writes nothing — no write call of any
kind appears in this file, by design: the ledger gate's V9
writer census (backend/glossa_lab/ledger_gate.py) classifies
production Python by whether a file that names a canonical
artifact also writes, and this file is a reader of those
artifacts, never a writer of anything.

The writer half is generate_red_team_docs.py in this directory.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ledger_census(root: Path) -> dict:
    rows = [json.loads(ln) for ln in
            (root / "glossa-indus/ledger/claims.jsonl").read_text(encoding="utf-8").splitlines() if ln.strip()]
    claims = [r for r in rows if r.get("kind") == "claim"]
    with_refs = [r for r in claims if r.get("sign_refs")]
    return {
        "lines": len(rows), "claims": len(claims),
        "annotations": len(rows) - len(claims),
        "with_falsifier": sum(1 for r in claims if r.get("falsifier")),
        "claims_with_sign_refs": len(with_refs),
        "sign_refs_total": sum(len(r["sign_refs"]) for r in with_refs),
    }


def anchors_census(root: Path) -> dict:
    data = json.loads((root / "backend/reports/INDUS_FINAL_ANCHORS.json").read_text(encoding="utf-8"))
    return {"total": data["total"], "by_confidence": data["by_confidence"]}


def matrix_census(root: Path) -> dict:
    matrix = json.loads((root / "glossa-indus/matrix/matrix.json").read_text(encoding="utf-8"))
    return {"rows": len(matrix["rows"]), "columns": len(matrix["columns"])}


def program_map_nodes(root: Path) -> int:
    pmap = json.loads((root / "glossa-indus/map/program-map.json").read_text(encoding="utf-8"))
    return len(pmap.get("nodes", []))


def task_states(path: Path) -> list[tuple[str, bool]]:
    out = []
    for ln in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"- \[(x| )\] \*\*(T\d+)", ln)
        if m:
            out.append((m.group(2), m.group(1) == "x"))
    return out


def gap_entries(root: Path) -> list[str]:
    text = (root / "glossa-indus/map/gap-register.md").read_text(encoding="utf-8")
    return sorted(set(re.findall(r"GR-088-\d+", text)))


def corpus_keys(root: Path) -> list[str]:
    ci_text = (root / "backend/glossa_lab/data/corpus_identity.py").read_text(encoding="utf-8")
    return re.findall(r'^[A-Z0-9_]+_KEY = "([a-z0-9_]+)"', ci_text, flags=re.MULTILINE)


def stage1_says_invalid(root: Path) -> bool:
    path = root / "specs/095-red-team-remediation/records/stage-1-record-2026-11-16.md"
    return path.is_file() and "INVALID AT GATE 0.1" in path.read_text(encoding="utf-8")


def audit_facts(root: Path) -> dict:
    rec_dir = root / "specs/095-red-team-remediation/records"
    run = json.loads((rec_dir / "t404-run-2026-11-17.json").read_text(encoding="utf-8"))
    corrections = {}
    corr_path = rec_dir / "t404-scoring-corrections.json"
    if corr_path.is_file():
        for c in json.loads(corr_path.read_text(encoding="utf-8"))["corrections"]:
            corrections[c["item"]] = c
    results = []
    for r in run["results"]:
        verdict = corrections.get(r["item"], {}).get("corrected_verdict", r["verdict"])
        results.append({**r, "scored_verdict": verdict})
    return {"run": run, "results": results, "corrections": corrections}


def source_sets(root: Path) -> dict[str, list[Path]]:
    """The per-document source lists, as paths (named on each
    document's face by the writer)."""
    spec095 = root / "specs/095-red-team-remediation"
    rec = spec095 / "records"
    candidates = {
        "program_audit": [
            root / "glossa-indus/ledger/claims.jsonl",
            root / "backend/reports/INDUS_FINAL_ANCHORS.json",
            root / "glossa-indus/matrix/matrix.json",
            root / "glossa-indus/map/program-map.json",
            spec095 / "tasks.md",
        ],
        "security_review": [
            root / "specs/092-platform-hardening-r4/tasks.md",
            root / "specs/094-research-loop-acceptance-hardening/tasks.md",
            root / "backend/glossa_lab/release_gate.py",
            root / "backend/glossa_lab/anchor_transition.py",
        ],
        "reproducibility_gaps": [
            root / "backend/glossa_lab/data/corpus_identity.py",
            rec / "stage-1-record-2026-11-16.md",
            rec / "stage-3-record-2026-11-16.md",
            rec / "t404-run-2026-11-17.json",
        ],
        "research_validity": [
            root / "glossa-indus/STANDARDS.md",
            rec / "stage-3-record-2026-11-16.md",
            rec / "t303-identifiability-application-2026-11-16.md",
            root / "glossa-indus/ledger/claims.jsonl",
        ],
        "ux_review": [
            rec / "t404-thresholds-2026-11-17.md",
            rec / "t404-run-2026-11-17.json",
            rec / "t404-scoring-corrections.json",
        ],
        "backlog": [
            root / "glossa-indus/map/gap-register.md",
            rec / "t404-run-2026-11-17.json",
            spec095 / "tasks.md",
        ],
    }
    return {k: [p for p in v if p.is_file()] for k, v in candidates.items()}


def collect(root: Path) -> dict:
    """All facts and source lists the documents state."""
    spec095_tasks = root / "specs/095-red-team-remediation/tasks.md"
    return {
        "ledger": ledger_census(root),
        "anchors": anchors_census(root),
        "matrix": matrix_census(root),
        "program_map_nodes": program_map_nodes(root),
        "tasks095": task_states(spec095_tasks),
        "gaps": gap_entries(root),
        "corpus_keys": corpus_keys(root),
        "stage1_invalid": stage1_says_invalid(root),
        "audit": audit_facts(root),
        "sources": source_sets(root),
    }
