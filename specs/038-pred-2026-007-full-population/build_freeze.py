#!/usr/bin/env python3
"""Build the Spec 038 freeze record (freeze.json).

This builder computes the DRAFT digest over the
draft contract under the owner's draft order of
2026-10-20 (adjudication.md). At the freeze act —
on the owner's separate freeze order, after the
AEE lifecycle hooks pass over the recovered
register under aee 1.5.0 (DD-038-7) — it is re-run
to compute the final digest over the frozen
contract exactly once, and its DEFINITION text is
finalised in the same act (the Spec 035/036
pattern). Run with the Glossa backend venv python
from the repository root:

    python specs/038-pred-2026-007-full-population/build_freeze.py

Writes specs/038-pred-2026-007-full-population/freeze.json
(framework026 build_freeze payload: definition +
source hashes + environment, digest = SHA-256 of
the canonical JSON serialisation) and prints the
digest.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "backend"))

from glossa_lab.framework026 import build_freeze  # noqa: E402

SPEC_DIR = "specs/038-pred-2026-007-full-population"

DEFINITION = {
    "spec": "specs/038-pred-2026-007-full-population/spec.md",
    "freeze_doc": "specs/038-pred-2026-007-full-population/freeze.md",
    "experiment_id": "spec038-pred-2026-007-full-population",
    "register": {
        "path": "specs/038-pred-2026-007-full-population/claims.json",
        "register_version": "0.5-draft",
        "claims": 14,
        "aee_hook_pass": (
            "NOT RUN on this draft: the AEE lifecycle "
            "hooks (after_specify / after_plan / "
            "after_tasks) are a freeze gate, run at the "
            "freeze act over the recovered register "
            "UNDER aee 1.5.0 (adoption in flight; "
            "DD-038-7; see "
            "specs/038-pred-2026-007-full-population/aee/"
            "freeze-aee-note.md)"
        ),
    },
    "basis": {
        "adjudication": (
            "specs/038-pred-2026-007-full-population/adjudication.md"
        ),
        "decisions": (
            "The owner's draft order of 2026-10-20 "
            "commissions this draft only (D-31 will be "
            "frozen for execution; this step drafts). "
            "No freeze order and no execution order "
            "exist for this contract. The freeze "
            "coordinator's three Stage-0 flags are "
            "disposed of in adjudication.md section 3 "
            "(DD-038-1 mechanical verdict rule, no "
            "pre-written outcome; DD-038-9 cluster-class "
            "operationalisation; DD-038-5 named sources "
            "and conflict rule). DD-038-6 is an open "
            "proposal for the freeze decision (file the "
            "frozen spec's own OSF contract "
            "registration). The contract implemented "
            "is design D-31 (PR #195) for the "
            "PRED-2026-007 registration "
            "(docs/PREDICTION_REGISTER.md, registered "
            "2026-04-22)."
        ),
    },
    "design": {
        "phase": "Phase-401 (provisional, DD-038-8)",
        "question_owner": (
            "docs/PREDICTION_REGISTER.md PRED-2026-007 "
            "(H4: ICIT Function Alignment)"
        ),
        "registered_prediction": (
            "Signs with ICIT function code ITM will "
            "cluster into TERMINAL class in CGSA "
            "Phase 5 at rate >= 70%."
        ),
        "criterion": {
            "verbatim": (
                ">= 70% of ITM-coded signs are TERMINAL "
                "or cluster in TERMINAL clusters"
            ),
            "share_min": 0.7,
            "verdict_rule": (
                "mechanical: the share of enumerated ITM "
                "signs counting as TERMINAL over the "
                "denominator the coverage rule fixes, "
                "against the 70% bar; CONFIRMED at or "
                "above, NOT CONFIRMED below; no band; "
                "no pre-written outcome for any branch "
                "(DD-038-1)"
            ),
            "recorded_partial_test": (
                "P385 (ITM) Cluster 21 TERMINAL; P378 "
                "(ITM) Cluster 39 TERMINAL; P098 (LOG) "
                "Cluster 10 INITIAL; recorded rate 2/3 "
                "(67%) - a pre-execution record whose "
                "denominator mixed in a non-ITM sign; "
                "outcome PARTIALLY CONFIRMED"
            ),
        },
        "population": {
            "unit": "distinct sign, by sign ID",
            "frame": (
                "every distinct sign whose function code "
                "in the primary source is exactly ITM; "
                "no sample, no frequency threshold, no "
                "attestation requirement"
            ),
            "excluded_by_rule": (
                "P098 (LOG) and every sign coded other "
                "than ITM, or uncoded"
            ),
            "status_at_draft": (
                "NOT enumerated: membership and size are "
                "execution-time facts (step 0, check 0.2)"
            ),
        },
        "sources": {
            "primary_function_code": {
                "file": "reports/indus_cgsa_cluster_analysis.json",
                "field": "data.a[].icit_function",
                "records": 611,
                "sha256": (
                    "8c2bd6059a671068b645204db37e29ff13ca53009117b9447ed6c7bd1ead02b3"
                ),
            },
            "cross_check_function_code": {
                "file": "data/crosswalks/canonical_sign_registry.csv",
                "field": "icit_function",
                "sha256": (
                    "8a0b2a82ac8d226d574ce01f5550c581efd91a97cab86201a62f7a7e435bd420"
                ),
            },
            "conflict_rule": (
                "the primary governs membership; every "
                "cross-check disagreement is recorded "
                "sign-by-sign and published; ambiguity "
                "or internal conflict within the primary "
                "closes the study as CANNOT BE RUN AS "
                "WRITTEN (DD-038-5)"
            ),
            "provenance_lineage": (
                "backend/glossa_lab/data/fuls_parser.py "
                "reads the function codes (NUM, LON, SHN, "
                "TMK, ITM, LOG, SYL) from Wells-derived "
                "catalog lines; the register's 'from "
                "mayig features' line is reconciled by "
                "appended note, never edited (DD-038-2)"
            ),
        },
        "phase5_output": {
            "assignment": {
                "file": "outputs/analysis/sign_clusters.json",
                "sha256": (
                    "623a787dd9cc93c4d3d36377890c4753e3427f57cf7ad70adcd6e8256ba1394a"
                ),
                "best_k": 40,
                "signs_clustered": 160,
            },
            "cluster_class_rule": (
                "DD-038-9 (disclosed operationalisation): "
                "a cluster's class is the class recorded "
                "for that cluster in "
                "reports/cluster_characterization.md "
                "(sha256 "
                "54ebf660873fd853a64ce91c7e30d8c4cedc5bc3a0a1555db1f6281a52e3c476); "
                "no recorded rule assigning classes to "
                "clusters has been located; no class is "
                "derived from rates at execution; a "
                "cluster with no recorded class leaves "
                "its signs unassigned under the coverage "
                "rule"
            ),
            "corroboration": (
                "reports/cgsa_validation_report.md "
                "(2026-04-22): best k 40, largest cluster "
                "12/160, entropy reduction 0.3204"
            ),
            "no_reclustering": (
                "scoring reads the recorded output only; "
                "if it does not survive in sign-assignable "
                "form the study closes as CANNOT BE RUN "
                "AS WRITTEN; a fresh clustering is a new "
                "prediction's business"
            ),
            "sanity_anchor": {
                "P385": 21,
                "P378": 39,
                "P098": 10,
            },
        },
        "step0": {
            "order": [
                "sources and provenance (primary and "
                "cross-check verified and hashed; "
                "conflict rule in force; reconciliation "
                "note drafted for append)",
                "enumeration (mechanical read of the "
                "primary's icit_function field over all "
                "611 records; record-count "
                "reconciliation; cross-check run; the "
                "enumeration written and hashed before "
                "any Phase 5 lookup)",
                "Phase 5 output verification (recorded "
                "output in sign-assignable form; the "
                "sanity anchor reproduced)",
            ],
            "failure_closure": (
                "CANNOT BE RUN AS WRITTEN, unscored, "
                "reported as a closure and never as a "
                "verdict; the census branch is a "
                "completion, not a closure"
            ),
        },
        "coverage_rule": {
            "denominator": (
                "the assigned population when some "
                "enumerated signs have no recorded "
                "Phase 5 assignment, with coverage "
                "stated in the verdict's first sentence"
            ),
            "decisiveness_exception": (
                "if the unassigned signs cannot change "
                "the outcome arithmetically, the verdict "
                "is decisive and coverage is still stated"
            ),
            "floor": 0.8,
            "below_floor": (
                "coverage below 80% and not "
                "arithmetically decisive: the appended "
                "entry records the test as "
                "run-at-partial-scope with the numbers"
            ),
            "provenance": (
                "the design's rule (D-31), not the "
                "register's (DD-038-4)"
            ),
        },
        "census_branch": (
            "if the enumerated population is exactly "
            "the ITM signs already tested, the design "
            "closes with the census as its finding: a "
            "completion, scored by the mechanical "
            "verdict rule; no outcome is pre-written "
            "for this branch (DD-038-1)"
        ),
        "register_handling": (
            "dated section 6 appends only (the outcome "
            "entry and the provenance reconciliation "
            "note); the registered section 3 text is "
            "never edited; every other prediction's "
            "entry stays byte-identical; on a step-0 "
            "closure the section 3 Outcome stays "
            "PARTIALLY CONFIRMED as the pre-execution "
            "record"
        ),
        "execution_gate": (
            "NOT satisfied: no freeze order and no "
            "execution order exist for this contract; "
            "the freeze and the execution (Phase-401, "
            "provisional) are separate future owner "
            "decisions; this draft performs neither and "
            "enumerates nothing"
        ),
    },
    "inputs": {
        "pred_register": {
            "file": "docs/PREDICTION_REGISTER.md",
            "sha256": (
                "548b13f22eabd1f10280d1544533b440f6d317977be2b26da6a0b4abd9de159c"
            ),
            "entry": "PRED-2026-007 (registered 2026-04-22)",
        },
        "design_source": {
            "file": (
                "docs/research/experiment-designs-2026-10-13/"
                "05-predictions.md (PR #195, D-31)"
            ),
            "branch": "designs/035-open-questions",
            "commit": "43f56191",
        },
        "sign_inventory": {
            "file": "docs/research/SIGN_INVENTORY.md",
            "sha256": (
                "c8e588327291896abe92e732fb85a9e02ed2ee8c3ad08fc18087bf6474e49db5"
            ),
        },
        "fuls_parser": {
            "file": "backend/glossa_lab/data/fuls_parser.py",
            "sha256": (
                "9b57f0ecc10905c0746f1e7fb8e0622ac18e3b08e62bb2eb34fbec4bbd8ef615"
            ),
        },
    },
    "environment": {
        "python": "3.12.3",
        "runner": "backend (venv glossa-lab)",
        "aee": (
            "1.5.0 at the freeze gate (adoption in "
            "flight; DD-038-7); hooks NOT RUN on this "
            "draft"
        ),
        "specify": "1.0.10",
    },
}

SOURCES = [
    f"{SPEC_DIR}/freeze.md",
    f"{SPEC_DIR}/spec.md",
    f"{SPEC_DIR}/claims.json",
    f"{SPEC_DIR}/adjudication.md",
    f"{SPEC_DIR}/osf-registration.md",
    f"{SPEC_DIR}/aee/freeze-aee-note.md",
    f"{SPEC_DIR}/build_freeze.py",
    "backend/tests/test_spec038_freeze.py",
]


def main() -> int:
    record = build_freeze(DEFINITION, REPO, SOURCES)
    out = REPO / SPEC_DIR / "freeze.json"
    out.write_text(
        json.dumps(record, indent=1) + "\n", encoding="utf-8"
    )
    print(record["digest"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
