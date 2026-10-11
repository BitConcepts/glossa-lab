"""Phase-386 (Spec 026) — replay comparator for the REPRODUCE-ONLY chain.

Rerun contract: specs/026-rcph-framework-transfer/reruns/
phase386-contract.md (frozen at the S3 merge; freeze record
phase386-freeze.json). The four original scripts (Phases 116,
125, 127, 131) are re-executed in a disposable worktree (see the
contract's mechanics paragraph); this comparator reads the
committed results file and the replayed results file for each
item and compares the declared headline quantities.

Outcomes per item: REPRODUCED (all quantities within tolerance),
DRIFT (a quantity differs — both values reported), or NOT
REPRODUCIBLE (replayed file absent — the reason is recorded by
the operator in the run report; the comparator marks the item
from the missing file, never invents values).
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT = REPO_ROOT / "reports" / "phase386_results.json"

# item -> (committed path, replayed path template, [(json path, recorded, tol)])
ITEMS = {
    "PHASE-116": {
        "file": "reports/phase116_harmonization_results.json",
        "quantities": [
            ("arms/definition/median_w1", 0.4519, 5e-4),
            ("arms/definition/spearman_mean_r", -0.0826, 5e-4),
        ],
    },
    "PHASE-125": {
        "file": "reports/phase125_cross_compilation_results.json",
        "quantities": [
            ("arms/primary/stats/median_tv", 0.636931, 5e-7),
            ("arms/primary/stats/n_judgeable", 16, 0),
            ("arms/primary/stats/null/n_null_median_le_observed", 823, 0),
        ],
    },
    "PHASE-127": {
        "file": "reports/phase127_cross_compilation_diagnostic_results.json",
        "quantities": [
            ("phase125_verdict_of_record/median_tv", 0.636931, 5e-7),
            ("arms/b_matched_size/median_tv_distribution/ci95_lo", 0.046665, 5e-7),
            ("arms/b_matched_size/median_tv_distribution/ci95_hi", 0.131316, 5e-7),
            ("arms/b_matched_size/median_tv_distribution/share_replicates_ge_observed", 0.0, 0),
            ("arms/c_bootstrap/median_tv/ci95_lo", 0.548638, 5e-7),
            ("arms/c_bootstrap/median_tv/ci95_hi", 0.722042, 5e-7),
        ],
    },
    "PHASE-131": {
        "file": "reports/phase131_attribution_results.json",
        "quantities": [
            ("arms/d_synthesis/sum_credited_shares", 0.061321, 5e-7),
            ("arms/d_synthesis/residual_unexplained_share", 0.938679, 5e-7),
        ],
    },
}


def _dig(doc: dict, path: str):
    cur = doc
    for part in path.split("/"):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


def compare_item(item_id: str, committed_doc: dict, replayed_doc: dict | None,
                 quantities: list[tuple[str, float, float]]) -> dict:
    if replayed_doc is None:
        return {"item": item_id, "outcome": "NOT REPRODUCIBLE",
                "reason": "replayed results file absent"}
    checks = []
    outcome = "REPRODUCED"
    for path, recorded, tol in quantities:
        got = _dig(replayed_doc, path)
        rec = _dig(committed_doc, path)
        ok = (
            isinstance(got, (int, float)) and isinstance(rec, (int, float))
            and abs(float(got) - float(rec)) <= tol
            and abs(float(rec) - recorded) <= max(tol, 5e-4)
        )
        checks.append({"quantity": path, "committed": rec,
                       "replayed": got, "within_tolerance": bool(ok)})
        if not ok:
            outcome = "DRIFT"
    return {"item": item_id, "outcome": outcome, "checks": checks}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--replayed-root", type=Path, required=True,
                    help="root of the disposable worktree where the "
                         "original scripts were re-executed")
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = ap.parse_args()

    items = []
    for item_id, spec in ITEMS.items():
        committed_path = REPO_ROOT / spec["file"]
        replayed_path = args.replayed_root / spec["file"]
        committed = json.loads(committed_path.read_text("utf-8"))
        replayed = (
            json.loads(replayed_path.read_text("utf-8"))
            if replayed_path.exists() else None
        )
        items.append(compare_item(item_id, committed, replayed,
                                  list(spec["quantities"])))
        print(item_id, items[-1]["outcome"])

    results = {
        "phase": "Phase-386",
        "spec": "026",
        "reruns": "Phases 116/125/127/131 — deterministic replay audit",
        "contract": "specs/026-rcph-framework-transfer/reruns/phase386-contract.md",
        "replayed_root": str(args.replayed_root),
        "items": items,
        "ai_disclosure": (
            "Executed by an AI agent (Muse Spark, via Muse) "
            "at the direction of Tristen Pierson, per constitution sec.VI."
        ),
    }
    args.out.write_text(json.dumps(results, indent=1), "utf-8")
    print("wrote", args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
