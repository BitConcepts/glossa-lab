#!/usr/bin/env python3
"""Spec 093 Stage 2 — T202 mechanical adjudication.

Reads the Stage 2 run records filed in the store and
applies the freeze's rules mechanically:
`t202-freeze-v1.md` section 7 (control validity),
section 8 (the recovery bar), section 3 (the fields that
do not form, with their forcing counts), and section 9
(the standing rule mapping per-field outcomes to
C093-1's standing in spec.md section 5's vocabulary).

Usage:

    python3 tools/spec093/check_stage2.py \
        --store <run-store-dir> [--audit <audit-json>]

Prints one JSON document: the per-field outcomes and
C093-1's standing. With --audit, the checker refuses to
adjudge unless the audit document's verdict is AGREE.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

BAR_KAPPA = 0.80
BAR_BALANCED_ACCURACY = 0.85

#: Freeze section 3: the fields whose administrations do
#: not form, with the forcing counts the freeze states.
NOT_ADMINISTERED = {
    "material class": {
        "outcome": "NOT ADMINISTERED",
        "forcing_counts": (
            "adjudged classes 1 (Steatite 176); Clay 1 and "
            "Faience 1 under the class floor; 1 empty of 179 "
            "joined pairs"
        ),
    },
    "artifact type": {
        "outcome": "NOT ADMINISTERED",
        "forcing_counts": (
            "3,085 sequence-bearing records carrying exactly "
            "1 distinct value ('seal'); the join concurs "
            "('SEAL:S', 179 of 179)"
        ),
    },
    "holding/provenance": {
        "outcome": "NOT ADMINISTERED",
        "forcing_counts": (
            "sequence and holding copresence in the pinned "
            "snapshot: 0 records; the join pairs carry no "
            "holding on either side"
        ),
    },
}

ADMINISTERED = ("site", "find-context")


def load_runs(store: Path) -> dict:
    runs = {}
    for path in sorted(store.glob("study-*.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        result = record.get("result")
        if not isinstance(result, dict):
            continue
        if result.get("spec") != "093" or result.get("stage") != "2":
            continue
        runs[(result["kind"], result["field"])] = {
            "run_id": record["run"]["run_id"],
            "record_file": path.name,
            "result": result,
        }
    return runs


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--store", required=True, type=Path)
    parser.add_argument("--audit", type=Path)
    args = parser.parse_args(argv)

    if args.audit is not None:
        audit = json.loads(args.audit.read_text(encoding="utf-8"))
        if audit.get("verdict") != "AGREE":
            print(json.dumps({
                "verdict": "REFUSED",
                "detail": "the audit verdict is not AGREE; "
                          "adjudication does not proceed on "
                          "unaudited runs",
            }, indent=1, sort_keys=True))
            return 1

    runs = load_runs(args.store)
    fields: dict[str, dict] = {}
    recovered, survived, unadministered = [], [], []
    for name, entry in NOT_ADMINISTERED.items():
        fields[name] = dict(entry)
        unadministered.append(name)
    not_yet = []
    for field in ADMINISTERED:
        admin = runs.get(("administration", field))
        controls = runs.get(("permutation-controls", field))
        if admin is None or controls is None:
            print(json.dumps({
                "verdict": "REFUSED",
                "detail": f"missing run records for field {field!r}",
            }, indent=1, sort_keys=True))
            return 1
        m = admin["result"]["metrics"]
        entry = {
            "administration_run": admin["run_id"],
            "controls_run": controls["run_id"],
            "controls_valid": controls["result"]["controls_valid"],
            "control_kappa_p99": controls["result"]["kappa_p99_index197"],
            "held_out_n": m["n_held_out"],
            "kappa": m["kappa"],
            "balanced_accuracy": m["balanced_accuracy"],
            "accuracy": m["accuracy"],
        }
        if not controls["result"]["controls_valid"]:
            entry["outcome"] = "NOT YET"
            not_yet.append(field)
        elif m["kappa"] >= BAR_KAPPA and m["balanced_accuracy"] >= BAR_BALANCED_ACCURACY:
            entry["outcome"] = "RECOVERED"
            recovered.append(field)
        else:
            entry["outcome"] = "NOT RECOVERED"
            survived.append(field)
        fields[field] = entry

    unadministered += not_yet
    if not recovered and not unadministered:
        standing = "INDEPENDENT AT FULL STRENGTH"
    elif not survived and not unadministered and recovered:
        standing = "NOT INDEPENDENT"
    else:
        standing = "INDEPENDENT IN PART"

    print(json.dumps({
        "spec": "093", "stage": "2", "task": "T202",
        "bar": {"kappa": BAR_KAPPA,
                "balanced_accuracy": BAR_BALANCED_ACCURACY},
        "fields": fields,
        "recovered_fields": recovered,
        "not_recovered_fields": survived,
        "not_administered_or_not_yet_fields": unadministered,
        "c093_1_standing": standing,
    }, indent=1, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
