#!/usr/bin/env python3
"""Build the Spec 040 freeze record (freeze.json).

This builder computes the DRAFT digest over the
draft contract under the owner's bundle decision
of 2026-10-20 (adjudication.md). At the freeze
act - on the owner's separate freeze order, after
spec section 1's dependency gate is verified
against the executed Spec 039 record and the AEE
lifecycle hooks pass over the recovered register -
it is re-run to compute the final digest over the
frozen contract exactly once, and its DEFINITION
text is finalised in the same act (the Spec 035
pattern): the dependency block's placeholders are
replaced by the Spec 039 artifact's path, version,
and SHA-256, and the phase block by the allocated
execution phase number. Run with the Glossa
backend venv python from the repository root:

    python specs/040-d25-g1-chronology-controlled/build_freeze.py

Writes specs/040-d25-g1-chronology-controlled/freeze.json
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

SPEC_DIR = "specs/040-d25-g1-chronology-controlled"

DEFINITION = {
    "spec": "specs/040-d25-g1-chronology-controlled/spec.md",
    "freeze_doc": "specs/040-d25-g1-chronology-controlled/freeze.md",
    "experiment_id": "spec040-d25-g1-chronology-controlled",
    "register": {
        "path": "specs/040-d25-g1-chronology-controlled/claims.json",
        "register_version": "0.5-draft",
        "claims": 15,
        "aee_hook_pass": (
            "NOT RUN on this draft: the AEE lifecycle "
            "hooks (after_specify / after_plan / "
            "after_tasks) are a freeze gate, run at the "
            "freeze act over the recovered register "
            "(the Spec 035 ordering; see "
            "specs/040-d25-g1-chronology-controlled/aee/"
            "freeze-aee-note.md)"
        ),
    },
    "basis": {
        "adjudication": (
            "specs/040-d25-g1-chronology-controlled/adjudication.md"
        ),
        "decisions": (
            "The owner's decisions of 2026-10-20 "
            "commission this draft and fix its basis: "
            "the gazetteer period-assignment act "
            "(Spec 039) and D-25 are authorised as a "
            "bundle with the act first, and the act's "
            "evidence standard is published period "
            "determinations only. No freeze order and "
            "no execution order exist for this "
            "contract. The design implemented is D-25 "
            "of the PR #195 experiment-design packet "
            "over the Spec 025 / Phase-140 / "
            "Phase-385 record of claim "
            "STUDY-SPEC-025/G1."
        ),
    },
    "design": {
        "phase": (
            "UNASSIGNED at draft (DD-040-10): allocated "
            "at the freeze act; Phase-400 is Spec 036's "
            "and Phase-401 is claimed by the Spec 037 "
            "and Spec 038 drafts"
        ),
        "claim_under_test": "STUDY-SPEC-025/G1",
        "design_source": (
            "D-25, docs/research/experiment-designs-"
            "2026-10-13/04-study-headlines.md (PR #195)"
        ),
        "question": (
            "When inscriptions are compared only "
            "against inscriptions from the same coarse "
            "period, with composition and preservation "
            "still held fixed, does the G1 site "
            "association stay clearly above the "
            "V = 0.10 practical margin?"
        ),
        "dependency_gate": {
            "state_at_draft": (
                "NOT SATISFIED: Spec 039 has not "
                "executed; the gazetteer assignment "
                "column is empty on every published "
                "Stage 0 row"
            ),
            "requires": [
                "Spec 039 executed, with its freeze "
                "digest and outcome merged and named in "
                "Spec 040's freeze record",
                "a frozen machine-readable "
                "period-assignment artifact, SHA-256 "
                "pinned in Spec 040's freeze record, "
                "resolving G1 inscriptions at "
                "site-period resolution",
                "every non-UNASSIGNED assignment "
                "carrying its published source citation "
                "and locator, the mapping rule applied, "
                "and its contested flag",
                "published period determinations only: "
                "no program-derived dates-to-period "
                "inference (the owner's 2026-10-20 "
                "evidence standard)",
            ],
            "failure_state": (
                "NOT-YET-TESTABLE - dependency gate; "
                "the freeze does not proceed"
            ),
            "spec039_artifact": {
                "path": "PENDING - named at the freeze act",
                "version": "PENDING - named at the freeze act",
                "sha256": "PENDING - named at the freeze act",
            },
        },
        "period_assignment": {
            "labels": ["EARLY", "MATURE", "LATE"],
            "key": (
                "site x the inscription's recorded local "
                "chronological label(s), per the frozen "
                "Spec 039 artifact"
            ),
            "primary_rule": (
                "a unique uncontested mapping places the "
                "inscription; missing, ambiguous, "
                "transitional, or contested-only "
                "mappings leave it UNASSIGNED and "
                "excluded from the primary, counted"
            ),
            "forbidden_placements": [
                "site-level occupation label inheritance",
                "a radiocarbon determination for the site",
                "the Phase-139 chron_band harmonization",
                "analyst judgement at execution time",
            ],
            "contested": (
                "excluded from the primary; included in "
                "the labelled sensitivity under the "
                "sensitivity labels Spec 039 froze, or "
                "the sensitivity is NOT ESTIMABLE for "
                "the affected mappings"
            ),
        },
        "margins_gate": {
            "sites_per_period_min": 5,
            "periods_required": ["EARLY", "MATURE", "LATE"],
            "unassigned_share_max": 0.4,
            "permutable_min": 1000,
            "permutable_arm_status": (
                "DD-040-6, proposed at draft: carried "
                "from Spec 025's covariate-gate floor"
            ),
            "failure_state": (
                "NOT-YET-TESTABLE, margins stated, no "
                "outcome quantity computed (D-25's "
                "source wording: INCONCLUSIVE-BY-DESIGN; "
                "the governing word is DD-040-5, "
                "proposed at draft)"
            ),
        },
        "primary_test": {
            "population": (
                "the Phase-137 F3 population reproduced "
                "by rule (7 eligible sites, 5,410 "
                "inscriptions), restricted to the "
                "assigned inscriptions of the assignment "
                "discipline"
            ),
            "profile_columns": (
                "fixed from the full base population "
                "(layer-wide count at least 10; rarer "
                "pooled to OTHER; placeholders 000/999 "
                "excluded); never re-derived on the "
                "assigned subset (DD-040-4)"
            ),
            "statistic": (
                "Pearson chi-square of the site x sign "
                "profile table; Cramer's V and per-site "
                "total-variation distances descriptive"
            ),
            "strata": (
                "composition_stratum | preservation_class "
                "| period_stratum"
            ),
            "permutation": {
                "B": 9999,
                "seed": 20261009,
                "p_formula": (
                    "(1 + #{chi2_perm >= chi2_obs}) / (1 + B)"
                ),
                "role": (
                    "reported with the outcome; not the "
                    "verdict rule (DD-040-1)"
                ),
            },
            "interval": {
                "estimator": (
                    "Phase-385 v2: stratified bootstrap of "
                    "inscriptions within the primary "
                    "strata, stratum sizes preserved"
                ),
                "B": 4999,
                "seed": 20261012,
                "governing": (
                    "basic bootstrap interval "
                    "[2V - q97.5, 2V - q2.5] for Cramer's V"
                ),
                "also_reported": "percentile interval",
            },
            "margin_v": 0.1,
        },
        "decision_rules": {
            "rule_source": (
                "DD-040-1, proposed at draft: the "
                "interval-at-margin rule of D-25 and "
                "Phase-385, re-derived in place of Spec "
                "025's permutation-p-only verdict rule"
            ),
            "supported": (
                "governing interval entirely above 0.10: "
                "SUPPORTED - CHRONOLOGY CONTROLLED; the "
                "rider is retired by appended record"
            ),
            "weakened": (
                "governing interval straddles 0.10: "
                "WEAKENED - RIDER CONFIRMED AS MATERIAL; "
                "G1 restated as a period-confounded "
                "association by appended record"
            ),
            "contradicted": (
                "governing interval entirely at or below "
                "0.10: CONTRADICTED AT THE DECLARED "
                "MARGIN; the chronology-controlled form "
                "of G1 is defeated at the margin"
            ),
        },
        "sensitivities": [
            "contested-included, under the frozen "
            "sensitivity labels (spec section 8.1)",
            "leave-one-site-out over every analysis "
            "site (spec section 8.2)",
            "drop-Harappa, named in the headline "
            "sensitivity paragraph or NOT APPLICABLE "
            "recorded (spec section 8.3)",
            "recorded companions, not recomputed: the "
            "Phase-140 primary and the Phase-385 "
            "interval; Spec 025's EXPLORATORY S-chron "
            "interval (spec section 8.4)",
        ],
        "regression": (
            "before the primary, the composition-only "
            "and composition x preservation "
            "configurations reproduce the Phase-137 "
            "and Phase-140 records exactly; any "
            "mismatch stops the run as INVALID"
        ),
        "execution_gate": (
            "NOT satisfied: no freeze order and no "
            "execution order exist for this contract, "
            "and the freeze itself is barred until the "
            "dependency gate is satisfied; this draft "
            "performs neither, joins no label, computes "
            "no margin, and calculates no repertoire "
            "quantity"
        ),
    },
    "inputs": {
        "layer": {
            "file": "horus84 inscriptions.csv (ICIT-lineage layer)",
            "sha256": (
                "c368f290d8d784093d804243100de27ae6ad09df3ae37cab7432a0205d4ec9ef"
            ),
            "population_rows": 5410,
            "eligible_sites": [
                "Chanhu-daro", "Dholavira", "Harappa",
                "Kalibangan", "Lothal", "Mohenjo-daro",
                "Nausharo",
            ],
        },
        "covariates": {
            "file": (
                "data/evidence_integration/"
                "phase139_harmonized_covariates.json"
            ),
            "sha256": (
                "a0f0d05a578826208e3fee5c8e1e296c44db3450d9ef27a9a837a57123b04413"
            ),
            "rows": 5410,
            "supplies": ["composition_stratum", "preservation_class"],
        },
        "spine": {
            "file": "data/movement/chronology_rows_phase394.jsonl",
            "sha256": (
                "9dc2fba5019c34ecc57bb1bda3c341ac142876f8ee5c4f058807458faf7eae93"
            ),
            "rows": 205,
            "role": (
                "support and cross-check for site-period "
                "assertions inside Spec 039's published "
                "record; never an inscription label and "
                "never recomputed under this spec"
            ),
        },
        "recorded_results": {
            "phase140": {
                "file": "reports/phase140_results.json",
                "observed_chi_square": 4966.362228365138,
                "permutations_ge_observed": 0,
                "B": 9999,
                "p_raw": 0.0001,
                "cramers_v": 0.2190084751289231,
                "verdict": (
                    "SUPPORTED under control (chronology "
                    "NOT controlled)"
                ),
            },
            "phase385": {
                "file": "reports/phase385_results.json",
                "governing_basic_ci95": [
                    0.1837750116366994, 0.2102434435947284,
                ],
                "margin_v": 0.1,
                "B_bootstrap": 4999,
                "seed": 20261012,
            },
            "spec025_s_chron_exploratory_basic_ci95": [
                0.18480004041254045, 0.20984224851507333,
            ],
        },
        "anchors": {
            "file": "backend/reports/INDUS_FINAL_ANCHORS.json",
            "sha256": (
                "eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86ebb1fa3b602cfaed"
            ),
            "rule": "asserted byte-identical before and after any execution",
        },
    },
    "environment": {
        "python": "3.12.3",
        "runner": "backend (venv glossa-lab)",
        "aee": (
            "the version pinned in the Glossa venv at "
            "the freeze act (the aee 1.5.0 adoption is "
            "a separate in-flight owner decision; this "
            "draft runs no hooks under any version)"
        ),
        "specify": "1.0.10",
    },
}

SOURCES = [
    f"{SPEC_DIR}/freeze.md",
    f"{SPEC_DIR}/spec.md",
    f"{SPEC_DIR}/claims.json",
    f"{SPEC_DIR}/adjudication.md",
    f"{SPEC_DIR}/aee/freeze-aee-note.md",
    f"{SPEC_DIR}/build_freeze.py",
    "backend/tests/test_spec040_freeze.py",
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
