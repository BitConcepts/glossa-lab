"""Spec 029 Phase E2 — lane-separated rendering (tasks E2.1–E2.4;
FR-029-09, FR-029-10, FR-029-05 display rule; claims F029-C06/C07;
OD-4).

Pins the serialization and source-level facts the E2 rendering
depends on:

* E2.3/E2.4 (backend) — ``GET /claims`` serializes, per claim:
  ``not_understood`` (the record's own statement, or ``None`` —
  absence is serialized, never filled with generated text) with
  ``not_understood_recorded``, and ``bundle`` (the Phase B bundle
  serialization for bundle parents; ``None`` otherwise), as fields
  distinct from the lane-2 ``stage`` object and the lane-1 score.
* E2.2 (backend) — a synthetic contested bundle parent serializes
  its contest on the parent: ``attribution_contested`` is true, the
  contest record travels with it, and the parent-stage computation
  carries the OD-3 cap at ``checked``.
* E2.1/E2.5 (frontend sources) — the touched surfaces carry the
  lane regions, the standing position, the stage summary, and the
  OD-4 legend with the five stage names verbatim; no stage-label
  synonym (``verified`` / ``proven`` / ``confirmed`` as warmer
  renames) appears in the touched sources outside the governed
  ``verified_unexplained`` flag name; lane-1 badges in
  IndusEvidenceView no longer take per-status colours.
* E1 stays withdrawn — the panel keeps none of the E1 purge list.

All bundle fixtures are synthetic (invented persons, example
references). No live record is authored a ``not_understood``
statement by these tests. (Amended 2026-10-13: the live-store
assertions originally pinned the absence form on every record,
which was the honest state until the owner's lane-2 adoption act
of 2026-10-13 authored texts for the 23 canonical claims; the
live test below now pins the partitioned state — authored texts
on the canonical claims, the absence form on the 8 preserved
evidence instances.)
"""
from __future__ import annotations

import asyncio
import json
from pathlib import Path

import pytest

from glossa_lab.api import indus_evidence
from glossa_lab.claim_bundle import (
    SUBCLAIM_KINDS,
    make_attribution_subclaim,
    make_bundle,
    make_subclaim,
)
from glossa_lab.claim_stage import with_stage_defaults

_REPO = Path(__file__).resolve().parents[2]
_CLAIMS_DIR = _REPO / "glossa-indus" / "claims" / "extracted_claims"
# The adopted lane-2 records (PR #190): the expected authored
# not_understood text for each canonical extracted claim, read from
# the adopted record itself so this test pins the live stores
# against the durable artifact of record.
_ADOPTED_DRAFTS = json.loads(
    (_REPO / "specs" / "029-tao-claim-lifecycle" / "lane2-drafts"
     / "drafts.json").read_text(encoding="utf-8"))
_ADOPTED_NOT_UNDERSTOOD = {
    d["claim_id"]: d["not_understood"]
    for d in _ADOPTED_DRAFTS["drafts"]
    if d["record_kind"] == "extracted_claim"
}
_PANEL = _REPO / "frontend" / "src" / "components" / "DeciphermentPanel.tsx"
_EVIDENCE_VIEW = _REPO / "frontend" / "src" / "components" / "IndusEvidenceView.tsx"
_LEGEND = _REPO / "frontend" / "src" / "components" / "StageLegend.tsx"

TS = "2026-10-12T12:00:00+00:00"
REFS = ["https://example.org/e2-evidence"]
AUTHORED_NOT_UNDERSTOOD = (
    "Synthetic authored statement: which sign values the neighbouring "
    "signs force remains not understood."
)


def _run_list_claims(monkeypatch, claims_dir: Path, **kwargs):
    monkeypatch.setattr(indus_evidence, "_CLAIMS_DIR", claims_dir)
    return asyncio.run(indus_evidence.list_claims(**kwargs))


def _write_claims_file(dirpath: Path, claims: list[dict]) -> None:
    dirpath.mkdir(parents=True, exist_ok=True)
    (dirpath / "synthetic_doc.json").write_text(
        json.dumps({"document_id": "synthetic_doc", "claims": claims}),
        encoding="utf-8",
    )


# ── E2.3/E2.4: live-store serialization (authored + absence forms) ───────


