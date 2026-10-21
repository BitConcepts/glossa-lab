#!/usr/bin/env python3
"""Build the Spec 039 freeze record (freeze.json).

This builder computed the DRAFT digest over the
draft contract under the owner's decisions of
2026-10-20 (adjudication.md: the act authorised,
bundled with D-25, evidence standard Option 1).
At the freeze act - in the bundle sequence of
plan.md, after the AEE lifecycle hooks passed over
the recovered register - it was re-run to compute
the final digest over the frozen contract exactly
once, and its DEFINITION text was finalised in the
same act (the Spec 035 pattern). Run with the
Glossa backend venv python from the repository
root:

    python specs/039-gazetteer-period-assignment/build_freeze.py

Writes specs/039-gazetteer-period-assignment/freeze.json
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

SPEC_DIR = "specs/039-gazetteer-period-assignment"

DEFINITION = {
    "spec": "specs/039-gazetteer-period-assignment/spec.md",
    "freeze_doc": "specs/039-gazetteer-period-assignment/freeze.md",
    "experiment_id": "spec039-gazetteer-period-assignment",
    "register": {
        "path": "specs/039-gazetteer-period-assignment/claims.json",
        "register_version": "0.7-draft",
        "claims": 15,
        "aee_hook_pass": (
            "PASSED at the freeze act of 2026-10-20 "
            "under aee 1.5.0: after_specify cleared "
            "in three adjudicated rounds (20 failure "
            "modes over 0.5-draft; 17 over the 0.6 "
            "recovery text; 15 FR-2.3 draft-cap "
            "records only over 0.7-draft), after_plan "
            "and after_tasks clean at first pass; at "
            "every hook zero correctness failure "
            "modes and no claim below the 0.70 "
            "threshold (minimum propagated 0.72); "
            "the engine outcome word reads iterate "
            "solely from the draft-cap records (gate "
            "reading DD-039-8; record in "
            "specs/039-gazetteer-period-assignment/aee/"
            "freeze-aee-note.md)"
        ),
    },
    "basis": {
        "adjudication": (
            "specs/039-gazetteer-period-assignment/adjudication.md"
        ),
        "decisions": (
            "DECIDED by the owner on 2026-10-20 (not "
            "proposals): (D1) the gazetteer "
            "period-assignment act (Spec 027 section "
            "6.2) is authorised, bundled with the D-25 "
            "chronology test - one adjudication cycle, "
            "this act executes first, D-25's own spec "
            "consumes the assigned gazetteer as a "
            "hash-pinned input; (D2) the evidence "
            "standard is Option 1 - published period "
            "determinations only, no program-derived "
            "assignments (Option 2 not adopted). "
            "Freeze decisions DD-039-1 to DD-039-8 "
            "are recorded in adjudication.md section "
            "4: the label set and source hierarchy "
            "adopted; the TwoRains published-venue "
            "rule adopted; Masudpur not established; "
            "the margins re-run adopted as this "
            "act's verification step; the spec's own "
            "OSF contract registration filed at the "
            "freeze; Phase-403 allocated; and the "
            "DD-038-10 / DD-037-9 AEE gate reading "
            "adopted as DD-039-8."
        ),
    },
    "design": {
        "phase": "Phase-403",
        "act": (
            "assign program period labels to the Stage 0 "
            "gazetteer sites (36 rows, 30 program sites) "
            "in the section 6.2 program_period_assignment "
            "field, from published determinations only, "
            "under rules frozen before any assignment is "
            "made"
        ),
        "evidence_standard": {
            "option": "Option 1 - published period determinations only",
            "admissible": (
                "a publication's own period statement "
                "about the named site, cited with its "
                "locator (page, table, or record)"
            ),
            "inadmissible": (
                "chronology-spine dates and any inference "
                "from them; neighbouring-site analogy; "
                "site-size or survey reasoning; "
                "unpublished data; the program's own "
                "prior prose; any determination that "
                "cannot be cited to a publication and a "
                "locator"
            ),
            "restricted_sources": (
                "Possehl's lists and Law (2011) stand "
                "catalogue_only and the CISI catalogue "
                "layers open_access_read_only in the "
                "Stage 0 record; assignments resting on "
                "them record citation, locator, and the "
                "determination as published - no bulk "
                "copying or redistribution (Spec 027 "
                "section 5.1 posture)"
            ),
            "no_program_derived": (
                "Option 2 (published plus program-derived "
                "assignments under frozen rules, e.g. "
                "spine dates to period) was not adopted; "
                "no label is an inference"
            ),
        },
        "label_set": {
            "dd": "DD-039-1 (decided at freeze)",
            "labels": [
                "Early Harappan",
                "Mature Harappan",
                "Late Harappan",
            ],
            "alignment": (
                "the vocabulary of Spec 031's frozen "
                "period rule (adopted 4A; F031-C10), which "
                "turns on Mature Harappan occupation and "
                "attempts no finer temporal slicing"
            ),
            "outside_the_sequence": (
                "a published determination outside the "
                "Harappan sequence (e.g. the gazetteer's "
                "own PN / Neo. values) grounds no "
                "assignment under this set"
            ),
            "multi_period": (
                "a multi-period occupation statement "
                "grounds a multi-label record stated as "
                "such, never silently collapsed"
            ),
        },
        "mapping_rule": {
            "form": (
                "a scheme-aware table, written into the "
                "freeze record before any assignment is "
                "made; the row's period_scheme governs "
                "which mapping applies"
            ),
            "entries": {
                "MAP-EXPLICIT-EARLY": (
                    "explicit three-period scheme value "
                    "Early Harappan (or EH where the "
                    "publication itself expands it) -> "
                    "Early Harappan"
                ),
                "MAP-EXPLICIT-MATURE": (
                    "explicit three-period scheme value "
                    "Mature Harappan (or MH where the "
                    "publication itself expands it) -> "
                    "Mature Harappan"
                ),
                "MAP-EXPLICIT-LATE": (
                    "explicit three-period scheme value "
                    "Late Harappan (or LH where the "
                    "publication itself expands it) -> "
                    "Late Harappan"
                ),
                "MAP-EXPLICIT-MULTI": (
                    "explicit three-period scheme value "
                    "naming two or three labels -> each "
                    "named label, as a multi-label record"
                ),
                "MAP-RANGE-EARLY-MATURE": (
                    "Early-Mature Harappan range -> "
                    "Early Harappan and Mature Harappan"
                ),
                "MAP-RANGE-MATURE-LATE": (
                    "Mature-Late Harappan range -> "
                    "Mature Harappan and Late Harappan"
                ),
                "MAP-RANGE-EARLY-LATE": (
                    "Early-Late Harappan range -> Early "
                    "Harappan, Mature Harappan, and Late "
                    "Harappan"
                ),
                "MAP-HARP-RAVI": (
                    "HARP/Harappa scheme Ravi Phase (or "
                    "Period 1 equated with it in the "
                    "same publication) -> Early Harappan"
                ),
                "MAP-HARP-KOTDIJI": (
                    "HARP/Harappa scheme Kot Diji Phase "
                    "(or Period 2 equated with it in "
                    "the same publication) -> Early "
                    "Harappan"
                ),
                "MAP-HARP-HARAPPAN": (
                    "HARP/Harappa scheme Harappa Phase "
                    "(or Period 3 equated with it in "
                    "the same publication) -> Mature "
                    "Harappan"
                ),
                "MAP-HARP-CEMETERY-H": (
                    "HARP/Harappa scheme Cemetery H "
                    "Phase (or Period 5 equated with "
                    "it in the same publication) -> "
                    "Late Harappan"
                ),
                "MAP-JHUKAR": (
                    "published scheme value Jhukar Phase "
                    "-> Late Harappan"
                ),
                "MAP-CEMETERY-H": (
                    "published scheme value Cemetery H "
                    "Phase outside the HARP scheme -> "
                    "Late Harappan"
                ),
            },
            "reviewer": (
                "Muse Spark via Muse "
                "(AI agent)"
            ),
            "unmapped_values": (
                "a value with no table entry maps to "
                "nothing: the site stays unassigned on "
                "that evidence, reason code "
                "UNMAPPED_SCHEME_VALUE; no mapping is "
                "improvised at assignment time"
            ),
            "recorded_per_assignment": (
                "the mapping entry applied, the reviewer "
                "of record, and every determination "
                "relied on (source, citation, locator, "
                "published value, scheme)"
            ),
        },
        "disagreement": {
            "posture": (
                "Spec 027 sections 6.3 and 6.5: contested "
                "assignments are flagged, every "
                "conflicting determination stays on the "
                "record verbatim, no majority vote "
                "silently resolves a conflict, and "
                "downstream consumers report both ways "
                "(contested counted / contested excluded)"
            ),
            "hierarchy_limit": (
                "the DD-039-2 source hierarchy orders "
                "citation and presentation only; it never "
                "suppresses a determination and never "
                "resolves a contest"
            ),
            "ask2_reserved": (
                "Spec 030 Ask 2 (CONTESTED sensitivity "
                "bindingness for a future Q6 freeze) is "
                "expressly NOT DECIDED and stays "
                "RESERVED; this act does not decide it, "
                "does not depend on it, and does not "
                "prejudge it - different fields in "
                "different records"
            ),
        },
        "assignment_record": {
            "unit": (
                "per program_site_id (30 sites), carried "
                "identically onto every gazetteer row "
                "for that site"
            ),
            "shape": (
                "label or label set; mapping_rule; "
                "reviewer; evidence list (source, "
                "citation, locator, published value, "
                "scheme); contested flag with the "
                "conflicting determinations where set"
            ),
            "blank_reason_codes": [
                "NO_PUBLISHED_DETERMINATION",
                "UNMAPPED_SCHEME_VALUE",
                "OUTSIDE_LABEL_SET",
            ],
        },
        "outputs": {
            "assigned_gazetteer": (
                "data/movement/gazetteer_rows_assigned.jsonl - "
                "all 36 rows, byte-identical to the "
                "pre-act file outside "
                "program_period_assignment; the pre-act "
                "file is not modified and its SHA-256 is "
                "pinned in the outcome record"
            ),
            "assignment_report": (
                "reports/phase403_results.json and "
                "reports/phase403_gazetteer_assignment_report.md "
                "per-site "
                "table with evidence, contested list, "
                "blank list with reason codes, the "
                "section 6.3 completeness report by source"
            ),
            "dataset_new_version": (
                "a NEW VERSION of Zenodo record 23300361 "
                "carrying the assigned gazetteer for the "
                "releasable rows under v1's licence "
                "posture; the existing deposit is never "
                "edited"
            ),
        },
        "margins_verification": {
            "dd": "DD-039-5 (decided at freeze)",
            "scope": (
                "recompute only the period-eligibility "
                "gate of the Phase-395 margins step, "
                "under Spec 031's frozen rule (F031-C10), "
                "over the assigned gazetteer; eligible "
                "sites reported both ways over contested "
                "assignments"
            ),
            "then_stated": (
                "the margins step's remaining frozen "
                "floors and the standing record against "
                "them: in-universe link mass 2 "
                "link-eligible sites and 1 linked pair "
                "against floors of 8 eligible sites and "
                "10 linked pairs - on the standing "
                "record the step closes at the link-mass "
                "floor, recorded as a verification "
                "result, not as a Q7 verdict"
            ),
            "never_reopened": (
                "no response is computed; no Spec 031 "
                "machinery beyond the margins first gate "
                "runs; Spec 031's closures (bead/craft "
                "NOT-YET-TESTABLE, ceramic NOT "
                "ESTIMABLE) are not amended, superseded, "
                "or restated"
            ),
        },
        "bundle": {
            "partner": (
                "D-25, the chronology-controlled re-test "
                "of Spec 025 G1 (SUPPORTED under control; "
                "chronology not controlled - the rider), "
                "design in the PR #195 portfolio"
            ),
            "sequencing": (
                "one adjudication cycle covers both "
                "acts; this act executes first; D-25's "
                "spec is a separate document consuming "
                "the assigned gazetteer as a hash-pinned "
                "input; this spec does not design, "
                "freeze, or prejudge D-25's test"
            ),
        },
        "masudpur": {
            "dd": "DD-039-4 (decided at freeze)",
            "state": (
                "28 TwoRains determinations (Masudpur "
                "VII, Masudpur I) extracted in full in "
                "the Phase-394 record and NOT ADMITTED: "
                "the sites are not gazetteer-established "
                "and no publication reached states their "
                "coordinates; Phase-394 rule 7 admits "
                "coordinate-less rows only for "
                "gazetteer-established sites"
            ),
            "default": (
                "this act establishes no new sites and "
                "admits no Masudpur determination; the "
                "act is confined to the existing 30 "
                "sites, and the establishment route "
                "stays recorded for a future act"
            ),
            "tworains_venue_rule": (
                "DD-039-3: a TwoRains determination "
                "counts as published only in a "
                "peer-reviewed journal article, its "
                "published supplementary material, or a "
                "published report series, with a locator; "
                "theses, project datasets, and data "
                "deposits do not count; doubtful venues "
                "default to not counting"
            ),
        },
        "fences": (
            "assignments are published-record "
            "statements, not dating evidence; the act "
            "changes no study verdict by itself; link "
            "mass (2 sites / 1 pair) is unaffected and "
            "is stated wherever the act's effect is "
            "described; a blank is an honest outcome, "
            "recorded with its reason code"
        ),
        "execution_gate": (
            "Satisfied at the freeze of 2026-10-20: "
            "the owner's standing pipeline "
            "authorisation ordered this contract "
            "frozen and executed; execution runs as "
            "Phase-403 under the frozen contract, "
            "and no period assignment was made at "
            "the freeze itself"
        ),
    },
    "inputs": {
        "gazetteer": {
            "file": "data/movement/gazetteer_rows.jsonl",
            "sha256": (
                "5ac76a3031121a61fa39f87b1d2760855374d171ddd036988fee2820dca9b8b6"
            ),
            "rows": 36,
            "program_sites": 30,
            "row_sources": {
                "XRONOS": 21,
                "CISI Vol. 1 catalogue (Phase-124 layer)": 11,
                "CISI Vol. 2 catalogue (Phase-124 layer)": 4,
            },
            "licence_states": {
                "verified_open": 21,
                "open_access_read_only": 15,
            },
            "period_label_as_published": {
                "null_rows": 33,
                "non_null": {
                    '["PN", "Neo.?"]': 2,
                    '["PN", "Neo."]': 1,
                },
            },
            "program_period_assignment_null_rows": 36,
        },
        "stage0_deposit": {
            "record": 23300361,
            "doi": "10.5281/zenodo.23300361",
            "title": (
                "Glossa Lab Spec 027 Stage 0 - Indus "
                "Settlement Gazetteer and Chronology "
                "Spine (Phase-391)"
            ),
            "gazetteer_csv_rows": 21,
            "note": (
                "the deposited CSV is the verified_open "
                "subset of the gazetteer; the deposit is "
                "superseded only by a new version"
            ),
        },
        "phase395_margins": {
            "results": "reports/phase395_results.json",
            "population_record_sha256": (
                "a0c98d56780051b46795621b644457e7674f7266321073e65a67ef51f83b54b8"
            ),
            "eligible_sites_at_margins": 0,
            "floors": {
                "eligible_sites_min": 8,
                "linked_pairs_min": 10,
            },
            "link_eligible_sites_in_gazetteer": [
                "harappa",
                "mohenjo daro",
            ],
            "linked_pairs_in_universe": 1,
            "closures": {
                "bead_craft": "NOT-YET-TESTABLE",
                "ceramic": "NOT ESTIMABLE",
            },
        },
        "spec031_period_rule": (
            "specs/031-stage2-q7-provenance-networks/spec.md "
            "section 6 (adopted 4A; F031-C10): a site is "
            "period-eligible iff its Stage 0 gazetteer "
            "period_label_as_published or Stage 0 program "
            "period assignment indicates Mature Harappan "
            "occupation as published; no finer temporal "
            "slicing is attempted"
        ),
        "extended_spine_rows": 205,
    },
    "environment": {
        "python": "3.12.3",
        "runner": "backend (venv glossa-lab)",
        "aee": (
            "1.5.0 (adopted environment, PR #231; "
            "package pinned >=1.5.0,<1.6)"
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
    "backend/tests/test_spec039_freeze.py",
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
