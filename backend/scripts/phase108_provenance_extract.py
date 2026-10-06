"""Phase-108 Step 1: anchor provenance evidence extraction (spec 006).

Assembles, for every anchor in INDUS_FINAL_ANCHORS.json, its evidence
trail from in-repo sources ONLY: entry fields, both ledgers, phase
artifacts in reports/ + backend/reports/ + outputs/ +
glossa-indus/reports/, structured SA/injection/crosswalk extracts, and
claims citing the sign. Output: reports/phase108_anchor_trails.json.

GPU: no compute; gpu_device recorded per H20 (torch guarded).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

try:
    import torch  # noqa: F401
    _GPU = "cuda" if torch.cuda.is_available() else "cpu"
except ImportError:
    _GPU = "cpu (torch absent)"
print(f"[phase108-extract] gpu_device={_GPU}", file=sys.stderr)

from glossa_lab.pipelines.provenance_audit import (  # noqa: E402
    CHANGELOG, GLOSSA_LEDGER, ROOT_LEDGER, build_mention_index,
    build_trail, ledger_sections, load_anchors, sign_ledger_mentions)

REPO = Path(__file__).parents[2]
OUT = REPO / "reports" / "phase108_anchor_trails.json"


def main() -> int:
    anchors = load_anchors()["anchors"]
    index = build_mention_index()
    sections = []
    for path, tag in ((GLOSSA_LEDGER, "glossa-indus/LEDGER.md"),
                      (ROOT_LEDGER, "LEDGER.md"),
                      (CHANGELOG, "CHANGELOG.md")):
        for s in ledger_sections(path):
            s["source"] = tag
            sections.append(s)
    trails = {}
    for sign, entry in anchors.items():
        hits: list[dict] = []
        for s in sections:
            hits.extend(sign_ledger_mentions(sign, [s], s["source"]))
        trails[sign] = build_trail(sign, entry, index, hits)
    payload = {
        "phase": 108, "step": 1, "spec": "specs/006-anchor-provenance-audit",
        "gpu_device": _GPU, "n_anchors": len(trails),
        "sources": ["backend/reports/INDUS_FINAL_ANCHORS.json",
                    "glossa-indus/LEDGER.md", "LEDGER.md", "CHANGELOG.md",
                    "reports/*.json", "backend/reports/*.json",
                    "outputs/*.json", "glossa-indus/reports/**/*.json",
                    "glossa-indus/claims/extracted_claims/*.json",
                    "backend/glossa_lab/data/mahadevan_parpola_crosswalk_v2.json"],
        "trails": trails,
    }
    OUT.write_text(json.dumps(payload, indent=1, ensure_ascii=False),
                   encoding="utf-8")
    print(f"wrote {OUT} ({len(trails)} trails)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
