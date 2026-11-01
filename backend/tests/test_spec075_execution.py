"""Tests for the Spec 075 execution records.

Phase-441 (the depicted-kind endings atlas) executed
under the frozen contract: all six step-0 gates
passed, the primary population reproduced exactly
(3,045 / 557 / 550) and keyed in full under the
two-leg route (token 999 the named exclusion), the
census was published before any rate with no kind
TOO THIN, and the frozen section 5 battery scored
per kind — other INCONCLUSIVE, human NOT SUPPORTED,
animal NOT SUPPORTED, object_goods NOT SUPPORTED —
with all three sensitivities agreeing in every word
and no verdict grade-sensitive. These tests pin the
recorded facts: a gate verdict, a count, a ratio, or
an append that drifts from the executed run fails
here.

Author: Spec 075 (Phase-441), 2026-10-25.
"""
from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
RESULTS = REPO_ROOT / "reports/phase441_results.json"
SPEC_DIR = REPO_ROOT / "specs/075-depicted-kind-endings-atlas"
FREEZE_DIGEST = (
    "aa06726f545218c5bcee4b3a5df94c920828fead4e06e2ccec1eeffce44ac5cf"
)
RESULTS_SHA256 = (
    "f55ae91124e1ac74268f79035d862586a81a2f2e9596fd2318f3741c6e39ea29"
)
KEYING_PUBLICATION_SHA256 = (
    "0a732022828db1bf"
)
VERDICTS = {
    "other": "INCONCLUSIVE",
    "human": "NOT SUPPORTED",
    "animal": "NOT SUPPORTED",
    "object_goods": "NOT SUPPORTED",
}
CENSUS_CLASSES = {
    "other": (307, 7006),
    "human": (53, 978),
    "animal": (39, 1179),
    "object_goods": (24, 2159),
}
TABLES = {
    "other": [[2032, 4974], [807, 2197]],
    "human": [[247, 731], [1778, 3703]],
    "animal": [[327, 852], [2128, 4710]],
    "object_goods": [[249, 1910], [2606, 6557]],
}
RATIOS = {
    "other": 1.0796, "human": 0.7785,
    "animal": 0.8912, "object_goods": 0.4055,
}


def _results() -> dict:
    return json.loads(RESULTS.read_text("utf-8"))


def test_phase441_results_record_complete():
    r = _results()
    assert r["spec"] == "075"
    assert r["phase"] == 441
    assert r["outcome"] == "PER-KIND VERDICTS"
    assert r["contract"]["freeze_digest"] == FREEZE_DIGEST
    assert r["contract"]["osf_registration"] == "jv74f"
    assert r["contract"]["osf_doi"] == "10.17605/OSF.IO/JV74F"
    assert r["verdicts"] == VERDICTS
    assert r["anchors"]["byte_identical"] is True
    assert r["keying_publication_sha256"].startswith(
        KEYING_PUBLICATION_SHA256)


def test_phase441_gates_all_pass_in_order():
    r = _results()
    assert [g["gate"] for g in r["gates"]] == [
        "0.1", "0.2", "0.3", "0.4", "0.5", "0.6"]
    assert all(g["result"] == "PASS" for g in r["gates"])
    readings = r["gate_0_6_readings"]
    assert readings["freeze_digest_recomputed"] == FREEZE_DIGEST
    assert readings["freeze_pr"]["state"] == "closed"
    assert readings["freeze_pr"]["merge_commit_sha"].startswith(
        "fd9bd448")
    assert readings["osf_registration"]["public"] is True
    assert readings["osf_registration"][
        "pending_registration_approval"] is False
    assert readings["osf_registration"][
        "reviews_state"] == "accepted"


def test_phase441_census_pinned():
    c = _results()["census"]
    assert c["population"] == {
        "analyzable_rows": 3045, "distinct_signs": 557,
        "signs_in_sequences_ge2": 550}
    for kind, (signs, occ) in CENSUS_CLASSES.items():
        assert c["classes"][kind]["member_signs"] == signs
        assert c["classes"][kind]["pooled_occurrences"] == occ
        assert c["floors"][kind]["too_thin"] is False
    assert c["unidentified"] == {"signs": 133, "pooled_occurrences": 481}
    assert c["token_999"] == {"primary_rows": 2, "occurrences": 2}
    cw = c["corpus_wide_final_position_rate"]
    assert cw["final_occurrences"] == 3045
    assert cw["total_occurrences"] == 11805
    named = {(e["sign"], e["sign_key"]) for e in
             c["borderline_signs_named_for_S1"]}
    assert named == {("255", "P073"), ("256", "P074"),
                     ("520", "P217"), ("716", "P320"),
                     ("717", "P320")}


