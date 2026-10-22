"""Tests for the paper-search client + RESEARCH-CHECK stage (spec 025).

Offline only: the MCP server is stubbed. Live behaviour is covered by
the smoke record in specs/025-paper-search-research-check/smoke/.
"""
from __future__ import annotations

import json

import pytest

from glossa_lab import paper_search, research_check


# ── Client ───────────────────────────────────────────────────────────

def test_server_python_default_and_override(monkeypatch):
    monkeypatch.delenv("GLOSSA_PAPER_SEARCH_PYTHON", raising=False)
    assert paper_search.server_python().endswith(
        "venvs/paper-search-mcp/bin/python")
    monkeypatch.setenv("GLOSSA_PAPER_SEARCH_PYTHON", "/x/y/python")
    assert paper_search.server_python() == "/x/y/python"


def test_no_proxy_is_sanitized():
    params = paper_search._params()
    assert params.env["NO_PROXY"] == "localhost,127.0.0.1,::1"
    assert params.args == ["-m", "paper_search_mcp.server"]


def test_scihub_refusal_is_hard(monkeypatch):
    called = []
    monkeypatch.setattr(paper_search, "call_tool",
                        lambda *a, **k: called.append((a, k)) or {})
    with pytest.raises(ValueError, match="hard-off"):
        paper_search._guarded_read(
            "download_with_fallback",
            {"source": "core", "paper_id": "1", "use_scihub": True},
            timeout=10)
    assert called == []  # refusal happens before any server call


def test_scihub_flag_stripped_when_false(monkeypatch):
    seen = {}
    monkeypatch.setattr(paper_search, "call_tool",
                        lambda tool, args, timeout=0: seen.update(args) or
                        {"tool": tool, "is_error": False, "result": {}})
    paper_search._guarded_read("download_with_fallback",
                               {"source": "core", "use_scihub": False},
                               timeout=10)
    assert "use_scihub" not in seen


# ── Stage: phrasing plan ─────────────────────────────────────────────

def test_phrasings_claim_plus_mechanical():
    ph = research_check.build_phrasings(
        "Indus script sign frequencies follow a Zipf law.")
    assert len(ph) >= 2
    assert ph[0]["origin"] == "claim"
    assert ph[1]["origin"] == "mechanical"


def test_phrasings_caller_supplied_wins_over_mechanical():
    ph = research_check.build_phrasings(
        "Some claim.", alt_phrasings=["a stranger's phrasing"])
    assert [p["origin"] for p in ph] == ["claim", "caller"]


# ── Stage: record shaping against a stub client ──────────────────────

class StubClient:
    DEFAULT_SOURCES = paper_search.DEFAULT_SOURCES

    def __init__(self):
        self.calls = []

    def search_papers(self, query, sources="", max_results=10, timeout=0):
        self.calls.append(("search_papers", query))
        return {"tool": "search_papers", "is_error": False, "result": {
            "papers": [{
                "title": "Statistical analysis of the Indus script "
                         "using n-grams",
                "authors": ["Yadav et al."], "year": 2009,
                "doi": "", "paper_id": "0907.1117", "source": "arxiv",
            }],
            "errors": {"openalex": "HTTP 429"},
        }}

    def search_source(self, source, query, max_results=10, timeout=0):
        self.calls.append((f"search_{source}", query))
        return {"tool": f"search_{source}", "is_error": False,
                "result": {"papers": []}}

    def call_tool(self, tool, args, timeout=0):
        self.calls.append((tool, args.get("paper_id")))
        return {"tool": tool, "is_error": False,
                "result": "Full text. " * 50}

    def resolve_doi(self, doi, timeout=0):
        self.calls.append(("resolve_doi", doi))
        return {"tool": "get_crossref_paper_by_doi", "is_error": False,
                "result": {"title": "Entropic evidence for linguistic "
                                    "structure in the Indus script",
                           "authors": ["Rao et al."], "year": 2009,
                           "venue": "Science"}}


CLAIM = {
    "claim_id": "c1",
    "source_document_id": "doc1",
    "normalized_claim": "Indus script sign frequencies follow a Zipf law.",
}


def test_record_is_advisory_and_complete():
    stub = StubClient()
    rec = research_check.run_research_check(
        CLAIM, dois=["10.1126/science.1170391"], client=stub)
    assert rec["verdict"] is None and rec["advisory"] is True
    assert rec["stage"] == "research_check"
    assert len(rec["phrasings"]) >= 2
    # >= 2 phrasings x (federated + arxiv + crossref) queries ran
    assert len(rec["queries"]) >= 6
    assert {q["tool"] for q in rec["queries"]} >= {
        "search_papers", "search_arxiv", "search_crossref"}
    # federated per-source failure is surfaced, not swallowed
    assert any("openalex" in str(e.get("where")) or
               "openalex" in str(e.get("error"))
               for e in rec["source_errors"])
    # neighbor merged once, full text read via the arXiv route
    assert len(rec["neighbors"]) == 1
    assert rec["neighbors_read_full_text"][0]["paper_id"] == "0907.1117"
    # DOI resolved into a citation check
    assert rec["citation_checks"][0]["resolved"]["venue"] == "Science"
    # the claim dict itself was not mutated with any status/score
    assert "claim_status" not in CLAIM and "score" not in CLAIM


def test_no_neighbors_is_a_gap_not_a_negative():
    class EmptyStub(StubClient):
        def search_papers(self, query, sources="", max_results=10,
                          timeout=0):
            return {"tool": "search_papers", "is_error": False,
                    "result": {"papers": [], "errors": {}}}

    rec = research_check.run_research_check(CLAIM, client=EmptyStub())
    assert rec["neighbors"] == []
    assert any("not evidence of no prior art" in str(g)
               for g in rec["gaps"])


def test_result_papers_handles_double_encoded_payload():
    payload = json.dumps([{"title": "T", "paper_id": "0901.3017"}])
    out = {"tool": "search_arxiv", "is_error": False, "result": payload}
    papers = research_check._result_papers(out)
    assert papers and papers[0]["paper_id"] == "0901.3017"


def test_write_record_sidecar(tmp_path):
    rec = research_check.run_research_check(CLAIM, client=StubClient())
    path = research_check.write_record(rec, tmp_path)
    assert path.name == "doc1__c1.research_check.json"
    assert '"verdict": null' in path.read_text(encoding="utf-8")
