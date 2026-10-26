"""Spec 077 freeze fences (three-witness sign-list triangulation).

Pins: (1) the frozen machine record replays exactly
(framework026 verify_freeze over every covered
source); (2) the definition carries the frozen
design exactly - the M7 design carried as written
with its amendment, the pins (Registry v2
42ab09fb..., the Spec 075 machine record
f55ae911..., dataset v3 9c619bfe..., the Wells 1998
dataset 22bde128..., the C-7 raw text 11441e38...),
the frozen bars (at least 502 of 557; token 999's
administered conditions), the closure words, no OSF
registration at this freeze (DD-077-5), and Phase
443; (3) the governed claim register is the frozen
register (10 claims, drafted directly in the
recovered 0.7-draft form, integrity-clean) and the
three freeze-hook artifacts record the pass as it
ran: 21 findings per artifact - the 10 FR-2.3 draft
caps, the 10 irreducibility challenges, and the 1
negation-conflict challenge (F077-C01 against
F077-C03) answered at DD-077-3 - zero findings of
independence, ambiguity, or evidence-resolution
kind, no claim below the 0.70 threshold (minimum
propagated 0.7200); (4) the cited inputs still
carry the facts the design rests on - Registry
v2's digest and row count recomputed in the tree,
the anchors' standing counts (287 / 94 / 44), Spec
075's census as printed in its machine record
(3,045 / 557 / 550; token 999 at 2 rows / 2
occurrences), and the M77 raw text's digest. These
tests run no counting, file no verdict, and attack
no token.
"""
from __future__ import annotations

import csv
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SPEC = REPO / "specs/077-signary-triangulation"
FREEZE_JSON = SPEC / "freeze.json"
REGISTER = SPEC / "claims.json"
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
REGISTRY_V2 = REPO / "data/crosswalks/canonical_sign_registry_v2.csv"
PHASE441 = REPO / "reports/phase441_results.json"
M77_RAW = REPO / "data/mahadevan_m77_raw.txt"

ANCHORS_SHA256 = (
    "df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569"
)
REGISTRY_V2_SHA256 = (
    "42ab09fb06750098dc8cc0370c4ba4c1a538353d943a49f983d7347f52e8ef71"
)
PHASE441_SHA256 = (
    "f55ae91124e1ac74268f79035d862586a81a2f2e9596fd2318f3741c6e39ea29"
)
M77_RAW_SHA256 = (
    "11441e38286784a1f4215f73d91cbba8acd153b7e5b30daed9252f9f7b77304a"
)
DESIGN_SHA256 = (
    "2e9f9967ec30a558e3a31f93f54540b3d8450e25080c447d37ecd598175c1369"
)

sys.path.insert(0, str(REPO / "backend"))


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_freeze_record_replays():
    from glossa_lab.framework026 import verify_freeze

    record = json.loads(FREEZE_JSON.read_text(encoding="utf-8"))
    assert record["digest"]
    assert verify_freeze(record, REPO) == []


def test_freeze_definition_constants():
    record = json.loads(FREEZE_JSON.read_text(encoding="utf-8"))
    definition = record["definition"]
    assert (
        definition["experiment_id"]
        == "spec077-signary-triangulation"
    )
    assert definition["register"]["claims"] == 10
    assert definition["register"]["register_version"] == "0.7-draft"
    assert "aee 1.5.3" in definition["register"]["aee_hook_pass"]
    assert "0.7200" in definition["register"]["aee_hook_pass"]
    assert "21 findings" in definition["register"]["aee_hook_pass"]
    assert DESIGN_SHA256 in definition["basis"]["design"]
    design = definition["design"]
    assert design["phase"] == "Phase 443"
    assert "502 of 557" in design["bars"]
    assert design["closures"] == [
        "SUPPORTED",
        "NOT SUPPORTED",
        "SIGNARY NOT WITNESSED AT THE STATED LEVEL",
        "NO PUBLISHED IDENTITY",
        "CANNOT BE RUN AS WRITTEN",
    ]
    assert "No OSF registration" in design["osf"]
    assert "DD-077-5" in design["osf"]
    assert "not deciphered" in design["limits"]
    inputs = definition["inputs"]
    assert inputs["registry_v2"]["sha256"] == REGISTRY_V2_SHA256
    assert inputs["registry_v2"]["rows"] == 1013
    assert inputs["registry_v2"]["breakdown"] == {
        "parpola_1982": 396,
        "yajnadevam_glyphid": 407,
        "icit_wells": 210,
    }
    assert inputs["population_record"]["sha256"] == PHASE441_SHA256
    assert inputs["population_record"]["census"] == {
        "analyzable_rows": 3045,
        "distinct_signs": 557,
        "signs_in_sequences_ge2": 550,
    }
    assert inputs["population_record"]["token_999"] == {
        "primary_rows": 2, "occurrences": 2, "finals": 0,
    }
    assert inputs["witness_m77"]["rows"] == 417
    assert inputs["witness_wells1998"]["printed_entries"] == 587
    assert inputs["witness_wells1998"]["fig36_pairings"] == 55
    assert inputs["anchors"]["sha256"] == ANCHORS_SHA256
    assert inputs["anchors"]["entries"] == 287


