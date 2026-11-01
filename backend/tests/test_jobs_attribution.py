"""Spec 083 Step 3 (T027): jobs carry the cloud actor stamp.

The Jobs screen's "Started by" line reads job.attribution_label,
which exists only in cloud mode and is computed from the created_by
stamp written at creation (schema v27). Desktop mode never carries
the label; unstamped jobs render the honest "via desktop import"
fallback in cloud mode.
"""

import asyncio
import json
import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from glossa_lab.config import get_settings
from glossa_lab.database import Database

SERVICE_CREDENTIAL = "test-service-credential-083"


def _member_headers() -> dict[str, str]:
    return {
        "X-Glossa-Service-Credential": SERVICE_CREDENTIAL,
        "X-Glossa-User-Id": "u-member",
        "X-Glossa-User-Name": "alice",
        "X-Glossa-Global-Type": "member",
        "X-Glossa-Workspace-Roles": json.dumps({"indus-script": "member"}),
    }


def test_create_job_stamp_roundtrip(tmp_path: Path):
    """The stamp is stored as JSON and read back as a dict; absent → ''."""

    async def _run():
        db = Database(tmp_path / "jobs.db")
        await db.connect()
        stamp = {"user_id": "u-member", "username": "alice", "via": "cloud"}
        job = await db.create_job(
            name="stamped",
            created_at="2026-10-31T00:00:00+00:00",
            created_by=stamp,
        )
        assert job["created_by"] == stamp
        bare = await db.create_job(
            name="unstamped", created_at="2026-10-31T00:00:00+00:00"
        )
        assert bare["created_by"] in ("", None)
        await db.close()

    asyncio.run(_run())


def test_desktop_mode_has_no_attribution_label(client):
    """The plain desktop app never invents a starter for a job."""
    created = client.post("/api/v1/jobs", json={"name": "desktop-job"})
    assert created.status_code == 201
    body = created.json()
    assert body["attribution_label"] is None
    assert body["created_by"] in ("", None)


@pytest.fixture(scope="module")
def cloud_client(tmp_path_factory):
    data_dir = tmp_path_factory.mktemp("glossa083jobs") / "data"
    saved = {
        key: os.environ.get(key)
        for key in ("GLOSSA_CLOUD", "GLOSSA_SERVICE_CREDENTIAL", "GLOSSA_DATA_DIR")
    }
    from glossa_lab import database as _database

    saved_db = _database.get_db()
    os.environ["GLOSSA_CLOUD"] = "1"
    os.environ["GLOSSA_SERVICE_CREDENTIAL"] = SERVICE_CREDENTIAL
    os.environ["GLOSSA_DATA_DIR"] = str(data_dir)
    get_settings.cache_clear()
    from glossa_lab.main import create_app

    with TestClient(create_app()) as client:
        yield client
    for key, value in saved.items():
        if value is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = value
    get_settings.cache_clear()
    _database._db = saved_db


def test_cloud_mode_stamps_the_acting_user(cloud_client):
    created = cloud_client.post(
        "/api/v1/jobs", json={"name": "cloud-job"}, headers=_member_headers()
    )
    assert created.status_code == 201
    body = created.json()
    assert body["attribution_label"] == "alice"
    assert body["created_by"]["username"] == "alice"

    listed = cloud_client.get("/api/v1/jobs", headers=_member_headers()).json()
    mine = [j for j in listed if j["id"] == body["id"]]
    assert mine and mine[0]["attribution_label"] == "alice"
