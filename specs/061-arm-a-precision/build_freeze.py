#!/usr/bin/env python3
"""Build the Spec 061 freeze record (freeze.json).

This builder was written at the freeze act of
2026-10-21 (the draft carried no builder and no
draft digest: the campaign's drafting wave opens
claims-first drafts only, and the digest is
computed over the recovered register exactly
once, at the freeze - the Spec 035 ordering).
Run with the Glossa backend venv python from the
repository root:

    python specs/061-arm-a-precision/build_freeze.py

Writes specs/061-arm-a-precision/freeze.json
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

SPEC_DIR = "specs/061-arm-a-precision"

DEFINITION = {
    "spec": "specs/061-arm-a-precision/spec.md",
    "freeze_doc": "specs/061-arm-a-precision/freeze.md",
    "experiment_id": "spec061-arm-a-precision",
    "register": {
        "path": "specs/061-arm-a-precision/claims.json",
        "register_version": "0.7-draft",
        "claims": 15,
        "aee_hook_pass": (
            "PASSED at the freeze act of 2026-10-21 under aee 1.5.0: "
            "after_specify, after_plan, and after_tasks each cleared in "
            "adjudicated rounds over the recovered register (a "
            "loadability recovery from 0.5-draft to 0.6-draft - the "
            "draft's free-form evidence kind and source_quality labels "
            "are not engine values and the loader refuses them; 51 "
            "failure modes over 0.6-draft: 21 independence-unmodelled, "
            "12 irreducibility, 2 negation-conflict, 1 counterexample, "
            "15 FR-2.3 draft-cap records; the irreducibility-challenged "
            "heads restated as single propositions with carried "
            "clauses moved into boundaries, and mutual independent_of "
            "declarations added, at 0.7-draft; 15 draft-cap records "
            "only over the final 0.7-draft register), at every hook "
            "zero correctness failure modes and no claim below the "
            "0.70 threshold (minimum propagated 0.795); the engine "
            "outcome word reads iterate solely from the draft-cap "
            "records "
            "(gate reading DD-061-17; record in "
            "specs/061-arm-a-precision/aee/freeze-aee-note.md)"
        ),
    },
    "basis": {
        "adjudication": "specs/061-arm-a-precision/adjudication.md",
        "decisions": (
            "DECIDED by the owner on 2026-10-21 (not proposals): the "
            "runnable-experiments campaign plan approved AS WRITTEN "
            "(decisions E-1 and E-3; member 18) commissions the campaign "
            "of which design D-27 arm A1 is a member; Spec 061 is D-27 "
            "arm A1's specification, and arm A2 is not a member of the "
            "pass (E-3). Draft decisions DD-061-1 to DD-061-7 are "
            "recorded in adjudication.md sections 4 and 6; DD-061-2, "
            "DD-061-3, and DD-061-5 are CONFIRMED at the freeze. Freeze "
            "decisions DD-061-8 to DD-061-17 are recorded in "
            "adjudication.md section 9: the composite pin remedy for "
            "DEF-061-1 confirmed with the pin set verified complete "
            "(DD-061-8); the integer multiplier grid m = 1..25 "
            "(DD-061-9); the ceiling m = 25 derived from the frozen "
            "49-member cell threshold (DD-061-10); 199 trials per grid "
            "point with 199 draws and 499 permutations per trial "
            "inherited from the frozen design (DD-061-11); the "
            "simulation seed 20261021 (DD-061-12); the "
            "effect-imposition construction - candidate (b), the "
            "frozen positive-control manner with the boost calibrated "
            "per scenario (DD-061-13); the spec's own OSF contract "
            "registration filed at the freeze under E-1 (DD-061-14); "
            "calibration required in three mechanical forms including "
            "the new gate 0.5 (DD-061-15); Phase-423 allocated "
            "(DD-061-16); and the DD-038-10 AEE gate reading adopted "
            "(DD-061-17)."
        ),
    },
    "design": {
        "phase": "Phase-423",
        "claim_under_test": {
            "id": "STUDY-SPEC-028/ARM-A",
            "verdict": "INCONCLUSIVE",
            "median_adj_r2": 0.00878393455594817,
            "interval": [0.004626892186724407, 0.01297407559730989],
            "share_draws_rejecting": 0.6231155778894473,
            "margin": 0.01,
            "records": 1593,
            "sites": 5,
        },
        "composite_pin": {
            "form": (
                "composite: the recorded summary (results file) plus "
                "the exact inputs and machinery that produced it "
                "(corpus layer, pipeline, margins audit, Spec 028 "
                "freeze record), with gate 0.3 exact reproduction as "
                "its verification (DD-061-1)"
            ),
            "defect": (
                "DEF-061-1: phase393_results.json records summaries "
                "only; the per-draw adj_draws the pipeline computes "
                "were never persisted to any file"
            ),
            "ruling": (
                "DD-061-8: the composite pin is confirmed as the "
                "remedy and the pin set is verified complete at the "
                "freeze - every component re-derived two-route at "
                "main a3509525fab64e22a4c053d7bbed14c7083a14d3"
            ),
            "results": {
                "file": "reports/phase393_results.json",
                "sha256": "0a1657a8af84615afbee95164cd1c10ea6fc5bc53d1b5a0a006b1862fa5ff607",
            },
            "corpus": {
                "file": "backend/glossa_lab/data/yajnadevam_inscriptions.csv",
                "sha256": "c02e3d7bb74cf5abb11cc94f88d8d469e6acc5d6fad4b7153c02c43428f58d98",
            },
            "pipeline": {
                "file": "specs/028-harappa-robustness/pipeline393.py",
                "sha256": "6c2ff91c41bbb283a513127c6ab7157c1805b640ba0d846f9c7d3349ab8a7b0e",
            },
            "margins_audit": {
                "file": "specs/028-harappa-robustness/margins-audit.json",
                "sha256": "15ae0281bb003f3b02742819349d3905004a282b28e9a2c00f433ac41c04bb6d",
            },
            "spec028_freeze": {
                "file": "specs/028-harappa-robustness/freeze.json",
                "sha256": "376cd8e7ebc21ef7c31d43270607f475bb7e685cdcbe88205d7092e17fc526cc",
            },
        },
        "step0_gates": (
            "0.1 composite pin integrity - a mismatch stops the run "
            "as INVALID; 0.2 population reproduction (1,593 records, "
            "five site totals, 6 included cells, 294 per draw) - "
            "INVALID; 0.3 recorded-distribution reproduction - the "
            "frozen primary re-run at seed 20261012 (R = 199, B = 499) "
            "reproduces the recorded median, interval, and rejection "
            "share exactly - INVALID; 0.4 search frame present in "
            "full in the freeze record - CANNOT BE RUN AS WRITTEN; "
            "0.5 construction calibration - per scenario, the "
            "DD-061-13 bracket is verified and the bisection achieves "
            "|A(b) - theta| <= 1e-6 - CANNOT BE RUN AS WRITTEN "
            "(gate 0.5 added at the freeze, DD-061-13/DD-061-15)"
        ),
        "scenarios": {
            "scenario_1": {
                "theta": 0.00878393455594817,
                "direction": "resolves downward (interval excludes the "
                             "0.01 margin from below)",
                "design_value": 0.00878,
            },
            "scenario_2": {
                "theta": 0.015,
                "direction": "resolves upward (interval excludes the "
                             "0.01 margin from above)",
            },
        },
        "resolution_rule": (
            "a trial resolves if and only if its adjusted-R2 "
            "percentile interval excludes 0.01 strictly in its "
            "scenario's direction - a touching bound does not "
            "resolve (DD-061-2 confirmed); a grid point qualifies if "
            "and only if at least 80% of its trials resolve"
        ),
        "search_frame": {
            "grid": "integer multiples m = 1, 2, ..., 25 (step 1)",
            "grid_ruling": (
                "DD-061-9: the design's method scales at multiples of "
                "current sizes; at integer multiples the per-site "
                "added counts are exactly (m - 1) x the recorded "
                "site totals, so no rounding rule is needed or "
                "supplied"
            ),
            "ceiling_multiple": 25,
            "ceiling_added_total": 38232,
            "ceiling_ruling": (
                "DD-061-10: the smallest multiple at which every "
                "recorded site x type cell reaches the frozen "
                "49-member inclusion threshold (pipeline N_CELL = "
                "49; the binding cells are the two 2-record TAB "
                "cells, reaching 50); at m = 25 the frozen draw "
                "reaches its maximum size, 10 cells x 49 = 490 "
                "inscriptions per draw"
            ),
            "trials_per_grid_point": 199,
            "trials_ruling": (
                "DD-061-11: the frozen replication count of the "
                "machinery (DRAWS = 199); the binomial standard "
                "deviation of a grid point's resolution share at the "
                "0.80 threshold is 0.0284 and is reported beside "
                "every share"
            ),
            "draws_per_trial": 199,
            "permutations_per_draw": 499,
            "simulation_seed": 20261021,
            "seed_ruling": (
                "DD-061-12: a fresh seed fixed in the freeze record "
                "(20261012 belongs to the recorded run and gate 0.3), "
                "following the Spec 053 freeze-date-seed precedent; "
                "one Generator per scenario consumed in ascending "
                "grid order, trials in order, template resampling "
                "then world generation then the pipeline run within "
                "each trial"
            ),
            "effect_imposition": {
                "ruling": "DD-061-13 (OP-061-5 decided)",
                "construction": (
                    "candidate (b): each site's composition is the "
                    "pooled composition (pooled mapped-token frequency "
                    "over the Arm A eligible population, as Spec "
                    "028's build_calibration.py computes it) with the "
                    "columns of the site's positive_control_sign_sets "
                    "(margins audit, pinned; 10 signs per site) "
                    "multiplied by a boost factor b >= 1 and "
                    "renormalised - the frozen positive-control "
                    "manner, verbatim; the trial world is the "
                    "recorded entries resampled per site with "
                    "replacement to m x site totals, generated by the "
                    "frozen pipeline393.synthetic_entries under the "
                    "imposed compositions, and the trial statistic is "
                    "the frozen run_pipeline_cells summarised by the "
                    "frozen summarise"
                ),
                "calibration": (
                    "b is chosen per scenario by bisection on the "
                    "bracket [1, 3] (b = 1: A(1) = -0.0025189, the "
                    "frozen adjusted-R2 null offset at n = 1593, "
                    "g = 5; b = 3 is the frozen POSITIVE_BOOST, whose "
                    "recorded Arm A positive-control median is "
                    "0.023963353007570576, above both thetas) so that "
                    "the frozen PERMANOVA + adjusted_r2 applied to "
                    "the constructed population in expectation (each "
                    "inscription's expected count vector = p_s(b) x "
                    "its legible length, over the full recorded "
                    "population, permutations off) returns A(b) = "
                    "theta; at most 100 iterations, stopping when "
                    "|A(b) - theta| <= 1e-6; the achieved b and A(b) "
                    "are recorded in the results JSON"
                ),
                "refused": (
                    "candidate (a) is not adopted: no record defines "
                    "a site-difference direction or a shift operator, "
                    "and inventing one is the assumption the "
                    "campaign's Part 7 tripwire forbids; candidate (c) "
                    "stays rejected for the draft's reason - the "
                    "design's criterion is stated over trials of a "
                    "resampled interval, which an analytic "
                    "width-scaling produces none of"
                ),
                "stated_limit": (
                    "calibration targets the constructed population's "
                    "expected adjusted R2 under the frozen estimator "
                    "on the full population; the trial machinery "
                    "measures resolution under the frozen equal-cell "
                    "draw design around that world; the two "
                    "weightings differ and the difference is stated, "
                    "not hidden (spec section 8)"
                ),
            },
        },
        "target_rule": {
            "rule": (
                "for each scenario independently, the target is the "
                "smallest total added-inscription count at a "
                "qualifying grid point, reported with its multiple "
                "and its per-site distribution allocated in "
                "proportion to the recorded Arm A site totals and "
                "summing exactly to the total (DD-061-3 confirmed; "
                "exact in integers at integer multiples); the full "
                "grid table is published either way"
            ),
            "operative_target": (
                "the operative (trigger) target T* is the larger "
                "returned target; a single returned target is "
                "operative with its scenario condition; no returned "
                "target leaves T* undefined and the trigger unable "
                "to fire on this record (DD-061-5 confirmed)"
            ),
        },
        "outcomes": [
            "TARGET UNDER BOTH SCENARIOS",
            "TARGET UNDER SCENARIO 1 ONLY",
            "TARGET UNDER SCENARIO 2 ONLY",
            "NO TARGET UNDER EITHER SCENARIO",
            "INVALID",
            "CANNOT BE RUN AS WRITTEN",
        ],
        "simulation_fence": (
            "every output labels the computation a simulation over "
            "recorded data, states that its added inscriptions are "
            "resamples of recorded inscriptions, and never presents "
            "simulated additions as data the program holds or as "
            "evidence; the fence sentence of spec section 6 stands: "
            "this computation measures the resolution of a recorded "
            "test and establishes nothing about the ancient world"
        ),
        "arm_a2": {
            "status": (
                "Arm A2, the decisive rerun of the frozen Arm A "
                "test, is not part of Spec 061 or of this campaign "
                "pass (campaign decision E-3)"
            ),
            "trigger": (
                "the trigger fires when new multi-site inscription "
                "data, verified through Phase-130 intake, brings the "
                "cumulative added non-Harappa inscription count to "
                "at least the operative target T* returned by this "
                "spec's computation (DD-061-5); a fired trigger "
                "queues a mini planning gate under E-3 - the arm "
                "does not join this pass and does not execute"
            ),
            "registration": (
                "the rerun's test is already frozen and registered "
                "(osf.io/7m35w); no new registration is filed for A2"
            ),
        },
        "freeze_does_not": (
            "the freeze computes nothing: no trial has run, no "
            "world has been built, no boost has been calibrated, and "
            "no target has been estimated or peeked at; it does not "
            "re-run, re-adjudicate, or edit Spec 028 Arm A, whose "
            "INCONCLUSIVE verdict stands exactly as recorded; it "
            "arms nothing - Arm A2's trigger is recorded, not fired"
        ),
        "execution_gate": (
            "Not satisfied at the freeze: execution (Phase-423) "
            "begins only after this freeze has merged, the OSF "
            "registration's approval act has completed, and a "
            "separate execution order is given (campaign Wave 3, "
            "group 2)"
        ),
    },
    "inputs": {
        "results": {
            "file": "reports/phase393_results.json",
            "sha256": "0a1657a8af84615afbee95164cd1c10ea6fc5bc53d1b5a0a006b1862fa5ff607",
            "bytes": 19753,
        },
        "corpus": {
            "file": "backend/glossa_lab/data/yajnadevam_inscriptions.csv",
            "sha256": "c02e3d7bb74cf5abb11cc94f88d8d469e6acc5d6fad4b7153c02c43428f58d98",
            "bytes": 1204144,
        },
        "pipeline": {
            "file": "specs/028-harappa-robustness/pipeline393.py",
            "sha256": "6c2ff91c41bbb283a513127c6ab7157c1805b640ba0d846f9c7d3349ab8a7b0e",
            "bytes": 15127,
        },
        "margins_audit": {
            "file": "specs/028-harappa-robustness/margins-audit.json",
            "sha256": "15ae0281bb003f3b02742819349d3905004a282b28e9a2c00f433ac41c04bb6d",
            "bytes": 5355,
        },
        "spec028_freeze": {
            "file": "specs/028-harappa-robustness/freeze.json",
            "sha256": "376cd8e7ebc21ef7c31d43270607f475bb7e685cdcbe88205d7092e17fc526cc",
            "bytes": 4212,
        },
        "anchors": {
            "file": "backend/reports/INDUS_FINAL_ANCHORS.json",
            "sha256": "df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569",
            "posture": "this spec moves no anchor; the file is "
                       "asserted byte-identical before and after "
                       "any execution",
        },
        "calibration_record": {
            "file": "specs/028-harappa-robustness/calibration.json",
            "sha256": "4198747b42121fea817db2e5ad82da10cca6118fef39bb14dc13cdf56ac204ff",
            "bytes": 2404,
            "posture": "read at the freeze as the DD-061-13 bracket "
                       "evidence (Arm A positive control at the "
                       "frozen boost 3.0: median adjusted R2 "
                       "0.023963353007570576); not a step-0 pin",
        },
        "pin_verification": (
            "at the freeze of 2026-10-21 every pin above was "
            "re-derived by two independent routes (contents-API raw "
            "and git-blob) at main "
            "a3509525fab64e22a4c053d7bbed14c7083a14d3; the two routes "
            "agree byte-for-byte on every file and every hash equals "
            "its pin (freeze.md section 2)"
        ),
    },
    "environment": {
        "python": "3.12.3",
        "runner": "backend (venv glossa-lab)",
        "aee": "1.5.0 (adopted environment; package pinned >=1.5.0,<1.6)",
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
    "backend/tests/test_spec061_freeze.py",
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
