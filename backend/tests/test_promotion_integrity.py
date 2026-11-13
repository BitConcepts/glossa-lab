"""Acceptance-path promotion-integrity regression tests (2026-11-13).

The 2026-11-13 acceptance-path test of the automated research loop
(probes against a scratch backend only; report in the glossa-run
working records) found three promotion defects in
POST /api/v1/research-loop/staging/promote, plus a reporting defect:

- Defect 3 (probe (d)): a grapheme that exists in no corpus and no
  register (ZZZ904, "phantom-grapheme") was promoted to a MEDIUM
  anchor. Promotion now requires membership in the anchor register
  or the pinned corpus snapshot's canonical grapheme inventory —
  the same dual-source rule as anchor-set creation — and fails
  closed when membership cannot be verified.
- Defect 4 (probe (c)): only HIGH/MEDIUM anchors were protected
  from overwrite; LOW anchor M252's reading was silently replaced
  and its confidence raised. No existing anchor of ANY confidence
  may be overwritten or mutated by promotion now.
- Defect 2, bug part (probe (b)): the promote request itself could
  supply the H26 evidence reference (evidence_refs map) for a
  candidate whose record carried none — README.md was accepted as
  a self-referential candidate's "evidence". Promotion now uses
  only the reference recorded on the candidate record; a request
  reference that differs from the recorded one refuses the sign.
- Minor (probe, promote-readme-refs call): the response reported
  new_coverage 0.0 / coverage_delta -0.9219 when the corpus CSV
  was unavailable, i.e. a measured-looking collapse that never
  happened (the stored value was guarded). Unavailable coverage
  is now reported as null.
"""
from __future__ import annotations

import json

import pytest
from fastapi.testclient import TestClient

from glossa_lab.api import research_loop as rl
from glossa_lab.main import create_app

BASE = "/api/v1/research-loop"

_REGISTER = {
    "total": 4, "corpus_token_coverage": 0.5,
    "anchors": {
        "M001": {"reading": "a", "confidence": "HIGH",
                 "basis": "b", "source": "s"},
        "M252": {"reading": "min", "confidence": "LOW",
                 "basis": "b", "source": "s"},
        "M342": {"reading": "fish-orig", "confidence": "HIGH",
                 "basis": "b", "source": "s"},
        "M400": {"reading": "an-orig", "confidence": "CANDIDATE",
                 "basis": "b", "source": "s"},
    },
}

# Bare inventory forms: "777" is a corpus sign with no anchor yet
# (the promotable positive control); 342/252/001 mirror the register.
_SNAPSHOT_RECORDS = [
    {"canonical_grapheme_ids": ["342", "252", "001"]},
    {"canonical_grapheme_ids": ["777", "100"]},
]


@pytest.fixture()
def promote_env(tmp_path, monkeypatch):
    staging = tmp_path / "anchor_staging.json"
    archive = tmp_path / "anchor_staging_archive.json"
    anchors = tmp_path / "INDUS_FINAL_ANCHORS.json"
    snapshot = tmp_path / "indus_research.jsonl"
    staging.write_text("[]", encoding="utf-8")
    archive.write_text("[]", encoding="utf-8")
    anchors.write_text(json.dumps(_REGISTER), encoding="utf-8")
    snapshot.write_text(
        "".join(json.dumps(r) + "\n" for r in _SNAPSHOT_RECORDS),
        encoding="utf-8")
    monkeypatch.setattr(rl, "_STAGING_JSON", staging)
    monkeypatch.setattr(rl, "_ARCHIVE_JSON", archive)
    monkeypatch.setattr(rl, "_FA_PATH", anchors)
    monkeypatch.setattr(rl, "_CORPUS_SNAPSHOT", snapshot, raising=False)
    monkeypatch.setattr(rl, "_CORPUS_GRAPHEMES", None, raising=False)
    return {"staging": staging, "archive": archive, "anchors": anchors}


@pytest.fixture()
def client():
    return TestClient(create_app())


def _candidate(**over):
    c = {"sign": "M777", "proposed_reading": "test-reading",
         "review_status": "verified", "evidence_score": 0.99,
         "evidence_type": "positional_profile",
         "source_experiment": "unit-test",
         "evidence_ref": "LEDGER.md"}
    c.update(over)
    return c


def _promote(client, promote_env, candidates, body=None):
    promote_env["archive"].write_text(
        json.dumps(candidates), encoding="utf-8")
    r = client.post(f"{BASE}/staging/promote", json=body or {})
    assert r.status_code == 200
    return r.json()


def _anchors(promote_env):
    return json.loads(promote_env["anchors"].read_text(encoding="utf-8"))


# ── Defect 3: corpus membership is a promotion precondition ────────────────

def test_phantom_grapheme_refused_at_promote(client, promote_env):
    """Probe (d): ZZZ904 exists in no corpus and no register; even
    with a resolving recorded evidence ref it must not promote."""
    before = promote_env["anchors"].read_text(encoding="utf-8")
    data = _promote(client, promote_env, [
        _candidate(sign="ZZZ904", proposed_reading="phantom-grapheme")])
    assert data["promoted"] == 0
    assert data["blocked_unknown_grapheme"] == ["ZZZ904"]
    assert promote_env["anchors"].read_text(encoding="utf-8") == before
    assert "ZZZ904" not in _anchors(promote_env)["anchors"]


