"""Tests for the Spec 074 execution records.

Phase-440 (Hunt's opening signs on the repaired
keying surface) executed under the frozen
contract: all six step-0 gates passed, gate 0.4's
reproduction assertion held exactly against Spec
070's recorded measurement, the 31-sign population
keyed 31/31 under the frozen two-leg route, and the
frozen section 4 test scored NOT SUPPORTED under
section 4.3 rule 1. The outcome was appended as a
dated entry to the claim's record. These tests pin
the recorded facts: a gate verdict, a count, or an
append that drifts from the executed run fails here.

Author: Spec 074 (Phase-440), 2026-10-24.
"""
from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
RESULTS = REPO_ROOT / "reports/phase440_results.json"
SPEC_DIR = REPO_ROOT / "specs/074-hunt-opening-signs-repaired-surface"
STORE = (REPO_ROOT / "glossa-indus/claims/extracted_claims/"
         "without_kings_or_conquests_the_indus_scr_ce9d98cc.json")
CLAIM_ID = "without_kings_or_conquests_the_indus_scr_ce9d98cc_manual_003"
APPEND_KEY = "spec074_outcome_append_2026_10_24"
FREEZE_DIGEST = (
    "5416a0d331e76fcec720746849969f2e86e9d79f2cc0fa583e1050662ffba36c"
)
PUBLICATION_SHA = (
    "30092b6fd64f221ee0808addeedd11e1e800cf3d79716ba26b3fb971f396a93b"
)
ASSET_A_V2_SHA = (
    "681e017da8b3f93aeade7e85361565fa8f3f4178b167dfa2448f5b4c239a8193"
)
FALSIFIER = (
    "Faunal signs not enriched in initial position above random baseline."
)


def _results() -> dict:
    return json.loads(RESULTS.read_text("utf-8"))


def _claim() -> dict:
    d = json.loads(STORE.read_text("utf-8"))
    for c in d["claims"]:
        if c["claim_id"] == CLAIM_ID:
            return c
    raise AssertionError("manual_003 not in the store")


def test_phase440_results_record_complete():
    r = _results()
    assert r["spec"] == "074"
    assert r["phase"] == 440
    assert r["outcome"] == "NOT SUPPORTED"
    assert r["claim_id"] == CLAIM_ID
    c = r["contract"]
    assert c["freeze_digest"] == FREEZE_DIGEST
    assert c["osf_registration"] == "cfe7z"
    assert c["spec070_freeze_digest"] == (
        "763108f89311ab2791827b347a155a8b4f9abad940ab59f921af129f79c73e3e"
    )
    assert c["asset_a_v2_sha256"] == ASSET_A_V2_SHA


def test_gates_in_frozen_order_all_pass():
    r = _results()
    assert [g["gate"] for g in r["gates"]] == [
        "0.1", "0.2", "0.3", "0.4", "0.5", "0.6"]
    assert all(g["result"] == "PASS" for g in r["gates"])


def test_gate_0_4_reproduction_is_exact():
    r = _results()
    rep = r["gate_0_4_reproduction"]
    assert rep["recorded_publication_sha256"] == PUBLICATION_SHA
    assert rep["executed_publication_sha256"] == PUBLICATION_SHA
    assert rep["enumeration_equal"] is True
    assert rep["census_equal"] is True
    assert r["gate_0_4_population_publication_sha256"] == PUBLICATION_SHA
    census = r["population"]["battery_class_counts_primary"]
    assert census == {
        "TERMINAL_STRONG": 42, "MEDIAL_STRONG": 81,
        "TERMINAL_MODERATE": 37, "INITIAL_MODERATE": 6,
        "MIXED": 23, "INITIAL_STRONG": 31,
    }
    enum = r["population"]["O_enumeration_wells_space"]
    assert len(enum) == 31
    by_code = {e["wells_code"]: e for e in enum}
    # Spot pins from Spec 070's recorded measurement.
    assert (by_code["740"]["I"], by_code["740"]["M"],
            by_code["740"]["T"]) == (919, 377, 3)
    assert (by_code["090"]["I"], by_code["090"]["M"],
            by_code["090"]["T"]) == (87, 15, 8)
    assert (by_code["617"]["I"], by_code["617"]["M"],
            by_code["617"]["T"]) == (36, 8, 12)


def test_keying_two_leg_route_and_the_five():
    r = _results()
    keyed = r["keyed_population"]
    assert len(keyed) == 31
    leg2 = {e["wells_code"]: e for e in keyed
            if e["keying_leg"] == "leg2_icit_wells"}
    assert sorted(leg2) == ["136", "298", "401", "617", "824"]
    for code, e in leg2.items():
        assert e["sign_key"] == "W" + code
        assert e["depicted_kind"] == "unidentified"
    leg1 = [e for e in keyed if e["keying_leg"] == "leg1_parpola_1982"]
    assert len(leg1) == 26
    animals = sorted(e["wells_code"] for e in keyed
                     if e["depicted_kind"] == "animal")
    assert animals == ["226", "241"]


def test_primary_quantities_pinned():
    p = _results()["primary"]
    assert p["O_size"] == 31 and p["U_size"] == 76
    assert p["O_animal"] == 2 and p["O_non_animal"] == 24
    assert p["O_contested"] == 0 and p["O_unidentified"] == 5
    assert p["U_contested"] == 0 and p["U_unidentified"] == 3
    assert p["table_R1"] == [[2, 24], [6, 58]]
    assert p["animal_share_O"] == 0.07692307692307693
    assert p["animal_share_U"] == 0.08888888888888889
    assert p["R1"] == 0.8653846153846154
    assert p["p_one_sided"] == 0.7345333427543884
    assert p["p_two_sided"] == 1.0
    assert p["table_R2"] == [[0, 6], [9, 58]]
    assert p["R2"] == 0.0
    assert p["R2_p_one_sided"] == 1.0
    # Precedence rule 1 fires on both grounds independently.
    assert p["R1"] <= 1.0 and p["p_one_sided"] >= 0.05


