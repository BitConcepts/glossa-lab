"""Spec 091 Stage 2 — supplementary locator pass tests.

Fixture side: synthetic extracted-page sets prove that a locator is
filed only from the adjudication table when the mechanical
cross-check corroborates it in the page text, that the build refuses
when the cross-check fails or the cited value does not match the
staged value under the pass's normalization, that a custody-PDF pin
mismatch refuses source construction, and that the delta builder
counts changes exactly.

Real-record side: when the supplementary artifact is present (it is
produced by the supplement's run, which needs the custody inputs),
its census is re-validated against the frozen provenance file, and
the filed delta and sample-verification records are checked for
internal consistency. These tests read only repo files — no custody
inputs — and skip when the records are absent.
"""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "backend" / "scripts" / "spec091_stage2_locator_supplement.py"
ARTIFACT = (
    REPO_ROOT
    / "backend"
    / "glossa_lab"
    / "data"
    / "mahadevan_parpola_crosswalk_v2_locators_supplement.json"
)
T202_ARTIFACT = (
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
RECORDS = REPO_ROOT / "specs" / "091-anchor-comparison-integrity" / "records"
DELTA = RECORDS / "stage-2-supplement-delta.json"
VERIFICATION = RECORDS / "stage-2-supplement-sample-verification.json"


def _load_module():
    spec = importlib.util.spec_from_file_location(
        "spec091_stage2_locator_supplement", SCRIPT
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


mod = _load_module()
base = mod.base


def _prov_entry(sign: str, value, source: str = "Parpola 1994 Appendix B") -> dict:
    return {
        "sign": sign,
        "mahadevan_id": sign,
        "parpola_id": "P" + sign[1:],
        "phonetic_reading": {
            "value": value,
            "source_as_stated": source,
        },
        "semantic_reading": {
            "value": None,
            "source_as_stated": source,
        },
    }


def _fixture_provenance() -> dict:
    return {
        "source_revision": "fixture v0",
        "entries": [
            _prov_entry("M261", "muruku"),
            _prov_entry("M002", "ku"),
            _prov_entry("M003", None),
        ],
    }


def _synthetic_1994_source(pages: dict) -> "mod.Source":
    return mod._parpola_source(
        work_key="1994",
        source_id="parpola_1994",
        work=mod.WORK_1994,
        pdf_sha256=mod.PARPOLA_1994_PDF_SHA256,
        pages=pages,
        legacy_font=False,
        pdf_offset=-18,
        layer_description="ocr_scan_text_layer",
    )


# Pages carrying the M261 adjudication's cross-check evidence: the
# cited value 'muruku' (letter-spaced, as the OCR renders it) and the
# designation 'circles' on PDF p. 247 (printed p. 229).
_M261_PAGES = {
    247: "the sign of 'two intersecting circles' engraved on many "
         "Harappan bangles denotes the Dravidian word m u r u k u",
    294: "ring(s)/bangle(s) m u r u k u boy, youth, Muruku",
}


def test_locator_filed_from_adjudicated_cross_checked_hit():
    record = mod.build_record_supp(
        _fixture_provenance(), {}, [_synthetic_1994_source(_M261_PAGES)],
        run_id="study-20260101T000000Z-abcdef", run_date="2026-01-01",
        input_pins={},
    )
    entry = record["entries"][0]
    assert entry["phonetic_reading"]["outcome"] == "located"
    locator = entry["phonetic_reading"]["locator"]
    assert locator["cited_value"] == "muruku"
    assert "§13.1" in locator["pinpoint"]
    assert locator["work"] == mod.WORK_1994
    # The semantic field is never located by a phonetic passage.
    assert entry["semantic_reading"]["outcome"] == "not_found"
    # Entries outside the adjudication table stay not-found, with the
    # documented search across the source.
    assert entry is record["entries"][0]
    other = record["entries"][1]
    assert other["phonetic_reading"]["outcome"] == "not_found"
    steps = other["phonetic_reading"]["not_found"]["search"]
    assert [s["source_id"] for s in steps] == ["parpola_1994"]
    assert record["summary"]["phonetic_reading"] == {"located": 1, "not_found": 2}


def test_cross_check_refusal_when_the_page_text_does_not_corroborate():
    pages = {247: "the sign of 'two intersecting circles' is discussed",
             294: "ring(s)/bangle(s)"}
    with pytest.raises(mod.LocatorPassError):
        mod.build_record_supp(
            _fixture_provenance(), {}, [_synthetic_1994_source(pages)],
            run_id="study-20260101T000000Z-abcdef", run_date="2026-01-01",
            input_pins={},
        )


def test_refusal_when_cited_value_does_not_match_the_staged_value():
    provenance = _fixture_provenance()
    provenance["entries"][0]["phonetic_reading"]["value"] = "tōḷ"
    with pytest.raises(mod.LocatorPassError):
        mod.build_record_supp(
            provenance, {}, [_synthetic_1994_source(_M261_PAGES)],
            run_id="study-20260101T000000Z-abcdef", run_date="2026-01-01",
            input_pins={},
        )


def test_custody_pin_mismatch_refuses_source_construction(tmp_path):
    bad_pdf = tmp_path / "bad.pdf"
    bad_pdf.write_bytes(b"not the recovered text")
    with pytest.raises(mod.LocatorPassError):
        mod.build_supplement_sources(
            REPO_ROOT,
            parpola_1994_pdf=bad_pdf,
            parpola_2010_pdf=bad_pdf,
            parpola_1994_pages_path=bad_pdf,
            parpola_2010_pages_path=bad_pdf,
        )


def test_value_normalization_forms():
    # The staged and cited spellings of the same reading meet.
    assert mod.value_forms("muu(n)-") & mod.value_forms("mu(m)")
    assert mod.value_forms("veL") & mod.value_forms("veḷ")
    assert mod.value_forms("min/mīn") & mod.value_forms("mīn")
    assert mod.value_forms("vaTa") & mod.value_forms("vaṭa")
    assert mod.value_forms("piLLai") & mod.value_forms("piḷḷai")
    # Different readings do not.
    assert not (mod.value_forms("kuTam") & mod.value_forms("kōḷ"))
    # The 2010 text layer's legacy-font encoding resolves (eZu = eḻu).
    toks = mod.page_tokens("the sequence eZu-miin gives seven stars", legacy_font=True)
    assert "elu" in toks
    # Letter-spaced OCR words rejoin.
    toks1994 = mod.page_tokens("denotes the word m u r u k u here", legacy_font=False)
    assert "muruku" in toks1994


def test_delta_builder_counts_and_carries_locators():
    def entry(sign, outcome, locator=None):
        block = {"outcome": outcome, "locator": locator, "not_found": None}
        return {"sign": sign,
                "phonetic_reading": dict(block),
                "semantic_reading": {"outcome": "not_found", "locator": None,
                                     "not_found": {"basis": "x", "search": []}}}

    loc = {"work": "W", "pinpoint": "p. 1", "sign_scheme": "S", "cited_value": "v"}
    t202 = {"run_id": "r1", "summary": {"n_entries": 2,
            "phonetic_reading": {"located": 0, "not_found": 2},
            "semantic_reading": {"located": 0, "not_found": 2}},
            "entries": [entry("M001", "not_found"), entry("M002", "not_found")]}
    supp = {"run_id": "r2", "summary": {"n_entries": 2,
            "phonetic_reading": {"located": 1, "not_found": 1},
            "semantic_reading": {"located": 0, "not_found": 2}},
            "entries": [entry("M001", "located", loc), entry("M002", "not_found")]}
    delta = mod.build_delta(t202, supp)
    assert delta["summary"]["phonetic_reading"] == {"changed": 1, "unchanged": 1}
    assert delta["summary"]["semantic_reading"] == {"changed": 0, "unchanged": 2}
    assert len(delta["changes"]) == 1
    assert delta["changes"][0]["sign"] == "M001"
    assert delta["changes"][0]["locator"] == loc
    assert "supplement" in delta["merge_rule"]


def test_validator_refuses_a_supplement_locator_missing_a_part():
    record = mod.build_record_supp(
        _fixture_provenance(), {}, [_synthetic_1994_source(_M261_PAGES)],
        run_id="study-20260101T000000Z-abcdef", run_date="2026-01-01",
        input_pins={},
    )
    broken = copy.deepcopy(record)
    broken["entries"][0]["phonetic_reading"]["locator"]["sign_scheme"] = ""
    with pytest.raises(mod.LocatorPassError):
        base.validate_locator_record(broken, ["M261", "M002", "M003"])


@pytest.mark.skipif(not ARTIFACT.exists(), reason="supplement artifact not yet generated")
def test_real_supplement_record_is_valid_and_total():
    record = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    provenance = json.loads(PROVENANCE.read_text(encoding="utf-8"))
    expected_signs = [e["sign"] for e in provenance["entries"]]
    base.validate_locator_record(record, expected_signs)
    assert record["summary"]["n_entries"] == 184
    for field in mod.FIELDS:
        census = record["summary"][field]
        assert census["located"] + census["not_found"] == 184
    assert record["supplement_to"]["run_id"] == mod.T202_RUN_ID
    # Every filed locator's cited value matches the entry's staged
    # value under the pass's normalization.
    prov_by_sign = {e["sign"]: e for e in provenance["entries"]}
    for e in record["entries"]:
        for field in mod.FIELDS:
            if e[field]["outcome"] == "located":
                staged = prov_by_sign[e["sign"]][field]["value"]
                cited = e[field]["locator"]["cited_value"]
                assert mod.value_forms(cited) & mod.value_forms(staged)


@pytest.mark.skipif(
    not (ARTIFACT.exists() and T202_ARTIFACT.exists() and DELTA.exists()),
    reason="supplement delta not yet filed",
)
def test_real_delta_matches_the_two_artifacts():
    t202 = json.loads(T202_ARTIFACT.read_text(encoding="utf-8"))
    supp = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    delta = json.loads(DELTA.read_text(encoding="utf-8"))
    rebuilt = mod.build_delta(t202, supp)
    assert delta["summary"] == rebuilt["summary"]
    assert delta["changes"] == rebuilt["changes"]


@pytest.mark.skipif(
    not (ARTIFACT.exists() and VERIFICATION.exists()),
    reason="supplement sample verification not yet filed",
)
def test_real_sample_verification_passes_and_covers_locators():
    verification = json.loads(VERIFICATION.read_text(encoding="utf-8"))
    record = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    assert verification["run_id"] == record["run_id"]
    assert verification["all_verified"] is True
    assert verification["all_locators_verified"] is True
    assert verification["n_locators_in_record"] == sum(
        1 for e in record["entries"] for f in mod.FIELDS
        if e[f]["outcome"] == "located"
    )
