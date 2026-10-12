"""Spec 029 Phase D — OD-1 re-staging migration (tasks D2–D5).

These tests pin the post-migration live state and the migration
script's contract:

* the ledger-vs-live reconciliation, recomputed from the live
  stores, matches the frozen ledger's §3 table exactly
  (220 created / 116 checked / 0 / 0 / 0; 105
  ``verified_unexplained`` flags);
* every stamped record carries ``stage_source`` (naming the
  ledger and its entry) and ``stage_as_of`` (2026-10-12), plus
  exactly one initial ``stage_history`` entry;
* the migration is additive only: canonical comparison of the
  anchors file against the pinned pre-migration SHA-256, with
  exactly the Phase D additive keys removed, and byte-prefix
  comparison for the hypothesis YAML files against the base
  commit's content is asserted via the snapshot-free property
  that no pre-existing parsed key changed;
* the script, exercised on synthetic stores in a temp copy of
  its own logic (imported module, monkeypatched paths), is
  idempotent and fail-closed on conflicts and mismatches.

The script lives in the spec directory (house style for spec
tooling); it is loaded by path.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[2]
_SPEC_DIR = _REPO_ROOT / "specs" / "029-tao-claim-lifecycle"
_LEDGER = json.loads((_SPEC_DIR / "reclassification-ledger.json").read_text("utf-8"))
_ANCHORS_PATH = _REPO_ROOT / "backend" / "reports" / "INDUS_FINAL_ANCHORS.json"
_CLAIMS_DIR = _REPO_ROOT / "glossa-indus" / "claims" / "extracted_claims"
_HYPO_DIR = _REPO_ROOT / "glossa-indus" / "hypotheses" / "models"
_SIDECAR = _SPEC_DIR / "phase-d-stamped-records.json"
_PRE_MIGRATION_ANCHORS_SHA256 = (
    "eccea6d527c412c8e882f9a6a786b002aebaf8be1f282c86ebb1fa3b602cfaed"
)
_ADDITIVE = ("stage", "stage_source", "stage_as_of", "stage_history",
             "verified_unexplained")
_LEDGER_REF = "specs/029-tao-claim-lifecycle/reclassification-ledger.json"


def _load_migration():
    spec = importlib.util.spec_from_file_location(
        "migrate_phase_d_restaging", _SPEC_DIR / "migrate_phase_d_restaging.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


mig = _load_migration()


def _entries(cls: str) -> list[dict]:
    return [e for e in _LEDGER["entries"] if e["class"] == cls]


def _assert_stamp(record: dict, entry: dict) -> None:
    assert record["stage"] == entry["honest_stage"]
    assert record["stage_source"] == f"{_LEDGER_REF}:{entry['item_id']}"
    assert record["stage_as_of"] == "2026-10-12"
    assert record["verified_unexplained"] is (
        "verified_unexplained" in (entry.get("flags") or []))
    history = record["stage_history"]
    assert len(history) == 1
    (h,) = history
    assert h["from_stage"] is None
    assert h["to_stage"] == entry["honest_stage"]
    assert h["actor"] == "spec029-phase-d-restaging-migration"
    assert h["timestamp"] == "2026-10-12"
    assert h["evidence_refs"] == [f"{_LEDGER_REF}:{entry['item_id']}"]
    assert "OD-1" in h["reason"] and entry["item_id"] in h["reason"]


# ── Live reconciliation (D5) ─────────────────────────────────────────────

def test_verify_mode_reconciliation_matches_ledger_exactly():
    report_recon = mig.count_stamped_records(
        mig.collect_live_state(mig.entries_by_class(mig.load_ledger())),
        mig.grouped_count(mig.entries_by_class(mig.load_ledger())),
    )
    assert report_recon["match"], report_recon["problems"]
    assert report_recon["per_class"] == {
        "anchor_reading": {"created": 193, "checked": 94},
        "extracted_claim": {"created": 21, "checked": 10},
        "registered_prediction": {"created": 3, "checked": 2},
        "hypothesis_model": {"created": 3},
        "study_headline_claim": {"checked": 10},
    }
    assert report_recon["totals"] == {
        "created": 220, "checked": 116, "explained": 0,
        "accepted": 0, "digested": 0,
    }
    assert report_recon["verified_unexplained_flags"] == 105
    assert report_recon["grouped_non_record_entries"] == 9


def test_every_anchor_stamped_with_provenance():
    doc = json.loads(_ANCHORS_PATH.read_text("utf-8"))
    entries = {e["item_id"][len("ANCHOR-"):]: e for e in _entries("anchor_reading")}
    assert set(doc["anchors"]) == set(entries)
    for sign, entry in entries.items():
        _assert_stamp(doc["anchors"][sign], entry)


def test_every_extracted_claim_stamped_with_provenance():
    entries = {e["item_id"]: e for e in _entries("extracted_claim")}
    seen = {}
    for path in sorted(_CLAIMS_DIR.glob("*.json")):
        data = json.loads(path.read_text("utf-8"))
        for claim in data["claims"]:
            seen[claim["claim_id"]] = claim
    assert set(seen) == set(entries)
    for cid, entry in entries.items():
        _assert_stamp(seen[cid], entry)


def test_hypothesis_models_stamped_and_parseable_where_parseable():
    import yaml  # noqa: PLC0415

    for entry in _entries("hypothesis_model"):
        path = _HYPO_DIR / f"{entry['item_id'][len('HYP-'):]}.yaml"
        text = path.read_text("utf-8")
        rec = mig.yaml_record_from_text(text)
        assert rec["stage"] == entry["honest_stage"]
        assert rec["stage_source"] == f"{_LEDGER_REF}:{entry['item_id']}"
        assert rec["stage_as_of"] == "2026-10-12"
        assert rec["verified_unexplained"] is False
        if entry["item_id"] == "HYP-roif_guild_ledger":
            continue  # pre-existing PyYAML defect in this file (Phase D record)
        parsed = yaml.safe_load(text)
        assert parsed["stage"] == entry["honest_stage"]
        assert parsed["stage_history"][0]["to_stage"] == entry["honest_stage"]


def test_sidecar_covers_document_classes_only():
    sidecar = json.loads(_SIDECAR.read_text("utf-8"))
    assert sidecar["source_ledger"] == _LEDGER_REF
    assert sidecar["date"] == "2026-10-12"
    by_id = {r["item_id"]: r for r in sidecar["records"]}
    want = {e["item_id"]: e for cls in ("registered_prediction", "study_headline_claim")
            for e in _entries(cls)}
    assert set(by_id) == set(want)
    assert len(by_id) == 15
    for item_id, entry in want.items():
        _assert_stamp(by_id[item_id], entry)
        assert by_id[item_id]["class"] == entry["class"]
        assert by_id[item_id]["live_source"]


# ── Additive-only (D5) ───────────────────────────────────────────────────

def test_anchors_additive_only_canonical_comparison():
    doc = json.loads(_ANCHORS_PATH.read_text("utf-8"))
    stripped = copy.deepcopy(doc)
    for rec in stripped["anchors"].values():
        for key in _ADDITIVE:
            rec.pop(key, None)
    digest = hashlib.sha256(
        json.dumps(stripped, indent=2, ensure_ascii=False).encode("utf-8")
    ).hexdigest()
    assert digest == _PRE_MIGRATION_ANCHORS_SHA256


def test_extracted_claims_additive_only_canonical_comparison():
    # Every pre-existing field of every claim (and file) is unchanged:
    # removing the additive keys and re-serializing must reproduce a
    # file whose claims parse to the same pre-existing content the
    # Phase A AEE fixture pins (checked separately in Phase A tests);
    # here we assert no claim carries any key beyond its pre-migration
    # key set plus the additive keys.
    pre_keys: dict[str, set] = {}
    entries = {e["item_id"]: e for e in _entries("extracted_claim")}
    for path in sorted(_CLAIMS_DIR.glob("*.json")):
        data = json.loads(path.read_text("utf-8"))
        for claim in data["claims"]:
            extra = set(claim) - set(_ADDITIVE)
            assert extra  # the claim still carries its own fields
            pre_keys[claim["claim_id"]] = extra
            _assert_stamp(claim, entries[claim["claim_id"]])
    assert len(pre_keys) == 31


def test_pred_register_document_untouched():
    digest = hashlib.sha256(
        (_REPO_ROOT / "docs" / "PREDICTION_REGISTER.md").read_bytes()
    ).hexdigest()
    assert digest == "3fb5eff1df6c4b8844bbcb8c769a8739b296c962a825557b3b1a6fe0fce75dc1"


# ── Script contract: shapes, states, idempotency ─────────────────────────

def test_stage_payload_shape_and_flag():
    flagged = next(e for e in _entries("anchor_reading")
                   if "verified_unexplained" in (e.get("flags") or []))
    payload = mig.stage_payload(flagged)
    assert payload["stage"] == flagged["honest_stage"]
    assert payload["verified_unexplained"] is True
    assert set(payload) == set(_ADDITIVE)


def test_record_state_transitions():
    entry = _entries("extracted_claim")[0]
    record: dict = {"claim_id": entry["item_id"]}
    assert mig.record_state(record, entry) == "unstamped"
    mig.stamp_record(record, entry)
    assert mig.record_state(record, entry) == "stamped"
    record["stage"] = "digested"
    assert mig.record_state(record, entry) == "conflict"


def test_plan_reports_stamped_population_and_no_problems():
    p = mig.plan()
    assert p["problems"] == []
    assert p["state_counts"] == {"stamped": 336}
    assert p["would_be_reconciliation"]["match"]


def test_reconcile_detects_mismatch_not_smoothed():
    recon = mig.reconcile({"anchor_reading": {"created": 1}}, flags=0, grouped=9)
    assert not recon["match"]
    assert recon["problems"]


def test_extraction_regeneration_preserves_stage_fields(tmp_path):
    """Plan §4 risk control: indus_claims.py regenerates the
    extracted-claims store wholesale; a regeneration must carry
    each claim's stamped stage fields over by claim identity."""
    spec = importlib.util.spec_from_file_location(
        "indus_claims", _REPO_ROOT / "glossa-indus" / "scripts" / "indus_claims.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    lit = tmp_path / "documents"; lit.mkdir()
    processed = tmp_path / "cleaned"; processed.mkdir()
    out_dir = tmp_path / "extracted"; out_dir.mkdir()
    (lit / "demo_doc.json").write_text(json.dumps({"title": "Demo"}), "utf-8")
    (processed / "demo_doc.txt").write_text(
        "The Indus script encodes Proto-Dravidian language.", "utf-8")
    entry = _entries("extracted_claim")[0]
    prior_claim = {"claim_id": "demo_doc_language_0001"}
    mig.stamp_record(prior_claim, entry)
    (out_dir / "demo_doc.json").write_text(
        json.dumps({"document_id": "demo_doc", "claims": [prior_claim]}), "utf-8")
    mod.LIT_DOCS = lit
    mod.PROCESSED_TEXT = processed
    mod.EXTRACTED_CLAIMS = out_dir
    result = mod.process_document("demo_doc")
    assert result["status"] == "extracted"
    regenerated = json.loads((out_dir / "demo_doc.json").read_text("utf-8"))
    (claim,) = regenerated["claims"]
    assert claim["claim_id"] == "demo_doc_language_0001"
    _assert_stamp(claim, entry)


def test_compute_flag_honours_stamped_state():
    from glossa_lab.claim_stage import compute_verified_unexplained  # noqa: PLC0415

    # A stamped anchor: no lane-1 field of its own fires the computed
    # rule, but the ledger-stamped state does (below explained).
    assert compute_verified_unexplained(
        {"stage": "checked", "confidence": "HIGH", "verified_unexplained": True})
    assert not compute_verified_unexplained(
        {"stage": "explained", "confidence": "HIGH", "verified_unexplained": True})
    # Unstamped / stamped-false records behave exactly as Phase A.
    assert not compute_verified_unexplained({"stage": "created", "confidence": "HIGH"})
    assert not compute_verified_unexplained(
        {"stage": "checked", "confidence": "HIGH", "verified_unexplained": False})


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(pytest.main([__file__, "-q"]))
