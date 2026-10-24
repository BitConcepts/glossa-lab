"""Tests for the Spec 054 execution records.

Phase-438 (Yadav opening/closing signs, the
amended falsifier act under battery NB-1)
executed under the frozen amended contract:
gate G1 (pin checks) passed, gate G2 (strict
corpus identification and pin) failed on
observed values, and the run closed STRICT
CORPUS NOT PINNABLE with gates G3–G5 not
reached and no positional quantity computed.
The outcome was appended as a dated entry to
the claim's record. These tests pin the
recorded facts: a gate verdict, a census
number, or an append that drifts from the
executed run fails here.

Author: Spec 054 (Phase-438), 2026-10-24.
"""
from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
RESULTS = REPO_ROOT / "reports/phase438_results.json"
SPEC_DIR = REPO_ROOT / "specs/054-yadav-opening-closing"
STORE = (REPO_ROOT / "glossa-indus/claims/extracted_claims/"
         "yadav_2009_arxiv.json")
APPEND_KEY = "spec054_outcome_append_2026_10_24"
FREEZE_DIGEST = (
    "d85f6ace80e2ae2935d96d4916e51db686f11fb2c4473dc24d1198580012bb57"
)
FALSIFIER = (
    "This claim, as evaluated under battery NB-1 (the Spec 054 "
    "amendment, as frozen), is falsified if any of the following "
    "holds when the frozen battery is run on the frozen arm-1 "
    "and arm-2 corpora: (1) either arm-1 positional-strong set "
    "(opening or closing) is empty; (2) for either class, fewer "
    "than half of arm 1's positional-strong signs are also "
    "positional-strong in arm 2 in the same class, through the "
    "pinned crosswalk; or (3) the pooled cross-arm overlap of "
    "positional-strong signs does not exceed the 95th "
    "percentile of the 999-shuffle label-permutation null — "
    "the three conditions applied under the precedence rule "
    "of the Spec 054 amendment (§5.5)."
)


def _results() -> dict:
    return json.loads(RESULTS.read_text("utf-8"))


def _claim() -> dict:
    d = json.loads(STORE.read_text("utf-8"))
    for c in d["claims"]:
        if c["claim_id"] == "yadav_2009_arxiv_manual_002":
            return c
    raise AssertionError("manual_002 not in the store")


def test_phase438_results_record_complete():
    r = _results()
    text = RESULTS.read_text("utf-8")
    assert r["spec"] == "054"
    assert r["phase"] == 438
    assert r["claim_id"] == "yadav_2009_arxiv_manual_002"
    assert r["contract"]["freeze_digest"] == FREEZE_DIGEST
    assert r["contract"]["osf_registration"] == "8spvf"
    assert r["contract"]["falsifier"] == FALSIFIER
    assert r["contract"]["falsifier_append_date"] == "2026-10-23"
    assert "938174b0dee14169a5340c9299c73f4eb5b997377f8198a146ef611e73924050" in text


def test_gates_in_frozen_order_closure_at_g2():
    r = _results()
    verdicts = [(g["gate"], g["verdict"]) for g in r["gates"]]
    assert verdicts == [
        ("G1", "PASS"),
        ("G2", "FAIL"),
        ("G3", "NOT REACHED"),
        ("G4", "NOT REACHED"),
        ("G5", "NOT REACHED"),
    ]
    assert r["outcome"] == "STRICT CORPUS NOT PINNABLE"
    # A step-0 closure computes no positional quantity:
    # no battery record and no decision record exist.
    assert r["battery_arm1"] is None
    assert r["battery_arm2"] is None
    assert r["decision"] is None
    pins = r["gates"][0]["inputs"]
    assert all(p["match"] for p in pins)
    assert r["gates"][0]["freeze_digest"]["match"] is True


