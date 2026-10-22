"""Spec 063 execution tests (Phase-425).

The execution's terminal outcome is RECOVERED:
step 0 passed in full (every section 2 pin; the
thesis file asserted to its frozen digest on the
local file BEFORE any plate was read; the
preserved reference producible at its pinned
digest with the plate page produced from the
pinned file), step D's two independent
derivations agree with each other and sustain
the preserved descriptor, step C passes on the
anchors' agreement, and step M identifies the
drawn sign by route 2 (route 1 attempted and
failed; no fallback to P378). Candidate K-1
therefore passes R-1 through R-5 — the argument
conditions of record in Spec 056's execution,
R-3 run afresh under section 5 — and enters at
created, untested, with a designed-never-run
test note. These tests pin the delivered form:
the results record's gate, derivation,
continuity and route facts, the frozen traps
asserted as traps (a W821 number match, the
Yunmapped_0821 collision, P378 as the target, or
sign 861 evidence used for 821 would fail
here), and the claim-record restatement append
in its prescribed form. On the live claim store
only regeneration-preserved facts are asserted
(the Spec 038 form): the store is regenerated
by the backend suite, so the append itself is
asserted through the run's machine record and
the outcome record, exactly as at Spec 056.
"""
from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
SPEC_DIR = REPO / "specs/063-sign821-identification-successor"
RESULTS = REPO / "reports/phase425_results.json"
IDENT = SPEC_DIR / "identification-record.md"
REFERENCE = SPEC_DIR / "drawn-form-reference-821.json"
CLAIM_FILE = (
    REPO / "glossa-indus/claims/extracted_claims/"
    "the_archaeology_and_epigraphy_of_indus_w_27f45a68.json"
)
CLAIM_ID = (
    "the_archaeology_and_epigraphy_of_indus_w_27f45a68_sign_val_0001")
REFERENCE_SHA256 = (
    "695dd35d55bd2f68d8c9db0ea79dde249b53c55d11ed2f622752a18511e65999")
THESIS_SHA256 = (
    "4b39330c7f4ccf2770093318bfdaf4efaffa7fdf4a8cb5763a650351fffa4b4e")


def _results() -> dict:
    return json.loads(RESULTS.read_text(encoding="utf-8"))


def _claim_entry() -> dict:
    doc = json.loads(CLAIM_FILE.read_text(encoding="utf-8"))

    def find(node):
        if isinstance(node, dict):
            if node.get("claim_id") == CLAIM_ID:
                return node
            for value in node.values():
                hit = find(value)
                if hit is not None:
                    return hit
        elif isinstance(node, list):
            for value in node:
                hit = find(value)
                if hit is not None:
                    return hit
        return None

    entry = find(doc)
    assert entry is not None
    return entry


def test_results_record_outcome_and_step0():
    r = _results()
    assert r["phase"] == "Phase-425"
    assert r["spec"] == "063"
    assert r["claim_id"] == CLAIM_ID
    assert r["candidate"] == "K-1"
    assert r["outcome"] == "RECOVERED"
    assert r["route_used"] == "route 2"
    assert "completes the recovery Spec 056 could not finish" in (
        r["headline_wording"])
    assert r["preserved_reference"]["sha256"] == REFERENCE_SHA256
    g1 = r["step0"]["gate_0_1"]
    for name, pin in g1.items():
        assert pin["match"] is True, name
    assert g1["claim_record_spec038_form"][
        "freeze_time_sha256_constant"] == (
        "bd0f7abddc9c26537f4ebe5f66f6a1fc69d394a4c2edbe745a8b7eb1ddc3333a")
    facts = g1["claim_record_spec038_form"]["facts"]
    assert facts["spec056_closure_append_present"] is True
    assert facts["spec056_closure_outcome"] == "IDENTIFICATION FAILED"
    assert g1["passage_of_record"]["match"] is True
    # Gate 0.2: the thesis file asserted to its
    # frozen digest before any plate was read.
    g2 = r["step0"]["gate_0_2"]
    assert g2["match"] is True
    assert g2["observed_sha256"] == THESIS_SHA256
    assert g2["observed_bytes"] == 19313853
    assert g2["asserted_before_any_plate_read"] is True
    # Gate 0.3: the plate page produced from the
    # pinned file; no image committed.
    g3 = r["step0"]["gate_0_3"]
    assert g3["produced_from_pinned_file"] is True
    assert g3["reference_at_pinned_digest"] is True
    assert g3["pdf_pages"] == 296
    assert g3["plate_page"]["pdf_page"] == 104
    assert g3["plate_page"]["thesis_page"] == 92
    assert g3["images_committed"] is False
    assert len(g3["plate_page"]["embedded_images"]) >= 1
    assert r["step0"]["all_gates_passed"] is True
    assert r["anchors"]["byte_identical"] is True


