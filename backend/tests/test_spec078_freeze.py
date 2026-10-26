"""Spec 078 freeze fences (projected-constraint bridge redesign).

Pins: (1) the frozen machine record replays exactly
(framework026 verify_freeze over every covered
source); (2) the definition carries the frozen
design exactly - the M13 design carried as written,
the inherited pilot frame's pins (export 08fc96c8...,
anchors df0cf620..., Registry v2 42ab09fb...), the
successor pilot's frozen bars (total failures at
most 3, neither line above 2, administrability at
least 25 of the 86 counted signs, the pattern clause
of FF-078-4), the freeze-fixed completions (the
counted-population definition FF-078-2, the
blindness protocol FF-078-3, the execution order
FF-078-5 with step 2 inherited, not re-run), an OSF
registration filed at this freeze (DD-078-5), and
Phase 444; (3) the governed claim register is the
frozen register (10 claims, drafted directly in the
recovered 0.7-draft form, integrity-clean) and the
three freeze-hook artifacts record the pass as it
ran: 19 findings per artifact - the 10 FR-2.3 draft
caps plus the 9 named irreducibility challenges -
zero findings of contradiction, independence,
ambiguity, or evidence-resolution kind, no claim
below the 0.70 threshold (minimum propagated
0.7200); (4) the cited inputs still carry the facts
the design rests on - the export's, anchors', and
Registry v2's digests and counts recomputed in the
tree, the anchors' standing counts (287 / 94 / 44),
the inherited census headline figures as printed in
spec section 7.1 (2,906 records to 11,507 tokens;
5,883 strict tokens; slot totals; the finals
partition; base rates to 4dp), and the counted
population of 86 derived under FF-078-2 (94 strict
minus 5 frame-absent minus 3 worked examples).
These tests run no pilot step, code no basis, and
derive no register.
"""
from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SPEC = REPO / "specs/078-projected-constraint-bridge-redesign"
FREEZE_JSON = SPEC / "freeze.json"
REGISTER = SPEC / "claims.json"
EXPORT = REPO / "glossa-corpus/indus/exports/indus_research.jsonl"
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
REGISTRY_V2 = REPO / "data/crosswalks/canonical_sign_registry_v2.csv"

EXPORT_SHA256 = (
    "08fc96c8dbc22a37effb65e789b22b144f4baf22be1da55dc3d84db5dc44505e"
)
ANCHORS_SHA256 = (
    "df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569"
)
REGISTRY_V2_SHA256 = (
    "42ab09fb06750098dc8cc0370c4ba4c1a538353d943a49f983d7347f52e8ef71"
)
DESIGN_SHA256 = (
    "8bb02c07a8ad3245a899da660c48430b4cf1e16a53b1fb53a132215093e9a211"
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
        == "spec078-projected-constraint-bridge-redesign"
    )
    assert definition["register"]["claims"] == 10
    assert definition["register"]["register_version"] == "0.7-draft"
    assert "aee 1.5.3" in definition["register"]["aee_hook_pass"]
    assert "0.7200" in definition["register"]["aee_hook_pass"]
    assert DESIGN_SHA256 in definition["basis"]["design"]
    design = definition["design"]
    assert design["phase"] == "Phase 444"
    assert "NC-1 to NC-8" in design["pilot"]
    assert "not re-run" in design["pilot"]
    assert "counted population of 86" in design["pilot"]
    assert "at most 3" in design["bars"]
    assert "neither line exceeding 2" in design["bars"]
    assert "at least 25 of the 86" in design["bars"]
    assert design["closures"] == [
        "PILOT PASSES",
        "CANNOT BE RUN AS WRITTEN",
        "CANNOT BE ADMINISTERED — THE CORE MAKES TOO FEW CHECKABLE CLAIMS",
        "BRIDGE DOES NOT HOLD",
        "NOT-RUN",
    ]
    assert "OSF registration IS filed" in design["osf"]
    assert "DD-078-5" in design["osf"]
    assert "not deciphered" in design["limits"]
    inputs = definition["inputs"]
    assert inputs["corpus_export"]["sha256"] == EXPORT_SHA256
    assert inputs["corpus_export"]["m77_records"] == 2906
    frame = inputs["corpus_export"]["frame"]
    assert frame["tokens"] == 11507
    assert frame["strict_tokens"] == 5883
    assert frame["slot_totals"] == {
        "init": 2655, "fin": 2655, "solo": 225, "med": 5972,
    }
    assert frame["finals_partition"]["no_anchor"] == 178
    assert frame["base_rates"] == {
        "init": 0.2307, "fin": 0.2307, "med": 0.519, "solo": 0.0196,
    }
    assert frame["counted_population"] == {
        "strict": 94, "frame_absent": 5, "frame_attested": 89,
        "worked_examples": 3, "counted": 86,
    }
    assert inputs["anchors"]["sha256"] == ANCHORS_SHA256
    assert inputs["anchors"]["entries"] == 287
    assert inputs["anchors"]["strict"] == 94
    assert inputs["anchors"]["pending"] == 44
    assert inputs["registry_v2"]["sha256"] == REGISTRY_V2_SHA256
    assert inputs["registry_v2"]["rows"] == 1013


