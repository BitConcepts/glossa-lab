"""Phase-395 (Spec 031) build-machinery fences.

Pins: (1) the Stage 0 gazetteer screens reproduce the frozen
record exactly (30 program sites; 21 with defensible
coordinates; ZERO period-eligible under the literal frozen
test of Spec 031 section 6 / F031-C10 — the only published
labels in the gazetteer are the three Central Asian
PN/Neo. labels); (2) link construction counts only
named-source determinations from audit-named instrumental
studies, never proxy-group assignments, and never resolves
an uncertain pair; (3) the margins closures fire exactly as
sections 4.2/4.3 prescribe (bead/craft NOT-YET-TESTABLE,
ceramic NOT ESTIMABLE), and do not fire on a viable
fixture; (4) the section 5 machinery (MRM partial R^2,
MRQAP-DSP permutation, jackknife estimability, verdict
rules) behaves on synthetic populations with known
structure — the pipeline that a viable arm would run.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = REPO / "backend" / "scripts"
sys.path.insert(0, str(REPO / "backend"))


def _load(name: str):
    spec = importlib.util.spec_from_file_location(
        name, SCRIPTS / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


p395 = _load("phase395_q7_execution")


def _gazetteer_rows() -> list[dict]:
    path = REPO / "data" / "movement" / "gazetteer_rows.jsonl"
    return [json.loads(line) for line in
            path.read_text(encoding="utf-8").splitlines()
            if line.strip()]


COORD_SITES = {
    "banawali", "chagylly", "harappa", "hiregudda",
    "islam chowki", "joenniemi", "kanispur", "khirsara",
    "kunal", "mullali", "ojiyana", "piklihal", "qasim bagh",
    "sannarachamma",
    "shahr i sokhta", "sheri khan tarakai",
    "sheri khan tarakai 3", "sheri khan tarakai 4",
    "ter kala dheri", "tigrana", "yalangach",
}


def test_gazetteer_screens_reproduce_stage0_record():
    screens = p395.gazetteer_screens(_gazetteer_rows())
    assert len(screens) == 30
    coord = {s for s, v in screens.items() if v["has_coordinates"]}
    assert coord == COORD_SITES
    period = {s for s, v in screens.items()
              if v["period_eligible"]}
    assert period == set()
    labelled = {s: v["period_labels"] for s, v in screens.items()
                if v["period_labels"]}
    assert labelled == {
        "chagylly": ["PN", "Neo."],
        "mullali": ["PN", "Neo.?"],
        "yalangach": ["PN", "Neo.?"],
    }


def test_period_test_is_literal():
    f = p395.indicates_mature_harappan
    assert f(None) is False
    assert f([]) is False
    assert f(["PN", "Neo."]) is False
    assert f("Early Harappan") is False
    assert f("Mature Harappan") is True
    assert f(["Period 3 (Mature Harappan)"]) is True


def _law_fixture() -> dict:
    return {"studies": [
        {"material": "agate", "chapter": 8, "method": "INAA",
         "tier": "primary",
         "sites": {
             "alpha": {"total": 10, "proxy_group": 3,
                       "named_source_total": 7},
             "beta": {"total": 4, "proxy_group": 2,
                      "named_source_total": 2},
             "gamma": {"total": 5, "proxy_group": 0,
                       "named_source_total": 5}},
         "certain_source_holders": {
             "Source A": ["alpha", "gamma"],
             "Source B": ["beta"]},
         "uncertain_pairs": [["beta", "gamma"]]},
        {"material": "alabaster", "chapter": 10,
         "method": "Sr/S isotopes", "tier": "primary",
         "counted_named_source_determinations": {"beta": 2}},
        {"material": "chert", "chapter": 6, "method": "visual",
         "tier": "excluded",
         "sites": {"delta": {"named_source_total": 99}}},
    ]}


def test_link_construction_counts_only_named_primary():
    links = p395.build_links(_law_fixture())
    # Proxy-group assignments never count: alpha has 7 named
    # of 10 total; the excluded chert study contributes
    # nothing (delta absent).
    assert links["named_source_totals"] == {
        "alpha": 7, "beta": 4, "gamma": 5}
    assert "delta" not in links["named_source_totals"]
    # Floor DD-1: >= 3 named-source determinations.
    assert links["link_eligible_sites"] == [
        "alpha", "beta", "gamma"]
    # Certain pairs only, from shared named sources among
    # eligible sites; beta-gamma rests on Source B alone
    # (single holder) so no pair; the flagged uncertain
    # pair is reported, never counted.
    assert links["linked_pairs_certain"] == [("alpha", "gamma")]
    assert links["linked_pairs_uncertain"] == [["beta", "gamma"]]


def _screens_fixture(period: bool) -> dict:
    return {
        f"site{i}": {
            "rows": 1, "gazetteer_row_ids": [f"G{i}"],
            "coordinate_states": ["exact_published"],
            "has_coordinates": True,
            "period_labels": ["Mature Harappan"] if period
            else [],
            "period_eligible": period,
            "row_counts_by_source": {},
        } for i in range(10)}


def test_margins_closures_fire_on_empty_period_screen():
    links = {"linked_pairs_certain": [], "link_eligible_sites": []}
    bead = p395.arm_margins("bead_craft", _screens_fixture(False),
                            links, set())
    ceramic = p395.arm_margins("ceramic", _screens_fixture(False),
                               links, set())
    assert bead["viable"] is False
    assert bead["closure"]["status"] == "NOT-YET-TESTABLE"
    assert ceramic["viable"] is False
    assert ceramic["closure"]["status"] == "NOT ESTIMABLE"


def test_margins_viable_fixture_does_not_close():
    screens = _screens_fixture(True)
    sites = sorted(screens)
    pairs = [(sites[i], sites[j]) for i in range(10)
             for j in range(i + 1, 10)][:12]
    links = {"linked_pairs_certain": pairs,
             "link_eligible_sites": sites}
    bead = p395.arm_margins("bead_craft", screens, links,
                            set(sites))
    assert bead["eligible_count"] == 10
    assert bead["linked_pairs_among_eligible"] == 12
    assert bead["viable"] is True
    assert bead["closure"] is None


def _synthetic(plant: float, n: int = 12, seed: int = 7):
    rng = np.random.default_rng(seed)
    coords = rng.uniform(0, 500, size=(n, 2))
    geo = np.sqrt(((coords[:, None, :] - coords[None, :, :])
                   ** 2).sum(-1))
    river = geo * rng.uniform(0.8, 1.4, size=(n, n))
    river = (river + river.T) / 2
    np.fill_diagonal(river, 0)
    shared = np.zeros((n, n))
    for a in range(0, n - 1, 2):
        shared[a, a + 1] = shared[a + 1, a] = 1.0
    base = 0.6 - 0.0006 * geo + rng.normal(0, 0.05, (n, n))
    sim = base + plant * shared
    sim = (sim + sim.T) / 2
    np.fill_diagonal(sim, 1.0)
    return sim, shared, geo, river, []


def test_mrm_partial_r2_detects_planted_structure():
    sim, shared, geo, river, covars = _synthetic(plant=0.25)
    r2 = p395.mrm_partial_r2(sim, shared, geo, river, covars)
    assert r2 > p395.MARGIN
    sim0, shared0, geo0, river0, _ = _synthetic(plant=0.0)
    r20 = p395.mrm_partial_r2(sim0, shared0, geo0, river0, [])
    assert r20 < r2


def test_mrqap_dsp_permutation():
    rng = np.random.default_rng(1)
    sim, shared, geo, river, covars = _synthetic(plant=0.35)
    p = p395.mrqap_pvalue(sim, shared, geo, river, covars,
                          199, rng)
    assert p <= 0.05


def test_loso_estimability_rule():
    sim, shared, geo, river, covars = _synthetic(plant=0.2)
    sites = [f"s{i}" for i in range(sim.shape[0])]
    cells = p395.loso_cells(sim, shared, geo, river, covars,
                            sites)
    assert len(cells) == 12
    # 6 disjoint linked pairs: dropping any site leaves 5
    # linked pairs < 10, so NO cell is estimable — the frozen
    # jackknife clause in action.
    assert all(c["estimable"] is False for c in cells)
    assert all(c["partial_r2"] is None for c in cells)


def test_verdict_rules_section_5_2():
    v = p395.verdict_from_rules
    good_cells = [{"estimable": True, "partial_r2": 0.05}]
    assert v(True, 0.01, [0.03, 0.09], good_cells, True) \
        == "SUPPORTED"
    assert v(True, 0.40, [0.03, 0.09], good_cells, True) \
        == "CONTRADICTED"
    assert v(True, 0.01, [0.0, 0.015], good_cells, True) \
        == "CONTRADICTED"
    assert v(True, 0.01, [0.03, 0.09],
             [{"estimable": False, "partial_r2": None}],
             True) == "INCONCLUSIVE"
    assert v(False, 0.01, [0.03, 0.09], good_cells, True) \
        == "INVALID"
    assert v(True, 0.01, [0.03, 0.09], good_cells, False) \
        == "INVALID"


def test_controls_machinery_runs_and_is_conservative():
    rng = np.random.default_rng(3)
    sim, shared, geo, river, covars = _synthetic(plant=0.3)
    sites = [f"s{i}" for i in range(sim.shape[0])]
    out = p395.run_controls(sim, shared, geo, river, covars,
                            sites, b_perm=49, b_boot=49,
                            r_reps=9, rng=rng)
    assert out["replicates"] == 9
    assert 0 <= out["negative_supported_fires"] <= 9
    assert 0 <= out["positive_supported_fires"] <= 9
    # With this fixture's sparse link structure no LOSO cell
    # is estimable, so the SUPPORTED rule can never fire in
    # either control — the machinery reports that honestly.
    assert out["negative_supported_fires"] == 0
    assert out["positive_supported_fires"] == 0


def test_frozen_constants():
    assert p395.SEED == 20261013
    assert p395.MARGIN == 0.02
    assert p395.B_PERM == 9999 and p395.B_BOOT == 9999
    assert p395.R_CONTROLS == 199
    assert p395.MIN_ELIGIBLE_SITES == 8
    assert p395.MIN_LINKED_PAIRS == 10
    assert p395.SITE_LINK_FLOOR == 3
    assert p395.BEAD_FLOOR == 10 and p395.CERAMIC_FLOOR == 20
