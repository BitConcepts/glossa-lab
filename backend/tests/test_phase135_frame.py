"""Phase-135 frame-rule tests (pure functions; no local store)."""

import importlib.util
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / \
    "phase135_frame.py"
_spec = importlib.util.spec_from_file_location("phase135_frame", SCRIPT)
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
    assert max(quotas, key=quotas.get) == ("Mohenjo-Daro", "Seals")


def test_allocate_small_total():
    cells = {("A", "Seals"): 10, ("B", "Seals"): 30}
    quotas = frame.allocate(cells, 10)
    assert sum(quotas.values()) == 10
    assert quotas[("B", "Seals")] > quotas[("A", "Seals")]


def test_exclude_frame_removes_exactly_the_frame():
    eligible = {f"k{i}": {"canonical_key": f"k{i}"} for i in range(10)}
    kept, removed = frame.exclude_frame(eligible, ["k2", "k5", "k9"])
    assert sorted(kept) == ["k0", "k1", "k3", "k4", "k6", "k7", "k8"]
    assert removed == ["k2", "k5", "k9"]
    assert not (set(kept) & {"k2", "k5", "k9"})


def test_exclude_frame_ignores_keys_not_in_population():
    eligible = {"k0": {"canonical_key": "k0"}}
    kept, removed = frame.exclude_frame(eligible, ["k0", "zz"])
    assert kept == {}
    assert removed == ["k0"]


def test_seed_is_the_phase135_salt():
    assert frame.SEED == "phase135-20261009"
    # the salt actually drives the hash order
    assert frame.hash_key("cisi:v1:M-1") != \
        frame.hash_key("cisi:v1:M-2")
