"""Spec 069 freeze fences (Hunt depicted-kind classification, Asset A build).

Pins: (1) the frozen machine record replays exactly
(framework026 verify_freeze over every covered
source); (2) the definition carries the frozen
contract exactly - Spec 045 sections 2-3 quoted
verbatim under Spec 045's freeze digest, the
asset's form and home in this spec's directory
(DD-069-6), no jurisdiction coding at entry
(DD-069-8), the section 2.3 source hierarchy, the
blind-entry order with Spec 045's DD-045-16
spot-check decision carried (DD-069-9), the
dispute rule, the D-18 terminal empty feed
(DD-069-7), the full-crosswalk coverage scope of
gate A3, gates A1-A6 in order, the outcome
classes, the OSF filing (DD-069-10), and
Phase 432 (DD-069-11); (3) the governed claim
register is the frozen register (12 claims,
recovered to 0.9-draft, integrity-clean) and the
three freeze-hook artifacts record the pass on
the DD-069-12 reading (zero failure modes; no
claim below the 0.70 threshold; minimum
propagated 0.845); (4) the cited records still
carry the facts the design rests on - the
quotation in spec section 2 is character-exact
against Spec 045's frozen sections 2-3 on main,
Spec 045's freeze digest, the crosswalk pin and
its census (205 rows, 187 distinct registry sign
ids), the D-18 delivery's pin, empty signs array
and IDENTIFICATION FAILED closure, and the
anchors pin. These tests build no asset, enter
no row, and compute no corpus quantity.
"""
from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SPEC = REPO / "specs/069-hunt-asset-a"
FREEZE_JSON = SPEC / "freeze.json"
REGISTER = SPEC / "claims.json"
SPEC045 = REPO / "specs/045-hunt-depicted-kinds"
CROSSWALK = REPO / "data/crosswalks/sign_crosswalk_master.csv"
CONCORDANCE = (
    REPO / "specs/046-horned-tiger-concordance/concordance-297.json"
)
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"

