"""Tests for the CORE client + its RESEARCH-CHECK source (spec 026).

Offline only: HTTP is faked at the urllib opener and the surrogate
is stubbed. Live behaviour is covered by the smoke record in
specs/026-core-research-source/smoke/.
"""
from __future__ import annotations

import io
import json
import urllib.error
import urllib.request

import pytest

from glossa_lab import core_search, research_check


# ── Fakes ────────────────────────────────────────────────────────────

class FakeResponse:
    def __init__(self, payload: dict):
        self._buf = io.BytesIO(json.dumps(payload).encode())

    def read(self, n: int = -1) -> bytes:
        return self._buf.read(n)

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


class FakeOpener:
    """Records requests; answers with a payload or raises `error`."""

    def __init__(self, payload=None, error: Exception | None = None):
        self.payload = payload or {"totalHits": 0, "results": []}
        self.error = error
        self.requests: list[urllib.request.Request] = []

    def open(self, request, timeout=None):
        self.requests.append(request)
        if self.error is not None:
            raise self.error
        return FakeResponse(self.payload)


@pytest.fixture
def fake_http(monkeypatch):
    """Stub the surrogate + opener; returns the FakeOpener in play."""
    state = {"opener": FakeOpener()}

    def fake_surrogate(request, credential_name, *, allowed_hosts):
        assert credential_name == "custom.core"
        assert allowed_hosts == ["api.core.ac.uk"]
        request.add_header("Authorization", "Bearer hsurr:test-token")

    monkeypatch.setattr(core_search, "add_surrogate_to_request",
                        fake_surrogate)
    monkeypatch.setattr(core_search, "MIN_INTERVAL_SECONDS", 0.0)
    monkeypatch.setattr(urllib.request, "build_opener",
                        lambda *a, **k: state["opener"])
    return state


def http_error(code: int, body: bytes = b"boom") -> urllib.error.HTTPError:
    return urllib.error.HTTPError(
        "https://api.core.ac.uk/v3/search/works/", code, "err", {},
        io.BytesIO(body))


# ── Client: request shape ────────────────────────────────────────────

def test_search_uses_slashed_path_and_bearer_surrogate(fake_http):
    fake_http["opener"].payload = {
        "totalHits": 1,
        "results": [{"id": 7, "title": "T", "authors": [],
                     "yearPublished": 2009, "doi": None,
                     "abstract": None, "fullText": None}],
    }
    out = core_search.search_works("Indus script decipherment", limit=5)
    assert out["totalHits"] == 1
    req = fake_http["opener"].requests[0]
    assert req.full_url.startswith(
        "https://api.core.ac.uk/v3/search/works/?")
    assert "q=Indus+script+decipherment" in req.full_url
    assert "limit=5" in req.full_url
    assert req.headers.get("Authorization") == "Bearer hsurr:test-token"


def test_get_work_path(fake_http):
    core_search.get_work("https://api.core.ac.uk/v3/works/4242")
    req = fake_http["opener"].requests[0]
    assert req.full_url == "https://api.core.ac.uk/v3/works/4242"


def test_redirect_is_refused():
    handler = core_search._NoRedirect()
    with pytest.raises(core_search.CoreError, match="redirect refused"):
        handler.redirect_request(None, None, None, None, None, None)


# ── Client: errors and the 429 hard stop ─────────────────────────────

def test_429_raises_ratelimit_and_never_retries(fake_http):
    fake_http["opener"] = FakeOpener(error=http_error(429, b"slow down"))
    with pytest.raises(core_search.CoreRateLimitError):
        core_search.search_works("anything")
    assert len(fake_http["opener"].requests) == 1  # no retry-loop


def test_500_is_a_plain_core_error(fake_http):
    fake_http["opener"] = FakeOpener(error=http_error(500))
    with pytest.raises(core_search.CoreError) as excinfo:
        core_search.search_works("anything")
    assert not isinstance(excinfo.value, core_search.CoreRateLimitError)


# ── Client: pacing ───────────────────────────────────────────────────

def test_pace_guard_sleeps_only_the_shortfall(monkeypatch):
    sleeps: list[float] = []
    monkeypatch.setattr(core_search.time, "sleep", sleeps.append)
    monkeypatch.setattr(core_search, "MIN_INTERVAL_SECONDS", 2.1)
    core_search._last_call_at = 100.0
    core_search._pace(now=101.0)
    assert sleeps == [pytest.approx(1.1)]
    assert core_search._last_call_at == pytest.approx(102.1)
    core_search._pace(now=200.0)
    assert len(sleeps) == 1  # already past the interval: no sleep


# ── Client: normalization ────────────────────────────────────────────