def test_identification_record_values():
    r = _results()
    idn = r["identification"]
    ref = idn["reference_census_C3"]
    assert ref["total_records"] == 3916
    assert ref["unique_dockeys"] == 2665
    assert ref["total_sequences"] == 3137
    assert ref["total_sign_instances"] == 12494
    # The loader's file is absent everywhere scanned and
    # the loader therefore loads zero.
    assert idn["C1_loader_file_found"] is None
    assert len(idn["C1_loader_file_candidates"]) >= 2
    assert not any(c["present"]
                   for c in idn["C1_loader_file_candidates"])
    cen = idn["C1_loader_census"]
    assert cen["total_records"] == 0
    assert cen["total_sequences"] == 0
    assert idn["census_reproduces_phase43_record"] is False
    assert idn["identified"] is False
    # No database copy in the execution tree.
    assert idn["C2_database"]["execution_tree_db_present"] is False
    # C4: every other layer censused, none substituted.
    others = {o["layer"]: o for o in idn["C4_other_layers"]}
    assert len(others) == 5
    yaj = next(v for k, v in others.items()
               if k.startswith("yajnadevam"))
    assert yaj["records"] == 5679
    mayig = next(v for k, v in others.items()
                 if k.startswith("mayig"))
    assert mayig["inscriptions"] == 179
    assert mayig["tokens"] == 1003
    holdat = next(v for k, v in others.items()
                  if k.startswith("the Holdat"))
    assert holdat["inscriptions"] == 1670
    assert holdat["tokens"] == 7002
    assert holdat["distinct_signs"] == 390
    shakti = next(v for k, v in others.items()
                  if k.startswith("the Shakti"))
    assert shakti["records"] == 5704


def test_headline_wording_is_the_frozen_closure_form():
    r = _results()
    h = r["headline_wording"]
    assert h.startswith(
        "Spec 054 closed at step 0, gate 0.3: the strict "
        "corpus layer of record could not be uniquely "
        "identified and pinned from the database as the "
        "V3 / Mahadevan-lineage corpus the Phase-43 "
        "battery used ("
    )
    assert "No positional quantity was computed." in h
    assert h.endswith(
        "the claim stands exactly as recorded, with the "
        "falsifier appended at this spec's freeze."
    )
    assert "RE-EARNED" not in h
    assert "RE-EARNED" not in r["outcome_append_text"]


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
    assert entry["outcome"] == "STRICT CORPUS NOT PINNABLE"
    assert entry["date"] == "2026-10-24"
    assert entry["phase"] == 438
    # The append moves nothing else on the record: the
    # falsifier appended at the freeze stands verbatim,
    # and the claim's status and stage are untouched.
    assert c["falsification_condition"] == FALSIFIER
    assert c["claim_status"] == "strongly_supported"
    assert c["stage"] == "explained"


def test_regeneration_preserves_the_outcome_append(tmp_path):
    """The extracted-claims generator regenerates the store
    wholesale (the Spec 029 tests do it in-tree); the dated
    outcome append is a record, not extraction output, and
    the generator's outcome-append carry-over must preserve
    it verbatim, as must the falsifier carry-over (the
    Spec 054 amendment's section 7 act)."""
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "indus_claims",
        REPO_ROOT / "glossa-indus" / "scripts" / "indus_claims.py",
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    lit = tmp_path / "documents"
    lit.mkdir()
    processed = tmp_path / "cleaned"
    processed.mkdir()
    out_dir = tmp_path / "extracted"
    out_dir.mkdir()
    prior_text = STORE.read_text("utf-8")
    prior = json.loads(prior_text)
    (lit / "yadav_2009_arxiv.json").write_text(
        json.dumps({"title": prior["title"]}), "utf-8"
    )
    (out_dir / "yadav_2009_arxiv.json").write_text(
        prior_text, "utf-8"
    )
    mod.LIT_DOCS = lit
    mod.PROCESSED_TEXT = processed
    mod.EXTRACTED_CLAIMS = out_dir
    result = mod.process_document("yadav_2009_arxiv")
    assert result["status"] == "extracted"
    regenerated = json.loads(
        (out_dir / "yadav_2009_arxiv.json").read_text("utf-8")
    )
    claim = next(
        c for c in regenerated["claims"]
        if c["claim_id"] == "yadav_2009_arxiv_manual_002"
    )
    before = _claim()
    assert claim[APPEND_KEY] == before[APPEND_KEY]
    assert claim["falsification_condition"] == FALSIFIER
    assert claim["claim_status"] == "strongly_supported"


def test_records_on_disk_carry_the_outcome():
    outcome_md = (SPEC_DIR / "outcome.md").read_text("utf-8")
    step0_md = (SPEC_DIR / "step0-record.md").read_text("utf-8")
    report = (REPO_ROOT / "reports/phase438_report.md").read_text(
        "utf-8")
    for text in (outcome_md, step0_md, report):
        assert "STRICT CORPUS NOT PINNABLE" in text
    assert FREEZE_DIGEST in outcome_md
    assert "8spvf" in outcome_md
    assert FALSIFIER in report
