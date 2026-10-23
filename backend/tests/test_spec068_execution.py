"""Spec 068 execution tests (Phase-430).

The execution's terminal outcome is COMPARISON
UNINFORMATIVE: all seven step-0 gates passed, no
non-linguistic control fitted as well as the
Indus primary (the falsifier did not fire), but
the linguistic positive control, Linear B, did
not fit strictly better than every
non-linguistic control — it fitted worst of all
five systems (NRMSE_log 0.9229) — so under the
frozen section 5.5 mapping the comparison
cannot judge the script and the claim stands
exactly as recorded with no strength label
added. These tests pin the delivered form: the
step-0 gate verdicts in frozen order, the
census and populations, the frozen control
tables as entered, the fits and the comparison
arithmetic, the sensitivity and subsampling
records, the estimator cross-check against
Phase-413's implementation of record, and the
anchors assertion.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SPEC_DIR = REPO / "specs/068-yadav-zipf-controls-successor"
RESULTS = REPO / "reports/phase430_results.json"
DATA = SPEC_DIR / "data"

TABLE_HASHES = {
    "n1_mesopotamian_numerical_signs.csv":
        "0f938c191db274985a9332a6f2fd64e6e7a59431d36d122cc83ddd70cc9f0b62",
    "n2_dering_charges.csv":
        "0c618df48e88b54bacd2dcff74f75033852da03396321d4f1b4394f7d4caf269",
    "n2_dering_blazons.csv":
        "c40dc7aa01a6a2274d3b38843382df62aa74802d7324c062e7caae44c89fa520",
    "n2_dering_extraction.csv":
        "c9244160e15d3d7ce71d901f0854cd2c3fb2f8c2ebca0253583640136e0721f1",
    "p1_linearb_syllabograms.csv":
        "895a1ebf60c87d7feaf17933c94e65b4b6d5f6b39dbb73c32208e8ea98a0255b",
}


def _results() -> dict:
    return json.loads(RESULTS.read_text(encoding="utf-8"))


def test_step0_gates_passed_in_frozen_order():
    r = _results()
    gates = r["gates"]
    assert [g["gate"] for g in gates] == [
        "0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7"]
    assert all(g["verdict"] == "PASS" for g in gates)
    # Gate 0.1: every pin matched, the intake stands.
    g1 = gates[0]
    assert all(p["match"] for p in g1["inputs"])
    assert g1["freeze068_digest"]["match"] is True
    assert g1["spec053_freeze_digest"]["match"] is True
    assert g1["intake_record_stands"] is True
    assert g1["anchors_census"] == {
        "anchors": 287, "strict_sa_independent": 94}
    # Gate 0.2: the self-test recovered its planted
    # parameters within the frozen tolerances.
    st = r["estimator_self_test"]
    assert st["recovered_within_tolerance"] is True
    assert st["fit"]["alpha"] == 1.256
    assert st["fit"]["q"] == 2.72
    # Gate 0.5: the population act states limb B.
    assert gates[4]["limb"] == "B"
    assert "full ICIT sign inventory" in gates[4]["statement"]


def test_census_and_populations():
    r = _results()
    census = r["census"]
    assert r["gates"][3]["audit_census_match"] is True
    audit = census["audit_census_recomputed"]
    assert audit["rows"] == 5704
    assert audit["analyzable"] == 5536
    assert audit["grades"] == {
        "documented-lineage": 3212,
        "undocumented-corroborated": 2087,
        "undocumented-uncorroborated": 405}
    assert audit["tokens"] == 18065
    assert audit["distinct_signs"] == 713
    assert audit["sites"] == 77
    pops = r["populations"]
    assert pops["primary"]["analyzable_rows"] == 3045
    assert pops["primary"]["tokens"] == 11805
    assert pops["primary"]["distinct_signs"] == 557
    assert pops["sensitivity"]["analyzable_rows"] == 5131
    assert pops["sensitivity"]["tokens"] == 17216
    assert pops["sensitivity"]["distinct_signs"] == 707
    # Floors (gate 0.7) were met by wide margins.
    g7 = r["gates"][6]
    assert g7["primary_types"] == 557
    assert g7["primary_tokens"] == 11805


def test_control_tables_as_entered():
    r = _results()
    cs = r["control_set"]
    assert cs["N1"]["types"] == 12
    assert cs["N1"]["tokens"] == 1981
    assert cs["N2"]["types"] == 57
    assert cs["N2"]["tokens"] == 825
    assert cs["P1"]["types"] == 89
    assert cs["P1"]["tokens"] == 47292
    for name, digest_expected in TABLE_HASHES.items():
        digest = hashlib.sha256(
            (DATA / name).read_bytes()).hexdigest()
        assert digest == digest_expected, name
    assert cs["N1"]["table_sha256"] == (
        TABLE_HASHES["n1_mesopotamian_numerical_signs.csv"])
    assert cs["N2"]["table_sha256"] == (
        TABLE_HASHES["n2_dering_charges.csv"])
    assert cs["P1"]["table_sha256"] == (
        TABLE_HASHES["p1_linearb_syllabograms.csv"])


def test_fits_and_comparison_arithmetic():
    r = _results()
    fits = r["fits"]
    primary = fits["indus_primary"]
    assert (primary["V"], primary["N"]) == (557, 11805)
    assert primary["alpha"] == 2.004
    assert abs(primary["NRMSE_log"] - 0.1584) < 0.0001
    assert abs(fits["N1"]["NRMSE_log"] - 0.5335) < 0.0001
    assert abs(fits["N2"]["NRMSE_log"] - 0.1839) < 0.0001
    assert abs(fits["P1"]["NRMSE_log"] - 0.9229) < 0.0001
    assert abs(fits["N3_median"]["NRMSE_log"] - 0.2405) < 0.0001
    assert len(fits["N3_replicates"]) == 99
    comp = r["comparison"]["primary"]
    # The falsifier did not fire; no NEAR MISS is named
    # (the closest gap, N2 at +0.0255, is above the
    # frozen 0.02 band).
    assert comp["as_well"] == {"N1": False, "N2": False,
                               "N3": False}
    assert comp["falsifier_fires"] is False
    assert comp["near_miss"] == []
    assert abs(comp["gaps"]["N2"] - 0.0255) < 0.0001
    # The positive-control condition failed, which is
    # what assigns the headline.
    assert comp["positive_control_passes"] is False
    assert r["comparison"]["n3_as_well_share"] == 0.0
    assert r["outcome"] == "COMPARISON UNINFORMATIVE"
    assert "no strength label added" in r["headline_wording"]
    assert r["headline_wording"].startswith(
        "This corpus is an ICIT-lineage corpus.")


def test_sensitivity_subsampling_and_integrity():
    r = _results()
    sens = r["sensitivity"]
    assert sens["fit"]["V"] == 707
    assert abs(sens["fit"]["NRMSE_log"] - 0.1544) < 0.0001
    assert sens["comparison"]["as_well"] == {
        "N1": False, "N2": False, "N3": False}
    assert sens["grade_sensitive"] is False
    assert r["grade_sensitive"] is False
    sub = r["subsampling"]
    assert sub["primary"]["half"]["inscriptions_per_replicate"] == 1522
    assert sub["primary"]["quarter"]["inscriptions_per_replicate"] == 761
    assert abs(sub["primary"]["half"]["nrmse_median"] - 0.1739) < 0.0001
    # The estimator cross-check against Phase-413's
    # implementation of record agreed on every system.
    xc = r["estimator_cross_check"]
    assert xc["systems_checked"] == 5
    assert xc["all_agree"] is True
    assert r["anchors"]["byte_identical"] is True
    assert r["anchors"]["sha256_before"] == (
        "df0cf620a0d66b71d778300b93a91d96b2f30f23580088e608659"
        "2b32d34f569")
    assert "neither confirms nor corrects" in r["fence"]
