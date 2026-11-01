"""Cloud-edition workspace scope enforcement (Spec 083, Step 2 — T018/T019/T023).

Container side of the two-axis access model (Amendment 1). The edge
Worker owns identity and injects it on every container-bound request
(``cloud/edge/README.md`` — the header contract):

* ``X-Glossa-Service-Credential`` — the per-deployment edge↔container
  service credential (FR-008), on every container-bound request;
* ``X-Glossa-User-Id`` / ``X-Glossa-User-Name`` / ``X-Glossa-Global-Type``
  — the authenticated actor (authenticated requests only);
* ``X-Glossa-Workspace-Roles`` — JSON object mapping workspace slug →
  role (``owner`` / ``admin`` / ``member`` / ``viewer``). Role keys may
  also be project ids in practice; resolution accepts both and maps
  them through the projects table.

The tenancy unit is the existing ``projects`` entity (a workspace).
A project's workspace slug is its ``slug`` column when set, else
derived: the seeded primary workspace is ``indus-script``; any other
project's slug is the slugified label (falling back to its id).

Enforcement (cloud mode only — this middleware is installed only when
``GLOSSA_CLOUD=1`` and desktop behaviour is unchanged):

* A request under ``/api/`` (health excepted) whose service-credential
  header does not match ``GLOSSA_SERVICE_CREDENTIAL`` is refused
  **401** — in the cloud topology the container is never directly
  reachable, and this check is the enforcement of that. The check
  engages when the credential is configured; a request that carries
  any ``X-Glossa-*`` header is always scope-checked even on a local
  production-shaped build where the secret is not configured, and a
  request with no edge headers at all on such a build is left alone
  (the Phase 1 surface tests exercise the app that way).
* An ``/api/`` request with a valid credential but no actor identity
  is anonymous: **401**. (The edge forwards anonymous pass-through
  only for the public pages/assets, which are not under ``/api/``.)
* Workspace-scoped requests resolve their target workspace (see
  :func:`_resolve_workspace` for the per-class rules) and then:
  read = any effective role (Viewer suffices) or global Owner/Admin
  (implicit Workspace Admin); write = Member/Admin/Owner role or
  global Owner/Admin. Anything else answers a **scoped 404** whose
  body is exactly ``{"detail": "Not found"}`` — no name, no count,
  no data — indistinguishable from a nonexistent workspace. (A
  Viewer's write therefore answers 404 rather than the amendment's
  403; the Step 2 tasking permits 404/405 for Viewer writes and the
  uniform scoped 404 leaks less.)
* Guests are capped at Viewer per workspace (Amendment 1), whatever
  the roles map says.
* The terminal surface (D-5) requires global Owner/Admin in cloud
  mode: anyone else gets **403** with the response marker header
  ``X-Glossa-Denial: terminal-admin-only`` for the edge audit log.
* Workspace materialization: a scoped request naming a slug the edge
  has authorized (present in the roles map, or the actor is a global
  Owner/Admin) but with no local project yet creates the project
  record idempotently, stamped as created via cloud — so edge-side
  workspace creation (D1) and container content stay in step without
  a synchronous cross-call.

Per-resource-class coverage (T019) — honest about the data model:

===================  =====================================================
claims, digestion,   The on-disk evidence store belongs to the primary
evidence             workspace (Spec 081 ``_program_scope`` semantics:
                     ``indus_decipherment`` owns the store; every other
                     program's register is honestly empty). The shim
                     routes under ``/indus-evidence`` and the scoped
                     routes under ``/programs/{id}`` are therefore
                     workspace-resolved, as are hypotheses/library.
anchors/data         ``anchor_sets`` and ``texts`` carry **no**
                     project linkage in the current model → global
                     class (see below). Corpus/catalogue/signs likewise.
studies              ``studies`` carries no project_id → global class.
experiments          Projects link experiments (``experiment_ids``),
                     so a named experiment resolves to the project
                     that links it; unlinked experiments are global.
jobs                 ``jobs`` carries no project_id and its params do
                     not reliably name one → global class.
discovery            A discovery item's ``topic`` maps to a project
                     via ``project_for_topic``; items/topics that map
                     resolve to that workspace, the rest are global.
research-loop        ``research_loop_state`` is a singleton with no
                     project linkage → global class.
notebooks            ``notebooks.project_id`` — fully scoped,
                     including list filtering and id probing.
reports              Report files carry no project linkage → global.
(hypotheses,         ``project_id`` columns — fully scoped like
citations,           notebooks.
correspondences)
===================  =====================================================

"Global class" is the strongest honest scoping the model supports:
the route requires an authenticated actor, and a mutating request
additionally requires a write-capable role *somewhere* (any non-Viewer
workspace role, or global Owner/Admin) — a Viewer-only or Guest actor
cannot mutate global-class resources. The gap is recorded here, not
papered over: these classes gain true workspace scope when their
records gain a project linkage.
"""

