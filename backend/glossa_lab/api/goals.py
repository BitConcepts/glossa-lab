"""Research Goals API — CRUD for multi-project research goals.

Each goal scopes a set of discovery topics, links to studies, and provides
a prompt_context string injected into the LLM system prompt during mine
classification and dashboard insight generation.

Endpoints (mounted at ``/api/v1/goals``):
* ``GET /``           — list all goals
* ``GET /{id}``       — get one
* ``PUT /{id}``       — create or update
* ``DELETE /{id}``    — delete
* ``GET /default``    — get the default goal
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from glossa_lab.database import get_db

router = APIRouter(prefix="/api/v1/goals", tags=["goals"])


class GoalBody(BaseModel):
    label: str
    description: str = ""
    prompt_context: str = ""
    topic_ids: list[str] = []
    study_ids: list[str] = []
    is_default: bool = False


@router.get("")
async def list_goals() -> list[dict[str, Any]]:
    db = get_db()
    if db is None:
        raise HTTPException(503, "Database not ready")
    return await db.list_goals()


@router.get("/default")
async def get_default_goal() -> dict[str, Any]:
    db = get_db()
    if db is None:
        raise HTTPException(503, "Database not ready")
    goal = await db.get_default_goal()
    if goal is None:
        raise HTTPException(404, "No goals configured")
    return goal


@router.get("/{goal_id}")
async def get_goal(goal_id: str) -> dict[str, Any]:
    db = get_db()
    if db is None:
        raise HTTPException(503, "Database not ready")
    goal = await db.get_goal(goal_id)
    if goal is None:
        raise HTTPException(404, f"Goal {goal_id} not found")
    return goal


@router.put("/{goal_id}")
async def upsert_goal(goal_id: str, body: GoalBody) -> dict[str, Any]:
    db = get_db()
    if db is None:
        raise HTTPException(503, "Database not ready")
    now = datetime.now(timezone.utc).isoformat()
    return await db.upsert_goal(
        goal_id=goal_id,
        label=body.label,
        description=body.description,
        prompt_context=body.prompt_context,
        topic_ids=body.topic_ids,
        study_ids=body.study_ids,
        is_default=body.is_default,
        created_at=now,
    )


@router.delete("/{goal_id}")
async def delete_goal(goal_id: str) -> dict[str, Any]:
    db = get_db()
    if db is None:
        raise HTTPException(503, "Database not ready")
    deleted = await db.delete_goal(goal_id)
    if deleted is None:
        raise HTTPException(404, f"Goal {goal_id} not found")
    return {"deleted": True, "goal": deleted}
