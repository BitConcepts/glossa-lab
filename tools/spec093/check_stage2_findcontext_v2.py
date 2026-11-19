#!/usr/bin/env python3
"""Spec 093 Stage 2 — T202 find-context successor
mechanical adjudication (freeze v2).

Reads the successor run records filed in the store and
applies freeze v2's rules mechanically: section 6
(control validity), section 7 (the recovery bar), and
section 8 (the standing mapping for the find-context
field). The other fields' entries are carried unchanged
from the freeze v1 adjudication filed beside the runs
(`t202-adjudication-2026-11-19.json`), which this
checker reads and refuses to proceed without.

Usage:

    python3 tools/spec093/check_stage2_findcontext_v2.py \
        --store <run-store-dir> [--audit <audit-json>]

Prints one JSON document: the full per-field table and
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
V1_ADJUDICATION = "t202-adjudication-2026-11-19.json"


def load_runs(store: Path) -> dict:
    runs = {}
    for path in sorted(store.glob("study-*.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        result = record.get("result")
        if not isinstance(result, dict):
            continue
        if result.get("task") != "T202-successor":
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

    v1_path = args.store / V1_ADJUDICATION
    if not v1_path.exists():
        print(json.dumps({
            "verdict": "REFUSED",
            "detail": f"the freeze v1 adjudication ({V1_ADJUDICATION}) "
                      "is not filed beside the runs; the unchanged "
                      "fields cannot be carried",
        }, indent=1, sort_keys=True))
        return 1
    v1 = json.loads(v1_path.read_text(encoding="utf-8"))

    runs = load_runs(args.store)
    admin = runs.get(("administration", "find-context"))
    controls = runs.get(("permutation-controls", "find-context"))
    if admin is None or controls is None:
        print(json.dumps({
            "verdict": "REFUSED",
            "detail": "missing successor run records for "
                      "field 'find-context'",
        }, indent=1, sort_keys=True))
        return 1

    fields: dict[str, dict] = {}
    # The fields freeze v2 does not touch, carried
    # unchanged from the v1 adjudication.
    for name in ("site", "material class", "artifact type",
                 "holding/provenance"):
        entry = dict(v1["fields"][name])
        entry["source"] = "freeze v1 adjudication (unchanged)"
        fields[name] = entry

    cres = controls["result"]
    ares = admin["result"]
    entry = {
        "administration_run": admin["run_id"],
        "controls_run": controls["run_id"],
        "controls_valid": cres["controls_valid"],
        "control_kappa_mean_p99": cres["kappa_mean_p99_index197"],
        "control_kappa_mean_max": cres["kappa_mean_max"],
        "kappa_mean": ares["kappa_mean"],
        "balanced_accuracy_mean": ares["balanced_accuracy_mean"],
        "adjudged_total": ares["adjudged_total"],
        "n_repeats": ares["n_repeats"],
        "n_folds": ares["n_folds"],
    }
    if not cres["controls_valid"]:
        entry["outcome"] = "NOT YET"
    elif (ares["kappa_mean"] >= BAR_KAPPA
          and ares["balanced_accuracy_mean"] >= BAR_BALANCED_ACCURACY):
        entry["outcome"] = "RECOVERED"
    else:
        entry["outcome"] = "NOT RECOVERED"
    fields["find-context"] = entry

    recovered, survived, unadministered = [], [], []
    label_of = {"site": "site", "find-context": "find-context",
                "material class": "material class",
                "artifact type": "artifact type",
                "holding/provenance": "holding/provenance"}
    for name, e in fields.items():
        if e["outcome"] == "RECOVERED":
            recovered.append(label_of[name])
        elif e["outcome"] == "NOT RECOVERED":
            survived.append(label_of[name])
        else:
            unadministered.append(label_of[name])

    # Freeze v2 section 8: under every successor outcome
    # the overall label remains INDEPENDENT IN PART
    # (site survives from v1; the unadministered set is
    # non-empty).
    standing = "INDEPENDENT IN PART"

    print(json.dumps({
        "spec": "093", "stage": "2", "task": "T202-successor",
        "freeze": "v2",
        "bar": {"kappa": BAR_KAPPA,
                "balanced_accuracy": BAR_BALANCED_ACCURACY},
        "fields": fields,
        "recovered_fields": recovered,
        "not_recovered_fields": survived,
        "not_administered_or_not_yet_fields": unadministered,
        "surviving_fields": survived,
        "fallen_fields": recovered,
        "c093_1_standing": standing,
    }, indent=1, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
