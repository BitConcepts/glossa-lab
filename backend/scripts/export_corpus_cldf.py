"""Export the anchored Indus corpus as a CLDF-style forms.csv.

Produces ``backend/reports/corpus_cldf_export.csv`` with header:
  ID,Language_ID,Parameter_ID,Form,Gloss,Source,Confidence

NOTE: This script is a standalone utility.  It is NOT registered as a graph
node.  Registering it would require the H23 5-step gate process, which is
out of scope for the initial project-config layer.

Usage::

    python -m scripts.export_corpus_cldf          # from backend/
    python backend/scripts/export_corpus_cldf.py  # from repo root
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from typing import Any


def run(*, max_iterations: int = 100_000) -> dict[str, Any]:
    """Export anchored corpus tokens as CLDF forms.csv.

    Parameters
    ----------
    max_iterations:
        Hard cap on the total number of tokens processed (H11 compliance).

    Returns
    -------
    dict with ``total_tokens``, ``anchored_tokens``, ``dedr_linked_tokens``,
    and ``output_path``.
    """
    # ── Resolve paths via project config ──────────────────────────────────
    try:
        from glossa_lab.config import get_project_config  # noqa: PLC0415
        cfg = get_project_config()
        anchors_path = cfg.anchors_json_path()
        corpus_path = cfg.corpus_csv_path()
        project_id = cfg.project_id
    except Exception:
        _repo = Path(__file__).resolve().parents[2]
        anchors_path = _repo / "backend" / "reports" / "INDUS_FINAL_ANCHORS.json"
        corpus_path = (
            _repo
            / "corpora"
            / "downloads"
            / "external_repos"
            / "holdatllc_indus"
            / "indus_corpus 2.csv"
        )
        project_id = "indus"

    # ── Load anchors ─────────────────────────────────────────────────────
    anchors: dict[str, dict[str, Any]] = {}
    if anchors_path.exists():
        raw = json.loads(anchors_path.read_text(encoding="utf-8"))
        anchors = raw.get("anchors", {})

    # ── Load corpus sequences ────────────────────────────────────────────
    inscriptions: list[list[str]] = []
    if corpus_path.exists():
        from collections import defaultdict  # noqa: PLC0415

        seals: dict[str, list[dict[str, str]]] = defaultdict(list)
        with open(corpus_path, encoding="utf-8") as f:
            for row in csv.DictReader(f):
                seals[row["cisi_number"]].append(row)
        for rows in seals.values():
            rows_s = sorted(rows, key=lambda r: int(r.get("position") or 0))
            signs = [r["letters"] for r in rows_s if r.get("letters")]
            if signs:
                inscriptions.append(signs)

    # ── Build CLDF rows ──────────────────────────────────────────────────
    output_rows: list[list[str]] = []
    total_tokens = 0
    anchored_tokens = 0
    dedr_linked_tokens = 0
    iteration = 0

    for insc_idx, seq in enumerate(inscriptions):
        for pos, sign_id in enumerate(seq):
            iteration += 1
            if iteration > max_iterations:
                break

            total_tokens += 1
            anchor = anchors.get(sign_id, {})
            reading = anchor.get("reading", "")
            dedr = anchor.get("dedr", "")
            confidence = anchor.get("confidence", "UNKNOWN")

            is_anchored = bool(reading)
            is_dedr = bool(dedr)
            if is_anchored:
                anchored_tokens += 1
            if is_dedr:
                dedr_linked_tokens += 1

            output_rows.append([
                f"{insc_idx}_{pos}",           # ID
                project_id.capitalize(),        # Language_ID
                str(dedr) if dedr else "",      # Parameter_ID
                sign_id,                        # Form
                reading if is_anchored else "", # Gloss
                "INDUS_FINAL_ANCHORS",          # Source
                confidence,                     # Confidence
            ])
        else:
            continue
        break  # break outer loop if max_iterations reached

    # ── Write output ─────────────────────────────────────────────────────
    _repo_root = Path(__file__).resolve().parents[2]
    output_path = _repo_root / "backend" / "reports" / "corpus_cldf_export.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            ["ID", "Language_ID", "Parameter_ID", "Form", "Gloss", "Source", "Confidence"]
        )
        writer.writerows(output_rows)

    summary = {
        "total_tokens": total_tokens,
        "anchored_tokens": anchored_tokens,
        "dedr_linked_tokens": dedr_linked_tokens,
        "output_path": str(output_path),
    }

    print(f"Total tokens:       {total_tokens}")
    print(f"Anchored tokens:    {anchored_tokens}")
    print(f"DEDR-linked tokens: {dedr_linked_tokens}")
    print(f"Output:             {output_path}")

    return summary


if __name__ == "__main__":
    # Allow overriding max_iterations from CLI for testing
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 100_000
    run(max_iterations=limit)