from __future__ import annotations

import hmac
import json
import os
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

PRIMARY_WORKSPACE_SLUG = "indus-script"
_PRIMARY_PROJECT_ID = "indus_decipherment"
_SERVICE_CREDENTIAL_ENV = "GLOSSA_SERVICE_CREDENTIAL"

GLOBAL_ADMIN_TYPES = ("owner", "admin")
WRITE_ROLES = ("owner", "admin", "member")
READ_ROLES = ("owner", "admin", "member", "viewer")
_ROLE_RANK = {"viewer": 1, "member": 2, "admin": 3, "owner": 4}

DESKTOP_IMPORT_LABEL = "via desktop import"


# ── Slugs ────────────────────────────────────────────────────────────


def slugify(text: str) -> str:
    """Slugify a label/id: lowercase, non-alphanumerics → single '-'."""
    slug = re.sub(r"[^a-z0-9]+", "-", (text or "").strip().lower()).strip("-")
    return slug or "workspace"


def project_slug(project: dict[str, Any] | None) -> str:
    """Return the workspace slug for a project record.

    An explicit ``slug`` field wins. The seeded primary project
    (id ``indus_decipherment``, or a project literally named
    "Indus Script") is ``indus-script``. Anything else slugifies its
    label, falling back to its id.
    """
    if not project:
        return PRIMARY_WORKSPACE_SLUG
    explicit = (project.get("slug") or "").strip()
    if explicit:
        return explicit
    if project.get("id") == _PRIMARY_PROJECT_ID or (
        (project.get("label") or "").strip().lower() == "indus script"
    ):
        return PRIMARY_WORKSPACE_SLUG
    return slugify(project.get("label") or project.get("id") or "")


# ── Actor context ────────────────────────────────────────────────────


@dataclass
class Actor:
    """The request-scoped actor parsed from the edge headers."""

    user_id: str
    username: str = ""
    global_type: str = "member"
    workspace_roles: dict[str, str] = field(default_factory=dict)

    @property
    def is_global_admin(self) -> bool:
        return self.global_type in GLOBAL_ADMIN_TYPES

    def role_for(self, slug: str, project_id: str | None = None) -> str | None:
        """Effective per-workspace role for *slug* (Guest-capped).

        Global Owner/Admin hold implicit Workspace Admin everywhere.
        Role-map keys may be slugs or project ids; both are consulted.
        """
        if self.is_global_admin:
            return "admin"
        role = self.workspace_roles.get(slug)
        if role is None and project_id:
            role = self.workspace_roles.get(project_id)
        if role is None:
            return None
        role = role.lower()
        if role not in _ROLE_RANK:
            return None
        if self.global_type == "guest" and _ROLE_RANK[role] > _ROLE_RANK["viewer"]:
            role = "viewer"  # Amendment 1: Guests hold Viewer only.
        return role

    def can_read(self, slug: str, project_id: str | None = None) -> bool:
        return self.role_for(slug, project_id) in READ_ROLES

    def can_write(self, slug: str, project_id: str | None = None) -> bool:
        return self.role_for(slug, project_id) in WRITE_ROLES

    def has_any_write_role(self) -> bool:
        """True when the actor may mutate global-class resources."""
        if self.is_global_admin:
            return True
        return any(
            self.role_for(slug) in WRITE_ROLES for slug in list(self.workspace_roles)
        )

    def stamp(self) -> dict[str, Any]:
        """The attribution stamp for a mutating act (T023)."""
        return {
            "user_id": self.user_id,
            "username": self.username,
            "at": datetime.now(timezone.utc).isoformat(),
            "via": "cloud",
        }


