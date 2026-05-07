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


async def _recent_discovery(
    limit: int = 30,
    days: int = 14,
    topic_ids: list[str] | None = None,
) -> list[dict[str, Any]]:
    """Recent discovery items, newest first, optionally restricted to N days.

    If *topic_ids* is provided, only items whose ``topic`` intersects the
    given set are returned (used for project-scoped dashboards).
    """
    db = get_db()
    if db is None:
        return []
    since = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
    rows = await db.list_discovery_items(
        topic=None, kind=None, status=None, since=since,
        limit=limit * 3 if topic_ids else limit,  # fetch extra when filtering
        offset=0,
    )
    if topic_ids:
        tid_set = set(topic_ids)
        filtered: list[dict[str, Any]] = []
        for r in rows:
            item_topics = {t.strip() for t in (r.get("topic") or "").split(",") if t.strip()}
            if item_topics & tid_set:
                filtered.append(r)
                if len(filtered) >= limit:
                    break
        return filtered
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


def _graph_experiment_ids() -> list[str]:
    """Return sorted IDs of graph experiments (what the user actually sees)."""
    try:
        from glossa_lab.experiment_graph import list_graph_experiments  # noqa: PLC0415

        return sorted(spec["id"] for spec in list_graph_experiments())
    except Exception:  # noqa: BLE001
        return []


def _graph_experiment_id_name_map() -> dict[str, str]:
    """Return {id: name} for graph experiments — used to give the LLM human-readable labels."""
    try:
        from glossa_lab.experiment_graph import list_graph_experiments  # noqa: PLC0415

        return {spec["id"]: spec.get("name", spec["id"]) for spec in list_graph_experiments()}
    except Exception:  # noqa: BLE001
        return {}


async def _hypothesis_count() -> int:
    """Count of tracked hypotheses (not discovery items tagged 'hypothesis')."""
    db = get_db()
    if db is None:
        return 0
    try:
        rows = await db.list_hypotheses()
        return len(rows)
    except Exception:  # noqa: BLE001
        return 0


# ── AI insight ─────────────────────────────────────────────────────────────


_INSIGHT_PROMPT_TEMPLATE = (
    "You are a {goal_label} research assistant. Given the most recent\n"
    "discovery items the user has captured, produce a JSON object with\n"
    "exactly these keys:\n\n"
    "  highlights      — list of the 3 most consequential items, each:\n"
    "                    {id, title, why_it_matters}\n"
    "  what_it_means   — 2-3 sentence narrative summarising the trend or\n"
    "                    cluster across the items\n"
    "  impact          — list of {study_or_experiment_id, name, impact,\n"
    "                    suggested_action, suggested_params}.\n"
    "                    CRITICAL: study_or_experiment_id MUST be an id\n"
    "                    that appears VERBATIM in the 'Registered\n"
    "                    experiments' or 'User's studies' lists below.\n"
    "                    NEVER invent, abbreviate, or hash an id.\n"
    "                    name is a short human-readable label for the\n"
    "                    experiment or study.\n"
    "                    suggested_action is one of the action_type\n"
    "                    string values listed below (NEVER an object).\n"
    "                    suggested_params is a JSON object carrying the\n"
    "                    same payload schema as the corresponding\n"
    "                    next_actions params (e.g. {experiment_id} for\n"
    "                    run_experiment); use {} when not applicable.\n"
    "  next_actions    — list of 3-5 EXECUTABLE suggestions, each:\n"
    "                    {label, action_type, params, rationale}.\n"
    "\n"
    "action_type MUST be one of:\n"
    "  run_experiment           — params: {experiment_id} where\n"
    "                             experiment_id MUST be copied EXACTLY\n"
    "                             from the 'Registered experiments'\n"
    "                             list. NEVER fabricate an id.\n"
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
    "empty).\n"
    "\n"
    "Return ONLY valid JSON, no markdown fences."
)


