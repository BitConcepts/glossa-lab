"""Privacy / data-handling statement endpoint (Spec 084, T011).

Serves the owner-approved privacy statement — the text carried in
``glossa_lab.privacy_statement`` and fixtured as the single source
of truth under Spec 084. Like every route except the health
readout, this one sits behind the install-token gate (Spec 082);
the statement itself says the health readout is the only thing the
program answers without the token, and this route keeps that true.
"""

from fastapi import APIRouter

from glossa_lab.privacy_statement import PRIVACY_STATEMENT

router = APIRouter()


@router.get("/privacy")
async def privacy_statement() -> dict[str, str]:
    """Return the approved privacy / data-handling statement text."""
    return {"text": PRIVACY_STATEMENT}
