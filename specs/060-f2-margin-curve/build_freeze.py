#!/usr/bin/env python3
"""Build the Spec 060 freeze record (freeze.json).

This builder was written at the freeze act of
2026-10-21 (the draft carried no builder and no
draft digest: the campaign's drafting wave opens
claims-first drafts only, and the digest is
computed over the recovered register exactly
once, at the freeze - the Spec 035 ordering).
Run with the Glossa backend venv python from the
repository root:

    python specs/060-f2-margin-curve/build_freeze.py

Writes specs/060-f2-margin-curve/freeze.json
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

SPEC_DIR = "specs/060-f2-margin-curve"

DEFINITION = {
    "spec": "specs/060-f2-margin-curve/spec.md",
    "freeze_doc": "specs/060-f2-margin-curve/freeze.md",
    "experiment_id": "spec060-f2-margin-curve",
    "register": {
        "path": "specs/060-f2-margin-curve/claims.json",
        "register_version": "0.7-draft",
        "claims": 15,
        "aee_hook_pass": (
            "PASSED at the freeze act of 2026-10-21 under aee 1.5.3: after_specify cleared in "
            "adjudicated rounds over the recovered register (a loadability recovery from 0.5-draft to "
            "0.6-draft - the draft's free-form evidence kind and source_quality labels are not engine "
            "values and the loader refuses them; 62 failure modes over 0.6-draft: 15 irreducibility, 30 "
            "independence-unmodelled, 1 negation-conflict, 1 counterexample, 15 FR-2.3 draft-cap "
            "records; head restatements within 0.7-draft cleared the remaining correctness records, "
            "the last a negation-conflict on F060-C04/F060-C12 cleared by restating F060-C12's head; 15 "
            "draft-cap records only over the final 0.7-draft), after_plan and after_tasks clean at "
            "first pass on the final register; at every hook zero correctness failure modes and no "
            "claim below the 0.70 threshold (minimum propagated 0.795); the engine outcome word reads "
            "iterate solely from the draft-cap records (gate reading DD-060-17; record in "
            "specs/060-f2-margin-curve/aee/freeze-aee-note.md)"
        ),
    },
    "basis": {
        "adjudication": "specs/060-f2-margin-curve/adjudication.md",
        "decisions": (
            "DECIDED by the owner on 2026-10-21 (not proposals): the runnable-experiments campaign "
            "plan approved AS WRITTEN (decision E-1; member 17) commissions the campaign of which "
            "design D-23 is a member; Spec 060 is D-23's specification. Draft decisions DD-060-1 to "
            "DD-060-5 and DD-060-9 are recorded in adjudication.md sections 5-6 and are confirmed at "
            "the freeze. Freeze decisions DD-060-10 to DD-060-17 are recorded in adjudication.md "
            "section 8: the spec's own OSF contract registration filed at the freeze under E-1 "
            "(DD-060-10); DD-060-2 confirmed - TOO THIN closes arm 2 only (DD-060-11); DD-060-3 "
            "confirmed - the shared type is SEAL, the Holdat layer's constant (DD-060-12); DD-060-4 "
            "confirmed - period mix stands as stated-unavailability per layer and no period "
            "assignment is imported from any other source (DD-060-13); no fresh synthetic calibration "
            "beyond gate 0.3 (DD-060-14); the execution venue named as the owner's machines at the "
            "Phase-137 loaders' default paths, both held copies verified at the freeze to hash "
            "exactly to their recorded pins (DD-060-15); Phase-422 allocated (DD-060-16); and the "
            "DD-038-10 AEE gate reading adopted as DD-060-17. The D-20 correction of adjudication "
            "section 2 stands exactly as drafted: arm 2 is written against Spec 034's finished "
            "composition result, never against a pending D-20."
        ),
    },
    "design": {
        "phase": "Phase-422",
        "act": (
            "recompute the Phase-384 v2 bounded interval estimate for F2 on the full Holdat "
            "population and report the verdict as a function of the margin on the fixed grid (arm 1, "
            "a sensitivity display), and compute each layer's site-effect interval on the shared "
            "population of spec section 5.2 under identical code and compare the two governing "
            "intervals (arm 2), reaching exactly one of arm 2's three pre-registered outcomes"
        ),
        "claim_under_test": {
            "id": "STUDY-SPEC-024/F2-HOLDAT",
            "record": (
                "SETTLED - CONTRADICTED at the declared margin 0.10: Phase-384 v2 governing basic "
                "interval [0.058939204306206666, 0.0777941604081594], point V 0.11539837515155221, "
                "n = 1,670 Holdat inscriptions; family sibling STUDY-SPEC-024/F3-ICIT stands "
                "SUPPORTED at the same margin (governing interval [0.18229651053139323, "
                "0.21036863506165235], point V 0.21900847512892316, n = 5,410)"
            ),
        },
        "hypothesis": (
            "on the population the two layers share (same sites, same object types), the Holdat "
            "effect and the ICIT effect move toward each other - the layer disagreement is "
            "substantially a composition difference"
        ),
        "falsifier": (
            "on the shared population the two layers' governing intervals still exclude each other "
            "(COMPOSITION DOES NOT) - stated under the corrected hand-off of spec section 2.3: the "
            "outcome stands alongside Spec 034's finished attribution (D-20 complete, Phase-398, "
            "ATTRIBUTED TO COMPOSITION on 169 matched objects, all Mohenjo-daro seals, median "
            "distance 0.025694, residual 0.040340), both statements stand, and no successor study is "
            "designed, registered, or implied"
        ),
        "arm1_margin_curve": (
            "the Phase-384 v2 estimator unchanged (populations built by the Phase-137 module's own "
            "loaders and frozen population rule; inscription-level bootstrap within site, site sizes "
            "fixed, B = 9,999, seed 20261012, the basic bootstrap interval governing), reported on "
            "the fixed grid 0.05 / 0.075 / 0.10 / 0.125 / 0.15 with each cell worded by the frozen "
            "family rule (CONTRADICTED AT m if the governing interval's upper bound is below m; "
            "SUPPORTED AT m if its lower bound is above m; STRADDLES m otherwise), labelled "
            "sensitivity in every output; the recorded verdict at 0.10 stands and no cell replaces it"
        ),
        "shared_population": {
            "sites": (
                "the sites present in both layers' Phase-137 analysis populations - on the record "
                "six sites (Chanhu-daro, Dholavira, Harappa, Kalibangan, Lothal, Mohenjo-daro), "
                "re-derived from the pinned layers at gate 0.4 rather than trusted from the text"
            ),
            "type_ruling": (
                "DD-060-12 (OPEN-060-4 resolved): DD-060-3 is CONFIRMED - the Phase-137 record "
                "states verbatim that the Holdat layer carries no object-type field and its "
                "inscriptions are seal texts, so the type mix is a constant; the type present in "
                "both layers is SEAL, the Holdat side enters whole, and the ICIT side is restricted "
                "to its recorded SEAL type class (the Phase-137 loader's type class, from the "
                "recorded type field); no inscription is re-typed and no other type class enters"
            ),
            "measurement": (
                "the site-effect size is computed in each layer separately with identical code "
                "(the Phase-384 v2 estimator), each layer in its own sign numbering; the two layers' "
                "signs are never pooled, mapped, or harmonised, and the comparison is of the two "
                "governing intervals only"
            ),
        },
        "period_ruling": (
            "DD-060-13 (OPEN-060-4 resolved): DD-060-4 is CONFIRMED - neither Phase-137 loader "
            "reads a period field (Holdat fields used: letters, position, seal_id, site; ICIT "
            "fields used: text, site, type; the Phase-137 record's confounder statement records "
            "period as not available in these layers), so where a layer carries no period field "
            "the outcome states PERIOD MIX NOT DESCRIBED FOR THIS LAYER - FIELD NOT CARRIED, period "
            "is never treated as controlled, and no period assignment is imported from any other "
            "source, including any Spec 041-style assignment"
        ),
        "calibration_ruling": (
            "DD-060-14 (OPEN-060-2 resolved): gate 0.3 - exact reproduction of both recorded "
            "governing intervals by the unchanged estimator on the two full populations - is this "
            "spec's estimator check; no fresh synthetic calibration is required beyond it, and none "
            "may be introduced at execution as a gate"
        ),
        "venue_ruling": (
            "DD-060-15 (OPEN-060-3 resolved): the execution venue is the owner's machines at the "
            "Phase-137 loaders' default paths as recorded in the Phase-137 results (the Holdat copy "
            "under the program checkout's corpora/downloads/external_repos/holdatllc_indus/, the "
            "ICIT copy under the research-notes sweep downloads/horus84-computational-linguistics/"
            "data/); at the freeze both copies at those paths hash exactly to the section 3 pins, "
            "and gate 0.1 asserts the execution venue's copies against the same pins; no other copy "
            "is authoritative"
        ),
        "outcomes_arm2": [
            "COMPOSITION EXPLAINS THE GAP",
            "COMPOSITION DOES NOT",
            "TOO THIN",
        ],
        "too_thin_ruling": (
            "DD-060-11 (OPEN-060-4 resolved): DD-060-2 is CONFIRMED - the gate-0.4 floors (fewer "
            "than 5 shared sites or fewer than 500 inscriptions in either layer) close arm 2 only, "
            "with the counts stated; arm 1 is independent of the shared census and still reports"
        ),
        "step0_gates": (
            "fail-closed, in order, before any arm quantity (spec section 4): gate 0.1 input "
            "integrity - every section 3 input hashes to its stated value, the two held layer "
            "files to the values recorded in the Phase-137 results, a mismatch stops the run as "
            "INVALID; gate 0.2 population reproduction, both layers - the Phase-137 loaders and "
            "frozen population rule reproduce each recorded profile table exactly (Holdat 1,670 "
            "inscriptions, 9 x 98, chi2 745.953, V 0.1154; ICIT 5,410 inscriptions, 7 x 187, chi2 "
            "4966.362, V 0.2190), a mismatch stops the run as INVALID; gate 0.3 estimator regression "
            "- the Phase-384 v2 estimator run unchanged on the two full-layer populations "
            "reproduces the recorded governing intervals exactly, a mismatch stops the run as "
            "INVALID; gate 0.4 shared-population census - a thin census closes arm 2 as TOO THIN "
            "only; nothing is repaired at run time"
        ),
        "freeze_does_not": (
            "this freeze does not itself compute anything: no margin-curve cell beyond the recorded "
            "0.10 adjudication, no shared-population quantity, and not the gate-0.4 census, which "
            "remains an execution act; it moves no verdict (F2 stands CONTRADICTED at 0.10 and F3 "
            "stands SUPPORTED at 0.10 exactly as recorded), re-runs no part of Spec 034, and "
            "imports no period assignment"
        ),
        "execution_gate": (
            "Not satisfied at the freeze of 2026-10-21: execution runs as Phase-422 only after "
            "this freeze has merged, the OSF contract registration's approval act has completed "
            "(the parent's approval click on OSF's admin notification), and a separate execution "
            "order is given, in campaign Wave 3 group 2"
        ),
    },
    "inputs": {
        "holdat_layer": {
            "file": "indus_corpus 2.csv (holdatllc_indus export, held file - not in this repository)",
            "sha256": "62d14d2bebf7c2c80d98a2958e75ec52bff3f240ff3f5e85d1f7f40cbe28218e",
            "posture": (
                "the pin is the value recorded in reports/phase137_results.json (F2 input.sha256); "
                "at the freeze the held copy at the Phase-137 loader's default path hashes exactly "
                "to this value (DD-060-15), and gate 0.1 re-asserts the execution venue's copy"
            ),
            "population": "7,002 token rows; 1,670 analysis inscriptions at 9 eligible sites; profile table 9 x 98; chi2 745.953; V 0.1154",
        },
        "icit_layer": {
            "file": "inscriptions.csv (horus84, held file - not in this repository)",
            "sha256": "c368f290d8d784093d804243100de27ae6ad09df3ae37cab7432a0205d4ec9ef",
            "posture": (
                "the pin is the value recorded in reports/phase137_results.json (F3 input.sha256); "
                "at the freeze the held copy at the Phase-137 loader's default path hashes exactly "
                "to this value (DD-060-15), and gate 0.1 re-asserts the execution venue's copy"
            ),
            "population": "5,679 rows; 5,410 analysis inscriptions at 7 eligible sites; profile table 7 x 187; chi2 4966.362; V 0.2190",
        },
        "phase137_results": {
            "file": "reports/phase137_results.json",
            "sha256": "18f86f45892526b947a4a7447201be9d69584ec96d33a1d18139309b9dc2a7a1",
        },
        "phase137_machinery": {
            "file": "backend/scripts/phase137_site_repertoire.py",
            "sha256": "e00dacf4df8f52871b482e36ca0a37f66503c5f1b107ee835ac99fa21dfc8c86",
        },
        "phase384_results": {
            "file": "reports/phase384_results.json",
            "sha256": "dda6092d9f4d368869a6e3a590948dfa97d02c5db50bf75868d6e055f0896aad",
            "f2_basic_ci95": [0.058939204306206666, 0.0777941604081594],
            "f2_percentile_ci95": [0.15300258989494483, 0.17185754599689756],
            "f2_bootstrap_median": 0.16180470665653984,
            "f3_basic_ci95": [0.18229651053139323, 0.21036863506165235],
        },
        "phase384_estimator": {
            "file": "backend/scripts/phase384_stage2_margins_v2.py",
            "sha256": "3313394e6a716898cdfd440a46333ebd2b9136b77306413ed1514eab322a72a5",
            "freeze_v2_sources_match": True,
        },
        "phase384_contract": {
            "file": "specs/026-rcph-framework-transfer/reruns/phase384-contract-v2.md",
            "sha256": "f0a67bd766ae28a33edc33553613bf9c50cc933df1bfbe2b5e1192d6571bbc75",
            "freeze_v2_sources_match": True,
        },
        "phase384_freeze_v2": {
            "file": "specs/026-rcph-framework-transfer/reruns/phase384-freeze-v2.json",
            "sha256": "5749c6b89ac26be6333e0c20457bc320ca624c15f5ca65e689c107aa12b7b8e9",
            "recorded_digest": "4e6c78bc917c96a3eeb80fc09e3345073dbaf38e809171f1f59041778784b28e",
        },
        "spec034_outcome": {
            "file": "specs/034-matched-object-attribution/outcome.md",
            "sha256": "c0cc615ddb062306aa43cc8441fe5c6c322b563badd351ebce54fed1d7b43175",
            "verdict": "ATTRIBUTED TO COMPOSITION",
            "matched_objects": 169,
            "median_distance": 0.025694,
            "residual": 0.040340,
            "slice": "all Mohenjo-daro seals",
            "freeze_digest": "696fd1855c8cbc1fe767fdc26a1697deb1f0dc85253376efdd7064f102594c2a",
        },
        "spec024_spec": {
            "file": "specs/024-evidence-integration/spec.md",
            "sha256": "a817f698fd5f2dd0a2d324d580d25cba41fc989762b20e0b77a4144a02d3ee25",
        },
        "anchors": {
            "file": "backend/reports/INDUS_FINAL_ANCHORS.json",
            "sha256": "df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569",
            "posture": "this spec moves no anchor; the file is asserted byte-identical before and after any execution",
        },
        "pin_verification": (
            "at the freeze of 2026-10-21 every repository pin above was re-derived by two "
            "independent routes (contents-API raw and git-blob) in the foreground at main "
            "a3509525fab64e22a4c053d7bbed14c7083a14d3; the two routes agree byte-for-byte on every "
            "file and every hash equals its pin (freeze.md section 2); the estimator and contract "
            "hashes also match the Phase-384 freeze-v2 sources record inside the pinned freeze-v2 "
            "file, and the two held-layer pins were verified against the held copies at the "
            "loaders' default paths, which hash exactly to the recorded values"
        ),
    },
    "environment": {
        "python": "3.12.3",
        "runner": "backend (venv glossa-lab)",
        "aee": "1.5.3 (venv glossa-aee153; package pinned >=1.5.0,<1.6)",
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
    "backend/tests/test_spec060_freeze.py",
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
