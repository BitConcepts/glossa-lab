#!/usr/bin/env python3
"""Build the Spec 052 freeze record (freeze.json).

This builder was written at the freeze act of
2026-10-23. The register is the draft register
(0.5-draft) with the freeze's recovery completed
in three rounds (0.8-draft), the AEE lifecycle
hooks passed over it at the freeze gate, the
corpus-layer pins taken at the freeze from the
restricted-local store and the populations
reproduced from the pinned files, and the digest
is computed over the recovered register and the
finalised freeze texts exactly once, at the
freeze - the Spec 035 ordering. Run with the
backend venv python from the repository root:

    python specs/052-farmer-not-writing-soviet/build_freeze.py

Writes specs/052-farmer-not-writing-soviet/freeze.json
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

SPEC_DIR = "specs/052-farmer-not-writing-soviet"

CORPUS_SHA256 = (
    "345241b13fedada87b4783c24cd241123491bbd7edaf5bf636f9cdb36c01da68"
)
GRADES_SHA256 = (
    "02394241773cf8700f49ba19c30cdbaa589cf119d2c97c35e15e0447434dd739"
)
INTAKE_SHA256 = (
    "bd14e2b1f0607366ca1845797bcd17f8b577d23140a2e3111fe0cc2652cf9a9d"
)
SPEC068_DIGEST = (
    "ab890859c0ec313b4e2cdf89a9dddd885fae505e888c5f8c9ef2ba68c5f3c62d"
)
PHASE43_SHA256 = (
    "78a6c21908b9362854c54dd3d820d717be22feab3af11135663fa14aaf554fe4"
)
FARMER_SHA256 = (
    "41a855c9a79845206d7e63ed6fd835ef60f3611f3e825de5d73615ffba85425e"
)

DEFINITION = {
    "spec": f"{SPEC_DIR}/spec.md",
    "freeze_doc": f"{SPEC_DIR}/freeze.md",
    "experiment_id": "spec052-farmer-not-writing-soviet",
    "register": {
        "path": f"{SPEC_DIR}/claims.json",
        "claims": 19,
        "register_version": "0.8-draft",
        "aee_hook_pass": (
            "PASSED at the freeze act 2026-10-23 "
            "(applied-epistemic-engineering 1.5.3, lenient load, "
            "evidence verification off, no ledger): after_specify, "
            "after_plan and after_tasks over the recovered register "
            "each carried exactly 19 failure modes, every one an "
            "FR-2.3 draft-cap record; zero correctness failure "
            "modes; no claim below the 0.70 propagated-confidence "
            "threshold (minimum 0.72). Three recovery rounds "
            "(0.5-draft to 0.8-draft) are recorded in the register "
            "note and aee/freeze-aee-note.md."
        ),
    },
    "inputs": {
        "shakti_corpus": {
            "pin": (
                "restricted-local file (never committed): "
                "research_notes/indus-data-deep-sweep-20261008/"
                "downloads/shaktiosindia-indus-sign-regimes-deposit/"
                "sanitized_corpus.json"
            ),
            "sha256": CORPUS_SHA256,
            "bytes": 1570041,
            "census": {
                "rows": 5704,
                "analyzable": 5536,
                "grades": {
                    "documented-lineage": 3212,
                    "undocumented-corroborated": 2087,
                    "undocumented-uncorroborated": 405,
                },
                "tokens_all_analyzable": 18065,
                "distinct_signs_corpus": 713,
                "analyzable_with_cisi": 4904,
                "sites": 77,
            },
            "note": (
                "hash and census recomputed at the freeze from the "
                "held file; both match the intake record and Spec "
                "068's executed step-0 census"
            ),
        },
        "row_grades": {
            "pin": (
                "restricted-local file (never committed): "
                "research_notes/indus-data-deep-sweep-20261008/"
                "downloads/shakti_row_grades_2026-10-22.csv"
            ),
            "sha256": GRADES_SHA256,
            "rows": 5704,
        },
        "intake_record": {
            "path": "docs/decisions/2026-10-22-shakti-corpus-intake-record.md",
            "sha256": INTAKE_SHA256,
            "merged": "PR #339 (bfc811df)",
        },
        "spec_068_record": {
            "freeze_digest": SPEC068_DIGEST,
            "freeze_file": "specs/068-yadav-zipf-controls-successor/freeze.json",
            "outcome": "specs/068-yadav-zipf-controls-successor/outcome.md",
            "note": (
                "the populations of this freeze are Spec 068's "
                "primary and sensitivity limbs under its step-0 "
                "extraction (backend/scripts/"
                "phase430_yadav_zipf_controls.py: analyzable iff at "
                "least one symbol is not the layer's '000' "
                "placeholder; tokens exclude '000'; a row's sequence "
                "is its symbols with '000' removed), reproduced at "
                "this freeze from the pinned files, not re-derived"
            ),
        },
        "phase43_record": {
            "path": "outputs/phase43_all.json",
            "sha256": PHASE43_SHA256,
            "facts": {
                "signs_profiled": 201,
                "sequences": 3137,
                "terminal_strong_count": 20,
                "initial_strong_count": 40,
                "exhibited_terminal_strong": 10,
                "exhibited_terminal_rate_range": [0.683, 0.892],
                "exhibited_smallest_total": 22,
                "opening_candidate_267_99": {
                    "bigram_count": 251,
                    "dominance": 0.74,
                },
            },
            "use": (
                "consistency anchor only: the partition property "
                "(NB-1.2) and the NB-1.5 band check against the ten "
                "exhibited TERMINAL_STRONG rates, with NB-1.4's floor "
                "read against the exhibited smallest total. The "
                "Phase-43 battery itself is not reproduced, derived, "
                "or run (adjudication.md sec.9.1), and NB-1 is never "
                "presented under its name"
            ),
        },
        "farmer_claim_record": {
            "path": (
                "glossa-indus/claims/extracted_claims/"
                "farmer_sproat_witzel_2004.json"
            ),
            "sha256": FARMER_SHA256,
            "note": (
                "hash at the freeze. The draft's pin (c4cf441f...) "
                "predates a dated append to the file: the Spec 025 "
                "material audit's framing note of 2026-10-22 "
                "(proposal P1, commit 51cf8b3c). The claim itself is "
                "unchanged: status contradicted, stage explained, "
                "three contradicting-evidence entries"
            ),
        },
        "soviet_tables": (
            "retired from the member by adjudication.md sec.9.2; "
            "the draft's sec.2 pins stand in spec.md as history "
            "and are not inputs to the amended run"
        ),
    },
    "design": {
        "question": (
            "whether the positional behaviour of the Shakti "
            "corpus layer's documented-lineage population is "
            "consistent with the Farmer-Sproat-Witzel 'not "
            "writing' pattern, measured by battery NB-1 under the "
            "amended design - the consistency check of design "
            "D-01 re-pointed by the owner's rulings of 2026-10-23 "
            "after arm A as designed closed at the failed freeze "
            "of 2026-10-21"
        ),
        "battery": {
            "name": "NB-1 (amendment.md sec.3, claim F052-C16)",
            "NB-1.1": (
                "the population's inscriptions in the layer's own "
                "numbering and segmentation; sequences are the "
                "rows' sign sequences from the pinned layer; no "
                "re-segmentation, renumbering, or crosswalk is "
                "applied to any sign at any point"
            ),
            "NB-1.2": (
                "position classes initial (first sign), terminal "
                "(last sign), medial (every other occurrence), for "
                "sequences of length >= 2; sequences of length 1 "
                "are counted and reported separately and enter no "
                "count; every counted occurrence falls in exactly "
                "one class (partition property: initial + terminal "
                "+ medial counts sum to the sequence-length total "
                "over sequences of length >= 2)"
            ),
            "NB-1.3": (
                "per sign s and class c: count n_c(s) and total "
                "N(s) over sequences of length >= 2; rate r_c(s) = "
                "n_c(s) / N(s); counts and rates both reported"
            ),
            "NB-1.4": (
                "a sign is classifiable iff N(s) >= 20 (basis: the "
                "smallest total among the ten exhibited Phase-43 "
                "TERMINAL_STRONG signs is 22; the floor admits "
                "signs of that order at rate resolution 1/20 = "
                "0.05; explicitly not a recovered Phase-43 value)"
            ),
            "NB-1.5": (
                "for classifiable signs: TERMINAL_STRONG iff "
                "r_terminal >= 2/3; TERMINAL_MODERATE iff 1/2 <= "
                "r_terminal < 2/3; INITIAL_ and MEDIAL_ by the same "
                "bands on their rates (basis: 2/3 sits just below "
                "the lowest exhibited Phase-43 TERMINAL_STRONG "
                "rate, 0.683, exhibited range 0.683-0.892, so the "
                "frozen Phase-43 strong set passes the consistency "
                "check against this band; the initial/medial bands "
                "are the same numbers by symmetry, a labelled "
                "design choice)"
            ),
            "NB-1.6": (
                "opening bigrams: the first two signs of each "
                "sequence of length >= 2; dominance of a pair = its "
                "count / B, where B = the number of sequences of "
                "length >= 2 (this repairs the Phase-43 record's "
                "denominator-less 0.74 and its self-contradiction "
                "on the (267, 99) count)"
            ),
            "NB-1.7": (
                "chance baseline: a within-sequence permutation "
                "null (each sequence's length and sign multiset "
                "fixed, order uniformly permuted), 999 permutations, "
                "seed 43052, over the primary population; the "
                "chance level of a statistic is its nearest-rank "
                "95th percentile across the 999 values (the 950th "
                "smallest); statistics: the TERMINAL_STRONG count "
                "and the maximum opening-bigram dominance"
            ),
            "NB-1.8": (
                "condition F: at least one TERMINAL_STRONG sign "
                "exists AND the observed TERMINAL_STRONG count "
                "exceeds its NB-1.7 chance level. Condition O: the "
                "top opening bigram's count is at least 10 AND its "
                "dominance exceeds its NB-1.7 chance level (the "
                "count floor of 10 is a stated design choice of "
                "this amendment)"
            ),
            "NB-1.9": (
                "TOO THIN gate: fewer than 30 sequences of length "
                ">= 3 in the primary population, or fewer than 10 "
                "classifiable signs, closes the run TOO THIN "
                "before conditions F and O are evaluated"
            ),
        },
        "populations": {
            "primary": (
                "analyzable documented-lineage rows of the Shakti "
                "corpus layer (Spec 068's primary limb): 3,045 "
                "rows, 11,805 tokens, 557 distinct signs; length "
                "census 2,942 sequences of length >= 2, 2,068 of "
                "length >= 3, 103 of length 1; 90 classifiable "
                "signs"
            ),
            "sensitivity": (
                "analyzable documented-lineage + "
                "undocumented-corroborated rows (Spec 068's "
                "sensitivity limb): 5,131 rows, 17,216 tokens, 707 "
                "distinct signs; 2,889 sequences of length >= 3; "
                "112 classifiable signs; run and reported with the "
                "same prominence as the primary only if the primary "
                "run reaches an outcome word"
            ),
            "venue": (
                "restricted local store only; the Shakti source "
                "rows never enter git; publishable products are the "
                "dataset label, the census, the per-sign "
                "quantities, the strong sets, the null percentiles, "
                "and the outcome word"
            ),
            "lineage_limit": (
                "the layer is a CISI-tradition compilation, a "
                "distinct compilation lineage from the Soviet "
                "compilation and from Holdat/M77, but its editions "
                "cover substantially the same excavated objects; "
                "agreement is cross-compilation robustness, not "
                "independent discovery"
            ),
        },
        "gates": {
            "A": (
                "corpus pin: the corpus-layer file and the "
                "row-grades file hash to the freeze values; "
                "failure INVALID"
            ),
            "B": (
                "population reproduction: extracting the primary "
                "population from the pinned layer under the frozen "
                "limb reproduces the freeze-recorded counts exactly "
                "(3,045 rows / 11,805 tokens / 557 distinct signs); "
                "failure INVALID"
            ),
            "C": (
                "determinism: the battery implementation, run "
                "twice over the pinned layer with seed 43052, "
                "produces identical outputs; failure INVALID"
            ),
            "D": (
                "thinness: NB-1.9 applied to the primary "
                "population; failure closes the run TOO THIN, with "
                "the census as its finding"
            ),
            "retired": (
                "BATTERY NOT PINNABLE cannot occur under the "
                "amendment; the draft's Soviet gates 0.1-0.3 and "
                "0.5 and the sec.4.3 mapping-failure closures are "
                "retired with the Soviet tables"
            ),
            "retained": (
                "NOT ADJUDICATED is retained for a chance baseline "
                "that cannot be computed as frozen"
            ),
        },
        "outcomes": [
            "CONSISTENT",
            "INCONSISTENT",
            "PARTIAL",
            "TOO THIN",
        ],
        "outcome_semantics": (
            "amendment.md sec.6, claim F052-C19: CONSISTENT iff "
            "neither condition F nor condition O holds on the "
            "primary population (the Farmer pattern present in "
            "the CISI-lineage corpus too; the recorded caveat "
            "narrows); INCONSISTENT iff both hold (the caveat "
            "widens); PARTIAL (DD-052-3, retained) iff exactly "
            "one holds, the outcome naming which; TOO THIN is "
            "gate D's closure. The word CONSISTENT is "
            "deliberately re-pointed from the draft sec.4.1 "
            "mapping, which used it for the both-signatures case; "
            "the amendment governs. Every outcome is appended, in "
            "the same words, to the parent claim's record and to "
            "each of the three fragments' records, naming the "
            "dataset (the Shakti corpus layer, CISI-compilation "
            "lineage) and the battery (NB-1, this amendment as "
            "frozen); the census and the per-sign quantities "
            "publish before the outcome word (spec sec.6 headline "
            "rules)"
        ),
        "claims_served": {
            "farmer_sproat_witzel_2004_manual_001": (
                "the parent claim (SETTLED - contradicted, stage "
                "explained, record SHA-256 41a855c9... at the "
                "freeze); no outcome of the amended run moves it "
                "(spec sec.6, sec.7 limit 1)"
            ),
            "fragments": (
                "indus_valley_script_deciphered_from_myth_"
                "65ff0a26_critique_0001, "
                "indus_valley_script_deciphered_from_myth_"
                "65ff0a26_critique_0002, "
                "without_kings_or_conquests_the_indus_scr_"
                "ce9d98cc_language_0001 (SETTLED as restatements of "
                "the parent proposition; the outcome is appended to "
                "each in the same words; status unchanged)"
            ),
        },
        "phase": "Phase-437",
        "freeze_does_not": (
            "execute the study or compute any positional "
            "quantity; derive, reconstruct, or reproduce the "
            "Phase-43 battery; map or use the Soviet tables; "
            "design or execute arm B; publish or copy any "
            "restricted corpus row; move the parent claim's or "
            "any fragment's recorded status"
        ),
        "execution_gate": (
            "execution (Phase-437) begins only on a separate "
            "owner order, after the OSF registration filed at "
            "this freeze is approved; step 0 re-asserts every "
            "freeze pin before any positional quantity is "
            "computed, and gates A-D run in order"
        ),
    },
}

SOURCES = [
    f"{SPEC_DIR}/freeze.md",
    f"{SPEC_DIR}/spec.md",
    f"{SPEC_DIR}/claims.json",
    f"{SPEC_DIR}/adjudication.md",
    f"{SPEC_DIR}/amendment.md",
    f"{SPEC_DIR}/aee/freeze-aee-note.md",
    f"{SPEC_DIR}/build_freeze.py",
    "backend/tests/test_spec052_freeze.py",
]


def main() -> int:
    record = build_freeze(DEFINITION, REPO, SOURCES)
    out = REPO / SPEC_DIR / "freeze.json"
    out.write_text(
        json.dumps(record, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(record["digest"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
