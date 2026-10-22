"""Spec 029 freeze fences (Tao claim lifecycle).

Pins: (1) the machine freeze record replays exactly
(framework026 verify_freeze over every frozen source);
(2) the frozen definition carries the adjudicated
design constants; (3) the reclassification ledger's
section 3 counts — the Phase D migration's target —
are exactly the audited ones; (4) the governed claim
register is the recovered register (13 claims,
integrity-clean).
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SPEC = REPO / "specs/029-tao-claim-lifecycle"
FREEZE_JSON = SPEC / "freeze.json"
LEDGER = SPEC / "reclassification-ledger.json"
REGISTER = SPEC / "claims.json"

sys.path.insert(0, str(REPO / "backend"))


def test_freeze_record_replays():
    from glossa_lab.framework026 import verify_freeze

    record = json.loads(FREEZE_JSON.read_text(encoding="utf-8"))
    assert record["digest"]
    # Freeze amendment (closeout, task X2, recorded in
    # closeout-record.md section 4 under freeze.md
    # section 2): the single closeout tick pass changed
    # checkbox states in tasks.md only -- no task text --
    # and this test's acknowledgment of that amendment
    # is the amendment's only other file. Those two
    # named drifts are the only permitted ones; the
    # freeze itself was never regenerated (freeze.json
    # untouched) and any other changed, missing, or
    # altered source still fails here.
    assert verify_freeze(record, REPO) == [
        "frozen source changed: "
        "backend/tests/test_spec029_freeze.py",
        "frozen source changed: "
        "specs/029-tao-claim-lifecycle/tasks.md",
    ]


def test_freeze_definition_constants():
    record = json.loads(FREEZE_JSON.read_text(encoding="utf-8"))
    definition = record["definition"]
    assert definition["experiment_id"] == "spec029-tao-claim-lifecycle"
    assert definition["register"]["claims"] == 13
    assert definition["register"]["register_version"] == "draft-2"
    design = definition["design"]
    assert design["stage_vocabulary"] == [
        "created", "checked", "explained", "accepted", "digested",
    ]
    assert design["automation_cap"] == "checked"
    inputs = definition["inputs"]
    assert inputs["ledger_entries"] == 345
    assert inputs["verified_unexplained_flags"] == 105


def test_ledger_section3_counts():
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    entries = ledger["entries"]
    assert len(entries) == 345

    by_class: dict[str, Counter] = {}
    for entry in entries:
        by_class.setdefault(entry["class"], Counter())[
            entry.get("honest_stage")
        ] += 1

    assert by_class["anchor_reading"]["created"] == 193
    assert by_class["anchor_reading"]["checked"] == 94
    assert by_class["extracted_claim"]["created"] == 21
    assert by_class["extracted_claim"]["checked"] == 10
    assert by_class["registered_prediction"]["created"] == 3
    assert by_class["registered_prediction"]["checked"] == 2
    assert by_class["hypothesis_model"]["created"] == 3
    assert by_class["study_headline_claim"]["checked"] == 10

    totals = Counter(e.get("honest_stage") for e in entries)
    assert totals["created"] == 220
    assert totals["checked"] == 116
    assert totals["explained"] == 0
    assert totals["accepted"] == 0
    assert totals["digested"] == 0

    flagged = sum(
        1 for e in entries
        if "verified_unexplained" in (e.get("flags") or [])
    )
    assert flagged == 105


def test_register_is_the_recovered_one():
    from glossa_lab.aee_core import Claim
    from glossa_lab.framework026 import check_dependency_integrity

    reg = json.loads(REGISTER.read_text(encoding="utf-8"))
    assert reg["register_version"] == "draft-2"
    claims = [Claim.from_dict(c) for c in reg["claims"]]
    assert len(claims) == 13
    ids = {c.id for c in claims}
    assert {"F029-C11", "F029-C12", "F029-C13"} <= ids
    for claim in reg["claims"]:
        assert claim["evidence"], claim["id"]
        assert claim["metadata"].get("boundary_confirmation"), claim["id"]
    report = check_dependency_integrity(claims)
    assert report["ok"] is True
