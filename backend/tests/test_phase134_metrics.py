"""Phase-134 metrics tests (pure functions; no local store)."""

import importlib.util
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / \
    "phase134_metrics.py"
_spec = importlib.util.spec_from_file_location(
    "phase134_metrics", SCRIPT)
metrics = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(metrics)


def test_kappa_perfect_agreement():
    a = ["UNICORN", "ZEBU", "SCRIPT_ONLY", "UNICORN"]
    kappa, po, pe, _ = metrics.cohens_kappa(a, list(a))
    assert po == 1.0
    assert kappa == 1.0


def test_kappa_known_value():
    # Classic 2-rater example restricted to two categories.
    a = ["UNICORN"] * 6 + ["ZEBU"] * 4
    b = ["UNICORN"] * 5 + ["ZEBU"] * 1 + ["UNICORN"] * 1 + \
        ["ZEBU"] * 3
    kappa, po, pe, _ = metrics.cohens_kappa(a, b)
    assert po == 0.8
    assert abs(pe - (0.6 * 0.6 + 0.4 * 0.4)) < 1e-12
    assert abs(kappa - (0.8 - 0.52) / (1 - 0.52)) < 1e-12


def test_kappa_chance_level():
    a = ["UNICORN", "ZEBU"] * 5
    b = ["ZEBU", "UNICORN"] * 5
    kappa, po, _, _ = metrics.cohens_kappa(a, b)
    assert po == 0.0
    assert kappa < 0


def test_categories_frozen_order():
    assert metrics.CATEGORIES == [
        "UNICORN", "ZEBU", "BUFFALO", "ELEPHANT", "RHINOCEROS",
        "GOAT_ANTELOPE", "TIGER", "COMPOSITE", "HUMAN_CULT",
        "GEOMETRIC", "SCRIPT_ONLY", "ILLEGIBLE"]