def parse_actor_headers(headers: Any) -> Actor | None:
    """Build an :class:`Actor` from edge headers, or None if anonymous."""
    user_id = (headers.get("x-glossa-user-id") or "").strip()
    if not user_id:
        return None
    roles: dict[str, str] = {}
    raw_roles = headers.get("x-glossa-workspace-roles") or ""
    if raw_roles:
        try:
            parsed = json.loads(raw_roles)
            if isinstance(parsed, dict):
                roles = {str(k): str(v).lower() for k, v in parsed.items()}
        except (json.JSONDecodeError, ValueError):
            roles = {}
    return Actor(
        user_id=user_id,
        username=(headers.get("x-glossa-user-name") or "").strip(),
        global_type=(headers.get("x-glossa-global-type") or "member").strip().lower(),
        workspace_roles=roles,
    )


def actor_from_scope(scope: dict) -> Actor | None:
    """Return the actor the middleware stashed on the ASGI scope."""
    state = scope.get("state") or {}
    actor = state.get("actor")
    return actor if isinstance(actor, Actor) else None


def actor_from_request(request: Any) -> Actor | None:
    """Return the actor for a FastAPI ``Request`` (None on desktop)."""
    try:
        actor = request.state.actor
    except Exception:  # noqa: BLE001 — no actor stashed (desktop mode)
        return None
    return actor if isinstance(actor, Actor) else None


# ── Attribution (T023) ───────────────────────────────────────────────


def attribution_label(record: dict[str, Any] | None) -> str:
    """Render a record's actor: the cloud username, or the import label.

    Records with no cloud actor (bundle-imported / desktop-created)
    are labelled ``"via desktop import"`` — the label is computed at
    serialization time; stored data is never rewritten for it.
    """
    if record:
        for key in ("created_by", "modified_by"):
            stamp = record.get(key)
            if isinstance(stamp, dict) and stamp.get("user_id"):
                return stamp.get("username") or stamp["user_id"]
            if isinstance(stamp, str) and stamp.strip():
                return stamp
    return DESKTOP_IMPORT_LABEL


def decorate_attribution(record: dict[str, Any]) -> dict[str, Any]:
    """Return a copy of *record* with ``attribution_label`` added."""
    out = dict(record)
    out["attribution_label"] = attribution_label(record)
    return out


# ── Responses ────────────────────────────────────────────────────────

_SCOPED_404_BODY = b'{"detail":"Not found"}'


async def _send_json(send: Any, status: int, body: bytes,
                     extra_headers: list | None = None) -> None:
    headers = [
        (b"content-type", b"application/json"),
        (b"content-length", str(len(body)).encode()),
    ]
    if extra_headers:
        headers.extend(extra_headers)
    await send({"type": "http.response.start", "status": status, "headers": headers})
    await send({"type": "http.response.body", "body": body})


# ── Middleware ───────────────────────────────────────────────────────

_PUBLIC_API_PATHS = {"/api/v1/health"}

# GET list endpoints whose JSON rows are filtered by workspace scope
# before they leave the container (no leakage through lists/counts).
_FILTER_LIST_PATHS = {
    "/api/v1/projects",
    "/api/v1/notebooks",
    "/api/v1/hypotheses",
    "/api/v1/citations",
    "/api/v1/correspondences",
    "/api/v1/discovery/items",
}

