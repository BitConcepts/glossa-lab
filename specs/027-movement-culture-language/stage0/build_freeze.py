"""Build the Spec 027 Stage 0 freeze record (framework026 machinery).

Run from the repo root with the Glossa venv:
    python specs/027-movement-culture-language/stage0/build_freeze.py

Writes stage0-freeze.json next to stage0-freeze.md. A freeze is
never regenerated over a run: a changed gate is a new version
and a new freeze (Spec 026 section 4.7 / FR-027-12).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "backend"))

from glossa_lab.framework026 import build_freeze  # noqa: E402

DEFINITION = {
    "experiment_id": "spec027-phase391-stage0",
    "spec": "specs/027-movement-culture-language/spec.md",
    "freeze_doc": "specs/027-movement-culture-language/stage0-freeze.md",
    "script": "backend/scripts/phase391_stage0_spine.py",
    "graph_module": "backend/glossa_lab/experiment_graph_phase391_392.py",
    "phase": 391,
    "inputs": {
        "store": "corpora/downloads/spec027_stage0/ (gitignored)",
        "sha256": {
            "xronos_data.csv":
                "8570bfd9b256ced2f9e840183ea52325b9a7079b79a2957c7db797f09c118655",
            "cisi_vol1_catalogue.csv":
                "e0d698f991fbd7cf26c491a2b25906b422903a0e2a26ea7b8c690420ca51dc1e",
            "cisi_vol2_catalogue.csv":
                "e751244e2d51bda3181d98e56af691c0d24099d76d035b54f0888504204bc7d9",
            "mutin_moesm1.pdf":
                "b5eae7291aa6a1ebb643b381bbf848651f8bccde0f68ccb282e79ed977857600",
        },
    },
    "environment": {"python": "3.12.3",
                    "runner": "backend/scripts (venv glossa-lab)"},
}

SOURCES = [
    "specs/027-movement-culture-language/stage0-freeze.md",
    "specs/027-movement-culture-language/adjudication.md",
    "specs/027-movement-culture-language/spec.md",
    "backend/scripts/phase391_stage0_spine.py",
    "backend/glossa_lab/experiment_graph_phase391_392.py",
    "backend/tests/test_phase391_stage0_spine.py",
]

if __name__ == "__main__":
    record = build_freeze(DEFINITION, REPO, SOURCES)
    out = REPO / "specs/027-movement-culture-language/stage0-freeze.json"
    out.write_text(json.dumps(record, indent=1) + "\n",
                   encoding="utf-8")
    print(f"wrote {out} digest {record['digest']}")
