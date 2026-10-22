"""Build the Spec 026 v2 freeze records (Phases 384/385).

Separate builder so the v1 records and their builder stay
byte-identical. Refuses to overwrite an existing freeze.
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
    "phase384": [
        "specs/026-rcph-framework-transfer/reruns/phase384-contract-v2.md",
        "backend/scripts/phase384_stage2_margins_v2.py",
        GRAPH,
    ],
    "phase385": [
        "specs/026-rcph-framework-transfer/reruns/phase385-contract-v2.md",
        "backend/scripts/phase385_g1_margins_v2.py",
        GRAPH,
    ],
}


def main() -> int:
    for phase, rel_paths in PHASES.items():
        out = SPEC_DIR / "reruns" / f"{phase}-freeze-v2.json"
        if out.exists():
            print(f"REFUSING to overwrite existing freeze: {out}")
            return 1
        record = build_freeze(
            definition={
                "experiment_id": f"spec026-{phase}-v2",
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
        print(phase, "v2 digest", record["digest"][:16], "->", out.name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