def test_live_claims_serialize_not_understood_state_and_no_bundle():
    """Live records, as amended by the lane-2 adoption act of
    2026-10-13 (owner act; PR #190 + ingestion): the 23 canonical
    claims carry the authored ``not_understood`` texts the owner
    adopted — the endpoint must serialize them verbatim, with the
    flag True. The 8 preserved evidence instances are not claims
    of their own and carry no authored text: for them the endpoint
    must serialize the absence form — the field present and None,
    the flag False — never substitute text. No extracted claim is
    a bundle parent."""
    if not _CLAIMS_DIR.exists():
        pytest.skip("extracted_claims dir not present")
    result = asyncio.run(indus_evidence.list_claims(limit=500))
    assert result["total"] == 31
    for entry in result["claims"]:
        assert "not_understood" in entry
        if entry["claim_id"] in _ADOPTED_NOT_UNDERSTOOD:
            assert entry["not_understood"] == \
                _ADOPTED_NOT_UNDERSTOOD[entry["claim_id"]]
            assert entry["not_understood_recorded"] is True
        else:
            assert entry["not_understood"] is None
            assert entry["not_understood_recorded"] is False
        assert "bundle" in entry
        assert entry["bundle"] is None
        assert entry["bundle_serialization_error"] is None
        # Lane separation at the serialization layer: stage stays a
        # distinct object; no score keys leak into it.
        assert isinstance(entry["stage"], dict)
        assert "propagated_score" not in entry["stage"]
        assert "band" not in entry["stage"]


def test_live_claims_with_aee_keep_score_out_of_stage_object():
    if not _CLAIMS_DIR.exists():
        pytest.skip("extracted_claims dir not present")
    result = asyncio.run(indus_evidence.list_claims(limit=5, aee=True))
    for entry in result["claims"]:
        score = entry["lane1_score"]
        assert score is not None
        assert "propagated_score" in score
        assert "band" in score
        # The retained per-claim score object is lane-1 only.
        assert entry["aee_score"] == score
        assert "stage" not in score


# ── E2.3/E2.4: synthetic records (authored text + contested bundle) ──────


def _plain_claim(**extra) -> dict:
    claim = with_stage_defaults({
        "claim_id": "synthetic-plain-001",
        "source_document_id": "synthetic_doc",
        "claim_type": "sign_value_claim",
        "normalized_claim": "Synthetic claim: sign value test.",
        "claim_status": "untested",
        "falsification_condition": "A synthetic counter-observation defeats it.",
    })
    claim.update(extra)
    return claim


def _contested_bundle_parent() -> dict:
    search_record = {
        "corpora_searched": ["synthetic-corpus-a"],
        "literature_searched": ["synthetic-bibliography-b"],
        "searched_on": "2026-10-01",
        "searcher": "Synthetic Searcher",
    }
    contest = {
        "contested_by": "Synthetic Contester",
        "evidence": ["https://example.org/rival-attribution"],
        "contested_on": "2026-10-05",
    }
    subs = []
    for kind in SUBCLAIM_KINDS:
        if kind == "attribution":
            subs.append(make_attribution_subclaim(
                "synthetic-sub-attribution",
                proposition="All prior readings of this synthetic sign are accounted for.",
                evidence=REFS,
                falsification_condition="A prior reading absent from prior_readings defeats it.",
                prior_readings=[{"citation": "https://example.org/prior-reading"}],
                search_record=search_record,
                contest_state="contested",
                contest_record=contest,
                stage="checked",
                timestamp=TS,
            ))
        else:
            subs.append(make_subclaim(
                kind, f"synthetic-sub-{kind}",
                proposition=f"Synthetic proposition for {kind}.",
                evidence=REFS,
                falsification_condition=f"A synthetic falsifier for {kind}.",
                stage="explained", timestamp=TS,
            ))
    parent = with_stage_defaults({
        "claim_id": "synthetic-bundle-001",
        "source_document_id": "synthetic_doc",
        "claim_type": "sign_value_claim",
        "normalized_claim": "Synthetic bundle parent claim.",
        "claim_status": "partially_supported",
        "not_understood": AUTHORED_NOT_UNDERSTOOD,
    })
    return make_bundle(parent, subs, timestamp=TS)


