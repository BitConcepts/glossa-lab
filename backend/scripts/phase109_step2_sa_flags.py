"""Phase-109 Step 2: SA-lineage HIGH provenance flags (spec 007).

The 44 SA load-bearing anchors (Phase-108 register categories
SA_DERIVED + SA_CONFIRMED_ONLY, all HIGH) gain machine-readable
fields — validation_status="pending_non_sa_validation" and
provenance_class=<register category> — WITHOUT any change to
reading or confidence in this step.

Modes: `decide` (default; writes reports/phase109_step2_flags.json)
and `apply` (writes anchors + change register).

GPU: no compute; gpu_device recorded per H20 (torch guarded).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

try:
    import torch  # noqa: F401
    _GPU = "cuda" if torch.cuda.is_available() else "cpu"
except ImportError:
    _GPU = "cpu (torch absent)"
print(f"[phase109-step2] gpu_device={_GPU}", file=sys.stderr)

from glossa_lab.pipelines import phase109_followthrough as p109  # noqa: E402

REPO = Path(__file__).parents[2]
OUT = REPO / "reports" / "phase109_step2_flags.json"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", nargs="?", default="decide",
                    choices=("decide", "apply"))
    args = ap.parse_args()
    anchors_data = p109.load_anchors_file()
    records = p109.load_register()
    lineage = p109.sa_lineage_anchors(records)
    payload = {
        "phase": 109, "step": 2, "spec": "specs/007-phase109-follow-through",
        "gpu_device": _GPU,
        "n_flagged": len(lineage),
        "flags": [
            {"sign": s, "provenance_class": cat,
             "reading": anchors_data["anchors"][s].get("reading"),
             "confidence": anchors_data["anchors"][s].get("confidence"),
             "validation_status": "pending_non_sa_validation"}
            for s, cat in lineage.items()],
    }
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False),
                   encoding="utf-8")
    print(f"[phase109-step2] flagged={len(lineage)} -> {OUT.name}")
    if args.mode == "apply":
        reg = p109.load_change_register()
        changes = p109.apply_sa_flags(anchors_data, lineage)
        p109.append_changes(reg, "step2", changes)
        p109.save_change_register(reg)
        p109.write_anchors_file(anchors_data)
        print(f"[phase109-step2] applied {len(changes)} flags; "
              "anchors + change register written")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
