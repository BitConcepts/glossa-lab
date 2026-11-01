"""Tests for the mesopotamian_contact loader hardening (C-8).

Before 2026-10-26, ``_safe_load`` returned ``{}`` silently when a
source file was missing, so a lost dataset was indistinguishable
from an empty one — the failure mode that hid the 2026-10-25
contact-zone loss (programme red team 2026-10-25, finding C-8).

No earlier test asserted that silent-empty behaviour by name; the
degradation was implicit in every caller that read ``.get(...)``
off the empty dict. These tests re-state the contract honestly:
a missing source RAISES ``FileNotFoundError`` naming the path,
and behaviour is unchanged when the file exists.

Author: rebuild-stream follow-ups, 2026-10-26.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from glossa_lab.data import mesopotamian_contact as mc


def test_safe_load_raises_on_missing_file(tmp_path):
    missing = tmp_path / "no_such_source.json"
    with pytest.raises(FileNotFoundError) as excinfo:
        mc._safe_load(missing)
    # The error names the missing path, so the loss is diagnosable.
    assert str(missing) in str(excinfo.value)


def test_safe_load_returns_parsed_content_when_file_exists(tmp_path):
    present = tmp_path / "present.json"
    present.write_text(json.dumps({"tablets": [1, 2, 3]}), encoding="utf-8")
    assert mc._safe_load(present) == {"tablets": [1, 2, 3]}


def test_public_getter_raises_on_missing_contact_zone_source(
    tmp_path, monkeypatch
):
    # Point the (lru-cached) meluhha loader at a missing file: the
    # getter must raise, not return an empty list as it did before
    # the hardening.
    missing = tmp_path / "meluhha_tablets.json"
    monkeypatch.setattr(mc, "_CDLI_MELUHHA", missing)
    mc._load_meluhha_tablets_data.cache_clear()
    try:
        with pytest.raises(FileNotFoundError) as excinfo:
            mc.get_meluhha_tablets()
        assert str(missing) in str(excinfo.value)
    finally:
        mc._load_meluhha_tablets_data.cache_clear()


def test_tracked_data_files_still_load_when_present():
    # Behaviour identical when files exist: the tracked data files
    # beside the module load and return their real contents.
    phonemes = mc.get_parpola_phoneme_map()
    assert isinstance(phonemes, dict) and phonemes
    findspots = mc.get_cisi_findspot_map()
    assert isinstance(findspots, dict) and findspots


def test_rebuilt_tracked_copies_carry_rebuild_labels():
    # C-10 / C-11 / F-13 (same PR): the tracked rebuilt copies
    # self-label as rebuilds, the seals metadata carries the
    # Phase-23 annotation, and the three none-tier seals carry
    # regenerated provenance that does not claim Phase-23a-verbatim
    # find_country.
    repo_root = Path(__file__).resolve().parents[2]
    base = (
        repo_root / "glossa-corpus" / "indus" / "sources"
        / "contact-zone-rebuilt-2026-10-25"
    )
    mel = json.loads((base / "meluhha_tablets.json").read_text("utf-8"))
    assert mel["rebuild"]["status"].startswith("REBUILT 2026-10-25")
    assert "#28" in mel["rebuild"]["register_citation"]
    assert len(mel["tablets"]) == 1462

    seals_doc = json.loads(
        (base / "seals_at_mesopotamia.json").read_text("utf-8")
    )
    md = seals_doc["metadata"]
    # The embedded historical block stands unaltered...
    assert md["phase23_sign_ingestion"]["n_seals"] == 13
    assert md["phase23_sign_ingestion"]["n_with_signs"] == 10
    assert md["phase23_sign_ingestion"]["total_indus_signs"] == 37
    # ...and the annotation beside it states this file's counts.
    annotation = md["phase23_sign_ingestion_annotation"]
    assert "14 seals" in annotation and "44" in annotation
    seals = seals_doc["seals"]
    assert len(seals) == 14
    assert sum(int(s.get("inscription_length") or 0) for s in seals) == 44
    for cid in (
        "AO_22310",
        "KONAR_SANDAL_S_CYLINDER",
        "AL_MAQSHA_TOKEN_2",
    ):
        rec = next(s for s in seals if s["catalogue_id"] == cid)
        assert rec["signs_confidence"] == "none"
        prov = rec["field_provenance"]
        assert "absent from that audit" in prov
        assert "re-derived" in prov
        assert (
            "find_country is verbatim from the Phase-23a audit"
            not in prov
        )
