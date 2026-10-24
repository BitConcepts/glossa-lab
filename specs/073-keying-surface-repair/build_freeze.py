#!/usr/bin/env python3
"""Build the Spec 073 freeze record (freeze.json).

This builder was written at the freeze act of
2026-10-23. The register was recovered from the
draft register (0.5-draft) to 0.9-draft in four
recovery rounds finished before the digest (the
record is in aee/freeze-aee-note.md and in the
register's own note), the AEE lifecycle hooks
passed over the recovered register, the
freeze-stage exhibits were performed in order
(every section 2 pin re-asserted, OPEN-073-9;
the ruled source list exhibited with two
sources struck for non-exhibition, OPEN-073-1;
freeze.md sections 3-4), and the digest is
computed over the recovered register and the
finalised freeze texts exactly once, at the
freeze - the Spec 035 ordering. Run with the
Glossa backend venv python from the repository
root:

    python specs/073-keying-surface-repair/build_freeze.py

Writes specs/073-keying-surface-repair/freeze.json
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

SPEC_DIR = "specs/073-keying-surface-repair"

DEFINITION = {
    "spec": "specs/073-keying-surface-repair/spec.md",
    "freeze_doc": "specs/073-keying-surface-repair/freeze.md",
    "experiment_id": "spec073-keying-surface-repair",
    "register": {
        "path": "specs/073-keying-surface-repair/claims.json",
        "register_version": "0.9-draft",
        "claims": 16,
        "aee_hook_pass": (
            "PASSED at the freeze act of 2026-10-23 under aee 1.5.3: the draft register "
            "(0.5-draft) was recovered in four rounds finished before the digest - round 1 "
            "(0.6-draft) restated every evidence item in engine values (kind observed, "
            "source_quality artifact); round 2 (0.7-draft) restated every claim head as a "
            "single proposition with its clauses carried into its boundary, added "
            "independent_of declarations to every evidence item, and carried the freeze "
            "rulings into the boundaries of F073-C03, C05, C06, C07, C08, C09 and C14; "
            "round 3 (0.8-draft) restated the ten remaining irreducibility-challenged "
            "heads to single clauses; round 4 (0.9-draft) restated the last two heads - "
            "and at the final round after_specify, after_plan and after_tasks each "
            "carried 16 FR-2.3 draft-cap records only, zero correctness failure modes, "
            "and no claim below the 0.70 threshold (minimum propagated 0.795); the "
            "engine outcome word reads iterate solely from the draft-cap records (gate "
            "reading DD-038-10; record in "
            "specs/073-keying-surface-repair/aee/freeze-aee-note.md)"
        ),
    },
    "basis": {
        "adjudication": "specs/073-keying-surface-repair/adjudication.md",
        "decisions": (
            "DECIDED by the owner on 2026-10-23 (not proposals): freeze Spec 073 with "
            "the draft's stated defaults and execute it - the governing source list and "
            "hierarchy confirmed as drafted, with Mahadevan 1977 and Wells 1998 struck "
            "from this study's ruled list at the freeze for non-exhibition (OPEN-073-1); "
            "Registry v2's form and the icit_wells value confirmed (OPEN-073-2); the "
            "attested frame confirmed as documented + corroborated rows (OPEN-073-3); "
            "the row_origin field confirmed (OPEN-073-4); two-pass entry checking as "
            "executed for v1, no added spot check (OPEN-073-5); direct entry under the "
            "hierarchy, no D-18-style concordance input, d18_input = none (OPEN-073-6); "
            "the OSF contract registration filed at the freeze (OPEN-073-7); the "
            "execution phase allocated as Phase-436 (OPEN-073-8); every section 2 pin "
            "re-asserted at the freeze (OPEN-073-9); DD-073-1 to DD-073-7 confirmed as "
            "drafted. The freeze record (freeze.md sections 2-4) carries each ruling "
            "and the freeze-stage exhibits."
        ),
    },
    "design": {
        "phase": "Phase-436",
        "claims_served": {
            "manual_003": (
                "without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_003 - IN "
                "QUESTION, as Spec 070's closure left it; this spec appends to it "
                "nothing and computes no quantity under its test"
            ),
            "manual_004": (
                "without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_004 - "
                "UNTESTED, as Specs 050/071 left it; this spec appends to it nothing "
                "and computes no quantity under its test"
            ),
        },
        "hierarchy": {
            "ruling": (
                "OPEN-073-1 confirmed as drafted: governing, in order - (1) CISI (the "
                "Corpus of Indus Seals and Inscriptions sign list, Shah and Parpola "
                "eds.); (2) Fuls 2023, A Catalog of Indus Signs; (3) Parpola 1994, as "
                "consulted in held form (the CISI volumes' own list and Parpola 2010's "
                "published identifications in the same numbering). Corroborating: Fuls "
                "2023, Corpus of Indus Inscriptions. Locators only, never evidence "
                "(DD-073-3): Yajnadevam and its derivatives, the Fuls volumes' "
                "April-2026 OCR texts, the ICIT documentation, and the registry's "
                "derived rate columns"
            ),
            "struck_at_the_freeze": {
                "wells_1998": (
                    "An Introduction to Indus Writing (MA thesis, University of "
                    "Calgary; DOI 10.11575/PRISM/23641) - struck for non-exhibition: "
                    "resolved at record level only; no copy held and the full-text "
                    "fetch from the publisher repository was refused (HTTP 403). "
                    "Wells identities enter Registry v2 only through the published "
                    "lists that state them (the CISI list's Wells grapheme statements "
                    "and the Catalog), never through the thesis itself"
                ),
                "mahadevan_1977": (
                    "The Indus Script: Texts, Concordance and Tables - struck for "
                    "non-exhibition: only the introduction's OCR text is held in the "
                    "program's sources; the sign-list tables are not in hand on the "
                    "executing machine. Nothing is entered, corroborated, or contested "
                    "from either struck source in this study; their standing in Spec "
                    "045's hierarchy as a program matter is untouched"
                ),
            },
            "exhibits": (
                "freeze.md section 4: CISI volumes 1-2 as the Internet Archive scans "
                "(sha256 8278d815450cb23cf04ffb1ffb43f62a6206bfc75f9a61f505b92eb41c627908 "
                "and 727132579a485ee626e48a64c663148a85fbc0811fb523818fd615231f8a327d), "
                "the sign list entered through the held mayig digitization at commit "
                "ad2f1e218a34b8c33c57de0d6cb8d99272765bbb; CISI 3.1 restricted-local "
                "under PROVENANCE entry 22 (scan sha256 "
                "772e929782119ff9293088e060562c18f14234e7a24efdf3deb68669fea67afa); the "
                "Fuls volumes under PROVENANCE entry 27; Parpola 2010 lecture PDF "
                "(sha256 c58137e54cdde3f2acdcfaf05293dfc5f5ba33def3e0b12585c451f76bd4ba84)"
            ),
        },
        "registry_v2": {
            "ruling": (
                "OPEN-073-2 confirmed: a new versioned file in v1's field order with "
                "no new columns; v1's 803 rows carried verbatim; additions only in "
                "the two forms of spec section 4.2 - (a) Wells-map completions on "
                "existing parpola_1982 rows, (b) new rows with numbering_system = "
                "icit_wells for ICIT codes with no v1 row in any numbering system, "
                "sign_id = W + the zero-padded code, wells_ids carrying that code, "
                "description carrying the source's verbatim description where the "
                "source states one; every addition cited cell-by-cell in the change "
                "schedule (registry-v2/change-schedule.json) with the source, the "
                "page or entry, and the source's own wording; conflicting published "
                "identities recorded as CONTESTED IDENTITY, never resolved; the "
                "residual attested codes named in registry-v2/no-published-identity.json"
            ),
            "path": "data/crosswalks/canonical_sign_registry_v2.csv",
            "record_dir": "specs/073-keying-surface-repair/registry-v2/",
        },
        "frame": (
            "OPEN-073-3 confirmed: the attested frame is the distinct ICIT codes "
            "attested in the Shakti corpus's documented and corroborated rows (P-F1 "
            "S4), enumerated from the pinned corpus at the build and published with "
            "its count; uncorroborated rows attest nothing"
        ),
        "asset_a_v2": {
            "ruling": (
                "a new asset with its own digest at "
                "specs/073-keying-surface-repair/asset-a-v2/ "
                "(depicted-kind-classification.csv + asset-a-v2-freeze.json): Asset A "
                "v1's 187 rows carried verbatim, each marked row_origin = carried_v1 "
                "(OPEN-073-4); new rows only for frame signs resolving to exactly one "
                "Registry v2 identity, keyed by that identity's registry sign_id, "
                "each marked row_origin = new_entry; Asset A v1's file, freeze "
                "record, and digest are never written by this spec"
            ),
            "entry": (
                "blind under Spec 045 sections 2.2-2.5 as carried in spec section "
                "5.3: the enterer is given frame signs in code order with, per sign, "
                "only its candidate governing-source depictions, verbatim with "
                "citations - no occurrence counts, no positional material, no "
                "population membership, no Spec 070/071 output beyond gate 0.2's "
                "published baselines; two passes (an enterer pass coding from the "
                "verbatim labels under the fixed reading rules, then an independent "
                "deterministic rule pass over the entered labels), disagreements "
                "adjudicated by re-reading the verbatim label, on the record in "
                "asset-a-v2/entry-decisions.json (OPEN-073-5); disputes coded "
                "contested with both labels; silence coded unidentified with the "
                "sources searched, never pooled; direct entry only, d18_input = "
                "none on every new row (OPEN-073-6)"
            ),
        },
        "baselines": {
            "A": (
                "Spec 070's opening-strong set: 31 signs; 26 keyed to Asset A rows, "
                "5 unkeyable - ICIT 136 (6 occurrences), 298 (7), 401 (5), 617 (56), "
                "824 (16) in the primary population"
            ),
            "B": (
                "Spec 071's coverage census: 557 distinct signs in the documented "
                "stratum; 285 carrying an Asset A row; 134 with no resolution in the "
                "registry's parpola_1982 Wells map; 138 resolving to registry signs "
                "outside Asset A's 187-row universe"
            ),
            "C": "the parpola_1982 Wells map of registry v1: 498 distinct Wells ids",
            "D": (
                "Asset A v1's census: 187 rows - animal 20, sky_cycle 0, "
                "object_goods 14, human 25, other 127, contested 0, unidentified 1"
            ),
        },
        "measures": (
            "computed only after both product digests exist, over the v2-route join "
            "of spec section 6 (DD-070-9's route restated against the v2 files): "
            "M1 Registry v2's distinct Wells ids against the 498 baseline; M2 the "
            "five named codes' dispositions by name (resolved and keyed / NO "
            "PUBLISHED IDENTITY / CONTESTED IDENTITY); M3 the keyable shares of the "
            "31-sign set (baseline 26) and the 557-sign set (baseline 285), "
            "remainders listed sign by sign by reason; M4 Asset A v2's census by "
            "kind x row_origin, the celestial count stated plainly beside Spec "
            "071's recorded floor of 30 as a comparison of numbers only; M5 the "
            "no-published-identity schedule, restated in the headline block. No "
            "coverage figure is a target, a floor, or a success condition anywhere "
            "in the design (DD-073-4)"
        ),
        "outcomes": [
            "KEYING SURFACE REPAIRED",
            "REPAIRED WITH NAMED SHORTFALL",
            "INPUT PIN MISMATCH",
            "SHAKTI INTAKE NOT REPRODUCED",
            "BASELINE NOT REPRODUCED",
            "SOURCE NOT IN HAND",
            "ENTRY DISCIPLINE FAILED",
            "ASSET FAILED (gate named)",
            "FROZEN INPUT MUTATED",
        ],
        "freeze_does_not": (
            "the freeze itself adds no registry row, enters no depiction, and "
            "computes no coverage figure; it re-opens nothing in Spec 070's or Spec "
            "071's closures, changes neither Hunt claim's standing, and amends "
            "neither Spec 045's contract nor Spec 069's asset; it promises nothing "
            "about the celestial class reaching Spec 071's floor of 30, or one "
            "member; and it does not decide whether either Hunt question should be "
            "re-asked - a re-freeze consuming the v2 products is a separate owner "
            "decision"
        ),
        "execution_gate": (
            "execution (Phase-436) runs after this freeze has merged and the OSF "
            "contract registration is filed, under the execution order given in the "
            "same owner tasking that commissioned this freeze; the registration's "
            "approval act remains the owner's click and is not performed by the "
            "freeze or the execution"
        ),
    },
    "inputs": {
        "registry_v1": {
            "path": "data/crosswalks/canonical_sign_registry.csv",
            "sha256": "8a0b2a82ac8d226d574ce01f5550c581efd91a97cab86201a62f7a7e435bd420",
            "rows": 803,
            "wells_map_distinct_ids": 498,
            "five_codes_absent": ["W136", "W298", "W401", "W617", "W824"],
        },
        "crosswalk": {
            "path": "data/crosswalks/sign_crosswalk_master.csv",
            "sha256": "4ace1a617f40afe8d0bbb82e5461d98a675296152e7577b04fb67b00f4f5dfcf",
            "rows": 205,
            "distinct_sign_ids": 187,
        },
        "asset_a_v1": {
            "csv_path": "specs/069-hunt-asset-a/asset-a/depicted-kind-classification.csv",
            "csv_sha256": "952319355098698f01e6d8499b0384f84ac964e1bc4ecdc03c77ed920c7a5b5b",
            "freeze_record_path": "specs/069-hunt-asset-a/asset-a/asset-a-freeze.json",
            "rows": 187,
            "census": {
                "animal": 20,
                "sky_cycle": 0,
                "object_goods": 14,
                "human": 25,
                "other": 127,
                "contested": 0,
                "unidentified": 1,
            },
            "contract": (
                "Spec 045 sections 2-3 under freeze digest "
                "5d8254ddc03045b68a0819f870fc9ccc1b9848a58fef3862dae3e4ca21b43f0a"
            ),
        },
        "spec_070_record": {
            "freeze_digest": "763108f89311ab2791827b347a155a8b4f9abad940ab59f921af129f79c73e3e",
            "machine_record": {
                "path": "reports/phase433_results.json",
                "sha256": "667560a5c185051ea7acc9afacf2f9c4bbf3f863e9d17851c634fa56eb3ad214",
            },
            "outcome": "POPULATION NOT KEYED (gate 0.4)",
        },
        "spec_071_record": {
            "freeze_digest": "c06a7a86804d8da2c9896638446f5712be9eccb8716a7b02303a5944f4bc0478",
            "machine_record": {
                "path": "reports/phase434_results.json",
                "sha256": "7158f79ce416e5e01fee041e6e97df827d3a048f9c1c178a8200bd79f68bbda7",
            },
            "outcome": "INVALID (gate 0.3)",
        },
        "shakti_corpus": {
            "file": "sanitized_corpus.json (restricted-local, never in git)",
            "sha256": "345241b13fedada87b4783c24cd241123491bbd7edaf5bf636f9cdb36c01da68",
            "bytes": 1570041,
        },
        "row_grades": {
            "file": "shakti_row_grades_2026-10-22.csv (restricted-local, never in git)",
            "sha256": "02394241773cf8700f49ba19c30cdbaa589cf119d2c97c35e15e0447434dd739",
        },
        "intake_record": {
            "path": "docs/decisions/2026-10-22-shakti-corpus-intake-record.md",
            "merged": "PR #339, merge commit bfc811df",
            "census": (
                "5,704 rows; 5,536 analyzable; grades 3,212 documented-lineage / "
                "2,087 undocumented-corroborated / 405 undocumented-uncorroborated; "
                "713 distinct signs corpus-wide; documented stratum alone 557 "
                "distinct signs - reproduced exactly at Specs 068-072's freezes and "
                "re-asserted by reference at this freeze"
            ),
        },
        "fuls_volumes": {
            "provenance": "PROVENANCE entry 27 (held on TRISTEN-DESKTOP, pinned in place)",
            "corpus_pdf_sha256": "185fd0575d881568583a7002d705b2ded1313a525fafe093108f72e0fe897727",
            "catalog_pdf_sha256": "31729a4f7b33bd1ec08633bb677f963b5de8f50d96afdfc25cff5ddc96f9a32a",
            "corpus_ocr_txt_sha256_local": "d8aab17680af50012a8d78487c9e047dfc1f9d93d7cbcd4ed3c5c5a84acb5cc5",
            "catalog_ocr_txt_sha256_local": "3e9c6758b112364f33c057c7c8464324511fa6008662aaeae26e10f1962df27c",
        },
        "pin_verification": (
            "at the freeze of 2026-10-23 every committed pin above was re-derived "
            "from the tree the freeze was built on (the PR #352 branch tree, whose "
            "pinned files are byte-identical to main's at d20bc1bc), the "
            "restricted-local pins were recomputed on the held files, and the Fuls "
            "OCR locator texts were recomputed on the local copies; every recomputed "
            "hash equals its pin (freeze.md section 3)"
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
    "specs/073-keying-surface-repair/freeze.md",
    "specs/073-keying-surface-repair/spec.md",
    "specs/073-keying-surface-repair/claims.json",
    "specs/073-keying-surface-repair/adjudication.md",
    "specs/073-keying-surface-repair/aee/freeze-aee-note.md",
    "specs/073-keying-surface-repair/build_freeze.py",
    "backend/tests/test_spec073_freeze.py",
]


def main() -> int:
    record = build_freeze(DEFINITION, REPO, SOURCES)
    out = REPO / SPEC_DIR / "freeze.json"
    out.write_text(
        json.dumps(record, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(record["digest"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