def test_register_integrity():
    register = json.loads(REGISTER.read_text(encoding="utf-8"))
    assert register["register_version"] == "0.7-draft"
    claims = register["claims"]
    assert len(claims) == 10
    ids = [c["id"] for c in claims]
    assert ids == [f"F077-C{i:02d}" for i in range(1, 11)]
    for claim in claims:
        assert claim["text"]
        assert claim["boundary"]
        assert claim["evidence"]
        for item in claim["evidence"]:
            assert item["kind"] == "observed"
            assert item["source_quality"] == "artifact"
            assert "independent_of" in item
    by_id = {c["id"]: c for c in claims}
    assert "502" in by_id["F077-C01"]["text"]
    assert "NO PUBLISHED IDENTITY" in by_id["F077-C02"]["text"]
    assert "3,045" in by_id["F077-C04"]["text"]
    assert "M409" in by_id["F077-C06"]["text"]
    assert "13372" in by_id["F077-C10"]["text"]


FREEZE_STAMPS = [
    "20261026T142310Z",
    "20261026T142310Z",
    "20261026T142310Z",
]

CHALLENGE_IDS = {
    "AEE-F077-C01-IRREDUCIBILITY-CHALLENGE",
    "AEE-F077-C01-NEGATION-CONFLICT-CHALLE",
    "AEE-F077-C02-IRREDUCIBILITY-CHALLENGE",
    "AEE-F077-C03-IRREDUCIBILITY-CHALLENGE",
    "AEE-F077-C04-IRREDUCIBILITY-CHALLENGE",
    "AEE-F077-C05-IRREDUCIBILITY-CHALLENGE",
    "AEE-F077-C06-IRREDUCIBILITY-CHALLENGE",
    "AEE-F077-C07-IRREDUCIBILITY-CHALLENGE",
    "AEE-F077-C08-IRREDUCIBILITY-CHALLENGE",
    "AEE-F077-C09-IRREDUCIBILITY-CHALLENGE",
    "AEE-F077-C10-IRREDUCIBILITY-CHALLENGE",
}

FORBIDDEN_CATEGORIES = {
    "independence_unmodeled",
    "ambiguous_requirement",
}


def test_freeze_hook_artifacts_record_the_pass():
    aee_dir = SPEC / "aee"
    for phase, stamp in zip(
        ("after_specify", "after_plan", "after_tasks"),
        FREEZE_STAMPS,
    ):
        record = json.loads(
            (aee_dir / f"aee-{phase}-{stamp}.json").read_text(
                encoding="utf-8"
            )
        )
        assert record["phase"] == phase
        failures = [
            f for c in record["claims"] for f in c["failures"]
        ]
        assert failures, phase
        assert not [
            f for f in failures if f["category"] in FORBIDDEN_CATEGORIES
        ], phase
        non_cap = [f for f in failures if f["category"] != "draft_cap"]
        assert {f["id"] for f in non_cap} == CHALLENGE_IDS, phase
        assert all(f["id"].endswith("CHALLENGE") or f["id"].endswith("CHALLE")
                   for f in non_cap), phase
        caps = [f for f in failures if f["category"] == "draft_cap"]
        assert len(caps) == 10, phase
        confidences = [c["confidence"] for c in record["claims"]]
        assert min(confidences) >= 0.70, phase
        scores = record["scores"]
        assert (
            min(s["propagated_score"] for s in scores.values()) >= 0.70
        ), phase
        evaluator = (
            aee_dir / f"evaluator-aee-{phase}-{stamp}.json"
        )
        assert evaluator.exists(), phase


def test_input_pins_recompute():
    assert _sha(ANCHORS) == ANCHORS_SHA256
    assert _sha(REGISTRY_V2) == REGISTRY_V2_SHA256
    assert _sha(PHASE441) == PHASE441_SHA256
    assert _sha(M77_RAW) == M77_RAW_SHA256
    anchors = json.loads(ANCHORS.read_text(encoding="utf-8"))["anchors"]
    assert len(anchors) == 287
    standings = Counter(
        v.get("validation_status") for v in anchors.values()
    )
    assert standings["strict_sa_independent"] == 94
    assert standings["pending_non_sa_validation"] == 44
    with REGISTRY_V2.open(encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    assert len(rows) == 1013
    systems = Counter(r["numbering_system"] for r in rows)
    assert systems == {
        "parpola_1982": 396,
        "yajnadevam_glyphid": 407,
        "icit_wells": 210,
    }
    # The 13 duplicated Mahadevan ids of Spec 073's accounting,
    # recomputed from the pinned registry: each claimed by
    # exactly two parpola_1982 rows.
    claims_by_id: dict[str, set[str]] = {}
    for r in rows:
        if r["numbering_system"] != "parpola_1982":
            continue
        for m in (r["mahadevan_ids"] or "").split("|"):
            if m:
                claims_by_id.setdefault(m, set()).add(r["sign_id"])
    duplicated = {
        m for m, ss in claims_by_id.items() if len(ss) == 2
    }
    assert duplicated == {
        "M002", "M050", "M064", "M076", "M099", "M103", "M161",
        "M167", "M168", "M199", "M216", "M264", "M409",
    }
    record441 = json.loads(PHASE441.read_text(encoding="utf-8"))
    assert record441["census"]["population"] == {
        "analyzable_rows": 3045,
        "distinct_signs": 557,
        "signs_in_sequences_ge2": 550,
    }
    assert record441["census"]["token_999"] == {
        "primary_rows": 2, "occurrences": 2,
    }
    assert len(record441["keyed_population"]) == 556
