"""Shutdown endpoint for tray/service integration."""

import os
import signal

from fastapi import APIRouter

router = APIRouter()


@router.post("/shutdown")
async def shutdown():
    """Request a clean backend shutdown.

    Sends SIGTERM to the current process, which triggers the
    lifespan shutdown sequence.
    """
    os.kill(os.getpid(), signal.SIGTERM)
    return {"status": "shutting_down"}
