"""Phase-109 Step 1: staging-cohort re-review (spec 007).

Assembles in-repo evidence for the 116 research-loop staging
anchors (Phase-108 register: research_loop_heuristic component) and
applies the pre-registered rules: (a) KEEP on recorded independent
non-SA support, (b) RESTORE the prior sourced reading the staging
promotion overwrote, (c) DEMOTE one tier otherwise.

Modes: `decide` (default; writes reports/phase109_step1_decisions
.json, touches nothing) and `apply` (writes the anchors file and
appends to reports/phase109_change_register.json).

GPU: no compute; gpu_device recorded per H20 (torch guarded).
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

try:
    import torch  # noqa: F401
    _GPU = "cuda" if torch.cuda.is_available() else "cpu"
except ImportError:
    _GPU = "cpu (torch absent)"
print(f"[phase109-step1] gpu_device={_GPU}", file=sys.stderr)

from glossa_lab.pipelines import phase109_followthrough as p109  # noqa: E402

REPO = Path(__file__).parents[2]
OUT = REPO / "reports" / "phase109_step1_decisions.json"


def build_decisions() -> tuple[dict, dict, dict]:
    anchors_data = p109.load_anchors_file()
    records = p109.load_register()
    trails = p109.load_trails()
    backups = p109.load_backups()
    archive = p109.load_staging_archive()
    cohort = p109.staging_cohort(records)
    evidence: dict[str, dict] = {}
    decisions: list[dict] = []
    for sign in cohort:
        ev = p109.assemble_staging_evidence(
            sign, anchors_data, records, trails, backups, archive)
        evidence[sign] = ev
        d = p109.decide_staging(ev)
        d["current"] = ev["current"]
        d["snapshots"] = ev["snapshots"]
        decisions.append(d)
    counts = Counter(d["rule"] for d in decisions)
    payload = {
        "phase": 109, "step": 1, "spec": "specs/007-phase109-follow-through",
        "gpu_device": _GPU,
        "cohort_size": len(cohort),
        "counts": {r: counts.get(r, 0) for r in ("a", "b", "c")},
        "restorations": [
            {"sign": d["sign"],
             "from": {"reading": d["current"]["reading"],
                      "confidence": d["current"]["confidence"]},
             "to": {"reading": d["prior"]["reading"],
                    "confidence": d["prior"]["confidence"]},
             "prior_file": d["prior"]["file"]}
            for d in decisions if d["rule"] == "b"],
        "decisions": decisions,
    }
    return payload, evidence, anchors_data


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", nargs="?", default="decide",
                    choices=("decide", "apply"))
    args = ap.parse_args()
    payload, evidence, anchors_data = build_decisions()
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False),
                   encoding="utf-8")
    print(f"[phase109-step1] cohort={payload['cohort_size']} "
          f"counts={payload['counts']} -> {OUT.name}")
    if args.mode == "apply":
        reg = p109.load_change_register()
        changes = p109.apply_staging_decisions(
            anchors_data, payload["decisions"], evidence)
        p109.append_changes(reg, "step1", changes)
        p109.save_change_register(reg)
        p109.write_anchors_file(anchors_data)
        print(f"[phase109-step1] applied {len(changes)} changes; "
              "anchors + change register written")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
