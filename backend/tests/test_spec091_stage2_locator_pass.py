"""Spec 091 Stage 2 — locator record tests (T201 acceptance; T202 census).

Fixture side: a synthetic provenance set + a synthetic held primary
source prove the locator path files a three-part locator, that a
file-level citation and an in-repo pointer do NOT file one, and that
the generator/validator refuses an entry filed with neither outcome.

Real-artifact side: when the generated locator record is present
(it is produced by the T202 run), its census is re-derived from the
frozen provenance file and checked exactly, and the sample
verification file is checked against the sample rule. When the
record is absent the census test skips — the stage record states
why (the run executes only with the held sign-list datasets at
their canonical source-store paths).
"""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "backend" / "scripts" / "spec091_stage2_locator_pass.py"
ARTIFACT = (
    REPO_ROOT
    / "backend"
    / "glossa_lab"
    / "data"
    / "mahadevan_parpola_crosswalk_v2_locators.json"
)
PROVENANCE = (
    REPO_ROOT
    / "backend"
    / "glossa_lab"
    / "data"
    / "mahadevan_parpola_crosswalk_v2_provenance.json"
)
VERIFICATION = (
    REPO_ROOT
    / "specs"
    / "091-anchor-comparison-integrity"
    / "records"
    / "t202-sample-verification.json"
)


