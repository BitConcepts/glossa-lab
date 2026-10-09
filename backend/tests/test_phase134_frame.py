"""Phase-134 frame-rule tests (pure functions; no local store)."""

import importlib.util
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / \
    "phase134_frame.py"
_spec = importlib.util.spec_from_file_location("phase134_frame", SCRIPT)
frame = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(frame)


def test_site_group():
    assert frame.site_group("Mohenjo-Daro") == "Mohenjo-Daro"
    assert frame.site_group("Harappa") == "Harappa"
    assert frame.site_group("Lothal") == "Other"
    assert frame.site_group("") == "Other"


def test_parse_box():
    assert frame.parse_box("150;103;346;174") == [150, 103, 346, 174]
    assert frame.parse_box("") is None
    assert frame.parse_box("1;2;3") is None
    assert frame.parse_box("a;b;c;d") is None


def test_allocate_totals_and_minimum():
    cells = {("Mohenjo-Daro", "Seals"): 1054,
             ("Mohenjo-Daro", "Tablets"): 362,
             ("Mohenjo-Daro", "Graffiti"): 37,
             ("Harappa", "Seals"): 547,
             ("Harappa", "Tablets"): 475,
             ("Harappa", "Graffiti"): 253,
             ("Other", "Seals"): 405,
             ("Other", "Tablets"): 24,
             ("Other", "Graffiti"): 88}
    quotas = frame.allocate(cells, 100)
    assert sum(quotas.values()) == 100
    assert all(q >= 2 for q in quotas.values())
    # largest cell keeps the largest quota
    assert max(quotas, key=quotas.get) == ("Mohenjo-Daro", "Seals")


def test_allocate_small_total():
    cells = {("A", "Seals"): 10, ("B", "Seals"): 30}
    quotas = frame.allocate(cells, 10)
    assert sum(quotas.values()) == 10
    assert quotas[("B", "Seals")] > quotas[("A", "Seals")]


def test_chapter_family():
    base = {"motif_chapters": set()}
    assert frame.chapter_family(base) == "NONE"
    assert frame.chapter_family(
        {"motif_chapters": {"unicorn"}}) == "UNICORN"
    assert frame.chapter_family(
        {"motif_chapters": {"unicom"}}) == "UNICORN"
    assert frame.chapter_family(
        {"motif_chapters": {"SEALS"}}) == "NONMAPPABLE"
    assert frame.chapter_family(
        {"motif_chapters": {"tigerwithzebu"}}) == "NONMAPPABLE"


def test_hash_key_deterministic():
    assert frame.hash_key("cisi:v1:H-301") == \
        frame.hash_key("cisi:v1:H-301")
    assert frame.hash_key("cisi:v1:H-301") != \
        frame.hash_key("cisi:v1:H-302")
