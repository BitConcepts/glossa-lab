"""Stdio MCP client for the paper-search-mcp server (openags).

Glossa-side client for the shared scholarly search/retrieval server
used by the RESEARCH-CHECK stage (see
``specs/025-paper-search-research-check/`` and
``docs/paper-search-mcp.md``). The server itself lives in its own
pinned venv (``~/workspace/venvs/paper-search-mcp``, maintained from
the RCPH workspace) and is spawned here as a stdio subprocess; this
module runs under Glossa's backend venv, which already depends on
``mcp>=1,<2``.

Configuration (environment):
  GLOSSA_PAPER_SEARCH_PYTHON  interpreter that runs the server
                              (default: ~/workspace/venvs/paper-search-mcp/bin/python)
  GLOSSA_PAPER_SEARCH_TIMEOUT default per-call timeout, seconds (300)
  PAPER_SEARCH_MCP_*          optional upstream API keys/config —
                              passed through to the server only when
                              already present in the caller's
                              environment; never stored in files.

Hard rules:
  * Sci-Hub is OFF. ``read_full_text`` refuses any argument set that
    would enable it; there is no override.
  * Every call has an explicit timeout (governance H9/H11).
  * Failures return clean error dicts (house style, cf.
    ``glossa_mcp/server.py``) instead of raising into callers, except
    for the Sci-Hub refusal, which raises ValueError by design.

CLI:
  python -m glossa_lab.paper_search tools [--names-only]
  python -m glossa_lab.paper_search call <tool> [--args '<json>'] [--timeout S]
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

DEFAULT_SERVER_PYTHON = os.path.expanduser(
    "~/workspace/venvs/paper-search-mcp/bin/python"
)
DEFAULT_TIMEOUT = float(os.environ.get("GLOSSA_PAPER_SEARCH_TIMEOUT", "300"))

# Default federated source set for prior-art searches: the sources
# that answer without keys from this network (measured status lives in
# docs/paper-search-mcp.md). Callers may pass a wider set; per-source
# failures surface in the result's ``errors`` field, never silently.
DEFAULT_SOURCES = "arxiv,crossref,openalex,semantic,core,europepmc"


def server_python() -> str:
    return os.environ.get("GLOSSA_PAPER_SEARCH_PYTHON", DEFAULT_SERVER_PYTHON)


def _params() -> StdioServerParameters:
    env = dict(os.environ)
    # The server talks to public HTTPS APIs, so KEEP the ambient proxy
    # settings (this VM reaches the internet through a CONNECT proxy).
    # But ambient NO_PROXY can contain bracketed IPv6 entries that
    # corrupt httpx URL parsing ("Invalid port: ':1]'"), so sanitize
    # it the same way the other clients in this project do.
    env["NO_PROXY"] = "localhost,127.0.0.1,::1"
    env["no_proxy"] = "localhost,127.0.0.1,::1"
    return StdioServerParameters(
        command=server_python(),
        args=["-m", "paper_search_mcp.server"],
        env=env,
    )


async def _list_tools() -> list[dict[str, Any]]:
    async with stdio_client(_params()) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.list_tools()
            return [
                {"name": t.name, "description": (t.description or "").strip()}
                for t in result.tools
            ]


async def _call(tool: str, args: dict[str, Any], timeout: float) -> dict[str, Any]:
    async with stdio_client(_params()) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await asyncio.wait_for(
                session.call_tool(tool, args), timeout=timeout
            )
            texts = [
                getattr(block, "text", None) for block in result.content
            ]
            text = "\n".join(t for t in texts if t is not None)
            parsed: Any = text
            for _ in range(2):  # some per-source tools double-encode
                if isinstance(parsed, str):
                    try:
                        parsed = json.loads(parsed)
                    except (json.JSONDecodeError, TypeError):
                        break
                else:
                    break
            return {
                "tool": tool,
                "is_error": bool(result.isError),
                "result": parsed,
            }


def _run(coro_factory, timeout: float) -> dict[str, Any]:
    """Run one server session with a hard deadline; error dict on failure."""
    try:
        return asyncio.run(
            asyncio.wait_for(coro_factory(), timeout=timeout + 30.0)
        )
    except asyncio.TimeoutError:
        return {"error": f"paper-search call exceeded {timeout:g}s",
                "type": "Timeout"}
    except Exception as exc:  # transport / spawn failures
        return {"error": str(exc), "type": type(exc).__name__}


def list_tools(timeout: float = DEFAULT_TIMEOUT) -> dict[str, Any]:
    """Return {"tools": [...], "count": n} or an error dict."""
    tools = _run(_list_tools, timeout)
    if isinstance(tools, list):
        return {"tools": tools, "count": len(tools)}
    return tools


def call_tool(tool: str, args: dict[str, Any] | None = None,
              timeout: float = DEFAULT_TIMEOUT) -> dict[str, Any]:
    """Call one paper-search tool; returns its parsed result or error dict."""
    return _run(lambda: _call(tool, args or {}, timeout), timeout)


# ── Typed helpers ────────────────────────────────────────────────────

def search_papers(query: str, sources: str = DEFAULT_SOURCES,
                  max_results: int = 10,
                  timeout: float = DEFAULT_TIMEOUT) -> dict[str, Any]:
    """Federated search; per-source failures appear in ``errors``."""
    return call_tool("search_papers", {
        "query": query, "sources": sources, "max_results": max_results,
    }, timeout=timeout)


def search_source(source: str, query: str, max_results: int = 10,
                  timeout: float = DEFAULT_TIMEOUT) -> dict[str, Any]:
    """Per-source search, e.g. source='arxiv' -> search_arxiv."""
    return call_tool(f"search_{source}", {
        "query": query, "max_results": max_results,
    }, timeout=timeout)


def resolve_doi(doi: str, timeout: float = DEFAULT_TIMEOUT) -> dict[str, Any]:
    """Canonical metadata for a DOI, via Crossref."""
    return call_tool("get_crossref_paper_by_doi", {"doi": doi},
                     timeout=timeout)


def read_full_text(source: str, paper_id: str = "", doi: str = "",
                     save_path: str = "",
                     timeout: float = DEFAULT_TIMEOUT) -> dict[str, Any]:
    """Open-access full text via the server's fallback chain.

    Sci-Hub is hard-off: any attempt to enable it raises ValueError.
    """
    args: dict[str, Any] = {"source": source}
    if paper_id:
        args["paper_id"] = paper_id
    if doi:
        args["doi"] = doi
    if save_path:
        args["save_path"] = save_path
    return _guarded_read("download_with_fallback", args, timeout)


def _guarded_read(tool: str, args: dict[str, Any],
                  timeout: float) -> dict[str, Any]:
    if args.get("use_scihub"):
        raise ValueError(
            "use_scihub is hard-off in Glossa Lab (docs/paper-search-mcp.md)"
        )
    args = {k: v for k, v in args.items() if k != "use_scihub"}
    return call_tool(tool, args, timeout=timeout)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="paper-search-mcp client")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p_tools = sub.add_parser("tools", help="list the server's tools")
    p_tools.add_argument("--names-only", action="store_true")
    p_tools.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT)
    p_call = sub.add_parser("call", help="call one tool")
    p_call.add_argument("tool")
    p_call.add_argument("--args", default="{}", help="JSON object of arguments")
    p_call.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT)
    ns = ap.parse_args(argv)
    if ns.cmd == "tools":
        out = list_tools(timeout=ns.timeout)
        if "tools" in out:
            for t in out["tools"]:
                if ns.names_only:
                    print(t["name"])
                else:
                    first = t["description"].split("\n")[0]
                    print(f"{t['name']} — {first}")
            print(f"total: {out['count']} tools", file=sys.stderr)
            return 0
        print(json.dumps(out), file=sys.stderr)
        return 2
    try:
        args = json.loads(ns.args)
    except json.JSONDecodeError as exc:
        print(f"--args is not valid JSON: {exc}", file=sys.stderr)
        return 1
    if not isinstance(args, dict):
        print("--args must be a JSON object", file=sys.stderr)
        return 1
    out = call_tool(ns.tool, args, timeout=ns.timeout)
    if "error" in out and "result" not in out:
        print(json.dumps(out), file=sys.stderr)
        return 3 if out.get("type") == "Timeout" else 2
    print(json.dumps(out.get("result", out), ensure_ascii=False, indent=1))
    return 2 if out.get("is_error") else 0


if __name__ == "__main__":
    raise SystemExit(main())