def test_corpus_only_grapheme_promotes(client, promote_env):
    """Positive control: M777 is in no register, but its bare form
    777 is in the pinned corpus inventory (M777 == 777), so with a
    recorded evidence ref it promotes."""
    data = _promote(client, promote_env, [_candidate()])
    assert data["promoted"] == 1
    assert data["blocked_unknown_grapheme"] == []
    anchors = _anchors(promote_env)["anchors"]
    assert anchors["M777"]["reading"] == "test-reading"
    assert anchors["M777"]["confidence"] == "MEDIUM"


# ── Defect 4: no existing anchor is overwritten, at any confidence ────────

def test_low_anchor_never_overwritten(client, promote_env):
    """Probe (c): LOW anchor M252's reading was silently replaced
    and its confidence raised to MEDIUM."""
    data = _promote(client, promote_env, [
        _candidate(sign="M252",
                   proposed_reading="PROBE-OVERWRITE-LOW")])
    assert data["promoted"] == 0
    assert data["skipped"] == 1
    assert data["promotable"] == 0
    assert _anchors(promote_env)["anchors"]["M252"] == {
        "reading": "min", "confidence": "LOW", "basis": "b", "source": "s"}


def test_candidate_anchor_never_overwritten(client, promote_env):
    """CANDIDATE anchors (113 of the 287) were equally unprotected."""
    data = _promote(client, promote_env, [
        _candidate(sign="M400", proposed_reading="PROBE-OVERWRITE-CAND")])
    assert data["promoted"] == 0
    assert data["skipped"] == 1
    assert _anchors(promote_env)["anchors"]["M400"]["reading"] == "an-orig"
    assert _anchors(promote_env)["anchors"]["M400"]["confidence"] == "CANDIDATE"


def test_bare_form_of_registered_sign_is_skipped(client, promote_env):
    """M252 == 252: a candidate in the register's bare form is the
    same sign, so it is skipped as already anchored and no second
    entry is created under the bare key."""
    data = _promote(client, promote_env, [
        _candidate(sign="252", proposed_reading="PROBE-BARE-FORM")])
    assert data["promoted"] == 0
    assert data["skipped"] == 1
    anchors = _anchors(promote_env)["anchors"]
    assert "252" not in anchors
    assert anchors["M252"]["reading"] == "min"


def test_high_anchor_still_skipped(client, promote_env):
    """Guard-rail (held pre-fix): HIGH anchors were already safe."""
    data = _promote(client, promote_env, [
        _candidate(sign="M342", proposed_reading="PROBE-OVERWRITE-HIGH")])
    assert data["promoted"] == 0
    assert data["skipped"] == 1
    assert _anchors(promote_env)["anchors"]["M342"]["reading"] == "fish-orig"


# ── Defect 2 (bug part): the request may not supply the evidence ──────────

def test_request_supplied_ref_refused_when_candidate_has_none(
        client, promote_env):
    """Probe (b): candidate with NO recorded ref + request-supplied
    evidence_refs README.md promoted a self-referential candidate.
    The request may not supply the evidence: refuse the sign."""
    cand = _candidate()
    del cand["evidence_ref"]
    before = promote_env["anchors"].read_text(encoding="utf-8")
    data = _promote(client, promote_env, [cand],
                    body={"evidence_refs": {"M777": "README.md"}})
    assert data["promoted"] == 0
    assert data["blocked_evidence_mismatch"] == ["M777"]
    assert promote_env["anchors"].read_text(encoding="utf-8") == before


def test_request_supplied_ref_refused_when_it_conflicts(
        client, promote_env):
    """A request ref that differs from the candidate's recorded ref
    refuses the sign (the recorded ref governs, not the request)."""
    data = _promote(client, promote_env, [_candidate()],
                    body={"evidence_refs": {"M777": "README.md"}})
    assert data["promoted"] == 0
    assert data["blocked_evidence_mismatch"] == ["M777"]
    assert "M777" not in _anchors(promote_env)["anchors"]


def test_request_ref_echoing_recorded_ref_is_accepted(
        client, promote_env):
    """A request ref identical to the recorded ref is a no-op echo,
    not a supply: promotion proceeds on the recorded ref."""
    data = _promote(client, promote_env, [_candidate()],
                    body={"evidence_refs": {"M777": "LEDGER.md"}})
    assert data["promoted"] == 1
    assert data["blocked_evidence_mismatch"] == []


# ── Minor: unavailable coverage is reported as unavailable ────────────────

def test_coverage_reported_unavailable_not_zero(client, promote_env):
    """The Holdat CSV is not tracked, so in this environment (as in
    CI) the recalculation cannot run: the response must report
    new_coverage / coverage_delta as null, never a measured-looking
    0.0, and the stored coverage must stay untouched."""
    data = _promote(client, promote_env, [_candidate()])
    assert data["promoted"] == 1
    assert data["prev_coverage"] == 0.5
    assert data["new_coverage"] is None
    assert data["coverage_delta"] is None
    assert _anchors(promote_env)["corpus_token_coverage"] == 0.5


def test_recalc_corpus_coverage_unavailable_returns_none(
        tmp_path, monkeypatch):
    """Unit leg: with the corpus CSV path pointing at a file that
    does not exist, the recalculation reports unavailable (None),
    not 0.0."""
    import glossa_lab.config as config

    class _Cfg:
        def corpus_csv_path(self):
            return tmp_path / "absent-corpus.csv"

    monkeypatch.setattr(config, "get_project_config", lambda: _Cfg())
    assert rl._recalc_corpus_coverage({}) is None