def test_register_integrity():
    register = json.loads(REGISTER.read_text(encoding="utf-8"))
    assert register["register_version"] == "0.7-draft"
    claims = register["claims"]
    assert len(claims) == 10
    ids = [c["id"] for c in claims]
    assert ids == [f"F078-C{i:02d}" for i in range(1, 11)]
    for claim in claims:
        assert claim["text"]
        assert claim["boundary"]
        assert claim["evidence"]
        for item in claim["evidence"]:
            assert item["kind"] == "observed"
            assert item["source_quality"] == "artifact"
            assert "independent_of" in item
    by_id = {c["id"]: c for c in claims}
    assert "86" in by_id["F078-C02"]["text"]
    assert "25" in by_id["F078-C02"]["text"]
    assert "A-FACE-2" in by_id["F078-C06"]["text"]
    assert "residue" in by_id["F078-C06"]["falsification_tests"][0]
    assert "M002" in by_id["F078-C08"]["boundary"]
    assert "triple" in by_id["F078-C09"]["text"]
    assert "not deciphered" in by_id["F078-C10"]["text"]


FREEZE_STAMPS = [
    "20261026T144557Z",
    "20261026T144557Z",
    "20261026T144557Z",
]

CHALLENGE_IDS = {
    "AEE-F078-C01-IRREDUCIBILITY-CHALLENGE",
    "AEE-F078-C02-IRREDUCIBILITY-CHALLENGE",
    "AEE-F078-C03-IRREDUCIBILITY-CHALLENGE",
    "AEE-F078-C04-IRREDUCIBILITY-CHALLENGE",
    "AEE-F078-C06-IRREDUCIBILITY-CHALLENGE",
    "AEE-F078-C07-IRREDUCIBILITY-CHALLENGE",
    "AEE-F078-C08-IRREDUCIBILITY-CHALLENGE",
    "AEE-F078-C09-IRREDUCIBILITY-CHALLENGE",
    "AEE-F078-C10-IRREDUCIBILITY-CHALLENGE",
}

FORBIDDEN_CATEGORIES = {
    "contradiction",
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
        assert all(f["id"].endswith("-CHALLENGE") for f in non_cap), phase
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
    assert _sha(EXPORT) == EXPORT_SHA256
    assert _sha(ANCHORS) == ANCHORS_SHA256
    assert _sha(REGISTRY_V2) == REGISTRY_V2_SHA256
    anchors = json.loads(ANCHORS.read_text(encoding="utf-8"))["anchors"]
    assert len(anchors) == 287
    standings = Counter(
        v.get("validation_status") for v in anchors.values()
    )
    assert standings["strict_sa_independent"] == 94
    assert standings["pending_non_sa_validation"] == 44
    with REGISTRY_V2.open(encoding="utf-8") as fh:
        import csv

        assert len(list(csv.DictReader(fh))) == 1013
    # The inherited census headline figures and the FF-078-2 counted
    # population, recomputed from the pinned export under the spec's
    # token construction - the pilot's step-0 gate reproduces these
    # at its run.
    strict_ids = {
        k[1:]
        for k, v in anchors.items()
        if v.get("validation_status") == "strict_sa_independent"
    }
    m77 = 0
    tokens = 0
    strict_tokens = 0
    attested: set[str] = set()
    for line in EXPORT.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        rec = json.loads(line)
        if rec["source_system"] != "indusscript-m77":
            continue
        m77 += 1
        for g in rec["canonical_grapheme_ids"]:
            if g == "000" or g.startswith("*"):
                continue
            tokens += 1
            attested.add(g)
            if g in strict_ids:
                strict_tokens += 1
    assert m77 == 2906
    assert tokens == 11507
    assert strict_tokens == 5883
    frame_absent = {s for s in strict_ids if s not in attested}
    assert frame_absent == {"039", "044", "046", "362", "374"}
    frame_attested = strict_ids & attested
    assert len(frame_attested) == 89
    counted = frame_attested - {"002", "342", "347"}
    assert len(counted) == 86
