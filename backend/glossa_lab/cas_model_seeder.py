"""Seed built-in CAS-YAML constraint models into the cas_models DB table.

Idempotent — uses INSERT OR REPLACE so re-running overwrites existing
built-in models but preserves user-created ones (is_builtin=0).
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from pathlib import Path

from glossa_lab.database import Database

_log = logging.getLogger("glossa_lab.cas_model_seeder")

_MODELS_DIR = Path(__file__).resolve().parent / "data" / "cas_models"


async def seed_cas_models(db: Database) -> None:
    """Read all .yaml files from data/cas_models/ and upsert into DB."""
    if not _MODELS_DIR.exists():
        _log.debug("No cas_models directory at %s, skipping.", _MODELS_DIR)
        return

    try:
        import yaml  # noqa: PLC0415
    except ImportError:
        _log.warning("PyYAML not installed — cannot seed CAS models.")
        return

    now = datetime.now(timezone.utc).isoformat()
    count = 0

    for p in sorted(_MODELS_DIR.glob("*.yaml")):
        try:
            raw_text = p.read_text("utf-8")
            parsed = yaml.safe_load(raw_text)
            model_id = str(parsed.get("model_id", p.stem))
            name = str(parsed.get("description", p.stem))[:200]
            description = str(parsed.get("description", ""))

            await db.create_cas_model(
                name=name,
                description=description,
                yaml_text=raw_text,
                engine_hint=str(parsed.get("projection", {}).get("strategy", "auto")
                              if isinstance(parsed.get("projection"), dict)
                              else "auto"),
                is_builtin=True,
                created_at=now,
                model_id=model_id,
            )
            count += 1
        except Exception as exc:  # noqa: BLE001
            _log.warning("Failed to seed CAS model %s: %s", p.name, exc)

    _log.info("Seeded %d built-in CAS model(s) from %s", count, _MODELS_DIR)