# Path prefixes that are deployment-global facilities, not workspace
# data: they require an authenticated actor (and, for the terminal,
# a global admin — handled separately) but no workspace resolution.
_GLOBAL_PREFIXES = (
    "/api/v1/health",
    "/api/v1/settings",
    "/api/v1/notifications",
    "/api/v1/providers",
    "/api/v1/ai-endpoints",
    "/api/v1/ai-profiles",
    "/api/v1/model-assignments",
    "/api/v1/model-intelligence",
    "/api/v1/node-registry",
    "/api/v1/dashboard",
    "/api/v1/events",
    "/api/v1/system",
    "/api/v1/ollama",
)


class CloudScopeMiddleware:
    """Pure-ASGI workspace-scope enforcement (cloud mode only).

    Installed by ``create_app`` only when ``GLOSSA_CLOUD=1``. See the
    module docstring for the enforcement contract and the honest
    per-class coverage table.
    """

    def __init__(self, app: Any) -> None:
        self.app = app

    async def __call__(self, scope: dict, receive: Any, send: Any) -> None:
        if scope.get("type") != "http":
            await self.app(scope, receive, send)
            return

        from starlette.datastructures import Headers  # noqa: PLC0415

        headers = Headers(scope=scope)
        path: str = scope.get("path", "")
        method: str = scope.get("method", "GET").upper()
        expected_credential = os.environ.get(_SERVICE_CREDENTIAL_ENV, "").strip()
        carries_edge_headers = any(
            key.startswith("x-glossa-") for key in headers
        )

        # Engagement rule (see module docstring): with no credential
        # configured and no edge headers present there is no edge in
        # front of this process — leave the request untouched.
        if not expected_credential and not carries_edge_headers:
            await self.app(scope, receive, send)
            return

        is_api = path.startswith("/api/")

        # ── Service credential (FR-008): the container is never
        # directly reachable in the cloud topology.
        if is_api and path not in _PUBLIC_API_PATHS:
            presented = headers.get("x-glossa-service-credential", "")
            if expected_credential and not hmac.compare_digest(
                presented, expected_credential
            ):
                await _send_json(
                    send, 401, b'{"detail":"service credential required"}'
                )
                return

        actor = parse_actor_headers(headers)
        scope.setdefault("state", {})["actor"] = actor

        if is_api and path not in _PUBLIC_API_PATHS:
            if actor is None:
                await _send_json(
                    send, 401, b'{"detail":"authentication required"}'
                )
                return

            # ── Terminal gating (D-5): global Owner/Admin only.
            if path.startswith("/api/v1/terminal"):
                if not actor.is_global_admin:
                    await _send_json(
                        send,
                        403,
                        b'{"detail":"terminal is restricted to global admins"}',
                        extra_headers=[
                            (b"x-glossa-denial", b"terminal-admin-only")
                        ],
                    )
                    return
                await self.app(scope, receive, send)
                return

            # Read (and replay) the body once for scope resolution on
            # mutating requests that name their workspace in the body.
            body = b""
            if method in ("POST", "PUT", "PATCH", "DELETE"):
                body = await _read_body(receive)
                receive = _replay_receive(body)

            verdict = await self._authorize(scope, actor, path, method, body)
            if verdict == "scoped-404":
                await _send_json(send, 404, _SCOPED_404_BODY)
                return
            if verdict == "filter-list":
                await self._call_with_list_filter(scope, receive, send, actor)
                return

        await self.app(scope, receive, send)

    # ── Authorization ────────────────────────────────────────────────

    async def _authorize(
        self, scope: dict, actor: Actor, path: str, method: str, body: bytes
    ) -> str:
        """Return "ok", "scoped-404", or "filter-list"."""
        is_write = method not in ("GET", "HEAD", "OPTIONS")
        segments = [seg for seg in path.split("/") if seg != ""]

        if any(path.startswith(prefix) for prefix in _GLOBAL_PREFIXES):
            return self._global_verdict(actor, is_write)

        resolution = await self._resolve_workspace(scope, segments, body)
        if resolution is None:
            # No workspace could be resolved: a global-class route.
            if method == "GET" and path in _FILTER_LIST_PATHS:
                return "filter-list"
            return self._global_verdict(actor, is_write)

        slug, project_id = resolution
        if is_write:
            allowed = actor.can_write(slug, project_id)
        else:
            allowed = actor.can_read(slug, project_id)
        if not allowed:
            return "scoped-404"
        await self._materialize(actor, slug, project_id)
        return "ok"

    @staticmethod
    def _global_verdict(actor: Actor, is_write: bool) -> str:
        if is_write and not actor.has_any_write_role():
            return "scoped-404"
        return "ok"

    # ── Workspace resolution ─────────────────────────────────────────

    async def _resolve_workspace(
        self, scope: dict, segments: list[str], body: bytes
    ) -> tuple[str, str | None] | None:
        """Resolve the target workspace as (slug, project_id|None).

        Returns None when the route is a global class (no workspace
        linkage in the data model — see the module docstring).
        """
        from glossa_lab.database import get_db  # noqa: PLC0415

        db = get_db()
        query = scope.get("query_string", b"").decode("latin-1")
        from urllib.parse import parse_qs  # noqa: PLC0415

        params = {k: v[0] for k, v in parse_qs(query).items() if v}

        async def by_project_id(project_id: str) -> tuple[str, str]:
            project = None
            if db is not None:
                project = await db.get_project(project_id)
                if project is None:
                    project = await self._project_by_slug(db, project_id)
            if project is not None:
                return project_slug(project), project["id"]
            # Unknown id: treat the id itself as the slug candidate so
            # an entitled actor can materialize it and an unentitled
            # one gets the scoped 404 (never the project's data).
            return slugify(project_id.replace("_", "-")), project_id

        # /api/v1/programs/{program_id}/…  (Spec 081 scoped router)
        if len(segments) >= 4 and segments[:3] == ["api", "v1", "programs"]:
            return await by_project_id(segments[3])

        if len(segments) >= 3 and segments[:2] == ["api", "v1"]:
            resource = segments[2]

            # The evidence store (claims / digestion / evidence) is the
            # primary workspace's store (Spec 081 semantics).
            if resource == "indus-evidence":
                return PRIMARY_WORKSPACE_SLUG, _PRIMARY_PROJECT_ID

            if resource == "projects":
                if len(segments) == 3:
                    return None  # list — response-filtered instead
                target = segments[3]
                if target == "active":
                    if db is not None:
                        active = await db.get_active_project()
                        if active is not None:
                            return project_slug(active), active["id"]
                    return PRIMARY_WORKSPACE_SLUG, _PRIMARY_PROJECT_ID
                if target == "import":
                    return None  # creates a new project — global write
                return await by_project_id(target)

            if resource in ("notebooks", "hypotheses", "citations",
                            "correspondences"):
                return await self._resolve_record_class(
                    db, resource, segments, params, body
                )

            if resource == "discovery":
                return await self._resolve_discovery(db, segments, params)

            if resource == "experiments" and len(segments) >= 4:
                experiment_id = segments[3]
                if db is not None:
                    for project in await db.list_projects():
                        if experiment_id in (project.get("experiment_ids") or []):
                            return project_slug(project), project["id"]
                return None

        # Workspace named in the query string or JSON body.
        for key in ("project_id", "program_id"):
            if params.get(key):
                return await by_project_id(params[key])
        if body:
            try:
                payload = json.loads(body)
            except (json.JSONDecodeError, ValueError):
                payload = None
            if isinstance(payload, dict):
                for key in ("project_id", "program_id"):
                    if payload.get(key):
                        return await by_project_id(str(payload[key]))
                slug_value = payload.get("workspace_slug") or payload.get("workspace")
                if slug_value:
                    return slugify(str(slug_value)), None
        return None

    async def _resolve_record_class(
        self, db: Any, resource: str, segments: list[str],
        params: dict, body: bytes,
    ) -> tuple[str, str | None] | None:
        """notebooks/hypotheses/citations/correspondences: project_id-scoped."""
        getters = {
            "notebooks": "get_notebook",
            "hypotheses": "get_hypothesis",
            "citations": "get_citation",
            "correspondences": "get_correspondence",
        }
        # Single-record routes: the record's own project_id is the scope.
        if len(segments) >= 4 and db is not None:
            getter = getattr(db, getters[resource], None)
            if getter is not None:
                record = await getter(segments[3])
                if record is not None:
                    project_id = record.get("project_id") or ""
                    if project_id:
                        project = await db.get_project(project_id)
                        return (
                            project_slug(project) if project else slugify(project_id),
                            project_id,
                        )
                    return None  # unscoped (global) record
                return None  # missing record — the handler's own 404 stands
        # Collection routes: a named project_id in query/body is the scope.
        named = params.get("project_id")
        if not named and body:
            try:
                payload = json.loads(body)
                if isinstance(payload, dict):
                    named = payload.get("project_id")
            except (json.JSONDecodeError, ValueError):
                named = None
        if named:
            project = await db.get_project(str(named)) if db is not None else None
            return (
                project_slug(project) if project else slugify(str(named)),
                str(named),
            )
        return None  # unscoped list/create — list is response-filtered

    async def _resolve_discovery(
        self, db: Any, segments: list[str], params: dict
    ) -> tuple[str, str | None] | None:
        """Discovery: an item's topic maps to a project when one claims it."""
        if db is None:
            return None
        topic = params.get("topic")
        if len(segments) >= 5 and segments[3] == "items":
            item = await db.get_discovery_item(segments[4])
            if item is not None:
                topic = item.get("topic") or topic
        if topic:
            project = await db.project_for_topic(topic)
            if project is not None:
                return project_slug(project), project["id"]
        return None

    # ── Materialization ──────────────────────────────────────────────

    @staticmethod
    async def _project_by_slug(db: Any, slug: str) -> dict | None:
        for project in await db.list_projects():
            if project_slug(project) == slug:
                return project
        return None

    async def _materialize(
        self, actor: Actor, slug: str, project_id: str | None
    ) -> None:
        """Create the local project for an authorized slug, idempotently.

        Only entitled actors reach this point (authorization ran
        first), so materialization never creates a workspace for a
        non-member. The record is stamped as created via cloud with
        the acting user's attribution.
        """
        from glossa_lab.database import get_db  # noqa: PLC0415

        db = get_db()
        if db is None:
            return
        if project_id and await db.get_project(project_id) is not None:
            return
        if await self._project_by_slug(db, slug) is not None:
            return
        now = datetime.now(timezone.utc).isoformat()
        label = slug.replace("-", " ").title()
        await db.upsert_project(
            project_id=project_id or slug,
            label=label,
            description="",
            prompt_context="",
            topic_ids=[],
            experiment_ids=[],
            corpus_ids=[],
            is_active=False,
            created_at=now,
            slug=slug,
            created_by=actor.stamp(),
        )

    # ── List filtering (leak prevention through lists/counts) ───────

    async def _call_with_list_filter(
        self, scope: dict, receive: Any, send: Any, actor: Actor
    ) -> None:
        from glossa_lab.database import get_db  # noqa: PLC0415

        db = get_db()
        projects = await db.list_projects() if db is not None else []
        slug_by_project_id = {p["id"]: project_slug(p) for p in projects}
        topic_slugs: dict[str, str] = {}
        for project in projects:
            for topic in project.get("topic_ids") or []:
                topic_slugs.setdefault(topic, project_slug(project))

        def entitled_project(project_id: str) -> bool:
            if not project_id:
                return True  # unscoped/global record — global class rule
            slug = slug_by_project_id.get(project_id)
            if slug is None:
                return False
            return actor.can_read(slug, project_id)

        captured: dict[str, Any] = {}

        async def capture_send(message: dict) -> None:
            if message["type"] == "http.response.start":
                captured["start"] = message
                return
            if message["type"] == "http.response.body":
                captured.setdefault("body", b"")
                captured["body"] += message.get("body", b"")
                if message.get("more_body"):
                    return
                start = captured.get("start")
                body = captured["body"]
                if start is not None and start["status"] == 200:
                    body = _filter_list_body(
                        scope["path"], body, actor, entitled_project,
                        slug_by_project_id, topic_slugs,
                    )
                    headers = [
                        (k, v) for k, v in start["headers"]
                        if k.lower() != b"content-length"
                    ]
                    headers.append(
                        (b"content-length", str(len(body)).encode())
                    )
                    start = {**start, "headers": headers}
                if start is not None:
                    await send(start)
                await send({"type": "http.response.body", "body": body})
                return
            await send(message)

        await self.app(scope, receive, capture_send)


