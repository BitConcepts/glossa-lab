"""Dated-append carry-over — realignment Item 1.2 (2026-10-25).

Finding RT-02 (red-team attack, 2026-10-24/25): the claim-store
generator's regeneration carried the dated outcome appends but NOT
the audit notes / corrections of 2026-10-22
(``audit_note_2026_10_22``, ``audit_correction_2026_10_22``) nor the
Spec 054 falsifier append (``spec054_falsifier_append_2026_10_23``) —
the exact key families the owner freeze-pin ruling of 2026-10-23
designated as carrying the corrected facts permanently. The strip was
proven live in suite conditions (Spec 054 adjudication §9.8: the
suite regenerates the store in place, and the on-disk store then has
no ``audit_note_2026_10_22``). The first committed regeneration on a
tree whose tests did not themselves regenerate first would have
stripped every such note, silently.

These tests pin the widened carry-over (2026-10-25):

* every dated-append family survives a regeneration verbatim, by
  claim identity;
* the §9.8 regression case itself: the real yadav_2009_arxiv record,
  whose manual_002 carries the Spec 054 falsifier append and an
  audit note, regenerated from the committed inputs;
* the scope stays deliberate: a prior key outside the dated-append
  family is NOT carried (the carry-over is not "keep everything").

Able-to-fail: on the pre-widening generator the first two tests fail
(the audit and falsifier-append keys are absent after regeneration);
they were verified failing against that generator before the fix
landed.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[2]
_CLAIMS_DIR = _REPO_ROOT / "glossa-indus" / "claims" / "extracted_claims"
_LIT_DIR = _REPO_ROOT / "glossa-indus" / "literature" / "documents"


def _load_indus_claims():
    spec = importlib.util.spec_from_file_location(
        "indus_claims", _REPO_ROOT / "glossa-indus" / "scripts" / "indus_claims.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _plant(tmp_path, doc_id: str, prior_claims: list[dict]):
    lit = tmp_path / "documents"; lit.mkdir(exist_ok=True)
    processed = tmp_path / "cleaned"; processed.mkdir(exist_ok=True)
    out_dir = tmp_path / "extracted"; out_dir.mkdir(exist_ok=True)
    (lit / f"{doc_id}.json").write_text(
        json.dumps({"title": "Planted"}), "utf-8")
    (out_dir / f"{doc_id}.json").write_text(
        json.dumps({"document_id": doc_id, "claims": prior_claims}), "utf-8")
    return lit, processed, out_dir


def _run(mod, tmp_path, doc_id: str, lit, processed, out_dir):
    mod.LIT_DOCS = lit
    mod.PROCESSED_TEXT = processed
    mod.EXTRACTED_CLAIMS = out_dir
    result = mod.process_document(doc_id)
    assert result["status"] == "extracted"
    regenerated = json.loads((out_dir / f"{doc_id}.json").read_text("utf-8"))
    return {c["claim_id"]: c for c in regenerated["claims"]}


_SENTINELS = {
    "audit_note_2026_10_22": {"date": "2026-10-22",
                              "note": "sentinel-audit-note"},
    "audit_correction_2026_10_22": {"date": "2026-10-22",
                                    "note": "sentinel-audit-correction"},
    "spec054_falsifier_append_2026_10_23": {"date": "2026-10-23",
                                            "note": "sentinel-falsifier-append"},
    "spec052_outcome_append_2026_10_24": {"date": "2026-10-24",
                                          "note": "sentinel-outcome-append"},
    "spec072_outcome_2026_10_22": {"date": "2026-10-22",
                                   "note": "sentinel-outcome-key"},
}


def test_dated_append_families_survive_regeneration(tmp_path):
    mod = _load_indus_claims()
    prior = {"claim_id": "demo_doc_language_0001", **_SENTINELS,
             "owner_memo": "not-a-dated-append-must-not-carry"}
    lit, processed, out_dir = _plant(tmp_path, "demo_doc", [prior])
    (processed / "demo_doc.txt").write_text(
        "The Indus script encodes Proto-Dravidian language.", "utf-8")
    claims = _run(mod, tmp_path, "demo_doc", lit, processed, out_dir)
    (claim,) = claims.values()
    assert claim["claim_id"] == "demo_doc_language_0001"
    for key, value in _SENTINELS.items():
        assert claim.get(key) == value, key
    # Scope boundary: the carry-over is the dated-append family,
    # not arbitrary prior keys.
    assert "owner_memo" not in claim


def test_spec054_regression_case_real_record(tmp_path):
    """The §9.8 case: the committed yadav_2009_arxiv store record,
    regenerated from the committed inputs, keeps its dated appends."""
    mod = _load_indus_claims()
    prior_doc = json.loads(
        (_CLAIMS_DIR / "yadav_2009_arxiv.json").read_text("utf-8"))
    prior = {c["claim_id"]: c for c in prior_doc["claims"]}
    manual_002 = prior["yadav_2009_arxiv_manual_002"]
    assert "spec054_falsifier_append_2026_10_23" in manual_002
    assert "audit_note_2026_10_22" in manual_002

    lit = tmp_path / "documents"; lit.mkdir()
    processed = tmp_path / "cleaned"; processed.mkdir()
    out_dir = tmp_path / "extracted"; out_dir.mkdir()
    (lit / "yadav_2009_arxiv.json").write_text(
        (_LIT_DIR / "yadav_2009_arxiv.json").read_text("utf-8"), "utf-8")
    (out_dir / "yadav_2009_arxiv.json").write_text(
        json.dumps(prior_doc), "utf-8")
    claims = _run(mod, tmp_path, "yadav_2009_arxiv", lit, processed, out_dir)

    regenerated_002 = claims["yadav_2009_arxiv_manual_002"]
    for key in ("spec054_falsifier_append_2026_10_23",
                "audit_note_2026_10_22",
                "spec054_outcome_append_2026_10_24"):
        assert regenerated_002.get(key) == manual_002[key], key
    regenerated_001 = claims["yadav_2009_arxiv_manual_001"]
    prior_001 = prior["yadav_2009_arxiv_manual_001"]
    assert regenerated_001.get("audit_note_2026_10_22") == \
        prior_001["audit_note_2026_10_22"]


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(pytest.main([__file__, "-q"]))