SPEC045_DIGEST = (
    "5d8254ddc03045b68a0819f870fc9ccc1b9848a58fef3862dae3e4ca21b43f0a"
)
CROSSWALK_SHA256 = (
    "4ace1a617f40afe8d0bbb82e5461d98a675296152e7577b04fb67b00f4f5dfcf"
)
CONCORDANCE_SHA256 = (
    "772db4df152ec4f1071bed088250677e55f69743532c9e89f339a8cf9134aaaf"
)
ANCHORS_SHA256 = (
    "df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569"
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
    assert definition["experiment_id"] == "spec069-hunt-asset-a"
    assert definition["register"]["claims"] == 12
    assert definition["register"]["register_version"] == "0.9-draft"
    assert "PASSED" in definition["register"]["aee_hook_pass"]
    assert "0.845" in definition["register"]["aee_hook_pass"]
    design = definition["design"]
    assert design["phase"] == "Phase 432"
    assert SPEC045_DIGEST in design["contract"]
    assert "DD-069-6" in design["product"]
    assert "asset-a/depicted-kind-classification.csv" in design["product"]
    assert "DD-069-8" in design["product"]
    assert "CISI" in design["sources"]
    assert "never governing on its own" in design["sources"]
    assert "DD-069-9" in design["blind_entry"]
    assert "DD-045-16" in design["blind_entry"]
    assert "contested" in design["disputes"]
    assert CONCORDANCE_SHA256 in design["d18"]
    assert "DD-069-7" in design["d18"]
    assert "187 distinct sign keys" in design["coverage"]
    assert "ASSET FAILED" in design["gates"]
    assert "Specs 070 and 071 pin that digest" in design["freeze_point"]
    assert "Shakti corpus" in design["corpus_independence"]
    assert "49 percent" in design["limits"]
    assert design["outcomes"] == [
        "ASSET BUILT AND FROZEN",
        "ASSET FAILED",
        "BUILD NOT STARTED (gate A2)",
    ]
    assert "DD-069-10" in design["osf"]
    assert "Phase 432" in design["execution_gate"]
    inputs = definition["inputs"]
    assert inputs["spec045_freeze"]["digest"] == SPEC045_DIGEST
    assert inputs["crosswalk"]["sha256"] == CROSSWALK_SHA256
    assert inputs["crosswalk"]["rows"] == 205
    assert inputs["crosswalk"]["distinct_registry_sign_ids"] == 187
    assert inputs["d18_concordance"]["sha256"] == CONCORDANCE_SHA256
    assert inputs["anchors"]["sha256"] == ANCHORS_SHA256
    assert "bfc811df" in inputs["pin_verification"]


def test_register_integrity():
    register = json.loads(REGISTER.read_text(encoding="utf-8"))
    assert register["register_version"] == "0.9-draft"
    claims = register["claims"]
    assert len(claims) == 12
    ids = [c["id"] for c in claims]
    assert ids == [f"F069-C{i:02d}" for i in range(1, 13)]
    for claim in claims:
        assert claim["text"]
        assert claim["boundary"]
        assert claim["evidence"]
        for item in claim["evidence"]:
            assert item["kind"] == "observed"
            assert item["source_quality"] == "artifact"
            assert "independent_of" in item
    by_id = {c["id"]: c for c in claims}
    assert "DD-069-6" in by_id["F069-C03"]["boundary"]
    assert "DD-069-9" in by_id["F069-C05"]["boundary"]
    assert "DD-069-7" in by_id["F069-C07"]["boundary"]
    assert "Phase 432" in by_id["F069-C09"]["boundary"]
    assert "DD-069-10" in by_id["F069-C10"]["boundary"]


def test_hook_artifacts_record_the_pass():
    aee_dir = SPEC / "aee"
    for phase in ("after_specify", "after_plan", "after_tasks"):
        matches = sorted(aee_dir.glob(f"aee-{phase}-*.json"))
        assert len(matches) == 1, phase
        artifact = json.loads(matches[0].read_text(encoding="utf-8"))
        assert artifact["phase"] == phase
        assert artifact["outcome"] == "pass"
        failures = [
            f for claim in artifact["claims"] for f in claim["failures"]
        ]
        assert failures == []
        scores = artifact["scores"]
        assert min(s["propagated_score"] for s in scores.values()) >= 0.70
        ev = sorted(aee_dir.glob(f"evaluator-aee-{phase}-*.json"))
        assert len(ev) == 1, phase


def test_quotation_is_character_exact():
    spec_lines = (SPEC / "spec.md").read_text(encoding="utf-8").split("\n")
    begin = next(
        i for i, line in enumerate(spec_lines)
        if "BEGIN VERBATIM QUOTATION" in line
    )
    end = next(
        i for i, line in enumerate(spec_lines)
        if "END VERBATIM QUOTATION" in line
    )
    quoted = "\n".join(
        line[2:] if line.startswith("> ")
        else ("" if line.strip() == ">" else line)
        for line in spec_lines[begin + 1:end]
    ).strip()
    source_lines = (
        (SPEC045 / "spec.md").read_text(encoding="utf-8").split("\n")
    )
    start = next(
        i for i, line in enumerate(source_lines)
        if line.startswith("## 2. Asset A")
    )
    stop = next(
        i for i, line in enumerate(source_lines)
        if i > start and line.startswith("## 4.")
    )
    source = "\n".join(source_lines[start:stop]).strip()
    assert quoted == source


def test_input_pins_recompute():
    assert _sha(CROSSWALK) == CROSSWALK_SHA256
    assert _sha(CONCORDANCE) == CONCORDANCE_SHA256
    assert _sha(ANCHORS) == ANCHORS_SHA256
    freeze045 = json.loads(
        (SPEC045 / "freeze.json").read_text(encoding="utf-8")
    )
    assert freeze045["digest"] == SPEC045_DIGEST
    with CROSSWALK.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 205
    assert len({row["registry_sign_id"] for row in rows}) == 187
    concordance = json.loads(CONCORDANCE.read_text(encoding="utf-8"))
    assert concordance["signs"] == []
    assert "IDENTIFICATION FAILED" in concordance["closure"]["class"]