def _filter_list_body(
    path: str, body: bytes, actor: Actor, entitled_project: Any,
    slug_by_project_id: dict, topic_slugs: dict,
) -> bytes:
    """Drop rows the actor is not entitled to from a JSON list body."""
    try:
        payload = json.loads(body)
    except (json.JSONDecodeError, ValueError):
        return body
    try:
        if path == "/api/v1/projects" and isinstance(payload, list):
            kept = [
                row for row in payload
                if isinstance(row, dict)
                and actor.can_read(project_slug(row), row.get("id"))
            ]
            return json.dumps(kept).encode()
        if path == "/api/v1/discovery/items":
            rows = payload.get("items") if isinstance(payload, dict) else payload
            if isinstance(rows, list):
                kept = []
                for row in rows:
                    if not isinstance(row, dict):
                        continue
                    slug = topic_slugs.get(row.get("topic") or "")
                    if slug is None or actor.can_read(slug):
                        kept.append(row)
                if isinstance(payload, dict):
                    payload = {**payload, "items": kept}
                    if "total" in payload:
                        payload["total"] = len(kept)
                    return json.dumps(payload).encode()
                return json.dumps(kept).encode()
            return body
        if isinstance(payload, list):
            kept = [
                row for row in payload
                if not isinstance(row, dict)
                or entitled_project(row.get("project_id") or "")
            ]
            return json.dumps(kept).encode()
        if isinstance(payload, dict):
            for key in ("items", "notebooks", "hypotheses", "citations",
                        "correspondences", "documents"):
                rows = payload.get(key)
                if isinstance(rows, list):
                    kept = [
                        row for row in rows
                        if not isinstance(row, dict)
                        or entitled_project(row.get("project_id") or "")
                    ]
                    payload = {**payload, key: kept}
                    if "total" in payload:
                        payload["total"] = len(kept)
                    return json.dumps(payload).encode()
    except Exception:  # noqa: BLE001 — filtering must never corrupt a response
        return body
    return body


# ── Body helpers ─────────────────────────────────────────────────────


async def _read_body(receive: Any) -> bytes:
    body = b""
    while True:
        message = await receive()
        if message["type"] == "http.request":
            body += message.get("body", b"")
            if not message.get("more_body"):
                break
        elif message["type"] == "http.disconnect":
            break
    return body


def _replay_receive(body: bytes) -> Any:
    delivered = False

    async def replay() -> dict:
        nonlocal delivered
        if not delivered:
            delivered = True
            return {"type": "http.request", "body": body, "more_body": False}
        return {"type": "http.disconnect"}

    return replay