def _load_module():
    spec = importlib.util.spec_from_file_location("spec091_stage2_locator_pass", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


mod = _load_module()


def _prov_entry(sign: str, value, source: str = "Parpola 1994 Appendix B") -> dict:
    return {
        "sign": sign,
        "mahadevan_id": sign,
        "parpola_id": "P" + sign[1:],
        "phonetic_reading": {
            "value": value,
            "field": "reading" if value is not None else None,
            "source_as_stated": source,
            "locator_present": False,
            "locator": None,
            "value_origin": "project_anchor_table_copy",
            "source_revision": "fixture",
        },
        "semantic_reading": {
            "value": None,
            "source_as_stated": source,
            "locator_present": False,
            "value_origin": "not_recorded_separately",
        },
    }


def _fixture_provenance() -> dict:
    return {
        "source_revision": "fixture v0",
        "entries": [
            _prov_entry("M001", "aa"),
            _prov_entry("M002", "ku"),
            _prov_entry("M003", None),
        ],
    }


def _grounding_source(values: dict) -> "mod.Source":
    """A synthetic HELD primary source carrying values at pinpoints."""

    def search(ctx, field):
        return {
            "status": "searched",
            "method": "fixture lookup",
            "facts": {"held": True},
            "result": "fixture source searched",
        }

    def locate(ctx, field):
        if field != "phonetic_reading":
            return None
        hit = values.get(ctx["sign"])
        if hit is None:
            return None
        return {
            "work": "Fixture Work (held primary source)",
            "pinpoint": hit["pinpoint"],
            "sign_scheme": "Mahadevan sign numbers",
            "cited_value": hit["value"],
        }

    return mod.Source(
        "fixture_primary",
        "Fixture Work (held primary source)",
        held=True,
        held_as=None,
        sha256=None,
        can_ground_locator=True,
        search=search,
        locate=locate,
    )


def _pointer_source() -> "mod.Source":
    """An in-repo derivative: consulted, never grounds a locator."""

    def search(ctx, field):
        return {
            "status": "searched",
            "method": "fixture lookup",
            "facts": {"hit": True},
            "result": "fixture pointer hit",
        }

    return mod.Source(
        "fixture_pointer",
        "Fixture in-repo table",
        held=True,
        held_as=None,
        sha256=None,
        can_ground_locator=False,
        search=search,
    )


def test_locator_filed_from_held_primary_source():
    sources = [_grounding_source({"M001": {"value": "aa", "pinpoint": "p. 1, fig. 1"}})]
    record = mod.build_record(
        _fixture_provenance(), {}, sources,
        run_id="study-20260101T000000Z-abcdef", run_date="2026-01-01", input_pins={},
    )
    entry = record["entries"][0]
    assert entry["phonetic_reading"]["outcome"] == "located"
    locator = entry["phonetic_reading"]["locator"]
    assert locator["cited_value"] == "aa"
    assert locator["pinpoint"] == "p. 1, fig. 1"
    # The semantic field is not located by a phonetic passage.
    assert entry["semantic_reading"]["outcome"] == "not_found"
    assert record["summary"]["phonetic_reading"] == {"located": 1, "not_found": 2}


def test_in_repo_pointer_never_grounds_a_locator():
    record = mod.build_record(
        _fixture_provenance(), {}, [_pointer_source()],
        run_id="study-20260101T000000Z-abcdef", run_date="2026-01-01", input_pins={},
    )
    for entry in record["entries"]:
        for field in mod.FIELDS:
            assert entry[field]["outcome"] == "not_found"
            assert entry[field]["not_found"]["search"]


def test_validator_refuses_an_entry_with_neither_outcome():
    record = mod.build_record(
        _fixture_provenance(), {}, [_pointer_source()],
        run_id="study-20260101T000000Z-abcdef", run_date="2026-01-01", input_pins={},
    )
    broken = copy.deepcopy(record)
    broken["entries"][1]["phonetic_reading"] = {
        "staged_value": "ku",
        "source_as_stated": "Parpola 1994 Appendix B",
        "outcome": "unexamined",
        "locator": None,
        "not_found": None,
    }
    with pytest.raises(mod.LocatorPassError):
        mod.validate_locator_record(broken, ["M001", "M002", "M003"])


def test_validator_refuses_a_locator_missing_a_part():
    record = mod.build_record(
        _fixture_provenance(), {},
        [_grounding_source({"M001": {"value": "aa", "pinpoint": "p. 1"}})],
        run_id="study-20260101T000000Z-abcdef", run_date="2026-01-01", input_pins={},
    )
    broken = copy.deepcopy(record)
    broken["entries"][0]["phonetic_reading"]["locator"]["pinpoint"] = "  "
    with pytest.raises(mod.LocatorPassError):
        mod.validate_locator_record(broken, ["M001", "M002", "M003"])


def test_validator_refuses_an_undocumented_not_found():
    record = mod.build_record(
        _fixture_provenance(), {}, [_pointer_source()],
        run_id="study-20260101T000000Z-abcdef", run_date="2026-01-01", input_pins={},
    )
    broken = copy.deepcopy(record)
    broken["entries"][0]["semantic_reading"]["not_found"]["search"] = []
    with pytest.raises(mod.LocatorPassError):
        mod.validate_locator_record(broken, ["M001", "M002", "M003"])


def test_execute_refuses_when_a_held_source_is_absent(tmp_path):
    with pytest.raises(mod.LocatorPassError):
        mod.build_real_sources(tmp_path)


@pytest.mark.skipif(not ARTIFACT.exists(), reason="locator record not yet generated (T202 run)")
def test_real_record_census_is_total_over_the_frozen_provenance():
    record = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    provenance = json.loads(PROVENANCE.read_text(encoding="utf-8"))
    expected_signs = [e["sign"] for e in provenance["entries"]]
    mod.validate_locator_record(record, expected_signs)
    assert record["summary"]["n_entries"] == 184 == len(expected_signs)
    for field in mod.FIELDS:
        census = record["summary"][field]
        assert census["located"] + census["not_found"] == 184


@pytest.mark.skipif(not VERIFICATION.exists(), reason="sample verification not yet filed (T202 run)")
def test_sample_verification_covers_the_rule_and_passes():
    record = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    verification = json.loads(VERIFICATION.read_text(encoding="utf-8"))
    assert verification["run_id"] == record["run_id"]
    assert verification["all_verified"]
    sampled = {r["sign"] for r in verification["results"]}
    assert sampled == set(mod.sample_signs(record))
    assert verification["n_sampled"] == len(sampled) >= 16
