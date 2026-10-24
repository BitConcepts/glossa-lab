#!/usr/bin/env python3
"""Build the Spec 068 freeze record (freeze.json).

This builder was written at the freeze act of
2026-10-22. The register is the draft register
(0.5-draft) with the freeze's own rulings carried
in and two AEE recovery rounds completed
(0.8-draft), the AEE lifecycle hooks passed over
it at the freeze gate, and the digest is computed
over the recovered register exactly once, at the
freeze - the Spec 035 ordering. Run with the
Glossa backend venv python from the repository
root:

    python specs/068-yadav-zipf-controls-successor/build_freeze.py

Writes specs/068-yadav-zipf-controls-successor/freeze.json
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

SPEC_DIR = "specs/068-yadav-zipf-controls-successor"

DEFINITION = {
    "spec": "specs/068-yadav-zipf-controls-successor/spec.md",
    "freeze_doc": "specs/068-yadav-zipf-controls-successor/freeze.md",
    "experiment_id": "spec068-yadav-zipf-controls-successor",
    "register": {
        "path": "specs/068-yadav-zipf-controls-successor/claims.json",
        "register_version": "0.8-draft",
        "claims": 14,
        "aee_hook_pass": (
            "PASSED at the freeze act of 2026-10-22 under aee 1.5.3: the draft register "
            "(0.5-draft) carried the freeze's rulings in (DD-068-7 limb B into F068-C01, "
            "C02, C06, C11; DD-068-8 pins into F068-C03, C05; DD-068-11 controls into "
            "F068-C08) and was recovered in two rounds the hooks forced (0.6-draft "
            "loadability: evidence normalised to kind observed / source_quality "
            "artifact with mutual independent_of declarations; 0.7-draft: 13 challenged "
            "heads restated as single propositions, carried clauses in boundaries; "
            "0.8-draft: 4 remaining heads tightened); after_specify, after_plan and "
            "after_tasks were then each clean - at every hook 14 FR-2.3 draft-cap "
            "records only, zero correctness failure modes, and no claim below the 0.70 "
            "threshold (minimum propagated 0.795); the engine outcome word reads "
            "iterate solely from the draft-cap records (gate reading DD-068-10, "
            "adopting DD-038-10 as in DD-053-19; record in "
            "specs/068-yadav-zipf-controls-successor/aee/freeze-aee-note.md)"
        ),
    },
    "basis": {
        "adjudication": "specs/068-yadav-zipf-controls-successor/adjudication.md",
        "decisions": (
            "DECIDED by the owner on 2026-10-22 (not proposals): Amendment S-053 "
            "carries Spec 053's frozen control-systems comparison onto the Shakti "
            "corpus as this successor, under the owner's 2026-10-22 readiness "
            "decisions (decision 2; decision 2c: the result is a new baseline, "
            "neither confirming nor correcting Phase-43) and the P-F1 intake gates "
            "S1-S4 adopted the same day. Draft decisions DD-068-1 to DD-068-6 are "
            "recorded in adjudication.md section 5 and are confirmed at the freeze. "
            "Freeze decisions DD-068-7 to DD-068-13 are recorded in adjudication.md "
            "section 7: OPEN-068-1 ruled LIMB B - the strict-sign-set restriction "
            "dropped openly, the population stated as the full ICIT sign inventory "
            "of the restricted corpus, limb A considered and not taken (DD-068-7); "
            "the intake record and pins re-asserted against the merged record, with "
            "the claim file re-pinned at its current hash on an open discrepancy "
            "record (DD-068-8); DD-068-1 to DD-068-6 confirmed as drafted "
            "(DD-068-9); the DD-038-10 AEE gate reading adopted (DD-068-10); the "
            "four control systems confirmed as named (DD-068-11); the spec's own "
            "OSF contract registration filed at the freeze (DD-068-12); Phase-430 "
            "allocated (DD-068-13)."
        ),
    },
    "design": {
        "phase": "Phase-430",
        "act": (
            "run the step-0 gates of spec section 4 in order - input integrity, the "
            "estimator self-test, the Shakti intake gates S1 and S2 asserted against "
            "the intake record, the limb-B population act, the control set entered "
            "whole as cited data and frozen, and the census floors - and, only if "
            "every gate passes, fit every system under Spec 053's one frozen "
            "estimator, apply the frozen comparison rule and positive-control "
            "condition on the primary fit, and report the grade sensitivity and "
            "subsampling in full beside it, reaching exactly one of the "
            "pre-registered outcomes of spec sections 7 and 11"
        ),
        "claim_under_test": {
            "id": "yadav_2009_arxiv_manual_001",
            "record": (
                "SETTLED - strongly supported, stage explained, on its recorded test: "
                "the recorded evidence string reads 'Phase-43: V3 Zipf exponent ~1.35 "
                "(super-Zipfian) [VERIFIED]'. This successor tests only the residue "
                "Spec 053 tested - what that recorded fit is worth against named "
                "controls - and appends its outcome as a dated bounded finding (a "
                "strength label); it changes no verdict and no recorded field"
            ),
        },
        "falsifier": (
            "at least one named non-linguistic control system fits the "
            "Zipf-Mandelbrot curve as well as or better than the Indus primary fit "
            "(its NRMSE_log less than or equal to the Indus primary NRMSE_log, "
            "epsilon = 0, the synthetic control by its replicate median), under the "
            "one estimator frozen by Spec 053"
        ),
        "population": {
            "ruling": (
                "DD-068-7 (OPEN-068-1 resolved): LIMB B - the strict-sign-set "
                "restriction is dropped, openly. The fitted population is the full "
                "ICIT sign inventory of the restricted corpus; no mapping act is "
                "performed, no mapping basis source is named, and no output may "
                "describe the population as a strict population. Limb A (the strict "
                "set retained, keyed to ICIT space by a mapping act stated and "
                "pinned at step 0) was considered and not taken; STRICT MAPPING NOT "
                "PINNABLE cannot fire under limb B, and spec section 6.3 has no "
                "separate full-inventory fit because the primary already is that fit"
            ),
            "primary": (
                "analyzable documented-lineage rows of the Shakti corpus, counting "
                "every token by ICIT sign type (draft-derived expectation, governed "
                "over by the step-0 census: 3,212 rows, 3,045 analyzable)"
            ),
            "sensitivity": (
                "analyzable documented-lineage + undocumented-corroborated rows "
                "under the same limb (draft-derived expectation: 5,299 rows, 5,131 "
                "analyzable), reported in full beside the primary; a differing "
                "verdict-relevant ordering is reported as grade-sensitivity under "
                "P-F1 S4 and never changes the headline word"
            ),
            "excluded": (
                "rows graded undocumented-uncorroborated (405) enter no fit, count, "
                "statistic, or argument (P-F1 S4)"
            ),
        },
        "intake": {
            "record": "docs/decisions/2026-10-22-shakti-corpus-intake-record.md",
            "record_sha256": "bd14e2b1f0607366ca1845797bcd17f8b577d23140a2e3111fe0cc2652cf9a9d",
            "standing": (
                "asserted at the freeze (DD-068-8): the record stands on the merged "
                "record (main, merged by PR #339 at merge commit bfc811df) carrying "
                "the P-F1 gates S1-S4 in their adopted form and both SHA-256 pins "
                "exactly as spec section 2.1 states them"
            ),
            "corpus": {
                "file": "sanitized_corpus.json (ShaktiOSindia deposit; restricted-local, never committed)",
                "sha256": "345241b13fedada87b4783c24cd241123491bbd7edaf5bf636f9cdb36c01da68",
                "bytes": 1570041,
            },
            "row_grades": {
                "file": "shakti_row_grades_2026-10-22.csv (provenance audit of 2026-10-22; restricted-local, never committed)",
                "sha256": "02394241773cf8700f49ba19c30cdbaa589cf119d2c97c35e15e0447434dd739",
            },
            "census": (
                "5,704 rows; 5,536 analyzable; grades 3,212 documented-lineage / "
                "2,087 undocumented-corroborated / 405 undocumented-uncorroborated; "
                "4,904 of 5,536 analyzable rows (88.6%) carrying a CISI identifier; "
                "18,065 true sign tokens; 713 distinct signs; 77 sites (the intake "
                "record's census, asserted at gate 0.4 under P-F1 S2)"
            ),
            "lineage_statement": (
                "This corpus is an ICIT-lineage corpus. Agreement between it and the "
                "program's earlier ICIT-lineage layer is consistency within one "
                "tradition, not independent corroboration. (P-F1 S3, verbatim, first "
                "in the headline block of every product)"
            ),
        },
        "estimator": (
            "identical to Spec 053's frozen estimator (DD-053-11; F068-C07): the "
            "Zipf-Mandelbrot model f_hat(r) = C / (r + q)^alpha with C fixed by "
            "normalisation (sum f_hat = N), fitted by minimising SSE = sum of squared "
            "log residuals over the deterministic grid alpha 0.00-3.00 in steps of "
            "0.01 and q 0.0-20.0 in steps of 0.1, then one refinement pass at "
            "one-tenth steps in alpha and q around the best grid cell; types ranked "
            "by count descending, ties by type identifier ascending; primary "
            "quantity NRMSE_log = sqrt(SSE / V); secondary R2 in log space and the "
            "fitted alpha, reported and never decisive. The gate 0.2 self-test "
            "(planted alpha 1.20, q 2.0, V 200, N 50,000, seed 20261021, by the "
            "stated multinomial procedure; pass iff alpha is recovered within 0.10 "
            "and q within 1.0) is carried unchanged"
        ),
        "controls": {
            "ruling": (
                "DD-068-11 (OPEN-068-5 resolved), carrying DD-053-13: the named "
                "systems stand, no system is replaced, no second positive control is "
                "added, and gate 0.6 is the fixed pin source for the exact tables "
                "and per-count locators - the tables are entered whole as cited data "
                "at gate 0.6, before any fit, and a system that cannot be entered "
                "whole closes the run CONTROL SET FREEZE FAILED"
            ),
            "N1": (
                "Mesopotamian numerical signs: token frequencies of numerical signs "
                "from published counts of archaic Mesopotamian administrative "
                "tablets (bibliographic pin: Nissen, Damerow & Englund, Archaic "
                "Bookkeeping (1993) and the published archaic sign counts it "
                "reports); numerical signs only"
            ),
            "N2": (
                "heraldic charges: frequencies of charges (the devices borne on "
                "shields) across a published roll of arms, the roll and edition "
                "entered with their citation at gate 0.6; counting unit one charge "
                "occurrence on one shield, as the roll records it"
            ),
            "N3": (
                "synthetic emblem inventory (DD-053-6, confirmed DD-053-16): a "
                "Yule-Simon process with innovation probability rho = 0.10, seed "
                "20261021, run to exactly the Indus primary fit's token total N; 99 "
                "replicates, each a separate system instance; N3's fit quantities "
                "are the medians across replicates, with the replicate distribution "
                "and the as-well share reported"
            ),
            "P1": (
                "linguistic positive control: Linear B syllabic sign frequencies "
                "from published corpus counts, the exact source entered with its "
                "citation at gate 0.6; no second positive control"
            ),
        },
        "comparison": (
            "Spec 053 sections 4.3-4.5 as frozen (DD-053-15, DD-053-19): a "
            "non-linguistic control fits as well iff its NRMSE_log is less than or "
            "equal to the Indus primary NRMSE_log (epsilon = 0, no tolerance band); "
            "the falsifier fires iff at least one of N1, N2, N3 fits as well; the "
            "gap Delta = E_control - E_Indus is reported for every control and "
            "0 < Delta <= 0.02 is named a NEAR MISS (reporting only); the "
            "positive-control condition is E_P1 strictly less than every "
            "non-linguistic control's error; the headline is SEPARABLE iff P1 "
            "passes and the falsifier does not fire, NOT SEPARABLE iff P1 passes "
            "and it fires, COMPARISON UNINFORMATIVE iff P1 does not pass - "
            "computed on the primary fit alone, in spec section 7's pre-written "
            "wordings"
        ),
        "floors": (
            "carried from Spec 053 (DD-053-7, confirmed DD-053-14), measured on the "
            "restricted set's fit population at gate 0.7: the primary proceeds only "
            "if distinct types present >= 50 and tokens >= 2,000; below either "
            "floor the execution closes as TOO THIN with the census as its "
            "finding; no floor applies to a control or to the sensitivity set"
        ),
        "sensitivities": (
            "the grade sensitivity of spec section 6.1 in full beside the primary "
            "(both orderings exhibited; a differing ordering is grade-sensitivity "
            "under P-F1 S4, quoted with its section 6.1 sentence wherever the "
            "headline is quoted); the subsampling tables of spec section 6.2 for "
            "both populations (random halves and quarters of inscriptions, 99 "
            "replicates per level, seed 20261021, sampling without replacement; "
            "median and central 90% interval of fitted alpha and NRMSE_log); no "
            "section 6.3 fit exists under limb B and no fit is reported beside "
            "any Phase-43 quantity in any case"
        ),
        "outcomes": [
            "SEPARABLE",
            "NOT SEPARABLE",
            "COMPARISON UNINFORMATIVE",
            "TOO THIN",
            "SHAKTI INTAKE NOT REPRODUCED",
            "CONTROL SET FREEZE FAILED",
            "INVALID",
        ],
        "step0_gates": (
            "fail-closed, in order, before any fit quantity (spec section 4): gate "
            "0.1 input integrity - every section 3 pin hashes to its freeze-record "
            "value (the claim file at its DD-068-8 re-pinned hash), the intake "
            "record stands as section 3 requires, and the anchors file is asserted "
            "byte-identical, or INVALID; gate 0.2 the estimator self-test, or "
            "INVALID; gate 0.3 Shakti intake identity (P-F1 S1: both SHA-256 pins "
            "recompute), or SHAKTI INTAKE NOT REPRODUCED; gate 0.4 Shakti intake "
            "census (P-F1 S2) plus this successor's own restricted census, which "
            "governs over the draft's derived figures, or SHAKTI INTAKE NOT "
            "REPRODUCED; gate 0.5 the population act under limb B (the step-0 "
            "record states the population as the full ICIT sign inventory of the "
            "restricted corpus with its measured distinct-sign count); gate 0.6 "
            "the control set entered whole as cited data and frozen, or CONTROL "
            "SET FREEZE FAILED; gate 0.7 the census floors on the restricted set, "
            "or TOO THIN; nothing is repaired at run time"
        ),
        "freeze_does_not": (
            "this freeze does not itself fit anything: no census has been taken by "
            "this spec, no control count entered, no synthetic replicate "
            "generated, and no fit quantity exists; it establishes nothing about "
            "the old corpus or Phase-43 (the result is a new baseline only, "
            "decision 2c); it does not revive limb A by the back door; and it "
            "edits no Spec 053 record, no claim field, and no intake gate"
        ),
        "execution_gate": (
            "Execution runs as Phase-430 under the owner's execution order of "
            "2026-10-22, given with the freeze rulings, after this freeze has "
            "merged and the OSF contract registration (DD-068-12) has been filed. "
            "The registration stands pending approval after filing; its approval "
            "act is the owner's approval click on OSF's admin-notification email, "
            "and the registration's pending state at execution is recorded in the "
            "outcome record as it stands (freeze.md section 7 states the gate "
            "exactly, including the departure from the earlier specs' wait-for-"
            "approval posture, which is this commission's to order)"
        ),
    },
    "inputs": {
        "spec053_freeze": {
            "file": "specs/053-yadav-zipf-controls/freeze.json",
            "digest": "fd2d5cb86b6aed51882a945719bb747ac34f149b08a21e6485b1407c6dc6b309",
        },
        "claim_record": {
            "file": "glossa-indus/claims/extracted_claims/yadav_2009_arxiv.json",
            "sha256": "ec31778a75cbc56f27f385ed7da800edb874a8f600cbe102f46087a8159d6239",
            "bytes": 15104,
            "posture": (
                "re-pinned at this freeze (DD-068-8): Spec 053's freeze pin "
                "904766238d4aec8fecf0a01dc7c8935689f378e31062485edc699874a36847a3 no "
                "longer recomputes - the file's bytes changed after that freeze by "
                "re-extraction timestamps (2026-10-21) and the Spec 025 audit "
                "appends (commit 51cf8b3c, 2026-10-22); manual_001's recorded "
                "status, evidence string, falsifier text, and stage were verified "
                "field-by-field unchanged against the pinned version, and the "
                "freeze re-pins the file at the current hash for gate 0.1"
            ),
        },
        "anchors": {
            "file": "backend/reports/INDUS_FINAL_ANCHORS.json",
            "sha256": "df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569",
            "bytes": 570344,
            "anchors": 287,
            "strict_sa_independent": 94,
            "posture": (
                "cited for the record of what limb B drops (DD-068-7); operative "
                "for no fit under limb B; this spec moves no anchor and the file is "
                "asserted byte-identical before and after any execution"
            ),
        },
        "crosswalk": {
            "file": "data/crosswalks/sign_crosswalk_master.csv",
            "sha256": "4ace1a617f40afe8d0bbb82e5461d98a675296152e7577b04fb67b00f4f5dfcf",
            "bytes": 18568,
            "posture": (
                "cited for numbering questions only; not a split/merge variant "
                "source for this successor (adjudication.md section 6, defect 4)"
            ),
        },
        "local_store": {
            "posture": (
                "the Shakti corpus and the row-grades file are held restricted-"
                "local under the corpus's GPL-3.0 terms and are never committed; "
                "their pins are carried as the definition constants in "
                "design.intake (the Spec 038 form), asserted on the held files at "
                "the freeze by sha256sum and re-asserted at execution gates "
                "0.3-0.4 against the intake record"
            ),
            "corpus_sha256": "345241b13fedada87b4783c24cd241123491bbd7edaf5bf636f9cdb36c01da68",
            "row_grades_sha256": "02394241773cf8700f49ba19c30cdbaa589cf119d2c97c35e15e0447434dd739",
        },
        "pin_verification": (
            "at the freeze of 2026-10-22 every committed pin above was re-derived "
            "by two independent routes (the worktree file and the git-blob route) "
            "at the freeze tree (the draft branch with origin/main merged in at "
            "bfc811df), and the restricted-local pins were recomputed on the held "
            "files by sha256sum; all routes agree (freeze.md section 2)"
        ),
    },
    "environment": {
        "python": "3.12.3",
        "runner": "backend (venv glossa-lab)",
        "aee": "1.5.3 (adopted environment; package pinned >=1.5.0,<1.6)",
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
    "backend/tests/test_spec068_freeze.py",
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