def test_synthetic_store_serializes_authored_not_understood_and_contest(tmp_path, monkeypatch):
    claims_dir = tmp_path / "extracted_claims"
    _write_claims_file(claims_dir, [_plain_claim(), _contested_bundle_parent()])
    result = _run_list_claims(monkeypatch, claims_dir, limit=50)
    by_id = {c["claim_id"]: c for c in result["claims"]}

    plain = by_id["synthetic-plain-001"]
    assert plain["not_understood"] is None
    assert plain["not_understood_recorded"] is False
    assert plain["bundle"] is None

    parent = by_id["synthetic-bundle-001"]
    # The record's own authored statement travels verbatim.
    assert parent["not_understood"] == AUTHORED_NOT_UNDERSTOOD
    assert parent["not_understood_recorded"] is True

    # E2.2: the contest renders on the parent serialization.
    bundle = parent["bundle"]
    assert bundle is not None
    assert bundle["attribution_contested"] is True
    assert bundle["contested"] is True
    assert bundle["contest_record"]["contested_by"] == "Synthetic Contester"
    assert bundle["contest_record"]["contested_on"] == "2026-10-05"
    # OD-3: the cap is visible in the parent-stage computation and
    # the computed stage is capped at checked.
    assert bundle["stage_computation"]["stage"] == "checked"
    assert any(
        cap.startswith("od3-contested-attribution-caps-at-checked")
        for cap in bundle["stage_computation"]["caps_applied"]
    )
    attribution = next(s for s in bundle["sub_claims"] if s["kind"] == "attribution")
    assert attribution["contest_state"] == "contested"
    assert attribution["attribution_contested"] is True


# ── E2.1/E2.5: frontend source guards on the touched surfaces ────────────

STAGE_NAMES = ("created", "checked", "explained", "accepted", "digested")
#: Warmer renames OD-4 forbids as stage labels. ``verified_unexplained``
#: is the governed FR-029-03 flag name, not a stage label — it is
#: stripped before scanning.
STAGE_SYNONYMS = ("verified", "proven", "confirmed")


def _synonym_scan(source: str) -> str:
    return source.replace("verified_unexplained", "").lower()


def test_legend_carries_the_five_stage_names_verbatim():
    source = _LEGEND.read_text(encoding="utf-8")
    for name in STAGE_NAMES:
        assert f'"{name}"' in source, name
    # The never-settles line of the OD-4 legend.
    assert "never settle a claim" in source
    # The absence form for unauthored not_understood.
    assert "not yet recorded" in source
    assert "no machine-generated text is substituted" in source


def test_touched_surfaces_have_no_stage_synonyms():
    for path in (_LEGEND, _EVIDENCE_VIEW, _PANEL):
        scanned = _synonym_scan(path.read_text(encoding="utf-8"))
        for synonym in STAGE_SYNONYMS:
            assert synonym not in scanned, f"{synonym} in {path.name}"


def test_evidence_view_renders_two_labelled_lane_regions():
    source = _EVIDENCE_VIEW.read_text(encoding="utf-8")
    assert 'data-testid="lane1-region"' in source
    assert 'data-testid="lane2-region"' in source
    assert "Lane 1 — machine-speed verification (checking only)" in source
    assert "Lane 2 — human-paced settlement" in source
    # The legend renders on this surface.
    assert "StageLegend" in source
    # Lane-1 badges lost their per-status colours (FR-029-10).
    assert "STATUS_COLORS" not in source
    # The score renders inside the lane-1 region with method context.
    assert "AEE library scoring" in source
    # The retained score is never in a summary/headline position here.
    assert "mean_propagated_score" not in source


def test_panel_leads_with_standing_position_and_stage_summary():
    source = _PANEL.read_text(encoding="utf-8")
    assert 'data-testid="standing-position"' in source
    assert "The Indus script is not deciphered" in source
    assert 'data-testid="stage-summary"' in source
    assert "by_stage" in source
    assert "StageLegend" in source
    # E1's withdrawals stay withdrawn on this surface.
    for withdrawn in ("signs deciphered", "Signs Deciphered", "SA Confidence",
                      "Seals Decoded", "Inscriptions Fully Decoded",
                      "Weighted Confidence", "Deciphered signs"):
        assert withdrawn not in source, withdrawn
