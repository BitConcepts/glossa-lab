"""Tests for Phase-113 (spec 011) non-SA validation battery.

Covers: the frozen syllable canon, reading normalization,
positional profiles / modal class / TV arithmetic, the section-5
decision-rule truth table, set recomputation against the real
repo files (44 / 94 / 113), graph registration (H23), and a toy
end-to-end: a core-consistent synthetic anchor validates, an
isolated one demotes, an unattested one stays unresolved.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

from glossa_lab.phase113_battery import (
    FAIL, INDETERMINATE, NOT_ATTESTED, PASS, CoreGrammar,
    CorpusContext, canon_legal, decide, evaluate_anchor,
    modal_class, normalize_reading, positional_counts, syllabify,
    tv_distance,
)
from glossa_lab.phase113_run import compute_sets

BACKEND = Path(__file__).resolve().parents[1]
REPO = BACKEND.parent


def _phase58_validator():
    spec = importlib.util.spec_from_file_location(
        "phase58_phonological_gap",
        BACKEND / "scripts" / "phase58_phonological_gap.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.is_valid_dravidian_initial


VALID_INITIAL = _phase58_validator()


# ── Syllable canon ─────────────────────────────────────────────

@pytest.mark.parametrize("s,expected", [
    ("kaḷiṟu", ["ka", "ḷi", "ṟu"]),
    ("kur", ["kur"]),
    ("nal", ["nal"]),
    ("kō", ["kō"]),
    ("kai", ["kai"]),          # diphthong nucleus
    ("ay", ["ay"]),            # VC syllable
    ("ā", ["ā"]),
    ("kanal", ["ka", "nal"]),
    ("tiru", ["ti", "ru"]),
])
def test_syllabify_legal(s, expected):
    assert syllabify(s) == expected
    assert canon_legal(s)


@pytest.mark.parametrize("s", [
    "strī",     # initial cluster
    "kra",      # initial cluster
    "alk",      # final cluster
    "kantr",    # final cluster after coda
    "aṅkr",     # cluster across the string
    "",         # empty
    "kx",       # unknown character / no nucleus
])
def test_syllabify_illegal(s):
    assert syllabify(s) is None
    assert not canon_legal(s)


# ── Normalization / profiles ───────────────────────────────────

def test_normalize_reading():
    assert normalize_reading("ay/ā") == "ay"
    assert normalize_reading("An/aṇ") == "an"
    assert normalize_reading("kaḷiṟu") == "kaḷiṟu"
    assert normalize_reading("") == ""


def test_positional_counts_convention():
    ins = [["A", "B"], ["A", "C", "B"], ["A"]]
    # A: initial twice (n>1), medial once (sole token)
    assert positional_counts(ins, "A") == (2, 1, 0)
    # B: terminal twice
    assert positional_counts(ins, "B") == (0, 0, 2)
    # C: medial once
    assert positional_counts(ins, "C") == (0, 1, 0)


def test_modal_and_tv():
    assert modal_class((0.5, 0.5, 0.0)) == "INITIAL"   # tie -> I
    assert modal_class((0.0, 0.5, 0.5)) == "TERMINAL"  # tie -> T over M
    assert modal_class((0.2, 0.3, 0.5)) == "TERMINAL"
    assert tv_distance((1.0, 0.0, 0.0), (0.5, 0.5, 0.0)) == 0.5


# ── Decision rule truth table ──────────────────────────────────

@pytest.mark.parametrize("states,outcome", [
    ({"t1": PASS, "t2": PASS, "t3": PASS}, "VALIDATED_NON_SA"),
    ({"t1": FAIL, "t2": PASS, "t3": PASS}, "DEMOTE"),
    ({"t1": PASS, "t2": FAIL, "t3": NOT_ATTESTED}, "DEMOTE"),
    ({"t1": NOT_ATTESTED, "t2": PASS, "t3": PASS}, "UNRESOLVED"),
    ({"t1": PASS, "t2": INDETERMINATE, "t3": PASS}, "UNRESOLVED"),
    ({"t1": NOT_ATTESTED, "t2": INDETERMINATE, "t3": INDETERMINATE},
     "UNRESOLVED"),
])
def test_decide(states, outcome):
    assert decide(states) == outcome


# ── Toy end-to-end ─────────────────────────────────────────────

def _toy():
    """Core: A 'ka' (initial), B 'nal' (terminal), C 'ay' (medial).
    Candidate X 'ka' behaves like a core sign; Y 'kur' is frequent
    but distributionally isolated; W 'ka' is barely attested."""
    holdat = ([["A", "B"]] * 10 + [["A", "C", "B"]] * 10
              + [["X", "B"]] * 12 + [["A", "X", "B"]] * 4
              + [["X", "C", "B"]] * 4
              + [["Y", "Q"]] * 10 + [["W", "B"]] * 2)
    icit = ([["A", "B"]] * 6 + [["X", "B"]] * 4 + [["X", "C", "B"]] * 2)
    readings = {"A": "ka", "B": "nal", "C": "ay"}
    core = {"A", "B", "C"}
    grammar = CoreGrammar(core, readings, CorpusContext(holdat))
    return (CorpusContext(holdat), CorpusContext(icit), grammar,
            readings)


def test_toy_core_consistent_anchor_validates():
    h, i, g, readings = _toy()
    r = evaluate_anchor("X", "ka", g, readings, h, i, VALID_INITIAL)
    assert r["t1"]["state"] == PASS
    assert r["t2"]["state"] == PASS
    assert r["t3"]["state"] == PASS
    assert r["outcome"] == "VALIDATED_NON_SA"


def test_toy_isolated_anchor_demotes():
    h, i, g, readings = _toy()
    r = evaluate_anchor("Y", "kur", g, readings, h, i, VALID_INITIAL)
    assert r["t3"]["state"] == FAIL       # zero strict-core partners
    assert r["outcome"] == "DEMOTE"


def test_toy_unattested_anchor_unresolved():
    h, i, g, readings = _toy()
    r = evaluate_anchor("W", "ka", g, readings, h, i, VALID_INITIAL)
    assert r["t1"]["state"] == NOT_ATTESTED
    assert r["t2"]["state"] == INDETERMINATE
    assert r["outcome"] == "UNRESOLVED"


# ── Real set recomputation (spec 011 section 2) ────────────────

def test_real_sets():
    anchors = json.loads(
        (BACKEND / "reports" / "INDUS_FINAL_ANCHORS.json")
        .read_text("utf-8"))["anchors"]
    register = json.loads(
        (REPO / "reports" / "phase108_provenance_register.json")
        .read_text("utf-8"))
    sets = compute_sets(anchors, register)
    assert len(sets["flagged44"]) == 44
    assert len(sets["strict94"]) == 94
    assert len(sets["kur113"]) == 113
    assert "M293" in sets["flagged44"]
    assert anchors["M293"]["confidence"] == "MEDIUM"


# ── H23 registration ───────────────────────────────────────────

def test_graph_registration():
    from glossa_lab.experiment_graph import ATOMIC_NODES
    assert "IndusPhase113NonSaValidation" in ATOMIC_NODES
