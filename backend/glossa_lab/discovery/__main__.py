"""CLI for the continuous-discovery engine.

Usage::

    python -m glossa_lab.discovery topics
    python -m glossa_lab.discovery sources
    python -m glossa_lab.discovery fetch  [--topics ID,ID] [--sources S,S] [--since ISO]
    python -m glossa_lab.discovery mine   [--topic ID] [--limit N]
    python -m glossa_lab.discovery daily  [--limit N]      # combined fetch+mine
    python -m glossa_lab.discovery status

Each working subcommand wraps its work in :class:`CliReporter` so the run
appears in the Jobs panel and a JSON report is dropped under ``reports/``.
The DB is initialised against the configured data directory so the CLI
talks to the same store the running backend does.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from datetime import datetime
from typing import Any

from glossa_lab.cli_bridge import CliReporter
from glossa_lab.config import get_settings
from glossa_lab.database import close_db, init_db
from glossa_lab.discovery import store
from glossa_lab.discovery.fetchers import (
    available_fetchers,
    list_topics,
    run_all,
    run_topic,
)
from glossa_lab.discovery.llm import LLMClient
from glossa_lab.discovery.mine import mine_pending


def _parse_csv(raw: str | None) -> list[str] | None:
    if not raw:
        return None
    out = [s.strip() for s in raw.split(",") if s.strip()]
    return out or None


def _parse_since(raw: str | None) -> datetime | None:
    if not raw:
        return None
    try:
        return datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError as exc:
        print(f"error: --since must be ISO-8601 ({exc})", file=sys.stderr)
        sys.exit(2)


# ── Subcommand handlers ─────────────────────────────────────────────────────


async def _cmd_topics(_args: argparse.Namespace) -> int:
    profiles = list_topics()
    if not profiles:
        print("(no topic profiles found)")
        return 0
    for t in profiles:
        kw = ", ".join(t.keywords[:5])
        more = "..." if len(t.keywords) > 5 else ""
        print(f"{t.id:<26} {t.label}")
        print(f"    {kw}{more}")
    return 0


async def _cmd_sources(_args: argparse.Namespace) -> int:
    for s in available_fetchers():
        flag = "OK " if s["configured"] else "OFF"
        reason = s["disabled_reason"] or ""
        reqs = ",".join(s["requires"]) or "-"
        print(f"  [{flag}] {s['source']:<10} requires={reqs}  {reason}")
    return 0


async def _cmd_status(_args: argparse.Namespace) -> int:
    """Print group counts (status / kind / topic / source)."""
    for group in ("status", "kind", "topic", "source"):
        counts = await store.count_by(group=group)
        if not counts:
            continue
        print(f"by {group}:")
        for k in sorted(counts):
            print(f"    {k or '<empty>':<24} {counts[k]}")
    return 0


async def _cmd_fetch(args: argparse.Namespace) -> int:
    topics = _parse_csv(args.topics)
    sources = _parse_csv(args.sources)
    since = _parse_since(args.since)
    with CliReporter("discovery_fetch", "Discovery Fetch") as rep:
        if topics:
            summaries = []
            for tid in topics:
                summaries.append(
                    await run_topic(tid, since=since, only_sources=sources)
                )
            agg: dict[str, Any] = {
                "topics_run": list(topics),
                "results": summaries,
                "fetched": sum(int(s.get("fetched", 0)) for s in summaries),
                "new": sum(int(s.get("new", 0)) for s in summaries),
                "merged": sum(int(s.get("merged", 0)) for s in summaries),
                "errors": sum(int(s.get("errors", 0)) for s in summaries),
            }
        else:
            agg = await run_all(since=since, only_sources=sources)
        rep.save_result(agg)
    print(json.dumps(
        {k: agg[k] for k in ("fetched", "new", "merged", "errors") if k in agg},
        indent=2,
    ))
    return 0


async def _cmd_mine(args: argparse.Namespace) -> int:
    client = LLMClient()
    if not client.configured_providers():
        print(
            "error: no LLM provider configured. Set MISTRAL_API_KEY / OPENAI_API_KEY "
            "/ GOOGLE_API_KEY before running mine.",
            file=sys.stderr,
        )
        return 2
    with CliReporter("discovery_mine", "Discovery Mine") as rep:
        result = await mine_pending(
            client=client, topic=args.topic, limit=int(args.limit),
        )
        rep.save_result(result)
    print(json.dumps(
        {k: result[k] for k in ("classified", "failed", "by_kind", "pending")},
        indent=2,
    ))
    return 0


async def _cmd_daily(args: argparse.Namespace) -> int:
    """Combined fetch + mine, mirroring the scheduler tick."""
    with CliReporter("discovery_daily", "Discovery Daily") as rep:
        fetch_result = await run_all()
        client = LLMClient()
        if client.configured_providers():
            mine_result = await mine_pending(client=client, limit=int(args.limit))
        else:
            mine_result = {"skipped": "no LLM provider configured"}
        result = {"fetch": fetch_result, "mine": mine_result}
        rep.save_result(result)
    print(json.dumps(
        {
            "fetched": fetch_result.get("fetched"),
            "new": fetch_result.get("new"),
            "classified": mine_result.get("classified") if isinstance(mine_result, dict) else None,
        },
        indent=2,
    ))
    return 0


# ── Argparse wiring ─────────────────────────────────────────────────────────


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="python -m glossa_lab.discovery",
        description="Continuous-discovery engine CLI",
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("topics", help="list topic profiles shipped with the package")
    sub.add_parser("sources", help="list registered fetchers + key status")
    sub.add_parser("status", help="print counts grouped by status / kind / topic / source")

    pf = sub.add_parser("fetch", help="fetch new items from configured sources")
    pf.add_argument("--topics", help="comma-separated topic ids (default: all)")
    pf.add_argument("--sources", help="comma-separated source names (default: all)")
    pf.add_argument("--since", help="ISO-8601 lower bound on published_at")

    pm = sub.add_parser("mine", help="classify + link un-mined items")
    pm.add_argument("--topic", help="restrict to a single topic id")
    pm.add_argument("--limit", default="20", help="max items per run (default: 20)")

    pd = sub.add_parser("daily", help="combined fetch + mine, like the scheduler")
    pd.add_argument("--limit", default="50", help="max items to mine (default: 50)")

    return p


_HANDLERS = {
    "topics": _cmd_topics,
    "sources": _cmd_sources,
    "status": _cmd_status,
    "fetch": _cmd_fetch,
    "mine": _cmd_mine,
    "daily": _cmd_daily,
}


async def _run(args: argparse.Namespace) -> int:
    settings = get_settings()
    await init_db(settings.data_dir)
    try:
        handler = _HANDLERS[args.cmd]
        return await handler(args)
    finally:
        await close_db()


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return asyncio.run(_run(args))


if __name__ == "__main__":
    raise SystemExit(main())
