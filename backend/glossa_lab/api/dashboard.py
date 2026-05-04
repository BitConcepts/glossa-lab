"""Dashboard API — main-page aggregator.

Endpoints (mounted at ``/api/v1/dashboard``):

* ``GET /highlights`` — recent saved + new discovery items, top kinds,
  AI-generated "what this means" insight, and a per-study/experiment impact
  suggestion the user can act on directly.
* ``GET /feed``       — RSS-style merged feed of the last 14 days of
  discovery items (handy for an at-a-glance dashboard tile that doesn't
  require the user to dig through filters).
* ``POST /insight``   — re-generates the insight on demand (e.g. user
  clicks "regenerate"). Same shape as /highlights but re-runs the LLM.

The endpoint is intentionally cheap by default: AI insight generation is
gated behind ``include_ai`` query param so the dashboard tile loads
instantly and only burns LLM tokens when the user clicks "Generate
insight" / scrolls to the AI block.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import APIRouter, HTTPException, Query

from glossa_lab.database import get_db

router = APIRouter(prefix="/api/v1/dashboard", tags=["dashboard"])

_log = logging.getLogger("glossa_lab.api.dashboard")


# ── Helpers ────────────────────────────────────────────────────────────────


async def _recent_discovery(limit: int = 30, days: int = 14) -> list[dict[str, Any]]:
    """Recent discovery items, newest first, optionally restricted to N days."""
    db = get_db()
    if db is None:
        return []
    since = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
    rows = await db.list_discovery_items(
        topic=None, kind=None, status=None, since=since,
        limit=limit, offset=0,
    )
    return rows


def _tally(items: list[dict[str, Any]], field: str) -> dict[str, int]:
    out: dict[str, int] = {}
    for it in items:
        v = (it.get(field) or "").strip().lower() or "unknown"
        if "," in v:  # topic CSV
            for part in v.split(","):
                p = part.strip()
                if p:
                    out[p] = out.get(p, 0) + 1
        else:
            out[v] = out.get(v, 0) + 1
    return dict(sorted(out.items(), key=lambda kv: kv[1], reverse=True))


async def _study_count() -> int:
    db = get_db()
    if db is None:
        return 0
    try:
        rows = await db.list_studies()
        return len(rows)
    except Exception:  # noqa: BLE001
        return 0


async def _experiment_count() -> int:
    """Approximate count of registered graph experiments."""
    try:
        from glossa_lab.experiment_base import discover_experiments  # noqa: PLC0415

        return len(discover_experiments())
    except Exception:  # noqa: BLE001
        return 0


# ── AI insight ─────────────────────────────────────────────────────────────


_INSIGHT_PROMPT = (
    "You are an Indus-script research assistant. Given the most recent\n"
    "discovery items the user has captured, produce a JSON object with\n"
    "exactly these keys:\n\n"
    "  highlights      — list of the 3 most consequential items, each:\n"
    "                    {id, title, why_it_matters}\n"
    "  what_it_means   — 2-3 sentence narrative summarising the trend or\n"
    "                    cluster across the items\n"
    "  impact          — list of {study_or_experiment_id, impact,\n"
    "                    suggested_action} where suggested_action is one\n"
    "                    of the action_type values listed below.\n"
    "  next_actions    — list of 3-5 EXECUTABLE suggestions, each:\n"
    "                    {label, action_type, params, rationale}.\n"
    "\n"
    "action_type MUST be one of:\n"
    "  run_experiment           — params: {experiment_id} (use exactly an\n"
    "                             id from the registered list).\n"
    "  open_view                — params: {view} (one of: discovery,\n"
    "                             builder, experiments, hypotheses,\n"
    "                             notebooks, ai-tools, reports, settings,\n"
    "                             dashboard).\n"
    "  run_fetch                — params: {} — trigger discovery fetch.\n"
    "  run_mine                 — params: {limit?: int}.\n"
    "  create_hypothesis        — params: {title, statement?}.\n"
    "  propose_experiment_chain — params: {hypothesis} — opens AI Hub\n"
    "                             prompt for chain planning.\n"
    "  ai_chat                  — params: {prompt} — send a starter\n"
    "                             prompt to the docked Glossa AI.\n"
    "  no_op                    — informational only; no Apply button.\n"
    "\n"
    "Pick action_type values that map to real next steps. Prefer\n"
    "run_experiment and propose_experiment_chain over no_op when there's\n"
    "a clear research move. params MUST be a JSON object (use {} when\n"
    "empty). Use ids exactly as given for run_experiment.\n"
    "\n"
    "Return ONLY valid JSON, no markdown fences."
)


def _build_insight_prompt(
    items: list[dict[str, Any]],
    studies: list[dict[str, Any]],
    experiments: list[str],
) -> str:
    items_block = "\n".join(
        f"- id={it.get('id', '')[:10]} kind={it.get('kind', 'other')} "
        f"conf={float(it.get('confidence') or 0):.2f} "
        f"status={it.get('status', 'new')} | {it.get('title', '')[:120]} "
        f"\u2014 {it.get('summary', '')[:160]}"
        for it in items[:25]
    )
    studies_block = "\n".join(
        f"- {s.get('id', '')}: {s.get('name', '')[:120]}" for s in studies[:25]
    ) or "(no studies yet)"
    exp_block = ", ".join(experiments[:80]) or "(no experiments registered)"
    return (
        f"{_INSIGHT_PROMPT}\n\n"
        f"## Recent discovery items ({len(items)} total, showing up to 25)\n"
        f"{items_block}\n\n"
        f"## User's studies\n{studies_block}\n\n"
        f"## Registered experiments\n{exp_block}\n"
    )


async def _generate_insight(
    items: list[dict[str, Any]],
    studies: list[dict[str, Any]],
    experiments: list[str],
) -> dict[str, Any]:
    """Call the configured LLM and return the structured insight payload.

    Falls back to a minimal heuristic summary if no provider is configured
    or if the call fails — so the dashboard never blocks on a 500.
    """
    if not items:
        return {
            "highlights": [],
            "what_it_means": "No discovery items yet \u2014 trigger a fetch from "
                              "Settings \u2192 Auto Discovery to populate the dashboard.",
            "impact": [],
            "next_actions": [
                "Settings \u2192 Auto Discovery \u2192 Fetch now",
                "Add at least one source API key (NewsAPI / SerpAPI / Brave) "
                "if no key-bearing source is configured",
                "Add one recipient + send a test email so digests land in your inbox",
            ],
            "model": "heuristic",
        }

    prompt = _build_insight_prompt(items, studies, experiments)

    try:
        from glossa_lab.ai_utils import call_llm  # noqa: PLC0415

        raw = call_llm(
            [
                {"role": "system", "content": "You produce concise structured JSON for a research dashboard."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=900, temperature=0.2,
        )
        # Strip any stray code fences before json-loading.
        cleaned = raw.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("```", 2)[1] if "```" in cleaned[3:] else cleaned[3:]
            if cleaned.lower().startswith("json"):
                cleaned = cleaned[4:].lstrip()
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
        parsed = json.loads(cleaned)
        # Light schema validation
        for k in ("highlights", "what_it_means", "impact", "next_actions"):
            parsed.setdefault(k, [] if k != "what_it_means" else "")
        # Coerce next_actions to the structured shape — the LLM sometimes
        # returns plain strings, in which case we fall back to no_op. The
        # frontend depends on action_type / params being present.
        normalised: list[dict[str, Any]] = []
        for a in parsed.get("next_actions", []):
            if isinstance(a, str):
                normalised.append({
                    "label": a, "action_type": "no_op", "params": {},
                    "rationale": "",
                })
            elif isinstance(a, dict):
                a.setdefault("label",       a.get("label", ""))
                a.setdefault("action_type", "no_op")
                a.setdefault("params",      {})
                if not isinstance(a.get("params"), dict):
                    a["params"] = {}
                a.setdefault("rationale",   "")
                normalised.append(a)
        parsed["next_actions"] = normalised
        # Same coercion for impact entries.
        impact_norm: list[dict[str, Any]] = []
        for im in parsed.get("impact", []):
            if isinstance(im, dict):
                im.setdefault("study_or_experiment_id", im.get("id", ""))
                im.setdefault("impact", "")
                im.setdefault("suggested_action", "no_op")
                impact_norm.append(im)
        parsed["impact"] = impact_norm
        parsed["model"] = "ai"
        return parsed
    except Exception as exc:  # noqa: BLE001
        _log.warning("dashboard insight LLM call failed: %s", exc)
        # Heuristic fallback: use the top-3 highest-confidence items.
        ranked = sorted(
            items, key=lambda x: float(x.get("confidence") or 0), reverse=True,
        )[:3]
        return {
            "highlights": [
                {
                    "id": it.get("id", ""),
                    "title": it.get("title", ""),
                    "why_it_matters": (it.get("summary") or "")[:200],
                }
                for it in ranked
            ],
            "what_it_means": (
                f"{len(items)} new item(s) in the last 14 days. "
                "AI insight unavailable \u2014 either no LLM provider is "
                "configured or the call timed out. Click Regenerate to retry."
            ),
            "impact": [],
            "next_actions": [
                "Settings \u2192 AI Profiles: pick a provider so insights work",
                "Discovery: triage the new items by status (saved / dismissed)",
                "AI Hub \u2192 Cross-Study Synthesis: run on saved findings + your studies",
            ],
            "model": "heuristic-fallback",
            "error": str(exc),
        }


# ── Endpoints ──────────────────────────────────────────────────────────────


@router.get("/highlights")
async def dashboard_highlights(
    days: int = Query(14, ge=1, le=90),
    limit: int = Query(30, ge=1, le=200),
    include_ai: bool = Query(False),
) -> dict[str, Any]:
    """Aggregated dashboard payload.

    With ``include_ai=false`` (default) the response is fast: just the
    recent items, status/kind tallies, and basic counts. With
    ``include_ai=true`` the configured LLM is also called to produce a
    structured insight.
    """
    items = await _recent_discovery(limit=limit, days=days)
    studies: list[dict[str, Any]] = []
    db = get_db()
    if db is not None:
        try:
            studies = await db.list_studies()
        except Exception:  # noqa: BLE001
            studies = []
    try:
        from glossa_lab.experiment_base import discover_experiments  # noqa: PLC0415

        exp_ids = sorted(discover_experiments().keys())
    except Exception:  # noqa: BLE001
        exp_ids = []

    payload: dict[str, Any] = {
        "items": items,
        "n_items": len(items),
        "by_kind":   _tally(items, "kind"),
        "by_status": _tally(items, "status"),
        "by_topic":  _tally(items, "topic"),
        "by_source": _tally(items, "source"),
        "n_studies":     len(studies),
        "n_experiments": len(exp_ids),
        "since_days":    days,
    }

    if include_ai:
        payload["insight"] = await _generate_insight(items, studies, exp_ids)
    else:
        payload["insight"] = None  # frontend can request it lazily

    return payload


@router.post("/insight")
async def dashboard_insight(
    days: int = Query(14, ge=1, le=90),
    limit: int = Query(30, ge=1, le=200),
) -> dict[str, Any]:
    """Force-regenerate the AI insight (always burns LLM tokens)."""
    items = await _recent_discovery(limit=limit, days=days)
    db = get_db()
    studies: list[dict[str, Any]] = []
    if db is not None:
        try:
            studies = await db.list_studies()
        except Exception:  # noqa: BLE001
            studies = []
    try:
        from glossa_lab.experiment_base import discover_experiments  # noqa: PLC0415

        exp_ids = sorted(discover_experiments().keys())
    except Exception:  # noqa: BLE001
        exp_ids = []
    return await _generate_insight(items, studies, exp_ids)


@router.get("/feed")
async def dashboard_feed(
    days: int = Query(14, ge=1, le=90),
    limit: int = Query(50, ge=1, le=200),
) -> dict[str, Any]:
    """RSS-style flat feed for the dashboard timeline tile."""
    items = await _recent_discovery(limit=limit, days=days)
    return {
        "items": items,
        "n_items": len(items),
        "since_days": days,
    }


__all__ = ["router"]
