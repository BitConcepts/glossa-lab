"""AI Profiles API — reusable bundles of (backend + model + params).

A profile points at one of three backend kinds:
  cloud     → backend_ref is a cloud provider id (openai/anthropic/google/mistral)
  ollama    → backend_ref is the Ollama model name (kept here for symmetry)
  endpoint  → backend_ref is an ai_endpoints.id

Profiles can carry a `role` so the user can assign different defaults to
different tasks (chat, decipher, draft, research, ...). Setting
``is_default=true`` enforces a single default per role.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from glossa_lab.database import get_db

router = APIRouter(prefix="/api/v1/ai-profiles", tags=["ai-profiles"])

# ── Models ─────────────────────────────────────────────────────────────


class AIProfileCreate(BaseModel):
    name: str
    backend_kind: str = "cloud"
    backend_ref: str = ""
    model: str = ""
    params: dict[str, Any] = {}
    tags: list[str] = []
    is_default: bool = False
    role: str = ""
    notes: str = ""


class AIProfileUpdate(BaseModel):
    name: str | None = None
    backend_kind: str | None = None
    backend_ref: str | None = None
    model: str | None = None
    params: dict[str, Any] | None = None
    tags: list[str] | None = None
    is_default: bool | None = None
    role: str | None = None
    notes: str | None = None


# ── Roles served by the AI hub ─────────────────────────────────────────

# These line up with the AIToolsView capability groups so the profiles
# settings UI can offer per-role defaults.
KNOWN_ROLES: list[dict[str, str]] = [
    {"id": "",            "label": "Global default"},
    {"id": "chat",        "label": "Chat / Conversation"},
    {"id": "decipher",    "label": "Decipherment"},
    {"id": "sign_reading","label": "Sign reading"},
    {"id": "hypotheses",  "label": "Hypothesis generation"},
    {"id": "experiment_chain", "label": "Experiment planning"},
    {"id": "draft",       "label": "Paper drafting"},
    {"id": "synthesis",   "label": "Cross-study synthesis"},
    {"id": "report",      "label": "Report synthesis"},
    {"id": "discovery",   "label": "Discovery classification"},
]


# ── Routes ─────────────────────────────────────────────────────────────


@router.get("/roles")
async def list_roles() -> dict[str, Any]:
    return {"roles": KNOWN_ROLES}


@router.get("")
async def list_profiles(role: str | None = None) -> dict[str, Any]:
    db = get_db()
    if db is None:
        return {"profiles": []}
    rows = await db.list_ai_profiles(role=role)
    return {"profiles": rows}


@router.get("/default")
async def get_default(role: str = "") -> dict[str, Any]:
    db = get_db()
    if db is None:
        raise HTTPException(503, "Database not ready")
    row = await db.get_default_ai_profile(role=role)
    if row is None:
        return {"profile": None}
    return {"profile": row}


@router.post("")
async def create_profile(body: AIProfileCreate) -> dict[str, Any]:
    db = get_db()
    if db is None:
        raise HTTPException(503, "Database not ready")
    row = await db.create_ai_profile(
        name=body.name,
        backend_kind=body.backend_kind,
        backend_ref=body.backend_ref,
        model=body.model,
        params=body.params,
        tags=body.tags,
        is_default=body.is_default,
        role=body.role,
        notes=body.notes,
        created_at=datetime.now(timezone.utc).isoformat(),
    )
    return row


@router.get("/{pid}")
async def get_profile(pid: str) -> dict[str, Any]:
    db = get_db()
    if db is None:
        raise HTTPException(503, "Database not ready")
    row = await db.get_ai_profile(pid)
    if row is None:
        raise HTTPException(404, "Profile not found")
    return row


@router.patch("/{pid}")
async def update_profile(pid: str, body: AIProfileUpdate) -> dict[str, Any]:
    db = get_db()
    if db is None:
        raise HTTPException(503, "Database not ready")
    update = {k: v for k, v in body.model_dump(exclude_unset=True).items()}
    row = await db.update_ai_profile(pid, **update)
    if row is None:
        raise HTTPException(404, "Profile not found")
    return row


@router.delete("/{pid}")
async def delete_profile(pid: str) -> dict[str, Any]:
    db = get_db()
    if db is None:
        raise HTTPException(503, "Database not ready")
    row = await db.delete_ai_profile(pid)
    if row is None:
        raise HTTPException(404, "Profile not found")
    return {"deleted": True, "id": pid}


# ── Auto-suggest profiles ───────────────────────────────────────────────
# Inspect the user's actual installed models / configured cloud keys / saved
# AI endpoints, then propose a small bundle of role-tagged profiles. The user
# previews them in the UI and clicks Create on the ones they want — each
# preview round-trips through POST / above so audit + uniqueness are
# preserved.


# Maps a role to (params, notes) tuned for that task. ``temperature`` and
# ``max_tokens`` are held at sensible defaults for each role.
_ROLE_TUNING: dict[str, dict[str, Any]] = {
    "chat":             {"temperature": 0.7, "max_tokens": 1500,
                          "notes": "Conversational; balanced creativity."},
    "decipher":         {"temperature": 0.2, "max_tokens": 1200,
                          "notes": "Low temperature for repeatable decipherment proposals."},
    "sign_reading":     {"temperature": 0.3, "max_tokens": 800,
                          "notes": "Slightly creative for phonetic + semantic readings."},
    "hypotheses":       {"temperature": 0.6, "max_tokens": 1500,
                          "notes": "Moderate creativity for diverse hypothesis brainstorming."},
    "experiment_chain": {"temperature": 0.3, "max_tokens": 1500,
                          "notes": "Structured planning of multi-step experiment chains."},
    "draft":            {"temperature": 0.4, "max_tokens": 2500,
                          "notes": "Journal-quality writing; long context."},
    "synthesis":        {"temperature": 0.4, "max_tokens": 2500,
                          "notes": "Cross-study patterns + contradictions; long context."},
    "report":           {"temperature": 0.4, "max_tokens": 3000,
                          "notes": "Multi-report markdown synthesis."},
    "discovery":        {"temperature": 0.1, "max_tokens": 600,
                          "notes": "Strict JSON classification; low temperature."},
}


# Small priors so the suggester picks something reasonable when the user has
# multiple cloud keys: cheaper / faster providers fly to chat+discovery,
# stronger reasoning fly to decipher+hypotheses, long-context to draft.
_CLOUD_DEFAULT_MODELS: dict[str, dict[str, str]] = {
    "openai":    {"chat": "gpt-4o-mini",       "decipher": "gpt-4o",      "draft": "gpt-4o",       "discovery": "gpt-4o-mini"},
    "anthropic": {"chat": "claude-3-5-haiku",  "decipher": "claude-3-5-sonnet", "draft": "claude-3-5-sonnet", "discovery": "claude-3-5-haiku"},
    "google":    {"chat": "gemini-1.5-flash",  "decipher": "gemini-1.5-pro",   "draft": "gemini-1.5-pro",   "discovery": "gemini-1.5-flash"},
    "mistral":   {"chat": "mistral-small-latest", "decipher": "mistral-large-latest", "draft": "mistral-large-latest", "discovery": "mistral-small-latest"},
}


class SuggestedProfile(BaseModel):
    name: str
    backend_kind: str
    backend_ref: str
    model: str
    role: str
    params: dict[str, Any]
    tags: list[str]
    notes: str
    rationale: str  # human-readable why we suggested it


@router.post("/suggest")
async def suggest_profiles() -> dict[str, Any]:
    """Inspect available backends and propose ready-to-create profile bundles.

    The response is intentionally inert — nothing is persisted. The frontend
    shows previews; the user clicks Create on the ones they want, which
    POSTs back to the standard ``POST /ai-profiles`` endpoint.
    """
    from glossa_lab.api.settings import get_key  # noqa: PLC0415

    suggestions: list[SuggestedProfile] = []

    # ---- 1. Cloud providers (one role-tuned profile per available key) ----
    cloud_available: list[str] = []
    for prov in ("openai", "anthropic", "google", "mistral"):
        if get_key(f"{prov}_api_key"):
            cloud_available.append(prov)

    cloud_role_targets = [
        ("chat",      "Conversation"),
        ("decipher",  "Decipherment"),
        ("hypotheses","Hypothesis brainstorming"),
        ("draft",     "Paper drafting"),
        ("discovery", "Discovery classification"),
    ]

    for prov in cloud_available:
        defaults = _CLOUD_DEFAULT_MODELS.get(prov, {})
        for role, friendly in cloud_role_targets:
            model = defaults.get(role) or defaults.get("chat") or ""
            if not model:
                continue
            tuning = _ROLE_TUNING.get(role, {})
            suggestions.append(SuggestedProfile(
                name=f"{prov.title()} · {friendly}",
                backend_kind="cloud",
                backend_ref=prov,
                model=model,
                role=role,
                params={k: v for k, v in tuning.items() if k != "notes"},
                tags=["cloud", prov, role],
                notes=tuning.get("notes", ""),
                rationale=(
                    f"You have a {prov.title()} API key configured. "
                    f"{model} is a sensible default for {friendly.lower()}."
                ),
            ))

    # ---- 2. Ollama installed models ----
    try:
        from glossa_lab.ollama_lib import list_local_models  # noqa: PLC0415

        ollama_models = list_local_models() or []
    except Exception:  # noqa: BLE001
        ollama_models = []

    # Default-AI-stack: when Ollama has at least one model, propose the
    # "local-first" full role bundle (chat, decipher, drafting,
    # classification, hypotheses, sign-reading) all backed by the best
    # locally-installed model. The user can one-click "Create all" to wire
    # the whole stack at once.
    if ollama_models:
        # Pick the largest installed model as the heavyweight reasoner and
        # the smallest as the fast classifier. ``size_gb`` is provided by
        # ``list_local_models`` which mirrors ``ollama list``.
        sized = sorted(
            ((m.get("name") or "", float(m.get("size_gb") or 0)) for m in ollama_models),
            key=lambda t: t[1],
        )
        small = next((n for n, _ in sized if n), "")
        large = next((n for n, _ in reversed(sized) if n), small)
        if small and large:
            local_role_plan = [
                ("chat",         "Chat",          large, "Local conversation — your default chatter; data never leaves the box."),
                ("decipher",     "Decipherment",  large, "Heavyweight reasoning for low-temperature decipherment runs."),
                ("hypotheses",   "Hypotheses",    large, "Brainstorming hypotheses with the larger local model for better diversity."),
                ("sign_reading", "Sign reading",  large, "Phonetic + semantic sign reading; uses the larger local model for nuance."),
                ("draft",        "Drafting",      large, "Long-form journal-quality drafting locally; no cloud cost or rate-limits."),
                ("discovery",    "Mine classify", small, "Fast, low-temperature classifier for the Mine pipeline; small model is fine here."),
            ]
            for role, friendly, model_name, why in local_role_plan:
                tuning = _ROLE_TUNING.get(role, _ROLE_TUNING["chat"])
                suggestions.append(SuggestedProfile(
                    name=f"Local Default · {friendly}",
                    backend_kind="ollama",
                    backend_ref=model_name,
                    model=model_name,
                    role=role,
                    params={k: v for k, v in tuning.items() if k != "notes"},
                    tags=["ollama", "local", "default-stack", role],
                    notes=tuning.get("notes", ""),
                    rationale=why,
                ))
        # OCR is the one role that *cannot* run on plain text Ollama models;
        # if the Mistral key is present, surface a Mistral-Pixtral profile so
        # the local-first stack still has an OCR option.
        if get_key("mistral_api_key"):
            tuning = _ROLE_TUNING.get("sign_reading", _ROLE_TUNING["chat"])
            suggestions.append(SuggestedProfile(
                name="OCR · Mistral Pixtral",
                backend_kind="cloud",
                backend_ref="mistral",
                model="pixtral-12b-latest",
                role="sign_reading",
                params={k: v for k, v in tuning.items() if k != "notes"},
                tags=["cloud", "mistral", "ocr", "vision"],
                notes="Vision OCR via Mistral pixtral-12b. Required for tablet image OCR.",
                rationale=(
                    "Ollama doesn't ship a tablet-OCR-quality vision model out "
                    "of the box. Mistral pixtral-12b is the recommended OCR "
                    "backend and your Mistral key is configured."
                ),
            ))

    # ---- 3. Custom AI endpoints (one profile per saved enabled endpoint) ----
    db = get_db()
    if db is not None:
        try:
            endpoints = await db.list_ai_endpoints(enabled_only=True)
        except Exception:  # noqa: BLE001
            endpoints = []
        for ep in endpoints[:6]:  # cap at 6 to keep the dialog tidy
            ep_id   = ep.get("id")
            ep_name = ep.get("name") or ep_id
            default_model = ep.get("default_model") or ""
            if not ep_id or not default_model:
                continue
            tuning = _ROLE_TUNING["chat"]
            suggestions.append(SuggestedProfile(
                name=f"{ep_name} · Chat",
                backend_kind="endpoint",
                backend_ref=ep_id,
                model=default_model,
                role="chat",
                params={k: v for k, v in tuning.items() if k != "notes"},
                tags=["endpoint", "custom", "chat"],
                notes=tuning.get("notes", ""),
                rationale=(
                    f"Custom endpoint '{ep_name}' is enabled. Default model "
                    f"{default_model} can serve chat without depending on "
                    "a cloud account."
                ),
            ))

    if not suggestions:
        return {
            "profiles": [],
            "message": (
                "No backends detected yet. Configure at least one cloud API key "
                "in Settings, install an Ollama model, or save a custom "
                "AI endpoint, then click Suggest again."
            ),
            "available": {"cloud": [], "ollama": 0, "endpoints": 0},
        }

    return {
        "profiles": [p.model_dump() for p in suggestions],
        "message": f"Found {len(suggestions)} suggestion(s).",
        "available": {
            "cloud":     cloud_available,
            "ollama":    len(ollama_models),
            "endpoints": len(suggestions) - (
                len(cloud_available) * len(cloud_role_targets)
            ) - (1 if ollama_models else 0),
        },
    }
