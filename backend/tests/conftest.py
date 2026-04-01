"""Shared test fixtures."""

import pytest
from fastapi.testclient import TestClient

from glossa_lab.main import create_app


@pytest.fixture(scope="session")
def app():
    """Create the FastAPI app once per test session."""
    return create_app()


@pytest.fixture(scope="session")
def client(app):
    """TestClient with lifespan properly entered (database initialised)."""
    with TestClient(app) as c:
        yield c
