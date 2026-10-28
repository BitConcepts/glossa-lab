"""RESEARCH-CHECK stage: prior-art and citation audit for claim dossiers.

Runs BEFORE AEE scoring / adjudication of a claim and attaches an
advisory audit record to the dossier. Design and protocol:
``specs/025-paper-search-research-check/`` and
``docs/paper-search-mcp.md`` (the audit protocol there is binding).

What the stage does, per claim:
  * searches the claim's concept in at least two phrasings (the
    claim's own words plus caller-supplied or mechanically derived
    phrasing, each marked with its origin) across at least two
    independent scholarly sources via the paper-search MCP client
    (``glossa_lab.paper_search``);
  * resolves every supplied DOI through Crossref and records the
    returned metadata for comparison against the citing text;
  * surfaces nearest neighbors from the merged results and reads the
    full text of reachable open-access neighbors (arXiv route);
    neighbors whose full text cannot be reached are recorded as
    open gaps — never as "no prior art";
  * additionally queries CORE per phrasing through the keyed client
    (``glossa_lab.core_search``, spec 026): CORE hits join the same
    neighbor pool, and a CORE hit that carries full text is its own
    read source. A CORE 429 stops CORE for the rest of the run and
    is recorded, per the connector's stop rule.

What it never does: score a claim, change a claim's status, or
adjudicate a decipherment. The record's ``verdict`` field is always
``None``; AEE scoring stays with ``glossa_lab.aee_core`` and
adjudication with the program's recorded gates. The claim file
itself is never modified — records are sidecars under
``glossa-indus/claims/research_checks/``.

CLI:
  python -m glossa_lab.research_check --claim-file <dossier.json>
      [--claim-id ID] [--alt-phrasing "..."] [--doi DOI ...]
      [--out DIR] [--no-full-text] [--no-core] [--timeout SECONDS]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from glossa_lab import core_search, paper_search

_REPO = Path(__file__).resolve().parent.parent.parent
DEFAULT_OUT_DIR = _REPO / "glossa-indus" / "claims" / "research_checks"
PROTOCOL_REF = "docs/paper-search-mcp.md#audit-protocol"

# Sources queried per phrasing, beyond the federated call: the two
# routes measured most reliable for concept queries (protocol rule 1:
# the per-source concept query is the reliable route; the federated
# call is kept for its visible per-source error reporting).
PER_SOURCE_ROUTES = ("arxiv", "crossref")

_STOPWORDS = {
    "the", "a", "an", "of", "in", "on", "for", "and", "or", "to", "is",
    "are", "was", "were", "with", "by", "from", "that", "this", "it",
    "its", "as", "at", "be", "been", "has", "have", "had", "not", "no",
}


def mechanical_phrasing(statement: str) -> str:
    """Keyword-reduced phrasing: content words only, order preserved.

    A deliberately dumb second phrasing (protocol rule 1: a stranger's
    words). Marked origin='mechanical' in every record so nobody
    mistakes it for a considered reformulation.
    """
    words = re.findall(r"[A-Za-z0-9][A-Za-z0-9\-']*", statement)
    kept = [w for w in words if w.lower() not in _STOPWORDS]
    return " ".join(kept[:14]) or statement


def build_phrasings(statement: str,
                    alt_phrasings: list[str] | None = None
                    ) -> list[dict[str, str]]:
    """At least two phrasings: the claim's words first, then supplied
    alternatives, then a mechanical reduction if still short."""
    out = [{"text": statement, "origin": "claim"}]
    for alt in alt_phrasings or []:
        if alt and alt != statement:
            out.append({"text": alt, "origin": "caller"})
    if len(out) < 2:
        mech = mechanical_phrasing(statement)
        if mech != statement:
            out.append({"text": mech, "origin": "mechanical"})
    return out


def _paper_key(paper: dict[str, Any]) -> str:
    doi = (paper.get("doi") or "").strip().lower()
    if doi:
        return f"doi:{doi}"
    title = re.sub(r"\s+", " ", (paper.get("title") or "")).strip().lower()
    return f"title:{title}"


def _neighbor(paper: dict[str, Any]) -> dict[str, Any]:
    return {
        "title": paper.get("title"),
        "authors": paper.get("authors"),
        "year": paper.get("year") or paper.get("published_date"),
        "doi": paper.get("doi"),
        "paper_id": paper.get("paper_id") or paper.get("id"),
        "source": paper.get("source"),
        "url": paper.get("url") or paper.get("pdf_url"),
        "abstract": (paper.get("abstract") or "")[:600] or None,
    }


def _content_words(text: str) -> set[str]:
    return {w.lower() for w in re.findall(r"[A-Za-z][A-Za-z0-9\-']*", text)
            if w.lower() not in _STOPWORDS and len(w) > 2}


def _relevance(claim_statement: str, paper: dict[str, Any]) -> float:
    """Share of the claim's content words appearing in the paper's
    title+abstract. A surfacing heuristic only — it ranks neighbors
    and gates the expensive full-text reads; it never removes a
    neighbor from the record and never judges the claim."""
    words = _content_words(claim_statement)
    if not words:
        return 0.0
    hay = _content_words(f"{paper.get('title') or ''} "
                         f"{paper.get('abstract') or ''}")
    return round(len(words & hay) / len(words), 3)


# Full-text reads are minutes each; only spend them on neighbors that
# share real vocabulary with the claim. Measured reason (spec 025
# smoke): the arXiv connector answers a no-match conjunction with a
# default high-profile list (ATLAS, gravitational-wave papers) rather
# than an empty result — unranked, those consumed every read slot.
MIN_READ_RELEVANCE = 0.1


def _result_papers(out: dict[str, Any]) -> list[dict[str, Any]]:
    """Extract a paper list from a client call result, whatever shape."""
    if not isinstance(out, dict) or "error" in out and "result" not in out:
        return []
    res = out.get("result", out)
    if isinstance(res, str):  # defensive: double-encoded payloads
        try:
            res = json.loads(res)
        except (json.JSONDecodeError, TypeError):
            return []
    if isinstance(res, dict):
        for key in ("papers", "results", "items"):
            if isinstance(res.get(key), list):
                return [p for p in res[key] if isinstance(p, dict)]
    if isinstance(res, list):
        return [p for p in res if isinstance(p, dict)]
    return []


def run_research_check(
    claim: dict[str, Any],
    *,
    document_id: str = "",
    alt_phrasings: list[str] | None = None,
    dois: list[str] | None = None,
    sources: str = paper_search.DEFAULT_SOURCES,
    max_results: int = 10,
    read_neighbors: bool = True,
    neighbor_limit: int = 3,
    download_dir: Path | None = None,
    timeout: float = paper_search.DEFAULT_TIMEOUT,
    client: Any = paper_search,
    use_core: bool = True,
    core_client: Any = core_search,
) -> dict[str, Any]:
    """Execute the research-check for one claim; return the record.

    ``client`` is injectable for tests (anything with the
    ``paper_search`` helper surface). ``core_client`` likewise
    (anything with the ``core_search`` surface: ``search_papers``).
    The record is advisory only: ``verdict`` is None by construction.
    """
    statement = claim.get("normalized_claim") or claim.get("claim") or ""
    phrasings = build_phrasings(statement, alt_phrasings)
    record: dict[str, Any] = {
        "stage": "research_check",
        "record_version": 1,
        "claim_id": claim.get("claim_id"),
        "document_id": document_id or claim.get("source_document_id"),
        "claim_statement": statement,
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "advisory": True,
        "verdict": None,
        "protocol": PROTOCOL_REF,
        "phrasings": phrasings,
        "sources_requested": [s.strip() for s in sources.split(",") if s.strip()],
        "queries": [],
        "source_errors": [],
        "neighbors": [],
        "neighbors_read_full_text": [],
        "gaps": [],
        "citation_checks": [],
    }

    neighbors: dict[str, dict[str, Any]] = {}
    core_texts: dict[str, str] = {}  # _paper_key -> CORE full text
    core_stopped = False

    def note_error(where: str, out: dict[str, Any]) -> None:
        if isinstance(out, dict) and "error" in out:
            record["source_errors"].append(
                {"where": where, "error": out.get("error"),
                 "type": out.get("type")})

    for ph in phrasings:
        fed = client.search_papers(ph["text"], sources=sources,
                                   max_results=max_results, timeout=timeout)
        record["queries"].append({"phrasing_origin": ph["origin"],
                                  "tool": "search_papers",
                                  "query": ph["text"]})
        note_error("search_papers", fed)
        fed_result = fed.get("result", {}) if isinstance(fed, dict) else {}
        if isinstance(fed_result, dict):
            for src, err in (fed_result.get("errors") or {}).items():
                record["source_errors"].append(
                    {"where": f"search_papers:{src}", "error": str(err)})
        for p in _result_papers(fed):
            neighbors.setdefault(_paper_key(p), _neighbor(p))
        for route in PER_SOURCE_ROUTES:
            out = client.search_source(route, ph["text"],
                                       max_results=max_results,
                                       timeout=timeout)
            record["queries"].append({"phrasing_origin": ph["origin"],
                                      "tool": f"search_{route}",
                                      "query": ph["text"]})
            note_error(f"search_{route}", out)
            if isinstance(out, dict) and out.get("is_error"):
                record["source_errors"].append(
                    {"where": f"search_{route}",
                     "error": str(out.get("result"))[:300]})
            for p in _result_papers(out):
                neighbors.setdefault(_paper_key(p), _neighbor(p))
        # CORE (spec 026): one keyed search per phrasing. Hits join
        # the same pool; a hit carrying full text keeps it aside for
        # the read step. A 429 stops CORE for the rest of the run
        # (connector stop rule) and is recorded, never retried.
        if use_core and not core_stopped:
            record["queries"].append({"phrasing_origin": ph["origin"],
                                      "tool": "core_search_works",
                                      "query": ph["text"]})
            core_papers: list[dict[str, Any]] = []
            try:
                core_papers = core_client.search_papers(
                    ph["text"], limit=max_results, timeout=timeout) or []
            except core_search.CoreRateLimitError as e:
                record["source_errors"].append(
                    {"where": "core_search_works", "error": str(e),
                     "type": "RateLimit"})
                core_stopped = True
            except core_search.CoreError as e:
                record["source_errors"].append(
                    {"where": "core_search_works", "error": str(e),
                     "type": "CoreError"})
            for p in core_papers:
                if not isinstance(p, dict):
                    continue
                key = _paper_key(p)
                if key not in neighbors:
                    neighbors[key] = _neighbor(p)
                if p.get("full_text"):
                    neighbors[key]["has_full_text"] = True
                    core_texts[key] = p["full_text"]

    if core_stopped:
        record["gaps"].append(
            {"gap": "CORE rate limit (HTTP 429): CORE stopped for "
                    "this run; remaining phrasings were not searched "
                    "on CORE"})

    ranked = list(neighbors.values())
    for nb in ranked:
        raw = {"title": nb.get("title"), "abstract": nb.get("abstract")}
        nb["relevance"] = _relevance(statement, raw)
    ranked.sort(key=lambda nb: nb["relevance"], reverse=True)
    record["neighbors"] = ranked

    # Nearest-neighbor full-text reads (protocol rule 2): arXiv route
    # only — the reliable OA path; other neighbors become gaps unless
    # a future audit reads them via download_with_fallback manually.
    # Reads go to the highest-relevance arXiv neighbors first.
    if read_neighbors:
        # CORE-carried neighbors are their own read source: the text
        # arrived with the hit, so the read is recorded (source +
        # word count only) without spending an arXiv read slot.
        for nb in record["neighbors"]:
            text = core_texts.get(_paper_key(nb))
            if not text or nb["relevance"] < MIN_READ_RELEVANCE:
                continue
            record["neighbors_read_full_text"].append({
                "title": nb.get("title"), "paper_id": nb.get("paper_id"),
                "source": "core", "words": len(text.split()),
            })
        read_count = 0
        for nb in record["neighbors"]:
            if read_count >= neighbor_limit:
                break
            if nb["relevance"] < MIN_READ_RELEVANCE:
                continue
            pid = str(nb.get("paper_id") or "")
            if not pid or not re.fullmatch(r"\d{4}\.\d{4,5}(v\d+)?", pid):
                continue
            args: dict[str, Any] = {"paper_id": pid}
            if download_dir is not None:
                args["save_path"] = str(download_dir)
            out = client.call_tool("read_arxiv_paper", args, timeout=timeout)
            note_error("read_arxiv_paper", out)
            text = ""
            if isinstance(out, dict):
                res = out.get("result")
                text = res if isinstance(res, str) else ""
            if text:
                record["neighbors_read_full_text"].append({
                    "title": nb.get("title"), "paper_id": pid,
                    "words": len(text.split()),
                })
                read_count += 1
            else:
                record["gaps"].append(
                    {"neighbor": nb.get("title"), "paper_id": pid,
                     "gap": "full text not returned by read_arxiv_paper"})
        unread = [nb.get("title") for nb in record["neighbors"]
                  if nb.get("title") not in
                  {r["title"] for r in record["neighbors_read_full_text"]}]
        if unread:
            record["gaps"].append({
                "gap": "neighbors surfaced but not read in full text "
                       "(abstracts never establish novelty)",
                "neighbors": unread[:10]})

    for doi in dois or []:
        out = client.resolve_doi(doi, timeout=timeout)
        note_error("get_crossref_paper_by_doi", out)
        entry: dict[str, Any] = {"doi": doi}
        res = out.get("result") if isinstance(out, dict) else None
        if isinstance(res, dict):
            entry["resolved"] = {
                "title": res.get("title"),
                "authors": res.get("authors"),
                "year": res.get("year") or res.get("published_date"),
                "venue": res.get("venue") or res.get("journal"),
            }
        else:
            entry["resolved"] = None
            entry["gap"] = "DOI did not resolve; verify the citation manually"
        record["citation_checks"].append(entry)

    if not record["neighbors"] and not record["citation_checks"]:
        record["gaps"].append(
            {"gap": "no neighbors surfaced and no citations supplied — "
                    "this is a search outcome, not evidence of no prior art"})
    return record


def load_dossier(path: Path) -> tuple[str, list[dict[str, Any]]]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return data.get("document_id", ""), list(data.get("claims", []))


def write_record(record: dict[str, Any], out_dir: Path) -> Path:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    safe = re.sub(r"[^A-Za-z0-9_.-]+", "_",
                  f"{record.get('document_id') or 'doc'}__"
                  f"{record.get('claim_id') or 'claim'}")
    path = out_dir / f"{safe}.research_check.json"
    path.write_text(json.dumps(record, ensure_ascii=False, indent=1),
                    encoding="utf-8")
    return path


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="RESEARCH-CHECK stage for one claim dossier")
    ap.add_argument("--claim-file", required=True)
    ap.add_argument("--claim-id", default=None,
                    help="default: every claim in the dossier")
    ap.add_argument("--alt-phrasing", action="append", default=[])
    ap.add_argument("--doi", action="append", default=[])
    ap.add_argument("--out", default=str(DEFAULT_OUT_DIR))
    ap.add_argument("--sources", default=paper_search.DEFAULT_SOURCES)
    ap.add_argument("--max-results", type=int, default=10)
    ap.add_argument("--no-full-text", action="store_true")
    ap.add_argument("--no-core", action="store_true",
                    help="skip the CORE source (spec 026); default: on")
    ap.add_argument("--timeout", type=float,
                    default=paper_search.DEFAULT_TIMEOUT)
    ns = ap.parse_args(argv)

    document_id, claims = load_dossier(Path(ns.claim_file))
    if ns.claim_id:
        claims = [c for c in claims if c.get("claim_id") == ns.claim_id]
        if not claims:
            print(f"claim_id {ns.claim_id} not found in dossier",
                  file=sys.stderr)
            return 1
    out_dir = Path(ns.out)
    download_dir = out_dir / "full_text" if not ns.no_full_text else None
    for claim in claims:
        record = run_research_check(
            claim, document_id=document_id,
            alt_phrasings=ns.alt_phrasing, dois=ns.doi,
            sources=ns.sources, max_results=ns.max_results,
            read_neighbors=not ns.no_full_text,
            use_core=not ns.no_core,
            download_dir=download_dir, timeout=ns.timeout)
        path = write_record(record, out_dir)
        print(json.dumps({
            "record": str(path), "claim_id": record["claim_id"],
            "neighbors": len(record["neighbors"]),
            "read_full_text": len(record["neighbors_read_full_text"]),
            "source_errors": len(record["source_errors"]),
            "verdict": None,
        }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
