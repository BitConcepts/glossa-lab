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

import asyncio
import json
import logging
import re
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

# JSON Schema for vLLM guided_json — forces the model to output exactly this
# structure at the token level (no wrong keys, no missing fields).
_INSIGHT_JSON_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "highlights": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "title": {"type": "string"},
                    "why_it_matters": {"type": "string"},
                },
                "required": ["id", "title", "why_it_matters"],
            },
        },
        "what_it_means": {"type": "string"},
        "impact": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "study_or_experiment_id": {"type": "string"},
                    "name": {"type": "string"},
                    "impact": {"type": "string"},
                    "suggested_action": {"type": "string"},
                    "suggested_params": {"type": "object"},
                },
                "required": ["study_or_experiment_id", "name", "impact",
                             "suggested_action"],
            },
        },
        "next_actions": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "label": {"type": "string"},
                    "action_type": {"type": "string"},
                    "params": {"type": "object"},
                    "rationale": {"type": "string"},
                },
                "required": ["label", "action_type", "params", "rationale"],
            },
        },
    },
    "required": ["highlights", "what_it_means", "impact", "next_actions"],
}

_INSIGHT_PROMPT_TEMPLATE = (
    "You are a {goal_label} research assistant. Given the most recent\n"
    "discovery items the user has captured, produce a JSON object with\n"
    "EXACTLY this structure (no other keys):\n\n"
    '{{\n'
    '  "highlights": [\n'
    '    {{"id": "<item_id>", "title": "<title>", "why_it_matters": "<1 sentence>"}}\n'
    '  ],\n'
    '  "what_it_means": "<2-3 sentence narrative>",\n'
    '  "impact": [\n'
    '    {{"study_or_experiment_id": "<EXACT id from list below>",\n'
    '      "name": "<label>", "impact": "<1 sentence>",\n'
    '      "suggested_action": "run_experiment",\n'
    '      "suggested_params": {{"experiment_id": "<same id>"}} }}\n'
    '  ],\n'
    '  "next_actions": [\n'
    '    {{"label": "<button text>", "action_type": "<type>",\n'
    '      "params": {{}}, "rationale": "<why>"}}\n'
    '  ]\n'
    '}}\n\n'
    "RULES:\n"
    "- highlights: pick the 3 most consequential items from the list below.\n"
    "- impact: study_or_experiment_id MUST appear VERBATIM in the experiment\n"
    "  or study lists below. NEVER invent or abbreviate an id.\n"
    "- next_actions: 3-5 executable suggestions.\n"
    "- action_type is one of: run_experiment, open_view, run_fetch, run_mine,\n"
    "  create_hypothesis, propose_experiment_chain, ai_chat, no_op.\n"
    "- params is always a JSON object (use {{}} when empty).\n"
    "- Be concise. Keep each string under 120 chars.\n"
    "- Return ONLY the JSON object. No markdown, no explanation."
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


def _try_repair_json(text: str) -> dict[str, Any] | None:
    """Try to repair truncated JSON by closing open brackets/braces.

    Returns the parsed dict if successful, None otherwise.
    """
    # Only attempt if the text starts with { (valid JSON object start)
    stripped = text.strip()
    if not stripped.startswith("{"):
        return None
    # Count unclosed brackets and braces
    # Walk the string tracking nesting, ignoring chars inside strings
    in_string = False
    escape = False
    stack: list[str] = []
    for ch in stripped:
        if escape:
            escape = False
            continue
        if ch == "\\" and in_string:
            escape = True
            continue
        if ch == '"' and not escape:
            in_string = not in_string
            continue
        if in_string:
            continue
        if ch in ("{", "["):
            stack.append(ch)
        elif ch == "}" and stack and stack[-1] == "{":
            stack.pop()
        elif ch == "]" and stack and stack[-1] == "[":
            stack.pop()
    if not stack:
        return None  # Already balanced — the error is something else
    # Close everything that's still open (in reverse order)
    # First, close any dangling string or value
    suffix = ""
    for bracket in reversed(stack):
        if bracket == "[":
            suffix += "]"
        elif bracket == "{":
            suffix += "}"
    # Try a few repair strategies
    for trim in ("", ","):
        # Trim trailing comma or partial value before closing
        candidate = stripped.rstrip()
        if trim and candidate.endswith(trim):
            candidate = candidate[:-len(trim)]
        # Also strip a trailing incomplete string (open quote without close)
        if candidate.count('"') % 2 != 0:
            # Remove chars back to the last complete key-value boundary
            last_comma = candidate.rfind(",")
            last_brace = max(candidate.rfind("{"), candidate.rfind("["))
            cut = max(last_comma, last_brace)
            if cut > 0:
                candidate = candidate[:cut + 1]
        candidate += suffix
        try:
            return json.loads(candidate)
        except (json.JSONDecodeError, ValueError):
            continue
    return None


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

        _log.info("dashboard insight: calling LLM (json_mode=True, %d items)", len(items))
        loop = asyncio.get_event_loop()
        raw = ""

        # ── Attempt 1: reasoning bucket with full JSON schema ────────────
        try:
            raw = await loop.run_in_executor(
                None,
                lambda: call_llm(
                    [
                        {
                            "role": "system",
                            "content": (
                                "/no_think\n"
                                "You produce concise structured JSON for a research dashboard. "
                                "Output ONLY a JSON object with keys: highlights, what_it_means, impact, next_actions. "
                                "No other keys. No markdown. No explanation. "
                                "Keep each string value under 120 characters. Be brief."
                            ),
                        },
                        {"role": "user", "content": prompt},
                    ],
                    bucket="reasoning",
                    json_mode=True,
                    json_schema=_INSIGHT_JSON_SCHEMA,
                    max_tokens=2000, temperature=0.2,
                ),
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
        except Exception as exc:  # noqa: BLE001 — RuntimeError or other LLM error
            _log.info(
                "dashboard insight: reasoning bucket failed (%s), trying conversational",
                type(exc).__name__,
            )

        # ── Attempt 2: conversational bucket, no json_schema (wider compat) ─
        if not raw or not raw.strip():
            try:
                raw = await loop.run_in_executor(
                    None,
                    lambda: call_llm(
                        [
                            {"role": "system", "content": (
                                "/no_think\n"
                                "Output ONLY a JSON object with exactly these keys: "
                                "highlights (array), what_it_means (string), "
                                "impact (array), next_actions (array). "
                                "No markdown. No explanation. Max 120 chars per value."
                            )},
                            {"role": "user", "content": prompt},
                        ],
                        bucket="conversational",
                        json_mode=True,
                        max_tokens=1800, temperature=0.3,
                    ),
                )
            except Exception as conv_exc:  # noqa: BLE001
                _log.info("dashboard insight: conversational bucket failed (%s)", type(conv_exc).__name__)

        # ── Attempt 3: reasoning bucket, shorter prompt, no schema ──────
        if not raw or not raw.strip():
            short_items = items[:8]  # minimal context to reduce token pressure
            short_prompt = _build_insight_prompt(short_items, studies[:5], experiments[:20], goal=goal)
            try:
                raw = await loop.run_in_executor(
                    None,
                    lambda: call_llm(
                        [
                            {"role": "system", "content": (
                                "/no_think\n"
                                "Return a JSON object: {\"highlights\":[],\"what_it_means\":\"\","
                                "\"impact\":[],\"next_actions\":[]}"
                            )},
                            {"role": "user", "content": short_prompt},
                        ],
                        bucket="reasoning",
                        json_mode=True,
                        max_tokens=1200, temperature=0.2,
                    ),
                )
            except Exception as s_exc:  # noqa: BLE001
                _log.info("dashboard insight: short-prompt attempt failed (%s)", type(s_exc).__name__)

        # Guard against empty / whitespace-only LLM responses.
        if not raw or not raw.strip():
            _log.warning(
                "dashboard insight LLM returned empty response after 3 attempts "
                "(reasoning → conversational → short-prompt)"
            )
            return {
                "highlights": [],
                "what_it_means": (
                    "Insight generation returned empty after 3 attempts \u2014 "
                    "the LLM provider may be overloaded or the model assignments may "
                    "not be configured. Try Auto-Configure in Settings \u2192 AI, "
                    "then click Regenerate."
                ),
                "impact": [],
                "next_actions": [
                    {"label": "Auto-Configure AI", "action_type": "open_view",
                     "params": {"view": "settings", "tab": "ai"},
                     "rationale": "Re-run auto-configure to assign the best available model."},
                ],
                "model": "empty-fallback",
            }
        _log.info("dashboard insight: got %d chars from LLM", len(raw))
        # Strip Qwen3-style <think>...</think> reasoning prefix.
        cleaned = raw.strip()
        think_match = re.search(r"</think>\s*", cleaned)
        if think_match:
            cleaned = cleaned[think_match.end():].strip()
        # Strip any stray code fences before json-loading.
        if cleaned.startswith("```"):
            cleaned = cleaned.split("```", 2)[1] if "```" in cleaned[3:] else cleaned[3:]
            if cleaned.lower().startswith("json"):
                cleaned = cleaned[4:].lstrip()
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
        try:
            parsed = json.loads(cleaned)
        except json.JSONDecodeError as jde:
            # Attempt repair: if the JSON was truncated (max_tokens hit),
            # close any open brackets/braces so json.loads can succeed.
            repaired = _try_repair_json(cleaned)
            if repaired is not None:
                _log.info("dashboard insight: repaired truncated JSON (%d chars)", len(cleaned))
                parsed = repaired
            else:
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
        # Reject effectively-empty responses (model outputting minimal
        # schema to satisfy guided_json without actually analyzing).
        if (
            not parsed.get("highlights")
            and not parsed.get("what_it_means", "").strip()
            and not parsed.get("next_actions")
        ):
            _log.warning(
                "dashboard insight: LLM returned empty schema (%d chars). "
                "Falling back to heuristic.", len(raw),
            )
            raise RuntimeError("LLM returned empty insight schema")
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
        # Phase F: Add AI metadata for output badges
        parsed["_ai_meta"] = {
            "bucket": "reasoning",
            "is_fallback": False,
        }
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


@router.get("/decipherment")
async def dashboard_decipherment() -> dict[str, Any]:
    """Indus script decipherment progress metrics.

    Returns the latest round results, anchor counts, confidence scores,
    and progression history from all V5-V17 report files.  This powers
    the "Decipherment Progress" panel on the dashboard.
    """
    import glob  # noqa: PLC0415
    from pathlib import Path  # noqa: PLC0415

    reports_dir = Path(__file__).resolve().parent.parent.parent / "reports"
    if not reports_dir.is_dir():
        return {"available": False, "reason": "No reports directory"}

    # Load the final anchor set
    final_path = reports_dir / "INDUS_FINAL_ANCHORS.json"
    anchors_summary: dict[str, Any] = {"total": 0}
    if final_path.exists():
        try:
            data = json.loads(final_path.read_text(encoding="utf-8"))
            total = data.get("total", 0)
            by_conf: dict[str, int] = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
            for _s, info in (data.get("anchors") or {}).items():
                c = (info.get("confidence") or "LOW").upper()
                by_conf[c] = by_conf.get(c, 0) + 1
            anchors_summary = {"total": total, "by_confidence": by_conf}
        except Exception:  # noqa: BLE001
            pass

    # Collect round progression from V8-V17 reports
    progression: list[dict[str, Any]] = []
    round_files = sorted(reports_dir.glob("INDUS_V*_ROUND*.json"))
    for rf in round_files:
        try:
            rd = json.loads(rf.read_text(encoding="utf-8"))
            r = rd.get("round", {})
            c = r.get("confidence", {})
            progression.append({
                "round": r.get("round"),
                "version": rd.get("title", ""),
                "level": r.get("level", ""),
                "weighted_pct": c.get("weighted_pct", 0),
                "signs_assigned": c.get("assigned", {}).get("total", 0),
                "signs_total": c.get("total_signs", 390),
                "token_coverage": c.get("token_cov", {}).get("total", 0),
                "fully_decoded_pct": c.get("fully_decoded_pct", 0),
                "tamil_brahmi_corr": r.get("tamil_brahmi", {}).get("correlation", 0),
                "remaining": r.get("remaining", []),
            })
        except Exception:  # noqa: BLE001
            continue

    # Latest state from V5/V6/V7 reports
    latest: dict[str, Any] = {}
    for fn in ["INDUS_V7_FULL_PUSH.json", "INDUS_V6_PMI_ANCHORS.json", "INDUS_V5_PHASES_1_3.json"]:
        p = reports_dir / fn
        if p.exists():
            try:
                latest[fn.replace(".json", "")] = json.loads(p.read_text(encoding="utf-8")).get("timestamp", "")
            except Exception:  # noqa: BLE001
                pass

    return {
        "available": True,
        "anchors": anchors_summary,
        "progression": progression,
        "n_rounds": len(progression),
        "latest_reports": latest,
        "current_state": progression[-1] if progression else None,
    }


__all__ = ["router"]
