#!/usr/bin/env python3
"""Build the Spec 058 freeze record (freeze.json).

This builder was written at the freeze act of
2026-10-21 (the draft carried no builder and no
draft digest: the campaign's drafting wave opens
claims-first drafts only, and the digest is
computed over the recovered register exactly
once, at the freeze - the Spec 035 ordering).
Run with the Glossa backend venv python from the
repository root:

    python specs/058-transcription-disagreement-mechanism/build_freeze.py

Writes specs/058-transcription-disagreement-mechanism/freeze.json
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

SPEC_DIR = "specs/058-transcription-disagreement-mechanism"

AEE_HOOK_PASS = (
    "PASSED at the freeze act of 2026-10-21 under aee 1.5.3: after_specify cleared in "
    "adjudicated rounds over the recovered register (a loadability recovery from 0.5-draft to "
    "0.6-draft - the draft's free-form evidence kind and source_quality labels are not engine "
    "values and the loader refuses them; round 1 over 0.6-draft: 31 failure modes - 13 "
    "irreducibility, 2 counterexample (absolute-language) on F058-C12/C13, 16 FR-2.3 draft-cap "
    "records; recovery to 0.7-draft restated the 13 challenged heads as single propositions; "
    "round 2: 21 failure modes - 5 irreducibility remaining, draft-cap only otherwise; recovery "
    "to 0.8-draft restated those five heads in final single-proposition form); after_specify, "
    "after_plan and after_tasks each carry exactly 16 FR-2.3 draft-cap records over 0.8-draft; "
    "at every hook zero correctness failure modes and no claim below the 0.70 threshold "
    "(minimum propagated 0.72); the engine outcome word reads iterate solely from the "
    "draft-cap records (gate reading DD-058-18; record in "
    "specs/058-transcription-disagreement-mechanism/aee/freeze-aee-note.md)"
)

DEFINITION = {
    "spec": "specs/058-transcription-disagreement-mechanism/spec.md",
    "freeze_doc": "specs/058-transcription-disagreement-mechanism/freeze.md",
    "experiment_id": "spec058-transcription-disagreement-mechanism",
    "register": {
        "path": "specs/058-transcription-disagreement-mechanism/claims.json",
        "register_version": "0.8-draft",
        "claims": 16,
        "aee_hook_pass": AEE_HOOK_PASS,
    },
    "basis": {
        "adjudication": "specs/058-transcription-disagreement-mechanism/adjudication.md",
        "decisions": (
            "DECIDED by the owner on 2026-10-21 (not proposals): the runnable-experiments campaign "
            "plan approved AS WRITTEN (decision E-1; member 15) commissions the campaign of which "
            "design D-21 arm A is a member; Spec 058 is D-21 arm A's specification. Draft decisions "
            "DD-058-1 to DD-058-9 and DD-058-13 are recorded in adjudication.md section 4 and are "
            "confirmed at the freeze. Freeze decisions DD-058-14 to DD-058-19 are recorded in "
            "adjudication.md section 7: the spec's own OSF contract registration filed at the "
            "freeze under E-1, resolving DD-058-10 (DD-058-14); DD-058-11 resolved - the Phase-132 "
            "store record set survives complete on the main-checkout machine, proven at the freeze "
            "by inventory and exact reproduction, and production is deferred to execution gate 0.2 "
            "exactly as drafted with no store bytes pinned and no separate preservation act "
            "ordered first (DD-058-15); DD-058-12 resolved - gates 0.4-0.6 suffice, no separate "
            "margins/census audit (DD-058-16); Phase-420 allocated (DD-058-17); the DD-038-10 AEE "
            "gate reading adopted (DD-058-18); and DD-058-1 to DD-058-9 and DD-058-13 confirmed as "
            "drafted, including the segmentation proxy (DD-058-3), the involvement basis "
            "(DD-058-6), the object-type locus rule (DD-058-8), and the MULTIPLE LOCI combination "
            "class (DD-058-9) (DD-058-19)."
        ),
    },
    "design": {
        "phase": "Phase-420",
        "act": (
            "re-analyse the recorded Phase-132 pilot passes of Spec 023 under spec sections 3-5: "
            "produce and prove the store record set at step 0, align the two passes with the "
            "frozen machinery, tabulate mismatch events by sign, object type, and divergence "
            "type, and record exactly one headline of spec section 5.2"
        ),
        "claim_under_test": {
            "id": "STUDY-SPEC-023/PHASE-132+383",
            "record": (
                "SETTLED - CONTRADICTED: Phase-132 pilot exact-sequence agreement 0.20 (10/50, P "
                "and M) against the frozen 0.80 floor - the stop-rule fired; per-token agreement "
                "0.4798 (95/198) all-50 and 0.4286 (18/42) gold; gold error estimator 0.05 (2/40); "
                "Phase-383 bootstrap interval for exact-sequence agreement [0.10, 0.32] "
                "(B = 9,999, seed 20261011); every coder an AI agent of a single model family "
                "(Phase-383 origin-group audit: effective independent coder origin groups = 1)"
            ),
            "residue": (
                "why the passes disagreed is not understood at the level of mechanism: which "
                "signs, objects or segmentation choices drive the disagreement (the claim's "
                "adopted lane-2 record); the 0.80 floor's correctness and any codebook question "
                "are excluded by spec section 8"
            ),
        },
        "hypothesis": (
            "the disagreement is concentrated, not uniform - a minority of signs or object types "
            "accounts for the majority of sequence mismatches (design D-21 arm A, verbatim in "
            "substance)"
        ),
        "falsifier": (
            "the recorded pilot passes do not localise the disagreement to signs, object types, "
            "or segmentation choices: no locus rule of spec section 5.1 fires, and the outcome "
            "is recorded as NOT LOCALISED with the deciding shares stated"
        ),
        "store": {
            "ruling": (
                "DD-058-15 (DD-058-11 resolved): the Phase-132 local store survives complete on "
                "the machine holding the program's main checkout, at "
                "corpora/downloads/cisi_image_layer/phase132_pilot/ (gitignored); inventoried "
                "read-only at the freeze (frame.json, 50 pass_a, 50 pass_b, 10 pass_gold, 50 "
                "adjudication records, effort_log.csv with 320 events - the pilot report section "
                "9 inventory) and proven to be the pilot's record set by exact reproduction of "
                "the committed metrics in full, the adjudication taxonomy (identity 93, "
                "legibility 45, count 11, key 10, orientation 2, order 1; total 162), and frame "
                "identity against the committed frame, all with the pinned machinery"
            ),
            "production": (
                "deferred to execution gate 0.2 exactly as drafted: the freeze produces, "
                "preserves, and pins no store bytes; preservation of the set as a committed, "
                "hashed record is not ordered as a separate act first and remains the named "
                "unblocking act if gate 0.2 fires; the execution venue is the machine holding "
                "the program's main checkout, or the venue the execution order names with the "
                "store produced there; gate 0.2's inventory and per-file SHA-256 manifest, and "
                "gates 0.3-0.5, remain the operative production proof, fail-closed"
            ),
            "layout": (
                "frame.json; pass_a/<canonical-key>.json x 50; pass_b/<canonical-key>.json x 50; "
                "pass_gold/<canonical-key>.json x 10; adjudication/<canonical-key>.json x 50; "
                "effort_log.csv - the layout the frozen metrics module's loader defines"
            ),
        },
        "step0_gates": (
            "fail-closed, in order, before any localisation quantity (spec section 3): gate 0.1 "
            "committed-record integrity - a section 2.1 hash mismatch stops the run as INVALID; "
            "gate 0.2 pilot-pass record production - the store record set produced and "
            "inventoried against the pilot report section 9 counts with a per-file SHA-256 "
            "manifest; a shortfall closes as PILOT-PASS RECORDS NOT PRODUCIBLE, unscored; gate "
            "0.3 frame identity - the produced frame differs from the committed frame: INVALID; "
            "gate 0.4 reproduction - the frozen metrics module computes the committed metrics "
            "from the produced set exactly (0.20 P and M, 0.4798, 0.4286, estimator 0.05, totals "
            "191/190/40/189, every per-object flag and match count): INVALID on any mismatch; "
            "gate 0.5 taxonomy cross-check (93/45/11/10/2/1, total 162): INVALID; gate 0.6 "
            "analysis census - the 40 mismatched objects published as the population every share "
            "is taken over; DD-058-16: gates 0.4-0.6 suffice, no separate margins/census audit; "
            "nothing is repaired at run time and no substitute source is admitted"
        ),
        "machinery": (
            "spec section 4: P space primary (Spec 023 section 5.6 freeze block); each token's "
            "P value is the crosswalk-v1 primary counterpart of its matched M (highest-confidence "
            "row, tie to lowest P number); UNK compares as UNK; an M with no crosswalk row "
            "compares as UNMAPPED:<M_ID>; alignment is the frozen module's minimum-edit "
            "alignment (unit cost; diagonal preferred over deletion over insertion); the pinned "
            "phase132_metrics.py is imported unchanged, per the Phase-383 precedent; M-space "
            "tabulations are a descriptive sensitivity only (DD-058-4)"
        ),
        "events": (
            "a mismatch event is an alignment column whose two sides are not equal values "
            "present on both sides: SUBSTITUTION when both sides are present and unequal (the "
            "event involves both values), INDEL when exactly one side is present (the event "
            "involves the one present value; insertion versus deletion is not distinguished); "
            "the event total E is the count over the 40 mismatched objects; the first "
            "mismatch-event column per mismatched object is its first divergence, tabulated "
            "descriptively and never verdict-bearing"
        ),
        "tabulations": (
            "T1 by sign: involvement counts per P-space value (a substitution counts once for "
            "each of its two values, an indel once for its present value), ranked by involvement "
            "with ties by value string ascending; the top-10 share is summed involvement of the "
            "10 highest-ranked values over summed involvement (DD-058-6, confirmed); the "
            "frequency share of the same 10 values is their share of the 381 tokens of both "
            "passes' full sequences (191 + 190). T2 by object type: events grouped by the "
            "frame's recorded type (Seals, Tablets, Unrecorded - the empty recorded value "
            "carried as recorded, never back-filled), with event share, object share, and "
            "mismatched-object counts. T3 by divergence type: SUBSTITUTION and INDEL counts "
            "and shares of E; the INDEL share is the registered segmentation proxy (DD-058-3, "
            "confirmed), carrying the spec section 8(4) limit wherever it is stated"
        ),
        "unk_handling": (
            "UNK and UNMAPPED:<M_ID> values are counted in the primary tabulations exactly as "
            "recorded (DD-058-7); a pre-registered descriptive secondary recomputes T1-T3 "
            "excluding events involving an UNK value, is reported wherever the primary is, and "
            "never carries the headline; if the sign locus fires with UNK among the top-10 "
            "values, the headline paragraph carries the mandatory spec section 5.2 sentence "
            "stating the localisation is in part a localisation to illegibility"
        ),
        "locus_rules": {
            "signs": (
                "the top-10 values by involvement account for at least 50% of summed "
                "involvement (the design's CONCENTRATED criterion, verbatim); companion states "
                "computed and reported: UNIFORM if the top-10 share is within 10 points of "
                "those values' frequency share, BETWEEN otherwise when the 50% line is not met"
            ),
            "object_types": (
                "DD-058-8, confirmed by DD-058-19: one recorded object type (Seals or Tablets; "
                "the Unrecorded category cannot fire) accounts for at least 50% of E and its "
                "event share exceeds its share of the 50 frame objects by at least 10 points"
            ),
            "segmentation": (
                "DD-058-3, confirmed by DD-058-19: INDEL events account for at least 50% of E"
            ),
        },
        "outcomes": [
            "LOCALISED TO SIGNS",
            "LOCALISED TO OBJECT TYPES",
            "LOCALISED TO SEGMENTATION",
            "LOCALISED TO MULTIPLE LOCI",
            "NOT LOCALISED",
            "PILOT-PASS RECORDS NOT PRODUCIBLE",
            "INVALID",
        ],
        "headline_mapping": (
            "DD-058-9, confirmed by DD-058-19: the headline is a mechanical function of the set "
            "of loci that fire - one firing locus gives its single-locus wording, two or more "
            "give LOCALISED TO MULTIPLE LOCI with every firing locus and share named, none "
            "gives NOT LOCALISED; PILOT-PASS RECORDS NOT PRODUCIBLE (gate 0.2) and INVALID "
            "(gates 0.1/0.3/0.4/0.5) are step-0/stop classes, not headlines; every headline is "
            "reported in its pre-written spec section 5.2 wording"
        ),
        "arm_b": (
            "blocked and out of scope (F058-C06): the human-coder calibration arm stands under "
            "the owner's expert-engagement hold of 2026-10-12, carried unchanged by the "
            "campaign plan (Part 6 item 4); this spec designs no part of it and no AI "
            "substitution for its human coders; the unblocking act is the owner lifting that "
            "hold and an engagement being made under its own planning gate"
        ),
        "freeze_does_not": (
            "this freeze does not itself localise anything: no alignment has been run under "
            "this spec, no event tabulated, the event total E is unstated, and no store bytes "
            "are produced or pinned; the freeze's store reproduction check is adjudication "
            "evidence for DD-058-15 only and computed no section 4 quantity; localisation, "
            "closures, and invalid stops are execution outcomes under Phase-420, not freeze "
            "acts; the freeze changes no verdict and establishes nothing about human coders, "
            "the 0.80 floor, or any codebook revision"
        ),
        "execution_gate": (
            "Not satisfied at the freeze of 2026-10-21: execution runs as Phase-420 only after "
            "this freeze has merged, the OSF contract registration's approval act has completed "
            "(the parent's approval click on OSF's admin notification), and a separate execution "
            "order is given, in campaign Wave 3 group 2"
        ),
    },
    "inputs": {
        "spec023": {
            "file": "specs/023-keyed-transcription-layer/spec.md",
            "sha256": "c2e5d1668b270266d5a20e30b1ec87cd4c1d5d2ffe786a45331a9a5ade1275d2",
            "bytes": 44521,
        },
        "pilot_metrics": {
            "file": "reports/phase132_pilot_metrics.json",
            "sha256": "e864fca57ecd1dc403c8e52ab9df6414372478d5781457f0aaca5e9084914554",
            "bytes": 21070,
            "facts": "exact-sequence 0.20 (10/50, P and M); per-token 0.4798 (95/198) all-50, 0.4286 (18/42) gold; gold estimator 0.05 (2/40); pass token totals 191/190/40/189",
        },
        "pilot_report": {
            "file": "reports/phase132_pilot_report.md",
            "sha256": "e1df32da86f7d3fd276d0ad546b3c351b58fd88b73f4468461f61075f6460e00",
            "bytes": 12880,
        },
        "pilot_frame": {
            "file": "data/keyed_transcription/phase132_pilot_frame.json",
            "sha256": "a967144be0531c9d8396615d1ca07161dca0bc7347ca8c2c0d6a3c21a037a2ea",
            "bytes": 48339,
            "facts": "50 objects: Mohenjo-Daro 25, Harappa 15, Lothal 6, Kalibangan 4; recorded types Seals 34, Tablets 11, unrecorded 5; gold sample 10 (seed 20261009)",
        },
        "pilot_dataset": {
            "file": "data/keyed_transcription/phase132_pilot_dataset_v1.json",
            "sha256": "adb596a1745470835e46c5148c1848d8408c45a030687d96427f00dbb6f74400",
            "bytes": 143834,
        },
        "pilot_dataset_meta": {
            "file": "data/keyed_transcription/phase132_pilot_dataset_v1_meta.json",
            "sha256": "b2c607fae5f2602bb7b9634ff103f01df1de3885a1f1bbeeb6da3fc489cdefd4",
            "bytes": 5815,
            "content_hash_of_record": "7bdc73f5e0f6a959f8d94a4317c642ebe36638e841f7bb80bae97c75477f224a",
        },
        "phase383_results": {
            "file": "reports/phase383_results.json",
            "sha256": "4e52942dc6be25fed4ab2004823a1d9353c9abfe6f5428e1050ee8d0d9a98334",
            "bytes": 2870,
            "facts": "bootstrap interval for exact-sequence agreement [0.10, 0.32] (B = 9,999, seed 20261011); verdict CONTRADICTED; origin groups = 1",
        },
        "phase383_report": {
            "file": "reports/phase383_report.md",
            "sha256": "9f35f722611f6acd57e1ee05c9de0c8e95267ccf7f93b27eacb31bdff9cd08ca",
            "bytes": 3400,
        },
        "metrics_module": {
            "file": "backend/scripts/phase132_metrics.py",
            "sha256": "238dfafa3bac17dc0ad610ff4b7e6cf4fa577462d04cd31a3c612537cbe21984",
            "bytes": 24363,
            "posture": "imported unchanged at execution for the store loader, the P-space derivation, the alignment, and the gate 0.4 reproduction; never reimplemented",
        },
        "rescoring_module": {
            "file": "backend/scripts/phase383_pilot_rescoring.py",
            "sha256": "b64b60de35d59bd99177e8ac3f68a80ffd2b0d31f8c75ea87312f69f927729ec",
            "bytes": 9384,
        },
        "crosswalk": {
            "file": "data/crosswalks/parpola_mahadevan_crosswalk_v1.json",
            "sha256": "4e7559dfc2ced83c79440029a1b2749fe9d21eca7f6db3bf3b66f0cfa647dcbb",
            "bytes": 257779,
        },
        "lane2_drafts": {
            "file": "specs/029-tao-claim-lifecycle/lane2-drafts/drafts.json",
            "sha256": "3f645c9a4132ba5a0bc5fca4ca22810b8b6169a2f1f9f85f35990c7b72df33fb",
            "claim_id": "STUDY-SPEC-023/PHASE-132+383",
        },
        "anchors": {
            "file": "backend/reports/INDUS_FINAL_ANCHORS.json",
            "sha256": "df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569",
            "bytes": 570344,
            "posture": "this spec moves no anchor; the file is asserted byte-identical before and after any execution",
        },
        "pin_verification": (
            "at the freeze of 2026-10-21 every section 2.1 pin above was re-derived by two "
            "independent routes (contents-API and git-blob) at main "
            "770155dea66c5d5dde194728560aacf83c7514d0; the two routes agree byte-for-byte on "
            "every file and every hash equals its pin (freeze.md section 2)"
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
    "backend/tests/test_spec058_freeze.py",
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
