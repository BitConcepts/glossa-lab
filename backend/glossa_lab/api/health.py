"""Health and status endpoints."""

import os
import time

from fastapi import APIRouter

from glossa_lab import __version__
from glossa_lab.auth import auth_mode

router = APIRouter()


@router.get("/health")
async def health():
    """Return health status, version, uptime, and served identity.

    Satisfies REQ-API-001.

    Leg C finding C-08: this endpoint previously returned only
    liveness (status/version/uptime), so a stale or wrong backend on
    the expected port passed every health check. It now also carries
    a served-identity stamp: the component name and a build id taken
    from the ``GLOSSA_BUILD_ID`` environment variable (set by launch
    tooling to the deployed commit/build stamp; ``"dev"`` when
    unset). Callers verifying a deployment must check ``component``
    and ``build``, not just ``status``.

    Spec 082 (C082-5): the payload also carries the auth mode word
    (``auth``: ``"token"`` when enforcing, ``"disabled"`` under the
    named ``GLOSSA_API_AUTH=off`` switch). The field set is pinned —
    identity and auth mode only, never any credential material.
    """
    from glossa_lab.main import get_start_time

    start = get_start_time()
    uptime = time.time() - start if start > 0 else 0.0

    return {
        "status": "healthy",
        "version": __version__,
        "uptime_seconds": round(uptime, 1),
        "component": "glossa-lab-backend",
        "build": os.environ.get("GLOSSA_BUILD_ID", "dev"),
        "auth": auth_mode(),
    }
