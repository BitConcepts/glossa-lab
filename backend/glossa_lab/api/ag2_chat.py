"""AG2 Research Agent API endpoint.

POST /api/v1/ag2/chat         — SSE streaming AG2 research conversation
GET  /api/v1/ag2/status       — AG2 availability (Ollama + model info)
GET  /api/v1/ag2/tools        — List of available research tools
"""
from __future__ import annotations

import json
from typing import Any

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

router = APIRouter()


class AG2ChatRequest(BaseModel):
    message: str
    history: list[dict[str, str]] = []
    context_type: str = ""
    context_id: str = ""


@router.get("/ag2/status")
async def ag2_status() -> dict[str, Any]:
    """Return AG2 availability: Ollama connection and active model."""
    try:
        from glossa_lab.ag2_agent import _get_llm_config  # noqa: PLC0415
        cfg = _get_llm_config()
        if cfg:
            return {
                "available": True,
                "model": cfg["config_list"][0]["model"],
                "base_url": cfg["config_list"][0]["base_url"],
                "mode": "llm_enabled",
                "tools": ["list_experiments", "run_experiment", "read_result",
                          "query_corpus", "read_ledger"],
            }
        return {
            "available": True,
            "model": None,
            "mode": "tool_only",
            "note": "Ollama not reachable — AG2 runs in tool-only mode (no LLM reasoning)",
            "tools": ["list_experiments", "run_experiment", "read_result",
                      "query_corpus", "read_ledger"],
        }
    except Exception as exc:  # noqa: BLE001
        return {"available": False, "error": str(exc)}


@router.get("/ag2/tools")
async def ag2_tools() -> list[dict[str, str]]:
    """List tools available to the AG2 research agent."""
    try:
        from glossa_lab.ag2_agent import _TOOLS  # noqa: PLC0415
        return [{"name": name, "description": desc} for name, (_, desc) in _TOOLS.items()]
    except Exception as exc:  # noqa: BLE001
        return [{"name": "error", "description": str(exc)}]


@router.post("/ag2/chat")
async def ag2_chat(req: AG2ChatRequest) -> StreamingResponse:
    """SSE streaming AG2 research conversation.

    Each SSE event is a JSON object:
      {"type": "agent_start"|"tool_call"|"tool_result"|"message"|"error"|"done",
       "agent": str, "content": str}
    """
    async def _generate():
        try:
            from glossa_lab.ag2_agent import run_ag2_chat  # noqa: PLC0415
            async for event in run_ag2_chat(
                message=req.message,
                history=req.history,
                context_type=req.context_type,
                context_id=req.context_id,
            ):
                yield f"data: {json.dumps(event)}\n\n"
        except Exception as exc:  # noqa: BLE001
            yield f"data: {json.dumps({'type':'error','agent':'system','content':str(exc)})}\n\n"
        finally:
            yield f"data: {json.dumps({'type':'done','agent':'system','content':''})}\n\n"

    return StreamingResponse(
        _generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )
