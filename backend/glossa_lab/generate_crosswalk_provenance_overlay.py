"""Generate the crosswalk provenance overlay (repair WP4, 2026-10-26).

Runs ``crosswalk_provenance.build_overlay`` over the real crosswalk
and anchor table and writes
``data/mahadevan_parpola_crosswalk_v2_provenance.json`` next to this
script's package. The original crosswalk file is never modified.

Reproduce (from the repair staging tree, byte-verified copies of repo
HEAD d80dcb7c under ``work/``):

    ~/workspace/venvs/glossa-lab/bin/python \
      patch/backend/glossa_lab/generate_crosswalk_provenance_overlay.py

Input paths can be overridden with --crosswalk / --anchors /
--register / --rebase / --subset; the output path with --out. Input
SHA-256 digests are recorded in the overlay so the run is auditable.

Construction-input signs (classifier rule 3) are established here,
from the anchor records themselves, by either of two recorded facts:
the anchor entry's own ``source`` field names the Phase-51 crosswalk
route ("via_phase51"), or the Phase-108 provenance register's reasons
state the value was "imported via the Phase-51 crosswalk".
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from crosswalk_provenance import build_overlay  # noqa: E402

REPAIR = Path(__file__).resolve().parents[3]
WORK = REPAIR / "work"
DEFAULT_OUT = (Path(__file__).resolve().parent / "data"
               / "mahadevan_parpola_crosswalk_v2_provenance.json")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def construction_signs(anchors: dict, register_records: dict) -> set[str]:
    signs: set[str] = set()
    for sign, entry in anchors.items():
        if "via_phase51" in str(entry.get("source") or ""):
            signs.add(sign)
    for sign, rec in register_records.items():
        reasons = " ".join(rec.get("reasons") or [])
        if "imported via the Phase-51 crosswalk" in reasons:
            signs.add(sign)
    return signs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--crosswalk", type=Path, default=WORK / "backend"
                    / "glossa_lab" / "data"
                    / "mahadevan_parpola_crosswalk_v2.json")
    ap.add_argument("--anchors", type=Path, default=WORK / "backend"
                    / "reports" / "INDUS_FINAL_ANCHORS.json")
    ap.add_argument("--register", type=Path, default=WORK / "reports"
                    / "phase108_provenance_register.json")
    ap.add_argument("--rebase", type=Path, default=WORK / "reports"
                    / "phase109_rebase.json")
    ap.add_argument("--subset", type=Path, default=WORK / "reports"
                    / "phase108_subset_recomputation.json")
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = ap.parse_args()

    cw_data = _load(args.crosswalk)
    anchors = _load(args.anchors)["anchors"]
    register_records = _load(args.register)["records"]
    rebase = _load(args.rebase)
    subset = _load(args.subset)

    crosswalk = cw_data["crosswalk"]
    cons = construction_signs(anchors, register_records)
    named_sets = {
        "phase109_rebase_strict_compared": {
            d["sign"] for d in
            rebase["sets"]["sa_independent_strict"]["parpola"]["details"]},
        "phase108_subset_strict_compared": {
            d["sign"] for d in
            subset["sets"]["sa_independent_strict"]["parpola"]["details"]},
    }
    revision = (f"crosswalk {cw_data.get('version')}; "
                f"sha256:{_sha256(args.crosswalk)[:16]}")
    overlay = build_overlay(crosswalk, anchors, cons,
                            source_revision=revision,
                            named_sets=named_sets)
    overlay["inputs"] = {
        "crosswalk": {"path": str(args.crosswalk),
                      "sha256": _sha256(args.crosswalk),
                      "version_as_stated": cw_data.get("version")},
        "anchors": {"path": str(args.anchors),
                    "sha256": _sha256(args.anchors)},
        "register": {"path": str(args.register),
                     "sha256": _sha256(args.register)},
        "rebase": {"path": str(args.rebase),
                   "sha256": _sha256(args.rebase)},
        "subset_recomputation": {"path": str(args.subset),
                                 "sha256": _sha256(args.subset)},
        "construction_input_signs": sorted(cons),
        "construction_input_rule": "anchor source field names the "
        "Phase-51 crosswalk route ('via_phase51'), or the Phase-108 "
        "register reasons state the value was 'imported via the "
        "Phase-51 crosswalk'",
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(overlay, indent=2, ensure_ascii=False),
                        encoding="utf-8")
    s = overlay["summary"]
    print(f"entries: {s['n_entries']}")
    print(f"by classification: {s['by_classification']}")
    print(f"eligible: {s['n_eligible_for_independent_validation']}")
    for name, b in overlay["named_sets"].items():
        print(f"{name}: n={b['n_entries']} "
              f"eligible={b['n_eligible_for_independent_validation']} "
              f"{b['by_classification']}")
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
