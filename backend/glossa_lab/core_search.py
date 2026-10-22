"""CORE client for the RESEARCH-CHECK stage (spec 026).

Direct client for the CORE scholarly API (core.ac.uk) — the largest
open-access full-text collection in the audit protocol's source
roster — used by ``glossa_lab.research_check`` as a keyed source.
Design and protocol: ``specs/026-core-research-source/`` and the
CORE section of ``docs/paper-search-mcp.md``.

Why a direct client and not the paper-search MCP server's CORE
tool: the server reads its CORE key from an environment variable,
while Glossa's CORE access is the registered ``custom.core``
connection (the route the RCPH workspace connected and verified
2026-10-22). This module attaches that connection's credential as a
runtime surrogate — ``dynamic_credentials.add_surrogate_to_request``
places an ``hsurr:`` token in the Authorization bearer header and the
runtime swaps in the real key only on egress to ``api.core.ac.uk``.
The key value is never read, printed, or stored by this code, and no
key is ever taken from an environment variable or a file here.

Hard rules (mirroring the connector contract in
``custom-connectors/custom.core/CONNECTOR.md``):
  * Canonical search path carries a trailing slash
    (``/v3/search/works/``). The slashless form answers 301 to the
    same host, and redirects are refused on authenticated requests,
    so the slash is part of the contract.
  * Pace: the registered tier allows about 5 single requests per
    10 seconds. Network calls are spaced by ``MIN_INTERVAL_SECONDS``.
  * A 429 is a hard stop: ``CoreRateLimitError`` is raised and never
    retried. Callers (the stage) record it and stop using CORE.
  * Every call has an explicit timeout (governance H9/H11).

CLI:
  python -m glossa_lab.core_search search '<query>' [--limit N]
  python -m glossa_lab.core_search get <core-id>
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
from dynamic_credentials import add_surrogate_to_request, read_json_response  # noqa: E402

BASE = "https://api.core.ac.uk/v3"
ALLOWED_HOSTS = ["api.core.ac.uk"]
CREDENTIAL = "custom.core"

DEFAULT_TIMEOUT = float(os.environ.get("GLOSSA_CORE_TIMEOUT", "120"))

# Registered tier: ~5 single requests per 10 s. 2.1 s spacing leaves
# margin; the pace guard sleeps only the shortfall, so a caller that
# is already slow pays nothing.
MIN_INTERVAL_SECONDS = 2.1

_last_call_at = 0.0


class CoreError(RuntimeError):
    """A CORE call failed; the message is safe to record verbatim."""


class CoreRateLimitError(CoreError):
    """HTTP 429: the registered tier was crossed. Hard stop."""


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args):
        raise CoreError("redirect refused, verify the endpoint")


def _pace(now: float | None = None) -> None:
    """Enforce MIN_INTERVAL_SECONDS between network calls."""
    global _last_call_at
    t = time.monotonic() if now is None else now
    wait = MIN_INTERVAL_SECONDS - (t - _last_call_at)
    if wait > 0:
        time.sleep(wait)
        t = time.monotonic() if now is None else t + wait
    _last_call_at = t


def _fetch(path: str, timeout: float) -> dict[str, Any]:
    if not path.startswith("/"):
        path = "/" + path
    request = urllib.request.Request(
        BASE + path,
        headers={"Accept": "application/json",
                 "User-Agent": "glossa-lab-core-search/1.0 (spec 026)"},
    )
    add_surrogate_to_request(request, CREDENTIAL,
                             allowed_hosts=ALLOWED_HOSTS)
    _pace()
    try:
        with urllib.request.build_opener(_NoRedirect()).open(
                request, timeout=timeout) as response:
            return read_json_response(response)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")[:300]
        if e.code == 429:
            raise CoreRateLimitError(
                f"HTTP 429 from CORE ({path}): rate tier crossed — "
                f"stop, do not retry. {body}") from e
        raise CoreError(f"HTTP {e.code} from CORE ({path}): {body}") from e
    except CoreError:
        raise
    except Exception as e:  # transport failures surface clean, not raw
        raise CoreError(f"CORE request failed ({path}): {e}") from e


def search_works(query: str, limit: int = 10,
                 timeout: float = DEFAULT_TIMEOUT) -> dict[str, Any]:
    """Search the CORE works index; returns the raw v3 result dict
    (``totalHits`` + ``results``). Raises CoreError on failure."""
    q = urllib.parse.urlencode({"q": query, "limit": int(limit)})
    return _fetch(f"/search/works/?{q}", timeout)


def get_work(core_id: str, timeout: float = DEFAULT_TIMEOUT) -> dict[str, Any]:
    """Fetch one work by CORE id (a bare id or a full v3 works URL)."""
    cid = str(core_id).strip()
    if "/works/" in cid:
        cid = cid.rsplit("/works/", 1)[-1]
    return _fetch(f"/works/{urllib.parse.quote(cid, safe='')}", timeout)


def normalize_work(work: dict[str, Any]) -> dict[str, Any]:
    """Map a CORE work record onto the stage's paper shape.

    Matches the neighbor fields ``research_check`` consumes, under
    source ``"core"``, plus ``has_full_text`` and — in memory only —
    ``full_text`` when CORE holds the text. The stage records the
    read (source + word count); the text itself is never written
    into a sidecar record.
    """
    authors: list[str] = []
    for a in work.get("authors") or []:
        if isinstance(a, dict):
            name = a.get("displayName") or a.get("name")
            if name:
                authors.append(str(name))
        elif a:
            authors.append(str(a))
    doi = (work.get("doi") or "").strip()
    for prefix in ("https://doi.org/", "http://doi.org/", "doi:"):
        if doi.lower().startswith(prefix):
            doi = doi[len(prefix):]
            break
    full_text = work.get("fullText") or None
    links = work.get("links") or []
    url = work.get("downloadUrl") or (links[0] if links else None)
    return {
        "title": work.get("title"),
        "authors": authors,
        "year": work.get("yearPublished"),
        "doi": doi or None,
        "paper_id": f"core:{work.get('id')}" if work.get("id") else None,
        "source": "core",
        "url": url,
        "abstract": work.get("abstract"),
        "has_full_text": bool(full_text),
        "full_text": full_text,
    }


def search_papers(query: str, limit: int = 10,
                  timeout: float = DEFAULT_TIMEOUT) -> list[dict[str, Any]]:
    """Search and return normalized papers (the stage-facing shape)."""
    out = search_works(query, limit=limit, timeout=timeout)
    results = out.get("results") if isinstance(out, dict) else None
    return [normalize_work(w) for w in results or []
            if isinstance(w, dict)]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="CORE API client (spec 026)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p_search = sub.add_parser("search", help="search the works index")
    p_search.add_argument("query")
    p_search.add_argument("--limit", type=int, default=10)
    p_search.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT)
    p_get = sub.add_parser("get", help="fetch one work by CORE id")
    p_get.add_argument("core_id")
    p_get.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT)
    ns = ap.parse_args(argv)
    try:
        if ns.cmd == "search":
            out = search_works(ns.query, limit=ns.limit, timeout=ns.timeout)
            slim = {
                "totalHits": out.get("totalHits"),
                "results": [{
                    "id": w.get("id"), "title": w.get("title"),
                    "year": w.get("yearPublished"),
                    "doi": w.get("doi"),
                    "has_full_text": bool(w.get("fullText")),
                    "full_text_words": len((w.get("fullText") or "").split()),
                } for w in out.get("results") or [] if isinstance(w, dict)],
            }
            print(json.dumps(slim, ensure_ascii=False, indent=1))
        else:
            print(json.dumps(get_work(ns.core_id, timeout=ns.timeout),
                             ensure_ascii=False, indent=1))
    except CoreRateLimitError as e:
        print(json.dumps({"error": str(e), "type": "RateLimit"}),
              file=sys.stderr)
        return 3
    except CoreError as e:
        print(json.dumps({"error": str(e), "type": "CoreError"}),
              file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