def _build_insight_prompt(
    items: list[dict[str, Any]],
    studies: list[dict[str, Any]],
    experiments: list[str],
    goal: dict[str, Any] | None = None,
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
    # Include experiment name so the LLM can use real labels, not invented ones.
    _names = _graph_experiment_id_name_map()
    exp_lines = [f"{eid} ({_names.get(eid, eid)})" for eid in experiments[:80]]
    exp_block = ", ".join(exp_lines) or "(no experiments registered)"
    goal_label = (goal or {}).get("label", "research")
    prompt_text = _INSIGHT_PROMPT_TEMPLATE.replace("{goal_label}", goal_label)
    goal_ctx = ""
    if goal and goal.get("prompt_context"):
        goal_ctx = f"\n## Research goal context\n{goal['prompt_context']}\n"
    return (
        f"{prompt_text}\n\n"
        f"{goal_ctx}"
        f"## Recent discovery items ({len(items)} total, showing up to 25)\n"
        f"{items_block}\n\n"
        f"## User's studies\n{studies_block}\n\n"
        f"## Registered experiments\n{exp_block}\n"
    )


async def _resolve_project(
    project_id: str | None,
) -> dict[str, Any] | None:
    """Resolve a project by ID, falling back to the active project."""
    db = get_db()
    if db is None:
        return None
    if project_id:
        return await db.get_project(project_id)
    return await db.get_active_project()


async def _generate_insight(
    items: list[dict[str, Any]],
    studies: list[dict[str, Any]],
    experiments: list[str],
    project: dict[str, Any] | None = None,
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

    # Use the provided project for context-scoped insight, or fall back to active.
    goal: dict[str, Any] | None = project
    if goal is None:
        try:
            _db = get_db()
            if _db is not None:
                goal = await _db.get_default_goal()
        except Exception:  # noqa: BLE001
            pass

    prompt = _build_insight_prompt(items, studies, experiments, goal=goal)

    try:
        from glossa_lab.ai_utils import call_llm  # noqa: PLC0415

        try:
            raw = call_llm(
                [
                    {"role": "system", "content": "You produce concise structured JSON for a research dashboard."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=900, temperature=0.2,
            )
        except ValueError as ve:
            # ValueError from call_llm = "No AI provider configured"
            _log.info("dashboard insight skipped: %s", ve)
            return {
                "highlights": [],
                "what_it_means": (
                    "No AI provider is configured. Go to Settings \u2192 AI Providers "
                    "to set up Ollama, Mistral, OpenAI, or Anthropic, then click "
                    "Regenerate."
                ),
                "impact": [],
                "next_actions": [
                    {"label": "Open Settings", "action_type": "open_view",
                     "params": {"view": "settings"}, "rationale": "Configure an AI provider to enable insights."},
                ],
                "model": "no-provider",
            }
        # Guard against empty / whitespace-only LLM responses (observed
        # when the provider times out or returns no content).
        if not raw or not raw.strip():
            _log.warning("dashboard insight LLM returned empty response")
            return {
                "highlights": [],
                "what_it_means": (
                    "Insight generation returned empty \u2014 this usually means "
                    "the LLM provider timed out or returned no content. "
                    "Try regenerating."
                ),
                "impact": [],
                "next_actions": [],
                "model": "empty-fallback",
            }
        # Strip any stray code fences before json-loading.
        cleaned = raw.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("```", 2)[1] if "```" in cleaned[3:] else cleaned[3:]
            if cleaned.lower().startswith("json"):
                cleaned = cleaned[4:].lstrip()
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
        try:
            parsed = json.loads(cleaned)
        except json.JSONDecodeError as jde:
            _log.warning(
                "dashboard insight: LLM returned invalid JSON (%s). First 200 chars: %s",
                jde, cleaned[:200],
            )
            return {
                "highlights": [],
                "what_it_means": (
                    "The AI returned a response but it wasn\u2019t valid JSON. "
                    "This sometimes happens when the model is overloaded or "
                    "the response was truncated. Click Regenerate to retry."
                ),
                "impact": [],
                "next_actions": [],
                "model": "json-error",
            }
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
        # The LLM occasionally emits ``suggested_action`` as a structured
        # object (``{action_type, params}``) instead of the contracted
        # string. Detect both shapes and split into a stable wire format:
        # ``suggested_action`` is always a string action_type and the
        # accompanying params (if any) move to ``suggested_params``.
        # Validate experiment IDs against the real registry.  The LLM
        # sometimes hallucinates hex-hash-style ids; we resolve or strip
        # them here so the frontend never sees a phantom experiment.
        exp_set = set(experiments)  # O(1) lookup
        import re as _re  # noqa: PLC0415
        _hex_re = _re.compile(r"^[0-9a-f]{8,}$", _re.IGNORECASE)

        def _resolve_exp_id(raw_id: str) -> str:
            """Return a valid experiment id, or '' if unresolvable."""
            if not raw_id:
                return ""
            if raw_id in exp_set:
                return raw_id
            # If it's a hex hash the LLM made up, drop it.
            if _hex_re.match(raw_id):
                return ""
            # Fuzzy match: substring containment + prefix similarity.
            best, best_score = "", 0
            low = raw_id.lower()
            for eid in experiments:
                eid_low = eid.lower()
                # Substring containment (either direction).
                if low in eid_low or eid_low in low:
                    score = min(len(low), len(eid_low))
                    if score > best_score:
                        best, best_score = eid, score
                    continue
                # Prefix similarity: common prefix ≥ 70% of the longer string.
                common = 0
                max_check = min(len(low), len(eid_low))
                while common < max_check and low[common] == eid_low[common]:
                    common += 1
                longer = max(len(low), len(eid_low))
                if longer > 0 and common / longer >= 0.7 and common > best_score:
                    best, best_score = eid, common
            if not best:
                _log.warning(
                    "Experiment ID '%s' unresolvable; %d registered: %s",
                    raw_id, len(experiments),
                    ", ".join(experiments[:20]) or "(empty)",
                )
            return best

        impact_norm: list[dict[str, Any]] = []
        for im in parsed.get("impact", []):
            if not isinstance(im, dict):
                continue
            im.setdefault("study_or_experiment_id", im.get("id", ""))
            im.setdefault("impact", "")
            # Resolve the experiment id. Strip hex hashes the LLM made up.
            raw_eid = str(im.get("study_or_experiment_id", ""))
            resolved = _resolve_exp_id(raw_eid)
            im["study_or_experiment_id"] = resolved  # may be "" if unresolvable
            sa = im.get("suggested_action", "no_op")
            sp = im.get("suggested_params")
            if isinstance(sa, dict):
                sp_inner = sa.get("params")
                if isinstance(sp_inner, dict) and not isinstance(sp, dict):
                    sp = sp_inner
                sa = sa.get("action_type") or sa.get("type") or "no_op"
            if not isinstance(sa, str):
                sa = "no_op"
            im["suggested_action"] = sa
            im["suggested_params"] = sp if isinstance(sp, dict) else {}
            # Ensure suggested_params.experiment_id is also valid.
            if sa == "run_experiment" and isinstance(sp, dict):
                p_eid = str(sp.get("experiment_id", resolved or ""))
                final_eid = _resolve_exp_id(p_eid) or resolved
                sp["experiment_id"] = final_eid
                # If experiment_id is still empty after resolution,
                # downgrade to open_view so the button still appears
                # and navigates the user to the experiments page.
                if not final_eid:
                    im["suggested_action"] = "open_view"
                    im["suggested_params"] = {"view": "experiments", "experiment_id": p_eid}
                    im["impact"] = (
                        f"{im.get('impact', '')} "
                        f"[experiment '{p_eid}' not in registry]"
                    ).strip()
                    sa = "open_view"
            impact_norm.append(im)
        parsed["impact"] = impact_norm

        # Same validation for next_actions with run_experiment.
        for a in normalised:
            if a.get("action_type") == "run_experiment":
                p = a.get("params", {})
                if isinstance(p, dict):
                    eid = str(p.get("experiment_id", ""))
                    resolved_na = _resolve_exp_id(eid)
                    if resolved_na:
                        p["experiment_id"] = resolved_na
                    elif eid:
                        # Unresolvable — downgrade to open_view so button
                        # still appears and points user to the experiments page.
                        a["action_type"] = "open_view"
                        a["params"] = {"view": "experiments", "experiment_id": eid}
                        a["rationale"] = (
                            f"{a.get('rationale', '')} "
                            f"[experiment '{eid}' not in registry — open Experiments to find it]"
                        ).strip()
        parsed["next_actions"] = normalised

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
    project_id: str | None = Query(None),
) -> dict[str, Any]:
    """Aggregated dashboard payload.

    With ``include_ai=false`` (default) the response is fast: just the
    recent items, status/kind tallies, and basic counts. With
    ``include_ai=true`` the configured LLM is also called to produce a
    structured insight.

    Pass ``project_id`` to scope discovery items to the project's topics.
    """
    project = await _resolve_project(project_id)
    topic_ids = project.get("topic_ids") if project else None
    items = await _recent_discovery(limit=limit, days=days, topic_ids=topic_ids)
    studies: list[dict[str, Any]] = []
    db = get_db()
    if db is not None:
        try:
            studies = await db.list_studies()
        except Exception:  # noqa: BLE001
            studies = []
    exp_ids = _graph_experiment_ids()
    n_hypotheses = await _hypothesis_count()

    payload: dict[str, Any] = {
        "items": items,
        "n_items": len(items),
        "by_kind":   _tally(items, "kind"),
        "by_status": _tally(items, "status"),
        "by_topic":  _tally(items, "topic"),
        "by_source": _tally(items, "source"),
        "n_studies":     len(studies),
        "n_experiments": len(exp_ids),
        "n_hypotheses":  n_hypotheses,
        "since_days":    days,
        "project_id":    project["id"] if project else None,
    }

    if include_ai:
        payload["insight"] = await _generate_insight(items, studies, exp_ids, project=project)
    else:
        payload["insight"] = None  # frontend can request it lazily

    return payload


@router.post("/insight")
async def dashboard_insight(
    days: int = Query(14, ge=1, le=90),
    limit: int = Query(30, ge=1, le=200),
    project_id: str | None = Query(None),
) -> dict[str, Any]:
    """Force-regenerate the AI insight (always burns LLM tokens)."""
    project = await _resolve_project(project_id)
    topic_ids = project.get("topic_ids") if project else None
    items = await _recent_discovery(limit=limit, days=days, topic_ids=topic_ids)
    db = get_db()
    studies: list[dict[str, Any]] = []
    if db is not None:
        try:
            studies = await db.list_studies()
        except Exception:  # noqa: BLE001
            studies = []
    exp_ids = _graph_experiment_ids()
    return await _generate_insight(items, studies, exp_ids, project=project)


@router.get("/feed")
async def dashboard_feed(
    days: int = Query(14, ge=1, le=90),
    limit: int = Query(50, ge=1, le=200),
    project_id: str | None = Query(None),
) -> dict[str, Any]:
    """RSS-style flat feed for the dashboard timeline tile."""
    project = await _resolve_project(project_id)
    topic_ids = project.get("topic_ids") if project else None
    items = await _recent_discovery(limit=limit, days=days, topic_ids=topic_ids)
    return {
        "items": items,
        "n_items": len(items),
        "since_days": days,
        "project_id": project["id"] if project else None,
    }


__all__ = ["router"]
