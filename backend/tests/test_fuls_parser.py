"""Tests for the Fuls corpus parser."""

from glossa_lab.data.fuls_parser import (
    entries_to_glossa_format,
    parse_corpus_entry,
    parse_inscription_line,
    parse_sign_catalog_entry,
)


def test_parse_simple_inscription():
    """Parse a basic Fuls-notation inscription."""
    result = parse_inscription_line("+407-032-520-100-585-017-231+")
    assert result is not None
    assert result["sign_ids"] == ["407", "032", "520", "100", "585", "017", "231"]
    assert result["total_signs"] == 7
    assert not result["has_eroded"]


def test_parse_multi_part_inscription():
    """Parse an inscription with multiple text parts."""
    result = parse_inscription_line("+144+700-033+")
    assert result is not None
    assert result["num_parts"] == 2
    assert result["sign_ids"] == ["144", "700", "033"]


def test_parse_eroded_signs():
    """Detect eroded signs (000)."""
    result = parse_inscription_line("+342-000-267-099+")
    assert result is not None
    assert result["has_eroded"] is True


def test_parse_invalid_line():
    """Non-inscription lines return None."""
    assert parse_inscription_line("") is None
    assert parse_inscription_line("just text") is None
    assert parse_inscription_line("no plus signs 123-456") is None


def test_parse_corpus_entry_with_metadata():
    """Parse a block with site and object info."""
    block = """M-1088 Mohenjo-daro
square seal, unicorn
R/L
+740-540-002-820+"""
    entry = parse_corpus_entry(block)
    assert entry is not None
    assert entry["findspot"] == "Mohenjo-daro"
    assert entry["object_type"] == "square_seal"
    assert entry["iconography"] == "unicorn_bull"
    assert entry["reading_direction"] == "R/L"
    assert entry["inscription"]["total_signs"] == 4


def test_entries_to_glossa_format():
    """Convert parsed entries to Glossa Lab upload format."""
    entries = [
        {
            "inscription": {
                "sign_ids": ["342", "099", "267"],
                "text_parts": [["342", "099", "267"]],
                "num_parts": 1,
                "total_signs": 3,
                "has_eroded": False,
                "raw": "+342-099-267+",
            },
            "findspot": "Harappa",
        },
        {
            "inscription": {
                "sign_ids": ["336", "000", "342"],
                "text_parts": [["336", "000", "342"]],
                "num_parts": 1,
                "total_signs": 3,
                "has_eroded": True,
                "raw": "+336-000-342+",
            },
        },
    ]
    result = entries_to_glossa_format(entries)
    assert result["name"] == "Indus Corpus (Fuls)"
    assert result["corpus_type"] == "target"
    # Eroded signs (000) should be filtered
    assert "000" not in result["content"]
    assert result["metadata"]["inscription_count"] == 2


def test_parse_sign_catalog():
    """Parse a sign catalog entry."""
    entry = parse_sign_catalog_entry("Sign 342: frequency 580, terminal, TMK")
    assert entry is not None
    assert entry["sign_id"] == "342"
    assert entry["frequency"] == 580
    assert entry["position_class"] == "terminal"
    assert entry["function"] == "TMK"