def test_phase441_primary_quantities_pinned():
    r = _results()
    for kind, table in TABLES.items():
        b = r["primary"]["kinds"][kind]
        assert b["table_2x2"] == table
        assert b["verdict"] == VERDICTS[kind]
        assert abs(b["enrichment_ratio"] - RATIOS[kind]) < 1.5e-4
        assert len(b["per_sign_table"]) == b["member_signs"]
        # The per-sign table recomputes the pooled cells.
        assert sum(s["total_occurrences"]
                   for s in b["per_sign_table"]) == \
            b["pooled_occurrences"]
        assert sum(s["final_occurrences"]
                   for s in b["per_sign_table"]) == \
            b["pooled_final_occurrences"]
    other = r["primary"]["kinds"]["other"]
    assert abs(other["fisher_p_two_sided"] - 0.0294888) < 1e-6
    assert other["half_occurrences_condition"]["met"] is False


def test_phase441_sensitivities_agree():
    r = _results()
    s1 = r["sensitivities"]["S1"]
    s2 = r["sensitivities"]["S2"]
    s3 = r["sensitivities"]["S3"]
    for arm in (s1, s2, s3):
        assert {k: arm["kinds"][k]["verdict"] for k in VERDICTS} \
            == VERDICTS
    assert s2["equals_primary"] is True
    assert s2["included_signs_named"] == []
    assert s3["population_figures"] == {
        "analyzable_rows": 5131, "distinct_signs": 707}
    assert s3["unkeyable_signs_named"] == []
    assert all(not g["grade_sensitive"]
               for g in r["grade_sensitivity"].values())


def test_phase441_claim_appends_recorded():
    appends = _results()["claim_family_appends"]
    assert appends["append_key"] == "spec075_outcome_append_2026_10_25"
    assert set(appends["appends"]) == {
        "F075-C03", "F075-C05", "F075-C06",
        "F075-C07", "F075-C08", "F075-C11"}
    assert "in question" in appends["appends"]["F075-C03"]
    assert "no pooled depicted-kinds verdict" in \
        appends["appends"]["F075-C11"]


def test_records_on_disk_carry_the_outcome():
    outcome_md = (SPEC_DIR / "outcome.md").read_text("utf-8")
    step0_md = (SPEC_DIR / "step0-record.md").read_text("utf-8")
    report = (REPO_ROOT / "reports/phase441_report.md").read_text(
        "utf-8")
    for text in (outcome_md, report):
        for kind, word in VERDICTS.items():
            assert f"{kind} {word}" in text or \
                f"{kind}: {word}" in text or \
                f"Kind {kind}: {word}" in text
        assert FREEZE_DIGEST in text
        assert "jv74f" in text
        assert RESULTS_SHA256 in text
        assert ("This corpus is an ICIT-lineage corpus. Agreement "
                "between it and the program's earlier ICIT-lineage "
                "layer is consistency within one tradition, not "
                "independent corroboration.") in text
        assert "celestial class as frozen in Asset A v2 contains " \
            "zero signs" in text
        assert "49%" in text
    for gate in ("0.1", "0.2", "0.3", "0.4", "0.5", "0.6"):
        assert f"Gate {gate}" in step0_md
    ledger = (REPO_ROOT / "LEDGER.md").read_text("utf-8")
    assert "Spec 075 EXECUTED (Phase-441)" in ledger
    graph = (REPO_ROOT / "backend/glossa_lab"
             / "experiment_graph_phase441.py").read_text("utf-8")
    assert "IndusPhase441DepictedKindEndingsAtlas" in graph
    registry = (REPO_ROOT / "backend/glossa_lab"
                / "experiment_graph.py").read_text("utf-8")
    assert "_phase441_node_defs" in registry
