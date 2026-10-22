#!/usr/bin/env python3
"""Build the Spec 043 freeze record (freeze.json).

This builder was written at the freeze act of
2026-10-21 (campaign Wave 2, under the campaign
plan approved AS WRITTEN on 2026-10-21; the draft
PR #242 carried no builder and no draft digest).
After the AEE lifecycle hooks passed over the
recovered register (0.7-draft), it computed the
final digest over the frozen contract exactly
once, and its DEFINITION text was finalised in
the same act (the Spec 035 pattern). Run with
the Glossa backend venv python from the
repository root:

    python specs/043-pred-2026-007-registry-frame/build_freeze.py

Writes specs/043-pred-2026-007-registry-frame/freeze.json
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

SPEC_DIR = "specs/043-pred-2026-007-registry-frame"

REGISTRY_SHA256 = (
    "8a0b2a82ac8d226d574ce01f5550c581efd91a97cab86201a62f7a7e435bd420"
)
CROSS_CHECK_SHA256 = (
    "8c2bd6059a671068b645204db37e29ff13ca53009117b9447ed6c7bd1ead02b3"
)
BUILDER_SHA256 = (
    "4af822f1ad5c924defed7852df967f8633899b27a27fdaea84e2cdad8744efb0"
)
PARSER_SHA256 = (
    "9b57f0ecc10905c0746f1e7fb8e0622ac18e3b08e62bb2eb34fbec4bbd8ef615"
)
SIGN_CLUSTERS_SHA256 = (
    "623a787dd9cc93c4d3d36377890c4753e3427f57cf7ad70adcd6e8256ba1394a"
)
CHARACTERIZATION_SHA256 = (
    "54ebf660873fd853a64ce91c7e30d8c4cedc5bc3a0a1555db1f6281a52e3c476"
)
PRED_REGISTER_SHA256 = (
    "254ccf039cf04cf2882e04c8658381cc05573163651ed5d478697058aa424984"
)

DEFINITION = {
    "spec": "specs/043-pred-2026-007-registry-frame/spec.md",
    "freeze_doc": "specs/043-pred-2026-007-registry-frame/freeze.md",
    "experiment_id": "spec043-pred-2026-007-registry-frame",
    "register": {
        "path": "specs/043-pred-2026-007-registry-frame/claims.json",
        "register_version": "0.7-draft",
        "claims": 16,
        "aee_hook_pass": (
            "PASSED at the freeze act of 2026-10-21 "
            "under aee 1.5.0: after_specify round 1 "
            "over 0.5-draft returned 54 failure modes "
            "(16 irreducibility, 20 independence, 1 "
            "counterexample, 1 circular-inference "
            "contradiction over the draft's mutual "
            "C08-C09 depends_on entries, 16 FR-2.3 "
            "draft-cap records; minimum propagated "
            "0.695); recovered to 0.6-draft "
            "(observed_at on every evidence item, "
            "independent_of declarations); round 2 "
            "returned 41 failure modes with no claim "
            "below the 0.70 threshold (minimum "
            "propagated 0.795); recovered to "
            "0.7-draft on the Spec 039 pattern "
            "(single head propositions, carried "
            "clauses in boundaries, the C08-C09 "
            "cycle carried as a boundary "
            "cross-reference, declarations for the "
            "shared builder and Spec 038 sources); "
            "round 3 returned 23 failure modes; "
            "final adjustments (the C04 registry "
            "item's declaration restored, the C07 "
            "and C09 heads narrowed) left round 4 at "
            "after_specify and first passes at "
            "after_plan and after_tasks each "
            "carrying 16 FR-2.3 draft-cap records "
            "only; at every passing hook zero "
            "correctness failure modes and no claim "
            "below the 0.70 threshold (minimum "
            "propagated 0.795); the engine outcome "
            "word reads iterate solely from the "
            "draft-cap records (gate reading "
            "DD-043-14; record in "
            "specs/043-pred-2026-007-registry-frame/aee/"
            "freeze-aee-note.md)"
        ),
    },
    "basis": {
        "adjudication": (
            "specs/043-pred-2026-007-registry-frame/adjudication.md"
        ),
        "decisions": (
            "The runnable-experiments campaign plan, "
            "approved by the owner AS WRITTEN on "
            "2026-10-21, commissions this spec (Wave 1 "
            "member 20, design D-31 successor; a new "
            "prediction number under E-4 - "
            "PRED-2026-012, registered 2026-10-21 on "
            "this branch and recorded in "
            "adjudication.md section 6; an OSF "
            "contract registration per spec at its "
            "freeze under E-1), the Wave 2 freeze wave "
            "was delegated under that approval, and "
            "that approval is also this member's Wave 3 "
            "execution authorization (adjudication.md "
            "section 7.6, answering the register's "
            "scoring-gate line). Freeze decisions are "
            "recorded in adjudication.md section 7: "
            "DD-043-10 adopted - a provenance basis "
            "counts only if stated in words with a "
            "locator (7.1); DD-043-11 decided yes - "
            "own OSF registration under E-1 (7.2); "
            "DD-043-12 ruled enumerated-only for the "
            "LOG class, as the draft frames it (7.3); "
            "DD-043-13 allocated Phase-410 (7.4); "
            "DD-043-14 adopts the DD-038-10 AEE gate "
            "reading (7.5)."
        ),
    },
    "design": {
        "phase": "Phase-410",
        "act": (
            "score PRED-2026-012 over the full "
            "enumerated ITM population of the pinned "
            "canonical sign registry, under a "
            "documentary provenance gate (step 0, "
            "check 0.3) that must pass before any "
            "Phase 5 assignment is looked up, reading "
            "only the recorded CGSA Phase 5 output"
        ),
        "question_owner": (
            "docs/PREDICTION_REGISTER.md PRED-2026-012 "
            "(H4 successor: ICIT Function Alignment), "
            "registered 2026-10-21 under campaign "
            "ruling E-4 as successor to PRED-2026-007"
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
                "(DD-038-1 carried)"
            ),
            "recorded_partial_test": (
                "PRED-2026-007's pre-execution record: "
                "P385 (ITM) Cluster 21 TERMINAL; P378 "
                "(ITM) Cluster 39 TERMINAL; P098 (LOG) "
                "Cluster 10 INITIAL; recorded rate 2/3 "
                "(67%) - a pre-execution record whose "
                "denominator mixed in a non-ITM sign; "
                "outcome PARTIALLY CONFIRMED, standing "
                "untouched under this spec"
            ),
        },
        "population": {
            "unit": "distinct sign, by parpola_id",
            "frame": (
                "every distinct sign whose icit_function "
                "value in the pinned canonical sign "
                "registry is exactly ITM; the registry "
                "is primary because its coded values "
                "were verified in full at draft; no "
                "frequency threshold, no attestation "
                "requirement"
            ),
            "listed_at_draft": ["P056", "P324", "P378", "P385"],
            "size": 4,
            "census": {
                "rows": 803,
                "uncoded": 791,
                "coded": 12,
                "coded_counts": {
                    "ITM": 4, "LOG": 2, "NUM": 2,
                    "TMK": 2, "SHN": 1, "SYL": 1,
                },
            },
            "excluded_by_rule": (
                "P098 (no function code at all in the "
                "primary source) and every sign coded "
                "other than ITM, or uncoded"
            ),
            "log_set": {
                "members": ["P217", "P310"],
                "role": (
                    "enumerated-only (DD-043-12, decided "
                    "at freeze): enumerated in the census "
                    "and the per-sign record, traced "
                    "through the provenance gate's "
                    "evidence set, never scored; no LOG "
                    "share enters the verdict and the "
                    "trace gates nothing"
                ),
            },
            "rederivation": (
                "step 0 re-derives all 803 icit_function "
                "values from the pinned builder rule "
                "(_WELLS_FUNCTIONS, first matching key "
                "in table order over each row's split "
                "wells_ids); verified at draft and "
                "re-verified at the freeze with zero "
                "mismatches; any mismatch or census "
                "difference closes the study as CANNOT "
                "BE RUN AS WRITTEN (check 0.2)"
            ),
        },
        "sources": {
            "primary_function_code": {
                "file": "data/crosswalks/canonical_sign_registry.csv",
                "field": "icit_function",
                "rows": 803,
                "sha256": REGISTRY_SHA256,
            },
            "cross_check_function_code": {
                "file": "reports/indus_cgsa_cluster_analysis.json",
                "field": "data.a[].icit_function",
                "records": 611,
                "sha256": CROSS_CHECK_SHA256,
                "known_state": (
                    "uncoded field (579 empty, 32 "
                    "free-text glosses, no ITM and no LOG "
                    "values), per Spec 038's execution "
                    "record; disagreements are expected "
                    "in that kind, published sign-by-sign, "
                    "and never move membership"
                ),
            },
            "builder": {
                "file": "scripts/cgsa_pipeline.py",
                "sha256": BUILDER_SHA256,
                "role": (
                    "the derivation rule: Phase 3 "
                    "build_canonical_registry populates "
                    "icit_function from the _WELLS_FUNCTIONS "
                    "table (14 keys; comment: from ICIT "
                    "docs + Fuls 2013)"
                ),
            },
            "parser": {
                "file": "backend/glossa_lab/data/fuls_parser.py",
                "sha256": PARSER_SHA256,
                "role": (
                    "the lineage record: function "
                    "classification (from Wells) read off "
                    "the same catalog lines as a "
                    "positional classification (DD-038-2)"
                ),
            },
            "conflict_rule": (
                "the primary governs membership; "
                "cross-check disagreements are recorded "
                "sign-by-sign and published; ambiguity "
                "or conflict within the primary itself "
                "closes the study as CANNOT BE RUN AS "
                "WRITTEN (DD-043-1)"
            ),
        },
        "provenance_gate": {
            "position": (
                "step 0, check 0.3: after the population "
                "is fixed (checks 0.1-0.2) and before "
                "any Phase 5 lookup, the sanity anchor "
                "included (DD-043-4)"
            ),
            "evidence_set": {
                "D1": "the pinned builder (check 0.1)",
                "D2": (
                    "the pinned parser, with its test "
                    "(the same-line juxtaposition of "
                    "function and positional class)"
                ),
                "D3": (
                    "Fuls 2013, the taxonomy source the "
                    "builder cites, produced at execution "
                    "with locators"
                ),
                "D4": (
                    "Wells' published sign list, as "
                    "transmitted by the ICIT documentation "
                    "the builder cites, produced at "
                    "execution with locators"
                ),
            },
            "limbs": [
                "class definition: the produced "
                "documents state what ITM is, and the "
                "stated definition is not a positional one",
                "per-sign basis: for each of the four "
                "ITM signs, the produced documents state "
                "a position-independent basis",
                "source agreement: the produced "
                "published documents agree with the "
                "builder table for all four ITM signs",
            ],
            "failure_closure": (
                "PROVENANCE - CANNOT BE RUN AS WRITTEN, "
                "unscored, on any single sign's failure; "
                "no subset verdict exists"
            ),
            "borderline_standard": (
                "DD-043-10 (adopted at freeze): a basis "
                "counts as stated only if the produced "
                "document states it in words, with a "
                "locator, for the class or the sign; "
                "inference from a class's name, from the "
                "builder table's glosses, or from the "
                "classification's general reputation "
                "does not count; borderline calls are "
                "recorded in the step-0 record with the "
                "quoted text; silence is failure"
            ),
        },
        "phase5_output": {
            "assignment": {
                "file": "outputs/analysis/sign_clusters.json",
                "sha256": SIGN_CLUSTERS_SHA256,
                "best_k": 40,
                "signs_clustered": 160,
            },
            "cluster_class_rule": (
                "DD-043-7 (carried DD-038-9): a "
                "cluster's class is the class recorded "
                "for that cluster in "
                "reports/cluster_characterization.md "
                "(sha256 "
                "54ebf660873fd853a64ce91c7e30d8c4cedc5bc3a0a1555db1f6281a52e3c476); "
                "deterministic lookup, no threshold "
                "invented, no class derived from rates "
                "at execution; a cluster with no "
                "recorded class leaves its signs "
                "unassigned under the coverage rule"
            ),
            "no_reclustering": (
                "scoring reads the recorded output only; "
                "if it does not survive in "
                "sign-assignable form the study closes "
                "as CANNOT BE RUN AS WRITTEN; no "
                "re-clustering is run under this spec "
                "for any reason"
            ),
            "sanity_anchor": {
                "P385": 21, "P378": 39, "P098": 10,
            },
        },
        "step0": {
            "order": [
                "check 0.1 sources and pins",
                "check 0.2 enumeration with "
                "re-derivation and census reconciliation, "
                "cross-check read",
                "check 0.3 provenance gate (D1-D4, "
                "three limbs, DD-043-10 standard)",
                "check 0.4 recorded Phase 5 output "
                "verification (sign-assignable form; "
                "sanity anchor)",
            ],
            "failure_closures": (
                "CANNOT BE RUN AS WRITTEN for source, "
                "integrity, or recorded-output failures "
                "(checks 0.1, 0.2, 0.4); PROVENANCE - "
                "CANNOT BE RUN AS WRITTEN for the gate's "
                "failure (check 0.3); each reported as "
                "itself, never as a verdict"
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
                "the design's rule, carried from "
                "DD-038-4 in substance (DD-043-8), not "
                "the register's"
            ),
        },
        "census_branch": (
            "foreclosed under this frame: the listed "
            "population (four signs) strictly exceeds "
            "the tested sample (two ITM signs), so "
            "D-31's census completion cannot arise; "
            "no outcome may claim one"
        ),
        "register_handling": (
            "dated section 6 appends only; the "
            "registered section 3 text is never "
            "edited; every other prediction's entry "
            "stays byte-identical; the Phase D "
            "register-hash pin is advanced by name "
            "for the authorised append; on a step-0 "
            "closure of either kind PRED-2026-012's "
            "section 3 Outcome stays PENDING and "
            "PRED-2026-007's stays PARTIALLY CONFIRMED, "
            "untouched"
        ),
        "fences": (
            "every outcome statement carries the "
            "lineage boundary (a verdict states the "
            "Wells-lineage ITM classification's "
            "consistency with the recorded Phase 5 "
            "clustering, and establishes nothing "
            "about sign meanings, the classification's "
            "truth, or any independent classification) "
            "and the clustering-stability caveat "
            "(fidelity to the named clustering, not "
            "a repair of it); the per-sign table is "
            "published with every scored outcome; a "
            "bare percentage over four signs is a "
            "misstatement of this test's weight"
        ),
        "execution_gate": (
            "Execution is Phase-410 under this frozen "
            "contract. The separate owner execution "
            "order the register's PRED-2026-012 "
            "scoring gate requires is the owner's "
            "approval of the runnable-experiments "
            "campaign plan AS WRITTEN on 2026-10-21, "
            "which orders this member's execution in "
            "Wave 3 (adjudication.md section 7.6); "
            "execution additionally awaits the "
            "verified approval of this spec's OSF "
            "contract registration (DD-043-11; "
            "osf-spec-registration.md). The freeze "
            "itself runs nothing: it does not run the "
            "provenance adjudication, produces or "
            "judges no D3/D4 document, computes no "
            "share, and looks up no Phase 5 assignment "
            "beyond the register's three named signs"
        ),
    },
    "inputs": {
        "pred_register": {
            "file": "docs/PREDICTION_REGISTER.md",
            "sha256": PRED_REGISTER_SHA256,
            "entry": (
                "PRED-2026-012 (registered 2026-10-21 "
                "under campaign ruling E-4; successor "
                "to PRED-2026-007, registered "
                "2026-04-22)"
            ),
            "note": (
                "the freeze-time hash is asserted as "
                "this definition constant; the live "
                "file is this contract's own append "
                "target at execution, so the freeze "
                "test asserts the entry's facts on the "
                "live file, not its whole-file hash "
                "(the Spec 038 form)"
            ),
        },
        "spec038_record": {
            "freeze_act_digest": (
                "b54571d845a2be3429bc532fee4bb58c20723f77e2d40ffcd43b56e0caab6eef"
            ),
            "closure": (
                "Spec 038 closed at step 0.2 as CANNOT "
                "BE RUN AS WRITTEN, unscored, "
                "2026-10-20; its outcome record and the "
                "register's section 6 entries of "
                "2026-10-20 (including DD-038-2's "
                "provenance reconciliation) are this "
                "design's predecessor record"
            ),
        },
    },
    "environment": {
        "python": "3.12.3",
        "runner": "backend (venv glossa-aee150)",
        "aee": "1.5.0 (adopted environment, PR #231; package pinned >=1.5.0,<1.6)",
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
    "backend/tests/test_spec043_freeze.py",
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
