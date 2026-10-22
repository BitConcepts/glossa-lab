#!/usr/bin/env python3
"""Build the Spec 059 freeze record (freeze.json).

This builder was written at the freeze act of
2026-10-21 (the draft carried no builder and no
draft digest: the campaign's drafting wave opens
claims-first drafts only, and the digest is
computed over the recovered register exactly
once, at the freeze - the Spec 035 ordering).
Run with the Glossa backend venv python from the
repository root:

    python specs/059-f1-object-join/build_freeze.py

Writes specs/059-f1-object-join/freeze.json
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

SPEC_DIR = "specs/059-f1-object-join"

DEFINITION = {
    "spec": "specs/059-f1-object-join/spec.md",
    "freeze_doc": "specs/059-f1-object-join/freeze.md",
    "experiment_id": "spec059-f1-object-join",
    "register": {
        "path": "specs/059-f1-object-join/claims.json",
        "register_version": "0.8-draft",
        "claims": 15,
        "aee_hook_pass": (
            "PASSED at the freeze act of 2026-10-21 under aee 1.5.3: after_specify cleared in "
            "adjudicated rounds over the recovered register (a loadability recovery from 0.5-draft to "
            "0.6-draft - the draft's free-form evidence kind and source_quality labels are not engine "
            "values and the loader refuses them; 48 failure modes over 0.6-draft: 14 irreducibility, 19 "
            "independence-unmodelled, 15 FR-2.3 draft-cap records; heads restated and independence "
            "declared at 0.7-draft; final restatements at 0.8-draft cleared the remaining irreducibility "
            "challenges, an absolute-language challenge on F059-C06, and a negation-conflict challenge "
            "on the F059-C06/F059-C15 pair, whose boundary-confirmation records stand in both claims' "
            "metadata; 15 draft-cap records only over the final register), after_plan and after_tasks "
            "clean at first pass on the final register; at every hook zero correctness failure modes "
            "and no claim below the 0.70 threshold (minimum propagated 0.72); the engine outcome word "
            "reads iterate solely from the draft-cap records (gate reading DD-059-14; record in "
            "specs/059-f1-object-join/aee/freeze-aee-note.md)"
        ),
    },
    "basis": {
        "adjudication": "specs/059-f1-object-join/adjudication.md",
        "decisions": (
            "DECIDED by the owner on 2026-10-21 (not proposals): the runnable-experiments campaign "
            "plan approved AS WRITTEN (decision E-1; member 16) commissions the campaign of which "
            "design D-22 is a member; Spec 059 is D-22's specification. Draft decisions DD-059-1 to "
            "DD-059-6 are recorded in adjudication.md sections 4-5 and are confirmed or completed at "
            "the freeze. Freeze decisions DD-059-7 to DD-059-14 are recorded in adjudication.md "
            "section 8: the gate bar's reading adopted - the design's stated 61.0 percent, at least "
            "3,465 of 5,679 joined rows, the exact-points and relative readings refused on the record "
            "(DD-059-7); the single-test correction family confirmed, DD-059-4 standing (DD-059-8); "
            "the object-identifier sources named and pinned - the lineage layer's cisi field carried "
            "as provenance.object_id under the pinned Phase-130 schema per the pinned Spec 034 "
            "route-(b) construction, resolving against the pinned catalogue layer's distinct objects "
            "(DD-059-9); the spec's own OSF contract registration filed at the freeze under E-1 "
            "(DD-059-10); the gate census confirmed sufficient as the join's audit (DD-059-11); "
            "DD-059-3's verdict precedence confirmed (DD-059-12); Phase-421 allocated (DD-059-13); "
            "and the DD-038-10 AEE gate reading adopted as DD-059-14."
        ),
    },
    "design": {
        "phase": "Phase-421",
        "act": (
            "run the step-0 gates of spec section 3 in order - input integrity, original-join "
            "reproduction, the object-identifier join census, and the gate comparison against the "
            "adopted bar - and, only if the gate passes, apply the frozen Phase-136 flow unchanged "
            "to the enlarged joined set, reaching exactly one of the pre-registered outcomes of "
            "spec sections 5 and 9"
        ),
        "claim_under_test": {
            "id": "STUDY-SPEC-024/F1",
            "record": (
                "SETTLED - SUPPORTED on its joined subset: Mantel-Haenszel common odds ratio 2.384, "
                "95% CI [1.847, 3.077], permutation raw p 0.0001 (B = 9,999, seed 20261009), family "
                "Benjamini-Hochberg q = 0.00015 in the combined Stage 2 report; Phase-141 "
                "leave-one-site-out STABLE, every dropped-site interval excluding 1"
            ),
        },
        "falsifier": (
            "on the enlarged set, the within-site test's interval for the odds ratio includes 1.0, "
            "or the point estimate falls below 1.5 - meaning the original result was partly an "
            "artefact of which rows could be joined; mapped onto the verdict words by F059-C11 with "
            "the precedence of DD-059-3, confirmed at DD-059-12"
        ),
        "gate": {
            "ruling": (
                "DD-059-7 (OF-059-1 resolved): the operative bar is the design's own parenthetical "
                "reading - joined share at least 61.0 percent, i.e. at least 3,465 joined rows of "
                "5,679 (0.61 x 5,679 = 3,464.19; 3,464 rows = 60.997 percent and fails)"
            ),
            "baseline": "2,895 / 5,679 = 50.977 percent (the design's rounded 51.0 percent)",
            "refused_readings": (
                "exact-points: 50.977 percent + 10 points = 60.977 percent, threshold 3,462.9 rows, "
                "i.e. at least 3,463 rows; relative: a 10 percent relative rise - 56.1 percent on "
                "the rounded base (threshold 3,185.92 rows, at least 3,186) or 56.075 percent on the "
                "unrounded base (threshold 3,184.5 rows, at least 3,185); both refused on the record "
                "in adjudication.md section 8; the adopted bar is the strictest of the three"
            ),
            "closure": (
                "below the bar the execution closes at step 0, unscored, as CLOSED AT STEP 0 - JOIN "
                "GATE NOT MET, in the pre-written wording of spec section 3.5, with the gate census "
                "published as the finding"
            ),
        },
        "join": {
            "ruling": (
                "DD-059-9 (OF-059-3 resolved): the object-identifier sources are named and pinned "
                "on the record of record; no source is invented and no substitute source is admitted"
            ),
            "construction": (
                "each lineage row's object identifier is carried as cited provenance data - "
                "provenance.object_id - under the Phase-130 intake schema, following Spec 034's "
                "route-(b) construction "
                "(build_intake_dataset in the pinned Phase-398 builder); a row is joined if and only "
                "if its identifier resolves to exactly one distinct object in the CISI catalogue "
                "layer; rows resolving to zero or to more than one are counted as unjoined or "
                "ambiguous and enter nothing; the census unit is the layer row (DD-059-2), with the "
                "distinct-object count reported descriptively"
            ),
            "lineage_source": {
                "file": "research_notes/indus-data-deep-sweep-20261008/downloads/horus84-computational-linguistics/data/inscriptions.csv (local store)",
                "sha256": "c368f290d8d784093d804243100de27ae6ad09df3ae37cab7432a0205d4ec9ef",
                "bytes": 1190884,
                "identifier": "each row's published CISI object reference is its cisi field, carried as provenance.object_id",
            },
            "converted_form": {
                "file": "corpora/downloads/icit_fieldcady/icit_converted_v2_keyed.json (local store)",
                "sha256": "bbfdbcd5d5e3e3121251de91462af51dc702a4114a4d10ffd7061e1f5593a5c8",
                "bytes": 1586137,
                "posture": (
                    "the programme-built converted form of the same lineage layer (build record in "
                    "reports/phase398_results.json: 5,679 source inscriptions, 5,018 carrying a CISI "
                    "reference) - the same rows and the same cisi values, not a second source"
                ),
            },
            "catalogue_source": {
                "files": "corpora/downloads/cisi_image_layer/catalogue/cisi_vol1_catalogue.csv + cisi_vol2_catalogue.csv (local store)",
                "object_key": "cisi_id",
                "rows": 7705,
                "distinct_objects": 3493,
            },
            "schema": {
                "file": "data/intake/intake_dataset_schema_v1.json",
                "sha256": "b94d03add0318044b559b7b2976bbd2722abc19adcf67a0ea0cf093f8d7de49b",
                "validator": "backend/glossa_lab/intake.py",
                "validator_sha256": "02b24e3312a9a4ac4f7e3b14aeaee2cda0268f41cb5bd573494340c2e7d2df03",
            },
            "construction_precedent": {
                "file": "backend/glossa_lab/phase398_matched_object.py",
                "sha256": "278f16b0ae8b02b77412cc925ac9e767110f5d5461729b73e8c122a9ff7673f0",
            },
            "audit": (
                "DD-059-11 (OF-059-5 resolved): the gate census of spec section 3.3, published "
                "either way with per-row identifier provenance, suffices as the join's audit; no "
                "separate join audit is required before execution"
            ),
        },
        "string_boundary": (
            "binding (F059-C06; spec section 7.1): no step of the join, census, or test treats "
            "equality of any string - a catalogue number string, a name, the layer's cisi field as "
            "a string, or a cisi_number - as evidence that two records concern the same physical "
            "object; the ground is Spec 037's census (693 exact-string candidates: 269 VERIFIED, "
            "341 CONFLICT (49.21 percent), 83 UNRESOLVED); the cisi value enters only as cited "
            "provenance data in the schema's declared provenance.object_id field and resolves "
            "against catalogue object IDs; the original concordance join is re-run at gate 0.2 "
            "only to reproduce the recorded baseline and contributes no row to the enlarged set"
        ),
        "machinery": (
            "identical to Phase-136, unchanged in every particular (F059-C10): catalogue "
            "object_type; restriction to {Seals, Tablets}; sequence parse re.findall(r'\\d{3}', "
            "text), terminal = last parsed code; frozen Spec 018 section 3 canonical W-to-P "
            "mapping over the pinned registry, UNK excluded and counted; TERMINAL14 = {P020, P076, "
            "P095, P099, P108, P125, P210, P226, P256, P346, P359, P378, P384, P385}; stratum "
            "eligibility N >= 20 and >= 5 Seals and >= 5 Tablets; estimability >= 2 eligible "
            "strata and pooled expected counts >= 5 in at least 80 percent of the 4 cells; "
            "Cochran-Mantel-Haenszel chi-square, no continuity correction; permutation null within "
            "strata, B = 9,999, seed 20261009, p = (1 + #{perm >= obs}) / (1 + B); Mantel-Haenszel "
            "common odds ratio with Robins-Breslow-Greenland 95 percent CI"
        ),
        "correction": (
            "DD-059-8 (OF-059-2 resolved), confirming DD-059-4: the confirmatory family under this "
            "spec is its single primary test; the Benjamini-Hochberg adjustment at q = 0.05 is over "
            "one p-value and the adjusted q equals the raw permutation p; the design's same-family "
            "instruction is not executed - the Spec 024 family (F1/F2/F3) was corrected once in its "
            "combined report and is closed, and re-running it would re-adjudicate F2's and F3's "
            "closed q-values; no wider family is declared"
        ),
        "verdicts": {
            "mapping": (
                "REPLICATED: adjusted q below 0.05 and the odds-ratio interval entirely above 1.5; "
                "WEAKENED: adjusted q below 0.05, the interval not including 1.0, but reaching "
                "below 1.5; NOT REPLICATED: adjusted q at or above 0.05, or the interval including "
                "1.0"
            ),
            "precedence": (
                "DD-059-12, confirming DD-059-3: an interval including 1.0 is NOT REPLICATED even "
                "when q is below 0.05; WEAKENED is reserved for intervals excluding 1.0 but reaching "
                "below 1.5"
            ),
        },
        "reporting": (
            "every gate-passed outcome reports the Phase-141 leave-one-site-out rerun "
            "descriptively (it mints no verdict and changes no verdict word) and both covariate "
            "comparisons - joined versus unjoined rows, and the original joined set versus the "
            "rows the object-ID join adds - on every covariate the data carries (site, object "
            "type, text length, preservation as recorded); a covariate the data does not carry is "
            "named as not carried, never reconstructed"
        ),
        "outcomes": [
            "INVALID",
            "CLOSED AT STEP 0 - JOIN GATE NOT MET",
            "NOT ESTIMABLE",
            "REPLICATED",
            "WEAKENED",
            "NOT REPLICATED",
        ],
        "step0_gates": (
            "fail-closed, in order, before any enlarged-set quantity (spec section 3): gate 0.1 "
            "input integrity - every spec section 2 pin and every DD-059-9 pin hashes to its "
            "freeze-record value and the Phase-130 validation of the join dataset returns pass, or "
            "the run stops as INVALID; gate 0.2 original-join reproduction - the frozen "
            "concordance rule reproduces the recorded census exactly (5,679 layer rows; 2,895 "
            "matched; 2 ambiguous; 2,782 unmatched), or INVALID; gate 0.3 the object-identifier "
            "join census by resolution class; gate 0.4 the gate comparison against the adopted "
            "bar (DD-059-7) - below it, CLOSED AT STEP 0 - JOIN GATE NOT MET; nothing is repaired "
            "at run time"
        ),
        "freeze_does_not": (
            "this freeze does not itself join anything: no object-ID join has been built, no census "
            "computed, no joined share exists, and the gate is not decided in either direction; it "
            "asserts nothing about the named sources' coverage of this layer beyond what the cited "
            "records state; it edits no Spec 024 record and moves no anchor"
        ),
        "execution_gate": (
            "Not satisfied at the freeze of 2026-10-21: execution runs as Phase-421 only after "
            "this freeze has merged, the OSF contract registration's approval act has completed "
            "(the parent's approval click on OSF's admin notification), and a separate execution "
            "order is given, in campaign Wave 3 group 2"
        ),
    },
    "inputs": {
        "phase136_results": {
            "file": "reports/phase136_results.json",
            "sha256": "11a0741317f50d9b8c2791fbfdd42ebec0f2a250d6f76809a2dec29fef857022",
        },
        "stage2a_freeze": {
            "file": "specs/024-evidence-integration/stage2a-freeze.md",
            "sha256": "c65a4b9ba7820f8dcf65fccfe64b8c271e488b036a754c76c45cd19f7cb4b94c",
        },
        "phase136_builder": {
            "file": "backend/scripts/phase136_terminal_type.py",
            "sha256": "d5ceec463bd271cd900fd2e5dbe2efb5b9e5f2b36444942b1d6cab12a6ee8871",
        },
        "phase141_report": {
            "file": "reports/phase141_report.md",
            "sha256": "d442f8d2bcd1e7500c6df169f1dda0d8f48117c349e1710b34ff83011c7e4347",
        },
        "stage2_report": {
            "file": "reports/phase136_137_138_stage2_report.md",
            "sha256": "6a4f5d2651ddc8316cf69d65ff6f4d29a7138ddc528c68310e6f07047eaed062",
        },
        "registry": {
            "file": "data/crosswalks/canonical_sign_registry.csv",
            "sha256": "8a0b2a82ac8d226d574ce01f5550c581efd91a97cab86201a62f7a7e435bd420",
            "rows": 803,
        },
        "spec034_outcome": {
            "file": "specs/034-matched-object-attribution/outcome.md",
            "sha256": "c0cc615ddb062306aa43cc8441fe5c6c322b563badd351ebce54fed1d7b43175",
        },
        "spec037_outcome": {
            "file": "specs/037-cisi31-concordance-spine/outcome.md",
            "sha256": "28e444f20e698b3533559aac3a4bc3efcbc50440e79427ae58f656642886a02a",
        },
        "anchors": {
            "file": "backend/reports/INDUS_FINAL_ANCHORS.json",
            "sha256": "df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569",
            "posture": "this spec moves no anchor; the file is asserted byte-identical before and after any execution",
        },
        "local_store": {
            "posture": (
                "the lineage layer, the catalogue volumes, and the converted keyed layer are held "
                "in the local store and are not committed; their freeze pins are carried as the "
                "definition constants in design.join (lineage_source, converted_form, "
                "catalogue_source via the Phase-136 results record) in the Spec 038 form, and the "
                "committed Phase-136 results file records the same hashes for the layer and the "
                "catalogue volumes, which the freeze tests assert in-repo; gate 0.1 recomputes "
                "every local-store pin at execution"
            ),
            "catalogue_vol1_sha256": "e0d698f991fbd7cf26c491a2b25906b422903a0e2a26ea7b8c690420ca51dc1e",
            "catalogue_vol2_sha256": "e751244e2d51bda3181d98e56af691c0d24099d76d035b54f0888504204bc7d9",
        },
        "pin_verification": (
            "at the freeze of 2026-10-21 every committed pin above was re-derived by two "
            "independent routes (contents-API raw and git-blob) at main "
            "a3509525fab64e22a4c053d7bbed14c7083a14d3, and every local-store pin by two further "
            "routes (Python hashlib and sha256sum); all routes agree byte-for-byte and every hash "
            "equals its pin (freeze.md section 2)"
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
    "backend/tests/test_spec059_freeze.py",
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