def test_sensitivities_recorded():
    r = _results()
    sa = r["primary"]["S_A"]
    assert sa["table_R1"] == [[2, 24], [6, 58]]
    assert sa["R1"] == r["primary"]["R1"]
    assert r["S_B_quantities"] is None
    assert "not applicable" in r["gate_0_5"]["S_B"]
    sc = r["S_C"]
    assert sc["O_size"] == 35 and sc["U_size"] == 89
    assert sc["unkeyable_signs_named"] == []
    assert sc["verdict_under_same_precedence"] == "NOT SUPPORTED"
    assert sc["grade_sensitive"] is False
    q = sc["quantities"]
    assert q["table_R1"] == [[2, 26], [6, 66]]
    assert q["R1"] == 0.8928571428571428
    assert q["p_one_sided"] == 0.7140271361703511


def test_headline_wording_is_the_frozen_form():
    r = _results()
    h = r["headline_wording"]
    assert "2 are animal signs" in h
    assert "0.0769" in h and "0.0889" in h
    assert "0.8654" in h and "0.7345" in h
    assert ASSET_A_V2_SHA in h
    assert "not supported in its re-scoped form" in h
    assert "stands on its positional half alone" in h
    assert h in r["outcome_append_text"]


def test_anchors_byte_identical_after_run():
    r = _results()
    assert r["anchors"]["byte_identical"] is True
    assert r["anchors"]["before"] == (
        "df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569"
    )
    assert r["anchors"]["after"] == r["anchors"]["before"]


def test_outcome_appended_to_the_claim_record():
    r = _results()
    c = _claim()
    entry = c.get(APPEND_KEY)
    assert entry is not None
    assert entry["note"] == r["outcome_append_text"]
    assert entry["outcome"] == "NOT SUPPORTED"
    assert entry["date"] == "2026-10-24"
    assert entry["phase"] == 440
    assert entry["spec"] == "074"
    # The append moves nothing else on the record.
    assert c["falsification_condition"] == FALSIFIER
    assert c["claim_status"] == "partially_supported"
    assert c["stage"] == "explained"


def test_regeneration_preserves_the_outcome_append(tmp_path):
    """The extracted-claims generator regenerates the store
    wholesale; the dated outcome append is a record, not
    extraction output, and the generator's outcome-append
    carry-over must preserve it verbatim."""
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "indus_claims",
        REPO_ROOT / "glossa-indus" / "scripts" / "indus_claims.py",
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    stem = "without_kings_or_conquests_the_indus_scr_ce9d98cc"
    lit = tmp_path / "documents"
    lit.mkdir()
    processed = tmp_path / "cleaned"
    processed.mkdir()
    out_dir = tmp_path / "extracted"
    out_dir.mkdir()
    prior_text = STORE.read_text("utf-8")
    prior = json.loads(prior_text)
    (lit / f"{stem}.json").write_text(
        json.dumps({"title": prior["title"]}), "utf-8"
    )
    (out_dir / f"{stem}.json").write_text(prior_text, "utf-8")
    mod.LIT_DOCS = lit
    mod.PROCESSED_TEXT = processed
    mod.EXTRACTED_CLAIMS = out_dir
    result = mod.process_document(stem)
    assert result["status"] == "extracted"
    regenerated = json.loads(
        (out_dir / f"{stem}.json").read_text("utf-8")
    )
    claim = next(
        c for c in regenerated["claims"] if c["claim_id"] == CLAIM_ID
    )
    before = _claim()
    assert claim[APPEND_KEY] == before[APPEND_KEY]
    assert claim["falsification_condition"] == FALSIFIER
    assert claim["claim_status"] == "partially_supported"


def test_records_on_disk_carry_the_outcome():
    outcome_md = (SPEC_DIR / "outcome.md").read_text("utf-8")
    step0_md = (SPEC_DIR / "step0-record.md").read_text("utf-8")
    report = (REPO_ROOT / "reports/phase440_report.md").read_text(
        "utf-8")
    for text in (outcome_md, step0_md, report):
        assert "NOT SUPPORTED" in text
    assert FREEZE_DIGEST in outcome_md
    assert "cfe7z" in outcome_md
    assert PUBLICATION_SHA in step0_md
    # The section 6 headline items ride in the report.
    assert CLAIM_ID in report
    assert ("This corpus is an ICIT-lineage corpus. Agreement between "
            "it and the program's earlier ICIT-lineage layer is "
            "consistency within one tradition, not independent "
            "corroboration.") in report
    assert ("This result is about depiction and position in recorded "
            "data. It is not evidence that any sign marked identity, "
            "a guild, or goods.") in report
    assert "49%" in report
    ledger = (REPO_ROOT / "LEDGER.md").read_text("utf-8")
    assert "Spec 074 EXECUTED (Phase-440)" in ledger
    graph = (REPO_ROOT / "backend/glossa_lab"
             / "experiment_graph_phase440.py").read_text("utf-8")
    assert "IndusPhase440HuntOpeningSigns" in graph
    registry = (REPO_ROOT / "backend/glossa_lab"
                / "experiment_graph.py").read_text("utf-8")
    assert "_phase440_node_defs" in registry
