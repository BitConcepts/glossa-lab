"""Build the Spec 026 rerun freeze records (framework026 machinery).

One canonical freeze per rerun phase, digesting the rerun
contract + the phase script + the shared graph module. Run from
the repository root. A changed contract/script after a freeze
is a NEW freeze (never a regenerated digest over an old run) —
this builder refuses to overwrite an existing freeze file.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "backend"))
from glossa_lab.framework026 import build_freeze  # noqa: E402

SPEC_DIR = REPO / "specs" / "026-rcph-framework-transfer"
GRAPH = "backend/glossa_lab/experiment_graph_phase383_386.py"

PHASES = {
    "phase383": [
        "specs/026-rcph-framework-transfer/reruns/phase383-contract.md",
        "backend/scripts/phase383_pilot_rescoring.py",
        GRAPH,
    ],
    "phase384": [
        "specs/026-rcph-framework-transfer/reruns/phase384-contract.md",
        "backend/scripts/phase384_stage2_margins.py",
        GRAPH,
    ],
    "phase385": [
        "specs/026-rcph-framework-transfer/reruns/phase385-contract.md",
        "backend/scripts/phase385_g1_margins.py",
        GRAPH,
    ],
    "phase386": [
        "specs/026-rcph-framework-transfer/reruns/phase386-contract.md",
        "backend/scripts/phase386_replay_audit.py",
        GRAPH,
    ],
}


def main() -> int:
    for phase, rel_paths in PHASES.items():
        out = SPEC_DIR / "reruns" / f"{phase}-freeze.json"
        if out.exists():
            print(f"REFUSING to overwrite existing freeze: {out}")
            return 1
        record = build_freeze(
            definition={
                "experiment_id": f"spec026-{phase}",
                "contract": rel_paths[0],
                "script": rel_paths[1],
                "graph_module": rel_paths[2],
                "environment": {
                    "python": sys.version.split()[0],
                    "runner": "backend/scripts (venv glossa-lab)",
                },
            },
            root=REPO,
            source_paths=rel_paths,
        )
        out.write_text(json.dumps(record, indent=1), "utf-8")
        print(phase, "digest", record["digest"][:16], "->", out.name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