def test_step_d_two_derivations_reconciled_and_sustained():
    r = _results()
    d = r["step_d"]
    for key in ("derivation_a", "derivation_b"):
        sheet = d[key]
        assert "without sight of" in sheet["method"]
        assert "thesis p. 92 / PDF p. 104" in sheet["plate_locator"]
        feats = sheet["features"]
        assert ("two" in feats["outline"].lower()
                or "pair" in feats["outline"].lower())
        assert "6" in feats["internal_divisions"] and (
            "sector" in feats["internal_divisions"].lower())
        assert "six sectors" in sheet["descriptor"]
        assert "vertical" in sheet["descriptor"]
        assert "diagonal" in sheet["descriptor"]
        assert set(sheet["neighbours"]) == {
            "818", "820", "822", "823", "791"}
    rec = d["reconciliation"]
    assert rec["disagreements"].startswith("None")
    assert rec["reconciled_features"]["outline_count"] == 2
    assert rec["reconciled_features"]["diameters_per_oval"] == 3
    assert rec["reconciled_features"]["sectors_per_oval"] == 6
    comp = d["comparison_with_preserved_descriptor"]
    assert comp["agreement"] is True
    assert comp["material_difference"] is None
    reference = json.loads(REFERENCE.read_text(encoding="utf-8"))
    assert comp["preserved_descriptor"] == reference["descriptor"]
    assert d["result"].startswith("PASS")


def test_step_c_continuity_on_the_anchors():
    r = _results()
    c = r["step_c"]
    assert c["agreement"] is True
    assert c["result"].startswith("PASS")
    anchors = c["anchors"]
    form = anchors["formation_passage"]
    assert "sign 820 doubles to form sign 821" in form["verbatim"]
    assert form["verified_verbatim_in_held_text"] is True
    reg = anchors["registry_anchor"]
    assert reg["row"] == "P378"
    assert reg["wells_ids"] == "W820"
    assert reg["mahadevan_ids"] == "M391"
    assert reg["description"] == (
        "Wheel with 6 spokes with even angles")


def test_step_m_routes_and_traps():
    r = _results()
    m = r["step_m"]
    assert m["route_used"] == "route 2"
    r1 = m["route_1_registry_by_drawn_form"]
    assert r1["attempted"] is True
    assert r1["satisfied"] is False
    assert r1["registry_rows"] == 803
    assert r1["rows_with_w821_token"] == []
    six = {row["sign_id"] for row in r1["rows_describing_6_spokes"]}
    assert six == {"P378", "P379"}
    r2 = m["route_2_list_entry_through_preserved_reference"]
    assert r2["satisfied"] is True
    assert r2["reference"]["sha256"] == REFERENCE_SHA256
    assert r2["preconditions"]["sustained_at_step_d"] is True
    assert r2["preconditions"]["anchored_at_step_c"] is True
    assert r2["preconditions"]["list_named_from_document"] is True
    r3 = m["route_3_composition"]
    assert r3["attempted_as_the_match"] is False
    assert r3["satisfied"] is False
    traps = m["traps_asserted"]
    yun = traps["Yunmapped_0821"]["row"]
    assert yun["numbering_system"] == "yajnadevam_glyphid"
    assert yun["wells_ids"] == ""
    assert yun["corpus_freq"] == "10"
    assert "never used" in traps["Yunmapped_0821"]["assertion"]
    assert traps["sign_861"]["paragraph_verified_in_held_text"] is True
    assert "base sign" in traps["p378_as_target"]["assertion"]
    assert "No number-only match" in (
        traps["number_only_matching"]["assertion"])


def test_recovery_test_and_restatement_form():
    r = _results()
    t = r["recovery_test_k1"]
    for cond in ("R-1", "R-2", "R-3", "R-4", "R-5"):
        assert t[cond].startswith("PASS"), cond
    assert t["quote_verified_verbatim"] is True
    assert "not a nullification" in t["falsification_condition"]
    append = r["claim_restatement_append"]
    assert append["key"] == "spec063_restatement"
    assert append["spec"] == "063"
    assert append["phase"] == "Phase-425"
    assert append["date"] == "2026-10-22"
    assert append["outcome"] == "RECOVERED"
    assert "route 2" in append["identification"].lower()
    assert REFERENCE_SHA256 in append["identification"]
    assert "created stage" in append["lifecycle"]
    assert "untested" in append["lifecycle"]
    assert "no test is" in append["test_design_note"].lower() or (
        "no test has been run" in append["lifecycle"])
    assert append["record"] == (
        "specs/063-sign821-identification-successor/outcome.md")
    assert append["identification_record"] == (
        "specs/063-sign821-identification-successor/"
        "identification-record.md")


def test_identification_record_carries_the_sheets():
    text = IDENT.read_text(encoding="utf-8")
    for needle in (
        "Derivation A — sequential plate read",
        "Derivation B — neighbour-contrast read",
        "Reconciliation",
        "Comparison with the preserved descriptor",
        "SUSTAINED",
        "Step C result: PASS",
        "Route 1 (registry, by drawn form)",
        "Route 2 (the list's own entry, through",
        "Yunmapped_0821",
        "sign 861",
        REFERENCE_SHA256,
        THESIS_SHA256,
        "Fence sentence (spec §8, element 8)",
        "identification on a preserved reference",
        "No image is committed",
    ):
        assert needle in text, needle


def test_claim_record_live_facts_spec038_form():
    # Regeneration-preserved facts only: the
    # fragment's own facts stand as the frozen
    # record states, and its Spec 056 closure
    # append is present. The Spec 063 restatement
    # append itself is asserted at the act
    # (removal reproduces the pre-act file
    # byte-identically; outcome.md, F063-C11)
    # and through the run's machine record, not
    # on the live store.
    entry = _claim_entry()
    assert entry["normalized_claim"] == (
        "Sign value: 821 / it is used in a variety of "
        "contexts (Figure 6")
    assert entry["claim_status"] == "untested"
    assert entry["stage"] == "created"
    assert entry["spec056_closure"]["outcome"] == (
        "IDENTIFICATION FAILED")
