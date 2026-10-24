#!/usr/bin/env python3
"""Build the Spec 062 freeze record (freeze.json).

This builder was written at the freeze act of
2026-10-21 (the draft carried no builder and no
draft digest: the amendment-queue drafting
commission opens claims-first drafts only, and
the digest is computed over the recovered
register exactly once, at the freeze - the
Spec 035 ordering). Run with the Glossa backend
venv python from the repository root:

    python specs/062-arm-a-precision-calibration-repair/build_freeze.py

Writes
specs/062-arm-a-precision-calibration-repair/freeze.json
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

SPEC_DIR = "specs/062-arm-a-precision-calibration-repair"

DEFINITION = {
    "spec": "specs/062-arm-a-precision-calibration-repair/spec.md",
    "freeze_doc": "specs/062-arm-a-precision-calibration-repair/freeze.md",
    "experiment_id": "spec062-arm-a-precision-calibration-repair",
    "register": {
        "path": "specs/062-arm-a-precision-calibration-repair/claims.json",
        "register_version": "0.6-draft",
        "claims": 15,
        "aee_hook_pass": (
            "PASSED at the freeze act of 2026-10-21 under aee 1.5.3: "
            "after_specify, after_plan, and after_tasks each cleared "
            "over the recovered register (the draft register already "
            "carried engine evidence values and mutual independent_of "
            "declarations, so no loadability recovery was needed; "
            "round 1 over 0.5-draft returned 22 failure modes: 15 "
            "FR-2.3 draft-cap records and 7 irreducibility challenges "
            "recorded under the coverage_gap category (F062-C05, C07, "
            "C09, C11, C12, C13, C15); the challenged heads restated "
            "as single propositions with carried clauses moved into "
            "boundaries, and the freeze rulings DD-062-7 to DD-062-9 "
            "carried into the boundaries of F062-C03, C06, C07, and "
            "C12, at 0.6-draft; 15 draft-cap records only over the "
            "final 0.6-draft register), at every hook zero "
            "correctness failure modes and no claim below the 0.70 "
            "threshold (minimum propagated 0.72); the engine outcome "
            "word reads iterate solely from the draft-cap records "
            "(gate reading DD-062-12; record in "
            "specs/062-arm-a-precision-calibration-repair/aee/freeze-aee-note.md)"
        ),
    },
    "basis": {
        "adjudication": "specs/062-arm-a-precision-calibration-repair/adjudication.md",
        "decisions": (
            "DECIDED by the owner on 2026-10-21 (not proposals): the "
            "amendment package Item 3 approval (take Spec 062 "
            "through freeze and OSF filing), on the amendment-queue "
            "commission of the same date (item 3: Spec 061 "
            "calibration repair). Spec 062 is the successor to Spec "
            "061 (design D-27 arm A1 only); arm A2 is not a member "
            "of this spec (campaign decision E-3). Draft decisions "
            "DD-062-1 to DD-062-6 are recorded in adjudication.md "
            "sections 4 and 6 and stand as drafted. Freeze decisions "
            "DD-062-7 to DD-062-12 are recorded in adjudication.md "
            "section 8: the calibration seed 20261021 adopted as "
            "drafted (DD-062-7); Phase-424 allocated (DD-062-8); "
            "the calibration construction R-1 adopted as drafted, "
            "R-2 not adopted and its tolerance amendment not taken, "
            "R-3 and R-4 standing rejected on measurement "
            "(DD-062-9); the spec's own OSF contract registration "
            "filed at the freeze under E-1 (DD-062-10); the freeze "
            "and filing acts taken, execution not authorised "
            "(DD-062-11); and the DD-038-10 AEE gate reading adopted "
            "(DD-062-12)."
        ),
    },
    "design": {
        "phase": "Phase-424",
        "predecessor": {
            "spec": "specs/061-arm-a-precision",
            "phase": "Phase-423",
            "outcome": (
                "CANNOT BE RUN AS WRITTEN at gate 0.5: the frozen "
                "calibration (candidate (b), DD-061-13) applies the "
                "estimator to the constructed population in "
                "expectation, within-site variation is exactly zero, "
                "and A(1) = -0.0025188916876574316 exactly with "
                "A(1.5) = A(2) = A(3) = 1.0 exactly, so no boost in "
                "[1, 3] achieves |A(b) - theta| <= 1e-6 for either "
                "scenario (DEF-062-1)"
            ),
            "posture": (
                "Spec 061's closed record is never patched "
                "(DD-062-1); its operative target T* stays undefined "
                "on Spec 061's record"
            ),
        },
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
                "its verification (DD-061-1, carried by DD-062-2)"
            ),
            "defect": (
                "DEF-061-1: phase393_results.json records summaries "
                "only; the per-draw adj_draws the pipeline computes "
                "were never persisted to any file"
            ),
            "ruling": (
                "the pin set is Spec 061's, unchanged, and is "
                "verified complete at this freeze - every component "
                "re-derived two-route at main "
                "b7a8c8a42d4e1137c04ef4c0123fb4ba4dbc3736"
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
            "share exactly - INVALID (the repair leaves gate 0.3's "
            "path untouched: it is a function of the section 2 pins, "
            "the frozen machinery, seed 20261012, and R/B, and the "
            "calibration shares no RNG stream with it); 0.4 search "
            "frame present in full in the freeze record - CANNOT BE "
            "RUN AS WRITTEN; 0.5-R construction calibration (repaired; "
            "replaces Spec 061's gate 0.5) - per scenario, the "
            "bracket recomputes (A_R(1) < theta < A_R(3)), A_R is "
            "strictly increasing on the recorded 9-point scan grid, "
            "and the bisection achieves |A_R(b) - theta| <= 1e-6 "
            "within 100 iterations - CANNOT BE RUN AS WRITTEN"
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
            "resolve (DD-061-2 carried); a grid point qualifies if "
            "and only if at least 80% of its trials resolve"
        ),
        "search_frame": {
            "grid": "integer multiples m = 1, 2, ..., 25 (step 1)",
            "grid_ruling": (
                "carried from Spec 061 (DD-061-9): the design's "
                "method scales at multiples of current sizes; at "
                "integer multiples the per-site added counts are "
                "exactly (m - 1) x the recorded site totals, so no "
                "rounding rule is needed or supplied"
            ),
            "ceiling_multiple": 25,
            "ceiling_added_total": 38232,
            "ceiling_ruling": (
                "carried from Spec 061 (DD-061-10): the smallest "
                "multiple at which every recorded site x type cell "
                "reaches the frozen 49-member inclusion threshold "
                "(pipeline N_CELL = 49; the binding cells are the "
                "two 2-record TAB cells, reaching 50); at m = 25 "
                "the frozen draw reaches its maximum size, 10 cells "
                "x 49 = 490 inscriptions per draw"
            ),
            "trials_per_grid_point": 199,
            "trials_ruling": (
                "carried from Spec 061 (DD-061-11): the frozen "
                "replication count of the machinery (DRAWS = 199); "
                "the binomial standard deviation of a grid point's "
                "resolution share at the 0.80 threshold is 0.0284 "
                "and is reported beside every share"
            ),
            "draws_per_trial": 199,
            "permutations_per_draw": 499,
            "simulation_seed": 20261021,
            "seed_ruling": (
                "carried from Spec 061 (DD-061-12): one Generator "
                "per scenario seeded 20261021 consumed in ascending "
                "grid order, trials in order, template resampling "
                "then world generation then the pipeline run within "
                "each trial; the calibration Generator is a "
                "separate object, also seeded 20261021 as drafted "
                "(DD-062-7), created before the trial Generators "
                "and exhausted by the calibration step"
            ),
            "effect_imposition": {
                "ruling": "DD-062-9 (OP-062-4 decided): construction R-1 adopted as drafted",
                "construction": (
                    "candidate (b)'s imposed compositions carried "
                    "(DD-061-13 steps 1-2 and trial world step 4): "
                    "each site's composition is the pooled "
                    "composition (pooled mapped-token frequency over "
                    "the Arm A eligible population, as Spec 028's "
                    "build_calibration.py computes it) with the "
                    "columns of the site's positive_control_sign_sets "
                    "(margins audit, pinned; 10 signs per site) "
                    "multiplied by a boost factor b >= 1 and "
                    "renormalised; the trial world is the recorded "
                    "entries resampled per site with replacement to "
                    "m x site totals, generated by the frozen "
                    "pipeline393.synthetic_entries under the imposed "
                    "compositions, and the trial statistic is the "
                    "frozen run_pipeline_cells summarised by the "
                    "frozen summarise. Only the calibration (step 3) "
                    "is replaced, by section 4.7-R construction R-1"
                ),
                "calibration": (
                    "construction R-1: b is chosen per scenario so "
                    "that A_R(b) = theta, where A_R is the median of "
                    "199 draw statistics at the positive control's "
                    "level - per draw, one generated population over "
                    "the full template, then the frozen cell "
                    "rarefaction (6 cells x 49 = 294). Per draw and "
                    "inscription i at site s, the proportion row is "
                    "a Dirichlet draw centred exactly on the imposed "
                    "composition p_s(b): q_i(b) = G_i / sum G, with "
                    "G_ik = GammaQuantile(U[d,i,k]; kappa_i x "
                    "p_s,k(b)) and kappa_i = n_legible(i) - 1, so "
                    "Var(q_k) = p_k(1 - p_k)/n_legible(i), exactly "
                    "the frozen token drawing's multinomial "
                    "proportion variance. The uniforms U and the "
                    "rarefaction selections are drawn once from a "
                    "dedicated calibration Generator (seed 20261021, "
                    "DD-062-7) and fixed for both scenarios and "
                    "every b, so A_R is a deterministic continuous "
                    "function of b. The draw statistic is the frozen "
                    "pipeline393 estimator (proportion normalisation, "
                    "Bray-Curtis, PERMANOVA, adjusted_r2; "
                    "permutations off) on the fixed selection. b is "
                    "found by bisection on [1, 3], at most 100 "
                    "iterations, stopping when |A_R(b) - theta| <= "
                    "1e-6; the achieved b and A_R(b) are recorded in "
                    "the results JSON (gate 0.5-R verifies the "
                    "bracket, strict increase on the recorded "
                    "9-point scan grid, and the tolerance before any "
                    "trial)"
                ),
                "refused": (
                    "R-2 (verbatim redraw-per-b, the frozen "
                    "synthetic_entries under p_s(b) redrawn per b) "
                    "is not adopted: as a function of b it is either "
                    "a noisy Monte Carlo estimate or, under common "
                    "random numbers, a deterministic step function "
                    "with measured jumps of 2.2e-05 to 7.6e-04 near "
                    "the root, so it cannot promise the frozen 1e-6 "
                    "tolerance; it stays on the record as a "
                    "non-adopted alternative (adjudication section "
                    "3), adoptable only with a tolerance amendment "
                    "that this freeze does not take. R-3 "
                    "(draw-then-tilt) and R-4 (Dirichlet "
                    "draw-then-tilt) stand rejected on measurement: "
                    "on planted data neither brackets theta (R-3 "
                    "A(3) = 0.004032, W = 49 probe; R-4 A(3) = "
                    "0.002790, W = 19 probe). Candidates (a) and (c) "
                    "of DD-061-13 remain refused for their stated "
                    "reasons"
                ),
                "stated_limit": (
                    "calibration rows are continuous proportions "
                    "where trial rows are token counts: the two row "
                    "kinds share the same centre and the same "
                    "per-column variance by construction, but their "
                    "higher moments differ; the difference is stated "
                    "openly in spec section 8, not hidden. The "
                    "calibration also sits at the positive control's "
                    "level (generated population, rarefaction, "
                    "median of draw statistics), removing the "
                    "population-versus-cell weighting difference "
                    "Spec 061 section 8 recorded (DD-062-5)"
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
                "summing exactly to the total (DD-061-3 carried; "
                "exact in integers at integer multiples); the full "
                "grid table is published either way"
            ),
            "operative_target": (
                "this spec's operative target is the larger returned "
                "target; a single returned target is operative with "
                "its scenario condition; no returned target leaves "
                "no operative target under this spec (the DD-061-5 "
                "rule carried as this spec's own). Spec 061's T* "
                "stays undefined on Spec 061's record regardless of "
                "anything this spec returns, and whether a returned "
                "operative target arms Arm A2 is the owner's "
                "decision at the mini planning gate a fired trigger "
                "queues under E-3 - never an act of this spec"
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
                "test, is not part of Spec 062 (campaign decision "
                "E-3, carried by DD-062-6)"
            ),
            "trigger": (
                "a successor operative target, if Spec 062's "
                "computation returns one, is recorded for the "
                "weekly data watch; a fired trigger (Phase-130-"
                "verified new non-Harappa intake reaching the "
                "operative target) queues a mini planning gate "
                "under E-3 at which the owner decides afresh - "
                "the arm does not join any pass and does not "
                "execute, and recording a target arms nothing by "
                "itself"
            ),
            "registration": (
                "the rerun's test is already frozen and registered "
                "(osf.io/7m35w); no new registration is filed for A2"
            ),
        },
        "freeze_does_not": (
            "the freeze computes nothing: no trial has run, no "
            "world has been built under this contract, no boost "
            "has been calibrated on the recorded population, gate "
            "0.5-R has not run, and no target has been estimated or "
            "peeked at; it does not patch Spec 061, re-run, "
            "re-adjudicate, or edit Spec 028 Arm A, whose "
            "INCONCLUSIVE verdict stands exactly as recorded; it "
            "arms nothing - Arm A2 stays unarmed and undesigned"
        ),
        "execution_gate": (
            "Not satisfied at the freeze: execution (Phase-424) "
            "begins only after this freeze has merged, the OSF "
            "registration's approval act has completed, and a "
            "separate execution order is given (DD-062-11)"
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
            "posture": "read at the freeze as the repaired "
                       "calibration's level of record (Arm A "
                       "positive control at the frozen boost 3.0 "
                       "over generated worlds: median adjusted R2 "
                       "0.023963353007570576); not a step-0 pin",
        },
        "pin_verification": (
            "at the freeze of 2026-10-21 every pin above was "
            "re-derived by two independent routes (contents-API raw "
            "and git-blob) at main "
            "b7a8c8a42d4e1137c04ef4c0123fb4ba4dbc3736, with the "
            "merged working tree agreeing as a third read; the "
            "routes agree byte-for-byte on every file and every "
            "hash equals its pin (freeze.md section 2)"
        ),
    },
    "environment": {
        "python": "3.12.3",
        "runner": "backend (venv glossa-lab)",
        "aee": "1.5.3 (the 1.5.x line; adopted environment; package pinned >=1.5.0,<1.6)",
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
    "backend/tests/test_spec062_freeze.py",
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