def test_normalize_work_maps_stage_shape():
    paper = core_search.normalize_work({
        "id": 777,
        "title": "Sign frequencies in the Indus script",
        "authors": [{"displayName": "N. Yadav"}, {"displayName": "M. Vahia"}],
        "yearPublished": 2011,
        "doi": "https://doi.org/10.1000/xyz123",
        "abstract": "We study sign frequencies.",
        "fullText": "full text body",
        "downloadUrl": "https://example.org/paper.pdf",
    })
    assert paper["source"] == "core"
    assert paper["paper_id"] == "core:777"
    assert paper["authors"] == ["N. Yadav", "M. Vahia"]
    assert paper["year"] == 2011
    assert paper["doi"] == "10.1000/xyz123"
    assert paper["has_full_text"] is True
    assert paper["full_text"] == "full text body"


def test_normalize_work_without_full_text():
    paper = core_search.normalize_work({
        "id": 3, "title": "Metadata only", "authors": [],
        "yearPublished": None, "doi": None, "abstract": None,
        "fullText": None,
    })
    assert paper["has_full_text"] is False
    assert paper["full_text"] is None
    assert paper["doi"] is None


# ── Stage: CORE as a source (stub clients) ───────────────────────────

class StubMcpClient:
    DEFAULT_SOURCES = "arxiv,crossref"

    def search_papers(self, query, sources="", max_results=10, timeout=0):
        return {"tool": "search_papers", "is_error": False,
                "result": {"papers": [], "errors": {}}}

    def search_source(self, source, query, max_results=10, timeout=0):
        return {"tool": f"search_{source}", "is_error": False,
                "result": {"papers": []}}

    def call_tool(self, tool, args, timeout=0):
        return {"tool": tool, "is_error": False, "result": ""}

    def resolve_doi(self, doi, timeout=0):
        return {"tool": "get_crossref_paper_by_doi", "is_error": False,
                "result": {}}


class StubCoreClient:
    def __init__(self):
        self.queries: list[str] = []

    def search_papers(self, query, limit=10, timeout=0):
        self.queries.append(query)
        return [{
            "title": "Sign frequencies in the Indus script follow "
                     "a Zipf distribution",
            "authors": ["N. Yadav"], "year": 2011, "doi": None,
            "paper_id": "core:777", "source": "core", "url": None,
            "abstract": "Indus script sign frequencies and the Zipf "
                        "law are studied.",
            "has_full_text": True,
            "full_text": "Indus script sign frequencies Zipf law " * 20,
        }]


CLAIM = {
    "claim_id": "c1",
    "source_document_id": "doc1",
    "normalized_claim": "Indus script sign frequencies follow a Zipf law.",
}


def test_stage_merges_core_hits_and_reads_core_full_text():
    core = StubCoreClient()
    rec = research_check.run_research_check(
        CLAIM, client=StubMcpClient(), core_client=core)
    assert rec["verdict"] is None and rec["advisory"] is True
    # one CORE query per phrasing (>= 2 phrasings)
    core_queries = [q for q in rec["queries"]
                    if q["tool"] == "core_search_works"]
    assert len(core_queries) == len(core.queries) >= 2
    # the CORE hit joined the pool under source "core"
    assert len(rec["neighbors"]) == 1
    nb = rec["neighbors"][0]
    assert nb["source"] == "core" and nb["has_full_text"] is True
    assert nb["relevance"] >= research_check.MIN_READ_RELEVANCE
    # and its carried full text was recorded as a read from CORE
    reads = rec["neighbors_read_full_text"]
    assert len(reads) == 1
    assert reads[0]["source"] == "core"
    assert reads[0]["paper_id"] == "core:777"
    assert reads[0]["words"] == 120
    # the raw text itself is never written into the record
    assert all("full_text" not in nb for nb in rec["neighbors"])
    assert all("full_text" not in r
               for r in rec["neighbors_read_full_text"])


def test_stage_core_429_stops_core_for_the_run():
    class Core429:
        def __init__(self):
            self.calls = 0

        def search_papers(self, query, limit=10, timeout=0):
            self.calls += 1
            raise core_search.CoreRateLimitError("HTTP 429 from CORE")

    core = Core429()
    rec = research_check.run_research_check(
        CLAIM, client=StubMcpClient(), core_client=core)
    assert core.calls == 1  # stopped after the first phrasing
    assert any(e.get("type") == "RateLimit" for e in rec["source_errors"])
    assert any("CORE stopped for this run" in str(g) for g in rec["gaps"])
    assert rec["verdict"] is None


def test_stage_core_disabled_by_flag():
    core = StubCoreClient()
    rec = research_check.run_research_check(
        CLAIM, client=StubMcpClient(), core_client=core, use_core=False)
    assert core.queries == []
    assert not any(q["tool"] == "core_search_works"
                   for q in rec["queries"])
